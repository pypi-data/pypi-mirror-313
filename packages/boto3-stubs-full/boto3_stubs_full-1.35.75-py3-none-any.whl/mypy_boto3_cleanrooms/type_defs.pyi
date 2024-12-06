"""
Type annotations for cleanrooms service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/type_defs/)

Usage::

    ```python
    from mypy_boto3_cleanrooms.type_defs import AggregateColumnOutputTypeDef

    data: AggregateColumnOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AdditionalAnalysesType,
    AggregateFunctionNameType,
    AnalysisRuleTypeType,
    AnalysisTemplateValidationStatusType,
    AnalysisTypeType,
    AnalyticsEngineType,
    CollaborationQueryLogStatusType,
    ConfiguredTableAnalysisRuleTypeType,
    ConfiguredTableAssociationAnalysisRuleTypeType,
    CustomMLMemberAbilityType,
    DifferentialPrivacyAggregationTypeType,
    FilterableMemberStatusType,
    IdNamespaceTypeType,
    JoinOperatorType,
    MemberAbilityType,
    MembershipQueryLogStatusType,
    MembershipStatusType,
    MemberStatusType,
    ParameterTypeType,
    PrivacyBudgetTemplateAutoRefreshType,
    ProtectedQueryStatusType,
    ResultFormatType,
    ScalarFunctionsType,
    SchemaStatusReasonCodeType,
    SchemaStatusType,
    SchemaTypeType,
    WorkerComputeTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AggregateColumnOutputTypeDef",
    "AggregateColumnTypeDef",
    "AggregateColumnUnionTypeDef",
    "AggregationConstraintTypeDef",
    "AnalysisParameterTypeDef",
    "AnalysisRuleAggregationOutputTypeDef",
    "AnalysisRuleAggregationTypeDef",
    "AnalysisRuleAggregationUnionTypeDef",
    "AnalysisRuleCustomOutputTypeDef",
    "AnalysisRuleCustomTypeDef",
    "AnalysisRuleCustomUnionTypeDef",
    "AnalysisRuleIdMappingTableTypeDef",
    "AnalysisRuleListOutputTypeDef",
    "AnalysisRuleListTypeDef",
    "AnalysisRuleListUnionTypeDef",
    "AnalysisRulePolicyTypeDef",
    "AnalysisRulePolicyV1TypeDef",
    "AnalysisRuleTypeDef",
    "AnalysisSchemaTypeDef",
    "AnalysisSourceTypeDef",
    "AnalysisTemplateSummaryTypeDef",
    "AnalysisTemplateTypeDef",
    "AnalysisTemplateValidationStatusDetailTypeDef",
    "AnalysisTemplateValidationStatusReasonTypeDef",
    "AthenaTableReferenceTypeDef",
    "BatchGetCollaborationAnalysisTemplateErrorTypeDef",
    "BatchGetCollaborationAnalysisTemplateInputRequestTypeDef",
    "BatchGetCollaborationAnalysisTemplateOutputTypeDef",
    "BatchGetSchemaAnalysisRuleErrorTypeDef",
    "BatchGetSchemaAnalysisRuleInputRequestTypeDef",
    "BatchGetSchemaAnalysisRuleOutputTypeDef",
    "BatchGetSchemaErrorTypeDef",
    "BatchGetSchemaInputRequestTypeDef",
    "BatchGetSchemaOutputTypeDef",
    "BilledResourceUtilizationTypeDef",
    "CollaborationAnalysisTemplateSummaryTypeDef",
    "CollaborationAnalysisTemplateTypeDef",
    "CollaborationConfiguredAudienceModelAssociationSummaryTypeDef",
    "CollaborationConfiguredAudienceModelAssociationTypeDef",
    "CollaborationIdNamespaceAssociationSummaryTypeDef",
    "CollaborationIdNamespaceAssociationTypeDef",
    "CollaborationPrivacyBudgetSummaryTypeDef",
    "CollaborationPrivacyBudgetTemplateSummaryTypeDef",
    "CollaborationPrivacyBudgetTemplateTypeDef",
    "CollaborationSummaryTypeDef",
    "CollaborationTypeDef",
    "ColumnTypeDef",
    "ComputeConfigurationTypeDef",
    "ConfigurationDetailsTypeDef",
    "ConfiguredAudienceModelAssociationSummaryTypeDef",
    "ConfiguredAudienceModelAssociationTypeDef",
    "ConfiguredTableAnalysisRulePolicyOutputTypeDef",
    "ConfiguredTableAnalysisRulePolicyTypeDef",
    "ConfiguredTableAnalysisRulePolicyV1OutputTypeDef",
    "ConfiguredTableAnalysisRulePolicyV1TypeDef",
    "ConfiguredTableAnalysisRulePolicyV1UnionTypeDef",
    "ConfiguredTableAnalysisRuleTypeDef",
    "ConfiguredTableAssociationAnalysisRuleAggregationOutputTypeDef",
    "ConfiguredTableAssociationAnalysisRuleAggregationTypeDef",
    "ConfiguredTableAssociationAnalysisRuleAggregationUnionTypeDef",
    "ConfiguredTableAssociationAnalysisRuleCustomOutputTypeDef",
    "ConfiguredTableAssociationAnalysisRuleCustomTypeDef",
    "ConfiguredTableAssociationAnalysisRuleCustomUnionTypeDef",
    "ConfiguredTableAssociationAnalysisRuleListOutputTypeDef",
    "ConfiguredTableAssociationAnalysisRuleListTypeDef",
    "ConfiguredTableAssociationAnalysisRuleListUnionTypeDef",
    "ConfiguredTableAssociationAnalysisRulePolicyOutputTypeDef",
    "ConfiguredTableAssociationAnalysisRulePolicyTypeDef",
    "ConfiguredTableAssociationAnalysisRulePolicyV1OutputTypeDef",
    "ConfiguredTableAssociationAnalysisRulePolicyV1TypeDef",
    "ConfiguredTableAssociationAnalysisRulePolicyV1UnionTypeDef",
    "ConfiguredTableAssociationAnalysisRuleTypeDef",
    "ConfiguredTableAssociationSummaryTypeDef",
    "ConfiguredTableAssociationTypeDef",
    "ConfiguredTableSummaryTypeDef",
    "ConfiguredTableTypeDef",
    "CreateAnalysisTemplateInputRequestTypeDef",
    "CreateAnalysisTemplateOutputTypeDef",
    "CreateCollaborationInputRequestTypeDef",
    "CreateCollaborationOutputTypeDef",
    "CreateConfiguredAudienceModelAssociationInputRequestTypeDef",
    "CreateConfiguredAudienceModelAssociationOutputTypeDef",
    "CreateConfiguredTableAnalysisRuleInputRequestTypeDef",
    "CreateConfiguredTableAnalysisRuleOutputTypeDef",
    "CreateConfiguredTableAssociationAnalysisRuleInputRequestTypeDef",
    "CreateConfiguredTableAssociationAnalysisRuleOutputTypeDef",
    "CreateConfiguredTableAssociationInputRequestTypeDef",
    "CreateConfiguredTableAssociationOutputTypeDef",
    "CreateConfiguredTableInputRequestTypeDef",
    "CreateConfiguredTableOutputTypeDef",
    "CreateIdMappingTableInputRequestTypeDef",
    "CreateIdMappingTableOutputTypeDef",
    "CreateIdNamespaceAssociationInputRequestTypeDef",
    "CreateIdNamespaceAssociationOutputTypeDef",
    "CreateMembershipInputRequestTypeDef",
    "CreateMembershipOutputTypeDef",
    "CreatePrivacyBudgetTemplateInputRequestTypeDef",
    "CreatePrivacyBudgetTemplateOutputTypeDef",
    "DataEncryptionMetadataTypeDef",
    "DeleteAnalysisTemplateInputRequestTypeDef",
    "DeleteCollaborationInputRequestTypeDef",
    "DeleteConfiguredAudienceModelAssociationInputRequestTypeDef",
    "DeleteConfiguredTableAnalysisRuleInputRequestTypeDef",
    "DeleteConfiguredTableAssociationAnalysisRuleInputRequestTypeDef",
    "DeleteConfiguredTableAssociationInputRequestTypeDef",
    "DeleteConfiguredTableInputRequestTypeDef",
    "DeleteIdMappingTableInputRequestTypeDef",
    "DeleteIdNamespaceAssociationInputRequestTypeDef",
    "DeleteMemberInputRequestTypeDef",
    "DeleteMembershipInputRequestTypeDef",
    "DeletePrivacyBudgetTemplateInputRequestTypeDef",
    "DifferentialPrivacyColumnTypeDef",
    "DifferentialPrivacyConfigurationOutputTypeDef",
    "DifferentialPrivacyConfigurationTypeDef",
    "DifferentialPrivacyConfigurationUnionTypeDef",
    "DifferentialPrivacyParametersTypeDef",
    "DifferentialPrivacyPreviewAggregationTypeDef",
    "DifferentialPrivacyPreviewParametersInputTypeDef",
    "DifferentialPrivacyPrivacyBudgetAggregationTypeDef",
    "DifferentialPrivacyPrivacyBudgetTypeDef",
    "DifferentialPrivacyPrivacyImpactTypeDef",
    "DifferentialPrivacySensitivityParametersTypeDef",
    "DifferentialPrivacyTemplateParametersInputTypeDef",
    "DifferentialPrivacyTemplateParametersOutputTypeDef",
    "DifferentialPrivacyTemplateUpdateParametersTypeDef",
    "DirectAnalysisConfigurationDetailsTypeDef",
    "GetAnalysisTemplateInputRequestTypeDef",
    "GetAnalysisTemplateOutputTypeDef",
    "GetCollaborationAnalysisTemplateInputRequestTypeDef",
    "GetCollaborationAnalysisTemplateOutputTypeDef",
    "GetCollaborationConfiguredAudienceModelAssociationInputRequestTypeDef",
    "GetCollaborationConfiguredAudienceModelAssociationOutputTypeDef",
    "GetCollaborationIdNamespaceAssociationInputRequestTypeDef",
    "GetCollaborationIdNamespaceAssociationOutputTypeDef",
    "GetCollaborationInputRequestTypeDef",
    "GetCollaborationOutputTypeDef",
    "GetCollaborationPrivacyBudgetTemplateInputRequestTypeDef",
    "GetCollaborationPrivacyBudgetTemplateOutputTypeDef",
    "GetConfiguredAudienceModelAssociationInputRequestTypeDef",
    "GetConfiguredAudienceModelAssociationOutputTypeDef",
    "GetConfiguredTableAnalysisRuleInputRequestTypeDef",
    "GetConfiguredTableAnalysisRuleOutputTypeDef",
    "GetConfiguredTableAssociationAnalysisRuleInputRequestTypeDef",
    "GetConfiguredTableAssociationAnalysisRuleOutputTypeDef",
    "GetConfiguredTableAssociationInputRequestTypeDef",
    "GetConfiguredTableAssociationOutputTypeDef",
    "GetConfiguredTableInputRequestTypeDef",
    "GetConfiguredTableOutputTypeDef",
    "GetIdMappingTableInputRequestTypeDef",
    "GetIdMappingTableOutputTypeDef",
    "GetIdNamespaceAssociationInputRequestTypeDef",
    "GetIdNamespaceAssociationOutputTypeDef",
    "GetMembershipInputRequestTypeDef",
    "GetMembershipOutputTypeDef",
    "GetPrivacyBudgetTemplateInputRequestTypeDef",
    "GetPrivacyBudgetTemplateOutputTypeDef",
    "GetProtectedQueryInputRequestTypeDef",
    "GetProtectedQueryOutputTypeDef",
    "GetSchemaAnalysisRuleInputRequestTypeDef",
    "GetSchemaAnalysisRuleOutputTypeDef",
    "GetSchemaInputRequestTypeDef",
    "GetSchemaOutputTypeDef",
    "GlueTableReferenceTypeDef",
    "IdMappingConfigTypeDef",
    "IdMappingTableInputReferenceConfigTypeDef",
    "IdMappingTableInputReferencePropertiesTypeDef",
    "IdMappingTableInputSourceTypeDef",
    "IdMappingTableSchemaTypePropertiesTypeDef",
    "IdMappingTableSummaryTypeDef",
    "IdMappingTableTypeDef",
    "IdNamespaceAssociationInputReferenceConfigTypeDef",
    "IdNamespaceAssociationInputReferencePropertiesSummaryTypeDef",
    "IdNamespaceAssociationInputReferencePropertiesTypeDef",
    "IdNamespaceAssociationSummaryTypeDef",
    "IdNamespaceAssociationTypeDef",
    "ListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef",
    "ListAnalysisTemplatesInputRequestTypeDef",
    "ListAnalysisTemplatesOutputTypeDef",
    "ListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef",
    "ListCollaborationAnalysisTemplatesInputRequestTypeDef",
    "ListCollaborationAnalysisTemplatesOutputTypeDef",
    "ListCollaborationConfiguredAudienceModelAssociationsInputListCollaborationConfiguredAudienceModelAssociationsPaginateTypeDef",
    "ListCollaborationConfiguredAudienceModelAssociationsInputRequestTypeDef",
    "ListCollaborationConfiguredAudienceModelAssociationsOutputTypeDef",
    "ListCollaborationIdNamespaceAssociationsInputListCollaborationIdNamespaceAssociationsPaginateTypeDef",
    "ListCollaborationIdNamespaceAssociationsInputRequestTypeDef",
    "ListCollaborationIdNamespaceAssociationsOutputTypeDef",
    "ListCollaborationPrivacyBudgetTemplatesInputListCollaborationPrivacyBudgetTemplatesPaginateTypeDef",
    "ListCollaborationPrivacyBudgetTemplatesInputRequestTypeDef",
    "ListCollaborationPrivacyBudgetTemplatesOutputTypeDef",
    "ListCollaborationPrivacyBudgetsInputListCollaborationPrivacyBudgetsPaginateTypeDef",
    "ListCollaborationPrivacyBudgetsInputRequestTypeDef",
    "ListCollaborationPrivacyBudgetsOutputTypeDef",
    "ListCollaborationsInputListCollaborationsPaginateTypeDef",
    "ListCollaborationsInputRequestTypeDef",
    "ListCollaborationsOutputTypeDef",
    "ListConfiguredAudienceModelAssociationsInputListConfiguredAudienceModelAssociationsPaginateTypeDef",
    "ListConfiguredAudienceModelAssociationsInputRequestTypeDef",
    "ListConfiguredAudienceModelAssociationsOutputTypeDef",
    "ListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef",
    "ListConfiguredTableAssociationsInputRequestTypeDef",
    "ListConfiguredTableAssociationsOutputTypeDef",
    "ListConfiguredTablesInputListConfiguredTablesPaginateTypeDef",
    "ListConfiguredTablesInputRequestTypeDef",
    "ListConfiguredTablesOutputTypeDef",
    "ListIdMappingTablesInputListIdMappingTablesPaginateTypeDef",
    "ListIdMappingTablesInputRequestTypeDef",
    "ListIdMappingTablesOutputTypeDef",
    "ListIdNamespaceAssociationsInputListIdNamespaceAssociationsPaginateTypeDef",
    "ListIdNamespaceAssociationsInputRequestTypeDef",
    "ListIdNamespaceAssociationsOutputTypeDef",
    "ListMembersInputListMembersPaginateTypeDef",
    "ListMembersInputRequestTypeDef",
    "ListMembersOutputTypeDef",
    "ListMembershipsInputListMembershipsPaginateTypeDef",
    "ListMembershipsInputRequestTypeDef",
    "ListMembershipsOutputTypeDef",
    "ListPrivacyBudgetTemplatesInputListPrivacyBudgetTemplatesPaginateTypeDef",
    "ListPrivacyBudgetTemplatesInputRequestTypeDef",
    "ListPrivacyBudgetTemplatesOutputTypeDef",
    "ListPrivacyBudgetsInputListPrivacyBudgetsPaginateTypeDef",
    "ListPrivacyBudgetsInputRequestTypeDef",
    "ListPrivacyBudgetsOutputTypeDef",
    "ListProtectedQueriesInputListProtectedQueriesPaginateTypeDef",
    "ListProtectedQueriesInputRequestTypeDef",
    "ListProtectedQueriesOutputTypeDef",
    "ListSchemasInputListSchemasPaginateTypeDef",
    "ListSchemasInputRequestTypeDef",
    "ListSchemasOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "MLMemberAbilitiesOutputTypeDef",
    "MLMemberAbilitiesTypeDef",
    "MLMemberAbilitiesUnionTypeDef",
    "MLPaymentConfigTypeDef",
    "MemberSpecificationTypeDef",
    "MemberSummaryTypeDef",
    "MembershipMLPaymentConfigTypeDef",
    "MembershipModelInferencePaymentConfigTypeDef",
    "MembershipModelTrainingPaymentConfigTypeDef",
    "MembershipPaymentConfigurationTypeDef",
    "MembershipProtectedQueryOutputConfigurationTypeDef",
    "MembershipProtectedQueryResultConfigurationTypeDef",
    "MembershipQueryComputePaymentConfigTypeDef",
    "MembershipSummaryTypeDef",
    "MembershipTypeDef",
    "ModelInferencePaymentConfigTypeDef",
    "ModelTrainingPaymentConfigTypeDef",
    "PaginatorConfigTypeDef",
    "PaymentConfigurationTypeDef",
    "PopulateIdMappingTableInputRequestTypeDef",
    "PopulateIdMappingTableOutputTypeDef",
    "PreviewPrivacyImpactInputRequestTypeDef",
    "PreviewPrivacyImpactOutputTypeDef",
    "PreviewPrivacyImpactParametersInputTypeDef",
    "PrivacyBudgetSummaryTypeDef",
    "PrivacyBudgetTemplateParametersInputTypeDef",
    "PrivacyBudgetTemplateParametersOutputTypeDef",
    "PrivacyBudgetTemplateSummaryTypeDef",
    "PrivacyBudgetTemplateTypeDef",
    "PrivacyBudgetTemplateUpdateParametersTypeDef",
    "PrivacyBudgetTypeDef",
    "PrivacyImpactTypeDef",
    "ProtectedQueryErrorTypeDef",
    "ProtectedQueryMemberOutputConfigurationTypeDef",
    "ProtectedQueryOutputConfigurationTypeDef",
    "ProtectedQueryOutputTypeDef",
    "ProtectedQueryResultConfigurationTypeDef",
    "ProtectedQueryResultTypeDef",
    "ProtectedQueryS3OutputConfigurationTypeDef",
    "ProtectedQueryS3OutputTypeDef",
    "ProtectedQuerySQLParametersOutputTypeDef",
    "ProtectedQuerySQLParametersTypeDef",
    "ProtectedQuerySingleMemberOutputTypeDef",
    "ProtectedQueryStatisticsTypeDef",
    "ProtectedQuerySummaryTypeDef",
    "ProtectedQueryTypeDef",
    "QueryComputePaymentConfigTypeDef",
    "QueryConstraintRequireOverlapTypeDef",
    "QueryConstraintTypeDef",
    "ReceiverConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "SchemaAnalysisRuleRequestTypeDef",
    "SchemaStatusDetailTypeDef",
    "SchemaStatusReasonTypeDef",
    "SchemaSummaryTypeDef",
    "SchemaTypeDef",
    "SchemaTypePropertiesTypeDef",
    "SnowflakeTableReferenceOutputTypeDef",
    "SnowflakeTableReferenceTypeDef",
    "SnowflakeTableReferenceUnionTypeDef",
    "SnowflakeTableSchemaOutputTypeDef",
    "SnowflakeTableSchemaTypeDef",
    "SnowflakeTableSchemaUnionTypeDef",
    "SnowflakeTableSchemaV1TypeDef",
    "StartProtectedQueryInputRequestTypeDef",
    "StartProtectedQueryOutputTypeDef",
    "TableReferenceOutputTypeDef",
    "TableReferenceTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateAnalysisTemplateInputRequestTypeDef",
    "UpdateAnalysisTemplateOutputTypeDef",
    "UpdateCollaborationInputRequestTypeDef",
    "UpdateCollaborationOutputTypeDef",
    "UpdateConfiguredAudienceModelAssociationInputRequestTypeDef",
    "UpdateConfiguredAudienceModelAssociationOutputTypeDef",
    "UpdateConfiguredTableAnalysisRuleInputRequestTypeDef",
    "UpdateConfiguredTableAnalysisRuleOutputTypeDef",
    "UpdateConfiguredTableAssociationAnalysisRuleInputRequestTypeDef",
    "UpdateConfiguredTableAssociationAnalysisRuleOutputTypeDef",
    "UpdateConfiguredTableAssociationInputRequestTypeDef",
    "UpdateConfiguredTableAssociationOutputTypeDef",
    "UpdateConfiguredTableInputRequestTypeDef",
    "UpdateConfiguredTableOutputTypeDef",
    "UpdateIdMappingTableInputRequestTypeDef",
    "UpdateIdMappingTableOutputTypeDef",
    "UpdateIdNamespaceAssociationInputRequestTypeDef",
    "UpdateIdNamespaceAssociationOutputTypeDef",
    "UpdateMembershipInputRequestTypeDef",
    "UpdateMembershipOutputTypeDef",
    "UpdatePrivacyBudgetTemplateInputRequestTypeDef",
    "UpdatePrivacyBudgetTemplateOutputTypeDef",
    "UpdateProtectedQueryInputRequestTypeDef",
    "UpdateProtectedQueryOutputTypeDef",
    "WorkerComputeConfigurationTypeDef",
)

class AggregateColumnOutputTypeDef(TypedDict):
    columnNames: List[str]
    function: AggregateFunctionNameType

class AggregateColumnTypeDef(TypedDict):
    columnNames: Sequence[str]
    function: AggregateFunctionNameType

AggregationConstraintTypeDef = TypedDict(
    "AggregationConstraintTypeDef",
    {
        "columnName": str,
        "minimum": int,
        "type": Literal["COUNT_DISTINCT"],
    },
)
AnalysisParameterTypeDef = TypedDict(
    "AnalysisParameterTypeDef",
    {
        "name": str,
        "type": ParameterTypeType,
        "defaultValue": NotRequired[str],
    },
)

class AnalysisRuleListOutputTypeDef(TypedDict):
    joinColumns: List[str]
    listColumns: List[str]
    allowedJoinOperators: NotRequired[List[JoinOperatorType]]
    additionalAnalyses: NotRequired[AdditionalAnalysesType]

class AnalysisRuleListTypeDef(TypedDict):
    joinColumns: Sequence[str]
    listColumns: Sequence[str]
    allowedJoinOperators: NotRequired[Sequence[JoinOperatorType]]
    additionalAnalyses: NotRequired[AdditionalAnalysesType]

class AnalysisSchemaTypeDef(TypedDict):
    referencedTables: NotRequired[List[str]]

class AnalysisSourceTypeDef(TypedDict):
    text: NotRequired[str]

AnalysisTemplateSummaryTypeDef = TypedDict(
    "AnalysisTemplateSummaryTypeDef",
    {
        "arn": str,
        "createTime": datetime,
        "id": str,
        "name": str,
        "updateTime": datetime,
        "membershipArn": str,
        "membershipId": str,
        "collaborationArn": str,
        "collaborationId": str,
        "description": NotRequired[str],
    },
)

class AnalysisTemplateValidationStatusReasonTypeDef(TypedDict):
    message: str

class AthenaTableReferenceTypeDef(TypedDict):
    workGroup: str
    databaseName: str
    tableName: str
    outputLocation: NotRequired[str]

class BatchGetCollaborationAnalysisTemplateErrorTypeDef(TypedDict):
    arn: str
    code: str
    message: str

class BatchGetCollaborationAnalysisTemplateInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    analysisTemplateArns: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

BatchGetSchemaAnalysisRuleErrorTypeDef = TypedDict(
    "BatchGetSchemaAnalysisRuleErrorTypeDef",
    {
        "name": str,
        "type": AnalysisRuleTypeType,
        "code": str,
        "message": str,
    },
)
SchemaAnalysisRuleRequestTypeDef = TypedDict(
    "SchemaAnalysisRuleRequestTypeDef",
    {
        "name": str,
        "type": AnalysisRuleTypeType,
    },
)

class BatchGetSchemaErrorTypeDef(TypedDict):
    name: str
    code: str
    message: str

class BatchGetSchemaInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    names: Sequence[str]

class BilledResourceUtilizationTypeDef(TypedDict):
    units: float

CollaborationAnalysisTemplateSummaryTypeDef = TypedDict(
    "CollaborationAnalysisTemplateSummaryTypeDef",
    {
        "arn": str,
        "createTime": datetime,
        "id": str,
        "name": str,
        "updateTime": datetime,
        "collaborationArn": str,
        "collaborationId": str,
        "creatorAccountId": str,
        "description": NotRequired[str],
    },
)
CollaborationConfiguredAudienceModelAssociationSummaryTypeDef = TypedDict(
    "CollaborationConfiguredAudienceModelAssociationSummaryTypeDef",
    {
        "arn": str,
        "createTime": datetime,
        "id": str,
        "name": str,
        "updateTime": datetime,
        "collaborationArn": str,
        "collaborationId": str,
        "creatorAccountId": str,
        "description": NotRequired[str],
    },
)
CollaborationConfiguredAudienceModelAssociationTypeDef = TypedDict(
    "CollaborationConfiguredAudienceModelAssociationTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "configuredAudienceModelArn": str,
        "name": str,
        "creatorAccountId": str,
        "createTime": datetime,
        "updateTime": datetime,
        "description": NotRequired[str],
    },
)

class IdNamespaceAssociationInputReferenceConfigTypeDef(TypedDict):
    inputReferenceArn: str
    manageResourcePolicies: bool

class IdNamespaceAssociationInputReferencePropertiesSummaryTypeDef(TypedDict):
    idNamespaceType: IdNamespaceTypeType

class IdMappingConfigTypeDef(TypedDict):
    allowUseAsDimensionColumn: bool

class IdNamespaceAssociationInputReferencePropertiesTypeDef(TypedDict):
    idNamespaceType: IdNamespaceTypeType
    idMappingWorkflowsSupported: List[Dict[str, Any]]

CollaborationPrivacyBudgetTemplateSummaryTypeDef = TypedDict(
    "CollaborationPrivacyBudgetTemplateSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "creatorAccountId": str,
        "privacyBudgetType": Literal["DIFFERENTIAL_PRIVACY"],
        "createTime": datetime,
        "updateTime": datetime,
    },
)
CollaborationSummaryTypeDef = TypedDict(
    "CollaborationSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "creatorAccountId": str,
        "creatorDisplayName": str,
        "createTime": datetime,
        "updateTime": datetime,
        "memberStatus": MemberStatusType,
        "membershipId": NotRequired[str],
        "membershipArn": NotRequired[str],
        "analyticsEngine": NotRequired[AnalyticsEngineType],
    },
)

class DataEncryptionMetadataTypeDef(TypedDict):
    allowCleartext: bool
    allowDuplicates: bool
    allowJoinsOnColumnsWithDifferentNames: bool
    preserveNulls: bool

ColumnTypeDef = TypedDict(
    "ColumnTypeDef",
    {
        "name": str,
        "type": str,
    },
)
WorkerComputeConfigurationTypeDef = TypedDict(
    "WorkerComputeConfigurationTypeDef",
    {
        "type": NotRequired[WorkerComputeTypeType],
        "number": NotRequired[int],
    },
)

class DirectAnalysisConfigurationDetailsTypeDef(TypedDict):
    receiverAccountIds: NotRequired[List[str]]

ConfiguredAudienceModelAssociationSummaryTypeDef = TypedDict(
    "ConfiguredAudienceModelAssociationSummaryTypeDef",
    {
        "membershipId": str,
        "membershipArn": str,
        "collaborationArn": str,
        "collaborationId": str,
        "createTime": datetime,
        "updateTime": datetime,
        "id": str,
        "arn": str,
        "name": str,
        "configuredAudienceModelArn": str,
        "description": NotRequired[str],
    },
)
ConfiguredAudienceModelAssociationTypeDef = TypedDict(
    "ConfiguredAudienceModelAssociationTypeDef",
    {
        "id": str,
        "arn": str,
        "configuredAudienceModelArn": str,
        "membershipId": str,
        "membershipArn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "name": str,
        "manageResourcePolicies": bool,
        "createTime": datetime,
        "updateTime": datetime,
        "description": NotRequired[str],
    },
)

class ConfiguredTableAssociationAnalysisRuleAggregationOutputTypeDef(TypedDict):
    allowedResultReceivers: NotRequired[List[str]]
    allowedAdditionalAnalyses: NotRequired[List[str]]

class ConfiguredTableAssociationAnalysisRuleAggregationTypeDef(TypedDict):
    allowedResultReceivers: NotRequired[Sequence[str]]
    allowedAdditionalAnalyses: NotRequired[Sequence[str]]

class ConfiguredTableAssociationAnalysisRuleCustomOutputTypeDef(TypedDict):
    allowedResultReceivers: NotRequired[List[str]]
    allowedAdditionalAnalyses: NotRequired[List[str]]

class ConfiguredTableAssociationAnalysisRuleCustomTypeDef(TypedDict):
    allowedResultReceivers: NotRequired[Sequence[str]]
    allowedAdditionalAnalyses: NotRequired[Sequence[str]]

class ConfiguredTableAssociationAnalysisRuleListOutputTypeDef(TypedDict):
    allowedResultReceivers: NotRequired[List[str]]
    allowedAdditionalAnalyses: NotRequired[List[str]]

class ConfiguredTableAssociationAnalysisRuleListTypeDef(TypedDict):
    allowedResultReceivers: NotRequired[Sequence[str]]
    allowedAdditionalAnalyses: NotRequired[Sequence[str]]

ConfiguredTableAssociationSummaryTypeDef = TypedDict(
    "ConfiguredTableAssociationSummaryTypeDef",
    {
        "configuredTableId": str,
        "membershipId": str,
        "membershipArn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "id": str,
        "arn": str,
    },
)
ConfiguredTableAssociationTypeDef = TypedDict(
    "ConfiguredTableAssociationTypeDef",
    {
        "arn": str,
        "id": str,
        "configuredTableId": str,
        "configuredTableArn": str,
        "membershipId": str,
        "membershipArn": str,
        "roleArn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "description": NotRequired[str],
        "analysisRuleTypes": NotRequired[List[ConfiguredTableAssociationAnalysisRuleTypeType]],
    },
)
ConfiguredTableSummaryTypeDef = TypedDict(
    "ConfiguredTableSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "analysisRuleTypes": List[ConfiguredTableAnalysisRuleTypeType],
        "analysisMethod": Literal["DIRECT_QUERY"],
    },
)

class MLMemberAbilitiesTypeDef(TypedDict):
    customMLMemberAbilities: Sequence[CustomMLMemberAbilityType]

class CreateConfiguredAudienceModelAssociationInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    configuredAudienceModelArn: str
    configuredAudienceModelAssociationName: str
    manageResourcePolicies: bool
    tags: NotRequired[Mapping[str, str]]
    description: NotRequired[str]

class CreateConfiguredTableAssociationInputRequestTypeDef(TypedDict):
    name: str
    membershipIdentifier: str
    configuredTableIdentifier: str
    roleArn: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class IdMappingTableInputReferenceConfigTypeDef(TypedDict):
    inputReferenceArn: str
    manageResourcePolicies: bool

class DeleteAnalysisTemplateInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    analysisTemplateIdentifier: str

class DeleteCollaborationInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str

class DeleteConfiguredAudienceModelAssociationInputRequestTypeDef(TypedDict):
    configuredAudienceModelAssociationIdentifier: str
    membershipIdentifier: str

class DeleteConfiguredTableAnalysisRuleInputRequestTypeDef(TypedDict):
    configuredTableIdentifier: str
    analysisRuleType: ConfiguredTableAnalysisRuleTypeType

class DeleteConfiguredTableAssociationAnalysisRuleInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    configuredTableAssociationIdentifier: str
    analysisRuleType: ConfiguredTableAssociationAnalysisRuleTypeType

class DeleteConfiguredTableAssociationInputRequestTypeDef(TypedDict):
    configuredTableAssociationIdentifier: str
    membershipIdentifier: str

class DeleteConfiguredTableInputRequestTypeDef(TypedDict):
    configuredTableIdentifier: str

class DeleteIdMappingTableInputRequestTypeDef(TypedDict):
    idMappingTableIdentifier: str
    membershipIdentifier: str

class DeleteIdNamespaceAssociationInputRequestTypeDef(TypedDict):
    idNamespaceAssociationIdentifier: str
    membershipIdentifier: str

class DeleteMemberInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    accountId: str

class DeleteMembershipInputRequestTypeDef(TypedDict):
    membershipIdentifier: str

class DeletePrivacyBudgetTemplateInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    privacyBudgetTemplateIdentifier: str

class DifferentialPrivacyColumnTypeDef(TypedDict):
    name: str

class DifferentialPrivacySensitivityParametersTypeDef(TypedDict):
    aggregationType: DifferentialPrivacyAggregationTypeType
    aggregationExpression: str
    userContributionLimit: int
    minColumnValue: NotRequired[float]
    maxColumnValue: NotRequired[float]

DifferentialPrivacyPreviewAggregationTypeDef = TypedDict(
    "DifferentialPrivacyPreviewAggregationTypeDef",
    {
        "type": DifferentialPrivacyAggregationTypeType,
        "maxCount": int,
    },
)

class DifferentialPrivacyPreviewParametersInputTypeDef(TypedDict):
    epsilon: int
    usersNoisePerQuery: int

DifferentialPrivacyPrivacyBudgetAggregationTypeDef = TypedDict(
    "DifferentialPrivacyPrivacyBudgetAggregationTypeDef",
    {
        "type": DifferentialPrivacyAggregationTypeType,
        "maxCount": int,
        "remainingCount": int,
    },
)

class DifferentialPrivacyTemplateParametersInputTypeDef(TypedDict):
    epsilon: int
    usersNoisePerQuery: int

class DifferentialPrivacyTemplateParametersOutputTypeDef(TypedDict):
    epsilon: int
    usersNoisePerQuery: int

class DifferentialPrivacyTemplateUpdateParametersTypeDef(TypedDict):
    epsilon: NotRequired[int]
    usersNoisePerQuery: NotRequired[int]

class GetAnalysisTemplateInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    analysisTemplateIdentifier: str

class GetCollaborationAnalysisTemplateInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    analysisTemplateArn: str

class GetCollaborationConfiguredAudienceModelAssociationInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    configuredAudienceModelAssociationIdentifier: str

class GetCollaborationIdNamespaceAssociationInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    idNamespaceAssociationIdentifier: str

class GetCollaborationInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str

class GetCollaborationPrivacyBudgetTemplateInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    privacyBudgetTemplateIdentifier: str

class GetConfiguredAudienceModelAssociationInputRequestTypeDef(TypedDict):
    configuredAudienceModelAssociationIdentifier: str
    membershipIdentifier: str

class GetConfiguredTableAnalysisRuleInputRequestTypeDef(TypedDict):
    configuredTableIdentifier: str
    analysisRuleType: ConfiguredTableAnalysisRuleTypeType

class GetConfiguredTableAssociationAnalysisRuleInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    configuredTableAssociationIdentifier: str
    analysisRuleType: ConfiguredTableAssociationAnalysisRuleTypeType

class GetConfiguredTableAssociationInputRequestTypeDef(TypedDict):
    configuredTableAssociationIdentifier: str
    membershipIdentifier: str

class GetConfiguredTableInputRequestTypeDef(TypedDict):
    configuredTableIdentifier: str

class GetIdMappingTableInputRequestTypeDef(TypedDict):
    idMappingTableIdentifier: str
    membershipIdentifier: str

class GetIdNamespaceAssociationInputRequestTypeDef(TypedDict):
    idNamespaceAssociationIdentifier: str
    membershipIdentifier: str

class GetMembershipInputRequestTypeDef(TypedDict):
    membershipIdentifier: str

class GetPrivacyBudgetTemplateInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    privacyBudgetTemplateIdentifier: str

class GetProtectedQueryInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    protectedQueryIdentifier: str

GetSchemaAnalysisRuleInputRequestTypeDef = TypedDict(
    "GetSchemaAnalysisRuleInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "name": str,
        "type": AnalysisRuleTypeType,
    },
)

class GetSchemaInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    name: str

class GlueTableReferenceTypeDef(TypedDict):
    tableName: str
    databaseName: str

IdMappingTableInputSourceTypeDef = TypedDict(
    "IdMappingTableInputSourceTypeDef",
    {
        "idNamespaceAssociationId": str,
        "type": IdNamespaceTypeType,
    },
)

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAnalysisTemplatesInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListCollaborationAnalysisTemplatesInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListCollaborationConfiguredAudienceModelAssociationsInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListCollaborationIdNamespaceAssociationsInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListCollaborationPrivacyBudgetTemplatesInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListCollaborationPrivacyBudgetsInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    privacyBudgetType: Literal["DIFFERENTIAL_PRIVACY"]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListCollaborationsInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    memberStatus: NotRequired[FilterableMemberStatusType]

class ListConfiguredAudienceModelAssociationsInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListConfiguredTableAssociationsInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListConfiguredTablesInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListIdMappingTablesInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListIdNamespaceAssociationsInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListMembersInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListMembershipsInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    status: NotRequired[MembershipStatusType]

class ListPrivacyBudgetTemplatesInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

PrivacyBudgetTemplateSummaryTypeDef = TypedDict(
    "PrivacyBudgetTemplateSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "membershipId": str,
        "membershipArn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "privacyBudgetType": Literal["DIFFERENTIAL_PRIVACY"],
        "createTime": datetime,
        "updateTime": datetime,
    },
)

class ListPrivacyBudgetsInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    privacyBudgetType: Literal["DIFFERENTIAL_PRIVACY"]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListProtectedQueriesInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    status: NotRequired[ProtectedQueryStatusType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListSchemasInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    schemaType: NotRequired[SchemaTypeType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

SchemaSummaryTypeDef = TypedDict(
    "SchemaSummaryTypeDef",
    {
        "name": str,
        "type": SchemaTypeType,
        "creatorAccountId": str,
        "createTime": datetime,
        "updateTime": datetime,
        "collaborationId": str,
        "collaborationArn": str,
        "analysisRuleTypes": List[AnalysisRuleTypeType],
        "analysisMethod": NotRequired[Literal["DIRECT_QUERY"]],
    },
)

class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str

class MLMemberAbilitiesOutputTypeDef(TypedDict):
    customMLMemberAbilities: List[CustomMLMemberAbilityType]

class ModelInferencePaymentConfigTypeDef(TypedDict):
    isResponsible: bool

class ModelTrainingPaymentConfigTypeDef(TypedDict):
    isResponsible: bool

class MembershipModelInferencePaymentConfigTypeDef(TypedDict):
    isResponsible: bool

class MembershipModelTrainingPaymentConfigTypeDef(TypedDict):
    isResponsible: bool

class MembershipQueryComputePaymentConfigTypeDef(TypedDict):
    isResponsible: bool

class ProtectedQueryS3OutputConfigurationTypeDef(TypedDict):
    resultFormat: ResultFormatType
    bucket: str
    keyPrefix: NotRequired[str]
    singleFileOutput: NotRequired[bool]

class QueryComputePaymentConfigTypeDef(TypedDict):
    isResponsible: bool

class PopulateIdMappingTableInputRequestTypeDef(TypedDict):
    idMappingTableIdentifier: str
    membershipIdentifier: str

class ProtectedQueryErrorTypeDef(TypedDict):
    message: str
    code: str

class ProtectedQueryMemberOutputConfigurationTypeDef(TypedDict):
    accountId: str

class ProtectedQueryS3OutputTypeDef(TypedDict):
    location: str

class ProtectedQuerySingleMemberOutputTypeDef(TypedDict):
    accountId: str

class ProtectedQuerySQLParametersOutputTypeDef(TypedDict):
    queryString: NotRequired[str]
    analysisTemplateArn: NotRequired[str]
    parameters: NotRequired[Dict[str, str]]

class ProtectedQuerySQLParametersTypeDef(TypedDict):
    queryString: NotRequired[str]
    analysisTemplateArn: NotRequired[str]
    parameters: NotRequired[Mapping[str, str]]

class QueryConstraintRequireOverlapTypeDef(TypedDict):
    columns: NotRequired[List[str]]

class SchemaStatusReasonTypeDef(TypedDict):
    code: SchemaStatusReasonCodeType
    message: str

class SnowflakeTableSchemaV1TypeDef(TypedDict):
    columnName: str
    columnType: str

class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateAnalysisTemplateInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    analysisTemplateIdentifier: str
    description: NotRequired[str]

class UpdateCollaborationInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    name: NotRequired[str]
    description: NotRequired[str]

class UpdateConfiguredAudienceModelAssociationInputRequestTypeDef(TypedDict):
    configuredAudienceModelAssociationIdentifier: str
    membershipIdentifier: str
    description: NotRequired[str]
    name: NotRequired[str]

class UpdateConfiguredTableAssociationInputRequestTypeDef(TypedDict):
    configuredTableAssociationIdentifier: str
    membershipIdentifier: str
    description: NotRequired[str]
    roleArn: NotRequired[str]

class UpdateConfiguredTableInputRequestTypeDef(TypedDict):
    configuredTableIdentifier: str
    name: NotRequired[str]
    description: NotRequired[str]

class UpdateIdMappingTableInputRequestTypeDef(TypedDict):
    idMappingTableIdentifier: str
    membershipIdentifier: str
    description: NotRequired[str]
    kmsKeyArn: NotRequired[str]

class UpdateProtectedQueryInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    protectedQueryIdentifier: str
    targetStatus: Literal["CANCELLED"]

AggregateColumnUnionTypeDef = Union[AggregateColumnTypeDef, AggregateColumnOutputTypeDef]

class AnalysisRuleAggregationOutputTypeDef(TypedDict):
    aggregateColumns: List[AggregateColumnOutputTypeDef]
    joinColumns: List[str]
    dimensionColumns: List[str]
    scalarFunctions: List[ScalarFunctionsType]
    outputConstraints: List[AggregationConstraintTypeDef]
    joinRequired: NotRequired[Literal["QUERY_RUNNER"]]
    allowedJoinOperators: NotRequired[List[JoinOperatorType]]
    additionalAnalyses: NotRequired[AdditionalAnalysesType]

AnalysisRuleListUnionTypeDef = Union[AnalysisRuleListTypeDef, AnalysisRuleListOutputTypeDef]
CreateAnalysisTemplateInputRequestTypeDef = TypedDict(
    "CreateAnalysisTemplateInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "name": str,
        "format": Literal["SQL"],
        "source": AnalysisSourceTypeDef,
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "analysisParameters": NotRequired[Sequence[AnalysisParameterTypeDef]],
    },
)
AnalysisTemplateValidationStatusDetailTypeDef = TypedDict(
    "AnalysisTemplateValidationStatusDetailTypeDef",
    {
        "type": Literal["DIFFERENTIAL_PRIVACY"],
        "status": AnalysisTemplateValidationStatusType,
        "reasons": NotRequired[List[AnalysisTemplateValidationStatusReasonTypeDef]],
    },
)

class ListAnalysisTemplatesOutputTypeDef(TypedDict):
    analysisTemplateSummaries: List[AnalysisTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PopulateIdMappingTableOutputTypeDef(TypedDict):
    idMappingJobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetSchemaAnalysisRuleInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    schemaAnalysisRuleRequests: Sequence[SchemaAnalysisRuleRequestTypeDef]

class ProtectedQueryStatisticsTypeDef(TypedDict):
    totalDurationInMillis: NotRequired[int]
    billedResourceUtilization: NotRequired[BilledResourceUtilizationTypeDef]

class ListCollaborationAnalysisTemplatesOutputTypeDef(TypedDict):
    collaborationAnalysisTemplateSummaries: List[CollaborationAnalysisTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListCollaborationConfiguredAudienceModelAssociationsOutputTypeDef(TypedDict):
    collaborationConfiguredAudienceModelAssociationSummaries: List[
        CollaborationConfiguredAudienceModelAssociationSummaryTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetCollaborationConfiguredAudienceModelAssociationOutputTypeDef(TypedDict):
    collaborationConfiguredAudienceModelAssociation: (
        CollaborationConfiguredAudienceModelAssociationTypeDef
    )
    ResponseMetadata: ResponseMetadataTypeDef

CollaborationIdNamespaceAssociationSummaryTypeDef = TypedDict(
    "CollaborationIdNamespaceAssociationSummaryTypeDef",
    {
        "arn": str,
        "createTime": datetime,
        "id": str,
        "updateTime": datetime,
        "collaborationArn": str,
        "collaborationId": str,
        "creatorAccountId": str,
        "inputReferenceConfig": IdNamespaceAssociationInputReferenceConfigTypeDef,
        "name": str,
        "inputReferenceProperties": IdNamespaceAssociationInputReferencePropertiesSummaryTypeDef,
        "description": NotRequired[str],
    },
)
IdNamespaceAssociationSummaryTypeDef = TypedDict(
    "IdNamespaceAssociationSummaryTypeDef",
    {
        "membershipId": str,
        "membershipArn": str,
        "collaborationArn": str,
        "collaborationId": str,
        "createTime": datetime,
        "updateTime": datetime,
        "id": str,
        "arn": str,
        "inputReferenceConfig": IdNamespaceAssociationInputReferenceConfigTypeDef,
        "name": str,
        "inputReferenceProperties": IdNamespaceAssociationInputReferencePropertiesSummaryTypeDef,
        "description": NotRequired[str],
    },
)

class CreateIdNamespaceAssociationInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    inputReferenceConfig: IdNamespaceAssociationInputReferenceConfigTypeDef
    name: str
    tags: NotRequired[Mapping[str, str]]
    description: NotRequired[str]
    idMappingConfig: NotRequired[IdMappingConfigTypeDef]

class UpdateIdNamespaceAssociationInputRequestTypeDef(TypedDict):
    idNamespaceAssociationIdentifier: str
    membershipIdentifier: str
    name: NotRequired[str]
    description: NotRequired[str]
    idMappingConfig: NotRequired[IdMappingConfigTypeDef]

CollaborationIdNamespaceAssociationTypeDef = TypedDict(
    "CollaborationIdNamespaceAssociationTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "name": str,
        "creatorAccountId": str,
        "createTime": datetime,
        "updateTime": datetime,
        "inputReferenceConfig": IdNamespaceAssociationInputReferenceConfigTypeDef,
        "inputReferenceProperties": IdNamespaceAssociationInputReferencePropertiesTypeDef,
        "description": NotRequired[str],
        "idMappingConfig": NotRequired[IdMappingConfigTypeDef],
    },
)
IdNamespaceAssociationTypeDef = TypedDict(
    "IdNamespaceAssociationTypeDef",
    {
        "id": str,
        "arn": str,
        "membershipId": str,
        "membershipArn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "inputReferenceConfig": IdNamespaceAssociationInputReferenceConfigTypeDef,
        "inputReferenceProperties": IdNamespaceAssociationInputReferencePropertiesTypeDef,
        "description": NotRequired[str],
        "idMappingConfig": NotRequired[IdMappingConfigTypeDef],
    },
)

class ListCollaborationPrivacyBudgetTemplatesOutputTypeDef(TypedDict):
    collaborationPrivacyBudgetTemplateSummaries: List[
        CollaborationPrivacyBudgetTemplateSummaryTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListCollaborationsOutputTypeDef(TypedDict):
    collaborationList: List[CollaborationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

CollaborationTypeDef = TypedDict(
    "CollaborationTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "creatorAccountId": str,
        "creatorDisplayName": str,
        "createTime": datetime,
        "updateTime": datetime,
        "memberStatus": MemberStatusType,
        "queryLogStatus": CollaborationQueryLogStatusType,
        "description": NotRequired[str],
        "membershipId": NotRequired[str],
        "membershipArn": NotRequired[str],
        "dataEncryptionMetadata": NotRequired[DataEncryptionMetadataTypeDef],
        "analyticsEngine": NotRequired[AnalyticsEngineType],
    },
)

class ComputeConfigurationTypeDef(TypedDict):
    worker: NotRequired[WorkerComputeConfigurationTypeDef]

class ConfigurationDetailsTypeDef(TypedDict):
    directAnalysisConfigurationDetails: NotRequired[DirectAnalysisConfigurationDetailsTypeDef]

class ListConfiguredAudienceModelAssociationsOutputTypeDef(TypedDict):
    configuredAudienceModelAssociationSummaries: List[
        ConfiguredAudienceModelAssociationSummaryTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateConfiguredAudienceModelAssociationOutputTypeDef(TypedDict):
    configuredAudienceModelAssociation: ConfiguredAudienceModelAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetConfiguredAudienceModelAssociationOutputTypeDef(TypedDict):
    configuredAudienceModelAssociation: ConfiguredAudienceModelAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConfiguredAudienceModelAssociationOutputTypeDef(TypedDict):
    configuredAudienceModelAssociation: ConfiguredAudienceModelAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ConfiguredTableAssociationAnalysisRuleAggregationUnionTypeDef = Union[
    ConfiguredTableAssociationAnalysisRuleAggregationTypeDef,
    ConfiguredTableAssociationAnalysisRuleAggregationOutputTypeDef,
]
ConfiguredTableAssociationAnalysisRuleCustomUnionTypeDef = Union[
    ConfiguredTableAssociationAnalysisRuleCustomTypeDef,
    ConfiguredTableAssociationAnalysisRuleCustomOutputTypeDef,
]
ConfiguredTableAssociationAnalysisRulePolicyV1OutputTypeDef = TypedDict(
    "ConfiguredTableAssociationAnalysisRulePolicyV1OutputTypeDef",
    {
        "list": NotRequired[ConfiguredTableAssociationAnalysisRuleListOutputTypeDef],
        "aggregation": NotRequired[ConfiguredTableAssociationAnalysisRuleAggregationOutputTypeDef],
        "custom": NotRequired[ConfiguredTableAssociationAnalysisRuleCustomOutputTypeDef],
    },
)
ConfiguredTableAssociationAnalysisRuleListUnionTypeDef = Union[
    ConfiguredTableAssociationAnalysisRuleListTypeDef,
    ConfiguredTableAssociationAnalysisRuleListOutputTypeDef,
]

class ListConfiguredTableAssociationsOutputTypeDef(TypedDict):
    configuredTableAssociationSummaries: List[ConfiguredTableAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateConfiguredTableAssociationOutputTypeDef(TypedDict):
    configuredTableAssociation: ConfiguredTableAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetConfiguredTableAssociationOutputTypeDef(TypedDict):
    configuredTableAssociation: ConfiguredTableAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConfiguredTableAssociationOutputTypeDef(TypedDict):
    configuredTableAssociation: ConfiguredTableAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListConfiguredTablesOutputTypeDef(TypedDict):
    configuredTableSummaries: List[ConfiguredTableSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateIdMappingTableInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    name: str
    inputReferenceConfig: IdMappingTableInputReferenceConfigTypeDef
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    kmsKeyArn: NotRequired[str]

IdMappingTableSummaryTypeDef = TypedDict(
    "IdMappingTableSummaryTypeDef",
    {
        "collaborationArn": str,
        "collaborationId": str,
        "membershipId": str,
        "membershipArn": str,
        "createTime": datetime,
        "updateTime": datetime,
        "id": str,
        "arn": str,
        "inputReferenceConfig": IdMappingTableInputReferenceConfigTypeDef,
        "name": str,
        "description": NotRequired[str],
    },
)

class DifferentialPrivacyConfigurationOutputTypeDef(TypedDict):
    columns: List[DifferentialPrivacyColumnTypeDef]

class DifferentialPrivacyConfigurationTypeDef(TypedDict):
    columns: Sequence[DifferentialPrivacyColumnTypeDef]

class DifferentialPrivacyParametersTypeDef(TypedDict):
    sensitivityParameters: List[DifferentialPrivacySensitivityParametersTypeDef]

class DifferentialPrivacyPrivacyImpactTypeDef(TypedDict):
    aggregations: List[DifferentialPrivacyPreviewAggregationTypeDef]

class PreviewPrivacyImpactParametersInputTypeDef(TypedDict):
    differentialPrivacy: NotRequired[DifferentialPrivacyPreviewParametersInputTypeDef]

class DifferentialPrivacyPrivacyBudgetTypeDef(TypedDict):
    aggregations: List[DifferentialPrivacyPrivacyBudgetAggregationTypeDef]
    epsilon: int

class PrivacyBudgetTemplateParametersInputTypeDef(TypedDict):
    differentialPrivacy: NotRequired[DifferentialPrivacyTemplateParametersInputTypeDef]

class PrivacyBudgetTemplateParametersOutputTypeDef(TypedDict):
    differentialPrivacy: NotRequired[DifferentialPrivacyTemplateParametersOutputTypeDef]

class PrivacyBudgetTemplateUpdateParametersTypeDef(TypedDict):
    differentialPrivacy: NotRequired[DifferentialPrivacyTemplateUpdateParametersTypeDef]

class IdMappingTableInputReferencePropertiesTypeDef(TypedDict):
    idMappingTableInputSource: List[IdMappingTableInputSourceTypeDef]

class IdMappingTableSchemaTypePropertiesTypeDef(TypedDict):
    idMappingTableInputSource: List[IdMappingTableInputSourceTypeDef]

class ListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef(TypedDict):
    membershipIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef(
    TypedDict
):
    collaborationIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCollaborationConfiguredAudienceModelAssociationsInputListCollaborationConfiguredAudienceModelAssociationsPaginateTypeDef(
    TypedDict
):
    collaborationIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCollaborationIdNamespaceAssociationsInputListCollaborationIdNamespaceAssociationsPaginateTypeDef(
    TypedDict
):
    collaborationIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCollaborationPrivacyBudgetTemplatesInputListCollaborationPrivacyBudgetTemplatesPaginateTypeDef(
    TypedDict
):
    collaborationIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCollaborationPrivacyBudgetsInputListCollaborationPrivacyBudgetsPaginateTypeDef(TypedDict):
    collaborationIdentifier: str
    privacyBudgetType: Literal["DIFFERENTIAL_PRIVACY"]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCollaborationsInputListCollaborationsPaginateTypeDef(TypedDict):
    memberStatus: NotRequired[FilterableMemberStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConfiguredAudienceModelAssociationsInputListConfiguredAudienceModelAssociationsPaginateTypeDef(
    TypedDict
):
    membershipIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef(TypedDict):
    membershipIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConfiguredTablesInputListConfiguredTablesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListIdMappingTablesInputListIdMappingTablesPaginateTypeDef(TypedDict):
    membershipIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListIdNamespaceAssociationsInputListIdNamespaceAssociationsPaginateTypeDef(TypedDict):
    membershipIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMembersInputListMembersPaginateTypeDef(TypedDict):
    collaborationIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMembershipsInputListMembershipsPaginateTypeDef(TypedDict):
    status: NotRequired[MembershipStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPrivacyBudgetTemplatesInputListPrivacyBudgetTemplatesPaginateTypeDef(TypedDict):
    membershipIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPrivacyBudgetsInputListPrivacyBudgetsPaginateTypeDef(TypedDict):
    membershipIdentifier: str
    privacyBudgetType: Literal["DIFFERENTIAL_PRIVACY"]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProtectedQueriesInputListProtectedQueriesPaginateTypeDef(TypedDict):
    membershipIdentifier: str
    status: NotRequired[ProtectedQueryStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSchemasInputListSchemasPaginateTypeDef(TypedDict):
    collaborationIdentifier: str
    schemaType: NotRequired[SchemaTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPrivacyBudgetTemplatesOutputTypeDef(TypedDict):
    privacyBudgetTemplateSummaries: List[PrivacyBudgetTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSchemasOutputTypeDef(TypedDict):
    schemaSummaries: List[SchemaSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

MLMemberAbilitiesUnionTypeDef = Union[MLMemberAbilitiesTypeDef, MLMemberAbilitiesOutputTypeDef]

class MLPaymentConfigTypeDef(TypedDict):
    modelTraining: NotRequired[ModelTrainingPaymentConfigTypeDef]
    modelInference: NotRequired[ModelInferencePaymentConfigTypeDef]

class MembershipMLPaymentConfigTypeDef(TypedDict):
    modelTraining: NotRequired[MembershipModelTrainingPaymentConfigTypeDef]
    modelInference: NotRequired[MembershipModelInferencePaymentConfigTypeDef]

class MembershipProtectedQueryOutputConfigurationTypeDef(TypedDict):
    s3: NotRequired[ProtectedQueryS3OutputConfigurationTypeDef]

class ProtectedQueryOutputConfigurationTypeDef(TypedDict):
    s3: NotRequired[ProtectedQueryS3OutputConfigurationTypeDef]
    member: NotRequired[ProtectedQueryMemberOutputConfigurationTypeDef]

class ProtectedQueryOutputTypeDef(TypedDict):
    s3: NotRequired[ProtectedQueryS3OutputTypeDef]
    memberList: NotRequired[List[ProtectedQuerySingleMemberOutputTypeDef]]

class QueryConstraintTypeDef(TypedDict):
    requireOverlap: NotRequired[QueryConstraintRequireOverlapTypeDef]

class SchemaStatusDetailTypeDef(TypedDict):
    status: SchemaStatusType
    analysisType: AnalysisTypeType
    reasons: NotRequired[List[SchemaStatusReasonTypeDef]]
    analysisRuleType: NotRequired[AnalysisRuleTypeType]
    configurations: NotRequired[List[Literal["DIFFERENTIAL_PRIVACY"]]]

class SnowflakeTableSchemaOutputTypeDef(TypedDict):
    v1: NotRequired[List[SnowflakeTableSchemaV1TypeDef]]

class SnowflakeTableSchemaTypeDef(TypedDict):
    v1: NotRequired[Sequence[SnowflakeTableSchemaV1TypeDef]]

class AnalysisRuleAggregationTypeDef(TypedDict):
    aggregateColumns: Sequence[AggregateColumnUnionTypeDef]
    joinColumns: Sequence[str]
    dimensionColumns: Sequence[str]
    scalarFunctions: Sequence[ScalarFunctionsType]
    outputConstraints: Sequence[AggregationConstraintTypeDef]
    joinRequired: NotRequired[Literal["QUERY_RUNNER"]]
    allowedJoinOperators: NotRequired[Sequence[JoinOperatorType]]
    additionalAnalyses: NotRequired[AdditionalAnalysesType]

AnalysisTemplateTypeDef = TypedDict(
    "AnalysisTemplateTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "membershipId": str,
        "membershipArn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "schema": AnalysisSchemaTypeDef,
        "format": Literal["SQL"],
        "source": AnalysisSourceTypeDef,
        "description": NotRequired[str],
        "analysisParameters": NotRequired[List[AnalysisParameterTypeDef]],
        "validations": NotRequired[List[AnalysisTemplateValidationStatusDetailTypeDef]],
    },
)
CollaborationAnalysisTemplateTypeDef = TypedDict(
    "CollaborationAnalysisTemplateTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "creatorAccountId": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "schema": AnalysisSchemaTypeDef,
        "format": Literal["SQL"],
        "source": AnalysisSourceTypeDef,
        "description": NotRequired[str],
        "analysisParameters": NotRequired[List[AnalysisParameterTypeDef]],
        "validations": NotRequired[List[AnalysisTemplateValidationStatusDetailTypeDef]],
    },
)

class ListCollaborationIdNamespaceAssociationsOutputTypeDef(TypedDict):
    collaborationIdNamespaceAssociationSummaries: List[
        CollaborationIdNamespaceAssociationSummaryTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListIdNamespaceAssociationsOutputTypeDef(TypedDict):
    idNamespaceAssociationSummaries: List[IdNamespaceAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetCollaborationIdNamespaceAssociationOutputTypeDef(TypedDict):
    collaborationIdNamespaceAssociation: CollaborationIdNamespaceAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateIdNamespaceAssociationOutputTypeDef(TypedDict):
    idNamespaceAssociation: IdNamespaceAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetIdNamespaceAssociationOutputTypeDef(TypedDict):
    idNamespaceAssociation: IdNamespaceAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateIdNamespaceAssociationOutputTypeDef(TypedDict):
    idNamespaceAssociation: IdNamespaceAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCollaborationOutputTypeDef(TypedDict):
    collaboration: CollaborationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetCollaborationOutputTypeDef(TypedDict):
    collaboration: CollaborationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCollaborationOutputTypeDef(TypedDict):
    collaboration: CollaborationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ReceiverConfigurationTypeDef(TypedDict):
    analysisType: AnalysisTypeType
    configurationDetails: NotRequired[ConfigurationDetailsTypeDef]

class ConfiguredTableAssociationAnalysisRulePolicyOutputTypeDef(TypedDict):
    v1: NotRequired[ConfiguredTableAssociationAnalysisRulePolicyV1OutputTypeDef]

ConfiguredTableAssociationAnalysisRulePolicyV1TypeDef = TypedDict(
    "ConfiguredTableAssociationAnalysisRulePolicyV1TypeDef",
    {
        "list": NotRequired[ConfiguredTableAssociationAnalysisRuleListUnionTypeDef],
        "aggregation": NotRequired[ConfiguredTableAssociationAnalysisRuleAggregationUnionTypeDef],
        "custom": NotRequired[ConfiguredTableAssociationAnalysisRuleCustomUnionTypeDef],
    },
)

class ListIdMappingTablesOutputTypeDef(TypedDict):
    idMappingTableSummaries: List[IdMappingTableSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AnalysisRuleCustomOutputTypeDef(TypedDict):
    allowedAnalyses: List[str]
    allowedAnalysisProviders: NotRequired[List[str]]
    additionalAnalyses: NotRequired[AdditionalAnalysesType]
    disallowedOutputColumns: NotRequired[List[str]]
    differentialPrivacy: NotRequired[DifferentialPrivacyConfigurationOutputTypeDef]

DifferentialPrivacyConfigurationUnionTypeDef = Union[
    DifferentialPrivacyConfigurationTypeDef, DifferentialPrivacyConfigurationOutputTypeDef
]

class PrivacyImpactTypeDef(TypedDict):
    differentialPrivacy: NotRequired[DifferentialPrivacyPrivacyImpactTypeDef]

class PreviewPrivacyImpactInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    parameters: PreviewPrivacyImpactParametersInputTypeDef

class PrivacyBudgetTypeDef(TypedDict):
    differentialPrivacy: NotRequired[DifferentialPrivacyPrivacyBudgetTypeDef]

class CreatePrivacyBudgetTemplateInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    autoRefresh: PrivacyBudgetTemplateAutoRefreshType
    privacyBudgetType: Literal["DIFFERENTIAL_PRIVACY"]
    parameters: PrivacyBudgetTemplateParametersInputTypeDef
    tags: NotRequired[Mapping[str, str]]

CollaborationPrivacyBudgetTemplateTypeDef = TypedDict(
    "CollaborationPrivacyBudgetTemplateTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "creatorAccountId": str,
        "createTime": datetime,
        "updateTime": datetime,
        "privacyBudgetType": Literal["DIFFERENTIAL_PRIVACY"],
        "autoRefresh": PrivacyBudgetTemplateAutoRefreshType,
        "parameters": PrivacyBudgetTemplateParametersOutputTypeDef,
    },
)
PrivacyBudgetTemplateTypeDef = TypedDict(
    "PrivacyBudgetTemplateTypeDef",
    {
        "id": str,
        "arn": str,
        "membershipId": str,
        "membershipArn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "createTime": datetime,
        "updateTime": datetime,
        "privacyBudgetType": Literal["DIFFERENTIAL_PRIVACY"],
        "autoRefresh": PrivacyBudgetTemplateAutoRefreshType,
        "parameters": PrivacyBudgetTemplateParametersOutputTypeDef,
    },
)

class UpdatePrivacyBudgetTemplateInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    privacyBudgetTemplateIdentifier: str
    privacyBudgetType: Literal["DIFFERENTIAL_PRIVACY"]
    parameters: NotRequired[PrivacyBudgetTemplateUpdateParametersTypeDef]

IdMappingTableTypeDef = TypedDict(
    "IdMappingTableTypeDef",
    {
        "id": str,
        "arn": str,
        "inputReferenceConfig": IdMappingTableInputReferenceConfigTypeDef,
        "membershipId": str,
        "membershipArn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "inputReferenceProperties": IdMappingTableInputReferencePropertiesTypeDef,
        "description": NotRequired[str],
        "kmsKeyArn": NotRequired[str],
    },
)

class SchemaTypePropertiesTypeDef(TypedDict):
    idMappingTable: NotRequired[IdMappingTableSchemaTypePropertiesTypeDef]

class PaymentConfigurationTypeDef(TypedDict):
    queryCompute: QueryComputePaymentConfigTypeDef
    machineLearning: NotRequired[MLPaymentConfigTypeDef]

class MembershipPaymentConfigurationTypeDef(TypedDict):
    queryCompute: MembershipQueryComputePaymentConfigTypeDef
    machineLearning: NotRequired[MembershipMLPaymentConfigTypeDef]

class MembershipProtectedQueryResultConfigurationTypeDef(TypedDict):
    outputConfiguration: MembershipProtectedQueryOutputConfigurationTypeDef
    roleArn: NotRequired[str]

class ProtectedQueryResultConfigurationTypeDef(TypedDict):
    outputConfiguration: ProtectedQueryOutputConfigurationTypeDef

class ProtectedQueryResultTypeDef(TypedDict):
    output: ProtectedQueryOutputTypeDef

class AnalysisRuleIdMappingTableTypeDef(TypedDict):
    joinColumns: List[str]
    queryConstraints: List[QueryConstraintTypeDef]
    dimensionColumns: NotRequired[List[str]]

class SnowflakeTableReferenceOutputTypeDef(TypedDict):
    secretArn: str
    accountIdentifier: str
    databaseName: str
    tableName: str
    schemaName: str
    tableSchema: SnowflakeTableSchemaOutputTypeDef

SnowflakeTableSchemaUnionTypeDef = Union[
    SnowflakeTableSchemaTypeDef, SnowflakeTableSchemaOutputTypeDef
]
AnalysisRuleAggregationUnionTypeDef = Union[
    AnalysisRuleAggregationTypeDef, AnalysisRuleAggregationOutputTypeDef
]

class CreateAnalysisTemplateOutputTypeDef(TypedDict):
    analysisTemplate: AnalysisTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAnalysisTemplateOutputTypeDef(TypedDict):
    analysisTemplate: AnalysisTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAnalysisTemplateOutputTypeDef(TypedDict):
    analysisTemplate: AnalysisTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetCollaborationAnalysisTemplateOutputTypeDef(TypedDict):
    collaborationAnalysisTemplates: List[CollaborationAnalysisTemplateTypeDef]
    errors: List[BatchGetCollaborationAnalysisTemplateErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetCollaborationAnalysisTemplateOutputTypeDef(TypedDict):
    collaborationAnalysisTemplate: CollaborationAnalysisTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ProtectedQuerySummaryTypeDef = TypedDict(
    "ProtectedQuerySummaryTypeDef",
    {
        "id": str,
        "membershipId": str,
        "membershipArn": str,
        "createTime": datetime,
        "status": ProtectedQueryStatusType,
        "receiverConfigurations": List[ReceiverConfigurationTypeDef],
    },
)
ConfiguredTableAssociationAnalysisRuleTypeDef = TypedDict(
    "ConfiguredTableAssociationAnalysisRuleTypeDef",
    {
        "membershipIdentifier": str,
        "configuredTableAssociationId": str,
        "configuredTableAssociationArn": str,
        "policy": ConfiguredTableAssociationAnalysisRulePolicyOutputTypeDef,
        "type": ConfiguredTableAssociationAnalysisRuleTypeType,
        "createTime": datetime,
        "updateTime": datetime,
    },
)
ConfiguredTableAssociationAnalysisRulePolicyV1UnionTypeDef = Union[
    ConfiguredTableAssociationAnalysisRulePolicyV1TypeDef,
    ConfiguredTableAssociationAnalysisRulePolicyV1OutputTypeDef,
]
ConfiguredTableAnalysisRulePolicyV1OutputTypeDef = TypedDict(
    "ConfiguredTableAnalysisRulePolicyV1OutputTypeDef",
    {
        "list": NotRequired[AnalysisRuleListOutputTypeDef],
        "aggregation": NotRequired[AnalysisRuleAggregationOutputTypeDef],
        "custom": NotRequired[AnalysisRuleCustomOutputTypeDef],
    },
)

class AnalysisRuleCustomTypeDef(TypedDict):
    allowedAnalyses: Sequence[str]
    allowedAnalysisProviders: NotRequired[Sequence[str]]
    additionalAnalyses: NotRequired[AdditionalAnalysesType]
    disallowedOutputColumns: NotRequired[Sequence[str]]
    differentialPrivacy: NotRequired[DifferentialPrivacyConfigurationUnionTypeDef]

class PreviewPrivacyImpactOutputTypeDef(TypedDict):
    privacyImpact: PrivacyImpactTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

CollaborationPrivacyBudgetSummaryTypeDef = TypedDict(
    "CollaborationPrivacyBudgetSummaryTypeDef",
    {
        "id": str,
        "privacyBudgetTemplateId": str,
        "privacyBudgetTemplateArn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "creatorAccountId": str,
        "type": Literal["DIFFERENTIAL_PRIVACY"],
        "createTime": datetime,
        "updateTime": datetime,
        "budget": PrivacyBudgetTypeDef,
    },
)
PrivacyBudgetSummaryTypeDef = TypedDict(
    "PrivacyBudgetSummaryTypeDef",
    {
        "id": str,
        "privacyBudgetTemplateId": str,
        "privacyBudgetTemplateArn": str,
        "membershipId": str,
        "membershipArn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "type": Literal["DIFFERENTIAL_PRIVACY"],
        "createTime": datetime,
        "updateTime": datetime,
        "budget": PrivacyBudgetTypeDef,
    },
)

class GetCollaborationPrivacyBudgetTemplateOutputTypeDef(TypedDict):
    collaborationPrivacyBudgetTemplate: CollaborationPrivacyBudgetTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePrivacyBudgetTemplateOutputTypeDef(TypedDict):
    privacyBudgetTemplate: PrivacyBudgetTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetPrivacyBudgetTemplateOutputTypeDef(TypedDict):
    privacyBudgetTemplate: PrivacyBudgetTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePrivacyBudgetTemplateOutputTypeDef(TypedDict):
    privacyBudgetTemplate: PrivacyBudgetTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateIdMappingTableOutputTypeDef(TypedDict):
    idMappingTable: IdMappingTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetIdMappingTableOutputTypeDef(TypedDict):
    idMappingTable: IdMappingTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateIdMappingTableOutputTypeDef(TypedDict):
    idMappingTable: IdMappingTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

SchemaTypeDef = TypedDict(
    "SchemaTypeDef",
    {
        "columns": List[ColumnTypeDef],
        "partitionKeys": List[ColumnTypeDef],
        "analysisRuleTypes": List[AnalysisRuleTypeType],
        "creatorAccountId": str,
        "name": str,
        "collaborationId": str,
        "collaborationArn": str,
        "description": str,
        "createTime": datetime,
        "updateTime": datetime,
        "type": SchemaTypeType,
        "schemaStatusDetails": List[SchemaStatusDetailTypeDef],
        "analysisMethod": NotRequired[Literal["DIRECT_QUERY"]],
        "schemaTypeProperties": NotRequired[SchemaTypePropertiesTypeDef],
    },
)

class MemberSpecificationTypeDef(TypedDict):
    accountId: str
    memberAbilities: Sequence[MemberAbilityType]
    displayName: str
    mlMemberAbilities: NotRequired[MLMemberAbilitiesUnionTypeDef]
    paymentConfiguration: NotRequired[PaymentConfigurationTypeDef]

class MemberSummaryTypeDef(TypedDict):
    accountId: str
    status: MemberStatusType
    displayName: str
    abilities: List[MemberAbilityType]
    createTime: datetime
    updateTime: datetime
    paymentConfiguration: PaymentConfigurationTypeDef
    mlAbilities: NotRequired[MLMemberAbilitiesOutputTypeDef]
    membershipId: NotRequired[str]
    membershipArn: NotRequired[str]

MembershipSummaryTypeDef = TypedDict(
    "MembershipSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationArn": str,
        "collaborationId": str,
        "collaborationCreatorAccountId": str,
        "collaborationCreatorDisplayName": str,
        "collaborationName": str,
        "createTime": datetime,
        "updateTime": datetime,
        "status": MembershipStatusType,
        "memberAbilities": List[MemberAbilityType],
        "paymentConfiguration": MembershipPaymentConfigurationTypeDef,
        "mlMemberAbilities": NotRequired[MLMemberAbilitiesOutputTypeDef],
    },
)

class CreateMembershipInputRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    queryLogStatus: MembershipQueryLogStatusType
    tags: NotRequired[Mapping[str, str]]
    defaultResultConfiguration: NotRequired[MembershipProtectedQueryResultConfigurationTypeDef]
    paymentConfiguration: NotRequired[MembershipPaymentConfigurationTypeDef]

MembershipTypeDef = TypedDict(
    "MembershipTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationArn": str,
        "collaborationId": str,
        "collaborationCreatorAccountId": str,
        "collaborationCreatorDisplayName": str,
        "collaborationName": str,
        "createTime": datetime,
        "updateTime": datetime,
        "status": MembershipStatusType,
        "memberAbilities": List[MemberAbilityType],
        "queryLogStatus": MembershipQueryLogStatusType,
        "paymentConfiguration": MembershipPaymentConfigurationTypeDef,
        "mlMemberAbilities": NotRequired[MLMemberAbilitiesOutputTypeDef],
        "defaultResultConfiguration": NotRequired[
            MembershipProtectedQueryResultConfigurationTypeDef
        ],
    },
)

class UpdateMembershipInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    queryLogStatus: NotRequired[MembershipQueryLogStatusType]
    defaultResultConfiguration: NotRequired[MembershipProtectedQueryResultConfigurationTypeDef]

StartProtectedQueryInputRequestTypeDef = TypedDict(
    "StartProtectedQueryInputRequestTypeDef",
    {
        "type": Literal["SQL"],
        "membershipIdentifier": str,
        "sqlParameters": ProtectedQuerySQLParametersTypeDef,
        "resultConfiguration": NotRequired[ProtectedQueryResultConfigurationTypeDef],
        "computeConfiguration": NotRequired[ComputeConfigurationTypeDef],
    },
)
ProtectedQueryTypeDef = TypedDict(
    "ProtectedQueryTypeDef",
    {
        "id": str,
        "membershipId": str,
        "membershipArn": str,
        "createTime": datetime,
        "status": ProtectedQueryStatusType,
        "sqlParameters": NotRequired[ProtectedQuerySQLParametersOutputTypeDef],
        "resultConfiguration": NotRequired[ProtectedQueryResultConfigurationTypeDef],
        "statistics": NotRequired[ProtectedQueryStatisticsTypeDef],
        "result": NotRequired[ProtectedQueryResultTypeDef],
        "error": NotRequired[ProtectedQueryErrorTypeDef],
        "differentialPrivacy": NotRequired[DifferentialPrivacyParametersTypeDef],
        "computeConfiguration": NotRequired[ComputeConfigurationTypeDef],
    },
)
AnalysisRulePolicyV1TypeDef = TypedDict(
    "AnalysisRulePolicyV1TypeDef",
    {
        "list": NotRequired[AnalysisRuleListOutputTypeDef],
        "aggregation": NotRequired[AnalysisRuleAggregationOutputTypeDef],
        "custom": NotRequired[AnalysisRuleCustomOutputTypeDef],
        "idMappingTable": NotRequired[AnalysisRuleIdMappingTableTypeDef],
    },
)

class TableReferenceOutputTypeDef(TypedDict):
    glue: NotRequired[GlueTableReferenceTypeDef]
    snowflake: NotRequired[SnowflakeTableReferenceOutputTypeDef]
    athena: NotRequired[AthenaTableReferenceTypeDef]

class SnowflakeTableReferenceTypeDef(TypedDict):
    secretArn: str
    accountIdentifier: str
    databaseName: str
    tableName: str
    schemaName: str
    tableSchema: SnowflakeTableSchemaUnionTypeDef

class ListProtectedQueriesOutputTypeDef(TypedDict):
    protectedQueries: List[ProtectedQuerySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateConfiguredTableAssociationAnalysisRuleOutputTypeDef(TypedDict):
    analysisRule: ConfiguredTableAssociationAnalysisRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetConfiguredTableAssociationAnalysisRuleOutputTypeDef(TypedDict):
    analysisRule: ConfiguredTableAssociationAnalysisRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConfiguredTableAssociationAnalysisRuleOutputTypeDef(TypedDict):
    analysisRule: ConfiguredTableAssociationAnalysisRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ConfiguredTableAssociationAnalysisRulePolicyTypeDef(TypedDict):
    v1: NotRequired[ConfiguredTableAssociationAnalysisRulePolicyV1UnionTypeDef]

class ConfiguredTableAnalysisRulePolicyOutputTypeDef(TypedDict):
    v1: NotRequired[ConfiguredTableAnalysisRulePolicyV1OutputTypeDef]

AnalysisRuleCustomUnionTypeDef = Union[AnalysisRuleCustomTypeDef, AnalysisRuleCustomOutputTypeDef]

class ListCollaborationPrivacyBudgetsOutputTypeDef(TypedDict):
    collaborationPrivacyBudgetSummaries: List[CollaborationPrivacyBudgetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPrivacyBudgetsOutputTypeDef(TypedDict):
    privacyBudgetSummaries: List[PrivacyBudgetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchGetSchemaOutputTypeDef(TypedDict):
    schemas: List[SchemaTypeDef]
    errors: List[BatchGetSchemaErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetSchemaOutputTypeDef(TypedDict):
    schema: SchemaTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCollaborationInputRequestTypeDef(TypedDict):
    members: Sequence[MemberSpecificationTypeDef]
    name: str
    description: str
    creatorMemberAbilities: Sequence[MemberAbilityType]
    creatorDisplayName: str
    queryLogStatus: CollaborationQueryLogStatusType
    creatorMLMemberAbilities: NotRequired[MLMemberAbilitiesTypeDef]
    dataEncryptionMetadata: NotRequired[DataEncryptionMetadataTypeDef]
    tags: NotRequired[Mapping[str, str]]
    creatorPaymentConfiguration: NotRequired[PaymentConfigurationTypeDef]
    analyticsEngine: NotRequired[AnalyticsEngineType]

class ListMembersOutputTypeDef(TypedDict):
    memberSummaries: List[MemberSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListMembershipsOutputTypeDef(TypedDict):
    membershipSummaries: List[MembershipSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateMembershipOutputTypeDef(TypedDict):
    membership: MembershipTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetMembershipOutputTypeDef(TypedDict):
    membership: MembershipTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMembershipOutputTypeDef(TypedDict):
    membership: MembershipTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetProtectedQueryOutputTypeDef(TypedDict):
    protectedQuery: ProtectedQueryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartProtectedQueryOutputTypeDef(TypedDict):
    protectedQuery: ProtectedQueryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProtectedQueryOutputTypeDef(TypedDict):
    protectedQuery: ProtectedQueryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AnalysisRulePolicyTypeDef(TypedDict):
    v1: NotRequired[AnalysisRulePolicyV1TypeDef]

ConfiguredTableTypeDef = TypedDict(
    "ConfiguredTableTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "tableReference": TableReferenceOutputTypeDef,
        "createTime": datetime,
        "updateTime": datetime,
        "analysisRuleTypes": List[ConfiguredTableAnalysisRuleTypeType],
        "analysisMethod": Literal["DIRECT_QUERY"],
        "allowedColumns": List[str],
        "description": NotRequired[str],
    },
)
SnowflakeTableReferenceUnionTypeDef = Union[
    SnowflakeTableReferenceTypeDef, SnowflakeTableReferenceOutputTypeDef
]

class CreateConfiguredTableAssociationAnalysisRuleInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    configuredTableAssociationIdentifier: str
    analysisRuleType: ConfiguredTableAssociationAnalysisRuleTypeType
    analysisRulePolicy: ConfiguredTableAssociationAnalysisRulePolicyTypeDef

class UpdateConfiguredTableAssociationAnalysisRuleInputRequestTypeDef(TypedDict):
    membershipIdentifier: str
    configuredTableAssociationIdentifier: str
    analysisRuleType: ConfiguredTableAssociationAnalysisRuleTypeType
    analysisRulePolicy: ConfiguredTableAssociationAnalysisRulePolicyTypeDef

ConfiguredTableAnalysisRuleTypeDef = TypedDict(
    "ConfiguredTableAnalysisRuleTypeDef",
    {
        "configuredTableId": str,
        "configuredTableArn": str,
        "policy": ConfiguredTableAnalysisRulePolicyOutputTypeDef,
        "type": ConfiguredTableAnalysisRuleTypeType,
        "createTime": datetime,
        "updateTime": datetime,
    },
)
ConfiguredTableAnalysisRulePolicyV1TypeDef = TypedDict(
    "ConfiguredTableAnalysisRulePolicyV1TypeDef",
    {
        "list": NotRequired[AnalysisRuleListUnionTypeDef],
        "aggregation": NotRequired[AnalysisRuleAggregationUnionTypeDef],
        "custom": NotRequired[AnalysisRuleCustomUnionTypeDef],
    },
)
AnalysisRuleTypeDef = TypedDict(
    "AnalysisRuleTypeDef",
    {
        "collaborationId": str,
        "type": AnalysisRuleTypeType,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "policy": AnalysisRulePolicyTypeDef,
    },
)

class CreateConfiguredTableOutputTypeDef(TypedDict):
    configuredTable: ConfiguredTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetConfiguredTableOutputTypeDef(TypedDict):
    configuredTable: ConfiguredTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConfiguredTableOutputTypeDef(TypedDict):
    configuredTable: ConfiguredTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class TableReferenceTypeDef(TypedDict):
    glue: NotRequired[GlueTableReferenceTypeDef]
    snowflake: NotRequired[SnowflakeTableReferenceUnionTypeDef]
    athena: NotRequired[AthenaTableReferenceTypeDef]

class CreateConfiguredTableAnalysisRuleOutputTypeDef(TypedDict):
    analysisRule: ConfiguredTableAnalysisRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetConfiguredTableAnalysisRuleOutputTypeDef(TypedDict):
    analysisRule: ConfiguredTableAnalysisRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConfiguredTableAnalysisRuleOutputTypeDef(TypedDict):
    analysisRule: ConfiguredTableAnalysisRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ConfiguredTableAnalysisRulePolicyV1UnionTypeDef = Union[
    ConfiguredTableAnalysisRulePolicyV1TypeDef, ConfiguredTableAnalysisRulePolicyV1OutputTypeDef
]

class BatchGetSchemaAnalysisRuleOutputTypeDef(TypedDict):
    analysisRules: List[AnalysisRuleTypeDef]
    errors: List[BatchGetSchemaAnalysisRuleErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetSchemaAnalysisRuleOutputTypeDef(TypedDict):
    analysisRule: AnalysisRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateConfiguredTableInputRequestTypeDef(TypedDict):
    name: str
    tableReference: TableReferenceTypeDef
    allowedColumns: Sequence[str]
    analysisMethod: Literal["DIRECT_QUERY"]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class ConfiguredTableAnalysisRulePolicyTypeDef(TypedDict):
    v1: NotRequired[ConfiguredTableAnalysisRulePolicyV1UnionTypeDef]

class CreateConfiguredTableAnalysisRuleInputRequestTypeDef(TypedDict):
    configuredTableIdentifier: str
    analysisRuleType: ConfiguredTableAnalysisRuleTypeType
    analysisRulePolicy: ConfiguredTableAnalysisRulePolicyTypeDef

class UpdateConfiguredTableAnalysisRuleInputRequestTypeDef(TypedDict):
    configuredTableIdentifier: str
    analysisRuleType: ConfiguredTableAnalysisRuleTypeType
    analysisRulePolicy: ConfiguredTableAnalysisRulePolicyTypeDef
