"""
Type annotations for account service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account/type_defs/)

Usage::

    ```python
    from mypy_boto3_account.type_defs import AcceptPrimaryEmailUpdateRequestRequestTypeDef

    data: AcceptPrimaryEmailUpdateRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Sequence

from .literals import AlternateContactTypeType, PrimaryEmailUpdateStatusType, RegionOptStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AcceptPrimaryEmailUpdateRequestRequestTypeDef",
    "AcceptPrimaryEmailUpdateResponseTypeDef",
    "AlternateContactTypeDef",
    "ContactInformationTypeDef",
    "DeleteAlternateContactRequestRequestTypeDef",
    "DisableRegionRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableRegionRequestRequestTypeDef",
    "GetAlternateContactRequestRequestTypeDef",
    "GetAlternateContactResponseTypeDef",
    "GetContactInformationRequestRequestTypeDef",
    "GetContactInformationResponseTypeDef",
    "GetPrimaryEmailRequestRequestTypeDef",
    "GetPrimaryEmailResponseTypeDef",
    "GetRegionOptStatusRequestRequestTypeDef",
    "GetRegionOptStatusResponseTypeDef",
    "ListRegionsRequestListRegionsPaginateTypeDef",
    "ListRegionsRequestRequestTypeDef",
    "ListRegionsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutAlternateContactRequestRequestTypeDef",
    "PutContactInformationRequestRequestTypeDef",
    "RegionTypeDef",
    "ResponseMetadataTypeDef",
    "StartPrimaryEmailUpdateRequestRequestTypeDef",
    "StartPrimaryEmailUpdateResponseTypeDef",
)


class AcceptPrimaryEmailUpdateRequestRequestTypeDef(TypedDict):
    AccountId: str
    Otp: str
    PrimaryEmail: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AlternateContactTypeDef(TypedDict):
    AlternateContactType: NotRequired[AlternateContactTypeType]
    EmailAddress: NotRequired[str]
    Name: NotRequired[str]
    PhoneNumber: NotRequired[str]
    Title: NotRequired[str]


class ContactInformationTypeDef(TypedDict):
    AddressLine1: str
    City: str
    CountryCode: str
    FullName: str
    PhoneNumber: str
    PostalCode: str
    AddressLine2: NotRequired[str]
    AddressLine3: NotRequired[str]
    CompanyName: NotRequired[str]
    DistrictOrCounty: NotRequired[str]
    StateOrRegion: NotRequired[str]
    WebsiteUrl: NotRequired[str]


class DeleteAlternateContactRequestRequestTypeDef(TypedDict):
    AlternateContactType: AlternateContactTypeType
    AccountId: NotRequired[str]


class DisableRegionRequestRequestTypeDef(TypedDict):
    RegionName: str
    AccountId: NotRequired[str]


class EnableRegionRequestRequestTypeDef(TypedDict):
    RegionName: str
    AccountId: NotRequired[str]


class GetAlternateContactRequestRequestTypeDef(TypedDict):
    AlternateContactType: AlternateContactTypeType
    AccountId: NotRequired[str]


class GetContactInformationRequestRequestTypeDef(TypedDict):
    AccountId: NotRequired[str]


class GetPrimaryEmailRequestRequestTypeDef(TypedDict):
    AccountId: str


class GetRegionOptStatusRequestRequestTypeDef(TypedDict):
    RegionName: str
    AccountId: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListRegionsRequestRequestTypeDef(TypedDict):
    AccountId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    RegionOptStatusContains: NotRequired[Sequence[RegionOptStatusType]]


class RegionTypeDef(TypedDict):
    RegionName: NotRequired[str]
    RegionOptStatus: NotRequired[RegionOptStatusType]


class PutAlternateContactRequestRequestTypeDef(TypedDict):
    AlternateContactType: AlternateContactTypeType
    EmailAddress: str
    Name: str
    PhoneNumber: str
    Title: str
    AccountId: NotRequired[str]


class StartPrimaryEmailUpdateRequestRequestTypeDef(TypedDict):
    AccountId: str
    PrimaryEmail: str


class AcceptPrimaryEmailUpdateResponseTypeDef(TypedDict):
    Status: PrimaryEmailUpdateStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetPrimaryEmailResponseTypeDef(TypedDict):
    PrimaryEmail: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRegionOptStatusResponseTypeDef(TypedDict):
    RegionName: str
    RegionOptStatus: RegionOptStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class StartPrimaryEmailUpdateResponseTypeDef(TypedDict):
    Status: PrimaryEmailUpdateStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetAlternateContactResponseTypeDef(TypedDict):
    AlternateContact: AlternateContactTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetContactInformationResponseTypeDef(TypedDict):
    ContactInformation: ContactInformationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutContactInformationRequestRequestTypeDef(TypedDict):
    ContactInformation: ContactInformationTypeDef
    AccountId: NotRequired[str]


class ListRegionsRequestListRegionsPaginateTypeDef(TypedDict):
    AccountId: NotRequired[str]
    RegionOptStatusContains: NotRequired[Sequence[RegionOptStatusType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRegionsResponseTypeDef(TypedDict):
    Regions: List[RegionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
