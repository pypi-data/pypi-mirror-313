"""
Main interface for marketplace-deployment service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_marketplace_deployment import (
        Client,
        MarketplaceDeploymentServiceClient,
    )

    session = Session()
    client: MarketplaceDeploymentServiceClient = session.client("marketplace-deployment")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MarketplaceDeploymentServiceClient

Client = MarketplaceDeploymentServiceClient

__all__ = ("Client", "MarketplaceDeploymentServiceClient")
