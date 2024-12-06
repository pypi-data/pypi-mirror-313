"""
Main interface for cloudhsm service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_cloudhsm import (
        Client,
        CloudHSMClient,
        ListHapgsPaginator,
        ListHsmsPaginator,
        ListLunaClientsPaginator,
    )

    session = Session()
    client: CloudHSMClient = session.client("cloudhsm")

    list_hapgs_paginator: ListHapgsPaginator = client.get_paginator("list_hapgs")
    list_hsms_paginator: ListHsmsPaginator = client.get_paginator("list_hsms")
    list_luna_clients_paginator: ListLunaClientsPaginator = client.get_paginator("list_luna_clients")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudHSMClient
from .paginator import ListHapgsPaginator, ListHsmsPaginator, ListLunaClientsPaginator

Client = CloudHSMClient

__all__ = (
    "Client",
    "CloudHSMClient",
    "ListHapgsPaginator",
    "ListHsmsPaginator",
    "ListLunaClientsPaginator",
)
