"""
Type annotations for cloudcontrol service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_cloudcontrol.client import CloudControlApiClient

    session = Session()
    client: CloudControlApiClient = session.client("cloudcontrol")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListResourceRequestsPaginator, ListResourcesPaginator
from .type_defs import (
    CancelResourceRequestInputRequestTypeDef,
    CancelResourceRequestOutputTypeDef,
    CreateResourceInputRequestTypeDef,
    CreateResourceOutputTypeDef,
    DeleteResourceInputRequestTypeDef,
    DeleteResourceOutputTypeDef,
    GetResourceInputRequestTypeDef,
    GetResourceOutputTypeDef,
    GetResourceRequestStatusInputRequestTypeDef,
    GetResourceRequestStatusOutputTypeDef,
    ListResourceRequestsInputRequestTypeDef,
    ListResourceRequestsOutputTypeDef,
    ListResourcesInputRequestTypeDef,
    ListResourcesOutputTypeDef,
    UpdateResourceInputRequestTypeDef,
    UpdateResourceOutputTypeDef,
)
from .waiter import ResourceRequestSuccessWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CloudControlApiClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientTokenConflictException: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConcurrentOperationException: Type[BotocoreClientError]
    GeneralServiceException: Type[BotocoreClientError]
    HandlerFailureException: Type[BotocoreClientError]
    HandlerInternalFailureException: Type[BotocoreClientError]
    InvalidCredentialsException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    NetworkFailureException: Type[BotocoreClientError]
    NotStabilizedException: Type[BotocoreClientError]
    NotUpdatableException: Type[BotocoreClientError]
    PrivateTypeException: Type[BotocoreClientError]
    RequestTokenNotFoundException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceInternalErrorException: Type[BotocoreClientError]
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TypeNotFoundException: Type[BotocoreClientError]
    UnsupportedActionException: Type[BotocoreClientError]


class CloudControlApiClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudControlApiClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#close)
        """

    def cancel_resource_request(
        self, **kwargs: Unpack[CancelResourceRequestInputRequestTypeDef]
    ) -> CancelResourceRequestOutputTypeDef:
        """
        Cancels the specified resource operation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/cancel_resource_request.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#cancel_resource_request)
        """

    def create_resource(
        self, **kwargs: Unpack[CreateResourceInputRequestTypeDef]
    ) -> CreateResourceOutputTypeDef:
        """
        Creates the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/create_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#create_resource)
        """

    def delete_resource(
        self, **kwargs: Unpack[DeleteResourceInputRequestTypeDef]
    ) -> DeleteResourceOutputTypeDef:
        """
        Deletes the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/delete_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#delete_resource)
        """

    def get_resource(
        self, **kwargs: Unpack[GetResourceInputRequestTypeDef]
    ) -> GetResourceOutputTypeDef:
        """
        Returns information about the current state of the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/get_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#get_resource)
        """

    def get_resource_request_status(
        self, **kwargs: Unpack[GetResourceRequestStatusInputRequestTypeDef]
    ) -> GetResourceRequestStatusOutputTypeDef:
        """
        Returns the current status of a resource operation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/get_resource_request_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#get_resource_request_status)
        """

    def list_resource_requests(
        self, **kwargs: Unpack[ListResourceRequestsInputRequestTypeDef]
    ) -> ListResourceRequestsOutputTypeDef:
        """
        Returns existing resource operation requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/list_resource_requests.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#list_resource_requests)
        """

    def list_resources(
        self, **kwargs: Unpack[ListResourcesInputRequestTypeDef]
    ) -> ListResourcesOutputTypeDef:
        """
        Returns information about the specified resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/list_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#list_resources)
        """

    def update_resource(
        self, **kwargs: Unpack[UpdateResourceInputRequestTypeDef]
    ) -> UpdateResourceOutputTypeDef:
        """
        Updates the specified property values in the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/update_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#update_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_requests"]
    ) -> ListResourceRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_resources"]) -> ListResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#get_paginator)
        """

    def get_waiter(
        self, waiter_name: Literal["resource_request_success"]
    ) -> ResourceRequestSuccessWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudcontrol/client/#get_waiter)
        """
