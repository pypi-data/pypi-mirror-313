"""
Type annotations for lightsail service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lightsail/type_defs/)

Usage::

    ```python
    from mypy_boto3_lightsail.type_defs import AccessKeyLastUsedTypeDef

    data: AccessKeyLastUsedTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AccessDirectionType,
    AccessTypeType,
    AccountLevelBpaSyncStatusType,
    AddOnTypeType,
    AlarmStateType,
    AutoMountStatusType,
    AutoSnapshotStatusType,
    BehaviorEnumType,
    BlueprintTypeType,
    BPAStatusMessageType,
    BucketMetricNameType,
    CertificateDomainValidationStatusType,
    CertificateStatusType,
    ComparisonOperatorType,
    ContactMethodStatusType,
    ContactProtocolType,
    ContainerServiceDeploymentStateType,
    ContainerServiceMetricNameType,
    ContainerServicePowerNameType,
    ContainerServiceProtocolType,
    ContainerServiceStateDetailCodeType,
    ContainerServiceStateType,
    DiskSnapshotStateType,
    DiskStateType,
    DistributionMetricNameType,
    DnsRecordCreationStateCodeType,
    ExportSnapshotRecordSourceTypeType,
    ForwardValuesType,
    HeaderEnumType,
    HttpEndpointType,
    HttpProtocolIpv6Type,
    HttpTokensType,
    InstanceAccessProtocolType,
    InstanceHealthReasonType,
    InstanceHealthStateType,
    InstanceMetadataStateType,
    InstanceMetricNameType,
    InstancePlatformType,
    InstanceSnapshotStateType,
    IpAddressTypeType,
    LoadBalancerAttributeNameType,
    LoadBalancerMetricNameType,
    LoadBalancerProtocolType,
    LoadBalancerStateType,
    LoadBalancerTlsCertificateDnsRecordCreationStateCodeType,
    LoadBalancerTlsCertificateDomainStatusType,
    LoadBalancerTlsCertificateFailureReasonType,
    LoadBalancerTlsCertificateRenewalStatusType,
    LoadBalancerTlsCertificateRevocationReasonType,
    LoadBalancerTlsCertificateStatusType,
    MetricNameType,
    MetricStatisticType,
    MetricUnitType,
    NameServersUpdateStateCodeType,
    NetworkProtocolType,
    OperationStatusType,
    OperationTypeType,
    OriginProtocolPolicyEnumType,
    PortAccessTypeType,
    PortInfoSourceTypeType,
    PortStateType,
    PricingUnitType,
    R53HostedZoneDeletionStateCodeType,
    RecordStateType,
    RegionNameType,
    RelationalDatabaseMetricNameType,
    RelationalDatabasePasswordVersionType,
    RenewalStatusType,
    ResourceBucketAccessType,
    ResourceTypeType,
    SetupStatusType,
    StatusType,
    StatusTypeType,
    TreatMissingDataType,
    ViewerMinimumTlsProtocolVersionEnumType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccessKeyLastUsedTypeDef",
    "AccessKeyTypeDef",
    "AccessRulesTypeDef",
    "AccountLevelBpaSyncTypeDef",
    "AddOnRequestTypeDef",
    "AddOnTypeDef",
    "AlarmTypeDef",
    "AllocateStaticIpRequestRequestTypeDef",
    "AllocateStaticIpResultTypeDef",
    "AttachCertificateToDistributionRequestRequestTypeDef",
    "AttachCertificateToDistributionResultTypeDef",
    "AttachDiskRequestRequestTypeDef",
    "AttachDiskResultTypeDef",
    "AttachInstancesToLoadBalancerRequestRequestTypeDef",
    "AttachInstancesToLoadBalancerResultTypeDef",
    "AttachLoadBalancerTlsCertificateRequestRequestTypeDef",
    "AttachLoadBalancerTlsCertificateResultTypeDef",
    "AttachStaticIpRequestRequestTypeDef",
    "AttachStaticIpResultTypeDef",
    "AttachedDiskTypeDef",
    "AutoSnapshotAddOnRequestTypeDef",
    "AutoSnapshotDetailsTypeDef",
    "AvailabilityZoneTypeDef",
    "BlueprintTypeDef",
    "BucketAccessLogConfigTypeDef",
    "BucketBundleTypeDef",
    "BucketStateTypeDef",
    "BucketTypeDef",
    "BundleTypeDef",
    "CacheBehaviorPerPathTypeDef",
    "CacheBehaviorTypeDef",
    "CacheSettingsOutputTypeDef",
    "CacheSettingsTypeDef",
    "CertificateSummaryTypeDef",
    "CertificateTypeDef",
    "CloseInstancePublicPortsRequestRequestTypeDef",
    "CloseInstancePublicPortsResultTypeDef",
    "CloudFormationStackRecordSourceInfoTypeDef",
    "CloudFormationStackRecordTypeDef",
    "ContactMethodTypeDef",
    "ContainerImageTypeDef",
    "ContainerOutputTypeDef",
    "ContainerServiceDeploymentRequestTypeDef",
    "ContainerServiceDeploymentTypeDef",
    "ContainerServiceECRImagePullerRoleRequestTypeDef",
    "ContainerServiceECRImagePullerRoleTypeDef",
    "ContainerServiceEndpointTypeDef",
    "ContainerServiceHealthCheckConfigTypeDef",
    "ContainerServiceLogEventTypeDef",
    "ContainerServicePowerTypeDef",
    "ContainerServiceRegistryLoginTypeDef",
    "ContainerServiceStateDetailTypeDef",
    "ContainerServiceTypeDef",
    "ContainerServicesListResultTypeDef",
    "ContainerTypeDef",
    "ContainerUnionTypeDef",
    "CookieObjectOutputTypeDef",
    "CookieObjectTypeDef",
    "CookieObjectUnionTypeDef",
    "CopySnapshotRequestRequestTypeDef",
    "CopySnapshotResultTypeDef",
    "CostEstimateTypeDef",
    "CreateBucketAccessKeyRequestRequestTypeDef",
    "CreateBucketAccessKeyResultTypeDef",
    "CreateBucketRequestRequestTypeDef",
    "CreateBucketResultTypeDef",
    "CreateCertificateRequestRequestTypeDef",
    "CreateCertificateResultTypeDef",
    "CreateCloudFormationStackRequestRequestTypeDef",
    "CreateCloudFormationStackResultTypeDef",
    "CreateContactMethodRequestRequestTypeDef",
    "CreateContactMethodResultTypeDef",
    "CreateContainerServiceDeploymentRequestRequestTypeDef",
    "CreateContainerServiceDeploymentResultTypeDef",
    "CreateContainerServiceRegistryLoginResultTypeDef",
    "CreateContainerServiceRequestRequestTypeDef",
    "CreateContainerServiceResultTypeDef",
    "CreateDiskFromSnapshotRequestRequestTypeDef",
    "CreateDiskFromSnapshotResultTypeDef",
    "CreateDiskRequestRequestTypeDef",
    "CreateDiskResultTypeDef",
    "CreateDiskSnapshotRequestRequestTypeDef",
    "CreateDiskSnapshotResultTypeDef",
    "CreateDistributionRequestRequestTypeDef",
    "CreateDistributionResultTypeDef",
    "CreateDomainEntryRequestRequestTypeDef",
    "CreateDomainEntryResultTypeDef",
    "CreateDomainRequestRequestTypeDef",
    "CreateDomainResultTypeDef",
    "CreateGUISessionAccessDetailsRequestRequestTypeDef",
    "CreateGUISessionAccessDetailsResultTypeDef",
    "CreateInstanceSnapshotRequestRequestTypeDef",
    "CreateInstanceSnapshotResultTypeDef",
    "CreateInstancesFromSnapshotRequestRequestTypeDef",
    "CreateInstancesFromSnapshotResultTypeDef",
    "CreateInstancesRequestRequestTypeDef",
    "CreateInstancesResultTypeDef",
    "CreateKeyPairRequestRequestTypeDef",
    "CreateKeyPairResultTypeDef",
    "CreateLoadBalancerRequestRequestTypeDef",
    "CreateLoadBalancerResultTypeDef",
    "CreateLoadBalancerTlsCertificateRequestRequestTypeDef",
    "CreateLoadBalancerTlsCertificateResultTypeDef",
    "CreateRelationalDatabaseFromSnapshotRequestRequestTypeDef",
    "CreateRelationalDatabaseFromSnapshotResultTypeDef",
    "CreateRelationalDatabaseRequestRequestTypeDef",
    "CreateRelationalDatabaseResultTypeDef",
    "CreateRelationalDatabaseSnapshotRequestRequestTypeDef",
    "CreateRelationalDatabaseSnapshotResultTypeDef",
    "DeleteAlarmRequestRequestTypeDef",
    "DeleteAlarmResultTypeDef",
    "DeleteAutoSnapshotRequestRequestTypeDef",
    "DeleteAutoSnapshotResultTypeDef",
    "DeleteBucketAccessKeyRequestRequestTypeDef",
    "DeleteBucketAccessKeyResultTypeDef",
    "DeleteBucketRequestRequestTypeDef",
    "DeleteBucketResultTypeDef",
    "DeleteCertificateRequestRequestTypeDef",
    "DeleteCertificateResultTypeDef",
    "DeleteContactMethodRequestRequestTypeDef",
    "DeleteContactMethodResultTypeDef",
    "DeleteContainerImageRequestRequestTypeDef",
    "DeleteContainerServiceRequestRequestTypeDef",
    "DeleteDiskRequestRequestTypeDef",
    "DeleteDiskResultTypeDef",
    "DeleteDiskSnapshotRequestRequestTypeDef",
    "DeleteDiskSnapshotResultTypeDef",
    "DeleteDistributionRequestRequestTypeDef",
    "DeleteDistributionResultTypeDef",
    "DeleteDomainEntryRequestRequestTypeDef",
    "DeleteDomainEntryResultTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DeleteDomainResultTypeDef",
    "DeleteInstanceRequestRequestTypeDef",
    "DeleteInstanceResultTypeDef",
    "DeleteInstanceSnapshotRequestRequestTypeDef",
    "DeleteInstanceSnapshotResultTypeDef",
    "DeleteKeyPairRequestRequestTypeDef",
    "DeleteKeyPairResultTypeDef",
    "DeleteKnownHostKeysRequestRequestTypeDef",
    "DeleteKnownHostKeysResultTypeDef",
    "DeleteLoadBalancerRequestRequestTypeDef",
    "DeleteLoadBalancerResultTypeDef",
    "DeleteLoadBalancerTlsCertificateRequestRequestTypeDef",
    "DeleteLoadBalancerTlsCertificateResultTypeDef",
    "DeleteRelationalDatabaseRequestRequestTypeDef",
    "DeleteRelationalDatabaseResultTypeDef",
    "DeleteRelationalDatabaseSnapshotRequestRequestTypeDef",
    "DeleteRelationalDatabaseSnapshotResultTypeDef",
    "DestinationInfoTypeDef",
    "DetachCertificateFromDistributionRequestRequestTypeDef",
    "DetachCertificateFromDistributionResultTypeDef",
    "DetachDiskRequestRequestTypeDef",
    "DetachDiskResultTypeDef",
    "DetachInstancesFromLoadBalancerRequestRequestTypeDef",
    "DetachInstancesFromLoadBalancerResultTypeDef",
    "DetachStaticIpRequestRequestTypeDef",
    "DetachStaticIpResultTypeDef",
    "DisableAddOnRequestRequestTypeDef",
    "DisableAddOnResultTypeDef",
    "DiskInfoTypeDef",
    "DiskMapTypeDef",
    "DiskSnapshotInfoTypeDef",
    "DiskSnapshotTypeDef",
    "DiskTypeDef",
    "DistributionBundleTypeDef",
    "DnsRecordCreationStateTypeDef",
    "DomainEntryOutputTypeDef",
    "DomainEntryTypeDef",
    "DomainTypeDef",
    "DomainValidationRecordTypeDef",
    "DownloadDefaultKeyPairResultTypeDef",
    "EnableAddOnRequestRequestTypeDef",
    "EnableAddOnResultTypeDef",
    "EndpointRequestTypeDef",
    "EstimateByTimeTypeDef",
    "ExportSnapshotRecordSourceInfoTypeDef",
    "ExportSnapshotRecordTypeDef",
    "ExportSnapshotRequestRequestTypeDef",
    "ExportSnapshotResultTypeDef",
    "GetActiveNamesRequestGetActiveNamesPaginateTypeDef",
    "GetActiveNamesRequestRequestTypeDef",
    "GetActiveNamesResultTypeDef",
    "GetAlarmsRequestRequestTypeDef",
    "GetAlarmsResultTypeDef",
    "GetAutoSnapshotsRequestRequestTypeDef",
    "GetAutoSnapshotsResultTypeDef",
    "GetBlueprintsRequestGetBlueprintsPaginateTypeDef",
    "GetBlueprintsRequestRequestTypeDef",
    "GetBlueprintsResultTypeDef",
    "GetBucketAccessKeysRequestRequestTypeDef",
    "GetBucketAccessKeysResultTypeDef",
    "GetBucketBundlesRequestRequestTypeDef",
    "GetBucketBundlesResultTypeDef",
    "GetBucketMetricDataRequestRequestTypeDef",
    "GetBucketMetricDataResultTypeDef",
    "GetBucketsRequestRequestTypeDef",
    "GetBucketsResultTypeDef",
    "GetBundlesRequestGetBundlesPaginateTypeDef",
    "GetBundlesRequestRequestTypeDef",
    "GetBundlesResultTypeDef",
    "GetCertificatesRequestRequestTypeDef",
    "GetCertificatesResultTypeDef",
    "GetCloudFormationStackRecordsRequestGetCloudFormationStackRecordsPaginateTypeDef",
    "GetCloudFormationStackRecordsRequestRequestTypeDef",
    "GetCloudFormationStackRecordsResultTypeDef",
    "GetContactMethodsRequestRequestTypeDef",
    "GetContactMethodsResultTypeDef",
    "GetContainerAPIMetadataResultTypeDef",
    "GetContainerImagesRequestRequestTypeDef",
    "GetContainerImagesResultTypeDef",
    "GetContainerLogRequestRequestTypeDef",
    "GetContainerLogResultTypeDef",
    "GetContainerServiceDeploymentsRequestRequestTypeDef",
    "GetContainerServiceDeploymentsResultTypeDef",
    "GetContainerServiceMetricDataRequestRequestTypeDef",
    "GetContainerServiceMetricDataResultTypeDef",
    "GetContainerServicePowersResultTypeDef",
    "GetContainerServicesRequestRequestTypeDef",
    "GetCostEstimateRequestRequestTypeDef",
    "GetCostEstimateResultTypeDef",
    "GetDiskRequestRequestTypeDef",
    "GetDiskResultTypeDef",
    "GetDiskSnapshotRequestRequestTypeDef",
    "GetDiskSnapshotResultTypeDef",
    "GetDiskSnapshotsRequestGetDiskSnapshotsPaginateTypeDef",
    "GetDiskSnapshotsRequestRequestTypeDef",
    "GetDiskSnapshotsResultTypeDef",
    "GetDisksRequestGetDisksPaginateTypeDef",
    "GetDisksRequestRequestTypeDef",
    "GetDisksResultTypeDef",
    "GetDistributionBundlesResultTypeDef",
    "GetDistributionLatestCacheResetRequestRequestTypeDef",
    "GetDistributionLatestCacheResetResultTypeDef",
    "GetDistributionMetricDataRequestRequestTypeDef",
    "GetDistributionMetricDataResultTypeDef",
    "GetDistributionsRequestRequestTypeDef",
    "GetDistributionsResultTypeDef",
    "GetDomainRequestRequestTypeDef",
    "GetDomainResultTypeDef",
    "GetDomainsRequestGetDomainsPaginateTypeDef",
    "GetDomainsRequestRequestTypeDef",
    "GetDomainsResultTypeDef",
    "GetExportSnapshotRecordsRequestGetExportSnapshotRecordsPaginateTypeDef",
    "GetExportSnapshotRecordsRequestRequestTypeDef",
    "GetExportSnapshotRecordsResultTypeDef",
    "GetInstanceAccessDetailsRequestRequestTypeDef",
    "GetInstanceAccessDetailsResultTypeDef",
    "GetInstanceMetricDataRequestRequestTypeDef",
    "GetInstanceMetricDataResultTypeDef",
    "GetInstancePortStatesRequestRequestTypeDef",
    "GetInstancePortStatesResultTypeDef",
    "GetInstanceRequestRequestTypeDef",
    "GetInstanceResultTypeDef",
    "GetInstanceSnapshotRequestRequestTypeDef",
    "GetInstanceSnapshotResultTypeDef",
    "GetInstanceSnapshotsRequestGetInstanceSnapshotsPaginateTypeDef",
    "GetInstanceSnapshotsRequestRequestTypeDef",
    "GetInstanceSnapshotsResultTypeDef",
    "GetInstanceStateRequestRequestTypeDef",
    "GetInstanceStateResultTypeDef",
    "GetInstancesRequestGetInstancesPaginateTypeDef",
    "GetInstancesRequestRequestTypeDef",
    "GetInstancesResultTypeDef",
    "GetKeyPairRequestRequestTypeDef",
    "GetKeyPairResultTypeDef",
    "GetKeyPairsRequestGetKeyPairsPaginateTypeDef",
    "GetKeyPairsRequestRequestTypeDef",
    "GetKeyPairsResultTypeDef",
    "GetLoadBalancerMetricDataRequestRequestTypeDef",
    "GetLoadBalancerMetricDataResultTypeDef",
    "GetLoadBalancerRequestRequestTypeDef",
    "GetLoadBalancerResultTypeDef",
    "GetLoadBalancerTlsCertificatesRequestRequestTypeDef",
    "GetLoadBalancerTlsCertificatesResultTypeDef",
    "GetLoadBalancerTlsPoliciesRequestRequestTypeDef",
    "GetLoadBalancerTlsPoliciesResultTypeDef",
    "GetLoadBalancersRequestGetLoadBalancersPaginateTypeDef",
    "GetLoadBalancersRequestRequestTypeDef",
    "GetLoadBalancersResultTypeDef",
    "GetOperationRequestRequestTypeDef",
    "GetOperationResultTypeDef",
    "GetOperationsForResourceRequestRequestTypeDef",
    "GetOperationsForResourceResultTypeDef",
    "GetOperationsRequestGetOperationsPaginateTypeDef",
    "GetOperationsRequestRequestTypeDef",
    "GetOperationsResultTypeDef",
    "GetRegionsRequestRequestTypeDef",
    "GetRegionsResultTypeDef",
    "GetRelationalDatabaseBlueprintsRequestGetRelationalDatabaseBlueprintsPaginateTypeDef",
    "GetRelationalDatabaseBlueprintsRequestRequestTypeDef",
    "GetRelationalDatabaseBlueprintsResultTypeDef",
    "GetRelationalDatabaseBundlesRequestGetRelationalDatabaseBundlesPaginateTypeDef",
    "GetRelationalDatabaseBundlesRequestRequestTypeDef",
    "GetRelationalDatabaseBundlesResultTypeDef",
    "GetRelationalDatabaseEventsRequestGetRelationalDatabaseEventsPaginateTypeDef",
    "GetRelationalDatabaseEventsRequestRequestTypeDef",
    "GetRelationalDatabaseEventsResultTypeDef",
    "GetRelationalDatabaseLogEventsRequestRequestTypeDef",
    "GetRelationalDatabaseLogEventsResultTypeDef",
    "GetRelationalDatabaseLogStreamsRequestRequestTypeDef",
    "GetRelationalDatabaseLogStreamsResultTypeDef",
    "GetRelationalDatabaseMasterUserPasswordRequestRequestTypeDef",
    "GetRelationalDatabaseMasterUserPasswordResultTypeDef",
    "GetRelationalDatabaseMetricDataRequestRequestTypeDef",
    "GetRelationalDatabaseMetricDataResultTypeDef",
    "GetRelationalDatabaseParametersRequestGetRelationalDatabaseParametersPaginateTypeDef",
    "GetRelationalDatabaseParametersRequestRequestTypeDef",
    "GetRelationalDatabaseParametersResultTypeDef",
    "GetRelationalDatabaseRequestRequestTypeDef",
    "GetRelationalDatabaseResultTypeDef",
    "GetRelationalDatabaseSnapshotRequestRequestTypeDef",
    "GetRelationalDatabaseSnapshotResultTypeDef",
    "GetRelationalDatabaseSnapshotsRequestGetRelationalDatabaseSnapshotsPaginateTypeDef",
    "GetRelationalDatabaseSnapshotsRequestRequestTypeDef",
    "GetRelationalDatabaseSnapshotsResultTypeDef",
    "GetRelationalDatabasesRequestGetRelationalDatabasesPaginateTypeDef",
    "GetRelationalDatabasesRequestRequestTypeDef",
    "GetRelationalDatabasesResultTypeDef",
    "GetSetupHistoryRequestRequestTypeDef",
    "GetSetupHistoryResultTypeDef",
    "GetStaticIpRequestRequestTypeDef",
    "GetStaticIpResultTypeDef",
    "GetStaticIpsRequestGetStaticIpsPaginateTypeDef",
    "GetStaticIpsRequestRequestTypeDef",
    "GetStaticIpsResultTypeDef",
    "HeaderObjectOutputTypeDef",
    "HeaderObjectTypeDef",
    "HeaderObjectUnionTypeDef",
    "HostKeyAttributesTypeDef",
    "ImportKeyPairRequestRequestTypeDef",
    "ImportKeyPairResultTypeDef",
    "InputOriginTypeDef",
    "InstanceAccessDetailsTypeDef",
    "InstanceEntryTypeDef",
    "InstanceHardwareTypeDef",
    "InstanceHealthSummaryTypeDef",
    "InstanceMetadataOptionsTypeDef",
    "InstanceNetworkingTypeDef",
    "InstancePortInfoTypeDef",
    "InstancePortStateTypeDef",
    "InstanceSnapshotInfoTypeDef",
    "InstanceSnapshotTypeDef",
    "InstanceStateTypeDef",
    "InstanceTypeDef",
    "IsVpcPeeredResultTypeDef",
    "KeyPairTypeDef",
    "LightsailDistributionTypeDef",
    "LoadBalancerTlsCertificateDnsRecordCreationStateTypeDef",
    "LoadBalancerTlsCertificateDomainValidationOptionTypeDef",
    "LoadBalancerTlsCertificateDomainValidationRecordTypeDef",
    "LoadBalancerTlsCertificateRenewalSummaryTypeDef",
    "LoadBalancerTlsCertificateSummaryTypeDef",
    "LoadBalancerTlsCertificateTypeDef",
    "LoadBalancerTlsPolicyTypeDef",
    "LoadBalancerTypeDef",
    "LogEventTypeDef",
    "MetricDatapointTypeDef",
    "MonitoredResourceInfoTypeDef",
    "MonthlyTransferTypeDef",
    "NameServersUpdateStateTypeDef",
    "OpenInstancePublicPortsRequestRequestTypeDef",
    "OpenInstancePublicPortsResultTypeDef",
    "OperationTypeDef",
    "OriginTypeDef",
    "PaginatorConfigTypeDef",
    "PasswordDataTypeDef",
    "PeerVpcResultTypeDef",
    "PendingMaintenanceActionTypeDef",
    "PendingModifiedRelationalDatabaseValuesTypeDef",
    "PortInfoTypeDef",
    "PrivateRegistryAccessRequestTypeDef",
    "PrivateRegistryAccessTypeDef",
    "PutAlarmRequestRequestTypeDef",
    "PutAlarmResultTypeDef",
    "PutInstancePublicPortsRequestRequestTypeDef",
    "PutInstancePublicPortsResultTypeDef",
    "QueryStringObjectOutputTypeDef",
    "QueryStringObjectTypeDef",
    "QueryStringObjectUnionTypeDef",
    "R53HostedZoneDeletionStateTypeDef",
    "RebootInstanceRequestRequestTypeDef",
    "RebootInstanceResultTypeDef",
    "RebootRelationalDatabaseRequestRequestTypeDef",
    "RebootRelationalDatabaseResultTypeDef",
    "RegionTypeDef",
    "RegisterContainerImageRequestRequestTypeDef",
    "RegisterContainerImageResultTypeDef",
    "RegisteredDomainDelegationInfoTypeDef",
    "RelationalDatabaseBlueprintTypeDef",
    "RelationalDatabaseBundleTypeDef",
    "RelationalDatabaseEndpointTypeDef",
    "RelationalDatabaseEventTypeDef",
    "RelationalDatabaseHardwareTypeDef",
    "RelationalDatabaseParameterTypeDef",
    "RelationalDatabaseSnapshotTypeDef",
    "RelationalDatabaseTypeDef",
    "ReleaseStaticIpRequestRequestTypeDef",
    "ReleaseStaticIpResultTypeDef",
    "RenewalSummaryTypeDef",
    "ResetDistributionCacheRequestRequestTypeDef",
    "ResetDistributionCacheResultTypeDef",
    "ResourceBudgetEstimateTypeDef",
    "ResourceLocationTypeDef",
    "ResourceReceivingAccessTypeDef",
    "ResourceRecordTypeDef",
    "ResponseMetadataTypeDef",
    "SendContactMethodVerificationRequestRequestTypeDef",
    "SendContactMethodVerificationResultTypeDef",
    "SessionTypeDef",
    "SetIpAddressTypeRequestRequestTypeDef",
    "SetIpAddressTypeResultTypeDef",
    "SetResourceAccessForBucketRequestRequestTypeDef",
    "SetResourceAccessForBucketResultTypeDef",
    "SetupExecutionDetailsTypeDef",
    "SetupHistoryResourceTypeDef",
    "SetupHistoryTypeDef",
    "SetupInstanceHttpsRequestRequestTypeDef",
    "SetupInstanceHttpsResultTypeDef",
    "SetupRequestTypeDef",
    "StartGUISessionRequestRequestTypeDef",
    "StartGUISessionResultTypeDef",
    "StartInstanceRequestRequestTypeDef",
    "StartInstanceResultTypeDef",
    "StartRelationalDatabaseRequestRequestTypeDef",
    "StartRelationalDatabaseResultTypeDef",
    "StaticIpTypeDef",
    "StopGUISessionRequestRequestTypeDef",
    "StopGUISessionResultTypeDef",
    "StopInstanceOnIdleRequestTypeDef",
    "StopInstanceRequestRequestTypeDef",
    "StopInstanceResultTypeDef",
    "StopRelationalDatabaseRequestRequestTypeDef",
    "StopRelationalDatabaseResultTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagResourceResultTypeDef",
    "TagTypeDef",
    "TestAlarmRequestRequestTypeDef",
    "TestAlarmResultTypeDef",
    "TimePeriodTypeDef",
    "TimestampTypeDef",
    "UnpeerVpcResultTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UntagResourceResultTypeDef",
    "UpdateBucketBundleRequestRequestTypeDef",
    "UpdateBucketBundleResultTypeDef",
    "UpdateBucketRequestRequestTypeDef",
    "UpdateBucketResultTypeDef",
    "UpdateContainerServiceRequestRequestTypeDef",
    "UpdateContainerServiceResultTypeDef",
    "UpdateDistributionBundleRequestRequestTypeDef",
    "UpdateDistributionBundleResultTypeDef",
    "UpdateDistributionRequestRequestTypeDef",
    "UpdateDistributionResultTypeDef",
    "UpdateDomainEntryRequestRequestTypeDef",
    "UpdateDomainEntryResultTypeDef",
    "UpdateInstanceMetadataOptionsRequestRequestTypeDef",
    "UpdateInstanceMetadataOptionsResultTypeDef",
    "UpdateLoadBalancerAttributeRequestRequestTypeDef",
    "UpdateLoadBalancerAttributeResultTypeDef",
    "UpdateRelationalDatabaseParametersRequestRequestTypeDef",
    "UpdateRelationalDatabaseParametersResultTypeDef",
    "UpdateRelationalDatabaseRequestRequestTypeDef",
    "UpdateRelationalDatabaseResultTypeDef",
)


class AccessKeyLastUsedTypeDef(TypedDict):
    lastUsedDate: NotRequired[datetime]
    region: NotRequired[str]
    serviceName: NotRequired[str]


class AccessRulesTypeDef(TypedDict):
    getObject: NotRequired[AccessTypeType]
    allowPublicOverrides: NotRequired[bool]


class AccountLevelBpaSyncTypeDef(TypedDict):
    status: NotRequired[AccountLevelBpaSyncStatusType]
    lastSyncedAt: NotRequired[datetime]
    message: NotRequired[BPAStatusMessageType]
    bpaImpactsLightsail: NotRequired[bool]


class AutoSnapshotAddOnRequestTypeDef(TypedDict):
    snapshotTimeOfDay: NotRequired[str]


class StopInstanceOnIdleRequestTypeDef(TypedDict):
    threshold: NotRequired[str]
    duration: NotRequired[str]


class AddOnTypeDef(TypedDict):
    name: NotRequired[str]
    status: NotRequired[str]
    snapshotTimeOfDay: NotRequired[str]
    nextSnapshotTimeOfDay: NotRequired[str]
    threshold: NotRequired[str]
    duration: NotRequired[str]


class MonitoredResourceInfoTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]


class ResourceLocationTypeDef(TypedDict):
    availabilityZone: NotRequired[str]
    regionName: NotRequired[RegionNameType]


class AllocateStaticIpRequestRequestTypeDef(TypedDict):
    staticIpName: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AttachCertificateToDistributionRequestRequestTypeDef(TypedDict):
    distributionName: str
    certificateName: str


class AttachDiskRequestRequestTypeDef(TypedDict):
    diskName: str
    instanceName: str
    diskPath: str
    autoMounting: NotRequired[bool]


class AttachInstancesToLoadBalancerRequestRequestTypeDef(TypedDict):
    loadBalancerName: str
    instanceNames: Sequence[str]


class AttachLoadBalancerTlsCertificateRequestRequestTypeDef(TypedDict):
    loadBalancerName: str
    certificateName: str


class AttachStaticIpRequestRequestTypeDef(TypedDict):
    staticIpName: str
    instanceName: str


class AttachedDiskTypeDef(TypedDict):
    path: NotRequired[str]
    sizeInGb: NotRequired[int]


class AvailabilityZoneTypeDef(TypedDict):
    zoneName: NotRequired[str]
    state: NotRequired[str]


BlueprintTypeDef = TypedDict(
    "BlueprintTypeDef",
    {
        "blueprintId": NotRequired[str],
        "name": NotRequired[str],
        "group": NotRequired[str],
        "type": NotRequired[BlueprintTypeType],
        "description": NotRequired[str],
        "isActive": NotRequired[bool],
        "minPower": NotRequired[int],
        "version": NotRequired[str],
        "versionCode": NotRequired[str],
        "productUrl": NotRequired[str],
        "licenseUrl": NotRequired[str],
        "platform": NotRequired[InstancePlatformType],
        "appCategory": NotRequired[Literal["LfR"]],
    },
)


class BucketAccessLogConfigTypeDef(TypedDict):
    enabled: bool
    destination: NotRequired[str]
    prefix: NotRequired[str]


class BucketBundleTypeDef(TypedDict):
    bundleId: NotRequired[str]
    name: NotRequired[str]
    price: NotRequired[float]
    storagePerMonthInGb: NotRequired[int]
    transferPerMonthInGb: NotRequired[int]
    isActive: NotRequired[bool]


class BucketStateTypeDef(TypedDict):
    code: NotRequired[str]
    message: NotRequired[str]


class ResourceReceivingAccessTypeDef(TypedDict):
    name: NotRequired[str]
    resourceType: NotRequired[str]


class TagTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]


class BundleTypeDef(TypedDict):
    price: NotRequired[float]
    cpuCount: NotRequired[int]
    diskSizeInGb: NotRequired[int]
    bundleId: NotRequired[str]
    instanceType: NotRequired[str]
    isActive: NotRequired[bool]
    name: NotRequired[str]
    power: NotRequired[int]
    ramSizeInGb: NotRequired[float]
    transferPerMonthInGb: NotRequired[int]
    supportedPlatforms: NotRequired[List[InstancePlatformType]]
    supportedAppCategories: NotRequired[List[Literal["LfR"]]]
    publicIpv4AddressCount: NotRequired[int]


class CacheBehaviorPerPathTypeDef(TypedDict):
    path: NotRequired[str]
    behavior: NotRequired[BehaviorEnumType]


class CacheBehaviorTypeDef(TypedDict):
    behavior: NotRequired[BehaviorEnumType]


class CookieObjectOutputTypeDef(TypedDict):
    option: NotRequired[ForwardValuesType]
    cookiesAllowList: NotRequired[List[str]]


class HeaderObjectOutputTypeDef(TypedDict):
    option: NotRequired[ForwardValuesType]
    headersAllowList: NotRequired[List[HeaderEnumType]]


class QueryStringObjectOutputTypeDef(TypedDict):
    option: NotRequired[bool]
    queryStringsAllowList: NotRequired[List[str]]


class PortInfoTypeDef(TypedDict):
    fromPort: NotRequired[int]
    toPort: NotRequired[int]
    protocol: NotRequired[NetworkProtocolType]
    cidrs: NotRequired[Sequence[str]]
    ipv6Cidrs: NotRequired[Sequence[str]]
    cidrListAliases: NotRequired[Sequence[str]]


class CloudFormationStackRecordSourceInfoTypeDef(TypedDict):
    resourceType: NotRequired[Literal["ExportSnapshotRecord"]]
    name: NotRequired[str]
    arn: NotRequired[str]


DestinationInfoTypeDef = TypedDict(
    "DestinationInfoTypeDef",
    {
        "id": NotRequired[str],
        "service": NotRequired[str],
    },
)


class ContainerImageTypeDef(TypedDict):
    image: NotRequired[str]
    digest: NotRequired[str]
    createdAt: NotRequired[datetime]


class ContainerOutputTypeDef(TypedDict):
    image: NotRequired[str]
    command: NotRequired[List[str]]
    environment: NotRequired[Dict[str, str]]
    ports: NotRequired[Dict[str, ContainerServiceProtocolType]]


class ContainerServiceECRImagePullerRoleRequestTypeDef(TypedDict):
    isActive: NotRequired[bool]


class ContainerServiceECRImagePullerRoleTypeDef(TypedDict):
    isActive: NotRequired[bool]
    principalArn: NotRequired[str]


class ContainerServiceHealthCheckConfigTypeDef(TypedDict):
    healthyThreshold: NotRequired[int]
    unhealthyThreshold: NotRequired[int]
    timeoutSeconds: NotRequired[int]
    intervalSeconds: NotRequired[int]
    path: NotRequired[str]
    successCodes: NotRequired[str]


class ContainerServiceLogEventTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    message: NotRequired[str]


class ContainerServicePowerTypeDef(TypedDict):
    powerId: NotRequired[str]
    price: NotRequired[float]
    cpuCount: NotRequired[float]
    ramSizeInGb: NotRequired[float]
    name: NotRequired[str]
    isActive: NotRequired[bool]


class ContainerServiceRegistryLoginTypeDef(TypedDict):
    username: NotRequired[str]
    password: NotRequired[str]
    expiresAt: NotRequired[datetime]
    registry: NotRequired[str]


class ContainerServiceStateDetailTypeDef(TypedDict):
    code: NotRequired[ContainerServiceStateDetailCodeType]
    message: NotRequired[str]


class ContainerTypeDef(TypedDict):
    image: NotRequired[str]
    command: NotRequired[Sequence[str]]
    environment: NotRequired[Mapping[str, str]]
    ports: NotRequired[Mapping[str, ContainerServiceProtocolType]]


class CookieObjectTypeDef(TypedDict):
    option: NotRequired[ForwardValuesType]
    cookiesAllowList: NotRequired[Sequence[str]]


class CopySnapshotRequestRequestTypeDef(TypedDict):
    targetSnapshotName: str
    sourceRegion: RegionNameType
    sourceSnapshotName: NotRequired[str]
    sourceResourceName: NotRequired[str]
    restoreDate: NotRequired[str]
    useLatestRestorableAutoSnapshot: NotRequired[bool]


class CreateBucketAccessKeyRequestRequestTypeDef(TypedDict):
    bucketName: str


class InstanceEntryTypeDef(TypedDict):
    sourceName: str
    instanceType: str
    portInfoSource: PortInfoSourceTypeType
    availabilityZone: str
    userData: NotRequired[str]


class CreateContactMethodRequestRequestTypeDef(TypedDict):
    protocol: ContactProtocolType
    contactEndpoint: str


class InputOriginTypeDef(TypedDict):
    name: NotRequired[str]
    regionName: NotRequired[RegionNameType]
    protocolPolicy: NotRequired[OriginProtocolPolicyEnumType]
    responseTimeout: NotRequired[int]


DomainEntryTypeDef = TypedDict(
    "DomainEntryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "target": NotRequired[str],
        "isAlias": NotRequired[bool],
        "type": NotRequired[str],
        "options": NotRequired[Mapping[str, str]],
    },
)


class CreateGUISessionAccessDetailsRequestRequestTypeDef(TypedDict):
    resourceName: str


class SessionTypeDef(TypedDict):
    name: NotRequired[str]
    url: NotRequired[str]
    isPrimary: NotRequired[bool]


class DiskMapTypeDef(TypedDict):
    originalDiskPath: NotRequired[str]
    newDiskName: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class DeleteAlarmRequestRequestTypeDef(TypedDict):
    alarmName: str


class DeleteAutoSnapshotRequestRequestTypeDef(TypedDict):
    resourceName: str
    date: str


class DeleteBucketAccessKeyRequestRequestTypeDef(TypedDict):
    bucketName: str
    accessKeyId: str


class DeleteBucketRequestRequestTypeDef(TypedDict):
    bucketName: str
    forceDelete: NotRequired[bool]


class DeleteCertificateRequestRequestTypeDef(TypedDict):
    certificateName: str


class DeleteContactMethodRequestRequestTypeDef(TypedDict):
    protocol: ContactProtocolType


class DeleteContainerImageRequestRequestTypeDef(TypedDict):
    serviceName: str
    image: str


class DeleteContainerServiceRequestRequestTypeDef(TypedDict):
    serviceName: str


class DeleteDiskRequestRequestTypeDef(TypedDict):
    diskName: str
    forceDeleteAddOns: NotRequired[bool]


class DeleteDiskSnapshotRequestRequestTypeDef(TypedDict):
    diskSnapshotName: str


class DeleteDistributionRequestRequestTypeDef(TypedDict):
    distributionName: NotRequired[str]


class DeleteDomainRequestRequestTypeDef(TypedDict):
    domainName: str


class DeleteInstanceRequestRequestTypeDef(TypedDict):
    instanceName: str
    forceDeleteAddOns: NotRequired[bool]


class DeleteInstanceSnapshotRequestRequestTypeDef(TypedDict):
    instanceSnapshotName: str


class DeleteKeyPairRequestRequestTypeDef(TypedDict):
    keyPairName: str
    expectedFingerprint: NotRequired[str]


class DeleteKnownHostKeysRequestRequestTypeDef(TypedDict):
    instanceName: str


class DeleteLoadBalancerRequestRequestTypeDef(TypedDict):
    loadBalancerName: str


class DeleteLoadBalancerTlsCertificateRequestRequestTypeDef(TypedDict):
    loadBalancerName: str
    certificateName: str
    force: NotRequired[bool]


class DeleteRelationalDatabaseRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    skipFinalSnapshot: NotRequired[bool]
    finalRelationalDatabaseSnapshotName: NotRequired[str]


class DeleteRelationalDatabaseSnapshotRequestRequestTypeDef(TypedDict):
    relationalDatabaseSnapshotName: str


class DetachCertificateFromDistributionRequestRequestTypeDef(TypedDict):
    distributionName: str


class DetachDiskRequestRequestTypeDef(TypedDict):
    diskName: str


class DetachInstancesFromLoadBalancerRequestRequestTypeDef(TypedDict):
    loadBalancerName: str
    instanceNames: Sequence[str]


class DetachStaticIpRequestRequestTypeDef(TypedDict):
    staticIpName: str


class DisableAddOnRequestRequestTypeDef(TypedDict):
    addOnType: AddOnTypeType
    resourceName: str


class DiskInfoTypeDef(TypedDict):
    name: NotRequired[str]
    path: NotRequired[str]
    sizeInGb: NotRequired[int]
    isSystemDisk: NotRequired[bool]


class DiskSnapshotInfoTypeDef(TypedDict):
    sizeInGb: NotRequired[int]


class DistributionBundleTypeDef(TypedDict):
    bundleId: NotRequired[str]
    name: NotRequired[str]
    price: NotRequired[float]
    transferPerMonthInGb: NotRequired[int]
    isActive: NotRequired[bool]


class DnsRecordCreationStateTypeDef(TypedDict):
    code: NotRequired[DnsRecordCreationStateCodeType]
    message: NotRequired[str]


DomainEntryOutputTypeDef = TypedDict(
    "DomainEntryOutputTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "target": NotRequired[str],
        "isAlias": NotRequired[bool],
        "type": NotRequired[str],
        "options": NotRequired[Dict[str, str]],
    },
)
ResourceRecordTypeDef = TypedDict(
    "ResourceRecordTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)


class TimePeriodTypeDef(TypedDict):
    start: NotRequired[datetime]
    end: NotRequired[datetime]


class ExportSnapshotRequestRequestTypeDef(TypedDict):
    sourceSnapshotName: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetActiveNamesRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class GetAlarmsRequestRequestTypeDef(TypedDict):
    alarmName: NotRequired[str]
    pageToken: NotRequired[str]
    monitoredResourceName: NotRequired[str]


class GetAutoSnapshotsRequestRequestTypeDef(TypedDict):
    resourceName: str


class GetBlueprintsRequestRequestTypeDef(TypedDict):
    includeInactive: NotRequired[bool]
    pageToken: NotRequired[str]
    appCategory: NotRequired[Literal["LfR"]]


class GetBucketAccessKeysRequestRequestTypeDef(TypedDict):
    bucketName: str


class GetBucketBundlesRequestRequestTypeDef(TypedDict):
    includeInactive: NotRequired[bool]


MetricDatapointTypeDef = TypedDict(
    "MetricDatapointTypeDef",
    {
        "average": NotRequired[float],
        "maximum": NotRequired[float],
        "minimum": NotRequired[float],
        "sampleCount": NotRequired[float],
        "sum": NotRequired[float],
        "timestamp": NotRequired[datetime],
        "unit": NotRequired[MetricUnitType],
    },
)


class GetBucketsRequestRequestTypeDef(TypedDict):
    bucketName: NotRequired[str]
    pageToken: NotRequired[str]
    includeConnectedResources: NotRequired[bool]


class GetBundlesRequestRequestTypeDef(TypedDict):
    includeInactive: NotRequired[bool]
    pageToken: NotRequired[str]
    appCategory: NotRequired[Literal["LfR"]]


class GetCertificatesRequestRequestTypeDef(TypedDict):
    certificateStatuses: NotRequired[Sequence[CertificateStatusType]]
    includeCertificateDetails: NotRequired[bool]
    certificateName: NotRequired[str]
    pageToken: NotRequired[str]


class GetCloudFormationStackRecordsRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class GetContactMethodsRequestRequestTypeDef(TypedDict):
    protocols: NotRequired[Sequence[ContactProtocolType]]


class GetContainerImagesRequestRequestTypeDef(TypedDict):
    serviceName: str


class GetContainerServiceDeploymentsRequestRequestTypeDef(TypedDict):
    serviceName: str


class GetContainerServicesRequestRequestTypeDef(TypedDict):
    serviceName: NotRequired[str]


class GetDiskRequestRequestTypeDef(TypedDict):
    diskName: str


class GetDiskSnapshotRequestRequestTypeDef(TypedDict):
    diskSnapshotName: str


class GetDiskSnapshotsRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class GetDisksRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class GetDistributionLatestCacheResetRequestRequestTypeDef(TypedDict):
    distributionName: NotRequired[str]


class GetDistributionsRequestRequestTypeDef(TypedDict):
    distributionName: NotRequired[str]
    pageToken: NotRequired[str]


class GetDomainRequestRequestTypeDef(TypedDict):
    domainName: str


class GetDomainsRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class GetExportSnapshotRecordsRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class GetInstanceAccessDetailsRequestRequestTypeDef(TypedDict):
    instanceName: str
    protocol: NotRequired[InstanceAccessProtocolType]


class GetInstancePortStatesRequestRequestTypeDef(TypedDict):
    instanceName: str


class InstancePortStateTypeDef(TypedDict):
    fromPort: NotRequired[int]
    toPort: NotRequired[int]
    protocol: NotRequired[NetworkProtocolType]
    state: NotRequired[PortStateType]
    cidrs: NotRequired[List[str]]
    ipv6Cidrs: NotRequired[List[str]]
    cidrListAliases: NotRequired[List[str]]


class GetInstanceRequestRequestTypeDef(TypedDict):
    instanceName: str


class GetInstanceSnapshotRequestRequestTypeDef(TypedDict):
    instanceSnapshotName: str


class GetInstanceSnapshotsRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class GetInstanceStateRequestRequestTypeDef(TypedDict):
    instanceName: str


class InstanceStateTypeDef(TypedDict):
    code: NotRequired[int]
    name: NotRequired[str]


class GetInstancesRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class GetKeyPairRequestRequestTypeDef(TypedDict):
    keyPairName: str


class GetKeyPairsRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]
    includeDefaultKeyPair: NotRequired[bool]


class GetLoadBalancerRequestRequestTypeDef(TypedDict):
    loadBalancerName: str


class GetLoadBalancerTlsCertificatesRequestRequestTypeDef(TypedDict):
    loadBalancerName: str


class GetLoadBalancerTlsPoliciesRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class LoadBalancerTlsPolicyTypeDef(TypedDict):
    name: NotRequired[str]
    isDefault: NotRequired[bool]
    description: NotRequired[str]
    protocols: NotRequired[List[str]]
    ciphers: NotRequired[List[str]]


class GetLoadBalancersRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class GetOperationRequestRequestTypeDef(TypedDict):
    operationId: str


class GetOperationsForResourceRequestRequestTypeDef(TypedDict):
    resourceName: str
    pageToken: NotRequired[str]


class GetOperationsRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class GetRegionsRequestRequestTypeDef(TypedDict):
    includeAvailabilityZones: NotRequired[bool]
    includeRelationalDatabaseAvailabilityZones: NotRequired[bool]


class GetRelationalDatabaseBlueprintsRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class RelationalDatabaseBlueprintTypeDef(TypedDict):
    blueprintId: NotRequired[str]
    engine: NotRequired[Literal["mysql"]]
    engineVersion: NotRequired[str]
    engineDescription: NotRequired[str]
    engineVersionDescription: NotRequired[str]
    isEngineDefault: NotRequired[bool]


class GetRelationalDatabaseBundlesRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]
    includeInactive: NotRequired[bool]


class RelationalDatabaseBundleTypeDef(TypedDict):
    bundleId: NotRequired[str]
    name: NotRequired[str]
    price: NotRequired[float]
    ramSizeInGb: NotRequired[float]
    diskSizeInGb: NotRequired[int]
    transferPerMonthInGb: NotRequired[int]
    cpuCount: NotRequired[int]
    isEncrypted: NotRequired[bool]
    isActive: NotRequired[bool]


class GetRelationalDatabaseEventsRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    durationInMinutes: NotRequired[int]
    pageToken: NotRequired[str]


class RelationalDatabaseEventTypeDef(TypedDict):
    resource: NotRequired[str]
    createdAt: NotRequired[datetime]
    message: NotRequired[str]
    eventCategories: NotRequired[List[str]]


class LogEventTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    message: NotRequired[str]


class GetRelationalDatabaseLogStreamsRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str


class GetRelationalDatabaseMasterUserPasswordRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    passwordVersion: NotRequired[RelationalDatabasePasswordVersionType]


class GetRelationalDatabaseParametersRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    pageToken: NotRequired[str]


class RelationalDatabaseParameterTypeDef(TypedDict):
    allowedValues: NotRequired[str]
    applyMethod: NotRequired[str]
    applyType: NotRequired[str]
    dataType: NotRequired[str]
    description: NotRequired[str]
    isModifiable: NotRequired[bool]
    parameterName: NotRequired[str]
    parameterValue: NotRequired[str]


class GetRelationalDatabaseRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str


class GetRelationalDatabaseSnapshotRequestRequestTypeDef(TypedDict):
    relationalDatabaseSnapshotName: str


class GetRelationalDatabaseSnapshotsRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class GetRelationalDatabasesRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class GetSetupHistoryRequestRequestTypeDef(TypedDict):
    resourceName: str
    pageToken: NotRequired[str]


class GetStaticIpRequestRequestTypeDef(TypedDict):
    staticIpName: str


class GetStaticIpsRequestRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]


class HeaderObjectTypeDef(TypedDict):
    option: NotRequired[ForwardValuesType]
    headersAllowList: NotRequired[Sequence[HeaderEnumType]]


class HostKeyAttributesTypeDef(TypedDict):
    algorithm: NotRequired[str]
    publicKey: NotRequired[str]
    witnessedAt: NotRequired[datetime]
    fingerprintSHA1: NotRequired[str]
    fingerprintSHA256: NotRequired[str]
    notValidBefore: NotRequired[datetime]
    notValidAfter: NotRequired[datetime]


class ImportKeyPairRequestRequestTypeDef(TypedDict):
    keyPairName: str
    publicKeyBase64: str


class PasswordDataTypeDef(TypedDict):
    ciphertext: NotRequired[str]
    keyPairName: NotRequired[str]


class InstanceHealthSummaryTypeDef(TypedDict):
    instanceName: NotRequired[str]
    instanceHealth: NotRequired[InstanceHealthStateType]
    instanceHealthReason: NotRequired[InstanceHealthReasonType]


class InstanceMetadataOptionsTypeDef(TypedDict):
    state: NotRequired[InstanceMetadataStateType]
    httpTokens: NotRequired[HttpTokensType]
    httpEndpoint: NotRequired[HttpEndpointType]
    httpPutResponseHopLimit: NotRequired[int]
    httpProtocolIpv6: NotRequired[HttpProtocolIpv6Type]


class InstancePortInfoTypeDef(TypedDict):
    fromPort: NotRequired[int]
    toPort: NotRequired[int]
    protocol: NotRequired[NetworkProtocolType]
    accessFrom: NotRequired[str]
    accessType: NotRequired[PortAccessTypeType]
    commonName: NotRequired[str]
    accessDirection: NotRequired[AccessDirectionType]
    cidrs: NotRequired[List[str]]
    ipv6Cidrs: NotRequired[List[str]]
    cidrListAliases: NotRequired[List[str]]


class MonthlyTransferTypeDef(TypedDict):
    gbPerMonthAllocated: NotRequired[int]


class OriginTypeDef(TypedDict):
    name: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]
    regionName: NotRequired[RegionNameType]
    protocolPolicy: NotRequired[OriginProtocolPolicyEnumType]
    responseTimeout: NotRequired[int]


class LoadBalancerTlsCertificateDnsRecordCreationStateTypeDef(TypedDict):
    code: NotRequired[LoadBalancerTlsCertificateDnsRecordCreationStateCodeType]
    message: NotRequired[str]


class LoadBalancerTlsCertificateDomainValidationOptionTypeDef(TypedDict):
    domainName: NotRequired[str]
    validationStatus: NotRequired[LoadBalancerTlsCertificateDomainStatusType]


class LoadBalancerTlsCertificateSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    isAttached: NotRequired[bool]


class NameServersUpdateStateTypeDef(TypedDict):
    code: NotRequired[NameServersUpdateStateCodeType]
    message: NotRequired[str]


class PendingMaintenanceActionTypeDef(TypedDict):
    action: NotRequired[str]
    description: NotRequired[str]
    currentApplyDate: NotRequired[datetime]


class PendingModifiedRelationalDatabaseValuesTypeDef(TypedDict):
    masterUserPassword: NotRequired[str]
    engineVersion: NotRequired[str]
    backupRetentionEnabled: NotRequired[bool]


class PutAlarmRequestRequestTypeDef(TypedDict):
    alarmName: str
    metricName: MetricNameType
    monitoredResourceName: str
    comparisonOperator: ComparisonOperatorType
    threshold: float
    evaluationPeriods: int
    datapointsToAlarm: NotRequired[int]
    treatMissingData: NotRequired[TreatMissingDataType]
    contactProtocols: NotRequired[Sequence[ContactProtocolType]]
    notificationTriggers: NotRequired[Sequence[AlarmStateType]]
    notificationEnabled: NotRequired[bool]


class QueryStringObjectTypeDef(TypedDict):
    option: NotRequired[bool]
    queryStringsAllowList: NotRequired[Sequence[str]]


class R53HostedZoneDeletionStateTypeDef(TypedDict):
    code: NotRequired[R53HostedZoneDeletionStateCodeType]
    message: NotRequired[str]


class RebootInstanceRequestRequestTypeDef(TypedDict):
    instanceName: str


class RebootRelationalDatabaseRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str


class RegisterContainerImageRequestRequestTypeDef(TypedDict):
    serviceName: str
    label: str
    digest: str


class RelationalDatabaseEndpointTypeDef(TypedDict):
    port: NotRequired[int]
    address: NotRequired[str]


class RelationalDatabaseHardwareTypeDef(TypedDict):
    cpuCount: NotRequired[int]
    diskSizeInGb: NotRequired[int]
    ramSizeInGb: NotRequired[float]


class ReleaseStaticIpRequestRequestTypeDef(TypedDict):
    staticIpName: str


class ResetDistributionCacheRequestRequestTypeDef(TypedDict):
    distributionName: NotRequired[str]


class SendContactMethodVerificationRequestRequestTypeDef(TypedDict):
    protocol: Literal["Email"]


class SetIpAddressTypeRequestRequestTypeDef(TypedDict):
    resourceType: ResourceTypeType
    resourceName: str
    ipAddressType: IpAddressTypeType
    acceptBundleUpdate: NotRequired[bool]


class SetResourceAccessForBucketRequestRequestTypeDef(TypedDict):
    resourceName: str
    bucketName: str
    access: ResourceBucketAccessType


class SetupExecutionDetailsTypeDef(TypedDict):
    command: NotRequired[str]
    dateTime: NotRequired[datetime]
    name: NotRequired[str]
    status: NotRequired[SetupStatusType]
    standardError: NotRequired[str]
    standardOutput: NotRequired[str]
    version: NotRequired[str]


class SetupRequestTypeDef(TypedDict):
    instanceName: NotRequired[str]
    domainNames: NotRequired[List[str]]
    certificateProvider: NotRequired[Literal["LetsEncrypt"]]


class SetupInstanceHttpsRequestRequestTypeDef(TypedDict):
    instanceName: str
    emailAddress: str
    domainNames: Sequence[str]
    certificateProvider: Literal["LetsEncrypt"]


class StartGUISessionRequestRequestTypeDef(TypedDict):
    resourceName: str


class StartInstanceRequestRequestTypeDef(TypedDict):
    instanceName: str


class StartRelationalDatabaseRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str


class StopGUISessionRequestRequestTypeDef(TypedDict):
    resourceName: str


class StopInstanceRequestRequestTypeDef(TypedDict):
    instanceName: str
    force: NotRequired[bool]


class StopRelationalDatabaseRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    relationalDatabaseSnapshotName: NotRequired[str]


class TestAlarmRequestRequestTypeDef(TypedDict):
    alarmName: str
    state: AlarmStateType


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceName: str
    tagKeys: Sequence[str]
    resourceArn: NotRequired[str]


class UpdateBucketBundleRequestRequestTypeDef(TypedDict):
    bucketName: str
    bundleId: str


class UpdateDistributionBundleRequestRequestTypeDef(TypedDict):
    distributionName: NotRequired[str]
    bundleId: NotRequired[str]


class UpdateInstanceMetadataOptionsRequestRequestTypeDef(TypedDict):
    instanceName: str
    httpTokens: NotRequired[HttpTokensType]
    httpEndpoint: NotRequired[HttpEndpointType]
    httpPutResponseHopLimit: NotRequired[int]
    httpProtocolIpv6: NotRequired[HttpProtocolIpv6Type]


class UpdateLoadBalancerAttributeRequestRequestTypeDef(TypedDict):
    loadBalancerName: str
    attributeName: LoadBalancerAttributeNameType
    attributeValue: str


class UpdateRelationalDatabaseRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    masterUserPassword: NotRequired[str]
    rotateMasterUserPassword: NotRequired[bool]
    preferredBackupWindow: NotRequired[str]
    preferredMaintenanceWindow: NotRequired[str]
    enableBackupRetention: NotRequired[bool]
    disableBackupRetention: NotRequired[bool]
    publiclyAccessible: NotRequired[bool]
    applyImmediately: NotRequired[bool]
    caCertificateIdentifier: NotRequired[str]
    relationalDatabaseBlueprintId: NotRequired[str]


class AccessKeyTypeDef(TypedDict):
    accessKeyId: NotRequired[str]
    secretAccessKey: NotRequired[str]
    status: NotRequired[StatusTypeType]
    createdAt: NotRequired[datetime]
    lastUsed: NotRequired[AccessKeyLastUsedTypeDef]


class AddOnRequestTypeDef(TypedDict):
    addOnType: AddOnTypeType
    autoSnapshotAddOnRequest: NotRequired[AutoSnapshotAddOnRequestTypeDef]
    stopInstanceOnIdleRequest: NotRequired[StopInstanceOnIdleRequestTypeDef]


class AlarmTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    supportCode: NotRequired[str]
    monitoredResourceInfo: NotRequired[MonitoredResourceInfoTypeDef]
    comparisonOperator: NotRequired[ComparisonOperatorType]
    evaluationPeriods: NotRequired[int]
    period: NotRequired[int]
    threshold: NotRequired[float]
    datapointsToAlarm: NotRequired[int]
    treatMissingData: NotRequired[TreatMissingDataType]
    statistic: NotRequired[MetricStatisticType]
    metricName: NotRequired[MetricNameType]
    state: NotRequired[AlarmStateType]
    unit: NotRequired[MetricUnitType]
    contactProtocols: NotRequired[List[ContactProtocolType]]
    notificationTriggers: NotRequired[List[AlarmStateType]]
    notificationEnabled: NotRequired[bool]


class ContactMethodTypeDef(TypedDict):
    contactEndpoint: NotRequired[str]
    status: NotRequired[ContactMethodStatusType]
    protocol: NotRequired[ContactProtocolType]
    name: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    supportCode: NotRequired[str]


OperationTypeDef = TypedDict(
    "OperationTypeDef",
    {
        "id": NotRequired[str],
        "resourceName": NotRequired[str],
        "resourceType": NotRequired[ResourceTypeType],
        "createdAt": NotRequired[datetime],
        "location": NotRequired[ResourceLocationTypeDef],
        "isTerminal": NotRequired[bool],
        "operationDetails": NotRequired[str],
        "operationType": NotRequired[OperationTypeType],
        "status": NotRequired[OperationStatusType],
        "statusChangedAt": NotRequired[datetime],
        "errorCode": NotRequired[str],
        "errorDetails": NotRequired[str],
    },
)


class SetupHistoryResourceTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]


class StaticIpTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    ipAddress: NotRequired[str]
    attachedTo: NotRequired[str]
    isAttached: NotRequired[bool]


class DownloadDefaultKeyPairResultTypeDef(TypedDict):
    publicKeyBase64: str
    privateKeyBase64: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetActiveNamesResultTypeDef(TypedDict):
    activeNames: List[str]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetContainerAPIMetadataResultTypeDef(TypedDict):
    metadata: List[Dict[str, str]]
    ResponseMetadata: ResponseMetadataTypeDef


class GetDistributionLatestCacheResetResultTypeDef(TypedDict):
    status: str
    createTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetRelationalDatabaseLogStreamsResultTypeDef(TypedDict):
    logStreams: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetRelationalDatabaseMasterUserPasswordResultTypeDef(TypedDict):
    masterUserPassword: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class IsVpcPeeredResultTypeDef(TypedDict):
    isPeered: bool
    ResponseMetadata: ResponseMetadataTypeDef


class AutoSnapshotDetailsTypeDef(TypedDict):
    date: NotRequired[str]
    createdAt: NotRequired[datetime]
    status: NotRequired[AutoSnapshotStatusType]
    fromAttachedDisks: NotRequired[List[AttachedDiskTypeDef]]


class RegionTypeDef(TypedDict):
    continentCode: NotRequired[str]
    description: NotRequired[str]
    displayName: NotRequired[str]
    name: NotRequired[RegionNameType]
    availabilityZones: NotRequired[List[AvailabilityZoneTypeDef]]
    relationalDatabaseAvailabilityZones: NotRequired[List[AvailabilityZoneTypeDef]]


class GetBlueprintsResultTypeDef(TypedDict):
    blueprints: List[BlueprintTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBucketRequestRequestTypeDef(TypedDict):
    bucketName: str
    accessRules: NotRequired[AccessRulesTypeDef]
    versioning: NotRequired[str]
    readonlyAccessAccounts: NotRequired[Sequence[str]]
    accessLogConfig: NotRequired[BucketAccessLogConfigTypeDef]


class GetBucketBundlesResultTypeDef(TypedDict):
    bundles: List[BucketBundleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BucketTypeDef(TypedDict):
    resourceType: NotRequired[str]
    accessRules: NotRequired[AccessRulesTypeDef]
    arn: NotRequired[str]
    bundleId: NotRequired[str]
    createdAt: NotRequired[datetime]
    url: NotRequired[str]
    location: NotRequired[ResourceLocationTypeDef]
    name: NotRequired[str]
    supportCode: NotRequired[str]
    tags: NotRequired[List[TagTypeDef]]
    objectVersioning: NotRequired[str]
    ableToUpdateBundle: NotRequired[bool]
    readonlyAccessAccounts: NotRequired[List[str]]
    resourcesReceivingAccess: NotRequired[List[ResourceReceivingAccessTypeDef]]
    state: NotRequired[BucketStateTypeDef]
    accessLogConfig: NotRequired[BucketAccessLogConfigTypeDef]


class CreateBucketRequestRequestTypeDef(TypedDict):
    bucketName: str
    bundleId: str
    tags: NotRequired[Sequence[TagTypeDef]]
    enableObjectVersioning: NotRequired[bool]


class CreateCertificateRequestRequestTypeDef(TypedDict):
    certificateName: str
    domainName: str
    subjectAlternativeNames: NotRequired[Sequence[str]]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateDiskSnapshotRequestRequestTypeDef(TypedDict):
    diskSnapshotName: str
    diskName: NotRequired[str]
    instanceName: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateDomainRequestRequestTypeDef(TypedDict):
    domainName: str
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateInstanceSnapshotRequestRequestTypeDef(TypedDict):
    instanceSnapshotName: str
    instanceName: str
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateKeyPairRequestRequestTypeDef(TypedDict):
    keyPairName: str
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateLoadBalancerRequestRequestTypeDef(TypedDict):
    loadBalancerName: str
    instancePort: int
    healthCheckPath: NotRequired[str]
    certificateName: NotRequired[str]
    certificateDomainName: NotRequired[str]
    certificateAlternativeNames: NotRequired[Sequence[str]]
    tags: NotRequired[Sequence[TagTypeDef]]
    ipAddressType: NotRequired[IpAddressTypeType]
    tlsPolicyName: NotRequired[str]


class CreateLoadBalancerTlsCertificateRequestRequestTypeDef(TypedDict):
    loadBalancerName: str
    certificateName: str
    certificateDomainName: str
    certificateAlternativeNames: NotRequired[Sequence[str]]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateRelationalDatabaseRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    relationalDatabaseBlueprintId: str
    relationalDatabaseBundleId: str
    masterDatabaseName: str
    masterUsername: str
    availabilityZone: NotRequired[str]
    masterUserPassword: NotRequired[str]
    preferredBackupWindow: NotRequired[str]
    preferredMaintenanceWindow: NotRequired[str]
    publiclyAccessible: NotRequired[bool]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateRelationalDatabaseSnapshotRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    relationalDatabaseSnapshotName: str
    tags: NotRequired[Sequence[TagTypeDef]]


class DiskSnapshotTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[List[TagTypeDef]]
    sizeInGb: NotRequired[int]
    state: NotRequired[DiskSnapshotStateType]
    progress: NotRequired[str]
    fromDiskName: NotRequired[str]
    fromDiskArn: NotRequired[str]
    fromInstanceName: NotRequired[str]
    fromInstanceArn: NotRequired[str]
    isFromAutoSnapshot: NotRequired[bool]


class DiskTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[List[TagTypeDef]]
    addOns: NotRequired[List[AddOnTypeDef]]
    sizeInGb: NotRequired[int]
    isSystemDisk: NotRequired[bool]
    iops: NotRequired[int]
    path: NotRequired[str]
    state: NotRequired[DiskStateType]
    attachedTo: NotRequired[str]
    isAttached: NotRequired[bool]
    attachmentState: NotRequired[str]
    gbInUse: NotRequired[int]
    autoMountStatus: NotRequired[AutoMountStatusType]


class KeyPairTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[List[TagTypeDef]]
    fingerprint: NotRequired[str]


class RelationalDatabaseSnapshotTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[List[TagTypeDef]]
    engine: NotRequired[str]
    engineVersion: NotRequired[str]
    sizeInGb: NotRequired[int]
    state: NotRequired[str]
    fromRelationalDatabaseName: NotRequired[str]
    fromRelationalDatabaseArn: NotRequired[str]
    fromRelationalDatabaseBundleId: NotRequired[str]
    fromRelationalDatabaseBlueprintId: NotRequired[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceName: str
    tags: Sequence[TagTypeDef]
    resourceArn: NotRequired[str]


class GetBundlesResultTypeDef(TypedDict):
    bundles: List[BundleTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class CacheSettingsOutputTypeDef(TypedDict):
    defaultTTL: NotRequired[int]
    minimumTTL: NotRequired[int]
    maximumTTL: NotRequired[int]
    allowedHTTPMethods: NotRequired[str]
    cachedHTTPMethods: NotRequired[str]
    forwardedCookies: NotRequired[CookieObjectOutputTypeDef]
    forwardedHeaders: NotRequired[HeaderObjectOutputTypeDef]
    forwardedQueryStrings: NotRequired[QueryStringObjectOutputTypeDef]


class CloseInstancePublicPortsRequestRequestTypeDef(TypedDict):
    portInfo: PortInfoTypeDef
    instanceName: str


class OpenInstancePublicPortsRequestRequestTypeDef(TypedDict):
    portInfo: PortInfoTypeDef
    instanceName: str


class PutInstancePublicPortsRequestRequestTypeDef(TypedDict):
    portInfos: Sequence[PortInfoTypeDef]
    instanceName: str


class CloudFormationStackRecordTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    state: NotRequired[RecordStateType]
    sourceInfo: NotRequired[List[CloudFormationStackRecordSourceInfoTypeDef]]
    destinationInfo: NotRequired[DestinationInfoTypeDef]


class GetContainerImagesResultTypeDef(TypedDict):
    containerImages: List[ContainerImageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterContainerImageResultTypeDef(TypedDict):
    containerImage: ContainerImageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PrivateRegistryAccessRequestTypeDef(TypedDict):
    ecrImagePullerRole: NotRequired[ContainerServiceECRImagePullerRoleRequestTypeDef]


class PrivateRegistryAccessTypeDef(TypedDict):
    ecrImagePullerRole: NotRequired[ContainerServiceECRImagePullerRoleTypeDef]


class ContainerServiceEndpointTypeDef(TypedDict):
    containerName: NotRequired[str]
    containerPort: NotRequired[int]
    healthCheck: NotRequired[ContainerServiceHealthCheckConfigTypeDef]


class EndpointRequestTypeDef(TypedDict):
    containerName: str
    containerPort: int
    healthCheck: NotRequired[ContainerServiceHealthCheckConfigTypeDef]


class GetContainerLogResultTypeDef(TypedDict):
    logEvents: List[ContainerServiceLogEventTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetContainerServicePowersResultTypeDef(TypedDict):
    powers: List[ContainerServicePowerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContainerServiceRegistryLoginResultTypeDef(TypedDict):
    registryLogin: ContainerServiceRegistryLoginTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ContainerUnionTypeDef = Union[ContainerTypeDef, ContainerOutputTypeDef]
CookieObjectUnionTypeDef = Union[CookieObjectTypeDef, CookieObjectOutputTypeDef]


class CreateCloudFormationStackRequestRequestTypeDef(TypedDict):
    instances: Sequence[InstanceEntryTypeDef]


class CreateDomainEntryRequestRequestTypeDef(TypedDict):
    domainName: str
    domainEntry: DomainEntryTypeDef


class DeleteDomainEntryRequestRequestTypeDef(TypedDict):
    domainName: str
    domainEntry: DomainEntryTypeDef


class UpdateDomainEntryRequestRequestTypeDef(TypedDict):
    domainName: str
    domainEntry: DomainEntryTypeDef


class CreateGUISessionAccessDetailsResultTypeDef(TypedDict):
    resourceName: str
    status: StatusType
    percentageComplete: int
    failureReason: str
    sessions: List[SessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRelationalDatabaseFromSnapshotRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    availabilityZone: NotRequired[str]
    publiclyAccessible: NotRequired[bool]
    relationalDatabaseSnapshotName: NotRequired[str]
    relationalDatabaseBundleId: NotRequired[str]
    sourceRelationalDatabaseName: NotRequired[str]
    restoreTime: NotRequired[TimestampTypeDef]
    useLatestRestorableTime: NotRequired[bool]
    tags: NotRequired[Sequence[TagTypeDef]]


class GetBucketMetricDataRequestRequestTypeDef(TypedDict):
    bucketName: str
    metricName: BucketMetricNameType
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    period: int
    statistics: Sequence[MetricStatisticType]
    unit: MetricUnitType


class GetContainerLogRequestRequestTypeDef(TypedDict):
    serviceName: str
    containerName: str
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    filterPattern: NotRequired[str]
    pageToken: NotRequired[str]


class GetContainerServiceMetricDataRequestRequestTypeDef(TypedDict):
    serviceName: str
    metricName: ContainerServiceMetricNameType
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    period: int
    statistics: Sequence[MetricStatisticType]


class GetCostEstimateRequestRequestTypeDef(TypedDict):
    resourceName: str
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef


class GetDistributionMetricDataRequestRequestTypeDef(TypedDict):
    distributionName: str
    metricName: DistributionMetricNameType
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    period: int
    unit: MetricUnitType
    statistics: Sequence[MetricStatisticType]


class GetInstanceMetricDataRequestRequestTypeDef(TypedDict):
    instanceName: str
    metricName: InstanceMetricNameType
    period: int
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    unit: MetricUnitType
    statistics: Sequence[MetricStatisticType]


class GetLoadBalancerMetricDataRequestRequestTypeDef(TypedDict):
    loadBalancerName: str
    metricName: LoadBalancerMetricNameType
    period: int
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    unit: MetricUnitType
    statistics: Sequence[MetricStatisticType]


class GetRelationalDatabaseLogEventsRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    logStreamName: str
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    startFromHead: NotRequired[bool]
    pageToken: NotRequired[str]


class GetRelationalDatabaseMetricDataRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    metricName: RelationalDatabaseMetricNameType
    period: int
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    unit: MetricUnitType
    statistics: Sequence[MetricStatisticType]


class InstanceSnapshotInfoTypeDef(TypedDict):
    fromBundleId: NotRequired[str]
    fromBlueprintId: NotRequired[str]
    fromDiskInfo: NotRequired[List[DiskInfoTypeDef]]


class GetDistributionBundlesResultTypeDef(TypedDict):
    bundles: List[DistributionBundleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DomainValidationRecordTypeDef(TypedDict):
    domainName: NotRequired[str]
    resourceRecord: NotRequired[ResourceRecordTypeDef]
    dnsRecordCreationState: NotRequired[DnsRecordCreationStateTypeDef]
    validationStatus: NotRequired[CertificateDomainValidationStatusType]


class EstimateByTimeTypeDef(TypedDict):
    usageCost: NotRequired[float]
    pricingUnit: NotRequired[PricingUnitType]
    unit: NotRequired[float]
    currency: NotRequired[Literal["USD"]]
    timePeriod: NotRequired[TimePeriodTypeDef]


class GetActiveNamesRequestGetActiveNamesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetBlueprintsRequestGetBlueprintsPaginateTypeDef(TypedDict):
    includeInactive: NotRequired[bool]
    appCategory: NotRequired[Literal["LfR"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetBundlesRequestGetBundlesPaginateTypeDef(TypedDict):
    includeInactive: NotRequired[bool]
    appCategory: NotRequired[Literal["LfR"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetCloudFormationStackRecordsRequestGetCloudFormationStackRecordsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetDiskSnapshotsRequestGetDiskSnapshotsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetDisksRequestGetDisksPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetDomainsRequestGetDomainsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetExportSnapshotRecordsRequestGetExportSnapshotRecordsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetInstanceSnapshotsRequestGetInstanceSnapshotsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetInstancesRequestGetInstancesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetKeyPairsRequestGetKeyPairsPaginateTypeDef(TypedDict):
    includeDefaultKeyPair: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetLoadBalancersRequestGetLoadBalancersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetOperationsRequestGetOperationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetRelationalDatabaseBlueprintsRequestGetRelationalDatabaseBlueprintsPaginateTypeDef(
    TypedDict
):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetRelationalDatabaseBundlesRequestGetRelationalDatabaseBundlesPaginateTypeDef(TypedDict):
    includeInactive: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetRelationalDatabaseEventsRequestGetRelationalDatabaseEventsPaginateTypeDef(TypedDict):
    relationalDatabaseName: str
    durationInMinutes: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetRelationalDatabaseParametersRequestGetRelationalDatabaseParametersPaginateTypeDef(
    TypedDict
):
    relationalDatabaseName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetRelationalDatabaseSnapshotsRequestGetRelationalDatabaseSnapshotsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetRelationalDatabasesRequestGetRelationalDatabasesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetStaticIpsRequestGetStaticIpsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetBucketMetricDataResultTypeDef(TypedDict):
    metricName: BucketMetricNameType
    metricData: List[MetricDatapointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetContainerServiceMetricDataResultTypeDef(TypedDict):
    metricName: ContainerServiceMetricNameType
    metricData: List[MetricDatapointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetDistributionMetricDataResultTypeDef(TypedDict):
    metricName: DistributionMetricNameType
    metricData: List[MetricDatapointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetInstanceMetricDataResultTypeDef(TypedDict):
    metricName: InstanceMetricNameType
    metricData: List[MetricDatapointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetLoadBalancerMetricDataResultTypeDef(TypedDict):
    metricName: LoadBalancerMetricNameType
    metricData: List[MetricDatapointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetRelationalDatabaseMetricDataResultTypeDef(TypedDict):
    metricName: RelationalDatabaseMetricNameType
    metricData: List[MetricDatapointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetInstancePortStatesResultTypeDef(TypedDict):
    portStates: List[InstancePortStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetInstanceStateResultTypeDef(TypedDict):
    state: InstanceStateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetLoadBalancerTlsPoliciesResultTypeDef(TypedDict):
    tlsPolicies: List[LoadBalancerTlsPolicyTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRelationalDatabaseBlueprintsResultTypeDef(TypedDict):
    blueprints: List[RelationalDatabaseBlueprintTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRelationalDatabaseBundlesResultTypeDef(TypedDict):
    bundles: List[RelationalDatabaseBundleTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRelationalDatabaseEventsResultTypeDef(TypedDict):
    relationalDatabaseEvents: List[RelationalDatabaseEventTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRelationalDatabaseLogEventsResultTypeDef(TypedDict):
    resourceLogEvents: List[LogEventTypeDef]
    nextBackwardToken: str
    nextForwardToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRelationalDatabaseParametersResultTypeDef(TypedDict):
    parameters: List[RelationalDatabaseParameterTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRelationalDatabaseParametersRequestRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    parameters: Sequence[RelationalDatabaseParameterTypeDef]


HeaderObjectUnionTypeDef = Union[HeaderObjectTypeDef, HeaderObjectOutputTypeDef]


class InstanceAccessDetailsTypeDef(TypedDict):
    certKey: NotRequired[str]
    expiresAt: NotRequired[datetime]
    ipAddress: NotRequired[str]
    ipv6Addresses: NotRequired[List[str]]
    password: NotRequired[str]
    passwordData: NotRequired[PasswordDataTypeDef]
    privateKey: NotRequired[str]
    protocol: NotRequired[InstanceAccessProtocolType]
    instanceName: NotRequired[str]
    username: NotRequired[str]
    hostKeys: NotRequired[List[HostKeyAttributesTypeDef]]


class InstanceNetworkingTypeDef(TypedDict):
    monthlyTransfer: NotRequired[MonthlyTransferTypeDef]
    ports: NotRequired[List[InstancePortInfoTypeDef]]


LoadBalancerTlsCertificateDomainValidationRecordTypeDef = TypedDict(
    "LoadBalancerTlsCertificateDomainValidationRecordTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
        "validationStatus": NotRequired[LoadBalancerTlsCertificateDomainStatusType],
        "domainName": NotRequired[str],
        "dnsRecordCreationState": NotRequired[
            LoadBalancerTlsCertificateDnsRecordCreationStateTypeDef
        ],
    },
)


class LoadBalancerTlsCertificateRenewalSummaryTypeDef(TypedDict):
    renewalStatus: NotRequired[LoadBalancerTlsCertificateRenewalStatusType]
    domainValidationOptions: NotRequired[
        List[LoadBalancerTlsCertificateDomainValidationOptionTypeDef]
    ]


class LoadBalancerTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[List[TagTypeDef]]
    dnsName: NotRequired[str]
    state: NotRequired[LoadBalancerStateType]
    protocol: NotRequired[LoadBalancerProtocolType]
    publicPorts: NotRequired[List[int]]
    healthCheckPath: NotRequired[str]
    instancePort: NotRequired[int]
    instanceHealthSummary: NotRequired[List[InstanceHealthSummaryTypeDef]]
    tlsCertificateSummaries: NotRequired[List[LoadBalancerTlsCertificateSummaryTypeDef]]
    configurationOptions: NotRequired[Dict[LoadBalancerAttributeNameType, str]]
    ipAddressType: NotRequired[IpAddressTypeType]
    httpsRedirectionEnabled: NotRequired[bool]
    tlsPolicyName: NotRequired[str]


QueryStringObjectUnionTypeDef = Union[QueryStringObjectTypeDef, QueryStringObjectOutputTypeDef]


class RegisteredDomainDelegationInfoTypeDef(TypedDict):
    nameServersUpdateState: NotRequired[NameServersUpdateStateTypeDef]
    r53HostedZoneDeletionState: NotRequired[R53HostedZoneDeletionStateTypeDef]


class RelationalDatabaseTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[List[TagTypeDef]]
    relationalDatabaseBlueprintId: NotRequired[str]
    relationalDatabaseBundleId: NotRequired[str]
    masterDatabaseName: NotRequired[str]
    hardware: NotRequired[RelationalDatabaseHardwareTypeDef]
    state: NotRequired[str]
    secondaryAvailabilityZone: NotRequired[str]
    backupRetentionEnabled: NotRequired[bool]
    pendingModifiedValues: NotRequired[PendingModifiedRelationalDatabaseValuesTypeDef]
    engine: NotRequired[str]
    engineVersion: NotRequired[str]
    latestRestorableTime: NotRequired[datetime]
    masterUsername: NotRequired[str]
    parameterApplyStatus: NotRequired[str]
    preferredBackupWindow: NotRequired[str]
    preferredMaintenanceWindow: NotRequired[str]
    publiclyAccessible: NotRequired[bool]
    masterEndpoint: NotRequired[RelationalDatabaseEndpointTypeDef]
    pendingMaintenanceActions: NotRequired[List[PendingMaintenanceActionTypeDef]]
    caCertificateIdentifier: NotRequired[str]


class GetBucketAccessKeysResultTypeDef(TypedDict):
    accessKeys: List[AccessKeyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDiskFromSnapshotRequestRequestTypeDef(TypedDict):
    diskName: str
    availabilityZone: str
    sizeInGb: int
    diskSnapshotName: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    addOns: NotRequired[Sequence[AddOnRequestTypeDef]]
    sourceDiskName: NotRequired[str]
    restoreDate: NotRequired[str]
    useLatestRestorableAutoSnapshot: NotRequired[bool]


class CreateDiskRequestRequestTypeDef(TypedDict):
    diskName: str
    availabilityZone: str
    sizeInGb: int
    tags: NotRequired[Sequence[TagTypeDef]]
    addOns: NotRequired[Sequence[AddOnRequestTypeDef]]


class CreateInstancesFromSnapshotRequestRequestTypeDef(TypedDict):
    instanceNames: Sequence[str]
    availabilityZone: str
    bundleId: str
    attachedDiskMapping: NotRequired[Mapping[str, Sequence[DiskMapTypeDef]]]
    instanceSnapshotName: NotRequired[str]
    userData: NotRequired[str]
    keyPairName: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    addOns: NotRequired[Sequence[AddOnRequestTypeDef]]
    ipAddressType: NotRequired[IpAddressTypeType]
    sourceInstanceName: NotRequired[str]
    restoreDate: NotRequired[str]
    useLatestRestorableAutoSnapshot: NotRequired[bool]


class CreateInstancesRequestRequestTypeDef(TypedDict):
    instanceNames: Sequence[str]
    availabilityZone: str
    blueprintId: str
    bundleId: str
    customImageName: NotRequired[str]
    userData: NotRequired[str]
    keyPairName: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    addOns: NotRequired[Sequence[AddOnRequestTypeDef]]
    ipAddressType: NotRequired[IpAddressTypeType]


class EnableAddOnRequestRequestTypeDef(TypedDict):
    resourceName: str
    addOnRequest: AddOnRequestTypeDef


class GetAlarmsResultTypeDef(TypedDict):
    alarms: List[AlarmTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetContactMethodsResultTypeDef(TypedDict):
    contactMethods: List[ContactMethodTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AllocateStaticIpResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AttachCertificateToDistributionResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AttachDiskResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AttachInstancesToLoadBalancerResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AttachLoadBalancerTlsCertificateResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AttachStaticIpResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CloseInstancePublicPortsResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CopySnapshotResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBucketAccessKeyResultTypeDef(TypedDict):
    accessKey: AccessKeyTypeDef
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCloudFormationStackResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContactMethodResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDiskFromSnapshotResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDiskResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDiskSnapshotResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDomainEntryResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDomainResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInstanceSnapshotResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInstancesFromSnapshotResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInstancesResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLoadBalancerResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLoadBalancerTlsCertificateResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRelationalDatabaseFromSnapshotResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRelationalDatabaseResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRelationalDatabaseSnapshotResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAlarmResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAutoSnapshotResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBucketAccessKeyResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBucketResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteCertificateResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteContactMethodResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDiskResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDiskSnapshotResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDistributionResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDomainEntryResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDomainResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteInstanceResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteInstanceSnapshotResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteKeyPairResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteKnownHostKeysResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteLoadBalancerResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteLoadBalancerTlsCertificateResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRelationalDatabaseResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRelationalDatabaseSnapshotResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DetachCertificateFromDistributionResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DetachDiskResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DetachInstancesFromLoadBalancerResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DetachStaticIpResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DisableAddOnResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class EnableAddOnResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ExportSnapshotResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetOperationResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetOperationsForResourceResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    nextPageCount: str
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetOperationsResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class ImportKeyPairResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class OpenInstancePublicPortsResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PeerVpcResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutAlarmResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PutInstancePublicPortsResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RebootInstanceResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RebootRelationalDatabaseResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ReleaseStaticIpResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ResetDistributionCacheResultTypeDef(TypedDict):
    status: str
    createTime: datetime
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SendContactMethodVerificationResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class SetIpAddressTypeResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class SetResourceAccessForBucketResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class SetupInstanceHttpsResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StartGUISessionResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StartInstanceResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StartRelationalDatabaseResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StopGUISessionResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StopInstanceResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StopRelationalDatabaseResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TestAlarmResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UnpeerVpcResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UntagResourceResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBucketBundleResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDistributionBundleResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDistributionResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDomainEntryResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateInstanceMetadataOptionsResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateLoadBalancerAttributeResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRelationalDatabaseParametersResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRelationalDatabaseResultTypeDef(TypedDict):
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class SetupHistoryTypeDef(TypedDict):
    operationId: NotRequired[str]
    request: NotRequired[SetupRequestTypeDef]
    resource: NotRequired[SetupHistoryResourceTypeDef]
    executionDetails: NotRequired[List[SetupExecutionDetailsTypeDef]]
    status: NotRequired[SetupStatusType]


class GetStaticIpResultTypeDef(TypedDict):
    staticIp: StaticIpTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetStaticIpsResultTypeDef(TypedDict):
    staticIps: List[StaticIpTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetAutoSnapshotsResultTypeDef(TypedDict):
    resourceName: str
    resourceType: ResourceTypeType
    autoSnapshots: List[AutoSnapshotDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetRegionsResultTypeDef(TypedDict):
    regions: List[RegionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBucketResultTypeDef(TypedDict):
    bucket: BucketTypeDef
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetBucketsResultTypeDef(TypedDict):
    buckets: List[BucketTypeDef]
    nextPageToken: str
    accountLevelBpaSync: AccountLevelBpaSyncTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBucketResultTypeDef(TypedDict):
    bucket: BucketTypeDef
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetDiskSnapshotResultTypeDef(TypedDict):
    diskSnapshot: DiskSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDiskSnapshotsResultTypeDef(TypedDict):
    diskSnapshots: List[DiskSnapshotTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetDiskResultTypeDef(TypedDict):
    disk: DiskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDisksResultTypeDef(TypedDict):
    disks: List[DiskTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class InstanceHardwareTypeDef(TypedDict):
    cpuCount: NotRequired[int]
    disks: NotRequired[List[DiskTypeDef]]
    ramSizeInGb: NotRequired[float]


class InstanceSnapshotTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[List[TagTypeDef]]
    state: NotRequired[InstanceSnapshotStateType]
    progress: NotRequired[str]
    fromAttachedDisks: NotRequired[List[DiskTypeDef]]
    fromInstanceName: NotRequired[str]
    fromInstanceArn: NotRequired[str]
    fromBlueprintId: NotRequired[str]
    fromBundleId: NotRequired[str]
    isFromAutoSnapshot: NotRequired[bool]
    sizeInGb: NotRequired[int]


class CreateKeyPairResultTypeDef(TypedDict):
    keyPair: KeyPairTypeDef
    publicKeyBase64: str
    privateKeyBase64: str
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetKeyPairResultTypeDef(TypedDict):
    keyPair: KeyPairTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetKeyPairsResultTypeDef(TypedDict):
    keyPairs: List[KeyPairTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRelationalDatabaseSnapshotResultTypeDef(TypedDict):
    relationalDatabaseSnapshot: RelationalDatabaseSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetRelationalDatabaseSnapshotsResultTypeDef(TypedDict):
    relationalDatabaseSnapshots: List[RelationalDatabaseSnapshotTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class LightsailDistributionTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    alternativeDomainNames: NotRequired[List[str]]
    status: NotRequired[str]
    isEnabled: NotRequired[bool]
    domainName: NotRequired[str]
    bundleId: NotRequired[str]
    certificateName: NotRequired[str]
    origin: NotRequired[OriginTypeDef]
    originPublicDNS: NotRequired[str]
    defaultCacheBehavior: NotRequired[CacheBehaviorTypeDef]
    cacheBehaviorSettings: NotRequired[CacheSettingsOutputTypeDef]
    cacheBehaviors: NotRequired[List[CacheBehaviorPerPathTypeDef]]
    ableToUpdateBundle: NotRequired[bool]
    ipAddressType: NotRequired[IpAddressTypeType]
    tags: NotRequired[List[TagTypeDef]]
    viewerMinimumTlsProtocolVersion: NotRequired[str]


class GetCloudFormationStackRecordsResultTypeDef(TypedDict):
    cloudFormationStackRecords: List[CloudFormationStackRecordTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateContainerServiceRequestRequestTypeDef(TypedDict):
    serviceName: str
    power: NotRequired[ContainerServicePowerNameType]
    scale: NotRequired[int]
    isDisabled: NotRequired[bool]
    publicDomainNames: NotRequired[Mapping[str, Sequence[str]]]
    privateRegistryAccess: NotRequired[PrivateRegistryAccessRequestTypeDef]


class ContainerServiceDeploymentTypeDef(TypedDict):
    version: NotRequired[int]
    state: NotRequired[ContainerServiceDeploymentStateType]
    containers: NotRequired[Dict[str, ContainerOutputTypeDef]]
    publicEndpoint: NotRequired[ContainerServiceEndpointTypeDef]
    createdAt: NotRequired[datetime]


class ContainerServiceDeploymentRequestTypeDef(TypedDict):
    containers: NotRequired[Mapping[str, ContainerUnionTypeDef]]
    publicEndpoint: NotRequired[EndpointRequestTypeDef]


class CreateContainerServiceDeploymentRequestRequestTypeDef(TypedDict):
    serviceName: str
    containers: NotRequired[Mapping[str, ContainerUnionTypeDef]]
    publicEndpoint: NotRequired[EndpointRequestTypeDef]


class ExportSnapshotRecordSourceInfoTypeDef(TypedDict):
    resourceType: NotRequired[ExportSnapshotRecordSourceTypeType]
    createdAt: NotRequired[datetime]
    name: NotRequired[str]
    arn: NotRequired[str]
    fromResourceName: NotRequired[str]
    fromResourceArn: NotRequired[str]
    instanceSnapshotInfo: NotRequired[InstanceSnapshotInfoTypeDef]
    diskSnapshotInfo: NotRequired[DiskSnapshotInfoTypeDef]


class RenewalSummaryTypeDef(TypedDict):
    domainValidationRecords: NotRequired[List[DomainValidationRecordTypeDef]]
    renewalStatus: NotRequired[RenewalStatusType]
    renewalStatusReason: NotRequired[str]
    updatedAt: NotRequired[datetime]


class CostEstimateTypeDef(TypedDict):
    usageType: NotRequired[str]
    resultsByTime: NotRequired[List[EstimateByTimeTypeDef]]


class GetInstanceAccessDetailsResultTypeDef(TypedDict):
    accessDetails: InstanceAccessDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class LoadBalancerTlsCertificateTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[List[TagTypeDef]]
    loadBalancerName: NotRequired[str]
    isAttached: NotRequired[bool]
    status: NotRequired[LoadBalancerTlsCertificateStatusType]
    domainName: NotRequired[str]
    domainValidationRecords: NotRequired[
        List[LoadBalancerTlsCertificateDomainValidationRecordTypeDef]
    ]
    failureReason: NotRequired[LoadBalancerTlsCertificateFailureReasonType]
    issuedAt: NotRequired[datetime]
    issuer: NotRequired[str]
    keyAlgorithm: NotRequired[str]
    notAfter: NotRequired[datetime]
    notBefore: NotRequired[datetime]
    renewalSummary: NotRequired[LoadBalancerTlsCertificateRenewalSummaryTypeDef]
    revocationReason: NotRequired[LoadBalancerTlsCertificateRevocationReasonType]
    revokedAt: NotRequired[datetime]
    serial: NotRequired[str]
    signatureAlgorithm: NotRequired[str]
    subject: NotRequired[str]
    subjectAlternativeNames: NotRequired[List[str]]


class GetLoadBalancerResultTypeDef(TypedDict):
    loadBalancer: LoadBalancerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetLoadBalancersResultTypeDef(TypedDict):
    loadBalancers: List[LoadBalancerTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class CacheSettingsTypeDef(TypedDict):
    defaultTTL: NotRequired[int]
    minimumTTL: NotRequired[int]
    maximumTTL: NotRequired[int]
    allowedHTTPMethods: NotRequired[str]
    cachedHTTPMethods: NotRequired[str]
    forwardedCookies: NotRequired[CookieObjectUnionTypeDef]
    forwardedHeaders: NotRequired[HeaderObjectUnionTypeDef]
    forwardedQueryStrings: NotRequired[QueryStringObjectUnionTypeDef]


class DomainTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[List[TagTypeDef]]
    domainEntries: NotRequired[List[DomainEntryOutputTypeDef]]
    registeredDomainDelegationInfo: NotRequired[RegisteredDomainDelegationInfoTypeDef]


class GetRelationalDatabaseResultTypeDef(TypedDict):
    relationalDatabase: RelationalDatabaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetRelationalDatabasesResultTypeDef(TypedDict):
    relationalDatabases: List[RelationalDatabaseTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSetupHistoryResultTypeDef(TypedDict):
    setupHistory: List[SetupHistoryTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class InstanceTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[List[TagTypeDef]]
    blueprintId: NotRequired[str]
    blueprintName: NotRequired[str]
    bundleId: NotRequired[str]
    addOns: NotRequired[List[AddOnTypeDef]]
    isStaticIp: NotRequired[bool]
    privateIpAddress: NotRequired[str]
    publicIpAddress: NotRequired[str]
    ipv6Addresses: NotRequired[List[str]]
    ipAddressType: NotRequired[IpAddressTypeType]
    hardware: NotRequired[InstanceHardwareTypeDef]
    networking: NotRequired[InstanceNetworkingTypeDef]
    state: NotRequired[InstanceStateTypeDef]
    username: NotRequired[str]
    sshKeyName: NotRequired[str]
    metadataOptions: NotRequired[InstanceMetadataOptionsTypeDef]


class GetInstanceSnapshotResultTypeDef(TypedDict):
    instanceSnapshot: InstanceSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetInstanceSnapshotsResultTypeDef(TypedDict):
    instanceSnapshots: List[InstanceSnapshotTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDistributionResultTypeDef(TypedDict):
    distribution: LightsailDistributionTypeDef
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDistributionsResultTypeDef(TypedDict):
    distributions: List[LightsailDistributionTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class ContainerServiceTypeDef(TypedDict):
    containerServiceName: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[List[TagTypeDef]]
    power: NotRequired[ContainerServicePowerNameType]
    powerId: NotRequired[str]
    state: NotRequired[ContainerServiceStateType]
    stateDetail: NotRequired[ContainerServiceStateDetailTypeDef]
    scale: NotRequired[int]
    currentDeployment: NotRequired[ContainerServiceDeploymentTypeDef]
    nextDeployment: NotRequired[ContainerServiceDeploymentTypeDef]
    isDisabled: NotRequired[bool]
    principalArn: NotRequired[str]
    privateDomainName: NotRequired[str]
    publicDomainNames: NotRequired[Dict[str, List[str]]]
    url: NotRequired[str]
    privateRegistryAccess: NotRequired[PrivateRegistryAccessTypeDef]


class GetContainerServiceDeploymentsResultTypeDef(TypedDict):
    deployments: List[ContainerServiceDeploymentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContainerServiceRequestRequestTypeDef(TypedDict):
    serviceName: str
    power: ContainerServicePowerNameType
    scale: int
    tags: NotRequired[Sequence[TagTypeDef]]
    publicDomainNames: NotRequired[Mapping[str, Sequence[str]]]
    deployment: NotRequired[ContainerServiceDeploymentRequestTypeDef]
    privateRegistryAccess: NotRequired[PrivateRegistryAccessRequestTypeDef]


class ExportSnapshotRecordTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    state: NotRequired[RecordStateType]
    sourceInfo: NotRequired[ExportSnapshotRecordSourceInfoTypeDef]
    destinationInfo: NotRequired[DestinationInfoTypeDef]


class CertificateTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    domainName: NotRequired[str]
    status: NotRequired[CertificateStatusType]
    serialNumber: NotRequired[str]
    subjectAlternativeNames: NotRequired[List[str]]
    domainValidationRecords: NotRequired[List[DomainValidationRecordTypeDef]]
    requestFailureReason: NotRequired[str]
    inUseResourceCount: NotRequired[int]
    keyAlgorithm: NotRequired[str]
    createdAt: NotRequired[datetime]
    issuedAt: NotRequired[datetime]
    issuerCA: NotRequired[str]
    notBefore: NotRequired[datetime]
    notAfter: NotRequired[datetime]
    eligibleToRenew: NotRequired[str]
    renewalSummary: NotRequired[RenewalSummaryTypeDef]
    revokedAt: NotRequired[datetime]
    revocationReason: NotRequired[str]
    tags: NotRequired[List[TagTypeDef]]
    supportCode: NotRequired[str]


class ResourceBudgetEstimateTypeDef(TypedDict):
    resourceName: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]
    costEstimates: NotRequired[List[CostEstimateTypeDef]]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]


class GetLoadBalancerTlsCertificatesResultTypeDef(TypedDict):
    tlsCertificates: List[LoadBalancerTlsCertificateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDistributionRequestRequestTypeDef(TypedDict):
    distributionName: str
    origin: InputOriginTypeDef
    defaultCacheBehavior: CacheBehaviorTypeDef
    bundleId: str
    cacheBehaviorSettings: NotRequired[CacheSettingsTypeDef]
    cacheBehaviors: NotRequired[Sequence[CacheBehaviorPerPathTypeDef]]
    ipAddressType: NotRequired[IpAddressTypeType]
    tags: NotRequired[Sequence[TagTypeDef]]
    certificateName: NotRequired[str]
    viewerMinimumTlsProtocolVersion: NotRequired[ViewerMinimumTlsProtocolVersionEnumType]


class UpdateDistributionRequestRequestTypeDef(TypedDict):
    distributionName: str
    origin: NotRequired[InputOriginTypeDef]
    defaultCacheBehavior: NotRequired[CacheBehaviorTypeDef]
    cacheBehaviorSettings: NotRequired[CacheSettingsTypeDef]
    cacheBehaviors: NotRequired[Sequence[CacheBehaviorPerPathTypeDef]]
    isEnabled: NotRequired[bool]
    viewerMinimumTlsProtocolVersion: NotRequired[ViewerMinimumTlsProtocolVersionEnumType]
    certificateName: NotRequired[str]
    useDefaultCertificate: NotRequired[bool]


class GetDomainResultTypeDef(TypedDict):
    domain: DomainTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDomainsResultTypeDef(TypedDict):
    domains: List[DomainTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetInstanceResultTypeDef(TypedDict):
    instance: InstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetInstancesResultTypeDef(TypedDict):
    instances: List[InstanceTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class ContainerServicesListResultTypeDef(TypedDict):
    containerServices: List[ContainerServiceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContainerServiceDeploymentResultTypeDef(TypedDict):
    containerService: ContainerServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContainerServiceResultTypeDef(TypedDict):
    containerService: ContainerServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateContainerServiceResultTypeDef(TypedDict):
    containerService: ContainerServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetExportSnapshotRecordsResultTypeDef(TypedDict):
    exportSnapshotRecords: List[ExportSnapshotRecordTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class CertificateSummaryTypeDef(TypedDict):
    certificateArn: NotRequired[str]
    certificateName: NotRequired[str]
    domainName: NotRequired[str]
    certificateDetail: NotRequired[CertificateTypeDef]
    tags: NotRequired[List[TagTypeDef]]


class GetCostEstimateResultTypeDef(TypedDict):
    resourcesBudgetEstimate: List[ResourceBudgetEstimateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCertificateResultTypeDef(TypedDict):
    certificate: CertificateSummaryTypeDef
    operations: List[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetCertificatesResultTypeDef(TypedDict):
    certificates: List[CertificateSummaryTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef
