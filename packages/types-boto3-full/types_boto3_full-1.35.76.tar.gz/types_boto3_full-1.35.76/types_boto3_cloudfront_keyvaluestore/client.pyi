"""
Type annotations for cloudfront-keyvaluestore service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudfront_keyvaluestore/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_cloudfront_keyvaluestore.client import CloudFrontKeyValueStoreClient

    session = Session()
    client: CloudFrontKeyValueStoreClient = session.client("cloudfront-keyvaluestore")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListKeysPaginator
from .type_defs import (
    DeleteKeyRequestRequestTypeDef,
    DeleteKeyResponseTypeDef,
    DescribeKeyValueStoreRequestRequestTypeDef,
    DescribeKeyValueStoreResponseTypeDef,
    GetKeyRequestRequestTypeDef,
    GetKeyResponseTypeDef,
    ListKeysRequestRequestTypeDef,
    ListKeysResponseTypeDef,
    PutKeyRequestRequestTypeDef,
    PutKeyResponseTypeDef,
    UpdateKeysRequestRequestTypeDef,
    UpdateKeysResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("CloudFrontKeyValueStoreClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CloudFrontKeyValueStoreClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore.html#CloudFrontKeyValueStore.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudfront_keyvaluestore/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudFrontKeyValueStoreClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore.html#CloudFrontKeyValueStore.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudfront_keyvaluestore/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudfront_keyvaluestore/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudfront_keyvaluestore/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudfront_keyvaluestore/client/#close)
        """

    def delete_key(
        self, **kwargs: Unpack[DeleteKeyRequestRequestTypeDef]
    ) -> DeleteKeyResponseTypeDef:
        """
        Deletes the key value pair specified by the key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/delete_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudfront_keyvaluestore/client/#delete_key)
        """

    def describe_key_value_store(
        self, **kwargs: Unpack[DescribeKeyValueStoreRequestRequestTypeDef]
    ) -> DescribeKeyValueStoreResponseTypeDef:
        """
        Returns metadata information about Key Value Store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/describe_key_value_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudfront_keyvaluestore/client/#describe_key_value_store)
        """

    def get_key(self, **kwargs: Unpack[GetKeyRequestRequestTypeDef]) -> GetKeyResponseTypeDef:
        """
        Returns a key value pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/get_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudfront_keyvaluestore/client/#get_key)
        """

    def list_keys(self, **kwargs: Unpack[ListKeysRequestRequestTypeDef]) -> ListKeysResponseTypeDef:
        """
        Returns a list of key value pairs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/list_keys.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudfront_keyvaluestore/client/#list_keys)
        """

    def put_key(self, **kwargs: Unpack[PutKeyRequestRequestTypeDef]) -> PutKeyResponseTypeDef:
        """
        Creates a new key value pair or replaces the value of an existing key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/put_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudfront_keyvaluestore/client/#put_key)
        """

    def update_keys(
        self, **kwargs: Unpack[UpdateKeysRequestRequestTypeDef]
    ) -> UpdateKeysResponseTypeDef:
        """
        Puts or Deletes multiple key value pairs in a single, all-or-nothing operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/update_keys.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudfront_keyvaluestore/client/#update_keys)
        """

    def get_paginator(self, operation_name: Literal["list_keys"]) -> ListKeysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudfront_keyvaluestore/client/#get_paginator)
        """
