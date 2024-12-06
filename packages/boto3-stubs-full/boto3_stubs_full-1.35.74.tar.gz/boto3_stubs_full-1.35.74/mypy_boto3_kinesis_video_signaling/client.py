"""
Type annotations for kinesis-video-signaling service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_signaling/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesis_video_signaling.client import KinesisVideoSignalingChannelsClient

    session = Session()
    client: KinesisVideoSignalingChannelsClient = session.client("kinesis-video-signaling")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    GetIceServerConfigRequestRequestTypeDef,
    GetIceServerConfigResponseTypeDef,
    SendAlexaOfferToMasterRequestRequestTypeDef,
    SendAlexaOfferToMasterResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("KinesisVideoSignalingChannelsClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ClientLimitExceededException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidClientException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    SessionExpiredException: Type[BotocoreClientError]


class KinesisVideoSignalingChannelsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling.html#KinesisVideoSignalingChannels.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_signaling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisVideoSignalingChannelsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling.html#KinesisVideoSignalingChannels.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_signaling/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_signaling/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_signaling/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_signaling/client/#close)
        """

    def get_ice_server_config(
        self, **kwargs: Unpack[GetIceServerConfigRequestRequestTypeDef]
    ) -> GetIceServerConfigResponseTypeDef:
        """
        Gets the Interactive Connectivity Establishment (ICE) server configuration
        information, including URIs, username, and password which can be used to
        configure the WebRTC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling/client/get_ice_server_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_signaling/client/#get_ice_server_config)
        """

    def send_alexa_offer_to_master(
        self, **kwargs: Unpack[SendAlexaOfferToMasterRequestRequestTypeDef]
    ) -> SendAlexaOfferToMasterResponseTypeDef:
        """
        This API allows you to connect WebRTC-enabled devices with Alexa display
        devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling/client/send_alexa_offer_to_master.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_signaling/client/#send_alexa_offer_to_master)
        """
