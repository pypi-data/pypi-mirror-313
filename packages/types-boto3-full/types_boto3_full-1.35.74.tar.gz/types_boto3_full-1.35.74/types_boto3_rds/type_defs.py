"""
Type annotations for rds service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/type_defs/)

Usage::

    ```python
    from types_boto3_rds.type_defs import AccountQuotaTypeDef

    data: AccountQuotaTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Optional, Sequence, Union

from .literals import (
    ActivityStreamModeType,
    ActivityStreamPolicyStatusType,
    ActivityStreamStatusType,
    ApplyMethodType,
    AuditPolicyStateType,
    AutomationModeType,
    ClientPasswordAuthTypeType,
    ClusterScalabilityTypeType,
    CustomEngineVersionStatusType,
    DatabaseInsightsModeType,
    DBProxyEndpointStatusType,
    DBProxyEndpointTargetRoleType,
    DBProxyStatusType,
    EngineFamilyType,
    ExportSourceTypeType,
    FailoverStatusType,
    GlobalClusterMemberSynchronizationStatusType,
    IAMAuthModeType,
    IntegrationStatusType,
    LimitlessDatabaseStatusType,
    LocalWriteForwardingStatusType,
    ReplicaModeType,
    SourceTypeType,
    TargetHealthReasonType,
    TargetRoleType,
    TargetStateType,
    TargetTypeType,
    WriteForwardingStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccountAttributesMessageTypeDef",
    "AccountQuotaTypeDef",
    "AddRoleToDBClusterMessageRequestTypeDef",
    "AddRoleToDBInstanceMessageRequestTypeDef",
    "AddSourceIdentifierToSubscriptionMessageRequestTypeDef",
    "AddSourceIdentifierToSubscriptionResultTypeDef",
    "AddTagsToResourceMessageRequestTypeDef",
    "ApplyPendingMaintenanceActionMessageRequestTypeDef",
    "ApplyPendingMaintenanceActionResultTypeDef",
    "AuthorizeDBSecurityGroupIngressMessageRequestTypeDef",
    "AuthorizeDBSecurityGroupIngressResultTypeDef",
    "AvailabilityZoneTypeDef",
    "AvailableProcessorFeatureTypeDef",
    "BacktrackDBClusterMessageRequestTypeDef",
    "BlueGreenDeploymentTaskTypeDef",
    "BlueGreenDeploymentTypeDef",
    "CancelExportTaskMessageRequestTypeDef",
    "CertificateDetailsTypeDef",
    "CertificateMessageTypeDef",
    "CertificateTypeDef",
    "CharacterSetTypeDef",
    "ClientGenerateDbAuthTokenRequestTypeDef",
    "CloudwatchLogsExportConfigurationTypeDef",
    "ClusterPendingModifiedValuesTypeDef",
    "ConnectionPoolConfigurationInfoTypeDef",
    "ConnectionPoolConfigurationTypeDef",
    "ContextAttributeTypeDef",
    "CopyDBClusterParameterGroupMessageRequestTypeDef",
    "CopyDBClusterParameterGroupResultTypeDef",
    "CopyDBClusterSnapshotMessageRequestTypeDef",
    "CopyDBClusterSnapshotResultTypeDef",
    "CopyDBParameterGroupMessageRequestTypeDef",
    "CopyDBParameterGroupResultTypeDef",
    "CopyDBSnapshotMessageRequestTypeDef",
    "CopyDBSnapshotResultTypeDef",
    "CopyOptionGroupMessageRequestTypeDef",
    "CopyOptionGroupResultTypeDef",
    "CreateBlueGreenDeploymentRequestRequestTypeDef",
    "CreateBlueGreenDeploymentResponseTypeDef",
    "CreateCustomDBEngineVersionMessageRequestTypeDef",
    "CreateDBClusterEndpointMessageRequestTypeDef",
    "CreateDBClusterMessageRequestTypeDef",
    "CreateDBClusterParameterGroupMessageRequestTypeDef",
    "CreateDBClusterParameterGroupResultTypeDef",
    "CreateDBClusterResultTypeDef",
    "CreateDBClusterSnapshotMessageRequestTypeDef",
    "CreateDBClusterSnapshotResultTypeDef",
    "CreateDBInstanceMessageRequestTypeDef",
    "CreateDBInstanceReadReplicaMessageRequestTypeDef",
    "CreateDBInstanceReadReplicaResultTypeDef",
    "CreateDBInstanceResultTypeDef",
    "CreateDBParameterGroupMessageRequestTypeDef",
    "CreateDBParameterGroupResultTypeDef",
    "CreateDBProxyEndpointRequestRequestTypeDef",
    "CreateDBProxyEndpointResponseTypeDef",
    "CreateDBProxyRequestRequestTypeDef",
    "CreateDBProxyResponseTypeDef",
    "CreateDBSecurityGroupMessageRequestTypeDef",
    "CreateDBSecurityGroupResultTypeDef",
    "CreateDBShardGroupMessageRequestTypeDef",
    "CreateDBSnapshotMessageRequestTypeDef",
    "CreateDBSnapshotResultTypeDef",
    "CreateDBSubnetGroupMessageRequestTypeDef",
    "CreateDBSubnetGroupResultTypeDef",
    "CreateEventSubscriptionMessageRequestTypeDef",
    "CreateEventSubscriptionResultTypeDef",
    "CreateGlobalClusterMessageRequestTypeDef",
    "CreateGlobalClusterResultTypeDef",
    "CreateIntegrationMessageRequestTypeDef",
    "CreateOptionGroupMessageRequestTypeDef",
    "CreateOptionGroupResultTypeDef",
    "CreateTenantDatabaseMessageRequestTypeDef",
    "CreateTenantDatabaseResultTypeDef",
    "CustomDBEngineVersionAMITypeDef",
    "DBClusterAutomatedBackupMessageTypeDef",
    "DBClusterAutomatedBackupTypeDef",
    "DBClusterBacktrackMessageTypeDef",
    "DBClusterBacktrackResponseTypeDef",
    "DBClusterBacktrackTypeDef",
    "DBClusterCapacityInfoTypeDef",
    "DBClusterEndpointMessageTypeDef",
    "DBClusterEndpointResponseTypeDef",
    "DBClusterEndpointTypeDef",
    "DBClusterMemberTypeDef",
    "DBClusterMessageTypeDef",
    "DBClusterOptionGroupStatusTypeDef",
    "DBClusterParameterGroupDetailsTypeDef",
    "DBClusterParameterGroupNameMessageTypeDef",
    "DBClusterParameterGroupTypeDef",
    "DBClusterParameterGroupsMessageTypeDef",
    "DBClusterRoleTypeDef",
    "DBClusterSnapshotAttributeTypeDef",
    "DBClusterSnapshotAttributesResultTypeDef",
    "DBClusterSnapshotMessageTypeDef",
    "DBClusterSnapshotTypeDef",
    "DBClusterStatusInfoTypeDef",
    "DBClusterTypeDef",
    "DBEngineVersionMessageTypeDef",
    "DBEngineVersionResponseTypeDef",
    "DBEngineVersionTypeDef",
    "DBInstanceAutomatedBackupMessageTypeDef",
    "DBInstanceAutomatedBackupTypeDef",
    "DBInstanceAutomatedBackupsReplicationTypeDef",
    "DBInstanceMessageTypeDef",
    "DBInstanceRoleTypeDef",
    "DBInstanceStatusInfoTypeDef",
    "DBInstanceTypeDef",
    "DBParameterGroupDetailsTypeDef",
    "DBParameterGroupNameMessageTypeDef",
    "DBParameterGroupStatusTypeDef",
    "DBParameterGroupTypeDef",
    "DBParameterGroupsMessageTypeDef",
    "DBProxyEndpointTypeDef",
    "DBProxyTargetGroupTypeDef",
    "DBProxyTargetTypeDef",
    "DBProxyTypeDef",
    "DBRecommendationMessageTypeDef",
    "DBRecommendationTypeDef",
    "DBRecommendationsMessageTypeDef",
    "DBSecurityGroupMembershipTypeDef",
    "DBSecurityGroupMessageTypeDef",
    "DBSecurityGroupTypeDef",
    "DBShardGroupResponseTypeDef",
    "DBShardGroupTypeDef",
    "DBSnapshotAttributeTypeDef",
    "DBSnapshotAttributesResultTypeDef",
    "DBSnapshotMessageTypeDef",
    "DBSnapshotTenantDatabaseTypeDef",
    "DBSnapshotTenantDatabasesMessageTypeDef",
    "DBSnapshotTypeDef",
    "DBSubnetGroupMessageTypeDef",
    "DBSubnetGroupTypeDef",
    "DeleteBlueGreenDeploymentRequestRequestTypeDef",
    "DeleteBlueGreenDeploymentResponseTypeDef",
    "DeleteCustomDBEngineVersionMessageRequestTypeDef",
    "DeleteDBClusterAutomatedBackupMessageRequestTypeDef",
    "DeleteDBClusterAutomatedBackupResultTypeDef",
    "DeleteDBClusterEndpointMessageRequestTypeDef",
    "DeleteDBClusterMessageRequestTypeDef",
    "DeleteDBClusterParameterGroupMessageRequestTypeDef",
    "DeleteDBClusterResultTypeDef",
    "DeleteDBClusterSnapshotMessageRequestTypeDef",
    "DeleteDBClusterSnapshotResultTypeDef",
    "DeleteDBInstanceAutomatedBackupMessageRequestTypeDef",
    "DeleteDBInstanceAutomatedBackupResultTypeDef",
    "DeleteDBInstanceMessageRequestTypeDef",
    "DeleteDBInstanceResultTypeDef",
    "DeleteDBParameterGroupMessageRequestTypeDef",
    "DeleteDBProxyEndpointRequestRequestTypeDef",
    "DeleteDBProxyEndpointResponseTypeDef",
    "DeleteDBProxyRequestRequestTypeDef",
    "DeleteDBProxyResponseTypeDef",
    "DeleteDBSecurityGroupMessageRequestTypeDef",
    "DeleteDBShardGroupMessageRequestTypeDef",
    "DeleteDBSnapshotMessageRequestTypeDef",
    "DeleteDBSnapshotResultTypeDef",
    "DeleteDBSubnetGroupMessageRequestTypeDef",
    "DeleteEventSubscriptionMessageRequestTypeDef",
    "DeleteEventSubscriptionResultTypeDef",
    "DeleteGlobalClusterMessageRequestTypeDef",
    "DeleteGlobalClusterResultTypeDef",
    "DeleteIntegrationMessageRequestTypeDef",
    "DeleteOptionGroupMessageRequestTypeDef",
    "DeleteTenantDatabaseMessageRequestTypeDef",
    "DeleteTenantDatabaseResultTypeDef",
    "DeregisterDBProxyTargetsRequestRequestTypeDef",
    "DescribeBlueGreenDeploymentsRequestDescribeBlueGreenDeploymentsPaginateTypeDef",
    "DescribeBlueGreenDeploymentsRequestRequestTypeDef",
    "DescribeBlueGreenDeploymentsResponseTypeDef",
    "DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef",
    "DescribeCertificatesMessageRequestTypeDef",
    "DescribeDBClusterAutomatedBackupsMessageDescribeDBClusterAutomatedBackupsPaginateTypeDef",
    "DescribeDBClusterAutomatedBackupsMessageRequestTypeDef",
    "DescribeDBClusterBacktracksMessageDescribeDBClusterBacktracksPaginateTypeDef",
    "DescribeDBClusterBacktracksMessageRequestTypeDef",
    "DescribeDBClusterEndpointsMessageDescribeDBClusterEndpointsPaginateTypeDef",
    "DescribeDBClusterEndpointsMessageRequestTypeDef",
    "DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef",
    "DescribeDBClusterParameterGroupsMessageRequestTypeDef",
    "DescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef",
    "DescribeDBClusterParametersMessageRequestTypeDef",
    "DescribeDBClusterSnapshotAttributesMessageRequestTypeDef",
    "DescribeDBClusterSnapshotAttributesResultTypeDef",
    "DescribeDBClusterSnapshotsMessageDBClusterSnapshotAvailableWaitTypeDef",
    "DescribeDBClusterSnapshotsMessageDBClusterSnapshotDeletedWaitTypeDef",
    "DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef",
    "DescribeDBClusterSnapshotsMessageRequestTypeDef",
    "DescribeDBClustersMessageDBClusterAvailableWaitTypeDef",
    "DescribeDBClustersMessageDBClusterDeletedWaitTypeDef",
    "DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef",
    "DescribeDBClustersMessageRequestTypeDef",
    "DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef",
    "DescribeDBEngineVersionsMessageRequestTypeDef",
    "DescribeDBInstanceAutomatedBackupsMessageDescribeDBInstanceAutomatedBackupsPaginateTypeDef",
    "DescribeDBInstanceAutomatedBackupsMessageRequestTypeDef",
    "DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef",
    "DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef",
    "DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef",
    "DescribeDBInstancesMessageRequestTypeDef",
    "DescribeDBLogFilesDetailsTypeDef",
    "DescribeDBLogFilesMessageDescribeDBLogFilesPaginateTypeDef",
    "DescribeDBLogFilesMessageRequestTypeDef",
    "DescribeDBLogFilesResponseTypeDef",
    "DescribeDBParameterGroupsMessageDescribeDBParameterGroupsPaginateTypeDef",
    "DescribeDBParameterGroupsMessageRequestTypeDef",
    "DescribeDBParametersMessageDescribeDBParametersPaginateTypeDef",
    "DescribeDBParametersMessageRequestTypeDef",
    "DescribeDBProxiesRequestDescribeDBProxiesPaginateTypeDef",
    "DescribeDBProxiesRequestRequestTypeDef",
    "DescribeDBProxiesResponseTypeDef",
    "DescribeDBProxyEndpointsRequestDescribeDBProxyEndpointsPaginateTypeDef",
    "DescribeDBProxyEndpointsRequestRequestTypeDef",
    "DescribeDBProxyEndpointsResponseTypeDef",
    "DescribeDBProxyTargetGroupsRequestDescribeDBProxyTargetGroupsPaginateTypeDef",
    "DescribeDBProxyTargetGroupsRequestRequestTypeDef",
    "DescribeDBProxyTargetGroupsResponseTypeDef",
    "DescribeDBProxyTargetsRequestDescribeDBProxyTargetsPaginateTypeDef",
    "DescribeDBProxyTargetsRequestRequestTypeDef",
    "DescribeDBProxyTargetsResponseTypeDef",
    "DescribeDBRecommendationsMessageDescribeDBRecommendationsPaginateTypeDef",
    "DescribeDBRecommendationsMessageRequestTypeDef",
    "DescribeDBSecurityGroupsMessageDescribeDBSecurityGroupsPaginateTypeDef",
    "DescribeDBSecurityGroupsMessageRequestTypeDef",
    "DescribeDBShardGroupsMessageRequestTypeDef",
    "DescribeDBShardGroupsResponseTypeDef",
    "DescribeDBSnapshotAttributesMessageRequestTypeDef",
    "DescribeDBSnapshotAttributesResultTypeDef",
    "DescribeDBSnapshotTenantDatabasesMessageDescribeDBSnapshotTenantDatabasesPaginateTypeDef",
    "DescribeDBSnapshotTenantDatabasesMessageRequestTypeDef",
    "DescribeDBSnapshotsMessageDBSnapshotAvailableWaitTypeDef",
    "DescribeDBSnapshotsMessageDBSnapshotCompletedWaitTypeDef",
    "DescribeDBSnapshotsMessageDBSnapshotDeletedWaitTypeDef",
    "DescribeDBSnapshotsMessageDescribeDBSnapshotsPaginateTypeDef",
    "DescribeDBSnapshotsMessageRequestTypeDef",
    "DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef",
    "DescribeDBSubnetGroupsMessageRequestTypeDef",
    "DescribeEngineDefaultClusterParametersMessageDescribeEngineDefaultClusterParametersPaginateTypeDef",
    "DescribeEngineDefaultClusterParametersMessageRequestTypeDef",
    "DescribeEngineDefaultClusterParametersResultTypeDef",
    "DescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef",
    "DescribeEngineDefaultParametersMessageRequestTypeDef",
    "DescribeEngineDefaultParametersResultTypeDef",
    "DescribeEventCategoriesMessageRequestTypeDef",
    "DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef",
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    "DescribeEventsMessageDescribeEventsPaginateTypeDef",
    "DescribeEventsMessageRequestTypeDef",
    "DescribeExportTasksMessageDescribeExportTasksPaginateTypeDef",
    "DescribeExportTasksMessageRequestTypeDef",
    "DescribeGlobalClustersMessageDescribeGlobalClustersPaginateTypeDef",
    "DescribeGlobalClustersMessageRequestTypeDef",
    "DescribeIntegrationsMessageDescribeIntegrationsPaginateTypeDef",
    "DescribeIntegrationsMessageRequestTypeDef",
    "DescribeIntegrationsResponseTypeDef",
    "DescribeOptionGroupOptionsMessageDescribeOptionGroupOptionsPaginateTypeDef",
    "DescribeOptionGroupOptionsMessageRequestTypeDef",
    "DescribeOptionGroupsMessageDescribeOptionGroupsPaginateTypeDef",
    "DescribeOptionGroupsMessageRequestTypeDef",
    "DescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef",
    "DescribeOrderableDBInstanceOptionsMessageRequestTypeDef",
    "DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef",
    "DescribePendingMaintenanceActionsMessageRequestTypeDef",
    "DescribeReservedDBInstancesMessageDescribeReservedDBInstancesPaginateTypeDef",
    "DescribeReservedDBInstancesMessageRequestTypeDef",
    "DescribeReservedDBInstancesOfferingsMessageDescribeReservedDBInstancesOfferingsPaginateTypeDef",
    "DescribeReservedDBInstancesOfferingsMessageRequestTypeDef",
    "DescribeSourceRegionsMessageDescribeSourceRegionsPaginateTypeDef",
    "DescribeSourceRegionsMessageRequestTypeDef",
    "DescribeTenantDatabasesMessageDescribeTenantDatabasesPaginateTypeDef",
    "DescribeTenantDatabasesMessageRequestTypeDef",
    "DescribeTenantDatabasesMessageTenantDatabaseAvailableWaitTypeDef",
    "DescribeTenantDatabasesMessageTenantDatabaseDeletedWaitTypeDef",
    "DescribeValidDBInstanceModificationsMessageRequestTypeDef",
    "DescribeValidDBInstanceModificationsResultTypeDef",
    "DisableHttpEndpointRequestRequestTypeDef",
    "DisableHttpEndpointResponseTypeDef",
    "DocLinkTypeDef",
    "DomainMembershipTypeDef",
    "DoubleRangeTypeDef",
    "DownloadDBLogFilePortionDetailsTypeDef",
    "DownloadDBLogFilePortionMessageDownloadDBLogFilePortionPaginateTypeDef",
    "DownloadDBLogFilePortionMessageRequestTypeDef",
    "EC2SecurityGroupTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableHttpEndpointRequestRequestTypeDef",
    "EnableHttpEndpointResponseTypeDef",
    "EndpointTypeDef",
    "EngineDefaultsTypeDef",
    "EventCategoriesMapTypeDef",
    "EventCategoriesMessageTypeDef",
    "EventSubscriptionTypeDef",
    "EventSubscriptionsMessageTypeDef",
    "EventTypeDef",
    "EventsMessageTypeDef",
    "ExportTaskResponseTypeDef",
    "ExportTaskTypeDef",
    "ExportTasksMessageTypeDef",
    "FailoverDBClusterMessageRequestTypeDef",
    "FailoverDBClusterResultTypeDef",
    "FailoverGlobalClusterMessageRequestTypeDef",
    "FailoverGlobalClusterResultTypeDef",
    "FailoverStateTypeDef",
    "FilterTypeDef",
    "GlobalClusterMemberTypeDef",
    "GlobalClusterTypeDef",
    "GlobalClustersMessageTypeDef",
    "IPRangeTypeDef",
    "IntegrationErrorTypeDef",
    "IntegrationResponseTypeDef",
    "IntegrationTypeDef",
    "IssueDetailsTypeDef",
    "LimitlessDatabaseTypeDef",
    "ListTagsForResourceMessageRequestTypeDef",
    "MasterUserSecretTypeDef",
    "MetricQueryTypeDef",
    "MetricReferenceTypeDef",
    "MetricTypeDef",
    "MinimumEngineVersionPerAllowedValueTypeDef",
    "ModifyActivityStreamRequestRequestTypeDef",
    "ModifyActivityStreamResponseTypeDef",
    "ModifyCertificatesMessageRequestTypeDef",
    "ModifyCertificatesResultTypeDef",
    "ModifyCurrentDBClusterCapacityMessageRequestTypeDef",
    "ModifyCustomDBEngineVersionMessageRequestTypeDef",
    "ModifyDBClusterEndpointMessageRequestTypeDef",
    "ModifyDBClusterMessageRequestTypeDef",
    "ModifyDBClusterParameterGroupMessageRequestTypeDef",
    "ModifyDBClusterResultTypeDef",
    "ModifyDBClusterSnapshotAttributeMessageRequestTypeDef",
    "ModifyDBClusterSnapshotAttributeResultTypeDef",
    "ModifyDBInstanceMessageRequestTypeDef",
    "ModifyDBInstanceResultTypeDef",
    "ModifyDBParameterGroupMessageRequestTypeDef",
    "ModifyDBProxyEndpointRequestRequestTypeDef",
    "ModifyDBProxyEndpointResponseTypeDef",
    "ModifyDBProxyRequestRequestTypeDef",
    "ModifyDBProxyResponseTypeDef",
    "ModifyDBProxyTargetGroupRequestRequestTypeDef",
    "ModifyDBProxyTargetGroupResponseTypeDef",
    "ModifyDBRecommendationMessageRequestTypeDef",
    "ModifyDBShardGroupMessageRequestTypeDef",
    "ModifyDBSnapshotAttributeMessageRequestTypeDef",
    "ModifyDBSnapshotAttributeResultTypeDef",
    "ModifyDBSnapshotMessageRequestTypeDef",
    "ModifyDBSnapshotResultTypeDef",
    "ModifyDBSubnetGroupMessageRequestTypeDef",
    "ModifyDBSubnetGroupResultTypeDef",
    "ModifyEventSubscriptionMessageRequestTypeDef",
    "ModifyEventSubscriptionResultTypeDef",
    "ModifyGlobalClusterMessageRequestTypeDef",
    "ModifyGlobalClusterResultTypeDef",
    "ModifyIntegrationMessageRequestTypeDef",
    "ModifyOptionGroupMessageRequestTypeDef",
    "ModifyOptionGroupResultTypeDef",
    "ModifyTenantDatabaseMessageRequestTypeDef",
    "ModifyTenantDatabaseResultTypeDef",
    "OptionConfigurationTypeDef",
    "OptionGroupMembershipTypeDef",
    "OptionGroupOptionSettingTypeDef",
    "OptionGroupOptionTypeDef",
    "OptionGroupOptionsMessageTypeDef",
    "OptionGroupTypeDef",
    "OptionGroupsTypeDef",
    "OptionSettingTypeDef",
    "OptionTypeDef",
    "OptionVersionTypeDef",
    "OrderableDBInstanceOptionTypeDef",
    "OrderableDBInstanceOptionsMessageTypeDef",
    "OutpostTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterOutputTypeDef",
    "ParameterTypeDef",
    "ParameterUnionTypeDef",
    "PendingCloudwatchLogsExportsTypeDef",
    "PendingMaintenanceActionTypeDef",
    "PendingMaintenanceActionsMessageTypeDef",
    "PendingModifiedValuesTypeDef",
    "PerformanceInsightsMetricDimensionGroupTypeDef",
    "PerformanceInsightsMetricQueryTypeDef",
    "PerformanceIssueDetailsTypeDef",
    "ProcessorFeatureTypeDef",
    "PromoteReadReplicaDBClusterMessageRequestTypeDef",
    "PromoteReadReplicaDBClusterResultTypeDef",
    "PromoteReadReplicaMessageRequestTypeDef",
    "PromoteReadReplicaResultTypeDef",
    "PurchaseReservedDBInstancesOfferingMessageRequestTypeDef",
    "PurchaseReservedDBInstancesOfferingResultTypeDef",
    "RangeTypeDef",
    "RdsCustomClusterConfigurationTypeDef",
    "RebootDBClusterMessageRequestTypeDef",
    "RebootDBClusterResultTypeDef",
    "RebootDBInstanceMessageRequestTypeDef",
    "RebootDBInstanceResultTypeDef",
    "RebootDBShardGroupMessageRequestTypeDef",
    "RecommendedActionParameterTypeDef",
    "RecommendedActionTypeDef",
    "RecommendedActionUpdateTypeDef",
    "RecurringChargeTypeDef",
    "ReferenceDetailsTypeDef",
    "RegisterDBProxyTargetsRequestRequestTypeDef",
    "RegisterDBProxyTargetsResponseTypeDef",
    "RemoveFromGlobalClusterMessageRequestTypeDef",
    "RemoveFromGlobalClusterResultTypeDef",
    "RemoveRoleFromDBClusterMessageRequestTypeDef",
    "RemoveRoleFromDBInstanceMessageRequestTypeDef",
    "RemoveSourceIdentifierFromSubscriptionMessageRequestTypeDef",
    "RemoveSourceIdentifierFromSubscriptionResultTypeDef",
    "RemoveTagsFromResourceMessageRequestTypeDef",
    "ReservedDBInstanceMessageTypeDef",
    "ReservedDBInstanceTypeDef",
    "ReservedDBInstancesOfferingMessageTypeDef",
    "ReservedDBInstancesOfferingTypeDef",
    "ResetDBClusterParameterGroupMessageRequestTypeDef",
    "ResetDBParameterGroupMessageRequestTypeDef",
    "ResourcePendingMaintenanceActionsTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreDBClusterFromS3MessageRequestTypeDef",
    "RestoreDBClusterFromS3ResultTypeDef",
    "RestoreDBClusterFromSnapshotMessageRequestTypeDef",
    "RestoreDBClusterFromSnapshotResultTypeDef",
    "RestoreDBClusterToPointInTimeMessageRequestTypeDef",
    "RestoreDBClusterToPointInTimeResultTypeDef",
    "RestoreDBInstanceFromDBSnapshotMessageRequestTypeDef",
    "RestoreDBInstanceFromDBSnapshotResultTypeDef",
    "RestoreDBInstanceFromS3MessageRequestTypeDef",
    "RestoreDBInstanceFromS3ResultTypeDef",
    "RestoreDBInstanceToPointInTimeMessageRequestTypeDef",
    "RestoreDBInstanceToPointInTimeResultTypeDef",
    "RestoreWindowTypeDef",
    "RevokeDBSecurityGroupIngressMessageRequestTypeDef",
    "RevokeDBSecurityGroupIngressResultTypeDef",
    "ScalarReferenceDetailsTypeDef",
    "ScalingConfigurationInfoTypeDef",
    "ScalingConfigurationTypeDef",
    "ServerlessV2FeaturesSupportTypeDef",
    "ServerlessV2ScalingConfigurationInfoTypeDef",
    "ServerlessV2ScalingConfigurationTypeDef",
    "SourceRegionMessageTypeDef",
    "SourceRegionTypeDef",
    "StartActivityStreamRequestRequestTypeDef",
    "StartActivityStreamResponseTypeDef",
    "StartDBClusterMessageRequestTypeDef",
    "StartDBClusterResultTypeDef",
    "StartDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef",
    "StartDBInstanceAutomatedBackupsReplicationResultTypeDef",
    "StartDBInstanceMessageRequestTypeDef",
    "StartDBInstanceResultTypeDef",
    "StartExportTaskMessageRequestTypeDef",
    "StopActivityStreamRequestRequestTypeDef",
    "StopActivityStreamResponseTypeDef",
    "StopDBClusterMessageRequestTypeDef",
    "StopDBClusterResultTypeDef",
    "StopDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef",
    "StopDBInstanceAutomatedBackupsReplicationResultTypeDef",
    "StopDBInstanceMessageRequestTypeDef",
    "StopDBInstanceResultTypeDef",
    "SubnetTypeDef",
    "SwitchoverBlueGreenDeploymentRequestRequestTypeDef",
    "SwitchoverBlueGreenDeploymentResponseTypeDef",
    "SwitchoverDetailTypeDef",
    "SwitchoverGlobalClusterMessageRequestTypeDef",
    "SwitchoverGlobalClusterResultTypeDef",
    "SwitchoverReadReplicaMessageRequestTypeDef",
    "SwitchoverReadReplicaResultTypeDef",
    "TagListMessageTypeDef",
    "TagTypeDef",
    "TargetHealthTypeDef",
    "TenantDatabasePendingModifiedValuesTypeDef",
    "TenantDatabaseTypeDef",
    "TenantDatabasesMessageTypeDef",
    "TimestampTypeDef",
    "TimezoneTypeDef",
    "UpgradeTargetTypeDef",
    "UserAuthConfigInfoTypeDef",
    "UserAuthConfigTypeDef",
    "ValidDBInstanceModificationsMessageTypeDef",
    "ValidStorageOptionsTypeDef",
    "VpcSecurityGroupMembershipTypeDef",
    "WaiterConfigTypeDef",
)


class AccountQuotaTypeDef(TypedDict):
    AccountQuotaName: NotRequired[str]
    Used: NotRequired[int]
    Max: NotRequired[int]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AddRoleToDBClusterMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str
    RoleArn: str
    FeatureName: NotRequired[str]


class AddRoleToDBInstanceMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    RoleArn: str
    FeatureName: str


class AddSourceIdentifierToSubscriptionMessageRequestTypeDef(TypedDict):
    SubscriptionName: str
    SourceIdentifier: str


class EventSubscriptionTypeDef(TypedDict):
    CustomerAwsId: NotRequired[str]
    CustSubscriptionId: NotRequired[str]
    SnsTopicArn: NotRequired[str]
    Status: NotRequired[str]
    SubscriptionCreationTime: NotRequired[str]
    SourceType: NotRequired[str]
    SourceIdsList: NotRequired[List[str]]
    EventCategoriesList: NotRequired[List[str]]
    Enabled: NotRequired[bool]
    EventSubscriptionArn: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class ApplyPendingMaintenanceActionMessageRequestTypeDef(TypedDict):
    ResourceIdentifier: str
    ApplyAction: str
    OptInType: str


class AuthorizeDBSecurityGroupIngressMessageRequestTypeDef(TypedDict):
    DBSecurityGroupName: str
    CIDRIP: NotRequired[str]
    EC2SecurityGroupName: NotRequired[str]
    EC2SecurityGroupId: NotRequired[str]
    EC2SecurityGroupOwnerId: NotRequired[str]


class AvailabilityZoneTypeDef(TypedDict):
    Name: NotRequired[str]


class AvailableProcessorFeatureTypeDef(TypedDict):
    Name: NotRequired[str]
    DefaultValue: NotRequired[str]
    AllowedValues: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class BlueGreenDeploymentTaskTypeDef(TypedDict):
    Name: NotRequired[str]
    Status: NotRequired[str]


class SwitchoverDetailTypeDef(TypedDict):
    SourceMember: NotRequired[str]
    TargetMember: NotRequired[str]
    Status: NotRequired[str]


class CancelExportTaskMessageRequestTypeDef(TypedDict):
    ExportTaskIdentifier: str


class CertificateDetailsTypeDef(TypedDict):
    CAIdentifier: NotRequired[str]
    ValidTill: NotRequired[datetime]


class CertificateTypeDef(TypedDict):
    CertificateIdentifier: NotRequired[str]
    CertificateType: NotRequired[str]
    Thumbprint: NotRequired[str]
    ValidFrom: NotRequired[datetime]
    ValidTill: NotRequired[datetime]
    CertificateArn: NotRequired[str]
    CustomerOverride: NotRequired[bool]
    CustomerOverrideValidTill: NotRequired[datetime]


class CharacterSetTypeDef(TypedDict):
    CharacterSetName: NotRequired[str]
    CharacterSetDescription: NotRequired[str]


class ClientGenerateDbAuthTokenRequestTypeDef(TypedDict):
    DBHostname: str
    Port: int
    DBUsername: str
    Region: NotRequired[Optional[str]]


class CloudwatchLogsExportConfigurationTypeDef(TypedDict):
    EnableLogTypes: NotRequired[Sequence[str]]
    DisableLogTypes: NotRequired[Sequence[str]]


class PendingCloudwatchLogsExportsTypeDef(TypedDict):
    LogTypesToEnable: NotRequired[List[str]]
    LogTypesToDisable: NotRequired[List[str]]


class RdsCustomClusterConfigurationTypeDef(TypedDict):
    InterconnectSubnetId: NotRequired[str]
    TransitGatewayMulticastDomainId: NotRequired[str]
    ReplicaMode: NotRequired[ReplicaModeType]


class ConnectionPoolConfigurationInfoTypeDef(TypedDict):
    MaxConnectionsPercent: NotRequired[int]
    MaxIdleConnectionsPercent: NotRequired[int]
    ConnectionBorrowTimeout: NotRequired[int]
    SessionPinningFilters: NotRequired[List[str]]
    InitQuery: NotRequired[str]


class ConnectionPoolConfigurationTypeDef(TypedDict):
    MaxConnectionsPercent: NotRequired[int]
    MaxIdleConnectionsPercent: NotRequired[int]
    ConnectionBorrowTimeout: NotRequired[int]
    SessionPinningFilters: NotRequired[Sequence[str]]
    InitQuery: NotRequired[str]


class ContextAttributeTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class DBClusterParameterGroupTypeDef(TypedDict):
    DBClusterParameterGroupName: NotRequired[str]
    DBParameterGroupFamily: NotRequired[str]
    Description: NotRequired[str]
    DBClusterParameterGroupArn: NotRequired[str]


class DBParameterGroupTypeDef(TypedDict):
    DBParameterGroupName: NotRequired[str]
    DBParameterGroupFamily: NotRequired[str]
    Description: NotRequired[str]
    DBParameterGroupArn: NotRequired[str]


class ScalingConfigurationTypeDef(TypedDict):
    MinCapacity: NotRequired[int]
    MaxCapacity: NotRequired[int]
    AutoPause: NotRequired[bool]
    SecondsUntilAutoPause: NotRequired[int]
    TimeoutAction: NotRequired[str]
    SecondsBeforeTimeout: NotRequired[int]


class ServerlessV2ScalingConfigurationTypeDef(TypedDict):
    MinCapacity: NotRequired[float]
    MaxCapacity: NotRequired[float]
    SecondsUntilAutoPause: NotRequired[int]


class ProcessorFeatureTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]


class DBProxyEndpointTypeDef(TypedDict):
    DBProxyEndpointName: NotRequired[str]
    DBProxyEndpointArn: NotRequired[str]
    DBProxyName: NotRequired[str]
    Status: NotRequired[DBProxyEndpointStatusType]
    VpcId: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[List[str]]
    VpcSubnetIds: NotRequired[List[str]]
    Endpoint: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    TargetRole: NotRequired[DBProxyEndpointTargetRoleType]
    IsDefault: NotRequired[bool]


class UserAuthConfigTypeDef(TypedDict):
    Description: NotRequired[str]
    UserName: NotRequired[str]
    AuthScheme: NotRequired[Literal["SECRETS"]]
    SecretArn: NotRequired[str]
    IAMAuth: NotRequired[IAMAuthModeType]
    ClientPasswordAuthType: NotRequired[ClientPasswordAuthTypeType]


class CustomDBEngineVersionAMITypeDef(TypedDict):
    ImageId: NotRequired[str]
    Status: NotRequired[str]


class RestoreWindowTypeDef(TypedDict):
    EarliestTime: NotRequired[datetime]
    LatestTime: NotRequired[datetime]


class DBClusterBacktrackTypeDef(TypedDict):
    DBClusterIdentifier: NotRequired[str]
    BacktrackIdentifier: NotRequired[str]
    BacktrackTo: NotRequired[datetime]
    BacktrackedFrom: NotRequired[datetime]
    BacktrackRequestCreationTime: NotRequired[datetime]
    Status: NotRequired[str]


class DBClusterEndpointTypeDef(TypedDict):
    DBClusterEndpointIdentifier: NotRequired[str]
    DBClusterIdentifier: NotRequired[str]
    DBClusterEndpointResourceIdentifier: NotRequired[str]
    Endpoint: NotRequired[str]
    Status: NotRequired[str]
    EndpointType: NotRequired[str]
    CustomEndpointType: NotRequired[str]
    StaticMembers: NotRequired[List[str]]
    ExcludedMembers: NotRequired[List[str]]
    DBClusterEndpointArn: NotRequired[str]


class DBClusterMemberTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    IsClusterWriter: NotRequired[bool]
    DBClusterParameterGroupStatus: NotRequired[str]
    PromotionTier: NotRequired[int]


class DBClusterOptionGroupStatusTypeDef(TypedDict):
    DBClusterOptionGroupName: NotRequired[str]
    Status: NotRequired[str]


class ParameterOutputTypeDef(TypedDict):
    ParameterName: NotRequired[str]
    ParameterValue: NotRequired[str]
    Description: NotRequired[str]
    Source: NotRequired[str]
    ApplyType: NotRequired[str]
    DataType: NotRequired[str]
    AllowedValues: NotRequired[str]
    IsModifiable: NotRequired[bool]
    MinimumEngineVersion: NotRequired[str]
    ApplyMethod: NotRequired[ApplyMethodType]
    SupportedEngineModes: NotRequired[List[str]]


class DBClusterRoleTypeDef(TypedDict):
    RoleArn: NotRequired[str]
    Status: NotRequired[str]
    FeatureName: NotRequired[str]


class DBClusterSnapshotAttributeTypeDef(TypedDict):
    AttributeName: NotRequired[str]
    AttributeValues: NotRequired[List[str]]


class DBClusterStatusInfoTypeDef(TypedDict):
    StatusType: NotRequired[str]
    Normal: NotRequired[bool]
    Status: NotRequired[str]
    Message: NotRequired[str]


class DomainMembershipTypeDef(TypedDict):
    Domain: NotRequired[str]
    Status: NotRequired[str]
    FQDN: NotRequired[str]
    IAMRoleName: NotRequired[str]
    OU: NotRequired[str]
    AuthSecretArn: NotRequired[str]
    DnsIps: NotRequired[List[str]]


class LimitlessDatabaseTypeDef(TypedDict):
    Status: NotRequired[LimitlessDatabaseStatusType]
    MinRequiredACU: NotRequired[float]


class MasterUserSecretTypeDef(TypedDict):
    SecretArn: NotRequired[str]
    SecretStatus: NotRequired[str]
    KmsKeyId: NotRequired[str]


class ScalingConfigurationInfoTypeDef(TypedDict):
    MinCapacity: NotRequired[int]
    MaxCapacity: NotRequired[int]
    AutoPause: NotRequired[bool]
    SecondsUntilAutoPause: NotRequired[int]
    TimeoutAction: NotRequired[str]
    SecondsBeforeTimeout: NotRequired[int]


class ServerlessV2ScalingConfigurationInfoTypeDef(TypedDict):
    MinCapacity: NotRequired[float]
    MaxCapacity: NotRequired[float]
    SecondsUntilAutoPause: NotRequired[int]


class VpcSecurityGroupMembershipTypeDef(TypedDict):
    VpcSecurityGroupId: NotRequired[str]
    Status: NotRequired[str]


class ServerlessV2FeaturesSupportTypeDef(TypedDict):
    MinCapacity: NotRequired[float]
    MaxCapacity: NotRequired[float]


class TimezoneTypeDef(TypedDict):
    TimezoneName: NotRequired[str]


class UpgradeTargetTypeDef(TypedDict):
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    Description: NotRequired[str]
    AutoUpgrade: NotRequired[bool]
    IsMajorVersionUpgrade: NotRequired[bool]
    SupportedEngineModes: NotRequired[List[str]]
    SupportsParallelQuery: NotRequired[bool]
    SupportsGlobalDatabases: NotRequired[bool]
    SupportsBabelfish: NotRequired[bool]
    SupportsLimitlessDatabase: NotRequired[bool]
    SupportsLocalWriteForwarding: NotRequired[bool]
    SupportsIntegrations: NotRequired[bool]


class DBInstanceAutomatedBackupsReplicationTypeDef(TypedDict):
    DBInstanceAutomatedBackupsArn: NotRequired[str]


class DBInstanceRoleTypeDef(TypedDict):
    RoleArn: NotRequired[str]
    FeatureName: NotRequired[str]
    Status: NotRequired[str]


class DBInstanceStatusInfoTypeDef(TypedDict):
    StatusType: NotRequired[str]
    Normal: NotRequired[bool]
    Status: NotRequired[str]
    Message: NotRequired[str]


class DBParameterGroupStatusTypeDef(TypedDict):
    DBParameterGroupName: NotRequired[str]
    ParameterApplyStatus: NotRequired[str]


class DBSecurityGroupMembershipTypeDef(TypedDict):
    DBSecurityGroupName: NotRequired[str]
    Status: NotRequired[str]


class EndpointTypeDef(TypedDict):
    Address: NotRequired[str]
    Port: NotRequired[int]
    HostedZoneId: NotRequired[str]


class OptionGroupMembershipTypeDef(TypedDict):
    OptionGroupName: NotRequired[str]
    Status: NotRequired[str]


class TargetHealthTypeDef(TypedDict):
    State: NotRequired[TargetStateType]
    Reason: NotRequired[TargetHealthReasonType]
    Description: NotRequired[str]


class UserAuthConfigInfoTypeDef(TypedDict):
    Description: NotRequired[str]
    UserName: NotRequired[str]
    AuthScheme: NotRequired[Literal["SECRETS"]]
    SecretArn: NotRequired[str]
    IAMAuth: NotRequired[IAMAuthModeType]
    ClientPasswordAuthType: NotRequired[ClientPasswordAuthTypeType]


DocLinkTypeDef = TypedDict(
    "DocLinkTypeDef",
    {
        "Text": NotRequired[str],
        "Url": NotRequired[str],
    },
)


class EC2SecurityGroupTypeDef(TypedDict):
    Status: NotRequired[str]
    EC2SecurityGroupName: NotRequired[str]
    EC2SecurityGroupId: NotRequired[str]
    EC2SecurityGroupOwnerId: NotRequired[str]


class IPRangeTypeDef(TypedDict):
    Status: NotRequired[str]
    CIDRIP: NotRequired[str]


class DBSnapshotAttributeTypeDef(TypedDict):
    AttributeName: NotRequired[str]
    AttributeValues: NotRequired[List[str]]


class DeleteBlueGreenDeploymentRequestRequestTypeDef(TypedDict):
    BlueGreenDeploymentIdentifier: str
    DeleteTarget: NotRequired[bool]


class DeleteCustomDBEngineVersionMessageRequestTypeDef(TypedDict):
    Engine: str
    EngineVersion: str


class DeleteDBClusterAutomatedBackupMessageRequestTypeDef(TypedDict):
    DbClusterResourceId: str


class DeleteDBClusterEndpointMessageRequestTypeDef(TypedDict):
    DBClusterEndpointIdentifier: str


class DeleteDBClusterMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str
    SkipFinalSnapshot: NotRequired[bool]
    FinalDBSnapshotIdentifier: NotRequired[str]
    DeleteAutomatedBackups: NotRequired[bool]


class DeleteDBClusterParameterGroupMessageRequestTypeDef(TypedDict):
    DBClusterParameterGroupName: str


class DeleteDBClusterSnapshotMessageRequestTypeDef(TypedDict):
    DBClusterSnapshotIdentifier: str


class DeleteDBInstanceAutomatedBackupMessageRequestTypeDef(TypedDict):
    DbiResourceId: NotRequired[str]
    DBInstanceAutomatedBackupsArn: NotRequired[str]


class DeleteDBInstanceMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    SkipFinalSnapshot: NotRequired[bool]
    FinalDBSnapshotIdentifier: NotRequired[str]
    DeleteAutomatedBackups: NotRequired[bool]


class DeleteDBParameterGroupMessageRequestTypeDef(TypedDict):
    DBParameterGroupName: str


class DeleteDBProxyEndpointRequestRequestTypeDef(TypedDict):
    DBProxyEndpointName: str


class DeleteDBProxyRequestRequestTypeDef(TypedDict):
    DBProxyName: str


class DeleteDBSecurityGroupMessageRequestTypeDef(TypedDict):
    DBSecurityGroupName: str


class DeleteDBShardGroupMessageRequestTypeDef(TypedDict):
    DBShardGroupIdentifier: str


class DeleteDBSnapshotMessageRequestTypeDef(TypedDict):
    DBSnapshotIdentifier: str


class DeleteDBSubnetGroupMessageRequestTypeDef(TypedDict):
    DBSubnetGroupName: str


class DeleteEventSubscriptionMessageRequestTypeDef(TypedDict):
    SubscriptionName: str


class DeleteGlobalClusterMessageRequestTypeDef(TypedDict):
    GlobalClusterIdentifier: str


class DeleteIntegrationMessageRequestTypeDef(TypedDict):
    IntegrationIdentifier: str


class DeleteOptionGroupMessageRequestTypeDef(TypedDict):
    OptionGroupName: str


class DeleteTenantDatabaseMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    TenantDBName: str
    SkipFinalSnapshot: NotRequired[bool]
    FinalDBSnapshotIdentifier: NotRequired[str]


class DeregisterDBProxyTargetsRequestRequestTypeDef(TypedDict):
    DBProxyName: str
    TargetGroupName: NotRequired[str]
    DBInstanceIdentifiers: NotRequired[Sequence[str]]
    DBClusterIdentifiers: NotRequired[Sequence[str]]


class FilterTypeDef(TypedDict):
    Name: str
    Values: Sequence[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeDBClusterSnapshotAttributesMessageRequestTypeDef(TypedDict):
    DBClusterSnapshotIdentifier: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class DescribeDBLogFilesDetailsTypeDef(TypedDict):
    LogFileName: NotRequired[str]
    LastWritten: NotRequired[int]
    Size: NotRequired[int]


class DescribeDBSnapshotAttributesMessageRequestTypeDef(TypedDict):
    DBSnapshotIdentifier: str


class DescribeValidDBInstanceModificationsMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str


class DisableHttpEndpointRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class DoubleRangeTypeDef(TypedDict):
    From: NotRequired[float]
    To: NotRequired[float]


class DownloadDBLogFilePortionMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    LogFileName: str
    Marker: NotRequired[str]
    NumberOfLines: NotRequired[int]


class EnableHttpEndpointRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class EventCategoriesMapTypeDef(TypedDict):
    SourceType: NotRequired[str]
    EventCategories: NotRequired[List[str]]


class EventTypeDef(TypedDict):
    SourceIdentifier: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]
    Message: NotRequired[str]
    EventCategories: NotRequired[List[str]]
    Date: NotRequired[datetime]
    SourceArn: NotRequired[str]


class ExportTaskTypeDef(TypedDict):
    ExportTaskIdentifier: NotRequired[str]
    SourceArn: NotRequired[str]
    ExportOnly: NotRequired[List[str]]
    SnapshotTime: NotRequired[datetime]
    TaskStartTime: NotRequired[datetime]
    TaskEndTime: NotRequired[datetime]
    S3Bucket: NotRequired[str]
    S3Prefix: NotRequired[str]
    IamRoleArn: NotRequired[str]
    KmsKeyId: NotRequired[str]
    Status: NotRequired[str]
    PercentProgress: NotRequired[int]
    TotalExtractedDataInGB: NotRequired[int]
    FailureCause: NotRequired[str]
    WarningMessage: NotRequired[str]
    SourceType: NotRequired[ExportSourceTypeType]


class FailoverDBClusterMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str
    TargetDBInstanceIdentifier: NotRequired[str]


class FailoverGlobalClusterMessageRequestTypeDef(TypedDict):
    GlobalClusterIdentifier: str
    TargetDbClusterIdentifier: str
    AllowDataLoss: NotRequired[bool]
    Switchover: NotRequired[bool]


class FailoverStateTypeDef(TypedDict):
    Status: NotRequired[FailoverStatusType]
    FromDbClusterArn: NotRequired[str]
    ToDbClusterArn: NotRequired[str]
    IsDataLossAllowed: NotRequired[bool]


class GlobalClusterMemberTypeDef(TypedDict):
    DBClusterArn: NotRequired[str]
    Readers: NotRequired[List[str]]
    IsWriter: NotRequired[bool]
    GlobalWriteForwardingStatus: NotRequired[WriteForwardingStatusType]
    SynchronizationStatus: NotRequired[GlobalClusterMemberSynchronizationStatusType]


class IntegrationErrorTypeDef(TypedDict):
    ErrorCode: str
    ErrorMessage: NotRequired[str]


class MinimumEngineVersionPerAllowedValueTypeDef(TypedDict):
    AllowedValue: NotRequired[str]
    MinimumEngineVersion: NotRequired[str]


class ModifyActivityStreamRequestRequestTypeDef(TypedDict):
    ResourceArn: NotRequired[str]
    AuditPolicyState: NotRequired[AuditPolicyStateType]


class ModifyCertificatesMessageRequestTypeDef(TypedDict):
    CertificateIdentifier: NotRequired[str]
    RemoveCustomerOverride: NotRequired[bool]


class ModifyCurrentDBClusterCapacityMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str
    Capacity: NotRequired[int]
    SecondsBeforeTimeout: NotRequired[int]
    TimeoutAction: NotRequired[str]


class ModifyCustomDBEngineVersionMessageRequestTypeDef(TypedDict):
    Engine: str
    EngineVersion: str
    Description: NotRequired[str]
    Status: NotRequired[CustomEngineVersionStatusType]


class ModifyDBClusterEndpointMessageRequestTypeDef(TypedDict):
    DBClusterEndpointIdentifier: str
    EndpointType: NotRequired[str]
    StaticMembers: NotRequired[Sequence[str]]
    ExcludedMembers: NotRequired[Sequence[str]]


class ModifyDBClusterSnapshotAttributeMessageRequestTypeDef(TypedDict):
    DBClusterSnapshotIdentifier: str
    AttributeName: str
    ValuesToAdd: NotRequired[Sequence[str]]
    ValuesToRemove: NotRequired[Sequence[str]]


class ParameterTypeDef(TypedDict):
    ParameterName: NotRequired[str]
    ParameterValue: NotRequired[str]
    Description: NotRequired[str]
    Source: NotRequired[str]
    ApplyType: NotRequired[str]
    DataType: NotRequired[str]
    AllowedValues: NotRequired[str]
    IsModifiable: NotRequired[bool]
    MinimumEngineVersion: NotRequired[str]
    ApplyMethod: NotRequired[ApplyMethodType]
    SupportedEngineModes: NotRequired[Sequence[str]]


class ModifyDBProxyEndpointRequestRequestTypeDef(TypedDict):
    DBProxyEndpointName: str
    NewDBProxyEndpointName: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]


class RecommendedActionUpdateTypeDef(TypedDict):
    ActionId: str
    Status: str


class ModifyDBShardGroupMessageRequestTypeDef(TypedDict):
    DBShardGroupIdentifier: str
    MaxACU: NotRequired[float]
    MinACU: NotRequired[float]
    ComputeRedundancy: NotRequired[int]


class ModifyDBSnapshotAttributeMessageRequestTypeDef(TypedDict):
    DBSnapshotIdentifier: str
    AttributeName: str
    ValuesToAdd: NotRequired[Sequence[str]]
    ValuesToRemove: NotRequired[Sequence[str]]


class ModifyDBSnapshotMessageRequestTypeDef(TypedDict):
    DBSnapshotIdentifier: str
    EngineVersion: NotRequired[str]
    OptionGroupName: NotRequired[str]


class ModifyDBSubnetGroupMessageRequestTypeDef(TypedDict):
    DBSubnetGroupName: str
    SubnetIds: Sequence[str]
    DBSubnetGroupDescription: NotRequired[str]


class ModifyEventSubscriptionMessageRequestTypeDef(TypedDict):
    SubscriptionName: str
    SnsTopicArn: NotRequired[str]
    SourceType: NotRequired[str]
    EventCategories: NotRequired[Sequence[str]]
    Enabled: NotRequired[bool]


class ModifyGlobalClusterMessageRequestTypeDef(TypedDict):
    GlobalClusterIdentifier: NotRequired[str]
    NewGlobalClusterIdentifier: NotRequired[str]
    DeletionProtection: NotRequired[bool]
    EngineVersion: NotRequired[str]
    AllowMajorVersionUpgrade: NotRequired[bool]


class ModifyIntegrationMessageRequestTypeDef(TypedDict):
    IntegrationIdentifier: str
    IntegrationName: NotRequired[str]
    DataFilter: NotRequired[str]
    Description: NotRequired[str]


class ModifyTenantDatabaseMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    TenantDBName: str
    MasterUserPassword: NotRequired[str]
    NewTenantDBName: NotRequired[str]


class OptionSettingTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]
    DefaultValue: NotRequired[str]
    Description: NotRequired[str]
    ApplyType: NotRequired[str]
    DataType: NotRequired[str]
    AllowedValues: NotRequired[str]
    IsModifiable: NotRequired[bool]
    IsCollection: NotRequired[bool]


class OptionVersionTypeDef(TypedDict):
    Version: NotRequired[str]
    IsDefault: NotRequired[bool]


class OutpostTypeDef(TypedDict):
    Arn: NotRequired[str]


class PendingMaintenanceActionTypeDef(TypedDict):
    Action: NotRequired[str]
    AutoAppliedAfterDate: NotRequired[datetime]
    ForcedApplyDate: NotRequired[datetime]
    OptInStatus: NotRequired[str]
    CurrentApplyDate: NotRequired[datetime]
    Description: NotRequired[str]


class PerformanceInsightsMetricDimensionGroupTypeDef(TypedDict):
    Dimensions: NotRequired[List[str]]
    Group: NotRequired[str]
    Limit: NotRequired[int]


class PromoteReadReplicaDBClusterMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str


class PromoteReadReplicaMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    BackupRetentionPeriod: NotRequired[int]
    PreferredBackupWindow: NotRequired[str]


class RangeTypeDef(TypedDict):
    From: NotRequired[int]
    To: NotRequired[int]
    Step: NotRequired[int]


class RebootDBClusterMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str


class RebootDBInstanceMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    ForceFailover: NotRequired[bool]


class RebootDBShardGroupMessageRequestTypeDef(TypedDict):
    DBShardGroupIdentifier: str


class RecommendedActionParameterTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class RecurringChargeTypeDef(TypedDict):
    RecurringChargeAmount: NotRequired[float]
    RecurringChargeFrequency: NotRequired[str]


class ScalarReferenceDetailsTypeDef(TypedDict):
    Value: NotRequired[float]


class RegisterDBProxyTargetsRequestRequestTypeDef(TypedDict):
    DBProxyName: str
    TargetGroupName: NotRequired[str]
    DBInstanceIdentifiers: NotRequired[Sequence[str]]
    DBClusterIdentifiers: NotRequired[Sequence[str]]


class RemoveFromGlobalClusterMessageRequestTypeDef(TypedDict):
    GlobalClusterIdentifier: NotRequired[str]
    DbClusterIdentifier: NotRequired[str]


class RemoveRoleFromDBClusterMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str
    RoleArn: str
    FeatureName: NotRequired[str]


class RemoveRoleFromDBInstanceMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    RoleArn: str
    FeatureName: str


class RemoveSourceIdentifierFromSubscriptionMessageRequestTypeDef(TypedDict):
    SubscriptionName: str
    SourceIdentifier: str


class RemoveTagsFromResourceMessageRequestTypeDef(TypedDict):
    ResourceName: str
    TagKeys: Sequence[str]


class RevokeDBSecurityGroupIngressMessageRequestTypeDef(TypedDict):
    DBSecurityGroupName: str
    CIDRIP: NotRequired[str]
    EC2SecurityGroupName: NotRequired[str]
    EC2SecurityGroupId: NotRequired[str]
    EC2SecurityGroupOwnerId: NotRequired[str]


SourceRegionTypeDef = TypedDict(
    "SourceRegionTypeDef",
    {
        "RegionName": NotRequired[str],
        "Endpoint": NotRequired[str],
        "Status": NotRequired[str],
        "SupportsDBInstanceAutomatedBackupsReplication": NotRequired[bool],
    },
)


class StartActivityStreamRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Mode: ActivityStreamModeType
    KmsKeyId: str
    ApplyImmediately: NotRequired[bool]
    EngineNativeAuditFieldsIncluded: NotRequired[bool]


class StartDBClusterMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str


class StartDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef(TypedDict):
    SourceDBInstanceArn: str
    BackupRetentionPeriod: NotRequired[int]
    KmsKeyId: NotRequired[str]
    PreSignedUrl: NotRequired[str]
    SourceRegion: NotRequired[str]


class StartDBInstanceMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str


class StartExportTaskMessageRequestTypeDef(TypedDict):
    ExportTaskIdentifier: str
    SourceArn: str
    S3BucketName: str
    IamRoleArn: str
    KmsKeyId: str
    S3Prefix: NotRequired[str]
    ExportOnly: NotRequired[Sequence[str]]


class StopActivityStreamRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    ApplyImmediately: NotRequired[bool]


class StopDBClusterMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str


class StopDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef(TypedDict):
    SourceDBInstanceArn: str


class StopDBInstanceMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    DBSnapshotIdentifier: NotRequired[str]


class SwitchoverBlueGreenDeploymentRequestRequestTypeDef(TypedDict):
    BlueGreenDeploymentIdentifier: str
    SwitchoverTimeout: NotRequired[int]


class SwitchoverGlobalClusterMessageRequestTypeDef(TypedDict):
    GlobalClusterIdentifier: str
    TargetDbClusterIdentifier: str


class SwitchoverReadReplicaMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str


class TenantDatabasePendingModifiedValuesTypeDef(TypedDict):
    MasterUserPassword: NotRequired[str]
    TenantDBName: NotRequired[str]


class AccountAttributesMessageTypeDef(TypedDict):
    AccountQuotas: List[AccountQuotaTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DBClusterBacktrackResponseTypeDef(TypedDict):
    DBClusterIdentifier: str
    BacktrackIdentifier: str
    BacktrackTo: datetime
    BacktrackedFrom: datetime
    BacktrackRequestCreationTime: datetime
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef


class DBClusterCapacityInfoTypeDef(TypedDict):
    DBClusterIdentifier: str
    PendingCapacity: int
    CurrentCapacity: int
    SecondsBeforeTimeout: int
    TimeoutAction: str
    ResponseMetadata: ResponseMetadataTypeDef


class DBClusterEndpointResponseTypeDef(TypedDict):
    DBClusterEndpointIdentifier: str
    DBClusterIdentifier: str
    DBClusterEndpointResourceIdentifier: str
    Endpoint: str
    Status: str
    EndpointType: str
    CustomEndpointType: str
    StaticMembers: List[str]
    ExcludedMembers: List[str]
    DBClusterEndpointArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DBClusterParameterGroupNameMessageTypeDef(TypedDict):
    DBClusterParameterGroupName: str
    ResponseMetadata: ResponseMetadataTypeDef


class DBParameterGroupNameMessageTypeDef(TypedDict):
    DBParameterGroupName: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisableHttpEndpointResponseTypeDef(TypedDict):
    ResourceArn: str
    HttpEndpointEnabled: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DownloadDBLogFilePortionDetailsTypeDef(TypedDict):
    LogFileData: str
    Marker: str
    AdditionalDataPending: bool
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class EnableHttpEndpointResponseTypeDef(TypedDict):
    ResourceArn: str
    HttpEndpointEnabled: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ExportTaskResponseTypeDef(TypedDict):
    ExportTaskIdentifier: str
    SourceArn: str
    ExportOnly: List[str]
    SnapshotTime: datetime
    TaskStartTime: datetime
    TaskEndTime: datetime
    S3Bucket: str
    S3Prefix: str
    IamRoleArn: str
    KmsKeyId: str
    Status: str
    PercentProgress: int
    TotalExtractedDataInGB: int
    FailureCause: str
    WarningMessage: str
    SourceType: ExportSourceTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyActivityStreamResponseTypeDef(TypedDict):
    KmsKeyId: str
    KinesisStreamName: str
    Status: ActivityStreamStatusType
    Mode: ActivityStreamModeType
    EngineNativeAuditFieldsIncluded: bool
    PolicyStatus: ActivityStreamPolicyStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class StartActivityStreamResponseTypeDef(TypedDict):
    KmsKeyId: str
    KinesisStreamName: str
    Status: ActivityStreamStatusType
    Mode: ActivityStreamModeType
    ApplyImmediately: bool
    EngineNativeAuditFieldsIncluded: bool
    ResponseMetadata: ResponseMetadataTypeDef


class StopActivityStreamResponseTypeDef(TypedDict):
    KmsKeyId: str
    KinesisStreamName: str
    Status: ActivityStreamStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class AddSourceIdentifierToSubscriptionResultTypeDef(TypedDict):
    EventSubscription: EventSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEventSubscriptionResultTypeDef(TypedDict):
    EventSubscription: EventSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteEventSubscriptionResultTypeDef(TypedDict):
    EventSubscription: EventSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EventSubscriptionsMessageTypeDef(TypedDict):
    Marker: str
    EventSubscriptionsList: List[EventSubscriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyEventSubscriptionResultTypeDef(TypedDict):
    EventSubscription: EventSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RemoveSourceIdentifierFromSubscriptionResultTypeDef(TypedDict):
    EventSubscription: EventSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AddTagsToResourceMessageRequestTypeDef(TypedDict):
    ResourceName: str
    Tags: Sequence[TagTypeDef]


class CopyDBClusterParameterGroupMessageRequestTypeDef(TypedDict):
    SourceDBClusterParameterGroupIdentifier: str
    TargetDBClusterParameterGroupIdentifier: str
    TargetDBClusterParameterGroupDescription: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CopyDBClusterSnapshotMessageRequestTypeDef(TypedDict):
    SourceDBClusterSnapshotIdentifier: str
    TargetDBClusterSnapshotIdentifier: str
    KmsKeyId: NotRequired[str]
    PreSignedUrl: NotRequired[str]
    CopyTags: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
    SourceRegion: NotRequired[str]


class CopyDBParameterGroupMessageRequestTypeDef(TypedDict):
    SourceDBParameterGroupIdentifier: str
    TargetDBParameterGroupIdentifier: str
    TargetDBParameterGroupDescription: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CopyDBSnapshotMessageRequestTypeDef(TypedDict):
    SourceDBSnapshotIdentifier: str
    TargetDBSnapshotIdentifier: str
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    CopyTags: NotRequired[bool]
    PreSignedUrl: NotRequired[str]
    OptionGroupName: NotRequired[str]
    TargetCustomAvailabilityZone: NotRequired[str]
    CopyOptionGroup: NotRequired[bool]
    SourceRegion: NotRequired[str]


class CopyOptionGroupMessageRequestTypeDef(TypedDict):
    SourceOptionGroupIdentifier: str
    TargetOptionGroupIdentifier: str
    TargetOptionGroupDescription: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateBlueGreenDeploymentRequestRequestTypeDef(TypedDict):
    BlueGreenDeploymentName: str
    Source: str
    TargetEngineVersion: NotRequired[str]
    TargetDBParameterGroupName: NotRequired[str]
    TargetDBClusterParameterGroupName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    TargetDBInstanceClass: NotRequired[str]
    UpgradeTargetStorageConfig: NotRequired[bool]
    TargetIops: NotRequired[int]
    TargetStorageType: NotRequired[str]
    TargetAllocatedStorage: NotRequired[int]
    TargetStorageThroughput: NotRequired[int]


class CreateCustomDBEngineVersionMessageRequestTypeDef(TypedDict):
    Engine: str
    EngineVersion: str
    DatabaseInstallationFilesS3BucketName: NotRequired[str]
    DatabaseInstallationFilesS3Prefix: NotRequired[str]
    ImageId: NotRequired[str]
    KMSKeyId: NotRequired[str]
    Description: NotRequired[str]
    Manifest: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    SourceCustomDbEngineVersionIdentifier: NotRequired[str]
    UseAwsProvidedLatestImage: NotRequired[bool]


class CreateDBClusterEndpointMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str
    DBClusterEndpointIdentifier: str
    EndpointType: str
    StaticMembers: NotRequired[Sequence[str]]
    ExcludedMembers: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateDBClusterParameterGroupMessageRequestTypeDef(TypedDict):
    DBClusterParameterGroupName: str
    DBParameterGroupFamily: str
    Description: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateDBClusterSnapshotMessageRequestTypeDef(TypedDict):
    DBClusterSnapshotIdentifier: str
    DBClusterIdentifier: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateDBParameterGroupMessageRequestTypeDef(TypedDict):
    DBParameterGroupName: str
    DBParameterGroupFamily: str
    Description: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateDBProxyEndpointRequestRequestTypeDef(TypedDict):
    DBProxyName: str
    DBProxyEndpointName: str
    VpcSubnetIds: Sequence[str]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    TargetRole: NotRequired[DBProxyEndpointTargetRoleType]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateDBSecurityGroupMessageRequestTypeDef(TypedDict):
    DBSecurityGroupName: str
    DBSecurityGroupDescription: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateDBShardGroupMessageRequestTypeDef(TypedDict):
    DBShardGroupIdentifier: str
    DBClusterIdentifier: str
    MaxACU: float
    ComputeRedundancy: NotRequired[int]
    MinACU: NotRequired[float]
    PubliclyAccessible: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateDBSnapshotMessageRequestTypeDef(TypedDict):
    DBSnapshotIdentifier: str
    DBInstanceIdentifier: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateDBSubnetGroupMessageRequestTypeDef(TypedDict):
    DBSubnetGroupName: str
    DBSubnetGroupDescription: str
    SubnetIds: Sequence[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateEventSubscriptionMessageRequestTypeDef(TypedDict):
    SubscriptionName: str
    SnsTopicArn: str
    SourceType: NotRequired[str]
    EventCategories: NotRequired[Sequence[str]]
    SourceIds: NotRequired[Sequence[str]]
    Enabled: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateGlobalClusterMessageRequestTypeDef(TypedDict):
    GlobalClusterIdentifier: NotRequired[str]
    SourceDBClusterIdentifier: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    EngineLifecycleSupport: NotRequired[str]
    DeletionProtection: NotRequired[bool]
    DatabaseName: NotRequired[str]
    StorageEncrypted: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateIntegrationMessageRequestTypeDef(TypedDict):
    SourceArn: str
    TargetArn: str
    IntegrationName: str
    KMSKeyId: NotRequired[str]
    AdditionalEncryptionContext: NotRequired[Mapping[str, str]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    DataFilter: NotRequired[str]
    Description: NotRequired[str]


class CreateOptionGroupMessageRequestTypeDef(TypedDict):
    OptionGroupName: str
    EngineName: str
    MajorEngineVersion: str
    OptionGroupDescription: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateTenantDatabaseMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    TenantDBName: str
    MasterUsername: str
    MasterUserPassword: str
    CharacterSetName: NotRequired[str]
    NcharCharacterSetName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DBClusterSnapshotTypeDef(TypedDict):
    AvailabilityZones: NotRequired[List[str]]
    DBClusterSnapshotIdentifier: NotRequired[str]
    DBClusterIdentifier: NotRequired[str]
    SnapshotCreateTime: NotRequired[datetime]
    Engine: NotRequired[str]
    EngineMode: NotRequired[str]
    AllocatedStorage: NotRequired[int]
    Status: NotRequired[str]
    Port: NotRequired[int]
    VpcId: NotRequired[str]
    ClusterCreateTime: NotRequired[datetime]
    MasterUsername: NotRequired[str]
    EngineVersion: NotRequired[str]
    LicenseModel: NotRequired[str]
    SnapshotType: NotRequired[str]
    PercentProgress: NotRequired[int]
    StorageEncrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    DBClusterSnapshotArn: NotRequired[str]
    SourceDBClusterSnapshotArn: NotRequired[str]
    IAMDatabaseAuthenticationEnabled: NotRequired[bool]
    TagList: NotRequired[List[TagTypeDef]]
    DBSystemId: NotRequired[str]
    StorageType: NotRequired[str]
    DbClusterResourceId: NotRequired[str]
    StorageThroughput: NotRequired[int]


class DBShardGroupResponseTypeDef(TypedDict):
    DBShardGroupResourceId: str
    DBShardGroupIdentifier: str
    DBClusterIdentifier: str
    MaxACU: float
    MinACU: float
    ComputeRedundancy: int
    Status: str
    PubliclyAccessible: bool
    Endpoint: str
    DBShardGroupArn: str
    TagList: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DBShardGroupTypeDef(TypedDict):
    DBShardGroupResourceId: NotRequired[str]
    DBShardGroupIdentifier: NotRequired[str]
    DBClusterIdentifier: NotRequired[str]
    MaxACU: NotRequired[float]
    MinACU: NotRequired[float]
    ComputeRedundancy: NotRequired[int]
    Status: NotRequired[str]
    PubliclyAccessible: NotRequired[bool]
    Endpoint: NotRequired[str]
    DBShardGroupArn: NotRequired[str]
    TagList: NotRequired[List[TagTypeDef]]


class DBSnapshotTenantDatabaseTypeDef(TypedDict):
    DBSnapshotIdentifier: NotRequired[str]
    DBInstanceIdentifier: NotRequired[str]
    DbiResourceId: NotRequired[str]
    EngineName: NotRequired[str]
    SnapshotType: NotRequired[str]
    TenantDatabaseCreateTime: NotRequired[datetime]
    TenantDBName: NotRequired[str]
    MasterUsername: NotRequired[str]
    TenantDatabaseResourceId: NotRequired[str]
    CharacterSetName: NotRequired[str]
    DBSnapshotTenantDatabaseARN: NotRequired[str]
    NcharCharacterSetName: NotRequired[str]
    TagList: NotRequired[List[TagTypeDef]]


class PurchaseReservedDBInstancesOfferingMessageRequestTypeDef(TypedDict):
    ReservedDBInstancesOfferingId: str
    ReservedDBInstanceId: NotRequired[str]
    DBInstanceCount: NotRequired[int]
    Tags: NotRequired[Sequence[TagTypeDef]]


class TagListMessageTypeDef(TypedDict):
    TagList: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class OrderableDBInstanceOptionTypeDef(TypedDict):
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    DBInstanceClass: NotRequired[str]
    LicenseModel: NotRequired[str]
    AvailabilityZoneGroup: NotRequired[str]
    AvailabilityZones: NotRequired[List[AvailabilityZoneTypeDef]]
    MultiAZCapable: NotRequired[bool]
    ReadReplicaCapable: NotRequired[bool]
    Vpc: NotRequired[bool]
    SupportsStorageEncryption: NotRequired[bool]
    StorageType: NotRequired[str]
    SupportsIops: NotRequired[bool]
    SupportsEnhancedMonitoring: NotRequired[bool]
    SupportsIAMDatabaseAuthentication: NotRequired[bool]
    SupportsPerformanceInsights: NotRequired[bool]
    MinStorageSize: NotRequired[int]
    MaxStorageSize: NotRequired[int]
    MinIopsPerDbInstance: NotRequired[int]
    MaxIopsPerDbInstance: NotRequired[int]
    MinIopsPerGib: NotRequired[float]
    MaxIopsPerGib: NotRequired[float]
    AvailableProcessorFeatures: NotRequired[List[AvailableProcessorFeatureTypeDef]]
    SupportedEngineModes: NotRequired[List[str]]
    SupportsStorageAutoscaling: NotRequired[bool]
    SupportsKerberosAuthentication: NotRequired[bool]
    OutpostCapable: NotRequired[bool]
    SupportedActivityStreamModes: NotRequired[List[str]]
    SupportsGlobalDatabases: NotRequired[bool]
    SupportsClusters: NotRequired[bool]
    SupportedNetworkTypes: NotRequired[List[str]]
    SupportsStorageThroughput: NotRequired[bool]
    MinStorageThroughputPerDbInstance: NotRequired[int]
    MaxStorageThroughputPerDbInstance: NotRequired[int]
    MinStorageThroughputPerIops: NotRequired[float]
    MaxStorageThroughputPerIops: NotRequired[float]
    SupportsDedicatedLogVolume: NotRequired[bool]


class BacktrackDBClusterMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str
    BacktrackTo: TimestampTypeDef
    Force: NotRequired[bool]
    UseEarliestTimeOnPointInTimeUnavailable: NotRequired[bool]


class BlueGreenDeploymentTypeDef(TypedDict):
    BlueGreenDeploymentIdentifier: NotRequired[str]
    BlueGreenDeploymentName: NotRequired[str]
    Source: NotRequired[str]
    Target: NotRequired[str]
    SwitchoverDetails: NotRequired[List[SwitchoverDetailTypeDef]]
    Tasks: NotRequired[List[BlueGreenDeploymentTaskTypeDef]]
    Status: NotRequired[str]
    StatusDetails: NotRequired[str]
    CreateTime: NotRequired[datetime]
    DeleteTime: NotRequired[datetime]
    TagList: NotRequired[List[TagTypeDef]]


class CertificateMessageTypeDef(TypedDict):
    DefaultCertificateForNewLaunches: str
    Certificates: List[CertificateTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyCertificatesResultTypeDef(TypedDict):
    Certificate: CertificateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ClusterPendingModifiedValuesTypeDef(TypedDict):
    PendingCloudwatchLogsExports: NotRequired[PendingCloudwatchLogsExportsTypeDef]
    DBClusterIdentifier: NotRequired[str]
    MasterUserPassword: NotRequired[str]
    IAMDatabaseAuthenticationEnabled: NotRequired[bool]
    EngineVersion: NotRequired[str]
    BackupRetentionPeriod: NotRequired[int]
    AllocatedStorage: NotRequired[int]
    RdsCustomClusterConfiguration: NotRequired[RdsCustomClusterConfigurationTypeDef]
    Iops: NotRequired[int]
    StorageType: NotRequired[str]
    CertificateDetails: NotRequired[CertificateDetailsTypeDef]


class DBProxyTargetGroupTypeDef(TypedDict):
    DBProxyName: NotRequired[str]
    TargetGroupName: NotRequired[str]
    TargetGroupArn: NotRequired[str]
    IsDefault: NotRequired[bool]
    Status: NotRequired[str]
    ConnectionPoolConfig: NotRequired[ConnectionPoolConfigurationInfoTypeDef]
    CreatedDate: NotRequired[datetime]
    UpdatedDate: NotRequired[datetime]


class ModifyDBProxyTargetGroupRequestRequestTypeDef(TypedDict):
    TargetGroupName: str
    DBProxyName: str
    ConnectionPoolConfig: NotRequired[ConnectionPoolConfigurationTypeDef]
    NewName: NotRequired[str]


class CopyDBClusterParameterGroupResultTypeDef(TypedDict):
    DBClusterParameterGroup: DBClusterParameterGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDBClusterParameterGroupResultTypeDef(TypedDict):
    DBClusterParameterGroup: DBClusterParameterGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DBClusterParameterGroupsMessageTypeDef(TypedDict):
    Marker: str
    DBClusterParameterGroups: List[DBClusterParameterGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CopyDBParameterGroupResultTypeDef(TypedDict):
    DBParameterGroup: DBParameterGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDBParameterGroupResultTypeDef(TypedDict):
    DBParameterGroup: DBParameterGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DBParameterGroupsMessageTypeDef(TypedDict):
    Marker: str
    DBParameterGroups: List[DBParameterGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDBClusterMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str
    Engine: str
    AvailabilityZones: NotRequired[Sequence[str]]
    BackupRetentionPeriod: NotRequired[int]
    CharacterSetName: NotRequired[str]
    DatabaseName: NotRequired[str]
    DBClusterParameterGroupName: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    DBSubnetGroupName: NotRequired[str]
    EngineVersion: NotRequired[str]
    Port: NotRequired[int]
    MasterUsername: NotRequired[str]
    MasterUserPassword: NotRequired[str]
    OptionGroupName: NotRequired[str]
    PreferredBackupWindow: NotRequired[str]
    PreferredMaintenanceWindow: NotRequired[str]
    ReplicationSourceIdentifier: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    StorageEncrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    PreSignedUrl: NotRequired[str]
    EnableIAMDatabaseAuthentication: NotRequired[bool]
    BacktrackWindow: NotRequired[int]
    EnableCloudwatchLogsExports: NotRequired[Sequence[str]]
    EngineMode: NotRequired[str]
    ScalingConfiguration: NotRequired[ScalingConfigurationTypeDef]
    RdsCustomClusterConfiguration: NotRequired[RdsCustomClusterConfigurationTypeDef]
    DeletionProtection: NotRequired[bool]
    GlobalClusterIdentifier: NotRequired[str]
    EnableHttpEndpoint: NotRequired[bool]
    CopyTagsToSnapshot: NotRequired[bool]
    Domain: NotRequired[str]
    DomainIAMRoleName: NotRequired[str]
    EnableGlobalWriteForwarding: NotRequired[bool]
    DBClusterInstanceClass: NotRequired[str]
    AllocatedStorage: NotRequired[int]
    StorageType: NotRequired[str]
    Iops: NotRequired[int]
    PubliclyAccessible: NotRequired[bool]
    AutoMinorVersionUpgrade: NotRequired[bool]
    MonitoringInterval: NotRequired[int]
    MonitoringRoleArn: NotRequired[str]
    DatabaseInsightsMode: NotRequired[DatabaseInsightsModeType]
    EnablePerformanceInsights: NotRequired[bool]
    PerformanceInsightsKMSKeyId: NotRequired[str]
    PerformanceInsightsRetentionPeriod: NotRequired[int]
    EnableLimitlessDatabase: NotRequired[bool]
    ServerlessV2ScalingConfiguration: NotRequired[ServerlessV2ScalingConfigurationTypeDef]
    NetworkType: NotRequired[str]
    ClusterScalabilityType: NotRequired[ClusterScalabilityTypeType]
    DBSystemId: NotRequired[str]
    ManageMasterUserPassword: NotRequired[bool]
    MasterUserSecretKmsKeyId: NotRequired[str]
    EnableLocalWriteForwarding: NotRequired[bool]
    CACertificateIdentifier: NotRequired[str]
    EngineLifecycleSupport: NotRequired[str]
    SourceRegion: NotRequired[str]


class ModifyDBClusterMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str
    NewDBClusterIdentifier: NotRequired[str]
    ApplyImmediately: NotRequired[bool]
    BackupRetentionPeriod: NotRequired[int]
    DBClusterParameterGroupName: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    Port: NotRequired[int]
    MasterUserPassword: NotRequired[str]
    OptionGroupName: NotRequired[str]
    PreferredBackupWindow: NotRequired[str]
    PreferredMaintenanceWindow: NotRequired[str]
    EnableIAMDatabaseAuthentication: NotRequired[bool]
    BacktrackWindow: NotRequired[int]
    CloudwatchLogsExportConfiguration: NotRequired[CloudwatchLogsExportConfigurationTypeDef]
    EngineVersion: NotRequired[str]
    AllowMajorVersionUpgrade: NotRequired[bool]
    DBInstanceParameterGroupName: NotRequired[str]
    Domain: NotRequired[str]
    DomainIAMRoleName: NotRequired[str]
    ScalingConfiguration: NotRequired[ScalingConfigurationTypeDef]
    DeletionProtection: NotRequired[bool]
    EnableHttpEndpoint: NotRequired[bool]
    CopyTagsToSnapshot: NotRequired[bool]
    EnableGlobalWriteForwarding: NotRequired[bool]
    DBClusterInstanceClass: NotRequired[str]
    AllocatedStorage: NotRequired[int]
    StorageType: NotRequired[str]
    Iops: NotRequired[int]
    AutoMinorVersionUpgrade: NotRequired[bool]
    MonitoringInterval: NotRequired[int]
    MonitoringRoleArn: NotRequired[str]
    DatabaseInsightsMode: NotRequired[DatabaseInsightsModeType]
    EnablePerformanceInsights: NotRequired[bool]
    PerformanceInsightsKMSKeyId: NotRequired[str]
    PerformanceInsightsRetentionPeriod: NotRequired[int]
    ServerlessV2ScalingConfiguration: NotRequired[ServerlessV2ScalingConfigurationTypeDef]
    NetworkType: NotRequired[str]
    ManageMasterUserPassword: NotRequired[bool]
    RotateMasterUserPassword: NotRequired[bool]
    MasterUserSecretKmsKeyId: NotRequired[str]
    EngineMode: NotRequired[str]
    AllowEngineModeChange: NotRequired[bool]
    EnableLocalWriteForwarding: NotRequired[bool]
    AwsBackupRecoveryPointArn: NotRequired[str]
    EnableLimitlessDatabase: NotRequired[bool]
    CACertificateIdentifier: NotRequired[str]


class RestoreDBClusterFromS3MessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str
    Engine: str
    MasterUsername: str
    SourceEngine: str
    SourceEngineVersion: str
    S3BucketName: str
    S3IngestionRoleArn: str
    AvailabilityZones: NotRequired[Sequence[str]]
    BackupRetentionPeriod: NotRequired[int]
    CharacterSetName: NotRequired[str]
    DatabaseName: NotRequired[str]
    DBClusterParameterGroupName: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    DBSubnetGroupName: NotRequired[str]
    EngineVersion: NotRequired[str]
    Port: NotRequired[int]
    MasterUserPassword: NotRequired[str]
    OptionGroupName: NotRequired[str]
    PreferredBackupWindow: NotRequired[str]
    PreferredMaintenanceWindow: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    StorageEncrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    EnableIAMDatabaseAuthentication: NotRequired[bool]
    S3Prefix: NotRequired[str]
    BacktrackWindow: NotRequired[int]
    EnableCloudwatchLogsExports: NotRequired[Sequence[str]]
    DeletionProtection: NotRequired[bool]
    CopyTagsToSnapshot: NotRequired[bool]
    Domain: NotRequired[str]
    DomainIAMRoleName: NotRequired[str]
    ServerlessV2ScalingConfiguration: NotRequired[ServerlessV2ScalingConfigurationTypeDef]
    NetworkType: NotRequired[str]
    ManageMasterUserPassword: NotRequired[bool]
    MasterUserSecretKmsKeyId: NotRequired[str]
    StorageType: NotRequired[str]
    EngineLifecycleSupport: NotRequired[str]


class RestoreDBClusterFromSnapshotMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str
    SnapshotIdentifier: str
    Engine: str
    AvailabilityZones: NotRequired[Sequence[str]]
    EngineVersion: NotRequired[str]
    Port: NotRequired[int]
    DBSubnetGroupName: NotRequired[str]
    DatabaseName: NotRequired[str]
    OptionGroupName: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    KmsKeyId: NotRequired[str]
    EnableIAMDatabaseAuthentication: NotRequired[bool]
    BacktrackWindow: NotRequired[int]
    EnableCloudwatchLogsExports: NotRequired[Sequence[str]]
    EngineMode: NotRequired[str]
    ScalingConfiguration: NotRequired[ScalingConfigurationTypeDef]
    DBClusterParameterGroupName: NotRequired[str]
    DeletionProtection: NotRequired[bool]
    CopyTagsToSnapshot: NotRequired[bool]
    Domain: NotRequired[str]
    DomainIAMRoleName: NotRequired[str]
    DBClusterInstanceClass: NotRequired[str]
    StorageType: NotRequired[str]
    Iops: NotRequired[int]
    PubliclyAccessible: NotRequired[bool]
    ServerlessV2ScalingConfiguration: NotRequired[ServerlessV2ScalingConfigurationTypeDef]
    NetworkType: NotRequired[str]
    RdsCustomClusterConfiguration: NotRequired[RdsCustomClusterConfigurationTypeDef]
    MonitoringInterval: NotRequired[int]
    MonitoringRoleArn: NotRequired[str]
    EnablePerformanceInsights: NotRequired[bool]
    PerformanceInsightsKMSKeyId: NotRequired[str]
    PerformanceInsightsRetentionPeriod: NotRequired[int]
    EngineLifecycleSupport: NotRequired[str]


class RestoreDBClusterToPointInTimeMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str
    RestoreType: NotRequired[str]
    SourceDBClusterIdentifier: NotRequired[str]
    RestoreToTime: NotRequired[TimestampTypeDef]
    UseLatestRestorableTime: NotRequired[bool]
    Port: NotRequired[int]
    DBSubnetGroupName: NotRequired[str]
    OptionGroupName: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    KmsKeyId: NotRequired[str]
    EnableIAMDatabaseAuthentication: NotRequired[bool]
    BacktrackWindow: NotRequired[int]
    EnableCloudwatchLogsExports: NotRequired[Sequence[str]]
    DBClusterParameterGroupName: NotRequired[str]
    DeletionProtection: NotRequired[bool]
    CopyTagsToSnapshot: NotRequired[bool]
    Domain: NotRequired[str]
    DomainIAMRoleName: NotRequired[str]
    ScalingConfiguration: NotRequired[ScalingConfigurationTypeDef]
    EngineMode: NotRequired[str]
    DBClusterInstanceClass: NotRequired[str]
    StorageType: NotRequired[str]
    PubliclyAccessible: NotRequired[bool]
    Iops: NotRequired[int]
    ServerlessV2ScalingConfiguration: NotRequired[ServerlessV2ScalingConfigurationTypeDef]
    NetworkType: NotRequired[str]
    SourceDbClusterResourceId: NotRequired[str]
    RdsCustomClusterConfiguration: NotRequired[RdsCustomClusterConfigurationTypeDef]
    MonitoringInterval: NotRequired[int]
    MonitoringRoleArn: NotRequired[str]
    EnablePerformanceInsights: NotRequired[bool]
    PerformanceInsightsKMSKeyId: NotRequired[str]
    PerformanceInsightsRetentionPeriod: NotRequired[int]
    EngineLifecycleSupport: NotRequired[str]


class CreateDBInstanceMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    DBInstanceClass: str
    Engine: str
    DBName: NotRequired[str]
    AllocatedStorage: NotRequired[int]
    MasterUsername: NotRequired[str]
    MasterUserPassword: NotRequired[str]
    DBSecurityGroups: NotRequired[Sequence[str]]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    AvailabilityZone: NotRequired[str]
    DBSubnetGroupName: NotRequired[str]
    PreferredMaintenanceWindow: NotRequired[str]
    DBParameterGroupName: NotRequired[str]
    BackupRetentionPeriod: NotRequired[int]
    PreferredBackupWindow: NotRequired[str]
    Port: NotRequired[int]
    MultiAZ: NotRequired[bool]
    EngineVersion: NotRequired[str]
    AutoMinorVersionUpgrade: NotRequired[bool]
    LicenseModel: NotRequired[str]
    Iops: NotRequired[int]
    OptionGroupName: NotRequired[str]
    CharacterSetName: NotRequired[str]
    NcharCharacterSetName: NotRequired[str]
    PubliclyAccessible: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
    DBClusterIdentifier: NotRequired[str]
    StorageType: NotRequired[str]
    TdeCredentialArn: NotRequired[str]
    TdeCredentialPassword: NotRequired[str]
    StorageEncrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    Domain: NotRequired[str]
    DomainFqdn: NotRequired[str]
    DomainOu: NotRequired[str]
    DomainAuthSecretArn: NotRequired[str]
    DomainDnsIps: NotRequired[Sequence[str]]
    CopyTagsToSnapshot: NotRequired[bool]
    MonitoringInterval: NotRequired[int]
    MonitoringRoleArn: NotRequired[str]
    DomainIAMRoleName: NotRequired[str]
    PromotionTier: NotRequired[int]
    Timezone: NotRequired[str]
    EnableIAMDatabaseAuthentication: NotRequired[bool]
    DatabaseInsightsMode: NotRequired[DatabaseInsightsModeType]
    EnablePerformanceInsights: NotRequired[bool]
    PerformanceInsightsKMSKeyId: NotRequired[str]
    PerformanceInsightsRetentionPeriod: NotRequired[int]
    EnableCloudwatchLogsExports: NotRequired[Sequence[str]]
    ProcessorFeatures: NotRequired[Sequence[ProcessorFeatureTypeDef]]
    DeletionProtection: NotRequired[bool]
    MaxAllocatedStorage: NotRequired[int]
    EnableCustomerOwnedIp: NotRequired[bool]
    CustomIamInstanceProfile: NotRequired[str]
    BackupTarget: NotRequired[str]
    NetworkType: NotRequired[str]
    StorageThroughput: NotRequired[int]
    ManageMasterUserPassword: NotRequired[bool]
    MasterUserSecretKmsKeyId: NotRequired[str]
    CACertificateIdentifier: NotRequired[str]
    DBSystemId: NotRequired[str]
    DedicatedLogVolume: NotRequired[bool]
    MultiTenant: NotRequired[bool]
    EngineLifecycleSupport: NotRequired[str]


class CreateDBInstanceReadReplicaMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    SourceDBInstanceIdentifier: NotRequired[str]
    DBInstanceClass: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    Port: NotRequired[int]
    MultiAZ: NotRequired[bool]
    AutoMinorVersionUpgrade: NotRequired[bool]
    Iops: NotRequired[int]
    OptionGroupName: NotRequired[str]
    DBParameterGroupName: NotRequired[str]
    PubliclyAccessible: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
    DBSubnetGroupName: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    StorageType: NotRequired[str]
    CopyTagsToSnapshot: NotRequired[bool]
    MonitoringInterval: NotRequired[int]
    MonitoringRoleArn: NotRequired[str]
    KmsKeyId: NotRequired[str]
    PreSignedUrl: NotRequired[str]
    EnableIAMDatabaseAuthentication: NotRequired[bool]
    DatabaseInsightsMode: NotRequired[DatabaseInsightsModeType]
    EnablePerformanceInsights: NotRequired[bool]
    PerformanceInsightsKMSKeyId: NotRequired[str]
    PerformanceInsightsRetentionPeriod: NotRequired[int]
    EnableCloudwatchLogsExports: NotRequired[Sequence[str]]
    ProcessorFeatures: NotRequired[Sequence[ProcessorFeatureTypeDef]]
    UseDefaultProcessorFeatures: NotRequired[bool]
    DeletionProtection: NotRequired[bool]
    Domain: NotRequired[str]
    DomainIAMRoleName: NotRequired[str]
    DomainFqdn: NotRequired[str]
    DomainOu: NotRequired[str]
    DomainAuthSecretArn: NotRequired[str]
    DomainDnsIps: NotRequired[Sequence[str]]
    ReplicaMode: NotRequired[ReplicaModeType]
    MaxAllocatedStorage: NotRequired[int]
    CustomIamInstanceProfile: NotRequired[str]
    NetworkType: NotRequired[str]
    StorageThroughput: NotRequired[int]
    EnableCustomerOwnedIp: NotRequired[bool]
    AllocatedStorage: NotRequired[int]
    SourceDBClusterIdentifier: NotRequired[str]
    DedicatedLogVolume: NotRequired[bool]
    UpgradeStorageConfig: NotRequired[bool]
    CACertificateIdentifier: NotRequired[str]
    SourceRegion: NotRequired[str]


class DBSnapshotTypeDef(TypedDict):
    DBSnapshotIdentifier: NotRequired[str]
    DBInstanceIdentifier: NotRequired[str]
    SnapshotCreateTime: NotRequired[datetime]
    Engine: NotRequired[str]
    AllocatedStorage: NotRequired[int]
    Status: NotRequired[str]
    Port: NotRequired[int]
    AvailabilityZone: NotRequired[str]
    VpcId: NotRequired[str]
    InstanceCreateTime: NotRequired[datetime]
    MasterUsername: NotRequired[str]
    EngineVersion: NotRequired[str]
    LicenseModel: NotRequired[str]
    SnapshotType: NotRequired[str]
    Iops: NotRequired[int]
    OptionGroupName: NotRequired[str]
    PercentProgress: NotRequired[int]
    SourceRegion: NotRequired[str]
    SourceDBSnapshotIdentifier: NotRequired[str]
    StorageType: NotRequired[str]
    TdeCredentialArn: NotRequired[str]
    Encrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    DBSnapshotArn: NotRequired[str]
    Timezone: NotRequired[str]
    IAMDatabaseAuthenticationEnabled: NotRequired[bool]
    ProcessorFeatures: NotRequired[List[ProcessorFeatureTypeDef]]
    DbiResourceId: NotRequired[str]
    TagList: NotRequired[List[TagTypeDef]]
    OriginalSnapshotCreateTime: NotRequired[datetime]
    SnapshotDatabaseTime: NotRequired[datetime]
    SnapshotTarget: NotRequired[str]
    StorageThroughput: NotRequired[int]
    DBSystemId: NotRequired[str]
    DedicatedLogVolume: NotRequired[bool]
    MultiTenant: NotRequired[bool]


class ModifyDBInstanceMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    AllocatedStorage: NotRequired[int]
    DBInstanceClass: NotRequired[str]
    DBSubnetGroupName: NotRequired[str]
    DBSecurityGroups: NotRequired[Sequence[str]]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    ApplyImmediately: NotRequired[bool]
    MasterUserPassword: NotRequired[str]
    DBParameterGroupName: NotRequired[str]
    BackupRetentionPeriod: NotRequired[int]
    PreferredBackupWindow: NotRequired[str]
    PreferredMaintenanceWindow: NotRequired[str]
    MultiAZ: NotRequired[bool]
    EngineVersion: NotRequired[str]
    AllowMajorVersionUpgrade: NotRequired[bool]
    AutoMinorVersionUpgrade: NotRequired[bool]
    LicenseModel: NotRequired[str]
    Iops: NotRequired[int]
    OptionGroupName: NotRequired[str]
    NewDBInstanceIdentifier: NotRequired[str]
    StorageType: NotRequired[str]
    TdeCredentialArn: NotRequired[str]
    TdeCredentialPassword: NotRequired[str]
    CACertificateIdentifier: NotRequired[str]
    Domain: NotRequired[str]
    DomainFqdn: NotRequired[str]
    DomainOu: NotRequired[str]
    DomainAuthSecretArn: NotRequired[str]
    DomainDnsIps: NotRequired[Sequence[str]]
    CopyTagsToSnapshot: NotRequired[bool]
    MonitoringInterval: NotRequired[int]
    DBPortNumber: NotRequired[int]
    PubliclyAccessible: NotRequired[bool]
    MonitoringRoleArn: NotRequired[str]
    DomainIAMRoleName: NotRequired[str]
    DisableDomain: NotRequired[bool]
    PromotionTier: NotRequired[int]
    EnableIAMDatabaseAuthentication: NotRequired[bool]
    DatabaseInsightsMode: NotRequired[DatabaseInsightsModeType]
    EnablePerformanceInsights: NotRequired[bool]
    PerformanceInsightsKMSKeyId: NotRequired[str]
    PerformanceInsightsRetentionPeriod: NotRequired[int]
    CloudwatchLogsExportConfiguration: NotRequired[CloudwatchLogsExportConfigurationTypeDef]
    ProcessorFeatures: NotRequired[Sequence[ProcessorFeatureTypeDef]]
    UseDefaultProcessorFeatures: NotRequired[bool]
    DeletionProtection: NotRequired[bool]
    MaxAllocatedStorage: NotRequired[int]
    CertificateRotationRestart: NotRequired[bool]
    ReplicaMode: NotRequired[ReplicaModeType]
    EnableCustomerOwnedIp: NotRequired[bool]
    AwsBackupRecoveryPointArn: NotRequired[str]
    AutomationMode: NotRequired[AutomationModeType]
    ResumeFullAutomationModeMinutes: NotRequired[int]
    NetworkType: NotRequired[str]
    StorageThroughput: NotRequired[int]
    ManageMasterUserPassword: NotRequired[bool]
    RotateMasterUserPassword: NotRequired[bool]
    MasterUserSecretKmsKeyId: NotRequired[str]
    Engine: NotRequired[str]
    DedicatedLogVolume: NotRequired[bool]
    MultiTenant: NotRequired[bool]


class PendingModifiedValuesTypeDef(TypedDict):
    DBInstanceClass: NotRequired[str]
    AllocatedStorage: NotRequired[int]
    MasterUserPassword: NotRequired[str]
    Port: NotRequired[int]
    BackupRetentionPeriod: NotRequired[int]
    MultiAZ: NotRequired[bool]
    EngineVersion: NotRequired[str]
    LicenseModel: NotRequired[str]
    Iops: NotRequired[int]
    DBInstanceIdentifier: NotRequired[str]
    StorageType: NotRequired[str]
    CACertificateIdentifier: NotRequired[str]
    DBSubnetGroupName: NotRequired[str]
    PendingCloudwatchLogsExports: NotRequired[PendingCloudwatchLogsExportsTypeDef]
    ProcessorFeatures: NotRequired[List[ProcessorFeatureTypeDef]]
    IAMDatabaseAuthenticationEnabled: NotRequired[bool]
    AutomationMode: NotRequired[AutomationModeType]
    ResumeFullAutomationModeTime: NotRequired[datetime]
    StorageThroughput: NotRequired[int]
    Engine: NotRequired[str]
    DedicatedLogVolume: NotRequired[bool]
    MultiTenant: NotRequired[bool]


class RestoreDBInstanceFromDBSnapshotMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    DBSnapshotIdentifier: NotRequired[str]
    DBInstanceClass: NotRequired[str]
    Port: NotRequired[int]
    AvailabilityZone: NotRequired[str]
    DBSubnetGroupName: NotRequired[str]
    MultiAZ: NotRequired[bool]
    PubliclyAccessible: NotRequired[bool]
    AutoMinorVersionUpgrade: NotRequired[bool]
    LicenseModel: NotRequired[str]
    DBName: NotRequired[str]
    Engine: NotRequired[str]
    Iops: NotRequired[int]
    OptionGroupName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    StorageType: NotRequired[str]
    TdeCredentialArn: NotRequired[str]
    TdeCredentialPassword: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    Domain: NotRequired[str]
    DomainFqdn: NotRequired[str]
    DomainOu: NotRequired[str]
    DomainAuthSecretArn: NotRequired[str]
    DomainDnsIps: NotRequired[Sequence[str]]
    CopyTagsToSnapshot: NotRequired[bool]
    DomainIAMRoleName: NotRequired[str]
    EnableIAMDatabaseAuthentication: NotRequired[bool]
    EnableCloudwatchLogsExports: NotRequired[Sequence[str]]
    ProcessorFeatures: NotRequired[Sequence[ProcessorFeatureTypeDef]]
    UseDefaultProcessorFeatures: NotRequired[bool]
    DBParameterGroupName: NotRequired[str]
    DeletionProtection: NotRequired[bool]
    EnableCustomerOwnedIp: NotRequired[bool]
    CustomIamInstanceProfile: NotRequired[str]
    BackupTarget: NotRequired[str]
    NetworkType: NotRequired[str]
    StorageThroughput: NotRequired[int]
    DBClusterSnapshotIdentifier: NotRequired[str]
    AllocatedStorage: NotRequired[int]
    DedicatedLogVolume: NotRequired[bool]
    CACertificateIdentifier: NotRequired[str]
    EngineLifecycleSupport: NotRequired[str]


class RestoreDBInstanceFromS3MessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    DBInstanceClass: str
    Engine: str
    SourceEngine: str
    SourceEngineVersion: str
    S3BucketName: str
    S3IngestionRoleArn: str
    DBName: NotRequired[str]
    AllocatedStorage: NotRequired[int]
    MasterUsername: NotRequired[str]
    MasterUserPassword: NotRequired[str]
    DBSecurityGroups: NotRequired[Sequence[str]]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    AvailabilityZone: NotRequired[str]
    DBSubnetGroupName: NotRequired[str]
    PreferredMaintenanceWindow: NotRequired[str]
    DBParameterGroupName: NotRequired[str]
    BackupRetentionPeriod: NotRequired[int]
    PreferredBackupWindow: NotRequired[str]
    Port: NotRequired[int]
    MultiAZ: NotRequired[bool]
    EngineVersion: NotRequired[str]
    AutoMinorVersionUpgrade: NotRequired[bool]
    LicenseModel: NotRequired[str]
    Iops: NotRequired[int]
    OptionGroupName: NotRequired[str]
    PubliclyAccessible: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
    StorageType: NotRequired[str]
    StorageEncrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    CopyTagsToSnapshot: NotRequired[bool]
    MonitoringInterval: NotRequired[int]
    MonitoringRoleArn: NotRequired[str]
    EnableIAMDatabaseAuthentication: NotRequired[bool]
    S3Prefix: NotRequired[str]
    DatabaseInsightsMode: NotRequired[DatabaseInsightsModeType]
    EnablePerformanceInsights: NotRequired[bool]
    PerformanceInsightsKMSKeyId: NotRequired[str]
    PerformanceInsightsRetentionPeriod: NotRequired[int]
    EnableCloudwatchLogsExports: NotRequired[Sequence[str]]
    ProcessorFeatures: NotRequired[Sequence[ProcessorFeatureTypeDef]]
    UseDefaultProcessorFeatures: NotRequired[bool]
    DeletionProtection: NotRequired[bool]
    MaxAllocatedStorage: NotRequired[int]
    NetworkType: NotRequired[str]
    StorageThroughput: NotRequired[int]
    ManageMasterUserPassword: NotRequired[bool]
    MasterUserSecretKmsKeyId: NotRequired[str]
    DedicatedLogVolume: NotRequired[bool]
    CACertificateIdentifier: NotRequired[str]
    EngineLifecycleSupport: NotRequired[str]


class RestoreDBInstanceToPointInTimeMessageRequestTypeDef(TypedDict):
    TargetDBInstanceIdentifier: str
    SourceDBInstanceIdentifier: NotRequired[str]
    RestoreTime: NotRequired[TimestampTypeDef]
    UseLatestRestorableTime: NotRequired[bool]
    DBInstanceClass: NotRequired[str]
    Port: NotRequired[int]
    AvailabilityZone: NotRequired[str]
    DBSubnetGroupName: NotRequired[str]
    MultiAZ: NotRequired[bool]
    PubliclyAccessible: NotRequired[bool]
    AutoMinorVersionUpgrade: NotRequired[bool]
    LicenseModel: NotRequired[str]
    DBName: NotRequired[str]
    Engine: NotRequired[str]
    Iops: NotRequired[int]
    OptionGroupName: NotRequired[str]
    CopyTagsToSnapshot: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
    StorageType: NotRequired[str]
    TdeCredentialArn: NotRequired[str]
    TdeCredentialPassword: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    Domain: NotRequired[str]
    DomainIAMRoleName: NotRequired[str]
    DomainFqdn: NotRequired[str]
    DomainOu: NotRequired[str]
    DomainAuthSecretArn: NotRequired[str]
    DomainDnsIps: NotRequired[Sequence[str]]
    EnableIAMDatabaseAuthentication: NotRequired[bool]
    EnableCloudwatchLogsExports: NotRequired[Sequence[str]]
    ProcessorFeatures: NotRequired[Sequence[ProcessorFeatureTypeDef]]
    UseDefaultProcessorFeatures: NotRequired[bool]
    DBParameterGroupName: NotRequired[str]
    DeletionProtection: NotRequired[bool]
    SourceDbiResourceId: NotRequired[str]
    MaxAllocatedStorage: NotRequired[int]
    SourceDBInstanceAutomatedBackupsArn: NotRequired[str]
    EnableCustomerOwnedIp: NotRequired[bool]
    CustomIamInstanceProfile: NotRequired[str]
    BackupTarget: NotRequired[str]
    NetworkType: NotRequired[str]
    StorageThroughput: NotRequired[int]
    AllocatedStorage: NotRequired[int]
    DedicatedLogVolume: NotRequired[bool]
    CACertificateIdentifier: NotRequired[str]
    EngineLifecycleSupport: NotRequired[str]


class CreateDBProxyEndpointResponseTypeDef(TypedDict):
    DBProxyEndpoint: DBProxyEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDBProxyEndpointResponseTypeDef(TypedDict):
    DBProxyEndpoint: DBProxyEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDBProxyEndpointsResponseTypeDef(TypedDict):
    DBProxyEndpoints: List[DBProxyEndpointTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyDBProxyEndpointResponseTypeDef(TypedDict):
    DBProxyEndpoint: DBProxyEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDBProxyRequestRequestTypeDef(TypedDict):
    DBProxyName: str
    EngineFamily: EngineFamilyType
    Auth: Sequence[UserAuthConfigTypeDef]
    RoleArn: str
    VpcSubnetIds: Sequence[str]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    RequireTLS: NotRequired[bool]
    IdleClientTimeout: NotRequired[int]
    DebugLogging: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ModifyDBProxyRequestRequestTypeDef(TypedDict):
    DBProxyName: str
    NewDBProxyName: NotRequired[str]
    Auth: NotRequired[Sequence[UserAuthConfigTypeDef]]
    RequireTLS: NotRequired[bool]
    IdleClientTimeout: NotRequired[int]
    DebugLogging: NotRequired[bool]
    RoleArn: NotRequired[str]
    SecurityGroups: NotRequired[Sequence[str]]


class DBClusterAutomatedBackupTypeDef(TypedDict):
    Engine: NotRequired[str]
    VpcId: NotRequired[str]
    DBClusterAutomatedBackupsArn: NotRequired[str]
    DBClusterIdentifier: NotRequired[str]
    RestoreWindow: NotRequired[RestoreWindowTypeDef]
    MasterUsername: NotRequired[str]
    DbClusterResourceId: NotRequired[str]
    Region: NotRequired[str]
    LicenseModel: NotRequired[str]
    Status: NotRequired[str]
    IAMDatabaseAuthenticationEnabled: NotRequired[bool]
    ClusterCreateTime: NotRequired[datetime]
    StorageEncrypted: NotRequired[bool]
    AllocatedStorage: NotRequired[int]
    EngineVersion: NotRequired[str]
    DBClusterArn: NotRequired[str]
    BackupRetentionPeriod: NotRequired[int]
    EngineMode: NotRequired[str]
    AvailabilityZones: NotRequired[List[str]]
    Port: NotRequired[int]
    KmsKeyId: NotRequired[str]
    StorageType: NotRequired[str]
    Iops: NotRequired[int]
    AwsBackupRecoveryPointArn: NotRequired[str]
    StorageThroughput: NotRequired[int]


class DBClusterBacktrackMessageTypeDef(TypedDict):
    Marker: str
    DBClusterBacktracks: List[DBClusterBacktrackTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DBClusterEndpointMessageTypeDef(TypedDict):
    Marker: str
    DBClusterEndpoints: List[DBClusterEndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DBClusterParameterGroupDetailsTypeDef(TypedDict):
    Parameters: List[ParameterOutputTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DBParameterGroupDetailsTypeDef(TypedDict):
    Parameters: List[ParameterOutputTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class EngineDefaultsTypeDef(TypedDict):
    DBParameterGroupFamily: NotRequired[str]
    Marker: NotRequired[str]
    Parameters: NotRequired[List[ParameterOutputTypeDef]]


class DBClusterSnapshotAttributesResultTypeDef(TypedDict):
    DBClusterSnapshotIdentifier: NotRequired[str]
    DBClusterSnapshotAttributes: NotRequired[List[DBClusterSnapshotAttributeTypeDef]]


class DBEngineVersionResponseTypeDef(TypedDict):
    Engine: str
    EngineVersion: str
    DBParameterGroupFamily: str
    DBEngineDescription: str
    DBEngineVersionDescription: str
    DefaultCharacterSet: CharacterSetTypeDef
    Image: CustomDBEngineVersionAMITypeDef
    DBEngineMediaType: str
    SupportedCharacterSets: List[CharacterSetTypeDef]
    SupportedNcharCharacterSets: List[CharacterSetTypeDef]
    ValidUpgradeTarget: List[UpgradeTargetTypeDef]
    SupportedTimezones: List[TimezoneTypeDef]
    ExportableLogTypes: List[str]
    SupportsLogExportsToCloudwatchLogs: bool
    SupportsReadReplica: bool
    SupportedEngineModes: List[str]
    SupportedFeatureNames: List[str]
    Status: str
    SupportsParallelQuery: bool
    SupportsGlobalDatabases: bool
    MajorEngineVersion: str
    DatabaseInstallationFilesS3BucketName: str
    DatabaseInstallationFilesS3Prefix: str
    DBEngineVersionArn: str
    KMSKeyId: str
    CreateTime: datetime
    TagList: List[TagTypeDef]
    SupportsBabelfish: bool
    CustomDBEngineVersionManifest: str
    SupportsLimitlessDatabase: bool
    SupportsCertificateRotationWithoutRestart: bool
    SupportedCACertificateIdentifiers: List[str]
    SupportsLocalWriteForwarding: bool
    SupportsIntegrations: bool
    ServerlessV2FeaturesSupport: ServerlessV2FeaturesSupportTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DBEngineVersionTypeDef(TypedDict):
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    DBParameterGroupFamily: NotRequired[str]
    DBEngineDescription: NotRequired[str]
    DBEngineVersionDescription: NotRequired[str]
    DefaultCharacterSet: NotRequired[CharacterSetTypeDef]
    Image: NotRequired[CustomDBEngineVersionAMITypeDef]
    DBEngineMediaType: NotRequired[str]
    SupportedCharacterSets: NotRequired[List[CharacterSetTypeDef]]
    SupportedNcharCharacterSets: NotRequired[List[CharacterSetTypeDef]]
    ValidUpgradeTarget: NotRequired[List[UpgradeTargetTypeDef]]
    SupportedTimezones: NotRequired[List[TimezoneTypeDef]]
    ExportableLogTypes: NotRequired[List[str]]
    SupportsLogExportsToCloudwatchLogs: NotRequired[bool]
    SupportsReadReplica: NotRequired[bool]
    SupportedEngineModes: NotRequired[List[str]]
    SupportedFeatureNames: NotRequired[List[str]]
    Status: NotRequired[str]
    SupportsParallelQuery: NotRequired[bool]
    SupportsGlobalDatabases: NotRequired[bool]
    MajorEngineVersion: NotRequired[str]
    DatabaseInstallationFilesS3BucketName: NotRequired[str]
    DatabaseInstallationFilesS3Prefix: NotRequired[str]
    DBEngineVersionArn: NotRequired[str]
    KMSKeyId: NotRequired[str]
    CreateTime: NotRequired[datetime]
    TagList: NotRequired[List[TagTypeDef]]
    SupportsBabelfish: NotRequired[bool]
    CustomDBEngineVersionManifest: NotRequired[str]
    SupportsLimitlessDatabase: NotRequired[bool]
    SupportsCertificateRotationWithoutRestart: NotRequired[bool]
    SupportedCACertificateIdentifiers: NotRequired[List[str]]
    SupportsLocalWriteForwarding: NotRequired[bool]
    SupportsIntegrations: NotRequired[bool]
    ServerlessV2FeaturesSupport: NotRequired[ServerlessV2FeaturesSupportTypeDef]


class DBInstanceAutomatedBackupTypeDef(TypedDict):
    DBInstanceArn: NotRequired[str]
    DbiResourceId: NotRequired[str]
    Region: NotRequired[str]
    DBInstanceIdentifier: NotRequired[str]
    RestoreWindow: NotRequired[RestoreWindowTypeDef]
    AllocatedStorage: NotRequired[int]
    Status: NotRequired[str]
    Port: NotRequired[int]
    AvailabilityZone: NotRequired[str]
    VpcId: NotRequired[str]
    InstanceCreateTime: NotRequired[datetime]
    MasterUsername: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    LicenseModel: NotRequired[str]
    Iops: NotRequired[int]
    OptionGroupName: NotRequired[str]
    TdeCredentialArn: NotRequired[str]
    Encrypted: NotRequired[bool]
    StorageType: NotRequired[str]
    KmsKeyId: NotRequired[str]
    Timezone: NotRequired[str]
    IAMDatabaseAuthenticationEnabled: NotRequired[bool]
    BackupRetentionPeriod: NotRequired[int]
    DBInstanceAutomatedBackupsArn: NotRequired[str]
    DBInstanceAutomatedBackupsReplications: NotRequired[
        List[DBInstanceAutomatedBackupsReplicationTypeDef]
    ]
    BackupTarget: NotRequired[str]
    StorageThroughput: NotRequired[int]
    AwsBackupRecoveryPointArn: NotRequired[str]
    DedicatedLogVolume: NotRequired[bool]
    MultiTenant: NotRequired[bool]


DBProxyTargetTypeDef = TypedDict(
    "DBProxyTargetTypeDef",
    {
        "TargetArn": NotRequired[str],
        "Endpoint": NotRequired[str],
        "TrackedClusterId": NotRequired[str],
        "RdsResourceId": NotRequired[str],
        "Port": NotRequired[int],
        "Type": NotRequired[TargetTypeType],
        "Role": NotRequired[TargetRoleType],
        "TargetHealth": NotRequired[TargetHealthTypeDef],
    },
)


class DBProxyTypeDef(TypedDict):
    DBProxyName: NotRequired[str]
    DBProxyArn: NotRequired[str]
    Status: NotRequired[DBProxyStatusType]
    EngineFamily: NotRequired[str]
    VpcId: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[List[str]]
    VpcSubnetIds: NotRequired[List[str]]
    Auth: NotRequired[List[UserAuthConfigInfoTypeDef]]
    RoleArn: NotRequired[str]
    Endpoint: NotRequired[str]
    RequireTLS: NotRequired[bool]
    IdleClientTimeout: NotRequired[int]
    DebugLogging: NotRequired[bool]
    CreatedDate: NotRequired[datetime]
    UpdatedDate: NotRequired[datetime]


class DBSecurityGroupTypeDef(TypedDict):
    OwnerId: NotRequired[str]
    DBSecurityGroupName: NotRequired[str]
    DBSecurityGroupDescription: NotRequired[str]
    VpcId: NotRequired[str]
    EC2SecurityGroups: NotRequired[List[EC2SecurityGroupTypeDef]]
    IPRanges: NotRequired[List[IPRangeTypeDef]]
    DBSecurityGroupArn: NotRequired[str]


class DBSnapshotAttributesResultTypeDef(TypedDict):
    DBSnapshotIdentifier: NotRequired[str]
    DBSnapshotAttributes: NotRequired[List[DBSnapshotAttributeTypeDef]]


class DescribeBlueGreenDeploymentsRequestRequestTypeDef(TypedDict):
    BlueGreenDeploymentIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeCertificatesMessageRequestTypeDef(TypedDict):
    CertificateIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeDBClusterAutomatedBackupsMessageRequestTypeDef(TypedDict):
    DbClusterResourceId: NotRequired[str]
    DBClusterIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeDBClusterBacktracksMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: str
    BacktrackIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeDBClusterEndpointsMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: NotRequired[str]
    DBClusterEndpointIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeDBClusterParameterGroupsMessageRequestTypeDef(TypedDict):
    DBClusterParameterGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeDBClusterParametersMessageRequestTypeDef(TypedDict):
    DBClusterParameterGroupName: str
    Source: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeDBClusterSnapshotsMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: NotRequired[str]
    DBClusterSnapshotIdentifier: NotRequired[str]
    SnapshotType: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    IncludeShared: NotRequired[bool]
    IncludePublic: NotRequired[bool]
    DbClusterResourceId: NotRequired[str]


class DescribeDBClustersMessageRequestTypeDef(TypedDict):
    DBClusterIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    IncludeShared: NotRequired[bool]


class DescribeDBEngineVersionsMessageRequestTypeDef(TypedDict):
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    DBParameterGroupFamily: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    DefaultOnly: NotRequired[bool]
    ListSupportedCharacterSets: NotRequired[bool]
    ListSupportedTimezones: NotRequired[bool]
    IncludeAll: NotRequired[bool]


class DescribeDBInstanceAutomatedBackupsMessageRequestTypeDef(TypedDict):
    DbiResourceId: NotRequired[str]
    DBInstanceIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    DBInstanceAutomatedBackupsArn: NotRequired[str]


class DescribeDBInstancesMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeDBLogFilesMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: str
    FilenameContains: NotRequired[str]
    FileLastWritten: NotRequired[int]
    FileSize: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeDBParameterGroupsMessageRequestTypeDef(TypedDict):
    DBParameterGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeDBParametersMessageRequestTypeDef(TypedDict):
    DBParameterGroupName: str
    Source: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeDBProxiesRequestRequestTypeDef(TypedDict):
    DBProxyName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeDBProxyEndpointsRequestRequestTypeDef(TypedDict):
    DBProxyName: NotRequired[str]
    DBProxyEndpointName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeDBProxyTargetGroupsRequestRequestTypeDef(TypedDict):
    DBProxyName: str
    TargetGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeDBProxyTargetsRequestRequestTypeDef(TypedDict):
    DBProxyName: str
    TargetGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeDBRecommendationsMessageRequestTypeDef(TypedDict):
    LastUpdatedAfter: NotRequired[TimestampTypeDef]
    LastUpdatedBefore: NotRequired[TimestampTypeDef]
    Locale: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeDBSecurityGroupsMessageRequestTypeDef(TypedDict):
    DBSecurityGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeDBShardGroupsMessageRequestTypeDef(TypedDict):
    DBShardGroupIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeDBSnapshotTenantDatabasesMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    DBSnapshotIdentifier: NotRequired[str]
    SnapshotType: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    DbiResourceId: NotRequired[str]


class DescribeDBSnapshotsMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    DBSnapshotIdentifier: NotRequired[str]
    SnapshotType: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    IncludeShared: NotRequired[bool]
    IncludePublic: NotRequired[bool]
    DbiResourceId: NotRequired[str]


class DescribeDBSubnetGroupsMessageRequestTypeDef(TypedDict):
    DBSubnetGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeEngineDefaultClusterParametersMessageRequestTypeDef(TypedDict):
    DBParameterGroupFamily: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeEngineDefaultParametersMessageRequestTypeDef(TypedDict):
    DBParameterGroupFamily: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeEventCategoriesMessageRequestTypeDef(TypedDict):
    SourceType: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeEventSubscriptionsMessageRequestTypeDef(TypedDict):
    SubscriptionName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeEventsMessageRequestTypeDef(TypedDict):
    SourceIdentifier: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Duration: NotRequired[int]
    EventCategories: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeExportTasksMessageRequestTypeDef(TypedDict):
    ExportTaskIdentifier: NotRequired[str]
    SourceArn: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]
    SourceType: NotRequired[ExportSourceTypeType]


class DescribeGlobalClustersMessageRequestTypeDef(TypedDict):
    GlobalClusterIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeIntegrationsMessageRequestTypeDef(TypedDict):
    IntegrationIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeOptionGroupOptionsMessageRequestTypeDef(TypedDict):
    EngineName: str
    MajorEngineVersion: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeOptionGroupsMessageRequestTypeDef(TypedDict):
    OptionGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]
    EngineName: NotRequired[str]
    MajorEngineVersion: NotRequired[str]


class DescribeOrderableDBInstanceOptionsMessageRequestTypeDef(TypedDict):
    Engine: str
    EngineVersion: NotRequired[str]
    DBInstanceClass: NotRequired[str]
    LicenseModel: NotRequired[str]
    AvailabilityZoneGroup: NotRequired[str]
    Vpc: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribePendingMaintenanceActionsMessageRequestTypeDef(TypedDict):
    ResourceIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeReservedDBInstancesMessageRequestTypeDef(TypedDict):
    ReservedDBInstanceId: NotRequired[str]
    ReservedDBInstancesOfferingId: NotRequired[str]
    DBInstanceClass: NotRequired[str]
    Duration: NotRequired[str]
    ProductDescription: NotRequired[str]
    OfferingType: NotRequired[str]
    MultiAZ: NotRequired[bool]
    LeaseId: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeReservedDBInstancesOfferingsMessageRequestTypeDef(TypedDict):
    ReservedDBInstancesOfferingId: NotRequired[str]
    DBInstanceClass: NotRequired[str]
    Duration: NotRequired[str]
    ProductDescription: NotRequired[str]
    OfferingType: NotRequired[str]
    MultiAZ: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


DescribeSourceRegionsMessageRequestTypeDef = TypedDict(
    "DescribeSourceRegionsMessageRequestTypeDef",
    {
        "RegionName": NotRequired[str],
        "MaxRecords": NotRequired[int],
        "Marker": NotRequired[str],
        "Filters": NotRequired[Sequence[FilterTypeDef]],
    },
)


class DescribeTenantDatabasesMessageRequestTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    TenantDBName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class ListTagsForResourceMessageRequestTypeDef(TypedDict):
    ResourceName: str
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeBlueGreenDeploymentsRequestDescribeBlueGreenDeploymentsPaginateTypeDef(TypedDict):
    BlueGreenDeploymentIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef(TypedDict):
    CertificateIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBClusterAutomatedBackupsMessageDescribeDBClusterAutomatedBackupsPaginateTypeDef(
    TypedDict
):
    DbClusterResourceId: NotRequired[str]
    DBClusterIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBClusterBacktracksMessageDescribeDBClusterBacktracksPaginateTypeDef(TypedDict):
    DBClusterIdentifier: str
    BacktrackIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBClusterEndpointsMessageDescribeDBClusterEndpointsPaginateTypeDef(TypedDict):
    DBClusterIdentifier: NotRequired[str]
    DBClusterEndpointIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef(
    TypedDict
):
    DBClusterParameterGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef(TypedDict):
    DBClusterParameterGroupName: str
    Source: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef(TypedDict):
    DBClusterIdentifier: NotRequired[str]
    DBClusterSnapshotIdentifier: NotRequired[str]
    SnapshotType: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    IncludeShared: NotRequired[bool]
    IncludePublic: NotRequired[bool]
    DbClusterResourceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef(TypedDict):
    DBClusterIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    IncludeShared: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef(TypedDict):
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    DBParameterGroupFamily: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DefaultOnly: NotRequired[bool]
    ListSupportedCharacterSets: NotRequired[bool]
    ListSupportedTimezones: NotRequired[bool]
    IncludeAll: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBInstanceAutomatedBackupsMessageDescribeDBInstanceAutomatedBackupsPaginateTypeDef(
    TypedDict
):
    DbiResourceId: NotRequired[str]
    DBInstanceIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DBInstanceAutomatedBackupsArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBLogFilesMessageDescribeDBLogFilesPaginateTypeDef(TypedDict):
    DBInstanceIdentifier: str
    FilenameContains: NotRequired[str]
    FileLastWritten: NotRequired[int]
    FileSize: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBParameterGroupsMessageDescribeDBParameterGroupsPaginateTypeDef(TypedDict):
    DBParameterGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBParametersMessageDescribeDBParametersPaginateTypeDef(TypedDict):
    DBParameterGroupName: str
    Source: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBProxiesRequestDescribeDBProxiesPaginateTypeDef(TypedDict):
    DBProxyName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBProxyEndpointsRequestDescribeDBProxyEndpointsPaginateTypeDef(TypedDict):
    DBProxyName: NotRequired[str]
    DBProxyEndpointName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBProxyTargetGroupsRequestDescribeDBProxyTargetGroupsPaginateTypeDef(TypedDict):
    DBProxyName: str
    TargetGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBProxyTargetsRequestDescribeDBProxyTargetsPaginateTypeDef(TypedDict):
    DBProxyName: str
    TargetGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBRecommendationsMessageDescribeDBRecommendationsPaginateTypeDef(TypedDict):
    LastUpdatedAfter: NotRequired[TimestampTypeDef]
    LastUpdatedBefore: NotRequired[TimestampTypeDef]
    Locale: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBSecurityGroupsMessageDescribeDBSecurityGroupsPaginateTypeDef(TypedDict):
    DBSecurityGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBSnapshotTenantDatabasesMessageDescribeDBSnapshotTenantDatabasesPaginateTypeDef(
    TypedDict
):
    DBInstanceIdentifier: NotRequired[str]
    DBSnapshotIdentifier: NotRequired[str]
    SnapshotType: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DbiResourceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBSnapshotsMessageDescribeDBSnapshotsPaginateTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    DBSnapshotIdentifier: NotRequired[str]
    SnapshotType: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    IncludeShared: NotRequired[bool]
    IncludePublic: NotRequired[bool]
    DbiResourceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef(TypedDict):
    DBSubnetGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEngineDefaultClusterParametersMessageDescribeEngineDefaultClusterParametersPaginateTypeDef(
    TypedDict
):
    DBParameterGroupFamily: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef(
    TypedDict
):
    DBParameterGroupFamily: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef(TypedDict):
    SubscriptionName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEventsMessageDescribeEventsPaginateTypeDef(TypedDict):
    SourceIdentifier: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Duration: NotRequired[int]
    EventCategories: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeExportTasksMessageDescribeExportTasksPaginateTypeDef(TypedDict):
    ExportTaskIdentifier: NotRequired[str]
    SourceArn: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    SourceType: NotRequired[ExportSourceTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeGlobalClustersMessageDescribeGlobalClustersPaginateTypeDef(TypedDict):
    GlobalClusterIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeIntegrationsMessageDescribeIntegrationsPaginateTypeDef(TypedDict):
    IntegrationIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeOptionGroupOptionsMessageDescribeOptionGroupOptionsPaginateTypeDef(TypedDict):
    EngineName: str
    MajorEngineVersion: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeOptionGroupsMessageDescribeOptionGroupsPaginateTypeDef(TypedDict):
    OptionGroupName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    EngineName: NotRequired[str]
    MajorEngineVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef(
    TypedDict
):
    Engine: str
    EngineVersion: NotRequired[str]
    DBInstanceClass: NotRequired[str]
    LicenseModel: NotRequired[str]
    AvailabilityZoneGroup: NotRequired[str]
    Vpc: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef(
    TypedDict
):
    ResourceIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReservedDBInstancesMessageDescribeReservedDBInstancesPaginateTypeDef(TypedDict):
    ReservedDBInstanceId: NotRequired[str]
    ReservedDBInstancesOfferingId: NotRequired[str]
    DBInstanceClass: NotRequired[str]
    Duration: NotRequired[str]
    ProductDescription: NotRequired[str]
    OfferingType: NotRequired[str]
    MultiAZ: NotRequired[bool]
    LeaseId: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReservedDBInstancesOfferingsMessageDescribeReservedDBInstancesOfferingsPaginateTypeDef(
    TypedDict
):
    ReservedDBInstancesOfferingId: NotRequired[str]
    DBInstanceClass: NotRequired[str]
    Duration: NotRequired[str]
    ProductDescription: NotRequired[str]
    OfferingType: NotRequired[str]
    MultiAZ: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


DescribeSourceRegionsMessageDescribeSourceRegionsPaginateTypeDef = TypedDict(
    "DescribeSourceRegionsMessageDescribeSourceRegionsPaginateTypeDef",
    {
        "RegionName": NotRequired[str],
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class DescribeTenantDatabasesMessageDescribeTenantDatabasesPaginateTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    TenantDBName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DownloadDBLogFilePortionMessageDownloadDBLogFilePortionPaginateTypeDef(TypedDict):
    DBInstanceIdentifier: str
    LogFileName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDBClusterSnapshotsMessageDBClusterSnapshotAvailableWaitTypeDef(TypedDict):
    DBClusterIdentifier: NotRequired[str]
    DBClusterSnapshotIdentifier: NotRequired[str]
    SnapshotType: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    IncludeShared: NotRequired[bool]
    IncludePublic: NotRequired[bool]
    DbClusterResourceId: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeDBClusterSnapshotsMessageDBClusterSnapshotDeletedWaitTypeDef(TypedDict):
    DBClusterIdentifier: NotRequired[str]
    DBClusterSnapshotIdentifier: NotRequired[str]
    SnapshotType: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    IncludeShared: NotRequired[bool]
    IncludePublic: NotRequired[bool]
    DbClusterResourceId: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeDBClustersMessageDBClusterAvailableWaitTypeDef(TypedDict):
    DBClusterIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    IncludeShared: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeDBClustersMessageDBClusterDeletedWaitTypeDef(TypedDict):
    DBClusterIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    IncludeShared: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeDBSnapshotsMessageDBSnapshotAvailableWaitTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    DBSnapshotIdentifier: NotRequired[str]
    SnapshotType: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    IncludeShared: NotRequired[bool]
    IncludePublic: NotRequired[bool]
    DbiResourceId: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeDBSnapshotsMessageDBSnapshotCompletedWaitTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    DBSnapshotIdentifier: NotRequired[str]
    SnapshotType: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    IncludeShared: NotRequired[bool]
    IncludePublic: NotRequired[bool]
    DbiResourceId: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeDBSnapshotsMessageDBSnapshotDeletedWaitTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    DBSnapshotIdentifier: NotRequired[str]
    SnapshotType: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    IncludeShared: NotRequired[bool]
    IncludePublic: NotRequired[bool]
    DbiResourceId: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeTenantDatabasesMessageTenantDatabaseAvailableWaitTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    TenantDBName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeTenantDatabasesMessageTenantDatabaseDeletedWaitTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    TenantDBName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeDBLogFilesResponseTypeDef(TypedDict):
    DescribeDBLogFiles: List[DescribeDBLogFilesDetailsTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class EventCategoriesMessageTypeDef(TypedDict):
    EventCategoriesMapList: List[EventCategoriesMapTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class EventsMessageTypeDef(TypedDict):
    Marker: str
    Events: List[EventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ExportTasksMessageTypeDef(TypedDict):
    Marker: str
    ExportTasks: List[ExportTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GlobalClusterTypeDef(TypedDict):
    GlobalClusterIdentifier: NotRequired[str]
    GlobalClusterResourceId: NotRequired[str]
    GlobalClusterArn: NotRequired[str]
    Status: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    EngineLifecycleSupport: NotRequired[str]
    DatabaseName: NotRequired[str]
    StorageEncrypted: NotRequired[bool]
    DeletionProtection: NotRequired[bool]
    GlobalClusterMembers: NotRequired[List[GlobalClusterMemberTypeDef]]
    Endpoint: NotRequired[str]
    FailoverState: NotRequired[FailoverStateTypeDef]
    TagList: NotRequired[List[TagTypeDef]]


class IntegrationResponseTypeDef(TypedDict):
    SourceArn: str
    TargetArn: str
    IntegrationName: str
    IntegrationArn: str
    KMSKeyId: str
    AdditionalEncryptionContext: Dict[str, str]
    Status: IntegrationStatusType
    Tags: List[TagTypeDef]
    CreateTime: datetime
    Errors: List[IntegrationErrorTypeDef]
    DataFilter: str
    Description: str
    ResponseMetadata: ResponseMetadataTypeDef


class IntegrationTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    TargetArn: NotRequired[str]
    IntegrationName: NotRequired[str]
    IntegrationArn: NotRequired[str]
    KMSKeyId: NotRequired[str]
    AdditionalEncryptionContext: NotRequired[Dict[str, str]]
    Status: NotRequired[IntegrationStatusType]
    Tags: NotRequired[List[TagTypeDef]]
    CreateTime: NotRequired[datetime]
    Errors: NotRequired[List[IntegrationErrorTypeDef]]
    DataFilter: NotRequired[str]
    Description: NotRequired[str]


class OptionGroupOptionSettingTypeDef(TypedDict):
    SettingName: NotRequired[str]
    SettingDescription: NotRequired[str]
    DefaultValue: NotRequired[str]
    ApplyType: NotRequired[str]
    AllowedValues: NotRequired[str]
    IsModifiable: NotRequired[bool]
    IsRequired: NotRequired[bool]
    MinimumEngineVersionPerAllowedValue: NotRequired[
        List[MinimumEngineVersionPerAllowedValueTypeDef]
    ]


class ModifyDBParameterGroupMessageRequestTypeDef(TypedDict):
    DBParameterGroupName: str
    Parameters: Sequence[ParameterTypeDef]


ParameterUnionTypeDef = Union[ParameterTypeDef, ParameterOutputTypeDef]


class ResetDBClusterParameterGroupMessageRequestTypeDef(TypedDict):
    DBClusterParameterGroupName: str
    ResetAllParameters: NotRequired[bool]
    Parameters: NotRequired[Sequence[ParameterTypeDef]]


class ResetDBParameterGroupMessageRequestTypeDef(TypedDict):
    DBParameterGroupName: str
    ResetAllParameters: NotRequired[bool]
    Parameters: NotRequired[Sequence[ParameterTypeDef]]


class ModifyDBRecommendationMessageRequestTypeDef(TypedDict):
    RecommendationId: str
    Locale: NotRequired[str]
    Status: NotRequired[str]
    RecommendedActionUpdates: NotRequired[Sequence[RecommendedActionUpdateTypeDef]]


class OptionConfigurationTypeDef(TypedDict):
    OptionName: str
    Port: NotRequired[int]
    OptionVersion: NotRequired[str]
    DBSecurityGroupMemberships: NotRequired[Sequence[str]]
    VpcSecurityGroupMemberships: NotRequired[Sequence[str]]
    OptionSettings: NotRequired[Sequence[OptionSettingTypeDef]]


class OptionTypeDef(TypedDict):
    OptionName: NotRequired[str]
    OptionDescription: NotRequired[str]
    Persistent: NotRequired[bool]
    Permanent: NotRequired[bool]
    Port: NotRequired[int]
    OptionVersion: NotRequired[str]
    OptionSettings: NotRequired[List[OptionSettingTypeDef]]
    DBSecurityGroupMemberships: NotRequired[List[DBSecurityGroupMembershipTypeDef]]
    VpcSecurityGroupMemberships: NotRequired[List[VpcSecurityGroupMembershipTypeDef]]


class SubnetTypeDef(TypedDict):
    SubnetIdentifier: NotRequired[str]
    SubnetAvailabilityZone: NotRequired[AvailabilityZoneTypeDef]
    SubnetOutpost: NotRequired[OutpostTypeDef]
    SubnetStatus: NotRequired[str]


class ResourcePendingMaintenanceActionsTypeDef(TypedDict):
    ResourceIdentifier: NotRequired[str]
    PendingMaintenanceActionDetails: NotRequired[List[PendingMaintenanceActionTypeDef]]


class PerformanceInsightsMetricQueryTypeDef(TypedDict):
    GroupBy: NotRequired[PerformanceInsightsMetricDimensionGroupTypeDef]
    Metric: NotRequired[str]


class ValidStorageOptionsTypeDef(TypedDict):
    StorageType: NotRequired[str]
    StorageSize: NotRequired[List[RangeTypeDef]]
    ProvisionedIops: NotRequired[List[RangeTypeDef]]
    IopsToStorageRatio: NotRequired[List[DoubleRangeTypeDef]]
    SupportsStorageAutoscaling: NotRequired[bool]
    ProvisionedStorageThroughput: NotRequired[List[RangeTypeDef]]
    StorageThroughputToIopsRatio: NotRequired[List[DoubleRangeTypeDef]]


class ReservedDBInstanceTypeDef(TypedDict):
    ReservedDBInstanceId: NotRequired[str]
    ReservedDBInstancesOfferingId: NotRequired[str]
    DBInstanceClass: NotRequired[str]
    StartTime: NotRequired[datetime]
    Duration: NotRequired[int]
    FixedPrice: NotRequired[float]
    UsagePrice: NotRequired[float]
    CurrencyCode: NotRequired[str]
    DBInstanceCount: NotRequired[int]
    ProductDescription: NotRequired[str]
    OfferingType: NotRequired[str]
    MultiAZ: NotRequired[bool]
    State: NotRequired[str]
    RecurringCharges: NotRequired[List[RecurringChargeTypeDef]]
    ReservedDBInstanceArn: NotRequired[str]
    LeaseId: NotRequired[str]


class ReservedDBInstancesOfferingTypeDef(TypedDict):
    ReservedDBInstancesOfferingId: NotRequired[str]
    DBInstanceClass: NotRequired[str]
    Duration: NotRequired[int]
    FixedPrice: NotRequired[float]
    UsagePrice: NotRequired[float]
    CurrencyCode: NotRequired[str]
    ProductDescription: NotRequired[str]
    OfferingType: NotRequired[str]
    MultiAZ: NotRequired[bool]
    RecurringCharges: NotRequired[List[RecurringChargeTypeDef]]


class ReferenceDetailsTypeDef(TypedDict):
    ScalarReferenceDetails: NotRequired[ScalarReferenceDetailsTypeDef]


class SourceRegionMessageTypeDef(TypedDict):
    Marker: str
    SourceRegions: List[SourceRegionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TenantDatabaseTypeDef(TypedDict):
    TenantDatabaseCreateTime: NotRequired[datetime]
    DBInstanceIdentifier: NotRequired[str]
    TenantDBName: NotRequired[str]
    Status: NotRequired[str]
    MasterUsername: NotRequired[str]
    DbiResourceId: NotRequired[str]
    TenantDatabaseResourceId: NotRequired[str]
    TenantDatabaseARN: NotRequired[str]
    CharacterSetName: NotRequired[str]
    NcharCharacterSetName: NotRequired[str]
    DeletionProtection: NotRequired[bool]
    PendingModifiedValues: NotRequired[TenantDatabasePendingModifiedValuesTypeDef]
    TagList: NotRequired[List[TagTypeDef]]


class CopyDBClusterSnapshotResultTypeDef(TypedDict):
    DBClusterSnapshot: DBClusterSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDBClusterSnapshotResultTypeDef(TypedDict):
    DBClusterSnapshot: DBClusterSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DBClusterSnapshotMessageTypeDef(TypedDict):
    Marker: str
    DBClusterSnapshots: List[DBClusterSnapshotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDBClusterSnapshotResultTypeDef(TypedDict):
    DBClusterSnapshot: DBClusterSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDBShardGroupsResponseTypeDef(TypedDict):
    DBShardGroups: List[DBShardGroupTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DBSnapshotTenantDatabasesMessageTypeDef(TypedDict):
    Marker: str
    DBSnapshotTenantDatabases: List[DBSnapshotTenantDatabaseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class OrderableDBInstanceOptionsMessageTypeDef(TypedDict):
    OrderableDBInstanceOptions: List[OrderableDBInstanceOptionTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBlueGreenDeploymentResponseTypeDef(TypedDict):
    BlueGreenDeployment: BlueGreenDeploymentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBlueGreenDeploymentResponseTypeDef(TypedDict):
    BlueGreenDeployment: BlueGreenDeploymentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBlueGreenDeploymentsResponseTypeDef(TypedDict):
    BlueGreenDeployments: List[BlueGreenDeploymentTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class SwitchoverBlueGreenDeploymentResponseTypeDef(TypedDict):
    BlueGreenDeployment: BlueGreenDeploymentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DBClusterTypeDef(TypedDict):
    AllocatedStorage: NotRequired[int]
    AvailabilityZones: NotRequired[List[str]]
    BackupRetentionPeriod: NotRequired[int]
    CharacterSetName: NotRequired[str]
    DatabaseName: NotRequired[str]
    DBClusterIdentifier: NotRequired[str]
    DBClusterParameterGroup: NotRequired[str]
    DBSubnetGroup: NotRequired[str]
    Status: NotRequired[str]
    AutomaticRestartTime: NotRequired[datetime]
    PercentProgress: NotRequired[str]
    EarliestRestorableTime: NotRequired[datetime]
    Endpoint: NotRequired[str]
    ReaderEndpoint: NotRequired[str]
    CustomEndpoints: NotRequired[List[str]]
    MultiAZ: NotRequired[bool]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    LatestRestorableTime: NotRequired[datetime]
    Port: NotRequired[int]
    MasterUsername: NotRequired[str]
    DBClusterOptionGroupMemberships: NotRequired[List[DBClusterOptionGroupStatusTypeDef]]
    PreferredBackupWindow: NotRequired[str]
    PreferredMaintenanceWindow: NotRequired[str]
    ReplicationSourceIdentifier: NotRequired[str]
    ReadReplicaIdentifiers: NotRequired[List[str]]
    StatusInfos: NotRequired[List[DBClusterStatusInfoTypeDef]]
    DBClusterMembers: NotRequired[List[DBClusterMemberTypeDef]]
    VpcSecurityGroups: NotRequired[List[VpcSecurityGroupMembershipTypeDef]]
    HostedZoneId: NotRequired[str]
    StorageEncrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    DbClusterResourceId: NotRequired[str]
    DBClusterArn: NotRequired[str]
    AssociatedRoles: NotRequired[List[DBClusterRoleTypeDef]]
    IAMDatabaseAuthenticationEnabled: NotRequired[bool]
    CloneGroupId: NotRequired[str]
    ClusterCreateTime: NotRequired[datetime]
    EarliestBacktrackTime: NotRequired[datetime]
    BacktrackWindow: NotRequired[int]
    BacktrackConsumedChangeRecords: NotRequired[int]
    EnabledCloudwatchLogsExports: NotRequired[List[str]]
    Capacity: NotRequired[int]
    EngineMode: NotRequired[str]
    ScalingConfigurationInfo: NotRequired[ScalingConfigurationInfoTypeDef]
    RdsCustomClusterConfiguration: NotRequired[RdsCustomClusterConfigurationTypeDef]
    DeletionProtection: NotRequired[bool]
    HttpEndpointEnabled: NotRequired[bool]
    ActivityStreamMode: NotRequired[ActivityStreamModeType]
    ActivityStreamStatus: NotRequired[ActivityStreamStatusType]
    ActivityStreamKmsKeyId: NotRequired[str]
    ActivityStreamKinesisStreamName: NotRequired[str]
    CopyTagsToSnapshot: NotRequired[bool]
    CrossAccountClone: NotRequired[bool]
    DomainMemberships: NotRequired[List[DomainMembershipTypeDef]]
    TagList: NotRequired[List[TagTypeDef]]
    GlobalWriteForwardingStatus: NotRequired[WriteForwardingStatusType]
    GlobalWriteForwardingRequested: NotRequired[bool]
    PendingModifiedValues: NotRequired[ClusterPendingModifiedValuesTypeDef]
    DBClusterInstanceClass: NotRequired[str]
    StorageType: NotRequired[str]
    Iops: NotRequired[int]
    PubliclyAccessible: NotRequired[bool]
    AutoMinorVersionUpgrade: NotRequired[bool]
    MonitoringInterval: NotRequired[int]
    MonitoringRoleArn: NotRequired[str]
    DatabaseInsightsMode: NotRequired[DatabaseInsightsModeType]
    PerformanceInsightsEnabled: NotRequired[bool]
    PerformanceInsightsKMSKeyId: NotRequired[str]
    PerformanceInsightsRetentionPeriod: NotRequired[int]
    ServerlessV2ScalingConfiguration: NotRequired[ServerlessV2ScalingConfigurationInfoTypeDef]
    NetworkType: NotRequired[str]
    DBSystemId: NotRequired[str]
    MasterUserSecret: NotRequired[MasterUserSecretTypeDef]
    IOOptimizedNextAllowedModificationTime: NotRequired[datetime]
    LocalWriteForwardingStatus: NotRequired[LocalWriteForwardingStatusType]
    AwsBackupRecoveryPointArn: NotRequired[str]
    LimitlessDatabase: NotRequired[LimitlessDatabaseTypeDef]
    StorageThroughput: NotRequired[int]
    ClusterScalabilityType: NotRequired[ClusterScalabilityTypeType]
    CertificateDetails: NotRequired[CertificateDetailsTypeDef]
    EngineLifecycleSupport: NotRequired[str]


class DescribeDBProxyTargetGroupsResponseTypeDef(TypedDict):
    TargetGroups: List[DBProxyTargetGroupTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyDBProxyTargetGroupResponseTypeDef(TypedDict):
    DBProxyTargetGroup: DBProxyTargetGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CopyDBSnapshotResultTypeDef(TypedDict):
    DBSnapshot: DBSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDBSnapshotResultTypeDef(TypedDict):
    DBSnapshot: DBSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DBSnapshotMessageTypeDef(TypedDict):
    Marker: str
    DBSnapshots: List[DBSnapshotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDBSnapshotResultTypeDef(TypedDict):
    DBSnapshot: DBSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyDBSnapshotResultTypeDef(TypedDict):
    DBSnapshot: DBSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DBClusterAutomatedBackupMessageTypeDef(TypedDict):
    Marker: str
    DBClusterAutomatedBackups: List[DBClusterAutomatedBackupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDBClusterAutomatedBackupResultTypeDef(TypedDict):
    DBClusterAutomatedBackup: DBClusterAutomatedBackupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEngineDefaultClusterParametersResultTypeDef(TypedDict):
    EngineDefaults: EngineDefaultsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEngineDefaultParametersResultTypeDef(TypedDict):
    EngineDefaults: EngineDefaultsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDBClusterSnapshotAttributesResultTypeDef(TypedDict):
    DBClusterSnapshotAttributesResult: DBClusterSnapshotAttributesResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyDBClusterSnapshotAttributeResultTypeDef(TypedDict):
    DBClusterSnapshotAttributesResult: DBClusterSnapshotAttributesResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DBEngineVersionMessageTypeDef(TypedDict):
    Marker: str
    DBEngineVersions: List[DBEngineVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DBInstanceAutomatedBackupMessageTypeDef(TypedDict):
    Marker: str
    DBInstanceAutomatedBackups: List[DBInstanceAutomatedBackupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDBInstanceAutomatedBackupResultTypeDef(TypedDict):
    DBInstanceAutomatedBackup: DBInstanceAutomatedBackupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartDBInstanceAutomatedBackupsReplicationResultTypeDef(TypedDict):
    DBInstanceAutomatedBackup: DBInstanceAutomatedBackupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StopDBInstanceAutomatedBackupsReplicationResultTypeDef(TypedDict):
    DBInstanceAutomatedBackup: DBInstanceAutomatedBackupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDBProxyTargetsResponseTypeDef(TypedDict):
    Targets: List[DBProxyTargetTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterDBProxyTargetsResponseTypeDef(TypedDict):
    DBProxyTargets: List[DBProxyTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDBProxyResponseTypeDef(TypedDict):
    DBProxy: DBProxyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDBProxyResponseTypeDef(TypedDict):
    DBProxy: DBProxyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDBProxiesResponseTypeDef(TypedDict):
    DBProxies: List[DBProxyTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyDBProxyResponseTypeDef(TypedDict):
    DBProxy: DBProxyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AuthorizeDBSecurityGroupIngressResultTypeDef(TypedDict):
    DBSecurityGroup: DBSecurityGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDBSecurityGroupResultTypeDef(TypedDict):
    DBSecurityGroup: DBSecurityGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DBSecurityGroupMessageTypeDef(TypedDict):
    Marker: str
    DBSecurityGroups: List[DBSecurityGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RevokeDBSecurityGroupIngressResultTypeDef(TypedDict):
    DBSecurityGroup: DBSecurityGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDBSnapshotAttributesResultTypeDef(TypedDict):
    DBSnapshotAttributesResult: DBSnapshotAttributesResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyDBSnapshotAttributeResultTypeDef(TypedDict):
    DBSnapshotAttributesResult: DBSnapshotAttributesResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateGlobalClusterResultTypeDef(TypedDict):
    GlobalCluster: GlobalClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteGlobalClusterResultTypeDef(TypedDict):
    GlobalCluster: GlobalClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class FailoverGlobalClusterResultTypeDef(TypedDict):
    GlobalCluster: GlobalClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GlobalClustersMessageTypeDef(TypedDict):
    Marker: str
    GlobalClusters: List[GlobalClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyGlobalClusterResultTypeDef(TypedDict):
    GlobalCluster: GlobalClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RemoveFromGlobalClusterResultTypeDef(TypedDict):
    GlobalCluster: GlobalClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SwitchoverGlobalClusterResultTypeDef(TypedDict):
    GlobalCluster: GlobalClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIntegrationsResponseTypeDef(TypedDict):
    Marker: str
    Integrations: List[IntegrationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class OptionGroupOptionTypeDef(TypedDict):
    Name: NotRequired[str]
    Description: NotRequired[str]
    EngineName: NotRequired[str]
    MajorEngineVersion: NotRequired[str]
    MinimumRequiredMinorEngineVersion: NotRequired[str]
    PortRequired: NotRequired[bool]
    DefaultPort: NotRequired[int]
    OptionsDependedOn: NotRequired[List[str]]
    OptionsConflictsWith: NotRequired[List[str]]
    Persistent: NotRequired[bool]
    Permanent: NotRequired[bool]
    RequiresAutoMinorEngineVersionUpgrade: NotRequired[bool]
    VpcOnly: NotRequired[bool]
    SupportsOptionVersionDowngrade: NotRequired[bool]
    OptionGroupOptionSettings: NotRequired[List[OptionGroupOptionSettingTypeDef]]
    OptionGroupOptionVersions: NotRequired[List[OptionVersionTypeDef]]
    CopyableCrossAccount: NotRequired[bool]


class ModifyDBClusterParameterGroupMessageRequestTypeDef(TypedDict):
    DBClusterParameterGroupName: str
    Parameters: Sequence[ParameterUnionTypeDef]


class ModifyOptionGroupMessageRequestTypeDef(TypedDict):
    OptionGroupName: str
    OptionsToInclude: NotRequired[Sequence[OptionConfigurationTypeDef]]
    OptionsToRemove: NotRequired[Sequence[str]]
    ApplyImmediately: NotRequired[bool]


class OptionGroupTypeDef(TypedDict):
    OptionGroupName: NotRequired[str]
    OptionGroupDescription: NotRequired[str]
    EngineName: NotRequired[str]
    MajorEngineVersion: NotRequired[str]
    Options: NotRequired[List[OptionTypeDef]]
    AllowsVpcAndNonVpcInstanceMemberships: NotRequired[bool]
    VpcId: NotRequired[str]
    OptionGroupArn: NotRequired[str]
    SourceOptionGroup: NotRequired[str]
    SourceAccountId: NotRequired[str]
    CopyTimestamp: NotRequired[datetime]


class DBSubnetGroupTypeDef(TypedDict):
    DBSubnetGroupName: NotRequired[str]
    DBSubnetGroupDescription: NotRequired[str]
    VpcId: NotRequired[str]
    SubnetGroupStatus: NotRequired[str]
    Subnets: NotRequired[List[SubnetTypeDef]]
    DBSubnetGroupArn: NotRequired[str]
    SupportedNetworkTypes: NotRequired[List[str]]


class ApplyPendingMaintenanceActionResultTypeDef(TypedDict):
    ResourcePendingMaintenanceActions: ResourcePendingMaintenanceActionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PendingMaintenanceActionsMessageTypeDef(TypedDict):
    PendingMaintenanceActions: List[ResourcePendingMaintenanceActionsTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class MetricQueryTypeDef(TypedDict):
    PerformanceInsightsMetricQuery: NotRequired[PerformanceInsightsMetricQueryTypeDef]


class ValidDBInstanceModificationsMessageTypeDef(TypedDict):
    Storage: NotRequired[List[ValidStorageOptionsTypeDef]]
    ValidProcessorFeatures: NotRequired[List[AvailableProcessorFeatureTypeDef]]
    SupportsDedicatedLogVolume: NotRequired[bool]


class PurchaseReservedDBInstancesOfferingResultTypeDef(TypedDict):
    ReservedDBInstance: ReservedDBInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ReservedDBInstanceMessageTypeDef(TypedDict):
    Marker: str
    ReservedDBInstances: List[ReservedDBInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ReservedDBInstancesOfferingMessageTypeDef(TypedDict):
    Marker: str
    ReservedDBInstancesOfferings: List[ReservedDBInstancesOfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class MetricReferenceTypeDef(TypedDict):
    Name: NotRequired[str]
    ReferenceDetails: NotRequired[ReferenceDetailsTypeDef]


class CreateTenantDatabaseResultTypeDef(TypedDict):
    TenantDatabase: TenantDatabaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTenantDatabaseResultTypeDef(TypedDict):
    TenantDatabase: TenantDatabaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyTenantDatabaseResultTypeDef(TypedDict):
    TenantDatabase: TenantDatabaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TenantDatabasesMessageTypeDef(TypedDict):
    Marker: str
    TenantDatabases: List[TenantDatabaseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDBClusterResultTypeDef(TypedDict):
    DBCluster: DBClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DBClusterMessageTypeDef(TypedDict):
    Marker: str
    DBClusters: List[DBClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDBClusterResultTypeDef(TypedDict):
    DBCluster: DBClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class FailoverDBClusterResultTypeDef(TypedDict):
    DBCluster: DBClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyDBClusterResultTypeDef(TypedDict):
    DBCluster: DBClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PromoteReadReplicaDBClusterResultTypeDef(TypedDict):
    DBCluster: DBClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RebootDBClusterResultTypeDef(TypedDict):
    DBCluster: DBClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreDBClusterFromS3ResultTypeDef(TypedDict):
    DBCluster: DBClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreDBClusterFromSnapshotResultTypeDef(TypedDict):
    DBCluster: DBClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreDBClusterToPointInTimeResultTypeDef(TypedDict):
    DBCluster: DBClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartDBClusterResultTypeDef(TypedDict):
    DBCluster: DBClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StopDBClusterResultTypeDef(TypedDict):
    DBCluster: DBClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class OptionGroupOptionsMessageTypeDef(TypedDict):
    OptionGroupOptions: List[OptionGroupOptionTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class CopyOptionGroupResultTypeDef(TypedDict):
    OptionGroup: OptionGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOptionGroupResultTypeDef(TypedDict):
    OptionGroup: OptionGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyOptionGroupResultTypeDef(TypedDict):
    OptionGroup: OptionGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class OptionGroupsTypeDef(TypedDict):
    OptionGroupsList: List[OptionGroupTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDBSubnetGroupResultTypeDef(TypedDict):
    DBSubnetGroup: DBSubnetGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DBInstanceTypeDef(TypedDict):
    DBInstanceIdentifier: NotRequired[str]
    DBInstanceClass: NotRequired[str]
    Engine: NotRequired[str]
    DBInstanceStatus: NotRequired[str]
    AutomaticRestartTime: NotRequired[datetime]
    MasterUsername: NotRequired[str]
    DBName: NotRequired[str]
    Endpoint: NotRequired[EndpointTypeDef]
    AllocatedStorage: NotRequired[int]
    InstanceCreateTime: NotRequired[datetime]
    PreferredBackupWindow: NotRequired[str]
    BackupRetentionPeriod: NotRequired[int]
    DBSecurityGroups: NotRequired[List[DBSecurityGroupMembershipTypeDef]]
    VpcSecurityGroups: NotRequired[List[VpcSecurityGroupMembershipTypeDef]]
    DBParameterGroups: NotRequired[List[DBParameterGroupStatusTypeDef]]
    AvailabilityZone: NotRequired[str]
    DBSubnetGroup: NotRequired[DBSubnetGroupTypeDef]
    PreferredMaintenanceWindow: NotRequired[str]
    PendingModifiedValues: NotRequired[PendingModifiedValuesTypeDef]
    LatestRestorableTime: NotRequired[datetime]
    MultiAZ: NotRequired[bool]
    EngineVersion: NotRequired[str]
    AutoMinorVersionUpgrade: NotRequired[bool]
    ReadReplicaSourceDBInstanceIdentifier: NotRequired[str]
    ReadReplicaDBInstanceIdentifiers: NotRequired[List[str]]
    ReadReplicaDBClusterIdentifiers: NotRequired[List[str]]
    ReplicaMode: NotRequired[ReplicaModeType]
    LicenseModel: NotRequired[str]
    Iops: NotRequired[int]
    OptionGroupMemberships: NotRequired[List[OptionGroupMembershipTypeDef]]
    CharacterSetName: NotRequired[str]
    NcharCharacterSetName: NotRequired[str]
    SecondaryAvailabilityZone: NotRequired[str]
    PubliclyAccessible: NotRequired[bool]
    StatusInfos: NotRequired[List[DBInstanceStatusInfoTypeDef]]
    StorageType: NotRequired[str]
    TdeCredentialArn: NotRequired[str]
    DbInstancePort: NotRequired[int]
    DBClusterIdentifier: NotRequired[str]
    StorageEncrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    DbiResourceId: NotRequired[str]
    CACertificateIdentifier: NotRequired[str]
    DomainMemberships: NotRequired[List[DomainMembershipTypeDef]]
    CopyTagsToSnapshot: NotRequired[bool]
    MonitoringInterval: NotRequired[int]
    EnhancedMonitoringResourceArn: NotRequired[str]
    MonitoringRoleArn: NotRequired[str]
    PromotionTier: NotRequired[int]
    DBInstanceArn: NotRequired[str]
    Timezone: NotRequired[str]
    IAMDatabaseAuthenticationEnabled: NotRequired[bool]
    DatabaseInsightsMode: NotRequired[DatabaseInsightsModeType]
    PerformanceInsightsEnabled: NotRequired[bool]
    PerformanceInsightsKMSKeyId: NotRequired[str]
    PerformanceInsightsRetentionPeriod: NotRequired[int]
    EnabledCloudwatchLogsExports: NotRequired[List[str]]
    ProcessorFeatures: NotRequired[List[ProcessorFeatureTypeDef]]
    DeletionProtection: NotRequired[bool]
    AssociatedRoles: NotRequired[List[DBInstanceRoleTypeDef]]
    ListenerEndpoint: NotRequired[EndpointTypeDef]
    MaxAllocatedStorage: NotRequired[int]
    TagList: NotRequired[List[TagTypeDef]]
    DBInstanceAutomatedBackupsReplications: NotRequired[
        List[DBInstanceAutomatedBackupsReplicationTypeDef]
    ]
    CustomerOwnedIpEnabled: NotRequired[bool]
    AwsBackupRecoveryPointArn: NotRequired[str]
    ActivityStreamStatus: NotRequired[ActivityStreamStatusType]
    ActivityStreamKmsKeyId: NotRequired[str]
    ActivityStreamKinesisStreamName: NotRequired[str]
    ActivityStreamMode: NotRequired[ActivityStreamModeType]
    ActivityStreamEngineNativeAuditFieldsIncluded: NotRequired[bool]
    AutomationMode: NotRequired[AutomationModeType]
    ResumeFullAutomationModeTime: NotRequired[datetime]
    CustomIamInstanceProfile: NotRequired[str]
    BackupTarget: NotRequired[str]
    NetworkType: NotRequired[str]
    ActivityStreamPolicyStatus: NotRequired[ActivityStreamPolicyStatusType]
    StorageThroughput: NotRequired[int]
    DBSystemId: NotRequired[str]
    MasterUserSecret: NotRequired[MasterUserSecretTypeDef]
    CertificateDetails: NotRequired[CertificateDetailsTypeDef]
    ReadReplicaSourceDBClusterIdentifier: NotRequired[str]
    PercentProgress: NotRequired[str]
    DedicatedLogVolume: NotRequired[bool]
    IsStorageConfigUpgradeAvailable: NotRequired[bool]
    MultiTenant: NotRequired[bool]
    EngineLifecycleSupport: NotRequired[str]


class DBSubnetGroupMessageTypeDef(TypedDict):
    Marker: str
    DBSubnetGroups: List[DBSubnetGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyDBSubnetGroupResultTypeDef(TypedDict):
    DBSubnetGroup: DBSubnetGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeValidDBInstanceModificationsResultTypeDef(TypedDict):
    ValidDBInstanceModificationsMessage: ValidDBInstanceModificationsMessageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class MetricTypeDef(TypedDict):
    Name: NotRequired[str]
    References: NotRequired[List[MetricReferenceTypeDef]]
    StatisticsDetails: NotRequired[str]
    MetricQuery: NotRequired[MetricQueryTypeDef]


class CreateDBInstanceReadReplicaResultTypeDef(TypedDict):
    DBInstance: DBInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDBInstanceResultTypeDef(TypedDict):
    DBInstance: DBInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DBInstanceMessageTypeDef(TypedDict):
    Marker: str
    DBInstances: List[DBInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDBInstanceResultTypeDef(TypedDict):
    DBInstance: DBInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyDBInstanceResultTypeDef(TypedDict):
    DBInstance: DBInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PromoteReadReplicaResultTypeDef(TypedDict):
    DBInstance: DBInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RebootDBInstanceResultTypeDef(TypedDict):
    DBInstance: DBInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreDBInstanceFromDBSnapshotResultTypeDef(TypedDict):
    DBInstance: DBInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreDBInstanceFromS3ResultTypeDef(TypedDict):
    DBInstance: DBInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreDBInstanceToPointInTimeResultTypeDef(TypedDict):
    DBInstance: DBInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartDBInstanceResultTypeDef(TypedDict):
    DBInstance: DBInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StopDBInstanceResultTypeDef(TypedDict):
    DBInstance: DBInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SwitchoverReadReplicaResultTypeDef(TypedDict):
    DBInstance: DBInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PerformanceIssueDetailsTypeDef(TypedDict):
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    Metrics: NotRequired[List[MetricTypeDef]]
    Analysis: NotRequired[str]


class IssueDetailsTypeDef(TypedDict):
    PerformanceIssueDetails: NotRequired[PerformanceIssueDetailsTypeDef]


class RecommendedActionTypeDef(TypedDict):
    ActionId: NotRequired[str]
    Title: NotRequired[str]
    Description: NotRequired[str]
    Operation: NotRequired[str]
    Parameters: NotRequired[List[RecommendedActionParameterTypeDef]]
    ApplyModes: NotRequired[List[str]]
    Status: NotRequired[str]
    IssueDetails: NotRequired[IssueDetailsTypeDef]
    ContextAttributes: NotRequired[List[ContextAttributeTypeDef]]


class DBRecommendationTypeDef(TypedDict):
    RecommendationId: NotRequired[str]
    TypeId: NotRequired[str]
    Severity: NotRequired[str]
    ResourceArn: NotRequired[str]
    Status: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    UpdatedTime: NotRequired[datetime]
    Detection: NotRequired[str]
    Recommendation: NotRequired[str]
    Description: NotRequired[str]
    Reason: NotRequired[str]
    RecommendedActions: NotRequired[List[RecommendedActionTypeDef]]
    Category: NotRequired[str]
    Source: NotRequired[str]
    TypeDetection: NotRequired[str]
    TypeRecommendation: NotRequired[str]
    Impact: NotRequired[str]
    AdditionalInfo: NotRequired[str]
    Links: NotRequired[List[DocLinkTypeDef]]
    IssueDetails: NotRequired[IssueDetailsTypeDef]


class DBRecommendationMessageTypeDef(TypedDict):
    DBRecommendation: DBRecommendationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DBRecommendationsMessageTypeDef(TypedDict):
    DBRecommendations: List[DBRecommendationTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef
