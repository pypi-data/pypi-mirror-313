"""
Type annotations for sagemaker-a2i-runtime service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_a2i_runtime/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sagemaker_a2i_runtime.client import AugmentedAIRuntimeClient

    session = Session()
    client: AugmentedAIRuntimeClient = session.client("sagemaker-a2i-runtime")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListHumanLoopsPaginator
from .type_defs import (
    DeleteHumanLoopRequestRequestTypeDef,
    DescribeHumanLoopRequestRequestTypeDef,
    DescribeHumanLoopResponseTypeDef,
    ListHumanLoopsRequestRequestTypeDef,
    ListHumanLoopsResponseTypeDef,
    StartHumanLoopRequestRequestTypeDef,
    StartHumanLoopResponseTypeDef,
    StopHumanLoopRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("AugmentedAIRuntimeClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class AugmentedAIRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_a2i_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AugmentedAIRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_a2i_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_a2i_runtime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_a2i_runtime/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_a2i_runtime/client/#close)
        """

    def delete_human_loop(
        self, **kwargs: Unpack[DeleteHumanLoopRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified human loop for a flow definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime/client/delete_human_loop.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_a2i_runtime/client/#delete_human_loop)
        """

    def describe_human_loop(
        self, **kwargs: Unpack[DescribeHumanLoopRequestRequestTypeDef]
    ) -> DescribeHumanLoopResponseTypeDef:
        """
        Returns information about the specified human loop.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime/client/describe_human_loop.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_a2i_runtime/client/#describe_human_loop)
        """

    def list_human_loops(
        self, **kwargs: Unpack[ListHumanLoopsRequestRequestTypeDef]
    ) -> ListHumanLoopsResponseTypeDef:
        """
        Returns information about human loops, given the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime/client/list_human_loops.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_a2i_runtime/client/#list_human_loops)
        """

    def start_human_loop(
        self, **kwargs: Unpack[StartHumanLoopRequestRequestTypeDef]
    ) -> StartHumanLoopResponseTypeDef:
        """
        Starts a human loop, provided that at least one activation condition is met.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime/client/start_human_loop.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_a2i_runtime/client/#start_human_loop)
        """

    def stop_human_loop(
        self, **kwargs: Unpack[StopHumanLoopRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops the specified human loop.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime/client/stop_human_loop.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_a2i_runtime/client/#stop_human_loop)
        """

    def get_paginator(self, operation_name: Literal["list_human_loops"]) -> ListHumanLoopsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_a2i_runtime/client/#get_paginator)
        """
