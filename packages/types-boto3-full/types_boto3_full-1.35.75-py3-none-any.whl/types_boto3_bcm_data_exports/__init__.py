"""
Main interface for bcm-data-exports service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_bcm_data_exports import (
        BillingandCostManagementDataExportsClient,
        Client,
        ListExecutionsPaginator,
        ListExportsPaginator,
        ListTablesPaginator,
    )

    session = Session()
    client: BillingandCostManagementDataExportsClient = session.client("bcm-data-exports")

    list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
    list_exports_paginator: ListExportsPaginator = client.get_paginator("list_exports")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import BillingandCostManagementDataExportsClient
from .paginator import ListExecutionsPaginator, ListExportsPaginator, ListTablesPaginator

Client = BillingandCostManagementDataExportsClient


__all__ = (
    "BillingandCostManagementDataExportsClient",
    "Client",
    "ListExecutionsPaginator",
    "ListExportsPaginator",
    "ListTablesPaginator",
)
