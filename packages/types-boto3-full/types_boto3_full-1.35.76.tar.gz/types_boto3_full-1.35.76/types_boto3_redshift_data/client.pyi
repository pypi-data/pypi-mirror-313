"""
Type annotations for redshift-data service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_redshift_data.client import RedshiftDataAPIServiceClient

    session = Session()
    client: RedshiftDataAPIServiceClient = session.client("redshift-data")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeTablePaginator,
    GetStatementResultPaginator,
    GetStatementResultV2Paginator,
    ListDatabasesPaginator,
    ListSchemasPaginator,
    ListStatementsPaginator,
    ListTablesPaginator,
)
from .type_defs import (
    BatchExecuteStatementInputRequestTypeDef,
    BatchExecuteStatementOutputTypeDef,
    CancelStatementRequestRequestTypeDef,
    CancelStatementResponseTypeDef,
    DescribeStatementRequestRequestTypeDef,
    DescribeStatementResponseTypeDef,
    DescribeTableRequestRequestTypeDef,
    DescribeTableResponseTypeDef,
    ExecuteStatementInputRequestTypeDef,
    ExecuteStatementOutputTypeDef,
    GetStatementResultRequestRequestTypeDef,
    GetStatementResultResponseTypeDef,
    GetStatementResultV2RequestRequestTypeDef,
    GetStatementResultV2ResponseTypeDef,
    ListDatabasesRequestRequestTypeDef,
    ListDatabasesResponseTypeDef,
    ListSchemasRequestRequestTypeDef,
    ListSchemasResponseTypeDef,
    ListStatementsRequestRequestTypeDef,
    ListStatementsResponseTypeDef,
    ListTablesRequestRequestTypeDef,
    ListTablesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("RedshiftDataAPIServiceClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ActiveSessionsExceededException: Type[BotocoreClientError]
    ActiveStatementsExceededException: Type[BotocoreClientError]
    BatchExecuteStatementException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DatabaseConnectionException: Type[BotocoreClientError]
    ExecuteStatementException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    QueryTimeoutException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class RedshiftDataAPIServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RedshiftDataAPIServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html#RedshiftDataAPIService.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#close)
        """

    def batch_execute_statement(
        self, **kwargs: Unpack[BatchExecuteStatementInputRequestTypeDef]
    ) -> BatchExecuteStatementOutputTypeDef:
        """
        Runs one or more SQL statements, which can be data manipulation language (DML)
        or data definition language (DDL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/batch_execute_statement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#batch_execute_statement)
        """

    def cancel_statement(
        self, **kwargs: Unpack[CancelStatementRequestRequestTypeDef]
    ) -> CancelStatementResponseTypeDef:
        """
        Cancels a running query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/cancel_statement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#cancel_statement)
        """

    def describe_statement(
        self, **kwargs: Unpack[DescribeStatementRequestRequestTypeDef]
    ) -> DescribeStatementResponseTypeDef:
        """
        Describes the details about a specific instance when a query was run by the
        Amazon Redshift Data API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/describe_statement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#describe_statement)
        """

    def describe_table(
        self, **kwargs: Unpack[DescribeTableRequestRequestTypeDef]
    ) -> DescribeTableResponseTypeDef:
        """
        Describes the detailed information about a table from metadata in the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/describe_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#describe_table)
        """

    def execute_statement(
        self, **kwargs: Unpack[ExecuteStatementInputRequestTypeDef]
    ) -> ExecuteStatementOutputTypeDef:
        """
        Runs an SQL statement, which can be data manipulation language (DML) or data
        definition language (DDL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/execute_statement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#execute_statement)
        """

    def get_statement_result(
        self, **kwargs: Unpack[GetStatementResultRequestRequestTypeDef]
    ) -> GetStatementResultResponseTypeDef:
        """
        Fetches the temporarily cached result of an SQL statement in JSON format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/get_statement_result.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#get_statement_result)
        """

    def get_statement_result_v2(
        self, **kwargs: Unpack[GetStatementResultV2RequestRequestTypeDef]
    ) -> GetStatementResultV2ResponseTypeDef:
        """
        Fetches the temporarily cached result of an SQL statement in CSV format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/get_statement_result_v2.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#get_statement_result_v2)
        """

    def list_databases(
        self, **kwargs: Unpack[ListDatabasesRequestRequestTypeDef]
    ) -> ListDatabasesResponseTypeDef:
        """
        List the databases in a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/list_databases.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#list_databases)
        """

    def list_schemas(
        self, **kwargs: Unpack[ListSchemasRequestRequestTypeDef]
    ) -> ListSchemasResponseTypeDef:
        """
        Lists the schemas in a database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/list_schemas.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#list_schemas)
        """

    def list_statements(
        self, **kwargs: Unpack[ListStatementsRequestRequestTypeDef]
    ) -> ListStatementsResponseTypeDef:
        """
        List of SQL statements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/list_statements.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#list_statements)
        """

    def list_tables(
        self, **kwargs: Unpack[ListTablesRequestRequestTypeDef]
    ) -> ListTablesResponseTypeDef:
        """
        List the tables in a database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/list_tables.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#list_tables)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_table"]) -> DescribeTablePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_statement_result"]
    ) -> GetStatementResultPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_statement_result_v2"]
    ) -> GetStatementResultV2Paginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_databases"]) -> ListDatabasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_schemas"]) -> ListSchemasPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_statements"]) -> ListStatementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tables"]) -> ListTablesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_data/client/#get_paginator)
        """
