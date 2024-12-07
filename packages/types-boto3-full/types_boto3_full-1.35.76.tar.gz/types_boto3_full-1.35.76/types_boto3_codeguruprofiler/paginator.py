"""
Type annotations for codeguruprofiler service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguruprofiler/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_codeguruprofiler.client import CodeGuruProfilerClient
    from types_boto3_codeguruprofiler.paginator import (
        ListProfileTimesPaginator,
    )

    session = Session()
    client: CodeGuruProfilerClient = session.client("codeguruprofiler")

    list_profile_times_paginator: ListProfileTimesPaginator = client.get_paginator("list_profile_times")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListProfileTimesRequestListProfileTimesPaginateTypeDef,
    ListProfileTimesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListProfileTimesPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListProfileTimesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/paginator/ListProfileTimes.html#CodeGuruProfiler.Paginator.ListProfileTimes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguruprofiler/paginators/#listprofiletimespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListProfileTimesRequestListProfileTimesPaginateTypeDef]
    ) -> _PageIterator[ListProfileTimesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/paginator/ListProfileTimes.html#CodeGuruProfiler.Paginator.ListProfileTimes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguruprofiler/paginators/#listprofiletimespaginator)
        """
