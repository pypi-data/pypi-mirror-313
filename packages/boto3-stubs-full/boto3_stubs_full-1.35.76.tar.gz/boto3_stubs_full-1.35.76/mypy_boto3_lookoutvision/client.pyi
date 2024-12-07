"""
Type annotations for lookoutvision service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_lookoutvision.client import LookoutforVisionClient

    session = Session()
    client: LookoutforVisionClient = session.client("lookoutvision")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListDatasetEntriesPaginator,
    ListModelPackagingJobsPaginator,
    ListModelsPaginator,
    ListProjectsPaginator,
)
from .type_defs import (
    CreateDatasetRequestRequestTypeDef,
    CreateDatasetResponseTypeDef,
    CreateModelRequestRequestTypeDef,
    CreateModelResponseTypeDef,
    CreateProjectRequestRequestTypeDef,
    CreateProjectResponseTypeDef,
    DeleteDatasetRequestRequestTypeDef,
    DeleteModelRequestRequestTypeDef,
    DeleteModelResponseTypeDef,
    DeleteProjectRequestRequestTypeDef,
    DeleteProjectResponseTypeDef,
    DescribeDatasetRequestRequestTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeModelPackagingJobRequestRequestTypeDef,
    DescribeModelPackagingJobResponseTypeDef,
    DescribeModelRequestRequestTypeDef,
    DescribeModelResponseTypeDef,
    DescribeProjectRequestRequestTypeDef,
    DescribeProjectResponseTypeDef,
    DetectAnomaliesRequestRequestTypeDef,
    DetectAnomaliesResponseTypeDef,
    ListDatasetEntriesRequestRequestTypeDef,
    ListDatasetEntriesResponseTypeDef,
    ListModelPackagingJobsRequestRequestTypeDef,
    ListModelPackagingJobsResponseTypeDef,
    ListModelsRequestRequestTypeDef,
    ListModelsResponseTypeDef,
    ListProjectsRequestRequestTypeDef,
    ListProjectsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartModelPackagingJobRequestRequestTypeDef,
    StartModelPackagingJobResponseTypeDef,
    StartModelRequestRequestTypeDef,
    StartModelResponseTypeDef,
    StopModelRequestRequestTypeDef,
    StopModelResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDatasetEntriesRequestRequestTypeDef,
    UpdateDatasetEntriesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("LookoutforVisionClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class LookoutforVisionClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LookoutforVisionClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#close)
        """

    def create_dataset(
        self, **kwargs: Unpack[CreateDatasetRequestRequestTypeDef]
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a new dataset in an Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/create_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#create_dataset)
        """

    def create_model(
        self, **kwargs: Unpack[CreateModelRequestRequestTypeDef]
    ) -> CreateModelResponseTypeDef:
        """
        Creates a new version of a model within an an Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/create_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#create_model)
        """

    def create_project(
        self, **kwargs: Unpack[CreateProjectRequestRequestTypeDef]
    ) -> CreateProjectResponseTypeDef:
        """
        Creates an empty Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/create_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#create_project)
        """

    def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing Amazon Lookout for Vision <code>dataset</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/delete_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#delete_dataset)
        """

    def delete_model(
        self, **kwargs: Unpack[DeleteModelRequestRequestTypeDef]
    ) -> DeleteModelResponseTypeDef:
        """
        Deletes an Amazon Lookout for Vision model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/delete_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#delete_model)
        """

    def delete_project(
        self, **kwargs: Unpack[DeleteProjectRequestRequestTypeDef]
    ) -> DeleteProjectResponseTypeDef:
        """
        Deletes an Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/delete_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#delete_project)
        """

    def describe_dataset(
        self, **kwargs: Unpack[DescribeDatasetRequestRequestTypeDef]
    ) -> DescribeDatasetResponseTypeDef:
        """
        Describe an Amazon Lookout for Vision dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/describe_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#describe_dataset)
        """

    def describe_model(
        self, **kwargs: Unpack[DescribeModelRequestRequestTypeDef]
    ) -> DescribeModelResponseTypeDef:
        """
        Describes a version of an Amazon Lookout for Vision model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/describe_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#describe_model)
        """

    def describe_model_packaging_job(
        self, **kwargs: Unpack[DescribeModelPackagingJobRequestRequestTypeDef]
    ) -> DescribeModelPackagingJobResponseTypeDef:
        """
        Describes an Amazon Lookout for Vision model packaging job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/describe_model_packaging_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#describe_model_packaging_job)
        """

    def describe_project(
        self, **kwargs: Unpack[DescribeProjectRequestRequestTypeDef]
    ) -> DescribeProjectResponseTypeDef:
        """
        Describes an Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/describe_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#describe_project)
        """

    def detect_anomalies(
        self, **kwargs: Unpack[DetectAnomaliesRequestRequestTypeDef]
    ) -> DetectAnomaliesResponseTypeDef:
        """
        Detects anomalies in an image that you supply.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/detect_anomalies.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#detect_anomalies)
        """

    def list_dataset_entries(
        self, **kwargs: Unpack[ListDatasetEntriesRequestRequestTypeDef]
    ) -> ListDatasetEntriesResponseTypeDef:
        """
        Lists the JSON Lines within a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/list_dataset_entries.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#list_dataset_entries)
        """

    def list_model_packaging_jobs(
        self, **kwargs: Unpack[ListModelPackagingJobsRequestRequestTypeDef]
    ) -> ListModelPackagingJobsResponseTypeDef:
        """
        Lists the model packaging jobs created for an Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/list_model_packaging_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#list_model_packaging_jobs)
        """

    def list_models(
        self, **kwargs: Unpack[ListModelsRequestRequestTypeDef]
    ) -> ListModelsResponseTypeDef:
        """
        Lists the versions of a model in an Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/list_models.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#list_models)
        """

    def list_projects(
        self, **kwargs: Unpack[ListProjectsRequestRequestTypeDef]
    ) -> ListProjectsResponseTypeDef:
        """
        Lists the Amazon Lookout for Vision projects in your AWS account that are in
        the AWS Region in which you call <code>ListProjects</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/list_projects.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#list_projects)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags attached to the specified Amazon Lookout for Vision
        model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#list_tags_for_resource)
        """

    def start_model(
        self, **kwargs: Unpack[StartModelRequestRequestTypeDef]
    ) -> StartModelResponseTypeDef:
        """
        Starts the running of the version of an Amazon Lookout for Vision model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/start_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#start_model)
        """

    def start_model_packaging_job(
        self, **kwargs: Unpack[StartModelPackagingJobRequestRequestTypeDef]
    ) -> StartModelPackagingJobResponseTypeDef:
        """
        Starts an Amazon Lookout for Vision model packaging job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/start_model_packaging_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#start_model_packaging_job)
        """

    def stop_model(
        self, **kwargs: Unpack[StopModelRequestRequestTypeDef]
    ) -> StopModelResponseTypeDef:
        """
        Stops the hosting of a running model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/stop_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#stop_model)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more key-value tags to an Amazon Lookout for Vision model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from an Amazon Lookout for Vision model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#untag_resource)
        """

    def update_dataset_entries(
        self, **kwargs: Unpack[UpdateDatasetEntriesRequestRequestTypeDef]
    ) -> UpdateDatasetEntriesResponseTypeDef:
        """
        Adds or updates one or more JSON Line entries in a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/update_dataset_entries.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#update_dataset_entries)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataset_entries"]
    ) -> ListDatasetEntriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_packaging_jobs"]
    ) -> ListModelPackagingJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_models"]) -> ListModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/client/#get_paginator)
        """
