"""
Type annotations for apprunner service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apprunner/type_defs/)

Usage::

    ```python
    from mypy_boto3_apprunner.type_defs import AssociateCustomDomainRequestRequestTypeDef

    data: AssociateCustomDomainRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AutoScalingConfigurationStatusType,
    CertificateValidationRecordStatusType,
    ConfigurationSourceType,
    ConnectionStatusType,
    CustomDomainAssociationStatusType,
    EgressTypeType,
    HealthCheckProtocolType,
    ImageRepositoryTypeType,
    IpAddressTypeType,
    ObservabilityConfigurationStatusType,
    OperationStatusType,
    OperationTypeType,
    ProviderTypeType,
    RuntimeType,
    ServiceStatusType,
    VpcConnectorStatusType,
    VpcIngressConnectionStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AssociateCustomDomainRequestRequestTypeDef",
    "AssociateCustomDomainResponseTypeDef",
    "AuthenticationConfigurationTypeDef",
    "AutoScalingConfigurationSummaryTypeDef",
    "AutoScalingConfigurationTypeDef",
    "CertificateValidationRecordTypeDef",
    "CodeConfigurationOutputTypeDef",
    "CodeConfigurationTypeDef",
    "CodeConfigurationUnionTypeDef",
    "CodeConfigurationValuesOutputTypeDef",
    "CodeConfigurationValuesTypeDef",
    "CodeConfigurationValuesUnionTypeDef",
    "CodeRepositoryOutputTypeDef",
    "CodeRepositoryTypeDef",
    "CodeRepositoryUnionTypeDef",
    "ConnectionSummaryTypeDef",
    "ConnectionTypeDef",
    "CreateAutoScalingConfigurationRequestRequestTypeDef",
    "CreateAutoScalingConfigurationResponseTypeDef",
    "CreateConnectionRequestRequestTypeDef",
    "CreateConnectionResponseTypeDef",
    "CreateObservabilityConfigurationRequestRequestTypeDef",
    "CreateObservabilityConfigurationResponseTypeDef",
    "CreateServiceRequestRequestTypeDef",
    "CreateServiceResponseTypeDef",
    "CreateVpcConnectorRequestRequestTypeDef",
    "CreateVpcConnectorResponseTypeDef",
    "CreateVpcIngressConnectionRequestRequestTypeDef",
    "CreateVpcIngressConnectionResponseTypeDef",
    "CustomDomainTypeDef",
    "DeleteAutoScalingConfigurationRequestRequestTypeDef",
    "DeleteAutoScalingConfigurationResponseTypeDef",
    "DeleteConnectionRequestRequestTypeDef",
    "DeleteConnectionResponseTypeDef",
    "DeleteObservabilityConfigurationRequestRequestTypeDef",
    "DeleteObservabilityConfigurationResponseTypeDef",
    "DeleteServiceRequestRequestTypeDef",
    "DeleteServiceResponseTypeDef",
    "DeleteVpcConnectorRequestRequestTypeDef",
    "DeleteVpcConnectorResponseTypeDef",
    "DeleteVpcIngressConnectionRequestRequestTypeDef",
    "DeleteVpcIngressConnectionResponseTypeDef",
    "DescribeAutoScalingConfigurationRequestRequestTypeDef",
    "DescribeAutoScalingConfigurationResponseTypeDef",
    "DescribeCustomDomainsRequestRequestTypeDef",
    "DescribeCustomDomainsResponseTypeDef",
    "DescribeObservabilityConfigurationRequestRequestTypeDef",
    "DescribeObservabilityConfigurationResponseTypeDef",
    "DescribeServiceRequestRequestTypeDef",
    "DescribeServiceResponseTypeDef",
    "DescribeVpcConnectorRequestRequestTypeDef",
    "DescribeVpcConnectorResponseTypeDef",
    "DescribeVpcIngressConnectionRequestRequestTypeDef",
    "DescribeVpcIngressConnectionResponseTypeDef",
    "DisassociateCustomDomainRequestRequestTypeDef",
    "DisassociateCustomDomainResponseTypeDef",
    "EgressConfigurationTypeDef",
    "EncryptionConfigurationTypeDef",
    "HealthCheckConfigurationTypeDef",
    "ImageConfigurationOutputTypeDef",
    "ImageConfigurationTypeDef",
    "ImageConfigurationUnionTypeDef",
    "ImageRepositoryOutputTypeDef",
    "ImageRepositoryTypeDef",
    "ImageRepositoryUnionTypeDef",
    "IngressConfigurationTypeDef",
    "IngressVpcConfigurationTypeDef",
    "InstanceConfigurationTypeDef",
    "ListAutoScalingConfigurationsRequestRequestTypeDef",
    "ListAutoScalingConfigurationsResponseTypeDef",
    "ListConnectionsRequestRequestTypeDef",
    "ListConnectionsResponseTypeDef",
    "ListObservabilityConfigurationsRequestRequestTypeDef",
    "ListObservabilityConfigurationsResponseTypeDef",
    "ListOperationsRequestRequestTypeDef",
    "ListOperationsResponseTypeDef",
    "ListServicesForAutoScalingConfigurationRequestRequestTypeDef",
    "ListServicesForAutoScalingConfigurationResponseTypeDef",
    "ListServicesRequestRequestTypeDef",
    "ListServicesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListVpcConnectorsRequestRequestTypeDef",
    "ListVpcConnectorsResponseTypeDef",
    "ListVpcIngressConnectionsFilterTypeDef",
    "ListVpcIngressConnectionsRequestRequestTypeDef",
    "ListVpcIngressConnectionsResponseTypeDef",
    "NetworkConfigurationTypeDef",
    "ObservabilityConfigurationSummaryTypeDef",
    "ObservabilityConfigurationTypeDef",
    "OperationSummaryTypeDef",
    "PauseServiceRequestRequestTypeDef",
    "PauseServiceResponseTypeDef",
    "ResponseMetadataTypeDef",
    "ResumeServiceRequestRequestTypeDef",
    "ResumeServiceResponseTypeDef",
    "ServiceObservabilityConfigurationTypeDef",
    "ServiceSummaryTypeDef",
    "ServiceTypeDef",
    "SourceCodeVersionTypeDef",
    "SourceConfigurationOutputTypeDef",
    "SourceConfigurationTypeDef",
    "StartDeploymentRequestRequestTypeDef",
    "StartDeploymentResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TraceConfigurationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDefaultAutoScalingConfigurationRequestRequestTypeDef",
    "UpdateDefaultAutoScalingConfigurationResponseTypeDef",
    "UpdateServiceRequestRequestTypeDef",
    "UpdateServiceResponseTypeDef",
    "UpdateVpcIngressConnectionRequestRequestTypeDef",
    "UpdateVpcIngressConnectionResponseTypeDef",
    "VpcConnectorTypeDef",
    "VpcDNSTargetTypeDef",
    "VpcIngressConnectionSummaryTypeDef",
    "VpcIngressConnectionTypeDef",
)

class AssociateCustomDomainRequestRequestTypeDef(TypedDict):
    ServiceArn: str
    DomainName: str
    EnableWWWSubdomain: NotRequired[bool]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class VpcDNSTargetTypeDef(TypedDict):
    VpcIngressConnectionArn: NotRequired[str]
    VpcId: NotRequired[str]
    DomainName: NotRequired[str]

class AuthenticationConfigurationTypeDef(TypedDict):
    ConnectionArn: NotRequired[str]
    AccessRoleArn: NotRequired[str]

class AutoScalingConfigurationSummaryTypeDef(TypedDict):
    AutoScalingConfigurationArn: NotRequired[str]
    AutoScalingConfigurationName: NotRequired[str]
    AutoScalingConfigurationRevision: NotRequired[int]
    Status: NotRequired[AutoScalingConfigurationStatusType]
    CreatedAt: NotRequired[datetime]
    HasAssociatedService: NotRequired[bool]
    IsDefault: NotRequired[bool]

class AutoScalingConfigurationTypeDef(TypedDict):
    AutoScalingConfigurationArn: NotRequired[str]
    AutoScalingConfigurationName: NotRequired[str]
    AutoScalingConfigurationRevision: NotRequired[int]
    Latest: NotRequired[bool]
    Status: NotRequired[AutoScalingConfigurationStatusType]
    MaxConcurrency: NotRequired[int]
    MinSize: NotRequired[int]
    MaxSize: NotRequired[int]
    CreatedAt: NotRequired[datetime]
    DeletedAt: NotRequired[datetime]
    HasAssociatedService: NotRequired[bool]
    IsDefault: NotRequired[bool]

CertificateValidationRecordTypeDef = TypedDict(
    "CertificateValidationRecordTypeDef",
    {
        "Name": NotRequired[str],
        "Type": NotRequired[str],
        "Value": NotRequired[str],
        "Status": NotRequired[CertificateValidationRecordStatusType],
    },
)

class CodeConfigurationValuesOutputTypeDef(TypedDict):
    Runtime: RuntimeType
    BuildCommand: NotRequired[str]
    StartCommand: NotRequired[str]
    Port: NotRequired[str]
    RuntimeEnvironmentVariables: NotRequired[Dict[str, str]]
    RuntimeEnvironmentSecrets: NotRequired[Dict[str, str]]

class CodeConfigurationValuesTypeDef(TypedDict):
    Runtime: RuntimeType
    BuildCommand: NotRequired[str]
    StartCommand: NotRequired[str]
    Port: NotRequired[str]
    RuntimeEnvironmentVariables: NotRequired[Mapping[str, str]]
    RuntimeEnvironmentSecrets: NotRequired[Mapping[str, str]]

SourceCodeVersionTypeDef = TypedDict(
    "SourceCodeVersionTypeDef",
    {
        "Type": Literal["BRANCH"],
        "Value": str,
    },
)

class ConnectionSummaryTypeDef(TypedDict):
    ConnectionName: NotRequired[str]
    ConnectionArn: NotRequired[str]
    ProviderType: NotRequired[ProviderTypeType]
    Status: NotRequired[ConnectionStatusType]
    CreatedAt: NotRequired[datetime]

class ConnectionTypeDef(TypedDict):
    ConnectionName: NotRequired[str]
    ConnectionArn: NotRequired[str]
    ProviderType: NotRequired[ProviderTypeType]
    Status: NotRequired[ConnectionStatusType]
    CreatedAt: NotRequired[datetime]

class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

class TraceConfigurationTypeDef(TypedDict):
    Vendor: Literal["AWSXRAY"]

class EncryptionConfigurationTypeDef(TypedDict):
    KmsKey: str

HealthCheckConfigurationTypeDef = TypedDict(
    "HealthCheckConfigurationTypeDef",
    {
        "Protocol": NotRequired[HealthCheckProtocolType],
        "Path": NotRequired[str],
        "Interval": NotRequired[int],
        "Timeout": NotRequired[int],
        "HealthyThreshold": NotRequired[int],
        "UnhealthyThreshold": NotRequired[int],
    },
)

class InstanceConfigurationTypeDef(TypedDict):
    Cpu: NotRequired[str]
    Memory: NotRequired[str]
    InstanceRoleArn: NotRequired[str]

class ServiceObservabilityConfigurationTypeDef(TypedDict):
    ObservabilityEnabled: bool
    ObservabilityConfigurationArn: NotRequired[str]

class VpcConnectorTypeDef(TypedDict):
    VpcConnectorName: NotRequired[str]
    VpcConnectorArn: NotRequired[str]
    VpcConnectorRevision: NotRequired[int]
    Subnets: NotRequired[List[str]]
    SecurityGroups: NotRequired[List[str]]
    Status: NotRequired[VpcConnectorStatusType]
    CreatedAt: NotRequired[datetime]
    DeletedAt: NotRequired[datetime]

class IngressVpcConfigurationTypeDef(TypedDict):
    VpcId: NotRequired[str]
    VpcEndpointId: NotRequired[str]

class DeleteAutoScalingConfigurationRequestRequestTypeDef(TypedDict):
    AutoScalingConfigurationArn: str
    DeleteAllRevisions: NotRequired[bool]

class DeleteConnectionRequestRequestTypeDef(TypedDict):
    ConnectionArn: str

class DeleteObservabilityConfigurationRequestRequestTypeDef(TypedDict):
    ObservabilityConfigurationArn: str

class DeleteServiceRequestRequestTypeDef(TypedDict):
    ServiceArn: str

class DeleteVpcConnectorRequestRequestTypeDef(TypedDict):
    VpcConnectorArn: str

class DeleteVpcIngressConnectionRequestRequestTypeDef(TypedDict):
    VpcIngressConnectionArn: str

class DescribeAutoScalingConfigurationRequestRequestTypeDef(TypedDict):
    AutoScalingConfigurationArn: str

class DescribeCustomDomainsRequestRequestTypeDef(TypedDict):
    ServiceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class DescribeObservabilityConfigurationRequestRequestTypeDef(TypedDict):
    ObservabilityConfigurationArn: str

class DescribeServiceRequestRequestTypeDef(TypedDict):
    ServiceArn: str

class DescribeVpcConnectorRequestRequestTypeDef(TypedDict):
    VpcConnectorArn: str

class DescribeVpcIngressConnectionRequestRequestTypeDef(TypedDict):
    VpcIngressConnectionArn: str

class DisassociateCustomDomainRequestRequestTypeDef(TypedDict):
    ServiceArn: str
    DomainName: str

class EgressConfigurationTypeDef(TypedDict):
    EgressType: NotRequired[EgressTypeType]
    VpcConnectorArn: NotRequired[str]

class ImageConfigurationOutputTypeDef(TypedDict):
    RuntimeEnvironmentVariables: NotRequired[Dict[str, str]]
    StartCommand: NotRequired[str]
    Port: NotRequired[str]
    RuntimeEnvironmentSecrets: NotRequired[Dict[str, str]]

class ImageConfigurationTypeDef(TypedDict):
    RuntimeEnvironmentVariables: NotRequired[Mapping[str, str]]
    StartCommand: NotRequired[str]
    Port: NotRequired[str]
    RuntimeEnvironmentSecrets: NotRequired[Mapping[str, str]]

class IngressConfigurationTypeDef(TypedDict):
    IsPubliclyAccessible: NotRequired[bool]

class ListAutoScalingConfigurationsRequestRequestTypeDef(TypedDict):
    AutoScalingConfigurationName: NotRequired[str]
    LatestOnly: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListConnectionsRequestRequestTypeDef(TypedDict):
    ConnectionName: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListObservabilityConfigurationsRequestRequestTypeDef(TypedDict):
    ObservabilityConfigurationName: NotRequired[str]
    LatestOnly: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ObservabilityConfigurationSummaryTypeDef(TypedDict):
    ObservabilityConfigurationArn: NotRequired[str]
    ObservabilityConfigurationName: NotRequired[str]
    ObservabilityConfigurationRevision: NotRequired[int]

class ListOperationsRequestRequestTypeDef(TypedDict):
    ServiceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

OperationSummaryTypeDef = TypedDict(
    "OperationSummaryTypeDef",
    {
        "Id": NotRequired[str],
        "Type": NotRequired[OperationTypeType],
        "Status": NotRequired[OperationStatusType],
        "TargetArn": NotRequired[str],
        "StartedAt": NotRequired[datetime],
        "EndedAt": NotRequired[datetime],
        "UpdatedAt": NotRequired[datetime],
    },
)

class ListServicesForAutoScalingConfigurationRequestRequestTypeDef(TypedDict):
    AutoScalingConfigurationArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListServicesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

ServiceSummaryTypeDef = TypedDict(
    "ServiceSummaryTypeDef",
    {
        "ServiceName": NotRequired[str],
        "ServiceId": NotRequired[str],
        "ServiceArn": NotRequired[str],
        "ServiceUrl": NotRequired[str],
        "CreatedAt": NotRequired[datetime],
        "UpdatedAt": NotRequired[datetime],
        "Status": NotRequired[ServiceStatusType],
    },
)

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class ListVpcConnectorsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListVpcIngressConnectionsFilterTypeDef(TypedDict):
    ServiceArn: NotRequired[str]
    VpcEndpointId: NotRequired[str]

class VpcIngressConnectionSummaryTypeDef(TypedDict):
    VpcIngressConnectionArn: NotRequired[str]
    ServiceArn: NotRequired[str]

class PauseServiceRequestRequestTypeDef(TypedDict):
    ServiceArn: str

class ResumeServiceRequestRequestTypeDef(TypedDict):
    ServiceArn: str

class StartDeploymentRequestRequestTypeDef(TypedDict):
    ServiceArn: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateDefaultAutoScalingConfigurationRequestRequestTypeDef(TypedDict):
    AutoScalingConfigurationArn: str

class ListServicesForAutoScalingConfigurationResponseTypeDef(TypedDict):
    ServiceArnList: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StartDeploymentResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAutoScalingConfigurationsResponseTypeDef(TypedDict):
    AutoScalingConfigurationSummaryList: List[AutoScalingConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateAutoScalingConfigurationResponseTypeDef(TypedDict):
    AutoScalingConfiguration: AutoScalingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAutoScalingConfigurationResponseTypeDef(TypedDict):
    AutoScalingConfiguration: AutoScalingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAutoScalingConfigurationResponseTypeDef(TypedDict):
    AutoScalingConfiguration: AutoScalingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDefaultAutoScalingConfigurationResponseTypeDef(TypedDict):
    AutoScalingConfiguration: AutoScalingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CustomDomainTypeDef(TypedDict):
    DomainName: str
    EnableWWWSubdomain: bool
    Status: CustomDomainAssociationStatusType
    CertificateValidationRecords: NotRequired[List[CertificateValidationRecordTypeDef]]

class CodeConfigurationOutputTypeDef(TypedDict):
    ConfigurationSource: ConfigurationSourceType
    CodeConfigurationValues: NotRequired[CodeConfigurationValuesOutputTypeDef]

CodeConfigurationValuesUnionTypeDef = Union[
    CodeConfigurationValuesTypeDef, CodeConfigurationValuesOutputTypeDef
]

class ListConnectionsResponseTypeDef(TypedDict):
    ConnectionSummaryList: List[ConnectionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateConnectionResponseTypeDef(TypedDict):
    Connection: ConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteConnectionResponseTypeDef(TypedDict):
    Connection: ConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAutoScalingConfigurationRequestRequestTypeDef(TypedDict):
    AutoScalingConfigurationName: str
    MaxConcurrency: NotRequired[int]
    MinSize: NotRequired[int]
    MaxSize: NotRequired[int]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateConnectionRequestRequestTypeDef(TypedDict):
    ConnectionName: str
    ProviderType: ProviderTypeType
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateVpcConnectorRequestRequestTypeDef(TypedDict):
    VpcConnectorName: str
    Subnets: Sequence[str]
    SecurityGroups: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class CreateObservabilityConfigurationRequestRequestTypeDef(TypedDict):
    ObservabilityConfigurationName: str
    TraceConfiguration: NotRequired[TraceConfigurationTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class ObservabilityConfigurationTypeDef(TypedDict):
    ObservabilityConfigurationArn: NotRequired[str]
    ObservabilityConfigurationName: NotRequired[str]
    TraceConfiguration: NotRequired[TraceConfigurationTypeDef]
    ObservabilityConfigurationRevision: NotRequired[int]
    Latest: NotRequired[bool]
    Status: NotRequired[ObservabilityConfigurationStatusType]
    CreatedAt: NotRequired[datetime]
    DeletedAt: NotRequired[datetime]

class CreateVpcConnectorResponseTypeDef(TypedDict):
    VpcConnector: VpcConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteVpcConnectorResponseTypeDef(TypedDict):
    VpcConnector: VpcConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeVpcConnectorResponseTypeDef(TypedDict):
    VpcConnector: VpcConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListVpcConnectorsResponseTypeDef(TypedDict):
    VpcConnectors: List[VpcConnectorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateVpcIngressConnectionRequestRequestTypeDef(TypedDict):
    ServiceArn: str
    VpcIngressConnectionName: str
    IngressVpcConfiguration: IngressVpcConfigurationTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]

class UpdateVpcIngressConnectionRequestRequestTypeDef(TypedDict):
    VpcIngressConnectionArn: str
    IngressVpcConfiguration: IngressVpcConfigurationTypeDef

class VpcIngressConnectionTypeDef(TypedDict):
    VpcIngressConnectionArn: NotRequired[str]
    VpcIngressConnectionName: NotRequired[str]
    ServiceArn: NotRequired[str]
    Status: NotRequired[VpcIngressConnectionStatusType]
    AccountId: NotRequired[str]
    DomainName: NotRequired[str]
    IngressVpcConfiguration: NotRequired[IngressVpcConfigurationTypeDef]
    CreatedAt: NotRequired[datetime]
    DeletedAt: NotRequired[datetime]

class ImageRepositoryOutputTypeDef(TypedDict):
    ImageIdentifier: str
    ImageRepositoryType: ImageRepositoryTypeType
    ImageConfiguration: NotRequired[ImageConfigurationOutputTypeDef]

ImageConfigurationUnionTypeDef = Union[ImageConfigurationTypeDef, ImageConfigurationOutputTypeDef]

class NetworkConfigurationTypeDef(TypedDict):
    EgressConfiguration: NotRequired[EgressConfigurationTypeDef]
    IngressConfiguration: NotRequired[IngressConfigurationTypeDef]
    IpAddressType: NotRequired[IpAddressTypeType]

class ListObservabilityConfigurationsResponseTypeDef(TypedDict):
    ObservabilityConfigurationSummaryList: List[ObservabilityConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListOperationsResponseTypeDef(TypedDict):
    OperationSummaryList: List[OperationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListServicesResponseTypeDef(TypedDict):
    ServiceSummaryList: List[ServiceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListVpcIngressConnectionsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[ListVpcIngressConnectionsFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListVpcIngressConnectionsResponseTypeDef(TypedDict):
    VpcIngressConnectionSummaryList: List[VpcIngressConnectionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class AssociateCustomDomainResponseTypeDef(TypedDict):
    DNSTarget: str
    ServiceArn: str
    CustomDomain: CustomDomainTypeDef
    VpcDNSTargets: List[VpcDNSTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCustomDomainsResponseTypeDef(TypedDict):
    DNSTarget: str
    ServiceArn: str
    CustomDomains: List[CustomDomainTypeDef]
    VpcDNSTargets: List[VpcDNSTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DisassociateCustomDomainResponseTypeDef(TypedDict):
    DNSTarget: str
    ServiceArn: str
    CustomDomain: CustomDomainTypeDef
    VpcDNSTargets: List[VpcDNSTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CodeRepositoryOutputTypeDef(TypedDict):
    RepositoryUrl: str
    SourceCodeVersion: SourceCodeVersionTypeDef
    CodeConfiguration: NotRequired[CodeConfigurationOutputTypeDef]
    SourceDirectory: NotRequired[str]

class CodeConfigurationTypeDef(TypedDict):
    ConfigurationSource: ConfigurationSourceType
    CodeConfigurationValues: NotRequired[CodeConfigurationValuesUnionTypeDef]

class CreateObservabilityConfigurationResponseTypeDef(TypedDict):
    ObservabilityConfiguration: ObservabilityConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteObservabilityConfigurationResponseTypeDef(TypedDict):
    ObservabilityConfiguration: ObservabilityConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeObservabilityConfigurationResponseTypeDef(TypedDict):
    ObservabilityConfiguration: ObservabilityConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateVpcIngressConnectionResponseTypeDef(TypedDict):
    VpcIngressConnection: VpcIngressConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteVpcIngressConnectionResponseTypeDef(TypedDict):
    VpcIngressConnection: VpcIngressConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeVpcIngressConnectionResponseTypeDef(TypedDict):
    VpcIngressConnection: VpcIngressConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateVpcIngressConnectionResponseTypeDef(TypedDict):
    VpcIngressConnection: VpcIngressConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ImageRepositoryTypeDef(TypedDict):
    ImageIdentifier: str
    ImageRepositoryType: ImageRepositoryTypeType
    ImageConfiguration: NotRequired[ImageConfigurationUnionTypeDef]

class SourceConfigurationOutputTypeDef(TypedDict):
    CodeRepository: NotRequired[CodeRepositoryOutputTypeDef]
    ImageRepository: NotRequired[ImageRepositoryOutputTypeDef]
    AutoDeploymentsEnabled: NotRequired[bool]
    AuthenticationConfiguration: NotRequired[AuthenticationConfigurationTypeDef]

CodeConfigurationUnionTypeDef = Union[CodeConfigurationTypeDef, CodeConfigurationOutputTypeDef]
ImageRepositoryUnionTypeDef = Union[ImageRepositoryTypeDef, ImageRepositoryOutputTypeDef]
ServiceTypeDef = TypedDict(
    "ServiceTypeDef",
    {
        "ServiceName": str,
        "ServiceId": str,
        "ServiceArn": str,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Status": ServiceStatusType,
        "SourceConfiguration": SourceConfigurationOutputTypeDef,
        "InstanceConfiguration": InstanceConfigurationTypeDef,
        "AutoScalingConfigurationSummary": AutoScalingConfigurationSummaryTypeDef,
        "NetworkConfiguration": NetworkConfigurationTypeDef,
        "ServiceUrl": NotRequired[str],
        "DeletedAt": NotRequired[datetime],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "HealthCheckConfiguration": NotRequired[HealthCheckConfigurationTypeDef],
        "ObservabilityConfiguration": NotRequired[ServiceObservabilityConfigurationTypeDef],
    },
)

class CodeRepositoryTypeDef(TypedDict):
    RepositoryUrl: str
    SourceCodeVersion: SourceCodeVersionTypeDef
    CodeConfiguration: NotRequired[CodeConfigurationUnionTypeDef]
    SourceDirectory: NotRequired[str]

class CreateServiceResponseTypeDef(TypedDict):
    Service: ServiceTypeDef
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteServiceResponseTypeDef(TypedDict):
    Service: ServiceTypeDef
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeServiceResponseTypeDef(TypedDict):
    Service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PauseServiceResponseTypeDef(TypedDict):
    Service: ServiceTypeDef
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ResumeServiceResponseTypeDef(TypedDict):
    Service: ServiceTypeDef
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateServiceResponseTypeDef(TypedDict):
    Service: ServiceTypeDef
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef

CodeRepositoryUnionTypeDef = Union[CodeRepositoryTypeDef, CodeRepositoryOutputTypeDef]

class SourceConfigurationTypeDef(TypedDict):
    CodeRepository: NotRequired[CodeRepositoryUnionTypeDef]
    ImageRepository: NotRequired[ImageRepositoryUnionTypeDef]
    AutoDeploymentsEnabled: NotRequired[bool]
    AuthenticationConfiguration: NotRequired[AuthenticationConfigurationTypeDef]

CreateServiceRequestRequestTypeDef = TypedDict(
    "CreateServiceRequestRequestTypeDef",
    {
        "ServiceName": str,
        "SourceConfiguration": SourceConfigurationTypeDef,
        "InstanceConfiguration": NotRequired[InstanceConfigurationTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "HealthCheckConfiguration": NotRequired[HealthCheckConfigurationTypeDef],
        "AutoScalingConfigurationArn": NotRequired[str],
        "NetworkConfiguration": NotRequired[NetworkConfigurationTypeDef],
        "ObservabilityConfiguration": NotRequired[ServiceObservabilityConfigurationTypeDef],
    },
)

class UpdateServiceRequestRequestTypeDef(TypedDict):
    ServiceArn: str
    SourceConfiguration: NotRequired[SourceConfigurationTypeDef]
    InstanceConfiguration: NotRequired[InstanceConfigurationTypeDef]
    AutoScalingConfigurationArn: NotRequired[str]
    HealthCheckConfiguration: NotRequired[HealthCheckConfigurationTypeDef]
    NetworkConfiguration: NotRequired[NetworkConfigurationTypeDef]
    ObservabilityConfiguration: NotRequired[ServiceObservabilityConfigurationTypeDef]
