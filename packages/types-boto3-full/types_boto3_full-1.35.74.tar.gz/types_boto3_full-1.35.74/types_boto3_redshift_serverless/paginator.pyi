"""
Type annotations for redshift-serverless service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_redshift_serverless.client import RedshiftServerlessClient
    from types_boto3_redshift_serverless.paginator import (
        ListCustomDomainAssociationsPaginator,
        ListEndpointAccessPaginator,
        ListManagedWorkgroupsPaginator,
        ListNamespacesPaginator,
        ListRecoveryPointsPaginator,
        ListScheduledActionsPaginator,
        ListSnapshotCopyConfigurationsPaginator,
        ListSnapshotsPaginator,
        ListTableRestoreStatusPaginator,
        ListUsageLimitsPaginator,
        ListWorkgroupsPaginator,
    )

    session = Session()
    client: RedshiftServerlessClient = session.client("redshift-serverless")

    list_custom_domain_associations_paginator: ListCustomDomainAssociationsPaginator = client.get_paginator("list_custom_domain_associations")
    list_endpoint_access_paginator: ListEndpointAccessPaginator = client.get_paginator("list_endpoint_access")
    list_managed_workgroups_paginator: ListManagedWorkgroupsPaginator = client.get_paginator("list_managed_workgroups")
    list_namespaces_paginator: ListNamespacesPaginator = client.get_paginator("list_namespaces")
    list_recovery_points_paginator: ListRecoveryPointsPaginator = client.get_paginator("list_recovery_points")
    list_scheduled_actions_paginator: ListScheduledActionsPaginator = client.get_paginator("list_scheduled_actions")
    list_snapshot_copy_configurations_paginator: ListSnapshotCopyConfigurationsPaginator = client.get_paginator("list_snapshot_copy_configurations")
    list_snapshots_paginator: ListSnapshotsPaginator = client.get_paginator("list_snapshots")
    list_table_restore_status_paginator: ListTableRestoreStatusPaginator = client.get_paginator("list_table_restore_status")
    list_usage_limits_paginator: ListUsageLimitsPaginator = client.get_paginator("list_usage_limits")
    list_workgroups_paginator: ListWorkgroupsPaginator = client.get_paginator("list_workgroups")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCustomDomainAssociationsRequestListCustomDomainAssociationsPaginateTypeDef,
    ListCustomDomainAssociationsResponseTypeDef,
    ListEndpointAccessRequestListEndpointAccessPaginateTypeDef,
    ListEndpointAccessResponseTypeDef,
    ListManagedWorkgroupsRequestListManagedWorkgroupsPaginateTypeDef,
    ListManagedWorkgroupsResponseTypeDef,
    ListNamespacesRequestListNamespacesPaginateTypeDef,
    ListNamespacesResponseTypeDef,
    ListRecoveryPointsRequestListRecoveryPointsPaginateTypeDef,
    ListRecoveryPointsResponseTypeDef,
    ListScheduledActionsRequestListScheduledActionsPaginateTypeDef,
    ListScheduledActionsResponseTypeDef,
    ListSnapshotCopyConfigurationsRequestListSnapshotCopyConfigurationsPaginateTypeDef,
    ListSnapshotCopyConfigurationsResponseTypeDef,
    ListSnapshotsRequestListSnapshotsPaginateTypeDef,
    ListSnapshotsResponseTypeDef,
    ListTableRestoreStatusRequestListTableRestoreStatusPaginateTypeDef,
    ListTableRestoreStatusResponseTypeDef,
    ListUsageLimitsRequestListUsageLimitsPaginateTypeDef,
    ListUsageLimitsResponseTypeDef,
    ListWorkgroupsRequestListWorkgroupsPaginateTypeDef,
    ListWorkgroupsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCustomDomainAssociationsPaginator",
    "ListEndpointAccessPaginator",
    "ListManagedWorkgroupsPaginator",
    "ListNamespacesPaginator",
    "ListRecoveryPointsPaginator",
    "ListScheduledActionsPaginator",
    "ListSnapshotCopyConfigurationsPaginator",
    "ListSnapshotsPaginator",
    "ListTableRestoreStatusPaginator",
    "ListUsageLimitsPaginator",
    "ListWorkgroupsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCustomDomainAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListCustomDomainAssociations.html#RedshiftServerless.Paginator.ListCustomDomainAssociations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listcustomdomainassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCustomDomainAssociationsRequestListCustomDomainAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCustomDomainAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListCustomDomainAssociations.html#RedshiftServerless.Paginator.ListCustomDomainAssociations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listcustomdomainassociationspaginator)
        """

class ListEndpointAccessPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListEndpointAccess.html#RedshiftServerless.Paginator.ListEndpointAccess)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listendpointaccesspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEndpointAccessRequestListEndpointAccessPaginateTypeDef]
    ) -> _PageIterator[ListEndpointAccessResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListEndpointAccess.html#RedshiftServerless.Paginator.ListEndpointAccess.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listendpointaccesspaginator)
        """

class ListManagedWorkgroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListManagedWorkgroups.html#RedshiftServerless.Paginator.ListManagedWorkgroups)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listmanagedworkgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListManagedWorkgroupsRequestListManagedWorkgroupsPaginateTypeDef]
    ) -> _PageIterator[ListManagedWorkgroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListManagedWorkgroups.html#RedshiftServerless.Paginator.ListManagedWorkgroups.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listmanagedworkgroupspaginator)
        """

class ListNamespacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListNamespaces.html#RedshiftServerless.Paginator.ListNamespaces)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listnamespacespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNamespacesRequestListNamespacesPaginateTypeDef]
    ) -> _PageIterator[ListNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListNamespaces.html#RedshiftServerless.Paginator.ListNamespaces.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listnamespacespaginator)
        """

class ListRecoveryPointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListRecoveryPoints.html#RedshiftServerless.Paginator.ListRecoveryPoints)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listrecoverypointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRecoveryPointsRequestListRecoveryPointsPaginateTypeDef]
    ) -> _PageIterator[ListRecoveryPointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListRecoveryPoints.html#RedshiftServerless.Paginator.ListRecoveryPoints.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listrecoverypointspaginator)
        """

class ListScheduledActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListScheduledActions.html#RedshiftServerless.Paginator.ListScheduledActions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listscheduledactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListScheduledActionsRequestListScheduledActionsPaginateTypeDef]
    ) -> _PageIterator[ListScheduledActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListScheduledActions.html#RedshiftServerless.Paginator.ListScheduledActions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listscheduledactionspaginator)
        """

class ListSnapshotCopyConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListSnapshotCopyConfigurations.html#RedshiftServerless.Paginator.ListSnapshotCopyConfigurations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listsnapshotcopyconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListSnapshotCopyConfigurationsRequestListSnapshotCopyConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListSnapshotCopyConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListSnapshotCopyConfigurations.html#RedshiftServerless.Paginator.ListSnapshotCopyConfigurations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listsnapshotcopyconfigurationspaginator)
        """

class ListSnapshotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListSnapshots.html#RedshiftServerless.Paginator.ListSnapshots)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listsnapshotspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSnapshotsRequestListSnapshotsPaginateTypeDef]
    ) -> _PageIterator[ListSnapshotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListSnapshots.html#RedshiftServerless.Paginator.ListSnapshots.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listsnapshotspaginator)
        """

class ListTableRestoreStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListTableRestoreStatus.html#RedshiftServerless.Paginator.ListTableRestoreStatus)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listtablerestorestatuspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTableRestoreStatusRequestListTableRestoreStatusPaginateTypeDef]
    ) -> _PageIterator[ListTableRestoreStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListTableRestoreStatus.html#RedshiftServerless.Paginator.ListTableRestoreStatus.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listtablerestorestatuspaginator)
        """

class ListUsageLimitsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListUsageLimits.html#RedshiftServerless.Paginator.ListUsageLimits)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listusagelimitspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsageLimitsRequestListUsageLimitsPaginateTypeDef]
    ) -> _PageIterator[ListUsageLimitsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListUsageLimits.html#RedshiftServerless.Paginator.ListUsageLimits.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listusagelimitspaginator)
        """

class ListWorkgroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListWorkgroups.html#RedshiftServerless.Paginator.ListWorkgroups)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listworkgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWorkgroupsRequestListWorkgroupsPaginateTypeDef]
    ) -> _PageIterator[ListWorkgroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListWorkgroups.html#RedshiftServerless.Paginator.ListWorkgroups.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/paginators/#listworkgroupspaginator)
        """
