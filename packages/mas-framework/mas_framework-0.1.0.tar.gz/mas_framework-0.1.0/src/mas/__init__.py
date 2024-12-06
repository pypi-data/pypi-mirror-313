import asyncio
from typing import Any, List

from mas.persistence.interfaces import IPersistenceProvider
from mas.protocol import Message, MessageType
from mas.transport.service import TransportService

from .discovery.service import DiscoveryService


class MASCoreService:
    """Core service handling registration and discovery."""

    def __init__(
        self, transport: TransportService, persistence: IPersistenceProvider
    ) -> None:
        self.transport = transport
        self.persistence = persistence
        self.discovery = DiscoveryService(persistence)
        self.background_tasks: List[asyncio.Task[Any]] = []

    async def start(self) -> None:
        """Start the core service."""
        await self.transport.initialize()
        await self.persistence.initialize()
        # Start listening for core messages
        self.background_tasks.append(asyncio.create_task(self._start_message_handler()))

    async def stop(self) -> None:
        """Stop the core service."""
        await self.transport.cleanup()
        await self.persistence.cleanup()
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

        handler = handlers.get(message.message_type)

        if handler:
            await handler(message)

    async def _handle_registration(self, message: Message) -> None:
        """Handle agent registration."""
        try:
            # Register agent
            token = await self.discovery.register_agent(
                agent_id=message.sender_id,
                capabilities=set(message.payload["capabilities"]),
                endpoint=message.payload["endpoint"],
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
                    sender_id="core",
                    target_id=message.sender_id,
                    message_type=MessageType.REGISTRATION_RESPONSE,
                    payload={"status": "error", "error": str(e)},
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
                sender_id="core",
                target_id=message.sender_id,
                message_type=MessageType.DISCOVERY_RESPONSE,
                payload={"agents": agents},
            )
        )

    async def _handle_status_update(self, message: Message) -> None:
        """Handle agent status update."""
        await self.discovery.update_status(
            agent_id=message.sender_id,
            status=message.payload["status"],
        )
