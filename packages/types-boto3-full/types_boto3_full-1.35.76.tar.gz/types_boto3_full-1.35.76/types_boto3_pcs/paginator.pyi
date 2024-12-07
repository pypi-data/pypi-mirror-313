"""
Type annotations for pcs service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pcs/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_pcs.client import ParallelComputingServiceClient
    from types_boto3_pcs.paginator import (
        ListClustersPaginator,
        ListComputeNodeGroupsPaginator,
        ListQueuesPaginator,
    )

    session = Session()
    client: ParallelComputingServiceClient = session.client("pcs")

    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_compute_node_groups_paginator: ListComputeNodeGroupsPaginator = client.get_paginator("list_compute_node_groups")
    list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListClustersRequestListClustersPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListComputeNodeGroupsRequestListComputeNodeGroupsPaginateTypeDef,
    ListComputeNodeGroupsResponseTypeDef,
    ListQueuesRequestListQueuesPaginateTypeDef,
    ListQueuesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListClustersPaginator", "ListComputeNodeGroupsPaginator", "ListQueuesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/paginator/ListClusters.html#ParallelComputingService.Paginator.ListClusters)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pcs/paginators/#listclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClustersRequestListClustersPaginateTypeDef]
    ) -> _PageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/paginator/ListClusters.html#ParallelComputingService.Paginator.ListClusters.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pcs/paginators/#listclusterspaginator)
        """

class ListComputeNodeGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/paginator/ListComputeNodeGroups.html#ParallelComputingService.Paginator.ListComputeNodeGroups)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pcs/paginators/#listcomputenodegroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListComputeNodeGroupsRequestListComputeNodeGroupsPaginateTypeDef]
    ) -> _PageIterator[ListComputeNodeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/paginator/ListComputeNodeGroups.html#ParallelComputingService.Paginator.ListComputeNodeGroups.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pcs/paginators/#listcomputenodegroupspaginator)
        """

class ListQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/paginator/ListQueues.html#ParallelComputingService.Paginator.ListQueues)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pcs/paginators/#listqueuespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListQueuesRequestListQueuesPaginateTypeDef]
    ) -> _PageIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/paginator/ListQueues.html#ParallelComputingService.Paginator.ListQueues.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pcs/paginators/#listqueuespaginator)
        """
