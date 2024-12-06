"""
Type annotations for comprehendmedical service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_comprehendmedical/type_defs/)

Usage::

    ```python
    from mypy_boto3_comprehendmedical.type_defs import TraitTypeDef

    data: TraitTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Union

from .literals import (
    AttributeNameType,
    EntitySubTypeType,
    EntityTypeType,
    ICD10CMAttributeTypeType,
    ICD10CMEntityTypeType,
    ICD10CMRelationshipTypeType,
    ICD10CMTraitNameType,
    JobStatusType,
    RelationshipTypeType,
    RxNormAttributeTypeType,
    RxNormEntityTypeType,
    RxNormTraitNameType,
    SNOMEDCTAttributeTypeType,
    SNOMEDCTEntityCategoryType,
    SNOMEDCTEntityTypeType,
    SNOMEDCTRelationshipTypeType,
    SNOMEDCTTraitNameType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AttributeTypeDef",
    "CharactersTypeDef",
    "ComprehendMedicalAsyncJobFilterTypeDef",
    "ComprehendMedicalAsyncJobPropertiesTypeDef",
    "DescribeEntitiesDetectionV2JobRequestRequestTypeDef",
    "DescribeEntitiesDetectionV2JobResponseTypeDef",
    "DescribeICD10CMInferenceJobRequestRequestTypeDef",
    "DescribeICD10CMInferenceJobResponseTypeDef",
    "DescribePHIDetectionJobRequestRequestTypeDef",
    "DescribePHIDetectionJobResponseTypeDef",
    "DescribeRxNormInferenceJobRequestRequestTypeDef",
    "DescribeRxNormInferenceJobResponseTypeDef",
    "DescribeSNOMEDCTInferenceJobRequestRequestTypeDef",
    "DescribeSNOMEDCTInferenceJobResponseTypeDef",
    "DetectEntitiesRequestRequestTypeDef",
    "DetectEntitiesResponseTypeDef",
    "DetectEntitiesV2RequestRequestTypeDef",
    "DetectEntitiesV2ResponseTypeDef",
    "DetectPHIRequestRequestTypeDef",
    "DetectPHIResponseTypeDef",
    "EntityTypeDef",
    "ICD10CMAttributeTypeDef",
    "ICD10CMConceptTypeDef",
    "ICD10CMEntityTypeDef",
    "ICD10CMTraitTypeDef",
    "InferICD10CMRequestRequestTypeDef",
    "InferICD10CMResponseTypeDef",
    "InferRxNormRequestRequestTypeDef",
    "InferRxNormResponseTypeDef",
    "InferSNOMEDCTRequestRequestTypeDef",
    "InferSNOMEDCTResponseTypeDef",
    "InputDataConfigTypeDef",
    "ListEntitiesDetectionV2JobsRequestRequestTypeDef",
    "ListEntitiesDetectionV2JobsResponseTypeDef",
    "ListICD10CMInferenceJobsRequestRequestTypeDef",
    "ListICD10CMInferenceJobsResponseTypeDef",
    "ListPHIDetectionJobsRequestRequestTypeDef",
    "ListPHIDetectionJobsResponseTypeDef",
    "ListRxNormInferenceJobsRequestRequestTypeDef",
    "ListRxNormInferenceJobsResponseTypeDef",
    "ListSNOMEDCTInferenceJobsRequestRequestTypeDef",
    "ListSNOMEDCTInferenceJobsResponseTypeDef",
    "OutputDataConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RxNormAttributeTypeDef",
    "RxNormConceptTypeDef",
    "RxNormEntityTypeDef",
    "RxNormTraitTypeDef",
    "SNOMEDCTAttributeTypeDef",
    "SNOMEDCTConceptTypeDef",
    "SNOMEDCTDetailsTypeDef",
    "SNOMEDCTEntityTypeDef",
    "SNOMEDCTTraitTypeDef",
    "StartEntitiesDetectionV2JobRequestRequestTypeDef",
    "StartEntitiesDetectionV2JobResponseTypeDef",
    "StartICD10CMInferenceJobRequestRequestTypeDef",
    "StartICD10CMInferenceJobResponseTypeDef",
    "StartPHIDetectionJobRequestRequestTypeDef",
    "StartPHIDetectionJobResponseTypeDef",
    "StartRxNormInferenceJobRequestRequestTypeDef",
    "StartRxNormInferenceJobResponseTypeDef",
    "StartSNOMEDCTInferenceJobRequestRequestTypeDef",
    "StartSNOMEDCTInferenceJobResponseTypeDef",
    "StopEntitiesDetectionV2JobRequestRequestTypeDef",
    "StopEntitiesDetectionV2JobResponseTypeDef",
    "StopICD10CMInferenceJobRequestRequestTypeDef",
    "StopICD10CMInferenceJobResponseTypeDef",
    "StopPHIDetectionJobRequestRequestTypeDef",
    "StopPHIDetectionJobResponseTypeDef",
    "StopRxNormInferenceJobRequestRequestTypeDef",
    "StopRxNormInferenceJobResponseTypeDef",
    "StopSNOMEDCTInferenceJobRequestRequestTypeDef",
    "StopSNOMEDCTInferenceJobResponseTypeDef",
    "TimestampTypeDef",
    "TraitTypeDef",
    "UnmappedAttributeTypeDef",
)

class TraitTypeDef(TypedDict):
    Name: NotRequired[AttributeNameType]
    Score: NotRequired[float]

class CharactersTypeDef(TypedDict):
    OriginalTextCharacters: NotRequired[int]

TimestampTypeDef = Union[datetime, str]

class InputDataConfigTypeDef(TypedDict):
    S3Bucket: str
    S3Key: NotRequired[str]

class OutputDataConfigTypeDef(TypedDict):
    S3Bucket: str
    S3Key: NotRequired[str]

class DescribeEntitiesDetectionV2JobRequestRequestTypeDef(TypedDict):
    JobId: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DescribeICD10CMInferenceJobRequestRequestTypeDef(TypedDict):
    JobId: str

class DescribePHIDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class DescribeRxNormInferenceJobRequestRequestTypeDef(TypedDict):
    JobId: str

class DescribeSNOMEDCTInferenceJobRequestRequestTypeDef(TypedDict):
    JobId: str

DetectEntitiesRequestRequestTypeDef = TypedDict(
    "DetectEntitiesRequestRequestTypeDef",
    {
        "Text": str,
    },
)
DetectEntitiesV2RequestRequestTypeDef = TypedDict(
    "DetectEntitiesV2RequestRequestTypeDef",
    {
        "Text": str,
    },
)
DetectPHIRequestRequestTypeDef = TypedDict(
    "DetectPHIRequestRequestTypeDef",
    {
        "Text": str,
    },
)

class ICD10CMTraitTypeDef(TypedDict):
    Name: NotRequired[ICD10CMTraitNameType]
    Score: NotRequired[float]

class ICD10CMConceptTypeDef(TypedDict):
    Description: NotRequired[str]
    Code: NotRequired[str]
    Score: NotRequired[float]

InferICD10CMRequestRequestTypeDef = TypedDict(
    "InferICD10CMRequestRequestTypeDef",
    {
        "Text": str,
    },
)
InferRxNormRequestRequestTypeDef = TypedDict(
    "InferRxNormRequestRequestTypeDef",
    {
        "Text": str,
    },
)
InferSNOMEDCTRequestRequestTypeDef = TypedDict(
    "InferSNOMEDCTRequestRequestTypeDef",
    {
        "Text": str,
    },
)

class SNOMEDCTDetailsTypeDef(TypedDict):
    Edition: NotRequired[str]
    Language: NotRequired[str]
    VersionDate: NotRequired[str]

class RxNormTraitTypeDef(TypedDict):
    Name: NotRequired[RxNormTraitNameType]
    Score: NotRequired[float]

class RxNormConceptTypeDef(TypedDict):
    Description: NotRequired[str]
    Code: NotRequired[str]
    Score: NotRequired[float]

class SNOMEDCTConceptTypeDef(TypedDict):
    Description: NotRequired[str]
    Code: NotRequired[str]
    Score: NotRequired[float]

class SNOMEDCTTraitTypeDef(TypedDict):
    Name: NotRequired[SNOMEDCTTraitNameType]
    Score: NotRequired[float]

class StopEntitiesDetectionV2JobRequestRequestTypeDef(TypedDict):
    JobId: str

class StopICD10CMInferenceJobRequestRequestTypeDef(TypedDict):
    JobId: str

class StopPHIDetectionJobRequestRequestTypeDef(TypedDict):
    JobId: str

class StopRxNormInferenceJobRequestRequestTypeDef(TypedDict):
    JobId: str

class StopSNOMEDCTInferenceJobRequestRequestTypeDef(TypedDict):
    JobId: str

AttributeTypeDef = TypedDict(
    "AttributeTypeDef",
    {
        "Type": NotRequired[EntitySubTypeType],
        "Score": NotRequired[float],
        "RelationshipScore": NotRequired[float],
        "RelationshipType": NotRequired[RelationshipTypeType],
        "Id": NotRequired[int],
        "BeginOffset": NotRequired[int],
        "EndOffset": NotRequired[int],
        "Text": NotRequired[str],
        "Category": NotRequired[EntityTypeType],
        "Traits": NotRequired[List[TraitTypeDef]],
    },
)

class ComprehendMedicalAsyncJobFilterTypeDef(TypedDict):
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmitTimeBefore: NotRequired[TimestampTypeDef]
    SubmitTimeAfter: NotRequired[TimestampTypeDef]

class ComprehendMedicalAsyncJobPropertiesTypeDef(TypedDict):
    JobId: NotRequired[str]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    Message: NotRequired[str]
    SubmitTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    ExpirationTime: NotRequired[datetime]
    InputDataConfig: NotRequired[InputDataConfigTypeDef]
    OutputDataConfig: NotRequired[OutputDataConfigTypeDef]
    LanguageCode: NotRequired[Literal["en"]]
    DataAccessRoleArn: NotRequired[str]
    ManifestFilePath: NotRequired[str]
    KMSKey: NotRequired[str]
    ModelVersion: NotRequired[str]

class StartEntitiesDetectionV2JobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    DataAccessRoleArn: str
    LanguageCode: Literal["en"]
    JobName: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    KMSKey: NotRequired[str]

class StartICD10CMInferenceJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    DataAccessRoleArn: str
    LanguageCode: Literal["en"]
    JobName: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    KMSKey: NotRequired[str]

class StartPHIDetectionJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    DataAccessRoleArn: str
    LanguageCode: Literal["en"]
    JobName: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    KMSKey: NotRequired[str]

class StartRxNormInferenceJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    DataAccessRoleArn: str
    LanguageCode: Literal["en"]
    JobName: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    KMSKey: NotRequired[str]

class StartSNOMEDCTInferenceJobRequestRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    OutputDataConfig: OutputDataConfigTypeDef
    DataAccessRoleArn: str
    LanguageCode: Literal["en"]
    JobName: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    KMSKey: NotRequired[str]

class StartEntitiesDetectionV2JobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartICD10CMInferenceJobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartPHIDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartRxNormInferenceJobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartSNOMEDCTInferenceJobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StopEntitiesDetectionV2JobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StopICD10CMInferenceJobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StopPHIDetectionJobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StopRxNormInferenceJobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StopSNOMEDCTInferenceJobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef

ICD10CMAttributeTypeDef = TypedDict(
    "ICD10CMAttributeTypeDef",
    {
        "Type": NotRequired[ICD10CMAttributeTypeType],
        "Score": NotRequired[float],
        "RelationshipScore": NotRequired[float],
        "Id": NotRequired[int],
        "BeginOffset": NotRequired[int],
        "EndOffset": NotRequired[int],
        "Text": NotRequired[str],
        "Traits": NotRequired[List[ICD10CMTraitTypeDef]],
        "Category": NotRequired[ICD10CMEntityTypeType],
        "RelationshipType": NotRequired[ICD10CMRelationshipTypeType],
    },
)
RxNormAttributeTypeDef = TypedDict(
    "RxNormAttributeTypeDef",
    {
        "Type": NotRequired[RxNormAttributeTypeType],
        "Score": NotRequired[float],
        "RelationshipScore": NotRequired[float],
        "Id": NotRequired[int],
        "BeginOffset": NotRequired[int],
        "EndOffset": NotRequired[int],
        "Text": NotRequired[str],
        "Traits": NotRequired[List[RxNormTraitTypeDef]],
    },
)
SNOMEDCTAttributeTypeDef = TypedDict(
    "SNOMEDCTAttributeTypeDef",
    {
        "Category": NotRequired[SNOMEDCTEntityCategoryType],
        "Type": NotRequired[SNOMEDCTAttributeTypeType],
        "Score": NotRequired[float],
        "RelationshipScore": NotRequired[float],
        "RelationshipType": NotRequired[SNOMEDCTRelationshipTypeType],
        "Id": NotRequired[int],
        "BeginOffset": NotRequired[int],
        "EndOffset": NotRequired[int],
        "Text": NotRequired[str],
        "Traits": NotRequired[List[SNOMEDCTTraitTypeDef]],
        "SNOMEDCTConcepts": NotRequired[List[SNOMEDCTConceptTypeDef]],
    },
)
EntityTypeDef = TypedDict(
    "EntityTypeDef",
    {
        "Id": NotRequired[int],
        "BeginOffset": NotRequired[int],
        "EndOffset": NotRequired[int],
        "Score": NotRequired[float],
        "Text": NotRequired[str],
        "Category": NotRequired[EntityTypeType],
        "Type": NotRequired[EntitySubTypeType],
        "Traits": NotRequired[List[TraitTypeDef]],
        "Attributes": NotRequired[List[AttributeTypeDef]],
    },
)
UnmappedAttributeTypeDef = TypedDict(
    "UnmappedAttributeTypeDef",
    {
        "Type": NotRequired[EntityTypeType],
        "Attribute": NotRequired[AttributeTypeDef],
    },
)

class ListEntitiesDetectionV2JobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[ComprehendMedicalAsyncJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListICD10CMInferenceJobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[ComprehendMedicalAsyncJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListPHIDetectionJobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[ComprehendMedicalAsyncJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListRxNormInferenceJobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[ComprehendMedicalAsyncJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListSNOMEDCTInferenceJobsRequestRequestTypeDef(TypedDict):
    Filter: NotRequired[ComprehendMedicalAsyncJobFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class DescribeEntitiesDetectionV2JobResponseTypeDef(TypedDict):
    ComprehendMedicalAsyncJobProperties: ComprehendMedicalAsyncJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeICD10CMInferenceJobResponseTypeDef(TypedDict):
    ComprehendMedicalAsyncJobProperties: ComprehendMedicalAsyncJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePHIDetectionJobResponseTypeDef(TypedDict):
    ComprehendMedicalAsyncJobProperties: ComprehendMedicalAsyncJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeRxNormInferenceJobResponseTypeDef(TypedDict):
    ComprehendMedicalAsyncJobProperties: ComprehendMedicalAsyncJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeSNOMEDCTInferenceJobResponseTypeDef(TypedDict):
    ComprehendMedicalAsyncJobProperties: ComprehendMedicalAsyncJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListEntitiesDetectionV2JobsResponseTypeDef(TypedDict):
    ComprehendMedicalAsyncJobPropertiesList: List[ComprehendMedicalAsyncJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListICD10CMInferenceJobsResponseTypeDef(TypedDict):
    ComprehendMedicalAsyncJobPropertiesList: List[ComprehendMedicalAsyncJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPHIDetectionJobsResponseTypeDef(TypedDict):
    ComprehendMedicalAsyncJobPropertiesList: List[ComprehendMedicalAsyncJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListRxNormInferenceJobsResponseTypeDef(TypedDict):
    ComprehendMedicalAsyncJobPropertiesList: List[ComprehendMedicalAsyncJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSNOMEDCTInferenceJobsResponseTypeDef(TypedDict):
    ComprehendMedicalAsyncJobPropertiesList: List[ComprehendMedicalAsyncJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

ICD10CMEntityTypeDef = TypedDict(
    "ICD10CMEntityTypeDef",
    {
        "Id": NotRequired[int],
        "Text": NotRequired[str],
        "Category": NotRequired[Literal["MEDICAL_CONDITION"]],
        "Type": NotRequired[ICD10CMEntityTypeType],
        "Score": NotRequired[float],
        "BeginOffset": NotRequired[int],
        "EndOffset": NotRequired[int],
        "Attributes": NotRequired[List[ICD10CMAttributeTypeDef]],
        "Traits": NotRequired[List[ICD10CMTraitTypeDef]],
        "ICD10CMConcepts": NotRequired[List[ICD10CMConceptTypeDef]],
    },
)
RxNormEntityTypeDef = TypedDict(
    "RxNormEntityTypeDef",
    {
        "Id": NotRequired[int],
        "Text": NotRequired[str],
        "Category": NotRequired[Literal["MEDICATION"]],
        "Type": NotRequired[RxNormEntityTypeType],
        "Score": NotRequired[float],
        "BeginOffset": NotRequired[int],
        "EndOffset": NotRequired[int],
        "Attributes": NotRequired[List[RxNormAttributeTypeDef]],
        "Traits": NotRequired[List[RxNormTraitTypeDef]],
        "RxNormConcepts": NotRequired[List[RxNormConceptTypeDef]],
    },
)
SNOMEDCTEntityTypeDef = TypedDict(
    "SNOMEDCTEntityTypeDef",
    {
        "Id": NotRequired[int],
        "Text": NotRequired[str],
        "Category": NotRequired[SNOMEDCTEntityCategoryType],
        "Type": NotRequired[SNOMEDCTEntityTypeType],
        "Score": NotRequired[float],
        "BeginOffset": NotRequired[int],
        "EndOffset": NotRequired[int],
        "Attributes": NotRequired[List[SNOMEDCTAttributeTypeDef]],
        "Traits": NotRequired[List[SNOMEDCTTraitTypeDef]],
        "SNOMEDCTConcepts": NotRequired[List[SNOMEDCTConceptTypeDef]],
    },
)

class DetectPHIResponseTypeDef(TypedDict):
    Entities: List[EntityTypeDef]
    PaginationToken: str
    ModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef

class DetectEntitiesResponseTypeDef(TypedDict):
    Entities: List[EntityTypeDef]
    UnmappedAttributes: List[UnmappedAttributeTypeDef]
    PaginationToken: str
    ModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef

class DetectEntitiesV2ResponseTypeDef(TypedDict):
    Entities: List[EntityTypeDef]
    UnmappedAttributes: List[UnmappedAttributeTypeDef]
    PaginationToken: str
    ModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef

class InferICD10CMResponseTypeDef(TypedDict):
    Entities: List[ICD10CMEntityTypeDef]
    PaginationToken: str
    ModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef

class InferRxNormResponseTypeDef(TypedDict):
    Entities: List[RxNormEntityTypeDef]
    PaginationToken: str
    ModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef

class InferSNOMEDCTResponseTypeDef(TypedDict):
    Entities: List[SNOMEDCTEntityTypeDef]
    PaginationToken: str
    ModelVersion: str
    SNOMEDCTDetails: SNOMEDCTDetailsTypeDef
    Characters: CharactersTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
