"""
Main interface for sms-voice service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sms_voice import (
        Client,
        PinpointSMSVoiceClient,
    )

    session = get_session()
    async with session.create_client("sms-voice") as client:
        client: PinpointSMSVoiceClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import PinpointSMSVoiceClient

Client = PinpointSMSVoiceClient


__all__ = ("Client", "PinpointSMSVoiceClient")
