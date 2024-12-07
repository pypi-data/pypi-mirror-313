"""
Type annotations for marketplace-entitlement service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_marketplace_entitlement.client import MarketplaceEntitlementServiceClient

    session = Session()
    client: MarketplaceEntitlementServiceClient = session.client("marketplace-entitlement")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import GetEntitlementsPaginator
from .type_defs import GetEntitlementsRequestRequestTypeDef, GetEntitlementsResultTypeDef

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("MarketplaceEntitlementServiceClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class MarketplaceEntitlementServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement.html#MarketplaceEntitlementService.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MarketplaceEntitlementServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement.html#MarketplaceEntitlementService.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/client/#close)
        """

    def get_entitlements(
        self, **kwargs: Unpack[GetEntitlementsRequestRequestTypeDef]
    ) -> GetEntitlementsResultTypeDef:
        """
        GetEntitlements retrieves entitlement values for a given product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement/client/get_entitlements.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/client/#get_entitlements)
        """

    def get_paginator(
        self, operation_name: Literal["get_entitlements"]
    ) -> GetEntitlementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/client/#get_paginator)
        """
