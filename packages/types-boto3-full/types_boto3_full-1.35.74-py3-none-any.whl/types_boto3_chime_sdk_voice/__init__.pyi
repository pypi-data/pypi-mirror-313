"""
Main interface for chime-sdk-voice service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_chime_sdk_voice import (
        ChimeSDKVoiceClient,
        Client,
        ListSipMediaApplicationsPaginator,
        ListSipRulesPaginator,
    )

    session = Session()
    client: ChimeSDKVoiceClient = session.client("chime-sdk-voice")

    list_sip_media_applications_paginator: ListSipMediaApplicationsPaginator = client.get_paginator("list_sip_media_applications")
    list_sip_rules_paginator: ListSipRulesPaginator = client.get_paginator("list_sip_rules")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ChimeSDKVoiceClient
from .paginator import ListSipMediaApplicationsPaginator, ListSipRulesPaginator

Client = ChimeSDKVoiceClient

__all__ = (
    "ChimeSDKVoiceClient",
    "Client",
    "ListSipMediaApplicationsPaginator",
    "ListSipRulesPaginator",
)
