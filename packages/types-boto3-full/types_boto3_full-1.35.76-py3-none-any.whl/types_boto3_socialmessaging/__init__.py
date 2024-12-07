"""
Main interface for socialmessaging service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_socialmessaging import (
        Client,
        EndUserMessagingSocialClient,
        ListLinkedWhatsAppBusinessAccountsPaginator,
    )

    session = Session()
    client: EndUserMessagingSocialClient = session.client("socialmessaging")

    list_linked_whatsapp_business_accounts_paginator: ListLinkedWhatsAppBusinessAccountsPaginator = client.get_paginator("list_linked_whatsapp_business_accounts")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import EndUserMessagingSocialClient
from .paginator import ListLinkedWhatsAppBusinessAccountsPaginator

Client = EndUserMessagingSocialClient


__all__ = ("Client", "EndUserMessagingSocialClient", "ListLinkedWhatsAppBusinessAccountsPaginator")
