"""
Type annotations for robomaker service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_robomaker.client import RoboMakerClient

    session = Session()
    client: RoboMakerClient = session.client("robomaker")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListDeploymentJobsPaginator,
    ListFleetsPaginator,
    ListRobotApplicationsPaginator,
    ListRobotsPaginator,
    ListSimulationApplicationsPaginator,
    ListSimulationJobBatchesPaginator,
    ListSimulationJobsPaginator,
    ListWorldExportJobsPaginator,
    ListWorldGenerationJobsPaginator,
    ListWorldsPaginator,
    ListWorldTemplatesPaginator,
)
from .type_defs import (
    BatchDeleteWorldsRequestRequestTypeDef,
    BatchDeleteWorldsResponseTypeDef,
    BatchDescribeSimulationJobRequestRequestTypeDef,
    BatchDescribeSimulationJobResponseTypeDef,
    CancelDeploymentJobRequestRequestTypeDef,
    CancelSimulationJobBatchRequestRequestTypeDef,
    CancelSimulationJobRequestRequestTypeDef,
    CancelWorldExportJobRequestRequestTypeDef,
    CancelWorldGenerationJobRequestRequestTypeDef,
    CreateDeploymentJobRequestRequestTypeDef,
    CreateDeploymentJobResponseTypeDef,
    CreateFleetRequestRequestTypeDef,
    CreateFleetResponseTypeDef,
    CreateRobotApplicationRequestRequestTypeDef,
    CreateRobotApplicationResponseTypeDef,
    CreateRobotApplicationVersionRequestRequestTypeDef,
    CreateRobotApplicationVersionResponseTypeDef,
    CreateRobotRequestRequestTypeDef,
    CreateRobotResponseTypeDef,
    CreateSimulationApplicationRequestRequestTypeDef,
    CreateSimulationApplicationResponseTypeDef,
    CreateSimulationApplicationVersionRequestRequestTypeDef,
    CreateSimulationApplicationVersionResponseTypeDef,
    CreateSimulationJobRequestRequestTypeDef,
    CreateSimulationJobResponseTypeDef,
    CreateWorldExportJobRequestRequestTypeDef,
    CreateWorldExportJobResponseTypeDef,
    CreateWorldGenerationJobRequestRequestTypeDef,
    CreateWorldGenerationJobResponseTypeDef,
    CreateWorldTemplateRequestRequestTypeDef,
    CreateWorldTemplateResponseTypeDef,
    DeleteFleetRequestRequestTypeDef,
    DeleteRobotApplicationRequestRequestTypeDef,
    DeleteRobotRequestRequestTypeDef,
    DeleteSimulationApplicationRequestRequestTypeDef,
    DeleteWorldTemplateRequestRequestTypeDef,
    DeregisterRobotRequestRequestTypeDef,
    DeregisterRobotResponseTypeDef,
    DescribeDeploymentJobRequestRequestTypeDef,
    DescribeDeploymentJobResponseTypeDef,
    DescribeFleetRequestRequestTypeDef,
    DescribeFleetResponseTypeDef,
    DescribeRobotApplicationRequestRequestTypeDef,
    DescribeRobotApplicationResponseTypeDef,
    DescribeRobotRequestRequestTypeDef,
    DescribeRobotResponseTypeDef,
    DescribeSimulationApplicationRequestRequestTypeDef,
    DescribeSimulationApplicationResponseTypeDef,
    DescribeSimulationJobBatchRequestRequestTypeDef,
    DescribeSimulationJobBatchResponseTypeDef,
    DescribeSimulationJobRequestRequestTypeDef,
    DescribeSimulationJobResponseTypeDef,
    DescribeWorldExportJobRequestRequestTypeDef,
    DescribeWorldExportJobResponseTypeDef,
    DescribeWorldGenerationJobRequestRequestTypeDef,
    DescribeWorldGenerationJobResponseTypeDef,
    DescribeWorldRequestRequestTypeDef,
    DescribeWorldResponseTypeDef,
    DescribeWorldTemplateRequestRequestTypeDef,
    DescribeWorldTemplateResponseTypeDef,
    GetWorldTemplateBodyRequestRequestTypeDef,
    GetWorldTemplateBodyResponseTypeDef,
    ListDeploymentJobsRequestRequestTypeDef,
    ListDeploymentJobsResponseTypeDef,
    ListFleetsRequestRequestTypeDef,
    ListFleetsResponseTypeDef,
    ListRobotApplicationsRequestRequestTypeDef,
    ListRobotApplicationsResponseTypeDef,
    ListRobotsRequestRequestTypeDef,
    ListRobotsResponseTypeDef,
    ListSimulationApplicationsRequestRequestTypeDef,
    ListSimulationApplicationsResponseTypeDef,
    ListSimulationJobBatchesRequestRequestTypeDef,
    ListSimulationJobBatchesResponseTypeDef,
    ListSimulationJobsRequestRequestTypeDef,
    ListSimulationJobsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorldExportJobsRequestRequestTypeDef,
    ListWorldExportJobsResponseTypeDef,
    ListWorldGenerationJobsRequestRequestTypeDef,
    ListWorldGenerationJobsResponseTypeDef,
    ListWorldsRequestRequestTypeDef,
    ListWorldsResponseTypeDef,
    ListWorldTemplatesRequestRequestTypeDef,
    ListWorldTemplatesResponseTypeDef,
    RegisterRobotRequestRequestTypeDef,
    RegisterRobotResponseTypeDef,
    RestartSimulationJobRequestRequestTypeDef,
    StartSimulationJobBatchRequestRequestTypeDef,
    StartSimulationJobBatchResponseTypeDef,
    SyncDeploymentJobRequestRequestTypeDef,
    SyncDeploymentJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateRobotApplicationRequestRequestTypeDef,
    UpdateRobotApplicationResponseTypeDef,
    UpdateSimulationApplicationRequestRequestTypeDef,
    UpdateSimulationApplicationResponseTypeDef,
    UpdateWorldTemplateRequestRequestTypeDef,
    UpdateWorldTemplateResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("RoboMakerClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentDeploymentException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]

class RoboMakerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RoboMakerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#close)
        """

    def batch_delete_worlds(
        self, **kwargs: Unpack[BatchDeleteWorldsRequestRequestTypeDef]
    ) -> BatchDeleteWorldsResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/batch_delete_worlds.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#batch_delete_worlds)
        """

    def batch_describe_simulation_job(
        self, **kwargs: Unpack[BatchDescribeSimulationJobRequestRequestTypeDef]
    ) -> BatchDescribeSimulationJobResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/batch_describe_simulation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#batch_describe_simulation_job)
        """

    def cancel_deployment_job(
        self, **kwargs: Unpack[CancelDeploymentJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This API is no longer supported.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/cancel_deployment_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#cancel_deployment_job)
        """

    def cancel_simulation_job(
        self, **kwargs: Unpack[CancelSimulationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/cancel_simulation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#cancel_simulation_job)
        """

    def cancel_simulation_job_batch(
        self, **kwargs: Unpack[CancelSimulationJobBatchRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/cancel_simulation_job_batch.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#cancel_simulation_job_batch)
        """

    def cancel_world_export_job(
        self, **kwargs: Unpack[CancelWorldExportJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/cancel_world_export_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#cancel_world_export_job)
        """

    def cancel_world_generation_job(
        self, **kwargs: Unpack[CancelWorldGenerationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/cancel_world_generation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#cancel_world_generation_job)
        """

    def create_deployment_job(
        self, **kwargs: Unpack[CreateDeploymentJobRequestRequestTypeDef]
    ) -> CreateDeploymentJobResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_deployment_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#create_deployment_job)
        """

    def create_fleet(
        self, **kwargs: Unpack[CreateFleetRequestRequestTypeDef]
    ) -> CreateFleetResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#create_fleet)
        """

    def create_robot(
        self, **kwargs: Unpack[CreateRobotRequestRequestTypeDef]
    ) -> CreateRobotResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_robot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#create_robot)
        """

    def create_robot_application(
        self, **kwargs: Unpack[CreateRobotApplicationRequestRequestTypeDef]
    ) -> CreateRobotApplicationResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_robot_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#create_robot_application)
        """

    def create_robot_application_version(
        self, **kwargs: Unpack[CreateRobotApplicationVersionRequestRequestTypeDef]
    ) -> CreateRobotApplicationVersionResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_robot_application_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#create_robot_application_version)
        """

    def create_simulation_application(
        self, **kwargs: Unpack[CreateSimulationApplicationRequestRequestTypeDef]
    ) -> CreateSimulationApplicationResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_simulation_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#create_simulation_application)
        """

    def create_simulation_application_version(
        self, **kwargs: Unpack[CreateSimulationApplicationVersionRequestRequestTypeDef]
    ) -> CreateSimulationApplicationVersionResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_simulation_application_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#create_simulation_application_version)
        """

    def create_simulation_job(
        self, **kwargs: Unpack[CreateSimulationJobRequestRequestTypeDef]
    ) -> CreateSimulationJobResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_simulation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#create_simulation_job)
        """

    def create_world_export_job(
        self, **kwargs: Unpack[CreateWorldExportJobRequestRequestTypeDef]
    ) -> CreateWorldExportJobResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_world_export_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#create_world_export_job)
        """

    def create_world_generation_job(
        self, **kwargs: Unpack[CreateWorldGenerationJobRequestRequestTypeDef]
    ) -> CreateWorldGenerationJobResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_world_generation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#create_world_generation_job)
        """

    def create_world_template(
        self, **kwargs: Unpack[CreateWorldTemplateRequestRequestTypeDef]
    ) -> CreateWorldTemplateResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/create_world_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#create_world_template)
        """

    def delete_fleet(self, **kwargs: Unpack[DeleteFleetRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/delete_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#delete_fleet)
        """

    def delete_robot(self, **kwargs: Unpack[DeleteRobotRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/delete_robot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#delete_robot)
        """

    def delete_robot_application(
        self, **kwargs: Unpack[DeleteRobotApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/delete_robot_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#delete_robot_application)
        """

    def delete_simulation_application(
        self, **kwargs: Unpack[DeleteSimulationApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/delete_simulation_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#delete_simulation_application)
        """

    def delete_world_template(
        self, **kwargs: Unpack[DeleteWorldTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/delete_world_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#delete_world_template)
        """

    def deregister_robot(
        self, **kwargs: Unpack[DeregisterRobotRequestRequestTypeDef]
    ) -> DeregisterRobotResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/deregister_robot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#deregister_robot)
        """

    def describe_deployment_job(
        self, **kwargs: Unpack[DescribeDeploymentJobRequestRequestTypeDef]
    ) -> DescribeDeploymentJobResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_deployment_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#describe_deployment_job)
        """

    def describe_fleet(
        self, **kwargs: Unpack[DescribeFleetRequestRequestTypeDef]
    ) -> DescribeFleetResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#describe_fleet)
        """

    def describe_robot(
        self, **kwargs: Unpack[DescribeRobotRequestRequestTypeDef]
    ) -> DescribeRobotResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_robot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#describe_robot)
        """

    def describe_robot_application(
        self, **kwargs: Unpack[DescribeRobotApplicationRequestRequestTypeDef]
    ) -> DescribeRobotApplicationResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_robot_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#describe_robot_application)
        """

    def describe_simulation_application(
        self, **kwargs: Unpack[DescribeSimulationApplicationRequestRequestTypeDef]
    ) -> DescribeSimulationApplicationResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_simulation_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#describe_simulation_application)
        """

    def describe_simulation_job(
        self, **kwargs: Unpack[DescribeSimulationJobRequestRequestTypeDef]
    ) -> DescribeSimulationJobResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_simulation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#describe_simulation_job)
        """

    def describe_simulation_job_batch(
        self, **kwargs: Unpack[DescribeSimulationJobBatchRequestRequestTypeDef]
    ) -> DescribeSimulationJobBatchResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_simulation_job_batch.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#describe_simulation_job_batch)
        """

    def describe_world(
        self, **kwargs: Unpack[DescribeWorldRequestRequestTypeDef]
    ) -> DescribeWorldResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_world.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#describe_world)
        """

    def describe_world_export_job(
        self, **kwargs: Unpack[DescribeWorldExportJobRequestRequestTypeDef]
    ) -> DescribeWorldExportJobResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_world_export_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#describe_world_export_job)
        """

    def describe_world_generation_job(
        self, **kwargs: Unpack[DescribeWorldGenerationJobRequestRequestTypeDef]
    ) -> DescribeWorldGenerationJobResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_world_generation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#describe_world_generation_job)
        """

    def describe_world_template(
        self, **kwargs: Unpack[DescribeWorldTemplateRequestRequestTypeDef]
    ) -> DescribeWorldTemplateResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/describe_world_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#describe_world_template)
        """

    def get_world_template_body(
        self, **kwargs: Unpack[GetWorldTemplateBodyRequestRequestTypeDef]
    ) -> GetWorldTemplateBodyResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_world_template_body.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#get_world_template_body)
        """

    def list_deployment_jobs(
        self, **kwargs: Unpack[ListDeploymentJobsRequestRequestTypeDef]
    ) -> ListDeploymentJobsResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_deployment_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#list_deployment_jobs)
        """

    def list_fleets(
        self, **kwargs: Unpack[ListFleetsRequestRequestTypeDef]
    ) -> ListFleetsResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_fleets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#list_fleets)
        """

    def list_robot_applications(
        self, **kwargs: Unpack[ListRobotApplicationsRequestRequestTypeDef]
    ) -> ListRobotApplicationsResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_robot_applications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#list_robot_applications)
        """

    def list_robots(
        self, **kwargs: Unpack[ListRobotsRequestRequestTypeDef]
    ) -> ListRobotsResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_robots.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#list_robots)
        """

    def list_simulation_applications(
        self, **kwargs: Unpack[ListSimulationApplicationsRequestRequestTypeDef]
    ) -> ListSimulationApplicationsResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_simulation_applications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#list_simulation_applications)
        """

    def list_simulation_job_batches(
        self, **kwargs: Unpack[ListSimulationJobBatchesRequestRequestTypeDef]
    ) -> ListSimulationJobBatchesResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_simulation_job_batches.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#list_simulation_job_batches)
        """

    def list_simulation_jobs(
        self, **kwargs: Unpack[ListSimulationJobsRequestRequestTypeDef]
    ) -> ListSimulationJobsResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_simulation_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#list_simulation_jobs)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#list_tags_for_resource)
        """

    def list_world_export_jobs(
        self, **kwargs: Unpack[ListWorldExportJobsRequestRequestTypeDef]
    ) -> ListWorldExportJobsResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_world_export_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#list_world_export_jobs)
        """

    def list_world_generation_jobs(
        self, **kwargs: Unpack[ListWorldGenerationJobsRequestRequestTypeDef]
    ) -> ListWorldGenerationJobsResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_world_generation_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#list_world_generation_jobs)
        """

    def list_world_templates(
        self, **kwargs: Unpack[ListWorldTemplatesRequestRequestTypeDef]
    ) -> ListWorldTemplatesResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_world_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#list_world_templates)
        """

    def list_worlds(
        self, **kwargs: Unpack[ListWorldsRequestRequestTypeDef]
    ) -> ListWorldsResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/list_worlds.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#list_worlds)
        """

    def register_robot(
        self, **kwargs: Unpack[RegisterRobotRequestRequestTypeDef]
    ) -> RegisterRobotResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/register_robot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#register_robot)
        """

    def restart_simulation_job(
        self, **kwargs: Unpack[RestartSimulationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/restart_simulation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#restart_simulation_job)
        """

    def start_simulation_job_batch(
        self, **kwargs: Unpack[StartSimulationJobBatchRequestRequestTypeDef]
    ) -> StartSimulationJobBatchResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/start_simulation_job_batch.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#start_simulation_job_batch)
        """

    def sync_deployment_job(
        self, **kwargs: Unpack[SyncDeploymentJobRequestRequestTypeDef]
    ) -> SyncDeploymentJobResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/sync_deployment_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#sync_deployment_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#untag_resource)
        """

    def update_robot_application(
        self, **kwargs: Unpack[UpdateRobotApplicationRequestRequestTypeDef]
    ) -> UpdateRobotApplicationResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/update_robot_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#update_robot_application)
        """

    def update_simulation_application(
        self, **kwargs: Unpack[UpdateSimulationApplicationRequestRequestTypeDef]
    ) -> UpdateSimulationApplicationResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/update_simulation_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#update_simulation_application)
        """

    def update_world_template(
        self, **kwargs: Unpack[UpdateWorldTemplateRequestRequestTypeDef]
    ) -> UpdateWorldTemplateResponseTypeDef:
        """
        End of support notice: On September 10, 2025, Amazon Web Services will
        discontinue support for Amazon Web Services RoboMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/update_world_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#update_world_template)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployment_jobs"]
    ) -> ListDeploymentJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_fleets"]) -> ListFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_robot_applications"]
    ) -> ListRobotApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_robots"]) -> ListRobotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_simulation_applications"]
    ) -> ListSimulationApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_simulation_job_batches"]
    ) -> ListSimulationJobBatchesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_simulation_jobs"]
    ) -> ListSimulationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_world_export_jobs"]
    ) -> ListWorldExportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_world_generation_jobs"]
    ) -> ListWorldGenerationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_world_templates"]
    ) -> ListWorldTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_worlds"]) -> ListWorldsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_robomaker/client/#get_paginator)
        """
