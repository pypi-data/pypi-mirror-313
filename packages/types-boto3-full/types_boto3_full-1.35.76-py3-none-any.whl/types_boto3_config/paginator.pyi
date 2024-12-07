"""
Type annotations for config service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_config.client import ConfigServiceClient
    from types_boto3_config.paginator import (
        DescribeAggregateComplianceByConfigRulesPaginator,
        DescribeAggregateComplianceByConformancePacksPaginator,
        DescribeAggregationAuthorizationsPaginator,
        DescribeComplianceByConfigRulePaginator,
        DescribeComplianceByResourcePaginator,
        DescribeConfigRuleEvaluationStatusPaginator,
        DescribeConfigRulesPaginator,
        DescribeConfigurationAggregatorSourcesStatusPaginator,
        DescribeConfigurationAggregatorsPaginator,
        DescribeConformancePackStatusPaginator,
        DescribeConformancePacksPaginator,
        DescribeOrganizationConfigRuleStatusesPaginator,
        DescribeOrganizationConfigRulesPaginator,
        DescribeOrganizationConformancePackStatusesPaginator,
        DescribeOrganizationConformancePacksPaginator,
        DescribePendingAggregationRequestsPaginator,
        DescribeRemediationExecutionStatusPaginator,
        DescribeRetentionConfigurationsPaginator,
        GetAggregateComplianceDetailsByConfigRulePaginator,
        GetComplianceDetailsByConfigRulePaginator,
        GetComplianceDetailsByResourcePaginator,
        GetConformancePackComplianceSummaryPaginator,
        GetOrganizationConfigRuleDetailedStatusPaginator,
        GetOrganizationConformancePackDetailedStatusPaginator,
        GetResourceConfigHistoryPaginator,
        ListAggregateDiscoveredResourcesPaginator,
        ListConfigurationRecordersPaginator,
        ListDiscoveredResourcesPaginator,
        ListResourceEvaluationsPaginator,
        ListTagsForResourcePaginator,
        SelectAggregateResourceConfigPaginator,
        SelectResourceConfigPaginator,
    )

    session = Session()
    client: ConfigServiceClient = session.client("config")

    describe_aggregate_compliance_by_config_rules_paginator: DescribeAggregateComplianceByConfigRulesPaginator = client.get_paginator("describe_aggregate_compliance_by_config_rules")
    describe_aggregate_compliance_by_conformance_packs_paginator: DescribeAggregateComplianceByConformancePacksPaginator = client.get_paginator("describe_aggregate_compliance_by_conformance_packs")
    describe_aggregation_authorizations_paginator: DescribeAggregationAuthorizationsPaginator = client.get_paginator("describe_aggregation_authorizations")
    describe_compliance_by_config_rule_paginator: DescribeComplianceByConfigRulePaginator = client.get_paginator("describe_compliance_by_config_rule")
    describe_compliance_by_resource_paginator: DescribeComplianceByResourcePaginator = client.get_paginator("describe_compliance_by_resource")
    describe_config_rule_evaluation_status_paginator: DescribeConfigRuleEvaluationStatusPaginator = client.get_paginator("describe_config_rule_evaluation_status")
    describe_config_rules_paginator: DescribeConfigRulesPaginator = client.get_paginator("describe_config_rules")
    describe_configuration_aggregator_sources_status_paginator: DescribeConfigurationAggregatorSourcesStatusPaginator = client.get_paginator("describe_configuration_aggregator_sources_status")
    describe_configuration_aggregators_paginator: DescribeConfigurationAggregatorsPaginator = client.get_paginator("describe_configuration_aggregators")
    describe_conformance_pack_status_paginator: DescribeConformancePackStatusPaginator = client.get_paginator("describe_conformance_pack_status")
    describe_conformance_packs_paginator: DescribeConformancePacksPaginator = client.get_paginator("describe_conformance_packs")
    describe_organization_config_rule_statuses_paginator: DescribeOrganizationConfigRuleStatusesPaginator = client.get_paginator("describe_organization_config_rule_statuses")
    describe_organization_config_rules_paginator: DescribeOrganizationConfigRulesPaginator = client.get_paginator("describe_organization_config_rules")
    describe_organization_conformance_pack_statuses_paginator: DescribeOrganizationConformancePackStatusesPaginator = client.get_paginator("describe_organization_conformance_pack_statuses")
    describe_organization_conformance_packs_paginator: DescribeOrganizationConformancePacksPaginator = client.get_paginator("describe_organization_conformance_packs")
    describe_pending_aggregation_requests_paginator: DescribePendingAggregationRequestsPaginator = client.get_paginator("describe_pending_aggregation_requests")
    describe_remediation_execution_status_paginator: DescribeRemediationExecutionStatusPaginator = client.get_paginator("describe_remediation_execution_status")
    describe_retention_configurations_paginator: DescribeRetentionConfigurationsPaginator = client.get_paginator("describe_retention_configurations")
    get_aggregate_compliance_details_by_config_rule_paginator: GetAggregateComplianceDetailsByConfigRulePaginator = client.get_paginator("get_aggregate_compliance_details_by_config_rule")
    get_compliance_details_by_config_rule_paginator: GetComplianceDetailsByConfigRulePaginator = client.get_paginator("get_compliance_details_by_config_rule")
    get_compliance_details_by_resource_paginator: GetComplianceDetailsByResourcePaginator = client.get_paginator("get_compliance_details_by_resource")
    get_conformance_pack_compliance_summary_paginator: GetConformancePackComplianceSummaryPaginator = client.get_paginator("get_conformance_pack_compliance_summary")
    get_organization_config_rule_detailed_status_paginator: GetOrganizationConfigRuleDetailedStatusPaginator = client.get_paginator("get_organization_config_rule_detailed_status")
    get_organization_conformance_pack_detailed_status_paginator: GetOrganizationConformancePackDetailedStatusPaginator = client.get_paginator("get_organization_conformance_pack_detailed_status")
    get_resource_config_history_paginator: GetResourceConfigHistoryPaginator = client.get_paginator("get_resource_config_history")
    list_aggregate_discovered_resources_paginator: ListAggregateDiscoveredResourcesPaginator = client.get_paginator("list_aggregate_discovered_resources")
    list_configuration_recorders_paginator: ListConfigurationRecordersPaginator = client.get_paginator("list_configuration_recorders")
    list_discovered_resources_paginator: ListDiscoveredResourcesPaginator = client.get_paginator("list_discovered_resources")
    list_resource_evaluations_paginator: ListResourceEvaluationsPaginator = client.get_paginator("list_resource_evaluations")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    select_aggregate_resource_config_paginator: SelectAggregateResourceConfigPaginator = client.get_paginator("select_aggregate_resource_config")
    select_resource_config_paginator: SelectResourceConfigPaginator = client.get_paginator("select_resource_config")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAggregateComplianceByConfigRulesRequestDescribeAggregateComplianceByConfigRulesPaginateTypeDef,
    DescribeAggregateComplianceByConfigRulesResponseTypeDef,
    DescribeAggregateComplianceByConformancePacksRequestDescribeAggregateComplianceByConformancePacksPaginateTypeDef,
    DescribeAggregateComplianceByConformancePacksResponseTypeDef,
    DescribeAggregationAuthorizationsRequestDescribeAggregationAuthorizationsPaginateTypeDef,
    DescribeAggregationAuthorizationsResponseTypeDef,
    DescribeComplianceByConfigRuleRequestDescribeComplianceByConfigRulePaginateTypeDef,
    DescribeComplianceByConfigRuleResponseTypeDef,
    DescribeComplianceByResourceRequestDescribeComplianceByResourcePaginateTypeDef,
    DescribeComplianceByResourceResponseTypeDef,
    DescribeConfigRuleEvaluationStatusRequestDescribeConfigRuleEvaluationStatusPaginateTypeDef,
    DescribeConfigRuleEvaluationStatusResponseTypeDef,
    DescribeConfigRulesRequestDescribeConfigRulesPaginateTypeDef,
    DescribeConfigRulesResponseTypeDef,
    DescribeConfigurationAggregatorSourcesStatusRequestDescribeConfigurationAggregatorSourcesStatusPaginateTypeDef,
    DescribeConfigurationAggregatorSourcesStatusResponseTypeDef,
    DescribeConfigurationAggregatorsRequestDescribeConfigurationAggregatorsPaginateTypeDef,
    DescribeConfigurationAggregatorsResponseTypeDef,
    DescribeConformancePacksRequestDescribeConformancePacksPaginateTypeDef,
    DescribeConformancePacksResponseTypeDef,
    DescribeConformancePackStatusRequestDescribeConformancePackStatusPaginateTypeDef,
    DescribeConformancePackStatusResponseTypeDef,
    DescribeOrganizationConfigRulesRequestDescribeOrganizationConfigRulesPaginateTypeDef,
    DescribeOrganizationConfigRulesResponseTypeDef,
    DescribeOrganizationConfigRuleStatusesRequestDescribeOrganizationConfigRuleStatusesPaginateTypeDef,
    DescribeOrganizationConfigRuleStatusesResponseTypeDef,
    DescribeOrganizationConformancePacksRequestDescribeOrganizationConformancePacksPaginateTypeDef,
    DescribeOrganizationConformancePacksResponseTypeDef,
    DescribeOrganizationConformancePackStatusesRequestDescribeOrganizationConformancePackStatusesPaginateTypeDef,
    DescribeOrganizationConformancePackStatusesResponseTypeDef,
    DescribePendingAggregationRequestsRequestDescribePendingAggregationRequestsPaginateTypeDef,
    DescribePendingAggregationRequestsResponseTypeDef,
    DescribeRemediationExecutionStatusRequestDescribeRemediationExecutionStatusPaginateTypeDef,
    DescribeRemediationExecutionStatusResponseTypeDef,
    DescribeRetentionConfigurationsRequestDescribeRetentionConfigurationsPaginateTypeDef,
    DescribeRetentionConfigurationsResponseTypeDef,
    GetAggregateComplianceDetailsByConfigRuleRequestGetAggregateComplianceDetailsByConfigRulePaginateTypeDef,
    GetAggregateComplianceDetailsByConfigRuleResponseTypeDef,
    GetComplianceDetailsByConfigRuleRequestGetComplianceDetailsByConfigRulePaginateTypeDef,
    GetComplianceDetailsByConfigRuleResponseTypeDef,
    GetComplianceDetailsByResourceRequestGetComplianceDetailsByResourcePaginateTypeDef,
    GetComplianceDetailsByResourceResponseTypeDef,
    GetConformancePackComplianceSummaryRequestGetConformancePackComplianceSummaryPaginateTypeDef,
    GetConformancePackComplianceSummaryResponseTypeDef,
    GetOrganizationConfigRuleDetailedStatusRequestGetOrganizationConfigRuleDetailedStatusPaginateTypeDef,
    GetOrganizationConfigRuleDetailedStatusResponseTypeDef,
    GetOrganizationConformancePackDetailedStatusRequestGetOrganizationConformancePackDetailedStatusPaginateTypeDef,
    GetOrganizationConformancePackDetailedStatusResponseTypeDef,
    GetResourceConfigHistoryRequestGetResourceConfigHistoryPaginateTypeDef,
    GetResourceConfigHistoryResponseTypeDef,
    ListAggregateDiscoveredResourcesRequestListAggregateDiscoveredResourcesPaginateTypeDef,
    ListAggregateDiscoveredResourcesResponseTypeDef,
    ListConfigurationRecordersRequestListConfigurationRecordersPaginateTypeDef,
    ListConfigurationRecordersResponseTypeDef,
    ListDiscoveredResourcesRequestListDiscoveredResourcesPaginateTypeDef,
    ListDiscoveredResourcesResponseTypeDef,
    ListResourceEvaluationsRequestListResourceEvaluationsPaginateTypeDef,
    ListResourceEvaluationsResponseTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    SelectAggregateResourceConfigRequestSelectAggregateResourceConfigPaginateTypeDef,
    SelectAggregateResourceConfigResponseTypeDef,
    SelectResourceConfigRequestSelectResourceConfigPaginateTypeDef,
    SelectResourceConfigResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAggregateComplianceByConfigRulesPaginator",
    "DescribeAggregateComplianceByConformancePacksPaginator",
    "DescribeAggregationAuthorizationsPaginator",
    "DescribeComplianceByConfigRulePaginator",
    "DescribeComplianceByResourcePaginator",
    "DescribeConfigRuleEvaluationStatusPaginator",
    "DescribeConfigRulesPaginator",
    "DescribeConfigurationAggregatorSourcesStatusPaginator",
    "DescribeConfigurationAggregatorsPaginator",
    "DescribeConformancePackStatusPaginator",
    "DescribeConformancePacksPaginator",
    "DescribeOrganizationConfigRuleStatusesPaginator",
    "DescribeOrganizationConfigRulesPaginator",
    "DescribeOrganizationConformancePackStatusesPaginator",
    "DescribeOrganizationConformancePacksPaginator",
    "DescribePendingAggregationRequestsPaginator",
    "DescribeRemediationExecutionStatusPaginator",
    "DescribeRetentionConfigurationsPaginator",
    "GetAggregateComplianceDetailsByConfigRulePaginator",
    "GetComplianceDetailsByConfigRulePaginator",
    "GetComplianceDetailsByResourcePaginator",
    "GetConformancePackComplianceSummaryPaginator",
    "GetOrganizationConfigRuleDetailedStatusPaginator",
    "GetOrganizationConformancePackDetailedStatusPaginator",
    "GetResourceConfigHistoryPaginator",
    "ListAggregateDiscoveredResourcesPaginator",
    "ListConfigurationRecordersPaginator",
    "ListDiscoveredResourcesPaginator",
    "ListResourceEvaluationsPaginator",
    "ListTagsForResourcePaginator",
    "SelectAggregateResourceConfigPaginator",
    "SelectResourceConfigPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAggregateComplianceByConfigRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeAggregateComplianceByConfigRules.html#ConfigService.Paginator.DescribeAggregateComplianceByConfigRules)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeaggregatecompliancebyconfigrulespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAggregateComplianceByConfigRulesRequestDescribeAggregateComplianceByConfigRulesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeAggregateComplianceByConfigRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeAggregateComplianceByConfigRules.html#ConfigService.Paginator.DescribeAggregateComplianceByConfigRules.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeaggregatecompliancebyconfigrulespaginator)
        """

class DescribeAggregateComplianceByConformancePacksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeAggregateComplianceByConformancePacks.html#ConfigService.Paginator.DescribeAggregateComplianceByConformancePacks)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeaggregatecompliancebyconformancepackspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAggregateComplianceByConformancePacksRequestDescribeAggregateComplianceByConformancePacksPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeAggregateComplianceByConformancePacksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeAggregateComplianceByConformancePacks.html#ConfigService.Paginator.DescribeAggregateComplianceByConformancePacks.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeaggregatecompliancebyconformancepackspaginator)
        """

class DescribeAggregationAuthorizationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeAggregationAuthorizations.html#ConfigService.Paginator.DescribeAggregationAuthorizations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeaggregationauthorizationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAggregationAuthorizationsRequestDescribeAggregationAuthorizationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeAggregationAuthorizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeAggregationAuthorizations.html#ConfigService.Paginator.DescribeAggregationAuthorizations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeaggregationauthorizationspaginator)
        """

class DescribeComplianceByConfigRulePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeComplianceByConfigRule.html#ConfigService.Paginator.DescribeComplianceByConfigRule)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describecompliancebyconfigrulepaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeComplianceByConfigRuleRequestDescribeComplianceByConfigRulePaginateTypeDef
        ],
    ) -> _PageIterator[DescribeComplianceByConfigRuleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeComplianceByConfigRule.html#ConfigService.Paginator.DescribeComplianceByConfigRule.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describecompliancebyconfigrulepaginator)
        """

class DescribeComplianceByResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeComplianceByResource.html#ConfigService.Paginator.DescribeComplianceByResource)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describecompliancebyresourcepaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeComplianceByResourceRequestDescribeComplianceByResourcePaginateTypeDef
        ],
    ) -> _PageIterator[DescribeComplianceByResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeComplianceByResource.html#ConfigService.Paginator.DescribeComplianceByResource.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describecompliancebyresourcepaginator)
        """

class DescribeConfigRuleEvaluationStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeConfigRuleEvaluationStatus.html#ConfigService.Paginator.DescribeConfigRuleEvaluationStatus)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeconfigruleevaluationstatuspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeConfigRuleEvaluationStatusRequestDescribeConfigRuleEvaluationStatusPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeConfigRuleEvaluationStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeConfigRuleEvaluationStatus.html#ConfigService.Paginator.DescribeConfigRuleEvaluationStatus.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeconfigruleevaluationstatuspaginator)
        """

class DescribeConfigRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeConfigRules.html#ConfigService.Paginator.DescribeConfigRules)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeconfigrulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeConfigRulesRequestDescribeConfigRulesPaginateTypeDef]
    ) -> _PageIterator[DescribeConfigRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeConfigRules.html#ConfigService.Paginator.DescribeConfigRules.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeconfigrulespaginator)
        """

class DescribeConfigurationAggregatorSourcesStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeConfigurationAggregatorSourcesStatus.html#ConfigService.Paginator.DescribeConfigurationAggregatorSourcesStatus)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeconfigurationaggregatorsourcesstatuspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeConfigurationAggregatorSourcesStatusRequestDescribeConfigurationAggregatorSourcesStatusPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeConfigurationAggregatorSourcesStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeConfigurationAggregatorSourcesStatus.html#ConfigService.Paginator.DescribeConfigurationAggregatorSourcesStatus.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeconfigurationaggregatorsourcesstatuspaginator)
        """

class DescribeConfigurationAggregatorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeConfigurationAggregators.html#ConfigService.Paginator.DescribeConfigurationAggregators)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeconfigurationaggregatorspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeConfigurationAggregatorsRequestDescribeConfigurationAggregatorsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeConfigurationAggregatorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeConfigurationAggregators.html#ConfigService.Paginator.DescribeConfigurationAggregators.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeconfigurationaggregatorspaginator)
        """

class DescribeConformancePackStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeConformancePackStatus.html#ConfigService.Paginator.DescribeConformancePackStatus)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeconformancepackstatuspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeConformancePackStatusRequestDescribeConformancePackStatusPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeConformancePackStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeConformancePackStatus.html#ConfigService.Paginator.DescribeConformancePackStatus.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeconformancepackstatuspaginator)
        """

class DescribeConformancePacksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeConformancePacks.html#ConfigService.Paginator.DescribeConformancePacks)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeconformancepackspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeConformancePacksRequestDescribeConformancePacksPaginateTypeDef],
    ) -> _PageIterator[DescribeConformancePacksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeConformancePacks.html#ConfigService.Paginator.DescribeConformancePacks.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeconformancepackspaginator)
        """

class DescribeOrganizationConfigRuleStatusesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeOrganizationConfigRuleStatuses.html#ConfigService.Paginator.DescribeOrganizationConfigRuleStatuses)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeorganizationconfigrulestatusespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeOrganizationConfigRuleStatusesRequestDescribeOrganizationConfigRuleStatusesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeOrganizationConfigRuleStatusesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeOrganizationConfigRuleStatuses.html#ConfigService.Paginator.DescribeOrganizationConfigRuleStatuses.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeorganizationconfigrulestatusespaginator)
        """

class DescribeOrganizationConfigRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeOrganizationConfigRules.html#ConfigService.Paginator.DescribeOrganizationConfigRules)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeorganizationconfigrulespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeOrganizationConfigRulesRequestDescribeOrganizationConfigRulesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeOrganizationConfigRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeOrganizationConfigRules.html#ConfigService.Paginator.DescribeOrganizationConfigRules.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeorganizationconfigrulespaginator)
        """

class DescribeOrganizationConformancePackStatusesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeOrganizationConformancePackStatuses.html#ConfigService.Paginator.DescribeOrganizationConformancePackStatuses)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeorganizationconformancepackstatusespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeOrganizationConformancePackStatusesRequestDescribeOrganizationConformancePackStatusesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeOrganizationConformancePackStatusesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeOrganizationConformancePackStatuses.html#ConfigService.Paginator.DescribeOrganizationConformancePackStatuses.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeorganizationconformancepackstatusespaginator)
        """

class DescribeOrganizationConformancePacksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeOrganizationConformancePacks.html#ConfigService.Paginator.DescribeOrganizationConformancePacks)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeorganizationconformancepackspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeOrganizationConformancePacksRequestDescribeOrganizationConformancePacksPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeOrganizationConformancePacksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeOrganizationConformancePacks.html#ConfigService.Paginator.DescribeOrganizationConformancePacks.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeorganizationconformancepackspaginator)
        """

class DescribePendingAggregationRequestsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribePendingAggregationRequests.html#ConfigService.Paginator.DescribePendingAggregationRequests)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describependingaggregationrequestspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribePendingAggregationRequestsRequestDescribePendingAggregationRequestsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribePendingAggregationRequestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribePendingAggregationRequests.html#ConfigService.Paginator.DescribePendingAggregationRequests.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describependingaggregationrequestspaginator)
        """

class DescribeRemediationExecutionStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeRemediationExecutionStatus.html#ConfigService.Paginator.DescribeRemediationExecutionStatus)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeremediationexecutionstatuspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeRemediationExecutionStatusRequestDescribeRemediationExecutionStatusPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeRemediationExecutionStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeRemediationExecutionStatus.html#ConfigService.Paginator.DescribeRemediationExecutionStatus.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeremediationexecutionstatuspaginator)
        """

class DescribeRetentionConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeRetentionConfigurations.html#ConfigService.Paginator.DescribeRetentionConfigurations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeretentionconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeRetentionConfigurationsRequestDescribeRetentionConfigurationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeRetentionConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/DescribeRetentionConfigurations.html#ConfigService.Paginator.DescribeRetentionConfigurations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#describeretentionconfigurationspaginator)
        """

class GetAggregateComplianceDetailsByConfigRulePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetAggregateComplianceDetailsByConfigRule.html#ConfigService.Paginator.GetAggregateComplianceDetailsByConfigRule)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getaggregatecompliancedetailsbyconfigrulepaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetAggregateComplianceDetailsByConfigRuleRequestGetAggregateComplianceDetailsByConfigRulePaginateTypeDef
        ],
    ) -> _PageIterator[GetAggregateComplianceDetailsByConfigRuleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetAggregateComplianceDetailsByConfigRule.html#ConfigService.Paginator.GetAggregateComplianceDetailsByConfigRule.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getaggregatecompliancedetailsbyconfigrulepaginator)
        """

class GetComplianceDetailsByConfigRulePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetComplianceDetailsByConfigRule.html#ConfigService.Paginator.GetComplianceDetailsByConfigRule)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getcompliancedetailsbyconfigrulepaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetComplianceDetailsByConfigRuleRequestGetComplianceDetailsByConfigRulePaginateTypeDef
        ],
    ) -> _PageIterator[GetComplianceDetailsByConfigRuleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetComplianceDetailsByConfigRule.html#ConfigService.Paginator.GetComplianceDetailsByConfigRule.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getcompliancedetailsbyconfigrulepaginator)
        """

class GetComplianceDetailsByResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetComplianceDetailsByResource.html#ConfigService.Paginator.GetComplianceDetailsByResource)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getcompliancedetailsbyresourcepaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetComplianceDetailsByResourceRequestGetComplianceDetailsByResourcePaginateTypeDef
        ],
    ) -> _PageIterator[GetComplianceDetailsByResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetComplianceDetailsByResource.html#ConfigService.Paginator.GetComplianceDetailsByResource.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getcompliancedetailsbyresourcepaginator)
        """

class GetConformancePackComplianceSummaryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetConformancePackComplianceSummary.html#ConfigService.Paginator.GetConformancePackComplianceSummary)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getconformancepackcompliancesummarypaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetConformancePackComplianceSummaryRequestGetConformancePackComplianceSummaryPaginateTypeDef
        ],
    ) -> _PageIterator[GetConformancePackComplianceSummaryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetConformancePackComplianceSummary.html#ConfigService.Paginator.GetConformancePackComplianceSummary.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getconformancepackcompliancesummarypaginator)
        """

class GetOrganizationConfigRuleDetailedStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetOrganizationConfigRuleDetailedStatus.html#ConfigService.Paginator.GetOrganizationConfigRuleDetailedStatus)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getorganizationconfigruledetailedstatuspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetOrganizationConfigRuleDetailedStatusRequestGetOrganizationConfigRuleDetailedStatusPaginateTypeDef
        ],
    ) -> _PageIterator[GetOrganizationConfigRuleDetailedStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetOrganizationConfigRuleDetailedStatus.html#ConfigService.Paginator.GetOrganizationConfigRuleDetailedStatus.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getorganizationconfigruledetailedstatuspaginator)
        """

class GetOrganizationConformancePackDetailedStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetOrganizationConformancePackDetailedStatus.html#ConfigService.Paginator.GetOrganizationConformancePackDetailedStatus)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getorganizationconformancepackdetailedstatuspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetOrganizationConformancePackDetailedStatusRequestGetOrganizationConformancePackDetailedStatusPaginateTypeDef
        ],
    ) -> _PageIterator[GetOrganizationConformancePackDetailedStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetOrganizationConformancePackDetailedStatus.html#ConfigService.Paginator.GetOrganizationConformancePackDetailedStatus.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getorganizationconformancepackdetailedstatuspaginator)
        """

class GetResourceConfigHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetResourceConfigHistory.html#ConfigService.Paginator.GetResourceConfigHistory)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getresourceconfighistorypaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[GetResourceConfigHistoryRequestGetResourceConfigHistoryPaginateTypeDef],
    ) -> _PageIterator[GetResourceConfigHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/GetResourceConfigHistory.html#ConfigService.Paginator.GetResourceConfigHistory.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#getresourceconfighistorypaginator)
        """

class ListAggregateDiscoveredResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/ListAggregateDiscoveredResources.html#ConfigService.Paginator.ListAggregateDiscoveredResources)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#listaggregatediscoveredresourcespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAggregateDiscoveredResourcesRequestListAggregateDiscoveredResourcesPaginateTypeDef
        ],
    ) -> _PageIterator[ListAggregateDiscoveredResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/ListAggregateDiscoveredResources.html#ConfigService.Paginator.ListAggregateDiscoveredResources.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#listaggregatediscoveredresourcespaginator)
        """

class ListConfigurationRecordersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/ListConfigurationRecorders.html#ConfigService.Paginator.ListConfigurationRecorders)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#listconfigurationrecorderspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListConfigurationRecordersRequestListConfigurationRecordersPaginateTypeDef
        ],
    ) -> _PageIterator[ListConfigurationRecordersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/ListConfigurationRecorders.html#ConfigService.Paginator.ListConfigurationRecorders.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#listconfigurationrecorderspaginator)
        """

class ListDiscoveredResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/ListDiscoveredResources.html#ConfigService.Paginator.ListDiscoveredResources)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#listdiscoveredresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDiscoveredResourcesRequestListDiscoveredResourcesPaginateTypeDef]
    ) -> _PageIterator[ListDiscoveredResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/ListDiscoveredResources.html#ConfigService.Paginator.ListDiscoveredResources.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#listdiscoveredresourcespaginator)
        """

class ListResourceEvaluationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/ListResourceEvaluations.html#ConfigService.Paginator.ListResourceEvaluations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#listresourceevaluationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResourceEvaluationsRequestListResourceEvaluationsPaginateTypeDef]
    ) -> _PageIterator[ListResourceEvaluationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/ListResourceEvaluations.html#ConfigService.Paginator.ListResourceEvaluations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#listresourceevaluationspaginator)
        """

class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/ListTagsForResource.html#ConfigService.Paginator.ListTagsForResource)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/ListTagsForResource.html#ConfigService.Paginator.ListTagsForResource.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#listtagsforresourcepaginator)
        """

class SelectAggregateResourceConfigPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/SelectAggregateResourceConfig.html#ConfigService.Paginator.SelectAggregateResourceConfig)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#selectaggregateresourceconfigpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            SelectAggregateResourceConfigRequestSelectAggregateResourceConfigPaginateTypeDef
        ],
    ) -> _PageIterator[SelectAggregateResourceConfigResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/SelectAggregateResourceConfig.html#ConfigService.Paginator.SelectAggregateResourceConfig.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#selectaggregateresourceconfigpaginator)
        """

class SelectResourceConfigPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/SelectResourceConfig.html#ConfigService.Paginator.SelectResourceConfig)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#selectresourceconfigpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SelectResourceConfigRequestSelectResourceConfigPaginateTypeDef]
    ) -> _PageIterator[SelectResourceConfigResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/paginator/SelectResourceConfig.html#ConfigService.Paginator.SelectResourceConfig.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_config/paginators/#selectresourceconfigpaginator)
        """
