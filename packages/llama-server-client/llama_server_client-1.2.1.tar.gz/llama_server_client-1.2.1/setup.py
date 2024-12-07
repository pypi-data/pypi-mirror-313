from setuptools import setup, find_packages

setup(
    name="llama_server_client",
    version="1.2.1",
    packages=find_packages(),
    package_data={'llama_server_client': ['schema/*']},
    author="Anil Aydiner",
    author_email="a.aydiner@qimia.de",
    description="A ZMQ client interface for llama server",
    long_description="Llama Server Client is a Python package that provides a ZMQ client for interacting with a TCP "
                     "Llama server that mimics"
                     "OpenAI's chat completion API.",
    url="https://github.com/Qimia/llama-server-client",
    python_requires=">=3.11",
    install_requires=[
        "pyzmq>=25.1.1",
        "msgpack>=1.0.7",
        "dacite>=1.8.1"
    ],
    extras_require={
        "tests": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.23.2",
            "polyfactory>=2.5.0",
        ]
    }
)
