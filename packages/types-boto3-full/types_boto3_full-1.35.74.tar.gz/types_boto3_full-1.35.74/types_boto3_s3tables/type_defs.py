"""
Type annotations for s3tables service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/type_defs/)

Usage::

    ```python
    from types_boto3_s3tables.type_defs import CreateNamespaceRequestRequestTypeDef

    data: CreateNamespaceRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    JobStatusType,
    MaintenanceStatusType,
    TableMaintenanceJobTypeType,
    TableMaintenanceTypeType,
    TableTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "CreateNamespaceRequestRequestTypeDef",
    "CreateNamespaceResponseTypeDef",
    "CreateTableBucketRequestRequestTypeDef",
    "CreateTableBucketResponseTypeDef",
    "CreateTableRequestRequestTypeDef",
    "CreateTableResponseTypeDef",
    "DeleteNamespaceRequestRequestTypeDef",
    "DeleteTableBucketPolicyRequestRequestTypeDef",
    "DeleteTableBucketRequestRequestTypeDef",
    "DeleteTablePolicyRequestRequestTypeDef",
    "DeleteTableRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetNamespaceRequestRequestTypeDef",
    "GetNamespaceResponseTypeDef",
    "GetTableBucketMaintenanceConfigurationRequestRequestTypeDef",
    "GetTableBucketMaintenanceConfigurationResponseTypeDef",
    "GetTableBucketPolicyRequestRequestTypeDef",
    "GetTableBucketPolicyResponseTypeDef",
    "GetTableBucketRequestRequestTypeDef",
    "GetTableBucketResponseTypeDef",
    "GetTableMaintenanceConfigurationRequestRequestTypeDef",
    "GetTableMaintenanceConfigurationResponseTypeDef",
    "GetTableMaintenanceJobStatusRequestRequestTypeDef",
    "GetTableMaintenanceJobStatusResponseTypeDef",
    "GetTableMetadataLocationRequestRequestTypeDef",
    "GetTableMetadataLocationResponseTypeDef",
    "GetTablePolicyRequestRequestTypeDef",
    "GetTablePolicyResponseTypeDef",
    "GetTableRequestRequestTypeDef",
    "GetTableResponseTypeDef",
    "IcebergCompactionSettingsTypeDef",
    "IcebergSnapshotManagementSettingsTypeDef",
    "IcebergUnreferencedFileRemovalSettingsTypeDef",
    "ListNamespacesRequestListNamespacesPaginateTypeDef",
    "ListNamespacesRequestRequestTypeDef",
    "ListNamespacesResponseTypeDef",
    "ListTableBucketsRequestListTableBucketsPaginateTypeDef",
    "ListTableBucketsRequestRequestTypeDef",
    "ListTableBucketsResponseTypeDef",
    "ListTablesRequestListTablesPaginateTypeDef",
    "ListTablesRequestRequestTypeDef",
    "ListTablesResponseTypeDef",
    "NamespaceSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "PutTableBucketMaintenanceConfigurationRequestRequestTypeDef",
    "PutTableBucketPolicyRequestRequestTypeDef",
    "PutTableMaintenanceConfigurationRequestRequestTypeDef",
    "PutTablePolicyRequestRequestTypeDef",
    "RenameTableRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "TableBucketMaintenanceConfigurationValueTypeDef",
    "TableBucketMaintenanceSettingsTypeDef",
    "TableBucketSummaryTypeDef",
    "TableMaintenanceConfigurationValueTypeDef",
    "TableMaintenanceJobStatusValueTypeDef",
    "TableMaintenanceSettingsTypeDef",
    "TableSummaryTypeDef",
    "UpdateTableMetadataLocationRequestRequestTypeDef",
    "UpdateTableMetadataLocationResponseTypeDef",
)


class CreateNamespaceRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateTableBucketRequestRequestTypeDef(TypedDict):
    name: str


CreateTableRequestRequestTypeDef = TypedDict(
    "CreateTableRequestRequestTypeDef",
    {
        "tableBucketARN": str,
        "namespace": str,
        "name": str,
        "format": Literal["ICEBERG"],
    },
)


class DeleteNamespaceRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: str


class DeleteTableBucketPolicyRequestRequestTypeDef(TypedDict):
    tableBucketARN: str


class DeleteTableBucketRequestRequestTypeDef(TypedDict):
    tableBucketARN: str


class DeleteTablePolicyRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: str
    name: str


class DeleteTableRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: str
    name: str
    versionToken: NotRequired[str]


class GetNamespaceRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: str


class GetTableBucketMaintenanceConfigurationRequestRequestTypeDef(TypedDict):
    tableBucketARN: str


class GetTableBucketPolicyRequestRequestTypeDef(TypedDict):
    tableBucketARN: str


class GetTableBucketRequestRequestTypeDef(TypedDict):
    tableBucketARN: str


class GetTableMaintenanceConfigurationRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: str
    name: str


class GetTableMaintenanceJobStatusRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: str
    name: str


class TableMaintenanceJobStatusValueTypeDef(TypedDict):
    status: JobStatusType
    lastRunTimestamp: NotRequired[datetime]
    failureMessage: NotRequired[str]


class GetTableMetadataLocationRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: str
    name: str


class GetTablePolicyRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: str
    name: str


class GetTableRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: str
    name: str


class IcebergCompactionSettingsTypeDef(TypedDict):
    targetFileSizeMB: NotRequired[int]


class IcebergSnapshotManagementSettingsTypeDef(TypedDict):
    minSnapshotsToKeep: NotRequired[int]
    maxSnapshotAgeHours: NotRequired[int]


class IcebergUnreferencedFileRemovalSettingsTypeDef(TypedDict):
    unreferencedDays: NotRequired[int]
    nonCurrentDays: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListNamespacesRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    prefix: NotRequired[str]
    continuationToken: NotRequired[str]
    maxNamespaces: NotRequired[int]


class NamespaceSummaryTypeDef(TypedDict):
    namespace: List[str]
    createdAt: datetime
    createdBy: str
    ownerAccountId: str


class ListTableBucketsRequestRequestTypeDef(TypedDict):
    prefix: NotRequired[str]
    continuationToken: NotRequired[str]
    maxBuckets: NotRequired[int]


class TableBucketSummaryTypeDef(TypedDict):
    arn: str
    name: str
    ownerAccountId: str
    createdAt: datetime


class ListTablesRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: NotRequired[str]
    prefix: NotRequired[str]
    continuationToken: NotRequired[str]
    maxTables: NotRequired[int]


TableSummaryTypeDef = TypedDict(
    "TableSummaryTypeDef",
    {
        "namespace": List[str],
        "name": str,
        "type": TableTypeType,
        "tableARN": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
    },
)


class PutTableBucketPolicyRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    resourcePolicy: str


class PutTablePolicyRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: str
    name: str
    resourcePolicy: str


class RenameTableRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: str
    name: str
    newNamespaceName: NotRequired[str]
    newName: NotRequired[str]
    versionToken: NotRequired[str]


class UpdateTableMetadataLocationRequestRequestTypeDef(TypedDict):
    tableBucketARN: str
    namespace: str
    name: str
    versionToken: str
    metadataLocation: str


class CreateNamespaceResponseTypeDef(TypedDict):
    tableBucketARN: str
    namespace: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTableBucketResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTableResponseTypeDef(TypedDict):
    tableARN: str
    versionToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetNamespaceResponseTypeDef(TypedDict):
    namespace: List[str]
    createdAt: datetime
    createdBy: str
    ownerAccountId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetTableBucketPolicyResponseTypeDef(TypedDict):
    resourcePolicy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetTableBucketResponseTypeDef(TypedDict):
    arn: str
    name: str
    ownerAccountId: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetTableMetadataLocationResponseTypeDef(TypedDict):
    versionToken: str
    metadataLocation: str
    warehouseLocation: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetTablePolicyResponseTypeDef(TypedDict):
    resourcePolicy: str
    ResponseMetadata: ResponseMetadataTypeDef


GetTableResponseTypeDef = TypedDict(
    "GetTableResponseTypeDef",
    {
        "name": str,
        "type": TableTypeType,
        "tableARN": str,
        "namespace": List[str],
        "versionToken": str,
        "metadataLocation": str,
        "warehouseLocation": str,
        "createdAt": datetime,
        "createdBy": str,
        "managedByService": str,
        "modifiedAt": datetime,
        "modifiedBy": str,
        "ownerAccountId": str,
        "format": Literal["ICEBERG"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class UpdateTableMetadataLocationResponseTypeDef(TypedDict):
    name: str
    tableARN: str
    namespace: List[str]
    versionToken: str
    metadataLocation: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetTableMaintenanceJobStatusResponseTypeDef(TypedDict):
    tableARN: str
    status: Dict[TableMaintenanceJobTypeType, TableMaintenanceJobStatusValueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TableMaintenanceSettingsTypeDef(TypedDict):
    icebergCompaction: NotRequired[IcebergCompactionSettingsTypeDef]
    icebergSnapshotManagement: NotRequired[IcebergSnapshotManagementSettingsTypeDef]


class TableBucketMaintenanceSettingsTypeDef(TypedDict):
    icebergUnreferencedFileRemoval: NotRequired[IcebergUnreferencedFileRemovalSettingsTypeDef]


class ListNamespacesRequestListNamespacesPaginateTypeDef(TypedDict):
    tableBucketARN: str
    prefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTableBucketsRequestListTableBucketsPaginateTypeDef(TypedDict):
    prefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTablesRequestListTablesPaginateTypeDef(TypedDict):
    tableBucketARN: str
    namespace: NotRequired[str]
    prefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNamespacesResponseTypeDef(TypedDict):
    namespaces: List[NamespaceSummaryTypeDef]
    continuationToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTableBucketsResponseTypeDef(TypedDict):
    tableBuckets: List[TableBucketSummaryTypeDef]
    continuationToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTablesResponseTypeDef(TypedDict):
    tables: List[TableSummaryTypeDef]
    continuationToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class TableMaintenanceConfigurationValueTypeDef(TypedDict):
    status: NotRequired[MaintenanceStatusType]
    settings: NotRequired[TableMaintenanceSettingsTypeDef]


class TableBucketMaintenanceConfigurationValueTypeDef(TypedDict):
    status: NotRequired[MaintenanceStatusType]
    settings: NotRequired[TableBucketMaintenanceSettingsTypeDef]


class GetTableMaintenanceConfigurationResponseTypeDef(TypedDict):
    tableARN: str
    configuration: Dict[TableMaintenanceTypeType, TableMaintenanceConfigurationValueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


PutTableMaintenanceConfigurationRequestRequestTypeDef = TypedDict(
    "PutTableMaintenanceConfigurationRequestRequestTypeDef",
    {
        "tableBucketARN": str,
        "namespace": str,
        "name": str,
        "type": TableMaintenanceTypeType,
        "value": TableMaintenanceConfigurationValueTypeDef,
    },
)


class GetTableBucketMaintenanceConfigurationResponseTypeDef(TypedDict):
    tableBucketARN: str
    configuration: Dict[
        Literal["icebergUnreferencedFileRemoval"], TableBucketMaintenanceConfigurationValueTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef


PutTableBucketMaintenanceConfigurationRequestRequestTypeDef = TypedDict(
    "PutTableBucketMaintenanceConfigurationRequestRequestTypeDef",
    {
        "tableBucketARN": str,
        "type": Literal["icebergUnreferencedFileRemoval"],
        "value": TableBucketMaintenanceConfigurationValueTypeDef,
    },
)
