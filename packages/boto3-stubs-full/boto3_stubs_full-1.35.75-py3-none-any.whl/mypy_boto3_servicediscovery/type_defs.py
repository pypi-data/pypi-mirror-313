"""
Type annotations for servicediscovery service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicediscovery/type_defs/)

Usage::

    ```python
    from mypy_boto3_servicediscovery.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    CustomHealthStatusType,
    FilterConditionType,
    HealthCheckTypeType,
    HealthStatusFilterType,
    HealthStatusType,
    NamespaceFilterNameType,
    NamespaceTypeType,
    OperationFilterNameType,
    OperationStatusType,
    OperationTargetTypeType,
    OperationTypeType,
    RecordTypeType,
    RoutingPolicyType,
    ServiceTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "CreateHttpNamespaceRequestRequestTypeDef",
    "CreateHttpNamespaceResponseTypeDef",
    "CreatePrivateDnsNamespaceRequestRequestTypeDef",
    "CreatePrivateDnsNamespaceResponseTypeDef",
    "CreatePublicDnsNamespaceRequestRequestTypeDef",
    "CreatePublicDnsNamespaceResponseTypeDef",
    "CreateServiceRequestRequestTypeDef",
    "CreateServiceResponseTypeDef",
    "DeleteNamespaceRequestRequestTypeDef",
    "DeleteNamespaceResponseTypeDef",
    "DeleteServiceRequestRequestTypeDef",
    "DeregisterInstanceRequestRequestTypeDef",
    "DeregisterInstanceResponseTypeDef",
    "DiscoverInstancesRequestRequestTypeDef",
    "DiscoverInstancesResponseTypeDef",
    "DiscoverInstancesRevisionRequestRequestTypeDef",
    "DiscoverInstancesRevisionResponseTypeDef",
    "DnsConfigChangeTypeDef",
    "DnsConfigOutputTypeDef",
    "DnsConfigTypeDef",
    "DnsPropertiesTypeDef",
    "DnsRecordTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetInstanceRequestRequestTypeDef",
    "GetInstanceResponseTypeDef",
    "GetInstancesHealthStatusRequestRequestTypeDef",
    "GetInstancesHealthStatusResponseTypeDef",
    "GetNamespaceRequestRequestTypeDef",
    "GetNamespaceResponseTypeDef",
    "GetOperationRequestRequestTypeDef",
    "GetOperationResponseTypeDef",
    "GetServiceRequestRequestTypeDef",
    "GetServiceResponseTypeDef",
    "HealthCheckConfigTypeDef",
    "HealthCheckCustomConfigTypeDef",
    "HttpInstanceSummaryTypeDef",
    "HttpNamespaceChangeTypeDef",
    "HttpPropertiesTypeDef",
    "InstanceSummaryTypeDef",
    "InstanceTypeDef",
    "ListInstancesRequestListInstancesPaginateTypeDef",
    "ListInstancesRequestRequestTypeDef",
    "ListInstancesResponseTypeDef",
    "ListNamespacesRequestListNamespacesPaginateTypeDef",
    "ListNamespacesRequestRequestTypeDef",
    "ListNamespacesResponseTypeDef",
    "ListOperationsRequestListOperationsPaginateTypeDef",
    "ListOperationsRequestRequestTypeDef",
    "ListOperationsResponseTypeDef",
    "ListServicesRequestListServicesPaginateTypeDef",
    "ListServicesRequestRequestTypeDef",
    "ListServicesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NamespaceFilterTypeDef",
    "NamespacePropertiesTypeDef",
    "NamespaceSummaryTypeDef",
    "NamespaceTypeDef",
    "OperationFilterTypeDef",
    "OperationSummaryTypeDef",
    "OperationTypeDef",
    "PaginatorConfigTypeDef",
    "PrivateDnsNamespaceChangeTypeDef",
    "PrivateDnsNamespacePropertiesChangeTypeDef",
    "PrivateDnsNamespacePropertiesTypeDef",
    "PrivateDnsPropertiesMutableChangeTypeDef",
    "PrivateDnsPropertiesMutableTypeDef",
    "PublicDnsNamespaceChangeTypeDef",
    "PublicDnsNamespacePropertiesChangeTypeDef",
    "PublicDnsNamespacePropertiesTypeDef",
    "PublicDnsPropertiesMutableChangeTypeDef",
    "PublicDnsPropertiesMutableTypeDef",
    "RegisterInstanceRequestRequestTypeDef",
    "RegisterInstanceResponseTypeDef",
    "ResponseMetadataTypeDef",
    "SOAChangeTypeDef",
    "SOATypeDef",
    "ServiceChangeTypeDef",
    "ServiceFilterTypeDef",
    "ServiceSummaryTypeDef",
    "ServiceTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateHttpNamespaceRequestRequestTypeDef",
    "UpdateHttpNamespaceResponseTypeDef",
    "UpdateInstanceCustomHealthStatusRequestRequestTypeDef",
    "UpdatePrivateDnsNamespaceRequestRequestTypeDef",
    "UpdatePrivateDnsNamespaceResponseTypeDef",
    "UpdatePublicDnsNamespaceRequestRequestTypeDef",
    "UpdatePublicDnsNamespaceResponseTypeDef",
    "UpdateServiceRequestRequestTypeDef",
    "UpdateServiceResponseTypeDef",
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


HealthCheckConfigTypeDef = TypedDict(
    "HealthCheckConfigTypeDef",
    {
        "Type": HealthCheckTypeType,
        "ResourcePath": NotRequired[str],
        "FailureThreshold": NotRequired[int],
    },
)


class HealthCheckCustomConfigTypeDef(TypedDict):
    FailureThreshold: NotRequired[int]


class DeleteNamespaceRequestRequestTypeDef(TypedDict):
    Id: str


class DeleteServiceRequestRequestTypeDef(TypedDict):
    Id: str


class DeregisterInstanceRequestRequestTypeDef(TypedDict):
    ServiceId: str
    InstanceId: str


DiscoverInstancesRequestRequestTypeDef = TypedDict(
    "DiscoverInstancesRequestRequestTypeDef",
    {
        "NamespaceName": str,
        "ServiceName": str,
        "MaxResults": NotRequired[int],
        "QueryParameters": NotRequired[Mapping[str, str]],
        "OptionalParameters": NotRequired[Mapping[str, str]],
        "HealthStatus": NotRequired[HealthStatusFilterType],
    },
)
HttpInstanceSummaryTypeDef = TypedDict(
    "HttpInstanceSummaryTypeDef",
    {
        "InstanceId": NotRequired[str],
        "NamespaceName": NotRequired[str],
        "ServiceName": NotRequired[str],
        "HealthStatus": NotRequired[HealthStatusType],
        "Attributes": NotRequired[Dict[str, str]],
    },
)
DiscoverInstancesRevisionRequestRequestTypeDef = TypedDict(
    "DiscoverInstancesRevisionRequestRequestTypeDef",
    {
        "NamespaceName": str,
        "ServiceName": str,
    },
)
DnsRecordTypeDef = TypedDict(
    "DnsRecordTypeDef",
    {
        "Type": RecordTypeType,
        "TTL": int,
    },
)


class SOATypeDef(TypedDict):
    TTL: int


class GetInstanceRequestRequestTypeDef(TypedDict):
    ServiceId: str
    InstanceId: str


class InstanceTypeDef(TypedDict):
    Id: str
    CreatorRequestId: NotRequired[str]
    Attributes: NotRequired[Dict[str, str]]


class GetInstancesHealthStatusRequestRequestTypeDef(TypedDict):
    ServiceId: str
    Instances: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetNamespaceRequestRequestTypeDef(TypedDict):
    Id: str


class GetOperationRequestRequestTypeDef(TypedDict):
    OperationId: str


OperationTypeDef = TypedDict(
    "OperationTypeDef",
    {
        "Id": NotRequired[str],
        "Type": NotRequired[OperationTypeType],
        "Status": NotRequired[OperationStatusType],
        "ErrorMessage": NotRequired[str],
        "ErrorCode": NotRequired[str],
        "CreateDate": NotRequired[datetime],
        "UpdateDate": NotRequired[datetime],
        "Targets": NotRequired[Dict[OperationTargetTypeType, str]],
    },
)


class GetServiceRequestRequestTypeDef(TypedDict):
    Id: str


class HttpNamespaceChangeTypeDef(TypedDict):
    Description: str


class HttpPropertiesTypeDef(TypedDict):
    HttpName: NotRequired[str]


class InstanceSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Attributes: NotRequired[Dict[str, str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListInstancesRequestRequestTypeDef(TypedDict):
    ServiceId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class NamespaceFilterTypeDef(TypedDict):
    Name: NamespaceFilterNameType
    Values: Sequence[str]
    Condition: NotRequired[FilterConditionType]


class OperationFilterTypeDef(TypedDict):
    Name: OperationFilterNameType
    Values: Sequence[str]
    Condition: NotRequired[FilterConditionType]


class OperationSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Status: NotRequired[OperationStatusType]


class ServiceFilterTypeDef(TypedDict):
    Name: Literal["NAMESPACE_ID"]
    Values: Sequence[str]
    Condition: NotRequired[FilterConditionType]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str


class SOAChangeTypeDef(TypedDict):
    TTL: int


class RegisterInstanceRequestRequestTypeDef(TypedDict):
    ServiceId: str
    InstanceId: str
    Attributes: Mapping[str, str]
    CreatorRequestId: NotRequired[str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class UpdateInstanceCustomHealthStatusRequestRequestTypeDef(TypedDict):
    ServiceId: str
    InstanceId: str
    Status: CustomHealthStatusType


class CreateHttpNamespaceRequestRequestTypeDef(TypedDict):
    Name: str
    CreatorRequestId: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class CreateHttpNamespaceResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePrivateDnsNamespaceResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePublicDnsNamespaceResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteNamespaceResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeregisterInstanceResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DiscoverInstancesRevisionResponseTypeDef(TypedDict):
    InstancesRevision: int
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetInstancesHealthStatusResponseTypeDef(TypedDict):
    Status: Dict[str, HealthStatusType]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterInstanceResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateHttpNamespaceResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePrivateDnsNamespaceResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePublicDnsNamespaceResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateServiceResponseTypeDef(TypedDict):
    OperationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DiscoverInstancesResponseTypeDef(TypedDict):
    Instances: List[HttpInstanceSummaryTypeDef]
    InstancesRevision: int
    ResponseMetadata: ResponseMetadataTypeDef


class DnsConfigChangeTypeDef(TypedDict):
    DnsRecords: Sequence[DnsRecordTypeDef]


class DnsConfigOutputTypeDef(TypedDict):
    DnsRecords: List[DnsRecordTypeDef]
    NamespaceId: NotRequired[str]
    RoutingPolicy: NotRequired[RoutingPolicyType]


class DnsConfigTypeDef(TypedDict):
    DnsRecords: Sequence[DnsRecordTypeDef]
    NamespaceId: NotRequired[str]
    RoutingPolicy: NotRequired[RoutingPolicyType]


class DnsPropertiesTypeDef(TypedDict):
    HostedZoneId: NotRequired[str]
    SOA: NotRequired[SOATypeDef]


class PrivateDnsPropertiesMutableTypeDef(TypedDict):
    SOA: SOATypeDef


class PublicDnsPropertiesMutableTypeDef(TypedDict):
    SOA: SOATypeDef


class GetInstanceResponseTypeDef(TypedDict):
    Instance: InstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetOperationResponseTypeDef(TypedDict):
    Operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateHttpNamespaceRequestRequestTypeDef(TypedDict):
    Id: str
    Namespace: HttpNamespaceChangeTypeDef
    UpdaterRequestId: NotRequired[str]


class ListInstancesResponseTypeDef(TypedDict):
    Instances: List[InstanceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListInstancesRequestListInstancesPaginateTypeDef(TypedDict):
    ServiceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNamespacesRequestListNamespacesPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[NamespaceFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNamespacesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[NamespaceFilterTypeDef]]


class ListOperationsRequestListOperationsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[OperationFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOperationsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[OperationFilterTypeDef]]


class ListOperationsResponseTypeDef(TypedDict):
    Operations: List[OperationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListServicesRequestListServicesPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ServiceFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServicesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[ServiceFilterTypeDef]]


class PrivateDnsPropertiesMutableChangeTypeDef(TypedDict):
    SOA: SOAChangeTypeDef


class PublicDnsPropertiesMutableChangeTypeDef(TypedDict):
    SOA: SOAChangeTypeDef


class ServiceChangeTypeDef(TypedDict):
    Description: NotRequired[str]
    DnsConfig: NotRequired[DnsConfigChangeTypeDef]
    HealthCheckConfig: NotRequired[HealthCheckConfigTypeDef]


ServiceSummaryTypeDef = TypedDict(
    "ServiceSummaryTypeDef",
    {
        "Id": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[ServiceTypeType],
        "Description": NotRequired[str],
        "InstanceCount": NotRequired[int],
        "DnsConfig": NotRequired[DnsConfigOutputTypeDef],
        "HealthCheckConfig": NotRequired[HealthCheckConfigTypeDef],
        "HealthCheckCustomConfig": NotRequired[HealthCheckCustomConfigTypeDef],
        "CreateDate": NotRequired[datetime],
    },
)
ServiceTypeDef = TypedDict(
    "ServiceTypeDef",
    {
        "Id": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "NamespaceId": NotRequired[str],
        "Description": NotRequired[str],
        "InstanceCount": NotRequired[int],
        "DnsConfig": NotRequired[DnsConfigOutputTypeDef],
        "Type": NotRequired[ServiceTypeType],
        "HealthCheckConfig": NotRequired[HealthCheckConfigTypeDef],
        "HealthCheckCustomConfig": NotRequired[HealthCheckCustomConfigTypeDef],
        "CreateDate": NotRequired[datetime],
        "CreatorRequestId": NotRequired[str],
    },
)
CreateServiceRequestRequestTypeDef = TypedDict(
    "CreateServiceRequestRequestTypeDef",
    {
        "Name": str,
        "NamespaceId": NotRequired[str],
        "CreatorRequestId": NotRequired[str],
        "Description": NotRequired[str],
        "DnsConfig": NotRequired[DnsConfigTypeDef],
        "HealthCheckConfig": NotRequired[HealthCheckConfigTypeDef],
        "HealthCheckCustomConfig": NotRequired[HealthCheckCustomConfigTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "Type": NotRequired[Literal["HTTP"]],
    },
)


class NamespacePropertiesTypeDef(TypedDict):
    DnsProperties: NotRequired[DnsPropertiesTypeDef]
    HttpProperties: NotRequired[HttpPropertiesTypeDef]


class PrivateDnsNamespacePropertiesTypeDef(TypedDict):
    DnsProperties: PrivateDnsPropertiesMutableTypeDef


class PublicDnsNamespacePropertiesTypeDef(TypedDict):
    DnsProperties: PublicDnsPropertiesMutableTypeDef


class PrivateDnsNamespacePropertiesChangeTypeDef(TypedDict):
    DnsProperties: PrivateDnsPropertiesMutableChangeTypeDef


class PublicDnsNamespacePropertiesChangeTypeDef(TypedDict):
    DnsProperties: PublicDnsPropertiesMutableChangeTypeDef


class UpdateServiceRequestRequestTypeDef(TypedDict):
    Id: str
    Service: ServiceChangeTypeDef


class ListServicesResponseTypeDef(TypedDict):
    Services: List[ServiceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateServiceResponseTypeDef(TypedDict):
    Service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetServiceResponseTypeDef(TypedDict):
    Service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


NamespaceSummaryTypeDef = TypedDict(
    "NamespaceSummaryTypeDef",
    {
        "Id": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[NamespaceTypeType],
        "Description": NotRequired[str],
        "ServiceCount": NotRequired[int],
        "Properties": NotRequired[NamespacePropertiesTypeDef],
        "CreateDate": NotRequired[datetime],
    },
)
NamespaceTypeDef = TypedDict(
    "NamespaceTypeDef",
    {
        "Id": NotRequired[str],
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[NamespaceTypeType],
        "Description": NotRequired[str],
        "ServiceCount": NotRequired[int],
        "Properties": NotRequired[NamespacePropertiesTypeDef],
        "CreateDate": NotRequired[datetime],
        "CreatorRequestId": NotRequired[str],
    },
)


class CreatePrivateDnsNamespaceRequestRequestTypeDef(TypedDict):
    Name: str
    Vpc: str
    CreatorRequestId: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    Properties: NotRequired[PrivateDnsNamespacePropertiesTypeDef]


class CreatePublicDnsNamespaceRequestRequestTypeDef(TypedDict):
    Name: str
    CreatorRequestId: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    Properties: NotRequired[PublicDnsNamespacePropertiesTypeDef]


class PrivateDnsNamespaceChangeTypeDef(TypedDict):
    Description: NotRequired[str]
    Properties: NotRequired[PrivateDnsNamespacePropertiesChangeTypeDef]


class PublicDnsNamespaceChangeTypeDef(TypedDict):
    Description: NotRequired[str]
    Properties: NotRequired[PublicDnsNamespacePropertiesChangeTypeDef]


class ListNamespacesResponseTypeDef(TypedDict):
    Namespaces: List[NamespaceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetNamespaceResponseTypeDef(TypedDict):
    Namespace: NamespaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePrivateDnsNamespaceRequestRequestTypeDef(TypedDict):
    Id: str
    Namespace: PrivateDnsNamespaceChangeTypeDef
    UpdaterRequestId: NotRequired[str]


class UpdatePublicDnsNamespaceRequestRequestTypeDef(TypedDict):
    Id: str
    Namespace: PublicDnsNamespaceChangeTypeDef
    UpdaterRequestId: NotRequired[str]
