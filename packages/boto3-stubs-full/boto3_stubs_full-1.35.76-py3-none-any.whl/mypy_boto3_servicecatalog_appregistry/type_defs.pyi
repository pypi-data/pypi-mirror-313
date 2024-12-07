"""
Type annotations for servicecatalog-appregistry service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/type_defs/)

Usage::

    ```python
    from mypy_boto3_servicecatalog_appregistry.type_defs import TagQueryConfigurationTypeDef

    data: TagQueryConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ApplicationTagStatusType,
    AssociationOptionType,
    ResourceGroupStateType,
    ResourceItemStatusType,
    ResourceTypeType,
    SyncActionType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AppRegistryConfigurationTypeDef",
    "ApplicationSummaryTypeDef",
    "ApplicationTagResultTypeDef",
    "ApplicationTypeDef",
    "AssociateAttributeGroupRequestRequestTypeDef",
    "AssociateAttributeGroupResponseTypeDef",
    "AssociateResourceRequestRequestTypeDef",
    "AssociateResourceResponseTypeDef",
    "AttributeGroupDetailsTypeDef",
    "AttributeGroupSummaryTypeDef",
    "AttributeGroupTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateAttributeGroupRequestRequestTypeDef",
    "CreateAttributeGroupResponseTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteApplicationResponseTypeDef",
    "DeleteAttributeGroupRequestRequestTypeDef",
    "DeleteAttributeGroupResponseTypeDef",
    "DisassociateAttributeGroupRequestRequestTypeDef",
    "DisassociateAttributeGroupResponseTypeDef",
    "DisassociateResourceRequestRequestTypeDef",
    "DisassociateResourceResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetApplicationResponseTypeDef",
    "GetAssociatedResourceRequestRequestTypeDef",
    "GetAssociatedResourceResponseTypeDef",
    "GetAttributeGroupRequestRequestTypeDef",
    "GetAttributeGroupResponseTypeDef",
    "GetConfigurationResponseTypeDef",
    "IntegrationsTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef",
    "ListAssociatedAttributeGroupsRequestRequestTypeDef",
    "ListAssociatedAttributeGroupsResponseTypeDef",
    "ListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef",
    "ListAssociatedResourcesRequestRequestTypeDef",
    "ListAssociatedResourcesResponseTypeDef",
    "ListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef",
    "ListAttributeGroupsForApplicationRequestRequestTypeDef",
    "ListAttributeGroupsForApplicationResponseTypeDef",
    "ListAttributeGroupsRequestListAttributeGroupsPaginateTypeDef",
    "ListAttributeGroupsRequestRequestTypeDef",
    "ListAttributeGroupsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutConfigurationRequestRequestTypeDef",
    "ResourceDetailsTypeDef",
    "ResourceGroupTypeDef",
    "ResourceInfoTypeDef",
    "ResourceIntegrationsTypeDef",
    "ResourceTypeDef",
    "ResourcesListItemTypeDef",
    "ResponseMetadataTypeDef",
    "SyncResourceRequestRequestTypeDef",
    "SyncResourceResponseTypeDef",
    "TagQueryConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateApplicationResponseTypeDef",
    "UpdateAttributeGroupRequestRequestTypeDef",
    "UpdateAttributeGroupResponseTypeDef",
)

class TagQueryConfigurationTypeDef(TypedDict):
    tagKey: NotRequired[str]

ApplicationSummaryTypeDef = TypedDict(
    "ApplicationSummaryTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "creationTime": NotRequired[datetime],
        "lastUpdateTime": NotRequired[datetime],
    },
)

class ResourcesListItemTypeDef(TypedDict):
    resourceArn: NotRequired[str]
    errorMessage: NotRequired[str]
    status: NotRequired[str]
    resourceType: NotRequired[str]

ApplicationTypeDef = TypedDict(
    "ApplicationTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "creationTime": NotRequired[datetime],
        "lastUpdateTime": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
        "applicationTag": NotRequired[Dict[str, str]],
    },
)

class AssociateAttributeGroupRequestRequestTypeDef(TypedDict):
    application: str
    attributeGroup: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AssociateResourceRequestRequestTypeDef(TypedDict):
    application: str
    resourceType: ResourceTypeType
    resource: str
    options: NotRequired[Sequence[AssociationOptionType]]

AttributeGroupDetailsTypeDef = TypedDict(
    "AttributeGroupDetailsTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "createdBy": NotRequired[str],
    },
)
AttributeGroupSummaryTypeDef = TypedDict(
    "AttributeGroupSummaryTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "creationTime": NotRequired[datetime],
        "lastUpdateTime": NotRequired[datetime],
        "createdBy": NotRequired[str],
    },
)
AttributeGroupTypeDef = TypedDict(
    "AttributeGroupTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "creationTime": NotRequired[datetime],
        "lastUpdateTime": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
    },
)

class CreateApplicationRequestRequestTypeDef(TypedDict):
    name: str
    clientToken: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CreateAttributeGroupRequestRequestTypeDef(TypedDict):
    name: str
    attributes: str
    clientToken: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class DeleteApplicationRequestRequestTypeDef(TypedDict):
    application: str

class DeleteAttributeGroupRequestRequestTypeDef(TypedDict):
    attributeGroup: str

class DisassociateAttributeGroupRequestRequestTypeDef(TypedDict):
    application: str
    attributeGroup: str

class DisassociateResourceRequestRequestTypeDef(TypedDict):
    application: str
    resourceType: ResourceTypeType
    resource: str

class GetApplicationRequestRequestTypeDef(TypedDict):
    application: str

class GetAssociatedResourceRequestRequestTypeDef(TypedDict):
    application: str
    resourceType: ResourceTypeType
    resource: str
    nextToken: NotRequired[str]
    resourceTagStatus: NotRequired[Sequence[ResourceItemStatusType]]
    maxResults: NotRequired[int]

class GetAttributeGroupRequestRequestTypeDef(TypedDict):
    attributeGroup: str

class ResourceGroupTypeDef(TypedDict):
    state: NotRequired[ResourceGroupStateType]
    arn: NotRequired[str]
    errorMessage: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListApplicationsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListAssociatedAttributeGroupsRequestRequestTypeDef(TypedDict):
    application: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListAssociatedResourcesRequestRequestTypeDef(TypedDict):
    application: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListAttributeGroupsForApplicationRequestRequestTypeDef(TypedDict):
    application: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListAttributeGroupsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class ResourceDetailsTypeDef(TypedDict):
    tagValue: NotRequired[str]

class SyncResourceRequestRequestTypeDef(TypedDict):
    resourceType: ResourceTypeType
    resource: str

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateApplicationRequestRequestTypeDef(TypedDict):
    application: str
    name: NotRequired[str]
    description: NotRequired[str]

class UpdateAttributeGroupRequestRequestTypeDef(TypedDict):
    attributeGroup: str
    name: NotRequired[str]
    description: NotRequired[str]
    attributes: NotRequired[str]

class AppRegistryConfigurationTypeDef(TypedDict):
    tagQueryConfiguration: NotRequired[TagQueryConfigurationTypeDef]

class ApplicationTagResultTypeDef(TypedDict):
    applicationTagStatus: NotRequired[ApplicationTagStatusType]
    errorMessage: NotRequired[str]
    resources: NotRequired[List[ResourcesListItemTypeDef]]
    nextToken: NotRequired[str]

class AssociateAttributeGroupResponseTypeDef(TypedDict):
    applicationArn: str
    attributeGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class AssociateResourceResponseTypeDef(TypedDict):
    applicationArn: str
    resourceArn: str
    options: List[AssociationOptionType]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateApplicationResponseTypeDef(TypedDict):
    application: ApplicationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteApplicationResponseTypeDef(TypedDict):
    application: ApplicationSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateAttributeGroupResponseTypeDef(TypedDict):
    applicationArn: str
    attributeGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateResourceResponseTypeDef(TypedDict):
    applicationArn: str
    resourceArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

GetAttributeGroupResponseTypeDef = TypedDict(
    "GetAttributeGroupResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "attributes": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "tags": Dict[str, str],
        "createdBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListApplicationsResponseTypeDef(TypedDict):
    applications: List[ApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAssociatedAttributeGroupsResponseTypeDef(TypedDict):
    attributeGroups: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class SyncResourceResponseTypeDef(TypedDict):
    applicationArn: str
    resourceArn: str
    actionTaken: SyncActionType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApplicationResponseTypeDef(TypedDict):
    application: ApplicationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAttributeGroupsForApplicationResponseTypeDef(TypedDict):
    attributeGroupsDetails: List[AttributeGroupDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DeleteAttributeGroupResponseTypeDef(TypedDict):
    attributeGroup: AttributeGroupSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAttributeGroupsResponseTypeDef(TypedDict):
    attributeGroups: List[AttributeGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateAttributeGroupResponseTypeDef(TypedDict):
    attributeGroup: AttributeGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAttributeGroupResponseTypeDef(TypedDict):
    attributeGroup: AttributeGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class IntegrationsTypeDef(TypedDict):
    resourceGroup: NotRequired[ResourceGroupTypeDef]
    applicationTagResourceGroup: NotRequired[ResourceGroupTypeDef]

class ResourceIntegrationsTypeDef(TypedDict):
    resourceGroup: NotRequired[ResourceGroupTypeDef]

class ListApplicationsRequestListApplicationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef(TypedDict):
    application: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef(TypedDict):
    application: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef(
    TypedDict
):
    application: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAttributeGroupsRequestListAttributeGroupsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ResourceInfoTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]
    resourceDetails: NotRequired[ResourceDetailsTypeDef]
    options: NotRequired[List[AssociationOptionType]]

class GetConfigurationResponseTypeDef(TypedDict):
    configuration: AppRegistryConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutConfigurationRequestRequestTypeDef(TypedDict):
    configuration: AppRegistryConfigurationTypeDef

GetApplicationResponseTypeDef = TypedDict(
    "GetApplicationResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "associatedResourceCount": int,
        "tags": Dict[str, str],
        "integrations": IntegrationsTypeDef,
        "applicationTag": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ResourceTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    associationTime: NotRequired[datetime]
    integrations: NotRequired[ResourceIntegrationsTypeDef]

class ListAssociatedResourcesResponseTypeDef(TypedDict):
    resources: List[ResourceInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetAssociatedResourceResponseTypeDef(TypedDict):
    resource: ResourceTypeDef
    options: List[AssociationOptionType]
    applicationTagResult: ApplicationTagResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
