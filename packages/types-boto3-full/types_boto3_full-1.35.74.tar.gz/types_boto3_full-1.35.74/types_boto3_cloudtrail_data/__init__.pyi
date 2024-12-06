"""
Main interface for cloudtrail-data service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_cloudtrail_data import (
        Client,
        CloudTrailDataServiceClient,
    )

    session = Session()
    client: CloudTrailDataServiceClient = session.client("cloudtrail-data")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudTrailDataServiceClient

Client = CloudTrailDataServiceClient

__all__ = ("Client", "CloudTrailDataServiceClient")
