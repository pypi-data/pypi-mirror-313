"""
Type annotations for ds-data service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_ds_data.client import DirectoryServiceDataClient

    session = Session()
    client: DirectoryServiceDataClient = session.client("ds-data")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListGroupMembersPaginator,
    ListGroupsForMemberPaginator,
    ListGroupsPaginator,
    ListUsersPaginator,
    SearchGroupsPaginator,
    SearchUsersPaginator,
)
from .type_defs import (
    AddGroupMemberRequestRequestTypeDef,
    CreateGroupRequestRequestTypeDef,
    CreateGroupResultTypeDef,
    CreateUserRequestRequestTypeDef,
    CreateUserResultTypeDef,
    DeleteGroupRequestRequestTypeDef,
    DeleteUserRequestRequestTypeDef,
    DescribeGroupRequestRequestTypeDef,
    DescribeGroupResultTypeDef,
    DescribeUserRequestRequestTypeDef,
    DescribeUserResultTypeDef,
    DisableUserRequestRequestTypeDef,
    ListGroupMembersRequestRequestTypeDef,
    ListGroupMembersResultTypeDef,
    ListGroupsForMemberRequestRequestTypeDef,
    ListGroupsForMemberResultTypeDef,
    ListGroupsRequestRequestTypeDef,
    ListGroupsResultTypeDef,
    ListUsersRequestRequestTypeDef,
    ListUsersResultTypeDef,
    RemoveGroupMemberRequestRequestTypeDef,
    SearchGroupsRequestRequestTypeDef,
    SearchGroupsResultTypeDef,
    SearchUsersRequestRequestTypeDef,
    SearchUsersResultTypeDef,
    UpdateGroupRequestRequestTypeDef,
    UpdateUserRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("DirectoryServiceDataClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DirectoryUnavailableException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class DirectoryServiceDataClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DirectoryServiceDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#close)
        """

    def add_group_member(
        self, **kwargs: Unpack[AddGroupMemberRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds an existing user, group, or computer as a group member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/add_group_member.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#add_group_member)
        """

    def create_group(
        self, **kwargs: Unpack[CreateGroupRequestRequestTypeDef]
    ) -> CreateGroupResultTypeDef:
        """
        Creates a new group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/create_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#create_group)
        """

    def create_user(
        self, **kwargs: Unpack[CreateUserRequestRequestTypeDef]
    ) -> CreateUserResultTypeDef:
        """
        Creates a new user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/create_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#create_user)
        """

    def delete_group(self, **kwargs: Unpack[DeleteGroupRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/delete_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#delete_group)
        """

    def delete_user(self, **kwargs: Unpack[DeleteUserRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/delete_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#delete_user)
        """

    def describe_group(
        self, **kwargs: Unpack[DescribeGroupRequestRequestTypeDef]
    ) -> DescribeGroupResultTypeDef:
        """
        Returns information about a specific group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/describe_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#describe_group)
        """

    def describe_user(
        self, **kwargs: Unpack[DescribeUserRequestRequestTypeDef]
    ) -> DescribeUserResultTypeDef:
        """
        Returns information about a specific user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/describe_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#describe_user)
        """

    def disable_user(self, **kwargs: Unpack[DisableUserRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deactivates an active user account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/disable_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#disable_user)
        """

    def list_group_members(
        self, **kwargs: Unpack[ListGroupMembersRequestRequestTypeDef]
    ) -> ListGroupMembersResultTypeDef:
        """
        Returns member information for the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/list_group_members.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#list_group_members)
        """

    def list_groups(
        self, **kwargs: Unpack[ListGroupsRequestRequestTypeDef]
    ) -> ListGroupsResultTypeDef:
        """
        Returns group information for the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/list_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#list_groups)
        """

    def list_groups_for_member(
        self, **kwargs: Unpack[ListGroupsForMemberRequestRequestTypeDef]
    ) -> ListGroupsForMemberResultTypeDef:
        """
        Returns group information for the specified member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/list_groups_for_member.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#list_groups_for_member)
        """

    def list_users(
        self, **kwargs: Unpack[ListUsersRequestRequestTypeDef]
    ) -> ListUsersResultTypeDef:
        """
        Returns user information for the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/list_users.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#list_users)
        """

    def remove_group_member(
        self, **kwargs: Unpack[RemoveGroupMemberRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a member from a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/remove_group_member.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#remove_group_member)
        """

    def search_groups(
        self, **kwargs: Unpack[SearchGroupsRequestRequestTypeDef]
    ) -> SearchGroupsResultTypeDef:
        """
        Searches the specified directory for a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/search_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#search_groups)
        """

    def search_users(
        self, **kwargs: Unpack[SearchUsersRequestRequestTypeDef]
    ) -> SearchUsersResultTypeDef:
        """
        Searches the specified directory for a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/search_users.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#search_users)
        """

    def update_group(self, **kwargs: Unpack[UpdateGroupRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates group information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/update_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#update_group)
        """

    def update_user(self, **kwargs: Unpack[UpdateUserRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates user information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/update_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#update_user)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_members"]
    ) -> ListGroupMembersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_groups_for_member"]
    ) -> ListGroupsForMemberPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_groups"]) -> SearchGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_users"]) -> SearchUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds_data/client/#get_paginator)
        """
