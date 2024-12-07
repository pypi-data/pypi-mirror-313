"""
Type annotations for cleanroomsml service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cleanroomsml.client import CleanRoomsMLClient
    from mypy_boto3_cleanroomsml.paginator import (
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

    session = Session()
    client: CleanRoomsMLClient = session.client("cleanroomsml")

    list_audience_export_jobs_paginator: ListAudienceExportJobsPaginator = client.get_paginator("list_audience_export_jobs")
    list_audience_generation_jobs_paginator: ListAudienceGenerationJobsPaginator = client.get_paginator("list_audience_generation_jobs")
    list_audience_models_paginator: ListAudienceModelsPaginator = client.get_paginator("list_audience_models")
    list_collaboration_configured_model_algorithm_associations_paginator: ListCollaborationConfiguredModelAlgorithmAssociationsPaginator = client.get_paginator("list_collaboration_configured_model_algorithm_associations")
    list_collaboration_ml_input_channels_paginator: ListCollaborationMLInputChannelsPaginator = client.get_paginator("list_collaboration_ml_input_channels")
    list_collaboration_trained_model_export_jobs_paginator: ListCollaborationTrainedModelExportJobsPaginator = client.get_paginator("list_collaboration_trained_model_export_jobs")
    list_collaboration_trained_model_inference_jobs_paginator: ListCollaborationTrainedModelInferenceJobsPaginator = client.get_paginator("list_collaboration_trained_model_inference_jobs")
    list_collaboration_trained_models_paginator: ListCollaborationTrainedModelsPaginator = client.get_paginator("list_collaboration_trained_models")
    list_configured_audience_models_paginator: ListConfiguredAudienceModelsPaginator = client.get_paginator("list_configured_audience_models")
    list_configured_model_algorithm_associations_paginator: ListConfiguredModelAlgorithmAssociationsPaginator = client.get_paginator("list_configured_model_algorithm_associations")
    list_configured_model_algorithms_paginator: ListConfiguredModelAlgorithmsPaginator = client.get_paginator("list_configured_model_algorithms")
    list_ml_input_channels_paginator: ListMLInputChannelsPaginator = client.get_paginator("list_ml_input_channels")
    list_trained_model_inference_jobs_paginator: ListTrainedModelInferenceJobsPaginator = client.get_paginator("list_trained_model_inference_jobs")
    list_trained_models_paginator: ListTrainedModelsPaginator = client.get_paginator("list_trained_models")
    list_training_datasets_paginator: ListTrainingDatasetsPaginator = client.get_paginator("list_training_datasets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAudienceExportJobsRequestListAudienceExportJobsPaginateTypeDef,
    ListAudienceExportJobsResponseTypeDef,
    ListAudienceGenerationJobsRequestListAudienceGenerationJobsPaginateTypeDef,
    ListAudienceGenerationJobsResponseTypeDef,
    ListAudienceModelsRequestListAudienceModelsPaginateTypeDef,
    ListAudienceModelsResponseTypeDef,
    ListCollaborationConfiguredModelAlgorithmAssociationsRequestListCollaborationConfiguredModelAlgorithmAssociationsPaginateTypeDef,
    ListCollaborationConfiguredModelAlgorithmAssociationsResponseTypeDef,
    ListCollaborationMLInputChannelsRequestListCollaborationMLInputChannelsPaginateTypeDef,
    ListCollaborationMLInputChannelsResponseTypeDef,
    ListCollaborationTrainedModelExportJobsRequestListCollaborationTrainedModelExportJobsPaginateTypeDef,
    ListCollaborationTrainedModelExportJobsResponseTypeDef,
    ListCollaborationTrainedModelInferenceJobsRequestListCollaborationTrainedModelInferenceJobsPaginateTypeDef,
    ListCollaborationTrainedModelInferenceJobsResponseTypeDef,
    ListCollaborationTrainedModelsRequestListCollaborationTrainedModelsPaginateTypeDef,
    ListCollaborationTrainedModelsResponseTypeDef,
    ListConfiguredAudienceModelsRequestListConfiguredAudienceModelsPaginateTypeDef,
    ListConfiguredAudienceModelsResponseTypeDef,
    ListConfiguredModelAlgorithmAssociationsRequestListConfiguredModelAlgorithmAssociationsPaginateTypeDef,
    ListConfiguredModelAlgorithmAssociationsResponseTypeDef,
    ListConfiguredModelAlgorithmsRequestListConfiguredModelAlgorithmsPaginateTypeDef,
    ListConfiguredModelAlgorithmsResponseTypeDef,
    ListMLInputChannelsRequestListMLInputChannelsPaginateTypeDef,
    ListMLInputChannelsResponseTypeDef,
    ListTrainedModelInferenceJobsRequestListTrainedModelInferenceJobsPaginateTypeDef,
    ListTrainedModelInferenceJobsResponseTypeDef,
    ListTrainedModelsRequestListTrainedModelsPaginateTypeDef,
    ListTrainedModelsResponseTypeDef,
    ListTrainingDatasetsRequestListTrainingDatasetsPaginateTypeDef,
    ListTrainingDatasetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAudienceExportJobsPaginator",
    "ListAudienceGenerationJobsPaginator",
    "ListAudienceModelsPaginator",
    "ListCollaborationConfiguredModelAlgorithmAssociationsPaginator",
    "ListCollaborationMLInputChannelsPaginator",
    "ListCollaborationTrainedModelExportJobsPaginator",
    "ListCollaborationTrainedModelInferenceJobsPaginator",
    "ListCollaborationTrainedModelsPaginator",
    "ListConfiguredAudienceModelsPaginator",
    "ListConfiguredModelAlgorithmAssociationsPaginator",
    "ListConfiguredModelAlgorithmsPaginator",
    "ListMLInputChannelsPaginator",
    "ListTrainedModelInferenceJobsPaginator",
    "ListTrainedModelsPaginator",
    "ListTrainingDatasetsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAudienceExportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceExportJobs.html#CleanRoomsML.Paginator.ListAudienceExportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listaudienceexportjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAudienceExportJobsRequestListAudienceExportJobsPaginateTypeDef]
    ) -> _PageIterator[ListAudienceExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceExportJobs.html#CleanRoomsML.Paginator.ListAudienceExportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listaudienceexportjobspaginator)
        """

class ListAudienceGenerationJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceGenerationJobs.html#CleanRoomsML.Paginator.ListAudienceGenerationJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listaudiencegenerationjobspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAudienceGenerationJobsRequestListAudienceGenerationJobsPaginateTypeDef
        ],
    ) -> _PageIterator[ListAudienceGenerationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceGenerationJobs.html#CleanRoomsML.Paginator.ListAudienceGenerationJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listaudiencegenerationjobspaginator)
        """

class ListAudienceModelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceModels.html#CleanRoomsML.Paginator.ListAudienceModels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listaudiencemodelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAudienceModelsRequestListAudienceModelsPaginateTypeDef]
    ) -> _PageIterator[ListAudienceModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceModels.html#CleanRoomsML.Paginator.ListAudienceModels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listaudiencemodelspaginator)
        """

class ListCollaborationConfiguredModelAlgorithmAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationConfiguredModelAlgorithmAssociations.html#CleanRoomsML.Paginator.ListCollaborationConfiguredModelAlgorithmAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listcollaborationconfiguredmodelalgorithmassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCollaborationConfiguredModelAlgorithmAssociationsRequestListCollaborationConfiguredModelAlgorithmAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCollaborationConfiguredModelAlgorithmAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationConfiguredModelAlgorithmAssociations.html#CleanRoomsML.Paginator.ListCollaborationConfiguredModelAlgorithmAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listcollaborationconfiguredmodelalgorithmassociationspaginator)
        """

class ListCollaborationMLInputChannelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationMLInputChannels.html#CleanRoomsML.Paginator.ListCollaborationMLInputChannels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listcollaborationmlinputchannelspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCollaborationMLInputChannelsRequestListCollaborationMLInputChannelsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCollaborationMLInputChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationMLInputChannels.html#CleanRoomsML.Paginator.ListCollaborationMLInputChannels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listcollaborationmlinputchannelspaginator)
        """

class ListCollaborationTrainedModelExportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationTrainedModelExportJobs.html#CleanRoomsML.Paginator.ListCollaborationTrainedModelExportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listcollaborationtrainedmodelexportjobspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCollaborationTrainedModelExportJobsRequestListCollaborationTrainedModelExportJobsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCollaborationTrainedModelExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationTrainedModelExportJobs.html#CleanRoomsML.Paginator.ListCollaborationTrainedModelExportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listcollaborationtrainedmodelexportjobspaginator)
        """

class ListCollaborationTrainedModelInferenceJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationTrainedModelInferenceJobs.html#CleanRoomsML.Paginator.ListCollaborationTrainedModelInferenceJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listcollaborationtrainedmodelinferencejobspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCollaborationTrainedModelInferenceJobsRequestListCollaborationTrainedModelInferenceJobsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCollaborationTrainedModelInferenceJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationTrainedModelInferenceJobs.html#CleanRoomsML.Paginator.ListCollaborationTrainedModelInferenceJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listcollaborationtrainedmodelinferencejobspaginator)
        """

class ListCollaborationTrainedModelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationTrainedModels.html#CleanRoomsML.Paginator.ListCollaborationTrainedModels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listcollaborationtrainedmodelspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCollaborationTrainedModelsRequestListCollaborationTrainedModelsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCollaborationTrainedModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationTrainedModels.html#CleanRoomsML.Paginator.ListCollaborationTrainedModels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listcollaborationtrainedmodelspaginator)
        """

class ListConfiguredAudienceModelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredAudienceModels.html#CleanRoomsML.Paginator.ListConfiguredAudienceModels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listconfiguredaudiencemodelspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListConfiguredAudienceModelsRequestListConfiguredAudienceModelsPaginateTypeDef
        ],
    ) -> _PageIterator[ListConfiguredAudienceModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredAudienceModels.html#CleanRoomsML.Paginator.ListConfiguredAudienceModels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listconfiguredaudiencemodelspaginator)
        """

class ListConfiguredModelAlgorithmAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredModelAlgorithmAssociations.html#CleanRoomsML.Paginator.ListConfiguredModelAlgorithmAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listconfiguredmodelalgorithmassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListConfiguredModelAlgorithmAssociationsRequestListConfiguredModelAlgorithmAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListConfiguredModelAlgorithmAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredModelAlgorithmAssociations.html#CleanRoomsML.Paginator.ListConfiguredModelAlgorithmAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listconfiguredmodelalgorithmassociationspaginator)
        """

class ListConfiguredModelAlgorithmsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredModelAlgorithms.html#CleanRoomsML.Paginator.ListConfiguredModelAlgorithms)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listconfiguredmodelalgorithmspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListConfiguredModelAlgorithmsRequestListConfiguredModelAlgorithmsPaginateTypeDef
        ],
    ) -> _PageIterator[ListConfiguredModelAlgorithmsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredModelAlgorithms.html#CleanRoomsML.Paginator.ListConfiguredModelAlgorithms.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listconfiguredmodelalgorithmspaginator)
        """

class ListMLInputChannelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListMLInputChannels.html#CleanRoomsML.Paginator.ListMLInputChannels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listmlinputchannelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMLInputChannelsRequestListMLInputChannelsPaginateTypeDef]
    ) -> _PageIterator[ListMLInputChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListMLInputChannels.html#CleanRoomsML.Paginator.ListMLInputChannels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listmlinputchannelspaginator)
        """

class ListTrainedModelInferenceJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainedModelInferenceJobs.html#CleanRoomsML.Paginator.ListTrainedModelInferenceJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listtrainedmodelinferencejobspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListTrainedModelInferenceJobsRequestListTrainedModelInferenceJobsPaginateTypeDef
        ],
    ) -> _PageIterator[ListTrainedModelInferenceJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainedModelInferenceJobs.html#CleanRoomsML.Paginator.ListTrainedModelInferenceJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listtrainedmodelinferencejobspaginator)
        """

class ListTrainedModelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainedModels.html#CleanRoomsML.Paginator.ListTrainedModels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listtrainedmodelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTrainedModelsRequestListTrainedModelsPaginateTypeDef]
    ) -> _PageIterator[ListTrainedModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainedModels.html#CleanRoomsML.Paginator.ListTrainedModels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listtrainedmodelspaginator)
        """

class ListTrainingDatasetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainingDatasets.html#CleanRoomsML.Paginator.ListTrainingDatasets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listtrainingdatasetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTrainingDatasetsRequestListTrainingDatasetsPaginateTypeDef]
    ) -> _PageIterator[ListTrainingDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainingDatasets.html#CleanRoomsML.Paginator.ListTrainingDatasets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/paginators/#listtrainingdatasetspaginator)
        """
