"""
Type annotations for iotanalytics service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iotanalytics.client import IoTAnalyticsClient

    session = Session()
    client: IoTAnalyticsClient = session.client("iotanalytics")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListChannelsPaginator,
    ListDatasetContentsPaginator,
    ListDatasetsPaginator,
    ListDatastoresPaginator,
    ListPipelinesPaginator,
)
from .type_defs import (
    BatchPutMessageRequestRequestTypeDef,
    BatchPutMessageResponseTypeDef,
    CancelPipelineReprocessingRequestRequestTypeDef,
    CreateChannelRequestRequestTypeDef,
    CreateChannelResponseTypeDef,
    CreateDatasetContentRequestRequestTypeDef,
    CreateDatasetContentResponseTypeDef,
    CreateDatasetRequestRequestTypeDef,
    CreateDatasetResponseTypeDef,
    CreateDatastoreRequestRequestTypeDef,
    CreateDatastoreResponseTypeDef,
    CreatePipelineRequestRequestTypeDef,
    CreatePipelineResponseTypeDef,
    DeleteChannelRequestRequestTypeDef,
    DeleteDatasetContentRequestRequestTypeDef,
    DeleteDatasetRequestRequestTypeDef,
    DeleteDatastoreRequestRequestTypeDef,
    DeletePipelineRequestRequestTypeDef,
    DescribeChannelRequestRequestTypeDef,
    DescribeChannelResponseTypeDef,
    DescribeDatasetRequestRequestTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeDatastoreRequestRequestTypeDef,
    DescribeDatastoreResponseTypeDef,
    DescribeLoggingOptionsResponseTypeDef,
    DescribePipelineRequestRequestTypeDef,
    DescribePipelineResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetDatasetContentRequestRequestTypeDef,
    GetDatasetContentResponseTypeDef,
    ListChannelsRequestRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListDatasetContentsRequestRequestTypeDef,
    ListDatasetContentsResponseTypeDef,
    ListDatasetsRequestRequestTypeDef,
    ListDatasetsResponseTypeDef,
    ListDatastoresRequestRequestTypeDef,
    ListDatastoresResponseTypeDef,
    ListPipelinesRequestRequestTypeDef,
    ListPipelinesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutLoggingOptionsRequestRequestTypeDef,
    RunPipelineActivityRequestRequestTypeDef,
    RunPipelineActivityResponseTypeDef,
    SampleChannelDataRequestRequestTypeDef,
    SampleChannelDataResponseTypeDef,
    StartPipelineReprocessingRequestRequestTypeDef,
    StartPipelineReprocessingResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateChannelRequestRequestTypeDef,
    UpdateDatasetRequestRequestTypeDef,
    UpdateDatastoreRequestRequestTypeDef,
    UpdatePipelineRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("IoTAnalyticsClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class IoTAnalyticsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics.html#IoTAnalytics.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTAnalyticsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics.html#IoTAnalytics.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#close)
        """

    def batch_put_message(
        self, **kwargs: Unpack[BatchPutMessageRequestRequestTypeDef]
    ) -> BatchPutMessageResponseTypeDef:
        """
        Sends messages to a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/batch_put_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#batch_put_message)
        """

    def cancel_pipeline_reprocessing(
        self, **kwargs: Unpack[CancelPipelineReprocessingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels the reprocessing of data through the pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/cancel_pipeline_reprocessing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#cancel_pipeline_reprocessing)
        """

    def create_channel(
        self, **kwargs: Unpack[CreateChannelRequestRequestTypeDef]
    ) -> CreateChannelResponseTypeDef:
        """
        Used to create a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/create_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#create_channel)
        """

    def create_dataset(
        self, **kwargs: Unpack[CreateDatasetRequestRequestTypeDef]
    ) -> CreateDatasetResponseTypeDef:
        """
        Used to create a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/create_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#create_dataset)
        """

    def create_dataset_content(
        self, **kwargs: Unpack[CreateDatasetContentRequestRequestTypeDef]
    ) -> CreateDatasetContentResponseTypeDef:
        """
        Creates the content of a dataset by applying a <code>queryAction</code> (a SQL
        query) or a <code>containerAction</code> (executing a containerized
        application).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/create_dataset_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#create_dataset_content)
        """

    def create_datastore(
        self, **kwargs: Unpack[CreateDatastoreRequestRequestTypeDef]
    ) -> CreateDatastoreResponseTypeDef:
        """
        Creates a data store, which is a repository for messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/create_datastore.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#create_datastore)
        """

    def create_pipeline(
        self, **kwargs: Unpack[CreatePipelineRequestRequestTypeDef]
    ) -> CreatePipelineResponseTypeDef:
        """
        Creates a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/create_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#create_pipeline)
        """

    def delete_channel(
        self, **kwargs: Unpack[DeleteChannelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/delete_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#delete_channel)
        """

    def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/delete_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#delete_dataset)
        """

    def delete_dataset_content(
        self, **kwargs: Unpack[DeleteDatasetContentRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the content of the specified dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/delete_dataset_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#delete_dataset_content)
        """

    def delete_datastore(
        self, **kwargs: Unpack[DeleteDatastoreRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/delete_datastore.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#delete_datastore)
        """

    def delete_pipeline(
        self, **kwargs: Unpack[DeletePipelineRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/delete_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#delete_pipeline)
        """

    def describe_channel(
        self, **kwargs: Unpack[DescribeChannelRequestRequestTypeDef]
    ) -> DescribeChannelResponseTypeDef:
        """
        Retrieves information about a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/describe_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#describe_channel)
        """

    def describe_dataset(
        self, **kwargs: Unpack[DescribeDatasetRequestRequestTypeDef]
    ) -> DescribeDatasetResponseTypeDef:
        """
        Retrieves information about a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/describe_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#describe_dataset)
        """

    def describe_datastore(
        self, **kwargs: Unpack[DescribeDatastoreRequestRequestTypeDef]
    ) -> DescribeDatastoreResponseTypeDef:
        """
        Retrieves information about a data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/describe_datastore.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#describe_datastore)
        """

    def describe_logging_options(self) -> DescribeLoggingOptionsResponseTypeDef:
        """
        Retrieves the current settings of the IoT Analytics logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/describe_logging_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#describe_logging_options)
        """

    def describe_pipeline(
        self, **kwargs: Unpack[DescribePipelineRequestRequestTypeDef]
    ) -> DescribePipelineResponseTypeDef:
        """
        Retrieves information about a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/describe_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#describe_pipeline)
        """

    def get_dataset_content(
        self, **kwargs: Unpack[GetDatasetContentRequestRequestTypeDef]
    ) -> GetDatasetContentResponseTypeDef:
        """
        Retrieves the contents of a dataset as presigned URIs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/get_dataset_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#get_dataset_content)
        """

    def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Retrieves a list of channels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/list_channels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#list_channels)
        """

    def list_dataset_contents(
        self, **kwargs: Unpack[ListDatasetContentsRequestRequestTypeDef]
    ) -> ListDatasetContentsResponseTypeDef:
        """
        Lists information about dataset contents that have been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/list_dataset_contents.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#list_dataset_contents)
        """

    def list_datasets(
        self, **kwargs: Unpack[ListDatasetsRequestRequestTypeDef]
    ) -> ListDatasetsResponseTypeDef:
        """
        Retrieves information about datasets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/list_datasets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#list_datasets)
        """

    def list_datastores(
        self, **kwargs: Unpack[ListDatastoresRequestRequestTypeDef]
    ) -> ListDatastoresResponseTypeDef:
        """
        Retrieves a list of data stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/list_datastores.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#list_datastores)
        """

    def list_pipelines(
        self, **kwargs: Unpack[ListPipelinesRequestRequestTypeDef]
    ) -> ListPipelinesResponseTypeDef:
        """
        Retrieves a list of pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/list_pipelines.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#list_pipelines)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags (metadata) that you have assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#list_tags_for_resource)
        """

    def put_logging_options(
        self, **kwargs: Unpack[PutLoggingOptionsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets or updates the IoT Analytics logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/put_logging_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#put_logging_options)
        """

    def run_pipeline_activity(
        self, **kwargs: Unpack[RunPipelineActivityRequestRequestTypeDef]
    ) -> RunPipelineActivityResponseTypeDef:
        """
        Simulates the results of running a pipeline activity on a message payload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/run_pipeline_activity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#run_pipeline_activity)
        """

    def sample_channel_data(
        self, **kwargs: Unpack[SampleChannelDataRequestRequestTypeDef]
    ) -> SampleChannelDataResponseTypeDef:
        """
        Retrieves a sample of messages from the specified channel ingested during the
        specified timeframe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/sample_channel_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#sample_channel_data)
        """

    def start_pipeline_reprocessing(
        self, **kwargs: Unpack[StartPipelineReprocessingRequestRequestTypeDef]
    ) -> StartPipelineReprocessingResponseTypeDef:
        """
        Starts the reprocessing of raw message data through the pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/start_pipeline_reprocessing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#start_pipeline_reprocessing)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds to or modifies the tags of the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the given tags (metadata) from the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#untag_resource)
        """

    def update_channel(
        self, **kwargs: Unpack[UpdateChannelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used to update the settings of a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/update_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#update_channel)
        """

    def update_dataset(
        self, **kwargs: Unpack[UpdateDatasetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the settings of a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/update_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#update_dataset)
        """

    def update_datastore(
        self, **kwargs: Unpack[UpdateDatastoreRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used to update the settings of a data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/update_datastore.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#update_datastore)
        """

    def update_pipeline(
        self, **kwargs: Unpack[UpdatePipelineRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the settings of a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/update_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#update_pipeline)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataset_contents"]
    ) -> ListDatasetContentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_datasets"]) -> ListDatasetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_datastores"]) -> ListDatastoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_pipelines"]) -> ListPipelinesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotanalytics/client/#get_paginator)
        """
