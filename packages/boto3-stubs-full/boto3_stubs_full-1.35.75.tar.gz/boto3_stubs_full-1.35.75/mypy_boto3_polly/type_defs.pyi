"""
Type annotations for polly service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/type_defs/)

Usage::

    ```python
    from mypy_boto3_polly.type_defs import DeleteLexiconInputRequestTypeDef

    data: DeleteLexiconInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from botocore.response import StreamingBody

from .literals import (
    EngineType,
    GenderType,
    LanguageCodeType,
    OutputFormatType,
    SpeechMarkTypeType,
    TaskStatusType,
    TextTypeType,
    VoiceIdType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "DeleteLexiconInputRequestTypeDef",
    "DescribeVoicesInputDescribeVoicesPaginateTypeDef",
    "DescribeVoicesInputRequestTypeDef",
    "DescribeVoicesOutputTypeDef",
    "GetLexiconInputRequestTypeDef",
    "GetLexiconOutputTypeDef",
    "GetSpeechSynthesisTaskInputRequestTypeDef",
    "GetSpeechSynthesisTaskOutputTypeDef",
    "LexiconAttributesTypeDef",
    "LexiconDescriptionTypeDef",
    "LexiconTypeDef",
    "ListLexiconsInputListLexiconsPaginateTypeDef",
    "ListLexiconsInputRequestTypeDef",
    "ListLexiconsOutputTypeDef",
    "ListSpeechSynthesisTasksInputListSpeechSynthesisTasksPaginateTypeDef",
    "ListSpeechSynthesisTasksInputRequestTypeDef",
    "ListSpeechSynthesisTasksOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PutLexiconInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "StartSpeechSynthesisTaskInputRequestTypeDef",
    "StartSpeechSynthesisTaskOutputTypeDef",
    "SynthesisTaskTypeDef",
    "SynthesizeSpeechInputRequestTypeDef",
    "SynthesizeSpeechOutputTypeDef",
    "VoiceTypeDef",
)

class DeleteLexiconInputRequestTypeDef(TypedDict):
    Name: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeVoicesInputRequestTypeDef(TypedDict):
    Engine: NotRequired[EngineType]
    LanguageCode: NotRequired[LanguageCodeType]
    IncludeAdditionalLanguageCodes: NotRequired[bool]
    NextToken: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class VoiceTypeDef(TypedDict):
    Gender: NotRequired[GenderType]
    Id: NotRequired[VoiceIdType]
    LanguageCode: NotRequired[LanguageCodeType]
    LanguageName: NotRequired[str]
    Name: NotRequired[str]
    AdditionalLanguageCodes: NotRequired[List[LanguageCodeType]]
    SupportedEngines: NotRequired[List[EngineType]]

class GetLexiconInputRequestTypeDef(TypedDict):
    Name: str

class LexiconAttributesTypeDef(TypedDict):
    Alphabet: NotRequired[str]
    LanguageCode: NotRequired[LanguageCodeType]
    LastModified: NotRequired[datetime]
    LexiconArn: NotRequired[str]
    LexemesCount: NotRequired[int]
    Size: NotRequired[int]

class LexiconTypeDef(TypedDict):
    Content: NotRequired[str]
    Name: NotRequired[str]

class GetSpeechSynthesisTaskInputRequestTypeDef(TypedDict):
    TaskId: str

class SynthesisTaskTypeDef(TypedDict):
    Engine: NotRequired[EngineType]
    TaskId: NotRequired[str]
    TaskStatus: NotRequired[TaskStatusType]
    TaskStatusReason: NotRequired[str]
    OutputUri: NotRequired[str]
    CreationTime: NotRequired[datetime]
    RequestCharacters: NotRequired[int]
    SnsTopicArn: NotRequired[str]
    LexiconNames: NotRequired[List[str]]
    OutputFormat: NotRequired[OutputFormatType]
    SampleRate: NotRequired[str]
    SpeechMarkTypes: NotRequired[List[SpeechMarkTypeType]]
    TextType: NotRequired[TextTypeType]
    VoiceId: NotRequired[VoiceIdType]
    LanguageCode: NotRequired[LanguageCodeType]

class ListLexiconsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]

class ListSpeechSynthesisTasksInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Status: NotRequired[TaskStatusType]

class PutLexiconInputRequestTypeDef(TypedDict):
    Name: str
    Content: str

StartSpeechSynthesisTaskInputRequestTypeDef = TypedDict(
    "StartSpeechSynthesisTaskInputRequestTypeDef",
    {
        "OutputFormat": OutputFormatType,
        "OutputS3BucketName": str,
        "Text": str,
        "VoiceId": VoiceIdType,
        "Engine": NotRequired[EngineType],
        "LanguageCode": NotRequired[LanguageCodeType],
        "LexiconNames": NotRequired[Sequence[str]],
        "OutputS3KeyPrefix": NotRequired[str],
        "SampleRate": NotRequired[str],
        "SnsTopicArn": NotRequired[str],
        "SpeechMarkTypes": NotRequired[Sequence[SpeechMarkTypeType]],
        "TextType": NotRequired[TextTypeType],
    },
)
SynthesizeSpeechInputRequestTypeDef = TypedDict(
    "SynthesizeSpeechInputRequestTypeDef",
    {
        "OutputFormat": OutputFormatType,
        "Text": str,
        "VoiceId": VoiceIdType,
        "Engine": NotRequired[EngineType],
        "LanguageCode": NotRequired[LanguageCodeType],
        "LexiconNames": NotRequired[Sequence[str]],
        "SampleRate": NotRequired[str],
        "SpeechMarkTypes": NotRequired[Sequence[SpeechMarkTypeType]],
        "TextType": NotRequired[TextTypeType],
    },
)

class DescribeVoicesInputDescribeVoicesPaginateTypeDef(TypedDict):
    Engine: NotRequired[EngineType]
    LanguageCode: NotRequired[LanguageCodeType]
    IncludeAdditionalLanguageCodes: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLexiconsInputListLexiconsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSpeechSynthesisTasksInputListSpeechSynthesisTasksPaginateTypeDef(TypedDict):
    Status: NotRequired[TaskStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SynthesizeSpeechOutputTypeDef(TypedDict):
    AudioStream: StreamingBody
    ContentType: str
    RequestCharacters: int
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeVoicesOutputTypeDef(TypedDict):
    Voices: List[VoiceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class LexiconDescriptionTypeDef(TypedDict):
    Name: NotRequired[str]
    Attributes: NotRequired[LexiconAttributesTypeDef]

class GetLexiconOutputTypeDef(TypedDict):
    Lexicon: LexiconTypeDef
    LexiconAttributes: LexiconAttributesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSpeechSynthesisTaskOutputTypeDef(TypedDict):
    SynthesisTask: SynthesisTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSpeechSynthesisTasksOutputTypeDef(TypedDict):
    SynthesisTasks: List[SynthesisTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StartSpeechSynthesisTaskOutputTypeDef(TypedDict):
    SynthesisTask: SynthesisTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListLexiconsOutputTypeDef(TypedDict):
    Lexicons: List[LexiconDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
