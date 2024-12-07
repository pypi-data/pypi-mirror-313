"""
Type annotations for voice-id service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_voice_id.client import VoiceIDClient
    from types_aiobotocore_voice_id.paginator import (
        ListDomainsPaginator,
        ListFraudsterRegistrationJobsPaginator,
        ListFraudstersPaginator,
        ListSpeakerEnrollmentJobsPaginator,
        ListSpeakersPaginator,
        ListWatchlistsPaginator,
    )

    session = get_session()
    with session.create_client("voice-id") as client:
        client: VoiceIDClient

        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_fraudster_registration_jobs_paginator: ListFraudsterRegistrationJobsPaginator = client.get_paginator("list_fraudster_registration_jobs")
        list_fraudsters_paginator: ListFraudstersPaginator = client.get_paginator("list_fraudsters")
        list_speaker_enrollment_jobs_paginator: ListSpeakerEnrollmentJobsPaginator = client.get_paginator("list_speaker_enrollment_jobs")
        list_speakers_paginator: ListSpeakersPaginator = client.get_paginator("list_speakers")
        list_watchlists_paginator: ListWatchlistsPaginator = client.get_paginator("list_watchlists")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDomainsRequestListDomainsPaginateTypeDef,
    ListDomainsResponseTypeDef,
    ListFraudsterRegistrationJobsRequestListFraudsterRegistrationJobsPaginateTypeDef,
    ListFraudsterRegistrationJobsResponseTypeDef,
    ListFraudstersRequestListFraudstersPaginateTypeDef,
    ListFraudstersResponseTypeDef,
    ListSpeakerEnrollmentJobsRequestListSpeakerEnrollmentJobsPaginateTypeDef,
    ListSpeakerEnrollmentJobsResponseTypeDef,
    ListSpeakersRequestListSpeakersPaginateTypeDef,
    ListSpeakersResponseTypeDef,
    ListWatchlistsRequestListWatchlistsPaginateTypeDef,
    ListWatchlistsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDomainsPaginator",
    "ListFraudsterRegistrationJobsPaginator",
    "ListFraudstersPaginator",
    "ListSpeakerEnrollmentJobsPaginator",
    "ListSpeakersPaginator",
    "ListWatchlistsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListDomains.html#VoiceID.Paginator.ListDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listdomainspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDomainsRequestListDomainsPaginateTypeDef]
    ) -> AsyncIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListDomains.html#VoiceID.Paginator.ListDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listdomainspaginator)
        """

class ListFraudsterRegistrationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListFraudsterRegistrationJobs.html#VoiceID.Paginator.ListFraudsterRegistrationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listfraudsterregistrationjobspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListFraudsterRegistrationJobsRequestListFraudsterRegistrationJobsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListFraudsterRegistrationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListFraudsterRegistrationJobs.html#VoiceID.Paginator.ListFraudsterRegistrationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listfraudsterregistrationjobspaginator)
        """

class ListFraudstersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListFraudsters.html#VoiceID.Paginator.ListFraudsters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listfraudsterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFraudstersRequestListFraudstersPaginateTypeDef]
    ) -> AsyncIterator[ListFraudstersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListFraudsters.html#VoiceID.Paginator.ListFraudsters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listfraudsterspaginator)
        """

class ListSpeakerEnrollmentJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListSpeakerEnrollmentJobs.html#VoiceID.Paginator.ListSpeakerEnrollmentJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listspeakerenrollmentjobspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListSpeakerEnrollmentJobsRequestListSpeakerEnrollmentJobsPaginateTypeDef],
    ) -> AsyncIterator[ListSpeakerEnrollmentJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListSpeakerEnrollmentJobs.html#VoiceID.Paginator.ListSpeakerEnrollmentJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listspeakerenrollmentjobspaginator)
        """

class ListSpeakersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListSpeakers.html#VoiceID.Paginator.ListSpeakers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listspeakerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSpeakersRequestListSpeakersPaginateTypeDef]
    ) -> AsyncIterator[ListSpeakersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListSpeakers.html#VoiceID.Paginator.ListSpeakers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listspeakerspaginator)
        """

class ListWatchlistsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListWatchlists.html#VoiceID.Paginator.ListWatchlists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listwatchlistspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWatchlistsRequestListWatchlistsPaginateTypeDef]
    ) -> AsyncIterator[ListWatchlistsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListWatchlists.html#VoiceID.Paginator.ListWatchlists.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listwatchlistspaginator)
        """
