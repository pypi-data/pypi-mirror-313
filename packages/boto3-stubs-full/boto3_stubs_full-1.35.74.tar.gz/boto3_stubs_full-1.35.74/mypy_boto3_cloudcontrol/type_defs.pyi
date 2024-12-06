"""
Type annotations for cloudcontrol service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudcontrol.type_defs import CancelResourceRequestInputRequestTypeDef

    data: CancelResourceRequestInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import HandlerErrorCodeType, OperationStatusType, OperationType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CancelResourceRequestInputRequestTypeDef",
    "CancelResourceRequestOutputTypeDef",
    "CreateResourceInputRequestTypeDef",
    "CreateResourceOutputTypeDef",
    "DeleteResourceInputRequestTypeDef",
    "DeleteResourceOutputTypeDef",
    "GetResourceInputRequestTypeDef",
    "GetResourceOutputTypeDef",
    "GetResourceRequestStatusInputRequestTypeDef",
    "GetResourceRequestStatusInputResourceRequestSuccessWaitTypeDef",
    "GetResourceRequestStatusOutputTypeDef",
    "HookProgressEventTypeDef",
    "ListResourceRequestsInputListResourceRequestsPaginateTypeDef",
    "ListResourceRequestsInputRequestTypeDef",
    "ListResourceRequestsOutputTypeDef",
    "ListResourcesInputListResourcesPaginateTypeDef",
    "ListResourcesInputRequestTypeDef",
    "ListResourcesOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ProgressEventTypeDef",
    "ResourceDescriptionTypeDef",
    "ResourceRequestStatusFilterTypeDef",
    "ResponseMetadataTypeDef",
    "UpdateResourceInputRequestTypeDef",
    "UpdateResourceOutputTypeDef",
    "WaiterConfigTypeDef",
)

class CancelResourceRequestInputRequestTypeDef(TypedDict):
    RequestToken: str

class ProgressEventTypeDef(TypedDict):
    TypeName: NotRequired[str]
    Identifier: NotRequired[str]
    RequestToken: NotRequired[str]
    HooksRequestToken: NotRequired[str]
    Operation: NotRequired[OperationType]
    OperationStatus: NotRequired[OperationStatusType]
    EventTime: NotRequired[datetime]
    ResourceModel: NotRequired[str]
    StatusMessage: NotRequired[str]
    ErrorCode: NotRequired[HandlerErrorCodeType]
    RetryAfter: NotRequired[datetime]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateResourceInputRequestTypeDef(TypedDict):
    TypeName: str
    DesiredState: str
    TypeVersionId: NotRequired[str]
    RoleArn: NotRequired[str]
    ClientToken: NotRequired[str]

class DeleteResourceInputRequestTypeDef(TypedDict):
    TypeName: str
    Identifier: str
    TypeVersionId: NotRequired[str]
    RoleArn: NotRequired[str]
    ClientToken: NotRequired[str]

class GetResourceInputRequestTypeDef(TypedDict):
    TypeName: str
    Identifier: str
    TypeVersionId: NotRequired[str]
    RoleArn: NotRequired[str]

class ResourceDescriptionTypeDef(TypedDict):
    Identifier: NotRequired[str]
    Properties: NotRequired[str]

class GetResourceRequestStatusInputRequestTypeDef(TypedDict):
    RequestToken: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class HookProgressEventTypeDef(TypedDict):
    HookTypeName: NotRequired[str]
    HookTypeVersionId: NotRequired[str]
    HookTypeArn: NotRequired[str]
    InvocationPoint: NotRequired[str]
    HookStatus: NotRequired[str]
    HookEventTime: NotRequired[datetime]
    HookStatusMessage: NotRequired[str]
    FailureMode: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ResourceRequestStatusFilterTypeDef(TypedDict):
    Operations: NotRequired[Sequence[OperationType]]
    OperationStatuses: NotRequired[Sequence[OperationStatusType]]

class ListResourcesInputRequestTypeDef(TypedDict):
    TypeName: str
    TypeVersionId: NotRequired[str]
    RoleArn: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ResourceModel: NotRequired[str]

class UpdateResourceInputRequestTypeDef(TypedDict):
    TypeName: str
    Identifier: str
    PatchDocument: str
    TypeVersionId: NotRequired[str]
    RoleArn: NotRequired[str]
    ClientToken: NotRequired[str]

class CancelResourceRequestOutputTypeDef(TypedDict):
    ProgressEvent: ProgressEventTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateResourceOutputTypeDef(TypedDict):
    ProgressEvent: ProgressEventTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteResourceOutputTypeDef(TypedDict):
    ProgressEvent: ProgressEventTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListResourceRequestsOutputTypeDef(TypedDict):
    ResourceRequestStatusSummaries: List[ProgressEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateResourceOutputTypeDef(TypedDict):
    ProgressEvent: ProgressEventTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourceOutputTypeDef(TypedDict):
    TypeName: str
    ResourceDescription: ResourceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListResourcesOutputTypeDef(TypedDict):
    TypeName: str
    ResourceDescriptions: List[ResourceDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetResourceRequestStatusInputResourceRequestSuccessWaitTypeDef(TypedDict):
    RequestToken: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetResourceRequestStatusOutputTypeDef(TypedDict):
    ProgressEvent: ProgressEventTypeDef
    HooksProgressEvent: List[HookProgressEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListResourcesInputListResourcesPaginateTypeDef(TypedDict):
    TypeName: str
    TypeVersionId: NotRequired[str]
    RoleArn: NotRequired[str]
    ResourceModel: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceRequestsInputListResourceRequestsPaginateTypeDef(TypedDict):
    ResourceRequestStatusFilter: NotRequired[ResourceRequestStatusFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceRequestsInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ResourceRequestStatusFilter: NotRequired[ResourceRequestStatusFilterTypeDef]
