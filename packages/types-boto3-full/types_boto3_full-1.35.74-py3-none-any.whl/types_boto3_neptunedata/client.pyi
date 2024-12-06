"""
Type annotations for neptunedata service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_neptunedata.client import NeptuneDataClient

    session = Session()
    client: NeptuneDataClient = session.client("neptunedata")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CancelGremlinQueryInputRequestTypeDef,
    CancelGremlinQueryOutputTypeDef,
    CancelLoaderJobInputRequestTypeDef,
    CancelLoaderJobOutputTypeDef,
    CancelMLDataProcessingJobInputRequestTypeDef,
    CancelMLDataProcessingJobOutputTypeDef,
    CancelMLModelTrainingJobInputRequestTypeDef,
    CancelMLModelTrainingJobOutputTypeDef,
    CancelMLModelTransformJobInputRequestTypeDef,
    CancelMLModelTransformJobOutputTypeDef,
    CancelOpenCypherQueryInputRequestTypeDef,
    CancelOpenCypherQueryOutputTypeDef,
    CreateMLEndpointInputRequestTypeDef,
    CreateMLEndpointOutputTypeDef,
    DeleteMLEndpointInputRequestTypeDef,
    DeleteMLEndpointOutputTypeDef,
    DeletePropertygraphStatisticsOutputTypeDef,
    DeleteSparqlStatisticsOutputTypeDef,
    ExecuteFastResetInputRequestTypeDef,
    ExecuteFastResetOutputTypeDef,
    ExecuteGremlinExplainQueryInputRequestTypeDef,
    ExecuteGremlinExplainQueryOutputTypeDef,
    ExecuteGremlinProfileQueryInputRequestTypeDef,
    ExecuteGremlinProfileQueryOutputTypeDef,
    ExecuteGremlinQueryInputRequestTypeDef,
    ExecuteGremlinQueryOutputTypeDef,
    ExecuteOpenCypherExplainQueryInputRequestTypeDef,
    ExecuteOpenCypherExplainQueryOutputTypeDef,
    ExecuteOpenCypherQueryInputRequestTypeDef,
    ExecuteOpenCypherQueryOutputTypeDef,
    GetEngineStatusOutputTypeDef,
    GetGremlinQueryStatusInputRequestTypeDef,
    GetGremlinQueryStatusOutputTypeDef,
    GetLoaderJobStatusInputRequestTypeDef,
    GetLoaderJobStatusOutputTypeDef,
    GetMLDataProcessingJobInputRequestTypeDef,
    GetMLDataProcessingJobOutputTypeDef,
    GetMLEndpointInputRequestTypeDef,
    GetMLEndpointOutputTypeDef,
    GetMLModelTrainingJobInputRequestTypeDef,
    GetMLModelTrainingJobOutputTypeDef,
    GetMLModelTransformJobInputRequestTypeDef,
    GetMLModelTransformJobOutputTypeDef,
    GetOpenCypherQueryStatusInputRequestTypeDef,
    GetOpenCypherQueryStatusOutputTypeDef,
    GetPropertygraphStatisticsOutputTypeDef,
    GetPropertygraphStreamInputRequestTypeDef,
    GetPropertygraphStreamOutputTypeDef,
    GetPropertygraphSummaryInputRequestTypeDef,
    GetPropertygraphSummaryOutputTypeDef,
    GetRDFGraphSummaryInputRequestTypeDef,
    GetRDFGraphSummaryOutputTypeDef,
    GetSparqlStatisticsOutputTypeDef,
    GetSparqlStreamInputRequestTypeDef,
    GetSparqlStreamOutputTypeDef,
    ListGremlinQueriesInputRequestTypeDef,
    ListGremlinQueriesOutputTypeDef,
    ListLoaderJobsInputRequestTypeDef,
    ListLoaderJobsOutputTypeDef,
    ListMLDataProcessingJobsInputRequestTypeDef,
    ListMLDataProcessingJobsOutputTypeDef,
    ListMLEndpointsInputRequestTypeDef,
    ListMLEndpointsOutputTypeDef,
    ListMLModelTrainingJobsInputRequestTypeDef,
    ListMLModelTrainingJobsOutputTypeDef,
    ListMLModelTransformJobsInputRequestTypeDef,
    ListMLModelTransformJobsOutputTypeDef,
    ListOpenCypherQueriesInputRequestTypeDef,
    ListOpenCypherQueriesOutputTypeDef,
    ManagePropertygraphStatisticsInputRequestTypeDef,
    ManagePropertygraphStatisticsOutputTypeDef,
    ManageSparqlStatisticsInputRequestTypeDef,
    ManageSparqlStatisticsOutputTypeDef,
    StartLoaderJobInputRequestTypeDef,
    StartLoaderJobOutputTypeDef,
    StartMLDataProcessingJobInputRequestTypeDef,
    StartMLDataProcessingJobOutputTypeDef,
    StartMLModelTrainingJobInputRequestTypeDef,
    StartMLModelTrainingJobOutputTypeDef,
    StartMLModelTransformJobInputRequestTypeDef,
    StartMLModelTransformJobOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("NeptuneDataClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    BulkLoadIdNotFoundException: Type[BotocoreClientError]
    CancelledByUserException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientTimeoutException: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConstraintViolationException: Type[BotocoreClientError]
    ExpiredStreamException: Type[BotocoreClientError]
    FailureByQueryException: Type[BotocoreClientError]
    IllegalArgumentException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidNumericDataException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LoadUrlAccessDeniedException: Type[BotocoreClientError]
    MLResourceNotFoundException: Type[BotocoreClientError]
    MalformedQueryException: Type[BotocoreClientError]
    MemoryLimitExceededException: Type[BotocoreClientError]
    MethodNotAllowedException: Type[BotocoreClientError]
    MissingParameterException: Type[BotocoreClientError]
    ParsingException: Type[BotocoreClientError]
    PreconditionsFailedException: Type[BotocoreClientError]
    QueryLimitExceededException: Type[BotocoreClientError]
    QueryLimitException: Type[BotocoreClientError]
    QueryTooLargeException: Type[BotocoreClientError]
    ReadOnlyViolationException: Type[BotocoreClientError]
    S3Exception: Type[BotocoreClientError]
    ServerShutdownException: Type[BotocoreClientError]
    StatisticsNotAvailableException: Type[BotocoreClientError]
    StreamRecordsNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TimeLimitExceededException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]

class NeptuneDataClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        NeptuneDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#close)
        """

    def cancel_gremlin_query(
        self, **kwargs: Unpack[CancelGremlinQueryInputRequestTypeDef]
    ) -> CancelGremlinQueryOutputTypeDef:
        """
        Cancels a Gremlin query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/cancel_gremlin_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#cancel_gremlin_query)
        """

    def cancel_loader_job(
        self, **kwargs: Unpack[CancelLoaderJobInputRequestTypeDef]
    ) -> CancelLoaderJobOutputTypeDef:
        """
        Cancels a specified load job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/cancel_loader_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#cancel_loader_job)
        """

    def cancel_ml_data_processing_job(
        self, **kwargs: Unpack[CancelMLDataProcessingJobInputRequestTypeDef]
    ) -> CancelMLDataProcessingJobOutputTypeDef:
        """
        Cancels a Neptune ML data processing job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/cancel_ml_data_processing_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#cancel_ml_data_processing_job)
        """

    def cancel_ml_model_training_job(
        self, **kwargs: Unpack[CancelMLModelTrainingJobInputRequestTypeDef]
    ) -> CancelMLModelTrainingJobOutputTypeDef:
        """
        Cancels a Neptune ML model training job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/cancel_ml_model_training_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#cancel_ml_model_training_job)
        """

    def cancel_ml_model_transform_job(
        self, **kwargs: Unpack[CancelMLModelTransformJobInputRequestTypeDef]
    ) -> CancelMLModelTransformJobOutputTypeDef:
        """
        Cancels a specified model transform job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/cancel_ml_model_transform_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#cancel_ml_model_transform_job)
        """

    def cancel_open_cypher_query(
        self, **kwargs: Unpack[CancelOpenCypherQueryInputRequestTypeDef]
    ) -> CancelOpenCypherQueryOutputTypeDef:
        """
        Cancels a specified openCypher query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/cancel_open_cypher_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#cancel_open_cypher_query)
        """

    def create_ml_endpoint(
        self, **kwargs: Unpack[CreateMLEndpointInputRequestTypeDef]
    ) -> CreateMLEndpointOutputTypeDef:
        """
        Creates a new Neptune ML inference endpoint that lets you query one specific
        model that the model-training process constructed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/create_ml_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#create_ml_endpoint)
        """

    def delete_ml_endpoint(
        self, **kwargs: Unpack[DeleteMLEndpointInputRequestTypeDef]
    ) -> DeleteMLEndpointOutputTypeDef:
        """
        Cancels the creation of a Neptune ML inference endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/delete_ml_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#delete_ml_endpoint)
        """

    def delete_propertygraph_statistics(self) -> DeletePropertygraphStatisticsOutputTypeDef:
        """
        Deletes statistics for Gremlin and openCypher (property graph) data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/delete_propertygraph_statistics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#delete_propertygraph_statistics)
        """

    def delete_sparql_statistics(self) -> DeleteSparqlStatisticsOutputTypeDef:
        """
        Deletes SPARQL statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/delete_sparql_statistics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#delete_sparql_statistics)
        """

    def execute_fast_reset(
        self, **kwargs: Unpack[ExecuteFastResetInputRequestTypeDef]
    ) -> ExecuteFastResetOutputTypeDef:
        """
        The fast reset REST API lets you reset a Neptune graph quicky and easily,
        removing all of its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/execute_fast_reset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#execute_fast_reset)
        """

    def execute_gremlin_explain_query(
        self, **kwargs: Unpack[ExecuteGremlinExplainQueryInputRequestTypeDef]
    ) -> ExecuteGremlinExplainQueryOutputTypeDef:
        """
        Executes a Gremlin Explain query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/execute_gremlin_explain_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#execute_gremlin_explain_query)
        """

    def execute_gremlin_profile_query(
        self, **kwargs: Unpack[ExecuteGremlinProfileQueryInputRequestTypeDef]
    ) -> ExecuteGremlinProfileQueryOutputTypeDef:
        """
        Executes a Gremlin Profile query, which runs a specified traversal, collects
        various metrics about the run, and produces a profile report as output.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/execute_gremlin_profile_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#execute_gremlin_profile_query)
        """

    def execute_gremlin_query(
        self, **kwargs: Unpack[ExecuteGremlinQueryInputRequestTypeDef]
    ) -> ExecuteGremlinQueryOutputTypeDef:
        """
        This commands executes a Gremlin query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/execute_gremlin_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#execute_gremlin_query)
        """

    def execute_open_cypher_explain_query(
        self, **kwargs: Unpack[ExecuteOpenCypherExplainQueryInputRequestTypeDef]
    ) -> ExecuteOpenCypherExplainQueryOutputTypeDef:
        """
        Executes an openCypher <code>explain</code> request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/execute_open_cypher_explain_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#execute_open_cypher_explain_query)
        """

    def execute_open_cypher_query(
        self, **kwargs: Unpack[ExecuteOpenCypherQueryInputRequestTypeDef]
    ) -> ExecuteOpenCypherQueryOutputTypeDef:
        """
        Executes an openCypher query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/execute_open_cypher_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#execute_open_cypher_query)
        """

    def get_engine_status(self) -> GetEngineStatusOutputTypeDef:
        """
        Retrieves the status of the graph database on the host.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_engine_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_engine_status)
        """

    def get_gremlin_query_status(
        self, **kwargs: Unpack[GetGremlinQueryStatusInputRequestTypeDef]
    ) -> GetGremlinQueryStatusOutputTypeDef:
        """
        Gets the status of a specified Gremlin query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_gremlin_query_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_gremlin_query_status)
        """

    def get_loader_job_status(
        self, **kwargs: Unpack[GetLoaderJobStatusInputRequestTypeDef]
    ) -> GetLoaderJobStatusOutputTypeDef:
        """
        Gets status information about a specified load job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_loader_job_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_loader_job_status)
        """

    def get_ml_data_processing_job(
        self, **kwargs: Unpack[GetMLDataProcessingJobInputRequestTypeDef]
    ) -> GetMLDataProcessingJobOutputTypeDef:
        """
        Retrieves information about a specified data processing job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_ml_data_processing_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_ml_data_processing_job)
        """

    def get_ml_endpoint(
        self, **kwargs: Unpack[GetMLEndpointInputRequestTypeDef]
    ) -> GetMLEndpointOutputTypeDef:
        """
        Retrieves details about an inference endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_ml_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_ml_endpoint)
        """

    def get_ml_model_training_job(
        self, **kwargs: Unpack[GetMLModelTrainingJobInputRequestTypeDef]
    ) -> GetMLModelTrainingJobOutputTypeDef:
        """
        Retrieves information about a Neptune ML model training job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_ml_model_training_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_ml_model_training_job)
        """

    def get_ml_model_transform_job(
        self, **kwargs: Unpack[GetMLModelTransformJobInputRequestTypeDef]
    ) -> GetMLModelTransformJobOutputTypeDef:
        """
        Gets information about a specified model transform job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_ml_model_transform_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_ml_model_transform_job)
        """

    def get_open_cypher_query_status(
        self, **kwargs: Unpack[GetOpenCypherQueryStatusInputRequestTypeDef]
    ) -> GetOpenCypherQueryStatusOutputTypeDef:
        """
        Retrieves the status of a specified openCypher query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_open_cypher_query_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_open_cypher_query_status)
        """

    def get_propertygraph_statistics(self) -> GetPropertygraphStatisticsOutputTypeDef:
        """
        Gets property graph statistics (Gremlin and openCypher).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_propertygraph_statistics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_propertygraph_statistics)
        """

    def get_propertygraph_stream(
        self, **kwargs: Unpack[GetPropertygraphStreamInputRequestTypeDef]
    ) -> GetPropertygraphStreamOutputTypeDef:
        """
        Gets a stream for a property graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_propertygraph_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_propertygraph_stream)
        """

    def get_propertygraph_summary(
        self, **kwargs: Unpack[GetPropertygraphSummaryInputRequestTypeDef]
    ) -> GetPropertygraphSummaryOutputTypeDef:
        """
        Gets a graph summary for a property graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_propertygraph_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_propertygraph_summary)
        """

    def get_rdf_graph_summary(
        self, **kwargs: Unpack[GetRDFGraphSummaryInputRequestTypeDef]
    ) -> GetRDFGraphSummaryOutputTypeDef:
        """
        Gets a graph summary for an RDF graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_rdf_graph_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_rdf_graph_summary)
        """

    def get_sparql_statistics(self) -> GetSparqlStatisticsOutputTypeDef:
        """
        Gets RDF statistics (SPARQL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_sparql_statistics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_sparql_statistics)
        """

    def get_sparql_stream(
        self, **kwargs: Unpack[GetSparqlStreamInputRequestTypeDef]
    ) -> GetSparqlStreamOutputTypeDef:
        """
        Gets a stream for an RDF graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_sparql_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#get_sparql_stream)
        """

    def list_gremlin_queries(
        self, **kwargs: Unpack[ListGremlinQueriesInputRequestTypeDef]
    ) -> ListGremlinQueriesOutputTypeDef:
        """
        Lists active Gremlin queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_gremlin_queries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#list_gremlin_queries)
        """

    def list_loader_jobs(
        self, **kwargs: Unpack[ListLoaderJobsInputRequestTypeDef]
    ) -> ListLoaderJobsOutputTypeDef:
        """
        Retrieves a list of the <code>loadIds</code> for all active loader jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_loader_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#list_loader_jobs)
        """

    def list_ml_data_processing_jobs(
        self, **kwargs: Unpack[ListMLDataProcessingJobsInputRequestTypeDef]
    ) -> ListMLDataProcessingJobsOutputTypeDef:
        """
        Returns a list of Neptune ML data processing jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_ml_data_processing_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#list_ml_data_processing_jobs)
        """

    def list_ml_endpoints(
        self, **kwargs: Unpack[ListMLEndpointsInputRequestTypeDef]
    ) -> ListMLEndpointsOutputTypeDef:
        """
        Lists existing inference endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_ml_endpoints.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#list_ml_endpoints)
        """

    def list_ml_model_training_jobs(
        self, **kwargs: Unpack[ListMLModelTrainingJobsInputRequestTypeDef]
    ) -> ListMLModelTrainingJobsOutputTypeDef:
        """
        Lists Neptune ML model-training jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_ml_model_training_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#list_ml_model_training_jobs)
        """

    def list_ml_model_transform_jobs(
        self, **kwargs: Unpack[ListMLModelTransformJobsInputRequestTypeDef]
    ) -> ListMLModelTransformJobsOutputTypeDef:
        """
        Returns a list of model transform job IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_ml_model_transform_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#list_ml_model_transform_jobs)
        """

    def list_open_cypher_queries(
        self, **kwargs: Unpack[ListOpenCypherQueriesInputRequestTypeDef]
    ) -> ListOpenCypherQueriesOutputTypeDef:
        """
        Lists active openCypher queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_open_cypher_queries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#list_open_cypher_queries)
        """

    def manage_propertygraph_statistics(
        self, **kwargs: Unpack[ManagePropertygraphStatisticsInputRequestTypeDef]
    ) -> ManagePropertygraphStatisticsOutputTypeDef:
        """
        Manages the generation and use of property graph statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/manage_propertygraph_statistics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#manage_propertygraph_statistics)
        """

    def manage_sparql_statistics(
        self, **kwargs: Unpack[ManageSparqlStatisticsInputRequestTypeDef]
    ) -> ManageSparqlStatisticsOutputTypeDef:
        """
        Manages the generation and use of RDF graph statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/manage_sparql_statistics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#manage_sparql_statistics)
        """

    def start_loader_job(
        self, **kwargs: Unpack[StartLoaderJobInputRequestTypeDef]
    ) -> StartLoaderJobOutputTypeDef:
        """
        Starts a Neptune bulk loader job to load data from an Amazon S3 bucket into a
        Neptune DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/start_loader_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#start_loader_job)
        """

    def start_ml_data_processing_job(
        self, **kwargs: Unpack[StartMLDataProcessingJobInputRequestTypeDef]
    ) -> StartMLDataProcessingJobOutputTypeDef:
        """
        Creates a new Neptune ML data processing job for processing the graph data
        exported from Neptune for training.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/start_ml_data_processing_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#start_ml_data_processing_job)
        """

    def start_ml_model_training_job(
        self, **kwargs: Unpack[StartMLModelTrainingJobInputRequestTypeDef]
    ) -> StartMLModelTrainingJobOutputTypeDef:
        """
        Creates a new Neptune ML model training job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/start_ml_model_training_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#start_ml_model_training_job)
        """

    def start_ml_model_transform_job(
        self, **kwargs: Unpack[StartMLModelTransformJobInputRequestTypeDef]
    ) -> StartMLModelTransformJobOutputTypeDef:
        """
        Creates a new model transform job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/start_ml_model_transform_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_neptunedata/client/#start_ml_model_transform_job)
        """
