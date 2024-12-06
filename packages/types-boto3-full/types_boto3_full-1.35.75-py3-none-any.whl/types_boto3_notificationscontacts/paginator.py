"""
Type annotations for notificationscontacts service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_notificationscontacts/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_notificationscontacts.client import UserNotificationsContactsClient
    from types_boto3_notificationscontacts.paginator import (
        ListEmailContactsPaginator,
    )

    session = Session()
    client: UserNotificationsContactsClient = session.client("notificationscontacts")

    list_email_contacts_paginator: ListEmailContactsPaginator = client.get_paginator("list_email_contacts")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListEmailContactsRequestListEmailContactsPaginateTypeDef,
    ListEmailContactsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListEmailContactsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEmailContactsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/paginator/ListEmailContacts.html#UserNotificationsContacts.Paginator.ListEmailContacts)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_notificationscontacts/paginators/#listemailcontactspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEmailContactsRequestListEmailContactsPaginateTypeDef]
    ) -> _PageIterator[ListEmailContactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/paginator/ListEmailContacts.html#UserNotificationsContacts.Paginator.ListEmailContacts.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_notificationscontacts/paginators/#listemailcontactspaginator)
        """
