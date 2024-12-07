"""
Type annotations for appmesh service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_appmesh.client import AppMeshClient
    from types_boto3_appmesh.paginator import (
        ListGatewayRoutesPaginator,
        ListMeshesPaginator,
        ListRoutesPaginator,
        ListTagsForResourcePaginator,
        ListVirtualGatewaysPaginator,
        ListVirtualNodesPaginator,
        ListVirtualRoutersPaginator,
        ListVirtualServicesPaginator,
    )

    session = Session()
    client: AppMeshClient = session.client("appmesh")

    list_gateway_routes_paginator: ListGatewayRoutesPaginator = client.get_paginator("list_gateway_routes")
    list_meshes_paginator: ListMeshesPaginator = client.get_paginator("list_meshes")
    list_routes_paginator: ListRoutesPaginator = client.get_paginator("list_routes")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_virtual_gateways_paginator: ListVirtualGatewaysPaginator = client.get_paginator("list_virtual_gateways")
    list_virtual_nodes_paginator: ListVirtualNodesPaginator = client.get_paginator("list_virtual_nodes")
    list_virtual_routers_paginator: ListVirtualRoutersPaginator = client.get_paginator("list_virtual_routers")
    list_virtual_services_paginator: ListVirtualServicesPaginator = client.get_paginator("list_virtual_services")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListGatewayRoutesInputListGatewayRoutesPaginateTypeDef,
    ListGatewayRoutesOutputTypeDef,
    ListMeshesInputListMeshesPaginateTypeDef,
    ListMeshesOutputTypeDef,
    ListRoutesInputListRoutesPaginateTypeDef,
    ListRoutesOutputTypeDef,
    ListTagsForResourceInputListTagsForResourcePaginateTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListVirtualGatewaysInputListVirtualGatewaysPaginateTypeDef,
    ListVirtualGatewaysOutputTypeDef,
    ListVirtualNodesInputListVirtualNodesPaginateTypeDef,
    ListVirtualNodesOutputTypeDef,
    ListVirtualRoutersInputListVirtualRoutersPaginateTypeDef,
    ListVirtualRoutersOutputTypeDef,
    ListVirtualServicesInputListVirtualServicesPaginateTypeDef,
    ListVirtualServicesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListGatewayRoutesPaginator",
    "ListMeshesPaginator",
    "ListRoutesPaginator",
    "ListTagsForResourcePaginator",
    "ListVirtualGatewaysPaginator",
    "ListVirtualNodesPaginator",
    "ListVirtualRoutersPaginator",
    "ListVirtualServicesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListGatewayRoutesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListGatewayRoutes.html#AppMesh.Paginator.ListGatewayRoutes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listgatewayroutespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGatewayRoutesInputListGatewayRoutesPaginateTypeDef]
    ) -> _PageIterator[ListGatewayRoutesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListGatewayRoutes.html#AppMesh.Paginator.ListGatewayRoutes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listgatewayroutespaginator)
        """


class ListMeshesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListMeshes.html#AppMesh.Paginator.ListMeshes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listmeshespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMeshesInputListMeshesPaginateTypeDef]
    ) -> _PageIterator[ListMeshesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListMeshes.html#AppMesh.Paginator.ListMeshes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listmeshespaginator)
        """


class ListRoutesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListRoutes.html#AppMesh.Paginator.ListRoutes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listroutespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRoutesInputListRoutesPaginateTypeDef]
    ) -> _PageIterator[ListRoutesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListRoutes.html#AppMesh.Paginator.ListRoutes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listroutespaginator)
        """


class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListTagsForResource.html#AppMesh.Paginator.ListTagsForResource)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceInputListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListTagsForResource.html#AppMesh.Paginator.ListTagsForResource.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listtagsforresourcepaginator)
        """


class ListVirtualGatewaysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualGateways.html#AppMesh.Paginator.ListVirtualGateways)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listvirtualgatewayspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVirtualGatewaysInputListVirtualGatewaysPaginateTypeDef]
    ) -> _PageIterator[ListVirtualGatewaysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualGateways.html#AppMesh.Paginator.ListVirtualGateways.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listvirtualgatewayspaginator)
        """


class ListVirtualNodesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualNodes.html#AppMesh.Paginator.ListVirtualNodes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listvirtualnodespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVirtualNodesInputListVirtualNodesPaginateTypeDef]
    ) -> _PageIterator[ListVirtualNodesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualNodes.html#AppMesh.Paginator.ListVirtualNodes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listvirtualnodespaginator)
        """


class ListVirtualRoutersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualRouters.html#AppMesh.Paginator.ListVirtualRouters)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listvirtualrouterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVirtualRoutersInputListVirtualRoutersPaginateTypeDef]
    ) -> _PageIterator[ListVirtualRoutersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualRouters.html#AppMesh.Paginator.ListVirtualRouters.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listvirtualrouterspaginator)
        """


class ListVirtualServicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualServices.html#AppMesh.Paginator.ListVirtualServices)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listvirtualservicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVirtualServicesInputListVirtualServicesPaginateTypeDef]
    ) -> _PageIterator[ListVirtualServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualServices.html#AppMesh.Paginator.ListVirtualServices.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appmesh/paginators/#listvirtualservicespaginator)
        """
