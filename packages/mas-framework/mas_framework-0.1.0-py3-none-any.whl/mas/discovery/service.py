from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set

from mas.persistence.interfaces import IPersistenceProvider
from mas.protocol import AgentStatus


class DiscoveryService:
    """Simple discovery service for agent registration and lookup."""

    def __init__(self, persistence: IPersistenceProvider):
        self.persistence = persistence
        self.active_timeout = timedelta(
            minutes=5
        )  # Consider agent inactive after 5 min

    async def register_agent(
        self,
        agent_id: str,
        capabilities: Set[str],
        endpoint: str,
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
        token = f"token_{agent_id}_{datetime.utcnow().timestamp()}"

        # Store agent
        await self.persistence.create_agent(
            id=agent_id,
            status=AgentStatus.ACTIVE,
            capabilities=list(capabilities),
            token=token,
            endpoint_url=endpoint,
        )

        return token

    async def find_agents(
        self,
        capabilities: Optional[Set[str]] = None,
    ) -> List[Dict]:
        """Find agents matching capabilities.

        Args:
            capabilities: Optional set of required capabilities

        Returns:
            List of matching agents
        """
        # Get all active agents
        agents = await self.persistence.get_active_agents()

        if not capabilities:
            return [self._format_agent(agent) for agent in agents]

        # Filter by capabilities
        matching = [
            agent for agent in agents if capabilities.issubset(set(agent.capabilities))
        ]

        return [self._format_agent(agent) for agent in matching]

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

    def _format_agent(self, agent) -> Dict:
        """Format agent data for response."""
        return {
            "id": agent.id,
            "status": agent.status,
            "capabilities": agent.capabilities,
            "endpoint": agent.endpoint_url,
            "last_seen": agent.last_seen.isoformat(),
        }
