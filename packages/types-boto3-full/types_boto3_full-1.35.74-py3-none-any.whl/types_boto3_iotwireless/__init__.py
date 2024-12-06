"""
Main interface for iotwireless service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iotwireless import (
        Client,
        IoTWirelessClient,
    )

    session = Session()
    client: IoTWirelessClient = session.client("iotwireless")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import IoTWirelessClient

Client = IoTWirelessClient


__all__ = ("Client", "IoTWirelessClient")
