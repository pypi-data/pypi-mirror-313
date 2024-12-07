"""
Type annotations for tnb service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_tnb.client import TelcoNetworkBuilderClient

    session = Session()
    client: TelcoNetworkBuilderClient = session.client("tnb")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListSolFunctionInstancesPaginator,
    ListSolFunctionPackagesPaginator,
    ListSolNetworkInstancesPaginator,
    ListSolNetworkOperationsPaginator,
    ListSolNetworkPackagesPaginator,
)
from .type_defs import (
    CancelSolNetworkOperationInputRequestTypeDef,
    CreateSolFunctionPackageInputRequestTypeDef,
    CreateSolFunctionPackageOutputTypeDef,
    CreateSolNetworkInstanceInputRequestTypeDef,
    CreateSolNetworkInstanceOutputTypeDef,
    CreateSolNetworkPackageInputRequestTypeDef,
    CreateSolNetworkPackageOutputTypeDef,
    DeleteSolFunctionPackageInputRequestTypeDef,
    DeleteSolNetworkInstanceInputRequestTypeDef,
    DeleteSolNetworkPackageInputRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetSolFunctionInstanceInputRequestTypeDef,
    GetSolFunctionInstanceOutputTypeDef,
    GetSolFunctionPackageContentInputRequestTypeDef,
    GetSolFunctionPackageContentOutputTypeDef,
    GetSolFunctionPackageDescriptorInputRequestTypeDef,
    GetSolFunctionPackageDescriptorOutputTypeDef,
    GetSolFunctionPackageInputRequestTypeDef,
    GetSolFunctionPackageOutputTypeDef,
    GetSolNetworkInstanceInputRequestTypeDef,
    GetSolNetworkInstanceOutputTypeDef,
    GetSolNetworkOperationInputRequestTypeDef,
    GetSolNetworkOperationOutputTypeDef,
    GetSolNetworkPackageContentInputRequestTypeDef,
    GetSolNetworkPackageContentOutputTypeDef,
    GetSolNetworkPackageDescriptorInputRequestTypeDef,
    GetSolNetworkPackageDescriptorOutputTypeDef,
    GetSolNetworkPackageInputRequestTypeDef,
    GetSolNetworkPackageOutputTypeDef,
    InstantiateSolNetworkInstanceInputRequestTypeDef,
    InstantiateSolNetworkInstanceOutputTypeDef,
    ListSolFunctionInstancesInputRequestTypeDef,
    ListSolFunctionInstancesOutputTypeDef,
    ListSolFunctionPackagesInputRequestTypeDef,
    ListSolFunctionPackagesOutputTypeDef,
    ListSolNetworkInstancesInputRequestTypeDef,
    ListSolNetworkInstancesOutputTypeDef,
    ListSolNetworkOperationsInputRequestTypeDef,
    ListSolNetworkOperationsOutputTypeDef,
    ListSolNetworkPackagesInputRequestTypeDef,
    ListSolNetworkPackagesOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    PutSolFunctionPackageContentInputRequestTypeDef,
    PutSolFunctionPackageContentOutputTypeDef,
    PutSolNetworkPackageContentInputRequestTypeDef,
    PutSolNetworkPackageContentOutputTypeDef,
    TagResourceInputRequestTypeDef,
    TerminateSolNetworkInstanceInputRequestTypeDef,
    TerminateSolNetworkInstanceOutputTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateSolFunctionPackageInputRequestTypeDef,
    UpdateSolFunctionPackageOutputTypeDef,
    UpdateSolNetworkInstanceInputRequestTypeDef,
    UpdateSolNetworkInstanceOutputTypeDef,
    UpdateSolNetworkPackageInputRequestTypeDef,
    UpdateSolNetworkPackageOutputTypeDef,
    ValidateSolFunctionPackageContentInputRequestTypeDef,
    ValidateSolFunctionPackageContentOutputTypeDef,
    ValidateSolNetworkPackageContentInputRequestTypeDef,
    ValidateSolNetworkPackageContentOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("TelcoNetworkBuilderClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class TelcoNetworkBuilderClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb.html#TelcoNetworkBuilder.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TelcoNetworkBuilderClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb.html#TelcoNetworkBuilder.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#close)
        """

    def cancel_sol_network_operation(
        self, **kwargs: Unpack[CancelSolNetworkOperationInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels a network operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/cancel_sol_network_operation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#cancel_sol_network_operation)
        """

    def create_sol_function_package(
        self, **kwargs: Unpack[CreateSolFunctionPackageInputRequestTypeDef]
    ) -> CreateSolFunctionPackageOutputTypeDef:
        """
        Creates a function package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/create_sol_function_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#create_sol_function_package)
        """

    def create_sol_network_instance(
        self, **kwargs: Unpack[CreateSolNetworkInstanceInputRequestTypeDef]
    ) -> CreateSolNetworkInstanceOutputTypeDef:
        """
        Creates a network instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/create_sol_network_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#create_sol_network_instance)
        """

    def create_sol_network_package(
        self, **kwargs: Unpack[CreateSolNetworkPackageInputRequestTypeDef]
    ) -> CreateSolNetworkPackageOutputTypeDef:
        """
        Creates a network package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/create_sol_network_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#create_sol_network_package)
        """

    def delete_sol_function_package(
        self, **kwargs: Unpack[DeleteSolFunctionPackageInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a function package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/delete_sol_function_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#delete_sol_function_package)
        """

    def delete_sol_network_instance(
        self, **kwargs: Unpack[DeleteSolNetworkInstanceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a network instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/delete_sol_network_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#delete_sol_network_instance)
        """

    def delete_sol_network_package(
        self, **kwargs: Unpack[DeleteSolNetworkPackageInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes network package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/delete_sol_network_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#delete_sol_network_package)
        """

    def get_sol_function_instance(
        self, **kwargs: Unpack[GetSolFunctionInstanceInputRequestTypeDef]
    ) -> GetSolFunctionInstanceOutputTypeDef:
        """
        Gets the details of a network function instance, including the instantiation
        state and metadata from the function package descriptor in the network function
        package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_function_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_sol_function_instance)
        """

    def get_sol_function_package(
        self, **kwargs: Unpack[GetSolFunctionPackageInputRequestTypeDef]
    ) -> GetSolFunctionPackageOutputTypeDef:
        """
        Gets the details of an individual function package, such as the operational
        state and whether the package is in use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_function_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_sol_function_package)
        """

    def get_sol_function_package_content(
        self, **kwargs: Unpack[GetSolFunctionPackageContentInputRequestTypeDef]
    ) -> GetSolFunctionPackageContentOutputTypeDef:
        """
        Gets the contents of a function package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_function_package_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_sol_function_package_content)
        """

    def get_sol_function_package_descriptor(
        self, **kwargs: Unpack[GetSolFunctionPackageDescriptorInputRequestTypeDef]
    ) -> GetSolFunctionPackageDescriptorOutputTypeDef:
        """
        Gets a function package descriptor in a function package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_function_package_descriptor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_sol_function_package_descriptor)
        """

    def get_sol_network_instance(
        self, **kwargs: Unpack[GetSolNetworkInstanceInputRequestTypeDef]
    ) -> GetSolNetworkInstanceOutputTypeDef:
        """
        Gets the details of the network instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_network_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_sol_network_instance)
        """

    def get_sol_network_operation(
        self, **kwargs: Unpack[GetSolNetworkOperationInputRequestTypeDef]
    ) -> GetSolNetworkOperationOutputTypeDef:
        """
        Gets the details of a network operation, including the tasks involved in the
        network operation and the status of the tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_network_operation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_sol_network_operation)
        """

    def get_sol_network_package(
        self, **kwargs: Unpack[GetSolNetworkPackageInputRequestTypeDef]
    ) -> GetSolNetworkPackageOutputTypeDef:
        """
        Gets the details of a network package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_network_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_sol_network_package)
        """

    def get_sol_network_package_content(
        self, **kwargs: Unpack[GetSolNetworkPackageContentInputRequestTypeDef]
    ) -> GetSolNetworkPackageContentOutputTypeDef:
        """
        Gets the contents of a network package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_network_package_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_sol_network_package_content)
        """

    def get_sol_network_package_descriptor(
        self, **kwargs: Unpack[GetSolNetworkPackageDescriptorInputRequestTypeDef]
    ) -> GetSolNetworkPackageDescriptorOutputTypeDef:
        """
        Gets the content of the network service descriptor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_network_package_descriptor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_sol_network_package_descriptor)
        """

    def instantiate_sol_network_instance(
        self, **kwargs: Unpack[InstantiateSolNetworkInstanceInputRequestTypeDef]
    ) -> InstantiateSolNetworkInstanceOutputTypeDef:
        """
        Instantiates a network instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/instantiate_sol_network_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#instantiate_sol_network_instance)
        """

    def list_sol_function_instances(
        self, **kwargs: Unpack[ListSolFunctionInstancesInputRequestTypeDef]
    ) -> ListSolFunctionInstancesOutputTypeDef:
        """
        Lists network function instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/list_sol_function_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#list_sol_function_instances)
        """

    def list_sol_function_packages(
        self, **kwargs: Unpack[ListSolFunctionPackagesInputRequestTypeDef]
    ) -> ListSolFunctionPackagesOutputTypeDef:
        """
        Lists information about function packages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/list_sol_function_packages.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#list_sol_function_packages)
        """

    def list_sol_network_instances(
        self, **kwargs: Unpack[ListSolNetworkInstancesInputRequestTypeDef]
    ) -> ListSolNetworkInstancesOutputTypeDef:
        """
        Lists your network instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/list_sol_network_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#list_sol_network_instances)
        """

    def list_sol_network_operations(
        self, **kwargs: Unpack[ListSolNetworkOperationsInputRequestTypeDef]
    ) -> ListSolNetworkOperationsOutputTypeDef:
        """
        Lists details for a network operation, including when the operation started and
        the status of the operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/list_sol_network_operations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#list_sol_network_operations)
        """

    def list_sol_network_packages(
        self, **kwargs: Unpack[ListSolNetworkPackagesInputRequestTypeDef]
    ) -> ListSolNetworkPackagesOutputTypeDef:
        """
        Lists network packages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/list_sol_network_packages.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#list_sol_network_packages)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists tags for AWS TNB resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#list_tags_for_resource)
        """

    def put_sol_function_package_content(
        self, **kwargs: Unpack[PutSolFunctionPackageContentInputRequestTypeDef]
    ) -> PutSolFunctionPackageContentOutputTypeDef:
        """
        Uploads the contents of a function package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/put_sol_function_package_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#put_sol_function_package_content)
        """

    def put_sol_network_package_content(
        self, **kwargs: Unpack[PutSolNetworkPackageContentInputRequestTypeDef]
    ) -> PutSolNetworkPackageContentOutputTypeDef:
        """
        Uploads the contents of a network package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/put_sol_network_package_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#put_sol_network_package_content)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags an AWS TNB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#tag_resource)
        """

    def terminate_sol_network_instance(
        self, **kwargs: Unpack[TerminateSolNetworkInstanceInputRequestTypeDef]
    ) -> TerminateSolNetworkInstanceOutputTypeDef:
        """
        Terminates a network instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/terminate_sol_network_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#terminate_sol_network_instance)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Untags an AWS TNB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#untag_resource)
        """

    def update_sol_function_package(
        self, **kwargs: Unpack[UpdateSolFunctionPackageInputRequestTypeDef]
    ) -> UpdateSolFunctionPackageOutputTypeDef:
        """
        Updates the operational state of function package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/update_sol_function_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#update_sol_function_package)
        """

    def update_sol_network_instance(
        self, **kwargs: Unpack[UpdateSolNetworkInstanceInputRequestTypeDef]
    ) -> UpdateSolNetworkInstanceOutputTypeDef:
        """
        Update a network instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/update_sol_network_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#update_sol_network_instance)
        """

    def update_sol_network_package(
        self, **kwargs: Unpack[UpdateSolNetworkPackageInputRequestTypeDef]
    ) -> UpdateSolNetworkPackageOutputTypeDef:
        """
        Updates the operational state of a network package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/update_sol_network_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#update_sol_network_package)
        """

    def validate_sol_function_package_content(
        self, **kwargs: Unpack[ValidateSolFunctionPackageContentInputRequestTypeDef]
    ) -> ValidateSolFunctionPackageContentOutputTypeDef:
        """
        Validates function package content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/validate_sol_function_package_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#validate_sol_function_package_content)
        """

    def validate_sol_network_package_content(
        self, **kwargs: Unpack[ValidateSolNetworkPackageContentInputRequestTypeDef]
    ) -> ValidateSolNetworkPackageContentOutputTypeDef:
        """
        Validates network package content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/validate_sol_network_package_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#validate_sol_network_package_content)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sol_function_instances"]
    ) -> ListSolFunctionInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sol_function_packages"]
    ) -> ListSolFunctionPackagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sol_network_instances"]
    ) -> ListSolNetworkInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sol_network_operations"]
    ) -> ListSolNetworkOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sol_network_packages"]
    ) -> ListSolNetworkPackagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_tnb/client/#get_paginator)
        """
