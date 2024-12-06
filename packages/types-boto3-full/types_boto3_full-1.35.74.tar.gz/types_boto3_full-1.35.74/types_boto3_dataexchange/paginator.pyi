"""
Type annotations for dataexchange service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_dataexchange.client import DataExchangeClient
    from types_boto3_dataexchange.paginator import (
        ListDataGrantsPaginator,
        ListDataSetRevisionsPaginator,
        ListDataSetsPaginator,
        ListEventActionsPaginator,
        ListJobsPaginator,
        ListReceivedDataGrantsPaginator,
        ListRevisionAssetsPaginator,
    )

    session = Session()
    client: DataExchangeClient = session.client("dataexchange")

    list_data_grants_paginator: ListDataGrantsPaginator = client.get_paginator("list_data_grants")
    list_data_set_revisions_paginator: ListDataSetRevisionsPaginator = client.get_paginator("list_data_set_revisions")
    list_data_sets_paginator: ListDataSetsPaginator = client.get_paginator("list_data_sets")
    list_event_actions_paginator: ListEventActionsPaginator = client.get_paginator("list_event_actions")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_received_data_grants_paginator: ListReceivedDataGrantsPaginator = client.get_paginator("list_received_data_grants")
    list_revision_assets_paginator: ListRevisionAssetsPaginator = client.get_paginator("list_revision_assets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDataGrantsRequestListDataGrantsPaginateTypeDef,
    ListDataGrantsResponseTypeDef,
    ListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef,
    ListDataSetRevisionsResponseTypeDef,
    ListDataSetsRequestListDataSetsPaginateTypeDef,
    ListDataSetsResponseTypeDef,
    ListEventActionsRequestListEventActionsPaginateTypeDef,
    ListEventActionsResponseTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListReceivedDataGrantsRequestListReceivedDataGrantsPaginateTypeDef,
    ListReceivedDataGrantsResponseTypeDef,
    ListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef,
    ListRevisionAssetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDataGrantsPaginator",
    "ListDataSetRevisionsPaginator",
    "ListDataSetsPaginator",
    "ListEventActionsPaginator",
    "ListJobsPaginator",
    "ListReceivedDataGrantsPaginator",
    "ListRevisionAssetsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDataGrantsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataGrants.html#DataExchange.Paginator.ListDataGrants)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listdatagrantspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataGrantsRequestListDataGrantsPaginateTypeDef]
    ) -> _PageIterator[ListDataGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataGrants.html#DataExchange.Paginator.ListDataGrants.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listdatagrantspaginator)
        """

class ListDataSetRevisionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataSetRevisions.html#DataExchange.Paginator.ListDataSetRevisions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listdatasetrevisionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef]
    ) -> _PageIterator[ListDataSetRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataSetRevisions.html#DataExchange.Paginator.ListDataSetRevisions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listdatasetrevisionspaginator)
        """

class ListDataSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataSets.html#DataExchange.Paginator.ListDataSets)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listdatasetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataSetsRequestListDataSetsPaginateTypeDef]
    ) -> _PageIterator[ListDataSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataSets.html#DataExchange.Paginator.ListDataSets.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listdatasetspaginator)
        """

class ListEventActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListEventActions.html#DataExchange.Paginator.ListEventActions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listeventactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEventActionsRequestListEventActionsPaginateTypeDef]
    ) -> _PageIterator[ListEventActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListEventActions.html#DataExchange.Paginator.ListEventActions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listeventactionspaginator)
        """

class ListJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListJobs.html#DataExchange.Paginator.ListJobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> _PageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListJobs.html#DataExchange.Paginator.ListJobs.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listjobspaginator)
        """

class ListReceivedDataGrantsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListReceivedDataGrants.html#DataExchange.Paginator.ListReceivedDataGrants)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listreceiveddatagrantspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListReceivedDataGrantsRequestListReceivedDataGrantsPaginateTypeDef]
    ) -> _PageIterator[ListReceivedDataGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListReceivedDataGrants.html#DataExchange.Paginator.ListReceivedDataGrants.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listreceiveddatagrantspaginator)
        """

class ListRevisionAssetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListRevisionAssets.html#DataExchange.Paginator.ListRevisionAssets)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listrevisionassetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef]
    ) -> _PageIterator[ListRevisionAssetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListRevisionAssets.html#DataExchange.Paginator.ListRevisionAssets.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dataexchange/paginators/#listrevisionassetspaginator)
        """
