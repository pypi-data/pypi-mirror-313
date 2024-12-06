"""
Main interface for connectcases service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_connectcases import (
        Client,
        ConnectCasesClient,
        SearchCasesPaginator,
        SearchRelatedItemsPaginator,
    )

    session = Session()
    client: ConnectCasesClient = session.client("connectcases")

    search_cases_paginator: SearchCasesPaginator = client.get_paginator("search_cases")
    search_related_items_paginator: SearchRelatedItemsPaginator = client.get_paginator("search_related_items")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ConnectCasesClient
from .paginator import SearchCasesPaginator, SearchRelatedItemsPaginator

Client = ConnectCasesClient

__all__ = ("Client", "ConnectCasesClient", "SearchCasesPaginator", "SearchRelatedItemsPaginator")
