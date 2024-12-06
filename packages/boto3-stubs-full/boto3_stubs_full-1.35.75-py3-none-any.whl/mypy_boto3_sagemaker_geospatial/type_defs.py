"""
Type annotations for sagemaker-geospatial service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/type_defs/)

Usage::

    ```python
    from mypy_boto3_sagemaker_geospatial.type_defs import MultiPolygonGeometryInputOutputTypeDef

    data: MultiPolygonGeometryInputOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AlgorithmNameGeoMosaicType,
    AlgorithmNameResamplingType,
    ComparisonOperatorType,
    DataCollectionTypeType,
    EarthObservationJobErrorTypeType,
    EarthObservationJobExportStatusType,
    EarthObservationJobStatusType,
    ExportErrorTypeType,
    GroupByType,
    OutputTypeType,
    PredefinedResolutionType,
    SortOrderType,
    TargetOptionsType,
    TemporalStatisticsType,
    VectorEnrichmentJobErrorTypeType,
    VectorEnrichmentJobExportErrorTypeType,
    VectorEnrichmentJobExportStatusType,
    VectorEnrichmentJobStatusType,
    VectorEnrichmentJobTypeType,
    ZonalStatisticsType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AreaOfInterestGeometryOutputTypeDef",
    "AreaOfInterestGeometryTypeDef",
    "AreaOfInterestGeometryUnionTypeDef",
    "AreaOfInterestOutputTypeDef",
    "AreaOfInterestTypeDef",
    "AreaOfInterestUnionTypeDef",
    "AssetValueTypeDef",
    "BandMathConfigInputOutputTypeDef",
    "BandMathConfigInputTypeDef",
    "BandMathConfigInputUnionTypeDef",
    "CloudRemovalConfigInputOutputTypeDef",
    "CloudRemovalConfigInputTypeDef",
    "CloudRemovalConfigInputUnionTypeDef",
    "CustomIndicesInputOutputTypeDef",
    "CustomIndicesInputTypeDef",
    "CustomIndicesInputUnionTypeDef",
    "DeleteEarthObservationJobInputRequestTypeDef",
    "DeleteVectorEnrichmentJobInputRequestTypeDef",
    "EarthObservationJobErrorDetailsTypeDef",
    "EoCloudCoverInputTypeDef",
    "ExportEarthObservationJobInputRequestTypeDef",
    "ExportEarthObservationJobOutputTypeDef",
    "ExportErrorDetailsOutputTypeDef",
    "ExportErrorDetailsTypeDef",
    "ExportS3DataInputTypeDef",
    "ExportVectorEnrichmentJobInputRequestTypeDef",
    "ExportVectorEnrichmentJobOutputConfigTypeDef",
    "ExportVectorEnrichmentJobOutputTypeDef",
    "FilterTypeDef",
    "GeoMosaicConfigInputOutputTypeDef",
    "GeoMosaicConfigInputTypeDef",
    "GeoMosaicConfigInputUnionTypeDef",
    "GeometryTypeDef",
    "GetEarthObservationJobInputRequestTypeDef",
    "GetEarthObservationJobOutputTypeDef",
    "GetRasterDataCollectionInputRequestTypeDef",
    "GetRasterDataCollectionOutputTypeDef",
    "GetTileInputRequestTypeDef",
    "GetTileOutputTypeDef",
    "GetVectorEnrichmentJobInputRequestTypeDef",
    "GetVectorEnrichmentJobOutputTypeDef",
    "InputConfigInputTypeDef",
    "InputConfigOutputTypeDef",
    "ItemSourceTypeDef",
    "JobConfigInputOutputTypeDef",
    "JobConfigInputTypeDef",
    "LandsatCloudCoverLandInputTypeDef",
    "ListEarthObservationJobInputListEarthObservationJobsPaginateTypeDef",
    "ListEarthObservationJobInputRequestTypeDef",
    "ListEarthObservationJobOutputConfigTypeDef",
    "ListEarthObservationJobOutputTypeDef",
    "ListRasterDataCollectionsInputListRasterDataCollectionsPaginateTypeDef",
    "ListRasterDataCollectionsInputRequestTypeDef",
    "ListRasterDataCollectionsOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListVectorEnrichmentJobInputListVectorEnrichmentJobsPaginateTypeDef",
    "ListVectorEnrichmentJobInputRequestTypeDef",
    "ListVectorEnrichmentJobOutputConfigTypeDef",
    "ListVectorEnrichmentJobOutputTypeDef",
    "MapMatchingConfigTypeDef",
    "MultiPolygonGeometryInputOutputTypeDef",
    "MultiPolygonGeometryInputTypeDef",
    "MultiPolygonGeometryInputUnionTypeDef",
    "OperationTypeDef",
    "OutputBandTypeDef",
    "OutputConfigInputTypeDef",
    "OutputResolutionResamplingInputTypeDef",
    "OutputResolutionStackInputTypeDef",
    "PaginatorConfigTypeDef",
    "PlatformInputTypeDef",
    "PolygonGeometryInputOutputTypeDef",
    "PolygonGeometryInputTypeDef",
    "PolygonGeometryInputUnionTypeDef",
    "PropertiesTypeDef",
    "PropertyFilterTypeDef",
    "PropertyFiltersOutputTypeDef",
    "PropertyFiltersTypeDef",
    "PropertyFiltersUnionTypeDef",
    "PropertyTypeDef",
    "RasterDataCollectionMetadataTypeDef",
    "RasterDataCollectionQueryInputTypeDef",
    "RasterDataCollectionQueryOutputTypeDef",
    "RasterDataCollectionQueryWithBandFilterInputTypeDef",
    "ResamplingConfigInputOutputTypeDef",
    "ResamplingConfigInputTypeDef",
    "ResamplingConfigInputUnionTypeDef",
    "ResponseMetadataTypeDef",
    "ReverseGeocodingConfigTypeDef",
    "SearchRasterDataCollectionInputRequestTypeDef",
    "SearchRasterDataCollectionOutputTypeDef",
    "StackConfigInputOutputTypeDef",
    "StackConfigInputTypeDef",
    "StackConfigInputUnionTypeDef",
    "StartEarthObservationJobInputRequestTypeDef",
    "StartEarthObservationJobOutputTypeDef",
    "StartVectorEnrichmentJobInputRequestTypeDef",
    "StartVectorEnrichmentJobOutputTypeDef",
    "StopEarthObservationJobInputRequestTypeDef",
    "StopVectorEnrichmentJobInputRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TemporalStatisticsConfigInputOutputTypeDef",
    "TemporalStatisticsConfigInputTypeDef",
    "TemporalStatisticsConfigInputUnionTypeDef",
    "TimeRangeFilterInputTypeDef",
    "TimeRangeFilterOutputTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UserDefinedTypeDef",
    "VectorEnrichmentJobConfigTypeDef",
    "VectorEnrichmentJobDataSourceConfigInputTypeDef",
    "VectorEnrichmentJobErrorDetailsTypeDef",
    "VectorEnrichmentJobExportErrorDetailsTypeDef",
    "VectorEnrichmentJobInputConfigTypeDef",
    "VectorEnrichmentJobS3DataTypeDef",
    "ViewOffNadirInputTypeDef",
    "ViewSunAzimuthInputTypeDef",
    "ViewSunElevationInputTypeDef",
    "ZonalStatisticsConfigInputOutputTypeDef",
    "ZonalStatisticsConfigInputTypeDef",
    "ZonalStatisticsConfigInputUnionTypeDef",
)


class MultiPolygonGeometryInputOutputTypeDef(TypedDict):
    Coordinates: List[List[List[List[float]]]]


class PolygonGeometryInputOutputTypeDef(TypedDict):
    Coordinates: List[List[List[float]]]


class AssetValueTypeDef(TypedDict):
    Href: NotRequired[str]


class CloudRemovalConfigInputOutputTypeDef(TypedDict):
    AlgorithmName: NotRequired[Literal["INTERPOLATION"]]
    InterpolationValue: NotRequired[str]
    TargetBands: NotRequired[List[str]]


class CloudRemovalConfigInputTypeDef(TypedDict):
    AlgorithmName: NotRequired[Literal["INTERPOLATION"]]
    InterpolationValue: NotRequired[str]
    TargetBands: NotRequired[Sequence[str]]


class OperationTypeDef(TypedDict):
    Equation: str
    Name: str
    OutputType: NotRequired[OutputTypeType]


class DeleteEarthObservationJobInputRequestTypeDef(TypedDict):
    Arn: str


class DeleteVectorEnrichmentJobInputRequestTypeDef(TypedDict):
    Arn: str


EarthObservationJobErrorDetailsTypeDef = TypedDict(
    "EarthObservationJobErrorDetailsTypeDef",
    {
        "Message": NotRequired[str],
        "Type": NotRequired[EarthObservationJobErrorTypeType],
    },
)


class EoCloudCoverInputTypeDef(TypedDict):
    LowerBound: float
    UpperBound: float


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


ExportErrorDetailsOutputTypeDef = TypedDict(
    "ExportErrorDetailsOutputTypeDef",
    {
        "Message": NotRequired[str],
        "Type": NotRequired[ExportErrorTypeType],
    },
)


class ExportS3DataInputTypeDef(TypedDict):
    S3Uri: str
    KmsKeyId: NotRequired[str]


class VectorEnrichmentJobS3DataTypeDef(TypedDict):
    S3Uri: str
    KmsKeyId: NotRequired[str]


FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Type": str,
        "Maximum": NotRequired[float],
        "Minimum": NotRequired[float],
    },
)


class GeoMosaicConfigInputOutputTypeDef(TypedDict):
    AlgorithmName: NotRequired[AlgorithmNameGeoMosaicType]
    TargetBands: NotRequired[List[str]]


class GeoMosaicConfigInputTypeDef(TypedDict):
    AlgorithmName: NotRequired[AlgorithmNameGeoMosaicType]
    TargetBands: NotRequired[Sequence[str]]


GeometryTypeDef = TypedDict(
    "GeometryTypeDef",
    {
        "Coordinates": List[List[List[float]]],
        "Type": str,
    },
)


class GetEarthObservationJobInputRequestTypeDef(TypedDict):
    Arn: str


class OutputBandTypeDef(TypedDict):
    BandName: str
    OutputDataType: OutputTypeType


class GetRasterDataCollectionInputRequestTypeDef(TypedDict):
    Arn: str


class GetTileInputRequestTypeDef(TypedDict):
    Arn: str
    ImageAssets: Sequence[str]
    Target: TargetOptionsType
    x: int
    y: int
    z: int
    ExecutionRoleArn: NotRequired[str]
    ImageMask: NotRequired[bool]
    OutputDataType: NotRequired[OutputTypeType]
    OutputFormat: NotRequired[str]
    PropertyFilters: NotRequired[str]
    TimeRangeFilter: NotRequired[str]


class GetVectorEnrichmentJobInputRequestTypeDef(TypedDict):
    Arn: str


class VectorEnrichmentJobErrorDetailsTypeDef(TypedDict):
    ErrorMessage: NotRequired[str]
    ErrorType: NotRequired[VectorEnrichmentJobErrorTypeType]


VectorEnrichmentJobExportErrorDetailsTypeDef = TypedDict(
    "VectorEnrichmentJobExportErrorDetailsTypeDef",
    {
        "Message": NotRequired[str],
        "Type": NotRequired[VectorEnrichmentJobExportErrorTypeType],
    },
)


class PropertiesTypeDef(TypedDict):
    EoCloudCover: NotRequired[float]
    LandsatCloudCoverLand: NotRequired[float]
    Platform: NotRequired[str]
    ViewOffNadir: NotRequired[float]
    ViewSunAzimuth: NotRequired[float]
    ViewSunElevation: NotRequired[float]


class TemporalStatisticsConfigInputOutputTypeDef(TypedDict):
    Statistics: List[TemporalStatisticsType]
    GroupBy: NotRequired[GroupByType]
    TargetBands: NotRequired[List[str]]


class ZonalStatisticsConfigInputOutputTypeDef(TypedDict):
    Statistics: List[ZonalStatisticsType]
    ZoneS3Path: str
    TargetBands: NotRequired[List[str]]
    ZoneS3PathKmsKeyId: NotRequired[str]


class LandsatCloudCoverLandInputTypeDef(TypedDict):
    LowerBound: float
    UpperBound: float


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListEarthObservationJobInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SortBy: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    StatusEquals: NotRequired[EarthObservationJobStatusType]


class ListEarthObservationJobOutputConfigTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    DurationInSeconds: int
    Name: str
    OperationType: str
    Status: EarthObservationJobStatusType
    Tags: NotRequired[Dict[str, str]]


class ListRasterDataCollectionsInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class ListVectorEnrichmentJobInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SortBy: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    StatusEquals: NotRequired[str]


ListVectorEnrichmentJobOutputConfigTypeDef = TypedDict(
    "ListVectorEnrichmentJobOutputConfigTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "Name": str,
        "Status": VectorEnrichmentJobStatusType,
        "Type": VectorEnrichmentJobTypeType,
        "Tags": NotRequired[Dict[str, str]],
    },
)


class MapMatchingConfigTypeDef(TypedDict):
    IdAttributeName: str
    TimestampAttributeName: str
    XAttributeName: str
    YAttributeName: str


class MultiPolygonGeometryInputTypeDef(TypedDict):
    Coordinates: Sequence[Sequence[Sequence[Sequence[float]]]]


class UserDefinedTypeDef(TypedDict):
    Unit: Literal["METERS"]
    Value: float


class PlatformInputTypeDef(TypedDict):
    Value: str
    ComparisonOperator: NotRequired[ComparisonOperatorType]


class PolygonGeometryInputTypeDef(TypedDict):
    Coordinates: Sequence[Sequence[Sequence[float]]]


class ViewOffNadirInputTypeDef(TypedDict):
    LowerBound: float
    UpperBound: float


class ViewSunAzimuthInputTypeDef(TypedDict):
    LowerBound: float
    UpperBound: float


class ViewSunElevationInputTypeDef(TypedDict):
    LowerBound: float
    UpperBound: float


class TimeRangeFilterOutputTypeDef(TypedDict):
    EndTime: datetime
    StartTime: datetime


class ReverseGeocodingConfigTypeDef(TypedDict):
    XAttributeName: str
    YAttributeName: str


class StopEarthObservationJobInputRequestTypeDef(TypedDict):
    Arn: str


class StopVectorEnrichmentJobInputRequestTypeDef(TypedDict):
    Arn: str


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class TemporalStatisticsConfigInputTypeDef(TypedDict):
    Statistics: Sequence[TemporalStatisticsType]
    GroupBy: NotRequired[GroupByType]
    TargetBands: NotRequired[Sequence[str]]


TimestampTypeDef = Union[datetime, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class ZonalStatisticsConfigInputTypeDef(TypedDict):
    Statistics: Sequence[ZonalStatisticsType]
    ZoneS3Path: str
    TargetBands: NotRequired[Sequence[str]]
    ZoneS3PathKmsKeyId: NotRequired[str]


class AreaOfInterestGeometryOutputTypeDef(TypedDict):
    MultiPolygonGeometry: NotRequired[MultiPolygonGeometryInputOutputTypeDef]
    PolygonGeometry: NotRequired[PolygonGeometryInputOutputTypeDef]


CloudRemovalConfigInputUnionTypeDef = Union[
    CloudRemovalConfigInputTypeDef, CloudRemovalConfigInputOutputTypeDef
]


class CustomIndicesInputOutputTypeDef(TypedDict):
    Operations: NotRequired[List[OperationTypeDef]]


class CustomIndicesInputTypeDef(TypedDict):
    Operations: NotRequired[Sequence[OperationTypeDef]]


class GetTileOutputTypeDef(TypedDict):
    BinaryFile: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ExportErrorDetailsTypeDef(TypedDict):
    ExportResults: NotRequired[ExportErrorDetailsOutputTypeDef]
    ExportSourceImages: NotRequired[ExportErrorDetailsOutputTypeDef]


class OutputConfigInputTypeDef(TypedDict):
    S3Data: ExportS3DataInputTypeDef


class ExportVectorEnrichmentJobOutputConfigTypeDef(TypedDict):
    S3Data: VectorEnrichmentJobS3DataTypeDef


class VectorEnrichmentJobDataSourceConfigInputTypeDef(TypedDict):
    S3Data: NotRequired[VectorEnrichmentJobS3DataTypeDef]


GetRasterDataCollectionOutputTypeDef = TypedDict(
    "GetRasterDataCollectionOutputTypeDef",
    {
        "Arn": str,
        "Description": str,
        "DescriptionPageUrl": str,
        "ImageSourceBands": List[str],
        "Name": str,
        "SupportedFilters": List[FilterTypeDef],
        "Tags": Dict[str, str],
        "Type": DataCollectionTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RasterDataCollectionMetadataTypeDef = TypedDict(
    "RasterDataCollectionMetadataTypeDef",
    {
        "Arn": str,
        "Description": str,
        "Name": str,
        "SupportedFilters": List[FilterTypeDef],
        "Type": DataCollectionTypeType,
        "DescriptionPageUrl": NotRequired[str],
        "Tags": NotRequired[Dict[str, str]],
    },
)
GeoMosaicConfigInputUnionTypeDef = Union[
    GeoMosaicConfigInputTypeDef, GeoMosaicConfigInputOutputTypeDef
]


class ItemSourceTypeDef(TypedDict):
    DateTime: datetime
    Geometry: GeometryTypeDef
    Id: str
    Assets: NotRequired[Dict[str, AssetValueTypeDef]]
    Properties: NotRequired[PropertiesTypeDef]


class ListEarthObservationJobInputListEarthObservationJobsPaginateTypeDef(TypedDict):
    SortBy: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    StatusEquals: NotRequired[EarthObservationJobStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRasterDataCollectionsInputListRasterDataCollectionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVectorEnrichmentJobInputListVectorEnrichmentJobsPaginateTypeDef(TypedDict):
    SortBy: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    StatusEquals: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEarthObservationJobOutputTypeDef(TypedDict):
    EarthObservationJobSummaries: List[ListEarthObservationJobOutputConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListVectorEnrichmentJobOutputTypeDef(TypedDict):
    VectorEnrichmentJobSummaries: List[ListVectorEnrichmentJobOutputConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


MultiPolygonGeometryInputUnionTypeDef = Union[
    MultiPolygonGeometryInputTypeDef, MultiPolygonGeometryInputOutputTypeDef
]


class OutputResolutionResamplingInputTypeDef(TypedDict):
    UserDefined: UserDefinedTypeDef


class OutputResolutionStackInputTypeDef(TypedDict):
    Predefined: NotRequired[PredefinedResolutionType]
    UserDefined: NotRequired[UserDefinedTypeDef]


PolygonGeometryInputUnionTypeDef = Union[
    PolygonGeometryInputTypeDef, PolygonGeometryInputOutputTypeDef
]


class PropertyTypeDef(TypedDict):
    EoCloudCover: NotRequired[EoCloudCoverInputTypeDef]
    LandsatCloudCoverLand: NotRequired[LandsatCloudCoverLandInputTypeDef]
    Platform: NotRequired[PlatformInputTypeDef]
    ViewOffNadir: NotRequired[ViewOffNadirInputTypeDef]
    ViewSunAzimuth: NotRequired[ViewSunAzimuthInputTypeDef]
    ViewSunElevation: NotRequired[ViewSunElevationInputTypeDef]


class VectorEnrichmentJobConfigTypeDef(TypedDict):
    MapMatchingConfig: NotRequired[MapMatchingConfigTypeDef]
    ReverseGeocodingConfig: NotRequired[ReverseGeocodingConfigTypeDef]


TemporalStatisticsConfigInputUnionTypeDef = Union[
    TemporalStatisticsConfigInputTypeDef, TemporalStatisticsConfigInputOutputTypeDef
]


class TimeRangeFilterInputTypeDef(TypedDict):
    EndTime: TimestampTypeDef
    StartTime: TimestampTypeDef


ZonalStatisticsConfigInputUnionTypeDef = Union[
    ZonalStatisticsConfigInputTypeDef, ZonalStatisticsConfigInputOutputTypeDef
]


class AreaOfInterestOutputTypeDef(TypedDict):
    AreaOfInterestGeometry: NotRequired[AreaOfInterestGeometryOutputTypeDef]


class BandMathConfigInputOutputTypeDef(TypedDict):
    CustomIndices: NotRequired[CustomIndicesInputOutputTypeDef]
    PredefinedIndices: NotRequired[List[str]]


CustomIndicesInputUnionTypeDef = Union[CustomIndicesInputTypeDef, CustomIndicesInputOutputTypeDef]


class ExportEarthObservationJobInputRequestTypeDef(TypedDict):
    Arn: str
    ExecutionRoleArn: str
    OutputConfig: OutputConfigInputTypeDef
    ClientToken: NotRequired[str]
    ExportSourceImages: NotRequired[bool]


class ExportEarthObservationJobOutputTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    ExecutionRoleArn: str
    ExportSourceImages: bool
    ExportStatus: EarthObservationJobExportStatusType
    OutputConfig: OutputConfigInputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ExportVectorEnrichmentJobInputRequestTypeDef(TypedDict):
    Arn: str
    ExecutionRoleArn: str
    OutputConfig: ExportVectorEnrichmentJobOutputConfigTypeDef
    ClientToken: NotRequired[str]


class ExportVectorEnrichmentJobOutputTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    ExecutionRoleArn: str
    ExportStatus: VectorEnrichmentJobExportStatusType
    OutputConfig: ExportVectorEnrichmentJobOutputConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class VectorEnrichmentJobInputConfigTypeDef(TypedDict):
    DataSourceConfig: VectorEnrichmentJobDataSourceConfigInputTypeDef
    DocumentType: Literal["CSV"]


class ListRasterDataCollectionsOutputTypeDef(TypedDict):
    RasterDataCollectionSummaries: List[RasterDataCollectionMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchRasterDataCollectionOutputTypeDef(TypedDict):
    ApproximateResultCount: int
    Items: List[ItemSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ResamplingConfigInputOutputTypeDef(TypedDict):
    OutputResolution: OutputResolutionResamplingInputTypeDef
    AlgorithmName: NotRequired[AlgorithmNameResamplingType]
    TargetBands: NotRequired[List[str]]


class ResamplingConfigInputTypeDef(TypedDict):
    OutputResolution: OutputResolutionResamplingInputTypeDef
    AlgorithmName: NotRequired[AlgorithmNameResamplingType]
    TargetBands: NotRequired[Sequence[str]]


class StackConfigInputOutputTypeDef(TypedDict):
    OutputResolution: NotRequired[OutputResolutionStackInputTypeDef]
    TargetBands: NotRequired[List[str]]


class StackConfigInputTypeDef(TypedDict):
    OutputResolution: NotRequired[OutputResolutionStackInputTypeDef]
    TargetBands: NotRequired[Sequence[str]]


class AreaOfInterestGeometryTypeDef(TypedDict):
    MultiPolygonGeometry: NotRequired[MultiPolygonGeometryInputUnionTypeDef]
    PolygonGeometry: NotRequired[PolygonGeometryInputUnionTypeDef]


class PropertyFilterTypeDef(TypedDict):
    Property: PropertyTypeDef


class BandMathConfigInputTypeDef(TypedDict):
    CustomIndices: NotRequired[CustomIndicesInputUnionTypeDef]
    PredefinedIndices: NotRequired[Sequence[str]]


GetVectorEnrichmentJobOutputTypeDef = TypedDict(
    "GetVectorEnrichmentJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "ErrorDetails": VectorEnrichmentJobErrorDetailsTypeDef,
        "ExecutionRoleArn": str,
        "ExportErrorDetails": VectorEnrichmentJobExportErrorDetailsTypeDef,
        "ExportStatus": VectorEnrichmentJobExportStatusType,
        "InputConfig": VectorEnrichmentJobInputConfigTypeDef,
        "JobConfig": VectorEnrichmentJobConfigTypeDef,
        "KmsKeyId": str,
        "Name": str,
        "Status": VectorEnrichmentJobStatusType,
        "Tags": Dict[str, str],
        "Type": VectorEnrichmentJobTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class StartVectorEnrichmentJobInputRequestTypeDef(TypedDict):
    ExecutionRoleArn: str
    InputConfig: VectorEnrichmentJobInputConfigTypeDef
    JobConfig: VectorEnrichmentJobConfigTypeDef
    Name: str
    ClientToken: NotRequired[str]
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


StartVectorEnrichmentJobOutputTypeDef = TypedDict(
    "StartVectorEnrichmentJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "ExecutionRoleArn": str,
        "InputConfig": VectorEnrichmentJobInputConfigTypeDef,
        "JobConfig": VectorEnrichmentJobConfigTypeDef,
        "KmsKeyId": str,
        "Name": str,
        "Status": VectorEnrichmentJobStatusType,
        "Tags": Dict[str, str],
        "Type": VectorEnrichmentJobTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ResamplingConfigInputUnionTypeDef = Union[
    ResamplingConfigInputTypeDef, ResamplingConfigInputOutputTypeDef
]


class JobConfigInputOutputTypeDef(TypedDict):
    BandMathConfig: NotRequired[BandMathConfigInputOutputTypeDef]
    CloudMaskingConfig: NotRequired[Dict[str, Any]]
    CloudRemovalConfig: NotRequired[CloudRemovalConfigInputOutputTypeDef]
    GeoMosaicConfig: NotRequired[GeoMosaicConfigInputOutputTypeDef]
    LandCoverSegmentationConfig: NotRequired[Dict[str, Any]]
    ResamplingConfig: NotRequired[ResamplingConfigInputOutputTypeDef]
    StackConfig: NotRequired[StackConfigInputOutputTypeDef]
    TemporalStatisticsConfig: NotRequired[TemporalStatisticsConfigInputOutputTypeDef]
    ZonalStatisticsConfig: NotRequired[ZonalStatisticsConfigInputOutputTypeDef]


StackConfigInputUnionTypeDef = Union[StackConfigInputTypeDef, StackConfigInputOutputTypeDef]
AreaOfInterestGeometryUnionTypeDef = Union[
    AreaOfInterestGeometryTypeDef, AreaOfInterestGeometryOutputTypeDef
]


class PropertyFiltersOutputTypeDef(TypedDict):
    LogicalOperator: NotRequired[Literal["AND"]]
    Properties: NotRequired[List[PropertyFilterTypeDef]]


class PropertyFiltersTypeDef(TypedDict):
    LogicalOperator: NotRequired[Literal["AND"]]
    Properties: NotRequired[Sequence[PropertyFilterTypeDef]]


BandMathConfigInputUnionTypeDef = Union[
    BandMathConfigInputTypeDef, BandMathConfigInputOutputTypeDef
]


class AreaOfInterestTypeDef(TypedDict):
    AreaOfInterestGeometry: NotRequired[AreaOfInterestGeometryUnionTypeDef]


class RasterDataCollectionQueryOutputTypeDef(TypedDict):
    RasterDataCollectionArn: str
    RasterDataCollectionName: str
    TimeRangeFilter: TimeRangeFilterOutputTypeDef
    AreaOfInterest: NotRequired[AreaOfInterestOutputTypeDef]
    PropertyFilters: NotRequired[PropertyFiltersOutputTypeDef]


PropertyFiltersUnionTypeDef = Union[PropertyFiltersTypeDef, PropertyFiltersOutputTypeDef]


class JobConfigInputTypeDef(TypedDict):
    BandMathConfig: NotRequired[BandMathConfigInputUnionTypeDef]
    CloudMaskingConfig: NotRequired[Mapping[str, Any]]
    CloudRemovalConfig: NotRequired[CloudRemovalConfigInputUnionTypeDef]
    GeoMosaicConfig: NotRequired[GeoMosaicConfigInputUnionTypeDef]
    LandCoverSegmentationConfig: NotRequired[Mapping[str, Any]]
    ResamplingConfig: NotRequired[ResamplingConfigInputUnionTypeDef]
    StackConfig: NotRequired[StackConfigInputUnionTypeDef]
    TemporalStatisticsConfig: NotRequired[TemporalStatisticsConfigInputUnionTypeDef]
    ZonalStatisticsConfig: NotRequired[ZonalStatisticsConfigInputUnionTypeDef]


AreaOfInterestUnionTypeDef = Union[AreaOfInterestTypeDef, AreaOfInterestOutputTypeDef]


class InputConfigOutputTypeDef(TypedDict):
    PreviousEarthObservationJobArn: NotRequired[str]
    RasterDataCollectionQuery: NotRequired[RasterDataCollectionQueryOutputTypeDef]


class RasterDataCollectionQueryInputTypeDef(TypedDict):
    RasterDataCollectionArn: str
    TimeRangeFilter: TimeRangeFilterInputTypeDef
    AreaOfInterest: NotRequired[AreaOfInterestUnionTypeDef]
    PropertyFilters: NotRequired[PropertyFiltersUnionTypeDef]


class RasterDataCollectionQueryWithBandFilterInputTypeDef(TypedDict):
    TimeRangeFilter: TimeRangeFilterInputTypeDef
    AreaOfInterest: NotRequired[AreaOfInterestUnionTypeDef]
    BandFilter: NotRequired[Sequence[str]]
    PropertyFilters: NotRequired[PropertyFiltersUnionTypeDef]


class GetEarthObservationJobOutputTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    DurationInSeconds: int
    ErrorDetails: EarthObservationJobErrorDetailsTypeDef
    ExecutionRoleArn: str
    ExportErrorDetails: ExportErrorDetailsTypeDef
    ExportStatus: EarthObservationJobExportStatusType
    InputConfig: InputConfigOutputTypeDef
    JobConfig: JobConfigInputOutputTypeDef
    KmsKeyId: str
    Name: str
    OutputBands: List[OutputBandTypeDef]
    Status: EarthObservationJobStatusType
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartEarthObservationJobOutputTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    DurationInSeconds: int
    ExecutionRoleArn: str
    InputConfig: InputConfigOutputTypeDef
    JobConfig: JobConfigInputOutputTypeDef
    KmsKeyId: str
    Name: str
    Status: EarthObservationJobStatusType
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class InputConfigInputTypeDef(TypedDict):
    PreviousEarthObservationJobArn: NotRequired[str]
    RasterDataCollectionQuery: NotRequired[RasterDataCollectionQueryInputTypeDef]


class SearchRasterDataCollectionInputRequestTypeDef(TypedDict):
    Arn: str
    RasterDataCollectionQuery: RasterDataCollectionQueryWithBandFilterInputTypeDef
    NextToken: NotRequired[str]


class StartEarthObservationJobInputRequestTypeDef(TypedDict):
    ExecutionRoleArn: str
    InputConfig: InputConfigInputTypeDef
    JobConfig: JobConfigInputTypeDef
    Name: str
    ClientToken: NotRequired[str]
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
