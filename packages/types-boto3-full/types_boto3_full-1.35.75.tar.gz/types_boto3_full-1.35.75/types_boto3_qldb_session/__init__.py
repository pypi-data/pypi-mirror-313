"""
Main interface for qldb-session service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_qldb_session import (
        Client,
        QLDBSessionClient,
    )

    session = Session()
    client: QLDBSessionClient = session.client("qldb-session")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import QLDBSessionClient

Client = QLDBSessionClient


__all__ = ("Client", "QLDBSessionClient")
