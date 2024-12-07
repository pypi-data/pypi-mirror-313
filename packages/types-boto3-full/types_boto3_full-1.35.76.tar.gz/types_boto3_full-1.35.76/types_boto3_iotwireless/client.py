"""
Type annotations for iotwireless service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iotwireless.client import IoTWirelessClient

    session = Session()
    client: IoTWirelessClient = session.client("iotwireless")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    AssociateAwsAccountWithPartnerAccountRequestRequestTypeDef,
    AssociateAwsAccountWithPartnerAccountResponseTypeDef,
    AssociateMulticastGroupWithFuotaTaskRequestRequestTypeDef,
    AssociateWirelessDeviceWithFuotaTaskRequestRequestTypeDef,
    AssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef,
    AssociateWirelessDeviceWithThingRequestRequestTypeDef,
    AssociateWirelessGatewayWithCertificateRequestRequestTypeDef,
    AssociateWirelessGatewayWithCertificateResponseTypeDef,
    AssociateWirelessGatewayWithThingRequestRequestTypeDef,
    CancelMulticastGroupSessionRequestRequestTypeDef,
    CreateDestinationRequestRequestTypeDef,
    CreateDestinationResponseTypeDef,
    CreateDeviceProfileRequestRequestTypeDef,
    CreateDeviceProfileResponseTypeDef,
    CreateFuotaTaskRequestRequestTypeDef,
    CreateFuotaTaskResponseTypeDef,
    CreateMulticastGroupRequestRequestTypeDef,
    CreateMulticastGroupResponseTypeDef,
    CreateNetworkAnalyzerConfigurationRequestRequestTypeDef,
    CreateNetworkAnalyzerConfigurationResponseTypeDef,
    CreateServiceProfileRequestRequestTypeDef,
    CreateServiceProfileResponseTypeDef,
    CreateWirelessDeviceRequestRequestTypeDef,
    CreateWirelessDeviceResponseTypeDef,
    CreateWirelessGatewayRequestRequestTypeDef,
    CreateWirelessGatewayResponseTypeDef,
    CreateWirelessGatewayTaskDefinitionRequestRequestTypeDef,
    CreateWirelessGatewayTaskDefinitionResponseTypeDef,
    CreateWirelessGatewayTaskRequestRequestTypeDef,
    CreateWirelessGatewayTaskResponseTypeDef,
    DeleteDestinationRequestRequestTypeDef,
    DeleteDeviceProfileRequestRequestTypeDef,
    DeleteFuotaTaskRequestRequestTypeDef,
    DeleteMulticastGroupRequestRequestTypeDef,
    DeleteNetworkAnalyzerConfigurationRequestRequestTypeDef,
    DeleteQueuedMessagesRequestRequestTypeDef,
    DeleteServiceProfileRequestRequestTypeDef,
    DeleteWirelessDeviceImportTaskRequestRequestTypeDef,
    DeleteWirelessDeviceRequestRequestTypeDef,
    DeleteWirelessGatewayRequestRequestTypeDef,
    DeleteWirelessGatewayTaskDefinitionRequestRequestTypeDef,
    DeleteWirelessGatewayTaskRequestRequestTypeDef,
    DeregisterWirelessDeviceRequestRequestTypeDef,
    DisassociateAwsAccountFromPartnerAccountRequestRequestTypeDef,
    DisassociateMulticastGroupFromFuotaTaskRequestRequestTypeDef,
    DisassociateWirelessDeviceFromFuotaTaskRequestRequestTypeDef,
    DisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef,
    DisassociateWirelessDeviceFromThingRequestRequestTypeDef,
    DisassociateWirelessGatewayFromCertificateRequestRequestTypeDef,
    DisassociateWirelessGatewayFromThingRequestRequestTypeDef,
    GetDestinationRequestRequestTypeDef,
    GetDestinationResponseTypeDef,
    GetDeviceProfileRequestRequestTypeDef,
    GetDeviceProfileResponseTypeDef,
    GetEventConfigurationByResourceTypesResponseTypeDef,
    GetFuotaTaskRequestRequestTypeDef,
    GetFuotaTaskResponseTypeDef,
    GetLogLevelsByResourceTypesResponseTypeDef,
    GetMetricConfigurationResponseTypeDef,
    GetMetricsRequestRequestTypeDef,
    GetMetricsResponseTypeDef,
    GetMulticastGroupRequestRequestTypeDef,
    GetMulticastGroupResponseTypeDef,
    GetMulticastGroupSessionRequestRequestTypeDef,
    GetMulticastGroupSessionResponseTypeDef,
    GetNetworkAnalyzerConfigurationRequestRequestTypeDef,
    GetNetworkAnalyzerConfigurationResponseTypeDef,
    GetPartnerAccountRequestRequestTypeDef,
    GetPartnerAccountResponseTypeDef,
    GetPositionConfigurationRequestRequestTypeDef,
    GetPositionConfigurationResponseTypeDef,
    GetPositionEstimateRequestRequestTypeDef,
    GetPositionEstimateResponseTypeDef,
    GetPositionRequestRequestTypeDef,
    GetPositionResponseTypeDef,
    GetResourceEventConfigurationRequestRequestTypeDef,
    GetResourceEventConfigurationResponseTypeDef,
    GetResourceLogLevelRequestRequestTypeDef,
    GetResourceLogLevelResponseTypeDef,
    GetResourcePositionRequestRequestTypeDef,
    GetResourcePositionResponseTypeDef,
    GetServiceEndpointRequestRequestTypeDef,
    GetServiceEndpointResponseTypeDef,
    GetServiceProfileRequestRequestTypeDef,
    GetServiceProfileResponseTypeDef,
    GetWirelessDeviceImportTaskRequestRequestTypeDef,
    GetWirelessDeviceImportTaskResponseTypeDef,
    GetWirelessDeviceRequestRequestTypeDef,
    GetWirelessDeviceResponseTypeDef,
    GetWirelessDeviceStatisticsRequestRequestTypeDef,
    GetWirelessDeviceStatisticsResponseTypeDef,
    GetWirelessGatewayCertificateRequestRequestTypeDef,
    GetWirelessGatewayCertificateResponseTypeDef,
    GetWirelessGatewayFirmwareInformationRequestRequestTypeDef,
    GetWirelessGatewayFirmwareInformationResponseTypeDef,
    GetWirelessGatewayRequestRequestTypeDef,
    GetWirelessGatewayResponseTypeDef,
    GetWirelessGatewayStatisticsRequestRequestTypeDef,
    GetWirelessGatewayStatisticsResponseTypeDef,
    GetWirelessGatewayTaskDefinitionRequestRequestTypeDef,
    GetWirelessGatewayTaskDefinitionResponseTypeDef,
    GetWirelessGatewayTaskRequestRequestTypeDef,
    GetWirelessGatewayTaskResponseTypeDef,
    ListDestinationsRequestRequestTypeDef,
    ListDestinationsResponseTypeDef,
    ListDeviceProfilesRequestRequestTypeDef,
    ListDeviceProfilesResponseTypeDef,
    ListDevicesForWirelessDeviceImportTaskRequestRequestTypeDef,
    ListDevicesForWirelessDeviceImportTaskResponseTypeDef,
    ListEventConfigurationsRequestRequestTypeDef,
    ListEventConfigurationsResponseTypeDef,
    ListFuotaTasksRequestRequestTypeDef,
    ListFuotaTasksResponseTypeDef,
    ListMulticastGroupsByFuotaTaskRequestRequestTypeDef,
    ListMulticastGroupsByFuotaTaskResponseTypeDef,
    ListMulticastGroupsRequestRequestTypeDef,
    ListMulticastGroupsResponseTypeDef,
    ListNetworkAnalyzerConfigurationsRequestRequestTypeDef,
    ListNetworkAnalyzerConfigurationsResponseTypeDef,
    ListPartnerAccountsRequestRequestTypeDef,
    ListPartnerAccountsResponseTypeDef,
    ListPositionConfigurationsRequestRequestTypeDef,
    ListPositionConfigurationsResponseTypeDef,
    ListQueuedMessagesRequestRequestTypeDef,
    ListQueuedMessagesResponseTypeDef,
    ListServiceProfilesRequestRequestTypeDef,
    ListServiceProfilesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWirelessDeviceImportTasksRequestRequestTypeDef,
    ListWirelessDeviceImportTasksResponseTypeDef,
    ListWirelessDevicesRequestRequestTypeDef,
    ListWirelessDevicesResponseTypeDef,
    ListWirelessGatewaysRequestRequestTypeDef,
    ListWirelessGatewaysResponseTypeDef,
    ListWirelessGatewayTaskDefinitionsRequestRequestTypeDef,
    ListWirelessGatewayTaskDefinitionsResponseTypeDef,
    PutPositionConfigurationRequestRequestTypeDef,
    PutResourceLogLevelRequestRequestTypeDef,
    ResetResourceLogLevelRequestRequestTypeDef,
    SendDataToMulticastGroupRequestRequestTypeDef,
    SendDataToMulticastGroupResponseTypeDef,
    SendDataToWirelessDeviceRequestRequestTypeDef,
    SendDataToWirelessDeviceResponseTypeDef,
    StartBulkAssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef,
    StartBulkDisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef,
    StartFuotaTaskRequestRequestTypeDef,
    StartMulticastGroupSessionRequestRequestTypeDef,
    StartSingleWirelessDeviceImportTaskRequestRequestTypeDef,
    StartSingleWirelessDeviceImportTaskResponseTypeDef,
    StartWirelessDeviceImportTaskRequestRequestTypeDef,
    StartWirelessDeviceImportTaskResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    TestWirelessDeviceRequestRequestTypeDef,
    TestWirelessDeviceResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDestinationRequestRequestTypeDef,
    UpdateEventConfigurationByResourceTypesRequestRequestTypeDef,
    UpdateFuotaTaskRequestRequestTypeDef,
    UpdateLogLevelsByResourceTypesRequestRequestTypeDef,
    UpdateMetricConfigurationRequestRequestTypeDef,
    UpdateMulticastGroupRequestRequestTypeDef,
    UpdateNetworkAnalyzerConfigurationRequestRequestTypeDef,
    UpdatePartnerAccountRequestRequestTypeDef,
    UpdatePositionRequestRequestTypeDef,
    UpdateResourceEventConfigurationRequestRequestTypeDef,
    UpdateResourcePositionRequestRequestTypeDef,
    UpdateWirelessDeviceImportTaskRequestRequestTypeDef,
    UpdateWirelessDeviceRequestRequestTypeDef,
    UpdateWirelessGatewayRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("IoTWirelessClient",)


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
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class IoTWirelessClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTWirelessClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless.html#IoTWireless.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#close)
        """

    def associate_aws_account_with_partner_account(
        self, **kwargs: Unpack[AssociateAwsAccountWithPartnerAccountRequestRequestTypeDef]
    ) -> AssociateAwsAccountWithPartnerAccountResponseTypeDef:
        """
        Associates a partner account with your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/associate_aws_account_with_partner_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#associate_aws_account_with_partner_account)
        """

    def associate_multicast_group_with_fuota_task(
        self, **kwargs: Unpack[AssociateMulticastGroupWithFuotaTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associate a multicast group with a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/associate_multicast_group_with_fuota_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#associate_multicast_group_with_fuota_task)
        """

    def associate_wireless_device_with_fuota_task(
        self, **kwargs: Unpack[AssociateWirelessDeviceWithFuotaTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associate a wireless device with a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/associate_wireless_device_with_fuota_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#associate_wireless_device_with_fuota_task)
        """

    def associate_wireless_device_with_multicast_group(
        self, **kwargs: Unpack[AssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a wireless device with a multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/associate_wireless_device_with_multicast_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#associate_wireless_device_with_multicast_group)
        """

    def associate_wireless_device_with_thing(
        self, **kwargs: Unpack[AssociateWirelessDeviceWithThingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a wireless device with a thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/associate_wireless_device_with_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#associate_wireless_device_with_thing)
        """

    def associate_wireless_gateway_with_certificate(
        self, **kwargs: Unpack[AssociateWirelessGatewayWithCertificateRequestRequestTypeDef]
    ) -> AssociateWirelessGatewayWithCertificateResponseTypeDef:
        """
        Associates a wireless gateway with a certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/associate_wireless_gateway_with_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#associate_wireless_gateway_with_certificate)
        """

    def associate_wireless_gateway_with_thing(
        self, **kwargs: Unpack[AssociateWirelessGatewayWithThingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a wireless gateway with a thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/associate_wireless_gateway_with_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#associate_wireless_gateway_with_thing)
        """

    def cancel_multicast_group_session(
        self, **kwargs: Unpack[CancelMulticastGroupSessionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels an existing multicast group session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/cancel_multicast_group_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#cancel_multicast_group_session)
        """

    def create_destination(
        self, **kwargs: Unpack[CreateDestinationRequestRequestTypeDef]
    ) -> CreateDestinationResponseTypeDef:
        """
        Creates a new destination that maps a device message to an AWS IoT rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/create_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#create_destination)
        """

    def create_device_profile(
        self, **kwargs: Unpack[CreateDeviceProfileRequestRequestTypeDef]
    ) -> CreateDeviceProfileResponseTypeDef:
        """
        Creates a new device profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/create_device_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#create_device_profile)
        """

    def create_fuota_task(
        self, **kwargs: Unpack[CreateFuotaTaskRequestRequestTypeDef]
    ) -> CreateFuotaTaskResponseTypeDef:
        """
        Creates a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/create_fuota_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#create_fuota_task)
        """

    def create_multicast_group(
        self, **kwargs: Unpack[CreateMulticastGroupRequestRequestTypeDef]
    ) -> CreateMulticastGroupResponseTypeDef:
        """
        Creates a multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/create_multicast_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#create_multicast_group)
        """

    def create_network_analyzer_configuration(
        self, **kwargs: Unpack[CreateNetworkAnalyzerConfigurationRequestRequestTypeDef]
    ) -> CreateNetworkAnalyzerConfigurationResponseTypeDef:
        """
        Creates a new network analyzer configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/create_network_analyzer_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#create_network_analyzer_configuration)
        """

    def create_service_profile(
        self, **kwargs: Unpack[CreateServiceProfileRequestRequestTypeDef]
    ) -> CreateServiceProfileResponseTypeDef:
        """
        Creates a new service profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/create_service_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#create_service_profile)
        """

    def create_wireless_device(
        self, **kwargs: Unpack[CreateWirelessDeviceRequestRequestTypeDef]
    ) -> CreateWirelessDeviceResponseTypeDef:
        """
        Provisions a wireless device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/create_wireless_device.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#create_wireless_device)
        """

    def create_wireless_gateway(
        self, **kwargs: Unpack[CreateWirelessGatewayRequestRequestTypeDef]
    ) -> CreateWirelessGatewayResponseTypeDef:
        """
        Provisions a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/create_wireless_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#create_wireless_gateway)
        """

    def create_wireless_gateway_task(
        self, **kwargs: Unpack[CreateWirelessGatewayTaskRequestRequestTypeDef]
    ) -> CreateWirelessGatewayTaskResponseTypeDef:
        """
        Creates a task for a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/create_wireless_gateway_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#create_wireless_gateway_task)
        """

    def create_wireless_gateway_task_definition(
        self, **kwargs: Unpack[CreateWirelessGatewayTaskDefinitionRequestRequestTypeDef]
    ) -> CreateWirelessGatewayTaskDefinitionResponseTypeDef:
        """
        Creates a gateway task definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/create_wireless_gateway_task_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#create_wireless_gateway_task_definition)
        """

    def delete_destination(
        self, **kwargs: Unpack[DeleteDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/delete_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#delete_destination)
        """

    def delete_device_profile(
        self, **kwargs: Unpack[DeleteDeviceProfileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a device profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/delete_device_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#delete_device_profile)
        """

    def delete_fuota_task(
        self, **kwargs: Unpack[DeleteFuotaTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/delete_fuota_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#delete_fuota_task)
        """

    def delete_multicast_group(
        self, **kwargs: Unpack[DeleteMulticastGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a multicast group if it is not in use by a fuota task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/delete_multicast_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#delete_multicast_group)
        """

    def delete_network_analyzer_configuration(
        self, **kwargs: Unpack[DeleteNetworkAnalyzerConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a network analyzer configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/delete_network_analyzer_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#delete_network_analyzer_configuration)
        """

    def delete_queued_messages(
        self, **kwargs: Unpack[DeleteQueuedMessagesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove queued messages from the downlink queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/delete_queued_messages.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#delete_queued_messages)
        """

    def delete_service_profile(
        self, **kwargs: Unpack[DeleteServiceProfileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a service profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/delete_service_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#delete_service_profile)
        """

    def delete_wireless_device(
        self, **kwargs: Unpack[DeleteWirelessDeviceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a wireless device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/delete_wireless_device.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#delete_wireless_device)
        """

    def delete_wireless_device_import_task(
        self, **kwargs: Unpack[DeleteWirelessDeviceImportTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an import task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/delete_wireless_device_import_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#delete_wireless_device_import_task)
        """

    def delete_wireless_gateway(
        self, **kwargs: Unpack[DeleteWirelessGatewayRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/delete_wireless_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#delete_wireless_gateway)
        """

    def delete_wireless_gateway_task(
        self, **kwargs: Unpack[DeleteWirelessGatewayTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a wireless gateway task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/delete_wireless_gateway_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#delete_wireless_gateway_task)
        """

    def delete_wireless_gateway_task_definition(
        self, **kwargs: Unpack[DeleteWirelessGatewayTaskDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a wireless gateway task definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/delete_wireless_gateway_task_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#delete_wireless_gateway_task_definition)
        """

    def deregister_wireless_device(
        self, **kwargs: Unpack[DeregisterWirelessDeviceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deregister a wireless device from AWS IoT Wireless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/deregister_wireless_device.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#deregister_wireless_device)
        """

    def disassociate_aws_account_from_partner_account(
        self, **kwargs: Unpack[DisassociateAwsAccountFromPartnerAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates your AWS account from a partner account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/disassociate_aws_account_from_partner_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#disassociate_aws_account_from_partner_account)
        """

    def disassociate_multicast_group_from_fuota_task(
        self, **kwargs: Unpack[DisassociateMulticastGroupFromFuotaTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a multicast group from a fuota task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/disassociate_multicast_group_from_fuota_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#disassociate_multicast_group_from_fuota_task)
        """

    def disassociate_wireless_device_from_fuota_task(
        self, **kwargs: Unpack[DisassociateWirelessDeviceFromFuotaTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a wireless device from a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/disassociate_wireless_device_from_fuota_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#disassociate_wireless_device_from_fuota_task)
        """

    def disassociate_wireless_device_from_multicast_group(
        self, **kwargs: Unpack[DisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a wireless device from a multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/disassociate_wireless_device_from_multicast_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#disassociate_wireless_device_from_multicast_group)
        """

    def disassociate_wireless_device_from_thing(
        self, **kwargs: Unpack[DisassociateWirelessDeviceFromThingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a wireless device from its currently associated thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/disassociate_wireless_device_from_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#disassociate_wireless_device_from_thing)
        """

    def disassociate_wireless_gateway_from_certificate(
        self, **kwargs: Unpack[DisassociateWirelessGatewayFromCertificateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a wireless gateway from its currently associated certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/disassociate_wireless_gateway_from_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#disassociate_wireless_gateway_from_certificate)
        """

    def disassociate_wireless_gateway_from_thing(
        self, **kwargs: Unpack[DisassociateWirelessGatewayFromThingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a wireless gateway from its currently associated thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/disassociate_wireless_gateway_from_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#disassociate_wireless_gateway_from_thing)
        """

    def get_destination(
        self, **kwargs: Unpack[GetDestinationRequestRequestTypeDef]
    ) -> GetDestinationResponseTypeDef:
        """
        Gets information about a destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_destination)
        """

    def get_device_profile(
        self, **kwargs: Unpack[GetDeviceProfileRequestRequestTypeDef]
    ) -> GetDeviceProfileResponseTypeDef:
        """
        Gets information about a device profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_device_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_device_profile)
        """

    def get_event_configuration_by_resource_types(
        self,
    ) -> GetEventConfigurationByResourceTypesResponseTypeDef:
        """
        Get the event configuration based on resource types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_event_configuration_by_resource_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_event_configuration_by_resource_types)
        """

    def get_fuota_task(
        self, **kwargs: Unpack[GetFuotaTaskRequestRequestTypeDef]
    ) -> GetFuotaTaskResponseTypeDef:
        """
        Gets information about a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_fuota_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_fuota_task)
        """

    def get_log_levels_by_resource_types(self) -> GetLogLevelsByResourceTypesResponseTypeDef:
        """
        Returns current default log levels or log levels by resource types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_log_levels_by_resource_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_log_levels_by_resource_types)
        """

    def get_metric_configuration(self) -> GetMetricConfigurationResponseTypeDef:
        """
        Get the metric configuration status for this AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_metric_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_metric_configuration)
        """

    def get_metrics(
        self, **kwargs: Unpack[GetMetricsRequestRequestTypeDef]
    ) -> GetMetricsResponseTypeDef:
        """
        Get the summary metrics for this AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_metrics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_metrics)
        """

    def get_multicast_group(
        self, **kwargs: Unpack[GetMulticastGroupRequestRequestTypeDef]
    ) -> GetMulticastGroupResponseTypeDef:
        """
        Gets information about a multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_multicast_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_multicast_group)
        """

    def get_multicast_group_session(
        self, **kwargs: Unpack[GetMulticastGroupSessionRequestRequestTypeDef]
    ) -> GetMulticastGroupSessionResponseTypeDef:
        """
        Gets information about a multicast group session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_multicast_group_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_multicast_group_session)
        """

    def get_network_analyzer_configuration(
        self, **kwargs: Unpack[GetNetworkAnalyzerConfigurationRequestRequestTypeDef]
    ) -> GetNetworkAnalyzerConfigurationResponseTypeDef:
        """
        Get network analyzer configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_network_analyzer_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_network_analyzer_configuration)
        """

    def get_partner_account(
        self, **kwargs: Unpack[GetPartnerAccountRequestRequestTypeDef]
    ) -> GetPartnerAccountResponseTypeDef:
        """
        Gets information about a partner account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_partner_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_partner_account)
        """

    def get_position(
        self, **kwargs: Unpack[GetPositionRequestRequestTypeDef]
    ) -> GetPositionResponseTypeDef:
        """
        Get the position information for a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_position.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_position)
        """

    def get_position_configuration(
        self, **kwargs: Unpack[GetPositionConfigurationRequestRequestTypeDef]
    ) -> GetPositionConfigurationResponseTypeDef:
        """
        Get position configuration for a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_position_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_position_configuration)
        """

    def get_position_estimate(
        self, **kwargs: Unpack[GetPositionEstimateRequestRequestTypeDef]
    ) -> GetPositionEstimateResponseTypeDef:
        """
        Get estimated position information as a payload in GeoJSON format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_position_estimate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_position_estimate)
        """

    def get_resource_event_configuration(
        self, **kwargs: Unpack[GetResourceEventConfigurationRequestRequestTypeDef]
    ) -> GetResourceEventConfigurationResponseTypeDef:
        """
        Get the event configuration for a particular resource identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_resource_event_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_resource_event_configuration)
        """

    def get_resource_log_level(
        self, **kwargs: Unpack[GetResourceLogLevelRequestRequestTypeDef]
    ) -> GetResourceLogLevelResponseTypeDef:
        """
        Fetches the log-level override, if any, for a given resource-ID and
        resource-type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_resource_log_level.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_resource_log_level)
        """

    def get_resource_position(
        self, **kwargs: Unpack[GetResourcePositionRequestRequestTypeDef]
    ) -> GetResourcePositionResponseTypeDef:
        """
        Get the position information for a given wireless device or a wireless gateway
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_resource_position.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_resource_position)
        """

    def get_service_endpoint(
        self, **kwargs: Unpack[GetServiceEndpointRequestRequestTypeDef]
    ) -> GetServiceEndpointResponseTypeDef:
        """
        Gets the account-specific endpoint for Configuration and Update Server (CUPS)
        protocol or LoRaWAN Network Server (LNS) connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_service_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_service_endpoint)
        """

    def get_service_profile(
        self, **kwargs: Unpack[GetServiceProfileRequestRequestTypeDef]
    ) -> GetServiceProfileResponseTypeDef:
        """
        Gets information about a service profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_service_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_service_profile)
        """

    def get_wireless_device(
        self, **kwargs: Unpack[GetWirelessDeviceRequestRequestTypeDef]
    ) -> GetWirelessDeviceResponseTypeDef:
        """
        Gets information about a wireless device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_wireless_device.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_wireless_device)
        """

    def get_wireless_device_import_task(
        self, **kwargs: Unpack[GetWirelessDeviceImportTaskRequestRequestTypeDef]
    ) -> GetWirelessDeviceImportTaskResponseTypeDef:
        """
        Get information about an import task and count of device onboarding summary
        information for the import task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_wireless_device_import_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_wireless_device_import_task)
        """

    def get_wireless_device_statistics(
        self, **kwargs: Unpack[GetWirelessDeviceStatisticsRequestRequestTypeDef]
    ) -> GetWirelessDeviceStatisticsResponseTypeDef:
        """
        Gets operating information about a wireless device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_wireless_device_statistics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_wireless_device_statistics)
        """

    def get_wireless_gateway(
        self, **kwargs: Unpack[GetWirelessGatewayRequestRequestTypeDef]
    ) -> GetWirelessGatewayResponseTypeDef:
        """
        Gets information about a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_wireless_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_wireless_gateway)
        """

    def get_wireless_gateway_certificate(
        self, **kwargs: Unpack[GetWirelessGatewayCertificateRequestRequestTypeDef]
    ) -> GetWirelessGatewayCertificateResponseTypeDef:
        """
        Gets the ID of the certificate that is currently associated with a wireless
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_wireless_gateway_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_wireless_gateway_certificate)
        """

    def get_wireless_gateway_firmware_information(
        self, **kwargs: Unpack[GetWirelessGatewayFirmwareInformationRequestRequestTypeDef]
    ) -> GetWirelessGatewayFirmwareInformationResponseTypeDef:
        """
        Gets the firmware version and other information about a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_wireless_gateway_firmware_information.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_wireless_gateway_firmware_information)
        """

    def get_wireless_gateway_statistics(
        self, **kwargs: Unpack[GetWirelessGatewayStatisticsRequestRequestTypeDef]
    ) -> GetWirelessGatewayStatisticsResponseTypeDef:
        """
        Gets operating information about a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_wireless_gateway_statistics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_wireless_gateway_statistics)
        """

    def get_wireless_gateway_task(
        self, **kwargs: Unpack[GetWirelessGatewayTaskRequestRequestTypeDef]
    ) -> GetWirelessGatewayTaskResponseTypeDef:
        """
        Gets information about a wireless gateway task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_wireless_gateway_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_wireless_gateway_task)
        """

    def get_wireless_gateway_task_definition(
        self, **kwargs: Unpack[GetWirelessGatewayTaskDefinitionRequestRequestTypeDef]
    ) -> GetWirelessGatewayTaskDefinitionResponseTypeDef:
        """
        Gets information about a wireless gateway task definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/get_wireless_gateway_task_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#get_wireless_gateway_task_definition)
        """

    def list_destinations(
        self, **kwargs: Unpack[ListDestinationsRequestRequestTypeDef]
    ) -> ListDestinationsResponseTypeDef:
        """
        Lists the destinations registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_destinations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_destinations)
        """

    def list_device_profiles(
        self, **kwargs: Unpack[ListDeviceProfilesRequestRequestTypeDef]
    ) -> ListDeviceProfilesResponseTypeDef:
        """
        Lists the device profiles registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_device_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_device_profiles)
        """

    def list_devices_for_wireless_device_import_task(
        self, **kwargs: Unpack[ListDevicesForWirelessDeviceImportTaskRequestRequestTypeDef]
    ) -> ListDevicesForWirelessDeviceImportTaskResponseTypeDef:
        """
        List the Sidewalk devices in an import task and their onboarding status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_devices_for_wireless_device_import_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_devices_for_wireless_device_import_task)
        """

    def list_event_configurations(
        self, **kwargs: Unpack[ListEventConfigurationsRequestRequestTypeDef]
    ) -> ListEventConfigurationsResponseTypeDef:
        """
        List event configurations where at least one event topic has been enabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_event_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_event_configurations)
        """

    def list_fuota_tasks(
        self, **kwargs: Unpack[ListFuotaTasksRequestRequestTypeDef]
    ) -> ListFuotaTasksResponseTypeDef:
        """
        Lists the FUOTA tasks registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_fuota_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_fuota_tasks)
        """

    def list_multicast_groups(
        self, **kwargs: Unpack[ListMulticastGroupsRequestRequestTypeDef]
    ) -> ListMulticastGroupsResponseTypeDef:
        """
        Lists the multicast groups registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_multicast_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_multicast_groups)
        """

    def list_multicast_groups_by_fuota_task(
        self, **kwargs: Unpack[ListMulticastGroupsByFuotaTaskRequestRequestTypeDef]
    ) -> ListMulticastGroupsByFuotaTaskResponseTypeDef:
        """
        List all multicast groups associated with a fuota task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_multicast_groups_by_fuota_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_multicast_groups_by_fuota_task)
        """

    def list_network_analyzer_configurations(
        self, **kwargs: Unpack[ListNetworkAnalyzerConfigurationsRequestRequestTypeDef]
    ) -> ListNetworkAnalyzerConfigurationsResponseTypeDef:
        """
        Lists the network analyzer configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_network_analyzer_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_network_analyzer_configurations)
        """

    def list_partner_accounts(
        self, **kwargs: Unpack[ListPartnerAccountsRequestRequestTypeDef]
    ) -> ListPartnerAccountsResponseTypeDef:
        """
        Lists the partner accounts associated with your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_partner_accounts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_partner_accounts)
        """

    def list_position_configurations(
        self, **kwargs: Unpack[ListPositionConfigurationsRequestRequestTypeDef]
    ) -> ListPositionConfigurationsResponseTypeDef:
        """
        List position configurations for a given resource, such as positioning solvers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_position_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_position_configurations)
        """

    def list_queued_messages(
        self, **kwargs: Unpack[ListQueuedMessagesRequestRequestTypeDef]
    ) -> ListQueuedMessagesResponseTypeDef:
        """
        List queued messages in the downlink queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_queued_messages.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_queued_messages)
        """

    def list_service_profiles(
        self, **kwargs: Unpack[ListServiceProfilesRequestRequestTypeDef]
    ) -> ListServiceProfilesResponseTypeDef:
        """
        Lists the service profiles registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_service_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_service_profiles)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags (metadata) you have assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_tags_for_resource)
        """

    def list_wireless_device_import_tasks(
        self, **kwargs: Unpack[ListWirelessDeviceImportTasksRequestRequestTypeDef]
    ) -> ListWirelessDeviceImportTasksResponseTypeDef:
        """
        List wireless devices that have been added to an import task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_wireless_device_import_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_wireless_device_import_tasks)
        """

    def list_wireless_devices(
        self, **kwargs: Unpack[ListWirelessDevicesRequestRequestTypeDef]
    ) -> ListWirelessDevicesResponseTypeDef:
        """
        Lists the wireless devices registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_wireless_devices.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_wireless_devices)
        """

    def list_wireless_gateway_task_definitions(
        self, **kwargs: Unpack[ListWirelessGatewayTaskDefinitionsRequestRequestTypeDef]
    ) -> ListWirelessGatewayTaskDefinitionsResponseTypeDef:
        """
        List the wireless gateway tasks definitions registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_wireless_gateway_task_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_wireless_gateway_task_definitions)
        """

    def list_wireless_gateways(
        self, **kwargs: Unpack[ListWirelessGatewaysRequestRequestTypeDef]
    ) -> ListWirelessGatewaysResponseTypeDef:
        """
        Lists the wireless gateways registered to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/list_wireless_gateways.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#list_wireless_gateways)
        """

    def put_position_configuration(
        self, **kwargs: Unpack[PutPositionConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Put position configuration for a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/put_position_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#put_position_configuration)
        """

    def put_resource_log_level(
        self, **kwargs: Unpack[PutResourceLogLevelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the log-level override for a resource-ID and resource-type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/put_resource_log_level.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#put_resource_log_level)
        """

    def reset_all_resource_log_levels(self) -> Dict[str, Any]:
        """
        Removes the log-level overrides for all resources; wireless devices, wireless
        gateways, and fuota tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/reset_all_resource_log_levels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#reset_all_resource_log_levels)
        """

    def reset_resource_log_level(
        self, **kwargs: Unpack[ResetResourceLogLevelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the log-level override, if any, for a specific resource-ID and
        resource-type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/reset_resource_log_level.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#reset_resource_log_level)
        """

    def send_data_to_multicast_group(
        self, **kwargs: Unpack[SendDataToMulticastGroupRequestRequestTypeDef]
    ) -> SendDataToMulticastGroupResponseTypeDef:
        """
        Sends the specified data to a multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/send_data_to_multicast_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#send_data_to_multicast_group)
        """

    def send_data_to_wireless_device(
        self, **kwargs: Unpack[SendDataToWirelessDeviceRequestRequestTypeDef]
    ) -> SendDataToWirelessDeviceResponseTypeDef:
        """
        Sends a decrypted application data frame to a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/send_data_to_wireless_device.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#send_data_to_wireless_device)
        """

    def start_bulk_associate_wireless_device_with_multicast_group(
        self,
        **kwargs: Unpack[StartBulkAssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef],
    ) -> Dict[str, Any]:
        """
        Starts a bulk association of all qualifying wireless devices with a multicast
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/start_bulk_associate_wireless_device_with_multicast_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#start_bulk_associate_wireless_device_with_multicast_group)
        """

    def start_bulk_disassociate_wireless_device_from_multicast_group(
        self,
        **kwargs: Unpack[
            StartBulkDisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef
        ],
    ) -> Dict[str, Any]:
        """
        Starts a bulk disassociatin of all qualifying wireless devices from a multicast
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/start_bulk_disassociate_wireless_device_from_multicast_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#start_bulk_disassociate_wireless_device_from_multicast_group)
        """

    def start_fuota_task(
        self, **kwargs: Unpack[StartFuotaTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/start_fuota_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#start_fuota_task)
        """

    def start_multicast_group_session(
        self, **kwargs: Unpack[StartMulticastGroupSessionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts a multicast group session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/start_multicast_group_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#start_multicast_group_session)
        """

    def start_single_wireless_device_import_task(
        self, **kwargs: Unpack[StartSingleWirelessDeviceImportTaskRequestRequestTypeDef]
    ) -> StartSingleWirelessDeviceImportTaskResponseTypeDef:
        """
        Start import task for a single wireless device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/start_single_wireless_device_import_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#start_single_wireless_device_import_task)
        """

    def start_wireless_device_import_task(
        self, **kwargs: Unpack[StartWirelessDeviceImportTaskRequestRequestTypeDef]
    ) -> StartWirelessDeviceImportTaskResponseTypeDef:
        """
        Start import task for provisioning Sidewalk devices in bulk using an S3 CSV
        file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/start_wireless_device_import_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#start_wireless_device_import_task)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#tag_resource)
        """

    def test_wireless_device(
        self, **kwargs: Unpack[TestWirelessDeviceRequestRequestTypeDef]
    ) -> TestWirelessDeviceResponseTypeDef:
        """
        Simulates a provisioned device by sending an uplink data payload of
        <code>Hello</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/test_wireless_device.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#test_wireless_device)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#untag_resource)
        """

    def update_destination(
        self, **kwargs: Unpack[UpdateDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates properties of a destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_destination)
        """

    def update_event_configuration_by_resource_types(
        self, **kwargs: Unpack[UpdateEventConfigurationByResourceTypesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update the event configuration based on resource types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_event_configuration_by_resource_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_event_configuration_by_resource_types)
        """

    def update_fuota_task(
        self, **kwargs: Unpack[UpdateFuotaTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates properties of a FUOTA task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_fuota_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_fuota_task)
        """

    def update_log_levels_by_resource_types(
        self, **kwargs: Unpack[UpdateLogLevelsByResourceTypesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Set default log level, or log levels by resource types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_log_levels_by_resource_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_log_levels_by_resource_types)
        """

    def update_metric_configuration(
        self, **kwargs: Unpack[UpdateMetricConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update the summary metric configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_metric_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_metric_configuration)
        """

    def update_multicast_group(
        self, **kwargs: Unpack[UpdateMulticastGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates properties of a multicast group session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_multicast_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_multicast_group)
        """

    def update_network_analyzer_configuration(
        self, **kwargs: Unpack[UpdateNetworkAnalyzerConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update network analyzer configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_network_analyzer_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_network_analyzer_configuration)
        """

    def update_partner_account(
        self, **kwargs: Unpack[UpdatePartnerAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates properties of a partner account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_partner_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_partner_account)
        """

    def update_position(
        self, **kwargs: Unpack[UpdatePositionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update the position information of a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_position.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_position)
        """

    def update_resource_event_configuration(
        self, **kwargs: Unpack[UpdateResourceEventConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update the event configuration for a particular resource identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_resource_event_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_resource_event_configuration)
        """

    def update_resource_position(
        self, **kwargs: Unpack[UpdateResourcePositionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update the position information of a given wireless device or a wireless
        gateway resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_resource_position.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_resource_position)
        """

    def update_wireless_device(
        self, **kwargs: Unpack[UpdateWirelessDeviceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates properties of a wireless device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_wireless_device.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_wireless_device)
        """

    def update_wireless_device_import_task(
        self, **kwargs: Unpack[UpdateWirelessDeviceImportTaskRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update an import task to add more devices to the task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_wireless_device_import_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_wireless_device_import_task)
        """

    def update_wireless_gateway(
        self, **kwargs: Unpack[UpdateWirelessGatewayRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates properties of a wireless gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotwireless/client/update_wireless_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotwireless/client/#update_wireless_gateway)
        """
