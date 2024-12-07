"""
Type annotations for polly service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_polly.client import PollyClient

    session = Session()
    client: PollyClient = session.client("polly")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeVoicesPaginator,
    ListLexiconsPaginator,
    ListSpeechSynthesisTasksPaginator,
)
from .type_defs import (
    DeleteLexiconInputRequestTypeDef,
    DescribeVoicesInputRequestTypeDef,
    DescribeVoicesOutputTypeDef,
    GetLexiconInputRequestTypeDef,
    GetLexiconOutputTypeDef,
    GetSpeechSynthesisTaskInputRequestTypeDef,
    GetSpeechSynthesisTaskOutputTypeDef,
    ListLexiconsInputRequestTypeDef,
    ListLexiconsOutputTypeDef,
    ListSpeechSynthesisTasksInputRequestTypeDef,
    ListSpeechSynthesisTasksOutputTypeDef,
    PutLexiconInputRequestTypeDef,
    StartSpeechSynthesisTaskInputRequestTypeDef,
    StartSpeechSynthesisTaskOutputTypeDef,
    SynthesizeSpeechInputRequestTypeDef,
    SynthesizeSpeechOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("PollyClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    EngineNotSupportedException: Type[BotocoreClientError]
    InvalidLexiconException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidS3BucketException: Type[BotocoreClientError]
    InvalidS3KeyException: Type[BotocoreClientError]
    InvalidSampleRateException: Type[BotocoreClientError]
    InvalidSnsTopicArnException: Type[BotocoreClientError]
    InvalidSsmlException: Type[BotocoreClientError]
    InvalidTaskIdException: Type[BotocoreClientError]
    LanguageNotSupportedException: Type[BotocoreClientError]
    LexiconNotFoundException: Type[BotocoreClientError]
    LexiconSizeExceededException: Type[BotocoreClientError]
    MarksNotSupportedForFormatException: Type[BotocoreClientError]
    MaxLexemeLengthExceededException: Type[BotocoreClientError]
    MaxLexiconsNumberExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    SsmlMarksNotSupportedForTextTypeException: Type[BotocoreClientError]
    SynthesisTaskNotFoundException: Type[BotocoreClientError]
    TextLengthExceededException: Type[BotocoreClientError]
    UnsupportedPlsAlphabetException: Type[BotocoreClientError]
    UnsupportedPlsLanguageException: Type[BotocoreClientError]


class PollyClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PollyClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#close)
        """

    def delete_lexicon(self, **kwargs: Unpack[DeleteLexiconInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified pronunciation lexicon stored in an Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/delete_lexicon.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#delete_lexicon)
        """

    def describe_voices(
        self, **kwargs: Unpack[DescribeVoicesInputRequestTypeDef]
    ) -> DescribeVoicesOutputTypeDef:
        """
        Returns the list of voices that are available for use when requesting speech
        synthesis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/describe_voices.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#describe_voices)
        """

    def get_lexicon(
        self, **kwargs: Unpack[GetLexiconInputRequestTypeDef]
    ) -> GetLexiconOutputTypeDef:
        """
        Returns the content of the specified pronunciation lexicon stored in an Amazon
        Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/get_lexicon.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#get_lexicon)
        """

    def get_speech_synthesis_task(
        self, **kwargs: Unpack[GetSpeechSynthesisTaskInputRequestTypeDef]
    ) -> GetSpeechSynthesisTaskOutputTypeDef:
        """
        Retrieves a specific SpeechSynthesisTask object based on its TaskID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/get_speech_synthesis_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#get_speech_synthesis_task)
        """

    def list_lexicons(
        self, **kwargs: Unpack[ListLexiconsInputRequestTypeDef]
    ) -> ListLexiconsOutputTypeDef:
        """
        Returns a list of pronunciation lexicons stored in an Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/list_lexicons.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#list_lexicons)
        """

    def list_speech_synthesis_tasks(
        self, **kwargs: Unpack[ListSpeechSynthesisTasksInputRequestTypeDef]
    ) -> ListSpeechSynthesisTasksOutputTypeDef:
        """
        Returns a list of SpeechSynthesisTask objects ordered by their creation date.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/list_speech_synthesis_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#list_speech_synthesis_tasks)
        """

    def put_lexicon(self, **kwargs: Unpack[PutLexiconInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Stores a pronunciation lexicon in an Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/put_lexicon.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#put_lexicon)
        """

    def start_speech_synthesis_task(
        self, **kwargs: Unpack[StartSpeechSynthesisTaskInputRequestTypeDef]
    ) -> StartSpeechSynthesisTaskOutputTypeDef:
        """
        Allows the creation of an asynchronous synthesis task, by starting a new
        <code>SpeechSynthesisTask</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/start_speech_synthesis_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#start_speech_synthesis_task)
        """

    def synthesize_speech(
        self, **kwargs: Unpack[SynthesizeSpeechInputRequestTypeDef]
    ) -> SynthesizeSpeechOutputTypeDef:
        """
        Synthesizes UTF-8 input, plain text or SSML, to a stream of bytes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/synthesize_speech.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#synthesize_speech)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_voices"]) -> DescribeVoicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_lexicons"]) -> ListLexiconsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_speech_synthesis_tasks"]
    ) -> ListSpeechSynthesisTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_polly/client/#get_paginator)
        """
