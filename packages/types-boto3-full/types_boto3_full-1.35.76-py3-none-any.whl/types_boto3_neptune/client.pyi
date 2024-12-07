"""
Type annotations for neptune service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_neptune.client import NeptuneClient

    session = Session()
    client: NeptuneClient = session.client("neptune")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeDBClusterEndpointsPaginator,
    DescribeDBClusterParameterGroupsPaginator,
    DescribeDBClusterParametersPaginator,
    DescribeDBClusterSnapshotsPaginator,
    DescribeDBClustersPaginator,
    DescribeDBEngineVersionsPaginator,
    DescribeDBInstancesPaginator,
    DescribeDBParameterGroupsPaginator,
    DescribeDBParametersPaginator,
    DescribeDBSubnetGroupsPaginator,
    DescribeEngineDefaultParametersPaginator,
    DescribeEventsPaginator,
    DescribeEventSubscriptionsPaginator,
    DescribeGlobalClustersPaginator,
    DescribeOrderableDBInstanceOptionsPaginator,
    DescribePendingMaintenanceActionsPaginator,
)
from .type_defs import (
    AddRoleToDBClusterMessageRequestTypeDef,
    AddSourceIdentifierToSubscriptionMessageRequestTypeDef,
    AddSourceIdentifierToSubscriptionResultTypeDef,
    AddTagsToResourceMessageRequestTypeDef,
    ApplyPendingMaintenanceActionMessageRequestTypeDef,
    ApplyPendingMaintenanceActionResultTypeDef,
    CopyDBClusterParameterGroupMessageRequestTypeDef,
    CopyDBClusterParameterGroupResultTypeDef,
    CopyDBClusterSnapshotMessageRequestTypeDef,
    CopyDBClusterSnapshotResultTypeDef,
    CopyDBParameterGroupMessageRequestTypeDef,
    CopyDBParameterGroupResultTypeDef,
    CreateDBClusterEndpointMessageRequestTypeDef,
    CreateDBClusterEndpointOutputTypeDef,
    CreateDBClusterMessageRequestTypeDef,
    CreateDBClusterParameterGroupMessageRequestTypeDef,
    CreateDBClusterParameterGroupResultTypeDef,
    CreateDBClusterResultTypeDef,
    CreateDBClusterSnapshotMessageRequestTypeDef,
    CreateDBClusterSnapshotResultTypeDef,
    CreateDBInstanceMessageRequestTypeDef,
    CreateDBInstanceResultTypeDef,
    CreateDBParameterGroupMessageRequestTypeDef,
    CreateDBParameterGroupResultTypeDef,
    CreateDBSubnetGroupMessageRequestTypeDef,
    CreateDBSubnetGroupResultTypeDef,
    CreateEventSubscriptionMessageRequestTypeDef,
    CreateEventSubscriptionResultTypeDef,
    CreateGlobalClusterMessageRequestTypeDef,
    CreateGlobalClusterResultTypeDef,
    DBClusterEndpointMessageTypeDef,
    DBClusterMessageTypeDef,
    DBClusterParameterGroupDetailsTypeDef,
    DBClusterParameterGroupNameMessageTypeDef,
    DBClusterParameterGroupsMessageTypeDef,
    DBClusterSnapshotMessageTypeDef,
    DBEngineVersionMessageTypeDef,
    DBInstanceMessageTypeDef,
    DBParameterGroupDetailsTypeDef,
    DBParameterGroupNameMessageTypeDef,
    DBParameterGroupsMessageTypeDef,
    DBSubnetGroupMessageTypeDef,
    DeleteDBClusterEndpointMessageRequestTypeDef,
    DeleteDBClusterEndpointOutputTypeDef,
    DeleteDBClusterMessageRequestTypeDef,
    DeleteDBClusterParameterGroupMessageRequestTypeDef,
    DeleteDBClusterResultTypeDef,
    DeleteDBClusterSnapshotMessageRequestTypeDef,
    DeleteDBClusterSnapshotResultTypeDef,
    DeleteDBInstanceMessageRequestTypeDef,
    DeleteDBInstanceResultTypeDef,
    DeleteDBParameterGroupMessageRequestTypeDef,
    DeleteDBSubnetGroupMessageRequestTypeDef,
    DeleteEventSubscriptionMessageRequestTypeDef,
    DeleteEventSubscriptionResultTypeDef,
    DeleteGlobalClusterMessageRequestTypeDef,
    DeleteGlobalClusterResultTypeDef,
    DescribeDBClusterEndpointsMessageRequestTypeDef,
    DescribeDBClusterParameterGroupsMessageRequestTypeDef,
    DescribeDBClusterParametersMessageRequestTypeDef,
    DescribeDBClustersMessageRequestTypeDef,
    DescribeDBClusterSnapshotAttributesMessageRequestTypeDef,
    DescribeDBClusterSnapshotAttributesResultTypeDef,
    DescribeDBClusterSnapshotsMessageRequestTypeDef,
    DescribeDBEngineVersionsMessageRequestTypeDef,
    DescribeDBInstancesMessageRequestTypeDef,
    DescribeDBParameterGroupsMessageRequestTypeDef,
    DescribeDBParametersMessageRequestTypeDef,
    DescribeDBSubnetGroupsMessageRequestTypeDef,
    DescribeEngineDefaultClusterParametersMessageRequestTypeDef,
    DescribeEngineDefaultClusterParametersResultTypeDef,
    DescribeEngineDefaultParametersMessageRequestTypeDef,
    DescribeEngineDefaultParametersResultTypeDef,
    DescribeEventCategoriesMessageRequestTypeDef,
    DescribeEventsMessageRequestTypeDef,
    DescribeEventSubscriptionsMessageRequestTypeDef,
    DescribeGlobalClustersMessageRequestTypeDef,
    DescribeOrderableDBInstanceOptionsMessageRequestTypeDef,
    DescribePendingMaintenanceActionsMessageRequestTypeDef,
    DescribeValidDBInstanceModificationsMessageRequestTypeDef,
    DescribeValidDBInstanceModificationsResultTypeDef,
    EmptyResponseMetadataTypeDef,
    EventCategoriesMessageTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    FailoverDBClusterMessageRequestTypeDef,
    FailoverDBClusterResultTypeDef,
    FailoverGlobalClusterMessageRequestTypeDef,
    FailoverGlobalClusterResultTypeDef,
    GlobalClustersMessageTypeDef,
    ListTagsForResourceMessageRequestTypeDef,
    ModifyDBClusterEndpointMessageRequestTypeDef,
    ModifyDBClusterEndpointOutputTypeDef,
    ModifyDBClusterMessageRequestTypeDef,
    ModifyDBClusterParameterGroupMessageRequestTypeDef,
    ModifyDBClusterResultTypeDef,
    ModifyDBClusterSnapshotAttributeMessageRequestTypeDef,
    ModifyDBClusterSnapshotAttributeResultTypeDef,
    ModifyDBInstanceMessageRequestTypeDef,
    ModifyDBInstanceResultTypeDef,
    ModifyDBParameterGroupMessageRequestTypeDef,
    ModifyDBSubnetGroupMessageRequestTypeDef,
    ModifyDBSubnetGroupResultTypeDef,
    ModifyEventSubscriptionMessageRequestTypeDef,
    ModifyEventSubscriptionResultTypeDef,
    ModifyGlobalClusterMessageRequestTypeDef,
    ModifyGlobalClusterResultTypeDef,
    OrderableDBInstanceOptionsMessageTypeDef,
    PendingMaintenanceActionsMessageTypeDef,
    PromoteReadReplicaDBClusterMessageRequestTypeDef,
    PromoteReadReplicaDBClusterResultTypeDef,
    RebootDBInstanceMessageRequestTypeDef,
    RebootDBInstanceResultTypeDef,
    RemoveFromGlobalClusterMessageRequestTypeDef,
    RemoveFromGlobalClusterResultTypeDef,
    RemoveRoleFromDBClusterMessageRequestTypeDef,
    RemoveSourceIdentifierFromSubscriptionMessageRequestTypeDef,
    RemoveSourceIdentifierFromSubscriptionResultTypeDef,
    RemoveTagsFromResourceMessageRequestTypeDef,
    ResetDBClusterParameterGroupMessageRequestTypeDef,
    ResetDBParameterGroupMessageRequestTypeDef,
    RestoreDBClusterFromSnapshotMessageRequestTypeDef,
    RestoreDBClusterFromSnapshotResultTypeDef,
    RestoreDBClusterToPointInTimeMessageRequestTypeDef,
    RestoreDBClusterToPointInTimeResultTypeDef,
    StartDBClusterMessageRequestTypeDef,
    StartDBClusterResultTypeDef,
    StopDBClusterMessageRequestTypeDef,
    StopDBClusterResultTypeDef,
    TagListMessageTypeDef,
)
from .waiter import DBInstanceAvailableWaiter, DBInstanceDeletedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("NeptuneClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AuthorizationNotFoundFault: Type[BotocoreClientError]
    CertificateNotFoundFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DBClusterAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterEndpointAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterEndpointNotFoundFault: Type[BotocoreClientError]
    DBClusterEndpointQuotaExceededFault: Type[BotocoreClientError]
    DBClusterNotFoundFault: Type[BotocoreClientError]
    DBClusterParameterGroupNotFoundFault: Type[BotocoreClientError]
    DBClusterQuotaExceededFault: Type[BotocoreClientError]
    DBClusterRoleAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterRoleNotFoundFault: Type[BotocoreClientError]
    DBClusterRoleQuotaExceededFault: Type[BotocoreClientError]
    DBClusterSnapshotAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterSnapshotNotFoundFault: Type[BotocoreClientError]
    DBInstanceAlreadyExistsFault: Type[BotocoreClientError]
    DBInstanceNotFoundFault: Type[BotocoreClientError]
    DBParameterGroupAlreadyExistsFault: Type[BotocoreClientError]
    DBParameterGroupNotFoundFault: Type[BotocoreClientError]
    DBParameterGroupQuotaExceededFault: Type[BotocoreClientError]
    DBSecurityGroupNotFoundFault: Type[BotocoreClientError]
    DBSnapshotAlreadyExistsFault: Type[BotocoreClientError]
    DBSnapshotNotFoundFault: Type[BotocoreClientError]
    DBSubnetGroupAlreadyExistsFault: Type[BotocoreClientError]
    DBSubnetGroupDoesNotCoverEnoughAZs: Type[BotocoreClientError]
    DBSubnetGroupNotFoundFault: Type[BotocoreClientError]
    DBSubnetGroupQuotaExceededFault: Type[BotocoreClientError]
    DBSubnetQuotaExceededFault: Type[BotocoreClientError]
    DBUpgradeDependencyFailureFault: Type[BotocoreClientError]
    DomainNotFoundFault: Type[BotocoreClientError]
    EventSubscriptionQuotaExceededFault: Type[BotocoreClientError]
    GlobalClusterAlreadyExistsFault: Type[BotocoreClientError]
    GlobalClusterNotFoundFault: Type[BotocoreClientError]
    GlobalClusterQuotaExceededFault: Type[BotocoreClientError]
    InstanceQuotaExceededFault: Type[BotocoreClientError]
    InsufficientDBClusterCapacityFault: Type[BotocoreClientError]
    InsufficientDBInstanceCapacityFault: Type[BotocoreClientError]
    InsufficientStorageClusterCapacityFault: Type[BotocoreClientError]
    InvalidDBClusterEndpointStateFault: Type[BotocoreClientError]
    InvalidDBClusterSnapshotStateFault: Type[BotocoreClientError]
    InvalidDBClusterStateFault: Type[BotocoreClientError]
    InvalidDBInstanceStateFault: Type[BotocoreClientError]
    InvalidDBParameterGroupStateFault: Type[BotocoreClientError]
    InvalidDBSecurityGroupStateFault: Type[BotocoreClientError]
    InvalidDBSnapshotStateFault: Type[BotocoreClientError]
    InvalidDBSubnetGroupStateFault: Type[BotocoreClientError]
    InvalidDBSubnetStateFault: Type[BotocoreClientError]
    InvalidEventSubscriptionStateFault: Type[BotocoreClientError]
    InvalidGlobalClusterStateFault: Type[BotocoreClientError]
    InvalidRestoreFault: Type[BotocoreClientError]
    InvalidSubnet: Type[BotocoreClientError]
    InvalidVPCNetworkStateFault: Type[BotocoreClientError]
    KMSKeyNotAccessibleFault: Type[BotocoreClientError]
    OptionGroupNotFoundFault: Type[BotocoreClientError]
    ProvisionedIopsNotAvailableInAZFault: Type[BotocoreClientError]
    ResourceNotFoundFault: Type[BotocoreClientError]
    SNSInvalidTopicFault: Type[BotocoreClientError]
    SNSNoAuthorizationFault: Type[BotocoreClientError]
    SNSTopicArnNotFoundFault: Type[BotocoreClientError]
    SharedSnapshotQuotaExceededFault: Type[BotocoreClientError]
    SnapshotQuotaExceededFault: Type[BotocoreClientError]
    SourceNotFoundFault: Type[BotocoreClientError]
    StorageQuotaExceededFault: Type[BotocoreClientError]
    StorageTypeNotSupportedFault: Type[BotocoreClientError]
    SubnetAlreadyInUse: Type[BotocoreClientError]
    SubscriptionAlreadyExistFault: Type[BotocoreClientError]
    SubscriptionCategoryNotFoundFault: Type[BotocoreClientError]
    SubscriptionNotFoundFault: Type[BotocoreClientError]

class NeptuneClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        NeptuneClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#close)
        """

    def add_role_to_db_cluster(
        self, **kwargs: Unpack[AddRoleToDBClusterMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates an Identity and Access Management (IAM) role with an Neptune DB
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/add_role_to_db_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#add_role_to_db_cluster)
        """

    def add_source_identifier_to_subscription(
        self, **kwargs: Unpack[AddSourceIdentifierToSubscriptionMessageRequestTypeDef]
    ) -> AddSourceIdentifierToSubscriptionResultTypeDef:
        """
        Adds a source identifier to an existing event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/add_source_identifier_to_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#add_source_identifier_to_subscription)
        """

    def add_tags_to_resource(
        self, **kwargs: Unpack[AddTagsToResourceMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds metadata tags to an Amazon Neptune resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/add_tags_to_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#add_tags_to_resource)
        """

    def apply_pending_maintenance_action(
        self, **kwargs: Unpack[ApplyPendingMaintenanceActionMessageRequestTypeDef]
    ) -> ApplyPendingMaintenanceActionResultTypeDef:
        """
        Applies a pending maintenance action to a resource (for example, to a DB
        instance).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/apply_pending_maintenance_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#apply_pending_maintenance_action)
        """

    def copy_db_cluster_parameter_group(
        self, **kwargs: Unpack[CopyDBClusterParameterGroupMessageRequestTypeDef]
    ) -> CopyDBClusterParameterGroupResultTypeDef:
        """
        Copies the specified DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/copy_db_cluster_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#copy_db_cluster_parameter_group)
        """

    def copy_db_cluster_snapshot(
        self, **kwargs: Unpack[CopyDBClusterSnapshotMessageRequestTypeDef]
    ) -> CopyDBClusterSnapshotResultTypeDef:
        """
        Copies a snapshot of a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/copy_db_cluster_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#copy_db_cluster_snapshot)
        """

    def copy_db_parameter_group(
        self, **kwargs: Unpack[CopyDBParameterGroupMessageRequestTypeDef]
    ) -> CopyDBParameterGroupResultTypeDef:
        """
        Copies the specified DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/copy_db_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#copy_db_parameter_group)
        """

    def create_db_cluster(
        self, **kwargs: Unpack[CreateDBClusterMessageRequestTypeDef]
    ) -> CreateDBClusterResultTypeDef:
        """
        Creates a new Amazon Neptune DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/create_db_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#create_db_cluster)
        """

    def create_db_cluster_endpoint(
        self, **kwargs: Unpack[CreateDBClusterEndpointMessageRequestTypeDef]
    ) -> CreateDBClusterEndpointOutputTypeDef:
        """
        Creates a new custom endpoint and associates it with an Amazon Neptune DB
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/create_db_cluster_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#create_db_cluster_endpoint)
        """

    def create_db_cluster_parameter_group(
        self, **kwargs: Unpack[CreateDBClusterParameterGroupMessageRequestTypeDef]
    ) -> CreateDBClusterParameterGroupResultTypeDef:
        """
        Creates a new DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/create_db_cluster_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#create_db_cluster_parameter_group)
        """

    def create_db_cluster_snapshot(
        self, **kwargs: Unpack[CreateDBClusterSnapshotMessageRequestTypeDef]
    ) -> CreateDBClusterSnapshotResultTypeDef:
        """
        Creates a snapshot of a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/create_db_cluster_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#create_db_cluster_snapshot)
        """

    def create_db_instance(
        self, **kwargs: Unpack[CreateDBInstanceMessageRequestTypeDef]
    ) -> CreateDBInstanceResultTypeDef:
        """
        Creates a new DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/create_db_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#create_db_instance)
        """

    def create_db_parameter_group(
        self, **kwargs: Unpack[CreateDBParameterGroupMessageRequestTypeDef]
    ) -> CreateDBParameterGroupResultTypeDef:
        """
        Creates a new DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/create_db_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#create_db_parameter_group)
        """

    def create_db_subnet_group(
        self, **kwargs: Unpack[CreateDBSubnetGroupMessageRequestTypeDef]
    ) -> CreateDBSubnetGroupResultTypeDef:
        """
        Creates a new DB subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/create_db_subnet_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#create_db_subnet_group)
        """

    def create_event_subscription(
        self, **kwargs: Unpack[CreateEventSubscriptionMessageRequestTypeDef]
    ) -> CreateEventSubscriptionResultTypeDef:
        """
        Creates an event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/create_event_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#create_event_subscription)
        """

    def create_global_cluster(
        self, **kwargs: Unpack[CreateGlobalClusterMessageRequestTypeDef]
    ) -> CreateGlobalClusterResultTypeDef:
        """
        Creates a Neptune global database spread across multiple Amazon Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/create_global_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#create_global_cluster)
        """

    def delete_db_cluster(
        self, **kwargs: Unpack[DeleteDBClusterMessageRequestTypeDef]
    ) -> DeleteDBClusterResultTypeDef:
        """
        The DeleteDBCluster action deletes a previously provisioned DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/delete_db_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#delete_db_cluster)
        """

    def delete_db_cluster_endpoint(
        self, **kwargs: Unpack[DeleteDBClusterEndpointMessageRequestTypeDef]
    ) -> DeleteDBClusterEndpointOutputTypeDef:
        """
        Deletes a custom endpoint and removes it from an Amazon Neptune DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/delete_db_cluster_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#delete_db_cluster_endpoint)
        """

    def delete_db_cluster_parameter_group(
        self, **kwargs: Unpack[DeleteDBClusterParameterGroupMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/delete_db_cluster_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#delete_db_cluster_parameter_group)
        """

    def delete_db_cluster_snapshot(
        self, **kwargs: Unpack[DeleteDBClusterSnapshotMessageRequestTypeDef]
    ) -> DeleteDBClusterSnapshotResultTypeDef:
        """
        Deletes a DB cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/delete_db_cluster_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#delete_db_cluster_snapshot)
        """

    def delete_db_instance(
        self, **kwargs: Unpack[DeleteDBInstanceMessageRequestTypeDef]
    ) -> DeleteDBInstanceResultTypeDef:
        """
        The DeleteDBInstance action deletes a previously provisioned DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/delete_db_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#delete_db_instance)
        """

    def delete_db_parameter_group(
        self, **kwargs: Unpack[DeleteDBParameterGroupMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified DBParameterGroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/delete_db_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#delete_db_parameter_group)
        """

    def delete_db_subnet_group(
        self, **kwargs: Unpack[DeleteDBSubnetGroupMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a DB subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/delete_db_subnet_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#delete_db_subnet_group)
        """

    def delete_event_subscription(
        self, **kwargs: Unpack[DeleteEventSubscriptionMessageRequestTypeDef]
    ) -> DeleteEventSubscriptionResultTypeDef:
        """
        Deletes an event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/delete_event_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#delete_event_subscription)
        """

    def delete_global_cluster(
        self, **kwargs: Unpack[DeleteGlobalClusterMessageRequestTypeDef]
    ) -> DeleteGlobalClusterResultTypeDef:
        """
        Deletes a global database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/delete_global_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#delete_global_cluster)
        """

    def describe_db_cluster_endpoints(
        self, **kwargs: Unpack[DescribeDBClusterEndpointsMessageRequestTypeDef]
    ) -> DBClusterEndpointMessageTypeDef:
        """
        Returns information about endpoints for an Amazon Neptune DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_db_cluster_endpoints.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_db_cluster_endpoints)
        """

    def describe_db_cluster_parameter_groups(
        self, **kwargs: Unpack[DescribeDBClusterParameterGroupsMessageRequestTypeDef]
    ) -> DBClusterParameterGroupsMessageTypeDef:
        """
        Returns a list of <code>DBClusterParameterGroup</code> descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_db_cluster_parameter_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_db_cluster_parameter_groups)
        """

    def describe_db_cluster_parameters(
        self, **kwargs: Unpack[DescribeDBClusterParametersMessageRequestTypeDef]
    ) -> DBClusterParameterGroupDetailsTypeDef:
        """
        Returns the detailed parameter list for a particular DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_db_cluster_parameters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_db_cluster_parameters)
        """

    def describe_db_cluster_snapshot_attributes(
        self, **kwargs: Unpack[DescribeDBClusterSnapshotAttributesMessageRequestTypeDef]
    ) -> DescribeDBClusterSnapshotAttributesResultTypeDef:
        """
        Returns a list of DB cluster snapshot attribute names and values for a manual
        DB cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_db_cluster_snapshot_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_db_cluster_snapshot_attributes)
        """

    def describe_db_cluster_snapshots(
        self, **kwargs: Unpack[DescribeDBClusterSnapshotsMessageRequestTypeDef]
    ) -> DBClusterSnapshotMessageTypeDef:
        """
        Returns information about DB cluster snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_db_cluster_snapshots.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_db_cluster_snapshots)
        """

    def describe_db_clusters(
        self, **kwargs: Unpack[DescribeDBClustersMessageRequestTypeDef]
    ) -> DBClusterMessageTypeDef:
        """
        Returns information about provisioned DB clusters, and supports pagination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_db_clusters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_db_clusters)
        """

    def describe_db_engine_versions(
        self, **kwargs: Unpack[DescribeDBEngineVersionsMessageRequestTypeDef]
    ) -> DBEngineVersionMessageTypeDef:
        """
        Returns a list of the available DB engines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_db_engine_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_db_engine_versions)
        """

    def describe_db_instances(
        self, **kwargs: Unpack[DescribeDBInstancesMessageRequestTypeDef]
    ) -> DBInstanceMessageTypeDef:
        """
        Returns information about provisioned instances, and supports pagination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_db_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_db_instances)
        """

    def describe_db_parameter_groups(
        self, **kwargs: Unpack[DescribeDBParameterGroupsMessageRequestTypeDef]
    ) -> DBParameterGroupsMessageTypeDef:
        """
        Returns a list of <code>DBParameterGroup</code> descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_db_parameter_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_db_parameter_groups)
        """

    def describe_db_parameters(
        self, **kwargs: Unpack[DescribeDBParametersMessageRequestTypeDef]
    ) -> DBParameterGroupDetailsTypeDef:
        """
        Returns the detailed parameter list for a particular DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_db_parameters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_db_parameters)
        """

    def describe_db_subnet_groups(
        self, **kwargs: Unpack[DescribeDBSubnetGroupsMessageRequestTypeDef]
    ) -> DBSubnetGroupMessageTypeDef:
        """
        Returns a list of DBSubnetGroup descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_db_subnet_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_db_subnet_groups)
        """

    def describe_engine_default_cluster_parameters(
        self, **kwargs: Unpack[DescribeEngineDefaultClusterParametersMessageRequestTypeDef]
    ) -> DescribeEngineDefaultClusterParametersResultTypeDef:
        """
        Returns the default engine and system parameter information for the cluster
        database engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_engine_default_cluster_parameters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_engine_default_cluster_parameters)
        """

    def describe_engine_default_parameters(
        self, **kwargs: Unpack[DescribeEngineDefaultParametersMessageRequestTypeDef]
    ) -> DescribeEngineDefaultParametersResultTypeDef:
        """
        Returns the default engine and system parameter information for the specified
        database engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_engine_default_parameters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_engine_default_parameters)
        """

    def describe_event_categories(
        self, **kwargs: Unpack[DescribeEventCategoriesMessageRequestTypeDef]
    ) -> EventCategoriesMessageTypeDef:
        """
        Displays a list of categories for all event source types, or, if specified, for
        a specified source type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_event_categories.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_event_categories)
        """

    def describe_event_subscriptions(
        self, **kwargs: Unpack[DescribeEventSubscriptionsMessageRequestTypeDef]
    ) -> EventSubscriptionsMessageTypeDef:
        """
        Lists all the subscription descriptions for a customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_event_subscriptions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_event_subscriptions)
        """

    def describe_events(
        self, **kwargs: Unpack[DescribeEventsMessageRequestTypeDef]
    ) -> EventsMessageTypeDef:
        """
        Returns events related to DB instances, DB security groups, DB snapshots, and
        DB parameter groups for the past 14 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_events)
        """

    def describe_global_clusters(
        self, **kwargs: Unpack[DescribeGlobalClustersMessageRequestTypeDef]
    ) -> GlobalClustersMessageTypeDef:
        """
        Returns information about Neptune global database clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_global_clusters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_global_clusters)
        """

    def describe_orderable_db_instance_options(
        self, **kwargs: Unpack[DescribeOrderableDBInstanceOptionsMessageRequestTypeDef]
    ) -> OrderableDBInstanceOptionsMessageTypeDef:
        """
        Returns a list of orderable DB instance options for the specified engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_orderable_db_instance_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_orderable_db_instance_options)
        """

    def describe_pending_maintenance_actions(
        self, **kwargs: Unpack[DescribePendingMaintenanceActionsMessageRequestTypeDef]
    ) -> PendingMaintenanceActionsMessageTypeDef:
        """
        Returns a list of resources (for example, DB instances) that have at least one
        pending maintenance action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_pending_maintenance_actions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_pending_maintenance_actions)
        """

    def describe_valid_db_instance_modifications(
        self, **kwargs: Unpack[DescribeValidDBInstanceModificationsMessageRequestTypeDef]
    ) -> DescribeValidDBInstanceModificationsResultTypeDef:
        """
        You can call <a>DescribeValidDBInstanceModifications</a> to learn what
        modifications you can make to your DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/describe_valid_db_instance_modifications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#describe_valid_db_instance_modifications)
        """

    def failover_db_cluster(
        self, **kwargs: Unpack[FailoverDBClusterMessageRequestTypeDef]
    ) -> FailoverDBClusterResultTypeDef:
        """
        Forces a failover for a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/failover_db_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#failover_db_cluster)
        """

    def failover_global_cluster(
        self, **kwargs: Unpack[FailoverGlobalClusterMessageRequestTypeDef]
    ) -> FailoverGlobalClusterResultTypeDef:
        """
        Initiates the failover process for a Neptune global database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/failover_global_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#failover_global_cluster)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceMessageRequestTypeDef]
    ) -> TagListMessageTypeDef:
        """
        Lists all tags on an Amazon Neptune resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#list_tags_for_resource)
        """

    def modify_db_cluster(
        self, **kwargs: Unpack[ModifyDBClusterMessageRequestTypeDef]
    ) -> ModifyDBClusterResultTypeDef:
        """
        Modify a setting for a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/modify_db_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#modify_db_cluster)
        """

    def modify_db_cluster_endpoint(
        self, **kwargs: Unpack[ModifyDBClusterEndpointMessageRequestTypeDef]
    ) -> ModifyDBClusterEndpointOutputTypeDef:
        """
        Modifies the properties of an endpoint in an Amazon Neptune DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/modify_db_cluster_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#modify_db_cluster_endpoint)
        """

    def modify_db_cluster_parameter_group(
        self, **kwargs: Unpack[ModifyDBClusterParameterGroupMessageRequestTypeDef]
    ) -> DBClusterParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/modify_db_cluster_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#modify_db_cluster_parameter_group)
        """

    def modify_db_cluster_snapshot_attribute(
        self, **kwargs: Unpack[ModifyDBClusterSnapshotAttributeMessageRequestTypeDef]
    ) -> ModifyDBClusterSnapshotAttributeResultTypeDef:
        """
        Adds an attribute and values to, or removes an attribute and values from, a
        manual DB cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/modify_db_cluster_snapshot_attribute.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#modify_db_cluster_snapshot_attribute)
        """

    def modify_db_instance(
        self, **kwargs: Unpack[ModifyDBInstanceMessageRequestTypeDef]
    ) -> ModifyDBInstanceResultTypeDef:
        """
        Modifies settings for a DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/modify_db_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#modify_db_instance)
        """

    def modify_db_parameter_group(
        self, **kwargs: Unpack[ModifyDBParameterGroupMessageRequestTypeDef]
    ) -> DBParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/modify_db_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#modify_db_parameter_group)
        """

    def modify_db_subnet_group(
        self, **kwargs: Unpack[ModifyDBSubnetGroupMessageRequestTypeDef]
    ) -> ModifyDBSubnetGroupResultTypeDef:
        """
        Modifies an existing DB subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/modify_db_subnet_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#modify_db_subnet_group)
        """

    def modify_event_subscription(
        self, **kwargs: Unpack[ModifyEventSubscriptionMessageRequestTypeDef]
    ) -> ModifyEventSubscriptionResultTypeDef:
        """
        Modifies an existing event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/modify_event_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#modify_event_subscription)
        """

    def modify_global_cluster(
        self, **kwargs: Unpack[ModifyGlobalClusterMessageRequestTypeDef]
    ) -> ModifyGlobalClusterResultTypeDef:
        """
        Modify a setting for an Amazon Neptune global cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/modify_global_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#modify_global_cluster)
        """

    def promote_read_replica_db_cluster(
        self, **kwargs: Unpack[PromoteReadReplicaDBClusterMessageRequestTypeDef]
    ) -> PromoteReadReplicaDBClusterResultTypeDef:
        """
        Not supported.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/promote_read_replica_db_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#promote_read_replica_db_cluster)
        """

    def reboot_db_instance(
        self, **kwargs: Unpack[RebootDBInstanceMessageRequestTypeDef]
    ) -> RebootDBInstanceResultTypeDef:
        """
        You might need to reboot your DB instance, usually for maintenance reasons.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/reboot_db_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#reboot_db_instance)
        """

    def remove_from_global_cluster(
        self, **kwargs: Unpack[RemoveFromGlobalClusterMessageRequestTypeDef]
    ) -> RemoveFromGlobalClusterResultTypeDef:
        """
        Detaches a Neptune DB cluster from a Neptune global database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/remove_from_global_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#remove_from_global_cluster)
        """

    def remove_role_from_db_cluster(
        self, **kwargs: Unpack[RemoveRoleFromDBClusterMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates an Identity and Access Management (IAM) role from a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/remove_role_from_db_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#remove_role_from_db_cluster)
        """

    def remove_source_identifier_from_subscription(
        self, **kwargs: Unpack[RemoveSourceIdentifierFromSubscriptionMessageRequestTypeDef]
    ) -> RemoveSourceIdentifierFromSubscriptionResultTypeDef:
        """
        Removes a source identifier from an existing event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/remove_source_identifier_from_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#remove_source_identifier_from_subscription)
        """

    def remove_tags_from_resource(
        self, **kwargs: Unpack[RemoveTagsFromResourceMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes metadata tags from an Amazon Neptune resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/remove_tags_from_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#remove_tags_from_resource)
        """

    def reset_db_cluster_parameter_group(
        self, **kwargs: Unpack[ResetDBClusterParameterGroupMessageRequestTypeDef]
    ) -> DBClusterParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a DB cluster parameter group to the default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/reset_db_cluster_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#reset_db_cluster_parameter_group)
        """

    def reset_db_parameter_group(
        self, **kwargs: Unpack[ResetDBParameterGroupMessageRequestTypeDef]
    ) -> DBParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a DB parameter group to the engine/system default
        value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/reset_db_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#reset_db_parameter_group)
        """

    def restore_db_cluster_from_snapshot(
        self, **kwargs: Unpack[RestoreDBClusterFromSnapshotMessageRequestTypeDef]
    ) -> RestoreDBClusterFromSnapshotResultTypeDef:
        """
        Creates a new DB cluster from a DB snapshot or DB cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/restore_db_cluster_from_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#restore_db_cluster_from_snapshot)
        """

    def restore_db_cluster_to_point_in_time(
        self, **kwargs: Unpack[RestoreDBClusterToPointInTimeMessageRequestTypeDef]
    ) -> RestoreDBClusterToPointInTimeResultTypeDef:
        """
        Restores a DB cluster to an arbitrary point in time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/restore_db_cluster_to_point_in_time.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#restore_db_cluster_to_point_in_time)
        """

    def start_db_cluster(
        self, **kwargs: Unpack[StartDBClusterMessageRequestTypeDef]
    ) -> StartDBClusterResultTypeDef:
        """
        Starts an Amazon Neptune DB cluster that was stopped using the Amazon console,
        the Amazon CLI stop-db-cluster command, or the StopDBCluster API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/start_db_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#start_db_cluster)
        """

    def stop_db_cluster(
        self, **kwargs: Unpack[StopDBClusterMessageRequestTypeDef]
    ) -> StopDBClusterResultTypeDef:
        """
        Stops an Amazon Neptune DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/stop_db_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#stop_db_cluster)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_endpoints"]
    ) -> DescribeDBClusterEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_parameter_groups"]
    ) -> DescribeDBClusterParameterGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_parameters"]
    ) -> DescribeDBClusterParametersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_snapshots"]
    ) -> DescribeDBClusterSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_clusters"]
    ) -> DescribeDBClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_engine_versions"]
    ) -> DescribeDBEngineVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_instances"]
    ) -> DescribeDBInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_parameter_groups"]
    ) -> DescribeDBParameterGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_parameters"]
    ) -> DescribeDBParametersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_subnet_groups"]
    ) -> DescribeDBSubnetGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_engine_default_parameters"]
    ) -> DescribeEngineDefaultParametersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_event_subscriptions"]
    ) -> DescribeEventSubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_global_clusters"]
    ) -> DescribeGlobalClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_orderable_db_instance_options"]
    ) -> DescribeOrderableDBInstanceOptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_pending_maintenance_actions"]
    ) -> DescribePendingMaintenanceActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["db_instance_available"]
    ) -> DBInstanceAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["db_instance_deleted"]) -> DBInstanceDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune/client/#get_waiter)
        """
