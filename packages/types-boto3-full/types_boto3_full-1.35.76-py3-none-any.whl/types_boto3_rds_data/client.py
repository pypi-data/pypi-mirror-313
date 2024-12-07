"""
Type annotations for rds-data service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds_data/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_rds_data.client import RDSDataServiceClient

    session = Session()
    client: RDSDataServiceClient = session.client("rds-data")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    BatchExecuteStatementRequestRequestTypeDef,
    BatchExecuteStatementResponseTypeDef,
    BeginTransactionRequestRequestTypeDef,
    BeginTransactionResponseTypeDef,
    CommitTransactionRequestRequestTypeDef,
    CommitTransactionResponseTypeDef,
    ExecuteSqlRequestRequestTypeDef,
    ExecuteSqlResponseTypeDef,
    ExecuteStatementRequestRequestTypeDef,
    ExecuteStatementResponseTypeDef,
    RollbackTransactionRequestRequestTypeDef,
    RollbackTransactionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("RDSDataServiceClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DatabaseErrorException: Type[BotocoreClientError]
    DatabaseNotFoundException: Type[BotocoreClientError]
    DatabaseResumingException: Type[BotocoreClientError]
    DatabaseUnavailableException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    HttpEndpointNotEnabledException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    InvalidSecretException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    SecretsErrorException: Type[BotocoreClientError]
    ServiceUnavailableError: Type[BotocoreClientError]
    StatementTimeoutException: Type[BotocoreClientError]
    TransactionNotFoundException: Type[BotocoreClientError]
    UnsupportedResultException: Type[BotocoreClientError]


class RDSDataServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data.html#RDSDataService.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RDSDataServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data.html#RDSDataService.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds_data/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds_data/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds_data/client/#close)
        """

    def batch_execute_statement(
        self, **kwargs: Unpack[BatchExecuteStatementRequestRequestTypeDef]
    ) -> BatchExecuteStatementResponseTypeDef:
        """
        Runs a batch SQL statement over an array of data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/batch_execute_statement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds_data/client/#batch_execute_statement)
        """

    def begin_transaction(
        self, **kwargs: Unpack[BeginTransactionRequestRequestTypeDef]
    ) -> BeginTransactionResponseTypeDef:
        """
        Starts a SQL transaction.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/begin_transaction.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds_data/client/#begin_transaction)
        """

    def commit_transaction(
        self, **kwargs: Unpack[CommitTransactionRequestRequestTypeDef]
    ) -> CommitTransactionResponseTypeDef:
        """
        Ends a SQL transaction started with the <code>BeginTransaction</code> operation
        and commits the changes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/commit_transaction.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds_data/client/#commit_transaction)
        """

    def execute_sql(
        self, **kwargs: Unpack[ExecuteSqlRequestRequestTypeDef]
    ) -> ExecuteSqlResponseTypeDef:
        """
        Runs one or more SQL statements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/execute_sql.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds_data/client/#execute_sql)
        """

    def execute_statement(
        self, **kwargs: Unpack[ExecuteStatementRequestRequestTypeDef]
    ) -> ExecuteStatementResponseTypeDef:
        """
        Runs a SQL statement against a database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/execute_statement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds_data/client/#execute_statement)
        """

    def rollback_transaction(
        self, **kwargs: Unpack[RollbackTransactionRequestRequestTypeDef]
    ) -> RollbackTransactionResponseTypeDef:
        """
        Performs a rollback of a transaction.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/rollback_transaction.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds_data/client/#rollback_transaction)
        """
