import asyncio
from typing import Any, Optional

from mas.logger import get_logger
from mas.protocol import Message, MessageType
from mas.sdk.agent import Agent

logger = get_logger()


class ChainAgent(Agent):
    """Base agent that participates in the message chain."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.next_agent_id: Optional[str] = None
        self.received_count = 0
        self.chain_complete = asyncio.Event()

    async def initialize(self) -> None:
        """Initialize the agent."""
        logger.info(f"Agent {self.id} initializing...")
        await self._initialize()

    async def _initialize(self) -> None:
        """Nothing to initialize for chain agent."""
        pass

    async def _cleanup(self) -> None:
        """Nothing to clean up."""
        pass

    async def set_next_agent(self, agent_id: str) -> None:
        """Set the next agent in the chain."""
        self.next_agent_id = agent_id

    async def start_chain(self) -> None:
        """Start the message chain."""
        logger.info(f"Agent {self.id} starting chain")
        if not self.next_agent_id:
            raise RuntimeError("Next agent not set")

        logger.info(f"Agent {self.id} sending initial message to {self.next_agent_id}")
        await self.send_message(
            target_id=self.next_agent_id,
            content={"chain_count": 1},
        )

    async def _handle_agent_message(self, message: Message) -> None:
        """Handle incoming chain message."""
        if message.message_type == MessageType.AGENT_MESSAGE:
            count = message.payload["chain_count"]
            logger.info(f"Agent {self.id} received message (count: {count})")

            self.received_count += 1

            # If this is the 4th pass (back to agent 1), complete the chain
            if count >= 4:
                logger.info(f"Chain complete at agent {self.id}")
                self.chain_complete.set()
                return

            # Forward to next agent
            if self.next_agent_id:
                logger.info(
                    f"Agent {self.id} forwarding to {self.next_agent_id} (count: {count + 1})"
                )
                await self.send_message(
                    target_id=self.next_agent_id,
                    content={"chain_count": count + 1},
                )
