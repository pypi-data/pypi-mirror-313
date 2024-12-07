"""
Main interface for supplychain service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_supplychain import (
        Client,
        ListDataIntegrationFlowsPaginator,
        ListDataLakeDatasetsPaginator,
        ListInstancesPaginator,
        SupplyChainClient,
    )

    session = Session()
    client: SupplyChainClient = session.client("supplychain")

    list_data_integration_flows_paginator: ListDataIntegrationFlowsPaginator = client.get_paginator("list_data_integration_flows")
    list_data_lake_datasets_paginator: ListDataLakeDatasetsPaginator = client.get_paginator("list_data_lake_datasets")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SupplyChainClient
from .paginator import (
    ListDataIntegrationFlowsPaginator,
    ListDataLakeDatasetsPaginator,
    ListInstancesPaginator,
)

Client = SupplyChainClient

__all__ = (
    "Client",
    "ListDataIntegrationFlowsPaginator",
    "ListDataLakeDatasetsPaginator",
    "ListInstancesPaginator",
    "SupplyChainClient",
)
