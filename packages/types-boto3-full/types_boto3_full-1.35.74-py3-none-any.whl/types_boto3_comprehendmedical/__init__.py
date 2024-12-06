"""
Main interface for comprehendmedical service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_comprehendmedical import (
        Client,
        ComprehendMedicalClient,
    )

    session = Session()
    client: ComprehendMedicalClient = session.client("comprehendmedical")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ComprehendMedicalClient

Client = ComprehendMedicalClient


__all__ = ("Client", "ComprehendMedicalClient")
