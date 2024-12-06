"""
Main interface for appconfigdata service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_appconfigdata import (
        AppConfigDataClient,
        Client,
    )

    session = Session()
    client: AppConfigDataClient = session.client("appconfigdata")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import AppConfigDataClient

Client = AppConfigDataClient


__all__ = ("AppConfigDataClient", "Client")
