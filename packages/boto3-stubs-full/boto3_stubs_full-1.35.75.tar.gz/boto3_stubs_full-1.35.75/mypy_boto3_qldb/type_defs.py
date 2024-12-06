"""
Type annotations for qldb service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qldb/type_defs/)

Usage::

    ```python
    from mypy_boto3_qldb.type_defs import CancelJournalKinesisStreamRequestRequestTypeDef

    data: CancelJournalKinesisStreamRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    EncryptionStatusType,
    ErrorCauseType,
    ExportStatusType,
    LedgerStateType,
    OutputFormatType,
    PermissionsModeType,
    S3ObjectEncryptionTypeType,
    StreamStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "CancelJournalKinesisStreamRequestRequestTypeDef",
    "CancelJournalKinesisStreamResponseTypeDef",
    "CreateLedgerRequestRequestTypeDef",
    "CreateLedgerResponseTypeDef",
    "DeleteLedgerRequestRequestTypeDef",
    "DescribeJournalKinesisStreamRequestRequestTypeDef",
    "DescribeJournalKinesisStreamResponseTypeDef",
    "DescribeJournalS3ExportRequestRequestTypeDef",
    "DescribeJournalS3ExportResponseTypeDef",
    "DescribeLedgerRequestRequestTypeDef",
    "DescribeLedgerResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportJournalToS3RequestRequestTypeDef",
    "ExportJournalToS3ResponseTypeDef",
    "GetBlockRequestRequestTypeDef",
    "GetBlockResponseTypeDef",
    "GetDigestRequestRequestTypeDef",
    "GetDigestResponseTypeDef",
    "GetRevisionRequestRequestTypeDef",
    "GetRevisionResponseTypeDef",
    "JournalKinesisStreamDescriptionTypeDef",
    "JournalS3ExportDescriptionTypeDef",
    "KinesisConfigurationTypeDef",
    "LedgerEncryptionDescriptionTypeDef",
    "LedgerSummaryTypeDef",
    "ListJournalKinesisStreamsForLedgerRequestRequestTypeDef",
    "ListJournalKinesisStreamsForLedgerResponseTypeDef",
    "ListJournalS3ExportsForLedgerRequestRequestTypeDef",
    "ListJournalS3ExportsForLedgerResponseTypeDef",
    "ListJournalS3ExportsRequestRequestTypeDef",
    "ListJournalS3ExportsResponseTypeDef",
    "ListLedgersRequestRequestTypeDef",
    "ListLedgersResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ResponseMetadataTypeDef",
    "S3EncryptionConfigurationTypeDef",
    "S3ExportConfigurationTypeDef",
    "StreamJournalToKinesisRequestRequestTypeDef",
    "StreamJournalToKinesisResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateLedgerPermissionsModeRequestRequestTypeDef",
    "UpdateLedgerPermissionsModeResponseTypeDef",
    "UpdateLedgerRequestRequestTypeDef",
    "UpdateLedgerResponseTypeDef",
    "ValueHolderTypeDef",
)


class CancelJournalKinesisStreamRequestRequestTypeDef(TypedDict):
    LedgerName: str
    StreamId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateLedgerRequestRequestTypeDef(TypedDict):
    Name: str
    PermissionsMode: PermissionsModeType
    Tags: NotRequired[Mapping[str, str]]
    DeletionProtection: NotRequired[bool]
    KmsKey: NotRequired[str]


class DeleteLedgerRequestRequestTypeDef(TypedDict):
    Name: str


class DescribeJournalKinesisStreamRequestRequestTypeDef(TypedDict):
    LedgerName: str
    StreamId: str


class DescribeJournalS3ExportRequestRequestTypeDef(TypedDict):
    Name: str
    ExportId: str


class DescribeLedgerRequestRequestTypeDef(TypedDict):
    Name: str


class LedgerEncryptionDescriptionTypeDef(TypedDict):
    KmsKeyArn: str
    EncryptionStatus: EncryptionStatusType
    InaccessibleKmsKeyDateTime: NotRequired[datetime]


TimestampTypeDef = Union[datetime, str]


class ValueHolderTypeDef(TypedDict):
    IonText: NotRequired[str]


class GetDigestRequestRequestTypeDef(TypedDict):
    Name: str


class KinesisConfigurationTypeDef(TypedDict):
    StreamArn: str
    AggregationEnabled: NotRequired[bool]


class LedgerSummaryTypeDef(TypedDict):
    Name: NotRequired[str]
    State: NotRequired[LedgerStateType]
    CreationDateTime: NotRequired[datetime]


class ListJournalKinesisStreamsForLedgerRequestRequestTypeDef(TypedDict):
    LedgerName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListJournalS3ExportsForLedgerRequestRequestTypeDef(TypedDict):
    Name: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListJournalS3ExportsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListLedgersRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class S3EncryptionConfigurationTypeDef(TypedDict):
    ObjectEncryptionType: S3ObjectEncryptionTypeType
    KmsKeyArn: NotRequired[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateLedgerPermissionsModeRequestRequestTypeDef(TypedDict):
    Name: str
    PermissionsMode: PermissionsModeType


class UpdateLedgerRequestRequestTypeDef(TypedDict):
    Name: str
    DeletionProtection: NotRequired[bool]
    KmsKey: NotRequired[str]


class CancelJournalKinesisStreamResponseTypeDef(TypedDict):
    StreamId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLedgerResponseTypeDef(TypedDict):
    Name: str
    Arn: str
    State: LedgerStateType
    CreationDateTime: datetime
    PermissionsMode: PermissionsModeType
    DeletionProtection: bool
    KmsKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ExportJournalToS3ResponseTypeDef(TypedDict):
    ExportId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StreamJournalToKinesisResponseTypeDef(TypedDict):
    StreamId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateLedgerPermissionsModeResponseTypeDef(TypedDict):
    Name: str
    Arn: str
    PermissionsMode: PermissionsModeType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLedgerResponseTypeDef(TypedDict):
    Name: str
    Arn: str
    State: LedgerStateType
    CreationDateTime: datetime
    PermissionsMode: PermissionsModeType
    DeletionProtection: bool
    EncryptionDescription: LedgerEncryptionDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateLedgerResponseTypeDef(TypedDict):
    Name: str
    Arn: str
    State: LedgerStateType
    CreationDateTime: datetime
    DeletionProtection: bool
    EncryptionDescription: LedgerEncryptionDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetBlockRequestRequestTypeDef(TypedDict):
    Name: str
    BlockAddress: ValueHolderTypeDef
    DigestTipAddress: NotRequired[ValueHolderTypeDef]


class GetBlockResponseTypeDef(TypedDict):
    Block: ValueHolderTypeDef
    Proof: ValueHolderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDigestResponseTypeDef(TypedDict):
    Digest: bytes
    DigestTipAddress: ValueHolderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetRevisionRequestRequestTypeDef(TypedDict):
    Name: str
    BlockAddress: ValueHolderTypeDef
    DocumentId: str
    DigestTipAddress: NotRequired[ValueHolderTypeDef]


class GetRevisionResponseTypeDef(TypedDict):
    Proof: ValueHolderTypeDef
    Revision: ValueHolderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class JournalKinesisStreamDescriptionTypeDef(TypedDict):
    LedgerName: str
    RoleArn: str
    StreamId: str
    Status: StreamStatusType
    KinesisConfiguration: KinesisConfigurationTypeDef
    StreamName: str
    CreationTime: NotRequired[datetime]
    InclusiveStartTime: NotRequired[datetime]
    ExclusiveEndTime: NotRequired[datetime]
    Arn: NotRequired[str]
    ErrorCause: NotRequired[ErrorCauseType]


class StreamJournalToKinesisRequestRequestTypeDef(TypedDict):
    LedgerName: str
    RoleArn: str
    InclusiveStartTime: TimestampTypeDef
    KinesisConfiguration: KinesisConfigurationTypeDef
    StreamName: str
    Tags: NotRequired[Mapping[str, str]]
    ExclusiveEndTime: NotRequired[TimestampTypeDef]


class ListLedgersResponseTypeDef(TypedDict):
    Ledgers: List[LedgerSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class S3ExportConfigurationTypeDef(TypedDict):
    Bucket: str
    Prefix: str
    EncryptionConfiguration: S3EncryptionConfigurationTypeDef


class DescribeJournalKinesisStreamResponseTypeDef(TypedDict):
    Stream: JournalKinesisStreamDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListJournalKinesisStreamsForLedgerResponseTypeDef(TypedDict):
    Streams: List[JournalKinesisStreamDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ExportJournalToS3RequestRequestTypeDef(TypedDict):
    Name: str
    InclusiveStartTime: TimestampTypeDef
    ExclusiveEndTime: TimestampTypeDef
    S3ExportConfiguration: S3ExportConfigurationTypeDef
    RoleArn: str
    OutputFormat: NotRequired[OutputFormatType]


class JournalS3ExportDescriptionTypeDef(TypedDict):
    LedgerName: str
    ExportId: str
    ExportCreationTime: datetime
    Status: ExportStatusType
    InclusiveStartTime: datetime
    ExclusiveEndTime: datetime
    S3ExportConfiguration: S3ExportConfigurationTypeDef
    RoleArn: str
    OutputFormat: NotRequired[OutputFormatType]


class DescribeJournalS3ExportResponseTypeDef(TypedDict):
    ExportDescription: JournalS3ExportDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListJournalS3ExportsForLedgerResponseTypeDef(TypedDict):
    JournalS3Exports: List[JournalS3ExportDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListJournalS3ExportsResponseTypeDef(TypedDict):
    JournalS3Exports: List[JournalS3ExportDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
