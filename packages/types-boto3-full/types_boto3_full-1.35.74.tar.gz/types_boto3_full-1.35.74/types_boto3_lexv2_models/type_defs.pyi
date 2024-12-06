"""
Type annotations for lexv2-models service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_models/type_defs/)

Usage::

    ```python
    from types_boto3_lexv2_models.type_defs import ActiveContextTypeDef

    data: ActiveContextTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AggregatedUtterancesFilterOperatorType,
    AggregatedUtterancesSortAttributeType,
    AnalyticsBinByNameType,
    AnalyticsCommonFilterNameType,
    AnalyticsFilterOperatorType,
    AnalyticsIntentFieldType,
    AnalyticsIntentFilterNameType,
    AnalyticsIntentMetricNameType,
    AnalyticsIntentStageFieldType,
    AnalyticsIntentStageFilterNameType,
    AnalyticsIntentStageMetricNameType,
    AnalyticsIntervalType,
    AnalyticsMetricStatisticType,
    AnalyticsModalityType,
    AnalyticsNodeTypeType,
    AnalyticsSessionFieldType,
    AnalyticsSessionFilterNameType,
    AnalyticsSessionMetricNameType,
    AnalyticsSessionSortByNameType,
    AnalyticsSortOrderType,
    AnalyticsUtteranceFieldType,
    AnalyticsUtteranceFilterNameType,
    AnalyticsUtteranceMetricNameType,
    AssociatedTranscriptFilterNameType,
    BedrockTraceStatusType,
    BotAliasReplicationStatusType,
    BotAliasStatusType,
    BotFilterNameType,
    BotFilterOperatorType,
    BotLocaleFilterOperatorType,
    BotLocaleStatusType,
    BotRecommendationStatusType,
    BotReplicaStatusType,
    BotStatusType,
    BotTypeType,
    BotVersionReplicationStatusType,
    ConversationEndStateType,
    ConversationLogsInputModeFilterType,
    CustomVocabularyStatusType,
    DialogActionTypeType,
    EffectType,
    ErrorCodeType,
    ExportFilterOperatorType,
    ExportStatusType,
    GenerationSortByAttributeType,
    GenerationStatusType,
    ImportExportFileFormatType,
    ImportFilterOperatorType,
    ImportResourceTypeType,
    ImportStatusType,
    IntentFilterOperatorType,
    IntentSortAttributeType,
    IntentStateType,
    MergeStrategyType,
    MessageSelectionStrategyType,
    ObfuscationSettingTypeType,
    PromptAttemptType,
    SearchOrderType,
    SlotConstraintType,
    SlotFilterOperatorType,
    SlotResolutionStrategyType,
    SlotShapeType,
    SlotSortAttributeType,
    SlotTypeCategoryType,
    SlotTypeFilterNameType,
    SlotTypeFilterOperatorType,
    SlotTypeSortAttributeType,
    SlotValueResolutionStrategyType,
    SortOrderType,
    TestExecutionApiModeType,
    TestExecutionModalityType,
    TestExecutionSortAttributeType,
    TestExecutionStatusType,
    TestResultMatchStatusType,
    TestResultTypeFilterType,
    TestSetDiscrepancyReportStatusType,
    TestSetGenerationStatusType,
    TestSetModalityType,
    TestSetSortAttributeType,
    TestSetStatusType,
    TimeDimensionType,
    UtteranceContentTypeType,
    VoiceEngineType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ActiveContextTypeDef",
    "AdvancedRecognitionSettingTypeDef",
    "AgentTurnResultTypeDef",
    "AgentTurnSpecificationTypeDef",
    "AggregatedUtterancesFilterTypeDef",
    "AggregatedUtterancesSortByTypeDef",
    "AggregatedUtterancesSummaryTypeDef",
    "AllowedInputTypesTypeDef",
    "AnalyticsBinBySpecificationTypeDef",
    "AnalyticsBinKeyTypeDef",
    "AnalyticsIntentFilterTypeDef",
    "AnalyticsIntentGroupByKeyTypeDef",
    "AnalyticsIntentGroupBySpecificationTypeDef",
    "AnalyticsIntentMetricResultTypeDef",
    "AnalyticsIntentMetricTypeDef",
    "AnalyticsIntentNodeSummaryTypeDef",
    "AnalyticsIntentResultTypeDef",
    "AnalyticsIntentStageFilterTypeDef",
    "AnalyticsIntentStageGroupByKeyTypeDef",
    "AnalyticsIntentStageGroupBySpecificationTypeDef",
    "AnalyticsIntentStageMetricResultTypeDef",
    "AnalyticsIntentStageMetricTypeDef",
    "AnalyticsIntentStageResultTypeDef",
    "AnalyticsPathFilterTypeDef",
    "AnalyticsSessionFilterTypeDef",
    "AnalyticsSessionGroupByKeyTypeDef",
    "AnalyticsSessionGroupBySpecificationTypeDef",
    "AnalyticsSessionMetricResultTypeDef",
    "AnalyticsSessionMetricTypeDef",
    "AnalyticsSessionResultTypeDef",
    "AnalyticsUtteranceAttributeResultTypeDef",
    "AnalyticsUtteranceAttributeTypeDef",
    "AnalyticsUtteranceFilterTypeDef",
    "AnalyticsUtteranceGroupByKeyTypeDef",
    "AnalyticsUtteranceGroupBySpecificationTypeDef",
    "AnalyticsUtteranceMetricResultTypeDef",
    "AnalyticsUtteranceMetricTypeDef",
    "AnalyticsUtteranceResultTypeDef",
    "AssociatedTranscriptFilterTypeDef",
    "AssociatedTranscriptTypeDef",
    "AudioAndDTMFInputSpecificationTypeDef",
    "AudioLogDestinationTypeDef",
    "AudioLogSettingTypeDef",
    "AudioSpecificationTypeDef",
    "BatchCreateCustomVocabularyItemRequestRequestTypeDef",
    "BatchCreateCustomVocabularyItemResponseTypeDef",
    "BatchDeleteCustomVocabularyItemRequestRequestTypeDef",
    "BatchDeleteCustomVocabularyItemResponseTypeDef",
    "BatchUpdateCustomVocabularyItemRequestRequestTypeDef",
    "BatchUpdateCustomVocabularyItemResponseTypeDef",
    "BedrockGuardrailConfigurationTypeDef",
    "BedrockKnowledgeStoreConfigurationTypeDef",
    "BedrockKnowledgeStoreExactResponseFieldsTypeDef",
    "BedrockModelSpecificationTypeDef",
    "BotAliasHistoryEventTypeDef",
    "BotAliasLocaleSettingsTypeDef",
    "BotAliasReplicaSummaryTypeDef",
    "BotAliasSummaryTypeDef",
    "BotAliasTestExecutionTargetTypeDef",
    "BotExportSpecificationTypeDef",
    "BotFilterTypeDef",
    "BotImportSpecificationOutputTypeDef",
    "BotImportSpecificationTypeDef",
    "BotImportSpecificationUnionTypeDef",
    "BotLocaleExportSpecificationTypeDef",
    "BotLocaleFilterTypeDef",
    "BotLocaleHistoryEventTypeDef",
    "BotLocaleImportSpecificationTypeDef",
    "BotLocaleSortByTypeDef",
    "BotLocaleSummaryTypeDef",
    "BotMemberTypeDef",
    "BotRecommendationResultStatisticsTypeDef",
    "BotRecommendationResultsTypeDef",
    "BotRecommendationSummaryTypeDef",
    "BotReplicaSummaryTypeDef",
    "BotSortByTypeDef",
    "BotSummaryTypeDef",
    "BotVersionLocaleDetailsTypeDef",
    "BotVersionReplicaSortByTypeDef",
    "BotVersionReplicaSummaryTypeDef",
    "BotVersionSortByTypeDef",
    "BotVersionSummaryTypeDef",
    "BuildBotLocaleRequestRequestTypeDef",
    "BuildBotLocaleResponseTypeDef",
    "BuildtimeSettingsTypeDef",
    "BuiltInIntentSortByTypeDef",
    "BuiltInIntentSummaryTypeDef",
    "BuiltInSlotTypeSortByTypeDef",
    "BuiltInSlotTypeSummaryTypeDef",
    "ButtonTypeDef",
    "CloudWatchLogGroupLogDestinationTypeDef",
    "CodeHookSpecificationTypeDef",
    "CompositeSlotTypeSettingOutputTypeDef",
    "CompositeSlotTypeSettingTypeDef",
    "ConditionTypeDef",
    "ConditionalBranchOutputTypeDef",
    "ConditionalBranchTypeDef",
    "ConditionalBranchUnionTypeDef",
    "ConditionalSpecificationOutputTypeDef",
    "ConditionalSpecificationTypeDef",
    "ConditionalSpecificationUnionTypeDef",
    "ConversationLevelIntentClassificationResultItemTypeDef",
    "ConversationLevelResultDetailTypeDef",
    "ConversationLevelSlotResolutionResultItemTypeDef",
    "ConversationLevelTestResultItemTypeDef",
    "ConversationLevelTestResultsFilterByTypeDef",
    "ConversationLevelTestResultsTypeDef",
    "ConversationLogSettingsOutputTypeDef",
    "ConversationLogSettingsTypeDef",
    "ConversationLogsDataSourceFilterByOutputTypeDef",
    "ConversationLogsDataSourceFilterByTypeDef",
    "ConversationLogsDataSourceFilterByUnionTypeDef",
    "ConversationLogsDataSourceOutputTypeDef",
    "ConversationLogsDataSourceTypeDef",
    "ConversationLogsDataSourceUnionTypeDef",
    "CreateBotAliasRequestRequestTypeDef",
    "CreateBotAliasResponseTypeDef",
    "CreateBotLocaleRequestRequestTypeDef",
    "CreateBotLocaleResponseTypeDef",
    "CreateBotReplicaRequestRequestTypeDef",
    "CreateBotReplicaResponseTypeDef",
    "CreateBotRequestRequestTypeDef",
    "CreateBotResponseTypeDef",
    "CreateBotVersionRequestRequestTypeDef",
    "CreateBotVersionResponseTypeDef",
    "CreateExportRequestRequestTypeDef",
    "CreateExportResponseTypeDef",
    "CreateIntentRequestRequestTypeDef",
    "CreateIntentResponseTypeDef",
    "CreateResourcePolicyRequestRequestTypeDef",
    "CreateResourcePolicyResponseTypeDef",
    "CreateResourcePolicyStatementRequestRequestTypeDef",
    "CreateResourcePolicyStatementResponseTypeDef",
    "CreateSlotRequestRequestTypeDef",
    "CreateSlotResponseTypeDef",
    "CreateSlotTypeRequestRequestTypeDef",
    "CreateSlotTypeResponseTypeDef",
    "CreateTestSetDiscrepancyReportRequestRequestTypeDef",
    "CreateTestSetDiscrepancyReportResponseTypeDef",
    "CreateUploadUrlResponseTypeDef",
    "CustomPayloadTypeDef",
    "CustomVocabularyEntryIdTypeDef",
    "CustomVocabularyExportSpecificationTypeDef",
    "CustomVocabularyImportSpecificationTypeDef",
    "CustomVocabularyItemTypeDef",
    "DTMFSpecificationTypeDef",
    "DataPrivacyTypeDef",
    "DataSourceConfigurationOutputTypeDef",
    "DataSourceConfigurationTypeDef",
    "DataSourceConfigurationUnionTypeDef",
    "DateRangeFilterOutputTypeDef",
    "DateRangeFilterTypeDef",
    "DateRangeFilterUnionTypeDef",
    "DefaultConditionalBranchOutputTypeDef",
    "DefaultConditionalBranchTypeDef",
    "DefaultConditionalBranchUnionTypeDef",
    "DeleteBotAliasRequestRequestTypeDef",
    "DeleteBotAliasResponseTypeDef",
    "DeleteBotLocaleRequestRequestTypeDef",
    "DeleteBotLocaleResponseTypeDef",
    "DeleteBotReplicaRequestRequestTypeDef",
    "DeleteBotReplicaResponseTypeDef",
    "DeleteBotRequestRequestTypeDef",
    "DeleteBotResponseTypeDef",
    "DeleteBotVersionRequestRequestTypeDef",
    "DeleteBotVersionResponseTypeDef",
    "DeleteCustomVocabularyRequestRequestTypeDef",
    "DeleteCustomVocabularyResponseTypeDef",
    "DeleteExportRequestRequestTypeDef",
    "DeleteExportResponseTypeDef",
    "DeleteImportRequestRequestTypeDef",
    "DeleteImportResponseTypeDef",
    "DeleteIntentRequestRequestTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteResourcePolicyResponseTypeDef",
    "DeleteResourcePolicyStatementRequestRequestTypeDef",
    "DeleteResourcePolicyStatementResponseTypeDef",
    "DeleteSlotRequestRequestTypeDef",
    "DeleteSlotTypeRequestRequestTypeDef",
    "DeleteTestSetRequestRequestTypeDef",
    "DeleteUtterancesRequestRequestTypeDef",
    "DescribeBotAliasRequestBotAliasAvailableWaitTypeDef",
    "DescribeBotAliasRequestRequestTypeDef",
    "DescribeBotAliasResponseTypeDef",
    "DescribeBotLocaleRequestBotLocaleBuiltWaitTypeDef",
    "DescribeBotLocaleRequestBotLocaleCreatedWaitTypeDef",
    "DescribeBotLocaleRequestBotLocaleExpressTestingAvailableWaitTypeDef",
    "DescribeBotLocaleRequestRequestTypeDef",
    "DescribeBotLocaleResponseTypeDef",
    "DescribeBotRecommendationRequestRequestTypeDef",
    "DescribeBotRecommendationResponseTypeDef",
    "DescribeBotReplicaRequestRequestTypeDef",
    "DescribeBotReplicaResponseTypeDef",
    "DescribeBotRequestBotAvailableWaitTypeDef",
    "DescribeBotRequestRequestTypeDef",
    "DescribeBotResourceGenerationRequestRequestTypeDef",
    "DescribeBotResourceGenerationResponseTypeDef",
    "DescribeBotResponseTypeDef",
    "DescribeBotVersionRequestBotVersionAvailableWaitTypeDef",
    "DescribeBotVersionRequestRequestTypeDef",
    "DescribeBotVersionResponseTypeDef",
    "DescribeCustomVocabularyMetadataRequestRequestTypeDef",
    "DescribeCustomVocabularyMetadataResponseTypeDef",
    "DescribeExportRequestBotExportCompletedWaitTypeDef",
    "DescribeExportRequestRequestTypeDef",
    "DescribeExportResponseTypeDef",
    "DescribeImportRequestBotImportCompletedWaitTypeDef",
    "DescribeImportRequestRequestTypeDef",
    "DescribeImportResponseTypeDef",
    "DescribeIntentRequestRequestTypeDef",
    "DescribeIntentResponseTypeDef",
    "DescribeResourcePolicyRequestRequestTypeDef",
    "DescribeResourcePolicyResponseTypeDef",
    "DescribeSlotRequestRequestTypeDef",
    "DescribeSlotResponseTypeDef",
    "DescribeSlotTypeRequestRequestTypeDef",
    "DescribeSlotTypeResponseTypeDef",
    "DescribeTestExecutionRequestRequestTypeDef",
    "DescribeTestExecutionResponseTypeDef",
    "DescribeTestSetDiscrepancyReportRequestRequestTypeDef",
    "DescribeTestSetDiscrepancyReportResponseTypeDef",
    "DescribeTestSetGenerationRequestRequestTypeDef",
    "DescribeTestSetGenerationResponseTypeDef",
    "DescribeTestSetRequestRequestTypeDef",
    "DescribeTestSetResponseTypeDef",
    "DescriptiveBotBuilderSpecificationTypeDef",
    "DialogActionTypeDef",
    "DialogCodeHookInvocationSettingOutputTypeDef",
    "DialogCodeHookInvocationSettingTypeDef",
    "DialogCodeHookInvocationSettingUnionTypeDef",
    "DialogCodeHookSettingsTypeDef",
    "DialogStateOutputTypeDef",
    "DialogStateTypeDef",
    "DialogStateUnionTypeDef",
    "ElicitationCodeHookInvocationSettingTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionSettingTypeDef",
    "ExactResponseFieldsTypeDef",
    "ExecutionErrorDetailsTypeDef",
    "ExportFilterTypeDef",
    "ExportResourceSpecificationTypeDef",
    "ExportSortByTypeDef",
    "ExportSummaryTypeDef",
    "ExternalSourceSettingTypeDef",
    "FailedCustomVocabularyItemTypeDef",
    "FulfillmentCodeHookSettingsOutputTypeDef",
    "FulfillmentCodeHookSettingsTypeDef",
    "FulfillmentStartResponseSpecificationOutputTypeDef",
    "FulfillmentStartResponseSpecificationTypeDef",
    "FulfillmentStartResponseSpecificationUnionTypeDef",
    "FulfillmentUpdateResponseSpecificationOutputTypeDef",
    "FulfillmentUpdateResponseSpecificationTypeDef",
    "FulfillmentUpdateResponseSpecificationUnionTypeDef",
    "FulfillmentUpdatesSpecificationOutputTypeDef",
    "FulfillmentUpdatesSpecificationTypeDef",
    "FulfillmentUpdatesSpecificationUnionTypeDef",
    "GenerateBotElementRequestRequestTypeDef",
    "GenerateBotElementResponseTypeDef",
    "GenerationSortByTypeDef",
    "GenerationSummaryTypeDef",
    "GenerativeAISettingsTypeDef",
    "GetTestExecutionArtifactsUrlRequestRequestTypeDef",
    "GetTestExecutionArtifactsUrlResponseTypeDef",
    "GrammarSlotTypeSettingTypeDef",
    "GrammarSlotTypeSourceTypeDef",
    "ImageResponseCardOutputTypeDef",
    "ImageResponseCardTypeDef",
    "ImageResponseCardUnionTypeDef",
    "ImportFilterTypeDef",
    "ImportResourceSpecificationOutputTypeDef",
    "ImportResourceSpecificationTypeDef",
    "ImportSortByTypeDef",
    "ImportSummaryTypeDef",
    "InitialResponseSettingOutputTypeDef",
    "InitialResponseSettingTypeDef",
    "InputContextTypeDef",
    "InputSessionStateSpecificationTypeDef",
    "IntentClassificationTestResultItemCountsTypeDef",
    "IntentClassificationTestResultItemTypeDef",
    "IntentClassificationTestResultsTypeDef",
    "IntentClosingSettingOutputTypeDef",
    "IntentClosingSettingTypeDef",
    "IntentConfirmationSettingOutputTypeDef",
    "IntentConfirmationSettingTypeDef",
    "IntentFilterTypeDef",
    "IntentLevelSlotResolutionTestResultItemTypeDef",
    "IntentLevelSlotResolutionTestResultsTypeDef",
    "IntentOverrideOutputTypeDef",
    "IntentOverrideTypeDef",
    "IntentOverrideUnionTypeDef",
    "IntentSortByTypeDef",
    "IntentStatisticsTypeDef",
    "IntentSummaryTypeDef",
    "InvokedIntentSampleTypeDef",
    "KendraConfigurationTypeDef",
    "LambdaCodeHookTypeDef",
    "LexTranscriptFilterOutputTypeDef",
    "LexTranscriptFilterTypeDef",
    "LexTranscriptFilterUnionTypeDef",
    "ListAggregatedUtterancesRequestRequestTypeDef",
    "ListAggregatedUtterancesResponseTypeDef",
    "ListBotAliasReplicasRequestRequestTypeDef",
    "ListBotAliasReplicasResponseTypeDef",
    "ListBotAliasesRequestRequestTypeDef",
    "ListBotAliasesResponseTypeDef",
    "ListBotLocalesRequestRequestTypeDef",
    "ListBotLocalesResponseTypeDef",
    "ListBotRecommendationsRequestRequestTypeDef",
    "ListBotRecommendationsResponseTypeDef",
    "ListBotReplicasRequestRequestTypeDef",
    "ListBotReplicasResponseTypeDef",
    "ListBotResourceGenerationsRequestRequestTypeDef",
    "ListBotResourceGenerationsResponseTypeDef",
    "ListBotVersionReplicasRequestRequestTypeDef",
    "ListBotVersionReplicasResponseTypeDef",
    "ListBotVersionsRequestRequestTypeDef",
    "ListBotVersionsResponseTypeDef",
    "ListBotsRequestRequestTypeDef",
    "ListBotsResponseTypeDef",
    "ListBuiltInIntentsRequestRequestTypeDef",
    "ListBuiltInIntentsResponseTypeDef",
    "ListBuiltInSlotTypesRequestRequestTypeDef",
    "ListBuiltInSlotTypesResponseTypeDef",
    "ListCustomVocabularyItemsRequestRequestTypeDef",
    "ListCustomVocabularyItemsResponseTypeDef",
    "ListExportsRequestRequestTypeDef",
    "ListExportsResponseTypeDef",
    "ListImportsRequestRequestTypeDef",
    "ListImportsResponseTypeDef",
    "ListIntentMetricsRequestRequestTypeDef",
    "ListIntentMetricsResponseTypeDef",
    "ListIntentPathsRequestRequestTypeDef",
    "ListIntentPathsResponseTypeDef",
    "ListIntentStageMetricsRequestRequestTypeDef",
    "ListIntentStageMetricsResponseTypeDef",
    "ListIntentsRequestRequestTypeDef",
    "ListIntentsResponseTypeDef",
    "ListRecommendedIntentsRequestRequestTypeDef",
    "ListRecommendedIntentsResponseTypeDef",
    "ListSessionAnalyticsDataRequestRequestTypeDef",
    "ListSessionAnalyticsDataResponseTypeDef",
    "ListSessionMetricsRequestRequestTypeDef",
    "ListSessionMetricsResponseTypeDef",
    "ListSlotTypesRequestRequestTypeDef",
    "ListSlotTypesResponseTypeDef",
    "ListSlotsRequestRequestTypeDef",
    "ListSlotsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTestExecutionResultItemsRequestRequestTypeDef",
    "ListTestExecutionResultItemsResponseTypeDef",
    "ListTestExecutionsRequestRequestTypeDef",
    "ListTestExecutionsResponseTypeDef",
    "ListTestSetRecordsRequestRequestTypeDef",
    "ListTestSetRecordsResponseTypeDef",
    "ListTestSetsRequestRequestTypeDef",
    "ListTestSetsResponseTypeDef",
    "ListUtteranceAnalyticsDataRequestRequestTypeDef",
    "ListUtteranceAnalyticsDataResponseTypeDef",
    "ListUtteranceMetricsRequestRequestTypeDef",
    "ListUtteranceMetricsResponseTypeDef",
    "MessageGroupOutputTypeDef",
    "MessageGroupTypeDef",
    "MessageGroupUnionTypeDef",
    "MessageOutputTypeDef",
    "MessageTypeDef",
    "MessageUnionTypeDef",
    "MultipleValuesSettingTypeDef",
    "NewCustomVocabularyItemTypeDef",
    "ObfuscationSettingTypeDef",
    "OpensearchConfigurationOutputTypeDef",
    "OpensearchConfigurationTypeDef",
    "OpensearchConfigurationUnionTypeDef",
    "OutputContextTypeDef",
    "OverallTestResultItemTypeDef",
    "OverallTestResultsTypeDef",
    "ParentBotNetworkTypeDef",
    "PathFormatOutputTypeDef",
    "PathFormatTypeDef",
    "PathFormatUnionTypeDef",
    "PlainTextMessageTypeDef",
    "PostDialogCodeHookInvocationSpecificationOutputTypeDef",
    "PostDialogCodeHookInvocationSpecificationTypeDef",
    "PostDialogCodeHookInvocationSpecificationUnionTypeDef",
    "PostFulfillmentStatusSpecificationOutputTypeDef",
    "PostFulfillmentStatusSpecificationTypeDef",
    "PostFulfillmentStatusSpecificationUnionTypeDef",
    "PrincipalTypeDef",
    "PromptAttemptSpecificationTypeDef",
    "PromptSpecificationOutputTypeDef",
    "PromptSpecificationTypeDef",
    "PromptSpecificationUnionTypeDef",
    "QnAIntentConfigurationOutputTypeDef",
    "QnAIntentConfigurationTypeDef",
    "QnAKendraConfigurationTypeDef",
    "RecommendedIntentSummaryTypeDef",
    "RelativeAggregationDurationTypeDef",
    "ResponseMetadataTypeDef",
    "ResponseSpecificationOutputTypeDef",
    "ResponseSpecificationTypeDef",
    "ResponseSpecificationUnionTypeDef",
    "RuntimeHintDetailsTypeDef",
    "RuntimeHintValueTypeDef",
    "RuntimeHintsTypeDef",
    "RuntimeSettingsTypeDef",
    "S3BucketLogDestinationTypeDef",
    "S3BucketTranscriptSourceOutputTypeDef",
    "S3BucketTranscriptSourceTypeDef",
    "S3BucketTranscriptSourceUnionTypeDef",
    "SSMLMessageTypeDef",
    "SampleUtteranceGenerationSpecificationTypeDef",
    "SampleUtteranceTypeDef",
    "SampleValueTypeDef",
    "SearchAssociatedTranscriptsRequestRequestTypeDef",
    "SearchAssociatedTranscriptsResponseTypeDef",
    "SentimentAnalysisSettingsTypeDef",
    "SessionDataSortByTypeDef",
    "SessionSpecificationTypeDef",
    "SlotCaptureSettingOutputTypeDef",
    "SlotCaptureSettingTypeDef",
    "SlotCaptureSettingUnionTypeDef",
    "SlotDefaultValueSpecificationOutputTypeDef",
    "SlotDefaultValueSpecificationTypeDef",
    "SlotDefaultValueSpecificationUnionTypeDef",
    "SlotDefaultValueTypeDef",
    "SlotFilterTypeDef",
    "SlotPriorityTypeDef",
    "SlotResolutionImprovementSpecificationTypeDef",
    "SlotResolutionSettingTypeDef",
    "SlotResolutionTestResultItemCountsTypeDef",
    "SlotResolutionTestResultItemTypeDef",
    "SlotSortByTypeDef",
    "SlotSummaryTypeDef",
    "SlotTypeFilterTypeDef",
    "SlotTypeSortByTypeDef",
    "SlotTypeStatisticsTypeDef",
    "SlotTypeSummaryTypeDef",
    "SlotTypeValueOutputTypeDef",
    "SlotTypeValueTypeDef",
    "SlotTypeValueUnionTypeDef",
    "SlotValueElicitationSettingOutputTypeDef",
    "SlotValueElicitationSettingTypeDef",
    "SlotValueOverrideOutputTypeDef",
    "SlotValueOverrideTypeDef",
    "SlotValueOverrideUnionTypeDef",
    "SlotValueRegexFilterTypeDef",
    "SlotValueSelectionSettingTypeDef",
    "SlotValueTypeDef",
    "SpecificationsOutputTypeDef",
    "SpecificationsTypeDef",
    "SpecificationsUnionTypeDef",
    "StartBotRecommendationRequestRequestTypeDef",
    "StartBotRecommendationResponseTypeDef",
    "StartBotResourceGenerationRequestRequestTypeDef",
    "StartBotResourceGenerationResponseTypeDef",
    "StartImportRequestRequestTypeDef",
    "StartImportResponseTypeDef",
    "StartTestExecutionRequestRequestTypeDef",
    "StartTestExecutionResponseTypeDef",
    "StartTestSetGenerationRequestRequestTypeDef",
    "StartTestSetGenerationResponseTypeDef",
    "StillWaitingResponseSpecificationOutputTypeDef",
    "StillWaitingResponseSpecificationTypeDef",
    "StillWaitingResponseSpecificationUnionTypeDef",
    "StopBotRecommendationRequestRequestTypeDef",
    "StopBotRecommendationResponseTypeDef",
    "SubSlotSettingOutputTypeDef",
    "SubSlotSettingTypeDef",
    "SubSlotTypeCompositionTypeDef",
    "SubSlotValueElicitationSettingOutputTypeDef",
    "SubSlotValueElicitationSettingTypeDef",
    "SubSlotValueElicitationSettingUnionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TestExecutionResultFilterByTypeDef",
    "TestExecutionResultItemsTypeDef",
    "TestExecutionSortByTypeDef",
    "TestExecutionSummaryTypeDef",
    "TestExecutionTargetTypeDef",
    "TestSetDiscrepancyErrorsTypeDef",
    "TestSetDiscrepancyReportBotAliasTargetTypeDef",
    "TestSetDiscrepancyReportResourceTargetTypeDef",
    "TestSetExportSpecificationTypeDef",
    "TestSetGenerationDataSourceOutputTypeDef",
    "TestSetGenerationDataSourceTypeDef",
    "TestSetImportInputLocationTypeDef",
    "TestSetImportResourceSpecificationOutputTypeDef",
    "TestSetImportResourceSpecificationTypeDef",
    "TestSetImportResourceSpecificationUnionTypeDef",
    "TestSetIntentDiscrepancyItemTypeDef",
    "TestSetSlotDiscrepancyItemTypeDef",
    "TestSetSortByTypeDef",
    "TestSetStorageLocationTypeDef",
    "TestSetSummaryTypeDef",
    "TestSetTurnRecordTypeDef",
    "TestSetTurnResultTypeDef",
    "TextInputSpecificationTypeDef",
    "TextLogDestinationTypeDef",
    "TextLogSettingTypeDef",
    "TimestampTypeDef",
    "TranscriptFilterOutputTypeDef",
    "TranscriptFilterTypeDef",
    "TranscriptFilterUnionTypeDef",
    "TranscriptSourceSettingOutputTypeDef",
    "TranscriptSourceSettingTypeDef",
    "TurnSpecificationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBotAliasRequestRequestTypeDef",
    "UpdateBotAliasResponseTypeDef",
    "UpdateBotLocaleRequestRequestTypeDef",
    "UpdateBotLocaleResponseTypeDef",
    "UpdateBotRecommendationRequestRequestTypeDef",
    "UpdateBotRecommendationResponseTypeDef",
    "UpdateBotRequestRequestTypeDef",
    "UpdateBotResponseTypeDef",
    "UpdateExportRequestRequestTypeDef",
    "UpdateExportResponseTypeDef",
    "UpdateIntentRequestRequestTypeDef",
    "UpdateIntentResponseTypeDef",
    "UpdateResourcePolicyRequestRequestTypeDef",
    "UpdateResourcePolicyResponseTypeDef",
    "UpdateSlotRequestRequestTypeDef",
    "UpdateSlotResponseTypeDef",
    "UpdateSlotTypeRequestRequestTypeDef",
    "UpdateSlotTypeResponseTypeDef",
    "UpdateTestSetRequestRequestTypeDef",
    "UpdateTestSetResponseTypeDef",
    "UserTurnInputSpecificationTypeDef",
    "UserTurnIntentOutputTypeDef",
    "UserTurnOutputSpecificationTypeDef",
    "UserTurnResultTypeDef",
    "UserTurnSlotOutputTypeDef",
    "UserTurnSpecificationTypeDef",
    "UtteranceAggregationDurationTypeDef",
    "UtteranceAudioInputSpecificationTypeDef",
    "UtteranceBotResponseTypeDef",
    "UtteranceDataSortByTypeDef",
    "UtteranceInputSpecificationTypeDef",
    "UtteranceLevelTestResultItemTypeDef",
    "UtteranceLevelTestResultsTypeDef",
    "UtteranceSpecificationTypeDef",
    "VoiceSettingsTypeDef",
    "WaitAndContinueSpecificationOutputTypeDef",
    "WaitAndContinueSpecificationTypeDef",
    "WaitAndContinueSpecificationUnionTypeDef",
    "WaiterConfigTypeDef",
)

class ActiveContextTypeDef(TypedDict):
    name: str

class AdvancedRecognitionSettingTypeDef(TypedDict):
    audioRecognitionStrategy: NotRequired[Literal["UseSlotValuesAsCustomVocabulary"]]

class ExecutionErrorDetailsTypeDef(TypedDict):
    errorCode: str
    errorMessage: str

class AgentTurnSpecificationTypeDef(TypedDict):
    agentPrompt: str

AggregatedUtterancesFilterTypeDef = TypedDict(
    "AggregatedUtterancesFilterTypeDef",
    {
        "name": Literal["Utterance"],
        "values": Sequence[str],
        "operator": AggregatedUtterancesFilterOperatorType,
    },
)

class AggregatedUtterancesSortByTypeDef(TypedDict):
    attribute: AggregatedUtterancesSortAttributeType
    order: SortOrderType

class AggregatedUtterancesSummaryTypeDef(TypedDict):
    utterance: NotRequired[str]
    hitCount: NotRequired[int]
    missedCount: NotRequired[int]
    utteranceFirstRecordedInAggregationDuration: NotRequired[datetime]
    utteranceLastRecordedInAggregationDuration: NotRequired[datetime]
    containsDataFromDeletedResources: NotRequired[bool]

class AllowedInputTypesTypeDef(TypedDict):
    allowAudioInput: bool
    allowDTMFInput: bool

class AnalyticsBinBySpecificationTypeDef(TypedDict):
    name: AnalyticsBinByNameType
    interval: AnalyticsIntervalType
    order: NotRequired[AnalyticsSortOrderType]

class AnalyticsBinKeyTypeDef(TypedDict):
    name: NotRequired[AnalyticsBinByNameType]
    value: NotRequired[int]

AnalyticsIntentFilterTypeDef = TypedDict(
    "AnalyticsIntentFilterTypeDef",
    {
        "name": AnalyticsIntentFilterNameType,
        "operator": AnalyticsFilterOperatorType,
        "values": Sequence[str],
    },
)

class AnalyticsIntentGroupByKeyTypeDef(TypedDict):
    name: NotRequired[AnalyticsIntentFieldType]
    value: NotRequired[str]

class AnalyticsIntentGroupBySpecificationTypeDef(TypedDict):
    name: AnalyticsIntentFieldType

class AnalyticsIntentMetricResultTypeDef(TypedDict):
    name: NotRequired[AnalyticsIntentMetricNameType]
    statistic: NotRequired[AnalyticsMetricStatisticType]
    value: NotRequired[float]

class AnalyticsIntentMetricTypeDef(TypedDict):
    name: AnalyticsIntentMetricNameType
    statistic: AnalyticsMetricStatisticType
    order: NotRequired[AnalyticsSortOrderType]

class AnalyticsIntentNodeSummaryTypeDef(TypedDict):
    intentName: NotRequired[str]
    intentPath: NotRequired[str]
    intentCount: NotRequired[int]
    intentLevel: NotRequired[int]
    nodeType: NotRequired[AnalyticsNodeTypeType]

AnalyticsIntentStageFilterTypeDef = TypedDict(
    "AnalyticsIntentStageFilterTypeDef",
    {
        "name": AnalyticsIntentStageFilterNameType,
        "operator": AnalyticsFilterOperatorType,
        "values": Sequence[str],
    },
)

class AnalyticsIntentStageGroupByKeyTypeDef(TypedDict):
    name: NotRequired[AnalyticsIntentStageFieldType]
    value: NotRequired[str]

class AnalyticsIntentStageGroupBySpecificationTypeDef(TypedDict):
    name: AnalyticsIntentStageFieldType

class AnalyticsIntentStageMetricResultTypeDef(TypedDict):
    name: NotRequired[AnalyticsIntentStageMetricNameType]
    statistic: NotRequired[AnalyticsMetricStatisticType]
    value: NotRequired[float]

class AnalyticsIntentStageMetricTypeDef(TypedDict):
    name: AnalyticsIntentStageMetricNameType
    statistic: AnalyticsMetricStatisticType
    order: NotRequired[AnalyticsSortOrderType]

AnalyticsPathFilterTypeDef = TypedDict(
    "AnalyticsPathFilterTypeDef",
    {
        "name": AnalyticsCommonFilterNameType,
        "operator": AnalyticsFilterOperatorType,
        "values": Sequence[str],
    },
)
AnalyticsSessionFilterTypeDef = TypedDict(
    "AnalyticsSessionFilterTypeDef",
    {
        "name": AnalyticsSessionFilterNameType,
        "operator": AnalyticsFilterOperatorType,
        "values": Sequence[str],
    },
)

class AnalyticsSessionGroupByKeyTypeDef(TypedDict):
    name: NotRequired[AnalyticsSessionFieldType]
    value: NotRequired[str]

class AnalyticsSessionGroupBySpecificationTypeDef(TypedDict):
    name: AnalyticsSessionFieldType

class AnalyticsSessionMetricResultTypeDef(TypedDict):
    name: NotRequired[AnalyticsSessionMetricNameType]
    statistic: NotRequired[AnalyticsMetricStatisticType]
    value: NotRequired[float]

class AnalyticsSessionMetricTypeDef(TypedDict):
    name: AnalyticsSessionMetricNameType
    statistic: AnalyticsMetricStatisticType
    order: NotRequired[AnalyticsSortOrderType]

class AnalyticsUtteranceAttributeResultTypeDef(TypedDict):
    lastUsedIntent: NotRequired[str]

class AnalyticsUtteranceAttributeTypeDef(TypedDict):
    name: Literal["LastUsedIntent"]

AnalyticsUtteranceFilterTypeDef = TypedDict(
    "AnalyticsUtteranceFilterTypeDef",
    {
        "name": AnalyticsUtteranceFilterNameType,
        "operator": AnalyticsFilterOperatorType,
        "values": Sequence[str],
    },
)

class AnalyticsUtteranceGroupByKeyTypeDef(TypedDict):
    name: NotRequired[AnalyticsUtteranceFieldType]
    value: NotRequired[str]

class AnalyticsUtteranceGroupBySpecificationTypeDef(TypedDict):
    name: AnalyticsUtteranceFieldType

class AnalyticsUtteranceMetricResultTypeDef(TypedDict):
    name: NotRequired[AnalyticsUtteranceMetricNameType]
    statistic: NotRequired[AnalyticsMetricStatisticType]
    value: NotRequired[float]

class AnalyticsUtteranceMetricTypeDef(TypedDict):
    name: AnalyticsUtteranceMetricNameType
    statistic: AnalyticsMetricStatisticType
    order: NotRequired[AnalyticsSortOrderType]

class AssociatedTranscriptFilterTypeDef(TypedDict):
    name: AssociatedTranscriptFilterNameType
    values: Sequence[str]

class AssociatedTranscriptTypeDef(TypedDict):
    transcript: NotRequired[str]

class AudioSpecificationTypeDef(TypedDict):
    maxLengthMs: int
    endTimeoutMs: int

class DTMFSpecificationTypeDef(TypedDict):
    maxLength: int
    endTimeoutMs: int
    deletionCharacter: str
    endCharacter: str

class S3BucketLogDestinationTypeDef(TypedDict):
    s3BucketArn: str
    logPrefix: str
    kmsKeyArn: NotRequired[str]

class NewCustomVocabularyItemTypeDef(TypedDict):
    phrase: str
    weight: NotRequired[int]
    displayAs: NotRequired[str]

class CustomVocabularyItemTypeDef(TypedDict):
    itemId: str
    phrase: str
    weight: NotRequired[int]
    displayAs: NotRequired[str]

class FailedCustomVocabularyItemTypeDef(TypedDict):
    itemId: NotRequired[str]
    errorMessage: NotRequired[str]
    errorCode: NotRequired[ErrorCodeType]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CustomVocabularyEntryIdTypeDef(TypedDict):
    itemId: str

class BedrockGuardrailConfigurationTypeDef(TypedDict):
    identifier: str
    version: str

class BedrockKnowledgeStoreExactResponseFieldsTypeDef(TypedDict):
    answerField: NotRequired[str]

class BotAliasHistoryEventTypeDef(TypedDict):
    botVersion: NotRequired[str]
    startDate: NotRequired[datetime]
    endDate: NotRequired[datetime]

class BotAliasReplicaSummaryTypeDef(TypedDict):
    botAliasId: NotRequired[str]
    botAliasReplicationStatus: NotRequired[BotAliasReplicationStatusType]
    botVersion: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    failureReasons: NotRequired[List[str]]

class BotAliasSummaryTypeDef(TypedDict):
    botAliasId: NotRequired[str]
    botAliasName: NotRequired[str]
    description: NotRequired[str]
    botVersion: NotRequired[str]
    botAliasStatus: NotRequired[BotAliasStatusType]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]

class BotAliasTestExecutionTargetTypeDef(TypedDict):
    botId: str
    botAliasId: str
    localeId: str

class BotExportSpecificationTypeDef(TypedDict):
    botId: str
    botVersion: str

BotFilterTypeDef = TypedDict(
    "BotFilterTypeDef",
    {
        "name": BotFilterNameType,
        "values": Sequence[str],
        "operator": BotFilterOperatorType,
    },
)

class DataPrivacyTypeDef(TypedDict):
    childDirected: bool

class BotLocaleExportSpecificationTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str

BotLocaleFilterTypeDef = TypedDict(
    "BotLocaleFilterTypeDef",
    {
        "name": Literal["BotLocaleName"],
        "values": Sequence[str],
        "operator": BotLocaleFilterOperatorType,
    },
)

class BotLocaleHistoryEventTypeDef(TypedDict):
    event: str
    eventDate: datetime

class VoiceSettingsTypeDef(TypedDict):
    voiceId: str
    engine: NotRequired[VoiceEngineType]

class BotLocaleSortByTypeDef(TypedDict):
    attribute: Literal["BotLocaleName"]
    order: SortOrderType

class BotLocaleSummaryTypeDef(TypedDict):
    localeId: NotRequired[str]
    localeName: NotRequired[str]
    description: NotRequired[str]
    botLocaleStatus: NotRequired[BotLocaleStatusType]
    lastUpdatedDateTime: NotRequired[datetime]
    lastBuildSubmittedDateTime: NotRequired[datetime]

class BotMemberTypeDef(TypedDict):
    botMemberId: str
    botMemberName: str
    botMemberAliasId: str
    botMemberAliasName: str
    botMemberVersion: str

class IntentStatisticsTypeDef(TypedDict):
    discoveredIntentCount: NotRequired[int]

class SlotTypeStatisticsTypeDef(TypedDict):
    discoveredSlotTypeCount: NotRequired[int]

class BotRecommendationSummaryTypeDef(TypedDict):
    botRecommendationStatus: BotRecommendationStatusType
    botRecommendationId: str
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]

class BotReplicaSummaryTypeDef(TypedDict):
    replicaRegion: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    botReplicaStatus: NotRequired[BotReplicaStatusType]
    failureReasons: NotRequired[List[str]]

class BotSortByTypeDef(TypedDict):
    attribute: Literal["BotName"]
    order: SortOrderType

class BotSummaryTypeDef(TypedDict):
    botId: NotRequired[str]
    botName: NotRequired[str]
    description: NotRequired[str]
    botStatus: NotRequired[BotStatusType]
    latestBotVersion: NotRequired[str]
    lastUpdatedDateTime: NotRequired[datetime]
    botType: NotRequired[BotTypeType]

class BotVersionLocaleDetailsTypeDef(TypedDict):
    sourceBotVersion: str

class BotVersionReplicaSortByTypeDef(TypedDict):
    attribute: Literal["BotVersion"]
    order: SortOrderType

class BotVersionReplicaSummaryTypeDef(TypedDict):
    botVersion: NotRequired[str]
    botVersionReplicationStatus: NotRequired[BotVersionReplicationStatusType]
    creationDateTime: NotRequired[datetime]
    failureReasons: NotRequired[List[str]]

class BotVersionSortByTypeDef(TypedDict):
    attribute: Literal["BotVersion"]
    order: SortOrderType

class BotVersionSummaryTypeDef(TypedDict):
    botName: NotRequired[str]
    botVersion: NotRequired[str]
    description: NotRequired[str]
    botStatus: NotRequired[BotStatusType]
    creationDateTime: NotRequired[datetime]

class BuildBotLocaleRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str

class BuiltInIntentSortByTypeDef(TypedDict):
    attribute: Literal["IntentSignature"]
    order: SortOrderType

class BuiltInIntentSummaryTypeDef(TypedDict):
    intentSignature: NotRequired[str]
    description: NotRequired[str]

class BuiltInSlotTypeSortByTypeDef(TypedDict):
    attribute: Literal["SlotTypeSignature"]
    order: SortOrderType

class BuiltInSlotTypeSummaryTypeDef(TypedDict):
    slotTypeSignature: NotRequired[str]
    description: NotRequired[str]

class ButtonTypeDef(TypedDict):
    text: str
    value: str

class CloudWatchLogGroupLogDestinationTypeDef(TypedDict):
    cloudWatchLogGroupArn: str
    logPrefix: str

class LambdaCodeHookTypeDef(TypedDict):
    lambdaARN: str
    codeHookInterfaceVersion: str

class SubSlotTypeCompositionTypeDef(TypedDict):
    name: str
    slotTypeId: str

class ConditionTypeDef(TypedDict):
    expressionString: str

class ConversationLevelIntentClassificationResultItemTypeDef(TypedDict):
    intentName: str
    matchResult: TestResultMatchStatusType

class ConversationLevelResultDetailTypeDef(TypedDict):
    endToEndResult: TestResultMatchStatusType
    speechTranscriptionResult: NotRequired[TestResultMatchStatusType]

class ConversationLevelSlotResolutionResultItemTypeDef(TypedDict):
    intentName: str
    slotName: str
    matchResult: TestResultMatchStatusType

class ConversationLevelTestResultsFilterByTypeDef(TypedDict):
    endToEndResult: NotRequired[TestResultMatchStatusType]

class ConversationLogsDataSourceFilterByOutputTypeDef(TypedDict):
    startTime: datetime
    endTime: datetime
    inputMode: ConversationLogsInputModeFilterType

TimestampTypeDef = Union[datetime, str]

class SentimentAnalysisSettingsTypeDef(TypedDict):
    detectSentiment: bool

class CreateBotReplicaRequestRequestTypeDef(TypedDict):
    botId: str
    replicaRegion: str

class DialogCodeHookSettingsTypeDef(TypedDict):
    enabled: bool

class InputContextTypeDef(TypedDict):
    name: str

class KendraConfigurationTypeDef(TypedDict):
    kendraIndex: str
    queryFilterStringEnabled: NotRequired[bool]
    queryFilterString: NotRequired[str]

class OutputContextTypeDef(TypedDict):
    name: str
    timeToLiveInSeconds: int
    turnsToLive: int

class SampleUtteranceTypeDef(TypedDict):
    utterance: str

class CreateResourcePolicyRequestRequestTypeDef(TypedDict):
    resourceArn: str
    policy: str

class PrincipalTypeDef(TypedDict):
    service: NotRequired[str]
    arn: NotRequired[str]

class MultipleValuesSettingTypeDef(TypedDict):
    allowMultipleValues: NotRequired[bool]

class ObfuscationSettingTypeDef(TypedDict):
    obfuscationSettingType: ObfuscationSettingTypeType

class CustomPayloadTypeDef(TypedDict):
    value: str

class CustomVocabularyExportSpecificationTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str

class CustomVocabularyImportSpecificationTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str

class QnAKendraConfigurationTypeDef(TypedDict):
    kendraIndex: str
    queryFilterStringEnabled: NotRequired[bool]
    queryFilterString: NotRequired[str]
    exactResponse: NotRequired[bool]

class DateRangeFilterOutputTypeDef(TypedDict):
    startDateTime: datetime
    endDateTime: datetime

class DeleteBotAliasRequestRequestTypeDef(TypedDict):
    botAliasId: str
    botId: str
    skipResourceInUseCheck: NotRequired[bool]

class DeleteBotLocaleRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str

class DeleteBotReplicaRequestRequestTypeDef(TypedDict):
    botId: str
    replicaRegion: str

class DeleteBotRequestRequestTypeDef(TypedDict):
    botId: str
    skipResourceInUseCheck: NotRequired[bool]

class DeleteBotVersionRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    skipResourceInUseCheck: NotRequired[bool]

class DeleteCustomVocabularyRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str

class DeleteExportRequestRequestTypeDef(TypedDict):
    exportId: str

class DeleteImportRequestRequestTypeDef(TypedDict):
    importId: str

class DeleteIntentRequestRequestTypeDef(TypedDict):
    intentId: str
    botId: str
    botVersion: str
    localeId: str

class DeleteResourcePolicyRequestRequestTypeDef(TypedDict):
    resourceArn: str
    expectedRevisionId: NotRequired[str]

class DeleteResourcePolicyStatementRequestRequestTypeDef(TypedDict):
    resourceArn: str
    statementId: str
    expectedRevisionId: NotRequired[str]

class DeleteSlotRequestRequestTypeDef(TypedDict):
    slotId: str
    botId: str
    botVersion: str
    localeId: str
    intentId: str

class DeleteSlotTypeRequestRequestTypeDef(TypedDict):
    slotTypeId: str
    botId: str
    botVersion: str
    localeId: str
    skipResourceInUseCheck: NotRequired[bool]

class DeleteTestSetRequestRequestTypeDef(TypedDict):
    testSetId: str

class DeleteUtterancesRequestRequestTypeDef(TypedDict):
    botId: str
    localeId: NotRequired[str]
    sessionId: NotRequired[str]

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class DescribeBotAliasRequestRequestTypeDef(TypedDict):
    botAliasId: str
    botId: str

class ParentBotNetworkTypeDef(TypedDict):
    botId: str
    botVersion: str

class DescribeBotLocaleRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str

class DescribeBotRecommendationRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botRecommendationId: str

class EncryptionSettingTypeDef(TypedDict):
    kmsKeyArn: NotRequired[str]
    botLocaleExportPassword: NotRequired[str]
    associatedTranscriptsPassword: NotRequired[str]

class DescribeBotReplicaRequestRequestTypeDef(TypedDict):
    botId: str
    replicaRegion: str

class DescribeBotRequestRequestTypeDef(TypedDict):
    botId: str

class DescribeBotResourceGenerationRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    generationId: str

class DescribeBotVersionRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str

class DescribeCustomVocabularyMetadataRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str

class DescribeExportRequestRequestTypeDef(TypedDict):
    exportId: str

class DescribeImportRequestRequestTypeDef(TypedDict):
    importId: str

class DescribeIntentRequestRequestTypeDef(TypedDict):
    intentId: str
    botId: str
    botVersion: str
    localeId: str

class SlotPriorityTypeDef(TypedDict):
    priority: int
    slotId: str

class DescribeResourcePolicyRequestRequestTypeDef(TypedDict):
    resourceArn: str

class DescribeSlotRequestRequestTypeDef(TypedDict):
    slotId: str
    botId: str
    botVersion: str
    localeId: str
    intentId: str

class DescribeSlotTypeRequestRequestTypeDef(TypedDict):
    slotTypeId: str
    botId: str
    botVersion: str
    localeId: str

class DescribeTestExecutionRequestRequestTypeDef(TypedDict):
    testExecutionId: str

class DescribeTestSetDiscrepancyReportRequestRequestTypeDef(TypedDict):
    testSetDiscrepancyReportId: str

class DescribeTestSetGenerationRequestRequestTypeDef(TypedDict):
    testSetGenerationId: str

class TestSetStorageLocationTypeDef(TypedDict):
    s3BucketName: str
    s3Path: str
    kmsKeyArn: NotRequired[str]

class DescribeTestSetRequestRequestTypeDef(TypedDict):
    testSetId: str

DialogActionTypeDef = TypedDict(
    "DialogActionTypeDef",
    {
        "type": DialogActionTypeType,
        "slotToElicit": NotRequired[str],
        "suppressNextMessage": NotRequired[bool],
    },
)

class ElicitationCodeHookInvocationSettingTypeDef(TypedDict):
    enableCodeHookInvocation: bool
    invocationLabel: NotRequired[str]

class ExactResponseFieldsTypeDef(TypedDict):
    questionField: str
    answerField: str

ExportFilterTypeDef = TypedDict(
    "ExportFilterTypeDef",
    {
        "name": Literal["ExportResourceType"],
        "values": Sequence[str],
        "operator": ExportFilterOperatorType,
    },
)

class TestSetExportSpecificationTypeDef(TypedDict):
    testSetId: str

class ExportSortByTypeDef(TypedDict):
    attribute: Literal["LastUpdatedDateTime"]
    order: SortOrderType

class GenerateBotElementRequestRequestTypeDef(TypedDict):
    intentId: str
    botId: str
    botVersion: str
    localeId: str

class GenerationSortByTypeDef(TypedDict):
    attribute: GenerationSortByAttributeType
    order: SortOrderType

class GenerationSummaryTypeDef(TypedDict):
    generationId: NotRequired[str]
    generationStatus: NotRequired[GenerationStatusType]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]

class GetTestExecutionArtifactsUrlRequestRequestTypeDef(TypedDict):
    testExecutionId: str

class GrammarSlotTypeSourceTypeDef(TypedDict):
    s3BucketName: str
    s3ObjectKey: str
    kmsKeyArn: NotRequired[str]

ImportFilterTypeDef = TypedDict(
    "ImportFilterTypeDef",
    {
        "name": Literal["ImportResourceType"],
        "values": Sequence[str],
        "operator": ImportFilterOperatorType,
    },
)

class ImportSortByTypeDef(TypedDict):
    attribute: Literal["LastUpdatedDateTime"]
    order: SortOrderType

class ImportSummaryTypeDef(TypedDict):
    importId: NotRequired[str]
    importedResourceId: NotRequired[str]
    importedResourceName: NotRequired[str]
    importStatus: NotRequired[ImportStatusType]
    mergeStrategy: NotRequired[MergeStrategyType]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    importedResourceType: NotRequired[ImportResourceTypeType]

class IntentClassificationTestResultItemCountsTypeDef(TypedDict):
    totalResultCount: int
    intentMatchResultCounts: Dict[TestResultMatchStatusType, int]
    speechTranscriptionResultCounts: NotRequired[Dict[TestResultMatchStatusType, int]]

IntentFilterTypeDef = TypedDict(
    "IntentFilterTypeDef",
    {
        "name": Literal["IntentName"],
        "values": Sequence[str],
        "operator": IntentFilterOperatorType,
    },
)

class IntentSortByTypeDef(TypedDict):
    attribute: IntentSortAttributeType
    order: SortOrderType

class InvokedIntentSampleTypeDef(TypedDict):
    intentName: NotRequired[str]

class ListBotAliasReplicasRequestRequestTypeDef(TypedDict):
    botId: str
    replicaRegion: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListBotAliasesRequestRequestTypeDef(TypedDict):
    botId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListBotRecommendationsRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListBotReplicasRequestRequestTypeDef(TypedDict):
    botId: str

class ListCustomVocabularyItemsRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListRecommendedIntentsRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botRecommendationId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class RecommendedIntentSummaryTypeDef(TypedDict):
    intentId: NotRequired[str]
    intentName: NotRequired[str]
    sampleUtterancesCount: NotRequired[int]

class SessionDataSortByTypeDef(TypedDict):
    name: AnalyticsSessionSortByNameType
    order: AnalyticsSortOrderType

SlotTypeFilterTypeDef = TypedDict(
    "SlotTypeFilterTypeDef",
    {
        "name": SlotTypeFilterNameType,
        "values": Sequence[str],
        "operator": SlotTypeFilterOperatorType,
    },
)

class SlotTypeSortByTypeDef(TypedDict):
    attribute: SlotTypeSortAttributeType
    order: SortOrderType

class SlotTypeSummaryTypeDef(TypedDict):
    slotTypeId: NotRequired[str]
    slotTypeName: NotRequired[str]
    description: NotRequired[str]
    parentSlotTypeSignature: NotRequired[str]
    lastUpdatedDateTime: NotRequired[datetime]
    slotTypeCategory: NotRequired[SlotTypeCategoryType]

SlotFilterTypeDef = TypedDict(
    "SlotFilterTypeDef",
    {
        "name": Literal["SlotName"],
        "values": Sequence[str],
        "operator": SlotFilterOperatorType,
    },
)

class SlotSortByTypeDef(TypedDict):
    attribute: SlotSortAttributeType
    order: SortOrderType

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str

class TestExecutionSortByTypeDef(TypedDict):
    attribute: TestExecutionSortAttributeType
    order: SortOrderType

class ListTestSetRecordsRequestRequestTypeDef(TypedDict):
    testSetId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class TestSetSortByTypeDef(TypedDict):
    attribute: TestSetSortAttributeType
    order: SortOrderType

class UtteranceDataSortByTypeDef(TypedDict):
    name: Literal["UtteranceTimestamp"]
    order: AnalyticsSortOrderType

class PlainTextMessageTypeDef(TypedDict):
    value: str

class SSMLMessageTypeDef(TypedDict):
    value: str

class OverallTestResultItemTypeDef(TypedDict):
    multiTurnConversation: bool
    totalResultCount: int
    endToEndResultCounts: Dict[TestResultMatchStatusType, int]
    speechTranscriptionResultCounts: NotRequired[Dict[TestResultMatchStatusType, int]]

class PathFormatOutputTypeDef(TypedDict):
    objectPrefixes: NotRequired[List[str]]

class PathFormatTypeDef(TypedDict):
    objectPrefixes: NotRequired[Sequence[str]]

class TextInputSpecificationTypeDef(TypedDict):
    startTimeoutMs: int

class RelativeAggregationDurationTypeDef(TypedDict):
    timeDimension: TimeDimensionType
    timeValue: int

class RuntimeHintValueTypeDef(TypedDict):
    phrase: str

class SampleValueTypeDef(TypedDict):
    value: str

class SlotDefaultValueTypeDef(TypedDict):
    defaultValue: str

class SlotResolutionSettingTypeDef(TypedDict):
    slotResolutionStrategy: SlotResolutionStrategyType

class SlotResolutionTestResultItemCountsTypeDef(TypedDict):
    totalResultCount: int
    slotMatchResultCounts: Dict[TestResultMatchStatusType, int]
    speechTranscriptionResultCounts: NotRequired[Dict[TestResultMatchStatusType, int]]

class SlotValueTypeDef(TypedDict):
    interpretedValue: NotRequired[str]

class SlotValueRegexFilterTypeDef(TypedDict):
    pattern: str

class StartBotResourceGenerationRequestRequestTypeDef(TypedDict):
    generationInputPrompt: str
    botId: str
    botVersion: str
    localeId: str

class StopBotRecommendationRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botRecommendationId: str

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tags: Mapping[str, str]

class TestSetIntentDiscrepancyItemTypeDef(TypedDict):
    intentName: str
    errorMessage: str

class TestSetSlotDiscrepancyItemTypeDef(TypedDict):
    intentName: str
    slotName: str
    errorMessage: str

class TestSetDiscrepancyReportBotAliasTargetTypeDef(TypedDict):
    botId: str
    botAliasId: str
    localeId: str

class TestSetImportInputLocationTypeDef(TypedDict):
    s3BucketName: str
    s3Path: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tagKeys: Sequence[str]

class UpdateExportRequestRequestTypeDef(TypedDict):
    exportId: str
    filePassword: NotRequired[str]

class UpdateResourcePolicyRequestRequestTypeDef(TypedDict):
    resourceArn: str
    policy: str
    expectedRevisionId: NotRequired[str]

class UpdateTestSetRequestRequestTypeDef(TypedDict):
    testSetId: str
    testSetName: str
    description: NotRequired[str]

class UserTurnSlotOutputTypeDef(TypedDict):
    value: NotRequired[str]
    values: NotRequired[List[Dict[str, Any]]]
    subSlots: NotRequired[Dict[str, Dict[str, Any]]]

class UtteranceAudioInputSpecificationTypeDef(TypedDict):
    audioFileS3Location: str

class AgentTurnResultTypeDef(TypedDict):
    expectedAgentPrompt: str
    actualAgentPrompt: NotRequired[str]
    errorDetails: NotRequired[ExecutionErrorDetailsTypeDef]
    actualElicitedSlot: NotRequired[str]
    actualIntent: NotRequired[str]

class AnalyticsIntentResultTypeDef(TypedDict):
    binKeys: NotRequired[List[AnalyticsBinKeyTypeDef]]
    groupByKeys: NotRequired[List[AnalyticsIntentGroupByKeyTypeDef]]
    metricsResults: NotRequired[List[AnalyticsIntentMetricResultTypeDef]]

class AnalyticsIntentStageResultTypeDef(TypedDict):
    binKeys: NotRequired[List[AnalyticsBinKeyTypeDef]]
    groupByKeys: NotRequired[List[AnalyticsIntentStageGroupByKeyTypeDef]]
    metricsResults: NotRequired[List[AnalyticsIntentStageMetricResultTypeDef]]

class AnalyticsSessionResultTypeDef(TypedDict):
    binKeys: NotRequired[List[AnalyticsBinKeyTypeDef]]
    groupByKeys: NotRequired[List[AnalyticsSessionGroupByKeyTypeDef]]
    metricsResults: NotRequired[List[AnalyticsSessionMetricResultTypeDef]]

class AnalyticsUtteranceResultTypeDef(TypedDict):
    binKeys: NotRequired[List[AnalyticsBinKeyTypeDef]]
    groupByKeys: NotRequired[List[AnalyticsUtteranceGroupByKeyTypeDef]]
    metricsResults: NotRequired[List[AnalyticsUtteranceMetricResultTypeDef]]
    attributeResults: NotRequired[List[AnalyticsUtteranceAttributeResultTypeDef]]

class SearchAssociatedTranscriptsRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botRecommendationId: str
    filters: Sequence[AssociatedTranscriptFilterTypeDef]
    searchOrder: NotRequired[SearchOrderType]
    maxResults: NotRequired[int]
    nextIndex: NotRequired[int]

class AudioAndDTMFInputSpecificationTypeDef(TypedDict):
    startTimeoutMs: int
    audioSpecification: NotRequired[AudioSpecificationTypeDef]
    dtmfSpecification: NotRequired[DTMFSpecificationTypeDef]

class AudioLogDestinationTypeDef(TypedDict):
    s3Bucket: S3BucketLogDestinationTypeDef

class BatchCreateCustomVocabularyItemRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    customVocabularyItemList: Sequence[NewCustomVocabularyItemTypeDef]

class BatchUpdateCustomVocabularyItemRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    customVocabularyItemList: Sequence[CustomVocabularyItemTypeDef]

class BatchCreateCustomVocabularyItemResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    errors: List[FailedCustomVocabularyItemTypeDef]
    resources: List[CustomVocabularyItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeleteCustomVocabularyItemResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    errors: List[FailedCustomVocabularyItemTypeDef]
    resources: List[CustomVocabularyItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchUpdateCustomVocabularyItemResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    errors: List[FailedCustomVocabularyItemTypeDef]
    resources: List[CustomVocabularyItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BuildBotLocaleResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botLocaleStatus: BotLocaleStatusType
    lastBuildSubmittedDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBotReplicaResponseTypeDef(TypedDict):
    botId: str
    replicaRegion: str
    sourceRegion: str
    creationDateTime: datetime
    botReplicaStatus: BotReplicaStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateResourcePolicyResponseTypeDef(TypedDict):
    resourceArn: str
    revisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateResourcePolicyStatementResponseTypeDef(TypedDict):
    resourceArn: str
    revisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateUploadUrlResponseTypeDef(TypedDict):
    importId: str
    uploadUrl: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBotAliasResponseTypeDef(TypedDict):
    botAliasId: str
    botId: str
    botAliasStatus: BotAliasStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBotLocaleResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botLocaleStatus: BotLocaleStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBotReplicaResponseTypeDef(TypedDict):
    botId: str
    replicaRegion: str
    botReplicaStatus: BotReplicaStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBotResponseTypeDef(TypedDict):
    botId: str
    botStatus: BotStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBotVersionResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    botStatus: BotStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteCustomVocabularyResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    customVocabularyStatus: CustomVocabularyStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteExportResponseTypeDef(TypedDict):
    exportId: str
    exportStatus: ExportStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteImportResponseTypeDef(TypedDict):
    importId: str
    importStatus: ImportStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteResourcePolicyResponseTypeDef(TypedDict):
    resourceArn: str
    revisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteResourcePolicyStatementResponseTypeDef(TypedDict):
    resourceArn: str
    revisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBotReplicaResponseTypeDef(TypedDict):
    botId: str
    replicaRegion: str
    sourceRegion: str
    creationDateTime: datetime
    botReplicaStatus: BotReplicaStatusType
    failureReasons: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBotResourceGenerationResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    generationId: str
    failureReasons: List[str]
    generationStatus: GenerationStatusType
    generationInputPrompt: str
    generatedBotLocaleUrl: str
    creationDateTime: datetime
    modelArn: str
    lastUpdatedDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCustomVocabularyMetadataResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    customVocabularyStatus: CustomVocabularyStatusType
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeResourcePolicyResponseTypeDef(TypedDict):
    resourceArn: str
    policy: str
    revisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetTestExecutionArtifactsUrlResponseTypeDef(TypedDict):
    testExecutionId: str
    downloadArtifactsUrl: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListCustomVocabularyItemsResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    customVocabularyItems: List[CustomVocabularyItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListIntentPathsResponseTypeDef(TypedDict):
    nodeSummaries: List[AnalyticsIntentNodeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class SearchAssociatedTranscriptsResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botRecommendationId: str
    nextIndex: int
    associatedTranscripts: List[AssociatedTranscriptTypeDef]
    totalResults: int
    ResponseMetadata: ResponseMetadataTypeDef

class StartBotResourceGenerationResponseTypeDef(TypedDict):
    generationInputPrompt: str
    generationId: str
    botId: str
    botVersion: str
    localeId: str
    generationStatus: GenerationStatusType
    creationDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class StopBotRecommendationResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botRecommendationStatus: BotRecommendationStatusType
    botRecommendationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateResourcePolicyResponseTypeDef(TypedDict):
    resourceArn: str
    revisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeleteCustomVocabularyItemRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    customVocabularyItemList: Sequence[CustomVocabularyEntryIdTypeDef]

class BedrockModelSpecificationTypeDef(TypedDict):
    modelArn: str
    guardrail: NotRequired[BedrockGuardrailConfigurationTypeDef]
    traceStatus: NotRequired[BedrockTraceStatusType]
    customPrompt: NotRequired[str]

class BedrockKnowledgeStoreConfigurationTypeDef(TypedDict):
    bedrockKnowledgeBaseArn: str
    exactResponse: NotRequired[bool]
    exactResponseFields: NotRequired[BedrockKnowledgeStoreExactResponseFieldsTypeDef]

class ListBotAliasReplicasResponseTypeDef(TypedDict):
    botId: str
    sourceRegion: str
    replicaRegion: str
    botAliasReplicaSummaries: List[BotAliasReplicaSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBotAliasesResponseTypeDef(TypedDict):
    botAliasSummaries: List[BotAliasSummaryTypeDef]
    botId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class TestExecutionTargetTypeDef(TypedDict):
    botAliasTarget: NotRequired[BotAliasTestExecutionTargetTypeDef]

class BotImportSpecificationOutputTypeDef(TypedDict):
    botName: str
    roleArn: str
    dataPrivacy: DataPrivacyTypeDef
    idleSessionTTLInSeconds: NotRequired[int]
    botTags: NotRequired[Dict[str, str]]
    testBotAliasTags: NotRequired[Dict[str, str]]

class BotImportSpecificationTypeDef(TypedDict):
    botName: str
    roleArn: str
    dataPrivacy: DataPrivacyTypeDef
    idleSessionTTLInSeconds: NotRequired[int]
    botTags: NotRequired[Mapping[str, str]]
    testBotAliasTags: NotRequired[Mapping[str, str]]

class BotLocaleImportSpecificationTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    nluIntentConfidenceThreshold: NotRequired[float]
    voiceSettings: NotRequired[VoiceSettingsTypeDef]

class ListBotLocalesRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    sortBy: NotRequired[BotLocaleSortByTypeDef]
    filters: NotRequired[Sequence[BotLocaleFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListBotLocalesResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    botLocaleSummaries: List[BotLocaleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateBotRequestRequestTypeDef(TypedDict):
    botName: str
    roleArn: str
    dataPrivacy: DataPrivacyTypeDef
    idleSessionTTLInSeconds: int
    description: NotRequired[str]
    botTags: NotRequired[Mapping[str, str]]
    testBotAliasTags: NotRequired[Mapping[str, str]]
    botType: NotRequired[BotTypeType]
    botMembers: NotRequired[Sequence[BotMemberTypeDef]]

class CreateBotResponseTypeDef(TypedDict):
    botId: str
    botName: str
    description: str
    roleArn: str
    dataPrivacy: DataPrivacyTypeDef
    idleSessionTTLInSeconds: int
    botStatus: BotStatusType
    creationDateTime: datetime
    botTags: Dict[str, str]
    testBotAliasTags: Dict[str, str]
    botType: BotTypeType
    botMembers: List[BotMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBotResponseTypeDef(TypedDict):
    botId: str
    botName: str
    description: str
    roleArn: str
    dataPrivacy: DataPrivacyTypeDef
    idleSessionTTLInSeconds: int
    botStatus: BotStatusType
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    botType: BotTypeType
    botMembers: List[BotMemberTypeDef]
    failureReasons: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBotRequestRequestTypeDef(TypedDict):
    botId: str
    botName: str
    roleArn: str
    dataPrivacy: DataPrivacyTypeDef
    idleSessionTTLInSeconds: int
    description: NotRequired[str]
    botType: NotRequired[BotTypeType]
    botMembers: NotRequired[Sequence[BotMemberTypeDef]]

class UpdateBotResponseTypeDef(TypedDict):
    botId: str
    botName: str
    description: str
    roleArn: str
    dataPrivacy: DataPrivacyTypeDef
    idleSessionTTLInSeconds: int
    botStatus: BotStatusType
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    botType: BotTypeType
    botMembers: List[BotMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BotRecommendationResultStatisticsTypeDef(TypedDict):
    intents: NotRequired[IntentStatisticsTypeDef]
    slotTypes: NotRequired[SlotTypeStatisticsTypeDef]

class ListBotRecommendationsResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botRecommendationSummaries: List[BotRecommendationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBotReplicasResponseTypeDef(TypedDict):
    botId: str
    sourceRegion: str
    botReplicaSummaries: List[BotReplicaSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListBotsRequestRequestTypeDef(TypedDict):
    sortBy: NotRequired[BotSortByTypeDef]
    filters: NotRequired[Sequence[BotFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListBotsResponseTypeDef(TypedDict):
    botSummaries: List[BotSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateBotVersionRequestRequestTypeDef(TypedDict):
    botId: str
    botVersionLocaleSpecification: Mapping[str, BotVersionLocaleDetailsTypeDef]
    description: NotRequired[str]

class CreateBotVersionResponseTypeDef(TypedDict):
    botId: str
    description: str
    botVersion: str
    botVersionLocaleSpecification: Dict[str, BotVersionLocaleDetailsTypeDef]
    botStatus: BotStatusType
    creationDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListBotVersionReplicasRequestRequestTypeDef(TypedDict):
    botId: str
    replicaRegion: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[BotVersionReplicaSortByTypeDef]

class ListBotVersionReplicasResponseTypeDef(TypedDict):
    botId: str
    sourceRegion: str
    replicaRegion: str
    botVersionReplicaSummaries: List[BotVersionReplicaSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBotVersionsRequestRequestTypeDef(TypedDict):
    botId: str
    sortBy: NotRequired[BotVersionSortByTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListBotVersionsResponseTypeDef(TypedDict):
    botId: str
    botVersionSummaries: List[BotVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBuiltInIntentsRequestRequestTypeDef(TypedDict):
    localeId: str
    sortBy: NotRequired[BuiltInIntentSortByTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListBuiltInIntentsResponseTypeDef(TypedDict):
    builtInIntentSummaries: List[BuiltInIntentSummaryTypeDef]
    localeId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBuiltInSlotTypesRequestRequestTypeDef(TypedDict):
    localeId: str
    sortBy: NotRequired[BuiltInSlotTypeSortByTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListBuiltInSlotTypesResponseTypeDef(TypedDict):
    builtInSlotTypeSummaries: List[BuiltInSlotTypeSummaryTypeDef]
    localeId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ImageResponseCardOutputTypeDef(TypedDict):
    title: str
    subtitle: NotRequired[str]
    imageUrl: NotRequired[str]
    buttons: NotRequired[List[ButtonTypeDef]]

class ImageResponseCardTypeDef(TypedDict):
    title: str
    subtitle: NotRequired[str]
    imageUrl: NotRequired[str]
    buttons: NotRequired[Sequence[ButtonTypeDef]]

class TextLogDestinationTypeDef(TypedDict):
    cloudWatch: CloudWatchLogGroupLogDestinationTypeDef

class CodeHookSpecificationTypeDef(TypedDict):
    lambdaCodeHook: LambdaCodeHookTypeDef

class CompositeSlotTypeSettingOutputTypeDef(TypedDict):
    subSlots: NotRequired[List[SubSlotTypeCompositionTypeDef]]

class CompositeSlotTypeSettingTypeDef(TypedDict):
    subSlots: NotRequired[Sequence[SubSlotTypeCompositionTypeDef]]

class ConversationLevelTestResultItemTypeDef(TypedDict):
    conversationId: str
    endToEndResult: TestResultMatchStatusType
    intentClassificationResults: List[ConversationLevelIntentClassificationResultItemTypeDef]
    slotResolutionResults: List[ConversationLevelSlotResolutionResultItemTypeDef]
    speechTranscriptionResult: NotRequired[TestResultMatchStatusType]

class TestExecutionResultFilterByTypeDef(TypedDict):
    resultTypeFilter: TestResultTypeFilterType
    conversationLevelTestResultsFilterBy: NotRequired[ConversationLevelTestResultsFilterByTypeDef]

ConversationLogsDataSourceOutputTypeDef = TypedDict(
    "ConversationLogsDataSourceOutputTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "filter": ConversationLogsDataSourceFilterByOutputTypeDef,
    },
)

class ConversationLogsDataSourceFilterByTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    inputMode: ConversationLogsInputModeFilterType

class DateRangeFilterTypeDef(TypedDict):
    startDateTime: TimestampTypeDef
    endDateTime: TimestampTypeDef

class ListIntentMetricsRequestRequestTypeDef(TypedDict):
    botId: str
    startDateTime: TimestampTypeDef
    endDateTime: TimestampTypeDef
    metrics: Sequence[AnalyticsIntentMetricTypeDef]
    binBy: NotRequired[Sequence[AnalyticsBinBySpecificationTypeDef]]
    groupBy: NotRequired[Sequence[AnalyticsIntentGroupBySpecificationTypeDef]]
    filters: NotRequired[Sequence[AnalyticsIntentFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListIntentPathsRequestRequestTypeDef(TypedDict):
    botId: str
    startDateTime: TimestampTypeDef
    endDateTime: TimestampTypeDef
    intentPath: str
    filters: NotRequired[Sequence[AnalyticsPathFilterTypeDef]]

class ListIntentStageMetricsRequestRequestTypeDef(TypedDict):
    botId: str
    startDateTime: TimestampTypeDef
    endDateTime: TimestampTypeDef
    metrics: Sequence[AnalyticsIntentStageMetricTypeDef]
    binBy: NotRequired[Sequence[AnalyticsBinBySpecificationTypeDef]]
    groupBy: NotRequired[Sequence[AnalyticsIntentStageGroupBySpecificationTypeDef]]
    filters: NotRequired[Sequence[AnalyticsIntentStageFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListSessionMetricsRequestRequestTypeDef(TypedDict):
    botId: str
    startDateTime: TimestampTypeDef
    endDateTime: TimestampTypeDef
    metrics: Sequence[AnalyticsSessionMetricTypeDef]
    binBy: NotRequired[Sequence[AnalyticsBinBySpecificationTypeDef]]
    groupBy: NotRequired[Sequence[AnalyticsSessionGroupBySpecificationTypeDef]]
    filters: NotRequired[Sequence[AnalyticsSessionFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListUtteranceMetricsRequestRequestTypeDef(TypedDict):
    botId: str
    startDateTime: TimestampTypeDef
    endDateTime: TimestampTypeDef
    metrics: Sequence[AnalyticsUtteranceMetricTypeDef]
    binBy: NotRequired[Sequence[AnalyticsBinBySpecificationTypeDef]]
    groupBy: NotRequired[Sequence[AnalyticsUtteranceGroupBySpecificationTypeDef]]
    attributes: NotRequired[Sequence[AnalyticsUtteranceAttributeTypeDef]]
    filters: NotRequired[Sequence[AnalyticsUtteranceFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class IntentSummaryTypeDef(TypedDict):
    intentId: NotRequired[str]
    intentName: NotRequired[str]
    description: NotRequired[str]
    parentIntentSignature: NotRequired[str]
    inputContexts: NotRequired[List[InputContextTypeDef]]
    outputContexts: NotRequired[List[OutputContextTypeDef]]
    lastUpdatedDateTime: NotRequired[datetime]

class GenerateBotElementResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    intentId: str
    sampleUtterances: List[SampleUtteranceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateResourcePolicyStatementRequestRequestTypeDef(TypedDict):
    resourceArn: str
    statementId: str
    effect: EffectType
    principal: Sequence[PrincipalTypeDef]
    action: Sequence[str]
    condition: NotRequired[Mapping[str, Mapping[str, str]]]
    expectedRevisionId: NotRequired[str]

class LexTranscriptFilterOutputTypeDef(TypedDict):
    dateRangeFilter: NotRequired[DateRangeFilterOutputTypeDef]

class DescribeBotAliasRequestBotAliasAvailableWaitTypeDef(TypedDict):
    botAliasId: str
    botId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeBotLocaleRequestBotLocaleBuiltWaitTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeBotLocaleRequestBotLocaleCreatedWaitTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeBotLocaleRequestBotLocaleExpressTestingAvailableWaitTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeBotRequestBotAvailableWaitTypeDef(TypedDict):
    botId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeBotVersionRequestBotVersionAvailableWaitTypeDef(TypedDict):
    botId: str
    botVersion: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeExportRequestBotExportCompletedWaitTypeDef(TypedDict):
    exportId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeImportRequestBotImportCompletedWaitTypeDef(TypedDict):
    importId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeBotVersionResponseTypeDef(TypedDict):
    botId: str
    botName: str
    botVersion: str
    description: str
    roleArn: str
    dataPrivacy: DataPrivacyTypeDef
    idleSessionTTLInSeconds: int
    botStatus: BotStatusType
    failureReasons: List[str]
    creationDateTime: datetime
    parentBotNetworks: List[ParentBotNetworkTypeDef]
    botType: BotTypeType
    botMembers: List[BotMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBotRecommendationRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botRecommendationId: str
    encryptionSetting: EncryptionSettingTypeDef

class DescribeTestSetResponseTypeDef(TypedDict):
    testSetId: str
    testSetName: str
    description: str
    modality: TestSetModalityType
    status: TestSetStatusType
    roleArn: str
    numTurns: int
    storageLocation: TestSetStorageLocationTypeDef
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class TestSetSummaryTypeDef(TypedDict):
    testSetId: NotRequired[str]
    testSetName: NotRequired[str]
    description: NotRequired[str]
    modality: NotRequired[TestSetModalityType]
    status: NotRequired[TestSetStatusType]
    roleArn: NotRequired[str]
    numTurns: NotRequired[int]
    storageLocation: NotRequired[TestSetStorageLocationTypeDef]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]

class UpdateTestSetResponseTypeDef(TypedDict):
    testSetId: str
    testSetName: str
    description: str
    modality: TestSetModalityType
    status: TestSetStatusType
    roleArn: str
    numTurns: int
    storageLocation: TestSetStorageLocationTypeDef
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class OpensearchConfigurationOutputTypeDef(TypedDict):
    domainEndpoint: str
    indexName: str
    exactResponse: NotRequired[bool]
    exactResponseFields: NotRequired[ExactResponseFieldsTypeDef]
    includeFields: NotRequired[List[str]]

class OpensearchConfigurationTypeDef(TypedDict):
    domainEndpoint: str
    indexName: str
    exactResponse: NotRequired[bool]
    exactResponseFields: NotRequired[ExactResponseFieldsTypeDef]
    includeFields: NotRequired[Sequence[str]]

class ExportResourceSpecificationTypeDef(TypedDict):
    botExportSpecification: NotRequired[BotExportSpecificationTypeDef]
    botLocaleExportSpecification: NotRequired[BotLocaleExportSpecificationTypeDef]
    customVocabularyExportSpecification: NotRequired[CustomVocabularyExportSpecificationTypeDef]
    testSetExportSpecification: NotRequired[TestSetExportSpecificationTypeDef]

class ListExportsRequestRequestTypeDef(TypedDict):
    botId: NotRequired[str]
    botVersion: NotRequired[str]
    sortBy: NotRequired[ExportSortByTypeDef]
    filters: NotRequired[Sequence[ExportFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    localeId: NotRequired[str]

class ListBotResourceGenerationsRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    sortBy: NotRequired[GenerationSortByTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListBotResourceGenerationsResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    generationSummaries: List[GenerationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GrammarSlotTypeSettingTypeDef(TypedDict):
    source: NotRequired[GrammarSlotTypeSourceTypeDef]

class ListImportsRequestRequestTypeDef(TypedDict):
    botId: NotRequired[str]
    botVersion: NotRequired[str]
    sortBy: NotRequired[ImportSortByTypeDef]
    filters: NotRequired[Sequence[ImportFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    localeId: NotRequired[str]

class ListImportsResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    importSummaries: List[ImportSummaryTypeDef]
    localeId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class IntentClassificationTestResultItemTypeDef(TypedDict):
    intentName: str
    multiTurnConversation: bool
    resultCounts: IntentClassificationTestResultItemCountsTypeDef

class ListIntentsRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    sortBy: NotRequired[IntentSortByTypeDef]
    filters: NotRequired[Sequence[IntentFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class SessionSpecificationTypeDef(TypedDict):
    botAliasId: NotRequired[str]
    botVersion: NotRequired[str]
    localeId: NotRequired[str]
    channel: NotRequired[str]
    sessionId: NotRequired[str]
    conversationStartTime: NotRequired[datetime]
    conversationEndTime: NotRequired[datetime]
    conversationDurationSeconds: NotRequired[int]
    conversationEndState: NotRequired[ConversationEndStateType]
    mode: NotRequired[AnalyticsModalityType]
    numberOfTurns: NotRequired[int]
    invokedIntentSamples: NotRequired[List[InvokedIntentSampleTypeDef]]
    originatingRequestId: NotRequired[str]

class ListRecommendedIntentsResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botRecommendationId: str
    summaryList: List[RecommendedIntentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSessionAnalyticsDataRequestRequestTypeDef(TypedDict):
    botId: str
    startDateTime: TimestampTypeDef
    endDateTime: TimestampTypeDef
    sortBy: NotRequired[SessionDataSortByTypeDef]
    filters: NotRequired[Sequence[AnalyticsSessionFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListSlotTypesRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    sortBy: NotRequired[SlotTypeSortByTypeDef]
    filters: NotRequired[Sequence[SlotTypeFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListSlotTypesResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    slotTypeSummaries: List[SlotTypeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSlotsRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    intentId: str
    sortBy: NotRequired[SlotSortByTypeDef]
    filters: NotRequired[Sequence[SlotFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTestExecutionsRequestRequestTypeDef(TypedDict):
    sortBy: NotRequired[TestExecutionSortByTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTestSetsRequestRequestTypeDef(TypedDict):
    sortBy: NotRequired[TestSetSortByTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListUtteranceAnalyticsDataRequestRequestTypeDef(TypedDict):
    botId: str
    startDateTime: TimestampTypeDef
    endDateTime: TimestampTypeDef
    sortBy: NotRequired[UtteranceDataSortByTypeDef]
    filters: NotRequired[Sequence[AnalyticsUtteranceFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class OverallTestResultsTypeDef(TypedDict):
    items: List[OverallTestResultItemTypeDef]

PathFormatUnionTypeDef = Union[PathFormatTypeDef, PathFormatOutputTypeDef]

class UtteranceAggregationDurationTypeDef(TypedDict):
    relativeAggregationDuration: RelativeAggregationDurationTypeDef

class RuntimeHintDetailsTypeDef(TypedDict):
    runtimeHintValues: NotRequired[List[RuntimeHintValueTypeDef]]
    subSlotHints: NotRequired[Dict[str, Dict[str, Any]]]

class SlotTypeValueOutputTypeDef(TypedDict):
    sampleValue: NotRequired[SampleValueTypeDef]
    synonyms: NotRequired[List[SampleValueTypeDef]]

class SlotTypeValueTypeDef(TypedDict):
    sampleValue: NotRequired[SampleValueTypeDef]
    synonyms: NotRequired[Sequence[SampleValueTypeDef]]

class SlotDefaultValueSpecificationOutputTypeDef(TypedDict):
    defaultValueList: List[SlotDefaultValueTypeDef]

class SlotDefaultValueSpecificationTypeDef(TypedDict):
    defaultValueList: Sequence[SlotDefaultValueTypeDef]

class SlotResolutionTestResultItemTypeDef(TypedDict):
    slotName: str
    resultCounts: SlotResolutionTestResultItemCountsTypeDef

class SlotValueOverrideOutputTypeDef(TypedDict):
    shape: NotRequired[SlotShapeType]
    value: NotRequired[SlotValueTypeDef]
    values: NotRequired[List[Dict[str, Any]]]

class SlotValueOverrideTypeDef(TypedDict):
    shape: NotRequired[SlotShapeType]
    value: NotRequired[SlotValueTypeDef]
    values: NotRequired[Sequence[Mapping[str, Any]]]

class SlotValueSelectionSettingTypeDef(TypedDict):
    resolutionStrategy: SlotValueResolutionStrategyType
    regexFilter: NotRequired[SlotValueRegexFilterTypeDef]
    advancedRecognitionSetting: NotRequired[AdvancedRecognitionSettingTypeDef]

class TestSetDiscrepancyErrorsTypeDef(TypedDict):
    intentDiscrepancies: List[TestSetIntentDiscrepancyItemTypeDef]
    slotDiscrepancies: List[TestSetSlotDiscrepancyItemTypeDef]

class TestSetDiscrepancyReportResourceTargetTypeDef(TypedDict):
    botAliasTarget: NotRequired[TestSetDiscrepancyReportBotAliasTargetTypeDef]

class TestSetImportResourceSpecificationOutputTypeDef(TypedDict):
    testSetName: str
    roleArn: str
    storageLocation: TestSetStorageLocationTypeDef
    importInputLocation: TestSetImportInputLocationTypeDef
    modality: TestSetModalityType
    description: NotRequired[str]
    testSetTags: NotRequired[Dict[str, str]]

class TestSetImportResourceSpecificationTypeDef(TypedDict):
    testSetName: str
    roleArn: str
    storageLocation: TestSetStorageLocationTypeDef
    importInputLocation: TestSetImportInputLocationTypeDef
    modality: TestSetModalityType
    description: NotRequired[str]
    testSetTags: NotRequired[Mapping[str, str]]

class UserTurnIntentOutputTypeDef(TypedDict):
    name: str
    slots: NotRequired[Dict[str, UserTurnSlotOutputTypeDef]]

class UtteranceInputSpecificationTypeDef(TypedDict):
    textInput: NotRequired[str]
    audioInput: NotRequired[UtteranceAudioInputSpecificationTypeDef]

class ListIntentMetricsResponseTypeDef(TypedDict):
    botId: str
    results: List[AnalyticsIntentResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListIntentStageMetricsResponseTypeDef(TypedDict):
    botId: str
    results: List[AnalyticsIntentStageResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSessionMetricsResponseTypeDef(TypedDict):
    botId: str
    results: List[AnalyticsSessionResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListUtteranceMetricsResponseTypeDef(TypedDict):
    botId: str
    results: List[AnalyticsUtteranceResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PromptAttemptSpecificationTypeDef(TypedDict):
    allowedInputTypes: AllowedInputTypesTypeDef
    allowInterrupt: NotRequired[bool]
    audioAndDTMFInputSpecification: NotRequired[AudioAndDTMFInputSpecificationTypeDef]
    textInputSpecification: NotRequired[TextInputSpecificationTypeDef]

class AudioLogSettingTypeDef(TypedDict):
    enabled: bool
    destination: AudioLogDestinationTypeDef
    selectiveLoggingEnabled: NotRequired[bool]

class DescriptiveBotBuilderSpecificationTypeDef(TypedDict):
    enabled: bool
    bedrockModelSpecification: NotRequired[BedrockModelSpecificationTypeDef]

class SampleUtteranceGenerationSpecificationTypeDef(TypedDict):
    enabled: bool
    bedrockModelSpecification: NotRequired[BedrockModelSpecificationTypeDef]

class SlotResolutionImprovementSpecificationTypeDef(TypedDict):
    enabled: bool
    bedrockModelSpecification: NotRequired[BedrockModelSpecificationTypeDef]

class DescribeTestExecutionResponseTypeDef(TypedDict):
    testExecutionId: str
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    testExecutionStatus: TestExecutionStatusType
    testSetId: str
    testSetName: str
    target: TestExecutionTargetTypeDef
    apiMode: TestExecutionApiModeType
    testExecutionModality: TestExecutionModalityType
    failureReasons: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartTestExecutionRequestRequestTypeDef(TypedDict):
    testSetId: str
    target: TestExecutionTargetTypeDef
    apiMode: TestExecutionApiModeType
    testExecutionModality: NotRequired[TestExecutionModalityType]

class StartTestExecutionResponseTypeDef(TypedDict):
    testExecutionId: str
    creationDateTime: datetime
    testSetId: str
    target: TestExecutionTargetTypeDef
    apiMode: TestExecutionApiModeType
    testExecutionModality: TestExecutionModalityType
    ResponseMetadata: ResponseMetadataTypeDef

class TestExecutionSummaryTypeDef(TypedDict):
    testExecutionId: NotRequired[str]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]
    testExecutionStatus: NotRequired[TestExecutionStatusType]
    testSetId: NotRequired[str]
    testSetName: NotRequired[str]
    target: NotRequired[TestExecutionTargetTypeDef]
    apiMode: NotRequired[TestExecutionApiModeType]
    testExecutionModality: NotRequired[TestExecutionModalityType]

BotImportSpecificationUnionTypeDef = Union[
    BotImportSpecificationTypeDef, BotImportSpecificationOutputTypeDef
]

class BotRecommendationResultsTypeDef(TypedDict):
    botLocaleExportUrl: NotRequired[str]
    associatedTranscriptsUrl: NotRequired[str]
    statistics: NotRequired[BotRecommendationResultStatisticsTypeDef]

class MessageOutputTypeDef(TypedDict):
    plainTextMessage: NotRequired[PlainTextMessageTypeDef]
    customPayload: NotRequired[CustomPayloadTypeDef]
    ssmlMessage: NotRequired[SSMLMessageTypeDef]
    imageResponseCard: NotRequired[ImageResponseCardOutputTypeDef]

class UtteranceBotResponseTypeDef(TypedDict):
    content: NotRequired[str]
    contentType: NotRequired[UtteranceContentTypeType]
    imageResponseCard: NotRequired[ImageResponseCardOutputTypeDef]

ImageResponseCardUnionTypeDef = Union[ImageResponseCardTypeDef, ImageResponseCardOutputTypeDef]

class TextLogSettingTypeDef(TypedDict):
    enabled: bool
    destination: TextLogDestinationTypeDef
    selectiveLoggingEnabled: NotRequired[bool]

class BotAliasLocaleSettingsTypeDef(TypedDict):
    enabled: bool
    codeHookSpecification: NotRequired[CodeHookSpecificationTypeDef]

class ConversationLevelTestResultsTypeDef(TypedDict):
    items: List[ConversationLevelTestResultItemTypeDef]

class ListTestExecutionResultItemsRequestRequestTypeDef(TypedDict):
    testExecutionId: str
    resultFilterBy: TestExecutionResultFilterByTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class TestSetGenerationDataSourceOutputTypeDef(TypedDict):
    conversationLogsDataSource: NotRequired[ConversationLogsDataSourceOutputTypeDef]

ConversationLogsDataSourceFilterByUnionTypeDef = Union[
    ConversationLogsDataSourceFilterByTypeDef, ConversationLogsDataSourceFilterByOutputTypeDef
]
DateRangeFilterUnionTypeDef = Union[DateRangeFilterTypeDef, DateRangeFilterOutputTypeDef]

class ListIntentsResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    intentSummaries: List[IntentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class TranscriptFilterOutputTypeDef(TypedDict):
    lexTranscriptFilter: NotRequired[LexTranscriptFilterOutputTypeDef]

class ListTestSetsResponseTypeDef(TypedDict):
    testSets: List[TestSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DataSourceConfigurationOutputTypeDef(TypedDict):
    opensearchConfiguration: NotRequired[OpensearchConfigurationOutputTypeDef]
    kendraConfiguration: NotRequired[QnAKendraConfigurationTypeDef]
    bedrockKnowledgeStoreConfiguration: NotRequired[BedrockKnowledgeStoreConfigurationTypeDef]

OpensearchConfigurationUnionTypeDef = Union[
    OpensearchConfigurationTypeDef, OpensearchConfigurationOutputTypeDef
]

class CreateExportRequestRequestTypeDef(TypedDict):
    resourceSpecification: ExportResourceSpecificationTypeDef
    fileFormat: ImportExportFileFormatType
    filePassword: NotRequired[str]

class CreateExportResponseTypeDef(TypedDict):
    exportId: str
    resourceSpecification: ExportResourceSpecificationTypeDef
    fileFormat: ImportExportFileFormatType
    exportStatus: ExportStatusType
    creationDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeExportResponseTypeDef(TypedDict):
    exportId: str
    resourceSpecification: ExportResourceSpecificationTypeDef
    fileFormat: ImportExportFileFormatType
    exportStatus: ExportStatusType
    failureReasons: List[str]
    downloadUrl: str
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ExportSummaryTypeDef(TypedDict):
    exportId: NotRequired[str]
    resourceSpecification: NotRequired[ExportResourceSpecificationTypeDef]
    fileFormat: NotRequired[ImportExportFileFormatType]
    exportStatus: NotRequired[ExportStatusType]
    creationDateTime: NotRequired[datetime]
    lastUpdatedDateTime: NotRequired[datetime]

class UpdateExportResponseTypeDef(TypedDict):
    exportId: str
    resourceSpecification: ExportResourceSpecificationTypeDef
    fileFormat: ImportExportFileFormatType
    exportStatus: ExportStatusType
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ExternalSourceSettingTypeDef(TypedDict):
    grammarSlotTypeSetting: NotRequired[GrammarSlotTypeSettingTypeDef]

class IntentClassificationTestResultsTypeDef(TypedDict):
    items: List[IntentClassificationTestResultItemTypeDef]

class ListSessionAnalyticsDataResponseTypeDef(TypedDict):
    botId: str
    sessions: List[SessionSpecificationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAggregatedUtterancesRequestRequestTypeDef(TypedDict):
    botId: str
    localeId: str
    aggregationDuration: UtteranceAggregationDurationTypeDef
    botAliasId: NotRequired[str]
    botVersion: NotRequired[str]
    sortBy: NotRequired[AggregatedUtterancesSortByTypeDef]
    filters: NotRequired[Sequence[AggregatedUtterancesFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAggregatedUtterancesResponseTypeDef(TypedDict):
    botId: str
    botAliasId: str
    botVersion: str
    localeId: str
    aggregationDuration: UtteranceAggregationDurationTypeDef
    aggregationWindowStartTime: datetime
    aggregationWindowEndTime: datetime
    aggregationLastRefreshedDateTime: datetime
    aggregatedUtterancesSummaries: List[AggregatedUtterancesSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class RuntimeHintsTypeDef(TypedDict):
    slotHints: NotRequired[Dict[str, Dict[str, RuntimeHintDetailsTypeDef]]]

SlotTypeValueUnionTypeDef = Union[SlotTypeValueTypeDef, SlotTypeValueOutputTypeDef]
SlotDefaultValueSpecificationUnionTypeDef = Union[
    SlotDefaultValueSpecificationTypeDef, SlotDefaultValueSpecificationOutputTypeDef
]

class IntentLevelSlotResolutionTestResultItemTypeDef(TypedDict):
    intentName: str
    multiTurnConversation: bool
    slotResolutionResults: List[SlotResolutionTestResultItemTypeDef]

class IntentOverrideOutputTypeDef(TypedDict):
    name: NotRequired[str]
    slots: NotRequired[Dict[str, SlotValueOverrideOutputTypeDef]]

SlotValueOverrideUnionTypeDef = Union[SlotValueOverrideTypeDef, SlotValueOverrideOutputTypeDef]

class CreateTestSetDiscrepancyReportRequestRequestTypeDef(TypedDict):
    testSetId: str
    target: TestSetDiscrepancyReportResourceTargetTypeDef

class CreateTestSetDiscrepancyReportResponseTypeDef(TypedDict):
    testSetDiscrepancyReportId: str
    creationDateTime: datetime
    testSetId: str
    target: TestSetDiscrepancyReportResourceTargetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeTestSetDiscrepancyReportResponseTypeDef(TypedDict):
    testSetDiscrepancyReportId: str
    testSetId: str
    creationDateTime: datetime
    target: TestSetDiscrepancyReportResourceTargetTypeDef
    testSetDiscrepancyReportStatus: TestSetDiscrepancyReportStatusType
    lastUpdatedDataTime: datetime
    testSetDiscrepancyTopErrors: TestSetDiscrepancyErrorsTypeDef
    testSetDiscrepancyRawOutputUrl: str
    failureReasons: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class ImportResourceSpecificationOutputTypeDef(TypedDict):
    botImportSpecification: NotRequired[BotImportSpecificationOutputTypeDef]
    botLocaleImportSpecification: NotRequired[BotLocaleImportSpecificationTypeDef]
    customVocabularyImportSpecification: NotRequired[CustomVocabularyImportSpecificationTypeDef]
    testSetImportResourceSpecification: NotRequired[TestSetImportResourceSpecificationOutputTypeDef]

TestSetImportResourceSpecificationUnionTypeDef = Union[
    TestSetImportResourceSpecificationTypeDef, TestSetImportResourceSpecificationOutputTypeDef
]

class UserTurnOutputSpecificationTypeDef(TypedDict):
    intent: UserTurnIntentOutputTypeDef
    activeContexts: NotRequired[List[ActiveContextTypeDef]]
    transcript: NotRequired[str]

class BuildtimeSettingsTypeDef(TypedDict):
    descriptiveBotBuilder: NotRequired[DescriptiveBotBuilderSpecificationTypeDef]
    sampleUtteranceGeneration: NotRequired[SampleUtteranceGenerationSpecificationTypeDef]

class RuntimeSettingsTypeDef(TypedDict):
    slotResolutionImprovement: NotRequired[SlotResolutionImprovementSpecificationTypeDef]

class ListTestExecutionsResponseTypeDef(TypedDict):
    testExecutions: List[TestExecutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class MessageGroupOutputTypeDef(TypedDict):
    message: MessageOutputTypeDef
    variations: NotRequired[List[MessageOutputTypeDef]]

class UtteranceSpecificationTypeDef(TypedDict):
    botAliasId: NotRequired[str]
    botVersion: NotRequired[str]
    localeId: NotRequired[str]
    sessionId: NotRequired[str]
    channel: NotRequired[str]
    mode: NotRequired[AnalyticsModalityType]
    conversationStartTime: NotRequired[datetime]
    conversationEndTime: NotRequired[datetime]
    utterance: NotRequired[str]
    utteranceTimestamp: NotRequired[datetime]
    audioVoiceDurationMillis: NotRequired[int]
    utteranceUnderstood: NotRequired[bool]
    inputType: NotRequired[str]
    outputType: NotRequired[str]
    associatedIntentName: NotRequired[str]
    associatedSlotName: NotRequired[str]
    intentState: NotRequired[IntentStateType]
    dialogActionType: NotRequired[str]
    botResponseAudioVoiceId: NotRequired[str]
    slotsFilledInSession: NotRequired[str]
    utteranceRequestId: NotRequired[str]
    botResponses: NotRequired[List[UtteranceBotResponseTypeDef]]

class MessageTypeDef(TypedDict):
    plainTextMessage: NotRequired[PlainTextMessageTypeDef]
    customPayload: NotRequired[CustomPayloadTypeDef]
    ssmlMessage: NotRequired[SSMLMessageTypeDef]
    imageResponseCard: NotRequired[ImageResponseCardUnionTypeDef]

class ConversationLogSettingsOutputTypeDef(TypedDict):
    textLogSettings: NotRequired[List[TextLogSettingTypeDef]]
    audioLogSettings: NotRequired[List[AudioLogSettingTypeDef]]

class ConversationLogSettingsTypeDef(TypedDict):
    textLogSettings: NotRequired[Sequence[TextLogSettingTypeDef]]
    audioLogSettings: NotRequired[Sequence[AudioLogSettingTypeDef]]

class DescribeTestSetGenerationResponseTypeDef(TypedDict):
    testSetGenerationId: str
    testSetGenerationStatus: TestSetGenerationStatusType
    failureReasons: List[str]
    testSetId: str
    testSetName: str
    description: str
    storageLocation: TestSetStorageLocationTypeDef
    generationDataSource: TestSetGenerationDataSourceOutputTypeDef
    roleArn: str
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class StartTestSetGenerationResponseTypeDef(TypedDict):
    testSetGenerationId: str
    creationDateTime: datetime
    testSetGenerationStatus: TestSetGenerationStatusType
    testSetName: str
    description: str
    storageLocation: TestSetStorageLocationTypeDef
    generationDataSource: TestSetGenerationDataSourceOutputTypeDef
    roleArn: str
    testSetTags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

ConversationLogsDataSourceTypeDef = TypedDict(
    "ConversationLogsDataSourceTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "filter": ConversationLogsDataSourceFilterByUnionTypeDef,
    },
)

class LexTranscriptFilterTypeDef(TypedDict):
    dateRangeFilter: NotRequired[DateRangeFilterUnionTypeDef]

class S3BucketTranscriptSourceOutputTypeDef(TypedDict):
    s3BucketName: str
    transcriptFormat: Literal["Lex"]
    pathFormat: NotRequired[PathFormatOutputTypeDef]
    transcriptFilter: NotRequired[TranscriptFilterOutputTypeDef]
    kmsKeyArn: NotRequired[str]

class QnAIntentConfigurationOutputTypeDef(TypedDict):
    dataSourceConfiguration: NotRequired[DataSourceConfigurationOutputTypeDef]
    bedrockModelConfiguration: NotRequired[BedrockModelSpecificationTypeDef]

class DataSourceConfigurationTypeDef(TypedDict):
    opensearchConfiguration: NotRequired[OpensearchConfigurationUnionTypeDef]
    kendraConfiguration: NotRequired[QnAKendraConfigurationTypeDef]
    bedrockKnowledgeStoreConfiguration: NotRequired[BedrockKnowledgeStoreConfigurationTypeDef]

class ListExportsResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    exportSummaries: List[ExportSummaryTypeDef]
    localeId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateSlotTypeResponseTypeDef(TypedDict):
    slotTypeId: str
    slotTypeName: str
    description: str
    slotTypeValues: List[SlotTypeValueOutputTypeDef]
    valueSelectionSetting: SlotValueSelectionSettingTypeDef
    parentSlotTypeSignature: str
    botId: str
    botVersion: str
    localeId: str
    creationDateTime: datetime
    externalSourceSetting: ExternalSourceSettingTypeDef
    compositeSlotTypeSetting: CompositeSlotTypeSettingOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeSlotTypeResponseTypeDef(TypedDict):
    slotTypeId: str
    slotTypeName: str
    description: str
    slotTypeValues: List[SlotTypeValueOutputTypeDef]
    valueSelectionSetting: SlotValueSelectionSettingTypeDef
    parentSlotTypeSignature: str
    botId: str
    botVersion: str
    localeId: str
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    externalSourceSetting: ExternalSourceSettingTypeDef
    compositeSlotTypeSetting: CompositeSlotTypeSettingOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSlotTypeRequestRequestTypeDef(TypedDict):
    slotTypeId: str
    slotTypeName: str
    botId: str
    botVersion: str
    localeId: str
    description: NotRequired[str]
    slotTypeValues: NotRequired[Sequence[SlotTypeValueTypeDef]]
    valueSelectionSetting: NotRequired[SlotValueSelectionSettingTypeDef]
    parentSlotTypeSignature: NotRequired[str]
    externalSourceSetting: NotRequired[ExternalSourceSettingTypeDef]
    compositeSlotTypeSetting: NotRequired[CompositeSlotTypeSettingTypeDef]

class UpdateSlotTypeResponseTypeDef(TypedDict):
    slotTypeId: str
    slotTypeName: str
    description: str
    slotTypeValues: List[SlotTypeValueOutputTypeDef]
    valueSelectionSetting: SlotValueSelectionSettingTypeDef
    parentSlotTypeSignature: str
    botId: str
    botVersion: str
    localeId: str
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    externalSourceSetting: ExternalSourceSettingTypeDef
    compositeSlotTypeSetting: CompositeSlotTypeSettingOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class InputSessionStateSpecificationTypeDef(TypedDict):
    sessionAttributes: NotRequired[Dict[str, str]]
    activeContexts: NotRequired[List[ActiveContextTypeDef]]
    runtimeHints: NotRequired[RuntimeHintsTypeDef]

class CreateSlotTypeRequestRequestTypeDef(TypedDict):
    slotTypeName: str
    botId: str
    botVersion: str
    localeId: str
    description: NotRequired[str]
    slotTypeValues: NotRequired[Sequence[SlotTypeValueUnionTypeDef]]
    valueSelectionSetting: NotRequired[SlotValueSelectionSettingTypeDef]
    parentSlotTypeSignature: NotRequired[str]
    externalSourceSetting: NotRequired[ExternalSourceSettingTypeDef]
    compositeSlotTypeSetting: NotRequired[CompositeSlotTypeSettingTypeDef]

class IntentLevelSlotResolutionTestResultsTypeDef(TypedDict):
    items: List[IntentLevelSlotResolutionTestResultItemTypeDef]

class DialogStateOutputTypeDef(TypedDict):
    dialogAction: NotRequired[DialogActionTypeDef]
    intent: NotRequired[IntentOverrideOutputTypeDef]
    sessionAttributes: NotRequired[Dict[str, str]]

class IntentOverrideTypeDef(TypedDict):
    name: NotRequired[str]
    slots: NotRequired[Mapping[str, SlotValueOverrideUnionTypeDef]]

class DescribeImportResponseTypeDef(TypedDict):
    importId: str
    resourceSpecification: ImportResourceSpecificationOutputTypeDef
    importedResourceId: str
    importedResourceName: str
    mergeStrategy: MergeStrategyType
    importStatus: ImportStatusType
    failureReasons: List[str]
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class StartImportResponseTypeDef(TypedDict):
    importId: str
    resourceSpecification: ImportResourceSpecificationOutputTypeDef
    mergeStrategy: MergeStrategyType
    importStatus: ImportStatusType
    creationDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ImportResourceSpecificationTypeDef(TypedDict):
    botImportSpecification: NotRequired[BotImportSpecificationUnionTypeDef]
    botLocaleImportSpecification: NotRequired[BotLocaleImportSpecificationTypeDef]
    customVocabularyImportSpecification: NotRequired[CustomVocabularyImportSpecificationTypeDef]
    testSetImportResourceSpecification: NotRequired[TestSetImportResourceSpecificationUnionTypeDef]

class GenerativeAISettingsTypeDef(TypedDict):
    runtimeSettings: NotRequired[RuntimeSettingsTypeDef]
    buildtimeSettings: NotRequired[BuildtimeSettingsTypeDef]

class FulfillmentStartResponseSpecificationOutputTypeDef(TypedDict):
    delayInSeconds: int
    messageGroups: List[MessageGroupOutputTypeDef]
    allowInterrupt: NotRequired[bool]

class FulfillmentUpdateResponseSpecificationOutputTypeDef(TypedDict):
    frequencyInSeconds: int
    messageGroups: List[MessageGroupOutputTypeDef]
    allowInterrupt: NotRequired[bool]

class PromptSpecificationOutputTypeDef(TypedDict):
    messageGroups: List[MessageGroupOutputTypeDef]
    maxRetries: int
    allowInterrupt: NotRequired[bool]
    messageSelectionStrategy: NotRequired[MessageSelectionStrategyType]
    promptAttemptsSpecification: NotRequired[
        Dict[PromptAttemptType, PromptAttemptSpecificationTypeDef]
    ]

class ResponseSpecificationOutputTypeDef(TypedDict):
    messageGroups: List[MessageGroupOutputTypeDef]
    allowInterrupt: NotRequired[bool]

class StillWaitingResponseSpecificationOutputTypeDef(TypedDict):
    messageGroups: List[MessageGroupOutputTypeDef]
    frequencyInSeconds: int
    timeoutInSeconds: int
    allowInterrupt: NotRequired[bool]

class ListUtteranceAnalyticsDataResponseTypeDef(TypedDict):
    botId: str
    utterances: List[UtteranceSpecificationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

MessageUnionTypeDef = Union[MessageTypeDef, MessageOutputTypeDef]

class CreateBotAliasResponseTypeDef(TypedDict):
    botAliasId: str
    botAliasName: str
    description: str
    botVersion: str
    botAliasLocaleSettings: Dict[str, BotAliasLocaleSettingsTypeDef]
    conversationLogSettings: ConversationLogSettingsOutputTypeDef
    sentimentAnalysisSettings: SentimentAnalysisSettingsTypeDef
    botAliasStatus: BotAliasStatusType
    botId: str
    creationDateTime: datetime
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBotAliasResponseTypeDef(TypedDict):
    botAliasId: str
    botAliasName: str
    description: str
    botVersion: str
    botAliasLocaleSettings: Dict[str, BotAliasLocaleSettingsTypeDef]
    conversationLogSettings: ConversationLogSettingsOutputTypeDef
    sentimentAnalysisSettings: SentimentAnalysisSettingsTypeDef
    botAliasHistoryEvents: List[BotAliasHistoryEventTypeDef]
    botAliasStatus: BotAliasStatusType
    botId: str
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    parentBotNetworks: List[ParentBotNetworkTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBotAliasResponseTypeDef(TypedDict):
    botAliasId: str
    botAliasName: str
    description: str
    botVersion: str
    botAliasLocaleSettings: Dict[str, BotAliasLocaleSettingsTypeDef]
    conversationLogSettings: ConversationLogSettingsOutputTypeDef
    sentimentAnalysisSettings: SentimentAnalysisSettingsTypeDef
    botAliasStatus: BotAliasStatusType
    botId: str
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBotAliasRequestRequestTypeDef(TypedDict):
    botAliasName: str
    botId: str
    description: NotRequired[str]
    botVersion: NotRequired[str]
    botAliasLocaleSettings: NotRequired[Mapping[str, BotAliasLocaleSettingsTypeDef]]
    conversationLogSettings: NotRequired[ConversationLogSettingsTypeDef]
    sentimentAnalysisSettings: NotRequired[SentimentAnalysisSettingsTypeDef]
    tags: NotRequired[Mapping[str, str]]

class UpdateBotAliasRequestRequestTypeDef(TypedDict):
    botAliasId: str
    botAliasName: str
    botId: str
    description: NotRequired[str]
    botVersion: NotRequired[str]
    botAliasLocaleSettings: NotRequired[Mapping[str, BotAliasLocaleSettingsTypeDef]]
    conversationLogSettings: NotRequired[ConversationLogSettingsTypeDef]
    sentimentAnalysisSettings: NotRequired[SentimentAnalysisSettingsTypeDef]

ConversationLogsDataSourceUnionTypeDef = Union[
    ConversationLogsDataSourceTypeDef, ConversationLogsDataSourceOutputTypeDef
]
LexTranscriptFilterUnionTypeDef = Union[
    LexTranscriptFilterTypeDef, LexTranscriptFilterOutputTypeDef
]

class TranscriptSourceSettingOutputTypeDef(TypedDict):
    s3BucketTranscriptSource: NotRequired[S3BucketTranscriptSourceOutputTypeDef]

DataSourceConfigurationUnionTypeDef = Union[
    DataSourceConfigurationTypeDef, DataSourceConfigurationOutputTypeDef
]

class UserTurnInputSpecificationTypeDef(TypedDict):
    utteranceInput: UtteranceInputSpecificationTypeDef
    requestAttributes: NotRequired[Dict[str, str]]
    sessionState: NotRequired[InputSessionStateSpecificationTypeDef]

IntentOverrideUnionTypeDef = Union[IntentOverrideTypeDef, IntentOverrideOutputTypeDef]

class StartImportRequestRequestTypeDef(TypedDict):
    importId: str
    resourceSpecification: ImportResourceSpecificationTypeDef
    mergeStrategy: MergeStrategyType
    filePassword: NotRequired[str]

class CreateBotLocaleRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    nluIntentConfidenceThreshold: float
    description: NotRequired[str]
    voiceSettings: NotRequired[VoiceSettingsTypeDef]
    generativeAISettings: NotRequired[GenerativeAISettingsTypeDef]

class CreateBotLocaleResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeName: str
    localeId: str
    description: str
    nluIntentConfidenceThreshold: float
    voiceSettings: VoiceSettingsTypeDef
    botLocaleStatus: BotLocaleStatusType
    creationDateTime: datetime
    generativeAISettings: GenerativeAISettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBotLocaleResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    localeName: str
    description: str
    nluIntentConfidenceThreshold: float
    voiceSettings: VoiceSettingsTypeDef
    intentsCount: int
    slotTypesCount: int
    botLocaleStatus: BotLocaleStatusType
    failureReasons: List[str]
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    lastBuildSubmittedDateTime: datetime
    botLocaleHistoryEvents: List[BotLocaleHistoryEventTypeDef]
    recommendedActions: List[str]
    generativeAISettings: GenerativeAISettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBotLocaleRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    nluIntentConfidenceThreshold: float
    description: NotRequired[str]
    voiceSettings: NotRequired[VoiceSettingsTypeDef]
    generativeAISettings: NotRequired[GenerativeAISettingsTypeDef]

class UpdateBotLocaleResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    localeName: str
    description: str
    nluIntentConfidenceThreshold: float
    voiceSettings: VoiceSettingsTypeDef
    botLocaleStatus: BotLocaleStatusType
    failureReasons: List[str]
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    recommendedActions: List[str]
    generativeAISettings: GenerativeAISettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class FulfillmentUpdatesSpecificationOutputTypeDef(TypedDict):
    active: bool
    startResponse: NotRequired[FulfillmentStartResponseSpecificationOutputTypeDef]
    updateResponse: NotRequired[FulfillmentUpdateResponseSpecificationOutputTypeDef]
    timeoutInSeconds: NotRequired[int]

class SlotSummaryTypeDef(TypedDict):
    slotId: NotRequired[str]
    slotName: NotRequired[str]
    description: NotRequired[str]
    slotConstraint: NotRequired[SlotConstraintType]
    slotTypeId: NotRequired[str]
    valueElicitationPromptSpecification: NotRequired[PromptSpecificationOutputTypeDef]
    lastUpdatedDateTime: NotRequired[datetime]

class ConditionalBranchOutputTypeDef(TypedDict):
    name: str
    condition: ConditionTypeDef
    nextStep: DialogStateOutputTypeDef
    response: NotRequired[ResponseSpecificationOutputTypeDef]

class DefaultConditionalBranchOutputTypeDef(TypedDict):
    nextStep: NotRequired[DialogStateOutputTypeDef]
    response: NotRequired[ResponseSpecificationOutputTypeDef]

class WaitAndContinueSpecificationOutputTypeDef(TypedDict):
    waitingResponse: ResponseSpecificationOutputTypeDef
    continueResponse: ResponseSpecificationOutputTypeDef
    stillWaitingResponse: NotRequired[StillWaitingResponseSpecificationOutputTypeDef]
    active: NotRequired[bool]

class MessageGroupTypeDef(TypedDict):
    message: MessageUnionTypeDef
    variations: NotRequired[Sequence[MessageUnionTypeDef]]

class TestSetGenerationDataSourceTypeDef(TypedDict):
    conversationLogsDataSource: NotRequired[ConversationLogsDataSourceUnionTypeDef]

class TranscriptFilterTypeDef(TypedDict):
    lexTranscriptFilter: NotRequired[LexTranscriptFilterUnionTypeDef]

class DescribeBotRecommendationResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botRecommendationStatus: BotRecommendationStatusType
    botRecommendationId: str
    failureReasons: List[str]
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    transcriptSourceSetting: TranscriptSourceSettingOutputTypeDef
    encryptionSetting: EncryptionSettingTypeDef
    botRecommendationResults: BotRecommendationResultsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartBotRecommendationResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botRecommendationStatus: BotRecommendationStatusType
    botRecommendationId: str
    creationDateTime: datetime
    transcriptSourceSetting: TranscriptSourceSettingOutputTypeDef
    encryptionSetting: EncryptionSettingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBotRecommendationResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    botRecommendationStatus: BotRecommendationStatusType
    botRecommendationId: str
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    transcriptSourceSetting: TranscriptSourceSettingOutputTypeDef
    encryptionSetting: EncryptionSettingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class QnAIntentConfigurationTypeDef(TypedDict):
    dataSourceConfiguration: NotRequired[DataSourceConfigurationUnionTypeDef]
    bedrockModelConfiguration: NotRequired[BedrockModelSpecificationTypeDef]

UserTurnResultTypeDef = TypedDict(
    "UserTurnResultTypeDef",
    {
        "input": UserTurnInputSpecificationTypeDef,
        "expectedOutput": UserTurnOutputSpecificationTypeDef,
        "actualOutput": NotRequired[UserTurnOutputSpecificationTypeDef],
        "errorDetails": NotRequired[ExecutionErrorDetailsTypeDef],
        "endToEndResult": NotRequired[TestResultMatchStatusType],
        "intentMatchResult": NotRequired[TestResultMatchStatusType],
        "slotMatchResult": NotRequired[TestResultMatchStatusType],
        "speechTranscriptionResult": NotRequired[TestResultMatchStatusType],
        "conversationLevelResult": NotRequired[ConversationLevelResultDetailTypeDef],
    },
)
UserTurnSpecificationTypeDef = TypedDict(
    "UserTurnSpecificationTypeDef",
    {
        "input": UserTurnInputSpecificationTypeDef,
        "expected": UserTurnOutputSpecificationTypeDef,
    },
)

class DialogStateTypeDef(TypedDict):
    dialogAction: NotRequired[DialogActionTypeDef]
    intent: NotRequired[IntentOverrideUnionTypeDef]
    sessionAttributes: NotRequired[Mapping[str, str]]

class ListSlotsResponseTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    intentId: str
    slotSummaries: List[SlotSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ConditionalSpecificationOutputTypeDef(TypedDict):
    active: bool
    conditionalBranches: List[ConditionalBranchOutputTypeDef]
    defaultBranch: DefaultConditionalBranchOutputTypeDef

class SubSlotValueElicitationSettingOutputTypeDef(TypedDict):
    promptSpecification: PromptSpecificationOutputTypeDef
    defaultValueSpecification: NotRequired[SlotDefaultValueSpecificationOutputTypeDef]
    sampleUtterances: NotRequired[List[SampleUtteranceTypeDef]]
    waitAndContinueSpecification: NotRequired[WaitAndContinueSpecificationOutputTypeDef]

class FulfillmentStartResponseSpecificationTypeDef(TypedDict):
    delayInSeconds: int
    messageGroups: Sequence[MessageGroupTypeDef]
    allowInterrupt: NotRequired[bool]

class FulfillmentUpdateResponseSpecificationTypeDef(TypedDict):
    frequencyInSeconds: int
    messageGroups: Sequence[MessageGroupTypeDef]
    allowInterrupt: NotRequired[bool]

MessageGroupUnionTypeDef = Union[MessageGroupTypeDef, MessageGroupOutputTypeDef]

class StartTestSetGenerationRequestRequestTypeDef(TypedDict):
    testSetName: str
    storageLocation: TestSetStorageLocationTypeDef
    generationDataSource: TestSetGenerationDataSourceTypeDef
    roleArn: str
    description: NotRequired[str]
    testSetTags: NotRequired[Mapping[str, str]]

TranscriptFilterUnionTypeDef = Union[TranscriptFilterTypeDef, TranscriptFilterOutputTypeDef]

class TestSetTurnResultTypeDef(TypedDict):
    agent: NotRequired[AgentTurnResultTypeDef]
    user: NotRequired[UserTurnResultTypeDef]

class TurnSpecificationTypeDef(TypedDict):
    agentTurn: NotRequired[AgentTurnSpecificationTypeDef]
    userTurn: NotRequired[UserTurnSpecificationTypeDef]

DialogStateUnionTypeDef = Union[DialogStateTypeDef, DialogStateOutputTypeDef]

class IntentClosingSettingOutputTypeDef(TypedDict):
    closingResponse: NotRequired[ResponseSpecificationOutputTypeDef]
    active: NotRequired[bool]
    nextStep: NotRequired[DialogStateOutputTypeDef]
    conditional: NotRequired[ConditionalSpecificationOutputTypeDef]

class PostDialogCodeHookInvocationSpecificationOutputTypeDef(TypedDict):
    successResponse: NotRequired[ResponseSpecificationOutputTypeDef]
    successNextStep: NotRequired[DialogStateOutputTypeDef]
    successConditional: NotRequired[ConditionalSpecificationOutputTypeDef]
    failureResponse: NotRequired[ResponseSpecificationOutputTypeDef]
    failureNextStep: NotRequired[DialogStateOutputTypeDef]
    failureConditional: NotRequired[ConditionalSpecificationOutputTypeDef]
    timeoutResponse: NotRequired[ResponseSpecificationOutputTypeDef]
    timeoutNextStep: NotRequired[DialogStateOutputTypeDef]
    timeoutConditional: NotRequired[ConditionalSpecificationOutputTypeDef]

class PostFulfillmentStatusSpecificationOutputTypeDef(TypedDict):
    successResponse: NotRequired[ResponseSpecificationOutputTypeDef]
    failureResponse: NotRequired[ResponseSpecificationOutputTypeDef]
    timeoutResponse: NotRequired[ResponseSpecificationOutputTypeDef]
    successNextStep: NotRequired[DialogStateOutputTypeDef]
    successConditional: NotRequired[ConditionalSpecificationOutputTypeDef]
    failureNextStep: NotRequired[DialogStateOutputTypeDef]
    failureConditional: NotRequired[ConditionalSpecificationOutputTypeDef]
    timeoutNextStep: NotRequired[DialogStateOutputTypeDef]
    timeoutConditional: NotRequired[ConditionalSpecificationOutputTypeDef]

class SpecificationsOutputTypeDef(TypedDict):
    slotTypeId: str
    valueElicitationSetting: SubSlotValueElicitationSettingOutputTypeDef

FulfillmentStartResponseSpecificationUnionTypeDef = Union[
    FulfillmentStartResponseSpecificationTypeDef, FulfillmentStartResponseSpecificationOutputTypeDef
]
FulfillmentUpdateResponseSpecificationUnionTypeDef = Union[
    FulfillmentUpdateResponseSpecificationTypeDef,
    FulfillmentUpdateResponseSpecificationOutputTypeDef,
]

class PromptSpecificationTypeDef(TypedDict):
    messageGroups: Sequence[MessageGroupUnionTypeDef]
    maxRetries: int
    allowInterrupt: NotRequired[bool]
    messageSelectionStrategy: NotRequired[MessageSelectionStrategyType]
    promptAttemptsSpecification: NotRequired[
        Mapping[PromptAttemptType, PromptAttemptSpecificationTypeDef]
    ]

class ResponseSpecificationTypeDef(TypedDict):
    messageGroups: Sequence[MessageGroupUnionTypeDef]
    allowInterrupt: NotRequired[bool]

class StillWaitingResponseSpecificationTypeDef(TypedDict):
    messageGroups: Sequence[MessageGroupUnionTypeDef]
    frequencyInSeconds: int
    timeoutInSeconds: int
    allowInterrupt: NotRequired[bool]

class S3BucketTranscriptSourceTypeDef(TypedDict):
    s3BucketName: str
    transcriptFormat: Literal["Lex"]
    pathFormat: NotRequired[PathFormatUnionTypeDef]
    transcriptFilter: NotRequired[TranscriptFilterUnionTypeDef]
    kmsKeyArn: NotRequired[str]

class UtteranceLevelTestResultItemTypeDef(TypedDict):
    recordNumber: int
    turnResult: TestSetTurnResultTypeDef
    conversationId: NotRequired[str]

class TestSetTurnRecordTypeDef(TypedDict):
    recordNumber: int
    turnSpecification: TurnSpecificationTypeDef
    conversationId: NotRequired[str]
    turnNumber: NotRequired[int]

class DialogCodeHookInvocationSettingOutputTypeDef(TypedDict):
    enableCodeHookInvocation: bool
    active: bool
    postCodeHookSpecification: PostDialogCodeHookInvocationSpecificationOutputTypeDef
    invocationLabel: NotRequired[str]

class FulfillmentCodeHookSettingsOutputTypeDef(TypedDict):
    enabled: bool
    postFulfillmentStatusSpecification: NotRequired[PostFulfillmentStatusSpecificationOutputTypeDef]
    fulfillmentUpdatesSpecification: NotRequired[FulfillmentUpdatesSpecificationOutputTypeDef]
    active: NotRequired[bool]

class SubSlotSettingOutputTypeDef(TypedDict):
    expression: NotRequired[str]
    slotSpecifications: NotRequired[Dict[str, SpecificationsOutputTypeDef]]

class FulfillmentUpdatesSpecificationTypeDef(TypedDict):
    active: bool
    startResponse: NotRequired[FulfillmentStartResponseSpecificationUnionTypeDef]
    updateResponse: NotRequired[FulfillmentUpdateResponseSpecificationUnionTypeDef]
    timeoutInSeconds: NotRequired[int]

PromptSpecificationUnionTypeDef = Union[
    PromptSpecificationTypeDef, PromptSpecificationOutputTypeDef
]
ResponseSpecificationUnionTypeDef = Union[
    ResponseSpecificationTypeDef, ResponseSpecificationOutputTypeDef
]
StillWaitingResponseSpecificationUnionTypeDef = Union[
    StillWaitingResponseSpecificationTypeDef, StillWaitingResponseSpecificationOutputTypeDef
]
S3BucketTranscriptSourceUnionTypeDef = Union[
    S3BucketTranscriptSourceTypeDef, S3BucketTranscriptSourceOutputTypeDef
]

class UtteranceLevelTestResultsTypeDef(TypedDict):
    items: List[UtteranceLevelTestResultItemTypeDef]

class ListTestSetRecordsResponseTypeDef(TypedDict):
    testSetRecords: List[TestSetTurnRecordTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class InitialResponseSettingOutputTypeDef(TypedDict):
    initialResponse: NotRequired[ResponseSpecificationOutputTypeDef]
    nextStep: NotRequired[DialogStateOutputTypeDef]
    conditional: NotRequired[ConditionalSpecificationOutputTypeDef]
    codeHook: NotRequired[DialogCodeHookInvocationSettingOutputTypeDef]

class IntentConfirmationSettingOutputTypeDef(TypedDict):
    promptSpecification: PromptSpecificationOutputTypeDef
    declinationResponse: NotRequired[ResponseSpecificationOutputTypeDef]
    active: NotRequired[bool]
    confirmationResponse: NotRequired[ResponseSpecificationOutputTypeDef]
    confirmationNextStep: NotRequired[DialogStateOutputTypeDef]
    confirmationConditional: NotRequired[ConditionalSpecificationOutputTypeDef]
    declinationNextStep: NotRequired[DialogStateOutputTypeDef]
    declinationConditional: NotRequired[ConditionalSpecificationOutputTypeDef]
    failureResponse: NotRequired[ResponseSpecificationOutputTypeDef]
    failureNextStep: NotRequired[DialogStateOutputTypeDef]
    failureConditional: NotRequired[ConditionalSpecificationOutputTypeDef]
    codeHook: NotRequired[DialogCodeHookInvocationSettingOutputTypeDef]
    elicitationCodeHook: NotRequired[ElicitationCodeHookInvocationSettingTypeDef]

class SlotCaptureSettingOutputTypeDef(TypedDict):
    captureResponse: NotRequired[ResponseSpecificationOutputTypeDef]
    captureNextStep: NotRequired[DialogStateOutputTypeDef]
    captureConditional: NotRequired[ConditionalSpecificationOutputTypeDef]
    failureResponse: NotRequired[ResponseSpecificationOutputTypeDef]
    failureNextStep: NotRequired[DialogStateOutputTypeDef]
    failureConditional: NotRequired[ConditionalSpecificationOutputTypeDef]
    codeHook: NotRequired[DialogCodeHookInvocationSettingOutputTypeDef]
    elicitationCodeHook: NotRequired[ElicitationCodeHookInvocationSettingTypeDef]

FulfillmentUpdatesSpecificationUnionTypeDef = Union[
    FulfillmentUpdatesSpecificationTypeDef, FulfillmentUpdatesSpecificationOutputTypeDef
]

class ConditionalBranchTypeDef(TypedDict):
    name: str
    condition: ConditionTypeDef
    nextStep: DialogStateUnionTypeDef
    response: NotRequired[ResponseSpecificationUnionTypeDef]

class DefaultConditionalBranchTypeDef(TypedDict):
    nextStep: NotRequired[DialogStateUnionTypeDef]
    response: NotRequired[ResponseSpecificationUnionTypeDef]

class WaitAndContinueSpecificationTypeDef(TypedDict):
    waitingResponse: ResponseSpecificationUnionTypeDef
    continueResponse: ResponseSpecificationUnionTypeDef
    stillWaitingResponse: NotRequired[StillWaitingResponseSpecificationUnionTypeDef]
    active: NotRequired[bool]

class TranscriptSourceSettingTypeDef(TypedDict):
    s3BucketTranscriptSource: NotRequired[S3BucketTranscriptSourceUnionTypeDef]

class TestExecutionResultItemsTypeDef(TypedDict):
    overallTestResults: NotRequired[OverallTestResultsTypeDef]
    conversationLevelTestResults: NotRequired[ConversationLevelTestResultsTypeDef]
    intentClassificationTestResults: NotRequired[IntentClassificationTestResultsTypeDef]
    intentLevelSlotResolutionTestResults: NotRequired[IntentLevelSlotResolutionTestResultsTypeDef]
    utteranceLevelTestResults: NotRequired[UtteranceLevelTestResultsTypeDef]

class CreateIntentResponseTypeDef(TypedDict):
    intentId: str
    intentName: str
    description: str
    parentIntentSignature: str
    sampleUtterances: List[SampleUtteranceTypeDef]
    dialogCodeHook: DialogCodeHookSettingsTypeDef
    fulfillmentCodeHook: FulfillmentCodeHookSettingsOutputTypeDef
    intentConfirmationSetting: IntentConfirmationSettingOutputTypeDef
    intentClosingSetting: IntentClosingSettingOutputTypeDef
    inputContexts: List[InputContextTypeDef]
    outputContexts: List[OutputContextTypeDef]
    kendraConfiguration: KendraConfigurationTypeDef
    botId: str
    botVersion: str
    localeId: str
    creationDateTime: datetime
    initialResponseSetting: InitialResponseSettingOutputTypeDef
    qnAIntentConfiguration: QnAIntentConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeIntentResponseTypeDef(TypedDict):
    intentId: str
    intentName: str
    description: str
    parentIntentSignature: str
    sampleUtterances: List[SampleUtteranceTypeDef]
    dialogCodeHook: DialogCodeHookSettingsTypeDef
    fulfillmentCodeHook: FulfillmentCodeHookSettingsOutputTypeDef
    slotPriorities: List[SlotPriorityTypeDef]
    intentConfirmationSetting: IntentConfirmationSettingOutputTypeDef
    intentClosingSetting: IntentClosingSettingOutputTypeDef
    inputContexts: List[InputContextTypeDef]
    outputContexts: List[OutputContextTypeDef]
    kendraConfiguration: KendraConfigurationTypeDef
    botId: str
    botVersion: str
    localeId: str
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    initialResponseSetting: InitialResponseSettingOutputTypeDef
    qnAIntentConfiguration: QnAIntentConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateIntentResponseTypeDef(TypedDict):
    intentId: str
    intentName: str
    description: str
    parentIntentSignature: str
    sampleUtterances: List[SampleUtteranceTypeDef]
    dialogCodeHook: DialogCodeHookSettingsTypeDef
    fulfillmentCodeHook: FulfillmentCodeHookSettingsOutputTypeDef
    slotPriorities: List[SlotPriorityTypeDef]
    intentConfirmationSetting: IntentConfirmationSettingOutputTypeDef
    intentClosingSetting: IntentClosingSettingOutputTypeDef
    inputContexts: List[InputContextTypeDef]
    outputContexts: List[OutputContextTypeDef]
    kendraConfiguration: KendraConfigurationTypeDef
    botId: str
    botVersion: str
    localeId: str
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    initialResponseSetting: InitialResponseSettingOutputTypeDef
    qnAIntentConfiguration: QnAIntentConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SlotValueElicitationSettingOutputTypeDef(TypedDict):
    slotConstraint: SlotConstraintType
    defaultValueSpecification: NotRequired[SlotDefaultValueSpecificationOutputTypeDef]
    promptSpecification: NotRequired[PromptSpecificationOutputTypeDef]
    sampleUtterances: NotRequired[List[SampleUtteranceTypeDef]]
    waitAndContinueSpecification: NotRequired[WaitAndContinueSpecificationOutputTypeDef]
    slotCaptureSetting: NotRequired[SlotCaptureSettingOutputTypeDef]
    slotResolutionSetting: NotRequired[SlotResolutionSettingTypeDef]

ConditionalBranchUnionTypeDef = Union[ConditionalBranchTypeDef, ConditionalBranchOutputTypeDef]
DefaultConditionalBranchUnionTypeDef = Union[
    DefaultConditionalBranchTypeDef, DefaultConditionalBranchOutputTypeDef
]
WaitAndContinueSpecificationUnionTypeDef = Union[
    WaitAndContinueSpecificationTypeDef, WaitAndContinueSpecificationOutputTypeDef
]

class StartBotRecommendationRequestRequestTypeDef(TypedDict):
    botId: str
    botVersion: str
    localeId: str
    transcriptSourceSetting: TranscriptSourceSettingTypeDef
    encryptionSetting: NotRequired[EncryptionSettingTypeDef]

class ListTestExecutionResultItemsResponseTypeDef(TypedDict):
    testExecutionResults: TestExecutionResultItemsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateSlotResponseTypeDef(TypedDict):
    slotId: str
    slotName: str
    description: str
    slotTypeId: str
    valueElicitationSetting: SlotValueElicitationSettingOutputTypeDef
    obfuscationSetting: ObfuscationSettingTypeDef
    botId: str
    botVersion: str
    localeId: str
    intentId: str
    creationDateTime: datetime
    multipleValuesSetting: MultipleValuesSettingTypeDef
    subSlotSetting: SubSlotSettingOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeSlotResponseTypeDef(TypedDict):
    slotId: str
    slotName: str
    description: str
    slotTypeId: str
    valueElicitationSetting: SlotValueElicitationSettingOutputTypeDef
    obfuscationSetting: ObfuscationSettingTypeDef
    botId: str
    botVersion: str
    localeId: str
    intentId: str
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    multipleValuesSetting: MultipleValuesSettingTypeDef
    subSlotSetting: SubSlotSettingOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSlotResponseTypeDef(TypedDict):
    slotId: str
    slotName: str
    description: str
    slotTypeId: str
    valueElicitationSetting: SlotValueElicitationSettingOutputTypeDef
    obfuscationSetting: ObfuscationSettingTypeDef
    botId: str
    botVersion: str
    localeId: str
    intentId: str
    creationDateTime: datetime
    lastUpdatedDateTime: datetime
    multipleValuesSetting: MultipleValuesSettingTypeDef
    subSlotSetting: SubSlotSettingOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ConditionalSpecificationTypeDef(TypedDict):
    active: bool
    conditionalBranches: Sequence[ConditionalBranchUnionTypeDef]
    defaultBranch: DefaultConditionalBranchUnionTypeDef

class SubSlotValueElicitationSettingTypeDef(TypedDict):
    promptSpecification: PromptSpecificationUnionTypeDef
    defaultValueSpecification: NotRequired[SlotDefaultValueSpecificationUnionTypeDef]
    sampleUtterances: NotRequired[Sequence[SampleUtteranceTypeDef]]
    waitAndContinueSpecification: NotRequired[WaitAndContinueSpecificationUnionTypeDef]

ConditionalSpecificationUnionTypeDef = Union[
    ConditionalSpecificationTypeDef, ConditionalSpecificationOutputTypeDef
]
SubSlotValueElicitationSettingUnionTypeDef = Union[
    SubSlotValueElicitationSettingTypeDef, SubSlotValueElicitationSettingOutputTypeDef
]

class IntentClosingSettingTypeDef(TypedDict):
    closingResponse: NotRequired[ResponseSpecificationUnionTypeDef]
    active: NotRequired[bool]
    nextStep: NotRequired[DialogStateUnionTypeDef]
    conditional: NotRequired[ConditionalSpecificationUnionTypeDef]

class PostDialogCodeHookInvocationSpecificationTypeDef(TypedDict):
    successResponse: NotRequired[ResponseSpecificationUnionTypeDef]
    successNextStep: NotRequired[DialogStateUnionTypeDef]
    successConditional: NotRequired[ConditionalSpecificationUnionTypeDef]
    failureResponse: NotRequired[ResponseSpecificationUnionTypeDef]
    failureNextStep: NotRequired[DialogStateUnionTypeDef]
    failureConditional: NotRequired[ConditionalSpecificationUnionTypeDef]
    timeoutResponse: NotRequired[ResponseSpecificationUnionTypeDef]
    timeoutNextStep: NotRequired[DialogStateUnionTypeDef]
    timeoutConditional: NotRequired[ConditionalSpecificationUnionTypeDef]

class PostFulfillmentStatusSpecificationTypeDef(TypedDict):
    successResponse: NotRequired[ResponseSpecificationUnionTypeDef]
    failureResponse: NotRequired[ResponseSpecificationUnionTypeDef]
    timeoutResponse: NotRequired[ResponseSpecificationUnionTypeDef]
    successNextStep: NotRequired[DialogStateUnionTypeDef]
    successConditional: NotRequired[ConditionalSpecificationUnionTypeDef]
    failureNextStep: NotRequired[DialogStateUnionTypeDef]
    failureConditional: NotRequired[ConditionalSpecificationUnionTypeDef]
    timeoutNextStep: NotRequired[DialogStateUnionTypeDef]
    timeoutConditional: NotRequired[ConditionalSpecificationUnionTypeDef]

class SpecificationsTypeDef(TypedDict):
    slotTypeId: str
    valueElicitationSetting: SubSlotValueElicitationSettingUnionTypeDef

PostDialogCodeHookInvocationSpecificationUnionTypeDef = Union[
    PostDialogCodeHookInvocationSpecificationTypeDef,
    PostDialogCodeHookInvocationSpecificationOutputTypeDef,
]
PostFulfillmentStatusSpecificationUnionTypeDef = Union[
    PostFulfillmentStatusSpecificationTypeDef, PostFulfillmentStatusSpecificationOutputTypeDef
]
SpecificationsUnionTypeDef = Union[SpecificationsTypeDef, SpecificationsOutputTypeDef]

class DialogCodeHookInvocationSettingTypeDef(TypedDict):
    enableCodeHookInvocation: bool
    active: bool
    postCodeHookSpecification: PostDialogCodeHookInvocationSpecificationUnionTypeDef
    invocationLabel: NotRequired[str]

class FulfillmentCodeHookSettingsTypeDef(TypedDict):
    enabled: bool
    postFulfillmentStatusSpecification: NotRequired[PostFulfillmentStatusSpecificationUnionTypeDef]
    fulfillmentUpdatesSpecification: NotRequired[FulfillmentUpdatesSpecificationUnionTypeDef]
    active: NotRequired[bool]

class SubSlotSettingTypeDef(TypedDict):
    expression: NotRequired[str]
    slotSpecifications: NotRequired[Mapping[str, SpecificationsUnionTypeDef]]

DialogCodeHookInvocationSettingUnionTypeDef = Union[
    DialogCodeHookInvocationSettingTypeDef, DialogCodeHookInvocationSettingOutputTypeDef
]

class InitialResponseSettingTypeDef(TypedDict):
    initialResponse: NotRequired[ResponseSpecificationUnionTypeDef]
    nextStep: NotRequired[DialogStateUnionTypeDef]
    conditional: NotRequired[ConditionalSpecificationUnionTypeDef]
    codeHook: NotRequired[DialogCodeHookInvocationSettingUnionTypeDef]

class IntentConfirmationSettingTypeDef(TypedDict):
    promptSpecification: PromptSpecificationUnionTypeDef
    declinationResponse: NotRequired[ResponseSpecificationUnionTypeDef]
    active: NotRequired[bool]
    confirmationResponse: NotRequired[ResponseSpecificationUnionTypeDef]
    confirmationNextStep: NotRequired[DialogStateUnionTypeDef]
    confirmationConditional: NotRequired[ConditionalSpecificationUnionTypeDef]
    declinationNextStep: NotRequired[DialogStateUnionTypeDef]
    declinationConditional: NotRequired[ConditionalSpecificationUnionTypeDef]
    failureResponse: NotRequired[ResponseSpecificationUnionTypeDef]
    failureNextStep: NotRequired[DialogStateUnionTypeDef]
    failureConditional: NotRequired[ConditionalSpecificationUnionTypeDef]
    codeHook: NotRequired[DialogCodeHookInvocationSettingUnionTypeDef]
    elicitationCodeHook: NotRequired[ElicitationCodeHookInvocationSettingTypeDef]

class SlotCaptureSettingTypeDef(TypedDict):
    captureResponse: NotRequired[ResponseSpecificationUnionTypeDef]
    captureNextStep: NotRequired[DialogStateUnionTypeDef]
    captureConditional: NotRequired[ConditionalSpecificationUnionTypeDef]
    failureResponse: NotRequired[ResponseSpecificationUnionTypeDef]
    failureNextStep: NotRequired[DialogStateUnionTypeDef]
    failureConditional: NotRequired[ConditionalSpecificationUnionTypeDef]
    codeHook: NotRequired[DialogCodeHookInvocationSettingUnionTypeDef]
    elicitationCodeHook: NotRequired[ElicitationCodeHookInvocationSettingTypeDef]

class CreateIntentRequestRequestTypeDef(TypedDict):
    intentName: str
    botId: str
    botVersion: str
    localeId: str
    description: NotRequired[str]
    parentIntentSignature: NotRequired[str]
    sampleUtterances: NotRequired[Sequence[SampleUtteranceTypeDef]]
    dialogCodeHook: NotRequired[DialogCodeHookSettingsTypeDef]
    fulfillmentCodeHook: NotRequired[FulfillmentCodeHookSettingsTypeDef]
    intentConfirmationSetting: NotRequired[IntentConfirmationSettingTypeDef]
    intentClosingSetting: NotRequired[IntentClosingSettingTypeDef]
    inputContexts: NotRequired[Sequence[InputContextTypeDef]]
    outputContexts: NotRequired[Sequence[OutputContextTypeDef]]
    kendraConfiguration: NotRequired[KendraConfigurationTypeDef]
    initialResponseSetting: NotRequired[InitialResponseSettingTypeDef]
    qnAIntentConfiguration: NotRequired[QnAIntentConfigurationTypeDef]

class UpdateIntentRequestRequestTypeDef(TypedDict):
    intentId: str
    intentName: str
    botId: str
    botVersion: str
    localeId: str
    description: NotRequired[str]
    parentIntentSignature: NotRequired[str]
    sampleUtterances: NotRequired[Sequence[SampleUtteranceTypeDef]]
    dialogCodeHook: NotRequired[DialogCodeHookSettingsTypeDef]
    fulfillmentCodeHook: NotRequired[FulfillmentCodeHookSettingsTypeDef]
    slotPriorities: NotRequired[Sequence[SlotPriorityTypeDef]]
    intentConfirmationSetting: NotRequired[IntentConfirmationSettingTypeDef]
    intentClosingSetting: NotRequired[IntentClosingSettingTypeDef]
    inputContexts: NotRequired[Sequence[InputContextTypeDef]]
    outputContexts: NotRequired[Sequence[OutputContextTypeDef]]
    kendraConfiguration: NotRequired[KendraConfigurationTypeDef]
    initialResponseSetting: NotRequired[InitialResponseSettingTypeDef]
    qnAIntentConfiguration: NotRequired[QnAIntentConfigurationTypeDef]

SlotCaptureSettingUnionTypeDef = Union[SlotCaptureSettingTypeDef, SlotCaptureSettingOutputTypeDef]

class SlotValueElicitationSettingTypeDef(TypedDict):
    slotConstraint: SlotConstraintType
    defaultValueSpecification: NotRequired[SlotDefaultValueSpecificationUnionTypeDef]
    promptSpecification: NotRequired[PromptSpecificationUnionTypeDef]
    sampleUtterances: NotRequired[Sequence[SampleUtteranceTypeDef]]
    waitAndContinueSpecification: NotRequired[WaitAndContinueSpecificationUnionTypeDef]
    slotCaptureSetting: NotRequired[SlotCaptureSettingUnionTypeDef]
    slotResolutionSetting: NotRequired[SlotResolutionSettingTypeDef]

class CreateSlotRequestRequestTypeDef(TypedDict):
    slotName: str
    valueElicitationSetting: SlotValueElicitationSettingTypeDef
    botId: str
    botVersion: str
    localeId: str
    intentId: str
    description: NotRequired[str]
    slotTypeId: NotRequired[str]
    obfuscationSetting: NotRequired[ObfuscationSettingTypeDef]
    multipleValuesSetting: NotRequired[MultipleValuesSettingTypeDef]
    subSlotSetting: NotRequired[SubSlotSettingTypeDef]

class UpdateSlotRequestRequestTypeDef(TypedDict):
    slotId: str
    slotName: str
    valueElicitationSetting: SlotValueElicitationSettingTypeDef
    botId: str
    botVersion: str
    localeId: str
    intentId: str
    description: NotRequired[str]
    slotTypeId: NotRequired[str]
    obfuscationSetting: NotRequired[ObfuscationSettingTypeDef]
    multipleValuesSetting: NotRequired[MultipleValuesSettingTypeDef]
    subSlotSetting: NotRequired[SubSlotSettingTypeDef]
