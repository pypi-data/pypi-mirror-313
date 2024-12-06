"""
Type annotations for iotfleetwise service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_iotfleetwise.client import IoTFleetWiseClient
    from types_boto3_iotfleetwise.paginator import (
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

    session = Session()
    client: IoTFleetWiseClient = session.client("iotfleetwise")

    get_vehicle_status_paginator: GetVehicleStatusPaginator = client.get_paginator("get_vehicle_status")
    list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
    list_decoder_manifest_network_interfaces_paginator: ListDecoderManifestNetworkInterfacesPaginator = client.get_paginator("list_decoder_manifest_network_interfaces")
    list_decoder_manifest_signals_paginator: ListDecoderManifestSignalsPaginator = client.get_paginator("list_decoder_manifest_signals")
    list_decoder_manifests_paginator: ListDecoderManifestsPaginator = client.get_paginator("list_decoder_manifests")
    list_fleets_for_vehicle_paginator: ListFleetsForVehiclePaginator = client.get_paginator("list_fleets_for_vehicle")
    list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
    list_model_manifest_nodes_paginator: ListModelManifestNodesPaginator = client.get_paginator("list_model_manifest_nodes")
    list_model_manifests_paginator: ListModelManifestsPaginator = client.get_paginator("list_model_manifests")
    list_signal_catalog_nodes_paginator: ListSignalCatalogNodesPaginator = client.get_paginator("list_signal_catalog_nodes")
    list_signal_catalogs_paginator: ListSignalCatalogsPaginator = client.get_paginator("list_signal_catalogs")
    list_state_templates_paginator: ListStateTemplatesPaginator = client.get_paginator("list_state_templates")
    list_vehicles_in_fleet_paginator: ListVehiclesInFleetPaginator = client.get_paginator("list_vehicles_in_fleet")
    list_vehicles_paginator: ListVehiclesPaginator = client.get_paginator("list_vehicles")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetVehicleStatusRequestGetVehicleStatusPaginateTypeDef,
    GetVehicleStatusResponseTypeDef,
    ListCampaignsRequestListCampaignsPaginateTypeDef,
    ListCampaignsResponseTypeDef,
    ListDecoderManifestNetworkInterfacesRequestListDecoderManifestNetworkInterfacesPaginateTypeDef,
    ListDecoderManifestNetworkInterfacesResponseTypeDef,
    ListDecoderManifestSignalsRequestListDecoderManifestSignalsPaginateTypeDef,
    ListDecoderManifestSignalsResponsePaginatorTypeDef,
    ListDecoderManifestsRequestListDecoderManifestsPaginateTypeDef,
    ListDecoderManifestsResponseTypeDef,
    ListFleetsForVehicleRequestListFleetsForVehiclePaginateTypeDef,
    ListFleetsForVehicleResponseTypeDef,
    ListFleetsRequestListFleetsPaginateTypeDef,
    ListFleetsResponseTypeDef,
    ListModelManifestNodesRequestListModelManifestNodesPaginateTypeDef,
    ListModelManifestNodesResponseTypeDef,
    ListModelManifestsRequestListModelManifestsPaginateTypeDef,
    ListModelManifestsResponseTypeDef,
    ListSignalCatalogNodesRequestListSignalCatalogNodesPaginateTypeDef,
    ListSignalCatalogNodesResponseTypeDef,
    ListSignalCatalogsRequestListSignalCatalogsPaginateTypeDef,
    ListSignalCatalogsResponseTypeDef,
    ListStateTemplatesRequestListStateTemplatesPaginateTypeDef,
    ListStateTemplatesResponseTypeDef,
    ListVehiclesInFleetRequestListVehiclesInFleetPaginateTypeDef,
    ListVehiclesInFleetResponseTypeDef,
    ListVehiclesRequestListVehiclesPaginateTypeDef,
    ListVehiclesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetVehicleStatusPaginator",
    "ListCampaignsPaginator",
    "ListDecoderManifestNetworkInterfacesPaginator",
    "ListDecoderManifestSignalsPaginator",
    "ListDecoderManifestsPaginator",
    "ListFleetsForVehiclePaginator",
    "ListFleetsPaginator",
    "ListModelManifestNodesPaginator",
    "ListModelManifestsPaginator",
    "ListSignalCatalogNodesPaginator",
    "ListSignalCatalogsPaginator",
    "ListStateTemplatesPaginator",
    "ListVehiclesInFleetPaginator",
    "ListVehiclesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetVehicleStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/GetVehicleStatus.html#IoTFleetWise.Paginator.GetVehicleStatus)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#getvehiclestatuspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetVehicleStatusRequestGetVehicleStatusPaginateTypeDef]
    ) -> _PageIterator[GetVehicleStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/GetVehicleStatus.html#IoTFleetWise.Paginator.GetVehicleStatus.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#getvehiclestatuspaginator)
        """


class ListCampaignsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListCampaigns.html#IoTFleetWise.Paginator.ListCampaigns)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listcampaignspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCampaignsRequestListCampaignsPaginateTypeDef]
    ) -> _PageIterator[ListCampaignsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListCampaigns.html#IoTFleetWise.Paginator.ListCampaigns.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listcampaignspaginator)
        """


class ListDecoderManifestNetworkInterfacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifestNetworkInterfaces.html#IoTFleetWise.Paginator.ListDecoderManifestNetworkInterfaces)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listdecodermanifestnetworkinterfacespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDecoderManifestNetworkInterfacesRequestListDecoderManifestNetworkInterfacesPaginateTypeDef
        ],
    ) -> _PageIterator[ListDecoderManifestNetworkInterfacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifestNetworkInterfaces.html#IoTFleetWise.Paginator.ListDecoderManifestNetworkInterfaces.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listdecodermanifestnetworkinterfacespaginator)
        """


class ListDecoderManifestSignalsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifestSignals.html#IoTFleetWise.Paginator.ListDecoderManifestSignals)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listdecodermanifestsignalspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDecoderManifestSignalsRequestListDecoderManifestSignalsPaginateTypeDef
        ],
    ) -> _PageIterator[ListDecoderManifestSignalsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifestSignals.html#IoTFleetWise.Paginator.ListDecoderManifestSignals.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listdecodermanifestsignalspaginator)
        """


class ListDecoderManifestsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifests.html#IoTFleetWise.Paginator.ListDecoderManifests)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listdecodermanifestspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDecoderManifestsRequestListDecoderManifestsPaginateTypeDef]
    ) -> _PageIterator[ListDecoderManifestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListDecoderManifests.html#IoTFleetWise.Paginator.ListDecoderManifests.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listdecodermanifestspaginator)
        """


class ListFleetsForVehiclePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListFleetsForVehicle.html#IoTFleetWise.Paginator.ListFleetsForVehicle)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listfleetsforvehiclepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFleetsForVehicleRequestListFleetsForVehiclePaginateTypeDef]
    ) -> _PageIterator[ListFleetsForVehicleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListFleetsForVehicle.html#IoTFleetWise.Paginator.ListFleetsForVehicle.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listfleetsforvehiclepaginator)
        """


class ListFleetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListFleets.html#IoTFleetWise.Paginator.ListFleets)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listfleetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFleetsRequestListFleetsPaginateTypeDef]
    ) -> _PageIterator[ListFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListFleets.html#IoTFleetWise.Paginator.ListFleets.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listfleetspaginator)
        """


class ListModelManifestNodesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListModelManifestNodes.html#IoTFleetWise.Paginator.ListModelManifestNodes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listmodelmanifestnodespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelManifestNodesRequestListModelManifestNodesPaginateTypeDef]
    ) -> _PageIterator[ListModelManifestNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListModelManifestNodes.html#IoTFleetWise.Paginator.ListModelManifestNodes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listmodelmanifestnodespaginator)
        """


class ListModelManifestsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListModelManifests.html#IoTFleetWise.Paginator.ListModelManifests)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listmodelmanifestspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelManifestsRequestListModelManifestsPaginateTypeDef]
    ) -> _PageIterator[ListModelManifestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListModelManifests.html#IoTFleetWise.Paginator.ListModelManifests.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listmodelmanifestspaginator)
        """


class ListSignalCatalogNodesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListSignalCatalogNodes.html#IoTFleetWise.Paginator.ListSignalCatalogNodes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listsignalcatalognodespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSignalCatalogNodesRequestListSignalCatalogNodesPaginateTypeDef]
    ) -> _PageIterator[ListSignalCatalogNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListSignalCatalogNodes.html#IoTFleetWise.Paginator.ListSignalCatalogNodes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listsignalcatalognodespaginator)
        """


class ListSignalCatalogsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListSignalCatalogs.html#IoTFleetWise.Paginator.ListSignalCatalogs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listsignalcatalogspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSignalCatalogsRequestListSignalCatalogsPaginateTypeDef]
    ) -> _PageIterator[ListSignalCatalogsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListSignalCatalogs.html#IoTFleetWise.Paginator.ListSignalCatalogs.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listsignalcatalogspaginator)
        """


class ListStateTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListStateTemplates.html#IoTFleetWise.Paginator.ListStateTemplates)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#liststatetemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStateTemplatesRequestListStateTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListStateTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListStateTemplates.html#IoTFleetWise.Paginator.ListStateTemplates.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#liststatetemplatespaginator)
        """


class ListVehiclesInFleetPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListVehiclesInFleet.html#IoTFleetWise.Paginator.ListVehiclesInFleet)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listvehiclesinfleetpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVehiclesInFleetRequestListVehiclesInFleetPaginateTypeDef]
    ) -> _PageIterator[ListVehiclesInFleetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListVehiclesInFleet.html#IoTFleetWise.Paginator.ListVehiclesInFleet.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listvehiclesinfleetpaginator)
        """


class ListVehiclesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListVehicles.html#IoTFleetWise.Paginator.ListVehicles)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listvehiclespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListVehiclesRequestListVehiclesPaginateTypeDef]
    ) -> _PageIterator[ListVehiclesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise/paginator/ListVehicles.html#IoTFleetWise.Paginator.ListVehicles.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleetwise/paginators/#listvehiclespaginator)
        """
