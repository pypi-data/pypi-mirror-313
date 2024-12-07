"""
Type annotations for datazone service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/type_defs/)

Usage::

    ```python
    from mypy_boto3_datazone.type_defs import AcceptChoiceTypeDef

    data: AcceptChoiceTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AcceptRuleBehaviorType,
    AuthenticationTypeType,
    AuthTypeType,
    ChangeActionType,
    ComputeEnvironmentsType,
    ConfigurableActionTypeAuthorizationType,
    ConnectionStatusType,
    ConnectionTypeType,
    DataAssetActivityStatusType,
    DataProductStatusType,
    DataSourceErrorTypeType,
    DataSourceRunStatusType,
    DataSourceRunTypeType,
    DataSourceStatusType,
    DeploymentModeType,
    DeploymentStatusType,
    DeploymentTypeType,
    DomainStatusType,
    DomainVersionType,
    EdgeDirectionType,
    EnableSettingType,
    EntityTypeType,
    EnvironmentStatusType,
    FilterExpressionTypeType,
    FilterStatusType,
    FormTypeStatusType,
    GlossaryStatusType,
    GlossaryTermStatusType,
    GlueConnectionTypeType,
    GovernanceTypeType,
    GroupProfileStatusType,
    GroupSearchTypeType,
    HyperPodOrchestratorType,
    InventorySearchScopeType,
    JobRunModeType,
    JobRunStatusType,
    LineageEventProcessingStatusType,
    LineageImportStatusType,
    ListingStatusType,
    ManagedPolicyTypeType,
    MetadataGenerationRunStatusType,
    NotificationRoleType,
    NotificationTypeType,
    OAuth2GrantTypeType,
    OpenLineageRunStateType,
    OverallDeploymentStatusType,
    ProjectDesignationType,
    ProjectStatusType,
    ProtocolType,
    RejectRuleBehaviorType,
    RuleScopeSelectionModeType,
    SearchOutputAdditionalAttributeType,
    SelfGrantStatusType,
    SortKeyType,
    SortOrderType,
    StatusType,
    SubscriptionGrantOverallStatusType,
    SubscriptionGrantStatusType,
    SubscriptionRequestStatusType,
    SubscriptionStatusType,
    TargetEntityTypeType,
    TaskStatusType,
    TimeSeriesEntityTypeType,
    TimezoneType,
    TypesSearchScopeType,
    UserAssignmentType,
    UserDesignationType,
    UserProfileStatusType,
    UserProfileTypeType,
    UserSearchTypeType,
    UserTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcceptChoiceTypeDef",
    "AcceptPredictionsInputRequestTypeDef",
    "AcceptPredictionsOutputTypeDef",
    "AcceptRuleTypeDef",
    "AcceptSubscriptionRequestInputRequestTypeDef",
    "AcceptSubscriptionRequestOutputTypeDef",
    "AcceptedAssetScopeTypeDef",
    "ActionParametersTypeDef",
    "AddEntityOwnerInputRequestTypeDef",
    "AddPolicyGrantInputRequestTypeDef",
    "AddToProjectMemberPoolPolicyGrantDetailTypeDef",
    "AssetFilterConfigurationOutputTypeDef",
    "AssetFilterConfigurationTypeDef",
    "AssetFilterSummaryTypeDef",
    "AssetInDataProductListingItemTypeDef",
    "AssetItemAdditionalAttributesTypeDef",
    "AssetItemTypeDef",
    "AssetListingDetailsTypeDef",
    "AssetListingItemAdditionalAttributesTypeDef",
    "AssetListingItemTypeDef",
    "AssetListingTypeDef",
    "AssetRevisionTypeDef",
    "AssetScopeTypeDef",
    "AssetTargetNameMapTypeDef",
    "AssetTypeItemTypeDef",
    "AssetTypesForRuleOutputTypeDef",
    "AssetTypesForRuleTypeDef",
    "AssetTypesForRuleUnionTypeDef",
    "AssociateEnvironmentRoleInputRequestTypeDef",
    "AthenaPropertiesInputTypeDef",
    "AthenaPropertiesOutputTypeDef",
    "AthenaPropertiesPatchTypeDef",
    "AuthenticationConfigurationInputTypeDef",
    "AuthenticationConfigurationPatchTypeDef",
    "AuthenticationConfigurationTypeDef",
    "AuthorizationCodePropertiesTypeDef",
    "AwsAccountTypeDef",
    "AwsConsoleLinkParametersTypeDef",
    "AwsLocationTypeDef",
    "BasicAuthenticationCredentialsTypeDef",
    "BlobTypeDef",
    "BusinessNameGenerationConfigurationTypeDef",
    "CancelMetadataGenerationRunInputRequestTypeDef",
    "CancelSubscriptionInputRequestTypeDef",
    "CancelSubscriptionOutputTypeDef",
    "CloudFormationPropertiesTypeDef",
    "ColumnFilterConfigurationOutputTypeDef",
    "ColumnFilterConfigurationTypeDef",
    "ColumnFilterConfigurationUnionTypeDef",
    "ConfigurableActionParameterTypeDef",
    "ConfigurableEnvironmentActionTypeDef",
    "ConnectionCredentialsTypeDef",
    "ConnectionPropertiesInputTypeDef",
    "ConnectionPropertiesOutputTypeDef",
    "ConnectionPropertiesPatchTypeDef",
    "ConnectionSummaryTypeDef",
    "CreateAssetFilterInputRequestTypeDef",
    "CreateAssetFilterOutputTypeDef",
    "CreateAssetInputRequestTypeDef",
    "CreateAssetOutputTypeDef",
    "CreateAssetRevisionInputRequestTypeDef",
    "CreateAssetRevisionOutputTypeDef",
    "CreateAssetTypeInputRequestTypeDef",
    "CreateAssetTypeOutputTypeDef",
    "CreateAssetTypePolicyGrantDetailTypeDef",
    "CreateConnectionInputRequestTypeDef",
    "CreateConnectionOutputTypeDef",
    "CreateDataProductInputRequestTypeDef",
    "CreateDataProductOutputTypeDef",
    "CreateDataProductRevisionInputRequestTypeDef",
    "CreateDataProductRevisionOutputTypeDef",
    "CreateDataSourceInputRequestTypeDef",
    "CreateDataSourceOutputTypeDef",
    "CreateDomainInputRequestTypeDef",
    "CreateDomainOutputTypeDef",
    "CreateDomainUnitInputRequestTypeDef",
    "CreateDomainUnitOutputTypeDef",
    "CreateDomainUnitPolicyGrantDetailTypeDef",
    "CreateEnvironmentActionInputRequestTypeDef",
    "CreateEnvironmentActionOutputTypeDef",
    "CreateEnvironmentInputRequestTypeDef",
    "CreateEnvironmentOutputTypeDef",
    "CreateEnvironmentProfileInputRequestTypeDef",
    "CreateEnvironmentProfileOutputTypeDef",
    "CreateEnvironmentProfilePolicyGrantDetailTypeDef",
    "CreateFormTypeInputRequestTypeDef",
    "CreateFormTypeOutputTypeDef",
    "CreateFormTypePolicyGrantDetailTypeDef",
    "CreateGlossaryInputRequestTypeDef",
    "CreateGlossaryOutputTypeDef",
    "CreateGlossaryPolicyGrantDetailTypeDef",
    "CreateGlossaryTermInputRequestTypeDef",
    "CreateGlossaryTermOutputTypeDef",
    "CreateGroupProfileInputRequestTypeDef",
    "CreateGroupProfileOutputTypeDef",
    "CreateListingChangeSetInputRequestTypeDef",
    "CreateListingChangeSetOutputTypeDef",
    "CreateProjectFromProjectProfilePolicyGrantDetailOutputTypeDef",
    "CreateProjectFromProjectProfilePolicyGrantDetailTypeDef",
    "CreateProjectFromProjectProfilePolicyGrantDetailUnionTypeDef",
    "CreateProjectInputRequestTypeDef",
    "CreateProjectMembershipInputRequestTypeDef",
    "CreateProjectOutputTypeDef",
    "CreateProjectPolicyGrantDetailTypeDef",
    "CreateProjectProfileInputRequestTypeDef",
    "CreateProjectProfileOutputTypeDef",
    "CreateRuleInputRequestTypeDef",
    "CreateRuleOutputTypeDef",
    "CreateSubscriptionGrantInputRequestTypeDef",
    "CreateSubscriptionGrantOutputTypeDef",
    "CreateSubscriptionRequestInputRequestTypeDef",
    "CreateSubscriptionRequestOutputTypeDef",
    "CreateSubscriptionTargetInputRequestTypeDef",
    "CreateSubscriptionTargetOutputTypeDef",
    "CreateUserProfileInputRequestTypeDef",
    "CreateUserProfileOutputTypeDef",
    "CustomParameterTypeDef",
    "DataProductItemOutputTypeDef",
    "DataProductItemTypeDef",
    "DataProductItemUnionTypeDef",
    "DataProductListingItemAdditionalAttributesTypeDef",
    "DataProductListingItemTypeDef",
    "DataProductListingTypeDef",
    "DataProductResultItemTypeDef",
    "DataProductRevisionTypeDef",
    "DataSourceConfigurationInputTypeDef",
    "DataSourceConfigurationOutputTypeDef",
    "DataSourceErrorMessageTypeDef",
    "DataSourceRunActivityTypeDef",
    "DataSourceRunLineageSummaryTypeDef",
    "DataSourceRunSummaryTypeDef",
    "DataSourceSummaryTypeDef",
    "DeleteAssetFilterInputRequestTypeDef",
    "DeleteAssetInputRequestTypeDef",
    "DeleteAssetTypeInputRequestTypeDef",
    "DeleteConnectionInputRequestTypeDef",
    "DeleteConnectionOutputTypeDef",
    "DeleteDataProductInputRequestTypeDef",
    "DeleteDataSourceInputRequestTypeDef",
    "DeleteDataSourceOutputTypeDef",
    "DeleteDomainInputRequestTypeDef",
    "DeleteDomainOutputTypeDef",
    "DeleteDomainUnitInputRequestTypeDef",
    "DeleteEnvironmentActionInputRequestTypeDef",
    "DeleteEnvironmentBlueprintConfigurationInputRequestTypeDef",
    "DeleteEnvironmentInputRequestTypeDef",
    "DeleteEnvironmentProfileInputRequestTypeDef",
    "DeleteFormTypeInputRequestTypeDef",
    "DeleteGlossaryInputRequestTypeDef",
    "DeleteGlossaryTermInputRequestTypeDef",
    "DeleteListingInputRequestTypeDef",
    "DeleteProjectInputRequestTypeDef",
    "DeleteProjectMembershipInputRequestTypeDef",
    "DeleteProjectProfileInputRequestTypeDef",
    "DeleteRuleInputRequestTypeDef",
    "DeleteSubscriptionGrantInputRequestTypeDef",
    "DeleteSubscriptionGrantOutputTypeDef",
    "DeleteSubscriptionRequestInputRequestTypeDef",
    "DeleteSubscriptionTargetInputRequestTypeDef",
    "DeleteTimeSeriesDataPointsInputRequestTypeDef",
    "DeploymentPropertiesTypeDef",
    "DeploymentTypeDef",
    "DetailedGlossaryTermTypeDef",
    "DisassociateEnvironmentRoleInputRequestTypeDef",
    "DomainSummaryTypeDef",
    "DomainUnitFilterForProjectTypeDef",
    "DomainUnitGrantFilterOutputTypeDef",
    "DomainUnitGrantFilterTypeDef",
    "DomainUnitGrantFilterUnionTypeDef",
    "DomainUnitGroupPropertiesTypeDef",
    "DomainUnitOwnerPropertiesTypeDef",
    "DomainUnitPolicyGrantPrincipalOutputTypeDef",
    "DomainUnitPolicyGrantPrincipalTypeDef",
    "DomainUnitPolicyGrantPrincipalUnionTypeDef",
    "DomainUnitSummaryTypeDef",
    "DomainUnitTargetTypeDef",
    "DomainUnitUserPropertiesTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnvironmentActionSummaryTypeDef",
    "EnvironmentBlueprintConfigurationItemTypeDef",
    "EnvironmentBlueprintSummaryTypeDef",
    "EnvironmentConfigurationOutputTypeDef",
    "EnvironmentConfigurationParameterTypeDef",
    "EnvironmentConfigurationParametersDetailsOutputTypeDef",
    "EnvironmentConfigurationParametersDetailsTypeDef",
    "EnvironmentConfigurationParametersDetailsUnionTypeDef",
    "EnvironmentConfigurationTypeDef",
    "EnvironmentConfigurationUnionTypeDef",
    "EnvironmentConfigurationUserParameterOutputTypeDef",
    "EnvironmentConfigurationUserParameterTypeDef",
    "EnvironmentConfigurationUserParameterUnionTypeDef",
    "EnvironmentDeploymentDetailsOutputTypeDef",
    "EnvironmentDeploymentDetailsTypeDef",
    "EnvironmentErrorTypeDef",
    "EnvironmentParameterTypeDef",
    "EnvironmentProfileSummaryTypeDef",
    "EnvironmentSummaryTypeDef",
    "EqualToExpressionTypeDef",
    "EventSummaryTypeDef",
    "FailureCauseTypeDef",
    "FilterClausePaginatorTypeDef",
    "FilterClauseTypeDef",
    "FilterExpressionTypeDef",
    "FilterTypeDef",
    "FormEntryInputTypeDef",
    "FormEntryOutputTypeDef",
    "FormInputTypeDef",
    "FormOutputTypeDef",
    "FormTypeDataTypeDef",
    "GetAssetFilterInputRequestTypeDef",
    "GetAssetFilterOutputTypeDef",
    "GetAssetInputRequestTypeDef",
    "GetAssetOutputTypeDef",
    "GetAssetTypeInputRequestTypeDef",
    "GetAssetTypeOutputTypeDef",
    "GetConnectionInputRequestTypeDef",
    "GetConnectionOutputTypeDef",
    "GetDataProductInputRequestTypeDef",
    "GetDataProductOutputTypeDef",
    "GetDataSourceInputRequestTypeDef",
    "GetDataSourceOutputTypeDef",
    "GetDataSourceRunInputRequestTypeDef",
    "GetDataSourceRunOutputTypeDef",
    "GetDomainInputRequestTypeDef",
    "GetDomainOutputTypeDef",
    "GetDomainUnitInputRequestTypeDef",
    "GetDomainUnitOutputTypeDef",
    "GetEnvironmentActionInputRequestTypeDef",
    "GetEnvironmentActionOutputTypeDef",
    "GetEnvironmentBlueprintConfigurationInputRequestTypeDef",
    "GetEnvironmentBlueprintConfigurationOutputTypeDef",
    "GetEnvironmentBlueprintInputRequestTypeDef",
    "GetEnvironmentBlueprintOutputTypeDef",
    "GetEnvironmentCredentialsInputRequestTypeDef",
    "GetEnvironmentCredentialsOutputTypeDef",
    "GetEnvironmentInputRequestTypeDef",
    "GetEnvironmentOutputTypeDef",
    "GetEnvironmentProfileInputRequestTypeDef",
    "GetEnvironmentProfileOutputTypeDef",
    "GetFormTypeInputRequestTypeDef",
    "GetFormTypeOutputTypeDef",
    "GetGlossaryInputRequestTypeDef",
    "GetGlossaryOutputTypeDef",
    "GetGlossaryTermInputRequestTypeDef",
    "GetGlossaryTermOutputTypeDef",
    "GetGroupProfileInputRequestTypeDef",
    "GetGroupProfileOutputTypeDef",
    "GetIamPortalLoginUrlInputRequestTypeDef",
    "GetIamPortalLoginUrlOutputTypeDef",
    "GetJobRunInputRequestTypeDef",
    "GetJobRunOutputTypeDef",
    "GetLineageEventInputRequestTypeDef",
    "GetLineageEventOutputTypeDef",
    "GetLineageNodeInputRequestTypeDef",
    "GetLineageNodeOutputTypeDef",
    "GetListingInputRequestTypeDef",
    "GetListingOutputTypeDef",
    "GetMetadataGenerationRunInputRequestTypeDef",
    "GetMetadataGenerationRunOutputTypeDef",
    "GetProjectInputRequestTypeDef",
    "GetProjectOutputTypeDef",
    "GetProjectProfileInputRequestTypeDef",
    "GetProjectProfileOutputTypeDef",
    "GetRuleInputRequestTypeDef",
    "GetRuleOutputTypeDef",
    "GetSubscriptionGrantInputRequestTypeDef",
    "GetSubscriptionGrantOutputTypeDef",
    "GetSubscriptionInputRequestTypeDef",
    "GetSubscriptionOutputTypeDef",
    "GetSubscriptionRequestDetailsInputRequestTypeDef",
    "GetSubscriptionRequestDetailsOutputTypeDef",
    "GetSubscriptionTargetInputRequestTypeDef",
    "GetSubscriptionTargetOutputTypeDef",
    "GetTimeSeriesDataPointInputRequestTypeDef",
    "GetTimeSeriesDataPointOutputTypeDef",
    "GetUserProfileInputRequestTypeDef",
    "GetUserProfileOutputTypeDef",
    "GlossaryItemTypeDef",
    "GlossaryTermItemTypeDef",
    "GlueConnectionInputTypeDef",
    "GlueConnectionPatchTypeDef",
    "GlueConnectionTypeDef",
    "GlueOAuth2CredentialsTypeDef",
    "GluePropertiesInputTypeDef",
    "GluePropertiesOutputTypeDef",
    "GluePropertiesPatchTypeDef",
    "GlueRunConfigurationInputTypeDef",
    "GlueRunConfigurationOutputTypeDef",
    "GlueSelfGrantStatusOutputTypeDef",
    "GrantedEntityInputTypeDef",
    "GrantedEntityTypeDef",
    "GreaterThanExpressionTypeDef",
    "GreaterThanOrEqualToExpressionTypeDef",
    "GroupDetailsTypeDef",
    "GroupPolicyGrantPrincipalTypeDef",
    "GroupProfileSummaryTypeDef",
    "HyperPodPropertiesInputTypeDef",
    "HyperPodPropertiesOutputTypeDef",
    "IamPropertiesInputTypeDef",
    "IamPropertiesOutputTypeDef",
    "IamPropertiesPatchTypeDef",
    "IamUserProfileDetailsTypeDef",
    "ImportTypeDef",
    "InExpressionOutputTypeDef",
    "InExpressionTypeDef",
    "InExpressionUnionTypeDef",
    "IsNotNullExpressionTypeDef",
    "IsNullExpressionTypeDef",
    "JobRunDetailsTypeDef",
    "JobRunErrorTypeDef",
    "JobRunSummaryTypeDef",
    "LakeFormationConfigurationOutputTypeDef",
    "LakeFormationConfigurationTypeDef",
    "LakeFormationConfigurationUnionTypeDef",
    "LessThanExpressionTypeDef",
    "LessThanOrEqualToExpressionTypeDef",
    "LikeExpressionTypeDef",
    "LineageEventSummaryTypeDef",
    "LineageInfoTypeDef",
    "LineageNodeReferenceTypeDef",
    "LineageNodeSummaryTypeDef",
    "LineageNodeTypeItemTypeDef",
    "LineageRunDetailsTypeDef",
    "LineageSqlQueryRunDetailsTypeDef",
    "LineageSyncScheduleTypeDef",
    "ListAssetFiltersInputListAssetFiltersPaginateTypeDef",
    "ListAssetFiltersInputRequestTypeDef",
    "ListAssetFiltersOutputTypeDef",
    "ListAssetRevisionsInputListAssetRevisionsPaginateTypeDef",
    "ListAssetRevisionsInputRequestTypeDef",
    "ListAssetRevisionsOutputTypeDef",
    "ListConnectionsInputListConnectionsPaginateTypeDef",
    "ListConnectionsInputRequestTypeDef",
    "ListConnectionsOutputTypeDef",
    "ListDataProductRevisionsInputListDataProductRevisionsPaginateTypeDef",
    "ListDataProductRevisionsInputRequestTypeDef",
    "ListDataProductRevisionsOutputTypeDef",
    "ListDataSourceRunActivitiesInputListDataSourceRunActivitiesPaginateTypeDef",
    "ListDataSourceRunActivitiesInputRequestTypeDef",
    "ListDataSourceRunActivitiesOutputTypeDef",
    "ListDataSourceRunsInputListDataSourceRunsPaginateTypeDef",
    "ListDataSourceRunsInputRequestTypeDef",
    "ListDataSourceRunsOutputTypeDef",
    "ListDataSourcesInputListDataSourcesPaginateTypeDef",
    "ListDataSourcesInputRequestTypeDef",
    "ListDataSourcesOutputTypeDef",
    "ListDomainUnitsForParentInputListDomainUnitsForParentPaginateTypeDef",
    "ListDomainUnitsForParentInputRequestTypeDef",
    "ListDomainUnitsForParentOutputTypeDef",
    "ListDomainsInputListDomainsPaginateTypeDef",
    "ListDomainsInputRequestTypeDef",
    "ListDomainsOutputTypeDef",
    "ListEntityOwnersInputListEntityOwnersPaginateTypeDef",
    "ListEntityOwnersInputRequestTypeDef",
    "ListEntityOwnersOutputTypeDef",
    "ListEnvironmentActionsInputListEnvironmentActionsPaginateTypeDef",
    "ListEnvironmentActionsInputRequestTypeDef",
    "ListEnvironmentActionsOutputTypeDef",
    "ListEnvironmentBlueprintConfigurationsInputListEnvironmentBlueprintConfigurationsPaginateTypeDef",
    "ListEnvironmentBlueprintConfigurationsInputRequestTypeDef",
    "ListEnvironmentBlueprintConfigurationsOutputTypeDef",
    "ListEnvironmentBlueprintsInputListEnvironmentBlueprintsPaginateTypeDef",
    "ListEnvironmentBlueprintsInputRequestTypeDef",
    "ListEnvironmentBlueprintsOutputTypeDef",
    "ListEnvironmentProfilesInputListEnvironmentProfilesPaginateTypeDef",
    "ListEnvironmentProfilesInputRequestTypeDef",
    "ListEnvironmentProfilesOutputTypeDef",
    "ListEnvironmentsInputListEnvironmentsPaginateTypeDef",
    "ListEnvironmentsInputRequestTypeDef",
    "ListEnvironmentsOutputTypeDef",
    "ListJobRunsInputListJobRunsPaginateTypeDef",
    "ListJobRunsInputRequestTypeDef",
    "ListJobRunsOutputTypeDef",
    "ListLineageEventsInputListLineageEventsPaginateTypeDef",
    "ListLineageEventsInputRequestTypeDef",
    "ListLineageEventsOutputTypeDef",
    "ListLineageNodeHistoryInputListLineageNodeHistoryPaginateTypeDef",
    "ListLineageNodeHistoryInputRequestTypeDef",
    "ListLineageNodeHistoryOutputTypeDef",
    "ListMetadataGenerationRunsInputListMetadataGenerationRunsPaginateTypeDef",
    "ListMetadataGenerationRunsInputRequestTypeDef",
    "ListMetadataGenerationRunsOutputTypeDef",
    "ListNotificationsInputListNotificationsPaginateTypeDef",
    "ListNotificationsInputRequestTypeDef",
    "ListNotificationsOutputTypeDef",
    "ListPolicyGrantsInputListPolicyGrantsPaginateTypeDef",
    "ListPolicyGrantsInputRequestTypeDef",
    "ListPolicyGrantsOutputTypeDef",
    "ListProjectMembershipsInputListProjectMembershipsPaginateTypeDef",
    "ListProjectMembershipsInputRequestTypeDef",
    "ListProjectMembershipsOutputTypeDef",
    "ListProjectProfilesInputListProjectProfilesPaginateTypeDef",
    "ListProjectProfilesInputRequestTypeDef",
    "ListProjectProfilesOutputTypeDef",
    "ListProjectsInputListProjectsPaginateTypeDef",
    "ListProjectsInputRequestTypeDef",
    "ListProjectsOutputTypeDef",
    "ListRulesInputListRulesPaginateTypeDef",
    "ListRulesInputRequestTypeDef",
    "ListRulesOutputTypeDef",
    "ListSubscriptionGrantsInputListSubscriptionGrantsPaginateTypeDef",
    "ListSubscriptionGrantsInputRequestTypeDef",
    "ListSubscriptionGrantsOutputTypeDef",
    "ListSubscriptionRequestsInputListSubscriptionRequestsPaginateTypeDef",
    "ListSubscriptionRequestsInputRequestTypeDef",
    "ListSubscriptionRequestsOutputTypeDef",
    "ListSubscriptionTargetsInputListSubscriptionTargetsPaginateTypeDef",
    "ListSubscriptionTargetsInputRequestTypeDef",
    "ListSubscriptionTargetsOutputTypeDef",
    "ListSubscriptionsInputListSubscriptionsPaginateTypeDef",
    "ListSubscriptionsInputRequestTypeDef",
    "ListSubscriptionsOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTimeSeriesDataPointsInputListTimeSeriesDataPointsPaginateTypeDef",
    "ListTimeSeriesDataPointsInputRequestTypeDef",
    "ListTimeSeriesDataPointsOutputTypeDef",
    "ListingItemTypeDef",
    "ListingRevisionInputTypeDef",
    "ListingRevisionTypeDef",
    "ListingSummaryItemTypeDef",
    "ListingSummaryTypeDef",
    "MemberDetailsTypeDef",
    "MemberTypeDef",
    "MetadataFormEnforcementDetailOutputTypeDef",
    "MetadataFormEnforcementDetailTypeDef",
    "MetadataFormEnforcementDetailUnionTypeDef",
    "MetadataFormReferenceTypeDef",
    "MetadataFormSummaryTypeDef",
    "MetadataGenerationRunItemTypeDef",
    "MetadataGenerationRunTargetTypeDef",
    "ModelTypeDef",
    "NameIdentifierTypeDef",
    "NotEqualToExpressionTypeDef",
    "NotInExpressionOutputTypeDef",
    "NotInExpressionTypeDef",
    "NotInExpressionUnionTypeDef",
    "NotLikeExpressionTypeDef",
    "NotificationOutputTypeDef",
    "NotificationResourceTypeDef",
    "OAuth2ClientApplicationTypeDef",
    "OAuth2PropertiesOutputTypeDef",
    "OAuth2PropertiesTypeDef",
    "OAuth2PropertiesUnionTypeDef",
    "OpenLineageRunEventSummaryTypeDef",
    "OverrideDomainUnitOwnersPolicyGrantDetailTypeDef",
    "OverrideProjectOwnersPolicyGrantDetailTypeDef",
    "OwnerGroupPropertiesOutputTypeDef",
    "OwnerGroupPropertiesTypeDef",
    "OwnerPropertiesOutputTypeDef",
    "OwnerPropertiesTypeDef",
    "OwnerUserPropertiesOutputTypeDef",
    "OwnerUserPropertiesTypeDef",
    "PaginatorConfigTypeDef",
    "PhysicalConnectionRequirementsOutputTypeDef",
    "PhysicalConnectionRequirementsTypeDef",
    "PhysicalConnectionRequirementsUnionTypeDef",
    "PhysicalEndpointTypeDef",
    "PolicyGrantDetailOutputTypeDef",
    "PolicyGrantDetailTypeDef",
    "PolicyGrantMemberTypeDef",
    "PolicyGrantPrincipalOutputTypeDef",
    "PolicyGrantPrincipalTypeDef",
    "PostLineageEventInputRequestTypeDef",
    "PostLineageEventOutputTypeDef",
    "PostTimeSeriesDataPointsInputRequestTypeDef",
    "PostTimeSeriesDataPointsOutputTypeDef",
    "PredictionConfigurationTypeDef",
    "ProjectDeletionErrorTypeDef",
    "ProjectGrantFilterTypeDef",
    "ProjectMemberTypeDef",
    "ProjectPolicyGrantPrincipalTypeDef",
    "ProjectProfileSummaryTypeDef",
    "ProjectSummaryTypeDef",
    "ProjectsForRuleOutputTypeDef",
    "ProjectsForRuleTypeDef",
    "ProjectsForRuleUnionTypeDef",
    "ProvisioningConfigurationOutputTypeDef",
    "ProvisioningConfigurationTypeDef",
    "ProvisioningConfigurationUnionTypeDef",
    "ProvisioningPropertiesTypeDef",
    "PutEnvironmentBlueprintConfigurationInputRequestTypeDef",
    "PutEnvironmentBlueprintConfigurationOutputTypeDef",
    "RecommendationConfigurationTypeDef",
    "RedshiftClusterStorageTypeDef",
    "RedshiftCredentialConfigurationTypeDef",
    "RedshiftCredentialsTypeDef",
    "RedshiftLineageSyncConfigurationInputTypeDef",
    "RedshiftLineageSyncConfigurationOutputTypeDef",
    "RedshiftPropertiesInputTypeDef",
    "RedshiftPropertiesOutputTypeDef",
    "RedshiftPropertiesPatchTypeDef",
    "RedshiftRunConfigurationInputTypeDef",
    "RedshiftRunConfigurationOutputTypeDef",
    "RedshiftSelfGrantStatusOutputTypeDef",
    "RedshiftServerlessStorageTypeDef",
    "RedshiftStoragePropertiesTypeDef",
    "RedshiftStorageTypeDef",
    "RegionTypeDef",
    "RejectChoiceTypeDef",
    "RejectPredictionsInputRequestTypeDef",
    "RejectPredictionsOutputTypeDef",
    "RejectRuleTypeDef",
    "RejectSubscriptionRequestInputRequestTypeDef",
    "RejectSubscriptionRequestOutputTypeDef",
    "RelationalFilterConfigurationOutputTypeDef",
    "RelationalFilterConfigurationTypeDef",
    "RelationalFilterConfigurationUnionTypeDef",
    "RemoveEntityOwnerInputRequestTypeDef",
    "RemovePolicyGrantInputRequestTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeSubscriptionInputRequestTypeDef",
    "RevokeSubscriptionOutputTypeDef",
    "RowFilterConfigurationOutputTypeDef",
    "RowFilterConfigurationTypeDef",
    "RowFilterConfigurationUnionTypeDef",
    "RowFilterExpressionOutputTypeDef",
    "RowFilterExpressionTypeDef",
    "RowFilterExpressionUnionTypeDef",
    "RowFilterOutputTypeDef",
    "RowFilterTypeDef",
    "RowFilterUnionTypeDef",
    "RuleDetailOutputTypeDef",
    "RuleDetailTypeDef",
    "RuleScopeOutputTypeDef",
    "RuleScopeTypeDef",
    "RuleSummaryTypeDef",
    "RuleTargetTypeDef",
    "RunStatisticsForAssetsTypeDef",
    "SageMakerRunConfigurationInputTypeDef",
    "SageMakerRunConfigurationOutputTypeDef",
    "ScheduleConfigurationTypeDef",
    "SearchGroupProfilesInputRequestTypeDef",
    "SearchGroupProfilesInputSearchGroupProfilesPaginateTypeDef",
    "SearchGroupProfilesOutputTypeDef",
    "SearchInItemTypeDef",
    "SearchInputRequestTypeDef",
    "SearchInputSearchPaginateTypeDef",
    "SearchInventoryResultItemTypeDef",
    "SearchListingsInputRequestTypeDef",
    "SearchListingsInputSearchListingsPaginateTypeDef",
    "SearchListingsOutputTypeDef",
    "SearchOutputTypeDef",
    "SearchResultItemTypeDef",
    "SearchSortTypeDef",
    "SearchTypesInputRequestTypeDef",
    "SearchTypesInputSearchTypesPaginateTypeDef",
    "SearchTypesOutputTypeDef",
    "SearchTypesResultItemTypeDef",
    "SearchUserProfilesInputRequestTypeDef",
    "SearchUserProfilesInputSearchUserProfilesPaginateTypeDef",
    "SearchUserProfilesOutputTypeDef",
    "SelfGrantStatusDetailTypeDef",
    "SelfGrantStatusOutputTypeDef",
    "SingleSignOnTypeDef",
    "SparkEmrPropertiesInputTypeDef",
    "SparkEmrPropertiesOutputTypeDef",
    "SparkEmrPropertiesPatchTypeDef",
    "SparkGlueArgsTypeDef",
    "SparkGluePropertiesInputTypeDef",
    "SparkGluePropertiesOutputTypeDef",
    "SsoUserProfileDetailsTypeDef",
    "StartDataSourceRunInputRequestTypeDef",
    "StartDataSourceRunOutputTypeDef",
    "StartMetadataGenerationRunInputRequestTypeDef",
    "StartMetadataGenerationRunOutputTypeDef",
    "SubscribedAssetListingTypeDef",
    "SubscribedAssetTypeDef",
    "SubscribedListingInputTypeDef",
    "SubscribedListingItemTypeDef",
    "SubscribedListingTypeDef",
    "SubscribedPrincipalInputTypeDef",
    "SubscribedPrincipalTypeDef",
    "SubscribedProductListingTypeDef",
    "SubscribedProjectInputTypeDef",
    "SubscribedProjectTypeDef",
    "SubscriptionGrantSummaryTypeDef",
    "SubscriptionRequestSummaryTypeDef",
    "SubscriptionSummaryTypeDef",
    "SubscriptionTargetFormTypeDef",
    "SubscriptionTargetSummaryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TermRelationsOutputTypeDef",
    "TermRelationsTypeDef",
    "TimeSeriesDataPointFormInputTypeDef",
    "TimeSeriesDataPointFormOutputTypeDef",
    "TimeSeriesDataPointSummaryFormOutputTypeDef",
    "TimestampTypeDef",
    "TopicTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAssetFilterInputRequestTypeDef",
    "UpdateAssetFilterOutputTypeDef",
    "UpdateConnectionInputRequestTypeDef",
    "UpdateConnectionOutputTypeDef",
    "UpdateDataSourceInputRequestTypeDef",
    "UpdateDataSourceOutputTypeDef",
    "UpdateDomainInputRequestTypeDef",
    "UpdateDomainOutputTypeDef",
    "UpdateDomainUnitInputRequestTypeDef",
    "UpdateDomainUnitOutputTypeDef",
    "UpdateEnvironmentActionInputRequestTypeDef",
    "UpdateEnvironmentActionOutputTypeDef",
    "UpdateEnvironmentInputRequestTypeDef",
    "UpdateEnvironmentOutputTypeDef",
    "UpdateEnvironmentProfileInputRequestTypeDef",
    "UpdateEnvironmentProfileOutputTypeDef",
    "UpdateGlossaryInputRequestTypeDef",
    "UpdateGlossaryOutputTypeDef",
    "UpdateGlossaryTermInputRequestTypeDef",
    "UpdateGlossaryTermOutputTypeDef",
    "UpdateGroupProfileInputRequestTypeDef",
    "UpdateGroupProfileOutputTypeDef",
    "UpdateProjectInputRequestTypeDef",
    "UpdateProjectOutputTypeDef",
    "UpdateProjectProfileInputRequestTypeDef",
    "UpdateProjectProfileOutputTypeDef",
    "UpdateRuleInputRequestTypeDef",
    "UpdateRuleOutputTypeDef",
    "UpdateSubscriptionGrantStatusInputRequestTypeDef",
    "UpdateSubscriptionGrantStatusOutputTypeDef",
    "UpdateSubscriptionRequestInputRequestTypeDef",
    "UpdateSubscriptionRequestOutputTypeDef",
    "UpdateSubscriptionTargetInputRequestTypeDef",
    "UpdateSubscriptionTargetOutputTypeDef",
    "UpdateUserProfileInputRequestTypeDef",
    "UpdateUserProfileOutputTypeDef",
    "UserDetailsTypeDef",
    "UserPolicyGrantPrincipalOutputTypeDef",
    "UserPolicyGrantPrincipalTypeDef",
    "UserPolicyGrantPrincipalUnionTypeDef",
    "UserProfileDetailsTypeDef",
    "UserProfileSummaryTypeDef",
    "UsernamePasswordTypeDef",
)

class AcceptChoiceTypeDef(TypedDict):
    predictionTarget: str
    editedValue: NotRequired[str]
    predictionChoice: NotRequired[int]

class AcceptRuleTypeDef(TypedDict):
    rule: NotRequired[AcceptRuleBehaviorType]
    threshold: NotRequired[float]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AcceptedAssetScopeTypeDef(TypedDict):
    assetId: str
    filterIds: Sequence[str]

class FormOutputTypeDef(TypedDict):
    formName: str
    content: NotRequired[str]
    typeName: NotRequired[str]
    typeRevision: NotRequired[str]

class AwsConsoleLinkParametersTypeDef(TypedDict):
    uri: NotRequired[str]

class AddToProjectMemberPoolPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class ColumnFilterConfigurationOutputTypeDef(TypedDict):
    includedColumnNames: NotRequired[List[str]]

AssetFilterSummaryTypeDef = TypedDict(
    "AssetFilterSummaryTypeDef",
    {
        "assetId": str,
        "domainId": str,
        "id": str,
        "name": str,
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "effectiveColumnNames": NotRequired[List[str]],
        "effectiveRowFilter": NotRequired[str],
        "errorMessage": NotRequired[str],
        "status": NotRequired[FilterStatusType],
    },
)

class AssetInDataProductListingItemTypeDef(TypedDict):
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    entityType: NotRequired[str]

TimeSeriesDataPointSummaryFormOutputTypeDef = TypedDict(
    "TimeSeriesDataPointSummaryFormOutputTypeDef",
    {
        "formName": str,
        "timestamp": datetime,
        "typeIdentifier": str,
        "contentSummary": NotRequired[str],
        "id": NotRequired[str],
        "typeRevision": NotRequired[str],
    },
)

class AssetListingDetailsTypeDef(TypedDict):
    listingId: str
    listingStatus: ListingStatusType

class DetailedGlossaryTermTypeDef(TypedDict):
    name: NotRequired[str]
    shortDescription: NotRequired[str]

AssetRevisionTypeDef = TypedDict(
    "AssetRevisionTypeDef",
    {
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "domainId": NotRequired[str],
        "id": NotRequired[str],
        "revision": NotRequired[str],
    },
)

class AssetScopeTypeDef(TypedDict):
    assetId: str
    filterIds: List[str]
    status: str
    errorMessage: NotRequired[str]

class AssetTargetNameMapTypeDef(TypedDict):
    assetId: str
    targetName: str

class FormEntryOutputTypeDef(TypedDict):
    typeName: str
    typeRevision: str
    required: NotRequired[bool]

class AssetTypesForRuleOutputTypeDef(TypedDict):
    selectionMode: RuleScopeSelectionModeType
    specificAssetTypes: NotRequired[List[str]]

class AssetTypesForRuleTypeDef(TypedDict):
    selectionMode: RuleScopeSelectionModeType
    specificAssetTypes: NotRequired[Sequence[str]]

class AssociateEnvironmentRoleInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    environmentRoleArn: str

class AthenaPropertiesInputTypeDef(TypedDict):
    workgroupName: NotRequired[str]

class AthenaPropertiesOutputTypeDef(TypedDict):
    workgroupName: NotRequired[str]

class AthenaPropertiesPatchTypeDef(TypedDict):
    workgroupName: NotRequired[str]

class BasicAuthenticationCredentialsTypeDef(TypedDict):
    password: NotRequired[str]
    userName: NotRequired[str]

class AuthorizationCodePropertiesTypeDef(TypedDict):
    authorizationCode: NotRequired[str]
    redirectUri: NotRequired[str]

class AwsAccountTypeDef(TypedDict):
    awsAccountId: NotRequired[str]
    awsAccountIdPath: NotRequired[str]

class AwsLocationTypeDef(TypedDict):
    accessRole: NotRequired[str]
    awsAccountId: NotRequired[str]
    awsRegion: NotRequired[str]
    iamConnectionId: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class BusinessNameGenerationConfigurationTypeDef(TypedDict):
    enabled: NotRequired[bool]

class CancelMetadataGenerationRunInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class CancelSubscriptionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class CloudFormationPropertiesTypeDef(TypedDict):
    templateUrl: str

class ColumnFilterConfigurationTypeDef(TypedDict):
    includedColumnNames: NotRequired[Sequence[str]]

class ConfigurableActionParameterTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]

class ConnectionCredentialsTypeDef(TypedDict):
    accessKeyId: NotRequired[str]
    expiration: NotRequired[datetime]
    secretAccessKey: NotRequired[str]
    sessionToken: NotRequired[str]

class HyperPodPropertiesInputTypeDef(TypedDict):
    clusterName: str

class IamPropertiesInputTypeDef(TypedDict):
    glueLineageSyncEnabled: NotRequired[bool]

class SparkEmrPropertiesInputTypeDef(TypedDict):
    computeArn: NotRequired[str]
    instanceProfileArn: NotRequired[str]
    javaVirtualEnv: NotRequired[str]
    logUri: NotRequired[str]
    pythonVirtualEnv: NotRequired[str]
    runtimeRole: NotRequired[str]
    trustedCertificatesS3Uri: NotRequired[str]

class GluePropertiesOutputTypeDef(TypedDict):
    errorMessage: NotRequired[str]
    status: NotRequired[ConnectionStatusType]

class HyperPodPropertiesOutputTypeDef(TypedDict):
    clusterName: str
    clusterArn: NotRequired[str]
    orchestrator: NotRequired[HyperPodOrchestratorType]

class IamPropertiesOutputTypeDef(TypedDict):
    environmentId: NotRequired[str]
    glueLineageSyncEnabled: NotRequired[bool]

class IamPropertiesPatchTypeDef(TypedDict):
    glueLineageSyncEnabled: NotRequired[bool]

class SparkEmrPropertiesPatchTypeDef(TypedDict):
    computeArn: NotRequired[str]
    instanceProfileArn: NotRequired[str]
    javaVirtualEnv: NotRequired[str]
    logUri: NotRequired[str]
    pythonVirtualEnv: NotRequired[str]
    runtimeRole: NotRequired[str]
    trustedCertificatesS3Uri: NotRequired[str]

class FormInputTypeDef(TypedDict):
    formName: str
    content: NotRequired[str]
    typeIdentifier: NotRequired[str]
    typeRevision: NotRequired[str]

class FormEntryInputTypeDef(TypedDict):
    typeIdentifier: str
    typeRevision: str
    required: NotRequired[bool]

class CreateAssetTypePolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class DataProductItemOutputTypeDef(TypedDict):
    identifier: str
    itemType: Literal["ASSET"]
    glossaryTerms: NotRequired[List[str]]
    revision: NotRequired[str]

class DataProductItemTypeDef(TypedDict):
    identifier: str
    itemType: Literal["ASSET"]
    glossaryTerms: NotRequired[Sequence[str]]
    revision: NotRequired[str]

class RecommendationConfigurationTypeDef(TypedDict):
    enableBusinessNameGeneration: NotRequired[bool]

class ScheduleConfigurationTypeDef(TypedDict):
    schedule: NotRequired[str]
    timezone: NotRequired[TimezoneType]

class DataSourceErrorMessageTypeDef(TypedDict):
    errorType: DataSourceErrorTypeType
    errorDetail: NotRequired[str]

SingleSignOnTypeDef = TypedDict(
    "SingleSignOnTypeDef",
    {
        "type": NotRequired[AuthTypeType],
        "userAssignment": NotRequired[UserAssignmentType],
    },
)

class CreateDomainUnitInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    parentDomainUnitIdentifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]

class CreateDomainUnitPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class EnvironmentParameterTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]

class CustomParameterTypeDef(TypedDict):
    fieldType: str
    keyName: str
    defaultValue: NotRequired[str]
    description: NotRequired[str]
    isEditable: NotRequired[bool]
    isOptional: NotRequired[bool]

class DeploymentPropertiesTypeDef(TypedDict):
    endTimeoutMinutes: NotRequired[int]
    startTimeoutMinutes: NotRequired[int]

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "type": str,
        "value": str,
        "name": NotRequired[str],
        "provider": NotRequired[str],
    },
)

class CreateEnvironmentProfilePolicyGrantDetailTypeDef(TypedDict):
    domainUnitId: NotRequired[str]

class ModelTypeDef(TypedDict):
    smithy: NotRequired[str]

class CreateFormTypePolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class CreateGlossaryInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    owningProjectIdentifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[GlossaryStatusType]

class CreateGlossaryPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class TermRelationsTypeDef(TypedDict):
    classifies: NotRequired[Sequence[str]]
    isA: NotRequired[Sequence[str]]

class TermRelationsOutputTypeDef(TypedDict):
    classifies: NotRequired[List[str]]
    isA: NotRequired[List[str]]

class CreateGroupProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    groupIdentifier: str
    clientToken: NotRequired[str]

class CreateListingChangeSetInputRequestTypeDef(TypedDict):
    action: ChangeActionType
    domainIdentifier: str
    entityIdentifier: str
    entityType: EntityTypeType
    clientToken: NotRequired[str]
    entityRevision: NotRequired[str]

class CreateProjectFromProjectProfilePolicyGrantDetailOutputTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]
    projectProfiles: NotRequired[List[str]]

class CreateProjectFromProjectProfilePolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]
    projectProfiles: NotRequired[Sequence[str]]

class MemberTypeDef(TypedDict):
    groupIdentifier: NotRequired[str]
    userIdentifier: NotRequired[str]

class ProjectDeletionErrorTypeDef(TypedDict):
    code: NotRequired[str]
    message: NotRequired[str]

class CreateProjectPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class SubscribedListingInputTypeDef(TypedDict):
    identifier: str

class SubscriptionTargetFormTypeDef(TypedDict):
    content: str
    formName: str

class CreateUserProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    userIdentifier: str
    clientToken: NotRequired[str]
    userType: NotRequired[UserTypeType]

class DataProductListingItemAdditionalAttributesTypeDef(TypedDict):
    forms: NotRequired[str]

DataProductResultItemTypeDef = TypedDict(
    "DataProductResultItemTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "description": NotRequired[str],
        "firstRevisionCreatedAt": NotRequired[datetime],
        "firstRevisionCreatedBy": NotRequired[str],
        "glossaryTerms": NotRequired[List[str]],
    },
)
DataProductRevisionTypeDef = TypedDict(
    "DataProductRevisionTypeDef",
    {
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "domainId": NotRequired[str],
        "id": NotRequired[str],
        "revision": NotRequired[str],
    },
)

class SageMakerRunConfigurationInputTypeDef(TypedDict):
    trackingAssets: Mapping[str, Sequence[str]]

class SageMakerRunConfigurationOutputTypeDef(TypedDict):
    trackingAssets: Dict[str, List[str]]
    accountId: NotRequired[str]
    region: NotRequired[str]

class LineageInfoTypeDef(TypedDict):
    errorMessage: NotRequired[str]
    eventId: NotRequired[str]
    eventStatus: NotRequired[LineageEventProcessingStatusType]

class DataSourceRunLineageSummaryTypeDef(TypedDict):
    importStatus: NotRequired[LineageImportStatusType]

class RunStatisticsForAssetsTypeDef(TypedDict):
    added: NotRequired[int]
    failed: NotRequired[int]
    skipped: NotRequired[int]
    unchanged: NotRequired[int]
    updated: NotRequired[int]

class DeleteAssetFilterInputRequestTypeDef(TypedDict):
    assetIdentifier: str
    domainIdentifier: str
    identifier: str

class DeleteAssetInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteAssetTypeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteConnectionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteDataProductInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteDataSourceInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    clientToken: NotRequired[str]
    retainPermissionsOnRevokeFailure: NotRequired[bool]

class DeleteDomainInputRequestTypeDef(TypedDict):
    identifier: str
    clientToken: NotRequired[str]
    skipDeletionCheck: NotRequired[bool]

class DeleteDomainUnitInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteEnvironmentActionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str

class DeleteEnvironmentBlueprintConfigurationInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentBlueprintIdentifier: str

class DeleteEnvironmentInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteEnvironmentProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteFormTypeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    formTypeIdentifier: str

class DeleteGlossaryInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteGlossaryTermInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteListingInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteProjectInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    skipDeletionCheck: NotRequired[bool]

class DeleteProjectProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteRuleInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteSubscriptionGrantInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteSubscriptionRequestInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteSubscriptionTargetInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str

class DeleteTimeSeriesDataPointsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    formName: str
    clientToken: NotRequired[str]

class EnvironmentErrorTypeDef(TypedDict):
    message: str
    code: NotRequired[str]

class DisassociateEnvironmentRoleInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    environmentRoleArn: str

DomainSummaryTypeDef = TypedDict(
    "DomainSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "managedAccountId": str,
        "name": str,
        "status": DomainStatusType,
        "description": NotRequired[str],
        "domainVersion": NotRequired[DomainVersionType],
        "lastUpdatedAt": NotRequired[datetime],
        "portalUrl": NotRequired[str],
    },
)

class DomainUnitFilterForProjectTypeDef(TypedDict):
    domainUnit: str
    includeChildDomainUnits: NotRequired[bool]

class DomainUnitGrantFilterOutputTypeDef(TypedDict):
    allDomainUnitsGrantFilter: NotRequired[Dict[str, Any]]

class DomainUnitGrantFilterTypeDef(TypedDict):
    allDomainUnitsGrantFilter: NotRequired[Mapping[str, Any]]

class DomainUnitGroupPropertiesTypeDef(TypedDict):
    groupId: NotRequired[str]

class DomainUnitUserPropertiesTypeDef(TypedDict):
    userId: NotRequired[str]

DomainUnitSummaryTypeDef = TypedDict(
    "DomainUnitSummaryTypeDef",
    {
        "id": str,
        "name": str,
    },
)

class DomainUnitTargetTypeDef(TypedDict):
    domainUnitId: str
    includeChildDomainUnits: NotRequired[bool]

class RegionTypeDef(TypedDict):
    regionName: NotRequired[str]
    regionNamePath: NotRequired[str]

class EnvironmentConfigurationParameterTypeDef(TypedDict):
    isEditable: NotRequired[bool]
    name: NotRequired[str]
    value: NotRequired[str]

EnvironmentProfileSummaryTypeDef = TypedDict(
    "EnvironmentProfileSummaryTypeDef",
    {
        "createdBy": str,
        "domainId": str,
        "environmentBlueprintId": str,
        "id": str,
        "name": str,
        "awsAccountId": NotRequired[str],
        "awsAccountRegion": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "projectId": NotRequired[str],
        "updatedAt": NotRequired[datetime],
    },
)
EnvironmentSummaryTypeDef = TypedDict(
    "EnvironmentSummaryTypeDef",
    {
        "createdBy": str,
        "domainId": str,
        "name": str,
        "projectId": str,
        "provider": str,
        "awsAccountId": NotRequired[str],
        "awsAccountRegion": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "environmentProfileId": NotRequired[str],
        "id": NotRequired[str],
        "status": NotRequired[EnvironmentStatusType],
        "updatedAt": NotRequired[datetime],
    },
)

class EqualToExpressionTypeDef(TypedDict):
    columnName: str
    value: str

class FailureCauseTypeDef(TypedDict):
    message: NotRequired[str]

class FilterTypeDef(TypedDict):
    attribute: str
    value: str

FilterExpressionTypeDef = TypedDict(
    "FilterExpressionTypeDef",
    {
        "expression": str,
        "type": FilterExpressionTypeType,
    },
)

class ImportTypeDef(TypedDict):
    name: str
    revision: str

class GetAssetFilterInputRequestTypeDef(TypedDict):
    assetIdentifier: str
    domainIdentifier: str
    identifier: str

class GetAssetInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    revision: NotRequired[str]

class GetAssetTypeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    revision: NotRequired[str]

class GetConnectionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    withSecret: NotRequired[bool]

class GetDataProductInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    revision: NotRequired[str]

class GetDataSourceInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetDataSourceRunInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetDomainInputRequestTypeDef(TypedDict):
    identifier: str

class GetDomainUnitInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetEnvironmentActionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str

class GetEnvironmentBlueprintConfigurationInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentBlueprintIdentifier: str

class GetEnvironmentBlueprintInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetEnvironmentCredentialsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str

class GetEnvironmentInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetEnvironmentProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetFormTypeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    formTypeIdentifier: str
    revision: NotRequired[str]

class GetGlossaryInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetGlossaryTermInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetGroupProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    groupIdentifier: str

class GetIamPortalLoginUrlInputRequestTypeDef(TypedDict):
    domainIdentifier: str

class GetJobRunInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class JobRunErrorTypeDef(TypedDict):
    message: str

class GetLineageEventInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

TimestampTypeDef = Union[datetime, str]
LineageNodeReferenceTypeDef = TypedDict(
    "LineageNodeReferenceTypeDef",
    {
        "eventTimestamp": NotRequired[datetime],
        "id": NotRequired[str],
    },
)

class GetListingInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    listingRevision: NotRequired[str]

class GetMetadataGenerationRunInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

MetadataGenerationRunTargetTypeDef = TypedDict(
    "MetadataGenerationRunTargetTypeDef",
    {
        "identifier": str,
        "type": Literal["ASSET"],
        "revision": NotRequired[str],
    },
)

class GetProjectInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetProjectProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetRuleInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    revision: NotRequired[str]

class GetSubscriptionGrantInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetSubscriptionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetSubscriptionRequestDetailsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetSubscriptionTargetInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str

class GetTimeSeriesDataPointInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    formName: str
    identifier: str

TimeSeriesDataPointFormOutputTypeDef = TypedDict(
    "TimeSeriesDataPointFormOutputTypeDef",
    {
        "formName": str,
        "timestamp": datetime,
        "typeIdentifier": str,
        "content": NotRequired[str],
        "id": NotRequired[str],
        "typeRevision": NotRequired[str],
    },
)
GetUserProfileInputRequestTypeDef = TypedDict(
    "GetUserProfileInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "userIdentifier": str,
        "type": NotRequired[UserProfileTypeType],
    },
)
GlossaryItemTypeDef = TypedDict(
    "GlossaryItemTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "status": GlossaryStatusType,
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "description": NotRequired[str],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)

class PhysicalConnectionRequirementsOutputTypeDef(TypedDict):
    availabilityZone: NotRequired[str]
    securityGroupIdList: NotRequired[List[str]]
    subnetId: NotRequired[str]
    subnetIdList: NotRequired[List[str]]

class GlueOAuth2CredentialsTypeDef(TypedDict):
    accessToken: NotRequired[str]
    jwtToken: NotRequired[str]
    refreshToken: NotRequired[str]
    userManagedClientApplicationClientSecret: NotRequired[str]

class SelfGrantStatusDetailTypeDef(TypedDict):
    databaseName: str
    status: SelfGrantStatusType
    failureCause: NotRequired[str]
    schemaName: NotRequired[str]

class ListingRevisionInputTypeDef(TypedDict):
    identifier: str
    revision: str

ListingRevisionTypeDef = TypedDict(
    "ListingRevisionTypeDef",
    {
        "id": str,
        "revision": str,
    },
)

class GreaterThanExpressionTypeDef(TypedDict):
    columnName: str
    value: str

class GreaterThanOrEqualToExpressionTypeDef(TypedDict):
    columnName: str
    value: str

class GroupDetailsTypeDef(TypedDict):
    groupId: str

class GroupPolicyGrantPrincipalTypeDef(TypedDict):
    groupIdentifier: NotRequired[str]

GroupProfileSummaryTypeDef = TypedDict(
    "GroupProfileSummaryTypeDef",
    {
        "domainId": NotRequired[str],
        "groupName": NotRequired[str],
        "id": NotRequired[str],
        "status": NotRequired[GroupProfileStatusType],
    },
)

class IamUserProfileDetailsTypeDef(TypedDict):
    arn: NotRequired[str]

class InExpressionOutputTypeDef(TypedDict):
    columnName: str
    values: List[str]

class InExpressionTypeDef(TypedDict):
    columnName: str
    values: Sequence[str]

class IsNotNullExpressionTypeDef(TypedDict):
    columnName: str

class IsNullExpressionTypeDef(TypedDict):
    columnName: str

class LakeFormationConfigurationOutputTypeDef(TypedDict):
    locationRegistrationExcludeS3Locations: NotRequired[List[str]]
    locationRegistrationRole: NotRequired[str]

class LakeFormationConfigurationTypeDef(TypedDict):
    locationRegistrationExcludeS3Locations: NotRequired[Sequence[str]]
    locationRegistrationRole: NotRequired[str]

class LessThanExpressionTypeDef(TypedDict):
    columnName: str
    value: str

class LessThanOrEqualToExpressionTypeDef(TypedDict):
    columnName: str
    value: str

class LikeExpressionTypeDef(TypedDict):
    columnName: str
    value: str

LineageNodeSummaryTypeDef = TypedDict(
    "LineageNodeSummaryTypeDef",
    {
        "domainId": str,
        "id": str,
        "typeName": str,
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "description": NotRequired[str],
        "eventTimestamp": NotRequired[datetime],
        "name": NotRequired[str],
        "sourceIdentifier": NotRequired[str],
        "typeRevision": NotRequired[str],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)

class LineageSqlQueryRunDetailsTypeDef(TypedDict):
    errorMessages: NotRequired[List[str]]
    numQueriesFailed: NotRequired[int]
    queryEndTime: NotRequired[datetime]
    queryStartTime: NotRequired[datetime]
    totalQueriesProcessed: NotRequired[int]

class LineageSyncScheduleTypeDef(TypedDict):
    schedule: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAssetFiltersInputRequestTypeDef(TypedDict):
    assetIdentifier: str
    domainIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[FilterStatusType]

class ListAssetRevisionsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

ListConnectionsInputRequestTypeDef = TypedDict(
    "ListConnectionsInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "projectIdentifier": str,
        "environmentIdentifier": NotRequired[str],
        "maxResults": NotRequired[int],
        "name": NotRequired[str],
        "nextToken": NotRequired[str],
        "sortBy": NotRequired[Literal["NAME"]],
        "sortOrder": NotRequired[SortOrderType],
        "type": NotRequired[ConnectionTypeType],
    },
)

class ListDataProductRevisionsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListDataSourceRunActivitiesInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[DataAssetActivityStatusType]

class ListDataSourceRunsInputRequestTypeDef(TypedDict):
    dataSourceIdentifier: str
    domainIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[DataSourceRunStatusType]

ListDataSourcesInputRequestTypeDef = TypedDict(
    "ListDataSourcesInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "projectIdentifier": str,
        "connectionIdentifier": NotRequired[str],
        "environmentIdentifier": NotRequired[str],
        "maxResults": NotRequired[int],
        "name": NotRequired[str],
        "nextToken": NotRequired[str],
        "status": NotRequired[DataSourceStatusType],
        "type": NotRequired[str],
    },
)

class ListDomainUnitsForParentInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    parentDomainUnitIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListDomainsInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[DomainStatusType]

class ListEntityOwnersInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: Literal["DOMAIN_UNIT"]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListEnvironmentActionsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListEnvironmentBlueprintConfigurationsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListEnvironmentBlueprintsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    managed: NotRequired[bool]
    maxResults: NotRequired[int]
    name: NotRequired[str]
    nextToken: NotRequired[str]

class ListEnvironmentProfilesInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    maxResults: NotRequired[int]
    name: NotRequired[str]
    nextToken: NotRequired[str]
    projectIdentifier: NotRequired[str]

class ListEnvironmentsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    environmentProfileIdentifier: NotRequired[str]
    maxResults: NotRequired[int]
    name: NotRequired[str]
    nextToken: NotRequired[str]
    provider: NotRequired[str]
    status: NotRequired[EnvironmentStatusType]

class ListJobRunsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    jobIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortOrder: NotRequired[SortOrderType]
    status: NotRequired[JobRunStatusType]

ListMetadataGenerationRunsInputRequestTypeDef = TypedDict(
    "ListMetadataGenerationRunsInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "status": NotRequired[MetadataGenerationRunStatusType],
        "type": NotRequired[Literal["BUSINESS_DESCRIPTIONS"]],
    },
)

class ListPolicyGrantsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TargetEntityTypeType
    policyType: ManagedPolicyTypeType
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListProjectMembershipsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["NAME"]]
    sortOrder: NotRequired[SortOrderType]

class ListProjectProfilesInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    maxResults: NotRequired[int]
    name: NotRequired[str]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["NAME"]]
    sortOrder: NotRequired[SortOrderType]

ProjectProfileSummaryTypeDef = TypedDict(
    "ProjectProfileSummaryTypeDef",
    {
        "createdBy": str,
        "domainId": str,
        "id": str,
        "name": str,
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "domainUnitId": NotRequired[str],
        "lastUpdatedAt": NotRequired[datetime],
        "status": NotRequired[StatusType],
    },
)

class ListProjectsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    groupIdentifier: NotRequired[str]
    maxResults: NotRequired[int]
    name: NotRequired[str]
    nextToken: NotRequired[str]
    userIdentifier: NotRequired[str]

class ListRulesInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    targetIdentifier: str
    targetType: Literal["DOMAIN_UNIT"]
    action: NotRequired[Literal["CREATE_SUBSCRIPTION_REQUEST"]]
    assetTypes: NotRequired[Sequence[str]]
    dataProduct: NotRequired[bool]
    includeCascaded: NotRequired[bool]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    projectIds: NotRequired[Sequence[str]]
    ruleType: NotRequired[Literal["METADATA_FORM_ENFORCEMENT"]]

class ListSubscriptionGrantsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    owningProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    subscribedListingId: NotRequired[str]
    subscriptionId: NotRequired[str]
    subscriptionTargetId: NotRequired[str]

class ListSubscriptionRequestsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    approverProjectId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    owningProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    status: NotRequired[SubscriptionRequestStatusType]
    subscribedListingId: NotRequired[str]

class ListSubscriptionTargetsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]

class ListSubscriptionsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    approverProjectId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    owningProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    status: NotRequired[SubscriptionStatusType]
    subscribedListingId: NotRequired[str]
    subscriptionRequestIdentifier: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class UserDetailsTypeDef(TypedDict):
    userId: str

class MetadataFormReferenceTypeDef(TypedDict):
    typeIdentifier: str
    typeRevision: str

class MetadataFormSummaryTypeDef(TypedDict):
    typeName: str
    typeRevision: str
    formName: NotRequired[str]

class NameIdentifierTypeDef(TypedDict):
    name: NotRequired[str]
    namespace: NotRequired[str]

class NotEqualToExpressionTypeDef(TypedDict):
    columnName: str
    value: str

class NotInExpressionOutputTypeDef(TypedDict):
    columnName: str
    values: List[str]

class NotInExpressionTypeDef(TypedDict):
    columnName: str
    values: Sequence[str]

class NotLikeExpressionTypeDef(TypedDict):
    columnName: str
    value: str

NotificationResourceTypeDef = TypedDict(
    "NotificationResourceTypeDef",
    {
        "id": str,
        "type": Literal["PROJECT"],
        "name": NotRequired[str],
    },
)

class OAuth2ClientApplicationTypeDef(TypedDict):
    aWSManagedClientApplicationReference: NotRequired[str]
    userManagedClientApplicationClientId: NotRequired[str]

class OverrideDomainUnitOwnersPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class OverrideProjectOwnersPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class OwnerGroupPropertiesOutputTypeDef(TypedDict):
    groupId: NotRequired[str]

class OwnerGroupPropertiesTypeDef(TypedDict):
    groupIdentifier: str

class OwnerUserPropertiesOutputTypeDef(TypedDict):
    userId: NotRequired[str]

class OwnerUserPropertiesTypeDef(TypedDict):
    userIdentifier: str

class PhysicalConnectionRequirementsTypeDef(TypedDict):
    availabilityZone: NotRequired[str]
    securityGroupIdList: NotRequired[Sequence[str]]
    subnetId: NotRequired[str]
    subnetIdList: NotRequired[Sequence[str]]

class UserPolicyGrantPrincipalOutputTypeDef(TypedDict):
    allUsersGrantFilter: NotRequired[Dict[str, Any]]
    userIdentifier: NotRequired[str]

class ProjectsForRuleOutputTypeDef(TypedDict):
    selectionMode: RuleScopeSelectionModeType
    specificProjects: NotRequired[List[str]]

class ProjectsForRuleTypeDef(TypedDict):
    selectionMode: RuleScopeSelectionModeType
    specificProjects: NotRequired[Sequence[str]]

class RedshiftClusterStorageTypeDef(TypedDict):
    clusterName: str

class RedshiftCredentialConfigurationTypeDef(TypedDict):
    secretManagerArn: str

class UsernamePasswordTypeDef(TypedDict):
    password: str
    username: str

class RedshiftStoragePropertiesTypeDef(TypedDict):
    clusterName: NotRequired[str]
    workgroupName: NotRequired[str]

class RedshiftServerlessStorageTypeDef(TypedDict):
    workgroupName: str

class RejectChoiceTypeDef(TypedDict):
    predictionTarget: str
    predictionChoices: NotRequired[Sequence[int]]

class RejectRuleTypeDef(TypedDict):
    rule: NotRequired[RejectRuleBehaviorType]
    threshold: NotRequired[float]

class RejectSubscriptionRequestInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    decisionComment: NotRequired[str]

class RevokeSubscriptionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    retainPermissions: NotRequired[bool]

class SearchGroupProfilesInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    groupType: GroupSearchTypeType
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    searchText: NotRequired[str]

class SearchInItemTypeDef(TypedDict):
    attribute: str

class SearchSortTypeDef(TypedDict):
    attribute: str
    order: NotRequired[SortOrderType]

class SearchUserProfilesInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    userType: UserSearchTypeType
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    searchText: NotRequired[str]

class SparkGlueArgsTypeDef(TypedDict):
    connection: NotRequired[str]

class SsoUserProfileDetailsTypeDef(TypedDict):
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    username: NotRequired[str]

class StartDataSourceRunInputRequestTypeDef(TypedDict):
    dataSourceIdentifier: str
    domainIdentifier: str
    clientToken: NotRequired[str]

class SubscribedProjectInputTypeDef(TypedDict):
    identifier: NotRequired[str]

SubscribedProjectTypeDef = TypedDict(
    "SubscribedProjectTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateDomainUnitInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    description: NotRequired[str]
    name: NotRequired[str]

class UpdateEnvironmentInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    description: NotRequired[str]
    glossaryTerms: NotRequired[Sequence[str]]
    name: NotRequired[str]

class UpdateGlossaryInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    name: NotRequired[str]
    status: NotRequired[GlossaryStatusType]

class UpdateGroupProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    groupIdentifier: str
    status: GroupProfileStatusType

class UpdateSubscriptionRequestInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    requestReason: str

UpdateUserProfileInputRequestTypeDef = TypedDict(
    "UpdateUserProfileInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "status": UserProfileStatusType,
        "userIdentifier": str,
        "type": NotRequired[UserProfileTypeType],
    },
)

class UserPolicyGrantPrincipalTypeDef(TypedDict):
    allUsersGrantFilter: NotRequired[Mapping[str, Any]]
    userIdentifier: NotRequired[str]

class AcceptPredictionsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    acceptChoices: NotRequired[Sequence[AcceptChoiceTypeDef]]
    acceptRule: NotRequired[AcceptRuleTypeDef]
    clientToken: NotRequired[str]
    revision: NotRequired[str]

class AcceptPredictionsOutputTypeDef(TypedDict):
    assetId: str
    domainId: str
    revision: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFormTypeOutputTypeDef(TypedDict):
    description: str
    domainId: str
    name: str
    originDomainId: str
    originProjectId: str
    owningProjectId: str
    revision: str
    ResponseMetadata: ResponseMetadataTypeDef

CreateGlossaryOutputTypeDef = TypedDict(
    "CreateGlossaryOutputTypeDef",
    {
        "description": str,
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "status": GlossaryStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateGroupProfileOutputTypeDef = TypedDict(
    "CreateGroupProfileOutputTypeDef",
    {
        "domainId": str,
        "groupName": str,
        "id": str,
        "status": GroupProfileStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateListingChangeSetOutputTypeDef(TypedDict):
    listingId: str
    listingRevision: str
    status: ListingStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteConnectionOutputTypeDef(TypedDict):
    status: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDomainOutputTypeDef(TypedDict):
    status: DomainStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetEnvironmentCredentialsOutputTypeDef(TypedDict):
    accessKeyId: str
    expiration: datetime
    secretAccessKey: str
    sessionToken: str
    ResponseMetadata: ResponseMetadataTypeDef

GetGlossaryOutputTypeDef = TypedDict(
    "GetGlossaryOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "status": GlossaryStatusType,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetGroupProfileOutputTypeDef = TypedDict(
    "GetGroupProfileOutputTypeDef",
    {
        "domainId": str,
        "groupName": str,
        "id": str,
        "status": GroupProfileStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetIamPortalLoginUrlOutputTypeDef(TypedDict):
    authCodeUrl: str
    userProfileId: str
    ResponseMetadata: ResponseMetadataTypeDef

GetLineageEventOutputTypeDef = TypedDict(
    "GetLineageEventOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "event": StreamingBody,
        "eventTime": datetime,
        "id": str,
        "processingStatus": LineageEventProcessingStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

PostLineageEventOutputTypeDef = TypedDict(
    "PostLineageEventOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class RejectPredictionsOutputTypeDef(TypedDict):
    assetId: str
    assetRevision: str
    domainId: str
    ResponseMetadata: ResponseMetadataTypeDef

StartMetadataGenerationRunOutputTypeDef = TypedDict(
    "StartMetadataGenerationRunOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "owningProjectId": str,
        "status": MetadataGenerationRunStatusType,
        "type": Literal["BUSINESS_DESCRIPTIONS"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateGlossaryOutputTypeDef = TypedDict(
    "UpdateGlossaryOutputTypeDef",
    {
        "description": str,
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "status": GlossaryStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateGroupProfileOutputTypeDef = TypedDict(
    "UpdateGroupProfileOutputTypeDef",
    {
        "domainId": str,
        "groupName": str,
        "id": str,
        "status": GroupProfileStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class AcceptSubscriptionRequestInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    assetScopes: NotRequired[Sequence[AcceptedAssetScopeTypeDef]]
    decisionComment: NotRequired[str]

class ActionParametersTypeDef(TypedDict):
    awsConsoleLink: NotRequired[AwsConsoleLinkParametersTypeDef]

class ListAssetFiltersOutputTypeDef(TypedDict):
    items: List[AssetFilterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AssetItemAdditionalAttributesTypeDef(TypedDict):
    formsOutput: NotRequired[List[FormOutputTypeDef]]
    latestTimeSeriesDataPointFormsOutput: NotRequired[
        List[TimeSeriesDataPointSummaryFormOutputTypeDef]
    ]
    readOnlyFormsOutput: NotRequired[List[FormOutputTypeDef]]

class AssetListingItemAdditionalAttributesTypeDef(TypedDict):
    forms: NotRequired[str]
    latestTimeSeriesDataPointForms: NotRequired[List[TimeSeriesDataPointSummaryFormOutputTypeDef]]

class ListTimeSeriesDataPointsOutputTypeDef(TypedDict):
    items: List[TimeSeriesDataPointSummaryFormOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

GetAssetOutputTypeDef = TypedDict(
    "GetAssetOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "externalIdentifier": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "formsOutput": List[FormOutputTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "latestTimeSeriesDataPointFormsOutput": List[TimeSeriesDataPointSummaryFormOutputTypeDef],
        "listing": AssetListingDetailsTypeDef,
        "name": str,
        "owningProjectId": str,
        "readOnlyFormsOutput": List[FormOutputTypeDef],
        "revision": str,
        "typeIdentifier": str,
        "typeRevision": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class AssetListingTypeDef(TypedDict):
    assetId: NotRequired[str]
    assetRevision: NotRequired[str]
    assetType: NotRequired[str]
    createdAt: NotRequired[datetime]
    forms: NotRequired[str]
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    latestTimeSeriesDataPointForms: NotRequired[List[TimeSeriesDataPointSummaryFormOutputTypeDef]]
    owningProjectId: NotRequired[str]

class ListingSummaryItemTypeDef(TypedDict):
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    listingId: NotRequired[str]
    listingRevision: NotRequired[str]

class ListingSummaryTypeDef(TypedDict):
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    listingId: NotRequired[str]
    listingRevision: NotRequired[str]

class SubscribedProductListingTypeDef(TypedDict):
    assetListings: NotRequired[List[AssetInDataProductListingItemTypeDef]]
    description: NotRequired[str]
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    name: NotRequired[str]

class ListAssetRevisionsOutputTypeDef(TypedDict):
    items: List[AssetRevisionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SubscribedAssetListingTypeDef(TypedDict):
    assetScope: NotRequired[AssetScopeTypeDef]
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    entityType: NotRequired[str]
    forms: NotRequired[str]
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]

class AssetTypeItemTypeDef(TypedDict):
    domainId: str
    formsOutput: Dict[str, FormEntryOutputTypeDef]
    name: str
    owningProjectId: str
    revision: str
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    description: NotRequired[str]
    originDomainId: NotRequired[str]
    originProjectId: NotRequired[str]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]

class CreateAssetTypeOutputTypeDef(TypedDict):
    createdAt: datetime
    createdBy: str
    description: str
    domainId: str
    formsOutput: Dict[str, FormEntryOutputTypeDef]
    name: str
    originDomainId: str
    originProjectId: str
    owningProjectId: str
    revision: str
    updatedAt: datetime
    updatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAssetTypeOutputTypeDef(TypedDict):
    createdAt: datetime
    createdBy: str
    description: str
    domainId: str
    formsOutput: Dict[str, FormEntryOutputTypeDef]
    name: str
    originDomainId: str
    originProjectId: str
    owningProjectId: str
    revision: str
    updatedAt: datetime
    updatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef

class LineageNodeTypeItemTypeDef(TypedDict):
    domainId: str
    formsOutput: Dict[str, FormEntryOutputTypeDef]
    revision: str
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    description: NotRequired[str]
    name: NotRequired[str]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]

AssetTypesForRuleUnionTypeDef = Union[AssetTypesForRuleTypeDef, AssetTypesForRuleOutputTypeDef]

class AuthenticationConfigurationPatchTypeDef(TypedDict):
    basicAuthenticationCredentials: NotRequired[BasicAuthenticationCredentialsTypeDef]
    secretArn: NotRequired[str]

class PostLineageEventInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    event: BlobTypeDef
    clientToken: NotRequired[str]

class PredictionConfigurationTypeDef(TypedDict):
    businessNameGeneration: NotRequired[BusinessNameGenerationConfigurationTypeDef]

class ProvisioningPropertiesTypeDef(TypedDict):
    cloudFormation: NotRequired[CloudFormationPropertiesTypeDef]

ColumnFilterConfigurationUnionTypeDef = Union[
    ColumnFilterConfigurationTypeDef, ColumnFilterConfigurationOutputTypeDef
]
ConfigurableEnvironmentActionTypeDef = TypedDict(
    "ConfigurableEnvironmentActionTypeDef",
    {
        "parameters": List[ConfigurableActionParameterTypeDef],
        "type": str,
        "auth": NotRequired[ConfigurableActionTypeAuthorizationType],
    },
)

class CreateAssetTypeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    formsInput: Mapping[str, FormEntryInputTypeDef]
    name: str
    owningProjectIdentifier: str
    description: NotRequired[str]

CreateDataProductOutputTypeDef = TypedDict(
    "CreateDataProductOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "formsOutput": List[FormOutputTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "items": List[DataProductItemOutputTypeDef],
        "name": str,
        "owningProjectId": str,
        "revision": str,
        "status": DataProductStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateDataProductRevisionOutputTypeDef = TypedDict(
    "CreateDataProductRevisionOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "formsOutput": List[FormOutputTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "items": List[DataProductItemOutputTypeDef],
        "name": str,
        "owningProjectId": str,
        "revision": str,
        "status": DataProductStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataProductOutputTypeDef = TypedDict(
    "GetDataProductOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "formsOutput": List[FormOutputTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "items": List[DataProductItemOutputTypeDef],
        "name": str,
        "owningProjectId": str,
        "revision": str,
        "status": DataProductStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateDataProductRevisionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    formsInput: NotRequired[Sequence[FormInputTypeDef]]
    glossaryTerms: NotRequired[Sequence[str]]
    items: NotRequired[Sequence[DataProductItemTypeDef]]

DataProductItemUnionTypeDef = Union[DataProductItemTypeDef, DataProductItemOutputTypeDef]
DataSourceSummaryTypeDef = TypedDict(
    "DataSourceSummaryTypeDef",
    {
        "dataSourceId": str,
        "domainId": str,
        "name": str,
        "status": DataSourceStatusType,
        "type": str,
        "connectionId": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "enableSetting": NotRequired[EnableSettingType],
        "environmentId": NotRequired[str],
        "lastRunAssetCount": NotRequired[int],
        "lastRunAt": NotRequired[datetime],
        "lastRunErrorMessage": NotRequired[DataSourceErrorMessageTypeDef],
        "lastRunStatus": NotRequired[DataSourceRunStatusType],
        "schedule": NotRequired[ScheduleConfigurationTypeDef],
        "updatedAt": NotRequired[datetime],
    },
)

class CreateDomainInputRequestTypeDef(TypedDict):
    domainExecutionRole: str
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    domainVersion: NotRequired[DomainVersionType]
    kmsKeyIdentifier: NotRequired[str]
    serviceRole: NotRequired[str]
    singleSignOn: NotRequired[SingleSignOnTypeDef]
    tags: NotRequired[Mapping[str, str]]

CreateDomainOutputTypeDef = TypedDict(
    "CreateDomainOutputTypeDef",
    {
        "arn": str,
        "description": str,
        "domainExecutionRole": str,
        "domainVersion": DomainVersionType,
        "id": str,
        "kmsKeyIdentifier": str,
        "name": str,
        "portalUrl": str,
        "rootDomainUnitId": str,
        "serviceRole": str,
        "singleSignOn": SingleSignOnTypeDef,
        "status": DomainStatusType,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDomainOutputTypeDef = TypedDict(
    "GetDomainOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "domainExecutionRole": str,
        "domainVersion": DomainVersionType,
        "id": str,
        "kmsKeyIdentifier": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "portalUrl": str,
        "rootDomainUnitId": str,
        "serviceRole": str,
        "singleSignOn": SingleSignOnTypeDef,
        "status": DomainStatusType,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class UpdateDomainInputRequestTypeDef(TypedDict):
    identifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    domainExecutionRole: NotRequired[str]
    name: NotRequired[str]
    serviceRole: NotRequired[str]
    singleSignOn: NotRequired[SingleSignOnTypeDef]

UpdateDomainOutputTypeDef = TypedDict(
    "UpdateDomainOutputTypeDef",
    {
        "description": str,
        "domainExecutionRole": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "rootDomainUnitId": str,
        "serviceRole": str,
        "singleSignOn": SingleSignOnTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateEnvironmentInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentProfileIdentifier: str
    name: str
    projectIdentifier: str
    deploymentOrder: NotRequired[int]
    description: NotRequired[str]
    environmentAccountIdentifier: NotRequired[str]
    environmentAccountRegion: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    environmentConfigurationId: NotRequired[str]
    glossaryTerms: NotRequired[Sequence[str]]
    userParameters: NotRequired[Sequence[EnvironmentParameterTypeDef]]

class CreateEnvironmentProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentBlueprintIdentifier: str
    name: str
    projectIdentifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    description: NotRequired[str]
    userParameters: NotRequired[Sequence[EnvironmentParameterTypeDef]]

class EnvironmentConfigurationUserParameterOutputTypeDef(TypedDict):
    environmentConfigurationName: NotRequired[str]
    environmentParameters: NotRequired[List[EnvironmentParameterTypeDef]]

class EnvironmentConfigurationUserParameterTypeDef(TypedDict):
    environmentConfigurationName: NotRequired[str]
    environmentParameters: NotRequired[Sequence[EnvironmentParameterTypeDef]]

class UpdateEnvironmentProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    description: NotRequired[str]
    name: NotRequired[str]
    userParameters: NotRequired[Sequence[EnvironmentParameterTypeDef]]

CreateEnvironmentProfileOutputTypeDef = TypedDict(
    "CreateEnvironmentProfileOutputTypeDef",
    {
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "environmentBlueprintId": str,
        "id": str,
        "name": str,
        "projectId": str,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetEnvironmentProfileOutputTypeDef = TypedDict(
    "GetEnvironmentProfileOutputTypeDef",
    {
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "environmentBlueprintId": str,
        "id": str,
        "name": str,
        "projectId": str,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateEnvironmentProfileOutputTypeDef = TypedDict(
    "UpdateEnvironmentProfileOutputTypeDef",
    {
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "environmentBlueprintId": str,
        "id": str,
        "name": str,
        "projectId": str,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateFormTypeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    model: ModelTypeDef
    name: str
    owningProjectIdentifier: str
    description: NotRequired[str]
    status: NotRequired[FormTypeStatusType]

class CreateGlossaryTermInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    glossaryIdentifier: str
    name: str
    clientToken: NotRequired[str]
    longDescription: NotRequired[str]
    shortDescription: NotRequired[str]
    status: NotRequired[GlossaryTermStatusType]
    termRelations: NotRequired[TermRelationsTypeDef]

class UpdateGlossaryTermInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    glossaryIdentifier: NotRequired[str]
    longDescription: NotRequired[str]
    name: NotRequired[str]
    shortDescription: NotRequired[str]
    status: NotRequired[GlossaryTermStatusType]
    termRelations: NotRequired[TermRelationsTypeDef]

CreateGlossaryTermOutputTypeDef = TypedDict(
    "CreateGlossaryTermOutputTypeDef",
    {
        "domainId": str,
        "glossaryId": str,
        "id": str,
        "longDescription": str,
        "name": str,
        "shortDescription": str,
        "status": GlossaryTermStatusType,
        "termRelations": TermRelationsOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetGlossaryTermOutputTypeDef = TypedDict(
    "GetGlossaryTermOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "glossaryId": str,
        "id": str,
        "longDescription": str,
        "name": str,
        "shortDescription": str,
        "status": GlossaryTermStatusType,
        "termRelations": TermRelationsOutputTypeDef,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GlossaryTermItemTypeDef = TypedDict(
    "GlossaryTermItemTypeDef",
    {
        "domainId": str,
        "glossaryId": str,
        "id": str,
        "name": str,
        "status": GlossaryTermStatusType,
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "longDescription": NotRequired[str],
        "shortDescription": NotRequired[str],
        "termRelations": NotRequired[TermRelationsOutputTypeDef],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
UpdateGlossaryTermOutputTypeDef = TypedDict(
    "UpdateGlossaryTermOutputTypeDef",
    {
        "domainId": str,
        "glossaryId": str,
        "id": str,
        "longDescription": str,
        "name": str,
        "shortDescription": str,
        "status": GlossaryTermStatusType,
        "termRelations": TermRelationsOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateProjectFromProjectProfilePolicyGrantDetailUnionTypeDef = Union[
    CreateProjectFromProjectProfilePolicyGrantDetailTypeDef,
    CreateProjectFromProjectProfilePolicyGrantDetailOutputTypeDef,
]

class CreateProjectMembershipInputRequestTypeDef(TypedDict):
    designation: UserDesignationType
    domainIdentifier: str
    member: MemberTypeDef
    projectIdentifier: str

class DeleteProjectMembershipInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    member: MemberTypeDef
    projectIdentifier: str

ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef",
    {
        "createdBy": str,
        "domainId": str,
        "id": str,
        "name": str,
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "domainUnitId": NotRequired[str],
        "failureReasons": NotRequired[List[ProjectDeletionErrorTypeDef]],
        "projectStatus": NotRequired[ProjectStatusType],
        "updatedAt": NotRequired[datetime],
    },
)
CreateSubscriptionTargetInputRequestTypeDef = TypedDict(
    "CreateSubscriptionTargetInputRequestTypeDef",
    {
        "applicableAssetTypes": Sequence[str],
        "authorizedPrincipals": Sequence[str],
        "domainIdentifier": str,
        "environmentIdentifier": str,
        "manageAccessRole": str,
        "name": str,
        "subscriptionTargetConfig": Sequence[SubscriptionTargetFormTypeDef],
        "type": str,
        "clientToken": NotRequired[str],
        "provider": NotRequired[str],
    },
)
CreateSubscriptionTargetOutputTypeDef = TypedDict(
    "CreateSubscriptionTargetOutputTypeDef",
    {
        "applicableAssetTypes": List[str],
        "authorizedPrincipals": List[str],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "manageAccessRole": str,
        "name": str,
        "projectId": str,
        "provider": str,
        "subscriptionTargetConfig": List[SubscriptionTargetFormTypeDef],
        "type": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSubscriptionTargetOutputTypeDef = TypedDict(
    "GetSubscriptionTargetOutputTypeDef",
    {
        "applicableAssetTypes": List[str],
        "authorizedPrincipals": List[str],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "manageAccessRole": str,
        "name": str,
        "projectId": str,
        "provider": str,
        "subscriptionTargetConfig": List[SubscriptionTargetFormTypeDef],
        "type": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SubscriptionTargetSummaryTypeDef = TypedDict(
    "SubscriptionTargetSummaryTypeDef",
    {
        "applicableAssetTypes": List[str],
        "authorizedPrincipals": List[str],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "name": str,
        "projectId": str,
        "provider": str,
        "subscriptionTargetConfig": List[SubscriptionTargetFormTypeDef],
        "type": str,
        "manageAccessRole": NotRequired[str],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)

class UpdateSubscriptionTargetInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str
    applicableAssetTypes: NotRequired[Sequence[str]]
    authorizedPrincipals: NotRequired[Sequence[str]]
    manageAccessRole: NotRequired[str]
    name: NotRequired[str]
    provider: NotRequired[str]
    subscriptionTargetConfig: NotRequired[Sequence[SubscriptionTargetFormTypeDef]]

UpdateSubscriptionTargetOutputTypeDef = TypedDict(
    "UpdateSubscriptionTargetOutputTypeDef",
    {
        "applicableAssetTypes": List[str],
        "authorizedPrincipals": List[str],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "manageAccessRole": str,
        "name": str,
        "projectId": str,
        "provider": str,
        "subscriptionTargetConfig": List[SubscriptionTargetFormTypeDef],
        "type": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListDataProductRevisionsOutputTypeDef(TypedDict):
    items: List[DataProductRevisionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DataSourceRunActivityTypeDef(TypedDict):
    createdAt: datetime
    dataAssetStatus: DataAssetActivityStatusType
    dataSourceRunId: str
    database: str
    projectId: str
    technicalName: str
    updatedAt: datetime
    dataAssetId: NotRequired[str]
    errorMessage: NotRequired[DataSourceErrorMessageTypeDef]
    lineageSummary: NotRequired[LineageInfoTypeDef]
    technicalDescription: NotRequired[str]

DataSourceRunSummaryTypeDef = TypedDict(
    "DataSourceRunSummaryTypeDef",
    {
        "createdAt": datetime,
        "dataSourceId": str,
        "id": str,
        "projectId": str,
        "status": DataSourceRunStatusType,
        "type": DataSourceRunTypeType,
        "updatedAt": datetime,
        "errorMessage": NotRequired[DataSourceErrorMessageTypeDef],
        "lineageSummary": NotRequired[DataSourceRunLineageSummaryTypeDef],
        "runStatisticsForAssets": NotRequired[RunStatisticsForAssetsTypeDef],
        "startedAt": NotRequired[datetime],
        "stoppedAt": NotRequired[datetime],
    },
)
GetDataSourceRunOutputTypeDef = TypedDict(
    "GetDataSourceRunOutputTypeDef",
    {
        "createdAt": datetime,
        "dataSourceConfigurationSnapshot": str,
        "dataSourceId": str,
        "domainId": str,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "id": str,
        "lineageSummary": DataSourceRunLineageSummaryTypeDef,
        "projectId": str,
        "runStatisticsForAssets": RunStatisticsForAssetsTypeDef,
        "startedAt": datetime,
        "status": DataSourceRunStatusType,
        "stoppedAt": datetime,
        "type": DataSourceRunTypeType,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartDataSourceRunOutputTypeDef = TypedDict(
    "StartDataSourceRunOutputTypeDef",
    {
        "createdAt": datetime,
        "dataSourceConfigurationSnapshot": str,
        "dataSourceId": str,
        "domainId": str,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "id": str,
        "projectId": str,
        "runStatisticsForAssets": RunStatisticsForAssetsTypeDef,
        "startedAt": datetime,
        "status": DataSourceRunStatusType,
        "stoppedAt": datetime,
        "type": DataSourceRunTypeType,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class DeploymentTypeDef(TypedDict):
    deploymentId: NotRequired[str]
    deploymentStatus: NotRequired[DeploymentStatusType]
    deploymentType: NotRequired[DeploymentTypeType]
    failureReason: NotRequired[EnvironmentErrorTypeDef]
    isDeploymentComplete: NotRequired[bool]
    messages: NotRequired[List[str]]

class EnvironmentDeploymentDetailsOutputTypeDef(TypedDict):
    environmentFailureReasons: NotRequired[Dict[str, List[EnvironmentErrorTypeDef]]]
    overallDeploymentStatus: NotRequired[OverallDeploymentStatusType]

class EnvironmentDeploymentDetailsTypeDef(TypedDict):
    environmentFailureReasons: NotRequired[Mapping[str, Sequence[EnvironmentErrorTypeDef]]]
    overallDeploymentStatus: NotRequired[OverallDeploymentStatusType]

class ListDomainsOutputTypeDef(TypedDict):
    items: List[DomainSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ProjectGrantFilterTypeDef(TypedDict):
    domainUnitFilter: NotRequired[DomainUnitFilterForProjectTypeDef]

class DomainUnitPolicyGrantPrincipalOutputTypeDef(TypedDict):
    domainUnitDesignation: Literal["OWNER"]
    domainUnitGrantFilter: NotRequired[DomainUnitGrantFilterOutputTypeDef]
    domainUnitIdentifier: NotRequired[str]

DomainUnitGrantFilterUnionTypeDef = Union[
    DomainUnitGrantFilterTypeDef, DomainUnitGrantFilterOutputTypeDef
]

class DomainUnitOwnerPropertiesTypeDef(TypedDict):
    group: NotRequired[DomainUnitGroupPropertiesTypeDef]
    user: NotRequired[DomainUnitUserPropertiesTypeDef]

class ListDomainUnitsForParentOutputTypeDef(TypedDict):
    items: List[DomainUnitSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class RuleTargetTypeDef(TypedDict):
    domainUnitTarget: NotRequired[DomainUnitTargetTypeDef]

class EnvironmentConfigurationParametersDetailsOutputTypeDef(TypedDict):
    parameterOverrides: NotRequired[List[EnvironmentConfigurationParameterTypeDef]]
    resolvedParameters: NotRequired[List[EnvironmentConfigurationParameterTypeDef]]
    ssmPath: NotRequired[str]

class EnvironmentConfigurationParametersDetailsTypeDef(TypedDict):
    parameterOverrides: NotRequired[Sequence[EnvironmentConfigurationParameterTypeDef]]
    resolvedParameters: NotRequired[Sequence[EnvironmentConfigurationParameterTypeDef]]
    ssmPath: NotRequired[str]

class ListEnvironmentProfilesOutputTypeDef(TypedDict):
    items: List[EnvironmentProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListEnvironmentsOutputTypeDef(TypedDict):
    items: List[EnvironmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SubscribedAssetTypeDef(TypedDict):
    assetId: str
    assetRevision: str
    status: SubscriptionGrantStatusType
    assetScope: NotRequired[AssetScopeTypeDef]
    failureCause: NotRequired[FailureCauseTypeDef]
    failureTimestamp: NotRequired[datetime]
    grantedTimestamp: NotRequired[datetime]
    targetName: NotRequired[str]

class UpdateSubscriptionGrantStatusInputRequestTypeDef(TypedDict):
    assetIdentifier: str
    domainIdentifier: str
    identifier: str
    status: SubscriptionGrantStatusType
    failureCause: NotRequired[FailureCauseTypeDef]
    targetName: NotRequired[str]

FilterClausePaginatorTypeDef = TypedDict(
    "FilterClausePaginatorTypeDef",
    {
        "and": NotRequired[Sequence[Mapping[str, Any]]],
        "filter": NotRequired[FilterTypeDef],
        "or": NotRequired[Sequence[Mapping[str, Any]]],
    },
)
FilterClauseTypeDef = TypedDict(
    "FilterClauseTypeDef",
    {
        "and": NotRequired[Sequence[Mapping[str, Any]]],
        "filter": NotRequired[FilterTypeDef],
        "or": NotRequired[Sequence[Mapping[str, Any]]],
    },
)

class RelationalFilterConfigurationOutputTypeDef(TypedDict):
    databaseName: str
    filterExpressions: NotRequired[List[FilterExpressionTypeDef]]
    schemaName: NotRequired[str]

class RelationalFilterConfigurationTypeDef(TypedDict):
    databaseName: str
    filterExpressions: NotRequired[Sequence[FilterExpressionTypeDef]]
    schemaName: NotRequired[str]

class FormTypeDataTypeDef(TypedDict):
    domainId: str
    name: str
    revision: str
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    description: NotRequired[str]
    imports: NotRequired[List[ImportTypeDef]]
    model: NotRequired[ModelTypeDef]
    originDomainId: NotRequired[str]
    originProjectId: NotRequired[str]
    owningProjectId: NotRequired[str]
    status: NotRequired[FormTypeStatusType]

class GetFormTypeOutputTypeDef(TypedDict):
    createdAt: datetime
    createdBy: str
    description: str
    domainId: str
    imports: List[ImportTypeDef]
    model: ModelTypeDef
    name: str
    originDomainId: str
    originProjectId: str
    owningProjectId: str
    revision: str
    status: FormTypeStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class JobRunSummaryTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    domainId: NotRequired[str]
    endTime: NotRequired[datetime]
    error: NotRequired[JobRunErrorTypeDef]
    jobId: NotRequired[str]
    jobType: NotRequired[Literal["LINEAGE"]]
    runId: NotRequired[str]
    runMode: NotRequired[JobRunModeType]
    startTime: NotRequired[datetime]
    status: NotRequired[JobRunStatusType]

class GetLineageNodeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    eventTimestamp: NotRequired[TimestampTypeDef]

class ListLineageEventsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    processingStatus: NotRequired[LineageEventProcessingStatusType]
    sortOrder: NotRequired[SortOrderType]
    timestampAfter: NotRequired[TimestampTypeDef]
    timestampBefore: NotRequired[TimestampTypeDef]

class ListLineageNodeHistoryInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    direction: NotRequired[EdgeDirectionType]
    eventTimestampGTE: NotRequired[TimestampTypeDef]
    eventTimestampLTE: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortOrder: NotRequired[SortOrderType]

ListNotificationsInputRequestTypeDef = TypedDict(
    "ListNotificationsInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "type": NotificationTypeType,
        "afterTimestamp": NotRequired[TimestampTypeDef],
        "beforeTimestamp": NotRequired[TimestampTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "subjects": NotRequired[Sequence[str]],
        "taskStatus": NotRequired[TaskStatusType],
    },
)

class ListTimeSeriesDataPointsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    formName: str
    endedAt: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    startedAt: NotRequired[TimestampTypeDef]

class TimeSeriesDataPointFormInputTypeDef(TypedDict):
    formName: str
    timestamp: TimestampTypeDef
    typeIdentifier: str
    content: NotRequired[str]
    typeRevision: NotRequired[str]

GetLineageNodeOutputTypeDef = TypedDict(
    "GetLineageNodeOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "downstreamNodes": List[LineageNodeReferenceTypeDef],
        "eventTimestamp": datetime,
        "formsOutput": List[FormOutputTypeDef],
        "id": str,
        "name": str,
        "sourceIdentifier": str,
        "typeName": str,
        "typeRevision": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "upstreamNodes": List[LineageNodeReferenceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetMetadataGenerationRunOutputTypeDef = TypedDict(
    "GetMetadataGenerationRunOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "owningProjectId": str,
        "status": MetadataGenerationRunStatusType,
        "target": MetadataGenerationRunTargetTypeDef,
        "type": Literal["BUSINESS_DESCRIPTIONS"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
MetadataGenerationRunItemTypeDef = TypedDict(
    "MetadataGenerationRunItemTypeDef",
    {
        "domainId": str,
        "id": str,
        "owningProjectId": str,
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "status": NotRequired[MetadataGenerationRunStatusType],
        "target": NotRequired[MetadataGenerationRunTargetTypeDef],
        "type": NotRequired[Literal["BUSINESS_DESCRIPTIONS"]],
    },
)
StartMetadataGenerationRunInputRequestTypeDef = TypedDict(
    "StartMetadataGenerationRunInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "owningProjectIdentifier": str,
        "target": MetadataGenerationRunTargetTypeDef,
        "type": Literal["BUSINESS_DESCRIPTIONS"],
        "clientToken": NotRequired[str],
    },
)

class GetTimeSeriesDataPointOutputTypeDef(TypedDict):
    domainId: str
    entityId: str
    entityType: TimeSeriesEntityTypeType
    form: TimeSeriesDataPointFormOutputTypeDef
    formName: str
    ResponseMetadata: ResponseMetadataTypeDef

class PostTimeSeriesDataPointsOutputTypeDef(TypedDict):
    domainId: str
    entityId: str
    entityType: TimeSeriesEntityTypeType
    forms: List[TimeSeriesDataPointFormOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GlueSelfGrantStatusOutputTypeDef(TypedDict):
    selfGrantStatusDetails: List[SelfGrantStatusDetailTypeDef]

class RedshiftSelfGrantStatusOutputTypeDef(TypedDict):
    selfGrantStatusDetails: List[SelfGrantStatusDetailTypeDef]

class GrantedEntityInputTypeDef(TypedDict):
    listing: NotRequired[ListingRevisionInputTypeDef]

class GrantedEntityTypeDef(TypedDict):
    listing: NotRequired[ListingRevisionTypeDef]

class SearchGroupProfilesOutputTypeDef(TypedDict):
    items: List[GroupProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

InExpressionUnionTypeDef = Union[InExpressionTypeDef, InExpressionOutputTypeDef]

class ProvisioningConfigurationOutputTypeDef(TypedDict):
    lakeFormationConfiguration: NotRequired[LakeFormationConfigurationOutputTypeDef]

LakeFormationConfigurationUnionTypeDef = Union[
    LakeFormationConfigurationTypeDef, LakeFormationConfigurationOutputTypeDef
]

class ListLineageNodeHistoryOutputTypeDef(TypedDict):
    nodes: List[LineageNodeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class LineageRunDetailsTypeDef(TypedDict):
    sqlQueryRunDetails: NotRequired[LineageSqlQueryRunDetailsTypeDef]

class RedshiftLineageSyncConfigurationInputTypeDef(TypedDict):
    enabled: NotRequired[bool]
    schedule: NotRequired[LineageSyncScheduleTypeDef]

class RedshiftLineageSyncConfigurationOutputTypeDef(TypedDict):
    enabled: NotRequired[bool]
    lineageJobId: NotRequired[str]
    schedule: NotRequired[LineageSyncScheduleTypeDef]

class ListAssetFiltersInputListAssetFiltersPaginateTypeDef(TypedDict):
    assetIdentifier: str
    domainIdentifier: str
    status: NotRequired[FilterStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssetRevisionsInputListAssetRevisionsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListConnectionsInputListConnectionsPaginateTypeDef = TypedDict(
    "ListConnectionsInputListConnectionsPaginateTypeDef",
    {
        "domainIdentifier": str,
        "projectIdentifier": str,
        "environmentIdentifier": NotRequired[str],
        "name": NotRequired[str],
        "sortBy": NotRequired[Literal["NAME"]],
        "sortOrder": NotRequired[SortOrderType],
        "type": NotRequired[ConnectionTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListDataProductRevisionsInputListDataProductRevisionsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataSourceRunActivitiesInputListDataSourceRunActivitiesPaginateTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    status: NotRequired[DataAssetActivityStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataSourceRunsInputListDataSourceRunsPaginateTypeDef(TypedDict):
    dataSourceIdentifier: str
    domainIdentifier: str
    status: NotRequired[DataSourceRunStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListDataSourcesInputListDataSourcesPaginateTypeDef = TypedDict(
    "ListDataSourcesInputListDataSourcesPaginateTypeDef",
    {
        "domainIdentifier": str,
        "projectIdentifier": str,
        "connectionIdentifier": NotRequired[str],
        "environmentIdentifier": NotRequired[str],
        "name": NotRequired[str],
        "status": NotRequired[DataSourceStatusType],
        "type": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListDomainUnitsForParentInputListDomainUnitsForParentPaginateTypeDef(TypedDict):
    domainIdentifier: str
    parentDomainUnitIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDomainsInputListDomainsPaginateTypeDef(TypedDict):
    status: NotRequired[DomainStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEntityOwnersInputListEntityOwnersPaginateTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: Literal["DOMAIN_UNIT"]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentActionsInputListEnvironmentActionsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentBlueprintConfigurationsInputListEnvironmentBlueprintConfigurationsPaginateTypeDef(
    TypedDict
):
    domainIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentBlueprintsInputListEnvironmentBlueprintsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    managed: NotRequired[bool]
    name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentProfilesInputListEnvironmentProfilesPaginateTypeDef(TypedDict):
    domainIdentifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    name: NotRequired[str]
    projectIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentsInputListEnvironmentsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    environmentProfileIdentifier: NotRequired[str]
    name: NotRequired[str]
    provider: NotRequired[str]
    status: NotRequired[EnvironmentStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListJobRunsInputListJobRunsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    jobIdentifier: str
    sortOrder: NotRequired[SortOrderType]
    status: NotRequired[JobRunStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLineageEventsInputListLineageEventsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    processingStatus: NotRequired[LineageEventProcessingStatusType]
    sortOrder: NotRequired[SortOrderType]
    timestampAfter: NotRequired[TimestampTypeDef]
    timestampBefore: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLineageNodeHistoryInputListLineageNodeHistoryPaginateTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    direction: NotRequired[EdgeDirectionType]
    eventTimestampGTE: NotRequired[TimestampTypeDef]
    eventTimestampLTE: NotRequired[TimestampTypeDef]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListMetadataGenerationRunsInputListMetadataGenerationRunsPaginateTypeDef = TypedDict(
    "ListMetadataGenerationRunsInputListMetadataGenerationRunsPaginateTypeDef",
    {
        "domainIdentifier": str,
        "status": NotRequired[MetadataGenerationRunStatusType],
        "type": NotRequired[Literal["BUSINESS_DESCRIPTIONS"]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListNotificationsInputListNotificationsPaginateTypeDef = TypedDict(
    "ListNotificationsInputListNotificationsPaginateTypeDef",
    {
        "domainIdentifier": str,
        "type": NotificationTypeType,
        "afterTimestamp": NotRequired[TimestampTypeDef],
        "beforeTimestamp": NotRequired[TimestampTypeDef],
        "subjects": NotRequired[Sequence[str]],
        "taskStatus": NotRequired[TaskStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListPolicyGrantsInputListPolicyGrantsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TargetEntityTypeType
    policyType: ManagedPolicyTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProjectMembershipsInputListProjectMembershipsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    sortBy: NotRequired[Literal["NAME"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProjectProfilesInputListProjectProfilesPaginateTypeDef(TypedDict):
    domainIdentifier: str
    name: NotRequired[str]
    sortBy: NotRequired[Literal["NAME"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProjectsInputListProjectsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    groupIdentifier: NotRequired[str]
    name: NotRequired[str]
    userIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRulesInputListRulesPaginateTypeDef(TypedDict):
    domainIdentifier: str
    targetIdentifier: str
    targetType: Literal["DOMAIN_UNIT"]
    action: NotRequired[Literal["CREATE_SUBSCRIPTION_REQUEST"]]
    assetTypes: NotRequired[Sequence[str]]
    dataProduct: NotRequired[bool]
    includeCascaded: NotRequired[bool]
    projectIds: NotRequired[Sequence[str]]
    ruleType: NotRequired[Literal["METADATA_FORM_ENFORCEMENT"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionGrantsInputListSubscriptionGrantsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    environmentId: NotRequired[str]
    owningProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    subscribedListingId: NotRequired[str]
    subscriptionId: NotRequired[str]
    subscriptionTargetId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionRequestsInputListSubscriptionRequestsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    approverProjectId: NotRequired[str]
    owningProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    status: NotRequired[SubscriptionRequestStatusType]
    subscribedListingId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionTargetsInputListSubscriptionTargetsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionsInputListSubscriptionsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    approverProjectId: NotRequired[str]
    owningProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    status: NotRequired[SubscriptionStatusType]
    subscribedListingId: NotRequired[str]
    subscriptionRequestIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTimeSeriesDataPointsInputListTimeSeriesDataPointsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    formName: str
    endedAt: NotRequired[TimestampTypeDef]
    startedAt: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchGroupProfilesInputSearchGroupProfilesPaginateTypeDef(TypedDict):
    domainIdentifier: str
    groupType: GroupSearchTypeType
    searchText: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchUserProfilesInputSearchUserProfilesPaginateTypeDef(TypedDict):
    domainIdentifier: str
    userType: UserSearchTypeType
    searchText: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProjectProfilesOutputTypeDef(TypedDict):
    items: List[ProjectProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class MemberDetailsTypeDef(TypedDict):
    group: NotRequired[GroupDetailsTypeDef]
    user: NotRequired[UserDetailsTypeDef]

class MetadataFormEnforcementDetailOutputTypeDef(TypedDict):
    requiredMetadataForms: NotRequired[List[MetadataFormReferenceTypeDef]]

class MetadataFormEnforcementDetailTypeDef(TypedDict):
    requiredMetadataForms: NotRequired[Sequence[MetadataFormReferenceTypeDef]]

class OpenLineageRunEventSummaryTypeDef(TypedDict):
    eventType: NotRequired[OpenLineageRunStateType]
    inputs: NotRequired[List[NameIdentifierTypeDef]]
    job: NotRequired[NameIdentifierTypeDef]
    outputs: NotRequired[List[NameIdentifierTypeDef]]
    runId: NotRequired[str]

NotInExpressionUnionTypeDef = Union[NotInExpressionTypeDef, NotInExpressionOutputTypeDef]
RowFilterExpressionOutputTypeDef = TypedDict(
    "RowFilterExpressionOutputTypeDef",
    {
        "equalTo": NotRequired[EqualToExpressionTypeDef],
        "greaterThan": NotRequired[GreaterThanExpressionTypeDef],
        "greaterThanOrEqualTo": NotRequired[GreaterThanOrEqualToExpressionTypeDef],
        "in": NotRequired[InExpressionOutputTypeDef],
        "isNotNull": NotRequired[IsNotNullExpressionTypeDef],
        "isNull": NotRequired[IsNullExpressionTypeDef],
        "lessThan": NotRequired[LessThanExpressionTypeDef],
        "lessThanOrEqualTo": NotRequired[LessThanOrEqualToExpressionTypeDef],
        "like": NotRequired[LikeExpressionTypeDef],
        "notEqualTo": NotRequired[NotEqualToExpressionTypeDef],
        "notIn": NotRequired[NotInExpressionOutputTypeDef],
        "notLike": NotRequired[NotLikeExpressionTypeDef],
    },
)

class TopicTypeDef(TypedDict):
    resource: NotificationResourceTypeDef
    role: NotificationRoleType
    subject: str

class OAuth2PropertiesOutputTypeDef(TypedDict):
    authorizationCodeProperties: NotRequired[AuthorizationCodePropertiesTypeDef]
    oAuth2ClientApplication: NotRequired[OAuth2ClientApplicationTypeDef]
    oAuth2Credentials: NotRequired[GlueOAuth2CredentialsTypeDef]
    oAuth2GrantType: NotRequired[OAuth2GrantTypeType]
    tokenUrl: NotRequired[str]
    tokenUrlParametersMap: NotRequired[Dict[str, str]]

class OAuth2PropertiesTypeDef(TypedDict):
    authorizationCodeProperties: NotRequired[AuthorizationCodePropertiesTypeDef]
    oAuth2ClientApplication: NotRequired[OAuth2ClientApplicationTypeDef]
    oAuth2Credentials: NotRequired[GlueOAuth2CredentialsTypeDef]
    oAuth2GrantType: NotRequired[OAuth2GrantTypeType]
    tokenUrl: NotRequired[str]
    tokenUrlParametersMap: NotRequired[Mapping[str, str]]

class PolicyGrantDetailOutputTypeDef(TypedDict):
    addToProjectMemberPool: NotRequired[AddToProjectMemberPoolPolicyGrantDetailTypeDef]
    createAssetType: NotRequired[CreateAssetTypePolicyGrantDetailTypeDef]
    createDomainUnit: NotRequired[CreateDomainUnitPolicyGrantDetailTypeDef]
    createEnvironment: NotRequired[Dict[str, Any]]
    createEnvironmentFromBlueprint: NotRequired[Dict[str, Any]]
    createEnvironmentProfile: NotRequired[CreateEnvironmentProfilePolicyGrantDetailTypeDef]
    createFormType: NotRequired[CreateFormTypePolicyGrantDetailTypeDef]
    createGlossary: NotRequired[CreateGlossaryPolicyGrantDetailTypeDef]
    createProject: NotRequired[CreateProjectPolicyGrantDetailTypeDef]
    createProjectFromProjectProfile: NotRequired[
        CreateProjectFromProjectProfilePolicyGrantDetailOutputTypeDef
    ]
    delegateCreateEnvironmentProfile: NotRequired[Dict[str, Any]]
    overrideDomainUnitOwners: NotRequired[OverrideDomainUnitOwnersPolicyGrantDetailTypeDef]
    overrideProjectOwners: NotRequired[OverrideProjectOwnersPolicyGrantDetailTypeDef]

class OwnerPropertiesOutputTypeDef(TypedDict):
    group: NotRequired[OwnerGroupPropertiesOutputTypeDef]
    user: NotRequired[OwnerUserPropertiesOutputTypeDef]

class OwnerPropertiesTypeDef(TypedDict):
    group: NotRequired[OwnerGroupPropertiesTypeDef]
    user: NotRequired[OwnerUserPropertiesTypeDef]

PhysicalConnectionRequirementsUnionTypeDef = Union[
    PhysicalConnectionRequirementsTypeDef, PhysicalConnectionRequirementsOutputTypeDef
]

class RuleScopeOutputTypeDef(TypedDict):
    assetType: NotRequired[AssetTypesForRuleOutputTypeDef]
    dataProduct: NotRequired[bool]
    project: NotRequired[ProjectsForRuleOutputTypeDef]

ProjectsForRuleUnionTypeDef = Union[ProjectsForRuleTypeDef, ProjectsForRuleOutputTypeDef]

class RedshiftCredentialsTypeDef(TypedDict):
    secretArn: NotRequired[str]
    usernamePassword: NotRequired[UsernamePasswordTypeDef]

class SparkEmrPropertiesOutputTypeDef(TypedDict):
    computeArn: NotRequired[str]
    credentials: NotRequired[UsernamePasswordTypeDef]
    credentialsExpiration: NotRequired[datetime]
    governanceType: NotRequired[GovernanceTypeType]
    instanceProfileArn: NotRequired[str]
    javaVirtualEnv: NotRequired[str]
    livyEndpoint: NotRequired[str]
    logUri: NotRequired[str]
    pythonVirtualEnv: NotRequired[str]
    runtimeRole: NotRequired[str]
    trustedCertificatesS3Uri: NotRequired[str]

class RedshiftStorageTypeDef(TypedDict):
    redshiftClusterSource: NotRequired[RedshiftClusterStorageTypeDef]
    redshiftServerlessSource: NotRequired[RedshiftServerlessStorageTypeDef]

class RejectPredictionsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    clientToken: NotRequired[str]
    rejectChoices: NotRequired[Sequence[RejectChoiceTypeDef]]
    rejectRule: NotRequired[RejectRuleTypeDef]
    revision: NotRequired[str]

class SparkGluePropertiesInputTypeDef(TypedDict):
    additionalArgs: NotRequired[SparkGlueArgsTypeDef]
    glueConnectionName: NotRequired[str]
    glueVersion: NotRequired[str]
    idleTimeout: NotRequired[int]
    javaVirtualEnv: NotRequired[str]
    numberOfWorkers: NotRequired[int]
    pythonVirtualEnv: NotRequired[str]
    workerType: NotRequired[str]

class SparkGluePropertiesOutputTypeDef(TypedDict):
    additionalArgs: NotRequired[SparkGlueArgsTypeDef]
    glueConnectionName: NotRequired[str]
    glueVersion: NotRequired[str]
    idleTimeout: NotRequired[int]
    javaVirtualEnv: NotRequired[str]
    numberOfWorkers: NotRequired[int]
    pythonVirtualEnv: NotRequired[str]
    workerType: NotRequired[str]

class UserProfileDetailsTypeDef(TypedDict):
    iam: NotRequired[IamUserProfileDetailsTypeDef]
    sso: NotRequired[SsoUserProfileDetailsTypeDef]

class SubscribedPrincipalInputTypeDef(TypedDict):
    project: NotRequired[SubscribedProjectInputTypeDef]

class SubscribedPrincipalTypeDef(TypedDict):
    project: NotRequired[SubscribedProjectTypeDef]

UserPolicyGrantPrincipalUnionTypeDef = Union[
    UserPolicyGrantPrincipalTypeDef, UserPolicyGrantPrincipalOutputTypeDef
]

class CreateEnvironmentActionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    name: str
    parameters: ActionParametersTypeDef
    description: NotRequired[str]

CreateEnvironmentActionOutputTypeDef = TypedDict(
    "CreateEnvironmentActionOutputTypeDef",
    {
        "description": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "name": str,
        "parameters": ActionParametersTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnvironmentActionSummaryTypeDef = TypedDict(
    "EnvironmentActionSummaryTypeDef",
    {
        "domainId": str,
        "environmentId": str,
        "id": str,
        "name": str,
        "parameters": ActionParametersTypeDef,
        "description": NotRequired[str],
    },
)
GetEnvironmentActionOutputTypeDef = TypedDict(
    "GetEnvironmentActionOutputTypeDef",
    {
        "description": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "name": str,
        "parameters": ActionParametersTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class UpdateEnvironmentActionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str
    description: NotRequired[str]
    name: NotRequired[str]
    parameters: NotRequired[ActionParametersTypeDef]

UpdateEnvironmentActionOutputTypeDef = TypedDict(
    "UpdateEnvironmentActionOutputTypeDef",
    {
        "description": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "name": str,
        "parameters": ActionParametersTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class AssetItemTypeDef(TypedDict):
    domainId: str
    identifier: str
    name: str
    owningProjectId: str
    typeIdentifier: str
    typeRevision: str
    additionalAttributes: NotRequired[AssetItemAdditionalAttributesTypeDef]
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    description: NotRequired[str]
    externalIdentifier: NotRequired[str]
    firstRevisionCreatedAt: NotRequired[datetime]
    firstRevisionCreatedBy: NotRequired[str]
    glossaryTerms: NotRequired[List[str]]

class AssetListingItemTypeDef(TypedDict):
    additionalAttributes: NotRequired[AssetListingItemAdditionalAttributesTypeDef]
    createdAt: NotRequired[datetime]
    description: NotRequired[str]
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    entityType: NotRequired[str]
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    listingCreatedBy: NotRequired[str]
    listingId: NotRequired[str]
    listingRevision: NotRequired[str]
    listingUpdatedBy: NotRequired[str]
    name: NotRequired[str]
    owningProjectId: NotRequired[str]

class DataProductListingItemTypeDef(TypedDict):
    additionalAttributes: NotRequired[DataProductListingItemAdditionalAttributesTypeDef]
    createdAt: NotRequired[datetime]
    description: NotRequired[str]
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    items: NotRequired[List[ListingSummaryItemTypeDef]]
    listingCreatedBy: NotRequired[str]
    listingId: NotRequired[str]
    listingRevision: NotRequired[str]
    listingUpdatedBy: NotRequired[str]
    name: NotRequired[str]
    owningProjectId: NotRequired[str]

class DataProductListingTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    dataProductId: NotRequired[str]
    dataProductRevision: NotRequired[str]
    forms: NotRequired[str]
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    items: NotRequired[List[ListingSummaryTypeDef]]
    owningProjectId: NotRequired[str]

class SubscribedListingItemTypeDef(TypedDict):
    assetListing: NotRequired[SubscribedAssetListingTypeDef]
    productListing: NotRequired[SubscribedProductListingTypeDef]

class GlueConnectionPatchTypeDef(TypedDict):
    authenticationConfiguration: NotRequired[AuthenticationConfigurationPatchTypeDef]
    connectionProperties: NotRequired[Mapping[str, str]]
    description: NotRequired[str]

class CreateAssetInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    owningProjectIdentifier: str
    typeIdentifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    externalIdentifier: NotRequired[str]
    formsInput: NotRequired[Sequence[FormInputTypeDef]]
    glossaryTerms: NotRequired[Sequence[str]]
    predictionConfiguration: NotRequired[PredictionConfigurationTypeDef]
    typeRevision: NotRequired[str]

CreateAssetOutputTypeDef = TypedDict(
    "CreateAssetOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "externalIdentifier": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "formsOutput": List[FormOutputTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "latestTimeSeriesDataPointFormsOutput": List[TimeSeriesDataPointSummaryFormOutputTypeDef],
        "listing": AssetListingDetailsTypeDef,
        "name": str,
        "owningProjectId": str,
        "predictionConfiguration": PredictionConfigurationTypeDef,
        "readOnlyFormsOutput": List[FormOutputTypeDef],
        "revision": str,
        "typeIdentifier": str,
        "typeRevision": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateAssetRevisionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    formsInput: NotRequired[Sequence[FormInputTypeDef]]
    glossaryTerms: NotRequired[Sequence[str]]
    predictionConfiguration: NotRequired[PredictionConfigurationTypeDef]
    typeRevision: NotRequired[str]

CreateAssetRevisionOutputTypeDef = TypedDict(
    "CreateAssetRevisionOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "externalIdentifier": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "formsOutput": List[FormOutputTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "latestTimeSeriesDataPointFormsOutput": List[TimeSeriesDataPointSummaryFormOutputTypeDef],
        "listing": AssetListingDetailsTypeDef,
        "name": str,
        "owningProjectId": str,
        "predictionConfiguration": PredictionConfigurationTypeDef,
        "readOnlyFormsOutput": List[FormOutputTypeDef],
        "revision": str,
        "typeIdentifier": str,
        "typeRevision": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnvironmentBlueprintSummaryTypeDef = TypedDict(
    "EnvironmentBlueprintSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "provider": str,
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "updatedAt": NotRequired[datetime],
    },
)
GetEnvironmentBlueprintOutputTypeDef = TypedDict(
    "GetEnvironmentBlueprintOutputTypeDef",
    {
        "createdAt": datetime,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "description": str,
        "glossaryTerms": List[str],
        "id": str,
        "name": str,
        "provider": str,
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateDataProductInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    owningProjectIdentifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    formsInput: NotRequired[Sequence[FormInputTypeDef]]
    glossaryTerms: NotRequired[Sequence[str]]
    items: NotRequired[Sequence[DataProductItemUnionTypeDef]]

class ListDataSourcesOutputTypeDef(TypedDict):
    items: List[DataSourceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

EnvironmentConfigurationUserParameterUnionTypeDef = Union[
    EnvironmentConfigurationUserParameterTypeDef, EnvironmentConfigurationUserParameterOutputTypeDef
]

class PolicyGrantDetailTypeDef(TypedDict):
    addToProjectMemberPool: NotRequired[AddToProjectMemberPoolPolicyGrantDetailTypeDef]
    createAssetType: NotRequired[CreateAssetTypePolicyGrantDetailTypeDef]
    createDomainUnit: NotRequired[CreateDomainUnitPolicyGrantDetailTypeDef]
    createEnvironment: NotRequired[Mapping[str, Any]]
    createEnvironmentFromBlueprint: NotRequired[Mapping[str, Any]]
    createEnvironmentProfile: NotRequired[CreateEnvironmentProfilePolicyGrantDetailTypeDef]
    createFormType: NotRequired[CreateFormTypePolicyGrantDetailTypeDef]
    createGlossary: NotRequired[CreateGlossaryPolicyGrantDetailTypeDef]
    createProject: NotRequired[CreateProjectPolicyGrantDetailTypeDef]
    createProjectFromProjectProfile: NotRequired[
        CreateProjectFromProjectProfilePolicyGrantDetailUnionTypeDef
    ]
    delegateCreateEnvironmentProfile: NotRequired[Mapping[str, Any]]
    overrideDomainUnitOwners: NotRequired[OverrideDomainUnitOwnersPolicyGrantDetailTypeDef]
    overrideProjectOwners: NotRequired[OverrideProjectOwnersPolicyGrantDetailTypeDef]

class ListProjectsOutputTypeDef(TypedDict):
    items: List[ProjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSubscriptionTargetsOutputTypeDef(TypedDict):
    items: List[SubscriptionTargetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDataSourceRunActivitiesOutputTypeDef(TypedDict):
    items: List[DataSourceRunActivityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDataSourceRunsOutputTypeDef(TypedDict):
    items: List[DataSourceRunSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

CreateEnvironmentOutputTypeDef = TypedDict(
    "CreateEnvironmentOutputTypeDef",
    {
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdAt": datetime,
        "createdBy": str,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "description": str,
        "domainId": str,
        "environmentActions": List[ConfigurableEnvironmentActionTypeDef],
        "environmentBlueprintId": str,
        "environmentProfileId": str,
        "glossaryTerms": List[str],
        "id": str,
        "lastDeployment": DeploymentTypeDef,
        "name": str,
        "projectId": str,
        "provider": str,
        "provisionedResources": List[ResourceTypeDef],
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "status": EnvironmentStatusType,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetEnvironmentOutputTypeDef = TypedDict(
    "GetEnvironmentOutputTypeDef",
    {
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdAt": datetime,
        "createdBy": str,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "description": str,
        "domainId": str,
        "environmentActions": List[ConfigurableEnvironmentActionTypeDef],
        "environmentBlueprintId": str,
        "environmentProfileId": str,
        "glossaryTerms": List[str],
        "id": str,
        "lastDeployment": DeploymentTypeDef,
        "name": str,
        "projectId": str,
        "provider": str,
        "provisionedResources": List[ResourceTypeDef],
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "status": EnvironmentStatusType,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateEnvironmentOutputTypeDef = TypedDict(
    "UpdateEnvironmentOutputTypeDef",
    {
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdAt": datetime,
        "createdBy": str,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "description": str,
        "domainId": str,
        "environmentActions": List[ConfigurableEnvironmentActionTypeDef],
        "environmentBlueprintId": str,
        "environmentProfileId": str,
        "glossaryTerms": List[str],
        "id": str,
        "lastDeployment": DeploymentTypeDef,
        "name": str,
        "projectId": str,
        "provider": str,
        "provisionedResources": List[ResourceTypeDef],
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "status": EnvironmentStatusType,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateProjectOutputTypeDef = TypedDict(
    "CreateProjectOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "environmentDeploymentDetails": EnvironmentDeploymentDetailsOutputTypeDef,
        "failureReasons": List[ProjectDeletionErrorTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "projectProfileId": str,
        "projectStatus": ProjectStatusType,
        "userParameters": List[EnvironmentConfigurationUserParameterOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetProjectOutputTypeDef = TypedDict(
    "GetProjectOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "environmentDeploymentDetails": EnvironmentDeploymentDetailsOutputTypeDef,
        "failureReasons": List[ProjectDeletionErrorTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "projectProfileId": str,
        "projectStatus": ProjectStatusType,
        "userParameters": List[EnvironmentConfigurationUserParameterOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateProjectOutputTypeDef = TypedDict(
    "UpdateProjectOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "environmentDeploymentDetails": EnvironmentDeploymentDetailsOutputTypeDef,
        "failureReasons": List[ProjectDeletionErrorTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "projectProfileId": str,
        "projectStatus": ProjectStatusType,
        "userParameters": List[EnvironmentConfigurationUserParameterOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class UpdateProjectInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    description: NotRequired[str]
    environmentDeploymentDetails: NotRequired[EnvironmentDeploymentDetailsTypeDef]
    glossaryTerms: NotRequired[Sequence[str]]
    name: NotRequired[str]

class ProjectPolicyGrantPrincipalTypeDef(TypedDict):
    projectDesignation: ProjectDesignationType
    projectGrantFilter: NotRequired[ProjectGrantFilterTypeDef]
    projectIdentifier: NotRequired[str]

class DomainUnitPolicyGrantPrincipalTypeDef(TypedDict):
    domainUnitDesignation: Literal["OWNER"]
    domainUnitGrantFilter: NotRequired[DomainUnitGrantFilterUnionTypeDef]
    domainUnitIdentifier: NotRequired[str]

CreateDomainUnitOutputTypeDef = TypedDict(
    "CreateDomainUnitOutputTypeDef",
    {
        "ancestorDomainUnitIds": List[str],
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "id": str,
        "name": str,
        "owners": List[DomainUnitOwnerPropertiesTypeDef],
        "parentDomainUnitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDomainUnitOutputTypeDef = TypedDict(
    "GetDomainUnitOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "lastUpdatedBy": str,
        "name": str,
        "owners": List[DomainUnitOwnerPropertiesTypeDef],
        "parentDomainUnitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateDomainUnitOutputTypeDef = TypedDict(
    "UpdateDomainUnitOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "lastUpdatedBy": str,
        "name": str,
        "owners": List[DomainUnitOwnerPropertiesTypeDef],
        "parentDomainUnitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnvironmentConfigurationOutputTypeDef = TypedDict(
    "EnvironmentConfigurationOutputTypeDef",
    {
        "awsAccount": AwsAccountTypeDef,
        "awsRegion": RegionTypeDef,
        "environmentBlueprintId": str,
        "name": str,
        "configurationParameters": NotRequired[
            EnvironmentConfigurationParametersDetailsOutputTypeDef
        ],
        "deploymentMode": NotRequired[DeploymentModeType],
        "deploymentOrder": NotRequired[int],
        "description": NotRequired[str],
        "id": NotRequired[str],
    },
)
EnvironmentConfigurationParametersDetailsUnionTypeDef = Union[
    EnvironmentConfigurationParametersDetailsTypeDef,
    EnvironmentConfigurationParametersDetailsOutputTypeDef,
]

class SearchInputSearchPaginateTypeDef(TypedDict):
    domainIdentifier: str
    searchScope: InventorySearchScopeType
    additionalAttributes: NotRequired[Sequence[SearchOutputAdditionalAttributeType]]
    filters: NotRequired[FilterClausePaginatorTypeDef]
    owningProjectIdentifier: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    searchText: NotRequired[str]
    sort: NotRequired[SearchSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchListingsInputSearchListingsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    additionalAttributes: NotRequired[Sequence[SearchOutputAdditionalAttributeType]]
    filters: NotRequired[FilterClausePaginatorTypeDef]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    searchText: NotRequired[str]
    sort: NotRequired[SearchSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchTypesInputSearchTypesPaginateTypeDef(TypedDict):
    domainIdentifier: str
    managed: bool
    searchScope: TypesSearchScopeType
    filters: NotRequired[FilterClausePaginatorTypeDef]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    searchText: NotRequired[str]
    sort: NotRequired[SearchSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    searchScope: InventorySearchScopeType
    additionalAttributes: NotRequired[Sequence[SearchOutputAdditionalAttributeType]]
    filters: NotRequired[FilterClauseTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    owningProjectIdentifier: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    searchText: NotRequired[str]
    sort: NotRequired[SearchSortTypeDef]

class SearchListingsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    additionalAttributes: NotRequired[Sequence[SearchOutputAdditionalAttributeType]]
    filters: NotRequired[FilterClauseTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    searchText: NotRequired[str]
    sort: NotRequired[SearchSortTypeDef]

class SearchTypesInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    managed: bool
    searchScope: TypesSearchScopeType
    filters: NotRequired[FilterClauseTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    searchText: NotRequired[str]
    sort: NotRequired[SearchSortTypeDef]

class GlueRunConfigurationOutputTypeDef(TypedDict):
    relationalFilterConfigurations: List[RelationalFilterConfigurationOutputTypeDef]
    accountId: NotRequired[str]
    autoImportDataQualityResult: NotRequired[bool]
    catalogName: NotRequired[str]
    dataAccessRole: NotRequired[str]
    region: NotRequired[str]

RelationalFilterConfigurationUnionTypeDef = Union[
    RelationalFilterConfigurationTypeDef, RelationalFilterConfigurationOutputTypeDef
]

class SearchTypesResultItemTypeDef(TypedDict):
    assetTypeItem: NotRequired[AssetTypeItemTypeDef]
    formTypeItem: NotRequired[FormTypeDataTypeDef]
    lineageNodeTypeItem: NotRequired[LineageNodeTypeItemTypeDef]

class ListJobRunsOutputTypeDef(TypedDict):
    items: List[JobRunSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PostTimeSeriesDataPointsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    forms: Sequence[TimeSeriesDataPointFormInputTypeDef]
    clientToken: NotRequired[str]

class ListMetadataGenerationRunsOutputTypeDef(TypedDict):
    items: List[MetadataGenerationRunItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SelfGrantStatusOutputTypeDef(TypedDict):
    glueSelfGrantStatus: NotRequired[GlueSelfGrantStatusOutputTypeDef]
    redshiftSelfGrantStatus: NotRequired[RedshiftSelfGrantStatusOutputTypeDef]

class CreateSubscriptionGrantInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    grantedEntity: GrantedEntityInputTypeDef
    assetTargetNames: NotRequired[Sequence[AssetTargetNameMapTypeDef]]
    clientToken: NotRequired[str]
    subscriptionTargetIdentifier: NotRequired[str]

CreateSubscriptionGrantOutputTypeDef = TypedDict(
    "CreateSubscriptionGrantOutputTypeDef",
    {
        "assets": List[SubscribedAssetTypeDef],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "id": str,
        "status": SubscriptionGrantOverallStatusType,
        "subscriptionId": str,
        "subscriptionTargetId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteSubscriptionGrantOutputTypeDef = TypedDict(
    "DeleteSubscriptionGrantOutputTypeDef",
    {
        "assets": List[SubscribedAssetTypeDef],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "id": str,
        "status": SubscriptionGrantOverallStatusType,
        "subscriptionId": str,
        "subscriptionTargetId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSubscriptionGrantOutputTypeDef = TypedDict(
    "GetSubscriptionGrantOutputTypeDef",
    {
        "assets": List[SubscribedAssetTypeDef],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "id": str,
        "status": SubscriptionGrantOverallStatusType,
        "subscriptionId": str,
        "subscriptionTargetId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SubscriptionGrantSummaryTypeDef = TypedDict(
    "SubscriptionGrantSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "id": str,
        "status": SubscriptionGrantOverallStatusType,
        "subscriptionTargetId": str,
        "updatedAt": datetime,
        "assets": NotRequired[List[SubscribedAssetTypeDef]],
        "subscriptionId": NotRequired[str],
        "updatedBy": NotRequired[str],
    },
)
UpdateSubscriptionGrantStatusOutputTypeDef = TypedDict(
    "UpdateSubscriptionGrantStatusOutputTypeDef",
    {
        "assets": List[SubscribedAssetTypeDef],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "id": str,
        "status": SubscriptionGrantOverallStatusType,
        "subscriptionId": str,
        "subscriptionTargetId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class EnvironmentBlueprintConfigurationItemTypeDef(TypedDict):
    domainId: str
    environmentBlueprintId: str
    createdAt: NotRequired[datetime]
    enabledRegions: NotRequired[List[str]]
    environmentRolePermissionBoundary: NotRequired[str]
    manageAccessRoleArn: NotRequired[str]
    provisioningConfigurations: NotRequired[List[ProvisioningConfigurationOutputTypeDef]]
    provisioningRoleArn: NotRequired[str]
    regionalParameters: NotRequired[Dict[str, Dict[str, str]]]
    updatedAt: NotRequired[datetime]

class GetEnvironmentBlueprintConfigurationOutputTypeDef(TypedDict):
    createdAt: datetime
    domainId: str
    enabledRegions: List[str]
    environmentBlueprintId: str
    environmentRolePermissionBoundary: str
    manageAccessRoleArn: str
    provisioningConfigurations: List[ProvisioningConfigurationOutputTypeDef]
    provisioningRoleArn: str
    regionalParameters: Dict[str, Dict[str, str]]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class PutEnvironmentBlueprintConfigurationOutputTypeDef(TypedDict):
    createdAt: datetime
    domainId: str
    enabledRegions: List[str]
    environmentBlueprintId: str
    environmentRolePermissionBoundary: str
    manageAccessRoleArn: str
    provisioningConfigurations: List[ProvisioningConfigurationOutputTypeDef]
    provisioningRoleArn: str
    regionalParameters: Dict[str, Dict[str, str]]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ProvisioningConfigurationTypeDef(TypedDict):
    lakeFormationConfiguration: NotRequired[LakeFormationConfigurationUnionTypeDef]

class JobRunDetailsTypeDef(TypedDict):
    lineageRunDetails: NotRequired[LineageRunDetailsTypeDef]

class ProjectMemberTypeDef(TypedDict):
    designation: UserDesignationType
    memberDetails: MemberDetailsTypeDef

class RuleDetailOutputTypeDef(TypedDict):
    metadataFormEnforcementDetail: NotRequired[MetadataFormEnforcementDetailOutputTypeDef]

MetadataFormEnforcementDetailUnionTypeDef = Union[
    MetadataFormEnforcementDetailTypeDef, MetadataFormEnforcementDetailOutputTypeDef
]

class EventSummaryTypeDef(TypedDict):
    openLineageRunEventSummary: NotRequired[OpenLineageRunEventSummaryTypeDef]

RowFilterExpressionTypeDef = TypedDict(
    "RowFilterExpressionTypeDef",
    {
        "equalTo": NotRequired[EqualToExpressionTypeDef],
        "greaterThan": NotRequired[GreaterThanExpressionTypeDef],
        "greaterThanOrEqualTo": NotRequired[GreaterThanOrEqualToExpressionTypeDef],
        "in": NotRequired[InExpressionUnionTypeDef],
        "isNotNull": NotRequired[IsNotNullExpressionTypeDef],
        "isNull": NotRequired[IsNullExpressionTypeDef],
        "lessThan": NotRequired[LessThanExpressionTypeDef],
        "lessThanOrEqualTo": NotRequired[LessThanOrEqualToExpressionTypeDef],
        "like": NotRequired[LikeExpressionTypeDef],
        "notEqualTo": NotRequired[NotEqualToExpressionTypeDef],
        "notIn": NotRequired[NotInExpressionUnionTypeDef],
        "notLike": NotRequired[NotLikeExpressionTypeDef],
    },
)
RowFilterOutputTypeDef = TypedDict(
    "RowFilterOutputTypeDef",
    {
        "and": NotRequired[List[Dict[str, Any]]],
        "expression": NotRequired[RowFilterExpressionOutputTypeDef],
        "or": NotRequired[List[Dict[str, Any]]],
    },
)
NotificationOutputTypeDef = TypedDict(
    "NotificationOutputTypeDef",
    {
        "actionLink": str,
        "creationTimestamp": datetime,
        "domainIdentifier": str,
        "identifier": str,
        "lastUpdatedTimestamp": datetime,
        "message": str,
        "title": str,
        "topic": TopicTypeDef,
        "type": NotificationTypeType,
        "metadata": NotRequired[Dict[str, str]],
        "status": NotRequired[TaskStatusType],
    },
)

class AuthenticationConfigurationTypeDef(TypedDict):
    authenticationType: NotRequired[AuthenticationTypeType]
    oAuth2Properties: NotRequired[OAuth2PropertiesOutputTypeDef]
    secretArn: NotRequired[str]

OAuth2PropertiesUnionTypeDef = Union[OAuth2PropertiesTypeDef, OAuth2PropertiesOutputTypeDef]

class ListEntityOwnersOutputTypeDef(TypedDict):
    owners: List[OwnerPropertiesOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AddEntityOwnerInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: Literal["DOMAIN_UNIT"]
    owner: OwnerPropertiesTypeDef
    clientToken: NotRequired[str]

class RemoveEntityOwnerInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: Literal["DOMAIN_UNIT"]
    owner: OwnerPropertiesTypeDef
    clientToken: NotRequired[str]

class RuleSummaryTypeDef(TypedDict):
    action: NotRequired[Literal["CREATE_SUBSCRIPTION_REQUEST"]]
    identifier: NotRequired[str]
    lastUpdatedBy: NotRequired[str]
    name: NotRequired[str]
    revision: NotRequired[str]
    ruleType: NotRequired[Literal["METADATA_FORM_ENFORCEMENT"]]
    scope: NotRequired[RuleScopeOutputTypeDef]
    target: NotRequired[RuleTargetTypeDef]
    targetType: NotRequired[Literal["DOMAIN_UNIT"]]
    updatedAt: NotRequired[datetime]

class RuleScopeTypeDef(TypedDict):
    assetType: NotRequired[AssetTypesForRuleUnionTypeDef]
    dataProduct: NotRequired[bool]
    project: NotRequired[ProjectsForRuleUnionTypeDef]

class RedshiftPropertiesInputTypeDef(TypedDict):
    credentials: NotRequired[RedshiftCredentialsTypeDef]
    databaseName: NotRequired[str]
    host: NotRequired[str]
    lineageSync: NotRequired[RedshiftLineageSyncConfigurationInputTypeDef]
    port: NotRequired[int]
    storage: NotRequired[RedshiftStoragePropertiesTypeDef]

class RedshiftPropertiesOutputTypeDef(TypedDict):
    credentials: NotRequired[RedshiftCredentialsTypeDef]
    databaseName: NotRequired[str]
    isProvisionedSecret: NotRequired[bool]
    jdbcIamUrl: NotRequired[str]
    jdbcUrl: NotRequired[str]
    lineageSync: NotRequired[RedshiftLineageSyncConfigurationOutputTypeDef]
    redshiftTempDir: NotRequired[str]
    status: NotRequired[ConnectionStatusType]
    storage: NotRequired[RedshiftStoragePropertiesTypeDef]

class RedshiftPropertiesPatchTypeDef(TypedDict):
    credentials: NotRequired[RedshiftCredentialsTypeDef]
    databaseName: NotRequired[str]
    host: NotRequired[str]
    lineageSync: NotRequired[RedshiftLineageSyncConfigurationInputTypeDef]
    port: NotRequired[int]
    storage: NotRequired[RedshiftStoragePropertiesTypeDef]

class RedshiftRunConfigurationInputTypeDef(TypedDict):
    relationalFilterConfigurations: Sequence[RelationalFilterConfigurationTypeDef]
    dataAccessRole: NotRequired[str]
    redshiftCredentialConfiguration: NotRequired[RedshiftCredentialConfigurationTypeDef]
    redshiftStorage: NotRequired[RedshiftStorageTypeDef]

class RedshiftRunConfigurationOutputTypeDef(TypedDict):
    redshiftStorage: RedshiftStorageTypeDef
    relationalFilterConfigurations: List[RelationalFilterConfigurationOutputTypeDef]
    accountId: NotRequired[str]
    dataAccessRole: NotRequired[str]
    redshiftCredentialConfiguration: NotRequired[RedshiftCredentialConfigurationTypeDef]
    region: NotRequired[str]

CreateUserProfileOutputTypeDef = TypedDict(
    "CreateUserProfileOutputTypeDef",
    {
        "details": UserProfileDetailsTypeDef,
        "domainId": str,
        "id": str,
        "status": UserProfileStatusType,
        "type": UserProfileTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetUserProfileOutputTypeDef = TypedDict(
    "GetUserProfileOutputTypeDef",
    {
        "details": UserProfileDetailsTypeDef,
        "domainId": str,
        "id": str,
        "status": UserProfileStatusType,
        "type": UserProfileTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateUserProfileOutputTypeDef = TypedDict(
    "UpdateUserProfileOutputTypeDef",
    {
        "details": UserProfileDetailsTypeDef,
        "domainId": str,
        "id": str,
        "status": UserProfileStatusType,
        "type": UserProfileTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UserProfileSummaryTypeDef = TypedDict(
    "UserProfileSummaryTypeDef",
    {
        "details": NotRequired[UserProfileDetailsTypeDef],
        "domainId": NotRequired[str],
        "id": NotRequired[str],
        "status": NotRequired[UserProfileStatusType],
        "type": NotRequired[UserProfileTypeType],
    },
)

class CreateSubscriptionRequestInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    requestReason: str
    subscribedListings: Sequence[SubscribedListingInputTypeDef]
    subscribedPrincipals: Sequence[SubscribedPrincipalInputTypeDef]
    clientToken: NotRequired[str]
    metadataForms: NotRequired[Sequence[FormInputTypeDef]]

class ListEnvironmentActionsOutputTypeDef(TypedDict):
    items: List[EnvironmentActionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SearchInventoryResultItemTypeDef(TypedDict):
    assetItem: NotRequired[AssetItemTypeDef]
    dataProductItem: NotRequired[DataProductResultItemTypeDef]
    glossaryItem: NotRequired[GlossaryItemTypeDef]
    glossaryTermItem: NotRequired[GlossaryTermItemTypeDef]

class SearchResultItemTypeDef(TypedDict):
    assetListing: NotRequired[AssetListingItemTypeDef]
    dataProductListing: NotRequired[DataProductListingItemTypeDef]

class ListingItemTypeDef(TypedDict):
    assetListing: NotRequired[AssetListingTypeDef]
    dataProductListing: NotRequired[DataProductListingTypeDef]

SubscribedListingTypeDef = TypedDict(
    "SubscribedListingTypeDef",
    {
        "description": str,
        "id": str,
        "item": SubscribedListingItemTypeDef,
        "name": str,
        "ownerProjectId": str,
        "ownerProjectName": NotRequired[str],
        "revision": NotRequired[str],
    },
)

class GluePropertiesPatchTypeDef(TypedDict):
    glueConnectionInput: NotRequired[GlueConnectionPatchTypeDef]

class ListEnvironmentBlueprintsOutputTypeDef(TypedDict):
    items: List[EnvironmentBlueprintSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateProjectInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    description: NotRequired[str]
    domainUnitId: NotRequired[str]
    glossaryTerms: NotRequired[Sequence[str]]
    projectProfileId: NotRequired[str]
    userParameters: NotRequired[Sequence[EnvironmentConfigurationUserParameterUnionTypeDef]]

class PolicyGrantPrincipalOutputTypeDef(TypedDict):
    domainUnit: NotRequired[DomainUnitPolicyGrantPrincipalOutputTypeDef]
    group: NotRequired[GroupPolicyGrantPrincipalTypeDef]
    project: NotRequired[ProjectPolicyGrantPrincipalTypeDef]
    user: NotRequired[UserPolicyGrantPrincipalOutputTypeDef]

DomainUnitPolicyGrantPrincipalUnionTypeDef = Union[
    DomainUnitPolicyGrantPrincipalTypeDef, DomainUnitPolicyGrantPrincipalOutputTypeDef
]
CreateProjectProfileOutputTypeDef = TypedDict(
    "CreateProjectProfileOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "environmentConfigurations": List[EnvironmentConfigurationOutputTypeDef],
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "status": StatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetProjectProfileOutputTypeDef = TypedDict(
    "GetProjectProfileOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "environmentConfigurations": List[EnvironmentConfigurationOutputTypeDef],
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "status": StatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateProjectProfileOutputTypeDef = TypedDict(
    "UpdateProjectProfileOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "environmentConfigurations": List[EnvironmentConfigurationOutputTypeDef],
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "status": StatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnvironmentConfigurationTypeDef = TypedDict(
    "EnvironmentConfigurationTypeDef",
    {
        "awsAccount": AwsAccountTypeDef,
        "awsRegion": RegionTypeDef,
        "environmentBlueprintId": str,
        "name": str,
        "configurationParameters": NotRequired[
            EnvironmentConfigurationParametersDetailsUnionTypeDef
        ],
        "deploymentMode": NotRequired[DeploymentModeType],
        "deploymentOrder": NotRequired[int],
        "description": NotRequired[str],
        "id": NotRequired[str],
    },
)

class GlueRunConfigurationInputTypeDef(TypedDict):
    relationalFilterConfigurations: Sequence[RelationalFilterConfigurationUnionTypeDef]
    autoImportDataQualityResult: NotRequired[bool]
    catalogName: NotRequired[str]
    dataAccessRole: NotRequired[str]

class SearchTypesOutputTypeDef(TypedDict):
    items: List[SearchTypesResultItemTypeDef]
    totalMatchCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSubscriptionGrantsOutputTypeDef(TypedDict):
    items: List[SubscriptionGrantSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListEnvironmentBlueprintConfigurationsOutputTypeDef(TypedDict):
    items: List[EnvironmentBlueprintConfigurationItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ProvisioningConfigurationUnionTypeDef = Union[
    ProvisioningConfigurationTypeDef, ProvisioningConfigurationOutputTypeDef
]
GetJobRunOutputTypeDef = TypedDict(
    "GetJobRunOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "details": JobRunDetailsTypeDef,
        "domainId": str,
        "endTime": datetime,
        "error": JobRunErrorTypeDef,
        "id": str,
        "jobId": str,
        "jobType": Literal["LINEAGE"],
        "runMode": JobRunModeType,
        "startTime": datetime,
        "status": JobRunStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListProjectMembershipsOutputTypeDef(TypedDict):
    members: List[ProjectMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateRuleOutputTypeDef(TypedDict):
    action: Literal["CREATE_SUBSCRIPTION_REQUEST"]
    createdAt: datetime
    createdBy: str
    description: str
    detail: RuleDetailOutputTypeDef
    identifier: str
    name: str
    ruleType: Literal["METADATA_FORM_ENFORCEMENT"]
    scope: RuleScopeOutputTypeDef
    target: RuleTargetTypeDef
    targetType: Literal["DOMAIN_UNIT"]
    ResponseMetadata: ResponseMetadataTypeDef

class GetRuleOutputTypeDef(TypedDict):
    action: Literal["CREATE_SUBSCRIPTION_REQUEST"]
    createdAt: datetime
    createdBy: str
    description: str
    detail: RuleDetailOutputTypeDef
    identifier: str
    lastUpdatedBy: str
    name: str
    revision: str
    ruleType: Literal["METADATA_FORM_ENFORCEMENT"]
    scope: RuleScopeOutputTypeDef
    target: RuleTargetTypeDef
    targetType: Literal["DOMAIN_UNIT"]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRuleOutputTypeDef(TypedDict):
    action: Literal["CREATE_SUBSCRIPTION_REQUEST"]
    createdAt: datetime
    createdBy: str
    description: str
    detail: RuleDetailOutputTypeDef
    identifier: str
    lastUpdatedBy: str
    name: str
    revision: str
    ruleType: Literal["METADATA_FORM_ENFORCEMENT"]
    scope: RuleScopeOutputTypeDef
    target: RuleTargetTypeDef
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class RuleDetailTypeDef(TypedDict):
    metadataFormEnforcementDetail: NotRequired[MetadataFormEnforcementDetailUnionTypeDef]

LineageEventSummaryTypeDef = TypedDict(
    "LineageEventSummaryTypeDef",
    {
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "domainId": NotRequired[str],
        "eventSummary": NotRequired[EventSummaryTypeDef],
        "eventTime": NotRequired[datetime],
        "id": NotRequired[str],
        "processingStatus": NotRequired[LineageEventProcessingStatusType],
    },
)
RowFilterExpressionUnionTypeDef = Union[
    RowFilterExpressionTypeDef, RowFilterExpressionOutputTypeDef
]

class RowFilterConfigurationOutputTypeDef(TypedDict):
    rowFilter: RowFilterOutputTypeDef
    sensitive: NotRequired[bool]

class ListNotificationsOutputTypeDef(TypedDict):
    notifications: List[NotificationOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GlueConnectionTypeDef(TypedDict):
    athenaProperties: NotRequired[Dict[str, str]]
    authenticationConfiguration: NotRequired[AuthenticationConfigurationTypeDef]
    compatibleComputeEnvironments: NotRequired[List[ComputeEnvironmentsType]]
    connectionProperties: NotRequired[Dict[str, str]]
    connectionSchemaVersion: NotRequired[int]
    connectionType: NotRequired[ConnectionTypeType]
    creationTime: NotRequired[datetime]
    description: NotRequired[str]
    lastConnectionValidationTime: NotRequired[datetime]
    lastUpdatedBy: NotRequired[str]
    lastUpdatedTime: NotRequired[datetime]
    matchCriteria: NotRequired[List[str]]
    name: NotRequired[str]
    physicalConnectionRequirements: NotRequired[PhysicalConnectionRequirementsOutputTypeDef]
    pythonProperties: NotRequired[Dict[str, str]]
    sparkProperties: NotRequired[Dict[str, str]]
    status: NotRequired[ConnectionStatusType]
    statusReason: NotRequired[str]

class AuthenticationConfigurationInputTypeDef(TypedDict):
    authenticationType: NotRequired[AuthenticationTypeType]
    basicAuthenticationCredentials: NotRequired[BasicAuthenticationCredentialsTypeDef]
    customAuthenticationCredentials: NotRequired[Mapping[str, str]]
    kmsKeyArn: NotRequired[str]
    oAuth2Properties: NotRequired[OAuth2PropertiesUnionTypeDef]
    secretArn: NotRequired[str]

class ListRulesOutputTypeDef(TypedDict):
    items: List[RuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ConnectionPropertiesOutputTypeDef(TypedDict):
    athenaProperties: NotRequired[AthenaPropertiesOutputTypeDef]
    glueProperties: NotRequired[GluePropertiesOutputTypeDef]
    hyperPodProperties: NotRequired[HyperPodPropertiesOutputTypeDef]
    iamProperties: NotRequired[IamPropertiesOutputTypeDef]
    redshiftProperties: NotRequired[RedshiftPropertiesOutputTypeDef]
    sparkEmrProperties: NotRequired[SparkEmrPropertiesOutputTypeDef]
    sparkGlueProperties: NotRequired[SparkGluePropertiesOutputTypeDef]

class DataSourceConfigurationOutputTypeDef(TypedDict):
    glueRunConfiguration: NotRequired[GlueRunConfigurationOutputTypeDef]
    redshiftRunConfiguration: NotRequired[RedshiftRunConfigurationOutputTypeDef]
    sageMakerRunConfiguration: NotRequired[SageMakerRunConfigurationOutputTypeDef]

class SearchUserProfilesOutputTypeDef(TypedDict):
    items: List[UserProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SearchOutputTypeDef(TypedDict):
    items: List[SearchInventoryResultItemTypeDef]
    totalMatchCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SearchListingsOutputTypeDef(TypedDict):
    items: List[SearchResultItemTypeDef]
    totalMatchCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

GetListingOutputTypeDef = TypedDict(
    "GetListingOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "id": str,
        "item": ListingItemTypeDef,
        "listingRevision": str,
        "name": str,
        "status": ListingStatusType,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AcceptSubscriptionRequestOutputTypeDef = TypedDict(
    "AcceptSubscriptionRequestOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "decisionComment": str,
        "domainId": str,
        "existingSubscriptionId": str,
        "id": str,
        "metadataForms": List[FormOutputTypeDef],
        "requestReason": str,
        "reviewerId": str,
        "status": SubscriptionRequestStatusType,
        "subscribedListings": List[SubscribedListingTypeDef],
        "subscribedPrincipals": List[SubscribedPrincipalTypeDef],
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CancelSubscriptionOutputTypeDef = TypedDict(
    "CancelSubscriptionOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "retainPermissions": bool,
        "status": SubscriptionStatusType,
        "subscribedListing": SubscribedListingTypeDef,
        "subscribedPrincipal": SubscribedPrincipalTypeDef,
        "subscriptionRequestId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateSubscriptionRequestOutputTypeDef = TypedDict(
    "CreateSubscriptionRequestOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "decisionComment": str,
        "domainId": str,
        "existingSubscriptionId": str,
        "id": str,
        "metadataForms": List[FormOutputTypeDef],
        "requestReason": str,
        "reviewerId": str,
        "status": SubscriptionRequestStatusType,
        "subscribedListings": List[SubscribedListingTypeDef],
        "subscribedPrincipals": List[SubscribedPrincipalTypeDef],
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSubscriptionOutputTypeDef = TypedDict(
    "GetSubscriptionOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "retainPermissions": bool,
        "status": SubscriptionStatusType,
        "subscribedListing": SubscribedListingTypeDef,
        "subscribedPrincipal": SubscribedPrincipalTypeDef,
        "subscriptionRequestId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSubscriptionRequestDetailsOutputTypeDef = TypedDict(
    "GetSubscriptionRequestDetailsOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "decisionComment": str,
        "domainId": str,
        "existingSubscriptionId": str,
        "id": str,
        "metadataForms": List[FormOutputTypeDef],
        "requestReason": str,
        "reviewerId": str,
        "status": SubscriptionRequestStatusType,
        "subscribedListings": List[SubscribedListingTypeDef],
        "subscribedPrincipals": List[SubscribedPrincipalTypeDef],
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RejectSubscriptionRequestOutputTypeDef = TypedDict(
    "RejectSubscriptionRequestOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "decisionComment": str,
        "domainId": str,
        "existingSubscriptionId": str,
        "id": str,
        "metadataForms": List[FormOutputTypeDef],
        "requestReason": str,
        "reviewerId": str,
        "status": SubscriptionRequestStatusType,
        "subscribedListings": List[SubscribedListingTypeDef],
        "subscribedPrincipals": List[SubscribedPrincipalTypeDef],
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RevokeSubscriptionOutputTypeDef = TypedDict(
    "RevokeSubscriptionOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "retainPermissions": bool,
        "status": SubscriptionStatusType,
        "subscribedListing": SubscribedListingTypeDef,
        "subscribedPrincipal": SubscribedPrincipalTypeDef,
        "subscriptionRequestId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SubscriptionRequestSummaryTypeDef = TypedDict(
    "SubscriptionRequestSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "requestReason": str,
        "status": SubscriptionRequestStatusType,
        "subscribedListings": List[SubscribedListingTypeDef],
        "subscribedPrincipals": List[SubscribedPrincipalTypeDef],
        "updatedAt": datetime,
        "decisionComment": NotRequired[str],
        "existingSubscriptionId": NotRequired[str],
        "metadataFormsSummary": NotRequired[List[MetadataFormSummaryTypeDef]],
        "reviewerId": NotRequired[str],
        "updatedBy": NotRequired[str],
    },
)
SubscriptionSummaryTypeDef = TypedDict(
    "SubscriptionSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "status": SubscriptionStatusType,
        "subscribedListing": SubscribedListingTypeDef,
        "subscribedPrincipal": SubscribedPrincipalTypeDef,
        "updatedAt": datetime,
        "retainPermissions": NotRequired[bool],
        "subscriptionRequestId": NotRequired[str],
        "updatedBy": NotRequired[str],
    },
)
UpdateSubscriptionRequestOutputTypeDef = TypedDict(
    "UpdateSubscriptionRequestOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "decisionComment": str,
        "domainId": str,
        "existingSubscriptionId": str,
        "id": str,
        "metadataForms": List[FormOutputTypeDef],
        "requestReason": str,
        "reviewerId": str,
        "status": SubscriptionRequestStatusType,
        "subscribedListings": List[SubscribedListingTypeDef],
        "subscribedPrincipals": List[SubscribedPrincipalTypeDef],
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ConnectionPropertiesPatchTypeDef(TypedDict):
    athenaProperties: NotRequired[AthenaPropertiesPatchTypeDef]
    glueProperties: NotRequired[GluePropertiesPatchTypeDef]
    iamProperties: NotRequired[IamPropertiesPatchTypeDef]
    redshiftProperties: NotRequired[RedshiftPropertiesPatchTypeDef]
    sparkEmrProperties: NotRequired[SparkEmrPropertiesPatchTypeDef]

class PolicyGrantMemberTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    detail: NotRequired[PolicyGrantDetailOutputTypeDef]
    principal: NotRequired[PolicyGrantPrincipalOutputTypeDef]

class PolicyGrantPrincipalTypeDef(TypedDict):
    domainUnit: NotRequired[DomainUnitPolicyGrantPrincipalUnionTypeDef]
    group: NotRequired[GroupPolicyGrantPrincipalTypeDef]
    project: NotRequired[ProjectPolicyGrantPrincipalTypeDef]
    user: NotRequired[UserPolicyGrantPrincipalUnionTypeDef]

EnvironmentConfigurationUnionTypeDef = Union[
    EnvironmentConfigurationTypeDef, EnvironmentConfigurationOutputTypeDef
]

class UpdateProjectProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    description: NotRequired[str]
    domainUnitIdentifier: NotRequired[str]
    environmentConfigurations: NotRequired[Sequence[EnvironmentConfigurationTypeDef]]
    name: NotRequired[str]
    status: NotRequired[StatusType]

class DataSourceConfigurationInputTypeDef(TypedDict):
    glueRunConfiguration: NotRequired[GlueRunConfigurationInputTypeDef]
    redshiftRunConfiguration: NotRequired[RedshiftRunConfigurationInputTypeDef]
    sageMakerRunConfiguration: NotRequired[SageMakerRunConfigurationInputTypeDef]

class PutEnvironmentBlueprintConfigurationInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    enabledRegions: Sequence[str]
    environmentBlueprintIdentifier: str
    environmentRolePermissionBoundary: NotRequired[str]
    manageAccessRoleArn: NotRequired[str]
    provisioningConfigurations: NotRequired[Sequence[ProvisioningConfigurationUnionTypeDef]]
    provisioningRoleArn: NotRequired[str]
    regionalParameters: NotRequired[Mapping[str, Mapping[str, str]]]

class CreateRuleInputRequestTypeDef(TypedDict):
    action: Literal["CREATE_SUBSCRIPTION_REQUEST"]
    detail: RuleDetailTypeDef
    domainIdentifier: str
    name: str
    scope: RuleScopeTypeDef
    target: RuleTargetTypeDef
    clientToken: NotRequired[str]
    description: NotRequired[str]

class UpdateRuleInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    description: NotRequired[str]
    detail: NotRequired[RuleDetailTypeDef]
    includeChildDomainUnits: NotRequired[bool]
    name: NotRequired[str]
    scope: NotRequired[RuleScopeTypeDef]

class ListLineageEventsOutputTypeDef(TypedDict):
    items: List[LineageEventSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

RowFilterTypeDef = TypedDict(
    "RowFilterTypeDef",
    {
        "and": NotRequired[Sequence[Mapping[str, Any]]],
        "expression": NotRequired[RowFilterExpressionUnionTypeDef],
        "or": NotRequired[Sequence[Mapping[str, Any]]],
    },
)

class AssetFilterConfigurationOutputTypeDef(TypedDict):
    columnConfiguration: NotRequired[ColumnFilterConfigurationOutputTypeDef]
    rowConfiguration: NotRequired[RowFilterConfigurationOutputTypeDef]

class PhysicalEndpointTypeDef(TypedDict):
    awsLocation: NotRequired[AwsLocationTypeDef]
    glueConnection: NotRequired[GlueConnectionTypeDef]
    glueConnectionName: NotRequired[str]
    host: NotRequired[str]
    port: NotRequired[int]
    protocol: NotRequired[ProtocolType]
    stage: NotRequired[str]

class GlueConnectionInputTypeDef(TypedDict):
    athenaProperties: NotRequired[Mapping[str, str]]
    authenticationConfiguration: NotRequired[AuthenticationConfigurationInputTypeDef]
    connectionProperties: NotRequired[Mapping[str, str]]
    connectionType: NotRequired[GlueConnectionTypeType]
    description: NotRequired[str]
    matchCriteria: NotRequired[str]
    name: NotRequired[str]
    physicalConnectionRequirements: NotRequired[PhysicalConnectionRequirementsUnionTypeDef]
    pythonProperties: NotRequired[Mapping[str, str]]
    sparkProperties: NotRequired[Mapping[str, str]]
    validateCredentials: NotRequired[bool]
    validateForComputeEnvironments: NotRequired[Sequence[ComputeEnvironmentsType]]

CreateDataSourceOutputTypeDef = TypedDict(
    "CreateDataSourceOutputTypeDef",
    {
        "assetFormsOutput": List[FormOutputTypeDef],
        "configuration": DataSourceConfigurationOutputTypeDef,
        "connectionId": str,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "enableSetting": EnableSettingType,
        "environmentId": str,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "id": str,
        "lastRunAt": datetime,
        "lastRunErrorMessage": DataSourceErrorMessageTypeDef,
        "lastRunStatus": DataSourceRunStatusType,
        "name": str,
        "projectId": str,
        "publishOnImport": bool,
        "recommendation": RecommendationConfigurationTypeDef,
        "schedule": ScheduleConfigurationTypeDef,
        "status": DataSourceStatusType,
        "type": str,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteDataSourceOutputTypeDef = TypedDict(
    "DeleteDataSourceOutputTypeDef",
    {
        "assetFormsOutput": List[FormOutputTypeDef],
        "configuration": DataSourceConfigurationOutputTypeDef,
        "connectionId": str,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "enableSetting": EnableSettingType,
        "environmentId": str,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "id": str,
        "lastRunAt": datetime,
        "lastRunErrorMessage": DataSourceErrorMessageTypeDef,
        "lastRunStatus": DataSourceRunStatusType,
        "name": str,
        "projectId": str,
        "publishOnImport": bool,
        "retainPermissionsOnRevokeFailure": bool,
        "schedule": ScheduleConfigurationTypeDef,
        "selfGrantStatus": SelfGrantStatusOutputTypeDef,
        "status": DataSourceStatusType,
        "type": str,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataSourceOutputTypeDef = TypedDict(
    "GetDataSourceOutputTypeDef",
    {
        "assetFormsOutput": List[FormOutputTypeDef],
        "configuration": DataSourceConfigurationOutputTypeDef,
        "connectionId": str,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "enableSetting": EnableSettingType,
        "environmentId": str,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "id": str,
        "lastRunAssetCount": int,
        "lastRunAt": datetime,
        "lastRunErrorMessage": DataSourceErrorMessageTypeDef,
        "lastRunStatus": DataSourceRunStatusType,
        "name": str,
        "projectId": str,
        "publishOnImport": bool,
        "recommendation": RecommendationConfigurationTypeDef,
        "schedule": ScheduleConfigurationTypeDef,
        "selfGrantStatus": SelfGrantStatusOutputTypeDef,
        "status": DataSourceStatusType,
        "type": str,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateDataSourceOutputTypeDef = TypedDict(
    "UpdateDataSourceOutputTypeDef",
    {
        "assetFormsOutput": List[FormOutputTypeDef],
        "configuration": DataSourceConfigurationOutputTypeDef,
        "connectionId": str,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "enableSetting": EnableSettingType,
        "environmentId": str,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "id": str,
        "lastRunAt": datetime,
        "lastRunErrorMessage": DataSourceErrorMessageTypeDef,
        "lastRunStatus": DataSourceRunStatusType,
        "name": str,
        "projectId": str,
        "publishOnImport": bool,
        "recommendation": RecommendationConfigurationTypeDef,
        "retainPermissionsOnRevokeFailure": bool,
        "schedule": ScheduleConfigurationTypeDef,
        "selfGrantStatus": SelfGrantStatusOutputTypeDef,
        "status": DataSourceStatusType,
        "type": str,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListSubscriptionRequestsOutputTypeDef(TypedDict):
    items: List[SubscriptionRequestSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSubscriptionsOutputTypeDef(TypedDict):
    items: List[SubscriptionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateConnectionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    awsLocation: NotRequired[AwsLocationTypeDef]
    description: NotRequired[str]
    props: NotRequired[ConnectionPropertiesPatchTypeDef]

class ListPolicyGrantsOutputTypeDef(TypedDict):
    grantList: List[PolicyGrantMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AddPolicyGrantInputRequestTypeDef(TypedDict):
    detail: PolicyGrantDetailTypeDef
    domainIdentifier: str
    entityIdentifier: str
    entityType: TargetEntityTypeType
    policyType: ManagedPolicyTypeType
    principal: PolicyGrantPrincipalTypeDef
    clientToken: NotRequired[str]

class RemovePolicyGrantInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TargetEntityTypeType
    policyType: ManagedPolicyTypeType
    principal: PolicyGrantPrincipalTypeDef
    clientToken: NotRequired[str]

class CreateProjectProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    description: NotRequired[str]
    domainUnitIdentifier: NotRequired[str]
    environmentConfigurations: NotRequired[Sequence[EnvironmentConfigurationUnionTypeDef]]
    status: NotRequired[StatusType]

CreateDataSourceInputRequestTypeDef = TypedDict(
    "CreateDataSourceInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "name": str,
        "projectIdentifier": str,
        "type": str,
        "assetFormsInput": NotRequired[Sequence[FormInputTypeDef]],
        "clientToken": NotRequired[str],
        "configuration": NotRequired[DataSourceConfigurationInputTypeDef],
        "connectionIdentifier": NotRequired[str],
        "description": NotRequired[str],
        "enableSetting": NotRequired[EnableSettingType],
        "environmentIdentifier": NotRequired[str],
        "publishOnImport": NotRequired[bool],
        "recommendation": NotRequired[RecommendationConfigurationTypeDef],
        "schedule": NotRequired[ScheduleConfigurationTypeDef],
    },
)

class UpdateDataSourceInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    assetFormsInput: NotRequired[Sequence[FormInputTypeDef]]
    configuration: NotRequired[DataSourceConfigurationInputTypeDef]
    description: NotRequired[str]
    enableSetting: NotRequired[EnableSettingType]
    name: NotRequired[str]
    publishOnImport: NotRequired[bool]
    recommendation: NotRequired[RecommendationConfigurationTypeDef]
    retainPermissionsOnRevokeFailure: NotRequired[bool]
    schedule: NotRequired[ScheduleConfigurationTypeDef]

RowFilterUnionTypeDef = Union[RowFilterTypeDef, RowFilterOutputTypeDef]
CreateAssetFilterOutputTypeDef = TypedDict(
    "CreateAssetFilterOutputTypeDef",
    {
        "assetId": str,
        "configuration": AssetFilterConfigurationOutputTypeDef,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "effectiveColumnNames": List[str],
        "effectiveRowFilter": str,
        "errorMessage": str,
        "id": str,
        "name": str,
        "status": FilterStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAssetFilterOutputTypeDef = TypedDict(
    "GetAssetFilterOutputTypeDef",
    {
        "assetId": str,
        "configuration": AssetFilterConfigurationOutputTypeDef,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "effectiveColumnNames": List[str],
        "effectiveRowFilter": str,
        "errorMessage": str,
        "id": str,
        "name": str,
        "status": FilterStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAssetFilterOutputTypeDef = TypedDict(
    "UpdateAssetFilterOutputTypeDef",
    {
        "assetId": str,
        "configuration": AssetFilterConfigurationOutputTypeDef,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "effectiveColumnNames": List[str],
        "effectiveRowFilter": str,
        "errorMessage": str,
        "id": str,
        "name": str,
        "status": FilterStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ConnectionSummaryTypeDef = TypedDict(
    "ConnectionSummaryTypeDef",
    {
        "connectionId": str,
        "domainId": str,
        "domainUnitId": str,
        "name": str,
        "physicalEndpoints": List[PhysicalEndpointTypeDef],
        "type": ConnectionTypeType,
        "environmentId": NotRequired[str],
        "projectId": NotRequired[str],
        "props": NotRequired[ConnectionPropertiesOutputTypeDef],
    },
)
CreateConnectionOutputTypeDef = TypedDict(
    "CreateConnectionOutputTypeDef",
    {
        "connectionId": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "environmentId": str,
        "name": str,
        "physicalEndpoints": List[PhysicalEndpointTypeDef],
        "projectId": str,
        "props": ConnectionPropertiesOutputTypeDef,
        "type": ConnectionTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetConnectionOutputTypeDef = TypedDict(
    "GetConnectionOutputTypeDef",
    {
        "connectionCredentials": ConnectionCredentialsTypeDef,
        "connectionId": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "environmentId": str,
        "environmentUserRole": str,
        "name": str,
        "physicalEndpoints": List[PhysicalEndpointTypeDef],
        "projectId": str,
        "props": ConnectionPropertiesOutputTypeDef,
        "type": ConnectionTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateConnectionOutputTypeDef = TypedDict(
    "UpdateConnectionOutputTypeDef",
    {
        "connectionId": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "environmentId": str,
        "name": str,
        "physicalEndpoints": List[PhysicalEndpointTypeDef],
        "projectId": str,
        "props": ConnectionPropertiesOutputTypeDef,
        "type": ConnectionTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GluePropertiesInputTypeDef(TypedDict):
    glueConnectionInput: NotRequired[GlueConnectionInputTypeDef]

class RowFilterConfigurationTypeDef(TypedDict):
    rowFilter: RowFilterUnionTypeDef
    sensitive: NotRequired[bool]

class ListConnectionsOutputTypeDef(TypedDict):
    items: List[ConnectionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ConnectionPropertiesInputTypeDef(TypedDict):
    athenaProperties: NotRequired[AthenaPropertiesInputTypeDef]
    glueProperties: NotRequired[GluePropertiesInputTypeDef]
    hyperPodProperties: NotRequired[HyperPodPropertiesInputTypeDef]
    iamProperties: NotRequired[IamPropertiesInputTypeDef]
    redshiftProperties: NotRequired[RedshiftPropertiesInputTypeDef]
    sparkEmrProperties: NotRequired[SparkEmrPropertiesInputTypeDef]
    sparkGlueProperties: NotRequired[SparkGluePropertiesInputTypeDef]

RowFilterConfigurationUnionTypeDef = Union[
    RowFilterConfigurationTypeDef, RowFilterConfigurationOutputTypeDef
]

class CreateConnectionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    name: str
    awsLocation: NotRequired[AwsLocationTypeDef]
    clientToken: NotRequired[str]
    description: NotRequired[str]
    props: NotRequired[ConnectionPropertiesInputTypeDef]

class AssetFilterConfigurationTypeDef(TypedDict):
    columnConfiguration: NotRequired[ColumnFilterConfigurationUnionTypeDef]
    rowConfiguration: NotRequired[RowFilterConfigurationUnionTypeDef]

class CreateAssetFilterInputRequestTypeDef(TypedDict):
    assetIdentifier: str
    configuration: AssetFilterConfigurationTypeDef
    domainIdentifier: str
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]

class UpdateAssetFilterInputRequestTypeDef(TypedDict):
    assetIdentifier: str
    domainIdentifier: str
    identifier: str
    configuration: NotRequired[AssetFilterConfigurationTypeDef]
    description: NotRequired[str]
    name: NotRequired[str]
