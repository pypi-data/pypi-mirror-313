import asyncio
from datetime import UTC, datetime

import pytest
import pytest_asyncio

from mas.protocol import Message, MessageType
from mas.transport.redis import RedisTransport


# Event loop fixture
@pytest_asyncio.fixture(scope="session")
async def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.get_running_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def redis_transport(event_loop):
    """Shared Redis transport instance."""
    transport = RedisTransport("redis://localhost")
    await transport.initialize()
    try:
        yield transport
    finally:
        await transport.cleanup()


@pytest.fixture
def message_factory():
    """Create test messages."""

    def create_message(
        sender_id: str, target_id: str, content: str = "test"
    ) -> Message:
        return Message(
            sender_id=sender_id,
            target_id=target_id,
            message_type=MessageType.AGENT_MESSAGE,
            payload={"content": content},
        )

    return create_message


@pytest.mark.asyncio
class TestRedisTransport:
    """Test Redis transport implementation."""

    async def test_basic_publish_subscribe(
        self,
        redis_transport,
        message_factory,
    ):
        """Test basic publish/subscribe functionality."""
        channel = "test_channel"
        message = message_factory("test_sender", channel)

        event_loop = asyncio.get_running_loop()

        received_messages = []

        # Set up subscriber
        async def subscriber():
            try:
                async with redis_transport._get_subscription(channel) as (state, queue):
                    msg = await queue.get()
                    received_messages.append(msg)
            except asyncio.CancelledError:
                pass

        # Start subscriber
        sub_task = event_loop.create_task(subscriber())
        await asyncio.sleep(0.1)  # Wait for subscription

        try:
            # Publish message
            await redis_transport.publish(message)

            # Wait for message
            await asyncio.wait_for(sub_task, timeout=2.0)
        finally:
            if not sub_task.done():
                sub_task.cancel()
                await asyncio.gather(sub_task, return_exceptions=True)

        assert len(received_messages) == 1
        assert received_messages[0].id == message.id

    async def test_multiple_subscribers(
        self,
        redis_transport,
        message_factory,
    ):
        """Test multiple subscribers to same channel."""
        event_loop = asyncio.get_running_loop()
        channel = "test_multi_sub"
        message = message_factory("test_sender", channel)

        received_messages = {"sub1": [], "sub2": []}

        async def subscriber(sub_id):
            try:
                async with redis_transport._get_subscription(channel) as (state, queue):
                    msg = await queue.get()
                    received_messages[sub_id].append(msg)
            except asyncio.CancelledError:
                pass

        # Start subscribers
        tasks = [
            event_loop.create_task(subscriber(sub_id)) for sub_id in received_messages
        ]

        try:
            await asyncio.sleep(0.1)  # Wait for subscriptions

            # Publish message
            await redis_transport.publish(message)

            # Wait for all subscribers
            await asyncio.wait_for(asyncio.gather(*tasks), timeout=2.0)
        finally:
            # Ensure tasks are cleaned up
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

        for sub_messages in received_messages.values():
            assert len(sub_messages) == 1
            assert sub_messages[0].id == message.id

    async def test_cleanup_with_active_subscriptions(self, redis_transport):
        """Test cleanup behavior with active subscriptions."""
        channel = "test_cleanup"

        async with redis_transport._get_subscription(channel) as (state, queue):
            assert channel in redis_transport._subscriptions
            initial_count = state.subscriber_count
            assert initial_count == 1  # Verify we start with one subscriber

            # Force cleanup
            await redis_transport.cleanup()

            # Verify cleanup
            assert channel not in redis_transport._subscriptions
            # The state might be None at this point, so we need to handle that
            if state:
                assert state.subscriber_count >= 0  # Should never be negative

    async def test_message_validation(self, redis_transport):
        """Test message validation."""
        # Test invalid message (no target)
        invalid_message = Message(
            sender_id="test_sender",
            target_id="",
            message_type=MessageType.AGENT_MESSAGE,
            payload={"content": "test"},
            timestamp=datetime.now(UTC),
        )

        with pytest.raises(ValueError, match="Message must have target_id"):
            await redis_transport.validate_message(invalid_message)

    async def test_subscription_cleanup(self, redis_transport):
        """Test subscription cleanup on unsubscribe."""
        channel = "test_unsub"

        # Create subscription
        async with redis_transport._get_subscription(channel) as (state, queue):
            assert channel in redis_transport._subscriptions

        # Verify cleanup after context exit
        assert channel not in redis_transport._subscriptions
