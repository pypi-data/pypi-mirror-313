import pytest
import pytest_asyncio
from redis.asyncio import ConnectionPool, Redis

from mas.transport.redis import RedisTransport
from mas.transport.service import TransportService

@pytest_asyncio.fixture(scope="session")
async def redis_pool():
    """Shared Redis connection pool for all tests."""
    pool = ConnectionPool.from_url(
        "redis://localhost",
        max_connections=50,  # Match transport settings
        decode_responses=True
    )
    try:
        # Verify pool works
        redis = Redis(connection_pool=pool)
        await redis.ping()
        await redis.aclose()
        yield pool
    finally:
        await pool.disconnect()

@pytest_asyncio.fixture
async def redis_transport(redis_pool):
    """Per-test transport instance with shared connection pool."""
    transport = RedisTransport("redis://localhost")
    # Initialize but don't start background tasks yet
    await transport.initialize()
    try:
        yield transport
    finally:
        # Ensure complete cleanup
        await transport.cleanup()

@pytest_asyncio.fixture
async def transport_service(redis_transport):
    """Per-test service instance."""
    service = TransportService(redis_transport)
    await service.start()
    try:
        yield service
    finally:
        await service.stop() 