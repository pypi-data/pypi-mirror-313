"""
Type annotations for datapipeline service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_datapipeline.client import DataPipelineClient

    session = get_session()
    async with session.create_client("datapipeline") as client:
        client: DataPipelineClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import DescribeObjectsPaginator, ListPipelinesPaginator, QueryObjectsPaginator
from .type_defs import (
    ActivatePipelineInputRequestTypeDef,
    AddTagsInputRequestTypeDef,
    CreatePipelineInputRequestTypeDef,
    CreatePipelineOutputTypeDef,
    DeactivatePipelineInputRequestTypeDef,
    DeletePipelineInputRequestTypeDef,
    DescribeObjectsInputRequestTypeDef,
    DescribeObjectsOutputTypeDef,
    DescribePipelinesInputRequestTypeDef,
    DescribePipelinesOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    EvaluateExpressionInputRequestTypeDef,
    EvaluateExpressionOutputTypeDef,
    GetPipelineDefinitionInputRequestTypeDef,
    GetPipelineDefinitionOutputTypeDef,
    ListPipelinesInputRequestTypeDef,
    ListPipelinesOutputTypeDef,
    PollForTaskInputRequestTypeDef,
    PollForTaskOutputTypeDef,
    PutPipelineDefinitionInputRequestTypeDef,
    PutPipelineDefinitionOutputTypeDef,
    QueryObjectsInputRequestTypeDef,
    QueryObjectsOutputTypeDef,
    RemoveTagsInputRequestTypeDef,
    ReportTaskProgressInputRequestTypeDef,
    ReportTaskProgressOutputTypeDef,
    ReportTaskRunnerHeartbeatInputRequestTypeDef,
    ReportTaskRunnerHeartbeatOutputTypeDef,
    SetStatusInputRequestTypeDef,
    SetTaskStatusInputRequestTypeDef,
    ValidatePipelineDefinitionInputRequestTypeDef,
    ValidatePipelineDefinitionOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("DataPipelineClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    PipelineDeletedException: Type[BotocoreClientError]
    PipelineNotFoundException: Type[BotocoreClientError]
    TaskNotFoundException: Type[BotocoreClientError]


class DataPipelineClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DataPipelineClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#close)
        """

    async def activate_pipeline(
        self, **kwargs: Unpack[ActivatePipelineInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Validates the specified pipeline and starts processing pipeline tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/activate_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#activate_pipeline)
        """

    async def add_tags(self, **kwargs: Unpack[AddTagsInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds or modifies tags for the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/add_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#add_tags)
        """

    async def create_pipeline(
        self, **kwargs: Unpack[CreatePipelineInputRequestTypeDef]
    ) -> CreatePipelineOutputTypeDef:
        """
        Creates a new, empty pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/create_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#create_pipeline)
        """

    async def deactivate_pipeline(
        self, **kwargs: Unpack[DeactivatePipelineInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deactivates the specified running pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/deactivate_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#deactivate_pipeline)
        """

    async def delete_pipeline(
        self, **kwargs: Unpack[DeletePipelineInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a pipeline, its pipeline definition, and its run history.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/delete_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#delete_pipeline)
        """

    async def describe_objects(
        self, **kwargs: Unpack[DescribeObjectsInputRequestTypeDef]
    ) -> DescribeObjectsOutputTypeDef:
        """
        Gets the object definitions for a set of objects associated with the pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/describe_objects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#describe_objects)
        """

    async def describe_pipelines(
        self, **kwargs: Unpack[DescribePipelinesInputRequestTypeDef]
    ) -> DescribePipelinesOutputTypeDef:
        """
        Retrieves metadata about one or more pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/describe_pipelines.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#describe_pipelines)
        """

    async def evaluate_expression(
        self, **kwargs: Unpack[EvaluateExpressionInputRequestTypeDef]
    ) -> EvaluateExpressionOutputTypeDef:
        """
        Task runners call <code>EvaluateExpression</code> to evaluate a string in the
        context of the specified object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/evaluate_expression.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#evaluate_expression)
        """

    async def get_pipeline_definition(
        self, **kwargs: Unpack[GetPipelineDefinitionInputRequestTypeDef]
    ) -> GetPipelineDefinitionOutputTypeDef:
        """
        Gets the definition of the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/get_pipeline_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#get_pipeline_definition)
        """

    async def list_pipelines(
        self, **kwargs: Unpack[ListPipelinesInputRequestTypeDef]
    ) -> ListPipelinesOutputTypeDef:
        """
        Lists the pipeline identifiers for all active pipelines that you have
        permission to access.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/list_pipelines.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#list_pipelines)
        """

    async def poll_for_task(
        self, **kwargs: Unpack[PollForTaskInputRequestTypeDef]
    ) -> PollForTaskOutputTypeDef:
        """
        Task runners call <code>PollForTask</code> to receive a task to perform from
        AWS Data Pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/poll_for_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#poll_for_task)
        """

    async def put_pipeline_definition(
        self, **kwargs: Unpack[PutPipelineDefinitionInputRequestTypeDef]
    ) -> PutPipelineDefinitionOutputTypeDef:
        """
        Adds tasks, schedules, and preconditions to the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/put_pipeline_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#put_pipeline_definition)
        """

    async def query_objects(
        self, **kwargs: Unpack[QueryObjectsInputRequestTypeDef]
    ) -> QueryObjectsOutputTypeDef:
        """
        Queries the specified pipeline for the names of objects that match the
        specified set of conditions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/query_objects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#query_objects)
        """

    async def remove_tags(self, **kwargs: Unpack[RemoveTagsInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes existing tags from the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/remove_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#remove_tags)
        """

    async def report_task_progress(
        self, **kwargs: Unpack[ReportTaskProgressInputRequestTypeDef]
    ) -> ReportTaskProgressOutputTypeDef:
        """
        Task runners call <code>ReportTaskProgress</code> when assigned a task to
        acknowledge that it has the task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/report_task_progress.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#report_task_progress)
        """

    async def report_task_runner_heartbeat(
        self, **kwargs: Unpack[ReportTaskRunnerHeartbeatInputRequestTypeDef]
    ) -> ReportTaskRunnerHeartbeatOutputTypeDef:
        """
        Task runners call <code>ReportTaskRunnerHeartbeat</code> every 15 minutes to
        indicate that they are operational.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/report_task_runner_heartbeat.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#report_task_runner_heartbeat)
        """

    async def set_status(
        self, **kwargs: Unpack[SetStatusInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Requests that the status of the specified physical or logical pipeline objects
        be updated in the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/set_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#set_status)
        """

    async def set_task_status(
        self, **kwargs: Unpack[SetTaskStatusInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Task runners call <code>SetTaskStatus</code> to notify AWS Data Pipeline that a
        task is completed and provide information about the final status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/set_task_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#set_task_status)
        """

    async def validate_pipeline_definition(
        self, **kwargs: Unpack[ValidatePipelineDefinitionInputRequestTypeDef]
    ) -> ValidatePipelineDefinitionOutputTypeDef:
        """
        Validates the specified pipeline definition to ensure that it is well formed
        and can be run without error.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/validate_pipeline_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#validate_pipeline_definition)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_objects"]
    ) -> DescribeObjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_pipelines"]) -> ListPipelinesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["query_objects"]) -> QueryObjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/#get_paginator)
        """

    async def __aenter__(self) -> "DataPipelineClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/client/)
        """
