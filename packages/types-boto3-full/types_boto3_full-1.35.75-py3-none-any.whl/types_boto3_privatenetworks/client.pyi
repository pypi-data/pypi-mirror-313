"""
Type annotations for privatenetworks service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_privatenetworks.client import Private5GClient

    session = Session()
    client: Private5GClient = session.client("privatenetworks")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListDeviceIdentifiersPaginator,
    ListNetworkResourcesPaginator,
    ListNetworkSitesPaginator,
    ListNetworksPaginator,
    ListOrdersPaginator,
)
from .type_defs import (
    AcknowledgeOrderReceiptRequestRequestTypeDef,
    AcknowledgeOrderReceiptResponseTypeDef,
    ActivateDeviceIdentifierRequestRequestTypeDef,
    ActivateDeviceIdentifierResponseTypeDef,
    ActivateNetworkSiteRequestRequestTypeDef,
    ActivateNetworkSiteResponseTypeDef,
    ConfigureAccessPointRequestRequestTypeDef,
    ConfigureAccessPointResponseTypeDef,
    CreateNetworkRequestRequestTypeDef,
    CreateNetworkResponseTypeDef,
    CreateNetworkSiteRequestRequestTypeDef,
    CreateNetworkSiteResponseTypeDef,
    DeactivateDeviceIdentifierRequestRequestTypeDef,
    DeactivateDeviceIdentifierResponseTypeDef,
    DeleteNetworkRequestRequestTypeDef,
    DeleteNetworkResponseTypeDef,
    DeleteNetworkSiteRequestRequestTypeDef,
    DeleteNetworkSiteResponseTypeDef,
    GetDeviceIdentifierRequestRequestTypeDef,
    GetDeviceIdentifierResponseTypeDef,
    GetNetworkRequestRequestTypeDef,
    GetNetworkResourceRequestRequestTypeDef,
    GetNetworkResourceResponseTypeDef,
    GetNetworkResponseTypeDef,
    GetNetworkSiteRequestRequestTypeDef,
    GetNetworkSiteResponseTypeDef,
    GetOrderRequestRequestTypeDef,
    GetOrderResponseTypeDef,
    ListDeviceIdentifiersRequestRequestTypeDef,
    ListDeviceIdentifiersResponseTypeDef,
    ListNetworkResourcesRequestRequestTypeDef,
    ListNetworkResourcesResponseTypeDef,
    ListNetworkSitesRequestRequestTypeDef,
    ListNetworkSitesResponseTypeDef,
    ListNetworksRequestRequestTypeDef,
    ListNetworksResponseTypeDef,
    ListOrdersRequestRequestTypeDef,
    ListOrdersResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PingResponseTypeDef,
    StartNetworkResourceUpdateRequestRequestTypeDef,
    StartNetworkResourceUpdateResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateNetworkSitePlanRequestRequestTypeDef,
    UpdateNetworkSiteRequestRequestTypeDef,
    UpdateNetworkSiteResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("Private5GClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class Private5GClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Private5GClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#close)
        """

    def acknowledge_order_receipt(
        self, **kwargs: Unpack[AcknowledgeOrderReceiptRequestRequestTypeDef]
    ) -> AcknowledgeOrderReceiptResponseTypeDef:
        """
        Acknowledges that the specified network order was received.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/acknowledge_order_receipt.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#acknowledge_order_receipt)
        """

    def activate_device_identifier(
        self, **kwargs: Unpack[ActivateDeviceIdentifierRequestRequestTypeDef]
    ) -> ActivateDeviceIdentifierResponseTypeDef:
        """
        Activates the specified device identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/activate_device_identifier.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#activate_device_identifier)
        """

    def activate_network_site(
        self, **kwargs: Unpack[ActivateNetworkSiteRequestRequestTypeDef]
    ) -> ActivateNetworkSiteResponseTypeDef:
        """
        Activates the specified network site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/activate_network_site.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#activate_network_site)
        """

    def configure_access_point(
        self, **kwargs: Unpack[ConfigureAccessPointRequestRequestTypeDef]
    ) -> ConfigureAccessPointResponseTypeDef:
        """
        Configures the specified network resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/configure_access_point.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#configure_access_point)
        """

    def create_network(
        self, **kwargs: Unpack[CreateNetworkRequestRequestTypeDef]
    ) -> CreateNetworkResponseTypeDef:
        """
        Creates a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/create_network.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#create_network)
        """

    def create_network_site(
        self, **kwargs: Unpack[CreateNetworkSiteRequestRequestTypeDef]
    ) -> CreateNetworkSiteResponseTypeDef:
        """
        Creates a network site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/create_network_site.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#create_network_site)
        """

    def deactivate_device_identifier(
        self, **kwargs: Unpack[DeactivateDeviceIdentifierRequestRequestTypeDef]
    ) -> DeactivateDeviceIdentifierResponseTypeDef:
        """
        Deactivates the specified device identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/deactivate_device_identifier.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#deactivate_device_identifier)
        """

    def delete_network(
        self, **kwargs: Unpack[DeleteNetworkRequestRequestTypeDef]
    ) -> DeleteNetworkResponseTypeDef:
        """
        Deletes the specified network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/delete_network.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#delete_network)
        """

    def delete_network_site(
        self, **kwargs: Unpack[DeleteNetworkSiteRequestRequestTypeDef]
    ) -> DeleteNetworkSiteResponseTypeDef:
        """
        Deletes the specified network site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/delete_network_site.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#delete_network_site)
        """

    def get_device_identifier(
        self, **kwargs: Unpack[GetDeviceIdentifierRequestRequestTypeDef]
    ) -> GetDeviceIdentifierResponseTypeDef:
        """
        Gets the specified device identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_device_identifier.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#get_device_identifier)
        """

    def get_network(
        self, **kwargs: Unpack[GetNetworkRequestRequestTypeDef]
    ) -> GetNetworkResponseTypeDef:
        """
        Gets the specified network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_network.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#get_network)
        """

    def get_network_resource(
        self, **kwargs: Unpack[GetNetworkResourceRequestRequestTypeDef]
    ) -> GetNetworkResourceResponseTypeDef:
        """
        Gets the specified network resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_network_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#get_network_resource)
        """

    def get_network_site(
        self, **kwargs: Unpack[GetNetworkSiteRequestRequestTypeDef]
    ) -> GetNetworkSiteResponseTypeDef:
        """
        Gets the specified network site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_network_site.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#get_network_site)
        """

    def get_order(self, **kwargs: Unpack[GetOrderRequestRequestTypeDef]) -> GetOrderResponseTypeDef:
        """
        Gets the specified order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_order.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#get_order)
        """

    def list_device_identifiers(
        self, **kwargs: Unpack[ListDeviceIdentifiersRequestRequestTypeDef]
    ) -> ListDeviceIdentifiersResponseTypeDef:
        """
        Lists device identifiers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/list_device_identifiers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#list_device_identifiers)
        """

    def list_network_resources(
        self, **kwargs: Unpack[ListNetworkResourcesRequestRequestTypeDef]
    ) -> ListNetworkResourcesResponseTypeDef:
        """
        Lists network resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/list_network_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#list_network_resources)
        """

    def list_network_sites(
        self, **kwargs: Unpack[ListNetworkSitesRequestRequestTypeDef]
    ) -> ListNetworkSitesResponseTypeDef:
        """
        Lists network sites.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/list_network_sites.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#list_network_sites)
        """

    def list_networks(
        self, **kwargs: Unpack[ListNetworksRequestRequestTypeDef]
    ) -> ListNetworksResponseTypeDef:
        """
        Lists networks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/list_networks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#list_networks)
        """

    def list_orders(
        self, **kwargs: Unpack[ListOrdersRequestRequestTypeDef]
    ) -> ListOrdersResponseTypeDef:
        """
        Lists orders.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/list_orders.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#list_orders)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#list_tags_for_resource)
        """

    def ping(self) -> PingResponseTypeDef:
        """
        Checks the health of the service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/ping.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#ping)
        """

    def start_network_resource_update(
        self, **kwargs: Unpack[StartNetworkResourceUpdateRequestRequestTypeDef]
    ) -> StartNetworkResourceUpdateResponseTypeDef:
        """
        Use this action to do the following tasks:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/start_network_resource_update.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#start_network_resource_update)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#untag_resource)
        """

    def update_network_site(
        self, **kwargs: Unpack[UpdateNetworkSiteRequestRequestTypeDef]
    ) -> UpdateNetworkSiteResponseTypeDef:
        """
        Updates the specified network site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/update_network_site.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#update_network_site)
        """

    def update_network_site_plan(
        self, **kwargs: Unpack[UpdateNetworkSitePlanRequestRequestTypeDef]
    ) -> UpdateNetworkSiteResponseTypeDef:
        """
        Updates the specified network site plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/update_network_site_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#update_network_site_plan)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_identifiers"]
    ) -> ListDeviceIdentifiersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_network_resources"]
    ) -> ListNetworkResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_network_sites"]
    ) -> ListNetworkSitesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_networks"]) -> ListNetworksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_orders"]) -> ListOrdersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/client/#get_paginator)
        """
