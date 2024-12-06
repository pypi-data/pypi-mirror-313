"""
Type annotations for kinesis-video-media service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_media/type_defs/)

Usage::

    ```python
    from mypy_boto3_kinesis_video_media.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, Union

from botocore.response import StreamingBody

from .literals import StartSelectorTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "GetMediaInputRequestTypeDef",
    "GetMediaOutputTypeDef",
    "ResponseMetadataTypeDef",
    "StartSelectorTypeDef",
    "TimestampTypeDef",
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class GetMediaOutputTypeDef(TypedDict):
    ContentType: str
    Payload: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef

class StartSelectorTypeDef(TypedDict):
    StartSelectorType: StartSelectorTypeType
    AfterFragmentNumber: NotRequired[str]
    StartTimestamp: NotRequired[TimestampTypeDef]
    ContinuationToken: NotRequired[str]

class GetMediaInputRequestTypeDef(TypedDict):
    StartSelector: StartSelectorTypeDef
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
