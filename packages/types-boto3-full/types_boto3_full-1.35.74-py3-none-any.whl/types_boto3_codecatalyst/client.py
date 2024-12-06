"""
Type annotations for codecatalyst service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_codecatalyst.client import CodeCatalystClient

    session = Session()
    client: CodeCatalystClient = session.client("codecatalyst")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAccessTokensPaginator,
    ListDevEnvironmentSessionsPaginator,
    ListDevEnvironmentsPaginator,
    ListEventLogsPaginator,
    ListProjectsPaginator,
    ListSourceRepositoriesPaginator,
    ListSourceRepositoryBranchesPaginator,
    ListSpacesPaginator,
    ListWorkflowRunsPaginator,
    ListWorkflowsPaginator,
)
from .type_defs import (
    CreateAccessTokenRequestRequestTypeDef,
    CreateAccessTokenResponseTypeDef,
    CreateDevEnvironmentRequestRequestTypeDef,
    CreateDevEnvironmentResponseTypeDef,
    CreateProjectRequestRequestTypeDef,
    CreateProjectResponseTypeDef,
    CreateSourceRepositoryBranchRequestRequestTypeDef,
    CreateSourceRepositoryBranchResponseTypeDef,
    CreateSourceRepositoryRequestRequestTypeDef,
    CreateSourceRepositoryResponseTypeDef,
    DeleteAccessTokenRequestRequestTypeDef,
    DeleteDevEnvironmentRequestRequestTypeDef,
    DeleteDevEnvironmentResponseTypeDef,
    DeleteProjectRequestRequestTypeDef,
    DeleteProjectResponseTypeDef,
    DeleteSourceRepositoryRequestRequestTypeDef,
    DeleteSourceRepositoryResponseTypeDef,
    DeleteSpaceRequestRequestTypeDef,
    DeleteSpaceResponseTypeDef,
    GetDevEnvironmentRequestRequestTypeDef,
    GetDevEnvironmentResponseTypeDef,
    GetProjectRequestRequestTypeDef,
    GetProjectResponseTypeDef,
    GetSourceRepositoryCloneUrlsRequestRequestTypeDef,
    GetSourceRepositoryCloneUrlsResponseTypeDef,
    GetSourceRepositoryRequestRequestTypeDef,
    GetSourceRepositoryResponseTypeDef,
    GetSpaceRequestRequestTypeDef,
    GetSpaceResponseTypeDef,
    GetSubscriptionRequestRequestTypeDef,
    GetSubscriptionResponseTypeDef,
    GetUserDetailsRequestRequestTypeDef,
    GetUserDetailsResponseTypeDef,
    GetWorkflowRequestRequestTypeDef,
    GetWorkflowResponseTypeDef,
    GetWorkflowRunRequestRequestTypeDef,
    GetWorkflowRunResponseTypeDef,
    ListAccessTokensRequestRequestTypeDef,
    ListAccessTokensResponseTypeDef,
    ListDevEnvironmentSessionsRequestRequestTypeDef,
    ListDevEnvironmentSessionsResponseTypeDef,
    ListDevEnvironmentsRequestRequestTypeDef,
    ListDevEnvironmentsResponseTypeDef,
    ListEventLogsRequestRequestTypeDef,
    ListEventLogsResponseTypeDef,
    ListProjectsRequestRequestTypeDef,
    ListProjectsResponseTypeDef,
    ListSourceRepositoriesRequestRequestTypeDef,
    ListSourceRepositoriesResponseTypeDef,
    ListSourceRepositoryBranchesRequestRequestTypeDef,
    ListSourceRepositoryBranchesResponseTypeDef,
    ListSpacesRequestRequestTypeDef,
    ListSpacesResponseTypeDef,
    ListWorkflowRunsRequestRequestTypeDef,
    ListWorkflowRunsResponseTypeDef,
    ListWorkflowsRequestRequestTypeDef,
    ListWorkflowsResponseTypeDef,
    StartDevEnvironmentRequestRequestTypeDef,
    StartDevEnvironmentResponseTypeDef,
    StartDevEnvironmentSessionRequestRequestTypeDef,
    StartDevEnvironmentSessionResponseTypeDef,
    StartWorkflowRunRequestRequestTypeDef,
    StartWorkflowRunResponseTypeDef,
    StopDevEnvironmentRequestRequestTypeDef,
    StopDevEnvironmentResponseTypeDef,
    StopDevEnvironmentSessionRequestRequestTypeDef,
    StopDevEnvironmentSessionResponseTypeDef,
    UpdateDevEnvironmentRequestRequestTypeDef,
    UpdateDevEnvironmentResponseTypeDef,
    UpdateProjectRequestRequestTypeDef,
    UpdateProjectResponseTypeDef,
    UpdateSpaceRequestRequestTypeDef,
    UpdateSpaceResponseTypeDef,
    VerifySessionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CodeCatalystClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CodeCatalystClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst.html#CodeCatalyst.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeCatalystClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst.html#CodeCatalyst.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#close)
        """

    def create_access_token(
        self, **kwargs: Unpack[CreateAccessTokenRequestRequestTypeDef]
    ) -> CreateAccessTokenResponseTypeDef:
        """
        Creates a personal access token (PAT) for the current user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/create_access_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#create_access_token)
        """

    def create_dev_environment(
        self, **kwargs: Unpack[CreateDevEnvironmentRequestRequestTypeDef]
    ) -> CreateDevEnvironmentResponseTypeDef:
        """
        Creates a Dev Environment in Amazon CodeCatalyst, a cloud-based development
        environment that you can use to quickly work on the code stored in the source
        repositories of your project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/create_dev_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#create_dev_environment)
        """

    def create_project(
        self, **kwargs: Unpack[CreateProjectRequestRequestTypeDef]
    ) -> CreateProjectResponseTypeDef:
        """
        Creates a project in a specified space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/create_project.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#create_project)
        """

    def create_source_repository(
        self, **kwargs: Unpack[CreateSourceRepositoryRequestRequestTypeDef]
    ) -> CreateSourceRepositoryResponseTypeDef:
        """
        Creates an empty Git-based source repository in a specified project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/create_source_repository.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#create_source_repository)
        """

    def create_source_repository_branch(
        self, **kwargs: Unpack[CreateSourceRepositoryBranchRequestRequestTypeDef]
    ) -> CreateSourceRepositoryBranchResponseTypeDef:
        """
        Creates a branch in a specified source repository in Amazon CodeCatalyst.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/create_source_repository_branch.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#create_source_repository_branch)
        """

    def delete_access_token(
        self, **kwargs: Unpack[DeleteAccessTokenRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specified personal access token (PAT).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/delete_access_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#delete_access_token)
        """

    def delete_dev_environment(
        self, **kwargs: Unpack[DeleteDevEnvironmentRequestRequestTypeDef]
    ) -> DeleteDevEnvironmentResponseTypeDef:
        """
        Deletes a Dev Environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/delete_dev_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#delete_dev_environment)
        """

    def delete_project(
        self, **kwargs: Unpack[DeleteProjectRequestRequestTypeDef]
    ) -> DeleteProjectResponseTypeDef:
        """
        Deletes a project in a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/delete_project.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#delete_project)
        """

    def delete_source_repository(
        self, **kwargs: Unpack[DeleteSourceRepositoryRequestRequestTypeDef]
    ) -> DeleteSourceRepositoryResponseTypeDef:
        """
        Deletes a source repository in Amazon CodeCatalyst.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/delete_source_repository.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#delete_source_repository)
        """

    def delete_space(
        self, **kwargs: Unpack[DeleteSpaceRequestRequestTypeDef]
    ) -> DeleteSpaceResponseTypeDef:
        """
        Deletes a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/delete_space.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#delete_space)
        """

    def get_dev_environment(
        self, **kwargs: Unpack[GetDevEnvironmentRequestRequestTypeDef]
    ) -> GetDevEnvironmentResponseTypeDef:
        """
        Returns information about a Dev Environment for a source repository in a
        project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_dev_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_dev_environment)
        """

    def get_project(
        self, **kwargs: Unpack[GetProjectRequestRequestTypeDef]
    ) -> GetProjectResponseTypeDef:
        """
        Returns information about a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_project.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_project)
        """

    def get_source_repository(
        self, **kwargs: Unpack[GetSourceRepositoryRequestRequestTypeDef]
    ) -> GetSourceRepositoryResponseTypeDef:
        """
        Returns information about a source repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_source_repository.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_source_repository)
        """

    def get_source_repository_clone_urls(
        self, **kwargs: Unpack[GetSourceRepositoryCloneUrlsRequestRequestTypeDef]
    ) -> GetSourceRepositoryCloneUrlsResponseTypeDef:
        """
        Returns information about the URLs that can be used with a Git client to clone
        a source repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_source_repository_clone_urls.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_source_repository_clone_urls)
        """

    def get_space(self, **kwargs: Unpack[GetSpaceRequestRequestTypeDef]) -> GetSpaceResponseTypeDef:
        """
        Returns information about an space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_space.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_space)
        """

    def get_subscription(
        self, **kwargs: Unpack[GetSubscriptionRequestRequestTypeDef]
    ) -> GetSubscriptionResponseTypeDef:
        """
        Returns information about the Amazon Web Services account used for billing
        purposes and the billing plan for the space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_subscription)
        """

    def get_user_details(
        self, **kwargs: Unpack[GetUserDetailsRequestRequestTypeDef]
    ) -> GetUserDetailsResponseTypeDef:
        """
        Returns information about a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_user_details.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_user_details)
        """

    def get_workflow(
        self, **kwargs: Unpack[GetWorkflowRequestRequestTypeDef]
    ) -> GetWorkflowResponseTypeDef:
        """
        Returns information about a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_workflow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_workflow)
        """

    def get_workflow_run(
        self, **kwargs: Unpack[GetWorkflowRunRequestRequestTypeDef]
    ) -> GetWorkflowRunResponseTypeDef:
        """
        Returns information about a specified run of a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_workflow_run.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_workflow_run)
        """

    def list_access_tokens(
        self, **kwargs: Unpack[ListAccessTokensRequestRequestTypeDef]
    ) -> ListAccessTokensResponseTypeDef:
        """
        Lists all personal access tokens (PATs) associated with the user who calls the
        API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/list_access_tokens.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#list_access_tokens)
        """

    def list_dev_environment_sessions(
        self, **kwargs: Unpack[ListDevEnvironmentSessionsRequestRequestTypeDef]
    ) -> ListDevEnvironmentSessionsResponseTypeDef:
        """
        Retrieves a list of active sessions for a Dev Environment in a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/list_dev_environment_sessions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#list_dev_environment_sessions)
        """

    def list_dev_environments(
        self, **kwargs: Unpack[ListDevEnvironmentsRequestRequestTypeDef]
    ) -> ListDevEnvironmentsResponseTypeDef:
        """
        Retrieves a list of Dev Environments in a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/list_dev_environments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#list_dev_environments)
        """

    def list_event_logs(
        self, **kwargs: Unpack[ListEventLogsRequestRequestTypeDef]
    ) -> ListEventLogsResponseTypeDef:
        """
        Retrieves a list of events that occurred during a specific time in a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/list_event_logs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#list_event_logs)
        """

    def list_projects(
        self, **kwargs: Unpack[ListProjectsRequestRequestTypeDef]
    ) -> ListProjectsResponseTypeDef:
        """
        Retrieves a list of projects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/list_projects.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#list_projects)
        """

    def list_source_repositories(
        self, **kwargs: Unpack[ListSourceRepositoriesRequestRequestTypeDef]
    ) -> ListSourceRepositoriesResponseTypeDef:
        """
        Retrieves a list of source repositories in a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/list_source_repositories.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#list_source_repositories)
        """

    def list_source_repository_branches(
        self, **kwargs: Unpack[ListSourceRepositoryBranchesRequestRequestTypeDef]
    ) -> ListSourceRepositoryBranchesResponseTypeDef:
        """
        Retrieves a list of branches in a specified source repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/list_source_repository_branches.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#list_source_repository_branches)
        """

    def list_spaces(
        self, **kwargs: Unpack[ListSpacesRequestRequestTypeDef]
    ) -> ListSpacesResponseTypeDef:
        """
        Retrieves a list of spaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/list_spaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#list_spaces)
        """

    def list_workflow_runs(
        self, **kwargs: Unpack[ListWorkflowRunsRequestRequestTypeDef]
    ) -> ListWorkflowRunsResponseTypeDef:
        """
        Retrieves a list of workflow runs of a specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/list_workflow_runs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#list_workflow_runs)
        """

    def list_workflows(
        self, **kwargs: Unpack[ListWorkflowsRequestRequestTypeDef]
    ) -> ListWorkflowsResponseTypeDef:
        """
        Retrieves a list of workflows in a specified project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/list_workflows.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#list_workflows)
        """

    def start_dev_environment(
        self, **kwargs: Unpack[StartDevEnvironmentRequestRequestTypeDef]
    ) -> StartDevEnvironmentResponseTypeDef:
        """
        Starts a specified Dev Environment and puts it into an active state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/start_dev_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#start_dev_environment)
        """

    def start_dev_environment_session(
        self, **kwargs: Unpack[StartDevEnvironmentSessionRequestRequestTypeDef]
    ) -> StartDevEnvironmentSessionResponseTypeDef:
        """
        Starts a session for a specified Dev Environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/start_dev_environment_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#start_dev_environment_session)
        """

    def start_workflow_run(
        self, **kwargs: Unpack[StartWorkflowRunRequestRequestTypeDef]
    ) -> StartWorkflowRunResponseTypeDef:
        """
        Begins a run of a specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/start_workflow_run.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#start_workflow_run)
        """

    def stop_dev_environment(
        self, **kwargs: Unpack[StopDevEnvironmentRequestRequestTypeDef]
    ) -> StopDevEnvironmentResponseTypeDef:
        """
        Pauses a specified Dev Environment and places it in a non-running state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/stop_dev_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#stop_dev_environment)
        """

    def stop_dev_environment_session(
        self, **kwargs: Unpack[StopDevEnvironmentSessionRequestRequestTypeDef]
    ) -> StopDevEnvironmentSessionResponseTypeDef:
        """
        Stops a session for a specified Dev Environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/stop_dev_environment_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#stop_dev_environment_session)
        """

    def update_dev_environment(
        self, **kwargs: Unpack[UpdateDevEnvironmentRequestRequestTypeDef]
    ) -> UpdateDevEnvironmentResponseTypeDef:
        """
        Changes one or more values for a Dev Environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/update_dev_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#update_dev_environment)
        """

    def update_project(
        self, **kwargs: Unpack[UpdateProjectRequestRequestTypeDef]
    ) -> UpdateProjectResponseTypeDef:
        """
        Changes one or more values for a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/update_project.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#update_project)
        """

    def update_space(
        self, **kwargs: Unpack[UpdateSpaceRequestRequestTypeDef]
    ) -> UpdateSpaceResponseTypeDef:
        """
        Changes one or more values for a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/update_space.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#update_space)
        """

    def verify_session(self) -> VerifySessionResponseTypeDef:
        """
        Verifies whether the calling user has a valid Amazon CodeCatalyst login and
        session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/verify_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#verify_session)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_access_tokens"]
    ) -> ListAccessTokensPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dev_environment_sessions"]
    ) -> ListDevEnvironmentSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dev_environments"]
    ) -> ListDevEnvironmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_event_logs"]) -> ListEventLogsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_source_repositories"]
    ) -> ListSourceRepositoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_source_repository_branches"]
    ) -> ListSourceRepositoryBranchesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_spaces"]) -> ListSpacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_workflow_runs"]
    ) -> ListWorkflowRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workflows"]) -> ListWorkflowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecatalyst/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codecatalyst/client/#get_paginator)
        """
