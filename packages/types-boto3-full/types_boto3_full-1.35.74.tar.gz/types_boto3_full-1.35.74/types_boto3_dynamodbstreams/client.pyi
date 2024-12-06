"""
Type annotations for dynamodbstreams service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dynamodbstreams/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_dynamodbstreams.client import DynamoDBStreamsClient

    session = Session()
    client: DynamoDBStreamsClient = session.client("dynamodbstreams")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    DescribeStreamInputRequestTypeDef,
    DescribeStreamOutputTypeDef,
    GetRecordsInputRequestTypeDef,
    GetRecordsOutputTypeDef,
    GetShardIteratorInputRequestTypeDef,
    GetShardIteratorOutputTypeDef,
    ListStreamsInputRequestTypeDef,
    ListStreamsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DynamoDBStreamsClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ExpiredIteratorException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TrimmedDataAccessException: Type[BotocoreClientError]

class DynamoDBStreamsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodbstreams.html#DynamoDBStreams.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dynamodbstreams/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DynamoDBStreamsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodbstreams.html#DynamoDBStreams.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dynamodbstreams/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodbstreams/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dynamodbstreams/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodbstreams/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dynamodbstreams/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodbstreams/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dynamodbstreams/client/#close)
        """

    def describe_stream(
        self, **kwargs: Unpack[DescribeStreamInputRequestTypeDef]
    ) -> DescribeStreamOutputTypeDef:
        """
        Returns information about a stream, including the current status of the stream,
        its Amazon Resource Name (ARN), the composition of its shards, and its
        corresponding DynamoDB table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodbstreams/client/describe_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dynamodbstreams/client/#describe_stream)
        """

    def get_records(
        self, **kwargs: Unpack[GetRecordsInputRequestTypeDef]
    ) -> GetRecordsOutputTypeDef:
        """
        Retrieves the stream records from a given shard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodbstreams/client/get_records.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dynamodbstreams/client/#get_records)
        """

    def get_shard_iterator(
        self, **kwargs: Unpack[GetShardIteratorInputRequestTypeDef]
    ) -> GetShardIteratorOutputTypeDef:
        """
        Returns a shard iterator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodbstreams/client/get_shard_iterator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dynamodbstreams/client/#get_shard_iterator)
        """

    def list_streams(
        self, **kwargs: Unpack[ListStreamsInputRequestTypeDef]
    ) -> ListStreamsOutputTypeDef:
        """
        Returns an array of stream ARNs associated with the current account and
        endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodbstreams/client/list_streams.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dynamodbstreams/client/#list_streams)
        """
