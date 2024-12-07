from llama_server_client.schema.zmq_message_header import ZmqMessageHeader


class LlamaClientError(Exception):
    """
    Custom exception class for LlamaClient errors.

    This exception class represents errors within the LlamaClient, including detailed
    information from the ZmqMessageHeader for context.

    Attributes:
        header (ZmqMessageHeader): The header of the ZMQ message associated with the error.
        additional_info (str): Additional context about the error.
        message_id (UUID): The ID of the ZMQ message.
        message_type (ZmqMessageType): The type of the ZMQ message.
        status (ZmqMessageStatus): The status of the ZMQ message.
        error_code (int): The error code associated with the ZMQ message.
        error_message (str): The error message associated with the ZMQ message.
        request_ts (datetime): The timestamp when the request was made.
        response_ts (datetime): The timestamp when the response was received.
    """

    def __init__(self, header: ZmqMessageHeader, additional_info: str = ""):
        """
        Initializes a new instance of the LlamaClientError.

        Args:
            header (ZmqMessageHeader): The ZMQ message header associated with the error.
            additional_info (str, optional): Additional context about the error. Defaults to an empty string.
        """
        self.header = header
        self.additional_info = additional_info

        self.message_id = header.zmq_message_id
        self.message_type = header.message_type
        self.status = header.status
        self.error_code = header.error_code
        self.error_message = header.error_message
        self.request_ts = header.request_ts
        self.response_ts = header.response_ts

        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """
        Formats the error message with details from the header and any additional info.

        Returns:
            str: The formatted error message.
        """
        header_info = [
            "Message ID: {}".format(self.message_id),
            "Type: {}".format(self.message_type),
            "Status: {}".format(self.status),
            "Request Timestamp: {}".format(self.request_ts),
            "Response Timestamp: {}".format(self.response_ts)
        ]

        error_info = "Error Code: {}, Message: {}".format(self.error_code, self.error_message)

        message_parts = ["LlamaClient Error: {}".format(error_info)]
        if self.additional_info:
            message_parts.append("Additional Info: {}".format(self.additional_info))

        message_parts.append("Header Info: {}".format(", ".join(header_info)))

        return "\n".join(message_parts)
