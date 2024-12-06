"""
Type annotations for deadline service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_deadline.client import DeadlineCloudClient

    session = Session()
    client: DeadlineCloudClient = session.client("deadline")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetSessionsStatisticsAggregationPaginator,
    ListAvailableMeteredProductsPaginator,
    ListBudgetsPaginator,
    ListFarmMembersPaginator,
    ListFarmsPaginator,
    ListFleetMembersPaginator,
    ListFleetsPaginator,
    ListJobMembersPaginator,
    ListJobParameterDefinitionsPaginator,
    ListJobsPaginator,
    ListLicenseEndpointsPaginator,
    ListMeteredProductsPaginator,
    ListMonitorsPaginator,
    ListQueueEnvironmentsPaginator,
    ListQueueFleetAssociationsPaginator,
    ListQueueMembersPaginator,
    ListQueuesPaginator,
    ListSessionActionsPaginator,
    ListSessionsForWorkerPaginator,
    ListSessionsPaginator,
    ListStepConsumersPaginator,
    ListStepDependenciesPaginator,
    ListStepsPaginator,
    ListStorageProfilesForQueuePaginator,
    ListStorageProfilesPaginator,
    ListTasksPaginator,
    ListWorkersPaginator,
)
from .type_defs import (
    AssociateMemberToFarmRequestRequestTypeDef,
    AssociateMemberToFleetRequestRequestTypeDef,
    AssociateMemberToJobRequestRequestTypeDef,
    AssociateMemberToQueueRequestRequestTypeDef,
    AssumeFleetRoleForReadRequestRequestTypeDef,
    AssumeFleetRoleForReadResponseTypeDef,
    AssumeFleetRoleForWorkerRequestRequestTypeDef,
    AssumeFleetRoleForWorkerResponseTypeDef,
    AssumeQueueRoleForReadRequestRequestTypeDef,
    AssumeQueueRoleForReadResponseTypeDef,
    AssumeQueueRoleForUserRequestRequestTypeDef,
    AssumeQueueRoleForUserResponseTypeDef,
    AssumeQueueRoleForWorkerRequestRequestTypeDef,
    AssumeQueueRoleForWorkerResponseTypeDef,
    BatchGetJobEntityRequestRequestTypeDef,
    BatchGetJobEntityResponseTypeDef,
    CopyJobTemplateRequestRequestTypeDef,
    CopyJobTemplateResponseTypeDef,
    CreateBudgetRequestRequestTypeDef,
    CreateBudgetResponseTypeDef,
    CreateFarmRequestRequestTypeDef,
    CreateFarmResponseTypeDef,
    CreateFleetRequestRequestTypeDef,
    CreateFleetResponseTypeDef,
    CreateJobRequestRequestTypeDef,
    CreateJobResponseTypeDef,
    CreateLicenseEndpointRequestRequestTypeDef,
    CreateLicenseEndpointResponseTypeDef,
    CreateMonitorRequestRequestTypeDef,
    CreateMonitorResponseTypeDef,
    CreateQueueEnvironmentRequestRequestTypeDef,
    CreateQueueEnvironmentResponseTypeDef,
    CreateQueueFleetAssociationRequestRequestTypeDef,
    CreateQueueRequestRequestTypeDef,
    CreateQueueResponseTypeDef,
    CreateStorageProfileRequestRequestTypeDef,
    CreateStorageProfileResponseTypeDef,
    CreateWorkerRequestRequestTypeDef,
    CreateWorkerResponseTypeDef,
    DeleteBudgetRequestRequestTypeDef,
    DeleteFarmRequestRequestTypeDef,
    DeleteFleetRequestRequestTypeDef,
    DeleteLicenseEndpointRequestRequestTypeDef,
    DeleteMeteredProductRequestRequestTypeDef,
    DeleteMonitorRequestRequestTypeDef,
    DeleteQueueEnvironmentRequestRequestTypeDef,
    DeleteQueueFleetAssociationRequestRequestTypeDef,
    DeleteQueueRequestRequestTypeDef,
    DeleteStorageProfileRequestRequestTypeDef,
    DeleteWorkerRequestRequestTypeDef,
    DisassociateMemberFromFarmRequestRequestTypeDef,
    DisassociateMemberFromFleetRequestRequestTypeDef,
    DisassociateMemberFromJobRequestRequestTypeDef,
    DisassociateMemberFromQueueRequestRequestTypeDef,
    GetBudgetRequestRequestTypeDef,
    GetBudgetResponseTypeDef,
    GetFarmRequestRequestTypeDef,
    GetFarmResponseTypeDef,
    GetFleetRequestRequestTypeDef,
    GetFleetResponseTypeDef,
    GetJobRequestRequestTypeDef,
    GetJobResponseTypeDef,
    GetLicenseEndpointRequestRequestTypeDef,
    GetLicenseEndpointResponseTypeDef,
    GetMonitorRequestRequestTypeDef,
    GetMonitorResponseTypeDef,
    GetQueueEnvironmentRequestRequestTypeDef,
    GetQueueEnvironmentResponseTypeDef,
    GetQueueFleetAssociationRequestRequestTypeDef,
    GetQueueFleetAssociationResponseTypeDef,
    GetQueueRequestRequestTypeDef,
    GetQueueResponseTypeDef,
    GetSessionActionRequestRequestTypeDef,
    GetSessionActionResponseTypeDef,
    GetSessionRequestRequestTypeDef,
    GetSessionResponseTypeDef,
    GetSessionsStatisticsAggregationRequestRequestTypeDef,
    GetSessionsStatisticsAggregationResponseTypeDef,
    GetStepRequestRequestTypeDef,
    GetStepResponseTypeDef,
    GetStorageProfileForQueueRequestRequestTypeDef,
    GetStorageProfileForQueueResponseTypeDef,
    GetStorageProfileRequestRequestTypeDef,
    GetStorageProfileResponseTypeDef,
    GetTaskRequestRequestTypeDef,
    GetTaskResponseTypeDef,
    GetWorkerRequestRequestTypeDef,
    GetWorkerResponseTypeDef,
    ListAvailableMeteredProductsRequestRequestTypeDef,
    ListAvailableMeteredProductsResponseTypeDef,
    ListBudgetsRequestRequestTypeDef,
    ListBudgetsResponseTypeDef,
    ListFarmMembersRequestRequestTypeDef,
    ListFarmMembersResponseTypeDef,
    ListFarmsRequestRequestTypeDef,
    ListFarmsResponseTypeDef,
    ListFleetMembersRequestRequestTypeDef,
    ListFleetMembersResponseTypeDef,
    ListFleetsRequestRequestTypeDef,
    ListFleetsResponseTypeDef,
    ListJobMembersRequestRequestTypeDef,
    ListJobMembersResponseTypeDef,
    ListJobParameterDefinitionsRequestRequestTypeDef,
    ListJobParameterDefinitionsResponseTypeDef,
    ListJobsRequestRequestTypeDef,
    ListJobsResponseTypeDef,
    ListLicenseEndpointsRequestRequestTypeDef,
    ListLicenseEndpointsResponseTypeDef,
    ListMeteredProductsRequestRequestTypeDef,
    ListMeteredProductsResponseTypeDef,
    ListMonitorsRequestRequestTypeDef,
    ListMonitorsResponseTypeDef,
    ListQueueEnvironmentsRequestRequestTypeDef,
    ListQueueEnvironmentsResponseTypeDef,
    ListQueueFleetAssociationsRequestRequestTypeDef,
    ListQueueFleetAssociationsResponseTypeDef,
    ListQueueMembersRequestRequestTypeDef,
    ListQueueMembersResponseTypeDef,
    ListQueuesRequestRequestTypeDef,
    ListQueuesResponseTypeDef,
    ListSessionActionsRequestRequestTypeDef,
    ListSessionActionsResponseTypeDef,
    ListSessionsForWorkerRequestRequestTypeDef,
    ListSessionsForWorkerResponseTypeDef,
    ListSessionsRequestRequestTypeDef,
    ListSessionsResponseTypeDef,
    ListStepConsumersRequestRequestTypeDef,
    ListStepConsumersResponseTypeDef,
    ListStepDependenciesRequestRequestTypeDef,
    ListStepDependenciesResponseTypeDef,
    ListStepsRequestRequestTypeDef,
    ListStepsResponseTypeDef,
    ListStorageProfilesForQueueRequestRequestTypeDef,
    ListStorageProfilesForQueueResponseTypeDef,
    ListStorageProfilesRequestRequestTypeDef,
    ListStorageProfilesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTasksRequestRequestTypeDef,
    ListTasksResponseTypeDef,
    ListWorkersRequestRequestTypeDef,
    ListWorkersResponseTypeDef,
    PutMeteredProductRequestRequestTypeDef,
    SearchJobsRequestRequestTypeDef,
    SearchJobsResponseTypeDef,
    SearchStepsRequestRequestTypeDef,
    SearchStepsResponseTypeDef,
    SearchTasksRequestRequestTypeDef,
    SearchTasksResponseTypeDef,
    SearchWorkersRequestRequestTypeDef,
    SearchWorkersResponseTypeDef,
    StartSessionsStatisticsAggregationRequestRequestTypeDef,
    StartSessionsStatisticsAggregationResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateBudgetRequestRequestTypeDef,
    UpdateFarmRequestRequestTypeDef,
    UpdateFleetRequestRequestTypeDef,
    UpdateJobRequestRequestTypeDef,
    UpdateMonitorRequestRequestTypeDef,
    UpdateQueueEnvironmentRequestRequestTypeDef,
    UpdateQueueFleetAssociationRequestRequestTypeDef,
    UpdateQueueRequestRequestTypeDef,
    UpdateSessionRequestRequestTypeDef,
    UpdateStepRequestRequestTypeDef,
    UpdateStorageProfileRequestRequestTypeDef,
    UpdateTaskRequestRequestTypeDef,
    UpdateWorkerRequestRequestTypeDef,
    UpdateWorkerResponseTypeDef,
    UpdateWorkerScheduleRequestRequestTypeDef,
    UpdateWorkerScheduleResponseTypeDef,
)
from .waiter import (
    FleetActiveWaiter,
    JobCreateCompleteWaiter,
    LicenseEndpointDeletedWaiter,
    LicenseEndpointValidWaiter,
    QueueFleetAssociationStoppedWaiter,
    QueueSchedulingBlockedWaiter,
    QueueSchedulingWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("DeadlineCloudClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class DeadlineCloudClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DeadlineCloudClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#close)
        """

    def associate_member_to_farm(
        self, **kwargs: Unpack[AssociateMemberToFarmRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Assigns a farm membership level to a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/associate_member_to_farm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#associate_member_to_farm)
        """

    def associate_member_to_fleet(
        self, **kwargs: Unpack[AssociateMemberToFleetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Assigns a fleet membership level to a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/associate_member_to_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#associate_member_to_fleet)
        """

    def associate_member_to_job(
        self, **kwargs: Unpack[AssociateMemberToJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Assigns a job membership level to a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/associate_member_to_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#associate_member_to_job)
        """

    def associate_member_to_queue(
        self, **kwargs: Unpack[AssociateMemberToQueueRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Assigns a queue membership level to a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/associate_member_to_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#associate_member_to_queue)
        """

    def assume_fleet_role_for_read(
        self, **kwargs: Unpack[AssumeFleetRoleForReadRequestRequestTypeDef]
    ) -> AssumeFleetRoleForReadResponseTypeDef:
        """
        Get Amazon Web Services credentials from the fleet role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/assume_fleet_role_for_read.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#assume_fleet_role_for_read)
        """

    def assume_fleet_role_for_worker(
        self, **kwargs: Unpack[AssumeFleetRoleForWorkerRequestRequestTypeDef]
    ) -> AssumeFleetRoleForWorkerResponseTypeDef:
        """
        Get credentials from the fleet role for a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/assume_fleet_role_for_worker.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#assume_fleet_role_for_worker)
        """

    def assume_queue_role_for_read(
        self, **kwargs: Unpack[AssumeQueueRoleForReadRequestRequestTypeDef]
    ) -> AssumeQueueRoleForReadResponseTypeDef:
        """
        Gets Amazon Web Services credentials from the queue role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/assume_queue_role_for_read.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#assume_queue_role_for_read)
        """

    def assume_queue_role_for_user(
        self, **kwargs: Unpack[AssumeQueueRoleForUserRequestRequestTypeDef]
    ) -> AssumeQueueRoleForUserResponseTypeDef:
        """
        Allows a user to assume a role for a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/assume_queue_role_for_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#assume_queue_role_for_user)
        """

    def assume_queue_role_for_worker(
        self, **kwargs: Unpack[AssumeQueueRoleForWorkerRequestRequestTypeDef]
    ) -> AssumeQueueRoleForWorkerResponseTypeDef:
        """
        Allows a worker to assume a queue role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/assume_queue_role_for_worker.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#assume_queue_role_for_worker)
        """

    def batch_get_job_entity(
        self, **kwargs: Unpack[BatchGetJobEntityRequestRequestTypeDef]
    ) -> BatchGetJobEntityResponseTypeDef:
        """
        Get batched job details for a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/batch_get_job_entity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#batch_get_job_entity)
        """

    def copy_job_template(
        self, **kwargs: Unpack[CopyJobTemplateRequestRequestTypeDef]
    ) -> CopyJobTemplateResponseTypeDef:
        """
        Copies a job template to an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/copy_job_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#copy_job_template)
        """

    def create_budget(
        self, **kwargs: Unpack[CreateBudgetRequestRequestTypeDef]
    ) -> CreateBudgetResponseTypeDef:
        """
        Creates a budget to set spending thresholds for your rendering activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/create_budget.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#create_budget)
        """

    def create_farm(
        self, **kwargs: Unpack[CreateFarmRequestRequestTypeDef]
    ) -> CreateFarmResponseTypeDef:
        """
        Creates a farm to allow space for queues and fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/create_farm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#create_farm)
        """

    def create_fleet(
        self, **kwargs: Unpack[CreateFleetRequestRequestTypeDef]
    ) -> CreateFleetResponseTypeDef:
        """
        Creates a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/create_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#create_fleet)
        """

    def create_job(
        self, **kwargs: Unpack[CreateJobRequestRequestTypeDef]
    ) -> CreateJobResponseTypeDef:
        """
        Creates a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/create_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#create_job)
        """

    def create_license_endpoint(
        self, **kwargs: Unpack[CreateLicenseEndpointRequestRequestTypeDef]
    ) -> CreateLicenseEndpointResponseTypeDef:
        """
        Creates a license endpoint to integrate your various licensed software used for
        rendering on Deadline Cloud.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/create_license_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#create_license_endpoint)
        """

    def create_monitor(
        self, **kwargs: Unpack[CreateMonitorRequestRequestTypeDef]
    ) -> CreateMonitorResponseTypeDef:
        """
        Creates an Amazon Web Services Deadline Cloud monitor that you can use to view
        your farms, queues, and fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/create_monitor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#create_monitor)
        """

    def create_queue(
        self, **kwargs: Unpack[CreateQueueRequestRequestTypeDef]
    ) -> CreateQueueResponseTypeDef:
        """
        Creates a queue to coordinate the order in which jobs run on a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/create_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#create_queue)
        """

    def create_queue_environment(
        self, **kwargs: Unpack[CreateQueueEnvironmentRequestRequestTypeDef]
    ) -> CreateQueueEnvironmentResponseTypeDef:
        """
        Creates an environment for a queue that defines how jobs in the queue run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/create_queue_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#create_queue_environment)
        """

    def create_queue_fleet_association(
        self, **kwargs: Unpack[CreateQueueFleetAssociationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates an association between a queue and a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/create_queue_fleet_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#create_queue_fleet_association)
        """

    def create_storage_profile(
        self, **kwargs: Unpack[CreateStorageProfileRequestRequestTypeDef]
    ) -> CreateStorageProfileResponseTypeDef:
        """
        Creates a storage profile that specifies the operating system, file type, and
        file location of resources used on a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/create_storage_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#create_storage_profile)
        """

    def create_worker(
        self, **kwargs: Unpack[CreateWorkerRequestRequestTypeDef]
    ) -> CreateWorkerResponseTypeDef:
        """
        Creates a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/create_worker.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#create_worker)
        """

    def delete_budget(self, **kwargs: Unpack[DeleteBudgetRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/delete_budget.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#delete_budget)
        """

    def delete_farm(self, **kwargs: Unpack[DeleteFarmRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/delete_farm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#delete_farm)
        """

    def delete_fleet(self, **kwargs: Unpack[DeleteFleetRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/delete_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#delete_fleet)
        """

    def delete_license_endpoint(
        self, **kwargs: Unpack[DeleteLicenseEndpointRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a license endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/delete_license_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#delete_license_endpoint)
        """

    def delete_metered_product(
        self, **kwargs: Unpack[DeleteMeteredProductRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a metered product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/delete_metered_product.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#delete_metered_product)
        """

    def delete_monitor(
        self, **kwargs: Unpack[DeleteMonitorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a Deadline Cloud monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/delete_monitor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#delete_monitor)
        """

    def delete_queue(self, **kwargs: Unpack[DeleteQueueRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/delete_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#delete_queue)
        """

    def delete_queue_environment(
        self, **kwargs: Unpack[DeleteQueueEnvironmentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a queue environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/delete_queue_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#delete_queue_environment)
        """

    def delete_queue_fleet_association(
        self, **kwargs: Unpack[DeleteQueueFleetAssociationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a queue-fleet association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/delete_queue_fleet_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#delete_queue_fleet_association)
        """

    def delete_storage_profile(
        self, **kwargs: Unpack[DeleteStorageProfileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a storage profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/delete_storage_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#delete_storage_profile)
        """

    def delete_worker(self, **kwargs: Unpack[DeleteWorkerRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/delete_worker.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#delete_worker)
        """

    def disassociate_member_from_farm(
        self, **kwargs: Unpack[DisassociateMemberFromFarmRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a member from a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/disassociate_member_from_farm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#disassociate_member_from_farm)
        """

    def disassociate_member_from_fleet(
        self, **kwargs: Unpack[DisassociateMemberFromFleetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a member from a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/disassociate_member_from_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#disassociate_member_from_fleet)
        """

    def disassociate_member_from_job(
        self, **kwargs: Unpack[DisassociateMemberFromJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a member from a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/disassociate_member_from_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#disassociate_member_from_job)
        """

    def disassociate_member_from_queue(
        self, **kwargs: Unpack[DisassociateMemberFromQueueRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a member from a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/disassociate_member_from_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#disassociate_member_from_queue)
        """

    def get_budget(
        self, **kwargs: Unpack[GetBudgetRequestRequestTypeDef]
    ) -> GetBudgetResponseTypeDef:
        """
        Get a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_budget.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_budget)
        """

    def get_farm(self, **kwargs: Unpack[GetFarmRequestRequestTypeDef]) -> GetFarmResponseTypeDef:
        """
        Get a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_farm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_farm)
        """

    def get_fleet(self, **kwargs: Unpack[GetFleetRequestRequestTypeDef]) -> GetFleetResponseTypeDef:
        """
        Get a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_fleet)
        """

    def get_job(self, **kwargs: Unpack[GetJobRequestRequestTypeDef]) -> GetJobResponseTypeDef:
        """
        Gets a Deadline Cloud job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_job)
        """

    def get_license_endpoint(
        self, **kwargs: Unpack[GetLicenseEndpointRequestRequestTypeDef]
    ) -> GetLicenseEndpointResponseTypeDef:
        """
        Gets a licence endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_license_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_license_endpoint)
        """

    def get_monitor(
        self, **kwargs: Unpack[GetMonitorRequestRequestTypeDef]
    ) -> GetMonitorResponseTypeDef:
        """
        Gets information about the specified monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_monitor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_monitor)
        """

    def get_queue(self, **kwargs: Unpack[GetQueueRequestRequestTypeDef]) -> GetQueueResponseTypeDef:
        """
        Gets a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_queue)
        """

    def get_queue_environment(
        self, **kwargs: Unpack[GetQueueEnvironmentRequestRequestTypeDef]
    ) -> GetQueueEnvironmentResponseTypeDef:
        """
        Gets a queue environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_queue_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_queue_environment)
        """

    def get_queue_fleet_association(
        self, **kwargs: Unpack[GetQueueFleetAssociationRequestRequestTypeDef]
    ) -> GetQueueFleetAssociationResponseTypeDef:
        """
        Gets a queue-fleet association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_queue_fleet_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_queue_fleet_association)
        """

    def get_session(
        self, **kwargs: Unpack[GetSessionRequestRequestTypeDef]
    ) -> GetSessionResponseTypeDef:
        """
        Gets a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_session)
        """

    def get_session_action(
        self, **kwargs: Unpack[GetSessionActionRequestRequestTypeDef]
    ) -> GetSessionActionResponseTypeDef:
        """
        Gets a session action for the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_session_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_session_action)
        """

    def get_sessions_statistics_aggregation(
        self, **kwargs: Unpack[GetSessionsStatisticsAggregationRequestRequestTypeDef]
    ) -> GetSessionsStatisticsAggregationResponseTypeDef:
        """
        Gets a set of statistics for queues or farms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_sessions_statistics_aggregation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_sessions_statistics_aggregation)
        """

    def get_step(self, **kwargs: Unpack[GetStepRequestRequestTypeDef]) -> GetStepResponseTypeDef:
        """
        Gets a step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_step.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_step)
        """

    def get_storage_profile(
        self, **kwargs: Unpack[GetStorageProfileRequestRequestTypeDef]
    ) -> GetStorageProfileResponseTypeDef:
        """
        Gets a storage profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_storage_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_storage_profile)
        """

    def get_storage_profile_for_queue(
        self, **kwargs: Unpack[GetStorageProfileForQueueRequestRequestTypeDef]
    ) -> GetStorageProfileForQueueResponseTypeDef:
        """
        Gets a storage profile for a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_storage_profile_for_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_storage_profile_for_queue)
        """

    def get_task(self, **kwargs: Unpack[GetTaskRequestRequestTypeDef]) -> GetTaskResponseTypeDef:
        """
        Gets a task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_task)
        """

    def get_worker(
        self, **kwargs: Unpack[GetWorkerRequestRequestTypeDef]
    ) -> GetWorkerResponseTypeDef:
        """
        Gets a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_worker.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_worker)
        """

    def list_available_metered_products(
        self, **kwargs: Unpack[ListAvailableMeteredProductsRequestRequestTypeDef]
    ) -> ListAvailableMeteredProductsResponseTypeDef:
        """
        A list of the available metered products.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_available_metered_products.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_available_metered_products)
        """

    def list_budgets(
        self, **kwargs: Unpack[ListBudgetsRequestRequestTypeDef]
    ) -> ListBudgetsResponseTypeDef:
        """
        A list of budgets in a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_budgets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_budgets)
        """

    def list_farm_members(
        self, **kwargs: Unpack[ListFarmMembersRequestRequestTypeDef]
    ) -> ListFarmMembersResponseTypeDef:
        """
        Lists the members of a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_farm_members.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_farm_members)
        """

    def list_farms(
        self, **kwargs: Unpack[ListFarmsRequestRequestTypeDef]
    ) -> ListFarmsResponseTypeDef:
        """
        Lists farms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_farms.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_farms)
        """

    def list_fleet_members(
        self, **kwargs: Unpack[ListFleetMembersRequestRequestTypeDef]
    ) -> ListFleetMembersResponseTypeDef:
        """
        Lists fleet members.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_fleet_members.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_fleet_members)
        """

    def list_fleets(
        self, **kwargs: Unpack[ListFleetsRequestRequestTypeDef]
    ) -> ListFleetsResponseTypeDef:
        """
        Lists fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_fleets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_fleets)
        """

    def list_job_members(
        self, **kwargs: Unpack[ListJobMembersRequestRequestTypeDef]
    ) -> ListJobMembersResponseTypeDef:
        """
        Lists members on a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_job_members.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_job_members)
        """

    def list_job_parameter_definitions(
        self, **kwargs: Unpack[ListJobParameterDefinitionsRequestRequestTypeDef]
    ) -> ListJobParameterDefinitionsResponseTypeDef:
        """
        Lists parameter definitions of a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_job_parameter_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_job_parameter_definitions)
        """

    def list_jobs(self, **kwargs: Unpack[ListJobsRequestRequestTypeDef]) -> ListJobsResponseTypeDef:
        """
        Lists jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_jobs)
        """

    def list_license_endpoints(
        self, **kwargs: Unpack[ListLicenseEndpointsRequestRequestTypeDef]
    ) -> ListLicenseEndpointsResponseTypeDef:
        """
        Lists license endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_license_endpoints.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_license_endpoints)
        """

    def list_metered_products(
        self, **kwargs: Unpack[ListMeteredProductsRequestRequestTypeDef]
    ) -> ListMeteredProductsResponseTypeDef:
        """
        Lists metered products.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_metered_products.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_metered_products)
        """

    def list_monitors(
        self, **kwargs: Unpack[ListMonitorsRequestRequestTypeDef]
    ) -> ListMonitorsResponseTypeDef:
        """
        Gets a list of your monitors in Deadline Cloud.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_monitors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_monitors)
        """

    def list_queue_environments(
        self, **kwargs: Unpack[ListQueueEnvironmentsRequestRequestTypeDef]
    ) -> ListQueueEnvironmentsResponseTypeDef:
        """
        Lists queue environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_queue_environments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_queue_environments)
        """

    def list_queue_fleet_associations(
        self, **kwargs: Unpack[ListQueueFleetAssociationsRequestRequestTypeDef]
    ) -> ListQueueFleetAssociationsResponseTypeDef:
        """
        Lists queue-fleet associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_queue_fleet_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_queue_fleet_associations)
        """

    def list_queue_members(
        self, **kwargs: Unpack[ListQueueMembersRequestRequestTypeDef]
    ) -> ListQueueMembersResponseTypeDef:
        """
        Lists the members in a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_queue_members.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_queue_members)
        """

    def list_queues(
        self, **kwargs: Unpack[ListQueuesRequestRequestTypeDef]
    ) -> ListQueuesResponseTypeDef:
        """
        Lists queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_queues.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_queues)
        """

    def list_session_actions(
        self, **kwargs: Unpack[ListSessionActionsRequestRequestTypeDef]
    ) -> ListSessionActionsResponseTypeDef:
        """
        Lists session actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_session_actions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_session_actions)
        """

    def list_sessions(
        self, **kwargs: Unpack[ListSessionsRequestRequestTypeDef]
    ) -> ListSessionsResponseTypeDef:
        """
        Lists sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_sessions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_sessions)
        """

    def list_sessions_for_worker(
        self, **kwargs: Unpack[ListSessionsForWorkerRequestRequestTypeDef]
    ) -> ListSessionsForWorkerResponseTypeDef:
        """
        Lists sessions for a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_sessions_for_worker.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_sessions_for_worker)
        """

    def list_step_consumers(
        self, **kwargs: Unpack[ListStepConsumersRequestRequestTypeDef]
    ) -> ListStepConsumersResponseTypeDef:
        """
        Lists step consumers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_step_consumers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_step_consumers)
        """

    def list_step_dependencies(
        self, **kwargs: Unpack[ListStepDependenciesRequestRequestTypeDef]
    ) -> ListStepDependenciesResponseTypeDef:
        """
        Lists the dependencies for a step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_step_dependencies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_step_dependencies)
        """

    def list_steps(
        self, **kwargs: Unpack[ListStepsRequestRequestTypeDef]
    ) -> ListStepsResponseTypeDef:
        """
        Lists steps for a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_steps.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_steps)
        """

    def list_storage_profiles(
        self, **kwargs: Unpack[ListStorageProfilesRequestRequestTypeDef]
    ) -> ListStorageProfilesResponseTypeDef:
        """
        Lists storage profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_storage_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_storage_profiles)
        """

    def list_storage_profiles_for_queue(
        self, **kwargs: Unpack[ListStorageProfilesForQueueRequestRequestTypeDef]
    ) -> ListStorageProfilesForQueueResponseTypeDef:
        """
        Lists storage profiles for a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_storage_profiles_for_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_storage_profiles_for_queue)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_tags_for_resource)
        """

    def list_tasks(
        self, **kwargs: Unpack[ListTasksRequestRequestTypeDef]
    ) -> ListTasksResponseTypeDef:
        """
        Lists tasks for a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_tasks)
        """

    def list_workers(
        self, **kwargs: Unpack[ListWorkersRequestRequestTypeDef]
    ) -> ListWorkersResponseTypeDef:
        """
        Lists workers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/list_workers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#list_workers)
        """

    def put_metered_product(
        self, **kwargs: Unpack[PutMeteredProductRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds a metered product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/put_metered_product.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#put_metered_product)
        """

    def search_jobs(
        self, **kwargs: Unpack[SearchJobsRequestRequestTypeDef]
    ) -> SearchJobsResponseTypeDef:
        """
        Searches for jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/search_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#search_jobs)
        """

    def search_steps(
        self, **kwargs: Unpack[SearchStepsRequestRequestTypeDef]
    ) -> SearchStepsResponseTypeDef:
        """
        Searches for steps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/search_steps.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#search_steps)
        """

    def search_tasks(
        self, **kwargs: Unpack[SearchTasksRequestRequestTypeDef]
    ) -> SearchTasksResponseTypeDef:
        """
        Searches for tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/search_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#search_tasks)
        """

    def search_workers(
        self, **kwargs: Unpack[SearchWorkersRequestRequestTypeDef]
    ) -> SearchWorkersResponseTypeDef:
        """
        Searches for workers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/search_workers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#search_workers)
        """

    def start_sessions_statistics_aggregation(
        self, **kwargs: Unpack[StartSessionsStatisticsAggregationRequestRequestTypeDef]
    ) -> StartSessionsStatisticsAggregationResponseTypeDef:
        """
        Starts an asynchronous request for getting aggregated statistics about queues
        and farms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/start_sessions_statistics_aggregation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#start_sessions_statistics_aggregation)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags a resource using the resource's ARN and desired tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag from a resource using the resource's ARN and tag to remove.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#untag_resource)
        """

    def update_budget(self, **kwargs: Unpack[UpdateBudgetRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a budget that sets spending thresholds for rendering activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_budget.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_budget)
        """

    def update_farm(self, **kwargs: Unpack[UpdateFarmRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_farm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_farm)
        """

    def update_fleet(self, **kwargs: Unpack[UpdateFleetRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_fleet)
        """

    def update_job(self, **kwargs: Unpack[UpdateJobRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_job)
        """

    def update_monitor(
        self, **kwargs: Unpack[UpdateMonitorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies the settings for a Deadline Cloud monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_monitor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_monitor)
        """

    def update_queue(self, **kwargs: Unpack[UpdateQueueRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_queue)
        """

    def update_queue_environment(
        self, **kwargs: Unpack[UpdateQueueEnvironmentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the queue environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_queue_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_queue_environment)
        """

    def update_queue_fleet_association(
        self, **kwargs: Unpack[UpdateQueueFleetAssociationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a queue-fleet association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_queue_fleet_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_queue_fleet_association)
        """

    def update_session(
        self, **kwargs: Unpack[UpdateSessionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_session)
        """

    def update_step(self, **kwargs: Unpack[UpdateStepRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_step.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_step)
        """

    def update_storage_profile(
        self, **kwargs: Unpack[UpdateStorageProfileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a storage profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_storage_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_storage_profile)
        """

    def update_task(self, **kwargs: Unpack[UpdateTaskRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_task)
        """

    def update_worker(
        self, **kwargs: Unpack[UpdateWorkerRequestRequestTypeDef]
    ) -> UpdateWorkerResponseTypeDef:
        """
        Updates a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_worker.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_worker)
        """

    def update_worker_schedule(
        self, **kwargs: Unpack[UpdateWorkerScheduleRequestRequestTypeDef]
    ) -> UpdateWorkerScheduleResponseTypeDef:
        """
        Updates the schedule for a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/update_worker_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#update_worker_schedule)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_sessions_statistics_aggregation"]
    ) -> GetSessionsStatisticsAggregationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_available_metered_products"]
    ) -> ListAvailableMeteredProductsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_budgets"]) -> ListBudgetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_farm_members"]
    ) -> ListFarmMembersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_farms"]) -> ListFarmsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_fleet_members"]
    ) -> ListFleetMembersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_fleets"]) -> ListFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_job_members"]) -> ListJobMembersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_job_parameter_definitions"]
    ) -> ListJobParameterDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_license_endpoints"]
    ) -> ListLicenseEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_metered_products"]
    ) -> ListMeteredProductsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_monitors"]) -> ListMonitorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_queue_environments"]
    ) -> ListQueueEnvironmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_queue_fleet_associations"]
    ) -> ListQueueFleetAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_queue_members"]
    ) -> ListQueueMembersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_queues"]) -> ListQueuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_session_actions"]
    ) -> ListSessionActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sessions_for_worker"]
    ) -> ListSessionsForWorkerPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_sessions"]) -> ListSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_step_consumers"]
    ) -> ListStepConsumersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_step_dependencies"]
    ) -> ListStepDependenciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_steps"]) -> ListStepsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_storage_profiles_for_queue"]
    ) -> ListStorageProfilesForQueuePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_storage_profiles"]
    ) -> ListStorageProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tasks"]) -> ListTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workers"]) -> ListWorkersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["fleet_active"]) -> FleetActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["job_create_complete"]) -> JobCreateCompleteWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["license_endpoint_deleted"]
    ) -> LicenseEndpointDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["license_endpoint_valid"]
    ) -> LicenseEndpointValidWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["queue_fleet_association_stopped"]
    ) -> QueueFleetAssociationStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["queue_scheduling_blocked"]
    ) -> QueueSchedulingBlockedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["queue_scheduling"]) -> QueueSchedulingWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_deadline/client/#get_waiter)
        """
