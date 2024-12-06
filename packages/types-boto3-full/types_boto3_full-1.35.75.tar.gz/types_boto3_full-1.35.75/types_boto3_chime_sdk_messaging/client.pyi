"""
Type annotations for chime-sdk-messaging service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_chime_sdk_messaging.client import ChimeSDKMessagingClient

    session = Session()
    client: ChimeSDKMessagingClient = session.client("chime-sdk-messaging")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    AssociateChannelFlowRequestRequestTypeDef,
    BatchCreateChannelMembershipRequestRequestTypeDef,
    BatchCreateChannelMembershipResponseTypeDef,
    ChannelFlowCallbackRequestRequestTypeDef,
    ChannelFlowCallbackResponseTypeDef,
    CreateChannelBanRequestRequestTypeDef,
    CreateChannelBanResponseTypeDef,
    CreateChannelFlowRequestRequestTypeDef,
    CreateChannelFlowResponseTypeDef,
    CreateChannelMembershipRequestRequestTypeDef,
    CreateChannelMembershipResponseTypeDef,
    CreateChannelModeratorRequestRequestTypeDef,
    CreateChannelModeratorResponseTypeDef,
    CreateChannelRequestRequestTypeDef,
    CreateChannelResponseTypeDef,
    DeleteChannelBanRequestRequestTypeDef,
    DeleteChannelFlowRequestRequestTypeDef,
    DeleteChannelMembershipRequestRequestTypeDef,
    DeleteChannelMessageRequestRequestTypeDef,
    DeleteChannelModeratorRequestRequestTypeDef,
    DeleteChannelRequestRequestTypeDef,
    DeleteMessagingStreamingConfigurationsRequestRequestTypeDef,
    DescribeChannelBanRequestRequestTypeDef,
    DescribeChannelBanResponseTypeDef,
    DescribeChannelFlowRequestRequestTypeDef,
    DescribeChannelFlowResponseTypeDef,
    DescribeChannelMembershipForAppInstanceUserRequestRequestTypeDef,
    DescribeChannelMembershipForAppInstanceUserResponseTypeDef,
    DescribeChannelMembershipRequestRequestTypeDef,
    DescribeChannelMembershipResponseTypeDef,
    DescribeChannelModeratedByAppInstanceUserRequestRequestTypeDef,
    DescribeChannelModeratedByAppInstanceUserResponseTypeDef,
    DescribeChannelModeratorRequestRequestTypeDef,
    DescribeChannelModeratorResponseTypeDef,
    DescribeChannelRequestRequestTypeDef,
    DescribeChannelResponseTypeDef,
    DisassociateChannelFlowRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetChannelMembershipPreferencesRequestRequestTypeDef,
    GetChannelMembershipPreferencesResponseTypeDef,
    GetChannelMessageRequestRequestTypeDef,
    GetChannelMessageResponseTypeDef,
    GetChannelMessageStatusRequestRequestTypeDef,
    GetChannelMessageStatusResponseTypeDef,
    GetMessagingSessionEndpointResponseTypeDef,
    GetMessagingStreamingConfigurationsRequestRequestTypeDef,
    GetMessagingStreamingConfigurationsResponseTypeDef,
    ListChannelBansRequestRequestTypeDef,
    ListChannelBansResponseTypeDef,
    ListChannelFlowsRequestRequestTypeDef,
    ListChannelFlowsResponseTypeDef,
    ListChannelMembershipsForAppInstanceUserRequestRequestTypeDef,
    ListChannelMembershipsForAppInstanceUserResponseTypeDef,
    ListChannelMembershipsRequestRequestTypeDef,
    ListChannelMembershipsResponseTypeDef,
    ListChannelMessagesRequestRequestTypeDef,
    ListChannelMessagesResponseTypeDef,
    ListChannelModeratorsRequestRequestTypeDef,
    ListChannelModeratorsResponseTypeDef,
    ListChannelsAssociatedWithChannelFlowRequestRequestTypeDef,
    ListChannelsAssociatedWithChannelFlowResponseTypeDef,
    ListChannelsModeratedByAppInstanceUserRequestRequestTypeDef,
    ListChannelsModeratedByAppInstanceUserResponseTypeDef,
    ListChannelsRequestRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListSubChannelsRequestRequestTypeDef,
    ListSubChannelsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutChannelExpirationSettingsRequestRequestTypeDef,
    PutChannelExpirationSettingsResponseTypeDef,
    PutChannelMembershipPreferencesRequestRequestTypeDef,
    PutChannelMembershipPreferencesResponseTypeDef,
    PutMessagingStreamingConfigurationsRequestRequestTypeDef,
    PutMessagingStreamingConfigurationsResponseTypeDef,
    RedactChannelMessageRequestRequestTypeDef,
    RedactChannelMessageResponseTypeDef,
    SearchChannelsRequestRequestTypeDef,
    SearchChannelsResponseTypeDef,
    SendChannelMessageRequestRequestTypeDef,
    SendChannelMessageResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateChannelFlowRequestRequestTypeDef,
    UpdateChannelFlowResponseTypeDef,
    UpdateChannelMessageRequestRequestTypeDef,
    UpdateChannelMessageResponseTypeDef,
    UpdateChannelReadMarkerRequestRequestTypeDef,
    UpdateChannelReadMarkerResponseTypeDef,
    UpdateChannelRequestRequestTypeDef,
    UpdateChannelResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ChimeSDKMessagingClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottledClientException: Type[BotocoreClientError]
    UnauthorizedClientException: Type[BotocoreClientError]

class ChimeSDKMessagingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging.html#ChimeSDKMessaging.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeSDKMessagingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging.html#ChimeSDKMessaging.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#close)
        """

    def associate_channel_flow(
        self, **kwargs: Unpack[AssociateChannelFlowRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates a channel flow with a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/associate_channel_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#associate_channel_flow)
        """

    def batch_create_channel_membership(
        self, **kwargs: Unpack[BatchCreateChannelMembershipRequestRequestTypeDef]
    ) -> BatchCreateChannelMembershipResponseTypeDef:
        """
        Adds a specified number of users and bots to a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/batch_create_channel_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#batch_create_channel_membership)
        """

    def channel_flow_callback(
        self, **kwargs: Unpack[ChannelFlowCallbackRequestRequestTypeDef]
    ) -> ChannelFlowCallbackResponseTypeDef:
        """
        Calls back Amazon Chime SDK messaging with a processing response message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/channel_flow_callback.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#channel_flow_callback)
        """

    def create_channel(
        self, **kwargs: Unpack[CreateChannelRequestRequestTypeDef]
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a channel to which you can add users and send messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/create_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#create_channel)
        """

    def create_channel_ban(
        self, **kwargs: Unpack[CreateChannelBanRequestRequestTypeDef]
    ) -> CreateChannelBanResponseTypeDef:
        """
        Permanently bans a member from a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/create_channel_ban.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#create_channel_ban)
        """

    def create_channel_flow(
        self, **kwargs: Unpack[CreateChannelFlowRequestRequestTypeDef]
    ) -> CreateChannelFlowResponseTypeDef:
        """
        Creates a channel flow, a container for processors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/create_channel_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#create_channel_flow)
        """

    def create_channel_membership(
        self, **kwargs: Unpack[CreateChannelMembershipRequestRequestTypeDef]
    ) -> CreateChannelMembershipResponseTypeDef:
        """
        Adds a member to a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/create_channel_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#create_channel_membership)
        """

    def create_channel_moderator(
        self, **kwargs: Unpack[CreateChannelModeratorRequestRequestTypeDef]
    ) -> CreateChannelModeratorResponseTypeDef:
        """
        Creates a new <code>ChannelModerator</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/create_channel_moderator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#create_channel_moderator)
        """

    def delete_channel(
        self, **kwargs: Unpack[DeleteChannelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Immediately makes a channel and its memberships inaccessible and marks them for
        deletion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#delete_channel)
        """

    def delete_channel_ban(
        self, **kwargs: Unpack[DeleteChannelBanRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a member from a channel's ban list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_channel_ban.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#delete_channel_ban)
        """

    def delete_channel_flow(
        self, **kwargs: Unpack[DeleteChannelFlowRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a channel flow, an irreversible process.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_channel_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#delete_channel_flow)
        """

    def delete_channel_membership(
        self, **kwargs: Unpack[DeleteChannelMembershipRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a member from a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_channel_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#delete_channel_membership)
        """

    def delete_channel_message(
        self, **kwargs: Unpack[DeleteChannelMessageRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a channel message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_channel_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#delete_channel_message)
        """

    def delete_channel_moderator(
        self, **kwargs: Unpack[DeleteChannelModeratorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a channel moderator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_channel_moderator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#delete_channel_moderator)
        """

    def delete_messaging_streaming_configurations(
        self, **kwargs: Unpack[DeleteMessagingStreamingConfigurationsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the streaming configurations for an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_messaging_streaming_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#delete_messaging_streaming_configurations)
        """

    def describe_channel(
        self, **kwargs: Unpack[DescribeChannelRequestRequestTypeDef]
    ) -> DescribeChannelResponseTypeDef:
        """
        Returns the full details of a channel in an Amazon Chime
        <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#describe_channel)
        """

    def describe_channel_ban(
        self, **kwargs: Unpack[DescribeChannelBanRequestRequestTypeDef]
    ) -> DescribeChannelBanResponseTypeDef:
        """
        Returns the full details of a channel ban.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel_ban.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#describe_channel_ban)
        """

    def describe_channel_flow(
        self, **kwargs: Unpack[DescribeChannelFlowRequestRequestTypeDef]
    ) -> DescribeChannelFlowResponseTypeDef:
        """
        Returns the full details of a channel flow in an Amazon Chime
        <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#describe_channel_flow)
        """

    def describe_channel_membership(
        self, **kwargs: Unpack[DescribeChannelMembershipRequestRequestTypeDef]
    ) -> DescribeChannelMembershipResponseTypeDef:
        """
        Returns the full details of a user's channel membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#describe_channel_membership)
        """

    def describe_channel_membership_for_app_instance_user(
        self, **kwargs: Unpack[DescribeChannelMembershipForAppInstanceUserRequestRequestTypeDef]
    ) -> DescribeChannelMembershipForAppInstanceUserResponseTypeDef:
        """
        Returns the details of a channel based on the membership of the specified
        <code>AppInstanceUser</code> or <code>AppInstanceBot</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel_membership_for_app_instance_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#describe_channel_membership_for_app_instance_user)
        """

    def describe_channel_moderated_by_app_instance_user(
        self, **kwargs: Unpack[DescribeChannelModeratedByAppInstanceUserRequestRequestTypeDef]
    ) -> DescribeChannelModeratedByAppInstanceUserResponseTypeDef:
        """
        Returns the full details of a channel moderated by the specified
        <code>AppInstanceUser</code> or <code>AppInstanceBot</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel_moderated_by_app_instance_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#describe_channel_moderated_by_app_instance_user)
        """

    def describe_channel_moderator(
        self, **kwargs: Unpack[DescribeChannelModeratorRequestRequestTypeDef]
    ) -> DescribeChannelModeratorResponseTypeDef:
        """
        Returns the full details of a single ChannelModerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel_moderator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#describe_channel_moderator)
        """

    def disassociate_channel_flow(
        self, **kwargs: Unpack[DisassociateChannelFlowRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates a channel flow from all its channels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/disassociate_channel_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#disassociate_channel_flow)
        """

    def get_channel_membership_preferences(
        self, **kwargs: Unpack[GetChannelMembershipPreferencesRequestRequestTypeDef]
    ) -> GetChannelMembershipPreferencesResponseTypeDef:
        """
        Gets the membership preferences of an <code>AppInstanceUser</code> or
        <code>AppInstanceBot</code> for the specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/get_channel_membership_preferences.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#get_channel_membership_preferences)
        """

    def get_channel_message(
        self, **kwargs: Unpack[GetChannelMessageRequestRequestTypeDef]
    ) -> GetChannelMessageResponseTypeDef:
        """
        Gets the full details of a channel message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/get_channel_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#get_channel_message)
        """

    def get_channel_message_status(
        self, **kwargs: Unpack[GetChannelMessageStatusRequestRequestTypeDef]
    ) -> GetChannelMessageStatusResponseTypeDef:
        """
        Gets message status for a specified <code>messageId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/get_channel_message_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#get_channel_message_status)
        """

    def get_messaging_session_endpoint(self) -> GetMessagingSessionEndpointResponseTypeDef:
        """
        The details of the endpoint for the messaging session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/get_messaging_session_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#get_messaging_session_endpoint)
        """

    def get_messaging_streaming_configurations(
        self, **kwargs: Unpack[GetMessagingStreamingConfigurationsRequestRequestTypeDef]
    ) -> GetMessagingStreamingConfigurationsResponseTypeDef:
        """
        Retrieves the data streaming configuration for an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/get_messaging_streaming_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#get_messaging_streaming_configurations)
        """

    def list_channel_bans(
        self, **kwargs: Unpack[ListChannelBansRequestRequestTypeDef]
    ) -> ListChannelBansResponseTypeDef:
        """
        Lists all the users and bots banned from a particular channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channel_bans.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#list_channel_bans)
        """

    def list_channel_flows(
        self, **kwargs: Unpack[ListChannelFlowsRequestRequestTypeDef]
    ) -> ListChannelFlowsResponseTypeDef:
        """
        Returns a paginated lists of all the channel flows created under a single Chime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channel_flows.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#list_channel_flows)
        """

    def list_channel_memberships(
        self, **kwargs: Unpack[ListChannelMembershipsRequestRequestTypeDef]
    ) -> ListChannelMembershipsResponseTypeDef:
        """
        Lists all channel memberships in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channel_memberships.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#list_channel_memberships)
        """

    def list_channel_memberships_for_app_instance_user(
        self, **kwargs: Unpack[ListChannelMembershipsForAppInstanceUserRequestRequestTypeDef]
    ) -> ListChannelMembershipsForAppInstanceUserResponseTypeDef:
        """
        Lists all channels that an <code>AppInstanceUser</code> or
        <code>AppInstanceBot</code> is a part of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channel_memberships_for_app_instance_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#list_channel_memberships_for_app_instance_user)
        """

    def list_channel_messages(
        self, **kwargs: Unpack[ListChannelMessagesRequestRequestTypeDef]
    ) -> ListChannelMessagesResponseTypeDef:
        """
        List all the messages in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channel_messages.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#list_channel_messages)
        """

    def list_channel_moderators(
        self, **kwargs: Unpack[ListChannelModeratorsRequestRequestTypeDef]
    ) -> ListChannelModeratorsResponseTypeDef:
        """
        Lists all the moderators for a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channel_moderators.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#list_channel_moderators)
        """

    def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Lists all Channels created under a single Chime App as a paginated list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#list_channels)
        """

    def list_channels_associated_with_channel_flow(
        self, **kwargs: Unpack[ListChannelsAssociatedWithChannelFlowRequestRequestTypeDef]
    ) -> ListChannelsAssociatedWithChannelFlowResponseTypeDef:
        """
        Lists all channels associated with a specified channel flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channels_associated_with_channel_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#list_channels_associated_with_channel_flow)
        """

    def list_channels_moderated_by_app_instance_user(
        self, **kwargs: Unpack[ListChannelsModeratedByAppInstanceUserRequestRequestTypeDef]
    ) -> ListChannelsModeratedByAppInstanceUserResponseTypeDef:
        """
        A list of the channels moderated by an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channels_moderated_by_app_instance_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#list_channels_moderated_by_app_instance_user)
        """

    def list_sub_channels(
        self, **kwargs: Unpack[ListSubChannelsRequestRequestTypeDef]
    ) -> ListSubChannelsResponseTypeDef:
        """
        Lists all the SubChannels in an elastic channel when given a channel ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_sub_channels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#list_sub_channels)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags applied to an Amazon Chime SDK messaging resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#list_tags_for_resource)
        """

    def put_channel_expiration_settings(
        self, **kwargs: Unpack[PutChannelExpirationSettingsRequestRequestTypeDef]
    ) -> PutChannelExpirationSettingsResponseTypeDef:
        """
        Sets the number of days before the channel is automatically deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/put_channel_expiration_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#put_channel_expiration_settings)
        """

    def put_channel_membership_preferences(
        self, **kwargs: Unpack[PutChannelMembershipPreferencesRequestRequestTypeDef]
    ) -> PutChannelMembershipPreferencesResponseTypeDef:
        """
        Sets the membership preferences of an <code>AppInstanceUser</code> or
        <code>AppInstanceBot</code> for the specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/put_channel_membership_preferences.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#put_channel_membership_preferences)
        """

    def put_messaging_streaming_configurations(
        self, **kwargs: Unpack[PutMessagingStreamingConfigurationsRequestRequestTypeDef]
    ) -> PutMessagingStreamingConfigurationsResponseTypeDef:
        """
        Sets the data streaming configuration for an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/put_messaging_streaming_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#put_messaging_streaming_configurations)
        """

    def redact_channel_message(
        self, **kwargs: Unpack[RedactChannelMessageRequestRequestTypeDef]
    ) -> RedactChannelMessageResponseTypeDef:
        """
        Redacts message content, but not metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/redact_channel_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#redact_channel_message)
        """

    def search_channels(
        self, **kwargs: Unpack[SearchChannelsRequestRequestTypeDef]
    ) -> SearchChannelsResponseTypeDef:
        """
        Allows the <code>ChimeBearer</code> to search channels by channel members.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/search_channels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#search_channels)
        """

    def send_channel_message(
        self, **kwargs: Unpack[SendChannelMessageRequestRequestTypeDef]
    ) -> SendChannelMessageResponseTypeDef:
        """
        Sends a message to a particular channel that the member is a part of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/send_channel_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#send_channel_message)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Applies the specified tags to the specified Amazon Chime SDK messaging resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified tags from the specified Amazon Chime SDK messaging
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#untag_resource)
        """

    def update_channel(
        self, **kwargs: Unpack[UpdateChannelRequestRequestTypeDef]
    ) -> UpdateChannelResponseTypeDef:
        """
        Update a channel's attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/update_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#update_channel)
        """

    def update_channel_flow(
        self, **kwargs: Unpack[UpdateChannelFlowRequestRequestTypeDef]
    ) -> UpdateChannelFlowResponseTypeDef:
        """
        Updates channel flow attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/update_channel_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#update_channel_flow)
        """

    def update_channel_message(
        self, **kwargs: Unpack[UpdateChannelMessageRequestRequestTypeDef]
    ) -> UpdateChannelMessageResponseTypeDef:
        """
        Updates the content of a message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/update_channel_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#update_channel_message)
        """

    def update_channel_read_marker(
        self, **kwargs: Unpack[UpdateChannelReadMarkerRequestRequestTypeDef]
    ) -> UpdateChannelReadMarkerResponseTypeDef:
        """
        The details of the time when a user last read messages in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/update_channel_read_marker.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/client/#update_channel_read_marker)
        """
