"""
Type annotations for launch-wizard service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_launch_wizard.client import LaunchWizardClient

    session = Session()
    client: LaunchWizardClient = session.client("launch-wizard")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListDeploymentEventsPaginator,
    ListDeploymentsPaginator,
    ListWorkloadDeploymentPatternsPaginator,
    ListWorkloadsPaginator,
)
from .type_defs import (
    CreateDeploymentInputRequestTypeDef,
    CreateDeploymentOutputTypeDef,
    DeleteDeploymentInputRequestTypeDef,
    DeleteDeploymentOutputTypeDef,
    GetDeploymentInputRequestTypeDef,
    GetDeploymentOutputTypeDef,
    GetWorkloadDeploymentPatternInputRequestTypeDef,
    GetWorkloadDeploymentPatternOutputTypeDef,
    GetWorkloadInputRequestTypeDef,
    GetWorkloadOutputTypeDef,
    ListDeploymentEventsInputRequestTypeDef,
    ListDeploymentEventsOutputTypeDef,
    ListDeploymentsInputRequestTypeDef,
    ListDeploymentsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListWorkloadDeploymentPatternsInputRequestTypeDef,
    ListWorkloadDeploymentPatternsOutputTypeDef,
    ListWorkloadsInputRequestTypeDef,
    ListWorkloadsOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("LaunchWizardClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceLimitException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LaunchWizardClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LaunchWizardClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#close)
        """

    def create_deployment(
        self, **kwargs: Unpack[CreateDeploymentInputRequestTypeDef]
    ) -> CreateDeploymentOutputTypeDef:
        """
        Creates a deployment for the given workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/create_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#create_deployment)
        """

    def delete_deployment(
        self, **kwargs: Unpack[DeleteDeploymentInputRequestTypeDef]
    ) -> DeleteDeploymentOutputTypeDef:
        """
        Deletes a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/delete_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#delete_deployment)
        """

    def get_deployment(
        self, **kwargs: Unpack[GetDeploymentInputRequestTypeDef]
    ) -> GetDeploymentOutputTypeDef:
        """
        Returns information about the deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#get_deployment)
        """

    def get_workload(
        self, **kwargs: Unpack[GetWorkloadInputRequestTypeDef]
    ) -> GetWorkloadOutputTypeDef:
        """
        Returns information about a workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_workload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#get_workload)
        """

    def get_workload_deployment_pattern(
        self, **kwargs: Unpack[GetWorkloadDeploymentPatternInputRequestTypeDef]
    ) -> GetWorkloadDeploymentPatternOutputTypeDef:
        """
        Returns details for a given workload and deployment pattern, including the
        available specifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_workload_deployment_pattern.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#get_workload_deployment_pattern)
        """

    def list_deployment_events(
        self, **kwargs: Unpack[ListDeploymentEventsInputRequestTypeDef]
    ) -> ListDeploymentEventsOutputTypeDef:
        """
        Lists the events of a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/list_deployment_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#list_deployment_events)
        """

    def list_deployments(
        self, **kwargs: Unpack[ListDeploymentsInputRequestTypeDef]
    ) -> ListDeploymentsOutputTypeDef:
        """
        Lists the deployments that have been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/list_deployments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#list_deployments)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags associated with a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#list_tags_for_resource)
        """

    def list_workload_deployment_patterns(
        self, **kwargs: Unpack[ListWorkloadDeploymentPatternsInputRequestTypeDef]
    ) -> ListWorkloadDeploymentPatternsOutputTypeDef:
        """
        Lists the workload deployment patterns for a given workload name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/list_workload_deployment_patterns.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#list_workload_deployment_patterns)
        """

    def list_workloads(
        self, **kwargs: Unpack[ListWorkloadsInputRequestTypeDef]
    ) -> ListWorkloadsOutputTypeDef:
        """
        Lists the available workload names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/list_workloads.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#list_workloads)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tags to the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes the specified tags from the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployment_events"]
    ) -> ListDeploymentEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployments"]
    ) -> ListDeploymentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_workload_deployment_patterns"]
    ) -> ListWorkloadDeploymentPatternsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workloads"]) -> ListWorkloadsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_launch_wizard/client/#get_paginator)
        """
