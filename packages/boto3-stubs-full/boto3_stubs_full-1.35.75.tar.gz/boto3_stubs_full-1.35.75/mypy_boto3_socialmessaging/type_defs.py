"""
Type annotations for socialmessaging service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/type_defs/)

Usage::

    ```python
    from mypy_boto3_socialmessaging.type_defs import WhatsAppSignupCallbackTypeDef

    data: WhatsAppSignupCallbackTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import RegistrationStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AssociateWhatsAppBusinessAccountInputRequestTypeDef",
    "AssociateWhatsAppBusinessAccountOutputTypeDef",
    "BlobTypeDef",
    "DeleteWhatsAppMessageMediaInputRequestTypeDef",
    "DeleteWhatsAppMessageMediaOutputTypeDef",
    "DisassociateWhatsAppBusinessAccountInputRequestTypeDef",
    "GetLinkedWhatsAppBusinessAccountInputRequestTypeDef",
    "GetLinkedWhatsAppBusinessAccountOutputTypeDef",
    "GetLinkedWhatsAppBusinessAccountPhoneNumberInputRequestTypeDef",
    "GetLinkedWhatsAppBusinessAccountPhoneNumberOutputTypeDef",
    "GetWhatsAppMessageMediaInputRequestTypeDef",
    "GetWhatsAppMessageMediaOutputTypeDef",
    "LinkedWhatsAppBusinessAccountIdMetaDataTypeDef",
    "LinkedWhatsAppBusinessAccountSummaryTypeDef",
    "LinkedWhatsAppBusinessAccountTypeDef",
    "ListLinkedWhatsAppBusinessAccountsInputListLinkedWhatsAppBusinessAccountsPaginateTypeDef",
    "ListLinkedWhatsAppBusinessAccountsInputRequestTypeDef",
    "ListLinkedWhatsAppBusinessAccountsOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PostWhatsAppMessageMediaInputRequestTypeDef",
    "PostWhatsAppMessageMediaOutputTypeDef",
    "PutWhatsAppBusinessAccountEventDestinationsInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "S3FileTypeDef",
    "S3PresignedUrlTypeDef",
    "SendWhatsAppMessageInputRequestTypeDef",
    "SendWhatsAppMessageOutputTypeDef",
    "TagResourceInputRequestTypeDef",
    "TagResourceOutputTypeDef",
    "TagTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UntagResourceOutputTypeDef",
    "WabaPhoneNumberSetupFinalizationTypeDef",
    "WabaSetupFinalizationTypeDef",
    "WhatsAppBusinessAccountEventDestinationTypeDef",
    "WhatsAppPhoneNumberDetailTypeDef",
    "WhatsAppPhoneNumberSummaryTypeDef",
    "WhatsAppSetupFinalizationTypeDef",
    "WhatsAppSignupCallbackResultTypeDef",
    "WhatsAppSignupCallbackTypeDef",
)


class WhatsAppSignupCallbackTypeDef(TypedDict):
    accessToken: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class DeleteWhatsAppMessageMediaInputRequestTypeDef(TypedDict):
    mediaId: str
    originationPhoneNumberId: str


DisassociateWhatsAppBusinessAccountInputRequestTypeDef = TypedDict(
    "DisassociateWhatsAppBusinessAccountInputRequestTypeDef",
    {
        "id": str,
    },
)
GetLinkedWhatsAppBusinessAccountInputRequestTypeDef = TypedDict(
    "GetLinkedWhatsAppBusinessAccountInputRequestTypeDef",
    {
        "id": str,
    },
)
GetLinkedWhatsAppBusinessAccountPhoneNumberInputRequestTypeDef = TypedDict(
    "GetLinkedWhatsAppBusinessAccountPhoneNumberInputRequestTypeDef",
    {
        "id": str,
    },
)


class WhatsAppPhoneNumberDetailTypeDef(TypedDict):
    arn: str
    phoneNumber: str
    phoneNumberId: str
    metaPhoneNumberId: str
    displayPhoneNumberName: str
    displayPhoneNumber: str
    qualityRating: str


class S3FileTypeDef(TypedDict):
    bucketName: str
    key: str


class S3PresignedUrlTypeDef(TypedDict):
    url: str
    headers: Mapping[str, str]


class WhatsAppBusinessAccountEventDestinationTypeDef(TypedDict):
    eventDestinationArn: str
    roleArn: NotRequired[str]


class WhatsAppPhoneNumberSummaryTypeDef(TypedDict):
    arn: str
    phoneNumber: str
    phoneNumberId: str
    metaPhoneNumberId: str
    displayPhoneNumberName: str
    displayPhoneNumber: str
    qualityRating: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListLinkedWhatsAppBusinessAccountsInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str


class TagTypeDef(TypedDict):
    key: str
    value: NotRequired[str]


class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class DeleteWhatsAppMessageMediaOutputTypeDef(TypedDict):
    success: bool
    ResponseMetadata: ResponseMetadataTypeDef


class GetWhatsAppMessageMediaOutputTypeDef(TypedDict):
    mimeType: str
    fileSize: int
    ResponseMetadata: ResponseMetadataTypeDef


class PostWhatsAppMessageMediaOutputTypeDef(TypedDict):
    mediaId: str
    ResponseMetadata: ResponseMetadataTypeDef


class SendWhatsAppMessageOutputTypeDef(TypedDict):
    messageId: str
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceOutputTypeDef(TypedDict):
    statusCode: int
    ResponseMetadata: ResponseMetadataTypeDef


class UntagResourceOutputTypeDef(TypedDict):
    statusCode: int
    ResponseMetadata: ResponseMetadataTypeDef


class SendWhatsAppMessageInputRequestTypeDef(TypedDict):
    originationPhoneNumberId: str
    message: BlobTypeDef
    metaApiVersion: str


class GetLinkedWhatsAppBusinessAccountPhoneNumberOutputTypeDef(TypedDict):
    phoneNumber: WhatsAppPhoneNumberDetailTypeDef
    linkedWhatsAppBusinessAccountId: str
    ResponseMetadata: ResponseMetadataTypeDef


class LinkedWhatsAppBusinessAccountIdMetaDataTypeDef(TypedDict):
    accountName: NotRequired[str]
    registrationStatus: NotRequired[RegistrationStatusType]
    unregisteredWhatsAppPhoneNumbers: NotRequired[List[WhatsAppPhoneNumberDetailTypeDef]]
    wabaId: NotRequired[str]


class GetWhatsAppMessageMediaInputRequestTypeDef(TypedDict):
    mediaId: str
    originationPhoneNumberId: str
    metadataOnly: NotRequired[bool]
    destinationS3PresignedUrl: NotRequired[S3PresignedUrlTypeDef]
    destinationS3File: NotRequired[S3FileTypeDef]


class PostWhatsAppMessageMediaInputRequestTypeDef(TypedDict):
    originationPhoneNumberId: str
    sourceS3PresignedUrl: NotRequired[S3PresignedUrlTypeDef]
    sourceS3File: NotRequired[S3FileTypeDef]


LinkedWhatsAppBusinessAccountSummaryTypeDef = TypedDict(
    "LinkedWhatsAppBusinessAccountSummaryTypeDef",
    {
        "arn": str,
        "id": str,
        "wabaId": str,
        "registrationStatus": RegistrationStatusType,
        "linkDate": datetime,
        "wabaName": str,
        "eventDestinations": List[WhatsAppBusinessAccountEventDestinationTypeDef],
    },
)
PutWhatsAppBusinessAccountEventDestinationsInputRequestTypeDef = TypedDict(
    "PutWhatsAppBusinessAccountEventDestinationsInputRequestTypeDef",
    {
        "id": str,
        "eventDestinations": Sequence[WhatsAppBusinessAccountEventDestinationTypeDef],
    },
)
LinkedWhatsAppBusinessAccountTypeDef = TypedDict(
    "LinkedWhatsAppBusinessAccountTypeDef",
    {
        "arn": str,
        "id": str,
        "wabaId": str,
        "registrationStatus": RegistrationStatusType,
        "linkDate": datetime,
        "wabaName": str,
        "eventDestinations": List[WhatsAppBusinessAccountEventDestinationTypeDef],
        "phoneNumbers": List[WhatsAppPhoneNumberSummaryTypeDef],
    },
)


class ListLinkedWhatsAppBusinessAccountsInputListLinkedWhatsAppBusinessAccountsPaginateTypeDef(
    TypedDict
):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsForResourceOutputTypeDef(TypedDict):
    statusCode: int
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]


WabaPhoneNumberSetupFinalizationTypeDef = TypedDict(
    "WabaPhoneNumberSetupFinalizationTypeDef",
    {
        "id": str,
        "twoFactorPin": str,
        "dataLocalizationRegion": NotRequired[str],
        "tags": NotRequired[Sequence[TagTypeDef]],
    },
)
WabaSetupFinalizationTypeDef = TypedDict(
    "WabaSetupFinalizationTypeDef",
    {
        "id": NotRequired[str],
        "eventDestinations": NotRequired[Sequence[WhatsAppBusinessAccountEventDestinationTypeDef]],
        "tags": NotRequired[Sequence[TagTypeDef]],
    },
)


class WhatsAppSignupCallbackResultTypeDef(TypedDict):
    associateInProgressToken: NotRequired[str]
    linkedAccountsWithIncompleteSetup: NotRequired[
        Dict[str, LinkedWhatsAppBusinessAccountIdMetaDataTypeDef]
    ]


class ListLinkedWhatsAppBusinessAccountsOutputTypeDef(TypedDict):
    linkedAccounts: List[LinkedWhatsAppBusinessAccountSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetLinkedWhatsAppBusinessAccountOutputTypeDef(TypedDict):
    account: LinkedWhatsAppBusinessAccountTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class WhatsAppSetupFinalizationTypeDef(TypedDict):
    associateInProgressToken: str
    phoneNumbers: Sequence[WabaPhoneNumberSetupFinalizationTypeDef]
    phoneNumberParent: NotRequired[str]
    waba: NotRequired[WabaSetupFinalizationTypeDef]


class AssociateWhatsAppBusinessAccountOutputTypeDef(TypedDict):
    signupCallbackResult: WhatsAppSignupCallbackResultTypeDef
    statusCode: int
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateWhatsAppBusinessAccountInputRequestTypeDef(TypedDict):
    signupCallback: NotRequired[WhatsAppSignupCallbackTypeDef]
    setupFinalization: NotRequired[WhatsAppSetupFinalizationTypeDef]
