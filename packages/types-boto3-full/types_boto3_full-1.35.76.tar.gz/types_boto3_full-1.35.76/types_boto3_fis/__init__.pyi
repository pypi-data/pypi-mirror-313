"""
Main interface for fis service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_fis import (
        Client,
        FISClient,
    )

    session = Session()
    client: FISClient = session.client("fis")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import FISClient

Client = FISClient

__all__ = ("Client", "FISClient")
