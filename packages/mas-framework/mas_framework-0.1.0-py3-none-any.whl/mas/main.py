import asyncio
import logging

from mas.persistence.memory import InMemoryProvider
from mas.transport.redis import RedisTransport
from mas.transport.service import TransportService

logger = logging.getLogger(__name__)


async def main() -> None:
    """Initialize and run the main service."""
    try:
        storage = InMemoryProvider()
        transport = TransportService(transport=RedisTransport())

        await storage.initialize()
        await transport.initialize()

        # Keep service running
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error in main service: {e}")
        raise
    finally:
        await storage.cleanup()
        await transport.cleanup()
