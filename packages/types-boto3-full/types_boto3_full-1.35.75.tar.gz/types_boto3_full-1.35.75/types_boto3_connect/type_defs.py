"""
Type annotations for connect service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connect/type_defs/)

Usage::

    ```python
    from types_boto3_connect.type_defs import ActionSummaryTypeDef

    data: ActionSummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    ActionTypeType,
    AgentAvailabilityTimerType,
    AgentStatusStateType,
    AgentStatusTypeType,
    AnsweringMachineDetectionStatusType,
    ArtifactStatusType,
    BehaviorTypeType,
    ChannelType,
    ChatEventTypeType,
    ContactFlowModuleStateType,
    ContactFlowModuleStatusType,
    ContactFlowStateType,
    ContactFlowStatusType,
    ContactFlowTypeType,
    ContactInitiationMethodType,
    ContactRecordingTypeType,
    ContactStateType,
    CurrentMetricNameType,
    DirectoryTypeType,
    EmailHeaderTypeType,
    EndpointTypeType,
    EvaluationFormQuestionTypeType,
    EvaluationFormScoringModeType,
    EvaluationFormScoringStatusType,
    EvaluationFormSingleSelectQuestionDisplayModeType,
    EvaluationFormVersionStatusType,
    EvaluationStatusType,
    EventSourceNameType,
    FailureReasonCodeType,
    FileStatusTypeType,
    FileUseCaseTypeType,
    FlowAssociationResourceTypeType,
    GroupingType,
    HierarchyGroupMatchTypeType,
    HistoricalMetricNameType,
    HoursOfOperationDaysType,
    InstanceAttributeTypeType,
    InstanceReplicationStatusType,
    InstanceStatusType,
    InstanceStorageResourceTypeType,
    IntegrationTypeType,
    IntervalPeriodType,
    LexVersionType,
    ListFlowAssociationResourceTypeType,
    MeetingFeatureStatusType,
    MonitorCapabilityType,
    NumberComparisonTypeType,
    NumericQuestionPropertyAutomationLabelType,
    OutboundMessageSourceTypeType,
    ParticipantRoleType,
    ParticipantTimerTypeType,
    PhoneNumberCountryCodeType,
    PhoneNumberTypeType,
    PhoneNumberWorkflowStatusType,
    PhoneTypeType,
    QueueStatusType,
    QueueTypeType,
    QuickConnectTypeType,
    RealTimeContactAnalysisOutputTypeType,
    RealTimeContactAnalysisPostContactSummaryFailureCodeType,
    RealTimeContactAnalysisPostContactSummaryStatusType,
    RealTimeContactAnalysisSegmentTypeType,
    RealTimeContactAnalysisSentimentLabelType,
    RealTimeContactAnalysisStatusType,
    RealTimeContactAnalysisSupportedChannelType,
    ReferenceStatusType,
    ReferenceTypeType,
    RehydrationTypeType,
    RoutingCriteriaStepStatusType,
    RulePublishStatusType,
    SearchContactsMatchTypeType,
    SearchContactsTimeRangeTypeType,
    SingleSelectQuestionRuleCategoryAutomationConditionType,
    SortableFieldNameType,
    SortOrderType,
    SourceTypeType,
    StatisticType,
    StorageTypeType,
    StringComparisonTypeType,
    TaskTemplateFieldTypeType,
    TaskTemplateStatusType,
    TimerEligibleParticipantRolesType,
    TrafficDistributionGroupStatusType,
    TrafficTypeType,
    UnitType,
    UseCaseTypeType,
    ViewStatusType,
    ViewTypeType,
    VocabularyLanguageCodeType,
    VocabularyStateType,
    VoiceRecordingTrackType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ActionSummaryTypeDef",
    "ActivateEvaluationFormRequestRequestTypeDef",
    "ActivateEvaluationFormResponseTypeDef",
    "AdditionalEmailRecipientsTypeDef",
    "AgentConfigOutputTypeDef",
    "AgentConfigTypeDef",
    "AgentContactReferenceTypeDef",
    "AgentHierarchyGroupTypeDef",
    "AgentHierarchyGroupsTypeDef",
    "AgentInfoTypeDef",
    "AgentQualityMetricsTypeDef",
    "AgentStatusReferenceTypeDef",
    "AgentStatusSearchCriteriaPaginatorTypeDef",
    "AgentStatusSearchCriteriaTypeDef",
    "AgentStatusSearchFilterTypeDef",
    "AgentStatusSummaryTypeDef",
    "AgentStatusTypeDef",
    "AgentsCriteriaOutputTypeDef",
    "AgentsCriteriaTypeDef",
    "AgentsCriteriaUnionTypeDef",
    "AllowedCapabilitiesTypeDef",
    "AnalyticsDataAssociationResultTypeDef",
    "AnswerMachineDetectionConfigTypeDef",
    "ApplicationOutputTypeDef",
    "ApplicationTypeDef",
    "ApplicationUnionTypeDef",
    "AssociateAnalyticsDataSetRequestRequestTypeDef",
    "AssociateAnalyticsDataSetResponseTypeDef",
    "AssociateApprovedOriginRequestRequestTypeDef",
    "AssociateBotRequestRequestTypeDef",
    "AssociateDefaultVocabularyRequestRequestTypeDef",
    "AssociateFlowRequestRequestTypeDef",
    "AssociateInstanceStorageConfigRequestRequestTypeDef",
    "AssociateInstanceStorageConfigResponseTypeDef",
    "AssociateLambdaFunctionRequestRequestTypeDef",
    "AssociateLexBotRequestRequestTypeDef",
    "AssociatePhoneNumberContactFlowRequestRequestTypeDef",
    "AssociateQueueQuickConnectsRequestRequestTypeDef",
    "AssociateRoutingProfileQueuesRequestRequestTypeDef",
    "AssociateSecurityKeyRequestRequestTypeDef",
    "AssociateSecurityKeyResponseTypeDef",
    "AssociateTrafficDistributionGroupUserRequestRequestTypeDef",
    "AssociateUserProficienciesRequestRequestTypeDef",
    "AssociatedContactSummaryTypeDef",
    "AttachedFileErrorTypeDef",
    "AttachedFileTypeDef",
    "AttachmentReferenceTypeDef",
    "AttendeeTypeDef",
    "AttributeAndConditionTypeDef",
    "AttributeConditionOutputTypeDef",
    "AttributeConditionTypeDef",
    "AttributeConditionUnionTypeDef",
    "AttributeTypeDef",
    "AudioFeaturesTypeDef",
    "AudioQualityMetricsInfoTypeDef",
    "AuthenticationProfileSummaryTypeDef",
    "AuthenticationProfileTypeDef",
    "AvailableNumberSummaryTypeDef",
    "BatchAssociateAnalyticsDataSetRequestRequestTypeDef",
    "BatchAssociateAnalyticsDataSetResponseTypeDef",
    "BatchDisassociateAnalyticsDataSetRequestRequestTypeDef",
    "BatchDisassociateAnalyticsDataSetResponseTypeDef",
    "BatchGetAttachedFileMetadataRequestRequestTypeDef",
    "BatchGetAttachedFileMetadataResponseTypeDef",
    "BatchGetFlowAssociationRequestRequestTypeDef",
    "BatchGetFlowAssociationResponseTypeDef",
    "BatchPutContactRequestRequestTypeDef",
    "BatchPutContactResponseTypeDef",
    "CampaignTypeDef",
    "ChatEventTypeDef",
    "ChatMessageTypeDef",
    "ChatParticipantRoleConfigTypeDef",
    "ChatStreamingConfigurationTypeDef",
    "ClaimPhoneNumberRequestRequestTypeDef",
    "ClaimPhoneNumberResponseTypeDef",
    "ClaimedPhoneNumberSummaryTypeDef",
    "CommonAttributeAndConditionTypeDef",
    "CompleteAttachedFileUploadRequestRequestTypeDef",
    "ConditionTypeDef",
    "ConnectionDataTypeDef",
    "ContactAnalysisTypeDef",
    "ContactDataRequestTypeDef",
    "ContactFilterTypeDef",
    "ContactFlowModuleSearchCriteriaPaginatorTypeDef",
    "ContactFlowModuleSearchCriteriaTypeDef",
    "ContactFlowModuleSearchFilterTypeDef",
    "ContactFlowModuleSummaryTypeDef",
    "ContactFlowModuleTypeDef",
    "ContactFlowSearchCriteriaPaginatorTypeDef",
    "ContactFlowSearchCriteriaTypeDef",
    "ContactFlowSearchFilterTypeDef",
    "ContactFlowSummaryTypeDef",
    "ContactFlowTypeDef",
    "ContactFlowVersionSummaryTypeDef",
    "ContactSearchSummaryAgentInfoTypeDef",
    "ContactSearchSummaryQueueInfoTypeDef",
    "ContactSearchSummarySegmentAttributeValueTypeDef",
    "ContactSearchSummaryTypeDef",
    "ContactTypeDef",
    "ControlPlaneAttributeFilterTypeDef",
    "ControlPlaneTagFilterTypeDef",
    "ControlPlaneUserAttributeFilterTypeDef",
    "CreateAgentStatusRequestRequestTypeDef",
    "CreateAgentStatusResponseTypeDef",
    "CreateCaseActionDefinitionOutputTypeDef",
    "CreateCaseActionDefinitionTypeDef",
    "CreateCaseActionDefinitionUnionTypeDef",
    "CreateContactFlowModuleRequestRequestTypeDef",
    "CreateContactFlowModuleResponseTypeDef",
    "CreateContactFlowRequestRequestTypeDef",
    "CreateContactFlowResponseTypeDef",
    "CreateContactFlowVersionRequestRequestTypeDef",
    "CreateContactFlowVersionResponseTypeDef",
    "CreateContactRequestRequestTypeDef",
    "CreateContactResponseTypeDef",
    "CreateEmailAddressRequestRequestTypeDef",
    "CreateEmailAddressResponseTypeDef",
    "CreateEvaluationFormRequestRequestTypeDef",
    "CreateEvaluationFormResponseTypeDef",
    "CreateHoursOfOperationRequestRequestTypeDef",
    "CreateHoursOfOperationResponseTypeDef",
    "CreateInstanceRequestRequestTypeDef",
    "CreateInstanceResponseTypeDef",
    "CreateIntegrationAssociationRequestRequestTypeDef",
    "CreateIntegrationAssociationResponseTypeDef",
    "CreateParticipantRequestRequestTypeDef",
    "CreateParticipantResponseTypeDef",
    "CreatePersistentContactAssociationRequestRequestTypeDef",
    "CreatePersistentContactAssociationResponseTypeDef",
    "CreatePredefinedAttributeRequestRequestTypeDef",
    "CreatePromptRequestRequestTypeDef",
    "CreatePromptResponseTypeDef",
    "CreateQueueRequestRequestTypeDef",
    "CreateQueueResponseTypeDef",
    "CreateQuickConnectRequestRequestTypeDef",
    "CreateQuickConnectResponseTypeDef",
    "CreateRoutingProfileRequestRequestTypeDef",
    "CreateRoutingProfileResponseTypeDef",
    "CreateRuleRequestRequestTypeDef",
    "CreateRuleResponseTypeDef",
    "CreateSecurityProfileRequestRequestTypeDef",
    "CreateSecurityProfileResponseTypeDef",
    "CreateTaskTemplateRequestRequestTypeDef",
    "CreateTaskTemplateResponseTypeDef",
    "CreateTrafficDistributionGroupRequestRequestTypeDef",
    "CreateTrafficDistributionGroupResponseTypeDef",
    "CreateUseCaseRequestRequestTypeDef",
    "CreateUseCaseResponseTypeDef",
    "CreateUserHierarchyGroupRequestRequestTypeDef",
    "CreateUserHierarchyGroupResponseTypeDef",
    "CreateUserRequestRequestTypeDef",
    "CreateUserResponseTypeDef",
    "CreateViewRequestRequestTypeDef",
    "CreateViewResponseTypeDef",
    "CreateViewVersionRequestRequestTypeDef",
    "CreateViewVersionResponseTypeDef",
    "CreateVocabularyRequestRequestTypeDef",
    "CreateVocabularyResponseTypeDef",
    "CreatedByInfoTypeDef",
    "CredentialsTypeDef",
    "CrossChannelBehaviorTypeDef",
    "CurrentMetricDataTypeDef",
    "CurrentMetricResultTypeDef",
    "CurrentMetricSortCriteriaTypeDef",
    "CurrentMetricTypeDef",
    "CustomerQualityMetricsTypeDef",
    "CustomerTypeDef",
    "CustomerVoiceActivityTypeDef",
    "DateReferenceTypeDef",
    "DeactivateEvaluationFormRequestRequestTypeDef",
    "DeactivateEvaluationFormResponseTypeDef",
    "DefaultVocabularyTypeDef",
    "DeleteAttachedFileRequestRequestTypeDef",
    "DeleteContactEvaluationRequestRequestTypeDef",
    "DeleteContactFlowModuleRequestRequestTypeDef",
    "DeleteContactFlowRequestRequestTypeDef",
    "DeleteEmailAddressRequestRequestTypeDef",
    "DeleteEvaluationFormRequestRequestTypeDef",
    "DeleteHoursOfOperationRequestRequestTypeDef",
    "DeleteInstanceRequestRequestTypeDef",
    "DeleteIntegrationAssociationRequestRequestTypeDef",
    "DeletePredefinedAttributeRequestRequestTypeDef",
    "DeletePromptRequestRequestTypeDef",
    "DeleteQueueRequestRequestTypeDef",
    "DeleteQuickConnectRequestRequestTypeDef",
    "DeleteRoutingProfileRequestRequestTypeDef",
    "DeleteRuleRequestRequestTypeDef",
    "DeleteSecurityProfileRequestRequestTypeDef",
    "DeleteTaskTemplateRequestRequestTypeDef",
    "DeleteTrafficDistributionGroupRequestRequestTypeDef",
    "DeleteUseCaseRequestRequestTypeDef",
    "DeleteUserHierarchyGroupRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeleteViewRequestRequestTypeDef",
    "DeleteViewVersionRequestRequestTypeDef",
    "DeleteVocabularyRequestRequestTypeDef",
    "DeleteVocabularyResponseTypeDef",
    "DescribeAgentStatusRequestRequestTypeDef",
    "DescribeAgentStatusResponseTypeDef",
    "DescribeAuthenticationProfileRequestRequestTypeDef",
    "DescribeAuthenticationProfileResponseTypeDef",
    "DescribeContactEvaluationRequestRequestTypeDef",
    "DescribeContactEvaluationResponseTypeDef",
    "DescribeContactFlowModuleRequestRequestTypeDef",
    "DescribeContactFlowModuleResponseTypeDef",
    "DescribeContactFlowRequestRequestTypeDef",
    "DescribeContactFlowResponseTypeDef",
    "DescribeContactRequestRequestTypeDef",
    "DescribeContactResponseTypeDef",
    "DescribeEmailAddressRequestRequestTypeDef",
    "DescribeEmailAddressResponseTypeDef",
    "DescribeEvaluationFormRequestRequestTypeDef",
    "DescribeEvaluationFormResponseTypeDef",
    "DescribeHoursOfOperationRequestRequestTypeDef",
    "DescribeHoursOfOperationResponseTypeDef",
    "DescribeInstanceAttributeRequestRequestTypeDef",
    "DescribeInstanceAttributeResponseTypeDef",
    "DescribeInstanceRequestRequestTypeDef",
    "DescribeInstanceResponseTypeDef",
    "DescribeInstanceStorageConfigRequestRequestTypeDef",
    "DescribeInstanceStorageConfigResponseTypeDef",
    "DescribePhoneNumberRequestRequestTypeDef",
    "DescribePhoneNumberResponseTypeDef",
    "DescribePredefinedAttributeRequestRequestTypeDef",
    "DescribePredefinedAttributeResponseTypeDef",
    "DescribePromptRequestRequestTypeDef",
    "DescribePromptResponseTypeDef",
    "DescribeQueueRequestRequestTypeDef",
    "DescribeQueueResponseTypeDef",
    "DescribeQuickConnectRequestRequestTypeDef",
    "DescribeQuickConnectResponseTypeDef",
    "DescribeRoutingProfileRequestRequestTypeDef",
    "DescribeRoutingProfileResponseTypeDef",
    "DescribeRuleRequestRequestTypeDef",
    "DescribeRuleResponseTypeDef",
    "DescribeSecurityProfileRequestRequestTypeDef",
    "DescribeSecurityProfileResponseTypeDef",
    "DescribeTrafficDistributionGroupRequestRequestTypeDef",
    "DescribeTrafficDistributionGroupResponseTypeDef",
    "DescribeUserHierarchyGroupRequestRequestTypeDef",
    "DescribeUserHierarchyGroupResponseTypeDef",
    "DescribeUserHierarchyStructureRequestRequestTypeDef",
    "DescribeUserHierarchyStructureResponseTypeDef",
    "DescribeUserRequestRequestTypeDef",
    "DescribeUserResponseTypeDef",
    "DescribeViewRequestRequestTypeDef",
    "DescribeViewResponseTypeDef",
    "DescribeVocabularyRequestRequestTypeDef",
    "DescribeVocabularyResponseTypeDef",
    "DeviceInfoTypeDef",
    "DimensionsTypeDef",
    "DisassociateAnalyticsDataSetRequestRequestTypeDef",
    "DisassociateApprovedOriginRequestRequestTypeDef",
    "DisassociateBotRequestRequestTypeDef",
    "DisassociateFlowRequestRequestTypeDef",
    "DisassociateInstanceStorageConfigRequestRequestTypeDef",
    "DisassociateLambdaFunctionRequestRequestTypeDef",
    "DisassociateLexBotRequestRequestTypeDef",
    "DisassociatePhoneNumberContactFlowRequestRequestTypeDef",
    "DisassociateQueueQuickConnectsRequestRequestTypeDef",
    "DisassociateRoutingProfileQueuesRequestRequestTypeDef",
    "DisassociateSecurityKeyRequestRequestTypeDef",
    "DisassociateTrafficDistributionGroupUserRequestRequestTypeDef",
    "DisassociateUserProficienciesRequestRequestTypeDef",
    "DisconnectDetailsTypeDef",
    "DisconnectReasonTypeDef",
    "DismissUserContactRequestRequestTypeDef",
    "DistributionTypeDef",
    "DownloadUrlMetadataTypeDef",
    "EmailAddressInfoTypeDef",
    "EmailAddressMetadataTypeDef",
    "EmailAddressSearchCriteriaTypeDef",
    "EmailAddressSearchFilterTypeDef",
    "EmailAttachmentTypeDef",
    "EmailMessageReferenceTypeDef",
    "EmailRecipientTypeDef",
    "EmailReferenceTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionConfigTypeDef",
    "EndpointInfoTypeDef",
    "EndpointTypeDef",
    "ErrorResultTypeDef",
    "EvaluationAnswerDataTypeDef",
    "EvaluationAnswerInputTypeDef",
    "EvaluationAnswerOutputTypeDef",
    "EvaluationFormContentTypeDef",
    "EvaluationFormItemOutputTypeDef",
    "EvaluationFormItemTypeDef",
    "EvaluationFormItemUnionTypeDef",
    "EvaluationFormNumericQuestionAutomationTypeDef",
    "EvaluationFormNumericQuestionOptionTypeDef",
    "EvaluationFormNumericQuestionPropertiesOutputTypeDef",
    "EvaluationFormNumericQuestionPropertiesTypeDef",
    "EvaluationFormNumericQuestionPropertiesUnionTypeDef",
    "EvaluationFormQuestionOutputTypeDef",
    "EvaluationFormQuestionTypeDef",
    "EvaluationFormQuestionTypePropertiesOutputTypeDef",
    "EvaluationFormQuestionTypePropertiesTypeDef",
    "EvaluationFormQuestionTypePropertiesUnionTypeDef",
    "EvaluationFormQuestionUnionTypeDef",
    "EvaluationFormScoringStrategyTypeDef",
    "EvaluationFormSectionOutputTypeDef",
    "EvaluationFormSectionTypeDef",
    "EvaluationFormSectionUnionTypeDef",
    "EvaluationFormSingleSelectQuestionAutomationOptionTypeDef",
    "EvaluationFormSingleSelectQuestionAutomationOutputTypeDef",
    "EvaluationFormSingleSelectQuestionAutomationTypeDef",
    "EvaluationFormSingleSelectQuestionAutomationUnionTypeDef",
    "EvaluationFormSingleSelectQuestionOptionTypeDef",
    "EvaluationFormSingleSelectQuestionPropertiesOutputTypeDef",
    "EvaluationFormSingleSelectQuestionPropertiesTypeDef",
    "EvaluationFormSingleSelectQuestionPropertiesUnionTypeDef",
    "EvaluationFormSummaryTypeDef",
    "EvaluationFormTypeDef",
    "EvaluationFormVersionSummaryTypeDef",
    "EvaluationMetadataTypeDef",
    "EvaluationNoteTypeDef",
    "EvaluationScoreTypeDef",
    "EvaluationSummaryTypeDef",
    "EvaluationTypeDef",
    "EventBridgeActionDefinitionTypeDef",
    "ExpiryTypeDef",
    "ExpressionOutputTypeDef",
    "ExpressionTypeDef",
    "ExpressionUnionTypeDef",
    "FailedRequestTypeDef",
    "FieldValueExtraUnionTypeDef",
    "FieldValueOutputTypeDef",
    "FieldValueTypeDef",
    "FieldValueUnionOutputTypeDef",
    "FieldValueUnionTypeDef",
    "FieldValueUnionUnionTypeDef",
    "FilterV2TypeDef",
    "FiltersTypeDef",
    "FlowAssociationSummaryTypeDef",
    "GetAttachedFileRequestRequestTypeDef",
    "GetAttachedFileResponseTypeDef",
    "GetContactAttributesRequestRequestTypeDef",
    "GetContactAttributesResponseTypeDef",
    "GetCurrentMetricDataRequestRequestTypeDef",
    "GetCurrentMetricDataResponseTypeDef",
    "GetCurrentUserDataRequestRequestTypeDef",
    "GetCurrentUserDataResponseTypeDef",
    "GetFederationTokenRequestRequestTypeDef",
    "GetFederationTokenResponseTypeDef",
    "GetFlowAssociationRequestRequestTypeDef",
    "GetFlowAssociationResponseTypeDef",
    "GetMetricDataRequestGetMetricDataPaginateTypeDef",
    "GetMetricDataRequestRequestTypeDef",
    "GetMetricDataResponseTypeDef",
    "GetMetricDataV2RequestRequestTypeDef",
    "GetMetricDataV2ResponseTypeDef",
    "GetPromptFileRequestRequestTypeDef",
    "GetPromptFileResponseTypeDef",
    "GetTaskTemplateRequestRequestTypeDef",
    "GetTaskTemplateResponseTypeDef",
    "GetTrafficDistributionRequestRequestTypeDef",
    "GetTrafficDistributionResponseTypeDef",
    "HierarchyGroupConditionTypeDef",
    "HierarchyGroupSummaryReferenceTypeDef",
    "HierarchyGroupSummaryTypeDef",
    "HierarchyGroupTypeDef",
    "HierarchyGroupsTypeDef",
    "HierarchyLevelTypeDef",
    "HierarchyLevelUpdateTypeDef",
    "HierarchyPathReferenceTypeDef",
    "HierarchyPathTypeDef",
    "HierarchyStructureTypeDef",
    "HierarchyStructureUpdateTypeDef",
    "HistoricalMetricDataTypeDef",
    "HistoricalMetricResultTypeDef",
    "HistoricalMetricTypeDef",
    "HoursOfOperationConfigTypeDef",
    "HoursOfOperationSearchCriteriaPaginatorTypeDef",
    "HoursOfOperationSearchCriteriaTypeDef",
    "HoursOfOperationSearchFilterTypeDef",
    "HoursOfOperationSummaryTypeDef",
    "HoursOfOperationTimeSliceTypeDef",
    "HoursOfOperationTypeDef",
    "ImportPhoneNumberRequestRequestTypeDef",
    "ImportPhoneNumberResponseTypeDef",
    "InboundAdditionalRecipientsTypeDef",
    "InboundEmailContentTypeDef",
    "InboundRawMessageTypeDef",
    "InstanceStatusReasonTypeDef",
    "InstanceStorageConfigTypeDef",
    "InstanceSummaryTypeDef",
    "InstanceTypeDef",
    "IntegrationAssociationSummaryTypeDef",
    "IntervalDetailsTypeDef",
    "InvisibleFieldInfoTypeDef",
    "KinesisFirehoseConfigTypeDef",
    "KinesisStreamConfigTypeDef",
    "KinesisVideoStreamConfigTypeDef",
    "LexBotConfigTypeDef",
    "LexBotTypeDef",
    "LexV2BotTypeDef",
    "ListAgentStatusRequestListAgentStatusesPaginateTypeDef",
    "ListAgentStatusRequestRequestTypeDef",
    "ListAgentStatusResponseTypeDef",
    "ListAnalyticsDataAssociationsRequestRequestTypeDef",
    "ListAnalyticsDataAssociationsResponseTypeDef",
    "ListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef",
    "ListApprovedOriginsRequestRequestTypeDef",
    "ListApprovedOriginsResponseTypeDef",
    "ListAssociatedContactsRequestRequestTypeDef",
    "ListAssociatedContactsResponseTypeDef",
    "ListAuthenticationProfilesRequestListAuthenticationProfilesPaginateTypeDef",
    "ListAuthenticationProfilesRequestRequestTypeDef",
    "ListAuthenticationProfilesResponseTypeDef",
    "ListBotsRequestListBotsPaginateTypeDef",
    "ListBotsRequestRequestTypeDef",
    "ListBotsResponseTypeDef",
    "ListConditionTypeDef",
    "ListContactEvaluationsRequestListContactEvaluationsPaginateTypeDef",
    "ListContactEvaluationsRequestRequestTypeDef",
    "ListContactEvaluationsResponseTypeDef",
    "ListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef",
    "ListContactFlowModulesRequestRequestTypeDef",
    "ListContactFlowModulesResponseTypeDef",
    "ListContactFlowVersionsRequestListContactFlowVersionsPaginateTypeDef",
    "ListContactFlowVersionsRequestRequestTypeDef",
    "ListContactFlowVersionsResponseTypeDef",
    "ListContactFlowsRequestListContactFlowsPaginateTypeDef",
    "ListContactFlowsRequestRequestTypeDef",
    "ListContactFlowsResponseTypeDef",
    "ListContactReferencesRequestListContactReferencesPaginateTypeDef",
    "ListContactReferencesRequestRequestTypeDef",
    "ListContactReferencesResponseTypeDef",
    "ListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef",
    "ListDefaultVocabulariesRequestRequestTypeDef",
    "ListDefaultVocabulariesResponseTypeDef",
    "ListEvaluationFormVersionsRequestListEvaluationFormVersionsPaginateTypeDef",
    "ListEvaluationFormVersionsRequestRequestTypeDef",
    "ListEvaluationFormVersionsResponseTypeDef",
    "ListEvaluationFormsRequestListEvaluationFormsPaginateTypeDef",
    "ListEvaluationFormsRequestRequestTypeDef",
    "ListEvaluationFormsResponseTypeDef",
    "ListFlowAssociationsRequestListFlowAssociationsPaginateTypeDef",
    "ListFlowAssociationsRequestRequestTypeDef",
    "ListFlowAssociationsResponseTypeDef",
    "ListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef",
    "ListHoursOfOperationsRequestRequestTypeDef",
    "ListHoursOfOperationsResponseTypeDef",
    "ListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef",
    "ListInstanceAttributesRequestRequestTypeDef",
    "ListInstanceAttributesResponseTypeDef",
    "ListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef",
    "ListInstanceStorageConfigsRequestRequestTypeDef",
    "ListInstanceStorageConfigsResponseTypeDef",
    "ListInstancesRequestListInstancesPaginateTypeDef",
    "ListInstancesRequestRequestTypeDef",
    "ListInstancesResponseTypeDef",
    "ListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef",
    "ListIntegrationAssociationsRequestRequestTypeDef",
    "ListIntegrationAssociationsResponseTypeDef",
    "ListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef",
    "ListLambdaFunctionsRequestRequestTypeDef",
    "ListLambdaFunctionsResponseTypeDef",
    "ListLexBotsRequestListLexBotsPaginateTypeDef",
    "ListLexBotsRequestRequestTypeDef",
    "ListLexBotsResponseTypeDef",
    "ListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef",
    "ListPhoneNumbersRequestRequestTypeDef",
    "ListPhoneNumbersResponseTypeDef",
    "ListPhoneNumbersSummaryTypeDef",
    "ListPhoneNumbersV2RequestListPhoneNumbersV2PaginateTypeDef",
    "ListPhoneNumbersV2RequestRequestTypeDef",
    "ListPhoneNumbersV2ResponseTypeDef",
    "ListPredefinedAttributesRequestListPredefinedAttributesPaginateTypeDef",
    "ListPredefinedAttributesRequestRequestTypeDef",
    "ListPredefinedAttributesResponseTypeDef",
    "ListPromptsRequestListPromptsPaginateTypeDef",
    "ListPromptsRequestRequestTypeDef",
    "ListPromptsResponseTypeDef",
    "ListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef",
    "ListQueueQuickConnectsRequestRequestTypeDef",
    "ListQueueQuickConnectsResponseTypeDef",
    "ListQueuesRequestListQueuesPaginateTypeDef",
    "ListQueuesRequestRequestTypeDef",
    "ListQueuesResponseTypeDef",
    "ListQuickConnectsRequestListQuickConnectsPaginateTypeDef",
    "ListQuickConnectsRequestRequestTypeDef",
    "ListQuickConnectsResponseTypeDef",
    "ListRealtimeContactAnalysisSegmentsV2RequestRequestTypeDef",
    "ListRealtimeContactAnalysisSegmentsV2ResponseTypeDef",
    "ListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef",
    "ListRoutingProfileQueuesRequestRequestTypeDef",
    "ListRoutingProfileQueuesResponseTypeDef",
    "ListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef",
    "ListRoutingProfilesRequestRequestTypeDef",
    "ListRoutingProfilesResponseTypeDef",
    "ListRulesRequestListRulesPaginateTypeDef",
    "ListRulesRequestRequestTypeDef",
    "ListRulesResponseTypeDef",
    "ListSecurityKeysRequestListSecurityKeysPaginateTypeDef",
    "ListSecurityKeysRequestRequestTypeDef",
    "ListSecurityKeysResponseTypeDef",
    "ListSecurityProfileApplicationsRequestListSecurityProfileApplicationsPaginateTypeDef",
    "ListSecurityProfileApplicationsRequestRequestTypeDef",
    "ListSecurityProfileApplicationsResponseTypeDef",
    "ListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef",
    "ListSecurityProfilePermissionsRequestRequestTypeDef",
    "ListSecurityProfilePermissionsResponseTypeDef",
    "ListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef",
    "ListSecurityProfilesRequestRequestTypeDef",
    "ListSecurityProfilesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef",
    "ListTaskTemplatesRequestRequestTypeDef",
    "ListTaskTemplatesResponseTypeDef",
    "ListTrafficDistributionGroupUsersRequestListTrafficDistributionGroupUsersPaginateTypeDef",
    "ListTrafficDistributionGroupUsersRequestRequestTypeDef",
    "ListTrafficDistributionGroupUsersResponseTypeDef",
    "ListTrafficDistributionGroupsRequestListTrafficDistributionGroupsPaginateTypeDef",
    "ListTrafficDistributionGroupsRequestRequestTypeDef",
    "ListTrafficDistributionGroupsResponseTypeDef",
    "ListUseCasesRequestListUseCasesPaginateTypeDef",
    "ListUseCasesRequestRequestTypeDef",
    "ListUseCasesResponseTypeDef",
    "ListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef",
    "ListUserHierarchyGroupsRequestRequestTypeDef",
    "ListUserHierarchyGroupsResponseTypeDef",
    "ListUserProficienciesRequestListUserProficienciesPaginateTypeDef",
    "ListUserProficienciesRequestRequestTypeDef",
    "ListUserProficienciesResponseTypeDef",
    "ListUsersRequestListUsersPaginateTypeDef",
    "ListUsersRequestRequestTypeDef",
    "ListUsersResponseTypeDef",
    "ListViewVersionsRequestListViewVersionsPaginateTypeDef",
    "ListViewVersionsRequestRequestTypeDef",
    "ListViewVersionsResponseTypeDef",
    "ListViewsRequestListViewsPaginateTypeDef",
    "ListViewsRequestRequestTypeDef",
    "ListViewsResponseTypeDef",
    "MatchCriteriaOutputTypeDef",
    "MatchCriteriaTypeDef",
    "MatchCriteriaUnionTypeDef",
    "MediaConcurrencyTypeDef",
    "MediaPlacementTypeDef",
    "MeetingFeaturesConfigurationTypeDef",
    "MeetingTypeDef",
    "MetricDataV2TypeDef",
    "MetricFilterV2OutputTypeDef",
    "MetricFilterV2TypeDef",
    "MetricFilterV2UnionTypeDef",
    "MetricIntervalTypeDef",
    "MetricResultV2TypeDef",
    "MetricV2OutputTypeDef",
    "MetricV2TypeDef",
    "MetricV2UnionTypeDef",
    "MonitorContactRequestRequestTypeDef",
    "MonitorContactResponseTypeDef",
    "NewSessionDetailsTypeDef",
    "NotificationRecipientTypeOutputTypeDef",
    "NotificationRecipientTypeTypeDef",
    "NotificationRecipientTypeUnionTypeDef",
    "NumberConditionTypeDef",
    "NumberReferenceTypeDef",
    "NumericQuestionPropertyValueAutomationTypeDef",
    "OutboundAdditionalRecipientsTypeDef",
    "OutboundCallerConfigTypeDef",
    "OutboundEmailConfigTypeDef",
    "OutboundEmailContentTypeDef",
    "OutboundRawMessageTypeDef",
    "PaginatorConfigTypeDef",
    "ParticipantCapabilitiesTypeDef",
    "ParticipantDetailsToAddTypeDef",
    "ParticipantDetailsTypeDef",
    "ParticipantTimerConfigurationTypeDef",
    "ParticipantTimerValueTypeDef",
    "ParticipantTokenCredentialsTypeDef",
    "PauseContactRequestRequestTypeDef",
    "PersistentChatTypeDef",
    "PhoneNumberQuickConnectConfigTypeDef",
    "PhoneNumberStatusTypeDef",
    "PhoneNumberSummaryTypeDef",
    "PredefinedAttributeSearchCriteriaPaginatorTypeDef",
    "PredefinedAttributeSearchCriteriaTypeDef",
    "PredefinedAttributeSummaryTypeDef",
    "PredefinedAttributeTypeDef",
    "PredefinedAttributeValuesOutputTypeDef",
    "PredefinedAttributeValuesTypeDef",
    "PromptSearchCriteriaPaginatorTypeDef",
    "PromptSearchCriteriaTypeDef",
    "PromptSearchFilterTypeDef",
    "PromptSummaryTypeDef",
    "PromptTypeDef",
    "PutUserStatusRequestRequestTypeDef",
    "QualityMetricsTypeDef",
    "QueueInfoInputTypeDef",
    "QueueInfoTypeDef",
    "QueueQuickConnectConfigTypeDef",
    "QueueReferenceTypeDef",
    "QueueSearchCriteriaPaginatorTypeDef",
    "QueueSearchCriteriaTypeDef",
    "QueueSearchFilterTypeDef",
    "QueueSummaryTypeDef",
    "QueueTypeDef",
    "QuickConnectConfigTypeDef",
    "QuickConnectSearchCriteriaPaginatorTypeDef",
    "QuickConnectSearchCriteriaTypeDef",
    "QuickConnectSearchFilterTypeDef",
    "QuickConnectSummaryTypeDef",
    "QuickConnectTypeDef",
    "ReadOnlyFieldInfoTypeDef",
    "RealTimeContactAnalysisAttachmentTypeDef",
    "RealTimeContactAnalysisCategoryDetailsTypeDef",
    "RealTimeContactAnalysisCharacterIntervalTypeDef",
    "RealTimeContactAnalysisIssueDetectedTypeDef",
    "RealTimeContactAnalysisPointOfInterestTypeDef",
    "RealTimeContactAnalysisSegmentAttachmentsTypeDef",
    "RealTimeContactAnalysisSegmentCategoriesTypeDef",
    "RealTimeContactAnalysisSegmentEventTypeDef",
    "RealTimeContactAnalysisSegmentIssuesTypeDef",
    "RealTimeContactAnalysisSegmentPostContactSummaryTypeDef",
    "RealTimeContactAnalysisSegmentTranscriptTypeDef",
    "RealTimeContactAnalysisTimeDataTypeDef",
    "RealTimeContactAnalysisTranscriptItemRedactionTypeDef",
    "RealTimeContactAnalysisTranscriptItemWithCharacterOffsetsTypeDef",
    "RealTimeContactAnalysisTranscriptItemWithContentTypeDef",
    "RealtimeContactAnalysisSegmentTypeDef",
    "ReferenceSummaryTypeDef",
    "ReferenceTypeDef",
    "ReleasePhoneNumberRequestRequestTypeDef",
    "ReplicateInstanceRequestRequestTypeDef",
    "ReplicateInstanceResponseTypeDef",
    "ReplicationConfigurationTypeDef",
    "ReplicationStatusSummaryTypeDef",
    "RequiredFieldInfoTypeDef",
    "ResourceTagsSearchCriteriaTypeDef",
    "ResponseMetadataTypeDef",
    "ResumeContactRecordingRequestRequestTypeDef",
    "ResumeContactRequestRequestTypeDef",
    "RoutingCriteriaInputStepExpiryTypeDef",
    "RoutingCriteriaInputStepTypeDef",
    "RoutingCriteriaInputTypeDef",
    "RoutingCriteriaTypeDef",
    "RoutingProfileQueueConfigSummaryTypeDef",
    "RoutingProfileQueueConfigTypeDef",
    "RoutingProfileQueueReferenceTypeDef",
    "RoutingProfileReferenceTypeDef",
    "RoutingProfileSearchCriteriaPaginatorTypeDef",
    "RoutingProfileSearchCriteriaTypeDef",
    "RoutingProfileSearchFilterTypeDef",
    "RoutingProfileSummaryTypeDef",
    "RoutingProfileTypeDef",
    "RuleActionOutputTypeDef",
    "RuleActionTypeDef",
    "RuleActionUnionTypeDef",
    "RuleSummaryTypeDef",
    "RuleTriggerEventSourceTypeDef",
    "RuleTypeDef",
    "S3ConfigTypeDef",
    "SearchAgentStatusesRequestRequestTypeDef",
    "SearchAgentStatusesRequestSearchAgentStatusesPaginateTypeDef",
    "SearchAgentStatusesResponseTypeDef",
    "SearchAvailablePhoneNumbersRequestRequestTypeDef",
    "SearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef",
    "SearchAvailablePhoneNumbersResponseTypeDef",
    "SearchContactFlowModulesRequestRequestTypeDef",
    "SearchContactFlowModulesRequestSearchContactFlowModulesPaginateTypeDef",
    "SearchContactFlowModulesResponseTypeDef",
    "SearchContactFlowsRequestRequestTypeDef",
    "SearchContactFlowsRequestSearchContactFlowsPaginateTypeDef",
    "SearchContactFlowsResponseTypeDef",
    "SearchContactsRequestRequestTypeDef",
    "SearchContactsRequestSearchContactsPaginateTypeDef",
    "SearchContactsResponseTypeDef",
    "SearchContactsTimeRangeTypeDef",
    "SearchCriteriaTypeDef",
    "SearchEmailAddressesRequestRequestTypeDef",
    "SearchEmailAddressesResponseTypeDef",
    "SearchHoursOfOperationsRequestRequestTypeDef",
    "SearchHoursOfOperationsRequestSearchHoursOfOperationsPaginateTypeDef",
    "SearchHoursOfOperationsResponseTypeDef",
    "SearchPredefinedAttributesRequestRequestTypeDef",
    "SearchPredefinedAttributesRequestSearchPredefinedAttributesPaginateTypeDef",
    "SearchPredefinedAttributesResponseTypeDef",
    "SearchPromptsRequestRequestTypeDef",
    "SearchPromptsRequestSearchPromptsPaginateTypeDef",
    "SearchPromptsResponseTypeDef",
    "SearchQueuesRequestRequestTypeDef",
    "SearchQueuesRequestSearchQueuesPaginateTypeDef",
    "SearchQueuesResponseTypeDef",
    "SearchQuickConnectsRequestRequestTypeDef",
    "SearchQuickConnectsRequestSearchQuickConnectsPaginateTypeDef",
    "SearchQuickConnectsResponseTypeDef",
    "SearchResourceTagsRequestRequestTypeDef",
    "SearchResourceTagsRequestSearchResourceTagsPaginateTypeDef",
    "SearchResourceTagsResponseTypeDef",
    "SearchRoutingProfilesRequestRequestTypeDef",
    "SearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef",
    "SearchRoutingProfilesResponseTypeDef",
    "SearchSecurityProfilesRequestRequestTypeDef",
    "SearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef",
    "SearchSecurityProfilesResponseTypeDef",
    "SearchUserHierarchyGroupsRequestRequestTypeDef",
    "SearchUserHierarchyGroupsRequestSearchUserHierarchyGroupsPaginateTypeDef",
    "SearchUserHierarchyGroupsResponseTypeDef",
    "SearchUsersRequestRequestTypeDef",
    "SearchUsersRequestSearchUsersPaginateTypeDef",
    "SearchUsersResponseTypeDef",
    "SearchVocabulariesRequestRequestTypeDef",
    "SearchVocabulariesRequestSearchVocabulariesPaginateTypeDef",
    "SearchVocabulariesResponseTypeDef",
    "SearchableContactAttributesCriteriaTypeDef",
    "SearchableContactAttributesTypeDef",
    "SearchableSegmentAttributesCriteriaTypeDef",
    "SearchableSegmentAttributesTypeDef",
    "SecurityKeyTypeDef",
    "SecurityProfileSearchCriteriaPaginatorTypeDef",
    "SecurityProfileSearchCriteriaTypeDef",
    "SecurityProfileSearchSummaryTypeDef",
    "SecurityProfileSummaryTypeDef",
    "SecurityProfileTypeDef",
    "SecurityProfilesSearchFilterTypeDef",
    "SegmentAttributeValueOutputTypeDef",
    "SegmentAttributeValueTypeDef",
    "SegmentAttributeValueUnionTypeDef",
    "SendChatIntegrationEventRequestRequestTypeDef",
    "SendChatIntegrationEventResponseTypeDef",
    "SendNotificationActionDefinitionOutputTypeDef",
    "SendNotificationActionDefinitionTypeDef",
    "SendNotificationActionDefinitionUnionTypeDef",
    "SendOutboundEmailRequestRequestTypeDef",
    "SignInConfigOutputTypeDef",
    "SignInConfigTypeDef",
    "SignInDistributionTypeDef",
    "SingleSelectQuestionRuleCategoryAutomationTypeDef",
    "SortTypeDef",
    "SourceCampaignTypeDef",
    "StartAttachedFileUploadRequestRequestTypeDef",
    "StartAttachedFileUploadResponseTypeDef",
    "StartChatContactRequestRequestTypeDef",
    "StartChatContactResponseTypeDef",
    "StartContactEvaluationRequestRequestTypeDef",
    "StartContactEvaluationResponseTypeDef",
    "StartContactRecordingRequestRequestTypeDef",
    "StartContactStreamingRequestRequestTypeDef",
    "StartContactStreamingResponseTypeDef",
    "StartEmailContactRequestRequestTypeDef",
    "StartEmailContactResponseTypeDef",
    "StartOutboundChatContactRequestRequestTypeDef",
    "StartOutboundChatContactResponseTypeDef",
    "StartOutboundEmailContactRequestRequestTypeDef",
    "StartOutboundEmailContactResponseTypeDef",
    "StartOutboundVoiceContactRequestRequestTypeDef",
    "StartOutboundVoiceContactResponseTypeDef",
    "StartScreenSharingRequestRequestTypeDef",
    "StartTaskContactRequestRequestTypeDef",
    "StartTaskContactResponseTypeDef",
    "StartWebRTCContactRequestRequestTypeDef",
    "StartWebRTCContactResponseTypeDef",
    "StepTypeDef",
    "StopContactRecordingRequestRequestTypeDef",
    "StopContactRequestRequestTypeDef",
    "StopContactStreamingRequestRequestTypeDef",
    "StringConditionTypeDef",
    "StringReferenceTypeDef",
    "SubmitAutoEvaluationActionDefinitionTypeDef",
    "SubmitContactEvaluationRequestRequestTypeDef",
    "SubmitContactEvaluationResponseTypeDef",
    "SuccessfulRequestTypeDef",
    "SuspendContactRecordingRequestRequestTypeDef",
    "TagConditionTypeDef",
    "TagContactRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagSearchConditionTypeDef",
    "TagSetTypeDef",
    "TaskActionDefinitionOutputTypeDef",
    "TaskActionDefinitionTypeDef",
    "TaskActionDefinitionUnionTypeDef",
    "TaskTemplateConstraintsOutputTypeDef",
    "TaskTemplateConstraintsTypeDef",
    "TaskTemplateDefaultFieldValueTypeDef",
    "TaskTemplateDefaultsOutputTypeDef",
    "TaskTemplateDefaultsTypeDef",
    "TaskTemplateFieldIdentifierTypeDef",
    "TaskTemplateFieldOutputTypeDef",
    "TaskTemplateFieldTypeDef",
    "TaskTemplateFieldUnionTypeDef",
    "TaskTemplateMetadataTypeDef",
    "TelephonyConfigOutputTypeDef",
    "TelephonyConfigTypeDef",
    "TemplateAttributesTypeDef",
    "TemplatedMessageConfigTypeDef",
    "ThresholdTypeDef",
    "ThresholdV2TypeDef",
    "TimestampTypeDef",
    "TrafficDistributionGroupSummaryTypeDef",
    "TrafficDistributionGroupTypeDef",
    "TrafficDistributionGroupUserSummaryTypeDef",
    "TranscriptCriteriaTypeDef",
    "TranscriptTypeDef",
    "TransferContactRequestRequestTypeDef",
    "TransferContactResponseTypeDef",
    "UntagContactRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAgentStatusRequestRequestTypeDef",
    "UpdateAuthenticationProfileRequestRequestTypeDef",
    "UpdateCaseActionDefinitionOutputTypeDef",
    "UpdateCaseActionDefinitionTypeDef",
    "UpdateCaseActionDefinitionUnionTypeDef",
    "UpdateContactAttributesRequestRequestTypeDef",
    "UpdateContactEvaluationRequestRequestTypeDef",
    "UpdateContactEvaluationResponseTypeDef",
    "UpdateContactFlowContentRequestRequestTypeDef",
    "UpdateContactFlowMetadataRequestRequestTypeDef",
    "UpdateContactFlowModuleContentRequestRequestTypeDef",
    "UpdateContactFlowModuleMetadataRequestRequestTypeDef",
    "UpdateContactFlowNameRequestRequestTypeDef",
    "UpdateContactRequestRequestTypeDef",
    "UpdateContactRoutingDataRequestRequestTypeDef",
    "UpdateContactScheduleRequestRequestTypeDef",
    "UpdateEmailAddressMetadataRequestRequestTypeDef",
    "UpdateEmailAddressMetadataResponseTypeDef",
    "UpdateEvaluationFormRequestRequestTypeDef",
    "UpdateEvaluationFormResponseTypeDef",
    "UpdateHoursOfOperationRequestRequestTypeDef",
    "UpdateInstanceAttributeRequestRequestTypeDef",
    "UpdateInstanceStorageConfigRequestRequestTypeDef",
    "UpdateParticipantRoleConfigChannelInfoTypeDef",
    "UpdateParticipantRoleConfigRequestRequestTypeDef",
    "UpdatePhoneNumberMetadataRequestRequestTypeDef",
    "UpdatePhoneNumberRequestRequestTypeDef",
    "UpdatePhoneNumberResponseTypeDef",
    "UpdatePredefinedAttributeRequestRequestTypeDef",
    "UpdatePromptRequestRequestTypeDef",
    "UpdatePromptResponseTypeDef",
    "UpdateQueueHoursOfOperationRequestRequestTypeDef",
    "UpdateQueueMaxContactsRequestRequestTypeDef",
    "UpdateQueueNameRequestRequestTypeDef",
    "UpdateQueueOutboundCallerConfigRequestRequestTypeDef",
    "UpdateQueueOutboundEmailConfigRequestRequestTypeDef",
    "UpdateQueueStatusRequestRequestTypeDef",
    "UpdateQuickConnectConfigRequestRequestTypeDef",
    "UpdateQuickConnectNameRequestRequestTypeDef",
    "UpdateRoutingProfileAgentAvailabilityTimerRequestRequestTypeDef",
    "UpdateRoutingProfileConcurrencyRequestRequestTypeDef",
    "UpdateRoutingProfileDefaultOutboundQueueRequestRequestTypeDef",
    "UpdateRoutingProfileNameRequestRequestTypeDef",
    "UpdateRoutingProfileQueuesRequestRequestTypeDef",
    "UpdateRuleRequestRequestTypeDef",
    "UpdateSecurityProfileRequestRequestTypeDef",
    "UpdateTaskTemplateRequestRequestTypeDef",
    "UpdateTaskTemplateResponseTypeDef",
    "UpdateTrafficDistributionRequestRequestTypeDef",
    "UpdateUserHierarchyGroupNameRequestRequestTypeDef",
    "UpdateUserHierarchyRequestRequestTypeDef",
    "UpdateUserHierarchyStructureRequestRequestTypeDef",
    "UpdateUserIdentityInfoRequestRequestTypeDef",
    "UpdateUserPhoneConfigRequestRequestTypeDef",
    "UpdateUserProficienciesRequestRequestTypeDef",
    "UpdateUserRoutingProfileRequestRequestTypeDef",
    "UpdateUserSecurityProfilesRequestRequestTypeDef",
    "UpdateViewContentRequestRequestTypeDef",
    "UpdateViewContentResponseTypeDef",
    "UpdateViewMetadataRequestRequestTypeDef",
    "UploadUrlMetadataTypeDef",
    "UrlReferenceTypeDef",
    "UseCaseTypeDef",
    "UserDataFiltersTypeDef",
    "UserDataTypeDef",
    "UserHierarchyGroupSearchCriteriaPaginatorTypeDef",
    "UserHierarchyGroupSearchCriteriaTypeDef",
    "UserHierarchyGroupSearchFilterTypeDef",
    "UserIdentityInfoLiteTypeDef",
    "UserIdentityInfoTypeDef",
    "UserInfoTypeDef",
    "UserPhoneConfigTypeDef",
    "UserProficiencyDisassociateTypeDef",
    "UserProficiencyTypeDef",
    "UserQuickConnectConfigTypeDef",
    "UserReferenceTypeDef",
    "UserSearchCriteriaPaginatorTypeDef",
    "UserSearchCriteriaTypeDef",
    "UserSearchFilterTypeDef",
    "UserSearchSummaryTypeDef",
    "UserSummaryTypeDef",
    "UserTypeDef",
    "ViewContentTypeDef",
    "ViewInputContentTypeDef",
    "ViewSummaryTypeDef",
    "ViewTypeDef",
    "ViewVersionSummaryTypeDef",
    "VocabularySummaryTypeDef",
    "VocabularyTypeDef",
    "VoiceRecordingConfigurationTypeDef",
    "WisdomInfoTypeDef",
)


class ActionSummaryTypeDef(TypedDict):
    ActionType: ActionTypeType


class ActivateEvaluationFormRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EvaluationFormId: str
    EvaluationFormVersion: int


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class EmailRecipientTypeDef(TypedDict):
    Address: NotRequired[str]
    DisplayName: NotRequired[str]


class DistributionTypeDef(TypedDict):
    Region: str
    Percentage: int


class QueueReferenceTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]


class AgentHierarchyGroupTypeDef(TypedDict):
    Arn: NotRequired[str]


class AgentHierarchyGroupsTypeDef(TypedDict):
    L1Ids: NotRequired[Sequence[str]]
    L2Ids: NotRequired[Sequence[str]]
    L3Ids: NotRequired[Sequence[str]]
    L4Ids: NotRequired[Sequence[str]]
    L5Ids: NotRequired[Sequence[str]]


class DeviceInfoTypeDef(TypedDict):
    PlatformName: NotRequired[str]
    PlatformVersion: NotRequired[str]
    OperatingSystem: NotRequired[str]


class ParticipantCapabilitiesTypeDef(TypedDict):
    Video: NotRequired[Literal["SEND"]]
    ScreenShare: NotRequired[Literal["SEND"]]


class AudioQualityMetricsInfoTypeDef(TypedDict):
    QualityScore: NotRequired[float]
    PotentialQualityIssues: NotRequired[List[str]]


class AgentStatusReferenceTypeDef(TypedDict):
    StatusStartTimestamp: NotRequired[datetime]
    StatusArn: NotRequired[str]
    StatusName: NotRequired[str]


StringConditionTypeDef = TypedDict(
    "StringConditionTypeDef",
    {
        "FieldName": NotRequired[str],
        "Value": NotRequired[str],
        "ComparisonType": NotRequired[StringComparisonTypeType],
    },
)
AgentStatusSummaryTypeDef = TypedDict(
    "AgentStatusSummaryTypeDef",
    {
        "Id": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[AgentStatusTypeType],
        "LastModifiedTime": NotRequired[datetime],
        "LastModifiedRegion": NotRequired[str],
    },
)
AgentStatusTypeDef = TypedDict(
    "AgentStatusTypeDef",
    {
        "AgentStatusARN": NotRequired[str],
        "AgentStatusId": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "Type": NotRequired[AgentStatusTypeType],
        "DisplayOrder": NotRequired[int],
        "State": NotRequired[AgentStatusStateType],
        "Tags": NotRequired[Dict[str, str]],
        "LastModifiedTime": NotRequired[datetime],
        "LastModifiedRegion": NotRequired[str],
    },
)


class AgentsCriteriaOutputTypeDef(TypedDict):
    AgentIds: NotRequired[List[str]]


class AgentsCriteriaTypeDef(TypedDict):
    AgentIds: NotRequired[Sequence[str]]


class AnalyticsDataAssociationResultTypeDef(TypedDict):
    DataSetId: NotRequired[str]
    TargetAccountId: NotRequired[str]
    ResourceShareId: NotRequired[str]
    ResourceShareArn: NotRequired[str]


class AnswerMachineDetectionConfigTypeDef(TypedDict):
    EnableAnswerMachineDetection: NotRequired[bool]
    AwaitAnswerMachinePrompt: NotRequired[bool]


class ApplicationOutputTypeDef(TypedDict):
    Namespace: NotRequired[str]
    ApplicationPermissions: NotRequired[List[str]]


class ApplicationTypeDef(TypedDict):
    Namespace: NotRequired[str]
    ApplicationPermissions: NotRequired[Sequence[str]]


class AssociateAnalyticsDataSetRequestRequestTypeDef(TypedDict):
    InstanceId: str
    DataSetId: str
    TargetAccountId: NotRequired[str]


class AssociateApprovedOriginRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Origin: str


class LexBotTypeDef(TypedDict):
    Name: str
    LexRegion: str


class LexV2BotTypeDef(TypedDict):
    AliasArn: NotRequired[str]


class AssociateDefaultVocabularyRequestRequestTypeDef(TypedDict):
    InstanceId: str
    LanguageCode: VocabularyLanguageCodeType
    VocabularyId: NotRequired[str]


class AssociateFlowRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ResourceId: str
    FlowId: str
    ResourceType: FlowAssociationResourceTypeType


class AssociateLambdaFunctionRequestRequestTypeDef(TypedDict):
    InstanceId: str
    FunctionArn: str


class AssociatePhoneNumberContactFlowRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str
    InstanceId: str
    ContactFlowId: str


class AssociateQueueQuickConnectsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QueueId: str
    QuickConnectIds: Sequence[str]


class AssociateSecurityKeyRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Key: str


class AssociateTrafficDistributionGroupUserRequestRequestTypeDef(TypedDict):
    TrafficDistributionGroupId: str
    UserId: str
    InstanceId: str


class UserProficiencyTypeDef(TypedDict):
    AttributeName: str
    AttributeValue: str
    Level: float


class AssociatedContactSummaryTypeDef(TypedDict):
    ContactId: NotRequired[str]
    ContactArn: NotRequired[str]
    InitiationTimestamp: NotRequired[datetime]
    DisconnectTimestamp: NotRequired[datetime]
    InitialContactId: NotRequired[str]
    PreviousContactId: NotRequired[str]
    RelatedContactId: NotRequired[str]
    InitiationMethod: NotRequired[ContactInitiationMethodType]
    Channel: NotRequired[ChannelType]


class AttachedFileErrorTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]
    FileId: NotRequired[str]


class CreatedByInfoTypeDef(TypedDict):
    ConnectUserArn: NotRequired[str]
    AWSIdentityArn: NotRequired[str]


class AttachmentReferenceTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]
    Status: NotRequired[ReferenceStatusType]
    Arn: NotRequired[str]


class AttendeeTypeDef(TypedDict):
    AttendeeId: NotRequired[str]
    JoinToken: NotRequired[str]


class HierarchyGroupConditionTypeDef(TypedDict):
    Value: NotRequired[str]
    HierarchyGroupMatchType: NotRequired[HierarchyGroupMatchTypeType]


class TagConditionTypeDef(TypedDict):
    TagKey: NotRequired[str]
    TagValue: NotRequired[str]


class AttributeTypeDef(TypedDict):
    AttributeType: NotRequired[InstanceAttributeTypeType]
    Value: NotRequired[str]


class AudioFeaturesTypeDef(TypedDict):
    EchoReduction: NotRequired[MeetingFeatureStatusType]


class AuthenticationProfileSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    IsDefault: NotRequired[bool]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class AuthenticationProfileTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    AllowedIps: NotRequired[List[str]]
    BlockedIps: NotRequired[List[str]]
    IsDefault: NotRequired[bool]
    CreatedTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]
    PeriodicSessionDuration: NotRequired[int]
    MaxSessionDuration: NotRequired[int]


class AvailableNumberSummaryTypeDef(TypedDict):
    PhoneNumber: NotRequired[str]
    PhoneNumberCountryCode: NotRequired[PhoneNumberCountryCodeType]
    PhoneNumberType: NotRequired[PhoneNumberTypeType]


class BatchAssociateAnalyticsDataSetRequestRequestTypeDef(TypedDict):
    InstanceId: str
    DataSetIds: Sequence[str]
    TargetAccountId: NotRequired[str]


class ErrorResultTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]


class BatchDisassociateAnalyticsDataSetRequestRequestTypeDef(TypedDict):
    InstanceId: str
    DataSetIds: Sequence[str]
    TargetAccountId: NotRequired[str]


class BatchGetAttachedFileMetadataRequestRequestTypeDef(TypedDict):
    FileIds: Sequence[str]
    InstanceId: str
    AssociatedResourceArn: str


class BatchGetFlowAssociationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ResourceIds: Sequence[str]
    ResourceType: NotRequired[ListFlowAssociationResourceTypeType]


class FlowAssociationSummaryTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    FlowId: NotRequired[str]
    ResourceType: NotRequired[ListFlowAssociationResourceTypeType]


class FailedRequestTypeDef(TypedDict):
    RequestIdentifier: NotRequired[str]
    FailureReasonCode: NotRequired[FailureReasonCodeType]
    FailureReasonMessage: NotRequired[str]


class SuccessfulRequestTypeDef(TypedDict):
    RequestIdentifier: NotRequired[str]
    ContactId: NotRequired[str]


class CampaignTypeDef(TypedDict):
    CampaignId: NotRequired[str]


ChatEventTypeDef = TypedDict(
    "ChatEventTypeDef",
    {
        "Type": ChatEventTypeType,
        "ContentType": NotRequired[str],
        "Content": NotRequired[str],
    },
)


class ChatMessageTypeDef(TypedDict):
    ContentType: str
    Content: str


class ChatStreamingConfigurationTypeDef(TypedDict):
    StreamingEndpointArn: str


class ClaimPhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumber: str
    TargetArn: NotRequired[str]
    InstanceId: NotRequired[str]
    PhoneNumberDescription: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]


class PhoneNumberStatusTypeDef(TypedDict):
    Status: NotRequired[PhoneNumberWorkflowStatusType]
    Message: NotRequired[str]


class CompleteAttachedFileUploadRequestRequestTypeDef(TypedDict):
    InstanceId: str
    FileId: str
    AssociatedResourceArn: str


NumberConditionTypeDef = TypedDict(
    "NumberConditionTypeDef",
    {
        "FieldName": NotRequired[str],
        "MinValue": NotRequired[int],
        "MaxValue": NotRequired[int],
        "ComparisonType": NotRequired[NumberComparisonTypeType],
    },
)
EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "Type": NotRequired[EndpointTypeType],
        "Address": NotRequired[str],
    },
)


class ContactFilterTypeDef(TypedDict):
    ContactStates: NotRequired[Sequence[ContactStateType]]


class ContactFlowModuleSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    State: NotRequired[ContactFlowModuleStateType]


class ContactFlowModuleTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]
    Content: NotRequired[str]
    Description: NotRequired[str]
    State: NotRequired[ContactFlowModuleStateType]
    Status: NotRequired[ContactFlowModuleStatusType]
    Tags: NotRequired[Dict[str, str]]


class ContactFlowSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    ContactFlowType: NotRequired[ContactFlowTypeType]
    ContactFlowState: NotRequired[ContactFlowStateType]
    ContactFlowStatus: NotRequired[ContactFlowStatusType]


ContactFlowTypeDef = TypedDict(
    "ContactFlowTypeDef",
    {
        "Arn": NotRequired[str],
        "Id": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[ContactFlowTypeType],
        "State": NotRequired[ContactFlowStateType],
        "Status": NotRequired[ContactFlowStatusType],
        "Description": NotRequired[str],
        "Content": NotRequired[str],
        "Tags": NotRequired[Dict[str, str]],
        "FlowContentSha256": NotRequired[str],
        "Version": NotRequired[int],
        "VersionDescription": NotRequired[str],
        "LastModifiedTime": NotRequired[datetime],
        "LastModifiedRegion": NotRequired[str],
    },
)


class ContactFlowVersionSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    VersionDescription: NotRequired[str]
    Version: NotRequired[int]


class ContactSearchSummaryAgentInfoTypeDef(TypedDict):
    Id: NotRequired[str]
    ConnectedToAgentTimestamp: NotRequired[datetime]


class ContactSearchSummaryQueueInfoTypeDef(TypedDict):
    Id: NotRequired[str]
    EnqueueTimestamp: NotRequired[datetime]


class ContactSearchSummarySegmentAttributeValueTypeDef(TypedDict):
    ValueString: NotRequired[str]


class CustomerVoiceActivityTypeDef(TypedDict):
    GreetingStartTimestamp: NotRequired[datetime]
    GreetingEndTimestamp: NotRequired[datetime]


class DisconnectDetailsTypeDef(TypedDict):
    PotentialDisconnectIssue: NotRequired[str]


EndpointInfoTypeDef = TypedDict(
    "EndpointInfoTypeDef",
    {
        "Type": NotRequired[EndpointTypeType],
        "Address": NotRequired[str],
        "DisplayName": NotRequired[str],
    },
)


class QueueInfoTypeDef(TypedDict):
    Id: NotRequired[str]
    EnqueueTimestamp: NotRequired[datetime]


class SegmentAttributeValueOutputTypeDef(TypedDict):
    ValueString: NotRequired[str]
    ValueMap: NotRequired[Dict[str, Dict[str, Any]]]
    ValueInteger: NotRequired[int]


class WisdomInfoTypeDef(TypedDict):
    SessionArn: NotRequired[str]


class CreateAgentStatusRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str
    State: AgentStatusStateType
    Description: NotRequired[str]
    DisplayOrder: NotRequired[int]
    Tags: NotRequired[Mapping[str, str]]


class CreateContactFlowModuleRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str
    Content: str
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]


CreateContactFlowRequestRequestTypeDef = TypedDict(
    "CreateContactFlowRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Name": str,
        "Type": ContactFlowTypeType,
        "Content": str,
        "Description": NotRequired[str],
        "Status": NotRequired[ContactFlowStatusType],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
TimestampTypeDef = Union[datetime, str]
ReferenceTypeDef = TypedDict(
    "ReferenceTypeDef",
    {
        "Type": ReferenceTypeType,
        "Value": NotRequired[str],
        "Status": NotRequired[ReferenceStatusType],
        "Arn": NotRequired[str],
        "StatusReason": NotRequired[str],
    },
)


class UserInfoTypeDef(TypedDict):
    UserId: NotRequired[str]


class CreateEmailAddressRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EmailAddress: str
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]


class EvaluationFormScoringStrategyTypeDef(TypedDict):
    Mode: EvaluationFormScoringModeType
    Status: EvaluationFormScoringStatusType


class CreateInstanceRequestRequestTypeDef(TypedDict):
    IdentityManagementType: DirectoryTypeType
    InboundCallsEnabled: bool
    OutboundCallsEnabled: bool
    ClientToken: NotRequired[str]
    InstanceAlias: NotRequired[str]
    DirectoryId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class CreateIntegrationAssociationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    IntegrationType: IntegrationTypeType
    IntegrationArn: str
    SourceApplicationUrl: NotRequired[str]
    SourceApplicationName: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]
    Tags: NotRequired[Mapping[str, str]]


class ParticipantDetailsToAddTypeDef(TypedDict):
    ParticipantRole: NotRequired[ParticipantRoleType]
    DisplayName: NotRequired[str]


class ParticipantTokenCredentialsTypeDef(TypedDict):
    ParticipantToken: NotRequired[str]
    Expiry: NotRequired[str]


class CreatePersistentContactAssociationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    InitialContactId: str
    RehydrationType: RehydrationTypeType
    SourceContactId: str
    ClientToken: NotRequired[str]


class PredefinedAttributeValuesTypeDef(TypedDict):
    StringList: NotRequired[Sequence[str]]


class CreatePromptRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str
    S3Uri: str
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class OutboundCallerConfigTypeDef(TypedDict):
    OutboundCallerIdName: NotRequired[str]
    OutboundCallerIdNumberId: NotRequired[str]
    OutboundFlowId: NotRequired[str]


class OutboundEmailConfigTypeDef(TypedDict):
    OutboundEmailAddressId: NotRequired[str]


class RuleTriggerEventSourceTypeDef(TypedDict):
    EventSourceName: EventSourceNameType
    IntegrationAssociationId: NotRequired[str]


class CreateTrafficDistributionGroupRequestRequestTypeDef(TypedDict):
    Name: str
    InstanceId: str
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class CreateUseCaseRequestRequestTypeDef(TypedDict):
    InstanceId: str
    IntegrationAssociationId: str
    UseCaseType: UseCaseTypeType
    Tags: NotRequired[Mapping[str, str]]


class CreateUserHierarchyGroupRequestRequestTypeDef(TypedDict):
    Name: str
    InstanceId: str
    ParentGroupId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class UserIdentityInfoTypeDef(TypedDict):
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    Email: NotRequired[str]
    SecondaryEmail: NotRequired[str]
    Mobile: NotRequired[str]


class UserPhoneConfigTypeDef(TypedDict):
    PhoneType: PhoneTypeType
    AutoAccept: NotRequired[bool]
    AfterContactWorkTimeLimit: NotRequired[int]
    DeskPhoneNumber: NotRequired[str]


class ViewInputContentTypeDef(TypedDict):
    Template: NotRequired[str]
    Actions: NotRequired[Sequence[str]]


class CreateViewVersionRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ViewId: str
    VersionDescription: NotRequired[str]
    ViewContentSha256: NotRequired[str]


class CreateVocabularyRequestRequestTypeDef(TypedDict):
    InstanceId: str
    VocabularyName: str
    LanguageCode: VocabularyLanguageCodeType
    Content: str
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class CredentialsTypeDef(TypedDict):
    AccessToken: NotRequired[str]
    AccessTokenExpiration: NotRequired[datetime]
    RefreshToken: NotRequired[str]
    RefreshTokenExpiration: NotRequired[datetime]


class CrossChannelBehaviorTypeDef(TypedDict):
    BehaviorType: BehaviorTypeType


class CurrentMetricTypeDef(TypedDict):
    Name: NotRequired[CurrentMetricNameType]
    Unit: NotRequired[UnitType]


class CurrentMetricSortCriteriaTypeDef(TypedDict):
    SortByMetric: NotRequired[CurrentMetricNameType]
    SortOrder: NotRequired[SortOrderType]


class DateReferenceTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]


class DeactivateEvaluationFormRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EvaluationFormId: str
    EvaluationFormVersion: int


class DefaultVocabularyTypeDef(TypedDict):
    InstanceId: str
    LanguageCode: VocabularyLanguageCodeType
    VocabularyId: str
    VocabularyName: str


class DeleteAttachedFileRequestRequestTypeDef(TypedDict):
    InstanceId: str
    FileId: str
    AssociatedResourceArn: str


class DeleteContactEvaluationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EvaluationId: str


class DeleteContactFlowModuleRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactFlowModuleId: str


class DeleteContactFlowRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactFlowId: str


class DeleteEmailAddressRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EmailAddressId: str


class DeleteEvaluationFormRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EvaluationFormId: str
    EvaluationFormVersion: NotRequired[int]


class DeleteHoursOfOperationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    HoursOfOperationId: str


class DeleteInstanceRequestRequestTypeDef(TypedDict):
    InstanceId: str


class DeleteIntegrationAssociationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    IntegrationAssociationId: str


class DeletePredefinedAttributeRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str


class DeletePromptRequestRequestTypeDef(TypedDict):
    InstanceId: str
    PromptId: str


class DeleteQueueRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QueueId: str


class DeleteQuickConnectRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QuickConnectId: str


class DeleteRoutingProfileRequestRequestTypeDef(TypedDict):
    InstanceId: str
    RoutingProfileId: str


class DeleteRuleRequestRequestTypeDef(TypedDict):
    InstanceId: str
    RuleId: str


class DeleteSecurityProfileRequestRequestTypeDef(TypedDict):
    InstanceId: str
    SecurityProfileId: str


class DeleteTaskTemplateRequestRequestTypeDef(TypedDict):
    InstanceId: str
    TaskTemplateId: str


class DeleteTrafficDistributionGroupRequestRequestTypeDef(TypedDict):
    TrafficDistributionGroupId: str


class DeleteUseCaseRequestRequestTypeDef(TypedDict):
    InstanceId: str
    IntegrationAssociationId: str
    UseCaseId: str


class DeleteUserHierarchyGroupRequestRequestTypeDef(TypedDict):
    HierarchyGroupId: str
    InstanceId: str


class DeleteUserRequestRequestTypeDef(TypedDict):
    InstanceId: str
    UserId: str


class DeleteViewRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ViewId: str


class DeleteViewVersionRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ViewId: str
    ViewVersion: int


class DeleteVocabularyRequestRequestTypeDef(TypedDict):
    InstanceId: str
    VocabularyId: str


class DescribeAgentStatusRequestRequestTypeDef(TypedDict):
    InstanceId: str
    AgentStatusId: str


class DescribeAuthenticationProfileRequestRequestTypeDef(TypedDict):
    AuthenticationProfileId: str
    InstanceId: str


class DescribeContactEvaluationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EvaluationId: str


class DescribeContactFlowModuleRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactFlowModuleId: str


class DescribeContactFlowRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactFlowId: str


class DescribeContactRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str


class DescribeEmailAddressRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EmailAddressId: str


class DescribeEvaluationFormRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EvaluationFormId: str
    EvaluationFormVersion: NotRequired[int]


class DescribeHoursOfOperationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    HoursOfOperationId: str


class DescribeInstanceAttributeRequestRequestTypeDef(TypedDict):
    InstanceId: str
    AttributeType: InstanceAttributeTypeType


class DescribeInstanceRequestRequestTypeDef(TypedDict):
    InstanceId: str


class DescribeInstanceStorageConfigRequestRequestTypeDef(TypedDict):
    InstanceId: str
    AssociationId: str
    ResourceType: InstanceStorageResourceTypeType


class DescribePhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str


class DescribePredefinedAttributeRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str


class DescribePromptRequestRequestTypeDef(TypedDict):
    InstanceId: str
    PromptId: str


class PromptTypeDef(TypedDict):
    PromptARN: NotRequired[str]
    PromptId: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class DescribeQueueRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QueueId: str


class DescribeQuickConnectRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QuickConnectId: str


class DescribeRoutingProfileRequestRequestTypeDef(TypedDict):
    InstanceId: str
    RoutingProfileId: str


class DescribeRuleRequestRequestTypeDef(TypedDict):
    InstanceId: str
    RuleId: str


class DescribeSecurityProfileRequestRequestTypeDef(TypedDict):
    SecurityProfileId: str
    InstanceId: str


class SecurityProfileTypeDef(TypedDict):
    Id: NotRequired[str]
    OrganizationResourceId: NotRequired[str]
    Arn: NotRequired[str]
    SecurityProfileName: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]
    AllowedAccessControlTags: NotRequired[Dict[str, str]]
    TagRestrictedResources: NotRequired[List[str]]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]
    HierarchyRestrictedResources: NotRequired[List[str]]
    AllowedAccessControlHierarchyGroupId: NotRequired[str]


class DescribeTrafficDistributionGroupRequestRequestTypeDef(TypedDict):
    TrafficDistributionGroupId: str


class TrafficDistributionGroupTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    InstanceArn: NotRequired[str]
    Status: NotRequired[TrafficDistributionGroupStatusType]
    Tags: NotRequired[Dict[str, str]]
    IsDefault: NotRequired[bool]


class DescribeUserHierarchyGroupRequestRequestTypeDef(TypedDict):
    HierarchyGroupId: str
    InstanceId: str


class DescribeUserHierarchyStructureRequestRequestTypeDef(TypedDict):
    InstanceId: str


class DescribeUserRequestRequestTypeDef(TypedDict):
    UserId: str
    InstanceId: str


class DescribeViewRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ViewId: str


class DescribeVocabularyRequestRequestTypeDef(TypedDict):
    InstanceId: str
    VocabularyId: str


class VocabularyTypeDef(TypedDict):
    Name: str
    Id: str
    Arn: str
    LanguageCode: VocabularyLanguageCodeType
    State: VocabularyStateType
    LastModifiedTime: datetime
    FailureReason: NotRequired[str]
    Content: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]


class RoutingProfileReferenceTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]


class DisassociateAnalyticsDataSetRequestRequestTypeDef(TypedDict):
    InstanceId: str
    DataSetId: str
    TargetAccountId: NotRequired[str]


class DisassociateApprovedOriginRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Origin: str


class DisassociateFlowRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ResourceId: str
    ResourceType: FlowAssociationResourceTypeType


class DisassociateInstanceStorageConfigRequestRequestTypeDef(TypedDict):
    InstanceId: str
    AssociationId: str
    ResourceType: InstanceStorageResourceTypeType


class DisassociateLambdaFunctionRequestRequestTypeDef(TypedDict):
    InstanceId: str
    FunctionArn: str


class DisassociateLexBotRequestRequestTypeDef(TypedDict):
    InstanceId: str
    BotName: str
    LexRegion: str


class DisassociatePhoneNumberContactFlowRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str
    InstanceId: str


class DisassociateQueueQuickConnectsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QueueId: str
    QuickConnectIds: Sequence[str]


class RoutingProfileQueueReferenceTypeDef(TypedDict):
    QueueId: str
    Channel: ChannelType


class DisassociateSecurityKeyRequestRequestTypeDef(TypedDict):
    InstanceId: str
    AssociationId: str


class DisassociateTrafficDistributionGroupUserRequestRequestTypeDef(TypedDict):
    TrafficDistributionGroupId: str
    UserId: str
    InstanceId: str


class UserProficiencyDisassociateTypeDef(TypedDict):
    AttributeName: str
    AttributeValue: str


class DisconnectReasonTypeDef(TypedDict):
    Code: NotRequired[str]


class DismissUserContactRequestRequestTypeDef(TypedDict):
    UserId: str
    InstanceId: str
    ContactId: str


class DownloadUrlMetadataTypeDef(TypedDict):
    Url: NotRequired[str]
    UrlExpiry: NotRequired[str]


class EmailAddressInfoTypeDef(TypedDict):
    EmailAddress: str
    DisplayName: NotRequired[str]


class EmailAddressMetadataTypeDef(TypedDict):
    EmailAddressId: NotRequired[str]
    EmailAddressArn: NotRequired[str]
    EmailAddress: NotRequired[str]
    Description: NotRequired[str]
    DisplayName: NotRequired[str]


class EmailAttachmentTypeDef(TypedDict):
    FileName: str
    S3Url: str


class EmailMessageReferenceTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]


class EmailReferenceTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]


class EncryptionConfigTypeDef(TypedDict):
    EncryptionType: Literal["KMS"]
    KeyId: str


class EvaluationAnswerDataTypeDef(TypedDict):
    StringValue: NotRequired[str]
    NumericValue: NotRequired[float]
    NotApplicable: NotRequired[bool]


class EvaluationFormSectionOutputTypeDef(TypedDict):
    Title: str
    RefId: str
    Items: List[Dict[str, Any]]
    Instructions: NotRequired[str]
    Weight: NotRequired[float]


class NumericQuestionPropertyValueAutomationTypeDef(TypedDict):
    Label: NumericQuestionPropertyAutomationLabelType


class EvaluationFormNumericQuestionOptionTypeDef(TypedDict):
    MinValue: int
    MaxValue: int
    Score: NotRequired[int]
    AutomaticFail: NotRequired[bool]


class EvaluationFormSectionTypeDef(TypedDict):
    Title: str
    RefId: str
    Items: Sequence[Mapping[str, Any]]
    Instructions: NotRequired[str]
    Weight: NotRequired[float]


class SingleSelectQuestionRuleCategoryAutomationTypeDef(TypedDict):
    Category: str
    Condition: SingleSelectQuestionRuleCategoryAutomationConditionType
    OptionRefId: str


EvaluationFormSingleSelectQuestionOptionTypeDef = TypedDict(
    "EvaluationFormSingleSelectQuestionOptionTypeDef",
    {
        "RefId": str,
        "Text": str,
        "Score": NotRequired[int],
        "AutomaticFail": NotRequired[bool],
    },
)


class EvaluationFormSummaryTypeDef(TypedDict):
    EvaluationFormId: str
    EvaluationFormArn: str
    Title: str
    CreatedTime: datetime
    CreatedBy: str
    LastModifiedTime: datetime
    LastModifiedBy: str
    LatestVersion: int
    LastActivatedTime: NotRequired[datetime]
    LastActivatedBy: NotRequired[str]
    ActiveVersion: NotRequired[int]


class EvaluationFormVersionSummaryTypeDef(TypedDict):
    EvaluationFormArn: str
    EvaluationFormId: str
    EvaluationFormVersion: int
    Locked: bool
    Status: EvaluationFormVersionStatusType
    CreatedTime: datetime
    CreatedBy: str
    LastModifiedTime: datetime
    LastModifiedBy: str


class EvaluationScoreTypeDef(TypedDict):
    Percentage: NotRequired[float]
    NotApplicable: NotRequired[bool]
    AutomaticFail: NotRequired[bool]


class EvaluationNoteTypeDef(TypedDict):
    Value: NotRequired[str]


class EventBridgeActionDefinitionTypeDef(TypedDict):
    Name: str


class ExpiryTypeDef(TypedDict):
    DurationInSeconds: NotRequired[int]
    ExpiryTimestamp: NotRequired[datetime]


class FieldValueUnionOutputTypeDef(TypedDict):
    BooleanValue: NotRequired[bool]
    DoubleValue: NotRequired[float]
    EmptyValue: NotRequired[Dict[str, Any]]
    StringValue: NotRequired[str]


class FieldValueUnionTypeDef(TypedDict):
    BooleanValue: NotRequired[bool]
    DoubleValue: NotRequired[float]
    EmptyValue: NotRequired[Mapping[str, Any]]
    StringValue: NotRequired[str]


class FilterV2TypeDef(TypedDict):
    FilterKey: NotRequired[str]
    FilterValues: NotRequired[Sequence[str]]


class FiltersTypeDef(TypedDict):
    Queues: NotRequired[Sequence[str]]
    Channels: NotRequired[Sequence[ChannelType]]
    RoutingProfiles: NotRequired[Sequence[str]]
    RoutingStepExpressions: NotRequired[Sequence[str]]


class GetAttachedFileRequestRequestTypeDef(TypedDict):
    InstanceId: str
    FileId: str
    AssociatedResourceArn: str
    UrlExpiryInSeconds: NotRequired[int]


class GetContactAttributesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    InitialContactId: str


class GetFederationTokenRequestRequestTypeDef(TypedDict):
    InstanceId: str


class GetFlowAssociationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ResourceId: str
    ResourceType: FlowAssociationResourceTypeType


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class IntervalDetailsTypeDef(TypedDict):
    TimeZone: NotRequired[str]
    IntervalPeriod: NotRequired[IntervalPeriodType]


class GetPromptFileRequestRequestTypeDef(TypedDict):
    InstanceId: str
    PromptId: str


class GetTaskTemplateRequestRequestTypeDef(TypedDict):
    InstanceId: str
    TaskTemplateId: str
    SnapshotVersion: NotRequired[str]


class GetTrafficDistributionRequestRequestTypeDef(TypedDict):
    Id: str


class HierarchyGroupSummaryReferenceTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]


class HierarchyGroupSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class HierarchyLevelTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class HierarchyLevelUpdateTypeDef(TypedDict):
    Name: str


class ThresholdTypeDef(TypedDict):
    Comparison: NotRequired[Literal["LT"]]
    ThresholdValue: NotRequired[float]


class HoursOfOperationTimeSliceTypeDef(TypedDict):
    Hours: int
    Minutes: int


class HoursOfOperationSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class ImportPhoneNumberRequestRequestTypeDef(TypedDict):
    InstanceId: str
    SourcePhoneNumberArn: str
    PhoneNumberDescription: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]


class InboundRawMessageTypeDef(TypedDict):
    Subject: str
    Body: str
    ContentType: str
    Headers: NotRequired[Mapping[EmailHeaderTypeType, str]]


class InstanceStatusReasonTypeDef(TypedDict):
    Message: NotRequired[str]


class KinesisFirehoseConfigTypeDef(TypedDict):
    FirehoseArn: str


class KinesisStreamConfigTypeDef(TypedDict):
    StreamArn: str


class InstanceSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    IdentityManagementType: NotRequired[DirectoryTypeType]
    InstanceAlias: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    ServiceRole: NotRequired[str]
    InstanceStatus: NotRequired[InstanceStatusType]
    InboundCallsEnabled: NotRequired[bool]
    OutboundCallsEnabled: NotRequired[bool]
    InstanceAccessUrl: NotRequired[str]


class IntegrationAssociationSummaryTypeDef(TypedDict):
    IntegrationAssociationId: NotRequired[str]
    IntegrationAssociationArn: NotRequired[str]
    InstanceId: NotRequired[str]
    IntegrationType: NotRequired[IntegrationTypeType]
    IntegrationArn: NotRequired[str]
    SourceApplicationUrl: NotRequired[str]
    SourceApplicationName: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]


class TaskTemplateFieldIdentifierTypeDef(TypedDict):
    Name: NotRequired[str]


class ListAgentStatusRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    AgentStatusTypes: NotRequired[Sequence[AgentStatusTypeType]]


class ListAnalyticsDataAssociationsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    DataSetId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListApprovedOriginsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAssociatedContactsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListAuthenticationProfilesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListBotsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    LexVersion: LexVersionType
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListContactEvaluationsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    NextToken: NotRequired[str]


class ListContactFlowModulesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ContactFlowModuleState: NotRequired[ContactFlowModuleStateType]


class ListContactFlowVersionsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactFlowId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListContactFlowsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactFlowTypes: NotRequired[Sequence[ContactFlowTypeType]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListContactReferencesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    ReferenceTypes: Sequence[ReferenceTypeType]
    NextToken: NotRequired[str]


class ListDefaultVocabulariesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    LanguageCode: NotRequired[VocabularyLanguageCodeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListEvaluationFormVersionsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EvaluationFormId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListEvaluationFormsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListFlowAssociationsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ResourceType: NotRequired[ListFlowAssociationResourceTypeType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListHoursOfOperationsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListInstanceAttributesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListInstanceStorageConfigsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ResourceType: InstanceStorageResourceTypeType
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListInstancesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListIntegrationAssociationsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    IntegrationType: NotRequired[IntegrationTypeType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    IntegrationArn: NotRequired[str]


class ListLambdaFunctionsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListLexBotsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListPhoneNumbersRequestRequestTypeDef(TypedDict):
    InstanceId: str
    PhoneNumberTypes: NotRequired[Sequence[PhoneNumberTypeType]]
    PhoneNumberCountryCodes: NotRequired[Sequence[PhoneNumberCountryCodeType]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class PhoneNumberSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    PhoneNumber: NotRequired[str]
    PhoneNumberType: NotRequired[PhoneNumberTypeType]
    PhoneNumberCountryCode: NotRequired[PhoneNumberCountryCodeType]


class ListPhoneNumbersSummaryTypeDef(TypedDict):
    PhoneNumberId: NotRequired[str]
    PhoneNumberArn: NotRequired[str]
    PhoneNumber: NotRequired[str]
    PhoneNumberCountryCode: NotRequired[PhoneNumberCountryCodeType]
    PhoneNumberType: NotRequired[PhoneNumberTypeType]
    TargetArn: NotRequired[str]
    InstanceId: NotRequired[str]
    PhoneNumberDescription: NotRequired[str]
    SourcePhoneNumberArn: NotRequired[str]


class ListPhoneNumbersV2RequestRequestTypeDef(TypedDict):
    TargetArn: NotRequired[str]
    InstanceId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    PhoneNumberCountryCodes: NotRequired[Sequence[PhoneNumberCountryCodeType]]
    PhoneNumberTypes: NotRequired[Sequence[PhoneNumberTypeType]]
    PhoneNumberPrefix: NotRequired[str]


class ListPredefinedAttributesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class PredefinedAttributeSummaryTypeDef(TypedDict):
    Name: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class ListPromptsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class PromptSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class ListQueueQuickConnectsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QueueId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class QuickConnectSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    QuickConnectType: NotRequired[QuickConnectTypeType]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class ListQueuesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QueueTypes: NotRequired[Sequence[QueueTypeType]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class QueueSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    QueueType: NotRequired[QueueTypeType]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class ListQuickConnectsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    QuickConnectTypes: NotRequired[Sequence[QuickConnectTypeType]]


class ListRealtimeContactAnalysisSegmentsV2RequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    OutputType: RealTimeContactAnalysisOutputTypeType
    SegmentTypes: Sequence[RealTimeContactAnalysisSegmentTypeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListRoutingProfileQueuesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    RoutingProfileId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class RoutingProfileQueueConfigSummaryTypeDef(TypedDict):
    QueueId: str
    QueueArn: str
    QueueName: str
    Priority: int
    Delay: int
    Channel: ChannelType


class ListRoutingProfilesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class RoutingProfileSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class ListRulesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    PublishStatus: NotRequired[RulePublishStatusType]
    EventSourceName: NotRequired[EventSourceNameType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListSecurityKeysRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SecurityKeyTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    Key: NotRequired[str]
    CreationTime: NotRequired[datetime]


class ListSecurityProfileApplicationsRequestRequestTypeDef(TypedDict):
    SecurityProfileId: str
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListSecurityProfilePermissionsRequestRequestTypeDef(TypedDict):
    SecurityProfileId: str
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListSecurityProfilesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SecurityProfileSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class ListTaskTemplatesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Status: NotRequired[TaskTemplateStatusType]
    Name: NotRequired[str]


class TaskTemplateMetadataTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[TaskTemplateStatusType]
    LastModifiedTime: NotRequired[datetime]
    CreatedTime: NotRequired[datetime]


class ListTrafficDistributionGroupUsersRequestRequestTypeDef(TypedDict):
    TrafficDistributionGroupId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class TrafficDistributionGroupUserSummaryTypeDef(TypedDict):
    UserId: NotRequired[str]


class ListTrafficDistributionGroupsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    InstanceId: NotRequired[str]


class TrafficDistributionGroupSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    InstanceArn: NotRequired[str]
    Status: NotRequired[TrafficDistributionGroupStatusType]
    IsDefault: NotRequired[bool]


class ListUseCasesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    IntegrationAssociationId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class UseCaseTypeDef(TypedDict):
    UseCaseId: NotRequired[str]
    UseCaseArn: NotRequired[str]
    UseCaseType: NotRequired[UseCaseTypeType]


class ListUserHierarchyGroupsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListUserProficienciesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    UserId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListUsersRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class UserSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Username: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class ListViewVersionsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ViewId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


ViewVersionSummaryTypeDef = TypedDict(
    "ViewVersionSummaryTypeDef",
    {
        "Id": NotRequired[str],
        "Arn": NotRequired[str],
        "Description": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[ViewTypeType],
        "Version": NotRequired[int],
        "VersionDescription": NotRequired[str],
    },
)
ListViewsRequestRequestTypeDef = TypedDict(
    "ListViewsRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Type": NotRequired[ViewTypeType],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ViewSummaryTypeDef = TypedDict(
    "ViewSummaryTypeDef",
    {
        "Id": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[ViewTypeType],
        "Status": NotRequired[ViewStatusType],
        "Description": NotRequired[str],
    },
)


class MediaPlacementTypeDef(TypedDict):
    AudioHostUrl: NotRequired[str]
    AudioFallbackUrl: NotRequired[str]
    SignalingUrl: NotRequired[str]
    TurnControlUrl: NotRequired[str]
    EventIngestionUrl: NotRequired[str]


class MetricFilterV2OutputTypeDef(TypedDict):
    MetricFilterKey: NotRequired[str]
    MetricFilterValues: NotRequired[List[str]]
    Negate: NotRequired[bool]


class MetricFilterV2TypeDef(TypedDict):
    MetricFilterKey: NotRequired[str]
    MetricFilterValues: NotRequired[Sequence[str]]
    Negate: NotRequired[bool]


class MetricIntervalTypeDef(TypedDict):
    Interval: NotRequired[IntervalPeriodType]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]


class ThresholdV2TypeDef(TypedDict):
    Comparison: NotRequired[str]
    ThresholdValue: NotRequired[float]


class MonitorContactRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    UserId: str
    AllowedMonitorCapabilities: NotRequired[Sequence[MonitorCapabilityType]]
    ClientToken: NotRequired[str]


class ParticipantDetailsTypeDef(TypedDict):
    DisplayName: str


class NotificationRecipientTypeOutputTypeDef(TypedDict):
    UserTags: NotRequired[Dict[str, str]]
    UserIds: NotRequired[List[str]]


class NotificationRecipientTypeTypeDef(TypedDict):
    UserTags: NotRequired[Mapping[str, str]]
    UserIds: NotRequired[Sequence[str]]


class NumberReferenceTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]


class OutboundRawMessageTypeDef(TypedDict):
    Subject: str
    Body: str
    ContentType: str


class ParticipantTimerValueTypeDef(TypedDict):
    ParticipantTimerAction: NotRequired[Literal["Unset"]]
    ParticipantTimerDurationInMinutes: NotRequired[int]


class PauseContactRequestRequestTypeDef(TypedDict):
    ContactId: str
    InstanceId: str
    ContactFlowId: NotRequired[str]


class PersistentChatTypeDef(TypedDict):
    RehydrationType: NotRequired[RehydrationTypeType]
    SourceContactId: NotRequired[str]


class PhoneNumberQuickConnectConfigTypeDef(TypedDict):
    PhoneNumber: str


class PredefinedAttributeValuesOutputTypeDef(TypedDict):
    StringList: NotRequired[List[str]]


class PutUserStatusRequestRequestTypeDef(TypedDict):
    UserId: str
    InstanceId: str
    AgentStatusId: str


class QueueInfoInputTypeDef(TypedDict):
    Id: NotRequired[str]


class QueueQuickConnectConfigTypeDef(TypedDict):
    QueueId: str
    ContactFlowId: str


class UserQuickConnectConfigTypeDef(TypedDict):
    UserId: str
    ContactFlowId: str


class RealTimeContactAnalysisAttachmentTypeDef(TypedDict):
    AttachmentName: str
    AttachmentId: str
    ContentType: NotRequired[str]
    Status: NotRequired[ArtifactStatusType]


class RealTimeContactAnalysisCharacterIntervalTypeDef(TypedDict):
    BeginOffsetChar: int
    EndOffsetChar: int


class RealTimeContactAnalysisTimeDataTypeDef(TypedDict):
    AbsoluteTime: NotRequired[datetime]


class RealTimeContactAnalysisSegmentPostContactSummaryTypeDef(TypedDict):
    Status: RealTimeContactAnalysisPostContactSummaryStatusType
    Content: NotRequired[str]
    FailureCode: NotRequired[RealTimeContactAnalysisPostContactSummaryFailureCodeType]


class StringReferenceTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]


class UrlReferenceTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]


class ReleasePhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str
    ClientToken: NotRequired[str]


class ReplicateInstanceRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ReplicaRegion: str
    ReplicaAlias: str
    ClientToken: NotRequired[str]


class ReplicationStatusSummaryTypeDef(TypedDict):
    Region: NotRequired[str]
    ReplicationStatus: NotRequired[InstanceReplicationStatusType]
    ReplicationStatusReason: NotRequired[str]


class TagSearchConditionTypeDef(TypedDict):
    tagKey: NotRequired[str]
    tagValue: NotRequired[str]
    tagKeyComparisonType: NotRequired[StringComparisonTypeType]
    tagValueComparisonType: NotRequired[StringComparisonTypeType]


class ResumeContactRecordingRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    InitialContactId: str
    ContactRecordingType: NotRequired[ContactRecordingTypeType]


class ResumeContactRequestRequestTypeDef(TypedDict):
    ContactId: str
    InstanceId: str
    ContactFlowId: NotRequired[str]


class RoutingCriteriaInputStepExpiryTypeDef(TypedDict):
    DurationInSeconds: NotRequired[int]


class SubmitAutoEvaluationActionDefinitionTypeDef(TypedDict):
    EvaluationFormId: str


class SearchAvailablePhoneNumbersRequestRequestTypeDef(TypedDict):
    PhoneNumberCountryCode: PhoneNumberCountryCodeType
    PhoneNumberType: PhoneNumberTypeType
    TargetArn: NotRequired[str]
    InstanceId: NotRequired[str]
    PhoneNumberPrefix: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class SortTypeDef(TypedDict):
    FieldName: SortableFieldNameType
    Order: SortOrderType


class TagSetTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]


class SecurityProfileSearchSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    OrganizationResourceId: NotRequired[str]
    Arn: NotRequired[str]
    SecurityProfileName: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]


class SearchVocabulariesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    State: NotRequired[VocabularyStateType]
    NameStartsWith: NotRequired[str]
    LanguageCode: NotRequired[VocabularyLanguageCodeType]


class VocabularySummaryTypeDef(TypedDict):
    Name: str
    Id: str
    Arn: str
    LanguageCode: VocabularyLanguageCodeType
    State: VocabularyStateType
    LastModifiedTime: datetime
    FailureReason: NotRequired[str]


class SearchableContactAttributesCriteriaTypeDef(TypedDict):
    Key: str
    Values: Sequence[str]


class SearchableSegmentAttributesCriteriaTypeDef(TypedDict):
    Key: str
    Values: Sequence[str]


class SegmentAttributeValueTypeDef(TypedDict):
    ValueString: NotRequired[str]
    ValueMap: NotRequired[Mapping[str, Mapping[str, Any]]]
    ValueInteger: NotRequired[int]


class SourceCampaignTypeDef(TypedDict):
    CampaignId: NotRequired[str]
    OutboundRequestId: NotRequired[str]


class SignInDistributionTypeDef(TypedDict):
    Region: str
    Enabled: bool


class UploadUrlMetadataTypeDef(TypedDict):
    Url: NotRequired[str]
    UrlExpiry: NotRequired[str]
    HeadersToInclude: NotRequired[Dict[str, str]]


class StartContactEvaluationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    EvaluationFormId: str
    ClientToken: NotRequired[str]


class VoiceRecordingConfigurationTypeDef(TypedDict):
    VoiceRecordingTrack: NotRequired[VoiceRecordingTrackType]
    IvrRecordingTrack: NotRequired[Literal["ALL"]]


class StartScreenSharingRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    ClientToken: NotRequired[str]


class StopContactRecordingRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    InitialContactId: str
    ContactRecordingType: NotRequired[ContactRecordingTypeType]


class StopContactStreamingRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    StreamingId: str


class SuspendContactRecordingRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    InitialContactId: str
    ContactRecordingType: NotRequired[ContactRecordingTypeType]


class TagContactRequestRequestTypeDef(TypedDict):
    ContactId: str
    InstanceId: str
    Tags: Mapping[str, str]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class TemplateAttributesTypeDef(TypedDict):
    CustomAttributes: NotRequired[Mapping[str, str]]
    CustomerProfileAttributes: NotRequired[str]


class TranscriptCriteriaTypeDef(TypedDict):
    ParticipantRole: ParticipantRoleType
    SearchText: Sequence[str]
    MatchType: SearchContactsMatchTypeType


class TransferContactRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    ContactFlowId: str
    QueueId: NotRequired[str]
    UserId: NotRequired[str]
    ClientToken: NotRequired[str]


class UntagContactRequestRequestTypeDef(TypedDict):
    ContactId: str
    InstanceId: str
    TagKeys: Sequence[str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateAgentStatusRequestRequestTypeDef(TypedDict):
    InstanceId: str
    AgentStatusId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    State: NotRequired[AgentStatusStateType]
    DisplayOrder: NotRequired[int]
    ResetOrderNumber: NotRequired[bool]


class UpdateAuthenticationProfileRequestRequestTypeDef(TypedDict):
    AuthenticationProfileId: str
    InstanceId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    AllowedIps: NotRequired[Sequence[str]]
    BlockedIps: NotRequired[Sequence[str]]
    PeriodicSessionDuration: NotRequired[int]


class UpdateContactAttributesRequestRequestTypeDef(TypedDict):
    InitialContactId: str
    InstanceId: str
    Attributes: Mapping[str, str]


class UpdateContactFlowContentRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactFlowId: str
    Content: str


class UpdateContactFlowMetadataRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactFlowId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    ContactFlowState: NotRequired[ContactFlowStateType]


class UpdateContactFlowModuleContentRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactFlowModuleId: str
    Content: str


class UpdateContactFlowModuleMetadataRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactFlowModuleId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    State: NotRequired[ContactFlowModuleStateType]


class UpdateContactFlowNameRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactFlowId: str
    Name: NotRequired[str]
    Description: NotRequired[str]


class UpdateEmailAddressMetadataRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EmailAddressId: str
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    ClientToken: NotRequired[str]


class UpdateInstanceAttributeRequestRequestTypeDef(TypedDict):
    InstanceId: str
    AttributeType: InstanceAttributeTypeType
    Value: str


class UpdatePhoneNumberMetadataRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str
    PhoneNumberDescription: NotRequired[str]
    ClientToken: NotRequired[str]


class UpdatePhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str
    TargetArn: NotRequired[str]
    InstanceId: NotRequired[str]
    ClientToken: NotRequired[str]


class UpdatePromptRequestRequestTypeDef(TypedDict):
    InstanceId: str
    PromptId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    S3Uri: NotRequired[str]


class UpdateQueueHoursOfOperationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QueueId: str
    HoursOfOperationId: str


class UpdateQueueMaxContactsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QueueId: str
    MaxContacts: NotRequired[int]


class UpdateQueueNameRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QueueId: str
    Name: NotRequired[str]
    Description: NotRequired[str]


class UpdateQueueStatusRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QueueId: str
    Status: QueueStatusType


class UpdateQuickConnectNameRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QuickConnectId: str
    Name: NotRequired[str]
    Description: NotRequired[str]


class UpdateRoutingProfileAgentAvailabilityTimerRequestRequestTypeDef(TypedDict):
    InstanceId: str
    RoutingProfileId: str
    AgentAvailabilityTimer: AgentAvailabilityTimerType


class UpdateRoutingProfileDefaultOutboundQueueRequestRequestTypeDef(TypedDict):
    InstanceId: str
    RoutingProfileId: str
    DefaultOutboundQueueId: str


class UpdateRoutingProfileNameRequestRequestTypeDef(TypedDict):
    InstanceId: str
    RoutingProfileId: str
    Name: NotRequired[str]
    Description: NotRequired[str]


class UpdateUserHierarchyGroupNameRequestRequestTypeDef(TypedDict):
    Name: str
    HierarchyGroupId: str
    InstanceId: str


class UpdateUserHierarchyRequestRequestTypeDef(TypedDict):
    UserId: str
    InstanceId: str
    HierarchyGroupId: NotRequired[str]


class UpdateUserRoutingProfileRequestRequestTypeDef(TypedDict):
    RoutingProfileId: str
    UserId: str
    InstanceId: str


class UpdateUserSecurityProfilesRequestRequestTypeDef(TypedDict):
    SecurityProfileIds: Sequence[str]
    UserId: str
    InstanceId: str


class UpdateViewMetadataRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ViewId: str
    Name: NotRequired[str]
    Description: NotRequired[str]


class UserReferenceTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]


class UserIdentityInfoLiteTypeDef(TypedDict):
    FirstName: NotRequired[str]
    LastName: NotRequired[str]


class ViewContentTypeDef(TypedDict):
    InputSchema: NotRequired[str]
    Template: NotRequired[str]
    Actions: NotRequired[List[str]]


class RuleSummaryTypeDef(TypedDict):
    Name: str
    RuleId: str
    RuleArn: str
    EventSourceName: EventSourceNameType
    PublishStatus: RulePublishStatusType
    ActionSummaries: List[ActionSummaryTypeDef]
    CreatedTime: datetime
    LastUpdatedTime: datetime


class ActivateEvaluationFormResponseTypeDef(TypedDict):
    EvaluationFormId: str
    EvaluationFormArn: str
    EvaluationFormVersion: int
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateAnalyticsDataSetResponseTypeDef(TypedDict):
    DataSetId: str
    TargetAccountId: str
    ResourceShareId: str
    ResourceShareArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateInstanceStorageConfigResponseTypeDef(TypedDict):
    AssociationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateSecurityKeyResponseTypeDef(TypedDict):
    AssociationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ClaimPhoneNumberResponseTypeDef(TypedDict):
    PhoneNumberId: str
    PhoneNumberArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAgentStatusResponseTypeDef(TypedDict):
    AgentStatusARN: str
    AgentStatusId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContactFlowModuleResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContactFlowResponseTypeDef(TypedDict):
    ContactFlowId: str
    ContactFlowArn: str
    FlowContentSha256: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContactFlowVersionResponseTypeDef(TypedDict):
    ContactFlowArn: str
    Version: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContactResponseTypeDef(TypedDict):
    ContactId: str
    ContactArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEmailAddressResponseTypeDef(TypedDict):
    EmailAddressId: str
    EmailAddressArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEvaluationFormResponseTypeDef(TypedDict):
    EvaluationFormId: str
    EvaluationFormArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHoursOfOperationResponseTypeDef(TypedDict):
    HoursOfOperationId: str
    HoursOfOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInstanceResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIntegrationAssociationResponseTypeDef(TypedDict):
    IntegrationAssociationId: str
    IntegrationAssociationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePersistentContactAssociationResponseTypeDef(TypedDict):
    ContinuedFromContactId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePromptResponseTypeDef(TypedDict):
    PromptARN: str
    PromptId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateQueueResponseTypeDef(TypedDict):
    QueueArn: str
    QueueId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateQuickConnectResponseTypeDef(TypedDict):
    QuickConnectARN: str
    QuickConnectId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRoutingProfileResponseTypeDef(TypedDict):
    RoutingProfileArn: str
    RoutingProfileId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRuleResponseTypeDef(TypedDict):
    RuleArn: str
    RuleId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSecurityProfileResponseTypeDef(TypedDict):
    SecurityProfileId: str
    SecurityProfileArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTaskTemplateResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrafficDistributionGroupResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUseCaseResponseTypeDef(TypedDict):
    UseCaseId: str
    UseCaseArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserHierarchyGroupResponseTypeDef(TypedDict):
    HierarchyGroupId: str
    HierarchyGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserResponseTypeDef(TypedDict):
    UserId: str
    UserArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVocabularyResponseTypeDef(TypedDict):
    VocabularyArn: str
    VocabularyId: str
    State: VocabularyStateType
    ResponseMetadata: ResponseMetadataTypeDef


class DeactivateEvaluationFormResponseTypeDef(TypedDict):
    EvaluationFormId: str
    EvaluationFormArn: str
    EvaluationFormVersion: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVocabularyResponseTypeDef(TypedDict):
    VocabularyArn: str
    VocabularyId: str
    State: VocabularyStateType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEmailAddressResponseTypeDef(TypedDict):
    EmailAddressId: str
    EmailAddressArn: str
    EmailAddress: str
    DisplayName: str
    Description: str
    CreateTimestamp: str
    ModifiedTimestamp: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetContactAttributesResponseTypeDef(TypedDict):
    Attributes: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetFlowAssociationResponseTypeDef(TypedDict):
    ResourceId: str
    FlowId: str
    ResourceType: FlowAssociationResourceTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class GetPromptFileResponseTypeDef(TypedDict):
    PromptPresignedUrl: str
    LastModifiedTime: datetime
    LastModifiedRegion: str
    ResponseMetadata: ResponseMetadataTypeDef


class ImportPhoneNumberResponseTypeDef(TypedDict):
    PhoneNumberId: str
    PhoneNumberArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListApprovedOriginsResponseTypeDef(TypedDict):
    Origins: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListLambdaFunctionsResponseTypeDef(TypedDict):
    LambdaFunctions: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListSecurityProfilePermissionsResponseTypeDef(TypedDict):
    Permissions: List[str]
    LastModifiedTime: datetime
    LastModifiedRegion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class MonitorContactResponseTypeDef(TypedDict):
    ContactId: str
    ContactArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ReplicateInstanceResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class SendChatIntegrationEventResponseTypeDef(TypedDict):
    InitialContactId: str
    NewChatCreated: bool
    ResponseMetadata: ResponseMetadataTypeDef


class StartChatContactResponseTypeDef(TypedDict):
    ContactId: str
    ParticipantId: str
    ParticipantToken: str
    ContinuedFromContactId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartContactEvaluationResponseTypeDef(TypedDict):
    EvaluationId: str
    EvaluationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartContactStreamingResponseTypeDef(TypedDict):
    StreamingId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartEmailContactResponseTypeDef(TypedDict):
    ContactId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartOutboundChatContactResponseTypeDef(TypedDict):
    ContactId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartOutboundEmailContactResponseTypeDef(TypedDict):
    ContactId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartOutboundVoiceContactResponseTypeDef(TypedDict):
    ContactId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartTaskContactResponseTypeDef(TypedDict):
    ContactId: str
    ResponseMetadata: ResponseMetadataTypeDef


class SubmitContactEvaluationResponseTypeDef(TypedDict):
    EvaluationId: str
    EvaluationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class TransferContactResponseTypeDef(TypedDict):
    ContactId: str
    ContactArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateContactEvaluationResponseTypeDef(TypedDict):
    EvaluationId: str
    EvaluationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEmailAddressMetadataResponseTypeDef(TypedDict):
    EmailAddressId: str
    EmailAddressArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEvaluationFormResponseTypeDef(TypedDict):
    EvaluationFormId: str
    EvaluationFormArn: str
    EvaluationFormVersion: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePhoneNumberResponseTypeDef(TypedDict):
    PhoneNumberId: str
    PhoneNumberArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePromptResponseTypeDef(TypedDict):
    PromptARN: str
    PromptId: str
    ResponseMetadata: ResponseMetadataTypeDef


class AdditionalEmailRecipientsTypeDef(TypedDict):
    ToList: NotRequired[List[EmailRecipientTypeDef]]
    CcList: NotRequired[List[EmailRecipientTypeDef]]


class AgentConfigOutputTypeDef(TypedDict):
    Distributions: List[DistributionTypeDef]


class AgentConfigTypeDef(TypedDict):
    Distributions: Sequence[DistributionTypeDef]


class TelephonyConfigOutputTypeDef(TypedDict):
    Distributions: List[DistributionTypeDef]


class TelephonyConfigTypeDef(TypedDict):
    Distributions: Sequence[DistributionTypeDef]


class AgentContactReferenceTypeDef(TypedDict):
    ContactId: NotRequired[str]
    Channel: NotRequired[ChannelType]
    InitiationMethod: NotRequired[ContactInitiationMethodType]
    AgentContactState: NotRequired[ContactStateType]
    StateStartTimestamp: NotRequired[datetime]
    ConnectedToAgentTimestamp: NotRequired[datetime]
    Queue: NotRequired[QueueReferenceTypeDef]


class HierarchyGroupsTypeDef(TypedDict):
    Level1: NotRequired[AgentHierarchyGroupTypeDef]
    Level2: NotRequired[AgentHierarchyGroupTypeDef]
    Level3: NotRequired[AgentHierarchyGroupTypeDef]
    Level4: NotRequired[AgentHierarchyGroupTypeDef]
    Level5: NotRequired[AgentHierarchyGroupTypeDef]


class AllowedCapabilitiesTypeDef(TypedDict):
    Customer: NotRequired[ParticipantCapabilitiesTypeDef]
    Agent: NotRequired[ParticipantCapabilitiesTypeDef]


class CustomerTypeDef(TypedDict):
    DeviceInfo: NotRequired[DeviceInfoTypeDef]
    Capabilities: NotRequired[ParticipantCapabilitiesTypeDef]


class AgentQualityMetricsTypeDef(TypedDict):
    Audio: NotRequired[AudioQualityMetricsInfoTypeDef]


class CustomerQualityMetricsTypeDef(TypedDict):
    Audio: NotRequired[AudioQualityMetricsInfoTypeDef]


class AgentStatusSearchCriteriaPaginatorTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class AgentStatusSearchCriteriaTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class ContactFlowModuleSearchCriteriaPaginatorTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class ContactFlowModuleSearchCriteriaTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class ContactFlowSearchCriteriaPaginatorTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]
    TypeCondition: NotRequired[ContactFlowTypeType]
    StateCondition: NotRequired[ContactFlowStateType]
    StatusCondition: NotRequired[ContactFlowStatusType]


class ContactFlowSearchCriteriaTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]
    TypeCondition: NotRequired[ContactFlowTypeType]
    StateCondition: NotRequired[ContactFlowStateType]
    StatusCondition: NotRequired[ContactFlowStatusType]


class EmailAddressSearchCriteriaTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class HoursOfOperationSearchCriteriaPaginatorTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class HoursOfOperationSearchCriteriaTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class PredefinedAttributeSearchCriteriaPaginatorTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class PredefinedAttributeSearchCriteriaTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class PromptSearchCriteriaPaginatorTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class PromptSearchCriteriaTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class QueueSearchCriteriaPaginatorTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]
    QueueTypeCondition: NotRequired[Literal["STANDARD"]]


class QueueSearchCriteriaTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]
    QueueTypeCondition: NotRequired[Literal["STANDARD"]]


class QuickConnectSearchCriteriaPaginatorTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class QuickConnectSearchCriteriaTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class RoutingProfileSearchCriteriaPaginatorTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class RoutingProfileSearchCriteriaTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class SecurityProfileSearchCriteriaPaginatorTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class SecurityProfileSearchCriteriaTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class UserHierarchyGroupSearchCriteriaPaginatorTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class UserHierarchyGroupSearchCriteriaTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]


class ListAgentStatusResponseTypeDef(TypedDict):
    AgentStatusSummaryList: List[AgentStatusSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeAgentStatusResponseTypeDef(TypedDict):
    AgentStatus: AgentStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchAgentStatusesResponseTypeDef(TypedDict):
    AgentStatuses: List[AgentStatusTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MatchCriteriaOutputTypeDef(TypedDict):
    AgentsCriteria: NotRequired[AgentsCriteriaOutputTypeDef]


AgentsCriteriaUnionTypeDef = Union[AgentsCriteriaTypeDef, AgentsCriteriaOutputTypeDef]


class ListAnalyticsDataAssociationsResponseTypeDef(TypedDict):
    Results: List[AnalyticsDataAssociationResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListSecurityProfileApplicationsResponseTypeDef(TypedDict):
    Applications: List[ApplicationOutputTypeDef]
    LastModifiedTime: datetime
    LastModifiedRegion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


ApplicationUnionTypeDef = Union[ApplicationTypeDef, ApplicationOutputTypeDef]


class UpdateSecurityProfileRequestRequestTypeDef(TypedDict):
    SecurityProfileId: str
    InstanceId: str
    Description: NotRequired[str]
    Permissions: NotRequired[Sequence[str]]
    AllowedAccessControlTags: NotRequired[Mapping[str, str]]
    TagRestrictedResources: NotRequired[Sequence[str]]
    Applications: NotRequired[Sequence[ApplicationTypeDef]]
    HierarchyRestrictedResources: NotRequired[Sequence[str]]
    AllowedAccessControlHierarchyGroupId: NotRequired[str]


class AssociateLexBotRequestRequestTypeDef(TypedDict):
    InstanceId: str
    LexBot: LexBotTypeDef


class ListLexBotsResponseTypeDef(TypedDict):
    LexBots: List[LexBotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AssociateBotRequestRequestTypeDef(TypedDict):
    InstanceId: str
    LexBot: NotRequired[LexBotTypeDef]
    LexV2Bot: NotRequired[LexV2BotTypeDef]


class DisassociateBotRequestRequestTypeDef(TypedDict):
    InstanceId: str
    LexBot: NotRequired[LexBotTypeDef]
    LexV2Bot: NotRequired[LexV2BotTypeDef]


class LexBotConfigTypeDef(TypedDict):
    LexBot: NotRequired[LexBotTypeDef]
    LexV2Bot: NotRequired[LexV2BotTypeDef]


class AssociateUserProficienciesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    UserId: str
    UserProficiencies: Sequence[UserProficiencyTypeDef]


class ListUserProficienciesResponseTypeDef(TypedDict):
    UserProficiencyList: List[UserProficiencyTypeDef]
    LastModifiedTime: datetime
    LastModifiedRegion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateUserProficienciesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    UserId: str
    UserProficiencies: Sequence[UserProficiencyTypeDef]


class ListAssociatedContactsResponseTypeDef(TypedDict):
    ContactSummaryList: List[AssociatedContactSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AttachedFileTypeDef(TypedDict):
    CreationTime: str
    FileArn: str
    FileId: str
    FileName: str
    FileSizeInBytes: int
    FileStatus: FileStatusTypeType
    CreatedBy: NotRequired[CreatedByInfoTypeDef]
    FileUseCaseType: NotRequired[FileUseCaseTypeType]
    AssociatedResourceArn: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]


class StartAttachedFileUploadRequestRequestTypeDef(TypedDict):
    InstanceId: str
    FileName: str
    FileSizeInBytes: int
    FileUseCaseType: FileUseCaseTypeType
    AssociatedResourceArn: str
    ClientToken: NotRequired[str]
    UrlExpiryInSeconds: NotRequired[int]
    CreatedBy: NotRequired[CreatedByInfoTypeDef]
    Tags: NotRequired[Mapping[str, str]]


class AttributeAndConditionTypeDef(TypedDict):
    TagConditions: NotRequired[Sequence[TagConditionTypeDef]]
    HierarchyGroupCondition: NotRequired[HierarchyGroupConditionTypeDef]


class CommonAttributeAndConditionTypeDef(TypedDict):
    TagConditions: NotRequired[Sequence[TagConditionTypeDef]]


class ControlPlaneTagFilterTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Sequence[TagConditionTypeDef]]]
    AndConditions: NotRequired[Sequence[TagConditionTypeDef]]
    TagCondition: NotRequired[TagConditionTypeDef]


class DescribeInstanceAttributeResponseTypeDef(TypedDict):
    Attribute: AttributeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListInstanceAttributesResponseTypeDef(TypedDict):
    Attributes: List[AttributeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MeetingFeaturesConfigurationTypeDef(TypedDict):
    Audio: NotRequired[AudioFeaturesTypeDef]


class ListAuthenticationProfilesResponseTypeDef(TypedDict):
    AuthenticationProfileSummaryList: List[AuthenticationProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeAuthenticationProfileResponseTypeDef(TypedDict):
    AuthenticationProfile: AuthenticationProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchAvailablePhoneNumbersResponseTypeDef(TypedDict):
    AvailableNumbersList: List[AvailableNumberSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class BatchAssociateAnalyticsDataSetResponseTypeDef(TypedDict):
    Created: List[AnalyticsDataAssociationResultTypeDef]
    Errors: List[ErrorResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDisassociateAnalyticsDataSetResponseTypeDef(TypedDict):
    Deleted: List[str]
    Errors: List[ErrorResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetFlowAssociationResponseTypeDef(TypedDict):
    FlowAssociationSummaryList: List[FlowAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListFlowAssociationsResponseTypeDef(TypedDict):
    FlowAssociationSummaryList: List[FlowAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class BatchPutContactResponseTypeDef(TypedDict):
    SuccessfulRequestList: List[SuccessfulRequestTypeDef]
    FailedRequestList: List[FailedRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StartContactStreamingRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    ChatStreamingConfiguration: ChatStreamingConfigurationTypeDef
    ClientToken: str


class ClaimedPhoneNumberSummaryTypeDef(TypedDict):
    PhoneNumberId: NotRequired[str]
    PhoneNumberArn: NotRequired[str]
    PhoneNumber: NotRequired[str]
    PhoneNumberCountryCode: NotRequired[PhoneNumberCountryCodeType]
    PhoneNumberType: NotRequired[PhoneNumberTypeType]
    PhoneNumberDescription: NotRequired[str]
    TargetArn: NotRequired[str]
    InstanceId: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]
    PhoneNumberStatus: NotRequired[PhoneNumberStatusTypeDef]
    SourcePhoneNumberArn: NotRequired[str]


class ConditionTypeDef(TypedDict):
    StringCondition: NotRequired[StringConditionTypeDef]
    NumberCondition: NotRequired[NumberConditionTypeDef]


class ContactDataRequestTypeDef(TypedDict):
    SystemEndpoint: NotRequired[EndpointTypeDef]
    CustomerEndpoint: NotRequired[EndpointTypeDef]
    RequestIdentifier: NotRequired[str]
    QueueId: NotRequired[str]
    Attributes: NotRequired[Mapping[str, str]]
    Campaign: NotRequired[CampaignTypeDef]


class UserDataFiltersTypeDef(TypedDict):
    Queues: NotRequired[Sequence[str]]
    ContactFilter: NotRequired[ContactFilterTypeDef]
    RoutingProfiles: NotRequired[Sequence[str]]
    Agents: NotRequired[Sequence[str]]
    UserHierarchyGroups: NotRequired[Sequence[str]]


class ListContactFlowModulesResponseTypeDef(TypedDict):
    ContactFlowModulesSummaryList: List[ContactFlowModuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeContactFlowModuleResponseTypeDef(TypedDict):
    ContactFlowModule: ContactFlowModuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchContactFlowModulesResponseTypeDef(TypedDict):
    ContactFlowModules: List[ContactFlowModuleTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListContactFlowsResponseTypeDef(TypedDict):
    ContactFlowSummaryList: List[ContactFlowSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeContactFlowResponseTypeDef(TypedDict):
    ContactFlow: ContactFlowTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchContactFlowsResponseTypeDef(TypedDict):
    ContactFlows: List[ContactFlowTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListContactFlowVersionsResponseTypeDef(TypedDict):
    ContactFlowVersionSummaryList: List[ContactFlowVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ContactSearchSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]
    InitialContactId: NotRequired[str]
    PreviousContactId: NotRequired[str]
    InitiationMethod: NotRequired[ContactInitiationMethodType]
    Channel: NotRequired[ChannelType]
    QueueInfo: NotRequired[ContactSearchSummaryQueueInfoTypeDef]
    AgentInfo: NotRequired[ContactSearchSummaryAgentInfoTypeDef]
    InitiationTimestamp: NotRequired[datetime]
    DisconnectTimestamp: NotRequired[datetime]
    ScheduledTimestamp: NotRequired[datetime]
    SegmentAttributes: NotRequired[Dict[str, ContactSearchSummarySegmentAttributeValueTypeDef]]


class CreateContactFlowVersionRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactFlowId: str
    Description: NotRequired[str]
    FlowContentSha256: NotRequired[str]
    LastModifiedTime: NotRequired[TimestampTypeDef]
    LastModifiedRegion: NotRequired[str]


SearchContactsTimeRangeTypeDef = TypedDict(
    "SearchContactsTimeRangeTypeDef",
    {
        "Type": SearchContactsTimeRangeTypeType,
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
    },
)


class UpdateContactScheduleRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    ScheduledTime: TimestampTypeDef


class StartOutboundVoiceContactRequestRequestTypeDef(TypedDict):
    DestinationPhoneNumber: str
    ContactFlowId: str
    InstanceId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    References: NotRequired[Mapping[str, ReferenceTypeDef]]
    RelatedContactId: NotRequired[str]
    ClientToken: NotRequired[str]
    SourcePhoneNumber: NotRequired[str]
    QueueId: NotRequired[str]
    Attributes: NotRequired[Mapping[str, str]]
    AnswerMachineDetectionConfig: NotRequired[AnswerMachineDetectionConfigTypeDef]
    CampaignId: NotRequired[str]
    TrafficType: NotRequired[TrafficTypeType]


class TaskActionDefinitionOutputTypeDef(TypedDict):
    Name: str
    ContactFlowId: str
    Description: NotRequired[str]
    References: NotRequired[Dict[str, ReferenceTypeDef]]


class TaskActionDefinitionTypeDef(TypedDict):
    Name: str
    ContactFlowId: str
    Description: NotRequired[str]
    References: NotRequired[Mapping[str, ReferenceTypeDef]]


class CreateParticipantRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    ParticipantDetails: ParticipantDetailsToAddTypeDef
    ClientToken: NotRequired[str]


class CreateParticipantResponseTypeDef(TypedDict):
    ParticipantCredentials: ParticipantTokenCredentialsTypeDef
    ParticipantId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePredefinedAttributeRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str
    Values: PredefinedAttributeValuesTypeDef


class UpdatePredefinedAttributeRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str
    Values: NotRequired[PredefinedAttributeValuesTypeDef]


class UpdateQueueOutboundCallerConfigRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QueueId: str
    OutboundCallerConfig: OutboundCallerConfigTypeDef


class CreateQueueRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str
    HoursOfOperationId: str
    Description: NotRequired[str]
    OutboundCallerConfig: NotRequired[OutboundCallerConfigTypeDef]
    OutboundEmailConfig: NotRequired[OutboundEmailConfigTypeDef]
    MaxContacts: NotRequired[int]
    QuickConnectIds: NotRequired[Sequence[str]]
    Tags: NotRequired[Mapping[str, str]]


class QueueTypeDef(TypedDict):
    Name: NotRequired[str]
    QueueArn: NotRequired[str]
    QueueId: NotRequired[str]
    Description: NotRequired[str]
    OutboundCallerConfig: NotRequired[OutboundCallerConfigTypeDef]
    OutboundEmailConfig: NotRequired[OutboundEmailConfigTypeDef]
    HoursOfOperationId: NotRequired[str]
    MaxContacts: NotRequired[int]
    Status: NotRequired[QueueStatusType]
    Tags: NotRequired[Dict[str, str]]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class UpdateQueueOutboundEmailConfigRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QueueId: str
    OutboundEmailConfig: OutboundEmailConfigTypeDef


class UpdateUserIdentityInfoRequestRequestTypeDef(TypedDict):
    IdentityInfo: UserIdentityInfoTypeDef
    UserId: str
    InstanceId: str


class CreateUserRequestRequestTypeDef(TypedDict):
    Username: str
    PhoneConfig: UserPhoneConfigTypeDef
    SecurityProfileIds: Sequence[str]
    RoutingProfileId: str
    InstanceId: str
    Password: NotRequired[str]
    IdentityInfo: NotRequired[UserIdentityInfoTypeDef]
    DirectoryUserId: NotRequired[str]
    HierarchyGroupId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class UpdateUserPhoneConfigRequestRequestTypeDef(TypedDict):
    PhoneConfig: UserPhoneConfigTypeDef
    UserId: str
    InstanceId: str


class UserTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Username: NotRequired[str]
    IdentityInfo: NotRequired[UserIdentityInfoTypeDef]
    PhoneConfig: NotRequired[UserPhoneConfigTypeDef]
    DirectoryUserId: NotRequired[str]
    SecurityProfileIds: NotRequired[List[str]]
    RoutingProfileId: NotRequired[str]
    HierarchyGroupId: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class CreateViewRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Status: ViewStatusType
    Content: ViewInputContentTypeDef
    Name: str
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class UpdateViewContentRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ViewId: str
    Status: ViewStatusType
    Content: ViewInputContentTypeDef


class GetFederationTokenResponseTypeDef(TypedDict):
    Credentials: CredentialsTypeDef
    SignInUrl: str
    UserArn: str
    UserId: str
    ResponseMetadata: ResponseMetadataTypeDef


class MediaConcurrencyTypeDef(TypedDict):
    Channel: ChannelType
    Concurrency: int
    CrossChannelBehavior: NotRequired[CrossChannelBehaviorTypeDef]


class CurrentMetricDataTypeDef(TypedDict):
    Metric: NotRequired[CurrentMetricTypeDef]
    Value: NotRequired[float]


class ListDefaultVocabulariesResponseTypeDef(TypedDict):
    DefaultVocabularyList: List[DefaultVocabularyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribePromptResponseTypeDef(TypedDict):
    Prompt: PromptTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchPromptsResponseTypeDef(TypedDict):
    Prompts: List[PromptTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeSecurityProfileResponseTypeDef(TypedDict):
    SecurityProfile: SecurityProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrafficDistributionGroupResponseTypeDef(TypedDict):
    TrafficDistributionGroup: TrafficDistributionGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVocabularyResponseTypeDef(TypedDict):
    Vocabulary: VocabularyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DimensionsTypeDef(TypedDict):
    Queue: NotRequired[QueueReferenceTypeDef]
    Channel: NotRequired[ChannelType]
    RoutingProfile: NotRequired[RoutingProfileReferenceTypeDef]
    RoutingStepExpression: NotRequired[str]


class DisassociateRoutingProfileQueuesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    RoutingProfileId: str
    QueueReferences: Sequence[RoutingProfileQueueReferenceTypeDef]


class RoutingProfileQueueConfigTypeDef(TypedDict):
    QueueReference: RoutingProfileQueueReferenceTypeDef
    Priority: int
    Delay: int


class DisassociateUserProficienciesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    UserId: str
    UserProficiencies: Sequence[UserProficiencyDisassociateTypeDef]


class StopContactRequestRequestTypeDef(TypedDict):
    ContactId: str
    InstanceId: str
    DisconnectReason: NotRequired[DisconnectReasonTypeDef]


class GetAttachedFileResponseTypeDef(TypedDict):
    FileArn: str
    FileId: str
    CreationTime: str
    FileStatus: FileStatusTypeType
    FileName: str
    FileSizeInBytes: int
    AssociatedResourceArn: str
    FileUseCaseType: FileUseCaseTypeType
    CreatedBy: CreatedByInfoTypeDef
    DownloadUrlMetadata: DownloadUrlMetadataTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class InboundAdditionalRecipientsTypeDef(TypedDict):
    ToAddresses: NotRequired[Sequence[EmailAddressInfoTypeDef]]
    CcAddresses: NotRequired[Sequence[EmailAddressInfoTypeDef]]


class OutboundAdditionalRecipientsTypeDef(TypedDict):
    CcEmailAddresses: NotRequired[Sequence[EmailAddressInfoTypeDef]]


class SearchEmailAddressesResponseTypeDef(TypedDict):
    EmailAddresses: List[EmailAddressMetadataTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class KinesisVideoStreamConfigTypeDef(TypedDict):
    Prefix: str
    RetentionPeriodHours: int
    EncryptionConfig: EncryptionConfigTypeDef


class S3ConfigTypeDef(TypedDict):
    BucketName: str
    BucketPrefix: str
    EncryptionConfig: NotRequired[EncryptionConfigTypeDef]


class EvaluationAnswerInputTypeDef(TypedDict):
    Value: NotRequired[EvaluationAnswerDataTypeDef]


class EvaluationAnswerOutputTypeDef(TypedDict):
    Value: NotRequired[EvaluationAnswerDataTypeDef]
    SystemSuggestedValue: NotRequired[EvaluationAnswerDataTypeDef]


class EvaluationFormNumericQuestionAutomationTypeDef(TypedDict):
    PropertyValue: NotRequired[NumericQuestionPropertyValueAutomationTypeDef]


EvaluationFormSectionUnionTypeDef = Union[
    EvaluationFormSectionTypeDef, EvaluationFormSectionOutputTypeDef
]


class EvaluationFormSingleSelectQuestionAutomationOptionTypeDef(TypedDict):
    RuleCategory: NotRequired[SingleSelectQuestionRuleCategoryAutomationTypeDef]


class ListEvaluationFormsResponseTypeDef(TypedDict):
    EvaluationFormSummaryList: List[EvaluationFormSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListEvaluationFormVersionsResponseTypeDef(TypedDict):
    EvaluationFormVersionSummaryList: List[EvaluationFormVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class EvaluationMetadataTypeDef(TypedDict):
    ContactId: str
    EvaluatorArn: str
    ContactAgentId: NotRequired[str]
    Score: NotRequired[EvaluationScoreTypeDef]


class EvaluationSummaryTypeDef(TypedDict):
    EvaluationId: str
    EvaluationArn: str
    EvaluationFormTitle: str
    EvaluationFormId: str
    Status: EvaluationStatusType
    EvaluatorArn: str
    CreatedTime: datetime
    LastModifiedTime: datetime
    Score: NotRequired[EvaluationScoreTypeDef]


class FieldValueOutputTypeDef(TypedDict):
    Id: str
    Value: FieldValueUnionOutputTypeDef


FieldValueUnionUnionTypeDef = Union[FieldValueUnionTypeDef, FieldValueUnionOutputTypeDef]


class GetCurrentMetricDataRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Filters: FiltersTypeDef
    CurrentMetrics: Sequence[CurrentMetricTypeDef]
    Groupings: NotRequired[Sequence[GroupingType]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortCriteria: NotRequired[Sequence[CurrentMetricSortCriteriaTypeDef]]


class ListAgentStatusRequestListAgentStatusesPaginateTypeDef(TypedDict):
    InstanceId: str
    AgentStatusTypes: NotRequired[Sequence[AgentStatusTypeType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAuthenticationProfilesRequestListAuthenticationProfilesPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBotsRequestListBotsPaginateTypeDef(TypedDict):
    InstanceId: str
    LexVersion: LexVersionType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContactEvaluationsRequestListContactEvaluationsPaginateTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef(TypedDict):
    InstanceId: str
    ContactFlowModuleState: NotRequired[ContactFlowModuleStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContactFlowVersionsRequestListContactFlowVersionsPaginateTypeDef(TypedDict):
    InstanceId: str
    ContactFlowId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContactFlowsRequestListContactFlowsPaginateTypeDef(TypedDict):
    InstanceId: str
    ContactFlowTypes: NotRequired[Sequence[ContactFlowTypeType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContactReferencesRequestListContactReferencesPaginateTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    ReferenceTypes: Sequence[ReferenceTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef(TypedDict):
    InstanceId: str
    LanguageCode: NotRequired[VocabularyLanguageCodeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEvaluationFormVersionsRequestListEvaluationFormVersionsPaginateTypeDef(TypedDict):
    InstanceId: str
    EvaluationFormId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEvaluationFormsRequestListEvaluationFormsPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFlowAssociationsRequestListFlowAssociationsPaginateTypeDef(TypedDict):
    InstanceId: str
    ResourceType: NotRequired[ListFlowAssociationResourceTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef(TypedDict):
    InstanceId: str
    ResourceType: InstanceStorageResourceTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInstancesRequestListInstancesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef(TypedDict):
    InstanceId: str
    IntegrationType: NotRequired[IntegrationTypeType]
    IntegrationArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLexBotsRequestListLexBotsPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef(TypedDict):
    InstanceId: str
    PhoneNumberTypes: NotRequired[Sequence[PhoneNumberTypeType]]
    PhoneNumberCountryCodes: NotRequired[Sequence[PhoneNumberCountryCodeType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPhoneNumbersV2RequestListPhoneNumbersV2PaginateTypeDef(TypedDict):
    TargetArn: NotRequired[str]
    InstanceId: NotRequired[str]
    PhoneNumberCountryCodes: NotRequired[Sequence[PhoneNumberCountryCodeType]]
    PhoneNumberTypes: NotRequired[Sequence[PhoneNumberTypeType]]
    PhoneNumberPrefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPredefinedAttributesRequestListPredefinedAttributesPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPromptsRequestListPromptsPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef(TypedDict):
    InstanceId: str
    QueueId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListQueuesRequestListQueuesPaginateTypeDef(TypedDict):
    InstanceId: str
    QueueTypes: NotRequired[Sequence[QueueTypeType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListQuickConnectsRequestListQuickConnectsPaginateTypeDef(TypedDict):
    InstanceId: str
    QuickConnectTypes: NotRequired[Sequence[QuickConnectTypeType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef(TypedDict):
    InstanceId: str
    RoutingProfileId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRulesRequestListRulesPaginateTypeDef(TypedDict):
    InstanceId: str
    PublishStatus: NotRequired[RulePublishStatusType]
    EventSourceName: NotRequired[EventSourceNameType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSecurityKeysRequestListSecurityKeysPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSecurityProfileApplicationsRequestListSecurityProfileApplicationsPaginateTypeDef(
    TypedDict
):
    SecurityProfileId: str
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef(TypedDict):
    SecurityProfileId: str
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef(TypedDict):
    InstanceId: str
    Status: NotRequired[TaskTemplateStatusType]
    Name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTrafficDistributionGroupUsersRequestListTrafficDistributionGroupUsersPaginateTypeDef(
    TypedDict
):
    TrafficDistributionGroupId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTrafficDistributionGroupsRequestListTrafficDistributionGroupsPaginateTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUseCasesRequestListUseCasesPaginateTypeDef(TypedDict):
    InstanceId: str
    IntegrationAssociationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUserProficienciesRequestListUserProficienciesPaginateTypeDef(TypedDict):
    InstanceId: str
    UserId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUsersRequestListUsersPaginateTypeDef(TypedDict):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListViewVersionsRequestListViewVersionsPaginateTypeDef(TypedDict):
    InstanceId: str
    ViewId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListViewsRequestListViewsPaginateTypeDef = TypedDict(
    "ListViewsRequestListViewsPaginateTypeDef",
    {
        "InstanceId": str,
        "Type": NotRequired[ViewTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class SearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef(TypedDict):
    PhoneNumberCountryCode: PhoneNumberCountryCodeType
    PhoneNumberType: PhoneNumberTypeType
    TargetArn: NotRequired[str]
    InstanceId: NotRequired[str]
    PhoneNumberPrefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchVocabulariesRequestSearchVocabulariesPaginateTypeDef(TypedDict):
    InstanceId: str
    State: NotRequired[VocabularyStateType]
    NameStartsWith: NotRequired[str]
    LanguageCode: NotRequired[VocabularyLanguageCodeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class HierarchyPathReferenceTypeDef(TypedDict):
    LevelOne: NotRequired[HierarchyGroupSummaryReferenceTypeDef]
    LevelTwo: NotRequired[HierarchyGroupSummaryReferenceTypeDef]
    LevelThree: NotRequired[HierarchyGroupSummaryReferenceTypeDef]
    LevelFour: NotRequired[HierarchyGroupSummaryReferenceTypeDef]
    LevelFive: NotRequired[HierarchyGroupSummaryReferenceTypeDef]


class HierarchyPathTypeDef(TypedDict):
    LevelOne: NotRequired[HierarchyGroupSummaryTypeDef]
    LevelTwo: NotRequired[HierarchyGroupSummaryTypeDef]
    LevelThree: NotRequired[HierarchyGroupSummaryTypeDef]
    LevelFour: NotRequired[HierarchyGroupSummaryTypeDef]
    LevelFive: NotRequired[HierarchyGroupSummaryTypeDef]


class ListUserHierarchyGroupsResponseTypeDef(TypedDict):
    UserHierarchyGroupSummaryList: List[HierarchyGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class HierarchyStructureTypeDef(TypedDict):
    LevelOne: NotRequired[HierarchyLevelTypeDef]
    LevelTwo: NotRequired[HierarchyLevelTypeDef]
    LevelThree: NotRequired[HierarchyLevelTypeDef]
    LevelFour: NotRequired[HierarchyLevelTypeDef]
    LevelFive: NotRequired[HierarchyLevelTypeDef]


class HierarchyStructureUpdateTypeDef(TypedDict):
    LevelOne: NotRequired[HierarchyLevelUpdateTypeDef]
    LevelTwo: NotRequired[HierarchyLevelUpdateTypeDef]
    LevelThree: NotRequired[HierarchyLevelUpdateTypeDef]
    LevelFour: NotRequired[HierarchyLevelUpdateTypeDef]
    LevelFive: NotRequired[HierarchyLevelUpdateTypeDef]


class HistoricalMetricTypeDef(TypedDict):
    Name: NotRequired[HistoricalMetricNameType]
    Threshold: NotRequired[ThresholdTypeDef]
    Statistic: NotRequired[StatisticType]
    Unit: NotRequired[UnitType]


class HoursOfOperationConfigTypeDef(TypedDict):
    Day: HoursOfOperationDaysType
    StartTime: HoursOfOperationTimeSliceTypeDef
    EndTime: HoursOfOperationTimeSliceTypeDef


class ListHoursOfOperationsResponseTypeDef(TypedDict):
    HoursOfOperationSummaryList: List[HoursOfOperationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class InboundEmailContentTypeDef(TypedDict):
    MessageSourceType: Literal["RAW"]
    RawMessage: NotRequired[InboundRawMessageTypeDef]


class InstanceTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    IdentityManagementType: NotRequired[DirectoryTypeType]
    InstanceAlias: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    ServiceRole: NotRequired[str]
    InstanceStatus: NotRequired[InstanceStatusType]
    StatusReason: NotRequired[InstanceStatusReasonTypeDef]
    InboundCallsEnabled: NotRequired[bool]
    OutboundCallsEnabled: NotRequired[bool]
    InstanceAccessUrl: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]


class ListInstancesResponseTypeDef(TypedDict):
    InstanceSummaryList: List[InstanceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListIntegrationAssociationsResponseTypeDef(TypedDict):
    IntegrationAssociationSummaryList: List[IntegrationAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class InvisibleFieldInfoTypeDef(TypedDict):
    Id: NotRequired[TaskTemplateFieldIdentifierTypeDef]


class ReadOnlyFieldInfoTypeDef(TypedDict):
    Id: NotRequired[TaskTemplateFieldIdentifierTypeDef]


class RequiredFieldInfoTypeDef(TypedDict):
    Id: NotRequired[TaskTemplateFieldIdentifierTypeDef]


class TaskTemplateDefaultFieldValueTypeDef(TypedDict):
    Id: NotRequired[TaskTemplateFieldIdentifierTypeDef]
    DefaultValue: NotRequired[str]


TaskTemplateFieldOutputTypeDef = TypedDict(
    "TaskTemplateFieldOutputTypeDef",
    {
        "Id": TaskTemplateFieldIdentifierTypeDef,
        "Description": NotRequired[str],
        "Type": NotRequired[TaskTemplateFieldTypeType],
        "SingleSelectOptions": NotRequired[List[str]],
    },
)
TaskTemplateFieldTypeDef = TypedDict(
    "TaskTemplateFieldTypeDef",
    {
        "Id": TaskTemplateFieldIdentifierTypeDef,
        "Description": NotRequired[str],
        "Type": NotRequired[TaskTemplateFieldTypeType],
        "SingleSelectOptions": NotRequired[Sequence[str]],
    },
)


class ListPhoneNumbersResponseTypeDef(TypedDict):
    PhoneNumberSummaryList: List[PhoneNumberSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPhoneNumbersV2ResponseTypeDef(TypedDict):
    ListPhoneNumbersSummaryList: List[ListPhoneNumbersSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPredefinedAttributesResponseTypeDef(TypedDict):
    PredefinedAttributeSummaryList: List[PredefinedAttributeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPromptsResponseTypeDef(TypedDict):
    PromptSummaryList: List[PromptSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListQueueQuickConnectsResponseTypeDef(TypedDict):
    QuickConnectSummaryList: List[QuickConnectSummaryTypeDef]
    LastModifiedTime: datetime
    LastModifiedRegion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListQuickConnectsResponseTypeDef(TypedDict):
    QuickConnectSummaryList: List[QuickConnectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListQueuesResponseTypeDef(TypedDict):
    QueueSummaryList: List[QueueSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRoutingProfileQueuesResponseTypeDef(TypedDict):
    RoutingProfileQueueConfigSummaryList: List[RoutingProfileQueueConfigSummaryTypeDef]
    LastModifiedTime: datetime
    LastModifiedRegion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRoutingProfilesResponseTypeDef(TypedDict):
    RoutingProfileSummaryList: List[RoutingProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListSecurityKeysResponseTypeDef(TypedDict):
    SecurityKeys: List[SecurityKeyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListSecurityProfilesResponseTypeDef(TypedDict):
    SecurityProfileSummaryList: List[SecurityProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTaskTemplatesResponseTypeDef(TypedDict):
    TaskTemplates: List[TaskTemplateMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTrafficDistributionGroupUsersResponseTypeDef(TypedDict):
    TrafficDistributionGroupUserSummaryList: List[TrafficDistributionGroupUserSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTrafficDistributionGroupsResponseTypeDef(TypedDict):
    TrafficDistributionGroupSummaryList: List[TrafficDistributionGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListUseCasesResponseTypeDef(TypedDict):
    UseCaseSummaryList: List[UseCaseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListUsersResponseTypeDef(TypedDict):
    UserSummaryList: List[UserSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListViewVersionsResponseTypeDef(TypedDict):
    ViewVersionSummaryList: List[ViewVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListViewsResponseTypeDef(TypedDict):
    ViewsSummaryList: List[ViewSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


MetricFilterV2UnionTypeDef = Union[MetricFilterV2TypeDef, MetricFilterV2OutputTypeDef]


class MetricV2OutputTypeDef(TypedDict):
    Name: NotRequired[str]
    Threshold: NotRequired[List[ThresholdV2TypeDef]]
    MetricFilters: NotRequired[List[MetricFilterV2OutputTypeDef]]


class NewSessionDetailsTypeDef(TypedDict):
    SupportedMessagingContentTypes: NotRequired[Sequence[str]]
    ParticipantDetails: NotRequired[ParticipantDetailsTypeDef]
    Attributes: NotRequired[Mapping[str, str]]
    StreamingConfiguration: NotRequired[ChatStreamingConfigurationTypeDef]


class SendNotificationActionDefinitionOutputTypeDef(TypedDict):
    DeliveryMethod: Literal["EMAIL"]
    Content: str
    ContentType: Literal["PLAIN_TEXT"]
    Recipient: NotificationRecipientTypeOutputTypeDef
    Subject: NotRequired[str]


NotificationRecipientTypeUnionTypeDef = Union[
    NotificationRecipientTypeTypeDef, NotificationRecipientTypeOutputTypeDef
]


class ParticipantTimerConfigurationTypeDef(TypedDict):
    ParticipantRole: TimerEligibleParticipantRolesType
    TimerType: ParticipantTimerTypeType
    TimerValue: ParticipantTimerValueTypeDef


class PredefinedAttributeTypeDef(TypedDict):
    Name: NotRequired[str]
    Values: NotRequired[PredefinedAttributeValuesOutputTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class QuickConnectConfigTypeDef(TypedDict):
    QuickConnectType: QuickConnectTypeType
    UserConfig: NotRequired[UserQuickConnectConfigTypeDef]
    QueueConfig: NotRequired[QueueQuickConnectConfigTypeDef]
    PhoneConfig: NotRequired[PhoneNumberQuickConnectConfigTypeDef]


class RealTimeContactAnalysisTranscriptItemRedactionTypeDef(TypedDict):
    CharacterOffsets: NotRequired[List[RealTimeContactAnalysisCharacterIntervalTypeDef]]


class RealTimeContactAnalysisTranscriptItemWithCharacterOffsetsTypeDef(TypedDict):
    Id: str
    CharacterOffsets: NotRequired[RealTimeContactAnalysisCharacterIntervalTypeDef]


class RealTimeContactAnalysisTranscriptItemWithContentTypeDef(TypedDict):
    Id: str
    Content: NotRequired[str]
    CharacterOffsets: NotRequired[RealTimeContactAnalysisCharacterIntervalTypeDef]


class RealTimeContactAnalysisSegmentAttachmentsTypeDef(TypedDict):
    Id: str
    ParticipantId: str
    ParticipantRole: ParticipantRoleType
    Attachments: List[RealTimeContactAnalysisAttachmentTypeDef]
    Time: RealTimeContactAnalysisTimeDataTypeDef
    DisplayName: NotRequired[str]


class RealTimeContactAnalysisSegmentEventTypeDef(TypedDict):
    Id: str
    EventType: str
    Time: RealTimeContactAnalysisTimeDataTypeDef
    ParticipantId: NotRequired[str]
    ParticipantRole: NotRequired[ParticipantRoleType]
    DisplayName: NotRequired[str]


class ReferenceSummaryTypeDef(TypedDict):
    Url: NotRequired[UrlReferenceTypeDef]
    Attachment: NotRequired[AttachmentReferenceTypeDef]
    EmailMessage: NotRequired[EmailMessageReferenceTypeDef]
    String: NotRequired[StringReferenceTypeDef]
    Number: NotRequired[NumberReferenceTypeDef]
    Date: NotRequired[DateReferenceTypeDef]
    Email: NotRequired[EmailReferenceTypeDef]


class ReplicationConfigurationTypeDef(TypedDict):
    ReplicationStatusSummaryList: NotRequired[List[ReplicationStatusSummaryTypeDef]]
    SourceRegion: NotRequired[str]
    GlobalSignInEndpoint: NotRequired[str]


class ResourceTagsSearchCriteriaTypeDef(TypedDict):
    TagSearchCondition: NotRequired[TagSearchConditionTypeDef]


class SearchResourceTagsResponseTypeDef(TypedDict):
    Tags: List[TagSetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchSecurityProfilesResponseTypeDef(TypedDict):
    SecurityProfiles: List[SecurityProfileSearchSummaryTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchVocabulariesResponseTypeDef(TypedDict):
    VocabularySummaryList: List[VocabularySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchableContactAttributesTypeDef(TypedDict):
    Criteria: Sequence[SearchableContactAttributesCriteriaTypeDef]
    MatchType: NotRequired[SearchContactsMatchTypeType]


class SearchableSegmentAttributesTypeDef(TypedDict):
    Criteria: Sequence[SearchableSegmentAttributesCriteriaTypeDef]
    MatchType: NotRequired[SearchContactsMatchTypeType]


SegmentAttributeValueUnionTypeDef = Union[
    SegmentAttributeValueTypeDef, SegmentAttributeValueOutputTypeDef
]


class StartChatContactRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactFlowId: str
    ParticipantDetails: ParticipantDetailsTypeDef
    Attributes: NotRequired[Mapping[str, str]]
    InitialMessage: NotRequired[ChatMessageTypeDef]
    ClientToken: NotRequired[str]
    ChatDurationInMinutes: NotRequired[int]
    SupportedMessagingContentTypes: NotRequired[Sequence[str]]
    PersistentChat: NotRequired[PersistentChatTypeDef]
    RelatedContactId: NotRequired[str]
    SegmentAttributes: NotRequired[Mapping[str, SegmentAttributeValueTypeDef]]


class StartOutboundChatContactRequestRequestTypeDef(TypedDict):
    SourceEndpoint: EndpointTypeDef
    DestinationEndpoint: EndpointTypeDef
    InstanceId: str
    SegmentAttributes: Mapping[str, SegmentAttributeValueTypeDef]
    ContactFlowId: str
    Attributes: NotRequired[Mapping[str, str]]
    ChatDurationInMinutes: NotRequired[int]
    ParticipantDetails: NotRequired[ParticipantDetailsTypeDef]
    InitialSystemMessage: NotRequired[ChatMessageTypeDef]
    RelatedContactId: NotRequired[str]
    SupportedMessagingContentTypes: NotRequired[Sequence[str]]
    ClientToken: NotRequired[str]


class StartTaskContactRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str
    PreviousContactId: NotRequired[str]
    ContactFlowId: NotRequired[str]
    Attributes: NotRequired[Mapping[str, str]]
    References: NotRequired[Mapping[str, ReferenceTypeDef]]
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
    ScheduledTime: NotRequired[TimestampTypeDef]
    TaskTemplateId: NotRequired[str]
    QuickConnectId: NotRequired[str]
    RelatedContactId: NotRequired[str]
    SegmentAttributes: NotRequired[Mapping[str, SegmentAttributeValueTypeDef]]


class UpdateContactRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    References: NotRequired[Mapping[str, ReferenceTypeDef]]
    SegmentAttributes: NotRequired[Mapping[str, SegmentAttributeValueTypeDef]]
    QueueInfo: NotRequired[QueueInfoInputTypeDef]
    UserInfo: NotRequired[UserInfoTypeDef]
    CustomerEndpoint: NotRequired[EndpointTypeDef]
    SystemEndpoint: NotRequired[EndpointTypeDef]


class SignInConfigOutputTypeDef(TypedDict):
    Distributions: List[SignInDistributionTypeDef]


class SignInConfigTypeDef(TypedDict):
    Distributions: Sequence[SignInDistributionTypeDef]


class StartAttachedFileUploadResponseTypeDef(TypedDict):
    FileArn: str
    FileId: str
    CreationTime: str
    FileStatus: FileStatusTypeType
    CreatedBy: CreatedByInfoTypeDef
    UploadUrlMetadata: UploadUrlMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartContactRecordingRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    InitialContactId: str
    VoiceRecordingConfiguration: VoiceRecordingConfigurationTypeDef


class TemplatedMessageConfigTypeDef(TypedDict):
    KnowledgeBaseId: str
    MessageTemplateId: str
    TemplateAttributes: TemplateAttributesTypeDef


class TranscriptTypeDef(TypedDict):
    Criteria: Sequence[TranscriptCriteriaTypeDef]
    MatchType: NotRequired[SearchContactsMatchTypeType]


class UserSearchSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    DirectoryUserId: NotRequired[str]
    HierarchyGroupId: NotRequired[str]
    Id: NotRequired[str]
    IdentityInfo: NotRequired[UserIdentityInfoLiteTypeDef]
    PhoneConfig: NotRequired[UserPhoneConfigTypeDef]
    RoutingProfileId: NotRequired[str]
    SecurityProfileIds: NotRequired[List[str]]
    Tags: NotRequired[Dict[str, str]]
    Username: NotRequired[str]


ViewTypeDef = TypedDict(
    "ViewTypeDef",
    {
        "Id": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Status": NotRequired[ViewStatusType],
        "Type": NotRequired[ViewTypeType],
        "Description": NotRequired[str],
        "Version": NotRequired[int],
        "VersionDescription": NotRequired[str],
        "Content": NotRequired[ViewContentTypeDef],
        "Tags": NotRequired[Dict[str, str]],
        "CreatedTime": NotRequired[datetime],
        "LastModifiedTime": NotRequired[datetime],
        "ViewContentSha256": NotRequired[str],
    },
)


class ListRulesResponseTypeDef(TypedDict):
    RuleSummaryList: List[RuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AgentInfoTypeDef(TypedDict):
    Id: NotRequired[str]
    ConnectedToAgentTimestamp: NotRequired[datetime]
    AgentPauseDurationInSeconds: NotRequired[int]
    HierarchyGroups: NotRequired[HierarchyGroupsTypeDef]
    DeviceInfo: NotRequired[DeviceInfoTypeDef]
    Capabilities: NotRequired[ParticipantCapabilitiesTypeDef]


class StartWebRTCContactRequestRequestTypeDef(TypedDict):
    ContactFlowId: str
    InstanceId: str
    ParticipantDetails: ParticipantDetailsTypeDef
    Attributes: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]
    AllowedCapabilities: NotRequired[AllowedCapabilitiesTypeDef]
    RelatedContactId: NotRequired[str]
    References: NotRequired[Mapping[str, ReferenceTypeDef]]
    Description: NotRequired[str]


class QualityMetricsTypeDef(TypedDict):
    Agent: NotRequired[AgentQualityMetricsTypeDef]
    Customer: NotRequired[CustomerQualityMetricsTypeDef]


class SearchPredefinedAttributesRequestSearchPredefinedAttributesPaginateTypeDef(TypedDict):
    InstanceId: str
    SearchCriteria: NotRequired[PredefinedAttributeSearchCriteriaPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchPredefinedAttributesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SearchCriteria: NotRequired[PredefinedAttributeSearchCriteriaTypeDef]


class AttributeConditionOutputTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]
    ProficiencyLevel: NotRequired[float]
    MatchCriteria: NotRequired[MatchCriteriaOutputTypeDef]
    ComparisonOperator: NotRequired[str]


class MatchCriteriaTypeDef(TypedDict):
    AgentsCriteria: NotRequired[AgentsCriteriaUnionTypeDef]


class CreateSecurityProfileRequestRequestTypeDef(TypedDict):
    SecurityProfileName: str
    InstanceId: str
    Description: NotRequired[str]
    Permissions: NotRequired[Sequence[str]]
    Tags: NotRequired[Mapping[str, str]]
    AllowedAccessControlTags: NotRequired[Mapping[str, str]]
    TagRestrictedResources: NotRequired[Sequence[str]]
    Applications: NotRequired[Sequence[ApplicationUnionTypeDef]]
    HierarchyRestrictedResources: NotRequired[Sequence[str]]
    AllowedAccessControlHierarchyGroupId: NotRequired[str]


class ListBotsResponseTypeDef(TypedDict):
    LexBots: List[LexBotConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class BatchGetAttachedFileMetadataResponseTypeDef(TypedDict):
    Files: List[AttachedFileTypeDef]
    Errors: List[AttachedFileErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ControlPlaneUserAttributeFilterTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[AttributeAndConditionTypeDef]]
    AndCondition: NotRequired[AttributeAndConditionTypeDef]
    TagCondition: NotRequired[TagConditionTypeDef]
    HierarchyGroupCondition: NotRequired[HierarchyGroupConditionTypeDef]


class ControlPlaneAttributeFilterTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[CommonAttributeAndConditionTypeDef]]
    AndCondition: NotRequired[CommonAttributeAndConditionTypeDef]
    TagCondition: NotRequired[TagConditionTypeDef]


class ContactFlowModuleSearchFilterTypeDef(TypedDict):
    TagFilter: NotRequired[ControlPlaneTagFilterTypeDef]


class ContactFlowSearchFilterTypeDef(TypedDict):
    TagFilter: NotRequired[ControlPlaneTagFilterTypeDef]


class EmailAddressSearchFilterTypeDef(TypedDict):
    TagFilter: NotRequired[ControlPlaneTagFilterTypeDef]


class HoursOfOperationSearchFilterTypeDef(TypedDict):
    TagFilter: NotRequired[ControlPlaneTagFilterTypeDef]


class PromptSearchFilterTypeDef(TypedDict):
    TagFilter: NotRequired[ControlPlaneTagFilterTypeDef]


class QueueSearchFilterTypeDef(TypedDict):
    TagFilter: NotRequired[ControlPlaneTagFilterTypeDef]


class QuickConnectSearchFilterTypeDef(TypedDict):
    TagFilter: NotRequired[ControlPlaneTagFilterTypeDef]


class RoutingProfileSearchFilterTypeDef(TypedDict):
    TagFilter: NotRequired[ControlPlaneTagFilterTypeDef]


class SecurityProfilesSearchFilterTypeDef(TypedDict):
    TagFilter: NotRequired[ControlPlaneTagFilterTypeDef]


class MeetingTypeDef(TypedDict):
    MediaRegion: NotRequired[str]
    MediaPlacement: NotRequired[MediaPlacementTypeDef]
    MeetingFeatures: NotRequired[MeetingFeaturesConfigurationTypeDef]
    MeetingId: NotRequired[str]


class DescribePhoneNumberResponseTypeDef(TypedDict):
    ClaimedPhoneNumberSummary: ClaimedPhoneNumberSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListConditionTypeDef(TypedDict):
    TargetListType: NotRequired[Literal["PROFICIENCIES"]]
    Conditions: NotRequired[Sequence[ConditionTypeDef]]


class BatchPutContactRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactDataRequestList: Sequence[ContactDataRequestTypeDef]
    ClientToken: NotRequired[str]


class GetCurrentUserDataRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Filters: UserDataFiltersTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SearchContactsResponseTypeDef(TypedDict):
    Contacts: List[ContactSearchSummaryTypeDef]
    TotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


TaskActionDefinitionUnionTypeDef = Union[
    TaskActionDefinitionTypeDef, TaskActionDefinitionOutputTypeDef
]


class DescribeQueueResponseTypeDef(TypedDict):
    Queue: QueueTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchQueuesResponseTypeDef(TypedDict):
    Queues: List[QueueTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RoutingProfileTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    Name: NotRequired[str]
    RoutingProfileArn: NotRequired[str]
    RoutingProfileId: NotRequired[str]
    Description: NotRequired[str]
    MediaConcurrencies: NotRequired[List[MediaConcurrencyTypeDef]]
    DefaultOutboundQueueId: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]
    NumberOfAssociatedQueues: NotRequired[int]
    NumberOfAssociatedUsers: NotRequired[int]
    AgentAvailabilityTimer: NotRequired[AgentAvailabilityTimerType]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]
    IsDefault: NotRequired[bool]
    AssociatedQueueIds: NotRequired[List[str]]


class UpdateRoutingProfileConcurrencyRequestRequestTypeDef(TypedDict):
    InstanceId: str
    RoutingProfileId: str
    MediaConcurrencies: Sequence[MediaConcurrencyTypeDef]


class CurrentMetricResultTypeDef(TypedDict):
    Dimensions: NotRequired[DimensionsTypeDef]
    Collections: NotRequired[List[CurrentMetricDataTypeDef]]


class AssociateRoutingProfileQueuesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    RoutingProfileId: str
    QueueConfigs: Sequence[RoutingProfileQueueConfigTypeDef]


class CreateRoutingProfileRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str
    Description: str
    DefaultOutboundQueueId: str
    MediaConcurrencies: Sequence[MediaConcurrencyTypeDef]
    QueueConfigs: NotRequired[Sequence[RoutingProfileQueueConfigTypeDef]]
    Tags: NotRequired[Mapping[str, str]]
    AgentAvailabilityTimer: NotRequired[AgentAvailabilityTimerType]


class UpdateRoutingProfileQueuesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    RoutingProfileId: str
    QueueConfigs: Sequence[RoutingProfileQueueConfigTypeDef]


class InstanceStorageConfigTypeDef(TypedDict):
    StorageType: StorageTypeType
    AssociationId: NotRequired[str]
    S3Config: NotRequired[S3ConfigTypeDef]
    KinesisVideoStreamConfig: NotRequired[KinesisVideoStreamConfigTypeDef]
    KinesisStreamConfig: NotRequired[KinesisStreamConfigTypeDef]
    KinesisFirehoseConfig: NotRequired[KinesisFirehoseConfigTypeDef]


class SubmitContactEvaluationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EvaluationId: str
    Answers: NotRequired[Mapping[str, EvaluationAnswerInputTypeDef]]
    Notes: NotRequired[Mapping[str, EvaluationNoteTypeDef]]


class UpdateContactEvaluationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EvaluationId: str
    Answers: NotRequired[Mapping[str, EvaluationAnswerInputTypeDef]]
    Notes: NotRequired[Mapping[str, EvaluationNoteTypeDef]]


class EvaluationFormNumericQuestionPropertiesOutputTypeDef(TypedDict):
    MinValue: int
    MaxValue: int
    Options: NotRequired[List[EvaluationFormNumericQuestionOptionTypeDef]]
    Automation: NotRequired[EvaluationFormNumericQuestionAutomationTypeDef]


class EvaluationFormNumericQuestionPropertiesTypeDef(TypedDict):
    MinValue: int
    MaxValue: int
    Options: NotRequired[Sequence[EvaluationFormNumericQuestionOptionTypeDef]]
    Automation: NotRequired[EvaluationFormNumericQuestionAutomationTypeDef]


class EvaluationFormSingleSelectQuestionAutomationOutputTypeDef(TypedDict):
    Options: List[EvaluationFormSingleSelectQuestionAutomationOptionTypeDef]
    DefaultOptionRefId: NotRequired[str]


class EvaluationFormSingleSelectQuestionAutomationTypeDef(TypedDict):
    Options: Sequence[EvaluationFormSingleSelectQuestionAutomationOptionTypeDef]
    DefaultOptionRefId: NotRequired[str]


class EvaluationTypeDef(TypedDict):
    EvaluationId: str
    EvaluationArn: str
    Metadata: EvaluationMetadataTypeDef
    Answers: Dict[str, EvaluationAnswerOutputTypeDef]
    Notes: Dict[str, EvaluationNoteTypeDef]
    Status: EvaluationStatusType
    CreatedTime: datetime
    LastModifiedTime: datetime
    Scores: NotRequired[Dict[str, EvaluationScoreTypeDef]]
    Tags: NotRequired[Dict[str, str]]


class ListContactEvaluationsResponseTypeDef(TypedDict):
    EvaluationSummaryList: List[EvaluationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateCaseActionDefinitionOutputTypeDef(TypedDict):
    Fields: List[FieldValueOutputTypeDef]
    TemplateId: str


class UpdateCaseActionDefinitionOutputTypeDef(TypedDict):
    Fields: List[FieldValueOutputTypeDef]


class FieldValueTypeDef(TypedDict):
    Id: str
    Value: FieldValueUnionUnionTypeDef


class UserDataTypeDef(TypedDict):
    User: NotRequired[UserReferenceTypeDef]
    RoutingProfile: NotRequired[RoutingProfileReferenceTypeDef]
    HierarchyPath: NotRequired[HierarchyPathReferenceTypeDef]
    Status: NotRequired[AgentStatusReferenceTypeDef]
    AvailableSlotsByChannel: NotRequired[Dict[ChannelType, int]]
    MaxSlotsByChannel: NotRequired[Dict[ChannelType, int]]
    ActiveSlotsByChannel: NotRequired[Dict[ChannelType, int]]
    Contacts: NotRequired[List[AgentContactReferenceTypeDef]]
    NextStatus: NotRequired[str]


class HierarchyGroupTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    LevelId: NotRequired[str]
    HierarchyPath: NotRequired[HierarchyPathTypeDef]
    Tags: NotRequired[Dict[str, str]]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class DescribeUserHierarchyStructureResponseTypeDef(TypedDict):
    HierarchyStructure: HierarchyStructureTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserHierarchyStructureRequestRequestTypeDef(TypedDict):
    HierarchyStructure: HierarchyStructureUpdateTypeDef
    InstanceId: str


class GetMetricDataRequestGetMetricDataPaginateTypeDef(TypedDict):
    InstanceId: str
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    Filters: FiltersTypeDef
    HistoricalMetrics: Sequence[HistoricalMetricTypeDef]
    Groupings: NotRequired[Sequence[GroupingType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetMetricDataRequestRequestTypeDef(TypedDict):
    InstanceId: str
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    Filters: FiltersTypeDef
    HistoricalMetrics: Sequence[HistoricalMetricTypeDef]
    Groupings: NotRequired[Sequence[GroupingType]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class HistoricalMetricDataTypeDef(TypedDict):
    Metric: NotRequired[HistoricalMetricTypeDef]
    Value: NotRequired[float]


class CreateHoursOfOperationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str
    TimeZone: str
    Config: Sequence[HoursOfOperationConfigTypeDef]
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class HoursOfOperationTypeDef(TypedDict):
    HoursOfOperationId: NotRequired[str]
    HoursOfOperationArn: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    TimeZone: NotRequired[str]
    Config: NotRequired[List[HoursOfOperationConfigTypeDef]]
    Tags: NotRequired[Dict[str, str]]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class UpdateHoursOfOperationRequestRequestTypeDef(TypedDict):
    InstanceId: str
    HoursOfOperationId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    TimeZone: NotRequired[str]
    Config: NotRequired[Sequence[HoursOfOperationConfigTypeDef]]


class StartEmailContactRequestRequestTypeDef(TypedDict):
    InstanceId: str
    FromEmailAddress: EmailAddressInfoTypeDef
    DestinationEmailAddress: str
    EmailMessage: InboundEmailContentTypeDef
    Description: NotRequired[str]
    References: NotRequired[Mapping[str, ReferenceTypeDef]]
    Name: NotRequired[str]
    AdditionalRecipients: NotRequired[InboundAdditionalRecipientsTypeDef]
    Attachments: NotRequired[Sequence[EmailAttachmentTypeDef]]
    ContactFlowId: NotRequired[str]
    RelatedContactId: NotRequired[str]
    Attributes: NotRequired[Mapping[str, str]]
    SegmentAttributes: NotRequired[Mapping[str, SegmentAttributeValueTypeDef]]
    ClientToken: NotRequired[str]


class TaskTemplateConstraintsOutputTypeDef(TypedDict):
    RequiredFields: NotRequired[List[RequiredFieldInfoTypeDef]]
    ReadOnlyFields: NotRequired[List[ReadOnlyFieldInfoTypeDef]]
    InvisibleFields: NotRequired[List[InvisibleFieldInfoTypeDef]]


class TaskTemplateConstraintsTypeDef(TypedDict):
    RequiredFields: NotRequired[Sequence[RequiredFieldInfoTypeDef]]
    ReadOnlyFields: NotRequired[Sequence[ReadOnlyFieldInfoTypeDef]]
    InvisibleFields: NotRequired[Sequence[InvisibleFieldInfoTypeDef]]


class TaskTemplateDefaultsOutputTypeDef(TypedDict):
    DefaultFieldValues: NotRequired[List[TaskTemplateDefaultFieldValueTypeDef]]


class TaskTemplateDefaultsTypeDef(TypedDict):
    DefaultFieldValues: NotRequired[Sequence[TaskTemplateDefaultFieldValueTypeDef]]


TaskTemplateFieldUnionTypeDef = Union[TaskTemplateFieldTypeDef, TaskTemplateFieldOutputTypeDef]


class MetricV2TypeDef(TypedDict):
    Name: NotRequired[str]
    Threshold: NotRequired[Sequence[ThresholdV2TypeDef]]
    MetricFilters: NotRequired[Sequence[MetricFilterV2UnionTypeDef]]


class MetricDataV2TypeDef(TypedDict):
    Metric: NotRequired[MetricV2OutputTypeDef]
    Value: NotRequired[float]


class SendChatIntegrationEventRequestRequestTypeDef(TypedDict):
    SourceId: str
    DestinationId: str
    Event: ChatEventTypeDef
    Subtype: NotRequired[str]
    NewSessionDetails: NotRequired[NewSessionDetailsTypeDef]


class SendNotificationActionDefinitionTypeDef(TypedDict):
    DeliveryMethod: Literal["EMAIL"]
    Content: str
    ContentType: Literal["PLAIN_TEXT"]
    Recipient: NotificationRecipientTypeUnionTypeDef
    Subject: NotRequired[str]


class ChatParticipantRoleConfigTypeDef(TypedDict):
    ParticipantTimerConfigList: Sequence[ParticipantTimerConfigurationTypeDef]


class DescribePredefinedAttributeResponseTypeDef(TypedDict):
    PredefinedAttribute: PredefinedAttributeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchPredefinedAttributesResponseTypeDef(TypedDict):
    PredefinedAttributes: List[PredefinedAttributeTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateQuickConnectRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str
    QuickConnectConfig: QuickConnectConfigTypeDef
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class QuickConnectTypeDef(TypedDict):
    QuickConnectARN: NotRequired[str]
    QuickConnectId: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    QuickConnectConfig: NotRequired[QuickConnectConfigTypeDef]
    Tags: NotRequired[Dict[str, str]]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedRegion: NotRequired[str]


class UpdateQuickConnectConfigRequestRequestTypeDef(TypedDict):
    InstanceId: str
    QuickConnectId: str
    QuickConnectConfig: QuickConnectConfigTypeDef


class RealTimeContactAnalysisSegmentTranscriptTypeDef(TypedDict):
    Id: str
    ParticipantId: str
    ParticipantRole: ParticipantRoleType
    Content: str
    Time: RealTimeContactAnalysisTimeDataTypeDef
    DisplayName: NotRequired[str]
    ContentType: NotRequired[str]
    Redaction: NotRequired[RealTimeContactAnalysisTranscriptItemRedactionTypeDef]
    Sentiment: NotRequired[RealTimeContactAnalysisSentimentLabelType]


class RealTimeContactAnalysisPointOfInterestTypeDef(TypedDict):
    TranscriptItems: NotRequired[
        List[RealTimeContactAnalysisTranscriptItemWithCharacterOffsetsTypeDef]
    ]


class RealTimeContactAnalysisIssueDetectedTypeDef(TypedDict):
    TranscriptItems: List[RealTimeContactAnalysisTranscriptItemWithContentTypeDef]


class ListContactReferencesResponseTypeDef(TypedDict):
    ReferenceSummaryList: List[ReferenceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeInstanceResponseTypeDef(TypedDict):
    Instance: InstanceTypeDef
    ReplicationConfiguration: ReplicationConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchResourceTagsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ResourceTypes: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SearchCriteria: NotRequired[ResourceTagsSearchCriteriaTypeDef]


class SearchResourceTagsRequestSearchResourceTagsPaginateTypeDef(TypedDict):
    InstanceId: str
    ResourceTypes: NotRequired[Sequence[str]]
    SearchCriteria: NotRequired[ResourceTagsSearchCriteriaTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class CreateContactRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Channel: ChannelType
    InitiationMethod: ContactInitiationMethodType
    ClientToken: NotRequired[str]
    RelatedContactId: NotRequired[str]
    Attributes: NotRequired[Mapping[str, str]]
    References: NotRequired[Mapping[str, ReferenceTypeDef]]
    ExpiryDurationInMinutes: NotRequired[int]
    UserInfo: NotRequired[UserInfoTypeDef]
    InitiateAs: NotRequired[Literal["CONNECTED_TO_USER"]]
    Name: NotRequired[str]
    Description: NotRequired[str]
    SegmentAttributes: NotRequired[Mapping[str, SegmentAttributeValueUnionTypeDef]]


class GetTrafficDistributionResponseTypeDef(TypedDict):
    TelephonyConfig: TelephonyConfigOutputTypeDef
    Id: str
    Arn: str
    SignInConfig: SignInConfigOutputTypeDef
    AgentConfig: AgentConfigOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrafficDistributionRequestRequestTypeDef(TypedDict):
    Id: str
    TelephonyConfig: NotRequired[TelephonyConfigTypeDef]
    SignInConfig: NotRequired[SignInConfigTypeDef]
    AgentConfig: NotRequired[AgentConfigTypeDef]


class OutboundEmailContentTypeDef(TypedDict):
    MessageSourceType: OutboundMessageSourceTypeType
    TemplatedMessageConfig: NotRequired[TemplatedMessageConfigTypeDef]
    RawMessage: NotRequired[OutboundRawMessageTypeDef]


class ContactAnalysisTypeDef(TypedDict):
    Transcript: NotRequired[TranscriptTypeDef]


class SearchUsersResponseTypeDef(TypedDict):
    Users: List[UserSearchSummaryTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateViewResponseTypeDef(TypedDict):
    View: ViewTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateViewVersionResponseTypeDef(TypedDict):
    View: ViewTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeViewResponseTypeDef(TypedDict):
    View: ViewTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateViewContentResponseTypeDef(TypedDict):
    View: ViewTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ExpressionOutputTypeDef(TypedDict):
    AttributeCondition: NotRequired[AttributeConditionOutputTypeDef]
    AndExpression: NotRequired[List[Dict[str, Any]]]
    OrExpression: NotRequired[List[Dict[str, Any]]]


MatchCriteriaUnionTypeDef = Union[MatchCriteriaTypeDef, MatchCriteriaOutputTypeDef]


class UserSearchFilterTypeDef(TypedDict):
    TagFilter: NotRequired[ControlPlaneTagFilterTypeDef]
    UserAttributeFilter: NotRequired[ControlPlaneUserAttributeFilterTypeDef]


class AgentStatusSearchFilterTypeDef(TypedDict):
    AttributeFilter: NotRequired[ControlPlaneAttributeFilterTypeDef]


class UserHierarchyGroupSearchFilterTypeDef(TypedDict):
    AttributeFilter: NotRequired[ControlPlaneAttributeFilterTypeDef]


class SearchContactFlowModulesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SearchFilter: NotRequired[ContactFlowModuleSearchFilterTypeDef]
    SearchCriteria: NotRequired[ContactFlowModuleSearchCriteriaTypeDef]


class SearchContactFlowModulesRequestSearchContactFlowModulesPaginateTypeDef(TypedDict):
    InstanceId: str
    SearchFilter: NotRequired[ContactFlowModuleSearchFilterTypeDef]
    SearchCriteria: NotRequired[ContactFlowModuleSearchCriteriaPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchContactFlowsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SearchFilter: NotRequired[ContactFlowSearchFilterTypeDef]
    SearchCriteria: NotRequired[ContactFlowSearchCriteriaTypeDef]


class SearchContactFlowsRequestSearchContactFlowsPaginateTypeDef(TypedDict):
    InstanceId: str
    SearchFilter: NotRequired[ContactFlowSearchFilterTypeDef]
    SearchCriteria: NotRequired[ContactFlowSearchCriteriaPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchEmailAddressesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SearchCriteria: NotRequired[EmailAddressSearchCriteriaTypeDef]
    SearchFilter: NotRequired[EmailAddressSearchFilterTypeDef]


class SearchHoursOfOperationsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SearchFilter: NotRequired[HoursOfOperationSearchFilterTypeDef]
    SearchCriteria: NotRequired[HoursOfOperationSearchCriteriaTypeDef]


class SearchHoursOfOperationsRequestSearchHoursOfOperationsPaginateTypeDef(TypedDict):
    InstanceId: str
    SearchFilter: NotRequired[HoursOfOperationSearchFilterTypeDef]
    SearchCriteria: NotRequired[HoursOfOperationSearchCriteriaPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchPromptsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SearchFilter: NotRequired[PromptSearchFilterTypeDef]
    SearchCriteria: NotRequired[PromptSearchCriteriaTypeDef]


class SearchPromptsRequestSearchPromptsPaginateTypeDef(TypedDict):
    InstanceId: str
    SearchFilter: NotRequired[PromptSearchFilterTypeDef]
    SearchCriteria: NotRequired[PromptSearchCriteriaPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchQueuesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SearchFilter: NotRequired[QueueSearchFilterTypeDef]
    SearchCriteria: NotRequired[QueueSearchCriteriaTypeDef]


class SearchQueuesRequestSearchQueuesPaginateTypeDef(TypedDict):
    InstanceId: str
    SearchFilter: NotRequired[QueueSearchFilterTypeDef]
    SearchCriteria: NotRequired[QueueSearchCriteriaPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchQuickConnectsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SearchFilter: NotRequired[QuickConnectSearchFilterTypeDef]
    SearchCriteria: NotRequired[QuickConnectSearchCriteriaTypeDef]


class SearchQuickConnectsRequestSearchQuickConnectsPaginateTypeDef(TypedDict):
    InstanceId: str
    SearchFilter: NotRequired[QuickConnectSearchFilterTypeDef]
    SearchCriteria: NotRequired[QuickConnectSearchCriteriaPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchRoutingProfilesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SearchFilter: NotRequired[RoutingProfileSearchFilterTypeDef]
    SearchCriteria: NotRequired[RoutingProfileSearchCriteriaTypeDef]


class SearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef(TypedDict):
    InstanceId: str
    SearchFilter: NotRequired[RoutingProfileSearchFilterTypeDef]
    SearchCriteria: NotRequired[RoutingProfileSearchCriteriaPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchSecurityProfilesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SearchCriteria: NotRequired[SecurityProfileSearchCriteriaTypeDef]
    SearchFilter: NotRequired[SecurityProfilesSearchFilterTypeDef]


class SearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef(TypedDict):
    InstanceId: str
    SearchCriteria: NotRequired[SecurityProfileSearchCriteriaPaginatorTypeDef]
    SearchFilter: NotRequired[SecurityProfilesSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ConnectionDataTypeDef(TypedDict):
    Attendee: NotRequired[AttendeeTypeDef]
    Meeting: NotRequired[MeetingTypeDef]


class UserSearchCriteriaPaginatorTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]
    ListCondition: NotRequired[ListConditionTypeDef]
    HierarchyGroupCondition: NotRequired[HierarchyGroupConditionTypeDef]


class UserSearchCriteriaTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[Mapping[str, Any]]]
    AndConditions: NotRequired[Sequence[Mapping[str, Any]]]
    StringCondition: NotRequired[StringConditionTypeDef]
    ListCondition: NotRequired[ListConditionTypeDef]
    HierarchyGroupCondition: NotRequired[HierarchyGroupConditionTypeDef]


class DescribeRoutingProfileResponseTypeDef(TypedDict):
    RoutingProfile: RoutingProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchRoutingProfilesResponseTypeDef(TypedDict):
    RoutingProfiles: List[RoutingProfileTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetCurrentMetricDataResponseTypeDef(TypedDict):
    MetricResults: List[CurrentMetricResultTypeDef]
    DataSnapshotTime: datetime
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AssociateInstanceStorageConfigRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ResourceType: InstanceStorageResourceTypeType
    StorageConfig: InstanceStorageConfigTypeDef


class DescribeInstanceStorageConfigResponseTypeDef(TypedDict):
    StorageConfig: InstanceStorageConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListInstanceStorageConfigsResponseTypeDef(TypedDict):
    StorageConfigs: List[InstanceStorageConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateInstanceStorageConfigRequestRequestTypeDef(TypedDict):
    InstanceId: str
    AssociationId: str
    ResourceType: InstanceStorageResourceTypeType
    StorageConfig: InstanceStorageConfigTypeDef


EvaluationFormNumericQuestionPropertiesUnionTypeDef = Union[
    EvaluationFormNumericQuestionPropertiesTypeDef,
    EvaluationFormNumericQuestionPropertiesOutputTypeDef,
]


class EvaluationFormSingleSelectQuestionPropertiesOutputTypeDef(TypedDict):
    Options: List[EvaluationFormSingleSelectQuestionOptionTypeDef]
    DisplayAs: NotRequired[EvaluationFormSingleSelectQuestionDisplayModeType]
    Automation: NotRequired[EvaluationFormSingleSelectQuestionAutomationOutputTypeDef]


EvaluationFormSingleSelectQuestionAutomationUnionTypeDef = Union[
    EvaluationFormSingleSelectQuestionAutomationTypeDef,
    EvaluationFormSingleSelectQuestionAutomationOutputTypeDef,
]


class RuleActionOutputTypeDef(TypedDict):
    ActionType: ActionTypeType
    TaskAction: NotRequired[TaskActionDefinitionOutputTypeDef]
    EventBridgeAction: NotRequired[EventBridgeActionDefinitionTypeDef]
    AssignContactCategoryAction: NotRequired[Dict[str, Any]]
    SendNotificationAction: NotRequired[SendNotificationActionDefinitionOutputTypeDef]
    CreateCaseAction: NotRequired[CreateCaseActionDefinitionOutputTypeDef]
    UpdateCaseAction: NotRequired[UpdateCaseActionDefinitionOutputTypeDef]
    EndAssociatedTasksAction: NotRequired[Dict[str, Any]]
    SubmitAutoEvaluationAction: NotRequired[SubmitAutoEvaluationActionDefinitionTypeDef]


FieldValueExtraUnionTypeDef = Union[FieldValueTypeDef, FieldValueOutputTypeDef]


class UpdateCaseActionDefinitionTypeDef(TypedDict):
    Fields: Sequence[FieldValueTypeDef]


class GetCurrentUserDataResponseTypeDef(TypedDict):
    UserDataList: List[UserDataTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeUserHierarchyGroupResponseTypeDef(TypedDict):
    HierarchyGroup: HierarchyGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchUserHierarchyGroupsResponseTypeDef(TypedDict):
    UserHierarchyGroups: List[HierarchyGroupTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class HistoricalMetricResultTypeDef(TypedDict):
    Dimensions: NotRequired[DimensionsTypeDef]
    Collections: NotRequired[List[HistoricalMetricDataTypeDef]]


class DescribeHoursOfOperationResponseTypeDef(TypedDict):
    HoursOfOperation: HoursOfOperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchHoursOfOperationsResponseTypeDef(TypedDict):
    HoursOfOperations: List[HoursOfOperationTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetTaskTemplateResponseTypeDef(TypedDict):
    InstanceId: str
    Id: str
    Arn: str
    Name: str
    Description: str
    ContactFlowId: str
    SelfAssignFlowId: str
    Constraints: TaskTemplateConstraintsOutputTypeDef
    Defaults: TaskTemplateDefaultsOutputTypeDef
    Fields: List[TaskTemplateFieldOutputTypeDef]
    Status: TaskTemplateStatusType
    LastModifiedTime: datetime
    CreatedTime: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTaskTemplateResponseTypeDef(TypedDict):
    InstanceId: str
    Id: str
    Arn: str
    Name: str
    Description: str
    ContactFlowId: str
    SelfAssignFlowId: str
    Constraints: TaskTemplateConstraintsOutputTypeDef
    Defaults: TaskTemplateDefaultsOutputTypeDef
    Fields: List[TaskTemplateFieldOutputTypeDef]
    Status: TaskTemplateStatusType
    LastModifiedTime: datetime
    CreatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTaskTemplateRequestRequestTypeDef(TypedDict):
    TaskTemplateId: str
    InstanceId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    ContactFlowId: NotRequired[str]
    SelfAssignFlowId: NotRequired[str]
    Constraints: NotRequired[TaskTemplateConstraintsTypeDef]
    Defaults: NotRequired[TaskTemplateDefaultsTypeDef]
    Status: NotRequired[TaskTemplateStatusType]
    Fields: NotRequired[Sequence[TaskTemplateFieldTypeDef]]


class CreateTaskTemplateRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str
    Fields: Sequence[TaskTemplateFieldUnionTypeDef]
    Description: NotRequired[str]
    ContactFlowId: NotRequired[str]
    SelfAssignFlowId: NotRequired[str]
    Constraints: NotRequired[TaskTemplateConstraintsTypeDef]
    Defaults: NotRequired[TaskTemplateDefaultsTypeDef]
    Status: NotRequired[TaskTemplateStatusType]
    ClientToken: NotRequired[str]


MetricV2UnionTypeDef = Union[MetricV2TypeDef, MetricV2OutputTypeDef]


class MetricResultV2TypeDef(TypedDict):
    Dimensions: NotRequired[Dict[str, str]]
    MetricInterval: NotRequired[MetricIntervalTypeDef]
    Collections: NotRequired[List[MetricDataV2TypeDef]]


SendNotificationActionDefinitionUnionTypeDef = Union[
    SendNotificationActionDefinitionTypeDef, SendNotificationActionDefinitionOutputTypeDef
]


class UpdateParticipantRoleConfigChannelInfoTypeDef(TypedDict):
    Chat: NotRequired[ChatParticipantRoleConfigTypeDef]


class DescribeQuickConnectResponseTypeDef(TypedDict):
    QuickConnect: QuickConnectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchQuickConnectsResponseTypeDef(TypedDict):
    QuickConnects: List[QuickConnectTypeDef]
    ApproximateTotalCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RealTimeContactAnalysisCategoryDetailsTypeDef(TypedDict):
    PointsOfInterest: List[RealTimeContactAnalysisPointOfInterestTypeDef]


class RealTimeContactAnalysisSegmentIssuesTypeDef(TypedDict):
    IssuesDetected: List[RealTimeContactAnalysisIssueDetectedTypeDef]


class SendOutboundEmailRequestRequestTypeDef(TypedDict):
    InstanceId: str
    FromEmailAddress: EmailAddressInfoTypeDef
    DestinationEmailAddress: EmailAddressInfoTypeDef
    EmailMessage: OutboundEmailContentTypeDef
    TrafficType: TrafficTypeType
    AdditionalRecipients: NotRequired[OutboundAdditionalRecipientsTypeDef]
    SourceCampaign: NotRequired[SourceCampaignTypeDef]
    ClientToken: NotRequired[str]


class StartOutboundEmailContactRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    DestinationEmailAddress: EmailAddressInfoTypeDef
    EmailMessage: OutboundEmailContentTypeDef
    FromEmailAddress: NotRequired[EmailAddressInfoTypeDef]
    AdditionalRecipients: NotRequired[OutboundAdditionalRecipientsTypeDef]
    ClientToken: NotRequired[str]


class SearchCriteriaTypeDef(TypedDict):
    AgentIds: NotRequired[Sequence[str]]
    AgentHierarchyGroups: NotRequired[AgentHierarchyGroupsTypeDef]
    Channels: NotRequired[Sequence[ChannelType]]
    ContactAnalysis: NotRequired[ContactAnalysisTypeDef]
    InitiationMethods: NotRequired[Sequence[ContactInitiationMethodType]]
    QueueIds: NotRequired[Sequence[str]]
    SearchableContactAttributes: NotRequired[SearchableContactAttributesTypeDef]
    SearchableSegmentAttributes: NotRequired[SearchableSegmentAttributesTypeDef]


class StepTypeDef(TypedDict):
    Expiry: NotRequired[ExpiryTypeDef]
    Expression: NotRequired[ExpressionOutputTypeDef]
    Status: NotRequired[RoutingCriteriaStepStatusType]


class AttributeConditionTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]
    ProficiencyLevel: NotRequired[float]
    MatchCriteria: NotRequired[MatchCriteriaUnionTypeDef]
    ComparisonOperator: NotRequired[str]


class SearchAgentStatusesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SearchFilter: NotRequired[AgentStatusSearchFilterTypeDef]
    SearchCriteria: NotRequired[AgentStatusSearchCriteriaTypeDef]


class SearchAgentStatusesRequestSearchAgentStatusesPaginateTypeDef(TypedDict):
    InstanceId: str
    SearchFilter: NotRequired[AgentStatusSearchFilterTypeDef]
    SearchCriteria: NotRequired[AgentStatusSearchCriteriaPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchUserHierarchyGroupsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SearchFilter: NotRequired[UserHierarchyGroupSearchFilterTypeDef]
    SearchCriteria: NotRequired[UserHierarchyGroupSearchCriteriaTypeDef]


class SearchUserHierarchyGroupsRequestSearchUserHierarchyGroupsPaginateTypeDef(TypedDict):
    InstanceId: str
    SearchFilter: NotRequired[UserHierarchyGroupSearchFilterTypeDef]
    SearchCriteria: NotRequired[UserHierarchyGroupSearchCriteriaPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class StartWebRTCContactResponseTypeDef(TypedDict):
    ConnectionData: ConnectionDataTypeDef
    ContactId: str
    ParticipantId: str
    ParticipantToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class SearchUsersRequestSearchUsersPaginateTypeDef(TypedDict):
    InstanceId: str
    SearchFilter: NotRequired[UserSearchFilterTypeDef]
    SearchCriteria: NotRequired[UserSearchCriteriaPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchUsersRequestRequestTypeDef(TypedDict):
    InstanceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SearchFilter: NotRequired[UserSearchFilterTypeDef]
    SearchCriteria: NotRequired[UserSearchCriteriaTypeDef]


class EvaluationFormQuestionTypePropertiesOutputTypeDef(TypedDict):
    Numeric: NotRequired[EvaluationFormNumericQuestionPropertiesOutputTypeDef]
    SingleSelect: NotRequired[EvaluationFormSingleSelectQuestionPropertiesOutputTypeDef]


class EvaluationFormSingleSelectQuestionPropertiesTypeDef(TypedDict):
    Options: Sequence[EvaluationFormSingleSelectQuestionOptionTypeDef]
    DisplayAs: NotRequired[EvaluationFormSingleSelectQuestionDisplayModeType]
    Automation: NotRequired[EvaluationFormSingleSelectQuestionAutomationUnionTypeDef]


class RuleTypeDef(TypedDict):
    Name: str
    RuleId: str
    RuleArn: str
    TriggerEventSource: RuleTriggerEventSourceTypeDef
    Function: str
    Actions: List[RuleActionOutputTypeDef]
    PublishStatus: RulePublishStatusType
    CreatedTime: datetime
    LastUpdatedTime: datetime
    LastUpdatedBy: str
    Tags: NotRequired[Dict[str, str]]


class CreateCaseActionDefinitionTypeDef(TypedDict):
    Fields: Sequence[FieldValueExtraUnionTypeDef]
    TemplateId: str


UpdateCaseActionDefinitionUnionTypeDef = Union[
    UpdateCaseActionDefinitionTypeDef, UpdateCaseActionDefinitionOutputTypeDef
]


class GetMetricDataResponseTypeDef(TypedDict):
    MetricResults: List[HistoricalMetricResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetMetricDataV2RequestRequestTypeDef(TypedDict):
    ResourceArn: str
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    Filters: Sequence[FilterV2TypeDef]
    Metrics: Sequence[MetricV2UnionTypeDef]
    Interval: NotRequired[IntervalDetailsTypeDef]
    Groupings: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class GetMetricDataV2ResponseTypeDef(TypedDict):
    MetricResults: List[MetricResultV2TypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateParticipantRoleConfigRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    ChannelConfiguration: UpdateParticipantRoleConfigChannelInfoTypeDef


class RealTimeContactAnalysisSegmentCategoriesTypeDef(TypedDict):
    MatchedDetails: Dict[str, RealTimeContactAnalysisCategoryDetailsTypeDef]


class SearchContactsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    TimeRange: SearchContactsTimeRangeTypeDef
    SearchCriteria: NotRequired[SearchCriteriaTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Sort: NotRequired[SortTypeDef]


class SearchContactsRequestSearchContactsPaginateTypeDef(TypedDict):
    InstanceId: str
    TimeRange: SearchContactsTimeRangeTypeDef
    SearchCriteria: NotRequired[SearchCriteriaTypeDef]
    Sort: NotRequired[SortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class RoutingCriteriaTypeDef(TypedDict):
    Steps: NotRequired[List[StepTypeDef]]
    ActivationTimestamp: NotRequired[datetime]
    Index: NotRequired[int]


AttributeConditionUnionTypeDef = Union[AttributeConditionTypeDef, AttributeConditionOutputTypeDef]


class EvaluationFormQuestionOutputTypeDef(TypedDict):
    Title: str
    RefId: str
    QuestionType: EvaluationFormQuestionTypeType
    Instructions: NotRequired[str]
    NotApplicableEnabled: NotRequired[bool]
    QuestionTypeProperties: NotRequired[EvaluationFormQuestionTypePropertiesOutputTypeDef]
    Weight: NotRequired[float]


EvaluationFormSingleSelectQuestionPropertiesUnionTypeDef = Union[
    EvaluationFormSingleSelectQuestionPropertiesTypeDef,
    EvaluationFormSingleSelectQuestionPropertiesOutputTypeDef,
]


class DescribeRuleResponseTypeDef(TypedDict):
    Rule: RuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


CreateCaseActionDefinitionUnionTypeDef = Union[
    CreateCaseActionDefinitionTypeDef, CreateCaseActionDefinitionOutputTypeDef
]


class RealtimeContactAnalysisSegmentTypeDef(TypedDict):
    Transcript: NotRequired[RealTimeContactAnalysisSegmentTranscriptTypeDef]
    Categories: NotRequired[RealTimeContactAnalysisSegmentCategoriesTypeDef]
    Issues: NotRequired[RealTimeContactAnalysisSegmentIssuesTypeDef]
    Event: NotRequired[RealTimeContactAnalysisSegmentEventTypeDef]
    Attachments: NotRequired[RealTimeContactAnalysisSegmentAttachmentsTypeDef]
    PostContactSummary: NotRequired[RealTimeContactAnalysisSegmentPostContactSummaryTypeDef]


class ContactTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]
    InitialContactId: NotRequired[str]
    PreviousContactId: NotRequired[str]
    ContactAssociationId: NotRequired[str]
    InitiationMethod: NotRequired[ContactInitiationMethodType]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Channel: NotRequired[ChannelType]
    QueueInfo: NotRequired[QueueInfoTypeDef]
    AgentInfo: NotRequired[AgentInfoTypeDef]
    InitiationTimestamp: NotRequired[datetime]
    DisconnectTimestamp: NotRequired[datetime]
    LastUpdateTimestamp: NotRequired[datetime]
    LastPausedTimestamp: NotRequired[datetime]
    LastResumedTimestamp: NotRequired[datetime]
    TotalPauseCount: NotRequired[int]
    TotalPauseDurationInSeconds: NotRequired[int]
    ScheduledTimestamp: NotRequired[datetime]
    RelatedContactId: NotRequired[str]
    WisdomInfo: NotRequired[WisdomInfoTypeDef]
    CustomerEndpoint: NotRequired[EndpointInfoTypeDef]
    SystemEndpoint: NotRequired[EndpointInfoTypeDef]
    QueueTimeAdjustmentSeconds: NotRequired[int]
    QueuePriority: NotRequired[int]
    Tags: NotRequired[Dict[str, str]]
    ConnectedToSystemTimestamp: NotRequired[datetime]
    RoutingCriteria: NotRequired[RoutingCriteriaTypeDef]
    Customer: NotRequired[CustomerTypeDef]
    Campaign: NotRequired[CampaignTypeDef]
    AnsweringMachineDetectionStatus: NotRequired[AnsweringMachineDetectionStatusType]
    CustomerVoiceActivity: NotRequired[CustomerVoiceActivityTypeDef]
    QualityMetrics: NotRequired[QualityMetricsTypeDef]
    DisconnectDetails: NotRequired[DisconnectDetailsTypeDef]
    AdditionalEmailRecipients: NotRequired[AdditionalEmailRecipientsTypeDef]
    SegmentAttributes: NotRequired[Dict[str, SegmentAttributeValueOutputTypeDef]]


class ExpressionTypeDef(TypedDict):
    AttributeCondition: NotRequired[AttributeConditionUnionTypeDef]
    AndExpression: NotRequired[Sequence[Mapping[str, Any]]]
    OrExpression: NotRequired[Sequence[Mapping[str, Any]]]


class EvaluationFormItemOutputTypeDef(TypedDict):
    Section: NotRequired[EvaluationFormSectionOutputTypeDef]
    Question: NotRequired[EvaluationFormQuestionOutputTypeDef]


class EvaluationFormQuestionTypePropertiesTypeDef(TypedDict):
    Numeric: NotRequired[EvaluationFormNumericQuestionPropertiesUnionTypeDef]
    SingleSelect: NotRequired[EvaluationFormSingleSelectQuestionPropertiesUnionTypeDef]


class RuleActionTypeDef(TypedDict):
    ActionType: ActionTypeType
    TaskAction: NotRequired[TaskActionDefinitionUnionTypeDef]
    EventBridgeAction: NotRequired[EventBridgeActionDefinitionTypeDef]
    AssignContactCategoryAction: NotRequired[Mapping[str, Any]]
    SendNotificationAction: NotRequired[SendNotificationActionDefinitionUnionTypeDef]
    CreateCaseAction: NotRequired[CreateCaseActionDefinitionUnionTypeDef]
    UpdateCaseAction: NotRequired[UpdateCaseActionDefinitionUnionTypeDef]
    EndAssociatedTasksAction: NotRequired[Mapping[str, Any]]
    SubmitAutoEvaluationAction: NotRequired[SubmitAutoEvaluationActionDefinitionTypeDef]


class ListRealtimeContactAnalysisSegmentsV2ResponseTypeDef(TypedDict):
    Channel: RealTimeContactAnalysisSupportedChannelType
    Status: RealTimeContactAnalysisStatusType
    Segments: List[RealtimeContactAnalysisSegmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeContactResponseTypeDef(TypedDict):
    Contact: ContactTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ExpressionUnionTypeDef = Union[ExpressionTypeDef, ExpressionOutputTypeDef]


class EvaluationFormContentTypeDef(TypedDict):
    EvaluationFormVersion: int
    EvaluationFormId: str
    EvaluationFormArn: str
    Title: str
    Items: List[EvaluationFormItemOutputTypeDef]
    Description: NotRequired[str]
    ScoringStrategy: NotRequired[EvaluationFormScoringStrategyTypeDef]


class EvaluationFormTypeDef(TypedDict):
    EvaluationFormId: str
    EvaluationFormVersion: int
    Locked: bool
    EvaluationFormArn: str
    Title: str
    Status: EvaluationFormVersionStatusType
    Items: List[EvaluationFormItemOutputTypeDef]
    CreatedTime: datetime
    CreatedBy: str
    LastModifiedTime: datetime
    LastModifiedBy: str
    Description: NotRequired[str]
    ScoringStrategy: NotRequired[EvaluationFormScoringStrategyTypeDef]
    Tags: NotRequired[Dict[str, str]]


EvaluationFormQuestionTypePropertiesUnionTypeDef = Union[
    EvaluationFormQuestionTypePropertiesTypeDef, EvaluationFormQuestionTypePropertiesOutputTypeDef
]
RuleActionUnionTypeDef = Union[RuleActionTypeDef, RuleActionOutputTypeDef]


class UpdateRuleRequestRequestTypeDef(TypedDict):
    RuleId: str
    InstanceId: str
    Name: str
    Function: str
    Actions: Sequence[RuleActionTypeDef]
    PublishStatus: RulePublishStatusType


class RoutingCriteriaInputStepTypeDef(TypedDict):
    Expiry: NotRequired[RoutingCriteriaInputStepExpiryTypeDef]
    Expression: NotRequired[ExpressionUnionTypeDef]


class DescribeContactEvaluationResponseTypeDef(TypedDict):
    Evaluation: EvaluationTypeDef
    EvaluationForm: EvaluationFormContentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEvaluationFormResponseTypeDef(TypedDict):
    EvaluationForm: EvaluationFormTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EvaluationFormQuestionTypeDef(TypedDict):
    Title: str
    RefId: str
    QuestionType: EvaluationFormQuestionTypeType
    Instructions: NotRequired[str]
    NotApplicableEnabled: NotRequired[bool]
    QuestionTypeProperties: NotRequired[EvaluationFormQuestionTypePropertiesUnionTypeDef]
    Weight: NotRequired[float]


class CreateRuleRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str
    TriggerEventSource: RuleTriggerEventSourceTypeDef
    Function: str
    Actions: Sequence[RuleActionUnionTypeDef]
    PublishStatus: RulePublishStatusType
    ClientToken: NotRequired[str]


class RoutingCriteriaInputTypeDef(TypedDict):
    Steps: NotRequired[Sequence[RoutingCriteriaInputStepTypeDef]]


EvaluationFormQuestionUnionTypeDef = Union[
    EvaluationFormQuestionTypeDef, EvaluationFormQuestionOutputTypeDef
]


class UpdateContactRoutingDataRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    QueueTimeAdjustmentSeconds: NotRequired[int]
    QueuePriority: NotRequired[int]
    RoutingCriteria: NotRequired[RoutingCriteriaInputTypeDef]


class EvaluationFormItemTypeDef(TypedDict):
    Section: NotRequired[EvaluationFormSectionUnionTypeDef]
    Question: NotRequired[EvaluationFormQuestionUnionTypeDef]


EvaluationFormItemUnionTypeDef = Union[EvaluationFormItemTypeDef, EvaluationFormItemOutputTypeDef]


class UpdateEvaluationFormRequestRequestTypeDef(TypedDict):
    InstanceId: str
    EvaluationFormId: str
    EvaluationFormVersion: int
    Title: str
    Items: Sequence[EvaluationFormItemTypeDef]
    CreateNewVersion: NotRequired[bool]
    Description: NotRequired[str]
    ScoringStrategy: NotRequired[EvaluationFormScoringStrategyTypeDef]
    ClientToken: NotRequired[str]


class CreateEvaluationFormRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Title: str
    Items: Sequence[EvaluationFormItemUnionTypeDef]
    Description: NotRequired[str]
    ScoringStrategy: NotRequired[EvaluationFormScoringStrategyTypeDef]
    ClientToken: NotRequired[str]
