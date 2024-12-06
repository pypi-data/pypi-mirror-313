"""
Type annotations for invoicing service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_invoicing/type_defs/)

Usage::

    ```python
    from mypy_boto3_invoicing.type_defs import BatchGetInvoiceProfileRequestRequestTypeDef

    data: BatchGetInvoiceProfileRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BatchGetInvoiceProfileRequestRequestTypeDef",
    "BatchGetInvoiceProfileResponseTypeDef",
    "CreateInvoiceUnitRequestRequestTypeDef",
    "CreateInvoiceUnitResponseTypeDef",
    "DeleteInvoiceUnitRequestRequestTypeDef",
    "DeleteInvoiceUnitResponseTypeDef",
    "FiltersTypeDef",
    "GetInvoiceUnitRequestRequestTypeDef",
    "GetInvoiceUnitResponseTypeDef",
    "InvoiceProfileTypeDef",
    "InvoiceUnitRuleOutputTypeDef",
    "InvoiceUnitRuleTypeDef",
    "InvoiceUnitTypeDef",
    "ListInvoiceUnitsRequestListInvoiceUnitsPaginateTypeDef",
    "ListInvoiceUnitsRequestRequestTypeDef",
    "ListInvoiceUnitsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ReceiverAddressTypeDef",
    "ResourceTagTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateInvoiceUnitRequestRequestTypeDef",
    "UpdateInvoiceUnitResponseTypeDef",
)

class BatchGetInvoiceProfileRequestRequestTypeDef(TypedDict):
    AccountIds: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class InvoiceUnitRuleTypeDef(TypedDict):
    LinkedAccounts: NotRequired[Sequence[str]]

class ResourceTagTypeDef(TypedDict):
    Key: str
    Value: str

class DeleteInvoiceUnitRequestRequestTypeDef(TypedDict):
    InvoiceUnitArn: str

class FiltersTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    InvoiceReceivers: NotRequired[Sequence[str]]
    Accounts: NotRequired[Sequence[str]]

TimestampTypeDef = Union[datetime, str]

class InvoiceUnitRuleOutputTypeDef(TypedDict):
    LinkedAccounts: NotRequired[List[str]]

class ReceiverAddressTypeDef(TypedDict):
    AddressLine1: NotRequired[str]
    AddressLine2: NotRequired[str]
    AddressLine3: NotRequired[str]
    DistrictOrCounty: NotRequired[str]
    City: NotRequired[str]
    StateOrRegion: NotRequired[str]
    CountryCode: NotRequired[str]
    CompanyName: NotRequired[str]
    PostalCode: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    ResourceTagKeys: Sequence[str]

class CreateInvoiceUnitResponseTypeDef(TypedDict):
    InvoiceUnitArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteInvoiceUnitResponseTypeDef(TypedDict):
    InvoiceUnitArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateInvoiceUnitResponseTypeDef(TypedDict):
    InvoiceUnitArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateInvoiceUnitRequestRequestTypeDef(TypedDict):
    InvoiceUnitArn: str
    Description: NotRequired[str]
    TaxInheritanceDisabled: NotRequired[bool]
    Rule: NotRequired[InvoiceUnitRuleTypeDef]

class CreateInvoiceUnitRequestRequestTypeDef(TypedDict):
    Name: str
    InvoiceReceiver: str
    Rule: InvoiceUnitRuleTypeDef
    Description: NotRequired[str]
    TaxInheritanceDisabled: NotRequired[bool]
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]

class ListTagsForResourceResponseTypeDef(TypedDict):
    ResourceTags: List[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    ResourceTags: Sequence[ResourceTagTypeDef]

class GetInvoiceUnitRequestRequestTypeDef(TypedDict):
    InvoiceUnitArn: str
    AsOf: NotRequired[TimestampTypeDef]

class ListInvoiceUnitsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[FiltersTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    AsOf: NotRequired[TimestampTypeDef]

class GetInvoiceUnitResponseTypeDef(TypedDict):
    InvoiceUnitArn: str
    InvoiceReceiver: str
    Name: str
    Description: str
    TaxInheritanceDisabled: bool
    Rule: InvoiceUnitRuleOutputTypeDef
    LastModified: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class InvoiceUnitTypeDef(TypedDict):
    InvoiceUnitArn: NotRequired[str]
    InvoiceReceiver: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    TaxInheritanceDisabled: NotRequired[bool]
    Rule: NotRequired[InvoiceUnitRuleOutputTypeDef]
    LastModified: NotRequired[datetime]

class InvoiceProfileTypeDef(TypedDict):
    AccountId: NotRequired[str]
    ReceiverName: NotRequired[str]
    ReceiverAddress: NotRequired[ReceiverAddressTypeDef]
    ReceiverEmail: NotRequired[str]
    Issuer: NotRequired[str]
    TaxRegistrationNumber: NotRequired[str]

class ListInvoiceUnitsRequestListInvoiceUnitsPaginateTypeDef(TypedDict):
    Filters: NotRequired[FiltersTypeDef]
    AsOf: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInvoiceUnitsResponseTypeDef(TypedDict):
    InvoiceUnits: List[InvoiceUnitTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class BatchGetInvoiceProfileResponseTypeDef(TypedDict):
    Profiles: List[InvoiceProfileTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
