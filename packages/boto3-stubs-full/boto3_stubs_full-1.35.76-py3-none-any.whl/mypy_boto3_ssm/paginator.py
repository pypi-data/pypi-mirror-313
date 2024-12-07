"""
Type annotations for ssm service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ssm.client import SSMClient
    from mypy_boto3_ssm.paginator import (
        DescribeActivationsPaginator,
        DescribeAssociationExecutionTargetsPaginator,
        DescribeAssociationExecutionsPaginator,
        DescribeAutomationExecutionsPaginator,
        DescribeAutomationStepExecutionsPaginator,
        DescribeAvailablePatchesPaginator,
        DescribeEffectiveInstanceAssociationsPaginator,
        DescribeEffectivePatchesForPatchBaselinePaginator,
        DescribeInstanceAssociationsStatusPaginator,
        DescribeInstanceInformationPaginator,
        DescribeInstancePatchStatesForPatchGroupPaginator,
        DescribeInstancePatchStatesPaginator,
        DescribeInstancePatchesPaginator,
        DescribeInstancePropertiesPaginator,
        DescribeInventoryDeletionsPaginator,
        DescribeMaintenanceWindowExecutionTaskInvocationsPaginator,
        DescribeMaintenanceWindowExecutionTasksPaginator,
        DescribeMaintenanceWindowExecutionsPaginator,
        DescribeMaintenanceWindowSchedulePaginator,
        DescribeMaintenanceWindowTargetsPaginator,
        DescribeMaintenanceWindowTasksPaginator,
        DescribeMaintenanceWindowsForTargetPaginator,
        DescribeMaintenanceWindowsPaginator,
        DescribeOpsItemsPaginator,
        DescribeParametersPaginator,
        DescribePatchBaselinesPaginator,
        DescribePatchGroupsPaginator,
        DescribePatchPropertiesPaginator,
        DescribeSessionsPaginator,
        GetInventoryPaginator,
        GetInventorySchemaPaginator,
        GetOpsSummaryPaginator,
        GetParameterHistoryPaginator,
        GetParametersByPathPaginator,
        GetResourcePoliciesPaginator,
        ListAssociationVersionsPaginator,
        ListAssociationsPaginator,
        ListCommandInvocationsPaginator,
        ListCommandsPaginator,
        ListComplianceItemsPaginator,
        ListComplianceSummariesPaginator,
        ListDocumentVersionsPaginator,
        ListDocumentsPaginator,
        ListNodesPaginator,
        ListNodesSummaryPaginator,
        ListOpsItemEventsPaginator,
        ListOpsItemRelatedItemsPaginator,
        ListOpsMetadataPaginator,
        ListResourceComplianceSummariesPaginator,
        ListResourceDataSyncPaginator,
    )

    session = Session()
    client: SSMClient = session.client("ssm")

    describe_activations_paginator: DescribeActivationsPaginator = client.get_paginator("describe_activations")
    describe_association_execution_targets_paginator: DescribeAssociationExecutionTargetsPaginator = client.get_paginator("describe_association_execution_targets")
    describe_association_executions_paginator: DescribeAssociationExecutionsPaginator = client.get_paginator("describe_association_executions")
    describe_automation_executions_paginator: DescribeAutomationExecutionsPaginator = client.get_paginator("describe_automation_executions")
    describe_automation_step_executions_paginator: DescribeAutomationStepExecutionsPaginator = client.get_paginator("describe_automation_step_executions")
    describe_available_patches_paginator: DescribeAvailablePatchesPaginator = client.get_paginator("describe_available_patches")
    describe_effective_instance_associations_paginator: DescribeEffectiveInstanceAssociationsPaginator = client.get_paginator("describe_effective_instance_associations")
    describe_effective_patches_for_patch_baseline_paginator: DescribeEffectivePatchesForPatchBaselinePaginator = client.get_paginator("describe_effective_patches_for_patch_baseline")
    describe_instance_associations_status_paginator: DescribeInstanceAssociationsStatusPaginator = client.get_paginator("describe_instance_associations_status")
    describe_instance_information_paginator: DescribeInstanceInformationPaginator = client.get_paginator("describe_instance_information")
    describe_instance_patch_states_for_patch_group_paginator: DescribeInstancePatchStatesForPatchGroupPaginator = client.get_paginator("describe_instance_patch_states_for_patch_group")
    describe_instance_patch_states_paginator: DescribeInstancePatchStatesPaginator = client.get_paginator("describe_instance_patch_states")
    describe_instance_patches_paginator: DescribeInstancePatchesPaginator = client.get_paginator("describe_instance_patches")
    describe_instance_properties_paginator: DescribeInstancePropertiesPaginator = client.get_paginator("describe_instance_properties")
    describe_inventory_deletions_paginator: DescribeInventoryDeletionsPaginator = client.get_paginator("describe_inventory_deletions")
    describe_maintenance_window_execution_task_invocations_paginator: DescribeMaintenanceWindowExecutionTaskInvocationsPaginator = client.get_paginator("describe_maintenance_window_execution_task_invocations")
    describe_maintenance_window_execution_tasks_paginator: DescribeMaintenanceWindowExecutionTasksPaginator = client.get_paginator("describe_maintenance_window_execution_tasks")
    describe_maintenance_window_executions_paginator: DescribeMaintenanceWindowExecutionsPaginator = client.get_paginator("describe_maintenance_window_executions")
    describe_maintenance_window_schedule_paginator: DescribeMaintenanceWindowSchedulePaginator = client.get_paginator("describe_maintenance_window_schedule")
    describe_maintenance_window_targets_paginator: DescribeMaintenanceWindowTargetsPaginator = client.get_paginator("describe_maintenance_window_targets")
    describe_maintenance_window_tasks_paginator: DescribeMaintenanceWindowTasksPaginator = client.get_paginator("describe_maintenance_window_tasks")
    describe_maintenance_windows_for_target_paginator: DescribeMaintenanceWindowsForTargetPaginator = client.get_paginator("describe_maintenance_windows_for_target")
    describe_maintenance_windows_paginator: DescribeMaintenanceWindowsPaginator = client.get_paginator("describe_maintenance_windows")
    describe_ops_items_paginator: DescribeOpsItemsPaginator = client.get_paginator("describe_ops_items")
    describe_parameters_paginator: DescribeParametersPaginator = client.get_paginator("describe_parameters")
    describe_patch_baselines_paginator: DescribePatchBaselinesPaginator = client.get_paginator("describe_patch_baselines")
    describe_patch_groups_paginator: DescribePatchGroupsPaginator = client.get_paginator("describe_patch_groups")
    describe_patch_properties_paginator: DescribePatchPropertiesPaginator = client.get_paginator("describe_patch_properties")
    describe_sessions_paginator: DescribeSessionsPaginator = client.get_paginator("describe_sessions")
    get_inventory_paginator: GetInventoryPaginator = client.get_paginator("get_inventory")
    get_inventory_schema_paginator: GetInventorySchemaPaginator = client.get_paginator("get_inventory_schema")
    get_ops_summary_paginator: GetOpsSummaryPaginator = client.get_paginator("get_ops_summary")
    get_parameter_history_paginator: GetParameterHistoryPaginator = client.get_paginator("get_parameter_history")
    get_parameters_by_path_paginator: GetParametersByPathPaginator = client.get_paginator("get_parameters_by_path")
    get_resource_policies_paginator: GetResourcePoliciesPaginator = client.get_paginator("get_resource_policies")
    list_association_versions_paginator: ListAssociationVersionsPaginator = client.get_paginator("list_association_versions")
    list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
    list_command_invocations_paginator: ListCommandInvocationsPaginator = client.get_paginator("list_command_invocations")
    list_commands_paginator: ListCommandsPaginator = client.get_paginator("list_commands")
    list_compliance_items_paginator: ListComplianceItemsPaginator = client.get_paginator("list_compliance_items")
    list_compliance_summaries_paginator: ListComplianceSummariesPaginator = client.get_paginator("list_compliance_summaries")
    list_document_versions_paginator: ListDocumentVersionsPaginator = client.get_paginator("list_document_versions")
    list_documents_paginator: ListDocumentsPaginator = client.get_paginator("list_documents")
    list_nodes_paginator: ListNodesPaginator = client.get_paginator("list_nodes")
    list_nodes_summary_paginator: ListNodesSummaryPaginator = client.get_paginator("list_nodes_summary")
    list_ops_item_events_paginator: ListOpsItemEventsPaginator = client.get_paginator("list_ops_item_events")
    list_ops_item_related_items_paginator: ListOpsItemRelatedItemsPaginator = client.get_paginator("list_ops_item_related_items")
    list_ops_metadata_paginator: ListOpsMetadataPaginator = client.get_paginator("list_ops_metadata")
    list_resource_compliance_summaries_paginator: ListResourceComplianceSummariesPaginator = client.get_paginator("list_resource_compliance_summaries")
    list_resource_data_sync_paginator: ListResourceDataSyncPaginator = client.get_paginator("list_resource_data_sync")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeActivationsRequestDescribeActivationsPaginateTypeDef,
    DescribeActivationsResultTypeDef,
    DescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef,
    DescribeAssociationExecutionsResultTypeDef,
    DescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef,
    DescribeAssociationExecutionTargetsResultTypeDef,
    DescribeAutomationExecutionsRequestDescribeAutomationExecutionsPaginateTypeDef,
    DescribeAutomationExecutionsResultTypeDef,
    DescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef,
    DescribeAutomationStepExecutionsResultTypeDef,
    DescribeAvailablePatchesRequestDescribeAvailablePatchesPaginateTypeDef,
    DescribeAvailablePatchesResultTypeDef,
    DescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef,
    DescribeEffectiveInstanceAssociationsResultTypeDef,
    DescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef,
    DescribeEffectivePatchesForPatchBaselineResultTypeDef,
    DescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef,
    DescribeInstanceAssociationsStatusResultTypeDef,
    DescribeInstanceInformationRequestDescribeInstanceInformationPaginateTypeDef,
    DescribeInstanceInformationResultTypeDef,
    DescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef,
    DescribeInstancePatchesResultTypeDef,
    DescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef,
    DescribeInstancePatchStatesForPatchGroupResultTypeDef,
    DescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef,
    DescribeInstancePatchStatesResultTypeDef,
    DescribeInstancePropertiesRequestDescribeInstancePropertiesPaginateTypeDef,
    DescribeInstancePropertiesResultTypeDef,
    DescribeInventoryDeletionsRequestDescribeInventoryDeletionsPaginateTypeDef,
    DescribeInventoryDeletionsResultTypeDef,
    DescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef,
    DescribeMaintenanceWindowExecutionsResultTypeDef,
    DescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef,
    DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef,
    DescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef,
    DescribeMaintenanceWindowExecutionTasksResultTypeDef,
    DescribeMaintenanceWindowScheduleRequestDescribeMaintenanceWindowSchedulePaginateTypeDef,
    DescribeMaintenanceWindowScheduleResultTypeDef,
    DescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef,
    DescribeMaintenanceWindowsForTargetResultTypeDef,
    DescribeMaintenanceWindowsRequestDescribeMaintenanceWindowsPaginateTypeDef,
    DescribeMaintenanceWindowsResultTypeDef,
    DescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef,
    DescribeMaintenanceWindowTargetsResultTypeDef,
    DescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef,
    DescribeMaintenanceWindowTasksResultTypeDef,
    DescribeOpsItemsRequestDescribeOpsItemsPaginateTypeDef,
    DescribeOpsItemsResponseTypeDef,
    DescribeParametersRequestDescribeParametersPaginateTypeDef,
    DescribeParametersResultTypeDef,
    DescribePatchBaselinesRequestDescribePatchBaselinesPaginateTypeDef,
    DescribePatchBaselinesResultTypeDef,
    DescribePatchGroupsRequestDescribePatchGroupsPaginateTypeDef,
    DescribePatchGroupsResultTypeDef,
    DescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef,
    DescribePatchPropertiesResultTypeDef,
    DescribeSessionsRequestDescribeSessionsPaginateTypeDef,
    DescribeSessionsResponseTypeDef,
    GetInventoryRequestGetInventoryPaginateTypeDef,
    GetInventoryResultTypeDef,
    GetInventorySchemaRequestGetInventorySchemaPaginateTypeDef,
    GetInventorySchemaResultTypeDef,
    GetOpsSummaryRequestGetOpsSummaryPaginateTypeDef,
    GetOpsSummaryResultTypeDef,
    GetParameterHistoryRequestGetParameterHistoryPaginateTypeDef,
    GetParameterHistoryResultTypeDef,
    GetParametersByPathRequestGetParametersByPathPaginateTypeDef,
    GetParametersByPathResultTypeDef,
    GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef,
    GetResourcePoliciesResponseTypeDef,
    ListAssociationsRequestListAssociationsPaginateTypeDef,
    ListAssociationsResultTypeDef,
    ListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef,
    ListAssociationVersionsResultTypeDef,
    ListCommandInvocationsRequestListCommandInvocationsPaginateTypeDef,
    ListCommandInvocationsResultTypeDef,
    ListCommandsRequestListCommandsPaginateTypeDef,
    ListCommandsResultTypeDef,
    ListComplianceItemsRequestListComplianceItemsPaginateTypeDef,
    ListComplianceItemsResultTypeDef,
    ListComplianceSummariesRequestListComplianceSummariesPaginateTypeDef,
    ListComplianceSummariesResultTypeDef,
    ListDocumentsRequestListDocumentsPaginateTypeDef,
    ListDocumentsResultTypeDef,
    ListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef,
    ListDocumentVersionsResultTypeDef,
    ListNodesRequestListNodesPaginateTypeDef,
    ListNodesResultTypeDef,
    ListNodesSummaryRequestListNodesSummaryPaginateTypeDef,
    ListNodesSummaryResultTypeDef,
    ListOpsItemEventsRequestListOpsItemEventsPaginateTypeDef,
    ListOpsItemEventsResponseTypeDef,
    ListOpsItemRelatedItemsRequestListOpsItemRelatedItemsPaginateTypeDef,
    ListOpsItemRelatedItemsResponseTypeDef,
    ListOpsMetadataRequestListOpsMetadataPaginateTypeDef,
    ListOpsMetadataResultTypeDef,
    ListResourceComplianceSummariesRequestListResourceComplianceSummariesPaginateTypeDef,
    ListResourceComplianceSummariesResultTypeDef,
    ListResourceDataSyncRequestListResourceDataSyncPaginateTypeDef,
    ListResourceDataSyncResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeActivationsPaginator",
    "DescribeAssociationExecutionTargetsPaginator",
    "DescribeAssociationExecutionsPaginator",
    "DescribeAutomationExecutionsPaginator",
    "DescribeAutomationStepExecutionsPaginator",
    "DescribeAvailablePatchesPaginator",
    "DescribeEffectiveInstanceAssociationsPaginator",
    "DescribeEffectivePatchesForPatchBaselinePaginator",
    "DescribeInstanceAssociationsStatusPaginator",
    "DescribeInstanceInformationPaginator",
    "DescribeInstancePatchStatesForPatchGroupPaginator",
    "DescribeInstancePatchStatesPaginator",
    "DescribeInstancePatchesPaginator",
    "DescribeInstancePropertiesPaginator",
    "DescribeInventoryDeletionsPaginator",
    "DescribeMaintenanceWindowExecutionTaskInvocationsPaginator",
    "DescribeMaintenanceWindowExecutionTasksPaginator",
    "DescribeMaintenanceWindowExecutionsPaginator",
    "DescribeMaintenanceWindowSchedulePaginator",
    "DescribeMaintenanceWindowTargetsPaginator",
    "DescribeMaintenanceWindowTasksPaginator",
    "DescribeMaintenanceWindowsForTargetPaginator",
    "DescribeMaintenanceWindowsPaginator",
    "DescribeOpsItemsPaginator",
    "DescribeParametersPaginator",
    "DescribePatchBaselinesPaginator",
    "DescribePatchGroupsPaginator",
    "DescribePatchPropertiesPaginator",
    "DescribeSessionsPaginator",
    "GetInventoryPaginator",
    "GetInventorySchemaPaginator",
    "GetOpsSummaryPaginator",
    "GetParameterHistoryPaginator",
    "GetParametersByPathPaginator",
    "GetResourcePoliciesPaginator",
    "ListAssociationVersionsPaginator",
    "ListAssociationsPaginator",
    "ListCommandInvocationsPaginator",
    "ListCommandsPaginator",
    "ListComplianceItemsPaginator",
    "ListComplianceSummariesPaginator",
    "ListDocumentVersionsPaginator",
    "ListDocumentsPaginator",
    "ListNodesPaginator",
    "ListNodesSummaryPaginator",
    "ListOpsItemEventsPaginator",
    "ListOpsItemRelatedItemsPaginator",
    "ListOpsMetadataPaginator",
    "ListResourceComplianceSummariesPaginator",
    "ListResourceDataSyncPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeActivationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeActivations.html#SSM.Paginator.DescribeActivations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeactivationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeActivationsRequestDescribeActivationsPaginateTypeDef]
    ) -> _PageIterator[DescribeActivationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeActivations.html#SSM.Paginator.DescribeActivations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeactivationspaginator)
        """


class DescribeAssociationExecutionTargetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAssociationExecutionTargets.html#SSM.Paginator.DescribeAssociationExecutionTargets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeassociationexecutiontargetspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeAssociationExecutionTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAssociationExecutionTargets.html#SSM.Paginator.DescribeAssociationExecutionTargets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeassociationexecutiontargetspaginator)
        """


class DescribeAssociationExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAssociationExecutions.html#SSM.Paginator.DescribeAssociationExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeassociationexecutionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeAssociationExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAssociationExecutions.html#SSM.Paginator.DescribeAssociationExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeassociationexecutionspaginator)
        """


class DescribeAutomationExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAutomationExecutions.html#SSM.Paginator.DescribeAutomationExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeautomationexecutionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAutomationExecutionsRequestDescribeAutomationExecutionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeAutomationExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAutomationExecutions.html#SSM.Paginator.DescribeAutomationExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeautomationexecutionspaginator)
        """


class DescribeAutomationStepExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAutomationStepExecutions.html#SSM.Paginator.DescribeAutomationStepExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeautomationstepexecutionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeAutomationStepExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAutomationStepExecutions.html#SSM.Paginator.DescribeAutomationStepExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeautomationstepexecutionspaginator)
        """


class DescribeAvailablePatchesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAvailablePatches.html#SSM.Paginator.DescribeAvailablePatches)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeavailablepatchespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeAvailablePatchesRequestDescribeAvailablePatchesPaginateTypeDef],
    ) -> _PageIterator[DescribeAvailablePatchesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAvailablePatches.html#SSM.Paginator.DescribeAvailablePatches.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeavailablepatchespaginator)
        """


class DescribeEffectiveInstanceAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeEffectiveInstanceAssociations.html#SSM.Paginator.DescribeEffectiveInstanceAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeeffectiveinstanceassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeEffectiveInstanceAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeEffectiveInstanceAssociations.html#SSM.Paginator.DescribeEffectiveInstanceAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeeffectiveinstanceassociationspaginator)
        """


class DescribeEffectivePatchesForPatchBaselinePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeEffectivePatchesForPatchBaseline.html#SSM.Paginator.DescribeEffectivePatchesForPatchBaseline)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeeffectivepatchesforpatchbaselinepaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef
        ],
    ) -> _PageIterator[DescribeEffectivePatchesForPatchBaselineResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeEffectivePatchesForPatchBaseline.html#SSM.Paginator.DescribeEffectivePatchesForPatchBaseline.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeeffectivepatchesforpatchbaselinepaginator)
        """


class DescribeInstanceAssociationsStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceAssociationsStatus.html#SSM.Paginator.DescribeInstanceAssociationsStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstanceassociationsstatuspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeInstanceAssociationsStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceAssociationsStatus.html#SSM.Paginator.DescribeInstanceAssociationsStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstanceassociationsstatuspaginator)
        """


class DescribeInstanceInformationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceInformation.html#SSM.Paginator.DescribeInstanceInformation)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstanceinformationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstanceInformationRequestDescribeInstanceInformationPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeInstanceInformationResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceInformation.html#SSM.Paginator.DescribeInstanceInformation.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstanceinformationpaginator)
        """


class DescribeInstancePatchStatesForPatchGroupPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatchStatesForPatchGroup.html#SSM.Paginator.DescribeInstancePatchStatesForPatchGroup)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepatchstatesforpatchgrouppaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeInstancePatchStatesForPatchGroupResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatchStatesForPatchGroup.html#SSM.Paginator.DescribeInstancePatchStatesForPatchGroup.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepatchstatesforpatchgrouppaginator)
        """


class DescribeInstancePatchStatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatchStates.html#SSM.Paginator.DescribeInstancePatchStates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepatchstatespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeInstancePatchStatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatchStates.html#SSM.Paginator.DescribeInstancePatchStates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepatchstatespaginator)
        """


class DescribeInstancePatchesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatches.html#SSM.Paginator.DescribeInstancePatches)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepatchespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef]
    ) -> _PageIterator[DescribeInstancePatchesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatches.html#SSM.Paginator.DescribeInstancePatches.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepatchespaginator)
        """


class DescribeInstancePropertiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceProperties.html#SSM.Paginator.DescribeInstanceProperties)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepropertiespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstancePropertiesRequestDescribeInstancePropertiesPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeInstancePropertiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceProperties.html#SSM.Paginator.DescribeInstanceProperties.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinstancepropertiespaginator)
        """


class DescribeInventoryDeletionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInventoryDeletions.html#SSM.Paginator.DescribeInventoryDeletions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinventorydeletionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInventoryDeletionsRequestDescribeInventoryDeletionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeInventoryDeletionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInventoryDeletions.html#SSM.Paginator.DescribeInventoryDeletions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeinventorydeletionspaginator)
        """


class DescribeMaintenanceWindowExecutionTaskInvocationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutionTaskInvocations.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTaskInvocations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowexecutiontaskinvocationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutionTaskInvocations.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTaskInvocations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowexecutiontaskinvocationspaginator)
        """


class DescribeMaintenanceWindowExecutionTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutionTasks.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowexecutiontaskspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeMaintenanceWindowExecutionTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutionTasks.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowexecutiontaskspaginator)
        """


class DescribeMaintenanceWindowExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutions.html#SSM.Paginator.DescribeMaintenanceWindowExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowexecutionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeMaintenanceWindowExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutions.html#SSM.Paginator.DescribeMaintenanceWindowExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowexecutionspaginator)
        """


class DescribeMaintenanceWindowSchedulePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowSchedule.html#SSM.Paginator.DescribeMaintenanceWindowSchedule)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowschedulepaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowScheduleRequestDescribeMaintenanceWindowSchedulePaginateTypeDef
        ],
    ) -> _PageIterator[DescribeMaintenanceWindowScheduleResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowSchedule.html#SSM.Paginator.DescribeMaintenanceWindowSchedule.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowschedulepaginator)
        """


class DescribeMaintenanceWindowTargetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowTargets.html#SSM.Paginator.DescribeMaintenanceWindowTargets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowtargetspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeMaintenanceWindowTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowTargets.html#SSM.Paginator.DescribeMaintenanceWindowTargets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowtargetspaginator)
        """


class DescribeMaintenanceWindowTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowTasks.html#SSM.Paginator.DescribeMaintenanceWindowTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowtaskspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeMaintenanceWindowTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowTasks.html#SSM.Paginator.DescribeMaintenanceWindowTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowtaskspaginator)
        """


class DescribeMaintenanceWindowsForTargetPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowsForTarget.html#SSM.Paginator.DescribeMaintenanceWindowsForTarget)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowsfortargetpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeMaintenanceWindowsForTargetResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowsForTarget.html#SSM.Paginator.DescribeMaintenanceWindowsForTarget.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowsfortargetpaginator)
        """


class DescribeMaintenanceWindowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindows.html#SSM.Paginator.DescribeMaintenanceWindows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowsRequestDescribeMaintenanceWindowsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeMaintenanceWindowsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindows.html#SSM.Paginator.DescribeMaintenanceWindows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describemaintenancewindowspaginator)
        """


class DescribeOpsItemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeOpsItems.html#SSM.Paginator.DescribeOpsItems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeopsitemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeOpsItemsRequestDescribeOpsItemsPaginateTypeDef]
    ) -> _PageIterator[DescribeOpsItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeOpsItems.html#SSM.Paginator.DescribeOpsItems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeopsitemspaginator)
        """


class DescribeParametersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeParameters.html#SSM.Paginator.DescribeParameters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeparameterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeParametersRequestDescribeParametersPaginateTypeDef]
    ) -> _PageIterator[DescribeParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeParameters.html#SSM.Paginator.DescribeParameters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describeparameterspaginator)
        """


class DescribePatchBaselinesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchBaselines.html#SSM.Paginator.DescribePatchBaselines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describepatchbaselinespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribePatchBaselinesRequestDescribePatchBaselinesPaginateTypeDef]
    ) -> _PageIterator[DescribePatchBaselinesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchBaselines.html#SSM.Paginator.DescribePatchBaselines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describepatchbaselinespaginator)
        """


class DescribePatchGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchGroups.html#SSM.Paginator.DescribePatchGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describepatchgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribePatchGroupsRequestDescribePatchGroupsPaginateTypeDef]
    ) -> _PageIterator[DescribePatchGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchGroups.html#SSM.Paginator.DescribePatchGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describepatchgroupspaginator)
        """


class DescribePatchPropertiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchProperties.html#SSM.Paginator.DescribePatchProperties)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describepatchpropertiespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef]
    ) -> _PageIterator[DescribePatchPropertiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchProperties.html#SSM.Paginator.DescribePatchProperties.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describepatchpropertiespaginator)
        """


class DescribeSessionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeSessions.html#SSM.Paginator.DescribeSessions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describesessionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSessionsRequestDescribeSessionsPaginateTypeDef]
    ) -> _PageIterator[DescribeSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeSessions.html#SSM.Paginator.DescribeSessions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#describesessionspaginator)
        """


class GetInventoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetInventory.html#SSM.Paginator.GetInventory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getinventorypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetInventoryRequestGetInventoryPaginateTypeDef]
    ) -> _PageIterator[GetInventoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetInventory.html#SSM.Paginator.GetInventory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getinventorypaginator)
        """


class GetInventorySchemaPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetInventorySchema.html#SSM.Paginator.GetInventorySchema)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getinventoryschemapaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetInventorySchemaRequestGetInventorySchemaPaginateTypeDef]
    ) -> _PageIterator[GetInventorySchemaResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetInventorySchema.html#SSM.Paginator.GetInventorySchema.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getinventoryschemapaginator)
        """


class GetOpsSummaryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetOpsSummary.html#SSM.Paginator.GetOpsSummary)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getopssummarypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetOpsSummaryRequestGetOpsSummaryPaginateTypeDef]
    ) -> _PageIterator[GetOpsSummaryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetOpsSummary.html#SSM.Paginator.GetOpsSummary.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getopssummarypaginator)
        """


class GetParameterHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetParameterHistory.html#SSM.Paginator.GetParameterHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getparameterhistorypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetParameterHistoryRequestGetParameterHistoryPaginateTypeDef]
    ) -> _PageIterator[GetParameterHistoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetParameterHistory.html#SSM.Paginator.GetParameterHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getparameterhistorypaginator)
        """


class GetParametersByPathPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetParametersByPath.html#SSM.Paginator.GetParametersByPath)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getparametersbypathpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetParametersByPathRequestGetParametersByPathPaginateTypeDef]
    ) -> _PageIterator[GetParametersByPathResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetParametersByPath.html#SSM.Paginator.GetParametersByPath.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getparametersbypathpaginator)
        """


class GetResourcePoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetResourcePolicies.html#SSM.Paginator.GetResourcePolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getresourcepoliciespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef]
    ) -> _PageIterator[GetResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetResourcePolicies.html#SSM.Paginator.GetResourcePolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#getresourcepoliciespaginator)
        """


class ListAssociationVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListAssociationVersions.html#SSM.Paginator.ListAssociationVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listassociationversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef]
    ) -> _PageIterator[ListAssociationVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListAssociationVersions.html#SSM.Paginator.ListAssociationVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listassociationversionspaginator)
        """


class ListAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListAssociations.html#SSM.Paginator.ListAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listassociationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssociationsRequestListAssociationsPaginateTypeDef]
    ) -> _PageIterator[ListAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListAssociations.html#SSM.Paginator.ListAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listassociationspaginator)
        """


class ListCommandInvocationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListCommandInvocations.html#SSM.Paginator.ListCommandInvocations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcommandinvocationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCommandInvocationsRequestListCommandInvocationsPaginateTypeDef]
    ) -> _PageIterator[ListCommandInvocationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListCommandInvocations.html#SSM.Paginator.ListCommandInvocations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcommandinvocationspaginator)
        """


class ListCommandsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListCommands.html#SSM.Paginator.ListCommands)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcommandspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCommandsRequestListCommandsPaginateTypeDef]
    ) -> _PageIterator[ListCommandsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListCommands.html#SSM.Paginator.ListCommands.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcommandspaginator)
        """


class ListComplianceItemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListComplianceItems.html#SSM.Paginator.ListComplianceItems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcomplianceitemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListComplianceItemsRequestListComplianceItemsPaginateTypeDef]
    ) -> _PageIterator[ListComplianceItemsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListComplianceItems.html#SSM.Paginator.ListComplianceItems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcomplianceitemspaginator)
        """


class ListComplianceSummariesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListComplianceSummaries.html#SSM.Paginator.ListComplianceSummaries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcompliancesummariespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListComplianceSummariesRequestListComplianceSummariesPaginateTypeDef]
    ) -> _PageIterator[ListComplianceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListComplianceSummaries.html#SSM.Paginator.ListComplianceSummaries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listcompliancesummariespaginator)
        """


class ListDocumentVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListDocumentVersions.html#SSM.Paginator.ListDocumentVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listdocumentversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef]
    ) -> _PageIterator[ListDocumentVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListDocumentVersions.html#SSM.Paginator.ListDocumentVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listdocumentversionspaginator)
        """


class ListDocumentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListDocuments.html#SSM.Paginator.ListDocuments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listdocumentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDocumentsRequestListDocumentsPaginateTypeDef]
    ) -> _PageIterator[ListDocumentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListDocuments.html#SSM.Paginator.ListDocuments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listdocumentspaginator)
        """


class ListNodesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListNodes.html#SSM.Paginator.ListNodes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listnodespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNodesRequestListNodesPaginateTypeDef]
    ) -> _PageIterator[ListNodesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListNodes.html#SSM.Paginator.ListNodes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listnodespaginator)
        """


class ListNodesSummaryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListNodesSummary.html#SSM.Paginator.ListNodesSummary)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listnodessummarypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNodesSummaryRequestListNodesSummaryPaginateTypeDef]
    ) -> _PageIterator[ListNodesSummaryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListNodesSummary.html#SSM.Paginator.ListNodesSummary.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listnodessummarypaginator)
        """


class ListOpsItemEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsItemEvents.html#SSM.Paginator.ListOpsItemEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listopsitemeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOpsItemEventsRequestListOpsItemEventsPaginateTypeDef]
    ) -> _PageIterator[ListOpsItemEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsItemEvents.html#SSM.Paginator.ListOpsItemEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listopsitemeventspaginator)
        """


class ListOpsItemRelatedItemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsItemRelatedItems.html#SSM.Paginator.ListOpsItemRelatedItems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listopsitemrelateditemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOpsItemRelatedItemsRequestListOpsItemRelatedItemsPaginateTypeDef]
    ) -> _PageIterator[ListOpsItemRelatedItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsItemRelatedItems.html#SSM.Paginator.ListOpsItemRelatedItems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listopsitemrelateditemspaginator)
        """


class ListOpsMetadataPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsMetadata.html#SSM.Paginator.ListOpsMetadata)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listopsmetadatapaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOpsMetadataRequestListOpsMetadataPaginateTypeDef]
    ) -> _PageIterator[ListOpsMetadataResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsMetadata.html#SSM.Paginator.ListOpsMetadata.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listopsmetadatapaginator)
        """


class ListResourceComplianceSummariesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListResourceComplianceSummaries.html#SSM.Paginator.ListResourceComplianceSummaries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listresourcecompliancesummariespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResourceComplianceSummariesRequestListResourceComplianceSummariesPaginateTypeDef
        ],
    ) -> _PageIterator[ListResourceComplianceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListResourceComplianceSummaries.html#SSM.Paginator.ListResourceComplianceSummaries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listresourcecompliancesummariespaginator)
        """


class ListResourceDataSyncPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListResourceDataSync.html#SSM.Paginator.ListResourceDataSync)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listresourcedatasyncpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResourceDataSyncRequestListResourceDataSyncPaginateTypeDef]
    ) -> _PageIterator[ListResourceDataSyncResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListResourceDataSync.html#SSM.Paginator.ListResourceDataSync.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/paginators/#listresourcedatasyncpaginator)
        """
