import asyncio
from datetime import UTC, datetime, timedelta
from typing import Any, List, Optional, Set

from mas.logger import get_logger
from mas.persistence.interfaces import IPersistenceProvider
from mas.protocol import Agent, AgentStatus

logger = get_logger()


class DiscoveryService:
    """Simple discovery service for agent registration and lookup."""

    def __init__(self, persistence: IPersistenceProvider):
        self.persistence = persistence
        self.active_timeout = timedelta(
            minutes=5
        )  # Consider agent inactive after 5 min
        self._tasks: List[asyncio.Task[Any]] = []
        self._running = False

    async def initialize(self) -> None:
        """Start the discovery service."""
        if self._running:
            return

        self._running = True
        self._tasks.append(asyncio.create_task(self._cleanup_inactive_agents()))

    async def _cleanup_inactive_agents(self) -> None:
        """Cleanup inactive agents."""
        while self._running:
            for agent in await self.persistence.get_active_agents():
                if agent.last_seen < datetime.now(UTC) - self.active_timeout:
                    await self.persistence.update_agent_status(
                        agent.id, AgentStatus.INACTIVE
                    )
            await asyncio.sleep(60)  # Check every minute

    async def cleanup(self) -> None:
        """Stop the discovery service."""
        self._running = False
        for task in self._tasks:
            try:
                task.cancel()
            except asyncio.CancelledError:
                pass
        self._tasks.clear()

    async def register_agent(
        self,
        agent_id: str,
        capabilities: Set[str],
    ) -> str:
        """Register an agent.

        Args:
            agent_id: Unique agent identifier
            capabilities: Set of agent capabilities
            endpoint: Agent's message endpoint

        Returns:
            Token for the agent
        """
        # Create simple token (in practice, use proper token generation)
        token = f"token_{agent_id}_{datetime.now(UTC).timestamp()}"

        # Store agent
        await self.persistence.create_agent(
            Agent(
                id=agent_id,
                status=AgentStatus.ACTIVE,
                capabilities=list(capabilities),
                token=token,
                metadata={},
            )
        )

        return token

    async def find_agents(
        self,
        capabilities: Optional[Set[str]] = None,
    ) -> List[Agent]:
        """Find agents matching capabilities.

        Args:
            capabilities: Optional set of required capabilities

        Returns:
            List of matching agents
        """
        # Get all active agents
        agents = await self.persistence.get_active_agents()

        if not capabilities:
            return agents

        # Filter by capabilities
        matching = [
            agent for agent in agents if capabilities.issubset(set(agent.capabilities))
        ]

        return matching

    async def update_status(self, agent_id: str, status: AgentStatus) -> bool:
        """Update agent status.

        Args:
            agent_id: Agent ID
            status: New status

        Returns:
            True if updated successfully
        """
        return await self.persistence.update_agent_status(agent_id, status)

    async def verify_token(self, agent_id: str, token: str) -> bool:
        """Verify agent's token.

        Args:
            agent_id: Agent ID
            token: Token to verify

        Returns:
            True if token is valid
        """
        agent = await self.persistence.get_agent(agent_id)
        return agent is not None and agent.token == token

    async def deregister_agent(self, agent_id: str) -> bool:
        """Remove agent registration.

        Args:
            agent_id: Agent ID to deregister

        Returns:
            True if deregistered successfully
        """
        return await self.persistence.delete_agent(agent_id)
