"""
Main interface for iotevents-data service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iotevents_data import (
        Client,
        IoTEventsDataClient,
    )

    session = Session()
    client: IoTEventsDataClient = session.client("iotevents-data")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import IoTEventsDataClient

Client = IoTEventsDataClient

__all__ = ("Client", "IoTEventsDataClient")
