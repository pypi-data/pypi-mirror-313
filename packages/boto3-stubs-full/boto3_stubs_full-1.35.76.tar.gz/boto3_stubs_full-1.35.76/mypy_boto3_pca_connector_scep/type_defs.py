"""
Type annotations for pca-connector-scep service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_scep/type_defs/)

Usage::

    ```python
    from mypy_boto3_pca_connector_scep.type_defs import ChallengeMetadataSummaryTypeDef

    data: ChallengeMetadataSummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import ConnectorStatusReasonType, ConnectorStatusType, ConnectorTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ChallengeMetadataSummaryTypeDef",
    "ChallengeMetadataTypeDef",
    "ChallengeTypeDef",
    "ConnectorSummaryTypeDef",
    "ConnectorTypeDef",
    "CreateChallengeRequestRequestTypeDef",
    "CreateChallengeResponseTypeDef",
    "CreateConnectorRequestRequestTypeDef",
    "CreateConnectorResponseTypeDef",
    "DeleteChallengeRequestRequestTypeDef",
    "DeleteConnectorRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetChallengeMetadataRequestRequestTypeDef",
    "GetChallengeMetadataResponseTypeDef",
    "GetChallengePasswordRequestRequestTypeDef",
    "GetChallengePasswordResponseTypeDef",
    "GetConnectorRequestRequestTypeDef",
    "GetConnectorResponseTypeDef",
    "IntuneConfigurationTypeDef",
    "ListChallengeMetadataRequestListChallengeMetadataPaginateTypeDef",
    "ListChallengeMetadataRequestRequestTypeDef",
    "ListChallengeMetadataResponseTypeDef",
    "ListConnectorsRequestListConnectorsPaginateTypeDef",
    "ListConnectorsRequestRequestTypeDef",
    "ListConnectorsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MobileDeviceManagementTypeDef",
    "OpenIdConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
)


class ChallengeMetadataSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    ConnectorArn: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]


class ChallengeMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]
    ConnectorArn: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]


class ChallengeTypeDef(TypedDict):
    Arn: NotRequired[str]
    ConnectorArn: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]
    Password: NotRequired[str]


class OpenIdConfigurationTypeDef(TypedDict):
    Issuer: NotRequired[str]
    Subject: NotRequired[str]
    Audience: NotRequired[str]


class CreateChallengeRequestRequestTypeDef(TypedDict):
    ConnectorArn: str
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteChallengeRequestRequestTypeDef(TypedDict):
    ChallengeArn: str


class DeleteConnectorRequestRequestTypeDef(TypedDict):
    ConnectorArn: str


class GetChallengeMetadataRequestRequestTypeDef(TypedDict):
    ChallengeArn: str


class GetChallengePasswordRequestRequestTypeDef(TypedDict):
    ChallengeArn: str


class GetConnectorRequestRequestTypeDef(TypedDict):
    ConnectorArn: str


class IntuneConfigurationTypeDef(TypedDict):
    AzureApplicationId: str
    Domain: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListChallengeMetadataRequestRequestTypeDef(TypedDict):
    ConnectorArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListConnectorsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class CreateChallengeResponseTypeDef(TypedDict):
    Challenge: ChallengeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateConnectorResponseTypeDef(TypedDict):
    ConnectorArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetChallengeMetadataResponseTypeDef(TypedDict):
    ChallengeMetadata: ChallengeMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetChallengePasswordResponseTypeDef(TypedDict):
    Password: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListChallengeMetadataResponseTypeDef(TypedDict):
    Challenges: List[ChallengeMetadataSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class MobileDeviceManagementTypeDef(TypedDict):
    Intune: NotRequired[IntuneConfigurationTypeDef]


class ListChallengeMetadataRequestListChallengeMetadataPaginateTypeDef(TypedDict):
    ConnectorArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListConnectorsRequestListConnectorsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ConnectorSummaryTypeDef = TypedDict(
    "ConnectorSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "CertificateAuthorityArn": NotRequired[str],
        "Type": NotRequired[ConnectorTypeType],
        "MobileDeviceManagement": NotRequired[MobileDeviceManagementTypeDef],
        "OpenIdConfiguration": NotRequired[OpenIdConfigurationTypeDef],
        "Status": NotRequired[ConnectorStatusType],
        "StatusReason": NotRequired[ConnectorStatusReasonType],
        "Endpoint": NotRequired[str],
        "CreatedAt": NotRequired[datetime],
        "UpdatedAt": NotRequired[datetime],
    },
)
ConnectorTypeDef = TypedDict(
    "ConnectorTypeDef",
    {
        "Arn": NotRequired[str],
        "CertificateAuthorityArn": NotRequired[str],
        "Type": NotRequired[ConnectorTypeType],
        "MobileDeviceManagement": NotRequired[MobileDeviceManagementTypeDef],
        "OpenIdConfiguration": NotRequired[OpenIdConfigurationTypeDef],
        "Status": NotRequired[ConnectorStatusType],
        "StatusReason": NotRequired[ConnectorStatusReasonType],
        "Endpoint": NotRequired[str],
        "CreatedAt": NotRequired[datetime],
        "UpdatedAt": NotRequired[datetime],
    },
)


class CreateConnectorRequestRequestTypeDef(TypedDict):
    CertificateAuthorityArn: str
    MobileDeviceManagement: NotRequired[MobileDeviceManagementTypeDef]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class ListConnectorsResponseTypeDef(TypedDict):
    Connectors: List[ConnectorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetConnectorResponseTypeDef(TypedDict):
    Connector: ConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
