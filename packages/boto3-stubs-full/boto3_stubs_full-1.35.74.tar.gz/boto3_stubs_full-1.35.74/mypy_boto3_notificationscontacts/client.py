"""
Type annotations for notificationscontacts service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_notificationscontacts.client import UserNotificationsContactsClient

    session = Session()
    client: UserNotificationsContactsClient = session.client("notificationscontacts")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListEmailContactsPaginator
from .type_defs import (
    ActivateEmailContactRequestRequestTypeDef,
    CreateEmailContactRequestRequestTypeDef,
    CreateEmailContactResponseTypeDef,
    DeleteEmailContactRequestRequestTypeDef,
    GetEmailContactRequestRequestTypeDef,
    GetEmailContactResponseTypeDef,
    ListEmailContactsRequestRequestTypeDef,
    ListEmailContactsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    SendActivationCodeRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("UserNotificationsContactsClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class UserNotificationsContactsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts.html#UserNotificationsContacts.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        UserNotificationsContactsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts.html#UserNotificationsContacts.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#close)
        """

    def activate_email_contact(
        self, **kwargs: Unpack[ActivateEmailContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Activates an email contact using an activation code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/client/activate_email_contact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#activate_email_contact)
        """

    def create_email_contact(
        self, **kwargs: Unpack[CreateEmailContactRequestRequestTypeDef]
    ) -> CreateEmailContactResponseTypeDef:
        """
        Creates an email contact for the provided email address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/client/create_email_contact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#create_email_contact)
        """

    def delete_email_contact(
        self, **kwargs: Unpack[DeleteEmailContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an email contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/client/delete_email_contact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#delete_email_contact)
        """

    def get_email_contact(
        self, **kwargs: Unpack[GetEmailContactRequestRequestTypeDef]
    ) -> GetEmailContactResponseTypeDef:
        """
        Returns an email contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/client/get_email_contact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#get_email_contact)
        """

    def list_email_contacts(
        self, **kwargs: Unpack[ListEmailContactsRequestRequestTypeDef]
    ) -> ListEmailContactsResponseTypeDef:
        """
        Lists all email contacts created under the Account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/client/list_email_contacts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#list_email_contacts)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all of the tags associated with the Amazon Resource Name (ARN) that you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#list_tags_for_resource)
        """

    def send_activation_code(
        self, **kwargs: Unpack[SendActivationCodeRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sends an activation email to the email address associated with the specified
        email contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/client/send_activation_code.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#send_activation_code)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Attaches a key-value pair to a resource, as identified by its Amazon Resource
        Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Detaches a key-value pair from a resource, as identified by its Amazon Resource
        Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#untag_resource)
        """

    def get_paginator(
        self, operation_name: Literal["list_email_contacts"]
    ) -> ListEmailContactsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_notificationscontacts/client/#get_paginator)
        """
