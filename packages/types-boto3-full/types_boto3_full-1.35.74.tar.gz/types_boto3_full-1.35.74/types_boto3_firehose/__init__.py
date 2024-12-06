"""
Main interface for firehose service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_firehose import (
        Client,
        FirehoseClient,
    )

    session = Session()
    client: FirehoseClient = session.client("firehose")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import FirehoseClient

Client = FirehoseClient


__all__ = ("Client", "FirehoseClient")
