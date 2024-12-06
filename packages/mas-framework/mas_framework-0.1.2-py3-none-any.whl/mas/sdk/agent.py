import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel

from mas.logger import get_logger
from mas.persistence.interfaces import IPersistenceProvider
from mas.protocol import Message, MessageType
from mas.transport.service import TransportService

logger = get_logger()


class AgentConfig(BaseModel):
    """Configuration for an agent."""

    agent_id: str
    metadata: Dict[str, Any]
    capabilities: Set[str]


class Agent(ABC):
    """Enhanced agent implementation with lifecycle management."""

    def __init__(
        self,
        config: AgentConfig,
        transport: TransportService,
        persistence: IPersistenceProvider,
    ):
        self.id = config.agent_id
        self.capabilities = config.capabilities
        self.metadata = config.metadata

        self.transport = transport
        self.persistence = persistence
        self._running = False
        self._registered = False
        self._health_check_interval = 30  # seconds
        self._tasks: List[asyncio.Task] = []
        self._token: Optional[str] = None
        self._authenticated: bool = False
        self._message_streams: List[asyncio.Task] = []

    async def initialize(self) -> None:
        """Initialize agent and register with core service."""
        logger.debug(f"Agent {self.id} initializing...")
        try:
            # Register with core service
            await self._register_with_core()

            # Initialize custom agent logic
            await self._initialize()

        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise RuntimeError(f"Failed to initialize agent: {e}")

    async def start(self) -> None:
        """Start the agent and its background tasks."""
        if self._running:
            return

        await self.initialize()
        self._running = True

        # Start message streams with proper subscription management
        core_stream = asyncio.create_task(self._manage_core_messages())
        agent_stream = asyncio.create_task(self._manage_agent_messages())
        health_check = asyncio.create_task(self._health_check_loop())

        self._message_streams = [core_stream, agent_stream]
        self._tasks = [*self._message_streams, health_check]

        logger.debug(f"Agent {self.id} started")

    async def stop(self) -> None:
        """Gracefully stop the agent."""
        if not self._running:
            return

        self._running = False

        # Cancel all tasks
        for task in self._tasks:
            task.cancel()

        # Wait for tasks to complete
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)

        # Custom cleanup
        await self._cleanup()

        # Deregister from core
        await self._deregister_from_core()
        logger.debug(f"Agent {self.id} stopped")

    async def send_message(
        self,
        target_id: str,
        content: Dict[str, Any],
        message_type: MessageType = MessageType.AGENT_MESSAGE,
    ) -> None:
        """Send message to another agent."""
        if not self._running:
            raise RuntimeError("Agent is not running")

        message = Message(
            payload=content,
            sender_id=self.id,
            target_id=target_id,
            message_type=message_type,
        )

        try:
            await self.transport.send_message(message)
            logger.debug(f"Agent {self.id} sent message to {target_id}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise

    async def _manage_core_messages(self) -> None:
        """Manage core message subscription and processing."""
        try:
            async with self.transport.message_stream(self.id, "core") as stream:
                async for message in stream:
                    if not self._running:
                        break
                    try:
                        msg = Message.model_validate(message)
                        if msg.sender_id == "core" and msg.target_id == self.id:
                            await self._handle_core_message(msg)
                    except Exception as e:
                        await self._handle_error(
                            f"Error processing core message: {e}", message
                        )
        except Exception as e:
            if self._running:  # Only log if not shutting down
                await self._handle_error(f"Core message stream failed: {e}")

    async def _manage_agent_messages(self) -> None:
        """Manage agent-specific message subscription and processing."""
        try:
            async with self.transport.message_stream(self.id, self.id) as stream:
                async for message in stream:
                    if not self._running:
                        break
                    try:
                        await self._handle_agent_message(message)
                    except Exception as e:
                        await self._handle_error(
                            f"Error processing agent message: {e}", message
                        )
        except Exception as e:
            if self._running:  # Only log if not shutting down
                await self._handle_error(f"Agent message stream failed: {e}")

    async def _register_with_core(self) -> None:
        """Register agent with the core service."""
        message = Message(
            sender_id=self.id,
            target_id="core",
            message_type=MessageType.REGISTRATION_REQUEST,
            payload={
                "metadata": self.metadata,
                "capabilities": list(self.capabilities),
            },
        )
        await self.transport.send_message(message)

    async def _health_check_loop(self) -> None:
        """Periodic health check and status update."""
        while self._running:
            try:
                await self.transport.send_message(
                    Message(
                        sender_id=self.id,
                        target_id="core",
                        message_type=MessageType.STATUS_UPDATE,
                        payload={"status": "active"},
                    )
                )
                await asyncio.sleep(self._health_check_interval)
            except Exception as e:
                if self._running:
                    await self._handle_error(f"Health check failed: {e}")

    async def _initialize(self) -> None:
        """Initialize agent-specific logic."""
        pass

    async def _cleanup(self) -> None:
        """Cleanup agent-specific resources."""
        pass

    @abstractmethod
    async def _handle_agent_message(self, message: Message) -> None:
        """Handle agent-specific messages. To be implemented by child classes."""
        pass

    async def _handle_error(
        self,
        error: str,
        message: Optional[Message] = None,
    ) -> None:
        """Handle errors during agent operation."""
        # Log error
        logger.error(f"Agent {self.id} error: {error}")

        if message:
            # Notify sender of failure if applicable
            error_message = Message(
                sender_id=self.id,
                target_id=message.sender_id,
                message_type=MessageType.ERROR,
                payload={"error": str(error), "original_message_id": str(message.id)},
            )
            await self.transport.send_message(error_message)

    async def _deregister_from_core(self) -> None:
        """Deregister agent from core service."""
        if self._registered:
            try:
                await self.transport.send_message(
                    Message(
                        sender_id=self.id,
                        target_id="core",
                        message_type=MessageType.STATUS_UPDATE,
                        payload={"status": "inactive"},
                    )
                )
            except Exception:
                pass  # Ignore errors during shutdown

    async def _handle_core_message(self, message: Message) -> None:
        """Handle core system messages."""
        handlers = {
            MessageType.REGISTRATION_RESPONSE: self._handle_registration_response,
            MessageType.STATUS_UPDATE_RESPONSE: self._handle_status_update,
            # Add other core message type handlers as needed
        }

        if handler := handlers.get(message.message_type):
            await handler(message)

    async def _handle_registration_response(self, message: Message) -> None:
        """Handle registration response from core."""
        if message.payload["status"] == "success":
            self._token = message.payload["token"]
            self._authenticated = True
            logger.info(f"Agent {self.id} successfully registered")
            # Additional registration success handling if needed
        else:
            error = message.payload.get("error", "Unknown error")
            logger.error(f"Registration failed for agent {self.id}: {error}")
            # Handle registration failure

    async def _handle_status_update(self, message: Message) -> None:
        """Handle status updates."""
        # Implement if needed
        pass
