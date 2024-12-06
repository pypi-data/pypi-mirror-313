"""
Type annotations for iot service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iot.client import IoTClient

    session = Session()
    client: IoTClient = session.client("iot")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetBehaviorModelTrainingSummariesPaginator,
    ListActiveViolationsPaginator,
    ListAttachedPoliciesPaginator,
    ListAuditFindingsPaginator,
    ListAuditMitigationActionsExecutionsPaginator,
    ListAuditMitigationActionsTasksPaginator,
    ListAuditSuppressionsPaginator,
    ListAuditTasksPaginator,
    ListAuthorizersPaginator,
    ListBillingGroupsPaginator,
    ListCACertificatesPaginator,
    ListCertificatesByCAPaginator,
    ListCertificatesPaginator,
    ListCommandExecutionsPaginator,
    ListCommandsPaginator,
    ListCustomMetricsPaginator,
    ListDetectMitigationActionsExecutionsPaginator,
    ListDetectMitigationActionsTasksPaginator,
    ListDimensionsPaginator,
    ListDomainConfigurationsPaginator,
    ListFleetMetricsPaginator,
    ListIndicesPaginator,
    ListJobExecutionsForJobPaginator,
    ListJobExecutionsForThingPaginator,
    ListJobsPaginator,
    ListJobTemplatesPaginator,
    ListManagedJobTemplatesPaginator,
    ListMetricValuesPaginator,
    ListMitigationActionsPaginator,
    ListOTAUpdatesPaginator,
    ListOutgoingCertificatesPaginator,
    ListPackagesPaginator,
    ListPackageVersionsPaginator,
    ListPoliciesPaginator,
    ListPolicyPrincipalsPaginator,
    ListPrincipalPoliciesPaginator,
    ListPrincipalThingsPaginator,
    ListPrincipalThingsV2Paginator,
    ListProvisioningTemplatesPaginator,
    ListProvisioningTemplateVersionsPaginator,
    ListRelatedResourcesForAuditFindingPaginator,
    ListRoleAliasesPaginator,
    ListSbomValidationResultsPaginator,
    ListScheduledAuditsPaginator,
    ListSecurityProfilesForTargetPaginator,
    ListSecurityProfilesPaginator,
    ListStreamsPaginator,
    ListTagsForResourcePaginator,
    ListTargetsForPolicyPaginator,
    ListTargetsForSecurityProfilePaginator,
    ListThingGroupsForThingPaginator,
    ListThingGroupsPaginator,
    ListThingPrincipalsPaginator,
    ListThingPrincipalsV2Paginator,
    ListThingRegistrationTaskReportsPaginator,
    ListThingRegistrationTasksPaginator,
    ListThingsInBillingGroupPaginator,
    ListThingsInThingGroupPaginator,
    ListThingsPaginator,
    ListThingTypesPaginator,
    ListTopicRuleDestinationsPaginator,
    ListTopicRulesPaginator,
    ListV2LoggingLevelsPaginator,
    ListViolationEventsPaginator,
)
from .type_defs import (
    AcceptCertificateTransferRequestRequestTypeDef,
    AddThingToBillingGroupRequestRequestTypeDef,
    AddThingToThingGroupRequestRequestTypeDef,
    AssociateSbomWithPackageVersionRequestRequestTypeDef,
    AssociateSbomWithPackageVersionResponseTypeDef,
    AssociateTargetsWithJobRequestRequestTypeDef,
    AssociateTargetsWithJobResponseTypeDef,
    AttachPolicyRequestRequestTypeDef,
    AttachPrincipalPolicyRequestRequestTypeDef,
    AttachSecurityProfileRequestRequestTypeDef,
    AttachThingPrincipalRequestRequestTypeDef,
    CancelAuditMitigationActionsTaskRequestRequestTypeDef,
    CancelAuditTaskRequestRequestTypeDef,
    CancelCertificateTransferRequestRequestTypeDef,
    CancelDetectMitigationActionsTaskRequestRequestTypeDef,
    CancelJobExecutionRequestRequestTypeDef,
    CancelJobRequestRequestTypeDef,
    CancelJobResponseTypeDef,
    ConfirmTopicRuleDestinationRequestRequestTypeDef,
    CreateAuditSuppressionRequestRequestTypeDef,
    CreateAuthorizerRequestRequestTypeDef,
    CreateAuthorizerResponseTypeDef,
    CreateBillingGroupRequestRequestTypeDef,
    CreateBillingGroupResponseTypeDef,
    CreateCertificateFromCsrRequestRequestTypeDef,
    CreateCertificateFromCsrResponseTypeDef,
    CreateCertificateProviderRequestRequestTypeDef,
    CreateCertificateProviderResponseTypeDef,
    CreateCommandRequestRequestTypeDef,
    CreateCommandResponseTypeDef,
    CreateCustomMetricRequestRequestTypeDef,
    CreateCustomMetricResponseTypeDef,
    CreateDimensionRequestRequestTypeDef,
    CreateDimensionResponseTypeDef,
    CreateDomainConfigurationRequestRequestTypeDef,
    CreateDomainConfigurationResponseTypeDef,
    CreateDynamicThingGroupRequestRequestTypeDef,
    CreateDynamicThingGroupResponseTypeDef,
    CreateFleetMetricRequestRequestTypeDef,
    CreateFleetMetricResponseTypeDef,
    CreateJobRequestRequestTypeDef,
    CreateJobResponseTypeDef,
    CreateJobTemplateRequestRequestTypeDef,
    CreateJobTemplateResponseTypeDef,
    CreateKeysAndCertificateRequestRequestTypeDef,
    CreateKeysAndCertificateResponseTypeDef,
    CreateMitigationActionRequestRequestTypeDef,
    CreateMitigationActionResponseTypeDef,
    CreateOTAUpdateRequestRequestTypeDef,
    CreateOTAUpdateResponseTypeDef,
    CreatePackageRequestRequestTypeDef,
    CreatePackageResponseTypeDef,
    CreatePackageVersionRequestRequestTypeDef,
    CreatePackageVersionResponseTypeDef,
    CreatePolicyRequestRequestTypeDef,
    CreatePolicyResponseTypeDef,
    CreatePolicyVersionRequestRequestTypeDef,
    CreatePolicyVersionResponseTypeDef,
    CreateProvisioningClaimRequestRequestTypeDef,
    CreateProvisioningClaimResponseTypeDef,
    CreateProvisioningTemplateRequestRequestTypeDef,
    CreateProvisioningTemplateResponseTypeDef,
    CreateProvisioningTemplateVersionRequestRequestTypeDef,
    CreateProvisioningTemplateVersionResponseTypeDef,
    CreateRoleAliasRequestRequestTypeDef,
    CreateRoleAliasResponseTypeDef,
    CreateScheduledAuditRequestRequestTypeDef,
    CreateScheduledAuditResponseTypeDef,
    CreateSecurityProfileRequestRequestTypeDef,
    CreateSecurityProfileResponseTypeDef,
    CreateStreamRequestRequestTypeDef,
    CreateStreamResponseTypeDef,
    CreateThingGroupRequestRequestTypeDef,
    CreateThingGroupResponseTypeDef,
    CreateThingRequestRequestTypeDef,
    CreateThingResponseTypeDef,
    CreateThingTypeRequestRequestTypeDef,
    CreateThingTypeResponseTypeDef,
    CreateTopicRuleDestinationRequestRequestTypeDef,
    CreateTopicRuleDestinationResponseTypeDef,
    CreateTopicRuleRequestRequestTypeDef,
    DeleteAccountAuditConfigurationRequestRequestTypeDef,
    DeleteAuditSuppressionRequestRequestTypeDef,
    DeleteAuthorizerRequestRequestTypeDef,
    DeleteBillingGroupRequestRequestTypeDef,
    DeleteCACertificateRequestRequestTypeDef,
    DeleteCertificateProviderRequestRequestTypeDef,
    DeleteCertificateRequestRequestTypeDef,
    DeleteCommandExecutionRequestRequestTypeDef,
    DeleteCommandRequestRequestTypeDef,
    DeleteCommandResponseTypeDef,
    DeleteCustomMetricRequestRequestTypeDef,
    DeleteDimensionRequestRequestTypeDef,
    DeleteDomainConfigurationRequestRequestTypeDef,
    DeleteDynamicThingGroupRequestRequestTypeDef,
    DeleteFleetMetricRequestRequestTypeDef,
    DeleteJobExecutionRequestRequestTypeDef,
    DeleteJobRequestRequestTypeDef,
    DeleteJobTemplateRequestRequestTypeDef,
    DeleteMitigationActionRequestRequestTypeDef,
    DeleteOTAUpdateRequestRequestTypeDef,
    DeletePackageRequestRequestTypeDef,
    DeletePackageVersionRequestRequestTypeDef,
    DeletePolicyRequestRequestTypeDef,
    DeletePolicyVersionRequestRequestTypeDef,
    DeleteProvisioningTemplateRequestRequestTypeDef,
    DeleteProvisioningTemplateVersionRequestRequestTypeDef,
    DeleteRoleAliasRequestRequestTypeDef,
    DeleteScheduledAuditRequestRequestTypeDef,
    DeleteSecurityProfileRequestRequestTypeDef,
    DeleteStreamRequestRequestTypeDef,
    DeleteThingGroupRequestRequestTypeDef,
    DeleteThingRequestRequestTypeDef,
    DeleteThingTypeRequestRequestTypeDef,
    DeleteTopicRuleDestinationRequestRequestTypeDef,
    DeleteTopicRuleRequestRequestTypeDef,
    DeleteV2LoggingLevelRequestRequestTypeDef,
    DeprecateThingTypeRequestRequestTypeDef,
    DescribeAccountAuditConfigurationResponseTypeDef,
    DescribeAuditFindingRequestRequestTypeDef,
    DescribeAuditFindingResponseTypeDef,
    DescribeAuditMitigationActionsTaskRequestRequestTypeDef,
    DescribeAuditMitigationActionsTaskResponseTypeDef,
    DescribeAuditSuppressionRequestRequestTypeDef,
    DescribeAuditSuppressionResponseTypeDef,
    DescribeAuditTaskRequestRequestTypeDef,
    DescribeAuditTaskResponseTypeDef,
    DescribeAuthorizerRequestRequestTypeDef,
    DescribeAuthorizerResponseTypeDef,
    DescribeBillingGroupRequestRequestTypeDef,
    DescribeBillingGroupResponseTypeDef,
    DescribeCACertificateRequestRequestTypeDef,
    DescribeCACertificateResponseTypeDef,
    DescribeCertificateProviderRequestRequestTypeDef,
    DescribeCertificateProviderResponseTypeDef,
    DescribeCertificateRequestRequestTypeDef,
    DescribeCertificateResponseTypeDef,
    DescribeCustomMetricRequestRequestTypeDef,
    DescribeCustomMetricResponseTypeDef,
    DescribeDefaultAuthorizerResponseTypeDef,
    DescribeDetectMitigationActionsTaskRequestRequestTypeDef,
    DescribeDetectMitigationActionsTaskResponseTypeDef,
    DescribeDimensionRequestRequestTypeDef,
    DescribeDimensionResponseTypeDef,
    DescribeDomainConfigurationRequestRequestTypeDef,
    DescribeDomainConfigurationResponseTypeDef,
    DescribeEndpointRequestRequestTypeDef,
    DescribeEndpointResponseTypeDef,
    DescribeEventConfigurationsResponseTypeDef,
    DescribeFleetMetricRequestRequestTypeDef,
    DescribeFleetMetricResponseTypeDef,
    DescribeIndexRequestRequestTypeDef,
    DescribeIndexResponseTypeDef,
    DescribeJobExecutionRequestRequestTypeDef,
    DescribeJobExecutionResponseTypeDef,
    DescribeJobRequestRequestTypeDef,
    DescribeJobResponseTypeDef,
    DescribeJobTemplateRequestRequestTypeDef,
    DescribeJobTemplateResponseTypeDef,
    DescribeManagedJobTemplateRequestRequestTypeDef,
    DescribeManagedJobTemplateResponseTypeDef,
    DescribeMitigationActionRequestRequestTypeDef,
    DescribeMitigationActionResponseTypeDef,
    DescribeProvisioningTemplateRequestRequestTypeDef,
    DescribeProvisioningTemplateResponseTypeDef,
    DescribeProvisioningTemplateVersionRequestRequestTypeDef,
    DescribeProvisioningTemplateVersionResponseTypeDef,
    DescribeRoleAliasRequestRequestTypeDef,
    DescribeRoleAliasResponseTypeDef,
    DescribeScheduledAuditRequestRequestTypeDef,
    DescribeScheduledAuditResponseTypeDef,
    DescribeSecurityProfileRequestRequestTypeDef,
    DescribeSecurityProfileResponseTypeDef,
    DescribeStreamRequestRequestTypeDef,
    DescribeStreamResponseTypeDef,
    DescribeThingGroupRequestRequestTypeDef,
    DescribeThingGroupResponseTypeDef,
    DescribeThingRegistrationTaskRequestRequestTypeDef,
    DescribeThingRegistrationTaskResponseTypeDef,
    DescribeThingRequestRequestTypeDef,
    DescribeThingResponseTypeDef,
    DescribeThingTypeRequestRequestTypeDef,
    DescribeThingTypeResponseTypeDef,
    DetachPolicyRequestRequestTypeDef,
    DetachPrincipalPolicyRequestRequestTypeDef,
    DetachSecurityProfileRequestRequestTypeDef,
    DetachThingPrincipalRequestRequestTypeDef,
    DisableTopicRuleRequestRequestTypeDef,
    DisassociateSbomFromPackageVersionRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableTopicRuleRequestRequestTypeDef,
    GetBehaviorModelTrainingSummariesRequestRequestTypeDef,
    GetBehaviorModelTrainingSummariesResponseTypeDef,
    GetBucketsAggregationRequestRequestTypeDef,
    GetBucketsAggregationResponseTypeDef,
    GetCardinalityRequestRequestTypeDef,
    GetCardinalityResponseTypeDef,
    GetCommandExecutionRequestRequestTypeDef,
    GetCommandExecutionResponseTypeDef,
    GetCommandRequestRequestTypeDef,
    GetCommandResponseTypeDef,
    GetEffectivePoliciesRequestRequestTypeDef,
    GetEffectivePoliciesResponseTypeDef,
    GetIndexingConfigurationResponseTypeDef,
    GetJobDocumentRequestRequestTypeDef,
    GetJobDocumentResponseTypeDef,
    GetLoggingOptionsResponseTypeDef,
    GetOTAUpdateRequestRequestTypeDef,
    GetOTAUpdateResponseTypeDef,
    GetPackageConfigurationResponseTypeDef,
    GetPackageRequestRequestTypeDef,
    GetPackageResponseTypeDef,
    GetPackageVersionRequestRequestTypeDef,
    GetPackageVersionResponseTypeDef,
    GetPercentilesRequestRequestTypeDef,
    GetPercentilesResponseTypeDef,
    GetPolicyRequestRequestTypeDef,
    GetPolicyResponseTypeDef,
    GetPolicyVersionRequestRequestTypeDef,
    GetPolicyVersionResponseTypeDef,
    GetRegistrationCodeResponseTypeDef,
    GetStatisticsRequestRequestTypeDef,
    GetStatisticsResponseTypeDef,
    GetTopicRuleDestinationRequestRequestTypeDef,
    GetTopicRuleDestinationResponseTypeDef,
    GetTopicRuleRequestRequestTypeDef,
    GetTopicRuleResponseTypeDef,
    GetV2LoggingOptionsResponseTypeDef,
    ListActiveViolationsRequestRequestTypeDef,
    ListActiveViolationsResponseTypeDef,
    ListAttachedPoliciesRequestRequestTypeDef,
    ListAttachedPoliciesResponseTypeDef,
    ListAuditFindingsRequestRequestTypeDef,
    ListAuditFindingsResponseTypeDef,
    ListAuditMitigationActionsExecutionsRequestRequestTypeDef,
    ListAuditMitigationActionsExecutionsResponseTypeDef,
    ListAuditMitigationActionsTasksRequestRequestTypeDef,
    ListAuditMitigationActionsTasksResponseTypeDef,
    ListAuditSuppressionsRequestRequestTypeDef,
    ListAuditSuppressionsResponseTypeDef,
    ListAuditTasksRequestRequestTypeDef,
    ListAuditTasksResponseTypeDef,
    ListAuthorizersRequestRequestTypeDef,
    ListAuthorizersResponseTypeDef,
    ListBillingGroupsRequestRequestTypeDef,
    ListBillingGroupsResponseTypeDef,
    ListCACertificatesRequestRequestTypeDef,
    ListCACertificatesResponseTypeDef,
    ListCertificateProvidersRequestRequestTypeDef,
    ListCertificateProvidersResponseTypeDef,
    ListCertificatesByCARequestRequestTypeDef,
    ListCertificatesByCAResponseTypeDef,
    ListCertificatesRequestRequestTypeDef,
    ListCertificatesResponseTypeDef,
    ListCommandExecutionsRequestRequestTypeDef,
    ListCommandExecutionsResponseTypeDef,
    ListCommandsRequestRequestTypeDef,
    ListCommandsResponseTypeDef,
    ListCustomMetricsRequestRequestTypeDef,
    ListCustomMetricsResponseTypeDef,
    ListDetectMitigationActionsExecutionsRequestRequestTypeDef,
    ListDetectMitigationActionsExecutionsResponseTypeDef,
    ListDetectMitigationActionsTasksRequestRequestTypeDef,
    ListDetectMitigationActionsTasksResponseTypeDef,
    ListDimensionsRequestRequestTypeDef,
    ListDimensionsResponseTypeDef,
    ListDomainConfigurationsRequestRequestTypeDef,
    ListDomainConfigurationsResponseTypeDef,
    ListFleetMetricsRequestRequestTypeDef,
    ListFleetMetricsResponseTypeDef,
    ListIndicesRequestRequestTypeDef,
    ListIndicesResponseTypeDef,
    ListJobExecutionsForJobRequestRequestTypeDef,
    ListJobExecutionsForJobResponseTypeDef,
    ListJobExecutionsForThingRequestRequestTypeDef,
    ListJobExecutionsForThingResponseTypeDef,
    ListJobsRequestRequestTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesRequestRequestTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListManagedJobTemplatesRequestRequestTypeDef,
    ListManagedJobTemplatesResponseTypeDef,
    ListMetricValuesRequestRequestTypeDef,
    ListMetricValuesResponseTypeDef,
    ListMitigationActionsRequestRequestTypeDef,
    ListMitigationActionsResponseTypeDef,
    ListOTAUpdatesRequestRequestTypeDef,
    ListOTAUpdatesResponseTypeDef,
    ListOutgoingCertificatesRequestRequestTypeDef,
    ListOutgoingCertificatesResponseTypeDef,
    ListPackagesRequestRequestTypeDef,
    ListPackagesResponseTypeDef,
    ListPackageVersionsRequestRequestTypeDef,
    ListPackageVersionsResponseTypeDef,
    ListPoliciesRequestRequestTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyPrincipalsRequestRequestTypeDef,
    ListPolicyPrincipalsResponseTypeDef,
    ListPolicyVersionsRequestRequestTypeDef,
    ListPolicyVersionsResponseTypeDef,
    ListPrincipalPoliciesRequestRequestTypeDef,
    ListPrincipalPoliciesResponseTypeDef,
    ListPrincipalThingsRequestRequestTypeDef,
    ListPrincipalThingsResponseTypeDef,
    ListPrincipalThingsV2RequestRequestTypeDef,
    ListPrincipalThingsV2ResponseTypeDef,
    ListProvisioningTemplatesRequestRequestTypeDef,
    ListProvisioningTemplatesResponseTypeDef,
    ListProvisioningTemplateVersionsRequestRequestTypeDef,
    ListProvisioningTemplateVersionsResponseTypeDef,
    ListRelatedResourcesForAuditFindingRequestRequestTypeDef,
    ListRelatedResourcesForAuditFindingResponseTypeDef,
    ListRoleAliasesRequestRequestTypeDef,
    ListRoleAliasesResponseTypeDef,
    ListSbomValidationResultsRequestRequestTypeDef,
    ListSbomValidationResultsResponseTypeDef,
    ListScheduledAuditsRequestRequestTypeDef,
    ListScheduledAuditsResponseTypeDef,
    ListSecurityProfilesForTargetRequestRequestTypeDef,
    ListSecurityProfilesForTargetResponseTypeDef,
    ListSecurityProfilesRequestRequestTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListStreamsRequestRequestTypeDef,
    ListStreamsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsForPolicyRequestRequestTypeDef,
    ListTargetsForPolicyResponseTypeDef,
    ListTargetsForSecurityProfileRequestRequestTypeDef,
    ListTargetsForSecurityProfileResponseTypeDef,
    ListThingGroupsForThingRequestRequestTypeDef,
    ListThingGroupsForThingResponseTypeDef,
    ListThingGroupsRequestRequestTypeDef,
    ListThingGroupsResponseTypeDef,
    ListThingPrincipalsRequestRequestTypeDef,
    ListThingPrincipalsResponseTypeDef,
    ListThingPrincipalsV2RequestRequestTypeDef,
    ListThingPrincipalsV2ResponseTypeDef,
    ListThingRegistrationTaskReportsRequestRequestTypeDef,
    ListThingRegistrationTaskReportsResponseTypeDef,
    ListThingRegistrationTasksRequestRequestTypeDef,
    ListThingRegistrationTasksResponseTypeDef,
    ListThingsInBillingGroupRequestRequestTypeDef,
    ListThingsInBillingGroupResponseTypeDef,
    ListThingsInThingGroupRequestRequestTypeDef,
    ListThingsInThingGroupResponseTypeDef,
    ListThingsRequestRequestTypeDef,
    ListThingsResponseTypeDef,
    ListThingTypesRequestRequestTypeDef,
    ListThingTypesResponseTypeDef,
    ListTopicRuleDestinationsRequestRequestTypeDef,
    ListTopicRuleDestinationsResponseTypeDef,
    ListTopicRulesRequestRequestTypeDef,
    ListTopicRulesResponseTypeDef,
    ListV2LoggingLevelsRequestRequestTypeDef,
    ListV2LoggingLevelsResponseTypeDef,
    ListViolationEventsRequestRequestTypeDef,
    ListViolationEventsResponseTypeDef,
    PutVerificationStateOnViolationRequestRequestTypeDef,
    RegisterCACertificateRequestRequestTypeDef,
    RegisterCACertificateResponseTypeDef,
    RegisterCertificateRequestRequestTypeDef,
    RegisterCertificateResponseTypeDef,
    RegisterCertificateWithoutCARequestRequestTypeDef,
    RegisterCertificateWithoutCAResponseTypeDef,
    RegisterThingRequestRequestTypeDef,
    RegisterThingResponseTypeDef,
    RejectCertificateTransferRequestRequestTypeDef,
    RemoveThingFromBillingGroupRequestRequestTypeDef,
    RemoveThingFromThingGroupRequestRequestTypeDef,
    ReplaceTopicRuleRequestRequestTypeDef,
    SearchIndexRequestRequestTypeDef,
    SearchIndexResponseTypeDef,
    SetDefaultAuthorizerRequestRequestTypeDef,
    SetDefaultAuthorizerResponseTypeDef,
    SetDefaultPolicyVersionRequestRequestTypeDef,
    SetLoggingOptionsRequestRequestTypeDef,
    SetV2LoggingLevelRequestRequestTypeDef,
    SetV2LoggingOptionsRequestRequestTypeDef,
    StartAuditMitigationActionsTaskRequestRequestTypeDef,
    StartAuditMitigationActionsTaskResponseTypeDef,
    StartDetectMitigationActionsTaskRequestRequestTypeDef,
    StartDetectMitigationActionsTaskResponseTypeDef,
    StartOnDemandAuditTaskRequestRequestTypeDef,
    StartOnDemandAuditTaskResponseTypeDef,
    StartThingRegistrationTaskRequestRequestTypeDef,
    StartThingRegistrationTaskResponseTypeDef,
    StopThingRegistrationTaskRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    TestAuthorizationRequestRequestTypeDef,
    TestAuthorizationResponseTypeDef,
    TestInvokeAuthorizerRequestRequestTypeDef,
    TestInvokeAuthorizerResponseTypeDef,
    TransferCertificateRequestRequestTypeDef,
    TransferCertificateResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAccountAuditConfigurationRequestRequestTypeDef,
    UpdateAuditSuppressionRequestRequestTypeDef,
    UpdateAuthorizerRequestRequestTypeDef,
    UpdateAuthorizerResponseTypeDef,
    UpdateBillingGroupRequestRequestTypeDef,
    UpdateBillingGroupResponseTypeDef,
    UpdateCACertificateRequestRequestTypeDef,
    UpdateCertificateProviderRequestRequestTypeDef,
    UpdateCertificateProviderResponseTypeDef,
    UpdateCertificateRequestRequestTypeDef,
    UpdateCommandRequestRequestTypeDef,
    UpdateCommandResponseTypeDef,
    UpdateCustomMetricRequestRequestTypeDef,
    UpdateCustomMetricResponseTypeDef,
    UpdateDimensionRequestRequestTypeDef,
    UpdateDimensionResponseTypeDef,
    UpdateDomainConfigurationRequestRequestTypeDef,
    UpdateDomainConfigurationResponseTypeDef,
    UpdateDynamicThingGroupRequestRequestTypeDef,
    UpdateDynamicThingGroupResponseTypeDef,
    UpdateEventConfigurationsRequestRequestTypeDef,
    UpdateFleetMetricRequestRequestTypeDef,
    UpdateIndexingConfigurationRequestRequestTypeDef,
    UpdateJobRequestRequestTypeDef,
    UpdateMitigationActionRequestRequestTypeDef,
    UpdateMitigationActionResponseTypeDef,
    UpdatePackageConfigurationRequestRequestTypeDef,
    UpdatePackageRequestRequestTypeDef,
    UpdatePackageVersionRequestRequestTypeDef,
    UpdateProvisioningTemplateRequestRequestTypeDef,
    UpdateRoleAliasRequestRequestTypeDef,
    UpdateRoleAliasResponseTypeDef,
    UpdateScheduledAuditRequestRequestTypeDef,
    UpdateScheduledAuditResponseTypeDef,
    UpdateSecurityProfileRequestRequestTypeDef,
    UpdateSecurityProfileResponseTypeDef,
    UpdateStreamRequestRequestTypeDef,
    UpdateStreamResponseTypeDef,
    UpdateThingGroupRequestRequestTypeDef,
    UpdateThingGroupResponseTypeDef,
    UpdateThingGroupsForThingRequestRequestTypeDef,
    UpdateThingRequestRequestTypeDef,
    UpdateThingTypeRequestRequestTypeDef,
    UpdateTopicRuleDestinationRequestRequestTypeDef,
    ValidateSecurityProfileBehaviorsRequestRequestTypeDef,
    ValidateSecurityProfileBehaviorsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("IoTClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    CertificateConflictException: Type[BotocoreClientError]
    CertificateStateException: Type[BotocoreClientError]
    CertificateValidationException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ConflictingResourceUpdateException: Type[BotocoreClientError]
    DeleteConflictException: Type[BotocoreClientError]
    IndexNotReadyException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidAggregationException: Type[BotocoreClientError]
    InvalidQueryException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidResponseException: Type[BotocoreClientError]
    InvalidStateTransitionException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedPolicyException: Type[BotocoreClientError]
    NotConfiguredException: Type[BotocoreClientError]
    RegistrationCodeValidationException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceRegistrationFailureException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    SqlParseException: Type[BotocoreClientError]
    TaskAlreadyExistsException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TransferAlreadyCompletedException: Type[BotocoreClientError]
    TransferConflictException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]
    VersionConflictException: Type[BotocoreClientError]
    VersionsLimitExceededException: Type[BotocoreClientError]


class IoTClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#close)
        """

    def accept_certificate_transfer(
        self, **kwargs: Unpack[AcceptCertificateTransferRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Accepts a pending certificate transfer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/accept_certificate_transfer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#accept_certificate_transfer)
        """

    def add_thing_to_billing_group(
        self, **kwargs: Unpack[AddThingToBillingGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds a thing to a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/add_thing_to_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#add_thing_to_billing_group)
        """

    def add_thing_to_thing_group(
        self, **kwargs: Unpack[AddThingToThingGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds a thing to a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/add_thing_to_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#add_thing_to_thing_group)
        """

    def associate_sbom_with_package_version(
        self, **kwargs: Unpack[AssociateSbomWithPackageVersionRequestRequestTypeDef]
    ) -> AssociateSbomWithPackageVersionResponseTypeDef:
        """
        Associates the selected software bill of materials (SBOM) with a specific
        software package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/associate_sbom_with_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#associate_sbom_with_package_version)
        """

    def associate_targets_with_job(
        self, **kwargs: Unpack[AssociateTargetsWithJobRequestRequestTypeDef]
    ) -> AssociateTargetsWithJobResponseTypeDef:
        """
        Associates a group with a continuous job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/associate_targets_with_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#associate_targets_with_job)
        """

    def attach_policy(
        self, **kwargs: Unpack[AttachPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches the specified policy to the specified principal (certificate or other
        credential).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/attach_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#attach_policy)
        """

    def attach_principal_policy(
        self, **kwargs: Unpack[AttachPrincipalPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches the specified policy to the specified principal (certificate or other
        credential).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/attach_principal_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#attach_principal_policy)
        """

    def attach_security_profile(
        self, **kwargs: Unpack[AttachSecurityProfileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a Device Defender security profile with a thing group or this
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/attach_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#attach_security_profile)
        """

    def attach_thing_principal(
        self, **kwargs: Unpack[AttachThingPrincipalRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches the specified principal to the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/attach_thing_principal.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#attach_thing_principal)
        """

    def cancel_audit_mitigation_actions_task(
        self, **kwargs: Unpack[CancelAuditMitigationActionsTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a mitigation action task that is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/cancel_audit_mitigation_actions_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#cancel_audit_mitigation_actions_task)
        """

    def cancel_audit_task(
        self, **kwargs: Unpack[CancelAuditTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels an audit that is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/cancel_audit_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#cancel_audit_task)
        """

    def cancel_certificate_transfer(
        self, **kwargs: Unpack[CancelCertificateTransferRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels a pending transfer for the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/cancel_certificate_transfer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#cancel_certificate_transfer)
        """

    def cancel_detect_mitigation_actions_task(
        self, **kwargs: Unpack[CancelDetectMitigationActionsTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a Device Defender ML Detect mitigation action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/cancel_detect_mitigation_actions_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#cancel_detect_mitigation_actions_task)
        """

    def cancel_job(
        self, **kwargs: Unpack[CancelJobRequestRequestTypeDef]
    ) -> CancelJobResponseTypeDef:
        """
        Cancels a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/cancel_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#cancel_job)
        """

    def cancel_job_execution(
        self, **kwargs: Unpack[CancelJobExecutionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels the execution of a job for a given thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/cancel_job_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#cancel_job_execution)
        """

    def clear_default_authorizer(self) -> Dict[str, Any]:
        """
        Clears the default authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/clear_default_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#clear_default_authorizer)
        """

    def confirm_topic_rule_destination(
        self, **kwargs: Unpack[ConfirmTopicRuleDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Confirms a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/confirm_topic_rule_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#confirm_topic_rule_destination)
        """

    def create_audit_suppression(
        self, **kwargs: Unpack[CreateAuditSuppressionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a Device Defender audit suppression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_audit_suppression.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_audit_suppression)
        """

    def create_authorizer(
        self, **kwargs: Unpack[CreateAuthorizerRequestRequestTypeDef]
    ) -> CreateAuthorizerResponseTypeDef:
        """
        Creates an authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_authorizer)
        """

    def create_billing_group(
        self, **kwargs: Unpack[CreateBillingGroupRequestRequestTypeDef]
    ) -> CreateBillingGroupResponseTypeDef:
        """
        Creates a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_billing_group)
        """

    def create_certificate_from_csr(
        self, **kwargs: Unpack[CreateCertificateFromCsrRequestRequestTypeDef]
    ) -> CreateCertificateFromCsrResponseTypeDef:
        """
        Creates an X.509 certificate using the specified certificate signing request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_certificate_from_csr.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_certificate_from_csr)
        """

    def create_certificate_provider(
        self, **kwargs: Unpack[CreateCertificateProviderRequestRequestTypeDef]
    ) -> CreateCertificateProviderResponseTypeDef:
        """
        Creates an Amazon Web Services IoT Core certificate provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_certificate_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_certificate_provider)
        """

    def create_command(
        self, **kwargs: Unpack[CreateCommandRequestRequestTypeDef]
    ) -> CreateCommandResponseTypeDef:
        """
        Creates a command.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_command.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_command)
        """

    def create_custom_metric(
        self, **kwargs: Unpack[CreateCustomMetricRequestRequestTypeDef]
    ) -> CreateCustomMetricResponseTypeDef:
        """
        Use this API to define a Custom Metric published by your devices to Device
        Defender.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_custom_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_custom_metric)
        """

    def create_dimension(
        self, **kwargs: Unpack[CreateDimensionRequestRequestTypeDef]
    ) -> CreateDimensionResponseTypeDef:
        """
        Create a dimension that you can use to limit the scope of a metric used in a
        security profile for IoT Device Defender.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_dimension.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_dimension)
        """

    def create_domain_configuration(
        self, **kwargs: Unpack[CreateDomainConfigurationRequestRequestTypeDef]
    ) -> CreateDomainConfigurationResponseTypeDef:
        """
        Creates a domain configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_domain_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_domain_configuration)
        """

    def create_dynamic_thing_group(
        self, **kwargs: Unpack[CreateDynamicThingGroupRequestRequestTypeDef]
    ) -> CreateDynamicThingGroupResponseTypeDef:
        """
        Creates a dynamic thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_dynamic_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_dynamic_thing_group)
        """

    def create_fleet_metric(
        self, **kwargs: Unpack[CreateFleetMetricRequestRequestTypeDef]
    ) -> CreateFleetMetricResponseTypeDef:
        """
        Creates a fleet metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_fleet_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_fleet_metric)
        """

    def create_job(
        self, **kwargs: Unpack[CreateJobRequestRequestTypeDef]
    ) -> CreateJobResponseTypeDef:
        """
        Creates a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_job)
        """

    def create_job_template(
        self, **kwargs: Unpack[CreateJobTemplateRequestRequestTypeDef]
    ) -> CreateJobTemplateResponseTypeDef:
        """
        Creates a job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_job_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_job_template)
        """

    def create_keys_and_certificate(
        self, **kwargs: Unpack[CreateKeysAndCertificateRequestRequestTypeDef]
    ) -> CreateKeysAndCertificateResponseTypeDef:
        """
        Creates a 2048-bit RSA key pair and issues an X.509 certificate using the
        issued public key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_keys_and_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_keys_and_certificate)
        """

    def create_mitigation_action(
        self, **kwargs: Unpack[CreateMitigationActionRequestRequestTypeDef]
    ) -> CreateMitigationActionResponseTypeDef:
        """
        Defines an action that can be applied to audit findings by using
        StartAuditMitigationActionsTask.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_mitigation_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_mitigation_action)
        """

    def create_ota_update(
        self, **kwargs: Unpack[CreateOTAUpdateRequestRequestTypeDef]
    ) -> CreateOTAUpdateResponseTypeDef:
        """
        Creates an IoT OTA update on a target group of things or groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_ota_update.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_ota_update)
        """

    def create_package(
        self, **kwargs: Unpack[CreatePackageRequestRequestTypeDef]
    ) -> CreatePackageResponseTypeDef:
        """
        Creates an IoT software package that can be deployed to your fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_package)
        """

    def create_package_version(
        self, **kwargs: Unpack[CreatePackageVersionRequestRequestTypeDef]
    ) -> CreatePackageVersionResponseTypeDef:
        """
        Creates a new version for an existing IoT software package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_package_version)
        """

    def create_policy(
        self, **kwargs: Unpack[CreatePolicyRequestRequestTypeDef]
    ) -> CreatePolicyResponseTypeDef:
        """
        Creates an IoT policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_policy)
        """

    def create_policy_version(
        self, **kwargs: Unpack[CreatePolicyVersionRequestRequestTypeDef]
    ) -> CreatePolicyVersionResponseTypeDef:
        """
        Creates a new version of the specified IoT policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_policy_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_policy_version)
        """

    def create_provisioning_claim(
        self, **kwargs: Unpack[CreateProvisioningClaimRequestRequestTypeDef]
    ) -> CreateProvisioningClaimResponseTypeDef:
        """
        Creates a provisioning claim.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_provisioning_claim.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_provisioning_claim)
        """

    def create_provisioning_template(
        self, **kwargs: Unpack[CreateProvisioningTemplateRequestRequestTypeDef]
    ) -> CreateProvisioningTemplateResponseTypeDef:
        """
        Creates a provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_provisioning_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_provisioning_template)
        """

    def create_provisioning_template_version(
        self, **kwargs: Unpack[CreateProvisioningTemplateVersionRequestRequestTypeDef]
    ) -> CreateProvisioningTemplateVersionResponseTypeDef:
        """
        Creates a new version of a provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_provisioning_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_provisioning_template_version)
        """

    def create_role_alias(
        self, **kwargs: Unpack[CreateRoleAliasRequestRequestTypeDef]
    ) -> CreateRoleAliasResponseTypeDef:
        """
        Creates a role alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_role_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_role_alias)
        """

    def create_scheduled_audit(
        self, **kwargs: Unpack[CreateScheduledAuditRequestRequestTypeDef]
    ) -> CreateScheduledAuditResponseTypeDef:
        """
        Creates a scheduled audit that is run at a specified time interval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_scheduled_audit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_scheduled_audit)
        """

    def create_security_profile(
        self, **kwargs: Unpack[CreateSecurityProfileRequestRequestTypeDef]
    ) -> CreateSecurityProfileResponseTypeDef:
        """
        Creates a Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_security_profile)
        """

    def create_stream(
        self, **kwargs: Unpack[CreateStreamRequestRequestTypeDef]
    ) -> CreateStreamResponseTypeDef:
        """
        Creates a stream for delivering one or more large files in chunks over MQTT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_stream)
        """

    def create_thing(
        self, **kwargs: Unpack[CreateThingRequestRequestTypeDef]
    ) -> CreateThingResponseTypeDef:
        """
        Creates a thing record in the registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_thing)
        """

    def create_thing_group(
        self, **kwargs: Unpack[CreateThingGroupRequestRequestTypeDef]
    ) -> CreateThingGroupResponseTypeDef:
        """
        Create a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_thing_group)
        """

    def create_thing_type(
        self, **kwargs: Unpack[CreateThingTypeRequestRequestTypeDef]
    ) -> CreateThingTypeResponseTypeDef:
        """
        Creates a new thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_thing_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_thing_type)
        """

    def create_topic_rule(
        self, **kwargs: Unpack[CreateTopicRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_topic_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_topic_rule)
        """

    def create_topic_rule_destination(
        self, **kwargs: Unpack[CreateTopicRuleDestinationRequestRequestTypeDef]
    ) -> CreateTopicRuleDestinationResponseTypeDef:
        """
        Creates a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_topic_rule_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_topic_rule_destination)
        """

    def delete_account_audit_configuration(
        self, **kwargs: Unpack[DeleteAccountAuditConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Restores the default settings for Device Defender audits for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_account_audit_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_account_audit_configuration)
        """

    def delete_audit_suppression(
        self, **kwargs: Unpack[DeleteAuditSuppressionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Device Defender audit suppression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_audit_suppression.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_audit_suppression)
        """

    def delete_authorizer(
        self, **kwargs: Unpack[DeleteAuthorizerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_authorizer)
        """

    def delete_billing_group(
        self, **kwargs: Unpack[DeleteBillingGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_billing_group)
        """

    def delete_ca_certificate(
        self, **kwargs: Unpack[DeleteCACertificateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a registered CA certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_ca_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_ca_certificate)
        """

    def delete_certificate(
        self, **kwargs: Unpack[DeleteCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_certificate)
        """

    def delete_certificate_provider(
        self, **kwargs: Unpack[DeleteCertificateProviderRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a certificate provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_certificate_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_certificate_provider)
        """

    def delete_command(
        self, **kwargs: Unpack[DeleteCommandRequestRequestTypeDef]
    ) -> DeleteCommandResponseTypeDef:
        """
        Delete a command resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_command.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_command)
        """

    def delete_command_execution(
        self, **kwargs: Unpack[DeleteCommandExecutionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete a command execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_command_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_command_execution)
        """

    def delete_custom_metric(
        self, **kwargs: Unpack[DeleteCustomMetricRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Device Defender detect custom metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_custom_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_custom_metric)
        """

    def delete_dimension(
        self, **kwargs: Unpack[DeleteDimensionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified dimension from your Amazon Web Services accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_dimension.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_dimension)
        """

    def delete_domain_configuration(
        self, **kwargs: Unpack[DeleteDomainConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified domain configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_domain_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_domain_configuration)
        """

    def delete_dynamic_thing_group(
        self, **kwargs: Unpack[DeleteDynamicThingGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a dynamic thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_dynamic_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_dynamic_thing_group)
        """

    def delete_fleet_metric(
        self, **kwargs: Unpack[DeleteFleetMetricRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified fleet metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_fleet_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_fleet_metric)
        """

    def delete_job(
        self, **kwargs: Unpack[DeleteJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a job and its related job executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_job)
        """

    def delete_job_execution(
        self, **kwargs: Unpack[DeleteJobExecutionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a job execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_job_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_job_execution)
        """

    def delete_job_template(
        self, **kwargs: Unpack[DeleteJobTemplateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_job_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_job_template)
        """

    def delete_mitigation_action(
        self, **kwargs: Unpack[DeleteMitigationActionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a defined mitigation action from your Amazon Web Services accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_mitigation_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_mitigation_action)
        """

    def delete_ota_update(
        self, **kwargs: Unpack[DeleteOTAUpdateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an OTA update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_ota_update.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_ota_update)
        """

    def delete_package(
        self, **kwargs: Unpack[DeletePackageRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specific version from a software package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_package)
        """

    def delete_package_version(
        self, **kwargs: Unpack[DeletePackageVersionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specific version from a software package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_package_version)
        """

    def delete_policy(
        self, **kwargs: Unpack[DeletePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_policy)
        """

    def delete_policy_version(
        self, **kwargs: Unpack[DeletePolicyVersionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified version of the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_policy_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_policy_version)
        """

    def delete_provisioning_template(
        self, **kwargs: Unpack[DeleteProvisioningTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_provisioning_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_provisioning_template)
        """

    def delete_provisioning_template_version(
        self, **kwargs: Unpack[DeleteProvisioningTemplateVersionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a provisioning template version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_provisioning_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_provisioning_template_version)
        """

    def delete_registration_code(self) -> Dict[str, Any]:
        """
        Deletes a CA certificate registration code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_registration_code.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_registration_code)
        """

    def delete_role_alias(
        self, **kwargs: Unpack[DeleteRoleAliasRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a role alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_role_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_role_alias)
        """

    def delete_scheduled_audit(
        self, **kwargs: Unpack[DeleteScheduledAuditRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a scheduled audit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_scheduled_audit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_scheduled_audit)
        """

    def delete_security_profile(
        self, **kwargs: Unpack[DeleteSecurityProfileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_security_profile)
        """

    def delete_stream(self, **kwargs: Unpack[DeleteStreamRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_stream)
        """

    def delete_thing(self, **kwargs: Unpack[DeleteThingRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_thing)
        """

    def delete_thing_group(
        self, **kwargs: Unpack[DeleteThingGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_thing_group)
        """

    def delete_thing_type(
        self, **kwargs: Unpack[DeleteThingTypeRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_thing_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_thing_type)
        """

    def delete_topic_rule(
        self, **kwargs: Unpack[DeleteTopicRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_topic_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_topic_rule)
        """

    def delete_topic_rule_destination(
        self, **kwargs: Unpack[DeleteTopicRuleDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_topic_rule_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_topic_rule_destination)
        """

    def delete_v2_logging_level(
        self, **kwargs: Unpack[DeleteV2LoggingLevelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a logging level.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_v2_logging_level.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_v2_logging_level)
        """

    def deprecate_thing_type(
        self, **kwargs: Unpack[DeprecateThingTypeRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deprecates a thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/deprecate_thing_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#deprecate_thing_type)
        """

    def describe_account_audit_configuration(
        self,
    ) -> DescribeAccountAuditConfigurationResponseTypeDef:
        """
        Gets information about the Device Defender audit settings for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_account_audit_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_account_audit_configuration)
        """

    def describe_audit_finding(
        self, **kwargs: Unpack[DescribeAuditFindingRequestRequestTypeDef]
    ) -> DescribeAuditFindingResponseTypeDef:
        """
        Gets information about a single audit finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_audit_finding.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_audit_finding)
        """

    def describe_audit_mitigation_actions_task(
        self, **kwargs: Unpack[DescribeAuditMitigationActionsTaskRequestRequestTypeDef]
    ) -> DescribeAuditMitigationActionsTaskResponseTypeDef:
        """
        Gets information about an audit mitigation task that is used to apply
        mitigation actions to a set of audit findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_audit_mitigation_actions_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_audit_mitigation_actions_task)
        """

    def describe_audit_suppression(
        self, **kwargs: Unpack[DescribeAuditSuppressionRequestRequestTypeDef]
    ) -> DescribeAuditSuppressionResponseTypeDef:
        """
        Gets information about a Device Defender audit suppression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_audit_suppression.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_audit_suppression)
        """

    def describe_audit_task(
        self, **kwargs: Unpack[DescribeAuditTaskRequestRequestTypeDef]
    ) -> DescribeAuditTaskResponseTypeDef:
        """
        Gets information about a Device Defender audit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_audit_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_audit_task)
        """

    def describe_authorizer(
        self, **kwargs: Unpack[DescribeAuthorizerRequestRequestTypeDef]
    ) -> DescribeAuthorizerResponseTypeDef:
        """
        Describes an authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_authorizer)
        """

    def describe_billing_group(
        self, **kwargs: Unpack[DescribeBillingGroupRequestRequestTypeDef]
    ) -> DescribeBillingGroupResponseTypeDef:
        """
        Returns information about a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_billing_group)
        """

    def describe_ca_certificate(
        self, **kwargs: Unpack[DescribeCACertificateRequestRequestTypeDef]
    ) -> DescribeCACertificateResponseTypeDef:
        """
        Describes a registered CA certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_ca_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_ca_certificate)
        """

    def describe_certificate(
        self, **kwargs: Unpack[DescribeCertificateRequestRequestTypeDef]
    ) -> DescribeCertificateResponseTypeDef:
        """
        Gets information about the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_certificate)
        """

    def describe_certificate_provider(
        self, **kwargs: Unpack[DescribeCertificateProviderRequestRequestTypeDef]
    ) -> DescribeCertificateProviderResponseTypeDef:
        """
        Describes a certificate provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_certificate_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_certificate_provider)
        """

    def describe_custom_metric(
        self, **kwargs: Unpack[DescribeCustomMetricRequestRequestTypeDef]
    ) -> DescribeCustomMetricResponseTypeDef:
        """
        Gets information about a Device Defender detect custom metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_custom_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_custom_metric)
        """

    def describe_default_authorizer(self) -> DescribeDefaultAuthorizerResponseTypeDef:
        """
        Describes the default authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_default_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_default_authorizer)
        """

    def describe_detect_mitigation_actions_task(
        self, **kwargs: Unpack[DescribeDetectMitigationActionsTaskRequestRequestTypeDef]
    ) -> DescribeDetectMitigationActionsTaskResponseTypeDef:
        """
        Gets information about a Device Defender ML Detect mitigation action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_detect_mitigation_actions_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_detect_mitigation_actions_task)
        """

    def describe_dimension(
        self, **kwargs: Unpack[DescribeDimensionRequestRequestTypeDef]
    ) -> DescribeDimensionResponseTypeDef:
        """
        Provides details about a dimension that is defined in your Amazon Web Services
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_dimension.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_dimension)
        """

    def describe_domain_configuration(
        self, **kwargs: Unpack[DescribeDomainConfigurationRequestRequestTypeDef]
    ) -> DescribeDomainConfigurationResponseTypeDef:
        """
        Gets summary information about a domain configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_domain_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_domain_configuration)
        """

    def describe_endpoint(
        self, **kwargs: Unpack[DescribeEndpointRequestRequestTypeDef]
    ) -> DescribeEndpointResponseTypeDef:
        """
        Returns or creates a unique endpoint specific to the Amazon Web Services
        account making the call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_endpoint)
        """

    def describe_event_configurations(self) -> DescribeEventConfigurationsResponseTypeDef:
        """
        Describes event configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_event_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_event_configurations)
        """

    def describe_fleet_metric(
        self, **kwargs: Unpack[DescribeFleetMetricRequestRequestTypeDef]
    ) -> DescribeFleetMetricResponseTypeDef:
        """
        Gets information about the specified fleet metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_fleet_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_fleet_metric)
        """

    def describe_index(
        self, **kwargs: Unpack[DescribeIndexRequestRequestTypeDef]
    ) -> DescribeIndexResponseTypeDef:
        """
        Describes a search index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_index.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_index)
        """

    def describe_job(
        self, **kwargs: Unpack[DescribeJobRequestRequestTypeDef]
    ) -> DescribeJobResponseTypeDef:
        """
        Describes a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_job)
        """

    def describe_job_execution(
        self, **kwargs: Unpack[DescribeJobExecutionRequestRequestTypeDef]
    ) -> DescribeJobExecutionResponseTypeDef:
        """
        Describes a job execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_job_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_job_execution)
        """

    def describe_job_template(
        self, **kwargs: Unpack[DescribeJobTemplateRequestRequestTypeDef]
    ) -> DescribeJobTemplateResponseTypeDef:
        """
        Returns information about a job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_job_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_job_template)
        """

    def describe_managed_job_template(
        self, **kwargs: Unpack[DescribeManagedJobTemplateRequestRequestTypeDef]
    ) -> DescribeManagedJobTemplateResponseTypeDef:
        """
        View details of a managed job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_managed_job_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_managed_job_template)
        """

    def describe_mitigation_action(
        self, **kwargs: Unpack[DescribeMitigationActionRequestRequestTypeDef]
    ) -> DescribeMitigationActionResponseTypeDef:
        """
        Gets information about a mitigation action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_mitigation_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_mitigation_action)
        """

    def describe_provisioning_template(
        self, **kwargs: Unpack[DescribeProvisioningTemplateRequestRequestTypeDef]
    ) -> DescribeProvisioningTemplateResponseTypeDef:
        """
        Returns information about a provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_provisioning_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_provisioning_template)
        """

    def describe_provisioning_template_version(
        self, **kwargs: Unpack[DescribeProvisioningTemplateVersionRequestRequestTypeDef]
    ) -> DescribeProvisioningTemplateVersionResponseTypeDef:
        """
        Returns information about a provisioning template version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_provisioning_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_provisioning_template_version)
        """

    def describe_role_alias(
        self, **kwargs: Unpack[DescribeRoleAliasRequestRequestTypeDef]
    ) -> DescribeRoleAliasResponseTypeDef:
        """
        Describes a role alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_role_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_role_alias)
        """

    def describe_scheduled_audit(
        self, **kwargs: Unpack[DescribeScheduledAuditRequestRequestTypeDef]
    ) -> DescribeScheduledAuditResponseTypeDef:
        """
        Gets information about a scheduled audit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_scheduled_audit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_scheduled_audit)
        """

    def describe_security_profile(
        self, **kwargs: Unpack[DescribeSecurityProfileRequestRequestTypeDef]
    ) -> DescribeSecurityProfileResponseTypeDef:
        """
        Gets information about a Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_security_profile)
        """

    def describe_stream(
        self, **kwargs: Unpack[DescribeStreamRequestRequestTypeDef]
    ) -> DescribeStreamResponseTypeDef:
        """
        Gets information about a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_stream)
        """

    def describe_thing(
        self, **kwargs: Unpack[DescribeThingRequestRequestTypeDef]
    ) -> DescribeThingResponseTypeDef:
        """
        Gets information about the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_thing)
        """

    def describe_thing_group(
        self, **kwargs: Unpack[DescribeThingGroupRequestRequestTypeDef]
    ) -> DescribeThingGroupResponseTypeDef:
        """
        Describe a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_thing_group)
        """

    def describe_thing_registration_task(
        self, **kwargs: Unpack[DescribeThingRegistrationTaskRequestRequestTypeDef]
    ) -> DescribeThingRegistrationTaskResponseTypeDef:
        """
        Describes a bulk thing provisioning task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_thing_registration_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_thing_registration_task)
        """

    def describe_thing_type(
        self, **kwargs: Unpack[DescribeThingTypeRequestRequestTypeDef]
    ) -> DescribeThingTypeResponseTypeDef:
        """
        Gets information about the specified thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_thing_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_thing_type)
        """

    def detach_policy(
        self, **kwargs: Unpack[DetachPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Detaches a policy from the specified target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/detach_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#detach_policy)
        """

    def detach_principal_policy(
        self, **kwargs: Unpack[DetachPrincipalPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified policy from the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/detach_principal_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#detach_principal_policy)
        """

    def detach_security_profile(
        self, **kwargs: Unpack[DetachSecurityProfileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a Device Defender security profile from a thing group or from
        this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/detach_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#detach_security_profile)
        """

    def detach_thing_principal(
        self, **kwargs: Unpack[DetachThingPrincipalRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Detaches the specified principal from the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/detach_thing_principal.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#detach_thing_principal)
        """

    def disable_topic_rule(
        self, **kwargs: Unpack[DisableTopicRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/disable_topic_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#disable_topic_rule)
        """

    def disassociate_sbom_from_package_version(
        self, **kwargs: Unpack[DisassociateSbomFromPackageVersionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the selected software bill of materials (SBOM) from a specific
        software package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/disassociate_sbom_from_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#disassociate_sbom_from_package_version)
        """

    def enable_topic_rule(
        self, **kwargs: Unpack[EnableTopicRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/enable_topic_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#enable_topic_rule)
        """

    def get_behavior_model_training_summaries(
        self, **kwargs: Unpack[GetBehaviorModelTrainingSummariesRequestRequestTypeDef]
    ) -> GetBehaviorModelTrainingSummariesResponseTypeDef:
        """
        Returns a Device Defender's ML Detect Security Profile training model's status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_behavior_model_training_summaries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_behavior_model_training_summaries)
        """

    def get_buckets_aggregation(
        self, **kwargs: Unpack[GetBucketsAggregationRequestRequestTypeDef]
    ) -> GetBucketsAggregationResponseTypeDef:
        """
        Aggregates on indexed data with search queries pertaining to particular fields.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_buckets_aggregation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_buckets_aggregation)
        """

    def get_cardinality(
        self, **kwargs: Unpack[GetCardinalityRequestRequestTypeDef]
    ) -> GetCardinalityResponseTypeDef:
        """
        Returns the approximate count of unique values that match the query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_cardinality.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_cardinality)
        """

    def get_command(
        self, **kwargs: Unpack[GetCommandRequestRequestTypeDef]
    ) -> GetCommandResponseTypeDef:
        """
        Gets information about the specified command.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_command.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_command)
        """

    def get_command_execution(
        self, **kwargs: Unpack[GetCommandExecutionRequestRequestTypeDef]
    ) -> GetCommandExecutionResponseTypeDef:
        """
        Gets information about the specific command execution on a single device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_command_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_command_execution)
        """

    def get_effective_policies(
        self, **kwargs: Unpack[GetEffectivePoliciesRequestRequestTypeDef]
    ) -> GetEffectivePoliciesResponseTypeDef:
        """
        Gets a list of the policies that have an effect on the authorization behavior
        of the specified device when it connects to the IoT device gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_effective_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_effective_policies)
        """

    def get_indexing_configuration(self) -> GetIndexingConfigurationResponseTypeDef:
        """
        Gets the indexing configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_indexing_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_indexing_configuration)
        """

    def get_job_document(
        self, **kwargs: Unpack[GetJobDocumentRequestRequestTypeDef]
    ) -> GetJobDocumentResponseTypeDef:
        """
        Gets a job document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_job_document.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_job_document)
        """

    def get_logging_options(self) -> GetLoggingOptionsResponseTypeDef:
        """
        Gets the logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_logging_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_logging_options)
        """

    def get_ota_update(
        self, **kwargs: Unpack[GetOTAUpdateRequestRequestTypeDef]
    ) -> GetOTAUpdateResponseTypeDef:
        """
        Gets an OTA update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_ota_update.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_ota_update)
        """

    def get_package(
        self, **kwargs: Unpack[GetPackageRequestRequestTypeDef]
    ) -> GetPackageResponseTypeDef:
        """
        Gets information about the specified software package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_package)
        """

    def get_package_configuration(self) -> GetPackageConfigurationResponseTypeDef:
        """
        Gets information about the specified software package's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_package_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_package_configuration)
        """

    def get_package_version(
        self, **kwargs: Unpack[GetPackageVersionRequestRequestTypeDef]
    ) -> GetPackageVersionResponseTypeDef:
        """
        Gets information about the specified package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_package_version)
        """

    def get_percentiles(
        self, **kwargs: Unpack[GetPercentilesRequestRequestTypeDef]
    ) -> GetPercentilesResponseTypeDef:
        """
        Groups the aggregated values that match the query into percentile groupings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_percentiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_percentiles)
        """

    def get_policy(
        self, **kwargs: Unpack[GetPolicyRequestRequestTypeDef]
    ) -> GetPolicyResponseTypeDef:
        """
        Gets information about the specified policy with the policy document of the
        default version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_policy)
        """

    def get_policy_version(
        self, **kwargs: Unpack[GetPolicyVersionRequestRequestTypeDef]
    ) -> GetPolicyVersionResponseTypeDef:
        """
        Gets information about the specified policy version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_policy_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_policy_version)
        """

    def get_registration_code(self) -> GetRegistrationCodeResponseTypeDef:
        """
        Gets a registration code used to register a CA certificate with IoT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_registration_code.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_registration_code)
        """

    def get_statistics(
        self, **kwargs: Unpack[GetStatisticsRequestRequestTypeDef]
    ) -> GetStatisticsResponseTypeDef:
        """
        Returns the count, average, sum, minimum, maximum, sum of squares, variance,
        and standard deviation for the specified aggregated field.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_statistics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_statistics)
        """

    def get_topic_rule(
        self, **kwargs: Unpack[GetTopicRuleRequestRequestTypeDef]
    ) -> GetTopicRuleResponseTypeDef:
        """
        Gets information about the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_topic_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_topic_rule)
        """

    def get_topic_rule_destination(
        self, **kwargs: Unpack[GetTopicRuleDestinationRequestRequestTypeDef]
    ) -> GetTopicRuleDestinationResponseTypeDef:
        """
        Gets information about a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_topic_rule_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_topic_rule_destination)
        """

    def get_v2_logging_options(self) -> GetV2LoggingOptionsResponseTypeDef:
        """
        Gets the fine grained logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_v2_logging_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_v2_logging_options)
        """

    def list_active_violations(
        self, **kwargs: Unpack[ListActiveViolationsRequestRequestTypeDef]
    ) -> ListActiveViolationsResponseTypeDef:
        """
        Lists the active violations for a given Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_active_violations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_active_violations)
        """

    def list_attached_policies(
        self, **kwargs: Unpack[ListAttachedPoliciesRequestRequestTypeDef]
    ) -> ListAttachedPoliciesResponseTypeDef:
        """
        Lists the policies attached to the specified thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_attached_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_attached_policies)
        """

    def list_audit_findings(
        self, **kwargs: Unpack[ListAuditFindingsRequestRequestTypeDef]
    ) -> ListAuditFindingsResponseTypeDef:
        """
        Lists the findings (results) of a Device Defender audit or of the audits
        performed during a specified time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_audit_findings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_audit_findings)
        """

    def list_audit_mitigation_actions_executions(
        self, **kwargs: Unpack[ListAuditMitigationActionsExecutionsRequestRequestTypeDef]
    ) -> ListAuditMitigationActionsExecutionsResponseTypeDef:
        """
        Gets the status of audit mitigation action tasks that were executed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_audit_mitigation_actions_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_audit_mitigation_actions_executions)
        """

    def list_audit_mitigation_actions_tasks(
        self, **kwargs: Unpack[ListAuditMitigationActionsTasksRequestRequestTypeDef]
    ) -> ListAuditMitigationActionsTasksResponseTypeDef:
        """
        Gets a list of audit mitigation action tasks that match the specified filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_audit_mitigation_actions_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_audit_mitigation_actions_tasks)
        """

    def list_audit_suppressions(
        self, **kwargs: Unpack[ListAuditSuppressionsRequestRequestTypeDef]
    ) -> ListAuditSuppressionsResponseTypeDef:
        """
        Lists your Device Defender audit listings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_audit_suppressions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_audit_suppressions)
        """

    def list_audit_tasks(
        self, **kwargs: Unpack[ListAuditTasksRequestRequestTypeDef]
    ) -> ListAuditTasksResponseTypeDef:
        """
        Lists the Device Defender audits that have been performed during a given time
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_audit_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_audit_tasks)
        """

    def list_authorizers(
        self, **kwargs: Unpack[ListAuthorizersRequestRequestTypeDef]
    ) -> ListAuthorizersResponseTypeDef:
        """
        Lists the authorizers registered in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_authorizers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_authorizers)
        """

    def list_billing_groups(
        self, **kwargs: Unpack[ListBillingGroupsRequestRequestTypeDef]
    ) -> ListBillingGroupsResponseTypeDef:
        """
        Lists the billing groups you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_billing_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_billing_groups)
        """

    def list_ca_certificates(
        self, **kwargs: Unpack[ListCACertificatesRequestRequestTypeDef]
    ) -> ListCACertificatesResponseTypeDef:
        """
        Lists the CA certificates registered for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_ca_certificates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_ca_certificates)
        """

    def list_certificate_providers(
        self, **kwargs: Unpack[ListCertificateProvidersRequestRequestTypeDef]
    ) -> ListCertificateProvidersResponseTypeDef:
        """
        Lists all your certificate providers in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_certificate_providers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_certificate_providers)
        """

    def list_certificates(
        self, **kwargs: Unpack[ListCertificatesRequestRequestTypeDef]
    ) -> ListCertificatesResponseTypeDef:
        """
        Lists the certificates registered in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_certificates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_certificates)
        """

    def list_certificates_by_ca(
        self, **kwargs: Unpack[ListCertificatesByCARequestRequestTypeDef]
    ) -> ListCertificatesByCAResponseTypeDef:
        """
        List the device certificates signed by the specified CA certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_certificates_by_ca.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_certificates_by_ca)
        """

    def list_command_executions(
        self, **kwargs: Unpack[ListCommandExecutionsRequestRequestTypeDef]
    ) -> ListCommandExecutionsResponseTypeDef:
        """
        List all command executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_command_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_command_executions)
        """

    def list_commands(
        self, **kwargs: Unpack[ListCommandsRequestRequestTypeDef]
    ) -> ListCommandsResponseTypeDef:
        """
        List all commands in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_commands.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_commands)
        """

    def list_custom_metrics(
        self, **kwargs: Unpack[ListCustomMetricsRequestRequestTypeDef]
    ) -> ListCustomMetricsResponseTypeDef:
        """
        Lists your Device Defender detect custom metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_custom_metrics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_custom_metrics)
        """

    def list_detect_mitigation_actions_executions(
        self, **kwargs: Unpack[ListDetectMitigationActionsExecutionsRequestRequestTypeDef]
    ) -> ListDetectMitigationActionsExecutionsResponseTypeDef:
        """
        Lists mitigation actions executions for a Device Defender ML Detect Security
        Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_detect_mitigation_actions_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_detect_mitigation_actions_executions)
        """

    def list_detect_mitigation_actions_tasks(
        self, **kwargs: Unpack[ListDetectMitigationActionsTasksRequestRequestTypeDef]
    ) -> ListDetectMitigationActionsTasksResponseTypeDef:
        """
        List of Device Defender ML Detect mitigation actions tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_detect_mitigation_actions_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_detect_mitigation_actions_tasks)
        """

    def list_dimensions(
        self, **kwargs: Unpack[ListDimensionsRequestRequestTypeDef]
    ) -> ListDimensionsResponseTypeDef:
        """
        List the set of dimensions that are defined for your Amazon Web Services
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_dimensions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_dimensions)
        """

    def list_domain_configurations(
        self, **kwargs: Unpack[ListDomainConfigurationsRequestRequestTypeDef]
    ) -> ListDomainConfigurationsResponseTypeDef:
        """
        Gets a list of domain configurations for the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_domain_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_domain_configurations)
        """

    def list_fleet_metrics(
        self, **kwargs: Unpack[ListFleetMetricsRequestRequestTypeDef]
    ) -> ListFleetMetricsResponseTypeDef:
        """
        Lists all your fleet metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_fleet_metrics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_fleet_metrics)
        """

    def list_indices(
        self, **kwargs: Unpack[ListIndicesRequestRequestTypeDef]
    ) -> ListIndicesResponseTypeDef:
        """
        Lists the search indices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_indices.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_indices)
        """

    def list_job_executions_for_job(
        self, **kwargs: Unpack[ListJobExecutionsForJobRequestRequestTypeDef]
    ) -> ListJobExecutionsForJobResponseTypeDef:
        """
        Lists the job executions for a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_job_executions_for_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_job_executions_for_job)
        """

    def list_job_executions_for_thing(
        self, **kwargs: Unpack[ListJobExecutionsForThingRequestRequestTypeDef]
    ) -> ListJobExecutionsForThingResponseTypeDef:
        """
        Lists the job executions for the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_job_executions_for_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_job_executions_for_thing)
        """

    def list_job_templates(
        self, **kwargs: Unpack[ListJobTemplatesRequestRequestTypeDef]
    ) -> ListJobTemplatesResponseTypeDef:
        """
        Returns a list of job templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_job_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_job_templates)
        """

    def list_jobs(self, **kwargs: Unpack[ListJobsRequestRequestTypeDef]) -> ListJobsResponseTypeDef:
        """
        Lists jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_jobs)
        """

    def list_managed_job_templates(
        self, **kwargs: Unpack[ListManagedJobTemplatesRequestRequestTypeDef]
    ) -> ListManagedJobTemplatesResponseTypeDef:
        """
        Returns a list of managed job templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_managed_job_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_managed_job_templates)
        """

    def list_metric_values(
        self, **kwargs: Unpack[ListMetricValuesRequestRequestTypeDef]
    ) -> ListMetricValuesResponseTypeDef:
        """
        Lists the values reported for an IoT Device Defender metric (device-side
        metric, cloud-side metric, or custom metric) by the given thing during the
        specified time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_metric_values.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_metric_values)
        """

    def list_mitigation_actions(
        self, **kwargs: Unpack[ListMitigationActionsRequestRequestTypeDef]
    ) -> ListMitigationActionsResponseTypeDef:
        """
        Gets a list of all mitigation actions that match the specified filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_mitigation_actions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_mitigation_actions)
        """

    def list_ota_updates(
        self, **kwargs: Unpack[ListOTAUpdatesRequestRequestTypeDef]
    ) -> ListOTAUpdatesResponseTypeDef:
        """
        Lists OTA updates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_ota_updates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_ota_updates)
        """

    def list_outgoing_certificates(
        self, **kwargs: Unpack[ListOutgoingCertificatesRequestRequestTypeDef]
    ) -> ListOutgoingCertificatesResponseTypeDef:
        """
        Lists certificates that are being transferred but not yet accepted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_outgoing_certificates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_outgoing_certificates)
        """

    def list_package_versions(
        self, **kwargs: Unpack[ListPackageVersionsRequestRequestTypeDef]
    ) -> ListPackageVersionsResponseTypeDef:
        """
        Lists the software package versions associated to the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_package_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_package_versions)
        """

    def list_packages(
        self, **kwargs: Unpack[ListPackagesRequestRequestTypeDef]
    ) -> ListPackagesResponseTypeDef:
        """
        Lists the software packages associated to the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_packages.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_packages)
        """

    def list_policies(
        self, **kwargs: Unpack[ListPoliciesRequestRequestTypeDef]
    ) -> ListPoliciesResponseTypeDef:
        """
        Lists your policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_policies)
        """

    def list_policy_principals(
        self, **kwargs: Unpack[ListPolicyPrincipalsRequestRequestTypeDef]
    ) -> ListPolicyPrincipalsResponseTypeDef:
        """
        Lists the principals associated with the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_policy_principals.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_policy_principals)
        """

    def list_policy_versions(
        self, **kwargs: Unpack[ListPolicyVersionsRequestRequestTypeDef]
    ) -> ListPolicyVersionsResponseTypeDef:
        """
        Lists the versions of the specified policy and identifies the default version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_policy_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_policy_versions)
        """

    def list_principal_policies(
        self, **kwargs: Unpack[ListPrincipalPoliciesRequestRequestTypeDef]
    ) -> ListPrincipalPoliciesResponseTypeDef:
        """
        Lists the policies attached to the specified principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_principal_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_principal_policies)
        """

    def list_principal_things(
        self, **kwargs: Unpack[ListPrincipalThingsRequestRequestTypeDef]
    ) -> ListPrincipalThingsResponseTypeDef:
        """
        Lists the things associated with the specified principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_principal_things.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_principal_things)
        """

    def list_principal_things_v2(
        self, **kwargs: Unpack[ListPrincipalThingsV2RequestRequestTypeDef]
    ) -> ListPrincipalThingsV2ResponseTypeDef:
        """
        Lists the things associated with the specified principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_principal_things_v2.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_principal_things_v2)
        """

    def list_provisioning_template_versions(
        self, **kwargs: Unpack[ListProvisioningTemplateVersionsRequestRequestTypeDef]
    ) -> ListProvisioningTemplateVersionsResponseTypeDef:
        """
        A list of provisioning template versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_provisioning_template_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_provisioning_template_versions)
        """

    def list_provisioning_templates(
        self, **kwargs: Unpack[ListProvisioningTemplatesRequestRequestTypeDef]
    ) -> ListProvisioningTemplatesResponseTypeDef:
        """
        Lists the provisioning templates in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_provisioning_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_provisioning_templates)
        """

    def list_related_resources_for_audit_finding(
        self, **kwargs: Unpack[ListRelatedResourcesForAuditFindingRequestRequestTypeDef]
    ) -> ListRelatedResourcesForAuditFindingResponseTypeDef:
        """
        The related resources of an Audit finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_related_resources_for_audit_finding.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_related_resources_for_audit_finding)
        """

    def list_role_aliases(
        self, **kwargs: Unpack[ListRoleAliasesRequestRequestTypeDef]
    ) -> ListRoleAliasesResponseTypeDef:
        """
        Lists the role aliases registered in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_role_aliases.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_role_aliases)
        """

    def list_sbom_validation_results(
        self, **kwargs: Unpack[ListSbomValidationResultsRequestRequestTypeDef]
    ) -> ListSbomValidationResultsResponseTypeDef:
        """
        The validation results for all software bill of materials (SBOM) attached to a
        specific software package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_sbom_validation_results.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_sbom_validation_results)
        """

    def list_scheduled_audits(
        self, **kwargs: Unpack[ListScheduledAuditsRequestRequestTypeDef]
    ) -> ListScheduledAuditsResponseTypeDef:
        """
        Lists all of your scheduled audits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_scheduled_audits.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_scheduled_audits)
        """

    def list_security_profiles(
        self, **kwargs: Unpack[ListSecurityProfilesRequestRequestTypeDef]
    ) -> ListSecurityProfilesResponseTypeDef:
        """
        Lists the Device Defender security profiles you've created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_security_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_security_profiles)
        """

    def list_security_profiles_for_target(
        self, **kwargs: Unpack[ListSecurityProfilesForTargetRequestRequestTypeDef]
    ) -> ListSecurityProfilesForTargetResponseTypeDef:
        """
        Lists the Device Defender security profiles attached to a target (thing group).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_security_profiles_for_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_security_profiles_for_target)
        """

    def list_streams(
        self, **kwargs: Unpack[ListStreamsRequestRequestTypeDef]
    ) -> ListStreamsResponseTypeDef:
        """
        Lists all of the streams in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_streams.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_streams)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags (metadata) you have assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_tags_for_resource)
        """

    def list_targets_for_policy(
        self, **kwargs: Unpack[ListTargetsForPolicyRequestRequestTypeDef]
    ) -> ListTargetsForPolicyResponseTypeDef:
        """
        List targets for the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_targets_for_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_targets_for_policy)
        """

    def list_targets_for_security_profile(
        self, **kwargs: Unpack[ListTargetsForSecurityProfileRequestRequestTypeDef]
    ) -> ListTargetsForSecurityProfileResponseTypeDef:
        """
        Lists the targets (thing groups) associated with a given Device Defender
        security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_targets_for_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_targets_for_security_profile)
        """

    def list_thing_groups(
        self, **kwargs: Unpack[ListThingGroupsRequestRequestTypeDef]
    ) -> ListThingGroupsResponseTypeDef:
        """
        List the thing groups in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_groups)
        """

    def list_thing_groups_for_thing(
        self, **kwargs: Unpack[ListThingGroupsForThingRequestRequestTypeDef]
    ) -> ListThingGroupsForThingResponseTypeDef:
        """
        List the thing groups to which the specified thing belongs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_groups_for_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_groups_for_thing)
        """

    def list_thing_principals(
        self, **kwargs: Unpack[ListThingPrincipalsRequestRequestTypeDef]
    ) -> ListThingPrincipalsResponseTypeDef:
        """
        Lists the principals associated with the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_principals.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_principals)
        """

    def list_thing_principals_v2(
        self, **kwargs: Unpack[ListThingPrincipalsV2RequestRequestTypeDef]
    ) -> ListThingPrincipalsV2ResponseTypeDef:
        """
        Lists the principals associated with the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_principals_v2.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_principals_v2)
        """

    def list_thing_registration_task_reports(
        self, **kwargs: Unpack[ListThingRegistrationTaskReportsRequestRequestTypeDef]
    ) -> ListThingRegistrationTaskReportsResponseTypeDef:
        """
        Information about the thing registration tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_registration_task_reports.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_registration_task_reports)
        """

    def list_thing_registration_tasks(
        self, **kwargs: Unpack[ListThingRegistrationTasksRequestRequestTypeDef]
    ) -> ListThingRegistrationTasksResponseTypeDef:
        """
        List bulk thing provisioning tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_registration_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_registration_tasks)
        """

    def list_thing_types(
        self, **kwargs: Unpack[ListThingTypesRequestRequestTypeDef]
    ) -> ListThingTypesResponseTypeDef:
        """
        Lists the existing thing types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_types)
        """

    def list_things(
        self, **kwargs: Unpack[ListThingsRequestRequestTypeDef]
    ) -> ListThingsResponseTypeDef:
        """
        Lists your things.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_things.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_things)
        """

    def list_things_in_billing_group(
        self, **kwargs: Unpack[ListThingsInBillingGroupRequestRequestTypeDef]
    ) -> ListThingsInBillingGroupResponseTypeDef:
        """
        Lists the things you have added to the given billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_things_in_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_things_in_billing_group)
        """

    def list_things_in_thing_group(
        self, **kwargs: Unpack[ListThingsInThingGroupRequestRequestTypeDef]
    ) -> ListThingsInThingGroupResponseTypeDef:
        """
        Lists the things in the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_things_in_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_things_in_thing_group)
        """

    def list_topic_rule_destinations(
        self, **kwargs: Unpack[ListTopicRuleDestinationsRequestRequestTypeDef]
    ) -> ListTopicRuleDestinationsResponseTypeDef:
        """
        Lists all the topic rule destinations in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_topic_rule_destinations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_topic_rule_destinations)
        """

    def list_topic_rules(
        self, **kwargs: Unpack[ListTopicRulesRequestRequestTypeDef]
    ) -> ListTopicRulesResponseTypeDef:
        """
        Lists the rules for the specific topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_topic_rules.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_topic_rules)
        """

    def list_v2_logging_levels(
        self, **kwargs: Unpack[ListV2LoggingLevelsRequestRequestTypeDef]
    ) -> ListV2LoggingLevelsResponseTypeDef:
        """
        Lists logging levels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_v2_logging_levels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_v2_logging_levels)
        """

    def list_violation_events(
        self, **kwargs: Unpack[ListViolationEventsRequestRequestTypeDef]
    ) -> ListViolationEventsResponseTypeDef:
        """
        Lists the Device Defender security profile violations discovered during the
        given time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_violation_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_violation_events)
        """

    def put_verification_state_on_violation(
        self, **kwargs: Unpack[PutVerificationStateOnViolationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Set a verification state and provide a description of that verification state
        on a violation (detect alarm).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/put_verification_state_on_violation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#put_verification_state_on_violation)
        """

    def register_ca_certificate(
        self, **kwargs: Unpack[RegisterCACertificateRequestRequestTypeDef]
    ) -> RegisterCACertificateResponseTypeDef:
        """
        Registers a CA certificate with Amazon Web Services IoT Core.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/register_ca_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#register_ca_certificate)
        """

    def register_certificate(
        self, **kwargs: Unpack[RegisterCertificateRequestRequestTypeDef]
    ) -> RegisterCertificateResponseTypeDef:
        """
        Registers a device certificate with IoT in the same <a
        href="https://docs.aws.amazon.com/iot/latest/apireference/API_CertificateDescription.html#iot-Type-CertificateDescription-certificateMode">certificate
        mode</a> as the signing CA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/register_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#register_certificate)
        """

    def register_certificate_without_ca(
        self, **kwargs: Unpack[RegisterCertificateWithoutCARequestRequestTypeDef]
    ) -> RegisterCertificateWithoutCAResponseTypeDef:
        """
        Register a certificate that does not have a certificate authority (CA).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/register_certificate_without_ca.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#register_certificate_without_ca)
        """

    def register_thing(
        self, **kwargs: Unpack[RegisterThingRequestRequestTypeDef]
    ) -> RegisterThingResponseTypeDef:
        """
        Provisions a thing in the device registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/register_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#register_thing)
        """

    def reject_certificate_transfer(
        self, **kwargs: Unpack[RejectCertificateTransferRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Rejects a pending certificate transfer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/reject_certificate_transfer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#reject_certificate_transfer)
        """

    def remove_thing_from_billing_group(
        self, **kwargs: Unpack[RemoveThingFromBillingGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the given thing from the billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/remove_thing_from_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#remove_thing_from_billing_group)
        """

    def remove_thing_from_thing_group(
        self, **kwargs: Unpack[RemoveThingFromThingGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove the specified thing from the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/remove_thing_from_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#remove_thing_from_thing_group)
        """

    def replace_topic_rule(
        self, **kwargs: Unpack[ReplaceTopicRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Replaces the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/replace_topic_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#replace_topic_rule)
        """

    def search_index(
        self, **kwargs: Unpack[SearchIndexRequestRequestTypeDef]
    ) -> SearchIndexResponseTypeDef:
        """
        The query search index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/search_index.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#search_index)
        """

    def set_default_authorizer(
        self, **kwargs: Unpack[SetDefaultAuthorizerRequestRequestTypeDef]
    ) -> SetDefaultAuthorizerResponseTypeDef:
        """
        Sets the default authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/set_default_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#set_default_authorizer)
        """

    def set_default_policy_version(
        self, **kwargs: Unpack[SetDefaultPolicyVersionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the specified version of the specified policy as the policy's default
        (operative) version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/set_default_policy_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#set_default_policy_version)
        """

    def set_logging_options(
        self, **kwargs: Unpack[SetLoggingOptionsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/set_logging_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#set_logging_options)
        """

    def set_v2_logging_level(
        self, **kwargs: Unpack[SetV2LoggingLevelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the logging level.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/set_v2_logging_level.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#set_v2_logging_level)
        """

    def set_v2_logging_options(
        self, **kwargs: Unpack[SetV2LoggingOptionsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the logging options for the V2 logging service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/set_v2_logging_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#set_v2_logging_options)
        """

    def start_audit_mitigation_actions_task(
        self, **kwargs: Unpack[StartAuditMitigationActionsTaskRequestRequestTypeDef]
    ) -> StartAuditMitigationActionsTaskResponseTypeDef:
        """
        Starts a task that applies a set of mitigation actions to the specified target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/start_audit_mitigation_actions_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#start_audit_mitigation_actions_task)
        """

    def start_detect_mitigation_actions_task(
        self, **kwargs: Unpack[StartDetectMitigationActionsTaskRequestRequestTypeDef]
    ) -> StartDetectMitigationActionsTaskResponseTypeDef:
        """
        Starts a Device Defender ML Detect mitigation actions task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/start_detect_mitigation_actions_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#start_detect_mitigation_actions_task)
        """

    def start_on_demand_audit_task(
        self, **kwargs: Unpack[StartOnDemandAuditTaskRequestRequestTypeDef]
    ) -> StartOnDemandAuditTaskResponseTypeDef:
        """
        Starts an on-demand Device Defender audit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/start_on_demand_audit_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#start_on_demand_audit_task)
        """

    def start_thing_registration_task(
        self, **kwargs: Unpack[StartThingRegistrationTaskRequestRequestTypeDef]
    ) -> StartThingRegistrationTaskResponseTypeDef:
        """
        Creates a bulk thing provisioning task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/start_thing_registration_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#start_thing_registration_task)
        """

    def stop_thing_registration_task(
        self, **kwargs: Unpack[StopThingRegistrationTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a bulk thing provisioning task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/stop_thing_registration_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#stop_thing_registration_task)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds to or modifies the tags of the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#tag_resource)
        """

    def test_authorization(
        self, **kwargs: Unpack[TestAuthorizationRequestRequestTypeDef]
    ) -> TestAuthorizationResponseTypeDef:
        """
        Tests if a specified principal is authorized to perform an IoT action on a
        specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/test_authorization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#test_authorization)
        """

    def test_invoke_authorizer(
        self, **kwargs: Unpack[TestInvokeAuthorizerRequestRequestTypeDef]
    ) -> TestInvokeAuthorizerResponseTypeDef:
        """
        Tests a custom authorization behavior by invoking a specified custom authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/test_invoke_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#test_invoke_authorizer)
        """

    def transfer_certificate(
        self, **kwargs: Unpack[TransferCertificateRequestRequestTypeDef]
    ) -> TransferCertificateResponseTypeDef:
        """
        Transfers the specified certificate to the specified Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/transfer_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#transfer_certificate)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the given tags (metadata) from the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#untag_resource)
        """

    def update_account_audit_configuration(
        self, **kwargs: Unpack[UpdateAccountAuditConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Configures or reconfigures the Device Defender audit settings for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_account_audit_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_account_audit_configuration)
        """

    def update_audit_suppression(
        self, **kwargs: Unpack[UpdateAuditSuppressionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a Device Defender audit suppression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_audit_suppression.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_audit_suppression)
        """

    def update_authorizer(
        self, **kwargs: Unpack[UpdateAuthorizerRequestRequestTypeDef]
    ) -> UpdateAuthorizerResponseTypeDef:
        """
        Updates an authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_authorizer)
        """

    def update_billing_group(
        self, **kwargs: Unpack[UpdateBillingGroupRequestRequestTypeDef]
    ) -> UpdateBillingGroupResponseTypeDef:
        """
        Updates information about the billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_billing_group)
        """

    def update_ca_certificate(
        self, **kwargs: Unpack[UpdateCACertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a registered CA certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_ca_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_ca_certificate)
        """

    def update_certificate(
        self, **kwargs: Unpack[UpdateCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the status of the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_certificate)
        """

    def update_certificate_provider(
        self, **kwargs: Unpack[UpdateCertificateProviderRequestRequestTypeDef]
    ) -> UpdateCertificateProviderResponseTypeDef:
        """
        Updates a certificate provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_certificate_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_certificate_provider)
        """

    def update_command(
        self, **kwargs: Unpack[UpdateCommandRequestRequestTypeDef]
    ) -> UpdateCommandResponseTypeDef:
        """
        Update information about a command or mark a command for deprecation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_command.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_command)
        """

    def update_custom_metric(
        self, **kwargs: Unpack[UpdateCustomMetricRequestRequestTypeDef]
    ) -> UpdateCustomMetricResponseTypeDef:
        """
        Updates a Device Defender detect custom metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_custom_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_custom_metric)
        """

    def update_dimension(
        self, **kwargs: Unpack[UpdateDimensionRequestRequestTypeDef]
    ) -> UpdateDimensionResponseTypeDef:
        """
        Updates the definition for a dimension.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_dimension.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_dimension)
        """

    def update_domain_configuration(
        self, **kwargs: Unpack[UpdateDomainConfigurationRequestRequestTypeDef]
    ) -> UpdateDomainConfigurationResponseTypeDef:
        """
        Updates values stored in the domain configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_domain_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_domain_configuration)
        """

    def update_dynamic_thing_group(
        self, **kwargs: Unpack[UpdateDynamicThingGroupRequestRequestTypeDef]
    ) -> UpdateDynamicThingGroupResponseTypeDef:
        """
        Updates a dynamic thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_dynamic_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_dynamic_thing_group)
        """

    def update_event_configurations(
        self, **kwargs: Unpack[UpdateEventConfigurationsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the event configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_event_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_event_configurations)
        """

    def update_fleet_metric(
        self, **kwargs: Unpack[UpdateFleetMetricRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the data for a fleet metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_fleet_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_fleet_metric)
        """

    def update_indexing_configuration(
        self, **kwargs: Unpack[UpdateIndexingConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the search configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_indexing_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_indexing_configuration)
        """

    def update_job(
        self, **kwargs: Unpack[UpdateJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates supported fields of the specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_job)
        """

    def update_mitigation_action(
        self, **kwargs: Unpack[UpdateMitigationActionRequestRequestTypeDef]
    ) -> UpdateMitigationActionResponseTypeDef:
        """
        Updates the definition for the specified mitigation action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_mitigation_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_mitigation_action)
        """

    def update_package(
        self, **kwargs: Unpack[UpdatePackageRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the supported fields for a specific software package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_package)
        """

    def update_package_configuration(
        self, **kwargs: Unpack[UpdatePackageConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the software package configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_package_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_package_configuration)
        """

    def update_package_version(
        self, **kwargs: Unpack[UpdatePackageVersionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the supported fields for a specific package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_package_version)
        """

    def update_provisioning_template(
        self, **kwargs: Unpack[UpdateProvisioningTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_provisioning_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_provisioning_template)
        """

    def update_role_alias(
        self, **kwargs: Unpack[UpdateRoleAliasRequestRequestTypeDef]
    ) -> UpdateRoleAliasResponseTypeDef:
        """
        Updates a role alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_role_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_role_alias)
        """

    def update_scheduled_audit(
        self, **kwargs: Unpack[UpdateScheduledAuditRequestRequestTypeDef]
    ) -> UpdateScheduledAuditResponseTypeDef:
        """
        Updates a scheduled audit, including which checks are performed and how often
        the audit takes place.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_scheduled_audit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_scheduled_audit)
        """

    def update_security_profile(
        self, **kwargs: Unpack[UpdateSecurityProfileRequestRequestTypeDef]
    ) -> UpdateSecurityProfileResponseTypeDef:
        """
        Updates a Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_security_profile)
        """

    def update_stream(
        self, **kwargs: Unpack[UpdateStreamRequestRequestTypeDef]
    ) -> UpdateStreamResponseTypeDef:
        """
        Updates an existing stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_stream)
        """

    def update_thing(self, **kwargs: Unpack[UpdateThingRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the data for a thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_thing)
        """

    def update_thing_group(
        self, **kwargs: Unpack[UpdateThingGroupRequestRequestTypeDef]
    ) -> UpdateThingGroupResponseTypeDef:
        """
        Update a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_thing_group)
        """

    def update_thing_groups_for_thing(
        self, **kwargs: Unpack[UpdateThingGroupsForThingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the groups to which the thing belongs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_thing_groups_for_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_thing_groups_for_thing)
        """

    def update_thing_type(
        self, **kwargs: Unpack[UpdateThingTypeRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_thing_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_thing_type)
        """

    def update_topic_rule_destination(
        self, **kwargs: Unpack[UpdateTopicRuleDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_topic_rule_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_topic_rule_destination)
        """

    def validate_security_profile_behaviors(
        self, **kwargs: Unpack[ValidateSecurityProfileBehaviorsRequestRequestTypeDef]
    ) -> ValidateSecurityProfileBehaviorsResponseTypeDef:
        """
        Validates a Device Defender security profile behaviors specification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/validate_security_profile_behaviors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#validate_security_profile_behaviors)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_behavior_model_training_summaries"]
    ) -> GetBehaviorModelTrainingSummariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_active_violations"]
    ) -> ListActiveViolationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_attached_policies"]
    ) -> ListAttachedPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audit_findings"]
    ) -> ListAuditFindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audit_mitigation_actions_executions"]
    ) -> ListAuditMitigationActionsExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audit_mitigation_actions_tasks"]
    ) -> ListAuditMitigationActionsTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audit_suppressions"]
    ) -> ListAuditSuppressionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_audit_tasks"]) -> ListAuditTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_authorizers"]
    ) -> ListAuthorizersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_billing_groups"]
    ) -> ListBillingGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ca_certificates"]
    ) -> ListCACertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_certificates_by_ca"]
    ) -> ListCertificatesByCAPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_certificates"]
    ) -> ListCertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_command_executions"]
    ) -> ListCommandExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_commands"]) -> ListCommandsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_metrics"]
    ) -> ListCustomMetricsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_detect_mitigation_actions_executions"]
    ) -> ListDetectMitigationActionsExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_detect_mitigation_actions_tasks"]
    ) -> ListDetectMitigationActionsTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_dimensions"]) -> ListDimensionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_domain_configurations"]
    ) -> ListDomainConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_fleet_metrics"]
    ) -> ListFleetMetricsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_indices"]) -> ListIndicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_job_executions_for_job"]
    ) -> ListJobExecutionsForJobPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_job_executions_for_thing"]
    ) -> ListJobExecutionsForThingPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_job_templates"]
    ) -> ListJobTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_managed_job_templates"]
    ) -> ListManagedJobTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_metric_values"]
    ) -> ListMetricValuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_mitigation_actions"]
    ) -> ListMitigationActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_ota_updates"]) -> ListOTAUpdatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_outgoing_certificates"]
    ) -> ListOutgoingCertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_package_versions"]
    ) -> ListPackageVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_packages"]) -> ListPackagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_policies"]) -> ListPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_policy_principals"]
    ) -> ListPolicyPrincipalsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_principal_policies"]
    ) -> ListPrincipalPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_principal_things"]
    ) -> ListPrincipalThingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_principal_things_v2"]
    ) -> ListPrincipalThingsV2Paginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provisioning_template_versions"]
    ) -> ListProvisioningTemplateVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provisioning_templates"]
    ) -> ListProvisioningTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_related_resources_for_audit_finding"]
    ) -> ListRelatedResourcesForAuditFindingPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_role_aliases"]
    ) -> ListRoleAliasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sbom_validation_results"]
    ) -> ListSbomValidationResultsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_scheduled_audits"]
    ) -> ListScheduledAuditsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_profiles_for_target"]
    ) -> ListSecurityProfilesForTargetPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_profiles"]
    ) -> ListSecurityProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_streams"]) -> ListStreamsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_targets_for_policy"]
    ) -> ListTargetsForPolicyPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_targets_for_security_profile"]
    ) -> ListTargetsForSecurityProfilePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_thing_groups_for_thing"]
    ) -> ListThingGroupsForThingPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_thing_groups"]
    ) -> ListThingGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_thing_principals"]
    ) -> ListThingPrincipalsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_thing_principals_v2"]
    ) -> ListThingPrincipalsV2Paginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_thing_registration_task_reports"]
    ) -> ListThingRegistrationTaskReportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_thing_registration_tasks"]
    ) -> ListThingRegistrationTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_thing_types"]) -> ListThingTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_things_in_billing_group"]
    ) -> ListThingsInBillingGroupPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_things_in_thing_group"]
    ) -> ListThingsInThingGroupPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_things"]) -> ListThingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_topic_rule_destinations"]
    ) -> ListTopicRuleDestinationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_topic_rules"]) -> ListTopicRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_v2_logging_levels"]
    ) -> ListV2LoggingLevelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_violation_events"]
    ) -> ListViolationEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """
