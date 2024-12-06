"""
Main interface for sagemaker-runtime service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sagemaker_runtime import (
        Client,
        SageMakerRuntimeClient,
    )

    session = Session()
    client: SageMakerRuntimeClient = session.client("sagemaker-runtime")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SageMakerRuntimeClient

Client = SageMakerRuntimeClient


__all__ = ("Client", "SageMakerRuntimeClient")
