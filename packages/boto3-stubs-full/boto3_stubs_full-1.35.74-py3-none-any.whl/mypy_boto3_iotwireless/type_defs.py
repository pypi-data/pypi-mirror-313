"""
Type annotations for iotwireless service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotwireless/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotwireless.type_defs import SessionKeysAbpV10XTypeDef

    data: SessionKeysAbpV10XTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AggregationPeriodType,
    BatteryLevelType,
    ConnectionStatusType,
    DeviceProfileTypeType,
    DeviceStateType,
    DimensionNameType,
    DlClassType,
    DownlinkModeType,
    EventNotificationResourceTypeType,
    EventNotificationTopicStatusType,
    EventType,
    ExpressionTypeType,
    FuotaDeviceStatusType,
    FuotaTaskStatusType,
    IdentifierTypeType,
    ImportTaskStatusType,
    LogLevelType,
    MessageTypeType,
    MetricNameType,
    MetricQueryStatusType,
    MulticastFrameInfoType,
    OnboardStatusType,
    PositionConfigurationFecType,
    PositionConfigurationStatusType,
    PositioningConfigStatusType,
    PositionResourceTypeType,
    SigningAlgType,
    SummaryMetricConfigurationStatusType,
    SupportedRfRegionType,
    WirelessDeviceEventType,
    WirelessDeviceFrameInfoType,
    WirelessDeviceIdTypeType,
    WirelessDeviceSidewalkStatusType,
    WirelessDeviceTypeType,
    WirelessGatewayEventType,
    WirelessGatewayIdTypeType,
    WirelessGatewayServiceTypeType,
    WirelessGatewayTaskStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AbpV10XTypeDef",
    "AbpV11TypeDef",
    "AccuracyTypeDef",
    "ApplicationConfigTypeDef",
    "AssociateAwsAccountWithPartnerAccountRequestRequestTypeDef",
    "AssociateAwsAccountWithPartnerAccountResponseTypeDef",
    "AssociateMulticastGroupWithFuotaTaskRequestRequestTypeDef",
    "AssociateWirelessDeviceWithFuotaTaskRequestRequestTypeDef",
    "AssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef",
    "AssociateWirelessDeviceWithThingRequestRequestTypeDef",
    "AssociateWirelessGatewayWithCertificateRequestRequestTypeDef",
    "AssociateWirelessGatewayWithCertificateResponseTypeDef",
    "AssociateWirelessGatewayWithThingRequestRequestTypeDef",
    "BeaconingOutputTypeDef",
    "BeaconingTypeDef",
    "BeaconingUnionTypeDef",
    "BlobTypeDef",
    "CancelMulticastGroupSessionRequestRequestTypeDef",
    "CdmaLocalIdTypeDef",
    "CdmaNmrObjTypeDef",
    "CdmaObjTypeDef",
    "CellTowersTypeDef",
    "CertificateListTypeDef",
    "ConnectionStatusEventConfigurationTypeDef",
    "ConnectionStatusResourceTypeEventConfigurationTypeDef",
    "CreateDestinationRequestRequestTypeDef",
    "CreateDestinationResponseTypeDef",
    "CreateDeviceProfileRequestRequestTypeDef",
    "CreateDeviceProfileResponseTypeDef",
    "CreateFuotaTaskRequestRequestTypeDef",
    "CreateFuotaTaskResponseTypeDef",
    "CreateMulticastGroupRequestRequestTypeDef",
    "CreateMulticastGroupResponseTypeDef",
    "CreateNetworkAnalyzerConfigurationRequestRequestTypeDef",
    "CreateNetworkAnalyzerConfigurationResponseTypeDef",
    "CreateServiceProfileRequestRequestTypeDef",
    "CreateServiceProfileResponseTypeDef",
    "CreateWirelessDeviceRequestRequestTypeDef",
    "CreateWirelessDeviceResponseTypeDef",
    "CreateWirelessGatewayRequestRequestTypeDef",
    "CreateWirelessGatewayResponseTypeDef",
    "CreateWirelessGatewayTaskDefinitionRequestRequestTypeDef",
    "CreateWirelessGatewayTaskDefinitionResponseTypeDef",
    "CreateWirelessGatewayTaskRequestRequestTypeDef",
    "CreateWirelessGatewayTaskResponseTypeDef",
    "DakCertificateMetadataTypeDef",
    "DeleteDestinationRequestRequestTypeDef",
    "DeleteDeviceProfileRequestRequestTypeDef",
    "DeleteFuotaTaskRequestRequestTypeDef",
    "DeleteMulticastGroupRequestRequestTypeDef",
    "DeleteNetworkAnalyzerConfigurationRequestRequestTypeDef",
    "DeleteQueuedMessagesRequestRequestTypeDef",
    "DeleteServiceProfileRequestRequestTypeDef",
    "DeleteWirelessDeviceImportTaskRequestRequestTypeDef",
    "DeleteWirelessDeviceRequestRequestTypeDef",
    "DeleteWirelessGatewayRequestRequestTypeDef",
    "DeleteWirelessGatewayTaskDefinitionRequestRequestTypeDef",
    "DeleteWirelessGatewayTaskRequestRequestTypeDef",
    "DeregisterWirelessDeviceRequestRequestTypeDef",
    "DestinationsTypeDef",
    "DeviceProfileTypeDef",
    "DeviceRegistrationStateEventConfigurationTypeDef",
    "DeviceRegistrationStateResourceTypeEventConfigurationTypeDef",
    "DimensionTypeDef",
    "DisassociateAwsAccountFromPartnerAccountRequestRequestTypeDef",
    "DisassociateMulticastGroupFromFuotaTaskRequestRequestTypeDef",
    "DisassociateWirelessDeviceFromFuotaTaskRequestRequestTypeDef",
    "DisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef",
    "DisassociateWirelessDeviceFromThingRequestRequestTypeDef",
    "DisassociateWirelessGatewayFromCertificateRequestRequestTypeDef",
    "DisassociateWirelessGatewayFromThingRequestRequestTypeDef",
    "DownlinkQueueMessageTypeDef",
    "EventConfigurationItemTypeDef",
    "EventNotificationItemConfigurationsTypeDef",
    "FPortsOutputTypeDef",
    "FPortsTypeDef",
    "FPortsUnionTypeDef",
    "FuotaTaskEventLogOptionTypeDef",
    "FuotaTaskLogOptionOutputTypeDef",
    "FuotaTaskLogOptionTypeDef",
    "FuotaTaskLogOptionUnionTypeDef",
    "FuotaTaskTypeDef",
    "GatewayListItemTypeDef",
    "GetDestinationRequestRequestTypeDef",
    "GetDestinationResponseTypeDef",
    "GetDeviceProfileRequestRequestTypeDef",
    "GetDeviceProfileResponseTypeDef",
    "GetEventConfigurationByResourceTypesResponseTypeDef",
    "GetFuotaTaskRequestRequestTypeDef",
    "GetFuotaTaskResponseTypeDef",
    "GetLogLevelsByResourceTypesResponseTypeDef",
    "GetMetricConfigurationResponseTypeDef",
    "GetMetricsRequestRequestTypeDef",
    "GetMetricsResponseTypeDef",
    "GetMulticastGroupRequestRequestTypeDef",
    "GetMulticastGroupResponseTypeDef",
    "GetMulticastGroupSessionRequestRequestTypeDef",
    "GetMulticastGroupSessionResponseTypeDef",
    "GetNetworkAnalyzerConfigurationRequestRequestTypeDef",
    "GetNetworkAnalyzerConfigurationResponseTypeDef",
    "GetPartnerAccountRequestRequestTypeDef",
    "GetPartnerAccountResponseTypeDef",
    "GetPositionConfigurationRequestRequestTypeDef",
    "GetPositionConfigurationResponseTypeDef",
    "GetPositionEstimateRequestRequestTypeDef",
    "GetPositionEstimateResponseTypeDef",
    "GetPositionRequestRequestTypeDef",
    "GetPositionResponseTypeDef",
    "GetResourceEventConfigurationRequestRequestTypeDef",
    "GetResourceEventConfigurationResponseTypeDef",
    "GetResourceLogLevelRequestRequestTypeDef",
    "GetResourceLogLevelResponseTypeDef",
    "GetResourcePositionRequestRequestTypeDef",
    "GetResourcePositionResponseTypeDef",
    "GetServiceEndpointRequestRequestTypeDef",
    "GetServiceEndpointResponseTypeDef",
    "GetServiceProfileRequestRequestTypeDef",
    "GetServiceProfileResponseTypeDef",
    "GetWirelessDeviceImportTaskRequestRequestTypeDef",
    "GetWirelessDeviceImportTaskResponseTypeDef",
    "GetWirelessDeviceRequestRequestTypeDef",
    "GetWirelessDeviceResponseTypeDef",
    "GetWirelessDeviceStatisticsRequestRequestTypeDef",
    "GetWirelessDeviceStatisticsResponseTypeDef",
    "GetWirelessGatewayCertificateRequestRequestTypeDef",
    "GetWirelessGatewayCertificateResponseTypeDef",
    "GetWirelessGatewayFirmwareInformationRequestRequestTypeDef",
    "GetWirelessGatewayFirmwareInformationResponseTypeDef",
    "GetWirelessGatewayRequestRequestTypeDef",
    "GetWirelessGatewayResponseTypeDef",
    "GetWirelessGatewayStatisticsRequestRequestTypeDef",
    "GetWirelessGatewayStatisticsResponseTypeDef",
    "GetWirelessGatewayTaskDefinitionRequestRequestTypeDef",
    "GetWirelessGatewayTaskDefinitionResponseTypeDef",
    "GetWirelessGatewayTaskRequestRequestTypeDef",
    "GetWirelessGatewayTaskResponseTypeDef",
    "GlobalIdentityTypeDef",
    "GnssTypeDef",
    "GsmLocalIdTypeDef",
    "GsmNmrObjTypeDef",
    "GsmObjTypeDef",
    "ImportedSidewalkDeviceTypeDef",
    "ImportedWirelessDeviceTypeDef",
    "IpTypeDef",
    "JoinEventConfigurationTypeDef",
    "JoinResourceTypeEventConfigurationTypeDef",
    "ListDestinationsRequestRequestTypeDef",
    "ListDestinationsResponseTypeDef",
    "ListDeviceProfilesRequestRequestTypeDef",
    "ListDeviceProfilesResponseTypeDef",
    "ListDevicesForWirelessDeviceImportTaskRequestRequestTypeDef",
    "ListDevicesForWirelessDeviceImportTaskResponseTypeDef",
    "ListEventConfigurationsRequestRequestTypeDef",
    "ListEventConfigurationsResponseTypeDef",
    "ListFuotaTasksRequestRequestTypeDef",
    "ListFuotaTasksResponseTypeDef",
    "ListMulticastGroupsByFuotaTaskRequestRequestTypeDef",
    "ListMulticastGroupsByFuotaTaskResponseTypeDef",
    "ListMulticastGroupsRequestRequestTypeDef",
    "ListMulticastGroupsResponseTypeDef",
    "ListNetworkAnalyzerConfigurationsRequestRequestTypeDef",
    "ListNetworkAnalyzerConfigurationsResponseTypeDef",
    "ListPartnerAccountsRequestRequestTypeDef",
    "ListPartnerAccountsResponseTypeDef",
    "ListPositionConfigurationsRequestRequestTypeDef",
    "ListPositionConfigurationsResponseTypeDef",
    "ListQueuedMessagesRequestRequestTypeDef",
    "ListQueuedMessagesResponseTypeDef",
    "ListServiceProfilesRequestRequestTypeDef",
    "ListServiceProfilesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListWirelessDeviceImportTasksRequestRequestTypeDef",
    "ListWirelessDeviceImportTasksResponseTypeDef",
    "ListWirelessDevicesRequestRequestTypeDef",
    "ListWirelessDevicesResponseTypeDef",
    "ListWirelessGatewayTaskDefinitionsRequestRequestTypeDef",
    "ListWirelessGatewayTaskDefinitionsResponseTypeDef",
    "ListWirelessGatewaysRequestRequestTypeDef",
    "ListWirelessGatewaysResponseTypeDef",
    "LoRaWANConnectionStatusEventNotificationConfigurationsTypeDef",
    "LoRaWANConnectionStatusResourceTypeEventConfigurationTypeDef",
    "LoRaWANDeviceMetadataTypeDef",
    "LoRaWANDeviceOutputTypeDef",
    "LoRaWANDeviceProfileOutputTypeDef",
    "LoRaWANDeviceProfileTypeDef",
    "LoRaWANDeviceTypeDef",
    "LoRaWANFuotaTaskGetInfoTypeDef",
    "LoRaWANFuotaTaskTypeDef",
    "LoRaWANGatewayCurrentVersionTypeDef",
    "LoRaWANGatewayMetadataTypeDef",
    "LoRaWANGatewayOutputTypeDef",
    "LoRaWANGatewayTypeDef",
    "LoRaWANGatewayVersionTypeDef",
    "LoRaWANGetServiceProfileInfoTypeDef",
    "LoRaWANJoinEventNotificationConfigurationsTypeDef",
    "LoRaWANJoinResourceTypeEventConfigurationTypeDef",
    "LoRaWANListDeviceTypeDef",
    "LoRaWANMulticastGetTypeDef",
    "LoRaWANMulticastMetadataTypeDef",
    "LoRaWANMulticastSessionOutputTypeDef",
    "LoRaWANMulticastSessionTypeDef",
    "LoRaWANMulticastTypeDef",
    "LoRaWANPublicGatewayMetadataTypeDef",
    "LoRaWANSendDataToDeviceOutputTypeDef",
    "LoRaWANSendDataToDeviceTypeDef",
    "LoRaWANSendDataToDeviceUnionTypeDef",
    "LoRaWANServiceProfileTypeDef",
    "LoRaWANStartFuotaTaskTypeDef",
    "LoRaWANUpdateDeviceTypeDef",
    "LoRaWANUpdateGatewayTaskCreateTypeDef",
    "LoRaWANUpdateGatewayTaskEntryTypeDef",
    "LteLocalIdTypeDef",
    "LteNmrObjTypeDef",
    "LteObjTypeDef",
    "MessageDeliveryStatusEventConfigurationTypeDef",
    "MessageDeliveryStatusResourceTypeEventConfigurationTypeDef",
    "MetricQueryValueTypeDef",
    "MulticastGroupByFuotaTaskTypeDef",
    "MulticastGroupTypeDef",
    "MulticastWirelessMetadataTypeDef",
    "NetworkAnalyzerConfigurationsTypeDef",
    "OtaaV10XTypeDef",
    "OtaaV11TypeDef",
    "ParticipatingGatewaysMulticastOutputTypeDef",
    "ParticipatingGatewaysMulticastTypeDef",
    "ParticipatingGatewaysMulticastUnionTypeDef",
    "ParticipatingGatewaysOutputTypeDef",
    "ParticipatingGatewaysTypeDef",
    "ParticipatingGatewaysUnionTypeDef",
    "PositionConfigurationItemTypeDef",
    "PositionSolverConfigurationsTypeDef",
    "PositionSolverDetailsTypeDef",
    "PositioningTypeDef",
    "ProximityEventConfigurationTypeDef",
    "ProximityResourceTypeEventConfigurationTypeDef",
    "PutPositionConfigurationRequestRequestTypeDef",
    "PutResourceLogLevelRequestRequestTypeDef",
    "ResetResourceLogLevelRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "SemtechGnssConfigurationTypeDef",
    "SemtechGnssDetailTypeDef",
    "SendDataToMulticastGroupRequestRequestTypeDef",
    "SendDataToMulticastGroupResponseTypeDef",
    "SendDataToWirelessDeviceRequestRequestTypeDef",
    "SendDataToWirelessDeviceResponseTypeDef",
    "ServiceProfileTypeDef",
    "SessionKeysAbpV10XTypeDef",
    "SessionKeysAbpV11TypeDef",
    "SidewalkAccountInfoTypeDef",
    "SidewalkAccountInfoWithFingerprintTypeDef",
    "SidewalkCreateWirelessDeviceTypeDef",
    "SidewalkDeviceMetadataTypeDef",
    "SidewalkDeviceTypeDef",
    "SidewalkEventNotificationConfigurationsTypeDef",
    "SidewalkGetDeviceProfileTypeDef",
    "SidewalkGetStartImportInfoTypeDef",
    "SidewalkListDeviceTypeDef",
    "SidewalkResourceTypeEventConfigurationTypeDef",
    "SidewalkSendDataToDeviceTypeDef",
    "SidewalkSingleStartImportInfoTypeDef",
    "SidewalkStartImportInfoTypeDef",
    "SidewalkUpdateAccountTypeDef",
    "SidewalkUpdateImportInfoTypeDef",
    "StartBulkAssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef",
    "StartBulkDisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef",
    "StartFuotaTaskRequestRequestTypeDef",
    "StartMulticastGroupSessionRequestRequestTypeDef",
    "StartSingleWirelessDeviceImportTaskRequestRequestTypeDef",
    "StartSingleWirelessDeviceImportTaskResponseTypeDef",
    "StartWirelessDeviceImportTaskRequestRequestTypeDef",
    "StartWirelessDeviceImportTaskResponseTypeDef",
    "SummaryMetricConfigurationTypeDef",
    "SummaryMetricQueryResultTypeDef",
    "SummaryMetricQueryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TdscdmaLocalIdTypeDef",
    "TdscdmaNmrObjTypeDef",
    "TdscdmaObjTypeDef",
    "TestWirelessDeviceRequestRequestTypeDef",
    "TestWirelessDeviceResponseTypeDef",
    "TimestampTypeDef",
    "TraceContentTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAbpV10XTypeDef",
    "UpdateAbpV11TypeDef",
    "UpdateDestinationRequestRequestTypeDef",
    "UpdateEventConfigurationByResourceTypesRequestRequestTypeDef",
    "UpdateFPortsTypeDef",
    "UpdateFuotaTaskRequestRequestTypeDef",
    "UpdateLogLevelsByResourceTypesRequestRequestTypeDef",
    "UpdateMetricConfigurationRequestRequestTypeDef",
    "UpdateMulticastGroupRequestRequestTypeDef",
    "UpdateNetworkAnalyzerConfigurationRequestRequestTypeDef",
    "UpdatePartnerAccountRequestRequestTypeDef",
    "UpdatePositionRequestRequestTypeDef",
    "UpdateResourceEventConfigurationRequestRequestTypeDef",
    "UpdateResourcePositionRequestRequestTypeDef",
    "UpdateWirelessDeviceImportTaskRequestRequestTypeDef",
    "UpdateWirelessDeviceRequestRequestTypeDef",
    "UpdateWirelessGatewayRequestRequestTypeDef",
    "UpdateWirelessGatewayTaskCreateTypeDef",
    "UpdateWirelessGatewayTaskEntryTypeDef",
    "WcdmaLocalIdTypeDef",
    "WcdmaNmrObjTypeDef",
    "WcdmaObjTypeDef",
    "WiFiAccessPointTypeDef",
    "WirelessDeviceEventLogOptionTypeDef",
    "WirelessDeviceImportTaskTypeDef",
    "WirelessDeviceLogOptionOutputTypeDef",
    "WirelessDeviceLogOptionTypeDef",
    "WirelessDeviceLogOptionUnionTypeDef",
    "WirelessDeviceStatisticsTypeDef",
    "WirelessGatewayEventLogOptionTypeDef",
    "WirelessGatewayLogOptionOutputTypeDef",
    "WirelessGatewayLogOptionTypeDef",
    "WirelessGatewayLogOptionUnionTypeDef",
    "WirelessGatewayStatisticsTypeDef",
    "WirelessMetadataTypeDef",
)


class SessionKeysAbpV10XTypeDef(TypedDict):
    NwkSKey: NotRequired[str]
    AppSKey: NotRequired[str]


class SessionKeysAbpV11TypeDef(TypedDict):
    FNwkSIntKey: NotRequired[str]
    SNwkSIntKey: NotRequired[str]
    NwkSEncKey: NotRequired[str]
    AppSKey: NotRequired[str]


class AccuracyTypeDef(TypedDict):
    HorizontalAccuracy: NotRequired[float]
    VerticalAccuracy: NotRequired[float]


ApplicationConfigTypeDef = TypedDict(
    "ApplicationConfigTypeDef",
    {
        "FPort": NotRequired[int],
        "Type": NotRequired[Literal["SemtechGeolocation"]],
        "DestinationName": NotRequired[str],
    },
)


class SidewalkAccountInfoTypeDef(TypedDict):
    AmazonId: NotRequired[str]
    AppServerPrivateKey: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AssociateMulticastGroupWithFuotaTaskRequestRequestTypeDef(TypedDict):
    Id: str
    MulticastGroupId: str


class AssociateWirelessDeviceWithFuotaTaskRequestRequestTypeDef(TypedDict):
    Id: str
    WirelessDeviceId: str


class AssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef(TypedDict):
    Id: str
    WirelessDeviceId: str


class AssociateWirelessDeviceWithThingRequestRequestTypeDef(TypedDict):
    Id: str
    ThingArn: str


class AssociateWirelessGatewayWithCertificateRequestRequestTypeDef(TypedDict):
    Id: str
    IotCertificateId: str


class AssociateWirelessGatewayWithThingRequestRequestTypeDef(TypedDict):
    Id: str
    ThingArn: str


class BeaconingOutputTypeDef(TypedDict):
    DataRate: NotRequired[int]
    Frequencies: NotRequired[List[int]]


class BeaconingTypeDef(TypedDict):
    DataRate: NotRequired[int]
    Frequencies: NotRequired[Sequence[int]]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class CancelMulticastGroupSessionRequestRequestTypeDef(TypedDict):
    Id: str


class CdmaLocalIdTypeDef(TypedDict):
    PnOffset: int
    CdmaChannel: int


class CdmaNmrObjTypeDef(TypedDict):
    PnOffset: int
    CdmaChannel: int
    PilotPower: NotRequired[int]
    BaseStationId: NotRequired[int]


class CertificateListTypeDef(TypedDict):
    SigningAlg: SigningAlgType
    Value: str


class LoRaWANConnectionStatusEventNotificationConfigurationsTypeDef(TypedDict):
    GatewayEuiEventTopic: NotRequired[EventNotificationTopicStatusType]


class LoRaWANConnectionStatusResourceTypeEventConfigurationTypeDef(TypedDict):
    WirelessGatewayEventTopic: NotRequired[EventNotificationTopicStatusType]


class LoRaWANDeviceProfileTypeDef(TypedDict):
    SupportsClassB: NotRequired[bool]
    ClassBTimeout: NotRequired[int]
    PingSlotPeriod: NotRequired[int]
    PingSlotDr: NotRequired[int]
    PingSlotFreq: NotRequired[int]
    SupportsClassC: NotRequired[bool]
    ClassCTimeout: NotRequired[int]
    MacVersion: NotRequired[str]
    RegParamsRevision: NotRequired[str]
    RxDelay1: NotRequired[int]
    RxDrOffset1: NotRequired[int]
    RxDataRate2: NotRequired[int]
    RxFreq2: NotRequired[int]
    FactoryPresetFreqsList: NotRequired[Sequence[int]]
    MaxEirp: NotRequired[int]
    MaxDutyCycle: NotRequired[int]
    RfRegion: NotRequired[str]
    SupportsJoin: NotRequired[bool]
    Supports32BitFCnt: NotRequired[bool]


class LoRaWANFuotaTaskTypeDef(TypedDict):
    RfRegion: NotRequired[SupportedRfRegionType]


class TraceContentTypeDef(TypedDict):
    WirelessDeviceFrameInfo: NotRequired[WirelessDeviceFrameInfoType]
    LogLevel: NotRequired[LogLevelType]
    MulticastFrameInfo: NotRequired[MulticastFrameInfoType]


class LoRaWANServiceProfileTypeDef(TypedDict):
    AddGwMetadata: NotRequired[bool]
    DrMin: NotRequired[int]
    DrMax: NotRequired[int]
    PrAllowed: NotRequired[bool]
    RaAllowed: NotRequired[bool]


class SidewalkCreateWirelessDeviceTypeDef(TypedDict):
    DeviceProfileId: NotRequired[str]


class CreateWirelessGatewayTaskRequestRequestTypeDef(TypedDict):
    Id: str
    WirelessGatewayTaskDefinitionId: str


class DakCertificateMetadataTypeDef(TypedDict):
    CertificateId: str
    MaxAllowedSignature: NotRequired[int]
    FactorySupport: NotRequired[bool]
    ApId: NotRequired[str]
    DeviceTypeId: NotRequired[str]


class DeleteDestinationRequestRequestTypeDef(TypedDict):
    Name: str


class DeleteDeviceProfileRequestRequestTypeDef(TypedDict):
    Id: str


class DeleteFuotaTaskRequestRequestTypeDef(TypedDict):
    Id: str


class DeleteMulticastGroupRequestRequestTypeDef(TypedDict):
    Id: str


class DeleteNetworkAnalyzerConfigurationRequestRequestTypeDef(TypedDict):
    ConfigurationName: str


class DeleteQueuedMessagesRequestRequestTypeDef(TypedDict):
    Id: str
    MessageId: str
    WirelessDeviceType: NotRequired[WirelessDeviceTypeType]


class DeleteServiceProfileRequestRequestTypeDef(TypedDict):
    Id: str


class DeleteWirelessDeviceImportTaskRequestRequestTypeDef(TypedDict):
    Id: str


class DeleteWirelessDeviceRequestRequestTypeDef(TypedDict):
    Id: str


class DeleteWirelessGatewayRequestRequestTypeDef(TypedDict):
    Id: str


class DeleteWirelessGatewayTaskDefinitionRequestRequestTypeDef(TypedDict):
    Id: str


class DeleteWirelessGatewayTaskRequestRequestTypeDef(TypedDict):
    Id: str


class DeregisterWirelessDeviceRequestRequestTypeDef(TypedDict):
    Identifier: str
    WirelessDeviceType: NotRequired[WirelessDeviceTypeType]


class DestinationsTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]
    ExpressionType: NotRequired[ExpressionTypeType]
    Expression: NotRequired[str]
    Description: NotRequired[str]
    RoleArn: NotRequired[str]


class DeviceProfileTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Id: NotRequired[str]


class SidewalkEventNotificationConfigurationsTypeDef(TypedDict):
    AmazonIdEventTopic: NotRequired[EventNotificationTopicStatusType]


class SidewalkResourceTypeEventConfigurationTypeDef(TypedDict):
    WirelessDeviceEventTopic: NotRequired[EventNotificationTopicStatusType]


class DimensionTypeDef(TypedDict):
    name: NotRequired[DimensionNameType]
    value: NotRequired[str]


class DisassociateAwsAccountFromPartnerAccountRequestRequestTypeDef(TypedDict):
    PartnerAccountId: str
    PartnerType: Literal["Sidewalk"]


class DisassociateMulticastGroupFromFuotaTaskRequestRequestTypeDef(TypedDict):
    Id: str
    MulticastGroupId: str


class DisassociateWirelessDeviceFromFuotaTaskRequestRequestTypeDef(TypedDict):
    Id: str
    WirelessDeviceId: str


class DisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef(TypedDict):
    Id: str
    WirelessDeviceId: str


class DisassociateWirelessDeviceFromThingRequestRequestTypeDef(TypedDict):
    Id: str


class DisassociateWirelessGatewayFromCertificateRequestRequestTypeDef(TypedDict):
    Id: str


class DisassociateWirelessGatewayFromThingRequestRequestTypeDef(TypedDict):
    Id: str


class PositioningTypeDef(TypedDict):
    ClockSync: NotRequired[int]
    Stream: NotRequired[int]
    Gnss: NotRequired[int]


class FuotaTaskEventLogOptionTypeDef(TypedDict):
    Event: Literal["Fuota"]
    LogLevel: LogLevelType


class FuotaTaskTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]


class GatewayListItemTypeDef(TypedDict):
    GatewayId: str
    DownlinkFrequency: int


class GetDestinationRequestRequestTypeDef(TypedDict):
    Name: str


class GetDeviceProfileRequestRequestTypeDef(TypedDict):
    Id: str


class LoRaWANDeviceProfileOutputTypeDef(TypedDict):
    SupportsClassB: NotRequired[bool]
    ClassBTimeout: NotRequired[int]
    PingSlotPeriod: NotRequired[int]
    PingSlotDr: NotRequired[int]
    PingSlotFreq: NotRequired[int]
    SupportsClassC: NotRequired[bool]
    ClassCTimeout: NotRequired[int]
    MacVersion: NotRequired[str]
    RegParamsRevision: NotRequired[str]
    RxDelay1: NotRequired[int]
    RxDrOffset1: NotRequired[int]
    RxDataRate2: NotRequired[int]
    RxFreq2: NotRequired[int]
    FactoryPresetFreqsList: NotRequired[List[int]]
    MaxEirp: NotRequired[int]
    MaxDutyCycle: NotRequired[int]
    RfRegion: NotRequired[str]
    SupportsJoin: NotRequired[bool]
    Supports32BitFCnt: NotRequired[bool]


class GetFuotaTaskRequestRequestTypeDef(TypedDict):
    Id: str


class LoRaWANFuotaTaskGetInfoTypeDef(TypedDict):
    RfRegion: NotRequired[str]
    StartTime: NotRequired[datetime]


class SummaryMetricConfigurationTypeDef(TypedDict):
    Status: NotRequired[SummaryMetricConfigurationStatusType]


class GetMulticastGroupRequestRequestTypeDef(TypedDict):
    Id: str


class GetMulticastGroupSessionRequestRequestTypeDef(TypedDict):
    Id: str


class LoRaWANMulticastSessionOutputTypeDef(TypedDict):
    DlDr: NotRequired[int]
    DlFreq: NotRequired[int]
    SessionStartTime: NotRequired[datetime]
    SessionTimeout: NotRequired[int]
    PingSlotPeriod: NotRequired[int]


class GetNetworkAnalyzerConfigurationRequestRequestTypeDef(TypedDict):
    ConfigurationName: str


class GetPartnerAccountRequestRequestTypeDef(TypedDict):
    PartnerAccountId: str
    PartnerType: Literal["Sidewalk"]


class SidewalkAccountInfoWithFingerprintTypeDef(TypedDict):
    AmazonId: NotRequired[str]
    Fingerprint: NotRequired[str]
    Arn: NotRequired[str]


class GetPositionConfigurationRequestRequestTypeDef(TypedDict):
    ResourceIdentifier: str
    ResourceType: PositionResourceTypeType


class GnssTypeDef(TypedDict):
    Payload: str
    CaptureTime: NotRequired[float]
    CaptureTimeAccuracy: NotRequired[float]
    AssistPosition: NotRequired[Sequence[float]]
    AssistAltitude: NotRequired[float]
    Use2DSolver: NotRequired[bool]


class IpTypeDef(TypedDict):
    IpAddress: str


TimestampTypeDef = Union[datetime, str]


class WiFiAccessPointTypeDef(TypedDict):
    MacAddress: str
    Rss: int


class GetPositionRequestRequestTypeDef(TypedDict):
    ResourceIdentifier: str
    ResourceType: PositionResourceTypeType


class GetResourceEventConfigurationRequestRequestTypeDef(TypedDict):
    Identifier: str
    IdentifierType: IdentifierTypeType
    PartnerType: NotRequired[Literal["Sidewalk"]]


class GetResourceLogLevelRequestRequestTypeDef(TypedDict):
    ResourceIdentifier: str
    ResourceType: str


class GetResourcePositionRequestRequestTypeDef(TypedDict):
    ResourceIdentifier: str
    ResourceType: PositionResourceTypeType


class GetServiceEndpointRequestRequestTypeDef(TypedDict):
    ServiceType: NotRequired[WirelessGatewayServiceTypeType]


class GetServiceProfileRequestRequestTypeDef(TypedDict):
    Id: str


class LoRaWANGetServiceProfileInfoTypeDef(TypedDict):
    UlRate: NotRequired[int]
    UlBucketSize: NotRequired[int]
    UlRatePolicy: NotRequired[str]
    DlRate: NotRequired[int]
    DlBucketSize: NotRequired[int]
    DlRatePolicy: NotRequired[str]
    AddGwMetadata: NotRequired[bool]
    DevStatusReqFreq: NotRequired[int]
    ReportDevStatusBattery: NotRequired[bool]
    ReportDevStatusMargin: NotRequired[bool]
    DrMin: NotRequired[int]
    DrMax: NotRequired[int]
    ChannelMask: NotRequired[str]
    PrAllowed: NotRequired[bool]
    HrAllowed: NotRequired[bool]
    RaAllowed: NotRequired[bool]
    NwkGeoLoc: NotRequired[bool]
    TargetPer: NotRequired[int]
    MinGwDiversity: NotRequired[int]


class GetWirelessDeviceImportTaskRequestRequestTypeDef(TypedDict):
    Id: str


class SidewalkGetStartImportInfoTypeDef(TypedDict):
    DeviceCreationFileList: NotRequired[List[str]]
    Role: NotRequired[str]


class GetWirelessDeviceRequestRequestTypeDef(TypedDict):
    Identifier: str
    IdentifierType: WirelessDeviceIdTypeType


class GetWirelessDeviceStatisticsRequestRequestTypeDef(TypedDict):
    WirelessDeviceId: str


class SidewalkDeviceMetadataTypeDef(TypedDict):
    Rssi: NotRequired[int]
    BatteryLevel: NotRequired[BatteryLevelType]
    Event: NotRequired[EventType]
    DeviceState: NotRequired[DeviceStateType]


class GetWirelessGatewayCertificateRequestRequestTypeDef(TypedDict):
    Id: str


class GetWirelessGatewayFirmwareInformationRequestRequestTypeDef(TypedDict):
    Id: str


class GetWirelessGatewayRequestRequestTypeDef(TypedDict):
    Identifier: str
    IdentifierType: WirelessGatewayIdTypeType


class GetWirelessGatewayStatisticsRequestRequestTypeDef(TypedDict):
    WirelessGatewayId: str


class GetWirelessGatewayTaskDefinitionRequestRequestTypeDef(TypedDict):
    Id: str


class GetWirelessGatewayTaskRequestRequestTypeDef(TypedDict):
    Id: str


class GlobalIdentityTypeDef(TypedDict):
    Lac: int
    GeranCid: int


class GsmLocalIdTypeDef(TypedDict):
    Bsic: int
    Bcch: int


class ImportedSidewalkDeviceTypeDef(TypedDict):
    SidewalkManufacturingSn: NotRequired[str]
    OnboardingStatus: NotRequired[OnboardStatusType]
    OnboardingStatusReason: NotRequired[str]
    LastUpdateTime: NotRequired[datetime]


class LoRaWANJoinEventNotificationConfigurationsTypeDef(TypedDict):
    DevEuiEventTopic: NotRequired[EventNotificationTopicStatusType]


class LoRaWANJoinResourceTypeEventConfigurationTypeDef(TypedDict):
    WirelessDeviceEventTopic: NotRequired[EventNotificationTopicStatusType]


class ListDestinationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListDeviceProfilesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DeviceProfileType: NotRequired[DeviceProfileTypeType]


class ListDevicesForWirelessDeviceImportTaskRequestRequestTypeDef(TypedDict):
    Id: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Status: NotRequired[OnboardStatusType]


class ListEventConfigurationsRequestRequestTypeDef(TypedDict):
    ResourceType: EventNotificationResourceTypeType
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListFuotaTasksRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListMulticastGroupsByFuotaTaskRequestRequestTypeDef(TypedDict):
    Id: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class MulticastGroupByFuotaTaskTypeDef(TypedDict):
    Id: NotRequired[str]


class ListMulticastGroupsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class MulticastGroupTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]


class ListNetworkAnalyzerConfigurationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class NetworkAnalyzerConfigurationsTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]


class ListPartnerAccountsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListPositionConfigurationsRequestRequestTypeDef(TypedDict):
    ResourceType: NotRequired[PositionResourceTypeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListQueuedMessagesRequestRequestTypeDef(TypedDict):
    Id: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    WirelessDeviceType: NotRequired[WirelessDeviceTypeType]


class ListServiceProfilesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ServiceProfileTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Id: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class ListWirelessDeviceImportTasksRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListWirelessDevicesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DestinationName: NotRequired[str]
    DeviceProfileId: NotRequired[str]
    ServiceProfileId: NotRequired[str]
    WirelessDeviceType: NotRequired[WirelessDeviceTypeType]
    FuotaTaskId: NotRequired[str]
    MulticastGroupId: NotRequired[str]


class ListWirelessGatewayTaskDefinitionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    TaskDefinitionType: NotRequired[Literal["UPDATE"]]


class ListWirelessGatewaysRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class LoRaWANGatewayMetadataTypeDef(TypedDict):
    GatewayEui: NotRequired[str]
    Snr: NotRequired[float]
    Rssi: NotRequired[float]


class LoRaWANPublicGatewayMetadataTypeDef(TypedDict):
    ProviderNetId: NotRequired[str]
    Id: NotRequired[str]
    Rssi: NotRequired[float]
    Snr: NotRequired[float]
    RfRegion: NotRequired[str]
    DlAllowed: NotRequired[bool]


class OtaaV10XTypeDef(TypedDict):
    AppKey: NotRequired[str]
    AppEui: NotRequired[str]
    JoinEui: NotRequired[str]
    GenAppKey: NotRequired[str]


class OtaaV11TypeDef(TypedDict):
    AppKey: NotRequired[str]
    NwkKey: NotRequired[str]
    JoinEui: NotRequired[str]


class LoRaWANGatewayVersionTypeDef(TypedDict):
    PackageVersion: NotRequired[str]
    Model: NotRequired[str]
    Station: NotRequired[str]


class LoRaWANListDeviceTypeDef(TypedDict):
    DevEui: NotRequired[str]


class ParticipatingGatewaysMulticastOutputTypeDef(TypedDict):
    GatewayList: NotRequired[List[str]]
    TransmissionInterval: NotRequired[int]


class LoRaWANMulticastMetadataTypeDef(TypedDict):
    FPort: NotRequired[int]


class UpdateAbpV10XTypeDef(TypedDict):
    FCntStart: NotRequired[int]


class UpdateAbpV11TypeDef(TypedDict):
    FCntStart: NotRequired[int]


class LteLocalIdTypeDef(TypedDict):
    Pci: int
    Earfcn: int


class LteNmrObjTypeDef(TypedDict):
    Pci: int
    Earfcn: int
    EutranCid: int
    Rsrp: NotRequired[int]
    Rsrq: NotRequired[float]


class MetricQueryValueTypeDef(TypedDict):
    Min: NotRequired[float]
    Max: NotRequired[float]
    Sum: NotRequired[float]
    Avg: NotRequired[float]
    Std: NotRequired[float]
    P90: NotRequired[float]


class ParticipatingGatewaysMulticastTypeDef(TypedDict):
    GatewayList: NotRequired[Sequence[str]]
    TransmissionInterval: NotRequired[int]


class SemtechGnssConfigurationTypeDef(TypedDict):
    Status: PositionConfigurationStatusType
    Fec: PositionConfigurationFecType


SemtechGnssDetailTypeDef = TypedDict(
    "SemtechGnssDetailTypeDef",
    {
        "Provider": NotRequired[Literal["Semtech"]],
        "Type": NotRequired[Literal["GNSS"]],
        "Status": NotRequired[PositionConfigurationStatusType],
        "Fec": NotRequired[PositionConfigurationFecType],
    },
)


class PutResourceLogLevelRequestRequestTypeDef(TypedDict):
    ResourceIdentifier: str
    ResourceType: str
    LogLevel: LogLevelType


class ResetResourceLogLevelRequestRequestTypeDef(TypedDict):
    ResourceIdentifier: str
    ResourceType: str


class SidewalkSendDataToDeviceTypeDef(TypedDict):
    Seq: NotRequired[int]
    MessageType: NotRequired[MessageTypeType]
    AckModeRetryDurationSecs: NotRequired[int]


class SidewalkSingleStartImportInfoTypeDef(TypedDict):
    SidewalkManufacturingSn: NotRequired[str]


class SidewalkStartImportInfoTypeDef(TypedDict):
    DeviceCreationFile: NotRequired[str]
    Role: NotRequired[str]


class SidewalkUpdateAccountTypeDef(TypedDict):
    AppServerPrivateKey: NotRequired[str]


class SidewalkUpdateImportInfoTypeDef(TypedDict):
    DeviceCreationFile: NotRequired[str]


class TdscdmaLocalIdTypeDef(TypedDict):
    Uarfcn: int
    CellParams: int


class TdscdmaNmrObjTypeDef(TypedDict):
    Uarfcn: int
    CellParams: int
    UtranCid: NotRequired[int]
    Rscp: NotRequired[int]
    PathLoss: NotRequired[int]


class TestWirelessDeviceRequestRequestTypeDef(TypedDict):
    Id: str


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateDestinationRequestRequestTypeDef(TypedDict):
    Name: str
    ExpressionType: NotRequired[ExpressionTypeType]
    Expression: NotRequired[str]
    Description: NotRequired[str]
    RoleArn: NotRequired[str]


class UpdatePositionRequestRequestTypeDef(TypedDict):
    ResourceIdentifier: str
    ResourceType: PositionResourceTypeType
    Position: Sequence[float]


class UpdateWirelessGatewayRequestRequestTypeDef(TypedDict):
    Id: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    JoinEuiFilters: NotRequired[Sequence[Sequence[str]]]
    NetIdFilters: NotRequired[Sequence[str]]
    MaxEirp: NotRequired[float]


class WcdmaLocalIdTypeDef(TypedDict):
    Uarfcndl: int
    Psc: int


class WcdmaNmrObjTypeDef(TypedDict):
    Uarfcndl: int
    Psc: int
    UtranCid: int
    Rscp: NotRequired[int]
    PathLoss: NotRequired[int]


class WirelessDeviceEventLogOptionTypeDef(TypedDict):
    Event: WirelessDeviceEventType
    LogLevel: LogLevelType


class WirelessGatewayEventLogOptionTypeDef(TypedDict):
    Event: WirelessGatewayEventType
    LogLevel: LogLevelType


class AbpV10XTypeDef(TypedDict):
    DevAddr: NotRequired[str]
    SessionKeys: NotRequired[SessionKeysAbpV10XTypeDef]
    FCntStart: NotRequired[int]


class AbpV11TypeDef(TypedDict):
    DevAddr: NotRequired[str]
    SessionKeys: NotRequired[SessionKeysAbpV11TypeDef]
    FCntStart: NotRequired[int]


class AssociateAwsAccountWithPartnerAccountRequestRequestTypeDef(TypedDict):
    Sidewalk: SidewalkAccountInfoTypeDef
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateDestinationRequestRequestTypeDef(TypedDict):
    Name: str
    ExpressionType: ExpressionTypeType
    Expression: str
    RoleArn: str
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientRequestToken: NotRequired[str]


class StartBulkAssociateWirelessDeviceWithMulticastGroupRequestRequestTypeDef(TypedDict):
    Id: str
    QueryString: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class StartBulkDisassociateWirelessDeviceFromMulticastGroupRequestRequestTypeDef(TypedDict):
    Id: str
    QueryString: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


class AssociateAwsAccountWithPartnerAccountResponseTypeDef(TypedDict):
    Sidewalk: SidewalkAccountInfoTypeDef
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateWirelessGatewayWithCertificateResponseTypeDef(TypedDict):
    IotCertificateId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDestinationResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDeviceProfileResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFuotaTaskResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMulticastGroupResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNetworkAnalyzerConfigurationResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateServiceProfileResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWirelessDeviceResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWirelessGatewayResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWirelessGatewayTaskDefinitionResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWirelessGatewayTaskResponseTypeDef(TypedDict):
    WirelessGatewayTaskDefinitionId: str
    Status: WirelessGatewayTaskStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetDestinationResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Expression: str
    ExpressionType: ExpressionTypeType
    Description: str
    RoleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetPositionEstimateResponseTypeDef(TypedDict):
    GeoJsonPayload: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef


class GetPositionResponseTypeDef(TypedDict):
    Position: List[float]
    Accuracy: AccuracyTypeDef
    SolverType: Literal["GNSS"]
    SolverProvider: Literal["Semtech"]
    SolverVersion: str
    Timestamp: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetResourceLogLevelResponseTypeDef(TypedDict):
    LogLevel: LogLevelType
    ResponseMetadata: ResponseMetadataTypeDef


class GetResourcePositionResponseTypeDef(TypedDict):
    GeoJsonPayload: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef


class GetServiceEndpointResponseTypeDef(TypedDict):
    ServiceType: WirelessGatewayServiceTypeType
    ServiceEndpoint: str
    ServerTrust: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetWirelessGatewayCertificateResponseTypeDef(TypedDict):
    IotCertificateId: str
    LoRaWANNetworkServerCertificateId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetWirelessGatewayStatisticsResponseTypeDef(TypedDict):
    WirelessGatewayId: str
    LastUplinkReceivedAt: str
    ConnectionStatus: ConnectionStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetWirelessGatewayTaskResponseTypeDef(TypedDict):
    WirelessGatewayId: str
    WirelessGatewayTaskDefinitionId: str
    LastUplinkReceivedAt: str
    TaskCreatedAt: str
    Status: WirelessGatewayTaskStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class SendDataToMulticastGroupResponseTypeDef(TypedDict):
    MessageId: str
    ResponseMetadata: ResponseMetadataTypeDef


class SendDataToWirelessDeviceResponseTypeDef(TypedDict):
    MessageId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartSingleWirelessDeviceImportTaskResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartWirelessDeviceImportTaskResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class TestWirelessDeviceResponseTypeDef(TypedDict):
    Result: str
    ResponseMetadata: ResponseMetadataTypeDef


class LoRaWANGatewayOutputTypeDef(TypedDict):
    GatewayEui: NotRequired[str]
    RfRegion: NotRequired[str]
    JoinEuiFilters: NotRequired[List[List[str]]]
    NetIdFilters: NotRequired[List[str]]
    SubBands: NotRequired[List[int]]
    Beaconing: NotRequired[BeaconingOutputTypeDef]
    MaxEirp: NotRequired[float]


BeaconingUnionTypeDef = Union[BeaconingTypeDef, BeaconingOutputTypeDef]


class UpdateResourcePositionRequestRequestTypeDef(TypedDict):
    ResourceIdentifier: str
    ResourceType: PositionResourceTypeType
    GeoJsonPayload: NotRequired[BlobTypeDef]


class CdmaObjTypeDef(TypedDict):
    SystemId: int
    NetworkId: int
    BaseStationId: int
    RegistrationZone: NotRequired[int]
    CdmaLocalId: NotRequired[CdmaLocalIdTypeDef]
    PilotPower: NotRequired[int]
    BaseLat: NotRequired[float]
    BaseLng: NotRequired[float]
    CdmaNmr: NotRequired[Sequence[CdmaNmrObjTypeDef]]


class SidewalkDeviceTypeDef(TypedDict):
    AmazonId: NotRequired[str]
    SidewalkId: NotRequired[str]
    SidewalkManufacturingSn: NotRequired[str]
    DeviceCertificates: NotRequired[List[CertificateListTypeDef]]
    PrivateKeys: NotRequired[List[CertificateListTypeDef]]
    DeviceProfileId: NotRequired[str]
    CertificateId: NotRequired[str]
    Status: NotRequired[WirelessDeviceSidewalkStatusType]


class SidewalkListDeviceTypeDef(TypedDict):
    AmazonId: NotRequired[str]
    SidewalkId: NotRequired[str]
    SidewalkManufacturingSn: NotRequired[str]
    DeviceCertificates: NotRequired[List[CertificateListTypeDef]]
    DeviceProfileId: NotRequired[str]
    Status: NotRequired[WirelessDeviceSidewalkStatusType]


class ConnectionStatusEventConfigurationTypeDef(TypedDict):
    LoRaWAN: NotRequired[LoRaWANConnectionStatusEventNotificationConfigurationsTypeDef]
    WirelessGatewayIdEventTopic: NotRequired[EventNotificationTopicStatusType]


class ConnectionStatusResourceTypeEventConfigurationTypeDef(TypedDict):
    LoRaWAN: NotRequired[LoRaWANConnectionStatusResourceTypeEventConfigurationTypeDef]


class CreateDeviceProfileRequestRequestTypeDef(TypedDict):
    Name: NotRequired[str]
    LoRaWAN: NotRequired[LoRaWANDeviceProfileTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientRequestToken: NotRequired[str]
    Sidewalk: NotRequired[Mapping[str, Any]]


class CreateFuotaTaskRequestRequestTypeDef(TypedDict):
    FirmwareUpdateImage: str
    FirmwareUpdateRole: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    LoRaWAN: NotRequired[LoRaWANFuotaTaskTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    RedundancyPercent: NotRequired[int]
    FragmentSizeBytes: NotRequired[int]
    FragmentIntervalMS: NotRequired[int]
    Descriptor: NotRequired[str]


class UpdateFuotaTaskRequestRequestTypeDef(TypedDict):
    Id: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    LoRaWAN: NotRequired[LoRaWANFuotaTaskTypeDef]
    FirmwareUpdateImage: NotRequired[str]
    FirmwareUpdateRole: NotRequired[str]
    RedundancyPercent: NotRequired[int]
    FragmentSizeBytes: NotRequired[int]
    FragmentIntervalMS: NotRequired[int]
    Descriptor: NotRequired[str]


class CreateNetworkAnalyzerConfigurationRequestRequestTypeDef(TypedDict):
    Name: str
    TraceContent: NotRequired[TraceContentTypeDef]
    WirelessDevices: NotRequired[Sequence[str]]
    WirelessGateways: NotRequired[Sequence[str]]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientRequestToken: NotRequired[str]
    MulticastGroups: NotRequired[Sequence[str]]


class GetNetworkAnalyzerConfigurationResponseTypeDef(TypedDict):
    TraceContent: TraceContentTypeDef
    WirelessDevices: List[str]
    WirelessGateways: List[str]
    Description: str
    Arn: str
    Name: str
    MulticastGroups: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateNetworkAnalyzerConfigurationRequestRequestTypeDef(TypedDict):
    ConfigurationName: str
    TraceContent: NotRequired[TraceContentTypeDef]
    WirelessDevicesToAdd: NotRequired[Sequence[str]]
    WirelessDevicesToRemove: NotRequired[Sequence[str]]
    WirelessGatewaysToAdd: NotRequired[Sequence[str]]
    WirelessGatewaysToRemove: NotRequired[Sequence[str]]
    Description: NotRequired[str]
    MulticastGroupsToAdd: NotRequired[Sequence[str]]
    MulticastGroupsToRemove: NotRequired[Sequence[str]]


class CreateServiceProfileRequestRequestTypeDef(TypedDict):
    Name: NotRequired[str]
    LoRaWAN: NotRequired[LoRaWANServiceProfileTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientRequestToken: NotRequired[str]


class SidewalkGetDeviceProfileTypeDef(TypedDict):
    ApplicationServerPublicKey: NotRequired[str]
    QualificationStatus: NotRequired[bool]
    DakCertificateMetadata: NotRequired[List[DakCertificateMetadataTypeDef]]


class ListDestinationsResponseTypeDef(TypedDict):
    DestinationList: List[DestinationsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDeviceProfilesResponseTypeDef(TypedDict):
    DeviceProfileList: List[DeviceProfileTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DeviceRegistrationStateEventConfigurationTypeDef(TypedDict):
    Sidewalk: NotRequired[SidewalkEventNotificationConfigurationsTypeDef]
    WirelessDeviceIdEventTopic: NotRequired[EventNotificationTopicStatusType]


class MessageDeliveryStatusEventConfigurationTypeDef(TypedDict):
    Sidewalk: NotRequired[SidewalkEventNotificationConfigurationsTypeDef]
    WirelessDeviceIdEventTopic: NotRequired[EventNotificationTopicStatusType]


class ProximityEventConfigurationTypeDef(TypedDict):
    Sidewalk: NotRequired[SidewalkEventNotificationConfigurationsTypeDef]
    WirelessDeviceIdEventTopic: NotRequired[EventNotificationTopicStatusType]


class DeviceRegistrationStateResourceTypeEventConfigurationTypeDef(TypedDict):
    Sidewalk: NotRequired[SidewalkResourceTypeEventConfigurationTypeDef]


class MessageDeliveryStatusResourceTypeEventConfigurationTypeDef(TypedDict):
    Sidewalk: NotRequired[SidewalkResourceTypeEventConfigurationTypeDef]


class ProximityResourceTypeEventConfigurationTypeDef(TypedDict):
    Sidewalk: NotRequired[SidewalkResourceTypeEventConfigurationTypeDef]


class FPortsOutputTypeDef(TypedDict):
    Fuota: NotRequired[int]
    Multicast: NotRequired[int]
    ClockSync: NotRequired[int]
    Positioning: NotRequired[PositioningTypeDef]
    Applications: NotRequired[List[ApplicationConfigTypeDef]]


class FPortsTypeDef(TypedDict):
    Fuota: NotRequired[int]
    Multicast: NotRequired[int]
    ClockSync: NotRequired[int]
    Positioning: NotRequired[PositioningTypeDef]
    Applications: NotRequired[Sequence[ApplicationConfigTypeDef]]


class UpdateFPortsTypeDef(TypedDict):
    Positioning: NotRequired[PositioningTypeDef]
    Applications: NotRequired[Sequence[ApplicationConfigTypeDef]]


FuotaTaskLogOptionOutputTypeDef = TypedDict(
    "FuotaTaskLogOptionOutputTypeDef",
    {
        "Type": Literal["LoRaWAN"],
        "LogLevel": LogLevelType,
        "Events": NotRequired[List[FuotaTaskEventLogOptionTypeDef]],
    },
)
FuotaTaskLogOptionTypeDef = TypedDict(
    "FuotaTaskLogOptionTypeDef",
    {
        "Type": Literal["LoRaWAN"],
        "LogLevel": LogLevelType,
        "Events": NotRequired[Sequence[FuotaTaskEventLogOptionTypeDef]],
    },
)


class ListFuotaTasksResponseTypeDef(TypedDict):
    FuotaTaskList: List[FuotaTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ParticipatingGatewaysOutputTypeDef(TypedDict):
    DownlinkMode: DownlinkModeType
    GatewayList: List[GatewayListItemTypeDef]
    TransmissionInterval: int


class ParticipatingGatewaysTypeDef(TypedDict):
    DownlinkMode: DownlinkModeType
    GatewayList: Sequence[GatewayListItemTypeDef]
    TransmissionInterval: int


class GetFuotaTaskResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    Status: FuotaTaskStatusType
    Name: str
    Description: str
    LoRaWAN: LoRaWANFuotaTaskGetInfoTypeDef
    FirmwareUpdateImage: str
    FirmwareUpdateRole: str
    CreatedAt: datetime
    RedundancyPercent: int
    FragmentSizeBytes: int
    FragmentIntervalMS: int
    Descriptor: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetMetricConfigurationResponseTypeDef(TypedDict):
    SummaryMetric: SummaryMetricConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMetricConfigurationRequestRequestTypeDef(TypedDict):
    SummaryMetric: NotRequired[SummaryMetricConfigurationTypeDef]


class GetMulticastGroupSessionResponseTypeDef(TypedDict):
    LoRaWAN: LoRaWANMulticastSessionOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetPartnerAccountResponseTypeDef(TypedDict):
    Sidewalk: SidewalkAccountInfoWithFingerprintTypeDef
    AccountLinked: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ListPartnerAccountsResponseTypeDef(TypedDict):
    Sidewalk: List[SidewalkAccountInfoWithFingerprintTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LoRaWANMulticastSessionTypeDef(TypedDict):
    DlDr: NotRequired[int]
    DlFreq: NotRequired[int]
    SessionStartTime: NotRequired[TimestampTypeDef]
    SessionTimeout: NotRequired[int]
    PingSlotPeriod: NotRequired[int]


class LoRaWANStartFuotaTaskTypeDef(TypedDict):
    StartTime: NotRequired[TimestampTypeDef]


class SummaryMetricQueryTypeDef(TypedDict):
    QueryId: NotRequired[str]
    MetricName: NotRequired[MetricNameType]
    Dimensions: NotRequired[Sequence[DimensionTypeDef]]
    AggregationPeriod: NotRequired[AggregationPeriodType]
    StartTimestamp: NotRequired[TimestampTypeDef]
    EndTimestamp: NotRequired[TimestampTypeDef]


class GetServiceProfileResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Id: str
    LoRaWAN: LoRaWANGetServiceProfileInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetWirelessDeviceImportTaskResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    DestinationName: str
    Sidewalk: SidewalkGetStartImportInfoTypeDef
    CreationTime: datetime
    Status: ImportTaskStatusType
    StatusReason: str
    InitializedImportedDeviceCount: int
    PendingImportedDeviceCount: int
    OnboardedImportedDeviceCount: int
    FailedImportedDeviceCount: int
    ResponseMetadata: ResponseMetadataTypeDef


class WirelessDeviceImportTaskTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    DestinationName: NotRequired[str]
    Sidewalk: NotRequired[SidewalkGetStartImportInfoTypeDef]
    CreationTime: NotRequired[datetime]
    Status: NotRequired[ImportTaskStatusType]
    StatusReason: NotRequired[str]
    InitializedImportedDeviceCount: NotRequired[int]
    PendingImportedDeviceCount: NotRequired[int]
    OnboardedImportedDeviceCount: NotRequired[int]
    FailedImportedDeviceCount: NotRequired[int]


class GsmNmrObjTypeDef(TypedDict):
    Bsic: int
    Bcch: int
    RxLevel: NotRequired[int]
    GlobalIdentity: NotRequired[GlobalIdentityTypeDef]


class ImportedWirelessDeviceTypeDef(TypedDict):
    Sidewalk: NotRequired[ImportedSidewalkDeviceTypeDef]


class JoinEventConfigurationTypeDef(TypedDict):
    LoRaWAN: NotRequired[LoRaWANJoinEventNotificationConfigurationsTypeDef]
    WirelessDeviceIdEventTopic: NotRequired[EventNotificationTopicStatusType]


class JoinResourceTypeEventConfigurationTypeDef(TypedDict):
    LoRaWAN: NotRequired[LoRaWANJoinResourceTypeEventConfigurationTypeDef]


class ListMulticastGroupsByFuotaTaskResponseTypeDef(TypedDict):
    MulticastGroupList: List[MulticastGroupByFuotaTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMulticastGroupsResponseTypeDef(TypedDict):
    MulticastGroupList: List[MulticastGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListNetworkAnalyzerConfigurationsResponseTypeDef(TypedDict):
    NetworkAnalyzerConfigurationList: List[NetworkAnalyzerConfigurationsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListServiceProfilesResponseTypeDef(TypedDict):
    ServiceProfileList: List[ServiceProfileTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LoRaWANDeviceMetadataTypeDef(TypedDict):
    DevEui: NotRequired[str]
    FPort: NotRequired[int]
    DataRate: NotRequired[int]
    Frequency: NotRequired[int]
    Timestamp: NotRequired[str]
    Gateways: NotRequired[List[LoRaWANGatewayMetadataTypeDef]]
    PublicGateways: NotRequired[List[LoRaWANPublicGatewayMetadataTypeDef]]


class LoRaWANGatewayCurrentVersionTypeDef(TypedDict):
    CurrentVersion: NotRequired[LoRaWANGatewayVersionTypeDef]


class LoRaWANUpdateGatewayTaskCreateTypeDef(TypedDict):
    UpdateSignature: NotRequired[str]
    SigKeyCrc: NotRequired[int]
    CurrentVersion: NotRequired[LoRaWANGatewayVersionTypeDef]
    UpdateVersion: NotRequired[LoRaWANGatewayVersionTypeDef]


class LoRaWANUpdateGatewayTaskEntryTypeDef(TypedDict):
    CurrentVersion: NotRequired[LoRaWANGatewayVersionTypeDef]
    UpdateVersion: NotRequired[LoRaWANGatewayVersionTypeDef]


class LoRaWANMulticastGetTypeDef(TypedDict):
    RfRegion: NotRequired[SupportedRfRegionType]
    DlClass: NotRequired[DlClassType]
    NumberOfDevicesRequested: NotRequired[int]
    NumberOfDevicesInGroup: NotRequired[int]
    ParticipatingGateways: NotRequired[ParticipatingGatewaysMulticastOutputTypeDef]


class MulticastWirelessMetadataTypeDef(TypedDict):
    LoRaWAN: NotRequired[LoRaWANMulticastMetadataTypeDef]


class LteObjTypeDef(TypedDict):
    Mcc: int
    Mnc: int
    EutranCid: int
    Tac: NotRequired[int]
    LteLocalId: NotRequired[LteLocalIdTypeDef]
    LteTimingAdvance: NotRequired[int]
    Rsrp: NotRequired[int]
    Rsrq: NotRequired[float]
    NrCapable: NotRequired[bool]
    LteNmr: NotRequired[Sequence[LteNmrObjTypeDef]]


class SummaryMetricQueryResultTypeDef(TypedDict):
    QueryId: NotRequired[str]
    QueryStatus: NotRequired[MetricQueryStatusType]
    Error: NotRequired[str]
    MetricName: NotRequired[MetricNameType]
    Dimensions: NotRequired[List[DimensionTypeDef]]
    AggregationPeriod: NotRequired[AggregationPeriodType]
    StartTimestamp: NotRequired[datetime]
    EndTimestamp: NotRequired[datetime]
    Timestamps: NotRequired[List[datetime]]
    Values: NotRequired[List[MetricQueryValueTypeDef]]
    Unit: NotRequired[str]


ParticipatingGatewaysMulticastUnionTypeDef = Union[
    ParticipatingGatewaysMulticastTypeDef, ParticipatingGatewaysMulticastOutputTypeDef
]


class PositionSolverConfigurationsTypeDef(TypedDict):
    SemtechGnss: NotRequired[SemtechGnssConfigurationTypeDef]


class PositionSolverDetailsTypeDef(TypedDict):
    SemtechGnss: NotRequired[SemtechGnssDetailTypeDef]


class StartSingleWirelessDeviceImportTaskRequestRequestTypeDef(TypedDict):
    DestinationName: str
    Sidewalk: SidewalkSingleStartImportInfoTypeDef
    ClientRequestToken: NotRequired[str]
    DeviceName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class StartWirelessDeviceImportTaskRequestRequestTypeDef(TypedDict):
    DestinationName: str
    Sidewalk: SidewalkStartImportInfoTypeDef
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdatePartnerAccountRequestRequestTypeDef(TypedDict):
    Sidewalk: SidewalkUpdateAccountTypeDef
    PartnerAccountId: str
    PartnerType: Literal["Sidewalk"]


class UpdateWirelessDeviceImportTaskRequestRequestTypeDef(TypedDict):
    Id: str
    Sidewalk: SidewalkUpdateImportInfoTypeDef


class TdscdmaObjTypeDef(TypedDict):
    Mcc: int
    Mnc: int
    UtranCid: int
    Lac: NotRequired[int]
    TdscdmaLocalId: NotRequired[TdscdmaLocalIdTypeDef]
    TdscdmaTimingAdvance: NotRequired[int]
    Rscp: NotRequired[int]
    PathLoss: NotRequired[int]
    TdscdmaNmr: NotRequired[Sequence[TdscdmaNmrObjTypeDef]]


class WcdmaObjTypeDef(TypedDict):
    Mcc: int
    Mnc: int
    UtranCid: int
    Lac: NotRequired[int]
    WcdmaLocalId: NotRequired[WcdmaLocalIdTypeDef]
    Rscp: NotRequired[int]
    PathLoss: NotRequired[int]
    WcdmaNmr: NotRequired[Sequence[WcdmaNmrObjTypeDef]]


WirelessDeviceLogOptionOutputTypeDef = TypedDict(
    "WirelessDeviceLogOptionOutputTypeDef",
    {
        "Type": WirelessDeviceTypeType,
        "LogLevel": LogLevelType,
        "Events": NotRequired[List[WirelessDeviceEventLogOptionTypeDef]],
    },
)
WirelessDeviceLogOptionTypeDef = TypedDict(
    "WirelessDeviceLogOptionTypeDef",
    {
        "Type": WirelessDeviceTypeType,
        "LogLevel": LogLevelType,
        "Events": NotRequired[Sequence[WirelessDeviceEventLogOptionTypeDef]],
    },
)
WirelessGatewayLogOptionOutputTypeDef = TypedDict(
    "WirelessGatewayLogOptionOutputTypeDef",
    {
        "Type": Literal["LoRaWAN"],
        "LogLevel": LogLevelType,
        "Events": NotRequired[List[WirelessGatewayEventLogOptionTypeDef]],
    },
)
WirelessGatewayLogOptionTypeDef = TypedDict(
    "WirelessGatewayLogOptionTypeDef",
    {
        "Type": Literal["LoRaWAN"],
        "LogLevel": LogLevelType,
        "Events": NotRequired[Sequence[WirelessGatewayEventLogOptionTypeDef]],
    },
)


class GetWirelessGatewayResponseTypeDef(TypedDict):
    Name: str
    Id: str
    Description: str
    LoRaWAN: LoRaWANGatewayOutputTypeDef
    Arn: str
    ThingName: str
    ThingArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class WirelessGatewayStatisticsTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    LoRaWAN: NotRequired[LoRaWANGatewayOutputTypeDef]
    LastUplinkReceivedAt: NotRequired[str]


class LoRaWANGatewayTypeDef(TypedDict):
    GatewayEui: NotRequired[str]
    RfRegion: NotRequired[str]
    JoinEuiFilters: NotRequired[Sequence[Sequence[str]]]
    NetIdFilters: NotRequired[Sequence[str]]
    SubBands: NotRequired[Sequence[int]]
    Beaconing: NotRequired[BeaconingUnionTypeDef]
    MaxEirp: NotRequired[float]


WirelessDeviceStatisticsTypeDef = TypedDict(
    "WirelessDeviceStatisticsTypeDef",
    {
        "Arn": NotRequired[str],
        "Id": NotRequired[str],
        "Type": NotRequired[WirelessDeviceTypeType],
        "Name": NotRequired[str],
        "DestinationName": NotRequired[str],
        "LastUplinkReceivedAt": NotRequired[str],
        "LoRaWAN": NotRequired[LoRaWANListDeviceTypeDef],
        "Sidewalk": NotRequired[SidewalkListDeviceTypeDef],
        "FuotaDeviceStatus": NotRequired[FuotaDeviceStatusType],
        "MulticastDeviceStatus": NotRequired[str],
        "McGroupId": NotRequired[int],
    },
)


class GetDeviceProfileResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Id: str
    LoRaWAN: LoRaWANDeviceProfileOutputTypeDef
    Sidewalk: SidewalkGetDeviceProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class LoRaWANDeviceOutputTypeDef(TypedDict):
    DevEui: NotRequired[str]
    DeviceProfileId: NotRequired[str]
    ServiceProfileId: NotRequired[str]
    OtaaV1_1: NotRequired[OtaaV11TypeDef]
    OtaaV1_0_x: NotRequired[OtaaV10XTypeDef]
    AbpV1_1: NotRequired[AbpV11TypeDef]
    AbpV1_0_x: NotRequired[AbpV10XTypeDef]
    FPorts: NotRequired[FPortsOutputTypeDef]


FPortsUnionTypeDef = Union[FPortsTypeDef, FPortsOutputTypeDef]


class LoRaWANUpdateDeviceTypeDef(TypedDict):
    DeviceProfileId: NotRequired[str]
    ServiceProfileId: NotRequired[str]
    AbpV1_1: NotRequired[UpdateAbpV11TypeDef]
    AbpV1_0_x: NotRequired[UpdateAbpV10XTypeDef]
    FPorts: NotRequired[UpdateFPortsTypeDef]


FuotaTaskLogOptionUnionTypeDef = Union[FuotaTaskLogOptionTypeDef, FuotaTaskLogOptionOutputTypeDef]


class LoRaWANSendDataToDeviceOutputTypeDef(TypedDict):
    FPort: NotRequired[int]
    ParticipatingGateways: NotRequired[ParticipatingGatewaysOutputTypeDef]


ParticipatingGatewaysUnionTypeDef = Union[
    ParticipatingGatewaysTypeDef, ParticipatingGatewaysOutputTypeDef
]


class StartMulticastGroupSessionRequestRequestTypeDef(TypedDict):
    Id: str
    LoRaWAN: LoRaWANMulticastSessionTypeDef


class StartFuotaTaskRequestRequestTypeDef(TypedDict):
    Id: str
    LoRaWAN: NotRequired[LoRaWANStartFuotaTaskTypeDef]


class GetMetricsRequestRequestTypeDef(TypedDict):
    SummaryMetricQueries: NotRequired[Sequence[SummaryMetricQueryTypeDef]]


class ListWirelessDeviceImportTasksResponseTypeDef(TypedDict):
    WirelessDeviceImportTaskList: List[WirelessDeviceImportTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GsmObjTypeDef(TypedDict):
    Mcc: int
    Mnc: int
    Lac: int
    GeranCid: int
    GsmLocalId: NotRequired[GsmLocalIdTypeDef]
    GsmTimingAdvance: NotRequired[int]
    RxLevel: NotRequired[int]
    GsmNmr: NotRequired[Sequence[GsmNmrObjTypeDef]]


class ListDevicesForWirelessDeviceImportTaskResponseTypeDef(TypedDict):
    DestinationName: str
    ImportedWirelessDeviceList: List[ImportedWirelessDeviceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class EventNotificationItemConfigurationsTypeDef(TypedDict):
    DeviceRegistrationState: NotRequired[DeviceRegistrationStateEventConfigurationTypeDef]
    Proximity: NotRequired[ProximityEventConfigurationTypeDef]
    Join: NotRequired[JoinEventConfigurationTypeDef]
    ConnectionStatus: NotRequired[ConnectionStatusEventConfigurationTypeDef]
    MessageDeliveryStatus: NotRequired[MessageDeliveryStatusEventConfigurationTypeDef]


class GetResourceEventConfigurationResponseTypeDef(TypedDict):
    DeviceRegistrationState: DeviceRegistrationStateEventConfigurationTypeDef
    Proximity: ProximityEventConfigurationTypeDef
    Join: JoinEventConfigurationTypeDef
    ConnectionStatus: ConnectionStatusEventConfigurationTypeDef
    MessageDeliveryStatus: MessageDeliveryStatusEventConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateResourceEventConfigurationRequestRequestTypeDef(TypedDict):
    Identifier: str
    IdentifierType: IdentifierTypeType
    PartnerType: NotRequired[Literal["Sidewalk"]]
    DeviceRegistrationState: NotRequired[DeviceRegistrationStateEventConfigurationTypeDef]
    Proximity: NotRequired[ProximityEventConfigurationTypeDef]
    Join: NotRequired[JoinEventConfigurationTypeDef]
    ConnectionStatus: NotRequired[ConnectionStatusEventConfigurationTypeDef]
    MessageDeliveryStatus: NotRequired[MessageDeliveryStatusEventConfigurationTypeDef]


class GetEventConfigurationByResourceTypesResponseTypeDef(TypedDict):
    DeviceRegistrationState: DeviceRegistrationStateResourceTypeEventConfigurationTypeDef
    Proximity: ProximityResourceTypeEventConfigurationTypeDef
    Join: JoinResourceTypeEventConfigurationTypeDef
    ConnectionStatus: ConnectionStatusResourceTypeEventConfigurationTypeDef
    MessageDeliveryStatus: MessageDeliveryStatusResourceTypeEventConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEventConfigurationByResourceTypesRequestRequestTypeDef(TypedDict):
    DeviceRegistrationState: NotRequired[
        DeviceRegistrationStateResourceTypeEventConfigurationTypeDef
    ]
    Proximity: NotRequired[ProximityResourceTypeEventConfigurationTypeDef]
    Join: NotRequired[JoinResourceTypeEventConfigurationTypeDef]
    ConnectionStatus: NotRequired[ConnectionStatusResourceTypeEventConfigurationTypeDef]
    MessageDeliveryStatus: NotRequired[MessageDeliveryStatusResourceTypeEventConfigurationTypeDef]


class GetWirelessDeviceStatisticsResponseTypeDef(TypedDict):
    WirelessDeviceId: str
    LastUplinkReceivedAt: str
    LoRaWAN: LoRaWANDeviceMetadataTypeDef
    Sidewalk: SidewalkDeviceMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetWirelessGatewayFirmwareInformationResponseTypeDef(TypedDict):
    LoRaWAN: LoRaWANGatewayCurrentVersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateWirelessGatewayTaskCreateTypeDef(TypedDict):
    UpdateDataSource: NotRequired[str]
    UpdateDataRole: NotRequired[str]
    LoRaWAN: NotRequired[LoRaWANUpdateGatewayTaskCreateTypeDef]


class UpdateWirelessGatewayTaskEntryTypeDef(TypedDict):
    Id: NotRequired[str]
    LoRaWAN: NotRequired[LoRaWANUpdateGatewayTaskEntryTypeDef]
    Arn: NotRequired[str]


class GetMulticastGroupResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    Name: str
    Description: str
    Status: str
    LoRaWAN: LoRaWANMulticastGetTypeDef
    CreatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class SendDataToMulticastGroupRequestRequestTypeDef(TypedDict):
    Id: str
    PayloadData: str
    WirelessMetadata: MulticastWirelessMetadataTypeDef


class GetMetricsResponseTypeDef(TypedDict):
    SummaryMetricQueryResults: List[SummaryMetricQueryResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class LoRaWANMulticastTypeDef(TypedDict):
    RfRegion: NotRequired[SupportedRfRegionType]
    DlClass: NotRequired[DlClassType]
    ParticipatingGateways: NotRequired[ParticipatingGatewaysMulticastUnionTypeDef]


class PutPositionConfigurationRequestRequestTypeDef(TypedDict):
    ResourceIdentifier: str
    ResourceType: PositionResourceTypeType
    Solvers: NotRequired[PositionSolverConfigurationsTypeDef]
    Destination: NotRequired[str]


class GetPositionConfigurationResponseTypeDef(TypedDict):
    Solvers: PositionSolverDetailsTypeDef
    Destination: str
    ResponseMetadata: ResponseMetadataTypeDef


class PositionConfigurationItemTypeDef(TypedDict):
    ResourceIdentifier: NotRequired[str]
    ResourceType: NotRequired[PositionResourceTypeType]
    Solvers: NotRequired[PositionSolverDetailsTypeDef]
    Destination: NotRequired[str]


WirelessDeviceLogOptionUnionTypeDef = Union[
    WirelessDeviceLogOptionTypeDef, WirelessDeviceLogOptionOutputTypeDef
]


class GetLogLevelsByResourceTypesResponseTypeDef(TypedDict):
    DefaultLogLevel: LogLevelType
    WirelessGatewayLogOptions: List[WirelessGatewayLogOptionOutputTypeDef]
    WirelessDeviceLogOptions: List[WirelessDeviceLogOptionOutputTypeDef]
    FuotaTaskLogOptions: List[FuotaTaskLogOptionOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


WirelessGatewayLogOptionUnionTypeDef = Union[
    WirelessGatewayLogOptionTypeDef, WirelessGatewayLogOptionOutputTypeDef
]


class ListWirelessGatewaysResponseTypeDef(TypedDict):
    WirelessGatewayList: List[WirelessGatewayStatisticsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateWirelessGatewayRequestRequestTypeDef(TypedDict):
    LoRaWAN: LoRaWANGatewayTypeDef
    Name: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientRequestToken: NotRequired[str]


class ListWirelessDevicesResponseTypeDef(TypedDict):
    WirelessDeviceList: List[WirelessDeviceStatisticsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


GetWirelessDeviceResponseTypeDef = TypedDict(
    "GetWirelessDeviceResponseTypeDef",
    {
        "Type": WirelessDeviceTypeType,
        "Name": str,
        "Description": str,
        "DestinationName": str,
        "Id": str,
        "Arn": str,
        "ThingName": str,
        "ThingArn": str,
        "LoRaWAN": LoRaWANDeviceOutputTypeDef,
        "Sidewalk": SidewalkDeviceTypeDef,
        "Positioning": PositioningConfigStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class LoRaWANDeviceTypeDef(TypedDict):
    DevEui: NotRequired[str]
    DeviceProfileId: NotRequired[str]
    ServiceProfileId: NotRequired[str]
    OtaaV1_1: NotRequired[OtaaV11TypeDef]
    OtaaV1_0_x: NotRequired[OtaaV10XTypeDef]
    AbpV1_1: NotRequired[AbpV11TypeDef]
    AbpV1_0_x: NotRequired[AbpV10XTypeDef]
    FPorts: NotRequired[FPortsUnionTypeDef]


class UpdateWirelessDeviceRequestRequestTypeDef(TypedDict):
    Id: str
    DestinationName: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    LoRaWAN: NotRequired[LoRaWANUpdateDeviceTypeDef]
    Positioning: NotRequired[PositioningConfigStatusType]


class DownlinkQueueMessageTypeDef(TypedDict):
    MessageId: NotRequired[str]
    TransmitMode: NotRequired[int]
    ReceivedAt: NotRequired[str]
    LoRaWAN: NotRequired[LoRaWANSendDataToDeviceOutputTypeDef]


class LoRaWANSendDataToDeviceTypeDef(TypedDict):
    FPort: NotRequired[int]
    ParticipatingGateways: NotRequired[ParticipatingGatewaysUnionTypeDef]


class CellTowersTypeDef(TypedDict):
    Gsm: NotRequired[Sequence[GsmObjTypeDef]]
    Wcdma: NotRequired[Sequence[WcdmaObjTypeDef]]
    Tdscdma: NotRequired[Sequence[TdscdmaObjTypeDef]]
    Lte: NotRequired[Sequence[LteObjTypeDef]]
    Cdma: NotRequired[Sequence[CdmaObjTypeDef]]


class EventConfigurationItemTypeDef(TypedDict):
    Identifier: NotRequired[str]
    IdentifierType: NotRequired[IdentifierTypeType]
    PartnerType: NotRequired[Literal["Sidewalk"]]
    Events: NotRequired[EventNotificationItemConfigurationsTypeDef]


class CreateWirelessGatewayTaskDefinitionRequestRequestTypeDef(TypedDict):
    AutoCreateTasks: bool
    Name: NotRequired[str]
    Update: NotRequired[UpdateWirelessGatewayTaskCreateTypeDef]
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class GetWirelessGatewayTaskDefinitionResponseTypeDef(TypedDict):
    AutoCreateTasks: bool
    Name: str
    Update: UpdateWirelessGatewayTaskCreateTypeDef
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListWirelessGatewayTaskDefinitionsResponseTypeDef(TypedDict):
    TaskDefinitions: List[UpdateWirelessGatewayTaskEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateMulticastGroupRequestRequestTypeDef(TypedDict):
    LoRaWAN: LoRaWANMulticastTypeDef
    Name: NotRequired[str]
    Description: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateMulticastGroupRequestRequestTypeDef(TypedDict):
    Id: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    LoRaWAN: NotRequired[LoRaWANMulticastTypeDef]


class ListPositionConfigurationsResponseTypeDef(TypedDict):
    PositionConfigurationList: List[PositionConfigurationItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateLogLevelsByResourceTypesRequestRequestTypeDef(TypedDict):
    DefaultLogLevel: NotRequired[LogLevelType]
    FuotaTaskLogOptions: NotRequired[Sequence[FuotaTaskLogOptionUnionTypeDef]]
    WirelessDeviceLogOptions: NotRequired[Sequence[WirelessDeviceLogOptionUnionTypeDef]]
    WirelessGatewayLogOptions: NotRequired[Sequence[WirelessGatewayLogOptionUnionTypeDef]]


CreateWirelessDeviceRequestRequestTypeDef = TypedDict(
    "CreateWirelessDeviceRequestRequestTypeDef",
    {
        "Type": WirelessDeviceTypeType,
        "DestinationName": str,
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "ClientRequestToken": NotRequired[str],
        "LoRaWAN": NotRequired[LoRaWANDeviceTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "Positioning": NotRequired[PositioningConfigStatusType],
        "Sidewalk": NotRequired[SidewalkCreateWirelessDeviceTypeDef],
    },
)


class ListQueuedMessagesResponseTypeDef(TypedDict):
    DownlinkQueueMessagesList: List[DownlinkQueueMessageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


LoRaWANSendDataToDeviceUnionTypeDef = Union[
    LoRaWANSendDataToDeviceTypeDef, LoRaWANSendDataToDeviceOutputTypeDef
]


class GetPositionEstimateRequestRequestTypeDef(TypedDict):
    WiFiAccessPoints: NotRequired[Sequence[WiFiAccessPointTypeDef]]
    CellTowers: NotRequired[CellTowersTypeDef]
    Ip: NotRequired[IpTypeDef]
    Gnss: NotRequired[GnssTypeDef]
    Timestamp: NotRequired[TimestampTypeDef]


class ListEventConfigurationsResponseTypeDef(TypedDict):
    EventConfigurationsList: List[EventConfigurationItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class WirelessMetadataTypeDef(TypedDict):
    LoRaWAN: NotRequired[LoRaWANSendDataToDeviceUnionTypeDef]
    Sidewalk: NotRequired[SidewalkSendDataToDeviceTypeDef]


class SendDataToWirelessDeviceRequestRequestTypeDef(TypedDict):
    Id: str
    TransmitMode: int
    PayloadData: str
    WirelessMetadata: NotRequired[WirelessMetadataTypeDef]
