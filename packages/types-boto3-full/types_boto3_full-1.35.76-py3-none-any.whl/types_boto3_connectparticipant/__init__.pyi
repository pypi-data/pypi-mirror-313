"""
Main interface for connectparticipant service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_connectparticipant import (
        Client,
        ConnectParticipantClient,
    )

    session = Session()
    client: ConnectParticipantClient = session.client("connectparticipant")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ConnectParticipantClient

Client = ConnectParticipantClient

__all__ = ("Client", "ConnectParticipantClient")
