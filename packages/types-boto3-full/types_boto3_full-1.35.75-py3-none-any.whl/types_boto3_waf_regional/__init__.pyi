"""
Main interface for waf-regional service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_waf_regional import (
        Client,
        WAFRegionalClient,
    )

    session = Session()
    client: WAFRegionalClient = session.client("waf-regional")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import WAFRegionalClient

Client = WAFRegionalClient

__all__ = ("Client", "WAFRegionalClient")
