"""
Type annotations for resource-groups service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_resource_groups.client import ResourceGroupsClient

    session = Session()
    client: ResourceGroupsClient = session.client("resource-groups")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListGroupingStatusesPaginator,
    ListGroupResourcesPaginator,
    ListGroupsPaginator,
    ListTagSyncTasksPaginator,
    SearchResourcesPaginator,
)
from .type_defs import (
    CancelTagSyncTaskInputRequestTypeDef,
    CreateGroupInputRequestTypeDef,
    CreateGroupOutputTypeDef,
    DeleteGroupInputRequestTypeDef,
    DeleteGroupOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAccountSettingsOutputTypeDef,
    GetGroupConfigurationInputRequestTypeDef,
    GetGroupConfigurationOutputTypeDef,
    GetGroupInputRequestTypeDef,
    GetGroupOutputTypeDef,
    GetGroupQueryInputRequestTypeDef,
    GetGroupQueryOutputTypeDef,
    GetTagsInputRequestTypeDef,
    GetTagsOutputTypeDef,
    GetTagSyncTaskInputRequestTypeDef,
    GetTagSyncTaskOutputTypeDef,
    GroupResourcesInputRequestTypeDef,
    GroupResourcesOutputTypeDef,
    ListGroupingStatusesInputRequestTypeDef,
    ListGroupingStatusesOutputTypeDef,
    ListGroupResourcesInputRequestTypeDef,
    ListGroupResourcesOutputTypeDef,
    ListGroupsInputRequestTypeDef,
    ListGroupsOutputTypeDef,
    ListTagSyncTasksInputRequestTypeDef,
    ListTagSyncTasksOutputTypeDef,
    PutGroupConfigurationInputRequestTypeDef,
    SearchResourcesInputRequestTypeDef,
    SearchResourcesOutputTypeDef,
    StartTagSyncTaskInputRequestTypeDef,
    StartTagSyncTaskOutputTypeDef,
    TagInputRequestTypeDef,
    TagOutputTypeDef,
    UngroupResourcesInputRequestTypeDef,
    UngroupResourcesOutputTypeDef,
    UntagInputRequestTypeDef,
    UntagOutputTypeDef,
    UpdateAccountSettingsInputRequestTypeDef,
    UpdateAccountSettingsOutputTypeDef,
    UpdateGroupInputRequestTypeDef,
    UpdateGroupOutputTypeDef,
    UpdateGroupQueryInputRequestTypeDef,
    UpdateGroupQueryOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ResourceGroupsClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    MethodNotAllowedException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]

class ResourceGroupsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ResourceGroupsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#close)
        """

    def cancel_tag_sync_task(
        self, **kwargs: Unpack[CancelTagSyncTaskInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels the specified tag-sync task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/cancel_tag_sync_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#cancel_tag_sync_task)
        """

    def create_group(
        self, **kwargs: Unpack[CreateGroupInputRequestTypeDef]
    ) -> CreateGroupOutputTypeDef:
        """
        Creates a resource group with the specified name and description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/create_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#create_group)
        """

    def delete_group(
        self, **kwargs: Unpack[DeleteGroupInputRequestTypeDef]
    ) -> DeleteGroupOutputTypeDef:
        """
        Deletes the specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/delete_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#delete_group)
        """

    def get_account_settings(self) -> GetAccountSettingsOutputTypeDef:
        """
        Retrieves the current status of optional features in Resource Groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_account_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#get_account_settings)
        """

    def get_group(self, **kwargs: Unpack[GetGroupInputRequestTypeDef]) -> GetGroupOutputTypeDef:
        """
        Returns information about a specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#get_group)
        """

    def get_group_configuration(
        self, **kwargs: Unpack[GetGroupConfigurationInputRequestTypeDef]
    ) -> GetGroupConfigurationOutputTypeDef:
        """
        Retrieves the service configuration associated with the specified resource
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_group_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#get_group_configuration)
        """

    def get_group_query(
        self, **kwargs: Unpack[GetGroupQueryInputRequestTypeDef]
    ) -> GetGroupQueryOutputTypeDef:
        """
        Retrieves the resource query associated with the specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_group_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#get_group_query)
        """

    def get_tag_sync_task(
        self, **kwargs: Unpack[GetTagSyncTaskInputRequestTypeDef]
    ) -> GetTagSyncTaskOutputTypeDef:
        """
        Returns information about a specified tag-sync task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_tag_sync_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#get_tag_sync_task)
        """

    def get_tags(self, **kwargs: Unpack[GetTagsInputRequestTypeDef]) -> GetTagsOutputTypeDef:
        """
        Returns a list of tags that are associated with a resource group, specified by
        an Amazon resource name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#get_tags)
        """

    def group_resources(
        self, **kwargs: Unpack[GroupResourcesInputRequestTypeDef]
    ) -> GroupResourcesOutputTypeDef:
        """
        Adds the specified resources to the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/group_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#group_resources)
        """

    def list_group_resources(
        self, **kwargs: Unpack[ListGroupResourcesInputRequestTypeDef]
    ) -> ListGroupResourcesOutputTypeDef:
        """
        Returns a list of Amazon resource names (ARNs) of the resources that are
        members of a specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/list_group_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#list_group_resources)
        """

    def list_grouping_statuses(
        self, **kwargs: Unpack[ListGroupingStatusesInputRequestTypeDef]
    ) -> ListGroupingStatusesOutputTypeDef:
        """
        Returns the status of the last grouping or ungrouping action for each resource
        in the specified application group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/list_grouping_statuses.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#list_grouping_statuses)
        """

    def list_groups(
        self, **kwargs: Unpack[ListGroupsInputRequestTypeDef]
    ) -> ListGroupsOutputTypeDef:
        """
        Returns a list of existing Resource Groups in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/list_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#list_groups)
        """

    def list_tag_sync_tasks(
        self, **kwargs: Unpack[ListTagSyncTasksInputRequestTypeDef]
    ) -> ListTagSyncTasksOutputTypeDef:
        """
        Returns a list of tag-sync tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/list_tag_sync_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#list_tag_sync_tasks)
        """

    def put_group_configuration(
        self, **kwargs: Unpack[PutGroupConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches a service configuration to the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/put_group_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#put_group_configuration)
        """

    def search_resources(
        self, **kwargs: Unpack[SearchResourcesInputRequestTypeDef]
    ) -> SearchResourcesOutputTypeDef:
        """
        Returns a list of Amazon Web Services resource identifiers that matches the
        specified query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/search_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#search_resources)
        """

    def start_tag_sync_task(
        self, **kwargs: Unpack[StartTagSyncTaskInputRequestTypeDef]
    ) -> StartTagSyncTaskOutputTypeDef:
        """
        Creates a new tag-sync task to onboard and sync resources tagged with a
        specific tag key-value pair to an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/start_tag_sync_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#start_tag_sync_task)
        """

    def tag(self, **kwargs: Unpack[TagInputRequestTypeDef]) -> TagOutputTypeDef:
        """
        Adds tags to a resource group with the specified Amazon resource name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/tag.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#tag)
        """

    def ungroup_resources(
        self, **kwargs: Unpack[UngroupResourcesInputRequestTypeDef]
    ) -> UngroupResourcesOutputTypeDef:
        """
        Removes the specified resources from the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/ungroup_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#ungroup_resources)
        """

    def untag(self, **kwargs: Unpack[UntagInputRequestTypeDef]) -> UntagOutputTypeDef:
        """
        Deletes tags from a specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/untag.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#untag)
        """

    def update_account_settings(
        self, **kwargs: Unpack[UpdateAccountSettingsInputRequestTypeDef]
    ) -> UpdateAccountSettingsOutputTypeDef:
        """
        Turns on or turns off optional features in Resource Groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/update_account_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#update_account_settings)
        """

    def update_group(
        self, **kwargs: Unpack[UpdateGroupInputRequestTypeDef]
    ) -> UpdateGroupOutputTypeDef:
        """
        Updates the description for an existing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/update_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#update_group)
        """

    def update_group_query(
        self, **kwargs: Unpack[UpdateGroupQueryInputRequestTypeDef]
    ) -> UpdateGroupQueryOutputTypeDef:
        """
        Updates the resource query of a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/update_group_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#update_group_query)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_resources"]
    ) -> ListGroupResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_grouping_statuses"]
    ) -> ListGroupingStatusesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tag_sync_tasks"]
    ) -> ListTagSyncTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_resources"]
    ) -> SearchResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resource_groups/client/#get_paginator)
        """
