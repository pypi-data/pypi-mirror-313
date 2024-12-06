"""
Type annotations for qconnect service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/type_defs/)

Usage::

    ```python
    from types_boto3_qconnect.type_defs import AIAgentConfigurationDataTypeDef

    data: AIAgentConfigurationDataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AIAgentTypeType,
    AIPromptAPIFormatType,
    AIPromptTypeType,
    AssistantCapabilityTypeType,
    AssistantStatusType,
    ChannelSubtypeType,
    ChunkingStrategyType,
    ContentStatusType,
    ConversationStatusReasonType,
    ConversationStatusType,
    GuardrailContentFilterTypeType,
    GuardrailContextualGroundingFilterTypeType,
    GuardrailFilterStrengthType,
    GuardrailPiiEntityTypeType,
    GuardrailSensitiveInformationActionType,
    ImportJobStatusType,
    KnowledgeBaseSearchTypeType,
    KnowledgeBaseStatusType,
    KnowledgeBaseTypeType,
    MessageTemplateAttributeTypeType,
    MessageTemplateFilterOperatorType,
    MessageTemplateQueryOperatorType,
    OrderType,
    OriginType,
    ParticipantType,
    PriorityType,
    QueryResultTypeType,
    QuickResponseFilterOperatorType,
    QuickResponseQueryOperatorType,
    QuickResponseStatusType,
    RecommendationSourceTypeType,
    RecommendationTriggerTypeType,
    RecommendationTypeType,
    ReferenceTypeType,
    RelevanceLevelType,
    RelevanceType,
    StatusType,
    SyncStatusType,
    TargetTypeType,
    VisibilityStatusType,
    WebScopeTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AIAgentConfigurationDataTypeDef",
    "AIAgentConfigurationOutputTypeDef",
    "AIAgentConfigurationTypeDef",
    "AIAgentDataTypeDef",
    "AIAgentSummaryTypeDef",
    "AIAgentVersionSummaryTypeDef",
    "AIGuardrailContentPolicyConfigOutputTypeDef",
    "AIGuardrailContentPolicyConfigTypeDef",
    "AIGuardrailContextualGroundingPolicyConfigOutputTypeDef",
    "AIGuardrailContextualGroundingPolicyConfigTypeDef",
    "AIGuardrailDataTypeDef",
    "AIGuardrailSensitiveInformationPolicyConfigOutputTypeDef",
    "AIGuardrailSensitiveInformationPolicyConfigTypeDef",
    "AIGuardrailSummaryTypeDef",
    "AIGuardrailTopicPolicyConfigOutputTypeDef",
    "AIGuardrailTopicPolicyConfigTypeDef",
    "AIGuardrailVersionSummaryTypeDef",
    "AIGuardrailWordPolicyConfigOutputTypeDef",
    "AIGuardrailWordPolicyConfigTypeDef",
    "AIPromptDataTypeDef",
    "AIPromptSummaryTypeDef",
    "AIPromptTemplateConfigurationTypeDef",
    "AIPromptVersionSummaryTypeDef",
    "ActivateMessageTemplateRequestRequestTypeDef",
    "ActivateMessageTemplateResponseTypeDef",
    "AgentAttributesTypeDef",
    "AmazonConnectGuideAssociationDataTypeDef",
    "AnswerRecommendationAIAgentConfigurationOutputTypeDef",
    "AnswerRecommendationAIAgentConfigurationTypeDef",
    "AnswerRecommendationAIAgentConfigurationUnionTypeDef",
    "AppIntegrationsConfigurationOutputTypeDef",
    "AppIntegrationsConfigurationTypeDef",
    "AppIntegrationsConfigurationUnionTypeDef",
    "AssistantAssociationDataTypeDef",
    "AssistantAssociationInputDataTypeDef",
    "AssistantAssociationOutputDataTypeDef",
    "AssistantAssociationSummaryTypeDef",
    "AssistantCapabilityConfigurationTypeDef",
    "AssistantDataTypeDef",
    "AssistantIntegrationConfigurationTypeDef",
    "AssistantSummaryTypeDef",
    "AssociationConfigurationDataOutputTypeDef",
    "AssociationConfigurationDataTypeDef",
    "AssociationConfigurationDataUnionTypeDef",
    "AssociationConfigurationOutputTypeDef",
    "AssociationConfigurationTypeDef",
    "AssociationConfigurationUnionTypeDef",
    "BedrockFoundationModelConfigurationForParsingTypeDef",
    "ChunkingConfigurationOutputTypeDef",
    "ChunkingConfigurationTypeDef",
    "ChunkingConfigurationUnionTypeDef",
    "CitationSpanTypeDef",
    "ConfigurationTypeDef",
    "ConnectConfigurationTypeDef",
    "ContentAssociationContentsTypeDef",
    "ContentAssociationDataTypeDef",
    "ContentAssociationSummaryTypeDef",
    "ContentDataDetailsTypeDef",
    "ContentDataTypeDef",
    "ContentFeedbackDataTypeDef",
    "ContentReferenceTypeDef",
    "ContentSummaryTypeDef",
    "ConversationContextTypeDef",
    "ConversationStateTypeDef",
    "CreateAIAgentRequestRequestTypeDef",
    "CreateAIAgentResponseTypeDef",
    "CreateAIAgentVersionRequestRequestTypeDef",
    "CreateAIAgentVersionResponseTypeDef",
    "CreateAIGuardrailRequestRequestTypeDef",
    "CreateAIGuardrailResponseTypeDef",
    "CreateAIGuardrailVersionRequestRequestTypeDef",
    "CreateAIGuardrailVersionResponseTypeDef",
    "CreateAIPromptRequestRequestTypeDef",
    "CreateAIPromptResponseTypeDef",
    "CreateAIPromptVersionRequestRequestTypeDef",
    "CreateAIPromptVersionResponseTypeDef",
    "CreateAssistantAssociationRequestRequestTypeDef",
    "CreateAssistantAssociationResponseTypeDef",
    "CreateAssistantRequestRequestTypeDef",
    "CreateAssistantResponseTypeDef",
    "CreateContentAssociationRequestRequestTypeDef",
    "CreateContentAssociationResponseTypeDef",
    "CreateContentRequestRequestTypeDef",
    "CreateContentResponseTypeDef",
    "CreateKnowledgeBaseRequestRequestTypeDef",
    "CreateKnowledgeBaseResponseTypeDef",
    "CreateMessageTemplateAttachmentRequestRequestTypeDef",
    "CreateMessageTemplateAttachmentResponseTypeDef",
    "CreateMessageTemplateRequestRequestTypeDef",
    "CreateMessageTemplateResponseTypeDef",
    "CreateMessageTemplateVersionRequestRequestTypeDef",
    "CreateMessageTemplateVersionResponseTypeDef",
    "CreateQuickResponseRequestRequestTypeDef",
    "CreateQuickResponseResponseTypeDef",
    "CreateSessionRequestRequestTypeDef",
    "CreateSessionResponseTypeDef",
    "CustomerProfileAttributesOutputTypeDef",
    "CustomerProfileAttributesTypeDef",
    "CustomerProfileAttributesUnionTypeDef",
    "DataDetailsPaginatorTypeDef",
    "DataDetailsTypeDef",
    "DataReferenceTypeDef",
    "DataSummaryPaginatorTypeDef",
    "DataSummaryTypeDef",
    "DeactivateMessageTemplateRequestRequestTypeDef",
    "DeactivateMessageTemplateResponseTypeDef",
    "DeleteAIAgentRequestRequestTypeDef",
    "DeleteAIAgentVersionRequestRequestTypeDef",
    "DeleteAIGuardrailRequestRequestTypeDef",
    "DeleteAIGuardrailVersionRequestRequestTypeDef",
    "DeleteAIPromptRequestRequestTypeDef",
    "DeleteAIPromptVersionRequestRequestTypeDef",
    "DeleteAssistantAssociationRequestRequestTypeDef",
    "DeleteAssistantRequestRequestTypeDef",
    "DeleteContentAssociationRequestRequestTypeDef",
    "DeleteContentRequestRequestTypeDef",
    "DeleteImportJobRequestRequestTypeDef",
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    "DeleteMessageTemplateAttachmentRequestRequestTypeDef",
    "DeleteMessageTemplateRequestRequestTypeDef",
    "DeleteQuickResponseRequestRequestTypeDef",
    "DocumentTextTypeDef",
    "DocumentTypeDef",
    "EmailHeaderTypeDef",
    "EmailMessageTemplateContentBodyTypeDef",
    "EmailMessageTemplateContentOutputTypeDef",
    "EmailMessageTemplateContentTypeDef",
    "EmailMessageTemplateContentUnionTypeDef",
    "ExtendedMessageTemplateDataTypeDef",
    "ExternalSourceConfigurationTypeDef",
    "FilterTypeDef",
    "FixedSizeChunkingConfigurationTypeDef",
    "GenerativeContentFeedbackDataTypeDef",
    "GenerativeDataDetailsPaginatorTypeDef",
    "GenerativeDataDetailsTypeDef",
    "GenerativeReferenceTypeDef",
    "GetAIAgentRequestRequestTypeDef",
    "GetAIAgentResponseTypeDef",
    "GetAIGuardrailRequestRequestTypeDef",
    "GetAIGuardrailResponseTypeDef",
    "GetAIPromptRequestRequestTypeDef",
    "GetAIPromptResponseTypeDef",
    "GetAssistantAssociationRequestRequestTypeDef",
    "GetAssistantAssociationResponseTypeDef",
    "GetAssistantRequestRequestTypeDef",
    "GetAssistantResponseTypeDef",
    "GetContentAssociationRequestRequestTypeDef",
    "GetContentAssociationResponseTypeDef",
    "GetContentRequestRequestTypeDef",
    "GetContentResponseTypeDef",
    "GetContentSummaryRequestRequestTypeDef",
    "GetContentSummaryResponseTypeDef",
    "GetImportJobRequestRequestTypeDef",
    "GetImportJobResponseTypeDef",
    "GetKnowledgeBaseRequestRequestTypeDef",
    "GetKnowledgeBaseResponseTypeDef",
    "GetMessageTemplateRequestRequestTypeDef",
    "GetMessageTemplateResponseTypeDef",
    "GetNextMessageRequestRequestTypeDef",
    "GetNextMessageResponseTypeDef",
    "GetQuickResponseRequestRequestTypeDef",
    "GetQuickResponseResponseTypeDef",
    "GetRecommendationsRequestRequestTypeDef",
    "GetRecommendationsResponseTypeDef",
    "GetSessionRequestRequestTypeDef",
    "GetSessionResponseTypeDef",
    "GroupingConfigurationOutputTypeDef",
    "GroupingConfigurationTypeDef",
    "GuardrailContentFilterConfigTypeDef",
    "GuardrailContextualGroundingFilterConfigTypeDef",
    "GuardrailManagedWordsConfigTypeDef",
    "GuardrailPiiEntityConfigTypeDef",
    "GuardrailRegexConfigTypeDef",
    "GuardrailTopicConfigOutputTypeDef",
    "GuardrailTopicConfigTypeDef",
    "GuardrailTopicConfigUnionTypeDef",
    "GuardrailWordConfigTypeDef",
    "HierarchicalChunkingConfigurationOutputTypeDef",
    "HierarchicalChunkingConfigurationTypeDef",
    "HierarchicalChunkingConfigurationUnionTypeDef",
    "HierarchicalChunkingLevelConfigurationTypeDef",
    "HighlightTypeDef",
    "ImportJobDataTypeDef",
    "ImportJobSummaryTypeDef",
    "IntentDetectedDataDetailsTypeDef",
    "IntentInputDataTypeDef",
    "KnowledgeBaseAssociationConfigurationDataOutputTypeDef",
    "KnowledgeBaseAssociationConfigurationDataTypeDef",
    "KnowledgeBaseAssociationConfigurationDataUnionTypeDef",
    "KnowledgeBaseAssociationDataTypeDef",
    "KnowledgeBaseDataTypeDef",
    "KnowledgeBaseSummaryTypeDef",
    "ListAIAgentVersionsRequestListAIAgentVersionsPaginateTypeDef",
    "ListAIAgentVersionsRequestRequestTypeDef",
    "ListAIAgentVersionsResponseTypeDef",
    "ListAIAgentsRequestListAIAgentsPaginateTypeDef",
    "ListAIAgentsRequestRequestTypeDef",
    "ListAIAgentsResponseTypeDef",
    "ListAIGuardrailVersionsRequestListAIGuardrailVersionsPaginateTypeDef",
    "ListAIGuardrailVersionsRequestRequestTypeDef",
    "ListAIGuardrailVersionsResponseTypeDef",
    "ListAIGuardrailsRequestListAIGuardrailsPaginateTypeDef",
    "ListAIGuardrailsRequestRequestTypeDef",
    "ListAIGuardrailsResponseTypeDef",
    "ListAIPromptVersionsRequestListAIPromptVersionsPaginateTypeDef",
    "ListAIPromptVersionsRequestRequestTypeDef",
    "ListAIPromptVersionsResponseTypeDef",
    "ListAIPromptsRequestListAIPromptsPaginateTypeDef",
    "ListAIPromptsRequestRequestTypeDef",
    "ListAIPromptsResponseTypeDef",
    "ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef",
    "ListAssistantAssociationsRequestRequestTypeDef",
    "ListAssistantAssociationsResponseTypeDef",
    "ListAssistantsRequestListAssistantsPaginateTypeDef",
    "ListAssistantsRequestRequestTypeDef",
    "ListAssistantsResponseTypeDef",
    "ListContentAssociationsRequestListContentAssociationsPaginateTypeDef",
    "ListContentAssociationsRequestRequestTypeDef",
    "ListContentAssociationsResponseTypeDef",
    "ListContentsRequestListContentsPaginateTypeDef",
    "ListContentsRequestRequestTypeDef",
    "ListContentsResponseTypeDef",
    "ListImportJobsRequestListImportJobsPaginateTypeDef",
    "ListImportJobsRequestRequestTypeDef",
    "ListImportJobsResponseTypeDef",
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    "ListKnowledgeBasesRequestRequestTypeDef",
    "ListKnowledgeBasesResponseTypeDef",
    "ListMessageTemplateVersionsRequestListMessageTemplateVersionsPaginateTypeDef",
    "ListMessageTemplateVersionsRequestRequestTypeDef",
    "ListMessageTemplateVersionsResponseTypeDef",
    "ListMessageTemplatesRequestListMessageTemplatesPaginateTypeDef",
    "ListMessageTemplatesRequestRequestTypeDef",
    "ListMessageTemplatesResponseTypeDef",
    "ListMessagesRequestListMessagesPaginateTypeDef",
    "ListMessagesRequestRequestTypeDef",
    "ListMessagesResponseTypeDef",
    "ListQuickResponsesRequestListQuickResponsesPaginateTypeDef",
    "ListQuickResponsesRequestRequestTypeDef",
    "ListQuickResponsesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ManagedSourceConfigurationOutputTypeDef",
    "ManagedSourceConfigurationTypeDef",
    "ManagedSourceConfigurationUnionTypeDef",
    "ManualSearchAIAgentConfigurationOutputTypeDef",
    "ManualSearchAIAgentConfigurationTypeDef",
    "ManualSearchAIAgentConfigurationUnionTypeDef",
    "MessageDataTypeDef",
    "MessageInputTypeDef",
    "MessageOutputTypeDef",
    "MessageTemplateAttachmentTypeDef",
    "MessageTemplateAttributesOutputTypeDef",
    "MessageTemplateAttributesTypeDef",
    "MessageTemplateBodyContentProviderTypeDef",
    "MessageTemplateContentProviderOutputTypeDef",
    "MessageTemplateContentProviderTypeDef",
    "MessageTemplateDataTypeDef",
    "MessageTemplateFilterFieldTypeDef",
    "MessageTemplateOrderFieldTypeDef",
    "MessageTemplateQueryFieldTypeDef",
    "MessageTemplateSearchExpressionTypeDef",
    "MessageTemplateSearchResultDataTypeDef",
    "MessageTemplateSummaryTypeDef",
    "MessageTemplateVersionSummaryTypeDef",
    "NotifyRecommendationsReceivedErrorTypeDef",
    "NotifyRecommendationsReceivedRequestRequestTypeDef",
    "NotifyRecommendationsReceivedResponseTypeDef",
    "OrConditionOutputTypeDef",
    "OrConditionTypeDef",
    "OrConditionUnionTypeDef",
    "PaginatorConfigTypeDef",
    "ParsingConfigurationTypeDef",
    "ParsingPromptTypeDef",
    "PutFeedbackRequestRequestTypeDef",
    "PutFeedbackResponseTypeDef",
    "QueryAssistantRequestQueryAssistantPaginateTypeDef",
    "QueryAssistantRequestRequestTypeDef",
    "QueryAssistantResponsePaginatorTypeDef",
    "QueryAssistantResponseTypeDef",
    "QueryConditionItemTypeDef",
    "QueryConditionTypeDef",
    "QueryInputDataTypeDef",
    "QueryRecommendationTriggerDataTypeDef",
    "QueryTextInputDataTypeDef",
    "QuickResponseContentProviderTypeDef",
    "QuickResponseContentsTypeDef",
    "QuickResponseDataProviderTypeDef",
    "QuickResponseDataTypeDef",
    "QuickResponseFilterFieldTypeDef",
    "QuickResponseOrderFieldTypeDef",
    "QuickResponseQueryFieldTypeDef",
    "QuickResponseSearchExpressionTypeDef",
    "QuickResponseSearchResultDataTypeDef",
    "QuickResponseSummaryTypeDef",
    "RankingDataTypeDef",
    "RecommendationDataTypeDef",
    "RecommendationTriggerDataTypeDef",
    "RecommendationTriggerTypeDef",
    "RemoveAssistantAIAgentRequestRequestTypeDef",
    "RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef",
    "RenderMessageTemplateRequestRequestTypeDef",
    "RenderMessageTemplateResponseTypeDef",
    "RenderingConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "ResultDataPaginatorTypeDef",
    "ResultDataTypeDef",
    "RuntimeSessionDataTypeDef",
    "RuntimeSessionDataValueTypeDef",
    "SMSMessageTemplateContentBodyTypeDef",
    "SMSMessageTemplateContentTypeDef",
    "SearchContentRequestRequestTypeDef",
    "SearchContentRequestSearchContentPaginateTypeDef",
    "SearchContentResponseTypeDef",
    "SearchExpressionTypeDef",
    "SearchMessageTemplatesRequestRequestTypeDef",
    "SearchMessageTemplatesRequestSearchMessageTemplatesPaginateTypeDef",
    "SearchMessageTemplatesResponseTypeDef",
    "SearchQuickResponsesRequestRequestTypeDef",
    "SearchQuickResponsesRequestSearchQuickResponsesPaginateTypeDef",
    "SearchQuickResponsesResponseTypeDef",
    "SearchSessionsRequestRequestTypeDef",
    "SearchSessionsRequestSearchSessionsPaginateTypeDef",
    "SearchSessionsResponseTypeDef",
    "SeedUrlTypeDef",
    "SelfServiceAIAgentConfigurationOutputTypeDef",
    "SelfServiceAIAgentConfigurationTypeDef",
    "SelfServiceAIAgentConfigurationUnionTypeDef",
    "SelfServiceConversationHistoryTypeDef",
    "SemanticChunkingConfigurationTypeDef",
    "SendMessageRequestRequestTypeDef",
    "SendMessageResponseTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "SessionDataTypeDef",
    "SessionIntegrationConfigurationTypeDef",
    "SessionSummaryTypeDef",
    "SourceConfigurationOutputTypeDef",
    "SourceConfigurationTypeDef",
    "SourceContentDataDetailsTypeDef",
    "StartContentUploadRequestRequestTypeDef",
    "StartContentUploadResponseTypeDef",
    "StartImportJobRequestRequestTypeDef",
    "StartImportJobResponseTypeDef",
    "SystemAttributesTypeDef",
    "SystemEndpointAttributesTypeDef",
    "TagConditionTypeDef",
    "TagFilterOutputTypeDef",
    "TagFilterTypeDef",
    "TagFilterUnionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TextDataTypeDef",
    "TextFullAIPromptEditTemplateConfigurationTypeDef",
    "TextMessageTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAIAgentRequestRequestTypeDef",
    "UpdateAIAgentResponseTypeDef",
    "UpdateAIGuardrailRequestRequestTypeDef",
    "UpdateAIGuardrailResponseTypeDef",
    "UpdateAIPromptRequestRequestTypeDef",
    "UpdateAIPromptResponseTypeDef",
    "UpdateAssistantAIAgentRequestRequestTypeDef",
    "UpdateAssistantAIAgentResponseTypeDef",
    "UpdateContentRequestRequestTypeDef",
    "UpdateContentResponseTypeDef",
    "UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef",
    "UpdateKnowledgeBaseTemplateUriResponseTypeDef",
    "UpdateMessageTemplateMetadataRequestRequestTypeDef",
    "UpdateMessageTemplateMetadataResponseTypeDef",
    "UpdateMessageTemplateRequestRequestTypeDef",
    "UpdateMessageTemplateResponseTypeDef",
    "UpdateQuickResponseRequestRequestTypeDef",
    "UpdateQuickResponseResponseTypeDef",
    "UpdateSessionDataRequestRequestTypeDef",
    "UpdateSessionDataResponseTypeDef",
    "UpdateSessionRequestRequestTypeDef",
    "UpdateSessionResponseTypeDef",
    "UrlConfigurationOutputTypeDef",
    "UrlConfigurationTypeDef",
    "UrlConfigurationUnionTypeDef",
    "VectorIngestionConfigurationOutputTypeDef",
    "VectorIngestionConfigurationTypeDef",
    "WebCrawlerConfigurationOutputTypeDef",
    "WebCrawlerConfigurationTypeDef",
    "WebCrawlerConfigurationUnionTypeDef",
    "WebCrawlerLimitsTypeDef",
)


class AIAgentConfigurationDataTypeDef(TypedDict):
    aiAgentId: str


GuardrailContentFilterConfigTypeDef = TypedDict(
    "GuardrailContentFilterConfigTypeDef",
    {
        "inputStrength": GuardrailFilterStrengthType,
        "outputStrength": GuardrailFilterStrengthType,
        "type": GuardrailContentFilterTypeType,
    },
)
GuardrailContextualGroundingFilterConfigTypeDef = TypedDict(
    "GuardrailContextualGroundingFilterConfigTypeDef",
    {
        "threshold": float,
        "type": GuardrailContextualGroundingFilterTypeType,
    },
)
GuardrailPiiEntityConfigTypeDef = TypedDict(
    "GuardrailPiiEntityConfigTypeDef",
    {
        "action": GuardrailSensitiveInformationActionType,
        "type": GuardrailPiiEntityTypeType,
    },
)


class GuardrailRegexConfigTypeDef(TypedDict):
    action: GuardrailSensitiveInformationActionType
    name: str
    pattern: str
    description: NotRequired[str]


class AIGuardrailSummaryTypeDef(TypedDict):
    aiGuardrailArn: str
    aiGuardrailId: str
    assistantArn: str
    assistantId: str
    name: str
    visibilityStatus: VisibilityStatusType
    description: NotRequired[str]
    modifiedTime: NotRequired[datetime]
    status: NotRequired[StatusType]
    tags: NotRequired[Dict[str, str]]


GuardrailTopicConfigOutputTypeDef = TypedDict(
    "GuardrailTopicConfigOutputTypeDef",
    {
        "definition": str,
        "name": str,
        "type": Literal["DENY"],
        "examples": NotRequired[List[str]],
    },
)
GuardrailManagedWordsConfigTypeDef = TypedDict(
    "GuardrailManagedWordsConfigTypeDef",
    {
        "type": Literal["PROFANITY"],
    },
)


class GuardrailWordConfigTypeDef(TypedDict):
    text: str


AIPromptSummaryTypeDef = TypedDict(
    "AIPromptSummaryTypeDef",
    {
        "aiPromptArn": str,
        "aiPromptId": str,
        "apiFormat": AIPromptAPIFormatType,
        "assistantArn": str,
        "assistantId": str,
        "modelId": str,
        "name": str,
        "templateType": Literal["TEXT"],
        "type": AIPromptTypeType,
        "visibilityStatus": VisibilityStatusType,
        "description": NotRequired[str],
        "modifiedTime": NotRequired[datetime],
        "origin": NotRequired[OriginType],
        "status": NotRequired[StatusType],
        "tags": NotRequired[Dict[str, str]],
    },
)


class TextFullAIPromptEditTemplateConfigurationTypeDef(TypedDict):
    text: str


class ActivateMessageTemplateRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    versionNumber: int


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AgentAttributesTypeDef(TypedDict):
    firstName: NotRequired[str]
    lastName: NotRequired[str]


class AmazonConnectGuideAssociationDataTypeDef(TypedDict):
    flowId: NotRequired[str]


class AppIntegrationsConfigurationOutputTypeDef(TypedDict):
    appIntegrationArn: str
    objectFields: NotRequired[List[str]]


class AppIntegrationsConfigurationTypeDef(TypedDict):
    appIntegrationArn: str
    objectFields: NotRequired[Sequence[str]]


class AssistantAssociationInputDataTypeDef(TypedDict):
    knowledgeBaseId: NotRequired[str]


class KnowledgeBaseAssociationDataTypeDef(TypedDict):
    knowledgeBaseArn: NotRequired[str]
    knowledgeBaseId: NotRequired[str]


AssistantCapabilityConfigurationTypeDef = TypedDict(
    "AssistantCapabilityConfigurationTypeDef",
    {
        "type": NotRequired[AssistantCapabilityTypeType],
    },
)


class AssistantIntegrationConfigurationTypeDef(TypedDict):
    topicIntegrationArn: NotRequired[str]


class ServerSideEncryptionConfigurationTypeDef(TypedDict):
    kmsKeyId: NotRequired[str]


class ParsingPromptTypeDef(TypedDict):
    parsingPromptText: str


class FixedSizeChunkingConfigurationTypeDef(TypedDict):
    maxTokens: int
    overlapPercentage: int


class SemanticChunkingConfigurationTypeDef(TypedDict):
    breakpointPercentileThreshold: int
    bufferSize: int
    maxTokens: int


class CitationSpanTypeDef(TypedDict):
    beginOffsetInclusive: NotRequired[int]
    endOffsetExclusive: NotRequired[int]


class ConnectConfigurationTypeDef(TypedDict):
    instanceId: NotRequired[str]


class RankingDataTypeDef(TypedDict):
    relevanceLevel: NotRequired[RelevanceLevelType]
    relevanceScore: NotRequired[float]


class ContentDataTypeDef(TypedDict):
    contentArn: str
    contentId: str
    contentType: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    metadata: Dict[str, str]
    name: str
    revisionId: str
    status: ContentStatusType
    title: str
    url: str
    urlExpiry: datetime
    linkOutUri: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class GenerativeContentFeedbackDataTypeDef(TypedDict):
    relevance: RelevanceType


class ContentReferenceTypeDef(TypedDict):
    contentArn: NotRequired[str]
    contentId: NotRequired[str]
    knowledgeBaseArn: NotRequired[str]
    knowledgeBaseId: NotRequired[str]
    referenceType: NotRequired[ReferenceTypeType]
    sourceURL: NotRequired[str]


class ContentSummaryTypeDef(TypedDict):
    contentArn: str
    contentId: str
    contentType: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    metadata: Dict[str, str]
    name: str
    revisionId: str
    status: ContentStatusType
    title: str
    tags: NotRequired[Dict[str, str]]


class SelfServiceConversationHistoryTypeDef(TypedDict):
    turnNumber: int
    botResponse: NotRequired[str]
    inputTranscript: NotRequired[str]


class ConversationStateTypeDef(TypedDict):
    status: ConversationStatusType
    reason: NotRequired[ConversationStatusReasonType]


TimestampTypeDef = Union[datetime, str]


class CreateContentRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    name: str
    uploadId: str
    clientToken: NotRequired[str]
    metadata: NotRequired[Mapping[str, str]]
    overrideLinkOutUri: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    title: NotRequired[str]


class RenderingConfigurationTypeDef(TypedDict):
    templateUri: NotRequired[str]


class CreateMessageTemplateAttachmentRequestRequestTypeDef(TypedDict):
    body: str
    contentDisposition: Literal["ATTACHMENT"]
    knowledgeBaseId: str
    messageTemplateId: str
    name: str
    clientToken: NotRequired[str]


class MessageTemplateAttachmentTypeDef(TypedDict):
    attachmentId: str
    contentDisposition: Literal["ATTACHMENT"]
    name: str
    uploadedTime: datetime
    url: str
    urlExpiry: datetime


class GroupingConfigurationTypeDef(TypedDict):
    criteria: NotRequired[str]
    values: NotRequired[Sequence[str]]


class CreateMessageTemplateVersionRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    messageTemplateContentSha256: NotRequired[str]


class QuickResponseDataProviderTypeDef(TypedDict):
    content: NotRequired[str]


class CustomerProfileAttributesOutputTypeDef(TypedDict):
    accountNumber: NotRequired[str]
    additionalInformation: NotRequired[str]
    address1: NotRequired[str]
    address2: NotRequired[str]
    address3: NotRequired[str]
    address4: NotRequired[str]
    billingAddress1: NotRequired[str]
    billingAddress2: NotRequired[str]
    billingAddress3: NotRequired[str]
    billingAddress4: NotRequired[str]
    billingCity: NotRequired[str]
    billingCountry: NotRequired[str]
    billingCounty: NotRequired[str]
    billingPostalCode: NotRequired[str]
    billingProvince: NotRequired[str]
    billingState: NotRequired[str]
    birthDate: NotRequired[str]
    businessEmailAddress: NotRequired[str]
    businessName: NotRequired[str]
    businessPhoneNumber: NotRequired[str]
    city: NotRequired[str]
    country: NotRequired[str]
    county: NotRequired[str]
    custom: NotRequired[Dict[str, str]]
    emailAddress: NotRequired[str]
    firstName: NotRequired[str]
    gender: NotRequired[str]
    homePhoneNumber: NotRequired[str]
    lastName: NotRequired[str]
    mailingAddress1: NotRequired[str]
    mailingAddress2: NotRequired[str]
    mailingAddress3: NotRequired[str]
    mailingAddress4: NotRequired[str]
    mailingCity: NotRequired[str]
    mailingCountry: NotRequired[str]
    mailingCounty: NotRequired[str]
    mailingPostalCode: NotRequired[str]
    mailingProvince: NotRequired[str]
    mailingState: NotRequired[str]
    middleName: NotRequired[str]
    mobilePhoneNumber: NotRequired[str]
    partyType: NotRequired[str]
    phoneNumber: NotRequired[str]
    postalCode: NotRequired[str]
    profileARN: NotRequired[str]
    profileId: NotRequired[str]
    province: NotRequired[str]
    shippingAddress1: NotRequired[str]
    shippingAddress2: NotRequired[str]
    shippingAddress3: NotRequired[str]
    shippingAddress4: NotRequired[str]
    shippingCity: NotRequired[str]
    shippingCountry: NotRequired[str]
    shippingCounty: NotRequired[str]
    shippingPostalCode: NotRequired[str]
    shippingProvince: NotRequired[str]
    shippingState: NotRequired[str]
    state: NotRequired[str]


class CustomerProfileAttributesTypeDef(TypedDict):
    accountNumber: NotRequired[str]
    additionalInformation: NotRequired[str]
    address1: NotRequired[str]
    address2: NotRequired[str]
    address3: NotRequired[str]
    address4: NotRequired[str]
    billingAddress1: NotRequired[str]
    billingAddress2: NotRequired[str]
    billingAddress3: NotRequired[str]
    billingAddress4: NotRequired[str]
    billingCity: NotRequired[str]
    billingCountry: NotRequired[str]
    billingCounty: NotRequired[str]
    billingPostalCode: NotRequired[str]
    billingProvince: NotRequired[str]
    billingState: NotRequired[str]
    birthDate: NotRequired[str]
    businessEmailAddress: NotRequired[str]
    businessName: NotRequired[str]
    businessPhoneNumber: NotRequired[str]
    city: NotRequired[str]
    country: NotRequired[str]
    county: NotRequired[str]
    custom: NotRequired[Mapping[str, str]]
    emailAddress: NotRequired[str]
    firstName: NotRequired[str]
    gender: NotRequired[str]
    homePhoneNumber: NotRequired[str]
    lastName: NotRequired[str]
    mailingAddress1: NotRequired[str]
    mailingAddress2: NotRequired[str]
    mailingAddress3: NotRequired[str]
    mailingAddress4: NotRequired[str]
    mailingCity: NotRequired[str]
    mailingCountry: NotRequired[str]
    mailingCounty: NotRequired[str]
    mailingPostalCode: NotRequired[str]
    mailingProvince: NotRequired[str]
    mailingState: NotRequired[str]
    middleName: NotRequired[str]
    mobilePhoneNumber: NotRequired[str]
    partyType: NotRequired[str]
    phoneNumber: NotRequired[str]
    postalCode: NotRequired[str]
    profileARN: NotRequired[str]
    profileId: NotRequired[str]
    province: NotRequired[str]
    shippingAddress1: NotRequired[str]
    shippingAddress2: NotRequired[str]
    shippingAddress3: NotRequired[str]
    shippingAddress4: NotRequired[str]
    shippingCity: NotRequired[str]
    shippingCountry: NotRequired[str]
    shippingCounty: NotRequired[str]
    shippingPostalCode: NotRequired[str]
    shippingProvince: NotRequired[str]
    shippingState: NotRequired[str]
    state: NotRequired[str]


class IntentDetectedDataDetailsTypeDef(TypedDict):
    intent: str
    intentId: str


class GenerativeReferenceTypeDef(TypedDict):
    generationId: NotRequired[str]
    modelId: NotRequired[str]


class DeactivateMessageTemplateRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    versionNumber: int


class DeleteAIAgentRequestRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str


class DeleteAIAgentVersionRequestRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    versionNumber: int


class DeleteAIGuardrailRequestRequestTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str


class DeleteAIGuardrailVersionRequestRequestTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str
    versionNumber: int


class DeleteAIPromptRequestRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str


class DeleteAIPromptVersionRequestRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    versionNumber: int


class DeleteAssistantAssociationRequestRequestTypeDef(TypedDict):
    assistantAssociationId: str
    assistantId: str


class DeleteAssistantRequestRequestTypeDef(TypedDict):
    assistantId: str


class DeleteContentAssociationRequestRequestTypeDef(TypedDict):
    contentAssociationId: str
    contentId: str
    knowledgeBaseId: str


class DeleteContentRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str


class DeleteImportJobRequestRequestTypeDef(TypedDict):
    importJobId: str
    knowledgeBaseId: str


class DeleteKnowledgeBaseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str


class DeleteMessageTemplateAttachmentRequestRequestTypeDef(TypedDict):
    attachmentId: str
    knowledgeBaseId: str
    messageTemplateId: str


class DeleteMessageTemplateRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str


class DeleteQuickResponseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    quickResponseId: str


class HighlightTypeDef(TypedDict):
    beginOffsetInclusive: NotRequired[int]
    endOffsetExclusive: NotRequired[int]


class EmailHeaderTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]


class MessageTemplateBodyContentProviderTypeDef(TypedDict):
    content: NotRequired[str]


class GroupingConfigurationOutputTypeDef(TypedDict):
    criteria: NotRequired[str]
    values: NotRequired[List[str]]


FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "field": Literal["NAME"],
        "operator": Literal["EQUALS"],
        "value": str,
    },
)


class GetAIAgentRequestRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str


class GetAIGuardrailRequestRequestTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str


class GetAIPromptRequestRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str


class GetAssistantAssociationRequestRequestTypeDef(TypedDict):
    assistantAssociationId: str
    assistantId: str


class GetAssistantRequestRequestTypeDef(TypedDict):
    assistantId: str


class GetContentAssociationRequestRequestTypeDef(TypedDict):
    contentAssociationId: str
    contentId: str
    knowledgeBaseId: str


class GetContentRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str


class GetContentSummaryRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str


class GetImportJobRequestRequestTypeDef(TypedDict):
    importJobId: str
    knowledgeBaseId: str


class GetKnowledgeBaseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str


class GetMessageTemplateRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str


class GetNextMessageRequestRequestTypeDef(TypedDict):
    assistantId: str
    nextMessageToken: str
    sessionId: str


class GetQuickResponseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    quickResponseId: str


class GetRecommendationsRequestRequestTypeDef(TypedDict):
    assistantId: str
    sessionId: str
    maxResults: NotRequired[int]
    waitTimeSeconds: NotRequired[int]


class GetSessionRequestRequestTypeDef(TypedDict):
    assistantId: str
    sessionId: str


GuardrailTopicConfigTypeDef = TypedDict(
    "GuardrailTopicConfigTypeDef",
    {
        "definition": str,
        "name": str,
        "type": Literal["DENY"],
        "examples": NotRequired[Sequence[str]],
    },
)


class HierarchicalChunkingLevelConfigurationTypeDef(TypedDict):
    maxTokens: int


class IntentInputDataTypeDef(TypedDict):
    intentId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAIAgentVersionsRequestRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    origin: NotRequired[OriginType]


class ListAIAgentsRequestRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    origin: NotRequired[OriginType]


class ListAIGuardrailVersionsRequestRequestTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListAIGuardrailsRequestRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListAIPromptVersionsRequestRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    origin: NotRequired[OriginType]


class ListAIPromptsRequestRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    origin: NotRequired[OriginType]


class ListAssistantAssociationsRequestRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListAssistantsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListContentAssociationsRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListContentsRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListImportJobsRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListKnowledgeBasesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListMessageTemplateVersionsRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class MessageTemplateVersionSummaryTypeDef(TypedDict):
    channelSubtype: ChannelSubtypeType
    isActive: bool
    knowledgeBaseArn: str
    knowledgeBaseId: str
    messageTemplateArn: str
    messageTemplateId: str
    name: str
    versionNumber: int


class ListMessageTemplatesRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class MessageTemplateSummaryTypeDef(TypedDict):
    channelSubtype: ChannelSubtypeType
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedBy: str
    lastModifiedTime: datetime
    messageTemplateArn: str
    messageTemplateId: str
    name: str
    activeVersionNumber: NotRequired[int]
    description: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class ListMessagesRequestRequestTypeDef(TypedDict):
    assistantId: str
    sessionId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListQuickResponsesRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class QuickResponseSummaryTypeDef(TypedDict):
    contentType: str
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    name: str
    quickResponseArn: str
    quickResponseId: str
    status: QuickResponseStatusType
    channels: NotRequired[List[str]]
    description: NotRequired[str]
    isActive: NotRequired[bool]
    lastModifiedBy: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class TextMessageTypeDef(TypedDict):
    value: NotRequired[str]


MessageTemplateFilterFieldTypeDef = TypedDict(
    "MessageTemplateFilterFieldTypeDef",
    {
        "name": str,
        "operator": MessageTemplateFilterOperatorType,
        "includeNoExistence": NotRequired[bool],
        "values": NotRequired[Sequence[str]],
    },
)


class MessageTemplateOrderFieldTypeDef(TypedDict):
    name: str
    order: NotRequired[OrderType]


MessageTemplateQueryFieldTypeDef = TypedDict(
    "MessageTemplateQueryFieldTypeDef",
    {
        "name": str,
        "operator": MessageTemplateQueryOperatorType,
        "values": Sequence[str],
        "allowFuzziness": NotRequired[bool],
        "priority": NotRequired[PriorityType],
    },
)


class NotifyRecommendationsReceivedErrorTypeDef(TypedDict):
    message: NotRequired[str]
    recommendationId: NotRequired[str]


class NotifyRecommendationsReceivedRequestRequestTypeDef(TypedDict):
    assistantId: str
    recommendationIds: Sequence[str]
    sessionId: str


class TagConditionTypeDef(TypedDict):
    key: str
    value: NotRequired[str]


class QueryConditionItemTypeDef(TypedDict):
    comparator: Literal["EQUALS"]
    field: Literal["RESULT_TYPE"]
    value: str


class QueryTextInputDataTypeDef(TypedDict):
    text: str


class QueryRecommendationTriggerDataTypeDef(TypedDict):
    text: NotRequired[str]


class QuickResponseContentProviderTypeDef(TypedDict):
    content: NotRequired[str]


QuickResponseFilterFieldTypeDef = TypedDict(
    "QuickResponseFilterFieldTypeDef",
    {
        "name": str,
        "operator": QuickResponseFilterOperatorType,
        "includeNoExistence": NotRequired[bool],
        "values": NotRequired[Sequence[str]],
    },
)


class QuickResponseOrderFieldTypeDef(TypedDict):
    name: str
    order: NotRequired[OrderType]


QuickResponseQueryFieldTypeDef = TypedDict(
    "QuickResponseQueryFieldTypeDef",
    {
        "name": str,
        "operator": QuickResponseQueryOperatorType,
        "values": Sequence[str],
        "allowFuzziness": NotRequired[bool],
        "priority": NotRequired[PriorityType],
    },
)


class RemoveAssistantAIAgentRequestRequestTypeDef(TypedDict):
    aiAgentType: AIAgentTypeType
    assistantId: str


class RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str


class RuntimeSessionDataValueTypeDef(TypedDict):
    stringValue: NotRequired[str]


class SessionSummaryTypeDef(TypedDict):
    assistantArn: str
    assistantId: str
    sessionArn: str
    sessionId: str


class SeedUrlTypeDef(TypedDict):
    url: NotRequired[str]


class SessionIntegrationConfigurationTypeDef(TypedDict):
    topicIntegrationArn: NotRequired[str]


class StartContentUploadRequestRequestTypeDef(TypedDict):
    contentType: str
    knowledgeBaseId: str
    presignedUrlTimeToLive: NotRequired[int]


class SystemEndpointAttributesTypeDef(TypedDict):
    address: NotRequired[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateContentRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str
    metadata: NotRequired[Mapping[str, str]]
    overrideLinkOutUri: NotRequired[str]
    removeOverrideLinkOutUri: NotRequired[bool]
    revisionId: NotRequired[str]
    title: NotRequired[str]
    uploadId: NotRequired[str]


class UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    templateUri: str


class WebCrawlerLimitsTypeDef(TypedDict):
    rateLimit: NotRequired[int]


class UpdateAssistantAIAgentRequestRequestTypeDef(TypedDict):
    aiAgentType: AIAgentTypeType
    assistantId: str
    configuration: AIAgentConfigurationDataTypeDef


class AIGuardrailContentPolicyConfigOutputTypeDef(TypedDict):
    filtersConfig: List[GuardrailContentFilterConfigTypeDef]


class AIGuardrailContentPolicyConfigTypeDef(TypedDict):
    filtersConfig: Sequence[GuardrailContentFilterConfigTypeDef]


class AIGuardrailContextualGroundingPolicyConfigOutputTypeDef(TypedDict):
    filtersConfig: List[GuardrailContextualGroundingFilterConfigTypeDef]


class AIGuardrailContextualGroundingPolicyConfigTypeDef(TypedDict):
    filtersConfig: Sequence[GuardrailContextualGroundingFilterConfigTypeDef]


class AIGuardrailSensitiveInformationPolicyConfigOutputTypeDef(TypedDict):
    piiEntitiesConfig: NotRequired[List[GuardrailPiiEntityConfigTypeDef]]
    regexesConfig: NotRequired[List[GuardrailRegexConfigTypeDef]]


class AIGuardrailSensitiveInformationPolicyConfigTypeDef(TypedDict):
    piiEntitiesConfig: NotRequired[Sequence[GuardrailPiiEntityConfigTypeDef]]
    regexesConfig: NotRequired[Sequence[GuardrailRegexConfigTypeDef]]


class AIGuardrailVersionSummaryTypeDef(TypedDict):
    aiGuardrailSummary: NotRequired[AIGuardrailSummaryTypeDef]
    versionNumber: NotRequired[int]


class AIGuardrailTopicPolicyConfigOutputTypeDef(TypedDict):
    topicsConfig: List[GuardrailTopicConfigOutputTypeDef]


class AIGuardrailWordPolicyConfigOutputTypeDef(TypedDict):
    managedWordListsConfig: NotRequired[List[GuardrailManagedWordsConfigTypeDef]]
    wordsConfig: NotRequired[List[GuardrailWordConfigTypeDef]]


class AIGuardrailWordPolicyConfigTypeDef(TypedDict):
    managedWordListsConfig: NotRequired[Sequence[GuardrailManagedWordsConfigTypeDef]]
    wordsConfig: NotRequired[Sequence[GuardrailWordConfigTypeDef]]


class AIPromptVersionSummaryTypeDef(TypedDict):
    aiPromptSummary: NotRequired[AIPromptSummaryTypeDef]
    versionNumber: NotRequired[int]


class AIPromptTemplateConfigurationTypeDef(TypedDict):
    textFullAIPromptEditTemplateConfiguration: NotRequired[
        TextFullAIPromptEditTemplateConfigurationTypeDef
    ]


class ActivateMessageTemplateResponseTypeDef(TypedDict):
    messageTemplateArn: str
    messageTemplateId: str
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeactivateMessageTemplateResponseTypeDef(TypedDict):
    messageTemplateArn: str
    messageTemplateId: str
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListAIGuardrailsResponseTypeDef(TypedDict):
    aiGuardrailSummaries: List[AIGuardrailSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAIPromptsResponseTypeDef(TypedDict):
    aiPromptSummaries: List[AIPromptSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class SendMessageResponseTypeDef(TypedDict):
    nextMessageToken: str
    requestMessageId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartContentUploadResponseTypeDef(TypedDict):
    headersToInclude: Dict[str, str]
    uploadId: str
    url: str
    urlExpiry: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ContentAssociationContentsTypeDef(TypedDict):
    amazonConnectGuideAssociation: NotRequired[AmazonConnectGuideAssociationDataTypeDef]


AppIntegrationsConfigurationUnionTypeDef = Union[
    AppIntegrationsConfigurationTypeDef, AppIntegrationsConfigurationOutputTypeDef
]


class CreateAssistantAssociationRequestRequestTypeDef(TypedDict):
    assistantId: str
    association: AssistantAssociationInputDataTypeDef
    associationType: Literal["KNOWLEDGE_BASE"]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class AssistantAssociationOutputDataTypeDef(TypedDict):
    knowledgeBaseAssociation: NotRequired[KnowledgeBaseAssociationDataTypeDef]


AssistantDataTypeDef = TypedDict(
    "AssistantDataTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
        "aiAgentConfiguration": NotRequired[Dict[AIAgentTypeType, AIAgentConfigurationDataTypeDef]],
        "capabilityConfiguration": NotRequired[AssistantCapabilityConfigurationTypeDef],
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[AssistantIntegrationConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
AssistantSummaryTypeDef = TypedDict(
    "AssistantSummaryTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
        "aiAgentConfiguration": NotRequired[Dict[AIAgentTypeType, AIAgentConfigurationDataTypeDef]],
        "capabilityConfiguration": NotRequired[AssistantCapabilityConfigurationTypeDef],
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[AssistantIntegrationConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateAssistantRequestRequestTypeDef = TypedDict(
    "CreateAssistantRequestRequestTypeDef",
    {
        "name": str,
        "type": Literal["AGENT"],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)


class BedrockFoundationModelConfigurationForParsingTypeDef(TypedDict):
    modelArn: str
    parsingPrompt: NotRequired[ParsingPromptTypeDef]


class ConfigurationTypeDef(TypedDict):
    connectConfiguration: NotRequired[ConnectConfigurationTypeDef]


class GenerativeDataDetailsPaginatorTypeDef(TypedDict):
    completion: str
    rankingData: RankingDataTypeDef
    references: List[Dict[str, Any]]


class GenerativeDataDetailsTypeDef(TypedDict):
    completion: str
    rankingData: RankingDataTypeDef
    references: List[Dict[str, Any]]


class CreateContentResponseTypeDef(TypedDict):
    content: ContentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetContentResponseTypeDef(TypedDict):
    content: ContentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateContentResponseTypeDef(TypedDict):
    content: ContentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ContentFeedbackDataTypeDef(TypedDict):
    generativeContentFeedbackData: NotRequired[GenerativeContentFeedbackDataTypeDef]


class GetContentSummaryResponseTypeDef(TypedDict):
    contentSummary: ContentSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListContentsResponseTypeDef(TypedDict):
    contentSummaries: List[ContentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SearchContentResponseTypeDef(TypedDict):
    contentSummaries: List[ContentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ConversationContextTypeDef(TypedDict):
    selfServiceConversationHistory: Sequence[SelfServiceConversationHistoryTypeDef]


class CreateAIAgentVersionRequestRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    clientToken: NotRequired[str]
    modifiedTime: NotRequired[TimestampTypeDef]


class CreateAIGuardrailVersionRequestRequestTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str
    clientToken: NotRequired[str]
    modifiedTime: NotRequired[TimestampTypeDef]


class CreateAIPromptVersionRequestRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    clientToken: NotRequired[str]
    modifiedTime: NotRequired[TimestampTypeDef]


class CreateMessageTemplateAttachmentResponseTypeDef(TypedDict):
    attachment: MessageTemplateAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMessageTemplateMetadataRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationTypeDef]
    name: NotRequired[str]


class CreateQuickResponseRequestRequestTypeDef(TypedDict):
    content: QuickResponseDataProviderTypeDef
    knowledgeBaseId: str
    name: str
    channels: NotRequired[Sequence[str]]
    clientToken: NotRequired[str]
    contentType: NotRequired[str]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    shortcutKey: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class UpdateQuickResponseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    quickResponseId: str
    channels: NotRequired[Sequence[str]]
    content: NotRequired[QuickResponseDataProviderTypeDef]
    contentType: NotRequired[str]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    name: NotRequired[str]
    removeDescription: NotRequired[bool]
    removeGroupingConfiguration: NotRequired[bool]
    removeShortcutKey: NotRequired[bool]
    shortcutKey: NotRequired[str]


CustomerProfileAttributesUnionTypeDef = Union[
    CustomerProfileAttributesTypeDef, CustomerProfileAttributesOutputTypeDef
]


class DataReferenceTypeDef(TypedDict):
    contentReference: NotRequired[ContentReferenceTypeDef]
    generativeReference: NotRequired[GenerativeReferenceTypeDef]


class DocumentTextTypeDef(TypedDict):
    highlights: NotRequired[List[HighlightTypeDef]]
    text: NotRequired[str]


class EmailMessageTemplateContentBodyTypeDef(TypedDict):
    html: NotRequired[MessageTemplateBodyContentProviderTypeDef]
    plainText: NotRequired[MessageTemplateBodyContentProviderTypeDef]


class SMSMessageTemplateContentBodyTypeDef(TypedDict):
    plainText: NotRequired[MessageTemplateBodyContentProviderTypeDef]


class MessageTemplateSearchResultDataTypeDef(TypedDict):
    channelSubtype: ChannelSubtypeType
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedBy: str
    lastModifiedTime: datetime
    messageTemplateArn: str
    messageTemplateId: str
    name: str
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    versionNumber: NotRequired[int]


class SearchExpressionTypeDef(TypedDict):
    filters: Sequence[FilterTypeDef]


GuardrailTopicConfigUnionTypeDef = Union[
    GuardrailTopicConfigTypeDef, GuardrailTopicConfigOutputTypeDef
]


class HierarchicalChunkingConfigurationOutputTypeDef(TypedDict):
    levelConfigurations: List[HierarchicalChunkingLevelConfigurationTypeDef]
    overlapTokens: int


class HierarchicalChunkingConfigurationTypeDef(TypedDict):
    levelConfigurations: Sequence[HierarchicalChunkingLevelConfigurationTypeDef]
    overlapTokens: int


class ListAIAgentVersionsRequestListAIAgentVersionsPaginateTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    origin: NotRequired[OriginType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAIAgentsRequestListAIAgentsPaginateTypeDef(TypedDict):
    assistantId: str
    origin: NotRequired[OriginType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAIGuardrailVersionsRequestListAIGuardrailVersionsPaginateTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAIGuardrailsRequestListAIGuardrailsPaginateTypeDef(TypedDict):
    assistantId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAIPromptVersionsRequestListAIPromptVersionsPaginateTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    origin: NotRequired[OriginType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAIPromptsRequestListAIPromptsPaginateTypeDef(TypedDict):
    assistantId: str
    origin: NotRequired[OriginType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef(TypedDict):
    assistantId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssistantsRequestListAssistantsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContentAssociationsRequestListContentAssociationsPaginateTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContentsRequestListContentsPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListImportJobsRequestListImportJobsPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMessageTemplateVersionsRequestListMessageTemplateVersionsPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMessageTemplatesRequestListMessageTemplatesPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMessagesRequestListMessagesPaginateTypeDef(TypedDict):
    assistantId: str
    sessionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListQuickResponsesRequestListQuickResponsesPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMessageTemplateVersionsResponseTypeDef(TypedDict):
    messageTemplateVersionSummaries: List[MessageTemplateVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListMessageTemplatesResponseTypeDef(TypedDict):
    messageTemplateSummaries: List[MessageTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListQuickResponsesResponseTypeDef(TypedDict):
    quickResponseSummaries: List[QuickResponseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class MessageDataTypeDef(TypedDict):
    text: NotRequired[TextMessageTypeDef]


class MessageTemplateSearchExpressionTypeDef(TypedDict):
    filters: NotRequired[Sequence[MessageTemplateFilterFieldTypeDef]]
    orderOnField: NotRequired[MessageTemplateOrderFieldTypeDef]
    queries: NotRequired[Sequence[MessageTemplateQueryFieldTypeDef]]


class NotifyRecommendationsReceivedResponseTypeDef(TypedDict):
    errors: List[NotifyRecommendationsReceivedErrorTypeDef]
    recommendationIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class OrConditionOutputTypeDef(TypedDict):
    andConditions: NotRequired[List[TagConditionTypeDef]]
    tagCondition: NotRequired[TagConditionTypeDef]


class OrConditionTypeDef(TypedDict):
    andConditions: NotRequired[Sequence[TagConditionTypeDef]]
    tagCondition: NotRequired[TagConditionTypeDef]


class QueryConditionTypeDef(TypedDict):
    single: NotRequired[QueryConditionItemTypeDef]


class QueryInputDataTypeDef(TypedDict):
    intentInputData: NotRequired[IntentInputDataTypeDef]
    queryTextInputData: NotRequired[QueryTextInputDataTypeDef]


class RecommendationTriggerDataTypeDef(TypedDict):
    query: NotRequired[QueryRecommendationTriggerDataTypeDef]


class QuickResponseContentsTypeDef(TypedDict):
    markdown: NotRequired[QuickResponseContentProviderTypeDef]
    plainText: NotRequired[QuickResponseContentProviderTypeDef]


class QuickResponseSearchExpressionTypeDef(TypedDict):
    filters: NotRequired[Sequence[QuickResponseFilterFieldTypeDef]]
    orderOnField: NotRequired[QuickResponseOrderFieldTypeDef]
    queries: NotRequired[Sequence[QuickResponseQueryFieldTypeDef]]


class RuntimeSessionDataTypeDef(TypedDict):
    key: str
    value: RuntimeSessionDataValueTypeDef


class SearchSessionsResponseTypeDef(TypedDict):
    sessionSummaries: List[SessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UrlConfigurationOutputTypeDef(TypedDict):
    seedUrls: NotRequired[List[SeedUrlTypeDef]]


class UrlConfigurationTypeDef(TypedDict):
    seedUrls: NotRequired[Sequence[SeedUrlTypeDef]]


class SystemAttributesTypeDef(TypedDict):
    customerEndpoint: NotRequired[SystemEndpointAttributesTypeDef]
    name: NotRequired[str]
    systemEndpoint: NotRequired[SystemEndpointAttributesTypeDef]


class ListAIGuardrailVersionsResponseTypeDef(TypedDict):
    aiGuardrailVersionSummaries: List[AIGuardrailVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AIGuardrailDataTypeDef(TypedDict):
    aiGuardrailArn: str
    aiGuardrailId: str
    assistantArn: str
    assistantId: str
    blockedInputMessaging: str
    blockedOutputsMessaging: str
    name: str
    visibilityStatus: VisibilityStatusType
    contentPolicyConfig: NotRequired[AIGuardrailContentPolicyConfigOutputTypeDef]
    contextualGroundingPolicyConfig: NotRequired[
        AIGuardrailContextualGroundingPolicyConfigOutputTypeDef
    ]
    description: NotRequired[str]
    modifiedTime: NotRequired[datetime]
    sensitiveInformationPolicyConfig: NotRequired[
        AIGuardrailSensitiveInformationPolicyConfigOutputTypeDef
    ]
    status: NotRequired[StatusType]
    tags: NotRequired[Dict[str, str]]
    topicPolicyConfig: NotRequired[AIGuardrailTopicPolicyConfigOutputTypeDef]
    wordPolicyConfig: NotRequired[AIGuardrailWordPolicyConfigOutputTypeDef]


class ListAIPromptVersionsResponseTypeDef(TypedDict):
    aiPromptVersionSummaries: List[AIPromptVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


AIPromptDataTypeDef = TypedDict(
    "AIPromptDataTypeDef",
    {
        "aiPromptArn": str,
        "aiPromptId": str,
        "apiFormat": AIPromptAPIFormatType,
        "assistantArn": str,
        "assistantId": str,
        "modelId": str,
        "name": str,
        "templateConfiguration": AIPromptTemplateConfigurationTypeDef,
        "templateType": Literal["TEXT"],
        "type": AIPromptTypeType,
        "visibilityStatus": VisibilityStatusType,
        "description": NotRequired[str],
        "modifiedTime": NotRequired[datetime],
        "origin": NotRequired[OriginType],
        "status": NotRequired[StatusType],
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateAIPromptRequestRequestTypeDef = TypedDict(
    "CreateAIPromptRequestRequestTypeDef",
    {
        "apiFormat": AIPromptAPIFormatType,
        "assistantId": str,
        "modelId": str,
        "name": str,
        "templateConfiguration": AIPromptTemplateConfigurationTypeDef,
        "templateType": Literal["TEXT"],
        "type": AIPromptTypeType,
        "visibilityStatus": VisibilityStatusType,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)


class UpdateAIPromptRequestRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    visibilityStatus: VisibilityStatusType
    clientToken: NotRequired[str]
    description: NotRequired[str]
    templateConfiguration: NotRequired[AIPromptTemplateConfigurationTypeDef]


class ContentAssociationDataTypeDef(TypedDict):
    associationData: ContentAssociationContentsTypeDef
    associationType: Literal["AMAZON_CONNECT_GUIDE"]
    contentArn: str
    contentAssociationArn: str
    contentAssociationId: str
    contentId: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    tags: NotRequired[Dict[str, str]]


class ContentAssociationSummaryTypeDef(TypedDict):
    associationData: ContentAssociationContentsTypeDef
    associationType: Literal["AMAZON_CONNECT_GUIDE"]
    contentArn: str
    contentAssociationArn: str
    contentAssociationId: str
    contentId: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    tags: NotRequired[Dict[str, str]]


class CreateContentAssociationRequestRequestTypeDef(TypedDict):
    association: ContentAssociationContentsTypeDef
    associationType: Literal["AMAZON_CONNECT_GUIDE"]
    contentId: str
    knowledgeBaseId: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class AssistantAssociationDataTypeDef(TypedDict):
    assistantArn: str
    assistantAssociationArn: str
    assistantAssociationId: str
    assistantId: str
    associationData: AssistantAssociationOutputDataTypeDef
    associationType: Literal["KNOWLEDGE_BASE"]
    tags: NotRequired[Dict[str, str]]


class AssistantAssociationSummaryTypeDef(TypedDict):
    assistantArn: str
    assistantAssociationArn: str
    assistantAssociationId: str
    assistantId: str
    associationData: AssistantAssociationOutputDataTypeDef
    associationType: Literal["KNOWLEDGE_BASE"]
    tags: NotRequired[Dict[str, str]]


class CreateAssistantResponseTypeDef(TypedDict):
    assistant: AssistantDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssistantResponseTypeDef(TypedDict):
    assistant: AssistantDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAssistantAIAgentResponseTypeDef(TypedDict):
    assistant: AssistantDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAssistantsResponseTypeDef(TypedDict):
    assistantSummaries: List[AssistantSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ParsingConfigurationTypeDef(TypedDict):
    parsingStrategy: Literal["BEDROCK_FOUNDATION_MODEL"]
    bedrockFoundationModelConfiguration: NotRequired[
        BedrockFoundationModelConfigurationForParsingTypeDef
    ]


class ExternalSourceConfigurationTypeDef(TypedDict):
    configuration: ConfigurationTypeDef
    source: Literal["AMAZON_CONNECT"]


class PutFeedbackRequestRequestTypeDef(TypedDict):
    assistantId: str
    contentFeedback: ContentFeedbackDataTypeDef
    targetId: str
    targetType: TargetTypeType


class PutFeedbackResponseTypeDef(TypedDict):
    assistantArn: str
    assistantId: str
    contentFeedback: ContentFeedbackDataTypeDef
    targetId: str
    targetType: TargetTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class DocumentTypeDef(TypedDict):
    contentReference: ContentReferenceTypeDef
    excerpt: NotRequired[DocumentTextTypeDef]
    title: NotRequired[DocumentTextTypeDef]


class TextDataTypeDef(TypedDict):
    excerpt: NotRequired[DocumentTextTypeDef]
    title: NotRequired[DocumentTextTypeDef]


class EmailMessageTemplateContentOutputTypeDef(TypedDict):
    body: NotRequired[EmailMessageTemplateContentBodyTypeDef]
    headers: NotRequired[List[EmailHeaderTypeDef]]
    subject: NotRequired[str]


class EmailMessageTemplateContentTypeDef(TypedDict):
    body: NotRequired[EmailMessageTemplateContentBodyTypeDef]
    headers: NotRequired[Sequence[EmailHeaderTypeDef]]
    subject: NotRequired[str]


class SMSMessageTemplateContentTypeDef(TypedDict):
    body: NotRequired[SMSMessageTemplateContentBodyTypeDef]


class SearchMessageTemplatesResponseTypeDef(TypedDict):
    results: List[MessageTemplateSearchResultDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SearchContentRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: SearchExpressionTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SearchContentRequestSearchContentPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: SearchExpressionTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchSessionsRequestRequestTypeDef(TypedDict):
    assistantId: str
    searchExpression: SearchExpressionTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SearchSessionsRequestSearchSessionsPaginateTypeDef(TypedDict):
    assistantId: str
    searchExpression: SearchExpressionTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class AIGuardrailTopicPolicyConfigTypeDef(TypedDict):
    topicsConfig: Sequence[GuardrailTopicConfigUnionTypeDef]


class ChunkingConfigurationOutputTypeDef(TypedDict):
    chunkingStrategy: ChunkingStrategyType
    fixedSizeChunkingConfiguration: NotRequired[FixedSizeChunkingConfigurationTypeDef]
    hierarchicalChunkingConfiguration: NotRequired[HierarchicalChunkingConfigurationOutputTypeDef]
    semanticChunkingConfiguration: NotRequired[SemanticChunkingConfigurationTypeDef]


HierarchicalChunkingConfigurationUnionTypeDef = Union[
    HierarchicalChunkingConfigurationTypeDef, HierarchicalChunkingConfigurationOutputTypeDef
]


class MessageInputTypeDef(TypedDict):
    value: MessageDataTypeDef


class MessageOutputTypeDef(TypedDict):
    messageId: str
    participant: ParticipantType
    timestamp: datetime
    value: MessageDataTypeDef


class SearchMessageTemplatesRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: MessageTemplateSearchExpressionTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SearchMessageTemplatesRequestSearchMessageTemplatesPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: MessageTemplateSearchExpressionTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class TagFilterOutputTypeDef(TypedDict):
    andConditions: NotRequired[List[TagConditionTypeDef]]
    orConditions: NotRequired[List[OrConditionOutputTypeDef]]
    tagCondition: NotRequired[TagConditionTypeDef]


OrConditionUnionTypeDef = Union[OrConditionTypeDef, OrConditionOutputTypeDef]


class QueryAssistantRequestQueryAssistantPaginateTypeDef(TypedDict):
    assistantId: str
    overrideKnowledgeBaseSearchType: NotRequired[KnowledgeBaseSearchTypeType]
    queryCondition: NotRequired[Sequence[QueryConditionTypeDef]]
    queryInputData: NotRequired[QueryInputDataTypeDef]
    queryText: NotRequired[str]
    sessionId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class QueryAssistantRequestRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    overrideKnowledgeBaseSearchType: NotRequired[KnowledgeBaseSearchTypeType]
    queryCondition: NotRequired[Sequence[QueryConditionTypeDef]]
    queryInputData: NotRequired[QueryInputDataTypeDef]
    queryText: NotRequired[str]
    sessionId: NotRequired[str]


RecommendationTriggerTypeDef = TypedDict(
    "RecommendationTriggerTypeDef",
    {
        "data": RecommendationTriggerDataTypeDef,
        "id": str,
        "recommendationIds": List[str],
        "source": RecommendationSourceTypeType,
        "type": RecommendationTriggerTypeType,
    },
)


class QuickResponseDataTypeDef(TypedDict):
    contentType: str
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    name: str
    quickResponseArn: str
    quickResponseId: str
    status: QuickResponseStatusType
    channels: NotRequired[List[str]]
    contents: NotRequired[QuickResponseContentsTypeDef]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    lastModifiedBy: NotRequired[str]
    shortcutKey: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class QuickResponseSearchResultDataTypeDef(TypedDict):
    contentType: str
    contents: QuickResponseContentsTypeDef
    createdTime: datetime
    isActive: bool
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    name: str
    quickResponseArn: str
    quickResponseId: str
    status: QuickResponseStatusType
    attributesInterpolated: NotRequired[List[str]]
    attributesNotInterpolated: NotRequired[List[str]]
    channels: NotRequired[List[str]]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    language: NotRequired[str]
    lastModifiedBy: NotRequired[str]
    shortcutKey: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class SearchQuickResponsesRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: QuickResponseSearchExpressionTypeDef
    attributes: NotRequired[Mapping[str, str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SearchQuickResponsesRequestSearchQuickResponsesPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: QuickResponseSearchExpressionTypeDef
    attributes: NotRequired[Mapping[str, str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class UpdateSessionDataRequestRequestTypeDef(TypedDict):
    assistantId: str
    data: Sequence[RuntimeSessionDataTypeDef]
    sessionId: str
    namespace: NotRequired[Literal["Custom"]]


class UpdateSessionDataResponseTypeDef(TypedDict):
    data: List[RuntimeSessionDataTypeDef]
    namespace: Literal["Custom"]
    sessionArn: str
    sessionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class WebCrawlerConfigurationOutputTypeDef(TypedDict):
    urlConfiguration: UrlConfigurationOutputTypeDef
    crawlerLimits: NotRequired[WebCrawlerLimitsTypeDef]
    exclusionFilters: NotRequired[List[str]]
    inclusionFilters: NotRequired[List[str]]
    scope: NotRequired[WebScopeTypeType]


UrlConfigurationUnionTypeDef = Union[UrlConfigurationTypeDef, UrlConfigurationOutputTypeDef]


class MessageTemplateAttributesOutputTypeDef(TypedDict):
    agentAttributes: NotRequired[AgentAttributesTypeDef]
    customAttributes: NotRequired[Dict[str, str]]
    customerProfileAttributes: NotRequired[CustomerProfileAttributesOutputTypeDef]
    systemAttributes: NotRequired[SystemAttributesTypeDef]


class MessageTemplateAttributesTypeDef(TypedDict):
    agentAttributes: NotRequired[AgentAttributesTypeDef]
    customAttributes: NotRequired[Mapping[str, str]]
    customerProfileAttributes: NotRequired[CustomerProfileAttributesUnionTypeDef]
    systemAttributes: NotRequired[SystemAttributesTypeDef]


class CreateAIGuardrailResponseTypeDef(TypedDict):
    aiGuardrail: AIGuardrailDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAIGuardrailVersionResponseTypeDef(TypedDict):
    aiGuardrail: AIGuardrailDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetAIGuardrailResponseTypeDef(TypedDict):
    aiGuardrail: AIGuardrailDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAIGuardrailResponseTypeDef(TypedDict):
    aiGuardrail: AIGuardrailDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAIPromptResponseTypeDef(TypedDict):
    aiPrompt: AIPromptDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAIPromptVersionResponseTypeDef(TypedDict):
    aiPrompt: AIPromptDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetAIPromptResponseTypeDef(TypedDict):
    aiPrompt: AIPromptDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAIPromptResponseTypeDef(TypedDict):
    aiPrompt: AIPromptDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContentAssociationResponseTypeDef(TypedDict):
    contentAssociation: ContentAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetContentAssociationResponseTypeDef(TypedDict):
    contentAssociation: ContentAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListContentAssociationsResponseTypeDef(TypedDict):
    contentAssociationSummaries: List[ContentAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateAssistantAssociationResponseTypeDef(TypedDict):
    assistantAssociation: AssistantAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssistantAssociationResponseTypeDef(TypedDict):
    assistantAssociation: AssistantAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAssistantAssociationsResponseTypeDef(TypedDict):
    assistantAssociationSummaries: List[AssistantAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ImportJobDataTypeDef(TypedDict):
    createdTime: datetime
    importJobId: str
    importJobType: Literal["QUICK_RESPONSES"]
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    status: ImportJobStatusType
    uploadId: str
    url: str
    urlExpiry: datetime
    externalSourceConfiguration: NotRequired[ExternalSourceConfigurationTypeDef]
    failedRecordReport: NotRequired[str]
    metadata: NotRequired[Dict[str, str]]


class ImportJobSummaryTypeDef(TypedDict):
    createdTime: datetime
    importJobId: str
    importJobType: Literal["QUICK_RESPONSES"]
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    status: ImportJobStatusType
    uploadId: str
    externalSourceConfiguration: NotRequired[ExternalSourceConfigurationTypeDef]
    metadata: NotRequired[Dict[str, str]]


class StartImportJobRequestRequestTypeDef(TypedDict):
    importJobType: Literal["QUICK_RESPONSES"]
    knowledgeBaseId: str
    uploadId: str
    clientToken: NotRequired[str]
    externalSourceConfiguration: NotRequired[ExternalSourceConfigurationTypeDef]
    metadata: NotRequired[Mapping[str, str]]


class ContentDataDetailsTypeDef(TypedDict):
    rankingData: RankingDataTypeDef
    textData: TextDataTypeDef


SourceContentDataDetailsTypeDef = TypedDict(
    "SourceContentDataDetailsTypeDef",
    {
        "id": str,
        "rankingData": RankingDataTypeDef,
        "textData": TextDataTypeDef,
        "type": Literal["KNOWLEDGE_CONTENT"],
        "citationSpan": NotRequired[CitationSpanTypeDef],
    },
)
EmailMessageTemplateContentUnionTypeDef = Union[
    EmailMessageTemplateContentTypeDef, EmailMessageTemplateContentOutputTypeDef
]


class MessageTemplateContentProviderOutputTypeDef(TypedDict):
    email: NotRequired[EmailMessageTemplateContentOutputTypeDef]
    sms: NotRequired[SMSMessageTemplateContentTypeDef]


class CreateAIGuardrailRequestRequestTypeDef(TypedDict):
    assistantId: str
    blockedInputMessaging: str
    blockedOutputsMessaging: str
    name: str
    visibilityStatus: VisibilityStatusType
    clientToken: NotRequired[str]
    contentPolicyConfig: NotRequired[AIGuardrailContentPolicyConfigTypeDef]
    contextualGroundingPolicyConfig: NotRequired[AIGuardrailContextualGroundingPolicyConfigTypeDef]
    description: NotRequired[str]
    sensitiveInformationPolicyConfig: NotRequired[
        AIGuardrailSensitiveInformationPolicyConfigTypeDef
    ]
    tags: NotRequired[Mapping[str, str]]
    topicPolicyConfig: NotRequired[AIGuardrailTopicPolicyConfigTypeDef]
    wordPolicyConfig: NotRequired[AIGuardrailWordPolicyConfigTypeDef]


class UpdateAIGuardrailRequestRequestTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str
    blockedInputMessaging: str
    blockedOutputsMessaging: str
    visibilityStatus: VisibilityStatusType
    clientToken: NotRequired[str]
    contentPolicyConfig: NotRequired[AIGuardrailContentPolicyConfigTypeDef]
    contextualGroundingPolicyConfig: NotRequired[AIGuardrailContextualGroundingPolicyConfigTypeDef]
    description: NotRequired[str]
    sensitiveInformationPolicyConfig: NotRequired[
        AIGuardrailSensitiveInformationPolicyConfigTypeDef
    ]
    topicPolicyConfig: NotRequired[AIGuardrailTopicPolicyConfigTypeDef]
    wordPolicyConfig: NotRequired[AIGuardrailWordPolicyConfigTypeDef]


class VectorIngestionConfigurationOutputTypeDef(TypedDict):
    chunkingConfiguration: NotRequired[ChunkingConfigurationOutputTypeDef]
    parsingConfiguration: NotRequired[ParsingConfigurationTypeDef]


class ChunkingConfigurationTypeDef(TypedDict):
    chunkingStrategy: ChunkingStrategyType
    fixedSizeChunkingConfiguration: NotRequired[FixedSizeChunkingConfigurationTypeDef]
    hierarchicalChunkingConfiguration: NotRequired[HierarchicalChunkingConfigurationUnionTypeDef]
    semanticChunkingConfiguration: NotRequired[SemanticChunkingConfigurationTypeDef]


SendMessageRequestRequestTypeDef = TypedDict(
    "SendMessageRequestRequestTypeDef",
    {
        "assistantId": str,
        "message": MessageInputTypeDef,
        "sessionId": str,
        "type": Literal["TEXT"],
        "clientToken": NotRequired[str],
        "conversationContext": NotRequired[ConversationContextTypeDef],
    },
)
GetNextMessageResponseTypeDef = TypedDict(
    "GetNextMessageResponseTypeDef",
    {
        "conversationSessionData": List[RuntimeSessionDataTypeDef],
        "conversationState": ConversationStateTypeDef,
        "nextMessageToken": str,
        "requestMessageId": str,
        "response": MessageOutputTypeDef,
        "type": Literal["TEXT"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListMessagesResponseTypeDef(TypedDict):
    messages: List[MessageOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class KnowledgeBaseAssociationConfigurationDataOutputTypeDef(TypedDict):
    contentTagFilter: NotRequired[TagFilterOutputTypeDef]
    maxResults: NotRequired[int]
    overrideKnowledgeBaseSearchType: NotRequired[KnowledgeBaseSearchTypeType]


class SessionDataTypeDef(TypedDict):
    name: str
    sessionArn: str
    sessionId: str
    aiAgentConfiguration: NotRequired[Dict[AIAgentTypeType, AIAgentConfigurationDataTypeDef]]
    description: NotRequired[str]
    integrationConfiguration: NotRequired[SessionIntegrationConfigurationTypeDef]
    tagFilter: NotRequired[TagFilterOutputTypeDef]
    tags: NotRequired[Dict[str, str]]


class TagFilterTypeDef(TypedDict):
    andConditions: NotRequired[Sequence[TagConditionTypeDef]]
    orConditions: NotRequired[Sequence[OrConditionUnionTypeDef]]
    tagCondition: NotRequired[TagConditionTypeDef]


class CreateQuickResponseResponseTypeDef(TypedDict):
    quickResponse: QuickResponseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetQuickResponseResponseTypeDef(TypedDict):
    quickResponse: QuickResponseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateQuickResponseResponseTypeDef(TypedDict):
    quickResponse: QuickResponseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchQuickResponsesResponseTypeDef(TypedDict):
    results: List[QuickResponseSearchResultDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ManagedSourceConfigurationOutputTypeDef(TypedDict):
    webCrawlerConfiguration: NotRequired[WebCrawlerConfigurationOutputTypeDef]


class WebCrawlerConfigurationTypeDef(TypedDict):
    urlConfiguration: UrlConfigurationUnionTypeDef
    crawlerLimits: NotRequired[WebCrawlerLimitsTypeDef]
    exclusionFilters: NotRequired[Sequence[str]]
    inclusionFilters: NotRequired[Sequence[str]]
    scope: NotRequired[WebScopeTypeType]


class RenderMessageTemplateRequestRequestTypeDef(TypedDict):
    attributes: MessageTemplateAttributesTypeDef
    knowledgeBaseId: str
    messageTemplateId: str


class GetImportJobResponseTypeDef(TypedDict):
    importJob: ImportJobDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartImportJobResponseTypeDef(TypedDict):
    importJob: ImportJobDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListImportJobsResponseTypeDef(TypedDict):
    importJobSummaries: List[ImportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DataDetailsPaginatorTypeDef(TypedDict):
    contentData: NotRequired[ContentDataDetailsTypeDef]
    generativeData: NotRequired[GenerativeDataDetailsPaginatorTypeDef]
    intentDetectedData: NotRequired[IntentDetectedDataDetailsTypeDef]
    sourceContentData: NotRequired[SourceContentDataDetailsTypeDef]


class DataDetailsTypeDef(TypedDict):
    contentData: NotRequired[ContentDataDetailsTypeDef]
    generativeData: NotRequired[GenerativeDataDetailsTypeDef]
    intentDetectedData: NotRequired[IntentDetectedDataDetailsTypeDef]
    sourceContentData: NotRequired[SourceContentDataDetailsTypeDef]


class MessageTemplateContentProviderTypeDef(TypedDict):
    email: NotRequired[EmailMessageTemplateContentUnionTypeDef]
    sms: NotRequired[SMSMessageTemplateContentTypeDef]


class ExtendedMessageTemplateDataTypeDef(TypedDict):
    channelSubtype: ChannelSubtypeType
    content: MessageTemplateContentProviderOutputTypeDef
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedBy: str
    lastModifiedTime: datetime
    messageTemplateArn: str
    messageTemplateContentSha256: str
    messageTemplateId: str
    name: str
    attachments: NotRequired[List[MessageTemplateAttachmentTypeDef]]
    attributeTypes: NotRequired[List[MessageTemplateAttributeTypeType]]
    defaultAttributes: NotRequired[MessageTemplateAttributesOutputTypeDef]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    versionNumber: NotRequired[int]


class MessageTemplateDataTypeDef(TypedDict):
    channelSubtype: ChannelSubtypeType
    content: MessageTemplateContentProviderOutputTypeDef
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedBy: str
    lastModifiedTime: datetime
    messageTemplateArn: str
    messageTemplateContentSha256: str
    messageTemplateId: str
    name: str
    attributeTypes: NotRequired[List[MessageTemplateAttributeTypeType]]
    defaultAttributes: NotRequired[MessageTemplateAttributesOutputTypeDef]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    language: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class RenderMessageTemplateResponseTypeDef(TypedDict):
    attachments: List[MessageTemplateAttachmentTypeDef]
    attributesNotInterpolated: List[str]
    content: MessageTemplateContentProviderOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ChunkingConfigurationUnionTypeDef = Union[
    ChunkingConfigurationTypeDef, ChunkingConfigurationOutputTypeDef
]


class AssociationConfigurationDataOutputTypeDef(TypedDict):
    knowledgeBaseAssociationConfigurationData: NotRequired[
        KnowledgeBaseAssociationConfigurationDataOutputTypeDef
    ]


class CreateSessionResponseTypeDef(TypedDict):
    session: SessionDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSessionResponseTypeDef(TypedDict):
    session: SessionDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSessionResponseTypeDef(TypedDict):
    session: SessionDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSessionRequestRequestTypeDef(TypedDict):
    assistantId: str
    name: str
    aiAgentConfiguration: NotRequired[Mapping[AIAgentTypeType, AIAgentConfigurationDataTypeDef]]
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tagFilter: NotRequired[TagFilterTypeDef]
    tags: NotRequired[Mapping[str, str]]


TagFilterUnionTypeDef = Union[TagFilterTypeDef, TagFilterOutputTypeDef]


class UpdateSessionRequestRequestTypeDef(TypedDict):
    assistantId: str
    sessionId: str
    aiAgentConfiguration: NotRequired[Mapping[AIAgentTypeType, AIAgentConfigurationDataTypeDef]]
    description: NotRequired[str]
    tagFilter: NotRequired[TagFilterTypeDef]


class SourceConfigurationOutputTypeDef(TypedDict):
    appIntegrations: NotRequired[AppIntegrationsConfigurationOutputTypeDef]
    managedSourceConfiguration: NotRequired[ManagedSourceConfigurationOutputTypeDef]


WebCrawlerConfigurationUnionTypeDef = Union[
    WebCrawlerConfigurationTypeDef, WebCrawlerConfigurationOutputTypeDef
]


class DataSummaryPaginatorTypeDef(TypedDict):
    details: DataDetailsPaginatorTypeDef
    reference: DataReferenceTypeDef


class DataSummaryTypeDef(TypedDict):
    details: DataDetailsTypeDef
    reference: DataReferenceTypeDef


class CreateMessageTemplateRequestRequestTypeDef(TypedDict):
    channelSubtype: ChannelSubtypeType
    content: MessageTemplateContentProviderTypeDef
    knowledgeBaseId: str
    name: str
    clientToken: NotRequired[str]
    defaultAttributes: NotRequired[MessageTemplateAttributesTypeDef]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationTypeDef]
    language: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class UpdateMessageTemplateRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    content: NotRequired[MessageTemplateContentProviderTypeDef]
    defaultAttributes: NotRequired[MessageTemplateAttributesTypeDef]
    language: NotRequired[str]


class CreateMessageTemplateVersionResponseTypeDef(TypedDict):
    messageTemplate: ExtendedMessageTemplateDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetMessageTemplateResponseTypeDef(TypedDict):
    messageTemplate: ExtendedMessageTemplateDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMessageTemplateResponseTypeDef(TypedDict):
    messageTemplate: MessageTemplateDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMessageTemplateMetadataResponseTypeDef(TypedDict):
    messageTemplate: MessageTemplateDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMessageTemplateResponseTypeDef(TypedDict):
    messageTemplate: MessageTemplateDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class VectorIngestionConfigurationTypeDef(TypedDict):
    chunkingConfiguration: NotRequired[ChunkingConfigurationUnionTypeDef]
    parsingConfiguration: NotRequired[ParsingConfigurationTypeDef]


class AssociationConfigurationOutputTypeDef(TypedDict):
    associationConfigurationData: NotRequired[AssociationConfigurationDataOutputTypeDef]
    associationId: NotRequired[str]
    associationType: NotRequired[Literal["KNOWLEDGE_BASE"]]


class KnowledgeBaseAssociationConfigurationDataTypeDef(TypedDict):
    contentTagFilter: NotRequired[TagFilterUnionTypeDef]
    maxResults: NotRequired[int]
    overrideKnowledgeBaseSearchType: NotRequired[KnowledgeBaseSearchTypeType]


class KnowledgeBaseDataTypeDef(TypedDict):
    knowledgeBaseArn: str
    knowledgeBaseId: str
    knowledgeBaseType: KnowledgeBaseTypeType
    name: str
    status: KnowledgeBaseStatusType
    description: NotRequired[str]
    ingestionFailureReasons: NotRequired[List[str]]
    ingestionStatus: NotRequired[SyncStatusType]
    lastContentModificationTime: NotRequired[datetime]
    renderingConfiguration: NotRequired[RenderingConfigurationTypeDef]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    sourceConfiguration: NotRequired[SourceConfigurationOutputTypeDef]
    tags: NotRequired[Dict[str, str]]
    vectorIngestionConfiguration: NotRequired[VectorIngestionConfigurationOutputTypeDef]


class KnowledgeBaseSummaryTypeDef(TypedDict):
    knowledgeBaseArn: str
    knowledgeBaseId: str
    knowledgeBaseType: KnowledgeBaseTypeType
    name: str
    status: KnowledgeBaseStatusType
    description: NotRequired[str]
    renderingConfiguration: NotRequired[RenderingConfigurationTypeDef]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    sourceConfiguration: NotRequired[SourceConfigurationOutputTypeDef]
    tags: NotRequired[Dict[str, str]]
    vectorIngestionConfiguration: NotRequired[VectorIngestionConfigurationOutputTypeDef]


class ManagedSourceConfigurationTypeDef(TypedDict):
    webCrawlerConfiguration: NotRequired[WebCrawlerConfigurationUnionTypeDef]


ResultDataPaginatorTypeDef = TypedDict(
    "ResultDataPaginatorTypeDef",
    {
        "resultId": str,
        "data": NotRequired[DataSummaryPaginatorTypeDef],
        "document": NotRequired[DocumentTypeDef],
        "relevanceScore": NotRequired[float],
        "type": NotRequired[QueryResultTypeType],
    },
)
RecommendationDataTypeDef = TypedDict(
    "RecommendationDataTypeDef",
    {
        "recommendationId": str,
        "data": NotRequired[DataSummaryTypeDef],
        "document": NotRequired[DocumentTypeDef],
        "relevanceLevel": NotRequired[RelevanceLevelType],
        "relevanceScore": NotRequired[float],
        "type": NotRequired[RecommendationTypeType],
    },
)
ResultDataTypeDef = TypedDict(
    "ResultDataTypeDef",
    {
        "resultId": str,
        "data": NotRequired[DataSummaryTypeDef],
        "document": NotRequired[DocumentTypeDef],
        "relevanceScore": NotRequired[float],
        "type": NotRequired[QueryResultTypeType],
    },
)


class AnswerRecommendationAIAgentConfigurationOutputTypeDef(TypedDict):
    answerGenerationAIGuardrailId: NotRequired[str]
    answerGenerationAIPromptId: NotRequired[str]
    associationConfigurations: NotRequired[List[AssociationConfigurationOutputTypeDef]]
    intentLabelingGenerationAIPromptId: NotRequired[str]
    queryReformulationAIPromptId: NotRequired[str]


class ManualSearchAIAgentConfigurationOutputTypeDef(TypedDict):
    answerGenerationAIGuardrailId: NotRequired[str]
    answerGenerationAIPromptId: NotRequired[str]
    associationConfigurations: NotRequired[List[AssociationConfigurationOutputTypeDef]]


class SelfServiceAIAgentConfigurationOutputTypeDef(TypedDict):
    associationConfigurations: NotRequired[List[AssociationConfigurationOutputTypeDef]]
    selfServiceAIGuardrailId: NotRequired[str]
    selfServiceAnswerGenerationAIPromptId: NotRequired[str]
    selfServicePreProcessingAIPromptId: NotRequired[str]


KnowledgeBaseAssociationConfigurationDataUnionTypeDef = Union[
    KnowledgeBaseAssociationConfigurationDataTypeDef,
    KnowledgeBaseAssociationConfigurationDataOutputTypeDef,
]


class CreateKnowledgeBaseResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetKnowledgeBaseResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateKnowledgeBaseTemplateUriResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListKnowledgeBasesResponseTypeDef(TypedDict):
    knowledgeBaseSummaries: List[KnowledgeBaseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


ManagedSourceConfigurationUnionTypeDef = Union[
    ManagedSourceConfigurationTypeDef, ManagedSourceConfigurationOutputTypeDef
]


class QueryAssistantResponsePaginatorTypeDef(TypedDict):
    results: List[ResultDataPaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetRecommendationsResponseTypeDef(TypedDict):
    recommendations: List[RecommendationDataTypeDef]
    triggers: List[RecommendationTriggerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class QueryAssistantResponseTypeDef(TypedDict):
    results: List[ResultDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AIAgentConfigurationOutputTypeDef(TypedDict):
    answerRecommendationAIAgentConfiguration: NotRequired[
        AnswerRecommendationAIAgentConfigurationOutputTypeDef
    ]
    manualSearchAIAgentConfiguration: NotRequired[ManualSearchAIAgentConfigurationOutputTypeDef]
    selfServiceAIAgentConfiguration: NotRequired[SelfServiceAIAgentConfigurationOutputTypeDef]


class AssociationConfigurationDataTypeDef(TypedDict):
    knowledgeBaseAssociationConfigurationData: NotRequired[
        KnowledgeBaseAssociationConfigurationDataUnionTypeDef
    ]


class SourceConfigurationTypeDef(TypedDict):
    appIntegrations: NotRequired[AppIntegrationsConfigurationUnionTypeDef]
    managedSourceConfiguration: NotRequired[ManagedSourceConfigurationUnionTypeDef]


AIAgentDataTypeDef = TypedDict(
    "AIAgentDataTypeDef",
    {
        "aiAgentArn": str,
        "aiAgentId": str,
        "assistantArn": str,
        "assistantId": str,
        "configuration": AIAgentConfigurationOutputTypeDef,
        "name": str,
        "type": AIAgentTypeType,
        "visibilityStatus": VisibilityStatusType,
        "description": NotRequired[str],
        "modifiedTime": NotRequired[datetime],
        "origin": NotRequired[OriginType],
        "status": NotRequired[StatusType],
        "tags": NotRequired[Dict[str, str]],
    },
)
AIAgentSummaryTypeDef = TypedDict(
    "AIAgentSummaryTypeDef",
    {
        "aiAgentArn": str,
        "aiAgentId": str,
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "type": AIAgentTypeType,
        "visibilityStatus": VisibilityStatusType,
        "configuration": NotRequired[AIAgentConfigurationOutputTypeDef],
        "description": NotRequired[str],
        "modifiedTime": NotRequired[datetime],
        "origin": NotRequired[OriginType],
        "status": NotRequired[StatusType],
        "tags": NotRequired[Dict[str, str]],
    },
)
AssociationConfigurationDataUnionTypeDef = Union[
    AssociationConfigurationDataTypeDef, AssociationConfigurationDataOutputTypeDef
]


class CreateKnowledgeBaseRequestRequestTypeDef(TypedDict):
    knowledgeBaseType: KnowledgeBaseTypeType
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    renderingConfiguration: NotRequired[RenderingConfigurationTypeDef]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    sourceConfiguration: NotRequired[SourceConfigurationTypeDef]
    tags: NotRequired[Mapping[str, str]]
    vectorIngestionConfiguration: NotRequired[VectorIngestionConfigurationTypeDef]


class CreateAIAgentResponseTypeDef(TypedDict):
    aiAgent: AIAgentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAIAgentVersionResponseTypeDef(TypedDict):
    aiAgent: AIAgentDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetAIAgentResponseTypeDef(TypedDict):
    aiAgent: AIAgentDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAIAgentResponseTypeDef(TypedDict):
    aiAgent: AIAgentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AIAgentVersionSummaryTypeDef(TypedDict):
    aiAgentSummary: NotRequired[AIAgentSummaryTypeDef]
    versionNumber: NotRequired[int]


class ListAIAgentsResponseTypeDef(TypedDict):
    aiAgentSummaries: List[AIAgentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AssociationConfigurationTypeDef(TypedDict):
    associationConfigurationData: NotRequired[AssociationConfigurationDataUnionTypeDef]
    associationId: NotRequired[str]
    associationType: NotRequired[Literal["KNOWLEDGE_BASE"]]


class ListAIAgentVersionsResponseTypeDef(TypedDict):
    aiAgentVersionSummaries: List[AIAgentVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


AssociationConfigurationUnionTypeDef = Union[
    AssociationConfigurationTypeDef, AssociationConfigurationOutputTypeDef
]


class ManualSearchAIAgentConfigurationTypeDef(TypedDict):
    answerGenerationAIGuardrailId: NotRequired[str]
    answerGenerationAIPromptId: NotRequired[str]
    associationConfigurations: NotRequired[Sequence[AssociationConfigurationTypeDef]]


class SelfServiceAIAgentConfigurationTypeDef(TypedDict):
    associationConfigurations: NotRequired[Sequence[AssociationConfigurationTypeDef]]
    selfServiceAIGuardrailId: NotRequired[str]
    selfServiceAnswerGenerationAIPromptId: NotRequired[str]
    selfServicePreProcessingAIPromptId: NotRequired[str]


class AnswerRecommendationAIAgentConfigurationTypeDef(TypedDict):
    answerGenerationAIGuardrailId: NotRequired[str]
    answerGenerationAIPromptId: NotRequired[str]
    associationConfigurations: NotRequired[Sequence[AssociationConfigurationUnionTypeDef]]
    intentLabelingGenerationAIPromptId: NotRequired[str]
    queryReformulationAIPromptId: NotRequired[str]


ManualSearchAIAgentConfigurationUnionTypeDef = Union[
    ManualSearchAIAgentConfigurationTypeDef, ManualSearchAIAgentConfigurationOutputTypeDef
]
SelfServiceAIAgentConfigurationUnionTypeDef = Union[
    SelfServiceAIAgentConfigurationTypeDef, SelfServiceAIAgentConfigurationOutputTypeDef
]
AnswerRecommendationAIAgentConfigurationUnionTypeDef = Union[
    AnswerRecommendationAIAgentConfigurationTypeDef,
    AnswerRecommendationAIAgentConfigurationOutputTypeDef,
]


class AIAgentConfigurationTypeDef(TypedDict):
    answerRecommendationAIAgentConfiguration: NotRequired[
        AnswerRecommendationAIAgentConfigurationUnionTypeDef
    ]
    manualSearchAIAgentConfiguration: NotRequired[ManualSearchAIAgentConfigurationUnionTypeDef]
    selfServiceAIAgentConfiguration: NotRequired[SelfServiceAIAgentConfigurationUnionTypeDef]


CreateAIAgentRequestRequestTypeDef = TypedDict(
    "CreateAIAgentRequestRequestTypeDef",
    {
        "assistantId": str,
        "configuration": AIAgentConfigurationTypeDef,
        "name": str,
        "type": AIAgentTypeType,
        "visibilityStatus": VisibilityStatusType,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)


class UpdateAIAgentRequestRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    visibilityStatus: VisibilityStatusType
    clientToken: NotRequired[str]
    configuration: NotRequired[AIAgentConfigurationTypeDef]
    description: NotRequired[str]
