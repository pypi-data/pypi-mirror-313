"""
Type annotations for controltower service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/type_defs/)

Usage::

    ```python
    from mypy_boto3_controltower.type_defs import BaselineOperationTypeDef

    data: BaselineOperationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence

from .literals import (
    BaselineOperationStatusType,
    BaselineOperationTypeType,
    ControlOperationStatusType,
    ControlOperationTypeType,
    DriftStatusType,
    EnablementStatusType,
    LandingZoneDriftStatusType,
    LandingZoneOperationStatusType,
    LandingZoneOperationTypeType,
    LandingZoneStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BaselineOperationTypeDef",
    "BaselineSummaryTypeDef",
    "ControlOperationFilterTypeDef",
    "ControlOperationSummaryTypeDef",
    "ControlOperationTypeDef",
    "CreateLandingZoneInputRequestTypeDef",
    "CreateLandingZoneOutputTypeDef",
    "DeleteLandingZoneInputRequestTypeDef",
    "DeleteLandingZoneOutputTypeDef",
    "DisableBaselineInputRequestTypeDef",
    "DisableBaselineOutputTypeDef",
    "DisableControlInputRequestTypeDef",
    "DisableControlOutputTypeDef",
    "DriftStatusSummaryTypeDef",
    "EnableBaselineInputRequestTypeDef",
    "EnableBaselineOutputTypeDef",
    "EnableControlInputRequestTypeDef",
    "EnableControlOutputTypeDef",
    "EnabledBaselineDetailsTypeDef",
    "EnabledBaselineFilterTypeDef",
    "EnabledBaselineParameterSummaryTypeDef",
    "EnabledBaselineParameterTypeDef",
    "EnabledBaselineSummaryTypeDef",
    "EnabledControlDetailsTypeDef",
    "EnabledControlFilterTypeDef",
    "EnabledControlParameterSummaryTypeDef",
    "EnabledControlParameterTypeDef",
    "EnabledControlSummaryTypeDef",
    "EnablementStatusSummaryTypeDef",
    "GetBaselineInputRequestTypeDef",
    "GetBaselineOperationInputRequestTypeDef",
    "GetBaselineOperationOutputTypeDef",
    "GetBaselineOutputTypeDef",
    "GetControlOperationInputRequestTypeDef",
    "GetControlOperationOutputTypeDef",
    "GetEnabledBaselineInputRequestTypeDef",
    "GetEnabledBaselineOutputTypeDef",
    "GetEnabledControlInputRequestTypeDef",
    "GetEnabledControlOutputTypeDef",
    "GetLandingZoneInputRequestTypeDef",
    "GetLandingZoneOperationInputRequestTypeDef",
    "GetLandingZoneOperationOutputTypeDef",
    "GetLandingZoneOutputTypeDef",
    "LandingZoneDetailTypeDef",
    "LandingZoneDriftStatusSummaryTypeDef",
    "LandingZoneOperationDetailTypeDef",
    "LandingZoneOperationFilterTypeDef",
    "LandingZoneOperationSummaryTypeDef",
    "LandingZoneSummaryTypeDef",
    "ListBaselinesInputListBaselinesPaginateTypeDef",
    "ListBaselinesInputRequestTypeDef",
    "ListBaselinesOutputTypeDef",
    "ListControlOperationsInputListControlOperationsPaginateTypeDef",
    "ListControlOperationsInputRequestTypeDef",
    "ListControlOperationsOutputTypeDef",
    "ListEnabledBaselinesInputListEnabledBaselinesPaginateTypeDef",
    "ListEnabledBaselinesInputRequestTypeDef",
    "ListEnabledBaselinesOutputTypeDef",
    "ListEnabledControlsInputListEnabledControlsPaginateTypeDef",
    "ListEnabledControlsInputRequestTypeDef",
    "ListEnabledControlsOutputTypeDef",
    "ListLandingZoneOperationsInputListLandingZoneOperationsPaginateTypeDef",
    "ListLandingZoneOperationsInputRequestTypeDef",
    "ListLandingZoneOperationsOutputTypeDef",
    "ListLandingZonesInputListLandingZonesPaginateTypeDef",
    "ListLandingZonesInputRequestTypeDef",
    "ListLandingZonesOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "PaginatorConfigTypeDef",
    "RegionTypeDef",
    "ResetEnabledBaselineInputRequestTypeDef",
    "ResetEnabledBaselineOutputTypeDef",
    "ResetEnabledControlInputRequestTypeDef",
    "ResetEnabledControlOutputTypeDef",
    "ResetLandingZoneInputRequestTypeDef",
    "ResetLandingZoneOutputTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateEnabledBaselineInputRequestTypeDef",
    "UpdateEnabledBaselineOutputTypeDef",
    "UpdateEnabledControlInputRequestTypeDef",
    "UpdateEnabledControlOutputTypeDef",
    "UpdateLandingZoneInputRequestTypeDef",
    "UpdateLandingZoneOutputTypeDef",
)

class BaselineOperationTypeDef(TypedDict):
    endTime: NotRequired[datetime]
    operationIdentifier: NotRequired[str]
    operationType: NotRequired[BaselineOperationTypeType]
    startTime: NotRequired[datetime]
    status: NotRequired[BaselineOperationStatusType]
    statusMessage: NotRequired[str]

class BaselineSummaryTypeDef(TypedDict):
    arn: str
    name: str
    description: NotRequired[str]

class ControlOperationFilterTypeDef(TypedDict):
    controlIdentifiers: NotRequired[Sequence[str]]
    controlOperationTypes: NotRequired[Sequence[ControlOperationTypeType]]
    enabledControlIdentifiers: NotRequired[Sequence[str]]
    statuses: NotRequired[Sequence[ControlOperationStatusType]]
    targetIdentifiers: NotRequired[Sequence[str]]

class ControlOperationSummaryTypeDef(TypedDict):
    controlIdentifier: NotRequired[str]
    enabledControlIdentifier: NotRequired[str]
    endTime: NotRequired[datetime]
    operationIdentifier: NotRequired[str]
    operationType: NotRequired[ControlOperationTypeType]
    startTime: NotRequired[datetime]
    status: NotRequired[ControlOperationStatusType]
    statusMessage: NotRequired[str]
    targetIdentifier: NotRequired[str]

class ControlOperationTypeDef(TypedDict):
    controlIdentifier: NotRequired[str]
    enabledControlIdentifier: NotRequired[str]
    endTime: NotRequired[datetime]
    operationIdentifier: NotRequired[str]
    operationType: NotRequired[ControlOperationTypeType]
    startTime: NotRequired[datetime]
    status: NotRequired[ControlOperationStatusType]
    statusMessage: NotRequired[str]
    targetIdentifier: NotRequired[str]

class CreateLandingZoneInputRequestTypeDef(TypedDict):
    manifest: Mapping[str, Any]
    version: str
    tags: NotRequired[Mapping[str, str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteLandingZoneInputRequestTypeDef(TypedDict):
    landingZoneIdentifier: str

class DisableBaselineInputRequestTypeDef(TypedDict):
    enabledBaselineIdentifier: str

class DisableControlInputRequestTypeDef(TypedDict):
    controlIdentifier: str
    targetIdentifier: str

class DriftStatusSummaryTypeDef(TypedDict):
    driftStatus: NotRequired[DriftStatusType]

class EnabledBaselineParameterTypeDef(TypedDict):
    key: str
    value: Mapping[str, Any]

class EnabledControlParameterTypeDef(TypedDict):
    key: str
    value: Mapping[str, Any]

class EnabledBaselineParameterSummaryTypeDef(TypedDict):
    key: str
    value: Dict[str, Any]

class EnablementStatusSummaryTypeDef(TypedDict):
    lastOperationIdentifier: NotRequired[str]
    status: NotRequired[EnablementStatusType]

class EnabledBaselineFilterTypeDef(TypedDict):
    baselineIdentifiers: NotRequired[Sequence[str]]
    parentIdentifiers: NotRequired[Sequence[str]]
    targetIdentifiers: NotRequired[Sequence[str]]

class EnabledControlParameterSummaryTypeDef(TypedDict):
    key: str
    value: Dict[str, Any]

class RegionTypeDef(TypedDict):
    name: NotRequired[str]

class EnabledControlFilterTypeDef(TypedDict):
    controlIdentifiers: NotRequired[Sequence[str]]
    driftStatuses: NotRequired[Sequence[DriftStatusType]]
    statuses: NotRequired[Sequence[EnablementStatusType]]

class GetBaselineInputRequestTypeDef(TypedDict):
    baselineIdentifier: str

class GetBaselineOperationInputRequestTypeDef(TypedDict):
    operationIdentifier: str

class GetControlOperationInputRequestTypeDef(TypedDict):
    operationIdentifier: str

class GetEnabledBaselineInputRequestTypeDef(TypedDict):
    enabledBaselineIdentifier: str

class GetEnabledControlInputRequestTypeDef(TypedDict):
    enabledControlIdentifier: str

class GetLandingZoneInputRequestTypeDef(TypedDict):
    landingZoneIdentifier: str

class GetLandingZoneOperationInputRequestTypeDef(TypedDict):
    operationIdentifier: str

class LandingZoneOperationDetailTypeDef(TypedDict):
    endTime: NotRequired[datetime]
    operationIdentifier: NotRequired[str]
    operationType: NotRequired[LandingZoneOperationTypeType]
    startTime: NotRequired[datetime]
    status: NotRequired[LandingZoneOperationStatusType]
    statusMessage: NotRequired[str]

class LandingZoneDriftStatusSummaryTypeDef(TypedDict):
    status: NotRequired[LandingZoneDriftStatusType]

LandingZoneOperationFilterTypeDef = TypedDict(
    "LandingZoneOperationFilterTypeDef",
    {
        "statuses": NotRequired[Sequence[LandingZoneOperationStatusType]],
        "types": NotRequired[Sequence[LandingZoneOperationTypeType]],
    },
)

class LandingZoneOperationSummaryTypeDef(TypedDict):
    operationIdentifier: NotRequired[str]
    operationType: NotRequired[LandingZoneOperationTypeType]
    status: NotRequired[LandingZoneOperationStatusType]

class LandingZoneSummaryTypeDef(TypedDict):
    arn: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListBaselinesInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListLandingZonesInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str

class ResetEnabledBaselineInputRequestTypeDef(TypedDict):
    enabledBaselineIdentifier: str

class ResetEnabledControlInputRequestTypeDef(TypedDict):
    enabledControlIdentifier: str

class ResetLandingZoneInputRequestTypeDef(TypedDict):
    landingZoneIdentifier: str

class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateLandingZoneInputRequestTypeDef(TypedDict):
    landingZoneIdentifier: str
    manifest: Mapping[str, Any]
    version: str

ListControlOperationsInputRequestTypeDef = TypedDict(
    "ListControlOperationsInputRequestTypeDef",
    {
        "filter": NotRequired[ControlOperationFilterTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

class CreateLandingZoneOutputTypeDef(TypedDict):
    arn: str
    operationIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteLandingZoneOutputTypeDef(TypedDict):
    operationIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class DisableBaselineOutputTypeDef(TypedDict):
    operationIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class DisableControlOutputTypeDef(TypedDict):
    operationIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class EnableBaselineOutputTypeDef(TypedDict):
    arn: str
    operationIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class EnableControlOutputTypeDef(TypedDict):
    arn: str
    operationIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetBaselineOperationOutputTypeDef(TypedDict):
    baselineOperation: BaselineOperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetBaselineOutputTypeDef(TypedDict):
    arn: str
    description: str
    name: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetControlOperationOutputTypeDef(TypedDict):
    controlOperation: ControlOperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListBaselinesOutputTypeDef(TypedDict):
    baselines: List[BaselineSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListControlOperationsOutputTypeDef(TypedDict):
    controlOperations: List[ControlOperationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ResetEnabledBaselineOutputTypeDef(TypedDict):
    operationIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class ResetEnabledControlOutputTypeDef(TypedDict):
    operationIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class ResetLandingZoneOutputTypeDef(TypedDict):
    operationIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEnabledBaselineOutputTypeDef(TypedDict):
    operationIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEnabledControlOutputTypeDef(TypedDict):
    operationIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateLandingZoneOutputTypeDef(TypedDict):
    operationIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class EnableBaselineInputRequestTypeDef(TypedDict):
    baselineIdentifier: str
    baselineVersion: str
    targetIdentifier: str
    parameters: NotRequired[Sequence[EnabledBaselineParameterTypeDef]]
    tags: NotRequired[Mapping[str, str]]

class UpdateEnabledBaselineInputRequestTypeDef(TypedDict):
    baselineVersion: str
    enabledBaselineIdentifier: str
    parameters: NotRequired[Sequence[EnabledBaselineParameterTypeDef]]

class EnableControlInputRequestTypeDef(TypedDict):
    controlIdentifier: str
    targetIdentifier: str
    parameters: NotRequired[Sequence[EnabledControlParameterTypeDef]]
    tags: NotRequired[Mapping[str, str]]

class UpdateEnabledControlInputRequestTypeDef(TypedDict):
    enabledControlIdentifier: str
    parameters: Sequence[EnabledControlParameterTypeDef]

class EnabledBaselineDetailsTypeDef(TypedDict):
    arn: str
    baselineIdentifier: str
    statusSummary: EnablementStatusSummaryTypeDef
    targetIdentifier: str
    baselineVersion: NotRequired[str]
    parameters: NotRequired[List[EnabledBaselineParameterSummaryTypeDef]]
    parentIdentifier: NotRequired[str]

class EnabledBaselineSummaryTypeDef(TypedDict):
    arn: str
    baselineIdentifier: str
    statusSummary: EnablementStatusSummaryTypeDef
    targetIdentifier: str
    baselineVersion: NotRequired[str]
    parentIdentifier: NotRequired[str]

class EnabledControlSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    controlIdentifier: NotRequired[str]
    driftStatusSummary: NotRequired[DriftStatusSummaryTypeDef]
    statusSummary: NotRequired[EnablementStatusSummaryTypeDef]
    targetIdentifier: NotRequired[str]

ListEnabledBaselinesInputRequestTypeDef = TypedDict(
    "ListEnabledBaselinesInputRequestTypeDef",
    {
        "filter": NotRequired[EnabledBaselineFilterTypeDef],
        "includeChildren": NotRequired[bool],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

class EnabledControlDetailsTypeDef(TypedDict):
    arn: NotRequired[str]
    controlIdentifier: NotRequired[str]
    driftStatusSummary: NotRequired[DriftStatusSummaryTypeDef]
    parameters: NotRequired[List[EnabledControlParameterSummaryTypeDef]]
    statusSummary: NotRequired[EnablementStatusSummaryTypeDef]
    targetIdentifier: NotRequired[str]
    targetRegions: NotRequired[List[RegionTypeDef]]

ListEnabledControlsInputRequestTypeDef = TypedDict(
    "ListEnabledControlsInputRequestTypeDef",
    {
        "filter": NotRequired[EnabledControlFilterTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "targetIdentifier": NotRequired[str],
    },
)

class GetLandingZoneOperationOutputTypeDef(TypedDict):
    operationDetails: LandingZoneOperationDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class LandingZoneDetailTypeDef(TypedDict):
    manifest: Dict[str, Any]
    version: str
    arn: NotRequired[str]
    driftStatus: NotRequired[LandingZoneDriftStatusSummaryTypeDef]
    latestAvailableVersion: NotRequired[str]
    status: NotRequired[LandingZoneStatusType]

ListLandingZoneOperationsInputRequestTypeDef = TypedDict(
    "ListLandingZoneOperationsInputRequestTypeDef",
    {
        "filter": NotRequired[LandingZoneOperationFilterTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

class ListLandingZoneOperationsOutputTypeDef(TypedDict):
    landingZoneOperations: List[LandingZoneOperationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListLandingZonesOutputTypeDef(TypedDict):
    landingZones: List[LandingZoneSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBaselinesInputListBaselinesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListControlOperationsInputListControlOperationsPaginateTypeDef = TypedDict(
    "ListControlOperationsInputListControlOperationsPaginateTypeDef",
    {
        "filter": NotRequired[ControlOperationFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListEnabledBaselinesInputListEnabledBaselinesPaginateTypeDef = TypedDict(
    "ListEnabledBaselinesInputListEnabledBaselinesPaginateTypeDef",
    {
        "filter": NotRequired[EnabledBaselineFilterTypeDef],
        "includeChildren": NotRequired[bool],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListEnabledControlsInputListEnabledControlsPaginateTypeDef = TypedDict(
    "ListEnabledControlsInputListEnabledControlsPaginateTypeDef",
    {
        "filter": NotRequired[EnabledControlFilterTypeDef],
        "targetIdentifier": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListLandingZoneOperationsInputListLandingZoneOperationsPaginateTypeDef = TypedDict(
    "ListLandingZoneOperationsInputListLandingZoneOperationsPaginateTypeDef",
    {
        "filter": NotRequired[LandingZoneOperationFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListLandingZonesInputListLandingZonesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetEnabledBaselineOutputTypeDef(TypedDict):
    enabledBaselineDetails: EnabledBaselineDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListEnabledBaselinesOutputTypeDef(TypedDict):
    enabledBaselines: List[EnabledBaselineSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListEnabledControlsOutputTypeDef(TypedDict):
    enabledControls: List[EnabledControlSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetEnabledControlOutputTypeDef(TypedDict):
    enabledControlDetails: EnabledControlDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetLandingZoneOutputTypeDef(TypedDict):
    landingZone: LandingZoneDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
