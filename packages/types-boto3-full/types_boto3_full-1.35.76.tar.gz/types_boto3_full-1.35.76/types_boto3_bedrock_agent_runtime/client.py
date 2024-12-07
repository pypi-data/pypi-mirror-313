"""
Type annotations for bedrock-agent-runtime service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient

    session = Session()
    client: AgentsforBedrockRuntimeClient = session.client("bedrock-agent-runtime")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import GetAgentMemoryPaginator, RerankPaginator, RetrievePaginator
from .type_defs import (
    DeleteAgentMemoryRequestRequestTypeDef,
    GenerateQueryRequestRequestTypeDef,
    GenerateQueryResponseTypeDef,
    GetAgentMemoryRequestRequestTypeDef,
    GetAgentMemoryResponseTypeDef,
    InvokeAgentRequestRequestTypeDef,
    InvokeAgentResponseTypeDef,
    InvokeFlowRequestRequestTypeDef,
    InvokeFlowResponseTypeDef,
    InvokeInlineAgentRequestRequestTypeDef,
    InvokeInlineAgentResponseTypeDef,
    OptimizePromptRequestRequestTypeDef,
    OptimizePromptResponseTypeDef,
    RerankRequestRequestTypeDef,
    RerankResponseTypeDef,
    RetrieveAndGenerateRequestRequestTypeDef,
    RetrieveAndGenerateResponseTypeDef,
    RetrieveAndGenerateStreamRequestRequestTypeDef,
    RetrieveAndGenerateStreamResponseTypeDef,
    RetrieveRequestRequestTypeDef,
    RetrieveResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("AgentsforBedrockRuntimeClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadGatewayException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DependencyFailedException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class AgentsforBedrockRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AgentsforBedrockRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#close)
        """

    def delete_agent_memory(
        self, **kwargs: Unpack[DeleteAgentMemoryRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes memory from the specified memory identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/delete_agent_memory.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#delete_agent_memory)
        """

    def generate_query(
        self, **kwargs: Unpack[GenerateQueryRequestRequestTypeDef]
    ) -> GenerateQueryResponseTypeDef:
        """
        Generates an SQL query from a natural language query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/generate_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#generate_query)
        """

    def get_agent_memory(
        self, **kwargs: Unpack[GetAgentMemoryRequestRequestTypeDef]
    ) -> GetAgentMemoryResponseTypeDef:
        """
        Gets the sessions stored in the memory of the agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/get_agent_memory.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#get_agent_memory)
        """

    def invoke_agent(
        self, **kwargs: Unpack[InvokeAgentRequestRequestTypeDef]
    ) -> InvokeAgentResponseTypeDef:
        """
        The CLI doesn't support streaming operations in Amazon Bedrock, including
        <code>InvokeAgent</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/invoke_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#invoke_agent)
        """

    def invoke_flow(
        self, **kwargs: Unpack[InvokeFlowRequestRequestTypeDef]
    ) -> InvokeFlowResponseTypeDef:
        """
        Invokes an alias of a flow to run the inputs that you specify and return the
        output of each node as a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/invoke_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#invoke_flow)
        """

    def invoke_inline_agent(
        self, **kwargs: Unpack[InvokeInlineAgentRequestRequestTypeDef]
    ) -> InvokeInlineAgentResponseTypeDef:
        """
        Invokes an inline Amazon Bedrock agent using the configurations you provide
        with the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/invoke_inline_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#invoke_inline_agent)
        """

    def optimize_prompt(
        self, **kwargs: Unpack[OptimizePromptRequestRequestTypeDef]
    ) -> OptimizePromptResponseTypeDef:
        """
        Optimizes a prompt for the task that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/optimize_prompt.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#optimize_prompt)
        """

    def rerank(self, **kwargs: Unpack[RerankRequestRequestTypeDef]) -> RerankResponseTypeDef:
        """
        Reranks the relevance of sources based on queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/rerank.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#rerank)
        """

    def retrieve(self, **kwargs: Unpack[RetrieveRequestRequestTypeDef]) -> RetrieveResponseTypeDef:
        """
        Queries a knowledge base and retrieves information from it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/retrieve.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#retrieve)
        """

    def retrieve_and_generate(
        self, **kwargs: Unpack[RetrieveAndGenerateRequestRequestTypeDef]
    ) -> RetrieveAndGenerateResponseTypeDef:
        """
        Queries a knowledge base and generates responses based on the retrieved results
        and using the specified foundation model or <a
        href="https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html">inference
        profile</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/retrieve_and_generate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#retrieve_and_generate)
        """

    def retrieve_and_generate_stream(
        self, **kwargs: Unpack[RetrieveAndGenerateStreamRequestRequestTypeDef]
    ) -> RetrieveAndGenerateStreamResponseTypeDef:
        """
        Queries a knowledge base and generates responses based on the retrieved
        results, with output in streaming format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/retrieve_and_generate_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#retrieve_and_generate_stream)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_agent_memory"]) -> GetAgentMemoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["rerank"]) -> RerankPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["retrieve"]) -> RetrievePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#get_paginator)
        """
