"""
Type annotations for securitylake service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/type_defs/)

Usage::

    ```python
    from mypy_boto3_securitylake.type_defs import AwsIdentityTypeDef

    data: AwsIdentityTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AccessTypeType,
    AwsLogSourceNameType,
    DataLakeStatusType,
    HttpMethodType,
    SourceCollectionStatusType,
    SubscriberStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AwsIdentityTypeDef",
    "AwsLogSourceConfigurationTypeDef",
    "AwsLogSourceResourceTypeDef",
    "CreateAwsLogSourceRequestRequestTypeDef",
    "CreateAwsLogSourceResponseTypeDef",
    "CreateCustomLogSourceRequestRequestTypeDef",
    "CreateCustomLogSourceResponseTypeDef",
    "CreateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    "CreateDataLakeOrganizationConfigurationRequestRequestTypeDef",
    "CreateDataLakeRequestRequestTypeDef",
    "CreateDataLakeResponseTypeDef",
    "CreateSubscriberNotificationRequestRequestTypeDef",
    "CreateSubscriberNotificationResponseTypeDef",
    "CreateSubscriberRequestRequestTypeDef",
    "CreateSubscriberResponseTypeDef",
    "CustomLogSourceAttributesTypeDef",
    "CustomLogSourceConfigurationTypeDef",
    "CustomLogSourceCrawlerConfigurationTypeDef",
    "CustomLogSourceProviderTypeDef",
    "CustomLogSourceResourceTypeDef",
    "DataLakeAutoEnableNewAccountConfigurationOutputTypeDef",
    "DataLakeAutoEnableNewAccountConfigurationTypeDef",
    "DataLakeAutoEnableNewAccountConfigurationUnionTypeDef",
    "DataLakeConfigurationTypeDef",
    "DataLakeEncryptionConfigurationTypeDef",
    "DataLakeExceptionTypeDef",
    "DataLakeLifecycleConfigurationOutputTypeDef",
    "DataLakeLifecycleConfigurationTypeDef",
    "DataLakeLifecycleConfigurationUnionTypeDef",
    "DataLakeLifecycleExpirationTypeDef",
    "DataLakeLifecycleTransitionTypeDef",
    "DataLakeReplicationConfigurationOutputTypeDef",
    "DataLakeReplicationConfigurationTypeDef",
    "DataLakeReplicationConfigurationUnionTypeDef",
    "DataLakeResourceTypeDef",
    "DataLakeSourceStatusTypeDef",
    "DataLakeSourceTypeDef",
    "DataLakeUpdateExceptionTypeDef",
    "DataLakeUpdateStatusTypeDef",
    "DeleteAwsLogSourceRequestRequestTypeDef",
    "DeleteAwsLogSourceResponseTypeDef",
    "DeleteCustomLogSourceRequestRequestTypeDef",
    "DeleteDataLakeOrganizationConfigurationRequestRequestTypeDef",
    "DeleteDataLakeRequestRequestTypeDef",
    "DeleteSubscriberNotificationRequestRequestTypeDef",
    "DeleteSubscriberRequestRequestTypeDef",
    "GetDataLakeExceptionSubscriptionResponseTypeDef",
    "GetDataLakeOrganizationConfigurationResponseTypeDef",
    "GetDataLakeSourcesRequestGetDataLakeSourcesPaginateTypeDef",
    "GetDataLakeSourcesRequestRequestTypeDef",
    "GetDataLakeSourcesResponseTypeDef",
    "GetSubscriberRequestRequestTypeDef",
    "GetSubscriberResponseTypeDef",
    "HttpsNotificationConfigurationTypeDef",
    "ListDataLakeExceptionsRequestListDataLakeExceptionsPaginateTypeDef",
    "ListDataLakeExceptionsRequestRequestTypeDef",
    "ListDataLakeExceptionsResponseTypeDef",
    "ListDataLakesRequestRequestTypeDef",
    "ListDataLakesResponseTypeDef",
    "ListLogSourcesRequestListLogSourcesPaginateTypeDef",
    "ListLogSourcesRequestRequestTypeDef",
    "ListLogSourcesResponseTypeDef",
    "ListSubscribersRequestListSubscribersPaginateTypeDef",
    "ListSubscribersRequestRequestTypeDef",
    "ListSubscribersResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LogSourceResourceTypeDef",
    "LogSourceTypeDef",
    "NotificationConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "RegisterDataLakeDelegatedAdministratorRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "SubscriberResourceTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    "UpdateDataLakeRequestRequestTypeDef",
    "UpdateDataLakeResponseTypeDef",
    "UpdateSubscriberNotificationRequestRequestTypeDef",
    "UpdateSubscriberNotificationResponseTypeDef",
    "UpdateSubscriberRequestRequestTypeDef",
    "UpdateSubscriberResponseTypeDef",
)

class AwsIdentityTypeDef(TypedDict):
    externalId: str
    principal: str

class AwsLogSourceConfigurationTypeDef(TypedDict):
    regions: Sequence[str]
    sourceName: AwsLogSourceNameType
    accounts: NotRequired[Sequence[str]]
    sourceVersion: NotRequired[str]

class AwsLogSourceResourceTypeDef(TypedDict):
    sourceName: NotRequired[AwsLogSourceNameType]
    sourceVersion: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateDataLakeExceptionSubscriptionRequestRequestTypeDef(TypedDict):
    notificationEndpoint: str
    subscriptionProtocol: str
    exceptionTimeToLive: NotRequired[int]

class TagTypeDef(TypedDict):
    key: str
    value: str

class CustomLogSourceAttributesTypeDef(TypedDict):
    crawlerArn: NotRequired[str]
    databaseArn: NotRequired[str]
    tableArn: NotRequired[str]

class CustomLogSourceCrawlerConfigurationTypeDef(TypedDict):
    roleArn: str

class CustomLogSourceProviderTypeDef(TypedDict):
    location: NotRequired[str]
    roleArn: NotRequired[str]

class DataLakeEncryptionConfigurationTypeDef(TypedDict):
    kmsKeyId: NotRequired[str]

class DataLakeExceptionTypeDef(TypedDict):
    exception: NotRequired[str]
    region: NotRequired[str]
    remediation: NotRequired[str]
    timestamp: NotRequired[datetime]

class DataLakeLifecycleExpirationTypeDef(TypedDict):
    days: NotRequired[int]

class DataLakeLifecycleTransitionTypeDef(TypedDict):
    days: NotRequired[int]
    storageClass: NotRequired[str]

class DataLakeReplicationConfigurationOutputTypeDef(TypedDict):
    regions: NotRequired[List[str]]
    roleArn: NotRequired[str]

class DataLakeReplicationConfigurationTypeDef(TypedDict):
    regions: NotRequired[Sequence[str]]
    roleArn: NotRequired[str]

class DataLakeSourceStatusTypeDef(TypedDict):
    resource: NotRequired[str]
    status: NotRequired[SourceCollectionStatusType]

class DataLakeUpdateExceptionTypeDef(TypedDict):
    code: NotRequired[str]
    reason: NotRequired[str]

class DeleteCustomLogSourceRequestRequestTypeDef(TypedDict):
    sourceName: str
    sourceVersion: NotRequired[str]

class DeleteDataLakeRequestRequestTypeDef(TypedDict):
    regions: Sequence[str]

class DeleteSubscriberNotificationRequestRequestTypeDef(TypedDict):
    subscriberId: str

class DeleteSubscriberRequestRequestTypeDef(TypedDict):
    subscriberId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetDataLakeSourcesRequestRequestTypeDef(TypedDict):
    accounts: NotRequired[Sequence[str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class GetSubscriberRequestRequestTypeDef(TypedDict):
    subscriberId: str

class HttpsNotificationConfigurationTypeDef(TypedDict):
    endpoint: str
    targetRoleArn: str
    authorizationApiKeyName: NotRequired[str]
    authorizationApiKeyValue: NotRequired[str]
    httpMethod: NotRequired[HttpMethodType]

class ListDataLakeExceptionsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    regions: NotRequired[Sequence[str]]

class ListDataLakesRequestRequestTypeDef(TypedDict):
    regions: NotRequired[Sequence[str]]

class ListSubscribersRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class RegisterDataLakeDelegatedAdministratorRequestRequestTypeDef(TypedDict):
    accountId: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateDataLakeExceptionSubscriptionRequestRequestTypeDef(TypedDict):
    notificationEndpoint: str
    subscriptionProtocol: str
    exceptionTimeToLive: NotRequired[int]

class CreateAwsLogSourceRequestRequestTypeDef(TypedDict):
    sources: Sequence[AwsLogSourceConfigurationTypeDef]

class DeleteAwsLogSourceRequestRequestTypeDef(TypedDict):
    sources: Sequence[AwsLogSourceConfigurationTypeDef]

class DataLakeAutoEnableNewAccountConfigurationOutputTypeDef(TypedDict):
    region: str
    sources: List[AwsLogSourceResourceTypeDef]

class DataLakeAutoEnableNewAccountConfigurationTypeDef(TypedDict):
    region: str
    sources: Sequence[AwsLogSourceResourceTypeDef]

class CreateAwsLogSourceResponseTypeDef(TypedDict):
    failed: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSubscriberNotificationResponseTypeDef(TypedDict):
    subscriberEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAwsLogSourceResponseTypeDef(TypedDict):
    failed: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetDataLakeExceptionSubscriptionResponseTypeDef(TypedDict):
    exceptionTimeToLive: int
    notificationEndpoint: str
    subscriptionProtocol: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSubscriberNotificationResponseTypeDef(TypedDict):
    subscriberEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]

class CustomLogSourceConfigurationTypeDef(TypedDict):
    crawlerConfiguration: CustomLogSourceCrawlerConfigurationTypeDef
    providerIdentity: AwsIdentityTypeDef

class CustomLogSourceResourceTypeDef(TypedDict):
    attributes: NotRequired[CustomLogSourceAttributesTypeDef]
    provider: NotRequired[CustomLogSourceProviderTypeDef]
    sourceName: NotRequired[str]
    sourceVersion: NotRequired[str]

class ListDataLakeExceptionsResponseTypeDef(TypedDict):
    exceptions: List[DataLakeExceptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DataLakeLifecycleConfigurationOutputTypeDef(TypedDict):
    expiration: NotRequired[DataLakeLifecycleExpirationTypeDef]
    transitions: NotRequired[List[DataLakeLifecycleTransitionTypeDef]]

class DataLakeLifecycleConfigurationTypeDef(TypedDict):
    expiration: NotRequired[DataLakeLifecycleExpirationTypeDef]
    transitions: NotRequired[Sequence[DataLakeLifecycleTransitionTypeDef]]

DataLakeReplicationConfigurationUnionTypeDef = Union[
    DataLakeReplicationConfigurationTypeDef, DataLakeReplicationConfigurationOutputTypeDef
]

class DataLakeSourceTypeDef(TypedDict):
    account: NotRequired[str]
    eventClasses: NotRequired[List[str]]
    sourceName: NotRequired[str]
    sourceStatuses: NotRequired[List[DataLakeSourceStatusTypeDef]]

class DataLakeUpdateStatusTypeDef(TypedDict):
    exception: NotRequired[DataLakeUpdateExceptionTypeDef]
    requestId: NotRequired[str]
    status: NotRequired[DataLakeStatusType]

class GetDataLakeSourcesRequestGetDataLakeSourcesPaginateTypeDef(TypedDict):
    accounts: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataLakeExceptionsRequestListDataLakeExceptionsPaginateTypeDef(TypedDict):
    regions: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscribersRequestListSubscribersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class NotificationConfigurationTypeDef(TypedDict):
    httpsNotificationConfiguration: NotRequired[HttpsNotificationConfigurationTypeDef]
    sqsNotificationConfiguration: NotRequired[Mapping[str, Any]]

class GetDataLakeOrganizationConfigurationResponseTypeDef(TypedDict):
    autoEnableNewAccount: List[DataLakeAutoEnableNewAccountConfigurationOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

DataLakeAutoEnableNewAccountConfigurationUnionTypeDef = Union[
    DataLakeAutoEnableNewAccountConfigurationTypeDef,
    DataLakeAutoEnableNewAccountConfigurationOutputTypeDef,
]

class DeleteDataLakeOrganizationConfigurationRequestRequestTypeDef(TypedDict):
    autoEnableNewAccount: NotRequired[Sequence[DataLakeAutoEnableNewAccountConfigurationTypeDef]]

class CreateCustomLogSourceRequestRequestTypeDef(TypedDict):
    configuration: CustomLogSourceConfigurationTypeDef
    sourceName: str
    eventClasses: NotRequired[Sequence[str]]
    sourceVersion: NotRequired[str]

class CreateCustomLogSourceResponseTypeDef(TypedDict):
    source: CustomLogSourceResourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class LogSourceResourceTypeDef(TypedDict):
    awsLogSource: NotRequired[AwsLogSourceResourceTypeDef]
    customLogSource: NotRequired[CustomLogSourceResourceTypeDef]

DataLakeLifecycleConfigurationUnionTypeDef = Union[
    DataLakeLifecycleConfigurationTypeDef, DataLakeLifecycleConfigurationOutputTypeDef
]

class GetDataLakeSourcesResponseTypeDef(TypedDict):
    dataLakeArn: str
    dataLakeSources: List[DataLakeSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DataLakeResourceTypeDef(TypedDict):
    dataLakeArn: str
    region: str
    createStatus: NotRequired[DataLakeStatusType]
    encryptionConfiguration: NotRequired[DataLakeEncryptionConfigurationTypeDef]
    lifecycleConfiguration: NotRequired[DataLakeLifecycleConfigurationOutputTypeDef]
    replicationConfiguration: NotRequired[DataLakeReplicationConfigurationOutputTypeDef]
    s3BucketArn: NotRequired[str]
    updateStatus: NotRequired[DataLakeUpdateStatusTypeDef]

class CreateSubscriberNotificationRequestRequestTypeDef(TypedDict):
    configuration: NotificationConfigurationTypeDef
    subscriberId: str

class UpdateSubscriberNotificationRequestRequestTypeDef(TypedDict):
    configuration: NotificationConfigurationTypeDef
    subscriberId: str

class CreateDataLakeOrganizationConfigurationRequestRequestTypeDef(TypedDict):
    autoEnableNewAccount: NotRequired[
        Sequence[DataLakeAutoEnableNewAccountConfigurationUnionTypeDef]
    ]

class CreateSubscriberRequestRequestTypeDef(TypedDict):
    sources: Sequence[LogSourceResourceTypeDef]
    subscriberIdentity: AwsIdentityTypeDef
    subscriberName: str
    accessTypes: NotRequired[Sequence[AccessTypeType]]
    subscriberDescription: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class ListLogSourcesRequestListLogSourcesPaginateTypeDef(TypedDict):
    accounts: NotRequired[Sequence[str]]
    regions: NotRequired[Sequence[str]]
    sources: NotRequired[Sequence[LogSourceResourceTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLogSourcesRequestRequestTypeDef(TypedDict):
    accounts: NotRequired[Sequence[str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    regions: NotRequired[Sequence[str]]
    sources: NotRequired[Sequence[LogSourceResourceTypeDef]]

class LogSourceTypeDef(TypedDict):
    account: NotRequired[str]
    region: NotRequired[str]
    sources: NotRequired[List[LogSourceResourceTypeDef]]

class SubscriberResourceTypeDef(TypedDict):
    sources: List[LogSourceResourceTypeDef]
    subscriberArn: str
    subscriberId: str
    subscriberIdentity: AwsIdentityTypeDef
    subscriberName: str
    accessTypes: NotRequired[List[AccessTypeType]]
    createdAt: NotRequired[datetime]
    resourceShareArn: NotRequired[str]
    resourceShareName: NotRequired[str]
    roleArn: NotRequired[str]
    s3BucketArn: NotRequired[str]
    subscriberDescription: NotRequired[str]
    subscriberEndpoint: NotRequired[str]
    subscriberStatus: NotRequired[SubscriberStatusType]
    updatedAt: NotRequired[datetime]

class UpdateSubscriberRequestRequestTypeDef(TypedDict):
    subscriberId: str
    sources: NotRequired[Sequence[LogSourceResourceTypeDef]]
    subscriberDescription: NotRequired[str]
    subscriberIdentity: NotRequired[AwsIdentityTypeDef]
    subscriberName: NotRequired[str]

class DataLakeConfigurationTypeDef(TypedDict):
    region: str
    encryptionConfiguration: NotRequired[DataLakeEncryptionConfigurationTypeDef]
    lifecycleConfiguration: NotRequired[DataLakeLifecycleConfigurationUnionTypeDef]
    replicationConfiguration: NotRequired[DataLakeReplicationConfigurationUnionTypeDef]

class CreateDataLakeResponseTypeDef(TypedDict):
    dataLakes: List[DataLakeResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListDataLakesResponseTypeDef(TypedDict):
    dataLakes: List[DataLakeResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDataLakeResponseTypeDef(TypedDict):
    dataLakes: List[DataLakeResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListLogSourcesResponseTypeDef(TypedDict):
    sources: List[LogSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateSubscriberResponseTypeDef(TypedDict):
    subscriber: SubscriberResourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSubscriberResponseTypeDef(TypedDict):
    subscriber: SubscriberResourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSubscribersResponseTypeDef(TypedDict):
    subscribers: List[SubscriberResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateSubscriberResponseTypeDef(TypedDict):
    subscriber: SubscriberResourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDataLakeRequestRequestTypeDef(TypedDict):
    configurations: Sequence[DataLakeConfigurationTypeDef]
    metaStoreManagerRoleArn: str
    tags: NotRequired[Sequence[TagTypeDef]]

class UpdateDataLakeRequestRequestTypeDef(TypedDict):
    configurations: Sequence[DataLakeConfigurationTypeDef]
    metaStoreManagerRoleArn: NotRequired[str]
