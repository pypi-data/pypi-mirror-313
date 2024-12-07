"""
Main interface for opsworks service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_opsworks import (
        AppExistsWaiter,
        Client,
        DeploymentSuccessfulWaiter,
        DescribeEcsClustersPaginator,
        InstanceOnlineWaiter,
        InstanceRegisteredWaiter,
        InstanceStoppedWaiter,
        InstanceTerminatedWaiter,
        OpsWorksClient,
    )

    session = get_session()
    async with session.create_client("opsworks") as client:
        client: OpsWorksClient
        ...


    app_exists_waiter: AppExistsWaiter = client.get_waiter("app_exists")
    deployment_successful_waiter: DeploymentSuccessfulWaiter = client.get_waiter("deployment_successful")
    instance_online_waiter: InstanceOnlineWaiter = client.get_waiter("instance_online")
    instance_registered_waiter: InstanceRegisteredWaiter = client.get_waiter("instance_registered")
    instance_stopped_waiter: InstanceStoppedWaiter = client.get_waiter("instance_stopped")
    instance_terminated_waiter: InstanceTerminatedWaiter = client.get_waiter("instance_terminated")

    describe_ecs_clusters_paginator: DescribeEcsClustersPaginator = client.get_paginator("describe_ecs_clusters")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import OpsWorksClient
from .paginator import DescribeEcsClustersPaginator
from .waiter import (
    AppExistsWaiter,
    DeploymentSuccessfulWaiter,
    InstanceOnlineWaiter,
    InstanceRegisteredWaiter,
    InstanceStoppedWaiter,
    InstanceTerminatedWaiter,
)

Client = OpsWorksClient

__all__ = (
    "AppExistsWaiter",
    "Client",
    "DeploymentSuccessfulWaiter",
    "DescribeEcsClustersPaginator",
    "InstanceOnlineWaiter",
    "InstanceRegisteredWaiter",
    "InstanceStoppedWaiter",
    "InstanceTerminatedWaiter",
    "OpsWorksClient",
)
