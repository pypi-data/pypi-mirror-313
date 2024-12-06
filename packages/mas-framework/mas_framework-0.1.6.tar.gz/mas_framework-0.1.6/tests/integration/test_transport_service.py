import asyncio
from datetime import UTC, datetime
from uuid import uuid4

import pytest
import pytest_asyncio
import redis.asyncio as redis

from mas.protocol import Message, MessageType
from mas.transport.redis import RedisTransport
from mas.transport.service import ServiceState, TransportService
from mas.logger import get_logger

logger = get_logger()


# Fixtures
@pytest_asyncio.fixture(scope="session")
async def event_loop():
    """Create an event loop for the test session."""
    logger.info("Creating event loop")
    loop = asyncio.get_running_loop()
    yield loop

    # Get pending tasks
    pending = asyncio.all_tasks(loop)
    if pending:
        # Cancel all tasks
        logger.info(f"Cancelling {len(pending)} pending tasks")
        for task in pending:
            task.cancel()
        # Wait for tasks to complete
        await asyncio.gather(
            *pending,
            return_exceptions=True,
        )

    # Clean up
    logger.info("Cleaning up event loop")
    await loop.shutdown_asyncgens()
    loop.stop()
    loop.close()


@pytest_asyncio.fixture
async def redis_transport(event_loop):
    logger.info("Creating Redis transport")
    transport = RedisTransport("redis://localhost")
    await transport.initialize()
    try:
        yield transport
    finally:
        logger.info("Cleaning up Redis transport")
        await transport.cleanup()


@pytest_asyncio.fixture
async def transport_service(redis_transport):
    logger.info("Creating transport service")
    service = TransportService(redis_transport)
    await service.start()
    try:
        yield service
    finally:
        logger.info("Cleaning up transport service")
        await service.stop()


@pytest.fixture
def channel_name():
    name = f"test_channel_{uuid4().hex[:8]}"
    logger.info(f"Created channel name: {name}")
    return name


@pytest.fixture
def message_factory():
    def create_message(
        sender_id: str,
        target_id: str,
        content: str = "test",
    ) -> Message:
        logger.debug(f"Creating message: sender={sender_id}, target={target_id}")
        return Message(
            sender_id=sender_id,
            target_id=target_id,
            message_type=MessageType.AGENT_MESSAGE,
            payload={"content": content},
            timestamp=datetime.now(UTC),
        )

    return create_message


@pytest_asyncio.fixture(autouse=True)
async def check_redis():
    try:
        logger.info("Checking Redis connection")
        client = redis.Redis(host="localhost")
        await client.ping()
        await client.aclose()
    except redis.ConnectionError:
        logger.error("Redis server not available")
        pytest.skip("Redis server is not available")


# Test Groups:
# 1. Service Lifecycle Tests
# 2. Subscription Tests
# 3. Message Routing Tests
# 4. Error Handling Tests


# 1. Service Lifecycle Tests
@pytest.mark.asyncio
class TestServiceLifecycle:
    async def test_service_starts_in_initialized_state(self):
        logger.info("Testing service initial state")
        service = TransportService(RedisTransport("redis://localhost"))
        assert service.state == ServiceState.INITIALIZED

    async def test_service_enters_running_state_after_start(self, transport_service):
        logger.info("Testing service running state")
        assert transport_service.state == ServiceState.RUNNING

    async def test_service_enters_shutdown_state_after_stop(self, redis_transport):
        logger.info("Testing service shutdown state")
        service = TransportService(redis_transport)
        await service.start()
        await service.stop()
        assert service.state == ServiceState.SHUTDOWN

    @pytest.mark.skip("unstable")
    async def test_cleanup_subscriptions_on_stop(self, redis_transport, channel_name):
        """Test cleanup behavior with active subscriptions."""
        logger.info("Starting cleanup subscriptions test")
        received_messages = []
        event_loop = asyncio.get_running_loop()

        transport_service = TransportService(redis_transport)
        await transport_service.start()

        async def message_handler():
            logger.info("Message handler starting")
            async with transport_service.message_stream(
                "test_subscriber", channel_name
            ) as stream:
                try:
                    logger.debug("Waiting for messages")
                    async for message in stream:
                        logger.debug(f"Received message: {message}")
                        received_messages.append(message)
                except asyncio.CancelledError:
                    logger.info("Message handler cancelled")
                    pass

        # Start message handler
        logger.info("Creating message handler task")
        handler_task = event_loop.create_task(message_handler())

        # Wait briefly for subscription to be established
        logger.debug("Waiting for subscription setup")
        await asyncio.sleep(0.1)

        # Stop service
        logger.info("Stopping transport service")
        await transport_service.stop()

        # Clean up handler task
        logger.info("Cleaning up handler task")
        handler_task.cancel()
        await asyncio.gather(handler_task, return_exceptions=True)

        # Verify cleanup
        logger.info("Verifying cleanup")
        assert transport_service.state == ServiceState.SHUTDOWN
        assert not transport_service._subscriptions


# 2. Subscription Tests
@pytest.mark.asyncio
class TestSubscriptions:
    @pytest.mark.skip("unstable")
    async def test_subscribe_to_channel(self, transport_service, channel_name):
        logger.info(f"Testing subscribe to {channel_name}")
        await transport_service.subscribe("test_subscriber", channel_name)
        assert "test_subscriber" in transport_service._subscriptions
        assert channel_name in transport_service._subscriptions["test_subscriber"]

    @pytest.mark.skip("unstable")
    async def test_unsubscribe_from_channel(self, transport_service, channel_name):
        logger.info(f"Testing unsubscribe from {channel_name}")
        # First subscribe
        await transport_service.subscribe("test_subscriber", channel_name)
        # Then unsubscribe
        await transport_service.unsubscribe("test_subscriber", channel_name)
        assert "test_subscriber" not in transport_service._subscriptions

    @pytest.mark.skip("unstable")
    async def test_multiple_subscribers_same_channel(
        self, transport_service, channel_name
    ):
        logger.info("Testing multiple subscribers")
        await transport_service.subscribe("subscriber1", channel_name)
        await transport_service.subscribe("subscriber2", channel_name)

        assert "subscriber1" in transport_service._subscriptions
        assert "subscriber2" in transport_service._subscriptions
        assert channel_name in transport_service._subscriptions["subscriber1"]
        assert channel_name in transport_service._subscriptions["subscriber2"]

    @pytest.mark.skip("unstable")
    async def test_duplicate_subscription_raises_error(
        self, transport_service, channel_name
    ):
        logger.info("Testing duplicate subscription")
        await transport_service.subscribe("test_subscriber", channel_name)

        with pytest.raises(RuntimeError, match="Already subscribed to channel"):
            await transport_service.subscribe("test_subscriber", channel_name)


# 3. Message Routing Tests
@pytest.mark.asyncio
class TestMessageRouting:
    async def test_send_and_receive_message(
        self,
        transport_service,
        channel_name,
        message_factory,
    ):
        logger.info("Testing send and receive message")
        event_loop = asyncio.get_running_loop()
        # Create test message
        test_message = message_factory("sender1", channel_name)

        # Set up receiver
        received_messages = []

        async def message_receiver():
            logger.debug("Message receiver starting")
            async with transport_service.message_stream(
                "receiver1", channel_name
            ) as stream:
                async for message in stream:
                    logger.debug(f"Received message: {message}")
                    received_messages.append(message)
                    break  # Exit after first message

        # Start receiver task
        logger.debug("Starting receiver task")
        receiver_task = event_loop.create_task(message_receiver())

        # Wait a bit for subscription to be ready
        await asyncio.sleep(0.1)

        # Send message
        logger.debug("Sending test message")
        await transport_service.send_message(test_message)

        # Wait for message to be received
        await asyncio.wait_for(receiver_task, timeout=2.0)

        assert len(received_messages) == 1
        assert received_messages[0].id == test_message.id
        assert (
            received_messages[0].payload["content"] == test_message.payload["content"]
        )

    async def test_message_delivery_to_multiple_subscribers(
        self,
        transport_service,
        channel_name,
        message_factory,
    ):
        logger.info("Testing message delivery to multiple subscribers")
        event_loop = asyncio.get_running_loop()
        test_message = message_factory("sender1", channel_name)

        # Set up receivers
        received_messages = {"receiver1": [], "receiver2": []}

        async def message_receiver(receiver_id):
            logger.debug(f"Starting receiver {receiver_id}")
            async with transport_service.message_stream(
                receiver_id, channel_name
            ) as stream:
                async for message in stream:
                    logger.debug(f"Receiver {receiver_id} got message: {message}")
                    received_messages[receiver_id].append(message)
                    break

        # Start receiver tasks
        logger.debug("Starting receiver tasks")
        tasks = [
            event_loop.create_task(message_receiver(receiver_id))
            for receiver_id in received_messages
        ]

        await asyncio.sleep(0.1)  # Wait for subscriptions

        # Send message
        logger.debug("Sending test message")
        await transport_service.send_message(test_message)

        # Wait for all receivers
        await asyncio.wait_for(asyncio.gather(*tasks), timeout=2.0)

        # Verify both receivers got the message
        for receiver_messages in received_messages.values():
            assert len(receiver_messages) == 1
            assert receiver_messages[0].id == test_message.id


# 4. Error Handling Tests
@pytest.mark.asyncio
class TestErrorHandling:
    async def test_send_message_with_service_stopped(
        self, redis_transport, message_factory
    ):
        logger.info("Testing send message with stopped service")
        service = TransportService(redis_transport)
        test_message = message_factory("sender1", "test_channel")

        with pytest.raises(RuntimeError, match="Transport service not running"):
            await service.send_message(test_message)

    async def test_subscribe_with_service_stopped(self, redis_transport):
        logger.info("Testing subscribe with stopped service")
        service = TransportService(redis_transport)

        with pytest.raises(RuntimeError, match="Transport service not running"):
            await service.subscribe("test_subscriber", "test_channel")

    async def test_unsubscribe_nonexistent_subscription(self, transport_service):
        logger.info("Testing unsubscribe nonexistent subscription")
        # Should not raise an error
        await transport_service.unsubscribe("nonexistent", "test_channel")

    @pytest.mark.skip("unstable")
    async def test_message_stream_cleanup_on_error(
        self, transport_service, channel_name, message_factory
    ):
        logger.info("Testing message stream cleanup on error")
        async with transport_service.message_stream(
            "test_receiver", channel_name
        ) as stream:
            async for message in stream:
                assert "test_receiver" in transport_service._subscriptions
                raise RuntimeError("Simulated error")

        # Verify cleanup happened despite error
        assert "test_receiver" not in transport_service._subscriptions


@pytest.mark.asyncio
class TestTransportServiceCleanup:
    """Test transport service cleanup behavior."""

    @pytest.mark.skip("unstable")
    async def test_cleanup_with_active_subscriptions(
        self, transport_service, channel_name
    ):
        """Test cleanup with active subscriptions."""
        logger.info("Testing cleanup with active subscriptions")
        # Create multiple subscriptions
        subscribers = ["sub1", "sub2", "sub3"]
        for subscriber in subscribers:
            logger.debug(f"Creating subscription for {subscriber}")
            await transport_service.subscribe(subscriber, channel_name)

        # Verify subscriptions are active
        for subscriber in subscribers:
            assert subscriber in transport_service._subscriptions
            assert channel_name in transport_service._subscriptions[subscriber]

        # Stop service
        logger.info("Stopping service")
        await transport_service.stop()

        # Verify cleanup
        logger.debug("Verifying cleanup")
        assert transport_service.state == ServiceState.SHUTDOWN
        assert not transport_service._subscriptions

    async def test_message_stream_cleanup_on_error(
        self, transport_service, channel_name
    ):
        """Test message stream cleanup when error occurs."""
        logger.info("Testing message stream cleanup on error")
        subscriber_id = "test_sub"

        try:
            async with transport_service.message_stream(subscriber_id, channel_name):
                assert subscriber_id in transport_service._subscriptions
                raise RuntimeError("Simulated error")
        except RuntimeError:
            pass

        # Verify cleanup happened despite error
        assert subscriber_id not in transport_service._subscriptions

    @pytest.mark.skip("unstable")
    async def test_concurrent_subscriptions(self, transport_service, channel_name):
        """Test handling multiple concurrent subscriptions."""
        logger.info("Testing concurrent subscriptions")
        subscriber_count = 5
        subscribers = [f"sub_{i}" for i in range(subscriber_count)]

        # Create subscriptions concurrently
        async def subscribe(sub_id):
            logger.debug(f"Creating subscription for {sub_id}")
            await transport_service.subscribe(sub_id, channel_name)

        await asyncio.gather(*(subscribe(sub_id) for sub_id in subscribers))

        # Verify all subscriptions are active
        for subscriber in subscribers:
            assert subscriber in transport_service._subscriptions
            assert channel_name in transport_service._subscriptions[subscriber]

        # Stop service
        logger.info("Stopping service")
        await transport_service.stop()

        # Verify all cleaned up
        assert not transport_service._subscriptions

    @pytest.mark.skip("unstable")
    async def test_cleanup_during_message_processing(
        self,
        transport_service,
        channel_name,
        message_factory,
    ):
        """Test cleanup while messages are being processed."""
        logger.info("Testing cleanup during message processing")
        event_loop = asyncio.get_running_loop()
        message_count = 5
        received_messages = []

        # Set up receiver
        async def message_receiver():
            logger.debug("Starting message receiver")
            try:
                async with transport_service.message_stream(
                    "receiver", channel_name
                ) as stream:
                    async for message in stream:
                        logger.debug(f"Received message: {message}")
                        received_messages.append(message)
                        await asyncio.sleep(0.1)  # Simulate processing time
            except RuntimeError:
                # Expected when service stops
                logger.info("Service stop detected")
                pass

        # Start receiver
        logger.debug("Starting receiver task")
        receiver_task = event_loop.create_task(message_receiver())
        await asyncio.sleep(0.1)  # Wait for subscription

        # Send messages
        for i in range(message_count):
            message = message_factory(f"sender_{i}", channel_name)
            logger.debug(f"Sending message {i}")
            await transport_service.send_message(message)

        # Stop service while processing
        logger.info("Stopping service during processing")
        await transport_service.stop()

        # Verify cleanup
        logger.debug("Verifying cleanup")
        assert transport_service.state == ServiceState.SHUTDOWN
        assert not transport_service._subscriptions

        # Cleanup
        await receiver_task

    async def test_stop_idempotency(self, transport_service):
        """Test that stopping multiple times is safe."""
        logger.info("Testing stop idempotency")
        # Stop multiple times
        await transport_service.stop()
        await transport_service.stop()
        await transport_service.stop()

        assert transport_service.state == ServiceState.SHUTDOWN
        assert not transport_service._subscriptions

    async def test_subscription_after_stop(self, transport_service, channel_name):
        """Test that subscribing after stop raises error."""
        logger.info("Testing subscription after stop")
        await transport_service.stop()

        with pytest.raises(RuntimeError, match="Transport service not running"):
            await transport_service.subscribe("test_sub", channel_name)
