"""
Main interface for sagemaker-edge service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker_edge import (
        Client,
        SagemakerEdgeManagerClient,
    )

    session = get_session()
    async with session.create_client("sagemaker-edge") as client:
        client: SagemakerEdgeManagerClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SagemakerEdgeManagerClient

Client = SagemakerEdgeManagerClient


__all__ = ("Client", "SagemakerEdgeManagerClient")
