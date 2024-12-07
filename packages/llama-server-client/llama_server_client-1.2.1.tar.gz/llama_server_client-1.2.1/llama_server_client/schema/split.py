from dataclasses import dataclass
from typing import List

from llama_server_client.schema import Base
from llama_server_client.schema.summary import Summary


@dataclass
class Split(Base):
    """
    Dataclass representing a Split response.
    """
    split_id: int
    sequence_id: int
    doc_id: int
    text_content: str
    token_len: int
    summaries: List[Summary]
