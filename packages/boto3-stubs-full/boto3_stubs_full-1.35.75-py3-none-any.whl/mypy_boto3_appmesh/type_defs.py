"""
Type annotations for appmesh service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appmesh/type_defs/)

Usage::

    ```python
    from mypy_boto3_appmesh.type_defs import AwsCloudMapInstanceAttributeTypeDef

    data: AwsCloudMapInstanceAttributeTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    DefaultGatewayRouteRewriteType,
    DnsResponseTypeType,
    DurationUnitType,
    EgressFilterTypeType,
    GatewayRouteStatusCodeType,
    GrpcRetryPolicyEventType,
    HttpMethodType,
    HttpSchemeType,
    IpPreferenceType,
    ListenerTlsModeType,
    MeshStatusCodeType,
    PortProtocolType,
    RouteStatusCodeType,
    VirtualGatewayListenerTlsModeType,
    VirtualGatewayPortProtocolType,
    VirtualGatewayStatusCodeType,
    VirtualNodeStatusCodeType,
    VirtualRouterStatusCodeType,
    VirtualServiceStatusCodeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccessLogOutputTypeDef",
    "AccessLogTypeDef",
    "AccessLogUnionTypeDef",
    "AwsCloudMapInstanceAttributeTypeDef",
    "AwsCloudMapServiceDiscoveryOutputTypeDef",
    "AwsCloudMapServiceDiscoveryTypeDef",
    "AwsCloudMapServiceDiscoveryUnionTypeDef",
    "BackendDefaultsOutputTypeDef",
    "BackendDefaultsTypeDef",
    "BackendDefaultsUnionTypeDef",
    "BackendOutputTypeDef",
    "BackendTypeDef",
    "BackendUnionTypeDef",
    "ClientPolicyOutputTypeDef",
    "ClientPolicyTlsOutputTypeDef",
    "ClientPolicyTlsTypeDef",
    "ClientPolicyTlsUnionTypeDef",
    "ClientPolicyTypeDef",
    "ClientPolicyUnionTypeDef",
    "ClientTlsCertificateTypeDef",
    "CreateGatewayRouteInputRequestTypeDef",
    "CreateGatewayRouteOutputTypeDef",
    "CreateMeshInputRequestTypeDef",
    "CreateMeshOutputTypeDef",
    "CreateRouteInputRequestTypeDef",
    "CreateRouteOutputTypeDef",
    "CreateVirtualGatewayInputRequestTypeDef",
    "CreateVirtualGatewayOutputTypeDef",
    "CreateVirtualNodeInputRequestTypeDef",
    "CreateVirtualNodeOutputTypeDef",
    "CreateVirtualRouterInputRequestTypeDef",
    "CreateVirtualRouterOutputTypeDef",
    "CreateVirtualServiceInputRequestTypeDef",
    "CreateVirtualServiceOutputTypeDef",
    "DeleteGatewayRouteInputRequestTypeDef",
    "DeleteGatewayRouteOutputTypeDef",
    "DeleteMeshInputRequestTypeDef",
    "DeleteMeshOutputTypeDef",
    "DeleteRouteInputRequestTypeDef",
    "DeleteRouteOutputTypeDef",
    "DeleteVirtualGatewayInputRequestTypeDef",
    "DeleteVirtualGatewayOutputTypeDef",
    "DeleteVirtualNodeInputRequestTypeDef",
    "DeleteVirtualNodeOutputTypeDef",
    "DeleteVirtualRouterInputRequestTypeDef",
    "DeleteVirtualRouterOutputTypeDef",
    "DeleteVirtualServiceInputRequestTypeDef",
    "DeleteVirtualServiceOutputTypeDef",
    "DescribeGatewayRouteInputRequestTypeDef",
    "DescribeGatewayRouteOutputTypeDef",
    "DescribeMeshInputRequestTypeDef",
    "DescribeMeshOutputTypeDef",
    "DescribeRouteInputRequestTypeDef",
    "DescribeRouteOutputTypeDef",
    "DescribeVirtualGatewayInputRequestTypeDef",
    "DescribeVirtualGatewayOutputTypeDef",
    "DescribeVirtualNodeInputRequestTypeDef",
    "DescribeVirtualNodeOutputTypeDef",
    "DescribeVirtualRouterInputRequestTypeDef",
    "DescribeVirtualRouterOutputTypeDef",
    "DescribeVirtualServiceInputRequestTypeDef",
    "DescribeVirtualServiceOutputTypeDef",
    "DnsServiceDiscoveryTypeDef",
    "DurationTypeDef",
    "EgressFilterTypeDef",
    "FileAccessLogOutputTypeDef",
    "FileAccessLogTypeDef",
    "FileAccessLogUnionTypeDef",
    "GatewayRouteDataTypeDef",
    "GatewayRouteHostnameMatchTypeDef",
    "GatewayRouteHostnameRewriteTypeDef",
    "GatewayRouteRefTypeDef",
    "GatewayRouteSpecOutputTypeDef",
    "GatewayRouteSpecTypeDef",
    "GatewayRouteStatusTypeDef",
    "GatewayRouteTargetTypeDef",
    "GatewayRouteVirtualServiceTypeDef",
    "GrpcGatewayRouteActionTypeDef",
    "GrpcGatewayRouteMatchOutputTypeDef",
    "GrpcGatewayRouteMatchTypeDef",
    "GrpcGatewayRouteMatchUnionTypeDef",
    "GrpcGatewayRouteMetadataTypeDef",
    "GrpcGatewayRouteOutputTypeDef",
    "GrpcGatewayRouteRewriteTypeDef",
    "GrpcGatewayRouteTypeDef",
    "GrpcGatewayRouteUnionTypeDef",
    "GrpcMetadataMatchMethodTypeDef",
    "GrpcRetryPolicyOutputTypeDef",
    "GrpcRetryPolicyTypeDef",
    "GrpcRetryPolicyUnionTypeDef",
    "GrpcRouteActionOutputTypeDef",
    "GrpcRouteActionTypeDef",
    "GrpcRouteActionUnionTypeDef",
    "GrpcRouteMatchOutputTypeDef",
    "GrpcRouteMatchTypeDef",
    "GrpcRouteMatchUnionTypeDef",
    "GrpcRouteMetadataMatchMethodTypeDef",
    "GrpcRouteMetadataTypeDef",
    "GrpcRouteOutputTypeDef",
    "GrpcRouteTypeDef",
    "GrpcRouteUnionTypeDef",
    "GrpcTimeoutTypeDef",
    "HeaderMatchMethodTypeDef",
    "HealthCheckPolicyTypeDef",
    "HttpGatewayRouteActionTypeDef",
    "HttpGatewayRouteHeaderTypeDef",
    "HttpGatewayRouteMatchOutputTypeDef",
    "HttpGatewayRouteMatchTypeDef",
    "HttpGatewayRouteMatchUnionTypeDef",
    "HttpGatewayRouteOutputTypeDef",
    "HttpGatewayRoutePathRewriteTypeDef",
    "HttpGatewayRoutePrefixRewriteTypeDef",
    "HttpGatewayRouteRewriteTypeDef",
    "HttpGatewayRouteTypeDef",
    "HttpGatewayRouteUnionTypeDef",
    "HttpPathMatchTypeDef",
    "HttpQueryParameterTypeDef",
    "HttpRetryPolicyOutputTypeDef",
    "HttpRetryPolicyTypeDef",
    "HttpRetryPolicyUnionTypeDef",
    "HttpRouteActionOutputTypeDef",
    "HttpRouteActionTypeDef",
    "HttpRouteActionUnionTypeDef",
    "HttpRouteHeaderTypeDef",
    "HttpRouteMatchOutputTypeDef",
    "HttpRouteMatchTypeDef",
    "HttpRouteMatchUnionTypeDef",
    "HttpRouteOutputTypeDef",
    "HttpRouteTypeDef",
    "HttpRouteUnionTypeDef",
    "HttpTimeoutTypeDef",
    "JsonFormatRefTypeDef",
    "ListGatewayRoutesInputListGatewayRoutesPaginateTypeDef",
    "ListGatewayRoutesInputRequestTypeDef",
    "ListGatewayRoutesOutputTypeDef",
    "ListMeshesInputListMeshesPaginateTypeDef",
    "ListMeshesInputRequestTypeDef",
    "ListMeshesOutputTypeDef",
    "ListRoutesInputListRoutesPaginateTypeDef",
    "ListRoutesInputRequestTypeDef",
    "ListRoutesOutputTypeDef",
    "ListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListVirtualGatewaysInputListVirtualGatewaysPaginateTypeDef",
    "ListVirtualGatewaysInputRequestTypeDef",
    "ListVirtualGatewaysOutputTypeDef",
    "ListVirtualNodesInputListVirtualNodesPaginateTypeDef",
    "ListVirtualNodesInputRequestTypeDef",
    "ListVirtualNodesOutputTypeDef",
    "ListVirtualRoutersInputListVirtualRoutersPaginateTypeDef",
    "ListVirtualRoutersInputRequestTypeDef",
    "ListVirtualRoutersOutputTypeDef",
    "ListVirtualServicesInputListVirtualServicesPaginateTypeDef",
    "ListVirtualServicesInputRequestTypeDef",
    "ListVirtualServicesOutputTypeDef",
    "ListenerOutputTypeDef",
    "ListenerTimeoutTypeDef",
    "ListenerTlsAcmCertificateTypeDef",
    "ListenerTlsCertificateTypeDef",
    "ListenerTlsFileCertificateTypeDef",
    "ListenerTlsOutputTypeDef",
    "ListenerTlsSdsCertificateTypeDef",
    "ListenerTlsTypeDef",
    "ListenerTlsUnionTypeDef",
    "ListenerTlsValidationContextOutputTypeDef",
    "ListenerTlsValidationContextTrustTypeDef",
    "ListenerTlsValidationContextTypeDef",
    "ListenerTlsValidationContextUnionTypeDef",
    "ListenerTypeDef",
    "ListenerUnionTypeDef",
    "LoggingFormatOutputTypeDef",
    "LoggingFormatTypeDef",
    "LoggingFormatUnionTypeDef",
    "LoggingOutputTypeDef",
    "LoggingTypeDef",
    "LoggingUnionTypeDef",
    "MatchRangeTypeDef",
    "MeshDataTypeDef",
    "MeshRefTypeDef",
    "MeshServiceDiscoveryTypeDef",
    "MeshSpecTypeDef",
    "MeshStatusTypeDef",
    "OutlierDetectionTypeDef",
    "PaginatorConfigTypeDef",
    "PortMappingTypeDef",
    "QueryParameterMatchTypeDef",
    "ResourceMetadataTypeDef",
    "ResponseMetadataTypeDef",
    "RouteDataTypeDef",
    "RouteRefTypeDef",
    "RouteSpecOutputTypeDef",
    "RouteSpecTypeDef",
    "RouteStatusTypeDef",
    "ServiceDiscoveryOutputTypeDef",
    "ServiceDiscoveryTypeDef",
    "ServiceDiscoveryUnionTypeDef",
    "SubjectAlternativeNameMatchersOutputTypeDef",
    "SubjectAlternativeNameMatchersTypeDef",
    "SubjectAlternativeNameMatchersUnionTypeDef",
    "SubjectAlternativeNamesOutputTypeDef",
    "SubjectAlternativeNamesTypeDef",
    "SubjectAlternativeNamesUnionTypeDef",
    "TagRefTypeDef",
    "TagResourceInputRequestTypeDef",
    "TcpRouteActionOutputTypeDef",
    "TcpRouteActionTypeDef",
    "TcpRouteActionUnionTypeDef",
    "TcpRouteMatchTypeDef",
    "TcpRouteOutputTypeDef",
    "TcpRouteTypeDef",
    "TcpRouteUnionTypeDef",
    "TcpTimeoutTypeDef",
    "TlsValidationContextAcmTrustOutputTypeDef",
    "TlsValidationContextAcmTrustTypeDef",
    "TlsValidationContextAcmTrustUnionTypeDef",
    "TlsValidationContextFileTrustTypeDef",
    "TlsValidationContextOutputTypeDef",
    "TlsValidationContextSdsTrustTypeDef",
    "TlsValidationContextTrustOutputTypeDef",
    "TlsValidationContextTrustTypeDef",
    "TlsValidationContextTrustUnionTypeDef",
    "TlsValidationContextTypeDef",
    "TlsValidationContextUnionTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateGatewayRouteInputRequestTypeDef",
    "UpdateGatewayRouteOutputTypeDef",
    "UpdateMeshInputRequestTypeDef",
    "UpdateMeshOutputTypeDef",
    "UpdateRouteInputRequestTypeDef",
    "UpdateRouteOutputTypeDef",
    "UpdateVirtualGatewayInputRequestTypeDef",
    "UpdateVirtualGatewayOutputTypeDef",
    "UpdateVirtualNodeInputRequestTypeDef",
    "UpdateVirtualNodeOutputTypeDef",
    "UpdateVirtualRouterInputRequestTypeDef",
    "UpdateVirtualRouterOutputTypeDef",
    "UpdateVirtualServiceInputRequestTypeDef",
    "UpdateVirtualServiceOutputTypeDef",
    "VirtualGatewayAccessLogOutputTypeDef",
    "VirtualGatewayAccessLogTypeDef",
    "VirtualGatewayAccessLogUnionTypeDef",
    "VirtualGatewayBackendDefaultsOutputTypeDef",
    "VirtualGatewayBackendDefaultsTypeDef",
    "VirtualGatewayBackendDefaultsUnionTypeDef",
    "VirtualGatewayClientPolicyOutputTypeDef",
    "VirtualGatewayClientPolicyTlsOutputTypeDef",
    "VirtualGatewayClientPolicyTlsTypeDef",
    "VirtualGatewayClientPolicyTlsUnionTypeDef",
    "VirtualGatewayClientPolicyTypeDef",
    "VirtualGatewayClientPolicyUnionTypeDef",
    "VirtualGatewayClientTlsCertificateTypeDef",
    "VirtualGatewayConnectionPoolTypeDef",
    "VirtualGatewayDataTypeDef",
    "VirtualGatewayFileAccessLogOutputTypeDef",
    "VirtualGatewayFileAccessLogTypeDef",
    "VirtualGatewayFileAccessLogUnionTypeDef",
    "VirtualGatewayGrpcConnectionPoolTypeDef",
    "VirtualGatewayHealthCheckPolicyTypeDef",
    "VirtualGatewayHttp2ConnectionPoolTypeDef",
    "VirtualGatewayHttpConnectionPoolTypeDef",
    "VirtualGatewayListenerOutputTypeDef",
    "VirtualGatewayListenerTlsAcmCertificateTypeDef",
    "VirtualGatewayListenerTlsCertificateTypeDef",
    "VirtualGatewayListenerTlsFileCertificateTypeDef",
    "VirtualGatewayListenerTlsOutputTypeDef",
    "VirtualGatewayListenerTlsSdsCertificateTypeDef",
    "VirtualGatewayListenerTlsTypeDef",
    "VirtualGatewayListenerTlsUnionTypeDef",
    "VirtualGatewayListenerTlsValidationContextOutputTypeDef",
    "VirtualGatewayListenerTlsValidationContextTrustTypeDef",
    "VirtualGatewayListenerTlsValidationContextTypeDef",
    "VirtualGatewayListenerTlsValidationContextUnionTypeDef",
    "VirtualGatewayListenerTypeDef",
    "VirtualGatewayListenerUnionTypeDef",
    "VirtualGatewayLoggingOutputTypeDef",
    "VirtualGatewayLoggingTypeDef",
    "VirtualGatewayLoggingUnionTypeDef",
    "VirtualGatewayPortMappingTypeDef",
    "VirtualGatewayRefTypeDef",
    "VirtualGatewaySpecOutputTypeDef",
    "VirtualGatewaySpecTypeDef",
    "VirtualGatewayStatusTypeDef",
    "VirtualGatewayTlsValidationContextAcmTrustOutputTypeDef",
    "VirtualGatewayTlsValidationContextAcmTrustTypeDef",
    "VirtualGatewayTlsValidationContextAcmTrustUnionTypeDef",
    "VirtualGatewayTlsValidationContextFileTrustTypeDef",
    "VirtualGatewayTlsValidationContextOutputTypeDef",
    "VirtualGatewayTlsValidationContextSdsTrustTypeDef",
    "VirtualGatewayTlsValidationContextTrustOutputTypeDef",
    "VirtualGatewayTlsValidationContextTrustTypeDef",
    "VirtualGatewayTlsValidationContextTrustUnionTypeDef",
    "VirtualGatewayTlsValidationContextTypeDef",
    "VirtualGatewayTlsValidationContextUnionTypeDef",
    "VirtualNodeConnectionPoolTypeDef",
    "VirtualNodeDataTypeDef",
    "VirtualNodeGrpcConnectionPoolTypeDef",
    "VirtualNodeHttp2ConnectionPoolTypeDef",
    "VirtualNodeHttpConnectionPoolTypeDef",
    "VirtualNodeRefTypeDef",
    "VirtualNodeServiceProviderTypeDef",
    "VirtualNodeSpecOutputTypeDef",
    "VirtualNodeSpecTypeDef",
    "VirtualNodeStatusTypeDef",
    "VirtualNodeTcpConnectionPoolTypeDef",
    "VirtualRouterDataTypeDef",
    "VirtualRouterListenerTypeDef",
    "VirtualRouterRefTypeDef",
    "VirtualRouterServiceProviderTypeDef",
    "VirtualRouterSpecOutputTypeDef",
    "VirtualRouterSpecTypeDef",
    "VirtualRouterStatusTypeDef",
    "VirtualServiceBackendOutputTypeDef",
    "VirtualServiceBackendTypeDef",
    "VirtualServiceBackendUnionTypeDef",
    "VirtualServiceDataTypeDef",
    "VirtualServiceProviderTypeDef",
    "VirtualServiceRefTypeDef",
    "VirtualServiceSpecTypeDef",
    "VirtualServiceStatusTypeDef",
    "WeightedTargetTypeDef",
)


class AwsCloudMapInstanceAttributeTypeDef(TypedDict):
    key: str
    value: str


class ListenerTlsFileCertificateTypeDef(TypedDict):
    certificateChain: str
    privateKey: str


class ListenerTlsSdsCertificateTypeDef(TypedDict):
    secretName: str


class TagRefTypeDef(TypedDict):
    key: str
    value: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteGatewayRouteInputRequestTypeDef(TypedDict):
    gatewayRouteName: str
    meshName: str
    virtualGatewayName: str
    meshOwner: NotRequired[str]


class DeleteMeshInputRequestTypeDef(TypedDict):
    meshName: str


class DeleteRouteInputRequestTypeDef(TypedDict):
    meshName: str
    routeName: str
    virtualRouterName: str
    meshOwner: NotRequired[str]


class DeleteVirtualGatewayInputRequestTypeDef(TypedDict):
    meshName: str
    virtualGatewayName: str
    meshOwner: NotRequired[str]


class DeleteVirtualNodeInputRequestTypeDef(TypedDict):
    meshName: str
    virtualNodeName: str
    meshOwner: NotRequired[str]


class DeleteVirtualRouterInputRequestTypeDef(TypedDict):
    meshName: str
    virtualRouterName: str
    meshOwner: NotRequired[str]


class DeleteVirtualServiceInputRequestTypeDef(TypedDict):
    meshName: str
    virtualServiceName: str
    meshOwner: NotRequired[str]


class DescribeGatewayRouteInputRequestTypeDef(TypedDict):
    gatewayRouteName: str
    meshName: str
    virtualGatewayName: str
    meshOwner: NotRequired[str]


class DescribeMeshInputRequestTypeDef(TypedDict):
    meshName: str
    meshOwner: NotRequired[str]


class DescribeRouteInputRequestTypeDef(TypedDict):
    meshName: str
    routeName: str
    virtualRouterName: str
    meshOwner: NotRequired[str]


class DescribeVirtualGatewayInputRequestTypeDef(TypedDict):
    meshName: str
    virtualGatewayName: str
    meshOwner: NotRequired[str]


class DescribeVirtualNodeInputRequestTypeDef(TypedDict):
    meshName: str
    virtualNodeName: str
    meshOwner: NotRequired[str]


class DescribeVirtualRouterInputRequestTypeDef(TypedDict):
    meshName: str
    virtualRouterName: str
    meshOwner: NotRequired[str]


class DescribeVirtualServiceInputRequestTypeDef(TypedDict):
    meshName: str
    virtualServiceName: str
    meshOwner: NotRequired[str]


class DnsServiceDiscoveryTypeDef(TypedDict):
    hostname: str
    ipPreference: NotRequired[IpPreferenceType]
    responseType: NotRequired[DnsResponseTypeType]


class DurationTypeDef(TypedDict):
    unit: NotRequired[DurationUnitType]
    value: NotRequired[int]


EgressFilterTypeDef = TypedDict(
    "EgressFilterTypeDef",
    {
        "type": EgressFilterTypeType,
    },
)


class GatewayRouteStatusTypeDef(TypedDict):
    status: GatewayRouteStatusCodeType


class ResourceMetadataTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastUpdatedAt: datetime
    meshOwner: str
    resourceOwner: str
    uid: str
    version: int


class GatewayRouteHostnameMatchTypeDef(TypedDict):
    exact: NotRequired[str]
    suffix: NotRequired[str]


class GatewayRouteHostnameRewriteTypeDef(TypedDict):
    defaultTargetHostname: NotRequired[DefaultGatewayRouteRewriteType]


class GatewayRouteRefTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    gatewayRouteName: str
    lastUpdatedAt: datetime
    meshName: str
    meshOwner: str
    resourceOwner: str
    version: int
    virtualGatewayName: str


class GatewayRouteVirtualServiceTypeDef(TypedDict):
    virtualServiceName: str


class MatchRangeTypeDef(TypedDict):
    end: int
    start: int


class WeightedTargetTypeDef(TypedDict):
    virtualNode: str
    weight: int
    port: NotRequired[int]


class HealthCheckPolicyTypeDef(TypedDict):
    healthyThreshold: int
    intervalMillis: int
    protocol: PortProtocolType
    timeoutMillis: int
    unhealthyThreshold: int
    path: NotRequired[str]
    port: NotRequired[int]


class HttpPathMatchTypeDef(TypedDict):
    exact: NotRequired[str]
    regex: NotRequired[str]


class HttpGatewayRoutePathRewriteTypeDef(TypedDict):
    exact: NotRequired[str]


class HttpGatewayRoutePrefixRewriteTypeDef(TypedDict):
    defaultPrefix: NotRequired[DefaultGatewayRouteRewriteType]
    value: NotRequired[str]


class QueryParameterMatchTypeDef(TypedDict):
    exact: NotRequired[str]


class JsonFormatRefTypeDef(TypedDict):
    key: str
    value: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListGatewayRoutesInputRequestTypeDef(TypedDict):
    meshName: str
    virtualGatewayName: str
    limit: NotRequired[int]
    meshOwner: NotRequired[str]
    nextToken: NotRequired[str]


class ListMeshesInputRequestTypeDef(TypedDict):
    limit: NotRequired[int]
    nextToken: NotRequired[str]


class MeshRefTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastUpdatedAt: datetime
    meshName: str
    meshOwner: str
    resourceOwner: str
    version: int


class ListRoutesInputRequestTypeDef(TypedDict):
    meshName: str
    virtualRouterName: str
    limit: NotRequired[int]
    meshOwner: NotRequired[str]
    nextToken: NotRequired[str]


class RouteRefTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastUpdatedAt: datetime
    meshName: str
    meshOwner: str
    resourceOwner: str
    routeName: str
    version: int
    virtualRouterName: str


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    limit: NotRequired[int]
    nextToken: NotRequired[str]


class ListVirtualGatewaysInputRequestTypeDef(TypedDict):
    meshName: str
    limit: NotRequired[int]
    meshOwner: NotRequired[str]
    nextToken: NotRequired[str]


class VirtualGatewayRefTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastUpdatedAt: datetime
    meshName: str
    meshOwner: str
    resourceOwner: str
    version: int
    virtualGatewayName: str


class ListVirtualNodesInputRequestTypeDef(TypedDict):
    meshName: str
    limit: NotRequired[int]
    meshOwner: NotRequired[str]
    nextToken: NotRequired[str]


class VirtualNodeRefTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastUpdatedAt: datetime
    meshName: str
    meshOwner: str
    resourceOwner: str
    version: int
    virtualNodeName: str


class ListVirtualRoutersInputRequestTypeDef(TypedDict):
    meshName: str
    limit: NotRequired[int]
    meshOwner: NotRequired[str]
    nextToken: NotRequired[str]


class VirtualRouterRefTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastUpdatedAt: datetime
    meshName: str
    meshOwner: str
    resourceOwner: str
    version: int
    virtualRouterName: str


class ListVirtualServicesInputRequestTypeDef(TypedDict):
    meshName: str
    limit: NotRequired[int]
    meshOwner: NotRequired[str]
    nextToken: NotRequired[str]


class VirtualServiceRefTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    lastUpdatedAt: datetime
    meshName: str
    meshOwner: str
    resourceOwner: str
    version: int
    virtualServiceName: str


class PortMappingTypeDef(TypedDict):
    port: int
    protocol: PortProtocolType


class ListenerTlsAcmCertificateTypeDef(TypedDict):
    certificateArn: str


class TlsValidationContextFileTrustTypeDef(TypedDict):
    certificateChain: str


class TlsValidationContextSdsTrustTypeDef(TypedDict):
    secretName: str


class MeshStatusTypeDef(TypedDict):
    status: NotRequired[MeshStatusCodeType]


class MeshServiceDiscoveryTypeDef(TypedDict):
    ipPreference: NotRequired[IpPreferenceType]


class RouteStatusTypeDef(TypedDict):
    status: RouteStatusCodeType


class SubjectAlternativeNameMatchersOutputTypeDef(TypedDict):
    exact: List[str]


class SubjectAlternativeNameMatchersTypeDef(TypedDict):
    exact: Sequence[str]


class TcpRouteMatchTypeDef(TypedDict):
    port: NotRequired[int]


class TlsValidationContextAcmTrustOutputTypeDef(TypedDict):
    certificateAuthorityArns: List[str]


class TlsValidationContextAcmTrustTypeDef(TypedDict):
    certificateAuthorityArns: Sequence[str]


class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class VirtualGatewayListenerTlsFileCertificateTypeDef(TypedDict):
    certificateChain: str
    privateKey: str


class VirtualGatewayListenerTlsSdsCertificateTypeDef(TypedDict):
    secretName: str


class VirtualGatewayGrpcConnectionPoolTypeDef(TypedDict):
    maxRequests: int


class VirtualGatewayHttp2ConnectionPoolTypeDef(TypedDict):
    maxRequests: int


class VirtualGatewayHttpConnectionPoolTypeDef(TypedDict):
    maxConnections: int
    maxPendingRequests: NotRequired[int]


class VirtualGatewayStatusTypeDef(TypedDict):
    status: VirtualGatewayStatusCodeType


class VirtualGatewayHealthCheckPolicyTypeDef(TypedDict):
    healthyThreshold: int
    intervalMillis: int
    protocol: VirtualGatewayPortProtocolType
    timeoutMillis: int
    unhealthyThreshold: int
    path: NotRequired[str]
    port: NotRequired[int]


class VirtualGatewayPortMappingTypeDef(TypedDict):
    port: int
    protocol: VirtualGatewayPortProtocolType


class VirtualGatewayListenerTlsAcmCertificateTypeDef(TypedDict):
    certificateArn: str


class VirtualGatewayTlsValidationContextFileTrustTypeDef(TypedDict):
    certificateChain: str


class VirtualGatewayTlsValidationContextSdsTrustTypeDef(TypedDict):
    secretName: str


class VirtualGatewayTlsValidationContextAcmTrustOutputTypeDef(TypedDict):
    certificateAuthorityArns: List[str]


class VirtualGatewayTlsValidationContextAcmTrustTypeDef(TypedDict):
    certificateAuthorityArns: Sequence[str]


class VirtualNodeGrpcConnectionPoolTypeDef(TypedDict):
    maxRequests: int


class VirtualNodeHttp2ConnectionPoolTypeDef(TypedDict):
    maxRequests: int


class VirtualNodeHttpConnectionPoolTypeDef(TypedDict):
    maxConnections: int
    maxPendingRequests: NotRequired[int]


class VirtualNodeTcpConnectionPoolTypeDef(TypedDict):
    maxConnections: int


class VirtualNodeStatusTypeDef(TypedDict):
    status: VirtualNodeStatusCodeType


class VirtualNodeServiceProviderTypeDef(TypedDict):
    virtualNodeName: str


class VirtualRouterStatusTypeDef(TypedDict):
    status: VirtualRouterStatusCodeType


class VirtualRouterServiceProviderTypeDef(TypedDict):
    virtualRouterName: str


class VirtualServiceStatusTypeDef(TypedDict):
    status: VirtualServiceStatusCodeType


class AwsCloudMapServiceDiscoveryOutputTypeDef(TypedDict):
    namespaceName: str
    serviceName: str
    attributes: NotRequired[List[AwsCloudMapInstanceAttributeTypeDef]]
    ipPreference: NotRequired[IpPreferenceType]


class AwsCloudMapServiceDiscoveryTypeDef(TypedDict):
    namespaceName: str
    serviceName: str
    attributes: NotRequired[Sequence[AwsCloudMapInstanceAttributeTypeDef]]
    ipPreference: NotRequired[IpPreferenceType]


class ClientTlsCertificateTypeDef(TypedDict):
    file: NotRequired[ListenerTlsFileCertificateTypeDef]
    sds: NotRequired[ListenerTlsSdsCertificateTypeDef]


class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagRefTypeDef]


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: List[TagRefTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GrpcRetryPolicyOutputTypeDef(TypedDict):
    maxRetries: int
    perRetryTimeout: DurationTypeDef
    grpcRetryEvents: NotRequired[List[GrpcRetryPolicyEventType]]
    httpRetryEvents: NotRequired[List[str]]
    tcpRetryEvents: NotRequired[List[Literal["connection-error"]]]


class GrpcRetryPolicyTypeDef(TypedDict):
    maxRetries: int
    perRetryTimeout: DurationTypeDef
    grpcRetryEvents: NotRequired[Sequence[GrpcRetryPolicyEventType]]
    httpRetryEvents: NotRequired[Sequence[str]]
    tcpRetryEvents: NotRequired[Sequence[Literal["connection-error"]]]


class GrpcTimeoutTypeDef(TypedDict):
    idle: NotRequired[DurationTypeDef]
    perRequest: NotRequired[DurationTypeDef]


class HttpRetryPolicyOutputTypeDef(TypedDict):
    maxRetries: int
    perRetryTimeout: DurationTypeDef
    httpRetryEvents: NotRequired[List[str]]
    tcpRetryEvents: NotRequired[List[Literal["connection-error"]]]


class HttpRetryPolicyTypeDef(TypedDict):
    maxRetries: int
    perRetryTimeout: DurationTypeDef
    httpRetryEvents: NotRequired[Sequence[str]]
    tcpRetryEvents: NotRequired[Sequence[Literal["connection-error"]]]


class HttpTimeoutTypeDef(TypedDict):
    idle: NotRequired[DurationTypeDef]
    perRequest: NotRequired[DurationTypeDef]


class OutlierDetectionTypeDef(TypedDict):
    baseEjectionDuration: DurationTypeDef
    interval: DurationTypeDef
    maxEjectionPercent: int
    maxServerErrors: int


class TcpTimeoutTypeDef(TypedDict):
    idle: NotRequired[DurationTypeDef]


class GrpcGatewayRouteRewriteTypeDef(TypedDict):
    hostname: NotRequired[GatewayRouteHostnameRewriteTypeDef]


class ListGatewayRoutesOutputTypeDef(TypedDict):
    gatewayRoutes: List[GatewayRouteRefTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GatewayRouteTargetTypeDef(TypedDict):
    virtualService: GatewayRouteVirtualServiceTypeDef
    port: NotRequired[int]


GrpcMetadataMatchMethodTypeDef = TypedDict(
    "GrpcMetadataMatchMethodTypeDef",
    {
        "exact": NotRequired[str],
        "prefix": NotRequired[str],
        "range": NotRequired[MatchRangeTypeDef],
        "regex": NotRequired[str],
        "suffix": NotRequired[str],
    },
)
GrpcRouteMetadataMatchMethodTypeDef = TypedDict(
    "GrpcRouteMetadataMatchMethodTypeDef",
    {
        "exact": NotRequired[str],
        "prefix": NotRequired[str],
        "range": NotRequired[MatchRangeTypeDef],
        "regex": NotRequired[str],
        "suffix": NotRequired[str],
    },
)
HeaderMatchMethodTypeDef = TypedDict(
    "HeaderMatchMethodTypeDef",
    {
        "exact": NotRequired[str],
        "prefix": NotRequired[str],
        "range": NotRequired[MatchRangeTypeDef],
        "regex": NotRequired[str],
        "suffix": NotRequired[str],
    },
)


class GrpcRouteActionOutputTypeDef(TypedDict):
    weightedTargets: List[WeightedTargetTypeDef]


class GrpcRouteActionTypeDef(TypedDict):
    weightedTargets: Sequence[WeightedTargetTypeDef]


class HttpRouteActionOutputTypeDef(TypedDict):
    weightedTargets: List[WeightedTargetTypeDef]


class HttpRouteActionTypeDef(TypedDict):
    weightedTargets: Sequence[WeightedTargetTypeDef]


class TcpRouteActionOutputTypeDef(TypedDict):
    weightedTargets: List[WeightedTargetTypeDef]


class TcpRouteActionTypeDef(TypedDict):
    weightedTargets: Sequence[WeightedTargetTypeDef]


class HttpGatewayRouteRewriteTypeDef(TypedDict):
    hostname: NotRequired[GatewayRouteHostnameRewriteTypeDef]
    path: NotRequired[HttpGatewayRoutePathRewriteTypeDef]
    prefix: NotRequired[HttpGatewayRoutePrefixRewriteTypeDef]


class HttpQueryParameterTypeDef(TypedDict):
    name: str
    match: NotRequired[QueryParameterMatchTypeDef]


class LoggingFormatOutputTypeDef(TypedDict):
    json: NotRequired[List[JsonFormatRefTypeDef]]
    text: NotRequired[str]


class LoggingFormatTypeDef(TypedDict):
    json: NotRequired[Sequence[JsonFormatRefTypeDef]]
    text: NotRequired[str]


class ListGatewayRoutesInputListGatewayRoutesPaginateTypeDef(TypedDict):
    meshName: str
    virtualGatewayName: str
    meshOwner: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMeshesInputListMeshesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRoutesInputListRoutesPaginateTypeDef(TypedDict):
    meshName: str
    virtualRouterName: str
    meshOwner: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsForResourceInputListTagsForResourcePaginateTypeDef(TypedDict):
    resourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVirtualGatewaysInputListVirtualGatewaysPaginateTypeDef(TypedDict):
    meshName: str
    meshOwner: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVirtualNodesInputListVirtualNodesPaginateTypeDef(TypedDict):
    meshName: str
    meshOwner: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVirtualRoutersInputListVirtualRoutersPaginateTypeDef(TypedDict):
    meshName: str
    meshOwner: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVirtualServicesInputListVirtualServicesPaginateTypeDef(TypedDict):
    meshName: str
    meshOwner: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMeshesOutputTypeDef(TypedDict):
    meshes: List[MeshRefTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListRoutesOutputTypeDef(TypedDict):
    routes: List[RouteRefTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListVirtualGatewaysOutputTypeDef(TypedDict):
    virtualGateways: List[VirtualGatewayRefTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListVirtualNodesOutputTypeDef(TypedDict):
    virtualNodes: List[VirtualNodeRefTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListVirtualRoutersOutputTypeDef(TypedDict):
    virtualRouters: List[VirtualRouterRefTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListVirtualServicesOutputTypeDef(TypedDict):
    virtualServices: List[VirtualServiceRefTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class VirtualRouterListenerTypeDef(TypedDict):
    portMapping: PortMappingTypeDef


class ListenerTlsCertificateTypeDef(TypedDict):
    acm: NotRequired[ListenerTlsAcmCertificateTypeDef]
    file: NotRequired[ListenerTlsFileCertificateTypeDef]
    sds: NotRequired[ListenerTlsSdsCertificateTypeDef]


class ListenerTlsValidationContextTrustTypeDef(TypedDict):
    file: NotRequired[TlsValidationContextFileTrustTypeDef]
    sds: NotRequired[TlsValidationContextSdsTrustTypeDef]


class MeshSpecTypeDef(TypedDict):
    egressFilter: NotRequired[EgressFilterTypeDef]
    serviceDiscovery: NotRequired[MeshServiceDiscoveryTypeDef]


class SubjectAlternativeNamesOutputTypeDef(TypedDict):
    match: SubjectAlternativeNameMatchersOutputTypeDef


SubjectAlternativeNameMatchersUnionTypeDef = Union[
    SubjectAlternativeNameMatchersTypeDef, SubjectAlternativeNameMatchersOutputTypeDef
]


class TlsValidationContextTrustOutputTypeDef(TypedDict):
    acm: NotRequired[TlsValidationContextAcmTrustOutputTypeDef]
    file: NotRequired[TlsValidationContextFileTrustTypeDef]
    sds: NotRequired[TlsValidationContextSdsTrustTypeDef]


TlsValidationContextAcmTrustUnionTypeDef = Union[
    TlsValidationContextAcmTrustTypeDef, TlsValidationContextAcmTrustOutputTypeDef
]


class VirtualGatewayClientTlsCertificateTypeDef(TypedDict):
    file: NotRequired[VirtualGatewayListenerTlsFileCertificateTypeDef]
    sds: NotRequired[VirtualGatewayListenerTlsSdsCertificateTypeDef]


class VirtualGatewayConnectionPoolTypeDef(TypedDict):
    grpc: NotRequired[VirtualGatewayGrpcConnectionPoolTypeDef]
    http: NotRequired[VirtualGatewayHttpConnectionPoolTypeDef]
    http2: NotRequired[VirtualGatewayHttp2ConnectionPoolTypeDef]


class VirtualGatewayListenerTlsCertificateTypeDef(TypedDict):
    acm: NotRequired[VirtualGatewayListenerTlsAcmCertificateTypeDef]
    file: NotRequired[VirtualGatewayListenerTlsFileCertificateTypeDef]
    sds: NotRequired[VirtualGatewayListenerTlsSdsCertificateTypeDef]


class VirtualGatewayListenerTlsValidationContextTrustTypeDef(TypedDict):
    file: NotRequired[VirtualGatewayTlsValidationContextFileTrustTypeDef]
    sds: NotRequired[VirtualGatewayTlsValidationContextSdsTrustTypeDef]


class VirtualGatewayTlsValidationContextTrustOutputTypeDef(TypedDict):
    acm: NotRequired[VirtualGatewayTlsValidationContextAcmTrustOutputTypeDef]
    file: NotRequired[VirtualGatewayTlsValidationContextFileTrustTypeDef]
    sds: NotRequired[VirtualGatewayTlsValidationContextSdsTrustTypeDef]


VirtualGatewayTlsValidationContextAcmTrustUnionTypeDef = Union[
    VirtualGatewayTlsValidationContextAcmTrustTypeDef,
    VirtualGatewayTlsValidationContextAcmTrustOutputTypeDef,
]


class VirtualNodeConnectionPoolTypeDef(TypedDict):
    grpc: NotRequired[VirtualNodeGrpcConnectionPoolTypeDef]
    http: NotRequired[VirtualNodeHttpConnectionPoolTypeDef]
    http2: NotRequired[VirtualNodeHttp2ConnectionPoolTypeDef]
    tcp: NotRequired[VirtualNodeTcpConnectionPoolTypeDef]


class VirtualServiceProviderTypeDef(TypedDict):
    virtualNode: NotRequired[VirtualNodeServiceProviderTypeDef]
    virtualRouter: NotRequired[VirtualRouterServiceProviderTypeDef]


class ServiceDiscoveryOutputTypeDef(TypedDict):
    awsCloudMap: NotRequired[AwsCloudMapServiceDiscoveryOutputTypeDef]
    dns: NotRequired[DnsServiceDiscoveryTypeDef]


AwsCloudMapServiceDiscoveryUnionTypeDef = Union[
    AwsCloudMapServiceDiscoveryTypeDef, AwsCloudMapServiceDiscoveryOutputTypeDef
]
GrpcRetryPolicyUnionTypeDef = Union[GrpcRetryPolicyTypeDef, GrpcRetryPolicyOutputTypeDef]
HttpRetryPolicyUnionTypeDef = Union[HttpRetryPolicyTypeDef, HttpRetryPolicyOutputTypeDef]


class ListenerTimeoutTypeDef(TypedDict):
    grpc: NotRequired[GrpcTimeoutTypeDef]
    http: NotRequired[HttpTimeoutTypeDef]
    http2: NotRequired[HttpTimeoutTypeDef]
    tcp: NotRequired[TcpTimeoutTypeDef]


class GrpcGatewayRouteActionTypeDef(TypedDict):
    target: GatewayRouteTargetTypeDef
    rewrite: NotRequired[GrpcGatewayRouteRewriteTypeDef]


class GrpcGatewayRouteMetadataTypeDef(TypedDict):
    name: str
    invert: NotRequired[bool]
    match: NotRequired[GrpcMetadataMatchMethodTypeDef]


class GrpcRouteMetadataTypeDef(TypedDict):
    name: str
    invert: NotRequired[bool]
    match: NotRequired[GrpcRouteMetadataMatchMethodTypeDef]


class HttpGatewayRouteHeaderTypeDef(TypedDict):
    name: str
    invert: NotRequired[bool]
    match: NotRequired[HeaderMatchMethodTypeDef]


class HttpRouteHeaderTypeDef(TypedDict):
    name: str
    invert: NotRequired[bool]
    match: NotRequired[HeaderMatchMethodTypeDef]


GrpcRouteActionUnionTypeDef = Union[GrpcRouteActionTypeDef, GrpcRouteActionOutputTypeDef]
HttpRouteActionUnionTypeDef = Union[HttpRouteActionTypeDef, HttpRouteActionOutputTypeDef]


class TcpRouteOutputTypeDef(TypedDict):
    action: TcpRouteActionOutputTypeDef
    match: NotRequired[TcpRouteMatchTypeDef]
    timeout: NotRequired[TcpTimeoutTypeDef]


TcpRouteActionUnionTypeDef = Union[TcpRouteActionTypeDef, TcpRouteActionOutputTypeDef]


class HttpGatewayRouteActionTypeDef(TypedDict):
    target: GatewayRouteTargetTypeDef
    rewrite: NotRequired[HttpGatewayRouteRewriteTypeDef]


FileAccessLogOutputTypeDef = TypedDict(
    "FileAccessLogOutputTypeDef",
    {
        "path": str,
        "format": NotRequired[LoggingFormatOutputTypeDef],
    },
)
VirtualGatewayFileAccessLogOutputTypeDef = TypedDict(
    "VirtualGatewayFileAccessLogOutputTypeDef",
    {
        "path": str,
        "format": NotRequired[LoggingFormatOutputTypeDef],
    },
)
LoggingFormatUnionTypeDef = Union[LoggingFormatTypeDef, LoggingFormatOutputTypeDef]


class VirtualRouterSpecOutputTypeDef(TypedDict):
    listeners: NotRequired[List[VirtualRouterListenerTypeDef]]


class VirtualRouterSpecTypeDef(TypedDict):
    listeners: NotRequired[Sequence[VirtualRouterListenerTypeDef]]


class CreateMeshInputRequestTypeDef(TypedDict):
    meshName: str
    clientToken: NotRequired[str]
    spec: NotRequired[MeshSpecTypeDef]
    tags: NotRequired[Sequence[TagRefTypeDef]]


class MeshDataTypeDef(TypedDict):
    meshName: str
    metadata: ResourceMetadataTypeDef
    spec: MeshSpecTypeDef
    status: MeshStatusTypeDef


class UpdateMeshInputRequestTypeDef(TypedDict):
    meshName: str
    clientToken: NotRequired[str]
    spec: NotRequired[MeshSpecTypeDef]


class ListenerTlsValidationContextOutputTypeDef(TypedDict):
    trust: ListenerTlsValidationContextTrustTypeDef
    subjectAlternativeNames: NotRequired[SubjectAlternativeNamesOutputTypeDef]


class SubjectAlternativeNamesTypeDef(TypedDict):
    match: SubjectAlternativeNameMatchersUnionTypeDef


class TlsValidationContextOutputTypeDef(TypedDict):
    trust: TlsValidationContextTrustOutputTypeDef
    subjectAlternativeNames: NotRequired[SubjectAlternativeNamesOutputTypeDef]


class TlsValidationContextTrustTypeDef(TypedDict):
    acm: NotRequired[TlsValidationContextAcmTrustUnionTypeDef]
    file: NotRequired[TlsValidationContextFileTrustTypeDef]
    sds: NotRequired[TlsValidationContextSdsTrustTypeDef]


class VirtualGatewayListenerTlsValidationContextOutputTypeDef(TypedDict):
    trust: VirtualGatewayListenerTlsValidationContextTrustTypeDef
    subjectAlternativeNames: NotRequired[SubjectAlternativeNamesOutputTypeDef]


class VirtualGatewayTlsValidationContextOutputTypeDef(TypedDict):
    trust: VirtualGatewayTlsValidationContextTrustOutputTypeDef
    subjectAlternativeNames: NotRequired[SubjectAlternativeNamesOutputTypeDef]


class VirtualGatewayTlsValidationContextTrustTypeDef(TypedDict):
    acm: NotRequired[VirtualGatewayTlsValidationContextAcmTrustUnionTypeDef]
    file: NotRequired[VirtualGatewayTlsValidationContextFileTrustTypeDef]
    sds: NotRequired[VirtualGatewayTlsValidationContextSdsTrustTypeDef]


class VirtualServiceSpecTypeDef(TypedDict):
    provider: NotRequired[VirtualServiceProviderTypeDef]


class ServiceDiscoveryTypeDef(TypedDict):
    awsCloudMap: NotRequired[AwsCloudMapServiceDiscoveryUnionTypeDef]
    dns: NotRequired[DnsServiceDiscoveryTypeDef]


class GrpcGatewayRouteMatchOutputTypeDef(TypedDict):
    hostname: NotRequired[GatewayRouteHostnameMatchTypeDef]
    metadata: NotRequired[List[GrpcGatewayRouteMetadataTypeDef]]
    port: NotRequired[int]
    serviceName: NotRequired[str]


class GrpcGatewayRouteMatchTypeDef(TypedDict):
    hostname: NotRequired[GatewayRouteHostnameMatchTypeDef]
    metadata: NotRequired[Sequence[GrpcGatewayRouteMetadataTypeDef]]
    port: NotRequired[int]
    serviceName: NotRequired[str]


class GrpcRouteMatchOutputTypeDef(TypedDict):
    metadata: NotRequired[List[GrpcRouteMetadataTypeDef]]
    methodName: NotRequired[str]
    port: NotRequired[int]
    serviceName: NotRequired[str]


class GrpcRouteMatchTypeDef(TypedDict):
    metadata: NotRequired[Sequence[GrpcRouteMetadataTypeDef]]
    methodName: NotRequired[str]
    port: NotRequired[int]
    serviceName: NotRequired[str]


class HttpGatewayRouteMatchOutputTypeDef(TypedDict):
    headers: NotRequired[List[HttpGatewayRouteHeaderTypeDef]]
    hostname: NotRequired[GatewayRouteHostnameMatchTypeDef]
    method: NotRequired[HttpMethodType]
    path: NotRequired[HttpPathMatchTypeDef]
    port: NotRequired[int]
    prefix: NotRequired[str]
    queryParameters: NotRequired[List[HttpQueryParameterTypeDef]]


class HttpGatewayRouteMatchTypeDef(TypedDict):
    headers: NotRequired[Sequence[HttpGatewayRouteHeaderTypeDef]]
    hostname: NotRequired[GatewayRouteHostnameMatchTypeDef]
    method: NotRequired[HttpMethodType]
    path: NotRequired[HttpPathMatchTypeDef]
    port: NotRequired[int]
    prefix: NotRequired[str]
    queryParameters: NotRequired[Sequence[HttpQueryParameterTypeDef]]


class HttpRouteMatchOutputTypeDef(TypedDict):
    headers: NotRequired[List[HttpRouteHeaderTypeDef]]
    method: NotRequired[HttpMethodType]
    path: NotRequired[HttpPathMatchTypeDef]
    port: NotRequired[int]
    prefix: NotRequired[str]
    queryParameters: NotRequired[List[HttpQueryParameterTypeDef]]
    scheme: NotRequired[HttpSchemeType]


class HttpRouteMatchTypeDef(TypedDict):
    headers: NotRequired[Sequence[HttpRouteHeaderTypeDef]]
    method: NotRequired[HttpMethodType]
    path: NotRequired[HttpPathMatchTypeDef]
    port: NotRequired[int]
    prefix: NotRequired[str]
    queryParameters: NotRequired[Sequence[HttpQueryParameterTypeDef]]
    scheme: NotRequired[HttpSchemeType]


class TcpRouteTypeDef(TypedDict):
    action: TcpRouteActionUnionTypeDef
    match: NotRequired[TcpRouteMatchTypeDef]
    timeout: NotRequired[TcpTimeoutTypeDef]


class AccessLogOutputTypeDef(TypedDict):
    file: NotRequired[FileAccessLogOutputTypeDef]


class VirtualGatewayAccessLogOutputTypeDef(TypedDict):
    file: NotRequired[VirtualGatewayFileAccessLogOutputTypeDef]


FileAccessLogTypeDef = TypedDict(
    "FileAccessLogTypeDef",
    {
        "path": str,
        "format": NotRequired[LoggingFormatUnionTypeDef],
    },
)
VirtualGatewayFileAccessLogTypeDef = TypedDict(
    "VirtualGatewayFileAccessLogTypeDef",
    {
        "path": str,
        "format": NotRequired[LoggingFormatUnionTypeDef],
    },
)


class VirtualRouterDataTypeDef(TypedDict):
    meshName: str
    metadata: ResourceMetadataTypeDef
    spec: VirtualRouterSpecOutputTypeDef
    status: VirtualRouterStatusTypeDef
    virtualRouterName: str


class CreateVirtualRouterInputRequestTypeDef(TypedDict):
    meshName: str
    spec: VirtualRouterSpecTypeDef
    virtualRouterName: str
    clientToken: NotRequired[str]
    meshOwner: NotRequired[str]
    tags: NotRequired[Sequence[TagRefTypeDef]]


class UpdateVirtualRouterInputRequestTypeDef(TypedDict):
    meshName: str
    spec: VirtualRouterSpecTypeDef
    virtualRouterName: str
    clientToken: NotRequired[str]
    meshOwner: NotRequired[str]


class CreateMeshOutputTypeDef(TypedDict):
    mesh: MeshDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMeshOutputTypeDef(TypedDict):
    mesh: MeshDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMeshOutputTypeDef(TypedDict):
    mesh: MeshDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMeshOutputTypeDef(TypedDict):
    mesh: MeshDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListenerTlsOutputTypeDef(TypedDict):
    certificate: ListenerTlsCertificateTypeDef
    mode: ListenerTlsModeType
    validation: NotRequired[ListenerTlsValidationContextOutputTypeDef]


SubjectAlternativeNamesUnionTypeDef = Union[
    SubjectAlternativeNamesTypeDef, SubjectAlternativeNamesOutputTypeDef
]


class ClientPolicyTlsOutputTypeDef(TypedDict):
    validation: TlsValidationContextOutputTypeDef
    certificate: NotRequired[ClientTlsCertificateTypeDef]
    enforce: NotRequired[bool]
    ports: NotRequired[List[int]]


TlsValidationContextTrustUnionTypeDef = Union[
    TlsValidationContextTrustTypeDef, TlsValidationContextTrustOutputTypeDef
]


class VirtualGatewayListenerTlsOutputTypeDef(TypedDict):
    certificate: VirtualGatewayListenerTlsCertificateTypeDef
    mode: VirtualGatewayListenerTlsModeType
    validation: NotRequired[VirtualGatewayListenerTlsValidationContextOutputTypeDef]


class VirtualGatewayClientPolicyTlsOutputTypeDef(TypedDict):
    validation: VirtualGatewayTlsValidationContextOutputTypeDef
    certificate: NotRequired[VirtualGatewayClientTlsCertificateTypeDef]
    enforce: NotRequired[bool]
    ports: NotRequired[List[int]]


VirtualGatewayTlsValidationContextTrustUnionTypeDef = Union[
    VirtualGatewayTlsValidationContextTrustTypeDef,
    VirtualGatewayTlsValidationContextTrustOutputTypeDef,
]


class CreateVirtualServiceInputRequestTypeDef(TypedDict):
    meshName: str
    spec: VirtualServiceSpecTypeDef
    virtualServiceName: str
    clientToken: NotRequired[str]
    meshOwner: NotRequired[str]
    tags: NotRequired[Sequence[TagRefTypeDef]]


class UpdateVirtualServiceInputRequestTypeDef(TypedDict):
    meshName: str
    spec: VirtualServiceSpecTypeDef
    virtualServiceName: str
    clientToken: NotRequired[str]
    meshOwner: NotRequired[str]


class VirtualServiceDataTypeDef(TypedDict):
    meshName: str
    metadata: ResourceMetadataTypeDef
    spec: VirtualServiceSpecTypeDef
    status: VirtualServiceStatusTypeDef
    virtualServiceName: str


ServiceDiscoveryUnionTypeDef = Union[ServiceDiscoveryTypeDef, ServiceDiscoveryOutputTypeDef]


class GrpcGatewayRouteOutputTypeDef(TypedDict):
    action: GrpcGatewayRouteActionTypeDef
    match: GrpcGatewayRouteMatchOutputTypeDef


GrpcGatewayRouteMatchUnionTypeDef = Union[
    GrpcGatewayRouteMatchTypeDef, GrpcGatewayRouteMatchOutputTypeDef
]


class GrpcRouteOutputTypeDef(TypedDict):
    action: GrpcRouteActionOutputTypeDef
    match: GrpcRouteMatchOutputTypeDef
    retryPolicy: NotRequired[GrpcRetryPolicyOutputTypeDef]
    timeout: NotRequired[GrpcTimeoutTypeDef]


GrpcRouteMatchUnionTypeDef = Union[GrpcRouteMatchTypeDef, GrpcRouteMatchOutputTypeDef]


class HttpGatewayRouteOutputTypeDef(TypedDict):
    action: HttpGatewayRouteActionTypeDef
    match: HttpGatewayRouteMatchOutputTypeDef


HttpGatewayRouteMatchUnionTypeDef = Union[
    HttpGatewayRouteMatchTypeDef, HttpGatewayRouteMatchOutputTypeDef
]


class HttpRouteOutputTypeDef(TypedDict):
    action: HttpRouteActionOutputTypeDef
    match: HttpRouteMatchOutputTypeDef
    retryPolicy: NotRequired[HttpRetryPolicyOutputTypeDef]
    timeout: NotRequired[HttpTimeoutTypeDef]


HttpRouteMatchUnionTypeDef = Union[HttpRouteMatchTypeDef, HttpRouteMatchOutputTypeDef]
TcpRouteUnionTypeDef = Union[TcpRouteTypeDef, TcpRouteOutputTypeDef]


class LoggingOutputTypeDef(TypedDict):
    accessLog: NotRequired[AccessLogOutputTypeDef]


class VirtualGatewayLoggingOutputTypeDef(TypedDict):
    accessLog: NotRequired[VirtualGatewayAccessLogOutputTypeDef]


FileAccessLogUnionTypeDef = Union[FileAccessLogTypeDef, FileAccessLogOutputTypeDef]
VirtualGatewayFileAccessLogUnionTypeDef = Union[
    VirtualGatewayFileAccessLogTypeDef, VirtualGatewayFileAccessLogOutputTypeDef
]


class CreateVirtualRouterOutputTypeDef(TypedDict):
    virtualRouter: VirtualRouterDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVirtualRouterOutputTypeDef(TypedDict):
    virtualRouter: VirtualRouterDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVirtualRouterOutputTypeDef(TypedDict):
    virtualRouter: VirtualRouterDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateVirtualRouterOutputTypeDef(TypedDict):
    virtualRouter: VirtualRouterDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListenerOutputTypeDef(TypedDict):
    portMapping: PortMappingTypeDef
    connectionPool: NotRequired[VirtualNodeConnectionPoolTypeDef]
    healthCheck: NotRequired[HealthCheckPolicyTypeDef]
    outlierDetection: NotRequired[OutlierDetectionTypeDef]
    timeout: NotRequired[ListenerTimeoutTypeDef]
    tls: NotRequired[ListenerTlsOutputTypeDef]


class ListenerTlsValidationContextTypeDef(TypedDict):
    trust: ListenerTlsValidationContextTrustTypeDef
    subjectAlternativeNames: NotRequired[SubjectAlternativeNamesUnionTypeDef]


class VirtualGatewayListenerTlsValidationContextTypeDef(TypedDict):
    trust: VirtualGatewayListenerTlsValidationContextTrustTypeDef
    subjectAlternativeNames: NotRequired[SubjectAlternativeNamesUnionTypeDef]


class ClientPolicyOutputTypeDef(TypedDict):
    tls: NotRequired[ClientPolicyTlsOutputTypeDef]


class TlsValidationContextTypeDef(TypedDict):
    trust: TlsValidationContextTrustUnionTypeDef
    subjectAlternativeNames: NotRequired[SubjectAlternativeNamesUnionTypeDef]


class VirtualGatewayListenerOutputTypeDef(TypedDict):
    portMapping: VirtualGatewayPortMappingTypeDef
    connectionPool: NotRequired[VirtualGatewayConnectionPoolTypeDef]
    healthCheck: NotRequired[VirtualGatewayHealthCheckPolicyTypeDef]
    tls: NotRequired[VirtualGatewayListenerTlsOutputTypeDef]


class VirtualGatewayClientPolicyOutputTypeDef(TypedDict):
    tls: NotRequired[VirtualGatewayClientPolicyTlsOutputTypeDef]


class VirtualGatewayTlsValidationContextTypeDef(TypedDict):
    trust: VirtualGatewayTlsValidationContextTrustUnionTypeDef
    subjectAlternativeNames: NotRequired[SubjectAlternativeNamesUnionTypeDef]


class CreateVirtualServiceOutputTypeDef(TypedDict):
    virtualService: VirtualServiceDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVirtualServiceOutputTypeDef(TypedDict):
    virtualService: VirtualServiceDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVirtualServiceOutputTypeDef(TypedDict):
    virtualService: VirtualServiceDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateVirtualServiceOutputTypeDef(TypedDict):
    virtualService: VirtualServiceDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GrpcGatewayRouteTypeDef(TypedDict):
    action: GrpcGatewayRouteActionTypeDef
    match: GrpcGatewayRouteMatchUnionTypeDef


class GrpcRouteTypeDef(TypedDict):
    action: GrpcRouteActionUnionTypeDef
    match: GrpcRouteMatchUnionTypeDef
    retryPolicy: NotRequired[GrpcRetryPolicyUnionTypeDef]
    timeout: NotRequired[GrpcTimeoutTypeDef]


class GatewayRouteSpecOutputTypeDef(TypedDict):
    grpcRoute: NotRequired[GrpcGatewayRouteOutputTypeDef]
    http2Route: NotRequired[HttpGatewayRouteOutputTypeDef]
    httpRoute: NotRequired[HttpGatewayRouteOutputTypeDef]
    priority: NotRequired[int]


class HttpGatewayRouteTypeDef(TypedDict):
    action: HttpGatewayRouteActionTypeDef
    match: HttpGatewayRouteMatchUnionTypeDef


class RouteSpecOutputTypeDef(TypedDict):
    grpcRoute: NotRequired[GrpcRouteOutputTypeDef]
    http2Route: NotRequired[HttpRouteOutputTypeDef]
    httpRoute: NotRequired[HttpRouteOutputTypeDef]
    priority: NotRequired[int]
    tcpRoute: NotRequired[TcpRouteOutputTypeDef]


class HttpRouteTypeDef(TypedDict):
    action: HttpRouteActionUnionTypeDef
    match: HttpRouteMatchUnionTypeDef
    retryPolicy: NotRequired[HttpRetryPolicyUnionTypeDef]
    timeout: NotRequired[HttpTimeoutTypeDef]


class AccessLogTypeDef(TypedDict):
    file: NotRequired[FileAccessLogUnionTypeDef]


class VirtualGatewayAccessLogTypeDef(TypedDict):
    file: NotRequired[VirtualGatewayFileAccessLogUnionTypeDef]


ListenerTlsValidationContextUnionTypeDef = Union[
    ListenerTlsValidationContextTypeDef, ListenerTlsValidationContextOutputTypeDef
]
VirtualGatewayListenerTlsValidationContextUnionTypeDef = Union[
    VirtualGatewayListenerTlsValidationContextTypeDef,
    VirtualGatewayListenerTlsValidationContextOutputTypeDef,
]


class BackendDefaultsOutputTypeDef(TypedDict):
    clientPolicy: NotRequired[ClientPolicyOutputTypeDef]


class VirtualServiceBackendOutputTypeDef(TypedDict):
    virtualServiceName: str
    clientPolicy: NotRequired[ClientPolicyOutputTypeDef]


TlsValidationContextUnionTypeDef = Union[
    TlsValidationContextTypeDef, TlsValidationContextOutputTypeDef
]


class VirtualGatewayBackendDefaultsOutputTypeDef(TypedDict):
    clientPolicy: NotRequired[VirtualGatewayClientPolicyOutputTypeDef]


VirtualGatewayTlsValidationContextUnionTypeDef = Union[
    VirtualGatewayTlsValidationContextTypeDef, VirtualGatewayTlsValidationContextOutputTypeDef
]
GrpcGatewayRouteUnionTypeDef = Union[GrpcGatewayRouteTypeDef, GrpcGatewayRouteOutputTypeDef]
GrpcRouteUnionTypeDef = Union[GrpcRouteTypeDef, GrpcRouteOutputTypeDef]


class GatewayRouteDataTypeDef(TypedDict):
    gatewayRouteName: str
    meshName: str
    metadata: ResourceMetadataTypeDef
    spec: GatewayRouteSpecOutputTypeDef
    status: GatewayRouteStatusTypeDef
    virtualGatewayName: str


HttpGatewayRouteUnionTypeDef = Union[HttpGatewayRouteTypeDef, HttpGatewayRouteOutputTypeDef]


class RouteDataTypeDef(TypedDict):
    meshName: str
    metadata: ResourceMetadataTypeDef
    routeName: str
    spec: RouteSpecOutputTypeDef
    status: RouteStatusTypeDef
    virtualRouterName: str


HttpRouteUnionTypeDef = Union[HttpRouteTypeDef, HttpRouteOutputTypeDef]
AccessLogUnionTypeDef = Union[AccessLogTypeDef, AccessLogOutputTypeDef]
VirtualGatewayAccessLogUnionTypeDef = Union[
    VirtualGatewayAccessLogTypeDef, VirtualGatewayAccessLogOutputTypeDef
]


class ListenerTlsTypeDef(TypedDict):
    certificate: ListenerTlsCertificateTypeDef
    mode: ListenerTlsModeType
    validation: NotRequired[ListenerTlsValidationContextUnionTypeDef]


class VirtualGatewayListenerTlsTypeDef(TypedDict):
    certificate: VirtualGatewayListenerTlsCertificateTypeDef
    mode: VirtualGatewayListenerTlsModeType
    validation: NotRequired[VirtualGatewayListenerTlsValidationContextUnionTypeDef]


class BackendOutputTypeDef(TypedDict):
    virtualService: NotRequired[VirtualServiceBackendOutputTypeDef]


class ClientPolicyTlsTypeDef(TypedDict):
    validation: TlsValidationContextUnionTypeDef
    certificate: NotRequired[ClientTlsCertificateTypeDef]
    enforce: NotRequired[bool]
    ports: NotRequired[Sequence[int]]


class VirtualGatewaySpecOutputTypeDef(TypedDict):
    listeners: List[VirtualGatewayListenerOutputTypeDef]
    backendDefaults: NotRequired[VirtualGatewayBackendDefaultsOutputTypeDef]
    logging: NotRequired[VirtualGatewayLoggingOutputTypeDef]


class VirtualGatewayClientPolicyTlsTypeDef(TypedDict):
    validation: VirtualGatewayTlsValidationContextUnionTypeDef
    certificate: NotRequired[VirtualGatewayClientTlsCertificateTypeDef]
    enforce: NotRequired[bool]
    ports: NotRequired[Sequence[int]]


class CreateGatewayRouteOutputTypeDef(TypedDict):
    gatewayRoute: GatewayRouteDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteGatewayRouteOutputTypeDef(TypedDict):
    gatewayRoute: GatewayRouteDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGatewayRouteOutputTypeDef(TypedDict):
    gatewayRoute: GatewayRouteDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateGatewayRouteOutputTypeDef(TypedDict):
    gatewayRoute: GatewayRouteDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GatewayRouteSpecTypeDef(TypedDict):
    grpcRoute: NotRequired[GrpcGatewayRouteUnionTypeDef]
    http2Route: NotRequired[HttpGatewayRouteUnionTypeDef]
    httpRoute: NotRequired[HttpGatewayRouteUnionTypeDef]
    priority: NotRequired[int]


class CreateRouteOutputTypeDef(TypedDict):
    route: RouteDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRouteOutputTypeDef(TypedDict):
    route: RouteDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRouteOutputTypeDef(TypedDict):
    route: RouteDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRouteOutputTypeDef(TypedDict):
    route: RouteDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RouteSpecTypeDef(TypedDict):
    grpcRoute: NotRequired[GrpcRouteUnionTypeDef]
    http2Route: NotRequired[HttpRouteUnionTypeDef]
    httpRoute: NotRequired[HttpRouteUnionTypeDef]
    priority: NotRequired[int]
    tcpRoute: NotRequired[TcpRouteUnionTypeDef]


class LoggingTypeDef(TypedDict):
    accessLog: NotRequired[AccessLogUnionTypeDef]


class VirtualGatewayLoggingTypeDef(TypedDict):
    accessLog: NotRequired[VirtualGatewayAccessLogUnionTypeDef]


ListenerTlsUnionTypeDef = Union[ListenerTlsTypeDef, ListenerTlsOutputTypeDef]
VirtualGatewayListenerTlsUnionTypeDef = Union[
    VirtualGatewayListenerTlsTypeDef, VirtualGatewayListenerTlsOutputTypeDef
]


class VirtualNodeSpecOutputTypeDef(TypedDict):
    backendDefaults: NotRequired[BackendDefaultsOutputTypeDef]
    backends: NotRequired[List[BackendOutputTypeDef]]
    listeners: NotRequired[List[ListenerOutputTypeDef]]
    logging: NotRequired[LoggingOutputTypeDef]
    serviceDiscovery: NotRequired[ServiceDiscoveryOutputTypeDef]


ClientPolicyTlsUnionTypeDef = Union[ClientPolicyTlsTypeDef, ClientPolicyTlsOutputTypeDef]


class VirtualGatewayDataTypeDef(TypedDict):
    meshName: str
    metadata: ResourceMetadataTypeDef
    spec: VirtualGatewaySpecOutputTypeDef
    status: VirtualGatewayStatusTypeDef
    virtualGatewayName: str


VirtualGatewayClientPolicyTlsUnionTypeDef = Union[
    VirtualGatewayClientPolicyTlsTypeDef, VirtualGatewayClientPolicyTlsOutputTypeDef
]


class CreateGatewayRouteInputRequestTypeDef(TypedDict):
    gatewayRouteName: str
    meshName: str
    spec: GatewayRouteSpecTypeDef
    virtualGatewayName: str
    clientToken: NotRequired[str]
    meshOwner: NotRequired[str]
    tags: NotRequired[Sequence[TagRefTypeDef]]


class UpdateGatewayRouteInputRequestTypeDef(TypedDict):
    gatewayRouteName: str
    meshName: str
    spec: GatewayRouteSpecTypeDef
    virtualGatewayName: str
    clientToken: NotRequired[str]
    meshOwner: NotRequired[str]


class CreateRouteInputRequestTypeDef(TypedDict):
    meshName: str
    routeName: str
    spec: RouteSpecTypeDef
    virtualRouterName: str
    clientToken: NotRequired[str]
    meshOwner: NotRequired[str]
    tags: NotRequired[Sequence[TagRefTypeDef]]


class UpdateRouteInputRequestTypeDef(TypedDict):
    meshName: str
    routeName: str
    spec: RouteSpecTypeDef
    virtualRouterName: str
    clientToken: NotRequired[str]
    meshOwner: NotRequired[str]


LoggingUnionTypeDef = Union[LoggingTypeDef, LoggingOutputTypeDef]
VirtualGatewayLoggingUnionTypeDef = Union[
    VirtualGatewayLoggingTypeDef, VirtualGatewayLoggingOutputTypeDef
]


class ListenerTypeDef(TypedDict):
    portMapping: PortMappingTypeDef
    connectionPool: NotRequired[VirtualNodeConnectionPoolTypeDef]
    healthCheck: NotRequired[HealthCheckPolicyTypeDef]
    outlierDetection: NotRequired[OutlierDetectionTypeDef]
    timeout: NotRequired[ListenerTimeoutTypeDef]
    tls: NotRequired[ListenerTlsUnionTypeDef]


class VirtualGatewayListenerTypeDef(TypedDict):
    portMapping: VirtualGatewayPortMappingTypeDef
    connectionPool: NotRequired[VirtualGatewayConnectionPoolTypeDef]
    healthCheck: NotRequired[VirtualGatewayHealthCheckPolicyTypeDef]
    tls: NotRequired[VirtualGatewayListenerTlsUnionTypeDef]


class VirtualNodeDataTypeDef(TypedDict):
    meshName: str
    metadata: ResourceMetadataTypeDef
    spec: VirtualNodeSpecOutputTypeDef
    status: VirtualNodeStatusTypeDef
    virtualNodeName: str


class ClientPolicyTypeDef(TypedDict):
    tls: NotRequired[ClientPolicyTlsUnionTypeDef]


class CreateVirtualGatewayOutputTypeDef(TypedDict):
    virtualGateway: VirtualGatewayDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVirtualGatewayOutputTypeDef(TypedDict):
    virtualGateway: VirtualGatewayDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVirtualGatewayOutputTypeDef(TypedDict):
    virtualGateway: VirtualGatewayDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateVirtualGatewayOutputTypeDef(TypedDict):
    virtualGateway: VirtualGatewayDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class VirtualGatewayClientPolicyTypeDef(TypedDict):
    tls: NotRequired[VirtualGatewayClientPolicyTlsUnionTypeDef]


ListenerUnionTypeDef = Union[ListenerTypeDef, ListenerOutputTypeDef]
VirtualGatewayListenerUnionTypeDef = Union[
    VirtualGatewayListenerTypeDef, VirtualGatewayListenerOutputTypeDef
]


class CreateVirtualNodeOutputTypeDef(TypedDict):
    virtualNode: VirtualNodeDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVirtualNodeOutputTypeDef(TypedDict):
    virtualNode: VirtualNodeDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVirtualNodeOutputTypeDef(TypedDict):
    virtualNode: VirtualNodeDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateVirtualNodeOutputTypeDef(TypedDict):
    virtualNode: VirtualNodeDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ClientPolicyUnionTypeDef = Union[ClientPolicyTypeDef, ClientPolicyOutputTypeDef]
VirtualGatewayClientPolicyUnionTypeDef = Union[
    VirtualGatewayClientPolicyTypeDef, VirtualGatewayClientPolicyOutputTypeDef
]


class BackendDefaultsTypeDef(TypedDict):
    clientPolicy: NotRequired[ClientPolicyUnionTypeDef]


class VirtualServiceBackendTypeDef(TypedDict):
    virtualServiceName: str
    clientPolicy: NotRequired[ClientPolicyUnionTypeDef]


class VirtualGatewayBackendDefaultsTypeDef(TypedDict):
    clientPolicy: NotRequired[VirtualGatewayClientPolicyUnionTypeDef]


BackendDefaultsUnionTypeDef = Union[BackendDefaultsTypeDef, BackendDefaultsOutputTypeDef]
VirtualServiceBackendUnionTypeDef = Union[
    VirtualServiceBackendTypeDef, VirtualServiceBackendOutputTypeDef
]
VirtualGatewayBackendDefaultsUnionTypeDef = Union[
    VirtualGatewayBackendDefaultsTypeDef, VirtualGatewayBackendDefaultsOutputTypeDef
]


class BackendTypeDef(TypedDict):
    virtualService: NotRequired[VirtualServiceBackendUnionTypeDef]


class VirtualGatewaySpecTypeDef(TypedDict):
    listeners: Sequence[VirtualGatewayListenerUnionTypeDef]
    backendDefaults: NotRequired[VirtualGatewayBackendDefaultsUnionTypeDef]
    logging: NotRequired[VirtualGatewayLoggingUnionTypeDef]


BackendUnionTypeDef = Union[BackendTypeDef, BackendOutputTypeDef]


class CreateVirtualGatewayInputRequestTypeDef(TypedDict):
    meshName: str
    spec: VirtualGatewaySpecTypeDef
    virtualGatewayName: str
    clientToken: NotRequired[str]
    meshOwner: NotRequired[str]
    tags: NotRequired[Sequence[TagRefTypeDef]]


class UpdateVirtualGatewayInputRequestTypeDef(TypedDict):
    meshName: str
    spec: VirtualGatewaySpecTypeDef
    virtualGatewayName: str
    clientToken: NotRequired[str]
    meshOwner: NotRequired[str]


class VirtualNodeSpecTypeDef(TypedDict):
    backendDefaults: NotRequired[BackendDefaultsUnionTypeDef]
    backends: NotRequired[Sequence[BackendUnionTypeDef]]
    listeners: NotRequired[Sequence[ListenerUnionTypeDef]]
    logging: NotRequired[LoggingUnionTypeDef]
    serviceDiscovery: NotRequired[ServiceDiscoveryUnionTypeDef]


class CreateVirtualNodeInputRequestTypeDef(TypedDict):
    meshName: str
    spec: VirtualNodeSpecTypeDef
    virtualNodeName: str
    clientToken: NotRequired[str]
    meshOwner: NotRequired[str]
    tags: NotRequired[Sequence[TagRefTypeDef]]


class UpdateVirtualNodeInputRequestTypeDef(TypedDict):
    meshName: str
    spec: VirtualNodeSpecTypeDef
    virtualNodeName: str
    clientToken: NotRequired[str]
    meshOwner: NotRequired[str]
