"""
Type annotations for chime-sdk-voice service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_chime_sdk_voice.client import ChimeSDKVoiceClient
    from types_aiobotocore_chime_sdk_voice.paginator import (
        ListSipMediaApplicationsPaginator,
        ListSipRulesPaginator,
    )

    session = get_session()
    with session.create_client("chime-sdk-voice") as client:
        client: ChimeSDKVoiceClient

        list_sip_media_applications_paginator: ListSipMediaApplicationsPaginator = client.get_paginator("list_sip_media_applications")
        list_sip_rules_paginator: ListSipRulesPaginator = client.get_paginator("list_sip_rules")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListSipMediaApplicationsRequestListSipMediaApplicationsPaginateTypeDef,
    ListSipMediaApplicationsResponseTypeDef,
    ListSipRulesRequestListSipRulesPaginateTypeDef,
    ListSipRulesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListSipMediaApplicationsPaginator", "ListSipRulesPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListSipMediaApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice/paginator/ListSipMediaApplications.html#ChimeSDKVoice.Paginator.ListSipMediaApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/paginators/#listsipmediaapplicationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListSipMediaApplicationsRequestListSipMediaApplicationsPaginateTypeDef],
    ) -> AsyncIterator[ListSipMediaApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice/paginator/ListSipMediaApplications.html#ChimeSDKVoice.Paginator.ListSipMediaApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/paginators/#listsipmediaapplicationspaginator)
        """


class ListSipRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice/paginator/ListSipRules.html#ChimeSDKVoice.Paginator.ListSipRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/paginators/#listsiprulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSipRulesRequestListSipRulesPaginateTypeDef]
    ) -> AsyncIterator[ListSipRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice/paginator/ListSipRules.html#ChimeSDKVoice.Paginator.ListSipRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/paginators/#listsiprulespaginator)
        """
