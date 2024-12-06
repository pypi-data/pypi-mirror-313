"""
Main interface for timestream-write service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_timestream_write import (
        Client,
        TimestreamWriteClient,
    )

    session = Session()
    client: TimestreamWriteClient = session.client("timestream-write")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import TimestreamWriteClient

Client = TimestreamWriteClient


__all__ = ("Client", "TimestreamWriteClient")
