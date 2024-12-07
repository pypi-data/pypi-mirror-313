"""
Main interface for ssm-quicksetup service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ssm_quicksetup import (
        Client,
        ListConfigurationManagersPaginator,
        SystemsManagerQuickSetupClient,
    )

    session = get_session()
    async with session.create_client("ssm-quicksetup") as client:
        client: SystemsManagerQuickSetupClient
        ...


    list_configuration_managers_paginator: ListConfigurationManagersPaginator = client.get_paginator("list_configuration_managers")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SystemsManagerQuickSetupClient
from .paginator import ListConfigurationManagersPaginator

Client = SystemsManagerQuickSetupClient


__all__ = ("Client", "ListConfigurationManagersPaginator", "SystemsManagerQuickSetupClient")
