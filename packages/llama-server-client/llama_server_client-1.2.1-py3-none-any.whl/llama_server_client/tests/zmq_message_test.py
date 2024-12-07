import uuid
from datetime import datetime, timezone
import zmq

from llama_server_client.schema.zmq_message_header import ZmqMessageHeader, ZmqMessageType


def test_msgpack_zmq_message_header():
    message_header = ZmqMessageHeader(
        zmq_message_id=uuid.uuid4(),
        message_type=ZmqMessageType.CHAT_COMPLETION,
        request_ts=datetime.now(tz=timezone.utc)
    )
    print(message_header.to_json_str())

    packed = message_header.msgpack_pack()

    message_header_unpacked = ZmqMessageHeader.msgpack_unpack(packed)

    assert message_header == message_header_unpacked

    print(message_header_unpacked.to_json_str())


def test_zmq_message_header_send():
    host = "tcp://localhost:5555"
    timeout = 15000
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.RCVTIMEO, timeout)
    socket.connect(host)

    message_header = ZmqMessageHeader(
        zmq_message_id=uuid.uuid4(),
        message_type=ZmqMessageType.CHAT_COMPLETION,
        request_ts=datetime.now(tz=timezone.utc)
    )
    print(message_header.to_json_str())

    packed = message_header.msgpack_pack()

    socket.send(packed)
    resp_raw = socket.recv()

    response_message_header = ZmqMessageHeader.msgpack_unpack(resp_raw)

    print(response_message_header.to_json_str())
