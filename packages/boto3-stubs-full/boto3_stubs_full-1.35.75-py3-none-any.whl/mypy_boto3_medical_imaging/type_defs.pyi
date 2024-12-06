"""
Type annotations for medical-imaging service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medical_imaging/type_defs/)

Usage::

    ```python
    from mypy_boto3_medical_imaging.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    DatastoreStatusType,
    ImageSetStateType,
    ImageSetWorkflowStatusType,
    JobStatusType,
    OperatorType,
    SortFieldType,
    SortOrderType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BlobTypeDef",
    "CopyDestinationImageSetPropertiesTypeDef",
    "CopyDestinationImageSetTypeDef",
    "CopyImageSetInformationTypeDef",
    "CopyImageSetRequestRequestTypeDef",
    "CopyImageSetResponseTypeDef",
    "CopySourceImageSetInformationTypeDef",
    "CopySourceImageSetPropertiesTypeDef",
    "CreateDatastoreRequestRequestTypeDef",
    "CreateDatastoreResponseTypeDef",
    "DICOMImportJobPropertiesTypeDef",
    "DICOMImportJobSummaryTypeDef",
    "DICOMStudyDateAndTimeTypeDef",
    "DICOMTagsTypeDef",
    "DICOMUpdatesTypeDef",
    "DatastorePropertiesTypeDef",
    "DatastoreSummaryTypeDef",
    "DeleteDatastoreRequestRequestTypeDef",
    "DeleteDatastoreResponseTypeDef",
    "DeleteImageSetRequestRequestTypeDef",
    "DeleteImageSetResponseTypeDef",
    "GetDICOMImportJobRequestRequestTypeDef",
    "GetDICOMImportJobResponseTypeDef",
    "GetDatastoreRequestRequestTypeDef",
    "GetDatastoreResponseTypeDef",
    "GetImageFrameRequestRequestTypeDef",
    "GetImageFrameResponseTypeDef",
    "GetImageSetMetadataRequestRequestTypeDef",
    "GetImageSetMetadataResponseTypeDef",
    "GetImageSetRequestRequestTypeDef",
    "GetImageSetResponseTypeDef",
    "ImageFrameInformationTypeDef",
    "ImageSetPropertiesTypeDef",
    "ImageSetsMetadataSummaryTypeDef",
    "ListDICOMImportJobsRequestListDICOMImportJobsPaginateTypeDef",
    "ListDICOMImportJobsRequestRequestTypeDef",
    "ListDICOMImportJobsResponseTypeDef",
    "ListDatastoresRequestListDatastoresPaginateTypeDef",
    "ListDatastoresRequestRequestTypeDef",
    "ListDatastoresResponseTypeDef",
    "ListImageSetVersionsRequestListImageSetVersionsPaginateTypeDef",
    "ListImageSetVersionsRequestRequestTypeDef",
    "ListImageSetVersionsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetadataCopiesTypeDef",
    "MetadataUpdatesTypeDef",
    "OverridesTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SearchByAttributeValueTypeDef",
    "SearchCriteriaTypeDef",
    "SearchFilterTypeDef",
    "SearchImageSetsRequestRequestTypeDef",
    "SearchImageSetsRequestSearchImageSetsPaginateTypeDef",
    "SearchImageSetsResponseTypeDef",
    "SortTypeDef",
    "StartDICOMImportJobRequestRequestTypeDef",
    "StartDICOMImportJobResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateImageSetMetadataRequestRequestTypeDef",
    "UpdateImageSetMetadataResponseTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class CopyDestinationImageSetPropertiesTypeDef(TypedDict):
    imageSetId: str
    latestVersionId: str
    imageSetState: NotRequired[ImageSetStateType]
    imageSetWorkflowStatus: NotRequired[ImageSetWorkflowStatusType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    imageSetArn: NotRequired[str]

class CopyDestinationImageSetTypeDef(TypedDict):
    imageSetId: str
    latestVersionId: str

class CopySourceImageSetPropertiesTypeDef(TypedDict):
    imageSetId: str
    latestVersionId: str
    imageSetState: NotRequired[ImageSetStateType]
    imageSetWorkflowStatus: NotRequired[ImageSetWorkflowStatusType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    imageSetArn: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class MetadataCopiesTypeDef(TypedDict):
    copiableAttributes: str

class CreateDatastoreRequestRequestTypeDef(TypedDict):
    clientToken: str
    datastoreName: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    kmsKeyArn: NotRequired[str]

class DICOMImportJobPropertiesTypeDef(TypedDict):
    jobId: str
    jobName: str
    jobStatus: JobStatusType
    datastoreId: str
    dataAccessRoleArn: str
    inputS3Uri: str
    outputS3Uri: str
    endedAt: NotRequired[datetime]
    submittedAt: NotRequired[datetime]
    message: NotRequired[str]

class DICOMImportJobSummaryTypeDef(TypedDict):
    jobId: str
    jobName: str
    jobStatus: JobStatusType
    datastoreId: str
    dataAccessRoleArn: NotRequired[str]
    endedAt: NotRequired[datetime]
    submittedAt: NotRequired[datetime]
    message: NotRequired[str]

class DICOMStudyDateAndTimeTypeDef(TypedDict):
    DICOMStudyDate: str
    DICOMStudyTime: NotRequired[str]

class DICOMTagsTypeDef(TypedDict):
    DICOMPatientId: NotRequired[str]
    DICOMPatientName: NotRequired[str]
    DICOMPatientBirthDate: NotRequired[str]
    DICOMPatientSex: NotRequired[str]
    DICOMStudyInstanceUID: NotRequired[str]
    DICOMStudyId: NotRequired[str]
    DICOMStudyDescription: NotRequired[str]
    DICOMNumberOfStudyRelatedSeries: NotRequired[int]
    DICOMNumberOfStudyRelatedInstances: NotRequired[int]
    DICOMAccessionNumber: NotRequired[str]
    DICOMSeriesInstanceUID: NotRequired[str]
    DICOMSeriesModality: NotRequired[str]
    DICOMSeriesBodyPart: NotRequired[str]
    DICOMSeriesNumber: NotRequired[int]
    DICOMStudyDate: NotRequired[str]
    DICOMStudyTime: NotRequired[str]

class DatastorePropertiesTypeDef(TypedDict):
    datastoreId: str
    datastoreName: str
    datastoreStatus: DatastoreStatusType
    kmsKeyArn: NotRequired[str]
    datastoreArn: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class DatastoreSummaryTypeDef(TypedDict):
    datastoreId: str
    datastoreName: str
    datastoreStatus: DatastoreStatusType
    datastoreArn: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class DeleteDatastoreRequestRequestTypeDef(TypedDict):
    datastoreId: str

class DeleteImageSetRequestRequestTypeDef(TypedDict):
    datastoreId: str
    imageSetId: str

class GetDICOMImportJobRequestRequestTypeDef(TypedDict):
    datastoreId: str
    jobId: str

class GetDatastoreRequestRequestTypeDef(TypedDict):
    datastoreId: str

class ImageFrameInformationTypeDef(TypedDict):
    imageFrameId: str

class GetImageSetMetadataRequestRequestTypeDef(TypedDict):
    datastoreId: str
    imageSetId: str
    versionId: NotRequired[str]

class GetImageSetRequestRequestTypeDef(TypedDict):
    datastoreId: str
    imageSetId: str
    versionId: NotRequired[str]

class OverridesTypeDef(TypedDict):
    forced: NotRequired[bool]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListDICOMImportJobsRequestRequestTypeDef(TypedDict):
    datastoreId: str
    jobStatus: NotRequired[JobStatusType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDatastoresRequestRequestTypeDef(TypedDict):
    datastoreStatus: NotRequired[DatastoreStatusType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListImageSetVersionsRequestRequestTypeDef(TypedDict):
    datastoreId: str
    imageSetId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

TimestampTypeDef = Union[datetime, str]

class SortTypeDef(TypedDict):
    sortOrder: SortOrderType
    sortField: SortFieldType

class StartDICOMImportJobRequestRequestTypeDef(TypedDict):
    dataAccessRoleArn: str
    clientToken: str
    datastoreId: str
    inputS3Uri: str
    outputS3Uri: str
    jobName: NotRequired[str]
    inputOwnerAccountId: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class DICOMUpdatesTypeDef(TypedDict):
    removableAttributes: NotRequired[BlobTypeDef]
    updatableAttributes: NotRequired[BlobTypeDef]

class CopyImageSetResponseTypeDef(TypedDict):
    datastoreId: str
    sourceImageSetProperties: CopySourceImageSetPropertiesTypeDef
    destinationImageSetProperties: CopyDestinationImageSetPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDatastoreResponseTypeDef(TypedDict):
    datastoreId: str
    datastoreStatus: DatastoreStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDatastoreResponseTypeDef(TypedDict):
    datastoreId: str
    datastoreStatus: DatastoreStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteImageSetResponseTypeDef(TypedDict):
    datastoreId: str
    imageSetId: str
    imageSetState: ImageSetStateType
    imageSetWorkflowStatus: ImageSetWorkflowStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class GetImageFrameResponseTypeDef(TypedDict):
    imageFrameBlob: StreamingBody
    contentType: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetImageSetMetadataResponseTypeDef(TypedDict):
    imageSetMetadataBlob: StreamingBody
    contentType: str
    contentEncoding: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartDICOMImportJobResponseTypeDef(TypedDict):
    datastoreId: str
    jobId: str
    jobStatus: JobStatusType
    submittedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateImageSetMetadataResponseTypeDef(TypedDict):
    datastoreId: str
    imageSetId: str
    latestVersionId: str
    imageSetState: ImageSetStateType
    imageSetWorkflowStatus: ImageSetWorkflowStatusType
    createdAt: datetime
    updatedAt: datetime
    message: str
    ResponseMetadata: ResponseMetadataTypeDef

class CopySourceImageSetInformationTypeDef(TypedDict):
    latestVersionId: str
    DICOMCopies: NotRequired[MetadataCopiesTypeDef]

class GetDICOMImportJobResponseTypeDef(TypedDict):
    jobProperties: DICOMImportJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDICOMImportJobsResponseTypeDef(TypedDict):
    jobSummaries: List[DICOMImportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ImageSetsMetadataSummaryTypeDef(TypedDict):
    imageSetId: str
    version: NotRequired[int]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    DICOMTags: NotRequired[DICOMTagsTypeDef]

class GetDatastoreResponseTypeDef(TypedDict):
    datastoreProperties: DatastorePropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDatastoresResponseTypeDef(TypedDict):
    datastoreSummaries: List[DatastoreSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetImageFrameRequestRequestTypeDef(TypedDict):
    datastoreId: str
    imageSetId: str
    imageFrameInformation: ImageFrameInformationTypeDef

class GetImageSetResponseTypeDef(TypedDict):
    datastoreId: str
    imageSetId: str
    versionId: str
    imageSetState: ImageSetStateType
    imageSetWorkflowStatus: ImageSetWorkflowStatusType
    createdAt: datetime
    updatedAt: datetime
    deletedAt: datetime
    message: str
    imageSetArn: str
    overrides: OverridesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ImageSetPropertiesTypeDef(TypedDict):
    imageSetId: str
    versionId: str
    imageSetState: ImageSetStateType
    ImageSetWorkflowStatus: NotRequired[ImageSetWorkflowStatusType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    deletedAt: NotRequired[datetime]
    message: NotRequired[str]
    overrides: NotRequired[OverridesTypeDef]

class ListDICOMImportJobsRequestListDICOMImportJobsPaginateTypeDef(TypedDict):
    datastoreId: str
    jobStatus: NotRequired[JobStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDatastoresRequestListDatastoresPaginateTypeDef(TypedDict):
    datastoreStatus: NotRequired[DatastoreStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListImageSetVersionsRequestListImageSetVersionsPaginateTypeDef(TypedDict):
    datastoreId: str
    imageSetId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchByAttributeValueTypeDef(TypedDict):
    DICOMPatientId: NotRequired[str]
    DICOMAccessionNumber: NotRequired[str]
    DICOMStudyId: NotRequired[str]
    DICOMStudyInstanceUID: NotRequired[str]
    DICOMSeriesInstanceUID: NotRequired[str]
    createdAt: NotRequired[TimestampTypeDef]
    updatedAt: NotRequired[TimestampTypeDef]
    DICOMStudyDateAndTime: NotRequired[DICOMStudyDateAndTimeTypeDef]

class MetadataUpdatesTypeDef(TypedDict):
    DICOMUpdates: NotRequired[DICOMUpdatesTypeDef]
    revertToVersionId: NotRequired[str]

class CopyImageSetInformationTypeDef(TypedDict):
    sourceImageSet: CopySourceImageSetInformationTypeDef
    destinationImageSet: NotRequired[CopyDestinationImageSetTypeDef]

class SearchImageSetsResponseTypeDef(TypedDict):
    imageSetsMetadataSummaries: List[ImageSetsMetadataSummaryTypeDef]
    sort: SortTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListImageSetVersionsResponseTypeDef(TypedDict):
    imageSetPropertiesList: List[ImageSetPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

SearchFilterTypeDef = TypedDict(
    "SearchFilterTypeDef",
    {
        "values": Sequence[SearchByAttributeValueTypeDef],
        "operator": OperatorType,
    },
)

class UpdateImageSetMetadataRequestRequestTypeDef(TypedDict):
    datastoreId: str
    imageSetId: str
    latestVersionId: str
    updateImageSetMetadataUpdates: MetadataUpdatesTypeDef
    force: NotRequired[bool]

class CopyImageSetRequestRequestTypeDef(TypedDict):
    datastoreId: str
    sourceImageSetId: str
    copyImageSetInformation: CopyImageSetInformationTypeDef
    force: NotRequired[bool]

class SearchCriteriaTypeDef(TypedDict):
    filters: NotRequired[Sequence[SearchFilterTypeDef]]
    sort: NotRequired[SortTypeDef]

class SearchImageSetsRequestRequestTypeDef(TypedDict):
    datastoreId: str
    searchCriteria: NotRequired[SearchCriteriaTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class SearchImageSetsRequestSearchImageSetsPaginateTypeDef(TypedDict):
    datastoreId: str
    searchCriteria: NotRequired[SearchCriteriaTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]
