"""
Type annotations for mediaconnect service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_mediaconnect.client import MediaConnectClient

    session = Session()
    client: MediaConnectClient = session.client("mediaconnect")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListBridgesPaginator,
    ListEntitlementsPaginator,
    ListFlowsPaginator,
    ListGatewayInstancesPaginator,
    ListGatewaysPaginator,
    ListOfferingsPaginator,
    ListReservationsPaginator,
)
from .type_defs import (
    AddBridgeOutputsRequestRequestTypeDef,
    AddBridgeOutputsResponseTypeDef,
    AddBridgeSourcesRequestRequestTypeDef,
    AddBridgeSourcesResponseTypeDef,
    AddFlowMediaStreamsRequestRequestTypeDef,
    AddFlowMediaStreamsResponseTypeDef,
    AddFlowOutputsRequestRequestTypeDef,
    AddFlowOutputsResponseTypeDef,
    AddFlowSourcesRequestRequestTypeDef,
    AddFlowSourcesResponseTypeDef,
    AddFlowVpcInterfacesRequestRequestTypeDef,
    AddFlowVpcInterfacesResponseTypeDef,
    CreateBridgeRequestRequestTypeDef,
    CreateBridgeResponseTypeDef,
    CreateFlowRequestRequestTypeDef,
    CreateFlowResponseTypeDef,
    CreateGatewayRequestRequestTypeDef,
    CreateGatewayResponseTypeDef,
    DeleteBridgeRequestRequestTypeDef,
    DeleteBridgeResponseTypeDef,
    DeleteFlowRequestRequestTypeDef,
    DeleteFlowResponseTypeDef,
    DeleteGatewayRequestRequestTypeDef,
    DeleteGatewayResponseTypeDef,
    DeregisterGatewayInstanceRequestRequestTypeDef,
    DeregisterGatewayInstanceResponseTypeDef,
    DescribeBridgeRequestRequestTypeDef,
    DescribeBridgeResponseTypeDef,
    DescribeFlowRequestRequestTypeDef,
    DescribeFlowResponseTypeDef,
    DescribeFlowSourceMetadataRequestRequestTypeDef,
    DescribeFlowSourceMetadataResponseTypeDef,
    DescribeFlowSourceThumbnailRequestRequestTypeDef,
    DescribeFlowSourceThumbnailResponseTypeDef,
    DescribeGatewayInstanceRequestRequestTypeDef,
    DescribeGatewayInstanceResponseTypeDef,
    DescribeGatewayRequestRequestTypeDef,
    DescribeGatewayResponseTypeDef,
    DescribeOfferingRequestRequestTypeDef,
    DescribeOfferingResponseTypeDef,
    DescribeReservationRequestRequestTypeDef,
    DescribeReservationResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GrantFlowEntitlementsRequestRequestTypeDef,
    GrantFlowEntitlementsResponseTypeDef,
    ListBridgesRequestRequestTypeDef,
    ListBridgesResponseTypeDef,
    ListEntitlementsRequestRequestTypeDef,
    ListEntitlementsResponseTypeDef,
    ListFlowsRequestRequestTypeDef,
    ListFlowsResponseTypeDef,
    ListGatewayInstancesRequestRequestTypeDef,
    ListGatewayInstancesResponseTypeDef,
    ListGatewaysRequestRequestTypeDef,
    ListGatewaysResponseTypeDef,
    ListOfferingsRequestRequestTypeDef,
    ListOfferingsResponseTypeDef,
    ListReservationsRequestRequestTypeDef,
    ListReservationsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PurchaseOfferingRequestRequestTypeDef,
    PurchaseOfferingResponseTypeDef,
    RemoveBridgeOutputRequestRequestTypeDef,
    RemoveBridgeOutputResponseTypeDef,
    RemoveBridgeSourceRequestRequestTypeDef,
    RemoveBridgeSourceResponseTypeDef,
    RemoveFlowMediaStreamRequestRequestTypeDef,
    RemoveFlowMediaStreamResponseTypeDef,
    RemoveFlowOutputRequestRequestTypeDef,
    RemoveFlowOutputResponseTypeDef,
    RemoveFlowSourceRequestRequestTypeDef,
    RemoveFlowSourceResponseTypeDef,
    RemoveFlowVpcInterfaceRequestRequestTypeDef,
    RemoveFlowVpcInterfaceResponseTypeDef,
    RevokeFlowEntitlementRequestRequestTypeDef,
    RevokeFlowEntitlementResponseTypeDef,
    StartFlowRequestRequestTypeDef,
    StartFlowResponseTypeDef,
    StopFlowRequestRequestTypeDef,
    StopFlowResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateBridgeOutputRequestRequestTypeDef,
    UpdateBridgeOutputResponseTypeDef,
    UpdateBridgeRequestRequestTypeDef,
    UpdateBridgeResponseTypeDef,
    UpdateBridgeSourceRequestRequestTypeDef,
    UpdateBridgeSourceResponseTypeDef,
    UpdateBridgeStateRequestRequestTypeDef,
    UpdateBridgeStateResponseTypeDef,
    UpdateFlowEntitlementRequestRequestTypeDef,
    UpdateFlowEntitlementResponseTypeDef,
    UpdateFlowMediaStreamRequestRequestTypeDef,
    UpdateFlowMediaStreamResponseTypeDef,
    UpdateFlowOutputRequestRequestTypeDef,
    UpdateFlowOutputResponseTypeDef,
    UpdateFlowRequestRequestTypeDef,
    UpdateFlowResponseTypeDef,
    UpdateFlowSourceRequestRequestTypeDef,
    UpdateFlowSourceResponseTypeDef,
    UpdateGatewayInstanceRequestRequestTypeDef,
    UpdateGatewayInstanceResponseTypeDef,
)
from .waiter import FlowActiveWaiter, FlowDeletedWaiter, FlowStandbyWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("MediaConnectClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AddFlowOutputs420Exception: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    CreateBridge420Exception: Type[BotocoreClientError]
    CreateFlow420Exception: Type[BotocoreClientError]
    CreateGateway420Exception: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    GrantFlowEntitlements420Exception: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class MediaConnectClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaConnectClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#close)
        """

    def add_bridge_outputs(
        self, **kwargs: Unpack[AddBridgeOutputsRequestRequestTypeDef]
    ) -> AddBridgeOutputsResponseTypeDef:
        """
        Adds outputs to an existing bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/add_bridge_outputs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#add_bridge_outputs)
        """

    def add_bridge_sources(
        self, **kwargs: Unpack[AddBridgeSourcesRequestRequestTypeDef]
    ) -> AddBridgeSourcesResponseTypeDef:
        """
        Adds sources to an existing bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/add_bridge_sources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#add_bridge_sources)
        """

    def add_flow_media_streams(
        self, **kwargs: Unpack[AddFlowMediaStreamsRequestRequestTypeDef]
    ) -> AddFlowMediaStreamsResponseTypeDef:
        """
        Adds media streams to an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/add_flow_media_streams.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#add_flow_media_streams)
        """

    def add_flow_outputs(
        self, **kwargs: Unpack[AddFlowOutputsRequestRequestTypeDef]
    ) -> AddFlowOutputsResponseTypeDef:
        """
        Adds outputs to an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/add_flow_outputs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#add_flow_outputs)
        """

    def add_flow_sources(
        self, **kwargs: Unpack[AddFlowSourcesRequestRequestTypeDef]
    ) -> AddFlowSourcesResponseTypeDef:
        """
        Adds Sources to flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/add_flow_sources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#add_flow_sources)
        """

    def add_flow_vpc_interfaces(
        self, **kwargs: Unpack[AddFlowVpcInterfacesRequestRequestTypeDef]
    ) -> AddFlowVpcInterfacesResponseTypeDef:
        """
        Adds VPC interfaces to flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/add_flow_vpc_interfaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#add_flow_vpc_interfaces)
        """

    def create_bridge(
        self, **kwargs: Unpack[CreateBridgeRequestRequestTypeDef]
    ) -> CreateBridgeResponseTypeDef:
        """
        Creates a new bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/create_bridge.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#create_bridge)
        """

    def create_flow(
        self, **kwargs: Unpack[CreateFlowRequestRequestTypeDef]
    ) -> CreateFlowResponseTypeDef:
        """
        Creates a new flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/create_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#create_flow)
        """

    def create_gateway(
        self, **kwargs: Unpack[CreateGatewayRequestRequestTypeDef]
    ) -> CreateGatewayResponseTypeDef:
        """
        Creates a new gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/create_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#create_gateway)
        """

    def delete_bridge(
        self, **kwargs: Unpack[DeleteBridgeRequestRequestTypeDef]
    ) -> DeleteBridgeResponseTypeDef:
        """
        Deletes a bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/delete_bridge.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#delete_bridge)
        """

    def delete_flow(
        self, **kwargs: Unpack[DeleteFlowRequestRequestTypeDef]
    ) -> DeleteFlowResponseTypeDef:
        """
        Deletes a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/delete_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#delete_flow)
        """

    def delete_gateway(
        self, **kwargs: Unpack[DeleteGatewayRequestRequestTypeDef]
    ) -> DeleteGatewayResponseTypeDef:
        """
        Deletes a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/delete_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#delete_gateway)
        """

    def deregister_gateway_instance(
        self, **kwargs: Unpack[DeregisterGatewayInstanceRequestRequestTypeDef]
    ) -> DeregisterGatewayInstanceResponseTypeDef:
        """
        Deregisters an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/deregister_gateway_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#deregister_gateway_instance)
        """

    def describe_bridge(
        self, **kwargs: Unpack[DescribeBridgeRequestRequestTypeDef]
    ) -> DescribeBridgeResponseTypeDef:
        """
        Displays the details of a bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/describe_bridge.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#describe_bridge)
        """

    def describe_flow(
        self, **kwargs: Unpack[DescribeFlowRequestRequestTypeDef]
    ) -> DescribeFlowResponseTypeDef:
        """
        Displays the details of a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/describe_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#describe_flow)
        """

    def describe_flow_source_metadata(
        self, **kwargs: Unpack[DescribeFlowSourceMetadataRequestRequestTypeDef]
    ) -> DescribeFlowSourceMetadataResponseTypeDef:
        """
        Displays details of the flow's source stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/describe_flow_source_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#describe_flow_source_metadata)
        """

    def describe_flow_source_thumbnail(
        self, **kwargs: Unpack[DescribeFlowSourceThumbnailRequestRequestTypeDef]
    ) -> DescribeFlowSourceThumbnailResponseTypeDef:
        """
        Displays the thumbnail details of a flow's source stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/describe_flow_source_thumbnail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#describe_flow_source_thumbnail)
        """

    def describe_gateway(
        self, **kwargs: Unpack[DescribeGatewayRequestRequestTypeDef]
    ) -> DescribeGatewayResponseTypeDef:
        """
        Displays the details of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/describe_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#describe_gateway)
        """

    def describe_gateway_instance(
        self, **kwargs: Unpack[DescribeGatewayInstanceRequestRequestTypeDef]
    ) -> DescribeGatewayInstanceResponseTypeDef:
        """
        Displays the details of an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/describe_gateway_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#describe_gateway_instance)
        """

    def describe_offering(
        self, **kwargs: Unpack[DescribeOfferingRequestRequestTypeDef]
    ) -> DescribeOfferingResponseTypeDef:
        """
        Displays the details of an offering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/describe_offering.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#describe_offering)
        """

    def describe_reservation(
        self, **kwargs: Unpack[DescribeReservationRequestRequestTypeDef]
    ) -> DescribeReservationResponseTypeDef:
        """
        Displays the details of a reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/describe_reservation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#describe_reservation)
        """

    def grant_flow_entitlements(
        self, **kwargs: Unpack[GrantFlowEntitlementsRequestRequestTypeDef]
    ) -> GrantFlowEntitlementsResponseTypeDef:
        """
        Grants entitlements to an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/grant_flow_entitlements.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#grant_flow_entitlements)
        """

    def list_bridges(
        self, **kwargs: Unpack[ListBridgesRequestRequestTypeDef]
    ) -> ListBridgesResponseTypeDef:
        """
        Displays a list of bridges that are associated with this account and an
        optionally specified Arn.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/list_bridges.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#list_bridges)
        """

    def list_entitlements(
        self, **kwargs: Unpack[ListEntitlementsRequestRequestTypeDef]
    ) -> ListEntitlementsResponseTypeDef:
        """
        Displays a list of all entitlements that have been granted to this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/list_entitlements.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#list_entitlements)
        """

    def list_flows(
        self, **kwargs: Unpack[ListFlowsRequestRequestTypeDef]
    ) -> ListFlowsResponseTypeDef:
        """
        Displays a list of flows that are associated with this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/list_flows.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#list_flows)
        """

    def list_gateway_instances(
        self, **kwargs: Unpack[ListGatewayInstancesRequestRequestTypeDef]
    ) -> ListGatewayInstancesResponseTypeDef:
        """
        Displays a list of instances associated with the AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/list_gateway_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#list_gateway_instances)
        """

    def list_gateways(
        self, **kwargs: Unpack[ListGatewaysRequestRequestTypeDef]
    ) -> ListGatewaysResponseTypeDef:
        """
        Displays a list of gateways that are associated with this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/list_gateways.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#list_gateways)
        """

    def list_offerings(
        self, **kwargs: Unpack[ListOfferingsRequestRequestTypeDef]
    ) -> ListOfferingsResponseTypeDef:
        """
        Displays a list of all offerings that are available to this account in the
        current AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/list_offerings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#list_offerings)
        """

    def list_reservations(
        self, **kwargs: Unpack[ListReservationsRequestRequestTypeDef]
    ) -> ListReservationsResponseTypeDef:
        """
        Displays a list of all reservations that have been purchased by this account in
        the current AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/list_reservations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#list_reservations)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all tags on an AWS Elemental MediaConnect resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#list_tags_for_resource)
        """

    def purchase_offering(
        self, **kwargs: Unpack[PurchaseOfferingRequestRequestTypeDef]
    ) -> PurchaseOfferingResponseTypeDef:
        """
        Submits a request to purchase an offering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/purchase_offering.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#purchase_offering)
        """

    def remove_bridge_output(
        self, **kwargs: Unpack[RemoveBridgeOutputRequestRequestTypeDef]
    ) -> RemoveBridgeOutputResponseTypeDef:
        """
        Removes an output from a bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/remove_bridge_output.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#remove_bridge_output)
        """

    def remove_bridge_source(
        self, **kwargs: Unpack[RemoveBridgeSourceRequestRequestTypeDef]
    ) -> RemoveBridgeSourceResponseTypeDef:
        """
        Removes a source from a bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/remove_bridge_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#remove_bridge_source)
        """

    def remove_flow_media_stream(
        self, **kwargs: Unpack[RemoveFlowMediaStreamRequestRequestTypeDef]
    ) -> RemoveFlowMediaStreamResponseTypeDef:
        """
        Removes a media stream from a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/remove_flow_media_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#remove_flow_media_stream)
        """

    def remove_flow_output(
        self, **kwargs: Unpack[RemoveFlowOutputRequestRequestTypeDef]
    ) -> RemoveFlowOutputResponseTypeDef:
        """
        Removes an output from an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/remove_flow_output.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#remove_flow_output)
        """

    def remove_flow_source(
        self, **kwargs: Unpack[RemoveFlowSourceRequestRequestTypeDef]
    ) -> RemoveFlowSourceResponseTypeDef:
        """
        Removes a source from an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/remove_flow_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#remove_flow_source)
        """

    def remove_flow_vpc_interface(
        self, **kwargs: Unpack[RemoveFlowVpcInterfaceRequestRequestTypeDef]
    ) -> RemoveFlowVpcInterfaceResponseTypeDef:
        """
        Removes a VPC Interface from an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/remove_flow_vpc_interface.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#remove_flow_vpc_interface)
        """

    def revoke_flow_entitlement(
        self, **kwargs: Unpack[RevokeFlowEntitlementRequestRequestTypeDef]
    ) -> RevokeFlowEntitlementResponseTypeDef:
        """
        Revokes an entitlement from a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/revoke_flow_entitlement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#revoke_flow_entitlement)
        """

    def start_flow(
        self, **kwargs: Unpack[StartFlowRequestRequestTypeDef]
    ) -> StartFlowResponseTypeDef:
        """
        Starts a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/start_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#start_flow)
        """

    def stop_flow(self, **kwargs: Unpack[StopFlowRequestRequestTypeDef]) -> StopFlowResponseTypeDef:
        """
        Stops a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/stop_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#stop_flow)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates the specified tags to a resource with the specified resourceArn.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#untag_resource)
        """

    def update_bridge(
        self, **kwargs: Unpack[UpdateBridgeRequestRequestTypeDef]
    ) -> UpdateBridgeResponseTypeDef:
        """
        Updates the bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/update_bridge.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#update_bridge)
        """

    def update_bridge_output(
        self, **kwargs: Unpack[UpdateBridgeOutputRequestRequestTypeDef]
    ) -> UpdateBridgeOutputResponseTypeDef:
        """
        Updates an existing bridge output.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/update_bridge_output.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#update_bridge_output)
        """

    def update_bridge_source(
        self, **kwargs: Unpack[UpdateBridgeSourceRequestRequestTypeDef]
    ) -> UpdateBridgeSourceResponseTypeDef:
        """
        Updates an existing bridge source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/update_bridge_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#update_bridge_source)
        """

    def update_bridge_state(
        self, **kwargs: Unpack[UpdateBridgeStateRequestRequestTypeDef]
    ) -> UpdateBridgeStateResponseTypeDef:
        """
        Updates the bridge state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/update_bridge_state.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#update_bridge_state)
        """

    def update_flow(
        self, **kwargs: Unpack[UpdateFlowRequestRequestTypeDef]
    ) -> UpdateFlowResponseTypeDef:
        """
        Updates flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/update_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#update_flow)
        """

    def update_flow_entitlement(
        self, **kwargs: Unpack[UpdateFlowEntitlementRequestRequestTypeDef]
    ) -> UpdateFlowEntitlementResponseTypeDef:
        """
        You can change an entitlement's description, subscribers, and encryption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/update_flow_entitlement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#update_flow_entitlement)
        """

    def update_flow_media_stream(
        self, **kwargs: Unpack[UpdateFlowMediaStreamRequestRequestTypeDef]
    ) -> UpdateFlowMediaStreamResponseTypeDef:
        """
        Updates an existing media stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/update_flow_media_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#update_flow_media_stream)
        """

    def update_flow_output(
        self, **kwargs: Unpack[UpdateFlowOutputRequestRequestTypeDef]
    ) -> UpdateFlowOutputResponseTypeDef:
        """
        Updates an existing flow output.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/update_flow_output.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#update_flow_output)
        """

    def update_flow_source(
        self, **kwargs: Unpack[UpdateFlowSourceRequestRequestTypeDef]
    ) -> UpdateFlowSourceResponseTypeDef:
        """
        Updates the source of a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/update_flow_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#update_flow_source)
        """

    def update_gateway_instance(
        self, **kwargs: Unpack[UpdateGatewayInstanceRequestRequestTypeDef]
    ) -> UpdateGatewayInstanceResponseTypeDef:
        """
        Updates the configuration of an existing Gateway Instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/update_gateway_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#update_gateway_instance)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_bridges"]) -> ListBridgesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_entitlements"]
    ) -> ListEntitlementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_flows"]) -> ListFlowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_gateway_instances"]
    ) -> ListGatewayInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_gateways"]) -> ListGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_offerings"]) -> ListOfferingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reservations"]
    ) -> ListReservationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["flow_active"]) -> FlowActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["flow_deleted"]) -> FlowDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["flow_standby"]) -> FlowStandbyWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediaconnect/client/#get_waiter)
        """
