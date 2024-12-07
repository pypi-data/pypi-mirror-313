"""
Type annotations for discovery service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_discovery.client import ApplicationDiscoveryServiceClient

    session = Session()
    client: ApplicationDiscoveryServiceClient = session.client("discovery")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeAgentsPaginator,
    DescribeContinuousExportsPaginator,
    DescribeExportConfigurationsPaginator,
    DescribeExportTasksPaginator,
    DescribeImportTasksPaginator,
    DescribeTagsPaginator,
    ListConfigurationsPaginator,
)
from .type_defs import (
    AssociateConfigurationItemsToApplicationRequestRequestTypeDef,
    BatchDeleteAgentsRequestRequestTypeDef,
    BatchDeleteAgentsResponseTypeDef,
    BatchDeleteImportDataRequestRequestTypeDef,
    BatchDeleteImportDataResponseTypeDef,
    CreateApplicationRequestRequestTypeDef,
    CreateApplicationResponseTypeDef,
    CreateTagsRequestRequestTypeDef,
    DeleteApplicationsRequestRequestTypeDef,
    DeleteTagsRequestRequestTypeDef,
    DescribeAgentsRequestRequestTypeDef,
    DescribeAgentsResponseTypeDef,
    DescribeBatchDeleteConfigurationTaskRequestRequestTypeDef,
    DescribeBatchDeleteConfigurationTaskResponseTypeDef,
    DescribeConfigurationsRequestRequestTypeDef,
    DescribeConfigurationsResponseTypeDef,
    DescribeContinuousExportsRequestRequestTypeDef,
    DescribeContinuousExportsResponseTypeDef,
    DescribeExportConfigurationsRequestRequestTypeDef,
    DescribeExportConfigurationsResponseTypeDef,
    DescribeExportTasksRequestRequestTypeDef,
    DescribeExportTasksResponseTypeDef,
    DescribeImportTasksRequestRequestTypeDef,
    DescribeImportTasksResponseTypeDef,
    DescribeTagsRequestRequestTypeDef,
    DescribeTagsResponseTypeDef,
    DisassociateConfigurationItemsFromApplicationRequestRequestTypeDef,
    ExportConfigurationsResponseTypeDef,
    GetDiscoverySummaryResponseTypeDef,
    ListConfigurationsRequestRequestTypeDef,
    ListConfigurationsResponseTypeDef,
    ListServerNeighborsRequestRequestTypeDef,
    ListServerNeighborsResponseTypeDef,
    StartBatchDeleteConfigurationTaskRequestRequestTypeDef,
    StartBatchDeleteConfigurationTaskResponseTypeDef,
    StartContinuousExportResponseTypeDef,
    StartDataCollectionByAgentIdsRequestRequestTypeDef,
    StartDataCollectionByAgentIdsResponseTypeDef,
    StartExportTaskRequestRequestTypeDef,
    StartExportTaskResponseTypeDef,
    StartImportTaskRequestRequestTypeDef,
    StartImportTaskResponseTypeDef,
    StopContinuousExportRequestRequestTypeDef,
    StopContinuousExportResponseTypeDef,
    StopDataCollectionByAgentIdsRequestRequestTypeDef,
    StopDataCollectionByAgentIdsResponseTypeDef,
    UpdateApplicationRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ApplicationDiscoveryServiceClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AuthorizationErrorException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictErrorException: Type[BotocoreClientError]
    HomeRegionNotSetException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    OperationNotPermittedException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServerInternalErrorException: Type[BotocoreClientError]


class ApplicationDiscoveryServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ApplicationDiscoveryServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#close)
        """

    def associate_configuration_items_to_application(
        self, **kwargs: Unpack[AssociateConfigurationItemsToApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates one or more configuration items with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/associate_configuration_items_to_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#associate_configuration_items_to_application)
        """

    def batch_delete_agents(
        self, **kwargs: Unpack[BatchDeleteAgentsRequestRequestTypeDef]
    ) -> BatchDeleteAgentsResponseTypeDef:
        """
        Deletes one or more agents or collectors as specified by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/batch_delete_agents.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#batch_delete_agents)
        """

    def batch_delete_import_data(
        self, **kwargs: Unpack[BatchDeleteImportDataRequestRequestTypeDef]
    ) -> BatchDeleteImportDataResponseTypeDef:
        """
        Deletes one or more import tasks, each identified by their import ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/batch_delete_import_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#batch_delete_import_data)
        """

    def create_application(
        self, **kwargs: Unpack[CreateApplicationRequestRequestTypeDef]
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates an application with the given name and description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/create_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#create_application)
        """

    def create_tags(self, **kwargs: Unpack[CreateTagsRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates one or more tags for configuration items.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/create_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#create_tags)
        """

    def delete_applications(
        self, **kwargs: Unpack[DeleteApplicationsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a list of applications and their associations with configuration items.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/delete_applications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#delete_applications)
        """

    def delete_tags(self, **kwargs: Unpack[DeleteTagsRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the association between configuration items and one or more tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/delete_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#delete_tags)
        """

    def describe_agents(
        self, **kwargs: Unpack[DescribeAgentsRequestRequestTypeDef]
    ) -> DescribeAgentsResponseTypeDef:
        """
        Lists agents or collectors as specified by ID or other filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/describe_agents.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#describe_agents)
        """

    def describe_batch_delete_configuration_task(
        self, **kwargs: Unpack[DescribeBatchDeleteConfigurationTaskRequestRequestTypeDef]
    ) -> DescribeBatchDeleteConfigurationTaskResponseTypeDef:
        """
        Takes a unique deletion task identifier as input and returns metadata about a
        configuration deletion task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/describe_batch_delete_configuration_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#describe_batch_delete_configuration_task)
        """

    def describe_configurations(
        self, **kwargs: Unpack[DescribeConfigurationsRequestRequestTypeDef]
    ) -> DescribeConfigurationsResponseTypeDef:
        """
        Retrieves attributes for a list of configuration item IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/describe_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#describe_configurations)
        """

    def describe_continuous_exports(
        self, **kwargs: Unpack[DescribeContinuousExportsRequestRequestTypeDef]
    ) -> DescribeContinuousExportsResponseTypeDef:
        """
        Lists exports as specified by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/describe_continuous_exports.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#describe_continuous_exports)
        """

    def describe_export_configurations(
        self, **kwargs: Unpack[DescribeExportConfigurationsRequestRequestTypeDef]
    ) -> DescribeExportConfigurationsResponseTypeDef:
        """
        <code>DescribeExportConfigurations</code> is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/describe_export_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#describe_export_configurations)
        """

    def describe_export_tasks(
        self, **kwargs: Unpack[DescribeExportTasksRequestRequestTypeDef]
    ) -> DescribeExportTasksResponseTypeDef:
        """
        Retrieve status of one or more export tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/describe_export_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#describe_export_tasks)
        """

    def describe_import_tasks(
        self, **kwargs: Unpack[DescribeImportTasksRequestRequestTypeDef]
    ) -> DescribeImportTasksResponseTypeDef:
        """
        Returns an array of import tasks for your account, including status
        information, times, IDs, the Amazon S3 Object URL for the import file, and
        more.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/describe_import_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#describe_import_tasks)
        """

    def describe_tags(
        self, **kwargs: Unpack[DescribeTagsRequestRequestTypeDef]
    ) -> DescribeTagsResponseTypeDef:
        """
        Retrieves a list of configuration items that have tags as specified by the
        key-value pairs, name and value, passed to the optional parameter
        <code>filters</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/describe_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#describe_tags)
        """

    def disassociate_configuration_items_from_application(
        self, **kwargs: Unpack[DisassociateConfigurationItemsFromApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates one or more configuration items from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/disassociate_configuration_items_from_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#disassociate_configuration_items_from_application)
        """

    def export_configurations(self) -> ExportConfigurationsResponseTypeDef:
        """
        Deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/export_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#export_configurations)
        """

    def get_discovery_summary(self) -> GetDiscoverySummaryResponseTypeDef:
        """
        Retrieves a short summary of discovered assets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/get_discovery_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#get_discovery_summary)
        """

    def list_configurations(
        self, **kwargs: Unpack[ListConfigurationsRequestRequestTypeDef]
    ) -> ListConfigurationsResponseTypeDef:
        """
        Retrieves a list of configuration items as specified by the value passed to the
        required parameter <code>configurationType</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/list_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#list_configurations)
        """

    def list_server_neighbors(
        self, **kwargs: Unpack[ListServerNeighborsRequestRequestTypeDef]
    ) -> ListServerNeighborsResponseTypeDef:
        """
        Retrieves a list of servers that are one network hop away from a specified
        server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/list_server_neighbors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#list_server_neighbors)
        """

    def start_batch_delete_configuration_task(
        self, **kwargs: Unpack[StartBatchDeleteConfigurationTaskRequestRequestTypeDef]
    ) -> StartBatchDeleteConfigurationTaskResponseTypeDef:
        """
        Takes a list of configurationId as input and starts an asynchronous deletion
        task to remove the configurationItems.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/start_batch_delete_configuration_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#start_batch_delete_configuration_task)
        """

    def start_continuous_export(self) -> StartContinuousExportResponseTypeDef:
        """
        Start the continuous flow of agent's discovered data into Amazon Athena.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/start_continuous_export.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#start_continuous_export)
        """

    def start_data_collection_by_agent_ids(
        self, **kwargs: Unpack[StartDataCollectionByAgentIdsRequestRequestTypeDef]
    ) -> StartDataCollectionByAgentIdsResponseTypeDef:
        """
        Instructs the specified agents to start collecting data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/start_data_collection_by_agent_ids.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#start_data_collection_by_agent_ids)
        """

    def start_export_task(
        self, **kwargs: Unpack[StartExportTaskRequestRequestTypeDef]
    ) -> StartExportTaskResponseTypeDef:
        """
        Begins the export of a discovered data report to an Amazon S3 bucket managed by
        Amazon Web Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/start_export_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#start_export_task)
        """

    def start_import_task(
        self, **kwargs: Unpack[StartImportTaskRequestRequestTypeDef]
    ) -> StartImportTaskResponseTypeDef:
        """
        Starts an import task, which allows you to import details of your on-premises
        environment directly into Amazon Web Services Migration Hub without having to
        use the Amazon Web Services Application Discovery Service (Application
        Discovery Service) tools such as the Amazon Web Services Application D...

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/start_import_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#start_import_task)
        """

    def stop_continuous_export(
        self, **kwargs: Unpack[StopContinuousExportRequestRequestTypeDef]
    ) -> StopContinuousExportResponseTypeDef:
        """
        Stop the continuous flow of agent's discovered data into Amazon Athena.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/stop_continuous_export.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#stop_continuous_export)
        """

    def stop_data_collection_by_agent_ids(
        self, **kwargs: Unpack[StopDataCollectionByAgentIdsRequestRequestTypeDef]
    ) -> StopDataCollectionByAgentIdsResponseTypeDef:
        """
        Instructs the specified agents to stop collecting data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/stop_data_collection_by_agent_ids.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#stop_data_collection_by_agent_ids)
        """

    def update_application(
        self, **kwargs: Unpack[UpdateApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates metadata about an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/update_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#update_application)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_agents"]) -> DescribeAgentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_continuous_exports"]
    ) -> DescribeContinuousExportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_export_configurations"]
    ) -> DescribeExportConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_export_tasks"]
    ) -> DescribeExportTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_import_tasks"]
    ) -> DescribeImportTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_tags"]) -> DescribeTagsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configurations"]
    ) -> ListConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_discovery/client/#get_paginator)
        """
