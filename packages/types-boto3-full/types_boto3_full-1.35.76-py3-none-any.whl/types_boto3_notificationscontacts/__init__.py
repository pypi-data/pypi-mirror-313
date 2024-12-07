"""
Main interface for notificationscontacts service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_notificationscontacts import (
        Client,
        ListEmailContactsPaginator,
        UserNotificationsContactsClient,
    )

    session = Session()
    client: UserNotificationsContactsClient = session.client("notificationscontacts")

    list_email_contacts_paginator: ListEmailContactsPaginator = client.get_paginator("list_email_contacts")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import UserNotificationsContactsClient
from .paginator import ListEmailContactsPaginator

Client = UserNotificationsContactsClient


__all__ = ("Client", "ListEmailContactsPaginator", "UserNotificationsContactsClient")
