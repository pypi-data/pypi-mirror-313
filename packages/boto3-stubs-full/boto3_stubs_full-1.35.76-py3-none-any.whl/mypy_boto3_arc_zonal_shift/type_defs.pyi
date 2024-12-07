"""
Type annotations for arc-zonal-shift service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_arc_zonal_shift/type_defs/)

Usage::

    ```python
    from mypy_boto3_arc_zonal_shift.type_defs import AutoshiftInResourceTypeDef

    data: AutoshiftInResourceTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AppliedStatusType,
    AutoshiftAppliedStatusType,
    AutoshiftExecutionStatusType,
    AutoshiftObserverNotificationStatusType,
    PracticeRunOutcomeType,
    ZonalAutoshiftStatusType,
    ZonalShiftStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AutoshiftInResourceTypeDef",
    "AutoshiftSummaryTypeDef",
    "CancelZonalShiftRequestRequestTypeDef",
    "ControlConditionTypeDef",
    "CreatePracticeRunConfigurationRequestRequestTypeDef",
    "CreatePracticeRunConfigurationResponseTypeDef",
    "DeletePracticeRunConfigurationRequestRequestTypeDef",
    "DeletePracticeRunConfigurationResponseTypeDef",
    "GetAutoshiftObserverNotificationStatusResponseTypeDef",
    "GetManagedResourceRequestRequestTypeDef",
    "GetManagedResourceResponseTypeDef",
    "ListAutoshiftsRequestListAutoshiftsPaginateTypeDef",
    "ListAutoshiftsRequestRequestTypeDef",
    "ListAutoshiftsResponseTypeDef",
    "ListManagedResourcesRequestListManagedResourcesPaginateTypeDef",
    "ListManagedResourcesRequestRequestTypeDef",
    "ListManagedResourcesResponseTypeDef",
    "ListZonalShiftsRequestListZonalShiftsPaginateTypeDef",
    "ListZonalShiftsRequestRequestTypeDef",
    "ListZonalShiftsResponseTypeDef",
    "ManagedResourceSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "PracticeRunConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "StartZonalShiftRequestRequestTypeDef",
    "UpdateAutoshiftObserverNotificationStatusRequestRequestTypeDef",
    "UpdateAutoshiftObserverNotificationStatusResponseTypeDef",
    "UpdatePracticeRunConfigurationRequestRequestTypeDef",
    "UpdatePracticeRunConfigurationResponseTypeDef",
    "UpdateZonalAutoshiftConfigurationRequestRequestTypeDef",
    "UpdateZonalAutoshiftConfigurationResponseTypeDef",
    "UpdateZonalShiftRequestRequestTypeDef",
    "ZonalShiftInResourceTypeDef",
    "ZonalShiftSummaryTypeDef",
    "ZonalShiftTypeDef",
)

class AutoshiftInResourceTypeDef(TypedDict):
    appliedStatus: AutoshiftAppliedStatusType
    awayFrom: str
    startTime: datetime

class AutoshiftSummaryTypeDef(TypedDict):
    awayFrom: str
    endTime: datetime
    startTime: datetime
    status: AutoshiftExecutionStatusType

class CancelZonalShiftRequestRequestTypeDef(TypedDict):
    zonalShiftId: str

ControlConditionTypeDef = TypedDict(
    "ControlConditionTypeDef",
    {
        "alarmIdentifier": str,
        "type": Literal["CLOUDWATCH"],
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeletePracticeRunConfigurationRequestRequestTypeDef(TypedDict):
    resourceIdentifier: str

class GetManagedResourceRequestRequestTypeDef(TypedDict):
    resourceIdentifier: str

class ZonalShiftInResourceTypeDef(TypedDict):
    appliedStatus: AppliedStatusType
    awayFrom: str
    comment: str
    expiryTime: datetime
    resourceIdentifier: str
    startTime: datetime
    zonalShiftId: str
    practiceRunOutcome: NotRequired[PracticeRunOutcomeType]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAutoshiftsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[AutoshiftExecutionStatusType]

class ListManagedResourcesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListZonalShiftsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    resourceIdentifier: NotRequired[str]
    status: NotRequired[ZonalShiftStatusType]

class ZonalShiftSummaryTypeDef(TypedDict):
    awayFrom: str
    comment: str
    expiryTime: datetime
    resourceIdentifier: str
    startTime: datetime
    status: ZonalShiftStatusType
    zonalShiftId: str
    practiceRunOutcome: NotRequired[PracticeRunOutcomeType]

class StartZonalShiftRequestRequestTypeDef(TypedDict):
    awayFrom: str
    comment: str
    expiresIn: str
    resourceIdentifier: str

class UpdateAutoshiftObserverNotificationStatusRequestRequestTypeDef(TypedDict):
    status: AutoshiftObserverNotificationStatusType

class UpdateZonalAutoshiftConfigurationRequestRequestTypeDef(TypedDict):
    resourceIdentifier: str
    zonalAutoshiftStatus: ZonalAutoshiftStatusType

class UpdateZonalShiftRequestRequestTypeDef(TypedDict):
    zonalShiftId: str
    comment: NotRequired[str]
    expiresIn: NotRequired[str]

class CreatePracticeRunConfigurationRequestRequestTypeDef(TypedDict):
    outcomeAlarms: Sequence[ControlConditionTypeDef]
    resourceIdentifier: str
    blockedDates: NotRequired[Sequence[str]]
    blockedWindows: NotRequired[Sequence[str]]
    blockingAlarms: NotRequired[Sequence[ControlConditionTypeDef]]

class PracticeRunConfigurationTypeDef(TypedDict):
    outcomeAlarms: List[ControlConditionTypeDef]
    blockedDates: NotRequired[List[str]]
    blockedWindows: NotRequired[List[str]]
    blockingAlarms: NotRequired[List[ControlConditionTypeDef]]

class UpdatePracticeRunConfigurationRequestRequestTypeDef(TypedDict):
    resourceIdentifier: str
    blockedDates: NotRequired[Sequence[str]]
    blockedWindows: NotRequired[Sequence[str]]
    blockingAlarms: NotRequired[Sequence[ControlConditionTypeDef]]
    outcomeAlarms: NotRequired[Sequence[ControlConditionTypeDef]]

class DeletePracticeRunConfigurationResponseTypeDef(TypedDict):
    arn: str
    name: str
    zonalAutoshiftStatus: ZonalAutoshiftStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class GetAutoshiftObserverNotificationStatusResponseTypeDef(TypedDict):
    status: AutoshiftObserverNotificationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ListAutoshiftsResponseTypeDef(TypedDict):
    items: List[AutoshiftSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateAutoshiftObserverNotificationStatusResponseTypeDef(TypedDict):
    status: AutoshiftObserverNotificationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateZonalAutoshiftConfigurationResponseTypeDef(TypedDict):
    resourceIdentifier: str
    zonalAutoshiftStatus: ZonalAutoshiftStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ZonalShiftTypeDef(TypedDict):
    awayFrom: str
    comment: str
    expiryTime: datetime
    resourceIdentifier: str
    startTime: datetime
    status: ZonalShiftStatusType
    zonalShiftId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ManagedResourceSummaryTypeDef(TypedDict):
    availabilityZones: List[str]
    appliedWeights: NotRequired[Dict[str, float]]
    arn: NotRequired[str]
    autoshifts: NotRequired[List[AutoshiftInResourceTypeDef]]
    name: NotRequired[str]
    practiceRunStatus: NotRequired[ZonalAutoshiftStatusType]
    zonalAutoshiftStatus: NotRequired[ZonalAutoshiftStatusType]
    zonalShifts: NotRequired[List[ZonalShiftInResourceTypeDef]]

class ListAutoshiftsRequestListAutoshiftsPaginateTypeDef(TypedDict):
    status: NotRequired[AutoshiftExecutionStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListManagedResourcesRequestListManagedResourcesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListZonalShiftsRequestListZonalShiftsPaginateTypeDef(TypedDict):
    resourceIdentifier: NotRequired[str]
    status: NotRequired[ZonalShiftStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListZonalShiftsResponseTypeDef(TypedDict):
    items: List[ZonalShiftSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreatePracticeRunConfigurationResponseTypeDef(TypedDict):
    arn: str
    name: str
    practiceRunConfiguration: PracticeRunConfigurationTypeDef
    zonalAutoshiftStatus: ZonalAutoshiftStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class GetManagedResourceResponseTypeDef(TypedDict):
    appliedWeights: Dict[str, float]
    arn: str
    autoshifts: List[AutoshiftInResourceTypeDef]
    name: str
    practiceRunConfiguration: PracticeRunConfigurationTypeDef
    zonalAutoshiftStatus: ZonalAutoshiftStatusType
    zonalShifts: List[ZonalShiftInResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePracticeRunConfigurationResponseTypeDef(TypedDict):
    arn: str
    name: str
    practiceRunConfiguration: PracticeRunConfigurationTypeDef
    zonalAutoshiftStatus: ZonalAutoshiftStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ListManagedResourcesResponseTypeDef(TypedDict):
    items: List[ManagedResourceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
