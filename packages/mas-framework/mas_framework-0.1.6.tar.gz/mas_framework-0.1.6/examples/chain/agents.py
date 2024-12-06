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
        self._message_handler: Optional[asyncio.Task] = None

    async def _initialize(self) -> None:
        """Initialize chain-specific resources."""
        logger.debug(f"Initializing chain agent {self.id}")
        # Any chain-specific initialization can go here
        pass

    async def _cleanup(self) -> None:
        """Cleanup chain-specific resources."""
        logger.debug(f"Cleaning up chain agent {self.id}")
        if self.chain_complete.is_set():
            logger.info(f"Agent {self.id} completed chain successfully")
        # Any chain-specific cleanup can go here
        pass

    async def set_next_agent(self, agent_id: str) -> None:
        """Set the next agent in the chain."""
        if not self._running:
            raise RuntimeError("Agent must be running to set next agent")

        self.next_agent_id = agent_id
        logger.debug(f"Agent {self.id} set next agent to {agent_id}")

    async def start_chain(self) -> None:
        """Start the message chain."""
        if not self._running:
            raise RuntimeError("Agent must be running to start chain")

        if not self.next_agent_id:
            raise RuntimeError("Next agent not set")

        logger.info(f"Agent {self.id} starting chain")
        try:
            await self.send_message(
                target_id=self.next_agent_id,
                content={"chain_count": 1},
            )
            logger.debug(f"Agent {self.id} sent initial chain message")
        except Exception as e:
            logger.error(f"Failed to start chain: {e}")
            self.chain_complete.set()  # Signal completion on error
            raise

    async def _handle_agent_message(self, message: Message) -> None:
        """Handle incoming chain message."""
        try:
            if not self._running:
                logger.debug(f"Agent {self.id} ignoring message while not running")
                return

            if message.message_type != MessageType.AGENT_MESSAGE:
                logger.warning(
                    f"Agent {self.id} received unexpected message type: {message.message_type}"
                )
                return

            count = message.payload.get("chain_count")
            if count is None:
                logger.error(f"Agent {self.id} received message without chain count")
                return

            logger.info(f"Agent {self.id} received message (count: {count})")
            self.received_count += 1

            # If this is the 4th pass (back to agent 1), complete the chain
            if count >= 4:
                logger.info(f"Chain complete at agent {self.id}")
                self.chain_complete.set()
                return

            # Forward to next agent if we're still running
            if self.next_agent_id and self._running:
                logger.info(
                    f"Agent {self.id} forwarding to {self.next_agent_id} (count: {count + 1})"
                )
                await self.send_message(
                    target_id=self.next_agent_id,
                    content={"chain_count": count + 1},
                )
                logger.debug(f"Agent {self.id} forwarded chain message successfully")

        except Exception as e:
            logger.error(f"Error handling chain message in agent {self.id}: {e}")
            self.chain_complete.set()  # Signal completion on error
            raise
