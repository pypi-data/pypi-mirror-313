"""
Type annotations for rekognition service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_rekognition.client import RekognitionClient

    session = Session()
    client: RekognitionClient = session.client("rekognition")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeProjectsPaginator,
    DescribeProjectVersionsPaginator,
    ListCollectionsPaginator,
    ListDatasetEntriesPaginator,
    ListDatasetLabelsPaginator,
    ListFacesPaginator,
    ListProjectPoliciesPaginator,
    ListStreamProcessorsPaginator,
    ListUsersPaginator,
)
from .type_defs import (
    AssociateFacesRequestRequestTypeDef,
    AssociateFacesResponseTypeDef,
    CompareFacesRequestRequestTypeDef,
    CompareFacesResponseTypeDef,
    CopyProjectVersionRequestRequestTypeDef,
    CopyProjectVersionResponseTypeDef,
    CreateCollectionRequestRequestTypeDef,
    CreateCollectionResponseTypeDef,
    CreateDatasetRequestRequestTypeDef,
    CreateDatasetResponseTypeDef,
    CreateFaceLivenessSessionRequestRequestTypeDef,
    CreateFaceLivenessSessionResponseTypeDef,
    CreateProjectRequestRequestTypeDef,
    CreateProjectResponseTypeDef,
    CreateProjectVersionRequestRequestTypeDef,
    CreateProjectVersionResponseTypeDef,
    CreateStreamProcessorRequestRequestTypeDef,
    CreateStreamProcessorResponseTypeDef,
    CreateUserRequestRequestTypeDef,
    DeleteCollectionRequestRequestTypeDef,
    DeleteCollectionResponseTypeDef,
    DeleteDatasetRequestRequestTypeDef,
    DeleteFacesRequestRequestTypeDef,
    DeleteFacesResponseTypeDef,
    DeleteProjectPolicyRequestRequestTypeDef,
    DeleteProjectRequestRequestTypeDef,
    DeleteProjectResponseTypeDef,
    DeleteProjectVersionRequestRequestTypeDef,
    DeleteProjectVersionResponseTypeDef,
    DeleteStreamProcessorRequestRequestTypeDef,
    DeleteUserRequestRequestTypeDef,
    DescribeCollectionRequestRequestTypeDef,
    DescribeCollectionResponseTypeDef,
    DescribeDatasetRequestRequestTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeProjectsRequestRequestTypeDef,
    DescribeProjectsResponseTypeDef,
    DescribeProjectVersionsRequestRequestTypeDef,
    DescribeProjectVersionsResponseTypeDef,
    DescribeStreamProcessorRequestRequestTypeDef,
    DescribeStreamProcessorResponseTypeDef,
    DetectCustomLabelsRequestRequestTypeDef,
    DetectCustomLabelsResponseTypeDef,
    DetectFacesRequestRequestTypeDef,
    DetectFacesResponseTypeDef,
    DetectLabelsRequestRequestTypeDef,
    DetectLabelsResponseTypeDef,
    DetectModerationLabelsRequestRequestTypeDef,
    DetectModerationLabelsResponseTypeDef,
    DetectProtectiveEquipmentRequestRequestTypeDef,
    DetectProtectiveEquipmentResponseTypeDef,
    DetectTextRequestRequestTypeDef,
    DetectTextResponseTypeDef,
    DisassociateFacesRequestRequestTypeDef,
    DisassociateFacesResponseTypeDef,
    DistributeDatasetEntriesRequestRequestTypeDef,
    GetCelebrityInfoRequestRequestTypeDef,
    GetCelebrityInfoResponseTypeDef,
    GetCelebrityRecognitionRequestRequestTypeDef,
    GetCelebrityRecognitionResponseTypeDef,
    GetContentModerationRequestRequestTypeDef,
    GetContentModerationResponseTypeDef,
    GetFaceDetectionRequestRequestTypeDef,
    GetFaceDetectionResponseTypeDef,
    GetFaceLivenessSessionResultsRequestRequestTypeDef,
    GetFaceLivenessSessionResultsResponseTypeDef,
    GetFaceSearchRequestRequestTypeDef,
    GetFaceSearchResponseTypeDef,
    GetLabelDetectionRequestRequestTypeDef,
    GetLabelDetectionResponseTypeDef,
    GetMediaAnalysisJobRequestRequestTypeDef,
    GetMediaAnalysisJobResponseTypeDef,
    GetPersonTrackingRequestRequestTypeDef,
    GetPersonTrackingResponseTypeDef,
    GetSegmentDetectionRequestRequestTypeDef,
    GetSegmentDetectionResponseTypeDef,
    GetTextDetectionRequestRequestTypeDef,
    GetTextDetectionResponseTypeDef,
    IndexFacesRequestRequestTypeDef,
    IndexFacesResponseTypeDef,
    ListCollectionsRequestRequestTypeDef,
    ListCollectionsResponseTypeDef,
    ListDatasetEntriesRequestRequestTypeDef,
    ListDatasetEntriesResponseTypeDef,
    ListDatasetLabelsRequestRequestTypeDef,
    ListDatasetLabelsResponseTypeDef,
    ListFacesRequestRequestTypeDef,
    ListFacesResponseTypeDef,
    ListMediaAnalysisJobsRequestRequestTypeDef,
    ListMediaAnalysisJobsResponseTypeDef,
    ListProjectPoliciesRequestRequestTypeDef,
    ListProjectPoliciesResponseTypeDef,
    ListStreamProcessorsRequestRequestTypeDef,
    ListStreamProcessorsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsersRequestRequestTypeDef,
    ListUsersResponseTypeDef,
    PutProjectPolicyRequestRequestTypeDef,
    PutProjectPolicyResponseTypeDef,
    RecognizeCelebritiesRequestRequestTypeDef,
    RecognizeCelebritiesResponseTypeDef,
    SearchFacesByImageRequestRequestTypeDef,
    SearchFacesByImageResponseTypeDef,
    SearchFacesRequestRequestTypeDef,
    SearchFacesResponseTypeDef,
    SearchUsersByImageRequestRequestTypeDef,
    SearchUsersByImageResponseTypeDef,
    SearchUsersRequestRequestTypeDef,
    SearchUsersResponseTypeDef,
    StartCelebrityRecognitionRequestRequestTypeDef,
    StartCelebrityRecognitionResponseTypeDef,
    StartContentModerationRequestRequestTypeDef,
    StartContentModerationResponseTypeDef,
    StartFaceDetectionRequestRequestTypeDef,
    StartFaceDetectionResponseTypeDef,
    StartFaceSearchRequestRequestTypeDef,
    StartFaceSearchResponseTypeDef,
    StartLabelDetectionRequestRequestTypeDef,
    StartLabelDetectionResponseTypeDef,
    StartMediaAnalysisJobRequestRequestTypeDef,
    StartMediaAnalysisJobResponseTypeDef,
    StartPersonTrackingRequestRequestTypeDef,
    StartPersonTrackingResponseTypeDef,
    StartProjectVersionRequestRequestTypeDef,
    StartProjectVersionResponseTypeDef,
    StartSegmentDetectionRequestRequestTypeDef,
    StartSegmentDetectionResponseTypeDef,
    StartStreamProcessorRequestRequestTypeDef,
    StartStreamProcessorResponseTypeDef,
    StartTextDetectionRequestRequestTypeDef,
    StartTextDetectionResponseTypeDef,
    StopProjectVersionRequestRequestTypeDef,
    StopProjectVersionResponseTypeDef,
    StopStreamProcessorRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDatasetEntriesRequestRequestTypeDef,
    UpdateStreamProcessorRequestRequestTypeDef,
)
from .waiter import ProjectVersionRunningWaiter, ProjectVersionTrainingCompletedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("RekognitionClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    HumanLoopQuotaExceededException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    ImageTooLargeException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidImageFormatException: Type[BotocoreClientError]
    InvalidManifestException: Type[BotocoreClientError]
    InvalidPaginationTokenException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidPolicyRevisionIdException: Type[BotocoreClientError]
    InvalidS3ObjectException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    ProvisionedThroughputExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceNotReadyException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    SessionNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    VideoTooLargeException: Type[BotocoreClientError]


class RekognitionClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RekognitionClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#close)
        """

    def associate_faces(
        self, **kwargs: Unpack[AssociateFacesRequestRequestTypeDef]
    ) -> AssociateFacesResponseTypeDef:
        """
        Associates one or more faces with an existing UserID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/associate_faces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#associate_faces)
        """

    def compare_faces(
        self, **kwargs: Unpack[CompareFacesRequestRequestTypeDef]
    ) -> CompareFacesResponseTypeDef:
        """
        Compares a face in the <i>source</i> input image with each of the 100 largest
        faces detected in the <i>target</i> input image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/compare_faces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#compare_faces)
        """

    def copy_project_version(
        self, **kwargs: Unpack[CopyProjectVersionRequestRequestTypeDef]
    ) -> CopyProjectVersionResponseTypeDef:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/copy_project_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#copy_project_version)
        """

    def create_collection(
        self, **kwargs: Unpack[CreateCollectionRequestRequestTypeDef]
    ) -> CreateCollectionResponseTypeDef:
        """
        Creates a collection in an AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/create_collection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#create_collection)
        """

    def create_dataset(
        self, **kwargs: Unpack[CreateDatasetRequestRequestTypeDef]
    ) -> CreateDatasetResponseTypeDef:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/create_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#create_dataset)
        """

    def create_face_liveness_session(
        self, **kwargs: Unpack[CreateFaceLivenessSessionRequestRequestTypeDef]
    ) -> CreateFaceLivenessSessionResponseTypeDef:
        """
        This API operation initiates a Face Liveness session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/create_face_liveness_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#create_face_liveness_session)
        """

    def create_project(
        self, **kwargs: Unpack[CreateProjectRequestRequestTypeDef]
    ) -> CreateProjectResponseTypeDef:
        """
        Creates a new Amazon Rekognition project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/create_project.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#create_project)
        """

    def create_project_version(
        self, **kwargs: Unpack[CreateProjectVersionRequestRequestTypeDef]
    ) -> CreateProjectVersionResponseTypeDef:
        """
        Creates a new version of Amazon Rekognition project (like a Custom Labels model
        or a custom adapter) and begins training.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/create_project_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#create_project_version)
        """

    def create_stream_processor(
        self, **kwargs: Unpack[CreateStreamProcessorRequestRequestTypeDef]
    ) -> CreateStreamProcessorResponseTypeDef:
        """
        Creates an Amazon Rekognition stream processor that you can use to detect and
        recognize faces or to detect labels in a streaming video.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/create_stream_processor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#create_stream_processor)
        """

    def create_user(self, **kwargs: Unpack[CreateUserRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates a new User within a collection specified by <code>CollectionId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/create_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#create_user)
        """

    def delete_collection(
        self, **kwargs: Unpack[DeleteCollectionRequestRequestTypeDef]
    ) -> DeleteCollectionResponseTypeDef:
        """
        Deletes the specified collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/delete_collection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#delete_collection)
        """

    def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/delete_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#delete_dataset)
        """

    def delete_faces(
        self, **kwargs: Unpack[DeleteFacesRequestRequestTypeDef]
    ) -> DeleteFacesResponseTypeDef:
        """
        Deletes faces from a collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/delete_faces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#delete_faces)
        """

    def delete_project(
        self, **kwargs: Unpack[DeleteProjectRequestRequestTypeDef]
    ) -> DeleteProjectResponseTypeDef:
        """
        Deletes a Amazon Rekognition project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/delete_project.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#delete_project)
        """

    def delete_project_policy(
        self, **kwargs: Unpack[DeleteProjectPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/delete_project_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#delete_project_policy)
        """

    def delete_project_version(
        self, **kwargs: Unpack[DeleteProjectVersionRequestRequestTypeDef]
    ) -> DeleteProjectVersionResponseTypeDef:
        """
        Deletes a Rekognition project model or project version, like a Amazon
        Rekognition Custom Labels model or a custom adapter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/delete_project_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#delete_project_version)
        """

    def delete_stream_processor(
        self, **kwargs: Unpack[DeleteStreamProcessorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the stream processor identified by <code>Name</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/delete_stream_processor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#delete_stream_processor)
        """

    def delete_user(self, **kwargs: Unpack[DeleteUserRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified UserID within the collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/delete_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#delete_user)
        """

    def describe_collection(
        self, **kwargs: Unpack[DescribeCollectionRequestRequestTypeDef]
    ) -> DescribeCollectionResponseTypeDef:
        """
        Describes the specified collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/describe_collection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#describe_collection)
        """

    def describe_dataset(
        self, **kwargs: Unpack[DescribeDatasetRequestRequestTypeDef]
    ) -> DescribeDatasetResponseTypeDef:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/describe_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#describe_dataset)
        """

    def describe_project_versions(
        self, **kwargs: Unpack[DescribeProjectVersionsRequestRequestTypeDef]
    ) -> DescribeProjectVersionsResponseTypeDef:
        """
        Lists and describes the versions of an Amazon Rekognition project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/describe_project_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#describe_project_versions)
        """

    def describe_projects(
        self, **kwargs: Unpack[DescribeProjectsRequestRequestTypeDef]
    ) -> DescribeProjectsResponseTypeDef:
        """
        Gets information about your Rekognition projects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/describe_projects.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#describe_projects)
        """

    def describe_stream_processor(
        self, **kwargs: Unpack[DescribeStreamProcessorRequestRequestTypeDef]
    ) -> DescribeStreamProcessorResponseTypeDef:
        """
        Provides information about a stream processor created by
        <a>CreateStreamProcessor</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/describe_stream_processor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#describe_stream_processor)
        """

    def detect_custom_labels(
        self, **kwargs: Unpack[DetectCustomLabelsRequestRequestTypeDef]
    ) -> DetectCustomLabelsResponseTypeDef:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/detect_custom_labels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#detect_custom_labels)
        """

    def detect_faces(
        self, **kwargs: Unpack[DetectFacesRequestRequestTypeDef]
    ) -> DetectFacesResponseTypeDef:
        """
        Detects faces within an image that is provided as input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/detect_faces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#detect_faces)
        """

    def detect_labels(
        self, **kwargs: Unpack[DetectLabelsRequestRequestTypeDef]
    ) -> DetectLabelsResponseTypeDef:
        """
        Detects instances of real-world entities within an image (JPEG or PNG) provided
        as input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/detect_labels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#detect_labels)
        """

    def detect_moderation_labels(
        self, **kwargs: Unpack[DetectModerationLabelsRequestRequestTypeDef]
    ) -> DetectModerationLabelsResponseTypeDef:
        """
        Detects unsafe content in a specified JPEG or PNG format image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/detect_moderation_labels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#detect_moderation_labels)
        """

    def detect_protective_equipment(
        self, **kwargs: Unpack[DetectProtectiveEquipmentRequestRequestTypeDef]
    ) -> DetectProtectiveEquipmentResponseTypeDef:
        """
        Detects Personal Protective Equipment (PPE) worn by people detected in an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/detect_protective_equipment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#detect_protective_equipment)
        """

    def detect_text(
        self, **kwargs: Unpack[DetectTextRequestRequestTypeDef]
    ) -> DetectTextResponseTypeDef:
        """
        Detects text in the input image and converts it into machine-readable text.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/detect_text.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#detect_text)
        """

    def disassociate_faces(
        self, **kwargs: Unpack[DisassociateFacesRequestRequestTypeDef]
    ) -> DisassociateFacesResponseTypeDef:
        """
        Removes the association between a <code>Face</code> supplied in an array of
        <code>FaceIds</code> and the User.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/disassociate_faces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#disassociate_faces)
        """

    def distribute_dataset_entries(
        self, **kwargs: Unpack[DistributeDatasetEntriesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/distribute_dataset_entries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#distribute_dataset_entries)
        """

    def get_celebrity_info(
        self, **kwargs: Unpack[GetCelebrityInfoRequestRequestTypeDef]
    ) -> GetCelebrityInfoResponseTypeDef:
        """
        Gets the name and additional information about a celebrity based on their
        Amazon Rekognition ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_celebrity_info.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_celebrity_info)
        """

    def get_celebrity_recognition(
        self, **kwargs: Unpack[GetCelebrityRecognitionRequestRequestTypeDef]
    ) -> GetCelebrityRecognitionResponseTypeDef:
        """
        Gets the celebrity recognition results for a Amazon Rekognition Video analysis
        started by <a>StartCelebrityRecognition</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_celebrity_recognition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_celebrity_recognition)
        """

    def get_content_moderation(
        self, **kwargs: Unpack[GetContentModerationRequestRequestTypeDef]
    ) -> GetContentModerationResponseTypeDef:
        """
        Gets the inappropriate, unwanted, or offensive content analysis results for a
        Amazon Rekognition Video analysis started by <a>StartContentModeration</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_content_moderation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_content_moderation)
        """

    def get_face_detection(
        self, **kwargs: Unpack[GetFaceDetectionRequestRequestTypeDef]
    ) -> GetFaceDetectionResponseTypeDef:
        """
        Gets face detection results for a Amazon Rekognition Video analysis started by
        <a>StartFaceDetection</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_face_detection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_face_detection)
        """

    def get_face_liveness_session_results(
        self, **kwargs: Unpack[GetFaceLivenessSessionResultsRequestRequestTypeDef]
    ) -> GetFaceLivenessSessionResultsResponseTypeDef:
        """
        Retrieves the results of a specific Face Liveness session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_face_liveness_session_results.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_face_liveness_session_results)
        """

    def get_face_search(
        self, **kwargs: Unpack[GetFaceSearchRequestRequestTypeDef]
    ) -> GetFaceSearchResponseTypeDef:
        """
        Gets the face search results for Amazon Rekognition Video face search started
        by <a>StartFaceSearch</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_face_search.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_face_search)
        """

    def get_label_detection(
        self, **kwargs: Unpack[GetLabelDetectionRequestRequestTypeDef]
    ) -> GetLabelDetectionResponseTypeDef:
        """
        Gets the label detection results of a Amazon Rekognition Video analysis started
        by <a>StartLabelDetection</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_label_detection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_label_detection)
        """

    def get_media_analysis_job(
        self, **kwargs: Unpack[GetMediaAnalysisJobRequestRequestTypeDef]
    ) -> GetMediaAnalysisJobResponseTypeDef:
        """
        Retrieves the results for a given media analysis job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_media_analysis_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_media_analysis_job)
        """

    def get_person_tracking(
        self, **kwargs: Unpack[GetPersonTrackingRequestRequestTypeDef]
    ) -> GetPersonTrackingResponseTypeDef:
        """
        Gets the path tracking results of a Amazon Rekognition Video analysis started
        by <a>StartPersonTracking</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_person_tracking.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_person_tracking)
        """

    def get_segment_detection(
        self, **kwargs: Unpack[GetSegmentDetectionRequestRequestTypeDef]
    ) -> GetSegmentDetectionResponseTypeDef:
        """
        Gets the segment detection results of a Amazon Rekognition Video analysis
        started by <a>StartSegmentDetection</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_segment_detection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_segment_detection)
        """

    def get_text_detection(
        self, **kwargs: Unpack[GetTextDetectionRequestRequestTypeDef]
    ) -> GetTextDetectionResponseTypeDef:
        """
        Gets the text detection results of a Amazon Rekognition Video analysis started
        by <a>StartTextDetection</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_text_detection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_text_detection)
        """

    def index_faces(
        self, **kwargs: Unpack[IndexFacesRequestRequestTypeDef]
    ) -> IndexFacesResponseTypeDef:
        """
        Detects faces in the input image and adds them to the specified collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/index_faces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#index_faces)
        """

    def list_collections(
        self, **kwargs: Unpack[ListCollectionsRequestRequestTypeDef]
    ) -> ListCollectionsResponseTypeDef:
        """
        Returns list of collection IDs in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/list_collections.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#list_collections)
        """

    def list_dataset_entries(
        self, **kwargs: Unpack[ListDatasetEntriesRequestRequestTypeDef]
    ) -> ListDatasetEntriesResponseTypeDef:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/list_dataset_entries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#list_dataset_entries)
        """

    def list_dataset_labels(
        self, **kwargs: Unpack[ListDatasetLabelsRequestRequestTypeDef]
    ) -> ListDatasetLabelsResponseTypeDef:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/list_dataset_labels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#list_dataset_labels)
        """

    def list_faces(
        self, **kwargs: Unpack[ListFacesRequestRequestTypeDef]
    ) -> ListFacesResponseTypeDef:
        """
        Returns metadata for faces in the specified collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/list_faces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#list_faces)
        """

    def list_media_analysis_jobs(
        self, **kwargs: Unpack[ListMediaAnalysisJobsRequestRequestTypeDef]
    ) -> ListMediaAnalysisJobsResponseTypeDef:
        """
        Returns a list of media analysis jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/list_media_analysis_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#list_media_analysis_jobs)
        """

    def list_project_policies(
        self, **kwargs: Unpack[ListProjectPoliciesRequestRequestTypeDef]
    ) -> ListProjectPoliciesResponseTypeDef:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/list_project_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#list_project_policies)
        """

    def list_stream_processors(
        self, **kwargs: Unpack[ListStreamProcessorsRequestRequestTypeDef]
    ) -> ListStreamProcessorsResponseTypeDef:
        """
        Gets a list of stream processors that you have created with
        <a>CreateStreamProcessor</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/list_stream_processors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#list_stream_processors)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags in an Amazon Rekognition collection, stream processor,
        or Custom Labels model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#list_tags_for_resource)
        """

    def list_users(
        self, **kwargs: Unpack[ListUsersRequestRequestTypeDef]
    ) -> ListUsersResponseTypeDef:
        """
        Returns metadata of the User such as <code>UserID</code> in the specified
        collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/list_users.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#list_users)
        """

    def put_project_policy(
        self, **kwargs: Unpack[PutProjectPolicyRequestRequestTypeDef]
    ) -> PutProjectPolicyResponseTypeDef:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/put_project_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#put_project_policy)
        """

    def recognize_celebrities(
        self, **kwargs: Unpack[RecognizeCelebritiesRequestRequestTypeDef]
    ) -> RecognizeCelebritiesResponseTypeDef:
        """
        Returns an array of celebrities recognized in the input image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/recognize_celebrities.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#recognize_celebrities)
        """

    def search_faces(
        self, **kwargs: Unpack[SearchFacesRequestRequestTypeDef]
    ) -> SearchFacesResponseTypeDef:
        """
        For a given input face ID, searches for matching faces in the collection the
        face belongs to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/search_faces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#search_faces)
        """

    def search_faces_by_image(
        self, **kwargs: Unpack[SearchFacesByImageRequestRequestTypeDef]
    ) -> SearchFacesByImageResponseTypeDef:
        """
        For a given input image, first detects the largest face in the image, and then
        searches the specified collection for matching faces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/search_faces_by_image.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#search_faces_by_image)
        """

    def search_users(
        self, **kwargs: Unpack[SearchUsersRequestRequestTypeDef]
    ) -> SearchUsersResponseTypeDef:
        """
        Searches for UserIDs within a collection based on a <code>FaceId</code> or
        <code>UserId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/search_users.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#search_users)
        """

    def search_users_by_image(
        self, **kwargs: Unpack[SearchUsersByImageRequestRequestTypeDef]
    ) -> SearchUsersByImageResponseTypeDef:
        """
        Searches for UserIDs using a supplied image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/search_users_by_image.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#search_users_by_image)
        """

    def start_celebrity_recognition(
        self, **kwargs: Unpack[StartCelebrityRecognitionRequestRequestTypeDef]
    ) -> StartCelebrityRecognitionResponseTypeDef:
        """
        Starts asynchronous recognition of celebrities in a stored video.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/start_celebrity_recognition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#start_celebrity_recognition)
        """

    def start_content_moderation(
        self, **kwargs: Unpack[StartContentModerationRequestRequestTypeDef]
    ) -> StartContentModerationResponseTypeDef:
        """
        Starts asynchronous detection of inappropriate, unwanted, or offensive content
        in a stored video.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/start_content_moderation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#start_content_moderation)
        """

    def start_face_detection(
        self, **kwargs: Unpack[StartFaceDetectionRequestRequestTypeDef]
    ) -> StartFaceDetectionResponseTypeDef:
        """
        Starts asynchronous detection of faces in a stored video.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/start_face_detection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#start_face_detection)
        """

    def start_face_search(
        self, **kwargs: Unpack[StartFaceSearchRequestRequestTypeDef]
    ) -> StartFaceSearchResponseTypeDef:
        """
        Starts the asynchronous search for faces in a collection that match the faces
        of persons detected in a stored video.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/start_face_search.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#start_face_search)
        """

    def start_label_detection(
        self, **kwargs: Unpack[StartLabelDetectionRequestRequestTypeDef]
    ) -> StartLabelDetectionResponseTypeDef:
        """
        Starts asynchronous detection of labels in a stored video.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/start_label_detection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#start_label_detection)
        """

    def start_media_analysis_job(
        self, **kwargs: Unpack[StartMediaAnalysisJobRequestRequestTypeDef]
    ) -> StartMediaAnalysisJobResponseTypeDef:
        """
        Initiates a new media analysis job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/start_media_analysis_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#start_media_analysis_job)
        """

    def start_person_tracking(
        self, **kwargs: Unpack[StartPersonTrackingRequestRequestTypeDef]
    ) -> StartPersonTrackingResponseTypeDef:
        """
        Starts the asynchronous tracking of a person's path in a stored video.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/start_person_tracking.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#start_person_tracking)
        """

    def start_project_version(
        self, **kwargs: Unpack[StartProjectVersionRequestRequestTypeDef]
    ) -> StartProjectVersionResponseTypeDef:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/start_project_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#start_project_version)
        """

    def start_segment_detection(
        self, **kwargs: Unpack[StartSegmentDetectionRequestRequestTypeDef]
    ) -> StartSegmentDetectionResponseTypeDef:
        """
        Starts asynchronous detection of segment detection in a stored video.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/start_segment_detection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#start_segment_detection)
        """

    def start_stream_processor(
        self, **kwargs: Unpack[StartStreamProcessorRequestRequestTypeDef]
    ) -> StartStreamProcessorResponseTypeDef:
        """
        Starts processing a stream processor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/start_stream_processor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#start_stream_processor)
        """

    def start_text_detection(
        self, **kwargs: Unpack[StartTextDetectionRequestRequestTypeDef]
    ) -> StartTextDetectionResponseTypeDef:
        """
        Starts asynchronous detection of text in a stored video.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/start_text_detection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#start_text_detection)
        """

    def stop_project_version(
        self, **kwargs: Unpack[StopProjectVersionRequestRequestTypeDef]
    ) -> StopProjectVersionResponseTypeDef:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/stop_project_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#stop_project_version)
        """

    def stop_stream_processor(
        self, **kwargs: Unpack[StopStreamProcessorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops a running stream processor that was created by
        <a>CreateStreamProcessor</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/stop_stream_processor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#stop_stream_processor)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more key-value tags to an Amazon Rekognition collection, stream
        processor, or Custom Labels model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from an Amazon Rekognition collection, stream
        processor, or Custom Labels model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#untag_resource)
        """

    def update_dataset_entries(
        self, **kwargs: Unpack[UpdateDatasetEntriesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation applies only to Amazon Rekognition Custom Labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/update_dataset_entries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#update_dataset_entries)
        """

    def update_stream_processor(
        self, **kwargs: Unpack[UpdateStreamProcessorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Allows you to update a stream processor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/update_stream_processor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#update_stream_processor)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_project_versions"]
    ) -> DescribeProjectVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_projects"]
    ) -> DescribeProjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_collections"]
    ) -> ListCollectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataset_entries"]
    ) -> ListDatasetEntriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataset_labels"]
    ) -> ListDatasetLabelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_faces"]) -> ListFacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_project_policies"]
    ) -> ListProjectPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_stream_processors"]
    ) -> ListStreamProcessorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["project_version_running"]
    ) -> ProjectVersionRunningWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["project_version_training_completed"]
    ) -> ProjectVersionTrainingCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rekognition/client/#get_waiter)
        """
