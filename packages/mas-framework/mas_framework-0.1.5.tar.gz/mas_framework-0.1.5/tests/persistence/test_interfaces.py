from typing import List, Optional
from uuid import UUID


from mas.persistence.interfaces import IPersistenceProvider
from mas.protocol import Agent, AgentStatus, Message


class MockPersistenceProvider(IPersistenceProvider):
    """Mock implementation to test interface compliance."""

    async def initialize(self) -> None:
        pass

    async def cleanup(self) -> None:
        pass

    async def create_agent(self, agent: Agent) -> Agent:
        return agent

    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        return None

    async def update_agent_status(self, agent_id: str, status: AgentStatus) -> bool:
        return True

    async def get_active_agents(self) -> List[Agent]:
        return []

    async def delete_agent(self, agent_id: str) -> bool:
        return True

    async def store_message(self, message: Message) -> None:
        pass

    async def get_message(self, message_id: UUID) -> Optional[Message]:
        return None

    async def get_agent_messages(self, agent_id: str) -> List[Message]:
        return []


def test_interface_compliance():
    """Test that the interface can be implemented."""
    provider = MockPersistenceProvider()
    assert isinstance(provider, IPersistenceProvider)
