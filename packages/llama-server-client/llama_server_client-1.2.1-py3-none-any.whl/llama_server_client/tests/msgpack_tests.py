from uuid import UUID, uuid4
from dataclasses import dataclass
from typing import Optional, Dict, Any

import pytest
from polyfactory.factories import DataclassFactory

from llama_server_client.schema import Base
from llama_server_client.schema.completion import Message, ChatCompletionRequest, MessageRole, ChatCompletion
from llama_server_client.schema.session_state import SessionState


@dataclass
class MyMapClass(Base):
    dummy: str
    key_values: Optional[Dict[str, Any]] = None  # Optional key_values for advanced options

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "session": UUID,
        }


def test_map_class():
    """
    Test if the datetime encoding and decoding works correctly.
    """

    my_map_class = MyMapClass(
        dummy="test",
        key_values={"session": uuid4()}
    )

    print(my_map_class)

    packed = my_map_class.msgpack_pack()

    print(packed)

    unpacked = MyMapClass.msgpack_unpack(packed)

    print(unpacked)

    assert my_map_class == unpacked


def test_chat_completion_request():
    """
    Test if the datetime encoding and decoding works correctly.
    """

    message = Message(
        content="test",
        role=MessageRole.system
    )

    request = ChatCompletionRequest(
        messages=[message],
        model="test",
        logit_bias={300: 1.0},
        stop=["test"],
        user=uuid4(),
        key_values={"session": uuid4()}
    )
    print(request.to_json_str())

    packed = request.msgpack_pack()

    print(packed)

    unpacked = ChatCompletionRequest.msgpack_unpack(packed)

    print(unpacked.to_json_str())
    assert request == unpacked


class ChatCompletionRequestFactory(DataclassFactory[ChatCompletionRequest]):
    __model__ = ChatCompletionRequest


def test_chat_completion_request_factory():
    """
    Test if the datetime encoding and decoding works correctly.
    """
    request = ChatCompletionRequestFactory.build()

    print(request.to_json_str())

    packed = request.msgpack_pack()

    unpacked = ChatCompletionRequest.msgpack_unpack(packed)

    print(unpacked.to_json_str())

    assert request == unpacked


class ChatCompletionFactory(DataclassFactory[ChatCompletion]):
    __model__ = ChatCompletion


def test_chat_completion_factory():
    """
    Test if the datetime encoding and decoding works correctly.
    """
    completion = ChatCompletionFactory.build()

    print(completion.to_json_str())

    packed = completion.msgpack_pack()

    unpacked = ChatCompletion.msgpack_unpack(packed)

    print(unpacked.to_json_str())

    assert completion == unpacked


class SessionStateFactory(DataclassFactory[SessionState]):
    __model__ = SessionState


def test_session_state_factory():
    """
    Test if the datetime encoding and decoding works correctly.
    """
    session_state = SessionStateFactory.build()

    print(session_state.to_json_str())

    packed = session_state.msgpack_pack()

    unpacked = SessionState.msgpack_unpack(packed)

    print(unpacked.to_json_str())

    assert session_state == unpacked


if __name__ == "__main__":
    pytest.main()
