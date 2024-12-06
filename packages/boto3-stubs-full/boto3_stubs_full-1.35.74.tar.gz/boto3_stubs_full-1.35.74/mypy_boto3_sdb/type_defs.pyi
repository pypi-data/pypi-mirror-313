"""
Type annotations for sdb service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sdb/type_defs/)

Usage::

    ```python
    from mypy_boto3_sdb.type_defs import AttributeTypeDef

    data: AttributeTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AttributeTypeDef",
    "BatchDeleteAttributesRequestRequestTypeDef",
    "BatchPutAttributesRequestRequestTypeDef",
    "CreateDomainRequestRequestTypeDef",
    "DeletableItemTypeDef",
    "DeleteAttributesRequestRequestTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DomainMetadataRequestRequestTypeDef",
    "DomainMetadataResultTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAttributesRequestRequestTypeDef",
    "GetAttributesResultTypeDef",
    "ItemTypeDef",
    "ListDomainsRequestListDomainsPaginateTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListDomainsResultTypeDef",
    "PaginatorConfigTypeDef",
    "PutAttributesRequestRequestTypeDef",
    "ReplaceableAttributeTypeDef",
    "ReplaceableItemTypeDef",
    "ResponseMetadataTypeDef",
    "SelectRequestRequestTypeDef",
    "SelectRequestSelectPaginateTypeDef",
    "SelectResultTypeDef",
    "UpdateConditionTypeDef",
)

class AttributeTypeDef(TypedDict):
    Name: str
    Value: str
    AlternateNameEncoding: NotRequired[str]
    AlternateValueEncoding: NotRequired[str]

class CreateDomainRequestRequestTypeDef(TypedDict):
    DomainName: str

class UpdateConditionTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]
    Exists: NotRequired[bool]

class DeleteDomainRequestRequestTypeDef(TypedDict):
    DomainName: str

class DomainMetadataRequestRequestTypeDef(TypedDict):
    DomainName: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class GetAttributesRequestRequestTypeDef(TypedDict):
    DomainName: str
    ItemName: str
    AttributeNames: NotRequired[Sequence[str]]
    ConsistentRead: NotRequired[bool]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListDomainsRequestRequestTypeDef(TypedDict):
    MaxNumberOfDomains: NotRequired[int]
    NextToken: NotRequired[str]

class ReplaceableAttributeTypeDef(TypedDict):
    Name: str
    Value: str
    Replace: NotRequired[bool]

class SelectRequestRequestTypeDef(TypedDict):
    SelectExpression: str
    NextToken: NotRequired[str]
    ConsistentRead: NotRequired[bool]

class DeletableItemTypeDef(TypedDict):
    Name: str
    Attributes: NotRequired[Sequence[AttributeTypeDef]]

class ItemTypeDef(TypedDict):
    Name: str
    Attributes: List[AttributeTypeDef]
    AlternateNameEncoding: NotRequired[str]

class DeleteAttributesRequestRequestTypeDef(TypedDict):
    DomainName: str
    ItemName: str
    Attributes: NotRequired[Sequence[AttributeTypeDef]]
    Expected: NotRequired[UpdateConditionTypeDef]

class DomainMetadataResultTypeDef(TypedDict):
    ItemCount: int
    ItemNamesSizeBytes: int
    AttributeNameCount: int
    AttributeNamesSizeBytes: int
    AttributeValueCount: int
    AttributeValuesSizeBytes: int
    Timestamp: int
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetAttributesResultTypeDef(TypedDict):
    Attributes: List[AttributeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListDomainsResultTypeDef(TypedDict):
    DomainNames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListDomainsRequestListDomainsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SelectRequestSelectPaginateTypeDef(TypedDict):
    SelectExpression: str
    ConsistentRead: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class PutAttributesRequestRequestTypeDef(TypedDict):
    DomainName: str
    ItemName: str
    Attributes: Sequence[ReplaceableAttributeTypeDef]
    Expected: NotRequired[UpdateConditionTypeDef]

class ReplaceableItemTypeDef(TypedDict):
    Name: str
    Attributes: Sequence[ReplaceableAttributeTypeDef]

class BatchDeleteAttributesRequestRequestTypeDef(TypedDict):
    DomainName: str
    Items: Sequence[DeletableItemTypeDef]

class SelectResultTypeDef(TypedDict):
    Items: List[ItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class BatchPutAttributesRequestRequestTypeDef(TypedDict):
    DomainName: str
    Items: Sequence[ReplaceableItemTypeDef]
