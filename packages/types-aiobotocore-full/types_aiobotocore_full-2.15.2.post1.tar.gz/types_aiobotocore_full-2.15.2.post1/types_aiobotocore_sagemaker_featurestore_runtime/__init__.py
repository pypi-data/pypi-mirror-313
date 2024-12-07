"""
Main interface for sagemaker-featurestore-runtime service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker_featurestore_runtime import (
        Client,
        SageMakerFeatureStoreRuntimeClient,
    )

    session = get_session()
    async with session.create_client("sagemaker-featurestore-runtime") as client:
        client: SageMakerFeatureStoreRuntimeClient
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SageMakerFeatureStoreRuntimeClient

Client = SageMakerFeatureStoreRuntimeClient


__all__ = ("Client", "SageMakerFeatureStoreRuntimeClient")
