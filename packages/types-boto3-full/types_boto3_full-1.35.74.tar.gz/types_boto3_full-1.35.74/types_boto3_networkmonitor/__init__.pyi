"""
Main interface for networkmonitor service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_networkmonitor import (
        Client,
        CloudWatchNetworkMonitorClient,
        ListMonitorsPaginator,
    )

    session = Session()
    client: CloudWatchNetworkMonitorClient = session.client("networkmonitor")

    list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudWatchNetworkMonitorClient
from .paginator import ListMonitorsPaginator

Client = CloudWatchNetworkMonitorClient

__all__ = ("Client", "CloudWatchNetworkMonitorClient", "ListMonitorsPaginator")
