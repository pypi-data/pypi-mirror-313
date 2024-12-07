"""
Type annotations for bedrock-agent service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_bedrock_agent.client import AgentsforBedrockClient
    from types_boto3_bedrock_agent.paginator import (
        ListAgentActionGroupsPaginator,
        ListAgentAliasesPaginator,
        ListAgentCollaboratorsPaginator,
        ListAgentKnowledgeBasesPaginator,
        ListAgentVersionsPaginator,
        ListAgentsPaginator,
        ListDataSourcesPaginator,
        ListFlowAliasesPaginator,
        ListFlowVersionsPaginator,
        ListFlowsPaginator,
        ListIngestionJobsPaginator,
        ListKnowledgeBaseDocumentsPaginator,
        ListKnowledgeBasesPaginator,
        ListPromptsPaginator,
    )

    session = Session()
    client: AgentsforBedrockClient = session.client("bedrock-agent")

    list_agent_action_groups_paginator: ListAgentActionGroupsPaginator = client.get_paginator("list_agent_action_groups")
    list_agent_aliases_paginator: ListAgentAliasesPaginator = client.get_paginator("list_agent_aliases")
    list_agent_collaborators_paginator: ListAgentCollaboratorsPaginator = client.get_paginator("list_agent_collaborators")
    list_agent_knowledge_bases_paginator: ListAgentKnowledgeBasesPaginator = client.get_paginator("list_agent_knowledge_bases")
    list_agent_versions_paginator: ListAgentVersionsPaginator = client.get_paginator("list_agent_versions")
    list_agents_paginator: ListAgentsPaginator = client.get_paginator("list_agents")
    list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
    list_flow_aliases_paginator: ListFlowAliasesPaginator = client.get_paginator("list_flow_aliases")
    list_flow_versions_paginator: ListFlowVersionsPaginator = client.get_paginator("list_flow_versions")
    list_flows_paginator: ListFlowsPaginator = client.get_paginator("list_flows")
    list_ingestion_jobs_paginator: ListIngestionJobsPaginator = client.get_paginator("list_ingestion_jobs")
    list_knowledge_base_documents_paginator: ListKnowledgeBaseDocumentsPaginator = client.get_paginator("list_knowledge_base_documents")
    list_knowledge_bases_paginator: ListKnowledgeBasesPaginator = client.get_paginator("list_knowledge_bases")
    list_prompts_paginator: ListPromptsPaginator = client.get_paginator("list_prompts")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAgentActionGroupsRequestListAgentActionGroupsPaginateTypeDef,
    ListAgentActionGroupsResponseTypeDef,
    ListAgentAliasesRequestListAgentAliasesPaginateTypeDef,
    ListAgentAliasesResponseTypeDef,
    ListAgentCollaboratorsRequestListAgentCollaboratorsPaginateTypeDef,
    ListAgentCollaboratorsResponseTypeDef,
    ListAgentKnowledgeBasesRequestListAgentKnowledgeBasesPaginateTypeDef,
    ListAgentKnowledgeBasesResponseTypeDef,
    ListAgentsRequestListAgentsPaginateTypeDef,
    ListAgentsResponseTypeDef,
    ListAgentVersionsRequestListAgentVersionsPaginateTypeDef,
    ListAgentVersionsResponseTypeDef,
    ListDataSourcesRequestListDataSourcesPaginateTypeDef,
    ListDataSourcesResponseTypeDef,
    ListFlowAliasesRequestListFlowAliasesPaginateTypeDef,
    ListFlowAliasesResponseTypeDef,
    ListFlowsRequestListFlowsPaginateTypeDef,
    ListFlowsResponseTypeDef,
    ListFlowVersionsRequestListFlowVersionsPaginateTypeDef,
    ListFlowVersionsResponseTypeDef,
    ListIngestionJobsRequestListIngestionJobsPaginateTypeDef,
    ListIngestionJobsResponseTypeDef,
    ListKnowledgeBaseDocumentsRequestListKnowledgeBaseDocumentsPaginateTypeDef,
    ListKnowledgeBaseDocumentsResponseTypeDef,
    ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef,
    ListKnowledgeBasesResponseTypeDef,
    ListPromptsRequestListPromptsPaginateTypeDef,
    ListPromptsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAgentActionGroupsPaginator",
    "ListAgentAliasesPaginator",
    "ListAgentCollaboratorsPaginator",
    "ListAgentKnowledgeBasesPaginator",
    "ListAgentVersionsPaginator",
    "ListAgentsPaginator",
    "ListDataSourcesPaginator",
    "ListFlowAliasesPaginator",
    "ListFlowVersionsPaginator",
    "ListFlowsPaginator",
    "ListIngestionJobsPaginator",
    "ListKnowledgeBaseDocumentsPaginator",
    "ListKnowledgeBasesPaginator",
    "ListPromptsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAgentActionGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentActionGroups.html#AgentsforBedrock.Paginator.ListAgentActionGroups)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listagentactiongroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAgentActionGroupsRequestListAgentActionGroupsPaginateTypeDef]
    ) -> _PageIterator[ListAgentActionGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentActionGroups.html#AgentsforBedrock.Paginator.ListAgentActionGroups.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listagentactiongroupspaginator)
        """


class ListAgentAliasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentAliases.html#AgentsforBedrock.Paginator.ListAgentAliases)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listagentaliasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAgentAliasesRequestListAgentAliasesPaginateTypeDef]
    ) -> _PageIterator[ListAgentAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentAliases.html#AgentsforBedrock.Paginator.ListAgentAliases.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listagentaliasespaginator)
        """


class ListAgentCollaboratorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentCollaborators.html#AgentsforBedrock.Paginator.ListAgentCollaborators)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listagentcollaboratorspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAgentCollaboratorsRequestListAgentCollaboratorsPaginateTypeDef]
    ) -> _PageIterator[ListAgentCollaboratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentCollaborators.html#AgentsforBedrock.Paginator.ListAgentCollaborators.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listagentcollaboratorspaginator)
        """


class ListAgentKnowledgeBasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentKnowledgeBases.html#AgentsforBedrock.Paginator.ListAgentKnowledgeBases)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listagentknowledgebasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAgentKnowledgeBasesRequestListAgentKnowledgeBasesPaginateTypeDef]
    ) -> _PageIterator[ListAgentKnowledgeBasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentKnowledgeBases.html#AgentsforBedrock.Paginator.ListAgentKnowledgeBases.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listagentknowledgebasespaginator)
        """


class ListAgentVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentVersions.html#AgentsforBedrock.Paginator.ListAgentVersions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listagentversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAgentVersionsRequestListAgentVersionsPaginateTypeDef]
    ) -> _PageIterator[ListAgentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgentVersions.html#AgentsforBedrock.Paginator.ListAgentVersions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listagentversionspaginator)
        """


class ListAgentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgents.html#AgentsforBedrock.Paginator.ListAgents)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listagentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAgentsRequestListAgentsPaginateTypeDef]
    ) -> _PageIterator[ListAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListAgents.html#AgentsforBedrock.Paginator.ListAgents.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listagentspaginator)
        """


class ListDataSourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListDataSources.html#AgentsforBedrock.Paginator.ListDataSources)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listdatasourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataSourcesRequestListDataSourcesPaginateTypeDef]
    ) -> _PageIterator[ListDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListDataSources.html#AgentsforBedrock.Paginator.ListDataSources.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listdatasourcespaginator)
        """


class ListFlowAliasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListFlowAliases.html#AgentsforBedrock.Paginator.ListFlowAliases)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listflowaliasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFlowAliasesRequestListFlowAliasesPaginateTypeDef]
    ) -> _PageIterator[ListFlowAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListFlowAliases.html#AgentsforBedrock.Paginator.ListFlowAliases.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listflowaliasespaginator)
        """


class ListFlowVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListFlowVersions.html#AgentsforBedrock.Paginator.ListFlowVersions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listflowversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFlowVersionsRequestListFlowVersionsPaginateTypeDef]
    ) -> _PageIterator[ListFlowVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListFlowVersions.html#AgentsforBedrock.Paginator.ListFlowVersions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listflowversionspaginator)
        """


class ListFlowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListFlows.html#AgentsforBedrock.Paginator.ListFlows)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listflowspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFlowsRequestListFlowsPaginateTypeDef]
    ) -> _PageIterator[ListFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListFlows.html#AgentsforBedrock.Paginator.ListFlows.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listflowspaginator)
        """


class ListIngestionJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListIngestionJobs.html#AgentsforBedrock.Paginator.ListIngestionJobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listingestionjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIngestionJobsRequestListIngestionJobsPaginateTypeDef]
    ) -> _PageIterator[ListIngestionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListIngestionJobs.html#AgentsforBedrock.Paginator.ListIngestionJobs.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listingestionjobspaginator)
        """


class ListKnowledgeBaseDocumentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListKnowledgeBaseDocuments.html#AgentsforBedrock.Paginator.ListKnowledgeBaseDocuments)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listknowledgebasedocumentspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListKnowledgeBaseDocumentsRequestListKnowledgeBaseDocumentsPaginateTypeDef
        ],
    ) -> _PageIterator[ListKnowledgeBaseDocumentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListKnowledgeBaseDocuments.html#AgentsforBedrock.Paginator.ListKnowledgeBaseDocuments.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listknowledgebasedocumentspaginator)
        """


class ListKnowledgeBasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListKnowledgeBases.html#AgentsforBedrock.Paginator.ListKnowledgeBases)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listknowledgebasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef]
    ) -> _PageIterator[ListKnowledgeBasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListKnowledgeBases.html#AgentsforBedrock.Paginator.ListKnowledgeBases.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listknowledgebasespaginator)
        """


class ListPromptsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListPrompts.html#AgentsforBedrock.Paginator.ListPrompts)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listpromptspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPromptsRequestListPromptsPaginateTypeDef]
    ) -> _PageIterator[ListPromptsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent/paginator/ListPrompts.html#AgentsforBedrock.Paginator.ListPrompts.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent/paginators/#listpromptspaginator)
        """
