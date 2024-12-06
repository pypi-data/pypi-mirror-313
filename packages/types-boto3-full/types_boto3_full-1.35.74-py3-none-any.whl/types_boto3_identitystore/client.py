"""
Type annotations for identitystore service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_identitystore.client import IdentityStoreClient

    session = Session()
    client: IdentityStoreClient = session.client("identitystore")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListGroupMembershipsForMemberPaginator,
    ListGroupMembershipsPaginator,
    ListGroupsPaginator,
    ListUsersPaginator,
)
from .type_defs import (
    CreateGroupMembershipRequestRequestTypeDef,
    CreateGroupMembershipResponseTypeDef,
    CreateGroupRequestRequestTypeDef,
    CreateGroupResponseTypeDef,
    CreateUserRequestRequestTypeDef,
    CreateUserResponseTypeDef,
    DeleteGroupMembershipRequestRequestTypeDef,
    DeleteGroupRequestRequestTypeDef,
    DeleteUserRequestRequestTypeDef,
    DescribeGroupMembershipRequestRequestTypeDef,
    DescribeGroupMembershipResponseTypeDef,
    DescribeGroupRequestRequestTypeDef,
    DescribeGroupResponseTypeDef,
    DescribeUserRequestRequestTypeDef,
    DescribeUserResponseTypeDef,
    GetGroupIdRequestRequestTypeDef,
    GetGroupIdResponseTypeDef,
    GetGroupMembershipIdRequestRequestTypeDef,
    GetGroupMembershipIdResponseTypeDef,
    GetUserIdRequestRequestTypeDef,
    GetUserIdResponseTypeDef,
    IsMemberInGroupsRequestRequestTypeDef,
    IsMemberInGroupsResponseTypeDef,
    ListGroupMembershipsForMemberRequestRequestTypeDef,
    ListGroupMembershipsForMemberResponseTypeDef,
    ListGroupMembershipsRequestRequestTypeDef,
    ListGroupMembershipsResponseTypeDef,
    ListGroupsRequestRequestTypeDef,
    ListGroupsResponseTypeDef,
    ListUsersRequestRequestTypeDef,
    ListUsersResponseTypeDef,
    UpdateGroupRequestRequestTypeDef,
    UpdateUserRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("IdentityStoreClient",)


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
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class IdentityStoreClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IdentityStoreClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#close)
        """

    def create_group(
        self, **kwargs: Unpack[CreateGroupRequestRequestTypeDef]
    ) -> CreateGroupResponseTypeDef:
        """
        Creates a group within the specified identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/create_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#create_group)
        """

    def create_group_membership(
        self, **kwargs: Unpack[CreateGroupMembershipRequestRequestTypeDef]
    ) -> CreateGroupMembershipResponseTypeDef:
        """
        Creates a relationship between a member and a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/create_group_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#create_group_membership)
        """

    def create_user(
        self, **kwargs: Unpack[CreateUserRequestRequestTypeDef]
    ) -> CreateUserResponseTypeDef:
        """
        Creates a user within the specified identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/create_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#create_user)
        """

    def delete_group(self, **kwargs: Unpack[DeleteGroupRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Delete a group within an identity store given <code>GroupId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/delete_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#delete_group)
        """

    def delete_group_membership(
        self, **kwargs: Unpack[DeleteGroupMembershipRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete a membership within a group given <code>MembershipId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/delete_group_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#delete_group_membership)
        """

    def delete_user(self, **kwargs: Unpack[DeleteUserRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a user within an identity store given <code>UserId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/delete_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#delete_user)
        """

    def describe_group(
        self, **kwargs: Unpack[DescribeGroupRequestRequestTypeDef]
    ) -> DescribeGroupResponseTypeDef:
        """
        Retrieves the group metadata and attributes from <code>GroupId</code> in an
        identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/describe_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#describe_group)
        """

    def describe_group_membership(
        self, **kwargs: Unpack[DescribeGroupMembershipRequestRequestTypeDef]
    ) -> DescribeGroupMembershipResponseTypeDef:
        """
        Retrieves membership metadata and attributes from <code>MembershipId</code> in
        an identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/describe_group_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#describe_group_membership)
        """

    def describe_user(
        self, **kwargs: Unpack[DescribeUserRequestRequestTypeDef]
    ) -> DescribeUserResponseTypeDef:
        """
        Retrieves the user metadata and attributes from the <code>UserId</code> in an
        identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/describe_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#describe_user)
        """

    def get_group_id(
        self, **kwargs: Unpack[GetGroupIdRequestRequestTypeDef]
    ) -> GetGroupIdResponseTypeDef:
        """
        Retrieves <code>GroupId</code> in an identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/get_group_id.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#get_group_id)
        """

    def get_group_membership_id(
        self, **kwargs: Unpack[GetGroupMembershipIdRequestRequestTypeDef]
    ) -> GetGroupMembershipIdResponseTypeDef:
        """
        Retrieves the <code>MembershipId</code> in an identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/get_group_membership_id.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#get_group_membership_id)
        """

    def get_user_id(
        self, **kwargs: Unpack[GetUserIdRequestRequestTypeDef]
    ) -> GetUserIdResponseTypeDef:
        """
        Retrieves the <code>UserId</code> in an identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/get_user_id.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#get_user_id)
        """

    def is_member_in_groups(
        self, **kwargs: Unpack[IsMemberInGroupsRequestRequestTypeDef]
    ) -> IsMemberInGroupsResponseTypeDef:
        """
        Checks the user's membership in all requested groups and returns if the member
        exists in all queried groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/is_member_in_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#is_member_in_groups)
        """

    def list_group_memberships(
        self, **kwargs: Unpack[ListGroupMembershipsRequestRequestTypeDef]
    ) -> ListGroupMembershipsResponseTypeDef:
        """
        For the specified group in the specified identity store, returns the list of
        all <code>GroupMembership</code> objects and returns results in paginated form.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/list_group_memberships.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#list_group_memberships)
        """

    def list_group_memberships_for_member(
        self, **kwargs: Unpack[ListGroupMembershipsForMemberRequestRequestTypeDef]
    ) -> ListGroupMembershipsForMemberResponseTypeDef:
        """
        For the specified member in the specified identity store, returns the list of
        all <code>GroupMembership</code> objects and returns results in paginated form.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/list_group_memberships_for_member.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#list_group_memberships_for_member)
        """

    def list_groups(
        self, **kwargs: Unpack[ListGroupsRequestRequestTypeDef]
    ) -> ListGroupsResponseTypeDef:
        """
        Lists all groups in the identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/list_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#list_groups)
        """

    def list_users(
        self, **kwargs: Unpack[ListUsersRequestRequestTypeDef]
    ) -> ListUsersResponseTypeDef:
        """
        Lists all users in the identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/list_users.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#list_users)
        """

    def update_group(self, **kwargs: Unpack[UpdateGroupRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        For the specified group in the specified identity store, updates the group
        metadata and attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/update_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#update_group)
        """

    def update_user(self, **kwargs: Unpack[UpdateUserRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        For the specified user in the specified identity store, updates the user
        metadata and attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/update_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#update_user)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_memberships_for_member"]
    ) -> ListGroupMembershipsForMemberPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_memberships"]
    ) -> ListGroupMembershipsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_identitystore/client/#get_paginator)
        """
