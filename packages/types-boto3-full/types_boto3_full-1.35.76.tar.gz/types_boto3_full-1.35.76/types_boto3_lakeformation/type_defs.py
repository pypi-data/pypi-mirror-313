"""
Type annotations for lakeformation service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lakeformation/type_defs/)

Usage::

    ```python
    from types_boto3_lakeformation.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ApplicationStatusType,
    ComparisonOperatorType,
    DataLakeResourceTypeType,
    EnableStatusType,
    FieldNameStringType,
    OptimizerTypeType,
    PermissionType,
    PermissionTypeType,
    QueryStateStringType,
    ResourceShareTypeType,
    ResourceTypeType,
    TransactionStatusFilterType,
    TransactionStatusType,
    TransactionTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AddLFTagsToResourceRequestRequestTypeDef",
    "AddLFTagsToResourceResponseTypeDef",
    "AddObjectInputTypeDef",
    "AssumeDecoratedRoleWithSAMLRequestRequestTypeDef",
    "AssumeDecoratedRoleWithSAMLResponseTypeDef",
    "AuditContextTypeDef",
    "BatchGrantPermissionsRequestRequestTypeDef",
    "BatchGrantPermissionsResponseTypeDef",
    "BatchPermissionsFailureEntryTypeDef",
    "BatchPermissionsRequestEntryOutputTypeDef",
    "BatchPermissionsRequestEntryTypeDef",
    "BatchPermissionsRequestEntryUnionTypeDef",
    "BatchRevokePermissionsRequestRequestTypeDef",
    "BatchRevokePermissionsResponseTypeDef",
    "CancelTransactionRequestRequestTypeDef",
    "CatalogResourceTypeDef",
    "ColumnLFTagTypeDef",
    "ColumnWildcardOutputTypeDef",
    "ColumnWildcardTypeDef",
    "ColumnWildcardUnionTypeDef",
    "CommitTransactionRequestRequestTypeDef",
    "CommitTransactionResponseTypeDef",
    "ConditionTypeDef",
    "CreateDataCellsFilterRequestRequestTypeDef",
    "CreateLFTagExpressionRequestRequestTypeDef",
    "CreateLFTagRequestRequestTypeDef",
    "CreateLakeFormationIdentityCenterConfigurationRequestRequestTypeDef",
    "CreateLakeFormationIdentityCenterConfigurationResponseTypeDef",
    "CreateLakeFormationOptInRequestRequestTypeDef",
    "DataCellsFilterOutputTypeDef",
    "DataCellsFilterResourceTypeDef",
    "DataCellsFilterTypeDef",
    "DataLakePrincipalTypeDef",
    "DataLakeSettingsOutputTypeDef",
    "DataLakeSettingsTypeDef",
    "DataLocationResourceTypeDef",
    "DatabaseResourceTypeDef",
    "DeleteDataCellsFilterRequestRequestTypeDef",
    "DeleteLFTagExpressionRequestRequestTypeDef",
    "DeleteLFTagRequestRequestTypeDef",
    "DeleteLakeFormationIdentityCenterConfigurationRequestRequestTypeDef",
    "DeleteLakeFormationOptInRequestRequestTypeDef",
    "DeleteObjectInputTypeDef",
    "DeleteObjectsOnCancelRequestRequestTypeDef",
    "DeregisterResourceRequestRequestTypeDef",
    "DescribeLakeFormationIdentityCenterConfigurationRequestRequestTypeDef",
    "DescribeLakeFormationIdentityCenterConfigurationResponseTypeDef",
    "DescribeResourceRequestRequestTypeDef",
    "DescribeResourceResponseTypeDef",
    "DescribeTransactionRequestRequestTypeDef",
    "DescribeTransactionResponseTypeDef",
    "DetailsMapTypeDef",
    "ErrorDetailTypeDef",
    "ExecutionStatisticsTypeDef",
    "ExtendTransactionRequestRequestTypeDef",
    "ExternalFilteringConfigurationOutputTypeDef",
    "ExternalFilteringConfigurationTypeDef",
    "FilterConditionTypeDef",
    "GetDataCellsFilterRequestRequestTypeDef",
    "GetDataCellsFilterResponseTypeDef",
    "GetDataLakePrincipalResponseTypeDef",
    "GetDataLakeSettingsRequestRequestTypeDef",
    "GetDataLakeSettingsResponseTypeDef",
    "GetEffectivePermissionsForPathRequestRequestTypeDef",
    "GetEffectivePermissionsForPathResponseTypeDef",
    "GetLFTagExpressionRequestRequestTypeDef",
    "GetLFTagExpressionResponseTypeDef",
    "GetLFTagRequestRequestTypeDef",
    "GetLFTagResponseTypeDef",
    "GetQueryStateRequestRequestTypeDef",
    "GetQueryStateResponseTypeDef",
    "GetQueryStatisticsRequestRequestTypeDef",
    "GetQueryStatisticsResponseTypeDef",
    "GetResourceLFTagsRequestRequestTypeDef",
    "GetResourceLFTagsResponseTypeDef",
    "GetTableObjectsRequestRequestTypeDef",
    "GetTableObjectsResponseTypeDef",
    "GetTemporaryGluePartitionCredentialsRequestRequestTypeDef",
    "GetTemporaryGluePartitionCredentialsResponseTypeDef",
    "GetTemporaryGlueTableCredentialsRequestRequestTypeDef",
    "GetTemporaryGlueTableCredentialsResponseTypeDef",
    "GetWorkUnitResultsRequestRequestTypeDef",
    "GetWorkUnitResultsResponseTypeDef",
    "GetWorkUnitsRequestGetWorkUnitsPaginateTypeDef",
    "GetWorkUnitsRequestRequestTypeDef",
    "GetWorkUnitsResponseTypeDef",
    "GrantPermissionsRequestRequestTypeDef",
    "LFTagErrorTypeDef",
    "LFTagExpressionResourceTypeDef",
    "LFTagExpressionTypeDef",
    "LFTagKeyResourceOutputTypeDef",
    "LFTagKeyResourceTypeDef",
    "LFTagKeyResourceUnionTypeDef",
    "LFTagOutputTypeDef",
    "LFTagPairOutputTypeDef",
    "LFTagPairTypeDef",
    "LFTagPairUnionTypeDef",
    "LFTagPolicyResourceOutputTypeDef",
    "LFTagPolicyResourceTypeDef",
    "LFTagPolicyResourceUnionTypeDef",
    "LFTagTypeDef",
    "LFTagUnionTypeDef",
    "LakeFormationOptInsInfoTypeDef",
    "ListDataCellsFilterRequestListDataCellsFilterPaginateTypeDef",
    "ListDataCellsFilterRequestRequestTypeDef",
    "ListDataCellsFilterResponseTypeDef",
    "ListLFTagExpressionsRequestListLFTagExpressionsPaginateTypeDef",
    "ListLFTagExpressionsRequestRequestTypeDef",
    "ListLFTagExpressionsResponseTypeDef",
    "ListLFTagsRequestListLFTagsPaginateTypeDef",
    "ListLFTagsRequestRequestTypeDef",
    "ListLFTagsResponseTypeDef",
    "ListLakeFormationOptInsRequestRequestTypeDef",
    "ListLakeFormationOptInsResponseTypeDef",
    "ListPermissionsRequestRequestTypeDef",
    "ListPermissionsResponseTypeDef",
    "ListResourcesRequestRequestTypeDef",
    "ListResourcesResponseTypeDef",
    "ListTableStorageOptimizersRequestRequestTypeDef",
    "ListTableStorageOptimizersResponseTypeDef",
    "ListTransactionsRequestRequestTypeDef",
    "ListTransactionsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PartitionObjectsTypeDef",
    "PartitionValueListTypeDef",
    "PlanningStatisticsTypeDef",
    "PrincipalPermissionsOutputTypeDef",
    "PrincipalPermissionsTypeDef",
    "PrincipalPermissionsUnionTypeDef",
    "PrincipalResourcePermissionsTypeDef",
    "PutDataLakeSettingsRequestRequestTypeDef",
    "QueryPlanningContextTypeDef",
    "QuerySessionContextTypeDef",
    "RegisterResourceRequestRequestTypeDef",
    "RemoveLFTagsFromResourceRequestRequestTypeDef",
    "RemoveLFTagsFromResourceResponseTypeDef",
    "ResourceInfoTypeDef",
    "ResourceOutputTypeDef",
    "ResourceTypeDef",
    "ResourceUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RevokePermissionsRequestRequestTypeDef",
    "RowFilterOutputTypeDef",
    "RowFilterTypeDef",
    "RowFilterUnionTypeDef",
    "SearchDatabasesByLFTagsRequestRequestTypeDef",
    "SearchDatabasesByLFTagsRequestSearchDatabasesByLFTagsPaginateTypeDef",
    "SearchDatabasesByLFTagsResponseTypeDef",
    "SearchTablesByLFTagsRequestRequestTypeDef",
    "SearchTablesByLFTagsRequestSearchTablesByLFTagsPaginateTypeDef",
    "SearchTablesByLFTagsResponseTypeDef",
    "StartQueryPlanningRequestRequestTypeDef",
    "StartQueryPlanningResponseTypeDef",
    "StartTransactionRequestRequestTypeDef",
    "StartTransactionResponseTypeDef",
    "StorageOptimizerTypeDef",
    "TableObjectTypeDef",
    "TableResourceOutputTypeDef",
    "TableResourceTypeDef",
    "TableResourceUnionTypeDef",
    "TableWithColumnsResourceOutputTypeDef",
    "TableWithColumnsResourceTypeDef",
    "TableWithColumnsResourceUnionTypeDef",
    "TaggedDatabaseTypeDef",
    "TaggedTableTypeDef",
    "TimestampTypeDef",
    "TransactionDescriptionTypeDef",
    "UpdateDataCellsFilterRequestRequestTypeDef",
    "UpdateLFTagExpressionRequestRequestTypeDef",
    "UpdateLFTagRequestRequestTypeDef",
    "UpdateLakeFormationIdentityCenterConfigurationRequestRequestTypeDef",
    "UpdateResourceRequestRequestTypeDef",
    "UpdateTableObjectsRequestRequestTypeDef",
    "UpdateTableStorageOptimizerRequestRequestTypeDef",
    "UpdateTableStorageOptimizerResponseTypeDef",
    "VirtualObjectTypeDef",
    "WorkUnitRangeTypeDef",
    "WriteOperationTypeDef",
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AddObjectInputTypeDef(TypedDict):
    Uri: str
    ETag: str
    Size: int
    PartitionValues: NotRequired[Sequence[str]]


class AssumeDecoratedRoleWithSAMLRequestRequestTypeDef(TypedDict):
    SAMLAssertion: str
    RoleArn: str
    PrincipalArn: str
    DurationSeconds: NotRequired[int]


class AuditContextTypeDef(TypedDict):
    AdditionalAuditContext: NotRequired[str]


class ErrorDetailTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]


class DataLakePrincipalTypeDef(TypedDict):
    DataLakePrincipalIdentifier: NotRequired[str]


class CancelTransactionRequestRequestTypeDef(TypedDict):
    TransactionId: str


class CatalogResourceTypeDef(TypedDict):
    Id: NotRequired[str]


class LFTagPairOutputTypeDef(TypedDict):
    TagKey: str
    TagValues: List[str]
    CatalogId: NotRequired[str]


class ColumnWildcardOutputTypeDef(TypedDict):
    ExcludedColumnNames: NotRequired[List[str]]


class ColumnWildcardTypeDef(TypedDict):
    ExcludedColumnNames: NotRequired[Sequence[str]]


class CommitTransactionRequestRequestTypeDef(TypedDict):
    TransactionId: str


class ConditionTypeDef(TypedDict):
    Expression: NotRequired[str]


class CreateLFTagRequestRequestTypeDef(TypedDict):
    TagKey: str
    TagValues: Sequence[str]
    CatalogId: NotRequired[str]


class ExternalFilteringConfigurationTypeDef(TypedDict):
    Status: EnableStatusType
    AuthorizedTargets: Sequence[str]


class RowFilterOutputTypeDef(TypedDict):
    FilterExpression: NotRequired[str]
    AllRowsWildcard: NotRequired[Dict[str, Any]]


class DataCellsFilterResourceTypeDef(TypedDict):
    TableCatalogId: NotRequired[str]
    DatabaseName: NotRequired[str]
    TableName: NotRequired[str]
    Name: NotRequired[str]


class DataLocationResourceTypeDef(TypedDict):
    ResourceArn: str
    CatalogId: NotRequired[str]


class DatabaseResourceTypeDef(TypedDict):
    Name: str
    CatalogId: NotRequired[str]


class DeleteDataCellsFilterRequestRequestTypeDef(TypedDict):
    TableCatalogId: NotRequired[str]
    DatabaseName: NotRequired[str]
    TableName: NotRequired[str]
    Name: NotRequired[str]


class DeleteLFTagExpressionRequestRequestTypeDef(TypedDict):
    Name: str
    CatalogId: NotRequired[str]


class DeleteLFTagRequestRequestTypeDef(TypedDict):
    TagKey: str
    CatalogId: NotRequired[str]


class DeleteLakeFormationIdentityCenterConfigurationRequestRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]


class DeleteObjectInputTypeDef(TypedDict):
    Uri: str
    ETag: NotRequired[str]
    PartitionValues: NotRequired[Sequence[str]]


class VirtualObjectTypeDef(TypedDict):
    Uri: str
    ETag: NotRequired[str]


class DeregisterResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class DescribeLakeFormationIdentityCenterConfigurationRequestRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]


class ExternalFilteringConfigurationOutputTypeDef(TypedDict):
    Status: EnableStatusType
    AuthorizedTargets: List[str]


class DescribeResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class ResourceInfoTypeDef(TypedDict):
    ResourceArn: NotRequired[str]
    RoleArn: NotRequired[str]
    LastModified: NotRequired[datetime]
    WithFederation: NotRequired[bool]
    HybridAccessEnabled: NotRequired[bool]


class DescribeTransactionRequestRequestTypeDef(TypedDict):
    TransactionId: str


class TransactionDescriptionTypeDef(TypedDict):
    TransactionId: NotRequired[str]
    TransactionStatus: NotRequired[TransactionStatusType]
    TransactionStartTime: NotRequired[datetime]
    TransactionEndTime: NotRequired[datetime]


class DetailsMapTypeDef(TypedDict):
    ResourceShare: NotRequired[List[str]]


class ExecutionStatisticsTypeDef(TypedDict):
    AverageExecutionTimeMillis: NotRequired[int]
    DataScannedBytes: NotRequired[int]
    WorkUnitsExecutedCount: NotRequired[int]


class ExtendTransactionRequestRequestTypeDef(TypedDict):
    TransactionId: NotRequired[str]


class FilterConditionTypeDef(TypedDict):
    Field: NotRequired[FieldNameStringType]
    ComparisonOperator: NotRequired[ComparisonOperatorType]
    StringValueList: NotRequired[Sequence[str]]


class GetDataCellsFilterRequestRequestTypeDef(TypedDict):
    TableCatalogId: str
    DatabaseName: str
    TableName: str
    Name: str


class GetDataLakeSettingsRequestRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]


class GetEffectivePermissionsForPathRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    CatalogId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class GetLFTagExpressionRequestRequestTypeDef(TypedDict):
    Name: str
    CatalogId: NotRequired[str]


class LFTagOutputTypeDef(TypedDict):
    TagKey: str
    TagValues: List[str]


class GetLFTagRequestRequestTypeDef(TypedDict):
    TagKey: str
    CatalogId: NotRequired[str]


class GetQueryStateRequestRequestTypeDef(TypedDict):
    QueryId: str


class GetQueryStatisticsRequestRequestTypeDef(TypedDict):
    QueryId: str


class PlanningStatisticsTypeDef(TypedDict):
    EstimatedDataToScanBytes: NotRequired[int]
    PlanningTimeMillis: NotRequired[int]
    QueueTimeMillis: NotRequired[int]
    WorkUnitsGeneratedCount: NotRequired[int]


TimestampTypeDef = Union[datetime, str]


class PartitionValueListTypeDef(TypedDict):
    Values: Sequence[str]


class GetWorkUnitResultsRequestRequestTypeDef(TypedDict):
    QueryId: str
    WorkUnitId: int
    WorkUnitToken: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetWorkUnitsRequestRequestTypeDef(TypedDict):
    QueryId: str
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]


class WorkUnitRangeTypeDef(TypedDict):
    WorkUnitIdMax: int
    WorkUnitIdMin: int
    WorkUnitToken: str


class LFTagExpressionResourceTypeDef(TypedDict):
    Name: str
    CatalogId: NotRequired[str]


class LFTagKeyResourceOutputTypeDef(TypedDict):
    TagKey: str
    TagValues: List[str]
    CatalogId: NotRequired[str]


class LFTagKeyResourceTypeDef(TypedDict):
    TagKey: str
    TagValues: Sequence[str]
    CatalogId: NotRequired[str]


class LFTagPairTypeDef(TypedDict):
    TagKey: str
    TagValues: Sequence[str]
    CatalogId: NotRequired[str]


class LFTagTypeDef(TypedDict):
    TagKey: str
    TagValues: Sequence[str]


class TableResourceTypeDef(TypedDict):
    DatabaseName: str
    CatalogId: NotRequired[str]
    Name: NotRequired[str]
    TableWildcard: NotRequired[Mapping[str, Any]]


class ListLFTagExpressionsRequestRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListLFTagsRequestRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    ResourceShareType: NotRequired[ResourceShareTypeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTableStorageOptimizersRequestRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    CatalogId: NotRequired[str]
    StorageOptimizerType: NotRequired[OptimizerTypeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class StorageOptimizerTypeDef(TypedDict):
    StorageOptimizerType: NotRequired[OptimizerTypeType]
    Config: NotRequired[Dict[str, str]]
    ErrorMessage: NotRequired[str]
    Warnings: NotRequired[str]
    LastRunDetails: NotRequired[str]


class ListTransactionsRequestRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    StatusFilter: NotRequired[TransactionStatusFilterType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class TableObjectTypeDef(TypedDict):
    Uri: NotRequired[str]
    ETag: NotRequired[str]
    Size: NotRequired[int]


class RegisterResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    UseServiceLinkedRole: NotRequired[bool]
    RoleArn: NotRequired[str]
    WithFederation: NotRequired[bool]
    HybridAccessEnabled: NotRequired[bool]


class TableResourceOutputTypeDef(TypedDict):
    DatabaseName: str
    CatalogId: NotRequired[str]
    Name: NotRequired[str]
    TableWildcard: NotRequired[Dict[str, Any]]


class RowFilterTypeDef(TypedDict):
    FilterExpression: NotRequired[str]
    AllRowsWildcard: NotRequired[Mapping[str, Any]]


class StartTransactionRequestRequestTypeDef(TypedDict):
    TransactionType: NotRequired[TransactionTypeType]


class UpdateLFTagRequestRequestTypeDef(TypedDict):
    TagKey: str
    CatalogId: NotRequired[str]
    TagValuesToDelete: NotRequired[Sequence[str]]
    TagValuesToAdd: NotRequired[Sequence[str]]


class UpdateResourceRequestRequestTypeDef(TypedDict):
    RoleArn: str
    ResourceArn: str
    WithFederation: NotRequired[bool]
    HybridAccessEnabled: NotRequired[bool]


class UpdateTableStorageOptimizerRequestRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    StorageOptimizerConfig: Mapping[OptimizerTypeType, Mapping[str, str]]
    CatalogId: NotRequired[str]


class AssumeDecoratedRoleWithSAMLResponseTypeDef(TypedDict):
    AccessKeyId: str
    SecretAccessKey: str
    SessionToken: str
    Expiration: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CommitTransactionResponseTypeDef(TypedDict):
    TransactionStatus: TransactionStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLakeFormationIdentityCenterConfigurationResponseTypeDef(TypedDict):
    ApplicationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetDataLakePrincipalResponseTypeDef(TypedDict):
    Identity: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetLFTagResponseTypeDef(TypedDict):
    CatalogId: str
    TagKey: str
    TagValues: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetQueryStateResponseTypeDef(TypedDict):
    Error: str
    State: QueryStateStringType
    ResponseMetadata: ResponseMetadataTypeDef


class GetTemporaryGluePartitionCredentialsResponseTypeDef(TypedDict):
    AccessKeyId: str
    SecretAccessKey: str
    SessionToken: str
    Expiration: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetTemporaryGlueTableCredentialsResponseTypeDef(TypedDict):
    AccessKeyId: str
    SecretAccessKey: str
    SessionToken: str
    Expiration: datetime
    VendedS3Path: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetWorkUnitResultsResponseTypeDef(TypedDict):
    ResultStream: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef


class StartQueryPlanningResponseTypeDef(TypedDict):
    QueryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartTransactionResponseTypeDef(TypedDict):
    TransactionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTableStorageOptimizerResponseTypeDef(TypedDict):
    Result: str
    ResponseMetadata: ResponseMetadataTypeDef


class PrincipalPermissionsOutputTypeDef(TypedDict):
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Permissions: NotRequired[List[PermissionType]]


class PrincipalPermissionsTypeDef(TypedDict):
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Permissions: NotRequired[Sequence[PermissionType]]


class ColumnLFTagTypeDef(TypedDict):
    Name: NotRequired[str]
    LFTags: NotRequired[List[LFTagPairOutputTypeDef]]


class LFTagErrorTypeDef(TypedDict):
    LFTag: NotRequired[LFTagPairOutputTypeDef]
    Error: NotRequired[ErrorDetailTypeDef]


class ListLFTagsResponseTypeDef(TypedDict):
    LFTags: List[LFTagPairOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TableWithColumnsResourceOutputTypeDef(TypedDict):
    DatabaseName: str
    Name: str
    CatalogId: NotRequired[str]
    ColumnNames: NotRequired[List[str]]
    ColumnWildcard: NotRequired[ColumnWildcardOutputTypeDef]


ColumnWildcardUnionTypeDef = Union[ColumnWildcardTypeDef, ColumnWildcardOutputTypeDef]


class CreateLakeFormationIdentityCenterConfigurationRequestRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    InstanceArn: NotRequired[str]
    ExternalFiltering: NotRequired[ExternalFilteringConfigurationTypeDef]
    ShareRecipients: NotRequired[Sequence[DataLakePrincipalTypeDef]]


class UpdateLakeFormationIdentityCenterConfigurationRequestRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    ShareRecipients: NotRequired[Sequence[DataLakePrincipalTypeDef]]
    ApplicationStatus: NotRequired[ApplicationStatusType]
    ExternalFiltering: NotRequired[ExternalFilteringConfigurationTypeDef]


class DataCellsFilterOutputTypeDef(TypedDict):
    TableCatalogId: str
    DatabaseName: str
    TableName: str
    Name: str
    RowFilter: NotRequired[RowFilterOutputTypeDef]
    ColumnNames: NotRequired[List[str]]
    ColumnWildcard: NotRequired[ColumnWildcardOutputTypeDef]
    VersionId: NotRequired[str]


class TaggedDatabaseTypeDef(TypedDict):
    Database: NotRequired[DatabaseResourceTypeDef]
    LFTags: NotRequired[List[LFTagPairOutputTypeDef]]


class WriteOperationTypeDef(TypedDict):
    AddObject: NotRequired[AddObjectInputTypeDef]
    DeleteObject: NotRequired[DeleteObjectInputTypeDef]


class DeleteObjectsOnCancelRequestRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    TransactionId: str
    Objects: Sequence[VirtualObjectTypeDef]
    CatalogId: NotRequired[str]


class DescribeLakeFormationIdentityCenterConfigurationResponseTypeDef(TypedDict):
    CatalogId: str
    InstanceArn: str
    ApplicationArn: str
    ExternalFiltering: ExternalFilteringConfigurationOutputTypeDef
    ShareRecipients: List[DataLakePrincipalTypeDef]
    ResourceShare: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeResourceResponseTypeDef(TypedDict):
    ResourceInfo: ResourceInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListResourcesResponseTypeDef(TypedDict):
    ResourceInfoList: List[ResourceInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeTransactionResponseTypeDef(TypedDict):
    TransactionDescription: TransactionDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTransactionsResponseTypeDef(TypedDict):
    Transactions: List[TransactionDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListResourcesRequestRequestTypeDef(TypedDict):
    FilterConditionList: NotRequired[Sequence[FilterConditionTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetLFTagExpressionResponseTypeDef(TypedDict):
    Name: str
    Description: str
    CatalogId: str
    Expression: List[LFTagOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class LFTagExpressionTypeDef(TypedDict):
    Name: NotRequired[str]
    Description: NotRequired[str]
    CatalogId: NotRequired[str]
    Expression: NotRequired[List[LFTagOutputTypeDef]]


class LFTagPolicyResourceOutputTypeDef(TypedDict):
    ResourceType: ResourceTypeType
    CatalogId: NotRequired[str]
    Expression: NotRequired[List[LFTagOutputTypeDef]]
    ExpressionName: NotRequired[str]


class GetQueryStatisticsResponseTypeDef(TypedDict):
    ExecutionStatistics: ExecutionStatisticsTypeDef
    PlanningStatistics: PlanningStatisticsTypeDef
    QuerySubmissionTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetTableObjectsRequestRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    CatalogId: NotRequired[str]
    TransactionId: NotRequired[str]
    QueryAsOfTime: NotRequired[TimestampTypeDef]
    PartitionPredicate: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class QueryPlanningContextTypeDef(TypedDict):
    DatabaseName: str
    CatalogId: NotRequired[str]
    QueryAsOfTime: NotRequired[TimestampTypeDef]
    QueryParameters: NotRequired[Mapping[str, str]]
    TransactionId: NotRequired[str]


class QuerySessionContextTypeDef(TypedDict):
    QueryId: NotRequired[str]
    QueryStartTime: NotRequired[TimestampTypeDef]
    ClusterId: NotRequired[str]
    QueryAuthorizationId: NotRequired[str]
    AdditionalContext: NotRequired[Mapping[str, str]]


class GetTemporaryGluePartitionCredentialsRequestRequestTypeDef(TypedDict):
    TableArn: str
    Partition: PartitionValueListTypeDef
    Permissions: NotRequired[Sequence[PermissionType]]
    DurationSeconds: NotRequired[int]
    AuditContext: NotRequired[AuditContextTypeDef]
    SupportedPermissionTypes: NotRequired[Sequence[PermissionTypeType]]


class GetWorkUnitsRequestGetWorkUnitsPaginateTypeDef(TypedDict):
    QueryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLFTagExpressionsRequestListLFTagExpressionsPaginateTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLFTagsRequestListLFTagsPaginateTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    ResourceShareType: NotRequired[ResourceShareTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetWorkUnitsResponseTypeDef(TypedDict):
    QueryId: str
    WorkUnitRanges: List[WorkUnitRangeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


LFTagKeyResourceUnionTypeDef = Union[LFTagKeyResourceTypeDef, LFTagKeyResourceOutputTypeDef]
LFTagPairUnionTypeDef = Union[LFTagPairTypeDef, LFTagPairOutputTypeDef]
LFTagUnionTypeDef = Union[LFTagTypeDef, LFTagOutputTypeDef]


class SearchDatabasesByLFTagsRequestRequestTypeDef(TypedDict):
    Expression: Sequence[LFTagTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CatalogId: NotRequired[str]


class SearchDatabasesByLFTagsRequestSearchDatabasesByLFTagsPaginateTypeDef(TypedDict):
    Expression: Sequence[LFTagTypeDef]
    CatalogId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchTablesByLFTagsRequestRequestTypeDef(TypedDict):
    Expression: Sequence[LFTagTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CatalogId: NotRequired[str]


class SearchTablesByLFTagsRequestSearchTablesByLFTagsPaginateTypeDef(TypedDict):
    Expression: Sequence[LFTagTypeDef]
    CatalogId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class UpdateLFTagExpressionRequestRequestTypeDef(TypedDict):
    Name: str
    Expression: Sequence[LFTagTypeDef]
    Description: NotRequired[str]
    CatalogId: NotRequired[str]


class ListDataCellsFilterRequestListDataCellsFilterPaginateTypeDef(TypedDict):
    Table: NotRequired[TableResourceTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataCellsFilterRequestRequestTypeDef(TypedDict):
    Table: NotRequired[TableResourceTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTableStorageOptimizersResponseTypeDef(TypedDict):
    StorageOptimizerList: List[StorageOptimizerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PartitionObjectsTypeDef(TypedDict):
    PartitionValues: NotRequired[List[str]]
    Objects: NotRequired[List[TableObjectTypeDef]]


TableResourceUnionTypeDef = Union[TableResourceTypeDef, TableResourceOutputTypeDef]
RowFilterUnionTypeDef = Union[RowFilterTypeDef, RowFilterOutputTypeDef]


class DataLakeSettingsOutputTypeDef(TypedDict):
    DataLakeAdmins: NotRequired[List[DataLakePrincipalTypeDef]]
    ReadOnlyAdmins: NotRequired[List[DataLakePrincipalTypeDef]]
    CreateDatabaseDefaultPermissions: NotRequired[List[PrincipalPermissionsOutputTypeDef]]
    CreateTableDefaultPermissions: NotRequired[List[PrincipalPermissionsOutputTypeDef]]
    Parameters: NotRequired[Dict[str, str]]
    TrustedResourceOwners: NotRequired[List[str]]
    AllowExternalDataFiltering: NotRequired[bool]
    AllowFullTableExternalDataAccess: NotRequired[bool]
    ExternalDataFilteringAllowList: NotRequired[List[DataLakePrincipalTypeDef]]
    AuthorizedSessionTagValueList: NotRequired[List[str]]


PrincipalPermissionsUnionTypeDef = Union[
    PrincipalPermissionsTypeDef, PrincipalPermissionsOutputTypeDef
]


class GetResourceLFTagsResponseTypeDef(TypedDict):
    LFTagOnDatabase: List[LFTagPairOutputTypeDef]
    LFTagsOnTable: List[LFTagPairOutputTypeDef]
    LFTagsOnColumns: List[ColumnLFTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TaggedTableTypeDef(TypedDict):
    Table: NotRequired[TableResourceOutputTypeDef]
    LFTagOnDatabase: NotRequired[List[LFTagPairOutputTypeDef]]
    LFTagsOnTable: NotRequired[List[LFTagPairOutputTypeDef]]
    LFTagsOnColumns: NotRequired[List[ColumnLFTagTypeDef]]


class AddLFTagsToResourceResponseTypeDef(TypedDict):
    Failures: List[LFTagErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RemoveLFTagsFromResourceResponseTypeDef(TypedDict):
    Failures: List[LFTagErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TableWithColumnsResourceTypeDef(TypedDict):
    DatabaseName: str
    Name: str
    CatalogId: NotRequired[str]
    ColumnNames: NotRequired[Sequence[str]]
    ColumnWildcard: NotRequired[ColumnWildcardUnionTypeDef]


class GetDataCellsFilterResponseTypeDef(TypedDict):
    DataCellsFilter: DataCellsFilterOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDataCellsFilterResponseTypeDef(TypedDict):
    DataCellsFilters: List[DataCellsFilterOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchDatabasesByLFTagsResponseTypeDef(TypedDict):
    DatabaseList: List[TaggedDatabaseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateTableObjectsRequestRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    WriteOperations: Sequence[WriteOperationTypeDef]
    CatalogId: NotRequired[str]
    TransactionId: NotRequired[str]


class ListLFTagExpressionsResponseTypeDef(TypedDict):
    LFTagExpressions: List[LFTagExpressionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ResourceOutputTypeDef(TypedDict):
    Catalog: NotRequired[CatalogResourceTypeDef]
    Database: NotRequired[DatabaseResourceTypeDef]
    Table: NotRequired[TableResourceOutputTypeDef]
    TableWithColumns: NotRequired[TableWithColumnsResourceOutputTypeDef]
    DataLocation: NotRequired[DataLocationResourceTypeDef]
    DataCellsFilter: NotRequired[DataCellsFilterResourceTypeDef]
    LFTag: NotRequired[LFTagKeyResourceOutputTypeDef]
    LFTagPolicy: NotRequired[LFTagPolicyResourceOutputTypeDef]
    LFTagExpression: NotRequired[LFTagExpressionResourceTypeDef]


class StartQueryPlanningRequestRequestTypeDef(TypedDict):
    QueryPlanningContext: QueryPlanningContextTypeDef
    QueryString: str


class GetTemporaryGlueTableCredentialsRequestRequestTypeDef(TypedDict):
    TableArn: str
    Permissions: NotRequired[Sequence[PermissionType]]
    DurationSeconds: NotRequired[int]
    AuditContext: NotRequired[AuditContextTypeDef]
    SupportedPermissionTypes: NotRequired[Sequence[PermissionTypeType]]
    S3Path: NotRequired[str]
    QuerySessionContext: NotRequired[QuerySessionContextTypeDef]


class CreateLFTagExpressionRequestRequestTypeDef(TypedDict):
    Name: str
    Expression: Sequence[LFTagUnionTypeDef]
    Description: NotRequired[str]
    CatalogId: NotRequired[str]


class LFTagPolicyResourceTypeDef(TypedDict):
    ResourceType: ResourceTypeType
    CatalogId: NotRequired[str]
    Expression: NotRequired[Sequence[LFTagUnionTypeDef]]
    ExpressionName: NotRequired[str]


class GetTableObjectsResponseTypeDef(TypedDict):
    Objects: List[PartitionObjectsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DataCellsFilterTypeDef(TypedDict):
    TableCatalogId: str
    DatabaseName: str
    TableName: str
    Name: str
    RowFilter: NotRequired[RowFilterUnionTypeDef]
    ColumnNames: NotRequired[Sequence[str]]
    ColumnWildcard: NotRequired[ColumnWildcardUnionTypeDef]
    VersionId: NotRequired[str]


class GetDataLakeSettingsResponseTypeDef(TypedDict):
    DataLakeSettings: DataLakeSettingsOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DataLakeSettingsTypeDef(TypedDict):
    DataLakeAdmins: NotRequired[Sequence[DataLakePrincipalTypeDef]]
    ReadOnlyAdmins: NotRequired[Sequence[DataLakePrincipalTypeDef]]
    CreateDatabaseDefaultPermissions: NotRequired[Sequence[PrincipalPermissionsUnionTypeDef]]
    CreateTableDefaultPermissions: NotRequired[Sequence[PrincipalPermissionsTypeDef]]
    Parameters: NotRequired[Mapping[str, str]]
    TrustedResourceOwners: NotRequired[Sequence[str]]
    AllowExternalDataFiltering: NotRequired[bool]
    AllowFullTableExternalDataAccess: NotRequired[bool]
    ExternalDataFilteringAllowList: NotRequired[Sequence[DataLakePrincipalTypeDef]]
    AuthorizedSessionTagValueList: NotRequired[Sequence[str]]


class SearchTablesByLFTagsResponseTypeDef(TypedDict):
    TableList: List[TaggedTableTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


TableWithColumnsResourceUnionTypeDef = Union[
    TableWithColumnsResourceTypeDef, TableWithColumnsResourceOutputTypeDef
]


class BatchPermissionsRequestEntryOutputTypeDef(TypedDict):
    Id: str
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Resource: NotRequired[ResourceOutputTypeDef]
    Permissions: NotRequired[List[PermissionType]]
    PermissionsWithGrantOption: NotRequired[List[PermissionType]]


class LakeFormationOptInsInfoTypeDef(TypedDict):
    Resource: NotRequired[ResourceOutputTypeDef]
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Condition: NotRequired[ConditionTypeDef]
    LastModified: NotRequired[datetime]
    LastUpdatedBy: NotRequired[str]


class PrincipalResourcePermissionsTypeDef(TypedDict):
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Resource: NotRequired[ResourceOutputTypeDef]
    Condition: NotRequired[ConditionTypeDef]
    Permissions: NotRequired[List[PermissionType]]
    PermissionsWithGrantOption: NotRequired[List[PermissionType]]
    AdditionalDetails: NotRequired[DetailsMapTypeDef]
    LastUpdated: NotRequired[datetime]
    LastUpdatedBy: NotRequired[str]


LFTagPolicyResourceUnionTypeDef = Union[
    LFTagPolicyResourceTypeDef, LFTagPolicyResourceOutputTypeDef
]


class CreateDataCellsFilterRequestRequestTypeDef(TypedDict):
    TableData: DataCellsFilterTypeDef


class UpdateDataCellsFilterRequestRequestTypeDef(TypedDict):
    TableData: DataCellsFilterTypeDef


class PutDataLakeSettingsRequestRequestTypeDef(TypedDict):
    DataLakeSettings: DataLakeSettingsTypeDef
    CatalogId: NotRequired[str]


class BatchPermissionsFailureEntryTypeDef(TypedDict):
    RequestEntry: NotRequired[BatchPermissionsRequestEntryOutputTypeDef]
    Error: NotRequired[ErrorDetailTypeDef]


class ListLakeFormationOptInsResponseTypeDef(TypedDict):
    LakeFormationOptInsInfoList: List[LakeFormationOptInsInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetEffectivePermissionsForPathResponseTypeDef(TypedDict):
    Permissions: List[PrincipalResourcePermissionsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPermissionsResponseTypeDef(TypedDict):
    PrincipalResourcePermissions: List[PrincipalResourcePermissionsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ResourceTypeDef(TypedDict):
    Catalog: NotRequired[CatalogResourceTypeDef]
    Database: NotRequired[DatabaseResourceTypeDef]
    Table: NotRequired[TableResourceUnionTypeDef]
    TableWithColumns: NotRequired[TableWithColumnsResourceUnionTypeDef]
    DataLocation: NotRequired[DataLocationResourceTypeDef]
    DataCellsFilter: NotRequired[DataCellsFilterResourceTypeDef]
    LFTag: NotRequired[LFTagKeyResourceUnionTypeDef]
    LFTagPolicy: NotRequired[LFTagPolicyResourceUnionTypeDef]
    LFTagExpression: NotRequired[LFTagExpressionResourceTypeDef]


class BatchGrantPermissionsResponseTypeDef(TypedDict):
    Failures: List[BatchPermissionsFailureEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchRevokePermissionsResponseTypeDef(TypedDict):
    Failures: List[BatchPermissionsFailureEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AddLFTagsToResourceRequestRequestTypeDef(TypedDict):
    Resource: ResourceTypeDef
    LFTags: Sequence[LFTagPairUnionTypeDef]
    CatalogId: NotRequired[str]


class CreateLakeFormationOptInRequestRequestTypeDef(TypedDict):
    Principal: DataLakePrincipalTypeDef
    Resource: ResourceTypeDef


class DeleteLakeFormationOptInRequestRequestTypeDef(TypedDict):
    Principal: DataLakePrincipalTypeDef
    Resource: ResourceTypeDef


class GetResourceLFTagsRequestRequestTypeDef(TypedDict):
    Resource: ResourceTypeDef
    CatalogId: NotRequired[str]
    ShowAssignedLFTags: NotRequired[bool]


class GrantPermissionsRequestRequestTypeDef(TypedDict):
    Principal: DataLakePrincipalTypeDef
    Resource: ResourceTypeDef
    Permissions: Sequence[PermissionType]
    CatalogId: NotRequired[str]
    PermissionsWithGrantOption: NotRequired[Sequence[PermissionType]]


class ListLakeFormationOptInsRequestRequestTypeDef(TypedDict):
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Resource: NotRequired[ResourceTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListPermissionsRequestRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    Principal: NotRequired[DataLakePrincipalTypeDef]
    ResourceType: NotRequired[DataLakeResourceTypeType]
    Resource: NotRequired[ResourceTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    IncludeRelated: NotRequired[str]


class RemoveLFTagsFromResourceRequestRequestTypeDef(TypedDict):
    Resource: ResourceTypeDef
    LFTags: Sequence[LFTagPairTypeDef]
    CatalogId: NotRequired[str]


ResourceUnionTypeDef = Union[ResourceTypeDef, ResourceOutputTypeDef]


class RevokePermissionsRequestRequestTypeDef(TypedDict):
    Principal: DataLakePrincipalTypeDef
    Resource: ResourceTypeDef
    Permissions: Sequence[PermissionType]
    CatalogId: NotRequired[str]
    PermissionsWithGrantOption: NotRequired[Sequence[PermissionType]]


class BatchPermissionsRequestEntryTypeDef(TypedDict):
    Id: str
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Resource: NotRequired[ResourceUnionTypeDef]
    Permissions: NotRequired[Sequence[PermissionType]]
    PermissionsWithGrantOption: NotRequired[Sequence[PermissionType]]


BatchPermissionsRequestEntryUnionTypeDef = Union[
    BatchPermissionsRequestEntryTypeDef, BatchPermissionsRequestEntryOutputTypeDef
]


class BatchRevokePermissionsRequestRequestTypeDef(TypedDict):
    Entries: Sequence[BatchPermissionsRequestEntryTypeDef]
    CatalogId: NotRequired[str]


class BatchGrantPermissionsRequestRequestTypeDef(TypedDict):
    Entries: Sequence[BatchPermissionsRequestEntryUnionTypeDef]
    CatalogId: NotRequired[str]
