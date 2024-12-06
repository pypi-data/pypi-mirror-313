"""
Main interface for rds-data service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_rds_data import (
        Client,
        RDSDataServiceClient,
    )

    session = Session()
    client: RDSDataServiceClient = session.client("rds-data")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import RDSDataServiceClient

Client = RDSDataServiceClient

__all__ = ("Client", "RDSDataServiceClient")
