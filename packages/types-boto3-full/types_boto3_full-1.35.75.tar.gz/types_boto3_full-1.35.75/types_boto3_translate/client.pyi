"""
Type annotations for translate service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_translate.client import TranslateClient

    session = Session()
    client: TranslateClient = session.client("translate")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListTerminologiesPaginator
from .type_defs import (
    CreateParallelDataRequestRequestTypeDef,
    CreateParallelDataResponseTypeDef,
    DeleteParallelDataRequestRequestTypeDef,
    DeleteParallelDataResponseTypeDef,
    DeleteTerminologyRequestRequestTypeDef,
    DescribeTextTranslationJobRequestRequestTypeDef,
    DescribeTextTranslationJobResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetParallelDataRequestRequestTypeDef,
    GetParallelDataResponseTypeDef,
    GetTerminologyRequestRequestTypeDef,
    GetTerminologyResponseTypeDef,
    ImportTerminologyRequestRequestTypeDef,
    ImportTerminologyResponseTypeDef,
    ListLanguagesRequestRequestTypeDef,
    ListLanguagesResponseTypeDef,
    ListParallelDataRequestRequestTypeDef,
    ListParallelDataResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTerminologiesRequestRequestTypeDef,
    ListTerminologiesResponseTypeDef,
    ListTextTranslationJobsRequestRequestTypeDef,
    ListTextTranslationJobsResponseTypeDef,
    StartTextTranslationJobRequestRequestTypeDef,
    StartTextTranslationJobResponseTypeDef,
    StopTextTranslationJobRequestRequestTypeDef,
    StopTextTranslationJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    TranslateDocumentRequestRequestTypeDef,
    TranslateDocumentResponseTypeDef,
    TranslateTextRequestRequestTypeDef,
    TranslateTextResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateParallelDataRequestRequestTypeDef,
    UpdateParallelDataResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("TranslateClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DetectedLanguageLowConfidenceException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidFilterException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TextSizeLimitExceededException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnsupportedDisplayLanguageCodeException: Type[BotocoreClientError]
    UnsupportedLanguagePairException: Type[BotocoreClientError]

class TranslateClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TranslateClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#close)
        """

    def create_parallel_data(
        self, **kwargs: Unpack[CreateParallelDataRequestRequestTypeDef]
    ) -> CreateParallelDataResponseTypeDef:
        """
        Creates a parallel data resource in Amazon Translate by importing an input file
        from Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/create_parallel_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#create_parallel_data)
        """

    def delete_parallel_data(
        self, **kwargs: Unpack[DeleteParallelDataRequestRequestTypeDef]
    ) -> DeleteParallelDataResponseTypeDef:
        """
        Deletes a parallel data resource in Amazon Translate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/delete_parallel_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#delete_parallel_data)
        """

    def delete_terminology(
        self, **kwargs: Unpack[DeleteTerminologyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        A synchronous action that deletes a custom terminology.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/delete_terminology.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#delete_terminology)
        """

    def describe_text_translation_job(
        self, **kwargs: Unpack[DescribeTextTranslationJobRequestRequestTypeDef]
    ) -> DescribeTextTranslationJobResponseTypeDef:
        """
        Gets the properties associated with an asynchronous batch translation job
        including name, ID, status, source and target languages, input/output S3
        buckets, and so on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/describe_text_translation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#describe_text_translation_job)
        """

    def get_parallel_data(
        self, **kwargs: Unpack[GetParallelDataRequestRequestTypeDef]
    ) -> GetParallelDataResponseTypeDef:
        """
        Provides information about a parallel data resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/get_parallel_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#get_parallel_data)
        """

    def get_terminology(
        self, **kwargs: Unpack[GetTerminologyRequestRequestTypeDef]
    ) -> GetTerminologyResponseTypeDef:
        """
        Retrieves a custom terminology.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/get_terminology.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#get_terminology)
        """

    def import_terminology(
        self, **kwargs: Unpack[ImportTerminologyRequestRequestTypeDef]
    ) -> ImportTerminologyResponseTypeDef:
        """
        Creates or updates a custom terminology, depending on whether one already
        exists for the given terminology name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/import_terminology.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#import_terminology)
        """

    def list_languages(
        self, **kwargs: Unpack[ListLanguagesRequestRequestTypeDef]
    ) -> ListLanguagesResponseTypeDef:
        """
        Provides a list of languages (RFC-5646 codes and names) that Amazon Translate
        supports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/list_languages.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#list_languages)
        """

    def list_parallel_data(
        self, **kwargs: Unpack[ListParallelDataRequestRequestTypeDef]
    ) -> ListParallelDataResponseTypeDef:
        """
        Provides a list of your parallel data resources in Amazon Translate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/list_parallel_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#list_parallel_data)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags associated with a given Amazon Translate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#list_tags_for_resource)
        """

    def list_terminologies(
        self, **kwargs: Unpack[ListTerminologiesRequestRequestTypeDef]
    ) -> ListTerminologiesResponseTypeDef:
        """
        Provides a list of custom terminologies associated with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/list_terminologies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#list_terminologies)
        """

    def list_text_translation_jobs(
        self, **kwargs: Unpack[ListTextTranslationJobsRequestRequestTypeDef]
    ) -> ListTextTranslationJobsResponseTypeDef:
        """
        Gets a list of the batch translation jobs that you have submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/list_text_translation_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#list_text_translation_jobs)
        """

    def start_text_translation_job(
        self, **kwargs: Unpack[StartTextTranslationJobRequestRequestTypeDef]
    ) -> StartTextTranslationJobResponseTypeDef:
        """
        Starts an asynchronous batch translation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/start_text_translation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#start_text_translation_job)
        """

    def stop_text_translation_job(
        self, **kwargs: Unpack[StopTextTranslationJobRequestRequestTypeDef]
    ) -> StopTextTranslationJobResponseTypeDef:
        """
        Stops an asynchronous batch translation job that is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/stop_text_translation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#stop_text_translation_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates a specific tag with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#tag_resource)
        """

    def translate_document(
        self, **kwargs: Unpack[TranslateDocumentRequestRequestTypeDef]
    ) -> TranslateDocumentResponseTypeDef:
        """
        Translates the input document from the source language to the target language.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/translate_document.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#translate_document)
        """

    def translate_text(
        self, **kwargs: Unpack[TranslateTextRequestRequestTypeDef]
    ) -> TranslateTextResponseTypeDef:
        """
        Translates input text from the source language to the target language.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/translate_text.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#translate_text)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a specific tag associated with an Amazon Translate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#untag_resource)
        """

    def update_parallel_data(
        self, **kwargs: Unpack[UpdateParallelDataRequestRequestTypeDef]
    ) -> UpdateParallelDataResponseTypeDef:
        """
        Updates a previously created parallel data resource by importing a new input
        file from Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/update_parallel_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#update_parallel_data)
        """

    def get_paginator(
        self, operation_name: Literal["list_terminologies"]
    ) -> ListTerminologiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_translate/client/#get_paginator)
        """
