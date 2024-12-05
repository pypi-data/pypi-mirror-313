"""
Main interface for bedrock-runtime service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_bedrock_runtime import (
        BedrockRuntimeClient,
        Client,
    )

    session = Session()
    client: BedrockRuntimeClient = session.client("bedrock-runtime")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import BedrockRuntimeClient

Client = BedrockRuntimeClient

__all__ = ("BedrockRuntimeClient", "Client")
