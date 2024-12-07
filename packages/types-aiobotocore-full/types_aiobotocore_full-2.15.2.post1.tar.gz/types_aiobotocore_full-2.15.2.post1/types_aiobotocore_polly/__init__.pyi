"""
Main interface for polly service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_polly import (
        Client,
        DescribeVoicesPaginator,
        ListLexiconsPaginator,
        ListSpeechSynthesisTasksPaginator,
        PollyClient,
    )

    session = get_session()
    async with session.create_client("polly") as client:
        client: PollyClient
        ...


    describe_voices_paginator: DescribeVoicesPaginator = client.get_paginator("describe_voices")
    list_lexicons_paginator: ListLexiconsPaginator = client.get_paginator("list_lexicons")
    list_speech_synthesis_tasks_paginator: ListSpeechSynthesisTasksPaginator = client.get_paginator("list_speech_synthesis_tasks")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import PollyClient
from .paginator import (
    DescribeVoicesPaginator,
    ListLexiconsPaginator,
    ListSpeechSynthesisTasksPaginator,
)

Client = PollyClient

__all__ = (
    "Client",
    "DescribeVoicesPaginator",
    "ListLexiconsPaginator",
    "ListSpeechSynthesisTasksPaginator",
    "PollyClient",
)
