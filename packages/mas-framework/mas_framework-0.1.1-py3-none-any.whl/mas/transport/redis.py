from typing import AsyncGenerator, Dict, override

from redis.asyncio import Redis
from redis.asyncio.client import PubSub
from redis.exceptions import RedisError

from mas.logger import get_logger
from mas.protocol import Message
from mas.transport.interfaces import ITransport

logger = get_logger()


class RedisTransport(ITransport):
    """Redis-based transport implementation."""

    def __init__(self, url: str = "redis://localhost") -> None:
        self.url = url
        self.redis: Redis | None = None
        self._pubsubs: Dict[str, PubSub] = {}  # Track PubSub instances per channel

    async def initialize(self) -> None:
        """Initialize Redis connection."""
        try:
            self.redis = Redis.from_url(self.url, decode_responses=True)
            await self.redis.ping()
        except RedisError as e:
            raise RuntimeError(f"Failed to initialize Redis connection: {e}")

    @override
    async def publish(self, message: Message) -> None:
        """Publish message to Redis."""
        try:
            logger.debug(
                f"Publishing message to channel {message.target_id}: {message.model_dump_json()}"
            )
            await self.redis.publish(message.target_id, message.model_dump_json())
        except RedisError as e:
            raise RuntimeError(f"Failed to publish message: {e}")

    @override
    async def subscribe(self, channel: str) -> AsyncGenerator[Message, None]:
        """Subscribe to Redis channel with separate PubSub instance."""
        try:
            # Create new PubSub instance for this channel if it doesn't exist
            if channel not in self._pubsubs:
                logger.debug(f"Creating new subscription for channel: {channel}")
                pubsub = self.redis.pubsub()
                await pubsub.subscribe(channel)
                self._pubsubs[channel] = pubsub
            else:
                pubsub = self._pubsubs[channel]
                logger.debug(f"Using existing subscription for channel: {channel}")

            async for message in pubsub.listen():
                logger.debug(f"Received raw message on channel {channel}: {message}")
                if message["type"] == "message":
                    try:
                        yield Message.model_validate_json(message["data"])
                    except Exception as e:
                        logger.error(f"Failed to parse message: {e}")
                        continue

        except RedisError as e:
            logger.error(f"Subscription error for channel {channel}: {e}")
            if channel in self._pubsubs:
                del self._pubsubs[channel]
            raise RuntimeError(f"Subscription error: {e}")

    @override
    async def unsubscribe(self, channel: str) -> None:
        """Unsubscribe from Redis channel."""
        if channel in self._pubsubs:
            try:
                await self._pubsubs[channel].unsubscribe(channel)
                await self._pubsubs[channel].close()
                del self._pubsubs[channel]
                logger.debug(f"Unsubscribed from channel: {channel}")
            except RedisError as e:
                logger.error(f"Error unsubscribing from channel {channel}: {e}")

    async def cleanup(self) -> None:
        """Close all Redis connections."""
        for channel, pubsub in self._pubsubs.items():
            try:
                await pubsub.unsubscribe()
                await pubsub.close()
            except Exception as e:
                logger.error(f"Error cleaning up subscription for {channel}: {e}")

        self._pubsubs.clear()
        if hasattr(self, "redis"):
            await self.redis.close()
