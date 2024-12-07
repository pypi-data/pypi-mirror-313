from dataclasses import dataclass

from llama_server_client.schema.base import Base


@dataclass
class HealthCheck(Base):
    """
    Dataclass representing a health check response.
    """
    status: str
    host: str
    worker_count: int
