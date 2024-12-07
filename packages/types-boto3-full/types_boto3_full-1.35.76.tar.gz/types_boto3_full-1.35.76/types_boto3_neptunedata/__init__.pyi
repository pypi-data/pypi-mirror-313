"""
Main interface for neptunedata service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_neptunedata import (
        Client,
        NeptuneDataClient,
    )

    session = Session()
    client: NeptuneDataClient = session.client("neptunedata")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import NeptuneDataClient

Client = NeptuneDataClient

__all__ = ("Client", "NeptuneDataClient")
