from typing import AsyncGenerator

from mas.protocol import Message

from .interfaces import ITransport


class TransportService:
    """Service for managing message transport."""

    def __init__(self, transport: ITransport) -> None:
        self.transport = transport

    async def initialize(self) -> None:
        """Initialize the transport."""
        await self.transport.initialize()

    async def send_message(self, message: Message) -> None:
        """Send a message through the transport."""
        await self.transport.publish(message)

    async def cleanup(self) -> None:
        """Cleanup transport resources."""
        await self.transport.cleanup()

    async def unsubscribe(self, channel: str) -> None:
        """Unsubscribe from a channel."""
        await self.transport.unsubscribe(channel)

    async def subscribe(self, channel: str) -> AsyncGenerator[Message, None]:
        """Subscribe to messages on a channel.

        Args:
            channel: Channel identifier to subscribe to

        Returns:
            AsyncGenerator yielding messages from the channel
        """
        async for message in self.transport.subscribe(channel):
            yield message
