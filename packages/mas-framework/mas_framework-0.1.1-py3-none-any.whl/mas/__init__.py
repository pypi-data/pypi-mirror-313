import asyncio
from typing import Any, List

from mas.persistence.interfaces import IPersistenceProvider
from mas.protocol import Message, MessageType
from mas.transport.service import TransportService
from .discovery.service import DiscoveryService


class MASCoreService:
    """Core service handling registration and discovery."""

    def __init__(
        self,
        transport: TransportService,
        persistence: IPersistenceProvider,
    ) -> None:
        self.transport = transport
        self.persistence = persistence
        self.discovery = DiscoveryService(persistence)
        self.background_tasks: List[asyncio.Task[Any]] = []

    async def start(self) -> None:
        """Start the core service."""
        await self.transport.initialize()
        await self.persistence.initialize()
        await self.discovery.initialize()
        # Start listening for core messages
        self.background_tasks.append(asyncio.create_task(self._start_message_handler()))

    async def stop(self) -> None:
        """Stop the core service."""
        await self.transport.cleanup()
        await self.persistence.cleanup()
        await self.discovery.cleanup()

        for task in self.background_tasks:
            try:
                task.cancel()
            except asyncio.CancelledError:
                pass
        self.background_tasks.clear()

    async def _start_message_handler(self) -> None:
        """Start message handler."""
        async for message in self.transport.subscribe("core"):
            await self._handle_message(message)

    async def _stop_message_handler(self) -> None:
        """Stop message handler."""
        await self.transport.unsubscribe("core")

    async def _handle_message(self, message: Message) -> None:
        """Handle core service messages."""
        handlers = {
            MessageType.STATUS_UPDATE: self._handle_status_update,
            MessageType.DISCOVERY_REQUEST: self._handle_discovery,
            MessageType.REGISTRATION_REQUEST: self._handle_registration,
        }

        if handler := handlers.get(message.message_type):
            await handler(message)

    async def _handle_registration(self, message: Message) -> None:
        """Handle agent registration."""
        try:
            # Register agent
            token = await self.discovery.register_agent(
                agent_id=message.sender_id,
                capabilities=set(message.payload["capabilities"]),
            )

            # Send response
            await self.transport.send_message(
                Message(
                    sender_id="core",
                    target_id=message.sender_id,
                    message_type=MessageType.REGISTRATION_RESPONSE,
                    payload={"token": token, "status": "success"},
                )
            )

        except Exception as e:
            await self.transport.send_message(
                Message(
                    payload={"status": "error", "error": str(e)},
                    sender_id="core",
                    target_id=message.sender_id,
                    message_type=MessageType.REGISTRATION_RESPONSE,
                )
            )

    async def _handle_discovery(self, message: Message) -> None:
        """Handle agent discovery request."""
        capabilities = set(message.payload.get("capabilities", []))

        # Find matching agents
        agents = await self.discovery.find_agents(capabilities)

        # Send response
        await self.transport.send_message(
            Message(
                payload={"agents": agents},
                sender_id="core",
                target_id=message.sender_id,
                message_type=MessageType.DISCOVERY_RESPONSE,
            )
        )

    async def _handle_status_update(self, message: Message) -> None:
        """Handle agent status update."""
        await self.discovery.update_status(
            status=message.payload["status"],
            agent_id=message.sender_id,
        )

        await self.transport.send_message(
            Message(
                payload={"status": "success"},
                sender_id="core",
                target_id=message.sender_id,
                message_type=MessageType.STATUS_UPDATE_RESPONSE,
            )
        )
