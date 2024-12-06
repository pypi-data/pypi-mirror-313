"""
Type annotations for support-app service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_support_app/type_defs/)

Usage::

    ```python
    from mypy_boto3_support_app.type_defs import CreateSlackChannelConfigurationRequestRequestTypeDef

    data: CreateSlackChannelConfigurationRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List

from .literals import AccountTypeType, NotificationSeverityLevelType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "CreateSlackChannelConfigurationRequestRequestTypeDef",
    "DeleteSlackChannelConfigurationRequestRequestTypeDef",
    "DeleteSlackWorkspaceConfigurationRequestRequestTypeDef",
    "GetAccountAliasResultTypeDef",
    "ListSlackChannelConfigurationsRequestRequestTypeDef",
    "ListSlackChannelConfigurationsResultTypeDef",
    "ListSlackWorkspaceConfigurationsRequestRequestTypeDef",
    "ListSlackWorkspaceConfigurationsResultTypeDef",
    "PutAccountAliasRequestRequestTypeDef",
    "RegisterSlackWorkspaceForOrganizationRequestRequestTypeDef",
    "RegisterSlackWorkspaceForOrganizationResultTypeDef",
    "ResponseMetadataTypeDef",
    "SlackChannelConfigurationTypeDef",
    "SlackWorkspaceConfigurationTypeDef",
    "UpdateSlackChannelConfigurationRequestRequestTypeDef",
    "UpdateSlackChannelConfigurationResultTypeDef",
)


class CreateSlackChannelConfigurationRequestRequestTypeDef(TypedDict):
    channelId: str
    channelRoleArn: str
    notifyOnCaseSeverity: NotificationSeverityLevelType
    teamId: str
    channelName: NotRequired[str]
    notifyOnAddCorrespondenceToCase: NotRequired[bool]
    notifyOnCreateOrReopenCase: NotRequired[bool]
    notifyOnResolveCase: NotRequired[bool]


class DeleteSlackChannelConfigurationRequestRequestTypeDef(TypedDict):
    channelId: str
    teamId: str


class DeleteSlackWorkspaceConfigurationRequestRequestTypeDef(TypedDict):
    teamId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ListSlackChannelConfigurationsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]


class SlackChannelConfigurationTypeDef(TypedDict):
    channelId: str
    teamId: str
    channelName: NotRequired[str]
    channelRoleArn: NotRequired[str]
    notifyOnAddCorrespondenceToCase: NotRequired[bool]
    notifyOnCaseSeverity: NotRequired[NotificationSeverityLevelType]
    notifyOnCreateOrReopenCase: NotRequired[bool]
    notifyOnResolveCase: NotRequired[bool]


class ListSlackWorkspaceConfigurationsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]


class SlackWorkspaceConfigurationTypeDef(TypedDict):
    teamId: str
    allowOrganizationMemberAccount: NotRequired[bool]
    teamName: NotRequired[str]


class PutAccountAliasRequestRequestTypeDef(TypedDict):
    accountAlias: str


class RegisterSlackWorkspaceForOrganizationRequestRequestTypeDef(TypedDict):
    teamId: str


class UpdateSlackChannelConfigurationRequestRequestTypeDef(TypedDict):
    channelId: str
    teamId: str
    channelName: NotRequired[str]
    channelRoleArn: NotRequired[str]
    notifyOnAddCorrespondenceToCase: NotRequired[bool]
    notifyOnCaseSeverity: NotRequired[NotificationSeverityLevelType]
    notifyOnCreateOrReopenCase: NotRequired[bool]
    notifyOnResolveCase: NotRequired[bool]


class GetAccountAliasResultTypeDef(TypedDict):
    accountAlias: str
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterSlackWorkspaceForOrganizationResultTypeDef(TypedDict):
    accountType: AccountTypeType
    teamId: str
    teamName: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSlackChannelConfigurationResultTypeDef(TypedDict):
    channelId: str
    channelName: str
    channelRoleArn: str
    notifyOnAddCorrespondenceToCase: bool
    notifyOnCaseSeverity: NotificationSeverityLevelType
    notifyOnCreateOrReopenCase: bool
    notifyOnResolveCase: bool
    teamId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListSlackChannelConfigurationsResultTypeDef(TypedDict):
    slackChannelConfigurations: List[SlackChannelConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSlackWorkspaceConfigurationsResultTypeDef(TypedDict):
    slackWorkspaceConfigurations: List[SlackWorkspaceConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
