"""
Type annotations for ram service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/type_defs/)

Usage::

    ```python
    from mypy_boto3_ram.type_defs import AcceptResourceShareInvitationRequestRequestTypeDef

    data: AcceptResourceShareInvitationRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    PermissionFeatureSetType,
    PermissionStatusType,
    PermissionTypeFilterType,
    PermissionTypeType,
    ReplacePermissionAssociationsWorkStatusType,
    ResourceOwnerType,
    ResourceRegionScopeFilterType,
    ResourceRegionScopeType,
    ResourceShareAssociationStatusType,
    ResourceShareAssociationTypeType,
    ResourceShareFeatureSetType,
    ResourceShareInvitationStatusType,
    ResourceShareStatusType,
    ResourceStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AcceptResourceShareInvitationRequestRequestTypeDef",
    "AcceptResourceShareInvitationResponseTypeDef",
    "AssociateResourceSharePermissionRequestRequestTypeDef",
    "AssociateResourceSharePermissionResponseTypeDef",
    "AssociateResourceShareRequestRequestTypeDef",
    "AssociateResourceShareResponseTypeDef",
    "AssociatedPermissionTypeDef",
    "CreatePermissionRequestRequestTypeDef",
    "CreatePermissionResponseTypeDef",
    "CreatePermissionVersionRequestRequestTypeDef",
    "CreatePermissionVersionResponseTypeDef",
    "CreateResourceShareRequestRequestTypeDef",
    "CreateResourceShareResponseTypeDef",
    "DeletePermissionRequestRequestTypeDef",
    "DeletePermissionResponseTypeDef",
    "DeletePermissionVersionRequestRequestTypeDef",
    "DeletePermissionVersionResponseTypeDef",
    "DeleteResourceShareRequestRequestTypeDef",
    "DeleteResourceShareResponseTypeDef",
    "DisassociateResourceSharePermissionRequestRequestTypeDef",
    "DisassociateResourceSharePermissionResponseTypeDef",
    "DisassociateResourceShareRequestRequestTypeDef",
    "DisassociateResourceShareResponseTypeDef",
    "EnableSharingWithAwsOrganizationResponseTypeDef",
    "GetPermissionRequestRequestTypeDef",
    "GetPermissionResponseTypeDef",
    "GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef",
    "GetResourcePoliciesRequestRequestTypeDef",
    "GetResourcePoliciesResponseTypeDef",
    "GetResourceShareAssociationsRequestGetResourceShareAssociationsPaginateTypeDef",
    "GetResourceShareAssociationsRequestRequestTypeDef",
    "GetResourceShareAssociationsResponseTypeDef",
    "GetResourceShareInvitationsRequestGetResourceShareInvitationsPaginateTypeDef",
    "GetResourceShareInvitationsRequestRequestTypeDef",
    "GetResourceShareInvitationsResponseTypeDef",
    "GetResourceSharesRequestGetResourceSharesPaginateTypeDef",
    "GetResourceSharesRequestRequestTypeDef",
    "GetResourceSharesResponseTypeDef",
    "ListPendingInvitationResourcesRequestRequestTypeDef",
    "ListPendingInvitationResourcesResponseTypeDef",
    "ListPermissionAssociationsRequestRequestTypeDef",
    "ListPermissionAssociationsResponseTypeDef",
    "ListPermissionVersionsRequestRequestTypeDef",
    "ListPermissionVersionsResponseTypeDef",
    "ListPermissionsRequestRequestTypeDef",
    "ListPermissionsResponseTypeDef",
    "ListPrincipalsRequestListPrincipalsPaginateTypeDef",
    "ListPrincipalsRequestRequestTypeDef",
    "ListPrincipalsResponseTypeDef",
    "ListReplacePermissionAssociationsWorkRequestRequestTypeDef",
    "ListReplacePermissionAssociationsWorkResponseTypeDef",
    "ListResourceSharePermissionsRequestRequestTypeDef",
    "ListResourceSharePermissionsResponseTypeDef",
    "ListResourceTypesRequestRequestTypeDef",
    "ListResourceTypesResponseTypeDef",
    "ListResourcesRequestListResourcesPaginateTypeDef",
    "ListResourcesRequestRequestTypeDef",
    "ListResourcesResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PrincipalTypeDef",
    "PromotePermissionCreatedFromPolicyRequestRequestTypeDef",
    "PromotePermissionCreatedFromPolicyResponseTypeDef",
    "PromoteResourceShareCreatedFromPolicyRequestRequestTypeDef",
    "PromoteResourceShareCreatedFromPolicyResponseTypeDef",
    "RejectResourceShareInvitationRequestRequestTypeDef",
    "RejectResourceShareInvitationResponseTypeDef",
    "ReplacePermissionAssociationsRequestRequestTypeDef",
    "ReplacePermissionAssociationsResponseTypeDef",
    "ReplacePermissionAssociationsWorkTypeDef",
    "ResourceShareAssociationTypeDef",
    "ResourceShareInvitationTypeDef",
    "ResourceSharePermissionDetailTypeDef",
    "ResourceSharePermissionSummaryTypeDef",
    "ResourceShareTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "ServiceNameAndResourceTypeTypeDef",
    "SetDefaultPermissionVersionRequestRequestTypeDef",
    "SetDefaultPermissionVersionResponseTypeDef",
    "TagFilterTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateResourceShareRequestRequestTypeDef",
    "UpdateResourceShareResponseTypeDef",
)

class AcceptResourceShareInvitationRequestRequestTypeDef(TypedDict):
    resourceShareInvitationArn: str
    clientToken: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AssociateResourceSharePermissionRequestRequestTypeDef(TypedDict):
    resourceShareArn: str
    permissionArn: str
    replace: NotRequired[bool]
    clientToken: NotRequired[str]
    permissionVersion: NotRequired[int]

class AssociateResourceShareRequestRequestTypeDef(TypedDict):
    resourceShareArn: str
    resourceArns: NotRequired[Sequence[str]]
    principals: NotRequired[Sequence[str]]
    clientToken: NotRequired[str]
    sources: NotRequired[Sequence[str]]

class ResourceShareAssociationTypeDef(TypedDict):
    resourceShareArn: NotRequired[str]
    resourceShareName: NotRequired[str]
    associatedEntity: NotRequired[str]
    associationType: NotRequired[ResourceShareAssociationTypeType]
    status: NotRequired[ResourceShareAssociationStatusType]
    statusMessage: NotRequired[str]
    creationTime: NotRequired[datetime]
    lastUpdatedTime: NotRequired[datetime]
    external: NotRequired[bool]

class AssociatedPermissionTypeDef(TypedDict):
    arn: NotRequired[str]
    permissionVersion: NotRequired[str]
    defaultVersion: NotRequired[bool]
    resourceType: NotRequired[str]
    status: NotRequired[str]
    featureSet: NotRequired[PermissionFeatureSetType]
    lastUpdatedTime: NotRequired[datetime]
    resourceShareArn: NotRequired[str]

class TagTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]

class CreatePermissionVersionRequestRequestTypeDef(TypedDict):
    permissionArn: str
    policyTemplate: str
    clientToken: NotRequired[str]

class DeletePermissionRequestRequestTypeDef(TypedDict):
    permissionArn: str
    clientToken: NotRequired[str]

class DeletePermissionVersionRequestRequestTypeDef(TypedDict):
    permissionArn: str
    permissionVersion: int
    clientToken: NotRequired[str]

class DeleteResourceShareRequestRequestTypeDef(TypedDict):
    resourceShareArn: str
    clientToken: NotRequired[str]

class DisassociateResourceSharePermissionRequestRequestTypeDef(TypedDict):
    resourceShareArn: str
    permissionArn: str
    clientToken: NotRequired[str]

class DisassociateResourceShareRequestRequestTypeDef(TypedDict):
    resourceShareArn: str
    resourceArns: NotRequired[Sequence[str]]
    principals: NotRequired[Sequence[str]]
    clientToken: NotRequired[str]
    sources: NotRequired[Sequence[str]]

class GetPermissionRequestRequestTypeDef(TypedDict):
    permissionArn: str
    permissionVersion: NotRequired[int]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetResourcePoliciesRequestRequestTypeDef(TypedDict):
    resourceArns: Sequence[str]
    principal: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetResourceShareAssociationsRequestRequestTypeDef(TypedDict):
    associationType: ResourceShareAssociationTypeType
    resourceShareArns: NotRequired[Sequence[str]]
    resourceArn: NotRequired[str]
    principal: NotRequired[str]
    associationStatus: NotRequired[ResourceShareAssociationStatusType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetResourceShareInvitationsRequestRequestTypeDef(TypedDict):
    resourceShareInvitationArns: NotRequired[Sequence[str]]
    resourceShareArns: NotRequired[Sequence[str]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class TagFilterTypeDef(TypedDict):
    tagKey: NotRequired[str]
    tagValues: NotRequired[Sequence[str]]

class ListPendingInvitationResourcesRequestRequestTypeDef(TypedDict):
    resourceShareInvitationArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    resourceRegionScope: NotRequired[ResourceRegionScopeFilterType]

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "arn": NotRequired[str],
        "type": NotRequired[str],
        "resourceShareArn": NotRequired[str],
        "resourceGroupArn": NotRequired[str],
        "status": NotRequired[ResourceStatusType],
        "statusMessage": NotRequired[str],
        "creationTime": NotRequired[datetime],
        "lastUpdatedTime": NotRequired[datetime],
        "resourceRegionScope": NotRequired[ResourceRegionScopeType],
    },
)

class ListPermissionAssociationsRequestRequestTypeDef(TypedDict):
    permissionArn: NotRequired[str]
    permissionVersion: NotRequired[int]
    associationStatus: NotRequired[ResourceShareAssociationStatusType]
    resourceType: NotRequired[str]
    featureSet: NotRequired[PermissionFeatureSetType]
    defaultVersion: NotRequired[bool]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListPermissionVersionsRequestRequestTypeDef(TypedDict):
    permissionArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListPermissionsRequestRequestTypeDef(TypedDict):
    resourceType: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    permissionType: NotRequired[PermissionTypeFilterType]

class ListPrincipalsRequestRequestTypeDef(TypedDict):
    resourceOwner: ResourceOwnerType
    resourceArn: NotRequired[str]
    principals: NotRequired[Sequence[str]]
    resourceType: NotRequired[str]
    resourceShareArns: NotRequired[Sequence[str]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

PrincipalTypeDef = TypedDict(
    "PrincipalTypeDef",
    {
        "id": NotRequired[str],
        "resourceShareArn": NotRequired[str],
        "creationTime": NotRequired[datetime],
        "lastUpdatedTime": NotRequired[datetime],
        "external": NotRequired[bool],
    },
)

class ListReplacePermissionAssociationsWorkRequestRequestTypeDef(TypedDict):
    workIds: NotRequired[Sequence[str]]
    status: NotRequired[ReplacePermissionAssociationsWorkStatusType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

ReplacePermissionAssociationsWorkTypeDef = TypedDict(
    "ReplacePermissionAssociationsWorkTypeDef",
    {
        "id": NotRequired[str],
        "fromPermissionArn": NotRequired[str],
        "fromPermissionVersion": NotRequired[str],
        "toPermissionArn": NotRequired[str],
        "toPermissionVersion": NotRequired[str],
        "status": NotRequired[ReplacePermissionAssociationsWorkStatusType],
        "statusMessage": NotRequired[str],
        "creationTime": NotRequired[datetime],
        "lastUpdatedTime": NotRequired[datetime],
    },
)

class ListResourceSharePermissionsRequestRequestTypeDef(TypedDict):
    resourceShareArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListResourceTypesRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    resourceRegionScope: NotRequired[ResourceRegionScopeFilterType]

class ServiceNameAndResourceTypeTypeDef(TypedDict):
    resourceType: NotRequired[str]
    serviceName: NotRequired[str]
    resourceRegionScope: NotRequired[ResourceRegionScopeType]

class ListResourcesRequestRequestTypeDef(TypedDict):
    resourceOwner: ResourceOwnerType
    principal: NotRequired[str]
    resourceType: NotRequired[str]
    resourceArns: NotRequired[Sequence[str]]
    resourceShareArns: NotRequired[Sequence[str]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    resourceRegionScope: NotRequired[ResourceRegionScopeFilterType]

class PromotePermissionCreatedFromPolicyRequestRequestTypeDef(TypedDict):
    permissionArn: str
    name: str
    clientToken: NotRequired[str]

class PromoteResourceShareCreatedFromPolicyRequestRequestTypeDef(TypedDict):
    resourceShareArn: str

class RejectResourceShareInvitationRequestRequestTypeDef(TypedDict):
    resourceShareInvitationArn: str
    clientToken: NotRequired[str]

class ReplacePermissionAssociationsRequestRequestTypeDef(TypedDict):
    fromPermissionArn: str
    toPermissionArn: str
    fromPermissionVersion: NotRequired[int]
    clientToken: NotRequired[str]

class SetDefaultPermissionVersionRequestRequestTypeDef(TypedDict):
    permissionArn: str
    permissionVersion: int
    clientToken: NotRequired[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    tagKeys: Sequence[str]
    resourceShareArn: NotRequired[str]
    resourceArn: NotRequired[str]

class UpdateResourceShareRequestRequestTypeDef(TypedDict):
    resourceShareArn: str
    name: NotRequired[str]
    allowExternalPrincipals: NotRequired[bool]
    clientToken: NotRequired[str]

class AssociateResourceSharePermissionResponseTypeDef(TypedDict):
    returnValue: bool
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePermissionResponseTypeDef(TypedDict):
    returnValue: bool
    clientToken: str
    permissionStatus: PermissionStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePermissionVersionResponseTypeDef(TypedDict):
    returnValue: bool
    clientToken: str
    permissionStatus: PermissionStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteResourceShareResponseTypeDef(TypedDict):
    returnValue: bool
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateResourceSharePermissionResponseTypeDef(TypedDict):
    returnValue: bool
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class EnableSharingWithAwsOrganizationResponseTypeDef(TypedDict):
    returnValue: bool
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourcePoliciesResponseTypeDef(TypedDict):
    policies: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PromoteResourceShareCreatedFromPolicyResponseTypeDef(TypedDict):
    returnValue: bool
    ResponseMetadata: ResponseMetadataTypeDef

class SetDefaultPermissionVersionResponseTypeDef(TypedDict):
    returnValue: bool
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class AssociateResourceShareResponseTypeDef(TypedDict):
    resourceShareAssociations: List[ResourceShareAssociationTypeDef]
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateResourceShareResponseTypeDef(TypedDict):
    resourceShareAssociations: List[ResourceShareAssociationTypeDef]
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourceShareAssociationsResponseTypeDef(TypedDict):
    resourceShareAssociations: List[ResourceShareAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ResourceShareInvitationTypeDef(TypedDict):
    resourceShareInvitationArn: NotRequired[str]
    resourceShareName: NotRequired[str]
    resourceShareArn: NotRequired[str]
    senderAccountId: NotRequired[str]
    receiverAccountId: NotRequired[str]
    invitationTimestamp: NotRequired[datetime]
    status: NotRequired[ResourceShareInvitationStatusType]
    resourceShareAssociations: NotRequired[List[ResourceShareAssociationTypeDef]]
    receiverArn: NotRequired[str]

class ListPermissionAssociationsResponseTypeDef(TypedDict):
    permissions: List[AssociatedPermissionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreatePermissionRequestRequestTypeDef(TypedDict):
    name: str
    resourceType: str
    policyTemplate: str
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateResourceShareRequestRequestTypeDef(TypedDict):
    name: str
    resourceArns: NotRequired[Sequence[str]]
    principals: NotRequired[Sequence[str]]
    tags: NotRequired[Sequence[TagTypeDef]]
    allowExternalPrincipals: NotRequired[bool]
    clientToken: NotRequired[str]
    permissionArns: NotRequired[Sequence[str]]
    sources: NotRequired[Sequence[str]]

class ResourceSharePermissionDetailTypeDef(TypedDict):
    arn: NotRequired[str]
    version: NotRequired[str]
    defaultVersion: NotRequired[bool]
    name: NotRequired[str]
    resourceType: NotRequired[str]
    permission: NotRequired[str]
    creationTime: NotRequired[datetime]
    lastUpdatedTime: NotRequired[datetime]
    isResourceTypeDefault: NotRequired[bool]
    permissionType: NotRequired[PermissionTypeType]
    featureSet: NotRequired[PermissionFeatureSetType]
    status: NotRequired[PermissionStatusType]
    tags: NotRequired[List[TagTypeDef]]

class ResourceSharePermissionSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    version: NotRequired[str]
    defaultVersion: NotRequired[bool]
    name: NotRequired[str]
    resourceType: NotRequired[str]
    status: NotRequired[str]
    creationTime: NotRequired[datetime]
    lastUpdatedTime: NotRequired[datetime]
    isResourceTypeDefault: NotRequired[bool]
    permissionType: NotRequired[PermissionTypeType]
    featureSet: NotRequired[PermissionFeatureSetType]
    tags: NotRequired[List[TagTypeDef]]

class ResourceShareTypeDef(TypedDict):
    resourceShareArn: NotRequired[str]
    name: NotRequired[str]
    owningAccountId: NotRequired[str]
    allowExternalPrincipals: NotRequired[bool]
    status: NotRequired[ResourceShareStatusType]
    statusMessage: NotRequired[str]
    tags: NotRequired[List[TagTypeDef]]
    creationTime: NotRequired[datetime]
    lastUpdatedTime: NotRequired[datetime]
    featureSet: NotRequired[ResourceShareFeatureSetType]

class TagResourceRequestRequestTypeDef(TypedDict):
    tags: Sequence[TagTypeDef]
    resourceShareArn: NotRequired[str]
    resourceArn: NotRequired[str]

class GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef(TypedDict):
    resourceArns: Sequence[str]
    principal: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetResourceShareAssociationsRequestGetResourceShareAssociationsPaginateTypeDef(TypedDict):
    associationType: ResourceShareAssociationTypeType
    resourceShareArns: NotRequired[Sequence[str]]
    resourceArn: NotRequired[str]
    principal: NotRequired[str]
    associationStatus: NotRequired[ResourceShareAssociationStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetResourceShareInvitationsRequestGetResourceShareInvitationsPaginateTypeDef(TypedDict):
    resourceShareInvitationArns: NotRequired[Sequence[str]]
    resourceShareArns: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPrincipalsRequestListPrincipalsPaginateTypeDef(TypedDict):
    resourceOwner: ResourceOwnerType
    resourceArn: NotRequired[str]
    principals: NotRequired[Sequence[str]]
    resourceType: NotRequired[str]
    resourceShareArns: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourcesRequestListResourcesPaginateTypeDef(TypedDict):
    resourceOwner: ResourceOwnerType
    principal: NotRequired[str]
    resourceType: NotRequired[str]
    resourceArns: NotRequired[Sequence[str]]
    resourceShareArns: NotRequired[Sequence[str]]
    resourceRegionScope: NotRequired[ResourceRegionScopeFilterType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetResourceSharesRequestGetResourceSharesPaginateTypeDef(TypedDict):
    resourceOwner: ResourceOwnerType
    resourceShareArns: NotRequired[Sequence[str]]
    resourceShareStatus: NotRequired[ResourceShareStatusType]
    name: NotRequired[str]
    tagFilters: NotRequired[Sequence[TagFilterTypeDef]]
    permissionArn: NotRequired[str]
    permissionVersion: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetResourceSharesRequestRequestTypeDef(TypedDict):
    resourceOwner: ResourceOwnerType
    resourceShareArns: NotRequired[Sequence[str]]
    resourceShareStatus: NotRequired[ResourceShareStatusType]
    name: NotRequired[str]
    tagFilters: NotRequired[Sequence[TagFilterTypeDef]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    permissionArn: NotRequired[str]
    permissionVersion: NotRequired[int]

class ListPendingInvitationResourcesResponseTypeDef(TypedDict):
    resources: List[ResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListResourcesResponseTypeDef(TypedDict):
    resources: List[ResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPrincipalsResponseTypeDef(TypedDict):
    principals: List[PrincipalTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListReplacePermissionAssociationsWorkResponseTypeDef(TypedDict):
    replacePermissionAssociationsWorks: List[ReplacePermissionAssociationsWorkTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ReplacePermissionAssociationsResponseTypeDef(TypedDict):
    replacePermissionAssociationsWork: ReplacePermissionAssociationsWorkTypeDef
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListResourceTypesResponseTypeDef(TypedDict):
    resourceTypes: List[ServiceNameAndResourceTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AcceptResourceShareInvitationResponseTypeDef(TypedDict):
    resourceShareInvitation: ResourceShareInvitationTypeDef
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourceShareInvitationsResponseTypeDef(TypedDict):
    resourceShareInvitations: List[ResourceShareInvitationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class RejectResourceShareInvitationResponseTypeDef(TypedDict):
    resourceShareInvitation: ResourceShareInvitationTypeDef
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePermissionVersionResponseTypeDef(TypedDict):
    permission: ResourceSharePermissionDetailTypeDef
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetPermissionResponseTypeDef(TypedDict):
    permission: ResourceSharePermissionDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePermissionResponseTypeDef(TypedDict):
    permission: ResourceSharePermissionSummaryTypeDef
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListPermissionVersionsResponseTypeDef(TypedDict):
    permissions: List[ResourceSharePermissionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPermissionsResponseTypeDef(TypedDict):
    permissions: List[ResourceSharePermissionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListResourceSharePermissionsResponseTypeDef(TypedDict):
    permissions: List[ResourceSharePermissionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PromotePermissionCreatedFromPolicyResponseTypeDef(TypedDict):
    permission: ResourceSharePermissionSummaryTypeDef
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateResourceShareResponseTypeDef(TypedDict):
    resourceShare: ResourceShareTypeDef
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourceSharesResponseTypeDef(TypedDict):
    resourceShares: List[ResourceShareTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateResourceShareResponseTypeDef(TypedDict):
    resourceShare: ResourceShareTypeDef
    clientToken: str
    ResponseMetadata: ResponseMetadataTypeDef
