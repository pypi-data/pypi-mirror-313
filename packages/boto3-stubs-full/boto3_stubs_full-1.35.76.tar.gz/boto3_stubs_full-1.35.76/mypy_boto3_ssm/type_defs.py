"""
Type annotations for ssm service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/type_defs/)

Usage::

    ```python
    from mypy_boto3_ssm.type_defs import AccountSharingInfoTypeDef

    data: AccountSharingInfoTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AssociationComplianceSeverityType,
    AssociationExecutionFilterKeyType,
    AssociationExecutionTargetsFilterKeyType,
    AssociationFilterKeyType,
    AssociationFilterOperatorTypeType,
    AssociationStatusNameType,
    AssociationSyncComplianceType,
    AttachmentsSourceKeyType,
    AutomationExecutionFilterKeyType,
    AutomationExecutionStatusType,
    AutomationTypeType,
    CalendarStateType,
    CommandFilterKeyType,
    CommandInvocationStatusType,
    CommandPluginStatusType,
    CommandStatusType,
    ComplianceQueryOperatorTypeType,
    ComplianceSeverityType,
    ComplianceStatusType,
    ComplianceUploadTypeType,
    ConnectionStatusType,
    DescribeActivationsFilterKeysType,
    DocumentFilterKeyType,
    DocumentFormatType,
    DocumentHashTypeType,
    DocumentParameterTypeType,
    DocumentReviewActionType,
    DocumentStatusType,
    DocumentTypeType,
    ExecutionModeType,
    ExecutionPreviewStatusType,
    ExternalAlarmStateType,
    FaultType,
    ImpactTypeType,
    InstanceInformationFilterKeyType,
    InstancePatchStateOperatorTypeType,
    InstancePropertyFilterKeyType,
    InstancePropertyFilterOperatorType,
    InventoryAttributeDataTypeType,
    InventoryDeletionStatusType,
    InventoryQueryOperatorTypeType,
    InventorySchemaDeleteOptionType,
    LastResourceDataSyncStatusType,
    MaintenanceWindowExecutionStatusType,
    MaintenanceWindowResourceTypeType,
    MaintenanceWindowTaskCutoffBehaviorType,
    MaintenanceWindowTaskTypeType,
    ManagedStatusType,
    NodeAttributeNameType,
    NodeFilterKeyType,
    NodeFilterOperatorTypeType,
    NotificationEventType,
    NotificationTypeType,
    OperatingSystemType,
    OpsFilterOperatorTypeType,
    OpsItemDataTypeType,
    OpsItemFilterKeyType,
    OpsItemFilterOperatorType,
    OpsItemRelatedItemsFilterKeyType,
    OpsItemStatusType,
    ParametersFilterKeyType,
    ParameterTierType,
    ParameterTypeType,
    PatchActionType,
    PatchComplianceDataStateType,
    PatchComplianceLevelType,
    PatchDeploymentStatusType,
    PatchFilterKeyType,
    PatchOperationTypeType,
    PatchPropertyType,
    PatchSetType,
    PingStatusType,
    PlatformTypeType,
    RebootOptionType,
    ResourceTypeForTaggingType,
    ResourceTypeType,
    ReviewStatusType,
    SessionFilterKeyType,
    SessionStateType,
    SessionStatusType,
    SignalTypeType,
    SourceTypeType,
    StepExecutionFilterKeyType,
    StopTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccountSharingInfoTypeDef",
    "ActivationTypeDef",
    "AddTagsToResourceRequestRequestTypeDef",
    "AlarmConfigurationOutputTypeDef",
    "AlarmConfigurationTypeDef",
    "AlarmConfigurationUnionTypeDef",
    "AlarmStateInformationTypeDef",
    "AlarmTypeDef",
    "AssociateOpsItemRelatedItemRequestRequestTypeDef",
    "AssociateOpsItemRelatedItemResponseTypeDef",
    "AssociationDescriptionTypeDef",
    "AssociationExecutionFilterTypeDef",
    "AssociationExecutionTargetTypeDef",
    "AssociationExecutionTargetsFilterTypeDef",
    "AssociationExecutionTypeDef",
    "AssociationFilterTypeDef",
    "AssociationOverviewTypeDef",
    "AssociationStatusOutputTypeDef",
    "AssociationStatusTypeDef",
    "AssociationTypeDef",
    "AssociationVersionInfoTypeDef",
    "AttachmentContentTypeDef",
    "AttachmentInformationTypeDef",
    "AttachmentsSourceTypeDef",
    "AutomationExecutionFilterTypeDef",
    "AutomationExecutionInputsTypeDef",
    "AutomationExecutionMetadataTypeDef",
    "AutomationExecutionPreviewTypeDef",
    "AutomationExecutionTypeDef",
    "BaselineOverrideTypeDef",
    "BlobTypeDef",
    "CancelCommandRequestRequestTypeDef",
    "CancelMaintenanceWindowExecutionRequestRequestTypeDef",
    "CancelMaintenanceWindowExecutionResultTypeDef",
    "CloudWatchOutputConfigTypeDef",
    "CommandFilterTypeDef",
    "CommandInvocationTypeDef",
    "CommandPluginTypeDef",
    "CommandTypeDef",
    "ComplianceExecutionSummaryOutputTypeDef",
    "ComplianceExecutionSummaryTypeDef",
    "ComplianceItemEntryTypeDef",
    "ComplianceItemTypeDef",
    "ComplianceStringFilterTypeDef",
    "ComplianceSummaryItemTypeDef",
    "CompliantSummaryTypeDef",
    "CreateActivationRequestRequestTypeDef",
    "CreateActivationResultTypeDef",
    "CreateAssociationBatchRequestEntryOutputTypeDef",
    "CreateAssociationBatchRequestEntryTypeDef",
    "CreateAssociationBatchRequestEntryUnionTypeDef",
    "CreateAssociationBatchRequestRequestTypeDef",
    "CreateAssociationBatchResultTypeDef",
    "CreateAssociationRequestRequestTypeDef",
    "CreateAssociationResultTypeDef",
    "CreateDocumentRequestRequestTypeDef",
    "CreateDocumentResultTypeDef",
    "CreateMaintenanceWindowRequestRequestTypeDef",
    "CreateMaintenanceWindowResultTypeDef",
    "CreateOpsItemRequestRequestTypeDef",
    "CreateOpsItemResponseTypeDef",
    "CreateOpsMetadataRequestRequestTypeDef",
    "CreateOpsMetadataResultTypeDef",
    "CreatePatchBaselineRequestRequestTypeDef",
    "CreatePatchBaselineResultTypeDef",
    "CreateResourceDataSyncRequestRequestTypeDef",
    "DeleteActivationRequestRequestTypeDef",
    "DeleteAssociationRequestRequestTypeDef",
    "DeleteDocumentRequestRequestTypeDef",
    "DeleteInventoryRequestRequestTypeDef",
    "DeleteInventoryResultTypeDef",
    "DeleteMaintenanceWindowRequestRequestTypeDef",
    "DeleteMaintenanceWindowResultTypeDef",
    "DeleteOpsItemRequestRequestTypeDef",
    "DeleteOpsMetadataRequestRequestTypeDef",
    "DeleteParameterRequestRequestTypeDef",
    "DeleteParametersRequestRequestTypeDef",
    "DeleteParametersResultTypeDef",
    "DeletePatchBaselineRequestRequestTypeDef",
    "DeletePatchBaselineResultTypeDef",
    "DeleteResourceDataSyncRequestRequestTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeregisterManagedInstanceRequestRequestTypeDef",
    "DeregisterPatchBaselineForPatchGroupRequestRequestTypeDef",
    "DeregisterPatchBaselineForPatchGroupResultTypeDef",
    "DeregisterTargetFromMaintenanceWindowRequestRequestTypeDef",
    "DeregisterTargetFromMaintenanceWindowResultTypeDef",
    "DeregisterTaskFromMaintenanceWindowRequestRequestTypeDef",
    "DeregisterTaskFromMaintenanceWindowResultTypeDef",
    "DescribeActivationsFilterTypeDef",
    "DescribeActivationsRequestDescribeActivationsPaginateTypeDef",
    "DescribeActivationsRequestRequestTypeDef",
    "DescribeActivationsResultTypeDef",
    "DescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef",
    "DescribeAssociationExecutionTargetsRequestRequestTypeDef",
    "DescribeAssociationExecutionTargetsResultTypeDef",
    "DescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef",
    "DescribeAssociationExecutionsRequestRequestTypeDef",
    "DescribeAssociationExecutionsResultTypeDef",
    "DescribeAssociationRequestRequestTypeDef",
    "DescribeAssociationResultTypeDef",
    "DescribeAutomationExecutionsRequestDescribeAutomationExecutionsPaginateTypeDef",
    "DescribeAutomationExecutionsRequestRequestTypeDef",
    "DescribeAutomationExecutionsResultTypeDef",
    "DescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef",
    "DescribeAutomationStepExecutionsRequestRequestTypeDef",
    "DescribeAutomationStepExecutionsResultTypeDef",
    "DescribeAvailablePatchesRequestDescribeAvailablePatchesPaginateTypeDef",
    "DescribeAvailablePatchesRequestRequestTypeDef",
    "DescribeAvailablePatchesResultTypeDef",
    "DescribeDocumentPermissionRequestRequestTypeDef",
    "DescribeDocumentPermissionResponseTypeDef",
    "DescribeDocumentRequestRequestTypeDef",
    "DescribeDocumentResultTypeDef",
    "DescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef",
    "DescribeEffectiveInstanceAssociationsRequestRequestTypeDef",
    "DescribeEffectiveInstanceAssociationsResultTypeDef",
    "DescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef",
    "DescribeEffectivePatchesForPatchBaselineRequestRequestTypeDef",
    "DescribeEffectivePatchesForPatchBaselineResultTypeDef",
    "DescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef",
    "DescribeInstanceAssociationsStatusRequestRequestTypeDef",
    "DescribeInstanceAssociationsStatusResultTypeDef",
    "DescribeInstanceInformationRequestDescribeInstanceInformationPaginateTypeDef",
    "DescribeInstanceInformationRequestRequestTypeDef",
    "DescribeInstanceInformationResultTypeDef",
    "DescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef",
    "DescribeInstancePatchStatesForPatchGroupRequestRequestTypeDef",
    "DescribeInstancePatchStatesForPatchGroupResultTypeDef",
    "DescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef",
    "DescribeInstancePatchStatesRequestRequestTypeDef",
    "DescribeInstancePatchStatesResultTypeDef",
    "DescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef",
    "DescribeInstancePatchesRequestRequestTypeDef",
    "DescribeInstancePatchesResultTypeDef",
    "DescribeInstancePropertiesRequestDescribeInstancePropertiesPaginateTypeDef",
    "DescribeInstancePropertiesRequestRequestTypeDef",
    "DescribeInstancePropertiesResultTypeDef",
    "DescribeInventoryDeletionsRequestDescribeInventoryDeletionsPaginateTypeDef",
    "DescribeInventoryDeletionsRequestRequestTypeDef",
    "DescribeInventoryDeletionsResultTypeDef",
    "DescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef",
    "DescribeMaintenanceWindowExecutionTaskInvocationsRequestRequestTypeDef",
    "DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef",
    "DescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef",
    "DescribeMaintenanceWindowExecutionTasksRequestRequestTypeDef",
    "DescribeMaintenanceWindowExecutionTasksResultTypeDef",
    "DescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef",
    "DescribeMaintenanceWindowExecutionsRequestRequestTypeDef",
    "DescribeMaintenanceWindowExecutionsResultTypeDef",
    "DescribeMaintenanceWindowScheduleRequestDescribeMaintenanceWindowSchedulePaginateTypeDef",
    "DescribeMaintenanceWindowScheduleRequestRequestTypeDef",
    "DescribeMaintenanceWindowScheduleResultTypeDef",
    "DescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef",
    "DescribeMaintenanceWindowTargetsRequestRequestTypeDef",
    "DescribeMaintenanceWindowTargetsResultTypeDef",
    "DescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef",
    "DescribeMaintenanceWindowTasksRequestRequestTypeDef",
    "DescribeMaintenanceWindowTasksResultTypeDef",
    "DescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef",
    "DescribeMaintenanceWindowsForTargetRequestRequestTypeDef",
    "DescribeMaintenanceWindowsForTargetResultTypeDef",
    "DescribeMaintenanceWindowsRequestDescribeMaintenanceWindowsPaginateTypeDef",
    "DescribeMaintenanceWindowsRequestRequestTypeDef",
    "DescribeMaintenanceWindowsResultTypeDef",
    "DescribeOpsItemsRequestDescribeOpsItemsPaginateTypeDef",
    "DescribeOpsItemsRequestRequestTypeDef",
    "DescribeOpsItemsResponseTypeDef",
    "DescribeParametersRequestDescribeParametersPaginateTypeDef",
    "DescribeParametersRequestRequestTypeDef",
    "DescribeParametersResultTypeDef",
    "DescribePatchBaselinesRequestDescribePatchBaselinesPaginateTypeDef",
    "DescribePatchBaselinesRequestRequestTypeDef",
    "DescribePatchBaselinesResultTypeDef",
    "DescribePatchGroupStateRequestRequestTypeDef",
    "DescribePatchGroupStateResultTypeDef",
    "DescribePatchGroupsRequestDescribePatchGroupsPaginateTypeDef",
    "DescribePatchGroupsRequestRequestTypeDef",
    "DescribePatchGroupsResultTypeDef",
    "DescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef",
    "DescribePatchPropertiesRequestRequestTypeDef",
    "DescribePatchPropertiesResultTypeDef",
    "DescribeSessionsRequestDescribeSessionsPaginateTypeDef",
    "DescribeSessionsRequestRequestTypeDef",
    "DescribeSessionsResponseTypeDef",
    "DisassociateOpsItemRelatedItemRequestRequestTypeDef",
    "DocumentDefaultVersionDescriptionTypeDef",
    "DocumentDescriptionTypeDef",
    "DocumentFilterTypeDef",
    "DocumentIdentifierTypeDef",
    "DocumentKeyValuesFilterTypeDef",
    "DocumentMetadataResponseInfoTypeDef",
    "DocumentParameterTypeDef",
    "DocumentRequiresTypeDef",
    "DocumentReviewCommentSourceTypeDef",
    "DocumentReviewerResponseSourceTypeDef",
    "DocumentReviewsTypeDef",
    "DocumentVersionInfoTypeDef",
    "EffectivePatchTypeDef",
    "ExecutionInputsTypeDef",
    "ExecutionPreviewTypeDef",
    "FailedCreateAssociationTypeDef",
    "FailureDetailsTypeDef",
    "GetAutomationExecutionRequestRequestTypeDef",
    "GetAutomationExecutionResultTypeDef",
    "GetCalendarStateRequestRequestTypeDef",
    "GetCalendarStateResponseTypeDef",
    "GetCommandInvocationRequestCommandExecutedWaitTypeDef",
    "GetCommandInvocationRequestRequestTypeDef",
    "GetCommandInvocationResultTypeDef",
    "GetConnectionStatusRequestRequestTypeDef",
    "GetConnectionStatusResponseTypeDef",
    "GetDefaultPatchBaselineRequestRequestTypeDef",
    "GetDefaultPatchBaselineResultTypeDef",
    "GetDeployablePatchSnapshotForInstanceRequestRequestTypeDef",
    "GetDeployablePatchSnapshotForInstanceResultTypeDef",
    "GetDocumentRequestRequestTypeDef",
    "GetDocumentResultTypeDef",
    "GetExecutionPreviewRequestRequestTypeDef",
    "GetExecutionPreviewResponseTypeDef",
    "GetInventoryRequestGetInventoryPaginateTypeDef",
    "GetInventoryRequestRequestTypeDef",
    "GetInventoryResultTypeDef",
    "GetInventorySchemaRequestGetInventorySchemaPaginateTypeDef",
    "GetInventorySchemaRequestRequestTypeDef",
    "GetInventorySchemaResultTypeDef",
    "GetMaintenanceWindowExecutionRequestRequestTypeDef",
    "GetMaintenanceWindowExecutionResultTypeDef",
    "GetMaintenanceWindowExecutionTaskInvocationRequestRequestTypeDef",
    "GetMaintenanceWindowExecutionTaskInvocationResultTypeDef",
    "GetMaintenanceWindowExecutionTaskRequestRequestTypeDef",
    "GetMaintenanceWindowExecutionTaskResultTypeDef",
    "GetMaintenanceWindowRequestRequestTypeDef",
    "GetMaintenanceWindowResultTypeDef",
    "GetMaintenanceWindowTaskRequestRequestTypeDef",
    "GetMaintenanceWindowTaskResultTypeDef",
    "GetOpsItemRequestRequestTypeDef",
    "GetOpsItemResponseTypeDef",
    "GetOpsMetadataRequestRequestTypeDef",
    "GetOpsMetadataResultTypeDef",
    "GetOpsSummaryRequestGetOpsSummaryPaginateTypeDef",
    "GetOpsSummaryRequestRequestTypeDef",
    "GetOpsSummaryResultTypeDef",
    "GetParameterHistoryRequestGetParameterHistoryPaginateTypeDef",
    "GetParameterHistoryRequestRequestTypeDef",
    "GetParameterHistoryResultTypeDef",
    "GetParameterRequestRequestTypeDef",
    "GetParameterResultTypeDef",
    "GetParametersByPathRequestGetParametersByPathPaginateTypeDef",
    "GetParametersByPathRequestRequestTypeDef",
    "GetParametersByPathResultTypeDef",
    "GetParametersRequestRequestTypeDef",
    "GetParametersResultTypeDef",
    "GetPatchBaselineForPatchGroupRequestRequestTypeDef",
    "GetPatchBaselineForPatchGroupResultTypeDef",
    "GetPatchBaselineRequestRequestTypeDef",
    "GetPatchBaselineResultTypeDef",
    "GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef",
    "GetResourcePoliciesRequestRequestTypeDef",
    "GetResourcePoliciesResponseEntryTypeDef",
    "GetResourcePoliciesResponseTypeDef",
    "GetServiceSettingRequestRequestTypeDef",
    "GetServiceSettingResultTypeDef",
    "InstanceAggregatedAssociationOverviewTypeDef",
    "InstanceAssociationOutputLocationTypeDef",
    "InstanceAssociationOutputUrlTypeDef",
    "InstanceAssociationStatusInfoTypeDef",
    "InstanceAssociationTypeDef",
    "InstanceInfoTypeDef",
    "InstanceInformationFilterTypeDef",
    "InstanceInformationStringFilterTypeDef",
    "InstanceInformationTypeDef",
    "InstancePatchStateFilterTypeDef",
    "InstancePatchStateTypeDef",
    "InstancePropertyFilterTypeDef",
    "InstancePropertyStringFilterTypeDef",
    "InstancePropertyTypeDef",
    "InventoryAggregatorPaginatorTypeDef",
    "InventoryAggregatorTypeDef",
    "InventoryDeletionStatusItemTypeDef",
    "InventoryDeletionSummaryItemTypeDef",
    "InventoryDeletionSummaryTypeDef",
    "InventoryFilterTypeDef",
    "InventoryGroupTypeDef",
    "InventoryItemAttributeTypeDef",
    "InventoryItemSchemaTypeDef",
    "InventoryItemTypeDef",
    "InventoryResultEntityTypeDef",
    "InventoryResultItemTypeDef",
    "LabelParameterVersionRequestRequestTypeDef",
    "LabelParameterVersionResultTypeDef",
    "ListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef",
    "ListAssociationVersionsRequestRequestTypeDef",
    "ListAssociationVersionsResultTypeDef",
    "ListAssociationsRequestListAssociationsPaginateTypeDef",
    "ListAssociationsRequestRequestTypeDef",
    "ListAssociationsResultTypeDef",
    "ListCommandInvocationsRequestListCommandInvocationsPaginateTypeDef",
    "ListCommandInvocationsRequestRequestTypeDef",
    "ListCommandInvocationsResultTypeDef",
    "ListCommandsRequestListCommandsPaginateTypeDef",
    "ListCommandsRequestRequestTypeDef",
    "ListCommandsResultTypeDef",
    "ListComplianceItemsRequestListComplianceItemsPaginateTypeDef",
    "ListComplianceItemsRequestRequestTypeDef",
    "ListComplianceItemsResultTypeDef",
    "ListComplianceSummariesRequestListComplianceSummariesPaginateTypeDef",
    "ListComplianceSummariesRequestRequestTypeDef",
    "ListComplianceSummariesResultTypeDef",
    "ListDocumentMetadataHistoryRequestRequestTypeDef",
    "ListDocumentMetadataHistoryResponseTypeDef",
    "ListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef",
    "ListDocumentVersionsRequestRequestTypeDef",
    "ListDocumentVersionsResultTypeDef",
    "ListDocumentsRequestListDocumentsPaginateTypeDef",
    "ListDocumentsRequestRequestTypeDef",
    "ListDocumentsResultTypeDef",
    "ListInventoryEntriesRequestRequestTypeDef",
    "ListInventoryEntriesResultTypeDef",
    "ListNodesRequestListNodesPaginateTypeDef",
    "ListNodesRequestRequestTypeDef",
    "ListNodesResultTypeDef",
    "ListNodesSummaryRequestListNodesSummaryPaginateTypeDef",
    "ListNodesSummaryRequestRequestTypeDef",
    "ListNodesSummaryResultTypeDef",
    "ListOpsItemEventsRequestListOpsItemEventsPaginateTypeDef",
    "ListOpsItemEventsRequestRequestTypeDef",
    "ListOpsItemEventsResponseTypeDef",
    "ListOpsItemRelatedItemsRequestListOpsItemRelatedItemsPaginateTypeDef",
    "ListOpsItemRelatedItemsRequestRequestTypeDef",
    "ListOpsItemRelatedItemsResponseTypeDef",
    "ListOpsMetadataRequestListOpsMetadataPaginateTypeDef",
    "ListOpsMetadataRequestRequestTypeDef",
    "ListOpsMetadataResultTypeDef",
    "ListResourceComplianceSummariesRequestListResourceComplianceSummariesPaginateTypeDef",
    "ListResourceComplianceSummariesRequestRequestTypeDef",
    "ListResourceComplianceSummariesResultTypeDef",
    "ListResourceDataSyncRequestListResourceDataSyncPaginateTypeDef",
    "ListResourceDataSyncRequestRequestTypeDef",
    "ListResourceDataSyncResultTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResultTypeDef",
    "LoggingInfoTypeDef",
    "MaintenanceWindowAutomationParametersOutputTypeDef",
    "MaintenanceWindowAutomationParametersTypeDef",
    "MaintenanceWindowAutomationParametersUnionTypeDef",
    "MaintenanceWindowExecutionTaskIdentityTypeDef",
    "MaintenanceWindowExecutionTaskInvocationIdentityTypeDef",
    "MaintenanceWindowExecutionTypeDef",
    "MaintenanceWindowFilterTypeDef",
    "MaintenanceWindowIdentityForTargetTypeDef",
    "MaintenanceWindowIdentityTypeDef",
    "MaintenanceWindowLambdaParametersOutputTypeDef",
    "MaintenanceWindowLambdaParametersTypeDef",
    "MaintenanceWindowLambdaParametersUnionTypeDef",
    "MaintenanceWindowRunCommandParametersOutputTypeDef",
    "MaintenanceWindowRunCommandParametersTypeDef",
    "MaintenanceWindowRunCommandParametersUnionTypeDef",
    "MaintenanceWindowStepFunctionsParametersTypeDef",
    "MaintenanceWindowTargetTypeDef",
    "MaintenanceWindowTaskInvocationParametersOutputTypeDef",
    "MaintenanceWindowTaskInvocationParametersTypeDef",
    "MaintenanceWindowTaskParameterValueExpressionOutputTypeDef",
    "MaintenanceWindowTaskParameterValueExpressionTypeDef",
    "MaintenanceWindowTaskParameterValueExpressionUnionTypeDef",
    "MaintenanceWindowTaskTypeDef",
    "MetadataValueTypeDef",
    "ModifyDocumentPermissionRequestRequestTypeDef",
    "NodeAggregatorPaginatorTypeDef",
    "NodeAggregatorTypeDef",
    "NodeFilterTypeDef",
    "NodeOwnerInfoTypeDef",
    "NodeTypeDef",
    "NodeTypeTypeDef",
    "NonCompliantSummaryTypeDef",
    "NotificationConfigOutputTypeDef",
    "NotificationConfigTypeDef",
    "NotificationConfigUnionTypeDef",
    "OpsAggregatorPaginatorTypeDef",
    "OpsAggregatorTypeDef",
    "OpsEntityItemTypeDef",
    "OpsEntityTypeDef",
    "OpsFilterTypeDef",
    "OpsItemDataValueTypeDef",
    "OpsItemEventFilterTypeDef",
    "OpsItemEventSummaryTypeDef",
    "OpsItemFilterTypeDef",
    "OpsItemIdentityTypeDef",
    "OpsItemNotificationTypeDef",
    "OpsItemRelatedItemSummaryTypeDef",
    "OpsItemRelatedItemsFilterTypeDef",
    "OpsItemSummaryTypeDef",
    "OpsItemTypeDef",
    "OpsMetadataFilterTypeDef",
    "OpsMetadataTypeDef",
    "OpsResultAttributeTypeDef",
    "OutputSourceTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterHistoryTypeDef",
    "ParameterInlinePolicyTypeDef",
    "ParameterMetadataTypeDef",
    "ParameterStringFilterTypeDef",
    "ParameterTypeDef",
    "ParametersFilterTypeDef",
    "ParentStepDetailsTypeDef",
    "PatchBaselineIdentityTypeDef",
    "PatchComplianceDataTypeDef",
    "PatchFilterGroupOutputTypeDef",
    "PatchFilterGroupTypeDef",
    "PatchFilterGroupUnionTypeDef",
    "PatchFilterOutputTypeDef",
    "PatchFilterTypeDef",
    "PatchFilterUnionTypeDef",
    "PatchGroupPatchBaselineMappingTypeDef",
    "PatchOrchestratorFilterTypeDef",
    "PatchRuleGroupOutputTypeDef",
    "PatchRuleGroupTypeDef",
    "PatchRuleGroupUnionTypeDef",
    "PatchRuleOutputTypeDef",
    "PatchRuleTypeDef",
    "PatchRuleUnionTypeDef",
    "PatchSourceOutputTypeDef",
    "PatchSourceTypeDef",
    "PatchSourceUnionTypeDef",
    "PatchStatusTypeDef",
    "PatchTypeDef",
    "ProgressCountersTypeDef",
    "PutComplianceItemsRequestRequestTypeDef",
    "PutInventoryRequestRequestTypeDef",
    "PutInventoryResultTypeDef",
    "PutParameterRequestRequestTypeDef",
    "PutParameterResultTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "RegisterDefaultPatchBaselineRequestRequestTypeDef",
    "RegisterDefaultPatchBaselineResultTypeDef",
    "RegisterPatchBaselineForPatchGroupRequestRequestTypeDef",
    "RegisterPatchBaselineForPatchGroupResultTypeDef",
    "RegisterTargetWithMaintenanceWindowRequestRequestTypeDef",
    "RegisterTargetWithMaintenanceWindowResultTypeDef",
    "RegisterTaskWithMaintenanceWindowRequestRequestTypeDef",
    "RegisterTaskWithMaintenanceWindowResultTypeDef",
    "RegistrationMetadataItemTypeDef",
    "RelatedOpsItemTypeDef",
    "RemoveTagsFromResourceRequestRequestTypeDef",
    "ResetServiceSettingRequestRequestTypeDef",
    "ResetServiceSettingResultTypeDef",
    "ResolvedTargetsTypeDef",
    "ResourceComplianceSummaryItemTypeDef",
    "ResourceDataSyncAwsOrganizationsSourceOutputTypeDef",
    "ResourceDataSyncAwsOrganizationsSourceTypeDef",
    "ResourceDataSyncAwsOrganizationsSourceUnionTypeDef",
    "ResourceDataSyncDestinationDataSharingTypeDef",
    "ResourceDataSyncItemTypeDef",
    "ResourceDataSyncOrganizationalUnitTypeDef",
    "ResourceDataSyncS3DestinationTypeDef",
    "ResourceDataSyncSourceTypeDef",
    "ResourceDataSyncSourceWithStateTypeDef",
    "ResponseMetadataTypeDef",
    "ResultAttributeTypeDef",
    "ResumeSessionRequestRequestTypeDef",
    "ResumeSessionResponseTypeDef",
    "ReviewInformationTypeDef",
    "RunbookOutputTypeDef",
    "RunbookTypeDef",
    "RunbookUnionTypeDef",
    "S3OutputLocationTypeDef",
    "S3OutputUrlTypeDef",
    "ScheduledWindowExecutionTypeDef",
    "SendAutomationSignalRequestRequestTypeDef",
    "SendCommandRequestRequestTypeDef",
    "SendCommandResultTypeDef",
    "ServiceSettingTypeDef",
    "SessionFilterTypeDef",
    "SessionManagerOutputUrlTypeDef",
    "SessionTypeDef",
    "SeveritySummaryTypeDef",
    "StartAssociationsOnceRequestRequestTypeDef",
    "StartAutomationExecutionRequestRequestTypeDef",
    "StartAutomationExecutionResultTypeDef",
    "StartChangeRequestExecutionRequestRequestTypeDef",
    "StartChangeRequestExecutionResultTypeDef",
    "StartExecutionPreviewRequestRequestTypeDef",
    "StartExecutionPreviewResponseTypeDef",
    "StartSessionRequestRequestTypeDef",
    "StartSessionResponseTypeDef",
    "StepExecutionFilterTypeDef",
    "StepExecutionTypeDef",
    "StopAutomationExecutionRequestRequestTypeDef",
    "TagTypeDef",
    "TargetLocationOutputTypeDef",
    "TargetLocationTypeDef",
    "TargetLocationUnionTypeDef",
    "TargetOutputTypeDef",
    "TargetPreviewTypeDef",
    "TargetTypeDef",
    "TargetUnionTypeDef",
    "TerminateSessionRequestRequestTypeDef",
    "TerminateSessionResponseTypeDef",
    "TimestampTypeDef",
    "UnlabelParameterVersionRequestRequestTypeDef",
    "UnlabelParameterVersionResultTypeDef",
    "UpdateAssociationRequestRequestTypeDef",
    "UpdateAssociationResultTypeDef",
    "UpdateAssociationStatusRequestRequestTypeDef",
    "UpdateAssociationStatusResultTypeDef",
    "UpdateDocumentDefaultVersionRequestRequestTypeDef",
    "UpdateDocumentDefaultVersionResultTypeDef",
    "UpdateDocumentMetadataRequestRequestTypeDef",
    "UpdateDocumentRequestRequestTypeDef",
    "UpdateDocumentResultTypeDef",
    "UpdateMaintenanceWindowRequestRequestTypeDef",
    "UpdateMaintenanceWindowResultTypeDef",
    "UpdateMaintenanceWindowTargetRequestRequestTypeDef",
    "UpdateMaintenanceWindowTargetResultTypeDef",
    "UpdateMaintenanceWindowTaskRequestRequestTypeDef",
    "UpdateMaintenanceWindowTaskResultTypeDef",
    "UpdateManagedInstanceRoleRequestRequestTypeDef",
    "UpdateOpsItemRequestRequestTypeDef",
    "UpdateOpsMetadataRequestRequestTypeDef",
    "UpdateOpsMetadataResultTypeDef",
    "UpdatePatchBaselineRequestRequestTypeDef",
    "UpdatePatchBaselineResultTypeDef",
    "UpdateResourceDataSyncRequestRequestTypeDef",
    "UpdateServiceSettingRequestRequestTypeDef",
    "WaiterConfigTypeDef",
)


class AccountSharingInfoTypeDef(TypedDict):
    AccountId: NotRequired[str]
    SharedDocumentVersion: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class AlarmTypeDef(TypedDict):
    Name: str


class AlarmStateInformationTypeDef(TypedDict):
    Name: str
    State: ExternalAlarmStateType


class AssociateOpsItemRelatedItemRequestRequestTypeDef(TypedDict):
    OpsItemId: str
    AssociationType: str
    ResourceType: str
    ResourceUri: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AssociationOverviewTypeDef(TypedDict):
    Status: NotRequired[str]
    DetailedStatus: NotRequired[str]
    AssociationStatusAggregatedCount: NotRequired[Dict[str, int]]


class AssociationStatusOutputTypeDef(TypedDict):
    Date: datetime
    Name: AssociationStatusNameType
    Message: str
    AdditionalInfo: NotRequired[str]


class TargetOutputTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[List[str]]


AssociationExecutionFilterTypeDef = TypedDict(
    "AssociationExecutionFilterTypeDef",
    {
        "Key": AssociationExecutionFilterKeyType,
        "Value": str,
        "Type": AssociationFilterOperatorTypeType,
    },
)


class OutputSourceTypeDef(TypedDict):
    OutputSourceId: NotRequired[str]
    OutputSourceType: NotRequired[str]


class AssociationExecutionTargetsFilterTypeDef(TypedDict):
    Key: AssociationExecutionTargetsFilterKeyType
    Value: str


class AssociationFilterTypeDef(TypedDict):
    key: AssociationFilterKeyType
    value: str


TimestampTypeDef = Union[datetime, str]


class AttachmentContentTypeDef(TypedDict):
    Name: NotRequired[str]
    Size: NotRequired[int]
    Hash: NotRequired[str]
    HashType: NotRequired[Literal["Sha256"]]
    Url: NotRequired[str]


class AttachmentInformationTypeDef(TypedDict):
    Name: NotRequired[str]


class AttachmentsSourceTypeDef(TypedDict):
    Key: NotRequired[AttachmentsSourceKeyType]
    Values: NotRequired[Sequence[str]]
    Name: NotRequired[str]


class AutomationExecutionFilterTypeDef(TypedDict):
    Key: AutomationExecutionFilterKeyType
    Values: Sequence[str]


class ResolvedTargetsTypeDef(TypedDict):
    ParameterValues: NotRequired[List[str]]
    Truncated: NotRequired[bool]


class TargetPreviewTypeDef(TypedDict):
    Count: NotRequired[int]
    TargetType: NotRequired[str]


class ProgressCountersTypeDef(TypedDict):
    TotalSteps: NotRequired[int]
    SuccessSteps: NotRequired[int]
    FailedSteps: NotRequired[int]
    CancelledSteps: NotRequired[int]
    TimedOutSteps: NotRequired[int]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class CancelCommandRequestRequestTypeDef(TypedDict):
    CommandId: str
    InstanceIds: NotRequired[Sequence[str]]


class CancelMaintenanceWindowExecutionRequestRequestTypeDef(TypedDict):
    WindowExecutionId: str


class CloudWatchOutputConfigTypeDef(TypedDict):
    CloudWatchLogGroupName: NotRequired[str]
    CloudWatchOutputEnabled: NotRequired[bool]


class CommandFilterTypeDef(TypedDict):
    key: CommandFilterKeyType
    value: str


class CommandPluginTypeDef(TypedDict):
    Name: NotRequired[str]
    Status: NotRequired[CommandPluginStatusType]
    StatusDetails: NotRequired[str]
    ResponseCode: NotRequired[int]
    ResponseStartDateTime: NotRequired[datetime]
    ResponseFinishDateTime: NotRequired[datetime]
    Output: NotRequired[str]
    StandardOutputUrl: NotRequired[str]
    StandardErrorUrl: NotRequired[str]
    OutputS3Region: NotRequired[str]
    OutputS3BucketName: NotRequired[str]
    OutputS3KeyPrefix: NotRequired[str]


class NotificationConfigOutputTypeDef(TypedDict):
    NotificationArn: NotRequired[str]
    NotificationEvents: NotRequired[List[NotificationEventType]]
    NotificationType: NotRequired[NotificationTypeType]


class ComplianceExecutionSummaryOutputTypeDef(TypedDict):
    ExecutionTime: datetime
    ExecutionId: NotRequired[str]
    ExecutionType: NotRequired[str]


class ComplianceItemEntryTypeDef(TypedDict):
    Severity: ComplianceSeverityType
    Status: ComplianceStatusType
    Id: NotRequired[str]
    Title: NotRequired[str]
    Details: NotRequired[Mapping[str, str]]


ComplianceStringFilterTypeDef = TypedDict(
    "ComplianceStringFilterTypeDef",
    {
        "Key": NotRequired[str],
        "Values": NotRequired[Sequence[str]],
        "Type": NotRequired[ComplianceQueryOperatorTypeType],
    },
)


class SeveritySummaryTypeDef(TypedDict):
    CriticalCount: NotRequired[int]
    HighCount: NotRequired[int]
    MediumCount: NotRequired[int]
    LowCount: NotRequired[int]
    InformationalCount: NotRequired[int]
    UnspecifiedCount: NotRequired[int]


class RegistrationMetadataItemTypeDef(TypedDict):
    Key: str
    Value: str


class DocumentRequiresTypeDef(TypedDict):
    Name: str
    Version: NotRequired[str]
    RequireType: NotRequired[str]
    VersionName: NotRequired[str]


OpsItemDataValueTypeDef = TypedDict(
    "OpsItemDataValueTypeDef",
    {
        "Value": NotRequired[str],
        "Type": NotRequired[OpsItemDataTypeType],
    },
)


class OpsItemNotificationTypeDef(TypedDict):
    Arn: NotRequired[str]


class RelatedOpsItemTypeDef(TypedDict):
    OpsItemId: str


class MetadataValueTypeDef(TypedDict):
    Value: NotRequired[str]


class DeleteActivationRequestRequestTypeDef(TypedDict):
    ActivationId: str


class DeleteAssociationRequestRequestTypeDef(TypedDict):
    Name: NotRequired[str]
    InstanceId: NotRequired[str]
    AssociationId: NotRequired[str]


class DeleteDocumentRequestRequestTypeDef(TypedDict):
    Name: str
    DocumentVersion: NotRequired[str]
    VersionName: NotRequired[str]
    Force: NotRequired[bool]


class DeleteInventoryRequestRequestTypeDef(TypedDict):
    TypeName: str
    SchemaDeleteOption: NotRequired[InventorySchemaDeleteOptionType]
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]


class DeleteMaintenanceWindowRequestRequestTypeDef(TypedDict):
    WindowId: str


class DeleteOpsItemRequestRequestTypeDef(TypedDict):
    OpsItemId: str


class DeleteOpsMetadataRequestRequestTypeDef(TypedDict):
    OpsMetadataArn: str


class DeleteParameterRequestRequestTypeDef(TypedDict):
    Name: str


class DeleteParametersRequestRequestTypeDef(TypedDict):
    Names: Sequence[str]


class DeletePatchBaselineRequestRequestTypeDef(TypedDict):
    BaselineId: str


class DeleteResourceDataSyncRequestRequestTypeDef(TypedDict):
    SyncName: str
    SyncType: NotRequired[str]


class DeleteResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    PolicyId: str
    PolicyHash: str


class DeregisterManagedInstanceRequestRequestTypeDef(TypedDict):
    InstanceId: str


class DeregisterPatchBaselineForPatchGroupRequestRequestTypeDef(TypedDict):
    BaselineId: str
    PatchGroup: str


class DeregisterTargetFromMaintenanceWindowRequestRequestTypeDef(TypedDict):
    WindowId: str
    WindowTargetId: str
    Safe: NotRequired[bool]


class DeregisterTaskFromMaintenanceWindowRequestRequestTypeDef(TypedDict):
    WindowId: str
    WindowTaskId: str


class DescribeActivationsFilterTypeDef(TypedDict):
    FilterKey: NotRequired[DescribeActivationsFilterKeysType]
    FilterValues: NotRequired[Sequence[str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeAssociationRequestRequestTypeDef(TypedDict):
    Name: NotRequired[str]
    InstanceId: NotRequired[str]
    AssociationId: NotRequired[str]
    AssociationVersion: NotRequired[str]


class StepExecutionFilterTypeDef(TypedDict):
    Key: StepExecutionFilterKeyType
    Values: Sequence[str]


class PatchOrchestratorFilterTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[Sequence[str]]


class PatchTypeDef(TypedDict):
    Id: NotRequired[str]
    ReleaseDate: NotRequired[datetime]
    Title: NotRequired[str]
    Description: NotRequired[str]
    ContentUrl: NotRequired[str]
    Vendor: NotRequired[str]
    ProductFamily: NotRequired[str]
    Product: NotRequired[str]
    Classification: NotRequired[str]
    MsrcSeverity: NotRequired[str]
    KbNumber: NotRequired[str]
    MsrcNumber: NotRequired[str]
    Language: NotRequired[str]
    AdvisoryIds: NotRequired[List[str]]
    BugzillaIds: NotRequired[List[str]]
    CVEIds: NotRequired[List[str]]
    Name: NotRequired[str]
    Epoch: NotRequired[int]
    Version: NotRequired[str]
    Release: NotRequired[str]
    Arch: NotRequired[str]
    Severity: NotRequired[str]
    Repository: NotRequired[str]


class DescribeDocumentPermissionRequestRequestTypeDef(TypedDict):
    Name: str
    PermissionType: Literal["Share"]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeDocumentRequestRequestTypeDef(TypedDict):
    Name: str
    DocumentVersion: NotRequired[str]
    VersionName: NotRequired[str]


class DescribeEffectiveInstanceAssociationsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class InstanceAssociationTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    InstanceId: NotRequired[str]
    Content: NotRequired[str]
    AssociationVersion: NotRequired[str]


class DescribeEffectivePatchesForPatchBaselineRequestRequestTypeDef(TypedDict):
    BaselineId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeInstanceAssociationsStatusRequestRequestTypeDef(TypedDict):
    InstanceId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class InstanceInformationFilterTypeDef(TypedDict):
    key: InstanceInformationFilterKeyType
    valueSet: Sequence[str]


class InstanceInformationStringFilterTypeDef(TypedDict):
    Key: str
    Values: Sequence[str]


InstancePatchStateFilterTypeDef = TypedDict(
    "InstancePatchStateFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
        "Type": InstancePatchStateOperatorTypeType,
    },
)


class InstancePatchStateTypeDef(TypedDict):
    InstanceId: str
    PatchGroup: str
    BaselineId: str
    OperationStartTime: datetime
    OperationEndTime: datetime
    Operation: PatchOperationTypeType
    SnapshotId: NotRequired[str]
    InstallOverrideList: NotRequired[str]
    OwnerInformation: NotRequired[str]
    InstalledCount: NotRequired[int]
    InstalledOtherCount: NotRequired[int]
    InstalledPendingRebootCount: NotRequired[int]
    InstalledRejectedCount: NotRequired[int]
    MissingCount: NotRequired[int]
    FailedCount: NotRequired[int]
    UnreportedNotApplicableCount: NotRequired[int]
    NotApplicableCount: NotRequired[int]
    LastNoRebootInstallOperationTime: NotRequired[datetime]
    RebootOption: NotRequired[RebootOptionType]
    CriticalNonCompliantCount: NotRequired[int]
    SecurityNonCompliantCount: NotRequired[int]
    OtherNonCompliantCount: NotRequired[int]


class DescribeInstancePatchStatesRequestRequestTypeDef(TypedDict):
    InstanceIds: Sequence[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class PatchComplianceDataTypeDef(TypedDict):
    Title: str
    KBId: str
    Classification: str
    Severity: str
    State: PatchComplianceDataStateType
    InstalledTime: datetime
    CVEIds: NotRequired[str]


class InstancePropertyFilterTypeDef(TypedDict):
    key: InstancePropertyFilterKeyType
    valueSet: Sequence[str]


class InstancePropertyStringFilterTypeDef(TypedDict):
    Key: str
    Values: Sequence[str]
    Operator: NotRequired[InstancePropertyFilterOperatorType]


class DescribeInventoryDeletionsRequestRequestTypeDef(TypedDict):
    DeletionId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class MaintenanceWindowFilterTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[Sequence[str]]


class MaintenanceWindowExecutionTaskInvocationIdentityTypeDef(TypedDict):
    WindowExecutionId: NotRequired[str]
    TaskExecutionId: NotRequired[str]
    InvocationId: NotRequired[str]
    ExecutionId: NotRequired[str]
    TaskType: NotRequired[MaintenanceWindowTaskTypeType]
    Parameters: NotRequired[str]
    Status: NotRequired[MaintenanceWindowExecutionStatusType]
    StatusDetails: NotRequired[str]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    OwnerInformation: NotRequired[str]
    WindowTargetId: NotRequired[str]


class MaintenanceWindowExecutionTypeDef(TypedDict):
    WindowId: NotRequired[str]
    WindowExecutionId: NotRequired[str]
    Status: NotRequired[MaintenanceWindowExecutionStatusType]
    StatusDetails: NotRequired[str]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]


class TargetTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[Sequence[str]]


class ScheduledWindowExecutionTypeDef(TypedDict):
    WindowId: NotRequired[str]
    Name: NotRequired[str]
    ExecutionTime: NotRequired[str]


class MaintenanceWindowIdentityForTargetTypeDef(TypedDict):
    WindowId: NotRequired[str]
    Name: NotRequired[str]


class MaintenanceWindowIdentityTypeDef(TypedDict):
    WindowId: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Enabled: NotRequired[bool]
    Duration: NotRequired[int]
    Cutoff: NotRequired[int]
    Schedule: NotRequired[str]
    ScheduleTimezone: NotRequired[str]
    ScheduleOffset: NotRequired[int]
    EndDate: NotRequired[str]
    StartDate: NotRequired[str]
    NextExecutionTime: NotRequired[str]


class OpsItemFilterTypeDef(TypedDict):
    Key: OpsItemFilterKeyType
    Values: Sequence[str]
    Operator: OpsItemFilterOperatorType


class ParameterStringFilterTypeDef(TypedDict):
    Key: str
    Option: NotRequired[str]
    Values: NotRequired[Sequence[str]]


class ParametersFilterTypeDef(TypedDict):
    Key: ParametersFilterKeyType
    Values: Sequence[str]


class PatchBaselineIdentityTypeDef(TypedDict):
    BaselineId: NotRequired[str]
    BaselineName: NotRequired[str]
    OperatingSystem: NotRequired[OperatingSystemType]
    BaselineDescription: NotRequired[str]
    DefaultBaseline: NotRequired[bool]


class DescribePatchGroupStateRequestRequestTypeDef(TypedDict):
    PatchGroup: str


class DescribePatchPropertiesRequestRequestTypeDef(TypedDict):
    OperatingSystem: OperatingSystemType
    Property: PatchPropertyType
    PatchSet: NotRequired[PatchSetType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class SessionFilterTypeDef(TypedDict):
    key: SessionFilterKeyType
    value: str


class DisassociateOpsItemRelatedItemRequestRequestTypeDef(TypedDict):
    OpsItemId: str
    AssociationId: str


class DocumentDefaultVersionDescriptionTypeDef(TypedDict):
    Name: NotRequired[str]
    DefaultVersion: NotRequired[str]
    DefaultVersionName: NotRequired[str]


DocumentParameterTypeDef = TypedDict(
    "DocumentParameterTypeDef",
    {
        "Name": NotRequired[str],
        "Type": NotRequired[DocumentParameterTypeType],
        "Description": NotRequired[str],
        "DefaultValue": NotRequired[str],
    },
)


class ReviewInformationTypeDef(TypedDict):
    ReviewedTime: NotRequired[datetime]
    Status: NotRequired[ReviewStatusType]
    Reviewer: NotRequired[str]


class DocumentFilterTypeDef(TypedDict):
    key: DocumentFilterKeyType
    value: str


class DocumentKeyValuesFilterTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[Sequence[str]]


DocumentReviewCommentSourceTypeDef = TypedDict(
    "DocumentReviewCommentSourceTypeDef",
    {
        "Type": NotRequired[Literal["Comment"]],
        "Content": NotRequired[str],
    },
)


class DocumentVersionInfoTypeDef(TypedDict):
    Name: NotRequired[str]
    DisplayName: NotRequired[str]
    DocumentVersion: NotRequired[str]
    VersionName: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    IsDefaultVersion: NotRequired[bool]
    DocumentFormat: NotRequired[DocumentFormatType]
    Status: NotRequired[DocumentStatusType]
    StatusInformation: NotRequired[str]
    ReviewStatus: NotRequired[ReviewStatusType]


class PatchStatusTypeDef(TypedDict):
    DeploymentStatus: NotRequired[PatchDeploymentStatusType]
    ComplianceLevel: NotRequired[PatchComplianceLevelType]
    ApprovalDate: NotRequired[datetime]


class FailureDetailsTypeDef(TypedDict):
    FailureStage: NotRequired[str]
    FailureType: NotRequired[str]
    Details: NotRequired[Dict[str, List[str]]]


class GetAutomationExecutionRequestRequestTypeDef(TypedDict):
    AutomationExecutionId: str


class GetCalendarStateRequestRequestTypeDef(TypedDict):
    CalendarNames: Sequence[str]
    AtTime: NotRequired[str]


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class GetCommandInvocationRequestRequestTypeDef(TypedDict):
    CommandId: str
    InstanceId: str
    PluginName: NotRequired[str]


class GetConnectionStatusRequestRequestTypeDef(TypedDict):
    Target: str


class GetDefaultPatchBaselineRequestRequestTypeDef(TypedDict):
    OperatingSystem: NotRequired[OperatingSystemType]


class GetDocumentRequestRequestTypeDef(TypedDict):
    Name: str
    VersionName: NotRequired[str]
    DocumentVersion: NotRequired[str]
    DocumentFormat: NotRequired[DocumentFormatType]


class GetExecutionPreviewRequestRequestTypeDef(TypedDict):
    ExecutionPreviewId: str


InventoryFilterTypeDef = TypedDict(
    "InventoryFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
        "Type": NotRequired[InventoryQueryOperatorTypeType],
    },
)


class ResultAttributeTypeDef(TypedDict):
    TypeName: str


class GetInventorySchemaRequestRequestTypeDef(TypedDict):
    TypeName: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Aggregator: NotRequired[bool]
    SubType: NotRequired[bool]


class GetMaintenanceWindowExecutionRequestRequestTypeDef(TypedDict):
    WindowExecutionId: str


class GetMaintenanceWindowExecutionTaskInvocationRequestRequestTypeDef(TypedDict):
    WindowExecutionId: str
    TaskId: str
    InvocationId: str


class GetMaintenanceWindowExecutionTaskRequestRequestTypeDef(TypedDict):
    WindowExecutionId: str
    TaskId: str


class MaintenanceWindowTaskParameterValueExpressionOutputTypeDef(TypedDict):
    Values: NotRequired[List[str]]


class GetMaintenanceWindowRequestRequestTypeDef(TypedDict):
    WindowId: str


class GetMaintenanceWindowTaskRequestRequestTypeDef(TypedDict):
    WindowId: str
    WindowTaskId: str


class LoggingInfoTypeDef(TypedDict):
    S3BucketName: str
    S3Region: str
    S3KeyPrefix: NotRequired[str]


class GetOpsItemRequestRequestTypeDef(TypedDict):
    OpsItemId: str
    OpsItemArn: NotRequired[str]


class GetOpsMetadataRequestRequestTypeDef(TypedDict):
    OpsMetadataArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


OpsFilterTypeDef = TypedDict(
    "OpsFilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
        "Type": NotRequired[OpsFilterOperatorTypeType],
    },
)


class OpsResultAttributeTypeDef(TypedDict):
    TypeName: str


class GetParameterHistoryRequestRequestTypeDef(TypedDict):
    Name: str
    WithDecryption: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetParameterRequestRequestTypeDef(TypedDict):
    Name: str
    WithDecryption: NotRequired[bool]


ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "Name": NotRequired[str],
        "Type": NotRequired[ParameterTypeType],
        "Value": NotRequired[str],
        "Version": NotRequired[int],
        "Selector": NotRequired[str],
        "SourceResult": NotRequired[str],
        "LastModifiedDate": NotRequired[datetime],
        "ARN": NotRequired[str],
        "DataType": NotRequired[str],
    },
)


class GetParametersRequestRequestTypeDef(TypedDict):
    Names: Sequence[str]
    WithDecryption: NotRequired[bool]


class GetPatchBaselineForPatchGroupRequestRequestTypeDef(TypedDict):
    PatchGroup: str
    OperatingSystem: NotRequired[OperatingSystemType]


class GetPatchBaselineRequestRequestTypeDef(TypedDict):
    BaselineId: str


class PatchSourceOutputTypeDef(TypedDict):
    Name: str
    Products: List[str]
    Configuration: str


class GetResourcePoliciesRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class GetResourcePoliciesResponseEntryTypeDef(TypedDict):
    PolicyId: NotRequired[str]
    PolicyHash: NotRequired[str]
    Policy: NotRequired[str]


class GetServiceSettingRequestRequestTypeDef(TypedDict):
    SettingId: str


class ServiceSettingTypeDef(TypedDict):
    SettingId: NotRequired[str]
    SettingValue: NotRequired[str]
    LastModifiedDate: NotRequired[datetime]
    LastModifiedUser: NotRequired[str]
    ARN: NotRequired[str]
    Status: NotRequired[str]


class InstanceAggregatedAssociationOverviewTypeDef(TypedDict):
    DetailedStatus: NotRequired[str]
    InstanceAssociationStatusAggregatedCount: NotRequired[Dict[str, int]]


class S3OutputLocationTypeDef(TypedDict):
    OutputS3Region: NotRequired[str]
    OutputS3BucketName: NotRequired[str]
    OutputS3KeyPrefix: NotRequired[str]


class S3OutputUrlTypeDef(TypedDict):
    OutputUrl: NotRequired[str]


class InstanceInfoTypeDef(TypedDict):
    AgentType: NotRequired[str]
    AgentVersion: NotRequired[str]
    ComputerName: NotRequired[str]
    InstanceStatus: NotRequired[str]
    IpAddress: NotRequired[str]
    ManagedStatus: NotRequired[ManagedStatusType]
    PlatformType: NotRequired[PlatformTypeType]
    PlatformName: NotRequired[str]
    PlatformVersion: NotRequired[str]
    ResourceType: NotRequired[ResourceTypeType]


class InventoryDeletionSummaryItemTypeDef(TypedDict):
    Version: NotRequired[str]
    Count: NotRequired[int]
    RemainingCount: NotRequired[int]


class InventoryItemAttributeTypeDef(TypedDict):
    Name: str
    DataType: InventoryAttributeDataTypeType


class InventoryItemTypeDef(TypedDict):
    TypeName: str
    SchemaVersion: str
    CaptureTime: str
    ContentHash: NotRequired[str]
    Content: NotRequired[Sequence[Mapping[str, str]]]
    Context: NotRequired[Mapping[str, str]]


class InventoryResultItemTypeDef(TypedDict):
    TypeName: str
    SchemaVersion: str
    Content: List[Dict[str, str]]
    CaptureTime: NotRequired[str]
    ContentHash: NotRequired[str]


class LabelParameterVersionRequestRequestTypeDef(TypedDict):
    Name: str
    Labels: Sequence[str]
    ParameterVersion: NotRequired[int]


class ListAssociationVersionsRequestRequestTypeDef(TypedDict):
    AssociationId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListDocumentMetadataHistoryRequestRequestTypeDef(TypedDict):
    Name: str
    Metadata: Literal["DocumentReviews"]
    DocumentVersion: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDocumentVersionsRequestRequestTypeDef(TypedDict):
    Name: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


NodeFilterTypeDef = TypedDict(
    "NodeFilterTypeDef",
    {
        "Key": NodeFilterKeyType,
        "Values": Sequence[str],
        "Type": NotRequired[NodeFilterOperatorTypeType],
    },
)


class NodeAggregatorPaginatorTypeDef(TypedDict):
    AggregatorType: Literal["Count"]
    TypeName: Literal["Instance"]
    AttributeName: NodeAttributeNameType
    Aggregators: NotRequired[Sequence[Mapping[str, Any]]]


class NodeAggregatorTypeDef(TypedDict):
    AggregatorType: Literal["Count"]
    TypeName: Literal["Instance"]
    AttributeName: NodeAttributeNameType
    Aggregators: NotRequired[Sequence[Mapping[str, Any]]]


class OpsItemEventFilterTypeDef(TypedDict):
    Key: Literal["OpsItemId"]
    Values: Sequence[str]
    Operator: Literal["Equal"]


class OpsItemRelatedItemsFilterTypeDef(TypedDict):
    Key: OpsItemRelatedItemsFilterKeyType
    Values: Sequence[str]
    Operator: Literal["Equal"]


class OpsMetadataFilterTypeDef(TypedDict):
    Key: str
    Values: Sequence[str]


class OpsMetadataTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    OpsMetadataArn: NotRequired[str]
    LastModifiedDate: NotRequired[datetime]
    LastModifiedUser: NotRequired[str]
    CreationDate: NotRequired[datetime]


class ListResourceDataSyncRequestRequestTypeDef(TypedDict):
    SyncType: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceType: ResourceTypeForTaggingType
    ResourceId: str


class MaintenanceWindowAutomationParametersOutputTypeDef(TypedDict):
    DocumentVersion: NotRequired[str]
    Parameters: NotRequired[Dict[str, List[str]]]


class MaintenanceWindowAutomationParametersTypeDef(TypedDict):
    DocumentVersion: NotRequired[str]
    Parameters: NotRequired[Mapping[str, Sequence[str]]]


class MaintenanceWindowLambdaParametersOutputTypeDef(TypedDict):
    ClientContext: NotRequired[str]
    Qualifier: NotRequired[str]
    Payload: NotRequired[bytes]


class MaintenanceWindowStepFunctionsParametersTypeDef(TypedDict):
    Input: NotRequired[str]
    Name: NotRequired[str]


class MaintenanceWindowTaskParameterValueExpressionTypeDef(TypedDict):
    Values: NotRequired[Sequence[str]]


class ModifyDocumentPermissionRequestRequestTypeDef(TypedDict):
    Name: str
    PermissionType: Literal["Share"]
    AccountIdsToAdd: NotRequired[Sequence[str]]
    AccountIdsToRemove: NotRequired[Sequence[str]]
    SharedDocumentVersion: NotRequired[str]


class NodeOwnerInfoTypeDef(TypedDict):
    AccountId: NotRequired[str]
    OrganizationalUnitId: NotRequired[str]
    OrganizationalUnitPath: NotRequired[str]


class NotificationConfigTypeDef(TypedDict):
    NotificationArn: NotRequired[str]
    NotificationEvents: NotRequired[Sequence[NotificationEventType]]
    NotificationType: NotRequired[NotificationTypeType]


class OpsEntityItemTypeDef(TypedDict):
    CaptureTime: NotRequired[str]
    Content: NotRequired[List[Dict[str, str]]]


class OpsItemIdentityTypeDef(TypedDict):
    Arn: NotRequired[str]


class ParameterInlinePolicyTypeDef(TypedDict):
    PolicyText: NotRequired[str]
    PolicyType: NotRequired[str]
    PolicyStatus: NotRequired[str]


class ParentStepDetailsTypeDef(TypedDict):
    StepExecutionId: NotRequired[str]
    StepName: NotRequired[str]
    Action: NotRequired[str]
    Iteration: NotRequired[int]
    IteratorValue: NotRequired[str]


class PatchFilterOutputTypeDef(TypedDict):
    Key: PatchFilterKeyType
    Values: List[str]


class PatchFilterTypeDef(TypedDict):
    Key: PatchFilterKeyType
    Values: Sequence[str]


class PatchSourceTypeDef(TypedDict):
    Name: str
    Products: Sequence[str]
    Configuration: str


class PutResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Policy: str
    PolicyId: NotRequired[str]
    PolicyHash: NotRequired[str]


class RegisterDefaultPatchBaselineRequestRequestTypeDef(TypedDict):
    BaselineId: str


class RegisterPatchBaselineForPatchGroupRequestRequestTypeDef(TypedDict):
    BaselineId: str
    PatchGroup: str


class RemoveTagsFromResourceRequestRequestTypeDef(TypedDict):
    ResourceType: ResourceTypeForTaggingType
    ResourceId: str
    TagKeys: Sequence[str]


class ResetServiceSettingRequestRequestTypeDef(TypedDict):
    SettingId: str


class ResourceDataSyncOrganizationalUnitTypeDef(TypedDict):
    OrganizationalUnitId: NotRequired[str]


class ResourceDataSyncDestinationDataSharingTypeDef(TypedDict):
    DestinationDataSharingType: NotRequired[str]


class ResumeSessionRequestRequestTypeDef(TypedDict):
    SessionId: str


class SendAutomationSignalRequestRequestTypeDef(TypedDict):
    AutomationExecutionId: str
    SignalType: SignalTypeType
    Payload: NotRequired[Mapping[str, Sequence[str]]]


class SessionManagerOutputUrlTypeDef(TypedDict):
    S3OutputUrl: NotRequired[str]
    CloudWatchOutputUrl: NotRequired[str]


class StartAssociationsOnceRequestRequestTypeDef(TypedDict):
    AssociationIds: Sequence[str]


class StartSessionRequestRequestTypeDef(TypedDict):
    Target: str
    DocumentName: NotRequired[str]
    Reason: NotRequired[str]
    Parameters: NotRequired[Mapping[str, Sequence[str]]]


StopAutomationExecutionRequestRequestTypeDef = TypedDict(
    "StopAutomationExecutionRequestRequestTypeDef",
    {
        "AutomationExecutionId": str,
        "Type": NotRequired[StopTypeType],
    },
)


class TerminateSessionRequestRequestTypeDef(TypedDict):
    SessionId: str


class UnlabelParameterVersionRequestRequestTypeDef(TypedDict):
    Name: str
    ParameterVersion: int
    Labels: Sequence[str]


class UpdateDocumentDefaultVersionRequestRequestTypeDef(TypedDict):
    Name: str
    DocumentVersion: str


class UpdateMaintenanceWindowRequestRequestTypeDef(TypedDict):
    WindowId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    StartDate: NotRequired[str]
    EndDate: NotRequired[str]
    Schedule: NotRequired[str]
    ScheduleTimezone: NotRequired[str]
    ScheduleOffset: NotRequired[int]
    Duration: NotRequired[int]
    Cutoff: NotRequired[int]
    AllowUnassociatedTargets: NotRequired[bool]
    Enabled: NotRequired[bool]
    Replace: NotRequired[bool]


class UpdateManagedInstanceRoleRequestRequestTypeDef(TypedDict):
    InstanceId: str
    IamRole: str


class UpdateServiceSettingRequestRequestTypeDef(TypedDict):
    SettingId: str
    SettingValue: str


class ActivationTypeDef(TypedDict):
    ActivationId: NotRequired[str]
    Description: NotRequired[str]
    DefaultInstanceName: NotRequired[str]
    IamRole: NotRequired[str]
    RegistrationLimit: NotRequired[int]
    RegistrationsCount: NotRequired[int]
    ExpirationDate: NotRequired[datetime]
    Expired: NotRequired[bool]
    CreatedDate: NotRequired[datetime]
    Tags: NotRequired[List[TagTypeDef]]


class AddTagsToResourceRequestRequestTypeDef(TypedDict):
    ResourceType: ResourceTypeForTaggingType
    ResourceId: str
    Tags: Sequence[TagTypeDef]


class CreateMaintenanceWindowRequestRequestTypeDef(TypedDict):
    Name: str
    Schedule: str
    Duration: int
    Cutoff: int
    AllowUnassociatedTargets: bool
    Description: NotRequired[str]
    StartDate: NotRequired[str]
    EndDate: NotRequired[str]
    ScheduleTimezone: NotRequired[str]
    ScheduleOffset: NotRequired[int]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


PutParameterRequestRequestTypeDef = TypedDict(
    "PutParameterRequestRequestTypeDef",
    {
        "Name": str,
        "Value": str,
        "Description": NotRequired[str],
        "Type": NotRequired[ParameterTypeType],
        "KeyId": NotRequired[str],
        "Overwrite": NotRequired[bool],
        "AllowedPattern": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "Tier": NotRequired[ParameterTierType],
        "Policies": NotRequired[str],
        "DataType": NotRequired[str],
    },
)


class AlarmConfigurationOutputTypeDef(TypedDict):
    Alarms: List[AlarmTypeDef]
    IgnorePollAlarmFailure: NotRequired[bool]


class AlarmConfigurationTypeDef(TypedDict):
    Alarms: Sequence[AlarmTypeDef]
    IgnorePollAlarmFailure: NotRequired[bool]


class AssociateOpsItemRelatedItemResponseTypeDef(TypedDict):
    AssociationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CancelMaintenanceWindowExecutionResultTypeDef(TypedDict):
    WindowExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateActivationResultTypeDef(TypedDict):
    ActivationId: str
    ActivationCode: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMaintenanceWindowResultTypeDef(TypedDict):
    WindowId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOpsItemResponseTypeDef(TypedDict):
    OpsItemId: str
    OpsItemArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOpsMetadataResultTypeDef(TypedDict):
    OpsMetadataArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePatchBaselineResultTypeDef(TypedDict):
    BaselineId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMaintenanceWindowResultTypeDef(TypedDict):
    WindowId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteParametersResultTypeDef(TypedDict):
    DeletedParameters: List[str]
    InvalidParameters: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePatchBaselineResultTypeDef(TypedDict):
    BaselineId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeregisterPatchBaselineForPatchGroupResultTypeDef(TypedDict):
    BaselineId: str
    PatchGroup: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeregisterTargetFromMaintenanceWindowResultTypeDef(TypedDict):
    WindowId: str
    WindowTargetId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeregisterTaskFromMaintenanceWindowResultTypeDef(TypedDict):
    WindowId: str
    WindowTaskId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDocumentPermissionResponseTypeDef(TypedDict):
    AccountIds: List[str]
    AccountSharingInfoList: List[AccountSharingInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribePatchGroupStateResultTypeDef(TypedDict):
    Instances: int
    InstancesWithInstalledPatches: int
    InstancesWithInstalledOtherPatches: int
    InstancesWithInstalledPendingRebootPatches: int
    InstancesWithInstalledRejectedPatches: int
    InstancesWithMissingPatches: int
    InstancesWithFailedPatches: int
    InstancesWithNotApplicablePatches: int
    InstancesWithUnreportedNotApplicablePatches: int
    InstancesWithCriticalNonCompliantPatches: int
    InstancesWithSecurityNonCompliantPatches: int
    InstancesWithOtherNonCompliantPatches: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePatchPropertiesResultTypeDef(TypedDict):
    Properties: List[Dict[str, str]]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetCalendarStateResponseTypeDef(TypedDict):
    State: CalendarStateType
    AtTime: str
    NextTransitionTime: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetConnectionStatusResponseTypeDef(TypedDict):
    Target: str
    Status: ConnectionStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetDefaultPatchBaselineResultTypeDef(TypedDict):
    BaselineId: str
    OperatingSystem: OperatingSystemType
    ResponseMetadata: ResponseMetadataTypeDef


class GetDeployablePatchSnapshotForInstanceResultTypeDef(TypedDict):
    InstanceId: str
    SnapshotId: str
    SnapshotDownloadUrl: str
    Product: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetMaintenanceWindowExecutionResultTypeDef(TypedDict):
    WindowExecutionId: str
    TaskIds: List[str]
    Status: MaintenanceWindowExecutionStatusType
    StatusDetails: str
    StartTime: datetime
    EndTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetMaintenanceWindowExecutionTaskInvocationResultTypeDef(TypedDict):
    WindowExecutionId: str
    TaskExecutionId: str
    InvocationId: str
    ExecutionId: str
    TaskType: MaintenanceWindowTaskTypeType
    Parameters: str
    Status: MaintenanceWindowExecutionStatusType
    StatusDetails: str
    StartTime: datetime
    EndTime: datetime
    OwnerInformation: str
    WindowTargetId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetMaintenanceWindowResultTypeDef(TypedDict):
    WindowId: str
    Name: str
    Description: str
    StartDate: str
    EndDate: str
    Schedule: str
    ScheduleTimezone: str
    ScheduleOffset: int
    NextExecutionTime: str
    Duration: int
    Cutoff: int
    AllowUnassociatedTargets: bool
    Enabled: bool
    CreatedDate: datetime
    ModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetPatchBaselineForPatchGroupResultTypeDef(TypedDict):
    BaselineId: str
    PatchGroup: str
    OperatingSystem: OperatingSystemType
    ResponseMetadata: ResponseMetadataTypeDef


class LabelParameterVersionResultTypeDef(TypedDict):
    InvalidLabels: List[str]
    ParameterVersion: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListInventoryEntriesResultTypeDef(TypedDict):
    TypeName: str
    InstanceId: str
    SchemaVersion: str
    CaptureTime: str
    Entries: List[Dict[str, str]]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListNodesSummaryResultTypeDef(TypedDict):
    Summary: List[Dict[str, str]]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResultTypeDef(TypedDict):
    TagList: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PutInventoryResultTypeDef(TypedDict):
    Message: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutParameterResultTypeDef(TypedDict):
    Version: int
    Tier: ParameterTierType
    ResponseMetadata: ResponseMetadataTypeDef


class PutResourcePolicyResponseTypeDef(TypedDict):
    PolicyId: str
    PolicyHash: str
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterDefaultPatchBaselineResultTypeDef(TypedDict):
    BaselineId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterPatchBaselineForPatchGroupResultTypeDef(TypedDict):
    BaselineId: str
    PatchGroup: str
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterTargetWithMaintenanceWindowResultTypeDef(TypedDict):
    WindowTargetId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterTaskWithMaintenanceWindowResultTypeDef(TypedDict):
    WindowTaskId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ResumeSessionResponseTypeDef(TypedDict):
    SessionId: str
    TokenValue: str
    StreamUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartAutomationExecutionResultTypeDef(TypedDict):
    AutomationExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartChangeRequestExecutionResultTypeDef(TypedDict):
    AutomationExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartExecutionPreviewResponseTypeDef(TypedDict):
    ExecutionPreviewId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartSessionResponseTypeDef(TypedDict):
    SessionId: str
    TokenValue: str
    StreamUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class TerminateSessionResponseTypeDef(TypedDict):
    SessionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UnlabelParameterVersionResultTypeDef(TypedDict):
    RemovedLabels: List[str]
    InvalidLabels: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMaintenanceWindowResultTypeDef(TypedDict):
    WindowId: str
    Name: str
    Description: str
    StartDate: str
    EndDate: str
    Schedule: str
    ScheduleTimezone: str
    ScheduleOffset: int
    Duration: int
    Cutoff: int
    AllowUnassociatedTargets: bool
    Enabled: bool
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateOpsMetadataResultTypeDef(TypedDict):
    OpsMetadataArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociationTypeDef(TypedDict):
    Name: NotRequired[str]
    InstanceId: NotRequired[str]
    AssociationId: NotRequired[str]
    AssociationVersion: NotRequired[str]
    DocumentVersion: NotRequired[str]
    Targets: NotRequired[List[TargetOutputTypeDef]]
    LastExecutionDate: NotRequired[datetime]
    Overview: NotRequired[AssociationOverviewTypeDef]
    ScheduleExpression: NotRequired[str]
    AssociationName: NotRequired[str]
    ScheduleOffset: NotRequired[int]
    Duration: NotRequired[int]
    TargetMaps: NotRequired[List[Dict[str, List[str]]]]


class MaintenanceWindowTargetTypeDef(TypedDict):
    WindowId: NotRequired[str]
    WindowTargetId: NotRequired[str]
    ResourceType: NotRequired[MaintenanceWindowResourceTypeType]
    Targets: NotRequired[List[TargetOutputTypeDef]]
    OwnerInformation: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]


class UpdateMaintenanceWindowTargetResultTypeDef(TypedDict):
    WindowId: str
    WindowTargetId: str
    Targets: List[TargetOutputTypeDef]
    OwnerInformation: str
    Name: str
    Description: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAssociationExecutionsRequestRequestTypeDef(TypedDict):
    AssociationId: str
    Filters: NotRequired[Sequence[AssociationExecutionFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class AssociationExecutionTargetTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    AssociationVersion: NotRequired[str]
    ExecutionId: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[str]
    Status: NotRequired[str]
    DetailedStatus: NotRequired[str]
    LastExecutionDate: NotRequired[datetime]
    OutputSource: NotRequired[OutputSourceTypeDef]


class DescribeAssociationExecutionTargetsRequestRequestTypeDef(TypedDict):
    AssociationId: str
    ExecutionId: str
    Filters: NotRequired[Sequence[AssociationExecutionTargetsFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListAssociationsRequestRequestTypeDef(TypedDict):
    AssociationFilterList: NotRequired[Sequence[AssociationFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class AssociationStatusTypeDef(TypedDict):
    Date: TimestampTypeDef
    Name: AssociationStatusNameType
    Message: str
    AdditionalInfo: NotRequired[str]


class ComplianceExecutionSummaryTypeDef(TypedDict):
    ExecutionTime: TimestampTypeDef
    ExecutionId: NotRequired[str]
    ExecutionType: NotRequired[str]


class UpdateDocumentRequestRequestTypeDef(TypedDict):
    Content: str
    Name: str
    Attachments: NotRequired[Sequence[AttachmentsSourceTypeDef]]
    DisplayName: NotRequired[str]
    VersionName: NotRequired[str]
    DocumentVersion: NotRequired[str]
    DocumentFormat: NotRequired[DocumentFormatType]
    TargetType: NotRequired[str]


class DescribeAutomationExecutionsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[AutomationExecutionFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class AutomationExecutionPreviewTypeDef(TypedDict):
    StepPreviews: NotRequired[Dict[ImpactTypeType, int]]
    Regions: NotRequired[List[str]]
    TargetPreviews: NotRequired[List[TargetPreviewTypeDef]]
    TotalAccounts: NotRequired[int]


class MaintenanceWindowLambdaParametersTypeDef(TypedDict):
    ClientContext: NotRequired[str]
    Qualifier: NotRequired[str]
    Payload: NotRequired[BlobTypeDef]


class GetCommandInvocationResultTypeDef(TypedDict):
    CommandId: str
    InstanceId: str
    Comment: str
    DocumentName: str
    DocumentVersion: str
    PluginName: str
    ResponseCode: int
    ExecutionStartDateTime: str
    ExecutionElapsedTime: str
    ExecutionEndDateTime: str
    Status: CommandInvocationStatusType
    StatusDetails: str
    StandardOutputContent: str
    StandardOutputUrl: str
    StandardErrorContent: str
    StandardErrorUrl: str
    CloudWatchOutputConfig: CloudWatchOutputConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListCommandInvocationsRequestRequestTypeDef(TypedDict):
    CommandId: NotRequired[str]
    InstanceId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[CommandFilterTypeDef]]
    Details: NotRequired[bool]


class ListCommandsRequestRequestTypeDef(TypedDict):
    CommandId: NotRequired[str]
    InstanceId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[CommandFilterTypeDef]]


class CommandInvocationTypeDef(TypedDict):
    CommandId: NotRequired[str]
    InstanceId: NotRequired[str]
    InstanceName: NotRequired[str]
    Comment: NotRequired[str]
    DocumentName: NotRequired[str]
    DocumentVersion: NotRequired[str]
    RequestedDateTime: NotRequired[datetime]
    Status: NotRequired[CommandInvocationStatusType]
    StatusDetails: NotRequired[str]
    TraceOutput: NotRequired[str]
    StandardOutputUrl: NotRequired[str]
    StandardErrorUrl: NotRequired[str]
    CommandPlugins: NotRequired[List[CommandPluginTypeDef]]
    ServiceRole: NotRequired[str]
    NotificationConfig: NotRequired[NotificationConfigOutputTypeDef]
    CloudWatchOutputConfig: NotRequired[CloudWatchOutputConfigTypeDef]


class MaintenanceWindowRunCommandParametersOutputTypeDef(TypedDict):
    Comment: NotRequired[str]
    CloudWatchOutputConfig: NotRequired[CloudWatchOutputConfigTypeDef]
    DocumentHash: NotRequired[str]
    DocumentHashType: NotRequired[DocumentHashTypeType]
    DocumentVersion: NotRequired[str]
    NotificationConfig: NotRequired[NotificationConfigOutputTypeDef]
    OutputS3BucketName: NotRequired[str]
    OutputS3KeyPrefix: NotRequired[str]
    Parameters: NotRequired[Dict[str, List[str]]]
    ServiceRoleArn: NotRequired[str]
    TimeoutSeconds: NotRequired[int]


class ComplianceItemTypeDef(TypedDict):
    ComplianceType: NotRequired[str]
    ResourceType: NotRequired[str]
    ResourceId: NotRequired[str]
    Id: NotRequired[str]
    Title: NotRequired[str]
    Status: NotRequired[ComplianceStatusType]
    Severity: NotRequired[ComplianceSeverityType]
    ExecutionSummary: NotRequired[ComplianceExecutionSummaryOutputTypeDef]
    Details: NotRequired[Dict[str, str]]


class ListComplianceItemsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ComplianceStringFilterTypeDef]]
    ResourceIds: NotRequired[Sequence[str]]
    ResourceTypes: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListComplianceSummariesRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ComplianceStringFilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListResourceComplianceSummariesRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ComplianceStringFilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class CompliantSummaryTypeDef(TypedDict):
    CompliantCount: NotRequired[int]
    SeveritySummary: NotRequired[SeveritySummaryTypeDef]


class NonCompliantSummaryTypeDef(TypedDict):
    NonCompliantCount: NotRequired[int]
    SeveritySummary: NotRequired[SeveritySummaryTypeDef]


class CreateActivationRequestRequestTypeDef(TypedDict):
    IamRole: str
    Description: NotRequired[str]
    DefaultInstanceName: NotRequired[str]
    RegistrationLimit: NotRequired[int]
    ExpirationDate: NotRequired[TimestampTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    RegistrationMetadata: NotRequired[Sequence[RegistrationMetadataItemTypeDef]]


class CreateDocumentRequestRequestTypeDef(TypedDict):
    Content: str
    Name: str
    Requires: NotRequired[Sequence[DocumentRequiresTypeDef]]
    Attachments: NotRequired[Sequence[AttachmentsSourceTypeDef]]
    DisplayName: NotRequired[str]
    VersionName: NotRequired[str]
    DocumentType: NotRequired[DocumentTypeType]
    DocumentFormat: NotRequired[DocumentFormatType]
    TargetType: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DocumentIdentifierTypeDef(TypedDict):
    Name: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    DisplayName: NotRequired[str]
    Owner: NotRequired[str]
    VersionName: NotRequired[str]
    PlatformTypes: NotRequired[List[PlatformTypeType]]
    DocumentVersion: NotRequired[str]
    DocumentType: NotRequired[DocumentTypeType]
    SchemaVersion: NotRequired[str]
    DocumentFormat: NotRequired[DocumentFormatType]
    TargetType: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]
    Requires: NotRequired[List[DocumentRequiresTypeDef]]
    ReviewStatus: NotRequired[ReviewStatusType]
    Author: NotRequired[str]


class GetDocumentResultTypeDef(TypedDict):
    Name: str
    CreatedDate: datetime
    DisplayName: str
    VersionName: str
    DocumentVersion: str
    Status: DocumentStatusType
    StatusInformation: str
    Content: str
    DocumentType: DocumentTypeType
    DocumentFormat: DocumentFormatType
    Requires: List[DocumentRequiresTypeDef]
    AttachmentsContent: List[AttachmentContentTypeDef]
    ReviewStatus: ReviewStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class OpsItemSummaryTypeDef(TypedDict):
    CreatedBy: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]
    Priority: NotRequired[int]
    Source: NotRequired[str]
    Status: NotRequired[OpsItemStatusType]
    OpsItemId: NotRequired[str]
    Title: NotRequired[str]
    OperationalData: NotRequired[Dict[str, OpsItemDataValueTypeDef]]
    Category: NotRequired[str]
    Severity: NotRequired[str]
    OpsItemType: NotRequired[str]
    ActualStartTime: NotRequired[datetime]
    ActualEndTime: NotRequired[datetime]
    PlannedStartTime: NotRequired[datetime]
    PlannedEndTime: NotRequired[datetime]


class CreateOpsItemRequestRequestTypeDef(TypedDict):
    Description: str
    Source: str
    Title: str
    OpsItemType: NotRequired[str]
    OperationalData: NotRequired[Mapping[str, OpsItemDataValueTypeDef]]
    Notifications: NotRequired[Sequence[OpsItemNotificationTypeDef]]
    Priority: NotRequired[int]
    RelatedOpsItems: NotRequired[Sequence[RelatedOpsItemTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    Category: NotRequired[str]
    Severity: NotRequired[str]
    ActualStartTime: NotRequired[TimestampTypeDef]
    ActualEndTime: NotRequired[TimestampTypeDef]
    PlannedStartTime: NotRequired[TimestampTypeDef]
    PlannedEndTime: NotRequired[TimestampTypeDef]
    AccountId: NotRequired[str]


class OpsItemTypeDef(TypedDict):
    CreatedBy: NotRequired[str]
    OpsItemType: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    Description: NotRequired[str]
    LastModifiedBy: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]
    Notifications: NotRequired[List[OpsItemNotificationTypeDef]]
    Priority: NotRequired[int]
    RelatedOpsItems: NotRequired[List[RelatedOpsItemTypeDef]]
    Status: NotRequired[OpsItemStatusType]
    OpsItemId: NotRequired[str]
    Version: NotRequired[str]
    Title: NotRequired[str]
    Source: NotRequired[str]
    OperationalData: NotRequired[Dict[str, OpsItemDataValueTypeDef]]
    Category: NotRequired[str]
    Severity: NotRequired[str]
    ActualStartTime: NotRequired[datetime]
    ActualEndTime: NotRequired[datetime]
    PlannedStartTime: NotRequired[datetime]
    PlannedEndTime: NotRequired[datetime]
    OpsItemArn: NotRequired[str]


class UpdateOpsItemRequestRequestTypeDef(TypedDict):
    OpsItemId: str
    Description: NotRequired[str]
    OperationalData: NotRequired[Mapping[str, OpsItemDataValueTypeDef]]
    OperationalDataToDelete: NotRequired[Sequence[str]]
    Notifications: NotRequired[Sequence[OpsItemNotificationTypeDef]]
    Priority: NotRequired[int]
    RelatedOpsItems: NotRequired[Sequence[RelatedOpsItemTypeDef]]
    Status: NotRequired[OpsItemStatusType]
    Title: NotRequired[str]
    Category: NotRequired[str]
    Severity: NotRequired[str]
    ActualStartTime: NotRequired[TimestampTypeDef]
    ActualEndTime: NotRequired[TimestampTypeDef]
    PlannedStartTime: NotRequired[TimestampTypeDef]
    PlannedEndTime: NotRequired[TimestampTypeDef]
    OpsItemArn: NotRequired[str]


class CreateOpsMetadataRequestRequestTypeDef(TypedDict):
    ResourceId: str
    Metadata: NotRequired[Mapping[str, MetadataValueTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class GetOpsMetadataResultTypeDef(TypedDict):
    ResourceId: str
    Metadata: Dict[str, MetadataValueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateOpsMetadataRequestRequestTypeDef(TypedDict):
    OpsMetadataArn: str
    MetadataToUpdate: NotRequired[Mapping[str, MetadataValueTypeDef]]
    KeysToDelete: NotRequired[Sequence[str]]


class DescribeActivationsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[DescribeActivationsFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeActivationsRequestDescribeActivationsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[DescribeActivationsFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef(
    TypedDict
):
    AssociationId: str
    ExecutionId: str
    Filters: NotRequired[Sequence[AssociationExecutionTargetsFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef(TypedDict):
    AssociationId: str
    Filters: NotRequired[Sequence[AssociationExecutionFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAutomationExecutionsRequestDescribeAutomationExecutionsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[AutomationExecutionFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef(
    TypedDict
):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef(
    TypedDict
):
    BaselineId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef(
    TypedDict
):
    InstanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef(TypedDict):
    InstanceIds: Sequence[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInventoryDeletionsRequestDescribeInventoryDeletionsPaginateTypeDef(TypedDict):
    DeletionId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef(TypedDict):
    OperatingSystem: OperatingSystemType
    Property: PatchPropertyType
    PatchSet: NotRequired[PatchSetType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetInventorySchemaRequestGetInventorySchemaPaginateTypeDef(TypedDict):
    TypeName: NotRequired[str]
    Aggregator: NotRequired[bool]
    SubType: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetParameterHistoryRequestGetParameterHistoryPaginateTypeDef(TypedDict):
    Name: str
    WithDecryption: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef(TypedDict):
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef(TypedDict):
    AssociationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssociationsRequestListAssociationsPaginateTypeDef(TypedDict):
    AssociationFilterList: NotRequired[Sequence[AssociationFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCommandInvocationsRequestListCommandInvocationsPaginateTypeDef(TypedDict):
    CommandId: NotRequired[str]
    InstanceId: NotRequired[str]
    Filters: NotRequired[Sequence[CommandFilterTypeDef]]
    Details: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCommandsRequestListCommandsPaginateTypeDef(TypedDict):
    CommandId: NotRequired[str]
    InstanceId: NotRequired[str]
    Filters: NotRequired[Sequence[CommandFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListComplianceItemsRequestListComplianceItemsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ComplianceStringFilterTypeDef]]
    ResourceIds: NotRequired[Sequence[str]]
    ResourceTypes: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListComplianceSummariesRequestListComplianceSummariesPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ComplianceStringFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef(TypedDict):
    Name: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourceComplianceSummariesRequestListResourceComplianceSummariesPaginateTypeDef(
    TypedDict
):
    Filters: NotRequired[Sequence[ComplianceStringFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourceDataSyncRequestListResourceDataSyncPaginateTypeDef(TypedDict):
    SyncType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef(
    TypedDict
):
    AutomationExecutionId: str
    Filters: NotRequired[Sequence[StepExecutionFilterTypeDef]]
    ReverseOrder: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAutomationStepExecutionsRequestRequestTypeDef(TypedDict):
    AutomationExecutionId: str
    Filters: NotRequired[Sequence[StepExecutionFilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ReverseOrder: NotRequired[bool]


class DescribeAvailablePatchesRequestDescribeAvailablePatchesPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[PatchOrchestratorFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAvailablePatchesRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[PatchOrchestratorFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef(TypedDict):
    InstanceId: str
    Filters: NotRequired[Sequence[PatchOrchestratorFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstancePatchesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Filters: NotRequired[Sequence[PatchOrchestratorFilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribePatchBaselinesRequestDescribePatchBaselinesPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[PatchOrchestratorFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribePatchBaselinesRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[PatchOrchestratorFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribePatchGroupsRequestDescribePatchGroupsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[PatchOrchestratorFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribePatchGroupsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[PatchOrchestratorFilterTypeDef]]
    NextToken: NotRequired[str]


class DescribeAvailablePatchesResultTypeDef(TypedDict):
    Patches: List[PatchTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeEffectiveInstanceAssociationsResultTypeDef(TypedDict):
    Associations: List[InstanceAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeInstanceInformationRequestDescribeInstanceInformationPaginateTypeDef(TypedDict):
    InstanceInformationFilterList: NotRequired[Sequence[InstanceInformationFilterTypeDef]]
    Filters: NotRequired[Sequence[InstanceInformationStringFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstanceInformationRequestRequestTypeDef(TypedDict):
    InstanceInformationFilterList: NotRequired[Sequence[InstanceInformationFilterTypeDef]]
    Filters: NotRequired[Sequence[InstanceInformationStringFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef(
    TypedDict
):
    PatchGroup: str
    Filters: NotRequired[Sequence[InstancePatchStateFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstancePatchStatesForPatchGroupRequestRequestTypeDef(TypedDict):
    PatchGroup: str
    Filters: NotRequired[Sequence[InstancePatchStateFilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeInstancePatchStatesForPatchGroupResultTypeDef(TypedDict):
    InstancePatchStates: List[InstancePatchStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeInstancePatchStatesResultTypeDef(TypedDict):
    InstancePatchStates: List[InstancePatchStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeInstancePatchesResultTypeDef(TypedDict):
    Patches: List[PatchComplianceDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeInstancePropertiesRequestDescribeInstancePropertiesPaginateTypeDef(TypedDict):
    InstancePropertyFilterList: NotRequired[Sequence[InstancePropertyFilterTypeDef]]
    FiltersWithOperator: NotRequired[Sequence[InstancePropertyStringFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstancePropertiesRequestRequestTypeDef(TypedDict):
    InstancePropertyFilterList: NotRequired[Sequence[InstancePropertyFilterTypeDef]]
    FiltersWithOperator: NotRequired[Sequence[InstancePropertyStringFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef(
    TypedDict
):
    WindowExecutionId: str
    TaskId: str
    Filters: NotRequired[Sequence[MaintenanceWindowFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeMaintenanceWindowExecutionTaskInvocationsRequestRequestTypeDef(TypedDict):
    WindowExecutionId: str
    TaskId: str
    Filters: NotRequired[Sequence[MaintenanceWindowFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef(
    TypedDict
):
    WindowExecutionId: str
    Filters: NotRequired[Sequence[MaintenanceWindowFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeMaintenanceWindowExecutionTasksRequestRequestTypeDef(TypedDict):
    WindowExecutionId: str
    Filters: NotRequired[Sequence[MaintenanceWindowFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef(
    TypedDict
):
    WindowId: str
    Filters: NotRequired[Sequence[MaintenanceWindowFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeMaintenanceWindowExecutionsRequestRequestTypeDef(TypedDict):
    WindowId: str
    Filters: NotRequired[Sequence[MaintenanceWindowFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef(
    TypedDict
):
    WindowId: str
    Filters: NotRequired[Sequence[MaintenanceWindowFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeMaintenanceWindowTargetsRequestRequestTypeDef(TypedDict):
    WindowId: str
    Filters: NotRequired[Sequence[MaintenanceWindowFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef(TypedDict):
    WindowId: str
    Filters: NotRequired[Sequence[MaintenanceWindowFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeMaintenanceWindowTasksRequestRequestTypeDef(TypedDict):
    WindowId: str
    Filters: NotRequired[Sequence[MaintenanceWindowFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowsRequestDescribeMaintenanceWindowsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[MaintenanceWindowFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeMaintenanceWindowsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[MaintenanceWindowFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef(TypedDict):
    WindowExecutionTaskInvocationIdentities: List[
        MaintenanceWindowExecutionTaskInvocationIdentityTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowExecutionsResultTypeDef(TypedDict):
    WindowExecutions: List[MaintenanceWindowExecutionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowScheduleRequestDescribeMaintenanceWindowSchedulePaginateTypeDef(
    TypedDict
):
    WindowId: NotRequired[str]
    Targets: NotRequired[Sequence[TargetTypeDef]]
    ResourceType: NotRequired[MaintenanceWindowResourceTypeType]
    Filters: NotRequired[Sequence[PatchOrchestratorFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeMaintenanceWindowScheduleRequestRequestTypeDef(TypedDict):
    WindowId: NotRequired[str]
    Targets: NotRequired[Sequence[TargetTypeDef]]
    ResourceType: NotRequired[MaintenanceWindowResourceTypeType]
    Filters: NotRequired[Sequence[PatchOrchestratorFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef(
    TypedDict
):
    Targets: Sequence[TargetTypeDef]
    ResourceType: MaintenanceWindowResourceTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeMaintenanceWindowsForTargetRequestRequestTypeDef(TypedDict):
    Targets: Sequence[TargetTypeDef]
    ResourceType: MaintenanceWindowResourceTypeType
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class RegisterTargetWithMaintenanceWindowRequestRequestTypeDef(TypedDict):
    WindowId: str
    ResourceType: MaintenanceWindowResourceTypeType
    Targets: Sequence[TargetTypeDef]
    OwnerInformation: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    ClientToken: NotRequired[str]


TargetUnionTypeDef = Union[TargetTypeDef, TargetOutputTypeDef]


class UpdateMaintenanceWindowTargetRequestRequestTypeDef(TypedDict):
    WindowId: str
    WindowTargetId: str
    Targets: NotRequired[Sequence[TargetTypeDef]]
    OwnerInformation: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Replace: NotRequired[bool]


class DescribeMaintenanceWindowScheduleResultTypeDef(TypedDict):
    ScheduledWindowExecutions: List[ScheduledWindowExecutionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowsForTargetResultTypeDef(TypedDict):
    WindowIdentities: List[MaintenanceWindowIdentityForTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowsResultTypeDef(TypedDict):
    WindowIdentities: List[MaintenanceWindowIdentityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeOpsItemsRequestDescribeOpsItemsPaginateTypeDef(TypedDict):
    OpsItemFilters: NotRequired[Sequence[OpsItemFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeOpsItemsRequestRequestTypeDef(TypedDict):
    OpsItemFilters: NotRequired[Sequence[OpsItemFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetParametersByPathRequestGetParametersByPathPaginateTypeDef(TypedDict):
    Path: str
    Recursive: NotRequired[bool]
    ParameterFilters: NotRequired[Sequence[ParameterStringFilterTypeDef]]
    WithDecryption: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetParametersByPathRequestRequestTypeDef(TypedDict):
    Path: str
    Recursive: NotRequired[bool]
    ParameterFilters: NotRequired[Sequence[ParameterStringFilterTypeDef]]
    WithDecryption: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeParametersRequestDescribeParametersPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ParametersFilterTypeDef]]
    ParameterFilters: NotRequired[Sequence[ParameterStringFilterTypeDef]]
    Shared: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeParametersRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ParametersFilterTypeDef]]
    ParameterFilters: NotRequired[Sequence[ParameterStringFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Shared: NotRequired[bool]


class DescribePatchBaselinesResultTypeDef(TypedDict):
    BaselineIdentities: List[PatchBaselineIdentityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PatchGroupPatchBaselineMappingTypeDef(TypedDict):
    PatchGroup: NotRequired[str]
    BaselineIdentity: NotRequired[PatchBaselineIdentityTypeDef]


class DescribeSessionsRequestDescribeSessionsPaginateTypeDef(TypedDict):
    State: SessionStateType
    Filters: NotRequired[Sequence[SessionFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSessionsRequestRequestTypeDef(TypedDict):
    State: SessionStateType
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[SessionFilterTypeDef]]


class UpdateDocumentDefaultVersionResultTypeDef(TypedDict):
    Description: DocumentDefaultVersionDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DocumentDescriptionTypeDef(TypedDict):
    Sha1: NotRequired[str]
    Hash: NotRequired[str]
    HashType: NotRequired[DocumentHashTypeType]
    Name: NotRequired[str]
    DisplayName: NotRequired[str]
    VersionName: NotRequired[str]
    Owner: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    Status: NotRequired[DocumentStatusType]
    StatusInformation: NotRequired[str]
    DocumentVersion: NotRequired[str]
    Description: NotRequired[str]
    Parameters: NotRequired[List[DocumentParameterTypeDef]]
    PlatformTypes: NotRequired[List[PlatformTypeType]]
    DocumentType: NotRequired[DocumentTypeType]
    SchemaVersion: NotRequired[str]
    LatestVersion: NotRequired[str]
    DefaultVersion: NotRequired[str]
    DocumentFormat: NotRequired[DocumentFormatType]
    TargetType: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]
    AttachmentsInformation: NotRequired[List[AttachmentInformationTypeDef]]
    Requires: NotRequired[List[DocumentRequiresTypeDef]]
    Author: NotRequired[str]
    ReviewInformation: NotRequired[List[ReviewInformationTypeDef]]
    ApprovedVersion: NotRequired[str]
    PendingReviewVersion: NotRequired[str]
    ReviewStatus: NotRequired[ReviewStatusType]
    Category: NotRequired[List[str]]
    CategoryEnum: NotRequired[List[str]]


class ListDocumentsRequestListDocumentsPaginateTypeDef(TypedDict):
    DocumentFilterList: NotRequired[Sequence[DocumentFilterTypeDef]]
    Filters: NotRequired[Sequence[DocumentKeyValuesFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDocumentsRequestRequestTypeDef(TypedDict):
    DocumentFilterList: NotRequired[Sequence[DocumentFilterTypeDef]]
    Filters: NotRequired[Sequence[DocumentKeyValuesFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DocumentReviewerResponseSourceTypeDef(TypedDict):
    CreateTime: NotRequired[datetime]
    UpdatedTime: NotRequired[datetime]
    ReviewStatus: NotRequired[ReviewStatusType]
    Comment: NotRequired[List[DocumentReviewCommentSourceTypeDef]]
    Reviewer: NotRequired[str]


class DocumentReviewsTypeDef(TypedDict):
    Action: DocumentReviewActionType
    Comment: NotRequired[Sequence[DocumentReviewCommentSourceTypeDef]]


class ListDocumentVersionsResultTypeDef(TypedDict):
    DocumentVersions: List[DocumentVersionInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class EffectivePatchTypeDef(TypedDict):
    Patch: NotRequired[PatchTypeDef]
    PatchStatus: NotRequired[PatchStatusTypeDef]


class GetCommandInvocationRequestCommandExecutedWaitTypeDef(TypedDict):
    CommandId: str
    InstanceId: str
    PluginName: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class InventoryGroupTypeDef(TypedDict):
    Name: str
    Filters: Sequence[InventoryFilterTypeDef]


class ListInventoryEntriesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    TypeName: str
    Filters: NotRequired[Sequence[InventoryFilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class OpsAggregatorPaginatorTypeDef(TypedDict):
    AggregatorType: NotRequired[str]
    TypeName: NotRequired[str]
    AttributeName: NotRequired[str]
    Values: NotRequired[Mapping[str, str]]
    Filters: NotRequired[Sequence[OpsFilterTypeDef]]
    Aggregators: NotRequired[Sequence[Mapping[str, Any]]]


class OpsAggregatorTypeDef(TypedDict):
    AggregatorType: NotRequired[str]
    TypeName: NotRequired[str]
    AttributeName: NotRequired[str]
    Values: NotRequired[Mapping[str, str]]
    Filters: NotRequired[Sequence[OpsFilterTypeDef]]
    Aggregators: NotRequired[Sequence[Mapping[str, Any]]]


class GetParameterResultTypeDef(TypedDict):
    Parameter: ParameterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetParametersByPathResultTypeDef(TypedDict):
    Parameters: List[ParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetParametersResultTypeDef(TypedDict):
    Parameters: List[ParameterTypeDef]
    InvalidParameters: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetResourcePoliciesResponseTypeDef(TypedDict):
    Policies: List[GetResourcePoliciesResponseEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetServiceSettingResultTypeDef(TypedDict):
    ServiceSetting: ServiceSettingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ResetServiceSettingResultTypeDef(TypedDict):
    ServiceSetting: ServiceSettingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class InstanceInformationTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    PingStatus: NotRequired[PingStatusType]
    LastPingDateTime: NotRequired[datetime]
    AgentVersion: NotRequired[str]
    IsLatestVersion: NotRequired[bool]
    PlatformType: NotRequired[PlatformTypeType]
    PlatformName: NotRequired[str]
    PlatformVersion: NotRequired[str]
    ActivationId: NotRequired[str]
    IamRole: NotRequired[str]
    RegistrationDate: NotRequired[datetime]
    ResourceType: NotRequired[ResourceTypeType]
    Name: NotRequired[str]
    IPAddress: NotRequired[str]
    ComputerName: NotRequired[str]
    AssociationStatus: NotRequired[str]
    LastAssociationExecutionDate: NotRequired[datetime]
    LastSuccessfulAssociationExecutionDate: NotRequired[datetime]
    AssociationOverview: NotRequired[InstanceAggregatedAssociationOverviewTypeDef]
    SourceId: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]


class InstancePropertyTypeDef(TypedDict):
    Name: NotRequired[str]
    InstanceId: NotRequired[str]
    InstanceType: NotRequired[str]
    InstanceRole: NotRequired[str]
    KeyName: NotRequired[str]
    InstanceState: NotRequired[str]
    Architecture: NotRequired[str]
    IPAddress: NotRequired[str]
    LaunchTime: NotRequired[datetime]
    PingStatus: NotRequired[PingStatusType]
    LastPingDateTime: NotRequired[datetime]
    AgentVersion: NotRequired[str]
    PlatformType: NotRequired[PlatformTypeType]
    PlatformName: NotRequired[str]
    PlatformVersion: NotRequired[str]
    ActivationId: NotRequired[str]
    IamRole: NotRequired[str]
    RegistrationDate: NotRequired[datetime]
    ResourceType: NotRequired[str]
    ComputerName: NotRequired[str]
    AssociationStatus: NotRequired[str]
    LastAssociationExecutionDate: NotRequired[datetime]
    LastSuccessfulAssociationExecutionDate: NotRequired[datetime]
    AssociationOverview: NotRequired[InstanceAggregatedAssociationOverviewTypeDef]
    SourceId: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]


class InstanceAssociationOutputLocationTypeDef(TypedDict):
    S3Location: NotRequired[S3OutputLocationTypeDef]


class InstanceAssociationOutputUrlTypeDef(TypedDict):
    S3OutputUrl: NotRequired[S3OutputUrlTypeDef]


class NodeTypeTypeDef(TypedDict):
    Instance: NotRequired[InstanceInfoTypeDef]


class InventoryDeletionSummaryTypeDef(TypedDict):
    TotalCount: NotRequired[int]
    RemainingCount: NotRequired[int]
    SummaryItems: NotRequired[List[InventoryDeletionSummaryItemTypeDef]]


class InventoryItemSchemaTypeDef(TypedDict):
    TypeName: str
    Attributes: List[InventoryItemAttributeTypeDef]
    Version: NotRequired[str]
    DisplayName: NotRequired[str]


class PutInventoryRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Items: Sequence[InventoryItemTypeDef]


class InventoryResultEntityTypeDef(TypedDict):
    Id: NotRequired[str]
    Data: NotRequired[Dict[str, InventoryResultItemTypeDef]]


class ListNodesRequestListNodesPaginateTypeDef(TypedDict):
    SyncName: NotRequired[str]
    Filters: NotRequired[Sequence[NodeFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNodesRequestRequestTypeDef(TypedDict):
    SyncName: NotRequired[str]
    Filters: NotRequired[Sequence[NodeFilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListNodesSummaryRequestListNodesSummaryPaginateTypeDef(TypedDict):
    Aggregators: Sequence[NodeAggregatorPaginatorTypeDef]
    SyncName: NotRequired[str]
    Filters: NotRequired[Sequence[NodeFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNodesSummaryRequestRequestTypeDef(TypedDict):
    Aggregators: Sequence[NodeAggregatorTypeDef]
    SyncName: NotRequired[str]
    Filters: NotRequired[Sequence[NodeFilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListOpsItemEventsRequestListOpsItemEventsPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[OpsItemEventFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOpsItemEventsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[OpsItemEventFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListOpsItemRelatedItemsRequestListOpsItemRelatedItemsPaginateTypeDef(TypedDict):
    OpsItemId: NotRequired[str]
    Filters: NotRequired[Sequence[OpsItemRelatedItemsFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOpsItemRelatedItemsRequestRequestTypeDef(TypedDict):
    OpsItemId: NotRequired[str]
    Filters: NotRequired[Sequence[OpsItemRelatedItemsFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListOpsMetadataRequestListOpsMetadataPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[OpsMetadataFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOpsMetadataRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[OpsMetadataFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListOpsMetadataResultTypeDef(TypedDict):
    OpsMetadataList: List[OpsMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


MaintenanceWindowAutomationParametersUnionTypeDef = Union[
    MaintenanceWindowAutomationParametersTypeDef, MaintenanceWindowAutomationParametersOutputTypeDef
]
MaintenanceWindowTaskParameterValueExpressionUnionTypeDef = Union[
    MaintenanceWindowTaskParameterValueExpressionTypeDef,
    MaintenanceWindowTaskParameterValueExpressionOutputTypeDef,
]
NotificationConfigUnionTypeDef = Union[NotificationConfigTypeDef, NotificationConfigOutputTypeDef]


class OpsEntityTypeDef(TypedDict):
    Id: NotRequired[str]
    Data: NotRequired[Dict[str, OpsEntityItemTypeDef]]


class OpsItemEventSummaryTypeDef(TypedDict):
    OpsItemId: NotRequired[str]
    EventId: NotRequired[str]
    Source: NotRequired[str]
    DetailType: NotRequired[str]
    Detail: NotRequired[str]
    CreatedBy: NotRequired[OpsItemIdentityTypeDef]
    CreatedTime: NotRequired[datetime]


class OpsItemRelatedItemSummaryTypeDef(TypedDict):
    OpsItemId: NotRequired[str]
    AssociationId: NotRequired[str]
    ResourceType: NotRequired[str]
    AssociationType: NotRequired[str]
    ResourceUri: NotRequired[str]
    CreatedBy: NotRequired[OpsItemIdentityTypeDef]
    CreatedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[OpsItemIdentityTypeDef]
    LastModifiedTime: NotRequired[datetime]


ParameterHistoryTypeDef = TypedDict(
    "ParameterHistoryTypeDef",
    {
        "Name": NotRequired[str],
        "Type": NotRequired[ParameterTypeType],
        "KeyId": NotRequired[str],
        "LastModifiedDate": NotRequired[datetime],
        "LastModifiedUser": NotRequired[str],
        "Description": NotRequired[str],
        "Value": NotRequired[str],
        "AllowedPattern": NotRequired[str],
        "Version": NotRequired[int],
        "Labels": NotRequired[List[str]],
        "Tier": NotRequired[ParameterTierType],
        "Policies": NotRequired[List[ParameterInlinePolicyTypeDef]],
        "DataType": NotRequired[str],
    },
)
ParameterMetadataTypeDef = TypedDict(
    "ParameterMetadataTypeDef",
    {
        "Name": NotRequired[str],
        "ARN": NotRequired[str],
        "Type": NotRequired[ParameterTypeType],
        "KeyId": NotRequired[str],
        "LastModifiedDate": NotRequired[datetime],
        "LastModifiedUser": NotRequired[str],
        "Description": NotRequired[str],
        "AllowedPattern": NotRequired[str],
        "Version": NotRequired[int],
        "Tier": NotRequired[ParameterTierType],
        "Policies": NotRequired[List[ParameterInlinePolicyTypeDef]],
        "DataType": NotRequired[str],
    },
)


class PatchFilterGroupOutputTypeDef(TypedDict):
    PatchFilters: List[PatchFilterOutputTypeDef]


PatchFilterUnionTypeDef = Union[PatchFilterTypeDef, PatchFilterOutputTypeDef]
PatchSourceUnionTypeDef = Union[PatchSourceTypeDef, PatchSourceOutputTypeDef]


class ResourceDataSyncAwsOrganizationsSourceOutputTypeDef(TypedDict):
    OrganizationSourceType: str
    OrganizationalUnits: NotRequired[List[ResourceDataSyncOrganizationalUnitTypeDef]]


class ResourceDataSyncAwsOrganizationsSourceTypeDef(TypedDict):
    OrganizationSourceType: str
    OrganizationalUnits: NotRequired[Sequence[ResourceDataSyncOrganizationalUnitTypeDef]]


class ResourceDataSyncS3DestinationTypeDef(TypedDict):
    BucketName: str
    SyncFormat: Literal["JsonSerDe"]
    Region: str
    Prefix: NotRequired[str]
    AWSKMSKeyARN: NotRequired[str]
    DestinationDataSharing: NotRequired[ResourceDataSyncDestinationDataSharingTypeDef]


class SessionTypeDef(TypedDict):
    SessionId: NotRequired[str]
    Target: NotRequired[str]
    Status: NotRequired[SessionStatusType]
    StartDate: NotRequired[datetime]
    EndDate: NotRequired[datetime]
    DocumentName: NotRequired[str]
    Owner: NotRequired[str]
    Reason: NotRequired[str]
    Details: NotRequired[str]
    OutputUrl: NotRequired[SessionManagerOutputUrlTypeDef]
    MaxSessionDuration: NotRequired[str]


class DescribeActivationsResultTypeDef(TypedDict):
    ActivationList: List[ActivationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AssociationExecutionTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    AssociationVersion: NotRequired[str]
    ExecutionId: NotRequired[str]
    Status: NotRequired[str]
    DetailedStatus: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastExecutionDate: NotRequired[datetime]
    ResourceCountByStatus: NotRequired[str]
    AlarmConfiguration: NotRequired[AlarmConfigurationOutputTypeDef]
    TriggeredAlarms: NotRequired[List[AlarmStateInformationTypeDef]]


class CommandTypeDef(TypedDict):
    CommandId: NotRequired[str]
    DocumentName: NotRequired[str]
    DocumentVersion: NotRequired[str]
    Comment: NotRequired[str]
    ExpiresAfter: NotRequired[datetime]
    Parameters: NotRequired[Dict[str, List[str]]]
    InstanceIds: NotRequired[List[str]]
    Targets: NotRequired[List[TargetOutputTypeDef]]
    RequestedDateTime: NotRequired[datetime]
    Status: NotRequired[CommandStatusType]
    StatusDetails: NotRequired[str]
    OutputS3Region: NotRequired[str]
    OutputS3BucketName: NotRequired[str]
    OutputS3KeyPrefix: NotRequired[str]
    MaxConcurrency: NotRequired[str]
    MaxErrors: NotRequired[str]
    TargetCount: NotRequired[int]
    CompletedCount: NotRequired[int]
    ErrorCount: NotRequired[int]
    DeliveryTimedOutCount: NotRequired[int]
    ServiceRole: NotRequired[str]
    NotificationConfig: NotRequired[NotificationConfigOutputTypeDef]
    CloudWatchOutputConfig: NotRequired[CloudWatchOutputConfigTypeDef]
    TimeoutSeconds: NotRequired[int]
    AlarmConfiguration: NotRequired[AlarmConfigurationOutputTypeDef]
    TriggeredAlarms: NotRequired[List[AlarmStateInformationTypeDef]]


GetMaintenanceWindowExecutionTaskResultTypeDef = TypedDict(
    "GetMaintenanceWindowExecutionTaskResultTypeDef",
    {
        "WindowExecutionId": str,
        "TaskExecutionId": str,
        "TaskArn": str,
        "ServiceRole": str,
        "Type": MaintenanceWindowTaskTypeType,
        "TaskParameters": List[
            Dict[str, MaintenanceWindowTaskParameterValueExpressionOutputTypeDef]
        ],
        "Priority": int,
        "MaxConcurrency": str,
        "MaxErrors": str,
        "Status": MaintenanceWindowExecutionStatusType,
        "StatusDetails": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "AlarmConfiguration": AlarmConfigurationOutputTypeDef,
        "TriggeredAlarms": List[AlarmStateInformationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class MaintenanceWindowExecutionTaskIdentityTypeDef(TypedDict):
    WindowExecutionId: NotRequired[str]
    TaskExecutionId: NotRequired[str]
    Status: NotRequired[MaintenanceWindowExecutionStatusType]
    StatusDetails: NotRequired[str]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    TaskArn: NotRequired[str]
    TaskType: NotRequired[MaintenanceWindowTaskTypeType]
    AlarmConfiguration: NotRequired[AlarmConfigurationOutputTypeDef]
    TriggeredAlarms: NotRequired[List[AlarmStateInformationTypeDef]]


MaintenanceWindowTaskTypeDef = TypedDict(
    "MaintenanceWindowTaskTypeDef",
    {
        "WindowId": NotRequired[str],
        "WindowTaskId": NotRequired[str],
        "TaskArn": NotRequired[str],
        "Type": NotRequired[MaintenanceWindowTaskTypeType],
        "Targets": NotRequired[List[TargetOutputTypeDef]],
        "TaskParameters": NotRequired[
            Dict[str, MaintenanceWindowTaskParameterValueExpressionOutputTypeDef]
        ],
        "Priority": NotRequired[int],
        "LoggingInfo": NotRequired[LoggingInfoTypeDef],
        "ServiceRoleArn": NotRequired[str],
        "MaxConcurrency": NotRequired[str],
        "MaxErrors": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "CutoffBehavior": NotRequired[MaintenanceWindowTaskCutoffBehaviorType],
        "AlarmConfiguration": NotRequired[AlarmConfigurationOutputTypeDef],
    },
)


class TargetLocationOutputTypeDef(TypedDict):
    Accounts: NotRequired[List[str]]
    Regions: NotRequired[List[str]]
    TargetLocationMaxConcurrency: NotRequired[str]
    TargetLocationMaxErrors: NotRequired[str]
    ExecutionRoleName: NotRequired[str]
    TargetLocationAlarmConfiguration: NotRequired[AlarmConfigurationOutputTypeDef]
    IncludeChildOrganizationUnits: NotRequired[bool]
    ExcludeAccounts: NotRequired[List[str]]
    Targets: NotRequired[List[TargetOutputTypeDef]]
    TargetsMaxConcurrency: NotRequired[str]
    TargetsMaxErrors: NotRequired[str]


AlarmConfigurationUnionTypeDef = Union[AlarmConfigurationTypeDef, AlarmConfigurationOutputTypeDef]


class SendCommandRequestRequestTypeDef(TypedDict):
    DocumentName: str
    InstanceIds: NotRequired[Sequence[str]]
    Targets: NotRequired[Sequence[TargetTypeDef]]
    DocumentVersion: NotRequired[str]
    DocumentHash: NotRequired[str]
    DocumentHashType: NotRequired[DocumentHashTypeType]
    TimeoutSeconds: NotRequired[int]
    Comment: NotRequired[str]
    Parameters: NotRequired[Mapping[str, Sequence[str]]]
    OutputS3Region: NotRequired[str]
    OutputS3BucketName: NotRequired[str]
    OutputS3KeyPrefix: NotRequired[str]
    MaxConcurrency: NotRequired[str]
    MaxErrors: NotRequired[str]
    ServiceRoleArn: NotRequired[str]
    NotificationConfig: NotRequired[NotificationConfigTypeDef]
    CloudWatchOutputConfig: NotRequired[CloudWatchOutputConfigTypeDef]
    AlarmConfiguration: NotRequired[AlarmConfigurationTypeDef]


class ListAssociationsResultTypeDef(TypedDict):
    Associations: List[AssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowTargetsResultTypeDef(TypedDict):
    Targets: List[MaintenanceWindowTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeAssociationExecutionTargetsResultTypeDef(TypedDict):
    AssociationExecutionTargets: List[AssociationExecutionTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateAssociationStatusRequestRequestTypeDef(TypedDict):
    Name: str
    InstanceId: str
    AssociationStatus: AssociationStatusTypeDef


class PutComplianceItemsRequestRequestTypeDef(TypedDict):
    ResourceId: str
    ResourceType: str
    ComplianceType: str
    ExecutionSummary: ComplianceExecutionSummaryTypeDef
    Items: Sequence[ComplianceItemEntryTypeDef]
    ItemContentHash: NotRequired[str]
    UploadType: NotRequired[ComplianceUploadTypeType]


class ExecutionPreviewTypeDef(TypedDict):
    Automation: NotRequired[AutomationExecutionPreviewTypeDef]


MaintenanceWindowLambdaParametersUnionTypeDef = Union[
    MaintenanceWindowLambdaParametersTypeDef, MaintenanceWindowLambdaParametersOutputTypeDef
]


class ListCommandInvocationsResultTypeDef(TypedDict):
    CommandInvocations: List[CommandInvocationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MaintenanceWindowTaskInvocationParametersOutputTypeDef(TypedDict):
    RunCommand: NotRequired[MaintenanceWindowRunCommandParametersOutputTypeDef]
    Automation: NotRequired[MaintenanceWindowAutomationParametersOutputTypeDef]
    StepFunctions: NotRequired[MaintenanceWindowStepFunctionsParametersTypeDef]
    Lambda: NotRequired[MaintenanceWindowLambdaParametersOutputTypeDef]


class ListComplianceItemsResultTypeDef(TypedDict):
    ComplianceItems: List[ComplianceItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ComplianceSummaryItemTypeDef(TypedDict):
    ComplianceType: NotRequired[str]
    CompliantSummary: NotRequired[CompliantSummaryTypeDef]
    NonCompliantSummary: NotRequired[NonCompliantSummaryTypeDef]


class ResourceComplianceSummaryItemTypeDef(TypedDict):
    ComplianceType: NotRequired[str]
    ResourceType: NotRequired[str]
    ResourceId: NotRequired[str]
    Status: NotRequired[ComplianceStatusType]
    OverallSeverity: NotRequired[ComplianceSeverityType]
    ExecutionSummary: NotRequired[ComplianceExecutionSummaryOutputTypeDef]
    CompliantSummary: NotRequired[CompliantSummaryTypeDef]
    NonCompliantSummary: NotRequired[NonCompliantSummaryTypeDef]


class ListDocumentsResultTypeDef(TypedDict):
    DocumentIdentifiers: List[DocumentIdentifierTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeOpsItemsResponseTypeDef(TypedDict):
    OpsItemSummaries: List[OpsItemSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetOpsItemResponseTypeDef(TypedDict):
    OpsItem: OpsItemTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePatchGroupsResultTypeDef(TypedDict):
    Mappings: List[PatchGroupPatchBaselineMappingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateDocumentResultTypeDef(TypedDict):
    DocumentDescription: DocumentDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDocumentResultTypeDef(TypedDict):
    Document: DocumentDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDocumentResultTypeDef(TypedDict):
    DocumentDescription: DocumentDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DocumentMetadataResponseInfoTypeDef(TypedDict):
    ReviewerResponse: NotRequired[List[DocumentReviewerResponseSourceTypeDef]]


class UpdateDocumentMetadataRequestRequestTypeDef(TypedDict):
    Name: str
    DocumentReviews: DocumentReviewsTypeDef
    DocumentVersion: NotRequired[str]


class DescribeEffectivePatchesForPatchBaselineResultTypeDef(TypedDict):
    EffectivePatches: List[EffectivePatchTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class InventoryAggregatorPaginatorTypeDef(TypedDict):
    Expression: NotRequired[str]
    Aggregators: NotRequired[Sequence[Mapping[str, Any]]]
    Groups: NotRequired[Sequence[InventoryGroupTypeDef]]


class InventoryAggregatorTypeDef(TypedDict):
    Expression: NotRequired[str]
    Aggregators: NotRequired[Sequence[Mapping[str, Any]]]
    Groups: NotRequired[Sequence[InventoryGroupTypeDef]]


class GetOpsSummaryRequestGetOpsSummaryPaginateTypeDef(TypedDict):
    SyncName: NotRequired[str]
    Filters: NotRequired[Sequence[OpsFilterTypeDef]]
    Aggregators: NotRequired[Sequence[OpsAggregatorPaginatorTypeDef]]
    ResultAttributes: NotRequired[Sequence[OpsResultAttributeTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetOpsSummaryRequestRequestTypeDef(TypedDict):
    SyncName: NotRequired[str]
    Filters: NotRequired[Sequence[OpsFilterTypeDef]]
    Aggregators: NotRequired[Sequence[OpsAggregatorTypeDef]]
    ResultAttributes: NotRequired[Sequence[OpsResultAttributeTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeInstanceInformationResultTypeDef(TypedDict):
    InstanceInformationList: List[InstanceInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeInstancePropertiesResultTypeDef(TypedDict):
    InstanceProperties: List[InstancePropertyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class InstanceAssociationStatusInfoTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    Name: NotRequired[str]
    DocumentVersion: NotRequired[str]
    AssociationVersion: NotRequired[str]
    InstanceId: NotRequired[str]
    ExecutionDate: NotRequired[datetime]
    Status: NotRequired[str]
    DetailedStatus: NotRequired[str]
    ExecutionSummary: NotRequired[str]
    ErrorCode: NotRequired[str]
    OutputUrl: NotRequired[InstanceAssociationOutputUrlTypeDef]
    AssociationName: NotRequired[str]


class NodeTypeDef(TypedDict):
    CaptureTime: NotRequired[datetime]
    Id: NotRequired[str]
    Owner: NotRequired[NodeOwnerInfoTypeDef]
    Region: NotRequired[str]
    NodeType: NotRequired[NodeTypeTypeDef]


class DeleteInventoryResultTypeDef(TypedDict):
    DeletionId: str
    TypeName: str
    DeletionSummary: InventoryDeletionSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class InventoryDeletionStatusItemTypeDef(TypedDict):
    DeletionId: NotRequired[str]
    TypeName: NotRequired[str]
    DeletionStartTime: NotRequired[datetime]
    LastStatus: NotRequired[InventoryDeletionStatusType]
    LastStatusMessage: NotRequired[str]
    DeletionSummary: NotRequired[InventoryDeletionSummaryTypeDef]
    LastStatusUpdateTime: NotRequired[datetime]


class GetInventorySchemaResultTypeDef(TypedDict):
    Schemas: List[InventoryItemSchemaTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetInventoryResultTypeDef(TypedDict):
    Entities: List[InventoryResultEntityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MaintenanceWindowRunCommandParametersTypeDef(TypedDict):
    Comment: NotRequired[str]
    CloudWatchOutputConfig: NotRequired[CloudWatchOutputConfigTypeDef]
    DocumentHash: NotRequired[str]
    DocumentHashType: NotRequired[DocumentHashTypeType]
    DocumentVersion: NotRequired[str]
    NotificationConfig: NotRequired[NotificationConfigUnionTypeDef]
    OutputS3BucketName: NotRequired[str]
    OutputS3KeyPrefix: NotRequired[str]
    Parameters: NotRequired[Mapping[str, Sequence[str]]]
    ServiceRoleArn: NotRequired[str]
    TimeoutSeconds: NotRequired[int]


class GetOpsSummaryResultTypeDef(TypedDict):
    Entities: List[OpsEntityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListOpsItemEventsResponseTypeDef(TypedDict):
    Summaries: List[OpsItemEventSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListOpsItemRelatedItemsResponseTypeDef(TypedDict):
    Summaries: List[OpsItemRelatedItemSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetParameterHistoryResultTypeDef(TypedDict):
    Parameters: List[ParameterHistoryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeParametersResultTypeDef(TypedDict):
    Parameters: List[ParameterMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PatchRuleOutputTypeDef(TypedDict):
    PatchFilterGroup: PatchFilterGroupOutputTypeDef
    ComplianceLevel: NotRequired[PatchComplianceLevelType]
    ApproveAfterDays: NotRequired[int]
    ApproveUntilDate: NotRequired[str]
    EnableNonSecurity: NotRequired[bool]


class PatchFilterGroupTypeDef(TypedDict):
    PatchFilters: Sequence[PatchFilterUnionTypeDef]


class ResourceDataSyncSourceWithStateTypeDef(TypedDict):
    SourceType: NotRequired[str]
    AwsOrganizationsSource: NotRequired[ResourceDataSyncAwsOrganizationsSourceOutputTypeDef]
    SourceRegions: NotRequired[List[str]]
    IncludeFutureRegions: NotRequired[bool]
    State: NotRequired[str]
    EnableAllOpsDataSources: NotRequired[bool]


ResourceDataSyncAwsOrganizationsSourceUnionTypeDef = Union[
    ResourceDataSyncAwsOrganizationsSourceTypeDef,
    ResourceDataSyncAwsOrganizationsSourceOutputTypeDef,
]


class DescribeSessionsResponseTypeDef(TypedDict):
    Sessions: List[SessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeAssociationExecutionsResultTypeDef(TypedDict):
    AssociationExecutions: List[AssociationExecutionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListCommandsResultTypeDef(TypedDict):
    Commands: List[CommandTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SendCommandResultTypeDef(TypedDict):
    Command: CommandTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMaintenanceWindowExecutionTasksResultTypeDef(TypedDict):
    WindowExecutionTaskIdentities: List[MaintenanceWindowExecutionTaskIdentityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeMaintenanceWindowTasksResultTypeDef(TypedDict):
    Tasks: List[MaintenanceWindowTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AssociationDescriptionTypeDef(TypedDict):
    Name: NotRequired[str]
    InstanceId: NotRequired[str]
    AssociationVersion: NotRequired[str]
    Date: NotRequired[datetime]
    LastUpdateAssociationDate: NotRequired[datetime]
    Status: NotRequired[AssociationStatusOutputTypeDef]
    Overview: NotRequired[AssociationOverviewTypeDef]
    DocumentVersion: NotRequired[str]
    AutomationTargetParameterName: NotRequired[str]
    Parameters: NotRequired[Dict[str, List[str]]]
    AssociationId: NotRequired[str]
    Targets: NotRequired[List[TargetOutputTypeDef]]
    ScheduleExpression: NotRequired[str]
    OutputLocation: NotRequired[InstanceAssociationOutputLocationTypeDef]
    LastExecutionDate: NotRequired[datetime]
    LastSuccessfulExecutionDate: NotRequired[datetime]
    AssociationName: NotRequired[str]
    MaxErrors: NotRequired[str]
    MaxConcurrency: NotRequired[str]
    ComplianceSeverity: NotRequired[AssociationComplianceSeverityType]
    SyncCompliance: NotRequired[AssociationSyncComplianceType]
    ApplyOnlyAtCronInterval: NotRequired[bool]
    CalendarNames: NotRequired[List[str]]
    TargetLocations: NotRequired[List[TargetLocationOutputTypeDef]]
    ScheduleOffset: NotRequired[int]
    Duration: NotRequired[int]
    TargetMaps: NotRequired[List[Dict[str, List[str]]]]
    AlarmConfiguration: NotRequired[AlarmConfigurationOutputTypeDef]
    TriggeredAlarms: NotRequired[List[AlarmStateInformationTypeDef]]


class AssociationVersionInfoTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    AssociationVersion: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    Name: NotRequired[str]
    DocumentVersion: NotRequired[str]
    Parameters: NotRequired[Dict[str, List[str]]]
    Targets: NotRequired[List[TargetOutputTypeDef]]
    ScheduleExpression: NotRequired[str]
    OutputLocation: NotRequired[InstanceAssociationOutputLocationTypeDef]
    AssociationName: NotRequired[str]
    MaxErrors: NotRequired[str]
    MaxConcurrency: NotRequired[str]
    ComplianceSeverity: NotRequired[AssociationComplianceSeverityType]
    SyncCompliance: NotRequired[AssociationSyncComplianceType]
    ApplyOnlyAtCronInterval: NotRequired[bool]
    CalendarNames: NotRequired[List[str]]
    TargetLocations: NotRequired[List[TargetLocationOutputTypeDef]]
    ScheduleOffset: NotRequired[int]
    Duration: NotRequired[int]
    TargetMaps: NotRequired[List[Dict[str, List[str]]]]


class CreateAssociationBatchRequestEntryOutputTypeDef(TypedDict):
    Name: str
    InstanceId: NotRequired[str]
    Parameters: NotRequired[Dict[str, List[str]]]
    AutomationTargetParameterName: NotRequired[str]
    DocumentVersion: NotRequired[str]
    Targets: NotRequired[List[TargetOutputTypeDef]]
    ScheduleExpression: NotRequired[str]
    OutputLocation: NotRequired[InstanceAssociationOutputLocationTypeDef]
    AssociationName: NotRequired[str]
    MaxErrors: NotRequired[str]
    MaxConcurrency: NotRequired[str]
    ComplianceSeverity: NotRequired[AssociationComplianceSeverityType]
    SyncCompliance: NotRequired[AssociationSyncComplianceType]
    ApplyOnlyAtCronInterval: NotRequired[bool]
    CalendarNames: NotRequired[List[str]]
    TargetLocations: NotRequired[List[TargetLocationOutputTypeDef]]
    ScheduleOffset: NotRequired[int]
    Duration: NotRequired[int]
    TargetMaps: NotRequired[List[Dict[str, List[str]]]]
    AlarmConfiguration: NotRequired[AlarmConfigurationOutputTypeDef]


class RunbookOutputTypeDef(TypedDict):
    DocumentName: str
    DocumentVersion: NotRequired[str]
    Parameters: NotRequired[Dict[str, List[str]]]
    TargetParameterName: NotRequired[str]
    Targets: NotRequired[List[TargetOutputTypeDef]]
    TargetMaps: NotRequired[List[Dict[str, List[str]]]]
    MaxConcurrency: NotRequired[str]
    MaxErrors: NotRequired[str]
    TargetLocations: NotRequired[List[TargetLocationOutputTypeDef]]


class StepExecutionTypeDef(TypedDict):
    StepName: NotRequired[str]
    Action: NotRequired[str]
    TimeoutSeconds: NotRequired[int]
    OnFailure: NotRequired[str]
    MaxAttempts: NotRequired[int]
    ExecutionStartTime: NotRequired[datetime]
    ExecutionEndTime: NotRequired[datetime]
    StepStatus: NotRequired[AutomationExecutionStatusType]
    ResponseCode: NotRequired[str]
    Inputs: NotRequired[Dict[str, str]]
    Outputs: NotRequired[Dict[str, List[str]]]
    Response: NotRequired[str]
    FailureMessage: NotRequired[str]
    FailureDetails: NotRequired[FailureDetailsTypeDef]
    StepExecutionId: NotRequired[str]
    OverriddenParameters: NotRequired[Dict[str, List[str]]]
    IsEnd: NotRequired[bool]
    NextStep: NotRequired[str]
    IsCritical: NotRequired[bool]
    ValidNextSteps: NotRequired[List[str]]
    Targets: NotRequired[List[TargetOutputTypeDef]]
    TargetLocation: NotRequired[TargetLocationOutputTypeDef]
    TriggeredAlarms: NotRequired[List[AlarmStateInformationTypeDef]]
    ParentStepDetails: NotRequired[ParentStepDetailsTypeDef]


class TargetLocationTypeDef(TypedDict):
    Accounts: NotRequired[Sequence[str]]
    Regions: NotRequired[Sequence[str]]
    TargetLocationMaxConcurrency: NotRequired[str]
    TargetLocationMaxErrors: NotRequired[str]
    ExecutionRoleName: NotRequired[str]
    TargetLocationAlarmConfiguration: NotRequired[AlarmConfigurationUnionTypeDef]
    IncludeChildOrganizationUnits: NotRequired[bool]
    ExcludeAccounts: NotRequired[Sequence[str]]
    Targets: NotRequired[Sequence[TargetUnionTypeDef]]
    TargetsMaxConcurrency: NotRequired[str]
    TargetsMaxErrors: NotRequired[str]


class GetExecutionPreviewResponseTypeDef(TypedDict):
    ExecutionPreviewId: str
    EndedAt: datetime
    Status: ExecutionPreviewStatusType
    StatusMessage: str
    ExecutionPreview: ExecutionPreviewTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetMaintenanceWindowTaskResultTypeDef(TypedDict):
    WindowId: str
    WindowTaskId: str
    Targets: List[TargetOutputTypeDef]
    TaskArn: str
    ServiceRoleArn: str
    TaskType: MaintenanceWindowTaskTypeType
    TaskParameters: Dict[str, MaintenanceWindowTaskParameterValueExpressionOutputTypeDef]
    TaskInvocationParameters: MaintenanceWindowTaskInvocationParametersOutputTypeDef
    Priority: int
    MaxConcurrency: str
    MaxErrors: str
    LoggingInfo: LoggingInfoTypeDef
    Name: str
    Description: str
    CutoffBehavior: MaintenanceWindowTaskCutoffBehaviorType
    AlarmConfiguration: AlarmConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMaintenanceWindowTaskResultTypeDef(TypedDict):
    WindowId: str
    WindowTaskId: str
    Targets: List[TargetOutputTypeDef]
    TaskArn: str
    ServiceRoleArn: str
    TaskParameters: Dict[str, MaintenanceWindowTaskParameterValueExpressionOutputTypeDef]
    TaskInvocationParameters: MaintenanceWindowTaskInvocationParametersOutputTypeDef
    Priority: int
    MaxConcurrency: str
    MaxErrors: str
    LoggingInfo: LoggingInfoTypeDef
    Name: str
    Description: str
    CutoffBehavior: MaintenanceWindowTaskCutoffBehaviorType
    AlarmConfiguration: AlarmConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListComplianceSummariesResultTypeDef(TypedDict):
    ComplianceSummaryItems: List[ComplianceSummaryItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListResourceComplianceSummariesResultTypeDef(TypedDict):
    ResourceComplianceSummaryItems: List[ResourceComplianceSummaryItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDocumentMetadataHistoryResponseTypeDef(TypedDict):
    Name: str
    DocumentVersion: str
    Author: str
    Metadata: DocumentMetadataResponseInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetInventoryRequestGetInventoryPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[InventoryFilterTypeDef]]
    Aggregators: NotRequired[Sequence[InventoryAggregatorPaginatorTypeDef]]
    ResultAttributes: NotRequired[Sequence[ResultAttributeTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetInventoryRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[InventoryFilterTypeDef]]
    Aggregators: NotRequired[Sequence[InventoryAggregatorTypeDef]]
    ResultAttributes: NotRequired[Sequence[ResultAttributeTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeInstanceAssociationsStatusResultTypeDef(TypedDict):
    InstanceAssociationStatusInfos: List[InstanceAssociationStatusInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListNodesResultTypeDef(TypedDict):
    Nodes: List[NodeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeInventoryDeletionsResultTypeDef(TypedDict):
    InventoryDeletions: List[InventoryDeletionStatusItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


MaintenanceWindowRunCommandParametersUnionTypeDef = Union[
    MaintenanceWindowRunCommandParametersTypeDef, MaintenanceWindowRunCommandParametersOutputTypeDef
]


class PatchRuleGroupOutputTypeDef(TypedDict):
    PatchRules: List[PatchRuleOutputTypeDef]


PatchFilterGroupUnionTypeDef = Union[PatchFilterGroupTypeDef, PatchFilterGroupOutputTypeDef]


class ResourceDataSyncItemTypeDef(TypedDict):
    SyncName: NotRequired[str]
    SyncType: NotRequired[str]
    SyncSource: NotRequired[ResourceDataSyncSourceWithStateTypeDef]
    S3Destination: NotRequired[ResourceDataSyncS3DestinationTypeDef]
    LastSyncTime: NotRequired[datetime]
    LastSuccessfulSyncTime: NotRequired[datetime]
    SyncLastModifiedTime: NotRequired[datetime]
    LastStatus: NotRequired[LastResourceDataSyncStatusType]
    SyncCreatedTime: NotRequired[datetime]
    LastSyncStatusMessage: NotRequired[str]


class ResourceDataSyncSourceTypeDef(TypedDict):
    SourceType: str
    SourceRegions: Sequence[str]
    AwsOrganizationsSource: NotRequired[ResourceDataSyncAwsOrganizationsSourceUnionTypeDef]
    IncludeFutureRegions: NotRequired[bool]
    EnableAllOpsDataSources: NotRequired[bool]


class CreateAssociationResultTypeDef(TypedDict):
    AssociationDescription: AssociationDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAssociationResultTypeDef(TypedDict):
    AssociationDescription: AssociationDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAssociationResultTypeDef(TypedDict):
    AssociationDescription: AssociationDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAssociationStatusResultTypeDef(TypedDict):
    AssociationDescription: AssociationDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAssociationVersionsResultTypeDef(TypedDict):
    AssociationVersions: List[AssociationVersionInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class FailedCreateAssociationTypeDef(TypedDict):
    Entry: NotRequired[CreateAssociationBatchRequestEntryOutputTypeDef]
    Message: NotRequired[str]
    Fault: NotRequired[FaultType]


class AutomationExecutionMetadataTypeDef(TypedDict):
    AutomationExecutionId: NotRequired[str]
    DocumentName: NotRequired[str]
    DocumentVersion: NotRequired[str]
    AutomationExecutionStatus: NotRequired[AutomationExecutionStatusType]
    ExecutionStartTime: NotRequired[datetime]
    ExecutionEndTime: NotRequired[datetime]
    ExecutedBy: NotRequired[str]
    LogFile: NotRequired[str]
    Outputs: NotRequired[Dict[str, List[str]]]
    Mode: NotRequired[ExecutionModeType]
    ParentAutomationExecutionId: NotRequired[str]
    CurrentStepName: NotRequired[str]
    CurrentAction: NotRequired[str]
    FailureMessage: NotRequired[str]
    TargetParameterName: NotRequired[str]
    Targets: NotRequired[List[TargetOutputTypeDef]]
    TargetMaps: NotRequired[List[Dict[str, List[str]]]]
    ResolvedTargets: NotRequired[ResolvedTargetsTypeDef]
    MaxConcurrency: NotRequired[str]
    MaxErrors: NotRequired[str]
    Target: NotRequired[str]
    AutomationType: NotRequired[AutomationTypeType]
    AlarmConfiguration: NotRequired[AlarmConfigurationOutputTypeDef]
    TriggeredAlarms: NotRequired[List[AlarmStateInformationTypeDef]]
    TargetLocationsURL: NotRequired[str]
    AutomationSubtype: NotRequired[Literal["ChangeRequest"]]
    ScheduledTime: NotRequired[datetime]
    Runbooks: NotRequired[List[RunbookOutputTypeDef]]
    OpsItemId: NotRequired[str]
    AssociationId: NotRequired[str]
    ChangeRequestName: NotRequired[str]


class AutomationExecutionTypeDef(TypedDict):
    AutomationExecutionId: NotRequired[str]
    DocumentName: NotRequired[str]
    DocumentVersion: NotRequired[str]
    ExecutionStartTime: NotRequired[datetime]
    ExecutionEndTime: NotRequired[datetime]
    AutomationExecutionStatus: NotRequired[AutomationExecutionStatusType]
    StepExecutions: NotRequired[List[StepExecutionTypeDef]]
    StepExecutionsTruncated: NotRequired[bool]
    Parameters: NotRequired[Dict[str, List[str]]]
    Outputs: NotRequired[Dict[str, List[str]]]
    FailureMessage: NotRequired[str]
    Mode: NotRequired[ExecutionModeType]
    ParentAutomationExecutionId: NotRequired[str]
    ExecutedBy: NotRequired[str]
    CurrentStepName: NotRequired[str]
    CurrentAction: NotRequired[str]
    TargetParameterName: NotRequired[str]
    Targets: NotRequired[List[TargetOutputTypeDef]]
    TargetMaps: NotRequired[List[Dict[str, List[str]]]]
    ResolvedTargets: NotRequired[ResolvedTargetsTypeDef]
    MaxConcurrency: NotRequired[str]
    MaxErrors: NotRequired[str]
    Target: NotRequired[str]
    TargetLocations: NotRequired[List[TargetLocationOutputTypeDef]]
    ProgressCounters: NotRequired[ProgressCountersTypeDef]
    AlarmConfiguration: NotRequired[AlarmConfigurationOutputTypeDef]
    TriggeredAlarms: NotRequired[List[AlarmStateInformationTypeDef]]
    TargetLocationsURL: NotRequired[str]
    AutomationSubtype: NotRequired[Literal["ChangeRequest"]]
    ScheduledTime: NotRequired[datetime]
    Runbooks: NotRequired[List[RunbookOutputTypeDef]]
    OpsItemId: NotRequired[str]
    AssociationId: NotRequired[str]
    ChangeRequestName: NotRequired[str]
    Variables: NotRequired[Dict[str, List[str]]]


class DescribeAutomationStepExecutionsResultTypeDef(TypedDict):
    StepExecutions: List[StepExecutionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartAutomationExecutionRequestRequestTypeDef(TypedDict):
    DocumentName: str
    DocumentVersion: NotRequired[str]
    Parameters: NotRequired[Mapping[str, Sequence[str]]]
    ClientToken: NotRequired[str]
    Mode: NotRequired[ExecutionModeType]
    TargetParameterName: NotRequired[str]
    Targets: NotRequired[Sequence[TargetTypeDef]]
    TargetMaps: NotRequired[Sequence[Mapping[str, Sequence[str]]]]
    MaxConcurrency: NotRequired[str]
    MaxErrors: NotRequired[str]
    TargetLocations: NotRequired[Sequence[TargetLocationTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    AlarmConfiguration: NotRequired[AlarmConfigurationTypeDef]
    TargetLocationsURL: NotRequired[str]


TargetLocationUnionTypeDef = Union[TargetLocationTypeDef, TargetLocationOutputTypeDef]


class UpdateAssociationRequestRequestTypeDef(TypedDict):
    AssociationId: str
    Parameters: NotRequired[Mapping[str, Sequence[str]]]
    DocumentVersion: NotRequired[str]
    ScheduleExpression: NotRequired[str]
    OutputLocation: NotRequired[InstanceAssociationOutputLocationTypeDef]
    Name: NotRequired[str]
    Targets: NotRequired[Sequence[TargetTypeDef]]
    AssociationName: NotRequired[str]
    AssociationVersion: NotRequired[str]
    AutomationTargetParameterName: NotRequired[str]
    MaxErrors: NotRequired[str]
    MaxConcurrency: NotRequired[str]
    ComplianceSeverity: NotRequired[AssociationComplianceSeverityType]
    SyncCompliance: NotRequired[AssociationSyncComplianceType]
    ApplyOnlyAtCronInterval: NotRequired[bool]
    CalendarNames: NotRequired[Sequence[str]]
    TargetLocations: NotRequired[Sequence[TargetLocationTypeDef]]
    ScheduleOffset: NotRequired[int]
    Duration: NotRequired[int]
    TargetMaps: NotRequired[Sequence[Mapping[str, Sequence[str]]]]
    AlarmConfiguration: NotRequired[AlarmConfigurationTypeDef]


class MaintenanceWindowTaskInvocationParametersTypeDef(TypedDict):
    RunCommand: NotRequired[MaintenanceWindowRunCommandParametersUnionTypeDef]
    Automation: NotRequired[MaintenanceWindowAutomationParametersUnionTypeDef]
    StepFunctions: NotRequired[MaintenanceWindowStepFunctionsParametersTypeDef]
    Lambda: NotRequired[MaintenanceWindowLambdaParametersUnionTypeDef]


class GetPatchBaselineResultTypeDef(TypedDict):
    BaselineId: str
    Name: str
    OperatingSystem: OperatingSystemType
    GlobalFilters: PatchFilterGroupOutputTypeDef
    ApprovalRules: PatchRuleGroupOutputTypeDef
    ApprovedPatches: List[str]
    ApprovedPatchesComplianceLevel: PatchComplianceLevelType
    ApprovedPatchesEnableNonSecurity: bool
    RejectedPatches: List[str]
    RejectedPatchesAction: PatchActionType
    PatchGroups: List[str]
    CreatedDate: datetime
    ModifiedDate: datetime
    Description: str
    Sources: List[PatchSourceOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePatchBaselineResultTypeDef(TypedDict):
    BaselineId: str
    Name: str
    OperatingSystem: OperatingSystemType
    GlobalFilters: PatchFilterGroupOutputTypeDef
    ApprovalRules: PatchRuleGroupOutputTypeDef
    ApprovedPatches: List[str]
    ApprovedPatchesComplianceLevel: PatchComplianceLevelType
    ApprovedPatchesEnableNonSecurity: bool
    RejectedPatches: List[str]
    RejectedPatchesAction: PatchActionType
    CreatedDate: datetime
    ModifiedDate: datetime
    Description: str
    Sources: List[PatchSourceOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PatchRuleTypeDef(TypedDict):
    PatchFilterGroup: PatchFilterGroupUnionTypeDef
    ComplianceLevel: NotRequired[PatchComplianceLevelType]
    ApproveAfterDays: NotRequired[int]
    ApproveUntilDate: NotRequired[str]
    EnableNonSecurity: NotRequired[bool]


class ListResourceDataSyncResultTypeDef(TypedDict):
    ResourceDataSyncItems: List[ResourceDataSyncItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateResourceDataSyncRequestRequestTypeDef(TypedDict):
    SyncName: str
    S3Destination: NotRequired[ResourceDataSyncS3DestinationTypeDef]
    SyncType: NotRequired[str]
    SyncSource: NotRequired[ResourceDataSyncSourceTypeDef]


class UpdateResourceDataSyncRequestRequestTypeDef(TypedDict):
    SyncName: str
    SyncType: str
    SyncSource: ResourceDataSyncSourceTypeDef


class CreateAssociationBatchResultTypeDef(TypedDict):
    Successful: List[AssociationDescriptionTypeDef]
    Failed: List[FailedCreateAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAutomationExecutionsResultTypeDef(TypedDict):
    AutomationExecutionMetadataList: List[AutomationExecutionMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetAutomationExecutionResultTypeDef(TypedDict):
    AutomationExecution: AutomationExecutionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AutomationExecutionInputsTypeDef(TypedDict):
    Parameters: NotRequired[Mapping[str, Sequence[str]]]
    TargetParameterName: NotRequired[str]
    Targets: NotRequired[Sequence[TargetUnionTypeDef]]
    TargetMaps: NotRequired[Sequence[Mapping[str, Sequence[str]]]]
    TargetLocations: NotRequired[Sequence[TargetLocationUnionTypeDef]]
    TargetLocationsURL: NotRequired[str]


class CreateAssociationBatchRequestEntryTypeDef(TypedDict):
    Name: str
    InstanceId: NotRequired[str]
    Parameters: NotRequired[Mapping[str, Sequence[str]]]
    AutomationTargetParameterName: NotRequired[str]
    DocumentVersion: NotRequired[str]
    Targets: NotRequired[Sequence[TargetUnionTypeDef]]
    ScheduleExpression: NotRequired[str]
    OutputLocation: NotRequired[InstanceAssociationOutputLocationTypeDef]
    AssociationName: NotRequired[str]
    MaxErrors: NotRequired[str]
    MaxConcurrency: NotRequired[str]
    ComplianceSeverity: NotRequired[AssociationComplianceSeverityType]
    SyncCompliance: NotRequired[AssociationSyncComplianceType]
    ApplyOnlyAtCronInterval: NotRequired[bool]
    CalendarNames: NotRequired[Sequence[str]]
    TargetLocations: NotRequired[Sequence[TargetLocationUnionTypeDef]]
    ScheduleOffset: NotRequired[int]
    Duration: NotRequired[int]
    TargetMaps: NotRequired[Sequence[Mapping[str, Sequence[str]]]]
    AlarmConfiguration: NotRequired[AlarmConfigurationUnionTypeDef]


class CreateAssociationRequestRequestTypeDef(TypedDict):
    Name: str
    DocumentVersion: NotRequired[str]
    InstanceId: NotRequired[str]
    Parameters: NotRequired[Mapping[str, Sequence[str]]]
    Targets: NotRequired[Sequence[TargetUnionTypeDef]]
    ScheduleExpression: NotRequired[str]
    OutputLocation: NotRequired[InstanceAssociationOutputLocationTypeDef]
    AssociationName: NotRequired[str]
    AutomationTargetParameterName: NotRequired[str]
    MaxErrors: NotRequired[str]
    MaxConcurrency: NotRequired[str]
    ComplianceSeverity: NotRequired[AssociationComplianceSeverityType]
    SyncCompliance: NotRequired[AssociationSyncComplianceType]
    ApplyOnlyAtCronInterval: NotRequired[bool]
    CalendarNames: NotRequired[Sequence[str]]
    TargetLocations: NotRequired[Sequence[TargetLocationUnionTypeDef]]
    ScheduleOffset: NotRequired[int]
    Duration: NotRequired[int]
    TargetMaps: NotRequired[Sequence[Mapping[str, Sequence[str]]]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    AlarmConfiguration: NotRequired[AlarmConfigurationTypeDef]


class RunbookTypeDef(TypedDict):
    DocumentName: str
    DocumentVersion: NotRequired[str]
    Parameters: NotRequired[Mapping[str, Sequence[str]]]
    TargetParameterName: NotRequired[str]
    Targets: NotRequired[Sequence[TargetUnionTypeDef]]
    TargetMaps: NotRequired[Sequence[Mapping[str, Sequence[str]]]]
    MaxConcurrency: NotRequired[str]
    MaxErrors: NotRequired[str]
    TargetLocations: NotRequired[Sequence[TargetLocationUnionTypeDef]]


class RegisterTaskWithMaintenanceWindowRequestRequestTypeDef(TypedDict):
    WindowId: str
    TaskArn: str
    TaskType: MaintenanceWindowTaskTypeType
    Targets: NotRequired[Sequence[TargetTypeDef]]
    ServiceRoleArn: NotRequired[str]
    TaskParameters: NotRequired[
        Mapping[str, MaintenanceWindowTaskParameterValueExpressionUnionTypeDef]
    ]
    TaskInvocationParameters: NotRequired[MaintenanceWindowTaskInvocationParametersTypeDef]
    Priority: NotRequired[int]
    MaxConcurrency: NotRequired[str]
    MaxErrors: NotRequired[str]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]
    Name: NotRequired[str]
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
    CutoffBehavior: NotRequired[MaintenanceWindowTaskCutoffBehaviorType]
    AlarmConfiguration: NotRequired[AlarmConfigurationTypeDef]


class UpdateMaintenanceWindowTaskRequestRequestTypeDef(TypedDict):
    WindowId: str
    WindowTaskId: str
    Targets: NotRequired[Sequence[TargetTypeDef]]
    TaskArn: NotRequired[str]
    ServiceRoleArn: NotRequired[str]
    TaskParameters: NotRequired[Mapping[str, MaintenanceWindowTaskParameterValueExpressionTypeDef]]
    TaskInvocationParameters: NotRequired[MaintenanceWindowTaskInvocationParametersTypeDef]
    Priority: NotRequired[int]
    MaxConcurrency: NotRequired[str]
    MaxErrors: NotRequired[str]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Replace: NotRequired[bool]
    CutoffBehavior: NotRequired[MaintenanceWindowTaskCutoffBehaviorType]
    AlarmConfiguration: NotRequired[AlarmConfigurationTypeDef]


PatchRuleUnionTypeDef = Union[PatchRuleTypeDef, PatchRuleOutputTypeDef]


class ExecutionInputsTypeDef(TypedDict):
    Automation: NotRequired[AutomationExecutionInputsTypeDef]


CreateAssociationBatchRequestEntryUnionTypeDef = Union[
    CreateAssociationBatchRequestEntryTypeDef, CreateAssociationBatchRequestEntryOutputTypeDef
]
RunbookUnionTypeDef = Union[RunbookTypeDef, RunbookOutputTypeDef]


class PatchRuleGroupTypeDef(TypedDict):
    PatchRules: Sequence[PatchRuleUnionTypeDef]


class StartExecutionPreviewRequestRequestTypeDef(TypedDict):
    DocumentName: str
    DocumentVersion: NotRequired[str]
    ExecutionInputs: NotRequired[ExecutionInputsTypeDef]


class CreateAssociationBatchRequestRequestTypeDef(TypedDict):
    Entries: Sequence[CreateAssociationBatchRequestEntryUnionTypeDef]


class StartChangeRequestExecutionRequestRequestTypeDef(TypedDict):
    DocumentName: str
    Runbooks: Sequence[RunbookUnionTypeDef]
    ScheduledTime: NotRequired[TimestampTypeDef]
    DocumentVersion: NotRequired[str]
    Parameters: NotRequired[Mapping[str, Sequence[str]]]
    ChangeRequestName: NotRequired[str]
    ClientToken: NotRequired[str]
    AutoApprove: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ScheduledEndTime: NotRequired[TimestampTypeDef]
    ChangeDetails: NotRequired[str]


class CreatePatchBaselineRequestRequestTypeDef(TypedDict):
    Name: str
    OperatingSystem: NotRequired[OperatingSystemType]
    GlobalFilters: NotRequired[PatchFilterGroupTypeDef]
    ApprovalRules: NotRequired[PatchRuleGroupTypeDef]
    ApprovedPatches: NotRequired[Sequence[str]]
    ApprovedPatchesComplianceLevel: NotRequired[PatchComplianceLevelType]
    ApprovedPatchesEnableNonSecurity: NotRequired[bool]
    RejectedPatches: NotRequired[Sequence[str]]
    RejectedPatchesAction: NotRequired[PatchActionType]
    Description: NotRequired[str]
    Sources: NotRequired[Sequence[PatchSourceUnionTypeDef]]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


PatchRuleGroupUnionTypeDef = Union[PatchRuleGroupTypeDef, PatchRuleGroupOutputTypeDef]


class UpdatePatchBaselineRequestRequestTypeDef(TypedDict):
    BaselineId: str
    Name: NotRequired[str]
    GlobalFilters: NotRequired[PatchFilterGroupTypeDef]
    ApprovalRules: NotRequired[PatchRuleGroupTypeDef]
    ApprovedPatches: NotRequired[Sequence[str]]
    ApprovedPatchesComplianceLevel: NotRequired[PatchComplianceLevelType]
    ApprovedPatchesEnableNonSecurity: NotRequired[bool]
    RejectedPatches: NotRequired[Sequence[str]]
    RejectedPatchesAction: NotRequired[PatchActionType]
    Description: NotRequired[str]
    Sources: NotRequired[Sequence[PatchSourceTypeDef]]
    Replace: NotRequired[bool]


class BaselineOverrideTypeDef(TypedDict):
    OperatingSystem: NotRequired[OperatingSystemType]
    GlobalFilters: NotRequired[PatchFilterGroupUnionTypeDef]
    ApprovalRules: NotRequired[PatchRuleGroupUnionTypeDef]
    ApprovedPatches: NotRequired[Sequence[str]]
    ApprovedPatchesComplianceLevel: NotRequired[PatchComplianceLevelType]
    RejectedPatches: NotRequired[Sequence[str]]
    RejectedPatchesAction: NotRequired[PatchActionType]
    ApprovedPatchesEnableNonSecurity: NotRequired[bool]
    Sources: NotRequired[Sequence[PatchSourceUnionTypeDef]]


class GetDeployablePatchSnapshotForInstanceRequestRequestTypeDef(TypedDict):
    InstanceId: str
    SnapshotId: str
    BaselineOverride: NotRequired[BaselineOverrideTypeDef]
