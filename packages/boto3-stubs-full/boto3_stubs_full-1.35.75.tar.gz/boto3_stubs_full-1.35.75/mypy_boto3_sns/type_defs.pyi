"""
Type annotations for sns service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/type_defs/)

Usage::

    ```python
    from mypy_boto3_sns.type_defs import AddPermissionInputRequestTypeDef

    data: AddPermissionInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    LanguageCodeStringType,
    NumberCapabilityType,
    RouteTypeType,
    SMSSandboxPhoneNumberVerificationStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AddPermissionInputRequestTypeDef",
    "AddPermissionInputTopicAddPermissionTypeDef",
    "BatchResultErrorEntryTypeDef",
    "BlobTypeDef",
    "CheckIfPhoneNumberIsOptedOutInputRequestTypeDef",
    "CheckIfPhoneNumberIsOptedOutResponseTypeDef",
    "ConfirmSubscriptionInputRequestTypeDef",
    "ConfirmSubscriptionInputTopicConfirmSubscriptionTypeDef",
    "ConfirmSubscriptionResponseTypeDef",
    "CreateEndpointResponseTypeDef",
    "CreatePlatformApplicationInputRequestTypeDef",
    "CreatePlatformApplicationInputServiceResourceCreatePlatformApplicationTypeDef",
    "CreatePlatformApplicationResponseTypeDef",
    "CreatePlatformEndpointInputPlatformApplicationCreatePlatformEndpointTypeDef",
    "CreatePlatformEndpointInputRequestTypeDef",
    "CreateSMSSandboxPhoneNumberInputRequestTypeDef",
    "CreateTopicInputRequestTypeDef",
    "CreateTopicInputServiceResourceCreateTopicTypeDef",
    "CreateTopicResponseTypeDef",
    "DeleteEndpointInputRequestTypeDef",
    "DeletePlatformApplicationInputRequestTypeDef",
    "DeleteSMSSandboxPhoneNumberInputRequestTypeDef",
    "DeleteTopicInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointTypeDef",
    "GetDataProtectionPolicyInputRequestTypeDef",
    "GetDataProtectionPolicyResponseTypeDef",
    "GetEndpointAttributesInputRequestTypeDef",
    "GetEndpointAttributesResponseTypeDef",
    "GetPlatformApplicationAttributesInputRequestTypeDef",
    "GetPlatformApplicationAttributesResponseTypeDef",
    "GetSMSAttributesInputRequestTypeDef",
    "GetSMSAttributesResponseTypeDef",
    "GetSMSSandboxAccountStatusResultTypeDef",
    "GetSubscriptionAttributesInputRequestTypeDef",
    "GetSubscriptionAttributesResponseTypeDef",
    "GetTopicAttributesInputRequestTypeDef",
    "GetTopicAttributesResponseTypeDef",
    "ListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef",
    "ListEndpointsByPlatformApplicationInputRequestTypeDef",
    "ListEndpointsByPlatformApplicationResponseTypeDef",
    "ListOriginationNumbersRequestListOriginationNumbersPaginateTypeDef",
    "ListOriginationNumbersRequestRequestTypeDef",
    "ListOriginationNumbersResultTypeDef",
    "ListPhoneNumbersOptedOutInputListPhoneNumbersOptedOutPaginateTypeDef",
    "ListPhoneNumbersOptedOutInputRequestTypeDef",
    "ListPhoneNumbersOptedOutResponseTypeDef",
    "ListPlatformApplicationsInputListPlatformApplicationsPaginateTypeDef",
    "ListPlatformApplicationsInputRequestTypeDef",
    "ListPlatformApplicationsResponseTypeDef",
    "ListSMSSandboxPhoneNumbersInputListSMSSandboxPhoneNumbersPaginateTypeDef",
    "ListSMSSandboxPhoneNumbersInputRequestTypeDef",
    "ListSMSSandboxPhoneNumbersResultTypeDef",
    "ListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef",
    "ListSubscriptionsByTopicInputRequestTypeDef",
    "ListSubscriptionsByTopicResponseTypeDef",
    "ListSubscriptionsInputListSubscriptionsPaginateTypeDef",
    "ListSubscriptionsInputRequestTypeDef",
    "ListSubscriptionsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTopicsInputListTopicsPaginateTypeDef",
    "ListTopicsInputRequestTypeDef",
    "ListTopicsResponseTypeDef",
    "MessageAttributeValueTypeDef",
    "OptInPhoneNumberInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "PhoneNumberInformationTypeDef",
    "PlatformApplicationTypeDef",
    "PublishBatchInputRequestTypeDef",
    "PublishBatchRequestEntryTypeDef",
    "PublishBatchResponseTypeDef",
    "PublishBatchResultEntryTypeDef",
    "PublishInputPlatformEndpointPublishTypeDef",
    "PublishInputRequestTypeDef",
    "PublishInputTopicPublishTypeDef",
    "PublishResponseTypeDef",
    "PutDataProtectionPolicyInputRequestTypeDef",
    "RemovePermissionInputRequestTypeDef",
    "RemovePermissionInputTopicRemovePermissionTypeDef",
    "ResponseMetadataTypeDef",
    "SMSSandboxPhoneNumberTypeDef",
    "SetEndpointAttributesInputPlatformEndpointSetAttributesTypeDef",
    "SetEndpointAttributesInputRequestTypeDef",
    "SetPlatformApplicationAttributesInputPlatformApplicationSetAttributesTypeDef",
    "SetPlatformApplicationAttributesInputRequestTypeDef",
    "SetSMSAttributesInputRequestTypeDef",
    "SetSubscriptionAttributesInputRequestTypeDef",
    "SetSubscriptionAttributesInputSubscriptionSetAttributesTypeDef",
    "SetTopicAttributesInputRequestTypeDef",
    "SetTopicAttributesInputTopicSetAttributesTypeDef",
    "SubscribeInputRequestTypeDef",
    "SubscribeInputTopicSubscribeTypeDef",
    "SubscribeResponseTypeDef",
    "SubscriptionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TopicTypeDef",
    "UnsubscribeInputRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "VerifySMSSandboxPhoneNumberInputRequestTypeDef",
)

class AddPermissionInputRequestTypeDef(TypedDict):
    TopicArn: str
    Label: str
    AWSAccountId: Sequence[str]
    ActionName: Sequence[str]

class AddPermissionInputTopicAddPermissionTypeDef(TypedDict):
    Label: str
    AWSAccountId: Sequence[str]
    ActionName: Sequence[str]

class BatchResultErrorEntryTypeDef(TypedDict):
    Id: str
    Code: str
    SenderFault: bool
    Message: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class CheckIfPhoneNumberIsOptedOutInputRequestTypeDef(TypedDict):
    phoneNumber: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ConfirmSubscriptionInputRequestTypeDef(TypedDict):
    TopicArn: str
    Token: str
    AuthenticateOnUnsubscribe: NotRequired[str]

class ConfirmSubscriptionInputTopicConfirmSubscriptionTypeDef(TypedDict):
    Token: str
    AuthenticateOnUnsubscribe: NotRequired[str]

class CreatePlatformApplicationInputRequestTypeDef(TypedDict):
    Name: str
    Platform: str
    Attributes: Mapping[str, str]

class CreatePlatformApplicationInputServiceResourceCreatePlatformApplicationTypeDef(TypedDict):
    Name: str
    Platform: str
    Attributes: Mapping[str, str]

class CreatePlatformEndpointInputPlatformApplicationCreatePlatformEndpointTypeDef(TypedDict):
    Token: str
    CustomUserData: NotRequired[str]
    Attributes: NotRequired[Mapping[str, str]]

class CreatePlatformEndpointInputRequestTypeDef(TypedDict):
    PlatformApplicationArn: str
    Token: str
    CustomUserData: NotRequired[str]
    Attributes: NotRequired[Mapping[str, str]]

class CreateSMSSandboxPhoneNumberInputRequestTypeDef(TypedDict):
    PhoneNumber: str
    LanguageCode: NotRequired[LanguageCodeStringType]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class DeleteEndpointInputRequestTypeDef(TypedDict):
    EndpointArn: str

class DeletePlatformApplicationInputRequestTypeDef(TypedDict):
    PlatformApplicationArn: str

class DeleteSMSSandboxPhoneNumberInputRequestTypeDef(TypedDict):
    PhoneNumber: str

class DeleteTopicInputRequestTypeDef(TypedDict):
    TopicArn: str

class EndpointTypeDef(TypedDict):
    EndpointArn: NotRequired[str]
    Attributes: NotRequired[Dict[str, str]]

class GetDataProtectionPolicyInputRequestTypeDef(TypedDict):
    ResourceArn: str

class GetEndpointAttributesInputRequestTypeDef(TypedDict):
    EndpointArn: str

class GetPlatformApplicationAttributesInputRequestTypeDef(TypedDict):
    PlatformApplicationArn: str

class GetSMSAttributesInputRequestTypeDef(TypedDict):
    attributes: NotRequired[Sequence[str]]

class GetSubscriptionAttributesInputRequestTypeDef(TypedDict):
    SubscriptionArn: str

class GetTopicAttributesInputRequestTypeDef(TypedDict):
    TopicArn: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListEndpointsByPlatformApplicationInputRequestTypeDef(TypedDict):
    PlatformApplicationArn: str
    NextToken: NotRequired[str]

class ListOriginationNumbersRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class PhoneNumberInformationTypeDef(TypedDict):
    CreatedAt: NotRequired[datetime]
    PhoneNumber: NotRequired[str]
    Status: NotRequired[str]
    Iso2CountryCode: NotRequired[str]
    RouteType: NotRequired[RouteTypeType]
    NumberCapabilities: NotRequired[List[NumberCapabilityType]]

class ListPhoneNumbersOptedOutInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]

class ListPlatformApplicationsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]

class PlatformApplicationTypeDef(TypedDict):
    PlatformApplicationArn: NotRequired[str]
    Attributes: NotRequired[Dict[str, str]]

class ListSMSSandboxPhoneNumbersInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class SMSSandboxPhoneNumberTypeDef(TypedDict):
    PhoneNumber: NotRequired[str]
    Status: NotRequired[SMSSandboxPhoneNumberVerificationStatusType]

class ListSubscriptionsByTopicInputRequestTypeDef(TypedDict):
    TopicArn: str
    NextToken: NotRequired[str]

SubscriptionTypeDef = TypedDict(
    "SubscriptionTypeDef",
    {
        "SubscriptionArn": NotRequired[str],
        "Owner": NotRequired[str],
        "Protocol": NotRequired[str],
        "Endpoint": NotRequired[str],
        "TopicArn": NotRequired[str],
    },
)

class ListSubscriptionsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class ListTopicsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]

class TopicTypeDef(TypedDict):
    TopicArn: NotRequired[str]

class OptInPhoneNumberInputRequestTypeDef(TypedDict):
    phoneNumber: str

class PublishBatchResultEntryTypeDef(TypedDict):
    Id: NotRequired[str]
    MessageId: NotRequired[str]
    SequenceNumber: NotRequired[str]

class PutDataProtectionPolicyInputRequestTypeDef(TypedDict):
    ResourceArn: str
    DataProtectionPolicy: str

class RemovePermissionInputRequestTypeDef(TypedDict):
    TopicArn: str
    Label: str

class RemovePermissionInputTopicRemovePermissionTypeDef(TypedDict):
    Label: str

class SetEndpointAttributesInputPlatformEndpointSetAttributesTypeDef(TypedDict):
    Attributes: Mapping[str, str]

class SetEndpointAttributesInputRequestTypeDef(TypedDict):
    EndpointArn: str
    Attributes: Mapping[str, str]

class SetPlatformApplicationAttributesInputPlatformApplicationSetAttributesTypeDef(TypedDict):
    Attributes: Mapping[str, str]

class SetPlatformApplicationAttributesInputRequestTypeDef(TypedDict):
    PlatformApplicationArn: str
    Attributes: Mapping[str, str]

class SetSMSAttributesInputRequestTypeDef(TypedDict):
    attributes: Mapping[str, str]

class SetSubscriptionAttributesInputRequestTypeDef(TypedDict):
    SubscriptionArn: str
    AttributeName: str
    AttributeValue: NotRequired[str]

class SetSubscriptionAttributesInputSubscriptionSetAttributesTypeDef(TypedDict):
    AttributeName: str
    AttributeValue: NotRequired[str]

class SetTopicAttributesInputRequestTypeDef(TypedDict):
    TopicArn: str
    AttributeName: str
    AttributeValue: NotRequired[str]

class SetTopicAttributesInputTopicSetAttributesTypeDef(TypedDict):
    AttributeName: str
    AttributeValue: NotRequired[str]

SubscribeInputRequestTypeDef = TypedDict(
    "SubscribeInputRequestTypeDef",
    {
        "TopicArn": str,
        "Protocol": str,
        "Endpoint": NotRequired[str],
        "Attributes": NotRequired[Mapping[str, str]],
        "ReturnSubscriptionArn": NotRequired[bool],
    },
)
SubscribeInputTopicSubscribeTypeDef = TypedDict(
    "SubscribeInputTopicSubscribeTypeDef",
    {
        "Protocol": str,
        "Endpoint": NotRequired[str],
        "Attributes": NotRequired[Mapping[str, str]],
        "ReturnSubscriptionArn": NotRequired[bool],
    },
)

class UnsubscribeInputRequestTypeDef(TypedDict):
    SubscriptionArn: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class VerifySMSSandboxPhoneNumberInputRequestTypeDef(TypedDict):
    PhoneNumber: str
    OneTimePassword: str

class MessageAttributeValueTypeDef(TypedDict):
    DataType: str
    StringValue: NotRequired[str]
    BinaryValue: NotRequired[BlobTypeDef]

class CheckIfPhoneNumberIsOptedOutResponseTypeDef(TypedDict):
    isOptedOut: bool
    ResponseMetadata: ResponseMetadataTypeDef

class ConfirmSubscriptionResponseTypeDef(TypedDict):
    SubscriptionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEndpointResponseTypeDef(TypedDict):
    EndpointArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePlatformApplicationResponseTypeDef(TypedDict):
    PlatformApplicationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTopicResponseTypeDef(TypedDict):
    TopicArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetDataProtectionPolicyResponseTypeDef(TypedDict):
    DataProtectionPolicy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetEndpointAttributesResponseTypeDef(TypedDict):
    Attributes: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetPlatformApplicationAttributesResponseTypeDef(TypedDict):
    Attributes: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetSMSAttributesResponseTypeDef(TypedDict):
    attributes: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetSMSSandboxAccountStatusResultTypeDef(TypedDict):
    IsInSandbox: bool
    ResponseMetadata: ResponseMetadataTypeDef

class GetSubscriptionAttributesResponseTypeDef(TypedDict):
    Attributes: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetTopicAttributesResponseTypeDef(TypedDict):
    Attributes: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListPhoneNumbersOptedOutResponseTypeDef(TypedDict):
    phoneNumbers: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PublishResponseTypeDef(TypedDict):
    MessageId: str
    SequenceNumber: str
    ResponseMetadata: ResponseMetadataTypeDef

class SubscribeResponseTypeDef(TypedDict):
    SubscriptionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTopicInputRequestTypeDef(TypedDict):
    Name: str
    Attributes: NotRequired[Mapping[str, str]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    DataProtectionPolicy: NotRequired[str]

class CreateTopicInputServiceResourceCreateTopicTypeDef(TypedDict):
    Name: str
    Attributes: NotRequired[Mapping[str, str]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    DataProtectionPolicy: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class ListEndpointsByPlatformApplicationResponseTypeDef(TypedDict):
    Endpoints: List[EndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef(
    TypedDict
):
    PlatformApplicationArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOriginationNumbersRequestListOriginationNumbersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPhoneNumbersOptedOutInputListPhoneNumbersOptedOutPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPlatformApplicationsInputListPlatformApplicationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSMSSandboxPhoneNumbersInputListSMSSandboxPhoneNumbersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef(TypedDict):
    TopicArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionsInputListSubscriptionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTopicsInputListTopicsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOriginationNumbersResultTypeDef(TypedDict):
    PhoneNumbers: List[PhoneNumberInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPlatformApplicationsResponseTypeDef(TypedDict):
    PlatformApplications: List[PlatformApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSMSSandboxPhoneNumbersResultTypeDef(TypedDict):
    PhoneNumbers: List[SMSSandboxPhoneNumberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSubscriptionsByTopicResponseTypeDef(TypedDict):
    Subscriptions: List[SubscriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSubscriptionsResponseTypeDef(TypedDict):
    Subscriptions: List[SubscriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTopicsResponseTypeDef(TypedDict):
    Topics: List[TopicTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PublishBatchResponseTypeDef(TypedDict):
    Successful: List[PublishBatchResultEntryTypeDef]
    Failed: List[BatchResultErrorEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PublishBatchRequestEntryTypeDef(TypedDict):
    Id: str
    Message: str
    Subject: NotRequired[str]
    MessageStructure: NotRequired[str]
    MessageAttributes: NotRequired[Mapping[str, MessageAttributeValueTypeDef]]
    MessageDeduplicationId: NotRequired[str]
    MessageGroupId: NotRequired[str]

class PublishInputPlatformEndpointPublishTypeDef(TypedDict):
    Message: str
    TopicArn: NotRequired[str]
    PhoneNumber: NotRequired[str]
    Subject: NotRequired[str]
    MessageStructure: NotRequired[str]
    MessageAttributes: NotRequired[Mapping[str, MessageAttributeValueTypeDef]]
    MessageDeduplicationId: NotRequired[str]
    MessageGroupId: NotRequired[str]

class PublishInputRequestTypeDef(TypedDict):
    Message: str
    TopicArn: NotRequired[str]
    TargetArn: NotRequired[str]
    PhoneNumber: NotRequired[str]
    Subject: NotRequired[str]
    MessageStructure: NotRequired[str]
    MessageAttributes: NotRequired[Mapping[str, MessageAttributeValueTypeDef]]
    MessageDeduplicationId: NotRequired[str]
    MessageGroupId: NotRequired[str]

class PublishInputTopicPublishTypeDef(TypedDict):
    Message: str
    TargetArn: NotRequired[str]
    PhoneNumber: NotRequired[str]
    Subject: NotRequired[str]
    MessageStructure: NotRequired[str]
    MessageAttributes: NotRequired[Mapping[str, MessageAttributeValueTypeDef]]
    MessageDeduplicationId: NotRequired[str]
    MessageGroupId: NotRequired[str]

class PublishBatchInputRequestTypeDef(TypedDict):
    TopicArn: str
    PublishBatchRequestEntries: Sequence[PublishBatchRequestEntryTypeDef]
