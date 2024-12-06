"""
Type annotations for swf service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_swf.client import SWFClient

    session = Session()
    client: SWFClient = session.client("swf")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetWorkflowExecutionHistoryPaginator,
    ListActivityTypesPaginator,
    ListClosedWorkflowExecutionsPaginator,
    ListDomainsPaginator,
    ListOpenWorkflowExecutionsPaginator,
    ListWorkflowTypesPaginator,
    PollForDecisionTaskPaginator,
)
from .type_defs import (
    ActivityTaskStatusTypeDef,
    ActivityTaskTypeDef,
    ActivityTypeDetailTypeDef,
    ActivityTypeInfosTypeDef,
    CountClosedWorkflowExecutionsInputRequestTypeDef,
    CountOpenWorkflowExecutionsInputRequestTypeDef,
    CountPendingActivityTasksInputRequestTypeDef,
    CountPendingDecisionTasksInputRequestTypeDef,
    DecisionTaskTypeDef,
    DeleteActivityTypeInputRequestTypeDef,
    DeleteWorkflowTypeInputRequestTypeDef,
    DeprecateActivityTypeInputRequestTypeDef,
    DeprecateDomainInputRequestTypeDef,
    DeprecateWorkflowTypeInputRequestTypeDef,
    DescribeActivityTypeInputRequestTypeDef,
    DescribeDomainInputRequestTypeDef,
    DescribeWorkflowExecutionInputRequestTypeDef,
    DescribeWorkflowTypeInputRequestTypeDef,
    DomainDetailTypeDef,
    DomainInfosTypeDef,
    EmptyResponseMetadataTypeDef,
    GetWorkflowExecutionHistoryInputRequestTypeDef,
    HistoryTypeDef,
    ListActivityTypesInputRequestTypeDef,
    ListClosedWorkflowExecutionsInputRequestTypeDef,
    ListDomainsInputRequestTypeDef,
    ListOpenWorkflowExecutionsInputRequestTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListWorkflowTypesInputRequestTypeDef,
    PendingTaskCountTypeDef,
    PollForActivityTaskInputRequestTypeDef,
    PollForDecisionTaskInputRequestTypeDef,
    RecordActivityTaskHeartbeatInputRequestTypeDef,
    RegisterActivityTypeInputRequestTypeDef,
    RegisterDomainInputRequestTypeDef,
    RegisterWorkflowTypeInputRequestTypeDef,
    RequestCancelWorkflowExecutionInputRequestTypeDef,
    RespondActivityTaskCanceledInputRequestTypeDef,
    RespondActivityTaskCompletedInputRequestTypeDef,
    RespondActivityTaskFailedInputRequestTypeDef,
    RespondDecisionTaskCompletedInputRequestTypeDef,
    RunTypeDef,
    SignalWorkflowExecutionInputRequestTypeDef,
    StartWorkflowExecutionInputRequestTypeDef,
    TagResourceInputRequestTypeDef,
    TerminateWorkflowExecutionInputRequestTypeDef,
    UndeprecateActivityTypeInputRequestTypeDef,
    UndeprecateDomainInputRequestTypeDef,
    UndeprecateWorkflowTypeInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    WorkflowExecutionCountTypeDef,
    WorkflowExecutionDetailTypeDef,
    WorkflowExecutionInfosTypeDef,
    WorkflowTypeDetailTypeDef,
    WorkflowTypeInfosTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("SWFClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    DefaultUndefinedFault: Type[BotocoreClientError]
    DomainAlreadyExistsFault: Type[BotocoreClientError]
    DomainDeprecatedFault: Type[BotocoreClientError]
    LimitExceededFault: Type[BotocoreClientError]
    OperationNotPermittedFault: Type[BotocoreClientError]
    TooManyTagsFault: Type[BotocoreClientError]
    TypeAlreadyExistsFault: Type[BotocoreClientError]
    TypeDeprecatedFault: Type[BotocoreClientError]
    TypeNotDeprecatedFault: Type[BotocoreClientError]
    UnknownResourceFault: Type[BotocoreClientError]
    WorkflowExecutionAlreadyStartedFault: Type[BotocoreClientError]


class SWFClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SWFClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#close)
        """

    def count_closed_workflow_executions(
        self, **kwargs: Unpack[CountClosedWorkflowExecutionsInputRequestTypeDef]
    ) -> WorkflowExecutionCountTypeDef:
        """
        Returns the number of closed workflow executions within the given domain that
        meet the specified filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/count_closed_workflow_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#count_closed_workflow_executions)
        """

    def count_open_workflow_executions(
        self, **kwargs: Unpack[CountOpenWorkflowExecutionsInputRequestTypeDef]
    ) -> WorkflowExecutionCountTypeDef:
        """
        Returns the number of open workflow executions within the given domain that
        meet the specified filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/count_open_workflow_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#count_open_workflow_executions)
        """

    def count_pending_activity_tasks(
        self, **kwargs: Unpack[CountPendingActivityTasksInputRequestTypeDef]
    ) -> PendingTaskCountTypeDef:
        """
        Returns the estimated number of activity tasks in the specified task list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/count_pending_activity_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#count_pending_activity_tasks)
        """

    def count_pending_decision_tasks(
        self, **kwargs: Unpack[CountPendingDecisionTasksInputRequestTypeDef]
    ) -> PendingTaskCountTypeDef:
        """
        Returns the estimated number of decision tasks in the specified task list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/count_pending_decision_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#count_pending_decision_tasks)
        """

    def delete_activity_type(
        self, **kwargs: Unpack[DeleteActivityTypeInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified <i>activity type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/delete_activity_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#delete_activity_type)
        """

    def delete_workflow_type(
        self, **kwargs: Unpack[DeleteWorkflowTypeInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified <i>workflow type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/delete_workflow_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#delete_workflow_type)
        """

    def deprecate_activity_type(
        self, **kwargs: Unpack[DeprecateActivityTypeInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deprecates the specified <i>activity type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/deprecate_activity_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#deprecate_activity_type)
        """

    def deprecate_domain(
        self, **kwargs: Unpack[DeprecateDomainInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deprecates the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/deprecate_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#deprecate_domain)
        """

    def deprecate_workflow_type(
        self, **kwargs: Unpack[DeprecateWorkflowTypeInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deprecates the specified <i>workflow type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/deprecate_workflow_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#deprecate_workflow_type)
        """

    def describe_activity_type(
        self, **kwargs: Unpack[DescribeActivityTypeInputRequestTypeDef]
    ) -> ActivityTypeDetailTypeDef:
        """
        Returns information about the specified activity type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/describe_activity_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#describe_activity_type)
        """

    def describe_domain(
        self, **kwargs: Unpack[DescribeDomainInputRequestTypeDef]
    ) -> DomainDetailTypeDef:
        """
        Returns information about the specified domain, including description and
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/describe_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#describe_domain)
        """

    def describe_workflow_execution(
        self, **kwargs: Unpack[DescribeWorkflowExecutionInputRequestTypeDef]
    ) -> WorkflowExecutionDetailTypeDef:
        """
        Returns information about the specified workflow execution including its type
        and some statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/describe_workflow_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#describe_workflow_execution)
        """

    def describe_workflow_type(
        self, **kwargs: Unpack[DescribeWorkflowTypeInputRequestTypeDef]
    ) -> WorkflowTypeDetailTypeDef:
        """
        Returns information about the specified <i>workflow type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/describe_workflow_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#describe_workflow_type)
        """

    def get_workflow_execution_history(
        self, **kwargs: Unpack[GetWorkflowExecutionHistoryInputRequestTypeDef]
    ) -> HistoryTypeDef:
        """
        Returns the history of the specified workflow execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_workflow_execution_history.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#get_workflow_execution_history)
        """

    def list_activity_types(
        self, **kwargs: Unpack[ListActivityTypesInputRequestTypeDef]
    ) -> ActivityTypeInfosTypeDef:
        """
        Returns information about all activities registered in the specified domain
        that match the specified name and registration status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/list_activity_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#list_activity_types)
        """

    def list_closed_workflow_executions(
        self, **kwargs: Unpack[ListClosedWorkflowExecutionsInputRequestTypeDef]
    ) -> WorkflowExecutionInfosTypeDef:
        """
        Returns a list of closed workflow executions in the specified domain that meet
        the filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/list_closed_workflow_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#list_closed_workflow_executions)
        """

    def list_domains(self, **kwargs: Unpack[ListDomainsInputRequestTypeDef]) -> DomainInfosTypeDef:
        """
        Returns the list of domains registered in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/list_domains.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#list_domains)
        """

    def list_open_workflow_executions(
        self, **kwargs: Unpack[ListOpenWorkflowExecutionsInputRequestTypeDef]
    ) -> WorkflowExecutionInfosTypeDef:
        """
        Returns a list of open workflow executions in the specified domain that meet
        the filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/list_open_workflow_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#list_open_workflow_executions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        List tags for a given domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#list_tags_for_resource)
        """

    def list_workflow_types(
        self, **kwargs: Unpack[ListWorkflowTypesInputRequestTypeDef]
    ) -> WorkflowTypeInfosTypeDef:
        """
        Returns information about workflow types in the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/list_workflow_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#list_workflow_types)
        """

    def poll_for_activity_task(
        self, **kwargs: Unpack[PollForActivityTaskInputRequestTypeDef]
    ) -> ActivityTaskTypeDef:
        """
        Used by workers to get an <a>ActivityTask</a> from the specified activity
        <code>taskList</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/poll_for_activity_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#poll_for_activity_task)
        """

    def poll_for_decision_task(
        self, **kwargs: Unpack[PollForDecisionTaskInputRequestTypeDef]
    ) -> DecisionTaskTypeDef:
        """
        Used by deciders to get a <a>DecisionTask</a> from the specified decision
        <code>taskList</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/poll_for_decision_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#poll_for_decision_task)
        """

    def record_activity_task_heartbeat(
        self, **kwargs: Unpack[RecordActivityTaskHeartbeatInputRequestTypeDef]
    ) -> ActivityTaskStatusTypeDef:
        """
        Used by activity workers to report to the service that the <a>ActivityTask</a>
        represented by the specified <code>taskToken</code> is still making progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/record_activity_task_heartbeat.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#record_activity_task_heartbeat)
        """

    def register_activity_type(
        self, **kwargs: Unpack[RegisterActivityTypeInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Registers a new <i>activity type</i> along with its configuration settings in
        the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/register_activity_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#register_activity_type)
        """

    def register_domain(
        self, **kwargs: Unpack[RegisterDomainInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Registers a new domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/register_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#register_domain)
        """

    def register_workflow_type(
        self, **kwargs: Unpack[RegisterWorkflowTypeInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Registers a new <i>workflow type</i> and its configuration settings in the
        specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/register_workflow_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#register_workflow_type)
        """

    def request_cancel_workflow_execution(
        self, **kwargs: Unpack[RequestCancelWorkflowExecutionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Records a <code>WorkflowExecutionCancelRequested</code> event in the currently
        running workflow execution identified by the given domain, workflowId, and
        runId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/request_cancel_workflow_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#request_cancel_workflow_execution)
        """

    def respond_activity_task_canceled(
        self, **kwargs: Unpack[RespondActivityTaskCanceledInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used by workers to tell the service that the <a>ActivityTask</a> identified by
        the <code>taskToken</code> was successfully canceled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/respond_activity_task_canceled.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#respond_activity_task_canceled)
        """

    def respond_activity_task_completed(
        self, **kwargs: Unpack[RespondActivityTaskCompletedInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used by workers to tell the service that the <a>ActivityTask</a> identified by
        the <code>taskToken</code> completed successfully with a <code>result</code>
        (if provided).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/respond_activity_task_completed.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#respond_activity_task_completed)
        """

    def respond_activity_task_failed(
        self, **kwargs: Unpack[RespondActivityTaskFailedInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used by workers to tell the service that the <a>ActivityTask</a> identified by
        the <code>taskToken</code> has failed with <code>reason</code> (if specified).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/respond_activity_task_failed.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#respond_activity_task_failed)
        """

    def respond_decision_task_completed(
        self, **kwargs: Unpack[RespondDecisionTaskCompletedInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used by deciders to tell the service that the <a>DecisionTask</a> identified by
        the <code>taskToken</code> has successfully completed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/respond_decision_task_completed.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#respond_decision_task_completed)
        """

    def signal_workflow_execution(
        self, **kwargs: Unpack[SignalWorkflowExecutionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Records a <code>WorkflowExecutionSignaled</code> event in the workflow
        execution history and creates a decision task for the workflow execution
        identified by the given domain, workflowId and runId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/signal_workflow_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#signal_workflow_execution)
        """

    def start_workflow_execution(
        self, **kwargs: Unpack[StartWorkflowExecutionInputRequestTypeDef]
    ) -> RunTypeDef:
        """
        Starts an execution of the workflow type in the specified domain using the
        provided <code>workflowId</code> and input data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/start_workflow_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#start_workflow_execution)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Add a tag to a Amazon SWF domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#tag_resource)
        """

    def terminate_workflow_execution(
        self, **kwargs: Unpack[TerminateWorkflowExecutionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Records a <code>WorkflowExecutionTerminated</code> event and forces closure of
        the workflow execution identified by the given domain, runId, and workflowId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/terminate_workflow_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#terminate_workflow_execution)
        """

    def undeprecate_activity_type(
        self, **kwargs: Unpack[UndeprecateActivityTypeInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Undeprecates a previously deprecated <i>activity type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/undeprecate_activity_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#undeprecate_activity_type)
        """

    def undeprecate_domain(
        self, **kwargs: Unpack[UndeprecateDomainInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Undeprecates a previously deprecated domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/undeprecate_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#undeprecate_domain)
        """

    def undeprecate_workflow_type(
        self, **kwargs: Unpack[UndeprecateWorkflowTypeInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Undeprecates a previously deprecated <i>workflow type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/undeprecate_workflow_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#undeprecate_workflow_type)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove a tag from a Amazon SWF domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_workflow_execution_history"]
    ) -> GetWorkflowExecutionHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_activity_types"]
    ) -> ListActivityTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_closed_workflow_executions"]
    ) -> ListClosedWorkflowExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_open_workflow_executions"]
    ) -> ListOpenWorkflowExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_workflow_types"]
    ) -> ListWorkflowTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["poll_for_decision_task"]
    ) -> PollForDecisionTaskPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_swf/client/#get_paginator)
        """
