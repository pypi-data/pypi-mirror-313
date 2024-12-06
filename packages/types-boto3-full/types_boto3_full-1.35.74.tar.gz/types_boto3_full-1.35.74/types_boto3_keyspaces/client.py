"""
Type annotations for keyspaces service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_keyspaces.client import KeyspacesClient

    session = Session()
    client: KeyspacesClient = session.client("keyspaces")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListKeyspacesPaginator,
    ListTablesPaginator,
    ListTagsForResourcePaginator,
    ListTypesPaginator,
)
from .type_defs import (
    CreateKeyspaceRequestRequestTypeDef,
    CreateKeyspaceResponseTypeDef,
    CreateTableRequestRequestTypeDef,
    CreateTableResponseTypeDef,
    CreateTypeRequestRequestTypeDef,
    CreateTypeResponseTypeDef,
    DeleteKeyspaceRequestRequestTypeDef,
    DeleteTableRequestRequestTypeDef,
    DeleteTypeRequestRequestTypeDef,
    DeleteTypeResponseTypeDef,
    GetKeyspaceRequestRequestTypeDef,
    GetKeyspaceResponseTypeDef,
    GetTableAutoScalingSettingsRequestRequestTypeDef,
    GetTableAutoScalingSettingsResponseTypeDef,
    GetTableRequestRequestTypeDef,
    GetTableResponseTypeDef,
    GetTypeRequestRequestTypeDef,
    GetTypeResponseTypeDef,
    ListKeyspacesRequestRequestTypeDef,
    ListKeyspacesResponseTypeDef,
    ListTablesRequestRequestTypeDef,
    ListTablesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTypesRequestRequestTypeDef,
    ListTypesResponseTypeDef,
    RestoreTableRequestRequestTypeDef,
    RestoreTableResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateKeyspaceRequestRequestTypeDef,
    UpdateKeyspaceResponseTypeDef,
    UpdateTableRequestRequestTypeDef,
    UpdateTableResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("KeyspacesClient",)


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
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class KeyspacesClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KeyspacesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#close)
        """

    def create_keyspace(
        self, **kwargs: Unpack[CreateKeyspaceRequestRequestTypeDef]
    ) -> CreateKeyspaceResponseTypeDef:
        """
        The <code>CreateKeyspace</code> operation adds a new keyspace to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/create_keyspace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#create_keyspace)
        """

    def create_table(
        self, **kwargs: Unpack[CreateTableRequestRequestTypeDef]
    ) -> CreateTableResponseTypeDef:
        """
        The <code>CreateTable</code> operation adds a new table to the specified
        keyspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/create_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#create_table)
        """

    def create_type(
        self, **kwargs: Unpack[CreateTypeRequestRequestTypeDef]
    ) -> CreateTypeResponseTypeDef:
        """
        The <code>CreateType</code> operation creates a new user-defined type in the
        specified keyspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/create_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#create_type)
        """

    def delete_keyspace(
        self, **kwargs: Unpack[DeleteKeyspaceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The <code>DeleteKeyspace</code> operation deletes a keyspace and all of its
        tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/delete_keyspace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#delete_keyspace)
        """

    def delete_table(self, **kwargs: Unpack[DeleteTableRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        The <code>DeleteTable</code> operation deletes a table and all of its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/delete_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#delete_table)
        """

    def delete_type(
        self, **kwargs: Unpack[DeleteTypeRequestRequestTypeDef]
    ) -> DeleteTypeResponseTypeDef:
        """
        The <code>DeleteType</code> operation deletes a user-defined type (UDT).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/delete_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#delete_type)
        """

    def get_keyspace(
        self, **kwargs: Unpack[GetKeyspaceRequestRequestTypeDef]
    ) -> GetKeyspaceResponseTypeDef:
        """
        Returns the name of the specified keyspace, the Amazon Resource Name (ARN), the
        replication strategy, the Amazon Web Services Regions of a multi-Region
        keyspace, and the status of newly added Regions after an
        <code>UpdateKeyspace</code> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_keyspace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#get_keyspace)
        """

    def get_table(self, **kwargs: Unpack[GetTableRequestRequestTypeDef]) -> GetTableResponseTypeDef:
        """
        Returns information about the table, including the table's name and current
        status, the keyspace name, configuration settings, and metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#get_table)
        """

    def get_table_auto_scaling_settings(
        self, **kwargs: Unpack[GetTableAutoScalingSettingsRequestRequestTypeDef]
    ) -> GetTableAutoScalingSettingsResponseTypeDef:
        """
        Returns auto scaling related settings of the specified table in JSON format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_table_auto_scaling_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#get_table_auto_scaling_settings)
        """

    def get_type(self, **kwargs: Unpack[GetTypeRequestRequestTypeDef]) -> GetTypeResponseTypeDef:
        """
        The <code>GetType</code> operation returns information about the type, for
        example the field definitions, the timestamp when the type was last modified,
        the level of nesting, the status, and details about if the type is used in
        other types and tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#get_type)
        """

    def list_keyspaces(
        self, **kwargs: Unpack[ListKeyspacesRequestRequestTypeDef]
    ) -> ListKeyspacesResponseTypeDef:
        """
        The <code>ListKeyspaces</code> operation returns a list of keyspaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/list_keyspaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#list_keyspaces)
        """

    def list_tables(
        self, **kwargs: Unpack[ListTablesRequestRequestTypeDef]
    ) -> ListTablesResponseTypeDef:
        """
        The <code>ListTables</code> operation returns a list of tables for a specified
        keyspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/list_tables.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#list_tables)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of all tags associated with the specified Amazon Keyspaces
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#list_tags_for_resource)
        """

    def list_types(
        self, **kwargs: Unpack[ListTypesRequestRequestTypeDef]
    ) -> ListTypesResponseTypeDef:
        """
        The <code>ListTypes</code> operation returns a list of types for a specified
        keyspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/list_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#list_types)
        """

    def restore_table(
        self, **kwargs: Unpack[RestoreTableRequestRequestTypeDef]
    ) -> RestoreTableResponseTypeDef:
        """
        Restores the table to the specified point in time within the
        <code>earliest_restorable_timestamp</code> and the current time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/restore_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#restore_table)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates a set of tags with a Amazon Keyspaces resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the association of tags from a Amazon Keyspaces resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#untag_resource)
        """

    def update_keyspace(
        self, **kwargs: Unpack[UpdateKeyspaceRequestRequestTypeDef]
    ) -> UpdateKeyspaceResponseTypeDef:
        """
        Adds a new Amazon Web Services Region to the keyspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/update_keyspace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#update_keyspace)
        """

    def update_table(
        self, **kwargs: Unpack[UpdateTableRequestRequestTypeDef]
    ) -> UpdateTableResponseTypeDef:
        """
        Adds new columns to the table or updates one of the table's settings, for
        example capacity mode, auto scaling, encryption, point-in-time recovery, or ttl
        settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/update_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#update_table)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_keyspaces"]) -> ListKeyspacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tables"]) -> ListTablesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_types"]) -> ListTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_keyspaces/client/#get_paginator)
        """
