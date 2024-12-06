"""
Type annotations for chime-sdk-identity service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_identity/type_defs/)

Usage::

    ```python
    from mypy_boto3_chime_sdk_identity.type_defs import IdentityTypeDef

    data: IdentityTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AllowMessagesType,
    AppInstanceUserEndpointTypeType,
    EndpointStatusReasonType,
    EndpointStatusType,
    StandardMessagesType,
    TargetedMessagesType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AppInstanceAdminSummaryTypeDef",
    "AppInstanceAdminTypeDef",
    "AppInstanceBotSummaryTypeDef",
    "AppInstanceBotTypeDef",
    "AppInstanceRetentionSettingsTypeDef",
    "AppInstanceSummaryTypeDef",
    "AppInstanceTypeDef",
    "AppInstanceUserEndpointSummaryTypeDef",
    "AppInstanceUserEndpointTypeDef",
    "AppInstanceUserSummaryTypeDef",
    "AppInstanceUserTypeDef",
    "ChannelRetentionSettingsTypeDef",
    "ConfigurationTypeDef",
    "CreateAppInstanceAdminRequestRequestTypeDef",
    "CreateAppInstanceAdminResponseTypeDef",
    "CreateAppInstanceBotRequestRequestTypeDef",
    "CreateAppInstanceBotResponseTypeDef",
    "CreateAppInstanceRequestRequestTypeDef",
    "CreateAppInstanceResponseTypeDef",
    "CreateAppInstanceUserRequestRequestTypeDef",
    "CreateAppInstanceUserResponseTypeDef",
    "DeleteAppInstanceAdminRequestRequestTypeDef",
    "DeleteAppInstanceBotRequestRequestTypeDef",
    "DeleteAppInstanceRequestRequestTypeDef",
    "DeleteAppInstanceUserRequestRequestTypeDef",
    "DeregisterAppInstanceUserEndpointRequestRequestTypeDef",
    "DescribeAppInstanceAdminRequestRequestTypeDef",
    "DescribeAppInstanceAdminResponseTypeDef",
    "DescribeAppInstanceBotRequestRequestTypeDef",
    "DescribeAppInstanceBotResponseTypeDef",
    "DescribeAppInstanceRequestRequestTypeDef",
    "DescribeAppInstanceResponseTypeDef",
    "DescribeAppInstanceUserEndpointRequestRequestTypeDef",
    "DescribeAppInstanceUserEndpointResponseTypeDef",
    "DescribeAppInstanceUserRequestRequestTypeDef",
    "DescribeAppInstanceUserResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointAttributesTypeDef",
    "EndpointStateTypeDef",
    "ExpirationSettingsTypeDef",
    "GetAppInstanceRetentionSettingsRequestRequestTypeDef",
    "GetAppInstanceRetentionSettingsResponseTypeDef",
    "IdentityTypeDef",
    "InvokedByTypeDef",
    "LexConfigurationTypeDef",
    "ListAppInstanceAdminsRequestRequestTypeDef",
    "ListAppInstanceAdminsResponseTypeDef",
    "ListAppInstanceBotsRequestRequestTypeDef",
    "ListAppInstanceBotsResponseTypeDef",
    "ListAppInstanceUserEndpointsRequestRequestTypeDef",
    "ListAppInstanceUserEndpointsResponseTypeDef",
    "ListAppInstanceUsersRequestRequestTypeDef",
    "ListAppInstanceUsersResponseTypeDef",
    "ListAppInstancesRequestRequestTypeDef",
    "ListAppInstancesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutAppInstanceRetentionSettingsRequestRequestTypeDef",
    "PutAppInstanceRetentionSettingsResponseTypeDef",
    "PutAppInstanceUserExpirationSettingsRequestRequestTypeDef",
    "PutAppInstanceUserExpirationSettingsResponseTypeDef",
    "RegisterAppInstanceUserEndpointRequestRequestTypeDef",
    "RegisterAppInstanceUserEndpointResponseTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAppInstanceBotRequestRequestTypeDef",
    "UpdateAppInstanceBotResponseTypeDef",
    "UpdateAppInstanceRequestRequestTypeDef",
    "UpdateAppInstanceResponseTypeDef",
    "UpdateAppInstanceUserEndpointRequestRequestTypeDef",
    "UpdateAppInstanceUserEndpointResponseTypeDef",
    "UpdateAppInstanceUserRequestRequestTypeDef",
    "UpdateAppInstanceUserResponseTypeDef",
)

class IdentityTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]

class AppInstanceBotSummaryTypeDef(TypedDict):
    AppInstanceBotArn: NotRequired[str]
    Name: NotRequired[str]
    Metadata: NotRequired[str]

class ChannelRetentionSettingsTypeDef(TypedDict):
    RetentionDays: NotRequired[int]

class AppInstanceSummaryTypeDef(TypedDict):
    AppInstanceArn: NotRequired[str]
    Name: NotRequired[str]
    Metadata: NotRequired[str]

class AppInstanceTypeDef(TypedDict):
    AppInstanceArn: NotRequired[str]
    Name: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    LastUpdatedTimestamp: NotRequired[datetime]
    Metadata: NotRequired[str]

class EndpointStateTypeDef(TypedDict):
    Status: EndpointStatusType
    StatusReason: NotRequired[EndpointStatusReasonType]

class EndpointAttributesTypeDef(TypedDict):
    DeviceToken: str
    VoipDeviceToken: NotRequired[str]

class AppInstanceUserSummaryTypeDef(TypedDict):
    AppInstanceUserArn: NotRequired[str]
    Name: NotRequired[str]
    Metadata: NotRequired[str]

class ExpirationSettingsTypeDef(TypedDict):
    ExpirationDays: int
    ExpirationCriterion: Literal["CREATED_TIMESTAMP"]

class CreateAppInstanceAdminRequestRequestTypeDef(TypedDict):
    AppInstanceAdminArn: str
    AppInstanceArn: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class DeleteAppInstanceAdminRequestRequestTypeDef(TypedDict):
    AppInstanceAdminArn: str
    AppInstanceArn: str

class DeleteAppInstanceBotRequestRequestTypeDef(TypedDict):
    AppInstanceBotArn: str

class DeleteAppInstanceRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str

class DeleteAppInstanceUserRequestRequestTypeDef(TypedDict):
    AppInstanceUserArn: str

class DeregisterAppInstanceUserEndpointRequestRequestTypeDef(TypedDict):
    AppInstanceUserArn: str
    EndpointId: str

class DescribeAppInstanceAdminRequestRequestTypeDef(TypedDict):
    AppInstanceAdminArn: str
    AppInstanceArn: str

class DescribeAppInstanceBotRequestRequestTypeDef(TypedDict):
    AppInstanceBotArn: str

class DescribeAppInstanceRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str

class DescribeAppInstanceUserEndpointRequestRequestTypeDef(TypedDict):
    AppInstanceUserArn: str
    EndpointId: str

class DescribeAppInstanceUserRequestRequestTypeDef(TypedDict):
    AppInstanceUserArn: str

class GetAppInstanceRetentionSettingsRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str

class InvokedByTypeDef(TypedDict):
    StandardMessages: StandardMessagesType
    TargetedMessages: TargetedMessagesType

class ListAppInstanceAdminsRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAppInstanceBotsRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAppInstanceUserEndpointsRequestRequestTypeDef(TypedDict):
    AppInstanceUserArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAppInstanceUsersRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAppInstancesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]

class UpdateAppInstanceRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    Name: str
    Metadata: str

class UpdateAppInstanceUserEndpointRequestRequestTypeDef(TypedDict):
    AppInstanceUserArn: str
    EndpointId: str
    Name: NotRequired[str]
    AllowMessages: NotRequired[AllowMessagesType]

class UpdateAppInstanceUserRequestRequestTypeDef(TypedDict):
    AppInstanceUserArn: str
    Name: str
    Metadata: str

class AppInstanceAdminSummaryTypeDef(TypedDict):
    Admin: NotRequired[IdentityTypeDef]

class AppInstanceAdminTypeDef(TypedDict):
    Admin: NotRequired[IdentityTypeDef]
    AppInstanceArn: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]

class AppInstanceRetentionSettingsTypeDef(TypedDict):
    ChannelRetentionSettings: NotRequired[ChannelRetentionSettingsTypeDef]

AppInstanceUserEndpointSummaryTypeDef = TypedDict(
    "AppInstanceUserEndpointSummaryTypeDef",
    {
        "AppInstanceUserArn": NotRequired[str],
        "EndpointId": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[AppInstanceUserEndpointTypeType],
        "AllowMessages": NotRequired[AllowMessagesType],
        "EndpointState": NotRequired[EndpointStateTypeDef],
    },
)
AppInstanceUserEndpointTypeDef = TypedDict(
    "AppInstanceUserEndpointTypeDef",
    {
        "AppInstanceUserArn": NotRequired[str],
        "EndpointId": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[AppInstanceUserEndpointTypeType],
        "ResourceArn": NotRequired[str],
        "EndpointAttributes": NotRequired[EndpointAttributesTypeDef],
        "CreatedTimestamp": NotRequired[datetime],
        "LastUpdatedTimestamp": NotRequired[datetime],
        "AllowMessages": NotRequired[AllowMessagesType],
        "EndpointState": NotRequired[EndpointStateTypeDef],
    },
)
RegisterAppInstanceUserEndpointRequestRequestTypeDef = TypedDict(
    "RegisterAppInstanceUserEndpointRequestRequestTypeDef",
    {
        "AppInstanceUserArn": str,
        "Type": AppInstanceUserEndpointTypeType,
        "ResourceArn": str,
        "EndpointAttributes": EndpointAttributesTypeDef,
        "ClientRequestToken": str,
        "Name": NotRequired[str],
        "AllowMessages": NotRequired[AllowMessagesType],
    },
)

class AppInstanceUserTypeDef(TypedDict):
    AppInstanceUserArn: NotRequired[str]
    Name: NotRequired[str]
    Metadata: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    LastUpdatedTimestamp: NotRequired[datetime]
    ExpirationSettings: NotRequired[ExpirationSettingsTypeDef]

class PutAppInstanceUserExpirationSettingsRequestRequestTypeDef(TypedDict):
    AppInstanceUserArn: str
    ExpirationSettings: NotRequired[ExpirationSettingsTypeDef]

class CreateAppInstanceAdminResponseTypeDef(TypedDict):
    AppInstanceAdmin: IdentityTypeDef
    AppInstanceArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAppInstanceBotResponseTypeDef(TypedDict):
    AppInstanceBotArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAppInstanceResponseTypeDef(TypedDict):
    AppInstanceArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAppInstanceUserResponseTypeDef(TypedDict):
    AppInstanceUserArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAppInstanceResponseTypeDef(TypedDict):
    AppInstance: AppInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListAppInstanceBotsResponseTypeDef(TypedDict):
    AppInstanceArn: str
    AppInstanceBots: List[AppInstanceBotSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAppInstanceUsersResponseTypeDef(TypedDict):
    AppInstanceArn: str
    AppInstanceUsers: List[AppInstanceUserSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAppInstancesResponseTypeDef(TypedDict):
    AppInstances: List[AppInstanceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PutAppInstanceUserExpirationSettingsResponseTypeDef(TypedDict):
    AppInstanceUserArn: str
    ExpirationSettings: ExpirationSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterAppInstanceUserEndpointResponseTypeDef(TypedDict):
    AppInstanceUserArn: str
    EndpointId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAppInstanceBotResponseTypeDef(TypedDict):
    AppInstanceBotArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAppInstanceResponseTypeDef(TypedDict):
    AppInstanceArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAppInstanceUserEndpointResponseTypeDef(TypedDict):
    AppInstanceUserArn: str
    EndpointId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAppInstanceUserResponseTypeDef(TypedDict):
    AppInstanceUserArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAppInstanceRequestRequestTypeDef(TypedDict):
    Name: str
    ClientRequestToken: str
    Metadata: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateAppInstanceUserRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    AppInstanceUserId: str
    Name: str
    ClientRequestToken: str
    Metadata: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ExpirationSettings: NotRequired[ExpirationSettingsTypeDef]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]

class LexConfigurationTypeDef(TypedDict):
    LexBotAliasArn: str
    LocaleId: str
    RespondsTo: NotRequired[Literal["STANDARD_MESSAGES"]]
    InvokedBy: NotRequired[InvokedByTypeDef]
    WelcomeIntent: NotRequired[str]

class ListAppInstanceAdminsResponseTypeDef(TypedDict):
    AppInstanceArn: str
    AppInstanceAdmins: List[AppInstanceAdminSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeAppInstanceAdminResponseTypeDef(TypedDict):
    AppInstanceAdmin: AppInstanceAdminTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAppInstanceRetentionSettingsResponseTypeDef(TypedDict):
    AppInstanceRetentionSettings: AppInstanceRetentionSettingsTypeDef
    InitiateDeletionTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class PutAppInstanceRetentionSettingsRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    AppInstanceRetentionSettings: AppInstanceRetentionSettingsTypeDef

class PutAppInstanceRetentionSettingsResponseTypeDef(TypedDict):
    AppInstanceRetentionSettings: AppInstanceRetentionSettingsTypeDef
    InitiateDeletionTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListAppInstanceUserEndpointsResponseTypeDef(TypedDict):
    AppInstanceUserEndpoints: List[AppInstanceUserEndpointSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeAppInstanceUserEndpointResponseTypeDef(TypedDict):
    AppInstanceUserEndpoint: AppInstanceUserEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAppInstanceUserResponseTypeDef(TypedDict):
    AppInstanceUser: AppInstanceUserTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ConfigurationTypeDef(TypedDict):
    Lex: LexConfigurationTypeDef

class AppInstanceBotTypeDef(TypedDict):
    AppInstanceBotArn: NotRequired[str]
    Name: NotRequired[str]
    Configuration: NotRequired[ConfigurationTypeDef]
    CreatedTimestamp: NotRequired[datetime]
    LastUpdatedTimestamp: NotRequired[datetime]
    Metadata: NotRequired[str]

class CreateAppInstanceBotRequestRequestTypeDef(TypedDict):
    AppInstanceArn: str
    ClientRequestToken: str
    Configuration: ConfigurationTypeDef
    Name: NotRequired[str]
    Metadata: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class UpdateAppInstanceBotRequestRequestTypeDef(TypedDict):
    AppInstanceBotArn: str
    Name: str
    Metadata: str
    Configuration: NotRequired[ConfigurationTypeDef]

class DescribeAppInstanceBotResponseTypeDef(TypedDict):
    AppInstanceBot: AppInstanceBotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
