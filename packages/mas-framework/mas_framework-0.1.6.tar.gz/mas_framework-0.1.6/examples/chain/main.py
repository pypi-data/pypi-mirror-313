import asyncio
import signal
from contextlib import AsyncExitStack
from typing import List

from examples.chain.agents import ChainAgent
from mas import mas_service
from mas.logger import get_logger
from mas.persistence.memory import InMemoryProvider
from mas.sdk.agent import AgentConfig
from mas.transport.service import TransportService

logger = get_logger()

# Global shutdown event
shutdown_event = asyncio.Event()


def handle_shutdown(signum, frame) -> None:
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}")
    shutdown_event.set()


async def setup_agents(
    transport: TransportService,
    persistence: InMemoryProvider,
    count: int = 4,
) -> List[ChainAgent]:
    """Set up chain agents."""
    agents: List[ChainAgent] = []

    for i in range(count):
        agent_id = f"agent_{i+1}"
        logger.info(f"Creating {agent_id}")

        agent = ChainAgent(
            config=AgentConfig(
                agent_id=agent_id,
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

    return agents


async def setup_chain(agents: List[ChainAgent]) -> None:
    """Configure the agent chain."""
    logger.info("Setting up agent chain")
    for i, agent in enumerate(agents):
        next_idx = (i + 1) % len(agents)
        await agent.set_next_agent(agents[next_idx].id)


async def run_chain(first_agent: ChainAgent) -> bool:
    """Run the chain and wait for completion or shutdown."""
    logger.info("Starting message chain")
    asyncio.create_task(first_agent.start_chain(), name="chain_task")

    return await first_agent.chain_complete.wait()


async def main() -> None:
    """Main entry point for the chain example."""
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    logger.info("Starting chain example")

    async with mas_service() as context:
        transport = context.transport
        persistence = context.persistence

        async with AsyncExitStack() as stack:
            try:
                # Set up agents
                agents = await setup_agents(transport, persistence)

                # Start all agents
                logger.info("Starting agents...")
                for agent in agents:
                    await agent.start()
                    stack.push_async_callback(agent.stop)
                    logger.info(f"Agent {agent.id} started")

                # Configure and run chain
                await setup_chain(agents)
                await asyncio.sleep(1)  # Wait for subscriptions

                success = await run_chain(agents[0])

                if success:
                    logger.info("Chain completed successfully")
                else:
                    logger.info("Chain interrupted by shutdown request")

            except Exception as e:
                logger.error(f"Error in chain example: {e}")
                raise


if __name__ == "__main__":
    asyncio.run(main())
