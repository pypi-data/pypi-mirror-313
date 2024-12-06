"""
Type annotations for workspaces-thin-client service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/type_defs/)

Usage::

    ```python
    from mypy_boto3_workspaces_thin_client.type_defs import MaintenanceWindowTypeDef

    data: MaintenanceWindowTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ApplyTimeOfType,
    DayOfWeekType,
    DesktopTypeType,
    DeviceSoftwareSetComplianceStatusType,
    DeviceStatusType,
    EnvironmentSoftwareSetComplianceStatusType,
    MaintenanceWindowTypeType,
    SoftwareSetUpdateModeType,
    SoftwareSetUpdateScheduleType,
    SoftwareSetUpdateStatusType,
    SoftwareSetValidationStatusType,
    TargetDeviceStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CreateEnvironmentRequestRequestTypeDef",
    "CreateEnvironmentResponseTypeDef",
    "DeleteDeviceRequestRequestTypeDef",
    "DeleteEnvironmentRequestRequestTypeDef",
    "DeregisterDeviceRequestRequestTypeDef",
    "DeviceSummaryTypeDef",
    "DeviceTypeDef",
    "EnvironmentSummaryTypeDef",
    "EnvironmentTypeDef",
    "GetDeviceRequestRequestTypeDef",
    "GetDeviceResponseTypeDef",
    "GetEnvironmentRequestRequestTypeDef",
    "GetEnvironmentResponseTypeDef",
    "GetSoftwareSetRequestRequestTypeDef",
    "GetSoftwareSetResponseTypeDef",
    "ListDevicesRequestListDevicesPaginateTypeDef",
    "ListDevicesRequestRequestTypeDef",
    "ListDevicesResponseTypeDef",
    "ListEnvironmentsRequestListEnvironmentsPaginateTypeDef",
    "ListEnvironmentsRequestRequestTypeDef",
    "ListEnvironmentsResponseTypeDef",
    "ListSoftwareSetsRequestListSoftwareSetsPaginateTypeDef",
    "ListSoftwareSetsRequestRequestTypeDef",
    "ListSoftwareSetsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MaintenanceWindowOutputTypeDef",
    "MaintenanceWindowTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SoftwareSetSummaryTypeDef",
    "SoftwareSetTypeDef",
    "SoftwareTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDeviceRequestRequestTypeDef",
    "UpdateDeviceResponseTypeDef",
    "UpdateEnvironmentRequestRequestTypeDef",
    "UpdateEnvironmentResponseTypeDef",
    "UpdateSoftwareSetRequestRequestTypeDef",
)

MaintenanceWindowTypeDef = TypedDict(
    "MaintenanceWindowTypeDef",
    {
        "type": NotRequired[MaintenanceWindowTypeType],
        "startTimeHour": NotRequired[int],
        "startTimeMinute": NotRequired[int],
        "endTimeHour": NotRequired[int],
        "endTimeMinute": NotRequired[int],
        "daysOfTheWeek": NotRequired[Sequence[DayOfWeekType]],
        "applyTimeOf": NotRequired[ApplyTimeOfType],
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

DeleteDeviceRequestRequestTypeDef = TypedDict(
    "DeleteDeviceRequestRequestTypeDef",
    {
        "id": str,
        "clientToken": NotRequired[str],
    },
)
DeleteEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteEnvironmentRequestRequestTypeDef",
    {
        "id": str,
        "clientToken": NotRequired[str],
    },
)
DeregisterDeviceRequestRequestTypeDef = TypedDict(
    "DeregisterDeviceRequestRequestTypeDef",
    {
        "id": str,
        "targetDeviceStatus": NotRequired[TargetDeviceStatusType],
        "clientToken": NotRequired[str],
    },
)
DeviceSummaryTypeDef = TypedDict(
    "DeviceSummaryTypeDef",
    {
        "id": NotRequired[str],
        "serialNumber": NotRequired[str],
        "name": NotRequired[str],
        "model": NotRequired[str],
        "environmentId": NotRequired[str],
        "status": NotRequired[DeviceStatusType],
        "currentSoftwareSetId": NotRequired[str],
        "desiredSoftwareSetId": NotRequired[str],
        "pendingSoftwareSetId": NotRequired[str],
        "softwareSetUpdateSchedule": NotRequired[SoftwareSetUpdateScheduleType],
        "lastConnectedAt": NotRequired[datetime],
        "lastPostureAt": NotRequired[datetime],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "arn": NotRequired[str],
    },
)
DeviceTypeDef = TypedDict(
    "DeviceTypeDef",
    {
        "id": NotRequired[str],
        "serialNumber": NotRequired[str],
        "name": NotRequired[str],
        "model": NotRequired[str],
        "environmentId": NotRequired[str],
        "status": NotRequired[DeviceStatusType],
        "currentSoftwareSetId": NotRequired[str],
        "currentSoftwareSetVersion": NotRequired[str],
        "desiredSoftwareSetId": NotRequired[str],
        "pendingSoftwareSetId": NotRequired[str],
        "pendingSoftwareSetVersion": NotRequired[str],
        "softwareSetUpdateSchedule": NotRequired[SoftwareSetUpdateScheduleType],
        "softwareSetComplianceStatus": NotRequired[DeviceSoftwareSetComplianceStatusType],
        "softwareSetUpdateStatus": NotRequired[SoftwareSetUpdateStatusType],
        "lastConnectedAt": NotRequired[datetime],
        "lastPostureAt": NotRequired[datetime],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "arn": NotRequired[str],
        "kmsKeyArn": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
MaintenanceWindowOutputTypeDef = TypedDict(
    "MaintenanceWindowOutputTypeDef",
    {
        "type": NotRequired[MaintenanceWindowTypeType],
        "startTimeHour": NotRequired[int],
        "startTimeMinute": NotRequired[int],
        "endTimeHour": NotRequired[int],
        "endTimeMinute": NotRequired[int],
        "daysOfTheWeek": NotRequired[List[DayOfWeekType]],
        "applyTimeOf": NotRequired[ApplyTimeOfType],
    },
)
GetDeviceRequestRequestTypeDef = TypedDict(
    "GetDeviceRequestRequestTypeDef",
    {
        "id": str,
    },
)
GetEnvironmentRequestRequestTypeDef = TypedDict(
    "GetEnvironmentRequestRequestTypeDef",
    {
        "id": str,
    },
)
GetSoftwareSetRequestRequestTypeDef = TypedDict(
    "GetSoftwareSetRequestRequestTypeDef",
    {
        "id": str,
    },
)

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListDevicesRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListEnvironmentsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListSoftwareSetsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

SoftwareSetSummaryTypeDef = TypedDict(
    "SoftwareSetSummaryTypeDef",
    {
        "id": NotRequired[str],
        "version": NotRequired[str],
        "releasedAt": NotRequired[datetime],
        "supportedUntil": NotRequired[datetime],
        "validationStatus": NotRequired[SoftwareSetValidationStatusType],
        "arn": NotRequired[str],
    },
)

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class SoftwareTypeDef(TypedDict):
    name: NotRequired[str]
    version: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

UpdateDeviceRequestRequestTypeDef = TypedDict(
    "UpdateDeviceRequestRequestTypeDef",
    {
        "id": str,
        "name": NotRequired[str],
        "desiredSoftwareSetId": NotRequired[str],
        "softwareSetUpdateSchedule": NotRequired[SoftwareSetUpdateScheduleType],
    },
)
UpdateSoftwareSetRequestRequestTypeDef = TypedDict(
    "UpdateSoftwareSetRequestRequestTypeDef",
    {
        "id": str,
        "validationStatus": SoftwareSetValidationStatusType,
    },
)

class CreateEnvironmentRequestRequestTypeDef(TypedDict):
    desktopArn: str
    name: NotRequired[str]
    desktopEndpoint: NotRequired[str]
    softwareSetUpdateSchedule: NotRequired[SoftwareSetUpdateScheduleType]
    maintenanceWindow: NotRequired[MaintenanceWindowTypeDef]
    softwareSetUpdateMode: NotRequired[SoftwareSetUpdateModeType]
    desiredSoftwareSetId: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    deviceCreationTags: NotRequired[Mapping[str, str]]

UpdateEnvironmentRequestRequestTypeDef = TypedDict(
    "UpdateEnvironmentRequestRequestTypeDef",
    {
        "id": str,
        "name": NotRequired[str],
        "desktopArn": NotRequired[str],
        "desktopEndpoint": NotRequired[str],
        "softwareSetUpdateSchedule": NotRequired[SoftwareSetUpdateScheduleType],
        "maintenanceWindow": NotRequired[MaintenanceWindowTypeDef],
        "softwareSetUpdateMode": NotRequired[SoftwareSetUpdateModeType],
        "desiredSoftwareSetId": NotRequired[str],
        "deviceCreationTags": NotRequired[Mapping[str, str]],
    },
)

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListDevicesResponseTypeDef(TypedDict):
    devices: List[DeviceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateDeviceResponseTypeDef(TypedDict):
    device: DeviceSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetDeviceResponseTypeDef(TypedDict):
    device: DeviceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

EnvironmentSummaryTypeDef = TypedDict(
    "EnvironmentSummaryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "desktopArn": NotRequired[str],
        "desktopEndpoint": NotRequired[str],
        "desktopType": NotRequired[DesktopTypeType],
        "activationCode": NotRequired[str],
        "softwareSetUpdateSchedule": NotRequired[SoftwareSetUpdateScheduleType],
        "maintenanceWindow": NotRequired[MaintenanceWindowOutputTypeDef],
        "softwareSetUpdateMode": NotRequired[SoftwareSetUpdateModeType],
        "desiredSoftwareSetId": NotRequired[str],
        "pendingSoftwareSetId": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "arn": NotRequired[str],
    },
)
EnvironmentTypeDef = TypedDict(
    "EnvironmentTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "desktopArn": NotRequired[str],
        "desktopEndpoint": NotRequired[str],
        "desktopType": NotRequired[DesktopTypeType],
        "activationCode": NotRequired[str],
        "registeredDevicesCount": NotRequired[int],
        "softwareSetUpdateSchedule": NotRequired[SoftwareSetUpdateScheduleType],
        "maintenanceWindow": NotRequired[MaintenanceWindowOutputTypeDef],
        "softwareSetUpdateMode": NotRequired[SoftwareSetUpdateModeType],
        "desiredSoftwareSetId": NotRequired[str],
        "pendingSoftwareSetId": NotRequired[str],
        "pendingSoftwareSetVersion": NotRequired[str],
        "softwareSetComplianceStatus": NotRequired[EnvironmentSoftwareSetComplianceStatusType],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "arn": NotRequired[str],
        "kmsKeyArn": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "deviceCreationTags": NotRequired[Dict[str, str]],
    },
)

class ListDevicesRequestListDevicesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentsRequestListEnvironmentsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSoftwareSetsRequestListSoftwareSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSoftwareSetsResponseTypeDef(TypedDict):
    softwareSets: List[SoftwareSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

SoftwareSetTypeDef = TypedDict(
    "SoftwareSetTypeDef",
    {
        "id": NotRequired[str],
        "version": NotRequired[str],
        "releasedAt": NotRequired[datetime],
        "supportedUntil": NotRequired[datetime],
        "validationStatus": NotRequired[SoftwareSetValidationStatusType],
        "software": NotRequired[List[SoftwareTypeDef]],
        "arn": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)

class CreateEnvironmentResponseTypeDef(TypedDict):
    environment: EnvironmentSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListEnvironmentsResponseTypeDef(TypedDict):
    environments: List[EnvironmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateEnvironmentResponseTypeDef(TypedDict):
    environment: EnvironmentSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetEnvironmentResponseTypeDef(TypedDict):
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSoftwareSetResponseTypeDef(TypedDict):
    softwareSet: SoftwareSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
