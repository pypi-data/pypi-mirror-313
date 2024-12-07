"""
Type annotations for autoscaling-plans service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_autoscaling_plans.client import AutoScalingPlansClient
    from types_aiobotocore_autoscaling_plans.paginator import (
        DescribeScalingPlanResourcesPaginator,
        DescribeScalingPlansPaginator,
    )

    session = get_session()
    with session.create_client("autoscaling-plans") as client:
        client: AutoScalingPlansClient

        describe_scaling_plan_resources_paginator: DescribeScalingPlanResourcesPaginator = client.get_paginator("describe_scaling_plan_resources")
        describe_scaling_plans_paginator: DescribeScalingPlansPaginator = client.get_paginator("describe_scaling_plans")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef,
    DescribeScalingPlanResourcesResponseTypeDef,
    DescribeScalingPlansRequestDescribeScalingPlansPaginateTypeDef,
    DescribeScalingPlansResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DescribeScalingPlanResourcesPaginator", "DescribeScalingPlansPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeScalingPlanResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlanResources.html#AutoScalingPlans.Paginator.DescribeScalingPlanResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/#describescalingplanresourcespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeScalingPlanResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlanResources.html#AutoScalingPlans.Paginator.DescribeScalingPlanResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/#describescalingplanresourcespaginator)
        """

class DescribeScalingPlansPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlans.html#AutoScalingPlans.Paginator.DescribeScalingPlans)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/#describescalingplanspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeScalingPlansRequestDescribeScalingPlansPaginateTypeDef]
    ) -> AsyncIterator[DescribeScalingPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans/paginator/DescribeScalingPlans.html#AutoScalingPlans.Paginator.DescribeScalingPlans.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/#describescalingplanspaginator)
        """
