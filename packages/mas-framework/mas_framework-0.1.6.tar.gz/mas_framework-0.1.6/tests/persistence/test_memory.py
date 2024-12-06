from datetime import UTC, datetime
from uuid import uuid4

import pytest

from mas.persistence.memory import InMemoryProvider
from mas.protocol import Agent, AgentStatus, Message, MessageType


@pytest.fixture
async def provider():
    """Provide a fresh InMemoryProvider instance."""
    provider = InMemoryProvider()
    await provider.initialize()
    try:
        return provider
    finally:
        await provider.cleanup()


@pytest.fixture
def sample_agent():
    """Create a sample agent for testing."""
    return Agent(
        id="test-agent",
        token="test-token",
        status=AgentStatus.ACTIVE,
        capabilities=["test"],
        metadata={"name": "Test Agent"},
        last_seen=datetime.now(UTC),
    )


@pytest.fixture
def sample_message():
    """Create a sample message for testing."""
    return Message(
        id=uuid4(),
        message_type=MessageType.AGENT_MESSAGE,
        sender_id="sender-agent",
        target_id="target-agent",
        timestamp=datetime.now(UTC),
        payload={"test": "data"},
    )


class TestInMemoryProvider:
    @pytest.mark.asyncio
    async def test_create_and_get_agent(self, provider, sample_agent):
        """Test creating and retrieving an agent."""
        provider = await provider

        # Create agent
        created = await provider.create_agent(sample_agent)
        assert created == sample_agent

        # Retrieve agent
        retrieved = await provider.get_agent(sample_agent.id)
        assert retrieved == sample_agent

    @pytest.mark.asyncio
    async def test_get_nonexistent_agent(self, provider):
        """Test retrieving a non-existent agent."""
        provider = await provider
        agent = await provider.get_agent("nonexistent")
        assert agent is None

    @pytest.mark.asyncio
    async def test_update_agent_status(self, provider, sample_agent):
        """Test updating agent status."""
        provider = await provider
        await provider.create_agent(sample_agent)

        # Update status
        success = await provider.update_agent_status(
            sample_agent.id, AgentStatus.INACTIVE
        )
        assert success is True

        # Verify update
        agent = await provider.get_agent(sample_agent.id)
        assert agent is not None
        assert agent.status == AgentStatus.INACTIVE

    @pytest.mark.asyncio
    async def test_get_active_agents(self, provider, sample_agent):
        """Test retrieving active agents."""
        provider = await provider

        # Create active agent
        await provider.create_agent(sample_agent)

        # Create inactive agent
        inactive_agent = Agent(
            id="inactive-agent",
            token="inactive-token",
            status=AgentStatus.INACTIVE,
            capabilities=[],
            metadata={},
            last_seen=datetime.now(UTC),
        )
        await provider.create_agent(inactive_agent)

        # Get active agents
        active_agents = await provider.get_active_agents()
        assert len(active_agents) == 1
        assert active_agents[0] == sample_agent

    @pytest.mark.asyncio
    async def test_delete_agent(self, provider, sample_agent):
        """Test deleting an agent."""
        provider = await provider
        await provider.create_agent(sample_agent)

        # Delete agent
        success = await provider.delete_agent(sample_agent.id)
        assert success is True

        # Verify deletion
        agent = await provider.get_agent(sample_agent.id)
        assert agent is None

    @pytest.mark.asyncio
    async def test_store_and_get_message(self, provider, sample_message):
        """Test storing and retrieving a message."""
        provider = await provider

        # Store message
        await provider.store_message(sample_message)

        # Retrieve message
        retrieved = await provider.get_message(sample_message.id)
        assert retrieved == sample_message

    @pytest.mark.asyncio
    async def test_get_agent_messages(self, provider, sample_message):
        """Test retrieving messages for an agent."""
        provider = await provider

        # Create agents for the message
        sender = Agent(
            id=sample_message.sender_id,
            token="sender-token",
            status=AgentStatus.ACTIVE,
            capabilities=[],
            metadata={},
            last_seen=datetime.now(UTC),
        )
        target = Agent(
            id=sample_message.target_id,
            token="target-token",
            status=AgentStatus.ACTIVE,
            capabilities=[],
            metadata={},
            last_seen=datetime.now(UTC),
        )

        await provider.create_agent(sender)
        await provider.create_agent(target)
        await provider.store_message(sample_message)

        # Get messages for sender
        sender_messages = await provider.get_agent_messages(sample_message.sender_id)
        assert len(sender_messages) == 1
        assert sender_messages[0] == sample_message

        # Get messages for target
        target_messages = await provider.get_agent_messages(sample_message.target_id)
        assert len(target_messages) == 1
        assert target_messages[0] == sample_message

    @pytest.mark.asyncio
    async def test_cleanup(self, provider, sample_agent, sample_message):
        """Test cleanup functionality."""
        provider = await provider

        # Add data
        await provider.create_agent(sample_agent)
        await provider.store_message(sample_message)

        # Cleanup
        await provider.cleanup()

        # Verify cleanup
        agent = await provider.get_agent(sample_agent.id)
        message = await provider.get_message(sample_message.id)
        assert agent is None
        assert message is None
