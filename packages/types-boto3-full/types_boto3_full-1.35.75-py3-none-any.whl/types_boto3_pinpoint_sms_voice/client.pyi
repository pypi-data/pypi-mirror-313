"""
Type annotations for pinpoint-sms-voice service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_sms_voice/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_pinpoint_sms_voice.client import PinpointSMSVoiceClient

    session = Session()
    client: PinpointSMSVoiceClient = session.client("pinpoint-sms-voice")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateConfigurationSetEventDestinationRequestRequestTypeDef,
    CreateConfigurationSetRequestRequestTypeDef,
    DeleteConfigurationSetEventDestinationRequestRequestTypeDef,
    DeleteConfigurationSetRequestRequestTypeDef,
    GetConfigurationSetEventDestinationsRequestRequestTypeDef,
    GetConfigurationSetEventDestinationsResponseTypeDef,
    SendVoiceMessageRequestRequestTypeDef,
    SendVoiceMessageResponseTypeDef,
    UpdateConfigurationSetEventDestinationRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("PinpointSMSVoiceClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]

class PinpointSMSVoiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice.html#PinpointSMSVoice.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_sms_voice/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PinpointSMSVoiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice.html#PinpointSMSVoice.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_sms_voice/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_sms_voice/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_sms_voice/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_sms_voice/client/#close)
        """

    def create_configuration_set(
        self, **kwargs: Unpack[CreateConfigurationSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Create a new configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice/client/create_configuration_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_sms_voice/client/#create_configuration_set)
        """

    def create_configuration_set_event_destination(
        self, **kwargs: Unpack[CreateConfigurationSetEventDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Create a new event destination in a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice/client/create_configuration_set_event_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_sms_voice/client/#create_configuration_set_event_destination)
        """

    def delete_configuration_set(
        self, **kwargs: Unpack[DeleteConfigurationSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice/client/delete_configuration_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_sms_voice/client/#delete_configuration_set)
        """

    def delete_configuration_set_event_destination(
        self, **kwargs: Unpack[DeleteConfigurationSetEventDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an event destination in a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice/client/delete_configuration_set_event_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_sms_voice/client/#delete_configuration_set_event_destination)
        """

    def get_configuration_set_event_destinations(
        self, **kwargs: Unpack[GetConfigurationSetEventDestinationsRequestRequestTypeDef]
    ) -> GetConfigurationSetEventDestinationsResponseTypeDef:
        """
        Obtain information about an event destination, including the types of events it
        reports, the Amazon Resource Name (ARN) of the destination, and the name of the
        event destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice/client/get_configuration_set_event_destinations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_sms_voice/client/#get_configuration_set_event_destinations)
        """

    def send_voice_message(
        self, **kwargs: Unpack[SendVoiceMessageRequestRequestTypeDef]
    ) -> SendVoiceMessageResponseTypeDef:
        """
        Create a new voice message and send it to a recipient's phone number.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice/client/send_voice_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_sms_voice/client/#send_voice_message)
        """

    def update_configuration_set_event_destination(
        self, **kwargs: Unpack[UpdateConfigurationSetEventDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update an event destination in a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice/client/update_configuration_set_event_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pinpoint_sms_voice/client/#update_configuration_set_event_destination)
        """
