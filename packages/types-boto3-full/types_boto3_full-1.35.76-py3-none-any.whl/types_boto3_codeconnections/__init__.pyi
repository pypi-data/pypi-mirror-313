"""
Main interface for codeconnections service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_codeconnections import (
        Client,
        CodeConnectionsClient,
    )

    session = Session()
    client: CodeConnectionsClient = session.client("codeconnections")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CodeConnectionsClient

Client = CodeConnectionsClient

__all__ = ("Client", "CodeConnectionsClient")
