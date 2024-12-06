"""
Type annotations for firehose service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_firehose.client import FirehoseClient

    session = Session()
    client: FirehoseClient = session.client("firehose")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateDeliveryStreamInputRequestTypeDef,
    CreateDeliveryStreamOutputTypeDef,
    DeleteDeliveryStreamInputRequestTypeDef,
    DescribeDeliveryStreamInputRequestTypeDef,
    DescribeDeliveryStreamOutputTypeDef,
    ListDeliveryStreamsInputRequestTypeDef,
    ListDeliveryStreamsOutputTypeDef,
    ListTagsForDeliveryStreamInputRequestTypeDef,
    ListTagsForDeliveryStreamOutputTypeDef,
    PutRecordBatchInputRequestTypeDef,
    PutRecordBatchOutputTypeDef,
    PutRecordInputRequestTypeDef,
    PutRecordOutputTypeDef,
    StartDeliveryStreamEncryptionInputRequestTypeDef,
    StopDeliveryStreamEncryptionInputRequestTypeDef,
    TagDeliveryStreamInputRequestTypeDef,
    UntagDeliveryStreamInputRequestTypeDef,
    UpdateDestinationInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("FirehoseClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidKMSResourceException: Type[BotocoreClientError]
    InvalidSourceException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]

class FirehoseClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FirehoseClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#close)
        """

    def create_delivery_stream(
        self, **kwargs: Unpack[CreateDeliveryStreamInputRequestTypeDef]
    ) -> CreateDeliveryStreamOutputTypeDef:
        """
        Creates a Firehose stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/create_delivery_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#create_delivery_stream)
        """

    def delete_delivery_stream(
        self, **kwargs: Unpack[DeleteDeliveryStreamInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Firehose stream and its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/delete_delivery_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#delete_delivery_stream)
        """

    def describe_delivery_stream(
        self, **kwargs: Unpack[DescribeDeliveryStreamInputRequestTypeDef]
    ) -> DescribeDeliveryStreamOutputTypeDef:
        """
        Describes the specified Firehose stream and its status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/describe_delivery_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#describe_delivery_stream)
        """

    def list_delivery_streams(
        self, **kwargs: Unpack[ListDeliveryStreamsInputRequestTypeDef]
    ) -> ListDeliveryStreamsOutputTypeDef:
        """
        Lists your Firehose streams in alphabetical order of their names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/list_delivery_streams.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#list_delivery_streams)
        """

    def list_tags_for_delivery_stream(
        self, **kwargs: Unpack[ListTagsForDeliveryStreamInputRequestTypeDef]
    ) -> ListTagsForDeliveryStreamOutputTypeDef:
        """
        Lists the tags for the specified Firehose stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/list_tags_for_delivery_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#list_tags_for_delivery_stream)
        """

    def put_record(self, **kwargs: Unpack[PutRecordInputRequestTypeDef]) -> PutRecordOutputTypeDef:
        """
        Writes a single data record into an Firehose stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/put_record.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#put_record)
        """

    def put_record_batch(
        self, **kwargs: Unpack[PutRecordBatchInputRequestTypeDef]
    ) -> PutRecordBatchOutputTypeDef:
        """
        Writes multiple data records into a Firehose stream in a single call, which can
        achieve higher throughput per producer than when writing single records.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/put_record_batch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#put_record_batch)
        """

    def start_delivery_stream_encryption(
        self, **kwargs: Unpack[StartDeliveryStreamEncryptionInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enables server-side encryption (SSE) for the Firehose stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/start_delivery_stream_encryption.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#start_delivery_stream_encryption)
        """

    def stop_delivery_stream_encryption(
        self, **kwargs: Unpack[StopDeliveryStreamEncryptionInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disables server-side encryption (SSE) for the Firehose stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/stop_delivery_stream_encryption.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#stop_delivery_stream_encryption)
        """

    def tag_delivery_stream(
        self, **kwargs: Unpack[TagDeliveryStreamInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds or updates tags for the specified Firehose stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/tag_delivery_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#tag_delivery_stream)
        """

    def untag_delivery_stream(
        self, **kwargs: Unpack[UntagDeliveryStreamInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from the specified Firehose stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/untag_delivery_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#untag_delivery_stream)
        """

    def update_destination(
        self, **kwargs: Unpack[UpdateDestinationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the specified destination of the specified Firehose stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose/client/update_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_firehose/client/#update_destination)
        """
