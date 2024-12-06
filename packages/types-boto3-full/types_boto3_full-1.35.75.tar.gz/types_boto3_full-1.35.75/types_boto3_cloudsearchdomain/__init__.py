"""
Main interface for cloudsearchdomain service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_cloudsearchdomain import (
        Client,
        CloudSearchDomainClient,
    )

    session = Session()
    client: CloudSearchDomainClient = session.client("cloudsearchdomain")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudSearchDomainClient

Client = CloudSearchDomainClient


__all__ = ("Client", "CloudSearchDomainClient")
