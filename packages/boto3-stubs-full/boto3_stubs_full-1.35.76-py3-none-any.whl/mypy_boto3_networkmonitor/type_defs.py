"""
Type annotations for networkmonitor service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkmonitor/type_defs/)

Usage::

    ```python
    from mypy_boto3_networkmonitor.type_defs import CreateMonitorProbeInputTypeDef

    data: CreateMonitorProbeInputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import AddressFamilyType, MonitorStateType, ProbeStateType, ProtocolType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "CreateMonitorInputRequestTypeDef",
    "CreateMonitorOutputTypeDef",
    "CreateMonitorProbeInputTypeDef",
    "CreateProbeInputRequestTypeDef",
    "CreateProbeOutputTypeDef",
    "DeleteMonitorInputRequestTypeDef",
    "DeleteProbeInputRequestTypeDef",
    "GetMonitorInputRequestTypeDef",
    "GetMonitorOutputTypeDef",
    "GetProbeInputRequestTypeDef",
    "GetProbeOutputTypeDef",
    "ListMonitorsInputListMonitorsPaginateTypeDef",
    "ListMonitorsInputRequestTypeDef",
    "ListMonitorsOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "MonitorSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ProbeInputTypeDef",
    "ProbeTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateMonitorInputRequestTypeDef",
    "UpdateMonitorOutputTypeDef",
    "UpdateProbeInputRequestTypeDef",
    "UpdateProbeOutputTypeDef",
)


class CreateMonitorProbeInputTypeDef(TypedDict):
    sourceArn: str
    destination: str
    protocol: ProtocolType
    destinationPort: NotRequired[int]
    packetSize: NotRequired[int]
    probeTags: NotRequired[Mapping[str, str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ProbeInputTypeDef(TypedDict):
    sourceArn: str
    destination: str
    protocol: ProtocolType
    destinationPort: NotRequired[int]
    packetSize: NotRequired[int]
    tags: NotRequired[Mapping[str, str]]


class DeleteMonitorInputRequestTypeDef(TypedDict):
    monitorName: str


class DeleteProbeInputRequestTypeDef(TypedDict):
    monitorName: str
    probeId: str


class GetMonitorInputRequestTypeDef(TypedDict):
    monitorName: str


class ProbeTypeDef(TypedDict):
    sourceArn: str
    destination: str
    protocol: ProtocolType
    probeId: NotRequired[str]
    probeArn: NotRequired[str]
    destinationPort: NotRequired[int]
    packetSize: NotRequired[int]
    addressFamily: NotRequired[AddressFamilyType]
    vpcId: NotRequired[str]
    state: NotRequired[ProbeStateType]
    createdAt: NotRequired[datetime]
    modifiedAt: NotRequired[datetime]
    tags: NotRequired[Dict[str, str]]


class GetProbeInputRequestTypeDef(TypedDict):
    monitorName: str
    probeId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListMonitorsInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    state: NotRequired[str]


class MonitorSummaryTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    state: MonitorStateType
    aggregationPeriod: NotRequired[int]
    tags: NotRequired[Dict[str, str]]


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str


class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateMonitorInputRequestTypeDef(TypedDict):
    monitorName: str
    aggregationPeriod: int


class UpdateProbeInputRequestTypeDef(TypedDict):
    monitorName: str
    probeId: str
    state: NotRequired[ProbeStateType]
    destination: NotRequired[str]
    destinationPort: NotRequired[int]
    protocol: NotRequired[ProtocolType]
    packetSize: NotRequired[int]


class CreateMonitorInputRequestTypeDef(TypedDict):
    monitorName: str
    probes: NotRequired[Sequence[CreateMonitorProbeInputTypeDef]]
    aggregationPeriod: NotRequired[int]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class CreateMonitorOutputTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    state: MonitorStateType
    aggregationPeriod: int
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProbeOutputTypeDef(TypedDict):
    probeId: str
    probeArn: str
    sourceArn: str
    destination: str
    destinationPort: int
    protocol: ProtocolType
    packetSize: int
    addressFamily: AddressFamilyType
    vpcId: str
    state: ProbeStateType
    createdAt: datetime
    modifiedAt: datetime
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetProbeOutputTypeDef(TypedDict):
    probeId: str
    probeArn: str
    sourceArn: str
    destination: str
    destinationPort: int
    protocol: ProtocolType
    packetSize: int
    addressFamily: AddressFamilyType
    vpcId: str
    state: ProbeStateType
    createdAt: datetime
    modifiedAt: datetime
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMonitorOutputTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    state: MonitorStateType
    aggregationPeriod: int
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateProbeOutputTypeDef(TypedDict):
    probeId: str
    probeArn: str
    sourceArn: str
    destination: str
    destinationPort: int
    protocol: ProtocolType
    packetSize: int
    addressFamily: AddressFamilyType
    vpcId: str
    state: ProbeStateType
    createdAt: datetime
    modifiedAt: datetime
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProbeInputRequestTypeDef(TypedDict):
    monitorName: str
    probe: ProbeInputTypeDef
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class GetMonitorOutputTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    state: MonitorStateType
    aggregationPeriod: int
    tags: Dict[str, str]
    probes: List[ProbeTypeDef]
    createdAt: datetime
    modifiedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ListMonitorsInputListMonitorsPaginateTypeDef(TypedDict):
    state: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMonitorsOutputTypeDef(TypedDict):
    monitors: List[MonitorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
