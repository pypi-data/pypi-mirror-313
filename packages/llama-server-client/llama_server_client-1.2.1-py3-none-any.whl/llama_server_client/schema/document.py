from dataclasses import dataclass
from typing import List

from llama_server_client.schema import Base
from llama_server_client.schema.split import Split
from llama_server_client.schema.summary import Summary


@dataclass
class Document(Base):
    """
    Dataclass representing a Document response.
    """
    document_id: int
    document_url: str
    splits: List[Split]
    summaries: List[Summary]
