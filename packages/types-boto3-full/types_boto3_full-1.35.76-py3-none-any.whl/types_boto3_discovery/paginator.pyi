"""
Type annotations for discovery service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_discovery.client import ApplicationDiscoveryServiceClient
    from types_boto3_discovery.paginator import (
        DescribeAgentsPaginator,
        DescribeContinuousExportsPaginator,
        DescribeExportConfigurationsPaginator,
        DescribeExportTasksPaginator,
        DescribeImportTasksPaginator,
        DescribeTagsPaginator,
        ListConfigurationsPaginator,
    )

    session = Session()
    client: ApplicationDiscoveryServiceClient = session.client("discovery")

    describe_agents_paginator: DescribeAgentsPaginator = client.get_paginator("describe_agents")
    describe_continuous_exports_paginator: DescribeContinuousExportsPaginator = client.get_paginator("describe_continuous_exports")
    describe_export_configurations_paginator: DescribeExportConfigurationsPaginator = client.get_paginator("describe_export_configurations")
    describe_export_tasks_paginator: DescribeExportTasksPaginator = client.get_paginator("describe_export_tasks")
    describe_import_tasks_paginator: DescribeImportTasksPaginator = client.get_paginator("describe_import_tasks")
    describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    list_configurations_paginator: ListConfigurationsPaginator = client.get_paginator("list_configurations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAgentsRequestDescribeAgentsPaginateTypeDef,
    DescribeAgentsResponseTypeDef,
    DescribeContinuousExportsRequestDescribeContinuousExportsPaginateTypeDef,
    DescribeContinuousExportsResponseTypeDef,
    DescribeExportConfigurationsRequestDescribeExportConfigurationsPaginateTypeDef,
    DescribeExportConfigurationsResponseTypeDef,
    DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef,
    DescribeExportTasksResponseTypeDef,
    DescribeImportTasksRequestDescribeImportTasksPaginateTypeDef,
    DescribeImportTasksResponseTypeDef,
    DescribeTagsRequestDescribeTagsPaginateTypeDef,
    DescribeTagsResponseTypeDef,
    ListConfigurationsRequestListConfigurationsPaginateTypeDef,
    ListConfigurationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAgentsPaginator",
    "DescribeContinuousExportsPaginator",
    "DescribeExportConfigurationsPaginator",
    "DescribeExportTasksPaginator",
    "DescribeImportTasksPaginator",
    "DescribeTagsPaginator",
    "ListConfigurationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAgentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeAgents.html#ApplicationDiscoveryService.Paginator.DescribeAgents)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#describeagentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeAgentsRequestDescribeAgentsPaginateTypeDef]
    ) -> _PageIterator[DescribeAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeAgents.html#ApplicationDiscoveryService.Paginator.DescribeAgents.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#describeagentspaginator)
        """

class DescribeContinuousExportsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeContinuousExports.html#ApplicationDiscoveryService.Paginator.DescribeContinuousExports)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#describecontinuousexportspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeContinuousExportsRequestDescribeContinuousExportsPaginateTypeDef],
    ) -> _PageIterator[DescribeContinuousExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeContinuousExports.html#ApplicationDiscoveryService.Paginator.DescribeContinuousExports.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#describecontinuousexportspaginator)
        """

class DescribeExportConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeExportConfigurations.html#ApplicationDiscoveryService.Paginator.DescribeExportConfigurations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#describeexportconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeExportConfigurationsRequestDescribeExportConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeExportConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeExportConfigurations.html#ApplicationDiscoveryService.Paginator.DescribeExportConfigurations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#describeexportconfigurationspaginator)
        """

class DescribeExportTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeExportTasks.html#ApplicationDiscoveryService.Paginator.DescribeExportTasks)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#describeexporttaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef]
    ) -> _PageIterator[DescribeExportTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeExportTasks.html#ApplicationDiscoveryService.Paginator.DescribeExportTasks.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#describeexporttaskspaginator)
        """

class DescribeImportTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeImportTasks.html#ApplicationDiscoveryService.Paginator.DescribeImportTasks)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#describeimporttaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeImportTasksRequestDescribeImportTasksPaginateTypeDef]
    ) -> _PageIterator[DescribeImportTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeImportTasks.html#ApplicationDiscoveryService.Paginator.DescribeImportTasks.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#describeimporttaskspaginator)
        """

class DescribeTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeTags.html#ApplicationDiscoveryService.Paginator.DescribeTags)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#describetagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeTagsRequestDescribeTagsPaginateTypeDef]
    ) -> _PageIterator[DescribeTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeTags.html#ApplicationDiscoveryService.Paginator.DescribeTags.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#describetagspaginator)
        """

class ListConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/ListConfigurations.html#ApplicationDiscoveryService.Paginator.ListConfigurations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#listconfigurationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListConfigurationsRequestListConfigurationsPaginateTypeDef]
    ) -> _PageIterator[ListConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/ListConfigurations.html#ApplicationDiscoveryService.Paginator.ListConfigurations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/paginators/#listconfigurationspaginator)
        """
