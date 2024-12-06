"""
Type annotations for elastictranscoder service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_elastictranscoder.client import ElasticTranscoderClient

    session = Session()
    client: ElasticTranscoderClient = session.client("elastictranscoder")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListJobsByPipelinePaginator,
    ListJobsByStatusPaginator,
    ListPipelinesPaginator,
    ListPresetsPaginator,
)
from .type_defs import (
    CancelJobRequestRequestTypeDef,
    CreateJobRequestRequestTypeDef,
    CreateJobResponseTypeDef,
    CreatePipelineRequestRequestTypeDef,
    CreatePipelineResponseTypeDef,
    CreatePresetRequestRequestTypeDef,
    CreatePresetResponseTypeDef,
    DeletePipelineRequestRequestTypeDef,
    DeletePresetRequestRequestTypeDef,
    ListJobsByPipelineRequestRequestTypeDef,
    ListJobsByPipelineResponseTypeDef,
    ListJobsByStatusRequestRequestTypeDef,
    ListJobsByStatusResponseTypeDef,
    ListPipelinesRequestRequestTypeDef,
    ListPipelinesResponseTypeDef,
    ListPresetsRequestRequestTypeDef,
    ListPresetsResponseTypeDef,
    ReadJobRequestRequestTypeDef,
    ReadJobResponseTypeDef,
    ReadPipelineRequestRequestTypeDef,
    ReadPipelineResponseTypeDef,
    ReadPresetRequestRequestTypeDef,
    ReadPresetResponseTypeDef,
    TestRoleRequestRequestTypeDef,
    TestRoleResponseTypeDef,
    UpdatePipelineNotificationsRequestRequestTypeDef,
    UpdatePipelineNotificationsResponseTypeDef,
    UpdatePipelineRequestRequestTypeDef,
    UpdatePipelineResponseTypeDef,
    UpdatePipelineStatusRequestRequestTypeDef,
    UpdatePipelineStatusResponseTypeDef,
)
from .waiter import JobCompleteWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ElasticTranscoderClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    IncompatibleVersionException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ElasticTranscoderClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticTranscoderClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#close)
        """

    def cancel_job(self, **kwargs: Unpack[CancelJobRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        The CancelJob operation cancels an unfinished job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/cancel_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#cancel_job)
        """

    def create_job(
        self, **kwargs: Unpack[CreateJobRequestRequestTypeDef]
    ) -> CreateJobResponseTypeDef:
        """
        When you create a job, Elastic Transcoder returns JSON data that includes the
        values that you specified plus information about the job that is created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/create_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#create_job)
        """

    def create_pipeline(
        self, **kwargs: Unpack[CreatePipelineRequestRequestTypeDef]
    ) -> CreatePipelineResponseTypeDef:
        """
        The CreatePipeline operation creates a pipeline with settings that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/create_pipeline.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#create_pipeline)
        """

    def create_preset(
        self, **kwargs: Unpack[CreatePresetRequestRequestTypeDef]
    ) -> CreatePresetResponseTypeDef:
        """
        The CreatePreset operation creates a preset with settings that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/create_preset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#create_preset)
        """

    def delete_pipeline(
        self, **kwargs: Unpack[DeletePipelineRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The DeletePipeline operation removes a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/delete_pipeline.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#delete_pipeline)
        """

    def delete_preset(self, **kwargs: Unpack[DeletePresetRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        The DeletePreset operation removes a preset that you've added in an AWS region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/delete_preset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#delete_preset)
        """

    def list_jobs_by_pipeline(
        self, **kwargs: Unpack[ListJobsByPipelineRequestRequestTypeDef]
    ) -> ListJobsByPipelineResponseTypeDef:
        """
        The ListJobsByPipeline operation gets a list of the jobs currently in a
        pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/list_jobs_by_pipeline.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#list_jobs_by_pipeline)
        """

    def list_jobs_by_status(
        self, **kwargs: Unpack[ListJobsByStatusRequestRequestTypeDef]
    ) -> ListJobsByStatusResponseTypeDef:
        """
        The ListJobsByStatus operation gets a list of jobs that have a specified status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/list_jobs_by_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#list_jobs_by_status)
        """

    def list_pipelines(
        self, **kwargs: Unpack[ListPipelinesRequestRequestTypeDef]
    ) -> ListPipelinesResponseTypeDef:
        """
        The ListPipelines operation gets a list of the pipelines associated with the
        current AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/list_pipelines.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#list_pipelines)
        """

    def list_presets(
        self, **kwargs: Unpack[ListPresetsRequestRequestTypeDef]
    ) -> ListPresetsResponseTypeDef:
        """
        The ListPresets operation gets a list of the default presets included with
        Elastic Transcoder and the presets that you've added in an AWS region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/list_presets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#list_presets)
        """

    def read_job(self, **kwargs: Unpack[ReadJobRequestRequestTypeDef]) -> ReadJobResponseTypeDef:
        """
        The ReadJob operation returns detailed information about a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/read_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#read_job)
        """

    def read_pipeline(
        self, **kwargs: Unpack[ReadPipelineRequestRequestTypeDef]
    ) -> ReadPipelineResponseTypeDef:
        """
        The ReadPipeline operation gets detailed information about a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/read_pipeline.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#read_pipeline)
        """

    def read_preset(
        self, **kwargs: Unpack[ReadPresetRequestRequestTypeDef]
    ) -> ReadPresetResponseTypeDef:
        """
        The ReadPreset operation gets detailed information about a preset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/read_preset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#read_preset)
        """

    def test_role(self, **kwargs: Unpack[TestRoleRequestRequestTypeDef]) -> TestRoleResponseTypeDef:
        """
        The TestRole operation tests the IAM role used to create the pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/test_role.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#test_role)
        """

    def update_pipeline(
        self, **kwargs: Unpack[UpdatePipelineRequestRequestTypeDef]
    ) -> UpdatePipelineResponseTypeDef:
        """
        Use the <code>UpdatePipeline</code> operation to update settings for a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/update_pipeline.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#update_pipeline)
        """

    def update_pipeline_notifications(
        self, **kwargs: Unpack[UpdatePipelineNotificationsRequestRequestTypeDef]
    ) -> UpdatePipelineNotificationsResponseTypeDef:
        """
        With the UpdatePipelineNotifications operation, you can update Amazon Simple
        Notification Service (Amazon SNS) notifications for a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/update_pipeline_notifications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#update_pipeline_notifications)
        """

    def update_pipeline_status(
        self, **kwargs: Unpack[UpdatePipelineStatusRequestRequestTypeDef]
    ) -> UpdatePipelineStatusResponseTypeDef:
        """
        The UpdatePipelineStatus operation pauses or reactivates a pipeline, so that
        the pipeline stops or restarts the processing of jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/update_pipeline_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#update_pipeline_status)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_jobs_by_pipeline"]
    ) -> ListJobsByPipelinePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_jobs_by_status"]
    ) -> ListJobsByStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_pipelines"]) -> ListPipelinesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_presets"]) -> ListPresetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#get_paginator)
        """

    def get_waiter(self, waiter_name: Literal["job_complete"]) -> JobCompleteWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#get_waiter)
        """
