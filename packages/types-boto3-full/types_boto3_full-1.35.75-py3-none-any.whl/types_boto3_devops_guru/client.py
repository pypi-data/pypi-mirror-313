"""
Type annotations for devops-guru service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_devops_guru.client import DevOpsGuruClient

    session = Session()
    client: DevOpsGuruClient = session.client("devops-guru")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeOrganizationResourceCollectionHealthPaginator,
    DescribeResourceCollectionHealthPaginator,
    GetCostEstimationPaginator,
    GetResourceCollectionPaginator,
    ListAnomaliesForInsightPaginator,
    ListAnomalousLogGroupsPaginator,
    ListEventsPaginator,
    ListInsightsPaginator,
    ListMonitoredResourcesPaginator,
    ListNotificationChannelsPaginator,
    ListOrganizationInsightsPaginator,
    ListRecommendationsPaginator,
    SearchInsightsPaginator,
    SearchOrganizationInsightsPaginator,
)
from .type_defs import (
    AddNotificationChannelRequestRequestTypeDef,
    AddNotificationChannelResponseTypeDef,
    DeleteInsightRequestRequestTypeDef,
    DescribeAccountHealthResponseTypeDef,
    DescribeAccountOverviewRequestRequestTypeDef,
    DescribeAccountOverviewResponseTypeDef,
    DescribeAnomalyRequestRequestTypeDef,
    DescribeAnomalyResponseTypeDef,
    DescribeEventSourcesConfigResponseTypeDef,
    DescribeFeedbackRequestRequestTypeDef,
    DescribeFeedbackResponseTypeDef,
    DescribeInsightRequestRequestTypeDef,
    DescribeInsightResponseTypeDef,
    DescribeOrganizationHealthRequestRequestTypeDef,
    DescribeOrganizationHealthResponseTypeDef,
    DescribeOrganizationOverviewRequestRequestTypeDef,
    DescribeOrganizationOverviewResponseTypeDef,
    DescribeOrganizationResourceCollectionHealthRequestRequestTypeDef,
    DescribeOrganizationResourceCollectionHealthResponseTypeDef,
    DescribeResourceCollectionHealthRequestRequestTypeDef,
    DescribeResourceCollectionHealthResponseTypeDef,
    DescribeServiceIntegrationResponseTypeDef,
    GetCostEstimationRequestRequestTypeDef,
    GetCostEstimationResponseTypeDef,
    GetResourceCollectionRequestRequestTypeDef,
    GetResourceCollectionResponseTypeDef,
    ListAnomaliesForInsightRequestRequestTypeDef,
    ListAnomaliesForInsightResponseTypeDef,
    ListAnomalousLogGroupsRequestRequestTypeDef,
    ListAnomalousLogGroupsResponseTypeDef,
    ListEventsRequestRequestTypeDef,
    ListEventsResponseTypeDef,
    ListInsightsRequestRequestTypeDef,
    ListInsightsResponseTypeDef,
    ListMonitoredResourcesRequestRequestTypeDef,
    ListMonitoredResourcesResponseTypeDef,
    ListNotificationChannelsRequestRequestTypeDef,
    ListNotificationChannelsResponseTypeDef,
    ListOrganizationInsightsRequestRequestTypeDef,
    ListOrganizationInsightsResponseTypeDef,
    ListRecommendationsRequestRequestTypeDef,
    ListRecommendationsResponseTypeDef,
    PutFeedbackRequestRequestTypeDef,
    RemoveNotificationChannelRequestRequestTypeDef,
    SearchInsightsRequestRequestTypeDef,
    SearchInsightsResponseTypeDef,
    SearchOrganizationInsightsRequestRequestTypeDef,
    SearchOrganizationInsightsResponseTypeDef,
    StartCostEstimationRequestRequestTypeDef,
    UpdateEventSourcesConfigRequestRequestTypeDef,
    UpdateResourceCollectionRequestRequestTypeDef,
    UpdateServiceIntegrationRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("DevOpsGuruClient",)


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


class DevOpsGuruClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DevOpsGuruClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#close)
        """

    def add_notification_channel(
        self, **kwargs: Unpack[AddNotificationChannelRequestRequestTypeDef]
    ) -> AddNotificationChannelResponseTypeDef:
        """
        Adds a notification channel to DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/add_notification_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#add_notification_channel)
        """

    def delete_insight(
        self, **kwargs: Unpack[DeleteInsightRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the insight along with the associated anomalies, events and
        recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/delete_insight.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#delete_insight)
        """

    def describe_account_health(self) -> DescribeAccountHealthResponseTypeDef:
        """
        Returns the number of open reactive insights, the number of open proactive
        insights, and the number of metrics analyzed in your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/describe_account_health.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#describe_account_health)
        """

    def describe_account_overview(
        self, **kwargs: Unpack[DescribeAccountOverviewRequestRequestTypeDef]
    ) -> DescribeAccountOverviewResponseTypeDef:
        """
        For the time range passed in, returns the number of open reactive insight that
        were created, the number of open proactive insights that were created, and the
        Mean Time to Recover (MTTR) for all closed reactive insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/describe_account_overview.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#describe_account_overview)
        """

    def describe_anomaly(
        self, **kwargs: Unpack[DescribeAnomalyRequestRequestTypeDef]
    ) -> DescribeAnomalyResponseTypeDef:
        """
        Returns details about an anomaly that you specify using its ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/describe_anomaly.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#describe_anomaly)
        """

    def describe_event_sources_config(self) -> DescribeEventSourcesConfigResponseTypeDef:
        """
        Returns the integration status of services that are integrated with DevOps Guru
        as Consumer via EventBridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/describe_event_sources_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#describe_event_sources_config)
        """

    def describe_feedback(
        self, **kwargs: Unpack[DescribeFeedbackRequestRequestTypeDef]
    ) -> DescribeFeedbackResponseTypeDef:
        """
        Returns the most recent feedback submitted in the current Amazon Web Services
        account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/describe_feedback.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#describe_feedback)
        """

    def describe_insight(
        self, **kwargs: Unpack[DescribeInsightRequestRequestTypeDef]
    ) -> DescribeInsightResponseTypeDef:
        """
        Returns details about an insight that you specify using its ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/describe_insight.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#describe_insight)
        """

    def describe_organization_health(
        self, **kwargs: Unpack[DescribeOrganizationHealthRequestRequestTypeDef]
    ) -> DescribeOrganizationHealthResponseTypeDef:
        """
        Returns active insights, predictive insights, and resource hours analyzed in
        last hour.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/describe_organization_health.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#describe_organization_health)
        """

    def describe_organization_overview(
        self, **kwargs: Unpack[DescribeOrganizationOverviewRequestRequestTypeDef]
    ) -> DescribeOrganizationOverviewResponseTypeDef:
        """
        Returns an overview of your organization's history based on the specified time
        range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/describe_organization_overview.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#describe_organization_overview)
        """

    def describe_organization_resource_collection_health(
        self, **kwargs: Unpack[DescribeOrganizationResourceCollectionHealthRequestRequestTypeDef]
    ) -> DescribeOrganizationResourceCollectionHealthResponseTypeDef:
        """
        Provides an overview of your system's health.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/describe_organization_resource_collection_health.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#describe_organization_resource_collection_health)
        """

    def describe_resource_collection_health(
        self, **kwargs: Unpack[DescribeResourceCollectionHealthRequestRequestTypeDef]
    ) -> DescribeResourceCollectionHealthResponseTypeDef:
        """
        Returns the number of open proactive insights, open reactive insights, and the
        Mean Time to Recover (MTTR) for all closed insights in resource collections in
        your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/describe_resource_collection_health.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#describe_resource_collection_health)
        """

    def describe_service_integration(self) -> DescribeServiceIntegrationResponseTypeDef:
        """
        Returns the integration status of services that are integrated with DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/describe_service_integration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#describe_service_integration)
        """

    def get_cost_estimation(
        self, **kwargs: Unpack[GetCostEstimationRequestRequestTypeDef]
    ) -> GetCostEstimationResponseTypeDef:
        """
        Returns an estimate of the monthly cost for DevOps Guru to analyze your Amazon
        Web Services resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_cost_estimation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_cost_estimation)
        """

    def get_resource_collection(
        self, **kwargs: Unpack[GetResourceCollectionRequestRequestTypeDef]
    ) -> GetResourceCollectionResponseTypeDef:
        """
        Returns lists Amazon Web Services resources that are of the specified resource
        collection type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_resource_collection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_resource_collection)
        """

    def list_anomalies_for_insight(
        self, **kwargs: Unpack[ListAnomaliesForInsightRequestRequestTypeDef]
    ) -> ListAnomaliesForInsightResponseTypeDef:
        """
        Returns a list of the anomalies that belong to an insight that you specify
        using its ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/list_anomalies_for_insight.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#list_anomalies_for_insight)
        """

    def list_anomalous_log_groups(
        self, **kwargs: Unpack[ListAnomalousLogGroupsRequestRequestTypeDef]
    ) -> ListAnomalousLogGroupsResponseTypeDef:
        """
        Returns the list of log groups that contain log anomalies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/list_anomalous_log_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#list_anomalous_log_groups)
        """

    def list_events(
        self, **kwargs: Unpack[ListEventsRequestRequestTypeDef]
    ) -> ListEventsResponseTypeDef:
        """
        Returns a list of the events emitted by the resources that are evaluated by
        DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/list_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#list_events)
        """

    def list_insights(
        self, **kwargs: Unpack[ListInsightsRequestRequestTypeDef]
    ) -> ListInsightsResponseTypeDef:
        """
        Returns a list of insights in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/list_insights.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#list_insights)
        """

    def list_monitored_resources(
        self, **kwargs: Unpack[ListMonitoredResourcesRequestRequestTypeDef]
    ) -> ListMonitoredResourcesResponseTypeDef:
        """
        Returns the list of all log groups that are being monitored and tagged by
        DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/list_monitored_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#list_monitored_resources)
        """

    def list_notification_channels(
        self, **kwargs: Unpack[ListNotificationChannelsRequestRequestTypeDef]
    ) -> ListNotificationChannelsResponseTypeDef:
        """
        Returns a list of notification channels configured for DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/list_notification_channels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#list_notification_channels)
        """

    def list_organization_insights(
        self, **kwargs: Unpack[ListOrganizationInsightsRequestRequestTypeDef]
    ) -> ListOrganizationInsightsResponseTypeDef:
        """
        Returns a list of insights associated with the account or OU Id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/list_organization_insights.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#list_organization_insights)
        """

    def list_recommendations(
        self, **kwargs: Unpack[ListRecommendationsRequestRequestTypeDef]
    ) -> ListRecommendationsResponseTypeDef:
        """
        Returns a list of a specified insight's recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/list_recommendations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#list_recommendations)
        """

    def put_feedback(self, **kwargs: Unpack[PutFeedbackRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Collects customer feedback about the specified insight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/put_feedback.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#put_feedback)
        """

    def remove_notification_channel(
        self, **kwargs: Unpack[RemoveNotificationChannelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a notification channel from DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/remove_notification_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#remove_notification_channel)
        """

    def search_insights(
        self, **kwargs: Unpack[SearchInsightsRequestRequestTypeDef]
    ) -> SearchInsightsResponseTypeDef:
        """
        Returns a list of insights in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/search_insights.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#search_insights)
        """

    def search_organization_insights(
        self, **kwargs: Unpack[SearchOrganizationInsightsRequestRequestTypeDef]
    ) -> SearchOrganizationInsightsResponseTypeDef:
        """
        Returns a list of insights in your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/search_organization_insights.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#search_organization_insights)
        """

    def start_cost_estimation(
        self, **kwargs: Unpack[StartCostEstimationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts the creation of an estimate of the monthly cost to analyze your Amazon
        Web Services resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/start_cost_estimation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#start_cost_estimation)
        """

    def update_event_sources_config(
        self, **kwargs: Unpack[UpdateEventSourcesConfigRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enables or disables integration with a service that can be integrated with
        DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/update_event_sources_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#update_event_sources_config)
        """

    def update_resource_collection(
        self, **kwargs: Unpack[UpdateResourceCollectionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the collection of resources that DevOps Guru analyzes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/update_resource_collection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#update_resource_collection)
        """

    def update_service_integration(
        self, **kwargs: Unpack[UpdateServiceIntegrationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enables or disables integration with a service that can be integrated with
        DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/update_service_integration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#update_service_integration)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_organization_resource_collection_health"]
    ) -> DescribeOrganizationResourceCollectionHealthPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_resource_collection_health"]
    ) -> DescribeResourceCollectionHealthPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_cost_estimation"]
    ) -> GetCostEstimationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_collection"]
    ) -> GetResourceCollectionPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_anomalies_for_insight"]
    ) -> ListAnomaliesForInsightPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_anomalous_log_groups"]
    ) -> ListAnomalousLogGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_events"]) -> ListEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_insights"]) -> ListInsightsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_monitored_resources"]
    ) -> ListMonitoredResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_notification_channels"]
    ) -> ListNotificationChannelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_organization_insights"]
    ) -> ListOrganizationInsightsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recommendations"]
    ) -> ListRecommendationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_insights"]) -> SearchInsightsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_organization_insights"]
    ) -> SearchOrganizationInsightsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_guru/client/#get_paginator)
        """
