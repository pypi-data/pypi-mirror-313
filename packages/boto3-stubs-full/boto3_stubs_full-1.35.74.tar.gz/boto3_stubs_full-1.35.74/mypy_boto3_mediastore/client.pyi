"""
Type annotations for mediastore service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_mediastore.client import MediaStoreClient

    session = Session()
    client: MediaStoreClient = session.client("mediastore")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListContainersPaginator
from .type_defs import (
    CreateContainerInputRequestTypeDef,
    CreateContainerOutputTypeDef,
    DeleteContainerInputRequestTypeDef,
    DeleteContainerPolicyInputRequestTypeDef,
    DeleteCorsPolicyInputRequestTypeDef,
    DeleteLifecyclePolicyInputRequestTypeDef,
    DeleteMetricPolicyInputRequestTypeDef,
    DescribeContainerInputRequestTypeDef,
    DescribeContainerOutputTypeDef,
    GetContainerPolicyInputRequestTypeDef,
    GetContainerPolicyOutputTypeDef,
    GetCorsPolicyInputRequestTypeDef,
    GetCorsPolicyOutputTypeDef,
    GetLifecyclePolicyInputRequestTypeDef,
    GetLifecyclePolicyOutputTypeDef,
    GetMetricPolicyInputRequestTypeDef,
    GetMetricPolicyOutputTypeDef,
    ListContainersInputRequestTypeDef,
    ListContainersOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    PutContainerPolicyInputRequestTypeDef,
    PutCorsPolicyInputRequestTypeDef,
    PutLifecyclePolicyInputRequestTypeDef,
    PutMetricPolicyInputRequestTypeDef,
    StartAccessLoggingInputRequestTypeDef,
    StopAccessLoggingInputRequestTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("MediaStoreClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ContainerInUseException: Type[BotocoreClientError]
    ContainerNotFoundException: Type[BotocoreClientError]
    CorsPolicyNotFoundException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    PolicyNotFoundException: Type[BotocoreClientError]

class MediaStoreClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaStoreClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#close)
        """

    def create_container(
        self, **kwargs: Unpack[CreateContainerInputRequestTypeDef]
    ) -> CreateContainerOutputTypeDef:
        """
        Creates a storage container to hold objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/create_container.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#create_container)
        """

    def delete_container(
        self, **kwargs: Unpack[DeleteContainerInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/delete_container.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#delete_container)
        """

    def delete_container_policy(
        self, **kwargs: Unpack[DeleteContainerPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the access policy that is associated with the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/delete_container_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#delete_container_policy)
        """

    def delete_cors_policy(
        self, **kwargs: Unpack[DeleteCorsPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the cross-origin resource sharing (CORS) configuration information that
        is set for the container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/delete_cors_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#delete_cors_policy)
        """

    def delete_lifecycle_policy(
        self, **kwargs: Unpack[DeleteLifecyclePolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes an object lifecycle policy from a container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/delete_lifecycle_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#delete_lifecycle_policy)
        """

    def delete_metric_policy(
        self, **kwargs: Unpack[DeleteMetricPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the metric policy that is associated with the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/delete_metric_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#delete_metric_policy)
        """

    def describe_container(
        self, **kwargs: Unpack[DescribeContainerInputRequestTypeDef]
    ) -> DescribeContainerOutputTypeDef:
        """
        Retrieves the properties of the requested container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/describe_container.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#describe_container)
        """

    def get_container_policy(
        self, **kwargs: Unpack[GetContainerPolicyInputRequestTypeDef]
    ) -> GetContainerPolicyOutputTypeDef:
        """
        Retrieves the access policy for the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/get_container_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#get_container_policy)
        """

    def get_cors_policy(
        self, **kwargs: Unpack[GetCorsPolicyInputRequestTypeDef]
    ) -> GetCorsPolicyOutputTypeDef:
        """
        Returns the cross-origin resource sharing (CORS) configuration information that
        is set for the container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/get_cors_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#get_cors_policy)
        """

    def get_lifecycle_policy(
        self, **kwargs: Unpack[GetLifecyclePolicyInputRequestTypeDef]
    ) -> GetLifecyclePolicyOutputTypeDef:
        """
        Retrieves the object lifecycle policy that is assigned to a container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/get_lifecycle_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#get_lifecycle_policy)
        """

    def get_metric_policy(
        self, **kwargs: Unpack[GetMetricPolicyInputRequestTypeDef]
    ) -> GetMetricPolicyOutputTypeDef:
        """
        Returns the metric policy for the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/get_metric_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#get_metric_policy)
        """

    def list_containers(
        self, **kwargs: Unpack[ListContainersInputRequestTypeDef]
    ) -> ListContainersOutputTypeDef:
        """
        Lists the properties of all containers in AWS Elemental MediaStore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/list_containers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#list_containers)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Returns a list of the tags assigned to the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#list_tags_for_resource)
        """

    def put_container_policy(
        self, **kwargs: Unpack[PutContainerPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates an access policy for the specified container to restrict the users and
        clients that can access it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/put_container_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#put_container_policy)
        """

    def put_cors_policy(self, **kwargs: Unpack[PutCorsPolicyInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Sets the cross-origin resource sharing (CORS) configuration on a container so
        that the container can service cross-origin requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/put_cors_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#put_cors_policy)
        """

    def put_lifecycle_policy(
        self, **kwargs: Unpack[PutLifecyclePolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Writes an object lifecycle policy to a container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/put_lifecycle_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#put_lifecycle_policy)
        """

    def put_metric_policy(
        self, **kwargs: Unpack[PutMetricPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The metric policy that you want to add to the container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/put_metric_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#put_metric_policy)
        """

    def start_access_logging(
        self, **kwargs: Unpack[StartAccessLoggingInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts access logging on the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/start_access_logging.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#start_access_logging)
        """

    def stop_access_logging(
        self, **kwargs: Unpack[StopAccessLoggingInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops access logging on the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/stop_access_logging.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#stop_access_logging)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to the specified AWS Elemental MediaStore container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes tags from the specified container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#untag_resource)
        """

    def get_paginator(self, operation_name: Literal["list_containers"]) -> ListContainersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediastore/client/#get_paginator)
        """
