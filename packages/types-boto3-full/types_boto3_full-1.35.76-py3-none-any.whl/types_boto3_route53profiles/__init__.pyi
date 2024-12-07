"""
Main interface for route53profiles service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_route53profiles import (
        Client,
        ListProfileAssociationsPaginator,
        ListProfileResourceAssociationsPaginator,
        ListProfilesPaginator,
        Route53ProfilesClient,
    )

    session = Session()
    client: Route53ProfilesClient = session.client("route53profiles")

    list_profile_associations_paginator: ListProfileAssociationsPaginator = client.get_paginator("list_profile_associations")
    list_profile_resource_associations_paginator: ListProfileResourceAssociationsPaginator = client.get_paginator("list_profile_resource_associations")
    list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import Route53ProfilesClient
from .paginator import (
    ListProfileAssociationsPaginator,
    ListProfileResourceAssociationsPaginator,
    ListProfilesPaginator,
)

Client = Route53ProfilesClient

__all__ = (
    "Client",
    "ListProfileAssociationsPaginator",
    "ListProfileResourceAssociationsPaginator",
    "ListProfilesPaginator",
    "Route53ProfilesClient",
)
