"""
Type annotations for workmailmessageflow service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_workmailmessageflow/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_workmailmessageflow.client import WorkMailMessageFlowClient

    session = Session()
    client: WorkMailMessageFlowClient = session.client("workmailmessageflow")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    GetRawMessageContentRequestRequestTypeDef,
    GetRawMessageContentResponseTypeDef,
    PutRawMessageContentRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("WorkMailMessageFlowClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InvalidContentLocation: Type[BotocoreClientError]
    MessageFrozen: Type[BotocoreClientError]
    MessageRejected: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class WorkMailMessageFlowClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_workmailmessageflow/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkMailMessageFlowClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_workmailmessageflow/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_workmailmessageflow/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_workmailmessageflow/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_workmailmessageflow/client/#close)
        """

    def get_raw_message_content(
        self, **kwargs: Unpack[GetRawMessageContentRequestRequestTypeDef]
    ) -> GetRawMessageContentResponseTypeDef:
        """
        Retrieves the raw content of an in-transit email message, in MIME format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow/client/get_raw_message_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_workmailmessageflow/client/#get_raw_message_content)
        """

    def put_raw_message_content(
        self, **kwargs: Unpack[PutRawMessageContentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the raw content of an in-transit email message, in MIME format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow/client/put_raw_message_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_workmailmessageflow/client/#put_raw_message_content)
        """
