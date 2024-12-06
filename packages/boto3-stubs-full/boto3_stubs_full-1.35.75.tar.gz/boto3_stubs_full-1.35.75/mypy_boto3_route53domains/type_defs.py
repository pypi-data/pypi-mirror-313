"""
Type annotations for route53domains service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53domains/type_defs/)

Usage::

    ```python
    from mypy_boto3_route53domains.type_defs import AcceptDomainTransferFromAnotherAwsAccountRequestRequestTypeDef

    data: AcceptDomainTransferFromAnotherAwsAccountRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ContactTypeType,
    CountryCodeType,
    DomainAvailabilityType,
    ExtraParamNameType,
    ListDomainsAttributeNameType,
    OperationStatusType,
    OperationTypeType,
    OperatorType,
    ReachabilityStatusType,
    SortOrderType,
    StatusFlagType,
    TransferableType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AcceptDomainTransferFromAnotherAwsAccountRequestRequestTypeDef",
    "AcceptDomainTransferFromAnotherAwsAccountResponseTypeDef",
    "AssociateDelegationSignerToDomainRequestRequestTypeDef",
    "AssociateDelegationSignerToDomainResponseTypeDef",
    "BillingRecordTypeDef",
    "CancelDomainTransferToAnotherAwsAccountRequestRequestTypeDef",
    "CancelDomainTransferToAnotherAwsAccountResponseTypeDef",
    "CheckDomainAvailabilityRequestRequestTypeDef",
    "CheckDomainAvailabilityResponseTypeDef",
    "CheckDomainTransferabilityRequestRequestTypeDef",
    "CheckDomainTransferabilityResponseTypeDef",
    "ConsentTypeDef",
    "ContactDetailOutputTypeDef",
    "ContactDetailTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DeleteDomainResponseTypeDef",
    "DeleteTagsForDomainRequestRequestTypeDef",
    "DisableDomainAutoRenewRequestRequestTypeDef",
    "DisableDomainTransferLockRequestRequestTypeDef",
    "DisableDomainTransferLockResponseTypeDef",
    "DisassociateDelegationSignerFromDomainRequestRequestTypeDef",
    "DisassociateDelegationSignerFromDomainResponseTypeDef",
    "DnssecKeyTypeDef",
    "DnssecSigningAttributesTypeDef",
    "DomainPriceTypeDef",
    "DomainSuggestionTypeDef",
    "DomainSummaryTypeDef",
    "DomainTransferabilityTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableDomainAutoRenewRequestRequestTypeDef",
    "EnableDomainTransferLockRequestRequestTypeDef",
    "EnableDomainTransferLockResponseTypeDef",
    "ExtraParamTypeDef",
    "FilterConditionTypeDef",
    "GetContactReachabilityStatusRequestRequestTypeDef",
    "GetContactReachabilityStatusResponseTypeDef",
    "GetDomainDetailRequestRequestTypeDef",
    "GetDomainDetailResponseTypeDef",
    "GetDomainSuggestionsRequestRequestTypeDef",
    "GetDomainSuggestionsResponseTypeDef",
    "GetOperationDetailRequestRequestTypeDef",
    "GetOperationDetailResponseTypeDef",
    "ListDomainsRequestListDomainsPaginateTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListDomainsResponseTypeDef",
    "ListOperationsRequestListOperationsPaginateTypeDef",
    "ListOperationsRequestRequestTypeDef",
    "ListOperationsResponseTypeDef",
    "ListPricesRequestListPricesPaginateTypeDef",
    "ListPricesRequestRequestTypeDef",
    "ListPricesResponseTypeDef",
    "ListTagsForDomainRequestRequestTypeDef",
    "ListTagsForDomainResponseTypeDef",
    "NameserverOutputTypeDef",
    "NameserverTypeDef",
    "NameserverUnionTypeDef",
    "OperationSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "PriceWithCurrencyTypeDef",
    "PushDomainRequestRequestTypeDef",
    "RegisterDomainRequestRequestTypeDef",
    "RegisterDomainResponseTypeDef",
    "RejectDomainTransferFromAnotherAwsAccountRequestRequestTypeDef",
    "RejectDomainTransferFromAnotherAwsAccountResponseTypeDef",
    "RenewDomainRequestRequestTypeDef",
    "RenewDomainResponseTypeDef",
    "ResendContactReachabilityEmailRequestRequestTypeDef",
    "ResendContactReachabilityEmailResponseTypeDef",
    "ResendOperationAuthorizationRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RetrieveDomainAuthCodeRequestRequestTypeDef",
    "RetrieveDomainAuthCodeResponseTypeDef",
    "SortConditionTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "TransferDomainRequestRequestTypeDef",
    "TransferDomainResponseTypeDef",
    "TransferDomainToAnotherAwsAccountRequestRequestTypeDef",
    "TransferDomainToAnotherAwsAccountResponseTypeDef",
    "UpdateDomainContactPrivacyRequestRequestTypeDef",
    "UpdateDomainContactPrivacyResponseTypeDef",
    "UpdateDomainContactRequestRequestTypeDef",
    "UpdateDomainContactResponseTypeDef",
    "UpdateDomainNameserversRequestRequestTypeDef",
    "UpdateDomainNameserversResponseTypeDef",
    "UpdateTagsForDomainRequestRequestTypeDef",
    "ViewBillingRequestRequestTypeDef",
    "ViewBillingRequestViewBillingPaginateTypeDef",
    "ViewBillingResponseTypeDef",
)


class AcceptDomainTransferFromAnotherAwsAccountRequestRequestTypeDef(TypedDict):
    DomainName: str
    Password: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DnssecSigningAttributesTypeDef(TypedDict):
    Algorithm: NotRequired[int]
    Flags: NotRequired[int]
    PublicKey: NotRequired[str]


class BillingRecordTypeDef(TypedDict):
    DomainName: NotRequired[str]
    Operation: NotRequired[OperationTypeType]
    InvoiceId: NotRequired[str]
    BillDate: NotRequired[datetime]
    Price: NotRequired[float]


class CancelDomainTransferToAnotherAwsAccountRequestRequestTypeDef(TypedDict):
    DomainName: str


class CheckDomainAvailabilityRequestRequestTypeDef(TypedDict):
    DomainName: str
    IdnLangCode: NotRequired[str]


class CheckDomainTransferabilityRequestRequestTypeDef(TypedDict):
    DomainName: str
    AuthCode: NotRequired[str]


class DomainTransferabilityTypeDef(TypedDict):
    Transferable: NotRequired[TransferableType]


class ConsentTypeDef(TypedDict):
    MaxPrice: float
    Currency: str


class ExtraParamTypeDef(TypedDict):
    Name: ExtraParamNameType
    Value: str


class DeleteDomainRequestRequestTypeDef(TypedDict):
    DomainName: str


class DeleteTagsForDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    TagsToDelete: Sequence[str]


class DisableDomainAutoRenewRequestRequestTypeDef(TypedDict):
    DomainName: str


class DisableDomainTransferLockRequestRequestTypeDef(TypedDict):
    DomainName: str


class DisassociateDelegationSignerFromDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    Id: str


class DnssecKeyTypeDef(TypedDict):
    Algorithm: NotRequired[int]
    Flags: NotRequired[int]
    PublicKey: NotRequired[str]
    DigestType: NotRequired[int]
    Digest: NotRequired[str]
    KeyTag: NotRequired[int]
    Id: NotRequired[str]


class PriceWithCurrencyTypeDef(TypedDict):
    Price: float
    Currency: str


class DomainSuggestionTypeDef(TypedDict):
    DomainName: NotRequired[str]
    Availability: NotRequired[str]


class DomainSummaryTypeDef(TypedDict):
    DomainName: NotRequired[str]
    AutoRenew: NotRequired[bool]
    TransferLock: NotRequired[bool]
    Expiry: NotRequired[datetime]


class EnableDomainAutoRenewRequestRequestTypeDef(TypedDict):
    DomainName: str


class EnableDomainTransferLockRequestRequestTypeDef(TypedDict):
    DomainName: str


class FilterConditionTypeDef(TypedDict):
    Name: ListDomainsAttributeNameType
    Operator: OperatorType
    Values: Sequence[str]


class GetContactReachabilityStatusRequestRequestTypeDef(TypedDict):
    domainName: NotRequired[str]


class GetDomainDetailRequestRequestTypeDef(TypedDict):
    DomainName: str


class NameserverOutputTypeDef(TypedDict):
    Name: str
    GlueIps: NotRequired[List[str]]


class GetDomainSuggestionsRequestRequestTypeDef(TypedDict):
    DomainName: str
    SuggestionCount: int
    OnlyAvailable: bool


class GetOperationDetailRequestRequestTypeDef(TypedDict):
    OperationId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class SortConditionTypeDef(TypedDict):
    Name: ListDomainsAttributeNameType
    SortOrder: SortOrderType


TimestampTypeDef = Union[datetime, str]
OperationSummaryTypeDef = TypedDict(
    "OperationSummaryTypeDef",
    {
        "OperationId": NotRequired[str],
        "Status": NotRequired[OperationStatusType],
        "Type": NotRequired[OperationTypeType],
        "SubmittedDate": NotRequired[datetime],
        "DomainName": NotRequired[str],
        "Message": NotRequired[str],
        "StatusFlag": NotRequired[StatusFlagType],
        "LastUpdatedDate": NotRequired[datetime],
    },
)


class ListPricesRequestRequestTypeDef(TypedDict):
    Tld: NotRequired[str]
    Marker: NotRequired[str]
    MaxItems: NotRequired[int]


class ListTagsForDomainRequestRequestTypeDef(TypedDict):
    DomainName: str


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class NameserverTypeDef(TypedDict):
    Name: str
    GlueIps: NotRequired[Sequence[str]]


class PushDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    Target: str


class RejectDomainTransferFromAnotherAwsAccountRequestRequestTypeDef(TypedDict):
    DomainName: str


class RenewDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    CurrentExpiryYear: int
    DurationInYears: NotRequired[int]


class ResendContactReachabilityEmailRequestRequestTypeDef(TypedDict):
    domainName: NotRequired[str]


class ResendOperationAuthorizationRequestRequestTypeDef(TypedDict):
    OperationId: str


class RetrieveDomainAuthCodeRequestRequestTypeDef(TypedDict):
    DomainName: str


class TransferDomainToAnotherAwsAccountRequestRequestTypeDef(TypedDict):
    DomainName: str
    AccountId: str


class UpdateDomainContactPrivacyRequestRequestTypeDef(TypedDict):
    DomainName: str
    AdminPrivacy: NotRequired[bool]
    RegistrantPrivacy: NotRequired[bool]
    TechPrivacy: NotRequired[bool]
    BillingPrivacy: NotRequired[bool]


class AcceptDomainTransferFromAnotherAwsAccountResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateDelegationSignerToDomainResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CancelDomainTransferToAnotherAwsAccountResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CheckDomainAvailabilityResponseTypeDef(TypedDict):
    Availability: DomainAvailabilityType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDomainResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisableDomainTransferLockResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateDelegationSignerFromDomainResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class EnableDomainTransferLockResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetContactReachabilityStatusResponseTypeDef(TypedDict):
    domainName: str
    status: ReachabilityStatusType
    ResponseMetadata: ResponseMetadataTypeDef


GetOperationDetailResponseTypeDef = TypedDict(
    "GetOperationDetailResponseTypeDef",
    {
        "OperationId": str,
        "Status": OperationStatusType,
        "Message": str,
        "DomainName": str,
        "Type": OperationTypeType,
        "SubmittedDate": datetime,
        "LastUpdatedDate": datetime,
        "StatusFlag": StatusFlagType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class RegisterDomainResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RejectDomainTransferFromAnotherAwsAccountResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RenewDomainResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ResendContactReachabilityEmailResponseTypeDef(TypedDict):
    domainName: str
    emailAddress: str
    isAlreadyVerified: bool
    ResponseMetadata: ResponseMetadataTypeDef


class RetrieveDomainAuthCodeResponseTypeDef(TypedDict):
    AuthCode: str
    ResponseMetadata: ResponseMetadataTypeDef


class TransferDomainResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class TransferDomainToAnotherAwsAccountResponseTypeDef(TypedDict):
    OperationId: str
    Password: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDomainContactPrivacyResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDomainContactResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDomainNameserversResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateDelegationSignerToDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    SigningAttributes: DnssecSigningAttributesTypeDef


class ViewBillingResponseTypeDef(TypedDict):
    NextPageMarker: str
    BillingRecords: List[BillingRecordTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CheckDomainTransferabilityResponseTypeDef(TypedDict):
    Transferability: DomainTransferabilityTypeDef
    Message: str
    ResponseMetadata: ResponseMetadataTypeDef


class ContactDetailOutputTypeDef(TypedDict):
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    ContactType: NotRequired[ContactTypeType]
    OrganizationName: NotRequired[str]
    AddressLine1: NotRequired[str]
    AddressLine2: NotRequired[str]
    City: NotRequired[str]
    State: NotRequired[str]
    CountryCode: NotRequired[CountryCodeType]
    ZipCode: NotRequired[str]
    PhoneNumber: NotRequired[str]
    Email: NotRequired[str]
    Fax: NotRequired[str]
    ExtraParams: NotRequired[List[ExtraParamTypeDef]]


class ContactDetailTypeDef(TypedDict):
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    ContactType: NotRequired[ContactTypeType]
    OrganizationName: NotRequired[str]
    AddressLine1: NotRequired[str]
    AddressLine2: NotRequired[str]
    City: NotRequired[str]
    State: NotRequired[str]
    CountryCode: NotRequired[CountryCodeType]
    ZipCode: NotRequired[str]
    PhoneNumber: NotRequired[str]
    Email: NotRequired[str]
    Fax: NotRequired[str]
    ExtraParams: NotRequired[Sequence[ExtraParamTypeDef]]


class DomainPriceTypeDef(TypedDict):
    Name: NotRequired[str]
    RegistrationPrice: NotRequired[PriceWithCurrencyTypeDef]
    TransferPrice: NotRequired[PriceWithCurrencyTypeDef]
    RenewalPrice: NotRequired[PriceWithCurrencyTypeDef]
    ChangeOwnershipPrice: NotRequired[PriceWithCurrencyTypeDef]
    RestorationPrice: NotRequired[PriceWithCurrencyTypeDef]


class GetDomainSuggestionsResponseTypeDef(TypedDict):
    SuggestionsList: List[DomainSuggestionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListDomainsResponseTypeDef(TypedDict):
    Domains: List[DomainSummaryTypeDef]
    NextPageMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListPricesRequestListPricesPaginateTypeDef(TypedDict):
    Tld: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDomainsRequestListDomainsPaginateTypeDef(TypedDict):
    FilterConditions: NotRequired[Sequence[FilterConditionTypeDef]]
    SortCondition: NotRequired[SortConditionTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDomainsRequestRequestTypeDef(TypedDict):
    FilterConditions: NotRequired[Sequence[FilterConditionTypeDef]]
    SortCondition: NotRequired[SortConditionTypeDef]
    Marker: NotRequired[str]
    MaxItems: NotRequired[int]


ListOperationsRequestListOperationsPaginateTypeDef = TypedDict(
    "ListOperationsRequestListOperationsPaginateTypeDef",
    {
        "SubmittedSince": NotRequired[TimestampTypeDef],
        "Status": NotRequired[Sequence[OperationStatusType]],
        "Type": NotRequired[Sequence[OperationTypeType]],
        "SortBy": NotRequired[Literal["SubmittedDate"]],
        "SortOrder": NotRequired[SortOrderType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListOperationsRequestRequestTypeDef = TypedDict(
    "ListOperationsRequestRequestTypeDef",
    {
        "SubmittedSince": NotRequired[TimestampTypeDef],
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[int],
        "Status": NotRequired[Sequence[OperationStatusType]],
        "Type": NotRequired[Sequence[OperationTypeType]],
        "SortBy": NotRequired[Literal["SubmittedDate"]],
        "SortOrder": NotRequired[SortOrderType],
    },
)


class ViewBillingRequestRequestTypeDef(TypedDict):
    Start: NotRequired[TimestampTypeDef]
    End: NotRequired[TimestampTypeDef]
    Marker: NotRequired[str]
    MaxItems: NotRequired[int]


class ViewBillingRequestViewBillingPaginateTypeDef(TypedDict):
    Start: NotRequired[TimestampTypeDef]
    End: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOperationsResponseTypeDef(TypedDict):
    Operations: List[OperationSummaryTypeDef]
    NextPageMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForDomainResponseTypeDef(TypedDict):
    TagList: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTagsForDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    TagsToUpdate: NotRequired[Sequence[TagTypeDef]]


NameserverUnionTypeDef = Union[NameserverTypeDef, NameserverOutputTypeDef]


class UpdateDomainNameserversRequestRequestTypeDef(TypedDict):
    DomainName: str
    Nameservers: Sequence[NameserverTypeDef]
    FIAuthKey: NotRequired[str]


class GetDomainDetailResponseTypeDef(TypedDict):
    DomainName: str
    Nameservers: List[NameserverOutputTypeDef]
    AutoRenew: bool
    AdminContact: ContactDetailOutputTypeDef
    RegistrantContact: ContactDetailOutputTypeDef
    TechContact: ContactDetailOutputTypeDef
    AdminPrivacy: bool
    RegistrantPrivacy: bool
    TechPrivacy: bool
    RegistrarName: str
    WhoIsServer: str
    RegistrarUrl: str
    AbuseContactEmail: str
    AbuseContactPhone: str
    RegistryDomainId: str
    CreationDate: datetime
    UpdatedDate: datetime
    ExpirationDate: datetime
    Reseller: str
    DnsSec: str
    StatusList: List[str]
    DnssecKeys: List[DnssecKeyTypeDef]
    BillingContact: ContactDetailOutputTypeDef
    BillingPrivacy: bool
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    DurationInYears: int
    AdminContact: ContactDetailTypeDef
    RegistrantContact: ContactDetailTypeDef
    TechContact: ContactDetailTypeDef
    IdnLangCode: NotRequired[str]
    AutoRenew: NotRequired[bool]
    PrivacyProtectAdminContact: NotRequired[bool]
    PrivacyProtectRegistrantContact: NotRequired[bool]
    PrivacyProtectTechContact: NotRequired[bool]
    BillingContact: NotRequired[ContactDetailTypeDef]
    PrivacyProtectBillingContact: NotRequired[bool]


class UpdateDomainContactRequestRequestTypeDef(TypedDict):
    DomainName: str
    AdminContact: NotRequired[ContactDetailTypeDef]
    RegistrantContact: NotRequired[ContactDetailTypeDef]
    TechContact: NotRequired[ContactDetailTypeDef]
    Consent: NotRequired[ConsentTypeDef]
    BillingContact: NotRequired[ContactDetailTypeDef]


class ListPricesResponseTypeDef(TypedDict):
    Prices: List[DomainPriceTypeDef]
    NextPageMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class TransferDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    DurationInYears: int
    AdminContact: ContactDetailTypeDef
    RegistrantContact: ContactDetailTypeDef
    TechContact: ContactDetailTypeDef
    IdnLangCode: NotRequired[str]
    Nameservers: NotRequired[Sequence[NameserverUnionTypeDef]]
    AuthCode: NotRequired[str]
    AutoRenew: NotRequired[bool]
    PrivacyProtectAdminContact: NotRequired[bool]
    PrivacyProtectRegistrantContact: NotRequired[bool]
    PrivacyProtectTechContact: NotRequired[bool]
    BillingContact: NotRequired[ContactDetailTypeDef]
    PrivacyProtectBillingContact: NotRequired[bool]
