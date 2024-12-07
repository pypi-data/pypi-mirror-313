import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from uuid import UUID

from llama_server_client.schema.base import Base
from llama_server_client.schema.completion import ChatCompletion, ChatCompletionChunk
from llama_server_client.schema.health_check import HealthCheck
from llama_server_client.schema.session_state import SessionState


class ZmqMessageType(Enum):
    """
    ZmqMessageType defines the types of messages used in a ZeroMQ messaging system.
    Each type is associated with a specific class for handling its data.
    """
    COMPLETION = 1
    CHAT_COMPLETION = 2
    SESSION_STATE = 3
    HEALTH_CHECK = 4
    UNKNOWN = 5

    @property
    def get_associated_class(self):
        return {
            ZmqMessageType.COMPLETION: ChatCompletion,
            ZmqMessageType.CHAT_COMPLETION: ChatCompletion,
            ZmqMessageType.SESSION_STATE: SessionState,
            ZmqMessageType.HEALTH_CHECK: HealthCheck,
            ZmqMessageType.UNKNOWN: lambda x: None,
        }.get(self, lambda x: None)


class ZmqMessageStatus(Enum):
    """
    ZmqMessageStatus is an enumeration representing the status of a ZeroMQ message.
    It indicates whether a message was processed successfully or encountered an error.
    """
    SUCCESS = 1
    ERROR = 2


@dataclass
class ZmqMessageHeader(Base):
    """
    ZmqMessageHeader represents the header information of a ZeroMQ message.
    It contains essential data like message ID, type, status, and timestamps.
    """
    zmq_message_id: UUID
    message_type: ZmqMessageType
    has_more_message: bool = False
    status: Optional[ZmqMessageStatus] = None
    error_code: Optional[int] = None
    error_message: Optional[str] = None
    request_ts: Optional[datetime] = None
    response_ts: Optional[datetime] = None

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        """
        Provides a mapping for decoding the fields of a ZmqMessageHeader.

        :return: A dictionary where keys are field names and values are their corresponding data types.
        """
        return {
            "zmq_message_id": UUID,
            "message_type": ZmqMessageType,
            "status": ZmqMessageStatus,
            "request_ts": datetime,
            "response_ts": datetime,
        }


def create_message_header(message_type: ZmqMessageType) -> ZmqMessageHeader:
    """
    Creates and returns a new ZmqMessageHeader with a unique ID and the current timestamp.

    :param message_type: The type of the ZeroMQ message.
    :return: An instance of ZmqMessageHeader with the specified message type and other default values.
    """
    return ZmqMessageHeader(
        zmq_message_id=uuid.uuid4(),
        message_type=message_type,
        request_ts=datetime.now()
    )
