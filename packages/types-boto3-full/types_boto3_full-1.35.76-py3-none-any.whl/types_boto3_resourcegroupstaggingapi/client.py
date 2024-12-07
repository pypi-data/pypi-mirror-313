"""
Type annotations for resourcegroupstaggingapi service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_resourcegroupstaggingapi.client import ResourceGroupsTaggingAPIClient

    session = Session()
    client: ResourceGroupsTaggingAPIClient = session.client("resourcegroupstaggingapi")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetComplianceSummaryPaginator,
    GetResourcesPaginator,
    GetTagKeysPaginator,
    GetTagValuesPaginator,
)
from .type_defs import (
    DescribeReportCreationOutputTypeDef,
    GetComplianceSummaryInputRequestTypeDef,
    GetComplianceSummaryOutputTypeDef,
    GetResourcesInputRequestTypeDef,
    GetResourcesOutputTypeDef,
    GetTagKeysInputRequestTypeDef,
    GetTagKeysOutputTypeDef,
    GetTagValuesInputRequestTypeDef,
    GetTagValuesOutputTypeDef,
    StartReportCreationInputRequestTypeDef,
    TagResourcesInputRequestTypeDef,
    TagResourcesOutputTypeDef,
    UntagResourcesInputRequestTypeDef,
    UntagResourcesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ResourceGroupsTaggingAPIClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConstraintViolationException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    PaginationTokenExpiredException: Type[BotocoreClientError]
    ThrottledException: Type[BotocoreClientError]


class ResourceGroupsTaggingAPIClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ResourceGroupsTaggingAPIClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#close)
        """

    def describe_report_creation(self) -> DescribeReportCreationOutputTypeDef:
        """
        Describes the status of the <code>StartReportCreation</code> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/describe_report_creation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#describe_report_creation)
        """

    def get_compliance_summary(
        self, **kwargs: Unpack[GetComplianceSummaryInputRequestTypeDef]
    ) -> GetComplianceSummaryOutputTypeDef:
        """
        Returns a table that shows counts of resources that are noncompliant with their
        tag policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/get_compliance_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#get_compliance_summary)
        """

    def get_resources(
        self, **kwargs: Unpack[GetResourcesInputRequestTypeDef]
    ) -> GetResourcesOutputTypeDef:
        """
        Returns all the tagged or previously tagged resources that are located in the
        specified Amazon Web Services Region for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/get_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#get_resources)
        """

    def get_tag_keys(
        self, **kwargs: Unpack[GetTagKeysInputRequestTypeDef]
    ) -> GetTagKeysOutputTypeDef:
        """
        Returns all tag keys currently in use in the specified Amazon Web Services
        Region for the calling account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/get_tag_keys.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#get_tag_keys)
        """

    def get_tag_values(
        self, **kwargs: Unpack[GetTagValuesInputRequestTypeDef]
    ) -> GetTagValuesOutputTypeDef:
        """
        Returns all tag values for the specified key that are used in the specified
        Amazon Web Services Region for the calling account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/get_tag_values.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#get_tag_values)
        """

    def start_report_creation(
        self, **kwargs: Unpack[StartReportCreationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Generates a report that lists all tagged resources in the accounts across your
        organization and tells whether each resource is compliant with the effective
        tag policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/start_report_creation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#start_report_creation)
        """

    def tag_resources(
        self, **kwargs: Unpack[TagResourcesInputRequestTypeDef]
    ) -> TagResourcesOutputTypeDef:
        """
        Applies one or more tags to the specified resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/tag_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#tag_resources)
        """

    def untag_resources(
        self, **kwargs: Unpack[UntagResourcesInputRequestTypeDef]
    ) -> UntagResourcesOutputTypeDef:
        """
        Removes the specified tags from the specified resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/untag_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#untag_resources)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_compliance_summary"]
    ) -> GetComplianceSummaryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_resources"]) -> GetResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_tag_keys"]) -> GetTagKeysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_tag_values"]) -> GetTagValuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resourcegroupstaggingapi/client/#get_paginator)
        """
