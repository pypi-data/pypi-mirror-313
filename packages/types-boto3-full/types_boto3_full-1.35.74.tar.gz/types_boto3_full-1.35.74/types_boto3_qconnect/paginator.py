"""
Type annotations for qconnect service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_qconnect.client import QConnectClient
    from types_boto3_qconnect.paginator import (
        ListAIAgentVersionsPaginator,
        ListAIAgentsPaginator,
        ListAIGuardrailVersionsPaginator,
        ListAIGuardrailsPaginator,
        ListAIPromptVersionsPaginator,
        ListAIPromptsPaginator,
        ListAssistantAssociationsPaginator,
        ListAssistantsPaginator,
        ListContentAssociationsPaginator,
        ListContentsPaginator,
        ListImportJobsPaginator,
        ListKnowledgeBasesPaginator,
        ListMessageTemplateVersionsPaginator,
        ListMessageTemplatesPaginator,
        ListMessagesPaginator,
        ListQuickResponsesPaginator,
        QueryAssistantPaginator,
        SearchContentPaginator,
        SearchMessageTemplatesPaginator,
        SearchQuickResponsesPaginator,
        SearchSessionsPaginator,
    )

    session = Session()
    client: QConnectClient = session.client("qconnect")

    list_ai_agent_versions_paginator: ListAIAgentVersionsPaginator = client.get_paginator("list_ai_agent_versions")
    list_ai_agents_paginator: ListAIAgentsPaginator = client.get_paginator("list_ai_agents")
    list_ai_guardrail_versions_paginator: ListAIGuardrailVersionsPaginator = client.get_paginator("list_ai_guardrail_versions")
    list_ai_guardrails_paginator: ListAIGuardrailsPaginator = client.get_paginator("list_ai_guardrails")
    list_ai_prompt_versions_paginator: ListAIPromptVersionsPaginator = client.get_paginator("list_ai_prompt_versions")
    list_ai_prompts_paginator: ListAIPromptsPaginator = client.get_paginator("list_ai_prompts")
    list_assistant_associations_paginator: ListAssistantAssociationsPaginator = client.get_paginator("list_assistant_associations")
    list_assistants_paginator: ListAssistantsPaginator = client.get_paginator("list_assistants")
    list_content_associations_paginator: ListContentAssociationsPaginator = client.get_paginator("list_content_associations")
    list_contents_paginator: ListContentsPaginator = client.get_paginator("list_contents")
    list_import_jobs_paginator: ListImportJobsPaginator = client.get_paginator("list_import_jobs")
    list_knowledge_bases_paginator: ListKnowledgeBasesPaginator = client.get_paginator("list_knowledge_bases")
    list_message_template_versions_paginator: ListMessageTemplateVersionsPaginator = client.get_paginator("list_message_template_versions")
    list_message_templates_paginator: ListMessageTemplatesPaginator = client.get_paginator("list_message_templates")
    list_messages_paginator: ListMessagesPaginator = client.get_paginator("list_messages")
    list_quick_responses_paginator: ListQuickResponsesPaginator = client.get_paginator("list_quick_responses")
    query_assistant_paginator: QueryAssistantPaginator = client.get_paginator("query_assistant")
    search_content_paginator: SearchContentPaginator = client.get_paginator("search_content")
    search_message_templates_paginator: SearchMessageTemplatesPaginator = client.get_paginator("search_message_templates")
    search_quick_responses_paginator: SearchQuickResponsesPaginator = client.get_paginator("search_quick_responses")
    search_sessions_paginator: SearchSessionsPaginator = client.get_paginator("search_sessions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAIAgentsRequestListAIAgentsPaginateTypeDef,
    ListAIAgentsResponseTypeDef,
    ListAIAgentVersionsRequestListAIAgentVersionsPaginateTypeDef,
    ListAIAgentVersionsResponseTypeDef,
    ListAIGuardrailsRequestListAIGuardrailsPaginateTypeDef,
    ListAIGuardrailsResponseTypeDef,
    ListAIGuardrailVersionsRequestListAIGuardrailVersionsPaginateTypeDef,
    ListAIGuardrailVersionsResponseTypeDef,
    ListAIPromptsRequestListAIPromptsPaginateTypeDef,
    ListAIPromptsResponseTypeDef,
    ListAIPromptVersionsRequestListAIPromptVersionsPaginateTypeDef,
    ListAIPromptVersionsResponseTypeDef,
    ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef,
    ListAssistantAssociationsResponseTypeDef,
    ListAssistantsRequestListAssistantsPaginateTypeDef,
    ListAssistantsResponseTypeDef,
    ListContentAssociationsRequestListContentAssociationsPaginateTypeDef,
    ListContentAssociationsResponseTypeDef,
    ListContentsRequestListContentsPaginateTypeDef,
    ListContentsResponseTypeDef,
    ListImportJobsRequestListImportJobsPaginateTypeDef,
    ListImportJobsResponseTypeDef,
    ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef,
    ListKnowledgeBasesResponseTypeDef,
    ListMessagesRequestListMessagesPaginateTypeDef,
    ListMessagesResponseTypeDef,
    ListMessageTemplatesRequestListMessageTemplatesPaginateTypeDef,
    ListMessageTemplatesResponseTypeDef,
    ListMessageTemplateVersionsRequestListMessageTemplateVersionsPaginateTypeDef,
    ListMessageTemplateVersionsResponseTypeDef,
    ListQuickResponsesRequestListQuickResponsesPaginateTypeDef,
    ListQuickResponsesResponseTypeDef,
    QueryAssistantRequestQueryAssistantPaginateTypeDef,
    QueryAssistantResponsePaginatorTypeDef,
    SearchContentRequestSearchContentPaginateTypeDef,
    SearchContentResponseTypeDef,
    SearchMessageTemplatesRequestSearchMessageTemplatesPaginateTypeDef,
    SearchMessageTemplatesResponseTypeDef,
    SearchQuickResponsesRequestSearchQuickResponsesPaginateTypeDef,
    SearchQuickResponsesResponseTypeDef,
    SearchSessionsRequestSearchSessionsPaginateTypeDef,
    SearchSessionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAIAgentVersionsPaginator",
    "ListAIAgentsPaginator",
    "ListAIGuardrailVersionsPaginator",
    "ListAIGuardrailsPaginator",
    "ListAIPromptVersionsPaginator",
    "ListAIPromptsPaginator",
    "ListAssistantAssociationsPaginator",
    "ListAssistantsPaginator",
    "ListContentAssociationsPaginator",
    "ListContentsPaginator",
    "ListImportJobsPaginator",
    "ListKnowledgeBasesPaginator",
    "ListMessageTemplateVersionsPaginator",
    "ListMessageTemplatesPaginator",
    "ListMessagesPaginator",
    "ListQuickResponsesPaginator",
    "QueryAssistantPaginator",
    "SearchContentPaginator",
    "SearchMessageTemplatesPaginator",
    "SearchQuickResponsesPaginator",
    "SearchSessionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAIAgentVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAIAgentVersions.html#QConnect.Paginator.ListAIAgentVersions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listaiagentversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAIAgentVersionsRequestListAIAgentVersionsPaginateTypeDef]
    ) -> _PageIterator[ListAIAgentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAIAgentVersions.html#QConnect.Paginator.ListAIAgentVersions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listaiagentversionspaginator)
        """


class ListAIAgentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAIAgents.html#QConnect.Paginator.ListAIAgents)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listaiagentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAIAgentsRequestListAIAgentsPaginateTypeDef]
    ) -> _PageIterator[ListAIAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAIAgents.html#QConnect.Paginator.ListAIAgents.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listaiagentspaginator)
        """


class ListAIGuardrailVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAIGuardrailVersions.html#QConnect.Paginator.ListAIGuardrailVersions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listaiguardrailversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAIGuardrailVersionsRequestListAIGuardrailVersionsPaginateTypeDef]
    ) -> _PageIterator[ListAIGuardrailVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAIGuardrailVersions.html#QConnect.Paginator.ListAIGuardrailVersions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listaiguardrailversionspaginator)
        """


class ListAIGuardrailsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAIGuardrails.html#QConnect.Paginator.ListAIGuardrails)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listaiguardrailspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAIGuardrailsRequestListAIGuardrailsPaginateTypeDef]
    ) -> _PageIterator[ListAIGuardrailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAIGuardrails.html#QConnect.Paginator.ListAIGuardrails.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listaiguardrailspaginator)
        """


class ListAIPromptVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAIPromptVersions.html#QConnect.Paginator.ListAIPromptVersions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listaipromptversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAIPromptVersionsRequestListAIPromptVersionsPaginateTypeDef]
    ) -> _PageIterator[ListAIPromptVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAIPromptVersions.html#QConnect.Paginator.ListAIPromptVersions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listaipromptversionspaginator)
        """


class ListAIPromptsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAIPrompts.html#QConnect.Paginator.ListAIPrompts)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listaipromptspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAIPromptsRequestListAIPromptsPaginateTypeDef]
    ) -> _PageIterator[ListAIPromptsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAIPrompts.html#QConnect.Paginator.ListAIPrompts.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listaipromptspaginator)
        """


class ListAssistantAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAssistantAssociations.html#QConnect.Paginator.ListAssistantAssociations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listassistantassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef],
    ) -> _PageIterator[ListAssistantAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAssistantAssociations.html#QConnect.Paginator.ListAssistantAssociations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listassistantassociationspaginator)
        """


class ListAssistantsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAssistants.html#QConnect.Paginator.ListAssistants)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listassistantspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssistantsRequestListAssistantsPaginateTypeDef]
    ) -> _PageIterator[ListAssistantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListAssistants.html#QConnect.Paginator.ListAssistants.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listassistantspaginator)
        """


class ListContentAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListContentAssociations.html#QConnect.Paginator.ListContentAssociations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listcontentassociationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContentAssociationsRequestListContentAssociationsPaginateTypeDef]
    ) -> _PageIterator[ListContentAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListContentAssociations.html#QConnect.Paginator.ListContentAssociations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listcontentassociationspaginator)
        """


class ListContentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListContents.html#QConnect.Paginator.ListContents)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listcontentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContentsRequestListContentsPaginateTypeDef]
    ) -> _PageIterator[ListContentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListContents.html#QConnect.Paginator.ListContents.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listcontentspaginator)
        """


class ListImportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListImportJobs.html#QConnect.Paginator.ListImportJobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listimportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListImportJobsRequestListImportJobsPaginateTypeDef]
    ) -> _PageIterator[ListImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListImportJobs.html#QConnect.Paginator.ListImportJobs.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listimportjobspaginator)
        """


class ListKnowledgeBasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListKnowledgeBases.html#QConnect.Paginator.ListKnowledgeBases)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listknowledgebasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef]
    ) -> _PageIterator[ListKnowledgeBasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListKnowledgeBases.html#QConnect.Paginator.ListKnowledgeBases.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listknowledgebasespaginator)
        """


class ListMessageTemplateVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListMessageTemplateVersions.html#QConnect.Paginator.ListMessageTemplateVersions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listmessagetemplateversionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListMessageTemplateVersionsRequestListMessageTemplateVersionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListMessageTemplateVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListMessageTemplateVersions.html#QConnect.Paginator.ListMessageTemplateVersions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listmessagetemplateversionspaginator)
        """


class ListMessageTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListMessageTemplates.html#QConnect.Paginator.ListMessageTemplates)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listmessagetemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMessageTemplatesRequestListMessageTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListMessageTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListMessageTemplates.html#QConnect.Paginator.ListMessageTemplates.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listmessagetemplatespaginator)
        """


class ListMessagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListMessages.html#QConnect.Paginator.ListMessages)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listmessagespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMessagesRequestListMessagesPaginateTypeDef]
    ) -> _PageIterator[ListMessagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListMessages.html#QConnect.Paginator.ListMessages.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listmessagespaginator)
        """


class ListQuickResponsesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListQuickResponses.html#QConnect.Paginator.ListQuickResponses)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listquickresponsespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListQuickResponsesRequestListQuickResponsesPaginateTypeDef]
    ) -> _PageIterator[ListQuickResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/ListQuickResponses.html#QConnect.Paginator.ListQuickResponses.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#listquickresponsespaginator)
        """


class QueryAssistantPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/QueryAssistant.html#QConnect.Paginator.QueryAssistant)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#queryassistantpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[QueryAssistantRequestQueryAssistantPaginateTypeDef]
    ) -> _PageIterator[QueryAssistantResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/QueryAssistant.html#QConnect.Paginator.QueryAssistant.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#queryassistantpaginator)
        """


class SearchContentPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/SearchContent.html#QConnect.Paginator.SearchContent)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#searchcontentpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchContentRequestSearchContentPaginateTypeDef]
    ) -> _PageIterator[SearchContentResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/SearchContent.html#QConnect.Paginator.SearchContent.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#searchcontentpaginator)
        """


class SearchMessageTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/SearchMessageTemplates.html#QConnect.Paginator.SearchMessageTemplates)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#searchmessagetemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchMessageTemplatesRequestSearchMessageTemplatesPaginateTypeDef]
    ) -> _PageIterator[SearchMessageTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/SearchMessageTemplates.html#QConnect.Paginator.SearchMessageTemplates.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#searchmessagetemplatespaginator)
        """


class SearchQuickResponsesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/SearchQuickResponses.html#QConnect.Paginator.SearchQuickResponses)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#searchquickresponsespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchQuickResponsesRequestSearchQuickResponsesPaginateTypeDef]
    ) -> _PageIterator[SearchQuickResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/SearchQuickResponses.html#QConnect.Paginator.SearchQuickResponses.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#searchquickresponsespaginator)
        """


class SearchSessionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/SearchSessions.html#QConnect.Paginator.SearchSessions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#searchsessionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchSessionsRequestSearchSessionsPaginateTypeDef]
    ) -> _PageIterator[SearchSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect/paginator/SearchSessions.html#QConnect.Paginator.SearchSessions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qconnect/paginators/#searchsessionspaginator)
        """
