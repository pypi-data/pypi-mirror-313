"""
Type annotations for grafana service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_grafana.client import ManagedGrafanaClient

    session = Session()
    client: ManagedGrafanaClient = session.client("grafana")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListPermissionsPaginator,
    ListVersionsPaginator,
    ListWorkspaceServiceAccountsPaginator,
    ListWorkspaceServiceAccountTokensPaginator,
    ListWorkspacesPaginator,
)
from .type_defs import (
    AssociateLicenseRequestRequestTypeDef,
    AssociateLicenseResponseTypeDef,
    CreateWorkspaceApiKeyRequestRequestTypeDef,
    CreateWorkspaceApiKeyResponseTypeDef,
    CreateWorkspaceRequestRequestTypeDef,
    CreateWorkspaceResponseTypeDef,
    CreateWorkspaceServiceAccountRequestRequestTypeDef,
    CreateWorkspaceServiceAccountResponseTypeDef,
    CreateWorkspaceServiceAccountTokenRequestRequestTypeDef,
    CreateWorkspaceServiceAccountTokenResponseTypeDef,
    DeleteWorkspaceApiKeyRequestRequestTypeDef,
    DeleteWorkspaceApiKeyResponseTypeDef,
    DeleteWorkspaceRequestRequestTypeDef,
    DeleteWorkspaceResponseTypeDef,
    DeleteWorkspaceServiceAccountRequestRequestTypeDef,
    DeleteWorkspaceServiceAccountResponseTypeDef,
    DeleteWorkspaceServiceAccountTokenRequestRequestTypeDef,
    DeleteWorkspaceServiceAccountTokenResponseTypeDef,
    DescribeWorkspaceAuthenticationRequestRequestTypeDef,
    DescribeWorkspaceAuthenticationResponseTypeDef,
    DescribeWorkspaceConfigurationRequestRequestTypeDef,
    DescribeWorkspaceConfigurationResponseTypeDef,
    DescribeWorkspaceRequestRequestTypeDef,
    DescribeWorkspaceResponseTypeDef,
    DisassociateLicenseRequestRequestTypeDef,
    DisassociateLicenseResponseTypeDef,
    ListPermissionsRequestRequestTypeDef,
    ListPermissionsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVersionsRequestRequestTypeDef,
    ListVersionsResponseTypeDef,
    ListWorkspaceServiceAccountsRequestRequestTypeDef,
    ListWorkspaceServiceAccountsResponseTypeDef,
    ListWorkspaceServiceAccountTokensRequestRequestTypeDef,
    ListWorkspaceServiceAccountTokensResponseTypeDef,
    ListWorkspacesRequestRequestTypeDef,
    ListWorkspacesResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdatePermissionsRequestRequestTypeDef,
    UpdatePermissionsResponseTypeDef,
    UpdateWorkspaceAuthenticationRequestRequestTypeDef,
    UpdateWorkspaceAuthenticationResponseTypeDef,
    UpdateWorkspaceConfigurationRequestRequestTypeDef,
    UpdateWorkspaceRequestRequestTypeDef,
    UpdateWorkspaceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ManagedGrafanaClient",)

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

class ManagedGrafanaClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ManagedGrafanaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#close)
        """

    def associate_license(
        self, **kwargs: Unpack[AssociateLicenseRequestRequestTypeDef]
    ) -> AssociateLicenseResponseTypeDef:
        """
        Assigns a Grafana Enterprise license to a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/associate_license.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#associate_license)
        """

    def create_workspace(
        self, **kwargs: Unpack[CreateWorkspaceRequestRequestTypeDef]
    ) -> CreateWorkspaceResponseTypeDef:
        """
        Creates a <i>workspace</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/create_workspace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#create_workspace)
        """

    def create_workspace_api_key(
        self, **kwargs: Unpack[CreateWorkspaceApiKeyRequestRequestTypeDef]
    ) -> CreateWorkspaceApiKeyResponseTypeDef:
        """
        Creates a Grafana API key for the workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/create_workspace_api_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#create_workspace_api_key)
        """

    def create_workspace_service_account(
        self, **kwargs: Unpack[CreateWorkspaceServiceAccountRequestRequestTypeDef]
    ) -> CreateWorkspaceServiceAccountResponseTypeDef:
        """
        Creates a service account for the workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/create_workspace_service_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#create_workspace_service_account)
        """

    def create_workspace_service_account_token(
        self, **kwargs: Unpack[CreateWorkspaceServiceAccountTokenRequestRequestTypeDef]
    ) -> CreateWorkspaceServiceAccountTokenResponseTypeDef:
        """
        Creates a token that can be used to authenticate and authorize Grafana HTTP API
        operations for the given <a
        href="https://docs.aws.amazon.com/grafana/latest/userguide/service-accounts.html">workspace
        service account</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/create_workspace_service_account_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#create_workspace_service_account_token)
        """

    def delete_workspace(
        self, **kwargs: Unpack[DeleteWorkspaceRequestRequestTypeDef]
    ) -> DeleteWorkspaceResponseTypeDef:
        """
        Deletes an Amazon Managed Grafana workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/delete_workspace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#delete_workspace)
        """

    def delete_workspace_api_key(
        self, **kwargs: Unpack[DeleteWorkspaceApiKeyRequestRequestTypeDef]
    ) -> DeleteWorkspaceApiKeyResponseTypeDef:
        """
        Deletes a Grafana API key for the workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/delete_workspace_api_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#delete_workspace_api_key)
        """

    def delete_workspace_service_account(
        self, **kwargs: Unpack[DeleteWorkspaceServiceAccountRequestRequestTypeDef]
    ) -> DeleteWorkspaceServiceAccountResponseTypeDef:
        """
        Deletes a workspace service account from the workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/delete_workspace_service_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#delete_workspace_service_account)
        """

    def delete_workspace_service_account_token(
        self, **kwargs: Unpack[DeleteWorkspaceServiceAccountTokenRequestRequestTypeDef]
    ) -> DeleteWorkspaceServiceAccountTokenResponseTypeDef:
        """
        Deletes a token for the workspace service account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/delete_workspace_service_account_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#delete_workspace_service_account_token)
        """

    def describe_workspace(
        self, **kwargs: Unpack[DescribeWorkspaceRequestRequestTypeDef]
    ) -> DescribeWorkspaceResponseTypeDef:
        """
        Displays information about one Amazon Managed Grafana workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/describe_workspace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#describe_workspace)
        """

    def describe_workspace_authentication(
        self, **kwargs: Unpack[DescribeWorkspaceAuthenticationRequestRequestTypeDef]
    ) -> DescribeWorkspaceAuthenticationResponseTypeDef:
        """
        Displays information about the authentication methods used in one Amazon
        Managed Grafana workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/describe_workspace_authentication.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#describe_workspace_authentication)
        """

    def describe_workspace_configuration(
        self, **kwargs: Unpack[DescribeWorkspaceConfigurationRequestRequestTypeDef]
    ) -> DescribeWorkspaceConfigurationResponseTypeDef:
        """
        Gets the current configuration string for the given workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/describe_workspace_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#describe_workspace_configuration)
        """

    def disassociate_license(
        self, **kwargs: Unpack[DisassociateLicenseRequestRequestTypeDef]
    ) -> DisassociateLicenseResponseTypeDef:
        """
        Removes the Grafana Enterprise license from a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/disassociate_license.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#disassociate_license)
        """

    def list_permissions(
        self, **kwargs: Unpack[ListPermissionsRequestRequestTypeDef]
    ) -> ListPermissionsResponseTypeDef:
        """
        Lists the users and groups who have the Grafana <code>Admin</code> and
        <code>Editor</code> roles in this workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/list_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#list_permissions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        The <code>ListTagsForResource</code> operation returns the tags that are
        associated with the Amazon Managed Service for Grafana resource specified by
        the <code>resourceArn</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#list_tags_for_resource)
        """

    def list_versions(
        self, **kwargs: Unpack[ListVersionsRequestRequestTypeDef]
    ) -> ListVersionsResponseTypeDef:
        """
        Lists available versions of Grafana.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/list_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#list_versions)
        """

    def list_workspace_service_account_tokens(
        self, **kwargs: Unpack[ListWorkspaceServiceAccountTokensRequestRequestTypeDef]
    ) -> ListWorkspaceServiceAccountTokensResponseTypeDef:
        """
        Returns a list of tokens for a workspace service account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/list_workspace_service_account_tokens.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#list_workspace_service_account_tokens)
        """

    def list_workspace_service_accounts(
        self, **kwargs: Unpack[ListWorkspaceServiceAccountsRequestRequestTypeDef]
    ) -> ListWorkspaceServiceAccountsResponseTypeDef:
        """
        Returns a list of service accounts for a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/list_workspace_service_accounts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#list_workspace_service_accounts)
        """

    def list_workspaces(
        self, **kwargs: Unpack[ListWorkspacesRequestRequestTypeDef]
    ) -> ListWorkspacesResponseTypeDef:
        """
        Returns a list of Amazon Managed Grafana workspaces in the account, with some
        information about each workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/list_workspaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#list_workspaces)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        The <code>TagResource</code> operation associates tags with an Amazon Managed
        Grafana resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The <code>UntagResource</code> operation removes the association of the tag
        with the Amazon Managed Grafana resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#untag_resource)
        """

    def update_permissions(
        self, **kwargs: Unpack[UpdatePermissionsRequestRequestTypeDef]
    ) -> UpdatePermissionsResponseTypeDef:
        """
        Updates which users in a workspace have the Grafana <code>Admin</code> or
        <code>Editor</code> roles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/update_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#update_permissions)
        """

    def update_workspace(
        self, **kwargs: Unpack[UpdateWorkspaceRequestRequestTypeDef]
    ) -> UpdateWorkspaceResponseTypeDef:
        """
        Modifies an existing Amazon Managed Grafana workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/update_workspace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#update_workspace)
        """

    def update_workspace_authentication(
        self, **kwargs: Unpack[UpdateWorkspaceAuthenticationRequestRequestTypeDef]
    ) -> UpdateWorkspaceAuthenticationResponseTypeDef:
        """
        Use this operation to define the identity provider (IdP) that this workspace
        authenticates users from, using SAML.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/update_workspace_authentication.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#update_workspace_authentication)
        """

    def update_workspace_configuration(
        self, **kwargs: Unpack[UpdateWorkspaceConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the configuration string for the given workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/update_workspace_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#update_workspace_configuration)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_permissions"]
    ) -> ListPermissionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_versions"]) -> ListVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_workspace_service_account_tokens"]
    ) -> ListWorkspaceServiceAccountTokensPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_workspace_service_accounts"]
    ) -> ListWorkspaceServiceAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workspaces"]) -> ListWorkspacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_grafana/client/#get_paginator)
        """
