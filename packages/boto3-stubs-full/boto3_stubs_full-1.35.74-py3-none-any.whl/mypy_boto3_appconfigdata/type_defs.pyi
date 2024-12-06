"""
Type annotations for appconfigdata service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfigdata/type_defs/)

Usage::

    ```python
    from mypy_boto3_appconfigdata.type_defs import GetLatestConfigurationRequestRequestTypeDef

    data: GetLatestConfigurationRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict

from botocore.response import StreamingBody

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "GetLatestConfigurationRequestRequestTypeDef",
    "GetLatestConfigurationResponseTypeDef",
    "ResponseMetadataTypeDef",
    "StartConfigurationSessionRequestRequestTypeDef",
    "StartConfigurationSessionResponseTypeDef",
)

class GetLatestConfigurationRequestRequestTypeDef(TypedDict):
    ConfigurationToken: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class StartConfigurationSessionRequestRequestTypeDef(TypedDict):
    ApplicationIdentifier: str
    EnvironmentIdentifier: str
    ConfigurationProfileIdentifier: str
    RequiredMinimumPollIntervalInSeconds: NotRequired[int]

class GetLatestConfigurationResponseTypeDef(TypedDict):
    NextPollConfigurationToken: str
    NextPollIntervalInSeconds: int
    ContentType: str
    Configuration: StreamingBody
    VersionLabel: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartConfigurationSessionResponseTypeDef(TypedDict):
    InitialConfigurationToken: str
    ResponseMetadata: ResponseMetadataTypeDef
