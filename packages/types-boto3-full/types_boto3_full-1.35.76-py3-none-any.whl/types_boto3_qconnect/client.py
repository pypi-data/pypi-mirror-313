"""
Type annotations for qconnect service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_qconnect.client import QConnectClient

    session = Session()
    client: QConnectClient = session.client("qconnect")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAIAgentsPaginator,
    ListAIAgentVersionsPaginator,
    ListAIGuardrailsPaginator,
    ListAIGuardrailVersionsPaginator,
    ListAIPromptsPaginator,
    ListAIPromptVersionsPaginator,
    ListAssistantAssociationsPaginator,
    ListAssistantsPaginator,
    ListContentAssociationsPaginator,
    ListContentsPaginator,
    ListImportJobsPaginator,
    ListKnowledgeBasesPaginator,
    ListMessagesPaginator,
    ListMessageTemplatesPaginator,
    ListMessageTemplateVersionsPaginator,
    ListQuickResponsesPaginator,
    QueryAssistantPaginator,
    SearchContentPaginator,
    SearchMessageTemplatesPaginator,
    SearchQuickResponsesPaginator,
    SearchSessionsPaginator,
)
from .type_defs import (
    ActivateMessageTemplateRequestRequestTypeDef,
    ActivateMessageTemplateResponseTypeDef,
    CreateAIAgentRequestRequestTypeDef,
    CreateAIAgentResponseTypeDef,
    CreateAIAgentVersionRequestRequestTypeDef,
    CreateAIAgentVersionResponseTypeDef,
    CreateAIGuardrailRequestRequestTypeDef,
    CreateAIGuardrailResponseTypeDef,
    CreateAIGuardrailVersionRequestRequestTypeDef,
    CreateAIGuardrailVersionResponseTypeDef,
    CreateAIPromptRequestRequestTypeDef,
    CreateAIPromptResponseTypeDef,
    CreateAIPromptVersionRequestRequestTypeDef,
    CreateAIPromptVersionResponseTypeDef,
    CreateAssistantAssociationRequestRequestTypeDef,
    CreateAssistantAssociationResponseTypeDef,
    CreateAssistantRequestRequestTypeDef,
    CreateAssistantResponseTypeDef,
    CreateContentAssociationRequestRequestTypeDef,
    CreateContentAssociationResponseTypeDef,
    CreateContentRequestRequestTypeDef,
    CreateContentResponseTypeDef,
    CreateKnowledgeBaseRequestRequestTypeDef,
    CreateKnowledgeBaseResponseTypeDef,
    CreateMessageTemplateAttachmentRequestRequestTypeDef,
    CreateMessageTemplateAttachmentResponseTypeDef,
    CreateMessageTemplateRequestRequestTypeDef,
    CreateMessageTemplateResponseTypeDef,
    CreateMessageTemplateVersionRequestRequestTypeDef,
    CreateMessageTemplateVersionResponseTypeDef,
    CreateQuickResponseRequestRequestTypeDef,
    CreateQuickResponseResponseTypeDef,
    CreateSessionRequestRequestTypeDef,
    CreateSessionResponseTypeDef,
    DeactivateMessageTemplateRequestRequestTypeDef,
    DeactivateMessageTemplateResponseTypeDef,
    DeleteAIAgentRequestRequestTypeDef,
    DeleteAIAgentVersionRequestRequestTypeDef,
    DeleteAIGuardrailRequestRequestTypeDef,
    DeleteAIGuardrailVersionRequestRequestTypeDef,
    DeleteAIPromptRequestRequestTypeDef,
    DeleteAIPromptVersionRequestRequestTypeDef,
    DeleteAssistantAssociationRequestRequestTypeDef,
    DeleteAssistantRequestRequestTypeDef,
    DeleteContentAssociationRequestRequestTypeDef,
    DeleteContentRequestRequestTypeDef,
    DeleteImportJobRequestRequestTypeDef,
    DeleteKnowledgeBaseRequestRequestTypeDef,
    DeleteMessageTemplateAttachmentRequestRequestTypeDef,
    DeleteMessageTemplateRequestRequestTypeDef,
    DeleteQuickResponseRequestRequestTypeDef,
    GetAIAgentRequestRequestTypeDef,
    GetAIAgentResponseTypeDef,
    GetAIGuardrailRequestRequestTypeDef,
    GetAIGuardrailResponseTypeDef,
    GetAIPromptRequestRequestTypeDef,
    GetAIPromptResponseTypeDef,
    GetAssistantAssociationRequestRequestTypeDef,
    GetAssistantAssociationResponseTypeDef,
    GetAssistantRequestRequestTypeDef,
    GetAssistantResponseTypeDef,
    GetContentAssociationRequestRequestTypeDef,
    GetContentAssociationResponseTypeDef,
    GetContentRequestRequestTypeDef,
    GetContentResponseTypeDef,
    GetContentSummaryRequestRequestTypeDef,
    GetContentSummaryResponseTypeDef,
    GetImportJobRequestRequestTypeDef,
    GetImportJobResponseTypeDef,
    GetKnowledgeBaseRequestRequestTypeDef,
    GetKnowledgeBaseResponseTypeDef,
    GetMessageTemplateRequestRequestTypeDef,
    GetMessageTemplateResponseTypeDef,
    GetNextMessageRequestRequestTypeDef,
    GetNextMessageResponseTypeDef,
    GetQuickResponseRequestRequestTypeDef,
    GetQuickResponseResponseTypeDef,
    GetRecommendationsRequestRequestTypeDef,
    GetRecommendationsResponseTypeDef,
    GetSessionRequestRequestTypeDef,
    GetSessionResponseTypeDef,
    ListAIAgentsRequestRequestTypeDef,
    ListAIAgentsResponseTypeDef,
    ListAIAgentVersionsRequestRequestTypeDef,
    ListAIAgentVersionsResponseTypeDef,
    ListAIGuardrailsRequestRequestTypeDef,
    ListAIGuardrailsResponseTypeDef,
    ListAIGuardrailVersionsRequestRequestTypeDef,
    ListAIGuardrailVersionsResponseTypeDef,
    ListAIPromptsRequestRequestTypeDef,
    ListAIPromptsResponseTypeDef,
    ListAIPromptVersionsRequestRequestTypeDef,
    ListAIPromptVersionsResponseTypeDef,
    ListAssistantAssociationsRequestRequestTypeDef,
    ListAssistantAssociationsResponseTypeDef,
    ListAssistantsRequestRequestTypeDef,
    ListAssistantsResponseTypeDef,
    ListContentAssociationsRequestRequestTypeDef,
    ListContentAssociationsResponseTypeDef,
    ListContentsRequestRequestTypeDef,
    ListContentsResponseTypeDef,
    ListImportJobsRequestRequestTypeDef,
    ListImportJobsResponseTypeDef,
    ListKnowledgeBasesRequestRequestTypeDef,
    ListKnowledgeBasesResponseTypeDef,
    ListMessagesRequestRequestTypeDef,
    ListMessagesResponseTypeDef,
    ListMessageTemplatesRequestRequestTypeDef,
    ListMessageTemplatesResponseTypeDef,
    ListMessageTemplateVersionsRequestRequestTypeDef,
    ListMessageTemplateVersionsResponseTypeDef,
    ListQuickResponsesRequestRequestTypeDef,
    ListQuickResponsesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    NotifyRecommendationsReceivedRequestRequestTypeDef,
    NotifyRecommendationsReceivedResponseTypeDef,
    PutFeedbackRequestRequestTypeDef,
    PutFeedbackResponseTypeDef,
    QueryAssistantRequestRequestTypeDef,
    QueryAssistantResponseTypeDef,
    RemoveAssistantAIAgentRequestRequestTypeDef,
    RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef,
    RenderMessageTemplateRequestRequestTypeDef,
    RenderMessageTemplateResponseTypeDef,
    SearchContentRequestRequestTypeDef,
    SearchContentResponseTypeDef,
    SearchMessageTemplatesRequestRequestTypeDef,
    SearchMessageTemplatesResponseTypeDef,
    SearchQuickResponsesRequestRequestTypeDef,
    SearchQuickResponsesResponseTypeDef,
    SearchSessionsRequestRequestTypeDef,
    SearchSessionsResponseTypeDef,
    SendMessageRequestRequestTypeDef,
    SendMessageResponseTypeDef,
    StartContentUploadRequestRequestTypeDef,
    StartContentUploadResponseTypeDef,
    StartImportJobRequestRequestTypeDef,
    StartImportJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAIAgentRequestRequestTypeDef,
    UpdateAIAgentResponseTypeDef,
    UpdateAIGuardrailRequestRequestTypeDef,
    UpdateAIGuardrailResponseTypeDef,
    UpdateAIPromptRequestRequestTypeDef,
    UpdateAIPromptResponseTypeDef,
    UpdateAssistantAIAgentRequestRequestTypeDef,
    UpdateAssistantAIAgentResponseTypeDef,
    UpdateContentRequestRequestTypeDef,
    UpdateContentResponseTypeDef,
    UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef,
    UpdateKnowledgeBaseTemplateUriResponseTypeDef,
    UpdateMessageTemplateMetadataRequestRequestTypeDef,
    UpdateMessageTemplateMetadataResponseTypeDef,
    UpdateMessageTemplateRequestRequestTypeDef,
    UpdateMessageTemplateResponseTypeDef,
    UpdateQuickResponseRequestRequestTypeDef,
    UpdateQuickResponseResponseTypeDef,
    UpdateSessionDataRequestRequestTypeDef,
    UpdateSessionDataResponseTypeDef,
    UpdateSessionRequestRequestTypeDef,
    UpdateSessionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("QConnectClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    PreconditionFailedException: Type[BotocoreClientError]
    RequestTimeoutException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class QConnectClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        QConnectClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#close)
        """

    def activate_message_template(
        self, **kwargs: Unpack[ActivateMessageTemplateRequestRequestTypeDef]
    ) -> ActivateMessageTemplateResponseTypeDef:
        """
        Activates a specific version of the Amazon Q in Connect message template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/activate_message_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#activate_message_template)
        """

    def create_ai_agent(
        self, **kwargs: Unpack[CreateAIAgentRequestRequestTypeDef]
    ) -> CreateAIAgentResponseTypeDef:
        """
        Creates an Amazon Q in Connect AI Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_ai_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_ai_agent)
        """

    def create_ai_agent_version(
        self, **kwargs: Unpack[CreateAIAgentVersionRequestRequestTypeDef]
    ) -> CreateAIAgentVersionResponseTypeDef:
        """
        Creates and Amazon Q in Connect AI Agent version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_ai_agent_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_ai_agent_version)
        """

    def create_ai_guardrail(
        self, **kwargs: Unpack[CreateAIGuardrailRequestRequestTypeDef]
    ) -> CreateAIGuardrailResponseTypeDef:
        """
        Creates an Amazon Q in Connect AI Guardrail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_ai_guardrail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_ai_guardrail)
        """

    def create_ai_guardrail_version(
        self, **kwargs: Unpack[CreateAIGuardrailVersionRequestRequestTypeDef]
    ) -> CreateAIGuardrailVersionResponseTypeDef:
        """
        Creates an Amazon Q in Connect AI Guardrail version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_ai_guardrail_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_ai_guardrail_version)
        """

    def create_ai_prompt(
        self, **kwargs: Unpack[CreateAIPromptRequestRequestTypeDef]
    ) -> CreateAIPromptResponseTypeDef:
        """
        Creates an Amazon Q in Connect AI Prompt.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_ai_prompt.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_ai_prompt)
        """

    def create_ai_prompt_version(
        self, **kwargs: Unpack[CreateAIPromptVersionRequestRequestTypeDef]
    ) -> CreateAIPromptVersionResponseTypeDef:
        """
        Creates an Amazon Q in Connect AI Prompt version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_ai_prompt_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_ai_prompt_version)
        """

    def create_assistant(
        self, **kwargs: Unpack[CreateAssistantRequestRequestTypeDef]
    ) -> CreateAssistantResponseTypeDef:
        """
        Creates an Amazon Q in Connect assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_assistant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_assistant)
        """

    def create_assistant_association(
        self, **kwargs: Unpack[CreateAssistantAssociationRequestRequestTypeDef]
    ) -> CreateAssistantAssociationResponseTypeDef:
        """
        Creates an association between an Amazon Q in Connect assistant and another
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_assistant_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_assistant_association)
        """

    def create_content(
        self, **kwargs: Unpack[CreateContentRequestRequestTypeDef]
    ) -> CreateContentResponseTypeDef:
        """
        Creates Amazon Q in Connect content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_content)
        """

    def create_content_association(
        self, **kwargs: Unpack[CreateContentAssociationRequestRequestTypeDef]
    ) -> CreateContentAssociationResponseTypeDef:
        """
        Creates an association between a content resource in a knowledge base and <a
        href="https://docs.aws.amazon.com/connect/latest/adminguide/step-by-step-guided-experiences.html">step-by-step
        guides</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_content_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_content_association)
        """

    def create_knowledge_base(
        self, **kwargs: Unpack[CreateKnowledgeBaseRequestRequestTypeDef]
    ) -> CreateKnowledgeBaseResponseTypeDef:
        """
        Creates a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_knowledge_base.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_knowledge_base)
        """

    def create_message_template(
        self, **kwargs: Unpack[CreateMessageTemplateRequestRequestTypeDef]
    ) -> CreateMessageTemplateResponseTypeDef:
        """
        Creates an Amazon Q in Connect message template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_message_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_message_template)
        """

    def create_message_template_attachment(
        self, **kwargs: Unpack[CreateMessageTemplateAttachmentRequestRequestTypeDef]
    ) -> CreateMessageTemplateAttachmentResponseTypeDef:
        """
        Uploads an attachment file to the specified Amazon Q in Connect message
        template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_message_template_attachment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_message_template_attachment)
        """

    def create_message_template_version(
        self, **kwargs: Unpack[CreateMessageTemplateVersionRequestRequestTypeDef]
    ) -> CreateMessageTemplateVersionResponseTypeDef:
        """
        Creates a new Amazon Q in Connect message template version from the current
        content and configuration of a message template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_message_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_message_template_version)
        """

    def create_quick_response(
        self, **kwargs: Unpack[CreateQuickResponseRequestRequestTypeDef]
    ) -> CreateQuickResponseResponseTypeDef:
        """
        Creates an Amazon Q in Connect quick response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_quick_response.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_quick_response)
        """

    def create_session(
        self, **kwargs: Unpack[CreateSessionRequestRequestTypeDef]
    ) -> CreateSessionResponseTypeDef:
        """
        Creates a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/create_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#create_session)
        """

    def deactivate_message_template(
        self, **kwargs: Unpack[DeactivateMessageTemplateRequestRequestTypeDef]
    ) -> DeactivateMessageTemplateResponseTypeDef:
        """
        Deactivates a specific version of the Amazon Q in Connect message template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/deactivate_message_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#deactivate_message_template)
        """

    def delete_ai_agent(
        self, **kwargs: Unpack[DeleteAIAgentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Q in Connect AI Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_ai_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_ai_agent)
        """

    def delete_ai_agent_version(
        self, **kwargs: Unpack[DeleteAIAgentVersionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Q in Connect AI Agent Version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_ai_agent_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_ai_agent_version)
        """

    def delete_ai_guardrail(
        self, **kwargs: Unpack[DeleteAIGuardrailRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Q in Connect AI Guardrail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_ai_guardrail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_ai_guardrail)
        """

    def delete_ai_guardrail_version(
        self, **kwargs: Unpack[DeleteAIGuardrailVersionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete and Amazon Q in Connect AI Guardrail version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_ai_guardrail_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_ai_guardrail_version)
        """

    def delete_ai_prompt(
        self, **kwargs: Unpack[DeleteAIPromptRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Q in Connect AI Prompt.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_ai_prompt.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_ai_prompt)
        """

    def delete_ai_prompt_version(
        self, **kwargs: Unpack[DeleteAIPromptVersionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete and Amazon Q in Connect AI Prompt version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_ai_prompt_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_ai_prompt_version)
        """

    def delete_assistant(
        self, **kwargs: Unpack[DeleteAssistantRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_assistant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_assistant)
        """

    def delete_assistant_association(
        self, **kwargs: Unpack[DeleteAssistantAssociationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an assistant association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_assistant_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_assistant_association)
        """

    def delete_content(
        self, **kwargs: Unpack[DeleteContentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_content)
        """

    def delete_content_association(
        self, **kwargs: Unpack[DeleteContentAssociationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the content association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_content_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_content_association)
        """

    def delete_import_job(
        self, **kwargs: Unpack[DeleteImportJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the quick response import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_import_job)
        """

    def delete_knowledge_base(
        self, **kwargs: Unpack[DeleteKnowledgeBaseRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_knowledge_base.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_knowledge_base)
        """

    def delete_message_template(
        self, **kwargs: Unpack[DeleteMessageTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Q in Connect message template entirely or a specific version
        of the message template if version is supplied in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_message_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_message_template)
        """

    def delete_message_template_attachment(
        self, **kwargs: Unpack[DeleteMessageTemplateAttachmentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the attachment file from the Amazon Q in Connect message template that
        is referenced by <code>$LATEST</code> qualifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_message_template_attachment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_message_template_attachment)
        """

    def delete_quick_response(
        self, **kwargs: Unpack[DeleteQuickResponseRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a quick response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/delete_quick_response.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#delete_quick_response)
        """

    def get_ai_agent(
        self, **kwargs: Unpack[GetAIAgentRequestRequestTypeDef]
    ) -> GetAIAgentResponseTypeDef:
        """
        Gets an Amazon Q in Connect AI Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_ai_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_ai_agent)
        """

    def get_ai_guardrail(
        self, **kwargs: Unpack[GetAIGuardrailRequestRequestTypeDef]
    ) -> GetAIGuardrailResponseTypeDef:
        """
        Gets the Amazon Q in Connect AI Guardrail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_ai_guardrail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_ai_guardrail)
        """

    def get_ai_prompt(
        self, **kwargs: Unpack[GetAIPromptRequestRequestTypeDef]
    ) -> GetAIPromptResponseTypeDef:
        """
        Gets and Amazon Q in Connect AI Prompt.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_ai_prompt.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_ai_prompt)
        """

    def get_assistant(
        self, **kwargs: Unpack[GetAssistantRequestRequestTypeDef]
    ) -> GetAssistantResponseTypeDef:
        """
        Retrieves information about an assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_assistant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_assistant)
        """

    def get_assistant_association(
        self, **kwargs: Unpack[GetAssistantAssociationRequestRequestTypeDef]
    ) -> GetAssistantAssociationResponseTypeDef:
        """
        Retrieves information about an assistant association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_assistant_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_assistant_association)
        """

    def get_content(
        self, **kwargs: Unpack[GetContentRequestRequestTypeDef]
    ) -> GetContentResponseTypeDef:
        """
        Retrieves content, including a pre-signed URL to download the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_content)
        """

    def get_content_association(
        self, **kwargs: Unpack[GetContentAssociationRequestRequestTypeDef]
    ) -> GetContentAssociationResponseTypeDef:
        """
        Returns the content association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_content_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_content_association)
        """

    def get_content_summary(
        self, **kwargs: Unpack[GetContentSummaryRequestRequestTypeDef]
    ) -> GetContentSummaryResponseTypeDef:
        """
        Retrieves summary information about the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_content_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_content_summary)
        """

    def get_import_job(
        self, **kwargs: Unpack[GetImportJobRequestRequestTypeDef]
    ) -> GetImportJobResponseTypeDef:
        """
        Retrieves the started import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_import_job)
        """

    def get_knowledge_base(
        self, **kwargs: Unpack[GetKnowledgeBaseRequestRequestTypeDef]
    ) -> GetKnowledgeBaseResponseTypeDef:
        """
        Retrieves information about the knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_knowledge_base.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_knowledge_base)
        """

    def get_message_template(
        self, **kwargs: Unpack[GetMessageTemplateRequestRequestTypeDef]
    ) -> GetMessageTemplateResponseTypeDef:
        """
        Retrieves the Amazon Q in Connect message template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_message_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_message_template)
        """

    def get_next_message(
        self, **kwargs: Unpack[GetNextMessageRequestRequestTypeDef]
    ) -> GetNextMessageResponseTypeDef:
        """
        Retrieves next message on an Amazon Q in Connect session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_next_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_next_message)
        """

    def get_quick_response(
        self, **kwargs: Unpack[GetQuickResponseRequestRequestTypeDef]
    ) -> GetQuickResponseResponseTypeDef:
        """
        Retrieves the quick response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_quick_response.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_quick_response)
        """

    def get_recommendations(
        self, **kwargs: Unpack[GetRecommendationsRequestRequestTypeDef]
    ) -> GetRecommendationsResponseTypeDef:
        """
        This API will be discontinued starting June 1, 2024.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_recommendations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_recommendations)
        """

    def get_session(
        self, **kwargs: Unpack[GetSessionRequestRequestTypeDef]
    ) -> GetSessionResponseTypeDef:
        """
        Retrieves information for a specified session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_session)
        """

    def list_ai_agent_versions(
        self, **kwargs: Unpack[ListAIAgentVersionsRequestRequestTypeDef]
    ) -> ListAIAgentVersionsResponseTypeDef:
        """
        List AI Agent versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_ai_agent_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_ai_agent_versions)
        """

    def list_ai_agents(
        self, **kwargs: Unpack[ListAIAgentsRequestRequestTypeDef]
    ) -> ListAIAgentsResponseTypeDef:
        """
        Lists AI Agents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_ai_agents.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_ai_agents)
        """

    def list_ai_guardrail_versions(
        self, **kwargs: Unpack[ListAIGuardrailVersionsRequestRequestTypeDef]
    ) -> ListAIGuardrailVersionsResponseTypeDef:
        """
        Lists AI Guardrail versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_ai_guardrail_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_ai_guardrail_versions)
        """

    def list_ai_guardrails(
        self, **kwargs: Unpack[ListAIGuardrailsRequestRequestTypeDef]
    ) -> ListAIGuardrailsResponseTypeDef:
        """
        Lists the AI Guardrails available on the Amazon Q in Connect assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_ai_guardrails.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_ai_guardrails)
        """

    def list_ai_prompt_versions(
        self, **kwargs: Unpack[ListAIPromptVersionsRequestRequestTypeDef]
    ) -> ListAIPromptVersionsResponseTypeDef:
        """
        Lists AI Prompt versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_ai_prompt_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_ai_prompt_versions)
        """

    def list_ai_prompts(
        self, **kwargs: Unpack[ListAIPromptsRequestRequestTypeDef]
    ) -> ListAIPromptsResponseTypeDef:
        """
        Lists the AI Prompts available on the Amazon Q in Connect assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_ai_prompts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_ai_prompts)
        """

    def list_assistant_associations(
        self, **kwargs: Unpack[ListAssistantAssociationsRequestRequestTypeDef]
    ) -> ListAssistantAssociationsResponseTypeDef:
        """
        Lists information about assistant associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_assistant_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_assistant_associations)
        """

    def list_assistants(
        self, **kwargs: Unpack[ListAssistantsRequestRequestTypeDef]
    ) -> ListAssistantsResponseTypeDef:
        """
        Lists information about assistants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_assistants.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_assistants)
        """

    def list_content_associations(
        self, **kwargs: Unpack[ListContentAssociationsRequestRequestTypeDef]
    ) -> ListContentAssociationsResponseTypeDef:
        """
        Lists the content associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_content_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_content_associations)
        """

    def list_contents(
        self, **kwargs: Unpack[ListContentsRequestRequestTypeDef]
    ) -> ListContentsResponseTypeDef:
        """
        Lists the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_contents.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_contents)
        """

    def list_import_jobs(
        self, **kwargs: Unpack[ListImportJobsRequestRequestTypeDef]
    ) -> ListImportJobsResponseTypeDef:
        """
        Lists information about import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_import_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_import_jobs)
        """

    def list_knowledge_bases(
        self, **kwargs: Unpack[ListKnowledgeBasesRequestRequestTypeDef]
    ) -> ListKnowledgeBasesResponseTypeDef:
        """
        Lists the knowledge bases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_knowledge_bases.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_knowledge_bases)
        """

    def list_message_template_versions(
        self, **kwargs: Unpack[ListMessageTemplateVersionsRequestRequestTypeDef]
    ) -> ListMessageTemplateVersionsResponseTypeDef:
        """
        Lists all the available versions for the specified Amazon Q in Connect message
        template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_message_template_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_message_template_versions)
        """

    def list_message_templates(
        self, **kwargs: Unpack[ListMessageTemplatesRequestRequestTypeDef]
    ) -> ListMessageTemplatesResponseTypeDef:
        """
        Lists all the available Amazon Q in Connect message templates for the specified
        knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_message_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_message_templates)
        """

    def list_messages(
        self, **kwargs: Unpack[ListMessagesRequestRequestTypeDef]
    ) -> ListMessagesResponseTypeDef:
        """
        Lists messages on an Amazon Q in Connect session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_messages.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_messages)
        """

    def list_quick_responses(
        self, **kwargs: Unpack[ListQuickResponsesRequestRequestTypeDef]
    ) -> ListQuickResponsesResponseTypeDef:
        """
        Lists information about quick response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_quick_responses.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_quick_responses)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#list_tags_for_resource)
        """

    def notify_recommendations_received(
        self, **kwargs: Unpack[NotifyRecommendationsReceivedRequestRequestTypeDef]
    ) -> NotifyRecommendationsReceivedResponseTypeDef:
        """
        Removes the specified recommendations from the specified assistant's queue of
        newly available recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/notify_recommendations_received.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#notify_recommendations_received)
        """

    def put_feedback(
        self, **kwargs: Unpack[PutFeedbackRequestRequestTypeDef]
    ) -> PutFeedbackResponseTypeDef:
        """
        Provides feedback against the specified assistant for the specified target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/put_feedback.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#put_feedback)
        """

    def query_assistant(
        self, **kwargs: Unpack[QueryAssistantRequestRequestTypeDef]
    ) -> QueryAssistantResponseTypeDef:
        """
        This API will be discontinued starting June 1, 2024.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/query_assistant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#query_assistant)
        """

    def remove_assistant_ai_agent(
        self, **kwargs: Unpack[RemoveAssistantAIAgentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the AI Agent that is set for use by defafult on an Amazon Q in Connect
        Assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/remove_assistant_ai_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#remove_assistant_ai_agent)
        """

    def remove_knowledge_base_template_uri(
        self, **kwargs: Unpack[RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a URI template from a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/remove_knowledge_base_template_uri.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#remove_knowledge_base_template_uri)
        """

    def render_message_template(
        self, **kwargs: Unpack[RenderMessageTemplateRequestRequestTypeDef]
    ) -> RenderMessageTemplateResponseTypeDef:
        """
        Renders the Amazon Q in Connect message template based on the attribute values
        provided and generates the message content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/render_message_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#render_message_template)
        """

    def search_content(
        self, **kwargs: Unpack[SearchContentRequestRequestTypeDef]
    ) -> SearchContentResponseTypeDef:
        """
        Searches for content in a specified knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/search_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#search_content)
        """

    def search_message_templates(
        self, **kwargs: Unpack[SearchMessageTemplatesRequestRequestTypeDef]
    ) -> SearchMessageTemplatesResponseTypeDef:
        """
        Searches for Amazon Q in Connect message templates in the specified knowledge
        base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/search_message_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#search_message_templates)
        """

    def search_quick_responses(
        self, **kwargs: Unpack[SearchQuickResponsesRequestRequestTypeDef]
    ) -> SearchQuickResponsesResponseTypeDef:
        """
        Searches existing Amazon Q in Connect quick responses in an Amazon Q in Connect
        knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/search_quick_responses.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#search_quick_responses)
        """

    def search_sessions(
        self, **kwargs: Unpack[SearchSessionsRequestRequestTypeDef]
    ) -> SearchSessionsResponseTypeDef:
        """
        Searches for sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/search_sessions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#search_sessions)
        """

    def send_message(
        self, **kwargs: Unpack[SendMessageRequestRequestTypeDef]
    ) -> SendMessageResponseTypeDef:
        """
        Submits a message to the Amazon Q in Connect session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/send_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#send_message)
        """

    def start_content_upload(
        self, **kwargs: Unpack[StartContentUploadRequestRequestTypeDef]
    ) -> StartContentUploadResponseTypeDef:
        """
        Get a URL to upload content to a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/start_content_upload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#start_content_upload)
        """

    def start_import_job(
        self, **kwargs: Unpack[StartImportJobRequestRequestTypeDef]
    ) -> StartImportJobResponseTypeDef:
        """
        Start an asynchronous job to import Amazon Q in Connect resources from an
        uploaded source file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/start_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#start_import_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#untag_resource)
        """

    def update_ai_agent(
        self, **kwargs: Unpack[UpdateAIAgentRequestRequestTypeDef]
    ) -> UpdateAIAgentResponseTypeDef:
        """
        Updates an AI Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/update_ai_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#update_ai_agent)
        """

    def update_ai_guardrail(
        self, **kwargs: Unpack[UpdateAIGuardrailRequestRequestTypeDef]
    ) -> UpdateAIGuardrailResponseTypeDef:
        """
        Updates an AI Guardrail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/update_ai_guardrail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#update_ai_guardrail)
        """

    def update_ai_prompt(
        self, **kwargs: Unpack[UpdateAIPromptRequestRequestTypeDef]
    ) -> UpdateAIPromptResponseTypeDef:
        """
        Updates an AI Prompt.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/update_ai_prompt.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#update_ai_prompt)
        """

    def update_assistant_ai_agent(
        self, **kwargs: Unpack[UpdateAssistantAIAgentRequestRequestTypeDef]
    ) -> UpdateAssistantAIAgentResponseTypeDef:
        """
        Updates the AI Agent that is set for use by defafult on an Amazon Q in Connect
        Assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/update_assistant_ai_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#update_assistant_ai_agent)
        """

    def update_content(
        self, **kwargs: Unpack[UpdateContentRequestRequestTypeDef]
    ) -> UpdateContentResponseTypeDef:
        """
        Updates information about the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/update_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#update_content)
        """

    def update_knowledge_base_template_uri(
        self, **kwargs: Unpack[UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef]
    ) -> UpdateKnowledgeBaseTemplateUriResponseTypeDef:
        """
        Updates the template URI of a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/update_knowledge_base_template_uri.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#update_knowledge_base_template_uri)
        """

    def update_message_template(
        self, **kwargs: Unpack[UpdateMessageTemplateRequestRequestTypeDef]
    ) -> UpdateMessageTemplateResponseTypeDef:
        """
        Updates the Amazon Q in Connect message template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/update_message_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#update_message_template)
        """

    def update_message_template_metadata(
        self, **kwargs: Unpack[UpdateMessageTemplateMetadataRequestRequestTypeDef]
    ) -> UpdateMessageTemplateMetadataResponseTypeDef:
        """
        Updates the Amazon Q in Connect message template metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/update_message_template_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#update_message_template_metadata)
        """

    def update_quick_response(
        self, **kwargs: Unpack[UpdateQuickResponseRequestRequestTypeDef]
    ) -> UpdateQuickResponseResponseTypeDef:
        """
        Updates an existing Amazon Q in Connect quick response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/update_quick_response.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#update_quick_response)
        """

    def update_session(
        self, **kwargs: Unpack[UpdateSessionRequestRequestTypeDef]
    ) -> UpdateSessionResponseTypeDef:
        """
        Updates a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/update_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#update_session)
        """

    def update_session_data(
        self, **kwargs: Unpack[UpdateSessionDataRequestRequestTypeDef]
    ) -> UpdateSessionDataResponseTypeDef:
        """
        Updates the data stored on an Amazon Q in Connect Session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/update_session_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#update_session_data)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ai_agent_versions"]
    ) -> ListAIAgentVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_ai_agents"]) -> ListAIAgentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ai_guardrail_versions"]
    ) -> ListAIGuardrailVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ai_guardrails"]
    ) -> ListAIGuardrailsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ai_prompt_versions"]
    ) -> ListAIPromptVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_ai_prompts"]) -> ListAIPromptsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_assistant_associations"]
    ) -> ListAssistantAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_assistants"]) -> ListAssistantsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_content_associations"]
    ) -> ListContentAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_contents"]) -> ListContentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_import_jobs"]) -> ListImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_knowledge_bases"]
    ) -> ListKnowledgeBasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_message_template_versions"]
    ) -> ListMessageTemplateVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_message_templates"]
    ) -> ListMessageTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_messages"]) -> ListMessagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_quick_responses"]
    ) -> ListQuickResponsesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["query_assistant"]) -> QueryAssistantPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_content"]) -> SearchContentPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_message_templates"]
    ) -> SearchMessageTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_quick_responses"]
    ) -> SearchQuickResponsesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_sessions"]) -> SearchSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/client/#get_paginator)
        """
