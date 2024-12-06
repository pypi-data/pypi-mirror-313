"""
Type annotations for cleanroomsml service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cleanroomsml.client import CleanRoomsMLClient

    session = Session()
    client: CleanRoomsMLClient = session.client("cleanroomsml")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAudienceExportJobsPaginator,
    ListAudienceGenerationJobsPaginator,
    ListAudienceModelsPaginator,
    ListCollaborationConfiguredModelAlgorithmAssociationsPaginator,
    ListCollaborationMLInputChannelsPaginator,
    ListCollaborationTrainedModelExportJobsPaginator,
    ListCollaborationTrainedModelInferenceJobsPaginator,
    ListCollaborationTrainedModelsPaginator,
    ListConfiguredAudienceModelsPaginator,
    ListConfiguredModelAlgorithmAssociationsPaginator,
    ListConfiguredModelAlgorithmsPaginator,
    ListMLInputChannelsPaginator,
    ListTrainedModelInferenceJobsPaginator,
    ListTrainedModelsPaginator,
    ListTrainingDatasetsPaginator,
)
from .type_defs import (
    CancelTrainedModelInferenceJobRequestRequestTypeDef,
    CancelTrainedModelRequestRequestTypeDef,
    CreateAudienceModelRequestRequestTypeDef,
    CreateAudienceModelResponseTypeDef,
    CreateConfiguredAudienceModelRequestRequestTypeDef,
    CreateConfiguredAudienceModelResponseTypeDef,
    CreateConfiguredModelAlgorithmAssociationRequestRequestTypeDef,
    CreateConfiguredModelAlgorithmAssociationResponseTypeDef,
    CreateConfiguredModelAlgorithmRequestRequestTypeDef,
    CreateConfiguredModelAlgorithmResponseTypeDef,
    CreateMLInputChannelRequestRequestTypeDef,
    CreateMLInputChannelResponseTypeDef,
    CreateTrainedModelRequestRequestTypeDef,
    CreateTrainedModelResponseTypeDef,
    CreateTrainingDatasetRequestRequestTypeDef,
    CreateTrainingDatasetResponseTypeDef,
    DeleteAudienceGenerationJobRequestRequestTypeDef,
    DeleteAudienceModelRequestRequestTypeDef,
    DeleteConfiguredAudienceModelPolicyRequestRequestTypeDef,
    DeleteConfiguredAudienceModelRequestRequestTypeDef,
    DeleteConfiguredModelAlgorithmAssociationRequestRequestTypeDef,
    DeleteConfiguredModelAlgorithmRequestRequestTypeDef,
    DeleteMLConfigurationRequestRequestTypeDef,
    DeleteMLInputChannelDataRequestRequestTypeDef,
    DeleteTrainedModelOutputRequestRequestTypeDef,
    DeleteTrainingDatasetRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAudienceGenerationJobRequestRequestTypeDef,
    GetAudienceGenerationJobResponseTypeDef,
    GetAudienceModelRequestRequestTypeDef,
    GetAudienceModelResponseTypeDef,
    GetCollaborationConfiguredModelAlgorithmAssociationRequestRequestTypeDef,
    GetCollaborationConfiguredModelAlgorithmAssociationResponseTypeDef,
    GetCollaborationMLInputChannelRequestRequestTypeDef,
    GetCollaborationMLInputChannelResponseTypeDef,
    GetCollaborationTrainedModelRequestRequestTypeDef,
    GetCollaborationTrainedModelResponseTypeDef,
    GetConfiguredAudienceModelPolicyRequestRequestTypeDef,
    GetConfiguredAudienceModelPolicyResponseTypeDef,
    GetConfiguredAudienceModelRequestRequestTypeDef,
    GetConfiguredAudienceModelResponseTypeDef,
    GetConfiguredModelAlgorithmAssociationRequestRequestTypeDef,
    GetConfiguredModelAlgorithmAssociationResponseTypeDef,
    GetConfiguredModelAlgorithmRequestRequestTypeDef,
    GetConfiguredModelAlgorithmResponseTypeDef,
    GetMLConfigurationRequestRequestTypeDef,
    GetMLConfigurationResponseTypeDef,
    GetMLInputChannelRequestRequestTypeDef,
    GetMLInputChannelResponseTypeDef,
    GetTrainedModelInferenceJobRequestRequestTypeDef,
    GetTrainedModelInferenceJobResponseTypeDef,
    GetTrainedModelRequestRequestTypeDef,
    GetTrainedModelResponseTypeDef,
    GetTrainingDatasetRequestRequestTypeDef,
    GetTrainingDatasetResponseTypeDef,
    ListAudienceExportJobsRequestRequestTypeDef,
    ListAudienceExportJobsResponseTypeDef,
    ListAudienceGenerationJobsRequestRequestTypeDef,
    ListAudienceGenerationJobsResponseTypeDef,
    ListAudienceModelsRequestRequestTypeDef,
    ListAudienceModelsResponseTypeDef,
    ListCollaborationConfiguredModelAlgorithmAssociationsRequestRequestTypeDef,
    ListCollaborationConfiguredModelAlgorithmAssociationsResponseTypeDef,
    ListCollaborationMLInputChannelsRequestRequestTypeDef,
    ListCollaborationMLInputChannelsResponseTypeDef,
    ListCollaborationTrainedModelExportJobsRequestRequestTypeDef,
    ListCollaborationTrainedModelExportJobsResponseTypeDef,
    ListCollaborationTrainedModelInferenceJobsRequestRequestTypeDef,
    ListCollaborationTrainedModelInferenceJobsResponseTypeDef,
    ListCollaborationTrainedModelsRequestRequestTypeDef,
    ListCollaborationTrainedModelsResponseTypeDef,
    ListConfiguredAudienceModelsRequestRequestTypeDef,
    ListConfiguredAudienceModelsResponseTypeDef,
    ListConfiguredModelAlgorithmAssociationsRequestRequestTypeDef,
    ListConfiguredModelAlgorithmAssociationsResponseTypeDef,
    ListConfiguredModelAlgorithmsRequestRequestTypeDef,
    ListConfiguredModelAlgorithmsResponseTypeDef,
    ListMLInputChannelsRequestRequestTypeDef,
    ListMLInputChannelsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrainedModelInferenceJobsRequestRequestTypeDef,
    ListTrainedModelInferenceJobsResponseTypeDef,
    ListTrainedModelsRequestRequestTypeDef,
    ListTrainedModelsResponseTypeDef,
    ListTrainingDatasetsRequestRequestTypeDef,
    ListTrainingDatasetsResponseTypeDef,
    PutConfiguredAudienceModelPolicyRequestRequestTypeDef,
    PutConfiguredAudienceModelPolicyResponseTypeDef,
    PutMLConfigurationRequestRequestTypeDef,
    StartAudienceExportJobRequestRequestTypeDef,
    StartAudienceGenerationJobRequestRequestTypeDef,
    StartAudienceGenerationJobResponseTypeDef,
    StartTrainedModelExportJobRequestRequestTypeDef,
    StartTrainedModelInferenceJobRequestRequestTypeDef,
    StartTrainedModelInferenceJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateConfiguredAudienceModelRequestRequestTypeDef,
    UpdateConfiguredAudienceModelResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CleanRoomsMLClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CleanRoomsMLClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CleanRoomsMLClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml.html#CleanRoomsML.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#close)
        """

    def cancel_trained_model(
        self, **kwargs: Unpack[CancelTrainedModelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Submits a request to cancel the trained model job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/cancel_trained_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#cancel_trained_model)
        """

    def cancel_trained_model_inference_job(
        self, **kwargs: Unpack[CancelTrainedModelInferenceJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Submits a request to cancel a trained model inference job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/cancel_trained_model_inference_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#cancel_trained_model_inference_job)
        """

    def create_audience_model(
        self, **kwargs: Unpack[CreateAudienceModelRequestRequestTypeDef]
    ) -> CreateAudienceModelResponseTypeDef:
        """
        Defines the information necessary to create an audience model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/create_audience_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#create_audience_model)
        """

    def create_configured_audience_model(
        self, **kwargs: Unpack[CreateConfiguredAudienceModelRequestRequestTypeDef]
    ) -> CreateConfiguredAudienceModelResponseTypeDef:
        """
        Defines the information necessary to create a configured audience model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/create_configured_audience_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#create_configured_audience_model)
        """

    def create_configured_model_algorithm(
        self, **kwargs: Unpack[CreateConfiguredModelAlgorithmRequestRequestTypeDef]
    ) -> CreateConfiguredModelAlgorithmResponseTypeDef:
        """
        Creates a configured model algorithm using a container image stored in an ECR
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/create_configured_model_algorithm.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#create_configured_model_algorithm)
        """

    def create_configured_model_algorithm_association(
        self, **kwargs: Unpack[CreateConfiguredModelAlgorithmAssociationRequestRequestTypeDef]
    ) -> CreateConfiguredModelAlgorithmAssociationResponseTypeDef:
        """
        Associates a configured model algorithm to a collaboration for use by any
        member of the collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/create_configured_model_algorithm_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#create_configured_model_algorithm_association)
        """

    def create_ml_input_channel(
        self, **kwargs: Unpack[CreateMLInputChannelRequestRequestTypeDef]
    ) -> CreateMLInputChannelResponseTypeDef:
        """
        Provides the information to create an ML input channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/create_ml_input_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#create_ml_input_channel)
        """

    def create_trained_model(
        self, **kwargs: Unpack[CreateTrainedModelRequestRequestTypeDef]
    ) -> CreateTrainedModelResponseTypeDef:
        """
        Creates a trained model from an associated configured model algorithm using
        data from any member of the collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/create_trained_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#create_trained_model)
        """

    def create_training_dataset(
        self, **kwargs: Unpack[CreateTrainingDatasetRequestRequestTypeDef]
    ) -> CreateTrainingDatasetResponseTypeDef:
        """
        Defines the information necessary to create a training dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/create_training_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#create_training_dataset)
        """

    def delete_audience_generation_job(
        self, **kwargs: Unpack[DeleteAudienceGenerationJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified audience generation job, and removes all data associated
        with the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/delete_audience_generation_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_audience_generation_job)
        """

    def delete_audience_model(
        self, **kwargs: Unpack[DeleteAudienceModelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specifies an audience model that you want to delete.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/delete_audience_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_audience_model)
        """

    def delete_configured_audience_model(
        self, **kwargs: Unpack[DeleteConfiguredAudienceModelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified configured audience model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/delete_configured_audience_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_configured_audience_model)
        """

    def delete_configured_audience_model_policy(
        self, **kwargs: Unpack[DeleteConfiguredAudienceModelPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified configured audience model policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/delete_configured_audience_model_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_configured_audience_model_policy)
        """

    def delete_configured_model_algorithm(
        self, **kwargs: Unpack[DeleteConfiguredModelAlgorithmRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a configured model algorithm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/delete_configured_model_algorithm.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_configured_model_algorithm)
        """

    def delete_configured_model_algorithm_association(
        self, **kwargs: Unpack[DeleteConfiguredModelAlgorithmAssociationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a configured model algorithm association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/delete_configured_model_algorithm_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_configured_model_algorithm_association)
        """

    def delete_ml_configuration(
        self, **kwargs: Unpack[DeleteMLConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a ML modeling configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/delete_ml_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_ml_configuration)
        """

    def delete_ml_input_channel_data(
        self, **kwargs: Unpack[DeleteMLInputChannelDataRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Provides the information necessary to delete an ML input channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/delete_ml_input_channel_data.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_ml_input_channel_data)
        """

    def delete_trained_model_output(
        self, **kwargs: Unpack[DeleteTrainedModelOutputRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the output of a trained model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/delete_trained_model_output.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_trained_model_output)
        """

    def delete_training_dataset(
        self, **kwargs: Unpack[DeleteTrainingDatasetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specifies a training dataset that you want to delete.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/delete_training_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#delete_training_dataset)
        """

    def get_audience_generation_job(
        self, **kwargs: Unpack[GetAudienceGenerationJobRequestRequestTypeDef]
    ) -> GetAudienceGenerationJobResponseTypeDef:
        """
        Returns information about an audience generation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_audience_generation_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_audience_generation_job)
        """

    def get_audience_model(
        self, **kwargs: Unpack[GetAudienceModelRequestRequestTypeDef]
    ) -> GetAudienceModelResponseTypeDef:
        """
        Returns information about an audience model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_audience_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_audience_model)
        """

    def get_collaboration_configured_model_algorithm_association(
        self,
        **kwargs: Unpack[GetCollaborationConfiguredModelAlgorithmAssociationRequestRequestTypeDef],
    ) -> GetCollaborationConfiguredModelAlgorithmAssociationResponseTypeDef:
        """
        Returns information about the configured model algorithm association in a
        collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_collaboration_configured_model_algorithm_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_collaboration_configured_model_algorithm_association)
        """

    def get_collaboration_ml_input_channel(
        self, **kwargs: Unpack[GetCollaborationMLInputChannelRequestRequestTypeDef]
    ) -> GetCollaborationMLInputChannelResponseTypeDef:
        """
        Returns information about a specific ML input channel in a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_collaboration_ml_input_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_collaboration_ml_input_channel)
        """

    def get_collaboration_trained_model(
        self, **kwargs: Unpack[GetCollaborationTrainedModelRequestRequestTypeDef]
    ) -> GetCollaborationTrainedModelResponseTypeDef:
        """
        Returns information about a trained model in a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_collaboration_trained_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_collaboration_trained_model)
        """

    def get_configured_audience_model(
        self, **kwargs: Unpack[GetConfiguredAudienceModelRequestRequestTypeDef]
    ) -> GetConfiguredAudienceModelResponseTypeDef:
        """
        Returns information about a specified configured audience model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_configured_audience_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_configured_audience_model)
        """

    def get_configured_audience_model_policy(
        self, **kwargs: Unpack[GetConfiguredAudienceModelPolicyRequestRequestTypeDef]
    ) -> GetConfiguredAudienceModelPolicyResponseTypeDef:
        """
        Returns information about a configured audience model policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_configured_audience_model_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_configured_audience_model_policy)
        """

    def get_configured_model_algorithm(
        self, **kwargs: Unpack[GetConfiguredModelAlgorithmRequestRequestTypeDef]
    ) -> GetConfiguredModelAlgorithmResponseTypeDef:
        """
        Returns information about a configured model algorithm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_configured_model_algorithm.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_configured_model_algorithm)
        """

    def get_configured_model_algorithm_association(
        self, **kwargs: Unpack[GetConfiguredModelAlgorithmAssociationRequestRequestTypeDef]
    ) -> GetConfiguredModelAlgorithmAssociationResponseTypeDef:
        """
        Returns information about a configured model algorithm association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_configured_model_algorithm_association.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_configured_model_algorithm_association)
        """

    def get_ml_configuration(
        self, **kwargs: Unpack[GetMLConfigurationRequestRequestTypeDef]
    ) -> GetMLConfigurationResponseTypeDef:
        """
        Returns information about a specific ML configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_ml_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_ml_configuration)
        """

    def get_ml_input_channel(
        self, **kwargs: Unpack[GetMLInputChannelRequestRequestTypeDef]
    ) -> GetMLInputChannelResponseTypeDef:
        """
        Returns information about an ML input channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_ml_input_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_ml_input_channel)
        """

    def get_trained_model(
        self, **kwargs: Unpack[GetTrainedModelRequestRequestTypeDef]
    ) -> GetTrainedModelResponseTypeDef:
        """
        Returns information about a trained model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_trained_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_trained_model)
        """

    def get_trained_model_inference_job(
        self, **kwargs: Unpack[GetTrainedModelInferenceJobRequestRequestTypeDef]
    ) -> GetTrainedModelInferenceJobResponseTypeDef:
        """
        Returns information about a trained model inference job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_trained_model_inference_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_trained_model_inference_job)
        """

    def get_training_dataset(
        self, **kwargs: Unpack[GetTrainingDatasetRequestRequestTypeDef]
    ) -> GetTrainingDatasetResponseTypeDef:
        """
        Returns information about a training dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_training_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_training_dataset)
        """

    def list_audience_export_jobs(
        self, **kwargs: Unpack[ListAudienceExportJobsRequestRequestTypeDef]
    ) -> ListAudienceExportJobsResponseTypeDef:
        """
        Returns a list of the audience export jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_audience_export_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_audience_export_jobs)
        """

    def list_audience_generation_jobs(
        self, **kwargs: Unpack[ListAudienceGenerationJobsRequestRequestTypeDef]
    ) -> ListAudienceGenerationJobsResponseTypeDef:
        """
        Returns a list of audience generation jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_audience_generation_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_audience_generation_jobs)
        """

    def list_audience_models(
        self, **kwargs: Unpack[ListAudienceModelsRequestRequestTypeDef]
    ) -> ListAudienceModelsResponseTypeDef:
        """
        Returns a list of audience models.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_audience_models.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_audience_models)
        """

    def list_collaboration_configured_model_algorithm_associations(
        self,
        **kwargs: Unpack[
            ListCollaborationConfiguredModelAlgorithmAssociationsRequestRequestTypeDef
        ],
    ) -> ListCollaborationConfiguredModelAlgorithmAssociationsResponseTypeDef:
        """
        Returns a list of the configured model algorithm associations in a
        collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_collaboration_configured_model_algorithm_associations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_collaboration_configured_model_algorithm_associations)
        """

    def list_collaboration_ml_input_channels(
        self, **kwargs: Unpack[ListCollaborationMLInputChannelsRequestRequestTypeDef]
    ) -> ListCollaborationMLInputChannelsResponseTypeDef:
        """
        Returns a list of the ML input channels in a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_collaboration_ml_input_channels.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_collaboration_ml_input_channels)
        """

    def list_collaboration_trained_model_export_jobs(
        self, **kwargs: Unpack[ListCollaborationTrainedModelExportJobsRequestRequestTypeDef]
    ) -> ListCollaborationTrainedModelExportJobsResponseTypeDef:
        """
        Returns a list of the export jobs for a trained model in a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_collaboration_trained_model_export_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_collaboration_trained_model_export_jobs)
        """

    def list_collaboration_trained_model_inference_jobs(
        self, **kwargs: Unpack[ListCollaborationTrainedModelInferenceJobsRequestRequestTypeDef]
    ) -> ListCollaborationTrainedModelInferenceJobsResponseTypeDef:
        """
        Returns a list of trained model inference jobs in a specified collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_collaboration_trained_model_inference_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_collaboration_trained_model_inference_jobs)
        """

    def list_collaboration_trained_models(
        self, **kwargs: Unpack[ListCollaborationTrainedModelsRequestRequestTypeDef]
    ) -> ListCollaborationTrainedModelsResponseTypeDef:
        """
        Returns a list of the trained models in a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_collaboration_trained_models.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_collaboration_trained_models)
        """

    def list_configured_audience_models(
        self, **kwargs: Unpack[ListConfiguredAudienceModelsRequestRequestTypeDef]
    ) -> ListConfiguredAudienceModelsResponseTypeDef:
        """
        Returns a list of the configured audience models.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_configured_audience_models.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_configured_audience_models)
        """

    def list_configured_model_algorithm_associations(
        self, **kwargs: Unpack[ListConfiguredModelAlgorithmAssociationsRequestRequestTypeDef]
    ) -> ListConfiguredModelAlgorithmAssociationsResponseTypeDef:
        """
        Returns a list of configured model algorithm associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_configured_model_algorithm_associations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_configured_model_algorithm_associations)
        """

    def list_configured_model_algorithms(
        self, **kwargs: Unpack[ListConfiguredModelAlgorithmsRequestRequestTypeDef]
    ) -> ListConfiguredModelAlgorithmsResponseTypeDef:
        """
        Returns a list of configured model algorithms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_configured_model_algorithms.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_configured_model_algorithms)
        """

    def list_ml_input_channels(
        self, **kwargs: Unpack[ListMLInputChannelsRequestRequestTypeDef]
    ) -> ListMLInputChannelsResponseTypeDef:
        """
        Returns a list of ML input channels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_ml_input_channels.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_ml_input_channels)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a provided resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_tags_for_resource)
        """

    def list_trained_model_inference_jobs(
        self, **kwargs: Unpack[ListTrainedModelInferenceJobsRequestRequestTypeDef]
    ) -> ListTrainedModelInferenceJobsResponseTypeDef:
        """
        Returns a list of trained model inference jobs that match the request
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_trained_model_inference_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_trained_model_inference_jobs)
        """

    def list_trained_models(
        self, **kwargs: Unpack[ListTrainedModelsRequestRequestTypeDef]
    ) -> ListTrainedModelsResponseTypeDef:
        """
        Returns a list of trained models.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_trained_models.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_trained_models)
        """

    def list_training_datasets(
        self, **kwargs: Unpack[ListTrainingDatasetsRequestRequestTypeDef]
    ) -> ListTrainingDatasetsResponseTypeDef:
        """
        Returns a list of training datasets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/list_training_datasets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#list_training_datasets)
        """

    def put_configured_audience_model_policy(
        self, **kwargs: Unpack[PutConfiguredAudienceModelPolicyRequestRequestTypeDef]
    ) -> PutConfiguredAudienceModelPolicyResponseTypeDef:
        """
        Create or update the resource policy for a configured audience model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/put_configured_audience_model_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#put_configured_audience_model_policy)
        """

    def put_ml_configuration(
        self, **kwargs: Unpack[PutMLConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns information about an ML configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/put_ml_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#put_ml_configuration)
        """

    def start_audience_export_job(
        self, **kwargs: Unpack[StartAudienceExportJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Export an audience of a specified size after you have generated an audience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/start_audience_export_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#start_audience_export_job)
        """

    def start_audience_generation_job(
        self, **kwargs: Unpack[StartAudienceGenerationJobRequestRequestTypeDef]
    ) -> StartAudienceGenerationJobResponseTypeDef:
        """
        Information necessary to start the audience generation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/start_audience_generation_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#start_audience_generation_job)
        """

    def start_trained_model_export_job(
        self, **kwargs: Unpack[StartTrainedModelExportJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Provides the information necessary to start a trained model export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/start_trained_model_export_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#start_trained_model_export_job)
        """

    def start_trained_model_inference_job(
        self, **kwargs: Unpack[StartTrainedModelInferenceJobRequestRequestTypeDef]
    ) -> StartTrainedModelInferenceJobResponseTypeDef:
        """
        Defines the information necessary to begin a trained model inference job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/start_trained_model_inference_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#start_trained_model_inference_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds metadata tags to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes metadata tags from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#untag_resource)
        """

    def update_configured_audience_model(
        self, **kwargs: Unpack[UpdateConfiguredAudienceModelRequestRequestTypeDef]
    ) -> UpdateConfiguredAudienceModelResponseTypeDef:
        """
        Provides the information necessary to update a configured audience model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/update_configured_audience_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#update_configured_audience_model)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audience_export_jobs"]
    ) -> ListAudienceExportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audience_generation_jobs"]
    ) -> ListAudienceGenerationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audience_models"]
    ) -> ListAudienceModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_collaboration_configured_model_algorithm_associations"]
    ) -> ListCollaborationConfiguredModelAlgorithmAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_collaboration_ml_input_channels"]
    ) -> ListCollaborationMLInputChannelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_collaboration_trained_model_export_jobs"]
    ) -> ListCollaborationTrainedModelExportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_collaboration_trained_model_inference_jobs"]
    ) -> ListCollaborationTrainedModelInferenceJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_collaboration_trained_models"]
    ) -> ListCollaborationTrainedModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configured_audience_models"]
    ) -> ListConfiguredAudienceModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configured_model_algorithm_associations"]
    ) -> ListConfiguredModelAlgorithmAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configured_model_algorithms"]
    ) -> ListConfiguredModelAlgorithmsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ml_input_channels"]
    ) -> ListMLInputChannelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_trained_model_inference_jobs"]
    ) -> ListTrainedModelInferenceJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_trained_models"]
    ) -> ListTrainedModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_training_datasets"]
    ) -> ListTrainingDatasetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/client/#get_paginator)
        """
