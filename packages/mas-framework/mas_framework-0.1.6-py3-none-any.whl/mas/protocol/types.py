from enum import Enum


class MessageType(str, Enum):
    """Core message types."""

    # Basic types
    ERROR = "error"
    COMMAND = "command"
    RESPONSE = "response"
    STATUS_UPDATE = "status.update"
    STATUS_UPDATE_RESPONSE = "status.update.response"

    # Registration
    REGISTRATION_REQUEST = "registration.request"
    REGISTRATION_RESPONSE = "registration.response"

    # Agent messages
    AGENT_MESSAGE = "agent.message"
    DISCOVERY_REQUEST = "discovery.request"
    DISCOVERY_RESPONSE = "discovery.response"


class AgentStatus(str, Enum):
    """Simplified agent status."""

    ACTIVE = "active"
    INACTIVE = "inactive"
