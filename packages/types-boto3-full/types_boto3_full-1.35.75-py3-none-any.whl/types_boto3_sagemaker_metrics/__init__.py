"""
Main interface for sagemaker-metrics service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sagemaker_metrics import (
        Client,
        SageMakerMetricsClient,
    )

    session = Session()
    client: SageMakerMetricsClient = session.client("sagemaker-metrics")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SageMakerMetricsClient

Client = SageMakerMetricsClient


__all__ = ("Client", "SageMakerMetricsClient")
