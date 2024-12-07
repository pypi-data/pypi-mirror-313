"""
Type annotations for rolesanywhere service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rolesanywhere/type_defs/)

Usage::

    ```python
    from mypy_boto3_rolesanywhere.type_defs import MappingRuleTypeDef

    data: MappingRuleTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import CertificateFieldType, NotificationEventType, TrustAnchorTypeType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AttributeMappingTypeDef",
    "BlobTypeDef",
    "CreateProfileRequestRequestTypeDef",
    "CreateTrustAnchorRequestRequestTypeDef",
    "CredentialSummaryTypeDef",
    "CrlDetailResponseTypeDef",
    "CrlDetailTypeDef",
    "DeleteAttributeMappingRequestRequestTypeDef",
    "DeleteAttributeMappingResponseTypeDef",
    "ImportCrlRequestRequestTypeDef",
    "InstancePropertyTypeDef",
    "ListCrlsResponseTypeDef",
    "ListProfilesResponseTypeDef",
    "ListRequestListCrlsPaginateTypeDef",
    "ListRequestListProfilesPaginateTypeDef",
    "ListRequestListSubjectsPaginateTypeDef",
    "ListRequestListTrustAnchorsPaginateTypeDef",
    "ListRequestRequestTypeDef",
    "ListSubjectsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTrustAnchorsResponseTypeDef",
    "MappingRuleTypeDef",
    "NotificationSettingDetailTypeDef",
    "NotificationSettingKeyTypeDef",
    "NotificationSettingTypeDef",
    "PaginatorConfigTypeDef",
    "ProfileDetailResponseTypeDef",
    "ProfileDetailTypeDef",
    "PutAttributeMappingRequestRequestTypeDef",
    "PutAttributeMappingResponseTypeDef",
    "PutNotificationSettingsRequestRequestTypeDef",
    "PutNotificationSettingsResponseTypeDef",
    "ResetNotificationSettingsRequestRequestTypeDef",
    "ResetNotificationSettingsResponseTypeDef",
    "ResponseMetadataTypeDef",
    "ScalarCrlRequestRequestTypeDef",
    "ScalarProfileRequestRequestTypeDef",
    "ScalarSubjectRequestRequestTypeDef",
    "ScalarTrustAnchorRequestRequestTypeDef",
    "SourceDataTypeDef",
    "SourceTypeDef",
    "SubjectDetailResponseTypeDef",
    "SubjectDetailTypeDef",
    "SubjectSummaryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TrustAnchorDetailResponseTypeDef",
    "TrustAnchorDetailTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCrlRequestRequestTypeDef",
    "UpdateProfileRequestRequestTypeDef",
    "UpdateTrustAnchorRequestRequestTypeDef",
)

class MappingRuleTypeDef(TypedDict):
    specifier: str

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class TagTypeDef(TypedDict):
    key: str
    value: str

class NotificationSettingTypeDef(TypedDict):
    enabled: bool
    event: NotificationEventType
    channel: NotRequired[Literal["ALL"]]
    threshold: NotRequired[int]

class CredentialSummaryTypeDef(TypedDict):
    enabled: NotRequired[bool]
    failed: NotRequired[bool]
    issuer: NotRequired[str]
    seenAt: NotRequired[datetime]
    serialNumber: NotRequired[str]
    x509CertificateData: NotRequired[str]

class CrlDetailTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    crlArn: NotRequired[str]
    crlData: NotRequired[bytes]
    crlId: NotRequired[str]
    enabled: NotRequired[bool]
    name: NotRequired[str]
    trustAnchorArn: NotRequired[str]
    updatedAt: NotRequired[datetime]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteAttributeMappingRequestRequestTypeDef(TypedDict):
    certificateField: CertificateFieldType
    profileId: str
    specifiers: NotRequired[Sequence[str]]

class InstancePropertyTypeDef(TypedDict):
    failed: NotRequired[bool]
    properties: NotRequired[Dict[str, str]]
    seenAt: NotRequired[datetime]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    pageSize: NotRequired[int]

class SubjectSummaryTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    enabled: NotRequired[bool]
    lastSeenAt: NotRequired[datetime]
    subjectArn: NotRequired[str]
    subjectId: NotRequired[str]
    updatedAt: NotRequired[datetime]
    x509Subject: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class NotificationSettingDetailTypeDef(TypedDict):
    enabled: bool
    event: NotificationEventType
    channel: NotRequired[Literal["ALL"]]
    configuredBy: NotRequired[str]
    threshold: NotRequired[int]

class NotificationSettingKeyTypeDef(TypedDict):
    event: NotificationEventType
    channel: NotRequired[Literal["ALL"]]

class ScalarCrlRequestRequestTypeDef(TypedDict):
    crlId: str

class ScalarProfileRequestRequestTypeDef(TypedDict):
    profileId: str

class ScalarSubjectRequestRequestTypeDef(TypedDict):
    subjectId: str

class ScalarTrustAnchorRequestRequestTypeDef(TypedDict):
    trustAnchorId: str

class SourceDataTypeDef(TypedDict):
    acmPcaArn: NotRequired[str]
    x509CertificateData: NotRequired[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateProfileRequestRequestTypeDef(TypedDict):
    profileId: str
    acceptRoleSessionName: NotRequired[bool]
    durationSeconds: NotRequired[int]
    managedPolicyArns: NotRequired[Sequence[str]]
    name: NotRequired[str]
    roleArns: NotRequired[Sequence[str]]
    sessionPolicy: NotRequired[str]

class AttributeMappingTypeDef(TypedDict):
    certificateField: NotRequired[CertificateFieldType]
    mappingRules: NotRequired[List[MappingRuleTypeDef]]

class PutAttributeMappingRequestRequestTypeDef(TypedDict):
    certificateField: CertificateFieldType
    mappingRules: Sequence[MappingRuleTypeDef]
    profileId: str

class UpdateCrlRequestRequestTypeDef(TypedDict):
    crlId: str
    crlData: NotRequired[BlobTypeDef]
    name: NotRequired[str]

class CreateProfileRequestRequestTypeDef(TypedDict):
    name: str
    roleArns: Sequence[str]
    acceptRoleSessionName: NotRequired[bool]
    durationSeconds: NotRequired[int]
    enabled: NotRequired[bool]
    managedPolicyArns: NotRequired[Sequence[str]]
    requireInstanceProperties: NotRequired[bool]
    sessionPolicy: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class ImportCrlRequestRequestTypeDef(TypedDict):
    crlData: BlobTypeDef
    name: str
    trustAnchorArn: str
    enabled: NotRequired[bool]
    tags: NotRequired[Sequence[TagTypeDef]]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]

class PutNotificationSettingsRequestRequestTypeDef(TypedDict):
    notificationSettings: Sequence[NotificationSettingTypeDef]
    trustAnchorId: str

class CrlDetailResponseTypeDef(TypedDict):
    crl: CrlDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListCrlsResponseTypeDef(TypedDict):
    crls: List[CrlDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SubjectDetailTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    credentials: NotRequired[List[CredentialSummaryTypeDef]]
    enabled: NotRequired[bool]
    instanceProperties: NotRequired[List[InstancePropertyTypeDef]]
    lastSeenAt: NotRequired[datetime]
    subjectArn: NotRequired[str]
    subjectId: NotRequired[str]
    updatedAt: NotRequired[datetime]
    x509Subject: NotRequired[str]

class ListRequestListCrlsPaginateTypeDef(TypedDict):
    pageSize: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRequestListProfilesPaginateTypeDef(TypedDict):
    pageSize: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRequestListSubjectsPaginateTypeDef(TypedDict):
    pageSize: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRequestListTrustAnchorsPaginateTypeDef(TypedDict):
    pageSize: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubjectsResponseTypeDef(TypedDict):
    subjects: List[SubjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ResetNotificationSettingsRequestRequestTypeDef(TypedDict):
    notificationSettingKeys: Sequence[NotificationSettingKeyTypeDef]
    trustAnchorId: str

class SourceTypeDef(TypedDict):
    sourceData: NotRequired[SourceDataTypeDef]
    sourceType: NotRequired[TrustAnchorTypeType]

class ProfileDetailTypeDef(TypedDict):
    acceptRoleSessionName: NotRequired[bool]
    attributeMappings: NotRequired[List[AttributeMappingTypeDef]]
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    durationSeconds: NotRequired[int]
    enabled: NotRequired[bool]
    managedPolicyArns: NotRequired[List[str]]
    name: NotRequired[str]
    profileArn: NotRequired[str]
    profileId: NotRequired[str]
    requireInstanceProperties: NotRequired[bool]
    roleArns: NotRequired[List[str]]
    sessionPolicy: NotRequired[str]
    updatedAt: NotRequired[datetime]

class SubjectDetailResponseTypeDef(TypedDict):
    subject: SubjectDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTrustAnchorRequestRequestTypeDef(TypedDict):
    name: str
    source: SourceTypeDef
    enabled: NotRequired[bool]
    notificationSettings: NotRequired[Sequence[NotificationSettingTypeDef]]
    tags: NotRequired[Sequence[TagTypeDef]]

class TrustAnchorDetailTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    enabled: NotRequired[bool]
    name: NotRequired[str]
    notificationSettings: NotRequired[List[NotificationSettingDetailTypeDef]]
    source: NotRequired[SourceTypeDef]
    trustAnchorArn: NotRequired[str]
    trustAnchorId: NotRequired[str]
    updatedAt: NotRequired[datetime]

class UpdateTrustAnchorRequestRequestTypeDef(TypedDict):
    trustAnchorId: str
    name: NotRequired[str]
    source: NotRequired[SourceTypeDef]

class DeleteAttributeMappingResponseTypeDef(TypedDict):
    profile: ProfileDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListProfilesResponseTypeDef(TypedDict):
    profiles: List[ProfileDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ProfileDetailResponseTypeDef(TypedDict):
    profile: ProfileDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutAttributeMappingResponseTypeDef(TypedDict):
    profile: ProfileDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListTrustAnchorsResponseTypeDef(TypedDict):
    trustAnchors: List[TrustAnchorDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PutNotificationSettingsResponseTypeDef(TypedDict):
    trustAnchor: TrustAnchorDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ResetNotificationSettingsResponseTypeDef(TypedDict):
    trustAnchor: TrustAnchorDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class TrustAnchorDetailResponseTypeDef(TypedDict):
    trustAnchor: TrustAnchorDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
