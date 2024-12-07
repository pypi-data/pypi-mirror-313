"""
Type annotations for amp service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_amp.client import PrometheusServiceClient

    session = Session()
    client: PrometheusServiceClient = session.client("amp")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListRuleGroupsNamespacesPaginator,
    ListScrapersPaginator,
    ListWorkspacesPaginator,
)
from .type_defs import (
    CreateAlertManagerDefinitionRequestRequestTypeDef,
    CreateAlertManagerDefinitionResponseTypeDef,
    CreateLoggingConfigurationRequestRequestTypeDef,
    CreateLoggingConfigurationResponseTypeDef,
    CreateRuleGroupsNamespaceRequestRequestTypeDef,
    CreateRuleGroupsNamespaceResponseTypeDef,
    CreateScraperRequestRequestTypeDef,
    CreateScraperResponseTypeDef,
    CreateWorkspaceRequestRequestTypeDef,
    CreateWorkspaceResponseTypeDef,
    DeleteAlertManagerDefinitionRequestRequestTypeDef,
    DeleteLoggingConfigurationRequestRequestTypeDef,
    DeleteRuleGroupsNamespaceRequestRequestTypeDef,
    DeleteScraperRequestRequestTypeDef,
    DeleteScraperResponseTypeDef,
    DeleteWorkspaceRequestRequestTypeDef,
    DescribeAlertManagerDefinitionRequestRequestTypeDef,
    DescribeAlertManagerDefinitionResponseTypeDef,
    DescribeLoggingConfigurationRequestRequestTypeDef,
    DescribeLoggingConfigurationResponseTypeDef,
    DescribeRuleGroupsNamespaceRequestRequestTypeDef,
    DescribeRuleGroupsNamespaceResponseTypeDef,
    DescribeScraperRequestRequestTypeDef,
    DescribeScraperResponseTypeDef,
    DescribeWorkspaceRequestRequestTypeDef,
    DescribeWorkspaceResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetDefaultScraperConfigurationResponseTypeDef,
    ListRuleGroupsNamespacesRequestRequestTypeDef,
    ListRuleGroupsNamespacesResponseTypeDef,
    ListScrapersRequestRequestTypeDef,
    ListScrapersResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorkspacesRequestRequestTypeDef,
    ListWorkspacesResponseTypeDef,
    PutAlertManagerDefinitionRequestRequestTypeDef,
    PutAlertManagerDefinitionResponseTypeDef,
    PutRuleGroupsNamespaceRequestRequestTypeDef,
    PutRuleGroupsNamespaceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateLoggingConfigurationRequestRequestTypeDef,
    UpdateLoggingConfigurationResponseTypeDef,
    UpdateScraperRequestRequestTypeDef,
    UpdateScraperResponseTypeDef,
    UpdateWorkspaceAliasRequestRequestTypeDef,
)
from .waiter import (
    ScraperActiveWaiter,
    ScraperDeletedWaiter,
    WorkspaceActiveWaiter,
    WorkspaceDeletedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("PrometheusServiceClient",)

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

class PrometheusServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp.html#PrometheusService.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PrometheusServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp.html#PrometheusService.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#close)
        """

    def create_alert_manager_definition(
        self, **kwargs: Unpack[CreateAlertManagerDefinitionRequestRequestTypeDef]
    ) -> CreateAlertManagerDefinitionResponseTypeDef:
        """
        The <code>CreateAlertManagerDefinition</code> operation creates the alert
        manager definition in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/create_alert_manager_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#create_alert_manager_definition)
        """

    def create_logging_configuration(
        self, **kwargs: Unpack[CreateLoggingConfigurationRequestRequestTypeDef]
    ) -> CreateLoggingConfigurationResponseTypeDef:
        """
        The <code>CreateLoggingConfiguration</code> operation creates a logging
        configuration for the workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/create_logging_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#create_logging_configuration)
        """

    def create_rule_groups_namespace(
        self, **kwargs: Unpack[CreateRuleGroupsNamespaceRequestRequestTypeDef]
    ) -> CreateRuleGroupsNamespaceResponseTypeDef:
        """
        The <code>CreateRuleGroupsNamespace</code> operation creates a rule groups
        namespace within a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/create_rule_groups_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#create_rule_groups_namespace)
        """

    def create_scraper(
        self, **kwargs: Unpack[CreateScraperRequestRequestTypeDef]
    ) -> CreateScraperResponseTypeDef:
        """
        The <code>CreateScraper</code> operation creates a scraper to collect metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/create_scraper.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#create_scraper)
        """

    def create_workspace(
        self, **kwargs: Unpack[CreateWorkspaceRequestRequestTypeDef]
    ) -> CreateWorkspaceResponseTypeDef:
        """
        Creates a Prometheus workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/create_workspace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#create_workspace)
        """

    def delete_alert_manager_definition(
        self, **kwargs: Unpack[DeleteAlertManagerDefinitionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the alert manager definition from a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/delete_alert_manager_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#delete_alert_manager_definition)
        """

    def delete_logging_configuration(
        self, **kwargs: Unpack[DeleteLoggingConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the logging configuration for a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/delete_logging_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#delete_logging_configuration)
        """

    def delete_rule_groups_namespace(
        self, **kwargs: Unpack[DeleteRuleGroupsNamespaceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes one rule groups namespace and its associated rule groups definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/delete_rule_groups_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#delete_rule_groups_namespace)
        """

    def delete_scraper(
        self, **kwargs: Unpack[DeleteScraperRequestRequestTypeDef]
    ) -> DeleteScraperResponseTypeDef:
        """
        The <code>DeleteScraper</code> operation deletes one scraper, and stops any
        metrics collection that the scraper performs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/delete_scraper.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#delete_scraper)
        """

    def delete_workspace(
        self, **kwargs: Unpack[DeleteWorkspaceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an existing workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/delete_workspace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#delete_workspace)
        """

    def describe_alert_manager_definition(
        self, **kwargs: Unpack[DescribeAlertManagerDefinitionRequestRequestTypeDef]
    ) -> DescribeAlertManagerDefinitionResponseTypeDef:
        """
        Retrieves the full information about the alert manager definition for a
        workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/describe_alert_manager_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#describe_alert_manager_definition)
        """

    def describe_logging_configuration(
        self, **kwargs: Unpack[DescribeLoggingConfigurationRequestRequestTypeDef]
    ) -> DescribeLoggingConfigurationResponseTypeDef:
        """
        Returns complete information about the current logging configuration of the
        workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/describe_logging_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#describe_logging_configuration)
        """

    def describe_rule_groups_namespace(
        self, **kwargs: Unpack[DescribeRuleGroupsNamespaceRequestRequestTypeDef]
    ) -> DescribeRuleGroupsNamespaceResponseTypeDef:
        """
        Returns complete information about one rule groups namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/describe_rule_groups_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#describe_rule_groups_namespace)
        """

    def describe_scraper(
        self, **kwargs: Unpack[DescribeScraperRequestRequestTypeDef]
    ) -> DescribeScraperResponseTypeDef:
        """
        The <code>DescribeScraper</code> operation displays information about an
        existing scraper.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/describe_scraper.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#describe_scraper)
        """

    def describe_workspace(
        self, **kwargs: Unpack[DescribeWorkspaceRequestRequestTypeDef]
    ) -> DescribeWorkspaceResponseTypeDef:
        """
        Returns information about an existing workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/describe_workspace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#describe_workspace)
        """

    def get_default_scraper_configuration(self) -> GetDefaultScraperConfigurationResponseTypeDef:
        """
        The <code>GetDefaultScraperConfiguration</code> operation returns the default
        scraper configuration used when Amazon EKS creates a scraper for you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/get_default_scraper_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#get_default_scraper_configuration)
        """

    def list_rule_groups_namespaces(
        self, **kwargs: Unpack[ListRuleGroupsNamespacesRequestRequestTypeDef]
    ) -> ListRuleGroupsNamespacesResponseTypeDef:
        """
        Returns a list of rule groups namespaces in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/list_rule_groups_namespaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#list_rule_groups_namespaces)
        """

    def list_scrapers(
        self, **kwargs: Unpack[ListScrapersRequestRequestTypeDef]
    ) -> ListScrapersResponseTypeDef:
        """
        The <code>ListScrapers</code> operation lists all of the scrapers in your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/list_scrapers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#list_scrapers)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        The <code>ListTagsForResource</code> operation returns the tags that are
        associated with an Amazon Managed Service for Prometheus resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#list_tags_for_resource)
        """

    def list_workspaces(
        self, **kwargs: Unpack[ListWorkspacesRequestRequestTypeDef]
    ) -> ListWorkspacesResponseTypeDef:
        """
        Lists all of the Amazon Managed Service for Prometheus workspaces in your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/list_workspaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#list_workspaces)
        """

    def put_alert_manager_definition(
        self, **kwargs: Unpack[PutAlertManagerDefinitionRequestRequestTypeDef]
    ) -> PutAlertManagerDefinitionResponseTypeDef:
        """
        Updates an existing alert manager definition in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/put_alert_manager_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#put_alert_manager_definition)
        """

    def put_rule_groups_namespace(
        self, **kwargs: Unpack[PutRuleGroupsNamespaceRequestRequestTypeDef]
    ) -> PutRuleGroupsNamespaceResponseTypeDef:
        """
        Updates an existing rule groups namespace within a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/put_rule_groups_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#put_rule_groups_namespace)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        The <code>TagResource</code> operation associates tags with an Amazon Managed
        Service for Prometheus resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from an Amazon Managed Service for Prometheus
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#untag_resource)
        """

    def update_logging_configuration(
        self, **kwargs: Unpack[UpdateLoggingConfigurationRequestRequestTypeDef]
    ) -> UpdateLoggingConfigurationResponseTypeDef:
        """
        Updates the log group ARN or the workspace ID of the current logging
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/update_logging_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#update_logging_configuration)
        """

    def update_scraper(
        self, **kwargs: Unpack[UpdateScraperRequestRequestTypeDef]
    ) -> UpdateScraperResponseTypeDef:
        """
        Updates an existing scraper.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/update_scraper.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#update_scraper)
        """

    def update_workspace_alias(
        self, **kwargs: Unpack[UpdateWorkspaceAliasRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the alias of an existing workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/update_workspace_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#update_workspace_alias)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_rule_groups_namespaces"]
    ) -> ListRuleGroupsNamespacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_scrapers"]) -> ListScrapersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workspaces"]) -> ListWorkspacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["scraper_active"]) -> ScraperActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["scraper_deleted"]) -> ScraperDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["workspace_active"]) -> WorkspaceActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["workspace_deleted"]) -> WorkspaceDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amp/client/#get_waiter)
        """
