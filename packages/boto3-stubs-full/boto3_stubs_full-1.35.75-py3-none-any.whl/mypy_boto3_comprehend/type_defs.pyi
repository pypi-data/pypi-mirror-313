"""
Type annotations for comprehend service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehend/type_defs/)

Usage::

    ```python
    from mypy_boto3_comprehend.type_defs import AugmentedManifestsListItemOutputTypeDef

    data: AugmentedManifestsListItemOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AugmentedManifestsDocumentTypeFormatType,
    BlockTypeType,
    DatasetDataFormatType,
    DatasetStatusType,
    DatasetTypeType,
    DocumentClassifierDataFormatType,
    DocumentClassifierDocumentTypeFormatType,
    DocumentClassifierModeType,
    DocumentReadActionType,
    DocumentReadFeatureTypesType,
    DocumentReadModeType,
    DocumentTypeType,
    EndpointStatusType,
    EntityRecognizerDataFormatType,
    EntityTypeType,
    FlywheelIterationStatusType,
    FlywheelStatusType,
    InputFormatType,
    JobStatusType,
    LanguageCodeType,
    ModelStatusType,
    ModelTypeType,
    PageBasedErrorCodeType,
    PageBasedWarningCodeType,
    PartOfSpeechTagTypeType,
    PiiEntitiesDetectionMaskModeType,
    PiiEntitiesDetectionModeType,
    PiiEntityTypeType,
    SentimentTypeType,
    SplitType,
    SyntaxLanguageCodeType,
    TargetedSentimentEntityTypeType,
    ToxicContentTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AugmentedManifestsListItemOutputTypeDef",
    "AugmentedManifestsListItemTypeDef",
    "AugmentedManifestsListItemUnionTypeDef",
    "BatchDetectDominantLanguageItemResultTypeDef",
    "BatchDetectDominantLanguageRequestRequestTypeDef",
    "BatchDetectDominantLanguageResponseTypeDef",
    "BatchDetectEntitiesItemResultTypeDef",
    "BatchDetectEntitiesRequestRequestTypeDef",
    "BatchDetectEntitiesResponseTypeDef",
    "BatchDetectKeyPhrasesItemResultTypeDef",
    "BatchDetectKeyPhrasesRequestRequestTypeDef",
    "BatchDetectKeyPhrasesResponseTypeDef",
    "BatchDetectSentimentItemResultTypeDef",
    "BatchDetectSentimentRequestRequestTypeDef",
    "BatchDetectSentimentResponseTypeDef",
    "BatchDetectSyntaxItemResultTypeDef",
    "BatchDetectSyntaxRequestRequestTypeDef",
    "BatchDetectSyntaxResponseTypeDef",
    "BatchDetectTargetedSentimentItemResultTypeDef",
    "BatchDetectTargetedSentimentRequestRequestTypeDef",
    "BatchDetectTargetedSentimentResponseTypeDef",
    "BatchItemErrorTypeDef",
    "BlobTypeDef",
    "BlockReferenceTypeDef",
    "BlockTypeDef",
    "BoundingBoxTypeDef",
    "ChildBlockTypeDef",
    "ClassifierEvaluationMetricsTypeDef",
    "ClassifierMetadataTypeDef",
    "ClassifyDocumentRequestRequestTypeDef",
    "ClassifyDocumentResponseTypeDef",
    "ContainsPiiEntitiesRequestRequestTypeDef",
    "ContainsPiiEntitiesResponseTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateDocumentClassifierRequestRequestTypeDef",
    "CreateDocumentClassifierResponseTypeDef",
    "CreateEndpointRequestRequestTypeDef",
    "CreateEndpointResponseTypeDef",
    "CreateEntityRecognizerRequestRequestTypeDef",
    "CreateEntityRecognizerResponseTypeDef",
    "CreateFlywheelRequestRequestTypeDef",
    "CreateFlywheelResponseTypeDef",
    "DataSecurityConfigOutputTypeDef",
    "DataSecurityConfigTypeDef",
    "DatasetAugmentedManifestsListItemTypeDef",
    "DatasetDocumentClassifierInputDataConfigTypeDef",
    "DatasetEntityRecognizerAnnotationsTypeDef",
    "DatasetEntityRecognizerDocumentsTypeDef",
    "DatasetEntityRecognizerEntityListTypeDef",
    "DatasetEntityRecognizerInputDataConfigTypeDef",
    "DatasetFilterTypeDef",
    "DatasetInputDataConfigTypeDef",
    "DatasetPropertiesTypeDef",
    "DeleteDocumentClassifierRequestRequestTypeDef",
    "DeleteEndpointRequestRequestTypeDef",
    "DeleteEntityRecognizerRequestRequestTypeDef",
    "DeleteFlywheelRequestRequestTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeDatasetResponseTypeDef",
    "DescribeDocumentClassificationJobRequestRequestTypeDef",
    "DescribeDocumentClassificationJobResponseTypeDef",
    "DescribeDocumentClassifierRequestRequestTypeDef",
    "DescribeDocumentClassifierResponseTypeDef",
    "DescribeDominantLanguageDetectionJobRequestRequestTypeDef",
    "DescribeDominantLanguageDetectionJobResponseTypeDef",
    "DescribeEndpointRequestRequestTypeDef",
    "DescribeEndpointResponseTypeDef",
    "DescribeEntitiesDetectionJobRequestRequestTypeDef",
    "DescribeEntitiesDetectionJobResponseTypeDef",
    "DescribeEntityRecognizerRequestRequestTypeDef",
    "DescribeEntityRecognizerResponseTypeDef",
    "DescribeEventsDetectionJobRequestRequestTypeDef",
    "DescribeEventsDetectionJobResponseTypeDef",
    "DescribeFlywheelIterationRequestRequestTypeDef",
    "DescribeFlywheelIterationResponseTypeDef",
    "DescribeFlywheelRequestRequestTypeDef",
    "DescribeFlywheelResponseTypeDef",
    "DescribeKeyPhrasesDetectionJobRequestRequestTypeDef",
    "DescribeKeyPhrasesDetectionJobResponseTypeDef",
    "DescribePiiEntitiesDetectionJobRequestRequestTypeDef",
    "DescribePiiEntitiesDetectionJobResponseTypeDef",
    "DescribeResourcePolicyRequestRequestTypeDef",
    "DescribeResourcePolicyResponseTypeDef",
    "DescribeSentimentDetectionJobRequestRequestTypeDef",
    "DescribeSentimentDetectionJobResponseTypeDef",
    "DescribeTargetedSentimentDetectionJobRequestRequestTypeDef",
    "DescribeTargetedSentimentDetectionJobResponseTypeDef",
    "DescribeTopicsDetectionJobRequestRequestTypeDef",
    "DescribeTopicsDetectionJobResponseTypeDef",
    "DetectDominantLanguageRequestRequestTypeDef",
    "DetectDominantLanguageResponseTypeDef",
    "DetectEntitiesRequestRequestTypeDef",
    "DetectEntitiesResponseTypeDef",
    "DetectKeyPhrasesRequestRequestTypeDef",
    "DetectKeyPhrasesResponseTypeDef",
    "DetectPiiEntitiesRequestRequestTypeDef",
    "DetectPiiEntitiesResponseTypeDef",
    "DetectSentimentRequestRequestTypeDef",
    "DetectSentimentResponseTypeDef",
    "DetectSyntaxRequestRequestTypeDef",
    "DetectSyntaxResponseTypeDef",
    "DetectTargetedSentimentRequestRequestTypeDef",
    "DetectTargetedSentimentResponseTypeDef",
    "DetectToxicContentRequestRequestTypeDef",
    "DetectToxicContentResponseTypeDef",
    "DocumentClassTypeDef",
    "DocumentClassificationConfigOutputTypeDef",
    "DocumentClassificationConfigTypeDef",
    "DocumentClassificationConfigUnionTypeDef",
    "DocumentClassificationJobFilterTypeDef",
    "DocumentClassificationJobPropertiesTypeDef",
    "DocumentClassifierDocumentsTypeDef",
    "DocumentClassifierFilterTypeDef",
    "DocumentClassifierInputDataConfigOutputTypeDef",
    "DocumentClassifierInputDataConfigTypeDef",
    "DocumentClassifierOutputDataConfigTypeDef",
    "DocumentClassifierPropertiesTypeDef",
    "DocumentClassifierSummaryTypeDef",
    "DocumentLabelTypeDef",
    "DocumentMetadataTypeDef",
    "DocumentReaderConfigOutputTypeDef",
    "DocumentReaderConfigTypeDef",
    "DocumentReaderConfigUnionTypeDef",
    "DocumentTypeListItemTypeDef",
    "DominantLanguageDetectionJobFilterTypeDef",
    "DominantLanguageDetectionJobPropertiesTypeDef",
    "DominantLanguageTypeDef",
    "EndpointFilterTypeDef",
    "EndpointPropertiesTypeDef",
    "EntitiesDetectionJobFilterTypeDef",
    "EntitiesDetectionJobPropertiesTypeDef",
    "EntityLabelTypeDef",
    "EntityRecognitionConfigOutputTypeDef",
    "EntityRecognitionConfigTypeDef",
    "EntityRecognitionConfigUnionTypeDef",
    "EntityRecognizerAnnotationsTypeDef",
    "EntityRecognizerDocumentsTypeDef",
    "EntityRecognizerEntityListTypeDef",
    "EntityRecognizerEvaluationMetricsTypeDef",
    "EntityRecognizerFilterTypeDef",
    "EntityRecognizerInputDataConfigOutputTypeDef",
    "EntityRecognizerInputDataConfigTypeDef",
    "EntityRecognizerMetadataEntityTypesListItemTypeDef",
    "EntityRecognizerMetadataTypeDef",
    "EntityRecognizerOutputDataConfigTypeDef",
    "EntityRecognizerPropertiesTypeDef",
    "EntityRecognizerSummaryTypeDef",
    "EntityTypeDef",
    "EntityTypesEvaluationMetricsTypeDef",
    "EntityTypesListItemTypeDef",
    "ErrorsListItemTypeDef",
    "EventsDetectionJobFilterTypeDef",
    "EventsDetectionJobPropertiesTypeDef",
    "ExtractedCharactersListItemTypeDef",
    "FlywheelFilterTypeDef",
    "FlywheelIterationFilterTypeDef",
    "FlywheelIterationPropertiesTypeDef",
    "FlywheelModelEvaluationMetricsTypeDef",
    "FlywheelPropertiesTypeDef",
    "FlywheelSummaryTypeDef",
    "GeometryTypeDef",
    "ImportModelRequestRequestTypeDef",
    "ImportModelResponseTypeDef",
    "InputDataConfigOutputTypeDef",
    "InputDataConfigTypeDef",
    "KeyPhraseTypeDef",
    "KeyPhrasesDetectionJobFilterTypeDef",
    "KeyPhrasesDetectionJobPropertiesTypeDef",
    "ListDatasetsRequestRequestTypeDef",
    "ListDatasetsResponseTypeDef",
    "ListDocumentClassificationJobsRequestListDocumentClassificationJobsPaginateTypeDef",
    "ListDocumentClassificationJobsRequestRequestTypeDef",
    "ListDocumentClassificationJobsResponseTypeDef",
    "ListDocumentClassifierSummariesRequestRequestTypeDef",
    "ListDocumentClassifierSummariesResponseTypeDef",
    "ListDocumentClassifiersRequestListDocumentClassifiersPaginateTypeDef",
    "ListDocumentClassifiersRequestRequestTypeDef",
    "ListDocumentClassifiersResponseTypeDef",
    "ListDominantLanguageDetectionJobsRequestListDominantLanguageDetectionJobsPaginateTypeDef",
    "ListDominantLanguageDetectionJobsRequestRequestTypeDef",
    "ListDominantLanguageDetectionJobsResponseTypeDef",
    "ListEndpointsRequestListEndpointsPaginateTypeDef",
    "ListEndpointsRequestRequestTypeDef",
    "ListEndpointsResponseTypeDef",
    "ListEntitiesDetectionJobsRequestListEntitiesDetectionJobsPaginateTypeDef",
    "ListEntitiesDetectionJobsRequestRequestTypeDef",
    "ListEntitiesDetectionJobsResponseTypeDef",
    "ListEntityRecognizerSummariesRequestRequestTypeDef",
    "ListEntityRecognizerSummariesResponseTypeDef",
    "ListEntityRecognizersRequestListEntityRecognizersPaginateTypeDef",
    "ListEntityRecognizersRequestRequestTypeDef",
    "ListEntityRecognizersResponseTypeDef",
    "ListEventsDetectionJobsRequestRequestTypeDef",
    "ListEventsDetectionJobsResponseTypeDef",
    "ListFlywheelIterationHistoryRequestRequestTypeDef",
    "ListFlywheelIterationHistoryResponseTypeDef",
    "ListFlywheelsRequestRequestTypeDef",
    "ListFlywheelsResponseTypeDef",
    "ListKeyPhrasesDetectionJobsRequestListKeyPhrasesDetectionJobsPaginateTypeDef",
    "ListKeyPhrasesDetectionJobsRequestRequestTypeDef",
    "ListKeyPhrasesDetectionJobsResponseTypeDef",
    "ListPiiEntitiesDetectionJobsRequestListPiiEntitiesDetectionJobsPaginateTypeDef",
    "ListPiiEntitiesDetectionJobsRequestRequestTypeDef",
    "ListPiiEntitiesDetectionJobsResponseTypeDef",
    "ListSentimentDetectionJobsRequestListSentimentDetectionJobsPaginateTypeDef",
    "ListSentimentDetectionJobsRequestRequestTypeDef",
    "ListSentimentDetectionJobsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTargetedSentimentDetectionJobsRequestRequestTypeDef",
    "ListTargetedSentimentDetectionJobsResponseTypeDef",
    "ListTopicsDetectionJobsRequestListTopicsDetectionJobsPaginateTypeDef",
    "ListTopicsDetectionJobsRequestRequestTypeDef",
    "ListTopicsDetectionJobsResponseTypeDef",
    "MentionSentimentTypeDef",
    "OutputDataConfigTypeDef",
    "PaginatorConfigTypeDef",
    "PartOfSpeechTagTypeDef",
    "PiiEntitiesDetectionJobFilterTypeDef",
    "PiiEntitiesDetectionJobPropertiesTypeDef",
    "PiiEntityTypeDef",
    "PiiOutputDataConfigTypeDef",
    "PointTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "RedactionConfigOutputTypeDef",
    "RedactionConfigTypeDef",
    "RelationshipsListItemTypeDef",
    "ResponseMetadataTypeDef",
    "SentimentDetectionJobFilterTypeDef",
    "SentimentDetectionJobPropertiesTypeDef",
    "SentimentScoreTypeDef",
    "StartDocumentClassificationJobRequestRequestTypeDef",
    "StartDocumentClassificationJobResponseTypeDef",
    "StartDominantLanguageDetectionJobRequestRequestTypeDef",
    "StartDominantLanguageDetectionJobResponseTypeDef",
    "StartEntitiesDetectionJobRequestRequestTypeDef",
    "StartEntitiesDetectionJobResponseTypeDef",
    "StartEventsDetectionJobRequestRequestTypeDef",
    "StartEventsDetectionJobResponseTypeDef",
    "StartFlywheelIterationRequestRequestTypeDef",
    "StartFlywheelIterationResponseTypeDef",
    "StartKeyPhrasesDetectionJobRequestRequestTypeDef",
    "StartKeyPhrasesDetectionJobResponseTypeDef",
    "StartPiiEntitiesDetectionJobRequestRequestTypeDef",
    "StartPiiEntitiesDetectionJobResponseTypeDef",
    "StartSentimentDetectionJobRequestRequestTypeDef",
    "StartSentimentDetectionJobResponseTypeDef",
    "StartTargetedSentimentDetectionJobRequestRequestTypeDef",
    "StartTargetedSentimentDetectionJobResponseTypeDef",
    "StartTopicsDetectionJobRequestRequestTypeDef",
    "StartTopicsDetectionJobResponseTypeDef",
    "StopDominantLanguageDetectionJobRequestRequestTypeDef",
    "StopDominantLanguageDetectionJobResponseTypeDef",
    "StopEntitiesDetectionJobRequestRequestTypeDef",
    "StopEntitiesDetectionJobResponseTypeDef",
    "StopEventsDetectionJobRequestRequestTypeDef",
    "StopEventsDetectionJobResponseTypeDef",
    "StopKeyPhrasesDetectionJobRequestRequestTypeDef",
    "StopKeyPhrasesDetectionJobResponseTypeDef",
    "StopPiiEntitiesDetectionJobRequestRequestTypeDef",
    "StopPiiEntitiesDetectionJobResponseTypeDef",
    "StopSentimentDetectionJobRequestRequestTypeDef",
    "StopSentimentDetectionJobResponseTypeDef",
    "StopTargetedSentimentDetectionJobRequestRequestTypeDef",
    "StopTargetedSentimentDetectionJobResponseTypeDef",
    "StopTrainingDocumentClassifierRequestRequestTypeDef",
    "StopTrainingEntityRecognizerRequestRequestTypeDef",
    "SyntaxTokenTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TargetedSentimentDetectionJobFilterTypeDef",
    "TargetedSentimentDetectionJobPropertiesTypeDef",
    "TargetedSentimentEntityTypeDef",
    "TargetedSentimentMentionTypeDef",
    "TaskConfigOutputTypeDef",
    "TaskConfigTypeDef",
    "TextSegmentTypeDef",
    "TimestampTypeDef",
    "TopicsDetectionJobFilterTypeDef",
    "TopicsDetectionJobPropertiesTypeDef",
    "ToxicContentTypeDef",
    "ToxicLabelsTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDataSecurityConfigTypeDef",
    "UpdateEndpointRequestRequestTypeDef",
    "UpdateEndpointResponseTypeDef",
    "UpdateFlywheelRequestRequestTypeDef",
    "UpdateFlywheelResponseTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
    "VpcConfigUnionTypeDef",
    "WarningsListItemTypeDef",
)

class AugmentedManifestsListItemOutputTypeDef(TypedDict):
    S3Uri: str
    AttributeNames: List[str]
    Split: NotRequired[SplitType]
    AnnotationDataS3Uri: NotRequired[str]
    SourceDocumentsS3Uri: NotRequired[str]
    DocumentType: NotRequired[AugmentedManifestsDocumentTypeFormatType]

class AugmentedManifestsListItemTypeDef(TypedDict):
    S3Uri: str
    AttributeNames: Sequence[str]
    Split: NotRequired[SplitType]
    AnnotationDataS3Uri: NotRequired[str]
    SourceDocumentsS3Uri: NotRequired[str]
    DocumentType: NotRequired[AugmentedManifestsDocumentTypeFormatType]

class DominantLanguageTypeDef(TypedDict):
    LanguageCode: NotRequired[str]
    Score: NotRequired[float]

class BatchDetectDominantLanguageRequestRequestTypeDef(TypedDict):
    TextList: Sequence[str]

class BatchItemErrorTypeDef(TypedDict):
    Index: NotRequired[int]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchDetectEntitiesRequestRequestTypeDef(TypedDict):
    TextList: Sequence[str]
    LanguageCode: LanguageCodeType

KeyPhraseTypeDef = TypedDict(
    "KeyPhraseTypeDef",
    {
        "Score": NotRequired[float],
        "Text": NotRequired[str],
        "BeginOffset": NotRequired[int],
        "EndOffset": NotRequired[int],
    },
)

class BatchDetectKeyPhrasesRequestRequestTypeDef(TypedDict):
    TextList: Sequence[str]
    LanguageCode: LanguageCodeType

class SentimentScoreTypeDef(TypedDict):
    Positive: NotRequired[float]
    Negative: NotRequired[float]
    Neutral: NotRequired[float]
    Mixed: NotRequired[float]

class BatchDetectSentimentRequestRequestTypeDef(TypedDict):
    TextList: Sequence[str]
    LanguageCode: LanguageCodeType

class BatchDetectSyntaxRequestRequestTypeDef(TypedDict):
    TextList: Sequence[str]
    LanguageCode: SyntaxLanguageCodeType

class BatchDetectTargetedSentimentRequestRequestTypeDef(TypedDict):
    TextList: Sequence[str]
    LanguageCode: LanguageCodeType

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class ChildBlockTypeDef(TypedDict):
    ChildBlockId: NotRequired[str]
    BeginOffset: NotRequired[int]
    EndOffset: NotRequired[int]

RelationshipsListItemTypeDef = TypedDict(
    "RelationshipsListItemTypeDef",
    {
        "Ids": NotRequired[List[str]],
        "Type": NotRequired[Literal["CHILD"]],
    },
)

class BoundingBoxTypeDef(TypedDict):
    Height: NotRequired[float]
    Left: NotRequired[float]
    Top: NotRequired[float]
    Width: NotRequired[float]

class ClassifierEvaluationMetricsTypeDef(TypedDict):
    Accuracy: NotRequired[float]
    Precision: NotRequired[float]
    Recall: NotRequired[float]
    F1Score: NotRequired[float]
    MicroPrecision: NotRequired[float]
    MicroRecall: NotRequired[float]
    MicroF1Score: NotRequired[float]
    HammingLoss: NotRequired[float]

class DocumentReaderConfigTypeDef(TypedDict):
    DocumentReadAction: DocumentReadActionType
    DocumentReadMode: NotRequired[DocumentReadModeType]
    FeatureTypes: NotRequired[Sequence[DocumentReadFeatureTypesType]]

class DocumentClassTypeDef(TypedDict):
    Name: NotRequired[str]
    Score: NotRequired[float]
    Page: NotRequired[int]

class DocumentLabelTypeDef(TypedDict):
    Name: NotRequired[str]
    Score: NotRequired[float]
    Page: NotRequired[int]

DocumentTypeListItemTypeDef = TypedDict(
    "DocumentTypeListItemTypeDef",
    {
        "Page": NotRequired[int],
        "Type": NotRequired[DocumentTypeType],
    },
)

class ErrorsListItemTypeDef(TypedDict):
    Page: NotRequired[int]
    ErrorCode: NotRequired[PageBasedErrorCodeType]
    ErrorMessage: NotRequired[str]

class WarningsListItemTypeDef(TypedDict):
    Page: NotRequired[int]
    WarnCode: NotRequired[PageBasedWarningCodeType]
    WarnMessage: NotRequired[str]

ContainsPiiEntitiesRequestRequestTypeDef = TypedDict(
    "ContainsPiiEntitiesRequestRequestTypeDef",
    {
        "Text": str,
        "LanguageCode": LanguageCodeType,
    },
)

class EntityLabelTypeDef(TypedDict):
    Name: NotRequired[PiiEntityTypeType]
    Score: NotRequired[float]

class TagTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]

class DocumentClassifierOutputDataConfigTypeDef(TypedDict):
    S3Uri: NotRequired[str]
    KmsKeyId: NotRequired[str]
    FlywheelStatsS3Prefix: NotRequired[str]

class VpcConfigTypeDef(TypedDict):
    SecurityGroupIds: Sequence[str]
    Subnets: Sequence[str]

class VpcConfigOutputTypeDef(TypedDict):
    SecurityGroupIds: List[str]
    Subnets: List[str]

class DatasetAugmentedManifestsListItemTypeDef(TypedDict):
    AttributeNames: Sequence[str]
    S3Uri: str
    AnnotationDataS3Uri: NotRequired[str]
    SourceDocumentsS3Uri: NotRequired[str]
    DocumentType: NotRequired[AugmentedManifestsDocumentTypeFormatType]

class DatasetDocumentClassifierInputDataConfigTypeDef(TypedDict):
    S3Uri: str
    LabelDelimiter: NotRequired[str]

class DatasetEntityRecognizerAnnotationsTypeDef(TypedDict):
    S3Uri: str

class DatasetEntityRecognizerDocumentsTypeDef(TypedDict):
    S3Uri: str
    InputFormat: NotRequired[InputFormatType]

class DatasetEntityRecognizerEntityListTypeDef(TypedDict):
    S3Uri: str

TimestampTypeDef = Union[datetime, str]

class DatasetPropertiesTypeDef(TypedDict):
    DatasetArn: NotRequired[str]
    DatasetName: NotRequired[str]
    DatasetType: NotRequired[DatasetTypeType]
    DatasetS3Uri: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[DatasetStatusType]
    Message: NotRequired[str]
    NumberOfDocuments: NotRequired[int]
    CreationTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]

class DeleteDocumentClassifierRequestRequestTypeDef(TypedDict):
    DocumentClassifierArn: str

class DeleteEndpointRequestRequestTypeDef(TypedDict):
    EndpointArn: str

class DeleteEntityRecognizerRequestRequestTypeDef(TypedDict):
    EntityRecognizerArn: str

class DeleteFlywheelRequestRequestTypeDef(TypedDict):
    FlywheelArn: str

class DeleteResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    PolicyRevisionId: NotRequired[str]

class DescribeDatasetRequestRequestTypeDef(TypedDict):
    DatasetArn: str

class DescribeDocumentClassificationJobRequestRequestTypeDef(TypedDict):
    JobId: str

class DescribeDocumentClassifierRequestRequestTypeDef(TypedDict):
    DocumentClassifierArn: str

class DescribeDominantLanguageDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class DescribeEndpointRequestRequestTypeDef(TypedDict):
    EndpointArn: str

class EndpointPropertiesTypeDef(TypedDict):
    EndpointArn: NotRequired[str]
    Status: NotRequired[EndpointStatusType]
    Message: NotRequired[str]
    ModelArn: NotRequired[str]
    DesiredModelArn: NotRequired[str]
    DesiredInferenceUnits: NotRequired[int]
    CurrentInferenceUnits: NotRequired[int]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    DataAccessRoleArn: NotRequired[str]
    DesiredDataAccessRoleArn: NotRequired[str]
    FlywheelArn: NotRequired[str]

class DescribeEntitiesDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class DescribeEntityRecognizerRequestRequestTypeDef(TypedDict):
    EntityRecognizerArn: str

class DescribeEventsDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class DescribeFlywheelIterationRequestRequestTypeDef(TypedDict):
    FlywheelArn: str
    FlywheelIterationId: str

class DescribeFlywheelRequestRequestTypeDef(TypedDict):
    FlywheelArn: str

class DescribeKeyPhrasesDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class DescribePiiEntitiesDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class DescribeResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class DescribeSentimentDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class DescribeTargetedSentimentDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class DescribeTopicsDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

DetectDominantLanguageRequestRequestTypeDef = TypedDict(
    "DetectDominantLanguageRequestRequestTypeDef",
    {
        "Text": str,
    },
)
DetectKeyPhrasesRequestRequestTypeDef = TypedDict(
    "DetectKeyPhrasesRequestRequestTypeDef",
    {
        "Text": str,
        "LanguageCode": LanguageCodeType,
    },
)
DetectPiiEntitiesRequestRequestTypeDef = TypedDict(
    "DetectPiiEntitiesRequestRequestTypeDef",
    {
        "Text": str,
        "LanguageCode": LanguageCodeType,
    },
)
PiiEntityTypeDef = TypedDict(
    "PiiEntityTypeDef",
    {
        "Score": NotRequired[float],
        "Type": NotRequired[PiiEntityTypeType],
        "BeginOffset": NotRequired[int],
        "EndOffset": NotRequired[int],
    },
)
DetectSentimentRequestRequestTypeDef = TypedDict(
    "DetectSentimentRequestRequestTypeDef",
    {
        "Text": str,
        "LanguageCode": LanguageCodeType,
    },
)
DetectSyntaxRequestRequestTypeDef = TypedDict(
    "DetectSyntaxRequestRequestTypeDef",
    {
        "Text": str,
        "LanguageCode": SyntaxLanguageCodeType,
    },
)
DetectTargetedSentimentRequestRequestTypeDef = TypedDict(
    "DetectTargetedSentimentRequestRequestTypeDef",
    {
        "Text": str,
        "LanguageCode": LanguageCodeType,
    },
)
TextSegmentTypeDef = TypedDict(
    "TextSegmentTypeDef",
    {
        "Text": str,
    },
)

class DocumentClassificationConfigOutputTypeDef(TypedDict):
    Mode: DocumentClassifierModeType
    Labels: NotRequired[List[str]]

class DocumentClassificationConfigTypeDef(TypedDict):
    Mode: DocumentClassifierModeType
    Labels: NotRequired[Sequence[str]]

class OutputDataConfigTypeDef(TypedDict):
    S3Uri: str
    KmsKeyId: NotRequired[str]

class DocumentClassifierDocumentsTypeDef(TypedDict):
    S3Uri: str
    TestS3Uri: NotRequired[str]

class DocumentReaderConfigOutputTypeDef(TypedDict):
    DocumentReadAction: DocumentReadActionType
    DocumentReadMode: NotRequired[DocumentReadModeType]
    FeatureTypes: NotRequired[List[DocumentReadFeatureTypesType]]

class DocumentClassifierSummaryTypeDef(TypedDict):
    DocumentClassifierName: NotRequired[str]
    NumberOfVersions: NotRequired[int]
    LatestVersionCreatedAt: NotRequired[datetime]
    LatestVersionName: NotRequired[str]
    LatestVersionStatus: NotRequired[ModelStatusType]

class ExtractedCharactersListItemTypeDef(TypedDict):
    Page: NotRequired[int]
    Count: NotRequired[int]

EntityTypesListItemTypeDef = TypedDict(
    "EntityTypesListItemTypeDef",
    {
        "Type": str,
    },
)

class EntityRecognizerAnnotationsTypeDef(TypedDict):
    S3Uri: str
    TestS3Uri: NotRequired[str]

class EntityRecognizerDocumentsTypeDef(TypedDict):
    S3Uri: str
    TestS3Uri: NotRequired[str]
    InputFormat: NotRequired[InputFormatType]

class EntityRecognizerEntityListTypeDef(TypedDict):
    S3Uri: str

class EntityRecognizerEvaluationMetricsTypeDef(TypedDict):
    Precision: NotRequired[float]
    Recall: NotRequired[float]
    F1Score: NotRequired[float]

class EntityTypesEvaluationMetricsTypeDef(TypedDict):
    Precision: NotRequired[float]
    Recall: NotRequired[float]
    F1Score: NotRequired[float]

class EntityRecognizerOutputDataConfigTypeDef(TypedDict):
    FlywheelStatsS3Prefix: NotRequired[str]

class EntityRecognizerSummaryTypeDef(TypedDict):
    RecognizerName: NotRequired[str]
    NumberOfVersions: NotRequired[int]
    LatestVersionCreatedAt: NotRequired[datetime]
    LatestVersionName: NotRequired[str]
    LatestVersionStatus: NotRequired[ModelStatusType]

class FlywheelModelEvaluationMetricsTypeDef(TypedDict):
    AverageF1Score: NotRequired[float]
    AveragePrecision: NotRequired[float]
    AverageRecall: NotRequired[float]
    AverageAccuracy: NotRequired[float]

class FlywheelSummaryTypeDef(TypedDict):
    FlywheelArn: NotRequired[str]
    ActiveModelArn: NotRequired[str]
    DataLakeS3Uri: NotRequired[str]
    Status: NotRequired[FlywheelStatusType]
    ModelType: NotRequired[ModelTypeType]
    Message: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    LatestFlywheelIteration: NotRequired[str]

class PointTypeDef(TypedDict):
    X: NotRequired[float]
    Y: NotRequired[float]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListDocumentClassifierSummariesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListEntityRecognizerSummariesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class PartOfSpeechTagTypeDef(TypedDict):
    Tag: NotRequired[PartOfSpeechTagTypeType]
    Score: NotRequired[float]

class PiiOutputDataConfigTypeDef(TypedDict):
    S3Uri: str
    KmsKeyId: NotRequired[str]

class RedactionConfigOutputTypeDef(TypedDict):
    PiiEntityTypes: NotRequired[List[PiiEntityTypeType]]
    MaskMode: NotRequired[PiiEntitiesDetectionMaskModeType]
    MaskCharacter: NotRequired[str]

class PutResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    ResourcePolicy: str
    PolicyRevisionId: NotRequired[str]

class RedactionConfigTypeDef(TypedDict):
    PiiEntityTypes: NotRequired[Sequence[PiiEntityTypeType]]
    MaskMode: NotRequired[PiiEntitiesDetectionMaskModeType]
    MaskCharacter: NotRequired[str]

class StartFlywheelIterationRequestRequestTypeDef(TypedDict):
    FlywheelArn: str
    ClientRequestToken: NotRequired[str]

class StopDominantLanguageDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class StopEntitiesDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class StopEventsDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class StopKeyPhrasesDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class StopPiiEntitiesDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class StopSentimentDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class StopTargetedSentimentDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class StopTrainingDocumentClassifierRequestRequestTypeDef(TypedDict):
    DocumentClassifierArn: str

class StopTrainingEntityRecognizerRequestRequestTypeDef(TypedDict):
    EntityRecognizerArn: str

class ToxicContentTypeDef(TypedDict):
    Name: NotRequired[ToxicContentTypeType]
    Score: NotRequired[float]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateEndpointRequestRequestTypeDef(TypedDict):
    EndpointArn: str
    DesiredModelArn: NotRequired[str]
    DesiredInferenceUnits: NotRequired[int]
    DesiredDataAccessRoleArn: NotRequired[str]
    FlywheelArn: NotRequired[str]

AugmentedManifestsListItemUnionTypeDef = Union[
    AugmentedManifestsListItemTypeDef, AugmentedManifestsListItemOutputTypeDef
]

class BatchDetectDominantLanguageItemResultTypeDef(TypedDict):
    Index: NotRequired[int]
    Languages: NotRequired[List[DominantLanguageTypeDef]]

class CreateDatasetResponseTypeDef(TypedDict):
    DatasetArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDocumentClassifierResponseTypeDef(TypedDict):
    DocumentClassifierArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEndpointResponseTypeDef(TypedDict):
    EndpointArn: str
    ModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEntityRecognizerResponseTypeDef(TypedDict):
    EntityRecognizerArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFlywheelResponseTypeDef(TypedDict):
    FlywheelArn: str
    ActiveModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeResourcePolicyResponseTypeDef(TypedDict):
    ResourcePolicy: str
    CreationTime: datetime
    LastModifiedTime: datetime
    PolicyRevisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DetectDominantLanguageResponseTypeDef(TypedDict):
    Languages: List[DominantLanguageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ImportModelResponseTypeDef(TypedDict):
    ModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutResourcePolicyResponseTypeDef(TypedDict):
    PolicyRevisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartDocumentClassificationJobResponseTypeDef(TypedDict):
    JobId: str
    JobArn: str
    JobStatus: JobStatusType
    DocumentClassifierArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartDominantLanguageDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobArn: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StartEntitiesDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobArn: str
    JobStatus: JobStatusType
    EntityRecognizerArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartEventsDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobArn: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StartFlywheelIterationResponseTypeDef(TypedDict):
    FlywheelArn: str
    FlywheelIterationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartKeyPhrasesDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobArn: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StartPiiEntitiesDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobArn: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StartSentimentDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobArn: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StartTargetedSentimentDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobArn: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StartTopicsDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobArn: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StopDominantLanguageDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StopEntitiesDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StopEventsDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StopKeyPhrasesDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StopPiiEntitiesDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StopSentimentDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StopTargetedSentimentDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEndpointResponseTypeDef(TypedDict):
    DesiredModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDetectKeyPhrasesItemResultTypeDef(TypedDict):
    Index: NotRequired[int]
    KeyPhrases: NotRequired[List[KeyPhraseTypeDef]]

class DetectKeyPhrasesResponseTypeDef(TypedDict):
    KeyPhrases: List[KeyPhraseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDetectSentimentItemResultTypeDef(TypedDict):
    Index: NotRequired[int]
    Sentiment: NotRequired[SentimentTypeType]
    SentimentScore: NotRequired[SentimentScoreTypeDef]

class DetectSentimentResponseTypeDef(TypedDict):
    Sentiment: SentimentTypeType
    SentimentScore: SentimentScoreTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class MentionSentimentTypeDef(TypedDict):
    Sentiment: NotRequired[SentimentTypeType]
    SentimentScore: NotRequired[SentimentScoreTypeDef]

class BlockReferenceTypeDef(TypedDict):
    BlockId: NotRequired[str]
    BeginOffset: NotRequired[int]
    EndOffset: NotRequired[int]
    ChildBlocks: NotRequired[List[ChildBlockTypeDef]]

class ClassifierMetadataTypeDef(TypedDict):
    NumberOfLabels: NotRequired[int]
    NumberOfTrainedDocuments: NotRequired[int]
    NumberOfTestDocuments: NotRequired[int]
    EvaluationMetrics: NotRequired[ClassifierEvaluationMetricsTypeDef]

ClassifyDocumentRequestRequestTypeDef = TypedDict(
    "ClassifyDocumentRequestRequestTypeDef",
    {
        "EndpointArn": str,
        "Text": NotRequired[str],
        "Bytes": NotRequired[BlobTypeDef],
        "DocumentReaderConfig": NotRequired[DocumentReaderConfigTypeDef],
    },
)
DetectEntitiesRequestRequestTypeDef = TypedDict(
    "DetectEntitiesRequestRequestTypeDef",
    {
        "Text": NotRequired[str],
        "LanguageCode": NotRequired[LanguageCodeType],
        "EndpointArn": NotRequired[str],
        "Bytes": NotRequired[BlobTypeDef],
        "DocumentReaderConfig": NotRequired[DocumentReaderConfigTypeDef],
    },
)

class ContainsPiiEntitiesResponseTypeDef(TypedDict):
    Labels: List[EntityLabelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEndpointRequestRequestTypeDef(TypedDict):
    EndpointName: str
    DesiredInferenceUnits: int
    ModelArn: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    DataAccessRoleArn: NotRequired[str]
    FlywheelArn: NotRequired[str]

class ImportModelRequestRequestTypeDef(TypedDict):
    SourceModelArn: str
    ModelName: NotRequired[str]
    VersionName: NotRequired[str]
    ModelKmsKeyId: NotRequired[str]
    DataAccessRoleArn: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class ListTagsForResourceResponseTypeDef(TypedDict):
    ResourceArn: str
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class DataSecurityConfigOutputTypeDef(TypedDict):
    ModelKmsKeyId: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    DataLakeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]

VpcConfigUnionTypeDef = Union[VpcConfigTypeDef, VpcConfigOutputTypeDef]

class DatasetEntityRecognizerInputDataConfigTypeDef(TypedDict):
    Documents: DatasetEntityRecognizerDocumentsTypeDef
    Annotations: NotRequired[DatasetEntityRecognizerAnnotationsTypeDef]
    EntityList: NotRequired[DatasetEntityRecognizerEntityListTypeDef]

class DatasetFilterTypeDef(TypedDict):
    Status: NotRequired[DatasetStatusType]
    DatasetType: NotRequired[DatasetTypeType]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]

class DocumentClassificationJobFilterTypeDef(TypedDict):
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmitTimeBefore: NotRequired[TimestampTypeDef]
    SubmitTimeAfter: NotRequired[TimestampTypeDef]

class DocumentClassifierFilterTypeDef(TypedDict):
    Status: NotRequired[ModelStatusType]
    DocumentClassifierName: NotRequired[str]
    SubmitTimeBefore: NotRequired[TimestampTypeDef]
    SubmitTimeAfter: NotRequired[TimestampTypeDef]

class DominantLanguageDetectionJobFilterTypeDef(TypedDict):
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmitTimeBefore: NotRequired[TimestampTypeDef]
    SubmitTimeAfter: NotRequired[TimestampTypeDef]

class EndpointFilterTypeDef(TypedDict):
    ModelArn: NotRequired[str]
    Status: NotRequired[EndpointStatusType]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]

class EntitiesDetectionJobFilterTypeDef(TypedDict):
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmitTimeBefore: NotRequired[TimestampTypeDef]
    SubmitTimeAfter: NotRequired[TimestampTypeDef]

class EntityRecognizerFilterTypeDef(TypedDict):
    Status: NotRequired[ModelStatusType]
    RecognizerName: NotRequired[str]
    SubmitTimeBefore: NotRequired[TimestampTypeDef]
    SubmitTimeAfter: NotRequired[TimestampTypeDef]

class EventsDetectionJobFilterTypeDef(TypedDict):
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmitTimeBefore: NotRequired[TimestampTypeDef]
    SubmitTimeAfter: NotRequired[TimestampTypeDef]

class FlywheelFilterTypeDef(TypedDict):
    Status: NotRequired[FlywheelStatusType]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]

class FlywheelIterationFilterTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]

class KeyPhrasesDetectionJobFilterTypeDef(TypedDict):
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmitTimeBefore: NotRequired[TimestampTypeDef]
    SubmitTimeAfter: NotRequired[TimestampTypeDef]

class PiiEntitiesDetectionJobFilterTypeDef(TypedDict):
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmitTimeBefore: NotRequired[TimestampTypeDef]
    SubmitTimeAfter: NotRequired[TimestampTypeDef]

class SentimentDetectionJobFilterTypeDef(TypedDict):
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmitTimeBefore: NotRequired[TimestampTypeDef]
    SubmitTimeAfter: NotRequired[TimestampTypeDef]

class TargetedSentimentDetectionJobFilterTypeDef(TypedDict):
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmitTimeBefore: NotRequired[TimestampTypeDef]
    SubmitTimeAfter: NotRequired[TimestampTypeDef]

class TopicsDetectionJobFilterTypeDef(TypedDict):
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmitTimeBefore: NotRequired[TimestampTypeDef]
    SubmitTimeAfter: NotRequired[TimestampTypeDef]

class DescribeDatasetResponseTypeDef(TypedDict):
    DatasetProperties: DatasetPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDatasetsResponseTypeDef(TypedDict):
    DatasetPropertiesList: List[DatasetPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeEndpointResponseTypeDef(TypedDict):
    EndpointProperties: EndpointPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListEndpointsResponseTypeDef(TypedDict):
    EndpointPropertiesList: List[EndpointPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DetectPiiEntitiesResponseTypeDef(TypedDict):
    Entities: List[PiiEntityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DetectToxicContentRequestRequestTypeDef(TypedDict):
    TextSegments: Sequence[TextSegmentTypeDef]
    LanguageCode: LanguageCodeType

DocumentClassificationConfigUnionTypeDef = Union[
    DocumentClassificationConfigTypeDef, DocumentClassificationConfigOutputTypeDef
]

class DocumentClassifierInputDataConfigOutputTypeDef(TypedDict):
    DataFormat: NotRequired[DocumentClassifierDataFormatType]
    S3Uri: NotRequired[str]
    TestS3Uri: NotRequired[str]
    LabelDelimiter: NotRequired[str]
    AugmentedManifests: NotRequired[List[AugmentedManifestsListItemOutputTypeDef]]
    DocumentType: NotRequired[DocumentClassifierDocumentTypeFormatType]
    Documents: NotRequired[DocumentClassifierDocumentsTypeDef]
    DocumentReaderConfig: NotRequired[DocumentReaderConfigOutputTypeDef]

DocumentReaderConfigUnionTypeDef = Union[
    DocumentReaderConfigTypeDef, DocumentReaderConfigOutputTypeDef
]

class InputDataConfigOutputTypeDef(TypedDict):
    S3Uri: str
    InputFormat: NotRequired[InputFormatType]
    DocumentReaderConfig: NotRequired[DocumentReaderConfigOutputTypeDef]

class ListDocumentClassifierSummariesResponseTypeDef(TypedDict):
    DocumentClassifierSummariesList: List[DocumentClassifierSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DocumentMetadataTypeDef(TypedDict):
    Pages: NotRequired[int]
    ExtractedCharacters: NotRequired[List[ExtractedCharactersListItemTypeDef]]

class EntityRecognitionConfigOutputTypeDef(TypedDict):
    EntityTypes: List[EntityTypesListItemTypeDef]

class EntityRecognitionConfigTypeDef(TypedDict):
    EntityTypes: Sequence[EntityTypesListItemTypeDef]

class EntityRecognizerInputDataConfigOutputTypeDef(TypedDict):
    EntityTypes: List[EntityTypesListItemTypeDef]
    DataFormat: NotRequired[EntityRecognizerDataFormatType]
    Documents: NotRequired[EntityRecognizerDocumentsTypeDef]
    Annotations: NotRequired[EntityRecognizerAnnotationsTypeDef]
    EntityList: NotRequired[EntityRecognizerEntityListTypeDef]
    AugmentedManifests: NotRequired[List[AugmentedManifestsListItemOutputTypeDef]]

EntityRecognizerMetadataEntityTypesListItemTypeDef = TypedDict(
    "EntityRecognizerMetadataEntityTypesListItemTypeDef",
    {
        "Type": NotRequired[str],
        "EvaluationMetrics": NotRequired[EntityTypesEvaluationMetricsTypeDef],
        "NumberOfTrainMentions": NotRequired[int],
    },
)

class ListEntityRecognizerSummariesResponseTypeDef(TypedDict):
    EntityRecognizerSummariesList: List[EntityRecognizerSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class FlywheelIterationPropertiesTypeDef(TypedDict):
    FlywheelArn: NotRequired[str]
    FlywheelIterationId: NotRequired[str]
    CreationTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    Status: NotRequired[FlywheelIterationStatusType]
    Message: NotRequired[str]
    EvaluatedModelArn: NotRequired[str]
    EvaluatedModelMetrics: NotRequired[FlywheelModelEvaluationMetricsTypeDef]
    TrainedModelArn: NotRequired[str]
    TrainedModelMetrics: NotRequired[FlywheelModelEvaluationMetricsTypeDef]
    EvaluationManifestS3Prefix: NotRequired[str]

class ListFlywheelsResponseTypeDef(TypedDict):
    FlywheelSummaryList: List[FlywheelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GeometryTypeDef(TypedDict):
    BoundingBox: NotRequired[BoundingBoxTypeDef]
    Polygon: NotRequired[List[PointTypeDef]]

SyntaxTokenTypeDef = TypedDict(
    "SyntaxTokenTypeDef",
    {
        "TokenId": NotRequired[int],
        "Text": NotRequired[str],
        "BeginOffset": NotRequired[int],
        "EndOffset": NotRequired[int],
        "PartOfSpeech": NotRequired[PartOfSpeechTagTypeDef],
    },
)

class ToxicLabelsTypeDef(TypedDict):
    Labels: NotRequired[List[ToxicContentTypeDef]]
    Toxicity: NotRequired[float]

class EntityRecognizerInputDataConfigTypeDef(TypedDict):
    EntityTypes: Sequence[EntityTypesListItemTypeDef]
    DataFormat: NotRequired[EntityRecognizerDataFormatType]
    Documents: NotRequired[EntityRecognizerDocumentsTypeDef]
    Annotations: NotRequired[EntityRecognizerAnnotationsTypeDef]
    EntityList: NotRequired[EntityRecognizerEntityListTypeDef]
    AugmentedManifests: NotRequired[Sequence[AugmentedManifestsListItemUnionTypeDef]]

class BatchDetectDominantLanguageResponseTypeDef(TypedDict):
    ResultList: List[BatchDetectDominantLanguageItemResultTypeDef]
    ErrorList: List[BatchItemErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDetectKeyPhrasesResponseTypeDef(TypedDict):
    ResultList: List[BatchDetectKeyPhrasesItemResultTypeDef]
    ErrorList: List[BatchItemErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDetectSentimentResponseTypeDef(TypedDict):
    ResultList: List[BatchDetectSentimentItemResultTypeDef]
    ErrorList: List[BatchItemErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

TargetedSentimentMentionTypeDef = TypedDict(
    "TargetedSentimentMentionTypeDef",
    {
        "Score": NotRequired[float],
        "GroupScore": NotRequired[float],
        "Text": NotRequired[str],
        "Type": NotRequired[TargetedSentimentEntityTypeType],
        "MentionSentiment": NotRequired[MentionSentimentTypeDef],
        "BeginOffset": NotRequired[int],
        "EndOffset": NotRequired[int],
    },
)
EntityTypeDef = TypedDict(
    "EntityTypeDef",
    {
        "Score": NotRequired[float],
        "Type": NotRequired[EntityTypeType],
        "Text": NotRequired[str],
        "BeginOffset": NotRequired[int],
        "EndOffset": NotRequired[int],
        "BlockReferences": NotRequired[List[BlockReferenceTypeDef]],
    },
)

class DataSecurityConfigTypeDef(TypedDict):
    ModelKmsKeyId: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    DataLakeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigUnionTypeDef]

class UpdateDataSecurityConfigTypeDef(TypedDict):
    ModelKmsKeyId: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigUnionTypeDef]

class DatasetInputDataConfigTypeDef(TypedDict):
    AugmentedManifests: NotRequired[Sequence[DatasetAugmentedManifestsListItemTypeDef]]
    DataFormat: NotRequired[DatasetDataFormatType]
    DocumentClassifierInputDataConfig: NotRequired[DatasetDocumentClassifierInputDataConfigTypeDef]
    EntityRecognizerInputDataConfig: NotRequired[DatasetEntityRecognizerInputDataConfigTypeDef]

class ListDatasetsRequestRequestTypeDef(TypedDict):
    FlywheelArn: NotRequired[str]
    Filter: NotRequired[DatasetFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListDocumentClassificationJobsRequestListDocumentClassificationJobsPaginateTypeDef(TypedDict):
    Filter: NotRequired[DocumentClassificationJobFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDocumentClassificationJobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[DocumentClassificationJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListDocumentClassifiersRequestListDocumentClassifiersPaginateTypeDef(TypedDict):
    Filter: NotRequired[DocumentClassifierFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDocumentClassifiersRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[DocumentClassifierFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListDominantLanguageDetectionJobsRequestListDominantLanguageDetectionJobsPaginateTypeDef(
    TypedDict
):
    Filter: NotRequired[DominantLanguageDetectionJobFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDominantLanguageDetectionJobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[DominantLanguageDetectionJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListEndpointsRequestListEndpointsPaginateTypeDef(TypedDict):
    Filter: NotRequired[EndpointFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEndpointsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[EndpointFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListEntitiesDetectionJobsRequestListEntitiesDetectionJobsPaginateTypeDef(TypedDict):
    Filter: NotRequired[EntitiesDetectionJobFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEntitiesDetectionJobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[EntitiesDetectionJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListEntityRecognizersRequestListEntityRecognizersPaginateTypeDef(TypedDict):
    Filter: NotRequired[EntityRecognizerFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEntityRecognizersRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[EntityRecognizerFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListEventsDetectionJobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[EventsDetectionJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListFlywheelsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[FlywheelFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListFlywheelIterationHistoryRequestRequestTypeDef(TypedDict):
    FlywheelArn: str
    Filter: NotRequired[FlywheelIterationFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListKeyPhrasesDetectionJobsRequestListKeyPhrasesDetectionJobsPaginateTypeDef(TypedDict):
    Filter: NotRequired[KeyPhrasesDetectionJobFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListKeyPhrasesDetectionJobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[KeyPhrasesDetectionJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListPiiEntitiesDetectionJobsRequestListPiiEntitiesDetectionJobsPaginateTypeDef(TypedDict):
    Filter: NotRequired[PiiEntitiesDetectionJobFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPiiEntitiesDetectionJobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[PiiEntitiesDetectionJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListSentimentDetectionJobsRequestListSentimentDetectionJobsPaginateTypeDef(TypedDict):
    Filter: NotRequired[SentimentDetectionJobFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSentimentDetectionJobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[SentimentDetectionJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListTargetedSentimentDetectionJobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[TargetedSentimentDetectionJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListTopicsDetectionJobsRequestListTopicsDetectionJobsPaginateTypeDef(TypedDict):
    Filter: NotRequired[TopicsDetectionJobFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTopicsDetectionJobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[TopicsDetectionJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class DocumentClassifierPropertiesTypeDef(TypedDict):
    DocumentClassifierArn: NotRequired[str]
    LanguageCode: NotRequired[LanguageCodeType]
    Status: NotRequired[ModelStatusType]
    Message: NotRequired[str]
    SubmitTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    TrainingStartTime: NotRequired[datetime]
    TrainingEndTime: NotRequired[datetime]
    InputDataConfig: NotRequired[DocumentClassifierInputDataConfigOutputTypeDef]
    OutputDataConfig: NotRequired[DocumentClassifierOutputDataConfigTypeDef]
    ClassifierMetadata: NotRequired[ClassifierMetadataTypeDef]
    DataAccessRoleArn: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]
    Mode: NotRequired[DocumentClassifierModeType]
    ModelKmsKeyId: NotRequired[str]
    VersionName: NotRequired[str]
    SourceModelArn: NotRequired[str]
    FlywheelArn: NotRequired[str]

class DocumentClassifierInputDataConfigTypeDef(TypedDict):
    DataFormat: NotRequired[DocumentClassifierDataFormatType]
    S3Uri: NotRequired[str]
    TestS3Uri: NotRequired[str]
    LabelDelimiter: NotRequired[str]
    AugmentedManifests: NotRequired[Sequence[AugmentedManifestsListItemUnionTypeDef]]
    DocumentType: NotRequired[DocumentClassifierDocumentTypeFormatType]
    Documents: NotRequired[DocumentClassifierDocumentsTypeDef]
    DocumentReaderConfig: NotRequired[DocumentReaderConfigUnionTypeDef]

class InputDataConfigTypeDef(TypedDict):
    S3Uri: str
    InputFormat: NotRequired[InputFormatType]
    DocumentReaderConfig: NotRequired[DocumentReaderConfigUnionTypeDef]

class DocumentClassificationJobPropertiesTypeDef(TypedDict):
    JobId: NotRequired[str]
    JobArn: NotRequired[str]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    Message: NotRequired[str]
    SubmitTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    DocumentClassifierArn: NotRequired[str]
    InputDataConfig: NotRequired[InputDataConfigOutputTypeDef]
    OutputDataConfig: NotRequired[OutputDataConfigTypeDef]
    DataAccessRoleArn: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]
    FlywheelArn: NotRequired[str]

class DominantLanguageDetectionJobPropertiesTypeDef(TypedDict):
    JobId: NotRequired[str]
    JobArn: NotRequired[str]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    Message: NotRequired[str]
    SubmitTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    InputDataConfig: NotRequired[InputDataConfigOutputTypeDef]
    OutputDataConfig: NotRequired[OutputDataConfigTypeDef]
    DataAccessRoleArn: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]

class EntitiesDetectionJobPropertiesTypeDef(TypedDict):
    JobId: NotRequired[str]
    JobArn: NotRequired[str]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    Message: NotRequired[str]
    SubmitTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    EntityRecognizerArn: NotRequired[str]
    InputDataConfig: NotRequired[InputDataConfigOutputTypeDef]
    OutputDataConfig: NotRequired[OutputDataConfigTypeDef]
    LanguageCode: NotRequired[LanguageCodeType]
    DataAccessRoleArn: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]
    FlywheelArn: NotRequired[str]

class EventsDetectionJobPropertiesTypeDef(TypedDict):
    JobId: NotRequired[str]
    JobArn: NotRequired[str]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    Message: NotRequired[str]
    SubmitTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    InputDataConfig: NotRequired[InputDataConfigOutputTypeDef]
    OutputDataConfig: NotRequired[OutputDataConfigTypeDef]
    LanguageCode: NotRequired[LanguageCodeType]
    DataAccessRoleArn: NotRequired[str]
    TargetEventTypes: NotRequired[List[str]]

class KeyPhrasesDetectionJobPropertiesTypeDef(TypedDict):
    JobId: NotRequired[str]
    JobArn: NotRequired[str]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    Message: NotRequired[str]
    SubmitTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    InputDataConfig: NotRequired[InputDataConfigOutputTypeDef]
    OutputDataConfig: NotRequired[OutputDataConfigTypeDef]
    LanguageCode: NotRequired[LanguageCodeType]
    DataAccessRoleArn: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]

class PiiEntitiesDetectionJobPropertiesTypeDef(TypedDict):
    JobId: NotRequired[str]
    JobArn: NotRequired[str]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    Message: NotRequired[str]
    SubmitTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    InputDataConfig: NotRequired[InputDataConfigOutputTypeDef]
    OutputDataConfig: NotRequired[PiiOutputDataConfigTypeDef]
    RedactionConfig: NotRequired[RedactionConfigOutputTypeDef]
    LanguageCode: NotRequired[LanguageCodeType]
    DataAccessRoleArn: NotRequired[str]
    Mode: NotRequired[PiiEntitiesDetectionModeType]

class SentimentDetectionJobPropertiesTypeDef(TypedDict):
    JobId: NotRequired[str]
    JobArn: NotRequired[str]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    Message: NotRequired[str]
    SubmitTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    InputDataConfig: NotRequired[InputDataConfigOutputTypeDef]
    OutputDataConfig: NotRequired[OutputDataConfigTypeDef]
    LanguageCode: NotRequired[LanguageCodeType]
    DataAccessRoleArn: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]

class TargetedSentimentDetectionJobPropertiesTypeDef(TypedDict):
    JobId: NotRequired[str]
    JobArn: NotRequired[str]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    Message: NotRequired[str]
    SubmitTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    InputDataConfig: NotRequired[InputDataConfigOutputTypeDef]
    OutputDataConfig: NotRequired[OutputDataConfigTypeDef]
    LanguageCode: NotRequired[LanguageCodeType]
    DataAccessRoleArn: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]

class TopicsDetectionJobPropertiesTypeDef(TypedDict):
    JobId: NotRequired[str]
    JobArn: NotRequired[str]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    Message: NotRequired[str]
    SubmitTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    InputDataConfig: NotRequired[InputDataConfigOutputTypeDef]
    OutputDataConfig: NotRequired[OutputDataConfigTypeDef]
    NumberOfTopics: NotRequired[int]
    DataAccessRoleArn: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]

class ClassifyDocumentResponseTypeDef(TypedDict):
    Classes: List[DocumentClassTypeDef]
    Labels: List[DocumentLabelTypeDef]
    DocumentMetadata: DocumentMetadataTypeDef
    DocumentType: List[DocumentTypeListItemTypeDef]
    Errors: List[ErrorsListItemTypeDef]
    Warnings: List[WarningsListItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TaskConfigOutputTypeDef(TypedDict):
    LanguageCode: LanguageCodeType
    DocumentClassificationConfig: NotRequired[DocumentClassificationConfigOutputTypeDef]
    EntityRecognitionConfig: NotRequired[EntityRecognitionConfigOutputTypeDef]

EntityRecognitionConfigUnionTypeDef = Union[
    EntityRecognitionConfigTypeDef, EntityRecognitionConfigOutputTypeDef
]

class EntityRecognizerMetadataTypeDef(TypedDict):
    NumberOfTrainedDocuments: NotRequired[int]
    NumberOfTestDocuments: NotRequired[int]
    EvaluationMetrics: NotRequired[EntityRecognizerEvaluationMetricsTypeDef]
    EntityTypes: NotRequired[List[EntityRecognizerMetadataEntityTypesListItemTypeDef]]

class DescribeFlywheelIterationResponseTypeDef(TypedDict):
    FlywheelIterationProperties: FlywheelIterationPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListFlywheelIterationHistoryResponseTypeDef(TypedDict):
    FlywheelIterationPropertiesList: List[FlywheelIterationPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

BlockTypeDef = TypedDict(
    "BlockTypeDef",
    {
        "Id": NotRequired[str],
        "BlockType": NotRequired[BlockTypeType],
        "Text": NotRequired[str],
        "Page": NotRequired[int],
        "Geometry": NotRequired[GeometryTypeDef],
        "Relationships": NotRequired[List[RelationshipsListItemTypeDef]],
    },
)

class BatchDetectSyntaxItemResultTypeDef(TypedDict):
    Index: NotRequired[int]
    SyntaxTokens: NotRequired[List[SyntaxTokenTypeDef]]

class DetectSyntaxResponseTypeDef(TypedDict):
    SyntaxTokens: List[SyntaxTokenTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DetectToxicContentResponseTypeDef(TypedDict):
    ResultList: List[ToxicLabelsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEntityRecognizerRequestRequestTypeDef(TypedDict):
    RecognizerName: str
    DataAccessRoleArn: str
    InputDataConfig: EntityRecognizerInputDataConfigTypeDef
    LanguageCode: LanguageCodeType
    VersionName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientRequestToken: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    ModelKmsKeyId: NotRequired[str]
    ModelPolicy: NotRequired[str]

class TargetedSentimentEntityTypeDef(TypedDict):
    DescriptiveMentionIndex: NotRequired[List[int]]
    Mentions: NotRequired[List[TargetedSentimentMentionTypeDef]]

class BatchDetectEntitiesItemResultTypeDef(TypedDict):
    Index: NotRequired[int]
    Entities: NotRequired[List[EntityTypeDef]]

class UpdateFlywheelRequestRequestTypeDef(TypedDict):
    FlywheelArn: str
    ActiveModelArn: NotRequired[str]
    DataAccessRoleArn: NotRequired[str]
    DataSecurityConfig: NotRequired[UpdateDataSecurityConfigTypeDef]

class CreateDatasetRequestRequestTypeDef(TypedDict):
    FlywheelArn: str
    DatasetName: str
    InputDataConfig: DatasetInputDataConfigTypeDef
    DatasetType: NotRequired[DatasetTypeType]
    Description: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class DescribeDocumentClassifierResponseTypeDef(TypedDict):
    DocumentClassifierProperties: DocumentClassifierPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDocumentClassifiersResponseTypeDef(TypedDict):
    DocumentClassifierPropertiesList: List[DocumentClassifierPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateDocumentClassifierRequestRequestTypeDef(TypedDict):
    DocumentClassifierName: str
    DataAccessRoleArn: str
    InputDataConfig: DocumentClassifierInputDataConfigTypeDef
    LanguageCode: LanguageCodeType
    VersionName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    OutputDataConfig: NotRequired[DocumentClassifierOutputDataConfigTypeDef]
    ClientRequestToken: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    Mode: NotRequired[DocumentClassifierModeType]
    ModelKmsKeyId: NotRequired[str]
    ModelPolicy: NotRequired[str]

class StartDocumentClassificationJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    DataAccessRoleArn: str
    JobName: NotRequired[str]
    DocumentClassifierArn: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    FlywheelArn: NotRequired[str]

class StartDominantLanguageDetectionJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    DataAccessRoleArn: str
    JobName: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class StartEntitiesDetectionJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    DataAccessRoleArn: str
    LanguageCode: LanguageCodeType
    JobName: NotRequired[str]
    EntityRecognizerArn: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    FlywheelArn: NotRequired[str]

class StartEventsDetectionJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    DataAccessRoleArn: str
    LanguageCode: LanguageCodeType
    TargetEventTypes: Sequence[str]
    JobName: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class StartKeyPhrasesDetectionJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    DataAccessRoleArn: str
    LanguageCode: LanguageCodeType
    JobName: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class StartPiiEntitiesDetectionJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    Mode: PiiEntitiesDetectionModeType
    DataAccessRoleArn: str
    LanguageCode: LanguageCodeType
    RedactionConfig: NotRequired[RedactionConfigTypeDef]
    JobName: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class StartSentimentDetectionJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    DataAccessRoleArn: str
    LanguageCode: LanguageCodeType
    JobName: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class StartTargetedSentimentDetectionJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    DataAccessRoleArn: str
    LanguageCode: LanguageCodeType
    JobName: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class StartTopicsDetectionJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    DataAccessRoleArn: str
    JobName: NotRequired[str]
    NumberOfTopics: NotRequired[int]
    ClientRequestToken: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class DescribeDocumentClassificationJobResponseTypeDef(TypedDict):
    DocumentClassificationJobProperties: DocumentClassificationJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDocumentClassificationJobsResponseTypeDef(TypedDict):
    DocumentClassificationJobPropertiesList: List[DocumentClassificationJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeDominantLanguageDetectionJobResponseTypeDef(TypedDict):
    DominantLanguageDetectionJobProperties: DominantLanguageDetectionJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDominantLanguageDetectionJobsResponseTypeDef(TypedDict):
    DominantLanguageDetectionJobPropertiesList: List[DominantLanguageDetectionJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeEntitiesDetectionJobResponseTypeDef(TypedDict):
    EntitiesDetectionJobProperties: EntitiesDetectionJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListEntitiesDetectionJobsResponseTypeDef(TypedDict):
    EntitiesDetectionJobPropertiesList: List[EntitiesDetectionJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeEventsDetectionJobResponseTypeDef(TypedDict):
    EventsDetectionJobProperties: EventsDetectionJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListEventsDetectionJobsResponseTypeDef(TypedDict):
    EventsDetectionJobPropertiesList: List[EventsDetectionJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeKeyPhrasesDetectionJobResponseTypeDef(TypedDict):
    KeyPhrasesDetectionJobProperties: KeyPhrasesDetectionJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListKeyPhrasesDetectionJobsResponseTypeDef(TypedDict):
    KeyPhrasesDetectionJobPropertiesList: List[KeyPhrasesDetectionJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribePiiEntitiesDetectionJobResponseTypeDef(TypedDict):
    PiiEntitiesDetectionJobProperties: PiiEntitiesDetectionJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListPiiEntitiesDetectionJobsResponseTypeDef(TypedDict):
    PiiEntitiesDetectionJobPropertiesList: List[PiiEntitiesDetectionJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeSentimentDetectionJobResponseTypeDef(TypedDict):
    SentimentDetectionJobProperties: SentimentDetectionJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSentimentDetectionJobsResponseTypeDef(TypedDict):
    SentimentDetectionJobPropertiesList: List[SentimentDetectionJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeTargetedSentimentDetectionJobResponseTypeDef(TypedDict):
    TargetedSentimentDetectionJobProperties: TargetedSentimentDetectionJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListTargetedSentimentDetectionJobsResponseTypeDef(TypedDict):
    TargetedSentimentDetectionJobPropertiesList: List[
        TargetedSentimentDetectionJobPropertiesTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeTopicsDetectionJobResponseTypeDef(TypedDict):
    TopicsDetectionJobProperties: TopicsDetectionJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListTopicsDetectionJobsResponseTypeDef(TypedDict):
    TopicsDetectionJobPropertiesList: List[TopicsDetectionJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class FlywheelPropertiesTypeDef(TypedDict):
    FlywheelArn: NotRequired[str]
    ActiveModelArn: NotRequired[str]
    DataAccessRoleArn: NotRequired[str]
    TaskConfig: NotRequired[TaskConfigOutputTypeDef]
    DataLakeS3Uri: NotRequired[str]
    DataSecurityConfig: NotRequired[DataSecurityConfigOutputTypeDef]
    Status: NotRequired[FlywheelStatusType]
    ModelType: NotRequired[ModelTypeType]
    Message: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    LatestFlywheelIteration: NotRequired[str]

class TaskConfigTypeDef(TypedDict):
    LanguageCode: LanguageCodeType
    DocumentClassificationConfig: NotRequired[DocumentClassificationConfigUnionTypeDef]
    EntityRecognitionConfig: NotRequired[EntityRecognitionConfigUnionTypeDef]

class EntityRecognizerPropertiesTypeDef(TypedDict):
    EntityRecognizerArn: NotRequired[str]
    LanguageCode: NotRequired[LanguageCodeType]
    Status: NotRequired[ModelStatusType]
    Message: NotRequired[str]
    SubmitTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    TrainingStartTime: NotRequired[datetime]
    TrainingEndTime: NotRequired[datetime]
    InputDataConfig: NotRequired[EntityRecognizerInputDataConfigOutputTypeDef]
    RecognizerMetadata: NotRequired[EntityRecognizerMetadataTypeDef]
    DataAccessRoleArn: NotRequired[str]
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]
    ModelKmsKeyId: NotRequired[str]
    VersionName: NotRequired[str]
    SourceModelArn: NotRequired[str]
    FlywheelArn: NotRequired[str]
    OutputDataConfig: NotRequired[EntityRecognizerOutputDataConfigTypeDef]

class DetectEntitiesResponseTypeDef(TypedDict):
    Entities: List[EntityTypeDef]
    DocumentMetadata: DocumentMetadataTypeDef
    DocumentType: List[DocumentTypeListItemTypeDef]
    Blocks: List[BlockTypeDef]
    Errors: List[ErrorsListItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDetectSyntaxResponseTypeDef(TypedDict):
    ResultList: List[BatchDetectSyntaxItemResultTypeDef]
    ErrorList: List[BatchItemErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDetectTargetedSentimentItemResultTypeDef(TypedDict):
    Index: NotRequired[int]
    Entities: NotRequired[List[TargetedSentimentEntityTypeDef]]

class DetectTargetedSentimentResponseTypeDef(TypedDict):
    Entities: List[TargetedSentimentEntityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDetectEntitiesResponseTypeDef(TypedDict):
    ResultList: List[BatchDetectEntitiesItemResultTypeDef]
    ErrorList: List[BatchItemErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeFlywheelResponseTypeDef(TypedDict):
    FlywheelProperties: FlywheelPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateFlywheelResponseTypeDef(TypedDict):
    FlywheelProperties: FlywheelPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFlywheelRequestRequestTypeDef(TypedDict):
    FlywheelName: str
    DataAccessRoleArn: str
    DataLakeS3Uri: str
    ActiveModelArn: NotRequired[str]
    TaskConfig: NotRequired[TaskConfigTypeDef]
    ModelType: NotRequired[ModelTypeType]
    DataSecurityConfig: NotRequired[DataSecurityConfigTypeDef]
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class DescribeEntityRecognizerResponseTypeDef(TypedDict):
    EntityRecognizerProperties: EntityRecognizerPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListEntityRecognizersResponseTypeDef(TypedDict):
    EntityRecognizerPropertiesList: List[EntityRecognizerPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class BatchDetectTargetedSentimentResponseTypeDef(TypedDict):
    ResultList: List[BatchDetectTargetedSentimentItemResultTypeDef]
    ErrorList: List[BatchItemErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
