"""
Type annotations for dynamodb service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dynamodb/type_defs/)

Usage::

    ```python
    from types_boto3_dynamodb.type_defs import ArchivalSummaryTypeDef

    data: ArchivalSummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Mapping, Sequence, Set, Union

from boto3.dynamodb.conditions import ConditionBase

from .literals import (
    ApproximateCreationDateTimePrecisionType,
    AttributeActionType,
    BackupStatusType,
    BackupTypeFilterType,
    BackupTypeType,
    BatchStatementErrorCodeEnumType,
    BillingModeType,
    ComparisonOperatorType,
    ConditionalOperatorType,
    ContinuousBackupsStatusType,
    ContributorInsightsActionType,
    ContributorInsightsStatusType,
    DestinationStatusType,
    ExportFormatType,
    ExportStatusType,
    ExportTypeType,
    ExportViewTypeType,
    GlobalTableStatusType,
    ImportStatusType,
    IndexStatusType,
    InputCompressionTypeType,
    InputFormatType,
    KeyTypeType,
    MultiRegionConsistencyType,
    PointInTimeRecoveryStatusType,
    ProjectionTypeType,
    ReplicaStatusType,
    ReturnConsumedCapacityType,
    ReturnItemCollectionMetricsType,
    ReturnValuesOnConditionCheckFailureType,
    ReturnValueType,
    S3SseAlgorithmType,
    ScalarAttributeTypeType,
    SelectType,
    SSEStatusType,
    SSETypeType,
    StreamViewTypeType,
    TableClassType,
    TableStatusType,
    TimeToLiveStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ArchivalSummaryTypeDef",
    "AttributeDefinitionTypeDef",
    "AttributeValueTypeDef",
    "AttributeValueUpdateTableTypeDef",
    "AttributeValueUpdateTypeDef",
    "AutoScalingPolicyDescriptionTypeDef",
    "AutoScalingPolicyUpdateTypeDef",
    "AutoScalingSettingsDescriptionTypeDef",
    "AutoScalingSettingsUpdateTypeDef",
    "AutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef",
    "AutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef",
    "BackupDescriptionTypeDef",
    "BackupDetailsTypeDef",
    "BackupSummaryTypeDef",
    "BatchExecuteStatementInputRequestTypeDef",
    "BatchExecuteStatementOutputTypeDef",
    "BatchGetItemInputRequestTypeDef",
    "BatchGetItemInputServiceResourceBatchGetItemTypeDef",
    "BatchGetItemOutputServiceResourceTypeDef",
    "BatchGetItemOutputTypeDef",
    "BatchStatementErrorTypeDef",
    "BatchStatementRequestTypeDef",
    "BatchStatementResponseTypeDef",
    "BatchWriteItemInputRequestTypeDef",
    "BatchWriteItemInputServiceResourceBatchWriteItemTypeDef",
    "BatchWriteItemOutputServiceResourceTypeDef",
    "BatchWriteItemOutputTypeDef",
    "BillingModeSummaryTypeDef",
    "CapacityTypeDef",
    "ConditionBaseImportTypeDef",
    "ConditionCheckTypeDef",
    "ConditionTableTypeDef",
    "ConditionTypeDef",
    "ConsumedCapacityTypeDef",
    "ContinuousBackupsDescriptionTypeDef",
    "ContributorInsightsSummaryTypeDef",
    "CreateBackupInputRequestTypeDef",
    "CreateBackupOutputTypeDef",
    "CreateGlobalSecondaryIndexActionTypeDef",
    "CreateGlobalTableInputRequestTypeDef",
    "CreateGlobalTableOutputTypeDef",
    "CreateReplicaActionTypeDef",
    "CreateReplicationGroupMemberActionTypeDef",
    "CreateTableInputRequestTypeDef",
    "CreateTableInputServiceResourceCreateTableTypeDef",
    "CreateTableOutputTypeDef",
    "CsvOptionsOutputTypeDef",
    "CsvOptionsTypeDef",
    "CsvOptionsUnionTypeDef",
    "DeleteBackupInputRequestTypeDef",
    "DeleteBackupOutputTypeDef",
    "DeleteGlobalSecondaryIndexActionTypeDef",
    "DeleteItemInputRequestTypeDef",
    "DeleteItemInputTableDeleteItemTypeDef",
    "DeleteItemOutputTableTypeDef",
    "DeleteItemOutputTypeDef",
    "DeleteReplicaActionTypeDef",
    "DeleteReplicationGroupMemberActionTypeDef",
    "DeleteRequestOutputTypeDef",
    "DeleteRequestServiceResourceOutputTypeDef",
    "DeleteRequestServiceResourceTypeDef",
    "DeleteRequestServiceResourceUnionTypeDef",
    "DeleteRequestTypeDef",
    "DeleteRequestUnionTypeDef",
    "DeleteResourcePolicyInputRequestTypeDef",
    "DeleteResourcePolicyOutputTypeDef",
    "DeleteTableInputRequestTypeDef",
    "DeleteTableOutputTypeDef",
    "DeleteTypeDef",
    "DescribeBackupInputRequestTypeDef",
    "DescribeBackupOutputTypeDef",
    "DescribeContinuousBackupsInputRequestTypeDef",
    "DescribeContinuousBackupsOutputTypeDef",
    "DescribeContributorInsightsInputRequestTypeDef",
    "DescribeContributorInsightsOutputTypeDef",
    "DescribeEndpointsResponseTypeDef",
    "DescribeExportInputRequestTypeDef",
    "DescribeExportOutputTypeDef",
    "DescribeGlobalTableInputRequestTypeDef",
    "DescribeGlobalTableOutputTypeDef",
    "DescribeGlobalTableSettingsInputRequestTypeDef",
    "DescribeGlobalTableSettingsOutputTypeDef",
    "DescribeImportInputRequestTypeDef",
    "DescribeImportOutputTypeDef",
    "DescribeKinesisStreamingDestinationInputRequestTypeDef",
    "DescribeKinesisStreamingDestinationOutputTypeDef",
    "DescribeLimitsOutputTypeDef",
    "DescribeTableInputRequestTypeDef",
    "DescribeTableInputTableExistsWaitTypeDef",
    "DescribeTableInputTableNotExistsWaitTypeDef",
    "DescribeTableOutputTypeDef",
    "DescribeTableReplicaAutoScalingInputRequestTypeDef",
    "DescribeTableReplicaAutoScalingOutputTypeDef",
    "DescribeTimeToLiveInputRequestTypeDef",
    "DescribeTimeToLiveOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableKinesisStreamingConfigurationTypeDef",
    "EndpointTypeDef",
    "ExecuteStatementInputRequestTypeDef",
    "ExecuteStatementOutputTypeDef",
    "ExecuteTransactionInputRequestTypeDef",
    "ExecuteTransactionOutputTypeDef",
    "ExpectedAttributeValueTableTypeDef",
    "ExpectedAttributeValueTypeDef",
    "ExportDescriptionTypeDef",
    "ExportSummaryTypeDef",
    "ExportTableToPointInTimeInputRequestTypeDef",
    "ExportTableToPointInTimeOutputTypeDef",
    "FailureExceptionTypeDef",
    "GetItemInputRequestTypeDef",
    "GetItemInputTableGetItemTypeDef",
    "GetItemOutputTableTypeDef",
    "GetItemOutputTypeDef",
    "GetResourcePolicyInputRequestTypeDef",
    "GetResourcePolicyOutputTypeDef",
    "GetTypeDef",
    "GlobalSecondaryIndexAutoScalingUpdateTypeDef",
    "GlobalSecondaryIndexDescriptionTypeDef",
    "GlobalSecondaryIndexInfoTypeDef",
    "GlobalSecondaryIndexOutputTypeDef",
    "GlobalSecondaryIndexTypeDef",
    "GlobalSecondaryIndexUnionTypeDef",
    "GlobalSecondaryIndexUpdateTypeDef",
    "GlobalSecondaryIndexWarmThroughputDescriptionTypeDef",
    "GlobalTableDescriptionTypeDef",
    "GlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef",
    "GlobalTableTypeDef",
    "ImportSummaryTypeDef",
    "ImportTableDescriptionTypeDef",
    "ImportTableInputRequestTypeDef",
    "ImportTableOutputTypeDef",
    "IncrementalExportSpecificationOutputTypeDef",
    "IncrementalExportSpecificationTypeDef",
    "InputFormatOptionsOutputTypeDef",
    "InputFormatOptionsTypeDef",
    "ItemCollectionMetricsServiceResourceTypeDef",
    "ItemCollectionMetricsTableTypeDef",
    "ItemCollectionMetricsTypeDef",
    "ItemResponseTypeDef",
    "KeySchemaElementTypeDef",
    "KeysAndAttributesOutputTypeDef",
    "KeysAndAttributesServiceResourceOutputTypeDef",
    "KeysAndAttributesServiceResourceTypeDef",
    "KeysAndAttributesServiceResourceUnionTypeDef",
    "KeysAndAttributesTypeDef",
    "KeysAndAttributesUnionTypeDef",
    "KinesisDataStreamDestinationTypeDef",
    "KinesisStreamingDestinationInputRequestTypeDef",
    "KinesisStreamingDestinationOutputTypeDef",
    "ListBackupsInputListBackupsPaginateTypeDef",
    "ListBackupsInputRequestTypeDef",
    "ListBackupsOutputTypeDef",
    "ListContributorInsightsInputRequestTypeDef",
    "ListContributorInsightsOutputTypeDef",
    "ListExportsInputRequestTypeDef",
    "ListExportsOutputTypeDef",
    "ListGlobalTablesInputRequestTypeDef",
    "ListGlobalTablesOutputTypeDef",
    "ListImportsInputRequestTypeDef",
    "ListImportsOutputTypeDef",
    "ListTablesInputListTablesPaginateTypeDef",
    "ListTablesInputRequestTypeDef",
    "ListTablesOutputTypeDef",
    "ListTagsOfResourceInputListTagsOfResourcePaginateTypeDef",
    "ListTagsOfResourceInputRequestTypeDef",
    "ListTagsOfResourceOutputTypeDef",
    "LocalSecondaryIndexDescriptionTypeDef",
    "LocalSecondaryIndexInfoTypeDef",
    "LocalSecondaryIndexTypeDef",
    "OnDemandThroughputOverrideTypeDef",
    "OnDemandThroughputTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterizedStatementTypeDef",
    "PointInTimeRecoveryDescriptionTypeDef",
    "PointInTimeRecoverySpecificationTypeDef",
    "ProjectionOutputTypeDef",
    "ProjectionTypeDef",
    "ProjectionUnionTypeDef",
    "ProvisionedThroughputDescriptionTypeDef",
    "ProvisionedThroughputOverrideTypeDef",
    "ProvisionedThroughputTypeDef",
    "PutItemInputRequestTypeDef",
    "PutItemInputTablePutItemTypeDef",
    "PutItemOutputTableTypeDef",
    "PutItemOutputTypeDef",
    "PutRequestOutputTypeDef",
    "PutRequestServiceResourceOutputTypeDef",
    "PutRequestServiceResourceTypeDef",
    "PutRequestServiceResourceUnionTypeDef",
    "PutRequestTypeDef",
    "PutRequestUnionTypeDef",
    "PutResourcePolicyInputRequestTypeDef",
    "PutResourcePolicyOutputTypeDef",
    "PutTypeDef",
    "QueryInputQueryPaginateTypeDef",
    "QueryInputRequestTypeDef",
    "QueryInputTableQueryTypeDef",
    "QueryOutputTableTypeDef",
    "QueryOutputTypeDef",
    "ReplicaAutoScalingDescriptionTypeDef",
    "ReplicaAutoScalingUpdateTypeDef",
    "ReplicaDescriptionTypeDef",
    "ReplicaGlobalSecondaryIndexAutoScalingDescriptionTypeDef",
    "ReplicaGlobalSecondaryIndexAutoScalingUpdateTypeDef",
    "ReplicaGlobalSecondaryIndexDescriptionTypeDef",
    "ReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef",
    "ReplicaGlobalSecondaryIndexSettingsUpdateTypeDef",
    "ReplicaGlobalSecondaryIndexTypeDef",
    "ReplicaSettingsDescriptionTypeDef",
    "ReplicaSettingsUpdateTypeDef",
    "ReplicaTypeDef",
    "ReplicaUpdateTypeDef",
    "ReplicationGroupUpdateTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreSummaryTypeDef",
    "RestoreTableFromBackupInputRequestTypeDef",
    "RestoreTableFromBackupOutputTypeDef",
    "RestoreTableToPointInTimeInputRequestTypeDef",
    "RestoreTableToPointInTimeOutputTypeDef",
    "S3BucketSourceTypeDef",
    "SSEDescriptionTypeDef",
    "SSESpecificationTypeDef",
    "ScanInputRequestTypeDef",
    "ScanInputScanPaginateTypeDef",
    "ScanInputTableScanTypeDef",
    "ScanOutputTableTypeDef",
    "ScanOutputTypeDef",
    "SourceTableDetailsTypeDef",
    "SourceTableFeatureDetailsTypeDef",
    "StreamSpecificationTypeDef",
    "TableAttributeValueTypeDef",
    "TableAutoScalingDescriptionTypeDef",
    "TableBatchWriterRequestTypeDef",
    "TableClassSummaryTypeDef",
    "TableCreationParametersOutputTypeDef",
    "TableCreationParametersTypeDef",
    "TableDescriptionTypeDef",
    "TableWarmThroughputDescriptionTypeDef",
    "TagResourceInputRequestTypeDef",
    "TagTypeDef",
    "TimeToLiveDescriptionTypeDef",
    "TimeToLiveSpecificationTypeDef",
    "TimestampTypeDef",
    "TransactGetItemTypeDef",
    "TransactGetItemsInputRequestTypeDef",
    "TransactGetItemsOutputTypeDef",
    "TransactWriteItemTypeDef",
    "TransactWriteItemsInputRequestTypeDef",
    "TransactWriteItemsOutputTypeDef",
    "UniversalAttributeValueTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateContinuousBackupsInputRequestTypeDef",
    "UpdateContinuousBackupsOutputTypeDef",
    "UpdateContributorInsightsInputRequestTypeDef",
    "UpdateContributorInsightsOutputTypeDef",
    "UpdateGlobalSecondaryIndexActionTypeDef",
    "UpdateGlobalTableInputRequestTypeDef",
    "UpdateGlobalTableOutputTypeDef",
    "UpdateGlobalTableSettingsInputRequestTypeDef",
    "UpdateGlobalTableSettingsOutputTypeDef",
    "UpdateItemInputRequestTypeDef",
    "UpdateItemInputTableUpdateItemTypeDef",
    "UpdateItemOutputTableTypeDef",
    "UpdateItemOutputTypeDef",
    "UpdateKinesisStreamingConfigurationTypeDef",
    "UpdateKinesisStreamingDestinationInputRequestTypeDef",
    "UpdateKinesisStreamingDestinationOutputTypeDef",
    "UpdateReplicationGroupMemberActionTypeDef",
    "UpdateTableInputRequestTypeDef",
    "UpdateTableInputTableUpdateTypeDef",
    "UpdateTableOutputTypeDef",
    "UpdateTableReplicaAutoScalingInputRequestTypeDef",
    "UpdateTableReplicaAutoScalingOutputTypeDef",
    "UpdateTimeToLiveInputRequestTypeDef",
    "UpdateTimeToLiveOutputTypeDef",
    "UpdateTypeDef",
    "WaiterConfigTypeDef",
    "WarmThroughputTypeDef",
    "WriteRequestOutputTypeDef",
    "WriteRequestServiceResourceOutputTypeDef",
    "WriteRequestServiceResourceTypeDef",
    "WriteRequestServiceResourceUnionTypeDef",
    "WriteRequestTypeDef",
    "WriteRequestUnionTypeDef",
)

class ArchivalSummaryTypeDef(TypedDict):
    ArchivalDateTime: NotRequired[datetime]
    ArchivalReason: NotRequired[str]
    ArchivalBackupArn: NotRequired[str]

class AttributeDefinitionTypeDef(TypedDict):
    AttributeName: str
    AttributeType: ScalarAttributeTypeType

class AttributeValueTypeDef(TypedDict):
    S: NotRequired[str]
    N: NotRequired[str]
    B: NotRequired[bytes]
    SS: NotRequired[Sequence[str]]
    NS: NotRequired[Sequence[str]]
    BS: NotRequired[Sequence[bytes]]
    M: NotRequired[Mapping[str, Any]]
    L: NotRequired[Sequence[Any]]
    NULL: NotRequired[bool]
    BOOL: NotRequired[bool]

TableAttributeValueTypeDef = Union[
    bytes,
    bytearray,
    str,
    int,
    Decimal,
    bool,
    Set[int],
    Set[Decimal],
    Set[str],
    Set[bytes],
    Set[bytearray],
    Sequence[Any],
    Mapping[str, Any],
    None,
]

class AutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef(TypedDict):
    TargetValue: float
    DisableScaleIn: NotRequired[bool]
    ScaleInCooldown: NotRequired[int]
    ScaleOutCooldown: NotRequired[int]

class AutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef(TypedDict):
    TargetValue: float
    DisableScaleIn: NotRequired[bool]
    ScaleInCooldown: NotRequired[int]
    ScaleOutCooldown: NotRequired[int]

class BackupDetailsTypeDef(TypedDict):
    BackupArn: str
    BackupName: str
    BackupStatus: BackupStatusType
    BackupType: BackupTypeType
    BackupCreationDateTime: datetime
    BackupSizeBytes: NotRequired[int]
    BackupExpiryDateTime: NotRequired[datetime]

class BackupSummaryTypeDef(TypedDict):
    TableName: NotRequired[str]
    TableId: NotRequired[str]
    TableArn: NotRequired[str]
    BackupArn: NotRequired[str]
    BackupName: NotRequired[str]
    BackupCreationDateTime: NotRequired[datetime]
    BackupExpiryDateTime: NotRequired[datetime]
    BackupStatus: NotRequired[BackupStatusType]
    BackupType: NotRequired[BackupTypeType]
    BackupSizeBytes: NotRequired[int]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BillingModeSummaryTypeDef(TypedDict):
    BillingMode: NotRequired[BillingModeType]
    LastUpdateToPayPerRequestDateTime: NotRequired[datetime]

class CapacityTypeDef(TypedDict):
    ReadCapacityUnits: NotRequired[float]
    WriteCapacityUnits: NotRequired[float]
    CapacityUnits: NotRequired[float]

ConditionBaseImportTypeDef = Union[str, ConditionBase]

class PointInTimeRecoveryDescriptionTypeDef(TypedDict):
    PointInTimeRecoveryStatus: NotRequired[PointInTimeRecoveryStatusType]
    EarliestRestorableDateTime: NotRequired[datetime]
    LatestRestorableDateTime: NotRequired[datetime]

class ContributorInsightsSummaryTypeDef(TypedDict):
    TableName: NotRequired[str]
    IndexName: NotRequired[str]
    ContributorInsightsStatus: NotRequired[ContributorInsightsStatusType]

class CreateBackupInputRequestTypeDef(TypedDict):
    TableName: str
    BackupName: str

class KeySchemaElementTypeDef(TypedDict):
    AttributeName: str
    KeyType: KeyTypeType

class OnDemandThroughputTypeDef(TypedDict):
    MaxReadRequestUnits: NotRequired[int]
    MaxWriteRequestUnits: NotRequired[int]

class ProvisionedThroughputTypeDef(TypedDict):
    ReadCapacityUnits: int
    WriteCapacityUnits: int

class WarmThroughputTypeDef(TypedDict):
    ReadUnitsPerSecond: NotRequired[int]
    WriteUnitsPerSecond: NotRequired[int]

ReplicaTypeDef = TypedDict(
    "ReplicaTypeDef",
    {
        "RegionName": NotRequired[str],
    },
)
CreateReplicaActionTypeDef = TypedDict(
    "CreateReplicaActionTypeDef",
    {
        "RegionName": str,
    },
)

class OnDemandThroughputOverrideTypeDef(TypedDict):
    MaxReadRequestUnits: NotRequired[int]

class ProvisionedThroughputOverrideTypeDef(TypedDict):
    ReadCapacityUnits: NotRequired[int]

class SSESpecificationTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    SSEType: NotRequired[SSETypeType]
    KMSMasterKeyId: NotRequired[str]

class StreamSpecificationTypeDef(TypedDict):
    StreamEnabled: bool
    StreamViewType: NotRequired[StreamViewTypeType]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class CsvOptionsOutputTypeDef(TypedDict):
    Delimiter: NotRequired[str]
    HeaderList: NotRequired[List[str]]

class CsvOptionsTypeDef(TypedDict):
    Delimiter: NotRequired[str]
    HeaderList: NotRequired[Sequence[str]]

class DeleteBackupInputRequestTypeDef(TypedDict):
    BackupArn: str

class DeleteGlobalSecondaryIndexActionTypeDef(TypedDict):
    IndexName: str

DeleteReplicaActionTypeDef = TypedDict(
    "DeleteReplicaActionTypeDef",
    {
        "RegionName": str,
    },
)
DeleteReplicationGroupMemberActionTypeDef = TypedDict(
    "DeleteReplicationGroupMemberActionTypeDef",
    {
        "RegionName": str,
    },
)

class DeleteResourcePolicyInputRequestTypeDef(TypedDict):
    ResourceArn: str
    ExpectedRevisionId: NotRequired[str]

class DeleteTableInputRequestTypeDef(TypedDict):
    TableName: str

class DescribeBackupInputRequestTypeDef(TypedDict):
    BackupArn: str

class DescribeContinuousBackupsInputRequestTypeDef(TypedDict):
    TableName: str

class DescribeContributorInsightsInputRequestTypeDef(TypedDict):
    TableName: str
    IndexName: NotRequired[str]

class FailureExceptionTypeDef(TypedDict):
    ExceptionName: NotRequired[str]
    ExceptionDescription: NotRequired[str]

class EndpointTypeDef(TypedDict):
    Address: str
    CachePeriodInMinutes: int

class DescribeExportInputRequestTypeDef(TypedDict):
    ExportArn: str

class DescribeGlobalTableInputRequestTypeDef(TypedDict):
    GlobalTableName: str

class DescribeGlobalTableSettingsInputRequestTypeDef(TypedDict):
    GlobalTableName: str

class DescribeImportInputRequestTypeDef(TypedDict):
    ImportArn: str

class DescribeKinesisStreamingDestinationInputRequestTypeDef(TypedDict):
    TableName: str

class KinesisDataStreamDestinationTypeDef(TypedDict):
    StreamArn: NotRequired[str]
    DestinationStatus: NotRequired[DestinationStatusType]
    DestinationStatusDescription: NotRequired[str]
    ApproximateCreationDateTimePrecision: NotRequired[ApproximateCreationDateTimePrecisionType]

class DescribeTableInputRequestTypeDef(TypedDict):
    TableName: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class DescribeTableReplicaAutoScalingInputRequestTypeDef(TypedDict):
    TableName: str

class DescribeTimeToLiveInputRequestTypeDef(TypedDict):
    TableName: str

class TimeToLiveDescriptionTypeDef(TypedDict):
    TimeToLiveStatus: NotRequired[TimeToLiveStatusType]
    AttributeName: NotRequired[str]

class EnableKinesisStreamingConfigurationTypeDef(TypedDict):
    ApproximateCreationDateTimePrecision: NotRequired[ApproximateCreationDateTimePrecisionType]

class IncrementalExportSpecificationOutputTypeDef(TypedDict):
    ExportFromTime: NotRequired[datetime]
    ExportToTime: NotRequired[datetime]
    ExportViewType: NotRequired[ExportViewTypeType]

class ExportSummaryTypeDef(TypedDict):
    ExportArn: NotRequired[str]
    ExportStatus: NotRequired[ExportStatusType]
    ExportType: NotRequired[ExportTypeType]

TimestampTypeDef = Union[datetime, str]

class GetResourcePolicyInputRequestTypeDef(TypedDict):
    ResourceArn: str

class GlobalSecondaryIndexWarmThroughputDescriptionTypeDef(TypedDict):
    ReadUnitsPerSecond: NotRequired[int]
    WriteUnitsPerSecond: NotRequired[int]
    Status: NotRequired[IndexStatusType]

class ProjectionOutputTypeDef(TypedDict):
    ProjectionType: NotRequired[ProjectionTypeType]
    NonKeyAttributes: NotRequired[List[str]]

class ProvisionedThroughputDescriptionTypeDef(TypedDict):
    LastIncreaseDateTime: NotRequired[datetime]
    LastDecreaseDateTime: NotRequired[datetime]
    NumberOfDecreasesToday: NotRequired[int]
    ReadCapacityUnits: NotRequired[int]
    WriteCapacityUnits: NotRequired[int]

class ProjectionTypeDef(TypedDict):
    ProjectionType: NotRequired[ProjectionTypeType]
    NonKeyAttributes: NotRequired[Sequence[str]]

class S3BucketSourceTypeDef(TypedDict):
    S3Bucket: str
    S3BucketOwner: NotRequired[str]
    S3KeyPrefix: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListContributorInsightsInputRequestTypeDef(TypedDict):
    TableName: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListExportsInputRequestTypeDef(TypedDict):
    TableArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

ListGlobalTablesInputRequestTypeDef = TypedDict(
    "ListGlobalTablesInputRequestTypeDef",
    {
        "ExclusiveStartGlobalTableName": NotRequired[str],
        "Limit": NotRequired[int],
        "RegionName": NotRequired[str],
    },
)

class ListImportsInputRequestTypeDef(TypedDict):
    TableArn: NotRequired[str]
    PageSize: NotRequired[int]
    NextToken: NotRequired[str]

class ListTablesInputRequestTypeDef(TypedDict):
    ExclusiveStartTableName: NotRequired[str]
    Limit: NotRequired[int]

class ListTagsOfResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    NextToken: NotRequired[str]

class PointInTimeRecoverySpecificationTypeDef(TypedDict):
    PointInTimeRecoveryEnabled: bool

class PutResourcePolicyInputRequestTypeDef(TypedDict):
    ResourceArn: str
    Policy: str
    ExpectedRevisionId: NotRequired[str]
    ConfirmRemoveSelfResourceAccess: NotRequired[bool]

class TableClassSummaryTypeDef(TypedDict):
    TableClass: NotRequired[TableClassType]
    LastUpdateDateTime: NotRequired[datetime]

class TableWarmThroughputDescriptionTypeDef(TypedDict):
    ReadUnitsPerSecond: NotRequired[int]
    WriteUnitsPerSecond: NotRequired[int]
    Status: NotRequired[TableStatusType]

class RestoreSummaryTypeDef(TypedDict):
    RestoreDateTime: datetime
    RestoreInProgress: bool
    SourceBackupArn: NotRequired[str]
    SourceTableArn: NotRequired[str]

class SSEDescriptionTypeDef(TypedDict):
    Status: NotRequired[SSEStatusType]
    SSEType: NotRequired[SSETypeType]
    KMSMasterKeyArn: NotRequired[str]
    InaccessibleEncryptionDateTime: NotRequired[datetime]

class TableBatchWriterRequestTypeDef(TypedDict):
    overwrite_by_pkeys: NotRequired[List[str]]

class TimeToLiveSpecificationTypeDef(TypedDict):
    Enabled: bool
    AttributeName: str

class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateContributorInsightsInputRequestTypeDef(TypedDict):
    TableName: str
    ContributorInsightsAction: ContributorInsightsActionType
    IndexName: NotRequired[str]

class UpdateKinesisStreamingConfigurationTypeDef(TypedDict):
    ApproximateCreationDateTimePrecision: NotRequired[ApproximateCreationDateTimePrecisionType]

class BatchStatementErrorTypeDef(TypedDict):
    Code: NotRequired[BatchStatementErrorCodeEnumType]
    Message: NotRequired[str]
    Item: NotRequired[Dict[str, AttributeValueTypeDef]]

class DeleteRequestOutputTypeDef(TypedDict):
    Key: Dict[str, AttributeValueTypeDef]

class ItemCollectionMetricsTypeDef(TypedDict):
    ItemCollectionKey: NotRequired[Dict[str, AttributeValueTypeDef]]
    SizeEstimateRangeGB: NotRequired[List[float]]

class ItemResponseTypeDef(TypedDict):
    Item: NotRequired[Dict[str, AttributeValueTypeDef]]

class KeysAndAttributesOutputTypeDef(TypedDict):
    Keys: List[Dict[str, AttributeValueTypeDef]]
    AttributesToGet: NotRequired[List[str]]
    ConsistentRead: NotRequired[bool]
    ProjectionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Dict[str, str]]

class PutRequestOutputTypeDef(TypedDict):
    Item: Dict[str, AttributeValueTypeDef]

UniversalAttributeValueTypeDef = Union[
    AttributeValueTypeDef,
    bytes,
    bytearray,
    str,
    int,
    Decimal,
    bool,
    Set[int],
    Set[Decimal],
    Set[str],
    Set[bytes],
    Set[bytearray],
    Sequence[Any],
    Mapping[str, Any],
    None,
]

class AttributeValueUpdateTableTypeDef(TypedDict):
    Value: NotRequired[TableAttributeValueTypeDef]
    Action: NotRequired[AttributeActionType]

class ConditionTableTypeDef(TypedDict):
    ComparisonOperator: ComparisonOperatorType
    AttributeValueList: NotRequired[Sequence[TableAttributeValueTypeDef]]

class DeleteRequestServiceResourceOutputTypeDef(TypedDict):
    Key: Dict[str, TableAttributeValueTypeDef]

class DeleteRequestServiceResourceTypeDef(TypedDict):
    Key: Mapping[str, TableAttributeValueTypeDef]

class ExpectedAttributeValueTableTypeDef(TypedDict):
    Value: NotRequired[TableAttributeValueTypeDef]
    Exists: NotRequired[bool]
    ComparisonOperator: NotRequired[ComparisonOperatorType]
    AttributeValueList: NotRequired[Sequence[TableAttributeValueTypeDef]]

class GetItemInputTableGetItemTypeDef(TypedDict):
    Key: Mapping[str, TableAttributeValueTypeDef]
    AttributesToGet: NotRequired[Sequence[str]]
    ConsistentRead: NotRequired[bool]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ProjectionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]

class ItemCollectionMetricsServiceResourceTypeDef(TypedDict):
    ItemCollectionKey: NotRequired[Dict[str, TableAttributeValueTypeDef]]
    SizeEstimateRangeGB: NotRequired[List[float]]

class ItemCollectionMetricsTableTypeDef(TypedDict):
    ItemCollectionKey: NotRequired[Dict[str, TableAttributeValueTypeDef]]
    SizeEstimateRangeGB: NotRequired[List[float]]

class KeysAndAttributesServiceResourceOutputTypeDef(TypedDict):
    Keys: List[Dict[str, TableAttributeValueTypeDef]]
    AttributesToGet: NotRequired[List[str]]
    ConsistentRead: NotRequired[bool]
    ProjectionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Dict[str, str]]

class KeysAndAttributesServiceResourceTypeDef(TypedDict):
    Keys: Sequence[Mapping[str, TableAttributeValueTypeDef]]
    AttributesToGet: NotRequired[Sequence[str]]
    ConsistentRead: NotRequired[bool]
    ProjectionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]

class PutRequestServiceResourceOutputTypeDef(TypedDict):
    Item: Dict[str, TableAttributeValueTypeDef]

class PutRequestServiceResourceTypeDef(TypedDict):
    Item: Mapping[str, TableAttributeValueTypeDef]

class AutoScalingPolicyDescriptionTypeDef(TypedDict):
    PolicyName: NotRequired[str]
    TargetTrackingScalingPolicyConfiguration: NotRequired[
        AutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef
    ]

class AutoScalingPolicyUpdateTypeDef(TypedDict):
    TargetTrackingScalingPolicyConfiguration: (
        AutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef
    )
    PolicyName: NotRequired[str]

class CreateBackupOutputTypeDef(TypedDict):
    BackupDetails: BackupDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteResourcePolicyOutputTypeDef(TypedDict):
    RevisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeLimitsOutputTypeDef(TypedDict):
    AccountMaxReadCapacityUnits: int
    AccountMaxWriteCapacityUnits: int
    TableMaxReadCapacityUnits: int
    TableMaxWriteCapacityUnits: int
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourcePolicyOutputTypeDef(TypedDict):
    Policy: str
    RevisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListBackupsOutputTypeDef(TypedDict):
    BackupSummaries: List[BackupSummaryTypeDef]
    LastEvaluatedBackupArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTablesOutputTypeDef(TypedDict):
    TableNames: List[str]
    LastEvaluatedTableName: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutResourcePolicyOutputTypeDef(TypedDict):
    RevisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateContributorInsightsOutputTypeDef(TypedDict):
    TableName: str
    IndexName: str
    ContributorInsightsStatus: ContributorInsightsStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ConsumedCapacityTypeDef(TypedDict):
    TableName: NotRequired[str]
    CapacityUnits: NotRequired[float]
    ReadCapacityUnits: NotRequired[float]
    WriteCapacityUnits: NotRequired[float]
    Table: NotRequired[CapacityTypeDef]
    LocalSecondaryIndexes: NotRequired[Dict[str, CapacityTypeDef]]
    GlobalSecondaryIndexes: NotRequired[Dict[str, CapacityTypeDef]]

class ContinuousBackupsDescriptionTypeDef(TypedDict):
    ContinuousBackupsStatus: ContinuousBackupsStatusType
    PointInTimeRecoveryDescription: NotRequired[PointInTimeRecoveryDescriptionTypeDef]

class ListContributorInsightsOutputTypeDef(TypedDict):
    ContributorInsightsSummaries: List[ContributorInsightsSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class SourceTableDetailsTypeDef(TypedDict):
    TableName: str
    TableId: str
    KeySchema: List[KeySchemaElementTypeDef]
    TableCreationDateTime: datetime
    ProvisionedThroughput: ProvisionedThroughputTypeDef
    TableArn: NotRequired[str]
    TableSizeBytes: NotRequired[int]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]
    ItemCount: NotRequired[int]
    BillingMode: NotRequired[BillingModeType]

class UpdateGlobalSecondaryIndexActionTypeDef(TypedDict):
    IndexName: str
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]
    WarmThroughput: NotRequired[WarmThroughputTypeDef]

class CreateGlobalTableInputRequestTypeDef(TypedDict):
    GlobalTableName: str
    ReplicationGroup: Sequence[ReplicaTypeDef]

class GlobalTableTypeDef(TypedDict):
    GlobalTableName: NotRequired[str]
    ReplicationGroup: NotRequired[List[ReplicaTypeDef]]

class ReplicaGlobalSecondaryIndexTypeDef(TypedDict):
    IndexName: str
    ProvisionedThroughputOverride: NotRequired[ProvisionedThroughputOverrideTypeDef]
    OnDemandThroughputOverride: NotRequired[OnDemandThroughputOverrideTypeDef]

class ListTagsOfResourceOutputTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class InputFormatOptionsOutputTypeDef(TypedDict):
    Csv: NotRequired[CsvOptionsOutputTypeDef]

CsvOptionsUnionTypeDef = Union[CsvOptionsTypeDef, CsvOptionsOutputTypeDef]

class ReplicaUpdateTypeDef(TypedDict):
    Create: NotRequired[CreateReplicaActionTypeDef]
    Delete: NotRequired[DeleteReplicaActionTypeDef]

class DescribeContributorInsightsOutputTypeDef(TypedDict):
    TableName: str
    IndexName: str
    ContributorInsightsRuleList: List[str]
    ContributorInsightsStatus: ContributorInsightsStatusType
    LastUpdateDateTime: datetime
    FailureException: FailureExceptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeEndpointsResponseTypeDef(TypedDict):
    Endpoints: List[EndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeKinesisStreamingDestinationOutputTypeDef(TypedDict):
    TableName: str
    KinesisDataStreamDestinations: List[KinesisDataStreamDestinationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeTableInputTableExistsWaitTypeDef(TypedDict):
    TableName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeTableInputTableNotExistsWaitTypeDef(TypedDict):
    TableName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeTimeToLiveOutputTypeDef(TypedDict):
    TimeToLiveDescription: TimeToLiveDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class KinesisStreamingDestinationInputRequestTypeDef(TypedDict):
    TableName: str
    StreamArn: str
    EnableKinesisStreamingConfiguration: NotRequired[EnableKinesisStreamingConfigurationTypeDef]

class KinesisStreamingDestinationOutputTypeDef(TypedDict):
    TableName: str
    StreamArn: str
    DestinationStatus: DestinationStatusType
    EnableKinesisStreamingConfiguration: EnableKinesisStreamingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExportDescriptionTypeDef(TypedDict):
    ExportArn: NotRequired[str]
    ExportStatus: NotRequired[ExportStatusType]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    ExportManifest: NotRequired[str]
    TableArn: NotRequired[str]
    TableId: NotRequired[str]
    ExportTime: NotRequired[datetime]
    ClientToken: NotRequired[str]
    S3Bucket: NotRequired[str]
    S3BucketOwner: NotRequired[str]
    S3Prefix: NotRequired[str]
    S3SseAlgorithm: NotRequired[S3SseAlgorithmType]
    S3SseKmsKeyId: NotRequired[str]
    FailureCode: NotRequired[str]
    FailureMessage: NotRequired[str]
    ExportFormat: NotRequired[ExportFormatType]
    BilledSizeBytes: NotRequired[int]
    ItemCount: NotRequired[int]
    ExportType: NotRequired[ExportTypeType]
    IncrementalExportSpecification: NotRequired[IncrementalExportSpecificationOutputTypeDef]

class ListExportsOutputTypeDef(TypedDict):
    ExportSummaries: List[ExportSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class IncrementalExportSpecificationTypeDef(TypedDict):
    ExportFromTime: NotRequired[TimestampTypeDef]
    ExportToTime: NotRequired[TimestampTypeDef]
    ExportViewType: NotRequired[ExportViewTypeType]

class ListBackupsInputRequestTypeDef(TypedDict):
    TableName: NotRequired[str]
    Limit: NotRequired[int]
    TimeRangeLowerBound: NotRequired[TimestampTypeDef]
    TimeRangeUpperBound: NotRequired[TimestampTypeDef]
    ExclusiveStartBackupArn: NotRequired[str]
    BackupType: NotRequired[BackupTypeFilterType]

class ReplicaGlobalSecondaryIndexDescriptionTypeDef(TypedDict):
    IndexName: NotRequired[str]
    ProvisionedThroughputOverride: NotRequired[ProvisionedThroughputOverrideTypeDef]
    OnDemandThroughputOverride: NotRequired[OnDemandThroughputOverrideTypeDef]
    WarmThroughput: NotRequired[GlobalSecondaryIndexWarmThroughputDescriptionTypeDef]

class GlobalSecondaryIndexInfoTypeDef(TypedDict):
    IndexName: NotRequired[str]
    KeySchema: NotRequired[List[KeySchemaElementTypeDef]]
    Projection: NotRequired[ProjectionOutputTypeDef]
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]

class GlobalSecondaryIndexOutputTypeDef(TypedDict):
    IndexName: str
    KeySchema: List[KeySchemaElementTypeDef]
    Projection: ProjectionOutputTypeDef
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]
    WarmThroughput: NotRequired[WarmThroughputTypeDef]

class LocalSecondaryIndexDescriptionTypeDef(TypedDict):
    IndexName: NotRequired[str]
    KeySchema: NotRequired[List[KeySchemaElementTypeDef]]
    Projection: NotRequired[ProjectionOutputTypeDef]
    IndexSizeBytes: NotRequired[int]
    ItemCount: NotRequired[int]
    IndexArn: NotRequired[str]

class LocalSecondaryIndexInfoTypeDef(TypedDict):
    IndexName: NotRequired[str]
    KeySchema: NotRequired[List[KeySchemaElementTypeDef]]
    Projection: NotRequired[ProjectionOutputTypeDef]

class GlobalSecondaryIndexDescriptionTypeDef(TypedDict):
    IndexName: NotRequired[str]
    KeySchema: NotRequired[List[KeySchemaElementTypeDef]]
    Projection: NotRequired[ProjectionOutputTypeDef]
    IndexStatus: NotRequired[IndexStatusType]
    Backfilling: NotRequired[bool]
    ProvisionedThroughput: NotRequired[ProvisionedThroughputDescriptionTypeDef]
    IndexSizeBytes: NotRequired[int]
    ItemCount: NotRequired[int]
    IndexArn: NotRequired[str]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]
    WarmThroughput: NotRequired[GlobalSecondaryIndexWarmThroughputDescriptionTypeDef]

class GlobalSecondaryIndexTypeDef(TypedDict):
    IndexName: str
    KeySchema: Sequence[KeySchemaElementTypeDef]
    Projection: ProjectionTypeDef
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]
    WarmThroughput: NotRequired[WarmThroughputTypeDef]

ProjectionUnionTypeDef = Union[ProjectionTypeDef, ProjectionOutputTypeDef]

class ImportSummaryTypeDef(TypedDict):
    ImportArn: NotRequired[str]
    ImportStatus: NotRequired[ImportStatusType]
    TableArn: NotRequired[str]
    S3BucketSource: NotRequired[S3BucketSourceTypeDef]
    CloudWatchLogGroupArn: NotRequired[str]
    InputFormat: NotRequired[InputFormatType]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]

class ListBackupsInputListBackupsPaginateTypeDef(TypedDict):
    TableName: NotRequired[str]
    TimeRangeLowerBound: NotRequired[TimestampTypeDef]
    TimeRangeUpperBound: NotRequired[TimestampTypeDef]
    BackupType: NotRequired[BackupTypeFilterType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTablesInputListTablesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTagsOfResourceInputListTagsOfResourcePaginateTypeDef(TypedDict):
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class UpdateContinuousBackupsInputRequestTypeDef(TypedDict):
    TableName: str
    PointInTimeRecoverySpecification: PointInTimeRecoverySpecificationTypeDef

class UpdateTimeToLiveInputRequestTypeDef(TypedDict):
    TableName: str
    TimeToLiveSpecification: TimeToLiveSpecificationTypeDef

class UpdateTimeToLiveOutputTypeDef(TypedDict):
    TimeToLiveSpecification: TimeToLiveSpecificationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateKinesisStreamingDestinationInputRequestTypeDef(TypedDict):
    TableName: str
    StreamArn: str
    UpdateKinesisStreamingConfiguration: NotRequired[UpdateKinesisStreamingConfigurationTypeDef]

class UpdateKinesisStreamingDestinationOutputTypeDef(TypedDict):
    TableName: str
    StreamArn: str
    DestinationStatus: DestinationStatusType
    UpdateKinesisStreamingConfiguration: UpdateKinesisStreamingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchStatementResponseTypeDef(TypedDict):
    Error: NotRequired[BatchStatementErrorTypeDef]
    TableName: NotRequired[str]
    Item: NotRequired[Dict[str, AttributeValueTypeDef]]

class WriteRequestOutputTypeDef(TypedDict):
    PutRequest: NotRequired[PutRequestOutputTypeDef]
    DeleteRequest: NotRequired[DeleteRequestOutputTypeDef]

class AttributeValueUpdateTypeDef(TypedDict):
    Value: NotRequired[UniversalAttributeValueTypeDef]
    Action: NotRequired[AttributeActionType]

class BatchStatementRequestTypeDef(TypedDict):
    Statement: str
    Parameters: NotRequired[Sequence[UniversalAttributeValueTypeDef]]
    ConsistentRead: NotRequired[bool]
    ReturnValuesOnConditionCheckFailure: NotRequired[ReturnValuesOnConditionCheckFailureType]

class ConditionCheckTypeDef(TypedDict):
    Key: Mapping[str, UniversalAttributeValueTypeDef]
    TableName: str
    ConditionExpression: str
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, UniversalAttributeValueTypeDef]]
    ReturnValuesOnConditionCheckFailure: NotRequired[ReturnValuesOnConditionCheckFailureType]

class ConditionTypeDef(TypedDict):
    ComparisonOperator: ComparisonOperatorType
    AttributeValueList: NotRequired[Sequence[UniversalAttributeValueTypeDef]]

class DeleteRequestTypeDef(TypedDict):
    Key: Mapping[str, UniversalAttributeValueTypeDef]

class DeleteTypeDef(TypedDict):
    Key: Mapping[str, UniversalAttributeValueTypeDef]
    TableName: str
    ConditionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, UniversalAttributeValueTypeDef]]
    ReturnValuesOnConditionCheckFailure: NotRequired[ReturnValuesOnConditionCheckFailureType]

class ExecuteStatementInputRequestTypeDef(TypedDict):
    Statement: str
    Parameters: NotRequired[Sequence[UniversalAttributeValueTypeDef]]
    ConsistentRead: NotRequired[bool]
    NextToken: NotRequired[str]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    Limit: NotRequired[int]
    ReturnValuesOnConditionCheckFailure: NotRequired[ReturnValuesOnConditionCheckFailureType]

class ExpectedAttributeValueTypeDef(TypedDict):
    Value: NotRequired[UniversalAttributeValueTypeDef]
    Exists: NotRequired[bool]
    ComparisonOperator: NotRequired[ComparisonOperatorType]
    AttributeValueList: NotRequired[Sequence[UniversalAttributeValueTypeDef]]

class GetItemInputRequestTypeDef(TypedDict):
    TableName: str
    Key: Mapping[str, UniversalAttributeValueTypeDef]
    AttributesToGet: NotRequired[Sequence[str]]
    ConsistentRead: NotRequired[bool]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ProjectionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]

class GetTypeDef(TypedDict):
    Key: Mapping[str, UniversalAttributeValueTypeDef]
    TableName: str
    ProjectionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]

class KeysAndAttributesTypeDef(TypedDict):
    Keys: Sequence[Mapping[str, UniversalAttributeValueTypeDef]]
    AttributesToGet: NotRequired[Sequence[str]]
    ConsistentRead: NotRequired[bool]
    ProjectionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]

class ParameterizedStatementTypeDef(TypedDict):
    Statement: str
    Parameters: NotRequired[Sequence[UniversalAttributeValueTypeDef]]
    ReturnValuesOnConditionCheckFailure: NotRequired[ReturnValuesOnConditionCheckFailureType]

class PutRequestTypeDef(TypedDict):
    Item: Mapping[str, UniversalAttributeValueTypeDef]

class PutTypeDef(TypedDict):
    Item: Mapping[str, UniversalAttributeValueTypeDef]
    TableName: str
    ConditionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, UniversalAttributeValueTypeDef]]
    ReturnValuesOnConditionCheckFailure: NotRequired[ReturnValuesOnConditionCheckFailureType]

class UpdateTypeDef(TypedDict):
    Key: Mapping[str, UniversalAttributeValueTypeDef]
    UpdateExpression: str
    TableName: str
    ConditionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, UniversalAttributeValueTypeDef]]
    ReturnValuesOnConditionCheckFailure: NotRequired[ReturnValuesOnConditionCheckFailureType]

class QueryInputTableQueryTypeDef(TypedDict):
    IndexName: NotRequired[str]
    Select: NotRequired[SelectType]
    AttributesToGet: NotRequired[Sequence[str]]
    Limit: NotRequired[int]
    ConsistentRead: NotRequired[bool]
    KeyConditions: NotRequired[Mapping[str, ConditionTableTypeDef]]
    QueryFilter: NotRequired[Mapping[str, ConditionTableTypeDef]]
    ConditionalOperator: NotRequired[ConditionalOperatorType]
    ScanIndexForward: NotRequired[bool]
    ExclusiveStartKey: NotRequired[Mapping[str, TableAttributeValueTypeDef]]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ProjectionExpression: NotRequired[str]
    FilterExpression: NotRequired[ConditionBaseImportTypeDef]
    KeyConditionExpression: NotRequired[ConditionBaseImportTypeDef]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, TableAttributeValueTypeDef]]

class ScanInputTableScanTypeDef(TypedDict):
    IndexName: NotRequired[str]
    AttributesToGet: NotRequired[Sequence[str]]
    Limit: NotRequired[int]
    Select: NotRequired[SelectType]
    ScanFilter: NotRequired[Mapping[str, ConditionTableTypeDef]]
    ConditionalOperator: NotRequired[ConditionalOperatorType]
    ExclusiveStartKey: NotRequired[Mapping[str, TableAttributeValueTypeDef]]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    TotalSegments: NotRequired[int]
    Segment: NotRequired[int]
    ProjectionExpression: NotRequired[str]
    FilterExpression: NotRequired[ConditionBaseImportTypeDef]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, TableAttributeValueTypeDef]]
    ConsistentRead: NotRequired[bool]

DeleteRequestServiceResourceUnionTypeDef = Union[
    DeleteRequestServiceResourceTypeDef, DeleteRequestServiceResourceOutputTypeDef
]

class DeleteItemInputTableDeleteItemTypeDef(TypedDict):
    Key: Mapping[str, TableAttributeValueTypeDef]
    Expected: NotRequired[Mapping[str, ExpectedAttributeValueTableTypeDef]]
    ConditionalOperator: NotRequired[ConditionalOperatorType]
    ReturnValues: NotRequired[ReturnValueType]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ReturnItemCollectionMetrics: NotRequired[ReturnItemCollectionMetricsType]
    ConditionExpression: NotRequired[ConditionBaseImportTypeDef]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, TableAttributeValueTypeDef]]
    ReturnValuesOnConditionCheckFailure: NotRequired[ReturnValuesOnConditionCheckFailureType]

class PutItemInputTablePutItemTypeDef(TypedDict):
    Item: Mapping[str, TableAttributeValueTypeDef]
    Expected: NotRequired[Mapping[str, ExpectedAttributeValueTableTypeDef]]
    ReturnValues: NotRequired[ReturnValueType]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ReturnItemCollectionMetrics: NotRequired[ReturnItemCollectionMetricsType]
    ConditionalOperator: NotRequired[ConditionalOperatorType]
    ConditionExpression: NotRequired[ConditionBaseImportTypeDef]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, TableAttributeValueTypeDef]]
    ReturnValuesOnConditionCheckFailure: NotRequired[ReturnValuesOnConditionCheckFailureType]

class UpdateItemInputTableUpdateItemTypeDef(TypedDict):
    Key: Mapping[str, TableAttributeValueTypeDef]
    AttributeUpdates: NotRequired[Mapping[str, AttributeValueUpdateTableTypeDef]]
    Expected: NotRequired[Mapping[str, ExpectedAttributeValueTableTypeDef]]
    ConditionalOperator: NotRequired[ConditionalOperatorType]
    ReturnValues: NotRequired[ReturnValueType]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ReturnItemCollectionMetrics: NotRequired[ReturnItemCollectionMetricsType]
    UpdateExpression: NotRequired[str]
    ConditionExpression: NotRequired[ConditionBaseImportTypeDef]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, TableAttributeValueTypeDef]]
    ReturnValuesOnConditionCheckFailure: NotRequired[ReturnValuesOnConditionCheckFailureType]

KeysAndAttributesServiceResourceUnionTypeDef = Union[
    KeysAndAttributesServiceResourceTypeDef, KeysAndAttributesServiceResourceOutputTypeDef
]

class WriteRequestServiceResourceOutputTypeDef(TypedDict):
    PutRequest: NotRequired[PutRequestServiceResourceOutputTypeDef]
    DeleteRequest: NotRequired[DeleteRequestServiceResourceOutputTypeDef]

PutRequestServiceResourceUnionTypeDef = Union[
    PutRequestServiceResourceTypeDef, PutRequestServiceResourceOutputTypeDef
]

class AutoScalingSettingsDescriptionTypeDef(TypedDict):
    MinimumUnits: NotRequired[int]
    MaximumUnits: NotRequired[int]
    AutoScalingDisabled: NotRequired[bool]
    AutoScalingRoleArn: NotRequired[str]
    ScalingPolicies: NotRequired[List[AutoScalingPolicyDescriptionTypeDef]]

class AutoScalingSettingsUpdateTypeDef(TypedDict):
    MinimumUnits: NotRequired[int]
    MaximumUnits: NotRequired[int]
    AutoScalingDisabled: NotRequired[bool]
    AutoScalingRoleArn: NotRequired[str]
    ScalingPolicyUpdate: NotRequired[AutoScalingPolicyUpdateTypeDef]

class BatchGetItemOutputServiceResourceTypeDef(TypedDict):
    Responses: Dict[str, List[Dict[str, TableAttributeValueTypeDef]]]
    UnprocessedKeys: Dict[str, KeysAndAttributesServiceResourceOutputTypeDef]
    ConsumedCapacity: List[ConsumedCapacityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetItemOutputTypeDef(TypedDict):
    Responses: Dict[str, List[Dict[str, AttributeValueTypeDef]]]
    UnprocessedKeys: Dict[str, KeysAndAttributesOutputTypeDef]
    ConsumedCapacity: List[ConsumedCapacityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteItemOutputTableTypeDef(TypedDict):
    Attributes: Dict[str, TableAttributeValueTypeDef]
    ConsumedCapacity: ConsumedCapacityTypeDef
    ItemCollectionMetrics: ItemCollectionMetricsTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteItemOutputTypeDef(TypedDict):
    Attributes: Dict[str, AttributeValueTypeDef]
    ConsumedCapacity: ConsumedCapacityTypeDef
    ItemCollectionMetrics: ItemCollectionMetricsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExecuteStatementOutputTypeDef(TypedDict):
    Items: List[Dict[str, AttributeValueTypeDef]]
    ConsumedCapacity: ConsumedCapacityTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
    LastEvaluatedKey: NotRequired[Dict[str, AttributeValueTypeDef]]

class ExecuteTransactionOutputTypeDef(TypedDict):
    Responses: List[ItemResponseTypeDef]
    ConsumedCapacity: List[ConsumedCapacityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetItemOutputTableTypeDef(TypedDict):
    ConsumedCapacity: ConsumedCapacityTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    Item: NotRequired[Dict[str, TableAttributeValueTypeDef]]

class GetItemOutputTypeDef(TypedDict):
    ConsumedCapacity: ConsumedCapacityTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    Item: NotRequired[Dict[str, AttributeValueTypeDef]]

class PutItemOutputTableTypeDef(TypedDict):
    Attributes: Dict[str, TableAttributeValueTypeDef]
    ConsumedCapacity: ConsumedCapacityTypeDef
    ItemCollectionMetrics: ItemCollectionMetricsTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutItemOutputTypeDef(TypedDict):
    Attributes: Dict[str, AttributeValueTypeDef]
    ConsumedCapacity: ConsumedCapacityTypeDef
    ItemCollectionMetrics: ItemCollectionMetricsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class QueryOutputTableTypeDef(TypedDict):
    Items: List[Dict[str, TableAttributeValueTypeDef]]
    Count: int
    ScannedCount: int
    ConsumedCapacity: ConsumedCapacityTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    LastEvaluatedKey: NotRequired[Dict[str, TableAttributeValueTypeDef]]

class QueryOutputTypeDef(TypedDict):
    Items: List[Dict[str, AttributeValueTypeDef]]
    Count: int
    ScannedCount: int
    ConsumedCapacity: ConsumedCapacityTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    LastEvaluatedKey: NotRequired[Dict[str, AttributeValueTypeDef]]

class ScanOutputTableTypeDef(TypedDict):
    Items: List[Dict[str, TableAttributeValueTypeDef]]
    Count: int
    ScannedCount: int
    ConsumedCapacity: ConsumedCapacityTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    LastEvaluatedKey: NotRequired[Dict[str, TableAttributeValueTypeDef]]

class ScanOutputTypeDef(TypedDict):
    Items: List[Dict[str, AttributeValueTypeDef]]
    Count: int
    ScannedCount: int
    ConsumedCapacity: ConsumedCapacityTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    LastEvaluatedKey: NotRequired[Dict[str, AttributeValueTypeDef]]

class TransactGetItemsOutputTypeDef(TypedDict):
    ConsumedCapacity: List[ConsumedCapacityTypeDef]
    Responses: List[ItemResponseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TransactWriteItemsOutputTypeDef(TypedDict):
    ConsumedCapacity: List[ConsumedCapacityTypeDef]
    ItemCollectionMetrics: Dict[str, List[ItemCollectionMetricsTypeDef]]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateItemOutputTableTypeDef(TypedDict):
    Attributes: Dict[str, TableAttributeValueTypeDef]
    ConsumedCapacity: ConsumedCapacityTypeDef
    ItemCollectionMetrics: ItemCollectionMetricsTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateItemOutputTypeDef(TypedDict):
    Attributes: Dict[str, AttributeValueTypeDef]
    ConsumedCapacity: ConsumedCapacityTypeDef
    ItemCollectionMetrics: ItemCollectionMetricsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeContinuousBackupsOutputTypeDef(TypedDict):
    ContinuousBackupsDescription: ContinuousBackupsDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateContinuousBackupsOutputTypeDef(TypedDict):
    ContinuousBackupsDescription: ContinuousBackupsDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListGlobalTablesOutputTypeDef(TypedDict):
    GlobalTables: List[GlobalTableTypeDef]
    LastEvaluatedGlobalTableName: str
    ResponseMetadata: ResponseMetadataTypeDef

CreateReplicationGroupMemberActionTypeDef = TypedDict(
    "CreateReplicationGroupMemberActionTypeDef",
    {
        "RegionName": str,
        "KMSMasterKeyId": NotRequired[str],
        "ProvisionedThroughputOverride": NotRequired[ProvisionedThroughputOverrideTypeDef],
        "OnDemandThroughputOverride": NotRequired[OnDemandThroughputOverrideTypeDef],
        "GlobalSecondaryIndexes": NotRequired[Sequence[ReplicaGlobalSecondaryIndexTypeDef]],
        "TableClassOverride": NotRequired[TableClassType],
    },
)
UpdateReplicationGroupMemberActionTypeDef = TypedDict(
    "UpdateReplicationGroupMemberActionTypeDef",
    {
        "RegionName": str,
        "KMSMasterKeyId": NotRequired[str],
        "ProvisionedThroughputOverride": NotRequired[ProvisionedThroughputOverrideTypeDef],
        "OnDemandThroughputOverride": NotRequired[OnDemandThroughputOverrideTypeDef],
        "GlobalSecondaryIndexes": NotRequired[Sequence[ReplicaGlobalSecondaryIndexTypeDef]],
        "TableClassOverride": NotRequired[TableClassType],
    },
)

class InputFormatOptionsTypeDef(TypedDict):
    Csv: NotRequired[CsvOptionsUnionTypeDef]

class UpdateGlobalTableInputRequestTypeDef(TypedDict):
    GlobalTableName: str
    ReplicaUpdates: Sequence[ReplicaUpdateTypeDef]

class DescribeExportOutputTypeDef(TypedDict):
    ExportDescription: ExportDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExportTableToPointInTimeOutputTypeDef(TypedDict):
    ExportDescription: ExportDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExportTableToPointInTimeInputRequestTypeDef(TypedDict):
    TableArn: str
    S3Bucket: str
    ExportTime: NotRequired[TimestampTypeDef]
    ClientToken: NotRequired[str]
    S3BucketOwner: NotRequired[str]
    S3Prefix: NotRequired[str]
    S3SseAlgorithm: NotRequired[S3SseAlgorithmType]
    S3SseKmsKeyId: NotRequired[str]
    ExportFormat: NotRequired[ExportFormatType]
    ExportType: NotRequired[ExportTypeType]
    IncrementalExportSpecification: NotRequired[IncrementalExportSpecificationTypeDef]

ReplicaDescriptionTypeDef = TypedDict(
    "ReplicaDescriptionTypeDef",
    {
        "RegionName": NotRequired[str],
        "ReplicaStatus": NotRequired[ReplicaStatusType],
        "ReplicaStatusDescription": NotRequired[str],
        "ReplicaStatusPercentProgress": NotRequired[str],
        "KMSMasterKeyId": NotRequired[str],
        "ProvisionedThroughputOverride": NotRequired[ProvisionedThroughputOverrideTypeDef],
        "OnDemandThroughputOverride": NotRequired[OnDemandThroughputOverrideTypeDef],
        "WarmThroughput": NotRequired[TableWarmThroughputDescriptionTypeDef],
        "GlobalSecondaryIndexes": NotRequired[List[ReplicaGlobalSecondaryIndexDescriptionTypeDef]],
        "ReplicaInaccessibleDateTime": NotRequired[datetime],
        "ReplicaTableClassSummary": NotRequired[TableClassSummaryTypeDef],
    },
)

class TableCreationParametersOutputTypeDef(TypedDict):
    TableName: str
    AttributeDefinitions: List[AttributeDefinitionTypeDef]
    KeySchema: List[KeySchemaElementTypeDef]
    BillingMode: NotRequired[BillingModeType]
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]
    SSESpecification: NotRequired[SSESpecificationTypeDef]
    GlobalSecondaryIndexes: NotRequired[List[GlobalSecondaryIndexOutputTypeDef]]

class SourceTableFeatureDetailsTypeDef(TypedDict):
    LocalSecondaryIndexes: NotRequired[List[LocalSecondaryIndexInfoTypeDef]]
    GlobalSecondaryIndexes: NotRequired[List[GlobalSecondaryIndexInfoTypeDef]]
    StreamDescription: NotRequired[StreamSpecificationTypeDef]
    TimeToLiveDescription: NotRequired[TimeToLiveDescriptionTypeDef]
    SSEDescription: NotRequired[SSEDescriptionTypeDef]

GlobalSecondaryIndexUnionTypeDef = Union[
    GlobalSecondaryIndexTypeDef, GlobalSecondaryIndexOutputTypeDef
]

class CreateGlobalSecondaryIndexActionTypeDef(TypedDict):
    IndexName: str
    KeySchema: Sequence[KeySchemaElementTypeDef]
    Projection: ProjectionUnionTypeDef
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]
    WarmThroughput: NotRequired[WarmThroughputTypeDef]

class LocalSecondaryIndexTypeDef(TypedDict):
    IndexName: str
    KeySchema: Sequence[KeySchemaElementTypeDef]
    Projection: ProjectionUnionTypeDef

class ListImportsOutputTypeDef(TypedDict):
    ImportSummaryList: List[ImportSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class BatchExecuteStatementOutputTypeDef(TypedDict):
    Responses: List[BatchStatementResponseTypeDef]
    ConsumedCapacity: List[ConsumedCapacityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchWriteItemOutputTypeDef(TypedDict):
    UnprocessedItems: Dict[str, List[WriteRequestOutputTypeDef]]
    ItemCollectionMetrics: Dict[str, List[ItemCollectionMetricsTypeDef]]
    ConsumedCapacity: List[ConsumedCapacityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchExecuteStatementInputRequestTypeDef(TypedDict):
    Statements: Sequence[BatchStatementRequestTypeDef]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]

class QueryInputQueryPaginateTypeDef(TypedDict):
    TableName: str
    IndexName: NotRequired[str]
    Select: NotRequired[SelectType]
    AttributesToGet: NotRequired[Sequence[str]]
    ConsistentRead: NotRequired[bool]
    KeyConditions: NotRequired[Mapping[str, ConditionTypeDef]]
    QueryFilter: NotRequired[Mapping[str, ConditionTypeDef]]
    ConditionalOperator: NotRequired[ConditionalOperatorType]
    ScanIndexForward: NotRequired[bool]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ProjectionExpression: NotRequired[str]
    FilterExpression: NotRequired[str]
    KeyConditionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, UniversalAttributeValueTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class QueryInputRequestTypeDef(TypedDict):
    TableName: str
    IndexName: NotRequired[str]
    Select: NotRequired[SelectType]
    AttributesToGet: NotRequired[Sequence[str]]
    Limit: NotRequired[int]
    ConsistentRead: NotRequired[bool]
    KeyConditions: NotRequired[Mapping[str, ConditionTypeDef]]
    QueryFilter: NotRequired[Mapping[str, ConditionTypeDef]]
    ConditionalOperator: NotRequired[ConditionalOperatorType]
    ScanIndexForward: NotRequired[bool]
    ExclusiveStartKey: NotRequired[Mapping[str, UniversalAttributeValueTypeDef]]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ProjectionExpression: NotRequired[str]
    FilterExpression: NotRequired[str]
    KeyConditionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, UniversalAttributeValueTypeDef]]

class ScanInputRequestTypeDef(TypedDict):
    TableName: str
    IndexName: NotRequired[str]
    AttributesToGet: NotRequired[Sequence[str]]
    Limit: NotRequired[int]
    Select: NotRequired[SelectType]
    ScanFilter: NotRequired[Mapping[str, ConditionTypeDef]]
    ConditionalOperator: NotRequired[ConditionalOperatorType]
    ExclusiveStartKey: NotRequired[Mapping[str, UniversalAttributeValueTypeDef]]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    TotalSegments: NotRequired[int]
    Segment: NotRequired[int]
    ProjectionExpression: NotRequired[str]
    FilterExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, UniversalAttributeValueTypeDef]]
    ConsistentRead: NotRequired[bool]

class ScanInputScanPaginateTypeDef(TypedDict):
    TableName: str
    IndexName: NotRequired[str]
    AttributesToGet: NotRequired[Sequence[str]]
    Select: NotRequired[SelectType]
    ScanFilter: NotRequired[Mapping[str, ConditionTypeDef]]
    ConditionalOperator: NotRequired[ConditionalOperatorType]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    TotalSegments: NotRequired[int]
    Segment: NotRequired[int]
    ProjectionExpression: NotRequired[str]
    FilterExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, UniversalAttributeValueTypeDef]]
    ConsistentRead: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

DeleteRequestUnionTypeDef = Union[DeleteRequestTypeDef, DeleteRequestOutputTypeDef]

class DeleteItemInputRequestTypeDef(TypedDict):
    TableName: str
    Key: Mapping[str, UniversalAttributeValueTypeDef]
    Expected: NotRequired[Mapping[str, ExpectedAttributeValueTypeDef]]
    ConditionalOperator: NotRequired[ConditionalOperatorType]
    ReturnValues: NotRequired[ReturnValueType]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ReturnItemCollectionMetrics: NotRequired[ReturnItemCollectionMetricsType]
    ConditionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, UniversalAttributeValueTypeDef]]
    ReturnValuesOnConditionCheckFailure: NotRequired[ReturnValuesOnConditionCheckFailureType]

class PutItemInputRequestTypeDef(TypedDict):
    TableName: str
    Item: Mapping[str, UniversalAttributeValueTypeDef]
    Expected: NotRequired[Mapping[str, ExpectedAttributeValueTypeDef]]
    ReturnValues: NotRequired[ReturnValueType]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ReturnItemCollectionMetrics: NotRequired[ReturnItemCollectionMetricsType]
    ConditionalOperator: NotRequired[ConditionalOperatorType]
    ConditionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, UniversalAttributeValueTypeDef]]
    ReturnValuesOnConditionCheckFailure: NotRequired[ReturnValuesOnConditionCheckFailureType]

class UpdateItemInputRequestTypeDef(TypedDict):
    TableName: str
    Key: Mapping[str, UniversalAttributeValueTypeDef]
    AttributeUpdates: NotRequired[Mapping[str, AttributeValueUpdateTypeDef]]
    Expected: NotRequired[Mapping[str, ExpectedAttributeValueTypeDef]]
    ConditionalOperator: NotRequired[ConditionalOperatorType]
    ReturnValues: NotRequired[ReturnValueType]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ReturnItemCollectionMetrics: NotRequired[ReturnItemCollectionMetricsType]
    UpdateExpression: NotRequired[str]
    ConditionExpression: NotRequired[str]
    ExpressionAttributeNames: NotRequired[Mapping[str, str]]
    ExpressionAttributeValues: NotRequired[Mapping[str, UniversalAttributeValueTypeDef]]
    ReturnValuesOnConditionCheckFailure: NotRequired[ReturnValuesOnConditionCheckFailureType]

class TransactGetItemTypeDef(TypedDict):
    Get: GetTypeDef

KeysAndAttributesUnionTypeDef = Union[KeysAndAttributesTypeDef, KeysAndAttributesOutputTypeDef]

class ExecuteTransactionInputRequestTypeDef(TypedDict):
    TransactStatements: Sequence[ParameterizedStatementTypeDef]
    ClientRequestToken: NotRequired[str]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]

PutRequestUnionTypeDef = Union[PutRequestTypeDef, PutRequestOutputTypeDef]

class TransactWriteItemTypeDef(TypedDict):
    ConditionCheck: NotRequired[ConditionCheckTypeDef]
    Put: NotRequired[PutTypeDef]
    Delete: NotRequired[DeleteTypeDef]
    Update: NotRequired[UpdateTypeDef]

class BatchGetItemInputServiceResourceBatchGetItemTypeDef(TypedDict):
    RequestItems: Mapping[str, KeysAndAttributesServiceResourceUnionTypeDef]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]

class BatchWriteItemOutputServiceResourceTypeDef(TypedDict):
    UnprocessedItems: Dict[str, List[WriteRequestServiceResourceOutputTypeDef]]
    ItemCollectionMetrics: Dict[str, List[ItemCollectionMetricsServiceResourceTypeDef]]
    ConsumedCapacity: List[ConsumedCapacityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class WriteRequestServiceResourceTypeDef(TypedDict):
    PutRequest: NotRequired[PutRequestServiceResourceUnionTypeDef]
    DeleteRequest: NotRequired[DeleteRequestServiceResourceUnionTypeDef]

class ReplicaGlobalSecondaryIndexAutoScalingDescriptionTypeDef(TypedDict):
    IndexName: NotRequired[str]
    IndexStatus: NotRequired[IndexStatusType]
    ProvisionedReadCapacityAutoScalingSettings: NotRequired[AutoScalingSettingsDescriptionTypeDef]
    ProvisionedWriteCapacityAutoScalingSettings: NotRequired[AutoScalingSettingsDescriptionTypeDef]

class ReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef(TypedDict):
    IndexName: str
    IndexStatus: NotRequired[IndexStatusType]
    ProvisionedReadCapacityUnits: NotRequired[int]
    ProvisionedReadCapacityAutoScalingSettings: NotRequired[AutoScalingSettingsDescriptionTypeDef]
    ProvisionedWriteCapacityUnits: NotRequired[int]
    ProvisionedWriteCapacityAutoScalingSettings: NotRequired[AutoScalingSettingsDescriptionTypeDef]

class GlobalSecondaryIndexAutoScalingUpdateTypeDef(TypedDict):
    IndexName: NotRequired[str]
    ProvisionedWriteCapacityAutoScalingUpdate: NotRequired[AutoScalingSettingsUpdateTypeDef]

class GlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef(TypedDict):
    IndexName: str
    ProvisionedWriteCapacityUnits: NotRequired[int]
    ProvisionedWriteCapacityAutoScalingSettingsUpdate: NotRequired[AutoScalingSettingsUpdateTypeDef]

class ReplicaGlobalSecondaryIndexAutoScalingUpdateTypeDef(TypedDict):
    IndexName: NotRequired[str]
    ProvisionedReadCapacityAutoScalingUpdate: NotRequired[AutoScalingSettingsUpdateTypeDef]

class ReplicaGlobalSecondaryIndexSettingsUpdateTypeDef(TypedDict):
    IndexName: str
    ProvisionedReadCapacityUnits: NotRequired[int]
    ProvisionedReadCapacityAutoScalingSettingsUpdate: NotRequired[AutoScalingSettingsUpdateTypeDef]

class ReplicationGroupUpdateTypeDef(TypedDict):
    Create: NotRequired[CreateReplicationGroupMemberActionTypeDef]
    Update: NotRequired[UpdateReplicationGroupMemberActionTypeDef]
    Delete: NotRequired[DeleteReplicationGroupMemberActionTypeDef]

class GlobalTableDescriptionTypeDef(TypedDict):
    ReplicationGroup: NotRequired[List[ReplicaDescriptionTypeDef]]
    GlobalTableArn: NotRequired[str]
    CreationDateTime: NotRequired[datetime]
    GlobalTableStatus: NotRequired[GlobalTableStatusType]
    GlobalTableName: NotRequired[str]

class TableDescriptionTypeDef(TypedDict):
    AttributeDefinitions: NotRequired[List[AttributeDefinitionTypeDef]]
    TableName: NotRequired[str]
    KeySchema: NotRequired[List[KeySchemaElementTypeDef]]
    TableStatus: NotRequired[TableStatusType]
    CreationDateTime: NotRequired[datetime]
    ProvisionedThroughput: NotRequired[ProvisionedThroughputDescriptionTypeDef]
    TableSizeBytes: NotRequired[int]
    ItemCount: NotRequired[int]
    TableArn: NotRequired[str]
    TableId: NotRequired[str]
    BillingModeSummary: NotRequired[BillingModeSummaryTypeDef]
    LocalSecondaryIndexes: NotRequired[List[LocalSecondaryIndexDescriptionTypeDef]]
    GlobalSecondaryIndexes: NotRequired[List[GlobalSecondaryIndexDescriptionTypeDef]]
    StreamSpecification: NotRequired[StreamSpecificationTypeDef]
    LatestStreamLabel: NotRequired[str]
    LatestStreamArn: NotRequired[str]
    GlobalTableVersion: NotRequired[str]
    Replicas: NotRequired[List[ReplicaDescriptionTypeDef]]
    RestoreSummary: NotRequired[RestoreSummaryTypeDef]
    SSEDescription: NotRequired[SSEDescriptionTypeDef]
    ArchivalSummary: NotRequired[ArchivalSummaryTypeDef]
    TableClassSummary: NotRequired[TableClassSummaryTypeDef]
    DeletionProtectionEnabled: NotRequired[bool]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]
    WarmThroughput: NotRequired[TableWarmThroughputDescriptionTypeDef]
    MultiRegionConsistency: NotRequired[MultiRegionConsistencyType]

class ImportTableDescriptionTypeDef(TypedDict):
    ImportArn: NotRequired[str]
    ImportStatus: NotRequired[ImportStatusType]
    TableArn: NotRequired[str]
    TableId: NotRequired[str]
    ClientToken: NotRequired[str]
    S3BucketSource: NotRequired[S3BucketSourceTypeDef]
    ErrorCount: NotRequired[int]
    CloudWatchLogGroupArn: NotRequired[str]
    InputFormat: NotRequired[InputFormatType]
    InputFormatOptions: NotRequired[InputFormatOptionsOutputTypeDef]
    InputCompressionType: NotRequired[InputCompressionTypeType]
    TableCreationParameters: NotRequired[TableCreationParametersOutputTypeDef]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    ProcessedSizeBytes: NotRequired[int]
    ProcessedItemCount: NotRequired[int]
    ImportedItemCount: NotRequired[int]
    FailureCode: NotRequired[str]
    FailureMessage: NotRequired[str]

class BackupDescriptionTypeDef(TypedDict):
    BackupDetails: NotRequired[BackupDetailsTypeDef]
    SourceTableDetails: NotRequired[SourceTableDetailsTypeDef]
    SourceTableFeatureDetails: NotRequired[SourceTableFeatureDetailsTypeDef]

class TableCreationParametersTypeDef(TypedDict):
    TableName: str
    AttributeDefinitions: Sequence[AttributeDefinitionTypeDef]
    KeySchema: Sequence[KeySchemaElementTypeDef]
    BillingMode: NotRequired[BillingModeType]
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]
    SSESpecification: NotRequired[SSESpecificationTypeDef]
    GlobalSecondaryIndexes: NotRequired[Sequence[GlobalSecondaryIndexUnionTypeDef]]

class GlobalSecondaryIndexUpdateTypeDef(TypedDict):
    Update: NotRequired[UpdateGlobalSecondaryIndexActionTypeDef]
    Create: NotRequired[CreateGlobalSecondaryIndexActionTypeDef]
    Delete: NotRequired[DeleteGlobalSecondaryIndexActionTypeDef]

class CreateTableInputRequestTypeDef(TypedDict):
    AttributeDefinitions: Sequence[AttributeDefinitionTypeDef]
    TableName: str
    KeySchema: Sequence[KeySchemaElementTypeDef]
    LocalSecondaryIndexes: NotRequired[Sequence[LocalSecondaryIndexTypeDef]]
    GlobalSecondaryIndexes: NotRequired[Sequence[GlobalSecondaryIndexUnionTypeDef]]
    BillingMode: NotRequired[BillingModeType]
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    StreamSpecification: NotRequired[StreamSpecificationTypeDef]
    SSESpecification: NotRequired[SSESpecificationTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    TableClass: NotRequired[TableClassType]
    DeletionProtectionEnabled: NotRequired[bool]
    WarmThroughput: NotRequired[WarmThroughputTypeDef]
    ResourcePolicy: NotRequired[str]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]

class CreateTableInputServiceResourceCreateTableTypeDef(TypedDict):
    AttributeDefinitions: Sequence[AttributeDefinitionTypeDef]
    TableName: str
    KeySchema: Sequence[KeySchemaElementTypeDef]
    LocalSecondaryIndexes: NotRequired[Sequence[LocalSecondaryIndexTypeDef]]
    GlobalSecondaryIndexes: NotRequired[Sequence[GlobalSecondaryIndexTypeDef]]
    BillingMode: NotRequired[BillingModeType]
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    StreamSpecification: NotRequired[StreamSpecificationTypeDef]
    SSESpecification: NotRequired[SSESpecificationTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    TableClass: NotRequired[TableClassType]
    DeletionProtectionEnabled: NotRequired[bool]
    WarmThroughput: NotRequired[WarmThroughputTypeDef]
    ResourcePolicy: NotRequired[str]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]

class RestoreTableFromBackupInputRequestTypeDef(TypedDict):
    TargetTableName: str
    BackupArn: str
    BillingModeOverride: NotRequired[BillingModeType]
    GlobalSecondaryIndexOverride: NotRequired[Sequence[GlobalSecondaryIndexTypeDef]]
    LocalSecondaryIndexOverride: NotRequired[Sequence[LocalSecondaryIndexTypeDef]]
    ProvisionedThroughputOverride: NotRequired[ProvisionedThroughputTypeDef]
    OnDemandThroughputOverride: NotRequired[OnDemandThroughputTypeDef]
    SSESpecificationOverride: NotRequired[SSESpecificationTypeDef]

class RestoreTableToPointInTimeInputRequestTypeDef(TypedDict):
    TargetTableName: str
    SourceTableArn: NotRequired[str]
    SourceTableName: NotRequired[str]
    UseLatestRestorableTime: NotRequired[bool]
    RestoreDateTime: NotRequired[TimestampTypeDef]
    BillingModeOverride: NotRequired[BillingModeType]
    GlobalSecondaryIndexOverride: NotRequired[Sequence[GlobalSecondaryIndexTypeDef]]
    LocalSecondaryIndexOverride: NotRequired[Sequence[LocalSecondaryIndexTypeDef]]
    ProvisionedThroughputOverride: NotRequired[ProvisionedThroughputTypeDef]
    OnDemandThroughputOverride: NotRequired[OnDemandThroughputTypeDef]
    SSESpecificationOverride: NotRequired[SSESpecificationTypeDef]

class TransactGetItemsInputRequestTypeDef(TypedDict):
    TransactItems: Sequence[TransactGetItemTypeDef]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]

class BatchGetItemInputRequestTypeDef(TypedDict):
    RequestItems: Mapping[str, KeysAndAttributesUnionTypeDef]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]

class WriteRequestTypeDef(TypedDict):
    PutRequest: NotRequired[PutRequestUnionTypeDef]
    DeleteRequest: NotRequired[DeleteRequestUnionTypeDef]

class TransactWriteItemsInputRequestTypeDef(TypedDict):
    TransactItems: Sequence[TransactWriteItemTypeDef]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ReturnItemCollectionMetrics: NotRequired[ReturnItemCollectionMetricsType]
    ClientRequestToken: NotRequired[str]

WriteRequestServiceResourceUnionTypeDef = Union[
    WriteRequestServiceResourceTypeDef, WriteRequestServiceResourceOutputTypeDef
]
ReplicaAutoScalingDescriptionTypeDef = TypedDict(
    "ReplicaAutoScalingDescriptionTypeDef",
    {
        "RegionName": NotRequired[str],
        "GlobalSecondaryIndexes": NotRequired[
            List[ReplicaGlobalSecondaryIndexAutoScalingDescriptionTypeDef]
        ],
        "ReplicaProvisionedReadCapacityAutoScalingSettings": NotRequired[
            AutoScalingSettingsDescriptionTypeDef
        ],
        "ReplicaProvisionedWriteCapacityAutoScalingSettings": NotRequired[
            AutoScalingSettingsDescriptionTypeDef
        ],
        "ReplicaStatus": NotRequired[ReplicaStatusType],
    },
)
ReplicaSettingsDescriptionTypeDef = TypedDict(
    "ReplicaSettingsDescriptionTypeDef",
    {
        "RegionName": str,
        "ReplicaStatus": NotRequired[ReplicaStatusType],
        "ReplicaBillingModeSummary": NotRequired[BillingModeSummaryTypeDef],
        "ReplicaProvisionedReadCapacityUnits": NotRequired[int],
        "ReplicaProvisionedReadCapacityAutoScalingSettings": NotRequired[
            AutoScalingSettingsDescriptionTypeDef
        ],
        "ReplicaProvisionedWriteCapacityUnits": NotRequired[int],
        "ReplicaProvisionedWriteCapacityAutoScalingSettings": NotRequired[
            AutoScalingSettingsDescriptionTypeDef
        ],
        "ReplicaGlobalSecondaryIndexSettings": NotRequired[
            List[ReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef]
        ],
        "ReplicaTableClassSummary": NotRequired[TableClassSummaryTypeDef],
    },
)
ReplicaAutoScalingUpdateTypeDef = TypedDict(
    "ReplicaAutoScalingUpdateTypeDef",
    {
        "RegionName": str,
        "ReplicaGlobalSecondaryIndexUpdates": NotRequired[
            Sequence[ReplicaGlobalSecondaryIndexAutoScalingUpdateTypeDef]
        ],
        "ReplicaProvisionedReadCapacityAutoScalingUpdate": NotRequired[
            AutoScalingSettingsUpdateTypeDef
        ],
    },
)
ReplicaSettingsUpdateTypeDef = TypedDict(
    "ReplicaSettingsUpdateTypeDef",
    {
        "RegionName": str,
        "ReplicaProvisionedReadCapacityUnits": NotRequired[int],
        "ReplicaProvisionedReadCapacityAutoScalingSettingsUpdate": NotRequired[
            AutoScalingSettingsUpdateTypeDef
        ],
        "ReplicaGlobalSecondaryIndexSettingsUpdate": NotRequired[
            Sequence[ReplicaGlobalSecondaryIndexSettingsUpdateTypeDef]
        ],
        "ReplicaTableClass": NotRequired[TableClassType],
    },
)

class CreateGlobalTableOutputTypeDef(TypedDict):
    GlobalTableDescription: GlobalTableDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeGlobalTableOutputTypeDef(TypedDict):
    GlobalTableDescription: GlobalTableDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGlobalTableOutputTypeDef(TypedDict):
    GlobalTableDescription: GlobalTableDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTableOutputTypeDef(TypedDict):
    TableDescription: TableDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteTableOutputTypeDef(TypedDict):
    TableDescription: TableDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeTableOutputTypeDef(TypedDict):
    Table: TableDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RestoreTableFromBackupOutputTypeDef(TypedDict):
    TableDescription: TableDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RestoreTableToPointInTimeOutputTypeDef(TypedDict):
    TableDescription: TableDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTableOutputTypeDef(TypedDict):
    TableDescription: TableDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeImportOutputTypeDef(TypedDict):
    ImportTableDescription: ImportTableDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ImportTableOutputTypeDef(TypedDict):
    ImportTableDescription: ImportTableDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBackupOutputTypeDef(TypedDict):
    BackupDescription: BackupDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBackupOutputTypeDef(TypedDict):
    BackupDescription: BackupDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ImportTableInputRequestTypeDef(TypedDict):
    S3BucketSource: S3BucketSourceTypeDef
    InputFormat: InputFormatType
    TableCreationParameters: TableCreationParametersTypeDef
    ClientToken: NotRequired[str]
    InputFormatOptions: NotRequired[InputFormatOptionsTypeDef]
    InputCompressionType: NotRequired[InputCompressionTypeType]

class UpdateTableInputRequestTypeDef(TypedDict):
    TableName: str
    AttributeDefinitions: NotRequired[Sequence[AttributeDefinitionTypeDef]]
    BillingMode: NotRequired[BillingModeType]
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    GlobalSecondaryIndexUpdates: NotRequired[Sequence[GlobalSecondaryIndexUpdateTypeDef]]
    StreamSpecification: NotRequired[StreamSpecificationTypeDef]
    SSESpecification: NotRequired[SSESpecificationTypeDef]
    ReplicaUpdates: NotRequired[Sequence[ReplicationGroupUpdateTypeDef]]
    TableClass: NotRequired[TableClassType]
    DeletionProtectionEnabled: NotRequired[bool]
    MultiRegionConsistency: NotRequired[MultiRegionConsistencyType]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]
    WarmThroughput: NotRequired[WarmThroughputTypeDef]

class UpdateTableInputTableUpdateTypeDef(TypedDict):
    AttributeDefinitions: NotRequired[Sequence[AttributeDefinitionTypeDef]]
    BillingMode: NotRequired[BillingModeType]
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    GlobalSecondaryIndexUpdates: NotRequired[Sequence[GlobalSecondaryIndexUpdateTypeDef]]
    StreamSpecification: NotRequired[StreamSpecificationTypeDef]
    SSESpecification: NotRequired[SSESpecificationTypeDef]
    ReplicaUpdates: NotRequired[Sequence[ReplicationGroupUpdateTypeDef]]
    TableClass: NotRequired[TableClassType]
    DeletionProtectionEnabled: NotRequired[bool]
    MultiRegionConsistency: NotRequired[MultiRegionConsistencyType]
    OnDemandThroughput: NotRequired[OnDemandThroughputTypeDef]
    WarmThroughput: NotRequired[WarmThroughputTypeDef]

WriteRequestUnionTypeDef = Union[WriteRequestTypeDef, WriteRequestOutputTypeDef]

class BatchWriteItemInputServiceResourceBatchWriteItemTypeDef(TypedDict):
    RequestItems: Mapping[str, Sequence[WriteRequestServiceResourceUnionTypeDef]]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ReturnItemCollectionMetrics: NotRequired[ReturnItemCollectionMetricsType]

class TableAutoScalingDescriptionTypeDef(TypedDict):
    TableName: NotRequired[str]
    TableStatus: NotRequired[TableStatusType]
    Replicas: NotRequired[List[ReplicaAutoScalingDescriptionTypeDef]]

class DescribeGlobalTableSettingsOutputTypeDef(TypedDict):
    GlobalTableName: str
    ReplicaSettings: List[ReplicaSettingsDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGlobalTableSettingsOutputTypeDef(TypedDict):
    GlobalTableName: str
    ReplicaSettings: List[ReplicaSettingsDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTableReplicaAutoScalingInputRequestTypeDef(TypedDict):
    TableName: str
    GlobalSecondaryIndexUpdates: NotRequired[Sequence[GlobalSecondaryIndexAutoScalingUpdateTypeDef]]
    ProvisionedWriteCapacityAutoScalingUpdate: NotRequired[AutoScalingSettingsUpdateTypeDef]
    ReplicaUpdates: NotRequired[Sequence[ReplicaAutoScalingUpdateTypeDef]]

class UpdateGlobalTableSettingsInputRequestTypeDef(TypedDict):
    GlobalTableName: str
    GlobalTableBillingMode: NotRequired[BillingModeType]
    GlobalTableProvisionedWriteCapacityUnits: NotRequired[int]
    GlobalTableProvisionedWriteCapacityAutoScalingSettingsUpdate: NotRequired[
        AutoScalingSettingsUpdateTypeDef
    ]
    GlobalTableGlobalSecondaryIndexSettingsUpdate: NotRequired[
        Sequence[GlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef]
    ]
    ReplicaSettingsUpdate: NotRequired[Sequence[ReplicaSettingsUpdateTypeDef]]

class BatchWriteItemInputRequestTypeDef(TypedDict):
    RequestItems: Mapping[str, Sequence[WriteRequestUnionTypeDef]]
    ReturnConsumedCapacity: NotRequired[ReturnConsumedCapacityType]
    ReturnItemCollectionMetrics: NotRequired[ReturnItemCollectionMetricsType]

class DescribeTableReplicaAutoScalingOutputTypeDef(TypedDict):
    TableAutoScalingDescription: TableAutoScalingDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTableReplicaAutoScalingOutputTypeDef(TypedDict):
    TableAutoScalingDescription: TableAutoScalingDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
