import asyncio
import signal
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncIterator, Dict, Optional, Type

from mas.logger import get_logger
from mas.persistence.interfaces import IPersistenceProvider
from mas.persistence.memory import InMemoryProvider
from mas.protocol import Message, MessageType
from mas.transport.redis import RedisTransport
from mas.transport.service import TransportService

from .discovery.service import DiscoveryService


class ShutdownManager:
    """Handles system shutdown signals (Ctrl+C, SIGTERM)."""

    def __init__(self):
        self.event = asyncio.Event()

    def _handle_signal(self, signum, frame) -> None:
        # When Ctrl+C is pressed, this gets called
        logger.info(f"Received shutdown signal {signum}")
        # Sets the event, which will wake up anyone waiting on event.wait()
        self.event.set()

    def __enter__(self):
        # When entering 'with' block, set up signal handlers
        self._original_sigint = signal.signal(signal.SIGINT, self._handle_signal)
        self._original_sigterm = signal.signal(signal.SIGTERM, self._handle_signal)
        return self

    def __exit__(self, *args):
        # When exiting 'with' block, restore original signal handlers
        signal.signal(signal.SIGINT, self._original_sigint)
        signal.signal(signal.SIGTERM, self._original_sigterm)


logger = get_logger()


class MAS:
    """Multi-Agent System (MAS) service."""

    def __init__(
        self,
        transport: TransportService,
        persistence: IPersistenceProvider,
    ) -> None:
        self._transport = transport
        self._persistence = persistence
        self._discovery = DiscoveryService(persistence)
        self._sender_id: str = "core"
        self._running = False
        self._message_handler: Optional[asyncio.Task] = None
        self._handlers: Dict[MessageType, Any] = {
            MessageType.STATUS_UPDATE: self._handle_status_update,
            MessageType.DISCOVERY_REQUEST: self._handle_discovery,
            MessageType.REGISTRATION_REQUEST: self._handle_registration,
        }

    async def start(self) -> None:
        """Start MAS."""
        if self._running:
            return

        logger.info("Starting MAS...")
        try:
            # Initialize services in order
            await self._persistence.initialize()
            await self._transport.start()
            await self._discovery.initialize()

            # Start message handling
            self._message_handler = asyncio.create_task(
                self._handle_messages(),
                name="core_message_handler",
            )
            self._running = True
            logger.info("MAS started successfully")

        except Exception as e:
            logger.error(f"Failed to start MAS: {e}")
            await self.stop()  # Cleanup any partially initialized services
            raise

    async def stop(self) -> None:
        """Stop MAS in a controlled manner."""
        if not self._running:
            return

        logger.info("Stopping MAS...")
        self._running = False

        try:
            # Cancel message handler
            if self._message_handler:
                self._message_handler.cancel()
                try:
                    await self._message_handler
                except asyncio.CancelledError:
                    pass

            # Cleanup services in reverse order
            await self._discovery.cleanup()
            await self._persistence.cleanup()
            await self._transport.stop()

            logger.info("MAS stopped successfully")

        except Exception as e:
            logger.error(f"Error during MAS shutdown: {e}")
            raise

    async def _handle_messages(self) -> None:
        """Handle incoming core messages."""
        try:
            async with self._transport.message_stream(
                self._sender_id,
                self._sender_id,
            ) as stream:
                async for message in stream:
                    if not self._running:
                        break

                    try:
                        await self._process_message(message)
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                        await self._send_error_response(message, str(e))
        except Exception as e:
            if self._running:
                logger.error(f"MAS message handler failed: {e}")
                raise

    async def _process_message(self, message: Message) -> None:
        """Process an incoming message."""
        if handler := self._handlers.get(message.message_type):
            try:
                await handler(message)
            except Exception as e:
                logger.error(
                    f"Handler failed for message type {message.message_type}: {e}"
                )
                await self._send_error_response(message, str(e))
        else:
            logger.warning(f"No handler for message type: {message.message_type}")

    async def _send_error_response(self, original_message: Message, error: str) -> None:
        """Send error response for a failed message."""
        try:
            await self._transport.send_message(
                Message(
                    sender_id=self._sender_id,
                    target_id=original_message.sender_id,
                    message_type=MessageType.ERROR,
                    payload={
                        "error": error,
                        "original_message_type": original_message.message_type,
                    },
                )
            )
        except Exception as e:
            logger.error(f"Failed to send error response: {e}")

    async def _handle_registration(self, message: Message) -> None:
        """Handle agent registration."""
        try:
            token = await self._discovery.register_agent(
                agent_id=message.sender_id,
                capabilities=set(message.payload["capabilities"]),
            )
            await self._send_success_response(
                message,
                MessageType.REGISTRATION_RESPONSE,
                {"token": token},
            )
        except Exception as e:
            await self._send_error_response(message, str(e))

    async def _handle_discovery(self, message: Message) -> None:
        """Handle agent discovery request."""
        try:
            capabilities = set(message.payload.get("capabilities", []))
            agents = await self._discovery.find_agents(capabilities)
            await self._send_success_response(
                message, MessageType.DISCOVERY_RESPONSE, {"agents": agents}
            )
        except Exception as e:
            await self._send_error_response(message, str(e))

    async def _handle_status_update(self, message: Message) -> None:
        """Handle agent status update."""
        try:
            await self._discovery.update_status(
                status=message.payload["status"],
                agent_id=message.sender_id,
            )
            await self._send_success_response(
                message, MessageType.STATUS_UPDATE_RESPONSE, {}
            )
        except Exception as e:
            await self._send_error_response(message, str(e))

    async def _send_success_response(
        self,
        original_message: Message,
        response_type: MessageType,
        payload: Dict[str, Any],
    ) -> None:
        """Send a success response."""
        payload["status"] = "success"
        await self._transport.send_message(
            Message(
                sender_id=self._sender_id,
                target_id=original_message.sender_id,
                message_type=response_type,
                payload=payload,
            )
        )


@dataclass(frozen=True)
class MASContext:
    mas: MAS
    transport: TransportService
    persistence: IPersistenceProvider


@asynccontextmanager
async def mas_service(
    provider: Type[IPersistenceProvider] = InMemoryProvider,
) -> AsyncIterator[MASContext]:
    """Run the MAS service until shutdown signal is received or context exits."""

    # Create all our services
    transport = TransportService(transport=RedisTransport())
    storage = provider()
    mas = MAS(transport, storage)

    # Create our shutdown handler
    shutdown = ShutdownManager()

    # Set up signal handling
    with shutdown:
        try:
            # Start the service
            await mas.start()

            # Give control back to the caller until they're done
            # or until a shutdown signal is received
            yield MASContext(mas, transport, storage)

            # Only wait for shutdown signal if one was received while running
            if not shutdown.event.is_set():
                logger.info("Shutdown signal received, stopping MAS")

        finally:
            # Always stop the service, whether we got a signal
            # or the caller finished naturally
            await mas.stop()
