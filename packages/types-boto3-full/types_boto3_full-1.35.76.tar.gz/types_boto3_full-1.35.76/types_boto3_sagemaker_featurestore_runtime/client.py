"""
Type annotations for sagemaker-featurestore-runtime service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_featurestore_runtime/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sagemaker_featurestore_runtime.client import SageMakerFeatureStoreRuntimeClient

    session = Session()
    client: SageMakerFeatureStoreRuntimeClient = session.client("sagemaker-featurestore-runtime")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    BatchGetRecordRequestRequestTypeDef,
    BatchGetRecordResponseTypeDef,
    DeleteRecordRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetRecordRequestRequestTypeDef,
    GetRecordResponseTypeDef,
    PutRecordRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SageMakerFeatureStoreRuntimeClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessForbidden: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalFailure: Type[BotocoreClientError]
    ResourceNotFound: Type[BotocoreClientError]
    ServiceUnavailable: Type[BotocoreClientError]
    ValidationError: Type[BotocoreClientError]


class SageMakerFeatureStoreRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime.html#SageMakerFeatureStoreRuntime.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_featurestore_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SageMakerFeatureStoreRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime.html#SageMakerFeatureStoreRuntime.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_featurestore_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_featurestore_runtime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_featurestore_runtime/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_featurestore_runtime/client/#close)
        """

    def batch_get_record(
        self, **kwargs: Unpack[BatchGetRecordRequestRequestTypeDef]
    ) -> BatchGetRecordResponseTypeDef:
        """
        Retrieves a batch of <code>Records</code> from a <code>FeatureGroup</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime/client/batch_get_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_featurestore_runtime/client/#batch_get_record)
        """

    def delete_record(
        self, **kwargs: Unpack[DeleteRecordRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a <code>Record</code> from a <code>FeatureGroup</code> in the
        <code>OnlineStore</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime/client/delete_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_featurestore_runtime/client/#delete_record)
        """

    def get_record(
        self, **kwargs: Unpack[GetRecordRequestRequestTypeDef]
    ) -> GetRecordResponseTypeDef:
        """
        Use for <code>OnlineStore</code> serving from a <code>FeatureStore</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime/client/get_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_featurestore_runtime/client/#get_record)
        """

    def put_record(
        self, **kwargs: Unpack[PutRecordRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The <code>PutRecord</code> API is used to ingest a list of <code>Records</code>
        into your feature group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime/client/put_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_featurestore_runtime/client/#put_record)
        """
