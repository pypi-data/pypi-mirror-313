"""
Type annotations for connectcases service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcases/type_defs/)

Usage::

    ```python
    from mypy_boto3_connectcases.type_defs import AuditEventFieldValueUnionTypeDef

    data: AuditEventFieldValueUnionTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AuditEventTypeType,
    DomainStatusType,
    FieldNamespaceType,
    FieldTypeType,
    OrderType,
    RelatedItemTypeType,
    TemplateStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AuditEventFieldTypeDef",
    "AuditEventFieldValueUnionTypeDef",
    "AuditEventPerformedByTypeDef",
    "AuditEventTypeDef",
    "BasicLayoutOutputTypeDef",
    "BasicLayoutTypeDef",
    "BasicLayoutUnionTypeDef",
    "BatchGetFieldRequestRequestTypeDef",
    "BatchGetFieldResponseTypeDef",
    "BatchPutFieldOptionsRequestRequestTypeDef",
    "BatchPutFieldOptionsResponseTypeDef",
    "CaseEventIncludedDataOutputTypeDef",
    "CaseEventIncludedDataTypeDef",
    "CaseEventIncludedDataUnionTypeDef",
    "CaseFilterPaginatorTypeDef",
    "CaseFilterTypeDef",
    "CaseSummaryTypeDef",
    "CommentContentTypeDef",
    "ContactContentTypeDef",
    "ContactFilterTypeDef",
    "ContactTypeDef",
    "CreateCaseRequestRequestTypeDef",
    "CreateCaseResponseTypeDef",
    "CreateDomainRequestRequestTypeDef",
    "CreateDomainResponseTypeDef",
    "CreateFieldRequestRequestTypeDef",
    "CreateFieldResponseTypeDef",
    "CreateLayoutRequestRequestTypeDef",
    "CreateLayoutResponseTypeDef",
    "CreateRelatedItemRequestRequestTypeDef",
    "CreateRelatedItemResponseTypeDef",
    "CreateTemplateRequestRequestTypeDef",
    "CreateTemplateResponseTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DeleteFieldRequestRequestTypeDef",
    "DeleteLayoutRequestRequestTypeDef",
    "DeleteTemplateRequestRequestTypeDef",
    "DomainSummaryTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventBridgeConfigurationOutputTypeDef",
    "EventBridgeConfigurationTypeDef",
    "EventIncludedDataOutputTypeDef",
    "EventIncludedDataTypeDef",
    "EventIncludedDataUnionTypeDef",
    "FieldErrorTypeDef",
    "FieldFilterTypeDef",
    "FieldGroupOutputTypeDef",
    "FieldGroupTypeDef",
    "FieldGroupUnionTypeDef",
    "FieldIdentifierTypeDef",
    "FieldItemTypeDef",
    "FieldOptionErrorTypeDef",
    "FieldOptionTypeDef",
    "FieldSummaryTypeDef",
    "FieldValueExtraUnionTypeDef",
    "FieldValueOutputTypeDef",
    "FieldValueTypeDef",
    "FieldValueUnionOutputTypeDef",
    "FieldValueUnionTypeDef",
    "FieldValueUnionUnionTypeDef",
    "FileContentTypeDef",
    "FileFilterTypeDef",
    "GetCaseAuditEventsRequestRequestTypeDef",
    "GetCaseAuditEventsResponseTypeDef",
    "GetCaseEventConfigurationRequestRequestTypeDef",
    "GetCaseEventConfigurationResponseTypeDef",
    "GetCaseRequestRequestTypeDef",
    "GetCaseResponseTypeDef",
    "GetDomainRequestRequestTypeDef",
    "GetDomainResponseTypeDef",
    "GetFieldResponseTypeDef",
    "GetLayoutRequestRequestTypeDef",
    "GetLayoutResponseTypeDef",
    "GetTemplateRequestRequestTypeDef",
    "GetTemplateResponseTypeDef",
    "LayoutConfigurationTypeDef",
    "LayoutContentOutputTypeDef",
    "LayoutContentTypeDef",
    "LayoutSectionsOutputTypeDef",
    "LayoutSectionsTypeDef",
    "LayoutSectionsUnionTypeDef",
    "LayoutSummaryTypeDef",
    "ListCasesForContactRequestRequestTypeDef",
    "ListCasesForContactResponseTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListDomainsResponseTypeDef",
    "ListFieldOptionsRequestRequestTypeDef",
    "ListFieldOptionsResponseTypeDef",
    "ListFieldsRequestRequestTypeDef",
    "ListFieldsResponseTypeDef",
    "ListLayoutsRequestRequestTypeDef",
    "ListLayoutsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTemplatesRequestRequestTypeDef",
    "ListTemplatesResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutCaseEventConfigurationRequestRequestTypeDef",
    "RelatedItemContentTypeDef",
    "RelatedItemEventIncludedDataTypeDef",
    "RelatedItemInputContentTypeDef",
    "RelatedItemTypeFilterTypeDef",
    "RequiredFieldTypeDef",
    "ResponseMetadataTypeDef",
    "SearchCasesRequestRequestTypeDef",
    "SearchCasesRequestSearchCasesPaginateTypeDef",
    "SearchCasesResponseItemTypeDef",
    "SearchCasesResponseTypeDef",
    "SearchRelatedItemsRequestRequestTypeDef",
    "SearchRelatedItemsRequestSearchRelatedItemsPaginateTypeDef",
    "SearchRelatedItemsResponseItemTypeDef",
    "SearchRelatedItemsResponseTypeDef",
    "SectionOutputTypeDef",
    "SectionTypeDef",
    "SectionUnionTypeDef",
    "SortTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TemplateSummaryTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCaseRequestRequestTypeDef",
    "UpdateFieldRequestRequestTypeDef",
    "UpdateLayoutRequestRequestTypeDef",
    "UpdateTemplateRequestRequestTypeDef",
    "UserUnionTypeDef",
)

class AuditEventFieldValueUnionTypeDef(TypedDict):
    booleanValue: NotRequired[bool]
    doubleValue: NotRequired[float]
    emptyValue: NotRequired[Dict[str, Any]]
    stringValue: NotRequired[str]
    userArnValue: NotRequired[str]

class UserUnionTypeDef(TypedDict):
    userArn: NotRequired[str]

FieldIdentifierTypeDef = TypedDict(
    "FieldIdentifierTypeDef",
    {
        "id": str,
    },
)
FieldErrorTypeDef = TypedDict(
    "FieldErrorTypeDef",
    {
        "errorCode": str,
        "id": str,
        "message": NotRequired[str],
    },
)
GetFieldResponseTypeDef = TypedDict(
    "GetFieldResponseTypeDef",
    {
        "fieldArn": str,
        "fieldId": str,
        "name": str,
        "namespace": FieldNamespaceType,
        "type": FieldTypeType,
        "createdTime": NotRequired[datetime],
        "deleted": NotRequired[bool],
        "description": NotRequired[str],
        "lastModifiedTime": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class FieldOptionTypeDef(TypedDict):
    active: bool
    name: str
    value: str

class FieldOptionErrorTypeDef(TypedDict):
    errorCode: str
    message: str
    value: str

class CaseSummaryTypeDef(TypedDict):
    caseId: str
    templateId: str

class CommentContentTypeDef(TypedDict):
    body: str
    contentType: Literal["Text/Plain"]

class ContactContentTypeDef(TypedDict):
    channel: str
    connectedToSystemTime: datetime
    contactArn: str

class ContactFilterTypeDef(TypedDict):
    channel: NotRequired[Sequence[str]]
    contactArn: NotRequired[str]

class ContactTypeDef(TypedDict):
    contactArn: str

class CreateDomainRequestRequestTypeDef(TypedDict):
    name: str

CreateFieldRequestRequestTypeDef = TypedDict(
    "CreateFieldRequestRequestTypeDef",
    {
        "domainId": str,
        "name": str,
        "type": FieldTypeType,
        "description": NotRequired[str],
    },
)

class LayoutConfigurationTypeDef(TypedDict):
    defaultLayout: NotRequired[str]

class RequiredFieldTypeDef(TypedDict):
    fieldId: str

class DeleteDomainRequestRequestTypeDef(TypedDict):
    domainId: str

class DeleteFieldRequestRequestTypeDef(TypedDict):
    domainId: str
    fieldId: str

class DeleteLayoutRequestRequestTypeDef(TypedDict):
    domainId: str
    layoutId: str

class DeleteTemplateRequestRequestTypeDef(TypedDict):
    domainId: str
    templateId: str

class DomainSummaryTypeDef(TypedDict):
    domainArn: str
    domainId: str
    name: str

class RelatedItemEventIncludedDataTypeDef(TypedDict):
    includeContent: bool

FieldItemTypeDef = TypedDict(
    "FieldItemTypeDef",
    {
        "id": str,
    },
)
FieldSummaryTypeDef = TypedDict(
    "FieldSummaryTypeDef",
    {
        "fieldArn": str,
        "fieldId": str,
        "name": str,
        "namespace": FieldNamespaceType,
        "type": FieldTypeType,
    },
)

class FieldValueUnionOutputTypeDef(TypedDict):
    booleanValue: NotRequired[bool]
    doubleValue: NotRequired[float]
    emptyValue: NotRequired[Dict[str, Any]]
    stringValue: NotRequired[str]
    userArnValue: NotRequired[str]

class FieldValueUnionTypeDef(TypedDict):
    booleanValue: NotRequired[bool]
    doubleValue: NotRequired[float]
    emptyValue: NotRequired[Mapping[str, Any]]
    stringValue: NotRequired[str]
    userArnValue: NotRequired[str]

class FileContentTypeDef(TypedDict):
    fileArn: str

class FileFilterTypeDef(TypedDict):
    fileArn: NotRequired[str]

class GetCaseAuditEventsRequestRequestTypeDef(TypedDict):
    caseId: str
    domainId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class GetCaseEventConfigurationRequestRequestTypeDef(TypedDict):
    domainId: str

class GetDomainRequestRequestTypeDef(TypedDict):
    domainId: str

class GetLayoutRequestRequestTypeDef(TypedDict):
    domainId: str
    layoutId: str

class GetTemplateRequestRequestTypeDef(TypedDict):
    domainId: str
    templateId: str

class LayoutSummaryTypeDef(TypedDict):
    layoutArn: str
    layoutId: str
    name: str

class ListCasesForContactRequestRequestTypeDef(TypedDict):
    contactArn: str
    domainId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListDomainsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListFieldOptionsRequestRequestTypeDef(TypedDict):
    domainId: str
    fieldId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    values: NotRequired[Sequence[str]]

class ListFieldsRequestRequestTypeDef(TypedDict):
    domainId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListLayoutsRequestRequestTypeDef(TypedDict):
    domainId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    arn: str

class ListTemplatesRequestRequestTypeDef(TypedDict):
    domainId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[Sequence[TemplateStatusType]]

class TemplateSummaryTypeDef(TypedDict):
    name: str
    status: TemplateStatusType
    templateArn: str
    templateId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class SortTypeDef(TypedDict):
    fieldId: str
    sortOrder: OrderType

class TagResourceRequestRequestTypeDef(TypedDict):
    arn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    arn: str
    tagKeys: Sequence[str]

class UpdateFieldRequestRequestTypeDef(TypedDict):
    domainId: str
    fieldId: str
    description: NotRequired[str]
    name: NotRequired[str]

class AuditEventFieldTypeDef(TypedDict):
    eventFieldId: str
    newValue: AuditEventFieldValueUnionTypeDef
    oldValue: NotRequired[AuditEventFieldValueUnionTypeDef]

class AuditEventPerformedByTypeDef(TypedDict):
    iamPrincipalArn: str
    user: NotRequired[UserUnionTypeDef]

class BatchGetFieldRequestRequestTypeDef(TypedDict):
    domainId: str
    fields: Sequence[FieldIdentifierTypeDef]

class CaseEventIncludedDataOutputTypeDef(TypedDict):
    fields: List[FieldIdentifierTypeDef]

class CaseEventIncludedDataTypeDef(TypedDict):
    fields: Sequence[FieldIdentifierTypeDef]

class GetCaseRequestRequestTypeDef(TypedDict):
    caseId: str
    domainId: str
    fields: Sequence[FieldIdentifierTypeDef]
    nextToken: NotRequired[str]

class BatchGetFieldResponseTypeDef(TypedDict):
    errors: List[FieldErrorTypeDef]
    fields: List[GetFieldResponseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCaseResponseTypeDef(TypedDict):
    caseArn: str
    caseId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDomainResponseTypeDef(TypedDict):
    domainArn: str
    domainId: str
    domainStatus: DomainStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFieldResponseTypeDef(TypedDict):
    fieldArn: str
    fieldId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLayoutResponseTypeDef(TypedDict):
    layoutArn: str
    layoutId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRelatedItemResponseTypeDef(TypedDict):
    relatedItemArn: str
    relatedItemId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTemplateResponseTypeDef(TypedDict):
    templateArn: str
    templateId: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetDomainResponseTypeDef(TypedDict):
    createdTime: datetime
    domainArn: str
    domainId: str
    domainStatus: DomainStatusType
    name: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchPutFieldOptionsRequestRequestTypeDef(TypedDict):
    domainId: str
    fieldId: str
    options: Sequence[FieldOptionTypeDef]

class ListFieldOptionsResponseTypeDef(TypedDict):
    options: List[FieldOptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchPutFieldOptionsResponseTypeDef(TypedDict):
    errors: List[FieldOptionErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListCasesForContactResponseTypeDef(TypedDict):
    cases: List[CaseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateTemplateRequestRequestTypeDef(TypedDict):
    domainId: str
    name: str
    description: NotRequired[str]
    layoutConfiguration: NotRequired[LayoutConfigurationTypeDef]
    requiredFields: NotRequired[Sequence[RequiredFieldTypeDef]]
    status: NotRequired[TemplateStatusType]

class GetTemplateResponseTypeDef(TypedDict):
    createdTime: datetime
    deleted: bool
    description: str
    lastModifiedTime: datetime
    layoutConfiguration: LayoutConfigurationTypeDef
    name: str
    requiredFields: List[RequiredFieldTypeDef]
    status: TemplateStatusType
    tags: Dict[str, str]
    templateArn: str
    templateId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTemplateRequestRequestTypeDef(TypedDict):
    domainId: str
    templateId: str
    description: NotRequired[str]
    layoutConfiguration: NotRequired[LayoutConfigurationTypeDef]
    name: NotRequired[str]
    requiredFields: NotRequired[Sequence[RequiredFieldTypeDef]]
    status: NotRequired[TemplateStatusType]

class ListDomainsResponseTypeDef(TypedDict):
    domains: List[DomainSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class FieldGroupOutputTypeDef(TypedDict):
    fields: List[FieldItemTypeDef]
    name: NotRequired[str]

class FieldGroupTypeDef(TypedDict):
    fields: Sequence[FieldItemTypeDef]
    name: NotRequired[str]

class ListFieldsResponseTypeDef(TypedDict):
    fields: List[FieldSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

FieldValueOutputTypeDef = TypedDict(
    "FieldValueOutputTypeDef",
    {
        "id": str,
        "value": FieldValueUnionOutputTypeDef,
    },
)
FieldValueUnionUnionTypeDef = Union[FieldValueUnionTypeDef, FieldValueUnionOutputTypeDef]

class RelatedItemContentTypeDef(TypedDict):
    comment: NotRequired[CommentContentTypeDef]
    contact: NotRequired[ContactContentTypeDef]
    file: NotRequired[FileContentTypeDef]

class RelatedItemInputContentTypeDef(TypedDict):
    comment: NotRequired[CommentContentTypeDef]
    contact: NotRequired[ContactTypeDef]
    file: NotRequired[FileContentTypeDef]

class RelatedItemTypeFilterTypeDef(TypedDict):
    comment: NotRequired[Mapping[str, Any]]
    contact: NotRequired[ContactFilterTypeDef]
    file: NotRequired[FileFilterTypeDef]

class ListLayoutsResponseTypeDef(TypedDict):
    layouts: List[LayoutSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTemplatesResponseTypeDef(TypedDict):
    templates: List[TemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

AuditEventTypeDef = TypedDict(
    "AuditEventTypeDef",
    {
        "eventId": str,
        "fields": List[AuditEventFieldTypeDef],
        "performedTime": datetime,
        "type": AuditEventTypeType,
        "performedBy": NotRequired[AuditEventPerformedByTypeDef],
        "relatedItemType": NotRequired[RelatedItemTypeType],
    },
)

class EventIncludedDataOutputTypeDef(TypedDict):
    caseData: NotRequired[CaseEventIncludedDataOutputTypeDef]
    relatedItemData: NotRequired[RelatedItemEventIncludedDataTypeDef]

CaseEventIncludedDataUnionTypeDef = Union[
    CaseEventIncludedDataTypeDef, CaseEventIncludedDataOutputTypeDef
]

class SectionOutputTypeDef(TypedDict):
    fieldGroup: NotRequired[FieldGroupOutputTypeDef]

FieldGroupUnionTypeDef = Union[FieldGroupTypeDef, FieldGroupOutputTypeDef]

class GetCaseResponseTypeDef(TypedDict):
    fields: List[FieldValueOutputTypeDef]
    tags: Dict[str, str]
    templateId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SearchCasesResponseItemTypeDef(TypedDict):
    caseId: str
    fields: List[FieldValueOutputTypeDef]
    templateId: str
    tags: NotRequired[Dict[str, str]]

FieldValueTypeDef = TypedDict(
    "FieldValueTypeDef",
    {
        "id": str,
        "value": FieldValueUnionUnionTypeDef,
    },
)
SearchRelatedItemsResponseItemTypeDef = TypedDict(
    "SearchRelatedItemsResponseItemTypeDef",
    {
        "associationTime": datetime,
        "content": RelatedItemContentTypeDef,
        "relatedItemId": str,
        "type": RelatedItemTypeType,
        "performedBy": NotRequired[UserUnionTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateRelatedItemRequestRequestTypeDef = TypedDict(
    "CreateRelatedItemRequestRequestTypeDef",
    {
        "caseId": str,
        "content": RelatedItemInputContentTypeDef,
        "domainId": str,
        "type": RelatedItemTypeType,
        "performedBy": NotRequired[UserUnionTypeDef],
    },
)

class SearchRelatedItemsRequestRequestTypeDef(TypedDict):
    caseId: str
    domainId: str
    filters: NotRequired[Sequence[RelatedItemTypeFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class SearchRelatedItemsRequestSearchRelatedItemsPaginateTypeDef(TypedDict):
    caseId: str
    domainId: str
    filters: NotRequired[Sequence[RelatedItemTypeFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetCaseAuditEventsResponseTypeDef(TypedDict):
    auditEvents: List[AuditEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class EventBridgeConfigurationOutputTypeDef(TypedDict):
    enabled: bool
    includedData: NotRequired[EventIncludedDataOutputTypeDef]

class EventIncludedDataTypeDef(TypedDict):
    caseData: NotRequired[CaseEventIncludedDataUnionTypeDef]
    relatedItemData: NotRequired[RelatedItemEventIncludedDataTypeDef]

class LayoutSectionsOutputTypeDef(TypedDict):
    sections: NotRequired[List[SectionOutputTypeDef]]

class SectionTypeDef(TypedDict):
    fieldGroup: NotRequired[FieldGroupUnionTypeDef]

class SearchCasesResponseTypeDef(TypedDict):
    cases: List[SearchCasesResponseItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

FieldValueExtraUnionTypeDef = Union[FieldValueTypeDef, FieldValueOutputTypeDef]

class UpdateCaseRequestRequestTypeDef(TypedDict):
    caseId: str
    domainId: str
    fields: Sequence[FieldValueTypeDef]
    performedBy: NotRequired[UserUnionTypeDef]

class SearchRelatedItemsResponseTypeDef(TypedDict):
    relatedItems: List[SearchRelatedItemsResponseItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetCaseEventConfigurationResponseTypeDef(TypedDict):
    eventBridge: EventBridgeConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

EventIncludedDataUnionTypeDef = Union[EventIncludedDataTypeDef, EventIncludedDataOutputTypeDef]

class BasicLayoutOutputTypeDef(TypedDict):
    moreInfo: NotRequired[LayoutSectionsOutputTypeDef]
    topPanel: NotRequired[LayoutSectionsOutputTypeDef]

SectionUnionTypeDef = Union[SectionTypeDef, SectionOutputTypeDef]

class CreateCaseRequestRequestTypeDef(TypedDict):
    domainId: str
    fields: Sequence[FieldValueExtraUnionTypeDef]
    templateId: str
    clientToken: NotRequired[str]
    performedBy: NotRequired[UserUnionTypeDef]

class FieldFilterTypeDef(TypedDict):
    contains: NotRequired[FieldValueExtraUnionTypeDef]
    equalTo: NotRequired[FieldValueExtraUnionTypeDef]
    greaterThan: NotRequired[FieldValueExtraUnionTypeDef]
    greaterThanOrEqualTo: NotRequired[FieldValueExtraUnionTypeDef]
    lessThan: NotRequired[FieldValueExtraUnionTypeDef]
    lessThanOrEqualTo: NotRequired[FieldValueExtraUnionTypeDef]

class EventBridgeConfigurationTypeDef(TypedDict):
    enabled: bool
    includedData: NotRequired[EventIncludedDataUnionTypeDef]

class LayoutContentOutputTypeDef(TypedDict):
    basic: NotRequired[BasicLayoutOutputTypeDef]

class LayoutSectionsTypeDef(TypedDict):
    sections: NotRequired[Sequence[SectionUnionTypeDef]]

CaseFilterPaginatorTypeDef = TypedDict(
    "CaseFilterPaginatorTypeDef",
    {
        "andAll": NotRequired[Sequence[Mapping[str, Any]]],
        "field": NotRequired[FieldFilterTypeDef],
        "not": NotRequired[Mapping[str, Any]],
        "orAll": NotRequired[Sequence[Mapping[str, Any]]],
    },
)
CaseFilterTypeDef = TypedDict(
    "CaseFilterTypeDef",
    {
        "andAll": NotRequired[Sequence[Mapping[str, Any]]],
        "field": NotRequired[FieldFilterTypeDef],
        "not": NotRequired[Mapping[str, Any]],
        "orAll": NotRequired[Sequence[Mapping[str, Any]]],
    },
)

class PutCaseEventConfigurationRequestRequestTypeDef(TypedDict):
    domainId: str
    eventBridge: EventBridgeConfigurationTypeDef

class GetLayoutResponseTypeDef(TypedDict):
    content: LayoutContentOutputTypeDef
    createdTime: datetime
    deleted: bool
    lastModifiedTime: datetime
    layoutArn: str
    layoutId: str
    name: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

LayoutSectionsUnionTypeDef = Union[LayoutSectionsTypeDef, LayoutSectionsOutputTypeDef]
SearchCasesRequestSearchCasesPaginateTypeDef = TypedDict(
    "SearchCasesRequestSearchCasesPaginateTypeDef",
    {
        "domainId": str,
        "fields": NotRequired[Sequence[FieldIdentifierTypeDef]],
        "filter": NotRequired[CaseFilterPaginatorTypeDef],
        "searchTerm": NotRequired[str],
        "sorts": NotRequired[Sequence[SortTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
SearchCasesRequestRequestTypeDef = TypedDict(
    "SearchCasesRequestRequestTypeDef",
    {
        "domainId": str,
        "fields": NotRequired[Sequence[FieldIdentifierTypeDef]],
        "filter": NotRequired[CaseFilterTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "searchTerm": NotRequired[str],
        "sorts": NotRequired[Sequence[SortTypeDef]],
    },
)

class BasicLayoutTypeDef(TypedDict):
    moreInfo: NotRequired[LayoutSectionsUnionTypeDef]
    topPanel: NotRequired[LayoutSectionsUnionTypeDef]

BasicLayoutUnionTypeDef = Union[BasicLayoutTypeDef, BasicLayoutOutputTypeDef]

class LayoutContentTypeDef(TypedDict):
    basic: NotRequired[BasicLayoutUnionTypeDef]

class CreateLayoutRequestRequestTypeDef(TypedDict):
    content: LayoutContentTypeDef
    domainId: str
    name: str

class UpdateLayoutRequestRequestTypeDef(TypedDict):
    domainId: str
    layoutId: str
    content: NotRequired[LayoutContentTypeDef]
    name: NotRequired[str]
