"""
Type annotations for cognito-sync service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cognito_sync/type_defs/)

Usage::

    ```python
    from mypy_boto3_cognito_sync.type_defs import BulkPublishRequestRequestTypeDef

    data: BulkPublishRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import BulkPublishStatusType, OperationType, PlatformType, StreamingStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BulkPublishRequestRequestTypeDef",
    "BulkPublishResponseTypeDef",
    "CognitoStreamsTypeDef",
    "DatasetTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DeleteDatasetResponseTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeDatasetResponseTypeDef",
    "DescribeIdentityPoolUsageRequestRequestTypeDef",
    "DescribeIdentityPoolUsageResponseTypeDef",
    "DescribeIdentityUsageRequestRequestTypeDef",
    "DescribeIdentityUsageResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetBulkPublishDetailsRequestRequestTypeDef",
    "GetBulkPublishDetailsResponseTypeDef",
    "GetCognitoEventsRequestRequestTypeDef",
    "GetCognitoEventsResponseTypeDef",
    "GetIdentityPoolConfigurationRequestRequestTypeDef",
    "GetIdentityPoolConfigurationResponseTypeDef",
    "IdentityPoolUsageTypeDef",
    "IdentityUsageTypeDef",
    "ListDatasetsRequestRequestTypeDef",
    "ListDatasetsResponseTypeDef",
    "ListIdentityPoolUsageRequestRequestTypeDef",
    "ListIdentityPoolUsageResponseTypeDef",
    "ListRecordsRequestRequestTypeDef",
    "ListRecordsResponseTypeDef",
    "PushSyncOutputTypeDef",
    "PushSyncTypeDef",
    "RecordPatchTypeDef",
    "RecordTypeDef",
    "RegisterDeviceRequestRequestTypeDef",
    "RegisterDeviceResponseTypeDef",
    "ResponseMetadataTypeDef",
    "SetCognitoEventsRequestRequestTypeDef",
    "SetIdentityPoolConfigurationRequestRequestTypeDef",
    "SetIdentityPoolConfigurationResponseTypeDef",
    "SubscribeToDatasetRequestRequestTypeDef",
    "TimestampTypeDef",
    "UnsubscribeFromDatasetRequestRequestTypeDef",
    "UpdateRecordsRequestRequestTypeDef",
    "UpdateRecordsResponseTypeDef",
)

class BulkPublishRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CognitoStreamsTypeDef(TypedDict):
    StreamName: NotRequired[str]
    RoleArn: NotRequired[str]
    StreamingStatus: NotRequired[StreamingStatusType]

class DatasetTypeDef(TypedDict):
    IdentityId: NotRequired[str]
    DatasetName: NotRequired[str]
    CreationDate: NotRequired[datetime]
    LastModifiedDate: NotRequired[datetime]
    LastModifiedBy: NotRequired[str]
    DataStorage: NotRequired[int]
    NumRecords: NotRequired[int]

class DeleteDatasetRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityId: str
    DatasetName: str

class DescribeDatasetRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityId: str
    DatasetName: str

class DescribeIdentityPoolUsageRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str

class IdentityPoolUsageTypeDef(TypedDict):
    IdentityPoolId: NotRequired[str]
    SyncSessionsCount: NotRequired[int]
    DataStorage: NotRequired[int]
    LastModifiedDate: NotRequired[datetime]

class DescribeIdentityUsageRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityId: str

class IdentityUsageTypeDef(TypedDict):
    IdentityId: NotRequired[str]
    IdentityPoolId: NotRequired[str]
    LastModifiedDate: NotRequired[datetime]
    DatasetCount: NotRequired[int]
    DataStorage: NotRequired[int]

class GetBulkPublishDetailsRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str

class GetCognitoEventsRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str

class GetIdentityPoolConfigurationRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str

class PushSyncOutputTypeDef(TypedDict):
    ApplicationArns: NotRequired[List[str]]
    RoleArn: NotRequired[str]

class ListDatasetsRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListIdentityPoolUsageRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListRecordsRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityId: str
    DatasetName: str
    LastSyncCount: NotRequired[int]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SyncSessionToken: NotRequired[str]

class RecordTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]
    SyncCount: NotRequired[int]
    LastModifiedDate: NotRequired[datetime]
    LastModifiedBy: NotRequired[str]
    DeviceLastModifiedDate: NotRequired[datetime]

class PushSyncTypeDef(TypedDict):
    ApplicationArns: NotRequired[Sequence[str]]
    RoleArn: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class RegisterDeviceRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityId: str
    Platform: PlatformType
    Token: str

class SetCognitoEventsRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str
    Events: Mapping[str, str]

class SubscribeToDatasetRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityId: str
    DatasetName: str
    DeviceId: str

class UnsubscribeFromDatasetRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityId: str
    DatasetName: str
    DeviceId: str

class BulkPublishResponseTypeDef(TypedDict):
    IdentityPoolId: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetBulkPublishDetailsResponseTypeDef(TypedDict):
    IdentityPoolId: str
    BulkPublishStartTime: datetime
    BulkPublishCompleteTime: datetime
    BulkPublishStatus: BulkPublishStatusType
    FailureMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetCognitoEventsResponseTypeDef(TypedDict):
    Events: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterDeviceResponseTypeDef(TypedDict):
    DeviceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDatasetResponseTypeDef(TypedDict):
    Dataset: DatasetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeDatasetResponseTypeDef(TypedDict):
    Dataset: DatasetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDatasetsResponseTypeDef(TypedDict):
    Datasets: List[DatasetTypeDef]
    Count: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeIdentityPoolUsageResponseTypeDef(TypedDict):
    IdentityPoolUsage: IdentityPoolUsageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListIdentityPoolUsageResponseTypeDef(TypedDict):
    IdentityPoolUsages: List[IdentityPoolUsageTypeDef]
    MaxResults: int
    Count: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeIdentityUsageResponseTypeDef(TypedDict):
    IdentityUsage: IdentityUsageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetIdentityPoolConfigurationResponseTypeDef(TypedDict):
    IdentityPoolId: str
    PushSync: PushSyncOutputTypeDef
    CognitoStreams: CognitoStreamsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SetIdentityPoolConfigurationResponseTypeDef(TypedDict):
    IdentityPoolId: str
    PushSync: PushSyncOutputTypeDef
    CognitoStreams: CognitoStreamsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListRecordsResponseTypeDef(TypedDict):
    Records: List[RecordTypeDef]
    Count: int
    DatasetSyncCount: int
    LastModifiedBy: str
    MergedDatasetNames: List[str]
    DatasetExists: bool
    DatasetDeletedAfterRequestedSyncCount: bool
    SyncSessionToken: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateRecordsResponseTypeDef(TypedDict):
    Records: List[RecordTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SetIdentityPoolConfigurationRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str
    PushSync: NotRequired[PushSyncTypeDef]
    CognitoStreams: NotRequired[CognitoStreamsTypeDef]

class RecordPatchTypeDef(TypedDict):
    Op: OperationType
    Key: str
    SyncCount: int
    Value: NotRequired[str]
    DeviceLastModifiedDate: NotRequired[TimestampTypeDef]

class UpdateRecordsRequestRequestTypeDef(TypedDict):
    IdentityPoolId: str
    IdentityId: str
    DatasetName: str
    SyncSessionToken: str
    DeviceId: NotRequired[str]
    RecordPatches: NotRequired[Sequence[RecordPatchTypeDef]]
    ClientContext: NotRequired[str]
