import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator, AsyncIterator, Dict, Optional, override

from redis.asyncio.client import PubSub
from redis.exceptions import ConnectionError, RedisError

from mas.logger import get_logger
from mas.protocol import Message
from mas.transport.interfaces import ITransport

from .connection import RedisConnectionManager

logger = get_logger()


@dataclass
class SubscriptionState:
    """Tracks state of a single subscription."""

    channel: str
    subscriber_count: int = 0
    pubsub: Optional[PubSub] = None
    task: Optional[asyncio.Task] = None
    message_queue: Optional[asyncio.Queue] = None


class RedisTransport(ITransport):
    """Redis-based transport implementation."""

    def __init__(self, url: str = "redis://localhost") -> None:
        self.connection_manager = RedisConnectionManager(url=url)
        self._subscriptions: Dict[str, SubscriptionState] = {}
        self._shutdown_event = asyncio.Event()
        self._subscription_lock = asyncio.Lock()

    async def initialize(self) -> None:
        """Initialize the transport."""
        await self.connection_manager.initialize()
        logger.debug("Redis transport initialized")

    @override
    async def publish(self, message: Message) -> None:
        """Publish message to Redis."""
        if self._shutdown_event.is_set():
            raise RuntimeError("Transport is shutting down")

        try:
            async with self.connection_manager.get_connection() as redis:
                await redis.publish(message.target_id, message.model_dump_json())
                logger.debug(f"Published message to {message.target_id}")
        except RedisError as e:
            logger.error(f"Failed to publish message: {e}")
            raise RuntimeError(f"Failed to publish message: {e}") from e

    async def _message_listener(self, state: SubscriptionState) -> None:
        """Background task to listen for messages on a subscription."""
        try:
            if not state.pubsub:
                return

            async for message in state.pubsub.listen():
                if not state.subscriber_count or self._shutdown_event.is_set():
                    break

                if state.message_queue is None:
                    break

                if message["type"] == "message":
                    try:
                        parsed_message = Message.model_validate_json(message["data"])
                        await state.message_queue.put(parsed_message)
                    except Exception as e:
                        logger.error(f"Failed to parse message: {e}")
                        continue

        except asyncio.CancelledError:
            logger.debug(f"Message listener cancelled for {state.channel}")
        except ConnectionError as e:
            if not self._shutdown_event.is_set():
                logger.error(f"Connection lost for {state.channel}: {e}")
        except Exception as e:
            if not self._shutdown_event.is_set():
                logger.error(f"Error in message listener for {state.channel}: {e}")
        finally:
            if state.message_queue:
                await state.message_queue.put(None)  # Signal end of stream

    @asynccontextmanager
    async def _get_subscription(self, channel: str) -> AsyncIterator[SubscriptionState]:
        """Get or create a subscription state."""
        async with self._subscription_lock:
            state = self._subscriptions.get(channel)
            if not state:
                state = SubscriptionState(
                    channel=channel,
                    message_queue=asyncio.Queue(),
                )
                self._subscriptions[channel] = state
                state.pubsub = await self.connection_manager.get_pubsub(channel)
                state.task = asyncio.create_task(self._message_listener(state))

            state.subscriber_count += 1

        try:
            yield state
        finally:
            async with self._subscription_lock:
                state.subscriber_count -= 1
                if state.subscriber_count <= 0:
                    await self._cleanup_subscription(channel)

    @override
    async def subscribe(self, channel: str) -> AsyncGenerator[Message, None]:
        """Subscribe to Redis channel."""
        if self._shutdown_event.is_set():
            raise RuntimeError("Transport is shutting down")

        async with self._get_subscription(channel) as state:
            while not self._shutdown_event.is_set():
                if state.message_queue is None:
                    break
                message = await state.message_queue.get()
                if message is None:  # End of stream
                    break
                yield message

    async def _cleanup_subscription(self, channel: str) -> None:
        """Clean up a subscription and its resources."""
        if state := self._subscriptions.get(channel):
            if state.task:
                state.task.cancel()
                try:
                    await state.task
                except asyncio.CancelledError:
                    pass

            if state.pubsub:
                try:
                    await state.pubsub.unsubscribe(channel)
                    await state.pubsub.close()
                except Exception as e:
                    logger.error(f"Error cleaning up pubsub for {channel}: {e}")

            if state.message_queue:
                await state.message_queue.put(None)
                state.message_queue = None

            del self._subscriptions[channel]
            logger.debug(f"Cleaned up subscription for {channel}")

    @override
    async def unsubscribe(self, channel: str) -> None:
        """Mark subscription for cleanup when no more subscribers."""
        async with self._subscription_lock:
            if state := self._subscriptions.get(channel):
                state.subscriber_count = 0
                await self._cleanup_subscription(channel)

    async def cleanup(self) -> None:
        """Clean up all transport resources."""
        logger.debug("Starting Redis transport cleanup")
        self._shutdown_event.set()

        channels = list(self._subscriptions.keys())
        cleanup_tasks = [
            asyncio.create_task(self._cleanup_subscription(channel))
            for channel in channels
        ]

        if cleanup_tasks:
            await asyncio.gather(*cleanup_tasks, return_exceptions=True)

        await self.connection_manager.cleanup()
        logger.debug("Redis transport cleanup completed")
