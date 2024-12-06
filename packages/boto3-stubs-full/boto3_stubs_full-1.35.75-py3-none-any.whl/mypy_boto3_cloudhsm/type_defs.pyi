"""
Type annotations for cloudhsm service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudhsm/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudhsm.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Sequence

from .literals import ClientVersionType, CloudHsmObjectStateType, HsmStatusType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AddTagsToResourceRequestRequestTypeDef",
    "AddTagsToResourceResponseTypeDef",
    "CreateHapgRequestRequestTypeDef",
    "CreateHapgResponseTypeDef",
    "CreateHsmRequestRequestTypeDef",
    "CreateHsmResponseTypeDef",
    "CreateLunaClientRequestRequestTypeDef",
    "CreateLunaClientResponseTypeDef",
    "DeleteHapgRequestRequestTypeDef",
    "DeleteHapgResponseTypeDef",
    "DeleteHsmRequestRequestTypeDef",
    "DeleteHsmResponseTypeDef",
    "DeleteLunaClientRequestRequestTypeDef",
    "DeleteLunaClientResponseTypeDef",
    "DescribeHapgRequestRequestTypeDef",
    "DescribeHapgResponseTypeDef",
    "DescribeHsmRequestRequestTypeDef",
    "DescribeHsmResponseTypeDef",
    "DescribeLunaClientRequestRequestTypeDef",
    "DescribeLunaClientResponseTypeDef",
    "GetConfigRequestRequestTypeDef",
    "GetConfigResponseTypeDef",
    "ListAvailableZonesResponseTypeDef",
    "ListHapgsRequestListHapgsPaginateTypeDef",
    "ListHapgsRequestRequestTypeDef",
    "ListHapgsResponseTypeDef",
    "ListHsmsRequestListHsmsPaginateTypeDef",
    "ListHsmsRequestRequestTypeDef",
    "ListHsmsResponseTypeDef",
    "ListLunaClientsRequestListLunaClientsPaginateTypeDef",
    "ListLunaClientsRequestRequestTypeDef",
    "ListLunaClientsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ModifyHapgRequestRequestTypeDef",
    "ModifyHapgResponseTypeDef",
    "ModifyHsmRequestRequestTypeDef",
    "ModifyHsmResponseTypeDef",
    "ModifyLunaClientRequestRequestTypeDef",
    "ModifyLunaClientResponseTypeDef",
    "PaginatorConfigTypeDef",
    "RemoveTagsFromResourceRequestRequestTypeDef",
    "RemoveTagsFromResourceResponseTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
)

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateHapgRequestRequestTypeDef(TypedDict):
    Label: str

class CreateHsmRequestRequestTypeDef(TypedDict):
    SubnetId: str
    SshKey: str
    IamRoleArn: str
    SubscriptionType: Literal["PRODUCTION"]
    EniIp: NotRequired[str]
    ExternalId: NotRequired[str]
    ClientToken: NotRequired[str]
    SyslogIp: NotRequired[str]

class CreateLunaClientRequestRequestTypeDef(TypedDict):
    Certificate: str
    Label: NotRequired[str]

class DeleteHapgRequestRequestTypeDef(TypedDict):
    HapgArn: str

class DeleteHsmRequestRequestTypeDef(TypedDict):
    HsmArn: str

class DeleteLunaClientRequestRequestTypeDef(TypedDict):
    ClientArn: str

class DescribeHapgRequestRequestTypeDef(TypedDict):
    HapgArn: str

class DescribeHsmRequestRequestTypeDef(TypedDict):
    HsmArn: NotRequired[str]
    HsmSerialNumber: NotRequired[str]

class DescribeLunaClientRequestRequestTypeDef(TypedDict):
    ClientArn: NotRequired[str]
    CertificateFingerprint: NotRequired[str]

class GetConfigRequestRequestTypeDef(TypedDict):
    ClientArn: str
    ClientVersion: ClientVersionType
    HapgList: Sequence[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListHapgsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]

class ListHsmsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]

class ListLunaClientsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class ModifyHapgRequestRequestTypeDef(TypedDict):
    HapgArn: str
    Label: NotRequired[str]
    PartitionSerialList: NotRequired[Sequence[str]]

class ModifyHsmRequestRequestTypeDef(TypedDict):
    HsmArn: str
    SubnetId: NotRequired[str]
    EniIp: NotRequired[str]
    IamRoleArn: NotRequired[str]
    ExternalId: NotRequired[str]
    SyslogIp: NotRequired[str]

class ModifyLunaClientRequestRequestTypeDef(TypedDict):
    ClientArn: str
    Certificate: str

class RemoveTagsFromResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeyList: Sequence[str]

class AddTagsToResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagList: Sequence[TagTypeDef]

class AddTagsToResourceResponseTypeDef(TypedDict):
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateHapgResponseTypeDef(TypedDict):
    HapgArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateHsmResponseTypeDef(TypedDict):
    HsmArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLunaClientResponseTypeDef(TypedDict):
    ClientArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteHapgResponseTypeDef(TypedDict):
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteHsmResponseTypeDef(TypedDict):
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteLunaClientResponseTypeDef(TypedDict):
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeHapgResponseTypeDef(TypedDict):
    HapgArn: str
    HapgSerial: str
    HsmsLastActionFailed: List[str]
    HsmsPendingDeletion: List[str]
    HsmsPendingRegistration: List[str]
    Label: str
    LastModifiedTimestamp: str
    PartitionSerialList: List[str]
    State: CloudHsmObjectStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeHsmResponseTypeDef(TypedDict):
    HsmArn: str
    Status: HsmStatusType
    StatusDetails: str
    AvailabilityZone: str
    EniId: str
    EniIp: str
    SubscriptionType: Literal["PRODUCTION"]
    SubscriptionStartDate: str
    SubscriptionEndDate: str
    VpcId: str
    SubnetId: str
    IamRoleArn: str
    SerialNumber: str
    VendorName: str
    HsmType: str
    SoftwareVersion: str
    SshPublicKey: str
    SshKeyLastUpdated: str
    ServerCertUri: str
    ServerCertLastUpdated: str
    Partitions: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeLunaClientResponseTypeDef(TypedDict):
    ClientArn: str
    Certificate: str
    CertificateFingerprint: str
    LastModifiedTimestamp: str
    Label: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetConfigResponseTypeDef(TypedDict):
    ConfigType: str
    ConfigFile: str
    ConfigCred: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAvailableZonesResponseTypeDef(TypedDict):
    AZList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListHapgsResponseTypeDef(TypedDict):
    HapgList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListHsmsResponseTypeDef(TypedDict):
    HsmList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListLunaClientsResponseTypeDef(TypedDict):
    ClientList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    TagList: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ModifyHapgResponseTypeDef(TypedDict):
    HapgArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ModifyHsmResponseTypeDef(TypedDict):
    HsmArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ModifyLunaClientResponseTypeDef(TypedDict):
    ClientArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class RemoveTagsFromResourceResponseTypeDef(TypedDict):
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListHapgsRequestListHapgsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListHsmsRequestListHsmsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLunaClientsRequestListLunaClientsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]
