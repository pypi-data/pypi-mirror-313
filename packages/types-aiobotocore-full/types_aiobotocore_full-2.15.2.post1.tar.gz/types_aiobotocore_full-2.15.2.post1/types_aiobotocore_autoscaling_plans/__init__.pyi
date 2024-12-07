"""
Main interface for autoscaling-plans service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_autoscaling_plans import (
        AutoScalingPlansClient,
        Client,
        DescribeScalingPlanResourcesPaginator,
        DescribeScalingPlansPaginator,
    )

    session = get_session()
    async with session.create_client("autoscaling-plans") as client:
        client: AutoScalingPlansClient
        ...


    describe_scaling_plan_resources_paginator: DescribeScalingPlanResourcesPaginator = client.get_paginator("describe_scaling_plan_resources")
    describe_scaling_plans_paginator: DescribeScalingPlansPaginator = client.get_paginator("describe_scaling_plans")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import AutoScalingPlansClient
from .paginator import DescribeScalingPlanResourcesPaginator, DescribeScalingPlansPaginator

Client = AutoScalingPlansClient

__all__ = (
    "AutoScalingPlansClient",
    "Client",
    "DescribeScalingPlanResourcesPaginator",
    "DescribeScalingPlansPaginator",
)
