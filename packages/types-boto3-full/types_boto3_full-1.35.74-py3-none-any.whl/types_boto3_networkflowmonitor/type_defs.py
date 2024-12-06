"""
Type annotations for networkflowmonitor service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/type_defs/)

Usage::

    ```python
    from types_boto3_networkflowmonitor.type_defs import MonitorLocalResourceTypeDef

    data: MonitorLocalResourceTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    DestinationCategoryType,
    MetricUnitType,
    MonitorLocalResourceTypeType,
    MonitorMetricType,
    MonitorRemoteResourceTypeType,
    MonitorStatusType,
    QueryStatusType,
    ScopeStatusType,
    WorkloadInsightsMetricType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "CreateMonitorInputRequestTypeDef",
    "CreateMonitorOutputTypeDef",
    "CreateScopeInputRequestTypeDef",
    "CreateScopeOutputTypeDef",
    "DeleteMonitorInputRequestTypeDef",
    "DeleteScopeInputRequestTypeDef",
    "GetMonitorInputRequestTypeDef",
    "GetMonitorOutputTypeDef",
    "GetQueryResultsMonitorTopContributorsInputGetQueryResultsMonitorTopContributorsPaginateTypeDef",
    "GetQueryResultsMonitorTopContributorsInputRequestTypeDef",
    "GetQueryResultsMonitorTopContributorsOutputTypeDef",
    "GetQueryResultsWorkloadInsightsTopContributorsDataInputGetQueryResultsWorkloadInsightsTopContributorsDataPaginateTypeDef",
    "GetQueryResultsWorkloadInsightsTopContributorsDataInputRequestTypeDef",
    "GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef",
    "GetQueryResultsWorkloadInsightsTopContributorsInputGetQueryResultsWorkloadInsightsTopContributorsPaginateTypeDef",
    "GetQueryResultsWorkloadInsightsTopContributorsInputRequestTypeDef",
    "GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef",
    "GetQueryStatusMonitorTopContributorsInputRequestTypeDef",
    "GetQueryStatusMonitorTopContributorsOutputTypeDef",
    "GetQueryStatusWorkloadInsightsTopContributorsDataInputRequestTypeDef",
    "GetQueryStatusWorkloadInsightsTopContributorsDataOutputTypeDef",
    "GetQueryStatusWorkloadInsightsTopContributorsInputRequestTypeDef",
    "GetQueryStatusWorkloadInsightsTopContributorsOutputTypeDef",
    "GetScopeInputRequestTypeDef",
    "GetScopeOutputTypeDef",
    "KubernetesMetadataTypeDef",
    "ListMonitorsInputListMonitorsPaginateTypeDef",
    "ListMonitorsInputRequestTypeDef",
    "ListMonitorsOutputTypeDef",
    "ListScopesInputListScopesPaginateTypeDef",
    "ListScopesInputRequestTypeDef",
    "ListScopesOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "MonitorLocalResourceTypeDef",
    "MonitorRemoteResourceTypeDef",
    "MonitorSummaryTypeDef",
    "MonitorTopContributorsRowTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "ScopeSummaryTypeDef",
    "StartQueryMonitorTopContributorsInputRequestTypeDef",
    "StartQueryMonitorTopContributorsOutputTypeDef",
    "StartQueryWorkloadInsightsTopContributorsDataInputRequestTypeDef",
    "StartQueryWorkloadInsightsTopContributorsDataOutputTypeDef",
    "StartQueryWorkloadInsightsTopContributorsInputRequestTypeDef",
    "StartQueryWorkloadInsightsTopContributorsOutputTypeDef",
    "StopQueryMonitorTopContributorsInputRequestTypeDef",
    "StopQueryWorkloadInsightsTopContributorsDataInputRequestTypeDef",
    "StopQueryWorkloadInsightsTopContributorsInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "TargetIdTypeDef",
    "TargetIdentifierTypeDef",
    "TargetResourceTypeDef",
    "TimestampTypeDef",
    "TraversedComponentTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateMonitorInputRequestTypeDef",
    "UpdateMonitorOutputTypeDef",
    "UpdateScopeInputRequestTypeDef",
    "UpdateScopeOutputTypeDef",
    "WorkloadInsightsTopContributorsDataPointTypeDef",
    "WorkloadInsightsTopContributorsRowTypeDef",
)

MonitorLocalResourceTypeDef = TypedDict(
    "MonitorLocalResourceTypeDef",
    {
        "type": MonitorLocalResourceTypeType,
        "identifier": str,
    },
)
MonitorRemoteResourceTypeDef = TypedDict(
    "MonitorRemoteResourceTypeDef",
    {
        "type": MonitorRemoteResourceTypeType,
        "identifier": str,
    },
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteMonitorInputRequestTypeDef(TypedDict):
    monitorName: str


class DeleteScopeInputRequestTypeDef(TypedDict):
    scopeId: str


class GetMonitorInputRequestTypeDef(TypedDict):
    monitorName: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetQueryResultsMonitorTopContributorsInputRequestTypeDef(TypedDict):
    monitorName: str
    queryId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class GetQueryResultsWorkloadInsightsTopContributorsDataInputRequestTypeDef(TypedDict):
    scopeId: str
    queryId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class WorkloadInsightsTopContributorsDataPointTypeDef(TypedDict):
    timestamps: List[datetime]
    values: List[float]
    label: str


class GetQueryResultsWorkloadInsightsTopContributorsInputRequestTypeDef(TypedDict):
    scopeId: str
    queryId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class WorkloadInsightsTopContributorsRowTypeDef(TypedDict):
    accountId: NotRequired[str]
    localSubnetId: NotRequired[str]
    localAz: NotRequired[str]
    localVpcId: NotRequired[str]
    localRegion: NotRequired[str]
    remoteIdentifier: NotRequired[str]
    value: NotRequired[int]
    localSubnetArn: NotRequired[str]
    localVpcArn: NotRequired[str]


class GetQueryStatusMonitorTopContributorsInputRequestTypeDef(TypedDict):
    monitorName: str
    queryId: str


class GetQueryStatusWorkloadInsightsTopContributorsDataInputRequestTypeDef(TypedDict):
    scopeId: str
    queryId: str


class GetQueryStatusWorkloadInsightsTopContributorsInputRequestTypeDef(TypedDict):
    scopeId: str
    queryId: str


class GetScopeInputRequestTypeDef(TypedDict):
    scopeId: str


class KubernetesMetadataTypeDef(TypedDict):
    localServiceName: NotRequired[str]
    localPodName: NotRequired[str]
    localPodNamespace: NotRequired[str]
    remoteServiceName: NotRequired[str]
    remotePodName: NotRequired[str]
    remotePodNamespace: NotRequired[str]


class ListMonitorsInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    monitorStatus: NotRequired[MonitorStatusType]


class MonitorSummaryTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    monitorStatus: MonitorStatusType


class ListScopesInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ScopeSummaryTypeDef(TypedDict):
    scopeId: str
    status: ScopeStatusType
    scopeArn: str


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str


class TraversedComponentTypeDef(TypedDict):
    componentId: NotRequired[str]
    componentType: NotRequired[str]
    componentArn: NotRequired[str]
    serviceName: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class StopQueryMonitorTopContributorsInputRequestTypeDef(TypedDict):
    monitorName: str
    queryId: str


class StopQueryWorkloadInsightsTopContributorsDataInputRequestTypeDef(TypedDict):
    scopeId: str
    queryId: str


class StopQueryWorkloadInsightsTopContributorsInputRequestTypeDef(TypedDict):
    scopeId: str
    queryId: str


class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class TargetIdTypeDef(TypedDict):
    accountId: NotRequired[str]


class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class CreateMonitorInputRequestTypeDef(TypedDict):
    monitorName: str
    localResources: Sequence[MonitorLocalResourceTypeDef]
    scopeArn: str
    remoteResources: NotRequired[Sequence[MonitorRemoteResourceTypeDef]]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class UpdateMonitorInputRequestTypeDef(TypedDict):
    monitorName: str
    localResourcesToAdd: NotRequired[Sequence[MonitorLocalResourceTypeDef]]
    localResourcesToRemove: NotRequired[Sequence[MonitorLocalResourceTypeDef]]
    remoteResourcesToAdd: NotRequired[Sequence[MonitorRemoteResourceTypeDef]]
    remoteResourcesToRemove: NotRequired[Sequence[MonitorRemoteResourceTypeDef]]
    clientToken: NotRequired[str]


class CreateMonitorOutputTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    monitorStatus: MonitorStatusType
    localResources: List[MonitorLocalResourceTypeDef]
    remoteResources: List[MonitorRemoteResourceTypeDef]
    createdAt: datetime
    modifiedAt: datetime
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateScopeOutputTypeDef(TypedDict):
    scopeId: str
    status: ScopeStatusType
    scopeArn: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetMonitorOutputTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    monitorStatus: MonitorStatusType
    localResources: List[MonitorLocalResourceTypeDef]
    remoteResources: List[MonitorRemoteResourceTypeDef]
    createdAt: datetime
    modifiedAt: datetime
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetQueryStatusMonitorTopContributorsOutputTypeDef(TypedDict):
    status: QueryStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetQueryStatusWorkloadInsightsTopContributorsDataOutputTypeDef(TypedDict):
    status: QueryStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetQueryStatusWorkloadInsightsTopContributorsOutputTypeDef(TypedDict):
    status: QueryStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartQueryMonitorTopContributorsOutputTypeDef(TypedDict):
    queryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartQueryWorkloadInsightsTopContributorsDataOutputTypeDef(TypedDict):
    queryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartQueryWorkloadInsightsTopContributorsOutputTypeDef(TypedDict):
    queryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMonitorOutputTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    monitorStatus: MonitorStatusType
    localResources: List[MonitorLocalResourceTypeDef]
    remoteResources: List[MonitorRemoteResourceTypeDef]
    createdAt: datetime
    modifiedAt: datetime
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateScopeOutputTypeDef(TypedDict):
    scopeId: str
    status: ScopeStatusType
    scopeArn: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetQueryResultsMonitorTopContributorsInputGetQueryResultsMonitorTopContributorsPaginateTypeDef(
    TypedDict
):
    monitorName: str
    queryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetQueryResultsWorkloadInsightsTopContributorsDataInputGetQueryResultsWorkloadInsightsTopContributorsDataPaginateTypeDef(
    TypedDict
):
    scopeId: str
    queryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetQueryResultsWorkloadInsightsTopContributorsInputGetQueryResultsWorkloadInsightsTopContributorsPaginateTypeDef(
    TypedDict
):
    scopeId: str
    queryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMonitorsInputListMonitorsPaginateTypeDef(TypedDict):
    monitorStatus: NotRequired[MonitorStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListScopesInputListScopesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef(TypedDict):
    unit: MetricUnitType
    datapoints: List[WorkloadInsightsTopContributorsDataPointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef(TypedDict):
    topContributors: List[WorkloadInsightsTopContributorsRowTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListMonitorsOutputTypeDef(TypedDict):
    monitors: List[MonitorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListScopesOutputTypeDef(TypedDict):
    scopes: List[ScopeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class MonitorTopContributorsRowTypeDef(TypedDict):
    localIp: NotRequired[str]
    snatIp: NotRequired[str]
    localInstanceId: NotRequired[str]
    localVpcId: NotRequired[str]
    localRegion: NotRequired[str]
    localAz: NotRequired[str]
    localSubnetId: NotRequired[str]
    targetPort: NotRequired[int]
    destinationCategory: NotRequired[DestinationCategoryType]
    remoteVpcId: NotRequired[str]
    remoteRegion: NotRequired[str]
    remoteAz: NotRequired[str]
    remoteSubnetId: NotRequired[str]
    remoteInstanceId: NotRequired[str]
    remoteIp: NotRequired[str]
    dnatIp: NotRequired[str]
    value: NotRequired[int]
    traversedConstructs: NotRequired[List[TraversedComponentTypeDef]]
    kubernetesMetadata: NotRequired[KubernetesMetadataTypeDef]
    localInstanceArn: NotRequired[str]
    localSubnetArn: NotRequired[str]
    localVpcArn: NotRequired[str]
    remoteInstanceArn: NotRequired[str]
    remoteSubnetArn: NotRequired[str]
    remoteVpcArn: NotRequired[str]


class StartQueryMonitorTopContributorsInputRequestTypeDef(TypedDict):
    monitorName: str
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    metricName: MonitorMetricType
    destinationCategory: DestinationCategoryType
    limit: NotRequired[int]


class StartQueryWorkloadInsightsTopContributorsDataInputRequestTypeDef(TypedDict):
    scopeId: str
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    metricName: WorkloadInsightsMetricType
    destinationCategory: DestinationCategoryType


class StartQueryWorkloadInsightsTopContributorsInputRequestTypeDef(TypedDict):
    scopeId: str
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    metricName: WorkloadInsightsMetricType
    destinationCategory: DestinationCategoryType
    limit: NotRequired[int]


class TargetIdentifierTypeDef(TypedDict):
    targetId: TargetIdTypeDef
    targetType: Literal["ACCOUNT"]


class GetQueryResultsMonitorTopContributorsOutputTypeDef(TypedDict):
    unit: MetricUnitType
    topContributors: List[MonitorTopContributorsRowTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class TargetResourceTypeDef(TypedDict):
    targetIdentifier: TargetIdentifierTypeDef
    region: str


class CreateScopeInputRequestTypeDef(TypedDict):
    targets: Sequence[TargetResourceTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class GetScopeOutputTypeDef(TypedDict):
    scopeId: str
    status: ScopeStatusType
    scopeArn: str
    targets: List[TargetResourceTypeDef]
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateScopeInputRequestTypeDef(TypedDict):
    scopeId: str
    resourcesToAdd: NotRequired[Sequence[TargetResourceTypeDef]]
    resourcesToDelete: NotRequired[Sequence[TargetResourceTypeDef]]
