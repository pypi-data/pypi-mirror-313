import multiprocessing
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List, Union, Iterable

import pytest

from llama_server_client.schema import HealthCheck, ZmqResponse, ZmqMessageHeader
from llama_server_client.client import LlamaClient
from llama_server_client.schema.completion import MessageRole, ChatCompletion, ChatCompletionChunk
from llama_server_client.schema.completion import Message, ChatCompletionRequest
from llama_server_client.schema.session_state import SessionState, SessionStateRequest


def send_chat_completion_request(client: LlamaClient, request: ChatCompletionRequest) -> Optional[
    Union[ChatCompletion, List[ChatCompletionChunk]]]:
    return client.send_chat_completion_request(request)


@pytest.fixture
def setup_client():
    host = "tcp://localhost:5555"
    timeout = 360000
    client = LlamaClient(host=host, timeout=timeout)
    return client


@pytest.fixture
def setup_chat_completion_request() -> ChatCompletionRequest:
    session_id = uuid.uuid4()
    user_id = uuid.uuid4()
    messages = [
        Message(role=MessageRole.system, content='You are a helpful assistant'),
        Message(role=MessageRole.user, content="What is the capital of Turkey?")
    ]
    stop = ["<|eot_id|>"]
    return ChatCompletionRequest(
        model='llama-3',
        messages=messages,
        temperature=0.8,
        max_tokens=256,
        stop=stop,
        stream=False,
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
    stop = ["<|eot_id|>"]
    return ChatCompletionRequest(
        model='llama-3',
        messages=messages,
        temperature=0.8,
        stream=False,
        n=1,
        max_tokens=256,
        stop=stop
    )


def test_session_state_request(setup_client, setup_session_state_request):
    try:
        response: SessionState = setup_client.send_session_state_request(setup_session_state_request)
        print(response.to_json_str())
        assert response is not None
        assert isinstance(response, SessionState)
    except TimeoutError as e:
        pytest.fail(str(e))


def test_session_state_request_raw_response(setup_client, setup_session_state_request):
    try:
        response: ZmqResponse = setup_client.send_session_state_request(
            setup_session_state_request,
            raw_response=True)

        assert isinstance(response.header, ZmqMessageHeader)
        assert isinstance(response.body, SessionState)
        print(response.header.to_json_str(indent=4))
        print(response.body.to_json_str(indent=4))
    except TimeoutError as e:
        pytest.fail(str(e))


def test_health_check_request(setup_client):
    try:
        response: HealthCheck = setup_client.send_health_check_request()
        print(response.to_json_str())
        assert response is not None
        assert isinstance(response, HealthCheck)
    except TimeoutError as e:
        pytest.fail(str(e))


def test_health_check_request_raw_response(setup_client):
    try:
        response: ZmqResponse = setup_client.send_health_check_request(raw_response=True)

        assert isinstance(response.header, ZmqMessageHeader)
        assert isinstance(response.body, HealthCheck)
        print(response.header.to_json_str(indent=4))
        print(response.body.to_json_str(indent=4))
    except TimeoutError as e:
        pytest.fail(str(e))


def test_chat_completion_request(setup_client, setup_chat_completion_request):
    setup_chat_completion_request.stream = False
    try:
        response: ChatCompletion = setup_client.send_chat_completion_request(setup_chat_completion_request)
        print(response.to_json_str())
        assert response is not None
        assert isinstance(response, ChatCompletion)
    except TimeoutError as e:
        pytest.fail(str(e))


def test_chat_completion_request_raw_response(setup_client, setup_chat_completion_request):
    setup_chat_completion_request.stream = False
    try:
        response: ZmqResponse = setup_client.send_chat_completion_request(
            setup_chat_completion_request,
            raw_response=True
        )
        assert isinstance(response.header, ZmqMessageHeader)
        assert isinstance(response.body, ChatCompletion)
        print(response.header.to_json_str(indent=4))
        print(response.body.to_json_str(indent=4))
    except TimeoutError as e:
        pytest.fail(str(e))


def test_chat_completion_request_stream(setup_client, setup_chat_completion_request):
    setup_chat_completion_request.stream = True
    try:
        responses = setup_client.send_chat_completion_request(setup_chat_completion_request)
        for response in responses:
            print(response.to_json_str(indent=4))
            assert response is not None
            assert isinstance(response, ChatCompletionChunk)
    except TimeoutError as e:
        pytest.fail(str(e))


def test_chat_completion_request_stream_raw_response(setup_client, setup_chat_completion_request):
    setup_chat_completion_request.stream = True
    try:
        responses: Iterable[ZmqResponse] = setup_client.send_chat_completion_request(
            setup_chat_completion_request,
            raw_response=True
        )
        for response in responses:
            assert isinstance(response.header, ZmqMessageHeader)
            assert isinstance(response.body, ChatCompletionChunk)
            print(response.header.to_json_str(indent=4))
            print(response.body.to_json_str(indent=4))
    except TimeoutError as e:
        pytest.fail(str(e))


def test_title_generation_request(setup_client, setup_title_generation_request):
    try:
        response: ChatCompletion = setup_client.send_chat_completion_request(setup_title_generation_request)
        print(response.to_json_str())
        assert response is not None
        assert isinstance(response, ChatCompletion)
    except TimeoutError as e:
        pytest.fail(str(e))


def test_mix_requests(setup_chat_completion_request, setup_title_generation_request):
    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = []
        client1 = LlamaClient('tcp://localhost:5555', timeout=360000)

        future1 = executor.submit(send_chat_completion_request, client1, setup_chat_completion_request)
        futures.append(future1)

        client2 = LlamaClient('tcp://localhost:5555', timeout=360000)

        future2 = executor.submit(send_chat_completion_request, client2, setup_title_generation_request)
        futures.append(future2)

        for future in futures:
            response = future.result()
            assert response is not None
            assert isinstance(response, ChatCompletion)


def test_parallel_mix_prompt_requests(setup_title_generation_request, setup_chat_completion_request):
    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = []
        client1 = LlamaClient('tcp://localhost:5555', timeout=360000)

        future1 = executor.submit(send_chat_completion_request, client1, setup_chat_completion_request)
        futures.append(future1)

        client2 = LlamaClient('tcp://localhost:5555', timeout=360000)

        future2 = executor.submit(send_chat_completion_request, client2, setup_title_generation_request)
        futures.append(future2)

        client3 = LlamaClient('tcp://localhost:5555', timeout=360000)

        future3 = executor.submit(send_chat_completion_request, client3, setup_chat_completion_request)
        futures.append(future3)

        for future in futures:
            response = future.result()
            assert response is not None
            assert isinstance(response, Union[ChatCompletion, ChatCompletionChunk])
            print(response.key_values["session"])
            print(response.choices[0].message.content)
