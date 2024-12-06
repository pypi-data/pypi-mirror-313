import asyncio
from contextlib import asynccontextmanager
from enum import Enum, auto
from typing import Dict, Set

from mas.logger import get_logger
from mas.protocol import Message

from .interfaces import ITransport

logger = get_logger()


class ServiceState(Enum):
    """Transport service states."""

    INITIALIZED = auto()
    RUNNING = auto()
    SHUTTING_DOWN = auto()
    SHUTDOWN = auto()


class TransportService:
    """
    Transport service facade that manages message routing and subscription state.
    Does not directly manage transport connections.
    """

    def __init__(self, transport: ITransport):
        self.transport = transport
        self._state = ServiceState.INITIALIZED
        self._state_lock = asyncio.Lock()

        # Track subscriptions by subscriber_id
        self._subscriptions: Dict[
            str, Set[str]
        ] = {}  # subscriber_id -> set of channels
        self._subscription_lock = asyncio.Lock()

    @property
    def state(self) -> ServiceState:
        """Current service state."""
        return self._state

    async def _set_state(self, new_state: ServiceState) -> None:
        """Thread-safe state transition."""
        async with self._state_lock:
            self._state = new_state
            logger.debug(f"Transport service state changed to {new_state.name}")

    async def subscribe(self, subscriber_id: str, channel: str) -> None:
        """
        Register a subscription for a subscriber.

        Args:
            subscriber_id: ID of the subscribing entity
            channel: Channel to subscribe to
        """
        if self._state != ServiceState.RUNNING:
            raise RuntimeError("Transport service not running")

        async with self._subscription_lock:
            if subscriber_id not in self._subscriptions:
                self._subscriptions[subscriber_id] = set()

            if channel in self._subscriptions[subscriber_id]:
                raise RuntimeError(f"Already subscribed to channel: {channel}")

            try:
                # Let the transport layer handle the actual subscription
                await self.transport.subscribe(channel)
                self._subscriptions[subscriber_id].add(channel)
                logger.debug(f"Subscriber {subscriber_id} subscribed to {channel}")
            except Exception as e:
                logger.error(f"Failed to subscribe {subscriber_id} to {channel}: {e}")
                raise

    async def unsubscribe(self, subscriber_id: str, channel: str) -> None:
        """
        Remove a subscription for a subscriber.

        Args:
            subscriber_id: ID of the subscribing entity
            channel: Channel to unsubscribe from
        """
        async with self._subscription_lock:
            if subscriber_id in self._subscriptions:
                if channel in self._subscriptions[subscriber_id]:
                    try:
                        await self.transport.unsubscribe(channel)
                        self._subscriptions[subscriber_id].remove(channel)
                        logger.debug(
                            f"Subscriber {subscriber_id} unsubscribed from {channel}"
                        )

                        # Clean up subscriber entry if no more subscriptions
                        if not self._subscriptions[subscriber_id]:
                            del self._subscriptions[subscriber_id]
                    except Exception as e:
                        logger.error(
                            f"Failed to unsubscribe {subscriber_id} from {channel}: {e}"
                        )
                        raise

    async def send_message(self, message: Message) -> None:
        """
        Send a message through the transport layer.

        Args:
            message: Message to send
        """
        if self._state != ServiceState.RUNNING:
            raise RuntimeError("Transport service not running")

        try:
            await self.transport.publish(message)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise

    @asynccontextmanager
    async def message_stream(self, subscriber_id: str, channel: str):
        """
        Context manager for receiving messages on a channel.

        Args:
            subscriber_id: ID of the subscribing entity
            channel: Channel to receive messages from
        """

        try:
            message_stream = self.transport.subscribe(channel)
            yield message_stream
        finally:
            await self.unsubscribe(subscriber_id, channel)

    async def start(self) -> None:
        """Start the transport service."""
        if self._state != ServiceState.INITIALIZED:
            return

        try:
            await self.transport.initialize()
            await self._set_state(ServiceState.RUNNING)
        except Exception as e:
            logger.error(f"Failed to start transport service: {e}")
            raise

    async def stop(self) -> None:
        """
        Stop the transport service.
        Waits for all subscribers to unsubscribe before stopping.
        """
        if self._state != ServiceState.RUNNING:
            return

        await self._set_state(ServiceState.SHUTTING_DOWN)

        # Wait for all subscribers to clean up their subscriptions
        while self._subscriptions:
            await asyncio.sleep(0.1)

        # Let the transport layer handle its own cleanup
        await self.transport.cleanup()
        await self._set_state(ServiceState.SHUTDOWN)
