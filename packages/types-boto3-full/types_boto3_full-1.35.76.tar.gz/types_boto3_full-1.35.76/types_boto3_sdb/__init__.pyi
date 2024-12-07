"""
Main interface for sdb service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sdb import (
        Client,
        ListDomainsPaginator,
        SelectPaginator,
        SimpleDBClient,
    )

    session = Session()
    client: SimpleDBClient = session.client("sdb")

    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    select_paginator: SelectPaginator = client.get_paginator("select")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SimpleDBClient
from .paginator import ListDomainsPaginator, SelectPaginator

Client = SimpleDBClient

__all__ = ("Client", "ListDomainsPaginator", "SelectPaginator", "SimpleDBClient")
