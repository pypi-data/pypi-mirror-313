from datetime import UTC, datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field

from .types import AgentStatus


def datetime_utc_now():
    return datetime.now(UTC)


class Agent(BaseModel):
    """Agent data model."""

    id: str
    status: AgentStatus
    capabilities: List[str]
    token: str
    endpoint_url: str
    metadata: Dict[str, Any] = {}
    last_seen: datetime = Field(default_factory=datetime_utc_now)
