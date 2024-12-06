"""
Type annotations for arc-zonal-shift service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_arc_zonal_shift/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_arc_zonal_shift.client import ARCZonalShiftClient
    from types_boto3_arc_zonal_shift.paginator import (
        ListAutoshiftsPaginator,
        ListManagedResourcesPaginator,
        ListZonalShiftsPaginator,
    )

    session = Session()
    client: ARCZonalShiftClient = session.client("arc-zonal-shift")

    list_autoshifts_paginator: ListAutoshiftsPaginator = client.get_paginator("list_autoshifts")
    list_managed_resources_paginator: ListManagedResourcesPaginator = client.get_paginator("list_managed_resources")
    list_zonal_shifts_paginator: ListZonalShiftsPaginator = client.get_paginator("list_zonal_shifts")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAutoshiftsRequestListAutoshiftsPaginateTypeDef,
    ListAutoshiftsResponseTypeDef,
    ListManagedResourcesRequestListManagedResourcesPaginateTypeDef,
    ListManagedResourcesResponseTypeDef,
    ListZonalShiftsRequestListZonalShiftsPaginateTypeDef,
    ListZonalShiftsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAutoshiftsPaginator", "ListManagedResourcesPaginator", "ListZonalShiftsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAutoshiftsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListAutoshifts.html#ARCZonalShift.Paginator.ListAutoshifts)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_arc_zonal_shift/paginators/#listautoshiftspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAutoshiftsRequestListAutoshiftsPaginateTypeDef]
    ) -> _PageIterator[ListAutoshiftsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListAutoshifts.html#ARCZonalShift.Paginator.ListAutoshifts.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_arc_zonal_shift/paginators/#listautoshiftspaginator)
        """

class ListManagedResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListManagedResources.html#ARCZonalShift.Paginator.ListManagedResources)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_arc_zonal_shift/paginators/#listmanagedresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListManagedResourcesRequestListManagedResourcesPaginateTypeDef]
    ) -> _PageIterator[ListManagedResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListManagedResources.html#ARCZonalShift.Paginator.ListManagedResources.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_arc_zonal_shift/paginators/#listmanagedresourcespaginator)
        """

class ListZonalShiftsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListZonalShifts.html#ARCZonalShift.Paginator.ListZonalShifts)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_arc_zonal_shift/paginators/#listzonalshiftspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListZonalShiftsRequestListZonalShiftsPaginateTypeDef]
    ) -> _PageIterator[ListZonalShiftsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListZonalShifts.html#ARCZonalShift.Paginator.ListZonalShifts.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_arc_zonal_shift/paginators/#listzonalshiftspaginator)
        """
