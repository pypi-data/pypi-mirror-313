import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from typing import AsyncGenerator, Dict, Optional, Set

from redis.asyncio import ConnectionPool, Redis
from redis.asyncio.client import PubSub
from redis.exceptions import RedisError

from mas.logger import get_logger

logger = get_logger()


@dataclass
class ConnectionState:
    """Tracks the state and health of Redis connections."""

    last_health_check: Optional[datetime] = None
    consecutive_failures: int = 0
    is_healthy: bool = False
    last_error: Optional[str] = None
    active_channels: Set[str] = field(default_factory=set)

    def __post_init__(self):
        self.active_channels = set()


class RedisConnectionManager:
    """Manages Redis connections and their lifecycle."""

    def __init__(
        self,
        url: str = "redis://localhost",
        pool_size: int = 10,
        health_check_interval: int = 30,
    ) -> None:
        self.url = url
        self.pool_size = pool_size
        self.health_check_interval = health_check_interval

        self._pool: Optional[ConnectionPool] = None
        self._pubsubs: Dict[str, PubSub] = {}
        self._state = ConnectionState()
        self._running = False
        self._health_check_task: Optional[asyncio.Task] = None
        self._cleanup_lock = asyncio.Lock()

    async def initialize(self) -> None:
        """Initialize the connection manager."""
        if self._running:
            return

        try:
            self._pool = ConnectionPool.from_url(
                self.url, max_connections=self.pool_size, decode_responses=True
            )

            # Create a direct connection for initialization check
            redis = Redis(connection_pool=self._pool)
            try:
                await redis.ping()
            finally:
                await redis.close()

            self._state.is_healthy = True
            self._running = True

            # Start health check loop
            self._health_check_task = asyncio.create_task(self._health_check_loop())
            logger.info("Redis connection manager initialized successfully")

        except RedisError as e:
            self._state.last_error = str(e)
            logger.error(f"Failed to initialize Redis connection manager: {e}")
            # Clean up pool if initialization fails
            if self._pool:
                await self._pool.disconnect()
                self._pool = None
            raise

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[Redis, None]:
        """Get a Redis connection from the pool."""
        if not self._running:
            raise RuntimeError("Connection manager not initialized or shutting down")

        if not self._pool:
            raise RuntimeError("Connection pool not initialized")

        redis = Redis(connection_pool=self._pool)
        try:
            yield redis
        finally:
            await redis.close()

    async def get_pubsub(self, channel: str) -> PubSub:
        """Get or create a PubSub instance for a channel."""
        if not self._running:
            raise RuntimeError("Connection manager not initialized or shutting down")

        if channel in self._pubsubs:
            return self._pubsubs[channel]

        async with self._cleanup_lock:
            # Double check after acquiring lock
            if channel in self._pubsubs:
                return self._pubsubs[channel]

            async with self.get_connection() as redis:
                pubsub = redis.pubsub()
                await pubsub.subscribe(channel)
                self._pubsubs[channel] = pubsub
                self._state.active_channels.add(channel)
                logger.debug(f"Created new PubSub for channel: {channel}")
                return pubsub

    async def _health_check_loop(self) -> None:
        """Periodic health check of Redis connection."""
        while self._running:
            try:
                async with self.get_connection() as redis:
                    await redis.ping()
                self._state.last_health_check = datetime.now()
                self._state.is_healthy = True
                self._state.consecutive_failures = 0

            except RedisError as e:
                self._state.consecutive_failures += 1
                self._state.is_healthy = False
                self._state.last_error = str(e)
                logger.error(f"Health check failed: {e}")

            await asyncio.sleep(self.health_check_interval)

    async def cleanup(self) -> None:
        """Cleanup all connections."""
        if not self._running:
            return

        async with self._cleanup_lock:
            logger.info("Starting Redis connection manager cleanup")
            self._running = False

            if self._health_check_task:
                self._health_check_task.cancel()
                try:
                    await self._health_check_task
                except asyncio.CancelledError:
                    pass

            # Cleanup PubSub connections
            for channel, pubsub in list(self._pubsubs.items()):
                try:
                    await pubsub.unsubscribe()
                    await pubsub.close()
                    self._state.active_channels.discard(channel)
                except Exception as e:
                    logger.error(f"Error cleaning up PubSub for channel {channel}: {e}")
            self._pubsubs.clear()

            # Close connection pool
            if self._pool:
                try:
                    await self._pool.disconnect()
                except Exception as e:
                    logger.error(f"Error disconnecting connection pool: {e}")
                finally:
                    self._pool = None

            logger.info("Redis connection manager cleanup completed")

    @property
    def is_healthy(self) -> bool:
        """Check if the connection is currently healthy."""
        return self._state.is_healthy and self._running

    @property
    def last_error(self) -> Optional[str]:
        """Get the last error message."""
        return self._state.last_error
