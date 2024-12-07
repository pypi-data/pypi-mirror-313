"""
Type annotations for mediatailor service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediatailor.client import MediaTailorClient
    from types_aiobotocore_mediatailor.paginator import (
        GetChannelSchedulePaginator,
        ListAlertsPaginator,
        ListChannelsPaginator,
        ListLiveSourcesPaginator,
        ListPlaybackConfigurationsPaginator,
        ListPrefetchSchedulesPaginator,
        ListSourceLocationsPaginator,
        ListVodSourcesPaginator,
    )

    session = get_session()
    with session.create_client("mediatailor") as client:
        client: MediaTailorClient

        get_channel_schedule_paginator: GetChannelSchedulePaginator = client.get_paginator("get_channel_schedule")
        list_alerts_paginator: ListAlertsPaginator = client.get_paginator("list_alerts")
        list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
        list_live_sources_paginator: ListLiveSourcesPaginator = client.get_paginator("list_live_sources")
        list_playback_configurations_paginator: ListPlaybackConfigurationsPaginator = client.get_paginator("list_playback_configurations")
        list_prefetch_schedules_paginator: ListPrefetchSchedulesPaginator = client.get_paginator("list_prefetch_schedules")
        list_source_locations_paginator: ListSourceLocationsPaginator = client.get_paginator("list_source_locations")
        list_vod_sources_paginator: ListVodSourcesPaginator = client.get_paginator("list_vod_sources")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetChannelScheduleRequestGetChannelSchedulePaginateTypeDef,
    GetChannelScheduleResponseTypeDef,
    ListAlertsRequestListAlertsPaginateTypeDef,
    ListAlertsResponseTypeDef,
    ListChannelsRequestListChannelsPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListLiveSourcesRequestListLiveSourcesPaginateTypeDef,
    ListLiveSourcesResponseTypeDef,
    ListPlaybackConfigurationsRequestListPlaybackConfigurationsPaginateTypeDef,
    ListPlaybackConfigurationsResponseTypeDef,
    ListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef,
    ListPrefetchSchedulesResponseTypeDef,
    ListSourceLocationsRequestListSourceLocationsPaginateTypeDef,
    ListSourceLocationsResponseTypeDef,
    ListVodSourcesRequestListVodSourcesPaginateTypeDef,
    ListVodSourcesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetChannelSchedulePaginator",
    "ListAlertsPaginator",
    "ListChannelsPaginator",
    "ListLiveSourcesPaginator",
    "ListPlaybackConfigurationsPaginator",
    "ListPrefetchSchedulesPaginator",
    "ListSourceLocationsPaginator",
    "ListVodSourcesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetChannelSchedulePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/GetChannelSchedule.html#MediaTailor.Paginator.GetChannelSchedule)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#getchannelschedulepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetChannelScheduleRequestGetChannelSchedulePaginateTypeDef]
    ) -> AsyncIterator[GetChannelScheduleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/GetChannelSchedule.html#MediaTailor.Paginator.GetChannelSchedule.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#getchannelschedulepaginator)
        """

class ListAlertsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListAlerts.html#MediaTailor.Paginator.ListAlerts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listalertspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAlertsRequestListAlertsPaginateTypeDef]
    ) -> AsyncIterator[ListAlertsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListAlerts.html#MediaTailor.Paginator.ListAlerts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listalertspaginator)
        """

class ListChannelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListChannels.html#MediaTailor.Paginator.ListChannels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listchannelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListChannelsRequestListChannelsPaginateTypeDef]
    ) -> AsyncIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListChannels.html#MediaTailor.Paginator.ListChannels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listchannelspaginator)
        """

class ListLiveSourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListLiveSources.html#MediaTailor.Paginator.ListLiveSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listlivesourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLiveSourcesRequestListLiveSourcesPaginateTypeDef]
    ) -> AsyncIterator[ListLiveSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListLiveSources.html#MediaTailor.Paginator.ListLiveSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listlivesourcespaginator)
        """

class ListPlaybackConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListPlaybackConfigurations.html#MediaTailor.Paginator.ListPlaybackConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listplaybackconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListPlaybackConfigurationsRequestListPlaybackConfigurationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListPlaybackConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListPlaybackConfigurations.html#MediaTailor.Paginator.ListPlaybackConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listplaybackconfigurationspaginator)
        """

class ListPrefetchSchedulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListPrefetchSchedules.html#MediaTailor.Paginator.ListPrefetchSchedules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listprefetchschedulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPrefetchSchedulesRequestListPrefetchSchedulesPaginateTypeDef]
    ) -> AsyncIterator[ListPrefetchSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListPrefetchSchedules.html#MediaTailor.Paginator.ListPrefetchSchedules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listprefetchschedulespaginator)
        """

class ListSourceLocationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListSourceLocations.html#MediaTailor.Paginator.ListSourceLocations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listsourcelocationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSourceLocationsRequestListSourceLocationsPaginateTypeDef]
    ) -> AsyncIterator[ListSourceLocationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListSourceLocations.html#MediaTailor.Paginator.ListSourceLocations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listsourcelocationspaginator)
        """

class ListVodSourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListVodSources.html#MediaTailor.Paginator.ListVodSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listvodsourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListVodSourcesRequestListVodSourcesPaginateTypeDef]
    ) -> AsyncIterator[ListVodSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListVodSources.html#MediaTailor.Paginator.ListVodSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listvodsourcespaginator)
        """
