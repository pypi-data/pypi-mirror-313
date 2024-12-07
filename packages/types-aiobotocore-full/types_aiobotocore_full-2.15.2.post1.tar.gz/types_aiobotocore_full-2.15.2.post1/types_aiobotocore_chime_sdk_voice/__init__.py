"""
Main interface for chime-sdk-voice service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime_sdk_voice import (
        ChimeSDKVoiceClient,
        Client,
        ListSipMediaApplicationsPaginator,
        ListSipRulesPaginator,
    )

    session = get_session()
    async with session.create_client("chime-sdk-voice") as client:
        client: ChimeSDKVoiceClient
        ...


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
