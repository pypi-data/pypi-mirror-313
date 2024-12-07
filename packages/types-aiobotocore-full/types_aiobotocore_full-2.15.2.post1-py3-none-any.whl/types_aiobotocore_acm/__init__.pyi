"""
Main interface for acm service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_acm import (
        ACMClient,
        CertificateValidatedWaiter,
        Client,
        ListCertificatesPaginator,
    )

    session = get_session()
    async with session.create_client("acm") as client:
        client: ACMClient
        ...


    certificate_validated_waiter: CertificateValidatedWaiter = client.get_waiter("certificate_validated")

    list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ACMClient
from .paginator import ListCertificatesPaginator
from .waiter import CertificateValidatedWaiter

Client = ACMClient

__all__ = ("ACMClient", "CertificateValidatedWaiter", "Client", "ListCertificatesPaginator")
