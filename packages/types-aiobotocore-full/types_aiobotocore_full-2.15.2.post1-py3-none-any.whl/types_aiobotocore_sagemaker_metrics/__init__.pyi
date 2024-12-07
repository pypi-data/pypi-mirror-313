"""
Main interface for sagemaker-metrics service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker_metrics import (
        Client,
        SageMakerMetricsClient,
    )

    session = get_session()
    async with session.create_client("sagemaker-metrics") as client:
        client: SageMakerMetricsClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SageMakerMetricsClient

Client = SageMakerMetricsClient

__all__ = ("Client", "SageMakerMetricsClient")
