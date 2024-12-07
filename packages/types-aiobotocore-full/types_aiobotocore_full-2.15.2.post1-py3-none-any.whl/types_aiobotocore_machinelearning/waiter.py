"""
Type annotations for machinelearning service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_machinelearning/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_machinelearning.client import MachineLearningClient
    from types_aiobotocore_machinelearning.waiter import (
        BatchPredictionAvailableWaiter,
        DataSourceAvailableWaiter,
        EvaluationAvailableWaiter,
        MLModelAvailableWaiter,
    )

    session = get_session()
    async with session.create_client("machinelearning") as client:
        client: MachineLearningClient

        batch_prediction_available_waiter: BatchPredictionAvailableWaiter = client.get_waiter("batch_prediction_available")
        data_source_available_waiter: DataSourceAvailableWaiter = client.get_waiter("data_source_available")
        evaluation_available_waiter: EvaluationAvailableWaiter = client.get_waiter("evaluation_available")
        ml_model_available_waiter: MLModelAvailableWaiter = client.get_waiter("ml_model_available")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeBatchPredictionsInputBatchPredictionAvailableWaitTypeDef,
    DescribeDataSourcesInputDataSourceAvailableWaitTypeDef,
    DescribeEvaluationsInputEvaluationAvailableWaitTypeDef,
    DescribeMLModelsInputMLModelAvailableWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "BatchPredictionAvailableWaiter",
    "DataSourceAvailableWaiter",
    "EvaluationAvailableWaiter",
    "MLModelAvailableWaiter",
)


class BatchPredictionAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/waiter/BatchPredictionAvailable.html#MachineLearning.Waiter.BatchPredictionAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_machinelearning/waiters/#batchpredictionavailablewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeBatchPredictionsInputBatchPredictionAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/waiter/BatchPredictionAvailable.html#MachineLearning.Waiter.BatchPredictionAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_machinelearning/waiters/#batchpredictionavailablewaiter)
        """


class DataSourceAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/waiter/DataSourceAvailable.html#MachineLearning.Waiter.DataSourceAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_machinelearning/waiters/#datasourceavailablewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeDataSourcesInputDataSourceAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/waiter/DataSourceAvailable.html#MachineLearning.Waiter.DataSourceAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_machinelearning/waiters/#datasourceavailablewaiter)
        """


class EvaluationAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/waiter/EvaluationAvailable.html#MachineLearning.Waiter.EvaluationAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_machinelearning/waiters/#evaluationavailablewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeEvaluationsInputEvaluationAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/waiter/EvaluationAvailable.html#MachineLearning.Waiter.EvaluationAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_machinelearning/waiters/#evaluationavailablewaiter)
        """


class MLModelAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/waiter/MLModelAvailable.html#MachineLearning.Waiter.MLModelAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_machinelearning/waiters/#mlmodelavailablewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[DescribeMLModelsInputMLModelAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/waiter/MLModelAvailable.html#MachineLearning.Waiter.MLModelAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_machinelearning/waiters/#mlmodelavailablewaiter)
        """
