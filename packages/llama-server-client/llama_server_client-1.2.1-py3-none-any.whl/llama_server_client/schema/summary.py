from dataclasses import dataclass
from typing import Optional, List

from llama_server_client.schema import Base


@dataclass
class Summary(Base):
    """
    Dataclass representing a Summary response.
    """
    summary_id: int
    document_id: int
    split_id: int
    split_sequence_id: int
    text_content: str
    token_len: int
    tokens: Optional[List[int]]
    centrality: float