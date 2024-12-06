"""
Type annotations for ssm-incidents service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_ssm_incidents.client import SSMIncidentsClient

    session = Session()
    client: SSMIncidentsClient = session.client("ssm-incidents")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetResourcePoliciesPaginator,
    ListIncidentFindingsPaginator,
    ListIncidentRecordsPaginator,
    ListRelatedItemsPaginator,
    ListReplicationSetsPaginator,
    ListResponsePlansPaginator,
    ListTimelineEventsPaginator,
)
from .type_defs import (
    BatchGetIncidentFindingsInputRequestTypeDef,
    BatchGetIncidentFindingsOutputTypeDef,
    CreateReplicationSetInputRequestTypeDef,
    CreateReplicationSetOutputTypeDef,
    CreateResponsePlanInputRequestTypeDef,
    CreateResponsePlanOutputTypeDef,
    CreateTimelineEventInputRequestTypeDef,
    CreateTimelineEventOutputTypeDef,
    DeleteIncidentRecordInputRequestTypeDef,
    DeleteReplicationSetInputRequestTypeDef,
    DeleteResourcePolicyInputRequestTypeDef,
    DeleteResponsePlanInputRequestTypeDef,
    DeleteTimelineEventInputRequestTypeDef,
    GetIncidentRecordInputRequestTypeDef,
    GetIncidentRecordOutputTypeDef,
    GetReplicationSetInputRequestTypeDef,
    GetReplicationSetOutputTypeDef,
    GetResourcePoliciesInputRequestTypeDef,
    GetResourcePoliciesOutputTypeDef,
    GetResponsePlanInputRequestTypeDef,
    GetResponsePlanOutputTypeDef,
    GetTimelineEventInputRequestTypeDef,
    GetTimelineEventOutputTypeDef,
    ListIncidentFindingsInputRequestTypeDef,
    ListIncidentFindingsOutputTypeDef,
    ListIncidentRecordsInputRequestTypeDef,
    ListIncidentRecordsOutputTypeDef,
    ListRelatedItemsInputRequestTypeDef,
    ListRelatedItemsOutputTypeDef,
    ListReplicationSetsInputRequestTypeDef,
    ListReplicationSetsOutputTypeDef,
    ListResponsePlansInputRequestTypeDef,
    ListResponsePlansOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTimelineEventsInputRequestTypeDef,
    ListTimelineEventsOutputTypeDef,
    PutResourcePolicyInputRequestTypeDef,
    PutResourcePolicyOutputTypeDef,
    StartIncidentInputRequestTypeDef,
    StartIncidentOutputTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDeletionProtectionInputRequestTypeDef,
    UpdateIncidentRecordInputRequestTypeDef,
    UpdateRelatedItemsInputRequestTypeDef,
    UpdateReplicationSetInputRequestTypeDef,
    UpdateResponsePlanInputRequestTypeDef,
    UpdateTimelineEventInputRequestTypeDef,
)
from .waiter import WaitForReplicationSetActiveWaiter, WaitForReplicationSetDeletedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("SSMIncidentsClient",)


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


class SSMIncidentsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SSMIncidentsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#close)
        """

    def batch_get_incident_findings(
        self, **kwargs: Unpack[BatchGetIncidentFindingsInputRequestTypeDef]
    ) -> BatchGetIncidentFindingsOutputTypeDef:
        """
        Retrieves details about all specified findings for an incident, including
        descriptive details about each finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/batch_get_incident_findings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#batch_get_incident_findings)
        """

    def create_replication_set(
        self, **kwargs: Unpack[CreateReplicationSetInputRequestTypeDef]
    ) -> CreateReplicationSetOutputTypeDef:
        """
        A replication set replicates and encrypts your data to the provided Regions
        with the provided KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/create_replication_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#create_replication_set)
        """

    def create_response_plan(
        self, **kwargs: Unpack[CreateResponsePlanInputRequestTypeDef]
    ) -> CreateResponsePlanOutputTypeDef:
        """
        Creates a response plan that automates the initial response to incidents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/create_response_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#create_response_plan)
        """

    def create_timeline_event(
        self, **kwargs: Unpack[CreateTimelineEventInputRequestTypeDef]
    ) -> CreateTimelineEventOutputTypeDef:
        """
        Creates a custom timeline event on the incident details page of an incident
        record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/create_timeline_event.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#create_timeline_event)
        """

    def delete_incident_record(
        self, **kwargs: Unpack[DeleteIncidentRecordInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an incident record from Incident Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/delete_incident_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#delete_incident_record)
        """

    def delete_replication_set(
        self, **kwargs: Unpack[DeleteReplicationSetInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes all Regions in your replication set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/delete_replication_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#delete_replication_set)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the resource policy that Resource Access Manager uses to share your
        Incident Manager resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/delete_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#delete_resource_policy)
        """

    def delete_response_plan(
        self, **kwargs: Unpack[DeleteResponsePlanInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/delete_response_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#delete_response_plan)
        """

    def delete_timeline_event(
        self, **kwargs: Unpack[DeleteTimelineEventInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a timeline event from an incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/delete_timeline_event.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#delete_timeline_event)
        """

    def get_incident_record(
        self, **kwargs: Unpack[GetIncidentRecordInputRequestTypeDef]
    ) -> GetIncidentRecordOutputTypeDef:
        """
        Returns the details for the specified incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_incident_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_incident_record)
        """

    def get_replication_set(
        self, **kwargs: Unpack[GetReplicationSetInputRequestTypeDef]
    ) -> GetReplicationSetOutputTypeDef:
        """
        Retrieve your Incident Manager replication set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_replication_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_replication_set)
        """

    def get_resource_policies(
        self, **kwargs: Unpack[GetResourcePoliciesInputRequestTypeDef]
    ) -> GetResourcePoliciesOutputTypeDef:
        """
        Retrieves the resource policies attached to the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_resource_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_resource_policies)
        """

    def get_response_plan(
        self, **kwargs: Unpack[GetResponsePlanInputRequestTypeDef]
    ) -> GetResponsePlanOutputTypeDef:
        """
        Retrieves the details of the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_response_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_response_plan)
        """

    def get_timeline_event(
        self, **kwargs: Unpack[GetTimelineEventInputRequestTypeDef]
    ) -> GetTimelineEventOutputTypeDef:
        """
        Retrieves a timeline event based on its ID and incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_timeline_event.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_timeline_event)
        """

    def list_incident_findings(
        self, **kwargs: Unpack[ListIncidentFindingsInputRequestTypeDef]
    ) -> ListIncidentFindingsOutputTypeDef:
        """
        Retrieves a list of the IDs of findings, plus their last modified times, that
        have been identified for a specified incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_incident_findings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#list_incident_findings)
        """

    def list_incident_records(
        self, **kwargs: Unpack[ListIncidentRecordsInputRequestTypeDef]
    ) -> ListIncidentRecordsOutputTypeDef:
        """
        Lists all incident records in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_incident_records.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#list_incident_records)
        """

    def list_related_items(
        self, **kwargs: Unpack[ListRelatedItemsInputRequestTypeDef]
    ) -> ListRelatedItemsOutputTypeDef:
        """
        List all related items for an incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_related_items.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#list_related_items)
        """

    def list_replication_sets(
        self, **kwargs: Unpack[ListReplicationSetsInputRequestTypeDef]
    ) -> ListReplicationSetsOutputTypeDef:
        """
        Lists details about the replication set configured in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_replication_sets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#list_replication_sets)
        """

    def list_response_plans(
        self, **kwargs: Unpack[ListResponsePlansInputRequestTypeDef]
    ) -> ListResponsePlansOutputTypeDef:
        """
        Lists all response plans in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_response_plans.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#list_response_plans)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that are attached to the specified response plan or incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#list_tags_for_resource)
        """

    def list_timeline_events(
        self, **kwargs: Unpack[ListTimelineEventsInputRequestTypeDef]
    ) -> ListTimelineEventsOutputTypeDef:
        """
        Lists timeline events for the specified incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_timeline_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#list_timeline_events)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyInputRequestTypeDef]
    ) -> PutResourcePolicyOutputTypeDef:
        """
        Adds a resource policy to the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/put_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#put_resource_policy)
        """

    def start_incident(
        self, **kwargs: Unpack[StartIncidentInputRequestTypeDef]
    ) -> StartIncidentOutputTypeDef:
        """
        Used to start an incident from CloudWatch alarms, EventBridge events, or
        manually.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/start_incident.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#start_incident)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds a tag to a response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#untag_resource)
        """

    def update_deletion_protection(
        self, **kwargs: Unpack[UpdateDeletionProtectionInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update deletion protection to either allow or deny deletion of the final Region
        in a replication set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/update_deletion_protection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#update_deletion_protection)
        """

    def update_incident_record(
        self, **kwargs: Unpack[UpdateIncidentRecordInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update the details of an incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/update_incident_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#update_incident_record)
        """

    def update_related_items(
        self, **kwargs: Unpack[UpdateRelatedItemsInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Add or remove related items from the related items tab of an incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/update_related_items.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#update_related_items)
        """

    def update_replication_set(
        self, **kwargs: Unpack[UpdateReplicationSetInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Add or delete Regions from your replication set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/update_replication_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#update_replication_set)
        """

    def update_response_plan(
        self, **kwargs: Unpack[UpdateResponsePlanInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/update_response_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#update_response_plan)
        """

    def update_timeline_event(
        self, **kwargs: Unpack[UpdateTimelineEventInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a timeline event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/update_timeline_event.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#update_timeline_event)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_policies"]
    ) -> GetResourcePoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_incident_findings"]
    ) -> ListIncidentFindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_incident_records"]
    ) -> ListIncidentRecordsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_related_items"]
    ) -> ListRelatedItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_replication_sets"]
    ) -> ListReplicationSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_response_plans"]
    ) -> ListResponsePlansPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_timeline_events"]
    ) -> ListTimelineEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["wait_for_replication_set_active"]
    ) -> WaitForReplicationSetActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["wait_for_replication_set_deleted"]
    ) -> WaitForReplicationSetDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_incidents/client/#get_waiter)
        """
