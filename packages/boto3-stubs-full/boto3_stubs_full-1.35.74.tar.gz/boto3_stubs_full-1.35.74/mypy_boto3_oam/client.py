"""
Type annotations for oam service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_oam.client import CloudWatchObservabilityAccessManagerClient

    session = Session()
    client: CloudWatchObservabilityAccessManagerClient = session.client("oam")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListAttachedLinksPaginator, ListLinksPaginator, ListSinksPaginator
from .type_defs import (
    CreateLinkInputRequestTypeDef,
    CreateLinkOutputTypeDef,
    CreateSinkInputRequestTypeDef,
    CreateSinkOutputTypeDef,
    DeleteLinkInputRequestTypeDef,
    DeleteSinkInputRequestTypeDef,
    GetLinkInputRequestTypeDef,
    GetLinkOutputTypeDef,
    GetSinkInputRequestTypeDef,
    GetSinkOutputTypeDef,
    GetSinkPolicyInputRequestTypeDef,
    GetSinkPolicyOutputTypeDef,
    ListAttachedLinksInputRequestTypeDef,
    ListAttachedLinksOutputTypeDef,
    ListLinksInputRequestTypeDef,
    ListLinksOutputTypeDef,
    ListSinksInputRequestTypeDef,
    ListSinksOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    PutSinkPolicyInputRequestTypeDef,
    PutSinkPolicyOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateLinkInputRequestTypeDef,
    UpdateLinkOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CloudWatchObservabilityAccessManagerClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServiceFault: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    MissingRequiredParameterException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CloudWatchObservabilityAccessManagerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam.html#CloudWatchObservabilityAccessManager.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchObservabilityAccessManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam.html#CloudWatchObservabilityAccessManager.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#close)
        """

    def create_link(
        self, **kwargs: Unpack[CreateLinkInputRequestTypeDef]
    ) -> CreateLinkOutputTypeDef:
        """
        Creates a link between a source account and a sink that you have created in a
        monitoring account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/create_link.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#create_link)
        """

    def create_sink(
        self, **kwargs: Unpack[CreateSinkInputRequestTypeDef]
    ) -> CreateSinkOutputTypeDef:
        """
        Use this to create a <i>sink</i> in the current account, so that it can be used
        as a monitoring account in CloudWatch cross-account observability.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/create_sink.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#create_sink)
        """

    def delete_link(self, **kwargs: Unpack[DeleteLinkInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a link between a monitoring account sink and a source account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/delete_link.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#delete_link)
        """

    def delete_sink(self, **kwargs: Unpack[DeleteSinkInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a sink.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/delete_sink.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#delete_sink)
        """

    def get_link(self, **kwargs: Unpack[GetLinkInputRequestTypeDef]) -> GetLinkOutputTypeDef:
        """
        Returns complete information about one link.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/get_link.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#get_link)
        """

    def get_sink(self, **kwargs: Unpack[GetSinkInputRequestTypeDef]) -> GetSinkOutputTypeDef:
        """
        Returns complete information about one monitoring account sink.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/get_sink.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#get_sink)
        """

    def get_sink_policy(
        self, **kwargs: Unpack[GetSinkPolicyInputRequestTypeDef]
    ) -> GetSinkPolicyOutputTypeDef:
        """
        Returns the current sink policy attached to this sink.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/get_sink_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#get_sink_policy)
        """

    def list_attached_links(
        self, **kwargs: Unpack[ListAttachedLinksInputRequestTypeDef]
    ) -> ListAttachedLinksOutputTypeDef:
        """
        Returns a list of source account links that are linked to this monitoring
        account sink.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/list_attached_links.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#list_attached_links)
        """

    def list_links(self, **kwargs: Unpack[ListLinksInputRequestTypeDef]) -> ListLinksOutputTypeDef:
        """
        Use this operation in a source account to return a list of links to monitoring
        account sinks that this source account has.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/list_links.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#list_links)
        """

    def list_sinks(self, **kwargs: Unpack[ListSinksInputRequestTypeDef]) -> ListSinksOutputTypeDef:
        """
        Use this operation in a monitoring account to return the list of sinks created
        in that account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/list_sinks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#list_sinks)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Displays the tags associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#list_tags_for_resource)
        """

    def put_sink_policy(
        self, **kwargs: Unpack[PutSinkPolicyInputRequestTypeDef]
    ) -> PutSinkPolicyOutputTypeDef:
        """
        Creates or updates the resource policy that grants permissions to source
        accounts to link to the monitoring account sink.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/put_sink_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#put_sink_policy)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#untag_resource)
        """

    def update_link(
        self, **kwargs: Unpack[UpdateLinkInputRequestTypeDef]
    ) -> UpdateLinkOutputTypeDef:
        """
        Use this operation to change what types of data are shared from a source
        account to its linked monitoring account sink.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/update_link.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#update_link)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_attached_links"]
    ) -> ListAttachedLinksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_links"]) -> ListLinksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_sinks"]) -> ListSinksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/client/#get_paginator)
        """
