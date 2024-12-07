"""
Type annotations for license-manager service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_license_manager.client import LicenseManagerClient

    session = Session()
    client: LicenseManagerClient = session.client("license-manager")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAssociationsForLicenseConfigurationPaginator,
    ListLicenseConfigurationsPaginator,
    ListLicenseSpecificationsForResourcePaginator,
    ListResourceInventoryPaginator,
    ListUsageForLicenseConfigurationPaginator,
)
from .type_defs import (
    AcceptGrantRequestRequestTypeDef,
    AcceptGrantResponseTypeDef,
    CheckInLicenseRequestRequestTypeDef,
    CheckoutBorrowLicenseRequestRequestTypeDef,
    CheckoutBorrowLicenseResponseTypeDef,
    CheckoutLicenseRequestRequestTypeDef,
    CheckoutLicenseResponseTypeDef,
    CreateGrantRequestRequestTypeDef,
    CreateGrantResponseTypeDef,
    CreateGrantVersionRequestRequestTypeDef,
    CreateGrantVersionResponseTypeDef,
    CreateLicenseConfigurationRequestRequestTypeDef,
    CreateLicenseConfigurationResponseTypeDef,
    CreateLicenseConversionTaskForResourceRequestRequestTypeDef,
    CreateLicenseConversionTaskForResourceResponseTypeDef,
    CreateLicenseManagerReportGeneratorRequestRequestTypeDef,
    CreateLicenseManagerReportGeneratorResponseTypeDef,
    CreateLicenseRequestRequestTypeDef,
    CreateLicenseResponseTypeDef,
    CreateLicenseVersionRequestRequestTypeDef,
    CreateLicenseVersionResponseTypeDef,
    CreateTokenRequestRequestTypeDef,
    CreateTokenResponseTypeDef,
    DeleteGrantRequestRequestTypeDef,
    DeleteGrantResponseTypeDef,
    DeleteLicenseConfigurationRequestRequestTypeDef,
    DeleteLicenseManagerReportGeneratorRequestRequestTypeDef,
    DeleteLicenseRequestRequestTypeDef,
    DeleteLicenseResponseTypeDef,
    DeleteTokenRequestRequestTypeDef,
    ExtendLicenseConsumptionRequestRequestTypeDef,
    ExtendLicenseConsumptionResponseTypeDef,
    GetAccessTokenRequestRequestTypeDef,
    GetAccessTokenResponseTypeDef,
    GetGrantRequestRequestTypeDef,
    GetGrantResponseTypeDef,
    GetLicenseConfigurationRequestRequestTypeDef,
    GetLicenseConfigurationResponseTypeDef,
    GetLicenseConversionTaskRequestRequestTypeDef,
    GetLicenseConversionTaskResponseTypeDef,
    GetLicenseManagerReportGeneratorRequestRequestTypeDef,
    GetLicenseManagerReportGeneratorResponseTypeDef,
    GetLicenseRequestRequestTypeDef,
    GetLicenseResponseTypeDef,
    GetLicenseUsageRequestRequestTypeDef,
    GetLicenseUsageResponseTypeDef,
    GetServiceSettingsResponseTypeDef,
    ListAssociationsForLicenseConfigurationRequestRequestTypeDef,
    ListAssociationsForLicenseConfigurationResponseTypeDef,
    ListDistributedGrantsRequestRequestTypeDef,
    ListDistributedGrantsResponseTypeDef,
    ListFailuresForLicenseConfigurationOperationsRequestRequestTypeDef,
    ListFailuresForLicenseConfigurationOperationsResponseTypeDef,
    ListLicenseConfigurationsRequestRequestTypeDef,
    ListLicenseConfigurationsResponseTypeDef,
    ListLicenseConversionTasksRequestRequestTypeDef,
    ListLicenseConversionTasksResponseTypeDef,
    ListLicenseManagerReportGeneratorsRequestRequestTypeDef,
    ListLicenseManagerReportGeneratorsResponseTypeDef,
    ListLicenseSpecificationsForResourceRequestRequestTypeDef,
    ListLicenseSpecificationsForResourceResponseTypeDef,
    ListLicensesRequestRequestTypeDef,
    ListLicensesResponseTypeDef,
    ListLicenseVersionsRequestRequestTypeDef,
    ListLicenseVersionsResponseTypeDef,
    ListReceivedGrantsForOrganizationRequestRequestTypeDef,
    ListReceivedGrantsForOrganizationResponseTypeDef,
    ListReceivedGrantsRequestRequestTypeDef,
    ListReceivedGrantsResponseTypeDef,
    ListReceivedLicensesForOrganizationRequestRequestTypeDef,
    ListReceivedLicensesForOrganizationResponseTypeDef,
    ListReceivedLicensesRequestRequestTypeDef,
    ListReceivedLicensesResponseTypeDef,
    ListResourceInventoryRequestRequestTypeDef,
    ListResourceInventoryResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTokensRequestRequestTypeDef,
    ListTokensResponseTypeDef,
    ListUsageForLicenseConfigurationRequestRequestTypeDef,
    ListUsageForLicenseConfigurationResponseTypeDef,
    RejectGrantRequestRequestTypeDef,
    RejectGrantResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateLicenseConfigurationRequestRequestTypeDef,
    UpdateLicenseManagerReportGeneratorRequestRequestTypeDef,
    UpdateLicenseSpecificationsForResourceRequestRequestTypeDef,
    UpdateServiceSettingsRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("LicenseManagerClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AuthorizationException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    EntitlementNotAllowedException: Type[BotocoreClientError]
    FailedDependencyException: Type[BotocoreClientError]
    FilterLimitExceededException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidResourceStateException: Type[BotocoreClientError]
    LicenseUsageException: Type[BotocoreClientError]
    NoEntitlementsAllowedException: Type[BotocoreClientError]
    RateLimitExceededException: Type[BotocoreClientError]
    RedirectException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServerInternalException: Type[BotocoreClientError]
    UnsupportedDigitalSignatureMethodException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class LicenseManagerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LicenseManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#close)
        """

    def accept_grant(
        self, **kwargs: Unpack[AcceptGrantRequestRequestTypeDef]
    ) -> AcceptGrantResponseTypeDef:
        """
        Accepts the specified grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/accept_grant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#accept_grant)
        """

    def check_in_license(
        self, **kwargs: Unpack[CheckInLicenseRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Checks in the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/check_in_license.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#check_in_license)
        """

    def checkout_borrow_license(
        self, **kwargs: Unpack[CheckoutBorrowLicenseRequestRequestTypeDef]
    ) -> CheckoutBorrowLicenseResponseTypeDef:
        """
        Checks out the specified license for offline use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/checkout_borrow_license.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#checkout_borrow_license)
        """

    def checkout_license(
        self, **kwargs: Unpack[CheckoutLicenseRequestRequestTypeDef]
    ) -> CheckoutLicenseResponseTypeDef:
        """
        Checks out the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/checkout_license.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#checkout_license)
        """

    def create_grant(
        self, **kwargs: Unpack[CreateGrantRequestRequestTypeDef]
    ) -> CreateGrantResponseTypeDef:
        """
        Creates a grant for the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/create_grant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#create_grant)
        """

    def create_grant_version(
        self, **kwargs: Unpack[CreateGrantVersionRequestRequestTypeDef]
    ) -> CreateGrantVersionResponseTypeDef:
        """
        Creates a new version of the specified grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/create_grant_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#create_grant_version)
        """

    def create_license(
        self, **kwargs: Unpack[CreateLicenseRequestRequestTypeDef]
    ) -> CreateLicenseResponseTypeDef:
        """
        Creates a license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/create_license.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#create_license)
        """

    def create_license_configuration(
        self, **kwargs: Unpack[CreateLicenseConfigurationRequestRequestTypeDef]
    ) -> CreateLicenseConfigurationResponseTypeDef:
        """
        Creates a license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/create_license_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#create_license_configuration)
        """

    def create_license_conversion_task_for_resource(
        self, **kwargs: Unpack[CreateLicenseConversionTaskForResourceRequestRequestTypeDef]
    ) -> CreateLicenseConversionTaskForResourceResponseTypeDef:
        """
        Creates a new license conversion task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/create_license_conversion_task_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#create_license_conversion_task_for_resource)
        """

    def create_license_manager_report_generator(
        self, **kwargs: Unpack[CreateLicenseManagerReportGeneratorRequestRequestTypeDef]
    ) -> CreateLicenseManagerReportGeneratorResponseTypeDef:
        """
        Creates a report generator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/create_license_manager_report_generator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#create_license_manager_report_generator)
        """

    def create_license_version(
        self, **kwargs: Unpack[CreateLicenseVersionRequestRequestTypeDef]
    ) -> CreateLicenseVersionResponseTypeDef:
        """
        Creates a new version of the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/create_license_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#create_license_version)
        """

    def create_token(
        self, **kwargs: Unpack[CreateTokenRequestRequestTypeDef]
    ) -> CreateTokenResponseTypeDef:
        """
        Creates a long-lived token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/create_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#create_token)
        """

    def delete_grant(
        self, **kwargs: Unpack[DeleteGrantRequestRequestTypeDef]
    ) -> DeleteGrantResponseTypeDef:
        """
        Deletes the specified grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/delete_grant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#delete_grant)
        """

    def delete_license(
        self, **kwargs: Unpack[DeleteLicenseRequestRequestTypeDef]
    ) -> DeleteLicenseResponseTypeDef:
        """
        Deletes the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/delete_license.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#delete_license)
        """

    def delete_license_configuration(
        self, **kwargs: Unpack[DeleteLicenseConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/delete_license_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#delete_license_configuration)
        """

    def delete_license_manager_report_generator(
        self, **kwargs: Unpack[DeleteLicenseManagerReportGeneratorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified report generator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/delete_license_manager_report_generator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#delete_license_manager_report_generator)
        """

    def delete_token(self, **kwargs: Unpack[DeleteTokenRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/delete_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#delete_token)
        """

    def extend_license_consumption(
        self, **kwargs: Unpack[ExtendLicenseConsumptionRequestRequestTypeDef]
    ) -> ExtendLicenseConsumptionResponseTypeDef:
        """
        Extends the expiration date for license consumption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/extend_license_consumption.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#extend_license_consumption)
        """

    def get_access_token(
        self, **kwargs: Unpack[GetAccessTokenRequestRequestTypeDef]
    ) -> GetAccessTokenResponseTypeDef:
        """
        Gets a temporary access token to use with AssumeRoleWithWebIdentity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/get_access_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#get_access_token)
        """

    def get_grant(self, **kwargs: Unpack[GetGrantRequestRequestTypeDef]) -> GetGrantResponseTypeDef:
        """
        Gets detailed information about the specified grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/get_grant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#get_grant)
        """

    def get_license(
        self, **kwargs: Unpack[GetLicenseRequestRequestTypeDef]
    ) -> GetLicenseResponseTypeDef:
        """
        Gets detailed information about the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/get_license.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#get_license)
        """

    def get_license_configuration(
        self, **kwargs: Unpack[GetLicenseConfigurationRequestRequestTypeDef]
    ) -> GetLicenseConfigurationResponseTypeDef:
        """
        Gets detailed information about the specified license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/get_license_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#get_license_configuration)
        """

    def get_license_conversion_task(
        self, **kwargs: Unpack[GetLicenseConversionTaskRequestRequestTypeDef]
    ) -> GetLicenseConversionTaskResponseTypeDef:
        """
        Gets information about the specified license type conversion task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/get_license_conversion_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#get_license_conversion_task)
        """

    def get_license_manager_report_generator(
        self, **kwargs: Unpack[GetLicenseManagerReportGeneratorRequestRequestTypeDef]
    ) -> GetLicenseManagerReportGeneratorResponseTypeDef:
        """
        Gets information about the specified report generator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/get_license_manager_report_generator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#get_license_manager_report_generator)
        """

    def get_license_usage(
        self, **kwargs: Unpack[GetLicenseUsageRequestRequestTypeDef]
    ) -> GetLicenseUsageResponseTypeDef:
        """
        Gets detailed information about the usage of the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/get_license_usage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#get_license_usage)
        """

    def get_service_settings(self) -> GetServiceSettingsResponseTypeDef:
        """
        Gets the License Manager settings for the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/get_service_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#get_service_settings)
        """

    def list_associations_for_license_configuration(
        self, **kwargs: Unpack[ListAssociationsForLicenseConfigurationRequestRequestTypeDef]
    ) -> ListAssociationsForLicenseConfigurationResponseTypeDef:
        """
        Lists the resource associations for the specified license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_associations_for_license_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_associations_for_license_configuration)
        """

    def list_distributed_grants(
        self, **kwargs: Unpack[ListDistributedGrantsRequestRequestTypeDef]
    ) -> ListDistributedGrantsResponseTypeDef:
        """
        Lists the grants distributed for the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_distributed_grants.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_distributed_grants)
        """

    def list_failures_for_license_configuration_operations(
        self, **kwargs: Unpack[ListFailuresForLicenseConfigurationOperationsRequestRequestTypeDef]
    ) -> ListFailuresForLicenseConfigurationOperationsResponseTypeDef:
        """
        Lists the license configuration operations that failed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_failures_for_license_configuration_operations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_failures_for_license_configuration_operations)
        """

    def list_license_configurations(
        self, **kwargs: Unpack[ListLicenseConfigurationsRequestRequestTypeDef]
    ) -> ListLicenseConfigurationsResponseTypeDef:
        """
        Lists the license configurations for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_license_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_license_configurations)
        """

    def list_license_conversion_tasks(
        self, **kwargs: Unpack[ListLicenseConversionTasksRequestRequestTypeDef]
    ) -> ListLicenseConversionTasksResponseTypeDef:
        """
        Lists the license type conversion tasks for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_license_conversion_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_license_conversion_tasks)
        """

    def list_license_manager_report_generators(
        self, **kwargs: Unpack[ListLicenseManagerReportGeneratorsRequestRequestTypeDef]
    ) -> ListLicenseManagerReportGeneratorsResponseTypeDef:
        """
        Lists the report generators for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_license_manager_report_generators.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_license_manager_report_generators)
        """

    def list_license_specifications_for_resource(
        self, **kwargs: Unpack[ListLicenseSpecificationsForResourceRequestRequestTypeDef]
    ) -> ListLicenseSpecificationsForResourceResponseTypeDef:
        """
        Describes the license configurations for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_license_specifications_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_license_specifications_for_resource)
        """

    def list_license_versions(
        self, **kwargs: Unpack[ListLicenseVersionsRequestRequestTypeDef]
    ) -> ListLicenseVersionsResponseTypeDef:
        """
        Lists all versions of the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_license_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_license_versions)
        """

    def list_licenses(
        self, **kwargs: Unpack[ListLicensesRequestRequestTypeDef]
    ) -> ListLicensesResponseTypeDef:
        """
        Lists the licenses for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_licenses.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_licenses)
        """

    def list_received_grants(
        self, **kwargs: Unpack[ListReceivedGrantsRequestRequestTypeDef]
    ) -> ListReceivedGrantsResponseTypeDef:
        """
        Lists grants that are received.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_received_grants.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_received_grants)
        """

    def list_received_grants_for_organization(
        self, **kwargs: Unpack[ListReceivedGrantsForOrganizationRequestRequestTypeDef]
    ) -> ListReceivedGrantsForOrganizationResponseTypeDef:
        """
        Lists the grants received for all accounts in the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_received_grants_for_organization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_received_grants_for_organization)
        """

    def list_received_licenses(
        self, **kwargs: Unpack[ListReceivedLicensesRequestRequestTypeDef]
    ) -> ListReceivedLicensesResponseTypeDef:
        """
        Lists received licenses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_received_licenses.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_received_licenses)
        """

    def list_received_licenses_for_organization(
        self, **kwargs: Unpack[ListReceivedLicensesForOrganizationRequestRequestTypeDef]
    ) -> ListReceivedLicensesForOrganizationResponseTypeDef:
        """
        Lists the licenses received for all accounts in the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_received_licenses_for_organization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_received_licenses_for_organization)
        """

    def list_resource_inventory(
        self, **kwargs: Unpack[ListResourceInventoryRequestRequestTypeDef]
    ) -> ListResourceInventoryResponseTypeDef:
        """
        Lists resources managed using Systems Manager inventory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_resource_inventory.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_resource_inventory)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_tags_for_resource)
        """

    def list_tokens(
        self, **kwargs: Unpack[ListTokensRequestRequestTypeDef]
    ) -> ListTokensResponseTypeDef:
        """
        Lists your tokens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_tokens.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_tokens)
        """

    def list_usage_for_license_configuration(
        self, **kwargs: Unpack[ListUsageForLicenseConfigurationRequestRequestTypeDef]
    ) -> ListUsageForLicenseConfigurationResponseTypeDef:
        """
        Lists all license usage records for a license configuration, displaying license
        consumption details by resource at a selected point in time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/list_usage_for_license_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#list_usage_for_license_configuration)
        """

    def reject_grant(
        self, **kwargs: Unpack[RejectGrantRequestRequestTypeDef]
    ) -> RejectGrantResponseTypeDef:
        """
        Rejects the specified grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/reject_grant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#reject_grant)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#untag_resource)
        """

    def update_license_configuration(
        self, **kwargs: Unpack[UpdateLicenseConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies the attributes of an existing license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/update_license_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#update_license_configuration)
        """

    def update_license_manager_report_generator(
        self, **kwargs: Unpack[UpdateLicenseManagerReportGeneratorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a report generator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/update_license_manager_report_generator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#update_license_manager_report_generator)
        """

    def update_license_specifications_for_resource(
        self, **kwargs: Unpack[UpdateLicenseSpecificationsForResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds or removes the specified license configurations for the specified Amazon
        Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/update_license_specifications_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#update_license_specifications_for_resource)
        """

    def update_service_settings(
        self, **kwargs: Unpack[UpdateServiceSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates License Manager settings for the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/update_service_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#update_service_settings)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_associations_for_license_configuration"]
    ) -> ListAssociationsForLicenseConfigurationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_license_configurations"]
    ) -> ListLicenseConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_license_specifications_for_resource"]
    ) -> ListLicenseSpecificationsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_inventory"]
    ) -> ListResourceInventoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_usage_for_license_configuration"]
    ) -> ListUsageForLicenseConfigurationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager/client/#get_paginator)
        """
