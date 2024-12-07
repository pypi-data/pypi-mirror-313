"""
Main interface for connectcampaigns service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connectcampaigns import (
        Client,
        ConnectCampaignServiceClient,
        ListCampaignsPaginator,
    )

    session = get_session()
    async with session.create_client("connectcampaigns") as client:
        client: ConnectCampaignServiceClient
        ...


    list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ConnectCampaignServiceClient
from .paginator import ListCampaignsPaginator

Client = ConnectCampaignServiceClient

__all__ = ("Client", "ConnectCampaignServiceClient", "ListCampaignsPaginator")
