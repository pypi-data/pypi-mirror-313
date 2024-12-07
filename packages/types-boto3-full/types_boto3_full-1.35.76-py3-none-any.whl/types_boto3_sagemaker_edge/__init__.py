"""
Main interface for sagemaker-edge service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sagemaker_edge import (
        Client,
        SagemakerEdgeManagerClient,
    )

    session = Session()
    client: SagemakerEdgeManagerClient = session.client("sagemaker-edge")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SagemakerEdgeManagerClient

Client = SagemakerEdgeManagerClient


__all__ = ("Client", "SagemakerEdgeManagerClient")
