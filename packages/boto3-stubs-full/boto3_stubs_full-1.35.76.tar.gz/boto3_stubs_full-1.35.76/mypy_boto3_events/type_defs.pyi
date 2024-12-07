"""
Type annotations for events service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_events/type_defs/)

Usage::

    ```python
    from mypy_boto3_events.type_defs import ActivateEventSourceRequestRequestTypeDef

    data: ActivateEventSourceRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ApiDestinationHttpMethodType,
    ApiDestinationStateType,
    ArchiveStateType,
    AssignPublicIpType,
    ConnectionAuthorizationTypeType,
    ConnectionOAuthHttpMethodType,
    ConnectionStateType,
    EndpointStateType,
    EventSourceStateType,
    LaunchTypeType,
    PlacementConstraintTypeType,
    PlacementStrategyTypeType,
    ReplayStateType,
    ReplicationStateType,
    RuleStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ActivateEventSourceRequestRequestTypeDef",
    "ApiDestinationTypeDef",
    "AppSyncParametersTypeDef",
    "ArchiveTypeDef",
    "AwsVpcConfigurationOutputTypeDef",
    "AwsVpcConfigurationTypeDef",
    "AwsVpcConfigurationUnionTypeDef",
    "BatchArrayPropertiesTypeDef",
    "BatchParametersTypeDef",
    "BatchRetryStrategyTypeDef",
    "CancelReplayRequestRequestTypeDef",
    "CancelReplayResponseTypeDef",
    "CapacityProviderStrategyItemTypeDef",
    "ConditionTypeDef",
    "ConnectionApiKeyAuthResponseParametersTypeDef",
    "ConnectionAuthResponseParametersTypeDef",
    "ConnectionBasicAuthResponseParametersTypeDef",
    "ConnectionBodyParameterTypeDef",
    "ConnectionHeaderParameterTypeDef",
    "ConnectionHttpParametersOutputTypeDef",
    "ConnectionHttpParametersTypeDef",
    "ConnectionHttpParametersUnionTypeDef",
    "ConnectionOAuthClientResponseParametersTypeDef",
    "ConnectionOAuthResponseParametersTypeDef",
    "ConnectionQueryStringParameterTypeDef",
    "ConnectionTypeDef",
    "ConnectivityResourceConfigurationArnTypeDef",
    "ConnectivityResourceParametersTypeDef",
    "CreateApiDestinationRequestRequestTypeDef",
    "CreateApiDestinationResponseTypeDef",
    "CreateArchiveRequestRequestTypeDef",
    "CreateArchiveResponseTypeDef",
    "CreateConnectionApiKeyAuthRequestParametersTypeDef",
    "CreateConnectionAuthRequestParametersTypeDef",
    "CreateConnectionBasicAuthRequestParametersTypeDef",
    "CreateConnectionOAuthClientRequestParametersTypeDef",
    "CreateConnectionOAuthRequestParametersTypeDef",
    "CreateConnectionRequestRequestTypeDef",
    "CreateConnectionResponseTypeDef",
    "CreateEndpointRequestRequestTypeDef",
    "CreateEndpointResponseTypeDef",
    "CreateEventBusRequestRequestTypeDef",
    "CreateEventBusResponseTypeDef",
    "CreatePartnerEventSourceRequestRequestTypeDef",
    "CreatePartnerEventSourceResponseTypeDef",
    "DeactivateEventSourceRequestRequestTypeDef",
    "DeadLetterConfigTypeDef",
    "DeauthorizeConnectionRequestRequestTypeDef",
    "DeauthorizeConnectionResponseTypeDef",
    "DeleteApiDestinationRequestRequestTypeDef",
    "DeleteArchiveRequestRequestTypeDef",
    "DeleteConnectionRequestRequestTypeDef",
    "DeleteConnectionResponseTypeDef",
    "DeleteEndpointRequestRequestTypeDef",
    "DeleteEventBusRequestRequestTypeDef",
    "DeletePartnerEventSourceRequestRequestTypeDef",
    "DeleteRuleRequestRequestTypeDef",
    "DescribeApiDestinationRequestRequestTypeDef",
    "DescribeApiDestinationResponseTypeDef",
    "DescribeArchiveRequestRequestTypeDef",
    "DescribeArchiveResponseTypeDef",
    "DescribeConnectionConnectivityParametersTypeDef",
    "DescribeConnectionRequestRequestTypeDef",
    "DescribeConnectionResourceParametersTypeDef",
    "DescribeConnectionResponseTypeDef",
    "DescribeEndpointRequestRequestTypeDef",
    "DescribeEndpointResponseTypeDef",
    "DescribeEventBusRequestRequestTypeDef",
    "DescribeEventBusResponseTypeDef",
    "DescribeEventSourceRequestRequestTypeDef",
    "DescribeEventSourceResponseTypeDef",
    "DescribePartnerEventSourceRequestRequestTypeDef",
    "DescribePartnerEventSourceResponseTypeDef",
    "DescribeReplayRequestRequestTypeDef",
    "DescribeReplayResponseTypeDef",
    "DescribeRuleRequestRequestTypeDef",
    "DescribeRuleResponseTypeDef",
    "DisableRuleRequestRequestTypeDef",
    "EcsParametersOutputTypeDef",
    "EcsParametersTypeDef",
    "EcsParametersUnionTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableRuleRequestRequestTypeDef",
    "EndpointEventBusTypeDef",
    "EndpointTypeDef",
    "EventBusTypeDef",
    "EventSourceTypeDef",
    "FailoverConfigTypeDef",
    "HttpParametersOutputTypeDef",
    "HttpParametersTypeDef",
    "HttpParametersUnionTypeDef",
    "InputTransformerOutputTypeDef",
    "InputTransformerTypeDef",
    "InputTransformerUnionTypeDef",
    "KinesisParametersTypeDef",
    "ListApiDestinationsRequestRequestTypeDef",
    "ListApiDestinationsResponseTypeDef",
    "ListArchivesRequestRequestTypeDef",
    "ListArchivesResponseTypeDef",
    "ListConnectionsRequestRequestTypeDef",
    "ListConnectionsResponseTypeDef",
    "ListEndpointsRequestRequestTypeDef",
    "ListEndpointsResponseTypeDef",
    "ListEventBusesRequestRequestTypeDef",
    "ListEventBusesResponseTypeDef",
    "ListEventSourcesRequestRequestTypeDef",
    "ListEventSourcesResponseTypeDef",
    "ListPartnerEventSourceAccountsRequestRequestTypeDef",
    "ListPartnerEventSourceAccountsResponseTypeDef",
    "ListPartnerEventSourcesRequestRequestTypeDef",
    "ListPartnerEventSourcesResponseTypeDef",
    "ListReplaysRequestRequestTypeDef",
    "ListReplaysResponseTypeDef",
    "ListRuleNamesByTargetRequestListRuleNamesByTargetPaginateTypeDef",
    "ListRuleNamesByTargetRequestRequestTypeDef",
    "ListRuleNamesByTargetResponseTypeDef",
    "ListRulesRequestListRulesPaginateTypeDef",
    "ListRulesRequestRequestTypeDef",
    "ListRulesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTargetsByRuleRequestListTargetsByRulePaginateTypeDef",
    "ListTargetsByRuleRequestRequestTypeDef",
    "ListTargetsByRuleResponseTypeDef",
    "NetworkConfigurationOutputTypeDef",
    "NetworkConfigurationTypeDef",
    "NetworkConfigurationUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PartnerEventSourceAccountTypeDef",
    "PartnerEventSourceTypeDef",
    "PlacementConstraintTypeDef",
    "PlacementStrategyTypeDef",
    "PrimaryTypeDef",
    "PutEventsRequestEntryTypeDef",
    "PutEventsRequestRequestTypeDef",
    "PutEventsResponseTypeDef",
    "PutEventsResultEntryTypeDef",
    "PutPartnerEventsRequestEntryTypeDef",
    "PutPartnerEventsRequestRequestTypeDef",
    "PutPartnerEventsResponseTypeDef",
    "PutPartnerEventsResultEntryTypeDef",
    "PutPermissionRequestRequestTypeDef",
    "PutRuleRequestRequestTypeDef",
    "PutRuleResponseTypeDef",
    "PutTargetsRequestRequestTypeDef",
    "PutTargetsResponseTypeDef",
    "PutTargetsResultEntryTypeDef",
    "RedshiftDataParametersOutputTypeDef",
    "RedshiftDataParametersTypeDef",
    "RedshiftDataParametersUnionTypeDef",
    "RemovePermissionRequestRequestTypeDef",
    "RemoveTargetsRequestRequestTypeDef",
    "RemoveTargetsResponseTypeDef",
    "RemoveTargetsResultEntryTypeDef",
    "ReplayDestinationOutputTypeDef",
    "ReplayDestinationTypeDef",
    "ReplayTypeDef",
    "ReplicationConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RetryPolicyTypeDef",
    "RoutingConfigTypeDef",
    "RuleTypeDef",
    "RunCommandParametersOutputTypeDef",
    "RunCommandParametersTypeDef",
    "RunCommandParametersUnionTypeDef",
    "RunCommandTargetOutputTypeDef",
    "RunCommandTargetTypeDef",
    "RunCommandTargetUnionTypeDef",
    "SageMakerPipelineParameterTypeDef",
    "SageMakerPipelineParametersOutputTypeDef",
    "SageMakerPipelineParametersTypeDef",
    "SageMakerPipelineParametersUnionTypeDef",
    "SecondaryTypeDef",
    "SqsParametersTypeDef",
    "StartReplayRequestRequestTypeDef",
    "StartReplayResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TargetOutputTypeDef",
    "TargetTypeDef",
    "TargetUnionTypeDef",
    "TestEventPatternRequestRequestTypeDef",
    "TestEventPatternResponseTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApiDestinationRequestRequestTypeDef",
    "UpdateApiDestinationResponseTypeDef",
    "UpdateArchiveRequestRequestTypeDef",
    "UpdateArchiveResponseTypeDef",
    "UpdateConnectionApiKeyAuthRequestParametersTypeDef",
    "UpdateConnectionAuthRequestParametersTypeDef",
    "UpdateConnectionBasicAuthRequestParametersTypeDef",
    "UpdateConnectionOAuthClientRequestParametersTypeDef",
    "UpdateConnectionOAuthRequestParametersTypeDef",
    "UpdateConnectionRequestRequestTypeDef",
    "UpdateConnectionResponseTypeDef",
    "UpdateEndpointRequestRequestTypeDef",
    "UpdateEndpointResponseTypeDef",
    "UpdateEventBusRequestRequestTypeDef",
    "UpdateEventBusResponseTypeDef",
)

class ActivateEventSourceRequestRequestTypeDef(TypedDict):
    Name: str

class ApiDestinationTypeDef(TypedDict):
    ApiDestinationArn: NotRequired[str]
    Name: NotRequired[str]
    ApiDestinationState: NotRequired[ApiDestinationStateType]
    ConnectionArn: NotRequired[str]
    InvocationEndpoint: NotRequired[str]
    HttpMethod: NotRequired[ApiDestinationHttpMethodType]
    InvocationRateLimitPerSecond: NotRequired[int]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]

class AppSyncParametersTypeDef(TypedDict):
    GraphQLOperation: NotRequired[str]

class ArchiveTypeDef(TypedDict):
    ArchiveName: NotRequired[str]
    EventSourceArn: NotRequired[str]
    State: NotRequired[ArchiveStateType]
    StateReason: NotRequired[str]
    RetentionDays: NotRequired[int]
    SizeBytes: NotRequired[int]
    EventCount: NotRequired[int]
    CreationTime: NotRequired[datetime]

class AwsVpcConfigurationOutputTypeDef(TypedDict):
    Subnets: List[str]
    SecurityGroups: NotRequired[List[str]]
    AssignPublicIp: NotRequired[AssignPublicIpType]

class AwsVpcConfigurationTypeDef(TypedDict):
    Subnets: Sequence[str]
    SecurityGroups: NotRequired[Sequence[str]]
    AssignPublicIp: NotRequired[AssignPublicIpType]

class BatchArrayPropertiesTypeDef(TypedDict):
    Size: NotRequired[int]

class BatchRetryStrategyTypeDef(TypedDict):
    Attempts: NotRequired[int]

class CancelReplayRequestRequestTypeDef(TypedDict):
    ReplayName: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CapacityProviderStrategyItemTypeDef(TypedDict):
    capacityProvider: str
    weight: NotRequired[int]
    base: NotRequired[int]

ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {
        "Type": str,
        "Key": str,
        "Value": str,
    },
)

class ConnectionApiKeyAuthResponseParametersTypeDef(TypedDict):
    ApiKeyName: NotRequired[str]

class ConnectionBasicAuthResponseParametersTypeDef(TypedDict):
    Username: NotRequired[str]

class ConnectionBodyParameterTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]
    IsValueSecret: NotRequired[bool]

class ConnectionHeaderParameterTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]
    IsValueSecret: NotRequired[bool]

class ConnectionQueryStringParameterTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]
    IsValueSecret: NotRequired[bool]

class ConnectionOAuthClientResponseParametersTypeDef(TypedDict):
    ClientID: NotRequired[str]

class ConnectionTypeDef(TypedDict):
    ConnectionArn: NotRequired[str]
    Name: NotRequired[str]
    ConnectionState: NotRequired[ConnectionStateType]
    StateReason: NotRequired[str]
    AuthorizationType: NotRequired[ConnectionAuthorizationTypeType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    LastAuthorizedTime: NotRequired[datetime]

class ConnectivityResourceConfigurationArnTypeDef(TypedDict):
    ResourceConfigurationArn: str

class CreateApiDestinationRequestRequestTypeDef(TypedDict):
    Name: str
    ConnectionArn: str
    InvocationEndpoint: str
    HttpMethod: ApiDestinationHttpMethodType
    Description: NotRequired[str]
    InvocationRateLimitPerSecond: NotRequired[int]

class CreateArchiveRequestRequestTypeDef(TypedDict):
    ArchiveName: str
    EventSourceArn: str
    Description: NotRequired[str]
    EventPattern: NotRequired[str]
    RetentionDays: NotRequired[int]

class CreateConnectionApiKeyAuthRequestParametersTypeDef(TypedDict):
    ApiKeyName: str
    ApiKeyValue: str

class CreateConnectionBasicAuthRequestParametersTypeDef(TypedDict):
    Username: str
    Password: str

class CreateConnectionOAuthClientRequestParametersTypeDef(TypedDict):
    ClientID: str
    ClientSecret: str

class EndpointEventBusTypeDef(TypedDict):
    EventBusArn: str

class ReplicationConfigTypeDef(TypedDict):
    State: NotRequired[ReplicationStateType]

class DeadLetterConfigTypeDef(TypedDict):
    Arn: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class CreatePartnerEventSourceRequestRequestTypeDef(TypedDict):
    Name: str
    Account: str

class DeactivateEventSourceRequestRequestTypeDef(TypedDict):
    Name: str

class DeauthorizeConnectionRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteApiDestinationRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteArchiveRequestRequestTypeDef(TypedDict):
    ArchiveName: str

class DeleteConnectionRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteEndpointRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteEventBusRequestRequestTypeDef(TypedDict):
    Name: str

class DeletePartnerEventSourceRequestRequestTypeDef(TypedDict):
    Name: str
    Account: str

class DeleteRuleRequestRequestTypeDef(TypedDict):
    Name: str
    EventBusName: NotRequired[str]
    Force: NotRequired[bool]

class DescribeApiDestinationRequestRequestTypeDef(TypedDict):
    Name: str

class DescribeArchiveRequestRequestTypeDef(TypedDict):
    ArchiveName: str

class DescribeConnectionResourceParametersTypeDef(TypedDict):
    ResourceConfigurationArn: str
    ResourceAssociationArn: str

class DescribeConnectionRequestRequestTypeDef(TypedDict):
    Name: str

class DescribeEndpointRequestRequestTypeDef(TypedDict):
    Name: str
    HomeRegion: NotRequired[str]

class DescribeEventBusRequestRequestTypeDef(TypedDict):
    Name: NotRequired[str]

class DescribeEventSourceRequestRequestTypeDef(TypedDict):
    Name: str

class DescribePartnerEventSourceRequestRequestTypeDef(TypedDict):
    Name: str

class DescribeReplayRequestRequestTypeDef(TypedDict):
    ReplayName: str

class ReplayDestinationOutputTypeDef(TypedDict):
    Arn: str
    FilterArns: NotRequired[List[str]]

class DescribeRuleRequestRequestTypeDef(TypedDict):
    Name: str
    EventBusName: NotRequired[str]

class DisableRuleRequestRequestTypeDef(TypedDict):
    Name: str
    EventBusName: NotRequired[str]

PlacementConstraintTypeDef = TypedDict(
    "PlacementConstraintTypeDef",
    {
        "type": NotRequired[PlacementConstraintTypeType],
        "expression": NotRequired[str],
    },
)
PlacementStrategyTypeDef = TypedDict(
    "PlacementStrategyTypeDef",
    {
        "type": NotRequired[PlacementStrategyTypeType],
        "field": NotRequired[str],
    },
)

class EnableRuleRequestRequestTypeDef(TypedDict):
    Name: str
    EventBusName: NotRequired[str]

class EventBusTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]
    Description: NotRequired[str]
    Policy: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]

class EventSourceTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreatedBy: NotRequired[str]
    CreationTime: NotRequired[datetime]
    ExpirationTime: NotRequired[datetime]
    Name: NotRequired[str]
    State: NotRequired[EventSourceStateType]

class PrimaryTypeDef(TypedDict):
    HealthCheck: str

class SecondaryTypeDef(TypedDict):
    Route: str

class HttpParametersOutputTypeDef(TypedDict):
    PathParameterValues: NotRequired[List[str]]
    HeaderParameters: NotRequired[Dict[str, str]]
    QueryStringParameters: NotRequired[Dict[str, str]]

class HttpParametersTypeDef(TypedDict):
    PathParameterValues: NotRequired[Sequence[str]]
    HeaderParameters: NotRequired[Mapping[str, str]]
    QueryStringParameters: NotRequired[Mapping[str, str]]

class InputTransformerOutputTypeDef(TypedDict):
    InputTemplate: str
    InputPathsMap: NotRequired[Dict[str, str]]

class InputTransformerTypeDef(TypedDict):
    InputTemplate: str
    InputPathsMap: NotRequired[Mapping[str, str]]

class KinesisParametersTypeDef(TypedDict):
    PartitionKeyPath: str

class ListApiDestinationsRequestRequestTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    ConnectionArn: NotRequired[str]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class ListArchivesRequestRequestTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    EventSourceArn: NotRequired[str]
    State: NotRequired[ArchiveStateType]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class ListConnectionsRequestRequestTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    ConnectionState: NotRequired[ConnectionStateType]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class ListEndpointsRequestRequestTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    HomeRegion: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListEventBusesRequestRequestTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class ListEventSourcesRequestRequestTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class ListPartnerEventSourceAccountsRequestRequestTypeDef(TypedDict):
    EventSourceName: str
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class PartnerEventSourceAccountTypeDef(TypedDict):
    Account: NotRequired[str]
    CreationTime: NotRequired[datetime]
    ExpirationTime: NotRequired[datetime]
    State: NotRequired[EventSourceStateType]

class ListPartnerEventSourcesRequestRequestTypeDef(TypedDict):
    NamePrefix: str
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class PartnerEventSourceTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]

class ListReplaysRequestRequestTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    State: NotRequired[ReplayStateType]
    EventSourceArn: NotRequired[str]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class ReplayTypeDef(TypedDict):
    ReplayName: NotRequired[str]
    EventSourceArn: NotRequired[str]
    State: NotRequired[ReplayStateType]
    StateReason: NotRequired[str]
    EventStartTime: NotRequired[datetime]
    EventEndTime: NotRequired[datetime]
    EventLastReplayedTime: NotRequired[datetime]
    ReplayStartTime: NotRequired[datetime]
    ReplayEndTime: NotRequired[datetime]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListRuleNamesByTargetRequestRequestTypeDef(TypedDict):
    TargetArn: str
    EventBusName: NotRequired[str]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class ListRulesRequestRequestTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    EventBusName: NotRequired[str]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

class RuleTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]
    EventPattern: NotRequired[str]
    State: NotRequired[RuleStateType]
    Description: NotRequired[str]
    ScheduleExpression: NotRequired[str]
    RoleArn: NotRequired[str]
    ManagedBy: NotRequired[str]
    EventBusName: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str

class ListTargetsByRuleRequestRequestTypeDef(TypedDict):
    Rule: str
    EventBusName: NotRequired[str]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]

TimestampTypeDef = Union[datetime, str]

class PutEventsResultEntryTypeDef(TypedDict):
    EventId: NotRequired[str]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]

class PutPartnerEventsResultEntryTypeDef(TypedDict):
    EventId: NotRequired[str]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]

class PutTargetsResultEntryTypeDef(TypedDict):
    TargetId: NotRequired[str]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]

class RedshiftDataParametersOutputTypeDef(TypedDict):
    Database: str
    SecretManagerArn: NotRequired[str]
    DbUser: NotRequired[str]
    Sql: NotRequired[str]
    StatementName: NotRequired[str]
    WithEvent: NotRequired[bool]
    Sqls: NotRequired[List[str]]

class RedshiftDataParametersTypeDef(TypedDict):
    Database: str
    SecretManagerArn: NotRequired[str]
    DbUser: NotRequired[str]
    Sql: NotRequired[str]
    StatementName: NotRequired[str]
    WithEvent: NotRequired[bool]
    Sqls: NotRequired[Sequence[str]]

class RemovePermissionRequestRequestTypeDef(TypedDict):
    StatementId: NotRequired[str]
    RemoveAllPermissions: NotRequired[bool]
    EventBusName: NotRequired[str]

class RemoveTargetsRequestRequestTypeDef(TypedDict):
    Rule: str
    Ids: Sequence[str]
    EventBusName: NotRequired[str]
    Force: NotRequired[bool]

class RemoveTargetsResultEntryTypeDef(TypedDict):
    TargetId: NotRequired[str]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]

class ReplayDestinationTypeDef(TypedDict):
    Arn: str
    FilterArns: NotRequired[Sequence[str]]

class RetryPolicyTypeDef(TypedDict):
    MaximumRetryAttempts: NotRequired[int]
    MaximumEventAgeInSeconds: NotRequired[int]

class RunCommandTargetOutputTypeDef(TypedDict):
    Key: str
    Values: List[str]

class RunCommandTargetTypeDef(TypedDict):
    Key: str
    Values: Sequence[str]

class SageMakerPipelineParameterTypeDef(TypedDict):
    Name: str
    Value: str

class SqsParametersTypeDef(TypedDict):
    MessageGroupId: NotRequired[str]

class TestEventPatternRequestRequestTypeDef(TypedDict):
    EventPattern: str
    Event: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]

class UpdateApiDestinationRequestRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    ConnectionArn: NotRequired[str]
    InvocationEndpoint: NotRequired[str]
    HttpMethod: NotRequired[ApiDestinationHttpMethodType]
    InvocationRateLimitPerSecond: NotRequired[int]

class UpdateArchiveRequestRequestTypeDef(TypedDict):
    ArchiveName: str
    Description: NotRequired[str]
    EventPattern: NotRequired[str]
    RetentionDays: NotRequired[int]

class UpdateConnectionApiKeyAuthRequestParametersTypeDef(TypedDict):
    ApiKeyName: NotRequired[str]
    ApiKeyValue: NotRequired[str]

class UpdateConnectionBasicAuthRequestParametersTypeDef(TypedDict):
    Username: NotRequired[str]
    Password: NotRequired[str]

class UpdateConnectionOAuthClientRequestParametersTypeDef(TypedDict):
    ClientID: NotRequired[str]
    ClientSecret: NotRequired[str]

class NetworkConfigurationOutputTypeDef(TypedDict):
    awsvpcConfiguration: NotRequired[AwsVpcConfigurationOutputTypeDef]

AwsVpcConfigurationUnionTypeDef = Union[
    AwsVpcConfigurationTypeDef, AwsVpcConfigurationOutputTypeDef
]

class BatchParametersTypeDef(TypedDict):
    JobDefinition: str
    JobName: str
    ArrayProperties: NotRequired[BatchArrayPropertiesTypeDef]
    RetryStrategy: NotRequired[BatchRetryStrategyTypeDef]

class CancelReplayResponseTypeDef(TypedDict):
    ReplayArn: str
    State: ReplayStateType
    StateReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateApiDestinationResponseTypeDef(TypedDict):
    ApiDestinationArn: str
    ApiDestinationState: ApiDestinationStateType
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateArchiveResponseTypeDef(TypedDict):
    ArchiveArn: str
    State: ArchiveStateType
    StateReason: str
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateConnectionResponseTypeDef(TypedDict):
    ConnectionArn: str
    ConnectionState: ConnectionStateType
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePartnerEventSourceResponseTypeDef(TypedDict):
    EventSourceArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeauthorizeConnectionResponseTypeDef(TypedDict):
    ConnectionArn: str
    ConnectionState: ConnectionStateType
    CreationTime: datetime
    LastModifiedTime: datetime
    LastAuthorizedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteConnectionResponseTypeDef(TypedDict):
    ConnectionArn: str
    ConnectionState: ConnectionStateType
    CreationTime: datetime
    LastModifiedTime: datetime
    LastAuthorizedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeApiDestinationResponseTypeDef(TypedDict):
    ApiDestinationArn: str
    Name: str
    Description: str
    ApiDestinationState: ApiDestinationStateType
    ConnectionArn: str
    InvocationEndpoint: str
    HttpMethod: ApiDestinationHttpMethodType
    InvocationRateLimitPerSecond: int
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeArchiveResponseTypeDef(TypedDict):
    ArchiveArn: str
    ArchiveName: str
    EventSourceArn: str
    Description: str
    EventPattern: str
    State: ArchiveStateType
    StateReason: str
    RetentionDays: int
    SizeBytes: int
    EventCount: int
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeEventSourceResponseTypeDef(TypedDict):
    Arn: str
    CreatedBy: str
    CreationTime: datetime
    ExpirationTime: datetime
    Name: str
    State: EventSourceStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePartnerEventSourceResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeRuleResponseTypeDef(TypedDict):
    Name: str
    Arn: str
    EventPattern: str
    ScheduleExpression: str
    State: RuleStateType
    Description: str
    RoleArn: str
    ManagedBy: str
    EventBusName: str
    CreatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListApiDestinationsResponseTypeDef(TypedDict):
    ApiDestinations: List[ApiDestinationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListArchivesResponseTypeDef(TypedDict):
    Archives: List[ArchiveTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListRuleNamesByTargetResponseTypeDef(TypedDict):
    RuleNames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PutRuleResponseTypeDef(TypedDict):
    RuleArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartReplayResponseTypeDef(TypedDict):
    ReplayArn: str
    State: ReplayStateType
    StateReason: str
    ReplayStartTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class TestEventPatternResponseTypeDef(TypedDict):
    Result: bool
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApiDestinationResponseTypeDef(TypedDict):
    ApiDestinationArn: str
    ApiDestinationState: ApiDestinationStateType
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateArchiveResponseTypeDef(TypedDict):
    ArchiveArn: str
    State: ArchiveStateType
    StateReason: str
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConnectionResponseTypeDef(TypedDict):
    ConnectionArn: str
    ConnectionState: ConnectionStateType
    CreationTime: datetime
    LastModifiedTime: datetime
    LastAuthorizedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class PutPermissionRequestRequestTypeDef(TypedDict):
    EventBusName: NotRequired[str]
    Action: NotRequired[str]
    Principal: NotRequired[str]
    StatementId: NotRequired[str]
    Condition: NotRequired[ConditionTypeDef]
    Policy: NotRequired[str]

class ConnectionHttpParametersOutputTypeDef(TypedDict):
    HeaderParameters: NotRequired[List[ConnectionHeaderParameterTypeDef]]
    QueryStringParameters: NotRequired[List[ConnectionQueryStringParameterTypeDef]]
    BodyParameters: NotRequired[List[ConnectionBodyParameterTypeDef]]

class ConnectionHttpParametersTypeDef(TypedDict):
    HeaderParameters: NotRequired[Sequence[ConnectionHeaderParameterTypeDef]]
    QueryStringParameters: NotRequired[Sequence[ConnectionQueryStringParameterTypeDef]]
    BodyParameters: NotRequired[Sequence[ConnectionBodyParameterTypeDef]]

class ListConnectionsResponseTypeDef(TypedDict):
    Connections: List[ConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ConnectivityResourceParametersTypeDef(TypedDict):
    ResourceParameters: ConnectivityResourceConfigurationArnTypeDef

class CreateEventBusResponseTypeDef(TypedDict):
    EventBusArn: str
    Description: str
    KmsKeyIdentifier: str
    DeadLetterConfig: DeadLetterConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeEventBusResponseTypeDef(TypedDict):
    Name: str
    Arn: str
    Description: str
    KmsKeyIdentifier: str
    DeadLetterConfig: DeadLetterConfigTypeDef
    Policy: str
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEventBusRequestRequestTypeDef(TypedDict):
    Name: NotRequired[str]
    KmsKeyIdentifier: NotRequired[str]
    Description: NotRequired[str]
    DeadLetterConfig: NotRequired[DeadLetterConfigTypeDef]

class UpdateEventBusResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    KmsKeyIdentifier: str
    Description: str
    DeadLetterConfig: DeadLetterConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEventBusRequestRequestTypeDef(TypedDict):
    Name: str
    EventSourceName: NotRequired[str]
    Description: NotRequired[str]
    KmsKeyIdentifier: NotRequired[str]
    DeadLetterConfig: NotRequired[DeadLetterConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PutRuleRequestRequestTypeDef(TypedDict):
    Name: str
    ScheduleExpression: NotRequired[str]
    EventPattern: NotRequired[str]
    State: NotRequired[RuleStateType]
    Description: NotRequired[str]
    RoleArn: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    EventBusName: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]

class DescribeConnectionConnectivityParametersTypeDef(TypedDict):
    ResourceParameters: DescribeConnectionResourceParametersTypeDef

class DescribeReplayResponseTypeDef(TypedDict):
    ReplayName: str
    ReplayArn: str
    Description: str
    State: ReplayStateType
    StateReason: str
    EventSourceArn: str
    Destination: ReplayDestinationOutputTypeDef
    EventStartTime: datetime
    EventEndTime: datetime
    EventLastReplayedTime: datetime
    ReplayStartTime: datetime
    ReplayEndTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListEventBusesResponseTypeDef(TypedDict):
    EventBuses: List[EventBusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListEventSourcesResponseTypeDef(TypedDict):
    EventSources: List[EventSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class FailoverConfigTypeDef(TypedDict):
    Primary: PrimaryTypeDef
    Secondary: SecondaryTypeDef

HttpParametersUnionTypeDef = Union[HttpParametersTypeDef, HttpParametersOutputTypeDef]
InputTransformerUnionTypeDef = Union[InputTransformerTypeDef, InputTransformerOutputTypeDef]

class ListPartnerEventSourceAccountsResponseTypeDef(TypedDict):
    PartnerEventSourceAccounts: List[PartnerEventSourceAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPartnerEventSourcesResponseTypeDef(TypedDict):
    PartnerEventSources: List[PartnerEventSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListReplaysResponseTypeDef(TypedDict):
    Replays: List[ReplayTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListRuleNamesByTargetRequestListRuleNamesByTargetPaginateTypeDef(TypedDict):
    TargetArn: str
    EventBusName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRulesRequestListRulesPaginateTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    EventBusName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTargetsByRuleRequestListTargetsByRulePaginateTypeDef(TypedDict):
    Rule: str
    EventBusName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRulesResponseTypeDef(TypedDict):
    Rules: List[RuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PutEventsRequestEntryTypeDef(TypedDict):
    Time: NotRequired[TimestampTypeDef]
    Source: NotRequired[str]
    Resources: NotRequired[Sequence[str]]
    DetailType: NotRequired[str]
    Detail: NotRequired[str]
    EventBusName: NotRequired[str]
    TraceHeader: NotRequired[str]

class PutPartnerEventsRequestEntryTypeDef(TypedDict):
    Time: NotRequired[TimestampTypeDef]
    Source: NotRequired[str]
    Resources: NotRequired[Sequence[str]]
    DetailType: NotRequired[str]
    Detail: NotRequired[str]

class PutEventsResponseTypeDef(TypedDict):
    FailedEntryCount: int
    Entries: List[PutEventsResultEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PutPartnerEventsResponseTypeDef(TypedDict):
    FailedEntryCount: int
    Entries: List[PutPartnerEventsResultEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PutTargetsResponseTypeDef(TypedDict):
    FailedEntryCount: int
    FailedEntries: List[PutTargetsResultEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

RedshiftDataParametersUnionTypeDef = Union[
    RedshiftDataParametersTypeDef, RedshiftDataParametersOutputTypeDef
]

class RemoveTargetsResponseTypeDef(TypedDict):
    FailedEntryCount: int
    FailedEntries: List[RemoveTargetsResultEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartReplayRequestRequestTypeDef(TypedDict):
    ReplayName: str
    EventSourceArn: str
    EventStartTime: TimestampTypeDef
    EventEndTime: TimestampTypeDef
    Destination: ReplayDestinationTypeDef
    Description: NotRequired[str]

class RunCommandParametersOutputTypeDef(TypedDict):
    RunCommandTargets: List[RunCommandTargetOutputTypeDef]

RunCommandTargetUnionTypeDef = Union[RunCommandTargetTypeDef, RunCommandTargetOutputTypeDef]

class SageMakerPipelineParametersOutputTypeDef(TypedDict):
    PipelineParameterList: NotRequired[List[SageMakerPipelineParameterTypeDef]]

class SageMakerPipelineParametersTypeDef(TypedDict):
    PipelineParameterList: NotRequired[Sequence[SageMakerPipelineParameterTypeDef]]

class EcsParametersOutputTypeDef(TypedDict):
    TaskDefinitionArn: str
    TaskCount: NotRequired[int]
    LaunchType: NotRequired[LaunchTypeType]
    NetworkConfiguration: NotRequired[NetworkConfigurationOutputTypeDef]
    PlatformVersion: NotRequired[str]
    Group: NotRequired[str]
    CapacityProviderStrategy: NotRequired[List[CapacityProviderStrategyItemTypeDef]]
    EnableECSManagedTags: NotRequired[bool]
    EnableExecuteCommand: NotRequired[bool]
    PlacementConstraints: NotRequired[List[PlacementConstraintTypeDef]]
    PlacementStrategy: NotRequired[List[PlacementStrategyTypeDef]]
    PropagateTags: NotRequired[Literal["TASK_DEFINITION"]]
    ReferenceId: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]

class NetworkConfigurationTypeDef(TypedDict):
    awsvpcConfiguration: NotRequired[AwsVpcConfigurationUnionTypeDef]

class ConnectionOAuthResponseParametersTypeDef(TypedDict):
    ClientParameters: NotRequired[ConnectionOAuthClientResponseParametersTypeDef]
    AuthorizationEndpoint: NotRequired[str]
    HttpMethod: NotRequired[ConnectionOAuthHttpMethodType]
    OAuthHttpParameters: NotRequired[ConnectionHttpParametersOutputTypeDef]

ConnectionHttpParametersUnionTypeDef = Union[
    ConnectionHttpParametersTypeDef, ConnectionHttpParametersOutputTypeDef
]

class RoutingConfigTypeDef(TypedDict):
    FailoverConfig: FailoverConfigTypeDef

class PutEventsRequestRequestTypeDef(TypedDict):
    Entries: Sequence[PutEventsRequestEntryTypeDef]
    EndpointId: NotRequired[str]

class PutPartnerEventsRequestRequestTypeDef(TypedDict):
    Entries: Sequence[PutPartnerEventsRequestEntryTypeDef]

class RunCommandParametersTypeDef(TypedDict):
    RunCommandTargets: Sequence[RunCommandTargetUnionTypeDef]

SageMakerPipelineParametersUnionTypeDef = Union[
    SageMakerPipelineParametersTypeDef, SageMakerPipelineParametersOutputTypeDef
]

class TargetOutputTypeDef(TypedDict):
    Id: str
    Arn: str
    RoleArn: NotRequired[str]
    Input: NotRequired[str]
    InputPath: NotRequired[str]
    InputTransformer: NotRequired[InputTransformerOutputTypeDef]
    KinesisParameters: NotRequired[KinesisParametersTypeDef]
    RunCommandParameters: NotRequired[RunCommandParametersOutputTypeDef]
    EcsParameters: NotRequired[EcsParametersOutputTypeDef]
    BatchParameters: NotRequired[BatchParametersTypeDef]
    SqsParameters: NotRequired[SqsParametersTypeDef]
    HttpParameters: NotRequired[HttpParametersOutputTypeDef]
    RedshiftDataParameters: NotRequired[RedshiftDataParametersOutputTypeDef]
    SageMakerPipelineParameters: NotRequired[SageMakerPipelineParametersOutputTypeDef]
    DeadLetterConfig: NotRequired[DeadLetterConfigTypeDef]
    RetryPolicy: NotRequired[RetryPolicyTypeDef]
    AppSyncParameters: NotRequired[AppSyncParametersTypeDef]

NetworkConfigurationUnionTypeDef = Union[
    NetworkConfigurationTypeDef, NetworkConfigurationOutputTypeDef
]

class ConnectionAuthResponseParametersTypeDef(TypedDict):
    BasicAuthParameters: NotRequired[ConnectionBasicAuthResponseParametersTypeDef]
    OAuthParameters: NotRequired[ConnectionOAuthResponseParametersTypeDef]
    ApiKeyAuthParameters: NotRequired[ConnectionApiKeyAuthResponseParametersTypeDef]
    InvocationHttpParameters: NotRequired[ConnectionHttpParametersOutputTypeDef]
    ConnectivityParameters: NotRequired[DescribeConnectionConnectivityParametersTypeDef]

class CreateConnectionOAuthRequestParametersTypeDef(TypedDict):
    ClientParameters: CreateConnectionOAuthClientRequestParametersTypeDef
    AuthorizationEndpoint: str
    HttpMethod: ConnectionOAuthHttpMethodType
    OAuthHttpParameters: NotRequired[ConnectionHttpParametersUnionTypeDef]

class UpdateConnectionOAuthRequestParametersTypeDef(TypedDict):
    ClientParameters: NotRequired[UpdateConnectionOAuthClientRequestParametersTypeDef]
    AuthorizationEndpoint: NotRequired[str]
    HttpMethod: NotRequired[ConnectionOAuthHttpMethodType]
    OAuthHttpParameters: NotRequired[ConnectionHttpParametersUnionTypeDef]

class CreateEndpointRequestRequestTypeDef(TypedDict):
    Name: str
    RoutingConfig: RoutingConfigTypeDef
    EventBuses: Sequence[EndpointEventBusTypeDef]
    Description: NotRequired[str]
    ReplicationConfig: NotRequired[ReplicationConfigTypeDef]
    RoleArn: NotRequired[str]

class CreateEndpointResponseTypeDef(TypedDict):
    Name: str
    Arn: str
    RoutingConfig: RoutingConfigTypeDef
    ReplicationConfig: ReplicationConfigTypeDef
    EventBuses: List[EndpointEventBusTypeDef]
    RoleArn: str
    State: EndpointStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeEndpointResponseTypeDef(TypedDict):
    Name: str
    Description: str
    Arn: str
    RoutingConfig: RoutingConfigTypeDef
    ReplicationConfig: ReplicationConfigTypeDef
    EventBuses: List[EndpointEventBusTypeDef]
    RoleArn: str
    EndpointId: str
    EndpointUrl: str
    State: EndpointStateType
    StateReason: str
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class EndpointTypeDef(TypedDict):
    Name: NotRequired[str]
    Description: NotRequired[str]
    Arn: NotRequired[str]
    RoutingConfig: NotRequired[RoutingConfigTypeDef]
    ReplicationConfig: NotRequired[ReplicationConfigTypeDef]
    EventBuses: NotRequired[List[EndpointEventBusTypeDef]]
    RoleArn: NotRequired[str]
    EndpointId: NotRequired[str]
    EndpointUrl: NotRequired[str]
    State: NotRequired[EndpointStateType]
    StateReason: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]

class UpdateEndpointRequestRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    RoutingConfig: NotRequired[RoutingConfigTypeDef]
    ReplicationConfig: NotRequired[ReplicationConfigTypeDef]
    EventBuses: NotRequired[Sequence[EndpointEventBusTypeDef]]
    RoleArn: NotRequired[str]

class UpdateEndpointResponseTypeDef(TypedDict):
    Name: str
    Arn: str
    RoutingConfig: RoutingConfigTypeDef
    ReplicationConfig: ReplicationConfigTypeDef
    EventBuses: List[EndpointEventBusTypeDef]
    RoleArn: str
    EndpointId: str
    EndpointUrl: str
    State: EndpointStateType
    ResponseMetadata: ResponseMetadataTypeDef

RunCommandParametersUnionTypeDef = Union[
    RunCommandParametersTypeDef, RunCommandParametersOutputTypeDef
]

class ListTargetsByRuleResponseTypeDef(TypedDict):
    Targets: List[TargetOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class EcsParametersTypeDef(TypedDict):
    TaskDefinitionArn: str
    TaskCount: NotRequired[int]
    LaunchType: NotRequired[LaunchTypeType]
    NetworkConfiguration: NotRequired[NetworkConfigurationUnionTypeDef]
    PlatformVersion: NotRequired[str]
    Group: NotRequired[str]
    CapacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    EnableECSManagedTags: NotRequired[bool]
    EnableExecuteCommand: NotRequired[bool]
    PlacementConstraints: NotRequired[Sequence[PlacementConstraintTypeDef]]
    PlacementStrategy: NotRequired[Sequence[PlacementStrategyTypeDef]]
    PropagateTags: NotRequired[Literal["TASK_DEFINITION"]]
    ReferenceId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class DescribeConnectionResponseTypeDef(TypedDict):
    ConnectionArn: str
    Name: str
    Description: str
    InvocationConnectivityParameters: DescribeConnectionConnectivityParametersTypeDef
    ConnectionState: ConnectionStateType
    StateReason: str
    AuthorizationType: ConnectionAuthorizationTypeType
    SecretArn: str
    AuthParameters: ConnectionAuthResponseParametersTypeDef
    CreationTime: datetime
    LastModifiedTime: datetime
    LastAuthorizedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateConnectionAuthRequestParametersTypeDef(TypedDict):
    BasicAuthParameters: NotRequired[CreateConnectionBasicAuthRequestParametersTypeDef]
    OAuthParameters: NotRequired[CreateConnectionOAuthRequestParametersTypeDef]
    ApiKeyAuthParameters: NotRequired[CreateConnectionApiKeyAuthRequestParametersTypeDef]
    InvocationHttpParameters: NotRequired[ConnectionHttpParametersUnionTypeDef]
    ConnectivityParameters: NotRequired[ConnectivityResourceParametersTypeDef]

class UpdateConnectionAuthRequestParametersTypeDef(TypedDict):
    BasicAuthParameters: NotRequired[UpdateConnectionBasicAuthRequestParametersTypeDef]
    OAuthParameters: NotRequired[UpdateConnectionOAuthRequestParametersTypeDef]
    ApiKeyAuthParameters: NotRequired[UpdateConnectionApiKeyAuthRequestParametersTypeDef]
    InvocationHttpParameters: NotRequired[ConnectionHttpParametersUnionTypeDef]
    ConnectivityParameters: NotRequired[ConnectivityResourceParametersTypeDef]

class ListEndpointsResponseTypeDef(TypedDict):
    Endpoints: List[EndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

EcsParametersUnionTypeDef = Union[EcsParametersTypeDef, EcsParametersOutputTypeDef]

class CreateConnectionRequestRequestTypeDef(TypedDict):
    Name: str
    AuthorizationType: ConnectionAuthorizationTypeType
    AuthParameters: CreateConnectionAuthRequestParametersTypeDef
    Description: NotRequired[str]
    InvocationConnectivityParameters: NotRequired[ConnectivityResourceParametersTypeDef]

class UpdateConnectionRequestRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    AuthorizationType: NotRequired[ConnectionAuthorizationTypeType]
    AuthParameters: NotRequired[UpdateConnectionAuthRequestParametersTypeDef]
    InvocationConnectivityParameters: NotRequired[ConnectivityResourceParametersTypeDef]

class TargetTypeDef(TypedDict):
    Id: str
    Arn: str
    RoleArn: NotRequired[str]
    Input: NotRequired[str]
    InputPath: NotRequired[str]
    InputTransformer: NotRequired[InputTransformerUnionTypeDef]
    KinesisParameters: NotRequired[KinesisParametersTypeDef]
    RunCommandParameters: NotRequired[RunCommandParametersUnionTypeDef]
    EcsParameters: NotRequired[EcsParametersUnionTypeDef]
    BatchParameters: NotRequired[BatchParametersTypeDef]
    SqsParameters: NotRequired[SqsParametersTypeDef]
    HttpParameters: NotRequired[HttpParametersUnionTypeDef]
    RedshiftDataParameters: NotRequired[RedshiftDataParametersUnionTypeDef]
    SageMakerPipelineParameters: NotRequired[SageMakerPipelineParametersUnionTypeDef]
    DeadLetterConfig: NotRequired[DeadLetterConfigTypeDef]
    RetryPolicy: NotRequired[RetryPolicyTypeDef]
    AppSyncParameters: NotRequired[AppSyncParametersTypeDef]

TargetUnionTypeDef = Union[TargetTypeDef, TargetOutputTypeDef]

class PutTargetsRequestRequestTypeDef(TypedDict):
    Rule: str
    Targets: Sequence[TargetUnionTypeDef]
    EventBusName: NotRequired[str]
