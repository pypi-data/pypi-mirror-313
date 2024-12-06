"""
Type annotations for textract service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/type_defs/)

Usage::

    ```python
    from mypy_boto3_textract.type_defs import AdapterOverviewTypeDef

    data: AdapterOverviewTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AdapterVersionStatusType,
    AutoUpdateType,
    BlockTypeType,
    ContentClassifierType,
    EntityTypeType,
    FeatureTypeType,
    JobStatusType,
    RelationshipTypeType,
    SelectionStatusType,
    TextTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AdapterOverviewTypeDef",
    "AdapterTypeDef",
    "AdapterVersionDatasetConfigTypeDef",
    "AdapterVersionEvaluationMetricTypeDef",
    "AdapterVersionOverviewTypeDef",
    "AdaptersConfigTypeDef",
    "AnalyzeDocumentRequestRequestTypeDef",
    "AnalyzeDocumentResponseTypeDef",
    "AnalyzeExpenseRequestRequestTypeDef",
    "AnalyzeExpenseResponseTypeDef",
    "AnalyzeIDDetectionsTypeDef",
    "AnalyzeIDRequestRequestTypeDef",
    "AnalyzeIDResponseTypeDef",
    "BlobTypeDef",
    "BlockTypeDef",
    "BoundingBoxTypeDef",
    "CreateAdapterRequestRequestTypeDef",
    "CreateAdapterResponseTypeDef",
    "CreateAdapterVersionRequestRequestTypeDef",
    "CreateAdapterVersionResponseTypeDef",
    "DeleteAdapterRequestRequestTypeDef",
    "DeleteAdapterVersionRequestRequestTypeDef",
    "DetectDocumentTextRequestRequestTypeDef",
    "DetectDocumentTextResponseTypeDef",
    "DetectedSignatureTypeDef",
    "DocumentGroupTypeDef",
    "DocumentLocationTypeDef",
    "DocumentMetadataTypeDef",
    "DocumentTypeDef",
    "EvaluationMetricTypeDef",
    "ExpenseCurrencyTypeDef",
    "ExpenseDetectionTypeDef",
    "ExpenseDocumentTypeDef",
    "ExpenseFieldTypeDef",
    "ExpenseGroupPropertyTypeDef",
    "ExpenseTypeTypeDef",
    "ExtractionTypeDef",
    "GeometryTypeDef",
    "GetAdapterRequestRequestTypeDef",
    "GetAdapterResponseTypeDef",
    "GetAdapterVersionRequestRequestTypeDef",
    "GetAdapterVersionResponseTypeDef",
    "GetDocumentAnalysisRequestRequestTypeDef",
    "GetDocumentAnalysisResponseTypeDef",
    "GetDocumentTextDetectionRequestRequestTypeDef",
    "GetDocumentTextDetectionResponseTypeDef",
    "GetExpenseAnalysisRequestRequestTypeDef",
    "GetExpenseAnalysisResponseTypeDef",
    "GetLendingAnalysisRequestRequestTypeDef",
    "GetLendingAnalysisResponseTypeDef",
    "GetLendingAnalysisSummaryRequestRequestTypeDef",
    "GetLendingAnalysisSummaryResponseTypeDef",
    "HumanLoopActivationOutputTypeDef",
    "HumanLoopConfigTypeDef",
    "HumanLoopDataAttributesTypeDef",
    "IdentityDocumentFieldTypeDef",
    "IdentityDocumentTypeDef",
    "LendingDetectionTypeDef",
    "LendingDocumentTypeDef",
    "LendingFieldTypeDef",
    "LendingResultTypeDef",
    "LendingSummaryTypeDef",
    "LineItemFieldsTypeDef",
    "LineItemGroupTypeDef",
    "ListAdapterVersionsRequestListAdapterVersionsPaginateTypeDef",
    "ListAdapterVersionsRequestRequestTypeDef",
    "ListAdapterVersionsResponseTypeDef",
    "ListAdaptersRequestListAdaptersPaginateTypeDef",
    "ListAdaptersRequestRequestTypeDef",
    "ListAdaptersResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NormalizedValueTypeDef",
    "NotificationChannelTypeDef",
    "OutputConfigTypeDef",
    "PageClassificationTypeDef",
    "PaginatorConfigTypeDef",
    "PointTypeDef",
    "PredictionTypeDef",
    "QueriesConfigTypeDef",
    "QueryOutputTypeDef",
    "QueryTypeDef",
    "QueryUnionTypeDef",
    "RelationshipTypeDef",
    "ResponseMetadataTypeDef",
    "S3ObjectTypeDef",
    "SignatureDetectionTypeDef",
    "SplitDocumentTypeDef",
    "StartDocumentAnalysisRequestRequestTypeDef",
    "StartDocumentAnalysisResponseTypeDef",
    "StartDocumentTextDetectionRequestRequestTypeDef",
    "StartDocumentTextDetectionResponseTypeDef",
    "StartExpenseAnalysisRequestRequestTypeDef",
    "StartExpenseAnalysisResponseTypeDef",
    "StartLendingAnalysisRequestRequestTypeDef",
    "StartLendingAnalysisResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "UndetectedSignatureTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAdapterRequestRequestTypeDef",
    "UpdateAdapterResponseTypeDef",
    "WarningTypeDef",
)


class AdapterOverviewTypeDef(TypedDict):
    AdapterId: NotRequired[str]
    AdapterName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    FeatureTypes: NotRequired[List[FeatureTypeType]]


class AdapterTypeDef(TypedDict):
    AdapterId: str
    Version: str
    Pages: NotRequired[Sequence[str]]


class S3ObjectTypeDef(TypedDict):
    Bucket: NotRequired[str]
    Name: NotRequired[str]
    Version: NotRequired[str]


class EvaluationMetricTypeDef(TypedDict):
    F1Score: NotRequired[float]
    Precision: NotRequired[float]
    Recall: NotRequired[float]


class AdapterVersionOverviewTypeDef(TypedDict):
    AdapterId: NotRequired[str]
    AdapterVersion: NotRequired[str]
    CreationTime: NotRequired[datetime]
    FeatureTypes: NotRequired[List[FeatureTypeType]]
    Status: NotRequired[AdapterVersionStatusType]
    StatusMessage: NotRequired[str]


class DocumentMetadataTypeDef(TypedDict):
    Pages: NotRequired[int]


class HumanLoopActivationOutputTypeDef(TypedDict):
    HumanLoopArn: NotRequired[str]
    HumanLoopActivationReasons: NotRequired[List[str]]
    HumanLoopActivationConditionsEvaluationResults: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class NormalizedValueTypeDef(TypedDict):
    Value: NotRequired[str]
    ValueType: NotRequired[Literal["DATE"]]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
QueryOutputTypeDef = TypedDict(
    "QueryOutputTypeDef",
    {
        "Text": str,
        "Alias": NotRequired[str],
        "Pages": NotRequired[List[str]],
    },
)
RelationshipTypeDef = TypedDict(
    "RelationshipTypeDef",
    {
        "Type": NotRequired[RelationshipTypeType],
        "Ids": NotRequired[List[str]],
    },
)


class BoundingBoxTypeDef(TypedDict):
    Width: NotRequired[float]
    Height: NotRequired[float]
    Left: NotRequired[float]
    Top: NotRequired[float]


class CreateAdapterRequestRequestTypeDef(TypedDict):
    AdapterName: str
    FeatureTypes: Sequence[FeatureTypeType]
    ClientRequestToken: NotRequired[str]
    Description: NotRequired[str]
    AutoUpdate: NotRequired[AutoUpdateType]
    Tags: NotRequired[Mapping[str, str]]


class OutputConfigTypeDef(TypedDict):
    S3Bucket: str
    S3Prefix: NotRequired[str]


class DeleteAdapterRequestRequestTypeDef(TypedDict):
    AdapterId: str


class DeleteAdapterVersionRequestRequestTypeDef(TypedDict):
    AdapterId: str
    AdapterVersion: str


class DetectedSignatureTypeDef(TypedDict):
    Page: NotRequired[int]


class SplitDocumentTypeDef(TypedDict):
    Index: NotRequired[int]
    Pages: NotRequired[List[int]]


class UndetectedSignatureTypeDef(TypedDict):
    Page: NotRequired[int]


class ExpenseCurrencyTypeDef(TypedDict):
    Code: NotRequired[str]
    Confidence: NotRequired[float]


class ExpenseGroupPropertyTypeDef(TypedDict):
    Types: NotRequired[List[str]]
    Id: NotRequired[str]


ExpenseTypeTypeDef = TypedDict(
    "ExpenseTypeTypeDef",
    {
        "Text": NotRequired[str],
        "Confidence": NotRequired[float],
    },
)


class PointTypeDef(TypedDict):
    X: NotRequired[float]
    Y: NotRequired[float]


class GetAdapterRequestRequestTypeDef(TypedDict):
    AdapterId: str


class GetAdapterVersionRequestRequestTypeDef(TypedDict):
    AdapterId: str
    AdapterVersion: str


class GetDocumentAnalysisRequestRequestTypeDef(TypedDict):
    JobId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class WarningTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    Pages: NotRequired[List[int]]


class GetDocumentTextDetectionRequestRequestTypeDef(TypedDict):
    JobId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetExpenseAnalysisRequestRequestTypeDef(TypedDict):
    JobId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetLendingAnalysisRequestRequestTypeDef(TypedDict):
    JobId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetLendingAnalysisSummaryRequestRequestTypeDef(TypedDict):
    JobId: str


class HumanLoopDataAttributesTypeDef(TypedDict):
    ContentClassifiers: NotRequired[Sequence[ContentClassifierType]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str


class NotificationChannelTypeDef(TypedDict):
    SNSTopicArn: str
    RoleArn: str


class PredictionTypeDef(TypedDict):
    Value: NotRequired[str]
    Confidence: NotRequired[float]


QueryTypeDef = TypedDict(
    "QueryTypeDef",
    {
        "Text": str,
        "Alias": NotRequired[str],
        "Pages": NotRequired[Sequence[str]],
    },
)


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class UpdateAdapterRequestRequestTypeDef(TypedDict):
    AdapterId: str
    Description: NotRequired[str]
    AdapterName: NotRequired[str]
    AutoUpdate: NotRequired[AutoUpdateType]


class AdaptersConfigTypeDef(TypedDict):
    Adapters: Sequence[AdapterTypeDef]


class AdapterVersionDatasetConfigTypeDef(TypedDict):
    ManifestS3Object: NotRequired[S3ObjectTypeDef]


class DocumentLocationTypeDef(TypedDict):
    S3Object: NotRequired[S3ObjectTypeDef]


class AdapterVersionEvaluationMetricTypeDef(TypedDict):
    Baseline: NotRequired[EvaluationMetricTypeDef]
    AdapterVersion: NotRequired[EvaluationMetricTypeDef]
    FeatureType: NotRequired[FeatureTypeType]


class CreateAdapterResponseTypeDef(TypedDict):
    AdapterId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAdapterVersionResponseTypeDef(TypedDict):
    AdapterId: str
    AdapterVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetAdapterResponseTypeDef(TypedDict):
    AdapterId: str
    AdapterName: str
    CreationTime: datetime
    Description: str
    FeatureTypes: List[FeatureTypeType]
    AutoUpdate: AutoUpdateType
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListAdapterVersionsResponseTypeDef(TypedDict):
    AdapterVersions: List[AdapterVersionOverviewTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAdaptersResponseTypeDef(TypedDict):
    Adapters: List[AdapterOverviewTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartDocumentAnalysisResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartDocumentTextDetectionResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartExpenseAnalysisResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartLendingAnalysisResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAdapterResponseTypeDef(TypedDict):
    AdapterId: str
    AdapterName: str
    CreationTime: datetime
    Description: str
    FeatureTypes: List[FeatureTypeType]
    AutoUpdate: AutoUpdateType
    ResponseMetadata: ResponseMetadataTypeDef


AnalyzeIDDetectionsTypeDef = TypedDict(
    "AnalyzeIDDetectionsTypeDef",
    {
        "Text": str,
        "NormalizedValue": NotRequired[NormalizedValueTypeDef],
        "Confidence": NotRequired[float],
    },
)


class DocumentTypeDef(TypedDict):
    Bytes: NotRequired[BlobTypeDef]
    S3Object: NotRequired[S3ObjectTypeDef]


DocumentGroupTypeDef = TypedDict(
    "DocumentGroupTypeDef",
    {
        "Type": NotRequired[str],
        "SplitDocuments": NotRequired[List[SplitDocumentTypeDef]],
        "DetectedSignatures": NotRequired[List[DetectedSignatureTypeDef]],
        "UndetectedSignatures": NotRequired[List[UndetectedSignatureTypeDef]],
    },
)


class GeometryTypeDef(TypedDict):
    BoundingBox: NotRequired[BoundingBoxTypeDef]
    Polygon: NotRequired[List[PointTypeDef]]


class HumanLoopConfigTypeDef(TypedDict):
    HumanLoopName: str
    FlowDefinitionArn: str
    DataAttributes: NotRequired[HumanLoopDataAttributesTypeDef]


class ListAdapterVersionsRequestListAdapterVersionsPaginateTypeDef(TypedDict):
    AdapterId: NotRequired[str]
    AfterCreationTime: NotRequired[TimestampTypeDef]
    BeforeCreationTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAdapterVersionsRequestRequestTypeDef(TypedDict):
    AdapterId: NotRequired[str]
    AfterCreationTime: NotRequired[TimestampTypeDef]
    BeforeCreationTime: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListAdaptersRequestListAdaptersPaginateTypeDef(TypedDict):
    AfterCreationTime: NotRequired[TimestampTypeDef]
    BeforeCreationTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAdaptersRequestRequestTypeDef(TypedDict):
    AfterCreationTime: NotRequired[TimestampTypeDef]
    BeforeCreationTime: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class PageClassificationTypeDef(TypedDict):
    PageType: List[PredictionTypeDef]
    PageNumber: List[PredictionTypeDef]


QueryUnionTypeDef = Union[QueryTypeDef, QueryOutputTypeDef]


class CreateAdapterVersionRequestRequestTypeDef(TypedDict):
    AdapterId: str
    DatasetConfig: AdapterVersionDatasetConfigTypeDef
    OutputConfig: OutputConfigTypeDef
    ClientRequestToken: NotRequired[str]
    KMSKeyId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class StartDocumentTextDetectionRequestRequestTypeDef(TypedDict):
    DocumentLocation: DocumentLocationTypeDef
    ClientRequestToken: NotRequired[str]
    JobTag: NotRequired[str]
    NotificationChannel: NotRequired[NotificationChannelTypeDef]
    OutputConfig: NotRequired[OutputConfigTypeDef]
    KMSKeyId: NotRequired[str]


class StartExpenseAnalysisRequestRequestTypeDef(TypedDict):
    DocumentLocation: DocumentLocationTypeDef
    ClientRequestToken: NotRequired[str]
    JobTag: NotRequired[str]
    NotificationChannel: NotRequired[NotificationChannelTypeDef]
    OutputConfig: NotRequired[OutputConfigTypeDef]
    KMSKeyId: NotRequired[str]


class StartLendingAnalysisRequestRequestTypeDef(TypedDict):
    DocumentLocation: DocumentLocationTypeDef
    ClientRequestToken: NotRequired[str]
    JobTag: NotRequired[str]
    NotificationChannel: NotRequired[NotificationChannelTypeDef]
    OutputConfig: NotRequired[OutputConfigTypeDef]
    KMSKeyId: NotRequired[str]


class GetAdapterVersionResponseTypeDef(TypedDict):
    AdapterId: str
    AdapterVersion: str
    CreationTime: datetime
    FeatureTypes: List[FeatureTypeType]
    Status: AdapterVersionStatusType
    StatusMessage: str
    DatasetConfig: AdapterVersionDatasetConfigTypeDef
    KMSKeyId: str
    OutputConfig: OutputConfigTypeDef
    EvaluationMetrics: List[AdapterVersionEvaluationMetricTypeDef]
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


IdentityDocumentFieldTypeDef = TypedDict(
    "IdentityDocumentFieldTypeDef",
    {
        "Type": NotRequired[AnalyzeIDDetectionsTypeDef],
        "ValueDetection": NotRequired[AnalyzeIDDetectionsTypeDef],
    },
)


class AnalyzeExpenseRequestRequestTypeDef(TypedDict):
    Document: DocumentTypeDef


class AnalyzeIDRequestRequestTypeDef(TypedDict):
    DocumentPages: Sequence[DocumentTypeDef]


class DetectDocumentTextRequestRequestTypeDef(TypedDict):
    Document: DocumentTypeDef


class LendingSummaryTypeDef(TypedDict):
    DocumentGroups: NotRequired[List[DocumentGroupTypeDef]]
    UndetectedDocumentTypes: NotRequired[List[str]]


BlockTypeDef = TypedDict(
    "BlockTypeDef",
    {
        "BlockType": NotRequired[BlockTypeType],
        "Confidence": NotRequired[float],
        "Text": NotRequired[str],
        "TextType": NotRequired[TextTypeType],
        "RowIndex": NotRequired[int],
        "ColumnIndex": NotRequired[int],
        "RowSpan": NotRequired[int],
        "ColumnSpan": NotRequired[int],
        "Geometry": NotRequired[GeometryTypeDef],
        "Id": NotRequired[str],
        "Relationships": NotRequired[List[RelationshipTypeDef]],
        "EntityTypes": NotRequired[List[EntityTypeType]],
        "SelectionStatus": NotRequired[SelectionStatusType],
        "Page": NotRequired[int],
        "Query": NotRequired[QueryOutputTypeDef],
    },
)
ExpenseDetectionTypeDef = TypedDict(
    "ExpenseDetectionTypeDef",
    {
        "Text": NotRequired[str],
        "Geometry": NotRequired[GeometryTypeDef],
        "Confidence": NotRequired[float],
    },
)
LendingDetectionTypeDef = TypedDict(
    "LendingDetectionTypeDef",
    {
        "Text": NotRequired[str],
        "SelectionStatus": NotRequired[SelectionStatusType],
        "Geometry": NotRequired[GeometryTypeDef],
        "Confidence": NotRequired[float],
    },
)


class SignatureDetectionTypeDef(TypedDict):
    Confidence: NotRequired[float]
    Geometry: NotRequired[GeometryTypeDef]


class QueriesConfigTypeDef(TypedDict):
    Queries: Sequence[QueryUnionTypeDef]


class GetLendingAnalysisSummaryResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    JobStatus: JobStatusType
    Summary: LendingSummaryTypeDef
    Warnings: List[WarningTypeDef]
    StatusMessage: str
    AnalyzeLendingModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class AnalyzeDocumentResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    Blocks: List[BlockTypeDef]
    HumanLoopActivationOutput: HumanLoopActivationOutputTypeDef
    AnalyzeDocumentModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class DetectDocumentTextResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    Blocks: List[BlockTypeDef]
    DetectDocumentTextModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetDocumentAnalysisResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    JobStatus: JobStatusType
    Blocks: List[BlockTypeDef]
    Warnings: List[WarningTypeDef]
    StatusMessage: str
    AnalyzeDocumentModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetDocumentTextDetectionResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    JobStatus: JobStatusType
    Blocks: List[BlockTypeDef]
    Warnings: List[WarningTypeDef]
    StatusMessage: str
    DetectDocumentTextModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class IdentityDocumentTypeDef(TypedDict):
    DocumentIndex: NotRequired[int]
    IdentityDocumentFields: NotRequired[List[IdentityDocumentFieldTypeDef]]
    Blocks: NotRequired[List[BlockTypeDef]]


ExpenseFieldTypeDef = TypedDict(
    "ExpenseFieldTypeDef",
    {
        "Type": NotRequired[ExpenseTypeTypeDef],
        "LabelDetection": NotRequired[ExpenseDetectionTypeDef],
        "ValueDetection": NotRequired[ExpenseDetectionTypeDef],
        "PageNumber": NotRequired[int],
        "Currency": NotRequired[ExpenseCurrencyTypeDef],
        "GroupProperties": NotRequired[List[ExpenseGroupPropertyTypeDef]],
    },
)
LendingFieldTypeDef = TypedDict(
    "LendingFieldTypeDef",
    {
        "Type": NotRequired[str],
        "KeyDetection": NotRequired[LendingDetectionTypeDef],
        "ValueDetections": NotRequired[List[LendingDetectionTypeDef]],
    },
)


class AnalyzeDocumentRequestRequestTypeDef(TypedDict):
    Document: DocumentTypeDef
    FeatureTypes: Sequence[FeatureTypeType]
    HumanLoopConfig: NotRequired[HumanLoopConfigTypeDef]
    QueriesConfig: NotRequired[QueriesConfigTypeDef]
    AdaptersConfig: NotRequired[AdaptersConfigTypeDef]


class StartDocumentAnalysisRequestRequestTypeDef(TypedDict):
    DocumentLocation: DocumentLocationTypeDef
    FeatureTypes: Sequence[FeatureTypeType]
    ClientRequestToken: NotRequired[str]
    JobTag: NotRequired[str]
    NotificationChannel: NotRequired[NotificationChannelTypeDef]
    OutputConfig: NotRequired[OutputConfigTypeDef]
    KMSKeyId: NotRequired[str]
    QueriesConfig: NotRequired[QueriesConfigTypeDef]
    AdaptersConfig: NotRequired[AdaptersConfigTypeDef]


class AnalyzeIDResponseTypeDef(TypedDict):
    IdentityDocuments: List[IdentityDocumentTypeDef]
    DocumentMetadata: DocumentMetadataTypeDef
    AnalyzeIDModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class LineItemFieldsTypeDef(TypedDict):
    LineItemExpenseFields: NotRequired[List[ExpenseFieldTypeDef]]


class LendingDocumentTypeDef(TypedDict):
    LendingFields: NotRequired[List[LendingFieldTypeDef]]
    SignatureDetections: NotRequired[List[SignatureDetectionTypeDef]]


class LineItemGroupTypeDef(TypedDict):
    LineItemGroupIndex: NotRequired[int]
    LineItems: NotRequired[List[LineItemFieldsTypeDef]]


class ExpenseDocumentTypeDef(TypedDict):
    ExpenseIndex: NotRequired[int]
    SummaryFields: NotRequired[List[ExpenseFieldTypeDef]]
    LineItemGroups: NotRequired[List[LineItemGroupTypeDef]]
    Blocks: NotRequired[List[BlockTypeDef]]


class AnalyzeExpenseResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    ExpenseDocuments: List[ExpenseDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ExtractionTypeDef(TypedDict):
    LendingDocument: NotRequired[LendingDocumentTypeDef]
    ExpenseDocument: NotRequired[ExpenseDocumentTypeDef]
    IdentityDocument: NotRequired[IdentityDocumentTypeDef]


class GetExpenseAnalysisResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    JobStatus: JobStatusType
    ExpenseDocuments: List[ExpenseDocumentTypeDef]
    Warnings: List[WarningTypeDef]
    StatusMessage: str
    AnalyzeExpenseModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LendingResultTypeDef(TypedDict):
    Page: NotRequired[int]
    PageClassification: NotRequired[PageClassificationTypeDef]
    Extractions: NotRequired[List[ExtractionTypeDef]]


class GetLendingAnalysisResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    JobStatus: JobStatusType
    Results: List[LendingResultTypeDef]
    Warnings: List[WarningTypeDef]
    StatusMessage: str
    AnalyzeLendingModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
