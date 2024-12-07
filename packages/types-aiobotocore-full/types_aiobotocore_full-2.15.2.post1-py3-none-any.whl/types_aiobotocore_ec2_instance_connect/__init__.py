"""
Main interface for ec2-instance-connect service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ec2_instance_connect import (
        Client,
        EC2InstanceConnectClient,
    )

    session = get_session()
    async with session.create_client("ec2-instance-connect") as client:
        client: EC2InstanceConnectClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import EC2InstanceConnectClient

Client = EC2InstanceConnectClient


__all__ = ("Client", "EC2InstanceConnectClient")
