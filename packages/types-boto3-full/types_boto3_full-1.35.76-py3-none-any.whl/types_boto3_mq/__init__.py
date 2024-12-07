"""
Main interface for mq service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_mq import (
        Client,
        ListBrokersPaginator,
        MQClient,
    )

    session = Session()
    client: MQClient = session.client("mq")

    list_brokers_paginator: ListBrokersPaginator = client.get_paginator("list_brokers")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MQClient
from .paginator import ListBrokersPaginator

Client = MQClient


__all__ = ("Client", "ListBrokersPaginator", "MQClient")
