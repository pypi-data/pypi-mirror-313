"""
Type annotations for acm service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/type_defs/)

Usage::

    ```python
    from mypy_boto3_acm.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    CertificateStatusType,
    CertificateTransparencyLoggingPreferenceType,
    CertificateTypeType,
    DomainStatusType,
    ExtendedKeyUsageNameType,
    FailureReasonType,
    KeyAlgorithmType,
    KeyUsageNameType,
    RenewalEligibilityType,
    RenewalStatusType,
    RevocationReasonType,
    SortOrderType,
    ValidationMethodType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AddTagsToCertificateRequestRequestTypeDef",
    "BlobTypeDef",
    "CertificateDetailTypeDef",
    "CertificateOptionsTypeDef",
    "CertificateSummaryTypeDef",
    "DeleteCertificateRequestRequestTypeDef",
    "DescribeCertificateRequestCertificateValidatedWaitTypeDef",
    "DescribeCertificateRequestRequestTypeDef",
    "DescribeCertificateResponseTypeDef",
    "DomainValidationOptionTypeDef",
    "DomainValidationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExpiryEventsConfigurationTypeDef",
    "ExportCertificateRequestRequestTypeDef",
    "ExportCertificateResponseTypeDef",
    "ExtendedKeyUsageTypeDef",
    "FiltersTypeDef",
    "GetAccountConfigurationResponseTypeDef",
    "GetCertificateRequestRequestTypeDef",
    "GetCertificateResponseTypeDef",
    "ImportCertificateRequestRequestTypeDef",
    "ImportCertificateResponseTypeDef",
    "KeyUsageTypeDef",
    "ListCertificatesRequestListCertificatesPaginateTypeDef",
    "ListCertificatesRequestRequestTypeDef",
    "ListCertificatesResponseTypeDef",
    "ListTagsForCertificateRequestRequestTypeDef",
    "ListTagsForCertificateResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutAccountConfigurationRequestRequestTypeDef",
    "RemoveTagsFromCertificateRequestRequestTypeDef",
    "RenewCertificateRequestRequestTypeDef",
    "RenewalSummaryTypeDef",
    "RequestCertificateRequestRequestTypeDef",
    "RequestCertificateResponseTypeDef",
    "ResendValidationEmailRequestRequestTypeDef",
    "ResourceRecordTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "UpdateCertificateOptionsRequestRequestTypeDef",
    "WaiterConfigTypeDef",
)

class TagTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class CertificateOptionsTypeDef(TypedDict):
    CertificateTransparencyLoggingPreference: NotRequired[
        CertificateTransparencyLoggingPreferenceType
    ]

class ExtendedKeyUsageTypeDef(TypedDict):
    Name: NotRequired[ExtendedKeyUsageNameType]
    OID: NotRequired[str]

class KeyUsageTypeDef(TypedDict):
    Name: NotRequired[KeyUsageNameType]

CertificateSummaryTypeDef = TypedDict(
    "CertificateSummaryTypeDef",
    {
        "CertificateArn": NotRequired[str],
        "DomainName": NotRequired[str],
        "SubjectAlternativeNameSummaries": NotRequired[List[str]],
        "HasAdditionalSubjectAlternativeNames": NotRequired[bool],
        "Status": NotRequired[CertificateStatusType],
        "Type": NotRequired[CertificateTypeType],
        "KeyAlgorithm": NotRequired[KeyAlgorithmType],
        "KeyUsages": NotRequired[List[KeyUsageNameType]],
        "ExtendedKeyUsages": NotRequired[List[ExtendedKeyUsageNameType]],
        "InUse": NotRequired[bool],
        "Exported": NotRequired[bool],
        "RenewalEligibility": NotRequired[RenewalEligibilityType],
        "NotBefore": NotRequired[datetime],
        "NotAfter": NotRequired[datetime],
        "CreatedAt": NotRequired[datetime],
        "IssuedAt": NotRequired[datetime],
        "ImportedAt": NotRequired[datetime],
        "RevokedAt": NotRequired[datetime],
    },
)

class DeleteCertificateRequestRequestTypeDef(TypedDict):
    CertificateArn: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class DescribeCertificateRequestRequestTypeDef(TypedDict):
    CertificateArn: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DomainValidationOptionTypeDef(TypedDict):
    DomainName: str
    ValidationDomain: str

ResourceRecordTypeDef = TypedDict(
    "ResourceRecordTypeDef",
    {
        "Name": str,
        "Type": Literal["CNAME"],
        "Value": str,
    },
)

class ExpiryEventsConfigurationTypeDef(TypedDict):
    DaysBeforeExpiry: NotRequired[int]

class FiltersTypeDef(TypedDict):
    extendedKeyUsage: NotRequired[Sequence[ExtendedKeyUsageNameType]]
    keyUsage: NotRequired[Sequence[KeyUsageNameType]]
    keyTypes: NotRequired[Sequence[KeyAlgorithmType]]

class GetCertificateRequestRequestTypeDef(TypedDict):
    CertificateArn: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListTagsForCertificateRequestRequestTypeDef(TypedDict):
    CertificateArn: str

class RenewCertificateRequestRequestTypeDef(TypedDict):
    CertificateArn: str

class ResendValidationEmailRequestRequestTypeDef(TypedDict):
    CertificateArn: str
    Domain: str
    ValidationDomain: str

class AddTagsToCertificateRequestRequestTypeDef(TypedDict):
    CertificateArn: str
    Tags: Sequence[TagTypeDef]

class RemoveTagsFromCertificateRequestRequestTypeDef(TypedDict):
    CertificateArn: str
    Tags: Sequence[TagTypeDef]

class ExportCertificateRequestRequestTypeDef(TypedDict):
    CertificateArn: str
    Passphrase: BlobTypeDef

class ImportCertificateRequestRequestTypeDef(TypedDict):
    Certificate: BlobTypeDef
    PrivateKey: BlobTypeDef
    CertificateArn: NotRequired[str]
    CertificateChain: NotRequired[BlobTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class UpdateCertificateOptionsRequestRequestTypeDef(TypedDict):
    CertificateArn: str
    Options: CertificateOptionsTypeDef

class DescribeCertificateRequestCertificateValidatedWaitTypeDef(TypedDict):
    CertificateArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ExportCertificateResponseTypeDef(TypedDict):
    Certificate: str
    CertificateChain: str
    PrivateKey: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetCertificateResponseTypeDef(TypedDict):
    Certificate: str
    CertificateChain: str
    ResponseMetadata: ResponseMetadataTypeDef

class ImportCertificateResponseTypeDef(TypedDict):
    CertificateArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListCertificatesResponseTypeDef(TypedDict):
    CertificateSummaryList: List[CertificateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForCertificateResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RequestCertificateResponseTypeDef(TypedDict):
    CertificateArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class RequestCertificateRequestRequestTypeDef(TypedDict):
    DomainName: str
    ValidationMethod: NotRequired[ValidationMethodType]
    SubjectAlternativeNames: NotRequired[Sequence[str]]
    IdempotencyToken: NotRequired[str]
    DomainValidationOptions: NotRequired[Sequence[DomainValidationOptionTypeDef]]
    Options: NotRequired[CertificateOptionsTypeDef]
    CertificateAuthorityArn: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    KeyAlgorithm: NotRequired[KeyAlgorithmType]

class DomainValidationTypeDef(TypedDict):
    DomainName: str
    ValidationEmails: NotRequired[List[str]]
    ValidationDomain: NotRequired[str]
    ValidationStatus: NotRequired[DomainStatusType]
    ResourceRecord: NotRequired[ResourceRecordTypeDef]
    ValidationMethod: NotRequired[ValidationMethodType]

class GetAccountConfigurationResponseTypeDef(TypedDict):
    ExpiryEvents: ExpiryEventsConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutAccountConfigurationRequestRequestTypeDef(TypedDict):
    IdempotencyToken: str
    ExpiryEvents: NotRequired[ExpiryEventsConfigurationTypeDef]

class ListCertificatesRequestRequestTypeDef(TypedDict):
    CertificateStatuses: NotRequired[Sequence[CertificateStatusType]]
    Includes: NotRequired[FiltersTypeDef]
    NextToken: NotRequired[str]
    MaxItems: NotRequired[int]
    SortBy: NotRequired[Literal["CREATED_AT"]]
    SortOrder: NotRequired[SortOrderType]

class ListCertificatesRequestListCertificatesPaginateTypeDef(TypedDict):
    CertificateStatuses: NotRequired[Sequence[CertificateStatusType]]
    Includes: NotRequired[FiltersTypeDef]
    SortBy: NotRequired[Literal["CREATED_AT"]]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class RenewalSummaryTypeDef(TypedDict):
    RenewalStatus: RenewalStatusType
    DomainValidationOptions: List[DomainValidationTypeDef]
    UpdatedAt: datetime
    RenewalStatusReason: NotRequired[FailureReasonType]

CertificateDetailTypeDef = TypedDict(
    "CertificateDetailTypeDef",
    {
        "CertificateArn": NotRequired[str],
        "DomainName": NotRequired[str],
        "SubjectAlternativeNames": NotRequired[List[str]],
        "DomainValidationOptions": NotRequired[List[DomainValidationTypeDef]],
        "Serial": NotRequired[str],
        "Subject": NotRequired[str],
        "Issuer": NotRequired[str],
        "CreatedAt": NotRequired[datetime],
        "IssuedAt": NotRequired[datetime],
        "ImportedAt": NotRequired[datetime],
        "Status": NotRequired[CertificateStatusType],
        "RevokedAt": NotRequired[datetime],
        "RevocationReason": NotRequired[RevocationReasonType],
        "NotBefore": NotRequired[datetime],
        "NotAfter": NotRequired[datetime],
        "KeyAlgorithm": NotRequired[KeyAlgorithmType],
        "SignatureAlgorithm": NotRequired[str],
        "InUseBy": NotRequired[List[str]],
        "FailureReason": NotRequired[FailureReasonType],
        "Type": NotRequired[CertificateTypeType],
        "RenewalSummary": NotRequired[RenewalSummaryTypeDef],
        "KeyUsages": NotRequired[List[KeyUsageTypeDef]],
        "ExtendedKeyUsages": NotRequired[List[ExtendedKeyUsageTypeDef]],
        "CertificateAuthorityArn": NotRequired[str],
        "RenewalEligibility": NotRequired[RenewalEligibilityType],
        "Options": NotRequired[CertificateOptionsTypeDef],
    },
)

class DescribeCertificateResponseTypeDef(TypedDict):
    Certificate: CertificateDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
