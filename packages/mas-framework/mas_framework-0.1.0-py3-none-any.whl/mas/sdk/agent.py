import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Set

from pydantic import BaseModel

from mas.persistence.interfaces import IPersistenceProvider
from mas.protocol import Message, MessageType
from mas.transport.service import TransportService

logger = logging.getLogger(__name__)


class AgentConfig(BaseModel):
    """Configuration for an agent."""

    agent_id: str
    capabilities: Set[str] = set()
    endpoint: str
    metadata: Dict[str, Any] = {}


class Agent(ABC):
    """Enhanced agent implementation with lifecycle management."""

    __slots__ = (
        "id",
        "capabilities",
        "endpoint",
        "metadata",
        "transport",
        "persistence",
        "_running",
        "_registered",
        "_health_check_interval",
        "_tasks",
    )

    def __init__(
        self,
        config: AgentConfig,
        transport: TransportService,
        persistence: IPersistenceProvider,
    ):
        self.id = config.agent_id
        self.capabilities = config.capabilities
        self.endpoint = config.endpoint
        self.metadata = config.metadata

        self.transport = transport
        self.persistence = persistence
        self._running = False
        self._registered = False
        self._health_check_interval = 30  # seconds

    async def initialize(self) -> None:
        """Initialize agent and register with core service."""
        try:
            # Register with core service
            await self._register_with_core()

            # Initialize custom agent logic
            await self._initialize()

        except Exception as e:
            raise RuntimeError(f"Failed to initialize agent: {e}")

    async def start(self) -> None:
        """Start the agent and its background tasks."""
        if not self._registered:
            await self.initialize()

        self._running = True

        # Start background tasks with separate listeners
        self._tasks = [
            asyncio.create_task(self._listen_for_core_messages()),
            asyncio.create_task(self._listen_for_agent_messages()),
            asyncio.create_task(self._health_check_loop()),
        ]

    async def stop(self) -> None:
        """Gracefully stop the agent."""
        self._running = False

        # Cancel all background tasks
        if hasattr(self, "_tasks"):
            for task in self._tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        # Custom cleanup
        await self._cleanup()

        # Deregister from core
        await self._deregister_from_core()

    async def send_message(
        self,
        target_id: str,
        content: Dict[str, Any],
        message_type: str = MessageType.AGENT_MESSAGE,
    ) -> None:
        """Send message to another agent."""
        logger.info(f"Agent {self.id} sending message to {target_id}: {content}")
        message = Message(
            payload=content,
            sender_id=self.id,
            target_id=target_id,
            message_type=message_type,
        )
        try:
            await self.transport.send_message(message)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise

    async def _listen_for_core_messages(self) -> None:
        """Listen for core system messages."""
        try:
            async for message in self.transport.subscribe("core"):
                try:
                    await self._handle_core_message(message)
                except Exception as e:
                    await self._handle_error(
                        f"Error processing core message: {e}", message
                    )
        except Exception as e:
            if self._running:  # Only log if not shutting down
                await self._handle_error(f"Core message listener failed: {e}")

    async def _listen_for_agent_messages(self) -> None:
        """Listen for agent-specific messages."""
        try:
            async for message in self.transport.subscribe(self.id):
                try:
                    await self._handle_agent_message(message)
                except Exception as e:
                    await self._handle_error(
                        f"Error processing agent message: {e}", message
                    )
        except Exception as e:
            if self._running:  # Only log if not shutting down
                await self._handle_error(f"Agent message listener failed: {e}")

    async def _register_with_core(self) -> None:
        """Register agent with the core service."""
        message = Message(
            sender_id=self.id,
            target_id="core",
            message_type=MessageType.REGISTRATION_REQUEST,
            payload={
                "endpoint": self.endpoint,
                "metadata": self.metadata,
                "capabilities": list(self.capabilities),
            },
        )
        await self.transport.send_message(message)
        self._registered = True

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
                await self._handle_error(f"Health check failed: {e}")

    @abstractmethod
    async def _initialize(self) -> None:
        """Initialize agent-specific logic."""
        pass

    @abstractmethod
    async def _cleanup(self) -> None:
        """Cleanup agent-specific resources."""
        pass

    @abstractmethod
    async def _handle_agent_message(self, message: Message) -> None:
        """Handle agent-specific messages. To be implemented by child classes."""
        pass

    async def _handle_error(
        self, error: str, message: Optional[Message] = None
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
            MessageType.STATUS_UPDATE: self._handle_status_update,
            # Add other core message type handlers as needed
        }

        handler = handlers.get(message.message_type)
        if handler:
            await handler(message)

    async def _handle_registration_response(self, message: Message) -> None:
        """Handle registration response from core."""
        if message.payload.get("status") == "success":
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
