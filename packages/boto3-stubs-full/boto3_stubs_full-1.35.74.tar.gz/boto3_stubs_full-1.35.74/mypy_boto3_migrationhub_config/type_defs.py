"""
Type annotations for migrationhub-config service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhub_config/type_defs/)

Usage::

    ```python
    from mypy_boto3_migrationhub_config.type_defs import TargetTypeDef

    data: TargetTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "CreateHomeRegionControlRequestRequestTypeDef",
    "CreateHomeRegionControlResultTypeDef",
    "DeleteHomeRegionControlRequestRequestTypeDef",
    "DescribeHomeRegionControlsRequestRequestTypeDef",
    "DescribeHomeRegionControlsResultTypeDef",
    "GetHomeRegionResultTypeDef",
    "HomeRegionControlTypeDef",
    "ResponseMetadataTypeDef",
    "TargetTypeDef",
)

TargetTypeDef = TypedDict(
    "TargetTypeDef",
    {
        "Type": Literal["ACCOUNT"],
        "Id": NotRequired[str],
    },
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteHomeRegionControlRequestRequestTypeDef(TypedDict):
    ControlId: str


class CreateHomeRegionControlRequestRequestTypeDef(TypedDict):
    HomeRegion: str
    Target: TargetTypeDef
    DryRun: NotRequired[bool]


class DescribeHomeRegionControlsRequestRequestTypeDef(TypedDict):
    ControlId: NotRequired[str]
    HomeRegion: NotRequired[str]
    Target: NotRequired[TargetTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class HomeRegionControlTypeDef(TypedDict):
    ControlId: NotRequired[str]
    HomeRegion: NotRequired[str]
    Target: NotRequired[TargetTypeDef]
    RequestedTime: NotRequired[datetime]


class GetHomeRegionResultTypeDef(TypedDict):
    HomeRegion: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHomeRegionControlResultTypeDef(TypedDict):
    HomeRegionControl: HomeRegionControlTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeHomeRegionControlsResultTypeDef(TypedDict):
    HomeRegionControls: List[HomeRegionControlTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
