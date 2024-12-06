"""
Type annotations for lookoutequipment service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_lookoutequipment.client import LookoutEquipmentClient

    session = Session()
    client: LookoutEquipmentClient = session.client("lookoutequipment")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateDatasetRequestRequestTypeDef,
    CreateDatasetResponseTypeDef,
    CreateInferenceSchedulerRequestRequestTypeDef,
    CreateInferenceSchedulerResponseTypeDef,
    CreateLabelGroupRequestRequestTypeDef,
    CreateLabelGroupResponseTypeDef,
    CreateLabelRequestRequestTypeDef,
    CreateLabelResponseTypeDef,
    CreateModelRequestRequestTypeDef,
    CreateModelResponseTypeDef,
    CreateRetrainingSchedulerRequestRequestTypeDef,
    CreateRetrainingSchedulerResponseTypeDef,
    DeleteDatasetRequestRequestTypeDef,
    DeleteInferenceSchedulerRequestRequestTypeDef,
    DeleteLabelGroupRequestRequestTypeDef,
    DeleteLabelRequestRequestTypeDef,
    DeleteModelRequestRequestTypeDef,
    DeleteResourcePolicyRequestRequestTypeDef,
    DeleteRetrainingSchedulerRequestRequestTypeDef,
    DescribeDataIngestionJobRequestRequestTypeDef,
    DescribeDataIngestionJobResponseTypeDef,
    DescribeDatasetRequestRequestTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeInferenceSchedulerRequestRequestTypeDef,
    DescribeInferenceSchedulerResponseTypeDef,
    DescribeLabelGroupRequestRequestTypeDef,
    DescribeLabelGroupResponseTypeDef,
    DescribeLabelRequestRequestTypeDef,
    DescribeLabelResponseTypeDef,
    DescribeModelRequestRequestTypeDef,
    DescribeModelResponseTypeDef,
    DescribeModelVersionRequestRequestTypeDef,
    DescribeModelVersionResponseTypeDef,
    DescribeResourcePolicyRequestRequestTypeDef,
    DescribeResourcePolicyResponseTypeDef,
    DescribeRetrainingSchedulerRequestRequestTypeDef,
    DescribeRetrainingSchedulerResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ImportDatasetRequestRequestTypeDef,
    ImportDatasetResponseTypeDef,
    ImportModelVersionRequestRequestTypeDef,
    ImportModelVersionResponseTypeDef,
    ListDataIngestionJobsRequestRequestTypeDef,
    ListDataIngestionJobsResponseTypeDef,
    ListDatasetsRequestRequestTypeDef,
    ListDatasetsResponseTypeDef,
    ListInferenceEventsRequestRequestTypeDef,
    ListInferenceEventsResponseTypeDef,
    ListInferenceExecutionsRequestRequestTypeDef,
    ListInferenceExecutionsResponseTypeDef,
    ListInferenceSchedulersRequestRequestTypeDef,
    ListInferenceSchedulersResponseTypeDef,
    ListLabelGroupsRequestRequestTypeDef,
    ListLabelGroupsResponseTypeDef,
    ListLabelsRequestRequestTypeDef,
    ListLabelsResponseTypeDef,
    ListModelsRequestRequestTypeDef,
    ListModelsResponseTypeDef,
    ListModelVersionsRequestRequestTypeDef,
    ListModelVersionsResponseTypeDef,
    ListRetrainingSchedulersRequestRequestTypeDef,
    ListRetrainingSchedulersResponseTypeDef,
    ListSensorStatisticsRequestRequestTypeDef,
    ListSensorStatisticsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutResourcePolicyRequestRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    StartDataIngestionJobRequestRequestTypeDef,
    StartDataIngestionJobResponseTypeDef,
    StartInferenceSchedulerRequestRequestTypeDef,
    StartInferenceSchedulerResponseTypeDef,
    StartRetrainingSchedulerRequestRequestTypeDef,
    StartRetrainingSchedulerResponseTypeDef,
    StopInferenceSchedulerRequestRequestTypeDef,
    StopInferenceSchedulerResponseTypeDef,
    StopRetrainingSchedulerRequestRequestTypeDef,
    StopRetrainingSchedulerResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateActiveModelVersionRequestRequestTypeDef,
    UpdateActiveModelVersionResponseTypeDef,
    UpdateInferenceSchedulerRequestRequestTypeDef,
    UpdateLabelGroupRequestRequestTypeDef,
    UpdateModelRequestRequestTypeDef,
    UpdateRetrainingSchedulerRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("LookoutEquipmentClient",)

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

class LookoutEquipmentClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LookoutEquipmentClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#close)
        """

    def create_dataset(
        self, **kwargs: Unpack[CreateDatasetRequestRequestTypeDef]
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a container for a collection of data being ingested for analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/create_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#create_dataset)
        """

    def create_inference_scheduler(
        self, **kwargs: Unpack[CreateInferenceSchedulerRequestRequestTypeDef]
    ) -> CreateInferenceSchedulerResponseTypeDef:
        """
        Creates a scheduled inference.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/create_inference_scheduler.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#create_inference_scheduler)
        """

    def create_label(
        self, **kwargs: Unpack[CreateLabelRequestRequestTypeDef]
    ) -> CreateLabelResponseTypeDef:
        """
        Creates a label for an event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/create_label.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#create_label)
        """

    def create_label_group(
        self, **kwargs: Unpack[CreateLabelGroupRequestRequestTypeDef]
    ) -> CreateLabelGroupResponseTypeDef:
        """
        Creates a group of labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/create_label_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#create_label_group)
        """

    def create_model(
        self, **kwargs: Unpack[CreateModelRequestRequestTypeDef]
    ) -> CreateModelResponseTypeDef:
        """
        Creates a machine learning model for data inference.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/create_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#create_model)
        """

    def create_retraining_scheduler(
        self, **kwargs: Unpack[CreateRetrainingSchedulerRequestRequestTypeDef]
    ) -> CreateRetrainingSchedulerResponseTypeDef:
        """
        Creates a retraining scheduler on the specified model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/create_retraining_scheduler.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#create_retraining_scheduler)
        """

    def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a dataset and associated artifacts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#delete_dataset)
        """

    def delete_inference_scheduler(
        self, **kwargs: Unpack[DeleteInferenceSchedulerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an inference scheduler that has been set up.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_inference_scheduler.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#delete_inference_scheduler)
        """

    def delete_label(
        self, **kwargs: Unpack[DeleteLabelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a label.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_label.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#delete_label)
        """

    def delete_label_group(
        self, **kwargs: Unpack[DeleteLabelGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a group of labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_label_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#delete_label_group)
        """

    def delete_model(
        self, **kwargs: Unpack[DeleteModelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a machine learning model currently available for Amazon Lookout for
        Equipment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#delete_model)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the resource policy attached to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#delete_resource_policy)
        """

    def delete_retraining_scheduler(
        self, **kwargs: Unpack[DeleteRetrainingSchedulerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a retraining scheduler from a model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_retraining_scheduler.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#delete_retraining_scheduler)
        """

    def describe_data_ingestion_job(
        self, **kwargs: Unpack[DescribeDataIngestionJobRequestRequestTypeDef]
    ) -> DescribeDataIngestionJobResponseTypeDef:
        """
        Provides information on a specific data ingestion job such as creation time,
        dataset ARN, and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_data_ingestion_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#describe_data_ingestion_job)
        """

    def describe_dataset(
        self, **kwargs: Unpack[DescribeDatasetRequestRequestTypeDef]
    ) -> DescribeDatasetResponseTypeDef:
        """
        Provides a JSON description of the data in each time series dataset, including
        names, column names, and data types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#describe_dataset)
        """

    def describe_inference_scheduler(
        self, **kwargs: Unpack[DescribeInferenceSchedulerRequestRequestTypeDef]
    ) -> DescribeInferenceSchedulerResponseTypeDef:
        """
        Specifies information about the inference scheduler being used, including name,
        model, status, and associated metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_inference_scheduler.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#describe_inference_scheduler)
        """

    def describe_label(
        self, **kwargs: Unpack[DescribeLabelRequestRequestTypeDef]
    ) -> DescribeLabelResponseTypeDef:
        """
        Returns the name of the label.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_label.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#describe_label)
        """

    def describe_label_group(
        self, **kwargs: Unpack[DescribeLabelGroupRequestRequestTypeDef]
    ) -> DescribeLabelGroupResponseTypeDef:
        """
        Returns information about the label group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_label_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#describe_label_group)
        """

    def describe_model(
        self, **kwargs: Unpack[DescribeModelRequestRequestTypeDef]
    ) -> DescribeModelResponseTypeDef:
        """
        Provides a JSON containing the overall information about a specific machine
        learning model, including model name and ARN, dataset, training and evaluation
        information, status, and so on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#describe_model)
        """

    def describe_model_version(
        self, **kwargs: Unpack[DescribeModelVersionRequestRequestTypeDef]
    ) -> DescribeModelVersionResponseTypeDef:
        """
        Retrieves information about a specific machine learning model version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_model_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#describe_model_version)
        """

    def describe_resource_policy(
        self, **kwargs: Unpack[DescribeResourcePolicyRequestRequestTypeDef]
    ) -> DescribeResourcePolicyResponseTypeDef:
        """
        Provides the details of a resource policy attached to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#describe_resource_policy)
        """

    def describe_retraining_scheduler(
        self, **kwargs: Unpack[DescribeRetrainingSchedulerRequestRequestTypeDef]
    ) -> DescribeRetrainingSchedulerResponseTypeDef:
        """
        Provides a description of the retraining scheduler, including information such
        as the model name and retraining parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_retraining_scheduler.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#describe_retraining_scheduler)
        """

    def import_dataset(
        self, **kwargs: Unpack[ImportDatasetRequestRequestTypeDef]
    ) -> ImportDatasetResponseTypeDef:
        """
        Imports a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/import_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#import_dataset)
        """

    def import_model_version(
        self, **kwargs: Unpack[ImportModelVersionRequestRequestTypeDef]
    ) -> ImportModelVersionResponseTypeDef:
        """
        Imports a model that has been trained successfully.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/import_model_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#import_model_version)
        """

    def list_data_ingestion_jobs(
        self, **kwargs: Unpack[ListDataIngestionJobsRequestRequestTypeDef]
    ) -> ListDataIngestionJobsResponseTypeDef:
        """
        Provides a list of all data ingestion jobs, including dataset name and ARN, S3
        location of the input data, status, and so on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_data_ingestion_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#list_data_ingestion_jobs)
        """

    def list_datasets(
        self, **kwargs: Unpack[ListDatasetsRequestRequestTypeDef]
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists all datasets currently available in your account, filtering on the
        dataset name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_datasets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#list_datasets)
        """

    def list_inference_events(
        self, **kwargs: Unpack[ListInferenceEventsRequestRequestTypeDef]
    ) -> ListInferenceEventsResponseTypeDef:
        """
        Lists all inference events that have been found for the specified inference
        scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_inference_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#list_inference_events)
        """

    def list_inference_executions(
        self, **kwargs: Unpack[ListInferenceExecutionsRequestRequestTypeDef]
    ) -> ListInferenceExecutionsResponseTypeDef:
        """
        Lists all inference executions that have been performed by the specified
        inference scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_inference_executions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#list_inference_executions)
        """

    def list_inference_schedulers(
        self, **kwargs: Unpack[ListInferenceSchedulersRequestRequestTypeDef]
    ) -> ListInferenceSchedulersResponseTypeDef:
        """
        Retrieves a list of all inference schedulers currently available for your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_inference_schedulers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#list_inference_schedulers)
        """

    def list_label_groups(
        self, **kwargs: Unpack[ListLabelGroupsRequestRequestTypeDef]
    ) -> ListLabelGroupsResponseTypeDef:
        """
        Returns a list of the label groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_label_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#list_label_groups)
        """

    def list_labels(
        self, **kwargs: Unpack[ListLabelsRequestRequestTypeDef]
    ) -> ListLabelsResponseTypeDef:
        """
        Provides a list of labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_labels.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#list_labels)
        """

    def list_model_versions(
        self, **kwargs: Unpack[ListModelVersionsRequestRequestTypeDef]
    ) -> ListModelVersionsResponseTypeDef:
        """
        Generates a list of all model versions for a given model, including the model
        version, model version ARN, and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_model_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#list_model_versions)
        """

    def list_models(
        self, **kwargs: Unpack[ListModelsRequestRequestTypeDef]
    ) -> ListModelsResponseTypeDef:
        """
        Generates a list of all models in the account, including model name and ARN,
        dataset, and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_models.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#list_models)
        """

    def list_retraining_schedulers(
        self, **kwargs: Unpack[ListRetrainingSchedulersRequestRequestTypeDef]
    ) -> ListRetrainingSchedulersResponseTypeDef:
        """
        Lists all retraining schedulers in your account, filtering by model name prefix
        and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_retraining_schedulers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#list_retraining_schedulers)
        """

    def list_sensor_statistics(
        self, **kwargs: Unpack[ListSensorStatisticsRequestRequestTypeDef]
    ) -> ListSensorStatisticsResponseTypeDef:
        """
        Lists statistics about the data collected for each of the sensors that have
        been successfully ingested in the particular dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_sensor_statistics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#list_sensor_statistics)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all the tags for a specified resource, including key and value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#list_tags_for_resource)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Creates a resource control policy for a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/put_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#put_resource_policy)
        """

    def start_data_ingestion_job(
        self, **kwargs: Unpack[StartDataIngestionJobRequestRequestTypeDef]
    ) -> StartDataIngestionJobResponseTypeDef:
        """
        Starts a data ingestion job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/start_data_ingestion_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#start_data_ingestion_job)
        """

    def start_inference_scheduler(
        self, **kwargs: Unpack[StartInferenceSchedulerRequestRequestTypeDef]
    ) -> StartInferenceSchedulerResponseTypeDef:
        """
        Starts an inference scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/start_inference_scheduler.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#start_inference_scheduler)
        """

    def start_retraining_scheduler(
        self, **kwargs: Unpack[StartRetrainingSchedulerRequestRequestTypeDef]
    ) -> StartRetrainingSchedulerResponseTypeDef:
        """
        Starts a retraining scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/start_retraining_scheduler.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#start_retraining_scheduler)
        """

    def stop_inference_scheduler(
        self, **kwargs: Unpack[StopInferenceSchedulerRequestRequestTypeDef]
    ) -> StopInferenceSchedulerResponseTypeDef:
        """
        Stops an inference scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/stop_inference_scheduler.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#stop_inference_scheduler)
        """

    def stop_retraining_scheduler(
        self, **kwargs: Unpack[StopRetrainingSchedulerRequestRequestTypeDef]
    ) -> StopRetrainingSchedulerResponseTypeDef:
        """
        Stops a retraining scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/stop_retraining_scheduler.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#stop_retraining_scheduler)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates a given tag to a resource in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a specific tag from a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#untag_resource)
        """

    def update_active_model_version(
        self, **kwargs: Unpack[UpdateActiveModelVersionRequestRequestTypeDef]
    ) -> UpdateActiveModelVersionResponseTypeDef:
        """
        Sets the active model version for a given machine learning model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/update_active_model_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#update_active_model_version)
        """

    def update_inference_scheduler(
        self, **kwargs: Unpack[UpdateInferenceSchedulerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an inference scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/update_inference_scheduler.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#update_inference_scheduler)
        """

    def update_label_group(
        self, **kwargs: Unpack[UpdateLabelGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the label group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/update_label_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#update_label_group)
        """

    def update_model(
        self, **kwargs: Unpack[UpdateModelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a model in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/update_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#update_model)
        """

    def update_retraining_scheduler(
        self, **kwargs: Unpack[UpdateRetrainingSchedulerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a retraining scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/update_retraining_scheduler.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lookoutequipment/client/#update_retraining_scheduler)
        """
