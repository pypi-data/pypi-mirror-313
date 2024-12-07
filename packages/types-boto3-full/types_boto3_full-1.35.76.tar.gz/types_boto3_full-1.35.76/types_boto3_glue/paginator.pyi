"""
Type annotations for glue service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_glue.client import GlueClient
    from types_boto3_glue.paginator import (
        DescribeEntityPaginator,
        GetClassifiersPaginator,
        GetConnectionsPaginator,
        GetCrawlerMetricsPaginator,
        GetCrawlersPaginator,
        GetDatabasesPaginator,
        GetDevEndpointsPaginator,
        GetJobRunsPaginator,
        GetJobsPaginator,
        GetPartitionIndexesPaginator,
        GetPartitionsPaginator,
        GetResourcePoliciesPaginator,
        GetSecurityConfigurationsPaginator,
        GetTableVersionsPaginator,
        GetTablesPaginator,
        GetTriggersPaginator,
        GetUserDefinedFunctionsPaginator,
        GetWorkflowRunsPaginator,
        ListBlueprintsPaginator,
        ListConnectionTypesPaginator,
        ListEntitiesPaginator,
        ListJobsPaginator,
        ListRegistriesPaginator,
        ListSchemaVersionsPaginator,
        ListSchemasPaginator,
        ListTableOptimizerRunsPaginator,
        ListTriggersPaginator,
        ListUsageProfilesPaginator,
        ListWorkflowsPaginator,
    )

    session = Session()
    client: GlueClient = session.client("glue")

    describe_entity_paginator: DescribeEntityPaginator = client.get_paginator("describe_entity")
    get_classifiers_paginator: GetClassifiersPaginator = client.get_paginator("get_classifiers")
    get_connections_paginator: GetConnectionsPaginator = client.get_paginator("get_connections")
    get_crawler_metrics_paginator: GetCrawlerMetricsPaginator = client.get_paginator("get_crawler_metrics")
    get_crawlers_paginator: GetCrawlersPaginator = client.get_paginator("get_crawlers")
    get_databases_paginator: GetDatabasesPaginator = client.get_paginator("get_databases")
    get_dev_endpoints_paginator: GetDevEndpointsPaginator = client.get_paginator("get_dev_endpoints")
    get_job_runs_paginator: GetJobRunsPaginator = client.get_paginator("get_job_runs")
    get_jobs_paginator: GetJobsPaginator = client.get_paginator("get_jobs")
    get_partition_indexes_paginator: GetPartitionIndexesPaginator = client.get_paginator("get_partition_indexes")
    get_partitions_paginator: GetPartitionsPaginator = client.get_paginator("get_partitions")
    get_resource_policies_paginator: GetResourcePoliciesPaginator = client.get_paginator("get_resource_policies")
    get_security_configurations_paginator: GetSecurityConfigurationsPaginator = client.get_paginator("get_security_configurations")
    get_table_versions_paginator: GetTableVersionsPaginator = client.get_paginator("get_table_versions")
    get_tables_paginator: GetTablesPaginator = client.get_paginator("get_tables")
    get_triggers_paginator: GetTriggersPaginator = client.get_paginator("get_triggers")
    get_user_defined_functions_paginator: GetUserDefinedFunctionsPaginator = client.get_paginator("get_user_defined_functions")
    get_workflow_runs_paginator: GetWorkflowRunsPaginator = client.get_paginator("get_workflow_runs")
    list_blueprints_paginator: ListBlueprintsPaginator = client.get_paginator("list_blueprints")
    list_connection_types_paginator: ListConnectionTypesPaginator = client.get_paginator("list_connection_types")
    list_entities_paginator: ListEntitiesPaginator = client.get_paginator("list_entities")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_registries_paginator: ListRegistriesPaginator = client.get_paginator("list_registries")
    list_schema_versions_paginator: ListSchemaVersionsPaginator = client.get_paginator("list_schema_versions")
    list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
    list_table_optimizer_runs_paginator: ListTableOptimizerRunsPaginator = client.get_paginator("list_table_optimizer_runs")
    list_triggers_paginator: ListTriggersPaginator = client.get_paginator("list_triggers")
    list_usage_profiles_paginator: ListUsageProfilesPaginator = client.get_paginator("list_usage_profiles")
    list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeEntityRequestDescribeEntityPaginateTypeDef,
    DescribeEntityResponseTypeDef,
    GetClassifiersRequestGetClassifiersPaginateTypeDef,
    GetClassifiersResponseTypeDef,
    GetConnectionsRequestGetConnectionsPaginateTypeDef,
    GetConnectionsResponseTypeDef,
    GetCrawlerMetricsRequestGetCrawlerMetricsPaginateTypeDef,
    GetCrawlerMetricsResponseTypeDef,
    GetCrawlersRequestGetCrawlersPaginateTypeDef,
    GetCrawlersResponseTypeDef,
    GetDatabasesRequestGetDatabasesPaginateTypeDef,
    GetDatabasesResponseTypeDef,
    GetDevEndpointsRequestGetDevEndpointsPaginateTypeDef,
    GetDevEndpointsResponseTypeDef,
    GetJobRunsRequestGetJobRunsPaginateTypeDef,
    GetJobRunsResponseTypeDef,
    GetJobsRequestGetJobsPaginateTypeDef,
    GetJobsResponsePaginatorTypeDef,
    GetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef,
    GetPartitionIndexesResponseTypeDef,
    GetPartitionsRequestGetPartitionsPaginateTypeDef,
    GetPartitionsResponseTypeDef,
    GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef,
    GetResourcePoliciesResponseTypeDef,
    GetSecurityConfigurationsRequestGetSecurityConfigurationsPaginateTypeDef,
    GetSecurityConfigurationsResponseTypeDef,
    GetTablesRequestGetTablesPaginateTypeDef,
    GetTablesResponsePaginatorTypeDef,
    GetTableVersionsRequestGetTableVersionsPaginateTypeDef,
    GetTableVersionsResponsePaginatorTypeDef,
    GetTriggersRequestGetTriggersPaginateTypeDef,
    GetTriggersResponseTypeDef,
    GetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef,
    GetUserDefinedFunctionsResponseTypeDef,
    GetWorkflowRunsRequestGetWorkflowRunsPaginateTypeDef,
    GetWorkflowRunsResponseTypeDef,
    ListBlueprintsRequestListBlueprintsPaginateTypeDef,
    ListBlueprintsResponseTypeDef,
    ListConnectionTypesRequestListConnectionTypesPaginateTypeDef,
    ListConnectionTypesResponseTypeDef,
    ListEntitiesRequestListEntitiesPaginateTypeDef,
    ListEntitiesResponseTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListRegistriesInputListRegistriesPaginateTypeDef,
    ListRegistriesResponseTypeDef,
    ListSchemasInputListSchemasPaginateTypeDef,
    ListSchemasResponseTypeDef,
    ListSchemaVersionsInputListSchemaVersionsPaginateTypeDef,
    ListSchemaVersionsResponseTypeDef,
    ListTableOptimizerRunsRequestListTableOptimizerRunsPaginateTypeDef,
    ListTableOptimizerRunsResponseTypeDef,
    ListTriggersRequestListTriggersPaginateTypeDef,
    ListTriggersResponseTypeDef,
    ListUsageProfilesRequestListUsageProfilesPaginateTypeDef,
    ListUsageProfilesResponseTypeDef,
    ListWorkflowsRequestListWorkflowsPaginateTypeDef,
    ListWorkflowsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeEntityPaginator",
    "GetClassifiersPaginator",
    "GetConnectionsPaginator",
    "GetCrawlerMetricsPaginator",
    "GetCrawlersPaginator",
    "GetDatabasesPaginator",
    "GetDevEndpointsPaginator",
    "GetJobRunsPaginator",
    "GetJobsPaginator",
    "GetPartitionIndexesPaginator",
    "GetPartitionsPaginator",
    "GetResourcePoliciesPaginator",
    "GetSecurityConfigurationsPaginator",
    "GetTableVersionsPaginator",
    "GetTablesPaginator",
    "GetTriggersPaginator",
    "GetUserDefinedFunctionsPaginator",
    "GetWorkflowRunsPaginator",
    "ListBlueprintsPaginator",
    "ListConnectionTypesPaginator",
    "ListEntitiesPaginator",
    "ListJobsPaginator",
    "ListRegistriesPaginator",
    "ListSchemaVersionsPaginator",
    "ListSchemasPaginator",
    "ListTableOptimizerRunsPaginator",
    "ListTriggersPaginator",
    "ListUsageProfilesPaginator",
    "ListWorkflowsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeEntityPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/DescribeEntity.html#Glue.Paginator.DescribeEntity)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#describeentitypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEntityRequestDescribeEntityPaginateTypeDef]
    ) -> _PageIterator[DescribeEntityResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/DescribeEntity.html#Glue.Paginator.DescribeEntity.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#describeentitypaginator)
        """

class GetClassifiersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetClassifiers.html#Glue.Paginator.GetClassifiers)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getclassifierspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetClassifiersRequestGetClassifiersPaginateTypeDef]
    ) -> _PageIterator[GetClassifiersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetClassifiers.html#Glue.Paginator.GetClassifiers.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getclassifierspaginator)
        """

class GetConnectionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetConnections.html#Glue.Paginator.GetConnections)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getconnectionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetConnectionsRequestGetConnectionsPaginateTypeDef]
    ) -> _PageIterator[GetConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetConnections.html#Glue.Paginator.GetConnections.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getconnectionspaginator)
        """

class GetCrawlerMetricsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetCrawlerMetrics.html#Glue.Paginator.GetCrawlerMetrics)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getcrawlermetricspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetCrawlerMetricsRequestGetCrawlerMetricsPaginateTypeDef]
    ) -> _PageIterator[GetCrawlerMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetCrawlerMetrics.html#Glue.Paginator.GetCrawlerMetrics.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getcrawlermetricspaginator)
        """

class GetCrawlersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetCrawlers.html#Glue.Paginator.GetCrawlers)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getcrawlerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetCrawlersRequestGetCrawlersPaginateTypeDef]
    ) -> _PageIterator[GetCrawlersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetCrawlers.html#Glue.Paginator.GetCrawlers.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getcrawlerspaginator)
        """

class GetDatabasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetDatabases.html#Glue.Paginator.GetDatabases)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getdatabasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDatabasesRequestGetDatabasesPaginateTypeDef]
    ) -> _PageIterator[GetDatabasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetDatabases.html#Glue.Paginator.GetDatabases.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getdatabasespaginator)
        """

class GetDevEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetDevEndpoints.html#Glue.Paginator.GetDevEndpoints)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getdevendpointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDevEndpointsRequestGetDevEndpointsPaginateTypeDef]
    ) -> _PageIterator[GetDevEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetDevEndpoints.html#Glue.Paginator.GetDevEndpoints.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getdevendpointspaginator)
        """

class GetJobRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetJobRuns.html#Glue.Paginator.GetJobRuns)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getjobrunspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetJobRunsRequestGetJobRunsPaginateTypeDef]
    ) -> _PageIterator[GetJobRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetJobRuns.html#Glue.Paginator.GetJobRuns.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getjobrunspaginator)
        """

class GetJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetJobs.html#Glue.Paginator.GetJobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetJobsRequestGetJobsPaginateTypeDef]
    ) -> _PageIterator[GetJobsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetJobs.html#Glue.Paginator.GetJobs.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getjobspaginator)
        """

class GetPartitionIndexesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetPartitionIndexes.html#Glue.Paginator.GetPartitionIndexes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getpartitionindexespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef]
    ) -> _PageIterator[GetPartitionIndexesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetPartitionIndexes.html#Glue.Paginator.GetPartitionIndexes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getpartitionindexespaginator)
        """

class GetPartitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetPartitions.html#Glue.Paginator.GetPartitions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getpartitionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetPartitionsRequestGetPartitionsPaginateTypeDef]
    ) -> _PageIterator[GetPartitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetPartitions.html#Glue.Paginator.GetPartitions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getpartitionspaginator)
        """

class GetResourcePoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetResourcePolicies.html#Glue.Paginator.GetResourcePolicies)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getresourcepoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef]
    ) -> _PageIterator[GetResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetResourcePolicies.html#Glue.Paginator.GetResourcePolicies.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getresourcepoliciespaginator)
        """

class GetSecurityConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetSecurityConfigurations.html#Glue.Paginator.GetSecurityConfigurations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getsecurityconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[GetSecurityConfigurationsRequestGetSecurityConfigurationsPaginateTypeDef],
    ) -> _PageIterator[GetSecurityConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetSecurityConfigurations.html#Glue.Paginator.GetSecurityConfigurations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getsecurityconfigurationspaginator)
        """

class GetTableVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetTableVersions.html#Glue.Paginator.GetTableVersions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#gettableversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetTableVersionsRequestGetTableVersionsPaginateTypeDef]
    ) -> _PageIterator[GetTableVersionsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetTableVersions.html#Glue.Paginator.GetTableVersions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#gettableversionspaginator)
        """

class GetTablesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetTables.html#Glue.Paginator.GetTables)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#gettablespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetTablesRequestGetTablesPaginateTypeDef]
    ) -> _PageIterator[GetTablesResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetTables.html#Glue.Paginator.GetTables.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#gettablespaginator)
        """

class GetTriggersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetTriggers.html#Glue.Paginator.GetTriggers)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#gettriggerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetTriggersRequestGetTriggersPaginateTypeDef]
    ) -> _PageIterator[GetTriggersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetTriggers.html#Glue.Paginator.GetTriggers.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#gettriggerspaginator)
        """

class GetUserDefinedFunctionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetUserDefinedFunctions.html#Glue.Paginator.GetUserDefinedFunctions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getuserdefinedfunctionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef]
    ) -> _PageIterator[GetUserDefinedFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetUserDefinedFunctions.html#Glue.Paginator.GetUserDefinedFunctions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getuserdefinedfunctionspaginator)
        """

class GetWorkflowRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetWorkflowRuns.html#Glue.Paginator.GetWorkflowRuns)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getworkflowrunspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetWorkflowRunsRequestGetWorkflowRunsPaginateTypeDef]
    ) -> _PageIterator[GetWorkflowRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/GetWorkflowRuns.html#Glue.Paginator.GetWorkflowRuns.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#getworkflowrunspaginator)
        """

class ListBlueprintsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListBlueprints.html#Glue.Paginator.ListBlueprints)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listblueprintspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBlueprintsRequestListBlueprintsPaginateTypeDef]
    ) -> _PageIterator[ListBlueprintsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListBlueprints.html#Glue.Paginator.ListBlueprints.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listblueprintspaginator)
        """

class ListConnectionTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListConnectionTypes.html#Glue.Paginator.ListConnectionTypes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listconnectiontypespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListConnectionTypesRequestListConnectionTypesPaginateTypeDef]
    ) -> _PageIterator[ListConnectionTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListConnectionTypes.html#Glue.Paginator.ListConnectionTypes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listconnectiontypespaginator)
        """

class ListEntitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListEntities.html#Glue.Paginator.ListEntities)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listentitiespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEntitiesRequestListEntitiesPaginateTypeDef]
    ) -> _PageIterator[ListEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListEntities.html#Glue.Paginator.ListEntities.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listentitiespaginator)
        """

class ListJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListJobs.html#Glue.Paginator.ListJobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> _PageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListJobs.html#Glue.Paginator.ListJobs.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listjobspaginator)
        """

class ListRegistriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListRegistries.html#Glue.Paginator.ListRegistries)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listregistriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRegistriesInputListRegistriesPaginateTypeDef]
    ) -> _PageIterator[ListRegistriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListRegistries.html#Glue.Paginator.ListRegistries.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listregistriespaginator)
        """

class ListSchemaVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListSchemaVersions.html#Glue.Paginator.ListSchemaVersions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listschemaversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSchemaVersionsInputListSchemaVersionsPaginateTypeDef]
    ) -> _PageIterator[ListSchemaVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListSchemaVersions.html#Glue.Paginator.ListSchemaVersions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listschemaversionspaginator)
        """

class ListSchemasPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListSchemas.html#Glue.Paginator.ListSchemas)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listschemaspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSchemasInputListSchemasPaginateTypeDef]
    ) -> _PageIterator[ListSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListSchemas.html#Glue.Paginator.ListSchemas.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listschemaspaginator)
        """

class ListTableOptimizerRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListTableOptimizerRuns.html#Glue.Paginator.ListTableOptimizerRuns)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listtableoptimizerrunspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTableOptimizerRunsRequestListTableOptimizerRunsPaginateTypeDef]
    ) -> _PageIterator[ListTableOptimizerRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListTableOptimizerRuns.html#Glue.Paginator.ListTableOptimizerRuns.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listtableoptimizerrunspaginator)
        """

class ListTriggersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListTriggers.html#Glue.Paginator.ListTriggers)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listtriggerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTriggersRequestListTriggersPaginateTypeDef]
    ) -> _PageIterator[ListTriggersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListTriggers.html#Glue.Paginator.ListTriggers.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listtriggerspaginator)
        """

class ListUsageProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListUsageProfiles.html#Glue.Paginator.ListUsageProfiles)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listusageprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsageProfilesRequestListUsageProfilesPaginateTypeDef]
    ) -> _PageIterator[ListUsageProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListUsageProfiles.html#Glue.Paginator.ListUsageProfiles.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listusageprofilespaginator)
        """

class ListWorkflowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListWorkflows.html#Glue.Paginator.ListWorkflows)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listworkflowspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWorkflowsRequestListWorkflowsPaginateTypeDef]
    ) -> _PageIterator[ListWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/paginator/ListWorkflows.html#Glue.Paginator.ListWorkflows.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glue/paginators/#listworkflowspaginator)
        """
