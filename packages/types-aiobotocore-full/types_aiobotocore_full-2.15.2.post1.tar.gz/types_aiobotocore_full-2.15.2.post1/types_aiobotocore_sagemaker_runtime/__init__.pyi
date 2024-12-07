"""
Main interface for sagemaker-runtime service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker_runtime import (
        Client,
        SageMakerRuntimeClient,
    )

    session = get_session()
    async with session.create_client("sagemaker-runtime") as client:
        client: SageMakerRuntimeClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SageMakerRuntimeClient

Client = SageMakerRuntimeClient

__all__ = ("Client", "SageMakerRuntimeClient")
