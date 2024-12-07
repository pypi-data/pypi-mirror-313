"""
Type annotations for ecr-public service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/type_defs/)

Usage::

    ```python
    from mypy_boto3_ecr_public.type_defs import AuthorizationDataTypeDef

    data: AuthorizationDataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ImageFailureCodeType,
    LayerAvailabilityType,
    LayerFailureCodeType,
    RegistryAliasStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AuthorizationDataTypeDef",
    "BatchCheckLayerAvailabilityRequestRequestTypeDef",
    "BatchCheckLayerAvailabilityResponseTypeDef",
    "BatchDeleteImageRequestRequestTypeDef",
    "BatchDeleteImageResponseTypeDef",
    "BlobTypeDef",
    "CompleteLayerUploadRequestRequestTypeDef",
    "CompleteLayerUploadResponseTypeDef",
    "CreateRepositoryRequestRequestTypeDef",
    "CreateRepositoryResponseTypeDef",
    "DeleteRepositoryPolicyRequestRequestTypeDef",
    "DeleteRepositoryPolicyResponseTypeDef",
    "DeleteRepositoryRequestRequestTypeDef",
    "DeleteRepositoryResponseTypeDef",
    "DescribeImageTagsRequestDescribeImageTagsPaginateTypeDef",
    "DescribeImageTagsRequestRequestTypeDef",
    "DescribeImageTagsResponseTypeDef",
    "DescribeImagesRequestDescribeImagesPaginateTypeDef",
    "DescribeImagesRequestRequestTypeDef",
    "DescribeImagesResponseTypeDef",
    "DescribeRegistriesRequestDescribeRegistriesPaginateTypeDef",
    "DescribeRegistriesRequestRequestTypeDef",
    "DescribeRegistriesResponseTypeDef",
    "DescribeRepositoriesRequestDescribeRepositoriesPaginateTypeDef",
    "DescribeRepositoriesRequestRequestTypeDef",
    "DescribeRepositoriesResponseTypeDef",
    "GetAuthorizationTokenResponseTypeDef",
    "GetRegistryCatalogDataResponseTypeDef",
    "GetRepositoryCatalogDataRequestRequestTypeDef",
    "GetRepositoryCatalogDataResponseTypeDef",
    "GetRepositoryPolicyRequestRequestTypeDef",
    "GetRepositoryPolicyResponseTypeDef",
    "ImageDetailTypeDef",
    "ImageFailureTypeDef",
    "ImageIdentifierTypeDef",
    "ImageTagDetailTypeDef",
    "ImageTypeDef",
    "InitiateLayerUploadRequestRequestTypeDef",
    "InitiateLayerUploadResponseTypeDef",
    "LayerFailureTypeDef",
    "LayerTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutImageRequestRequestTypeDef",
    "PutImageResponseTypeDef",
    "PutRegistryCatalogDataRequestRequestTypeDef",
    "PutRegistryCatalogDataResponseTypeDef",
    "PutRepositoryCatalogDataRequestRequestTypeDef",
    "PutRepositoryCatalogDataResponseTypeDef",
    "ReferencedImageDetailTypeDef",
    "RegistryAliasTypeDef",
    "RegistryCatalogDataTypeDef",
    "RegistryTypeDef",
    "RepositoryCatalogDataInputTypeDef",
    "RepositoryCatalogDataTypeDef",
    "RepositoryTypeDef",
    "ResponseMetadataTypeDef",
    "SetRepositoryPolicyRequestRequestTypeDef",
    "SetRepositoryPolicyResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UploadLayerPartRequestRequestTypeDef",
    "UploadLayerPartResponseTypeDef",
)


class AuthorizationDataTypeDef(TypedDict):
    authorizationToken: NotRequired[str]
    expiresAt: NotRequired[datetime]


class BatchCheckLayerAvailabilityRequestRequestTypeDef(TypedDict):
    repositoryName: str
    layerDigests: Sequence[str]
    registryId: NotRequired[str]


class LayerFailureTypeDef(TypedDict):
    layerDigest: NotRequired[str]
    failureCode: NotRequired[LayerFailureCodeType]
    failureReason: NotRequired[str]


class LayerTypeDef(TypedDict):
    layerDigest: NotRequired[str]
    layerAvailability: NotRequired[LayerAvailabilityType]
    layerSize: NotRequired[int]
    mediaType: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ImageIdentifierTypeDef(TypedDict):
    imageDigest: NotRequired[str]
    imageTag: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class CompleteLayerUploadRequestRequestTypeDef(TypedDict):
    repositoryName: str
    uploadId: str
    layerDigests: Sequence[str]
    registryId: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class RepositoryCatalogDataTypeDef(TypedDict):
    description: NotRequired[str]
    architectures: NotRequired[List[str]]
    operatingSystems: NotRequired[List[str]]
    logoUrl: NotRequired[str]
    aboutText: NotRequired[str]
    usageText: NotRequired[str]
    marketplaceCertified: NotRequired[bool]


class RepositoryTypeDef(TypedDict):
    repositoryArn: NotRequired[str]
    registryId: NotRequired[str]
    repositoryName: NotRequired[str]
    repositoryUri: NotRequired[str]
    createdAt: NotRequired[datetime]


class DeleteRepositoryPolicyRequestRequestTypeDef(TypedDict):
    repositoryName: str
    registryId: NotRequired[str]


class DeleteRepositoryRequestRequestTypeDef(TypedDict):
    repositoryName: str
    registryId: NotRequired[str]
    force: NotRequired[bool]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeImageTagsRequestRequestTypeDef(TypedDict):
    repositoryName: str
    registryId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ImageDetailTypeDef(TypedDict):
    registryId: NotRequired[str]
    repositoryName: NotRequired[str]
    imageDigest: NotRequired[str]
    imageTags: NotRequired[List[str]]
    imageSizeInBytes: NotRequired[int]
    imagePushedAt: NotRequired[datetime]
    imageManifestMediaType: NotRequired[str]
    artifactMediaType: NotRequired[str]


class DescribeRegistriesRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class DescribeRepositoriesRequestRequestTypeDef(TypedDict):
    registryId: NotRequired[str]
    repositoryNames: NotRequired[Sequence[str]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class RegistryCatalogDataTypeDef(TypedDict):
    displayName: NotRequired[str]


class GetRepositoryCatalogDataRequestRequestTypeDef(TypedDict):
    repositoryName: str
    registryId: NotRequired[str]


class GetRepositoryPolicyRequestRequestTypeDef(TypedDict):
    repositoryName: str
    registryId: NotRequired[str]


class ReferencedImageDetailTypeDef(TypedDict):
    imageDigest: NotRequired[str]
    imageSizeInBytes: NotRequired[int]
    imagePushedAt: NotRequired[datetime]
    imageManifestMediaType: NotRequired[str]
    artifactMediaType: NotRequired[str]


class InitiateLayerUploadRequestRequestTypeDef(TypedDict):
    repositoryName: str
    registryId: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class PutImageRequestRequestTypeDef(TypedDict):
    repositoryName: str
    imageManifest: str
    registryId: NotRequired[str]
    imageManifestMediaType: NotRequired[str]
    imageTag: NotRequired[str]
    imageDigest: NotRequired[str]


class PutRegistryCatalogDataRequestRequestTypeDef(TypedDict):
    displayName: NotRequired[str]


class RegistryAliasTypeDef(TypedDict):
    name: str
    status: RegistryAliasStatusType
    primaryRegistryAlias: bool
    defaultRegistryAlias: bool


class SetRepositoryPolicyRequestRequestTypeDef(TypedDict):
    repositoryName: str
    policyText: str
    registryId: NotRequired[str]
    force: NotRequired[bool]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class BatchCheckLayerAvailabilityResponseTypeDef(TypedDict):
    layers: List[LayerTypeDef]
    failures: List[LayerFailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CompleteLayerUploadResponseTypeDef(TypedDict):
    registryId: str
    repositoryName: str
    uploadId: str
    layerDigest: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRepositoryPolicyResponseTypeDef(TypedDict):
    registryId: str
    repositoryName: str
    policyText: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetAuthorizationTokenResponseTypeDef(TypedDict):
    authorizationData: AuthorizationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetRepositoryPolicyResponseTypeDef(TypedDict):
    registryId: str
    repositoryName: str
    policyText: str
    ResponseMetadata: ResponseMetadataTypeDef


class InitiateLayerUploadResponseTypeDef(TypedDict):
    uploadId: str
    partSize: int
    ResponseMetadata: ResponseMetadataTypeDef


class SetRepositoryPolicyResponseTypeDef(TypedDict):
    registryId: str
    repositoryName: str
    policyText: str
    ResponseMetadata: ResponseMetadataTypeDef


class UploadLayerPartResponseTypeDef(TypedDict):
    registryId: str
    repositoryName: str
    uploadId: str
    lastByteReceived: int
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDeleteImageRequestRequestTypeDef(TypedDict):
    repositoryName: str
    imageIds: Sequence[ImageIdentifierTypeDef]
    registryId: NotRequired[str]


class DescribeImagesRequestRequestTypeDef(TypedDict):
    repositoryName: str
    registryId: NotRequired[str]
    imageIds: NotRequired[Sequence[ImageIdentifierTypeDef]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ImageFailureTypeDef(TypedDict):
    imageId: NotRequired[ImageIdentifierTypeDef]
    failureCode: NotRequired[ImageFailureCodeType]
    failureReason: NotRequired[str]


class ImageTypeDef(TypedDict):
    registryId: NotRequired[str]
    repositoryName: NotRequired[str]
    imageId: NotRequired[ImageIdentifierTypeDef]
    imageManifest: NotRequired[str]
    imageManifestMediaType: NotRequired[str]


class RepositoryCatalogDataInputTypeDef(TypedDict):
    description: NotRequired[str]
    architectures: NotRequired[Sequence[str]]
    operatingSystems: NotRequired[Sequence[str]]
    logoImageBlob: NotRequired[BlobTypeDef]
    aboutText: NotRequired[str]
    usageText: NotRequired[str]


class UploadLayerPartRequestRequestTypeDef(TypedDict):
    repositoryName: str
    uploadId: str
    partFirstByte: int
    partLastByte: int
    layerPartBlob: BlobTypeDef
    registryId: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]


class GetRepositoryCatalogDataResponseTypeDef(TypedDict):
    catalogData: RepositoryCatalogDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutRepositoryCatalogDataResponseTypeDef(TypedDict):
    catalogData: RepositoryCatalogDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRepositoryResponseTypeDef(TypedDict):
    repository: RepositoryTypeDef
    catalogData: RepositoryCatalogDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRepositoryResponseTypeDef(TypedDict):
    repository: RepositoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRepositoriesResponseTypeDef(TypedDict):
    repositories: List[RepositoryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DescribeImageTagsRequestDescribeImageTagsPaginateTypeDef(TypedDict):
    repositoryName: str
    registryId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeImagesRequestDescribeImagesPaginateTypeDef(TypedDict):
    repositoryName: str
    registryId: NotRequired[str]
    imageIds: NotRequired[Sequence[ImageIdentifierTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeRegistriesRequestDescribeRegistriesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeRepositoriesRequestDescribeRepositoriesPaginateTypeDef(TypedDict):
    registryId: NotRequired[str]
    repositoryNames: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeImagesResponseTypeDef(TypedDict):
    imageDetails: List[ImageDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetRegistryCatalogDataResponseTypeDef(TypedDict):
    registryCatalogData: RegistryCatalogDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutRegistryCatalogDataResponseTypeDef(TypedDict):
    registryCatalogData: RegistryCatalogDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ImageTagDetailTypeDef(TypedDict):
    imageTag: NotRequired[str]
    createdAt: NotRequired[datetime]
    imageDetail: NotRequired[ReferencedImageDetailTypeDef]


class RegistryTypeDef(TypedDict):
    registryId: str
    registryArn: str
    registryUri: str
    verified: bool
    aliases: List[RegistryAliasTypeDef]


class BatchDeleteImageResponseTypeDef(TypedDict):
    imageIds: List[ImageIdentifierTypeDef]
    failures: List[ImageFailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PutImageResponseTypeDef(TypedDict):
    image: ImageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRepositoryRequestRequestTypeDef(TypedDict):
    repositoryName: str
    catalogData: NotRequired[RepositoryCatalogDataInputTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]


class PutRepositoryCatalogDataRequestRequestTypeDef(TypedDict):
    repositoryName: str
    catalogData: RepositoryCatalogDataInputTypeDef
    registryId: NotRequired[str]


class DescribeImageTagsResponseTypeDef(TypedDict):
    imageTagDetails: List[ImageTagDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DescribeRegistriesResponseTypeDef(TypedDict):
    registries: List[RegistryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
