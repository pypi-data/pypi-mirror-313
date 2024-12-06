"""
Type annotations for neptune-graph service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_neptune_graph.client import NeptuneGraphClient

    session = Session()
    client: NeptuneGraphClient = session.client("neptune-graph")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListExportTasksPaginator,
    ListGraphSnapshotsPaginator,
    ListGraphsPaginator,
    ListImportTasksPaginator,
    ListPrivateGraphEndpointsPaginator,
)
from .type_defs import (
    CancelExportTaskInputRequestTypeDef,
    CancelExportTaskOutputTypeDef,
    CancelImportTaskInputRequestTypeDef,
    CancelImportTaskOutputTypeDef,
    CancelQueryInputRequestTypeDef,
    CreateGraphInputRequestTypeDef,
    CreateGraphOutputTypeDef,
    CreateGraphSnapshotInputRequestTypeDef,
    CreateGraphSnapshotOutputTypeDef,
    CreateGraphUsingImportTaskInputRequestTypeDef,
    CreateGraphUsingImportTaskOutputTypeDef,
    CreatePrivateGraphEndpointInputRequestTypeDef,
    CreatePrivateGraphEndpointOutputTypeDef,
    DeleteGraphInputRequestTypeDef,
    DeleteGraphOutputTypeDef,
    DeleteGraphSnapshotInputRequestTypeDef,
    DeleteGraphSnapshotOutputTypeDef,
    DeletePrivateGraphEndpointInputRequestTypeDef,
    DeletePrivateGraphEndpointOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    ExecuteQueryInputRequestTypeDef,
    ExecuteQueryOutputTypeDef,
    GetExportTaskInputRequestTypeDef,
    GetExportTaskOutputTypeDef,
    GetGraphInputRequestTypeDef,
    GetGraphOutputTypeDef,
    GetGraphSnapshotInputRequestTypeDef,
    GetGraphSnapshotOutputTypeDef,
    GetGraphSummaryInputRequestTypeDef,
    GetGraphSummaryOutputTypeDef,
    GetImportTaskInputRequestTypeDef,
    GetImportTaskOutputTypeDef,
    GetPrivateGraphEndpointInputRequestTypeDef,
    GetPrivateGraphEndpointOutputTypeDef,
    GetQueryInputRequestTypeDef,
    GetQueryOutputTypeDef,
    ListExportTasksInputRequestTypeDef,
    ListExportTasksOutputTypeDef,
    ListGraphsInputRequestTypeDef,
    ListGraphSnapshotsInputRequestTypeDef,
    ListGraphSnapshotsOutputTypeDef,
    ListGraphsOutputTypeDef,
    ListImportTasksInputRequestTypeDef,
    ListImportTasksOutputTypeDef,
    ListPrivateGraphEndpointsInputRequestTypeDef,
    ListPrivateGraphEndpointsOutputTypeDef,
    ListQueriesInputRequestTypeDef,
    ListQueriesOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ResetGraphInputRequestTypeDef,
    ResetGraphOutputTypeDef,
    RestoreGraphFromSnapshotInputRequestTypeDef,
    RestoreGraphFromSnapshotOutputTypeDef,
    StartExportTaskInputRequestTypeDef,
    StartExportTaskOutputTypeDef,
    StartImportTaskInputRequestTypeDef,
    StartImportTaskOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateGraphInputRequestTypeDef,
    UpdateGraphOutputTypeDef,
)
from .waiter import (
    ExportTaskCancelledWaiter,
    ExportTaskSuccessfulWaiter,
    GraphAvailableWaiter,
    GraphDeletedWaiter,
    GraphSnapshotAvailableWaiter,
    GraphSnapshotDeletedWaiter,
    ImportTaskCancelledWaiter,
    ImportTaskSuccessfulWaiter,
    PrivateGraphEndpointAvailableWaiter,
    PrivateGraphEndpointDeletedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("NeptuneGraphClient",)


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
    UnprocessableException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class NeptuneGraphClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph.html#NeptuneGraph.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        NeptuneGraphClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph.html#NeptuneGraph.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#close)
        """

    def cancel_export_task(
        self, **kwargs: Unpack[CancelExportTaskInputRequestTypeDef]
    ) -> CancelExportTaskOutputTypeDef:
        """
        Cancel the specified export task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/cancel_export_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#cancel_export_task)
        """

    def cancel_import_task(
        self, **kwargs: Unpack[CancelImportTaskInputRequestTypeDef]
    ) -> CancelImportTaskOutputTypeDef:
        """
        Deletes the specified import task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/cancel_import_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#cancel_import_task)
        """

    def cancel_query(
        self, **kwargs: Unpack[CancelQueryInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels a specified query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/cancel_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#cancel_query)
        """

    def create_graph(
        self, **kwargs: Unpack[CreateGraphInputRequestTypeDef]
    ) -> CreateGraphOutputTypeDef:
        """
        Creates a new Neptune Analytics graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/create_graph.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#create_graph)
        """

    def create_graph_snapshot(
        self, **kwargs: Unpack[CreateGraphSnapshotInputRequestTypeDef]
    ) -> CreateGraphSnapshotOutputTypeDef:
        """
        Creates a snapshot of the specific graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/create_graph_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#create_graph_snapshot)
        """

    def create_graph_using_import_task(
        self, **kwargs: Unpack[CreateGraphUsingImportTaskInputRequestTypeDef]
    ) -> CreateGraphUsingImportTaskOutputTypeDef:
        """
        Creates a new Neptune Analytics graph and imports data into it, either from
        Amazon Simple Storage Service (S3) or from a Neptune database or a Neptune
        database snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/create_graph_using_import_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#create_graph_using_import_task)
        """

    def create_private_graph_endpoint(
        self, **kwargs: Unpack[CreatePrivateGraphEndpointInputRequestTypeDef]
    ) -> CreatePrivateGraphEndpointOutputTypeDef:
        """
        Create a private graph endpoint to allow private access from to the graph from
        within a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/create_private_graph_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#create_private_graph_endpoint)
        """

    def delete_graph(
        self, **kwargs: Unpack[DeleteGraphInputRequestTypeDef]
    ) -> DeleteGraphOutputTypeDef:
        """
        Deletes the specified graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/delete_graph.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#delete_graph)
        """

    def delete_graph_snapshot(
        self, **kwargs: Unpack[DeleteGraphSnapshotInputRequestTypeDef]
    ) -> DeleteGraphSnapshotOutputTypeDef:
        """
        Deletes the specifed graph snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/delete_graph_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#delete_graph_snapshot)
        """

    def delete_private_graph_endpoint(
        self, **kwargs: Unpack[DeletePrivateGraphEndpointInputRequestTypeDef]
    ) -> DeletePrivateGraphEndpointOutputTypeDef:
        """
        Deletes a private graph endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/delete_private_graph_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#delete_private_graph_endpoint)
        """

    def execute_query(
        self, **kwargs: Unpack[ExecuteQueryInputRequestTypeDef]
    ) -> ExecuteQueryOutputTypeDef:
        """
        Execute an openCypher query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/execute_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#execute_query)
        """

    def get_export_task(
        self, **kwargs: Unpack[GetExportTaskInputRequestTypeDef]
    ) -> GetExportTaskOutputTypeDef:
        """
        Retrieves a specified export task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_export_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_export_task)
        """

    def get_graph(self, **kwargs: Unpack[GetGraphInputRequestTypeDef]) -> GetGraphOutputTypeDef:
        """
        Gets information about a specified graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_graph.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_graph)
        """

    def get_graph_snapshot(
        self, **kwargs: Unpack[GetGraphSnapshotInputRequestTypeDef]
    ) -> GetGraphSnapshotOutputTypeDef:
        """
        Retrieves a specified graph snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_graph_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_graph_snapshot)
        """

    def get_graph_summary(
        self, **kwargs: Unpack[GetGraphSummaryInputRequestTypeDef]
    ) -> GetGraphSummaryOutputTypeDef:
        """
        Gets a graph summary for a property graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_graph_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_graph_summary)
        """

    def get_import_task(
        self, **kwargs: Unpack[GetImportTaskInputRequestTypeDef]
    ) -> GetImportTaskOutputTypeDef:
        """
        Retrieves a specified import task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_import_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_import_task)
        """

    def get_private_graph_endpoint(
        self, **kwargs: Unpack[GetPrivateGraphEndpointInputRequestTypeDef]
    ) -> GetPrivateGraphEndpointOutputTypeDef:
        """
        Retrieves information about a specified private endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_private_graph_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_private_graph_endpoint)
        """

    def get_query(self, **kwargs: Unpack[GetQueryInputRequestTypeDef]) -> GetQueryOutputTypeDef:
        """
        Retrieves the status of a specified query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_query)
        """

    def list_export_tasks(
        self, **kwargs: Unpack[ListExportTasksInputRequestTypeDef]
    ) -> ListExportTasksOutputTypeDef:
        """
        Retrieves a list of export tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/list_export_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#list_export_tasks)
        """

    def list_graph_snapshots(
        self, **kwargs: Unpack[ListGraphSnapshotsInputRequestTypeDef]
    ) -> ListGraphSnapshotsOutputTypeDef:
        """
        Lists available snapshots of a specified Neptune Analytics graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/list_graph_snapshots.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#list_graph_snapshots)
        """

    def list_graphs(
        self, **kwargs: Unpack[ListGraphsInputRequestTypeDef]
    ) -> ListGraphsOutputTypeDef:
        """
        Lists available Neptune Analytics graphs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/list_graphs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#list_graphs)
        """

    def list_import_tasks(
        self, **kwargs: Unpack[ListImportTasksInputRequestTypeDef]
    ) -> ListImportTasksOutputTypeDef:
        """
        Lists import tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/list_import_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#list_import_tasks)
        """

    def list_private_graph_endpoints(
        self, **kwargs: Unpack[ListPrivateGraphEndpointsInputRequestTypeDef]
    ) -> ListPrivateGraphEndpointsOutputTypeDef:
        """
        Lists private endpoints for a specified Neptune Analytics graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/list_private_graph_endpoints.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#list_private_graph_endpoints)
        """

    def list_queries(
        self, **kwargs: Unpack[ListQueriesInputRequestTypeDef]
    ) -> ListQueriesOutputTypeDef:
        """
        Lists active openCypher queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/list_queries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#list_queries)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists tags associated with a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#list_tags_for_resource)
        """

    def reset_graph(
        self, **kwargs: Unpack[ResetGraphInputRequestTypeDef]
    ) -> ResetGraphOutputTypeDef:
        """
        Empties the data from a specified Neptune Analytics graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/reset_graph.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#reset_graph)
        """

    def restore_graph_from_snapshot(
        self, **kwargs: Unpack[RestoreGraphFromSnapshotInputRequestTypeDef]
    ) -> RestoreGraphFromSnapshotOutputTypeDef:
        """
        Restores a graph from a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/restore_graph_from_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#restore_graph_from_snapshot)
        """

    def start_export_task(
        self, **kwargs: Unpack[StartExportTaskInputRequestTypeDef]
    ) -> StartExportTaskOutputTypeDef:
        """
        Export data from an existing Neptune Analytics graph to Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/start_export_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#start_export_task)
        """

    def start_import_task(
        self, **kwargs: Unpack[StartImportTaskInputRequestTypeDef]
    ) -> StartImportTaskOutputTypeDef:
        """
        Import data into existing Neptune Analytics graph from Amazon Simple Storage
        Service (S3).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/start_import_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#start_import_task)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#untag_resource)
        """

    def update_graph(
        self, **kwargs: Unpack[UpdateGraphInputRequestTypeDef]
    ) -> UpdateGraphOutputTypeDef:
        """
        Updates the configuration of a specified Neptune Analytics graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/update_graph.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#update_graph)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_export_tasks"]
    ) -> ListExportTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_graph_snapshots"]
    ) -> ListGraphSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_graphs"]) -> ListGraphsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_import_tasks"]
    ) -> ListImportTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_private_graph_endpoints"]
    ) -> ListPrivateGraphEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["export_task_cancelled"]
    ) -> ExportTaskCancelledWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["export_task_successful"]
    ) -> ExportTaskSuccessfulWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["graph_available"]) -> GraphAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["graph_deleted"]) -> GraphDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["graph_snapshot_available"]
    ) -> GraphSnapshotAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["graph_snapshot_deleted"]
    ) -> GraphSnapshotDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["import_task_cancelled"]
    ) -> ImportTaskCancelledWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["import_task_successful"]
    ) -> ImportTaskSuccessfulWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["private_graph_endpoint_available"]
    ) -> PrivateGraphEndpointAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["private_graph_endpoint_deleted"]
    ) -> PrivateGraphEndpointDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptune_graph/client/#get_waiter)
        """
