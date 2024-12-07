"""
Type annotations for transfer service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_transfer/type_defs/)

Usage::

    ```python
    from mypy_boto3_transfer.type_defs import As2ConnectorConfigTypeDef

    data: As2ConnectorConfigTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AgreementStatusTypeType,
    CertificateStatusTypeType,
    CertificateTypeType,
    CertificateUsageTypeType,
    CompressionEnumType,
    CustomStepStatusType,
    DirectoryListingOptimizationType,
    DomainType,
    EncryptionAlgType,
    EndpointTypeType,
    ExecutionErrorTypeType,
    ExecutionStatusType,
    HomeDirectoryTypeType,
    IdentityProviderTypeType,
    MapTypeType,
    MdnResponseType,
    MdnSigningAlgType,
    OverwriteExistingType,
    ProfileTypeType,
    ProtocolType,
    SecurityPolicyProtocolType,
    SecurityPolicyResourceTypeType,
    SetStatOptionType,
    SftpAuthenticationMethodsType,
    SigningAlgType,
    StateType,
    TlsSessionResumptionModeType,
    TransferTableStatusType,
    WorkflowStepTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "As2ConnectorConfigTypeDef",
    "BlobTypeDef",
    "ConnectorFileTransferResultTypeDef",
    "CopyStepDetailsTypeDef",
    "CreateAccessRequestRequestTypeDef",
    "CreateAccessResponseTypeDef",
    "CreateAgreementRequestRequestTypeDef",
    "CreateAgreementResponseTypeDef",
    "CreateConnectorRequestRequestTypeDef",
    "CreateConnectorResponseTypeDef",
    "CreateProfileRequestRequestTypeDef",
    "CreateProfileResponseTypeDef",
    "CreateServerRequestRequestTypeDef",
    "CreateServerResponseTypeDef",
    "CreateUserRequestRequestTypeDef",
    "CreateUserResponseTypeDef",
    "CreateWebAppRequestRequestTypeDef",
    "CreateWebAppResponseTypeDef",
    "CreateWorkflowRequestRequestTypeDef",
    "CreateWorkflowResponseTypeDef",
    "CustomStepDetailsTypeDef",
    "DecryptStepDetailsTypeDef",
    "DeleteAccessRequestRequestTypeDef",
    "DeleteAgreementRequestRequestTypeDef",
    "DeleteCertificateRequestRequestTypeDef",
    "DeleteConnectorRequestRequestTypeDef",
    "DeleteHostKeyRequestRequestTypeDef",
    "DeleteProfileRequestRequestTypeDef",
    "DeleteServerRequestRequestTypeDef",
    "DeleteSshPublicKeyRequestRequestTypeDef",
    "DeleteStepDetailsTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeleteWebAppCustomizationRequestRequestTypeDef",
    "DeleteWebAppRequestRequestTypeDef",
    "DeleteWorkflowRequestRequestTypeDef",
    "DescribeAccessRequestRequestTypeDef",
    "DescribeAccessResponseTypeDef",
    "DescribeAgreementRequestRequestTypeDef",
    "DescribeAgreementResponseTypeDef",
    "DescribeCertificateRequestRequestTypeDef",
    "DescribeCertificateResponseTypeDef",
    "DescribeConnectorRequestRequestTypeDef",
    "DescribeConnectorResponseTypeDef",
    "DescribeExecutionRequestRequestTypeDef",
    "DescribeExecutionResponseTypeDef",
    "DescribeHostKeyRequestRequestTypeDef",
    "DescribeHostKeyResponseTypeDef",
    "DescribeProfileRequestRequestTypeDef",
    "DescribeProfileResponseTypeDef",
    "DescribeSecurityPolicyRequestRequestTypeDef",
    "DescribeSecurityPolicyResponseTypeDef",
    "DescribeServerRequestRequestTypeDef",
    "DescribeServerRequestServerOfflineWaitTypeDef",
    "DescribeServerRequestServerOnlineWaitTypeDef",
    "DescribeServerResponseTypeDef",
    "DescribeUserRequestRequestTypeDef",
    "DescribeUserResponseTypeDef",
    "DescribeWebAppCustomizationRequestRequestTypeDef",
    "DescribeWebAppCustomizationResponseTypeDef",
    "DescribeWebAppRequestRequestTypeDef",
    "DescribeWebAppResponseTypeDef",
    "DescribeWorkflowRequestRequestTypeDef",
    "DescribeWorkflowResponseTypeDef",
    "DescribedAccessTypeDef",
    "DescribedAgreementTypeDef",
    "DescribedCertificateTypeDef",
    "DescribedConnectorTypeDef",
    "DescribedExecutionTypeDef",
    "DescribedHostKeyTypeDef",
    "DescribedIdentityCenterConfigTypeDef",
    "DescribedProfileTypeDef",
    "DescribedSecurityPolicyTypeDef",
    "DescribedServerTypeDef",
    "DescribedUserTypeDef",
    "DescribedWebAppCustomizationTypeDef",
    "DescribedWebAppIdentityProviderDetailsTypeDef",
    "DescribedWebAppTypeDef",
    "DescribedWorkflowTypeDef",
    "EfsFileLocationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointDetailsOutputTypeDef",
    "EndpointDetailsTypeDef",
    "ExecutionErrorTypeDef",
    "ExecutionResultsTypeDef",
    "ExecutionStepResultTypeDef",
    "FileLocationTypeDef",
    "HomeDirectoryMapEntryTypeDef",
    "IdentityCenterConfigTypeDef",
    "IdentityProviderDetailsTypeDef",
    "ImportCertificateRequestRequestTypeDef",
    "ImportCertificateResponseTypeDef",
    "ImportHostKeyRequestRequestTypeDef",
    "ImportHostKeyResponseTypeDef",
    "ImportSshPublicKeyRequestRequestTypeDef",
    "ImportSshPublicKeyResponseTypeDef",
    "InputFileLocationTypeDef",
    "ListAccessesRequestListAccessesPaginateTypeDef",
    "ListAccessesRequestRequestTypeDef",
    "ListAccessesResponseTypeDef",
    "ListAgreementsRequestListAgreementsPaginateTypeDef",
    "ListAgreementsRequestRequestTypeDef",
    "ListAgreementsResponseTypeDef",
    "ListCertificatesRequestListCertificatesPaginateTypeDef",
    "ListCertificatesRequestRequestTypeDef",
    "ListCertificatesResponseTypeDef",
    "ListConnectorsRequestListConnectorsPaginateTypeDef",
    "ListConnectorsRequestRequestTypeDef",
    "ListConnectorsResponseTypeDef",
    "ListExecutionsRequestListExecutionsPaginateTypeDef",
    "ListExecutionsRequestRequestTypeDef",
    "ListExecutionsResponseTypeDef",
    "ListFileTransferResultsRequestListFileTransferResultsPaginateTypeDef",
    "ListFileTransferResultsRequestRequestTypeDef",
    "ListFileTransferResultsResponseTypeDef",
    "ListHostKeysRequestRequestTypeDef",
    "ListHostKeysResponseTypeDef",
    "ListProfilesRequestListProfilesPaginateTypeDef",
    "ListProfilesRequestRequestTypeDef",
    "ListProfilesResponseTypeDef",
    "ListSecurityPoliciesRequestListSecurityPoliciesPaginateTypeDef",
    "ListSecurityPoliciesRequestRequestTypeDef",
    "ListSecurityPoliciesResponseTypeDef",
    "ListServersRequestListServersPaginateTypeDef",
    "ListServersRequestRequestTypeDef",
    "ListServersResponseTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUsersRequestListUsersPaginateTypeDef",
    "ListUsersRequestRequestTypeDef",
    "ListUsersResponseTypeDef",
    "ListWebAppsRequestListWebAppsPaginateTypeDef",
    "ListWebAppsRequestRequestTypeDef",
    "ListWebAppsResponseTypeDef",
    "ListWorkflowsRequestListWorkflowsPaginateTypeDef",
    "ListWorkflowsRequestRequestTypeDef",
    "ListWorkflowsResponseTypeDef",
    "ListedAccessTypeDef",
    "ListedAgreementTypeDef",
    "ListedCertificateTypeDef",
    "ListedConnectorTypeDef",
    "ListedExecutionTypeDef",
    "ListedHostKeyTypeDef",
    "ListedProfileTypeDef",
    "ListedServerTypeDef",
    "ListedUserTypeDef",
    "ListedWebAppTypeDef",
    "ListedWorkflowTypeDef",
    "LoggingConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PosixProfileOutputTypeDef",
    "PosixProfileTypeDef",
    "ProtocolDetailsOutputTypeDef",
    "ProtocolDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "S3FileLocationTypeDef",
    "S3InputFileLocationTypeDef",
    "S3StorageOptionsTypeDef",
    "S3TagTypeDef",
    "SendWorkflowStepStateRequestRequestTypeDef",
    "ServiceMetadataTypeDef",
    "SftpConnectorConfigOutputTypeDef",
    "SftpConnectorConfigTypeDef",
    "SshPublicKeyTypeDef",
    "StartDirectoryListingRequestRequestTypeDef",
    "StartDirectoryListingResponseTypeDef",
    "StartFileTransferRequestRequestTypeDef",
    "StartFileTransferResponseTypeDef",
    "StartServerRequestRequestTypeDef",
    "StopServerRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagStepDetailsOutputTypeDef",
    "TagStepDetailsTypeDef",
    "TagStepDetailsUnionTypeDef",
    "TagTypeDef",
    "TestConnectionRequestRequestTypeDef",
    "TestConnectionResponseTypeDef",
    "TestIdentityProviderRequestRequestTypeDef",
    "TestIdentityProviderResponseTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccessRequestRequestTypeDef",
    "UpdateAccessResponseTypeDef",
    "UpdateAgreementRequestRequestTypeDef",
    "UpdateAgreementResponseTypeDef",
    "UpdateCertificateRequestRequestTypeDef",
    "UpdateCertificateResponseTypeDef",
    "UpdateConnectorRequestRequestTypeDef",
    "UpdateConnectorResponseTypeDef",
    "UpdateHostKeyRequestRequestTypeDef",
    "UpdateHostKeyResponseTypeDef",
    "UpdateProfileRequestRequestTypeDef",
    "UpdateProfileResponseTypeDef",
    "UpdateServerRequestRequestTypeDef",
    "UpdateServerResponseTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UpdateUserResponseTypeDef",
    "UpdateWebAppCustomizationRequestRequestTypeDef",
    "UpdateWebAppCustomizationResponseTypeDef",
    "UpdateWebAppIdentityCenterConfigTypeDef",
    "UpdateWebAppIdentityProviderDetailsTypeDef",
    "UpdateWebAppRequestRequestTypeDef",
    "UpdateWebAppResponseTypeDef",
    "UserDetailsTypeDef",
    "WaiterConfigTypeDef",
    "WebAppIdentityProviderDetailsTypeDef",
    "WebAppUnitsTypeDef",
    "WorkflowDetailTypeDef",
    "WorkflowDetailsOutputTypeDef",
    "WorkflowDetailsTypeDef",
    "WorkflowStepOutputTypeDef",
    "WorkflowStepTypeDef",
    "WorkflowStepUnionTypeDef",
)

class As2ConnectorConfigTypeDef(TypedDict):
    LocalProfileId: NotRequired[str]
    PartnerProfileId: NotRequired[str]
    MessageSubject: NotRequired[str]
    Compression: NotRequired[CompressionEnumType]
    EncryptionAlgorithm: NotRequired[EncryptionAlgType]
    SigningAlgorithm: NotRequired[SigningAlgType]
    MdnSigningAlgorithm: NotRequired[MdnSigningAlgType]
    MdnResponse: NotRequired[MdnResponseType]
    BasicAuthSecretId: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class ConnectorFileTransferResultTypeDef(TypedDict):
    FilePath: str
    StatusCode: TransferTableStatusType
    FailureCode: NotRequired[str]
    FailureMessage: NotRequired[str]

HomeDirectoryMapEntryTypeDef = TypedDict(
    "HomeDirectoryMapEntryTypeDef",
    {
        "Entry": str,
        "Target": str,
        "Type": NotRequired[MapTypeType],
    },
)

class PosixProfileTypeDef(TypedDict):
    Uid: int
    Gid: int
    SecondaryGids: NotRequired[Sequence[int]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class SftpConnectorConfigTypeDef(TypedDict):
    UserSecretId: NotRequired[str]
    TrustedHostKeys: NotRequired[Sequence[str]]

class EndpointDetailsTypeDef(TypedDict):
    AddressAllocationIds: NotRequired[Sequence[str]]
    SubnetIds: NotRequired[Sequence[str]]
    VpcEndpointId: NotRequired[str]
    VpcId: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]

class IdentityProviderDetailsTypeDef(TypedDict):
    Url: NotRequired[str]
    InvocationRole: NotRequired[str]
    DirectoryId: NotRequired[str]
    Function: NotRequired[str]
    SftpAuthenticationMethods: NotRequired[SftpAuthenticationMethodsType]

class ProtocolDetailsTypeDef(TypedDict):
    PassiveIp: NotRequired[str]
    TlsSessionResumptionMode: NotRequired[TlsSessionResumptionModeType]
    SetStatOption: NotRequired[SetStatOptionType]
    As2Transports: NotRequired[Sequence[Literal["HTTP"]]]

class S3StorageOptionsTypeDef(TypedDict):
    DirectoryListingOptimization: NotRequired[DirectoryListingOptimizationType]

class WebAppUnitsTypeDef(TypedDict):
    Provisioned: NotRequired[int]

class CustomStepDetailsTypeDef(TypedDict):
    Name: NotRequired[str]
    Target: NotRequired[str]
    TimeoutSeconds: NotRequired[int]
    SourceFileLocation: NotRequired[str]

class DeleteAccessRequestRequestTypeDef(TypedDict):
    ServerId: str
    ExternalId: str

class DeleteAgreementRequestRequestTypeDef(TypedDict):
    AgreementId: str
    ServerId: str

class DeleteCertificateRequestRequestTypeDef(TypedDict):
    CertificateId: str

class DeleteConnectorRequestRequestTypeDef(TypedDict):
    ConnectorId: str

class DeleteHostKeyRequestRequestTypeDef(TypedDict):
    ServerId: str
    HostKeyId: str

class DeleteProfileRequestRequestTypeDef(TypedDict):
    ProfileId: str

class DeleteServerRequestRequestTypeDef(TypedDict):
    ServerId: str

class DeleteSshPublicKeyRequestRequestTypeDef(TypedDict):
    ServerId: str
    SshPublicKeyId: str
    UserName: str

class DeleteStepDetailsTypeDef(TypedDict):
    Name: NotRequired[str]
    SourceFileLocation: NotRequired[str]

class DeleteUserRequestRequestTypeDef(TypedDict):
    ServerId: str
    UserName: str

class DeleteWebAppCustomizationRequestRequestTypeDef(TypedDict):
    WebAppId: str

class DeleteWebAppRequestRequestTypeDef(TypedDict):
    WebAppId: str

class DeleteWorkflowRequestRequestTypeDef(TypedDict):
    WorkflowId: str

class DescribeAccessRequestRequestTypeDef(TypedDict):
    ServerId: str
    ExternalId: str

class DescribeAgreementRequestRequestTypeDef(TypedDict):
    AgreementId: str
    ServerId: str

class DescribeCertificateRequestRequestTypeDef(TypedDict):
    CertificateId: str

class DescribeConnectorRequestRequestTypeDef(TypedDict):
    ConnectorId: str

class DescribeExecutionRequestRequestTypeDef(TypedDict):
    ExecutionId: str
    WorkflowId: str

class DescribeHostKeyRequestRequestTypeDef(TypedDict):
    ServerId: str
    HostKeyId: str

class DescribeProfileRequestRequestTypeDef(TypedDict):
    ProfileId: str

class DescribeSecurityPolicyRequestRequestTypeDef(TypedDict):
    SecurityPolicyName: str

DescribedSecurityPolicyTypeDef = TypedDict(
    "DescribedSecurityPolicyTypeDef",
    {
        "SecurityPolicyName": str,
        "Fips": NotRequired[bool],
        "SshCiphers": NotRequired[List[str]],
        "SshKexs": NotRequired[List[str]],
        "SshMacs": NotRequired[List[str]],
        "TlsCiphers": NotRequired[List[str]],
        "SshHostKeyAlgorithms": NotRequired[List[str]],
        "Type": NotRequired[SecurityPolicyResourceTypeType],
        "Protocols": NotRequired[List[SecurityPolicyProtocolType]],
    },
)

class DescribeServerRequestRequestTypeDef(TypedDict):
    ServerId: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class DescribeUserRequestRequestTypeDef(TypedDict):
    ServerId: str
    UserName: str

class DescribeWebAppCustomizationRequestRequestTypeDef(TypedDict):
    WebAppId: str

class DescribedWebAppCustomizationTypeDef(TypedDict):
    Arn: str
    WebAppId: str
    Title: NotRequired[str]
    LogoFile: NotRequired[bytes]
    FaviconFile: NotRequired[bytes]

class DescribeWebAppRequestRequestTypeDef(TypedDict):
    WebAppId: str

class DescribeWorkflowRequestRequestTypeDef(TypedDict):
    WorkflowId: str

class PosixProfileOutputTypeDef(TypedDict):
    Uid: int
    Gid: int
    SecondaryGids: NotRequired[List[int]]

class SftpConnectorConfigOutputTypeDef(TypedDict):
    UserSecretId: NotRequired[str]
    TrustedHostKeys: NotRequired[List[str]]

class LoggingConfigurationTypeDef(TypedDict):
    LoggingRole: NotRequired[str]
    LogGroupName: NotRequired[str]

class DescribedIdentityCenterConfigTypeDef(TypedDict):
    ApplicationArn: NotRequired[str]
    InstanceArn: NotRequired[str]
    Role: NotRequired[str]

class EndpointDetailsOutputTypeDef(TypedDict):
    AddressAllocationIds: NotRequired[List[str]]
    SubnetIds: NotRequired[List[str]]
    VpcEndpointId: NotRequired[str]
    VpcId: NotRequired[str]
    SecurityGroupIds: NotRequired[List[str]]

class ProtocolDetailsOutputTypeDef(TypedDict):
    PassiveIp: NotRequired[str]
    TlsSessionResumptionMode: NotRequired[TlsSessionResumptionModeType]
    SetStatOption: NotRequired[SetStatOptionType]
    As2Transports: NotRequired[List[Literal["HTTP"]]]

class SshPublicKeyTypeDef(TypedDict):
    DateImported: datetime
    SshPublicKeyBody: str
    SshPublicKeyId: str

class EfsFileLocationTypeDef(TypedDict):
    FileSystemId: NotRequired[str]
    Path: NotRequired[str]

ExecutionErrorTypeDef = TypedDict(
    "ExecutionErrorTypeDef",
    {
        "Type": ExecutionErrorTypeType,
        "Message": str,
    },
)

class S3FileLocationTypeDef(TypedDict):
    Bucket: NotRequired[str]
    Key: NotRequired[str]
    VersionId: NotRequired[str]
    Etag: NotRequired[str]

class IdentityCenterConfigTypeDef(TypedDict):
    InstanceArn: NotRequired[str]
    Role: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class ImportSshPublicKeyRequestRequestTypeDef(TypedDict):
    ServerId: str
    SshPublicKeyBody: str
    UserName: str

class S3InputFileLocationTypeDef(TypedDict):
    Bucket: NotRequired[str]
    Key: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAccessesRequestRequestTypeDef(TypedDict):
    ServerId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListedAccessTypeDef(TypedDict):
    HomeDirectory: NotRequired[str]
    HomeDirectoryType: NotRequired[HomeDirectoryTypeType]
    Role: NotRequired[str]
    ExternalId: NotRequired[str]

class ListAgreementsRequestRequestTypeDef(TypedDict):
    ServerId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListedAgreementTypeDef(TypedDict):
    Arn: NotRequired[str]
    AgreementId: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[AgreementStatusTypeType]
    ServerId: NotRequired[str]
    LocalProfileId: NotRequired[str]
    PartnerProfileId: NotRequired[str]

class ListCertificatesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

ListedCertificateTypeDef = TypedDict(
    "ListedCertificateTypeDef",
    {
        "Arn": NotRequired[str],
        "CertificateId": NotRequired[str],
        "Usage": NotRequired[CertificateUsageTypeType],
        "Status": NotRequired[CertificateStatusTypeType],
        "ActiveDate": NotRequired[datetime],
        "InactiveDate": NotRequired[datetime],
        "Type": NotRequired[CertificateTypeType],
        "Description": NotRequired[str],
    },
)

class ListConnectorsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListedConnectorTypeDef(TypedDict):
    Arn: NotRequired[str]
    ConnectorId: NotRequired[str]
    Url: NotRequired[str]

class ListExecutionsRequestRequestTypeDef(TypedDict):
    WorkflowId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListFileTransferResultsRequestRequestTypeDef(TypedDict):
    ConnectorId: str
    TransferId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListHostKeysRequestRequestTypeDef(TypedDict):
    ServerId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

ListedHostKeyTypeDef = TypedDict(
    "ListedHostKeyTypeDef",
    {
        "Arn": str,
        "HostKeyId": NotRequired[str],
        "Fingerprint": NotRequired[str],
        "Description": NotRequired[str],
        "Type": NotRequired[str],
        "DateImported": NotRequired[datetime],
    },
)

class ListProfilesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ProfileType: NotRequired[ProfileTypeType]

class ListedProfileTypeDef(TypedDict):
    Arn: NotRequired[str]
    ProfileId: NotRequired[str]
    As2Id: NotRequired[str]
    ProfileType: NotRequired[ProfileTypeType]

class ListSecurityPoliciesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListServersRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListedServerTypeDef(TypedDict):
    Arn: str
    Domain: NotRequired[DomainType]
    IdentityProviderType: NotRequired[IdentityProviderTypeType]
    EndpointType: NotRequired[EndpointTypeType]
    LoggingRole: NotRequired[str]
    ServerId: NotRequired[str]
    State: NotRequired[StateType]
    UserCount: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    Arn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListUsersRequestRequestTypeDef(TypedDict):
    ServerId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListedUserTypeDef(TypedDict):
    Arn: str
    HomeDirectory: NotRequired[str]
    HomeDirectoryType: NotRequired[HomeDirectoryTypeType]
    Role: NotRequired[str]
    SshPublicKeyCount: NotRequired[int]
    UserName: NotRequired[str]

class ListWebAppsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListedWebAppTypeDef(TypedDict):
    Arn: str
    WebAppId: str
    AccessEndpoint: NotRequired[str]
    WebAppEndpoint: NotRequired[str]

class ListWorkflowsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListedWorkflowTypeDef(TypedDict):
    WorkflowId: NotRequired[str]
    Description: NotRequired[str]
    Arn: NotRequired[str]

class S3TagTypeDef(TypedDict):
    Key: str
    Value: str

class SendWorkflowStepStateRequestRequestTypeDef(TypedDict):
    WorkflowId: str
    ExecutionId: str
    Token: str
    Status: CustomStepStatusType

class UserDetailsTypeDef(TypedDict):
    UserName: str
    ServerId: str
    SessionId: NotRequired[str]

class StartDirectoryListingRequestRequestTypeDef(TypedDict):
    ConnectorId: str
    RemoteDirectoryPath: str
    OutputDirectoryPath: str
    MaxItems: NotRequired[int]

class StartFileTransferRequestRequestTypeDef(TypedDict):
    ConnectorId: str
    SendFilePaths: NotRequired[Sequence[str]]
    RetrieveFilePaths: NotRequired[Sequence[str]]
    LocalDirectoryPath: NotRequired[str]
    RemoteDirectoryPath: NotRequired[str]

class StartServerRequestRequestTypeDef(TypedDict):
    ServerId: str

class StopServerRequestRequestTypeDef(TypedDict):
    ServerId: str

class TestConnectionRequestRequestTypeDef(TypedDict):
    ConnectorId: str

class TestIdentityProviderRequestRequestTypeDef(TypedDict):
    ServerId: str
    UserName: str
    ServerProtocol: NotRequired[ProtocolType]
    SourceIp: NotRequired[str]
    UserPassword: NotRequired[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    Arn: str
    TagKeys: Sequence[str]

class UpdateAgreementRequestRequestTypeDef(TypedDict):
    AgreementId: str
    ServerId: str
    Description: NotRequired[str]
    Status: NotRequired[AgreementStatusTypeType]
    LocalProfileId: NotRequired[str]
    PartnerProfileId: NotRequired[str]
    BaseDirectory: NotRequired[str]
    AccessRole: NotRequired[str]

class UpdateHostKeyRequestRequestTypeDef(TypedDict):
    ServerId: str
    HostKeyId: str
    Description: str

class UpdateProfileRequestRequestTypeDef(TypedDict):
    ProfileId: str
    CertificateIds: NotRequired[Sequence[str]]

class UpdateWebAppIdentityCenterConfigTypeDef(TypedDict):
    Role: NotRequired[str]

class WorkflowDetailTypeDef(TypedDict):
    WorkflowId: str
    ExecutionRole: str

class UpdateWebAppCustomizationRequestRequestTypeDef(TypedDict):
    WebAppId: str
    Title: NotRequired[str]
    LogoFile: NotRequired[BlobTypeDef]
    FaviconFile: NotRequired[BlobTypeDef]

class CreateAccessRequestRequestTypeDef(TypedDict):
    Role: str
    ServerId: str
    ExternalId: str
    HomeDirectory: NotRequired[str]
    HomeDirectoryType: NotRequired[HomeDirectoryTypeType]
    HomeDirectoryMappings: NotRequired[Sequence[HomeDirectoryMapEntryTypeDef]]
    Policy: NotRequired[str]
    PosixProfile: NotRequired[PosixProfileTypeDef]

class UpdateAccessRequestRequestTypeDef(TypedDict):
    ServerId: str
    ExternalId: str
    HomeDirectory: NotRequired[str]
    HomeDirectoryType: NotRequired[HomeDirectoryTypeType]
    HomeDirectoryMappings: NotRequired[Sequence[HomeDirectoryMapEntryTypeDef]]
    Policy: NotRequired[str]
    PosixProfile: NotRequired[PosixProfileTypeDef]
    Role: NotRequired[str]

class UpdateUserRequestRequestTypeDef(TypedDict):
    ServerId: str
    UserName: str
    HomeDirectory: NotRequired[str]
    HomeDirectoryType: NotRequired[HomeDirectoryTypeType]
    HomeDirectoryMappings: NotRequired[Sequence[HomeDirectoryMapEntryTypeDef]]
    Policy: NotRequired[str]
    PosixProfile: NotRequired[PosixProfileTypeDef]
    Role: NotRequired[str]

class CreateAccessResponseTypeDef(TypedDict):
    ServerId: str
    ExternalId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAgreementResponseTypeDef(TypedDict):
    AgreementId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateConnectorResponseTypeDef(TypedDict):
    ConnectorId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateProfileResponseTypeDef(TypedDict):
    ProfileId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateServerResponseTypeDef(TypedDict):
    ServerId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateUserResponseTypeDef(TypedDict):
    ServerId: str
    UserName: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateWebAppResponseTypeDef(TypedDict):
    WebAppId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateWorkflowResponseTypeDef(TypedDict):
    WorkflowId: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ImportCertificateResponseTypeDef(TypedDict):
    CertificateId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ImportHostKeyResponseTypeDef(TypedDict):
    ServerId: str
    HostKeyId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ImportSshPublicKeyResponseTypeDef(TypedDict):
    ServerId: str
    SshPublicKeyId: str
    UserName: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListFileTransferResultsResponseTypeDef(TypedDict):
    FileTransferResults: List[ConnectorFileTransferResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSecurityPoliciesResponseTypeDef(TypedDict):
    SecurityPolicyNames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StartDirectoryListingResponseTypeDef(TypedDict):
    ListingId: str
    OutputFileName: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartFileTransferResponseTypeDef(TypedDict):
    TransferId: str
    ResponseMetadata: ResponseMetadataTypeDef

class TestConnectionResponseTypeDef(TypedDict):
    ConnectorId: str
    Status: str
    StatusMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class TestIdentityProviderResponseTypeDef(TypedDict):
    Response: str
    StatusCode: int
    Message: str
    Url: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAccessResponseTypeDef(TypedDict):
    ServerId: str
    ExternalId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAgreementResponseTypeDef(TypedDict):
    AgreementId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCertificateResponseTypeDef(TypedDict):
    CertificateId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConnectorResponseTypeDef(TypedDict):
    ConnectorId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateHostKeyResponseTypeDef(TypedDict):
    ServerId: str
    HostKeyId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProfileResponseTypeDef(TypedDict):
    ProfileId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateServerResponseTypeDef(TypedDict):
    ServerId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateUserResponseTypeDef(TypedDict):
    ServerId: str
    UserName: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateWebAppCustomizationResponseTypeDef(TypedDict):
    WebAppId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateWebAppResponseTypeDef(TypedDict):
    WebAppId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAgreementRequestRequestTypeDef(TypedDict):
    ServerId: str
    LocalProfileId: str
    PartnerProfileId: str
    BaseDirectory: str
    AccessRole: str
    Description: NotRequired[str]
    Status: NotRequired[AgreementStatusTypeType]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateProfileRequestRequestTypeDef(TypedDict):
    As2Id: str
    ProfileType: ProfileTypeType
    CertificateIds: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateUserRequestRequestTypeDef(TypedDict):
    Role: str
    ServerId: str
    UserName: str
    HomeDirectory: NotRequired[str]
    HomeDirectoryType: NotRequired[HomeDirectoryTypeType]
    HomeDirectoryMappings: NotRequired[Sequence[HomeDirectoryMapEntryTypeDef]]
    Policy: NotRequired[str]
    PosixProfile: NotRequired[PosixProfileTypeDef]
    SshPublicKeyBody: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class DescribedAgreementTypeDef(TypedDict):
    Arn: str
    AgreementId: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[AgreementStatusTypeType]
    ServerId: NotRequired[str]
    LocalProfileId: NotRequired[str]
    PartnerProfileId: NotRequired[str]
    BaseDirectory: NotRequired[str]
    AccessRole: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]

DescribedCertificateTypeDef = TypedDict(
    "DescribedCertificateTypeDef",
    {
        "Arn": str,
        "CertificateId": NotRequired[str],
        "Usage": NotRequired[CertificateUsageTypeType],
        "Status": NotRequired[CertificateStatusTypeType],
        "Certificate": NotRequired[str],
        "CertificateChain": NotRequired[str],
        "ActiveDate": NotRequired[datetime],
        "InactiveDate": NotRequired[datetime],
        "Serial": NotRequired[str],
        "NotBeforeDate": NotRequired[datetime],
        "NotAfterDate": NotRequired[datetime],
        "Type": NotRequired[CertificateTypeType],
        "Description": NotRequired[str],
        "Tags": NotRequired[List[TagTypeDef]],
    },
)
DescribedHostKeyTypeDef = TypedDict(
    "DescribedHostKeyTypeDef",
    {
        "Arn": str,
        "HostKeyId": NotRequired[str],
        "HostKeyFingerprint": NotRequired[str],
        "Description": NotRequired[str],
        "Type": NotRequired[str],
        "DateImported": NotRequired[datetime],
        "Tags": NotRequired[List[TagTypeDef]],
    },
)

class DescribedProfileTypeDef(TypedDict):
    Arn: str
    ProfileId: NotRequired[str]
    ProfileType: NotRequired[ProfileTypeType]
    As2Id: NotRequired[str]
    CertificateIds: NotRequired[List[str]]
    Tags: NotRequired[List[TagTypeDef]]

class ImportHostKeyRequestRequestTypeDef(TypedDict):
    ServerId: str
    HostKeyBody: str
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Arn: str
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    Arn: str
    Tags: Sequence[TagTypeDef]

class CreateConnectorRequestRequestTypeDef(TypedDict):
    Url: str
    AccessRole: str
    As2Config: NotRequired[As2ConnectorConfigTypeDef]
    LoggingRole: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    SftpConfig: NotRequired[SftpConnectorConfigTypeDef]
    SecurityPolicyName: NotRequired[str]

class UpdateConnectorRequestRequestTypeDef(TypedDict):
    ConnectorId: str
    Url: NotRequired[str]
    As2Config: NotRequired[As2ConnectorConfigTypeDef]
    AccessRole: NotRequired[str]
    LoggingRole: NotRequired[str]
    SftpConfig: NotRequired[SftpConnectorConfigTypeDef]
    SecurityPolicyName: NotRequired[str]

class DescribeSecurityPolicyResponseTypeDef(TypedDict):
    SecurityPolicy: DescribedSecurityPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeServerRequestServerOfflineWaitTypeDef(TypedDict):
    ServerId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeServerRequestServerOnlineWaitTypeDef(TypedDict):
    ServerId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeWebAppCustomizationResponseTypeDef(TypedDict):
    WebAppCustomization: DescribedWebAppCustomizationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribedAccessTypeDef(TypedDict):
    HomeDirectory: NotRequired[str]
    HomeDirectoryMappings: NotRequired[List[HomeDirectoryMapEntryTypeDef]]
    HomeDirectoryType: NotRequired[HomeDirectoryTypeType]
    Policy: NotRequired[str]
    PosixProfile: NotRequired[PosixProfileOutputTypeDef]
    Role: NotRequired[str]
    ExternalId: NotRequired[str]

class DescribedConnectorTypeDef(TypedDict):
    Arn: str
    ConnectorId: NotRequired[str]
    Url: NotRequired[str]
    As2Config: NotRequired[As2ConnectorConfigTypeDef]
    AccessRole: NotRequired[str]
    LoggingRole: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]
    SftpConfig: NotRequired[SftpConnectorConfigOutputTypeDef]
    ServiceManagedEgressIpAddresses: NotRequired[List[str]]
    SecurityPolicyName: NotRequired[str]

class DescribedWebAppIdentityProviderDetailsTypeDef(TypedDict):
    IdentityCenterConfig: NotRequired[DescribedIdentityCenterConfigTypeDef]

class DescribedUserTypeDef(TypedDict):
    Arn: str
    HomeDirectory: NotRequired[str]
    HomeDirectoryMappings: NotRequired[List[HomeDirectoryMapEntryTypeDef]]
    HomeDirectoryType: NotRequired[HomeDirectoryTypeType]
    Policy: NotRequired[str]
    PosixProfile: NotRequired[PosixProfileOutputTypeDef]
    Role: NotRequired[str]
    SshPublicKeys: NotRequired[List[SshPublicKeyTypeDef]]
    Tags: NotRequired[List[TagTypeDef]]
    UserName: NotRequired[str]

class ExecutionStepResultTypeDef(TypedDict):
    StepType: NotRequired[WorkflowStepTypeType]
    Outputs: NotRequired[str]
    Error: NotRequired[ExecutionErrorTypeDef]

class FileLocationTypeDef(TypedDict):
    S3FileLocation: NotRequired[S3FileLocationTypeDef]
    EfsFileLocation: NotRequired[EfsFileLocationTypeDef]

class WebAppIdentityProviderDetailsTypeDef(TypedDict):
    IdentityCenterConfig: NotRequired[IdentityCenterConfigTypeDef]

class ImportCertificateRequestRequestTypeDef(TypedDict):
    Usage: CertificateUsageTypeType
    Certificate: str
    CertificateChain: NotRequired[str]
    PrivateKey: NotRequired[str]
    ActiveDate: NotRequired[TimestampTypeDef]
    InactiveDate: NotRequired[TimestampTypeDef]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class UpdateCertificateRequestRequestTypeDef(TypedDict):
    CertificateId: str
    ActiveDate: NotRequired[TimestampTypeDef]
    InactiveDate: NotRequired[TimestampTypeDef]
    Description: NotRequired[str]

class InputFileLocationTypeDef(TypedDict):
    S3FileLocation: NotRequired[S3InputFileLocationTypeDef]
    EfsFileLocation: NotRequired[EfsFileLocationTypeDef]

class ListAccessesRequestListAccessesPaginateTypeDef(TypedDict):
    ServerId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAgreementsRequestListAgreementsPaginateTypeDef(TypedDict):
    ServerId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCertificatesRequestListCertificatesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConnectorsRequestListConnectorsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListExecutionsRequestListExecutionsPaginateTypeDef(TypedDict):
    WorkflowId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFileTransferResultsRequestListFileTransferResultsPaginateTypeDef(TypedDict):
    ConnectorId: str
    TransferId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProfilesRequestListProfilesPaginateTypeDef(TypedDict):
    ProfileType: NotRequired[ProfileTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSecurityPoliciesRequestListSecurityPoliciesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServersRequestListServersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(TypedDict):
    Arn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListUsersRequestListUsersPaginateTypeDef(TypedDict):
    ServerId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWebAppsRequestListWebAppsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorkflowsRequestListWorkflowsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAccessesResponseTypeDef(TypedDict):
    ServerId: str
    Accesses: List[ListedAccessTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAgreementsResponseTypeDef(TypedDict):
    Agreements: List[ListedAgreementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCertificatesResponseTypeDef(TypedDict):
    Certificates: List[ListedCertificateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListConnectorsResponseTypeDef(TypedDict):
    Connectors: List[ListedConnectorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListHostKeysResponseTypeDef(TypedDict):
    ServerId: str
    HostKeys: List[ListedHostKeyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListProfilesResponseTypeDef(TypedDict):
    Profiles: List[ListedProfileTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListServersResponseTypeDef(TypedDict):
    Servers: List[ListedServerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListUsersResponseTypeDef(TypedDict):
    ServerId: str
    Users: List[ListedUserTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListWebAppsResponseTypeDef(TypedDict):
    WebApps: List[ListedWebAppTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListWorkflowsResponseTypeDef(TypedDict):
    Workflows: List[ListedWorkflowTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TagStepDetailsOutputTypeDef(TypedDict):
    Name: NotRequired[str]
    Tags: NotRequired[List[S3TagTypeDef]]
    SourceFileLocation: NotRequired[str]

class TagStepDetailsTypeDef(TypedDict):
    Name: NotRequired[str]
    Tags: NotRequired[Sequence[S3TagTypeDef]]
    SourceFileLocation: NotRequired[str]

class ServiceMetadataTypeDef(TypedDict):
    UserDetails: UserDetailsTypeDef

class UpdateWebAppIdentityProviderDetailsTypeDef(TypedDict):
    IdentityCenterConfig: NotRequired[UpdateWebAppIdentityCenterConfigTypeDef]

class WorkflowDetailsOutputTypeDef(TypedDict):
    OnUpload: NotRequired[List[WorkflowDetailTypeDef]]
    OnPartialUpload: NotRequired[List[WorkflowDetailTypeDef]]

class WorkflowDetailsTypeDef(TypedDict):
    OnUpload: NotRequired[Sequence[WorkflowDetailTypeDef]]
    OnPartialUpload: NotRequired[Sequence[WorkflowDetailTypeDef]]

class DescribeAgreementResponseTypeDef(TypedDict):
    Agreement: DescribedAgreementTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCertificateResponseTypeDef(TypedDict):
    Certificate: DescribedCertificateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeHostKeyResponseTypeDef(TypedDict):
    HostKey: DescribedHostKeyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeProfileResponseTypeDef(TypedDict):
    Profile: DescribedProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAccessResponseTypeDef(TypedDict):
    ServerId: str
    Access: DescribedAccessTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeConnectorResponseTypeDef(TypedDict):
    Connector: DescribedConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribedWebAppTypeDef(TypedDict):
    Arn: str
    WebAppId: str
    DescribedIdentityProviderDetails: NotRequired[DescribedWebAppIdentityProviderDetailsTypeDef]
    AccessEndpoint: NotRequired[str]
    WebAppEndpoint: NotRequired[str]
    WebAppUnits: NotRequired[WebAppUnitsTypeDef]
    Tags: NotRequired[List[TagTypeDef]]

class DescribeUserResponseTypeDef(TypedDict):
    ServerId: str
    User: DescribedUserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExecutionResultsTypeDef(TypedDict):
    Steps: NotRequired[List[ExecutionStepResultTypeDef]]
    OnExceptionSteps: NotRequired[List[ExecutionStepResultTypeDef]]

class CreateWebAppRequestRequestTypeDef(TypedDict):
    IdentityProviderDetails: WebAppIdentityProviderDetailsTypeDef
    AccessEndpoint: NotRequired[str]
    WebAppUnits: NotRequired[WebAppUnitsTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CopyStepDetailsTypeDef(TypedDict):
    Name: NotRequired[str]
    DestinationFileLocation: NotRequired[InputFileLocationTypeDef]
    OverwriteExisting: NotRequired[OverwriteExistingType]
    SourceFileLocation: NotRequired[str]

DecryptStepDetailsTypeDef = TypedDict(
    "DecryptStepDetailsTypeDef",
    {
        "Type": Literal["PGP"],
        "DestinationFileLocation": InputFileLocationTypeDef,
        "Name": NotRequired[str],
        "SourceFileLocation": NotRequired[str],
        "OverwriteExisting": NotRequired[OverwriteExistingType],
    },
)
TagStepDetailsUnionTypeDef = Union[TagStepDetailsTypeDef, TagStepDetailsOutputTypeDef]

class ListedExecutionTypeDef(TypedDict):
    ExecutionId: NotRequired[str]
    InitialFileLocation: NotRequired[FileLocationTypeDef]
    ServiceMetadata: NotRequired[ServiceMetadataTypeDef]
    Status: NotRequired[ExecutionStatusType]

class UpdateWebAppRequestRequestTypeDef(TypedDict):
    WebAppId: str
    IdentityProviderDetails: NotRequired[UpdateWebAppIdentityProviderDetailsTypeDef]
    AccessEndpoint: NotRequired[str]
    WebAppUnits: NotRequired[WebAppUnitsTypeDef]

class DescribedServerTypeDef(TypedDict):
    Arn: str
    Certificate: NotRequired[str]
    ProtocolDetails: NotRequired[ProtocolDetailsOutputTypeDef]
    Domain: NotRequired[DomainType]
    EndpointDetails: NotRequired[EndpointDetailsOutputTypeDef]
    EndpointType: NotRequired[EndpointTypeType]
    HostKeyFingerprint: NotRequired[str]
    IdentityProviderDetails: NotRequired[IdentityProviderDetailsTypeDef]
    IdentityProviderType: NotRequired[IdentityProviderTypeType]
    LoggingRole: NotRequired[str]
    PostAuthenticationLoginBanner: NotRequired[str]
    PreAuthenticationLoginBanner: NotRequired[str]
    Protocols: NotRequired[List[ProtocolType]]
    SecurityPolicyName: NotRequired[str]
    ServerId: NotRequired[str]
    State: NotRequired[StateType]
    Tags: NotRequired[List[TagTypeDef]]
    UserCount: NotRequired[int]
    WorkflowDetails: NotRequired[WorkflowDetailsOutputTypeDef]
    StructuredLogDestinations: NotRequired[List[str]]
    S3StorageOptions: NotRequired[S3StorageOptionsTypeDef]
    As2ServiceManagedEgressIpAddresses: NotRequired[List[str]]

class CreateServerRequestRequestTypeDef(TypedDict):
    Certificate: NotRequired[str]
    Domain: NotRequired[DomainType]
    EndpointDetails: NotRequired[EndpointDetailsTypeDef]
    EndpointType: NotRequired[EndpointTypeType]
    HostKey: NotRequired[str]
    IdentityProviderDetails: NotRequired[IdentityProviderDetailsTypeDef]
    IdentityProviderType: NotRequired[IdentityProviderTypeType]
    LoggingRole: NotRequired[str]
    PostAuthenticationLoginBanner: NotRequired[str]
    PreAuthenticationLoginBanner: NotRequired[str]
    Protocols: NotRequired[Sequence[ProtocolType]]
    ProtocolDetails: NotRequired[ProtocolDetailsTypeDef]
    SecurityPolicyName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    WorkflowDetails: NotRequired[WorkflowDetailsTypeDef]
    StructuredLogDestinations: NotRequired[Sequence[str]]
    S3StorageOptions: NotRequired[S3StorageOptionsTypeDef]

class UpdateServerRequestRequestTypeDef(TypedDict):
    ServerId: str
    Certificate: NotRequired[str]
    ProtocolDetails: NotRequired[ProtocolDetailsTypeDef]
    EndpointDetails: NotRequired[EndpointDetailsTypeDef]
    EndpointType: NotRequired[EndpointTypeType]
    HostKey: NotRequired[str]
    IdentityProviderDetails: NotRequired[IdentityProviderDetailsTypeDef]
    LoggingRole: NotRequired[str]
    PostAuthenticationLoginBanner: NotRequired[str]
    PreAuthenticationLoginBanner: NotRequired[str]
    Protocols: NotRequired[Sequence[ProtocolType]]
    SecurityPolicyName: NotRequired[str]
    WorkflowDetails: NotRequired[WorkflowDetailsTypeDef]
    StructuredLogDestinations: NotRequired[Sequence[str]]
    S3StorageOptions: NotRequired[S3StorageOptionsTypeDef]

class DescribeWebAppResponseTypeDef(TypedDict):
    WebApp: DescribedWebAppTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribedExecutionTypeDef(TypedDict):
    ExecutionId: NotRequired[str]
    InitialFileLocation: NotRequired[FileLocationTypeDef]
    ServiceMetadata: NotRequired[ServiceMetadataTypeDef]
    ExecutionRole: NotRequired[str]
    LoggingConfiguration: NotRequired[LoggingConfigurationTypeDef]
    PosixProfile: NotRequired[PosixProfileOutputTypeDef]
    Status: NotRequired[ExecutionStatusType]
    Results: NotRequired[ExecutionResultsTypeDef]

WorkflowStepOutputTypeDef = TypedDict(
    "WorkflowStepOutputTypeDef",
    {
        "Type": NotRequired[WorkflowStepTypeType],
        "CopyStepDetails": NotRequired[CopyStepDetailsTypeDef],
        "CustomStepDetails": NotRequired[CustomStepDetailsTypeDef],
        "DeleteStepDetails": NotRequired[DeleteStepDetailsTypeDef],
        "TagStepDetails": NotRequired[TagStepDetailsOutputTypeDef],
        "DecryptStepDetails": NotRequired[DecryptStepDetailsTypeDef],
    },
)
WorkflowStepTypeDef = TypedDict(
    "WorkflowStepTypeDef",
    {
        "Type": NotRequired[WorkflowStepTypeType],
        "CopyStepDetails": NotRequired[CopyStepDetailsTypeDef],
        "CustomStepDetails": NotRequired[CustomStepDetailsTypeDef],
        "DeleteStepDetails": NotRequired[DeleteStepDetailsTypeDef],
        "TagStepDetails": NotRequired[TagStepDetailsUnionTypeDef],
        "DecryptStepDetails": NotRequired[DecryptStepDetailsTypeDef],
    },
)

class ListExecutionsResponseTypeDef(TypedDict):
    WorkflowId: str
    Executions: List[ListedExecutionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeServerResponseTypeDef(TypedDict):
    Server: DescribedServerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeExecutionResponseTypeDef(TypedDict):
    WorkflowId: str
    Execution: DescribedExecutionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribedWorkflowTypeDef(TypedDict):
    Arn: str
    Description: NotRequired[str]
    Steps: NotRequired[List[WorkflowStepOutputTypeDef]]
    OnExceptionSteps: NotRequired[List[WorkflowStepOutputTypeDef]]
    WorkflowId: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]

WorkflowStepUnionTypeDef = Union[WorkflowStepTypeDef, WorkflowStepOutputTypeDef]

class DescribeWorkflowResponseTypeDef(TypedDict):
    Workflow: DescribedWorkflowTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateWorkflowRequestRequestTypeDef(TypedDict):
    Steps: Sequence[WorkflowStepUnionTypeDef]
    Description: NotRequired[str]
    OnExceptionSteps: NotRequired[Sequence[WorkflowStepTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]
