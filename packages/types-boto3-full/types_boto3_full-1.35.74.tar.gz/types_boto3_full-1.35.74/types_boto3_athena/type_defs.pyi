"""
Type annotations for athena service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_athena/type_defs/)

Usage::

    ```python
    from types_boto3_athena.type_defs import AclConfigurationTypeDef

    data: AclConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    CalculationExecutionStateType,
    CapacityAllocationStatusType,
    CapacityReservationStatusType,
    ColumnNullableType,
    ConnectionTypeType,
    DataCatalogStatusType,
    DataCatalogTypeType,
    EncryptionOptionType,
    ExecutorStateType,
    ExecutorTypeType,
    QueryExecutionStateType,
    SessionStateType,
    StatementTypeType,
    WorkGroupStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AclConfigurationTypeDef",
    "ApplicationDPUSizesTypeDef",
    "AthenaErrorTypeDef",
    "BatchGetNamedQueryInputRequestTypeDef",
    "BatchGetNamedQueryOutputTypeDef",
    "BatchGetPreparedStatementInputRequestTypeDef",
    "BatchGetPreparedStatementOutputTypeDef",
    "BatchGetQueryExecutionInputRequestTypeDef",
    "BatchGetQueryExecutionOutputTypeDef",
    "CalculationConfigurationTypeDef",
    "CalculationResultTypeDef",
    "CalculationStatisticsTypeDef",
    "CalculationStatusTypeDef",
    "CalculationSummaryTypeDef",
    "CancelCapacityReservationInputRequestTypeDef",
    "CapacityAllocationTypeDef",
    "CapacityAssignmentConfigurationTypeDef",
    "CapacityAssignmentOutputTypeDef",
    "CapacityAssignmentTypeDef",
    "CapacityAssignmentUnionTypeDef",
    "CapacityReservationTypeDef",
    "ColumnInfoTypeDef",
    "ColumnTypeDef",
    "CreateCapacityReservationInputRequestTypeDef",
    "CreateDataCatalogInputRequestTypeDef",
    "CreateDataCatalogOutputTypeDef",
    "CreateNamedQueryInputRequestTypeDef",
    "CreateNamedQueryOutputTypeDef",
    "CreateNotebookInputRequestTypeDef",
    "CreateNotebookOutputTypeDef",
    "CreatePreparedStatementInputRequestTypeDef",
    "CreatePresignedNotebookUrlRequestRequestTypeDef",
    "CreatePresignedNotebookUrlResponseTypeDef",
    "CreateWorkGroupInputRequestTypeDef",
    "CustomerContentEncryptionConfigurationTypeDef",
    "DataCatalogSummaryTypeDef",
    "DataCatalogTypeDef",
    "DatabaseTypeDef",
    "DatumTypeDef",
    "DeleteCapacityReservationInputRequestTypeDef",
    "DeleteDataCatalogInputRequestTypeDef",
    "DeleteDataCatalogOutputTypeDef",
    "DeleteNamedQueryInputRequestTypeDef",
    "DeleteNotebookInputRequestTypeDef",
    "DeletePreparedStatementInputRequestTypeDef",
    "DeleteWorkGroupInputRequestTypeDef",
    "EncryptionConfigurationTypeDef",
    "EngineConfigurationOutputTypeDef",
    "EngineConfigurationTypeDef",
    "EngineVersionTypeDef",
    "ExecutorsSummaryTypeDef",
    "ExportNotebookInputRequestTypeDef",
    "ExportNotebookOutputTypeDef",
    "FilterDefinitionTypeDef",
    "GetCalculationExecutionCodeRequestRequestTypeDef",
    "GetCalculationExecutionCodeResponseTypeDef",
    "GetCalculationExecutionRequestRequestTypeDef",
    "GetCalculationExecutionResponseTypeDef",
    "GetCalculationExecutionStatusRequestRequestTypeDef",
    "GetCalculationExecutionStatusResponseTypeDef",
    "GetCapacityAssignmentConfigurationInputRequestTypeDef",
    "GetCapacityAssignmentConfigurationOutputTypeDef",
    "GetCapacityReservationInputRequestTypeDef",
    "GetCapacityReservationOutputTypeDef",
    "GetDataCatalogInputRequestTypeDef",
    "GetDataCatalogOutputTypeDef",
    "GetDatabaseInputRequestTypeDef",
    "GetDatabaseOutputTypeDef",
    "GetNamedQueryInputRequestTypeDef",
    "GetNamedQueryOutputTypeDef",
    "GetNotebookMetadataInputRequestTypeDef",
    "GetNotebookMetadataOutputTypeDef",
    "GetPreparedStatementInputRequestTypeDef",
    "GetPreparedStatementOutputTypeDef",
    "GetQueryExecutionInputRequestTypeDef",
    "GetQueryExecutionOutputTypeDef",
    "GetQueryResultsInputGetQueryResultsPaginateTypeDef",
    "GetQueryResultsInputRequestTypeDef",
    "GetQueryResultsOutputTypeDef",
    "GetQueryRuntimeStatisticsInputRequestTypeDef",
    "GetQueryRuntimeStatisticsOutputTypeDef",
    "GetSessionRequestRequestTypeDef",
    "GetSessionResponseTypeDef",
    "GetSessionStatusRequestRequestTypeDef",
    "GetSessionStatusResponseTypeDef",
    "GetTableMetadataInputRequestTypeDef",
    "GetTableMetadataOutputTypeDef",
    "GetWorkGroupInputRequestTypeDef",
    "GetWorkGroupOutputTypeDef",
    "IdentityCenterConfigurationTypeDef",
    "ImportNotebookInputRequestTypeDef",
    "ImportNotebookOutputTypeDef",
    "ListApplicationDPUSizesInputRequestTypeDef",
    "ListApplicationDPUSizesOutputTypeDef",
    "ListCalculationExecutionsRequestRequestTypeDef",
    "ListCalculationExecutionsResponseTypeDef",
    "ListCapacityReservationsInputRequestTypeDef",
    "ListCapacityReservationsOutputTypeDef",
    "ListDataCatalogsInputListDataCatalogsPaginateTypeDef",
    "ListDataCatalogsInputRequestTypeDef",
    "ListDataCatalogsOutputTypeDef",
    "ListDatabasesInputListDatabasesPaginateTypeDef",
    "ListDatabasesInputRequestTypeDef",
    "ListDatabasesOutputTypeDef",
    "ListEngineVersionsInputRequestTypeDef",
    "ListEngineVersionsOutputTypeDef",
    "ListExecutorsRequestRequestTypeDef",
    "ListExecutorsResponseTypeDef",
    "ListNamedQueriesInputListNamedQueriesPaginateTypeDef",
    "ListNamedQueriesInputRequestTypeDef",
    "ListNamedQueriesOutputTypeDef",
    "ListNotebookMetadataInputRequestTypeDef",
    "ListNotebookMetadataOutputTypeDef",
    "ListNotebookSessionsRequestRequestTypeDef",
    "ListNotebookSessionsResponseTypeDef",
    "ListPreparedStatementsInputRequestTypeDef",
    "ListPreparedStatementsOutputTypeDef",
    "ListQueryExecutionsInputListQueryExecutionsPaginateTypeDef",
    "ListQueryExecutionsInputRequestTypeDef",
    "ListQueryExecutionsOutputTypeDef",
    "ListSessionsRequestRequestTypeDef",
    "ListSessionsResponseTypeDef",
    "ListTableMetadataInputListTableMetadataPaginateTypeDef",
    "ListTableMetadataInputRequestTypeDef",
    "ListTableMetadataOutputTypeDef",
    "ListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListWorkGroupsInputRequestTypeDef",
    "ListWorkGroupsOutputTypeDef",
    "NamedQueryTypeDef",
    "NotebookMetadataTypeDef",
    "NotebookSessionSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "PreparedStatementSummaryTypeDef",
    "PreparedStatementTypeDef",
    "PutCapacityAssignmentConfigurationInputRequestTypeDef",
    "QueryExecutionContextTypeDef",
    "QueryExecutionStatisticsTypeDef",
    "QueryExecutionStatusTypeDef",
    "QueryExecutionTypeDef",
    "QueryResultsS3AccessGrantsConfigurationTypeDef",
    "QueryRuntimeStatisticsRowsTypeDef",
    "QueryRuntimeStatisticsTimelineTypeDef",
    "QueryRuntimeStatisticsTypeDef",
    "QueryStagePlanNodeTypeDef",
    "QueryStageTypeDef",
    "ResponseMetadataTypeDef",
    "ResultConfigurationTypeDef",
    "ResultConfigurationUpdatesTypeDef",
    "ResultReuseByAgeConfigurationTypeDef",
    "ResultReuseConfigurationTypeDef",
    "ResultReuseInformationTypeDef",
    "ResultSetMetadataTypeDef",
    "ResultSetTypeDef",
    "RowTypeDef",
    "SessionConfigurationTypeDef",
    "SessionStatisticsTypeDef",
    "SessionStatusTypeDef",
    "SessionSummaryTypeDef",
    "StartCalculationExecutionRequestRequestTypeDef",
    "StartCalculationExecutionResponseTypeDef",
    "StartQueryExecutionInputRequestTypeDef",
    "StartQueryExecutionOutputTypeDef",
    "StartSessionRequestRequestTypeDef",
    "StartSessionResponseTypeDef",
    "StopCalculationExecutionRequestRequestTypeDef",
    "StopCalculationExecutionResponseTypeDef",
    "StopQueryExecutionInputRequestTypeDef",
    "TableMetadataTypeDef",
    "TagResourceInputRequestTypeDef",
    "TagTypeDef",
    "TerminateSessionRequestRequestTypeDef",
    "TerminateSessionResponseTypeDef",
    "UnprocessedNamedQueryIdTypeDef",
    "UnprocessedPreparedStatementNameTypeDef",
    "UnprocessedQueryExecutionIdTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateCapacityReservationInputRequestTypeDef",
    "UpdateDataCatalogInputRequestTypeDef",
    "UpdateNamedQueryInputRequestTypeDef",
    "UpdateNotebookInputRequestTypeDef",
    "UpdateNotebookMetadataInputRequestTypeDef",
    "UpdatePreparedStatementInputRequestTypeDef",
    "UpdateWorkGroupInputRequestTypeDef",
    "WorkGroupConfigurationTypeDef",
    "WorkGroupConfigurationUpdatesTypeDef",
    "WorkGroupSummaryTypeDef",
    "WorkGroupTypeDef",
)

class AclConfigurationTypeDef(TypedDict):
    S3AclOption: Literal["BUCKET_OWNER_FULL_CONTROL"]

class ApplicationDPUSizesTypeDef(TypedDict):
    ApplicationRuntimeId: NotRequired[str]
    SupportedDPUSizes: NotRequired[List[int]]

class AthenaErrorTypeDef(TypedDict):
    ErrorCategory: NotRequired[int]
    ErrorType: NotRequired[int]
    Retryable: NotRequired[bool]
    ErrorMessage: NotRequired[str]

class BatchGetNamedQueryInputRequestTypeDef(TypedDict):
    NamedQueryIds: Sequence[str]

class NamedQueryTypeDef(TypedDict):
    Name: str
    Database: str
    QueryString: str
    Description: NotRequired[str]
    NamedQueryId: NotRequired[str]
    WorkGroup: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class UnprocessedNamedQueryIdTypeDef(TypedDict):
    NamedQueryId: NotRequired[str]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]

class BatchGetPreparedStatementInputRequestTypeDef(TypedDict):
    PreparedStatementNames: Sequence[str]
    WorkGroup: str

class PreparedStatementTypeDef(TypedDict):
    StatementName: NotRequired[str]
    QueryStatement: NotRequired[str]
    WorkGroupName: NotRequired[str]
    Description: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]

class UnprocessedPreparedStatementNameTypeDef(TypedDict):
    StatementName: NotRequired[str]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]

class BatchGetQueryExecutionInputRequestTypeDef(TypedDict):
    QueryExecutionIds: Sequence[str]

class UnprocessedQueryExecutionIdTypeDef(TypedDict):
    QueryExecutionId: NotRequired[str]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]

class CalculationConfigurationTypeDef(TypedDict):
    CodeBlock: NotRequired[str]

class CalculationResultTypeDef(TypedDict):
    StdOutS3Uri: NotRequired[str]
    StdErrorS3Uri: NotRequired[str]
    ResultS3Uri: NotRequired[str]
    ResultType: NotRequired[str]

class CalculationStatisticsTypeDef(TypedDict):
    DpuExecutionInMillis: NotRequired[int]
    Progress: NotRequired[str]

class CalculationStatusTypeDef(TypedDict):
    SubmissionDateTime: NotRequired[datetime]
    CompletionDateTime: NotRequired[datetime]
    State: NotRequired[CalculationExecutionStateType]
    StateChangeReason: NotRequired[str]

class CancelCapacityReservationInputRequestTypeDef(TypedDict):
    Name: str

class CapacityAllocationTypeDef(TypedDict):
    Status: CapacityAllocationStatusType
    RequestTime: datetime
    StatusMessage: NotRequired[str]
    RequestCompletionTime: NotRequired[datetime]

class CapacityAssignmentOutputTypeDef(TypedDict):
    WorkGroupNames: NotRequired[List[str]]

class CapacityAssignmentTypeDef(TypedDict):
    WorkGroupNames: NotRequired[Sequence[str]]

ColumnInfoTypeDef = TypedDict(
    "ColumnInfoTypeDef",
    {
        "Name": str,
        "Type": str,
        "CatalogName": NotRequired[str],
        "SchemaName": NotRequired[str],
        "TableName": NotRequired[str],
        "Label": NotRequired[str],
        "Precision": NotRequired[int],
        "Scale": NotRequired[int],
        "Nullable": NotRequired[ColumnNullableType],
        "CaseSensitive": NotRequired[bool],
    },
)
ColumnTypeDef = TypedDict(
    "ColumnTypeDef",
    {
        "Name": str,
        "Type": NotRequired[str],
        "Comment": NotRequired[str],
    },
)

class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

DataCatalogTypeDef = TypedDict(
    "DataCatalogTypeDef",
    {
        "Name": str,
        "Type": DataCatalogTypeType,
        "Description": NotRequired[str],
        "Parameters": NotRequired[Dict[str, str]],
        "Status": NotRequired[DataCatalogStatusType],
        "ConnectionType": NotRequired[ConnectionTypeType],
        "Error": NotRequired[str],
    },
)

class CreateNamedQueryInputRequestTypeDef(TypedDict):
    Name: str
    Database: str
    QueryString: str
    Description: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    WorkGroup: NotRequired[str]

class CreateNotebookInputRequestTypeDef(TypedDict):
    WorkGroup: str
    Name: str
    ClientRequestToken: NotRequired[str]

class CreatePreparedStatementInputRequestTypeDef(TypedDict):
    StatementName: str
    WorkGroup: str
    QueryStatement: str
    Description: NotRequired[str]

class CreatePresignedNotebookUrlRequestRequestTypeDef(TypedDict):
    SessionId: str

class CustomerContentEncryptionConfigurationTypeDef(TypedDict):
    KmsKey: str

DataCatalogSummaryTypeDef = TypedDict(
    "DataCatalogSummaryTypeDef",
    {
        "CatalogName": NotRequired[str],
        "Type": NotRequired[DataCatalogTypeType],
        "Status": NotRequired[DataCatalogStatusType],
        "ConnectionType": NotRequired[ConnectionTypeType],
        "Error": NotRequired[str],
    },
)

class DatabaseTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    Parameters: NotRequired[Dict[str, str]]

class DatumTypeDef(TypedDict):
    VarCharValue: NotRequired[str]

class DeleteCapacityReservationInputRequestTypeDef(TypedDict):
    Name: str

class DeleteDataCatalogInputRequestTypeDef(TypedDict):
    Name: str
    DeleteCatalogOnly: NotRequired[bool]

class DeleteNamedQueryInputRequestTypeDef(TypedDict):
    NamedQueryId: str

class DeleteNotebookInputRequestTypeDef(TypedDict):
    NotebookId: str

class DeletePreparedStatementInputRequestTypeDef(TypedDict):
    StatementName: str
    WorkGroup: str

class DeleteWorkGroupInputRequestTypeDef(TypedDict):
    WorkGroup: str
    RecursiveDeleteOption: NotRequired[bool]

class EncryptionConfigurationTypeDef(TypedDict):
    EncryptionOption: EncryptionOptionType
    KmsKey: NotRequired[str]

class EngineConfigurationOutputTypeDef(TypedDict):
    MaxConcurrentDpus: int
    CoordinatorDpuSize: NotRequired[int]
    DefaultExecutorDpuSize: NotRequired[int]
    AdditionalConfigs: NotRequired[Dict[str, str]]
    SparkProperties: NotRequired[Dict[str, str]]

class EngineConfigurationTypeDef(TypedDict):
    MaxConcurrentDpus: int
    CoordinatorDpuSize: NotRequired[int]
    DefaultExecutorDpuSize: NotRequired[int]
    AdditionalConfigs: NotRequired[Mapping[str, str]]
    SparkProperties: NotRequired[Mapping[str, str]]

class EngineVersionTypeDef(TypedDict):
    SelectedEngineVersion: NotRequired[str]
    EffectiveEngineVersion: NotRequired[str]

class ExecutorsSummaryTypeDef(TypedDict):
    ExecutorId: str
    ExecutorType: NotRequired[ExecutorTypeType]
    StartDateTime: NotRequired[int]
    TerminationDateTime: NotRequired[int]
    ExecutorState: NotRequired[ExecutorStateType]
    ExecutorSize: NotRequired[int]

class ExportNotebookInputRequestTypeDef(TypedDict):
    NotebookId: str

NotebookMetadataTypeDef = TypedDict(
    "NotebookMetadataTypeDef",
    {
        "NotebookId": NotRequired[str],
        "Name": NotRequired[str],
        "WorkGroup": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "Type": NotRequired[Literal["IPYNB"]],
        "LastModifiedTime": NotRequired[datetime],
    },
)

class FilterDefinitionTypeDef(TypedDict):
    Name: NotRequired[str]

class GetCalculationExecutionCodeRequestRequestTypeDef(TypedDict):
    CalculationExecutionId: str

class GetCalculationExecutionRequestRequestTypeDef(TypedDict):
    CalculationExecutionId: str

class GetCalculationExecutionStatusRequestRequestTypeDef(TypedDict):
    CalculationExecutionId: str

class GetCapacityAssignmentConfigurationInputRequestTypeDef(TypedDict):
    CapacityReservationName: str

class GetCapacityReservationInputRequestTypeDef(TypedDict):
    Name: str

class GetDataCatalogInputRequestTypeDef(TypedDict):
    Name: str
    WorkGroup: NotRequired[str]

class GetDatabaseInputRequestTypeDef(TypedDict):
    CatalogName: str
    DatabaseName: str
    WorkGroup: NotRequired[str]

class GetNamedQueryInputRequestTypeDef(TypedDict):
    NamedQueryId: str

class GetNotebookMetadataInputRequestTypeDef(TypedDict):
    NotebookId: str

class GetPreparedStatementInputRequestTypeDef(TypedDict):
    StatementName: str
    WorkGroup: str

class GetQueryExecutionInputRequestTypeDef(TypedDict):
    QueryExecutionId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetQueryResultsInputRequestTypeDef(TypedDict):
    QueryExecutionId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class GetQueryRuntimeStatisticsInputRequestTypeDef(TypedDict):
    QueryExecutionId: str

class GetSessionRequestRequestTypeDef(TypedDict):
    SessionId: str

class SessionStatisticsTypeDef(TypedDict):
    DpuExecutionInMillis: NotRequired[int]

class SessionStatusTypeDef(TypedDict):
    StartDateTime: NotRequired[datetime]
    LastModifiedDateTime: NotRequired[datetime]
    EndDateTime: NotRequired[datetime]
    IdleSinceDateTime: NotRequired[datetime]
    State: NotRequired[SessionStateType]
    StateChangeReason: NotRequired[str]

class GetSessionStatusRequestRequestTypeDef(TypedDict):
    SessionId: str

class GetTableMetadataInputRequestTypeDef(TypedDict):
    CatalogName: str
    DatabaseName: str
    TableName: str
    WorkGroup: NotRequired[str]

class GetWorkGroupInputRequestTypeDef(TypedDict):
    WorkGroup: str

class IdentityCenterConfigurationTypeDef(TypedDict):
    EnableIdentityCenter: NotRequired[bool]
    IdentityCenterInstanceArn: NotRequired[str]

ImportNotebookInputRequestTypeDef = TypedDict(
    "ImportNotebookInputRequestTypeDef",
    {
        "WorkGroup": str,
        "Name": str,
        "Type": Literal["IPYNB"],
        "Payload": NotRequired[str],
        "NotebookS3LocationUri": NotRequired[str],
        "ClientRequestToken": NotRequired[str],
    },
)

class ListApplicationDPUSizesInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCalculationExecutionsRequestRequestTypeDef(TypedDict):
    SessionId: str
    StateFilter: NotRequired[CalculationExecutionStateType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCapacityReservationsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListDataCatalogsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    WorkGroup: NotRequired[str]

class ListDatabasesInputRequestTypeDef(TypedDict):
    CatalogName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    WorkGroup: NotRequired[str]

class ListEngineVersionsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListExecutorsRequestRequestTypeDef(TypedDict):
    SessionId: str
    ExecutorStateFilter: NotRequired[ExecutorStateType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListNamedQueriesInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    WorkGroup: NotRequired[str]

class ListNotebookSessionsRequestRequestTypeDef(TypedDict):
    NotebookId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class NotebookSessionSummaryTypeDef(TypedDict):
    SessionId: NotRequired[str]
    CreationTime: NotRequired[datetime]

class ListPreparedStatementsInputRequestTypeDef(TypedDict):
    WorkGroup: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class PreparedStatementSummaryTypeDef(TypedDict):
    StatementName: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]

class ListQueryExecutionsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    WorkGroup: NotRequired[str]

class ListSessionsRequestRequestTypeDef(TypedDict):
    WorkGroup: str
    StateFilter: NotRequired[SessionStateType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTableMetadataInputRequestTypeDef(TypedDict):
    CatalogName: str
    DatabaseName: str
    Expression: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    WorkGroup: NotRequired[str]

class ListTagsForResourceInputRequestTypeDef(TypedDict):
    ResourceARN: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListWorkGroupsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class QueryExecutionContextTypeDef(TypedDict):
    Database: NotRequired[str]
    Catalog: NotRequired[str]

class ResultReuseInformationTypeDef(TypedDict):
    ReusedPreviousResult: bool

class QueryResultsS3AccessGrantsConfigurationTypeDef(TypedDict):
    EnableS3AccessGrants: bool
    AuthenticationType: Literal["DIRECTORY_IDENTITY"]
    CreateUserLevelPrefix: NotRequired[bool]

class QueryRuntimeStatisticsRowsTypeDef(TypedDict):
    InputRows: NotRequired[int]
    InputBytes: NotRequired[int]
    OutputBytes: NotRequired[int]
    OutputRows: NotRequired[int]

class QueryRuntimeStatisticsTimelineTypeDef(TypedDict):
    QueryQueueTimeInMillis: NotRequired[int]
    ServicePreProcessingTimeInMillis: NotRequired[int]
    QueryPlanningTimeInMillis: NotRequired[int]
    EngineExecutionTimeInMillis: NotRequired[int]
    ServiceProcessingTimeInMillis: NotRequired[int]
    TotalExecutionTimeInMillis: NotRequired[int]

class QueryStagePlanNodeTypeDef(TypedDict):
    Name: NotRequired[str]
    Identifier: NotRequired[str]
    Children: NotRequired[List[Dict[str, Any]]]
    RemoteSources: NotRequired[List[str]]

class ResultReuseByAgeConfigurationTypeDef(TypedDict):
    Enabled: bool
    MaxAgeInMinutes: NotRequired[int]

class StopCalculationExecutionRequestRequestTypeDef(TypedDict):
    CalculationExecutionId: str

class StopQueryExecutionInputRequestTypeDef(TypedDict):
    QueryExecutionId: str

class TerminateSessionRequestRequestTypeDef(TypedDict):
    SessionId: str

class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]

class UpdateCapacityReservationInputRequestTypeDef(TypedDict):
    TargetDpus: int
    Name: str

UpdateDataCatalogInputRequestTypeDef = TypedDict(
    "UpdateDataCatalogInputRequestTypeDef",
    {
        "Name": str,
        "Type": DataCatalogTypeType,
        "Description": NotRequired[str],
        "Parameters": NotRequired[Mapping[str, str]],
    },
)

class UpdateNamedQueryInputRequestTypeDef(TypedDict):
    NamedQueryId: str
    Name: str
    QueryString: str
    Description: NotRequired[str]

UpdateNotebookInputRequestTypeDef = TypedDict(
    "UpdateNotebookInputRequestTypeDef",
    {
        "NotebookId": str,
        "Payload": str,
        "Type": Literal["IPYNB"],
        "SessionId": NotRequired[str],
        "ClientRequestToken": NotRequired[str],
    },
)

class UpdateNotebookMetadataInputRequestTypeDef(TypedDict):
    NotebookId: str
    Name: str
    ClientRequestToken: NotRequired[str]

class UpdatePreparedStatementInputRequestTypeDef(TypedDict):
    StatementName: str
    WorkGroup: str
    QueryStatement: str
    Description: NotRequired[str]

class QueryExecutionStatusTypeDef(TypedDict):
    State: NotRequired[QueryExecutionStateType]
    StateChangeReason: NotRequired[str]
    SubmissionDateTime: NotRequired[datetime]
    CompletionDateTime: NotRequired[datetime]
    AthenaError: NotRequired[AthenaErrorTypeDef]

class CreateNamedQueryOutputTypeDef(TypedDict):
    NamedQueryId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateNotebookOutputTypeDef(TypedDict):
    NotebookId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePresignedNotebookUrlResponseTypeDef(TypedDict):
    NotebookUrl: str
    AuthToken: str
    AuthTokenExpirationTime: int
    ResponseMetadata: ResponseMetadataTypeDef

class GetCalculationExecutionCodeResponseTypeDef(TypedDict):
    CodeBlock: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetNamedQueryOutputTypeDef(TypedDict):
    NamedQuery: NamedQueryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ImportNotebookOutputTypeDef(TypedDict):
    NotebookId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListApplicationDPUSizesOutputTypeDef(TypedDict):
    ApplicationDPUSizes: List[ApplicationDPUSizesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListNamedQueriesOutputTypeDef(TypedDict):
    NamedQueryIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListQueryExecutionsOutputTypeDef(TypedDict):
    QueryExecutionIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StartCalculationExecutionResponseTypeDef(TypedDict):
    CalculationExecutionId: str
    State: CalculationExecutionStateType
    ResponseMetadata: ResponseMetadataTypeDef

class StartQueryExecutionOutputTypeDef(TypedDict):
    QueryExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartSessionResponseTypeDef(TypedDict):
    SessionId: str
    State: SessionStateType
    ResponseMetadata: ResponseMetadataTypeDef

class StopCalculationExecutionResponseTypeDef(TypedDict):
    State: CalculationExecutionStateType
    ResponseMetadata: ResponseMetadataTypeDef

class TerminateSessionResponseTypeDef(TypedDict):
    State: SessionStateType
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetNamedQueryOutputTypeDef(TypedDict):
    NamedQueries: List[NamedQueryTypeDef]
    UnprocessedNamedQueryIds: List[UnprocessedNamedQueryIdTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetPreparedStatementOutputTypeDef(TypedDict):
    PreparedStatement: PreparedStatementTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetPreparedStatementOutputTypeDef(TypedDict):
    PreparedStatements: List[PreparedStatementTypeDef]
    UnprocessedPreparedStatementNames: List[UnprocessedPreparedStatementNameTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartCalculationExecutionRequestRequestTypeDef(TypedDict):
    SessionId: str
    Description: NotRequired[str]
    CalculationConfiguration: NotRequired[CalculationConfigurationTypeDef]
    CodeBlock: NotRequired[str]
    ClientRequestToken: NotRequired[str]

class CalculationSummaryTypeDef(TypedDict):
    CalculationExecutionId: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[CalculationStatusTypeDef]

class GetCalculationExecutionResponseTypeDef(TypedDict):
    CalculationExecutionId: str
    SessionId: str
    Description: str
    WorkingDirectory: str
    Status: CalculationStatusTypeDef
    Statistics: CalculationStatisticsTypeDef
    Result: CalculationResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetCalculationExecutionStatusResponseTypeDef(TypedDict):
    Status: CalculationStatusTypeDef
    Statistics: CalculationStatisticsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CapacityReservationTypeDef(TypedDict):
    Name: str
    Status: CapacityReservationStatusType
    TargetDpus: int
    AllocatedDpus: int
    CreationTime: datetime
    LastAllocation: NotRequired[CapacityAllocationTypeDef]
    LastSuccessfulAllocationTime: NotRequired[datetime]

class CapacityAssignmentConfigurationTypeDef(TypedDict):
    CapacityReservationName: NotRequired[str]
    CapacityAssignments: NotRequired[List[CapacityAssignmentOutputTypeDef]]

CapacityAssignmentUnionTypeDef = Union[CapacityAssignmentTypeDef, CapacityAssignmentOutputTypeDef]

class ResultSetMetadataTypeDef(TypedDict):
    ColumnInfo: NotRequired[List[ColumnInfoTypeDef]]

class TableMetadataTypeDef(TypedDict):
    Name: str
    CreateTime: NotRequired[datetime]
    LastAccessTime: NotRequired[datetime]
    TableType: NotRequired[str]
    Columns: NotRequired[List[ColumnTypeDef]]
    PartitionKeys: NotRequired[List[ColumnTypeDef]]
    Parameters: NotRequired[Dict[str, str]]

class CreateCapacityReservationInputRequestTypeDef(TypedDict):
    TargetDpus: int
    Name: str
    Tags: NotRequired[Sequence[TagTypeDef]]

CreateDataCatalogInputRequestTypeDef = TypedDict(
    "CreateDataCatalogInputRequestTypeDef",
    {
        "Name": str,
        "Type": DataCatalogTypeType,
        "Description": NotRequired[str],
        "Parameters": NotRequired[Mapping[str, str]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TagResourceInputRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]

class CreateDataCatalogOutputTypeDef(TypedDict):
    DataCatalog: DataCatalogTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDataCatalogOutputTypeDef(TypedDict):
    DataCatalog: DataCatalogTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetDataCatalogOutputTypeDef(TypedDict):
    DataCatalog: DataCatalogTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDataCatalogsOutputTypeDef(TypedDict):
    DataCatalogsSummary: List[DataCatalogSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetDatabaseOutputTypeDef(TypedDict):
    Database: DatabaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDatabasesOutputTypeDef(TypedDict):
    DatabaseList: List[DatabaseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RowTypeDef(TypedDict):
    Data: NotRequired[List[DatumTypeDef]]

class ResultConfigurationTypeDef(TypedDict):
    OutputLocation: NotRequired[str]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    ExpectedBucketOwner: NotRequired[str]
    AclConfiguration: NotRequired[AclConfigurationTypeDef]

class ResultConfigurationUpdatesTypeDef(TypedDict):
    OutputLocation: NotRequired[str]
    RemoveOutputLocation: NotRequired[bool]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    RemoveEncryptionConfiguration: NotRequired[bool]
    ExpectedBucketOwner: NotRequired[str]
    RemoveExpectedBucketOwner: NotRequired[bool]
    AclConfiguration: NotRequired[AclConfigurationTypeDef]
    RemoveAclConfiguration: NotRequired[bool]

class SessionConfigurationTypeDef(TypedDict):
    ExecutionRole: NotRequired[str]
    WorkingDirectory: NotRequired[str]
    IdleTimeoutSeconds: NotRequired[int]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]

class StartSessionRequestRequestTypeDef(TypedDict):
    WorkGroup: str
    EngineConfiguration: EngineConfigurationTypeDef
    Description: NotRequired[str]
    NotebookVersion: NotRequired[str]
    SessionIdleTimeoutInMinutes: NotRequired[int]
    ClientRequestToken: NotRequired[str]

class ListEngineVersionsOutputTypeDef(TypedDict):
    EngineVersions: List[EngineVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class WorkGroupSummaryTypeDef(TypedDict):
    Name: NotRequired[str]
    State: NotRequired[WorkGroupStateType]
    Description: NotRequired[str]
    CreationTime: NotRequired[datetime]
    EngineVersion: NotRequired[EngineVersionTypeDef]
    IdentityCenterApplicationArn: NotRequired[str]

class ListExecutorsResponseTypeDef(TypedDict):
    SessionId: str
    ExecutorsSummary: List[ExecutorsSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ExportNotebookOutputTypeDef(TypedDict):
    NotebookMetadata: NotebookMetadataTypeDef
    Payload: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetNotebookMetadataOutputTypeDef(TypedDict):
    NotebookMetadata: NotebookMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListNotebookMetadataOutputTypeDef(TypedDict):
    NotebookMetadataList: List[NotebookMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListNotebookMetadataInputRequestTypeDef(TypedDict):
    WorkGroup: str
    Filters: NotRequired[FilterDefinitionTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class GetQueryResultsInputGetQueryResultsPaginateTypeDef(TypedDict):
    QueryExecutionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataCatalogsInputListDataCatalogsPaginateTypeDef(TypedDict):
    WorkGroup: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDatabasesInputListDatabasesPaginateTypeDef(TypedDict):
    CatalogName: str
    WorkGroup: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNamedQueriesInputListNamedQueriesPaginateTypeDef(TypedDict):
    WorkGroup: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQueryExecutionsInputListQueryExecutionsPaginateTypeDef(TypedDict):
    WorkGroup: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTableMetadataInputListTableMetadataPaginateTypeDef(TypedDict):
    CatalogName: str
    DatabaseName: str
    Expression: NotRequired[str]
    WorkGroup: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTagsForResourceInputListTagsForResourcePaginateTypeDef(TypedDict):
    ResourceARN: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetSessionStatusResponseTypeDef(TypedDict):
    SessionId: str
    Status: SessionStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SessionSummaryTypeDef(TypedDict):
    SessionId: NotRequired[str]
    Description: NotRequired[str]
    EngineVersion: NotRequired[EngineVersionTypeDef]
    NotebookVersion: NotRequired[str]
    Status: NotRequired[SessionStatusTypeDef]

class ListNotebookSessionsResponseTypeDef(TypedDict):
    NotebookSessionsList: List[NotebookSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPreparedStatementsOutputTypeDef(TypedDict):
    PreparedStatements: List[PreparedStatementSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class QueryExecutionStatisticsTypeDef(TypedDict):
    EngineExecutionTimeInMillis: NotRequired[int]
    DataScannedInBytes: NotRequired[int]
    DataManifestLocation: NotRequired[str]
    TotalExecutionTimeInMillis: NotRequired[int]
    QueryQueueTimeInMillis: NotRequired[int]
    ServicePreProcessingTimeInMillis: NotRequired[int]
    QueryPlanningTimeInMillis: NotRequired[int]
    ServiceProcessingTimeInMillis: NotRequired[int]
    ResultReuseInformation: NotRequired[ResultReuseInformationTypeDef]

class QueryStageTypeDef(TypedDict):
    StageId: NotRequired[int]
    State: NotRequired[str]
    OutputBytes: NotRequired[int]
    OutputRows: NotRequired[int]
    InputBytes: NotRequired[int]
    InputRows: NotRequired[int]
    ExecutionTime: NotRequired[int]
    QueryStagePlan: NotRequired[QueryStagePlanNodeTypeDef]
    SubStages: NotRequired[List[Dict[str, Any]]]

class ResultReuseConfigurationTypeDef(TypedDict):
    ResultReuseByAgeConfiguration: NotRequired[ResultReuseByAgeConfigurationTypeDef]

class ListCalculationExecutionsResponseTypeDef(TypedDict):
    Calculations: List[CalculationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetCapacityReservationOutputTypeDef(TypedDict):
    CapacityReservation: CapacityReservationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListCapacityReservationsOutputTypeDef(TypedDict):
    CapacityReservations: List[CapacityReservationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetCapacityAssignmentConfigurationOutputTypeDef(TypedDict):
    CapacityAssignmentConfiguration: CapacityAssignmentConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutCapacityAssignmentConfigurationInputRequestTypeDef(TypedDict):
    CapacityReservationName: str
    CapacityAssignments: Sequence[CapacityAssignmentUnionTypeDef]

class GetTableMetadataOutputTypeDef(TypedDict):
    TableMetadata: TableMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListTableMetadataOutputTypeDef(TypedDict):
    TableMetadataList: List[TableMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ResultSetTypeDef(TypedDict):
    Rows: NotRequired[List[RowTypeDef]]
    ResultSetMetadata: NotRequired[ResultSetMetadataTypeDef]

class WorkGroupConfigurationTypeDef(TypedDict):
    ResultConfiguration: NotRequired[ResultConfigurationTypeDef]
    EnforceWorkGroupConfiguration: NotRequired[bool]
    PublishCloudWatchMetricsEnabled: NotRequired[bool]
    BytesScannedCutoffPerQuery: NotRequired[int]
    RequesterPaysEnabled: NotRequired[bool]
    EngineVersion: NotRequired[EngineVersionTypeDef]
    AdditionalConfiguration: NotRequired[str]
    ExecutionRole: NotRequired[str]
    CustomerContentEncryptionConfiguration: NotRequired[
        CustomerContentEncryptionConfigurationTypeDef
    ]
    EnableMinimumEncryptionConfiguration: NotRequired[bool]
    IdentityCenterConfiguration: NotRequired[IdentityCenterConfigurationTypeDef]
    QueryResultsS3AccessGrantsConfiguration: NotRequired[
        QueryResultsS3AccessGrantsConfigurationTypeDef
    ]

class WorkGroupConfigurationUpdatesTypeDef(TypedDict):
    EnforceWorkGroupConfiguration: NotRequired[bool]
    ResultConfigurationUpdates: NotRequired[ResultConfigurationUpdatesTypeDef]
    PublishCloudWatchMetricsEnabled: NotRequired[bool]
    BytesScannedCutoffPerQuery: NotRequired[int]
    RemoveBytesScannedCutoffPerQuery: NotRequired[bool]
    RequesterPaysEnabled: NotRequired[bool]
    EngineVersion: NotRequired[EngineVersionTypeDef]
    RemoveCustomerContentEncryptionConfiguration: NotRequired[bool]
    AdditionalConfiguration: NotRequired[str]
    ExecutionRole: NotRequired[str]
    CustomerContentEncryptionConfiguration: NotRequired[
        CustomerContentEncryptionConfigurationTypeDef
    ]
    EnableMinimumEncryptionConfiguration: NotRequired[bool]
    QueryResultsS3AccessGrantsConfiguration: NotRequired[
        QueryResultsS3AccessGrantsConfigurationTypeDef
    ]

class GetSessionResponseTypeDef(TypedDict):
    SessionId: str
    Description: str
    WorkGroup: str
    EngineVersion: str
    EngineConfiguration: EngineConfigurationOutputTypeDef
    NotebookVersion: str
    SessionConfiguration: SessionConfigurationTypeDef
    Status: SessionStatusTypeDef
    Statistics: SessionStatisticsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListWorkGroupsOutputTypeDef(TypedDict):
    WorkGroups: List[WorkGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSessionsResponseTypeDef(TypedDict):
    Sessions: List[SessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class QueryRuntimeStatisticsTypeDef(TypedDict):
    Timeline: NotRequired[QueryRuntimeStatisticsTimelineTypeDef]
    Rows: NotRequired[QueryRuntimeStatisticsRowsTypeDef]
    OutputStage: NotRequired[QueryStageTypeDef]

class QueryExecutionTypeDef(TypedDict):
    QueryExecutionId: NotRequired[str]
    Query: NotRequired[str]
    StatementType: NotRequired[StatementTypeType]
    ResultConfiguration: NotRequired[ResultConfigurationTypeDef]
    ResultReuseConfiguration: NotRequired[ResultReuseConfigurationTypeDef]
    QueryExecutionContext: NotRequired[QueryExecutionContextTypeDef]
    Status: NotRequired[QueryExecutionStatusTypeDef]
    Statistics: NotRequired[QueryExecutionStatisticsTypeDef]
    WorkGroup: NotRequired[str]
    EngineVersion: NotRequired[EngineVersionTypeDef]
    ExecutionParameters: NotRequired[List[str]]
    SubstatementType: NotRequired[str]
    QueryResultsS3AccessGrantsConfiguration: NotRequired[
        QueryResultsS3AccessGrantsConfigurationTypeDef
    ]

class StartQueryExecutionInputRequestTypeDef(TypedDict):
    QueryString: str
    ClientRequestToken: NotRequired[str]
    QueryExecutionContext: NotRequired[QueryExecutionContextTypeDef]
    ResultConfiguration: NotRequired[ResultConfigurationTypeDef]
    WorkGroup: NotRequired[str]
    ExecutionParameters: NotRequired[Sequence[str]]
    ResultReuseConfiguration: NotRequired[ResultReuseConfigurationTypeDef]

class GetQueryResultsOutputTypeDef(TypedDict):
    UpdateCount: int
    ResultSet: ResultSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateWorkGroupInputRequestTypeDef(TypedDict):
    Name: str
    Configuration: NotRequired[WorkGroupConfigurationTypeDef]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class WorkGroupTypeDef(TypedDict):
    Name: str
    State: NotRequired[WorkGroupStateType]
    Configuration: NotRequired[WorkGroupConfigurationTypeDef]
    Description: NotRequired[str]
    CreationTime: NotRequired[datetime]
    IdentityCenterApplicationArn: NotRequired[str]

class UpdateWorkGroupInputRequestTypeDef(TypedDict):
    WorkGroup: str
    Description: NotRequired[str]
    ConfigurationUpdates: NotRequired[WorkGroupConfigurationUpdatesTypeDef]
    State: NotRequired[WorkGroupStateType]

class GetQueryRuntimeStatisticsOutputTypeDef(TypedDict):
    QueryRuntimeStatistics: QueryRuntimeStatisticsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetQueryExecutionOutputTypeDef(TypedDict):
    QueryExecutions: List[QueryExecutionTypeDef]
    UnprocessedQueryExecutionIds: List[UnprocessedQueryExecutionIdTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetQueryExecutionOutputTypeDef(TypedDict):
    QueryExecution: QueryExecutionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetWorkGroupOutputTypeDef(TypedDict):
    WorkGroup: WorkGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
