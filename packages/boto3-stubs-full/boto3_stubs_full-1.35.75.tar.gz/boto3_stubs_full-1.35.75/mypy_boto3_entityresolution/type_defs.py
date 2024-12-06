"""
Type annotations for entityresolution service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_entityresolution/type_defs/)

Usage::

    ```python
    from mypy_boto3_entityresolution.type_defs import AddPolicyStatementInputRequestTypeDef

    data: AddPolicyStatementInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AttributeMatchingModelType,
    DeleteUniqueIdErrorTypeType,
    DeleteUniqueIdStatusType,
    IdMappingTypeType,
    IdMappingWorkflowRuleDefinitionTypeType,
    IdNamespaceTypeType,
    JobStatusType,
    MatchPurposeType,
    RecordMatchingModelType,
    ResolutionTypeType,
    SchemaAttributeTypeType,
    ServiceTypeType,
    StatementEffectType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AddPolicyStatementInputRequestTypeDef",
    "AddPolicyStatementOutputTypeDef",
    "BatchDeleteUniqueIdInputRequestTypeDef",
    "BatchDeleteUniqueIdOutputTypeDef",
    "CreateIdMappingWorkflowInputRequestTypeDef",
    "CreateIdMappingWorkflowOutputTypeDef",
    "CreateIdNamespaceInputRequestTypeDef",
    "CreateIdNamespaceOutputTypeDef",
    "CreateMatchingWorkflowInputRequestTypeDef",
    "CreateMatchingWorkflowOutputTypeDef",
    "CreateSchemaMappingInputRequestTypeDef",
    "CreateSchemaMappingOutputTypeDef",
    "DeleteIdMappingWorkflowInputRequestTypeDef",
    "DeleteIdMappingWorkflowOutputTypeDef",
    "DeleteIdNamespaceInputRequestTypeDef",
    "DeleteIdNamespaceOutputTypeDef",
    "DeleteMatchingWorkflowInputRequestTypeDef",
    "DeleteMatchingWorkflowOutputTypeDef",
    "DeletePolicyStatementInputRequestTypeDef",
    "DeletePolicyStatementOutputTypeDef",
    "DeleteSchemaMappingInputRequestTypeDef",
    "DeleteSchemaMappingOutputTypeDef",
    "DeleteUniqueIdErrorTypeDef",
    "DeletedUniqueIdTypeDef",
    "ErrorDetailsTypeDef",
    "GetIdMappingJobInputRequestTypeDef",
    "GetIdMappingJobOutputTypeDef",
    "GetIdMappingWorkflowInputRequestTypeDef",
    "GetIdMappingWorkflowOutputTypeDef",
    "GetIdNamespaceInputRequestTypeDef",
    "GetIdNamespaceOutputTypeDef",
    "GetMatchIdInputRequestTypeDef",
    "GetMatchIdOutputTypeDef",
    "GetMatchingJobInputRequestTypeDef",
    "GetMatchingJobOutputTypeDef",
    "GetMatchingWorkflowInputRequestTypeDef",
    "GetMatchingWorkflowOutputTypeDef",
    "GetPolicyInputRequestTypeDef",
    "GetPolicyOutputTypeDef",
    "GetProviderServiceInputRequestTypeDef",
    "GetProviderServiceOutputTypeDef",
    "GetSchemaMappingInputRequestTypeDef",
    "GetSchemaMappingOutputTypeDef",
    "IdMappingJobMetricsTypeDef",
    "IdMappingJobOutputSourceTypeDef",
    "IdMappingRuleBasedPropertiesOutputTypeDef",
    "IdMappingRuleBasedPropertiesTypeDef",
    "IdMappingRuleBasedPropertiesUnionTypeDef",
    "IdMappingTechniquesOutputTypeDef",
    "IdMappingTechniquesTypeDef",
    "IdMappingWorkflowInputSourceTypeDef",
    "IdMappingWorkflowOutputSourceTypeDef",
    "IdMappingWorkflowSummaryTypeDef",
    "IdNamespaceIdMappingWorkflowMetadataTypeDef",
    "IdNamespaceIdMappingWorkflowPropertiesOutputTypeDef",
    "IdNamespaceIdMappingWorkflowPropertiesTypeDef",
    "IdNamespaceIdMappingWorkflowPropertiesUnionTypeDef",
    "IdNamespaceInputSourceTypeDef",
    "IdNamespaceSummaryTypeDef",
    "IncrementalRunConfigTypeDef",
    "InputSourceTypeDef",
    "IntermediateSourceConfigurationTypeDef",
    "JobMetricsTypeDef",
    "JobOutputSourceTypeDef",
    "JobSummaryTypeDef",
    "ListIdMappingJobsInputListIdMappingJobsPaginateTypeDef",
    "ListIdMappingJobsInputRequestTypeDef",
    "ListIdMappingJobsOutputTypeDef",
    "ListIdMappingWorkflowsInputListIdMappingWorkflowsPaginateTypeDef",
    "ListIdMappingWorkflowsInputRequestTypeDef",
    "ListIdMappingWorkflowsOutputTypeDef",
    "ListIdNamespacesInputListIdNamespacesPaginateTypeDef",
    "ListIdNamespacesInputRequestTypeDef",
    "ListIdNamespacesOutputTypeDef",
    "ListMatchingJobsInputListMatchingJobsPaginateTypeDef",
    "ListMatchingJobsInputRequestTypeDef",
    "ListMatchingJobsOutputTypeDef",
    "ListMatchingWorkflowsInputListMatchingWorkflowsPaginateTypeDef",
    "ListMatchingWorkflowsInputRequestTypeDef",
    "ListMatchingWorkflowsOutputTypeDef",
    "ListProviderServicesInputListProviderServicesPaginateTypeDef",
    "ListProviderServicesInputRequestTypeDef",
    "ListProviderServicesOutputTypeDef",
    "ListSchemaMappingsInputListSchemaMappingsPaginateTypeDef",
    "ListSchemaMappingsInputRequestTypeDef",
    "ListSchemaMappingsOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "MatchingWorkflowSummaryTypeDef",
    "NamespaceProviderPropertiesOutputTypeDef",
    "NamespaceProviderPropertiesTypeDef",
    "NamespaceProviderPropertiesUnionTypeDef",
    "NamespaceRuleBasedPropertiesOutputTypeDef",
    "NamespaceRuleBasedPropertiesTypeDef",
    "NamespaceRuleBasedPropertiesUnionTypeDef",
    "OutputAttributeTypeDef",
    "OutputSourceOutputTypeDef",
    "OutputSourceTypeDef",
    "OutputSourceUnionTypeDef",
    "PaginatorConfigTypeDef",
    "ProviderComponentSchemaTypeDef",
    "ProviderEndpointConfigurationTypeDef",
    "ProviderIdNameSpaceConfigurationTypeDef",
    "ProviderIntermediateDataAccessConfigurationTypeDef",
    "ProviderMarketplaceConfigurationTypeDef",
    "ProviderPropertiesOutputTypeDef",
    "ProviderPropertiesTypeDef",
    "ProviderPropertiesUnionTypeDef",
    "ProviderSchemaAttributeTypeDef",
    "ProviderServiceSummaryTypeDef",
    "PutPolicyInputRequestTypeDef",
    "PutPolicyOutputTypeDef",
    "ResolutionTechniquesOutputTypeDef",
    "ResolutionTechniquesTypeDef",
    "ResponseMetadataTypeDef",
    "RuleBasedPropertiesOutputTypeDef",
    "RuleBasedPropertiesTypeDef",
    "RuleBasedPropertiesUnionTypeDef",
    "RuleOutputTypeDef",
    "RuleTypeDef",
    "RuleUnionTypeDef",
    "SchemaInputAttributeTypeDef",
    "SchemaMappingSummaryTypeDef",
    "StartIdMappingJobInputRequestTypeDef",
    "StartIdMappingJobOutputTypeDef",
    "StartMatchingJobInputRequestTypeDef",
    "StartMatchingJobOutputTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateIdMappingWorkflowInputRequestTypeDef",
    "UpdateIdMappingWorkflowOutputTypeDef",
    "UpdateIdNamespaceInputRequestTypeDef",
    "UpdateIdNamespaceOutputTypeDef",
    "UpdateMatchingWorkflowInputRequestTypeDef",
    "UpdateMatchingWorkflowOutputTypeDef",
    "UpdateSchemaMappingInputRequestTypeDef",
    "UpdateSchemaMappingOutputTypeDef",
)


class AddPolicyStatementInputRequestTypeDef(TypedDict):
    action: Sequence[str]
    arn: str
    effect: StatementEffectType
    principal: Sequence[str]
    statementId: str
    condition: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BatchDeleteUniqueIdInputRequestTypeDef(TypedDict):
    uniqueIds: Sequence[str]
    workflowName: str
    inputSource: NotRequired[str]


class DeleteUniqueIdErrorTypeDef(TypedDict):
    errorType: DeleteUniqueIdErrorTypeType
    uniqueId: str


class DeletedUniqueIdTypeDef(TypedDict):
    uniqueId: str


IdMappingWorkflowInputSourceTypeDef = TypedDict(
    "IdMappingWorkflowInputSourceTypeDef",
    {
        "inputSourceARN": str,
        "schemaName": NotRequired[str],
        "type": NotRequired[IdNamespaceTypeType],
    },
)


class IdMappingWorkflowOutputSourceTypeDef(TypedDict):
    outputS3Path: str
    KMSArn: NotRequired[str]


class IdNamespaceInputSourceTypeDef(TypedDict):
    inputSourceARN: str
    schemaName: NotRequired[str]


class IncrementalRunConfigTypeDef(TypedDict):
    incrementalRunType: NotRequired[Literal["IMMEDIATE"]]


class InputSourceTypeDef(TypedDict):
    inputSourceARN: str
    schemaName: str
    applyNormalization: NotRequired[bool]


SchemaInputAttributeTypeDef = TypedDict(
    "SchemaInputAttributeTypeDef",
    {
        "fieldName": str,
        "type": SchemaAttributeTypeType,
        "groupName": NotRequired[str],
        "hashed": NotRequired[bool],
        "matchKey": NotRequired[str],
        "subType": NotRequired[str],
    },
)


class DeleteIdMappingWorkflowInputRequestTypeDef(TypedDict):
    workflowName: str


class DeleteIdNamespaceInputRequestTypeDef(TypedDict):
    idNamespaceName: str


class DeleteMatchingWorkflowInputRequestTypeDef(TypedDict):
    workflowName: str


class DeletePolicyStatementInputRequestTypeDef(TypedDict):
    arn: str
    statementId: str


class DeleteSchemaMappingInputRequestTypeDef(TypedDict):
    schemaName: str


class ErrorDetailsTypeDef(TypedDict):
    errorMessage: NotRequired[str]


class GetIdMappingJobInputRequestTypeDef(TypedDict):
    jobId: str
    workflowName: str


class IdMappingJobMetricsTypeDef(TypedDict):
    inputRecords: NotRequired[int]
    recordsNotProcessed: NotRequired[int]
    totalMappedRecords: NotRequired[int]
    totalMappedSourceRecords: NotRequired[int]
    totalMappedTargetRecords: NotRequired[int]
    totalRecordsProcessed: NotRequired[int]


class IdMappingJobOutputSourceTypeDef(TypedDict):
    outputS3Path: str
    roleArn: str
    KMSArn: NotRequired[str]


class GetIdMappingWorkflowInputRequestTypeDef(TypedDict):
    workflowName: str


class GetIdNamespaceInputRequestTypeDef(TypedDict):
    idNamespaceName: str


class GetMatchIdInputRequestTypeDef(TypedDict):
    record: Mapping[str, str]
    workflowName: str
    applyNormalization: NotRequired[bool]


class GetMatchingJobInputRequestTypeDef(TypedDict):
    jobId: str
    workflowName: str


class JobMetricsTypeDef(TypedDict):
    inputRecords: NotRequired[int]
    matchIDs: NotRequired[int]
    recordsNotProcessed: NotRequired[int]
    totalRecordsProcessed: NotRequired[int]


class JobOutputSourceTypeDef(TypedDict):
    outputS3Path: str
    roleArn: str
    KMSArn: NotRequired[str]


class GetMatchingWorkflowInputRequestTypeDef(TypedDict):
    workflowName: str


class GetPolicyInputRequestTypeDef(TypedDict):
    arn: str


class GetProviderServiceInputRequestTypeDef(TypedDict):
    providerName: str
    providerServiceName: str


class ProviderIdNameSpaceConfigurationTypeDef(TypedDict):
    description: NotRequired[str]
    providerSourceConfigurationDefinition: NotRequired[Dict[str, Any]]
    providerTargetConfigurationDefinition: NotRequired[Dict[str, Any]]


class ProviderIntermediateDataAccessConfigurationTypeDef(TypedDict):
    awsAccountIds: NotRequired[List[str]]
    requiredBucketActions: NotRequired[List[str]]


class GetSchemaMappingInputRequestTypeDef(TypedDict):
    schemaName: str


class RuleOutputTypeDef(TypedDict):
    matchingKeys: List[str]
    ruleName: str


class IdMappingWorkflowSummaryTypeDef(TypedDict):
    createdAt: datetime
    updatedAt: datetime
    workflowArn: str
    workflowName: str


class IdNamespaceIdMappingWorkflowMetadataTypeDef(TypedDict):
    idMappingType: IdMappingTypeType


class NamespaceProviderPropertiesOutputTypeDef(TypedDict):
    providerServiceArn: str
    providerConfiguration: NotRequired[Dict[str, Any]]


class IntermediateSourceConfigurationTypeDef(TypedDict):
    intermediateS3Path: str


class JobSummaryTypeDef(TypedDict):
    jobId: str
    startTime: datetime
    status: JobStatusType
    endTime: NotRequired[datetime]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListIdMappingJobsInputRequestTypeDef(TypedDict):
    workflowName: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListIdMappingWorkflowsInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListIdNamespacesInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListMatchingJobsInputRequestTypeDef(TypedDict):
    workflowName: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListMatchingWorkflowsInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class MatchingWorkflowSummaryTypeDef(TypedDict):
    createdAt: datetime
    resolutionType: ResolutionTypeType
    updatedAt: datetime
    workflowArn: str
    workflowName: str


class ListProviderServicesInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    providerName: NotRequired[str]


class ProviderServiceSummaryTypeDef(TypedDict):
    providerName: str
    providerServiceArn: str
    providerServiceDisplayName: str
    providerServiceName: str
    providerServiceType: ServiceTypeType


class ListSchemaMappingsInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SchemaMappingSummaryTypeDef(TypedDict):
    createdAt: datetime
    hasWorkflows: bool
    schemaArn: str
    schemaName: str
    updatedAt: datetime


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str


class NamespaceProviderPropertiesTypeDef(TypedDict):
    providerServiceArn: str
    providerConfiguration: NotRequired[Mapping[str, Any]]


class OutputAttributeTypeDef(TypedDict):
    name: str
    hashed: NotRequired[bool]


ProviderSchemaAttributeTypeDef = TypedDict(
    "ProviderSchemaAttributeTypeDef",
    {
        "fieldName": str,
        "type": SchemaAttributeTypeType,
        "hashing": NotRequired[bool],
        "subType": NotRequired[str],
    },
)


class ProviderMarketplaceConfigurationTypeDef(TypedDict):
    assetId: str
    dataSetId: str
    listingId: str
    revisionId: str


class PutPolicyInputRequestTypeDef(TypedDict):
    arn: str
    policy: str
    token: NotRequired[str]


class RuleTypeDef(TypedDict):
    matchingKeys: Sequence[str]
    ruleName: str


class StartMatchingJobInputRequestTypeDef(TypedDict):
    workflowName: str


class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class AddPolicyStatementOutputTypeDef(TypedDict):
    arn: str
    policy: str
    token: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIdMappingWorkflowOutputTypeDef(TypedDict):
    message: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIdNamespaceOutputTypeDef(TypedDict):
    message: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMatchingWorkflowOutputTypeDef(TypedDict):
    message: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePolicyStatementOutputTypeDef(TypedDict):
    arn: str
    policy: str
    token: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSchemaMappingOutputTypeDef(TypedDict):
    message: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetMatchIdOutputTypeDef(TypedDict):
    matchId: str
    matchRule: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetPolicyOutputTypeDef(TypedDict):
    arn: str
    policy: str
    token: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutPolicyOutputTypeDef(TypedDict):
    arn: str
    policy: str
    token: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartMatchingJobOutputTypeDef(TypedDict):
    jobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDeleteUniqueIdOutputTypeDef(TypedDict):
    deleted: List[DeletedUniqueIdTypeDef]
    disconnectedUniqueIds: List[str]
    errors: List[DeleteUniqueIdErrorTypeDef]
    status: DeleteUniqueIdStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSchemaMappingInputRequestTypeDef(TypedDict):
    mappedInputFields: Sequence[SchemaInputAttributeTypeDef]
    schemaName: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class CreateSchemaMappingOutputTypeDef(TypedDict):
    description: str
    mappedInputFields: List[SchemaInputAttributeTypeDef]
    schemaArn: str
    schemaName: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSchemaMappingOutputTypeDef(TypedDict):
    createdAt: datetime
    description: str
    hasWorkflows: bool
    mappedInputFields: List[SchemaInputAttributeTypeDef]
    schemaArn: str
    schemaName: str
    tags: Dict[str, str]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSchemaMappingInputRequestTypeDef(TypedDict):
    mappedInputFields: Sequence[SchemaInputAttributeTypeDef]
    schemaName: str
    description: NotRequired[str]


class UpdateSchemaMappingOutputTypeDef(TypedDict):
    description: str
    mappedInputFields: List[SchemaInputAttributeTypeDef]
    schemaArn: str
    schemaName: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetIdMappingJobOutputTypeDef(TypedDict):
    endTime: datetime
    errorDetails: ErrorDetailsTypeDef
    jobId: str
    metrics: IdMappingJobMetricsTypeDef
    outputSourceConfig: List[IdMappingJobOutputSourceTypeDef]
    startTime: datetime
    status: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class StartIdMappingJobInputRequestTypeDef(TypedDict):
    workflowName: str
    outputSourceConfig: NotRequired[Sequence[IdMappingJobOutputSourceTypeDef]]


class StartIdMappingJobOutputTypeDef(TypedDict):
    jobId: str
    outputSourceConfig: List[IdMappingJobOutputSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetMatchingJobOutputTypeDef(TypedDict):
    endTime: datetime
    errorDetails: ErrorDetailsTypeDef
    jobId: str
    metrics: JobMetricsTypeDef
    outputSourceConfig: List[JobOutputSourceTypeDef]
    startTime: datetime
    status: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class IdMappingRuleBasedPropertiesOutputTypeDef(TypedDict):
    attributeMatchingModel: AttributeMatchingModelType
    recordMatchingModel: RecordMatchingModelType
    ruleDefinitionType: IdMappingWorkflowRuleDefinitionTypeType
    rules: NotRequired[List[RuleOutputTypeDef]]


class NamespaceRuleBasedPropertiesOutputTypeDef(TypedDict):
    attributeMatchingModel: NotRequired[AttributeMatchingModelType]
    recordMatchingModels: NotRequired[List[RecordMatchingModelType]]
    ruleDefinitionTypes: NotRequired[List[IdMappingWorkflowRuleDefinitionTypeType]]
    rules: NotRequired[List[RuleOutputTypeDef]]


class RuleBasedPropertiesOutputTypeDef(TypedDict):
    attributeMatchingModel: AttributeMatchingModelType
    rules: List[RuleOutputTypeDef]
    matchPurpose: NotRequired[MatchPurposeType]


class ListIdMappingWorkflowsOutputTypeDef(TypedDict):
    workflowSummaries: List[IdMappingWorkflowSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


IdNamespaceSummaryTypeDef = TypedDict(
    "IdNamespaceSummaryTypeDef",
    {
        "createdAt": datetime,
        "idNamespaceArn": str,
        "idNamespaceName": str,
        "type": IdNamespaceTypeType,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "idMappingWorkflowProperties": NotRequired[
            List[IdNamespaceIdMappingWorkflowMetadataTypeDef]
        ],
    },
)


class ProviderPropertiesOutputTypeDef(TypedDict):
    providerServiceArn: str
    intermediateSourceConfiguration: NotRequired[IntermediateSourceConfigurationTypeDef]
    providerConfiguration: NotRequired[Dict[str, Any]]


class ProviderPropertiesTypeDef(TypedDict):
    providerServiceArn: str
    intermediateSourceConfiguration: NotRequired[IntermediateSourceConfigurationTypeDef]
    providerConfiguration: NotRequired[Mapping[str, Any]]


class ListIdMappingJobsOutputTypeDef(TypedDict):
    jobs: List[JobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListMatchingJobsOutputTypeDef(TypedDict):
    jobs: List[JobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListIdMappingJobsInputListIdMappingJobsPaginateTypeDef(TypedDict):
    workflowName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIdMappingWorkflowsInputListIdMappingWorkflowsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIdNamespacesInputListIdNamespacesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMatchingJobsInputListMatchingJobsPaginateTypeDef(TypedDict):
    workflowName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMatchingWorkflowsInputListMatchingWorkflowsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProviderServicesInputListProviderServicesPaginateTypeDef(TypedDict):
    providerName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSchemaMappingsInputListSchemaMappingsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMatchingWorkflowsOutputTypeDef(TypedDict):
    workflowSummaries: List[MatchingWorkflowSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListProviderServicesOutputTypeDef(TypedDict):
    providerServiceSummaries: List[ProviderServiceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSchemaMappingsOutputTypeDef(TypedDict):
    schemaList: List[SchemaMappingSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


NamespaceProviderPropertiesUnionTypeDef = Union[
    NamespaceProviderPropertiesTypeDef, NamespaceProviderPropertiesOutputTypeDef
]


class OutputSourceOutputTypeDef(TypedDict):
    output: List[OutputAttributeTypeDef]
    outputS3Path: str
    KMSArn: NotRequired[str]
    applyNormalization: NotRequired[bool]


class OutputSourceTypeDef(TypedDict):
    output: Sequence[OutputAttributeTypeDef]
    outputS3Path: str
    KMSArn: NotRequired[str]
    applyNormalization: NotRequired[bool]


class ProviderComponentSchemaTypeDef(TypedDict):
    providerSchemaAttributes: NotRequired[List[ProviderSchemaAttributeTypeDef]]
    schemas: NotRequired[List[List[str]]]


class ProviderEndpointConfigurationTypeDef(TypedDict):
    marketplaceConfiguration: NotRequired[ProviderMarketplaceConfigurationTypeDef]


RuleUnionTypeDef = Union[RuleTypeDef, RuleOutputTypeDef]


class IdNamespaceIdMappingWorkflowPropertiesOutputTypeDef(TypedDict):
    idMappingType: IdMappingTypeType
    providerProperties: NotRequired[NamespaceProviderPropertiesOutputTypeDef]
    ruleBasedProperties: NotRequired[NamespaceRuleBasedPropertiesOutputTypeDef]


class ListIdNamespacesOutputTypeDef(TypedDict):
    idNamespaceSummaries: List[IdNamespaceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class IdMappingTechniquesOutputTypeDef(TypedDict):
    idMappingType: IdMappingTypeType
    providerProperties: NotRequired[ProviderPropertiesOutputTypeDef]
    ruleBasedProperties: NotRequired[IdMappingRuleBasedPropertiesOutputTypeDef]


class ResolutionTechniquesOutputTypeDef(TypedDict):
    resolutionType: ResolutionTypeType
    providerProperties: NotRequired[ProviderPropertiesOutputTypeDef]
    ruleBasedProperties: NotRequired[RuleBasedPropertiesOutputTypeDef]


ProviderPropertiesUnionTypeDef = Union[ProviderPropertiesTypeDef, ProviderPropertiesOutputTypeDef]
OutputSourceUnionTypeDef = Union[OutputSourceTypeDef, OutputSourceOutputTypeDef]


class GetProviderServiceOutputTypeDef(TypedDict):
    anonymizedOutput: bool
    providerComponentSchema: ProviderComponentSchemaTypeDef
    providerConfigurationDefinition: Dict[str, Any]
    providerEndpointConfiguration: ProviderEndpointConfigurationTypeDef
    providerEntityOutputDefinition: Dict[str, Any]
    providerIdNameSpaceConfiguration: ProviderIdNameSpaceConfigurationTypeDef
    providerIntermediateDataAccessConfiguration: ProviderIntermediateDataAccessConfigurationTypeDef
    providerJobConfiguration: Dict[str, Any]
    providerName: str
    providerServiceArn: str
    providerServiceDisplayName: str
    providerServiceName: str
    providerServiceType: ServiceTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class IdMappingRuleBasedPropertiesTypeDef(TypedDict):
    attributeMatchingModel: AttributeMatchingModelType
    recordMatchingModel: RecordMatchingModelType
    ruleDefinitionType: IdMappingWorkflowRuleDefinitionTypeType
    rules: NotRequired[Sequence[RuleUnionTypeDef]]


class NamespaceRuleBasedPropertiesTypeDef(TypedDict):
    attributeMatchingModel: NotRequired[AttributeMatchingModelType]
    recordMatchingModels: NotRequired[Sequence[RecordMatchingModelType]]
    ruleDefinitionTypes: NotRequired[Sequence[IdMappingWorkflowRuleDefinitionTypeType]]
    rules: NotRequired[Sequence[RuleUnionTypeDef]]


class RuleBasedPropertiesTypeDef(TypedDict):
    attributeMatchingModel: AttributeMatchingModelType
    rules: Sequence[RuleUnionTypeDef]
    matchPurpose: NotRequired[MatchPurposeType]


CreateIdNamespaceOutputTypeDef = TypedDict(
    "CreateIdNamespaceOutputTypeDef",
    {
        "createdAt": datetime,
        "description": str,
        "idMappingWorkflowProperties": List[IdNamespaceIdMappingWorkflowPropertiesOutputTypeDef],
        "idNamespaceArn": str,
        "idNamespaceName": str,
        "inputSourceConfig": List[IdNamespaceInputSourceTypeDef],
        "roleArn": str,
        "tags": Dict[str, str],
        "type": IdNamespaceTypeType,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetIdNamespaceOutputTypeDef = TypedDict(
    "GetIdNamespaceOutputTypeDef",
    {
        "createdAt": datetime,
        "description": str,
        "idMappingWorkflowProperties": List[IdNamespaceIdMappingWorkflowPropertiesOutputTypeDef],
        "idNamespaceArn": str,
        "idNamespaceName": str,
        "inputSourceConfig": List[IdNamespaceInputSourceTypeDef],
        "roleArn": str,
        "tags": Dict[str, str],
        "type": IdNamespaceTypeType,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateIdNamespaceOutputTypeDef = TypedDict(
    "UpdateIdNamespaceOutputTypeDef",
    {
        "createdAt": datetime,
        "description": str,
        "idMappingWorkflowProperties": List[IdNamespaceIdMappingWorkflowPropertiesOutputTypeDef],
        "idNamespaceArn": str,
        "idNamespaceName": str,
        "inputSourceConfig": List[IdNamespaceInputSourceTypeDef],
        "roleArn": str,
        "type": IdNamespaceTypeType,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreateIdMappingWorkflowOutputTypeDef(TypedDict):
    description: str
    idMappingTechniques: IdMappingTechniquesOutputTypeDef
    inputSourceConfig: List[IdMappingWorkflowInputSourceTypeDef]
    outputSourceConfig: List[IdMappingWorkflowOutputSourceTypeDef]
    roleArn: str
    workflowArn: str
    workflowName: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetIdMappingWorkflowOutputTypeDef(TypedDict):
    createdAt: datetime
    description: str
    idMappingTechniques: IdMappingTechniquesOutputTypeDef
    inputSourceConfig: List[IdMappingWorkflowInputSourceTypeDef]
    outputSourceConfig: List[IdMappingWorkflowOutputSourceTypeDef]
    roleArn: str
    tags: Dict[str, str]
    updatedAt: datetime
    workflowArn: str
    workflowName: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIdMappingWorkflowOutputTypeDef(TypedDict):
    description: str
    idMappingTechniques: IdMappingTechniquesOutputTypeDef
    inputSourceConfig: List[IdMappingWorkflowInputSourceTypeDef]
    outputSourceConfig: List[IdMappingWorkflowOutputSourceTypeDef]
    roleArn: str
    workflowArn: str
    workflowName: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMatchingWorkflowOutputTypeDef(TypedDict):
    description: str
    incrementalRunConfig: IncrementalRunConfigTypeDef
    inputSourceConfig: List[InputSourceTypeDef]
    outputSourceConfig: List[OutputSourceOutputTypeDef]
    resolutionTechniques: ResolutionTechniquesOutputTypeDef
    roleArn: str
    workflowArn: str
    workflowName: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetMatchingWorkflowOutputTypeDef(TypedDict):
    createdAt: datetime
    description: str
    incrementalRunConfig: IncrementalRunConfigTypeDef
    inputSourceConfig: List[InputSourceTypeDef]
    outputSourceConfig: List[OutputSourceOutputTypeDef]
    resolutionTechniques: ResolutionTechniquesOutputTypeDef
    roleArn: str
    tags: Dict[str, str]
    updatedAt: datetime
    workflowArn: str
    workflowName: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMatchingWorkflowOutputTypeDef(TypedDict):
    description: str
    incrementalRunConfig: IncrementalRunConfigTypeDef
    inputSourceConfig: List[InputSourceTypeDef]
    outputSourceConfig: List[OutputSourceOutputTypeDef]
    resolutionTechniques: ResolutionTechniquesOutputTypeDef
    roleArn: str
    workflowName: str
    ResponseMetadata: ResponseMetadataTypeDef


IdMappingRuleBasedPropertiesUnionTypeDef = Union[
    IdMappingRuleBasedPropertiesTypeDef, IdMappingRuleBasedPropertiesOutputTypeDef
]
NamespaceRuleBasedPropertiesUnionTypeDef = Union[
    NamespaceRuleBasedPropertiesTypeDef, NamespaceRuleBasedPropertiesOutputTypeDef
]
RuleBasedPropertiesUnionTypeDef = Union[
    RuleBasedPropertiesTypeDef, RuleBasedPropertiesOutputTypeDef
]


class IdMappingTechniquesTypeDef(TypedDict):
    idMappingType: IdMappingTypeType
    providerProperties: NotRequired[ProviderPropertiesUnionTypeDef]
    ruleBasedProperties: NotRequired[IdMappingRuleBasedPropertiesUnionTypeDef]


class IdNamespaceIdMappingWorkflowPropertiesTypeDef(TypedDict):
    idMappingType: IdMappingTypeType
    providerProperties: NotRequired[NamespaceProviderPropertiesUnionTypeDef]
    ruleBasedProperties: NotRequired[NamespaceRuleBasedPropertiesUnionTypeDef]


class ResolutionTechniquesTypeDef(TypedDict):
    resolutionType: ResolutionTypeType
    providerProperties: NotRequired[ProviderPropertiesUnionTypeDef]
    ruleBasedProperties: NotRequired[RuleBasedPropertiesUnionTypeDef]


class CreateIdMappingWorkflowInputRequestTypeDef(TypedDict):
    idMappingTechniques: IdMappingTechniquesTypeDef
    inputSourceConfig: Sequence[IdMappingWorkflowInputSourceTypeDef]
    workflowName: str
    description: NotRequired[str]
    outputSourceConfig: NotRequired[Sequence[IdMappingWorkflowOutputSourceTypeDef]]
    roleArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class UpdateIdMappingWorkflowInputRequestTypeDef(TypedDict):
    idMappingTechniques: IdMappingTechniquesTypeDef
    inputSourceConfig: Sequence[IdMappingWorkflowInputSourceTypeDef]
    workflowName: str
    description: NotRequired[str]
    outputSourceConfig: NotRequired[Sequence[IdMappingWorkflowOutputSourceTypeDef]]
    roleArn: NotRequired[str]


IdNamespaceIdMappingWorkflowPropertiesUnionTypeDef = Union[
    IdNamespaceIdMappingWorkflowPropertiesTypeDef,
    IdNamespaceIdMappingWorkflowPropertiesOutputTypeDef,
]


class UpdateIdNamespaceInputRequestTypeDef(TypedDict):
    idNamespaceName: str
    description: NotRequired[str]
    idMappingWorkflowProperties: NotRequired[
        Sequence[IdNamespaceIdMappingWorkflowPropertiesTypeDef]
    ]
    inputSourceConfig: NotRequired[Sequence[IdNamespaceInputSourceTypeDef]]
    roleArn: NotRequired[str]


class CreateMatchingWorkflowInputRequestTypeDef(TypedDict):
    inputSourceConfig: Sequence[InputSourceTypeDef]
    outputSourceConfig: Sequence[OutputSourceUnionTypeDef]
    resolutionTechniques: ResolutionTechniquesTypeDef
    roleArn: str
    workflowName: str
    description: NotRequired[str]
    incrementalRunConfig: NotRequired[IncrementalRunConfigTypeDef]
    tags: NotRequired[Mapping[str, str]]


class UpdateMatchingWorkflowInputRequestTypeDef(TypedDict):
    inputSourceConfig: Sequence[InputSourceTypeDef]
    outputSourceConfig: Sequence[OutputSourceTypeDef]
    resolutionTechniques: ResolutionTechniquesTypeDef
    roleArn: str
    workflowName: str
    description: NotRequired[str]
    incrementalRunConfig: NotRequired[IncrementalRunConfigTypeDef]


CreateIdNamespaceInputRequestTypeDef = TypedDict(
    "CreateIdNamespaceInputRequestTypeDef",
    {
        "idNamespaceName": str,
        "type": IdNamespaceTypeType,
        "description": NotRequired[str],
        "idMappingWorkflowProperties": NotRequired[
            Sequence[IdNamespaceIdMappingWorkflowPropertiesUnionTypeDef]
        ],
        "inputSourceConfig": NotRequired[Sequence[IdNamespaceInputSourceTypeDef]],
        "roleArn": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
