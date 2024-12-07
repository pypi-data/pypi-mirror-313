"""
Main interface for s3control service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_s3control import (
        Client,
        ListAccessPointsForObjectLambdaPaginator,
        ListCallerAccessGrantsPaginator,
        S3ControlClient,
    )

    session = Session()
    client: S3ControlClient = session.client("s3control")

    list_access_points_for_object_lambda_paginator: ListAccessPointsForObjectLambdaPaginator = client.get_paginator("list_access_points_for_object_lambda")
    list_caller_access_grants_paginator: ListCallerAccessGrantsPaginator = client.get_paginator("list_caller_access_grants")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import S3ControlClient
from .paginator import ListAccessPointsForObjectLambdaPaginator, ListCallerAccessGrantsPaginator

Client = S3ControlClient


__all__ = (
    "Client",
    "ListAccessPointsForObjectLambdaPaginator",
    "ListCallerAccessGrantsPaginator",
    "S3ControlClient",
)
