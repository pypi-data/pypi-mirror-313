"""
Type annotations for sagemaker-geospatial service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sagemaker_geospatial.client import SageMakergeospatialcapabilitiesClient

    session = Session()
    client: SageMakergeospatialcapabilitiesClient = session.client("sagemaker-geospatial")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListEarthObservationJobsPaginator,
    ListRasterDataCollectionsPaginator,
    ListVectorEnrichmentJobsPaginator,
)
from .type_defs import (
    DeleteEarthObservationJobInputRequestTypeDef,
    DeleteVectorEnrichmentJobInputRequestTypeDef,
    ExportEarthObservationJobInputRequestTypeDef,
    ExportEarthObservationJobOutputTypeDef,
    ExportVectorEnrichmentJobInputRequestTypeDef,
    ExportVectorEnrichmentJobOutputTypeDef,
    GetEarthObservationJobInputRequestTypeDef,
    GetEarthObservationJobOutputTypeDef,
    GetRasterDataCollectionInputRequestTypeDef,
    GetRasterDataCollectionOutputTypeDef,
    GetTileInputRequestTypeDef,
    GetTileOutputTypeDef,
    GetVectorEnrichmentJobInputRequestTypeDef,
    GetVectorEnrichmentJobOutputTypeDef,
    ListEarthObservationJobInputRequestTypeDef,
    ListEarthObservationJobOutputTypeDef,
    ListRasterDataCollectionsInputRequestTypeDef,
    ListRasterDataCollectionsOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVectorEnrichmentJobInputRequestTypeDef,
    ListVectorEnrichmentJobOutputTypeDef,
    SearchRasterDataCollectionInputRequestTypeDef,
    SearchRasterDataCollectionOutputTypeDef,
    StartEarthObservationJobInputRequestTypeDef,
    StartEarthObservationJobOutputTypeDef,
    StartVectorEnrichmentJobInputRequestTypeDef,
    StartVectorEnrichmentJobOutputTypeDef,
    StopEarthObservationJobInputRequestTypeDef,
    StopVectorEnrichmentJobInputRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("SageMakergeospatialcapabilitiesClient",)

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

class SageMakergeospatialcapabilitiesClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SageMakergeospatialcapabilitiesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#close)
        """

    def delete_earth_observation_job(
        self, **kwargs: Unpack[DeleteEarthObservationJobInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Use this operation to delete an Earth Observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/delete_earth_observation_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#delete_earth_observation_job)
        """

    def delete_vector_enrichment_job(
        self, **kwargs: Unpack[DeleteVectorEnrichmentJobInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Use this operation to delete a Vector Enrichment job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/delete_vector_enrichment_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#delete_vector_enrichment_job)
        """

    def export_earth_observation_job(
        self, **kwargs: Unpack[ExportEarthObservationJobInputRequestTypeDef]
    ) -> ExportEarthObservationJobOutputTypeDef:
        """
        Use this operation to export results of an Earth Observation job and optionally
        source images used as input to the EOJ to an Amazon S3 location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/export_earth_observation_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#export_earth_observation_job)
        """

    def export_vector_enrichment_job(
        self, **kwargs: Unpack[ExportVectorEnrichmentJobInputRequestTypeDef]
    ) -> ExportVectorEnrichmentJobOutputTypeDef:
        """
        Use this operation to copy results of a Vector Enrichment job to an Amazon S3
        location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/export_vector_enrichment_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#export_vector_enrichment_job)
        """

    def get_earth_observation_job(
        self, **kwargs: Unpack[GetEarthObservationJobInputRequestTypeDef]
    ) -> GetEarthObservationJobOutputTypeDef:
        """
        Get the details for a previously initiated Earth Observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_earth_observation_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_earth_observation_job)
        """

    def get_raster_data_collection(
        self, **kwargs: Unpack[GetRasterDataCollectionInputRequestTypeDef]
    ) -> GetRasterDataCollectionOutputTypeDef:
        """
        Use this operation to get details of a specific raster data collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_raster_data_collection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_raster_data_collection)
        """

    def get_tile(self, **kwargs: Unpack[GetTileInputRequestTypeDef]) -> GetTileOutputTypeDef:
        """
        Gets a web mercator tile for the given Earth Observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_tile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_tile)
        """

    def get_vector_enrichment_job(
        self, **kwargs: Unpack[GetVectorEnrichmentJobInputRequestTypeDef]
    ) -> GetVectorEnrichmentJobOutputTypeDef:
        """
        Retrieves details of a Vector Enrichment Job for a given job Amazon Resource
        Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_vector_enrichment_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_vector_enrichment_job)
        """

    def list_earth_observation_jobs(
        self, **kwargs: Unpack[ListEarthObservationJobInputRequestTypeDef]
    ) -> ListEarthObservationJobOutputTypeDef:
        """
        Use this operation to get a list of the Earth Observation jobs associated with
        the calling Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/list_earth_observation_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#list_earth_observation_jobs)
        """

    def list_raster_data_collections(
        self, **kwargs: Unpack[ListRasterDataCollectionsInputRequestTypeDef]
    ) -> ListRasterDataCollectionsOutputTypeDef:
        """
        Use this operation to get raster data collections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/list_raster_data_collections.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#list_raster_data_collections)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags attached to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#list_tags_for_resource)
        """

    def list_vector_enrichment_jobs(
        self, **kwargs: Unpack[ListVectorEnrichmentJobInputRequestTypeDef]
    ) -> ListVectorEnrichmentJobOutputTypeDef:
        """
        Retrieves a list of vector enrichment jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/list_vector_enrichment_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#list_vector_enrichment_jobs)
        """

    def search_raster_data_collection(
        self, **kwargs: Unpack[SearchRasterDataCollectionInputRequestTypeDef]
    ) -> SearchRasterDataCollectionOutputTypeDef:
        """
        Allows you run image query on a specific raster data collection to get a list
        of the satellite imagery matching the selected filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/search_raster_data_collection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#search_raster_data_collection)
        """

    def start_earth_observation_job(
        self, **kwargs: Unpack[StartEarthObservationJobInputRequestTypeDef]
    ) -> StartEarthObservationJobOutputTypeDef:
        """
        Use this operation to create an Earth observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/start_earth_observation_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#start_earth_observation_job)
        """

    def start_vector_enrichment_job(
        self, **kwargs: Unpack[StartVectorEnrichmentJobInputRequestTypeDef]
    ) -> StartVectorEnrichmentJobOutputTypeDef:
        """
        Creates a Vector Enrichment job for the supplied job type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/start_vector_enrichment_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#start_vector_enrichment_job)
        """

    def stop_earth_observation_job(
        self, **kwargs: Unpack[StopEarthObservationJobInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Use this operation to stop an existing earth observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/stop_earth_observation_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#stop_earth_observation_job)
        """

    def stop_vector_enrichment_job(
        self, **kwargs: Unpack[StopVectorEnrichmentJobInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops the Vector Enrichment job for a given job ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/stop_vector_enrichment_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#stop_vector_enrichment_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        The resource you want to tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The resource you want to untag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_earth_observation_jobs"]
    ) -> ListEarthObservationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_raster_data_collections"]
    ) -> ListRasterDataCollectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_vector_enrichment_jobs"]
    ) -> ListVectorEnrichmentJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_paginator)
        """
