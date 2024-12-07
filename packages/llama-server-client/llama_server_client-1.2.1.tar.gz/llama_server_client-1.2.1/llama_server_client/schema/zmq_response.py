from dataclasses import dataclass

from llama_server_client.schema import Base
from llama_server_client.schema import ZmqMessageHeader
from llama_server_client.schema.base import T


@dataclass
class ZmqResponse(Base):
    header: ZmqMessageHeader
    body: T
