"""
Type annotations for sagemaker-runtime service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_runtime/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sagemaker_runtime.client import SageMakerRuntimeClient

    session = Session()
    client: SageMakerRuntimeClient = session.client("sagemaker-runtime")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    InvokeEndpointAsyncInputRequestTypeDef,
    InvokeEndpointAsyncOutputTypeDef,
    InvokeEndpointInputRequestTypeDef,
    InvokeEndpointOutputTypeDef,
    InvokeEndpointWithResponseStreamInputRequestTypeDef,
    InvokeEndpointWithResponseStreamOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SageMakerRuntimeClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalDependencyException: Type[BotocoreClientError]
    InternalFailure: Type[BotocoreClientError]
    InternalStreamFailure: Type[BotocoreClientError]
    ModelError: Type[BotocoreClientError]
    ModelNotReadyException: Type[BotocoreClientError]
    ModelStreamError: Type[BotocoreClientError]
    ServiceUnavailable: Type[BotocoreClientError]
    ValidationError: Type[BotocoreClientError]


class SageMakerRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SageMakerRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_runtime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_runtime/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_runtime/client/#close)
        """

    def invoke_endpoint(
        self, **kwargs: Unpack[InvokeEndpointInputRequestTypeDef]
    ) -> InvokeEndpointOutputTypeDef:
        """
        After you deploy a model into production using Amazon SageMaker hosting
        services, your client applications use this API to get inferences from the
        model hosted at the specified endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime/client/invoke_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_runtime/client/#invoke_endpoint)
        """

    def invoke_endpoint_async(
        self, **kwargs: Unpack[InvokeEndpointAsyncInputRequestTypeDef]
    ) -> InvokeEndpointAsyncOutputTypeDef:
        """
        After you deploy a model into production using Amazon SageMaker hosting
        services, your client applications use this API to get inferences from the
        model hosted at the specified endpoint in an asynchronous manner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime/client/invoke_endpoint_async.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_runtime/client/#invoke_endpoint_async)
        """

    def invoke_endpoint_with_response_stream(
        self, **kwargs: Unpack[InvokeEndpointWithResponseStreamInputRequestTypeDef]
    ) -> InvokeEndpointWithResponseStreamOutputTypeDef:
        """
        Invokes a model at the specified endpoint to return the inference response as a
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime/client/invoke_endpoint_with_response_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_runtime/client/#invoke_endpoint_with_response_stream)
        """
