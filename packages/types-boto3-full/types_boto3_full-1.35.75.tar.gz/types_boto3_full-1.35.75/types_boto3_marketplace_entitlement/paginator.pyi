"""
Type annotations for marketplace-entitlement service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_marketplace_entitlement.client import MarketplaceEntitlementServiceClient
    from types_boto3_marketplace_entitlement.paginator import (
        GetEntitlementsPaginator,
    )

    session = Session()
    client: MarketplaceEntitlementServiceClient = session.client("marketplace-entitlement")

    get_entitlements_paginator: GetEntitlementsPaginator = client.get_paginator("get_entitlements")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetEntitlementsRequestGetEntitlementsPaginateTypeDef,
    GetEntitlementsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("GetEntitlementsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetEntitlementsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement/paginator/GetEntitlements.html#MarketplaceEntitlementService.Paginator.GetEntitlements)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/paginators/#getentitlementspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetEntitlementsRequestGetEntitlementsPaginateTypeDef]
    ) -> _PageIterator[GetEntitlementsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement/paginator/GetEntitlements.html#MarketplaceEntitlementService.Paginator.GetEntitlements.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/paginators/#getentitlementspaginator)
        """
