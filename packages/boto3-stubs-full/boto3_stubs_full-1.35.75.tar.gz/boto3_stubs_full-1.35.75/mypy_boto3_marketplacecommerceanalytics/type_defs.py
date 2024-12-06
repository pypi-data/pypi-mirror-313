"""
Type annotations for marketplacecommerceanalytics service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplacecommerceanalytics/type_defs/)

Usage::

    ```python
    from mypy_boto3_marketplacecommerceanalytics.type_defs import TimestampTypeDef

    data: TimestampTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, Mapping, Union

from .literals import DataSetTypeType, SupportDataSetTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "GenerateDataSetRequestRequestTypeDef",
    "GenerateDataSetResultTypeDef",
    "ResponseMetadataTypeDef",
    "StartSupportDataExportRequestRequestTypeDef",
    "StartSupportDataExportResultTypeDef",
    "TimestampTypeDef",
)

TimestampTypeDef = Union[datetime, str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class GenerateDataSetRequestRequestTypeDef(TypedDict):
    dataSetType: DataSetTypeType
    dataSetPublicationDate: TimestampTypeDef
    roleNameArn: str
    destinationS3BucketName: str
    snsTopicArn: str
    destinationS3Prefix: NotRequired[str]
    customerDefinedValues: NotRequired[Mapping[str, str]]


class StartSupportDataExportRequestRequestTypeDef(TypedDict):
    dataSetType: SupportDataSetTypeType
    fromDate: TimestampTypeDef
    roleNameArn: str
    destinationS3BucketName: str
    snsTopicArn: str
    destinationS3Prefix: NotRequired[str]
    customerDefinedValues: NotRequired[Mapping[str, str]]


class GenerateDataSetResultTypeDef(TypedDict):
    dataSetRequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartSupportDataExportResultTypeDef(TypedDict):
    dataSetRequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
