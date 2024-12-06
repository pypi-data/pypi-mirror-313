"""
Type annotations for chime-sdk-meetings service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_chime_sdk_meetings.client import ChimeSDKMeetingsClient

    session = Session()
    client: ChimeSDKMeetingsClient = session.client("chime-sdk-meetings")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    BatchCreateAttendeeRequestRequestTypeDef,
    BatchCreateAttendeeResponseTypeDef,
    BatchUpdateAttendeeCapabilitiesExceptRequestRequestTypeDef,
    CreateAttendeeRequestRequestTypeDef,
    CreateAttendeeResponseTypeDef,
    CreateMeetingRequestRequestTypeDef,
    CreateMeetingResponseTypeDef,
    CreateMeetingWithAttendeesRequestRequestTypeDef,
    CreateMeetingWithAttendeesResponseTypeDef,
    DeleteAttendeeRequestRequestTypeDef,
    DeleteMeetingRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAttendeeRequestRequestTypeDef,
    GetAttendeeResponseTypeDef,
    GetMeetingRequestRequestTypeDef,
    GetMeetingResponseTypeDef,
    ListAttendeesRequestRequestTypeDef,
    ListAttendeesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartMeetingTranscriptionRequestRequestTypeDef,
    StopMeetingTranscriptionRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAttendeeCapabilitiesRequestRequestTypeDef,
    UpdateAttendeeCapabilitiesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ChimeSDKMeetingsClient",)


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
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]


class ChimeSDKMeetingsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeSDKMeetingsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#close)
        """

    def batch_create_attendee(
        self, **kwargs: Unpack[BatchCreateAttendeeRequestRequestTypeDef]
    ) -> BatchCreateAttendeeResponseTypeDef:
        """
        Creates up to 100 attendees for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/batch_create_attendee.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#batch_create_attendee)
        """

    def batch_update_attendee_capabilities_except(
        self, **kwargs: Unpack[BatchUpdateAttendeeCapabilitiesExceptRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates <code>AttendeeCapabilities</code> except the capabilities listed in an
        <code>ExcludedAttendeeIds</code> table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/batch_update_attendee_capabilities_except.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#batch_update_attendee_capabilities_except)
        """

    def create_attendee(
        self, **kwargs: Unpack[CreateAttendeeRequestRequestTypeDef]
    ) -> CreateAttendeeResponseTypeDef:
        """
        Creates a new attendee for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/create_attendee.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#create_attendee)
        """

    def create_meeting(
        self, **kwargs: Unpack[CreateMeetingRequestRequestTypeDef]
    ) -> CreateMeetingResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region with no
        initial attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/create_meeting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#create_meeting)
        """

    def create_meeting_with_attendees(
        self, **kwargs: Unpack[CreateMeetingWithAttendeesRequestRequestTypeDef]
    ) -> CreateMeetingWithAttendeesResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region, with
        attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/create_meeting_with_attendees.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#create_meeting_with_attendees)
        """

    def delete_attendee(
        self, **kwargs: Unpack[DeleteAttendeeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an attendee from the specified Amazon Chime SDK meeting and deletes
        their <code>JoinToken</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/delete_attendee.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#delete_attendee)
        """

    def delete_meeting(
        self, **kwargs: Unpack[DeleteMeetingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/delete_meeting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#delete_meeting)
        """

    def get_attendee(
        self, **kwargs: Unpack[GetAttendeeRequestRequestTypeDef]
    ) -> GetAttendeeResponseTypeDef:
        """
        Gets the Amazon Chime SDK attendee details for a specified meeting ID and
        attendee ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/get_attendee.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#get_attendee)
        """

    def get_meeting(
        self, **kwargs: Unpack[GetMeetingRequestRequestTypeDef]
    ) -> GetMeetingResponseTypeDef:
        """
        Gets the Amazon Chime SDK meeting details for the specified meeting ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/get_meeting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#get_meeting)
        """

    def list_attendees(
        self, **kwargs: Unpack[ListAttendeesRequestRequestTypeDef]
    ) -> ListAttendeesResponseTypeDef:
        """
        Lists the attendees for the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/list_attendees.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#list_attendees)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of the tags available for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#list_tags_for_resource)
        """

    def start_meeting_transcription(
        self, **kwargs: Unpack[StartMeetingTranscriptionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts transcription for the specified <code>meetingId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/start_meeting_transcription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#start_meeting_transcription)
        """

    def stop_meeting_transcription(
        self, **kwargs: Unpack[StopMeetingTranscriptionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops transcription for the specified <code>meetingId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/stop_meeting_transcription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#stop_meeting_transcription)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        The resource that supports tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#untag_resource)
        """

    def update_attendee_capabilities(
        self, **kwargs: Unpack[UpdateAttendeeCapabilitiesRequestRequestTypeDef]
    ) -> UpdateAttendeeCapabilitiesResponseTypeDef:
        """
        The capabilities that you want to update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/update_attendee_capabilities.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_meetings/client/#update_attendee_capabilities)
        """
