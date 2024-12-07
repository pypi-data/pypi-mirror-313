"""
Type annotations for greengrass service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_greengrass.client import GreengrassClient

    session = Session()
    client: GreengrassClient = session.client("greengrass")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListBulkDeploymentDetailedReportsPaginator,
    ListBulkDeploymentsPaginator,
    ListConnectorDefinitionsPaginator,
    ListConnectorDefinitionVersionsPaginator,
    ListCoreDefinitionsPaginator,
    ListCoreDefinitionVersionsPaginator,
    ListDeploymentsPaginator,
    ListDeviceDefinitionsPaginator,
    ListDeviceDefinitionVersionsPaginator,
    ListFunctionDefinitionsPaginator,
    ListFunctionDefinitionVersionsPaginator,
    ListGroupsPaginator,
    ListGroupVersionsPaginator,
    ListLoggerDefinitionsPaginator,
    ListLoggerDefinitionVersionsPaginator,
    ListResourceDefinitionsPaginator,
    ListResourceDefinitionVersionsPaginator,
    ListSubscriptionDefinitionsPaginator,
    ListSubscriptionDefinitionVersionsPaginator,
)
from .type_defs import (
    AssociateRoleToGroupRequestRequestTypeDef,
    AssociateRoleToGroupResponseTypeDef,
    AssociateServiceRoleToAccountRequestRequestTypeDef,
    AssociateServiceRoleToAccountResponseTypeDef,
    CreateConnectorDefinitionRequestRequestTypeDef,
    CreateConnectorDefinitionResponseTypeDef,
    CreateConnectorDefinitionVersionRequestRequestTypeDef,
    CreateConnectorDefinitionVersionResponseTypeDef,
    CreateCoreDefinitionRequestRequestTypeDef,
    CreateCoreDefinitionResponseTypeDef,
    CreateCoreDefinitionVersionRequestRequestTypeDef,
    CreateCoreDefinitionVersionResponseTypeDef,
    CreateDeploymentRequestRequestTypeDef,
    CreateDeploymentResponseTypeDef,
    CreateDeviceDefinitionRequestRequestTypeDef,
    CreateDeviceDefinitionResponseTypeDef,
    CreateDeviceDefinitionVersionRequestRequestTypeDef,
    CreateDeviceDefinitionVersionResponseTypeDef,
    CreateFunctionDefinitionRequestRequestTypeDef,
    CreateFunctionDefinitionResponseTypeDef,
    CreateFunctionDefinitionVersionRequestRequestTypeDef,
    CreateFunctionDefinitionVersionResponseTypeDef,
    CreateGroupCertificateAuthorityRequestRequestTypeDef,
    CreateGroupCertificateAuthorityResponseTypeDef,
    CreateGroupRequestRequestTypeDef,
    CreateGroupResponseTypeDef,
    CreateGroupVersionRequestRequestTypeDef,
    CreateGroupVersionResponseTypeDef,
    CreateLoggerDefinitionRequestRequestTypeDef,
    CreateLoggerDefinitionResponseTypeDef,
    CreateLoggerDefinitionVersionRequestRequestTypeDef,
    CreateLoggerDefinitionVersionResponseTypeDef,
    CreateResourceDefinitionRequestRequestTypeDef,
    CreateResourceDefinitionResponseTypeDef,
    CreateResourceDefinitionVersionRequestRequestTypeDef,
    CreateResourceDefinitionVersionResponseTypeDef,
    CreateSoftwareUpdateJobRequestRequestTypeDef,
    CreateSoftwareUpdateJobResponseTypeDef,
    CreateSubscriptionDefinitionRequestRequestTypeDef,
    CreateSubscriptionDefinitionResponseTypeDef,
    CreateSubscriptionDefinitionVersionRequestRequestTypeDef,
    CreateSubscriptionDefinitionVersionResponseTypeDef,
    DeleteConnectorDefinitionRequestRequestTypeDef,
    DeleteCoreDefinitionRequestRequestTypeDef,
    DeleteDeviceDefinitionRequestRequestTypeDef,
    DeleteFunctionDefinitionRequestRequestTypeDef,
    DeleteGroupRequestRequestTypeDef,
    DeleteLoggerDefinitionRequestRequestTypeDef,
    DeleteResourceDefinitionRequestRequestTypeDef,
    DeleteSubscriptionDefinitionRequestRequestTypeDef,
    DisassociateRoleFromGroupRequestRequestTypeDef,
    DisassociateRoleFromGroupResponseTypeDef,
    DisassociateServiceRoleFromAccountResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAssociatedRoleRequestRequestTypeDef,
    GetAssociatedRoleResponseTypeDef,
    GetBulkDeploymentStatusRequestRequestTypeDef,
    GetBulkDeploymentStatusResponseTypeDef,
    GetConnectivityInfoRequestRequestTypeDef,
    GetConnectivityInfoResponseTypeDef,
    GetConnectorDefinitionRequestRequestTypeDef,
    GetConnectorDefinitionResponseTypeDef,
    GetConnectorDefinitionVersionRequestRequestTypeDef,
    GetConnectorDefinitionVersionResponseTypeDef,
    GetCoreDefinitionRequestRequestTypeDef,
    GetCoreDefinitionResponseTypeDef,
    GetCoreDefinitionVersionRequestRequestTypeDef,
    GetCoreDefinitionVersionResponseTypeDef,
    GetDeploymentStatusRequestRequestTypeDef,
    GetDeploymentStatusResponseTypeDef,
    GetDeviceDefinitionRequestRequestTypeDef,
    GetDeviceDefinitionResponseTypeDef,
    GetDeviceDefinitionVersionRequestRequestTypeDef,
    GetDeviceDefinitionVersionResponseTypeDef,
    GetFunctionDefinitionRequestRequestTypeDef,
    GetFunctionDefinitionResponseTypeDef,
    GetFunctionDefinitionVersionRequestRequestTypeDef,
    GetFunctionDefinitionVersionResponseTypeDef,
    GetGroupCertificateAuthorityRequestRequestTypeDef,
    GetGroupCertificateAuthorityResponseTypeDef,
    GetGroupCertificateConfigurationRequestRequestTypeDef,
    GetGroupCertificateConfigurationResponseTypeDef,
    GetGroupRequestRequestTypeDef,
    GetGroupResponseTypeDef,
    GetGroupVersionRequestRequestTypeDef,
    GetGroupVersionResponseTypeDef,
    GetLoggerDefinitionRequestRequestTypeDef,
    GetLoggerDefinitionResponseTypeDef,
    GetLoggerDefinitionVersionRequestRequestTypeDef,
    GetLoggerDefinitionVersionResponseTypeDef,
    GetResourceDefinitionRequestRequestTypeDef,
    GetResourceDefinitionResponseTypeDef,
    GetResourceDefinitionVersionRequestRequestTypeDef,
    GetResourceDefinitionVersionResponseTypeDef,
    GetServiceRoleForAccountResponseTypeDef,
    GetSubscriptionDefinitionRequestRequestTypeDef,
    GetSubscriptionDefinitionResponseTypeDef,
    GetSubscriptionDefinitionVersionRequestRequestTypeDef,
    GetSubscriptionDefinitionVersionResponseTypeDef,
    GetThingRuntimeConfigurationRequestRequestTypeDef,
    GetThingRuntimeConfigurationResponseTypeDef,
    ListBulkDeploymentDetailedReportsRequestRequestTypeDef,
    ListBulkDeploymentDetailedReportsResponseTypeDef,
    ListBulkDeploymentsRequestRequestTypeDef,
    ListBulkDeploymentsResponseTypeDef,
    ListConnectorDefinitionsRequestRequestTypeDef,
    ListConnectorDefinitionsResponseTypeDef,
    ListConnectorDefinitionVersionsRequestRequestTypeDef,
    ListConnectorDefinitionVersionsResponseTypeDef,
    ListCoreDefinitionsRequestRequestTypeDef,
    ListCoreDefinitionsResponseTypeDef,
    ListCoreDefinitionVersionsRequestRequestTypeDef,
    ListCoreDefinitionVersionsResponseTypeDef,
    ListDeploymentsRequestRequestTypeDef,
    ListDeploymentsResponseTypeDef,
    ListDeviceDefinitionsRequestRequestTypeDef,
    ListDeviceDefinitionsResponseTypeDef,
    ListDeviceDefinitionVersionsRequestRequestTypeDef,
    ListDeviceDefinitionVersionsResponseTypeDef,
    ListFunctionDefinitionsRequestRequestTypeDef,
    ListFunctionDefinitionsResponseTypeDef,
    ListFunctionDefinitionVersionsRequestRequestTypeDef,
    ListFunctionDefinitionVersionsResponseTypeDef,
    ListGroupCertificateAuthoritiesRequestRequestTypeDef,
    ListGroupCertificateAuthoritiesResponseTypeDef,
    ListGroupsRequestRequestTypeDef,
    ListGroupsResponseTypeDef,
    ListGroupVersionsRequestRequestTypeDef,
    ListGroupVersionsResponseTypeDef,
    ListLoggerDefinitionsRequestRequestTypeDef,
    ListLoggerDefinitionsResponseTypeDef,
    ListLoggerDefinitionVersionsRequestRequestTypeDef,
    ListLoggerDefinitionVersionsResponseTypeDef,
    ListResourceDefinitionsRequestRequestTypeDef,
    ListResourceDefinitionsResponseTypeDef,
    ListResourceDefinitionVersionsRequestRequestTypeDef,
    ListResourceDefinitionVersionsResponseTypeDef,
    ListSubscriptionDefinitionsRequestRequestTypeDef,
    ListSubscriptionDefinitionsResponseTypeDef,
    ListSubscriptionDefinitionVersionsRequestRequestTypeDef,
    ListSubscriptionDefinitionVersionsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ResetDeploymentsRequestRequestTypeDef,
    ResetDeploymentsResponseTypeDef,
    StartBulkDeploymentRequestRequestTypeDef,
    StartBulkDeploymentResponseTypeDef,
    StopBulkDeploymentRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateConnectivityInfoRequestRequestTypeDef,
    UpdateConnectivityInfoResponseTypeDef,
    UpdateConnectorDefinitionRequestRequestTypeDef,
    UpdateCoreDefinitionRequestRequestTypeDef,
    UpdateDeviceDefinitionRequestRequestTypeDef,
    UpdateFunctionDefinitionRequestRequestTypeDef,
    UpdateGroupCertificateConfigurationRequestRequestTypeDef,
    UpdateGroupCertificateConfigurationResponseTypeDef,
    UpdateGroupRequestRequestTypeDef,
    UpdateLoggerDefinitionRequestRequestTypeDef,
    UpdateResourceDefinitionRequestRequestTypeDef,
    UpdateSubscriptionDefinitionRequestRequestTypeDef,
    UpdateThingRuntimeConfigurationRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("GreengrassClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]

class GreengrassClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GreengrassClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#close)
        """

    def associate_role_to_group(
        self, **kwargs: Unpack[AssociateRoleToGroupRequestRequestTypeDef]
    ) -> AssociateRoleToGroupResponseTypeDef:
        """
        Associates a role with a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/associate_role_to_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#associate_role_to_group)
        """

    def associate_service_role_to_account(
        self, **kwargs: Unpack[AssociateServiceRoleToAccountRequestRequestTypeDef]
    ) -> AssociateServiceRoleToAccountResponseTypeDef:
        """
        Associates a role with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/associate_service_role_to_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#associate_service_role_to_account)
        """

    def create_connector_definition(
        self, **kwargs: Unpack[CreateConnectorDefinitionRequestRequestTypeDef]
    ) -> CreateConnectorDefinitionResponseTypeDef:
        """
        Creates a connector definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_connector_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_connector_definition)
        """

    def create_connector_definition_version(
        self, **kwargs: Unpack[CreateConnectorDefinitionVersionRequestRequestTypeDef]
    ) -> CreateConnectorDefinitionVersionResponseTypeDef:
        """
        Creates a version of a connector definition which has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_connector_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_connector_definition_version)
        """

    def create_core_definition(
        self, **kwargs: Unpack[CreateCoreDefinitionRequestRequestTypeDef]
    ) -> CreateCoreDefinitionResponseTypeDef:
        """
        Creates a core definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_core_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_core_definition)
        """

    def create_core_definition_version(
        self, **kwargs: Unpack[CreateCoreDefinitionVersionRequestRequestTypeDef]
    ) -> CreateCoreDefinitionVersionResponseTypeDef:
        """
        Creates a version of a core definition that has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_core_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_core_definition_version)
        """

    def create_deployment(
        self, **kwargs: Unpack[CreateDeploymentRequestRequestTypeDef]
    ) -> CreateDeploymentResponseTypeDef:
        """
        Creates a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_deployment)
        """

    def create_device_definition(
        self, **kwargs: Unpack[CreateDeviceDefinitionRequestRequestTypeDef]
    ) -> CreateDeviceDefinitionResponseTypeDef:
        """
        Creates a device definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_device_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_device_definition)
        """

    def create_device_definition_version(
        self, **kwargs: Unpack[CreateDeviceDefinitionVersionRequestRequestTypeDef]
    ) -> CreateDeviceDefinitionVersionResponseTypeDef:
        """
        Creates a version of a device definition that has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_device_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_device_definition_version)
        """

    def create_function_definition(
        self, **kwargs: Unpack[CreateFunctionDefinitionRequestRequestTypeDef]
    ) -> CreateFunctionDefinitionResponseTypeDef:
        """
        Creates a Lambda function definition which contains a list of Lambda functions
        and their configurations to be used in a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_function_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_function_definition)
        """

    def create_function_definition_version(
        self, **kwargs: Unpack[CreateFunctionDefinitionVersionRequestRequestTypeDef]
    ) -> CreateFunctionDefinitionVersionResponseTypeDef:
        """
        Creates a version of a Lambda function definition that has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_function_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_function_definition_version)
        """

    def create_group(
        self, **kwargs: Unpack[CreateGroupRequestRequestTypeDef]
    ) -> CreateGroupResponseTypeDef:
        """
        Creates a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_group)
        """

    def create_group_certificate_authority(
        self, **kwargs: Unpack[CreateGroupCertificateAuthorityRequestRequestTypeDef]
    ) -> CreateGroupCertificateAuthorityResponseTypeDef:
        """
        Creates a CA for the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_group_certificate_authority.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_group_certificate_authority)
        """

    def create_group_version(
        self, **kwargs: Unpack[CreateGroupVersionRequestRequestTypeDef]
    ) -> CreateGroupVersionResponseTypeDef:
        """
        Creates a version of a group which has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_group_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_group_version)
        """

    def create_logger_definition(
        self, **kwargs: Unpack[CreateLoggerDefinitionRequestRequestTypeDef]
    ) -> CreateLoggerDefinitionResponseTypeDef:
        """
        Creates a logger definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_logger_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_logger_definition)
        """

    def create_logger_definition_version(
        self, **kwargs: Unpack[CreateLoggerDefinitionVersionRequestRequestTypeDef]
    ) -> CreateLoggerDefinitionVersionResponseTypeDef:
        """
        Creates a version of a logger definition that has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_logger_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_logger_definition_version)
        """

    def create_resource_definition(
        self, **kwargs: Unpack[CreateResourceDefinitionRequestRequestTypeDef]
    ) -> CreateResourceDefinitionResponseTypeDef:
        """
        Creates a resource definition which contains a list of resources to be used in
        a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_resource_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_resource_definition)
        """

    def create_resource_definition_version(
        self, **kwargs: Unpack[CreateResourceDefinitionVersionRequestRequestTypeDef]
    ) -> CreateResourceDefinitionVersionResponseTypeDef:
        """
        Creates a version of a resource definition that has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_resource_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_resource_definition_version)
        """

    def create_software_update_job(
        self, **kwargs: Unpack[CreateSoftwareUpdateJobRequestRequestTypeDef]
    ) -> CreateSoftwareUpdateJobResponseTypeDef:
        """
        Creates a software update for a core or group of cores (specified as an IoT
        thing group.) Use this to update the OTA Agent as well as the Greengrass core
        software.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_software_update_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_software_update_job)
        """

    def create_subscription_definition(
        self, **kwargs: Unpack[CreateSubscriptionDefinitionRequestRequestTypeDef]
    ) -> CreateSubscriptionDefinitionResponseTypeDef:
        """
        Creates a subscription definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_subscription_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_subscription_definition)
        """

    def create_subscription_definition_version(
        self, **kwargs: Unpack[CreateSubscriptionDefinitionVersionRequestRequestTypeDef]
    ) -> CreateSubscriptionDefinitionVersionResponseTypeDef:
        """
        Creates a version of a subscription definition which has already been defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/create_subscription_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#create_subscription_definition_version)
        """

    def delete_connector_definition(
        self, **kwargs: Unpack[DeleteConnectorDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a connector definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/delete_connector_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#delete_connector_definition)
        """

    def delete_core_definition(
        self, **kwargs: Unpack[DeleteCoreDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a core definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/delete_core_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#delete_core_definition)
        """

    def delete_device_definition(
        self, **kwargs: Unpack[DeleteDeviceDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a device definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/delete_device_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#delete_device_definition)
        """

    def delete_function_definition(
        self, **kwargs: Unpack[DeleteFunctionDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Lambda function definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/delete_function_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#delete_function_definition)
        """

    def delete_group(self, **kwargs: Unpack[DeleteGroupRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/delete_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#delete_group)
        """

    def delete_logger_definition(
        self, **kwargs: Unpack[DeleteLoggerDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a logger definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/delete_logger_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#delete_logger_definition)
        """

    def delete_resource_definition(
        self, **kwargs: Unpack[DeleteResourceDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a resource definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/delete_resource_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#delete_resource_definition)
        """

    def delete_subscription_definition(
        self, **kwargs: Unpack[DeleteSubscriptionDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a subscription definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/delete_subscription_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#delete_subscription_definition)
        """

    def disassociate_role_from_group(
        self, **kwargs: Unpack[DisassociateRoleFromGroupRequestRequestTypeDef]
    ) -> DisassociateRoleFromGroupResponseTypeDef:
        """
        Disassociates the role from a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/disassociate_role_from_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#disassociate_role_from_group)
        """

    def disassociate_service_role_from_account(
        self,
    ) -> DisassociateServiceRoleFromAccountResponseTypeDef:
        """
        Disassociates the service role from your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/disassociate_service_role_from_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#disassociate_service_role_from_account)
        """

    def get_associated_role(
        self, **kwargs: Unpack[GetAssociatedRoleRequestRequestTypeDef]
    ) -> GetAssociatedRoleResponseTypeDef:
        """
        Retrieves the role associated with a particular group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_associated_role.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_associated_role)
        """

    def get_bulk_deployment_status(
        self, **kwargs: Unpack[GetBulkDeploymentStatusRequestRequestTypeDef]
    ) -> GetBulkDeploymentStatusResponseTypeDef:
        """
        Returns the status of a bulk deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_bulk_deployment_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_bulk_deployment_status)
        """

    def get_connectivity_info(
        self, **kwargs: Unpack[GetConnectivityInfoRequestRequestTypeDef]
    ) -> GetConnectivityInfoResponseTypeDef:
        """
        Retrieves the connectivity information for a core.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_connectivity_info.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_connectivity_info)
        """

    def get_connector_definition(
        self, **kwargs: Unpack[GetConnectorDefinitionRequestRequestTypeDef]
    ) -> GetConnectorDefinitionResponseTypeDef:
        """
        Retrieves information about a connector definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_connector_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_connector_definition)
        """

    def get_connector_definition_version(
        self, **kwargs: Unpack[GetConnectorDefinitionVersionRequestRequestTypeDef]
    ) -> GetConnectorDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a connector definition version, including the
        connectors that the version contains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_connector_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_connector_definition_version)
        """

    def get_core_definition(
        self, **kwargs: Unpack[GetCoreDefinitionRequestRequestTypeDef]
    ) -> GetCoreDefinitionResponseTypeDef:
        """
        Retrieves information about a core definition version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_core_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_core_definition)
        """

    def get_core_definition_version(
        self, **kwargs: Unpack[GetCoreDefinitionVersionRequestRequestTypeDef]
    ) -> GetCoreDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a core definition version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_core_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_core_definition_version)
        """

    def get_deployment_status(
        self, **kwargs: Unpack[GetDeploymentStatusRequestRequestTypeDef]
    ) -> GetDeploymentStatusResponseTypeDef:
        """
        Returns the status of a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_deployment_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_deployment_status)
        """

    def get_device_definition(
        self, **kwargs: Unpack[GetDeviceDefinitionRequestRequestTypeDef]
    ) -> GetDeviceDefinitionResponseTypeDef:
        """
        Retrieves information about a device definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_device_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_device_definition)
        """

    def get_device_definition_version(
        self, **kwargs: Unpack[GetDeviceDefinitionVersionRequestRequestTypeDef]
    ) -> GetDeviceDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a device definition version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_device_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_device_definition_version)
        """

    def get_function_definition(
        self, **kwargs: Unpack[GetFunctionDefinitionRequestRequestTypeDef]
    ) -> GetFunctionDefinitionResponseTypeDef:
        """
        Retrieves information about a Lambda function definition, including its
        creation time and latest version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_function_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_function_definition)
        """

    def get_function_definition_version(
        self, **kwargs: Unpack[GetFunctionDefinitionVersionRequestRequestTypeDef]
    ) -> GetFunctionDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a Lambda function definition version, including
        which Lambda functions are included in the version and their configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_function_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_function_definition_version)
        """

    def get_group(self, **kwargs: Unpack[GetGroupRequestRequestTypeDef]) -> GetGroupResponseTypeDef:
        """
        Retrieves information about a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_group)
        """

    def get_group_certificate_authority(
        self, **kwargs: Unpack[GetGroupCertificateAuthorityRequestRequestTypeDef]
    ) -> GetGroupCertificateAuthorityResponseTypeDef:
        """
        Retreives the CA associated with a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_group_certificate_authority.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_group_certificate_authority)
        """

    def get_group_certificate_configuration(
        self, **kwargs: Unpack[GetGroupCertificateConfigurationRequestRequestTypeDef]
    ) -> GetGroupCertificateConfigurationResponseTypeDef:
        """
        Retrieves the current configuration for the CA used by the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_group_certificate_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_group_certificate_configuration)
        """

    def get_group_version(
        self, **kwargs: Unpack[GetGroupVersionRequestRequestTypeDef]
    ) -> GetGroupVersionResponseTypeDef:
        """
        Retrieves information about a group version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_group_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_group_version)
        """

    def get_logger_definition(
        self, **kwargs: Unpack[GetLoggerDefinitionRequestRequestTypeDef]
    ) -> GetLoggerDefinitionResponseTypeDef:
        """
        Retrieves information about a logger definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_logger_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_logger_definition)
        """

    def get_logger_definition_version(
        self, **kwargs: Unpack[GetLoggerDefinitionVersionRequestRequestTypeDef]
    ) -> GetLoggerDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a logger definition version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_logger_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_logger_definition_version)
        """

    def get_resource_definition(
        self, **kwargs: Unpack[GetResourceDefinitionRequestRequestTypeDef]
    ) -> GetResourceDefinitionResponseTypeDef:
        """
        Retrieves information about a resource definition, including its creation time
        and latest version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_resource_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_resource_definition)
        """

    def get_resource_definition_version(
        self, **kwargs: Unpack[GetResourceDefinitionVersionRequestRequestTypeDef]
    ) -> GetResourceDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a resource definition version, including which
        resources are included in the version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_resource_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_resource_definition_version)
        """

    def get_service_role_for_account(self) -> GetServiceRoleForAccountResponseTypeDef:
        """
        Retrieves the service role that is attached to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_service_role_for_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_service_role_for_account)
        """

    def get_subscription_definition(
        self, **kwargs: Unpack[GetSubscriptionDefinitionRequestRequestTypeDef]
    ) -> GetSubscriptionDefinitionResponseTypeDef:
        """
        Retrieves information about a subscription definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_subscription_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_subscription_definition)
        """

    def get_subscription_definition_version(
        self, **kwargs: Unpack[GetSubscriptionDefinitionVersionRequestRequestTypeDef]
    ) -> GetSubscriptionDefinitionVersionResponseTypeDef:
        """
        Retrieves information about a subscription definition version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_subscription_definition_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_subscription_definition_version)
        """

    def get_thing_runtime_configuration(
        self, **kwargs: Unpack[GetThingRuntimeConfigurationRequestRequestTypeDef]
    ) -> GetThingRuntimeConfigurationResponseTypeDef:
        """
        Get the runtime configuration of a thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_thing_runtime_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_thing_runtime_configuration)
        """

    def list_bulk_deployment_detailed_reports(
        self, **kwargs: Unpack[ListBulkDeploymentDetailedReportsRequestRequestTypeDef]
    ) -> ListBulkDeploymentDetailedReportsResponseTypeDef:
        """
        Gets a paginated list of the deployments that have been started in a bulk
        deployment operation, and their current deployment status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_bulk_deployment_detailed_reports.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_bulk_deployment_detailed_reports)
        """

    def list_bulk_deployments(
        self, **kwargs: Unpack[ListBulkDeploymentsRequestRequestTypeDef]
    ) -> ListBulkDeploymentsResponseTypeDef:
        """
        Returns a list of bulk deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_bulk_deployments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_bulk_deployments)
        """

    def list_connector_definition_versions(
        self, **kwargs: Unpack[ListConnectorDefinitionVersionsRequestRequestTypeDef]
    ) -> ListConnectorDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a connector definition, which are containers for
        connectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_connector_definition_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_connector_definition_versions)
        """

    def list_connector_definitions(
        self, **kwargs: Unpack[ListConnectorDefinitionsRequestRequestTypeDef]
    ) -> ListConnectorDefinitionsResponseTypeDef:
        """
        Retrieves a list of connector definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_connector_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_connector_definitions)
        """

    def list_core_definition_versions(
        self, **kwargs: Unpack[ListCoreDefinitionVersionsRequestRequestTypeDef]
    ) -> ListCoreDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a core definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_core_definition_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_core_definition_versions)
        """

    def list_core_definitions(
        self, **kwargs: Unpack[ListCoreDefinitionsRequestRequestTypeDef]
    ) -> ListCoreDefinitionsResponseTypeDef:
        """
        Retrieves a list of core definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_core_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_core_definitions)
        """

    def list_deployments(
        self, **kwargs: Unpack[ListDeploymentsRequestRequestTypeDef]
    ) -> ListDeploymentsResponseTypeDef:
        """
        Returns a history of deployments for the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_deployments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_deployments)
        """

    def list_device_definition_versions(
        self, **kwargs: Unpack[ListDeviceDefinitionVersionsRequestRequestTypeDef]
    ) -> ListDeviceDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a device definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_device_definition_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_device_definition_versions)
        """

    def list_device_definitions(
        self, **kwargs: Unpack[ListDeviceDefinitionsRequestRequestTypeDef]
    ) -> ListDeviceDefinitionsResponseTypeDef:
        """
        Retrieves a list of device definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_device_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_device_definitions)
        """

    def list_function_definition_versions(
        self, **kwargs: Unpack[ListFunctionDefinitionVersionsRequestRequestTypeDef]
    ) -> ListFunctionDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a Lambda function definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_function_definition_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_function_definition_versions)
        """

    def list_function_definitions(
        self, **kwargs: Unpack[ListFunctionDefinitionsRequestRequestTypeDef]
    ) -> ListFunctionDefinitionsResponseTypeDef:
        """
        Retrieves a list of Lambda function definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_function_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_function_definitions)
        """

    def list_group_certificate_authorities(
        self, **kwargs: Unpack[ListGroupCertificateAuthoritiesRequestRequestTypeDef]
    ) -> ListGroupCertificateAuthoritiesResponseTypeDef:
        """
        Retrieves the current CAs for a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_group_certificate_authorities.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_group_certificate_authorities)
        """

    def list_group_versions(
        self, **kwargs: Unpack[ListGroupVersionsRequestRequestTypeDef]
    ) -> ListGroupVersionsResponseTypeDef:
        """
        Lists the versions of a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_group_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_group_versions)
        """

    def list_groups(
        self, **kwargs: Unpack[ListGroupsRequestRequestTypeDef]
    ) -> ListGroupsResponseTypeDef:
        """
        Retrieves a list of groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_groups)
        """

    def list_logger_definition_versions(
        self, **kwargs: Unpack[ListLoggerDefinitionVersionsRequestRequestTypeDef]
    ) -> ListLoggerDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a logger definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_logger_definition_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_logger_definition_versions)
        """

    def list_logger_definitions(
        self, **kwargs: Unpack[ListLoggerDefinitionsRequestRequestTypeDef]
    ) -> ListLoggerDefinitionsResponseTypeDef:
        """
        Retrieves a list of logger definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_logger_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_logger_definitions)
        """

    def list_resource_definition_versions(
        self, **kwargs: Unpack[ListResourceDefinitionVersionsRequestRequestTypeDef]
    ) -> ListResourceDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a resource definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_resource_definition_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_resource_definition_versions)
        """

    def list_resource_definitions(
        self, **kwargs: Unpack[ListResourceDefinitionsRequestRequestTypeDef]
    ) -> ListResourceDefinitionsResponseTypeDef:
        """
        Retrieves a list of resource definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_resource_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_resource_definitions)
        """

    def list_subscription_definition_versions(
        self, **kwargs: Unpack[ListSubscriptionDefinitionVersionsRequestRequestTypeDef]
    ) -> ListSubscriptionDefinitionVersionsResponseTypeDef:
        """
        Lists the versions of a subscription definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_subscription_definition_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_subscription_definition_versions)
        """

    def list_subscription_definitions(
        self, **kwargs: Unpack[ListSubscriptionDefinitionsRequestRequestTypeDef]
    ) -> ListSubscriptionDefinitionsResponseTypeDef:
        """
        Retrieves a list of subscription definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_subscription_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_subscription_definitions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves a list of resource tags for a resource arn.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#list_tags_for_resource)
        """

    def reset_deployments(
        self, **kwargs: Unpack[ResetDeploymentsRequestRequestTypeDef]
    ) -> ResetDeploymentsResponseTypeDef:
        """
        Resets a group's deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/reset_deployments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#reset_deployments)
        """

    def start_bulk_deployment(
        self, **kwargs: Unpack[StartBulkDeploymentRequestRequestTypeDef]
    ) -> StartBulkDeploymentResponseTypeDef:
        """
        Deploys multiple groups in one operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/start_bulk_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#start_bulk_deployment)
        """

    def stop_bulk_deployment(
        self, **kwargs: Unpack[StopBulkDeploymentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops the execution of a bulk deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/stop_bulk_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#stop_bulk_deployment)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds tags to a Greengrass resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove resource tags from a Greengrass Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#untag_resource)
        """

    def update_connectivity_info(
        self, **kwargs: Unpack[UpdateConnectivityInfoRequestRequestTypeDef]
    ) -> UpdateConnectivityInfoResponseTypeDef:
        """
        Updates the connectivity information for the core.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/update_connectivity_info.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#update_connectivity_info)
        """

    def update_connector_definition(
        self, **kwargs: Unpack[UpdateConnectorDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a connector definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/update_connector_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#update_connector_definition)
        """

    def update_core_definition(
        self, **kwargs: Unpack[UpdateCoreDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a core definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/update_core_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#update_core_definition)
        """

    def update_device_definition(
        self, **kwargs: Unpack[UpdateDeviceDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a device definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/update_device_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#update_device_definition)
        """

    def update_function_definition(
        self, **kwargs: Unpack[UpdateFunctionDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a Lambda function definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/update_function_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#update_function_definition)
        """

    def update_group(self, **kwargs: Unpack[UpdateGroupRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/update_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#update_group)
        """

    def update_group_certificate_configuration(
        self, **kwargs: Unpack[UpdateGroupCertificateConfigurationRequestRequestTypeDef]
    ) -> UpdateGroupCertificateConfigurationResponseTypeDef:
        """
        Updates the Certificate expiry time for a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/update_group_certificate_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#update_group_certificate_configuration)
        """

    def update_logger_definition(
        self, **kwargs: Unpack[UpdateLoggerDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a logger definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/update_logger_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#update_logger_definition)
        """

    def update_resource_definition(
        self, **kwargs: Unpack[UpdateResourceDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a resource definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/update_resource_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#update_resource_definition)
        """

    def update_subscription_definition(
        self, **kwargs: Unpack[UpdateSubscriptionDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a subscription definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/update_subscription_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#update_subscription_definition)
        """

    def update_thing_runtime_configuration(
        self, **kwargs: Unpack[UpdateThingRuntimeConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the runtime configuration of a thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/update_thing_runtime_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#update_thing_runtime_configuration)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bulk_deployment_detailed_reports"]
    ) -> ListBulkDeploymentDetailedReportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bulk_deployments"]
    ) -> ListBulkDeploymentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_connector_definition_versions"]
    ) -> ListConnectorDefinitionVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_connector_definitions"]
    ) -> ListConnectorDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_core_definition_versions"]
    ) -> ListCoreDefinitionVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_core_definitions"]
    ) -> ListCoreDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployments"]
    ) -> ListDeploymentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_definition_versions"]
    ) -> ListDeviceDefinitionVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_definitions"]
    ) -> ListDeviceDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_function_definition_versions"]
    ) -> ListFunctionDefinitionVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_function_definitions"]
    ) -> ListFunctionDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_versions"]
    ) -> ListGroupVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_logger_definition_versions"]
    ) -> ListLoggerDefinitionVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_logger_definitions"]
    ) -> ListLoggerDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_definition_versions"]
    ) -> ListResourceDefinitionVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_definitions"]
    ) -> ListResourceDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscription_definition_versions"]
    ) -> ListSubscriptionDefinitionVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscription_definitions"]
    ) -> ListSubscriptionDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrass/client/#get_paginator)
        """
