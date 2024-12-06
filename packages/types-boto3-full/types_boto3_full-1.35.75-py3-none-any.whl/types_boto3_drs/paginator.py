"""
Type annotations for drs service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_drs.client import DrsClient
    from types_boto3_drs.paginator import (
        DescribeJobLogItemsPaginator,
        DescribeJobsPaginator,
        DescribeLaunchConfigurationTemplatesPaginator,
        DescribeRecoveryInstancesPaginator,
        DescribeRecoverySnapshotsPaginator,
        DescribeReplicationConfigurationTemplatesPaginator,
        DescribeSourceNetworksPaginator,
        DescribeSourceServersPaginator,
        ListExtensibleSourceServersPaginator,
        ListLaunchActionsPaginator,
        ListStagingAccountsPaginator,
    )

    session = Session()
    client: DrsClient = session.client("drs")

    describe_job_log_items_paginator: DescribeJobLogItemsPaginator = client.get_paginator("describe_job_log_items")
    describe_jobs_paginator: DescribeJobsPaginator = client.get_paginator("describe_jobs")
    describe_launch_configuration_templates_paginator: DescribeLaunchConfigurationTemplatesPaginator = client.get_paginator("describe_launch_configuration_templates")
    describe_recovery_instances_paginator: DescribeRecoveryInstancesPaginator = client.get_paginator("describe_recovery_instances")
    describe_recovery_snapshots_paginator: DescribeRecoverySnapshotsPaginator = client.get_paginator("describe_recovery_snapshots")
    describe_replication_configuration_templates_paginator: DescribeReplicationConfigurationTemplatesPaginator = client.get_paginator("describe_replication_configuration_templates")
    describe_source_networks_paginator: DescribeSourceNetworksPaginator = client.get_paginator("describe_source_networks")
    describe_source_servers_paginator: DescribeSourceServersPaginator = client.get_paginator("describe_source_servers")
    list_extensible_source_servers_paginator: ListExtensibleSourceServersPaginator = client.get_paginator("list_extensible_source_servers")
    list_launch_actions_paginator: ListLaunchActionsPaginator = client.get_paginator("list_launch_actions")
    list_staging_accounts_paginator: ListStagingAccountsPaginator = client.get_paginator("list_staging_accounts")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef,
    DescribeJobLogItemsResponseTypeDef,
    DescribeJobsRequestDescribeJobsPaginateTypeDef,
    DescribeJobsResponseTypeDef,
    DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef,
    DescribeLaunchConfigurationTemplatesResponseTypeDef,
    DescribeRecoveryInstancesRequestDescribeRecoveryInstancesPaginateTypeDef,
    DescribeRecoveryInstancesResponseTypeDef,
    DescribeRecoverySnapshotsRequestDescribeRecoverySnapshotsPaginateTypeDef,
    DescribeRecoverySnapshotsResponseTypeDef,
    DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef,
    DescribeReplicationConfigurationTemplatesResponseTypeDef,
    DescribeSourceNetworksRequestDescribeSourceNetworksPaginateTypeDef,
    DescribeSourceNetworksResponseTypeDef,
    DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef,
    DescribeSourceServersResponseTypeDef,
    ListExtensibleSourceServersRequestListExtensibleSourceServersPaginateTypeDef,
    ListExtensibleSourceServersResponseTypeDef,
    ListLaunchActionsRequestListLaunchActionsPaginateTypeDef,
    ListLaunchActionsResponseTypeDef,
    ListStagingAccountsRequestListStagingAccountsPaginateTypeDef,
    ListStagingAccountsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeJobLogItemsPaginator",
    "DescribeJobsPaginator",
    "DescribeLaunchConfigurationTemplatesPaginator",
    "DescribeRecoveryInstancesPaginator",
    "DescribeRecoverySnapshotsPaginator",
    "DescribeReplicationConfigurationTemplatesPaginator",
    "DescribeSourceNetworksPaginator",
    "DescribeSourceServersPaginator",
    "ListExtensibleSourceServersPaginator",
    "ListLaunchActionsPaginator",
    "ListStagingAccountsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeJobLogItemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeJobLogItems.html#Drs.Paginator.DescribeJobLogItems)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describejoblogitemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef]
    ) -> _PageIterator[DescribeJobLogItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeJobLogItems.html#Drs.Paginator.DescribeJobLogItems.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describejoblogitemspaginator)
        """


class DescribeJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeJobs.html#Drs.Paginator.DescribeJobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describejobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeJobsRequestDescribeJobsPaginateTypeDef]
    ) -> _PageIterator[DescribeJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeJobs.html#Drs.Paginator.DescribeJobs.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describejobspaginator)
        """


class DescribeLaunchConfigurationTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeLaunchConfigurationTemplates.html#Drs.Paginator.DescribeLaunchConfigurationTemplates)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describelaunchconfigurationtemplatespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeLaunchConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeLaunchConfigurationTemplates.html#Drs.Paginator.DescribeLaunchConfigurationTemplates.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describelaunchconfigurationtemplatespaginator)
        """


class DescribeRecoveryInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeRecoveryInstances.html#Drs.Paginator.DescribeRecoveryInstances)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describerecoveryinstancespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeRecoveryInstancesRequestDescribeRecoveryInstancesPaginateTypeDef],
    ) -> _PageIterator[DescribeRecoveryInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeRecoveryInstances.html#Drs.Paginator.DescribeRecoveryInstances.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describerecoveryinstancespaginator)
        """


class DescribeRecoverySnapshotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeRecoverySnapshots.html#Drs.Paginator.DescribeRecoverySnapshots)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describerecoverysnapshotspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeRecoverySnapshotsRequestDescribeRecoverySnapshotsPaginateTypeDef],
    ) -> _PageIterator[DescribeRecoverySnapshotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeRecoverySnapshots.html#Drs.Paginator.DescribeRecoverySnapshots.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describerecoverysnapshotspaginator)
        """


class DescribeReplicationConfigurationTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeReplicationConfigurationTemplates.html#Drs.Paginator.DescribeReplicationConfigurationTemplates)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describereplicationconfigurationtemplatespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeReplicationConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeReplicationConfigurationTemplates.html#Drs.Paginator.DescribeReplicationConfigurationTemplates.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describereplicationconfigurationtemplatespaginator)
        """


class DescribeSourceNetworksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeSourceNetworks.html#Drs.Paginator.DescribeSourceNetworks)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describesourcenetworkspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSourceNetworksRequestDescribeSourceNetworksPaginateTypeDef]
    ) -> _PageIterator[DescribeSourceNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeSourceNetworks.html#Drs.Paginator.DescribeSourceNetworks.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describesourcenetworkspaginator)
        """


class DescribeSourceServersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeSourceServers.html#Drs.Paginator.DescribeSourceServers)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describesourceserverspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef]
    ) -> _PageIterator[DescribeSourceServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/DescribeSourceServers.html#Drs.Paginator.DescribeSourceServers.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#describesourceserverspaginator)
        """


class ListExtensibleSourceServersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListExtensibleSourceServers.html#Drs.Paginator.ListExtensibleSourceServers)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#listextensiblesourceserverspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListExtensibleSourceServersRequestListExtensibleSourceServersPaginateTypeDef
        ],
    ) -> _PageIterator[ListExtensibleSourceServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListExtensibleSourceServers.html#Drs.Paginator.ListExtensibleSourceServers.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#listextensiblesourceserverspaginator)
        """


class ListLaunchActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListLaunchActions.html#Drs.Paginator.ListLaunchActions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#listlaunchactionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLaunchActionsRequestListLaunchActionsPaginateTypeDef]
    ) -> _PageIterator[ListLaunchActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListLaunchActions.html#Drs.Paginator.ListLaunchActions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#listlaunchactionspaginator)
        """


class ListStagingAccountsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListStagingAccounts.html#Drs.Paginator.ListStagingAccounts)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#liststagingaccountspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStagingAccountsRequestListStagingAccountsPaginateTypeDef]
    ) -> _PageIterator[ListStagingAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/drs/paginator/ListStagingAccounts.html#Drs.Paginator.ListStagingAccounts.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_drs/paginators/#liststagingaccountspaginator)
        """
