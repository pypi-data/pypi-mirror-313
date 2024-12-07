"""
Type annotations for batch service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_batch.client import BatchClient

    session = Session()
    client: BatchClient = session.client("batch")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeComputeEnvironmentsPaginator,
    DescribeJobDefinitionsPaginator,
    DescribeJobQueuesPaginator,
    ListJobsPaginator,
    ListSchedulingPoliciesPaginator,
)
from .type_defs import (
    CancelJobRequestRequestTypeDef,
    CreateComputeEnvironmentRequestRequestTypeDef,
    CreateComputeEnvironmentResponseTypeDef,
    CreateJobQueueRequestRequestTypeDef,
    CreateJobQueueResponseTypeDef,
    CreateSchedulingPolicyRequestRequestTypeDef,
    CreateSchedulingPolicyResponseTypeDef,
    DeleteComputeEnvironmentRequestRequestTypeDef,
    DeleteJobQueueRequestRequestTypeDef,
    DeleteSchedulingPolicyRequestRequestTypeDef,
    DeregisterJobDefinitionRequestRequestTypeDef,
    DescribeComputeEnvironmentsRequestRequestTypeDef,
    DescribeComputeEnvironmentsResponseTypeDef,
    DescribeJobDefinitionsRequestRequestTypeDef,
    DescribeJobDefinitionsResponseTypeDef,
    DescribeJobQueuesRequestRequestTypeDef,
    DescribeJobQueuesResponseTypeDef,
    DescribeJobsRequestRequestTypeDef,
    DescribeJobsResponseTypeDef,
    DescribeSchedulingPoliciesRequestRequestTypeDef,
    DescribeSchedulingPoliciesResponseTypeDef,
    GetJobQueueSnapshotRequestRequestTypeDef,
    GetJobQueueSnapshotResponseTypeDef,
    ListJobsRequestRequestTypeDef,
    ListJobsResponseTypeDef,
    ListSchedulingPoliciesRequestRequestTypeDef,
    ListSchedulingPoliciesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterJobDefinitionRequestRequestTypeDef,
    RegisterJobDefinitionResponseTypeDef,
    SubmitJobRequestRequestTypeDef,
    SubmitJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    TerminateJobRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateComputeEnvironmentRequestRequestTypeDef,
    UpdateComputeEnvironmentResponseTypeDef,
    UpdateJobQueueRequestRequestTypeDef,
    UpdateJobQueueResponseTypeDef,
    UpdateSchedulingPolicyRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("BatchClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ClientException: Type[BotocoreClientError]
    ServerException: Type[BotocoreClientError]


class BatchClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BatchClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#close)
        """

    def cancel_job(self, **kwargs: Unpack[CancelJobRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Cancels a job in an Batch job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/cancel_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#cancel_job)
        """

    def create_compute_environment(
        self, **kwargs: Unpack[CreateComputeEnvironmentRequestRequestTypeDef]
    ) -> CreateComputeEnvironmentResponseTypeDef:
        """
        Creates an Batch compute environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/create_compute_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#create_compute_environment)
        """

    def create_job_queue(
        self, **kwargs: Unpack[CreateJobQueueRequestRequestTypeDef]
    ) -> CreateJobQueueResponseTypeDef:
        """
        Creates an Batch job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/create_job_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#create_job_queue)
        """

    def create_scheduling_policy(
        self, **kwargs: Unpack[CreateSchedulingPolicyRequestRequestTypeDef]
    ) -> CreateSchedulingPolicyResponseTypeDef:
        """
        Creates an Batch scheduling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/create_scheduling_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#create_scheduling_policy)
        """

    def delete_compute_environment(
        self, **kwargs: Unpack[DeleteComputeEnvironmentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Batch compute environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/delete_compute_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#delete_compute_environment)
        """

    def delete_job_queue(
        self, **kwargs: Unpack[DeleteJobQueueRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/delete_job_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#delete_job_queue)
        """

    def delete_scheduling_policy(
        self, **kwargs: Unpack[DeleteSchedulingPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified scheduling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/delete_scheduling_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#delete_scheduling_policy)
        """

    def deregister_job_definition(
        self, **kwargs: Unpack[DeregisterJobDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deregisters an Batch job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/deregister_job_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#deregister_job_definition)
        """

    def describe_compute_environments(
        self, **kwargs: Unpack[DescribeComputeEnvironmentsRequestRequestTypeDef]
    ) -> DescribeComputeEnvironmentsResponseTypeDef:
        """
        Describes one or more of your compute environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/describe_compute_environments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#describe_compute_environments)
        """

    def describe_job_definitions(
        self, **kwargs: Unpack[DescribeJobDefinitionsRequestRequestTypeDef]
    ) -> DescribeJobDefinitionsResponseTypeDef:
        """
        Describes a list of job definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/describe_job_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#describe_job_definitions)
        """

    def describe_job_queues(
        self, **kwargs: Unpack[DescribeJobQueuesRequestRequestTypeDef]
    ) -> DescribeJobQueuesResponseTypeDef:
        """
        Describes one or more of your job queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/describe_job_queues.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#describe_job_queues)
        """

    def describe_jobs(
        self, **kwargs: Unpack[DescribeJobsRequestRequestTypeDef]
    ) -> DescribeJobsResponseTypeDef:
        """
        Describes a list of Batch jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/describe_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#describe_jobs)
        """

    def describe_scheduling_policies(
        self, **kwargs: Unpack[DescribeSchedulingPoliciesRequestRequestTypeDef]
    ) -> DescribeSchedulingPoliciesResponseTypeDef:
        """
        Describes one or more of your scheduling policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/describe_scheduling_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#describe_scheduling_policies)
        """

    def get_job_queue_snapshot(
        self, **kwargs: Unpack[GetJobQueueSnapshotRequestRequestTypeDef]
    ) -> GetJobQueueSnapshotResponseTypeDef:
        """
        Provides a list of the first 100 <code>RUNNABLE</code> jobs associated to a
        single job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_job_queue_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#get_job_queue_snapshot)
        """

    def list_jobs(self, **kwargs: Unpack[ListJobsRequestRequestTypeDef]) -> ListJobsResponseTypeDef:
        """
        Returns a list of Batch jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/list_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#list_jobs)
        """

    def list_scheduling_policies(
        self, **kwargs: Unpack[ListSchedulingPoliciesRequestRequestTypeDef]
    ) -> ListSchedulingPoliciesResponseTypeDef:
        """
        Returns a list of Batch scheduling policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/list_scheduling_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#list_scheduling_policies)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for an Batch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#list_tags_for_resource)
        """

    def register_job_definition(
        self, **kwargs: Unpack[RegisterJobDefinitionRequestRequestTypeDef]
    ) -> RegisterJobDefinitionResponseTypeDef:
        """
        Registers an Batch job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/register_job_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#register_job_definition)
        """

    def submit_job(
        self, **kwargs: Unpack[SubmitJobRequestRequestTypeDef]
    ) -> SubmitJobResponseTypeDef:
        """
        Submits an Batch job from a job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/submit_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#submit_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified
        <code>resourceArn</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#tag_resource)
        """

    def terminate_job(self, **kwargs: Unpack[TerminateJobRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Terminates a job in a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/terminate_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#terminate_job)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes specified tags from an Batch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#untag_resource)
        """

    def update_compute_environment(
        self, **kwargs: Unpack[UpdateComputeEnvironmentRequestRequestTypeDef]
    ) -> UpdateComputeEnvironmentResponseTypeDef:
        """
        Updates an Batch compute environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/update_compute_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#update_compute_environment)
        """

    def update_job_queue(
        self, **kwargs: Unpack[UpdateJobQueueRequestRequestTypeDef]
    ) -> UpdateJobQueueResponseTypeDef:
        """
        Updates a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/update_job_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#update_job_queue)
        """

    def update_scheduling_policy(
        self, **kwargs: Unpack[UpdateSchedulingPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a scheduling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/update_scheduling_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#update_scheduling_policy)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_compute_environments"]
    ) -> DescribeComputeEnvironmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_job_definitions"]
    ) -> DescribeJobDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_job_queues"]
    ) -> DescribeJobQueuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_scheduling_policies"]
    ) -> ListSchedulingPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_batch/client/#get_paginator)
        """
