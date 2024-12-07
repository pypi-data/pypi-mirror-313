"""
Type annotations for autoscaling service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_autoscaling.client import AutoScalingClient
    from types_aiobotocore_autoscaling.paginator import (
        DescribeAutoScalingGroupsPaginator,
        DescribeAutoScalingInstancesPaginator,
        DescribeLaunchConfigurationsPaginator,
        DescribeLoadBalancerTargetGroupsPaginator,
        DescribeLoadBalancersPaginator,
        DescribeNotificationConfigurationsPaginator,
        DescribePoliciesPaginator,
        DescribeScalingActivitiesPaginator,
        DescribeScheduledActionsPaginator,
        DescribeTagsPaginator,
        DescribeWarmPoolPaginator,
    )

    session = get_session()
    with session.create_client("autoscaling") as client:
        client: AutoScalingClient

        describe_auto_scaling_groups_paginator: DescribeAutoScalingGroupsPaginator = client.get_paginator("describe_auto_scaling_groups")
        describe_auto_scaling_instances_paginator: DescribeAutoScalingInstancesPaginator = client.get_paginator("describe_auto_scaling_instances")
        describe_launch_configurations_paginator: DescribeLaunchConfigurationsPaginator = client.get_paginator("describe_launch_configurations")
        describe_load_balancer_target_groups_paginator: DescribeLoadBalancerTargetGroupsPaginator = client.get_paginator("describe_load_balancer_target_groups")
        describe_load_balancers_paginator: DescribeLoadBalancersPaginator = client.get_paginator("describe_load_balancers")
        describe_notification_configurations_paginator: DescribeNotificationConfigurationsPaginator = client.get_paginator("describe_notification_configurations")
        describe_policies_paginator: DescribePoliciesPaginator = client.get_paginator("describe_policies")
        describe_scaling_activities_paginator: DescribeScalingActivitiesPaginator = client.get_paginator("describe_scaling_activities")
        describe_scheduled_actions_paginator: DescribeScheduledActionsPaginator = client.get_paginator("describe_scheduled_actions")
        describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
        describe_warm_pool_paginator: DescribeWarmPoolPaginator = client.get_paginator("describe_warm_pool")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ActivitiesTypeTypeDef,
    AutoScalingGroupNamesTypeDescribeAutoScalingGroupsPaginateTypeDef,
    AutoScalingGroupsTypeTypeDef,
    AutoScalingInstancesTypeTypeDef,
    DescribeAutoScalingInstancesTypeDescribeAutoScalingInstancesPaginateTypeDef,
    DescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef,
    DescribeLoadBalancersResponseTypeDef,
    DescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef,
    DescribeLoadBalancerTargetGroupsResponseTypeDef,
    DescribeNotificationConfigurationsAnswerTypeDef,
    DescribeNotificationConfigurationsTypeDescribeNotificationConfigurationsPaginateTypeDef,
    DescribePoliciesTypeDescribePoliciesPaginateTypeDef,
    DescribeScalingActivitiesTypeDescribeScalingActivitiesPaginateTypeDef,
    DescribeScheduledActionsTypeDescribeScheduledActionsPaginateTypeDef,
    DescribeTagsTypeDescribeTagsPaginateTypeDef,
    DescribeWarmPoolAnswerTypeDef,
    DescribeWarmPoolTypeDescribeWarmPoolPaginateTypeDef,
    LaunchConfigurationNamesTypeDescribeLaunchConfigurationsPaginateTypeDef,
    LaunchConfigurationsTypeTypeDef,
    PoliciesTypeTypeDef,
    ScheduledActionsTypeTypeDef,
    TagsTypeTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAutoScalingGroupsPaginator",
    "DescribeAutoScalingInstancesPaginator",
    "DescribeLaunchConfigurationsPaginator",
    "DescribeLoadBalancerTargetGroupsPaginator",
    "DescribeLoadBalancersPaginator",
    "DescribeNotificationConfigurationsPaginator",
    "DescribePoliciesPaginator",
    "DescribeScalingActivitiesPaginator",
    "DescribeScheduledActionsPaginator",
    "DescribeTagsPaginator",
    "DescribeWarmPoolPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAutoScalingGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeAutoScalingGroups.html#AutoScaling.Paginator.DescribeAutoScalingGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeautoscalinggroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[AutoScalingGroupNamesTypeDescribeAutoScalingGroupsPaginateTypeDef]
    ) -> AsyncIterator[AutoScalingGroupsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeAutoScalingGroups.html#AutoScaling.Paginator.DescribeAutoScalingGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeautoscalinggroupspaginator)
        """


class DescribeAutoScalingInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeAutoScalingInstances.html#AutoScaling.Paginator.DescribeAutoScalingInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeautoscalinginstancespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAutoScalingInstancesTypeDescribeAutoScalingInstancesPaginateTypeDef
        ],
    ) -> AsyncIterator[AutoScalingInstancesTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeAutoScalingInstances.html#AutoScaling.Paginator.DescribeAutoScalingInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeautoscalinginstancespaginator)
        """


class DescribeLaunchConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLaunchConfigurations.html#AutoScaling.Paginator.DescribeLaunchConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describelaunchconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[LaunchConfigurationNamesTypeDescribeLaunchConfigurationsPaginateTypeDef],
    ) -> AsyncIterator[LaunchConfigurationsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLaunchConfigurations.html#AutoScaling.Paginator.DescribeLaunchConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describelaunchconfigurationspaginator)
        """


class DescribeLoadBalancerTargetGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLoadBalancerTargetGroups.html#AutoScaling.Paginator.DescribeLoadBalancerTargetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeloadbalancertargetgroupspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeLoadBalancerTargetGroupsRequestDescribeLoadBalancerTargetGroupsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeLoadBalancerTargetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLoadBalancerTargetGroups.html#AutoScaling.Paginator.DescribeLoadBalancerTargetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeloadbalancertargetgroupspaginator)
        """


class DescribeLoadBalancersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLoadBalancers.html#AutoScaling.Paginator.DescribeLoadBalancers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeloadbalancerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeLoadBalancersRequestDescribeLoadBalancersPaginateTypeDef]
    ) -> AsyncIterator[DescribeLoadBalancersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeLoadBalancers.html#AutoScaling.Paginator.DescribeLoadBalancers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describeloadbalancerspaginator)
        """


class DescribeNotificationConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeNotificationConfigurations.html#AutoScaling.Paginator.DescribeNotificationConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describenotificationconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeNotificationConfigurationsTypeDescribeNotificationConfigurationsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeNotificationConfigurationsAnswerTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeNotificationConfigurations.html#AutoScaling.Paginator.DescribeNotificationConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describenotificationconfigurationspaginator)
        """


class DescribePoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribePolicies.html#AutoScaling.Paginator.DescribePolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describepoliciespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribePoliciesTypeDescribePoliciesPaginateTypeDef]
    ) -> AsyncIterator[PoliciesTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribePolicies.html#AutoScaling.Paginator.DescribePolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describepoliciespaginator)
        """


class DescribeScalingActivitiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeScalingActivities.html#AutoScaling.Paginator.DescribeScalingActivities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describescalingactivitiespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeScalingActivitiesTypeDescribeScalingActivitiesPaginateTypeDef],
    ) -> AsyncIterator[ActivitiesTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeScalingActivities.html#AutoScaling.Paginator.DescribeScalingActivities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describescalingactivitiespaginator)
        """


class DescribeScheduledActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeScheduledActions.html#AutoScaling.Paginator.DescribeScheduledActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describescheduledactionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeScheduledActionsTypeDescribeScheduledActionsPaginateTypeDef]
    ) -> AsyncIterator[ScheduledActionsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeScheduledActions.html#AutoScaling.Paginator.DescribeScheduledActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describescheduledactionspaginator)
        """


class DescribeTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeTags.html#AutoScaling.Paginator.DescribeTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describetagspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeTagsTypeDescribeTagsPaginateTypeDef]
    ) -> AsyncIterator[TagsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeTags.html#AutoScaling.Paginator.DescribeTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describetagspaginator)
        """


class DescribeWarmPoolPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeWarmPool.html#AutoScaling.Paginator.DescribeWarmPool)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describewarmpoolpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeWarmPoolTypeDescribeWarmPoolPaginateTypeDef]
    ) -> AsyncIterator[DescribeWarmPoolAnswerTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/paginator/DescribeWarmPool.html#AutoScaling.Paginator.DescribeWarmPool.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/paginators/#describewarmpoolpaginator)
        """
