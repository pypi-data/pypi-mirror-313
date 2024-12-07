"""
Main interface for kinesis-video-webrtc-storage service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesis_video_webrtc_storage import (
        Client,
        KinesisVideoWebRTCStorageClient,
    )

    session = Session()
    client: KinesisVideoWebRTCStorageClient = session.client("kinesis-video-webrtc-storage")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import KinesisVideoWebRTCStorageClient

Client = KinesisVideoWebRTCStorageClient

__all__ = ("Client", "KinesisVideoWebRTCStorageClient")
