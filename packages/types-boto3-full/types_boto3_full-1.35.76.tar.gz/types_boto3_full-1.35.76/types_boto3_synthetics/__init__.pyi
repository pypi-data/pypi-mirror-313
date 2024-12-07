"""
Main interface for synthetics service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_synthetics import (
        Client,
        SyntheticsClient,
    )

    session = Session()
    client: SyntheticsClient = session.client("synthetics")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SyntheticsClient

Client = SyntheticsClient

__all__ = ("Client", "SyntheticsClient")
