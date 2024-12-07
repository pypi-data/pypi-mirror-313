"""
Type annotations for healthlake service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_healthlake/type_defs/)

Usage::

    ```python
    from mypy_boto3_healthlake.type_defs import IdentityProviderConfigurationTypeDef

    data: IdentityProviderConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AuthorizationStrategyType,
    CmkTypeType,
    DatastoreStatusType,
    ErrorCategoryType,
    JobStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "CreateFHIRDatastoreRequestRequestTypeDef",
    "CreateFHIRDatastoreResponseTypeDef",
    "DatastoreFilterTypeDef",
    "DatastorePropertiesTypeDef",
    "DeleteFHIRDatastoreRequestRequestTypeDef",
    "DeleteFHIRDatastoreResponseTypeDef",
    "DescribeFHIRDatastoreRequestRequestTypeDef",
    "DescribeFHIRDatastoreResponseTypeDef",
    "DescribeFHIRExportJobRequestRequestTypeDef",
    "DescribeFHIRExportJobResponseTypeDef",
    "DescribeFHIRImportJobRequestRequestTypeDef",
    "DescribeFHIRImportJobResponseTypeDef",
    "ErrorCauseTypeDef",
    "ExportJobPropertiesTypeDef",
    "IdentityProviderConfigurationTypeDef",
    "ImportJobPropertiesTypeDef",
    "InputDataConfigTypeDef",
    "JobProgressReportTypeDef",
    "KmsEncryptionConfigTypeDef",
    "ListFHIRDatastoresRequestRequestTypeDef",
    "ListFHIRDatastoresResponseTypeDef",
    "ListFHIRExportJobsRequestRequestTypeDef",
    "ListFHIRExportJobsResponseTypeDef",
    "ListFHIRImportJobsRequestRequestTypeDef",
    "ListFHIRImportJobsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "OutputDataConfigTypeDef",
    "PreloadDataConfigTypeDef",
    "ResponseMetadataTypeDef",
    "S3ConfigurationTypeDef",
    "SseConfigurationTypeDef",
    "StartFHIRExportJobRequestRequestTypeDef",
    "StartFHIRExportJobResponseTypeDef",
    "StartFHIRImportJobRequestRequestTypeDef",
    "StartFHIRImportJobResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
)

class IdentityProviderConfigurationTypeDef(TypedDict):
    AuthorizationStrategy: AuthorizationStrategyType
    FineGrainedAuthorizationEnabled: NotRequired[bool]
    Metadata: NotRequired[str]
    IdpLambdaArn: NotRequired[str]

class PreloadDataConfigTypeDef(TypedDict):
    PreloadDataType: Literal["SYNTHEA"]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class ErrorCauseTypeDef(TypedDict):
    ErrorMessage: NotRequired[str]
    ErrorCategory: NotRequired[ErrorCategoryType]

class DeleteFHIRDatastoreRequestRequestTypeDef(TypedDict):
    DatastoreId: str

class DescribeFHIRDatastoreRequestRequestTypeDef(TypedDict):
    DatastoreId: str

class DescribeFHIRExportJobRequestRequestTypeDef(TypedDict):
    DatastoreId: str
    JobId: str

class DescribeFHIRImportJobRequestRequestTypeDef(TypedDict):
    DatastoreId: str
    JobId: str

class InputDataConfigTypeDef(TypedDict):
    S3Uri: NotRequired[str]

class JobProgressReportTypeDef(TypedDict):
    TotalNumberOfScannedFiles: NotRequired[int]
    TotalSizeOfScannedFilesInMB: NotRequired[float]
    TotalNumberOfImportedFiles: NotRequired[int]
    TotalNumberOfResourcesScanned: NotRequired[int]
    TotalNumberOfResourcesImported: NotRequired[int]
    TotalNumberOfResourcesWithCustomerError: NotRequired[int]
    TotalNumberOfFilesReadWithCustomerError: NotRequired[int]
    Throughput: NotRequired[float]

class KmsEncryptionConfigTypeDef(TypedDict):
    CmkType: CmkTypeType
    KmsKeyId: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str

class S3ConfigurationTypeDef(TypedDict):
    S3Uri: str
    KmsKeyId: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]

class CreateFHIRDatastoreResponseTypeDef(TypedDict):
    DatastoreId: str
    DatastoreArn: str
    DatastoreStatus: DatastoreStatusType
    DatastoreEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteFHIRDatastoreResponseTypeDef(TypedDict):
    DatastoreId: str
    DatastoreArn: str
    DatastoreStatus: DatastoreStatusType
    DatastoreEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartFHIRExportJobResponseTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    DatastoreId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartFHIRImportJobResponseTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    DatastoreId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DatastoreFilterTypeDef(TypedDict):
    DatastoreName: NotRequired[str]
    DatastoreStatus: NotRequired[DatastoreStatusType]
    CreatedBefore: NotRequired[TimestampTypeDef]
    CreatedAfter: NotRequired[TimestampTypeDef]

class ListFHIRExportJobsRequestRequestTypeDef(TypedDict):
    DatastoreId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmittedBefore: NotRequired[TimestampTypeDef]
    SubmittedAfter: NotRequired[TimestampTypeDef]

class ListFHIRImportJobsRequestRequestTypeDef(TypedDict):
    DatastoreId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmittedBefore: NotRequired[TimestampTypeDef]
    SubmittedAfter: NotRequired[TimestampTypeDef]

class SseConfigurationTypeDef(TypedDict):
    KmsEncryptionConfig: KmsEncryptionConfigTypeDef

class OutputDataConfigTypeDef(TypedDict):
    S3Configuration: NotRequired[S3ConfigurationTypeDef]

class ListFHIRDatastoresRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[DatastoreFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class CreateFHIRDatastoreRequestRequestTypeDef(TypedDict):
    DatastoreTypeVersion: Literal["R4"]
    DatastoreName: NotRequired[str]
    SseConfiguration: NotRequired[SseConfigurationTypeDef]
    PreloadDataConfig: NotRequired[PreloadDataConfigTypeDef]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    IdentityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]

class DatastorePropertiesTypeDef(TypedDict):
    DatastoreId: str
    DatastoreArn: str
    DatastoreStatus: DatastoreStatusType
    DatastoreTypeVersion: Literal["R4"]
    DatastoreEndpoint: str
    DatastoreName: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    SseConfiguration: NotRequired[SseConfigurationTypeDef]
    PreloadDataConfig: NotRequired[PreloadDataConfigTypeDef]
    IdentityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]
    ErrorCause: NotRequired[ErrorCauseTypeDef]

class ExportJobPropertiesTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    SubmitTime: datetime
    DatastoreId: str
    OutputDataConfig: OutputDataConfigTypeDef
    JobName: NotRequired[str]
    EndTime: NotRequired[datetime]
    DataAccessRoleArn: NotRequired[str]
    Message: NotRequired[str]

class ImportJobPropertiesTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    SubmitTime: datetime
    DatastoreId: str
    InputDataConfig: InputDataConfigTypeDef
    JobName: NotRequired[str]
    EndTime: NotRequired[datetime]
    JobOutputDataConfig: NotRequired[OutputDataConfigTypeDef]
    JobProgressReport: NotRequired[JobProgressReportTypeDef]
    DataAccessRoleArn: NotRequired[str]
    Message: NotRequired[str]

class StartFHIRExportJobRequestRequestTypeDef(TypedDict):
    OutputDataConfig: OutputDataConfigTypeDef
    DatastoreId: str
    DataAccessRoleArn: str
    ClientToken: str
    JobName: NotRequired[str]

class StartFHIRImportJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    JobOutputDataConfig: OutputDataConfigTypeDef
    DatastoreId: str
    DataAccessRoleArn: str
    ClientToken: str
    JobName: NotRequired[str]

class DescribeFHIRDatastoreResponseTypeDef(TypedDict):
    DatastoreProperties: DatastorePropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListFHIRDatastoresResponseTypeDef(TypedDict):
    DatastorePropertiesList: List[DatastorePropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeFHIRExportJobResponseTypeDef(TypedDict):
    ExportJobProperties: ExportJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListFHIRExportJobsResponseTypeDef(TypedDict):
    ExportJobPropertiesList: List[ExportJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeFHIRImportJobResponseTypeDef(TypedDict):
    ImportJobProperties: ImportJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListFHIRImportJobsResponseTypeDef(TypedDict):
    ImportJobPropertiesList: List[ImportJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
