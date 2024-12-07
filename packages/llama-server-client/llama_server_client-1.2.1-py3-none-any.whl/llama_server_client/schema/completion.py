from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, Literal, Any
from uuid import UUID

from llama_server_client.schema.base import Base


class MessageRole(Enum):
    assistant = 1
    system = 2
    user = 3


@dataclass
class Message(Base):
    """
    Dataclass representing a message in the request.
    """
    content: str  # Content of the message
    role: MessageRole  # Role of the message


@dataclass
class Delta(Base):
    content: str
    role: MessageRole


class FinishReason(Enum):
    stop = 1
    length = 2
    content_filter = 3


@dataclass
class ChatCompletionChoice:
    """
    Dataclass representing a choice in a chat completion.
    """
    finish_reason: Optional[FinishReason]  # Reason for finishing the choice
    index: int  # Index of the choice
    message: Optional[Message]  # Message associated with the choice
    delta: Optional[Delta]  # Delta associated with the choice


@dataclass
class ChatCompletionUsage:
    """
    Dataclass representing the usage statistics of a chat completion.
    """
    completion_tokens: int  # Number of tokens in the completion
    prompt_tokens: int  # Number of tokens in the prompt
    total_tokens: int  # Total number of tokens (prompt + completion)


@dataclass
class ChatCompletion(Base):
    """
    Dataclass representing a chat completion.
    """
    id: str  # Unique identifier for the completion
    choices: List[ChatCompletionChoice]  # List of choices in the completion
    created: int  # Timestamp of when the completion was created
    model: str  # Name of the model to be used
    object: Literal["chat.completion"]  # Type of the object (always "chat_completion" for this class)
    usage: ChatCompletionUsage  # Usage statistics for the completion
    system_fingerprint: Optional[str] = None  # Fingerprint of the system
    key_values: Optional[Dict[str, Any]] = None  # Optional key_values for advanced options

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "role": MessageRole,
            "finish_reason": FinishReason,
            "session": UUID
        }


@dataclass
class ChatCompletionChunk(Base):
    """
    Dataclass representing a chat completion chunk.
    """
    id: str  # Unique identifier for the completion
    choices: List[ChatCompletionChoice]  # List of choices in the completion
    created: int  # Timestamp of when the completion was created
    model: str  # Name of the model to be used
    object: Literal["chat.completion.chunk"]  # Type of the object (always "chat_completion_chunk" for this class)
    usage: Optional[ChatCompletionUsage]  # Usage statistics for the completion
    system_fingerprint: Optional[str] = None  # Fingerprint of the system
    key_values: Optional[Dict[str, Any]] = None  # Optional key_values for advanced options

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "role": MessageRole,
            "finish_reason": FinishReason,
            "session": UUID
        }


class ResponseFormatType(Enum):
    json_object = 1
    text = 2


@dataclass
class ResponseFormat(Base):
    """
    Dataclass representing the response format of a chat completion.
    """
    type: ResponseFormatType


@dataclass
class CompletionRequest(Base):
    """
    Dataclass representing a completion request to the model.
    """
    model: str  # Name of the model to be used
    prompt: str # Prompt for the model
    suffix: str # Suffix
    frequency_penalty: Optional[float] = 0.0  # Penalty for frequent tokens in the output
    logit_bias: Optional[Dict[int, float]] = None  # Bias for certain tokens in the output
    max_tokens: Optional[int] = 2 ** 31 - 1  # Maximum number of tokens in the output
    n: Optional[int] = 1  # Number of completions to generate
    presence_penalty: Optional[float] = 0.0  # Penalty for new tokens in the output
    response_format: Optional[ResponseFormat] = None  # Format of the response
    seed: Optional[int] = None  # Seed for the random number generator
    stop: Optional[List[str]] = None  # List of tokens to stop the generation
    stream: Optional[bool] = False  # Whether to stream the output
    temperature: Optional[float] = 1.0  # Sampling temperature for the model's output
    top_p: Optional[float] = 1.0  # Nucleus sampling parameter
    user: Optional[UUID] = None  # Optional user identifier for the request
    key_values: Optional[Dict[str, Any]] = None  # Optional key_values for advanced options

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
            "role": MessageRole,
            "type": ResponseFormatType,
            "session": UUID
        }


@dataclass
class ChatCompletionRequest(Base):
    """
    Dataclass representing a chat completion request to the model.
    """
    messages: List[Message]  # List of messages in the request
    model: str  # Name of the model to be used
    frequency_penalty: Optional[float] = 0.0  # Penalty for frequent tokens in the output
    logit_bias: Optional[Dict[int, float]] = None  # Bias for certain tokens in the output
    max_tokens: Optional[int] = 2 ** 31 - 1  # Maximum number of tokens in the output
    n: Optional[int] = 1  # Number of completions to generate
    presence_penalty: Optional[float] = 0.0  # Penalty for new tokens in the output
    response_format: Optional[ResponseFormat] = None  # Format of the response
    seed: Optional[int] = None  # Seed for the random number generator
    stop: Optional[List[str]] = None  # List of tokens to stop the generation
    stream: Optional[bool] = False  # Whether to stream the output
    temperature: Optional[float] = 1.0  # Sampling temperature for the model's output
    top_p: Optional[float] = 1.0  # Nucleus sampling parameter
    user: Optional[UUID] = None  # Optional user identifier for the request
    key_values: Optional[Dict[str, Any]] = None  # Optional key_values for advanced options

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
            "role": MessageRole,
            "type": ResponseFormatType,
            "session": UUID
        }
