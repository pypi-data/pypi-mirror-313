"""
Type annotations for chime service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_chime.client import ChimeClient

    session = Session()
    client: ChimeClient = session.client("chime")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListAccountsPaginator, ListUsersPaginator
from .type_defs import (
    AssociatePhoneNumbersWithVoiceConnectorGroupRequestRequestTypeDef,
    AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef,
    AssociatePhoneNumbersWithVoiceConnectorRequestRequestTypeDef,
    AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef,
    AssociatePhoneNumberWithUserRequestRequestTypeDef,
    AssociateSigninDelegateGroupsWithAccountRequestRequestTypeDef,
    BatchCreateAttendeeRequestRequestTypeDef,
    BatchCreateAttendeeResponseTypeDef,
    BatchCreateChannelMembershipRequestRequestTypeDef,
    BatchCreateChannelMembershipResponseTypeDef,
    BatchCreateRoomMembershipRequestRequestTypeDef,
    BatchCreateRoomMembershipResponseTypeDef,
    BatchDeletePhoneNumberRequestRequestTypeDef,
    BatchDeletePhoneNumberResponseTypeDef,
    BatchSuspendUserRequestRequestTypeDef,
    BatchSuspendUserResponseTypeDef,
    BatchUnsuspendUserRequestRequestTypeDef,
    BatchUnsuspendUserResponseTypeDef,
    BatchUpdatePhoneNumberRequestRequestTypeDef,
    BatchUpdatePhoneNumberResponseTypeDef,
    BatchUpdateUserRequestRequestTypeDef,
    BatchUpdateUserResponseTypeDef,
    CreateAccountRequestRequestTypeDef,
    CreateAccountResponseTypeDef,
    CreateAppInstanceAdminRequestRequestTypeDef,
    CreateAppInstanceAdminResponseTypeDef,
    CreateAppInstanceRequestRequestTypeDef,
    CreateAppInstanceResponseTypeDef,
    CreateAppInstanceUserRequestRequestTypeDef,
    CreateAppInstanceUserResponseTypeDef,
    CreateAttendeeRequestRequestTypeDef,
    CreateAttendeeResponseTypeDef,
    CreateBotRequestRequestTypeDef,
    CreateBotResponseTypeDef,
    CreateChannelBanRequestRequestTypeDef,
    CreateChannelBanResponseTypeDef,
    CreateChannelMembershipRequestRequestTypeDef,
    CreateChannelMembershipResponseTypeDef,
    CreateChannelModeratorRequestRequestTypeDef,
    CreateChannelModeratorResponseTypeDef,
    CreateChannelRequestRequestTypeDef,
    CreateChannelResponseTypeDef,
    CreateMediaCapturePipelineRequestRequestTypeDef,
    CreateMediaCapturePipelineResponseTypeDef,
    CreateMeetingDialOutRequestRequestTypeDef,
    CreateMeetingDialOutResponseTypeDef,
    CreateMeetingRequestRequestTypeDef,
    CreateMeetingResponseTypeDef,
    CreateMeetingWithAttendeesRequestRequestTypeDef,
    CreateMeetingWithAttendeesResponseTypeDef,
    CreatePhoneNumberOrderRequestRequestTypeDef,
    CreatePhoneNumberOrderResponseTypeDef,
    CreateProxySessionRequestRequestTypeDef,
    CreateProxySessionResponseTypeDef,
    CreateRoomMembershipRequestRequestTypeDef,
    CreateRoomMembershipResponseTypeDef,
    CreateRoomRequestRequestTypeDef,
    CreateRoomResponseTypeDef,
    CreateSipMediaApplicationCallRequestRequestTypeDef,
    CreateSipMediaApplicationCallResponseTypeDef,
    CreateSipMediaApplicationRequestRequestTypeDef,
    CreateSipMediaApplicationResponseTypeDef,
    CreateSipRuleRequestRequestTypeDef,
    CreateSipRuleResponseTypeDef,
    CreateUserRequestRequestTypeDef,
    CreateUserResponseTypeDef,
    CreateVoiceConnectorGroupRequestRequestTypeDef,
    CreateVoiceConnectorGroupResponseTypeDef,
    CreateVoiceConnectorRequestRequestTypeDef,
    CreateVoiceConnectorResponseTypeDef,
    DeleteAccountRequestRequestTypeDef,
    DeleteAppInstanceAdminRequestRequestTypeDef,
    DeleteAppInstanceRequestRequestTypeDef,
    DeleteAppInstanceStreamingConfigurationsRequestRequestTypeDef,
    DeleteAppInstanceUserRequestRequestTypeDef,
    DeleteAttendeeRequestRequestTypeDef,
    DeleteChannelBanRequestRequestTypeDef,
    DeleteChannelMembershipRequestRequestTypeDef,
    DeleteChannelMessageRequestRequestTypeDef,
    DeleteChannelModeratorRequestRequestTypeDef,
    DeleteChannelRequestRequestTypeDef,
    DeleteEventsConfigurationRequestRequestTypeDef,
    DeleteMediaCapturePipelineRequestRequestTypeDef,
    DeleteMeetingRequestRequestTypeDef,
    DeletePhoneNumberRequestRequestTypeDef,
    DeleteProxySessionRequestRequestTypeDef,
    DeleteRoomMembershipRequestRequestTypeDef,
    DeleteRoomRequestRequestTypeDef,
    DeleteSipMediaApplicationRequestRequestTypeDef,
    DeleteSipRuleRequestRequestTypeDef,
    DeleteVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef,
    DeleteVoiceConnectorGroupRequestRequestTypeDef,
    DeleteVoiceConnectorOriginationRequestRequestTypeDef,
    DeleteVoiceConnectorProxyRequestRequestTypeDef,
    DeleteVoiceConnectorRequestRequestTypeDef,
    DeleteVoiceConnectorStreamingConfigurationRequestRequestTypeDef,
    DeleteVoiceConnectorTerminationCredentialsRequestRequestTypeDef,
    DeleteVoiceConnectorTerminationRequestRequestTypeDef,
    DescribeAppInstanceAdminRequestRequestTypeDef,
    DescribeAppInstanceAdminResponseTypeDef,
    DescribeAppInstanceRequestRequestTypeDef,
    DescribeAppInstanceResponseTypeDef,
    DescribeAppInstanceUserRequestRequestTypeDef,
    DescribeAppInstanceUserResponseTypeDef,
    DescribeChannelBanRequestRequestTypeDef,
    DescribeChannelBanResponseTypeDef,
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
    DisassociatePhoneNumberFromUserRequestRequestTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorGroupRequestRequestTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorRequestRequestTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef,
    DisassociateSigninDelegateGroupsFromAccountRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAccountRequestRequestTypeDef,
    GetAccountResponseTypeDef,
    GetAccountSettingsRequestRequestTypeDef,
    GetAccountSettingsResponseTypeDef,
    GetAppInstanceRetentionSettingsRequestRequestTypeDef,
    GetAppInstanceRetentionSettingsResponseTypeDef,
    GetAppInstanceStreamingConfigurationsRequestRequestTypeDef,
    GetAppInstanceStreamingConfigurationsResponseTypeDef,
    GetAttendeeRequestRequestTypeDef,
    GetAttendeeResponseTypeDef,
    GetBotRequestRequestTypeDef,
    GetBotResponseTypeDef,
    GetChannelMessageRequestRequestTypeDef,
    GetChannelMessageResponseTypeDef,
    GetEventsConfigurationRequestRequestTypeDef,
    GetEventsConfigurationResponseTypeDef,
    GetGlobalSettingsResponseTypeDef,
    GetMediaCapturePipelineRequestRequestTypeDef,
    GetMediaCapturePipelineResponseTypeDef,
    GetMeetingRequestRequestTypeDef,
    GetMeetingResponseTypeDef,
    GetMessagingSessionEndpointResponseTypeDef,
    GetPhoneNumberOrderRequestRequestTypeDef,
    GetPhoneNumberOrderResponseTypeDef,
    GetPhoneNumberRequestRequestTypeDef,
    GetPhoneNumberResponseTypeDef,
    GetPhoneNumberSettingsResponseTypeDef,
    GetProxySessionRequestRequestTypeDef,
    GetProxySessionResponseTypeDef,
    GetRetentionSettingsRequestRequestTypeDef,
    GetRetentionSettingsResponseTypeDef,
    GetRoomRequestRequestTypeDef,
    GetRoomResponseTypeDef,
    GetSipMediaApplicationLoggingConfigurationRequestRequestTypeDef,
    GetSipMediaApplicationLoggingConfigurationResponseTypeDef,
    GetSipMediaApplicationRequestRequestTypeDef,
    GetSipMediaApplicationResponseTypeDef,
    GetSipRuleRequestRequestTypeDef,
    GetSipRuleResponseTypeDef,
    GetUserRequestRequestTypeDef,
    GetUserResponseTypeDef,
    GetUserSettingsRequestRequestTypeDef,
    GetUserSettingsResponseTypeDef,
    GetVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef,
    GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef,
    GetVoiceConnectorGroupRequestRequestTypeDef,
    GetVoiceConnectorGroupResponseTypeDef,
    GetVoiceConnectorLoggingConfigurationRequestRequestTypeDef,
    GetVoiceConnectorLoggingConfigurationResponseTypeDef,
    GetVoiceConnectorOriginationRequestRequestTypeDef,
    GetVoiceConnectorOriginationResponseTypeDef,
    GetVoiceConnectorProxyRequestRequestTypeDef,
    GetVoiceConnectorProxyResponseTypeDef,
    GetVoiceConnectorRequestRequestTypeDef,
    GetVoiceConnectorResponseTypeDef,
    GetVoiceConnectorStreamingConfigurationRequestRequestTypeDef,
    GetVoiceConnectorStreamingConfigurationResponseTypeDef,
    GetVoiceConnectorTerminationHealthRequestRequestTypeDef,
    GetVoiceConnectorTerminationHealthResponseTypeDef,
    GetVoiceConnectorTerminationRequestRequestTypeDef,
    GetVoiceConnectorTerminationResponseTypeDef,
    InviteUsersRequestRequestTypeDef,
    InviteUsersResponseTypeDef,
    ListAccountsRequestRequestTypeDef,
    ListAccountsResponseTypeDef,
    ListAppInstanceAdminsRequestRequestTypeDef,
    ListAppInstanceAdminsResponseTypeDef,
    ListAppInstancesRequestRequestTypeDef,
    ListAppInstancesResponseTypeDef,
    ListAppInstanceUsersRequestRequestTypeDef,
    ListAppInstanceUsersResponseTypeDef,
    ListAttendeesRequestRequestTypeDef,
    ListAttendeesResponseTypeDef,
    ListAttendeeTagsRequestRequestTypeDef,
    ListAttendeeTagsResponseTypeDef,
    ListBotsRequestRequestTypeDef,
    ListBotsResponseTypeDef,
    ListChannelBansRequestRequestTypeDef,
    ListChannelBansResponseTypeDef,
    ListChannelMembershipsForAppInstanceUserRequestRequestTypeDef,
    ListChannelMembershipsForAppInstanceUserResponseTypeDef,
    ListChannelMembershipsRequestRequestTypeDef,
    ListChannelMembershipsResponseTypeDef,
    ListChannelMessagesRequestRequestTypeDef,
    ListChannelMessagesResponseTypeDef,
    ListChannelModeratorsRequestRequestTypeDef,
    ListChannelModeratorsResponseTypeDef,
    ListChannelsModeratedByAppInstanceUserRequestRequestTypeDef,
    ListChannelsModeratedByAppInstanceUserResponseTypeDef,
    ListChannelsRequestRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListMediaCapturePipelinesRequestRequestTypeDef,
    ListMediaCapturePipelinesResponseTypeDef,
    ListMeetingsRequestRequestTypeDef,
    ListMeetingsResponseTypeDef,
    ListMeetingTagsRequestRequestTypeDef,
    ListMeetingTagsResponseTypeDef,
    ListPhoneNumberOrdersRequestRequestTypeDef,
    ListPhoneNumberOrdersResponseTypeDef,
    ListPhoneNumbersRequestRequestTypeDef,
    ListPhoneNumbersResponseTypeDef,
    ListProxySessionsRequestRequestTypeDef,
    ListProxySessionsResponseTypeDef,
    ListRoomMembershipsRequestRequestTypeDef,
    ListRoomMembershipsResponseTypeDef,
    ListRoomsRequestRequestTypeDef,
    ListRoomsResponseTypeDef,
    ListSipMediaApplicationsRequestRequestTypeDef,
    ListSipMediaApplicationsResponseTypeDef,
    ListSipRulesRequestRequestTypeDef,
    ListSipRulesResponseTypeDef,
    ListSupportedPhoneNumberCountriesRequestRequestTypeDef,
    ListSupportedPhoneNumberCountriesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsersRequestRequestTypeDef,
    ListUsersResponseTypeDef,
    ListVoiceConnectorGroupsRequestRequestTypeDef,
    ListVoiceConnectorGroupsResponseTypeDef,
    ListVoiceConnectorsRequestRequestTypeDef,
    ListVoiceConnectorsResponseTypeDef,
    ListVoiceConnectorTerminationCredentialsRequestRequestTypeDef,
    ListVoiceConnectorTerminationCredentialsResponseTypeDef,
    LogoutUserRequestRequestTypeDef,
    PutAppInstanceRetentionSettingsRequestRequestTypeDef,
    PutAppInstanceRetentionSettingsResponseTypeDef,
    PutAppInstanceStreamingConfigurationsRequestRequestTypeDef,
    PutAppInstanceStreamingConfigurationsResponseTypeDef,
    PutEventsConfigurationRequestRequestTypeDef,
    PutEventsConfigurationResponseTypeDef,
    PutRetentionSettingsRequestRequestTypeDef,
    PutRetentionSettingsResponseTypeDef,
    PutSipMediaApplicationLoggingConfigurationRequestRequestTypeDef,
    PutSipMediaApplicationLoggingConfigurationResponseTypeDef,
    PutVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef,
    PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef,
    PutVoiceConnectorLoggingConfigurationRequestRequestTypeDef,
    PutVoiceConnectorLoggingConfigurationResponseTypeDef,
    PutVoiceConnectorOriginationRequestRequestTypeDef,
    PutVoiceConnectorOriginationResponseTypeDef,
    PutVoiceConnectorProxyRequestRequestTypeDef,
    PutVoiceConnectorProxyResponseTypeDef,
    PutVoiceConnectorStreamingConfigurationRequestRequestTypeDef,
    PutVoiceConnectorStreamingConfigurationResponseTypeDef,
    PutVoiceConnectorTerminationCredentialsRequestRequestTypeDef,
    PutVoiceConnectorTerminationRequestRequestTypeDef,
    PutVoiceConnectorTerminationResponseTypeDef,
    RedactChannelMessageRequestRequestTypeDef,
    RedactChannelMessageResponseTypeDef,
    RedactConversationMessageRequestRequestTypeDef,
    RedactRoomMessageRequestRequestTypeDef,
    RegenerateSecurityTokenRequestRequestTypeDef,
    RegenerateSecurityTokenResponseTypeDef,
    ResetPersonalPINRequestRequestTypeDef,
    ResetPersonalPINResponseTypeDef,
    RestorePhoneNumberRequestRequestTypeDef,
    RestorePhoneNumberResponseTypeDef,
    SearchAvailablePhoneNumbersRequestRequestTypeDef,
    SearchAvailablePhoneNumbersResponseTypeDef,
    SendChannelMessageRequestRequestTypeDef,
    SendChannelMessageResponseTypeDef,
    StartMeetingTranscriptionRequestRequestTypeDef,
    StopMeetingTranscriptionRequestRequestTypeDef,
    TagAttendeeRequestRequestTypeDef,
    TagMeetingRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagAttendeeRequestRequestTypeDef,
    UntagMeetingRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAccountRequestRequestTypeDef,
    UpdateAccountResponseTypeDef,
    UpdateAccountSettingsRequestRequestTypeDef,
    UpdateAppInstanceRequestRequestTypeDef,
    UpdateAppInstanceResponseTypeDef,
    UpdateAppInstanceUserRequestRequestTypeDef,
    UpdateAppInstanceUserResponseTypeDef,
    UpdateBotRequestRequestTypeDef,
    UpdateBotResponseTypeDef,
    UpdateChannelMessageRequestRequestTypeDef,
    UpdateChannelMessageResponseTypeDef,
    UpdateChannelReadMarkerRequestRequestTypeDef,
    UpdateChannelReadMarkerResponseTypeDef,
    UpdateChannelRequestRequestTypeDef,
    UpdateChannelResponseTypeDef,
    UpdateGlobalSettingsRequestRequestTypeDef,
    UpdatePhoneNumberRequestRequestTypeDef,
    UpdatePhoneNumberResponseTypeDef,
    UpdatePhoneNumberSettingsRequestRequestTypeDef,
    UpdateProxySessionRequestRequestTypeDef,
    UpdateProxySessionResponseTypeDef,
    UpdateRoomMembershipRequestRequestTypeDef,
    UpdateRoomMembershipResponseTypeDef,
    UpdateRoomRequestRequestTypeDef,
    UpdateRoomResponseTypeDef,
    UpdateSipMediaApplicationCallRequestRequestTypeDef,
    UpdateSipMediaApplicationCallResponseTypeDef,
    UpdateSipMediaApplicationRequestRequestTypeDef,
    UpdateSipMediaApplicationResponseTypeDef,
    UpdateSipRuleRequestRequestTypeDef,
    UpdateSipRuleResponseTypeDef,
    UpdateUserRequestRequestTypeDef,
    UpdateUserResponseTypeDef,
    UpdateUserSettingsRequestRequestTypeDef,
    UpdateVoiceConnectorGroupRequestRequestTypeDef,
    UpdateVoiceConnectorGroupResponseTypeDef,
    UpdateVoiceConnectorRequestRequestTypeDef,
    UpdateVoiceConnectorResponseTypeDef,
    ValidateE911AddressRequestRequestTypeDef,
    ValidateE911AddressResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ChimeClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
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
    UnprocessableEntityException: Type[BotocoreClientError]


class ChimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#close)
        """

    def associate_phone_number_with_user(
        self, **kwargs: Unpack[AssociatePhoneNumberWithUserRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a phone number with the specified Amazon Chime user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/associate_phone_number_with_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#associate_phone_number_with_user)
        """

    def associate_phone_numbers_with_voice_connector(
        self, **kwargs: Unpack[AssociatePhoneNumbersWithVoiceConnectorRequestRequestTypeDef]
    ) -> AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef:
        """
        Associates phone numbers with the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/associate_phone_numbers_with_voice_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#associate_phone_numbers_with_voice_connector)
        """

    def associate_phone_numbers_with_voice_connector_group(
        self, **kwargs: Unpack[AssociatePhoneNumbersWithVoiceConnectorGroupRequestRequestTypeDef]
    ) -> AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef:
        """
        Associates phone numbers with the specified Amazon Chime Voice Connector group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/associate_phone_numbers_with_voice_connector_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#associate_phone_numbers_with_voice_connector_group)
        """

    def associate_signin_delegate_groups_with_account(
        self, **kwargs: Unpack[AssociateSigninDelegateGroupsWithAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates the specified sign-in delegate groups with the specified Amazon
        Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/associate_signin_delegate_groups_with_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#associate_signin_delegate_groups_with_account)
        """

    def batch_create_attendee(
        self, **kwargs: Unpack[BatchCreateAttendeeRequestRequestTypeDef]
    ) -> BatchCreateAttendeeResponseTypeDef:
        """
        Creates up to 100 new attendees for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_create_attendee.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#batch_create_attendee)
        """

    def batch_create_channel_membership(
        self, **kwargs: Unpack[BatchCreateChannelMembershipRequestRequestTypeDef]
    ) -> BatchCreateChannelMembershipResponseTypeDef:
        """
        Adds a specified number of users to a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_create_channel_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#batch_create_channel_membership)
        """

    def batch_create_room_membership(
        self, **kwargs: Unpack[BatchCreateRoomMembershipRequestRequestTypeDef]
    ) -> BatchCreateRoomMembershipResponseTypeDef:
        """
        Adds up to 50 members to a chat room in an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_create_room_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#batch_create_room_membership)
        """

    def batch_delete_phone_number(
        self, **kwargs: Unpack[BatchDeletePhoneNumberRequestRequestTypeDef]
    ) -> BatchDeletePhoneNumberResponseTypeDef:
        """
        Moves phone numbers into the <b>Deletion queue</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_delete_phone_number.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#batch_delete_phone_number)
        """

    def batch_suspend_user(
        self, **kwargs: Unpack[BatchSuspendUserRequestRequestTypeDef]
    ) -> BatchSuspendUserResponseTypeDef:
        """
        Suspends up to 50 users from a <code>Team</code> or <code>EnterpriseLWA</code>
        Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_suspend_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#batch_suspend_user)
        """

    def batch_unsuspend_user(
        self, **kwargs: Unpack[BatchUnsuspendUserRequestRequestTypeDef]
    ) -> BatchUnsuspendUserResponseTypeDef:
        """
        Removes the suspension from up to 50 previously suspended users for the
        specified Amazon Chime <code>EnterpriseLWA</code> account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_unsuspend_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#batch_unsuspend_user)
        """

    def batch_update_phone_number(
        self, **kwargs: Unpack[BatchUpdatePhoneNumberRequestRequestTypeDef]
    ) -> BatchUpdatePhoneNumberResponseTypeDef:
        """
        Updates phone number product types or calling names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_update_phone_number.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#batch_update_phone_number)
        """

    def batch_update_user(
        self, **kwargs: Unpack[BatchUpdateUserRequestRequestTypeDef]
    ) -> BatchUpdateUserResponseTypeDef:
        """
        Updates user details within the <a>UpdateUserRequestItem</a> object for up to
        20 users for the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/batch_update_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#batch_update_user)
        """

    def create_account(
        self, **kwargs: Unpack[CreateAccountRequestRequestTypeDef]
    ) -> CreateAccountResponseTypeDef:
        """
        Creates an Amazon Chime account under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_account)
        """

    def create_app_instance(
        self, **kwargs: Unpack[CreateAppInstanceRequestRequestTypeDef]
    ) -> CreateAppInstanceResponseTypeDef:
        """
        Creates an Amazon Chime SDK messaging <code>AppInstance</code> under an AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_app_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_app_instance)
        """

    def create_app_instance_admin(
        self, **kwargs: Unpack[CreateAppInstanceAdminRequestRequestTypeDef]
    ) -> CreateAppInstanceAdminResponseTypeDef:
        """
        Promotes an <code>AppInstanceUser</code> to an <code>AppInstanceAdmin</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_app_instance_admin.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_app_instance_admin)
        """

    def create_app_instance_user(
        self, **kwargs: Unpack[CreateAppInstanceUserRequestRequestTypeDef]
    ) -> CreateAppInstanceUserResponseTypeDef:
        """
        Creates a user under an Amazon Chime <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_app_instance_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_app_instance_user)
        """

    def create_attendee(
        self, **kwargs: Unpack[CreateAttendeeRequestRequestTypeDef]
    ) -> CreateAttendeeResponseTypeDef:
        """
        Creates a new attendee for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_attendee.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_attendee)
        """

    def create_bot(
        self, **kwargs: Unpack[CreateBotRequestRequestTypeDef]
    ) -> CreateBotResponseTypeDef:
        """
        Creates a bot for an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_bot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_bot)
        """

    def create_channel(
        self, **kwargs: Unpack[CreateChannelRequestRequestTypeDef]
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a channel to which you can add users and send messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_channel)
        """

    def create_channel_ban(
        self, **kwargs: Unpack[CreateChannelBanRequestRequestTypeDef]
    ) -> CreateChannelBanResponseTypeDef:
        """
        Permanently bans a member from a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_channel_ban.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_channel_ban)
        """

    def create_channel_membership(
        self, **kwargs: Unpack[CreateChannelMembershipRequestRequestTypeDef]
    ) -> CreateChannelMembershipResponseTypeDef:
        """
        Adds a user to a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_channel_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_channel_membership)
        """

    def create_channel_moderator(
        self, **kwargs: Unpack[CreateChannelModeratorRequestRequestTypeDef]
    ) -> CreateChannelModeratorResponseTypeDef:
        """
        Creates a new <code>ChannelModerator</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_channel_moderator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_channel_moderator)
        """

    def create_media_capture_pipeline(
        self, **kwargs: Unpack[CreateMediaCapturePipelineRequestRequestTypeDef]
    ) -> CreateMediaCapturePipelineResponseTypeDef:
        """
        Creates a media capture pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_media_capture_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_media_capture_pipeline)
        """

    def create_meeting(
        self, **kwargs: Unpack[CreateMeetingRequestRequestTypeDef]
    ) -> CreateMeetingResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region with no
        initial attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_meeting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_meeting)
        """

    def create_meeting_dial_out(
        self, **kwargs: Unpack[CreateMeetingDialOutRequestRequestTypeDef]
    ) -> CreateMeetingDialOutResponseTypeDef:
        """
        Uses the join token and call metadata in a meeting request (From number, To
        number, and so forth) to initiate an outbound call to a public switched
        telephone network (PSTN) and join them into a Chime meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_meeting_dial_out.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_meeting_dial_out)
        """

    def create_meeting_with_attendees(
        self, **kwargs: Unpack[CreateMeetingWithAttendeesRequestRequestTypeDef]
    ) -> CreateMeetingWithAttendeesResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region, with
        attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_meeting_with_attendees.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_meeting_with_attendees)
        """

    def create_phone_number_order(
        self, **kwargs: Unpack[CreatePhoneNumberOrderRequestRequestTypeDef]
    ) -> CreatePhoneNumberOrderResponseTypeDef:
        """
        Creates an order for phone numbers to be provisioned.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_phone_number_order.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_phone_number_order)
        """

    def create_proxy_session(
        self, **kwargs: Unpack[CreateProxySessionRequestRequestTypeDef]
    ) -> CreateProxySessionResponseTypeDef:
        """
        Creates a proxy session on the specified Amazon Chime Voice Connector for the
        specified participant phone numbers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_proxy_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_proxy_session)
        """

    def create_room(
        self, **kwargs: Unpack[CreateRoomRequestRequestTypeDef]
    ) -> CreateRoomResponseTypeDef:
        """
        Creates a chat room for the specified Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_room.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_room)
        """

    def create_room_membership(
        self, **kwargs: Unpack[CreateRoomMembershipRequestRequestTypeDef]
    ) -> CreateRoomMembershipResponseTypeDef:
        """
        Adds a member to a chat room in an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_room_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_room_membership)
        """

    def create_sip_media_application(
        self, **kwargs: Unpack[CreateSipMediaApplicationRequestRequestTypeDef]
    ) -> CreateSipMediaApplicationResponseTypeDef:
        """
        Creates a SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_sip_media_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_sip_media_application)
        """

    def create_sip_media_application_call(
        self, **kwargs: Unpack[CreateSipMediaApplicationCallRequestRequestTypeDef]
    ) -> CreateSipMediaApplicationCallResponseTypeDef:
        """
        Creates an outbound call to a phone number from the phone number specified in
        the request, and it invokes the endpoint of the specified
        <code>sipMediaApplicationId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_sip_media_application_call.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_sip_media_application_call)
        """

    def create_sip_rule(
        self, **kwargs: Unpack[CreateSipRuleRequestRequestTypeDef]
    ) -> CreateSipRuleResponseTypeDef:
        """
        Creates a SIP rule which can be used to run a SIP media application as a target
        for a specific trigger type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_sip_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_sip_rule)
        """

    def create_user(
        self, **kwargs: Unpack[CreateUserRequestRequestTypeDef]
    ) -> CreateUserResponseTypeDef:
        """
        Creates a user under the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_user)
        """

    def create_voice_connector(
        self, **kwargs: Unpack[CreateVoiceConnectorRequestRequestTypeDef]
    ) -> CreateVoiceConnectorResponseTypeDef:
        """
        Creates an Amazon Chime Voice Connector under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_voice_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_voice_connector)
        """

    def create_voice_connector_group(
        self, **kwargs: Unpack[CreateVoiceConnectorGroupRequestRequestTypeDef]
    ) -> CreateVoiceConnectorGroupResponseTypeDef:
        """
        Creates an Amazon Chime Voice Connector group under the administrator's AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/create_voice_connector_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#create_voice_connector_group)
        """

    def delete_account(
        self, **kwargs: Unpack[DeleteAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_account)
        """

    def delete_app_instance(
        self, **kwargs: Unpack[DeleteAppInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an <code>AppInstance</code> and all associated data asynchronously.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_app_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_app_instance)
        """

    def delete_app_instance_admin(
        self, **kwargs: Unpack[DeleteAppInstanceAdminRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Demotes an <code>AppInstanceAdmin</code> to an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_app_instance_admin.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_app_instance_admin)
        """

    def delete_app_instance_streaming_configurations(
        self, **kwargs: Unpack[DeleteAppInstanceStreamingConfigurationsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the streaming configurations of an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_app_instance_streaming_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_app_instance_streaming_configurations)
        """

    def delete_app_instance_user(
        self, **kwargs: Unpack[DeleteAppInstanceUserRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_app_instance_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_app_instance_user)
        """

    def delete_attendee(
        self, **kwargs: Unpack[DeleteAttendeeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an attendee from the specified Amazon Chime SDK meeting and deletes
        their <code>JoinToken</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_attendee.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_attendee)
        """

    def delete_channel(
        self, **kwargs: Unpack[DeleteChannelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Immediately makes a channel and its memberships inaccessible and marks them for
        deletion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_channel)
        """

    def delete_channel_ban(
        self, **kwargs: Unpack[DeleteChannelBanRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a user from a channel's ban list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_channel_ban.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_channel_ban)
        """

    def delete_channel_membership(
        self, **kwargs: Unpack[DeleteChannelMembershipRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a member from a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_channel_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_channel_membership)
        """

    def delete_channel_message(
        self, **kwargs: Unpack[DeleteChannelMessageRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a channel message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_channel_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_channel_message)
        """

    def delete_channel_moderator(
        self, **kwargs: Unpack[DeleteChannelModeratorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a channel moderator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_channel_moderator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_channel_moderator)
        """

    def delete_events_configuration(
        self, **kwargs: Unpack[DeleteEventsConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the events configuration that allows a bot to receive outgoing events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_events_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_events_configuration)
        """

    def delete_media_capture_pipeline(
        self, **kwargs: Unpack[DeleteMediaCapturePipelineRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the media capture pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_media_capture_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_media_capture_pipeline)
        """

    def delete_meeting(
        self, **kwargs: Unpack[DeleteMeetingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_meeting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_meeting)
        """

    def delete_phone_number(
        self, **kwargs: Unpack[DeletePhoneNumberRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Moves the specified phone number into the <b>Deletion queue</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_phone_number.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_phone_number)
        """

    def delete_proxy_session(
        self, **kwargs: Unpack[DeleteProxySessionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified proxy session from the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_proxy_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_proxy_session)
        """

    def delete_room(
        self, **kwargs: Unpack[DeleteRoomRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a chat room in an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_room.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_room)
        """

    def delete_room_membership(
        self, **kwargs: Unpack[DeleteRoomMembershipRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a member from a chat room in an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_room_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_room_membership)
        """

    def delete_sip_media_application(
        self, **kwargs: Unpack[DeleteSipMediaApplicationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_sip_media_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_sip_media_application)
        """

    def delete_sip_rule(
        self, **kwargs: Unpack[DeleteSipRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a SIP rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_sip_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_sip_rule)
        """

    def delete_voice_connector(
        self, **kwargs: Unpack[DeleteVoiceConnectorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_voice_connector)
        """

    def delete_voice_connector_emergency_calling_configuration(
        self,
        **kwargs: Unpack[DeleteVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef],
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the emergency calling configuration details from the specified Amazon
        Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_emergency_calling_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_voice_connector_emergency_calling_configuration)
        """

    def delete_voice_connector_group(
        self, **kwargs: Unpack[DeleteVoiceConnectorGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Amazon Chime Voice Connector group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_voice_connector_group)
        """

    def delete_voice_connector_origination(
        self, **kwargs: Unpack[DeleteVoiceConnectorOriginationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the origination settings for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_origination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_voice_connector_origination)
        """

    def delete_voice_connector_proxy(
        self, **kwargs: Unpack[DeleteVoiceConnectorProxyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the proxy configuration from the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_proxy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_voice_connector_proxy)
        """

    def delete_voice_connector_streaming_configuration(
        self, **kwargs: Unpack[DeleteVoiceConnectorStreamingConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the streaming configuration for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_streaming_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_voice_connector_streaming_configuration)
        """

    def delete_voice_connector_termination(
        self, **kwargs: Unpack[DeleteVoiceConnectorTerminationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the termination settings for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_termination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_voice_connector_termination)
        """

    def delete_voice_connector_termination_credentials(
        self, **kwargs: Unpack[DeleteVoiceConnectorTerminationCredentialsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified SIP credentials used by your equipment to authenticate
        during call termination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/delete_voice_connector_termination_credentials.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#delete_voice_connector_termination_credentials)
        """

    def describe_app_instance(
        self, **kwargs: Unpack[DescribeAppInstanceRequestRequestTypeDef]
    ) -> DescribeAppInstanceResponseTypeDef:
        """
        Returns the full details of an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_app_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#describe_app_instance)
        """

    def describe_app_instance_admin(
        self, **kwargs: Unpack[DescribeAppInstanceAdminRequestRequestTypeDef]
    ) -> DescribeAppInstanceAdminResponseTypeDef:
        """
        Returns the full details of an <code>AppInstanceAdmin</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_app_instance_admin.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#describe_app_instance_admin)
        """

    def describe_app_instance_user(
        self, **kwargs: Unpack[DescribeAppInstanceUserRequestRequestTypeDef]
    ) -> DescribeAppInstanceUserResponseTypeDef:
        """
        Returns the full details of an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_app_instance_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#describe_app_instance_user)
        """

    def describe_channel(
        self, **kwargs: Unpack[DescribeChannelRequestRequestTypeDef]
    ) -> DescribeChannelResponseTypeDef:
        """
        Returns the full details of a channel in an Amazon Chime
        <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#describe_channel)
        """

    def describe_channel_ban(
        self, **kwargs: Unpack[DescribeChannelBanRequestRequestTypeDef]
    ) -> DescribeChannelBanResponseTypeDef:
        """
        Returns the full details of a channel ban.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_channel_ban.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#describe_channel_ban)
        """

    def describe_channel_membership(
        self, **kwargs: Unpack[DescribeChannelMembershipRequestRequestTypeDef]
    ) -> DescribeChannelMembershipResponseTypeDef:
        """
        Returns the full details of a user's channel membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_channel_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#describe_channel_membership)
        """

    def describe_channel_membership_for_app_instance_user(
        self, **kwargs: Unpack[DescribeChannelMembershipForAppInstanceUserRequestRequestTypeDef]
    ) -> DescribeChannelMembershipForAppInstanceUserResponseTypeDef:
        """
        Returns the details of a channel based on the membership of the specified
        <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_channel_membership_for_app_instance_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#describe_channel_membership_for_app_instance_user)
        """

    def describe_channel_moderated_by_app_instance_user(
        self, **kwargs: Unpack[DescribeChannelModeratedByAppInstanceUserRequestRequestTypeDef]
    ) -> DescribeChannelModeratedByAppInstanceUserResponseTypeDef:
        """
        Returns the full details of a channel moderated by the specified
        <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_channel_moderated_by_app_instance_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#describe_channel_moderated_by_app_instance_user)
        """

    def describe_channel_moderator(
        self, **kwargs: Unpack[DescribeChannelModeratorRequestRequestTypeDef]
    ) -> DescribeChannelModeratorResponseTypeDef:
        """
        Returns the full details of a single ChannelModerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/describe_channel_moderator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#describe_channel_moderator)
        """

    def disassociate_phone_number_from_user(
        self, **kwargs: Unpack[DisassociatePhoneNumberFromUserRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the primary provisioned phone number from the specified Amazon
        Chime user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/disassociate_phone_number_from_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#disassociate_phone_number_from_user)
        """

    def disassociate_phone_numbers_from_voice_connector(
        self, **kwargs: Unpack[DisassociatePhoneNumbersFromVoiceConnectorRequestRequestTypeDef]
    ) -> DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef:
        """
        Disassociates the specified phone numbers from the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/disassociate_phone_numbers_from_voice_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#disassociate_phone_numbers_from_voice_connector)
        """

    def disassociate_phone_numbers_from_voice_connector_group(
        self, **kwargs: Unpack[DisassociatePhoneNumbersFromVoiceConnectorGroupRequestRequestTypeDef]
    ) -> DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef:
        """
        Disassociates the specified phone numbers from the specified Amazon Chime Voice
        Connector group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/disassociate_phone_numbers_from_voice_connector_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#disassociate_phone_numbers_from_voice_connector_group)
        """

    def disassociate_signin_delegate_groups_from_account(
        self, **kwargs: Unpack[DisassociateSigninDelegateGroupsFromAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified sign-in delegate groups from the specified Amazon
        Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/disassociate_signin_delegate_groups_from_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#disassociate_signin_delegate_groups_from_account)
        """

    def get_account(
        self, **kwargs: Unpack[GetAccountRequestRequestTypeDef]
    ) -> GetAccountResponseTypeDef:
        """
        Retrieves details for the specified Amazon Chime account, such as account type
        and supported licenses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_account)
        """

    def get_account_settings(
        self, **kwargs: Unpack[GetAccountSettingsRequestRequestTypeDef]
    ) -> GetAccountSettingsResponseTypeDef:
        """
        Retrieves account settings for the specified Amazon Chime account ID, such as
        remote control and dialout settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_account_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_account_settings)
        """

    def get_app_instance_retention_settings(
        self, **kwargs: Unpack[GetAppInstanceRetentionSettingsRequestRequestTypeDef]
    ) -> GetAppInstanceRetentionSettingsResponseTypeDef:
        """
        Gets the retention settings for an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_app_instance_retention_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_app_instance_retention_settings)
        """

    def get_app_instance_streaming_configurations(
        self, **kwargs: Unpack[GetAppInstanceStreamingConfigurationsRequestRequestTypeDef]
    ) -> GetAppInstanceStreamingConfigurationsResponseTypeDef:
        """
        Gets the streaming settings for an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_app_instance_streaming_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_app_instance_streaming_configurations)
        """

    def get_attendee(
        self, **kwargs: Unpack[GetAttendeeRequestRequestTypeDef]
    ) -> GetAttendeeResponseTypeDef:
        """
        Gets the Amazon Chime SDK attendee details for a specified meeting ID and
        attendee ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_attendee.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_attendee)
        """

    def get_bot(self, **kwargs: Unpack[GetBotRequestRequestTypeDef]) -> GetBotResponseTypeDef:
        """
        Retrieves details for the specified bot, such as bot email address, bot type,
        status, and display name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_bot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_bot)
        """

    def get_channel_message(
        self, **kwargs: Unpack[GetChannelMessageRequestRequestTypeDef]
    ) -> GetChannelMessageResponseTypeDef:
        """
        Gets the full details of a channel message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_channel_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_channel_message)
        """

    def get_events_configuration(
        self, **kwargs: Unpack[GetEventsConfigurationRequestRequestTypeDef]
    ) -> GetEventsConfigurationResponseTypeDef:
        """
        Gets details for an events configuration that allows a bot to receive outgoing
        events, such as an HTTPS endpoint or Lambda function ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_events_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_events_configuration)
        """

    def get_global_settings(self) -> GetGlobalSettingsResponseTypeDef:
        """
        Retrieves global settings for the administrator's AWS account, such as Amazon
        Chime Business Calling and Amazon Chime Voice Connector settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_global_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_global_settings)
        """

    def get_media_capture_pipeline(
        self, **kwargs: Unpack[GetMediaCapturePipelineRequestRequestTypeDef]
    ) -> GetMediaCapturePipelineResponseTypeDef:
        """
        Gets an existing media capture pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_media_capture_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_media_capture_pipeline)
        """

    def get_meeting(
        self, **kwargs: Unpack[GetMeetingRequestRequestTypeDef]
    ) -> GetMeetingResponseTypeDef:
        """
        <b>This API is is no longer supported and will not be updated.</b> We recommend
        using the latest version, <a
        href="https://docs.aws.amazon.com/chime-sdk/latest/APIReference/API_meeting-chime_GetMeeting.html">GetMeeting</a>,
        in the Amazon Chime SDK.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_meeting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_meeting)
        """

    def get_messaging_session_endpoint(self) -> GetMessagingSessionEndpointResponseTypeDef:
        """
        The details of the endpoint for the messaging session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_messaging_session_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_messaging_session_endpoint)
        """

    def get_phone_number(
        self, **kwargs: Unpack[GetPhoneNumberRequestRequestTypeDef]
    ) -> GetPhoneNumberResponseTypeDef:
        """
        Retrieves details for the specified phone number ID, such as associations,
        capabilities, and product type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_phone_number.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_phone_number)
        """

    def get_phone_number_order(
        self, **kwargs: Unpack[GetPhoneNumberOrderRequestRequestTypeDef]
    ) -> GetPhoneNumberOrderResponseTypeDef:
        """
        Retrieves details for the specified phone number order, such as the order
        creation timestamp, phone numbers in E.164 format, product type, and order
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_phone_number_order.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_phone_number_order)
        """

    def get_phone_number_settings(self) -> GetPhoneNumberSettingsResponseTypeDef:
        """
        Retrieves the phone number settings for the administrator's AWS account, such
        as the default outbound calling name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_phone_number_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_phone_number_settings)
        """

    def get_proxy_session(
        self, **kwargs: Unpack[GetProxySessionRequestRequestTypeDef]
    ) -> GetProxySessionResponseTypeDef:
        """
        Gets the specified proxy session details for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_proxy_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_proxy_session)
        """

    def get_retention_settings(
        self, **kwargs: Unpack[GetRetentionSettingsRequestRequestTypeDef]
    ) -> GetRetentionSettingsResponseTypeDef:
        """
        Gets the retention settings for the specified Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_retention_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_retention_settings)
        """

    def get_room(self, **kwargs: Unpack[GetRoomRequestRequestTypeDef]) -> GetRoomResponseTypeDef:
        """
        Retrieves room details, such as the room name, for a room in an Amazon Chime
        Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_room.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_room)
        """

    def get_sip_media_application(
        self, **kwargs: Unpack[GetSipMediaApplicationRequestRequestTypeDef]
    ) -> GetSipMediaApplicationResponseTypeDef:
        """
        Retrieves the information for a SIP media application, including name, AWS
        Region, and endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_sip_media_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_sip_media_application)
        """

    def get_sip_media_application_logging_configuration(
        self, **kwargs: Unpack[GetSipMediaApplicationLoggingConfigurationRequestRequestTypeDef]
    ) -> GetSipMediaApplicationLoggingConfigurationResponseTypeDef:
        """
        Returns the logging configuration for the specified SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_sip_media_application_logging_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_sip_media_application_logging_configuration)
        """

    def get_sip_rule(
        self, **kwargs: Unpack[GetSipRuleRequestRequestTypeDef]
    ) -> GetSipRuleResponseTypeDef:
        """
        Retrieves the details of a SIP rule, such as the rule ID, name, triggers, and
        target endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_sip_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_sip_rule)
        """

    def get_user(self, **kwargs: Unpack[GetUserRequestRequestTypeDef]) -> GetUserResponseTypeDef:
        """
        Retrieves details for the specified user ID, such as primary email address,
        license type,and personal meeting PIN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_user)
        """

    def get_user_settings(
        self, **kwargs: Unpack[GetUserSettingsRequestRequestTypeDef]
    ) -> GetUserSettingsResponseTypeDef:
        """
        Retrieves settings for the specified user ID, such as any associated phone
        number settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_user_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_user_settings)
        """

    def get_voice_connector(
        self, **kwargs: Unpack[GetVoiceConnectorRequestRequestTypeDef]
    ) -> GetVoiceConnectorResponseTypeDef:
        """
        Retrieves details for the specified Amazon Chime Voice Connector, such as
        timestamps,name, outbound host, and encryption requirements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_voice_connector)
        """

    def get_voice_connector_emergency_calling_configuration(
        self, **kwargs: Unpack[GetVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef]
    ) -> GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef:
        """
        Gets the emergency calling configuration details for the specified Amazon Chime
        Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_emergency_calling_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_voice_connector_emergency_calling_configuration)
        """

    def get_voice_connector_group(
        self, **kwargs: Unpack[GetVoiceConnectorGroupRequestRequestTypeDef]
    ) -> GetVoiceConnectorGroupResponseTypeDef:
        """
        Retrieves details for the specified Amazon Chime Voice Connector group, such as
        timestamps,name, and associated <code>VoiceConnectorItems</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_voice_connector_group)
        """

    def get_voice_connector_logging_configuration(
        self, **kwargs: Unpack[GetVoiceConnectorLoggingConfigurationRequestRequestTypeDef]
    ) -> GetVoiceConnectorLoggingConfigurationResponseTypeDef:
        """
        Retrieves the logging configuration details for the specified Amazon Chime
        Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_logging_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_voice_connector_logging_configuration)
        """

    def get_voice_connector_origination(
        self, **kwargs: Unpack[GetVoiceConnectorOriginationRequestRequestTypeDef]
    ) -> GetVoiceConnectorOriginationResponseTypeDef:
        """
        Retrieves origination setting details for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_origination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_voice_connector_origination)
        """

    def get_voice_connector_proxy(
        self, **kwargs: Unpack[GetVoiceConnectorProxyRequestRequestTypeDef]
    ) -> GetVoiceConnectorProxyResponseTypeDef:
        """
        Gets the proxy configuration details for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_proxy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_voice_connector_proxy)
        """

    def get_voice_connector_streaming_configuration(
        self, **kwargs: Unpack[GetVoiceConnectorStreamingConfigurationRequestRequestTypeDef]
    ) -> GetVoiceConnectorStreamingConfigurationResponseTypeDef:
        """
        Retrieves the streaming configuration details for the specified Amazon Chime
        Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_streaming_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_voice_connector_streaming_configuration)
        """

    def get_voice_connector_termination(
        self, **kwargs: Unpack[GetVoiceConnectorTerminationRequestRequestTypeDef]
    ) -> GetVoiceConnectorTerminationResponseTypeDef:
        """
        Retrieves termination setting details for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_termination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_voice_connector_termination)
        """

    def get_voice_connector_termination_health(
        self, **kwargs: Unpack[GetVoiceConnectorTerminationHealthRequestRequestTypeDef]
    ) -> GetVoiceConnectorTerminationHealthResponseTypeDef:
        """
        <b>This API is is no longer supported and will not be updated.</b> We recommend
        using the latest version, <a
        href="https://docs.aws.amazon.com/chime-sdk/latest/APIReference/API_voice-chime_GetVoiceConnectorTerminationHealth.html">GetVoiceConnectorTerminationHealth</a>,
        in the Amazon Chime SDK.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_voice_connector_termination_health.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_voice_connector_termination_health)
        """

    def invite_users(
        self, **kwargs: Unpack[InviteUsersRequestRequestTypeDef]
    ) -> InviteUsersResponseTypeDef:
        """
        Sends email to a maximum of 50 users, inviting them to the specified Amazon
        Chime <code>Team</code> account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/invite_users.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#invite_users)
        """

    def list_accounts(
        self, **kwargs: Unpack[ListAccountsRequestRequestTypeDef]
    ) -> ListAccountsResponseTypeDef:
        """
        Lists the Amazon Chime accounts under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_accounts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_accounts)
        """

    def list_app_instance_admins(
        self, **kwargs: Unpack[ListAppInstanceAdminsRequestRequestTypeDef]
    ) -> ListAppInstanceAdminsResponseTypeDef:
        """
        Returns a list of the administrators in the <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_app_instance_admins.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_app_instance_admins)
        """

    def list_app_instance_users(
        self, **kwargs: Unpack[ListAppInstanceUsersRequestRequestTypeDef]
    ) -> ListAppInstanceUsersResponseTypeDef:
        """
        List all <code>AppInstanceUsers</code> created under a single
        <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_app_instance_users.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_app_instance_users)
        """

    def list_app_instances(
        self, **kwargs: Unpack[ListAppInstancesRequestRequestTypeDef]
    ) -> ListAppInstancesResponseTypeDef:
        """
        Lists all Amazon Chime <code>AppInstance</code>s created under a single AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_app_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_app_instances)
        """

    def list_attendee_tags(
        self, **kwargs: Unpack[ListAttendeeTagsRequestRequestTypeDef]
    ) -> ListAttendeeTagsResponseTypeDef:
        """
        Lists the tags applied to an Amazon Chime SDK attendee resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_attendee_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_attendee_tags)
        """

    def list_attendees(
        self, **kwargs: Unpack[ListAttendeesRequestRequestTypeDef]
    ) -> ListAttendeesResponseTypeDef:
        """
        Lists the attendees for the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_attendees.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_attendees)
        """

    def list_bots(self, **kwargs: Unpack[ListBotsRequestRequestTypeDef]) -> ListBotsResponseTypeDef:
        """
        Lists the bots associated with the administrator's Amazon Chime Enterprise
        account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_bots.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_bots)
        """

    def list_channel_bans(
        self, **kwargs: Unpack[ListChannelBansRequestRequestTypeDef]
    ) -> ListChannelBansResponseTypeDef:
        """
        Lists all the users banned from a particular channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channel_bans.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_channel_bans)
        """

    def list_channel_memberships(
        self, **kwargs: Unpack[ListChannelMembershipsRequestRequestTypeDef]
    ) -> ListChannelMembershipsResponseTypeDef:
        """
        Lists all channel memberships in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channel_memberships.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_channel_memberships)
        """

    def list_channel_memberships_for_app_instance_user(
        self, **kwargs: Unpack[ListChannelMembershipsForAppInstanceUserRequestRequestTypeDef]
    ) -> ListChannelMembershipsForAppInstanceUserResponseTypeDef:
        """
        Lists all channels that a particular <code>AppInstanceUser</code> is a part of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channel_memberships_for_app_instance_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_channel_memberships_for_app_instance_user)
        """

    def list_channel_messages(
        self, **kwargs: Unpack[ListChannelMessagesRequestRequestTypeDef]
    ) -> ListChannelMessagesResponseTypeDef:
        """
        List all the messages in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channel_messages.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_channel_messages)
        """

    def list_channel_moderators(
        self, **kwargs: Unpack[ListChannelModeratorsRequestRequestTypeDef]
    ) -> ListChannelModeratorsResponseTypeDef:
        """
        Lists all the moderators for a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channel_moderators.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_channel_moderators)
        """

    def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Lists all Channels created under a single Chime App as a paginated list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_channels)
        """

    def list_channels_moderated_by_app_instance_user(
        self, **kwargs: Unpack[ListChannelsModeratedByAppInstanceUserRequestRequestTypeDef]
    ) -> ListChannelsModeratedByAppInstanceUserResponseTypeDef:
        """
        A list of the channels moderated by an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_channels_moderated_by_app_instance_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_channels_moderated_by_app_instance_user)
        """

    def list_media_capture_pipelines(
        self, **kwargs: Unpack[ListMediaCapturePipelinesRequestRequestTypeDef]
    ) -> ListMediaCapturePipelinesResponseTypeDef:
        """
        Returns a list of media capture pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_media_capture_pipelines.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_media_capture_pipelines)
        """

    def list_meeting_tags(
        self, **kwargs: Unpack[ListMeetingTagsRequestRequestTypeDef]
    ) -> ListMeetingTagsResponseTypeDef:
        """
        Lists the tags applied to an Amazon Chime SDK meeting resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_meeting_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_meeting_tags)
        """

    def list_meetings(
        self, **kwargs: Unpack[ListMeetingsRequestRequestTypeDef]
    ) -> ListMeetingsResponseTypeDef:
        """
        Lists up to 100 active Amazon Chime SDK meetings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_meetings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_meetings)
        """

    def list_phone_number_orders(
        self, **kwargs: Unpack[ListPhoneNumberOrdersRequestRequestTypeDef]
    ) -> ListPhoneNumberOrdersResponseTypeDef:
        """
        Lists the phone number orders for the administrator's Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_phone_number_orders.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_phone_number_orders)
        """

    def list_phone_numbers(
        self, **kwargs: Unpack[ListPhoneNumbersRequestRequestTypeDef]
    ) -> ListPhoneNumbersResponseTypeDef:
        """
        Lists the phone numbers for the specified Amazon Chime account, Amazon Chime
        user, Amazon Chime Voice Connector, or Amazon Chime Voice Connector group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_phone_numbers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_phone_numbers)
        """

    def list_proxy_sessions(
        self, **kwargs: Unpack[ListProxySessionsRequestRequestTypeDef]
    ) -> ListProxySessionsResponseTypeDef:
        """
        Lists the proxy sessions for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_proxy_sessions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_proxy_sessions)
        """

    def list_room_memberships(
        self, **kwargs: Unpack[ListRoomMembershipsRequestRequestTypeDef]
    ) -> ListRoomMembershipsResponseTypeDef:
        """
        Lists the membership details for the specified room in an Amazon Chime
        Enterprise account, such as the members' IDs, email addresses, and names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_room_memberships.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_room_memberships)
        """

    def list_rooms(
        self, **kwargs: Unpack[ListRoomsRequestRequestTypeDef]
    ) -> ListRoomsResponseTypeDef:
        """
        Lists the room details for the specified Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_rooms.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_rooms)
        """

    def list_sip_media_applications(
        self, **kwargs: Unpack[ListSipMediaApplicationsRequestRequestTypeDef]
    ) -> ListSipMediaApplicationsResponseTypeDef:
        """
        Lists the SIP media applications under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_sip_media_applications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_sip_media_applications)
        """

    def list_sip_rules(
        self, **kwargs: Unpack[ListSipRulesRequestRequestTypeDef]
    ) -> ListSipRulesResponseTypeDef:
        """
        Lists the SIP rules under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_sip_rules.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_sip_rules)
        """

    def list_supported_phone_number_countries(
        self, **kwargs: Unpack[ListSupportedPhoneNumberCountriesRequestRequestTypeDef]
    ) -> ListSupportedPhoneNumberCountriesResponseTypeDef:
        """
        Lists supported phone number countries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_supported_phone_number_countries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_supported_phone_number_countries)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags applied to an Amazon Chime SDK meeting and messaging resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_tags_for_resource)
        """

    def list_users(
        self, **kwargs: Unpack[ListUsersRequestRequestTypeDef]
    ) -> ListUsersResponseTypeDef:
        """
        Lists the users that belong to the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_users.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_users)
        """

    def list_voice_connector_groups(
        self, **kwargs: Unpack[ListVoiceConnectorGroupsRequestRequestTypeDef]
    ) -> ListVoiceConnectorGroupsResponseTypeDef:
        """
        Lists the Amazon Chime Voice Connector groups for the administrator's AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_voice_connector_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_voice_connector_groups)
        """

    def list_voice_connector_termination_credentials(
        self, **kwargs: Unpack[ListVoiceConnectorTerminationCredentialsRequestRequestTypeDef]
    ) -> ListVoiceConnectorTerminationCredentialsResponseTypeDef:
        """
        Lists the SIP credentials for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_voice_connector_termination_credentials.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_voice_connector_termination_credentials)
        """

    def list_voice_connectors(
        self, **kwargs: Unpack[ListVoiceConnectorsRequestRequestTypeDef]
    ) -> ListVoiceConnectorsResponseTypeDef:
        """
        Lists the Amazon Chime Voice Connectors for the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/list_voice_connectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#list_voice_connectors)
        """

    def logout_user(self, **kwargs: Unpack[LogoutUserRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Logs out the specified user from all of the devices they are currently logged
        into.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/logout_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#logout_user)
        """

    def put_app_instance_retention_settings(
        self, **kwargs: Unpack[PutAppInstanceRetentionSettingsRequestRequestTypeDef]
    ) -> PutAppInstanceRetentionSettingsResponseTypeDef:
        """
        Sets the amount of time in days that a given <code>AppInstance</code> retains
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_app_instance_retention_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#put_app_instance_retention_settings)
        """

    def put_app_instance_streaming_configurations(
        self, **kwargs: Unpack[PutAppInstanceStreamingConfigurationsRequestRequestTypeDef]
    ) -> PutAppInstanceStreamingConfigurationsResponseTypeDef:
        """
        The data streaming configurations of an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_app_instance_streaming_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#put_app_instance_streaming_configurations)
        """

    def put_events_configuration(
        self, **kwargs: Unpack[PutEventsConfigurationRequestRequestTypeDef]
    ) -> PutEventsConfigurationResponseTypeDef:
        """
        Creates an events configuration that allows a bot to receive outgoing events
        sent by Amazon Chime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_events_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#put_events_configuration)
        """

    def put_retention_settings(
        self, **kwargs: Unpack[PutRetentionSettingsRequestRequestTypeDef]
    ) -> PutRetentionSettingsResponseTypeDef:
        """
        Puts retention settings for the specified Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_retention_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#put_retention_settings)
        """

    def put_sip_media_application_logging_configuration(
        self, **kwargs: Unpack[PutSipMediaApplicationLoggingConfigurationRequestRequestTypeDef]
    ) -> PutSipMediaApplicationLoggingConfigurationResponseTypeDef:
        """
        Updates the logging configuration for the specified SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_sip_media_application_logging_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#put_sip_media_application_logging_configuration)
        """

    def put_voice_connector_emergency_calling_configuration(
        self, **kwargs: Unpack[PutVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef]
    ) -> PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef:
        """
        Puts emergency calling configuration details to the specified Amazon Chime
        Voice Connector, such as emergency phone numbers and calling countries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_emergency_calling_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#put_voice_connector_emergency_calling_configuration)
        """

    def put_voice_connector_logging_configuration(
        self, **kwargs: Unpack[PutVoiceConnectorLoggingConfigurationRequestRequestTypeDef]
    ) -> PutVoiceConnectorLoggingConfigurationResponseTypeDef:
        """
        Adds a logging configuration for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_logging_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#put_voice_connector_logging_configuration)
        """

    def put_voice_connector_origination(
        self, **kwargs: Unpack[PutVoiceConnectorOriginationRequestRequestTypeDef]
    ) -> PutVoiceConnectorOriginationResponseTypeDef:
        """
        Adds origination settings for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_origination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#put_voice_connector_origination)
        """

    def put_voice_connector_proxy(
        self, **kwargs: Unpack[PutVoiceConnectorProxyRequestRequestTypeDef]
    ) -> PutVoiceConnectorProxyResponseTypeDef:
        """
        Puts the specified proxy configuration to the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_proxy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#put_voice_connector_proxy)
        """

    def put_voice_connector_streaming_configuration(
        self, **kwargs: Unpack[PutVoiceConnectorStreamingConfigurationRequestRequestTypeDef]
    ) -> PutVoiceConnectorStreamingConfigurationResponseTypeDef:
        """
        Adds a streaming configuration for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_streaming_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#put_voice_connector_streaming_configuration)
        """

    def put_voice_connector_termination(
        self, **kwargs: Unpack[PutVoiceConnectorTerminationRequestRequestTypeDef]
    ) -> PutVoiceConnectorTerminationResponseTypeDef:
        """
        Adds termination settings for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_termination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#put_voice_connector_termination)
        """

    def put_voice_connector_termination_credentials(
        self, **kwargs: Unpack[PutVoiceConnectorTerminationCredentialsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds termination SIP credentials for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/put_voice_connector_termination_credentials.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#put_voice_connector_termination_credentials)
        """

    def redact_channel_message(
        self, **kwargs: Unpack[RedactChannelMessageRequestRequestTypeDef]
    ) -> RedactChannelMessageResponseTypeDef:
        """
        Redacts message content, but not metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/redact_channel_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#redact_channel_message)
        """

    def redact_conversation_message(
        self, **kwargs: Unpack[RedactConversationMessageRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Redacts the specified message from the specified Amazon Chime conversation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/redact_conversation_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#redact_conversation_message)
        """

    def redact_room_message(
        self, **kwargs: Unpack[RedactRoomMessageRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Redacts the specified message from the specified Amazon Chime channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/redact_room_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#redact_room_message)
        """

    def regenerate_security_token(
        self, **kwargs: Unpack[RegenerateSecurityTokenRequestRequestTypeDef]
    ) -> RegenerateSecurityTokenResponseTypeDef:
        """
        Regenerates the security token for a bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/regenerate_security_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#regenerate_security_token)
        """

    def reset_personal_pin(
        self, **kwargs: Unpack[ResetPersonalPINRequestRequestTypeDef]
    ) -> ResetPersonalPINResponseTypeDef:
        """
        Resets the personal meeting PIN for the specified user on an Amazon Chime
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/reset_personal_pin.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#reset_personal_pin)
        """

    def restore_phone_number(
        self, **kwargs: Unpack[RestorePhoneNumberRequestRequestTypeDef]
    ) -> RestorePhoneNumberResponseTypeDef:
        """
        Moves a phone number from the <b>Deletion queue</b> back into the phone number
        <b>Inventory</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/restore_phone_number.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#restore_phone_number)
        """

    def search_available_phone_numbers(
        self, **kwargs: Unpack[SearchAvailablePhoneNumbersRequestRequestTypeDef]
    ) -> SearchAvailablePhoneNumbersResponseTypeDef:
        """
        Searches for phone numbers that can be ordered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/search_available_phone_numbers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#search_available_phone_numbers)
        """

    def send_channel_message(
        self, **kwargs: Unpack[SendChannelMessageRequestRequestTypeDef]
    ) -> SendChannelMessageResponseTypeDef:
        """
        Sends a message to a particular channel that the member is a part of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/send_channel_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#send_channel_message)
        """

    def start_meeting_transcription(
        self, **kwargs: Unpack[StartMeetingTranscriptionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts transcription for the specified <code>meetingId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/start_meeting_transcription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#start_meeting_transcription)
        """

    def stop_meeting_transcription(
        self, **kwargs: Unpack[StopMeetingTranscriptionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops transcription for the specified <code>meetingId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/stop_meeting_transcription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#stop_meeting_transcription)
        """

    def tag_attendee(
        self, **kwargs: Unpack[TagAttendeeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Applies the specified tags to the specified Amazon Chime attendee.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/tag_attendee.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#tag_attendee)
        """

    def tag_meeting(
        self, **kwargs: Unpack[TagMeetingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Applies the specified tags to the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/tag_meeting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#tag_meeting)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Applies the specified tags to the specified Amazon Chime SDK meeting resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#tag_resource)
        """

    def untag_attendee(
        self, **kwargs: Unpack[UntagAttendeeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Untags the specified tags from the specified Amazon Chime SDK attendee.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/untag_attendee.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#untag_attendee)
        """

    def untag_meeting(
        self, **kwargs: Unpack[UntagMeetingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Untags the specified tags from the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/untag_meeting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#untag_meeting)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Untags the specified tags from the specified Amazon Chime SDK meeting resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#untag_resource)
        """

    def update_account(
        self, **kwargs: Unpack[UpdateAccountRequestRequestTypeDef]
    ) -> UpdateAccountResponseTypeDef:
        """
        Updates account details for the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_account)
        """

    def update_account_settings(
        self, **kwargs: Unpack[UpdateAccountSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the settings for the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_account_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_account_settings)
        """

    def update_app_instance(
        self, **kwargs: Unpack[UpdateAppInstanceRequestRequestTypeDef]
    ) -> UpdateAppInstanceResponseTypeDef:
        """
        Updates <code>AppInstance</code> metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_app_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_app_instance)
        """

    def update_app_instance_user(
        self, **kwargs: Unpack[UpdateAppInstanceUserRequestRequestTypeDef]
    ) -> UpdateAppInstanceUserResponseTypeDef:
        """
        Updates the details of an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_app_instance_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_app_instance_user)
        """

    def update_bot(
        self, **kwargs: Unpack[UpdateBotRequestRequestTypeDef]
    ) -> UpdateBotResponseTypeDef:
        """
        Updates the status of the specified bot, such as starting or stopping the bot
        from running in your Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_bot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_bot)
        """

    def update_channel(
        self, **kwargs: Unpack[UpdateChannelRequestRequestTypeDef]
    ) -> UpdateChannelResponseTypeDef:
        """
        Update a channel's attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_channel)
        """

    def update_channel_message(
        self, **kwargs: Unpack[UpdateChannelMessageRequestRequestTypeDef]
    ) -> UpdateChannelMessageResponseTypeDef:
        """
        Updates the content of a message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_channel_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_channel_message)
        """

    def update_channel_read_marker(
        self, **kwargs: Unpack[UpdateChannelReadMarkerRequestRequestTypeDef]
    ) -> UpdateChannelReadMarkerResponseTypeDef:
        """
        The details of the time when a user last read messages in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_channel_read_marker.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_channel_read_marker)
        """

    def update_global_settings(
        self, **kwargs: Unpack[UpdateGlobalSettingsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates global settings for the administrator's AWS account, such as Amazon
        Chime Business Calling and Amazon Chime Voice Connector settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_global_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_global_settings)
        """

    def update_phone_number(
        self, **kwargs: Unpack[UpdatePhoneNumberRequestRequestTypeDef]
    ) -> UpdatePhoneNumberResponseTypeDef:
        """
        Updates phone number details, such as product type or calling name, for the
        specified phone number ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_phone_number.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_phone_number)
        """

    def update_phone_number_settings(
        self, **kwargs: Unpack[UpdatePhoneNumberSettingsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the phone number settings for the administrator's AWS account, such as
        the default outbound calling name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_phone_number_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_phone_number_settings)
        """

    def update_proxy_session(
        self, **kwargs: Unpack[UpdateProxySessionRequestRequestTypeDef]
    ) -> UpdateProxySessionResponseTypeDef:
        """
        Updates the specified proxy session details, such as voice or SMS capabilities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_proxy_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_proxy_session)
        """

    def update_room(
        self, **kwargs: Unpack[UpdateRoomRequestRequestTypeDef]
    ) -> UpdateRoomResponseTypeDef:
        """
        Updates room details, such as the room name, for a room in an Amazon Chime
        Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_room.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_room)
        """

    def update_room_membership(
        self, **kwargs: Unpack[UpdateRoomMembershipRequestRequestTypeDef]
    ) -> UpdateRoomMembershipResponseTypeDef:
        """
        Updates room membership details, such as the member role, for a room in an
        Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_room_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_room_membership)
        """

    def update_sip_media_application(
        self, **kwargs: Unpack[UpdateSipMediaApplicationRequestRequestTypeDef]
    ) -> UpdateSipMediaApplicationResponseTypeDef:
        """
        Updates the details of the specified SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_sip_media_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_sip_media_application)
        """

    def update_sip_media_application_call(
        self, **kwargs: Unpack[UpdateSipMediaApplicationCallRequestRequestTypeDef]
    ) -> UpdateSipMediaApplicationCallResponseTypeDef:
        """
        Invokes the AWS Lambda function associated with the SIP media application and
        transaction ID in an update request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_sip_media_application_call.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_sip_media_application_call)
        """

    def update_sip_rule(
        self, **kwargs: Unpack[UpdateSipRuleRequestRequestTypeDef]
    ) -> UpdateSipRuleResponseTypeDef:
        """
        Updates the details of the specified SIP rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_sip_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_sip_rule)
        """

    def update_user(
        self, **kwargs: Unpack[UpdateUserRequestRequestTypeDef]
    ) -> UpdateUserResponseTypeDef:
        """
        Updates user details for a specified user ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_user)
        """

    def update_user_settings(
        self, **kwargs: Unpack[UpdateUserSettingsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the settings for the specified user, such as phone number settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_user_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_user_settings)
        """

    def update_voice_connector(
        self, **kwargs: Unpack[UpdateVoiceConnectorRequestRequestTypeDef]
    ) -> UpdateVoiceConnectorResponseTypeDef:
        """
        Updates details for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_voice_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_voice_connector)
        """

    def update_voice_connector_group(
        self, **kwargs: Unpack[UpdateVoiceConnectorGroupRequestRequestTypeDef]
    ) -> UpdateVoiceConnectorGroupResponseTypeDef:
        """
        Updates details of the specified Amazon Chime Voice Connector group, such as
        the name and Amazon Chime Voice Connector priority ranking.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/update_voice_connector_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#update_voice_connector_group)
        """

    def validate_e911_address(
        self, **kwargs: Unpack[ValidateE911AddressRequestRequestTypeDef]
    ) -> ValidateE911AddressResponseTypeDef:
        """
        Validates an address to be used for 911 calls made with Amazon Chime Voice
        Connectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/validate_e911_address.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#validate_e911_address)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_accounts"]) -> ListAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime/client/#get_paginator)
        """
