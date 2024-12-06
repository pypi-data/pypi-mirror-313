from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .types import MessageType


class Message(BaseModel):
    """Base message type."""

    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sender_id: str
    target_id: str
    message_type: MessageType
    payload: Dict[str, Any]
