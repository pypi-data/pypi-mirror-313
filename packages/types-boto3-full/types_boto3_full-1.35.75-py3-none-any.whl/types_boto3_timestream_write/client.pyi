"""
Type annotations for timestream-write service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_timestream_write.client import TimestreamWriteClient

    session = Session()
    client: TimestreamWriteClient = session.client("timestream-write")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateBatchLoadTaskRequestRequestTypeDef,
    CreateBatchLoadTaskResponseTypeDef,
    CreateDatabaseRequestRequestTypeDef,
    CreateDatabaseResponseTypeDef,
    CreateTableRequestRequestTypeDef,
    CreateTableResponseTypeDef,
    DeleteDatabaseRequestRequestTypeDef,
    DeleteTableRequestRequestTypeDef,
    DescribeBatchLoadTaskRequestRequestTypeDef,
    DescribeBatchLoadTaskResponseTypeDef,
    DescribeDatabaseRequestRequestTypeDef,
    DescribeDatabaseResponseTypeDef,
    DescribeEndpointsResponseTypeDef,
    DescribeTableRequestRequestTypeDef,
    DescribeTableResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ListBatchLoadTasksRequestRequestTypeDef,
    ListBatchLoadTasksResponseTypeDef,
    ListDatabasesRequestRequestTypeDef,
    ListDatabasesResponseTypeDef,
    ListTablesRequestRequestTypeDef,
    ListTablesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ResumeBatchLoadTaskRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDatabaseRequestRequestTypeDef,
    UpdateDatabaseResponseTypeDef,
    UpdateTableRequestRequestTypeDef,
    UpdateTableResponseTypeDef,
    WriteRecordsRequestRequestTypeDef,
    WriteRecordsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("TimestreamWriteClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidEndpointException: Type[BotocoreClientError]
    RejectedRecordsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class TimestreamWriteClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write.html#TimestreamWrite.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TimestreamWriteClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write.html#TimestreamWrite.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#close)
        """

    def create_batch_load_task(
        self, **kwargs: Unpack[CreateBatchLoadTaskRequestRequestTypeDef]
    ) -> CreateBatchLoadTaskResponseTypeDef:
        """
        Creates a new Timestream batch load task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/create_batch_load_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#create_batch_load_task)
        """

    def create_database(
        self, **kwargs: Unpack[CreateDatabaseRequestRequestTypeDef]
    ) -> CreateDatabaseResponseTypeDef:
        """
        Creates a new Timestream database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/create_database.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#create_database)
        """

    def create_table(
        self, **kwargs: Unpack[CreateTableRequestRequestTypeDef]
    ) -> CreateTableResponseTypeDef:
        """
        Adds a new table to an existing database in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/create_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#create_table)
        """

    def delete_database(
        self, **kwargs: Unpack[DeleteDatabaseRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a given Timestream database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/delete_database.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#delete_database)
        """

    def delete_table(
        self, **kwargs: Unpack[DeleteTableRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a given Timestream table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/delete_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#delete_table)
        """

    def describe_batch_load_task(
        self, **kwargs: Unpack[DescribeBatchLoadTaskRequestRequestTypeDef]
    ) -> DescribeBatchLoadTaskResponseTypeDef:
        """
        Returns information about the batch load task, including configurations,
        mappings, progress, and other details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/describe_batch_load_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#describe_batch_load_task)
        """

    def describe_database(
        self, **kwargs: Unpack[DescribeDatabaseRequestRequestTypeDef]
    ) -> DescribeDatabaseResponseTypeDef:
        """
        Returns information about the database, including the database name, time that
        the database was created, and the total number of tables found within the
        database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/describe_database.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#describe_database)
        """

    def describe_endpoints(self) -> DescribeEndpointsResponseTypeDef:
        """
        Returns a list of available endpoints to make Timestream API calls against.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/describe_endpoints.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#describe_endpoints)
        """

    def describe_table(
        self, **kwargs: Unpack[DescribeTableRequestRequestTypeDef]
    ) -> DescribeTableResponseTypeDef:
        """
        Returns information about the table, including the table name, database name,
        retention duration of the memory store and the magnetic store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/describe_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#describe_table)
        """

    def list_batch_load_tasks(
        self, **kwargs: Unpack[ListBatchLoadTasksRequestRequestTypeDef]
    ) -> ListBatchLoadTasksResponseTypeDef:
        """
        Provides a list of batch load tasks, along with the name, status, when the task
        is resumable until, and other details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/list_batch_load_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#list_batch_load_tasks)
        """

    def list_databases(
        self, **kwargs: Unpack[ListDatabasesRequestRequestTypeDef]
    ) -> ListDatabasesResponseTypeDef:
        """
        Returns a list of your Timestream databases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/list_databases.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#list_databases)
        """

    def list_tables(
        self, **kwargs: Unpack[ListTablesRequestRequestTypeDef]
    ) -> ListTablesResponseTypeDef:
        """
        Provides a list of tables, along with the name, status, and retention
        properties of each table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/list_tables.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#list_tables)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags on a Timestream resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#list_tags_for_resource)
        """

    def resume_batch_load_task(
        self, **kwargs: Unpack[ResumeBatchLoadTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/resume_batch_load_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#resume_batch_load_task)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates a set of tags with a Timestream resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the association of tags from a Timestream resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#untag_resource)
        """

    def update_database(
        self, **kwargs: Unpack[UpdateDatabaseRequestRequestTypeDef]
    ) -> UpdateDatabaseResponseTypeDef:
        """
        Modifies the KMS key for an existing database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/update_database.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#update_database)
        """

    def update_table(
        self, **kwargs: Unpack[UpdateTableRequestRequestTypeDef]
    ) -> UpdateTableResponseTypeDef:
        """
        Modifies the retention duration of the memory store and magnetic store for your
        Timestream table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/update_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#update_table)
        """

    def write_records(
        self, **kwargs: Unpack[WriteRecordsRequestRequestTypeDef]
    ) -> WriteRecordsResponseTypeDef:
        """
        Enables you to write your time-series data into Timestream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/write_records.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/client/#write_records)
        """
