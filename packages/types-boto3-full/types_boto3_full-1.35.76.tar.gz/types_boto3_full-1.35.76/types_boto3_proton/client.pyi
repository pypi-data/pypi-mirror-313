"""
Type annotations for proton service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_proton.client import ProtonClient

    session = Session()
    client: ProtonClient = session.client("proton")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListComponentOutputsPaginator,
    ListComponentProvisionedResourcesPaginator,
    ListComponentsPaginator,
    ListDeploymentsPaginator,
    ListEnvironmentAccountConnectionsPaginator,
    ListEnvironmentOutputsPaginator,
    ListEnvironmentProvisionedResourcesPaginator,
    ListEnvironmentsPaginator,
    ListEnvironmentTemplatesPaginator,
    ListEnvironmentTemplateVersionsPaginator,
    ListRepositoriesPaginator,
    ListRepositorySyncDefinitionsPaginator,
    ListServiceInstanceOutputsPaginator,
    ListServiceInstanceProvisionedResourcesPaginator,
    ListServiceInstancesPaginator,
    ListServicePipelineOutputsPaginator,
    ListServicePipelineProvisionedResourcesPaginator,
    ListServicesPaginator,
    ListServiceTemplatesPaginator,
    ListServiceTemplateVersionsPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    AcceptEnvironmentAccountConnectionInputRequestTypeDef,
    AcceptEnvironmentAccountConnectionOutputTypeDef,
    CancelComponentDeploymentInputRequestTypeDef,
    CancelComponentDeploymentOutputTypeDef,
    CancelEnvironmentDeploymentInputRequestTypeDef,
    CancelEnvironmentDeploymentOutputTypeDef,
    CancelServiceInstanceDeploymentInputRequestTypeDef,
    CancelServiceInstanceDeploymentOutputTypeDef,
    CancelServicePipelineDeploymentInputRequestTypeDef,
    CancelServicePipelineDeploymentOutputTypeDef,
    CreateComponentInputRequestTypeDef,
    CreateComponentOutputTypeDef,
    CreateEnvironmentAccountConnectionInputRequestTypeDef,
    CreateEnvironmentAccountConnectionOutputTypeDef,
    CreateEnvironmentInputRequestTypeDef,
    CreateEnvironmentOutputTypeDef,
    CreateEnvironmentTemplateInputRequestTypeDef,
    CreateEnvironmentTemplateOutputTypeDef,
    CreateEnvironmentTemplateVersionInputRequestTypeDef,
    CreateEnvironmentTemplateVersionOutputTypeDef,
    CreateRepositoryInputRequestTypeDef,
    CreateRepositoryOutputTypeDef,
    CreateServiceInputRequestTypeDef,
    CreateServiceInstanceInputRequestTypeDef,
    CreateServiceInstanceOutputTypeDef,
    CreateServiceOutputTypeDef,
    CreateServiceSyncConfigInputRequestTypeDef,
    CreateServiceSyncConfigOutputTypeDef,
    CreateServiceTemplateInputRequestTypeDef,
    CreateServiceTemplateOutputTypeDef,
    CreateServiceTemplateVersionInputRequestTypeDef,
    CreateServiceTemplateVersionOutputTypeDef,
    CreateTemplateSyncConfigInputRequestTypeDef,
    CreateTemplateSyncConfigOutputTypeDef,
    DeleteComponentInputRequestTypeDef,
    DeleteComponentOutputTypeDef,
    DeleteDeploymentInputRequestTypeDef,
    DeleteDeploymentOutputTypeDef,
    DeleteEnvironmentAccountConnectionInputRequestTypeDef,
    DeleteEnvironmentAccountConnectionOutputTypeDef,
    DeleteEnvironmentInputRequestTypeDef,
    DeleteEnvironmentOutputTypeDef,
    DeleteEnvironmentTemplateInputRequestTypeDef,
    DeleteEnvironmentTemplateOutputTypeDef,
    DeleteEnvironmentTemplateVersionInputRequestTypeDef,
    DeleteEnvironmentTemplateVersionOutputTypeDef,
    DeleteRepositoryInputRequestTypeDef,
    DeleteRepositoryOutputTypeDef,
    DeleteServiceInputRequestTypeDef,
    DeleteServiceOutputTypeDef,
    DeleteServiceSyncConfigInputRequestTypeDef,
    DeleteServiceSyncConfigOutputTypeDef,
    DeleteServiceTemplateInputRequestTypeDef,
    DeleteServiceTemplateOutputTypeDef,
    DeleteServiceTemplateVersionInputRequestTypeDef,
    DeleteServiceTemplateVersionOutputTypeDef,
    DeleteTemplateSyncConfigInputRequestTypeDef,
    DeleteTemplateSyncConfigOutputTypeDef,
    GetAccountSettingsOutputTypeDef,
    GetComponentInputRequestTypeDef,
    GetComponentOutputTypeDef,
    GetDeploymentInputRequestTypeDef,
    GetDeploymentOutputTypeDef,
    GetEnvironmentAccountConnectionInputRequestTypeDef,
    GetEnvironmentAccountConnectionOutputTypeDef,
    GetEnvironmentInputRequestTypeDef,
    GetEnvironmentOutputTypeDef,
    GetEnvironmentTemplateInputRequestTypeDef,
    GetEnvironmentTemplateOutputTypeDef,
    GetEnvironmentTemplateVersionInputRequestTypeDef,
    GetEnvironmentTemplateVersionOutputTypeDef,
    GetRepositoryInputRequestTypeDef,
    GetRepositoryOutputTypeDef,
    GetRepositorySyncStatusInputRequestTypeDef,
    GetRepositorySyncStatusOutputTypeDef,
    GetResourcesSummaryOutputTypeDef,
    GetServiceInputRequestTypeDef,
    GetServiceInstanceInputRequestTypeDef,
    GetServiceInstanceOutputTypeDef,
    GetServiceInstanceSyncStatusInputRequestTypeDef,
    GetServiceInstanceSyncStatusOutputTypeDef,
    GetServiceOutputTypeDef,
    GetServiceSyncBlockerSummaryInputRequestTypeDef,
    GetServiceSyncBlockerSummaryOutputTypeDef,
    GetServiceSyncConfigInputRequestTypeDef,
    GetServiceSyncConfigOutputTypeDef,
    GetServiceTemplateInputRequestTypeDef,
    GetServiceTemplateOutputTypeDef,
    GetServiceTemplateVersionInputRequestTypeDef,
    GetServiceTemplateVersionOutputTypeDef,
    GetTemplateSyncConfigInputRequestTypeDef,
    GetTemplateSyncConfigOutputTypeDef,
    GetTemplateSyncStatusInputRequestTypeDef,
    GetTemplateSyncStatusOutputTypeDef,
    ListComponentOutputsInputRequestTypeDef,
    ListComponentOutputsOutputTypeDef,
    ListComponentProvisionedResourcesInputRequestTypeDef,
    ListComponentProvisionedResourcesOutputTypeDef,
    ListComponentsInputRequestTypeDef,
    ListComponentsOutputTypeDef,
    ListDeploymentsInputRequestTypeDef,
    ListDeploymentsOutputTypeDef,
    ListEnvironmentAccountConnectionsInputRequestTypeDef,
    ListEnvironmentAccountConnectionsOutputTypeDef,
    ListEnvironmentOutputsInputRequestTypeDef,
    ListEnvironmentOutputsOutputTypeDef,
    ListEnvironmentProvisionedResourcesInputRequestTypeDef,
    ListEnvironmentProvisionedResourcesOutputTypeDef,
    ListEnvironmentsInputRequestTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListEnvironmentTemplatesInputRequestTypeDef,
    ListEnvironmentTemplatesOutputTypeDef,
    ListEnvironmentTemplateVersionsInputRequestTypeDef,
    ListEnvironmentTemplateVersionsOutputTypeDef,
    ListRepositoriesInputRequestTypeDef,
    ListRepositoriesOutputTypeDef,
    ListRepositorySyncDefinitionsInputRequestTypeDef,
    ListRepositorySyncDefinitionsOutputTypeDef,
    ListServiceInstanceOutputsInputRequestTypeDef,
    ListServiceInstanceOutputsOutputTypeDef,
    ListServiceInstanceProvisionedResourcesInputRequestTypeDef,
    ListServiceInstanceProvisionedResourcesOutputTypeDef,
    ListServiceInstancesInputRequestTypeDef,
    ListServiceInstancesOutputTypeDef,
    ListServicePipelineOutputsInputRequestTypeDef,
    ListServicePipelineOutputsOutputTypeDef,
    ListServicePipelineProvisionedResourcesInputRequestTypeDef,
    ListServicePipelineProvisionedResourcesOutputTypeDef,
    ListServicesInputRequestTypeDef,
    ListServicesOutputTypeDef,
    ListServiceTemplatesInputRequestTypeDef,
    ListServiceTemplatesOutputTypeDef,
    ListServiceTemplateVersionsInputRequestTypeDef,
    ListServiceTemplateVersionsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    NotifyResourceDeploymentStatusChangeInputRequestTypeDef,
    RejectEnvironmentAccountConnectionInputRequestTypeDef,
    RejectEnvironmentAccountConnectionOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateAccountSettingsInputRequestTypeDef,
    UpdateAccountSettingsOutputTypeDef,
    UpdateComponentInputRequestTypeDef,
    UpdateComponentOutputTypeDef,
    UpdateEnvironmentAccountConnectionInputRequestTypeDef,
    UpdateEnvironmentAccountConnectionOutputTypeDef,
    UpdateEnvironmentInputRequestTypeDef,
    UpdateEnvironmentOutputTypeDef,
    UpdateEnvironmentTemplateInputRequestTypeDef,
    UpdateEnvironmentTemplateOutputTypeDef,
    UpdateEnvironmentTemplateVersionInputRequestTypeDef,
    UpdateEnvironmentTemplateVersionOutputTypeDef,
    UpdateServiceInputRequestTypeDef,
    UpdateServiceInstanceInputRequestTypeDef,
    UpdateServiceInstanceOutputTypeDef,
    UpdateServiceOutputTypeDef,
    UpdateServicePipelineInputRequestTypeDef,
    UpdateServicePipelineOutputTypeDef,
    UpdateServiceSyncBlockerInputRequestTypeDef,
    UpdateServiceSyncBlockerOutputTypeDef,
    UpdateServiceSyncConfigInputRequestTypeDef,
    UpdateServiceSyncConfigOutputTypeDef,
    UpdateServiceTemplateInputRequestTypeDef,
    UpdateServiceTemplateOutputTypeDef,
    UpdateServiceTemplateVersionInputRequestTypeDef,
    UpdateServiceTemplateVersionOutputTypeDef,
    UpdateTemplateSyncConfigInputRequestTypeDef,
    UpdateTemplateSyncConfigOutputTypeDef,
)
from .waiter import (
    ComponentDeletedWaiter,
    ComponentDeployedWaiter,
    EnvironmentDeployedWaiter,
    EnvironmentTemplateVersionRegisteredWaiter,
    ServiceCreatedWaiter,
    ServiceDeletedWaiter,
    ServiceInstanceDeployedWaiter,
    ServicePipelineDeployedWaiter,
    ServiceTemplateVersionRegisteredWaiter,
    ServiceUpdatedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ProtonClient",)

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
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class ProtonClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ProtonClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#close)
        """

    def accept_environment_account_connection(
        self, **kwargs: Unpack[AcceptEnvironmentAccountConnectionInputRequestTypeDef]
    ) -> AcceptEnvironmentAccountConnectionOutputTypeDef:
        """
        In a management account, an environment account connection request is accepted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/accept_environment_account_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#accept_environment_account_connection)
        """

    def cancel_component_deployment(
        self, **kwargs: Unpack[CancelComponentDeploymentInputRequestTypeDef]
    ) -> CancelComponentDeploymentOutputTypeDef:
        """
        Attempts to cancel a component deployment (for a component that is in the
        <code>IN_PROGRESS</code> deployment status).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/cancel_component_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#cancel_component_deployment)
        """

    def cancel_environment_deployment(
        self, **kwargs: Unpack[CancelEnvironmentDeploymentInputRequestTypeDef]
    ) -> CancelEnvironmentDeploymentOutputTypeDef:
        """
        Attempts to cancel an environment deployment on an <a>UpdateEnvironment</a>
        action, if the deployment is <code>IN_PROGRESS</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/cancel_environment_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#cancel_environment_deployment)
        """

    def cancel_service_instance_deployment(
        self, **kwargs: Unpack[CancelServiceInstanceDeploymentInputRequestTypeDef]
    ) -> CancelServiceInstanceDeploymentOutputTypeDef:
        """
        Attempts to cancel a service instance deployment on an
        <a>UpdateServiceInstance</a> action, if the deployment is
        <code>IN_PROGRESS</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/cancel_service_instance_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#cancel_service_instance_deployment)
        """

    def cancel_service_pipeline_deployment(
        self, **kwargs: Unpack[CancelServicePipelineDeploymentInputRequestTypeDef]
    ) -> CancelServicePipelineDeploymentOutputTypeDef:
        """
        Attempts to cancel a service pipeline deployment on an
        <a>UpdateServicePipeline</a> action, if the deployment is
        <code>IN_PROGRESS</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/cancel_service_pipeline_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#cancel_service_pipeline_deployment)
        """

    def create_component(
        self, **kwargs: Unpack[CreateComponentInputRequestTypeDef]
    ) -> CreateComponentOutputTypeDef:
        """
        Create an Proton component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_component.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#create_component)
        """

    def create_environment(
        self, **kwargs: Unpack[CreateEnvironmentInputRequestTypeDef]
    ) -> CreateEnvironmentOutputTypeDef:
        """
        Deploy a new environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#create_environment)
        """

    def create_environment_account_connection(
        self, **kwargs: Unpack[CreateEnvironmentAccountConnectionInputRequestTypeDef]
    ) -> CreateEnvironmentAccountConnectionOutputTypeDef:
        """
        Create an environment account connection in an environment account so that
        environment infrastructure resources can be provisioned in the environment
        account from a management account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_environment_account_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#create_environment_account_connection)
        """

    def create_environment_template(
        self, **kwargs: Unpack[CreateEnvironmentTemplateInputRequestTypeDef]
    ) -> CreateEnvironmentTemplateOutputTypeDef:
        """
        Create an environment template for Proton.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_environment_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#create_environment_template)
        """

    def create_environment_template_version(
        self, **kwargs: Unpack[CreateEnvironmentTemplateVersionInputRequestTypeDef]
    ) -> CreateEnvironmentTemplateVersionOutputTypeDef:
        """
        Create a new major or minor version of an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_environment_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#create_environment_template_version)
        """

    def create_repository(
        self, **kwargs: Unpack[CreateRepositoryInputRequestTypeDef]
    ) -> CreateRepositoryOutputTypeDef:
        """
        Create and register a link to a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_repository.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#create_repository)
        """

    def create_service(
        self, **kwargs: Unpack[CreateServiceInputRequestTypeDef]
    ) -> CreateServiceOutputTypeDef:
        """
        Create an Proton service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_service.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#create_service)
        """

    def create_service_instance(
        self, **kwargs: Unpack[CreateServiceInstanceInputRequestTypeDef]
    ) -> CreateServiceInstanceOutputTypeDef:
        """
        Create a service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_service_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#create_service_instance)
        """

    def create_service_sync_config(
        self, **kwargs: Unpack[CreateServiceSyncConfigInputRequestTypeDef]
    ) -> CreateServiceSyncConfigOutputTypeDef:
        """
        Create the Proton Ops configuration file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_service_sync_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#create_service_sync_config)
        """

    def create_service_template(
        self, **kwargs: Unpack[CreateServiceTemplateInputRequestTypeDef]
    ) -> CreateServiceTemplateOutputTypeDef:
        """
        Create a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_service_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#create_service_template)
        """

    def create_service_template_version(
        self, **kwargs: Unpack[CreateServiceTemplateVersionInputRequestTypeDef]
    ) -> CreateServiceTemplateVersionOutputTypeDef:
        """
        Create a new major or minor version of a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_service_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#create_service_template_version)
        """

    def create_template_sync_config(
        self, **kwargs: Unpack[CreateTemplateSyncConfigInputRequestTypeDef]
    ) -> CreateTemplateSyncConfigOutputTypeDef:
        """
        Set up a template to create new template versions automatically by tracking a
        linked repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_template_sync_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#create_template_sync_config)
        """

    def delete_component(
        self, **kwargs: Unpack[DeleteComponentInputRequestTypeDef]
    ) -> DeleteComponentOutputTypeDef:
        """
        Delete an Proton component resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_component.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#delete_component)
        """

    def delete_deployment(
        self, **kwargs: Unpack[DeleteDeploymentInputRequestTypeDef]
    ) -> DeleteDeploymentOutputTypeDef:
        """
        Delete the deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#delete_deployment)
        """

    def delete_environment(
        self, **kwargs: Unpack[DeleteEnvironmentInputRequestTypeDef]
    ) -> DeleteEnvironmentOutputTypeDef:
        """
        Delete an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#delete_environment)
        """

    def delete_environment_account_connection(
        self, **kwargs: Unpack[DeleteEnvironmentAccountConnectionInputRequestTypeDef]
    ) -> DeleteEnvironmentAccountConnectionOutputTypeDef:
        """
        In an environment account, delete an environment account connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_environment_account_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#delete_environment_account_connection)
        """

    def delete_environment_template(
        self, **kwargs: Unpack[DeleteEnvironmentTemplateInputRequestTypeDef]
    ) -> DeleteEnvironmentTemplateOutputTypeDef:
        """
        If no other major or minor versions of an environment template exist, delete
        the environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_environment_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#delete_environment_template)
        """

    def delete_environment_template_version(
        self, **kwargs: Unpack[DeleteEnvironmentTemplateVersionInputRequestTypeDef]
    ) -> DeleteEnvironmentTemplateVersionOutputTypeDef:
        """
        If no other minor versions of an environment template exist, delete a major
        version of the environment template if it's not the <code>Recommended</code>
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_environment_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#delete_environment_template_version)
        """

    def delete_repository(
        self, **kwargs: Unpack[DeleteRepositoryInputRequestTypeDef]
    ) -> DeleteRepositoryOutputTypeDef:
        """
        De-register and unlink your repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_repository.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#delete_repository)
        """

    def delete_service(
        self, **kwargs: Unpack[DeleteServiceInputRequestTypeDef]
    ) -> DeleteServiceOutputTypeDef:
        """
        Delete a service, with its instances and pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_service.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#delete_service)
        """

    def delete_service_sync_config(
        self, **kwargs: Unpack[DeleteServiceSyncConfigInputRequestTypeDef]
    ) -> DeleteServiceSyncConfigOutputTypeDef:
        """
        Delete the Proton Ops file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_service_sync_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#delete_service_sync_config)
        """

    def delete_service_template(
        self, **kwargs: Unpack[DeleteServiceTemplateInputRequestTypeDef]
    ) -> DeleteServiceTemplateOutputTypeDef:
        """
        If no other major or minor versions of the service template exist, delete the
        service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_service_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#delete_service_template)
        """

    def delete_service_template_version(
        self, **kwargs: Unpack[DeleteServiceTemplateVersionInputRequestTypeDef]
    ) -> DeleteServiceTemplateVersionOutputTypeDef:
        """
        If no other minor versions of a service template exist, delete a major version
        of the service template if it's not the <code>Recommended</code> version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_service_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#delete_service_template_version)
        """

    def delete_template_sync_config(
        self, **kwargs: Unpack[DeleteTemplateSyncConfigInputRequestTypeDef]
    ) -> DeleteTemplateSyncConfigOutputTypeDef:
        """
        Delete a template sync configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_template_sync_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#delete_template_sync_config)
        """

    def get_account_settings(self) -> GetAccountSettingsOutputTypeDef:
        """
        Get detail data for Proton account-wide settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_account_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_account_settings)
        """

    def get_component(
        self, **kwargs: Unpack[GetComponentInputRequestTypeDef]
    ) -> GetComponentOutputTypeDef:
        """
        Get detailed data for a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_component.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_component)
        """

    def get_deployment(
        self, **kwargs: Unpack[GetDeploymentInputRequestTypeDef]
    ) -> GetDeploymentOutputTypeDef:
        """
        Get detailed data for a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_deployment)
        """

    def get_environment(
        self, **kwargs: Unpack[GetEnvironmentInputRequestTypeDef]
    ) -> GetEnvironmentOutputTypeDef:
        """
        Get detailed data for an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_environment)
        """

    def get_environment_account_connection(
        self, **kwargs: Unpack[GetEnvironmentAccountConnectionInputRequestTypeDef]
    ) -> GetEnvironmentAccountConnectionOutputTypeDef:
        """
        In an environment account, get the detailed data for an environment account
        connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_environment_account_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_environment_account_connection)
        """

    def get_environment_template(
        self, **kwargs: Unpack[GetEnvironmentTemplateInputRequestTypeDef]
    ) -> GetEnvironmentTemplateOutputTypeDef:
        """
        Get detailed data for an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_environment_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_environment_template)
        """

    def get_environment_template_version(
        self, **kwargs: Unpack[GetEnvironmentTemplateVersionInputRequestTypeDef]
    ) -> GetEnvironmentTemplateVersionOutputTypeDef:
        """
        Get detailed data for a major or minor version of an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_environment_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_environment_template_version)
        """

    def get_repository(
        self, **kwargs: Unpack[GetRepositoryInputRequestTypeDef]
    ) -> GetRepositoryOutputTypeDef:
        """
        Get detail data for a linked repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_repository.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_repository)
        """

    def get_repository_sync_status(
        self, **kwargs: Unpack[GetRepositorySyncStatusInputRequestTypeDef]
    ) -> GetRepositorySyncStatusOutputTypeDef:
        """
        Get the sync status of a repository used for Proton template sync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_repository_sync_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_repository_sync_status)
        """

    def get_resources_summary(self) -> GetResourcesSummaryOutputTypeDef:
        """
        Get counts of Proton resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_resources_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_resources_summary)
        """

    def get_service(
        self, **kwargs: Unpack[GetServiceInputRequestTypeDef]
    ) -> GetServiceOutputTypeDef:
        """
        Get detailed data for a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_service)
        """

    def get_service_instance(
        self, **kwargs: Unpack[GetServiceInstanceInputRequestTypeDef]
    ) -> GetServiceInstanceOutputTypeDef:
        """
        Get detailed data for a service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_service_instance)
        """

    def get_service_instance_sync_status(
        self, **kwargs: Unpack[GetServiceInstanceSyncStatusInputRequestTypeDef]
    ) -> GetServiceInstanceSyncStatusOutputTypeDef:
        """
        Get the status of the synced service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service_instance_sync_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_service_instance_sync_status)
        """

    def get_service_sync_blocker_summary(
        self, **kwargs: Unpack[GetServiceSyncBlockerSummaryInputRequestTypeDef]
    ) -> GetServiceSyncBlockerSummaryOutputTypeDef:
        """
        Get detailed data for the service sync blocker summary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service_sync_blocker_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_service_sync_blocker_summary)
        """

    def get_service_sync_config(
        self, **kwargs: Unpack[GetServiceSyncConfigInputRequestTypeDef]
    ) -> GetServiceSyncConfigOutputTypeDef:
        """
        Get detailed information for the service sync configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service_sync_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_service_sync_config)
        """

    def get_service_template(
        self, **kwargs: Unpack[GetServiceTemplateInputRequestTypeDef]
    ) -> GetServiceTemplateOutputTypeDef:
        """
        Get detailed data for a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_service_template)
        """

    def get_service_template_version(
        self, **kwargs: Unpack[GetServiceTemplateVersionInputRequestTypeDef]
    ) -> GetServiceTemplateVersionOutputTypeDef:
        """
        Get detailed data for a major or minor version of a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_service_template_version)
        """

    def get_template_sync_config(
        self, **kwargs: Unpack[GetTemplateSyncConfigInputRequestTypeDef]
    ) -> GetTemplateSyncConfigOutputTypeDef:
        """
        Get detail data for a template sync configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_template_sync_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_template_sync_config)
        """

    def get_template_sync_status(
        self, **kwargs: Unpack[GetTemplateSyncStatusInputRequestTypeDef]
    ) -> GetTemplateSyncStatusOutputTypeDef:
        """
        Get the status of a template sync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_template_sync_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_template_sync_status)
        """

    def list_component_outputs(
        self, **kwargs: Unpack[ListComponentOutputsInputRequestTypeDef]
    ) -> ListComponentOutputsOutputTypeDef:
        """
        Get a list of component Infrastructure as Code (IaC) outputs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_component_outputs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_component_outputs)
        """

    def list_component_provisioned_resources(
        self, **kwargs: Unpack[ListComponentProvisionedResourcesInputRequestTypeDef]
    ) -> ListComponentProvisionedResourcesOutputTypeDef:
        """
        List provisioned resources for a component with details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_component_provisioned_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_component_provisioned_resources)
        """

    def list_components(
        self, **kwargs: Unpack[ListComponentsInputRequestTypeDef]
    ) -> ListComponentsOutputTypeDef:
        """
        List components with summary data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_components.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_components)
        """

    def list_deployments(
        self, **kwargs: Unpack[ListDeploymentsInputRequestTypeDef]
    ) -> ListDeploymentsOutputTypeDef:
        """
        List deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_deployments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_deployments)
        """

    def list_environment_account_connections(
        self, **kwargs: Unpack[ListEnvironmentAccountConnectionsInputRequestTypeDef]
    ) -> ListEnvironmentAccountConnectionsOutputTypeDef:
        """
        View a list of environment account connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_environment_account_connections.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_environment_account_connections)
        """

    def list_environment_outputs(
        self, **kwargs: Unpack[ListEnvironmentOutputsInputRequestTypeDef]
    ) -> ListEnvironmentOutputsOutputTypeDef:
        """
        List the infrastructure as code outputs for your environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_environment_outputs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_environment_outputs)
        """

    def list_environment_provisioned_resources(
        self, **kwargs: Unpack[ListEnvironmentProvisionedResourcesInputRequestTypeDef]
    ) -> ListEnvironmentProvisionedResourcesOutputTypeDef:
        """
        List the provisioned resources for your environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_environment_provisioned_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_environment_provisioned_resources)
        """

    def list_environment_template_versions(
        self, **kwargs: Unpack[ListEnvironmentTemplateVersionsInputRequestTypeDef]
    ) -> ListEnvironmentTemplateVersionsOutputTypeDef:
        """
        List major or minor versions of an environment template with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_environment_template_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_environment_template_versions)
        """

    def list_environment_templates(
        self, **kwargs: Unpack[ListEnvironmentTemplatesInputRequestTypeDef]
    ) -> ListEnvironmentTemplatesOutputTypeDef:
        """
        List environment templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_environment_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_environment_templates)
        """

    def list_environments(
        self, **kwargs: Unpack[ListEnvironmentsInputRequestTypeDef]
    ) -> ListEnvironmentsOutputTypeDef:
        """
        List environments with detail data summaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_environments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_environments)
        """

    def list_repositories(
        self, **kwargs: Unpack[ListRepositoriesInputRequestTypeDef]
    ) -> ListRepositoriesOutputTypeDef:
        """
        List linked repositories with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_repositories.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_repositories)
        """

    def list_repository_sync_definitions(
        self, **kwargs: Unpack[ListRepositorySyncDefinitionsInputRequestTypeDef]
    ) -> ListRepositorySyncDefinitionsOutputTypeDef:
        """
        List repository sync definitions with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_repository_sync_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_repository_sync_definitions)
        """

    def list_service_instance_outputs(
        self, **kwargs: Unpack[ListServiceInstanceOutputsInputRequestTypeDef]
    ) -> ListServiceInstanceOutputsOutputTypeDef:
        """
        Get a list service of instance Infrastructure as Code (IaC) outputs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_instance_outputs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_service_instance_outputs)
        """

    def list_service_instance_provisioned_resources(
        self, **kwargs: Unpack[ListServiceInstanceProvisionedResourcesInputRequestTypeDef]
    ) -> ListServiceInstanceProvisionedResourcesOutputTypeDef:
        """
        List provisioned resources for a service instance with details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_instance_provisioned_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_service_instance_provisioned_resources)
        """

    def list_service_instances(
        self, **kwargs: Unpack[ListServiceInstancesInputRequestTypeDef]
    ) -> ListServiceInstancesOutputTypeDef:
        """
        List service instances with summary data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_service_instances)
        """

    def list_service_pipeline_outputs(
        self, **kwargs: Unpack[ListServicePipelineOutputsInputRequestTypeDef]
    ) -> ListServicePipelineOutputsOutputTypeDef:
        """
        Get a list of service pipeline Infrastructure as Code (IaC) outputs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_pipeline_outputs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_service_pipeline_outputs)
        """

    def list_service_pipeline_provisioned_resources(
        self, **kwargs: Unpack[ListServicePipelineProvisionedResourcesInputRequestTypeDef]
    ) -> ListServicePipelineProvisionedResourcesOutputTypeDef:
        """
        List provisioned resources for a service and pipeline with details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_pipeline_provisioned_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_service_pipeline_provisioned_resources)
        """

    def list_service_template_versions(
        self, **kwargs: Unpack[ListServiceTemplateVersionsInputRequestTypeDef]
    ) -> ListServiceTemplateVersionsOutputTypeDef:
        """
        List major or minor versions of a service template with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_template_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_service_template_versions)
        """

    def list_service_templates(
        self, **kwargs: Unpack[ListServiceTemplatesInputRequestTypeDef]
    ) -> ListServiceTemplatesOutputTypeDef:
        """
        List service templates with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_service_templates)
        """

    def list_services(
        self, **kwargs: Unpack[ListServicesInputRequestTypeDef]
    ) -> ListServicesOutputTypeDef:
        """
        List services with summaries of detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_services.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_services)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        List tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#list_tags_for_resource)
        """

    def notify_resource_deployment_status_change(
        self, **kwargs: Unpack[NotifyResourceDeploymentStatusChangeInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Notify Proton of status changes to a provisioned resource when you use
        self-managed provisioning.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/notify_resource_deployment_status_change.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#notify_resource_deployment_status_change)
        """

    def reject_environment_account_connection(
        self, **kwargs: Unpack[RejectEnvironmentAccountConnectionInputRequestTypeDef]
    ) -> RejectEnvironmentAccountConnectionOutputTypeDef:
        """
        In a management account, reject an environment account connection from another
        environment account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/reject_environment_account_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#reject_environment_account_connection)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Tag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Remove a customer tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#untag_resource)
        """

    def update_account_settings(
        self, **kwargs: Unpack[UpdateAccountSettingsInputRequestTypeDef]
    ) -> UpdateAccountSettingsOutputTypeDef:
        """
        Update Proton settings that are used for multiple services in the Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_account_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_account_settings)
        """

    def update_component(
        self, **kwargs: Unpack[UpdateComponentInputRequestTypeDef]
    ) -> UpdateComponentOutputTypeDef:
        """
        Update a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_component.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_component)
        """

    def update_environment(
        self, **kwargs: Unpack[UpdateEnvironmentInputRequestTypeDef]
    ) -> UpdateEnvironmentOutputTypeDef:
        """
        Update an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_environment)
        """

    def update_environment_account_connection(
        self, **kwargs: Unpack[UpdateEnvironmentAccountConnectionInputRequestTypeDef]
    ) -> UpdateEnvironmentAccountConnectionOutputTypeDef:
        """
        In an environment account, update an environment account connection to use a
        new IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_environment_account_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_environment_account_connection)
        """

    def update_environment_template(
        self, **kwargs: Unpack[UpdateEnvironmentTemplateInputRequestTypeDef]
    ) -> UpdateEnvironmentTemplateOutputTypeDef:
        """
        Update an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_environment_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_environment_template)
        """

    def update_environment_template_version(
        self, **kwargs: Unpack[UpdateEnvironmentTemplateVersionInputRequestTypeDef]
    ) -> UpdateEnvironmentTemplateVersionOutputTypeDef:
        """
        Update a major or minor version of an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_environment_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_environment_template_version)
        """

    def update_service(
        self, **kwargs: Unpack[UpdateServiceInputRequestTypeDef]
    ) -> UpdateServiceOutputTypeDef:
        """
        Edit a service description or use a spec to add and delete service instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_service)
        """

    def update_service_instance(
        self, **kwargs: Unpack[UpdateServiceInstanceInputRequestTypeDef]
    ) -> UpdateServiceInstanceOutputTypeDef:
        """
        Update a service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_service_instance)
        """

    def update_service_pipeline(
        self, **kwargs: Unpack[UpdateServicePipelineInputRequestTypeDef]
    ) -> UpdateServicePipelineOutputTypeDef:
        """
        Update the service pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service_pipeline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_service_pipeline)
        """

    def update_service_sync_blocker(
        self, **kwargs: Unpack[UpdateServiceSyncBlockerInputRequestTypeDef]
    ) -> UpdateServiceSyncBlockerOutputTypeDef:
        """
        Update the service sync blocker by resolving it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service_sync_blocker.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_service_sync_blocker)
        """

    def update_service_sync_config(
        self, **kwargs: Unpack[UpdateServiceSyncConfigInputRequestTypeDef]
    ) -> UpdateServiceSyncConfigOutputTypeDef:
        """
        Update the Proton Ops config file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service_sync_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_service_sync_config)
        """

    def update_service_template(
        self, **kwargs: Unpack[UpdateServiceTemplateInputRequestTypeDef]
    ) -> UpdateServiceTemplateOutputTypeDef:
        """
        Update a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_service_template)
        """

    def update_service_template_version(
        self, **kwargs: Unpack[UpdateServiceTemplateVersionInputRequestTypeDef]
    ) -> UpdateServiceTemplateVersionOutputTypeDef:
        """
        Update a major or minor version of a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_service_template_version)
        """

    def update_template_sync_config(
        self, **kwargs: Unpack[UpdateTemplateSyncConfigInputRequestTypeDef]
    ) -> UpdateTemplateSyncConfigOutputTypeDef:
        """
        Update template sync configuration parameters, except for the
        <code>templateName</code> and <code>templateType</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_template_sync_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#update_template_sync_config)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_component_outputs"]
    ) -> ListComponentOutputsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_component_provisioned_resources"]
    ) -> ListComponentProvisionedResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_components"]) -> ListComponentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployments"]
    ) -> ListDeploymentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_account_connections"]
    ) -> ListEnvironmentAccountConnectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_outputs"]
    ) -> ListEnvironmentOutputsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_provisioned_resources"]
    ) -> ListEnvironmentProvisionedResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_template_versions"]
    ) -> ListEnvironmentTemplateVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_templates"]
    ) -> ListEnvironmentTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repositories"]
    ) -> ListRepositoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repository_sync_definitions"]
    ) -> ListRepositorySyncDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_instance_outputs"]
    ) -> ListServiceInstanceOutputsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_instance_provisioned_resources"]
    ) -> ListServiceInstanceProvisionedResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_instances"]
    ) -> ListServiceInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_pipeline_outputs"]
    ) -> ListServicePipelineOutputsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_pipeline_provisioned_resources"]
    ) -> ListServicePipelineProvisionedResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_template_versions"]
    ) -> ListServiceTemplateVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_templates"]
    ) -> ListServiceTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_services"]) -> ListServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["component_deleted"]) -> ComponentDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["component_deployed"]) -> ComponentDeployedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["environment_deployed"]) -> EnvironmentDeployedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["environment_template_version_registered"]
    ) -> EnvironmentTemplateVersionRegisteredWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["service_created"]) -> ServiceCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["service_deleted"]) -> ServiceDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["service_instance_deployed"]
    ) -> ServiceInstanceDeployedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["service_pipeline_deployed"]
    ) -> ServicePipelineDeployedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["service_template_version_registered"]
    ) -> ServiceTemplateVersionRegisteredWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["service_updated"]) -> ServiceUpdatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_proton/client/#get_waiter)
        """
