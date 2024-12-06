"""
Type annotations for socialmessaging service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_socialmessaging.client import EndUserMessagingSocialClient

    session = Session()
    client: EndUserMessagingSocialClient = session.client("socialmessaging")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListLinkedWhatsAppBusinessAccountsPaginator
from .type_defs import (
    AssociateWhatsAppBusinessAccountInputRequestTypeDef,
    AssociateWhatsAppBusinessAccountOutputTypeDef,
    DeleteWhatsAppMessageMediaInputRequestTypeDef,
    DeleteWhatsAppMessageMediaOutputTypeDef,
    DisassociateWhatsAppBusinessAccountInputRequestTypeDef,
    GetLinkedWhatsAppBusinessAccountInputRequestTypeDef,
    GetLinkedWhatsAppBusinessAccountOutputTypeDef,
    GetLinkedWhatsAppBusinessAccountPhoneNumberInputRequestTypeDef,
    GetLinkedWhatsAppBusinessAccountPhoneNumberOutputTypeDef,
    GetWhatsAppMessageMediaInputRequestTypeDef,
    GetWhatsAppMessageMediaOutputTypeDef,
    ListLinkedWhatsAppBusinessAccountsInputRequestTypeDef,
    ListLinkedWhatsAppBusinessAccountsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    PostWhatsAppMessageMediaInputRequestTypeDef,
    PostWhatsAppMessageMediaOutputTypeDef,
    PutWhatsAppBusinessAccountEventDestinationsInputRequestTypeDef,
    SendWhatsAppMessageInputRequestTypeDef,
    SendWhatsAppMessageOutputTypeDef,
    TagResourceInputRequestTypeDef,
    TagResourceOutputTypeDef,
    UntagResourceInputRequestTypeDef,
    UntagResourceOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("EndUserMessagingSocialClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedByMetaException: Type[BotocoreClientError]
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DependencyException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidParametersException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottledRequestException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class EndUserMessagingSocialClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging.html#EndUserMessagingSocial.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EndUserMessagingSocialClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging.html#EndUserMessagingSocial.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#close)
        """

    def associate_whatsapp_business_account(
        self, **kwargs: Unpack[AssociateWhatsAppBusinessAccountInputRequestTypeDef]
    ) -> AssociateWhatsAppBusinessAccountOutputTypeDef:
        """
        This is only used through the Amazon Web Services console during sign-up to
        associate your WhatsApp Business Account to your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/associate_whatsapp_business_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#associate_whatsapp_business_account)
        """

    def delete_whatsapp_media_message(
        self, **kwargs: Unpack[DeleteWhatsAppMessageMediaInputRequestTypeDef]
    ) -> DeleteWhatsAppMessageMediaOutputTypeDef:
        """
        Delete a media object from the WhatsApp service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/delete_whatsapp_media_message.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#delete_whatsapp_media_message)
        """

    def disassociate_whatsapp_business_account(
        self, **kwargs: Unpack[DisassociateWhatsAppBusinessAccountInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociate a WhatsApp Business Account (WABA) from your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/disassociate_whatsapp_business_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#disassociate_whatsapp_business_account)
        """

    def get_linked_whatsapp_business_account(
        self, **kwargs: Unpack[GetLinkedWhatsAppBusinessAccountInputRequestTypeDef]
    ) -> GetLinkedWhatsAppBusinessAccountOutputTypeDef:
        """
        Get the details of your linked WhatsApp Business Account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_linked_whatsapp_business_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#get_linked_whatsapp_business_account)
        """

    def get_linked_whatsapp_business_account_phone_number(
        self, **kwargs: Unpack[GetLinkedWhatsAppBusinessAccountPhoneNumberInputRequestTypeDef]
    ) -> GetLinkedWhatsAppBusinessAccountPhoneNumberOutputTypeDef:
        """
        Use your WhatsApp phone number id to get the WABA account id and phone number
        details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_linked_whatsapp_business_account_phone_number.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#get_linked_whatsapp_business_account_phone_number)
        """

    def get_whatsapp_message_media(
        self, **kwargs: Unpack[GetWhatsAppMessageMediaInputRequestTypeDef]
    ) -> GetWhatsAppMessageMediaOutputTypeDef:
        """
        Get a media file from the WhatsApp service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_whatsapp_message_media.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#get_whatsapp_message_media)
        """

    def list_linked_whatsapp_business_accounts(
        self, **kwargs: Unpack[ListLinkedWhatsAppBusinessAccountsInputRequestTypeDef]
    ) -> ListLinkedWhatsAppBusinessAccountsOutputTypeDef:
        """
        List all WhatsApp Business Accounts linked to your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/list_linked_whatsapp_business_accounts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#list_linked_whatsapp_business_accounts)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        List all tags associated with a resource, such as a phone number or WABA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#list_tags_for_resource)
        """

    def post_whatsapp_message_media(
        self, **kwargs: Unpack[PostWhatsAppMessageMediaInputRequestTypeDef]
    ) -> PostWhatsAppMessageMediaOutputTypeDef:
        """
        Upload a media file to the WhatsApp service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/post_whatsapp_message_media.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#post_whatsapp_message_media)
        """

    def put_whatsapp_business_account_event_destinations(
        self, **kwargs: Unpack[PutWhatsAppBusinessAccountEventDestinationsInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Add an event destination to log event data from WhatsApp for a WhatsApp
        Business Account (WABA).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/put_whatsapp_business_account_event_destinations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#put_whatsapp_business_account_event_destinations)
        """

    def send_whatsapp_message(
        self, **kwargs: Unpack[SendWhatsAppMessageInputRequestTypeDef]
    ) -> SendWhatsAppMessageOutputTypeDef:
        """
        Send a WhatsApp message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/send_whatsapp_message.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#send_whatsapp_message)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> TagResourceOutputTypeDef:
        """
        Adds or overwrites only the specified tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> UntagResourceOutputTypeDef:
        """
        Removes the specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#untag_resource)
        """

    def get_paginator(
        self, operation_name: Literal["list_linked_whatsapp_business_accounts"]
    ) -> ListLinkedWhatsAppBusinessAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/client/#get_paginator)
        """
