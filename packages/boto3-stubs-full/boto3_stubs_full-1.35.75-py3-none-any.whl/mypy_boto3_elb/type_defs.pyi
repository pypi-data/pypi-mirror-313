"""
Type annotations for elb service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/type_defs/)

Usage::

    ```python
    from mypy_boto3_elb.type_defs import AccessLogTypeDef

    data: AccessLogTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AccessLogTypeDef",
    "AddAvailabilityZonesInputRequestTypeDef",
    "AddAvailabilityZonesOutputTypeDef",
    "AddTagsInputRequestTypeDef",
    "AdditionalAttributeTypeDef",
    "AppCookieStickinessPolicyTypeDef",
    "ApplySecurityGroupsToLoadBalancerInputRequestTypeDef",
    "ApplySecurityGroupsToLoadBalancerOutputTypeDef",
    "AttachLoadBalancerToSubnetsInputRequestTypeDef",
    "AttachLoadBalancerToSubnetsOutputTypeDef",
    "BackendServerDescriptionTypeDef",
    "ConfigureHealthCheckInputRequestTypeDef",
    "ConfigureHealthCheckOutputTypeDef",
    "ConnectionDrainingTypeDef",
    "ConnectionSettingsTypeDef",
    "CreateAccessPointInputRequestTypeDef",
    "CreateAccessPointOutputTypeDef",
    "CreateAppCookieStickinessPolicyInputRequestTypeDef",
    "CreateLBCookieStickinessPolicyInputRequestTypeDef",
    "CreateLoadBalancerListenerInputRequestTypeDef",
    "CreateLoadBalancerPolicyInputRequestTypeDef",
    "CrossZoneLoadBalancingTypeDef",
    "DeleteAccessPointInputRequestTypeDef",
    "DeleteLoadBalancerListenerInputRequestTypeDef",
    "DeleteLoadBalancerPolicyInputRequestTypeDef",
    "DeregisterEndPointsInputRequestTypeDef",
    "DeregisterEndPointsOutputTypeDef",
    "DescribeAccessPointsInputDescribeLoadBalancersPaginateTypeDef",
    "DescribeAccessPointsInputRequestTypeDef",
    "DescribeAccessPointsOutputTypeDef",
    "DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef",
    "DescribeAccountLimitsInputRequestTypeDef",
    "DescribeAccountLimitsOutputTypeDef",
    "DescribeEndPointStateInputAnyInstanceInServiceWaitTypeDef",
    "DescribeEndPointStateInputInstanceDeregisteredWaitTypeDef",
    "DescribeEndPointStateInputInstanceInServiceWaitTypeDef",
    "DescribeEndPointStateInputRequestTypeDef",
    "DescribeEndPointStateOutputTypeDef",
    "DescribeLoadBalancerAttributesInputRequestTypeDef",
    "DescribeLoadBalancerAttributesOutputTypeDef",
    "DescribeLoadBalancerPoliciesInputRequestTypeDef",
    "DescribeLoadBalancerPoliciesOutputTypeDef",
    "DescribeLoadBalancerPolicyTypesInputRequestTypeDef",
    "DescribeLoadBalancerPolicyTypesOutputTypeDef",
    "DescribeTagsInputRequestTypeDef",
    "DescribeTagsOutputTypeDef",
    "DetachLoadBalancerFromSubnetsInputRequestTypeDef",
    "DetachLoadBalancerFromSubnetsOutputTypeDef",
    "HealthCheckTypeDef",
    "InstanceStateTypeDef",
    "InstanceTypeDef",
    "LBCookieStickinessPolicyTypeDef",
    "LimitTypeDef",
    "ListenerDescriptionTypeDef",
    "ListenerTypeDef",
    "LoadBalancerAttributesOutputTypeDef",
    "LoadBalancerAttributesTypeDef",
    "LoadBalancerDescriptionTypeDef",
    "ModifyLoadBalancerAttributesInputRequestTypeDef",
    "ModifyLoadBalancerAttributesOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PoliciesTypeDef",
    "PolicyAttributeDescriptionTypeDef",
    "PolicyAttributeTypeDef",
    "PolicyAttributeTypeDescriptionTypeDef",
    "PolicyDescriptionTypeDef",
    "PolicyTypeDescriptionTypeDef",
    "RegisterEndPointsInputRequestTypeDef",
    "RegisterEndPointsOutputTypeDef",
    "RemoveAvailabilityZonesInputRequestTypeDef",
    "RemoveAvailabilityZonesOutputTypeDef",
    "RemoveTagsInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "SetLoadBalancerListenerSSLCertificateInputRequestTypeDef",
    "SetLoadBalancerPoliciesForBackendServerInputRequestTypeDef",
    "SetLoadBalancerPoliciesOfListenerInputRequestTypeDef",
    "SourceSecurityGroupTypeDef",
    "TagDescriptionTypeDef",
    "TagKeyOnlyTypeDef",
    "TagTypeDef",
    "WaiterConfigTypeDef",
)

class AccessLogTypeDef(TypedDict):
    Enabled: bool
    S3BucketName: NotRequired[str]
    EmitInterval: NotRequired[int]
    S3BucketPrefix: NotRequired[str]

class AddAvailabilityZonesInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    AvailabilityZones: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]

class AdditionalAttributeTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

class AppCookieStickinessPolicyTypeDef(TypedDict):
    PolicyName: NotRequired[str]
    CookieName: NotRequired[str]

class ApplySecurityGroupsToLoadBalancerInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    SecurityGroups: Sequence[str]

class AttachLoadBalancerToSubnetsInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    Subnets: Sequence[str]

class BackendServerDescriptionTypeDef(TypedDict):
    InstancePort: NotRequired[int]
    PolicyNames: NotRequired[List[str]]

class HealthCheckTypeDef(TypedDict):
    Target: str
    Interval: int
    Timeout: int
    UnhealthyThreshold: int
    HealthyThreshold: int

class ConnectionDrainingTypeDef(TypedDict):
    Enabled: bool
    Timeout: NotRequired[int]

class ConnectionSettingsTypeDef(TypedDict):
    IdleTimeout: int

ListenerTypeDef = TypedDict(
    "ListenerTypeDef",
    {
        "Protocol": str,
        "LoadBalancerPort": int,
        "InstancePort": int,
        "InstanceProtocol": NotRequired[str],
        "SSLCertificateId": NotRequired[str],
    },
)

class CreateAppCookieStickinessPolicyInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    PolicyName: str
    CookieName: str

class CreateLBCookieStickinessPolicyInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    PolicyName: str
    CookieExpirationPeriod: NotRequired[int]

class PolicyAttributeTypeDef(TypedDict):
    AttributeName: NotRequired[str]
    AttributeValue: NotRequired[str]

class CrossZoneLoadBalancingTypeDef(TypedDict):
    Enabled: bool

class DeleteAccessPointInputRequestTypeDef(TypedDict):
    LoadBalancerName: str

class DeleteLoadBalancerListenerInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    LoadBalancerPorts: Sequence[int]

class DeleteLoadBalancerPolicyInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    PolicyName: str

class InstanceTypeDef(TypedDict):
    InstanceId: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeAccessPointsInputRequestTypeDef(TypedDict):
    LoadBalancerNames: NotRequired[Sequence[str]]
    Marker: NotRequired[str]
    PageSize: NotRequired[int]

class DescribeAccountLimitsInputRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    PageSize: NotRequired[int]

class LimitTypeDef(TypedDict):
    Name: NotRequired[str]
    Max: NotRequired[str]

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class InstanceStateTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    State: NotRequired[str]
    ReasonCode: NotRequired[str]
    Description: NotRequired[str]

class DescribeLoadBalancerAttributesInputRequestTypeDef(TypedDict):
    LoadBalancerName: str

class DescribeLoadBalancerPoliciesInputRequestTypeDef(TypedDict):
    LoadBalancerName: NotRequired[str]
    PolicyNames: NotRequired[Sequence[str]]

class DescribeLoadBalancerPolicyTypesInputRequestTypeDef(TypedDict):
    PolicyTypeNames: NotRequired[Sequence[str]]

class DescribeTagsInputRequestTypeDef(TypedDict):
    LoadBalancerNames: Sequence[str]

class DetachLoadBalancerFromSubnetsInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    Subnets: Sequence[str]

class LBCookieStickinessPolicyTypeDef(TypedDict):
    PolicyName: NotRequired[str]
    CookieExpirationPeriod: NotRequired[int]

class SourceSecurityGroupTypeDef(TypedDict):
    OwnerAlias: NotRequired[str]
    GroupName: NotRequired[str]

class PolicyAttributeDescriptionTypeDef(TypedDict):
    AttributeName: NotRequired[str]
    AttributeValue: NotRequired[str]

class PolicyAttributeTypeDescriptionTypeDef(TypedDict):
    AttributeName: NotRequired[str]
    AttributeType: NotRequired[str]
    Description: NotRequired[str]
    DefaultValue: NotRequired[str]
    Cardinality: NotRequired[str]

class RemoveAvailabilityZonesInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    AvailabilityZones: Sequence[str]

class TagKeyOnlyTypeDef(TypedDict):
    Key: NotRequired[str]

class SetLoadBalancerListenerSSLCertificateInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    LoadBalancerPort: int
    SSLCertificateId: str

class SetLoadBalancerPoliciesForBackendServerInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    InstancePort: int
    PolicyNames: Sequence[str]

class SetLoadBalancerPoliciesOfListenerInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    LoadBalancerPort: int
    PolicyNames: Sequence[str]

class AddAvailabilityZonesOutputTypeDef(TypedDict):
    AvailabilityZones: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class ApplySecurityGroupsToLoadBalancerOutputTypeDef(TypedDict):
    SecurityGroups: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class AttachLoadBalancerToSubnetsOutputTypeDef(TypedDict):
    Subnets: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAccessPointOutputTypeDef(TypedDict):
    DNSName: str
    ResponseMetadata: ResponseMetadataTypeDef

class DetachLoadBalancerFromSubnetsOutputTypeDef(TypedDict):
    Subnets: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class RemoveAvailabilityZonesOutputTypeDef(TypedDict):
    AvailabilityZones: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class AddTagsInputRequestTypeDef(TypedDict):
    LoadBalancerNames: Sequence[str]
    Tags: Sequence[TagTypeDef]

class TagDescriptionTypeDef(TypedDict):
    LoadBalancerName: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]

class ConfigureHealthCheckInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    HealthCheck: HealthCheckTypeDef

class ConfigureHealthCheckOutputTypeDef(TypedDict):
    HealthCheck: HealthCheckTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAccessPointInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    Listeners: Sequence[ListenerTypeDef]
    AvailabilityZones: NotRequired[Sequence[str]]
    Subnets: NotRequired[Sequence[str]]
    SecurityGroups: NotRequired[Sequence[str]]
    Scheme: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateLoadBalancerListenerInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    Listeners: Sequence[ListenerTypeDef]

class ListenerDescriptionTypeDef(TypedDict):
    Listener: NotRequired[ListenerTypeDef]
    PolicyNames: NotRequired[List[str]]

class CreateLoadBalancerPolicyInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    PolicyName: str
    PolicyTypeName: str
    PolicyAttributes: NotRequired[Sequence[PolicyAttributeTypeDef]]

class LoadBalancerAttributesOutputTypeDef(TypedDict):
    CrossZoneLoadBalancing: NotRequired[CrossZoneLoadBalancingTypeDef]
    AccessLog: NotRequired[AccessLogTypeDef]
    ConnectionDraining: NotRequired[ConnectionDrainingTypeDef]
    ConnectionSettings: NotRequired[ConnectionSettingsTypeDef]
    AdditionalAttributes: NotRequired[List[AdditionalAttributeTypeDef]]

class LoadBalancerAttributesTypeDef(TypedDict):
    CrossZoneLoadBalancing: NotRequired[CrossZoneLoadBalancingTypeDef]
    AccessLog: NotRequired[AccessLogTypeDef]
    ConnectionDraining: NotRequired[ConnectionDrainingTypeDef]
    ConnectionSettings: NotRequired[ConnectionSettingsTypeDef]
    AdditionalAttributes: NotRequired[Sequence[AdditionalAttributeTypeDef]]

class DeregisterEndPointsInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    Instances: Sequence[InstanceTypeDef]

class DeregisterEndPointsOutputTypeDef(TypedDict):
    Instances: List[InstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeEndPointStateInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    Instances: NotRequired[Sequence[InstanceTypeDef]]

class RegisterEndPointsInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    Instances: Sequence[InstanceTypeDef]

class RegisterEndPointsOutputTypeDef(TypedDict):
    Instances: List[InstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAccessPointsInputDescribeLoadBalancersPaginateTypeDef(TypedDict):
    LoadBalancerNames: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeAccountLimitsOutputTypeDef(TypedDict):
    Limits: List[LimitTypeDef]
    NextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeEndPointStateInputAnyInstanceInServiceWaitTypeDef(TypedDict):
    LoadBalancerName: str
    Instances: NotRequired[Sequence[InstanceTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeEndPointStateInputInstanceDeregisteredWaitTypeDef(TypedDict):
    LoadBalancerName: str
    Instances: NotRequired[Sequence[InstanceTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeEndPointStateInputInstanceInServiceWaitTypeDef(TypedDict):
    LoadBalancerName: str
    Instances: NotRequired[Sequence[InstanceTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeEndPointStateOutputTypeDef(TypedDict):
    InstanceStates: List[InstanceStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PoliciesTypeDef(TypedDict):
    AppCookieStickinessPolicies: NotRequired[List[AppCookieStickinessPolicyTypeDef]]
    LBCookieStickinessPolicies: NotRequired[List[LBCookieStickinessPolicyTypeDef]]
    OtherPolicies: NotRequired[List[str]]

class PolicyDescriptionTypeDef(TypedDict):
    PolicyName: NotRequired[str]
    PolicyTypeName: NotRequired[str]
    PolicyAttributeDescriptions: NotRequired[List[PolicyAttributeDescriptionTypeDef]]

class PolicyTypeDescriptionTypeDef(TypedDict):
    PolicyTypeName: NotRequired[str]
    Description: NotRequired[str]
    PolicyAttributeTypeDescriptions: NotRequired[List[PolicyAttributeTypeDescriptionTypeDef]]

class RemoveTagsInputRequestTypeDef(TypedDict):
    LoadBalancerNames: Sequence[str]
    Tags: Sequence[TagKeyOnlyTypeDef]

class DescribeTagsOutputTypeDef(TypedDict):
    TagDescriptions: List[TagDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeLoadBalancerAttributesOutputTypeDef(TypedDict):
    LoadBalancerAttributes: LoadBalancerAttributesOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ModifyLoadBalancerAttributesOutputTypeDef(TypedDict):
    LoadBalancerName: str
    LoadBalancerAttributes: LoadBalancerAttributesOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ModifyLoadBalancerAttributesInputRequestTypeDef(TypedDict):
    LoadBalancerName: str
    LoadBalancerAttributes: LoadBalancerAttributesTypeDef

class LoadBalancerDescriptionTypeDef(TypedDict):
    LoadBalancerName: NotRequired[str]
    DNSName: NotRequired[str]
    CanonicalHostedZoneName: NotRequired[str]
    CanonicalHostedZoneNameID: NotRequired[str]
    ListenerDescriptions: NotRequired[List[ListenerDescriptionTypeDef]]
    Policies: NotRequired[PoliciesTypeDef]
    BackendServerDescriptions: NotRequired[List[BackendServerDescriptionTypeDef]]
    AvailabilityZones: NotRequired[List[str]]
    Subnets: NotRequired[List[str]]
    VPCId: NotRequired[str]
    Instances: NotRequired[List[InstanceTypeDef]]
    HealthCheck: NotRequired[HealthCheckTypeDef]
    SourceSecurityGroup: NotRequired[SourceSecurityGroupTypeDef]
    SecurityGroups: NotRequired[List[str]]
    CreatedTime: NotRequired[datetime]
    Scheme: NotRequired[str]

class DescribeLoadBalancerPoliciesOutputTypeDef(TypedDict):
    PolicyDescriptions: List[PolicyDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeLoadBalancerPolicyTypesOutputTypeDef(TypedDict):
    PolicyTypeDescriptions: List[PolicyTypeDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAccessPointsOutputTypeDef(TypedDict):
    LoadBalancerDescriptions: List[LoadBalancerDescriptionTypeDef]
    NextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef
