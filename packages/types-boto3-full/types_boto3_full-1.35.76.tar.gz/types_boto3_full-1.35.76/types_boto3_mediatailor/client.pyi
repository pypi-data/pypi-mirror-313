"""
Type annotations for mediatailor service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_mediatailor.client import MediaTailorClient

    session = Session()
    client: MediaTailorClient = session.client("mediatailor")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetChannelSchedulePaginator,
    ListAlertsPaginator,
    ListChannelsPaginator,
    ListLiveSourcesPaginator,
    ListPlaybackConfigurationsPaginator,
    ListPrefetchSchedulesPaginator,
    ListSourceLocationsPaginator,
    ListVodSourcesPaginator,
)
from .type_defs import (
    ConfigureLogsForChannelRequestRequestTypeDef,
    ConfigureLogsForChannelResponseTypeDef,
    ConfigureLogsForPlaybackConfigurationRequestRequestTypeDef,
    ConfigureLogsForPlaybackConfigurationResponseTypeDef,
    CreateChannelRequestRequestTypeDef,
    CreateChannelResponseTypeDef,
    CreateLiveSourceRequestRequestTypeDef,
    CreateLiveSourceResponseTypeDef,
    CreatePrefetchScheduleRequestRequestTypeDef,
    CreatePrefetchScheduleResponseTypeDef,
    CreateProgramRequestRequestTypeDef,
    CreateProgramResponseTypeDef,
    CreateSourceLocationRequestRequestTypeDef,
    CreateSourceLocationResponseTypeDef,
    CreateVodSourceRequestRequestTypeDef,
    CreateVodSourceResponseTypeDef,
    DeleteChannelPolicyRequestRequestTypeDef,
    DeleteChannelRequestRequestTypeDef,
    DeleteLiveSourceRequestRequestTypeDef,
    DeletePlaybackConfigurationRequestRequestTypeDef,
    DeletePrefetchScheduleRequestRequestTypeDef,
    DeleteProgramRequestRequestTypeDef,
    DeleteSourceLocationRequestRequestTypeDef,
    DeleteVodSourceRequestRequestTypeDef,
    DescribeChannelRequestRequestTypeDef,
    DescribeChannelResponseTypeDef,
    DescribeLiveSourceRequestRequestTypeDef,
    DescribeLiveSourceResponseTypeDef,
    DescribeProgramRequestRequestTypeDef,
    DescribeProgramResponseTypeDef,
    DescribeSourceLocationRequestRequestTypeDef,
    DescribeSourceLocationResponseTypeDef,
    DescribeVodSourceRequestRequestTypeDef,
    DescribeVodSourceResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetChannelPolicyRequestRequestTypeDef,
    GetChannelPolicyResponseTypeDef,
    GetChannelScheduleRequestRequestTypeDef,
    GetChannelScheduleResponseTypeDef,
    GetPlaybackConfigurationRequestRequestTypeDef,
    GetPlaybackConfigurationResponseTypeDef,
    GetPrefetchScheduleRequestRequestTypeDef,
    GetPrefetchScheduleResponseTypeDef,
    ListAlertsRequestRequestTypeDef,
    ListAlertsResponseTypeDef,
    ListChannelsRequestRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListLiveSourcesRequestRequestTypeDef,
    ListLiveSourcesResponseTypeDef,
    ListPlaybackConfigurationsRequestRequestTypeDef,
    ListPlaybackConfigurationsResponseTypeDef,
    ListPrefetchSchedulesRequestRequestTypeDef,
    ListPrefetchSchedulesResponseTypeDef,
    ListSourceLocationsRequestRequestTypeDef,
    ListSourceLocationsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVodSourcesRequestRequestTypeDef,
    ListVodSourcesResponseTypeDef,
    PutChannelPolicyRequestRequestTypeDef,
    PutPlaybackConfigurationRequestRequestTypeDef,
    PutPlaybackConfigurationResponseTypeDef,
    StartChannelRequestRequestTypeDef,
    StopChannelRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateChannelRequestRequestTypeDef,
    UpdateChannelResponseTypeDef,
    UpdateLiveSourceRequestRequestTypeDef,
    UpdateLiveSourceResponseTypeDef,
    UpdateProgramRequestRequestTypeDef,
    UpdateProgramResponseTypeDef,
    UpdateSourceLocationRequestRequestTypeDef,
    UpdateSourceLocationResponseTypeDef,
    UpdateVodSourceRequestRequestTypeDef,
    UpdateVodSourceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("MediaTailorClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]

class MediaTailorClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaTailorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#close)
        """

    def configure_logs_for_channel(
        self, **kwargs: Unpack[ConfigureLogsForChannelRequestRequestTypeDef]
    ) -> ConfigureLogsForChannelResponseTypeDef:
        """
        Configures Amazon CloudWatch log settings for a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/configure_logs_for_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#configure_logs_for_channel)
        """

    def configure_logs_for_playback_configuration(
        self, **kwargs: Unpack[ConfigureLogsForPlaybackConfigurationRequestRequestTypeDef]
    ) -> ConfigureLogsForPlaybackConfigurationResponseTypeDef:
        """
        Amazon CloudWatch log settings for a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/configure_logs_for_playback_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#configure_logs_for_playback_configuration)
        """

    def create_channel(
        self, **kwargs: Unpack[CreateChannelRequestRequestTypeDef]
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/create_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#create_channel)
        """

    def create_live_source(
        self, **kwargs: Unpack[CreateLiveSourceRequestRequestTypeDef]
    ) -> CreateLiveSourceResponseTypeDef:
        """
        The live source configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/create_live_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#create_live_source)
        """

    def create_prefetch_schedule(
        self, **kwargs: Unpack[CreatePrefetchScheduleRequestRequestTypeDef]
    ) -> CreatePrefetchScheduleResponseTypeDef:
        """
        Creates a prefetch schedule for a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/create_prefetch_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#create_prefetch_schedule)
        """

    def create_program(
        self, **kwargs: Unpack[CreateProgramRequestRequestTypeDef]
    ) -> CreateProgramResponseTypeDef:
        """
        Creates a program within a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/create_program.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#create_program)
        """

    def create_source_location(
        self, **kwargs: Unpack[CreateSourceLocationRequestRequestTypeDef]
    ) -> CreateSourceLocationResponseTypeDef:
        """
        Creates a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/create_source_location.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#create_source_location)
        """

    def create_vod_source(
        self, **kwargs: Unpack[CreateVodSourceRequestRequestTypeDef]
    ) -> CreateVodSourceResponseTypeDef:
        """
        The VOD source configuration parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/create_vod_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#create_vod_source)
        """

    def delete_channel(
        self, **kwargs: Unpack[DeleteChannelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/delete_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#delete_channel)
        """

    def delete_channel_policy(
        self, **kwargs: Unpack[DeleteChannelPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The channel policy to delete.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/delete_channel_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#delete_channel_policy)
        """

    def delete_live_source(
        self, **kwargs: Unpack[DeleteLiveSourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The live source to delete.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/delete_live_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#delete_live_source)
        """

    def delete_playback_configuration(
        self, **kwargs: Unpack[DeletePlaybackConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/delete_playback_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#delete_playback_configuration)
        """

    def delete_prefetch_schedule(
        self, **kwargs: Unpack[DeletePrefetchScheduleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a prefetch schedule for a specific playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/delete_prefetch_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#delete_prefetch_schedule)
        """

    def delete_program(
        self, **kwargs: Unpack[DeleteProgramRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a program within a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/delete_program.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#delete_program)
        """

    def delete_source_location(
        self, **kwargs: Unpack[DeleteSourceLocationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/delete_source_location.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#delete_source_location)
        """

    def delete_vod_source(
        self, **kwargs: Unpack[DeleteVodSourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The video on demand (VOD) source to delete.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/delete_vod_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#delete_vod_source)
        """

    def describe_channel(
        self, **kwargs: Unpack[DescribeChannelRequestRequestTypeDef]
    ) -> DescribeChannelResponseTypeDef:
        """
        Describes a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/describe_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#describe_channel)
        """

    def describe_live_source(
        self, **kwargs: Unpack[DescribeLiveSourceRequestRequestTypeDef]
    ) -> DescribeLiveSourceResponseTypeDef:
        """
        The live source to describe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/describe_live_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#describe_live_source)
        """

    def describe_program(
        self, **kwargs: Unpack[DescribeProgramRequestRequestTypeDef]
    ) -> DescribeProgramResponseTypeDef:
        """
        Describes a program within a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/describe_program.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#describe_program)
        """

    def describe_source_location(
        self, **kwargs: Unpack[DescribeSourceLocationRequestRequestTypeDef]
    ) -> DescribeSourceLocationResponseTypeDef:
        """
        Describes a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/describe_source_location.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#describe_source_location)
        """

    def describe_vod_source(
        self, **kwargs: Unpack[DescribeVodSourceRequestRequestTypeDef]
    ) -> DescribeVodSourceResponseTypeDef:
        """
        Provides details about a specific video on demand (VOD) source in a specific
        source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/describe_vod_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#describe_vod_source)
        """

    def get_channel_policy(
        self, **kwargs: Unpack[GetChannelPolicyRequestRequestTypeDef]
    ) -> GetChannelPolicyResponseTypeDef:
        """
        Returns the channel's IAM policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/get_channel_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#get_channel_policy)
        """

    def get_channel_schedule(
        self, **kwargs: Unpack[GetChannelScheduleRequestRequestTypeDef]
    ) -> GetChannelScheduleResponseTypeDef:
        """
        Retrieves information about your channel's schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/get_channel_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#get_channel_schedule)
        """

    def get_playback_configuration(
        self, **kwargs: Unpack[GetPlaybackConfigurationRequestRequestTypeDef]
    ) -> GetPlaybackConfigurationResponseTypeDef:
        """
        Retrieves a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/get_playback_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#get_playback_configuration)
        """

    def get_prefetch_schedule(
        self, **kwargs: Unpack[GetPrefetchScheduleRequestRequestTypeDef]
    ) -> GetPrefetchScheduleResponseTypeDef:
        """
        Retrieves a prefetch schedule for a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/get_prefetch_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#get_prefetch_schedule)
        """

    def list_alerts(
        self, **kwargs: Unpack[ListAlertsRequestRequestTypeDef]
    ) -> ListAlertsResponseTypeDef:
        """
        Lists the alerts that are associated with a MediaTailor channel assembly
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/list_alerts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#list_alerts)
        """

    def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Retrieves information about the channels that are associated with the current
        AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/list_channels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#list_channels)
        """

    def list_live_sources(
        self, **kwargs: Unpack[ListLiveSourcesRequestRequestTypeDef]
    ) -> ListLiveSourcesResponseTypeDef:
        """
        Lists the live sources contained in a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/list_live_sources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#list_live_sources)
        """

    def list_playback_configurations(
        self, **kwargs: Unpack[ListPlaybackConfigurationsRequestRequestTypeDef]
    ) -> ListPlaybackConfigurationsResponseTypeDef:
        """
        Retrieves existing playback configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/list_playback_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#list_playback_configurations)
        """

    def list_prefetch_schedules(
        self, **kwargs: Unpack[ListPrefetchSchedulesRequestRequestTypeDef]
    ) -> ListPrefetchSchedulesResponseTypeDef:
        """
        Lists the prefetch schedules for a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/list_prefetch_schedules.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#list_prefetch_schedules)
        """

    def list_source_locations(
        self, **kwargs: Unpack[ListSourceLocationsRequestRequestTypeDef]
    ) -> ListSourceLocationsResponseTypeDef:
        """
        Lists the source locations for a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/list_source_locations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#list_source_locations)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        A list of tags that are associated with this resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#list_tags_for_resource)
        """

    def list_vod_sources(
        self, **kwargs: Unpack[ListVodSourcesRequestRequestTypeDef]
    ) -> ListVodSourcesResponseTypeDef:
        """
        Lists the VOD sources contained in a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/list_vod_sources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#list_vod_sources)
        """

    def put_channel_policy(
        self, **kwargs: Unpack[PutChannelPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates an IAM policy for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/put_channel_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#put_channel_policy)
        """

    def put_playback_configuration(
        self, **kwargs: Unpack[PutPlaybackConfigurationRequestRequestTypeDef]
    ) -> PutPlaybackConfigurationResponseTypeDef:
        """
        Creates a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/put_playback_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#put_playback_configuration)
        """

    def start_channel(self, **kwargs: Unpack[StartChannelRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Starts a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/start_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#start_channel)
        """

    def stop_channel(self, **kwargs: Unpack[StopChannelRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Stops a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/stop_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#stop_channel)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The resource to tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The resource to untag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#untag_resource)
        """

    def update_channel(
        self, **kwargs: Unpack[UpdateChannelRequestRequestTypeDef]
    ) -> UpdateChannelResponseTypeDef:
        """
        Updates a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/update_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#update_channel)
        """

    def update_live_source(
        self, **kwargs: Unpack[UpdateLiveSourceRequestRequestTypeDef]
    ) -> UpdateLiveSourceResponseTypeDef:
        """
        Updates a live source's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/update_live_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#update_live_source)
        """

    def update_program(
        self, **kwargs: Unpack[UpdateProgramRequestRequestTypeDef]
    ) -> UpdateProgramResponseTypeDef:
        """
        Updates a program within a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/update_program.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#update_program)
        """

    def update_source_location(
        self, **kwargs: Unpack[UpdateSourceLocationRequestRequestTypeDef]
    ) -> UpdateSourceLocationResponseTypeDef:
        """
        Updates a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/update_source_location.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#update_source_location)
        """

    def update_vod_source(
        self, **kwargs: Unpack[UpdateVodSourceRequestRequestTypeDef]
    ) -> UpdateVodSourceResponseTypeDef:
        """
        Updates a VOD source's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/update_vod_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#update_vod_source)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_channel_schedule"]
    ) -> GetChannelSchedulePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_alerts"]) -> ListAlertsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_live_sources"]
    ) -> ListLiveSourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_playback_configurations"]
    ) -> ListPlaybackConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_prefetch_schedules"]
    ) -> ListPrefetchSchedulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_source_locations"]
    ) -> ListSourceLocationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_vod_sources"]) -> ListVodSourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediatailor/client/#get_paginator)
        """
