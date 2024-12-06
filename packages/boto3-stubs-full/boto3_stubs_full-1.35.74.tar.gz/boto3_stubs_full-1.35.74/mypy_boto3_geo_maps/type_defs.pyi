"""
Type annotations for geo-maps service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_maps/type_defs/)

Usage::

    ```python
    from mypy_boto3_geo_maps.type_defs import GetGlyphsRequestRequestTypeDef

    data: GetGlyphsRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict

from botocore.response import StreamingBody

from .literals import ColorSchemeType, MapStyleType, ScaleBarUnitType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "GetGlyphsRequestRequestTypeDef",
    "GetGlyphsResponseTypeDef",
    "GetSpritesRequestRequestTypeDef",
    "GetSpritesResponseTypeDef",
    "GetStaticMapRequestRequestTypeDef",
    "GetStaticMapResponseTypeDef",
    "GetStyleDescriptorRequestRequestTypeDef",
    "GetStyleDescriptorResponseTypeDef",
    "GetTileRequestRequestTypeDef",
    "GetTileResponseTypeDef",
    "ResponseMetadataTypeDef",
)

class GetGlyphsRequestRequestTypeDef(TypedDict):
    FontStack: str
    FontUnicodeRange: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class GetSpritesRequestRequestTypeDef(TypedDict):
    FileName: str
    Style: MapStyleType
    ColorScheme: ColorSchemeType
    Variant: Literal["Default"]

class GetStaticMapRequestRequestTypeDef(TypedDict):
    Height: int
    FileName: str
    Width: int
    BoundingBox: NotRequired[str]
    BoundedPositions: NotRequired[str]
    Center: NotRequired[str]
    CompactOverlay: NotRequired[str]
    GeoJsonOverlay: NotRequired[str]
    Key: NotRequired[str]
    Padding: NotRequired[int]
    Radius: NotRequired[int]
    ScaleBarUnit: NotRequired[ScaleBarUnitType]
    Style: NotRequired[Literal["Satellite"]]
    Zoom: NotRequired[float]

class GetStyleDescriptorRequestRequestTypeDef(TypedDict):
    Style: MapStyleType
    ColorScheme: NotRequired[ColorSchemeType]
    PoliticalView: NotRequired[str]
    Key: NotRequired[str]

class GetTileRequestRequestTypeDef(TypedDict):
    Tileset: str
    Z: str
    X: str
    Y: str
    Key: NotRequired[str]

class GetGlyphsResponseTypeDef(TypedDict):
    Blob: StreamingBody
    ContentType: str
    CacheControl: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetSpritesResponseTypeDef(TypedDict):
    Blob: StreamingBody
    ContentType: str
    CacheControl: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetStaticMapResponseTypeDef(TypedDict):
    Blob: StreamingBody
    ContentType: str
    CacheControl: str
    ETag: str
    PricingBucket: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetStyleDescriptorResponseTypeDef(TypedDict):
    Blob: StreamingBody
    ContentType: str
    CacheControl: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetTileResponseTypeDef(TypedDict):
    Blob: StreamingBody
    ContentType: str
    CacheControl: str
    ETag: str
    PricingBucket: str
    ResponseMetadata: ResponseMetadataTypeDef
