"""
Main interface for bedrock-runtime service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_bedrock_runtime import (
        BedrockRuntimeClient,
        Client,
        ListAsyncInvokesPaginator,
    )

    session = Session()
    client: BedrockRuntimeClient = session.client("bedrock-runtime")

    list_async_invokes_paginator: ListAsyncInvokesPaginator = client.get_paginator("list_async_invokes")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import BedrockRuntimeClient
from .paginator import ListAsyncInvokesPaginator

Client = BedrockRuntimeClient

__all__ = ("BedrockRuntimeClient", "Client", "ListAsyncInvokesPaginator")
