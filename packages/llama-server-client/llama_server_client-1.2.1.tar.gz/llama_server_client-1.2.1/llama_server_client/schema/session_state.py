from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID

from llama_server_client.schema.base import Base


@dataclass
class SessionState(Base):
    """
    Dataclass representing a session cache response.
    """
    key: int
    session: UUID
    user: UUID
    exist: bool
    create_ts: Optional[datetime] = None
    update_ts: Optional[datetime] = None
    session_prompt: Optional[str] = None
    session_tokens: Optional[List[int]] = None
    session_tokens_size: Optional[int] = None
    session_tokens_keep_size: Optional[int] = None
    context_truncated: Optional[bool] = None
    key_values: Optional[Dict[str, Any]] = None

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "session": UUID,
            "user": UUID,
            "create_ts": datetime,
            "update_ts": datetime,
        }


@dataclass
class SessionStateRequest(Base):
    """
    Dataclass representing a session cache request to the model.
    """
    session: UUID
    user: UUID

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "session": UUID,
            "user": UUID,
        }
