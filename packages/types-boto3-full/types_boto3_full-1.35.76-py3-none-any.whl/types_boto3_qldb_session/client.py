"""
Type annotations for qldb-session service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qldb_session/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_qldb_session.client import QLDBSessionClient

    session = Session()
    client: QLDBSessionClient = session.client("qldb-session")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import SendCommandRequestRequestTypeDef, SendCommandResultTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("QLDBSessionClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    CapacityExceededException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InvalidSessionException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    OccConflictException: Type[BotocoreClientError]
    RateExceededException: Type[BotocoreClientError]


class QLDBSessionClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session.html#QLDBSession.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qldb_session/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        QLDBSessionClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session.html#QLDBSession.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qldb_session/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qldb_session/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qldb_session/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qldb_session/client/#close)
        """

    def send_command(
        self, **kwargs: Unpack[SendCommandRequestRequestTypeDef]
    ) -> SendCommandResultTypeDef:
        """
        Sends a command to an Amazon QLDB ledger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session/client/send_command.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qldb_session/client/#send_command)
        """
