"""
Type annotations for pca-connector-ad service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/type_defs/)

Usage::

    ```python
    from mypy_boto3_pca_connector_ad.type_defs import AccessRightsTypeDef

    data: AccessRightsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AccessRightType,
    ApplicationPolicyTypeType,
    ClientCompatibilityV2Type,
    ClientCompatibilityV3Type,
    ClientCompatibilityV4Type,
    ConnectorStatusReasonType,
    ConnectorStatusType,
    DirectoryRegistrationStatusReasonType,
    DirectoryRegistrationStatusType,
    HashAlgorithmType,
    KeySpecType,
    PrivateKeyAlgorithmType,
    ServicePrincipalNameStatusReasonType,
    ServicePrincipalNameStatusType,
    TemplateStatusType,
    ValidityPeriodTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccessControlEntrySummaryTypeDef",
    "AccessControlEntryTypeDef",
    "AccessRightsTypeDef",
    "ApplicationPoliciesOutputTypeDef",
    "ApplicationPoliciesTypeDef",
    "ApplicationPoliciesUnionTypeDef",
    "ApplicationPolicyTypeDef",
    "CertificateValidityTypeDef",
    "ConnectorSummaryTypeDef",
    "ConnectorTypeDef",
    "CreateConnectorRequestRequestTypeDef",
    "CreateConnectorResponseTypeDef",
    "CreateDirectoryRegistrationRequestRequestTypeDef",
    "CreateDirectoryRegistrationResponseTypeDef",
    "CreateServicePrincipalNameRequestRequestTypeDef",
    "CreateTemplateGroupAccessControlEntryRequestRequestTypeDef",
    "CreateTemplateRequestRequestTypeDef",
    "CreateTemplateResponseTypeDef",
    "DeleteConnectorRequestRequestTypeDef",
    "DeleteDirectoryRegistrationRequestRequestTypeDef",
    "DeleteServicePrincipalNameRequestRequestTypeDef",
    "DeleteTemplateGroupAccessControlEntryRequestRequestTypeDef",
    "DeleteTemplateRequestRequestTypeDef",
    "DirectoryRegistrationSummaryTypeDef",
    "DirectoryRegistrationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnrollmentFlagsV2TypeDef",
    "EnrollmentFlagsV3TypeDef",
    "EnrollmentFlagsV4TypeDef",
    "ExtensionsV2OutputTypeDef",
    "ExtensionsV2TypeDef",
    "ExtensionsV2UnionTypeDef",
    "ExtensionsV3OutputTypeDef",
    "ExtensionsV3TypeDef",
    "ExtensionsV3UnionTypeDef",
    "ExtensionsV4OutputTypeDef",
    "ExtensionsV4TypeDef",
    "ExtensionsV4UnionTypeDef",
    "GeneralFlagsV2TypeDef",
    "GeneralFlagsV3TypeDef",
    "GeneralFlagsV4TypeDef",
    "GetConnectorRequestRequestTypeDef",
    "GetConnectorResponseTypeDef",
    "GetDirectoryRegistrationRequestRequestTypeDef",
    "GetDirectoryRegistrationResponseTypeDef",
    "GetServicePrincipalNameRequestRequestTypeDef",
    "GetServicePrincipalNameResponseTypeDef",
    "GetTemplateGroupAccessControlEntryRequestRequestTypeDef",
    "GetTemplateGroupAccessControlEntryResponseTypeDef",
    "GetTemplateRequestRequestTypeDef",
    "GetTemplateResponseTypeDef",
    "KeyUsageFlagsTypeDef",
    "KeyUsagePropertyFlagsTypeDef",
    "KeyUsagePropertyTypeDef",
    "KeyUsageTypeDef",
    "ListConnectorsRequestListConnectorsPaginateTypeDef",
    "ListConnectorsRequestRequestTypeDef",
    "ListConnectorsResponseTypeDef",
    "ListDirectoryRegistrationsRequestListDirectoryRegistrationsPaginateTypeDef",
    "ListDirectoryRegistrationsRequestRequestTypeDef",
    "ListDirectoryRegistrationsResponseTypeDef",
    "ListServicePrincipalNamesRequestListServicePrincipalNamesPaginateTypeDef",
    "ListServicePrincipalNamesRequestRequestTypeDef",
    "ListServicePrincipalNamesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTemplateGroupAccessControlEntriesRequestListTemplateGroupAccessControlEntriesPaginateTypeDef",
    "ListTemplateGroupAccessControlEntriesRequestRequestTypeDef",
    "ListTemplateGroupAccessControlEntriesResponseTypeDef",
    "ListTemplatesRequestListTemplatesPaginateTypeDef",
    "ListTemplatesRequestRequestTypeDef",
    "ListTemplatesResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PrivateKeyAttributesV2OutputTypeDef",
    "PrivateKeyAttributesV2TypeDef",
    "PrivateKeyAttributesV2UnionTypeDef",
    "PrivateKeyAttributesV3OutputTypeDef",
    "PrivateKeyAttributesV3TypeDef",
    "PrivateKeyAttributesV3UnionTypeDef",
    "PrivateKeyAttributesV4OutputTypeDef",
    "PrivateKeyAttributesV4TypeDef",
    "PrivateKeyAttributesV4UnionTypeDef",
    "PrivateKeyFlagsV2TypeDef",
    "PrivateKeyFlagsV3TypeDef",
    "PrivateKeyFlagsV4TypeDef",
    "ResponseMetadataTypeDef",
    "ServicePrincipalNameSummaryTypeDef",
    "ServicePrincipalNameTypeDef",
    "SubjectNameFlagsV2TypeDef",
    "SubjectNameFlagsV3TypeDef",
    "SubjectNameFlagsV4TypeDef",
    "TagResourceRequestRequestTypeDef",
    "TemplateDefinitionOutputTypeDef",
    "TemplateDefinitionTypeDef",
    "TemplateRevisionTypeDef",
    "TemplateSummaryTypeDef",
    "TemplateTypeDef",
    "TemplateV2OutputTypeDef",
    "TemplateV2TypeDef",
    "TemplateV2UnionTypeDef",
    "TemplateV3OutputTypeDef",
    "TemplateV3TypeDef",
    "TemplateV3UnionTypeDef",
    "TemplateV4OutputTypeDef",
    "TemplateV4TypeDef",
    "TemplateV4UnionTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateTemplateGroupAccessControlEntryRequestRequestTypeDef",
    "UpdateTemplateRequestRequestTypeDef",
    "ValidityPeriodTypeDef",
    "VpcInformationOutputTypeDef",
    "VpcInformationTypeDef",
)

class AccessRightsTypeDef(TypedDict):
    AutoEnroll: NotRequired[AccessRightType]
    Enroll: NotRequired[AccessRightType]

class ApplicationPolicyTypeDef(TypedDict):
    PolicyObjectIdentifier: NotRequired[str]
    PolicyType: NotRequired[ApplicationPolicyTypeType]

class ValidityPeriodTypeDef(TypedDict):
    Period: int
    PeriodType: ValidityPeriodTypeType

class VpcInformationOutputTypeDef(TypedDict):
    SecurityGroupIds: List[str]

class VpcInformationTypeDef(TypedDict):
    SecurityGroupIds: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateDirectoryRegistrationRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class CreateServicePrincipalNameRequestRequestTypeDef(TypedDict):
    ConnectorArn: str
    DirectoryRegistrationArn: str
    ClientToken: NotRequired[str]

class DeleteConnectorRequestRequestTypeDef(TypedDict):
    ConnectorArn: str

class DeleteDirectoryRegistrationRequestRequestTypeDef(TypedDict):
    DirectoryRegistrationArn: str

class DeleteServicePrincipalNameRequestRequestTypeDef(TypedDict):
    ConnectorArn: str
    DirectoryRegistrationArn: str

class DeleteTemplateGroupAccessControlEntryRequestRequestTypeDef(TypedDict):
    GroupSecurityIdentifier: str
    TemplateArn: str

class DeleteTemplateRequestRequestTypeDef(TypedDict):
    TemplateArn: str

class DirectoryRegistrationSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    DirectoryId: NotRequired[str]
    Status: NotRequired[DirectoryRegistrationStatusType]
    StatusReason: NotRequired[DirectoryRegistrationStatusReasonType]
    UpdatedAt: NotRequired[datetime]

class DirectoryRegistrationTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    DirectoryId: NotRequired[str]
    Status: NotRequired[DirectoryRegistrationStatusType]
    StatusReason: NotRequired[DirectoryRegistrationStatusReasonType]
    UpdatedAt: NotRequired[datetime]

class EnrollmentFlagsV2TypeDef(TypedDict):
    EnableKeyReuseOnNtTokenKeysetStorageFull: NotRequired[bool]
    IncludeSymmetricAlgorithms: NotRequired[bool]
    NoSecurityExtension: NotRequired[bool]
    RemoveInvalidCertificateFromPersonalStore: NotRequired[bool]
    UserInteractionRequired: NotRequired[bool]

class EnrollmentFlagsV3TypeDef(TypedDict):
    EnableKeyReuseOnNtTokenKeysetStorageFull: NotRequired[bool]
    IncludeSymmetricAlgorithms: NotRequired[bool]
    NoSecurityExtension: NotRequired[bool]
    RemoveInvalidCertificateFromPersonalStore: NotRequired[bool]
    UserInteractionRequired: NotRequired[bool]

class EnrollmentFlagsV4TypeDef(TypedDict):
    EnableKeyReuseOnNtTokenKeysetStorageFull: NotRequired[bool]
    IncludeSymmetricAlgorithms: NotRequired[bool]
    NoSecurityExtension: NotRequired[bool]
    RemoveInvalidCertificateFromPersonalStore: NotRequired[bool]
    UserInteractionRequired: NotRequired[bool]

class GeneralFlagsV2TypeDef(TypedDict):
    AutoEnrollment: NotRequired[bool]
    MachineType: NotRequired[bool]

class GeneralFlagsV3TypeDef(TypedDict):
    AutoEnrollment: NotRequired[bool]
    MachineType: NotRequired[bool]

class GeneralFlagsV4TypeDef(TypedDict):
    AutoEnrollment: NotRequired[bool]
    MachineType: NotRequired[bool]

class GetConnectorRequestRequestTypeDef(TypedDict):
    ConnectorArn: str

class GetDirectoryRegistrationRequestRequestTypeDef(TypedDict):
    DirectoryRegistrationArn: str

class GetServicePrincipalNameRequestRequestTypeDef(TypedDict):
    ConnectorArn: str
    DirectoryRegistrationArn: str

class ServicePrincipalNameTypeDef(TypedDict):
    ConnectorArn: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    DirectoryRegistrationArn: NotRequired[str]
    Status: NotRequired[ServicePrincipalNameStatusType]
    StatusReason: NotRequired[ServicePrincipalNameStatusReasonType]
    UpdatedAt: NotRequired[datetime]

class GetTemplateGroupAccessControlEntryRequestRequestTypeDef(TypedDict):
    GroupSecurityIdentifier: str
    TemplateArn: str

class GetTemplateRequestRequestTypeDef(TypedDict):
    TemplateArn: str

class KeyUsageFlagsTypeDef(TypedDict):
    DataEncipherment: NotRequired[bool]
    DigitalSignature: NotRequired[bool]
    KeyAgreement: NotRequired[bool]
    KeyEncipherment: NotRequired[bool]
    NonRepudiation: NotRequired[bool]

class KeyUsagePropertyFlagsTypeDef(TypedDict):
    Decrypt: NotRequired[bool]
    KeyAgreement: NotRequired[bool]
    Sign: NotRequired[bool]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListConnectorsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListDirectoryRegistrationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListServicePrincipalNamesRequestRequestTypeDef(TypedDict):
    DirectoryRegistrationArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ServicePrincipalNameSummaryTypeDef(TypedDict):
    ConnectorArn: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    DirectoryRegistrationArn: NotRequired[str]
    Status: NotRequired[ServicePrincipalNameStatusType]
    StatusReason: NotRequired[ServicePrincipalNameStatusReasonType]
    UpdatedAt: NotRequired[datetime]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class ListTemplateGroupAccessControlEntriesRequestRequestTypeDef(TypedDict):
    TemplateArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTemplatesRequestRequestTypeDef(TypedDict):
    ConnectorArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class PrivateKeyAttributesV2OutputTypeDef(TypedDict):
    KeySpec: KeySpecType
    MinimalKeyLength: int
    CryptoProviders: NotRequired[List[str]]

class PrivateKeyAttributesV2TypeDef(TypedDict):
    KeySpec: KeySpecType
    MinimalKeyLength: int
    CryptoProviders: NotRequired[Sequence[str]]

class PrivateKeyFlagsV2TypeDef(TypedDict):
    ClientVersion: ClientCompatibilityV2Type
    ExportableKey: NotRequired[bool]
    StrongKeyProtectionRequired: NotRequired[bool]

class PrivateKeyFlagsV3TypeDef(TypedDict):
    ClientVersion: ClientCompatibilityV3Type
    ExportableKey: NotRequired[bool]
    RequireAlternateSignatureAlgorithm: NotRequired[bool]
    StrongKeyProtectionRequired: NotRequired[bool]

class PrivateKeyFlagsV4TypeDef(TypedDict):
    ClientVersion: ClientCompatibilityV4Type
    ExportableKey: NotRequired[bool]
    RequireAlternateSignatureAlgorithm: NotRequired[bool]
    RequireSameKeyRenewal: NotRequired[bool]
    StrongKeyProtectionRequired: NotRequired[bool]
    UseLegacyProvider: NotRequired[bool]

class SubjectNameFlagsV2TypeDef(TypedDict):
    RequireCommonName: NotRequired[bool]
    RequireDirectoryPath: NotRequired[bool]
    RequireDnsAsCn: NotRequired[bool]
    RequireEmail: NotRequired[bool]
    SanRequireDirectoryGuid: NotRequired[bool]
    SanRequireDns: NotRequired[bool]
    SanRequireDomainDns: NotRequired[bool]
    SanRequireEmail: NotRequired[bool]
    SanRequireSpn: NotRequired[bool]
    SanRequireUpn: NotRequired[bool]

class SubjectNameFlagsV3TypeDef(TypedDict):
    RequireCommonName: NotRequired[bool]
    RequireDirectoryPath: NotRequired[bool]
    RequireDnsAsCn: NotRequired[bool]
    RequireEmail: NotRequired[bool]
    SanRequireDirectoryGuid: NotRequired[bool]
    SanRequireDns: NotRequired[bool]
    SanRequireDomainDns: NotRequired[bool]
    SanRequireEmail: NotRequired[bool]
    SanRequireSpn: NotRequired[bool]
    SanRequireUpn: NotRequired[bool]

class SubjectNameFlagsV4TypeDef(TypedDict):
    RequireCommonName: NotRequired[bool]
    RequireDirectoryPath: NotRequired[bool]
    RequireDnsAsCn: NotRequired[bool]
    RequireEmail: NotRequired[bool]
    SanRequireDirectoryGuid: NotRequired[bool]
    SanRequireDns: NotRequired[bool]
    SanRequireDomainDns: NotRequired[bool]
    SanRequireEmail: NotRequired[bool]
    SanRequireSpn: NotRequired[bool]
    SanRequireUpn: NotRequired[bool]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class TemplateRevisionTypeDef(TypedDict):
    MajorRevision: int
    MinorRevision: int

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class AccessControlEntrySummaryTypeDef(TypedDict):
    AccessRights: NotRequired[AccessRightsTypeDef]
    CreatedAt: NotRequired[datetime]
    GroupDisplayName: NotRequired[str]
    GroupSecurityIdentifier: NotRequired[str]
    TemplateArn: NotRequired[str]
    UpdatedAt: NotRequired[datetime]

class AccessControlEntryTypeDef(TypedDict):
    AccessRights: NotRequired[AccessRightsTypeDef]
    CreatedAt: NotRequired[datetime]
    GroupDisplayName: NotRequired[str]
    GroupSecurityIdentifier: NotRequired[str]
    TemplateArn: NotRequired[str]
    UpdatedAt: NotRequired[datetime]

class CreateTemplateGroupAccessControlEntryRequestRequestTypeDef(TypedDict):
    AccessRights: AccessRightsTypeDef
    GroupDisplayName: str
    GroupSecurityIdentifier: str
    TemplateArn: str
    ClientToken: NotRequired[str]

class UpdateTemplateGroupAccessControlEntryRequestRequestTypeDef(TypedDict):
    GroupSecurityIdentifier: str
    TemplateArn: str
    AccessRights: NotRequired[AccessRightsTypeDef]
    GroupDisplayName: NotRequired[str]

class ApplicationPoliciesOutputTypeDef(TypedDict):
    Policies: List[ApplicationPolicyTypeDef]
    Critical: NotRequired[bool]

class ApplicationPoliciesTypeDef(TypedDict):
    Policies: Sequence[ApplicationPolicyTypeDef]
    Critical: NotRequired[bool]

class CertificateValidityTypeDef(TypedDict):
    RenewalPeriod: ValidityPeriodTypeDef
    ValidityPeriod: ValidityPeriodTypeDef

class ConnectorSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    CertificateAuthorityArn: NotRequired[str]
    CertificateEnrollmentPolicyServerEndpoint: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    DirectoryId: NotRequired[str]
    Status: NotRequired[ConnectorStatusType]
    StatusReason: NotRequired[ConnectorStatusReasonType]
    UpdatedAt: NotRequired[datetime]
    VpcInformation: NotRequired[VpcInformationOutputTypeDef]

class ConnectorTypeDef(TypedDict):
    Arn: NotRequired[str]
    CertificateAuthorityArn: NotRequired[str]
    CertificateEnrollmentPolicyServerEndpoint: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    DirectoryId: NotRequired[str]
    Status: NotRequired[ConnectorStatusType]
    StatusReason: NotRequired[ConnectorStatusReasonType]
    UpdatedAt: NotRequired[datetime]
    VpcInformation: NotRequired[VpcInformationOutputTypeDef]

class CreateConnectorRequestRequestTypeDef(TypedDict):
    CertificateAuthorityArn: str
    DirectoryId: str
    VpcInformation: VpcInformationTypeDef
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class CreateConnectorResponseTypeDef(TypedDict):
    ConnectorArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDirectoryRegistrationResponseTypeDef(TypedDict):
    DirectoryRegistrationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTemplateResponseTypeDef(TypedDict):
    TemplateArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListDirectoryRegistrationsResponseTypeDef(TypedDict):
    DirectoryRegistrations: List[DirectoryRegistrationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetDirectoryRegistrationResponseTypeDef(TypedDict):
    DirectoryRegistration: DirectoryRegistrationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetServicePrincipalNameResponseTypeDef(TypedDict):
    ServicePrincipalName: ServicePrincipalNameTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class KeyUsageTypeDef(TypedDict):
    UsageFlags: KeyUsageFlagsTypeDef
    Critical: NotRequired[bool]

class KeyUsagePropertyTypeDef(TypedDict):
    PropertyFlags: NotRequired[KeyUsagePropertyFlagsTypeDef]
    PropertyType: NotRequired[Literal["ALL"]]

class ListConnectorsRequestListConnectorsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDirectoryRegistrationsRequestListDirectoryRegistrationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServicePrincipalNamesRequestListServicePrincipalNamesPaginateTypeDef(TypedDict):
    DirectoryRegistrationArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTemplateGroupAccessControlEntriesRequestListTemplateGroupAccessControlEntriesPaginateTypeDef(
    TypedDict
):
    TemplateArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTemplatesRequestListTemplatesPaginateTypeDef(TypedDict):
    ConnectorArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServicePrincipalNamesResponseTypeDef(TypedDict):
    ServicePrincipalNames: List[ServicePrincipalNameSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

PrivateKeyAttributesV2UnionTypeDef = Union[
    PrivateKeyAttributesV2TypeDef, PrivateKeyAttributesV2OutputTypeDef
]

class ListTemplateGroupAccessControlEntriesResponseTypeDef(TypedDict):
    AccessControlEntries: List[AccessControlEntrySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetTemplateGroupAccessControlEntryResponseTypeDef(TypedDict):
    AccessControlEntry: AccessControlEntryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ApplicationPoliciesUnionTypeDef = Union[
    ApplicationPoliciesTypeDef, ApplicationPoliciesOutputTypeDef
]

class ListConnectorsResponseTypeDef(TypedDict):
    Connectors: List[ConnectorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetConnectorResponseTypeDef(TypedDict):
    Connector: ConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExtensionsV2OutputTypeDef(TypedDict):
    KeyUsage: KeyUsageTypeDef
    ApplicationPolicies: NotRequired[ApplicationPoliciesOutputTypeDef]

class ExtensionsV3OutputTypeDef(TypedDict):
    KeyUsage: KeyUsageTypeDef
    ApplicationPolicies: NotRequired[ApplicationPoliciesOutputTypeDef]

class ExtensionsV4OutputTypeDef(TypedDict):
    KeyUsage: KeyUsageTypeDef
    ApplicationPolicies: NotRequired[ApplicationPoliciesOutputTypeDef]

class PrivateKeyAttributesV3OutputTypeDef(TypedDict):
    Algorithm: PrivateKeyAlgorithmType
    KeySpec: KeySpecType
    KeyUsageProperty: KeyUsagePropertyTypeDef
    MinimalKeyLength: int
    CryptoProviders: NotRequired[List[str]]

class PrivateKeyAttributesV3TypeDef(TypedDict):
    Algorithm: PrivateKeyAlgorithmType
    KeySpec: KeySpecType
    KeyUsageProperty: KeyUsagePropertyTypeDef
    MinimalKeyLength: int
    CryptoProviders: NotRequired[Sequence[str]]

class PrivateKeyAttributesV4OutputTypeDef(TypedDict):
    KeySpec: KeySpecType
    MinimalKeyLength: int
    Algorithm: NotRequired[PrivateKeyAlgorithmType]
    CryptoProviders: NotRequired[List[str]]
    KeyUsageProperty: NotRequired[KeyUsagePropertyTypeDef]

class PrivateKeyAttributesV4TypeDef(TypedDict):
    KeySpec: KeySpecType
    MinimalKeyLength: int
    Algorithm: NotRequired[PrivateKeyAlgorithmType]
    CryptoProviders: NotRequired[Sequence[str]]
    KeyUsageProperty: NotRequired[KeyUsagePropertyTypeDef]

class ExtensionsV2TypeDef(TypedDict):
    KeyUsage: KeyUsageTypeDef
    ApplicationPolicies: NotRequired[ApplicationPoliciesUnionTypeDef]

class ExtensionsV3TypeDef(TypedDict):
    KeyUsage: KeyUsageTypeDef
    ApplicationPolicies: NotRequired[ApplicationPoliciesUnionTypeDef]

class ExtensionsV4TypeDef(TypedDict):
    KeyUsage: KeyUsageTypeDef
    ApplicationPolicies: NotRequired[ApplicationPoliciesUnionTypeDef]

class TemplateV2OutputTypeDef(TypedDict):
    CertificateValidity: CertificateValidityTypeDef
    EnrollmentFlags: EnrollmentFlagsV2TypeDef
    Extensions: ExtensionsV2OutputTypeDef
    GeneralFlags: GeneralFlagsV2TypeDef
    PrivateKeyAttributes: PrivateKeyAttributesV2OutputTypeDef
    PrivateKeyFlags: PrivateKeyFlagsV2TypeDef
    SubjectNameFlags: SubjectNameFlagsV2TypeDef
    SupersededTemplates: NotRequired[List[str]]

class TemplateV3OutputTypeDef(TypedDict):
    CertificateValidity: CertificateValidityTypeDef
    EnrollmentFlags: EnrollmentFlagsV3TypeDef
    Extensions: ExtensionsV3OutputTypeDef
    GeneralFlags: GeneralFlagsV3TypeDef
    HashAlgorithm: HashAlgorithmType
    PrivateKeyAttributes: PrivateKeyAttributesV3OutputTypeDef
    PrivateKeyFlags: PrivateKeyFlagsV3TypeDef
    SubjectNameFlags: SubjectNameFlagsV3TypeDef
    SupersededTemplates: NotRequired[List[str]]

PrivateKeyAttributesV3UnionTypeDef = Union[
    PrivateKeyAttributesV3TypeDef, PrivateKeyAttributesV3OutputTypeDef
]

class TemplateV4OutputTypeDef(TypedDict):
    CertificateValidity: CertificateValidityTypeDef
    EnrollmentFlags: EnrollmentFlagsV4TypeDef
    Extensions: ExtensionsV4OutputTypeDef
    GeneralFlags: GeneralFlagsV4TypeDef
    PrivateKeyAttributes: PrivateKeyAttributesV4OutputTypeDef
    PrivateKeyFlags: PrivateKeyFlagsV4TypeDef
    SubjectNameFlags: SubjectNameFlagsV4TypeDef
    HashAlgorithm: NotRequired[HashAlgorithmType]
    SupersededTemplates: NotRequired[List[str]]

PrivateKeyAttributesV4UnionTypeDef = Union[
    PrivateKeyAttributesV4TypeDef, PrivateKeyAttributesV4OutputTypeDef
]
ExtensionsV2UnionTypeDef = Union[ExtensionsV2TypeDef, ExtensionsV2OutputTypeDef]
ExtensionsV3UnionTypeDef = Union[ExtensionsV3TypeDef, ExtensionsV3OutputTypeDef]
ExtensionsV4UnionTypeDef = Union[ExtensionsV4TypeDef, ExtensionsV4OutputTypeDef]

class TemplateDefinitionOutputTypeDef(TypedDict):
    TemplateV2: NotRequired[TemplateV2OutputTypeDef]
    TemplateV3: NotRequired[TemplateV3OutputTypeDef]
    TemplateV4: NotRequired[TemplateV4OutputTypeDef]

class TemplateV2TypeDef(TypedDict):
    CertificateValidity: CertificateValidityTypeDef
    EnrollmentFlags: EnrollmentFlagsV2TypeDef
    Extensions: ExtensionsV2UnionTypeDef
    GeneralFlags: GeneralFlagsV2TypeDef
    PrivateKeyAttributes: PrivateKeyAttributesV2UnionTypeDef
    PrivateKeyFlags: PrivateKeyFlagsV2TypeDef
    SubjectNameFlags: SubjectNameFlagsV2TypeDef
    SupersededTemplates: NotRequired[Sequence[str]]

class TemplateV3TypeDef(TypedDict):
    CertificateValidity: CertificateValidityTypeDef
    EnrollmentFlags: EnrollmentFlagsV3TypeDef
    Extensions: ExtensionsV3UnionTypeDef
    GeneralFlags: GeneralFlagsV3TypeDef
    HashAlgorithm: HashAlgorithmType
    PrivateKeyAttributes: PrivateKeyAttributesV3UnionTypeDef
    PrivateKeyFlags: PrivateKeyFlagsV3TypeDef
    SubjectNameFlags: SubjectNameFlagsV3TypeDef
    SupersededTemplates: NotRequired[Sequence[str]]

class TemplateV4TypeDef(TypedDict):
    CertificateValidity: CertificateValidityTypeDef
    EnrollmentFlags: EnrollmentFlagsV4TypeDef
    Extensions: ExtensionsV4UnionTypeDef
    GeneralFlags: GeneralFlagsV4TypeDef
    PrivateKeyAttributes: PrivateKeyAttributesV4UnionTypeDef
    PrivateKeyFlags: PrivateKeyFlagsV4TypeDef
    SubjectNameFlags: SubjectNameFlagsV4TypeDef
    HashAlgorithm: NotRequired[HashAlgorithmType]
    SupersededTemplates: NotRequired[Sequence[str]]

class TemplateSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    ConnectorArn: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    Definition: NotRequired[TemplateDefinitionOutputTypeDef]
    Name: NotRequired[str]
    ObjectIdentifier: NotRequired[str]
    PolicySchema: NotRequired[int]
    Revision: NotRequired[TemplateRevisionTypeDef]
    Status: NotRequired[TemplateStatusType]
    UpdatedAt: NotRequired[datetime]

class TemplateTypeDef(TypedDict):
    Arn: NotRequired[str]
    ConnectorArn: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    Definition: NotRequired[TemplateDefinitionOutputTypeDef]
    Name: NotRequired[str]
    ObjectIdentifier: NotRequired[str]
    PolicySchema: NotRequired[int]
    Revision: NotRequired[TemplateRevisionTypeDef]
    Status: NotRequired[TemplateStatusType]
    UpdatedAt: NotRequired[datetime]

TemplateV2UnionTypeDef = Union[TemplateV2TypeDef, TemplateV2OutputTypeDef]
TemplateV3UnionTypeDef = Union[TemplateV3TypeDef, TemplateV3OutputTypeDef]
TemplateV4UnionTypeDef = Union[TemplateV4TypeDef, TemplateV4OutputTypeDef]

class ListTemplatesResponseTypeDef(TypedDict):
    Templates: List[TemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetTemplateResponseTypeDef(TypedDict):
    Template: TemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class TemplateDefinitionTypeDef(TypedDict):
    TemplateV2: NotRequired[TemplateV2UnionTypeDef]
    TemplateV3: NotRequired[TemplateV3UnionTypeDef]
    TemplateV4: NotRequired[TemplateV4UnionTypeDef]

class CreateTemplateRequestRequestTypeDef(TypedDict):
    ConnectorArn: str
    Definition: TemplateDefinitionTypeDef
    Name: str
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class UpdateTemplateRequestRequestTypeDef(TypedDict):
    TemplateArn: str
    Definition: NotRequired[TemplateDefinitionTypeDef]
    ReenrollAllCertificateHolders: NotRequired[bool]
