"""
Type annotations for elasticbeanstalk service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_elasticbeanstalk.client import ElasticBeanstalkClient

    session = Session()
    client: ElasticBeanstalkClient = session.client("elasticbeanstalk")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeApplicationVersionsPaginator,
    DescribeEnvironmentManagedActionHistoryPaginator,
    DescribeEnvironmentsPaginator,
    DescribeEventsPaginator,
    ListPlatformVersionsPaginator,
)
from .type_defs import (
    AbortEnvironmentUpdateMessageRequestTypeDef,
    ApplicationDescriptionMessageTypeDef,
    ApplicationDescriptionsMessageTypeDef,
    ApplicationResourceLifecycleDescriptionMessageTypeDef,
    ApplicationVersionDescriptionMessageTypeDef,
    ApplicationVersionDescriptionsMessageTypeDef,
    ApplyEnvironmentManagedActionRequestRequestTypeDef,
    ApplyEnvironmentManagedActionResultTypeDef,
    AssociateEnvironmentOperationsRoleMessageRequestTypeDef,
    CheckDNSAvailabilityMessageRequestTypeDef,
    CheckDNSAvailabilityResultMessageTypeDef,
    ComposeEnvironmentsMessageRequestTypeDef,
    ConfigurationOptionsDescriptionTypeDef,
    ConfigurationSettingsDescriptionResponseTypeDef,
    ConfigurationSettingsDescriptionsTypeDef,
    ConfigurationSettingsValidationMessagesTypeDef,
    CreateApplicationMessageRequestTypeDef,
    CreateApplicationVersionMessageRequestTypeDef,
    CreateConfigurationTemplateMessageRequestTypeDef,
    CreateEnvironmentMessageRequestTypeDef,
    CreatePlatformVersionRequestRequestTypeDef,
    CreatePlatformVersionResultTypeDef,
    CreateStorageLocationResultMessageTypeDef,
    DeleteApplicationMessageRequestTypeDef,
    DeleteApplicationVersionMessageRequestTypeDef,
    DeleteConfigurationTemplateMessageRequestTypeDef,
    DeleteEnvironmentConfigurationMessageRequestTypeDef,
    DeletePlatformVersionRequestRequestTypeDef,
    DeletePlatformVersionResultTypeDef,
    DescribeAccountAttributesResultTypeDef,
    DescribeApplicationsMessageRequestTypeDef,
    DescribeApplicationVersionsMessageRequestTypeDef,
    DescribeConfigurationOptionsMessageRequestTypeDef,
    DescribeConfigurationSettingsMessageRequestTypeDef,
    DescribeEnvironmentHealthRequestRequestTypeDef,
    DescribeEnvironmentHealthResultTypeDef,
    DescribeEnvironmentManagedActionHistoryRequestRequestTypeDef,
    DescribeEnvironmentManagedActionHistoryResultTypeDef,
    DescribeEnvironmentManagedActionsRequestRequestTypeDef,
    DescribeEnvironmentManagedActionsResultTypeDef,
    DescribeEnvironmentResourcesMessageRequestTypeDef,
    DescribeEnvironmentsMessageRequestTypeDef,
    DescribeEventsMessageRequestTypeDef,
    DescribeInstancesHealthRequestRequestTypeDef,
    DescribeInstancesHealthResultTypeDef,
    DescribePlatformVersionRequestRequestTypeDef,
    DescribePlatformVersionResultTypeDef,
    DisassociateEnvironmentOperationsRoleMessageRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EnvironmentDescriptionResponseTypeDef,
    EnvironmentDescriptionsMessageTypeDef,
    EnvironmentResourceDescriptionsMessageTypeDef,
    EventDescriptionsMessageTypeDef,
    ListAvailableSolutionStacksResultMessageTypeDef,
    ListPlatformBranchesRequestRequestTypeDef,
    ListPlatformBranchesResultTypeDef,
    ListPlatformVersionsRequestRequestTypeDef,
    ListPlatformVersionsResultTypeDef,
    ListTagsForResourceMessageRequestTypeDef,
    RebuildEnvironmentMessageRequestTypeDef,
    RequestEnvironmentInfoMessageRequestTypeDef,
    ResourceTagsDescriptionMessageTypeDef,
    RestartAppServerMessageRequestTypeDef,
    RetrieveEnvironmentInfoMessageRequestTypeDef,
    RetrieveEnvironmentInfoResultMessageTypeDef,
    SwapEnvironmentCNAMEsMessageRequestTypeDef,
    TerminateEnvironmentMessageRequestTypeDef,
    UpdateApplicationMessageRequestTypeDef,
    UpdateApplicationResourceLifecycleMessageRequestTypeDef,
    UpdateApplicationVersionMessageRequestTypeDef,
    UpdateConfigurationTemplateMessageRequestTypeDef,
    UpdateEnvironmentMessageRequestTypeDef,
    UpdateTagsForResourceMessageRequestTypeDef,
    ValidateConfigurationSettingsMessageRequestTypeDef,
)
from .waiter import EnvironmentExistsWaiter, EnvironmentTerminatedWaiter, EnvironmentUpdatedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ElasticBeanstalkClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    CodeBuildNotInServiceRegionException: Type[BotocoreClientError]
    ElasticBeanstalkServiceException: Type[BotocoreClientError]
    InsufficientPrivilegesException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ManagedActionInvalidStateException: Type[BotocoreClientError]
    OperationInProgressException: Type[BotocoreClientError]
    PlatformVersionStillReferencedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceTypeNotSupportedException: Type[BotocoreClientError]
    S3LocationNotInServiceRegionException: Type[BotocoreClientError]
    S3SubscriptionRequiredException: Type[BotocoreClientError]
    SourceBundleDeletionException: Type[BotocoreClientError]
    TooManyApplicationVersionsException: Type[BotocoreClientError]
    TooManyApplicationsException: Type[BotocoreClientError]
    TooManyBucketsException: Type[BotocoreClientError]
    TooManyConfigurationTemplatesException: Type[BotocoreClientError]
    TooManyEnvironmentsException: Type[BotocoreClientError]
    TooManyPlatformsException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class ElasticBeanstalkClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticBeanstalkClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#close)
        """

    def abort_environment_update(
        self, **kwargs: Unpack[AbortEnvironmentUpdateMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels in-progress environment configuration update or application version
        deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/abort_environment_update.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#abort_environment_update)
        """

    def apply_environment_managed_action(
        self, **kwargs: Unpack[ApplyEnvironmentManagedActionRequestRequestTypeDef]
    ) -> ApplyEnvironmentManagedActionResultTypeDef:
        """
        Applies a scheduled managed action immediately.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/apply_environment_managed_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#apply_environment_managed_action)
        """

    def associate_environment_operations_role(
        self, **kwargs: Unpack[AssociateEnvironmentOperationsRoleMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Add or change the operations role used by an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/associate_environment_operations_role.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#associate_environment_operations_role)
        """

    def check_dns_availability(
        self, **kwargs: Unpack[CheckDNSAvailabilityMessageRequestTypeDef]
    ) -> CheckDNSAvailabilityResultMessageTypeDef:
        """
        Checks if the specified CNAME is available.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/check_dns_availability.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#check_dns_availability)
        """

    def compose_environments(
        self, **kwargs: Unpack[ComposeEnvironmentsMessageRequestTypeDef]
    ) -> EnvironmentDescriptionsMessageTypeDef:
        """
        Create or update a group of environments that each run a separate component of
        a single application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/compose_environments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#compose_environments)
        """

    def create_application(
        self, **kwargs: Unpack[CreateApplicationMessageRequestTypeDef]
    ) -> ApplicationDescriptionMessageTypeDef:
        """
        Creates an application that has one configuration template named
        <code>default</code> and no application versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/create_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#create_application)
        """

    def create_application_version(
        self, **kwargs: Unpack[CreateApplicationVersionMessageRequestTypeDef]
    ) -> ApplicationVersionDescriptionMessageTypeDef:
        """
        Creates an application version for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/create_application_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#create_application_version)
        """

    def create_configuration_template(
        self, **kwargs: Unpack[CreateConfigurationTemplateMessageRequestTypeDef]
    ) -> ConfigurationSettingsDescriptionResponseTypeDef:
        """
        Creates an AWS Elastic Beanstalk configuration template, associated with a
        specific Elastic Beanstalk application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/create_configuration_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#create_configuration_template)
        """

    def create_environment(
        self, **kwargs: Unpack[CreateEnvironmentMessageRequestTypeDef]
    ) -> EnvironmentDescriptionResponseTypeDef:
        """
        Launches an AWS Elastic Beanstalk environment for the specified application
        using the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/create_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#create_environment)
        """

    def create_platform_version(
        self, **kwargs: Unpack[CreatePlatformVersionRequestRequestTypeDef]
    ) -> CreatePlatformVersionResultTypeDef:
        """
        Create a new version of your custom platform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/create_platform_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#create_platform_version)
        """

    def create_storage_location(self) -> CreateStorageLocationResultMessageTypeDef:
        """
        Creates a bucket in Amazon S3 to store application versions, logs, and other
        files used by Elastic Beanstalk environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/create_storage_location.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#create_storage_location)
        """

    def delete_application(
        self, **kwargs: Unpack[DeleteApplicationMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified application along with all associated versions and
        configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/delete_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#delete_application)
        """

    def delete_application_version(
        self, **kwargs: Unpack[DeleteApplicationVersionMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified version from the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/delete_application_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#delete_application_version)
        """

    def delete_configuration_template(
        self, **kwargs: Unpack[DeleteConfigurationTemplateMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified configuration template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/delete_configuration_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#delete_configuration_template)
        """

    def delete_environment_configuration(
        self, **kwargs: Unpack[DeleteEnvironmentConfigurationMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the draft configuration associated with the running environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/delete_environment_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#delete_environment_configuration)
        """

    def delete_platform_version(
        self, **kwargs: Unpack[DeletePlatformVersionRequestRequestTypeDef]
    ) -> DeletePlatformVersionResultTypeDef:
        """
        Deletes the specified version of a custom platform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/delete_platform_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#delete_platform_version)
        """

    def describe_account_attributes(self) -> DescribeAccountAttributesResultTypeDef:
        """
        Returns attributes related to AWS Elastic Beanstalk that are associated with
        the calling AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/describe_account_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#describe_account_attributes)
        """

    def describe_application_versions(
        self, **kwargs: Unpack[DescribeApplicationVersionsMessageRequestTypeDef]
    ) -> ApplicationVersionDescriptionsMessageTypeDef:
        """
        Retrieve a list of application versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/describe_application_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#describe_application_versions)
        """

    def describe_applications(
        self, **kwargs: Unpack[DescribeApplicationsMessageRequestTypeDef]
    ) -> ApplicationDescriptionsMessageTypeDef:
        """
        Returns the descriptions of existing applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/describe_applications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#describe_applications)
        """

    def describe_configuration_options(
        self, **kwargs: Unpack[DescribeConfigurationOptionsMessageRequestTypeDef]
    ) -> ConfigurationOptionsDescriptionTypeDef:
        """
        Describes the configuration options that are used in a particular configuration
        template or environment, or that a specified solution stack defines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/describe_configuration_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#describe_configuration_options)
        """

    def describe_configuration_settings(
        self, **kwargs: Unpack[DescribeConfigurationSettingsMessageRequestTypeDef]
    ) -> ConfigurationSettingsDescriptionsTypeDef:
        """
        Returns a description of the settings for the specified configuration set, that
        is, either a configuration template or the configuration set associated with a
        running environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/describe_configuration_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#describe_configuration_settings)
        """

    def describe_environment_health(
        self, **kwargs: Unpack[DescribeEnvironmentHealthRequestRequestTypeDef]
    ) -> DescribeEnvironmentHealthResultTypeDef:
        """
        Returns information about the overall health of the specified environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/describe_environment_health.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#describe_environment_health)
        """

    def describe_environment_managed_action_history(
        self, **kwargs: Unpack[DescribeEnvironmentManagedActionHistoryRequestRequestTypeDef]
    ) -> DescribeEnvironmentManagedActionHistoryResultTypeDef:
        """
        Lists an environment's completed and failed managed actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/describe_environment_managed_action_history.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#describe_environment_managed_action_history)
        """

    def describe_environment_managed_actions(
        self, **kwargs: Unpack[DescribeEnvironmentManagedActionsRequestRequestTypeDef]
    ) -> DescribeEnvironmentManagedActionsResultTypeDef:
        """
        Lists an environment's upcoming and in-progress managed actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/describe_environment_managed_actions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#describe_environment_managed_actions)
        """

    def describe_environment_resources(
        self, **kwargs: Unpack[DescribeEnvironmentResourcesMessageRequestTypeDef]
    ) -> EnvironmentResourceDescriptionsMessageTypeDef:
        """
        Returns AWS resources for this environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/describe_environment_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#describe_environment_resources)
        """

    def describe_environments(
        self, **kwargs: Unpack[DescribeEnvironmentsMessageRequestTypeDef]
    ) -> EnvironmentDescriptionsMessageTypeDef:
        """
        Returns descriptions for existing environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/describe_environments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#describe_environments)
        """

    def describe_events(
        self, **kwargs: Unpack[DescribeEventsMessageRequestTypeDef]
    ) -> EventDescriptionsMessageTypeDef:
        """
        Returns list of event descriptions matching criteria up to the last 6 weeks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/describe_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#describe_events)
        """

    def describe_instances_health(
        self, **kwargs: Unpack[DescribeInstancesHealthRequestRequestTypeDef]
    ) -> DescribeInstancesHealthResultTypeDef:
        """
        Retrieves detailed information about the health of instances in your AWS
        Elastic Beanstalk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/describe_instances_health.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#describe_instances_health)
        """

    def describe_platform_version(
        self, **kwargs: Unpack[DescribePlatformVersionRequestRequestTypeDef]
    ) -> DescribePlatformVersionResultTypeDef:
        """
        Describes a platform version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/describe_platform_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#describe_platform_version)
        """

    def disassociate_environment_operations_role(
        self, **kwargs: Unpack[DisassociateEnvironmentOperationsRoleMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociate the operations role from an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/disassociate_environment_operations_role.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#disassociate_environment_operations_role)
        """

    def list_available_solution_stacks(self) -> ListAvailableSolutionStacksResultMessageTypeDef:
        """
        Returns a list of the available solution stack names, with the public version
        first and then in reverse chronological order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/list_available_solution_stacks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#list_available_solution_stacks)
        """

    def list_platform_branches(
        self, **kwargs: Unpack[ListPlatformBranchesRequestRequestTypeDef]
    ) -> ListPlatformBranchesResultTypeDef:
        """
        Lists the platform branches available for your account in an AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/list_platform_branches.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#list_platform_branches)
        """

    def list_platform_versions(
        self, **kwargs: Unpack[ListPlatformVersionsRequestRequestTypeDef]
    ) -> ListPlatformVersionsResultTypeDef:
        """
        Lists the platform versions available for your account in an AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/list_platform_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#list_platform_versions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceMessageRequestTypeDef]
    ) -> ResourceTagsDescriptionMessageTypeDef:
        """
        Return the tags applied to an AWS Elastic Beanstalk resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#list_tags_for_resource)
        """

    def rebuild_environment(
        self, **kwargs: Unpack[RebuildEnvironmentMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes and recreates all of the AWS resources (for example: the Auto Scaling
        group, load balancer, etc.) for a specified environment and forces a restart.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/rebuild_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#rebuild_environment)
        """

    def request_environment_info(
        self, **kwargs: Unpack[RequestEnvironmentInfoMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Initiates a request to compile the specified type of information of the
        deployed environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/request_environment_info.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#request_environment_info)
        """

    def restart_app_server(
        self, **kwargs: Unpack[RestartAppServerMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Causes the environment to restart the application container server running on
        each Amazon EC2 instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/restart_app_server.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#restart_app_server)
        """

    def retrieve_environment_info(
        self, **kwargs: Unpack[RetrieveEnvironmentInfoMessageRequestTypeDef]
    ) -> RetrieveEnvironmentInfoResultMessageTypeDef:
        """
        Retrieves the compiled information from a <a>RequestEnvironmentInfo</a> request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/retrieve_environment_info.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#retrieve_environment_info)
        """

    def swap_environment_cnames(
        self, **kwargs: Unpack[SwapEnvironmentCNAMEsMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Swaps the CNAMEs of two environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/swap_environment_cnames.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#swap_environment_cnames)
        """

    def terminate_environment(
        self, **kwargs: Unpack[TerminateEnvironmentMessageRequestTypeDef]
    ) -> EnvironmentDescriptionResponseTypeDef:
        """
        Terminates the specified environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/terminate_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#terminate_environment)
        """

    def update_application(
        self, **kwargs: Unpack[UpdateApplicationMessageRequestTypeDef]
    ) -> ApplicationDescriptionMessageTypeDef:
        """
        Updates the specified application to have the specified properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/update_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#update_application)
        """

    def update_application_resource_lifecycle(
        self, **kwargs: Unpack[UpdateApplicationResourceLifecycleMessageRequestTypeDef]
    ) -> ApplicationResourceLifecycleDescriptionMessageTypeDef:
        """
        Modifies lifecycle settings for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/update_application_resource_lifecycle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#update_application_resource_lifecycle)
        """

    def update_application_version(
        self, **kwargs: Unpack[UpdateApplicationVersionMessageRequestTypeDef]
    ) -> ApplicationVersionDescriptionMessageTypeDef:
        """
        Updates the specified application version to have the specified properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/update_application_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#update_application_version)
        """

    def update_configuration_template(
        self, **kwargs: Unpack[UpdateConfigurationTemplateMessageRequestTypeDef]
    ) -> ConfigurationSettingsDescriptionResponseTypeDef:
        """
        Updates the specified configuration template to have the specified properties
        or configuration option values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/update_configuration_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#update_configuration_template)
        """

    def update_environment(
        self, **kwargs: Unpack[UpdateEnvironmentMessageRequestTypeDef]
    ) -> EnvironmentDescriptionResponseTypeDef:
        """
        Updates the environment description, deploys a new application version, updates
        the configuration settings to an entirely new configuration template, or
        updates select configuration option values in the running environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/update_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#update_environment)
        """

    def update_tags_for_resource(
        self, **kwargs: Unpack[UpdateTagsForResourceMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update the list of tags applied to an AWS Elastic Beanstalk resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/update_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#update_tags_for_resource)
        """

    def validate_configuration_settings(
        self, **kwargs: Unpack[ValidateConfigurationSettingsMessageRequestTypeDef]
    ) -> ConfigurationSettingsValidationMessagesTypeDef:
        """
        Takes a set of configuration settings and either a configuration template or
        environment, and determines whether those values are valid.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/validate_configuration_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#validate_configuration_settings)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_application_versions"]
    ) -> DescribeApplicationVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_environment_managed_action_history"]
    ) -> DescribeEnvironmentManagedActionHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_environments"]
    ) -> DescribeEnvironmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_platform_versions"]
    ) -> ListPlatformVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["environment_exists"]) -> EnvironmentExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["environment_terminated"]
    ) -> EnvironmentTerminatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["environment_updated"]) -> EnvironmentUpdatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elasticbeanstalk/client/#get_waiter)
        """
