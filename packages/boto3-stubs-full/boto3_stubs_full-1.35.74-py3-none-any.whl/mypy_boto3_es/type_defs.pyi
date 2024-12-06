"""
Type annotations for es service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/type_defs/)

Usage::

    ```python
    from mypy_boto3_es.type_defs import AcceptInboundCrossClusterSearchConnectionRequestRequestTypeDef

    data: AcceptInboundCrossClusterSearchConnectionRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AutoTuneDesiredStateType,
    AutoTuneStateType,
    ConfigChangeStatusType,
    DeploymentStatusType,
    DescribePackagesFilterNameType,
    DomainPackageStatusType,
    DomainProcessingStatusTypeType,
    EngineTypeType,
    ESPartitionInstanceTypeType,
    ESWarmPartitionInstanceTypeType,
    InboundCrossClusterSearchConnectionStatusCodeType,
    InitiatedByType,
    LogTypeType,
    OptionStateType,
    OutboundCrossClusterSearchConnectionStatusCodeType,
    OverallChangeStatusType,
    PackageStatusType,
    PrincipalTypeType,
    PropertyValueTypeType,
    ReservedElasticsearchInstancePaymentOptionType,
    RollbackOnDisableType,
    ScheduledAutoTuneActionTypeType,
    ScheduledAutoTuneSeverityTypeType,
    TLSSecurityPolicyType,
    UpgradeStatusType,
    UpgradeStepType,
    VolumeTypeType,
    VpcEndpointErrorCodeType,
    VpcEndpointStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcceptInboundCrossClusterSearchConnectionRequestRequestTypeDef",
    "AcceptInboundCrossClusterSearchConnectionResponseTypeDef",
    "AccessPoliciesStatusTypeDef",
    "AddTagsRequestRequestTypeDef",
    "AdditionalLimitTypeDef",
    "AdvancedOptionsStatusTypeDef",
    "AdvancedSecurityOptionsInputTypeDef",
    "AdvancedSecurityOptionsStatusTypeDef",
    "AdvancedSecurityOptionsTypeDef",
    "AssociatePackageRequestRequestTypeDef",
    "AssociatePackageResponseTypeDef",
    "AuthorizeVpcEndpointAccessRequestRequestTypeDef",
    "AuthorizeVpcEndpointAccessResponseTypeDef",
    "AuthorizedPrincipalTypeDef",
    "AutoTuneDetailsTypeDef",
    "AutoTuneMaintenanceScheduleOutputTypeDef",
    "AutoTuneMaintenanceScheduleTypeDef",
    "AutoTuneMaintenanceScheduleUnionTypeDef",
    "AutoTuneOptionsExtraOutputTypeDef",
    "AutoTuneOptionsInputTypeDef",
    "AutoTuneOptionsOutputTypeDef",
    "AutoTuneOptionsStatusTypeDef",
    "AutoTuneOptionsTypeDef",
    "AutoTuneStatusTypeDef",
    "AutoTuneTypeDef",
    "CancelDomainConfigChangeRequestRequestTypeDef",
    "CancelDomainConfigChangeResponseTypeDef",
    "CancelElasticsearchServiceSoftwareUpdateRequestRequestTypeDef",
    "CancelElasticsearchServiceSoftwareUpdateResponseTypeDef",
    "CancelledChangePropertyTypeDef",
    "ChangeProgressDetailsTypeDef",
    "ChangeProgressStageTypeDef",
    "ChangeProgressStatusDetailsTypeDef",
    "CognitoOptionsStatusTypeDef",
    "CognitoOptionsTypeDef",
    "ColdStorageOptionsTypeDef",
    "CompatibleVersionsMapTypeDef",
    "CreateElasticsearchDomainRequestRequestTypeDef",
    "CreateElasticsearchDomainResponseTypeDef",
    "CreateOutboundCrossClusterSearchConnectionRequestRequestTypeDef",
    "CreateOutboundCrossClusterSearchConnectionResponseTypeDef",
    "CreatePackageRequestRequestTypeDef",
    "CreatePackageResponseTypeDef",
    "CreateVpcEndpointRequestRequestTypeDef",
    "CreateVpcEndpointResponseTypeDef",
    "DeleteElasticsearchDomainRequestRequestTypeDef",
    "DeleteElasticsearchDomainResponseTypeDef",
    "DeleteInboundCrossClusterSearchConnectionRequestRequestTypeDef",
    "DeleteInboundCrossClusterSearchConnectionResponseTypeDef",
    "DeleteOutboundCrossClusterSearchConnectionRequestRequestTypeDef",
    "DeleteOutboundCrossClusterSearchConnectionResponseTypeDef",
    "DeletePackageRequestRequestTypeDef",
    "DeletePackageResponseTypeDef",
    "DeleteVpcEndpointRequestRequestTypeDef",
    "DeleteVpcEndpointResponseTypeDef",
    "DescribeDomainAutoTunesRequestRequestTypeDef",
    "DescribeDomainAutoTunesResponseTypeDef",
    "DescribeDomainChangeProgressRequestRequestTypeDef",
    "DescribeDomainChangeProgressResponseTypeDef",
    "DescribeElasticsearchDomainConfigRequestRequestTypeDef",
    "DescribeElasticsearchDomainConfigResponseTypeDef",
    "DescribeElasticsearchDomainRequestRequestTypeDef",
    "DescribeElasticsearchDomainResponseTypeDef",
    "DescribeElasticsearchDomainsRequestRequestTypeDef",
    "DescribeElasticsearchDomainsResponseTypeDef",
    "DescribeElasticsearchInstanceTypeLimitsRequestRequestTypeDef",
    "DescribeElasticsearchInstanceTypeLimitsResponseTypeDef",
    "DescribeInboundCrossClusterSearchConnectionsRequestRequestTypeDef",
    "DescribeInboundCrossClusterSearchConnectionsResponseTypeDef",
    "DescribeOutboundCrossClusterSearchConnectionsRequestRequestTypeDef",
    "DescribeOutboundCrossClusterSearchConnectionsResponseTypeDef",
    "DescribePackagesFilterTypeDef",
    "DescribePackagesRequestRequestTypeDef",
    "DescribePackagesResponseTypeDef",
    "DescribeReservedElasticsearchInstanceOfferingsRequestDescribeReservedElasticsearchInstanceOfferingsPaginateTypeDef",
    "DescribeReservedElasticsearchInstanceOfferingsRequestRequestTypeDef",
    "DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef",
    "DescribeReservedElasticsearchInstancesRequestDescribeReservedElasticsearchInstancesPaginateTypeDef",
    "DescribeReservedElasticsearchInstancesRequestRequestTypeDef",
    "DescribeReservedElasticsearchInstancesResponseTypeDef",
    "DescribeVpcEndpointsRequestRequestTypeDef",
    "DescribeVpcEndpointsResponseTypeDef",
    "DissociatePackageRequestRequestTypeDef",
    "DissociatePackageResponseTypeDef",
    "DomainEndpointOptionsStatusTypeDef",
    "DomainEndpointOptionsTypeDef",
    "DomainInfoTypeDef",
    "DomainInformationTypeDef",
    "DomainPackageDetailsTypeDef",
    "DryRunResultsTypeDef",
    "DurationTypeDef",
    "EBSOptionsStatusTypeDef",
    "EBSOptionsTypeDef",
    "ElasticsearchClusterConfigStatusTypeDef",
    "ElasticsearchClusterConfigTypeDef",
    "ElasticsearchDomainConfigTypeDef",
    "ElasticsearchDomainStatusTypeDef",
    "ElasticsearchVersionStatusTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionAtRestOptionsStatusTypeDef",
    "EncryptionAtRestOptionsTypeDef",
    "ErrorDetailsTypeDef",
    "FilterTypeDef",
    "GetCompatibleElasticsearchVersionsRequestRequestTypeDef",
    "GetCompatibleElasticsearchVersionsResponseTypeDef",
    "GetPackageVersionHistoryRequestRequestTypeDef",
    "GetPackageVersionHistoryResponseTypeDef",
    "GetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef",
    "GetUpgradeHistoryRequestRequestTypeDef",
    "GetUpgradeHistoryResponseTypeDef",
    "GetUpgradeStatusRequestRequestTypeDef",
    "GetUpgradeStatusResponseTypeDef",
    "InboundCrossClusterSearchConnectionStatusTypeDef",
    "InboundCrossClusterSearchConnectionTypeDef",
    "InstanceCountLimitsTypeDef",
    "InstanceLimitsTypeDef",
    "LimitsTypeDef",
    "ListDomainNamesRequestRequestTypeDef",
    "ListDomainNamesResponseTypeDef",
    "ListDomainsForPackageRequestRequestTypeDef",
    "ListDomainsForPackageResponseTypeDef",
    "ListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef",
    "ListElasticsearchInstanceTypesRequestRequestTypeDef",
    "ListElasticsearchInstanceTypesResponseTypeDef",
    "ListElasticsearchVersionsRequestListElasticsearchVersionsPaginateTypeDef",
    "ListElasticsearchVersionsRequestRequestTypeDef",
    "ListElasticsearchVersionsResponseTypeDef",
    "ListPackagesForDomainRequestRequestTypeDef",
    "ListPackagesForDomainResponseTypeDef",
    "ListTagsRequestRequestTypeDef",
    "ListTagsResponseTypeDef",
    "ListVpcEndpointAccessRequestRequestTypeDef",
    "ListVpcEndpointAccessResponseTypeDef",
    "ListVpcEndpointsForDomainRequestRequestTypeDef",
    "ListVpcEndpointsForDomainResponseTypeDef",
    "ListVpcEndpointsRequestRequestTypeDef",
    "ListVpcEndpointsResponseTypeDef",
    "LogPublishingOptionTypeDef",
    "LogPublishingOptionsStatusTypeDef",
    "MasterUserOptionsTypeDef",
    "ModifyingPropertiesTypeDef",
    "NodeToNodeEncryptionOptionsStatusTypeDef",
    "NodeToNodeEncryptionOptionsTypeDef",
    "OptionStatusTypeDef",
    "OutboundCrossClusterSearchConnectionStatusTypeDef",
    "OutboundCrossClusterSearchConnectionTypeDef",
    "PackageDetailsTypeDef",
    "PackageSourceTypeDef",
    "PackageVersionHistoryTypeDef",
    "PaginatorConfigTypeDef",
    "PurchaseReservedElasticsearchInstanceOfferingRequestRequestTypeDef",
    "PurchaseReservedElasticsearchInstanceOfferingResponseTypeDef",
    "RecurringChargeTypeDef",
    "RejectInboundCrossClusterSearchConnectionRequestRequestTypeDef",
    "RejectInboundCrossClusterSearchConnectionResponseTypeDef",
    "RemoveTagsRequestRequestTypeDef",
    "ReservedElasticsearchInstanceOfferingTypeDef",
    "ReservedElasticsearchInstanceTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeVpcEndpointAccessRequestRequestTypeDef",
    "SAMLIdpTypeDef",
    "SAMLOptionsInputTypeDef",
    "SAMLOptionsOutputTypeDef",
    "ScheduledAutoTuneDetailsTypeDef",
    "ServiceSoftwareOptionsTypeDef",
    "SnapshotOptionsStatusTypeDef",
    "SnapshotOptionsTypeDef",
    "StartElasticsearchServiceSoftwareUpdateRequestRequestTypeDef",
    "StartElasticsearchServiceSoftwareUpdateResponseTypeDef",
    "StorageTypeLimitTypeDef",
    "StorageTypeTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "UpdateElasticsearchDomainConfigRequestRequestTypeDef",
    "UpdateElasticsearchDomainConfigResponseTypeDef",
    "UpdatePackageRequestRequestTypeDef",
    "UpdatePackageResponseTypeDef",
    "UpdateVpcEndpointRequestRequestTypeDef",
    "UpdateVpcEndpointResponseTypeDef",
    "UpgradeElasticsearchDomainRequestRequestTypeDef",
    "UpgradeElasticsearchDomainResponseTypeDef",
    "UpgradeHistoryTypeDef",
    "UpgradeStepItemTypeDef",
    "VPCDerivedInfoStatusTypeDef",
    "VPCDerivedInfoTypeDef",
    "VPCOptionsTypeDef",
    "VpcEndpointErrorTypeDef",
    "VpcEndpointSummaryTypeDef",
    "VpcEndpointTypeDef",
    "ZoneAwarenessConfigTypeDef",
)

class AcceptInboundCrossClusterSearchConnectionRequestRequestTypeDef(TypedDict):
    CrossClusterSearchConnectionId: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class OptionStatusTypeDef(TypedDict):
    CreationDate: datetime
    UpdateDate: datetime
    State: OptionStateType
    UpdateVersion: NotRequired[int]
    PendingDeletion: NotRequired[bool]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class AdditionalLimitTypeDef(TypedDict):
    LimitName: NotRequired[str]
    LimitValues: NotRequired[List[str]]

class MasterUserOptionsTypeDef(TypedDict):
    MasterUserARN: NotRequired[str]
    MasterUserName: NotRequired[str]
    MasterUserPassword: NotRequired[str]

class AssociatePackageRequestRequestTypeDef(TypedDict):
    PackageID: str
    DomainName: str

class AuthorizeVpcEndpointAccessRequestRequestTypeDef(TypedDict):
    DomainName: str
    Account: str

class AuthorizedPrincipalTypeDef(TypedDict):
    PrincipalType: NotRequired[PrincipalTypeType]
    Principal: NotRequired[str]

class ScheduledAutoTuneDetailsTypeDef(TypedDict):
    Date: NotRequired[datetime]
    ActionType: NotRequired[ScheduledAutoTuneActionTypeType]
    Action: NotRequired[str]
    Severity: NotRequired[ScheduledAutoTuneSeverityTypeType]

class DurationTypeDef(TypedDict):
    Value: NotRequired[int]
    Unit: NotRequired[Literal["HOURS"]]

TimestampTypeDef = Union[datetime, str]

class AutoTuneOptionsOutputTypeDef(TypedDict):
    State: NotRequired[AutoTuneStateType]
    ErrorMessage: NotRequired[str]

class AutoTuneStatusTypeDef(TypedDict):
    CreationDate: datetime
    UpdateDate: datetime
    State: AutoTuneStateType
    UpdateVersion: NotRequired[int]
    ErrorMessage: NotRequired[str]
    PendingDeletion: NotRequired[bool]

class CancelDomainConfigChangeRequestRequestTypeDef(TypedDict):
    DomainName: str
    DryRun: NotRequired[bool]

class CancelledChangePropertyTypeDef(TypedDict):
    PropertyName: NotRequired[str]
    CancelledValue: NotRequired[str]
    ActiveValue: NotRequired[str]

class CancelElasticsearchServiceSoftwareUpdateRequestRequestTypeDef(TypedDict):
    DomainName: str

class ServiceSoftwareOptionsTypeDef(TypedDict):
    CurrentVersion: NotRequired[str]
    NewVersion: NotRequired[str]
    UpdateAvailable: NotRequired[bool]
    Cancellable: NotRequired[bool]
    UpdateStatus: NotRequired[DeploymentStatusType]
    Description: NotRequired[str]
    AutomatedUpdateDate: NotRequired[datetime]
    OptionalDeployment: NotRequired[bool]

class ChangeProgressDetailsTypeDef(TypedDict):
    ChangeId: NotRequired[str]
    Message: NotRequired[str]
    ConfigChangeStatus: NotRequired[ConfigChangeStatusType]
    StartTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    InitiatedBy: NotRequired[InitiatedByType]

class ChangeProgressStageTypeDef(TypedDict):
    Name: NotRequired[str]
    Status: NotRequired[str]
    Description: NotRequired[str]
    LastUpdated: NotRequired[datetime]

class CognitoOptionsTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    UserPoolId: NotRequired[str]
    IdentityPoolId: NotRequired[str]
    RoleArn: NotRequired[str]

class ColdStorageOptionsTypeDef(TypedDict):
    Enabled: bool

class CompatibleVersionsMapTypeDef(TypedDict):
    SourceVersion: NotRequired[str]
    TargetVersions: NotRequired[List[str]]

class DomainEndpointOptionsTypeDef(TypedDict):
    EnforceHTTPS: NotRequired[bool]
    TLSSecurityPolicy: NotRequired[TLSSecurityPolicyType]
    CustomEndpointEnabled: NotRequired[bool]
    CustomEndpoint: NotRequired[str]
    CustomEndpointCertificateArn: NotRequired[str]

class EBSOptionsTypeDef(TypedDict):
    EBSEnabled: NotRequired[bool]
    VolumeType: NotRequired[VolumeTypeType]
    VolumeSize: NotRequired[int]
    Iops: NotRequired[int]
    Throughput: NotRequired[int]

class EncryptionAtRestOptionsTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    KmsKeyId: NotRequired[str]

class LogPublishingOptionTypeDef(TypedDict):
    CloudWatchLogsLogGroupArn: NotRequired[str]
    Enabled: NotRequired[bool]

class NodeToNodeEncryptionOptionsTypeDef(TypedDict):
    Enabled: NotRequired[bool]

class SnapshotOptionsTypeDef(TypedDict):
    AutomatedSnapshotStartHour: NotRequired[int]

class VPCOptionsTypeDef(TypedDict):
    SubnetIds: NotRequired[Sequence[str]]
    SecurityGroupIds: NotRequired[Sequence[str]]

class DomainInformationTypeDef(TypedDict):
    DomainName: str
    OwnerId: NotRequired[str]
    Region: NotRequired[str]

class OutboundCrossClusterSearchConnectionStatusTypeDef(TypedDict):
    StatusCode: NotRequired[OutboundCrossClusterSearchConnectionStatusCodeType]
    Message: NotRequired[str]

class PackageSourceTypeDef(TypedDict):
    S3BucketName: NotRequired[str]
    S3Key: NotRequired[str]

class DeleteElasticsearchDomainRequestRequestTypeDef(TypedDict):
    DomainName: str

class DeleteInboundCrossClusterSearchConnectionRequestRequestTypeDef(TypedDict):
    CrossClusterSearchConnectionId: str

class DeleteOutboundCrossClusterSearchConnectionRequestRequestTypeDef(TypedDict):
    CrossClusterSearchConnectionId: str

class DeletePackageRequestRequestTypeDef(TypedDict):
    PackageID: str

class DeleteVpcEndpointRequestRequestTypeDef(TypedDict):
    VpcEndpointId: str

class VpcEndpointSummaryTypeDef(TypedDict):
    VpcEndpointId: NotRequired[str]
    VpcEndpointOwner: NotRequired[str]
    DomainArn: NotRequired[str]
    Status: NotRequired[VpcEndpointStatusType]

class DescribeDomainAutoTunesRequestRequestTypeDef(TypedDict):
    DomainName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeDomainChangeProgressRequestRequestTypeDef(TypedDict):
    DomainName: str
    ChangeId: NotRequired[str]

class DescribeElasticsearchDomainConfigRequestRequestTypeDef(TypedDict):
    DomainName: str

class DescribeElasticsearchDomainRequestRequestTypeDef(TypedDict):
    DomainName: str

class DescribeElasticsearchDomainsRequestRequestTypeDef(TypedDict):
    DomainNames: Sequence[str]

class DescribeElasticsearchInstanceTypeLimitsRequestRequestTypeDef(TypedDict):
    InstanceType: ESPartitionInstanceTypeType
    ElasticsearchVersion: str
    DomainName: NotRequired[str]

class FilterTypeDef(TypedDict):
    Name: NotRequired[str]
    Values: NotRequired[Sequence[str]]

class DescribePackagesFilterTypeDef(TypedDict):
    Name: NotRequired[DescribePackagesFilterNameType]
    Value: NotRequired[Sequence[str]]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeReservedElasticsearchInstanceOfferingsRequestRequestTypeDef(TypedDict):
    ReservedElasticsearchInstanceOfferingId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeReservedElasticsearchInstancesRequestRequestTypeDef(TypedDict):
    ReservedElasticsearchInstanceId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeVpcEndpointsRequestRequestTypeDef(TypedDict):
    VpcEndpointIds: Sequence[str]

class VpcEndpointErrorTypeDef(TypedDict):
    VpcEndpointId: NotRequired[str]
    ErrorCode: NotRequired[VpcEndpointErrorCodeType]
    ErrorMessage: NotRequired[str]

class DissociatePackageRequestRequestTypeDef(TypedDict):
    PackageID: str
    DomainName: str

class DomainInfoTypeDef(TypedDict):
    DomainName: NotRequired[str]
    EngineType: NotRequired[EngineTypeType]

class ErrorDetailsTypeDef(TypedDict):
    ErrorType: NotRequired[str]
    ErrorMessage: NotRequired[str]

class DryRunResultsTypeDef(TypedDict):
    DeploymentType: NotRequired[str]
    Message: NotRequired[str]

class ZoneAwarenessConfigTypeDef(TypedDict):
    AvailabilityZoneCount: NotRequired[int]

class ModifyingPropertiesTypeDef(TypedDict):
    Name: NotRequired[str]
    ActiveValue: NotRequired[str]
    PendingValue: NotRequired[str]
    ValueType: NotRequired[PropertyValueTypeType]

class VPCDerivedInfoTypeDef(TypedDict):
    VPCId: NotRequired[str]
    SubnetIds: NotRequired[List[str]]
    AvailabilityZones: NotRequired[List[str]]
    SecurityGroupIds: NotRequired[List[str]]

class GetCompatibleElasticsearchVersionsRequestRequestTypeDef(TypedDict):
    DomainName: NotRequired[str]

class GetPackageVersionHistoryRequestRequestTypeDef(TypedDict):
    PackageID: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class PackageVersionHistoryTypeDef(TypedDict):
    PackageVersion: NotRequired[str]
    CommitMessage: NotRequired[str]
    CreatedAt: NotRequired[datetime]

class GetUpgradeHistoryRequestRequestTypeDef(TypedDict):
    DomainName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class GetUpgradeStatusRequestRequestTypeDef(TypedDict):
    DomainName: str

class InboundCrossClusterSearchConnectionStatusTypeDef(TypedDict):
    StatusCode: NotRequired[InboundCrossClusterSearchConnectionStatusCodeType]
    Message: NotRequired[str]

class InstanceCountLimitsTypeDef(TypedDict):
    MinimumInstanceCount: NotRequired[int]
    MaximumInstanceCount: NotRequired[int]

class ListDomainNamesRequestRequestTypeDef(TypedDict):
    EngineType: NotRequired[EngineTypeType]

class ListDomainsForPackageRequestRequestTypeDef(TypedDict):
    PackageID: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListElasticsearchInstanceTypesRequestRequestTypeDef(TypedDict):
    ElasticsearchVersion: str
    DomainName: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListElasticsearchVersionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListPackagesForDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsRequestRequestTypeDef(TypedDict):
    ARN: str

class ListVpcEndpointAccessRequestRequestTypeDef(TypedDict):
    DomainName: str
    NextToken: NotRequired[str]

class ListVpcEndpointsForDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    NextToken: NotRequired[str]

class ListVpcEndpointsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]

class PurchaseReservedElasticsearchInstanceOfferingRequestRequestTypeDef(TypedDict):
    ReservedElasticsearchInstanceOfferingId: str
    ReservationName: str
    InstanceCount: NotRequired[int]

class RecurringChargeTypeDef(TypedDict):
    RecurringChargeAmount: NotRequired[float]
    RecurringChargeFrequency: NotRequired[str]

class RejectInboundCrossClusterSearchConnectionRequestRequestTypeDef(TypedDict):
    CrossClusterSearchConnectionId: str

class RemoveTagsRequestRequestTypeDef(TypedDict):
    ARN: str
    TagKeys: Sequence[str]

class RevokeVpcEndpointAccessRequestRequestTypeDef(TypedDict):
    DomainName: str
    Account: str

class SAMLIdpTypeDef(TypedDict):
    MetadataContent: str
    EntityId: str

class StartElasticsearchServiceSoftwareUpdateRequestRequestTypeDef(TypedDict):
    DomainName: str

class StorageTypeLimitTypeDef(TypedDict):
    LimitName: NotRequired[str]
    LimitValues: NotRequired[List[str]]

class UpgradeElasticsearchDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    TargetVersion: str
    PerformCheckOnly: NotRequired[bool]

class UpgradeStepItemTypeDef(TypedDict):
    UpgradeStep: NotRequired[UpgradeStepType]
    UpgradeStepStatus: NotRequired[UpgradeStatusType]
    Issues: NotRequired[List[str]]
    ProgressPercent: NotRequired[float]

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetUpgradeStatusResponseTypeDef(TypedDict):
    UpgradeStep: UpgradeStepType
    StepStatus: UpgradeStatusType
    UpgradeName: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListElasticsearchInstanceTypesResponseTypeDef(TypedDict):
    ElasticsearchInstanceTypes: List[ESPartitionInstanceTypeType]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListElasticsearchVersionsResponseTypeDef(TypedDict):
    ElasticsearchVersions: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PurchaseReservedElasticsearchInstanceOfferingResponseTypeDef(TypedDict):
    ReservedElasticsearchInstanceId: str
    ReservationName: str
    ResponseMetadata: ResponseMetadataTypeDef

class AccessPoliciesStatusTypeDef(TypedDict):
    Options: str
    Status: OptionStatusTypeDef

class AdvancedOptionsStatusTypeDef(TypedDict):
    Options: Dict[str, str]
    Status: OptionStatusTypeDef

class ElasticsearchVersionStatusTypeDef(TypedDict):
    Options: str
    Status: OptionStatusTypeDef

class AddTagsRequestRequestTypeDef(TypedDict):
    ARN: str
    TagList: Sequence[TagTypeDef]

class ListTagsResponseTypeDef(TypedDict):
    TagList: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class AuthorizeVpcEndpointAccessResponseTypeDef(TypedDict):
    AuthorizedPrincipal: AuthorizedPrincipalTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListVpcEndpointAccessResponseTypeDef(TypedDict):
    AuthorizedPrincipalList: List[AuthorizedPrincipalTypeDef]
    NextToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class AutoTuneDetailsTypeDef(TypedDict):
    ScheduledAutoTuneDetails: NotRequired[ScheduledAutoTuneDetailsTypeDef]

class AutoTuneMaintenanceScheduleOutputTypeDef(TypedDict):
    StartAt: NotRequired[datetime]
    Duration: NotRequired[DurationTypeDef]
    CronExpressionForRecurrence: NotRequired[str]

class AutoTuneMaintenanceScheduleTypeDef(TypedDict):
    StartAt: NotRequired[TimestampTypeDef]
    Duration: NotRequired[DurationTypeDef]
    CronExpressionForRecurrence: NotRequired[str]

class CancelDomainConfigChangeResponseTypeDef(TypedDict):
    DryRun: bool
    CancelledChangeIds: List[str]
    CancelledChangeProperties: List[CancelledChangePropertyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CancelElasticsearchServiceSoftwareUpdateResponseTypeDef(TypedDict):
    ServiceSoftwareOptions: ServiceSoftwareOptionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartElasticsearchServiceSoftwareUpdateResponseTypeDef(TypedDict):
    ServiceSoftwareOptions: ServiceSoftwareOptionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpgradeElasticsearchDomainResponseTypeDef(TypedDict):
    DomainName: str
    TargetVersion: str
    PerformCheckOnly: bool
    ChangeProgressDetails: ChangeProgressDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ChangeProgressStatusDetailsTypeDef(TypedDict):
    ChangeId: NotRequired[str]
    StartTime: NotRequired[datetime]
    Status: NotRequired[OverallChangeStatusType]
    PendingProperties: NotRequired[List[str]]
    CompletedProperties: NotRequired[List[str]]
    TotalNumberOfStages: NotRequired[int]
    ChangeProgressStages: NotRequired[List[ChangeProgressStageTypeDef]]
    ConfigChangeStatus: NotRequired[ConfigChangeStatusType]
    LastUpdatedTime: NotRequired[datetime]
    InitiatedBy: NotRequired[InitiatedByType]

class CognitoOptionsStatusTypeDef(TypedDict):
    Options: CognitoOptionsTypeDef
    Status: OptionStatusTypeDef

class GetCompatibleElasticsearchVersionsResponseTypeDef(TypedDict):
    CompatibleElasticsearchVersions: List[CompatibleVersionsMapTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DomainEndpointOptionsStatusTypeDef(TypedDict):
    Options: DomainEndpointOptionsTypeDef
    Status: OptionStatusTypeDef

class EBSOptionsStatusTypeDef(TypedDict):
    Options: EBSOptionsTypeDef
    Status: OptionStatusTypeDef

class EncryptionAtRestOptionsStatusTypeDef(TypedDict):
    Options: EncryptionAtRestOptionsTypeDef
    Status: OptionStatusTypeDef

class LogPublishingOptionsStatusTypeDef(TypedDict):
    Options: NotRequired[Dict[LogTypeType, LogPublishingOptionTypeDef]]
    Status: NotRequired[OptionStatusTypeDef]

class NodeToNodeEncryptionOptionsStatusTypeDef(TypedDict):
    Options: NodeToNodeEncryptionOptionsTypeDef
    Status: OptionStatusTypeDef

class SnapshotOptionsStatusTypeDef(TypedDict):
    Options: SnapshotOptionsTypeDef
    Status: OptionStatusTypeDef

class CreateVpcEndpointRequestRequestTypeDef(TypedDict):
    DomainArn: str
    VpcOptions: VPCOptionsTypeDef
    ClientToken: NotRequired[str]

class UpdateVpcEndpointRequestRequestTypeDef(TypedDict):
    VpcEndpointId: str
    VpcOptions: VPCOptionsTypeDef

class CreateOutboundCrossClusterSearchConnectionRequestRequestTypeDef(TypedDict):
    SourceDomainInfo: DomainInformationTypeDef
    DestinationDomainInfo: DomainInformationTypeDef
    ConnectionAlias: str

class CreateOutboundCrossClusterSearchConnectionResponseTypeDef(TypedDict):
    SourceDomainInfo: DomainInformationTypeDef
    DestinationDomainInfo: DomainInformationTypeDef
    ConnectionAlias: str
    ConnectionStatus: OutboundCrossClusterSearchConnectionStatusTypeDef
    CrossClusterSearchConnectionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class OutboundCrossClusterSearchConnectionTypeDef(TypedDict):
    SourceDomainInfo: NotRequired[DomainInformationTypeDef]
    DestinationDomainInfo: NotRequired[DomainInformationTypeDef]
    CrossClusterSearchConnectionId: NotRequired[str]
    ConnectionAlias: NotRequired[str]
    ConnectionStatus: NotRequired[OutboundCrossClusterSearchConnectionStatusTypeDef]

class CreatePackageRequestRequestTypeDef(TypedDict):
    PackageName: str
    PackageType: Literal["TXT-DICTIONARY"]
    PackageSource: PackageSourceTypeDef
    PackageDescription: NotRequired[str]

class UpdatePackageRequestRequestTypeDef(TypedDict):
    PackageID: str
    PackageSource: PackageSourceTypeDef
    PackageDescription: NotRequired[str]
    CommitMessage: NotRequired[str]

class DeleteVpcEndpointResponseTypeDef(TypedDict):
    VpcEndpointSummary: VpcEndpointSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListVpcEndpointsForDomainResponseTypeDef(TypedDict):
    VpcEndpointSummaryList: List[VpcEndpointSummaryTypeDef]
    NextToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListVpcEndpointsResponseTypeDef(TypedDict):
    VpcEndpointSummaryList: List[VpcEndpointSummaryTypeDef]
    NextToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeInboundCrossClusterSearchConnectionsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeOutboundCrossClusterSearchConnectionsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribePackagesRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[DescribePackagesFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeReservedElasticsearchInstanceOfferingsRequestDescribeReservedElasticsearchInstanceOfferingsPaginateTypeDef(
    TypedDict
):
    ReservedElasticsearchInstanceOfferingId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeReservedElasticsearchInstancesRequestDescribeReservedElasticsearchInstancesPaginateTypeDef(
    TypedDict
):
    ReservedElasticsearchInstanceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef(TypedDict):
    DomainName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef(TypedDict):
    ElasticsearchVersion: str
    DomainName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListElasticsearchVersionsRequestListElasticsearchVersionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDomainNamesResponseTypeDef(TypedDict):
    DomainNames: List[DomainInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DomainPackageDetailsTypeDef(TypedDict):
    PackageID: NotRequired[str]
    PackageName: NotRequired[str]
    PackageType: NotRequired[Literal["TXT-DICTIONARY"]]
    LastUpdated: NotRequired[datetime]
    DomainName: NotRequired[str]
    DomainPackageStatus: NotRequired[DomainPackageStatusType]
    PackageVersion: NotRequired[str]
    ReferencePath: NotRequired[str]
    ErrorDetails: NotRequired[ErrorDetailsTypeDef]

class PackageDetailsTypeDef(TypedDict):
    PackageID: NotRequired[str]
    PackageName: NotRequired[str]
    PackageType: NotRequired[Literal["TXT-DICTIONARY"]]
    PackageDescription: NotRequired[str]
    PackageStatus: NotRequired[PackageStatusType]
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    AvailablePackageVersion: NotRequired[str]
    ErrorDetails: NotRequired[ErrorDetailsTypeDef]

class ElasticsearchClusterConfigTypeDef(TypedDict):
    InstanceType: NotRequired[ESPartitionInstanceTypeType]
    InstanceCount: NotRequired[int]
    DedicatedMasterEnabled: NotRequired[bool]
    ZoneAwarenessEnabled: NotRequired[bool]
    ZoneAwarenessConfig: NotRequired[ZoneAwarenessConfigTypeDef]
    DedicatedMasterType: NotRequired[ESPartitionInstanceTypeType]
    DedicatedMasterCount: NotRequired[int]
    WarmEnabled: NotRequired[bool]
    WarmType: NotRequired[ESWarmPartitionInstanceTypeType]
    WarmCount: NotRequired[int]
    ColdStorageOptions: NotRequired[ColdStorageOptionsTypeDef]

class VPCDerivedInfoStatusTypeDef(TypedDict):
    Options: VPCDerivedInfoTypeDef
    Status: OptionStatusTypeDef

class VpcEndpointTypeDef(TypedDict):
    VpcEndpointId: NotRequired[str]
    VpcEndpointOwner: NotRequired[str]
    DomainArn: NotRequired[str]
    VpcOptions: NotRequired[VPCDerivedInfoTypeDef]
    Status: NotRequired[VpcEndpointStatusType]
    Endpoint: NotRequired[str]

class GetPackageVersionHistoryResponseTypeDef(TypedDict):
    PackageID: str
    PackageVersionHistoryList: List[PackageVersionHistoryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class InboundCrossClusterSearchConnectionTypeDef(TypedDict):
    SourceDomainInfo: NotRequired[DomainInformationTypeDef]
    DestinationDomainInfo: NotRequired[DomainInformationTypeDef]
    CrossClusterSearchConnectionId: NotRequired[str]
    ConnectionStatus: NotRequired[InboundCrossClusterSearchConnectionStatusTypeDef]

class InstanceLimitsTypeDef(TypedDict):
    InstanceCountLimits: NotRequired[InstanceCountLimitsTypeDef]

class ReservedElasticsearchInstanceOfferingTypeDef(TypedDict):
    ReservedElasticsearchInstanceOfferingId: NotRequired[str]
    ElasticsearchInstanceType: NotRequired[ESPartitionInstanceTypeType]
    Duration: NotRequired[int]
    FixedPrice: NotRequired[float]
    UsagePrice: NotRequired[float]
    CurrencyCode: NotRequired[str]
    PaymentOption: NotRequired[ReservedElasticsearchInstancePaymentOptionType]
    RecurringCharges: NotRequired[List[RecurringChargeTypeDef]]

class ReservedElasticsearchInstanceTypeDef(TypedDict):
    ReservationName: NotRequired[str]
    ReservedElasticsearchInstanceId: NotRequired[str]
    ReservedElasticsearchInstanceOfferingId: NotRequired[str]
    ElasticsearchInstanceType: NotRequired[ESPartitionInstanceTypeType]
    StartTime: NotRequired[datetime]
    Duration: NotRequired[int]
    FixedPrice: NotRequired[float]
    UsagePrice: NotRequired[float]
    CurrencyCode: NotRequired[str]
    ElasticsearchInstanceCount: NotRequired[int]
    State: NotRequired[str]
    PaymentOption: NotRequired[ReservedElasticsearchInstancePaymentOptionType]
    RecurringCharges: NotRequired[List[RecurringChargeTypeDef]]

class SAMLOptionsInputTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    Idp: NotRequired[SAMLIdpTypeDef]
    MasterUserName: NotRequired[str]
    MasterBackendRole: NotRequired[str]
    SubjectKey: NotRequired[str]
    RolesKey: NotRequired[str]
    SessionTimeoutMinutes: NotRequired[int]

class SAMLOptionsOutputTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    Idp: NotRequired[SAMLIdpTypeDef]
    SubjectKey: NotRequired[str]
    RolesKey: NotRequired[str]
    SessionTimeoutMinutes: NotRequired[int]

class StorageTypeTypeDef(TypedDict):
    StorageTypeName: NotRequired[str]
    StorageSubTypeName: NotRequired[str]
    StorageTypeLimits: NotRequired[List[StorageTypeLimitTypeDef]]

class UpgradeHistoryTypeDef(TypedDict):
    UpgradeName: NotRequired[str]
    StartTimestamp: NotRequired[datetime]
    UpgradeStatus: NotRequired[UpgradeStatusType]
    StepsList: NotRequired[List[UpgradeStepItemTypeDef]]

class AutoTuneTypeDef(TypedDict):
    AutoTuneType: NotRequired[Literal["SCHEDULED_ACTION"]]
    AutoTuneDetails: NotRequired[AutoTuneDetailsTypeDef]

class AutoTuneOptionsExtraOutputTypeDef(TypedDict):
    DesiredState: NotRequired[AutoTuneDesiredStateType]
    RollbackOnDisable: NotRequired[RollbackOnDisableType]
    MaintenanceSchedules: NotRequired[List[AutoTuneMaintenanceScheduleOutputTypeDef]]

AutoTuneMaintenanceScheduleUnionTypeDef = Union[
    AutoTuneMaintenanceScheduleTypeDef, AutoTuneMaintenanceScheduleOutputTypeDef
]

class DescribeDomainChangeProgressResponseTypeDef(TypedDict):
    ChangeProgressStatus: ChangeProgressStatusDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteOutboundCrossClusterSearchConnectionResponseTypeDef(TypedDict):
    CrossClusterSearchConnection: OutboundCrossClusterSearchConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeOutboundCrossClusterSearchConnectionsResponseTypeDef(TypedDict):
    CrossClusterSearchConnections: List[OutboundCrossClusterSearchConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class AssociatePackageResponseTypeDef(TypedDict):
    DomainPackageDetails: DomainPackageDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DissociatePackageResponseTypeDef(TypedDict):
    DomainPackageDetails: DomainPackageDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDomainsForPackageResponseTypeDef(TypedDict):
    DomainPackageDetailsList: List[DomainPackageDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPackagesForDomainResponseTypeDef(TypedDict):
    DomainPackageDetailsList: List[DomainPackageDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreatePackageResponseTypeDef(TypedDict):
    PackageDetails: PackageDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePackageResponseTypeDef(TypedDict):
    PackageDetails: PackageDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePackagesResponseTypeDef(TypedDict):
    PackageDetailsList: List[PackageDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdatePackageResponseTypeDef(TypedDict):
    PackageDetails: PackageDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ElasticsearchClusterConfigStatusTypeDef(TypedDict):
    Options: ElasticsearchClusterConfigTypeDef
    Status: OptionStatusTypeDef

class CreateVpcEndpointResponseTypeDef(TypedDict):
    VpcEndpoint: VpcEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeVpcEndpointsResponseTypeDef(TypedDict):
    VpcEndpoints: List[VpcEndpointTypeDef]
    VpcEndpointErrors: List[VpcEndpointErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateVpcEndpointResponseTypeDef(TypedDict):
    VpcEndpoint: VpcEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AcceptInboundCrossClusterSearchConnectionResponseTypeDef(TypedDict):
    CrossClusterSearchConnection: InboundCrossClusterSearchConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteInboundCrossClusterSearchConnectionResponseTypeDef(TypedDict):
    CrossClusterSearchConnection: InboundCrossClusterSearchConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeInboundCrossClusterSearchConnectionsResponseTypeDef(TypedDict):
    CrossClusterSearchConnections: List[InboundCrossClusterSearchConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RejectInboundCrossClusterSearchConnectionResponseTypeDef(TypedDict):
    CrossClusterSearchConnection: InboundCrossClusterSearchConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef(TypedDict):
    ReservedElasticsearchInstanceOfferings: List[ReservedElasticsearchInstanceOfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeReservedElasticsearchInstancesResponseTypeDef(TypedDict):
    ReservedElasticsearchInstances: List[ReservedElasticsearchInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class AdvancedSecurityOptionsInputTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    InternalUserDatabaseEnabled: NotRequired[bool]
    MasterUserOptions: NotRequired[MasterUserOptionsTypeDef]
    SAMLOptions: NotRequired[SAMLOptionsInputTypeDef]
    AnonymousAuthEnabled: NotRequired[bool]

class AdvancedSecurityOptionsTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    InternalUserDatabaseEnabled: NotRequired[bool]
    SAMLOptions: NotRequired[SAMLOptionsOutputTypeDef]
    AnonymousAuthDisableDate: NotRequired[datetime]
    AnonymousAuthEnabled: NotRequired[bool]

class LimitsTypeDef(TypedDict):
    StorageTypes: NotRequired[List[StorageTypeTypeDef]]
    InstanceLimits: NotRequired[InstanceLimitsTypeDef]
    AdditionalLimits: NotRequired[List[AdditionalLimitTypeDef]]

class GetUpgradeHistoryResponseTypeDef(TypedDict):
    UpgradeHistories: List[UpgradeHistoryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeDomainAutoTunesResponseTypeDef(TypedDict):
    AutoTunes: List[AutoTuneTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class AutoTuneOptionsStatusTypeDef(TypedDict):
    Options: NotRequired[AutoTuneOptionsExtraOutputTypeDef]
    Status: NotRequired[AutoTuneStatusTypeDef]

class AutoTuneOptionsInputTypeDef(TypedDict):
    DesiredState: NotRequired[AutoTuneDesiredStateType]
    MaintenanceSchedules: NotRequired[Sequence[AutoTuneMaintenanceScheduleUnionTypeDef]]

class AutoTuneOptionsTypeDef(TypedDict):
    DesiredState: NotRequired[AutoTuneDesiredStateType]
    RollbackOnDisable: NotRequired[RollbackOnDisableType]
    MaintenanceSchedules: NotRequired[Sequence[AutoTuneMaintenanceScheduleUnionTypeDef]]

class AdvancedSecurityOptionsStatusTypeDef(TypedDict):
    Options: AdvancedSecurityOptionsTypeDef
    Status: OptionStatusTypeDef

class ElasticsearchDomainStatusTypeDef(TypedDict):
    DomainId: str
    DomainName: str
    ARN: str
    ElasticsearchClusterConfig: ElasticsearchClusterConfigTypeDef
    Created: NotRequired[bool]
    Deleted: NotRequired[bool]
    Endpoint: NotRequired[str]
    Endpoints: NotRequired[Dict[str, str]]
    Processing: NotRequired[bool]
    UpgradeProcessing: NotRequired[bool]
    ElasticsearchVersion: NotRequired[str]
    EBSOptions: NotRequired[EBSOptionsTypeDef]
    AccessPolicies: NotRequired[str]
    SnapshotOptions: NotRequired[SnapshotOptionsTypeDef]
    VPCOptions: NotRequired[VPCDerivedInfoTypeDef]
    CognitoOptions: NotRequired[CognitoOptionsTypeDef]
    EncryptionAtRestOptions: NotRequired[EncryptionAtRestOptionsTypeDef]
    NodeToNodeEncryptionOptions: NotRequired[NodeToNodeEncryptionOptionsTypeDef]
    AdvancedOptions: NotRequired[Dict[str, str]]
    LogPublishingOptions: NotRequired[Dict[LogTypeType, LogPublishingOptionTypeDef]]
    ServiceSoftwareOptions: NotRequired[ServiceSoftwareOptionsTypeDef]
    DomainEndpointOptions: NotRequired[DomainEndpointOptionsTypeDef]
    AdvancedSecurityOptions: NotRequired[AdvancedSecurityOptionsTypeDef]
    AutoTuneOptions: NotRequired[AutoTuneOptionsOutputTypeDef]
    ChangeProgressDetails: NotRequired[ChangeProgressDetailsTypeDef]
    DomainProcessingStatus: NotRequired[DomainProcessingStatusTypeType]
    ModifyingProperties: NotRequired[List[ModifyingPropertiesTypeDef]]

class DescribeElasticsearchInstanceTypeLimitsResponseTypeDef(TypedDict):
    LimitsByRole: Dict[str, LimitsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateElasticsearchDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    ElasticsearchVersion: NotRequired[str]
    ElasticsearchClusterConfig: NotRequired[ElasticsearchClusterConfigTypeDef]
    EBSOptions: NotRequired[EBSOptionsTypeDef]
    AccessPolicies: NotRequired[str]
    SnapshotOptions: NotRequired[SnapshotOptionsTypeDef]
    VPCOptions: NotRequired[VPCOptionsTypeDef]
    CognitoOptions: NotRequired[CognitoOptionsTypeDef]
    EncryptionAtRestOptions: NotRequired[EncryptionAtRestOptionsTypeDef]
    NodeToNodeEncryptionOptions: NotRequired[NodeToNodeEncryptionOptionsTypeDef]
    AdvancedOptions: NotRequired[Mapping[str, str]]
    LogPublishingOptions: NotRequired[Mapping[LogTypeType, LogPublishingOptionTypeDef]]
    DomainEndpointOptions: NotRequired[DomainEndpointOptionsTypeDef]
    AdvancedSecurityOptions: NotRequired[AdvancedSecurityOptionsInputTypeDef]
    AutoTuneOptions: NotRequired[AutoTuneOptionsInputTypeDef]
    TagList: NotRequired[Sequence[TagTypeDef]]

class UpdateElasticsearchDomainConfigRequestRequestTypeDef(TypedDict):
    DomainName: str
    ElasticsearchClusterConfig: NotRequired[ElasticsearchClusterConfigTypeDef]
    EBSOptions: NotRequired[EBSOptionsTypeDef]
    SnapshotOptions: NotRequired[SnapshotOptionsTypeDef]
    VPCOptions: NotRequired[VPCOptionsTypeDef]
    CognitoOptions: NotRequired[CognitoOptionsTypeDef]
    AdvancedOptions: NotRequired[Mapping[str, str]]
    AccessPolicies: NotRequired[str]
    LogPublishingOptions: NotRequired[Mapping[LogTypeType, LogPublishingOptionTypeDef]]
    DomainEndpointOptions: NotRequired[DomainEndpointOptionsTypeDef]
    AdvancedSecurityOptions: NotRequired[AdvancedSecurityOptionsInputTypeDef]
    NodeToNodeEncryptionOptions: NotRequired[NodeToNodeEncryptionOptionsTypeDef]
    EncryptionAtRestOptions: NotRequired[EncryptionAtRestOptionsTypeDef]
    AutoTuneOptions: NotRequired[AutoTuneOptionsTypeDef]
    DryRun: NotRequired[bool]

class ElasticsearchDomainConfigTypeDef(TypedDict):
    ElasticsearchVersion: NotRequired[ElasticsearchVersionStatusTypeDef]
    ElasticsearchClusterConfig: NotRequired[ElasticsearchClusterConfigStatusTypeDef]
    EBSOptions: NotRequired[EBSOptionsStatusTypeDef]
    AccessPolicies: NotRequired[AccessPoliciesStatusTypeDef]
    SnapshotOptions: NotRequired[SnapshotOptionsStatusTypeDef]
    VPCOptions: NotRequired[VPCDerivedInfoStatusTypeDef]
    CognitoOptions: NotRequired[CognitoOptionsStatusTypeDef]
    EncryptionAtRestOptions: NotRequired[EncryptionAtRestOptionsStatusTypeDef]
    NodeToNodeEncryptionOptions: NotRequired[NodeToNodeEncryptionOptionsStatusTypeDef]
    AdvancedOptions: NotRequired[AdvancedOptionsStatusTypeDef]
    LogPublishingOptions: NotRequired[LogPublishingOptionsStatusTypeDef]
    DomainEndpointOptions: NotRequired[DomainEndpointOptionsStatusTypeDef]
    AdvancedSecurityOptions: NotRequired[AdvancedSecurityOptionsStatusTypeDef]
    AutoTuneOptions: NotRequired[AutoTuneOptionsStatusTypeDef]
    ChangeProgressDetails: NotRequired[ChangeProgressDetailsTypeDef]
    ModifyingProperties: NotRequired[List[ModifyingPropertiesTypeDef]]

class CreateElasticsearchDomainResponseTypeDef(TypedDict):
    DomainStatus: ElasticsearchDomainStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteElasticsearchDomainResponseTypeDef(TypedDict):
    DomainStatus: ElasticsearchDomainStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeElasticsearchDomainResponseTypeDef(TypedDict):
    DomainStatus: ElasticsearchDomainStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeElasticsearchDomainsResponseTypeDef(TypedDict):
    DomainStatusList: List[ElasticsearchDomainStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeElasticsearchDomainConfigResponseTypeDef(TypedDict):
    DomainConfig: ElasticsearchDomainConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateElasticsearchDomainConfigResponseTypeDef(TypedDict):
    DomainConfig: ElasticsearchDomainConfigTypeDef
    DryRunResults: DryRunResultsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
