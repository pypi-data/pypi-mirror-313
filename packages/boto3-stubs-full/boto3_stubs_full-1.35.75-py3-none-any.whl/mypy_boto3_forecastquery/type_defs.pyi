"""
Type annotations for forecastquery service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_forecastquery/type_defs/)

Usage::

    ```python
    from mypy_boto3_forecastquery.type_defs import DataPointTypeDef

    data: DataPointTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Mapping

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "DataPointTypeDef",
    "ForecastTypeDef",
    "QueryForecastRequestRequestTypeDef",
    "QueryForecastResponseTypeDef",
    "QueryWhatIfForecastRequestRequestTypeDef",
    "QueryWhatIfForecastResponseTypeDef",
    "ResponseMetadataTypeDef",
)

class DataPointTypeDef(TypedDict):
    Timestamp: NotRequired[str]
    Value: NotRequired[float]

class QueryForecastRequestRequestTypeDef(TypedDict):
    ForecastArn: str
    Filters: Mapping[str, str]
    StartDate: NotRequired[str]
    EndDate: NotRequired[str]
    NextToken: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class QueryWhatIfForecastRequestRequestTypeDef(TypedDict):
    WhatIfForecastArn: str
    Filters: Mapping[str, str]
    StartDate: NotRequired[str]
    EndDate: NotRequired[str]
    NextToken: NotRequired[str]

class ForecastTypeDef(TypedDict):
    Predictions: NotRequired[Dict[str, List[DataPointTypeDef]]]

class QueryForecastResponseTypeDef(TypedDict):
    Forecast: ForecastTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class QueryWhatIfForecastResponseTypeDef(TypedDict):
    Forecast: ForecastTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
