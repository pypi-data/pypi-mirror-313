"""
Type annotations for rbin service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_rbin.client import RecycleBinClient

    session = Session()
    client: RecycleBinClient = session.client("rbin")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListRulesPaginator
from .type_defs import (
    CreateRuleRequestRequestTypeDef,
    CreateRuleResponseTypeDef,
    DeleteRuleRequestRequestTypeDef,
    GetRuleRequestRequestTypeDef,
    GetRuleResponseTypeDef,
    ListRulesRequestRequestTypeDef,
    ListRulesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    LockRuleRequestRequestTypeDef,
    LockRuleResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UnlockRuleRequestRequestTypeDef,
    UnlockRuleResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateRuleRequestRequestTypeDef,
    UpdateRuleResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("RecycleBinClient",)

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
    ValidationException: Type[BotocoreClientError]

class RecycleBinClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RecycleBinClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin.html#RecycleBin.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#close)
        """

    def create_rule(
        self, **kwargs: Unpack[CreateRuleRequestRequestTypeDef]
    ) -> CreateRuleResponseTypeDef:
        """
        Creates a Recycle Bin retention rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/create_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#create_rule)
        """

    def delete_rule(self, **kwargs: Unpack[DeleteRuleRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a Recycle Bin retention rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/delete_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#delete_rule)
        """

    def get_rule(self, **kwargs: Unpack[GetRuleRequestRequestTypeDef]) -> GetRuleResponseTypeDef:
        """
        Gets information about a Recycle Bin retention rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/get_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#get_rule)
        """

    def list_rules(
        self, **kwargs: Unpack[ListRulesRequestRequestTypeDef]
    ) -> ListRulesResponseTypeDef:
        """
        Lists the Recycle Bin retention rules in the Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/list_rules.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#list_rules)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags assigned to a retention rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#list_tags_for_resource)
        """

    def lock_rule(self, **kwargs: Unpack[LockRuleRequestRequestTypeDef]) -> LockRuleResponseTypeDef:
        """
        Locks a Region-level retention rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/lock_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#lock_rule)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns tags to the specified retention rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#tag_resource)
        """

    def unlock_rule(
        self, **kwargs: Unpack[UnlockRuleRequestRequestTypeDef]
    ) -> UnlockRuleResponseTypeDef:
        """
        Unlocks a retention rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/unlock_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#unlock_rule)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Unassigns a tag from a retention rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#untag_resource)
        """

    def update_rule(
        self, **kwargs: Unpack[UpdateRuleRequestRequestTypeDef]
    ) -> UpdateRuleResponseTypeDef:
        """
        Updates an existing Recycle Bin retention rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/update_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#update_rule)
        """

    def get_paginator(self, operation_name: Literal["list_rules"]) -> ListRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rbin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rbin/client/#get_paginator)
        """
