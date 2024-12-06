"""
Type annotations for vpc-lattice service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/type_defs/)

Usage::

    ```python
    from types_boto3_vpc_lattice.type_defs import AccessLogSubscriptionSummaryTypeDef

    data: AccessLogSubscriptionSummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AuthPolicyStateType,
    AuthTypeType,
    HealthCheckProtocolVersionType,
    IpAddressTypeType,
    LambdaEventStructureVersionType,
    ListenerProtocolType,
    ResourceConfigurationIpAddressTypeType,
    ResourceConfigurationStatusType,
    ResourceConfigurationTypeType,
    ResourceGatewayIpAddressTypeType,
    ResourceGatewayStatusType,
    ServiceNetworkLogTypeType,
    ServiceNetworkResourceAssociationStatusType,
    ServiceNetworkServiceAssociationStatusType,
    ServiceNetworkVpcAssociationStatusType,
    ServiceStatusType,
    TargetGroupProtocolType,
    TargetGroupProtocolVersionType,
    TargetGroupStatusType,
    TargetGroupTypeType,
    TargetStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccessLogSubscriptionSummaryTypeDef",
    "ArnResourceTypeDef",
    "BatchUpdateRuleRequestRequestTypeDef",
    "BatchUpdateRuleResponseTypeDef",
    "CreateAccessLogSubscriptionRequestRequestTypeDef",
    "CreateAccessLogSubscriptionResponseTypeDef",
    "CreateListenerRequestRequestTypeDef",
    "CreateListenerResponseTypeDef",
    "CreateResourceConfigurationRequestRequestTypeDef",
    "CreateResourceConfigurationResponseTypeDef",
    "CreateResourceGatewayRequestRequestTypeDef",
    "CreateResourceGatewayResponseTypeDef",
    "CreateRuleRequestRequestTypeDef",
    "CreateRuleResponseTypeDef",
    "CreateServiceNetworkRequestRequestTypeDef",
    "CreateServiceNetworkResourceAssociationRequestRequestTypeDef",
    "CreateServiceNetworkResourceAssociationResponseTypeDef",
    "CreateServiceNetworkResponseTypeDef",
    "CreateServiceNetworkServiceAssociationRequestRequestTypeDef",
    "CreateServiceNetworkServiceAssociationResponseTypeDef",
    "CreateServiceNetworkVpcAssociationRequestRequestTypeDef",
    "CreateServiceNetworkVpcAssociationResponseTypeDef",
    "CreateServiceRequestRequestTypeDef",
    "CreateServiceResponseTypeDef",
    "CreateTargetGroupRequestRequestTypeDef",
    "CreateTargetGroupResponseTypeDef",
    "DeleteAccessLogSubscriptionRequestRequestTypeDef",
    "DeleteAuthPolicyRequestRequestTypeDef",
    "DeleteListenerRequestRequestTypeDef",
    "DeleteResourceConfigurationRequestRequestTypeDef",
    "DeleteResourceEndpointAssociationRequestRequestTypeDef",
    "DeleteResourceEndpointAssociationResponseTypeDef",
    "DeleteResourceGatewayRequestRequestTypeDef",
    "DeleteResourceGatewayResponseTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteRuleRequestRequestTypeDef",
    "DeleteServiceNetworkRequestRequestTypeDef",
    "DeleteServiceNetworkResourceAssociationRequestRequestTypeDef",
    "DeleteServiceNetworkResourceAssociationResponseTypeDef",
    "DeleteServiceNetworkServiceAssociationRequestRequestTypeDef",
    "DeleteServiceNetworkServiceAssociationResponseTypeDef",
    "DeleteServiceNetworkVpcAssociationRequestRequestTypeDef",
    "DeleteServiceNetworkVpcAssociationResponseTypeDef",
    "DeleteServiceRequestRequestTypeDef",
    "DeleteServiceResponseTypeDef",
    "DeleteTargetGroupRequestRequestTypeDef",
    "DeleteTargetGroupResponseTypeDef",
    "DeregisterTargetsRequestRequestTypeDef",
    "DeregisterTargetsResponseTypeDef",
    "DnsEntryTypeDef",
    "DnsResourceTypeDef",
    "FixedResponseActionTypeDef",
    "ForwardActionOutputTypeDef",
    "ForwardActionTypeDef",
    "ForwardActionUnionTypeDef",
    "GetAccessLogSubscriptionRequestRequestTypeDef",
    "GetAccessLogSubscriptionResponseTypeDef",
    "GetAuthPolicyRequestRequestTypeDef",
    "GetAuthPolicyResponseTypeDef",
    "GetListenerRequestRequestTypeDef",
    "GetListenerResponseTypeDef",
    "GetResourceConfigurationRequestRequestTypeDef",
    "GetResourceConfigurationResponseTypeDef",
    "GetResourceGatewayRequestRequestTypeDef",
    "GetResourceGatewayResponseTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "GetRuleRequestRequestTypeDef",
    "GetRuleResponseTypeDef",
    "GetServiceNetworkRequestRequestTypeDef",
    "GetServiceNetworkResourceAssociationRequestRequestTypeDef",
    "GetServiceNetworkResourceAssociationResponseTypeDef",
    "GetServiceNetworkResponseTypeDef",
    "GetServiceNetworkServiceAssociationRequestRequestTypeDef",
    "GetServiceNetworkServiceAssociationResponseTypeDef",
    "GetServiceNetworkVpcAssociationRequestRequestTypeDef",
    "GetServiceNetworkVpcAssociationResponseTypeDef",
    "GetServiceRequestRequestTypeDef",
    "GetServiceResponseTypeDef",
    "GetTargetGroupRequestRequestTypeDef",
    "GetTargetGroupResponseTypeDef",
    "HeaderMatchTypeDef",
    "HeaderMatchTypeTypeDef",
    "HealthCheckConfigTypeDef",
    "HttpMatchOutputTypeDef",
    "HttpMatchTypeDef",
    "HttpMatchUnionTypeDef",
    "IpResourceTypeDef",
    "ListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef",
    "ListAccessLogSubscriptionsRequestRequestTypeDef",
    "ListAccessLogSubscriptionsResponseTypeDef",
    "ListListenersRequestListListenersPaginateTypeDef",
    "ListListenersRequestRequestTypeDef",
    "ListListenersResponseTypeDef",
    "ListResourceConfigurationsRequestListResourceConfigurationsPaginateTypeDef",
    "ListResourceConfigurationsRequestRequestTypeDef",
    "ListResourceConfigurationsResponseTypeDef",
    "ListResourceEndpointAssociationsRequestListResourceEndpointAssociationsPaginateTypeDef",
    "ListResourceEndpointAssociationsRequestRequestTypeDef",
    "ListResourceEndpointAssociationsResponseTypeDef",
    "ListResourceGatewaysRequestListResourceGatewaysPaginateTypeDef",
    "ListResourceGatewaysRequestRequestTypeDef",
    "ListResourceGatewaysResponseTypeDef",
    "ListRulesRequestListRulesPaginateTypeDef",
    "ListRulesRequestRequestTypeDef",
    "ListRulesResponseTypeDef",
    "ListServiceNetworkResourceAssociationsRequestListServiceNetworkResourceAssociationsPaginateTypeDef",
    "ListServiceNetworkResourceAssociationsRequestRequestTypeDef",
    "ListServiceNetworkResourceAssociationsResponseTypeDef",
    "ListServiceNetworkServiceAssociationsRequestListServiceNetworkServiceAssociationsPaginateTypeDef",
    "ListServiceNetworkServiceAssociationsRequestRequestTypeDef",
    "ListServiceNetworkServiceAssociationsResponseTypeDef",
    "ListServiceNetworkVpcAssociationsRequestListServiceNetworkVpcAssociationsPaginateTypeDef",
    "ListServiceNetworkVpcAssociationsRequestRequestTypeDef",
    "ListServiceNetworkVpcAssociationsResponseTypeDef",
    "ListServiceNetworkVpcEndpointAssociationsRequestListServiceNetworkVpcEndpointAssociationsPaginateTypeDef",
    "ListServiceNetworkVpcEndpointAssociationsRequestRequestTypeDef",
    "ListServiceNetworkVpcEndpointAssociationsResponseTypeDef",
    "ListServiceNetworksRequestListServiceNetworksPaginateTypeDef",
    "ListServiceNetworksRequestRequestTypeDef",
    "ListServiceNetworksResponseTypeDef",
    "ListServicesRequestListServicesPaginateTypeDef",
    "ListServicesRequestRequestTypeDef",
    "ListServicesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTargetGroupsRequestListTargetGroupsPaginateTypeDef",
    "ListTargetGroupsRequestRequestTypeDef",
    "ListTargetGroupsResponseTypeDef",
    "ListTargetsRequestListTargetsPaginateTypeDef",
    "ListTargetsRequestRequestTypeDef",
    "ListTargetsResponseTypeDef",
    "ListenerSummaryTypeDef",
    "MatcherTypeDef",
    "PaginatorConfigTypeDef",
    "PathMatchTypeDef",
    "PathMatchTypeTypeDef",
    "PutAuthPolicyRequestRequestTypeDef",
    "PutAuthPolicyResponseTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "RegisterTargetsRequestRequestTypeDef",
    "RegisterTargetsResponseTypeDef",
    "ResourceConfigurationDefinitionTypeDef",
    "ResourceConfigurationSummaryTypeDef",
    "ResourceEndpointAssociationSummaryTypeDef",
    "ResourceGatewaySummaryTypeDef",
    "ResponseMetadataTypeDef",
    "RuleActionOutputTypeDef",
    "RuleActionTypeDef",
    "RuleActionUnionTypeDef",
    "RuleMatchOutputTypeDef",
    "RuleMatchTypeDef",
    "RuleMatchUnionTypeDef",
    "RuleSummaryTypeDef",
    "RuleUpdateFailureTypeDef",
    "RuleUpdateSuccessTypeDef",
    "RuleUpdateTypeDef",
    "ServiceNetworkEndpointAssociationTypeDef",
    "ServiceNetworkResourceAssociationSummaryTypeDef",
    "ServiceNetworkServiceAssociationSummaryTypeDef",
    "ServiceNetworkSummaryTypeDef",
    "ServiceNetworkVpcAssociationSummaryTypeDef",
    "ServiceSummaryTypeDef",
    "SharingConfigTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TargetFailureTypeDef",
    "TargetGroupConfigTypeDef",
    "TargetGroupSummaryTypeDef",
    "TargetSummaryTypeDef",
    "TargetTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccessLogSubscriptionRequestRequestTypeDef",
    "UpdateAccessLogSubscriptionResponseTypeDef",
    "UpdateListenerRequestRequestTypeDef",
    "UpdateListenerResponseTypeDef",
    "UpdateResourceConfigurationRequestRequestTypeDef",
    "UpdateResourceConfigurationResponseTypeDef",
    "UpdateResourceGatewayRequestRequestTypeDef",
    "UpdateResourceGatewayResponseTypeDef",
    "UpdateRuleRequestRequestTypeDef",
    "UpdateRuleResponseTypeDef",
    "UpdateServiceNetworkRequestRequestTypeDef",
    "UpdateServiceNetworkResponseTypeDef",
    "UpdateServiceNetworkVpcAssociationRequestRequestTypeDef",
    "UpdateServiceNetworkVpcAssociationResponseTypeDef",
    "UpdateServiceRequestRequestTypeDef",
    "UpdateServiceResponseTypeDef",
    "UpdateTargetGroupRequestRequestTypeDef",
    "UpdateTargetGroupResponseTypeDef",
    "WeightedTargetGroupTypeDef",
)

AccessLogSubscriptionSummaryTypeDef = TypedDict(
    "AccessLogSubscriptionSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "destinationArn": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "resourceArn": str,
        "resourceId": str,
        "serviceNetworkLogType": NotRequired[ServiceNetworkLogTypeType],
    },
)

class ArnResourceTypeDef(TypedDict):
    arn: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class RuleUpdateFailureTypeDef(TypedDict):
    failureCode: NotRequired[str]
    failureMessage: NotRequired[str]
    ruleIdentifier: NotRequired[str]

class CreateAccessLogSubscriptionRequestRequestTypeDef(TypedDict):
    destinationArn: str
    resourceIdentifier: str
    clientToken: NotRequired[str]
    serviceNetworkLogType: NotRequired[ServiceNetworkLogTypeType]
    tags: NotRequired[Mapping[str, str]]

class CreateResourceGatewayRequestRequestTypeDef(TypedDict):
    name: str
    subnetIds: Sequence[str]
    vpcIdentifier: str
    clientToken: NotRequired[str]
    ipAddressType: NotRequired[ResourceGatewayIpAddressTypeType]
    securityGroupIds: NotRequired[Sequence[str]]
    tags: NotRequired[Mapping[str, str]]

class SharingConfigTypeDef(TypedDict):
    enabled: NotRequired[bool]

class CreateServiceNetworkResourceAssociationRequestRequestTypeDef(TypedDict):
    resourceConfigurationIdentifier: str
    serviceNetworkIdentifier: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CreateServiceNetworkServiceAssociationRequestRequestTypeDef(TypedDict):
    serviceIdentifier: str
    serviceNetworkIdentifier: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class DnsEntryTypeDef(TypedDict):
    domainName: NotRequired[str]
    hostedZoneId: NotRequired[str]

class CreateServiceNetworkVpcAssociationRequestRequestTypeDef(TypedDict):
    serviceNetworkIdentifier: str
    vpcIdentifier: str
    clientToken: NotRequired[str]
    securityGroupIds: NotRequired[Sequence[str]]
    tags: NotRequired[Mapping[str, str]]

class CreateServiceRequestRequestTypeDef(TypedDict):
    name: str
    authType: NotRequired[AuthTypeType]
    certificateArn: NotRequired[str]
    clientToken: NotRequired[str]
    customDomainName: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class DeleteAccessLogSubscriptionRequestRequestTypeDef(TypedDict):
    accessLogSubscriptionIdentifier: str

class DeleteAuthPolicyRequestRequestTypeDef(TypedDict):
    resourceIdentifier: str

class DeleteListenerRequestRequestTypeDef(TypedDict):
    listenerIdentifier: str
    serviceIdentifier: str

class DeleteResourceConfigurationRequestRequestTypeDef(TypedDict):
    resourceConfigurationIdentifier: str

class DeleteResourceEndpointAssociationRequestRequestTypeDef(TypedDict):
    resourceEndpointAssociationIdentifier: str

class DeleteResourceGatewayRequestRequestTypeDef(TypedDict):
    resourceGatewayIdentifier: str

class DeleteResourcePolicyRequestRequestTypeDef(TypedDict):
    resourceArn: str

class DeleteRuleRequestRequestTypeDef(TypedDict):
    listenerIdentifier: str
    ruleIdentifier: str
    serviceIdentifier: str

class DeleteServiceNetworkRequestRequestTypeDef(TypedDict):
    serviceNetworkIdentifier: str

class DeleteServiceNetworkResourceAssociationRequestRequestTypeDef(TypedDict):
    serviceNetworkResourceAssociationIdentifier: str

class DeleteServiceNetworkServiceAssociationRequestRequestTypeDef(TypedDict):
    serviceNetworkServiceAssociationIdentifier: str

class DeleteServiceNetworkVpcAssociationRequestRequestTypeDef(TypedDict):
    serviceNetworkVpcAssociationIdentifier: str

class DeleteServiceRequestRequestTypeDef(TypedDict):
    serviceIdentifier: str

class DeleteTargetGroupRequestRequestTypeDef(TypedDict):
    targetGroupIdentifier: str

TargetTypeDef = TypedDict(
    "TargetTypeDef",
    {
        "id": str,
        "port": NotRequired[int],
    },
)
TargetFailureTypeDef = TypedDict(
    "TargetFailureTypeDef",
    {
        "failureCode": NotRequired[str],
        "failureMessage": NotRequired[str],
        "id": NotRequired[str],
        "port": NotRequired[int],
    },
)

class DnsResourceTypeDef(TypedDict):
    domainName: NotRequired[str]
    ipAddressType: NotRequired[ResourceConfigurationIpAddressTypeType]

class FixedResponseActionTypeDef(TypedDict):
    statusCode: int

class WeightedTargetGroupTypeDef(TypedDict):
    targetGroupIdentifier: str
    weight: NotRequired[int]

class GetAccessLogSubscriptionRequestRequestTypeDef(TypedDict):
    accessLogSubscriptionIdentifier: str

class GetAuthPolicyRequestRequestTypeDef(TypedDict):
    resourceIdentifier: str

class GetListenerRequestRequestTypeDef(TypedDict):
    listenerIdentifier: str
    serviceIdentifier: str

class GetResourceConfigurationRequestRequestTypeDef(TypedDict):
    resourceConfigurationIdentifier: str

class GetResourceGatewayRequestRequestTypeDef(TypedDict):
    resourceGatewayIdentifier: str

class GetResourcePolicyRequestRequestTypeDef(TypedDict):
    resourceArn: str

class GetRuleRequestRequestTypeDef(TypedDict):
    listenerIdentifier: str
    ruleIdentifier: str
    serviceIdentifier: str

class GetServiceNetworkRequestRequestTypeDef(TypedDict):
    serviceNetworkIdentifier: str

class GetServiceNetworkResourceAssociationRequestRequestTypeDef(TypedDict):
    serviceNetworkResourceAssociationIdentifier: str

class GetServiceNetworkServiceAssociationRequestRequestTypeDef(TypedDict):
    serviceNetworkServiceAssociationIdentifier: str

class GetServiceNetworkVpcAssociationRequestRequestTypeDef(TypedDict):
    serviceNetworkVpcAssociationIdentifier: str

class GetServiceRequestRequestTypeDef(TypedDict):
    serviceIdentifier: str

class GetTargetGroupRequestRequestTypeDef(TypedDict):
    targetGroupIdentifier: str

class HeaderMatchTypeTypeDef(TypedDict):
    contains: NotRequired[str]
    exact: NotRequired[str]
    prefix: NotRequired[str]

class MatcherTypeDef(TypedDict):
    httpCode: NotRequired[str]

class IpResourceTypeDef(TypedDict):
    ipAddress: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAccessLogSubscriptionsRequestRequestTypeDef(TypedDict):
    resourceIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListListenersRequestRequestTypeDef(TypedDict):
    serviceIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

ListenerSummaryTypeDef = TypedDict(
    "ListenerSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "id": NotRequired[str],
        "lastUpdatedAt": NotRequired[datetime],
        "name": NotRequired[str],
        "port": NotRequired[int],
        "protocol": NotRequired[ListenerProtocolType],
    },
)

class ListResourceConfigurationsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    resourceConfigurationGroupIdentifier: NotRequired[str]
    resourceGatewayIdentifier: NotRequired[str]

ResourceConfigurationSummaryTypeDef = TypedDict(
    "ResourceConfigurationSummaryTypeDef",
    {
        "amazonManaged": NotRequired[bool],
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "id": NotRequired[str],
        "lastUpdatedAt": NotRequired[datetime],
        "name": NotRequired[str],
        "resourceConfigurationGroupId": NotRequired[str],
        "resourceGatewayId": NotRequired[str],
        "status": NotRequired[ResourceConfigurationStatusType],
        "type": NotRequired[ResourceConfigurationTypeType],
    },
)

class ListResourceEndpointAssociationsRequestRequestTypeDef(TypedDict):
    resourceConfigurationIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    resourceEndpointAssociationIdentifier: NotRequired[str]
    vpcEndpointId: NotRequired[str]
    vpcEndpointOwner: NotRequired[str]

ResourceEndpointAssociationSummaryTypeDef = TypedDict(
    "ResourceEndpointAssociationSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "id": NotRequired[str],
        "resourceConfigurationArn": NotRequired[str],
        "resourceConfigurationId": NotRequired[str],
        "resourceConfigurationName": NotRequired[str],
        "vpcEndpointId": NotRequired[str],
        "vpcEndpointOwner": NotRequired[str],
    },
)

class ListResourceGatewaysRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

ResourceGatewaySummaryTypeDef = TypedDict(
    "ResourceGatewaySummaryTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "id": NotRequired[str],
        "ipAddressType": NotRequired[ResourceGatewayIpAddressTypeType],
        "lastUpdatedAt": NotRequired[datetime],
        "name": NotRequired[str],
        "securityGroupIds": NotRequired[List[str]],
        "status": NotRequired[ResourceGatewayStatusType],
        "subnetIds": NotRequired[List[str]],
        "vpcIdentifier": NotRequired[str],
    },
)

class ListRulesRequestRequestTypeDef(TypedDict):
    listenerIdentifier: str
    serviceIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

RuleSummaryTypeDef = TypedDict(
    "RuleSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "id": NotRequired[str],
        "isDefault": NotRequired[bool],
        "lastUpdatedAt": NotRequired[datetime],
        "name": NotRequired[str],
        "priority": NotRequired[int],
    },
)

class ListServiceNetworkResourceAssociationsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    resourceConfigurationIdentifier: NotRequired[str]
    serviceNetworkIdentifier: NotRequired[str]

class ListServiceNetworkServiceAssociationsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    serviceIdentifier: NotRequired[str]
    serviceNetworkIdentifier: NotRequired[str]

class ListServiceNetworkVpcAssociationsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    serviceNetworkIdentifier: NotRequired[str]
    vpcIdentifier: NotRequired[str]

ServiceNetworkVpcAssociationSummaryTypeDef = TypedDict(
    "ServiceNetworkVpcAssociationSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "id": NotRequired[str],
        "lastUpdatedAt": NotRequired[datetime],
        "serviceNetworkArn": NotRequired[str],
        "serviceNetworkId": NotRequired[str],
        "serviceNetworkName": NotRequired[str],
        "status": NotRequired[ServiceNetworkVpcAssociationStatusType],
        "vpcId": NotRequired[str],
    },
)

class ListServiceNetworkVpcEndpointAssociationsRequestRequestTypeDef(TypedDict):
    serviceNetworkIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

ServiceNetworkEndpointAssociationTypeDef = TypedDict(
    "ServiceNetworkEndpointAssociationTypeDef",
    {
        "createdAt": NotRequired[datetime],
        "id": NotRequired[str],
        "serviceNetworkArn": NotRequired[str],
        "state": NotRequired[str],
        "vpcEndpointId": NotRequired[str],
        "vpcEndpointOwnerId": NotRequired[str],
        "vpcId": NotRequired[str],
    },
)

class ListServiceNetworksRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

ServiceNetworkSummaryTypeDef = TypedDict(
    "ServiceNetworkSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "id": NotRequired[str],
        "lastUpdatedAt": NotRequired[datetime],
        "name": NotRequired[str],
        "numberOfAssociatedResourceConfigurations": NotRequired[int],
        "numberOfAssociatedServices": NotRequired[int],
        "numberOfAssociatedVPCs": NotRequired[int],
    },
)

class ListServicesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class ListTargetGroupsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    targetGroupType: NotRequired[TargetGroupTypeType]
    vpcIdentifier: NotRequired[str]

TargetGroupSummaryTypeDef = TypedDict(
    "TargetGroupSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "id": NotRequired[str],
        "ipAddressType": NotRequired[IpAddressTypeType],
        "lambdaEventStructureVersion": NotRequired[LambdaEventStructureVersionType],
        "lastUpdatedAt": NotRequired[datetime],
        "name": NotRequired[str],
        "port": NotRequired[int],
        "protocol": NotRequired[TargetGroupProtocolType],
        "serviceArns": NotRequired[List[str]],
        "status": NotRequired[TargetGroupStatusType],
        "type": NotRequired[TargetGroupTypeType],
        "vpcIdentifier": NotRequired[str],
    },
)
TargetSummaryTypeDef = TypedDict(
    "TargetSummaryTypeDef",
    {
        "id": NotRequired[str],
        "port": NotRequired[int],
        "reasonCode": NotRequired[str],
        "status": NotRequired[TargetStatusType],
    },
)

class PathMatchTypeTypeDef(TypedDict):
    exact: NotRequired[str]
    prefix: NotRequired[str]

class PutAuthPolicyRequestRequestTypeDef(TypedDict):
    policy: str
    resourceIdentifier: str

class PutResourcePolicyRequestRequestTypeDef(TypedDict):
    policy: str
    resourceArn: str

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateAccessLogSubscriptionRequestRequestTypeDef(TypedDict):
    accessLogSubscriptionIdentifier: str
    destinationArn: str

class UpdateResourceGatewayRequestRequestTypeDef(TypedDict):
    resourceGatewayIdentifier: str
    securityGroupIds: NotRequired[Sequence[str]]

class UpdateServiceNetworkRequestRequestTypeDef(TypedDict):
    authType: AuthTypeType
    serviceNetworkIdentifier: str

class UpdateServiceNetworkVpcAssociationRequestRequestTypeDef(TypedDict):
    securityGroupIds: Sequence[str]
    serviceNetworkVpcAssociationIdentifier: str

class UpdateServiceRequestRequestTypeDef(TypedDict):
    serviceIdentifier: str
    authType: NotRequired[AuthTypeType]
    certificateArn: NotRequired[str]

CreateAccessLogSubscriptionResponseTypeDef = TypedDict(
    "CreateAccessLogSubscriptionResponseTypeDef",
    {
        "arn": str,
        "destinationArn": str,
        "id": str,
        "resourceArn": str,
        "resourceId": str,
        "serviceNetworkLogType": ServiceNetworkLogTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateResourceGatewayResponseTypeDef = TypedDict(
    "CreateResourceGatewayResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "ipAddressType": ResourceGatewayIpAddressTypeType,
        "name": str,
        "securityGroupIds": List[str],
        "status": ResourceGatewayStatusType,
        "subnetIds": List[str],
        "vpcIdentifier": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateServiceNetworkResourceAssociationResponseTypeDef = TypedDict(
    "CreateServiceNetworkResourceAssociationResponseTypeDef",
    {
        "arn": str,
        "createdBy": str,
        "id": str,
        "status": ServiceNetworkResourceAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateServiceNetworkVpcAssociationResponseTypeDef = TypedDict(
    "CreateServiceNetworkVpcAssociationResponseTypeDef",
    {
        "arn": str,
        "createdBy": str,
        "id": str,
        "securityGroupIds": List[str],
        "status": ServiceNetworkVpcAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteResourceEndpointAssociationResponseTypeDef = TypedDict(
    "DeleteResourceEndpointAssociationResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "resourceConfigurationArn": str,
        "resourceConfigurationId": str,
        "vpcEndpointId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteResourceGatewayResponseTypeDef = TypedDict(
    "DeleteResourceGatewayResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "status": ResourceGatewayStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteServiceNetworkResourceAssociationResponseTypeDef = TypedDict(
    "DeleteServiceNetworkResourceAssociationResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "status": ServiceNetworkResourceAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteServiceNetworkServiceAssociationResponseTypeDef = TypedDict(
    "DeleteServiceNetworkServiceAssociationResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "status": ServiceNetworkServiceAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteServiceNetworkVpcAssociationResponseTypeDef = TypedDict(
    "DeleteServiceNetworkVpcAssociationResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "status": ServiceNetworkVpcAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteServiceResponseTypeDef = TypedDict(
    "DeleteServiceResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "status": ServiceStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteTargetGroupResponseTypeDef = TypedDict(
    "DeleteTargetGroupResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "status": TargetGroupStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAccessLogSubscriptionResponseTypeDef = TypedDict(
    "GetAccessLogSubscriptionResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "destinationArn": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "resourceArn": str,
        "resourceId": str,
        "serviceNetworkLogType": ServiceNetworkLogTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetAuthPolicyResponseTypeDef(TypedDict):
    createdAt: datetime
    lastUpdatedAt: datetime
    policy: str
    state: AuthPolicyStateType
    ResponseMetadata: ResponseMetadataTypeDef

GetResourceGatewayResponseTypeDef = TypedDict(
    "GetResourceGatewayResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "ipAddressType": ResourceGatewayIpAddressTypeType,
        "lastUpdatedAt": datetime,
        "name": str,
        "securityGroupIds": List[str],
        "status": ResourceGatewayStatusType,
        "subnetIds": List[str],
        "vpcId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetResourcePolicyResponseTypeDef(TypedDict):
    policy: str
    ResponseMetadata: ResponseMetadataTypeDef

GetServiceNetworkVpcAssociationResponseTypeDef = TypedDict(
    "GetServiceNetworkVpcAssociationResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "createdBy": str,
        "failureCode": str,
        "failureMessage": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "securityGroupIds": List[str],
        "serviceNetworkArn": str,
        "serviceNetworkId": str,
        "serviceNetworkName": str,
        "status": ServiceNetworkVpcAssociationStatusType,
        "vpcId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListAccessLogSubscriptionsResponseTypeDef(TypedDict):
    items: List[AccessLogSubscriptionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutAuthPolicyResponseTypeDef(TypedDict):
    policy: str
    state: AuthPolicyStateType
    ResponseMetadata: ResponseMetadataTypeDef

UpdateAccessLogSubscriptionResponseTypeDef = TypedDict(
    "UpdateAccessLogSubscriptionResponseTypeDef",
    {
        "arn": str,
        "destinationArn": str,
        "id": str,
        "resourceArn": str,
        "resourceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateResourceGatewayResponseTypeDef = TypedDict(
    "UpdateResourceGatewayResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "ipAddressType": IpAddressTypeType,
        "name": str,
        "securityGroupIds": List[str],
        "status": ResourceGatewayStatusType,
        "subnetIds": List[str],
        "vpcId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateServiceNetworkResponseTypeDef = TypedDict(
    "UpdateServiceNetworkResponseTypeDef",
    {
        "arn": str,
        "authType": AuthTypeType,
        "id": str,
        "name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateServiceNetworkVpcAssociationResponseTypeDef = TypedDict(
    "UpdateServiceNetworkVpcAssociationResponseTypeDef",
    {
        "arn": str,
        "createdBy": str,
        "id": str,
        "securityGroupIds": List[str],
        "status": ServiceNetworkVpcAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateServiceResponseTypeDef = TypedDict(
    "UpdateServiceResponseTypeDef",
    {
        "arn": str,
        "authType": AuthTypeType,
        "certificateArn": str,
        "customDomainName": str,
        "id": str,
        "name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateServiceNetworkRequestRequestTypeDef(TypedDict):
    name: str
    authType: NotRequired[AuthTypeType]
    clientToken: NotRequired[str]
    sharingConfig: NotRequired[SharingConfigTypeDef]
    tags: NotRequired[Mapping[str, str]]

CreateServiceNetworkResponseTypeDef = TypedDict(
    "CreateServiceNetworkResponseTypeDef",
    {
        "arn": str,
        "authType": AuthTypeType,
        "id": str,
        "name": str,
        "sharingConfig": SharingConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetServiceNetworkResponseTypeDef = TypedDict(
    "GetServiceNetworkResponseTypeDef",
    {
        "arn": str,
        "authType": AuthTypeType,
        "createdAt": datetime,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "numberOfAssociatedServices": int,
        "numberOfAssociatedVPCs": int,
        "sharingConfig": SharingConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateServiceNetworkServiceAssociationResponseTypeDef = TypedDict(
    "CreateServiceNetworkServiceAssociationResponseTypeDef",
    {
        "arn": str,
        "createdBy": str,
        "customDomainName": str,
        "dnsEntry": DnsEntryTypeDef,
        "id": str,
        "status": ServiceNetworkServiceAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateServiceResponseTypeDef = TypedDict(
    "CreateServiceResponseTypeDef",
    {
        "arn": str,
        "authType": AuthTypeType,
        "certificateArn": str,
        "customDomainName": str,
        "dnsEntry": DnsEntryTypeDef,
        "id": str,
        "name": str,
        "status": ServiceStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetServiceNetworkResourceAssociationResponseTypeDef = TypedDict(
    "GetServiceNetworkResourceAssociationResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "createdBy": str,
        "dnsEntry": DnsEntryTypeDef,
        "failureCode": str,
        "failureReason": str,
        "id": str,
        "isManagedAssociation": bool,
        "lastUpdatedAt": datetime,
        "privateDnsEntry": DnsEntryTypeDef,
        "resourceConfigurationArn": str,
        "resourceConfigurationId": str,
        "resourceConfigurationName": str,
        "serviceNetworkArn": str,
        "serviceNetworkId": str,
        "serviceNetworkName": str,
        "status": ServiceNetworkResourceAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetServiceNetworkServiceAssociationResponseTypeDef = TypedDict(
    "GetServiceNetworkServiceAssociationResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "createdBy": str,
        "customDomainName": str,
        "dnsEntry": DnsEntryTypeDef,
        "failureCode": str,
        "failureMessage": str,
        "id": str,
        "serviceArn": str,
        "serviceId": str,
        "serviceName": str,
        "serviceNetworkArn": str,
        "serviceNetworkId": str,
        "serviceNetworkName": str,
        "status": ServiceNetworkServiceAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetServiceResponseTypeDef = TypedDict(
    "GetServiceResponseTypeDef",
    {
        "arn": str,
        "authType": AuthTypeType,
        "certificateArn": str,
        "createdAt": datetime,
        "customDomainName": str,
        "dnsEntry": DnsEntryTypeDef,
        "failureCode": str,
        "failureMessage": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "status": ServiceStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ServiceNetworkResourceAssociationSummaryTypeDef = TypedDict(
    "ServiceNetworkResourceAssociationSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "dnsEntry": NotRequired[DnsEntryTypeDef],
        "failureCode": NotRequired[str],
        "id": NotRequired[str],
        "isManagedAssociation": NotRequired[bool],
        "privateDnsEntry": NotRequired[DnsEntryTypeDef],
        "resourceConfigurationArn": NotRequired[str],
        "resourceConfigurationId": NotRequired[str],
        "resourceConfigurationName": NotRequired[str],
        "serviceNetworkArn": NotRequired[str],
        "serviceNetworkId": NotRequired[str],
        "serviceNetworkName": NotRequired[str],
        "status": NotRequired[ServiceNetworkResourceAssociationStatusType],
    },
)
ServiceNetworkServiceAssociationSummaryTypeDef = TypedDict(
    "ServiceNetworkServiceAssociationSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "customDomainName": NotRequired[str],
        "dnsEntry": NotRequired[DnsEntryTypeDef],
        "id": NotRequired[str],
        "serviceArn": NotRequired[str],
        "serviceId": NotRequired[str],
        "serviceName": NotRequired[str],
        "serviceNetworkArn": NotRequired[str],
        "serviceNetworkId": NotRequired[str],
        "serviceNetworkName": NotRequired[str],
        "status": NotRequired[ServiceNetworkServiceAssociationStatusType],
    },
)
ServiceSummaryTypeDef = TypedDict(
    "ServiceSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "customDomainName": NotRequired[str],
        "dnsEntry": NotRequired[DnsEntryTypeDef],
        "id": NotRequired[str],
        "lastUpdatedAt": NotRequired[datetime],
        "name": NotRequired[str],
        "status": NotRequired[ServiceStatusType],
    },
)

class DeregisterTargetsRequestRequestTypeDef(TypedDict):
    targetGroupIdentifier: str
    targets: Sequence[TargetTypeDef]

class ListTargetsRequestRequestTypeDef(TypedDict):
    targetGroupIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    targets: NotRequired[Sequence[TargetTypeDef]]

class RegisterTargetsRequestRequestTypeDef(TypedDict):
    targetGroupIdentifier: str
    targets: Sequence[TargetTypeDef]

class DeregisterTargetsResponseTypeDef(TypedDict):
    successful: List[TargetTypeDef]
    unsuccessful: List[TargetFailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterTargetsResponseTypeDef(TypedDict):
    successful: List[TargetTypeDef]
    unsuccessful: List[TargetFailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ForwardActionOutputTypeDef(TypedDict):
    targetGroups: List[WeightedTargetGroupTypeDef]

class ForwardActionTypeDef(TypedDict):
    targetGroups: Sequence[WeightedTargetGroupTypeDef]

class HeaderMatchTypeDef(TypedDict):
    match: HeaderMatchTypeTypeDef
    name: str
    caseSensitive: NotRequired[bool]

class HealthCheckConfigTypeDef(TypedDict):
    enabled: NotRequired[bool]
    healthCheckIntervalSeconds: NotRequired[int]
    healthCheckTimeoutSeconds: NotRequired[int]
    healthyThresholdCount: NotRequired[int]
    matcher: NotRequired[MatcherTypeDef]
    path: NotRequired[str]
    port: NotRequired[int]
    protocol: NotRequired[TargetGroupProtocolType]
    protocolVersion: NotRequired[HealthCheckProtocolVersionType]
    unhealthyThresholdCount: NotRequired[int]

class ResourceConfigurationDefinitionTypeDef(TypedDict):
    arnResource: NotRequired[ArnResourceTypeDef]
    dnsResource: NotRequired[DnsResourceTypeDef]
    ipResource: NotRequired[IpResourceTypeDef]

class ListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef(TypedDict):
    resourceIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListListenersRequestListListenersPaginateTypeDef(TypedDict):
    serviceIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceConfigurationsRequestListResourceConfigurationsPaginateTypeDef(TypedDict):
    resourceConfigurationGroupIdentifier: NotRequired[str]
    resourceGatewayIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceEndpointAssociationsRequestListResourceEndpointAssociationsPaginateTypeDef(
    TypedDict
):
    resourceConfigurationIdentifier: str
    resourceEndpointAssociationIdentifier: NotRequired[str]
    vpcEndpointId: NotRequired[str]
    vpcEndpointOwner: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceGatewaysRequestListResourceGatewaysPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRulesRequestListRulesPaginateTypeDef(TypedDict):
    listenerIdentifier: str
    serviceIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceNetworkResourceAssociationsRequestListServiceNetworkResourceAssociationsPaginateTypeDef(
    TypedDict
):
    resourceConfigurationIdentifier: NotRequired[str]
    serviceNetworkIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceNetworkServiceAssociationsRequestListServiceNetworkServiceAssociationsPaginateTypeDef(
    TypedDict
):
    serviceIdentifier: NotRequired[str]
    serviceNetworkIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceNetworkVpcAssociationsRequestListServiceNetworkVpcAssociationsPaginateTypeDef(
    TypedDict
):
    serviceNetworkIdentifier: NotRequired[str]
    vpcIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceNetworkVpcEndpointAssociationsRequestListServiceNetworkVpcEndpointAssociationsPaginateTypeDef(
    TypedDict
):
    serviceNetworkIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceNetworksRequestListServiceNetworksPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServicesRequestListServicesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTargetGroupsRequestListTargetGroupsPaginateTypeDef(TypedDict):
    targetGroupType: NotRequired[TargetGroupTypeType]
    vpcIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTargetsRequestListTargetsPaginateTypeDef(TypedDict):
    targetGroupIdentifier: str
    targets: NotRequired[Sequence[TargetTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListListenersResponseTypeDef(TypedDict):
    items: List[ListenerSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListResourceConfigurationsResponseTypeDef(TypedDict):
    items: List[ResourceConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListResourceEndpointAssociationsResponseTypeDef(TypedDict):
    items: List[ResourceEndpointAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListResourceGatewaysResponseTypeDef(TypedDict):
    items: List[ResourceGatewaySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListRulesResponseTypeDef(TypedDict):
    items: List[RuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServiceNetworkVpcAssociationsResponseTypeDef(TypedDict):
    items: List[ServiceNetworkVpcAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServiceNetworkVpcEndpointAssociationsResponseTypeDef(TypedDict):
    items: List[ServiceNetworkEndpointAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServiceNetworksResponseTypeDef(TypedDict):
    items: List[ServiceNetworkSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTargetGroupsResponseTypeDef(TypedDict):
    items: List[TargetGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTargetsResponseTypeDef(TypedDict):
    items: List[TargetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PathMatchTypeDef(TypedDict):
    match: PathMatchTypeTypeDef
    caseSensitive: NotRequired[bool]

class ListServiceNetworkResourceAssociationsResponseTypeDef(TypedDict):
    items: List[ServiceNetworkResourceAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServiceNetworkServiceAssociationsResponseTypeDef(TypedDict):
    items: List[ServiceNetworkServiceAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServicesResponseTypeDef(TypedDict):
    items: List[ServiceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class RuleActionOutputTypeDef(TypedDict):
    fixedResponse: NotRequired[FixedResponseActionTypeDef]
    forward: NotRequired[ForwardActionOutputTypeDef]

ForwardActionUnionTypeDef = Union[ForwardActionTypeDef, ForwardActionOutputTypeDef]

class TargetGroupConfigTypeDef(TypedDict):
    healthCheck: NotRequired[HealthCheckConfigTypeDef]
    ipAddressType: NotRequired[IpAddressTypeType]
    lambdaEventStructureVersion: NotRequired[LambdaEventStructureVersionType]
    port: NotRequired[int]
    protocol: NotRequired[TargetGroupProtocolType]
    protocolVersion: NotRequired[TargetGroupProtocolVersionType]
    vpcIdentifier: NotRequired[str]

class UpdateTargetGroupRequestRequestTypeDef(TypedDict):
    healthCheck: HealthCheckConfigTypeDef
    targetGroupIdentifier: str

CreateResourceConfigurationRequestRequestTypeDef = TypedDict(
    "CreateResourceConfigurationRequestRequestTypeDef",
    {
        "name": str,
        "type": ResourceConfigurationTypeType,
        "allowAssociationToShareableServiceNetwork": NotRequired[bool],
        "clientToken": NotRequired[str],
        "portRanges": NotRequired[Sequence[str]],
        "protocol": NotRequired[Literal["TCP"]],
        "resourceConfigurationDefinition": NotRequired[ResourceConfigurationDefinitionTypeDef],
        "resourceConfigurationGroupIdentifier": NotRequired[str],
        "resourceGatewayIdentifier": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
CreateResourceConfigurationResponseTypeDef = TypedDict(
    "CreateResourceConfigurationResponseTypeDef",
    {
        "allowAssociationToShareableServiceNetwork": bool,
        "arn": str,
        "createdAt": datetime,
        "failureReason": str,
        "id": str,
        "name": str,
        "portRanges": List[str],
        "protocol": Literal["TCP"],
        "resourceConfigurationDefinition": ResourceConfigurationDefinitionTypeDef,
        "resourceConfigurationGroupId": str,
        "resourceGatewayId": str,
        "status": ResourceConfigurationStatusType,
        "type": ResourceConfigurationTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetResourceConfigurationResponseTypeDef = TypedDict(
    "GetResourceConfigurationResponseTypeDef",
    {
        "allowAssociationToShareableServiceNetwork": bool,
        "amazonManaged": bool,
        "arn": str,
        "createdAt": datetime,
        "customDomainName": str,
        "failureReason": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "portRanges": List[str],
        "protocol": Literal["TCP"],
        "resourceConfigurationDefinition": ResourceConfigurationDefinitionTypeDef,
        "resourceConfigurationGroupId": str,
        "resourceGatewayId": str,
        "status": ResourceConfigurationStatusType,
        "type": ResourceConfigurationTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class UpdateResourceConfigurationRequestRequestTypeDef(TypedDict):
    resourceConfigurationIdentifier: str
    allowAssociationToShareableServiceNetwork: NotRequired[bool]
    portRanges: NotRequired[Sequence[str]]
    resourceConfigurationDefinition: NotRequired[ResourceConfigurationDefinitionTypeDef]

UpdateResourceConfigurationResponseTypeDef = TypedDict(
    "UpdateResourceConfigurationResponseTypeDef",
    {
        "allowAssociationToShareableServiceNetwork": bool,
        "arn": str,
        "id": str,
        "name": str,
        "portRanges": List[str],
        "protocol": Literal["TCP"],
        "resourceConfigurationDefinition": ResourceConfigurationDefinitionTypeDef,
        "resourceConfigurationGroupId": str,
        "resourceGatewayId": str,
        "status": ResourceConfigurationStatusType,
        "type": ResourceConfigurationTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class HttpMatchOutputTypeDef(TypedDict):
    headerMatches: NotRequired[List[HeaderMatchTypeDef]]
    method: NotRequired[str]
    pathMatch: NotRequired[PathMatchTypeDef]

class HttpMatchTypeDef(TypedDict):
    headerMatches: NotRequired[Sequence[HeaderMatchTypeDef]]
    method: NotRequired[str]
    pathMatch: NotRequired[PathMatchTypeDef]

CreateListenerResponseTypeDef = TypedDict(
    "CreateListenerResponseTypeDef",
    {
        "arn": str,
        "defaultAction": RuleActionOutputTypeDef,
        "id": str,
        "name": str,
        "port": int,
        "protocol": ListenerProtocolType,
        "serviceArn": str,
        "serviceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetListenerResponseTypeDef = TypedDict(
    "GetListenerResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "defaultAction": RuleActionOutputTypeDef,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "port": int,
        "protocol": ListenerProtocolType,
        "serviceArn": str,
        "serviceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateListenerResponseTypeDef = TypedDict(
    "UpdateListenerResponseTypeDef",
    {
        "arn": str,
        "defaultAction": RuleActionOutputTypeDef,
        "id": str,
        "name": str,
        "port": int,
        "protocol": ListenerProtocolType,
        "serviceArn": str,
        "serviceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class RuleActionTypeDef(TypedDict):
    fixedResponse: NotRequired[FixedResponseActionTypeDef]
    forward: NotRequired[ForwardActionUnionTypeDef]

CreateTargetGroupRequestRequestTypeDef = TypedDict(
    "CreateTargetGroupRequestRequestTypeDef",
    {
        "name": str,
        "type": TargetGroupTypeType,
        "clientToken": NotRequired[str],
        "config": NotRequired[TargetGroupConfigTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)
CreateTargetGroupResponseTypeDef = TypedDict(
    "CreateTargetGroupResponseTypeDef",
    {
        "arn": str,
        "config": TargetGroupConfigTypeDef,
        "id": str,
        "name": str,
        "status": TargetGroupStatusType,
        "type": TargetGroupTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTargetGroupResponseTypeDef = TypedDict(
    "GetTargetGroupResponseTypeDef",
    {
        "arn": str,
        "config": TargetGroupConfigTypeDef,
        "createdAt": datetime,
        "failureCode": str,
        "failureMessage": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "serviceArns": List[str],
        "status": TargetGroupStatusType,
        "type": TargetGroupTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateTargetGroupResponseTypeDef = TypedDict(
    "UpdateTargetGroupResponseTypeDef",
    {
        "arn": str,
        "config": TargetGroupConfigTypeDef,
        "id": str,
        "name": str,
        "status": TargetGroupStatusType,
        "type": TargetGroupTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class RuleMatchOutputTypeDef(TypedDict):
    httpMatch: NotRequired[HttpMatchOutputTypeDef]

HttpMatchUnionTypeDef = Union[HttpMatchTypeDef, HttpMatchOutputTypeDef]

class CreateListenerRequestRequestTypeDef(TypedDict):
    defaultAction: RuleActionTypeDef
    name: str
    protocol: ListenerProtocolType
    serviceIdentifier: str
    clientToken: NotRequired[str]
    port: NotRequired[int]
    tags: NotRequired[Mapping[str, str]]

RuleActionUnionTypeDef = Union[RuleActionTypeDef, RuleActionOutputTypeDef]

class UpdateListenerRequestRequestTypeDef(TypedDict):
    defaultAction: RuleActionTypeDef
    listenerIdentifier: str
    serviceIdentifier: str

CreateRuleResponseTypeDef = TypedDict(
    "CreateRuleResponseTypeDef",
    {
        "action": RuleActionOutputTypeDef,
        "arn": str,
        "id": str,
        "match": RuleMatchOutputTypeDef,
        "name": str,
        "priority": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetRuleResponseTypeDef = TypedDict(
    "GetRuleResponseTypeDef",
    {
        "action": RuleActionOutputTypeDef,
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "isDefault": bool,
        "lastUpdatedAt": datetime,
        "match": RuleMatchOutputTypeDef,
        "name": str,
        "priority": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RuleUpdateSuccessTypeDef = TypedDict(
    "RuleUpdateSuccessTypeDef",
    {
        "action": NotRequired[RuleActionOutputTypeDef],
        "arn": NotRequired[str],
        "id": NotRequired[str],
        "isDefault": NotRequired[bool],
        "match": NotRequired[RuleMatchOutputTypeDef],
        "name": NotRequired[str],
        "priority": NotRequired[int],
    },
)
UpdateRuleResponseTypeDef = TypedDict(
    "UpdateRuleResponseTypeDef",
    {
        "action": RuleActionOutputTypeDef,
        "arn": str,
        "id": str,
        "isDefault": bool,
        "match": RuleMatchOutputTypeDef,
        "name": str,
        "priority": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class RuleMatchTypeDef(TypedDict):
    httpMatch: NotRequired[HttpMatchUnionTypeDef]

class BatchUpdateRuleResponseTypeDef(TypedDict):
    successful: List[RuleUpdateSuccessTypeDef]
    unsuccessful: List[RuleUpdateFailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRuleRequestRequestTypeDef(TypedDict):
    action: RuleActionTypeDef
    listenerIdentifier: str
    match: RuleMatchTypeDef
    name: str
    priority: int
    serviceIdentifier: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

RuleMatchUnionTypeDef = Union[RuleMatchTypeDef, RuleMatchOutputTypeDef]

class UpdateRuleRequestRequestTypeDef(TypedDict):
    listenerIdentifier: str
    ruleIdentifier: str
    serviceIdentifier: str
    action: NotRequired[RuleActionTypeDef]
    match: NotRequired[RuleMatchTypeDef]
    priority: NotRequired[int]

class RuleUpdateTypeDef(TypedDict):
    ruleIdentifier: str
    action: NotRequired[RuleActionUnionTypeDef]
    match: NotRequired[RuleMatchUnionTypeDef]
    priority: NotRequired[int]

class BatchUpdateRuleRequestRequestTypeDef(TypedDict):
    listenerIdentifier: str
    rules: Sequence[RuleUpdateTypeDef]
    serviceIdentifier: str
