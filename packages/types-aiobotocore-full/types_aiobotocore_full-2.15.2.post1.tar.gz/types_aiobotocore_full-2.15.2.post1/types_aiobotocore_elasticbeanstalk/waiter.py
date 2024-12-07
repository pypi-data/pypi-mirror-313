"""
Type annotations for elasticbeanstalk service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elasticbeanstalk.client import ElasticBeanstalkClient
    from types_aiobotocore_elasticbeanstalk.waiter import (
        EnvironmentExistsWaiter,
        EnvironmentTerminatedWaiter,
        EnvironmentUpdatedWaiter,
    )

    session = get_session()
    async with session.create_client("elasticbeanstalk") as client:
        client: ElasticBeanstalkClient

        environment_exists_waiter: EnvironmentExistsWaiter = client.get_waiter("environment_exists")
        environment_terminated_waiter: EnvironmentTerminatedWaiter = client.get_waiter("environment_terminated")
        environment_updated_waiter: EnvironmentUpdatedWaiter = client.get_waiter("environment_updated")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeEnvironmentsMessageEnvironmentExistsWaitTypeDef,
    DescribeEnvironmentsMessageEnvironmentTerminatedWaitTypeDef,
    DescribeEnvironmentsMessageEnvironmentUpdatedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("EnvironmentExistsWaiter", "EnvironmentTerminatedWaiter", "EnvironmentUpdatedWaiter")


class EnvironmentExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/waiter/EnvironmentExists.html#ElasticBeanstalk.Waiter.EnvironmentExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/waiters/#environmentexistswaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeEnvironmentsMessageEnvironmentExistsWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/waiter/EnvironmentExists.html#ElasticBeanstalk.Waiter.EnvironmentExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/waiters/#environmentexistswaiter)
        """


class EnvironmentTerminatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/waiter/EnvironmentTerminated.html#ElasticBeanstalk.Waiter.EnvironmentTerminated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/waiters/#environmentterminatedwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeEnvironmentsMessageEnvironmentTerminatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/waiter/EnvironmentTerminated.html#ElasticBeanstalk.Waiter.EnvironmentTerminated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/waiters/#environmentterminatedwaiter)
        """


class EnvironmentUpdatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/waiter/EnvironmentUpdated.html#ElasticBeanstalk.Waiter.EnvironmentUpdated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/waiters/#environmentupdatedwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeEnvironmentsMessageEnvironmentUpdatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/waiter/EnvironmentUpdated.html#ElasticBeanstalk.Waiter.EnvironmentUpdated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/waiters/#environmentupdatedwaiter)
        """
