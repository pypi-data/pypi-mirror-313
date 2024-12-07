"""
Main interface for iotevents service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iotevents import (
        Client,
        IoTEventsClient,
    )

    session = Session()
    client: IoTEventsClient = session.client("iotevents")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import IoTEventsClient

Client = IoTEventsClient


__all__ = ("Client", "IoTEventsClient")
