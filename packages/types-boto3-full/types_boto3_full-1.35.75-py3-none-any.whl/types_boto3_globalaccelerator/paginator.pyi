"""
Type annotations for globalaccelerator service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_globalaccelerator.client import GlobalAcceleratorClient
    from types_boto3_globalaccelerator.paginator import (
        ListAcceleratorsPaginator,
        ListByoipCidrsPaginator,
        ListCrossAccountAttachmentsPaginator,
        ListCrossAccountResourcesPaginator,
        ListCustomRoutingAcceleratorsPaginator,
        ListCustomRoutingEndpointGroupsPaginator,
        ListCustomRoutingListenersPaginator,
        ListCustomRoutingPortMappingsByDestinationPaginator,
        ListCustomRoutingPortMappingsPaginator,
        ListEndpointGroupsPaginator,
        ListListenersPaginator,
    )

    session = Session()
    client: GlobalAcceleratorClient = session.client("globalaccelerator")

    list_accelerators_paginator: ListAcceleratorsPaginator = client.get_paginator("list_accelerators")
    list_byoip_cidrs_paginator: ListByoipCidrsPaginator = client.get_paginator("list_byoip_cidrs")
    list_cross_account_attachments_paginator: ListCrossAccountAttachmentsPaginator = client.get_paginator("list_cross_account_attachments")
    list_cross_account_resources_paginator: ListCrossAccountResourcesPaginator = client.get_paginator("list_cross_account_resources")
    list_custom_routing_accelerators_paginator: ListCustomRoutingAcceleratorsPaginator = client.get_paginator("list_custom_routing_accelerators")
    list_custom_routing_endpoint_groups_paginator: ListCustomRoutingEndpointGroupsPaginator = client.get_paginator("list_custom_routing_endpoint_groups")
    list_custom_routing_listeners_paginator: ListCustomRoutingListenersPaginator = client.get_paginator("list_custom_routing_listeners")
    list_custom_routing_port_mappings_by_destination_paginator: ListCustomRoutingPortMappingsByDestinationPaginator = client.get_paginator("list_custom_routing_port_mappings_by_destination")
    list_custom_routing_port_mappings_paginator: ListCustomRoutingPortMappingsPaginator = client.get_paginator("list_custom_routing_port_mappings")
    list_endpoint_groups_paginator: ListEndpointGroupsPaginator = client.get_paginator("list_endpoint_groups")
    list_listeners_paginator: ListListenersPaginator = client.get_paginator("list_listeners")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAcceleratorsRequestListAcceleratorsPaginateTypeDef,
    ListAcceleratorsResponseTypeDef,
    ListByoipCidrsRequestListByoipCidrsPaginateTypeDef,
    ListByoipCidrsResponseTypeDef,
    ListCrossAccountAttachmentsRequestListCrossAccountAttachmentsPaginateTypeDef,
    ListCrossAccountAttachmentsResponseTypeDef,
    ListCrossAccountResourcesRequestListCrossAccountResourcesPaginateTypeDef,
    ListCrossAccountResourcesResponseTypeDef,
    ListCustomRoutingAcceleratorsRequestListCustomRoutingAcceleratorsPaginateTypeDef,
    ListCustomRoutingAcceleratorsResponseTypeDef,
    ListCustomRoutingEndpointGroupsRequestListCustomRoutingEndpointGroupsPaginateTypeDef,
    ListCustomRoutingEndpointGroupsResponseTypeDef,
    ListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef,
    ListCustomRoutingListenersResponseTypeDef,
    ListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef,
    ListCustomRoutingPortMappingsByDestinationResponseTypeDef,
    ListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef,
    ListCustomRoutingPortMappingsResponseTypeDef,
    ListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef,
    ListEndpointGroupsResponseTypeDef,
    ListListenersRequestListListenersPaginateTypeDef,
    ListListenersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAcceleratorsPaginator",
    "ListByoipCidrsPaginator",
    "ListCrossAccountAttachmentsPaginator",
    "ListCrossAccountResourcesPaginator",
    "ListCustomRoutingAcceleratorsPaginator",
    "ListCustomRoutingEndpointGroupsPaginator",
    "ListCustomRoutingListenersPaginator",
    "ListCustomRoutingPortMappingsByDestinationPaginator",
    "ListCustomRoutingPortMappingsPaginator",
    "ListEndpointGroupsPaginator",
    "ListListenersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAcceleratorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListAccelerators.html#GlobalAccelerator.Paginator.ListAccelerators)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listacceleratorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAcceleratorsRequestListAcceleratorsPaginateTypeDef]
    ) -> _PageIterator[ListAcceleratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListAccelerators.html#GlobalAccelerator.Paginator.ListAccelerators.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listacceleratorspaginator)
        """

class ListByoipCidrsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListByoipCidrs.html#GlobalAccelerator.Paginator.ListByoipCidrs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listbyoipcidrspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListByoipCidrsRequestListByoipCidrsPaginateTypeDef]
    ) -> _PageIterator[ListByoipCidrsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListByoipCidrs.html#GlobalAccelerator.Paginator.ListByoipCidrs.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listbyoipcidrspaginator)
        """

class ListCrossAccountAttachmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCrossAccountAttachments.html#GlobalAccelerator.Paginator.ListCrossAccountAttachments)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcrossaccountattachmentspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCrossAccountAttachmentsRequestListCrossAccountAttachmentsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCrossAccountAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCrossAccountAttachments.html#GlobalAccelerator.Paginator.ListCrossAccountAttachments.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcrossaccountattachmentspaginator)
        """

class ListCrossAccountResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCrossAccountResources.html#GlobalAccelerator.Paginator.ListCrossAccountResources)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcrossaccountresourcespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListCrossAccountResourcesRequestListCrossAccountResourcesPaginateTypeDef],
    ) -> _PageIterator[ListCrossAccountResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCrossAccountResources.html#GlobalAccelerator.Paginator.ListCrossAccountResources.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcrossaccountresourcespaginator)
        """

class ListCustomRoutingAcceleratorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingAccelerators.html#GlobalAccelerator.Paginator.ListCustomRoutingAccelerators)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcustomroutingacceleratorspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCustomRoutingAcceleratorsRequestListCustomRoutingAcceleratorsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCustomRoutingAcceleratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingAccelerators.html#GlobalAccelerator.Paginator.ListCustomRoutingAccelerators.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcustomroutingacceleratorspaginator)
        """

class ListCustomRoutingEndpointGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingEndpointGroups.html#GlobalAccelerator.Paginator.ListCustomRoutingEndpointGroups)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcustomroutingendpointgroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCustomRoutingEndpointGroupsRequestListCustomRoutingEndpointGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCustomRoutingEndpointGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingEndpointGroups.html#GlobalAccelerator.Paginator.ListCustomRoutingEndpointGroups.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcustomroutingendpointgroupspaginator)
        """

class ListCustomRoutingListenersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingListeners.html#GlobalAccelerator.Paginator.ListCustomRoutingListeners)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcustomroutinglistenerspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef
        ],
    ) -> _PageIterator[ListCustomRoutingListenersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingListeners.html#GlobalAccelerator.Paginator.ListCustomRoutingListeners.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcustomroutinglistenerspaginator)
        """

class ListCustomRoutingPortMappingsByDestinationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingPortMappingsByDestination.html#GlobalAccelerator.Paginator.ListCustomRoutingPortMappingsByDestination)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcustomroutingportmappingsbydestinationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef
        ],
    ) -> _PageIterator[ListCustomRoutingPortMappingsByDestinationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingPortMappingsByDestination.html#GlobalAccelerator.Paginator.ListCustomRoutingPortMappingsByDestination.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcustomroutingportmappingsbydestinationpaginator)
        """

class ListCustomRoutingPortMappingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingPortMappings.html#GlobalAccelerator.Paginator.ListCustomRoutingPortMappings)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcustomroutingportmappingspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCustomRoutingPortMappingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingPortMappings.html#GlobalAccelerator.Paginator.ListCustomRoutingPortMappings.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listcustomroutingportmappingspaginator)
        """

class ListEndpointGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListEndpointGroups.html#GlobalAccelerator.Paginator.ListEndpointGroups)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listendpointgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef]
    ) -> _PageIterator[ListEndpointGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListEndpointGroups.html#GlobalAccelerator.Paginator.ListEndpointGroups.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listendpointgroupspaginator)
        """

class ListListenersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListListeners.html#GlobalAccelerator.Paginator.ListListeners)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listlistenerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListListenersRequestListListenersPaginateTypeDef]
    ) -> _PageIterator[ListListenersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListListeners.html#GlobalAccelerator.Paginator.ListListeners.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_globalaccelerator/paginators/#listlistenerspaginator)
        """
