# Llama Server Client

Llama Server Client is a Python package that provides a ZMQ client for interacting with a TCP Llama Server that mimics
OpenAI's chat completion API.

## Features

- Uses ZMQ for efficient, low-latency communication.
- Accepts chat completion requests in a similar format to OpenAI's API.
- Returns responses that closely match OpenAI's response format.
- Includes an Unpacker for handling flattened message responses.
