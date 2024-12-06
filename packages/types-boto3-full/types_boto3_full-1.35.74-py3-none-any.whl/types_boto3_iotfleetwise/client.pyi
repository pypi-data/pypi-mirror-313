"""
Type annotations for iotfleetwise service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iotfleetwise.client import IoTFleetWiseClient

    session = Session()
    client: IoTFleetWiseClient = session.client("iotfleetwise")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetVehicleStatusPaginator,
    ListCampaignsPaginator,
    ListDecoderManifestNetworkInterfacesPaginator,
    ListDecoderManifestSignalsPaginator,
    ListDecoderManifestsPaginator,
    ListFleetsForVehiclePaginator,
    ListFleetsPaginator,
    ListModelManifestNodesPaginator,
    ListModelManifestsPaginator,
    ListSignalCatalogNodesPaginator,
    ListSignalCatalogsPaginator,
    ListStateTemplatesPaginator,
    ListVehiclesInFleetPaginator,
    ListVehiclesPaginator,
)
from .type_defs import (
    AssociateVehicleFleetRequestRequestTypeDef,
    BatchCreateVehicleRequestRequestTypeDef,
    BatchCreateVehicleResponseTypeDef,
    BatchUpdateVehicleRequestRequestTypeDef,
    BatchUpdateVehicleResponseTypeDef,
    CreateCampaignRequestRequestTypeDef,
    CreateCampaignResponseTypeDef,
    CreateDecoderManifestRequestRequestTypeDef,
    CreateDecoderManifestResponseTypeDef,
    CreateFleetRequestRequestTypeDef,
    CreateFleetResponseTypeDef,
    CreateModelManifestRequestRequestTypeDef,
    CreateModelManifestResponseTypeDef,
    CreateSignalCatalogRequestRequestTypeDef,
    CreateSignalCatalogResponseTypeDef,
    CreateStateTemplateRequestRequestTypeDef,
    CreateStateTemplateResponseTypeDef,
    CreateVehicleRequestRequestTypeDef,
    CreateVehicleResponseTypeDef,
    DeleteCampaignRequestRequestTypeDef,
    DeleteCampaignResponseTypeDef,
    DeleteDecoderManifestRequestRequestTypeDef,
    DeleteDecoderManifestResponseTypeDef,
    DeleteFleetRequestRequestTypeDef,
    DeleteFleetResponseTypeDef,
    DeleteModelManifestRequestRequestTypeDef,
    DeleteModelManifestResponseTypeDef,
    DeleteSignalCatalogRequestRequestTypeDef,
    DeleteSignalCatalogResponseTypeDef,
    DeleteStateTemplateRequestRequestTypeDef,
    DeleteStateTemplateResponseTypeDef,
    DeleteVehicleRequestRequestTypeDef,
    DeleteVehicleResponseTypeDef,
    DisassociateVehicleFleetRequestRequestTypeDef,
    GetCampaignRequestRequestTypeDef,
    GetCampaignResponseTypeDef,
    GetDecoderManifestRequestRequestTypeDef,
    GetDecoderManifestResponseTypeDef,
    GetEncryptionConfigurationResponseTypeDef,
    GetFleetRequestRequestTypeDef,
    GetFleetResponseTypeDef,
    GetLoggingOptionsResponseTypeDef,
    GetModelManifestRequestRequestTypeDef,
    GetModelManifestResponseTypeDef,
    GetRegisterAccountStatusResponseTypeDef,
    GetSignalCatalogRequestRequestTypeDef,
    GetSignalCatalogResponseTypeDef,
    GetStateTemplateRequestRequestTypeDef,
    GetStateTemplateResponseTypeDef,
    GetVehicleRequestRequestTypeDef,
    GetVehicleResponseTypeDef,
    GetVehicleStatusRequestRequestTypeDef,
    GetVehicleStatusResponseTypeDef,
    ImportDecoderManifestRequestRequestTypeDef,
    ImportDecoderManifestResponseTypeDef,
    ImportSignalCatalogRequestRequestTypeDef,
    ImportSignalCatalogResponseTypeDef,
    ListCampaignsRequestRequestTypeDef,
    ListCampaignsResponseTypeDef,
    ListDecoderManifestNetworkInterfacesRequestRequestTypeDef,
    ListDecoderManifestNetworkInterfacesResponseTypeDef,
    ListDecoderManifestSignalsRequestRequestTypeDef,
    ListDecoderManifestSignalsResponseTypeDef,
    ListDecoderManifestsRequestRequestTypeDef,
    ListDecoderManifestsResponseTypeDef,
    ListFleetsForVehicleRequestRequestTypeDef,
    ListFleetsForVehicleResponseTypeDef,
    ListFleetsRequestRequestTypeDef,
    ListFleetsResponseTypeDef,
    ListModelManifestNodesRequestRequestTypeDef,
    ListModelManifestNodesResponseTypeDef,
    ListModelManifestsRequestRequestTypeDef,
    ListModelManifestsResponseTypeDef,
    ListSignalCatalogNodesRequestRequestTypeDef,
    ListSignalCatalogNodesResponseTypeDef,
    ListSignalCatalogsRequestRequestTypeDef,
    ListSignalCatalogsResponseTypeDef,
    ListStateTemplatesRequestRequestTypeDef,
    ListStateTemplatesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVehiclesInFleetRequestRequestTypeDef,
    ListVehiclesInFleetResponseTypeDef,
    ListVehiclesRequestRequestTypeDef,
    ListVehiclesResponseTypeDef,
    PutEncryptionConfigurationRequestRequestTypeDef,
    PutEncryptionConfigurationResponseTypeDef,
    PutLoggingOptionsRequestRequestTypeDef,
    RegisterAccountRequestRequestTypeDef,
    RegisterAccountResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateCampaignRequestRequestTypeDef,
    UpdateCampaignResponseTypeDef,
    UpdateDecoderManifestRequestRequestTypeDef,
    UpdateDecoderManifestResponseTypeDef,
    UpdateFleetRequestRequestTypeDef,
    UpdateFleetResponseTypeDef,
    UpdateModelManifestRequestRequestTypeDef,
    UpdateModelManifestResponseTypeDef,
    UpdateSignalCatalogRequestRequestTypeDef,
    UpdateSignalCatalogResponseTypeDef,
    UpdateStateTemplateRequestRequestTypeDef,
    UpdateStateTemplateResponseTypeDef,
    UpdateVehicleRequestRequestTypeDef,
    UpdateVehicleResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("IoTFleetWiseClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DecoderManifestValidationException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidNodeException: Type[BotocoreClientError]
    InvalidSignalsException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class IoTFleetWiseClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTFleetWiseClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#close)
        """

    def associate_vehicle_fleet(
        self, **kwargs: Unpack[AssociateVehicleFleetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds, or associates, a vehicle with a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/associate_vehicle_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#associate_vehicle_fleet)
        """

    def batch_create_vehicle(
        self, **kwargs: Unpack[BatchCreateVehicleRequestRequestTypeDef]
    ) -> BatchCreateVehicleResponseTypeDef:
        """
        Creates a group, or batch, of vehicles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/batch_create_vehicle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#batch_create_vehicle)
        """

    def batch_update_vehicle(
        self, **kwargs: Unpack[BatchUpdateVehicleRequestRequestTypeDef]
    ) -> BatchUpdateVehicleResponseTypeDef:
        """
        Updates a group, or batch, of vehicles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/batch_update_vehicle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#batch_update_vehicle)
        """

    def create_campaign(
        self, **kwargs: Unpack[CreateCampaignRequestRequestTypeDef]
    ) -> CreateCampaignResponseTypeDef:
        """
        Creates an orchestration of data collection rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/create_campaign.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#create_campaign)
        """

    def create_decoder_manifest(
        self, **kwargs: Unpack[CreateDecoderManifestRequestRequestTypeDef]
    ) -> CreateDecoderManifestResponseTypeDef:
        """
        Creates the decoder manifest associated with a model manifest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/create_decoder_manifest.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#create_decoder_manifest)
        """

    def create_fleet(
        self, **kwargs: Unpack[CreateFleetRequestRequestTypeDef]
    ) -> CreateFleetResponseTypeDef:
        """
        Creates a fleet that represents a group of vehicles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/create_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#create_fleet)
        """

    def create_model_manifest(
        self, **kwargs: Unpack[CreateModelManifestRequestRequestTypeDef]
    ) -> CreateModelManifestResponseTypeDef:
        """
        Creates a vehicle model (model manifest) that specifies signals (attributes,
        branches, sensors, and actuators).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/create_model_manifest.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#create_model_manifest)
        """

    def create_signal_catalog(
        self, **kwargs: Unpack[CreateSignalCatalogRequestRequestTypeDef]
    ) -> CreateSignalCatalogResponseTypeDef:
        """
        Creates a collection of standardized signals that can be reused to create
        vehicle models.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/create_signal_catalog.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#create_signal_catalog)
        """

    def create_state_template(
        self, **kwargs: Unpack[CreateStateTemplateRequestRequestTypeDef]
    ) -> CreateStateTemplateResponseTypeDef:
        """
        Creates a state template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/create_state_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#create_state_template)
        """

    def create_vehicle(
        self, **kwargs: Unpack[CreateVehicleRequestRequestTypeDef]
    ) -> CreateVehicleResponseTypeDef:
        """
        Creates a vehicle, which is an instance of a vehicle model (model manifest).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/create_vehicle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#create_vehicle)
        """

    def delete_campaign(
        self, **kwargs: Unpack[DeleteCampaignRequestRequestTypeDef]
    ) -> DeleteCampaignResponseTypeDef:
        """
        Deletes a data collection campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/delete_campaign.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#delete_campaign)
        """

    def delete_decoder_manifest(
        self, **kwargs: Unpack[DeleteDecoderManifestRequestRequestTypeDef]
    ) -> DeleteDecoderManifestResponseTypeDef:
        """
        Deletes a decoder manifest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/delete_decoder_manifest.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#delete_decoder_manifest)
        """

    def delete_fleet(
        self, **kwargs: Unpack[DeleteFleetRequestRequestTypeDef]
    ) -> DeleteFleetResponseTypeDef:
        """
        Deletes a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/delete_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#delete_fleet)
        """

    def delete_model_manifest(
        self, **kwargs: Unpack[DeleteModelManifestRequestRequestTypeDef]
    ) -> DeleteModelManifestResponseTypeDef:
        """
        Deletes a vehicle model (model manifest).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/delete_model_manifest.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#delete_model_manifest)
        """

    def delete_signal_catalog(
        self, **kwargs: Unpack[DeleteSignalCatalogRequestRequestTypeDef]
    ) -> DeleteSignalCatalogResponseTypeDef:
        """
        Deletes a signal catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/delete_signal_catalog.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#delete_signal_catalog)
        """

    def delete_state_template(
        self, **kwargs: Unpack[DeleteStateTemplateRequestRequestTypeDef]
    ) -> DeleteStateTemplateResponseTypeDef:
        """
        Deletes a state template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/delete_state_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#delete_state_template)
        """

    def delete_vehicle(
        self, **kwargs: Unpack[DeleteVehicleRequestRequestTypeDef]
    ) -> DeleteVehicleResponseTypeDef:
        """
        Deletes a vehicle and removes it from any campaigns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/delete_vehicle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#delete_vehicle)
        """

    def disassociate_vehicle_fleet(
        self, **kwargs: Unpack[DisassociateVehicleFleetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes, or disassociates, a vehicle from a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/disassociate_vehicle_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#disassociate_vehicle_fleet)
        """

    def get_campaign(
        self, **kwargs: Unpack[GetCampaignRequestRequestTypeDef]
    ) -> GetCampaignResponseTypeDef:
        """
        Retrieves information about a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_campaign.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_campaign)
        """

    def get_decoder_manifest(
        self, **kwargs: Unpack[GetDecoderManifestRequestRequestTypeDef]
    ) -> GetDecoderManifestResponseTypeDef:
        """
        Retrieves information about a created decoder manifest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_decoder_manifest.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_decoder_manifest)
        """

    def get_encryption_configuration(self) -> GetEncryptionConfigurationResponseTypeDef:
        """
        Retrieves the encryption configuration for resources and data in Amazon Web
        Services IoT FleetWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_encryption_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_encryption_configuration)
        """

    def get_fleet(self, **kwargs: Unpack[GetFleetRequestRequestTypeDef]) -> GetFleetResponseTypeDef:
        """
        Retrieves information about a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_fleet)
        """

    def get_logging_options(self) -> GetLoggingOptionsResponseTypeDef:
        """
        Retrieves the logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_logging_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_logging_options)
        """

    def get_model_manifest(
        self, **kwargs: Unpack[GetModelManifestRequestRequestTypeDef]
    ) -> GetModelManifestResponseTypeDef:
        """
        Retrieves information about a vehicle model (model manifest).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_model_manifest.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_model_manifest)
        """

    def get_register_account_status(self) -> GetRegisterAccountStatusResponseTypeDef:
        """
        Retrieves information about the status of registering your Amazon Web Services
        account, IAM, and Amazon Timestream resources so that Amazon Web Services IoT
        FleetWise can transfer your vehicle data to the Amazon Web Services Cloud.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_register_account_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_register_account_status)
        """

    def get_signal_catalog(
        self, **kwargs: Unpack[GetSignalCatalogRequestRequestTypeDef]
    ) -> GetSignalCatalogResponseTypeDef:
        """
        Retrieves information about a signal catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_signal_catalog.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_signal_catalog)
        """

    def get_state_template(
        self, **kwargs: Unpack[GetStateTemplateRequestRequestTypeDef]
    ) -> GetStateTemplateResponseTypeDef:
        """
        Retrieves information about a state template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_state_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_state_template)
        """

    def get_vehicle(
        self, **kwargs: Unpack[GetVehicleRequestRequestTypeDef]
    ) -> GetVehicleResponseTypeDef:
        """
        Retrieves information about a vehicle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_vehicle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_vehicle)
        """

    def get_vehicle_status(
        self, **kwargs: Unpack[GetVehicleStatusRequestRequestTypeDef]
    ) -> GetVehicleStatusResponseTypeDef:
        """
        Retrieves information about the status of campaigns, decoder manifests, or
        state templates associated with a vehicle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_vehicle_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_vehicle_status)
        """

    def import_decoder_manifest(
        self, **kwargs: Unpack[ImportDecoderManifestRequestRequestTypeDef]
    ) -> ImportDecoderManifestResponseTypeDef:
        """
        Creates a decoder manifest using your existing CAN DBC file from your local
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/import_decoder_manifest.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#import_decoder_manifest)
        """

    def import_signal_catalog(
        self, **kwargs: Unpack[ImportSignalCatalogRequestRequestTypeDef]
    ) -> ImportSignalCatalogResponseTypeDef:
        """
        Creates a signal catalog using your existing VSS formatted content from your
        local device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/import_signal_catalog.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#import_signal_catalog)
        """

    def list_campaigns(
        self, **kwargs: Unpack[ListCampaignsRequestRequestTypeDef]
    ) -> ListCampaignsResponseTypeDef:
        """
        Lists information about created campaigns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_campaigns.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_campaigns)
        """

    def list_decoder_manifest_network_interfaces(
        self, **kwargs: Unpack[ListDecoderManifestNetworkInterfacesRequestRequestTypeDef]
    ) -> ListDecoderManifestNetworkInterfacesResponseTypeDef:
        """
        Lists the network interfaces specified in a decoder manifest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_decoder_manifest_network_interfaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_decoder_manifest_network_interfaces)
        """

    def list_decoder_manifest_signals(
        self, **kwargs: Unpack[ListDecoderManifestSignalsRequestRequestTypeDef]
    ) -> ListDecoderManifestSignalsResponseTypeDef:
        """
        A list of information about signal decoders specified in a decoder manifest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_decoder_manifest_signals.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_decoder_manifest_signals)
        """

    def list_decoder_manifests(
        self, **kwargs: Unpack[ListDecoderManifestsRequestRequestTypeDef]
    ) -> ListDecoderManifestsResponseTypeDef:
        """
        Lists decoder manifests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_decoder_manifests.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_decoder_manifests)
        """

    def list_fleets(
        self, **kwargs: Unpack[ListFleetsRequestRequestTypeDef]
    ) -> ListFleetsResponseTypeDef:
        """
        Retrieves information for each created fleet in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_fleets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_fleets)
        """

    def list_fleets_for_vehicle(
        self, **kwargs: Unpack[ListFleetsForVehicleRequestRequestTypeDef]
    ) -> ListFleetsForVehicleResponseTypeDef:
        """
        Retrieves a list of IDs for all fleets that the vehicle is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_fleets_for_vehicle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_fleets_for_vehicle)
        """

    def list_model_manifest_nodes(
        self, **kwargs: Unpack[ListModelManifestNodesRequestRequestTypeDef]
    ) -> ListModelManifestNodesResponseTypeDef:
        """
        Lists information about nodes specified in a vehicle model (model manifest).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_model_manifest_nodes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_model_manifest_nodes)
        """

    def list_model_manifests(
        self, **kwargs: Unpack[ListModelManifestsRequestRequestTypeDef]
    ) -> ListModelManifestsResponseTypeDef:
        """
        Retrieves a list of vehicle models (model manifests).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_model_manifests.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_model_manifests)
        """

    def list_signal_catalog_nodes(
        self, **kwargs: Unpack[ListSignalCatalogNodesRequestRequestTypeDef]
    ) -> ListSignalCatalogNodesResponseTypeDef:
        """
        Lists of information about the signals (nodes) specified in a signal catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_signal_catalog_nodes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_signal_catalog_nodes)
        """

    def list_signal_catalogs(
        self, **kwargs: Unpack[ListSignalCatalogsRequestRequestTypeDef]
    ) -> ListSignalCatalogsResponseTypeDef:
        """
        Lists all the created signal catalogs in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_signal_catalogs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_signal_catalogs)
        """

    def list_state_templates(
        self, **kwargs: Unpack[ListStateTemplatesRequestRequestTypeDef]
    ) -> ListStateTemplatesResponseTypeDef:
        """
        Lists information about created state templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_state_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_state_templates)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags (metadata) you have assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_tags_for_resource)
        """

    def list_vehicles(
        self, **kwargs: Unpack[ListVehiclesRequestRequestTypeDef]
    ) -> ListVehiclesResponseTypeDef:
        """
        Retrieves a list of summaries of created vehicles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_vehicles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_vehicles)
        """

    def list_vehicles_in_fleet(
        self, **kwargs: Unpack[ListVehiclesInFleetRequestRequestTypeDef]
    ) -> ListVehiclesInFleetResponseTypeDef:
        """
        Retrieves a list of summaries of all vehicles associated with a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/list_vehicles_in_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#list_vehicles_in_fleet)
        """

    def put_encryption_configuration(
        self, **kwargs: Unpack[PutEncryptionConfigurationRequestRequestTypeDef]
    ) -> PutEncryptionConfigurationResponseTypeDef:
        """
        Creates or updates the encryption configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/put_encryption_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#put_encryption_configuration)
        """

    def put_logging_options(
        self, **kwargs: Unpack[PutLoggingOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates the logging option.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/put_logging_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#put_logging_options)
        """

    def register_account(
        self, **kwargs: Unpack[RegisterAccountRequestRequestTypeDef]
    ) -> RegisterAccountResponseTypeDef:
        """
        This API operation contains deprecated parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/register_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#register_account)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds to or modifies the tags of the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the given tags (metadata) from the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#untag_resource)
        """

    def update_campaign(
        self, **kwargs: Unpack[UpdateCampaignRequestRequestTypeDef]
    ) -> UpdateCampaignResponseTypeDef:
        """
        Updates a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/update_campaign.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#update_campaign)
        """

    def update_decoder_manifest(
        self, **kwargs: Unpack[UpdateDecoderManifestRequestRequestTypeDef]
    ) -> UpdateDecoderManifestResponseTypeDef:
        """
        Updates a decoder manifest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/update_decoder_manifest.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#update_decoder_manifest)
        """

    def update_fleet(
        self, **kwargs: Unpack[UpdateFleetRequestRequestTypeDef]
    ) -> UpdateFleetResponseTypeDef:
        """
        Updates the description of an existing fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/update_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#update_fleet)
        """

    def update_model_manifest(
        self, **kwargs: Unpack[UpdateModelManifestRequestRequestTypeDef]
    ) -> UpdateModelManifestResponseTypeDef:
        """
        Updates a vehicle model (model manifest).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/update_model_manifest.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#update_model_manifest)
        """

    def update_signal_catalog(
        self, **kwargs: Unpack[UpdateSignalCatalogRequestRequestTypeDef]
    ) -> UpdateSignalCatalogResponseTypeDef:
        """
        Updates a signal catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/update_signal_catalog.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#update_signal_catalog)
        """

    def update_state_template(
        self, **kwargs: Unpack[UpdateStateTemplateRequestRequestTypeDef]
    ) -> UpdateStateTemplateResponseTypeDef:
        """
        Updates a state template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/update_state_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#update_state_template)
        """

    def update_vehicle(
        self, **kwargs: Unpack[UpdateVehicleRequestRequestTypeDef]
    ) -> UpdateVehicleResponseTypeDef:
        """
        Updates a vehicle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/update_vehicle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#update_vehicle)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_vehicle_status"]
    ) -> GetVehicleStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_campaigns"]) -> ListCampaignsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_decoder_manifest_network_interfaces"]
    ) -> ListDecoderManifestNetworkInterfacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_decoder_manifest_signals"]
    ) -> ListDecoderManifestSignalsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_decoder_manifests"]
    ) -> ListDecoderManifestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_fleets_for_vehicle"]
    ) -> ListFleetsForVehiclePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_fleets"]) -> ListFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_manifest_nodes"]
    ) -> ListModelManifestNodesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_manifests"]
    ) -> ListModelManifestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_signal_catalog_nodes"]
    ) -> ListSignalCatalogNodesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_signal_catalogs"]
    ) -> ListSignalCatalogsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_state_templates"]
    ) -> ListStateTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_vehicles_in_fleet"]
    ) -> ListVehiclesInFleetPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_vehicles"]) -> ListVehiclesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/client/#get_paginator)
        """
