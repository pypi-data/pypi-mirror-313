"""
Type annotations for lexv2-runtime service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_runtime/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_lexv2_runtime.client import LexRuntimeV2Client

    session = Session()
    client: LexRuntimeV2Client = session.client("lexv2-runtime")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    DeleteSessionRequestRequestTypeDef,
    DeleteSessionResponseTypeDef,
    GetSessionRequestRequestTypeDef,
    GetSessionResponseTypeDef,
    PutSessionRequestRequestTypeDef,
    PutSessionResponseTypeDef,
    RecognizeTextRequestRequestTypeDef,
    RecognizeTextResponseTypeDef,
    RecognizeUtteranceRequestRequestTypeDef,
    RecognizeUtteranceResponseTypeDef,
    StartConversationRequestRequestTypeDef,
    StartConversationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("LexRuntimeV2Client",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadGatewayException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DependencyFailedException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LexRuntimeV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime.html#LexRuntimeV2.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LexRuntimeV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime.html#LexRuntimeV2.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_runtime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_runtime/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_runtime/client/#close)
        """

    def delete_session(
        self, **kwargs: Unpack[DeleteSessionRequestRequestTypeDef]
    ) -> DeleteSessionResponseTypeDef:
        """
        Removes session information for a specified bot, alias, and user ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime/client/delete_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_runtime/client/#delete_session)
        """

    def get_session(
        self, **kwargs: Unpack[GetSessionRequestRequestTypeDef]
    ) -> GetSessionResponseTypeDef:
        """
        Returns session information for a specified bot, alias, and user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime/client/get_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_runtime/client/#get_session)
        """

    def put_session(
        self, **kwargs: Unpack[PutSessionRequestRequestTypeDef]
    ) -> PutSessionResponseTypeDef:
        """
        Creates a new session or modifies an existing session with an Amazon Lex V2 bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime/client/put_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_runtime/client/#put_session)
        """

    def recognize_text(
        self, **kwargs: Unpack[RecognizeTextRequestRequestTypeDef]
    ) -> RecognizeTextResponseTypeDef:
        """
        Sends user input to Amazon Lex V2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime/client/recognize_text.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_runtime/client/#recognize_text)
        """

    def recognize_utterance(
        self, **kwargs: Unpack[RecognizeUtteranceRequestRequestTypeDef]
    ) -> RecognizeUtteranceResponseTypeDef:
        """
        Sends user input to Amazon Lex V2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime/client/recognize_utterance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_runtime/client/#recognize_utterance)
        """

    def start_conversation(
        self, **kwargs: Unpack[StartConversationRequestRequestTypeDef]
    ) -> StartConversationResponseTypeDef:
        """
        Starts an HTTP/2 bidirectional event stream that enables you to send audio,
        text, or DTMF input in real time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime/client/start_conversation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_runtime/client/#start_conversation)
        """
