import asyncio
import logging
from typing import List

from examples.chain.agents import ChainAgent
from mas import MASCoreService
from mas.persistence.memory import InMemoryProvider
from mas.sdk.agent import AgentConfig
from mas.transport.redis import RedisTransport
from mas.transport.service import TransportService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Starting chain example")

    # Initialize core services
    persistence = InMemoryProvider.create()
    transport = TransportService(transport=RedisTransport())
    core = MASCoreService(transport=transport, persistence=persistence)

    logger.info("Starting core service")
    await core.start()

    # Create agents
    agents: List[ChainAgent] = []
    for i in range(4):
        logger.info(f"Creating agent_{i+1}")
        agent = ChainAgent(
            config=AgentConfig(
                agent_id=f"agent_{i+1}",
                metadata={
                    "name": f"Agent {i+1}",
                    "description": f"Chain agent {i+1}",
                },
                capabilities={"chain"},
            ),
            transport=transport,
            persistence=persistence,
        )
        agents.append(agent)

    # Set up the chain
    logger.info("Setting up agent chain")
    for i, agent in enumerate(agents):
        next_idx = (i + 1) % len(agents)
        await agent.set_next_agent(agents[next_idx].id)

    # Start all agents
    logger.info("Starting all agents")
    for agent in agents:
        await agent.start()

    await asyncio.sleep(2)

    logger.info("Starting message chain")
    await agents[0].start_chain()

    logger.info("Waiting for chain completion")
    await agents[0].chain_complete.wait()

    # Stop all agents
    for agent in agents:
        await agent.stop()

    # Stop core service
    await core.stop()


if __name__ == "__main__":
    asyncio.run(main())
