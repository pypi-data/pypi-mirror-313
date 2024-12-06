"""
Type annotations for codeartifact service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/type_defs/)

Usage::

    ```python
    from mypy_boto3_codeartifact.type_defs import AssetSummaryTypeDef

    data: AssetSummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AllowPublishType,
    AllowUpstreamType,
    DomainStatusType,
    EndpointTypeType,
    HashAlgorithmType,
    PackageFormatType,
    PackageGroupAllowedRepositoryUpdateTypeType,
    PackageGroupAssociationTypeType,
    PackageGroupOriginRestrictionModeType,
    PackageGroupOriginRestrictionTypeType,
    PackageVersionErrorCodeType,
    PackageVersionOriginTypeType,
    PackageVersionStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AssetSummaryTypeDef",
    "AssociateExternalConnectionRequestRequestTypeDef",
    "AssociateExternalConnectionResultTypeDef",
    "AssociatedPackageTypeDef",
    "BlobTypeDef",
    "CopyPackageVersionsRequestRequestTypeDef",
    "CopyPackageVersionsResultTypeDef",
    "CreateDomainRequestRequestTypeDef",
    "CreateDomainResultTypeDef",
    "CreatePackageGroupRequestRequestTypeDef",
    "CreatePackageGroupResultTypeDef",
    "CreateRepositoryRequestRequestTypeDef",
    "CreateRepositoryResultTypeDef",
    "DeleteDomainPermissionsPolicyRequestRequestTypeDef",
    "DeleteDomainPermissionsPolicyResultTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DeleteDomainResultTypeDef",
    "DeletePackageGroupRequestRequestTypeDef",
    "DeletePackageGroupResultTypeDef",
    "DeletePackageRequestRequestTypeDef",
    "DeletePackageResultTypeDef",
    "DeletePackageVersionsRequestRequestTypeDef",
    "DeletePackageVersionsResultTypeDef",
    "DeleteRepositoryPermissionsPolicyRequestRequestTypeDef",
    "DeleteRepositoryPermissionsPolicyResultTypeDef",
    "DeleteRepositoryRequestRequestTypeDef",
    "DeleteRepositoryResultTypeDef",
    "DescribeDomainRequestRequestTypeDef",
    "DescribeDomainResultTypeDef",
    "DescribePackageGroupRequestRequestTypeDef",
    "DescribePackageGroupResultTypeDef",
    "DescribePackageRequestRequestTypeDef",
    "DescribePackageResultTypeDef",
    "DescribePackageVersionRequestRequestTypeDef",
    "DescribePackageVersionResultTypeDef",
    "DescribeRepositoryRequestRequestTypeDef",
    "DescribeRepositoryResultTypeDef",
    "DisassociateExternalConnectionRequestRequestTypeDef",
    "DisassociateExternalConnectionResultTypeDef",
    "DisposePackageVersionsRequestRequestTypeDef",
    "DisposePackageVersionsResultTypeDef",
    "DomainDescriptionTypeDef",
    "DomainEntryPointTypeDef",
    "DomainSummaryTypeDef",
    "GetAssociatedPackageGroupRequestRequestTypeDef",
    "GetAssociatedPackageGroupResultTypeDef",
    "GetAuthorizationTokenRequestRequestTypeDef",
    "GetAuthorizationTokenResultTypeDef",
    "GetDomainPermissionsPolicyRequestRequestTypeDef",
    "GetDomainPermissionsPolicyResultTypeDef",
    "GetPackageVersionAssetRequestRequestTypeDef",
    "GetPackageVersionAssetResultTypeDef",
    "GetPackageVersionReadmeRequestRequestTypeDef",
    "GetPackageVersionReadmeResultTypeDef",
    "GetRepositoryEndpointRequestRequestTypeDef",
    "GetRepositoryEndpointResultTypeDef",
    "GetRepositoryPermissionsPolicyRequestRequestTypeDef",
    "GetRepositoryPermissionsPolicyResultTypeDef",
    "LicenseInfoTypeDef",
    "ListAllowedRepositoriesForGroupRequestListAllowedRepositoriesForGroupPaginateTypeDef",
    "ListAllowedRepositoriesForGroupRequestRequestTypeDef",
    "ListAllowedRepositoriesForGroupResultTypeDef",
    "ListAssociatedPackagesRequestListAssociatedPackagesPaginateTypeDef",
    "ListAssociatedPackagesRequestRequestTypeDef",
    "ListAssociatedPackagesResultTypeDef",
    "ListDomainsRequestListDomainsPaginateTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListDomainsResultTypeDef",
    "ListPackageGroupsRequestListPackageGroupsPaginateTypeDef",
    "ListPackageGroupsRequestRequestTypeDef",
    "ListPackageGroupsResultTypeDef",
    "ListPackageVersionAssetsRequestListPackageVersionAssetsPaginateTypeDef",
    "ListPackageVersionAssetsRequestRequestTypeDef",
    "ListPackageVersionAssetsResultTypeDef",
    "ListPackageVersionDependenciesRequestRequestTypeDef",
    "ListPackageVersionDependenciesResultTypeDef",
    "ListPackageVersionsRequestListPackageVersionsPaginateTypeDef",
    "ListPackageVersionsRequestRequestTypeDef",
    "ListPackageVersionsResultTypeDef",
    "ListPackagesRequestListPackagesPaginateTypeDef",
    "ListPackagesRequestRequestTypeDef",
    "ListPackagesResultTypeDef",
    "ListRepositoriesInDomainRequestListRepositoriesInDomainPaginateTypeDef",
    "ListRepositoriesInDomainRequestRequestTypeDef",
    "ListRepositoriesInDomainResultTypeDef",
    "ListRepositoriesRequestListRepositoriesPaginateTypeDef",
    "ListRepositoriesRequestRequestTypeDef",
    "ListRepositoriesResultTypeDef",
    "ListSubPackageGroupsRequestListSubPackageGroupsPaginateTypeDef",
    "ListSubPackageGroupsRequestRequestTypeDef",
    "ListSubPackageGroupsResultTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResultTypeDef",
    "PackageDependencyTypeDef",
    "PackageDescriptionTypeDef",
    "PackageGroupAllowedRepositoryTypeDef",
    "PackageGroupDescriptionTypeDef",
    "PackageGroupOriginConfigurationTypeDef",
    "PackageGroupOriginRestrictionTypeDef",
    "PackageGroupReferenceTypeDef",
    "PackageGroupSummaryTypeDef",
    "PackageOriginConfigurationTypeDef",
    "PackageOriginRestrictionsTypeDef",
    "PackageSummaryTypeDef",
    "PackageVersionDescriptionTypeDef",
    "PackageVersionErrorTypeDef",
    "PackageVersionOriginTypeDef",
    "PackageVersionSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "PublishPackageVersionRequestRequestTypeDef",
    "PublishPackageVersionResultTypeDef",
    "PutDomainPermissionsPolicyRequestRequestTypeDef",
    "PutDomainPermissionsPolicyResultTypeDef",
    "PutPackageOriginConfigurationRequestRequestTypeDef",
    "PutPackageOriginConfigurationResultTypeDef",
    "PutRepositoryPermissionsPolicyRequestRequestTypeDef",
    "PutRepositoryPermissionsPolicyResultTypeDef",
    "RepositoryDescriptionTypeDef",
    "RepositoryExternalConnectionInfoTypeDef",
    "RepositorySummaryTypeDef",
    "ResourcePolicyTypeDef",
    "ResponseMetadataTypeDef",
    "SuccessfulPackageVersionInfoTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdatePackageGroupOriginConfigurationRequestRequestTypeDef",
    "UpdatePackageGroupOriginConfigurationResultTypeDef",
    "UpdatePackageGroupRequestRequestTypeDef",
    "UpdatePackageGroupResultTypeDef",
    "UpdatePackageVersionsStatusRequestRequestTypeDef",
    "UpdatePackageVersionsStatusResultTypeDef",
    "UpdateRepositoryRequestRequestTypeDef",
    "UpdateRepositoryResultTypeDef",
    "UpstreamRepositoryInfoTypeDef",
    "UpstreamRepositoryTypeDef",
)


class AssetSummaryTypeDef(TypedDict):
    name: str
    size: NotRequired[int]
    hashes: NotRequired[Dict[HashAlgorithmType, str]]


class AssociateExternalConnectionRequestRequestTypeDef(TypedDict):
    domain: str
    repository: str
    externalConnection: str
    domainOwner: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


AssociatedPackageTypeDef = TypedDict(
    "AssociatedPackageTypeDef",
    {
        "format": NotRequired[PackageFormatType],
        "namespace": NotRequired[str],
        "package": NotRequired[str],
        "associationType": NotRequired[PackageGroupAssociationTypeType],
    },
)
BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
CopyPackageVersionsRequestRequestTypeDef = TypedDict(
    "CopyPackageVersionsRequestRequestTypeDef",
    {
        "domain": str,
        "sourceRepository": str,
        "destinationRepository": str,
        "format": PackageFormatType,
        "package": str,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
        "versions": NotRequired[Sequence[str]],
        "versionRevisions": NotRequired[Mapping[str, str]],
        "allowOverwrite": NotRequired[bool],
        "includeFromUpstream": NotRequired[bool],
    },
)


class PackageVersionErrorTypeDef(TypedDict):
    errorCode: NotRequired[PackageVersionErrorCodeType]
    errorMessage: NotRequired[str]


class SuccessfulPackageVersionInfoTypeDef(TypedDict):
    revision: NotRequired[str]
    status: NotRequired[PackageVersionStatusType]


class TagTypeDef(TypedDict):
    key: str
    value: str


class DomainDescriptionTypeDef(TypedDict):
    name: NotRequired[str]
    owner: NotRequired[str]
    arn: NotRequired[str]
    status: NotRequired[DomainStatusType]
    createdTime: NotRequired[datetime]
    encryptionKey: NotRequired[str]
    repositoryCount: NotRequired[int]
    assetSizeBytes: NotRequired[int]
    s3BucketArn: NotRequired[str]


class UpstreamRepositoryTypeDef(TypedDict):
    repositoryName: str


class DeleteDomainPermissionsPolicyRequestRequestTypeDef(TypedDict):
    domain: str
    domainOwner: NotRequired[str]
    policyRevision: NotRequired[str]


class ResourcePolicyTypeDef(TypedDict):
    resourceArn: NotRequired[str]
    revision: NotRequired[str]
    document: NotRequired[str]


class DeleteDomainRequestRequestTypeDef(TypedDict):
    domain: str
    domainOwner: NotRequired[str]


class DeletePackageGroupRequestRequestTypeDef(TypedDict):
    domain: str
    packageGroup: str
    domainOwner: NotRequired[str]


DeletePackageRequestRequestTypeDef = TypedDict(
    "DeletePackageRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
    },
)
DeletePackageVersionsRequestRequestTypeDef = TypedDict(
    "DeletePackageVersionsRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "versions": Sequence[str],
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
        "expectedStatus": NotRequired[PackageVersionStatusType],
    },
)


class DeleteRepositoryPermissionsPolicyRequestRequestTypeDef(TypedDict):
    domain: str
    repository: str
    domainOwner: NotRequired[str]
    policyRevision: NotRequired[str]


class DeleteRepositoryRequestRequestTypeDef(TypedDict):
    domain: str
    repository: str
    domainOwner: NotRequired[str]


class DescribeDomainRequestRequestTypeDef(TypedDict):
    domain: str
    domainOwner: NotRequired[str]


class DescribePackageGroupRequestRequestTypeDef(TypedDict):
    domain: str
    packageGroup: str
    domainOwner: NotRequired[str]


DescribePackageRequestRequestTypeDef = TypedDict(
    "DescribePackageRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
    },
)
DescribePackageVersionRequestRequestTypeDef = TypedDict(
    "DescribePackageVersionRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "packageVersion": str,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
    },
)


class DescribeRepositoryRequestRequestTypeDef(TypedDict):
    domain: str
    repository: str
    domainOwner: NotRequired[str]


class DisassociateExternalConnectionRequestRequestTypeDef(TypedDict):
    domain: str
    repository: str
    externalConnection: str
    domainOwner: NotRequired[str]


DisposePackageVersionsRequestRequestTypeDef = TypedDict(
    "DisposePackageVersionsRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "versions": Sequence[str],
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
        "versionRevisions": NotRequired[Mapping[str, str]],
        "expectedStatus": NotRequired[PackageVersionStatusType],
    },
)


class DomainEntryPointTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    externalConnectionName: NotRequired[str]


class DomainSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    owner: NotRequired[str]
    arn: NotRequired[str]
    status: NotRequired[DomainStatusType]
    createdTime: NotRequired[datetime]
    encryptionKey: NotRequired[str]


GetAssociatedPackageGroupRequestRequestTypeDef = TypedDict(
    "GetAssociatedPackageGroupRequestRequestTypeDef",
    {
        "domain": str,
        "format": PackageFormatType,
        "package": str,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
    },
)


class GetAuthorizationTokenRequestRequestTypeDef(TypedDict):
    domain: str
    domainOwner: NotRequired[str]
    durationSeconds: NotRequired[int]


class GetDomainPermissionsPolicyRequestRequestTypeDef(TypedDict):
    domain: str
    domainOwner: NotRequired[str]


GetPackageVersionAssetRequestRequestTypeDef = TypedDict(
    "GetPackageVersionAssetRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "packageVersion": str,
        "asset": str,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
        "packageVersionRevision": NotRequired[str],
    },
)
GetPackageVersionReadmeRequestRequestTypeDef = TypedDict(
    "GetPackageVersionReadmeRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "packageVersion": str,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
    },
)
GetRepositoryEndpointRequestRequestTypeDef = TypedDict(
    "GetRepositoryEndpointRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "domainOwner": NotRequired[str],
        "endpointType": NotRequired[EndpointTypeType],
    },
)


class GetRepositoryPermissionsPolicyRequestRequestTypeDef(TypedDict):
    domain: str
    repository: str
    domainOwner: NotRequired[str]


class LicenseInfoTypeDef(TypedDict):
    name: NotRequired[str]
    url: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAllowedRepositoriesForGroupRequestRequestTypeDef(TypedDict):
    domain: str
    packageGroup: str
    originRestrictionType: PackageGroupOriginRestrictionTypeType
    domainOwner: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListAssociatedPackagesRequestRequestTypeDef(TypedDict):
    domain: str
    packageGroup: str
    domainOwner: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    preview: NotRequired[bool]


class ListDomainsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListPackageGroupsRequestRequestTypeDef(TypedDict):
    domain: str
    domainOwner: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    prefix: NotRequired[str]


ListPackageVersionAssetsRequestRequestTypeDef = TypedDict(
    "ListPackageVersionAssetsRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "packageVersion": str,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListPackageVersionDependenciesRequestRequestTypeDef = TypedDict(
    "ListPackageVersionDependenciesRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "packageVersion": str,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
        "nextToken": NotRequired[str],
    },
)


class PackageDependencyTypeDef(TypedDict):
    namespace: NotRequired[str]
    package: NotRequired[str]
    dependencyType: NotRequired[str]
    versionRequirement: NotRequired[str]


ListPackageVersionsRequestRequestTypeDef = TypedDict(
    "ListPackageVersionsRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
        "status": NotRequired[PackageVersionStatusType],
        "sortBy": NotRequired[Literal["PUBLISHED_TIME"]],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "originType": NotRequired[PackageVersionOriginTypeType],
    },
)
ListPackagesRequestRequestTypeDef = TypedDict(
    "ListPackagesRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "domainOwner": NotRequired[str],
        "format": NotRequired[PackageFormatType],
        "namespace": NotRequired[str],
        "packagePrefix": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "publish": NotRequired[AllowPublishType],
        "upstream": NotRequired[AllowUpstreamType],
    },
)


class ListRepositoriesInDomainRequestRequestTypeDef(TypedDict):
    domain: str
    domainOwner: NotRequired[str]
    administratorAccount: NotRequired[str]
    repositoryPrefix: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class RepositorySummaryTypeDef(TypedDict):
    name: NotRequired[str]
    administratorAccount: NotRequired[str]
    domainName: NotRequired[str]
    domainOwner: NotRequired[str]
    arn: NotRequired[str]
    description: NotRequired[str]
    createdTime: NotRequired[datetime]


class ListRepositoriesRequestRequestTypeDef(TypedDict):
    repositoryPrefix: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListSubPackageGroupsRequestRequestTypeDef(TypedDict):
    domain: str
    packageGroup: str
    domainOwner: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class PackageGroupAllowedRepositoryTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    originRestrictionType: NotRequired[PackageGroupOriginRestrictionTypeType]


class PackageGroupReferenceTypeDef(TypedDict):
    arn: NotRequired[str]
    pattern: NotRequired[str]


class PackageOriginRestrictionsTypeDef(TypedDict):
    publish: AllowPublishType
    upstream: AllowUpstreamType


class PutDomainPermissionsPolicyRequestRequestTypeDef(TypedDict):
    domain: str
    policyDocument: str
    domainOwner: NotRequired[str]
    policyRevision: NotRequired[str]


class PutRepositoryPermissionsPolicyRequestRequestTypeDef(TypedDict):
    domain: str
    repository: str
    policyDocument: str
    domainOwner: NotRequired[str]
    policyRevision: NotRequired[str]


class RepositoryExternalConnectionInfoTypeDef(TypedDict):
    externalConnectionName: NotRequired[str]
    packageFormat: NotRequired[PackageFormatType]
    status: NotRequired[Literal["Available"]]


class UpstreamRepositoryInfoTypeDef(TypedDict):
    repositoryName: NotRequired[str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdatePackageGroupRequestRequestTypeDef(TypedDict):
    domain: str
    packageGroup: str
    domainOwner: NotRequired[str]
    contactInfo: NotRequired[str]
    description: NotRequired[str]


UpdatePackageVersionsStatusRequestRequestTypeDef = TypedDict(
    "UpdatePackageVersionsStatusRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "versions": Sequence[str],
        "targetStatus": PackageVersionStatusType,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
        "versionRevisions": NotRequired[Mapping[str, str]],
        "expectedStatus": NotRequired[PackageVersionStatusType],
    },
)


class GetAuthorizationTokenResultTypeDef(TypedDict):
    authorizationToken: str
    expiration: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetPackageVersionAssetResultTypeDef(TypedDict):
    asset: StreamingBody
    assetName: str
    packageVersion: str
    packageVersionRevision: str
    ResponseMetadata: ResponseMetadataTypeDef


GetPackageVersionReadmeResultTypeDef = TypedDict(
    "GetPackageVersionReadmeResultTypeDef",
    {
        "format": PackageFormatType,
        "namespace": str,
        "package": str,
        "version": str,
        "versionRevision": str,
        "readme": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class GetRepositoryEndpointResultTypeDef(TypedDict):
    repositoryEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListAllowedRepositoriesForGroupResultTypeDef(TypedDict):
    allowedRepositories: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


ListPackageVersionAssetsResultTypeDef = TypedDict(
    "ListPackageVersionAssetsResultTypeDef",
    {
        "format": PackageFormatType,
        "namespace": str,
        "package": str,
        "version": str,
        "versionRevision": str,
        "assets": List[AssetSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
PublishPackageVersionResultTypeDef = TypedDict(
    "PublishPackageVersionResultTypeDef",
    {
        "format": PackageFormatType,
        "namespace": str,
        "package": str,
        "version": str,
        "versionRevision": str,
        "status": PackageVersionStatusType,
        "asset": AssetSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListAssociatedPackagesResultTypeDef(TypedDict):
    packages: List[AssociatedPackageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


PublishPackageVersionRequestRequestTypeDef = TypedDict(
    "PublishPackageVersionRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "packageVersion": str,
        "assetContent": BlobTypeDef,
        "assetName": str,
        "assetSHA256": str,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
        "unfinished": NotRequired[bool],
    },
)


class CopyPackageVersionsResultTypeDef(TypedDict):
    successfulVersions: Dict[str, SuccessfulPackageVersionInfoTypeDef]
    failedVersions: Dict[str, PackageVersionErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePackageVersionsResultTypeDef(TypedDict):
    successfulVersions: Dict[str, SuccessfulPackageVersionInfoTypeDef]
    failedVersions: Dict[str, PackageVersionErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DisposePackageVersionsResultTypeDef(TypedDict):
    successfulVersions: Dict[str, SuccessfulPackageVersionInfoTypeDef]
    failedVersions: Dict[str, PackageVersionErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePackageVersionsStatusResultTypeDef(TypedDict):
    successfulVersions: Dict[str, SuccessfulPackageVersionInfoTypeDef]
    failedVersions: Dict[str, PackageVersionErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDomainRequestRequestTypeDef(TypedDict):
    domain: str
    encryptionKey: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreatePackageGroupRequestRequestTypeDef(TypedDict):
    domain: str
    packageGroup: str
    domainOwner: NotRequired[str]
    contactInfo: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class ListTagsForResourceResultTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]


class CreateDomainResultTypeDef(TypedDict):
    domain: DomainDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDomainResultTypeDef(TypedDict):
    domain: DomainDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDomainResultTypeDef(TypedDict):
    domain: DomainDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRepositoryRequestRequestTypeDef(TypedDict):
    domain: str
    repository: str
    domainOwner: NotRequired[str]
    description: NotRequired[str]
    upstreams: NotRequired[Sequence[UpstreamRepositoryTypeDef]]
    tags: NotRequired[Sequence[TagTypeDef]]


class UpdateRepositoryRequestRequestTypeDef(TypedDict):
    domain: str
    repository: str
    domainOwner: NotRequired[str]
    description: NotRequired[str]
    upstreams: NotRequired[Sequence[UpstreamRepositoryTypeDef]]


class DeleteDomainPermissionsPolicyResultTypeDef(TypedDict):
    policy: ResourcePolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRepositoryPermissionsPolicyResultTypeDef(TypedDict):
    policy: ResourcePolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDomainPermissionsPolicyResultTypeDef(TypedDict):
    policy: ResourcePolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetRepositoryPermissionsPolicyResultTypeDef(TypedDict):
    policy: ResourcePolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutDomainPermissionsPolicyResultTypeDef(TypedDict):
    policy: ResourcePolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutRepositoryPermissionsPolicyResultTypeDef(TypedDict):
    policy: ResourcePolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PackageVersionOriginTypeDef(TypedDict):
    domainEntryPoint: NotRequired[DomainEntryPointTypeDef]
    originType: NotRequired[PackageVersionOriginTypeType]


class ListDomainsResultTypeDef(TypedDict):
    domains: List[DomainSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAllowedRepositoriesForGroupRequestListAllowedRepositoriesForGroupPaginateTypeDef(
    TypedDict
):
    domain: str
    packageGroup: str
    originRestrictionType: PackageGroupOriginRestrictionTypeType
    domainOwner: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssociatedPackagesRequestListAssociatedPackagesPaginateTypeDef(TypedDict):
    domain: str
    packageGroup: str
    domainOwner: NotRequired[str]
    preview: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDomainsRequestListDomainsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPackageGroupsRequestListPackageGroupsPaginateTypeDef(TypedDict):
    domain: str
    domainOwner: NotRequired[str]
    prefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListPackageVersionAssetsRequestListPackageVersionAssetsPaginateTypeDef = TypedDict(
    "ListPackageVersionAssetsRequestListPackageVersionAssetsPaginateTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "packageVersion": str,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListPackageVersionsRequestListPackageVersionsPaginateTypeDef = TypedDict(
    "ListPackageVersionsRequestListPackageVersionsPaginateTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
        "status": NotRequired[PackageVersionStatusType],
        "sortBy": NotRequired[Literal["PUBLISHED_TIME"]],
        "originType": NotRequired[PackageVersionOriginTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListPackagesRequestListPackagesPaginateTypeDef = TypedDict(
    "ListPackagesRequestListPackagesPaginateTypeDef",
    {
        "domain": str,
        "repository": str,
        "domainOwner": NotRequired[str],
        "format": NotRequired[PackageFormatType],
        "namespace": NotRequired[str],
        "packagePrefix": NotRequired[str],
        "publish": NotRequired[AllowPublishType],
        "upstream": NotRequired[AllowUpstreamType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListRepositoriesInDomainRequestListRepositoriesInDomainPaginateTypeDef(TypedDict):
    domain: str
    domainOwner: NotRequired[str]
    administratorAccount: NotRequired[str]
    repositoryPrefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRepositoriesRequestListRepositoriesPaginateTypeDef(TypedDict):
    repositoryPrefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSubPackageGroupsRequestListSubPackageGroupsPaginateTypeDef(TypedDict):
    domain: str
    packageGroup: str
    domainOwner: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListPackageVersionDependenciesResultTypeDef = TypedDict(
    "ListPackageVersionDependenciesResultTypeDef",
    {
        "format": PackageFormatType,
        "namespace": str,
        "package": str,
        "version": str,
        "versionRevision": str,
        "dependencies": List[PackageDependencyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)


class ListRepositoriesInDomainResultTypeDef(TypedDict):
    repositories: List[RepositorySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListRepositoriesResultTypeDef(TypedDict):
    repositories: List[RepositorySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdatePackageGroupOriginConfigurationRequestRequestTypeDef(TypedDict):
    domain: str
    packageGroup: str
    domainOwner: NotRequired[str]
    restrictions: NotRequired[
        Mapping[PackageGroupOriginRestrictionTypeType, PackageGroupOriginRestrictionModeType]
    ]
    addAllowedRepositories: NotRequired[Sequence[PackageGroupAllowedRepositoryTypeDef]]
    removeAllowedRepositories: NotRequired[Sequence[PackageGroupAllowedRepositoryTypeDef]]


class PackageGroupOriginRestrictionTypeDef(TypedDict):
    mode: NotRequired[PackageGroupOriginRestrictionModeType]
    effectiveMode: NotRequired[PackageGroupOriginRestrictionModeType]
    inheritedFrom: NotRequired[PackageGroupReferenceTypeDef]
    repositoriesCount: NotRequired[int]


class PackageOriginConfigurationTypeDef(TypedDict):
    restrictions: NotRequired[PackageOriginRestrictionsTypeDef]


PutPackageOriginConfigurationRequestRequestTypeDef = TypedDict(
    "PutPackageOriginConfigurationRequestRequestTypeDef",
    {
        "domain": str,
        "repository": str,
        "format": PackageFormatType,
        "package": str,
        "restrictions": PackageOriginRestrictionsTypeDef,
        "domainOwner": NotRequired[str],
        "namespace": NotRequired[str],
    },
)


class RepositoryDescriptionTypeDef(TypedDict):
    name: NotRequired[str]
    administratorAccount: NotRequired[str]
    domainName: NotRequired[str]
    domainOwner: NotRequired[str]
    arn: NotRequired[str]
    description: NotRequired[str]
    upstreams: NotRequired[List[UpstreamRepositoryInfoTypeDef]]
    externalConnections: NotRequired[List[RepositoryExternalConnectionInfoTypeDef]]
    createdTime: NotRequired[datetime]


PackageVersionDescriptionTypeDef = TypedDict(
    "PackageVersionDescriptionTypeDef",
    {
        "format": NotRequired[PackageFormatType],
        "namespace": NotRequired[str],
        "packageName": NotRequired[str],
        "displayName": NotRequired[str],
        "version": NotRequired[str],
        "summary": NotRequired[str],
        "homePage": NotRequired[str],
        "sourceCodeRepository": NotRequired[str],
        "publishedTime": NotRequired[datetime],
        "licenses": NotRequired[List[LicenseInfoTypeDef]],
        "revision": NotRequired[str],
        "status": NotRequired[PackageVersionStatusType],
        "origin": NotRequired[PackageVersionOriginTypeDef],
    },
)


class PackageVersionSummaryTypeDef(TypedDict):
    version: str
    status: PackageVersionStatusType
    revision: NotRequired[str]
    origin: NotRequired[PackageVersionOriginTypeDef]


class PackageGroupOriginConfigurationTypeDef(TypedDict):
    restrictions: NotRequired[
        Dict[PackageGroupOriginRestrictionTypeType, PackageGroupOriginRestrictionTypeDef]
    ]


PackageDescriptionTypeDef = TypedDict(
    "PackageDescriptionTypeDef",
    {
        "format": NotRequired[PackageFormatType],
        "namespace": NotRequired[str],
        "name": NotRequired[str],
        "originConfiguration": NotRequired[PackageOriginConfigurationTypeDef],
    },
)
PackageSummaryTypeDef = TypedDict(
    "PackageSummaryTypeDef",
    {
        "format": NotRequired[PackageFormatType],
        "namespace": NotRequired[str],
        "package": NotRequired[str],
        "originConfiguration": NotRequired[PackageOriginConfigurationTypeDef],
    },
)


class PutPackageOriginConfigurationResultTypeDef(TypedDict):
    originConfiguration: PackageOriginConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateExternalConnectionResultTypeDef(TypedDict):
    repository: RepositoryDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRepositoryResultTypeDef(TypedDict):
    repository: RepositoryDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRepositoryResultTypeDef(TypedDict):
    repository: RepositoryDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRepositoryResultTypeDef(TypedDict):
    repository: RepositoryDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateExternalConnectionResultTypeDef(TypedDict):
    repository: RepositoryDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRepositoryResultTypeDef(TypedDict):
    repository: RepositoryDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePackageVersionResultTypeDef(TypedDict):
    packageVersion: PackageVersionDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ListPackageVersionsResultTypeDef = TypedDict(
    "ListPackageVersionsResultTypeDef",
    {
        "defaultDisplayVersion": str,
        "format": PackageFormatType,
        "namespace": str,
        "package": str,
        "versions": List[PackageVersionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)


class PackageGroupDescriptionTypeDef(TypedDict):
    arn: NotRequired[str]
    pattern: NotRequired[str]
    domainName: NotRequired[str]
    domainOwner: NotRequired[str]
    createdTime: NotRequired[datetime]
    contactInfo: NotRequired[str]
    description: NotRequired[str]
    originConfiguration: NotRequired[PackageGroupOriginConfigurationTypeDef]
    parent: NotRequired[PackageGroupReferenceTypeDef]


class PackageGroupSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    pattern: NotRequired[str]
    domainName: NotRequired[str]
    domainOwner: NotRequired[str]
    createdTime: NotRequired[datetime]
    contactInfo: NotRequired[str]
    description: NotRequired[str]
    originConfiguration: NotRequired[PackageGroupOriginConfigurationTypeDef]
    parent: NotRequired[PackageGroupReferenceTypeDef]


class DescribePackageResultTypeDef(TypedDict):
    package: PackageDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePackageResultTypeDef(TypedDict):
    deletedPackage: PackageSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListPackagesResultTypeDef(TypedDict):
    packages: List[PackageSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreatePackageGroupResultTypeDef(TypedDict):
    packageGroup: PackageGroupDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePackageGroupResultTypeDef(TypedDict):
    packageGroup: PackageGroupDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePackageGroupResultTypeDef(TypedDict):
    packageGroup: PackageGroupDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssociatedPackageGroupResultTypeDef(TypedDict):
    packageGroup: PackageGroupDescriptionTypeDef
    associationType: PackageGroupAssociationTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePackageGroupOriginConfigurationResultTypeDef(TypedDict):
    packageGroup: PackageGroupDescriptionTypeDef
    allowedRepositoryUpdates: Dict[
        PackageGroupOriginRestrictionTypeType,
        Dict[PackageGroupAllowedRepositoryUpdateTypeType, List[str]],
    ]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePackageGroupResultTypeDef(TypedDict):
    packageGroup: PackageGroupDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListPackageGroupsResultTypeDef(TypedDict):
    packageGroups: List[PackageGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSubPackageGroupsResultTypeDef(TypedDict):
    packageGroups: List[PackageGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
