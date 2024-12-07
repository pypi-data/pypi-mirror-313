"""
Main interface for support service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_support import (
        Client,
        DescribeCasesPaginator,
        DescribeCommunicationsPaginator,
        SupportClient,
    )

    session = get_session()
    async with session.create_client("support") as client:
        client: SupportClient
        ...


    describe_cases_paginator: DescribeCasesPaginator = client.get_paginator("describe_cases")
    describe_communications_paginator: DescribeCommunicationsPaginator = client.get_paginator("describe_communications")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SupportClient
from .paginator import DescribeCasesPaginator, DescribeCommunicationsPaginator

Client = SupportClient

__all__ = ("Client", "DescribeCasesPaginator", "DescribeCommunicationsPaginator", "SupportClient")
