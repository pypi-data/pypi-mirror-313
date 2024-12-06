"""
Type annotations for chime-sdk-media-pipelines service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_chime_sdk_media_pipelines.client import ChimeSDKMediaPipelinesClient

    session = Session()
    client: ChimeSDKMediaPipelinesClient = session.client("chime-sdk-media-pipelines")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateMediaCapturePipelineRequestRequestTypeDef,
    CreateMediaCapturePipelineResponseTypeDef,
    CreateMediaConcatenationPipelineRequestRequestTypeDef,
    CreateMediaConcatenationPipelineResponseTypeDef,
    CreateMediaInsightsPipelineConfigurationRequestRequestTypeDef,
    CreateMediaInsightsPipelineConfigurationResponseTypeDef,
    CreateMediaInsightsPipelineRequestRequestTypeDef,
    CreateMediaInsightsPipelineResponseTypeDef,
    CreateMediaLiveConnectorPipelineRequestRequestTypeDef,
    CreateMediaLiveConnectorPipelineResponseTypeDef,
    CreateMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef,
    CreateMediaPipelineKinesisVideoStreamPoolResponseTypeDef,
    CreateMediaStreamPipelineRequestRequestTypeDef,
    CreateMediaStreamPipelineResponseTypeDef,
    DeleteMediaCapturePipelineRequestRequestTypeDef,
    DeleteMediaInsightsPipelineConfigurationRequestRequestTypeDef,
    DeleteMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef,
    DeleteMediaPipelineRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetMediaCapturePipelineRequestRequestTypeDef,
    GetMediaCapturePipelineResponseTypeDef,
    GetMediaInsightsPipelineConfigurationRequestRequestTypeDef,
    GetMediaInsightsPipelineConfigurationResponseTypeDef,
    GetMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef,
    GetMediaPipelineKinesisVideoStreamPoolResponseTypeDef,
    GetMediaPipelineRequestRequestTypeDef,
    GetMediaPipelineResponseTypeDef,
    GetSpeakerSearchTaskRequestRequestTypeDef,
    GetSpeakerSearchTaskResponseTypeDef,
    GetVoiceToneAnalysisTaskRequestRequestTypeDef,
    GetVoiceToneAnalysisTaskResponseTypeDef,
    ListMediaCapturePipelinesRequestRequestTypeDef,
    ListMediaCapturePipelinesResponseTypeDef,
    ListMediaInsightsPipelineConfigurationsRequestRequestTypeDef,
    ListMediaInsightsPipelineConfigurationsResponseTypeDef,
    ListMediaPipelineKinesisVideoStreamPoolsRequestRequestTypeDef,
    ListMediaPipelineKinesisVideoStreamPoolsResponseTypeDef,
    ListMediaPipelinesRequestRequestTypeDef,
    ListMediaPipelinesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartSpeakerSearchTaskRequestRequestTypeDef,
    StartSpeakerSearchTaskResponseTypeDef,
    StartVoiceToneAnalysisTaskRequestRequestTypeDef,
    StartVoiceToneAnalysisTaskResponseTypeDef,
    StopSpeakerSearchTaskRequestRequestTypeDef,
    StopVoiceToneAnalysisTaskRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateMediaInsightsPipelineConfigurationRequestRequestTypeDef,
    UpdateMediaInsightsPipelineConfigurationResponseTypeDef,
    UpdateMediaInsightsPipelineStatusRequestRequestTypeDef,
    UpdateMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef,
    UpdateMediaPipelineKinesisVideoStreamPoolResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ChimeSDKMediaPipelinesClient",)


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


class ChimeSDKMediaPipelinesClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeSDKMediaPipelinesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines.html#ChimeSDKMediaPipelines.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#close)
        """

    def create_media_capture_pipeline(
        self, **kwargs: Unpack[CreateMediaCapturePipelineRequestRequestTypeDef]
    ) -> CreateMediaCapturePipelineResponseTypeDef:
        """
        Creates a media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/create_media_capture_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#create_media_capture_pipeline)
        """

    def create_media_concatenation_pipeline(
        self, **kwargs: Unpack[CreateMediaConcatenationPipelineRequestRequestTypeDef]
    ) -> CreateMediaConcatenationPipelineResponseTypeDef:
        """
        Creates a media concatenation pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/create_media_concatenation_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#create_media_concatenation_pipeline)
        """

    def create_media_insights_pipeline(
        self, **kwargs: Unpack[CreateMediaInsightsPipelineRequestRequestTypeDef]
    ) -> CreateMediaInsightsPipelineResponseTypeDef:
        """
        Creates a media insights pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/create_media_insights_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#create_media_insights_pipeline)
        """

    def create_media_insights_pipeline_configuration(
        self, **kwargs: Unpack[CreateMediaInsightsPipelineConfigurationRequestRequestTypeDef]
    ) -> CreateMediaInsightsPipelineConfigurationResponseTypeDef:
        """
        A structure that contains the static configurations for a media insights
        pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/create_media_insights_pipeline_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#create_media_insights_pipeline_configuration)
        """

    def create_media_live_connector_pipeline(
        self, **kwargs: Unpack[CreateMediaLiveConnectorPipelineRequestRequestTypeDef]
    ) -> CreateMediaLiveConnectorPipelineResponseTypeDef:
        """
        Creates a media live connector pipeline in an Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/create_media_live_connector_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#create_media_live_connector_pipeline)
        """

    def create_media_pipeline_kinesis_video_stream_pool(
        self, **kwargs: Unpack[CreateMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef]
    ) -> CreateMediaPipelineKinesisVideoStreamPoolResponseTypeDef:
        """
        Creates an Amazon Kinesis Video Stream pool for use with media stream pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/create_media_pipeline_kinesis_video_stream_pool.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#create_media_pipeline_kinesis_video_stream_pool)
        """

    def create_media_stream_pipeline(
        self, **kwargs: Unpack[CreateMediaStreamPipelineRequestRequestTypeDef]
    ) -> CreateMediaStreamPipelineResponseTypeDef:
        """
        Creates a streaming media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/create_media_stream_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#create_media_stream_pipeline)
        """

    def delete_media_capture_pipeline(
        self, **kwargs: Unpack[DeleteMediaCapturePipelineRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/delete_media_capture_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#delete_media_capture_pipeline)
        """

    def delete_media_insights_pipeline_configuration(
        self, **kwargs: Unpack[DeleteMediaInsightsPipelineConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified configuration settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/delete_media_insights_pipeline_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#delete_media_insights_pipeline_configuration)
        """

    def delete_media_pipeline(
        self, **kwargs: Unpack[DeleteMediaPipelineRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/delete_media_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#delete_media_pipeline)
        """

    def delete_media_pipeline_kinesis_video_stream_pool(
        self, **kwargs: Unpack[DeleteMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Kinesis Video Stream pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/delete_media_pipeline_kinesis_video_stream_pool.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#delete_media_pipeline_kinesis_video_stream_pool)
        """

    def get_media_capture_pipeline(
        self, **kwargs: Unpack[GetMediaCapturePipelineRequestRequestTypeDef]
    ) -> GetMediaCapturePipelineResponseTypeDef:
        """
        Gets an existing media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/get_media_capture_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#get_media_capture_pipeline)
        """

    def get_media_insights_pipeline_configuration(
        self, **kwargs: Unpack[GetMediaInsightsPipelineConfigurationRequestRequestTypeDef]
    ) -> GetMediaInsightsPipelineConfigurationResponseTypeDef:
        """
        Gets the configuration settings for a media insights pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/get_media_insights_pipeline_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#get_media_insights_pipeline_configuration)
        """

    def get_media_pipeline(
        self, **kwargs: Unpack[GetMediaPipelineRequestRequestTypeDef]
    ) -> GetMediaPipelineResponseTypeDef:
        """
        Gets an existing media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/get_media_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#get_media_pipeline)
        """

    def get_media_pipeline_kinesis_video_stream_pool(
        self, **kwargs: Unpack[GetMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef]
    ) -> GetMediaPipelineKinesisVideoStreamPoolResponseTypeDef:
        """
        Gets an Kinesis video stream pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/get_media_pipeline_kinesis_video_stream_pool.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#get_media_pipeline_kinesis_video_stream_pool)
        """

    def get_speaker_search_task(
        self, **kwargs: Unpack[GetSpeakerSearchTaskRequestRequestTypeDef]
    ) -> GetSpeakerSearchTaskResponseTypeDef:
        """
        Retrieves the details of the specified speaker search task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/get_speaker_search_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#get_speaker_search_task)
        """

    def get_voice_tone_analysis_task(
        self, **kwargs: Unpack[GetVoiceToneAnalysisTaskRequestRequestTypeDef]
    ) -> GetVoiceToneAnalysisTaskResponseTypeDef:
        """
        Retrieves the details of a voice tone analysis task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/get_voice_tone_analysis_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#get_voice_tone_analysis_task)
        """

    def list_media_capture_pipelines(
        self, **kwargs: Unpack[ListMediaCapturePipelinesRequestRequestTypeDef]
    ) -> ListMediaCapturePipelinesResponseTypeDef:
        """
        Returns a list of media pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/list_media_capture_pipelines.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#list_media_capture_pipelines)
        """

    def list_media_insights_pipeline_configurations(
        self, **kwargs: Unpack[ListMediaInsightsPipelineConfigurationsRequestRequestTypeDef]
    ) -> ListMediaInsightsPipelineConfigurationsResponseTypeDef:
        """
        Lists the available media insights pipeline configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/list_media_insights_pipeline_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#list_media_insights_pipeline_configurations)
        """

    def list_media_pipeline_kinesis_video_stream_pools(
        self, **kwargs: Unpack[ListMediaPipelineKinesisVideoStreamPoolsRequestRequestTypeDef]
    ) -> ListMediaPipelineKinesisVideoStreamPoolsResponseTypeDef:
        """
        Lists the video stream pools in the media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/list_media_pipeline_kinesis_video_stream_pools.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#list_media_pipeline_kinesis_video_stream_pools)
        """

    def list_media_pipelines(
        self, **kwargs: Unpack[ListMediaPipelinesRequestRequestTypeDef]
    ) -> ListMediaPipelinesResponseTypeDef:
        """
        Returns a list of media pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/list_media_pipelines.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#list_media_pipelines)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags available for a media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#list_tags_for_resource)
        """

    def start_speaker_search_task(
        self, **kwargs: Unpack[StartSpeakerSearchTaskRequestRequestTypeDef]
    ) -> StartSpeakerSearchTaskResponseTypeDef:
        """
        Starts a speaker search task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/start_speaker_search_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#start_speaker_search_task)
        """

    def start_voice_tone_analysis_task(
        self, **kwargs: Unpack[StartVoiceToneAnalysisTaskRequestRequestTypeDef]
    ) -> StartVoiceToneAnalysisTaskResponseTypeDef:
        """
        Starts a voice tone analysis task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/start_voice_tone_analysis_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#start_voice_tone_analysis_task)
        """

    def stop_speaker_search_task(
        self, **kwargs: Unpack[StopSpeakerSearchTaskRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a speaker search task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/stop_speaker_search_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#stop_speaker_search_task)
        """

    def stop_voice_tone_analysis_task(
        self, **kwargs: Unpack[StopVoiceToneAnalysisTaskRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a voice tone analysis task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/stop_voice_tone_analysis_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#stop_voice_tone_analysis_task)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        The ARN of the media pipeline that you want to tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes any tags from a media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#untag_resource)
        """

    def update_media_insights_pipeline_configuration(
        self, **kwargs: Unpack[UpdateMediaInsightsPipelineConfigurationRequestRequestTypeDef]
    ) -> UpdateMediaInsightsPipelineConfigurationResponseTypeDef:
        """
        Updates the media insights pipeline's configuration settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/update_media_insights_pipeline_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#update_media_insights_pipeline_configuration)
        """

    def update_media_insights_pipeline_status(
        self, **kwargs: Unpack[UpdateMediaInsightsPipelineStatusRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the status of a media insights pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/update_media_insights_pipeline_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#update_media_insights_pipeline_status)
        """

    def update_media_pipeline_kinesis_video_stream_pool(
        self, **kwargs: Unpack[UpdateMediaPipelineKinesisVideoStreamPoolRequestRequestTypeDef]
    ) -> UpdateMediaPipelineKinesisVideoStreamPoolResponseTypeDef:
        """
        Updates an Amazon Kinesis Video Stream pool in a media pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-media-pipelines/client/update_media_pipeline_kinesis_video_stream_pool.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_media_pipelines/client/#update_media_pipeline_kinesis_video_stream_pool)
        """
