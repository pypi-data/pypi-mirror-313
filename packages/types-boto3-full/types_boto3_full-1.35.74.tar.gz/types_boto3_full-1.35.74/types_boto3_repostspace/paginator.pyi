"""
Type annotations for repostspace service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_repostspace.client import RePostPrivateClient
    from types_boto3_repostspace.paginator import (
        ListSpacesPaginator,
    )

    session = Session()
    client: RePostPrivateClient = session.client("repostspace")

    list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListSpacesInputListSpacesPaginateTypeDef, ListSpacesOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListSpacesPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListSpacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/paginator/ListSpaces.html#RePostPrivate.Paginator.ListSpaces)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/paginators/#listspacespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSpacesInputListSpacesPaginateTypeDef]
    ) -> _PageIterator[ListSpacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/paginator/ListSpaces.html#RePostPrivate.Paginator.ListSpaces.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/paginators/#listspacespaginator)
        """
