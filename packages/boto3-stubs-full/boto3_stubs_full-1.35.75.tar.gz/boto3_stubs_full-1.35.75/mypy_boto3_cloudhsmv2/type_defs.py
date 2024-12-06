"""
Type annotations for cloudhsmv2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudhsmv2.type_defs import BackupRetentionPolicyTypeDef

    data: BackupRetentionPolicyTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import BackupStateType, ClusterModeType, ClusterStateType, HsmStateType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "BackupRetentionPolicyTypeDef",
    "BackupTypeDef",
    "CertificatesTypeDef",
    "ClusterTypeDef",
    "CopyBackupToRegionRequestRequestTypeDef",
    "CopyBackupToRegionResponseTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateHsmRequestRequestTypeDef",
    "CreateHsmResponseTypeDef",
    "DeleteBackupRequestRequestTypeDef",
    "DeleteBackupResponseTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeleteHsmRequestRequestTypeDef",
    "DeleteHsmResponseTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteResourcePolicyResponseTypeDef",
    "DescribeBackupsRequestDescribeBackupsPaginateTypeDef",
    "DescribeBackupsRequestRequestTypeDef",
    "DescribeBackupsResponseTypeDef",
    "DescribeClustersRequestDescribeClustersPaginateTypeDef",
    "DescribeClustersRequestRequestTypeDef",
    "DescribeClustersResponseTypeDef",
    "DestinationBackupTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "HsmTypeDef",
    "InitializeClusterRequestRequestTypeDef",
    "InitializeClusterResponseTypeDef",
    "ListTagsRequestListTagsPaginateTypeDef",
    "ListTagsRequestRequestTypeDef",
    "ListTagsResponseTypeDef",
    "ModifyBackupAttributesRequestRequestTypeDef",
    "ModifyBackupAttributesResponseTypeDef",
    "ModifyClusterRequestRequestTypeDef",
    "ModifyClusterResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreBackupRequestRequestTypeDef",
    "RestoreBackupResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
)

BackupRetentionPolicyTypeDef = TypedDict(
    "BackupRetentionPolicyTypeDef",
    {
        "Type": NotRequired[Literal["DAYS"]],
        "Value": NotRequired[str],
    },
)


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class CertificatesTypeDef(TypedDict):
    ClusterCsr: NotRequired[str]
    HsmCertificate: NotRequired[str]
    AwsHardwareCertificate: NotRequired[str]
    ManufacturerHardwareCertificate: NotRequired[str]
    ClusterCertificate: NotRequired[str]


class HsmTypeDef(TypedDict):
    HsmId: str
    AvailabilityZone: NotRequired[str]
    ClusterId: NotRequired[str]
    SubnetId: NotRequired[str]
    EniId: NotRequired[str]
    EniIp: NotRequired[str]
    State: NotRequired[HsmStateType]
    StateMessage: NotRequired[str]


class DestinationBackupTypeDef(TypedDict):
    CreateTimestamp: NotRequired[datetime]
    SourceRegion: NotRequired[str]
    SourceBackup: NotRequired[str]
    SourceCluster: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateHsmRequestRequestTypeDef(TypedDict):
    ClusterId: str
    AvailabilityZone: str
    IpAddress: NotRequired[str]


class DeleteBackupRequestRequestTypeDef(TypedDict):
    BackupId: str


class DeleteClusterRequestRequestTypeDef(TypedDict):
    ClusterId: str


class DeleteHsmRequestRequestTypeDef(TypedDict):
    ClusterId: str
    HsmId: NotRequired[str]
    EniId: NotRequired[str]
    EniIp: NotRequired[str]


class DeleteResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeBackupsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Mapping[str, Sequence[str]]]
    Shared: NotRequired[bool]
    SortAscending: NotRequired[bool]


class DescribeClustersRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Mapping[str, Sequence[str]]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class GetResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: NotRequired[str]


class InitializeClusterRequestRequestTypeDef(TypedDict):
    ClusterId: str
    SignedCert: str
    TrustAnchor: str


class ListTagsRequestRequestTypeDef(TypedDict):
    ResourceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ModifyBackupAttributesRequestRequestTypeDef(TypedDict):
    BackupId: str
    NeverExpires: bool


class PutResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: NotRequired[str]
    Policy: NotRequired[str]


class RestoreBackupRequestRequestTypeDef(TypedDict):
    BackupId: str


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceId: str
    TagKeyList: Sequence[str]


class ModifyClusterRequestRequestTypeDef(TypedDict):
    BackupRetentionPolicy: BackupRetentionPolicyTypeDef
    ClusterId: str


class BackupTypeDef(TypedDict):
    BackupId: str
    BackupArn: NotRequired[str]
    BackupState: NotRequired[BackupStateType]
    ClusterId: NotRequired[str]
    CreateTimestamp: NotRequired[datetime]
    CopyTimestamp: NotRequired[datetime]
    NeverExpires: NotRequired[bool]
    SourceRegion: NotRequired[str]
    SourceBackup: NotRequired[str]
    SourceCluster: NotRequired[str]
    DeleteTimestamp: NotRequired[datetime]
    TagList: NotRequired[List[TagTypeDef]]
    HsmType: NotRequired[str]
    Mode: NotRequired[ClusterModeType]


class CopyBackupToRegionRequestRequestTypeDef(TypedDict):
    DestinationRegion: str
    BackupId: str
    TagList: NotRequired[Sequence[TagTypeDef]]


class CreateClusterRequestRequestTypeDef(TypedDict):
    HsmType: str
    SubnetIds: Sequence[str]
    BackupRetentionPolicy: NotRequired[BackupRetentionPolicyTypeDef]
    SourceBackupId: NotRequired[str]
    TagList: NotRequired[Sequence[TagTypeDef]]
    Mode: NotRequired[ClusterModeType]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceId: str
    TagList: Sequence[TagTypeDef]


class ClusterTypeDef(TypedDict):
    BackupPolicy: NotRequired[Literal["DEFAULT"]]
    BackupRetentionPolicy: NotRequired[BackupRetentionPolicyTypeDef]
    ClusterId: NotRequired[str]
    CreateTimestamp: NotRequired[datetime]
    Hsms: NotRequired[List[HsmTypeDef]]
    HsmType: NotRequired[str]
    PreCoPassword: NotRequired[str]
    SecurityGroup: NotRequired[str]
    SourceBackupId: NotRequired[str]
    State: NotRequired[ClusterStateType]
    StateMessage: NotRequired[str]
    SubnetMapping: NotRequired[Dict[str, str]]
    VpcId: NotRequired[str]
    Certificates: NotRequired[CertificatesTypeDef]
    TagList: NotRequired[List[TagTypeDef]]
    Mode: NotRequired[ClusterModeType]


class CopyBackupToRegionResponseTypeDef(TypedDict):
    DestinationBackup: DestinationBackupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHsmResponseTypeDef(TypedDict):
    Hsm: HsmTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteHsmResponseTypeDef(TypedDict):
    HsmId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteResourcePolicyResponseTypeDef(TypedDict):
    ResourceArn: str
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetResourcePolicyResponseTypeDef(TypedDict):
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class InitializeClusterResponseTypeDef(TypedDict):
    State: ClusterStateType
    StateMessage: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsResponseTypeDef(TypedDict):
    TagList: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PutResourcePolicyResponseTypeDef(TypedDict):
    ResourceArn: str
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBackupsRequestDescribeBackupsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Mapping[str, Sequence[str]]]
    Shared: NotRequired[bool]
    SortAscending: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeClustersRequestDescribeClustersPaginateTypeDef(TypedDict):
    Filters: NotRequired[Mapping[str, Sequence[str]]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsRequestListTagsPaginateTypeDef(TypedDict):
    ResourceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DeleteBackupResponseTypeDef(TypedDict):
    Backup: BackupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBackupsResponseTypeDef(TypedDict):
    Backups: List[BackupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyBackupAttributesResponseTypeDef(TypedDict):
    Backup: BackupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreBackupResponseTypeDef(TypedDict):
    Backup: BackupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateClusterResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteClusterResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeClustersResponseTypeDef(TypedDict):
    Clusters: List[ClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyClusterResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
