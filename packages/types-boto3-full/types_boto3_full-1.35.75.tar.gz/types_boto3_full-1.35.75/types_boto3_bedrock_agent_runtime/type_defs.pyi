"""
Type annotations for bedrock-agent-runtime service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/type_defs/)

Usage::

    ```python
    from types_boto3_bedrock_agent_runtime.type_defs import S3IdentifierTypeDef

    data: S3IdentifierTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.eventstream import EventStream
from botocore.response import StreamingBody

from .literals import (
    ActionGroupSignatureType,
    ActionInvocationTypeType,
    AttributeTypeType,
    ConfirmationStateType,
    ConversationRoleType,
    CreationModeType,
    ExecutionTypeType,
    ExternalSourceTypeType,
    FileSourceTypeType,
    FileUseCaseType,
    GuadrailActionType,
    GuardrailActionType,
    GuardrailContentFilterConfidenceType,
    GuardrailContentFilterTypeType,
    GuardrailPiiEntityTypeType,
    GuardrailSensitiveInformationPolicyActionType,
    InvocationTypeType,
    NodeTypeType,
    ParameterTypeType,
    PayloadTypeType,
    PromptStateType,
    PromptTypeType,
    RequireConfirmationType,
    RerankDocumentTypeType,
    RerankingMetadataSelectionModeType,
    ResponseStateType,
    RetrievalResultContentColumnTypeType,
    RetrievalResultContentTypeType,
    RetrievalResultLocationTypeType,
    RetrieveAndGenerateTypeType,
    SearchTypeType,
    SourceType,
    TypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "APISchemaTypeDef",
    "AccessDeniedExceptionTypeDef",
    "ActionGroupExecutorTypeDef",
    "ActionGroupInvocationInputTypeDef",
    "ActionGroupInvocationOutputTypeDef",
    "AgentActionGroupTypeDef",
    "AgentCollaboratorInputPayloadTypeDef",
    "AgentCollaboratorInvocationInputTypeDef",
    "AgentCollaboratorInvocationOutputTypeDef",
    "AgentCollaboratorOutputPayloadTypeDef",
    "AnalyzePromptEventTypeDef",
    "ApiInvocationInputTypeDef",
    "ApiParameterTypeDef",
    "ApiRequestBodyTypeDef",
    "ApiResultOutputTypeDef",
    "ApiResultTypeDef",
    "ApiResultUnionTypeDef",
    "AttributionTypeDef",
    "BadGatewayExceptionTypeDef",
    "BedrockRerankingConfigurationTypeDef",
    "BedrockRerankingModelConfigurationTypeDef",
    "BlobTypeDef",
    "ByteContentDocTypeDef",
    "ByteContentFileTypeDef",
    "CallerTypeDef",
    "CitationEventTypeDef",
    "CitationTypeDef",
    "CodeInterpreterInvocationInputTypeDef",
    "CodeInterpreterInvocationOutputTypeDef",
    "ConflictExceptionTypeDef",
    "ContentBlockTypeDef",
    "ContentBodyTypeDef",
    "ConversationHistoryTypeDef",
    "CustomOrchestrationTraceEventTypeDef",
    "CustomOrchestrationTraceTypeDef",
    "DeleteAgentMemoryRequestRequestTypeDef",
    "DependencyFailedExceptionTypeDef",
    "ExternalSourceTypeDef",
    "ExternalSourcesGenerationConfigurationTypeDef",
    "ExternalSourcesRetrieveAndGenerateConfigurationTypeDef",
    "FailureTraceTypeDef",
    "FieldForRerankingTypeDef",
    "FilePartTypeDef",
    "FileSourceTypeDef",
    "FilterAttributeTypeDef",
    "FinalResponseTypeDef",
    "FlowCompletionEventTypeDef",
    "FlowInputContentTypeDef",
    "FlowInputTypeDef",
    "FlowOutputContentTypeDef",
    "FlowOutputEventTypeDef",
    "FlowResponseStreamTypeDef",
    "FlowTraceConditionNodeResultEventTypeDef",
    "FlowTraceConditionTypeDef",
    "FlowTraceEventTypeDef",
    "FlowTraceNodeInputContentTypeDef",
    "FlowTraceNodeInputEventTypeDef",
    "FlowTraceNodeInputFieldTypeDef",
    "FlowTraceNodeOutputContentTypeDef",
    "FlowTraceNodeOutputEventTypeDef",
    "FlowTraceNodeOutputFieldTypeDef",
    "FlowTraceTypeDef",
    "FunctionDefinitionTypeDef",
    "FunctionInvocationInputTypeDef",
    "FunctionParameterTypeDef",
    "FunctionResultOutputTypeDef",
    "FunctionResultTypeDef",
    "FunctionResultUnionTypeDef",
    "FunctionSchemaTypeDef",
    "GenerateQueryRequestRequestTypeDef",
    "GenerateQueryResponseTypeDef",
    "GeneratedQueryTypeDef",
    "GeneratedResponsePartTypeDef",
    "GenerationConfigurationTypeDef",
    "GetAgentMemoryRequestGetAgentMemoryPaginateTypeDef",
    "GetAgentMemoryRequestRequestTypeDef",
    "GetAgentMemoryResponseTypeDef",
    "GuardrailAssessmentTypeDef",
    "GuardrailConfigurationTypeDef",
    "GuardrailConfigurationWithArnTypeDef",
    "GuardrailContentFilterTypeDef",
    "GuardrailContentPolicyAssessmentTypeDef",
    "GuardrailCustomWordTypeDef",
    "GuardrailEventTypeDef",
    "GuardrailManagedWordTypeDef",
    "GuardrailPiiEntityFilterTypeDef",
    "GuardrailRegexFilterTypeDef",
    "GuardrailSensitiveInformationPolicyAssessmentTypeDef",
    "GuardrailTopicPolicyAssessmentTypeDef",
    "GuardrailTopicTypeDef",
    "GuardrailTraceTypeDef",
    "GuardrailWordPolicyAssessmentTypeDef",
    "ImplicitFilterConfigurationTypeDef",
    "InferenceConfigTypeDef",
    "InferenceConfigurationOutputTypeDef",
    "InferenceConfigurationTypeDef",
    "InferenceConfigurationUnionTypeDef",
    "InlineAgentFilePartTypeDef",
    "InlineAgentPayloadPartTypeDef",
    "InlineAgentResponseStreamTypeDef",
    "InlineAgentReturnControlPayloadTypeDef",
    "InlineAgentTracePartTypeDef",
    "InlineSessionStateTypeDef",
    "InputFileTypeDef",
    "InputPromptTypeDef",
    "InternalServerExceptionTypeDef",
    "InvocationInputMemberTypeDef",
    "InvocationInputTypeDef",
    "InvocationResultMemberOutputTypeDef",
    "InvocationResultMemberTypeDef",
    "InvocationResultMemberUnionTypeDef",
    "InvokeAgentRequestRequestTypeDef",
    "InvokeAgentResponseTypeDef",
    "InvokeFlowRequestRequestTypeDef",
    "InvokeFlowResponseTypeDef",
    "InvokeInlineAgentRequestRequestTypeDef",
    "InvokeInlineAgentResponseTypeDef",
    "KnowledgeBaseConfigurationTypeDef",
    "KnowledgeBaseLookupInputTypeDef",
    "KnowledgeBaseLookupOutputTypeDef",
    "KnowledgeBaseQueryTypeDef",
    "KnowledgeBaseRetrievalConfigurationPaginatorTypeDef",
    "KnowledgeBaseRetrievalConfigurationTypeDef",
    "KnowledgeBaseRetrievalResultTypeDef",
    "KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef",
    "KnowledgeBaseTypeDef",
    "KnowledgeBaseVectorSearchConfigurationPaginatorTypeDef",
    "KnowledgeBaseVectorSearchConfigurationTypeDef",
    "MemorySessionSummaryTypeDef",
    "MemoryTypeDef",
    "MessageTypeDef",
    "MetadataAttributeSchemaTypeDef",
    "MetadataConfigurationForRerankingTypeDef",
    "MetadataTypeDef",
    "ModelInvocationInputTypeDef",
    "ObservationTypeDef",
    "OptimizePromptRequestRequestTypeDef",
    "OptimizePromptResponseTypeDef",
    "OptimizedPromptEventTypeDef",
    "OptimizedPromptStreamTypeDef",
    "OptimizedPromptTypeDef",
    "OrchestrationConfigurationTypeDef",
    "OrchestrationModelInvocationOutputTypeDef",
    "OrchestrationTraceTypeDef",
    "OutputFileTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterDetailTypeDef",
    "ParameterTypeDef",
    "PayloadPartTypeDef",
    "PostProcessingModelInvocationOutputTypeDef",
    "PostProcessingParsedResponseTypeDef",
    "PostProcessingTraceTypeDef",
    "PreProcessingModelInvocationOutputTypeDef",
    "PreProcessingParsedResponseTypeDef",
    "PreProcessingTraceTypeDef",
    "PromptConfigurationTypeDef",
    "PromptOverrideConfigurationTypeDef",
    "PromptTemplateTypeDef",
    "PropertyParametersTypeDef",
    "QueryGenerationInputTypeDef",
    "QueryTransformationConfigurationTypeDef",
    "RationaleTypeDef",
    "RawResponseTypeDef",
    "RepromptResponseTypeDef",
    "RequestBodyTypeDef",
    "RerankDocumentOutputTypeDef",
    "RerankDocumentTypeDef",
    "RerankDocumentUnionTypeDef",
    "RerankQueryTypeDef",
    "RerankRequestRequestTypeDef",
    "RerankRequestRerankPaginateTypeDef",
    "RerankResponseTypeDef",
    "RerankResultTypeDef",
    "RerankSourceTypeDef",
    "RerankTextDocumentTypeDef",
    "RerankingConfigurationTypeDef",
    "RerankingMetadataSelectiveModeConfigurationTypeDef",
    "ResourceNotFoundExceptionTypeDef",
    "ResponseMetadataTypeDef",
    "ResponseStreamTypeDef",
    "RetrievalFilterPaginatorTypeDef",
    "RetrievalFilterTypeDef",
    "RetrievalResultConfluenceLocationTypeDef",
    "RetrievalResultContentColumnTypeDef",
    "RetrievalResultContentTypeDef",
    "RetrievalResultCustomDocumentLocationTypeDef",
    "RetrievalResultKendraDocumentLocationTypeDef",
    "RetrievalResultLocationTypeDef",
    "RetrievalResultS3LocationTypeDef",
    "RetrievalResultSalesforceLocationTypeDef",
    "RetrievalResultSharePointLocationTypeDef",
    "RetrievalResultSqlLocationTypeDef",
    "RetrievalResultWebLocationTypeDef",
    "RetrieveAndGenerateConfigurationTypeDef",
    "RetrieveAndGenerateInputTypeDef",
    "RetrieveAndGenerateOutputEventTypeDef",
    "RetrieveAndGenerateOutputTypeDef",
    "RetrieveAndGenerateRequestRequestTypeDef",
    "RetrieveAndGenerateResponseTypeDef",
    "RetrieveAndGenerateSessionConfigurationTypeDef",
    "RetrieveAndGenerateStreamRequestRequestTypeDef",
    "RetrieveAndGenerateStreamResponseOutputTypeDef",
    "RetrieveAndGenerateStreamResponseTypeDef",
    "RetrieveRequestRequestTypeDef",
    "RetrieveRequestRetrievePaginateTypeDef",
    "RetrieveResponseTypeDef",
    "RetrievedReferenceTypeDef",
    "ReturnControlPayloadTypeDef",
    "ReturnControlResultsTypeDef",
    "RoutingClassifierModelInvocationOutputTypeDef",
    "RoutingClassifierTraceTypeDef",
    "S3IdentifierTypeDef",
    "S3ObjectDocTypeDef",
    "S3ObjectFileTypeDef",
    "ServiceQuotaExceededExceptionTypeDef",
    "SessionStateTypeDef",
    "SpanTypeDef",
    "StreamingConfigurationsTypeDef",
    "TextInferenceConfigTypeDef",
    "TextPromptTypeDef",
    "TextResponsePartTypeDef",
    "TextToSqlConfigurationTypeDef",
    "TextToSqlKnowledgeBaseConfigurationTypeDef",
    "ThrottlingExceptionTypeDef",
    "TracePartTypeDef",
    "TraceTypeDef",
    "TransformationConfigurationTypeDef",
    "UsageTypeDef",
    "ValidationExceptionTypeDef",
    "VectorSearchBedrockRerankingConfigurationTypeDef",
    "VectorSearchBedrockRerankingModelConfigurationTypeDef",
    "VectorSearchRerankingConfigurationTypeDef",
)

class S3IdentifierTypeDef(TypedDict):
    s3BucketName: NotRequired[str]
    s3ObjectKey: NotRequired[str]

class AccessDeniedExceptionTypeDef(TypedDict):
    message: NotRequired[str]

ActionGroupExecutorTypeDef = TypedDict(
    "ActionGroupExecutorTypeDef",
    {
        "customControl": NotRequired[Literal["RETURN_CONTROL"]],
        "lambda": NotRequired[str],
    },
)
ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)

class ActionGroupInvocationOutputTypeDef(TypedDict):
    text: NotRequired[str]

class AnalyzePromptEventTypeDef(TypedDict):
    message: NotRequired[str]

ApiParameterTypeDef = TypedDict(
    "ApiParameterTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)

class ContentBodyTypeDef(TypedDict):
    body: NotRequired[str]

class BadGatewayExceptionTypeDef(TypedDict):
    message: NotRequired[str]
    resourceName: NotRequired[str]

class BedrockRerankingModelConfigurationTypeDef(TypedDict):
    modelArn: str
    additionalModelRequestFields: NotRequired[Mapping[str, Mapping[str, Any]]]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class CallerTypeDef(TypedDict):
    agentAliasArn: NotRequired[str]

class CodeInterpreterInvocationInputTypeDef(TypedDict):
    code: NotRequired[str]
    files: NotRequired[List[str]]

class CodeInterpreterInvocationOutputTypeDef(TypedDict):
    executionError: NotRequired[str]
    executionOutput: NotRequired[str]
    executionTimeout: NotRequired[bool]
    files: NotRequired[List[str]]

class ConflictExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class ContentBlockTypeDef(TypedDict):
    text: NotRequired[str]

class CustomOrchestrationTraceEventTypeDef(TypedDict):
    text: NotRequired[str]

class DeleteAgentMemoryRequestRequestTypeDef(TypedDict):
    agentAliasId: str
    agentId: str
    memoryId: NotRequired[str]

class DependencyFailedExceptionTypeDef(TypedDict):
    message: NotRequired[str]
    resourceName: NotRequired[str]

class S3ObjectDocTypeDef(TypedDict):
    uri: str

class GuardrailConfigurationTypeDef(TypedDict):
    guardrailId: str
    guardrailVersion: str

class PromptTemplateTypeDef(TypedDict):
    textPromptTemplate: NotRequired[str]

class FailureTraceTypeDef(TypedDict):
    failureReason: NotRequired[str]
    traceId: NotRequired[str]

class FieldForRerankingTypeDef(TypedDict):
    fieldName: str

OutputFileTypeDef = TypedDict(
    "OutputFileTypeDef",
    {
        "bytes": NotRequired[bytes],
        "name": NotRequired[str],
        "type": NotRequired[str],
    },
)

class S3ObjectFileTypeDef(TypedDict):
    uri: str

class FilterAttributeTypeDef(TypedDict):
    key: str
    value: Mapping[str, Any]

class FinalResponseTypeDef(TypedDict):
    text: NotRequired[str]

class FlowCompletionEventTypeDef(TypedDict):
    completionReason: Literal["SUCCESS"]

class FlowInputContentTypeDef(TypedDict):
    document: NotRequired[Mapping[str, Any]]

class FlowOutputContentTypeDef(TypedDict):
    document: NotRequired[Dict[str, Any]]

class InternalServerExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class ResourceNotFoundExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class ServiceQuotaExceededExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class ThrottlingExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class ValidationExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class FlowTraceConditionTypeDef(TypedDict):
    conditionName: str

class FlowTraceNodeInputContentTypeDef(TypedDict):
    document: NotRequired[Dict[str, Any]]

class FlowTraceNodeOutputContentTypeDef(TypedDict):
    document: NotRequired[Dict[str, Any]]

ParameterDetailTypeDef = TypedDict(
    "ParameterDetailTypeDef",
    {
        "type": ParameterTypeType,
        "description": NotRequired[str],
        "required": NotRequired[bool],
    },
)
FunctionParameterTypeDef = TypedDict(
    "FunctionParameterTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)
QueryGenerationInputTypeDef = TypedDict(
    "QueryGenerationInputTypeDef",
    {
        "text": str,
        "type": Literal["TEXT"],
    },
)
GeneratedQueryTypeDef = TypedDict(
    "GeneratedQueryTypeDef",
    {
        "sql": NotRequired[str],
        "type": NotRequired[Literal["REDSHIFT_SQL"]],
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetAgentMemoryRequestRequestTypeDef(TypedDict):
    agentAliasId: str
    agentId: str
    memoryId: str
    memoryType: Literal["SESSION_SUMMARY"]
    maxItems: NotRequired[int]
    nextToken: NotRequired[str]

class GuardrailConfigurationWithArnTypeDef(TypedDict):
    guardrailIdentifier: str
    guardrailVersion: str

GuardrailContentFilterTypeDef = TypedDict(
    "GuardrailContentFilterTypeDef",
    {
        "action": NotRequired[Literal["BLOCKED"]],
        "confidence": NotRequired[GuardrailContentFilterConfidenceType],
        "type": NotRequired[GuardrailContentFilterTypeType],
    },
)

class GuardrailCustomWordTypeDef(TypedDict):
    action: NotRequired[Literal["BLOCKED"]]
    match: NotRequired[str]

class GuardrailEventTypeDef(TypedDict):
    action: NotRequired[GuadrailActionType]

GuardrailManagedWordTypeDef = TypedDict(
    "GuardrailManagedWordTypeDef",
    {
        "action": NotRequired[Literal["BLOCKED"]],
        "match": NotRequired[str],
        "type": NotRequired[Literal["PROFANITY"]],
    },
)
GuardrailPiiEntityFilterTypeDef = TypedDict(
    "GuardrailPiiEntityFilterTypeDef",
    {
        "action": NotRequired[GuardrailSensitiveInformationPolicyActionType],
        "match": NotRequired[str],
        "type": NotRequired[GuardrailPiiEntityTypeType],
    },
)

class GuardrailRegexFilterTypeDef(TypedDict):
    action: NotRequired[GuardrailSensitiveInformationPolicyActionType]
    match: NotRequired[str]
    name: NotRequired[str]
    regex: NotRequired[str]

GuardrailTopicTypeDef = TypedDict(
    "GuardrailTopicTypeDef",
    {
        "action": NotRequired[Literal["BLOCKED"]],
        "name": NotRequired[str],
        "type": NotRequired[Literal["DENY"]],
    },
)
MetadataAttributeSchemaTypeDef = TypedDict(
    "MetadataAttributeSchemaTypeDef",
    {
        "description": str,
        "key": str,
        "type": AttributeTypeType,
    },
)

class TextInferenceConfigTypeDef(TypedDict):
    maxTokens: NotRequired[int]
    stopSequences: NotRequired[Sequence[str]]
    temperature: NotRequired[float]
    topP: NotRequired[float]

class InferenceConfigurationOutputTypeDef(TypedDict):
    maximumLength: NotRequired[int]
    stopSequences: NotRequired[List[str]]
    temperature: NotRequired[float]
    topK: NotRequired[int]
    topP: NotRequired[float]

class InferenceConfigurationTypeDef(TypedDict):
    maximumLength: NotRequired[int]
    stopSequences: NotRequired[Sequence[str]]
    temperature: NotRequired[float]
    topK: NotRequired[int]
    topP: NotRequired[float]

class TextPromptTypeDef(TypedDict):
    text: str

class KnowledgeBaseLookupInputTypeDef(TypedDict):
    knowledgeBaseId: NotRequired[str]
    text: NotRequired[str]

class StreamingConfigurationsTypeDef(TypedDict):
    applyGuardrailInterval: NotRequired[int]
    streamFinalResponse: NotRequired[bool]

class KnowledgeBaseQueryTypeDef(TypedDict):
    text: str

class MemorySessionSummaryTypeDef(TypedDict):
    memoryId: NotRequired[str]
    sessionExpiryTime: NotRequired[datetime]
    sessionId: NotRequired[str]
    sessionStartTime: NotRequired[datetime]
    summaryText: NotRequired[str]

class UsageTypeDef(TypedDict):
    inputTokens: NotRequired[int]
    outputTokens: NotRequired[int]

class RepromptResponseTypeDef(TypedDict):
    source: NotRequired[SourceType]
    text: NotRequired[str]

QueryTransformationConfigurationTypeDef = TypedDict(
    "QueryTransformationConfigurationTypeDef",
    {
        "type": Literal["QUERY_DECOMPOSITION"],
    },
)

class RawResponseTypeDef(TypedDict):
    content: NotRequired[str]

class RationaleTypeDef(TypedDict):
    text: NotRequired[str]
    traceId: NotRequired[str]

class PostProcessingParsedResponseTypeDef(TypedDict):
    text: NotRequired[str]

class PreProcessingParsedResponseTypeDef(TypedDict):
    isValid: NotRequired[bool]
    rationale: NotRequired[str]

class RerankTextDocumentTypeDef(TypedDict):
    text: NotRequired[str]

class RetrievalResultConfluenceLocationTypeDef(TypedDict):
    url: NotRequired[str]

RetrievalResultContentColumnTypeDef = TypedDict(
    "RetrievalResultContentColumnTypeDef",
    {
        "columnName": NotRequired[str],
        "columnValue": NotRequired[str],
        "type": NotRequired[RetrievalResultContentColumnTypeType],
    },
)
RetrievalResultCustomDocumentLocationTypeDef = TypedDict(
    "RetrievalResultCustomDocumentLocationTypeDef",
    {
        "id": NotRequired[str],
    },
)

class RetrievalResultKendraDocumentLocationTypeDef(TypedDict):
    uri: NotRequired[str]

class RetrievalResultS3LocationTypeDef(TypedDict):
    uri: NotRequired[str]

class RetrievalResultSalesforceLocationTypeDef(TypedDict):
    url: NotRequired[str]

class RetrievalResultSharePointLocationTypeDef(TypedDict):
    url: NotRequired[str]

class RetrievalResultSqlLocationTypeDef(TypedDict):
    query: NotRequired[str]

class RetrievalResultWebLocationTypeDef(TypedDict):
    url: NotRequired[str]

class RetrieveAndGenerateInputTypeDef(TypedDict):
    text: str

class RetrieveAndGenerateOutputEventTypeDef(TypedDict):
    text: str

class RetrieveAndGenerateOutputTypeDef(TypedDict):
    text: str

class RetrieveAndGenerateSessionConfigurationTypeDef(TypedDict):
    kmsKeyArn: str

class SpanTypeDef(TypedDict):
    end: NotRequired[int]
    start: NotRequired[int]

class TextToSqlKnowledgeBaseConfigurationTypeDef(TypedDict):
    knowledgeBaseArn: str

class VectorSearchBedrockRerankingModelConfigurationTypeDef(TypedDict):
    modelArn: str
    additionalModelRequestFields: NotRequired[Mapping[str, Mapping[str, Any]]]

class APISchemaTypeDef(TypedDict):
    payload: NotRequired[str]
    s3: NotRequired[S3IdentifierTypeDef]

class PropertyParametersTypeDef(TypedDict):
    properties: NotRequired[List[ParameterTypeDef]]

class RequestBodyTypeDef(TypedDict):
    content: NotRequired[Dict[str, List[ParameterTypeDef]]]

class ApiResultOutputTypeDef(TypedDict):
    actionGroup: str
    agentId: NotRequired[str]
    apiPath: NotRequired[str]
    confirmationState: NotRequired[ConfirmationStateType]
    httpMethod: NotRequired[str]
    httpStatusCode: NotRequired[int]
    responseBody: NotRequired[Dict[str, ContentBodyTypeDef]]
    responseState: NotRequired[ResponseStateType]

class ApiResultTypeDef(TypedDict):
    actionGroup: str
    agentId: NotRequired[str]
    apiPath: NotRequired[str]
    confirmationState: NotRequired[ConfirmationStateType]
    httpMethod: NotRequired[str]
    httpStatusCode: NotRequired[int]
    responseBody: NotRequired[Mapping[str, ContentBodyTypeDef]]
    responseState: NotRequired[ResponseStateType]

class FunctionResultOutputTypeDef(TypedDict):
    actionGroup: str
    agentId: NotRequired[str]
    confirmationState: NotRequired[ConfirmationStateType]
    function: NotRequired[str]
    responseBody: NotRequired[Dict[str, ContentBodyTypeDef]]
    responseState: NotRequired[ResponseStateType]

class FunctionResultTypeDef(TypedDict):
    actionGroup: str
    agentId: NotRequired[str]
    confirmationState: NotRequired[ConfirmationStateType]
    function: NotRequired[str]
    responseBody: NotRequired[Mapping[str, ContentBodyTypeDef]]
    responseState: NotRequired[ResponseStateType]

class BedrockRerankingConfigurationTypeDef(TypedDict):
    modelConfiguration: BedrockRerankingModelConfigurationTypeDef
    numberOfResults: NotRequired[int]

class ByteContentDocTypeDef(TypedDict):
    contentType: str
    data: BlobTypeDef
    identifier: str

class ByteContentFileTypeDef(TypedDict):
    data: BlobTypeDef
    mediaType: str

class MessageTypeDef(TypedDict):
    content: Sequence[ContentBlockTypeDef]
    role: ConversationRoleType

class CustomOrchestrationTraceTypeDef(TypedDict):
    event: NotRequired[CustomOrchestrationTraceEventTypeDef]
    traceId: NotRequired[str]

class RerankingMetadataSelectiveModeConfigurationTypeDef(TypedDict):
    fieldsToExclude: NotRequired[Sequence[FieldForRerankingTypeDef]]
    fieldsToInclude: NotRequired[Sequence[FieldForRerankingTypeDef]]

class FilePartTypeDef(TypedDict):
    files: NotRequired[List[OutputFileTypeDef]]

class InlineAgentFilePartTypeDef(TypedDict):
    files: NotRequired[List[OutputFileTypeDef]]

RetrievalFilterPaginatorTypeDef = TypedDict(
    "RetrievalFilterPaginatorTypeDef",
    {
        "andAll": NotRequired[Sequence[Mapping[str, Any]]],
        "equals": NotRequired[FilterAttributeTypeDef],
        "greaterThan": NotRequired[FilterAttributeTypeDef],
        "greaterThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "in": NotRequired[FilterAttributeTypeDef],
        "lessThan": NotRequired[FilterAttributeTypeDef],
        "lessThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "listContains": NotRequired[FilterAttributeTypeDef],
        "notEquals": NotRequired[FilterAttributeTypeDef],
        "notIn": NotRequired[FilterAttributeTypeDef],
        "orAll": NotRequired[Sequence[Mapping[str, Any]]],
        "startsWith": NotRequired[FilterAttributeTypeDef],
        "stringContains": NotRequired[FilterAttributeTypeDef],
    },
)
RetrievalFilterTypeDef = TypedDict(
    "RetrievalFilterTypeDef",
    {
        "andAll": NotRequired[Sequence[Mapping[str, Any]]],
        "equals": NotRequired[FilterAttributeTypeDef],
        "greaterThan": NotRequired[FilterAttributeTypeDef],
        "greaterThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "in": NotRequired[FilterAttributeTypeDef],
        "lessThan": NotRequired[FilterAttributeTypeDef],
        "lessThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "listContains": NotRequired[FilterAttributeTypeDef],
        "notEquals": NotRequired[FilterAttributeTypeDef],
        "notIn": NotRequired[FilterAttributeTypeDef],
        "orAll": NotRequired[Sequence[Mapping[str, Any]]],
        "startsWith": NotRequired[FilterAttributeTypeDef],
        "stringContains": NotRequired[FilterAttributeTypeDef],
    },
)

class FlowInputTypeDef(TypedDict):
    content: FlowInputContentTypeDef
    nodeName: str
    nodeOutputName: str

class FlowOutputEventTypeDef(TypedDict):
    content: FlowOutputContentTypeDef
    nodeName: str
    nodeType: NodeTypeType

class FlowTraceConditionNodeResultEventTypeDef(TypedDict):
    nodeName: str
    satisfiedConditions: List[FlowTraceConditionTypeDef]
    timestamp: datetime

class FlowTraceNodeInputFieldTypeDef(TypedDict):
    content: FlowTraceNodeInputContentTypeDef
    nodeInputName: str

class FlowTraceNodeOutputFieldTypeDef(TypedDict):
    content: FlowTraceNodeOutputContentTypeDef
    nodeOutputName: str

class FunctionDefinitionTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    parameters: NotRequired[Mapping[str, ParameterDetailTypeDef]]
    requireConfirmation: NotRequired[RequireConfirmationType]

class FunctionInvocationInputTypeDef(TypedDict):
    actionGroup: str
    actionInvocationType: NotRequired[ActionInvocationTypeType]
    agentId: NotRequired[str]
    collaboratorName: NotRequired[str]
    function: NotRequired[str]
    parameters: NotRequired[List[FunctionParameterTypeDef]]

class GenerateQueryResponseTypeDef(TypedDict):
    queries: List[GeneratedQueryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetAgentMemoryRequestGetAgentMemoryPaginateTypeDef(TypedDict):
    agentAliasId: str
    agentId: str
    memoryId: str
    memoryType: Literal["SESSION_SUMMARY"]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GuardrailContentPolicyAssessmentTypeDef(TypedDict):
    filters: NotRequired[List[GuardrailContentFilterTypeDef]]

class GuardrailWordPolicyAssessmentTypeDef(TypedDict):
    customWords: NotRequired[List[GuardrailCustomWordTypeDef]]
    managedWordLists: NotRequired[List[GuardrailManagedWordTypeDef]]

class GuardrailSensitiveInformationPolicyAssessmentTypeDef(TypedDict):
    piiEntities: NotRequired[List[GuardrailPiiEntityFilterTypeDef]]
    regexes: NotRequired[List[GuardrailRegexFilterTypeDef]]

class GuardrailTopicPolicyAssessmentTypeDef(TypedDict):
    topics: NotRequired[List[GuardrailTopicTypeDef]]

class ImplicitFilterConfigurationTypeDef(TypedDict):
    metadataAttributes: Sequence[MetadataAttributeSchemaTypeDef]
    modelArn: str

class InferenceConfigTypeDef(TypedDict):
    textInferenceConfig: NotRequired[TextInferenceConfigTypeDef]

ModelInvocationInputTypeDef = TypedDict(
    "ModelInvocationInputTypeDef",
    {
        "foundationModel": NotRequired[str],
        "inferenceConfiguration": NotRequired[InferenceConfigurationOutputTypeDef],
        "overrideLambda": NotRequired[str],
        "parserMode": NotRequired[CreationModeType],
        "promptCreationMode": NotRequired[CreationModeType],
        "text": NotRequired[str],
        "traceId": NotRequired[str],
        "type": NotRequired[PromptTypeType],
    },
)
InferenceConfigurationUnionTypeDef = Union[
    InferenceConfigurationTypeDef, InferenceConfigurationOutputTypeDef
]

class InputPromptTypeDef(TypedDict):
    textPrompt: NotRequired[TextPromptTypeDef]

class OptimizedPromptTypeDef(TypedDict):
    textPrompt: NotRequired[TextPromptTypeDef]

class MemoryTypeDef(TypedDict):
    sessionSummary: NotRequired[MemorySessionSummaryTypeDef]

class MetadataTypeDef(TypedDict):
    usage: NotRequired[UsageTypeDef]

RerankDocumentOutputTypeDef = TypedDict(
    "RerankDocumentOutputTypeDef",
    {
        "type": RerankDocumentTypeType,
        "jsonDocument": NotRequired[Dict[str, Any]],
        "textDocument": NotRequired[RerankTextDocumentTypeDef],
    },
)
RerankDocumentTypeDef = TypedDict(
    "RerankDocumentTypeDef",
    {
        "type": RerankDocumentTypeType,
        "jsonDocument": NotRequired[Mapping[str, Any]],
        "textDocument": NotRequired[RerankTextDocumentTypeDef],
    },
)
RerankQueryTypeDef = TypedDict(
    "RerankQueryTypeDef",
    {
        "textQuery": RerankTextDocumentTypeDef,
        "type": Literal["TEXT"],
    },
)
RetrievalResultContentTypeDef = TypedDict(
    "RetrievalResultContentTypeDef",
    {
        "byteContent": NotRequired[str],
        "row": NotRequired[List[RetrievalResultContentColumnTypeDef]],
        "text": NotRequired[str],
        "type": NotRequired[RetrievalResultContentTypeType],
    },
)
RetrievalResultLocationTypeDef = TypedDict(
    "RetrievalResultLocationTypeDef",
    {
        "type": RetrievalResultLocationTypeType,
        "confluenceLocation": NotRequired[RetrievalResultConfluenceLocationTypeDef],
        "customDocumentLocation": NotRequired[RetrievalResultCustomDocumentLocationTypeDef],
        "kendraDocumentLocation": NotRequired[RetrievalResultKendraDocumentLocationTypeDef],
        "s3Location": NotRequired[RetrievalResultS3LocationTypeDef],
        "salesforceLocation": NotRequired[RetrievalResultSalesforceLocationTypeDef],
        "sharePointLocation": NotRequired[RetrievalResultSharePointLocationTypeDef],
        "sqlLocation": NotRequired[RetrievalResultSqlLocationTypeDef],
        "webLocation": NotRequired[RetrievalResultWebLocationTypeDef],
    },
)

class TextResponsePartTypeDef(TypedDict):
    span: NotRequired[SpanTypeDef]
    text: NotRequired[str]

TextToSqlConfigurationTypeDef = TypedDict(
    "TextToSqlConfigurationTypeDef",
    {
        "type": Literal["KNOWLEDGE_BASE"],
        "knowledgeBaseConfiguration": NotRequired[TextToSqlKnowledgeBaseConfigurationTypeDef],
    },
)

class ApiRequestBodyTypeDef(TypedDict):
    content: NotRequired[Dict[str, PropertyParametersTypeDef]]

class ActionGroupInvocationInputTypeDef(TypedDict):
    actionGroupName: NotRequired[str]
    apiPath: NotRequired[str]
    executionType: NotRequired[ExecutionTypeType]
    function: NotRequired[str]
    invocationId: NotRequired[str]
    parameters: NotRequired[List[ParameterTypeDef]]
    requestBody: NotRequired[RequestBodyTypeDef]
    verb: NotRequired[str]

ApiResultUnionTypeDef = Union[ApiResultTypeDef, ApiResultOutputTypeDef]

class InvocationResultMemberOutputTypeDef(TypedDict):
    apiResult: NotRequired[ApiResultOutputTypeDef]
    functionResult: NotRequired[FunctionResultOutputTypeDef]

FunctionResultUnionTypeDef = Union[FunctionResultTypeDef, FunctionResultOutputTypeDef]
RerankingConfigurationTypeDef = TypedDict(
    "RerankingConfigurationTypeDef",
    {
        "bedrockRerankingConfiguration": BedrockRerankingConfigurationTypeDef,
        "type": Literal["BEDROCK_RERANKING_MODEL"],
    },
)

class ExternalSourceTypeDef(TypedDict):
    sourceType: ExternalSourceTypeType
    byteContent: NotRequired[ByteContentDocTypeDef]
    s3Location: NotRequired[S3ObjectDocTypeDef]

class FileSourceTypeDef(TypedDict):
    sourceType: FileSourceTypeType
    byteContent: NotRequired[ByteContentFileTypeDef]
    s3Location: NotRequired[S3ObjectFileTypeDef]

class ConversationHistoryTypeDef(TypedDict):
    messages: NotRequired[Sequence[MessageTypeDef]]

class MetadataConfigurationForRerankingTypeDef(TypedDict):
    selectionMode: RerankingMetadataSelectionModeType
    selectiveModeConfiguration: NotRequired[RerankingMetadataSelectiveModeConfigurationTypeDef]

class InvokeFlowRequestRequestTypeDef(TypedDict):
    flowAliasIdentifier: str
    flowIdentifier: str
    inputs: Sequence[FlowInputTypeDef]
    enableTrace: NotRequired[bool]

class FlowTraceNodeInputEventTypeDef(TypedDict):
    fields: List[FlowTraceNodeInputFieldTypeDef]
    nodeName: str
    timestamp: datetime

class FlowTraceNodeOutputEventTypeDef(TypedDict):
    fields: List[FlowTraceNodeOutputFieldTypeDef]
    nodeName: str
    timestamp: datetime

class FunctionSchemaTypeDef(TypedDict):
    functions: NotRequired[Sequence[FunctionDefinitionTypeDef]]

class GuardrailAssessmentTypeDef(TypedDict):
    contentPolicy: NotRequired[GuardrailContentPolicyAssessmentTypeDef]
    sensitiveInformationPolicy: NotRequired[GuardrailSensitiveInformationPolicyAssessmentTypeDef]
    topicPolicy: NotRequired[GuardrailTopicPolicyAssessmentTypeDef]
    wordPolicy: NotRequired[GuardrailWordPolicyAssessmentTypeDef]

class ExternalSourcesGenerationConfigurationTypeDef(TypedDict):
    additionalModelRequestFields: NotRequired[Mapping[str, Mapping[str, Any]]]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    inferenceConfig: NotRequired[InferenceConfigTypeDef]
    promptTemplate: NotRequired[PromptTemplateTypeDef]

class GenerationConfigurationTypeDef(TypedDict):
    additionalModelRequestFields: NotRequired[Mapping[str, Mapping[str, Any]]]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    inferenceConfig: NotRequired[InferenceConfigTypeDef]
    promptTemplate: NotRequired[PromptTemplateTypeDef]

class OrchestrationConfigurationTypeDef(TypedDict):
    additionalModelRequestFields: NotRequired[Mapping[str, Mapping[str, Any]]]
    inferenceConfig: NotRequired[InferenceConfigTypeDef]
    promptTemplate: NotRequired[PromptTemplateTypeDef]
    queryTransformationConfiguration: NotRequired[QueryTransformationConfigurationTypeDef]

class PromptConfigurationTypeDef(TypedDict):
    basePromptTemplate: NotRequired[str]
    inferenceConfiguration: NotRequired[InferenceConfigurationUnionTypeDef]
    parserMode: NotRequired[CreationModeType]
    promptCreationMode: NotRequired[CreationModeType]
    promptState: NotRequired[PromptStateType]
    promptType: NotRequired[PromptTypeType]

OptimizePromptRequestRequestTypeDef = TypedDict(
    "OptimizePromptRequestRequestTypeDef",
    {
        "input": InputPromptTypeDef,
        "targetModelId": str,
    },
)

class OptimizedPromptEventTypeDef(TypedDict):
    optimizedPrompt: NotRequired[OptimizedPromptTypeDef]

class GetAgentMemoryResponseTypeDef(TypedDict):
    memoryContents: List[MemoryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class OrchestrationModelInvocationOutputTypeDef(TypedDict):
    metadata: NotRequired[MetadataTypeDef]
    rawResponse: NotRequired[RawResponseTypeDef]
    traceId: NotRequired[str]

class PostProcessingModelInvocationOutputTypeDef(TypedDict):
    metadata: NotRequired[MetadataTypeDef]
    parsedResponse: NotRequired[PostProcessingParsedResponseTypeDef]
    rawResponse: NotRequired[RawResponseTypeDef]
    traceId: NotRequired[str]

class PreProcessingModelInvocationOutputTypeDef(TypedDict):
    metadata: NotRequired[MetadataTypeDef]
    parsedResponse: NotRequired[PreProcessingParsedResponseTypeDef]
    rawResponse: NotRequired[RawResponseTypeDef]
    traceId: NotRequired[str]

class RoutingClassifierModelInvocationOutputTypeDef(TypedDict):
    metadata: NotRequired[MetadataTypeDef]
    rawResponse: NotRequired[RawResponseTypeDef]
    traceId: NotRequired[str]

class RerankResultTypeDef(TypedDict):
    index: int
    relevanceScore: float
    document: NotRequired[RerankDocumentOutputTypeDef]

RerankDocumentUnionTypeDef = Union[RerankDocumentTypeDef, RerankDocumentOutputTypeDef]

class KnowledgeBaseRetrievalResultTypeDef(TypedDict):
    content: RetrievalResultContentTypeDef
    location: NotRequired[RetrievalResultLocationTypeDef]
    metadata: NotRequired[Dict[str, Dict[str, Any]]]
    score: NotRequired[float]

class RetrievedReferenceTypeDef(TypedDict):
    content: NotRequired[RetrievalResultContentTypeDef]
    location: NotRequired[RetrievalResultLocationTypeDef]
    metadata: NotRequired[Dict[str, Dict[str, Any]]]

class GeneratedResponsePartTypeDef(TypedDict):
    textResponsePart: NotRequired[TextResponsePartTypeDef]

class TransformationConfigurationTypeDef(TypedDict):
    mode: Literal["TEXT_TO_SQL"]
    textToSqlConfiguration: NotRequired[TextToSqlConfigurationTypeDef]

class ApiInvocationInputTypeDef(TypedDict):
    actionGroup: str
    actionInvocationType: NotRequired[ActionInvocationTypeType]
    agentId: NotRequired[str]
    apiPath: NotRequired[str]
    collaboratorName: NotRequired[str]
    httpMethod: NotRequired[str]
    parameters: NotRequired[List[ApiParameterTypeDef]]
    requestBody: NotRequired[ApiRequestBodyTypeDef]

class ReturnControlResultsTypeDef(TypedDict):
    invocationId: NotRequired[str]
    returnControlInvocationResults: NotRequired[List[InvocationResultMemberOutputTypeDef]]

class InvocationResultMemberTypeDef(TypedDict):
    apiResult: NotRequired[ApiResultUnionTypeDef]
    functionResult: NotRequired[FunctionResultUnionTypeDef]

class InputFileTypeDef(TypedDict):
    name: str
    source: FileSourceTypeDef
    useCase: FileUseCaseType

class VectorSearchBedrockRerankingConfigurationTypeDef(TypedDict):
    modelConfiguration: VectorSearchBedrockRerankingModelConfigurationTypeDef
    metadataConfiguration: NotRequired[MetadataConfigurationForRerankingTypeDef]
    numberOfRerankedResults: NotRequired[int]

class FlowTraceTypeDef(TypedDict):
    conditionNodeResultTrace: NotRequired[FlowTraceConditionNodeResultEventTypeDef]
    nodeInputTrace: NotRequired[FlowTraceNodeInputEventTypeDef]
    nodeOutputTrace: NotRequired[FlowTraceNodeOutputEventTypeDef]

class AgentActionGroupTypeDef(TypedDict):
    actionGroupName: str
    actionGroupExecutor: NotRequired[ActionGroupExecutorTypeDef]
    apiSchema: NotRequired[APISchemaTypeDef]
    description: NotRequired[str]
    functionSchema: NotRequired[FunctionSchemaTypeDef]
    parentActionGroupSignature: NotRequired[ActionGroupSignatureType]

class GuardrailTraceTypeDef(TypedDict):
    action: NotRequired[GuardrailActionType]
    inputAssessments: NotRequired[List[GuardrailAssessmentTypeDef]]
    outputAssessments: NotRequired[List[GuardrailAssessmentTypeDef]]
    traceId: NotRequired[str]

class ExternalSourcesRetrieveAndGenerateConfigurationTypeDef(TypedDict):
    modelArn: str
    sources: Sequence[ExternalSourceTypeDef]
    generationConfiguration: NotRequired[ExternalSourcesGenerationConfigurationTypeDef]

class PromptOverrideConfigurationTypeDef(TypedDict):
    promptConfigurations: Sequence[PromptConfigurationTypeDef]
    overrideLambda: NotRequired[str]

class OptimizedPromptStreamTypeDef(TypedDict):
    accessDeniedException: NotRequired[AccessDeniedExceptionTypeDef]
    analyzePromptEvent: NotRequired[AnalyzePromptEventTypeDef]
    badGatewayException: NotRequired[BadGatewayExceptionTypeDef]
    dependencyFailedException: NotRequired[DependencyFailedExceptionTypeDef]
    internalServerException: NotRequired[InternalServerExceptionTypeDef]
    optimizedPromptEvent: NotRequired[OptimizedPromptEventTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]

class PostProcessingTraceTypeDef(TypedDict):
    modelInvocationInput: NotRequired[ModelInvocationInputTypeDef]
    modelInvocationOutput: NotRequired[PostProcessingModelInvocationOutputTypeDef]

class PreProcessingTraceTypeDef(TypedDict):
    modelInvocationInput: NotRequired[ModelInvocationInputTypeDef]
    modelInvocationOutput: NotRequired[PreProcessingModelInvocationOutputTypeDef]

class RerankResponseTypeDef(TypedDict):
    results: List[RerankResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

RerankSourceTypeDef = TypedDict(
    "RerankSourceTypeDef",
    {
        "inlineDocumentSource": RerankDocumentUnionTypeDef,
        "type": Literal["INLINE"],
    },
)

class RetrieveResponseTypeDef(TypedDict):
    guardrailAction: GuadrailActionType
    retrievalResults: List[KnowledgeBaseRetrievalResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class KnowledgeBaseLookupOutputTypeDef(TypedDict):
    retrievedReferences: NotRequired[List[RetrievedReferenceTypeDef]]

class CitationTypeDef(TypedDict):
    generatedResponsePart: NotRequired[GeneratedResponsePartTypeDef]
    retrievedReferences: NotRequired[List[RetrievedReferenceTypeDef]]

class GenerateQueryRequestRequestTypeDef(TypedDict):
    queryGenerationInput: QueryGenerationInputTypeDef
    transformationConfiguration: TransformationConfigurationTypeDef

class InvocationInputMemberTypeDef(TypedDict):
    apiInvocationInput: NotRequired[ApiInvocationInputTypeDef]
    functionInvocationInput: NotRequired[FunctionInvocationInputTypeDef]

AgentCollaboratorInputPayloadTypeDef = TypedDict(
    "AgentCollaboratorInputPayloadTypeDef",
    {
        "returnControlResults": NotRequired[ReturnControlResultsTypeDef],
        "text": NotRequired[str],
        "type": NotRequired[PayloadTypeType],
    },
)
InvocationResultMemberUnionTypeDef = Union[
    InvocationResultMemberTypeDef, InvocationResultMemberOutputTypeDef
]
VectorSearchRerankingConfigurationTypeDef = TypedDict(
    "VectorSearchRerankingConfigurationTypeDef",
    {
        "type": Literal["BEDROCK_RERANKING_MODEL"],
        "bedrockRerankingConfiguration": NotRequired[
            VectorSearchBedrockRerankingConfigurationTypeDef
        ],
    },
)

class FlowTraceEventTypeDef(TypedDict):
    trace: FlowTraceTypeDef

class OptimizePromptResponseTypeDef(TypedDict):
    optimizedPrompt: "EventStream[OptimizedPromptStreamTypeDef]"
    ResponseMetadata: ResponseMetadataTypeDef

class RerankRequestRequestTypeDef(TypedDict):
    queries: Sequence[RerankQueryTypeDef]
    rerankingConfiguration: RerankingConfigurationTypeDef
    sources: Sequence[RerankSourceTypeDef]
    nextToken: NotRequired[str]

class RerankRequestRerankPaginateTypeDef(TypedDict):
    queries: Sequence[RerankQueryTypeDef]
    rerankingConfiguration: RerankingConfigurationTypeDef
    sources: Sequence[RerankSourceTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class AttributionTypeDef(TypedDict):
    citations: NotRequired[List[CitationTypeDef]]

class CitationEventTypeDef(TypedDict):
    citation: NotRequired[CitationTypeDef]

class RetrieveAndGenerateResponseTypeDef(TypedDict):
    citations: List[CitationTypeDef]
    guardrailAction: GuadrailActionType
    output: RetrieveAndGenerateOutputTypeDef
    sessionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class InlineAgentReturnControlPayloadTypeDef(TypedDict):
    invocationId: NotRequired[str]
    invocationInputs: NotRequired[List[InvocationInputMemberTypeDef]]

class ReturnControlPayloadTypeDef(TypedDict):
    invocationId: NotRequired[str]
    invocationInputs: NotRequired[List[InvocationInputMemberTypeDef]]

AgentCollaboratorInvocationInputTypeDef = TypedDict(
    "AgentCollaboratorInvocationInputTypeDef",
    {
        "agentCollaboratorAliasArn": NotRequired[str],
        "agentCollaboratorName": NotRequired[str],
        "input": NotRequired[AgentCollaboratorInputPayloadTypeDef],
    },
)

class InlineSessionStateTypeDef(TypedDict):
    files: NotRequired[Sequence[InputFileTypeDef]]
    invocationId: NotRequired[str]
    promptSessionAttributes: NotRequired[Mapping[str, str]]
    returnControlInvocationResults: NotRequired[Sequence[InvocationResultMemberUnionTypeDef]]
    sessionAttributes: NotRequired[Mapping[str, str]]

KnowledgeBaseVectorSearchConfigurationPaginatorTypeDef = TypedDict(
    "KnowledgeBaseVectorSearchConfigurationPaginatorTypeDef",
    {
        "filter": NotRequired[RetrievalFilterPaginatorTypeDef],
        "implicitFilterConfiguration": NotRequired[ImplicitFilterConfigurationTypeDef],
        "numberOfResults": NotRequired[int],
        "overrideSearchType": NotRequired[SearchTypeType],
        "rerankingConfiguration": NotRequired[VectorSearchRerankingConfigurationTypeDef],
    },
)
KnowledgeBaseVectorSearchConfigurationTypeDef = TypedDict(
    "KnowledgeBaseVectorSearchConfigurationTypeDef",
    {
        "filter": NotRequired[RetrievalFilterTypeDef],
        "implicitFilterConfiguration": NotRequired[ImplicitFilterConfigurationTypeDef],
        "numberOfResults": NotRequired[int],
        "overrideSearchType": NotRequired[SearchTypeType],
        "rerankingConfiguration": NotRequired[VectorSearchRerankingConfigurationTypeDef],
    },
)

class FlowResponseStreamTypeDef(TypedDict):
    accessDeniedException: NotRequired[AccessDeniedExceptionTypeDef]
    badGatewayException: NotRequired[BadGatewayExceptionTypeDef]
    conflictException: NotRequired[ConflictExceptionTypeDef]
    dependencyFailedException: NotRequired[DependencyFailedExceptionTypeDef]
    flowCompletionEvent: NotRequired[FlowCompletionEventTypeDef]
    flowOutputEvent: NotRequired[FlowOutputEventTypeDef]
    flowTraceEvent: NotRequired[FlowTraceEventTypeDef]
    internalServerException: NotRequired[InternalServerExceptionTypeDef]
    resourceNotFoundException: NotRequired[ResourceNotFoundExceptionTypeDef]
    serviceQuotaExceededException: NotRequired[ServiceQuotaExceededExceptionTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]

InlineAgentPayloadPartTypeDef = TypedDict(
    "InlineAgentPayloadPartTypeDef",
    {
        "attribution": NotRequired[AttributionTypeDef],
        "bytes": NotRequired[bytes],
    },
)
PayloadPartTypeDef = TypedDict(
    "PayloadPartTypeDef",
    {
        "attribution": NotRequired[AttributionTypeDef],
        "bytes": NotRequired[bytes],
    },
)

class RetrieveAndGenerateStreamResponseOutputTypeDef(TypedDict):
    accessDeniedException: NotRequired[AccessDeniedExceptionTypeDef]
    badGatewayException: NotRequired[BadGatewayExceptionTypeDef]
    citation: NotRequired[CitationEventTypeDef]
    conflictException: NotRequired[ConflictExceptionTypeDef]
    dependencyFailedException: NotRequired[DependencyFailedExceptionTypeDef]
    guardrail: NotRequired[GuardrailEventTypeDef]
    internalServerException: NotRequired[InternalServerExceptionTypeDef]
    output: NotRequired[RetrieveAndGenerateOutputEventTypeDef]
    resourceNotFoundException: NotRequired[ResourceNotFoundExceptionTypeDef]
    serviceQuotaExceededException: NotRequired[ServiceQuotaExceededExceptionTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]

AgentCollaboratorOutputPayloadTypeDef = TypedDict(
    "AgentCollaboratorOutputPayloadTypeDef",
    {
        "returnControlPayload": NotRequired[ReturnControlPayloadTypeDef],
        "text": NotRequired[str],
        "type": NotRequired[PayloadTypeType],
    },
)

class InvocationInputTypeDef(TypedDict):
    actionGroupInvocationInput: NotRequired[ActionGroupInvocationInputTypeDef]
    agentCollaboratorInvocationInput: NotRequired[AgentCollaboratorInvocationInputTypeDef]
    codeInterpreterInvocationInput: NotRequired[CodeInterpreterInvocationInputTypeDef]
    invocationType: NotRequired[InvocationTypeType]
    knowledgeBaseLookupInput: NotRequired[KnowledgeBaseLookupInputTypeDef]
    traceId: NotRequired[str]

class KnowledgeBaseRetrievalConfigurationPaginatorTypeDef(TypedDict):
    vectorSearchConfiguration: KnowledgeBaseVectorSearchConfigurationPaginatorTypeDef

class KnowledgeBaseRetrievalConfigurationTypeDef(TypedDict):
    vectorSearchConfiguration: KnowledgeBaseVectorSearchConfigurationTypeDef

class InvokeFlowResponseTypeDef(TypedDict):
    responseStream: "EventStream[FlowResponseStreamTypeDef]"
    ResponseMetadata: ResponseMetadataTypeDef

class RetrieveAndGenerateStreamResponseTypeDef(TypedDict):
    sessionId: str
    stream: "EventStream[RetrieveAndGenerateStreamResponseOutputTypeDef]"
    ResponseMetadata: ResponseMetadataTypeDef

class AgentCollaboratorInvocationOutputTypeDef(TypedDict):
    agentCollaboratorAliasArn: NotRequired[str]
    agentCollaboratorName: NotRequired[str]
    output: NotRequired[AgentCollaboratorOutputPayloadTypeDef]

class RetrieveRequestRetrievePaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    retrievalQuery: KnowledgeBaseQueryTypeDef
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    retrievalConfiguration: NotRequired[KnowledgeBaseRetrievalConfigurationPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class KnowledgeBaseConfigurationTypeDef(TypedDict):
    knowledgeBaseId: str
    retrievalConfiguration: KnowledgeBaseRetrievalConfigurationTypeDef

class KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef(TypedDict):
    knowledgeBaseId: str
    modelArn: str
    generationConfiguration: NotRequired[GenerationConfigurationTypeDef]
    orchestrationConfiguration: NotRequired[OrchestrationConfigurationTypeDef]
    retrievalConfiguration: NotRequired[KnowledgeBaseRetrievalConfigurationTypeDef]

class KnowledgeBaseTypeDef(TypedDict):
    description: str
    knowledgeBaseId: str
    retrievalConfiguration: NotRequired[KnowledgeBaseRetrievalConfigurationTypeDef]

class RetrieveRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    retrievalQuery: KnowledgeBaseQueryTypeDef
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    nextToken: NotRequired[str]
    retrievalConfiguration: NotRequired[KnowledgeBaseRetrievalConfigurationTypeDef]

ObservationTypeDef = TypedDict(
    "ObservationTypeDef",
    {
        "actionGroupInvocationOutput": NotRequired[ActionGroupInvocationOutputTypeDef],
        "agentCollaboratorInvocationOutput": NotRequired[AgentCollaboratorInvocationOutputTypeDef],
        "codeInterpreterInvocationOutput": NotRequired[CodeInterpreterInvocationOutputTypeDef],
        "finalResponse": NotRequired[FinalResponseTypeDef],
        "knowledgeBaseLookupOutput": NotRequired[KnowledgeBaseLookupOutputTypeDef],
        "repromptResponse": NotRequired[RepromptResponseTypeDef],
        "traceId": NotRequired[str],
        "type": NotRequired[TypeType],
    },
)

class SessionStateTypeDef(TypedDict):
    conversationHistory: NotRequired[ConversationHistoryTypeDef]
    files: NotRequired[Sequence[InputFileTypeDef]]
    invocationId: NotRequired[str]
    knowledgeBaseConfigurations: NotRequired[Sequence[KnowledgeBaseConfigurationTypeDef]]
    promptSessionAttributes: NotRequired[Mapping[str, str]]
    returnControlInvocationResults: NotRequired[Sequence[InvocationResultMemberUnionTypeDef]]
    sessionAttributes: NotRequired[Mapping[str, str]]

RetrieveAndGenerateConfigurationTypeDef = TypedDict(
    "RetrieveAndGenerateConfigurationTypeDef",
    {
        "type": RetrieveAndGenerateTypeType,
        "externalSourcesConfiguration": NotRequired[
            ExternalSourcesRetrieveAndGenerateConfigurationTypeDef
        ],
        "knowledgeBaseConfiguration": NotRequired[
            KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef
        ],
    },
)

class InvokeInlineAgentRequestRequestTypeDef(TypedDict):
    foundationModel: str
    instruction: str
    sessionId: str
    actionGroups: NotRequired[Sequence[AgentActionGroupTypeDef]]
    customerEncryptionKeyArn: NotRequired[str]
    enableTrace: NotRequired[bool]
    endSession: NotRequired[bool]
    guardrailConfiguration: NotRequired[GuardrailConfigurationWithArnTypeDef]
    idleSessionTTLInSeconds: NotRequired[int]
    inlineSessionState: NotRequired[InlineSessionStateTypeDef]
    inputText: NotRequired[str]
    knowledgeBases: NotRequired[Sequence[KnowledgeBaseTypeDef]]
    promptOverrideConfiguration: NotRequired[PromptOverrideConfigurationTypeDef]

class OrchestrationTraceTypeDef(TypedDict):
    invocationInput: NotRequired[InvocationInputTypeDef]
    modelInvocationInput: NotRequired[ModelInvocationInputTypeDef]
    modelInvocationOutput: NotRequired[OrchestrationModelInvocationOutputTypeDef]
    observation: NotRequired[ObservationTypeDef]
    rationale: NotRequired[RationaleTypeDef]

class RoutingClassifierTraceTypeDef(TypedDict):
    invocationInput: NotRequired[InvocationInputTypeDef]
    modelInvocationInput: NotRequired[ModelInvocationInputTypeDef]
    modelInvocationOutput: NotRequired[RoutingClassifierModelInvocationOutputTypeDef]
    observation: NotRequired[ObservationTypeDef]

class InvokeAgentRequestRequestTypeDef(TypedDict):
    agentAliasId: str
    agentId: str
    sessionId: str
    enableTrace: NotRequired[bool]
    endSession: NotRequired[bool]
    inputText: NotRequired[str]
    memoryId: NotRequired[str]
    sessionState: NotRequired[SessionStateTypeDef]
    sourceArn: NotRequired[str]
    streamingConfigurations: NotRequired[StreamingConfigurationsTypeDef]

RetrieveAndGenerateRequestRequestTypeDef = TypedDict(
    "RetrieveAndGenerateRequestRequestTypeDef",
    {
        "input": RetrieveAndGenerateInputTypeDef,
        "retrieveAndGenerateConfiguration": NotRequired[RetrieveAndGenerateConfigurationTypeDef],
        "sessionConfiguration": NotRequired[RetrieveAndGenerateSessionConfigurationTypeDef],
        "sessionId": NotRequired[str],
    },
)
RetrieveAndGenerateStreamRequestRequestTypeDef = TypedDict(
    "RetrieveAndGenerateStreamRequestRequestTypeDef",
    {
        "input": RetrieveAndGenerateInputTypeDef,
        "retrieveAndGenerateConfiguration": NotRequired[RetrieveAndGenerateConfigurationTypeDef],
        "sessionConfiguration": NotRequired[RetrieveAndGenerateSessionConfigurationTypeDef],
        "sessionId": NotRequired[str],
    },
)

class TraceTypeDef(TypedDict):
    customOrchestrationTrace: NotRequired[CustomOrchestrationTraceTypeDef]
    failureTrace: NotRequired[FailureTraceTypeDef]
    guardrailTrace: NotRequired[GuardrailTraceTypeDef]
    orchestrationTrace: NotRequired[OrchestrationTraceTypeDef]
    postProcessingTrace: NotRequired[PostProcessingTraceTypeDef]
    preProcessingTrace: NotRequired[PreProcessingTraceTypeDef]
    routingClassifierTrace: NotRequired[RoutingClassifierTraceTypeDef]

class InlineAgentTracePartTypeDef(TypedDict):
    sessionId: NotRequired[str]
    trace: NotRequired[TraceTypeDef]

class TracePartTypeDef(TypedDict):
    agentAliasId: NotRequired[str]
    agentId: NotRequired[str]
    agentVersion: NotRequired[str]
    callerChain: NotRequired[List[CallerTypeDef]]
    collaboratorName: NotRequired[str]
    sessionId: NotRequired[str]
    trace: NotRequired[TraceTypeDef]

class InlineAgentResponseStreamTypeDef(TypedDict):
    accessDeniedException: NotRequired[AccessDeniedExceptionTypeDef]
    badGatewayException: NotRequired[BadGatewayExceptionTypeDef]
    chunk: NotRequired[InlineAgentPayloadPartTypeDef]
    conflictException: NotRequired[ConflictExceptionTypeDef]
    dependencyFailedException: NotRequired[DependencyFailedExceptionTypeDef]
    files: NotRequired[InlineAgentFilePartTypeDef]
    internalServerException: NotRequired[InternalServerExceptionTypeDef]
    resourceNotFoundException: NotRequired[ResourceNotFoundExceptionTypeDef]
    returnControl: NotRequired[InlineAgentReturnControlPayloadTypeDef]
    serviceQuotaExceededException: NotRequired[ServiceQuotaExceededExceptionTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]
    trace: NotRequired[InlineAgentTracePartTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]

class ResponseStreamTypeDef(TypedDict):
    accessDeniedException: NotRequired[AccessDeniedExceptionTypeDef]
    badGatewayException: NotRequired[BadGatewayExceptionTypeDef]
    chunk: NotRequired[PayloadPartTypeDef]
    conflictException: NotRequired[ConflictExceptionTypeDef]
    dependencyFailedException: NotRequired[DependencyFailedExceptionTypeDef]
    files: NotRequired[FilePartTypeDef]
    internalServerException: NotRequired[InternalServerExceptionTypeDef]
    resourceNotFoundException: NotRequired[ResourceNotFoundExceptionTypeDef]
    returnControl: NotRequired[ReturnControlPayloadTypeDef]
    serviceQuotaExceededException: NotRequired[ServiceQuotaExceededExceptionTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]
    trace: NotRequired[TracePartTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]

class InvokeInlineAgentResponseTypeDef(TypedDict):
    completion: "EventStream[InlineAgentResponseStreamTypeDef]"
    contentType: str
    sessionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class InvokeAgentResponseTypeDef(TypedDict):
    completion: "EventStream[ResponseStreamTypeDef]"
    contentType: str
    memoryId: str
    sessionId: str
    ResponseMetadata: ResponseMetadataTypeDef
