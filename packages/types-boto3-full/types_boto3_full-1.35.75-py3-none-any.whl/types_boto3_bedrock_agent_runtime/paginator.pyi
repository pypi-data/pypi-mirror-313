"""
Type annotations for bedrock-agent-runtime service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient
    from types_boto3_bedrock_agent_runtime.paginator import (
        GetAgentMemoryPaginator,
        RerankPaginator,
        RetrievePaginator,
    )

    session = Session()
    client: AgentsforBedrockRuntimeClient = session.client("bedrock-agent-runtime")

    get_agent_memory_paginator: GetAgentMemoryPaginator = client.get_paginator("get_agent_memory")
    rerank_paginator: RerankPaginator = client.get_paginator("rerank")
    retrieve_paginator: RetrievePaginator = client.get_paginator("retrieve")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetAgentMemoryRequestGetAgentMemoryPaginateTypeDef,
    GetAgentMemoryResponseTypeDef,
    RerankRequestRerankPaginateTypeDef,
    RerankResponseTypeDef,
    RetrieveRequestRetrievePaginateTypeDef,
    RetrieveResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("GetAgentMemoryPaginator", "RerankPaginator", "RetrievePaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetAgentMemoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/GetAgentMemory.html#AgentsforBedrockRuntime.Paginator.GetAgentMemory)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/paginators/#getagentmemorypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetAgentMemoryRequestGetAgentMemoryPaginateTypeDef]
    ) -> _PageIterator[GetAgentMemoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/GetAgentMemory.html#AgentsforBedrockRuntime.Paginator.GetAgentMemory.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/paginators/#getagentmemorypaginator)
        """

class RerankPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Rerank.html#AgentsforBedrockRuntime.Paginator.Rerank)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/paginators/#rerankpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[RerankRequestRerankPaginateTypeDef]
    ) -> _PageIterator[RerankResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Rerank.html#AgentsforBedrockRuntime.Paginator.Rerank.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/paginators/#rerankpaginator)
        """

class RetrievePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Retrieve.html#AgentsforBedrockRuntime.Paginator.Retrieve)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/paginators/#retrievepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[RetrieveRequestRetrievePaginateTypeDef]
    ) -> _PageIterator[RetrieveResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Retrieve.html#AgentsforBedrockRuntime.Paginator.Retrieve.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/paginators/#retrievepaginator)
        """
