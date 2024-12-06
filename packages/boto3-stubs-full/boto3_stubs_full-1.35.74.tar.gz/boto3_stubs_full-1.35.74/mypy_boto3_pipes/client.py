"""
Type annotations for pipes service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_pipes.client import EventBridgePipesClient

    session = Session()
    client: EventBridgePipesClient = session.client("pipes")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListPipesPaginator
from .type_defs import (
    CreatePipeRequestRequestTypeDef,
    CreatePipeResponseTypeDef,
    DeletePipeRequestRequestTypeDef,
    DeletePipeResponseTypeDef,
    DescribePipeRequestRequestTypeDef,
    DescribePipeResponseTypeDef,
    ListPipesRequestRequestTypeDef,
    ListPipesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartPipeRequestRequestTypeDef,
    StartPipeResponseTypeDef,
    StopPipeRequestRequestTypeDef,
    StopPipeResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdatePipeRequestRequestTypeDef,
    UpdatePipeResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("EventBridgePipesClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class EventBridgePipesClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes.html#EventBridgePipes.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EventBridgePipesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes.html#EventBridgePipes.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#close)
        """

    def create_pipe(
        self, **kwargs: Unpack[CreatePipeRequestRequestTypeDef]
    ) -> CreatePipeResponseTypeDef:
        """
        Create a pipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/create_pipe.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#create_pipe)
        """

    def delete_pipe(
        self, **kwargs: Unpack[DeletePipeRequestRequestTypeDef]
    ) -> DeletePipeResponseTypeDef:
        """
        Delete an existing pipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/delete_pipe.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#delete_pipe)
        """

    def describe_pipe(
        self, **kwargs: Unpack[DescribePipeRequestRequestTypeDef]
    ) -> DescribePipeResponseTypeDef:
        """
        Get the information about an existing pipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/describe_pipe.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#describe_pipe)
        """

    def list_pipes(
        self, **kwargs: Unpack[ListPipesRequestRequestTypeDef]
    ) -> ListPipesResponseTypeDef:
        """
        Get the pipes associated with this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/list_pipes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#list_pipes)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Displays the tags associated with a pipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#list_tags_for_resource)
        """

    def start_pipe(
        self, **kwargs: Unpack[StartPipeRequestRequestTypeDef]
    ) -> StartPipeResponseTypeDef:
        """
        Start an existing pipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/start_pipe.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#start_pipe)
        """

    def stop_pipe(self, **kwargs: Unpack[StopPipeRequestRequestTypeDef]) -> StopPipeResponseTypeDef:
        """
        Stop an existing pipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/stop_pipe.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#stop_pipe)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified pipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified pipes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#untag_resource)
        """

    def update_pipe(
        self, **kwargs: Unpack[UpdatePipeRequestRequestTypeDef]
    ) -> UpdatePipeResponseTypeDef:
        """
        Update an existing pipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/update_pipe.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#update_pipe)
        """

    def get_paginator(self, operation_name: Literal["list_pipes"]) -> ListPipesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/client/#get_paginator)
        """
