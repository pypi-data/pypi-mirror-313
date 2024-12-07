"""
Type annotations for transcribe service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transcribe/type_defs/)

Usage::

    ```python
    from mypy_boto3_transcribe.type_defs import AbsoluteTimeRangeTypeDef

    data: AbsoluteTimeRangeTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    BaseModelNameType,
    CallAnalyticsJobStatusType,
    CallAnalyticsSkippedReasonCodeType,
    CLMLanguageCodeType,
    InputTypeType,
    LanguageCodeType,
    MediaFormatType,
    MedicalScribeJobStatusType,
    MedicalScribeParticipantRoleType,
    ModelStatusType,
    OutputLocationTypeType,
    ParticipantRoleType,
    PiiEntityTypeType,
    RedactionOutputType,
    SentimentValueType,
    SubtitleFormatType,
    TranscriptionJobStatusType,
    TypeType,
    VocabularyFilterMethodType,
    VocabularyStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AbsoluteTimeRangeTypeDef",
    "CallAnalyticsJobDetailsTypeDef",
    "CallAnalyticsJobSettingsOutputTypeDef",
    "CallAnalyticsJobSettingsTypeDef",
    "CallAnalyticsJobSummaryTypeDef",
    "CallAnalyticsJobTypeDef",
    "CallAnalyticsSkippedFeatureTypeDef",
    "CategoryPropertiesTypeDef",
    "ChannelDefinitionTypeDef",
    "ContentRedactionOutputTypeDef",
    "ContentRedactionTypeDef",
    "ContentRedactionUnionTypeDef",
    "CreateCallAnalyticsCategoryRequestRequestTypeDef",
    "CreateCallAnalyticsCategoryResponseTypeDef",
    "CreateLanguageModelRequestRequestTypeDef",
    "CreateLanguageModelResponseTypeDef",
    "CreateMedicalVocabularyRequestRequestTypeDef",
    "CreateMedicalVocabularyResponseTypeDef",
    "CreateVocabularyFilterRequestRequestTypeDef",
    "CreateVocabularyFilterResponseTypeDef",
    "CreateVocabularyRequestRequestTypeDef",
    "CreateVocabularyResponseTypeDef",
    "DeleteCallAnalyticsCategoryRequestRequestTypeDef",
    "DeleteCallAnalyticsJobRequestRequestTypeDef",
    "DeleteLanguageModelRequestRequestTypeDef",
    "DeleteMedicalScribeJobRequestRequestTypeDef",
    "DeleteMedicalTranscriptionJobRequestRequestTypeDef",
    "DeleteMedicalVocabularyRequestRequestTypeDef",
    "DeleteTranscriptionJobRequestRequestTypeDef",
    "DeleteVocabularyFilterRequestRequestTypeDef",
    "DeleteVocabularyRequestRequestTypeDef",
    "DescribeLanguageModelRequestRequestTypeDef",
    "DescribeLanguageModelResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetCallAnalyticsCategoryRequestRequestTypeDef",
    "GetCallAnalyticsCategoryResponseTypeDef",
    "GetCallAnalyticsJobRequestRequestTypeDef",
    "GetCallAnalyticsJobResponseTypeDef",
    "GetMedicalScribeJobRequestRequestTypeDef",
    "GetMedicalScribeJobResponseTypeDef",
    "GetMedicalTranscriptionJobRequestRequestTypeDef",
    "GetMedicalTranscriptionJobResponseTypeDef",
    "GetMedicalVocabularyRequestRequestTypeDef",
    "GetMedicalVocabularyResponseTypeDef",
    "GetTranscriptionJobRequestRequestTypeDef",
    "GetTranscriptionJobResponseTypeDef",
    "GetVocabularyFilterRequestRequestTypeDef",
    "GetVocabularyFilterResponseTypeDef",
    "GetVocabularyRequestRequestTypeDef",
    "GetVocabularyResponseTypeDef",
    "InputDataConfigTypeDef",
    "InterruptionFilterTypeDef",
    "JobExecutionSettingsTypeDef",
    "LanguageCodeItemTypeDef",
    "LanguageIdSettingsTypeDef",
    "LanguageModelTypeDef",
    "ListCallAnalyticsCategoriesRequestRequestTypeDef",
    "ListCallAnalyticsCategoriesResponseTypeDef",
    "ListCallAnalyticsJobsRequestRequestTypeDef",
    "ListCallAnalyticsJobsResponseTypeDef",
    "ListLanguageModelsRequestRequestTypeDef",
    "ListLanguageModelsResponseTypeDef",
    "ListMedicalScribeJobsRequestRequestTypeDef",
    "ListMedicalScribeJobsResponseTypeDef",
    "ListMedicalTranscriptionJobsRequestRequestTypeDef",
    "ListMedicalTranscriptionJobsResponseTypeDef",
    "ListMedicalVocabulariesRequestRequestTypeDef",
    "ListMedicalVocabulariesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTranscriptionJobsRequestRequestTypeDef",
    "ListTranscriptionJobsResponseTypeDef",
    "ListVocabulariesRequestRequestTypeDef",
    "ListVocabulariesResponseTypeDef",
    "ListVocabularyFiltersRequestRequestTypeDef",
    "ListVocabularyFiltersResponseTypeDef",
    "MediaTypeDef",
    "MedicalScribeChannelDefinitionTypeDef",
    "MedicalScribeJobSummaryTypeDef",
    "MedicalScribeJobTypeDef",
    "MedicalScribeOutputTypeDef",
    "MedicalScribeSettingsTypeDef",
    "MedicalTranscriptTypeDef",
    "MedicalTranscriptionJobSummaryTypeDef",
    "MedicalTranscriptionJobTypeDef",
    "MedicalTranscriptionSettingTypeDef",
    "ModelSettingsTypeDef",
    "NonTalkTimeFilterTypeDef",
    "RelativeTimeRangeTypeDef",
    "ResponseMetadataTypeDef",
    "RuleOutputTypeDef",
    "RuleTypeDef",
    "RuleUnionTypeDef",
    "SentimentFilterOutputTypeDef",
    "SentimentFilterTypeDef",
    "SentimentFilterUnionTypeDef",
    "SettingsTypeDef",
    "StartCallAnalyticsJobRequestRequestTypeDef",
    "StartCallAnalyticsJobResponseTypeDef",
    "StartMedicalScribeJobRequestRequestTypeDef",
    "StartMedicalScribeJobResponseTypeDef",
    "StartMedicalTranscriptionJobRequestRequestTypeDef",
    "StartMedicalTranscriptionJobResponseTypeDef",
    "StartTranscriptionJobRequestRequestTypeDef",
    "StartTranscriptionJobResponseTypeDef",
    "SubtitlesOutputTypeDef",
    "SubtitlesTypeDef",
    "SummarizationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "ToxicityDetectionSettingsOutputTypeDef",
    "ToxicityDetectionSettingsTypeDef",
    "ToxicityDetectionSettingsUnionTypeDef",
    "TranscriptFilterOutputTypeDef",
    "TranscriptFilterTypeDef",
    "TranscriptFilterUnionTypeDef",
    "TranscriptTypeDef",
    "TranscriptionJobSummaryTypeDef",
    "TranscriptionJobTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCallAnalyticsCategoryRequestRequestTypeDef",
    "UpdateCallAnalyticsCategoryResponseTypeDef",
    "UpdateMedicalVocabularyRequestRequestTypeDef",
    "UpdateMedicalVocabularyResponseTypeDef",
    "UpdateVocabularyFilterRequestRequestTypeDef",
    "UpdateVocabularyFilterResponseTypeDef",
    "UpdateVocabularyRequestRequestTypeDef",
    "UpdateVocabularyResponseTypeDef",
    "VocabularyFilterInfoTypeDef",
    "VocabularyInfoTypeDef",
)

class AbsoluteTimeRangeTypeDef(TypedDict):
    StartTime: NotRequired[int]
    EndTime: NotRequired[int]
    First: NotRequired[int]
    Last: NotRequired[int]

class CallAnalyticsSkippedFeatureTypeDef(TypedDict):
    Feature: NotRequired[Literal["GENERATIVE_SUMMARIZATION"]]
    ReasonCode: NotRequired[CallAnalyticsSkippedReasonCodeType]
    Message: NotRequired[str]

class ContentRedactionOutputTypeDef(TypedDict):
    RedactionType: Literal["PII"]
    RedactionOutput: RedactionOutputType
    PiiEntityTypes: NotRequired[List[PiiEntityTypeType]]

class LanguageIdSettingsTypeDef(TypedDict):
    VocabularyName: NotRequired[str]
    VocabularyFilterName: NotRequired[str]
    LanguageModelName: NotRequired[str]

class SummarizationTypeDef(TypedDict):
    GenerateAbstractiveSummary: bool

class ChannelDefinitionTypeDef(TypedDict):
    ChannelId: NotRequired[int]
    ParticipantRole: NotRequired[ParticipantRoleType]

class MediaTypeDef(TypedDict):
    MediaFileUri: NotRequired[str]
    RedactedMediaFileUri: NotRequired[str]

class TranscriptTypeDef(TypedDict):
    TranscriptFileUri: NotRequired[str]
    RedactedTranscriptFileUri: NotRequired[str]

class ContentRedactionTypeDef(TypedDict):
    RedactionType: Literal["PII"]
    RedactionOutput: RedactionOutputType
    PiiEntityTypes: NotRequired[Sequence[PiiEntityTypeType]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class InputDataConfigTypeDef(TypedDict):
    S3Uri: str
    DataAccessRoleArn: str
    TuningDataS3Uri: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class DeleteCallAnalyticsCategoryRequestRequestTypeDef(TypedDict):
    CategoryName: str

class DeleteCallAnalyticsJobRequestRequestTypeDef(TypedDict):
    CallAnalyticsJobName: str

class DeleteLanguageModelRequestRequestTypeDef(TypedDict):
    ModelName: str

class DeleteMedicalScribeJobRequestRequestTypeDef(TypedDict):
    MedicalScribeJobName: str

class DeleteMedicalTranscriptionJobRequestRequestTypeDef(TypedDict):
    MedicalTranscriptionJobName: str

class DeleteMedicalVocabularyRequestRequestTypeDef(TypedDict):
    VocabularyName: str

class DeleteTranscriptionJobRequestRequestTypeDef(TypedDict):
    TranscriptionJobName: str

class DeleteVocabularyFilterRequestRequestTypeDef(TypedDict):
    VocabularyFilterName: str

class DeleteVocabularyRequestRequestTypeDef(TypedDict):
    VocabularyName: str

class DescribeLanguageModelRequestRequestTypeDef(TypedDict):
    ModelName: str

class GetCallAnalyticsCategoryRequestRequestTypeDef(TypedDict):
    CategoryName: str

class GetCallAnalyticsJobRequestRequestTypeDef(TypedDict):
    CallAnalyticsJobName: str

class GetMedicalScribeJobRequestRequestTypeDef(TypedDict):
    MedicalScribeJobName: str

class GetMedicalTranscriptionJobRequestRequestTypeDef(TypedDict):
    MedicalTranscriptionJobName: str

class GetMedicalVocabularyRequestRequestTypeDef(TypedDict):
    VocabularyName: str

class GetTranscriptionJobRequestRequestTypeDef(TypedDict):
    TranscriptionJobName: str

class GetVocabularyFilterRequestRequestTypeDef(TypedDict):
    VocabularyFilterName: str

class GetVocabularyRequestRequestTypeDef(TypedDict):
    VocabularyName: str

class RelativeTimeRangeTypeDef(TypedDict):
    StartPercentage: NotRequired[int]
    EndPercentage: NotRequired[int]
    First: NotRequired[int]
    Last: NotRequired[int]

class JobExecutionSettingsTypeDef(TypedDict):
    AllowDeferredExecution: NotRequired[bool]
    DataAccessRoleArn: NotRequired[str]

class LanguageCodeItemTypeDef(TypedDict):
    LanguageCode: NotRequired[LanguageCodeType]
    DurationInSeconds: NotRequired[float]

class ListCallAnalyticsCategoriesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListCallAnalyticsJobsRequestRequestTypeDef(TypedDict):
    Status: NotRequired[CallAnalyticsJobStatusType]
    JobNameContains: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListLanguageModelsRequestRequestTypeDef(TypedDict):
    StatusEquals: NotRequired[ModelStatusType]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListMedicalScribeJobsRequestRequestTypeDef(TypedDict):
    Status: NotRequired[MedicalScribeJobStatusType]
    JobNameContains: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class MedicalScribeJobSummaryTypeDef(TypedDict):
    MedicalScribeJobName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    StartTime: NotRequired[datetime]
    CompletionTime: NotRequired[datetime]
    LanguageCode: NotRequired[Literal["en-US"]]
    MedicalScribeJobStatus: NotRequired[MedicalScribeJobStatusType]
    FailureReason: NotRequired[str]

class ListMedicalTranscriptionJobsRequestRequestTypeDef(TypedDict):
    Status: NotRequired[TranscriptionJobStatusType]
    JobNameContains: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

MedicalTranscriptionJobSummaryTypeDef = TypedDict(
    "MedicalTranscriptionJobSummaryTypeDef",
    {
        "MedicalTranscriptionJobName": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "StartTime": NotRequired[datetime],
        "CompletionTime": NotRequired[datetime],
        "LanguageCode": NotRequired[LanguageCodeType],
        "TranscriptionJobStatus": NotRequired[TranscriptionJobStatusType],
        "FailureReason": NotRequired[str],
        "OutputLocationType": NotRequired[OutputLocationTypeType],
        "Specialty": NotRequired[Literal["PRIMARYCARE"]],
        "ContentIdentificationType": NotRequired[Literal["PHI"]],
        "Type": NotRequired[TypeType],
    },
)

class ListMedicalVocabulariesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    StateEquals: NotRequired[VocabularyStateType]
    NameContains: NotRequired[str]

class VocabularyInfoTypeDef(TypedDict):
    VocabularyName: NotRequired[str]
    LanguageCode: NotRequired[LanguageCodeType]
    LastModifiedTime: NotRequired[datetime]
    VocabularyState: NotRequired[VocabularyStateType]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class ListTranscriptionJobsRequestRequestTypeDef(TypedDict):
    Status: NotRequired[TranscriptionJobStatusType]
    JobNameContains: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListVocabulariesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    StateEquals: NotRequired[VocabularyStateType]
    NameContains: NotRequired[str]

class ListVocabularyFiltersRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]

class VocabularyFilterInfoTypeDef(TypedDict):
    VocabularyFilterName: NotRequired[str]
    LanguageCode: NotRequired[LanguageCodeType]
    LastModifiedTime: NotRequired[datetime]

class MedicalScribeChannelDefinitionTypeDef(TypedDict):
    ChannelId: int
    ParticipantRole: MedicalScribeParticipantRoleType

class MedicalScribeOutputTypeDef(TypedDict):
    TranscriptFileUri: str
    ClinicalDocumentUri: str

class MedicalScribeSettingsTypeDef(TypedDict):
    ShowSpeakerLabels: NotRequired[bool]
    MaxSpeakerLabels: NotRequired[int]
    ChannelIdentification: NotRequired[bool]
    VocabularyName: NotRequired[str]
    VocabularyFilterName: NotRequired[str]
    VocabularyFilterMethod: NotRequired[VocabularyFilterMethodType]

class MedicalTranscriptTypeDef(TypedDict):
    TranscriptFileUri: NotRequired[str]

class MedicalTranscriptionSettingTypeDef(TypedDict):
    ShowSpeakerLabels: NotRequired[bool]
    MaxSpeakerLabels: NotRequired[int]
    ChannelIdentification: NotRequired[bool]
    ShowAlternatives: NotRequired[bool]
    MaxAlternatives: NotRequired[int]
    VocabularyName: NotRequired[str]

class ModelSettingsTypeDef(TypedDict):
    LanguageModelName: NotRequired[str]

class SettingsTypeDef(TypedDict):
    VocabularyName: NotRequired[str]
    ShowSpeakerLabels: NotRequired[bool]
    MaxSpeakerLabels: NotRequired[int]
    ChannelIdentification: NotRequired[bool]
    ShowAlternatives: NotRequired[bool]
    MaxAlternatives: NotRequired[int]
    VocabularyFilterName: NotRequired[str]
    VocabularyFilterMethod: NotRequired[VocabularyFilterMethodType]

class SubtitlesTypeDef(TypedDict):
    Formats: NotRequired[Sequence[SubtitleFormatType]]
    OutputStartIndex: NotRequired[int]

class SubtitlesOutputTypeDef(TypedDict):
    Formats: NotRequired[List[SubtitleFormatType]]
    SubtitleFileUris: NotRequired[List[str]]
    OutputStartIndex: NotRequired[int]

class ToxicityDetectionSettingsOutputTypeDef(TypedDict):
    ToxicityCategories: List[Literal["ALL"]]

class ToxicityDetectionSettingsTypeDef(TypedDict):
    ToxicityCategories: Sequence[Literal["ALL"]]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateMedicalVocabularyRequestRequestTypeDef(TypedDict):
    VocabularyName: str
    LanguageCode: LanguageCodeType
    VocabularyFileUri: str

class UpdateVocabularyFilterRequestRequestTypeDef(TypedDict):
    VocabularyFilterName: str
    Words: NotRequired[Sequence[str]]
    VocabularyFilterFileUri: NotRequired[str]
    DataAccessRoleArn: NotRequired[str]

class UpdateVocabularyRequestRequestTypeDef(TypedDict):
    VocabularyName: str
    LanguageCode: LanguageCodeType
    Phrases: NotRequired[Sequence[str]]
    VocabularyFileUri: NotRequired[str]
    DataAccessRoleArn: NotRequired[str]

class CallAnalyticsJobDetailsTypeDef(TypedDict):
    Skipped: NotRequired[List[CallAnalyticsSkippedFeatureTypeDef]]

class CallAnalyticsJobSettingsOutputTypeDef(TypedDict):
    VocabularyName: NotRequired[str]
    VocabularyFilterName: NotRequired[str]
    VocabularyFilterMethod: NotRequired[VocabularyFilterMethodType]
    LanguageModelName: NotRequired[str]
    ContentRedaction: NotRequired[ContentRedactionOutputTypeDef]
    LanguageOptions: NotRequired[List[LanguageCodeType]]
    LanguageIdSettings: NotRequired[Dict[LanguageCodeType, LanguageIdSettingsTypeDef]]
    Summarization: NotRequired[SummarizationTypeDef]

ContentRedactionUnionTypeDef = Union[ContentRedactionTypeDef, ContentRedactionOutputTypeDef]

class CreateMedicalVocabularyResponseTypeDef(TypedDict):
    VocabularyName: str
    LanguageCode: LanguageCodeType
    VocabularyState: VocabularyStateType
    LastModifiedTime: datetime
    FailureReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateVocabularyFilterResponseTypeDef(TypedDict):
    VocabularyFilterName: str
    LanguageCode: LanguageCodeType
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateVocabularyResponseTypeDef(TypedDict):
    VocabularyName: str
    LanguageCode: LanguageCodeType
    VocabularyState: VocabularyStateType
    LastModifiedTime: datetime
    FailureReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetMedicalVocabularyResponseTypeDef(TypedDict):
    VocabularyName: str
    LanguageCode: LanguageCodeType
    VocabularyState: VocabularyStateType
    LastModifiedTime: datetime
    FailureReason: str
    DownloadUri: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetVocabularyFilterResponseTypeDef(TypedDict):
    VocabularyFilterName: str
    LanguageCode: LanguageCodeType
    LastModifiedTime: datetime
    DownloadUri: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetVocabularyResponseTypeDef(TypedDict):
    VocabularyName: str
    LanguageCode: LanguageCodeType
    VocabularyState: VocabularyStateType
    LastModifiedTime: datetime
    FailureReason: str
    DownloadUri: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMedicalVocabularyResponseTypeDef(TypedDict):
    VocabularyName: str
    LanguageCode: LanguageCodeType
    LastModifiedTime: datetime
    VocabularyState: VocabularyStateType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateVocabularyFilterResponseTypeDef(TypedDict):
    VocabularyFilterName: str
    LanguageCode: LanguageCodeType
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateVocabularyResponseTypeDef(TypedDict):
    VocabularyName: str
    LanguageCode: LanguageCodeType
    LastModifiedTime: datetime
    VocabularyState: VocabularyStateType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLanguageModelResponseTypeDef(TypedDict):
    LanguageCode: CLMLanguageCodeType
    BaseModelName: BaseModelNameType
    ModelName: str
    InputDataConfig: InputDataConfigTypeDef
    ModelStatus: ModelStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class LanguageModelTypeDef(TypedDict):
    ModelName: NotRequired[str]
    CreateTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    LanguageCode: NotRequired[CLMLanguageCodeType]
    BaseModelName: NotRequired[BaseModelNameType]
    ModelStatus: NotRequired[ModelStatusType]
    UpgradeAvailability: NotRequired[bool]
    FailureReason: NotRequired[str]
    InputDataConfig: NotRequired[InputDataConfigTypeDef]

class CreateLanguageModelRequestRequestTypeDef(TypedDict):
    LanguageCode: CLMLanguageCodeType
    BaseModelName: BaseModelNameType
    ModelName: str
    InputDataConfig: InputDataConfigTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateMedicalVocabularyRequestRequestTypeDef(TypedDict):
    VocabularyName: str
    LanguageCode: LanguageCodeType
    VocabularyFileUri: str
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateVocabularyFilterRequestRequestTypeDef(TypedDict):
    VocabularyFilterName: str
    LanguageCode: LanguageCodeType
    Words: NotRequired[Sequence[str]]
    VocabularyFilterFileUri: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    DataAccessRoleArn: NotRequired[str]

class CreateVocabularyRequestRequestTypeDef(TypedDict):
    VocabularyName: str
    LanguageCode: LanguageCodeType
    Phrases: NotRequired[Sequence[str]]
    VocabularyFileUri: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    DataAccessRoleArn: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    ResourceArn: str
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class InterruptionFilterTypeDef(TypedDict):
    Threshold: NotRequired[int]
    ParticipantRole: NotRequired[ParticipantRoleType]
    AbsoluteTimeRange: NotRequired[AbsoluteTimeRangeTypeDef]
    RelativeTimeRange: NotRequired[RelativeTimeRangeTypeDef]
    Negate: NotRequired[bool]

class NonTalkTimeFilterTypeDef(TypedDict):
    Threshold: NotRequired[int]
    AbsoluteTimeRange: NotRequired[AbsoluteTimeRangeTypeDef]
    RelativeTimeRange: NotRequired[RelativeTimeRangeTypeDef]
    Negate: NotRequired[bool]

class SentimentFilterOutputTypeDef(TypedDict):
    Sentiments: List[SentimentValueType]
    AbsoluteTimeRange: NotRequired[AbsoluteTimeRangeTypeDef]
    RelativeTimeRange: NotRequired[RelativeTimeRangeTypeDef]
    ParticipantRole: NotRequired[ParticipantRoleType]
    Negate: NotRequired[bool]

class SentimentFilterTypeDef(TypedDict):
    Sentiments: Sequence[SentimentValueType]
    AbsoluteTimeRange: NotRequired[AbsoluteTimeRangeTypeDef]
    RelativeTimeRange: NotRequired[RelativeTimeRangeTypeDef]
    ParticipantRole: NotRequired[ParticipantRoleType]
    Negate: NotRequired[bool]

class TranscriptFilterOutputTypeDef(TypedDict):
    TranscriptFilterType: Literal["EXACT"]
    Targets: List[str]
    AbsoluteTimeRange: NotRequired[AbsoluteTimeRangeTypeDef]
    RelativeTimeRange: NotRequired[RelativeTimeRangeTypeDef]
    ParticipantRole: NotRequired[ParticipantRoleType]
    Negate: NotRequired[bool]

class TranscriptFilterTypeDef(TypedDict):
    TranscriptFilterType: Literal["EXACT"]
    Targets: Sequence[str]
    AbsoluteTimeRange: NotRequired[AbsoluteTimeRangeTypeDef]
    RelativeTimeRange: NotRequired[RelativeTimeRangeTypeDef]
    ParticipantRole: NotRequired[ParticipantRoleType]
    Negate: NotRequired[bool]

class ListMedicalScribeJobsResponseTypeDef(TypedDict):
    Status: MedicalScribeJobStatusType
    MedicalScribeJobSummaries: List[MedicalScribeJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListMedicalTranscriptionJobsResponseTypeDef(TypedDict):
    Status: TranscriptionJobStatusType
    MedicalTranscriptionJobSummaries: List[MedicalTranscriptionJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListMedicalVocabulariesResponseTypeDef(TypedDict):
    Status: VocabularyStateType
    Vocabularies: List[VocabularyInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListVocabulariesResponseTypeDef(TypedDict):
    Status: VocabularyStateType
    Vocabularies: List[VocabularyInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListVocabularyFiltersResponseTypeDef(TypedDict):
    VocabularyFilters: List[VocabularyFilterInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class MedicalScribeJobTypeDef(TypedDict):
    MedicalScribeJobName: NotRequired[str]
    MedicalScribeJobStatus: NotRequired[MedicalScribeJobStatusType]
    LanguageCode: NotRequired[Literal["en-US"]]
    Media: NotRequired[MediaTypeDef]
    MedicalScribeOutput: NotRequired[MedicalScribeOutputTypeDef]
    StartTime: NotRequired[datetime]
    CreationTime: NotRequired[datetime]
    CompletionTime: NotRequired[datetime]
    FailureReason: NotRequired[str]
    Settings: NotRequired[MedicalScribeSettingsTypeDef]
    DataAccessRoleArn: NotRequired[str]
    ChannelDefinitions: NotRequired[List[MedicalScribeChannelDefinitionTypeDef]]
    Tags: NotRequired[List[TagTypeDef]]

class StartMedicalScribeJobRequestRequestTypeDef(TypedDict):
    MedicalScribeJobName: str
    Media: MediaTypeDef
    OutputBucketName: str
    DataAccessRoleArn: str
    Settings: MedicalScribeSettingsTypeDef
    OutputEncryptionKMSKeyId: NotRequired[str]
    KMSEncryptionContext: NotRequired[Mapping[str, str]]
    ChannelDefinitions: NotRequired[Sequence[MedicalScribeChannelDefinitionTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]

MedicalTranscriptionJobTypeDef = TypedDict(
    "MedicalTranscriptionJobTypeDef",
    {
        "MedicalTranscriptionJobName": NotRequired[str],
        "TranscriptionJobStatus": NotRequired[TranscriptionJobStatusType],
        "LanguageCode": NotRequired[LanguageCodeType],
        "MediaSampleRateHertz": NotRequired[int],
        "MediaFormat": NotRequired[MediaFormatType],
        "Media": NotRequired[MediaTypeDef],
        "Transcript": NotRequired[MedicalTranscriptTypeDef],
        "StartTime": NotRequired[datetime],
        "CreationTime": NotRequired[datetime],
        "CompletionTime": NotRequired[datetime],
        "FailureReason": NotRequired[str],
        "Settings": NotRequired[MedicalTranscriptionSettingTypeDef],
        "ContentIdentificationType": NotRequired[Literal["PHI"]],
        "Specialty": NotRequired[Literal["PRIMARYCARE"]],
        "Type": NotRequired[TypeType],
        "Tags": NotRequired[List[TagTypeDef]],
    },
)
StartMedicalTranscriptionJobRequestRequestTypeDef = TypedDict(
    "StartMedicalTranscriptionJobRequestRequestTypeDef",
    {
        "MedicalTranscriptionJobName": str,
        "LanguageCode": LanguageCodeType,
        "Media": MediaTypeDef,
        "OutputBucketName": str,
        "Specialty": Literal["PRIMARYCARE"],
        "Type": TypeType,
        "MediaSampleRateHertz": NotRequired[int],
        "MediaFormat": NotRequired[MediaFormatType],
        "OutputKey": NotRequired[str],
        "OutputEncryptionKMSKeyId": NotRequired[str],
        "KMSEncryptionContext": NotRequired[Mapping[str, str]],
        "Settings": NotRequired[MedicalTranscriptionSettingTypeDef],
        "ContentIdentificationType": NotRequired[Literal["PHI"]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

class TranscriptionJobSummaryTypeDef(TypedDict):
    TranscriptionJobName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    StartTime: NotRequired[datetime]
    CompletionTime: NotRequired[datetime]
    LanguageCode: NotRequired[LanguageCodeType]
    TranscriptionJobStatus: NotRequired[TranscriptionJobStatusType]
    FailureReason: NotRequired[str]
    OutputLocationType: NotRequired[OutputLocationTypeType]
    ContentRedaction: NotRequired[ContentRedactionOutputTypeDef]
    ModelSettings: NotRequired[ModelSettingsTypeDef]
    IdentifyLanguage: NotRequired[bool]
    IdentifyMultipleLanguages: NotRequired[bool]
    IdentifiedLanguageScore: NotRequired[float]
    LanguageCodes: NotRequired[List[LanguageCodeItemTypeDef]]
    ToxicityDetection: NotRequired[List[ToxicityDetectionSettingsOutputTypeDef]]

class TranscriptionJobTypeDef(TypedDict):
    TranscriptionJobName: NotRequired[str]
    TranscriptionJobStatus: NotRequired[TranscriptionJobStatusType]
    LanguageCode: NotRequired[LanguageCodeType]
    MediaSampleRateHertz: NotRequired[int]
    MediaFormat: NotRequired[MediaFormatType]
    Media: NotRequired[MediaTypeDef]
    Transcript: NotRequired[TranscriptTypeDef]
    StartTime: NotRequired[datetime]
    CreationTime: NotRequired[datetime]
    CompletionTime: NotRequired[datetime]
    FailureReason: NotRequired[str]
    Settings: NotRequired[SettingsTypeDef]
    ModelSettings: NotRequired[ModelSettingsTypeDef]
    JobExecutionSettings: NotRequired[JobExecutionSettingsTypeDef]
    ContentRedaction: NotRequired[ContentRedactionOutputTypeDef]
    IdentifyLanguage: NotRequired[bool]
    IdentifyMultipleLanguages: NotRequired[bool]
    LanguageOptions: NotRequired[List[LanguageCodeType]]
    IdentifiedLanguageScore: NotRequired[float]
    LanguageCodes: NotRequired[List[LanguageCodeItemTypeDef]]
    Tags: NotRequired[List[TagTypeDef]]
    Subtitles: NotRequired[SubtitlesOutputTypeDef]
    LanguageIdSettings: NotRequired[Dict[LanguageCodeType, LanguageIdSettingsTypeDef]]
    ToxicityDetection: NotRequired[List[ToxicityDetectionSettingsOutputTypeDef]]

ToxicityDetectionSettingsUnionTypeDef = Union[
    ToxicityDetectionSettingsTypeDef, ToxicityDetectionSettingsOutputTypeDef
]

class CallAnalyticsJobSummaryTypeDef(TypedDict):
    CallAnalyticsJobName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    StartTime: NotRequired[datetime]
    CompletionTime: NotRequired[datetime]
    LanguageCode: NotRequired[LanguageCodeType]
    CallAnalyticsJobStatus: NotRequired[CallAnalyticsJobStatusType]
    CallAnalyticsJobDetails: NotRequired[CallAnalyticsJobDetailsTypeDef]
    FailureReason: NotRequired[str]

class CallAnalyticsJobTypeDef(TypedDict):
    CallAnalyticsJobName: NotRequired[str]
    CallAnalyticsJobStatus: NotRequired[CallAnalyticsJobStatusType]
    CallAnalyticsJobDetails: NotRequired[CallAnalyticsJobDetailsTypeDef]
    LanguageCode: NotRequired[LanguageCodeType]
    MediaSampleRateHertz: NotRequired[int]
    MediaFormat: NotRequired[MediaFormatType]
    Media: NotRequired[MediaTypeDef]
    Transcript: NotRequired[TranscriptTypeDef]
    StartTime: NotRequired[datetime]
    CreationTime: NotRequired[datetime]
    CompletionTime: NotRequired[datetime]
    FailureReason: NotRequired[str]
    DataAccessRoleArn: NotRequired[str]
    IdentifiedLanguageScore: NotRequired[float]
    Settings: NotRequired[CallAnalyticsJobSettingsOutputTypeDef]
    ChannelDefinitions: NotRequired[List[ChannelDefinitionTypeDef]]

class CallAnalyticsJobSettingsTypeDef(TypedDict):
    VocabularyName: NotRequired[str]
    VocabularyFilterName: NotRequired[str]
    VocabularyFilterMethod: NotRequired[VocabularyFilterMethodType]
    LanguageModelName: NotRequired[str]
    ContentRedaction: NotRequired[ContentRedactionUnionTypeDef]
    LanguageOptions: NotRequired[Sequence[LanguageCodeType]]
    LanguageIdSettings: NotRequired[Mapping[LanguageCodeType, LanguageIdSettingsTypeDef]]
    Summarization: NotRequired[SummarizationTypeDef]

class DescribeLanguageModelResponseTypeDef(TypedDict):
    LanguageModel: LanguageModelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListLanguageModelsResponseTypeDef(TypedDict):
    Models: List[LanguageModelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

SentimentFilterUnionTypeDef = Union[SentimentFilterTypeDef, SentimentFilterOutputTypeDef]

class RuleOutputTypeDef(TypedDict):
    NonTalkTimeFilter: NotRequired[NonTalkTimeFilterTypeDef]
    InterruptionFilter: NotRequired[InterruptionFilterTypeDef]
    TranscriptFilter: NotRequired[TranscriptFilterOutputTypeDef]
    SentimentFilter: NotRequired[SentimentFilterOutputTypeDef]

TranscriptFilterUnionTypeDef = Union[TranscriptFilterTypeDef, TranscriptFilterOutputTypeDef]

class GetMedicalScribeJobResponseTypeDef(TypedDict):
    MedicalScribeJob: MedicalScribeJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartMedicalScribeJobResponseTypeDef(TypedDict):
    MedicalScribeJob: MedicalScribeJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetMedicalTranscriptionJobResponseTypeDef(TypedDict):
    MedicalTranscriptionJob: MedicalTranscriptionJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartMedicalTranscriptionJobResponseTypeDef(TypedDict):
    MedicalTranscriptionJob: MedicalTranscriptionJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListTranscriptionJobsResponseTypeDef(TypedDict):
    Status: TranscriptionJobStatusType
    TranscriptionJobSummaries: List[TranscriptionJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetTranscriptionJobResponseTypeDef(TypedDict):
    TranscriptionJob: TranscriptionJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartTranscriptionJobResponseTypeDef(TypedDict):
    TranscriptionJob: TranscriptionJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartTranscriptionJobRequestRequestTypeDef(TypedDict):
    TranscriptionJobName: str
    Media: MediaTypeDef
    LanguageCode: NotRequired[LanguageCodeType]
    MediaSampleRateHertz: NotRequired[int]
    MediaFormat: NotRequired[MediaFormatType]
    OutputBucketName: NotRequired[str]
    OutputKey: NotRequired[str]
    OutputEncryptionKMSKeyId: NotRequired[str]
    KMSEncryptionContext: NotRequired[Mapping[str, str]]
    Settings: NotRequired[SettingsTypeDef]
    ModelSettings: NotRequired[ModelSettingsTypeDef]
    JobExecutionSettings: NotRequired[JobExecutionSettingsTypeDef]
    ContentRedaction: NotRequired[ContentRedactionTypeDef]
    IdentifyLanguage: NotRequired[bool]
    IdentifyMultipleLanguages: NotRequired[bool]
    LanguageOptions: NotRequired[Sequence[LanguageCodeType]]
    Subtitles: NotRequired[SubtitlesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    LanguageIdSettings: NotRequired[Mapping[LanguageCodeType, LanguageIdSettingsTypeDef]]
    ToxicityDetection: NotRequired[Sequence[ToxicityDetectionSettingsUnionTypeDef]]

class ListCallAnalyticsJobsResponseTypeDef(TypedDict):
    Status: CallAnalyticsJobStatusType
    CallAnalyticsJobSummaries: List[CallAnalyticsJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetCallAnalyticsJobResponseTypeDef(TypedDict):
    CallAnalyticsJob: CallAnalyticsJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartCallAnalyticsJobResponseTypeDef(TypedDict):
    CallAnalyticsJob: CallAnalyticsJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartCallAnalyticsJobRequestRequestTypeDef(TypedDict):
    CallAnalyticsJobName: str
    Media: MediaTypeDef
    OutputLocation: NotRequired[str]
    OutputEncryptionKMSKeyId: NotRequired[str]
    DataAccessRoleArn: NotRequired[str]
    Settings: NotRequired[CallAnalyticsJobSettingsTypeDef]
    ChannelDefinitions: NotRequired[Sequence[ChannelDefinitionTypeDef]]

class CategoryPropertiesTypeDef(TypedDict):
    CategoryName: NotRequired[str]
    Rules: NotRequired[List[RuleOutputTypeDef]]
    CreateTime: NotRequired[datetime]
    LastUpdateTime: NotRequired[datetime]
    InputType: NotRequired[InputTypeType]

class RuleTypeDef(TypedDict):
    NonTalkTimeFilter: NotRequired[NonTalkTimeFilterTypeDef]
    InterruptionFilter: NotRequired[InterruptionFilterTypeDef]
    TranscriptFilter: NotRequired[TranscriptFilterUnionTypeDef]
    SentimentFilter: NotRequired[SentimentFilterUnionTypeDef]

class CreateCallAnalyticsCategoryResponseTypeDef(TypedDict):
    CategoryProperties: CategoryPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetCallAnalyticsCategoryResponseTypeDef(TypedDict):
    CategoryProperties: CategoryPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListCallAnalyticsCategoriesResponseTypeDef(TypedDict):
    Categories: List[CategoryPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateCallAnalyticsCategoryResponseTypeDef(TypedDict):
    CategoryProperties: CategoryPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

RuleUnionTypeDef = Union[RuleTypeDef, RuleOutputTypeDef]

class UpdateCallAnalyticsCategoryRequestRequestTypeDef(TypedDict):
    CategoryName: str
    Rules: Sequence[RuleTypeDef]
    InputType: NotRequired[InputTypeType]

class CreateCallAnalyticsCategoryRequestRequestTypeDef(TypedDict):
    CategoryName: str
    Rules: Sequence[RuleUnionTypeDef]
    InputType: NotRequired[InputTypeType]
