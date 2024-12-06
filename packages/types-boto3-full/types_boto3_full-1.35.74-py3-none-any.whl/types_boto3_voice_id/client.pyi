"""
Type annotations for voice-id service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_voice_id.client import VoiceIDClient

    session = Session()
    client: VoiceIDClient = session.client("voice-id")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListDomainsPaginator,
    ListFraudsterRegistrationJobsPaginator,
    ListFraudstersPaginator,
    ListSpeakerEnrollmentJobsPaginator,
    ListSpeakersPaginator,
    ListWatchlistsPaginator,
)
from .type_defs import (
    AssociateFraudsterRequestRequestTypeDef,
    AssociateFraudsterResponseTypeDef,
    CreateDomainRequestRequestTypeDef,
    CreateDomainResponseTypeDef,
    CreateWatchlistRequestRequestTypeDef,
    CreateWatchlistResponseTypeDef,
    DeleteDomainRequestRequestTypeDef,
    DeleteFraudsterRequestRequestTypeDef,
    DeleteSpeakerRequestRequestTypeDef,
    DeleteWatchlistRequestRequestTypeDef,
    DescribeDomainRequestRequestTypeDef,
    DescribeDomainResponseTypeDef,
    DescribeFraudsterRegistrationJobRequestRequestTypeDef,
    DescribeFraudsterRegistrationJobResponseTypeDef,
    DescribeFraudsterRequestRequestTypeDef,
    DescribeFraudsterResponseTypeDef,
    DescribeSpeakerEnrollmentJobRequestRequestTypeDef,
    DescribeSpeakerEnrollmentJobResponseTypeDef,
    DescribeSpeakerRequestRequestTypeDef,
    DescribeSpeakerResponseTypeDef,
    DescribeWatchlistRequestRequestTypeDef,
    DescribeWatchlistResponseTypeDef,
    DisassociateFraudsterRequestRequestTypeDef,
    DisassociateFraudsterResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EvaluateSessionRequestRequestTypeDef,
    EvaluateSessionResponseTypeDef,
    ListDomainsRequestRequestTypeDef,
    ListDomainsResponseTypeDef,
    ListFraudsterRegistrationJobsRequestRequestTypeDef,
    ListFraudsterRegistrationJobsResponseTypeDef,
    ListFraudstersRequestRequestTypeDef,
    ListFraudstersResponseTypeDef,
    ListSpeakerEnrollmentJobsRequestRequestTypeDef,
    ListSpeakerEnrollmentJobsResponseTypeDef,
    ListSpeakersRequestRequestTypeDef,
    ListSpeakersResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWatchlistsRequestRequestTypeDef,
    ListWatchlistsResponseTypeDef,
    OptOutSpeakerRequestRequestTypeDef,
    OptOutSpeakerResponseTypeDef,
    StartFraudsterRegistrationJobRequestRequestTypeDef,
    StartFraudsterRegistrationJobResponseTypeDef,
    StartSpeakerEnrollmentJobRequestRequestTypeDef,
    StartSpeakerEnrollmentJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDomainRequestRequestTypeDef,
    UpdateDomainResponseTypeDef,
    UpdateWatchlistRequestRequestTypeDef,
    UpdateWatchlistResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("VoiceIDClient",)

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

class VoiceIDClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id.html#VoiceID.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        VoiceIDClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id.html#VoiceID.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#close)
        """

    def associate_fraudster(
        self, **kwargs: Unpack[AssociateFraudsterRequestRequestTypeDef]
    ) -> AssociateFraudsterResponseTypeDef:
        """
        Associates the fraudsters with the watchlist specified in the same domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/associate_fraudster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#associate_fraudster)
        """

    def create_domain(
        self, **kwargs: Unpack[CreateDomainRequestRequestTypeDef]
    ) -> CreateDomainResponseTypeDef:
        """
        Creates a domain that contains all Amazon Connect Voice ID data, such as
        speakers, fraudsters, customer audio, and voiceprints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/create_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#create_domain)
        """

    def create_watchlist(
        self, **kwargs: Unpack[CreateWatchlistRequestRequestTypeDef]
    ) -> CreateWatchlistResponseTypeDef:
        """
        Creates a watchlist that fraudsters can be a part of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/create_watchlist.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#create_watchlist)
        """

    def delete_domain(
        self, **kwargs: Unpack[DeleteDomainRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified domain from Voice ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/delete_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#delete_domain)
        """

    def delete_fraudster(
        self, **kwargs: Unpack[DeleteFraudsterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified fraudster from Voice ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/delete_fraudster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#delete_fraudster)
        """

    def delete_speaker(
        self, **kwargs: Unpack[DeleteSpeakerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified speaker from Voice ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/delete_speaker.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#delete_speaker)
        """

    def delete_watchlist(
        self, **kwargs: Unpack[DeleteWatchlistRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified watchlist from Voice ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/delete_watchlist.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#delete_watchlist)
        """

    def describe_domain(
        self, **kwargs: Unpack[DescribeDomainRequestRequestTypeDef]
    ) -> DescribeDomainResponseTypeDef:
        """
        Describes the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/describe_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#describe_domain)
        """

    def describe_fraudster(
        self, **kwargs: Unpack[DescribeFraudsterRequestRequestTypeDef]
    ) -> DescribeFraudsterResponseTypeDef:
        """
        Describes the specified fraudster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/describe_fraudster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#describe_fraudster)
        """

    def describe_fraudster_registration_job(
        self, **kwargs: Unpack[DescribeFraudsterRegistrationJobRequestRequestTypeDef]
    ) -> DescribeFraudsterRegistrationJobResponseTypeDef:
        """
        Describes the specified fraudster registration job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/describe_fraudster_registration_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#describe_fraudster_registration_job)
        """

    def describe_speaker(
        self, **kwargs: Unpack[DescribeSpeakerRequestRequestTypeDef]
    ) -> DescribeSpeakerResponseTypeDef:
        """
        Describes the specified speaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/describe_speaker.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#describe_speaker)
        """

    def describe_speaker_enrollment_job(
        self, **kwargs: Unpack[DescribeSpeakerEnrollmentJobRequestRequestTypeDef]
    ) -> DescribeSpeakerEnrollmentJobResponseTypeDef:
        """
        Describes the specified speaker enrollment job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/describe_speaker_enrollment_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#describe_speaker_enrollment_job)
        """

    def describe_watchlist(
        self, **kwargs: Unpack[DescribeWatchlistRequestRequestTypeDef]
    ) -> DescribeWatchlistResponseTypeDef:
        """
        Describes the specified watchlist.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/describe_watchlist.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#describe_watchlist)
        """

    def disassociate_fraudster(
        self, **kwargs: Unpack[DisassociateFraudsterRequestRequestTypeDef]
    ) -> DisassociateFraudsterResponseTypeDef:
        """
        Disassociates the fraudsters from the watchlist specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/disassociate_fraudster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#disassociate_fraudster)
        """

    def evaluate_session(
        self, **kwargs: Unpack[EvaluateSessionRequestRequestTypeDef]
    ) -> EvaluateSessionResponseTypeDef:
        """
        Evaluates a specified session based on audio data accumulated during a
        streaming Amazon Connect Voice ID call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/evaluate_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#evaluate_session)
        """

    def list_domains(
        self, **kwargs: Unpack[ListDomainsRequestRequestTypeDef]
    ) -> ListDomainsResponseTypeDef:
        """
        Lists all the domains in the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_domains.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#list_domains)
        """

    def list_fraudster_registration_jobs(
        self, **kwargs: Unpack[ListFraudsterRegistrationJobsRequestRequestTypeDef]
    ) -> ListFraudsterRegistrationJobsResponseTypeDef:
        """
        Lists all the fraudster registration jobs in the domain with the given
        <code>JobStatus</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_fraudster_registration_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#list_fraudster_registration_jobs)
        """

    def list_fraudsters(
        self, **kwargs: Unpack[ListFraudstersRequestRequestTypeDef]
    ) -> ListFraudstersResponseTypeDef:
        """
        Lists all fraudsters in a specified watchlist or domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_fraudsters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#list_fraudsters)
        """

    def list_speaker_enrollment_jobs(
        self, **kwargs: Unpack[ListSpeakerEnrollmentJobsRequestRequestTypeDef]
    ) -> ListSpeakerEnrollmentJobsResponseTypeDef:
        """
        Lists all the speaker enrollment jobs in the domain with the specified
        <code>JobStatus</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_speaker_enrollment_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#list_speaker_enrollment_jobs)
        """

    def list_speakers(
        self, **kwargs: Unpack[ListSpeakersRequestRequestTypeDef]
    ) -> ListSpeakersResponseTypeDef:
        """
        Lists all speakers in a specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_speakers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#list_speakers)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags associated with a specified Voice ID resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#list_tags_for_resource)
        """

    def list_watchlists(
        self, **kwargs: Unpack[ListWatchlistsRequestRequestTypeDef]
    ) -> ListWatchlistsResponseTypeDef:
        """
        Lists all watchlists in a specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_watchlists.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#list_watchlists)
        """

    def opt_out_speaker(
        self, **kwargs: Unpack[OptOutSpeakerRequestRequestTypeDef]
    ) -> OptOutSpeakerResponseTypeDef:
        """
        Opts out a speaker from Voice ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/opt_out_speaker.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#opt_out_speaker)
        """

    def start_fraudster_registration_job(
        self, **kwargs: Unpack[StartFraudsterRegistrationJobRequestRequestTypeDef]
    ) -> StartFraudsterRegistrationJobResponseTypeDef:
        """
        Starts a new batch fraudster registration job using provided details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/start_fraudster_registration_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#start_fraudster_registration_job)
        """

    def start_speaker_enrollment_job(
        self, **kwargs: Unpack[StartSpeakerEnrollmentJobRequestRequestTypeDef]
    ) -> StartSpeakerEnrollmentJobResponseTypeDef:
        """
        Starts a new batch speaker enrollment job using specified details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/start_speaker_enrollment_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#start_speaker_enrollment_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags a Voice ID resource with the provided list of tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes specified tags from a specified Amazon Connect Voice ID resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#untag_resource)
        """

    def update_domain(
        self, **kwargs: Unpack[UpdateDomainRequestRequestTypeDef]
    ) -> UpdateDomainResponseTypeDef:
        """
        Updates the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/update_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#update_domain)
        """

    def update_watchlist(
        self, **kwargs: Unpack[UpdateWatchlistRequestRequestTypeDef]
    ) -> UpdateWatchlistResponseTypeDef:
        """
        Updates the specified watchlist.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/update_watchlist.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#update_watchlist)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_fraudster_registration_jobs"]
    ) -> ListFraudsterRegistrationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_fraudsters"]) -> ListFraudstersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_speaker_enrollment_jobs"]
    ) -> ListSpeakerEnrollmentJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_speakers"]) -> ListSpeakersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_watchlists"]) -> ListWatchlistsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_voice_id/client/#get_paginator)
        """
