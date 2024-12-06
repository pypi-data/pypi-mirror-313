"""
Main interface for pinpoint-sms-voice service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_pinpoint_sms_voice import (
        Client,
        PinpointSMSVoiceClient,
    )

    session = Session()
    client: PinpointSMSVoiceClient = session.client("pinpoint-sms-voice")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import PinpointSMSVoiceClient

Client = PinpointSMSVoiceClient

__all__ = ("Client", "PinpointSMSVoiceClient")
