"""
Type annotations for logs service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_logs.client import CloudWatchLogsClient

    session = Session()
    client: CloudWatchLogsClient = session.client("logs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeConfigurationTemplatesPaginator,
    DescribeDeliveriesPaginator,
    DescribeDeliveryDestinationsPaginator,
    DescribeDeliverySourcesPaginator,
    DescribeDestinationsPaginator,
    DescribeExportTasksPaginator,
    DescribeLogGroupsPaginator,
    DescribeLogStreamsPaginator,
    DescribeMetricFiltersPaginator,
    DescribeQueriesPaginator,
    DescribeResourcePoliciesPaginator,
    DescribeSubscriptionFiltersPaginator,
    FilterLogEventsPaginator,
    ListAnomaliesPaginator,
    ListLogAnomalyDetectorsPaginator,
    ListLogGroupsForQueryPaginator,
)
from .type_defs import (
    AssociateKmsKeyRequestRequestTypeDef,
    CancelExportTaskRequestRequestTypeDef,
    CreateDeliveryRequestRequestTypeDef,
    CreateDeliveryResponseTypeDef,
    CreateExportTaskRequestRequestTypeDef,
    CreateExportTaskResponseTypeDef,
    CreateLogAnomalyDetectorRequestRequestTypeDef,
    CreateLogAnomalyDetectorResponseTypeDef,
    CreateLogGroupRequestRequestTypeDef,
    CreateLogStreamRequestRequestTypeDef,
    DeleteAccountPolicyRequestRequestTypeDef,
    DeleteDataProtectionPolicyRequestRequestTypeDef,
    DeleteDeliveryDestinationPolicyRequestRequestTypeDef,
    DeleteDeliveryDestinationRequestRequestTypeDef,
    DeleteDeliveryRequestRequestTypeDef,
    DeleteDeliverySourceRequestRequestTypeDef,
    DeleteDestinationRequestRequestTypeDef,
    DeleteIndexPolicyRequestRequestTypeDef,
    DeleteIntegrationRequestRequestTypeDef,
    DeleteLogAnomalyDetectorRequestRequestTypeDef,
    DeleteLogGroupRequestRequestTypeDef,
    DeleteLogStreamRequestRequestTypeDef,
    DeleteMetricFilterRequestRequestTypeDef,
    DeleteQueryDefinitionRequestRequestTypeDef,
    DeleteQueryDefinitionResponseTypeDef,
    DeleteResourcePolicyRequestRequestTypeDef,
    DeleteRetentionPolicyRequestRequestTypeDef,
    DeleteSubscriptionFilterRequestRequestTypeDef,
    DeleteTransformerRequestRequestTypeDef,
    DescribeAccountPoliciesRequestRequestTypeDef,
    DescribeAccountPoliciesResponseTypeDef,
    DescribeConfigurationTemplatesRequestRequestTypeDef,
    DescribeConfigurationTemplatesResponseTypeDef,
    DescribeDeliveriesRequestRequestTypeDef,
    DescribeDeliveriesResponseTypeDef,
    DescribeDeliveryDestinationsRequestRequestTypeDef,
    DescribeDeliveryDestinationsResponseTypeDef,
    DescribeDeliverySourcesRequestRequestTypeDef,
    DescribeDeliverySourcesResponseTypeDef,
    DescribeDestinationsRequestRequestTypeDef,
    DescribeDestinationsResponseTypeDef,
    DescribeExportTasksRequestRequestTypeDef,
    DescribeExportTasksResponseTypeDef,
    DescribeFieldIndexesRequestRequestTypeDef,
    DescribeFieldIndexesResponseTypeDef,
    DescribeIndexPoliciesRequestRequestTypeDef,
    DescribeIndexPoliciesResponseTypeDef,
    DescribeLogGroupsRequestRequestTypeDef,
    DescribeLogGroupsResponseTypeDef,
    DescribeLogStreamsRequestRequestTypeDef,
    DescribeLogStreamsResponseTypeDef,
    DescribeMetricFiltersRequestRequestTypeDef,
    DescribeMetricFiltersResponseTypeDef,
    DescribeQueriesRequestRequestTypeDef,
    DescribeQueriesResponseTypeDef,
    DescribeQueryDefinitionsRequestRequestTypeDef,
    DescribeQueryDefinitionsResponseTypeDef,
    DescribeResourcePoliciesRequestRequestTypeDef,
    DescribeResourcePoliciesResponseTypeDef,
    DescribeSubscriptionFiltersRequestRequestTypeDef,
    DescribeSubscriptionFiltersResponseTypeDef,
    DisassociateKmsKeyRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    FilterLogEventsRequestRequestTypeDef,
    FilterLogEventsResponseTypeDef,
    GetDataProtectionPolicyRequestRequestTypeDef,
    GetDataProtectionPolicyResponseTypeDef,
    GetDeliveryDestinationPolicyRequestRequestTypeDef,
    GetDeliveryDestinationPolicyResponseTypeDef,
    GetDeliveryDestinationRequestRequestTypeDef,
    GetDeliveryDestinationResponseTypeDef,
    GetDeliveryRequestRequestTypeDef,
    GetDeliveryResponseTypeDef,
    GetDeliverySourceRequestRequestTypeDef,
    GetDeliverySourceResponseTypeDef,
    GetIntegrationRequestRequestTypeDef,
    GetIntegrationResponseTypeDef,
    GetLogAnomalyDetectorRequestRequestTypeDef,
    GetLogAnomalyDetectorResponseTypeDef,
    GetLogEventsRequestRequestTypeDef,
    GetLogEventsResponseTypeDef,
    GetLogGroupFieldsRequestRequestTypeDef,
    GetLogGroupFieldsResponseTypeDef,
    GetLogRecordRequestRequestTypeDef,
    GetLogRecordResponseTypeDef,
    GetQueryResultsRequestRequestTypeDef,
    GetQueryResultsResponseTypeDef,
    GetTransformerRequestRequestTypeDef,
    GetTransformerResponseTypeDef,
    ListAnomaliesRequestRequestTypeDef,
    ListAnomaliesResponseTypeDef,
    ListIntegrationsRequestRequestTypeDef,
    ListIntegrationsResponseTypeDef,
    ListLogAnomalyDetectorsRequestRequestTypeDef,
    ListLogAnomalyDetectorsResponseTypeDef,
    ListLogGroupsForQueryRequestRequestTypeDef,
    ListLogGroupsForQueryResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTagsLogGroupRequestRequestTypeDef,
    ListTagsLogGroupResponseTypeDef,
    PutAccountPolicyRequestRequestTypeDef,
    PutAccountPolicyResponseTypeDef,
    PutDataProtectionPolicyRequestRequestTypeDef,
    PutDataProtectionPolicyResponseTypeDef,
    PutDeliveryDestinationPolicyRequestRequestTypeDef,
    PutDeliveryDestinationPolicyResponseTypeDef,
    PutDeliveryDestinationRequestRequestTypeDef,
    PutDeliveryDestinationResponseTypeDef,
    PutDeliverySourceRequestRequestTypeDef,
    PutDeliverySourceResponseTypeDef,
    PutDestinationPolicyRequestRequestTypeDef,
    PutDestinationRequestRequestTypeDef,
    PutDestinationResponseTypeDef,
    PutIndexPolicyRequestRequestTypeDef,
    PutIndexPolicyResponseTypeDef,
    PutIntegrationRequestRequestTypeDef,
    PutIntegrationResponseTypeDef,
    PutLogEventsRequestRequestTypeDef,
    PutLogEventsResponseTypeDef,
    PutMetricFilterRequestRequestTypeDef,
    PutQueryDefinitionRequestRequestTypeDef,
    PutQueryDefinitionResponseTypeDef,
    PutResourcePolicyRequestRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    PutRetentionPolicyRequestRequestTypeDef,
    PutSubscriptionFilterRequestRequestTypeDef,
    PutTransformerRequestRequestTypeDef,
    StartLiveTailRequestRequestTypeDef,
    StartLiveTailResponseTypeDef,
    StartQueryRequestRequestTypeDef,
    StartQueryResponseTypeDef,
    StopQueryRequestRequestTypeDef,
    StopQueryResponseTypeDef,
    TagLogGroupRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    TestMetricFilterRequestRequestTypeDef,
    TestMetricFilterResponseTypeDef,
    TestTransformerRequestRequestTypeDef,
    TestTransformerResponseTypeDef,
    UntagLogGroupRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAnomalyRequestRequestTypeDef,
    UpdateDeliveryConfigurationRequestRequestTypeDef,
    UpdateLogAnomalyDetectorRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("CloudWatchLogsClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DataAlreadyAcceptedException: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidSequenceTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedQueryException: Type[BotocoreClientError]
    OperationAbortedException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    SessionStreamingException: Type[BotocoreClientError]
    SessionTimeoutException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnrecognizedClientException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CloudWatchLogsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchLogsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#close)
        """

    def associate_kms_key(
        self, **kwargs: Unpack[AssociateKmsKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates the specified KMS key with either one log group in the account, or
        with all stored CloudWatch Logs query insights results in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/associate_kms_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#associate_kms_key)
        """

    def cancel_export_task(
        self, **kwargs: Unpack[CancelExportTaskRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels the specified export task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/cancel_export_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#cancel_export_task)
        """

    def create_delivery(
        self, **kwargs: Unpack[CreateDeliveryRequestRequestTypeDef]
    ) -> CreateDeliveryResponseTypeDef:
        """
        Creates a <i>delivery</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_delivery.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#create_delivery)
        """

    def create_export_task(
        self, **kwargs: Unpack[CreateExportTaskRequestRequestTypeDef]
    ) -> CreateExportTaskResponseTypeDef:
        """
        Creates an export task so that you can efficiently export data from a log group
        to an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_export_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#create_export_task)
        """

    def create_log_anomaly_detector(
        self, **kwargs: Unpack[CreateLogAnomalyDetectorRequestRequestTypeDef]
    ) -> CreateLogAnomalyDetectorResponseTypeDef:
        """
        Creates an <i>anomaly detector</i> that regularly scans one or more log groups
        and look for patterns and anomalies in the logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_log_anomaly_detector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#create_log_anomaly_detector)
        """

    def create_log_group(
        self, **kwargs: Unpack[CreateLogGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a log group with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_log_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#create_log_group)
        """

    def create_log_stream(
        self, **kwargs: Unpack[CreateLogStreamRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a log stream for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_log_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#create_log_stream)
        """

    def delete_account_policy(
        self, **kwargs: Unpack[DeleteAccountPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a CloudWatch Logs account policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_account_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_account_policy)
        """

    def delete_data_protection_policy(
        self, **kwargs: Unpack[DeleteDataProtectionPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the data protection policy from the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_data_protection_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_data_protection_policy)
        """

    def delete_delivery(
        self, **kwargs: Unpack[DeleteDeliveryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes s <i>delivery</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_delivery.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_delivery)
        """

    def delete_delivery_destination(
        self, **kwargs: Unpack[DeleteDeliveryDestinationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a <i>delivery destination</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_delivery_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_delivery_destination)
        """

    def delete_delivery_destination_policy(
        self, **kwargs: Unpack[DeleteDeliveryDestinationPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a delivery destination policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_delivery_destination_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_delivery_destination_policy)
        """

    def delete_delivery_source(
        self, **kwargs: Unpack[DeleteDeliverySourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a <i>delivery source</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_delivery_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_delivery_source)
        """

    def delete_destination(
        self, **kwargs: Unpack[DeleteDestinationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified destination, and eventually disables all the subscription
        filters that publish to it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_destination)
        """

    def delete_index_policy(
        self, **kwargs: Unpack[DeleteIndexPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a log-group level field index policy that was applied to a single log
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_index_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_index_policy)
        """

    def delete_integration(
        self, **kwargs: Unpack[DeleteIntegrationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the integration between CloudWatch Logs and OpenSearch Service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_integration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_integration)
        """

    def delete_log_anomaly_detector(
        self, **kwargs: Unpack[DeleteLogAnomalyDetectorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified CloudWatch Logs anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_log_anomaly_detector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_log_anomaly_detector)
        """

    def delete_log_group(
        self, **kwargs: Unpack[DeleteLogGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified log group and permanently deletes all the archived log
        events associated with the log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_log_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_log_group)
        """

    def delete_log_stream(
        self, **kwargs: Unpack[DeleteLogStreamRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified log stream and permanently deletes all the archived log
        events associated with the log stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_log_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_log_stream)
        """

    def delete_metric_filter(
        self, **kwargs: Unpack[DeleteMetricFilterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified metric filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_metric_filter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_metric_filter)
        """

    def delete_query_definition(
        self, **kwargs: Unpack[DeleteQueryDefinitionRequestRequestTypeDef]
    ) -> DeleteQueryDefinitionResponseTypeDef:
        """
        Deletes a saved CloudWatch Logs Insights query definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_query_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_query_definition)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a resource policy from this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_resource_policy)
        """

    def delete_retention_policy(
        self, **kwargs: Unpack[DeleteRetentionPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified retention policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_retention_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_retention_policy)
        """

    def delete_subscription_filter(
        self, **kwargs: Unpack[DeleteSubscriptionFilterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified subscription filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_subscription_filter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_subscription_filter)
        """

    def delete_transformer(
        self, **kwargs: Unpack[DeleteTransformerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the log transformer for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_transformer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#delete_transformer)
        """

    def describe_account_policies(
        self, **kwargs: Unpack[DescribeAccountPoliciesRequestRequestTypeDef]
    ) -> DescribeAccountPoliciesResponseTypeDef:
        """
        Returns a list of all CloudWatch Logs account policies in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_account_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_account_policies)
        """

    def describe_configuration_templates(
        self, **kwargs: Unpack[DescribeConfigurationTemplatesRequestRequestTypeDef]
    ) -> DescribeConfigurationTemplatesResponseTypeDef:
        """
        Use this operation to return the valid and default values that are used when
        creating delivery sources, delivery destinations, and deliveries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_configuration_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_configuration_templates)
        """

    def describe_deliveries(
        self, **kwargs: Unpack[DescribeDeliveriesRequestRequestTypeDef]
    ) -> DescribeDeliveriesResponseTypeDef:
        """
        Retrieves a list of the deliveries that have been created in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_deliveries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_deliveries)
        """

    def describe_delivery_destinations(
        self, **kwargs: Unpack[DescribeDeliveryDestinationsRequestRequestTypeDef]
    ) -> DescribeDeliveryDestinationsResponseTypeDef:
        """
        Retrieves a list of the delivery destinations that have been created in the
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_delivery_destinations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_delivery_destinations)
        """

    def describe_delivery_sources(
        self, **kwargs: Unpack[DescribeDeliverySourcesRequestRequestTypeDef]
    ) -> DescribeDeliverySourcesResponseTypeDef:
        """
        Retrieves a list of the delivery sources that have been created in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_delivery_sources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_delivery_sources)
        """

    def describe_destinations(
        self, **kwargs: Unpack[DescribeDestinationsRequestRequestTypeDef]
    ) -> DescribeDestinationsResponseTypeDef:
        """
        Lists all your destinations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_destinations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_destinations)
        """

    def describe_export_tasks(
        self, **kwargs: Unpack[DescribeExportTasksRequestRequestTypeDef]
    ) -> DescribeExportTasksResponseTypeDef:
        """
        Lists the specified export tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_export_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_export_tasks)
        """

    def describe_field_indexes(
        self, **kwargs: Unpack[DescribeFieldIndexesRequestRequestTypeDef]
    ) -> DescribeFieldIndexesResponseTypeDef:
        """
        Returns a list of field indexes listed in the field index policies of one or
        more log groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_field_indexes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_field_indexes)
        """

    def describe_index_policies(
        self, **kwargs: Unpack[DescribeIndexPoliciesRequestRequestTypeDef]
    ) -> DescribeIndexPoliciesResponseTypeDef:
        """
        Returns the field index policies of one or more log groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_index_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_index_policies)
        """

    def describe_log_groups(
        self, **kwargs: Unpack[DescribeLogGroupsRequestRequestTypeDef]
    ) -> DescribeLogGroupsResponseTypeDef:
        """
        Lists the specified log groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_log_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_log_groups)
        """

    def describe_log_streams(
        self, **kwargs: Unpack[DescribeLogStreamsRequestRequestTypeDef]
    ) -> DescribeLogStreamsResponseTypeDef:
        """
        Lists the log streams for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_log_streams.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_log_streams)
        """

    def describe_metric_filters(
        self, **kwargs: Unpack[DescribeMetricFiltersRequestRequestTypeDef]
    ) -> DescribeMetricFiltersResponseTypeDef:
        """
        Lists the specified metric filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_metric_filters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_metric_filters)
        """

    def describe_queries(
        self, **kwargs: Unpack[DescribeQueriesRequestRequestTypeDef]
    ) -> DescribeQueriesResponseTypeDef:
        """
        Returns a list of CloudWatch Logs Insights queries that are scheduled, running,
        or have been run recently in this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_queries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_queries)
        """

    def describe_query_definitions(
        self, **kwargs: Unpack[DescribeQueryDefinitionsRequestRequestTypeDef]
    ) -> DescribeQueryDefinitionsResponseTypeDef:
        """
        This operation returns a paginated list of your saved CloudWatch Logs Insights
        query definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_query_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_query_definitions)
        """

    def describe_resource_policies(
        self, **kwargs: Unpack[DescribeResourcePoliciesRequestRequestTypeDef]
    ) -> DescribeResourcePoliciesResponseTypeDef:
        """
        Lists the resource policies in this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_resource_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_resource_policies)
        """

    def describe_subscription_filters(
        self, **kwargs: Unpack[DescribeSubscriptionFiltersRequestRequestTypeDef]
    ) -> DescribeSubscriptionFiltersResponseTypeDef:
        """
        Lists the subscription filters for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_subscription_filters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#describe_subscription_filters)
        """

    def disassociate_kms_key(
        self, **kwargs: Unpack[DisassociateKmsKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates the specified KMS key from the specified log group or from all
        CloudWatch Logs Insights query results in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/disassociate_kms_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#disassociate_kms_key)
        """

    def filter_log_events(
        self, **kwargs: Unpack[FilterLogEventsRequestRequestTypeDef]
    ) -> FilterLogEventsResponseTypeDef:
        """
        Lists log events from the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/filter_log_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#filter_log_events)
        """

    def get_data_protection_policy(
        self, **kwargs: Unpack[GetDataProtectionPolicyRequestRequestTypeDef]
    ) -> GetDataProtectionPolicyResponseTypeDef:
        """
        Returns information about a log group data protection policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_data_protection_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_data_protection_policy)
        """

    def get_delivery(
        self, **kwargs: Unpack[GetDeliveryRequestRequestTypeDef]
    ) -> GetDeliveryResponseTypeDef:
        """
        Returns complete information about one logical <i>delivery</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_delivery.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_delivery)
        """

    def get_delivery_destination(
        self, **kwargs: Unpack[GetDeliveryDestinationRequestRequestTypeDef]
    ) -> GetDeliveryDestinationResponseTypeDef:
        """
        Retrieves complete information about one delivery destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_delivery_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_delivery_destination)
        """

    def get_delivery_destination_policy(
        self, **kwargs: Unpack[GetDeliveryDestinationPolicyRequestRequestTypeDef]
    ) -> GetDeliveryDestinationPolicyResponseTypeDef:
        """
        Retrieves the delivery destination policy assigned to the delivery destination
        that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_delivery_destination_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_delivery_destination_policy)
        """

    def get_delivery_source(
        self, **kwargs: Unpack[GetDeliverySourceRequestRequestTypeDef]
    ) -> GetDeliverySourceResponseTypeDef:
        """
        Retrieves complete information about one delivery source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_delivery_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_delivery_source)
        """

    def get_integration(
        self, **kwargs: Unpack[GetIntegrationRequestRequestTypeDef]
    ) -> GetIntegrationResponseTypeDef:
        """
        Returns information about one integration between CloudWatch Logs and
        OpenSearch Service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_integration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_integration)
        """

    def get_log_anomaly_detector(
        self, **kwargs: Unpack[GetLogAnomalyDetectorRequestRequestTypeDef]
    ) -> GetLogAnomalyDetectorResponseTypeDef:
        """
        Retrieves information about the log anomaly detector that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_log_anomaly_detector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_log_anomaly_detector)
        """

    def get_log_events(
        self, **kwargs: Unpack[GetLogEventsRequestRequestTypeDef]
    ) -> GetLogEventsResponseTypeDef:
        """
        Lists log events from the specified log stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_log_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_log_events)
        """

    def get_log_group_fields(
        self, **kwargs: Unpack[GetLogGroupFieldsRequestRequestTypeDef]
    ) -> GetLogGroupFieldsResponseTypeDef:
        """
        Returns a list of the fields that are included in log events in the specified
        log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_log_group_fields.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_log_group_fields)
        """

    def get_log_record(
        self, **kwargs: Unpack[GetLogRecordRequestRequestTypeDef]
    ) -> GetLogRecordResponseTypeDef:
        """
        Retrieves all of the fields and values of a single log event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_log_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_log_record)
        """

    def get_query_results(
        self, **kwargs: Unpack[GetQueryResultsRequestRequestTypeDef]
    ) -> GetQueryResultsResponseTypeDef:
        """
        Returns the results from the specified query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_query_results.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_query_results)
        """

    def get_transformer(
        self, **kwargs: Unpack[GetTransformerRequestRequestTypeDef]
    ) -> GetTransformerResponseTypeDef:
        """
        Returns the information about the log transformer associated with this log
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_transformer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_transformer)
        """

    def list_anomalies(
        self, **kwargs: Unpack[ListAnomaliesRequestRequestTypeDef]
    ) -> ListAnomaliesResponseTypeDef:
        """
        Returns a list of anomalies that log anomaly detectors have found.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/list_anomalies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#list_anomalies)
        """

    def list_integrations(
        self, **kwargs: Unpack[ListIntegrationsRequestRequestTypeDef]
    ) -> ListIntegrationsResponseTypeDef:
        """
        Returns a list of integrations between CloudWatch Logs and other services in
        this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/list_integrations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#list_integrations)
        """

    def list_log_anomaly_detectors(
        self, **kwargs: Unpack[ListLogAnomalyDetectorsRequestRequestTypeDef]
    ) -> ListLogAnomalyDetectorsResponseTypeDef:
        """
        Retrieves a list of the log anomaly detectors in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/list_log_anomaly_detectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#list_log_anomaly_detectors)
        """

    def list_log_groups_for_query(
        self, **kwargs: Unpack[ListLogGroupsForQueryRequestRequestTypeDef]
    ) -> ListLogGroupsForQueryResponseTypeDef:
        """
        Returns a list of the log groups that were analyzed during a single CloudWatch
        Logs Insights query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/list_log_groups_for_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#list_log_groups_for_query)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Displays the tags associated with a CloudWatch Logs resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#list_tags_for_resource)
        """

    def list_tags_log_group(
        self, **kwargs: Unpack[ListTagsLogGroupRequestRequestTypeDef]
    ) -> ListTagsLogGroupResponseTypeDef:
        """
        The ListTagsLogGroup operation is on the path to deprecation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/list_tags_log_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#list_tags_log_group)
        """

    def put_account_policy(
        self, **kwargs: Unpack[PutAccountPolicyRequestRequestTypeDef]
    ) -> PutAccountPolicyResponseTypeDef:
        """
        Creates an account-level data protection policy, subscription filter policy, or
        field index policy that applies to all log groups or a subset of log groups in
        the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_account_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_account_policy)
        """

    def put_data_protection_policy(
        self, **kwargs: Unpack[PutDataProtectionPolicyRequestRequestTypeDef]
    ) -> PutDataProtectionPolicyResponseTypeDef:
        """
        Creates a data protection policy for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_data_protection_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_data_protection_policy)
        """

    def put_delivery_destination(
        self, **kwargs: Unpack[PutDeliveryDestinationRequestRequestTypeDef]
    ) -> PutDeliveryDestinationResponseTypeDef:
        """
        Creates or updates a logical <i>delivery destination</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_delivery_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_delivery_destination)
        """

    def put_delivery_destination_policy(
        self, **kwargs: Unpack[PutDeliveryDestinationPolicyRequestRequestTypeDef]
    ) -> PutDeliveryDestinationPolicyResponseTypeDef:
        """
        Creates and assigns an IAM policy that grants permissions to CloudWatch Logs to
        deliver logs cross-account to a specified destination in this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_delivery_destination_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_delivery_destination_policy)
        """

    def put_delivery_source(
        self, **kwargs: Unpack[PutDeliverySourceRequestRequestTypeDef]
    ) -> PutDeliverySourceResponseTypeDef:
        """
        Creates or updates a logical <i>delivery source</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_delivery_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_delivery_source)
        """

    def put_destination(
        self, **kwargs: Unpack[PutDestinationRequestRequestTypeDef]
    ) -> PutDestinationResponseTypeDef:
        """
        Creates or updates a destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_destination)
        """

    def put_destination_policy(
        self, **kwargs: Unpack[PutDestinationPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates an access policy associated with an existing destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_destination_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_destination_policy)
        """

    def put_index_policy(
        self, **kwargs: Unpack[PutIndexPolicyRequestRequestTypeDef]
    ) -> PutIndexPolicyResponseTypeDef:
        """
        Creates or updates a <i>field index policy</i> for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_index_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_index_policy)
        """

    def put_integration(
        self, **kwargs: Unpack[PutIntegrationRequestRequestTypeDef]
    ) -> PutIntegrationResponseTypeDef:
        """
        Creates an integration between CloudWatch Logs and another service in this
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_integration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_integration)
        """

    def put_log_events(
        self, **kwargs: Unpack[PutLogEventsRequestRequestTypeDef]
    ) -> PutLogEventsResponseTypeDef:
        """
        Uploads a batch of log events to the specified log stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_log_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_log_events)
        """

    def put_metric_filter(
        self, **kwargs: Unpack[PutMetricFilterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates a metric filter and associates it with the specified log
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_metric_filter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_metric_filter)
        """

    def put_query_definition(
        self, **kwargs: Unpack[PutQueryDefinitionRequestRequestTypeDef]
    ) -> PutQueryDefinitionResponseTypeDef:
        """
        Creates or updates a query definition for CloudWatch Logs Insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_query_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_query_definition)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Creates or updates a resource policy allowing other Amazon Web Services
        services to put log events to this account, such as Amazon Route 53.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_resource_policy)
        """

    def put_retention_policy(
        self, **kwargs: Unpack[PutRetentionPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the retention of the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_retention_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_retention_policy)
        """

    def put_subscription_filter(
        self, **kwargs: Unpack[PutSubscriptionFilterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates a subscription filter and associates it with the specified
        log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_subscription_filter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_subscription_filter)
        """

    def put_transformer(
        self, **kwargs: Unpack[PutTransformerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates a <i>log transformer</i> for a single log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_transformer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#put_transformer)
        """

    def start_live_tail(
        self, **kwargs: Unpack[StartLiveTailRequestRequestTypeDef]
    ) -> StartLiveTailResponseTypeDef:
        """
        Starts a Live Tail streaming session for one or more log groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/start_live_tail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#start_live_tail)
        """

    def start_query(
        self, **kwargs: Unpack[StartQueryRequestRequestTypeDef]
    ) -> StartQueryResponseTypeDef:
        """
        Starts a query of one or more log groups using CloudWatch Logs Insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/start_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#start_query)
        """

    def stop_query(
        self, **kwargs: Unpack[StopQueryRequestRequestTypeDef]
    ) -> StopQueryResponseTypeDef:
        """
        Stops a CloudWatch Logs Insights query that is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/stop_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#stop_query)
        """

    def tag_log_group(
        self, **kwargs: Unpack[TagLogGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The TagLogGroup operation is on the path to deprecation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/tag_log_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#tag_log_group)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns one or more tags (key-value pairs) to the specified CloudWatch Logs
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#tag_resource)
        """

    def test_metric_filter(
        self, **kwargs: Unpack[TestMetricFilterRequestRequestTypeDef]
    ) -> TestMetricFilterResponseTypeDef:
        """
        Tests the filter pattern of a metric filter against a sample of log event
        messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/test_metric_filter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#test_metric_filter)
        """

    def test_transformer(
        self, **kwargs: Unpack[TestTransformerRequestRequestTypeDef]
    ) -> TestTransformerResponseTypeDef:
        """
        Use this operation to test a log transformer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/test_transformer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#test_transformer)
        """

    def untag_log_group(
        self, **kwargs: Unpack[UntagLogGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The UntagLogGroup operation is on the path to deprecation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/untag_log_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#untag_log_group)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#untag_resource)
        """

    def update_anomaly(
        self, **kwargs: Unpack[UpdateAnomalyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Use this operation to <i>suppress</i> anomaly detection for a specified anomaly
        or pattern.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/update_anomaly.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#update_anomaly)
        """

    def update_delivery_configuration(
        self, **kwargs: Unpack[UpdateDeliveryConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Use this operation to update the configuration of a <a
        href="https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_Delivery.html">delivery</a>
        to change either the S3 path pattern or the format of the delivered logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/update_delivery_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#update_delivery_configuration)
        """

    def update_log_anomaly_detector(
        self, **kwargs: Unpack[UpdateLogAnomalyDetectorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an existing log anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/update_log_anomaly_detector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#update_log_anomaly_detector)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_configuration_templates"]
    ) -> DescribeConfigurationTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_deliveries"]
    ) -> DescribeDeliveriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_delivery_destinations"]
    ) -> DescribeDeliveryDestinationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_delivery_sources"]
    ) -> DescribeDeliverySourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_destinations"]
    ) -> DescribeDestinationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_export_tasks"]
    ) -> DescribeExportTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_log_groups"]
    ) -> DescribeLogGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_log_streams"]
    ) -> DescribeLogStreamsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_metric_filters"]
    ) -> DescribeMetricFiltersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_queries"]
    ) -> DescribeQueriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_resource_policies"]
    ) -> DescribeResourcePoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_subscription_filters"]
    ) -> DescribeSubscriptionFiltersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["filter_log_events"]
    ) -> FilterLogEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_anomalies"]) -> ListAnomaliesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_log_anomaly_detectors"]
    ) -> ListLogAnomalyDetectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_log_groups_for_query"]
    ) -> ListLogGroupsForQueryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_logs/client/#get_paginator)
        """
