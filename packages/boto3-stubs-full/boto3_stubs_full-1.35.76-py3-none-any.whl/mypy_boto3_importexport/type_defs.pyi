"""
Type annotations for importexport service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_importexport/type_defs/)

Usage::

    ```python
    from mypy_boto3_importexport.type_defs import ArtifactTypeDef

    data: ArtifactTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import JobTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ArtifactTypeDef",
    "CancelJobInputRequestTypeDef",
    "CancelJobOutputTypeDef",
    "CreateJobInputRequestTypeDef",
    "CreateJobOutputTypeDef",
    "GetShippingLabelInputRequestTypeDef",
    "GetShippingLabelOutputTypeDef",
    "GetStatusInputRequestTypeDef",
    "GetStatusOutputTypeDef",
    "JobTypeDef",
    "ListJobsInputListJobsPaginateTypeDef",
    "ListJobsInputRequestTypeDef",
    "ListJobsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "UpdateJobInputRequestTypeDef",
    "UpdateJobOutputTypeDef",
)

class ArtifactTypeDef(TypedDict):
    Description: NotRequired[str]
    URL: NotRequired[str]

class CancelJobInputRequestTypeDef(TypedDict):
    JobId: str
    APIVersion: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateJobInputRequestTypeDef(TypedDict):
    JobType: JobTypeType
    Manifest: str
    ValidateOnly: bool
    ManifestAddendum: NotRequired[str]
    APIVersion: NotRequired[str]

class GetShippingLabelInputRequestTypeDef(TypedDict):
    jobIds: Sequence[str]
    name: NotRequired[str]
    company: NotRequired[str]
    phoneNumber: NotRequired[str]
    country: NotRequired[str]
    stateOrProvince: NotRequired[str]
    city: NotRequired[str]
    postalCode: NotRequired[str]
    street1: NotRequired[str]
    street2: NotRequired[str]
    street3: NotRequired[str]
    APIVersion: NotRequired[str]

class GetStatusInputRequestTypeDef(TypedDict):
    JobId: str
    APIVersion: NotRequired[str]

class JobTypeDef(TypedDict):
    JobId: NotRequired[str]
    CreationDate: NotRequired[datetime]
    IsCanceled: NotRequired[bool]
    JobType: NotRequired[JobTypeType]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListJobsInputRequestTypeDef(TypedDict):
    MaxJobs: NotRequired[int]
    Marker: NotRequired[str]
    APIVersion: NotRequired[str]

class UpdateJobInputRequestTypeDef(TypedDict):
    JobId: str
    Manifest: str
    JobType: JobTypeType
    ValidateOnly: bool
    APIVersion: NotRequired[str]

class CancelJobOutputTypeDef(TypedDict):
    Success: bool
    ResponseMetadata: ResponseMetadataTypeDef

class CreateJobOutputTypeDef(TypedDict):
    JobId: str
    JobType: JobTypeType
    Signature: str
    SignatureFileContents: str
    WarningMessage: str
    ArtifactList: List[ArtifactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

GetShippingLabelOutputTypeDef = TypedDict(
    "GetShippingLabelOutputTypeDef",
    {
        "ShippingLabelURL": str,
        "Warning": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetStatusOutputTypeDef(TypedDict):
    JobId: str
    JobType: JobTypeType
    LocationCode: str
    LocationMessage: str
    ProgressCode: str
    ProgressMessage: str
    Carrier: str
    TrackingNumber: str
    LogBucket: str
    LogKey: str
    ErrorCount: int
    Signature: str
    SignatureFileContents: str
    CurrentManifest: str
    CreationDate: datetime
    ArtifactList: List[ArtifactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateJobOutputTypeDef(TypedDict):
    Success: bool
    WarningMessage: str
    ArtifactList: List[ArtifactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListJobsOutputTypeDef(TypedDict):
    Jobs: List[JobTypeDef]
    IsTruncated: bool
    ResponseMetadata: ResponseMetadataTypeDef

class ListJobsInputListJobsPaginateTypeDef(TypedDict):
    APIVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]
