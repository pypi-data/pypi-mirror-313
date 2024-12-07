"""
Main interface for ses service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ses import (
        Client,
        IdentityExistsWaiter,
        ListConfigurationSetsPaginator,
        ListCustomVerificationEmailTemplatesPaginator,
        ListIdentitiesPaginator,
        ListReceiptRuleSetsPaginator,
        ListTemplatesPaginator,
        SESClient,
    )

    session = get_session()
    async with session.create_client("ses") as client:
        client: SESClient
        ...


    identity_exists_waiter: IdentityExistsWaiter = client.get_waiter("identity_exists")

    list_configuration_sets_paginator: ListConfigurationSetsPaginator = client.get_paginator("list_configuration_sets")
    list_custom_verification_email_templates_paginator: ListCustomVerificationEmailTemplatesPaginator = client.get_paginator("list_custom_verification_email_templates")
    list_identities_paginator: ListIdentitiesPaginator = client.get_paginator("list_identities")
    list_receipt_rule_sets_paginator: ListReceiptRuleSetsPaginator = client.get_paginator("list_receipt_rule_sets")
    list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SESClient
from .paginator import (
    ListConfigurationSetsPaginator,
    ListCustomVerificationEmailTemplatesPaginator,
    ListIdentitiesPaginator,
    ListReceiptRuleSetsPaginator,
    ListTemplatesPaginator,
)
from .waiter import IdentityExistsWaiter

Client = SESClient

__all__ = (
    "Client",
    "IdentityExistsWaiter",
    "ListConfigurationSetsPaginator",
    "ListCustomVerificationEmailTemplatesPaginator",
    "ListIdentitiesPaginator",
    "ListReceiptRuleSetsPaginator",
    "ListTemplatesPaginator",
    "SESClient",
)
