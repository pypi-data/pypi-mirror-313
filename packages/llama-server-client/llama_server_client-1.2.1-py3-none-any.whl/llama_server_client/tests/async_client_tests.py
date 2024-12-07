import asyncio
import uuid
from typing import Optional, List, Union, AsyncIterable

import pytest

from llama_server_client import AsyncLlamaClient
from llama_server_client.schema import HealthCheck, ZmqMessageHeader
from llama_server_client.client import LlamaClient
from llama_server_client.schema.completion import MessageRole, ChatCompletion, ChatCompletionChunk, CompletionRequest
from llama_server_client.schema.completion import Message, ChatCompletionRequest
from llama_server_client.schema.session_state import SessionState, SessionStateRequest
from llama_server_client.schema.zmq_response import ZmqResponse


def send_chat_completion_request(client: LlamaClient, request: ChatCompletionRequest) -> Optional[
    Union[ChatCompletion, List[ChatCompletionChunk]]]:
    return client.send_chat_completion_request(request)


@pytest.fixture
def setup_client():
    timeout: int = 360000
    host = "tcp://localhost:5555"
    client = AsyncLlamaClient(host=host, timeout=timeout)
    return client


@pytest.fixture
def setup_chat_completion_request() -> ChatCompletionRequest:
    session_id = uuid.uuid4()
    user_id = uuid.uuid4()
    messages = [
        Message(role=MessageRole.system, content='You are a helpful assistant'),
        Message(role=MessageRole.user, content="What is the capital of Turkey?")
    ]
    stop = ["<|eot_id>|"]
    return ChatCompletionRequest(
        model='llama-3',
        messages=messages,
        temperature=0.8,
        max_tokens=256,
        stop=stop,
        stream=True,
        user=user_id,
        key_values={"session": session_id}
    )


@pytest.fixture
def setup_fim_request() -> CompletionRequest:
    session_id = uuid.uuid4()
    user_id = uuid.uuid4()

    prefix = (
        "def calculate_area(radius):\n"
        "    # Calculate the area of a circle given the radius\n"
        "    pi = 3.14\n"
    )

    suffix = (
        "    return area\n"
        "\n"
        "# Example usage\n"
        "result = calculate_area(5)"
    )

    stop = ["<|im_end|>"]

    return CompletionRequest(
        model='Gwen-Coder',
        prompt=prefix,
        suffix=suffix,
        temperature=0.8,
        max_tokens=256,
        stop=stop,
        stream=True,
        user=user_id,
        key_values={"session": session_id}
    )


@pytest.fixture
def setup_session_state_request() -> SessionStateRequest:
    session_id = uuid.uuid4()
    user_id = uuid.uuid4()
    return SessionStateRequest(
        session=session_id,
        user=user_id,
    )


@pytest.fixture
def setup_title_generation_request() -> ChatCompletionRequest:
    messages = [
        Message(
            role=MessageRole.system,
            content="You are a helpful assistant. You generate a descriptive, short and meaningful title for the given "
                    "conversation.",
        ),
        Message(
            role=MessageRole.user,
            content=f"Question: What is the capital of France? Answer: The capital of France is Paris"
        )
    ]
    stop = ["<|eot_id>|"]
    return ChatCompletionRequest(
        model='llama-3',
        messages=messages,
        temperature=0.8,
        stream=False,
        n=1,
        max_tokens=256,
        stop=stop
    )


@pytest.mark.asyncio
async def test_session_state_request(setup_client, setup_session_state_request):
    try:
        response: SessionState = await setup_client.send_session_state_request(setup_session_state_request)
        print(response.to_json_str(indent=4))
        assert response is not None
        assert isinstance(response, SessionState)
    except TimeoutError as e:
        pytest.fail(str(e))


@pytest.mark.asyncio
async def test_session_state_request_raw_response(setup_client, setup_session_state_request):
    try:
        response: ZmqResponse = await setup_client.send_session_state_request(
            setup_session_state_request,
            raw_response=True)

        assert isinstance(response.header, ZmqMessageHeader)
        assert isinstance(response.body, SessionState)
        print(response.header.to_json_str(indent=4))
        print(response.body.to_json_str(indent=4))
    except TimeoutError as e:
        pytest.fail(str(e))


@pytest.mark.asyncio
async def test_health_check_request(setup_client):
    try:
        response: HealthCheck = await setup_client.send_health_check_request()
        print(response.to_json_str(indent=4))
        assert response is not None
        assert isinstance(response, HealthCheck)
    except TimeoutError as e:
        pytest.fail(str(e))


@pytest.mark.asyncio
async def test_health_check_request_raw_response(setup_client):
    try:
        response: ZmqResponse = await setup_client.send_health_check_request(raw_response=True)

        assert isinstance(response.header, ZmqMessageHeader)
        assert isinstance(response.body, HealthCheck)
        print(response.header.to_json_str(indent=4))
        print(response.body.to_json_str(indent=4))
    except TimeoutError as e:
        pytest.fail(str(e))


@pytest.mark.asyncio
async def test_chat_completion_request(setup_client, setup_chat_completion_request):
    setup_chat_completion_request.stream = False
    try:
        response: ChatCompletion = await setup_client.send_chat_completion_request(setup_chat_completion_request)
        print(response.to_json_str(indent=4))
        assert response is not None
        assert isinstance(response, ChatCompletion)
    except TimeoutError as e:
        pytest.fail(str(e))

@pytest.mark.asyncio
async def test_completion_request(setup_client, setup_fim_request):
    setup_fim_request.stream = False
    try:
        response: ChatCompletion = await setup_client.send_completion_request(setup_fim_request)
        print(response.to_json_str(indent=4))
        assert response is not None
        assert isinstance(response, ChatCompletion)
    except TimeoutError as e:
        pytest.fail(str(e))


@pytest.mark.asyncio
async def test_chat_completion_request_raw_response(setup_client, setup_chat_completion_request):
    setup_chat_completion_request.stream = False
    try:
        response: ZmqResponse = await setup_client.send_chat_completion_request(
            setup_chat_completion_request,
            raw_response=True
        )
        assert isinstance(response.header, ZmqMessageHeader)
        assert isinstance(response.body, ChatCompletion)
        print(response.header.to_json_str(indent=4))
        print(response.body.to_json_str(indent=4))
    except TimeoutError as e:
        pytest.fail(str(e))


@pytest.mark.asyncio
async def test_chat_completion_request_stream(setup_client, setup_chat_completion_request):
    setup_chat_completion_request.stream = True
    print(setup_chat_completion_request)
    try:
        responses = await setup_client.send_chat_completion_request(setup_chat_completion_request)
        async for response in responses:
            print(response.to_json_str(indent=4))
            assert response is not None
            assert isinstance(response, ChatCompletionChunk)
    except TimeoutError as e:
        pytest.fail(str(e))


@pytest.mark.asyncio
async def test_chat_completion_request_stream_raw_response(setup_client, setup_chat_completion_request):
    setup_chat_completion_request.stream = True
    try:
        responses: AsyncIterable[ZmqResponse] = await setup_client.send_chat_completion_request(
            setup_chat_completion_request,
            raw_response=True
        )
        async for response in responses:
            assert isinstance(response.header, ZmqMessageHeader)
            assert isinstance(response.body, ChatCompletionChunk)
            print(response.header.to_json_str(indent=4))
            print(response.body.to_json_str(indent=4))
    except TimeoutError as e:
        pytest.fail(str(e))


@pytest.mark.asyncio
async def test_title_generation_request(setup_client, setup_title_generation_request):
    try:
        response: ChatCompletion = await setup_client.send_chat_completion_request(setup_title_generation_request)
        print(response.to_json_str(indent=4))
        assert response is not None
        assert isinstance(response, ChatCompletion)
    except TimeoutError as e:
        pytest.fail(str(e))


@pytest.mark.asyncio
async def test_mix_requests(setup_chat_completion_request, setup_title_generation_request):
    client1 = AsyncLlamaClient('tcp://localhost:5555', timeout=360000)
    client2 = AsyncLlamaClient('tcp://localhost:5555', timeout=360000)

    async def send_request(client, request):
        return await client.send_chat_completion_request(request)

    response1, response2 = await asyncio.gather(
        send_request(client1, setup_chat_completion_request),
        send_request(client2, setup_title_generation_request)
    )
    client1.close()
    client2.close()

    assert response1 is not None
    assert isinstance(response1, ChatCompletion)
    print(response1.to_json_str(indent=4))
    assert response2 is not None
    assert isinstance(response2, ChatCompletion)
    print(response2.to_json_str(indent=4))
