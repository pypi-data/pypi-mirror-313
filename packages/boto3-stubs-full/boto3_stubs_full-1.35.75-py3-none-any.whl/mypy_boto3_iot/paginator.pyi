"""
Type annotations for iot service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_iot.client import IoTClient
    from mypy_boto3_iot.paginator import (
        GetBehaviorModelTrainingSummariesPaginator,
        ListActiveViolationsPaginator,
        ListAttachedPoliciesPaginator,
        ListAuditFindingsPaginator,
        ListAuditMitigationActionsExecutionsPaginator,
        ListAuditMitigationActionsTasksPaginator,
        ListAuditSuppressionsPaginator,
        ListAuditTasksPaginator,
        ListAuthorizersPaginator,
        ListBillingGroupsPaginator,
        ListCACertificatesPaginator,
        ListCertificatesByCAPaginator,
        ListCertificatesPaginator,
        ListCommandExecutionsPaginator,
        ListCommandsPaginator,
        ListCustomMetricsPaginator,
        ListDetectMitigationActionsExecutionsPaginator,
        ListDetectMitigationActionsTasksPaginator,
        ListDimensionsPaginator,
        ListDomainConfigurationsPaginator,
        ListFleetMetricsPaginator,
        ListIndicesPaginator,
        ListJobExecutionsForJobPaginator,
        ListJobExecutionsForThingPaginator,
        ListJobTemplatesPaginator,
        ListJobsPaginator,
        ListManagedJobTemplatesPaginator,
        ListMetricValuesPaginator,
        ListMitigationActionsPaginator,
        ListOTAUpdatesPaginator,
        ListOutgoingCertificatesPaginator,
        ListPackageVersionsPaginator,
        ListPackagesPaginator,
        ListPoliciesPaginator,
        ListPolicyPrincipalsPaginator,
        ListPrincipalPoliciesPaginator,
        ListPrincipalThingsPaginator,
        ListPrincipalThingsV2Paginator,
        ListProvisioningTemplateVersionsPaginator,
        ListProvisioningTemplatesPaginator,
        ListRelatedResourcesForAuditFindingPaginator,
        ListRoleAliasesPaginator,
        ListSbomValidationResultsPaginator,
        ListScheduledAuditsPaginator,
        ListSecurityProfilesForTargetPaginator,
        ListSecurityProfilesPaginator,
        ListStreamsPaginator,
        ListTagsForResourcePaginator,
        ListTargetsForPolicyPaginator,
        ListTargetsForSecurityProfilePaginator,
        ListThingGroupsForThingPaginator,
        ListThingGroupsPaginator,
        ListThingPrincipalsPaginator,
        ListThingPrincipalsV2Paginator,
        ListThingRegistrationTaskReportsPaginator,
        ListThingRegistrationTasksPaginator,
        ListThingTypesPaginator,
        ListThingsInBillingGroupPaginator,
        ListThingsInThingGroupPaginator,
        ListThingsPaginator,
        ListTopicRuleDestinationsPaginator,
        ListTopicRulesPaginator,
        ListV2LoggingLevelsPaginator,
        ListViolationEventsPaginator,
    )

    session = Session()
    client: IoTClient = session.client("iot")

    get_behavior_model_training_summaries_paginator: GetBehaviorModelTrainingSummariesPaginator = client.get_paginator("get_behavior_model_training_summaries")
    list_active_violations_paginator: ListActiveViolationsPaginator = client.get_paginator("list_active_violations")
    list_attached_policies_paginator: ListAttachedPoliciesPaginator = client.get_paginator("list_attached_policies")
    list_audit_findings_paginator: ListAuditFindingsPaginator = client.get_paginator("list_audit_findings")
    list_audit_mitigation_actions_executions_paginator: ListAuditMitigationActionsExecutionsPaginator = client.get_paginator("list_audit_mitigation_actions_executions")
    list_audit_mitigation_actions_tasks_paginator: ListAuditMitigationActionsTasksPaginator = client.get_paginator("list_audit_mitigation_actions_tasks")
    list_audit_suppressions_paginator: ListAuditSuppressionsPaginator = client.get_paginator("list_audit_suppressions")
    list_audit_tasks_paginator: ListAuditTasksPaginator = client.get_paginator("list_audit_tasks")
    list_authorizers_paginator: ListAuthorizersPaginator = client.get_paginator("list_authorizers")
    list_billing_groups_paginator: ListBillingGroupsPaginator = client.get_paginator("list_billing_groups")
    list_ca_certificates_paginator: ListCACertificatesPaginator = client.get_paginator("list_ca_certificates")
    list_certificates_by_ca_paginator: ListCertificatesByCAPaginator = client.get_paginator("list_certificates_by_ca")
    list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
    list_command_executions_paginator: ListCommandExecutionsPaginator = client.get_paginator("list_command_executions")
    list_commands_paginator: ListCommandsPaginator = client.get_paginator("list_commands")
    list_custom_metrics_paginator: ListCustomMetricsPaginator = client.get_paginator("list_custom_metrics")
    list_detect_mitigation_actions_executions_paginator: ListDetectMitigationActionsExecutionsPaginator = client.get_paginator("list_detect_mitigation_actions_executions")
    list_detect_mitigation_actions_tasks_paginator: ListDetectMitigationActionsTasksPaginator = client.get_paginator("list_detect_mitigation_actions_tasks")
    list_dimensions_paginator: ListDimensionsPaginator = client.get_paginator("list_dimensions")
    list_domain_configurations_paginator: ListDomainConfigurationsPaginator = client.get_paginator("list_domain_configurations")
    list_fleet_metrics_paginator: ListFleetMetricsPaginator = client.get_paginator("list_fleet_metrics")
    list_indices_paginator: ListIndicesPaginator = client.get_paginator("list_indices")
    list_job_executions_for_job_paginator: ListJobExecutionsForJobPaginator = client.get_paginator("list_job_executions_for_job")
    list_job_executions_for_thing_paginator: ListJobExecutionsForThingPaginator = client.get_paginator("list_job_executions_for_thing")
    list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_managed_job_templates_paginator: ListManagedJobTemplatesPaginator = client.get_paginator("list_managed_job_templates")
    list_metric_values_paginator: ListMetricValuesPaginator = client.get_paginator("list_metric_values")
    list_mitigation_actions_paginator: ListMitigationActionsPaginator = client.get_paginator("list_mitigation_actions")
    list_ota_updates_paginator: ListOTAUpdatesPaginator = client.get_paginator("list_ota_updates")
    list_outgoing_certificates_paginator: ListOutgoingCertificatesPaginator = client.get_paginator("list_outgoing_certificates")
    list_package_versions_paginator: ListPackageVersionsPaginator = client.get_paginator("list_package_versions")
    list_packages_paginator: ListPackagesPaginator = client.get_paginator("list_packages")
    list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
    list_policy_principals_paginator: ListPolicyPrincipalsPaginator = client.get_paginator("list_policy_principals")
    list_principal_policies_paginator: ListPrincipalPoliciesPaginator = client.get_paginator("list_principal_policies")
    list_principal_things_paginator: ListPrincipalThingsPaginator = client.get_paginator("list_principal_things")
    list_principal_things_v2_paginator: ListPrincipalThingsV2Paginator = client.get_paginator("list_principal_things_v2")
    list_provisioning_template_versions_paginator: ListProvisioningTemplateVersionsPaginator = client.get_paginator("list_provisioning_template_versions")
    list_provisioning_templates_paginator: ListProvisioningTemplatesPaginator = client.get_paginator("list_provisioning_templates")
    list_related_resources_for_audit_finding_paginator: ListRelatedResourcesForAuditFindingPaginator = client.get_paginator("list_related_resources_for_audit_finding")
    list_role_aliases_paginator: ListRoleAliasesPaginator = client.get_paginator("list_role_aliases")
    list_sbom_validation_results_paginator: ListSbomValidationResultsPaginator = client.get_paginator("list_sbom_validation_results")
    list_scheduled_audits_paginator: ListScheduledAuditsPaginator = client.get_paginator("list_scheduled_audits")
    list_security_profiles_for_target_paginator: ListSecurityProfilesForTargetPaginator = client.get_paginator("list_security_profiles_for_target")
    list_security_profiles_paginator: ListSecurityProfilesPaginator = client.get_paginator("list_security_profiles")
    list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_targets_for_policy_paginator: ListTargetsForPolicyPaginator = client.get_paginator("list_targets_for_policy")
    list_targets_for_security_profile_paginator: ListTargetsForSecurityProfilePaginator = client.get_paginator("list_targets_for_security_profile")
    list_thing_groups_for_thing_paginator: ListThingGroupsForThingPaginator = client.get_paginator("list_thing_groups_for_thing")
    list_thing_groups_paginator: ListThingGroupsPaginator = client.get_paginator("list_thing_groups")
    list_thing_principals_paginator: ListThingPrincipalsPaginator = client.get_paginator("list_thing_principals")
    list_thing_principals_v2_paginator: ListThingPrincipalsV2Paginator = client.get_paginator("list_thing_principals_v2")
    list_thing_registration_task_reports_paginator: ListThingRegistrationTaskReportsPaginator = client.get_paginator("list_thing_registration_task_reports")
    list_thing_registration_tasks_paginator: ListThingRegistrationTasksPaginator = client.get_paginator("list_thing_registration_tasks")
    list_thing_types_paginator: ListThingTypesPaginator = client.get_paginator("list_thing_types")
    list_things_in_billing_group_paginator: ListThingsInBillingGroupPaginator = client.get_paginator("list_things_in_billing_group")
    list_things_in_thing_group_paginator: ListThingsInThingGroupPaginator = client.get_paginator("list_things_in_thing_group")
    list_things_paginator: ListThingsPaginator = client.get_paginator("list_things")
    list_topic_rule_destinations_paginator: ListTopicRuleDestinationsPaginator = client.get_paginator("list_topic_rule_destinations")
    list_topic_rules_paginator: ListTopicRulesPaginator = client.get_paginator("list_topic_rules")
    list_v2_logging_levels_paginator: ListV2LoggingLevelsPaginator = client.get_paginator("list_v2_logging_levels")
    list_violation_events_paginator: ListViolationEventsPaginator = client.get_paginator("list_violation_events")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetBehaviorModelTrainingSummariesRequestGetBehaviorModelTrainingSummariesPaginateTypeDef,
    GetBehaviorModelTrainingSummariesResponseTypeDef,
    ListActiveViolationsRequestListActiveViolationsPaginateTypeDef,
    ListActiveViolationsResponseTypeDef,
    ListAttachedPoliciesRequestListAttachedPoliciesPaginateTypeDef,
    ListAttachedPoliciesResponseTypeDef,
    ListAuditFindingsRequestListAuditFindingsPaginateTypeDef,
    ListAuditFindingsResponseTypeDef,
    ListAuditMitigationActionsExecutionsRequestListAuditMitigationActionsExecutionsPaginateTypeDef,
    ListAuditMitigationActionsExecutionsResponseTypeDef,
    ListAuditMitigationActionsTasksRequestListAuditMitigationActionsTasksPaginateTypeDef,
    ListAuditMitigationActionsTasksResponseTypeDef,
    ListAuditSuppressionsRequestListAuditSuppressionsPaginateTypeDef,
    ListAuditSuppressionsResponseTypeDef,
    ListAuditTasksRequestListAuditTasksPaginateTypeDef,
    ListAuditTasksResponseTypeDef,
    ListAuthorizersRequestListAuthorizersPaginateTypeDef,
    ListAuthorizersResponseTypeDef,
    ListBillingGroupsRequestListBillingGroupsPaginateTypeDef,
    ListBillingGroupsResponseTypeDef,
    ListCACertificatesRequestListCACertificatesPaginateTypeDef,
    ListCACertificatesResponseTypeDef,
    ListCertificatesByCARequestListCertificatesByCAPaginateTypeDef,
    ListCertificatesByCAResponseTypeDef,
    ListCertificatesRequestListCertificatesPaginateTypeDef,
    ListCertificatesResponseTypeDef,
    ListCommandExecutionsRequestListCommandExecutionsPaginateTypeDef,
    ListCommandExecutionsResponseTypeDef,
    ListCommandsRequestListCommandsPaginateTypeDef,
    ListCommandsResponseTypeDef,
    ListCustomMetricsRequestListCustomMetricsPaginateTypeDef,
    ListCustomMetricsResponseTypeDef,
    ListDetectMitigationActionsExecutionsRequestListDetectMitigationActionsExecutionsPaginateTypeDef,
    ListDetectMitigationActionsExecutionsResponseTypeDef,
    ListDetectMitigationActionsTasksRequestListDetectMitigationActionsTasksPaginateTypeDef,
    ListDetectMitigationActionsTasksResponseTypeDef,
    ListDimensionsRequestListDimensionsPaginateTypeDef,
    ListDimensionsResponseTypeDef,
    ListDomainConfigurationsRequestListDomainConfigurationsPaginateTypeDef,
    ListDomainConfigurationsResponseTypeDef,
    ListFleetMetricsRequestListFleetMetricsPaginateTypeDef,
    ListFleetMetricsResponseTypeDef,
    ListIndicesRequestListIndicesPaginateTypeDef,
    ListIndicesResponseTypeDef,
    ListJobExecutionsForJobRequestListJobExecutionsForJobPaginateTypeDef,
    ListJobExecutionsForJobResponseTypeDef,
    ListJobExecutionsForThingRequestListJobExecutionsForThingPaginateTypeDef,
    ListJobExecutionsForThingResponseTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesRequestListJobTemplatesPaginateTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListManagedJobTemplatesRequestListManagedJobTemplatesPaginateTypeDef,
    ListManagedJobTemplatesResponseTypeDef,
    ListMetricValuesRequestListMetricValuesPaginateTypeDef,
    ListMetricValuesResponseTypeDef,
    ListMitigationActionsRequestListMitigationActionsPaginateTypeDef,
    ListMitigationActionsResponseTypeDef,
    ListOTAUpdatesRequestListOTAUpdatesPaginateTypeDef,
    ListOTAUpdatesResponseTypeDef,
    ListOutgoingCertificatesRequestListOutgoingCertificatesPaginateTypeDef,
    ListOutgoingCertificatesResponseTypeDef,
    ListPackagesRequestListPackagesPaginateTypeDef,
    ListPackagesResponseTypeDef,
    ListPackageVersionsRequestListPackageVersionsPaginateTypeDef,
    ListPackageVersionsResponseTypeDef,
    ListPoliciesRequestListPoliciesPaginateTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyPrincipalsRequestListPolicyPrincipalsPaginateTypeDef,
    ListPolicyPrincipalsResponseTypeDef,
    ListPrincipalPoliciesRequestListPrincipalPoliciesPaginateTypeDef,
    ListPrincipalPoliciesResponseTypeDef,
    ListPrincipalThingsRequestListPrincipalThingsPaginateTypeDef,
    ListPrincipalThingsResponseTypeDef,
    ListPrincipalThingsV2RequestListPrincipalThingsV2PaginateTypeDef,
    ListPrincipalThingsV2ResponseTypeDef,
    ListProvisioningTemplatesRequestListProvisioningTemplatesPaginateTypeDef,
    ListProvisioningTemplatesResponseTypeDef,
    ListProvisioningTemplateVersionsRequestListProvisioningTemplateVersionsPaginateTypeDef,
    ListProvisioningTemplateVersionsResponseTypeDef,
    ListRelatedResourcesForAuditFindingRequestListRelatedResourcesForAuditFindingPaginateTypeDef,
    ListRelatedResourcesForAuditFindingResponseTypeDef,
    ListRoleAliasesRequestListRoleAliasesPaginateTypeDef,
    ListRoleAliasesResponseTypeDef,
    ListSbomValidationResultsRequestListSbomValidationResultsPaginateTypeDef,
    ListSbomValidationResultsResponseTypeDef,
    ListScheduledAuditsRequestListScheduledAuditsPaginateTypeDef,
    ListScheduledAuditsResponseTypeDef,
    ListSecurityProfilesForTargetRequestListSecurityProfilesForTargetPaginateTypeDef,
    ListSecurityProfilesForTargetResponseTypeDef,
    ListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListStreamsRequestListStreamsPaginateTypeDef,
    ListStreamsResponseTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef,
    ListTargetsForPolicyResponseTypeDef,
    ListTargetsForSecurityProfileRequestListTargetsForSecurityProfilePaginateTypeDef,
    ListTargetsForSecurityProfileResponseTypeDef,
    ListThingGroupsForThingRequestListThingGroupsForThingPaginateTypeDef,
    ListThingGroupsForThingResponseTypeDef,
    ListThingGroupsRequestListThingGroupsPaginateTypeDef,
    ListThingGroupsResponseTypeDef,
    ListThingPrincipalsRequestListThingPrincipalsPaginateTypeDef,
    ListThingPrincipalsResponseTypeDef,
    ListThingPrincipalsV2RequestListThingPrincipalsV2PaginateTypeDef,
    ListThingPrincipalsV2ResponseTypeDef,
    ListThingRegistrationTaskReportsRequestListThingRegistrationTaskReportsPaginateTypeDef,
    ListThingRegistrationTaskReportsResponseTypeDef,
    ListThingRegistrationTasksRequestListThingRegistrationTasksPaginateTypeDef,
    ListThingRegistrationTasksResponseTypeDef,
    ListThingsInBillingGroupRequestListThingsInBillingGroupPaginateTypeDef,
    ListThingsInBillingGroupResponseTypeDef,
    ListThingsInThingGroupRequestListThingsInThingGroupPaginateTypeDef,
    ListThingsInThingGroupResponseTypeDef,
    ListThingsRequestListThingsPaginateTypeDef,
    ListThingsResponseTypeDef,
    ListThingTypesRequestListThingTypesPaginateTypeDef,
    ListThingTypesResponseTypeDef,
    ListTopicRuleDestinationsRequestListTopicRuleDestinationsPaginateTypeDef,
    ListTopicRuleDestinationsResponseTypeDef,
    ListTopicRulesRequestListTopicRulesPaginateTypeDef,
    ListTopicRulesResponseTypeDef,
    ListV2LoggingLevelsRequestListV2LoggingLevelsPaginateTypeDef,
    ListV2LoggingLevelsResponseTypeDef,
    ListViolationEventsRequestListViolationEventsPaginateTypeDef,
    ListViolationEventsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetBehaviorModelTrainingSummariesPaginator",
    "ListActiveViolationsPaginator",
    "ListAttachedPoliciesPaginator",
    "ListAuditFindingsPaginator",
    "ListAuditMitigationActionsExecutionsPaginator",
    "ListAuditMitigationActionsTasksPaginator",
    "ListAuditSuppressionsPaginator",
    "ListAuditTasksPaginator",
    "ListAuthorizersPaginator",
    "ListBillingGroupsPaginator",
    "ListCACertificatesPaginator",
    "ListCertificatesByCAPaginator",
    "ListCertificatesPaginator",
    "ListCommandExecutionsPaginator",
    "ListCommandsPaginator",
    "ListCustomMetricsPaginator",
    "ListDetectMitigationActionsExecutionsPaginator",
    "ListDetectMitigationActionsTasksPaginator",
    "ListDimensionsPaginator",
    "ListDomainConfigurationsPaginator",
    "ListFleetMetricsPaginator",
    "ListIndicesPaginator",
    "ListJobExecutionsForJobPaginator",
    "ListJobExecutionsForThingPaginator",
    "ListJobTemplatesPaginator",
    "ListJobsPaginator",
    "ListManagedJobTemplatesPaginator",
    "ListMetricValuesPaginator",
    "ListMitigationActionsPaginator",
    "ListOTAUpdatesPaginator",
    "ListOutgoingCertificatesPaginator",
    "ListPackageVersionsPaginator",
    "ListPackagesPaginator",
    "ListPoliciesPaginator",
    "ListPolicyPrincipalsPaginator",
    "ListPrincipalPoliciesPaginator",
    "ListPrincipalThingsPaginator",
    "ListPrincipalThingsV2Paginator",
    "ListProvisioningTemplateVersionsPaginator",
    "ListProvisioningTemplatesPaginator",
    "ListRelatedResourcesForAuditFindingPaginator",
    "ListRoleAliasesPaginator",
    "ListSbomValidationResultsPaginator",
    "ListScheduledAuditsPaginator",
    "ListSecurityProfilesForTargetPaginator",
    "ListSecurityProfilesPaginator",
    "ListStreamsPaginator",
    "ListTagsForResourcePaginator",
    "ListTargetsForPolicyPaginator",
    "ListTargetsForSecurityProfilePaginator",
    "ListThingGroupsForThingPaginator",
    "ListThingGroupsPaginator",
    "ListThingPrincipalsPaginator",
    "ListThingPrincipalsV2Paginator",
    "ListThingRegistrationTaskReportsPaginator",
    "ListThingRegistrationTasksPaginator",
    "ListThingTypesPaginator",
    "ListThingsInBillingGroupPaginator",
    "ListThingsInThingGroupPaginator",
    "ListThingsPaginator",
    "ListTopicRuleDestinationsPaginator",
    "ListTopicRulesPaginator",
    "ListV2LoggingLevelsPaginator",
    "ListViolationEventsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetBehaviorModelTrainingSummariesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/GetBehaviorModelTrainingSummaries.html#IoT.Paginator.GetBehaviorModelTrainingSummaries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#getbehaviormodeltrainingsummariespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetBehaviorModelTrainingSummariesRequestGetBehaviorModelTrainingSummariesPaginateTypeDef
        ],
    ) -> _PageIterator[GetBehaviorModelTrainingSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/GetBehaviorModelTrainingSummaries.html#IoT.Paginator.GetBehaviorModelTrainingSummaries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#getbehaviormodeltrainingsummariespaginator)
        """

class ListActiveViolationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListActiveViolations.html#IoT.Paginator.ListActiveViolations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listactiveviolationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListActiveViolationsRequestListActiveViolationsPaginateTypeDef]
    ) -> _PageIterator[ListActiveViolationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListActiveViolations.html#IoT.Paginator.ListActiveViolations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listactiveviolationspaginator)
        """

class ListAttachedPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAttachedPolicies.html#IoT.Paginator.ListAttachedPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listattachedpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAttachedPoliciesRequestListAttachedPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListAttachedPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAttachedPolicies.html#IoT.Paginator.ListAttachedPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listattachedpoliciespaginator)
        """

class ListAuditFindingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditFindings.html#IoT.Paginator.ListAuditFindings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditfindingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAuditFindingsRequestListAuditFindingsPaginateTypeDef]
    ) -> _PageIterator[ListAuditFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditFindings.html#IoT.Paginator.ListAuditFindings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditfindingspaginator)
        """

class ListAuditMitigationActionsExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditMitigationActionsExecutions.html#IoT.Paginator.ListAuditMitigationActionsExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditmitigationactionsexecutionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAuditMitigationActionsExecutionsRequestListAuditMitigationActionsExecutionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListAuditMitigationActionsExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditMitigationActionsExecutions.html#IoT.Paginator.ListAuditMitigationActionsExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditmitigationactionsexecutionspaginator)
        """

class ListAuditMitigationActionsTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditMitigationActionsTasks.html#IoT.Paginator.ListAuditMitigationActionsTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditmitigationactionstaskspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAuditMitigationActionsTasksRequestListAuditMitigationActionsTasksPaginateTypeDef
        ],
    ) -> _PageIterator[ListAuditMitigationActionsTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditMitigationActionsTasks.html#IoT.Paginator.ListAuditMitigationActionsTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditmitigationactionstaskspaginator)
        """

class ListAuditSuppressionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditSuppressions.html#IoT.Paginator.ListAuditSuppressions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditsuppressionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAuditSuppressionsRequestListAuditSuppressionsPaginateTypeDef]
    ) -> _PageIterator[ListAuditSuppressionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditSuppressions.html#IoT.Paginator.ListAuditSuppressions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauditsuppressionspaginator)
        """

class ListAuditTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditTasks.html#IoT.Paginator.ListAuditTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listaudittaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAuditTasksRequestListAuditTasksPaginateTypeDef]
    ) -> _PageIterator[ListAuditTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditTasks.html#IoT.Paginator.ListAuditTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listaudittaskspaginator)
        """

class ListAuthorizersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuthorizers.html#IoT.Paginator.ListAuthorizers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauthorizerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAuthorizersRequestListAuthorizersPaginateTypeDef]
    ) -> _PageIterator[ListAuthorizersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuthorizers.html#IoT.Paginator.ListAuthorizers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listauthorizerspaginator)
        """

class ListBillingGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListBillingGroups.html#IoT.Paginator.ListBillingGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listbillinggroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBillingGroupsRequestListBillingGroupsPaginateTypeDef]
    ) -> _PageIterator[ListBillingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListBillingGroups.html#IoT.Paginator.ListBillingGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listbillinggroupspaginator)
        """

class ListCACertificatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCACertificates.html#IoT.Paginator.ListCACertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcacertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCACertificatesRequestListCACertificatesPaginateTypeDef]
    ) -> _PageIterator[ListCACertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCACertificates.html#IoT.Paginator.ListCACertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcacertificatespaginator)
        """

class ListCertificatesByCAPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCertificatesByCA.html#IoT.Paginator.ListCertificatesByCA)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcertificatesbycapaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCertificatesByCARequestListCertificatesByCAPaginateTypeDef]
    ) -> _PageIterator[ListCertificatesByCAResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCertificatesByCA.html#IoT.Paginator.ListCertificatesByCA.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcertificatesbycapaginator)
        """

class ListCertificatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCertificates.html#IoT.Paginator.ListCertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCertificatesRequestListCertificatesPaginateTypeDef]
    ) -> _PageIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCertificates.html#IoT.Paginator.ListCertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcertificatespaginator)
        """

class ListCommandExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCommandExecutions.html#IoT.Paginator.ListCommandExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcommandexecutionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCommandExecutionsRequestListCommandExecutionsPaginateTypeDef]
    ) -> _PageIterator[ListCommandExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCommandExecutions.html#IoT.Paginator.ListCommandExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcommandexecutionspaginator)
        """

class ListCommandsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCommands.html#IoT.Paginator.ListCommands)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcommandspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCommandsRequestListCommandsPaginateTypeDef]
    ) -> _PageIterator[ListCommandsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCommands.html#IoT.Paginator.ListCommands.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcommandspaginator)
        """

class ListCustomMetricsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCustomMetrics.html#IoT.Paginator.ListCustomMetrics)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcustommetricspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCustomMetricsRequestListCustomMetricsPaginateTypeDef]
    ) -> _PageIterator[ListCustomMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCustomMetrics.html#IoT.Paginator.ListCustomMetrics.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listcustommetricspaginator)
        """

class ListDetectMitigationActionsExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDetectMitigationActionsExecutions.html#IoT.Paginator.ListDetectMitigationActionsExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdetectmitigationactionsexecutionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListDetectMitigationActionsExecutionsRequestListDetectMitigationActionsExecutionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListDetectMitigationActionsExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDetectMitigationActionsExecutions.html#IoT.Paginator.ListDetectMitigationActionsExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdetectmitigationactionsexecutionspaginator)
        """

class ListDetectMitigationActionsTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDetectMitigationActionsTasks.html#IoT.Paginator.ListDetectMitigationActionsTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdetectmitigationactionstaskspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListDetectMitigationActionsTasksRequestListDetectMitigationActionsTasksPaginateTypeDef
        ],
    ) -> _PageIterator[ListDetectMitigationActionsTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDetectMitigationActionsTasks.html#IoT.Paginator.ListDetectMitigationActionsTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdetectmitigationactionstaskspaginator)
        """

class ListDimensionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDimensions.html#IoT.Paginator.ListDimensions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdimensionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDimensionsRequestListDimensionsPaginateTypeDef]
    ) -> _PageIterator[ListDimensionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDimensions.html#IoT.Paginator.ListDimensions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdimensionspaginator)
        """

class ListDomainConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDomainConfigurations.html#IoT.Paginator.ListDomainConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdomainconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListDomainConfigurationsRequestListDomainConfigurationsPaginateTypeDef],
    ) -> _PageIterator[ListDomainConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDomainConfigurations.html#IoT.Paginator.ListDomainConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listdomainconfigurationspaginator)
        """

class ListFleetMetricsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListFleetMetrics.html#IoT.Paginator.ListFleetMetrics)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listfleetmetricspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFleetMetricsRequestListFleetMetricsPaginateTypeDef]
    ) -> _PageIterator[ListFleetMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListFleetMetrics.html#IoT.Paginator.ListFleetMetrics.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listfleetmetricspaginator)
        """

class ListIndicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListIndices.html#IoT.Paginator.ListIndices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listindicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIndicesRequestListIndicesPaginateTypeDef]
    ) -> _PageIterator[ListIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListIndices.html#IoT.Paginator.ListIndices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listindicespaginator)
        """

class ListJobExecutionsForJobPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobExecutionsForJob.html#IoT.Paginator.ListJobExecutionsForJob)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobexecutionsforjobpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobExecutionsForJobRequestListJobExecutionsForJobPaginateTypeDef]
    ) -> _PageIterator[ListJobExecutionsForJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobExecutionsForJob.html#IoT.Paginator.ListJobExecutionsForJob.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobexecutionsforjobpaginator)
        """

class ListJobExecutionsForThingPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobExecutionsForThing.html#IoT.Paginator.ListJobExecutionsForThing)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobexecutionsforthingpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListJobExecutionsForThingRequestListJobExecutionsForThingPaginateTypeDef],
    ) -> _PageIterator[ListJobExecutionsForThingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobExecutionsForThing.html#IoT.Paginator.ListJobExecutionsForThing.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobexecutionsforthingpaginator)
        """

class ListJobTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobTemplates.html#IoT.Paginator.ListJobTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobtemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobTemplatesRequestListJobTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListJobTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobTemplates.html#IoT.Paginator.ListJobTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobtemplatespaginator)
        """

class ListJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobs.html#IoT.Paginator.ListJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> _PageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobs.html#IoT.Paginator.ListJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listjobspaginator)
        """

class ListManagedJobTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListManagedJobTemplates.html#IoT.Paginator.ListManagedJobTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listmanagedjobtemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListManagedJobTemplatesRequestListManagedJobTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListManagedJobTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListManagedJobTemplates.html#IoT.Paginator.ListManagedJobTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listmanagedjobtemplatespaginator)
        """

class ListMetricValuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListMetricValues.html#IoT.Paginator.ListMetricValues)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listmetricvaluespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMetricValuesRequestListMetricValuesPaginateTypeDef]
    ) -> _PageIterator[ListMetricValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListMetricValues.html#IoT.Paginator.ListMetricValues.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listmetricvaluespaginator)
        """

class ListMitigationActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListMitigationActions.html#IoT.Paginator.ListMitigationActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listmitigationactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMitigationActionsRequestListMitigationActionsPaginateTypeDef]
    ) -> _PageIterator[ListMitigationActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListMitigationActions.html#IoT.Paginator.ListMitigationActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listmitigationactionspaginator)
        """

class ListOTAUpdatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListOTAUpdates.html#IoT.Paginator.ListOTAUpdates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listotaupdatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOTAUpdatesRequestListOTAUpdatesPaginateTypeDef]
    ) -> _PageIterator[ListOTAUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListOTAUpdates.html#IoT.Paginator.ListOTAUpdates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listotaupdatespaginator)
        """

class ListOutgoingCertificatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListOutgoingCertificates.html#IoT.Paginator.ListOutgoingCertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listoutgoingcertificatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListOutgoingCertificatesRequestListOutgoingCertificatesPaginateTypeDef],
    ) -> _PageIterator[ListOutgoingCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListOutgoingCertificates.html#IoT.Paginator.ListOutgoingCertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listoutgoingcertificatespaginator)
        """

class ListPackageVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPackageVersions.html#IoT.Paginator.ListPackageVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listpackageversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPackageVersionsRequestListPackageVersionsPaginateTypeDef]
    ) -> _PageIterator[ListPackageVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPackageVersions.html#IoT.Paginator.ListPackageVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listpackageversionspaginator)
        """

class ListPackagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPackages.html#IoT.Paginator.ListPackages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listpackagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPackagesRequestListPackagesPaginateTypeDef]
    ) -> _PageIterator[ListPackagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPackages.html#IoT.Paginator.ListPackages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listpackagespaginator)
        """

class ListPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPolicies.html#IoT.Paginator.ListPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPoliciesRequestListPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPolicies.html#IoT.Paginator.ListPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listpoliciespaginator)
        """

class ListPolicyPrincipalsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPolicyPrincipals.html#IoT.Paginator.ListPolicyPrincipals)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listpolicyprincipalspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPolicyPrincipalsRequestListPolicyPrincipalsPaginateTypeDef]
    ) -> _PageIterator[ListPolicyPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPolicyPrincipals.html#IoT.Paginator.ListPolicyPrincipals.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listpolicyprincipalspaginator)
        """

class ListPrincipalPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalPolicies.html#IoT.Paginator.ListPrincipalPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprincipalpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPrincipalPoliciesRequestListPrincipalPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListPrincipalPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalPolicies.html#IoT.Paginator.ListPrincipalPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprincipalpoliciespaginator)
        """

class ListPrincipalThingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalThings.html#IoT.Paginator.ListPrincipalThings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprincipalthingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPrincipalThingsRequestListPrincipalThingsPaginateTypeDef]
    ) -> _PageIterator[ListPrincipalThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalThings.html#IoT.Paginator.ListPrincipalThings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprincipalthingspaginator)
        """

class ListPrincipalThingsV2Paginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalThingsV2.html#IoT.Paginator.ListPrincipalThingsV2)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprincipalthingsv2paginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPrincipalThingsV2RequestListPrincipalThingsV2PaginateTypeDef]
    ) -> _PageIterator[ListPrincipalThingsV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalThingsV2.html#IoT.Paginator.ListPrincipalThingsV2.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprincipalthingsv2paginator)
        """

class ListProvisioningTemplateVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListProvisioningTemplateVersions.html#IoT.Paginator.ListProvisioningTemplateVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprovisioningtemplateversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListProvisioningTemplateVersionsRequestListProvisioningTemplateVersionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListProvisioningTemplateVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListProvisioningTemplateVersions.html#IoT.Paginator.ListProvisioningTemplateVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprovisioningtemplateversionspaginator)
        """

class ListProvisioningTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListProvisioningTemplates.html#IoT.Paginator.ListProvisioningTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprovisioningtemplatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListProvisioningTemplatesRequestListProvisioningTemplatesPaginateTypeDef],
    ) -> _PageIterator[ListProvisioningTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListProvisioningTemplates.html#IoT.Paginator.ListProvisioningTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listprovisioningtemplatespaginator)
        """

class ListRelatedResourcesForAuditFindingPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListRelatedResourcesForAuditFinding.html#IoT.Paginator.ListRelatedResourcesForAuditFinding)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listrelatedresourcesforauditfindingpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListRelatedResourcesForAuditFindingRequestListRelatedResourcesForAuditFindingPaginateTypeDef
        ],
    ) -> _PageIterator[ListRelatedResourcesForAuditFindingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListRelatedResourcesForAuditFinding.html#IoT.Paginator.ListRelatedResourcesForAuditFinding.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listrelatedresourcesforauditfindingpaginator)
        """

class ListRoleAliasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListRoleAliases.html#IoT.Paginator.ListRoleAliases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listrolealiasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRoleAliasesRequestListRoleAliasesPaginateTypeDef]
    ) -> _PageIterator[ListRoleAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListRoleAliases.html#IoT.Paginator.ListRoleAliases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listrolealiasespaginator)
        """

class ListSbomValidationResultsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSbomValidationResults.html#IoT.Paginator.ListSbomValidationResults)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listsbomvalidationresultspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListSbomValidationResultsRequestListSbomValidationResultsPaginateTypeDef],
    ) -> _PageIterator[ListSbomValidationResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSbomValidationResults.html#IoT.Paginator.ListSbomValidationResults.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listsbomvalidationresultspaginator)
        """

class ListScheduledAuditsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListScheduledAudits.html#IoT.Paginator.ListScheduledAudits)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listscheduledauditspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListScheduledAuditsRequestListScheduledAuditsPaginateTypeDef]
    ) -> _PageIterator[ListScheduledAuditsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListScheduledAudits.html#IoT.Paginator.ListScheduledAudits.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listscheduledauditspaginator)
        """

class ListSecurityProfilesForTargetPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSecurityProfilesForTarget.html#IoT.Paginator.ListSecurityProfilesForTarget)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listsecurityprofilesfortargetpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListSecurityProfilesForTargetRequestListSecurityProfilesForTargetPaginateTypeDef
        ],
    ) -> _PageIterator[ListSecurityProfilesForTargetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSecurityProfilesForTarget.html#IoT.Paginator.ListSecurityProfilesForTarget.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listsecurityprofilesfortargetpaginator)
        """

class ListSecurityProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSecurityProfiles.html#IoT.Paginator.ListSecurityProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listsecurityprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef]
    ) -> _PageIterator[ListSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSecurityProfiles.html#IoT.Paginator.ListSecurityProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listsecurityprofilespaginator)
        """

class ListStreamsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListStreams.html#IoT.Paginator.ListStreams)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#liststreamspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStreamsRequestListStreamsPaginateTypeDef]
    ) -> _PageIterator[ListStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListStreams.html#IoT.Paginator.ListStreams.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#liststreamspaginator)
        """

class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTagsForResource.html#IoT.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTagsForResource.html#IoT.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtagsforresourcepaginator)
        """

class ListTargetsForPolicyPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTargetsForPolicy.html#IoT.Paginator.ListTargetsForPolicy)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtargetsforpolicypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef]
    ) -> _PageIterator[ListTargetsForPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTargetsForPolicy.html#IoT.Paginator.ListTargetsForPolicy.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtargetsforpolicypaginator)
        """

class ListTargetsForSecurityProfilePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTargetsForSecurityProfile.html#IoT.Paginator.ListTargetsForSecurityProfile)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtargetsforsecurityprofilepaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListTargetsForSecurityProfileRequestListTargetsForSecurityProfilePaginateTypeDef
        ],
    ) -> _PageIterator[ListTargetsForSecurityProfileResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTargetsForSecurityProfile.html#IoT.Paginator.ListTargetsForSecurityProfile.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtargetsforsecurityprofilepaginator)
        """

class ListThingGroupsForThingPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingGroupsForThing.html#IoT.Paginator.ListThingGroupsForThing)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthinggroupsforthingpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThingGroupsForThingRequestListThingGroupsForThingPaginateTypeDef]
    ) -> _PageIterator[ListThingGroupsForThingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingGroupsForThing.html#IoT.Paginator.ListThingGroupsForThing.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthinggroupsforthingpaginator)
        """

class ListThingGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingGroups.html#IoT.Paginator.ListThingGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthinggroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThingGroupsRequestListThingGroupsPaginateTypeDef]
    ) -> _PageIterator[ListThingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingGroups.html#IoT.Paginator.ListThingGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthinggroupspaginator)
        """

class ListThingPrincipalsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingPrincipals.html#IoT.Paginator.ListThingPrincipals)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingprincipalspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThingPrincipalsRequestListThingPrincipalsPaginateTypeDef]
    ) -> _PageIterator[ListThingPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingPrincipals.html#IoT.Paginator.ListThingPrincipals.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingprincipalspaginator)
        """

class ListThingPrincipalsV2Paginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingPrincipalsV2.html#IoT.Paginator.ListThingPrincipalsV2)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingprincipalsv2paginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThingPrincipalsV2RequestListThingPrincipalsV2PaginateTypeDef]
    ) -> _PageIterator[ListThingPrincipalsV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingPrincipalsV2.html#IoT.Paginator.ListThingPrincipalsV2.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingprincipalsv2paginator)
        """

class ListThingRegistrationTaskReportsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingRegistrationTaskReports.html#IoT.Paginator.ListThingRegistrationTaskReports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingregistrationtaskreportspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListThingRegistrationTaskReportsRequestListThingRegistrationTaskReportsPaginateTypeDef
        ],
    ) -> _PageIterator[ListThingRegistrationTaskReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingRegistrationTaskReports.html#IoT.Paginator.ListThingRegistrationTaskReports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingregistrationtaskreportspaginator)
        """

class ListThingRegistrationTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingRegistrationTasks.html#IoT.Paginator.ListThingRegistrationTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingregistrationtaskspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListThingRegistrationTasksRequestListThingRegistrationTasksPaginateTypeDef
        ],
    ) -> _PageIterator[ListThingRegistrationTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingRegistrationTasks.html#IoT.Paginator.ListThingRegistrationTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingregistrationtaskspaginator)
        """

class ListThingTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingTypes.html#IoT.Paginator.ListThingTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingtypespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThingTypesRequestListThingTypesPaginateTypeDef]
    ) -> _PageIterator[ListThingTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingTypes.html#IoT.Paginator.ListThingTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingtypespaginator)
        """

class ListThingsInBillingGroupPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingsInBillingGroup.html#IoT.Paginator.ListThingsInBillingGroup)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingsinbillinggrouppaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListThingsInBillingGroupRequestListThingsInBillingGroupPaginateTypeDef],
    ) -> _PageIterator[ListThingsInBillingGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingsInBillingGroup.html#IoT.Paginator.ListThingsInBillingGroup.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingsinbillinggrouppaginator)
        """

class ListThingsInThingGroupPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingsInThingGroup.html#IoT.Paginator.ListThingsInThingGroup)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingsinthinggrouppaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThingsInThingGroupRequestListThingsInThingGroupPaginateTypeDef]
    ) -> _PageIterator[ListThingsInThingGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingsInThingGroup.html#IoT.Paginator.ListThingsInThingGroup.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingsinthinggrouppaginator)
        """

class ListThingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThings.html#IoT.Paginator.ListThings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThingsRequestListThingsPaginateTypeDef]
    ) -> _PageIterator[ListThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThings.html#IoT.Paginator.ListThings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listthingspaginator)
        """

class ListTopicRuleDestinationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTopicRuleDestinations.html#IoT.Paginator.ListTopicRuleDestinations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtopicruledestinationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListTopicRuleDestinationsRequestListTopicRuleDestinationsPaginateTypeDef],
    ) -> _PageIterator[ListTopicRuleDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTopicRuleDestinations.html#IoT.Paginator.ListTopicRuleDestinations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtopicruledestinationspaginator)
        """

class ListTopicRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTopicRules.html#IoT.Paginator.ListTopicRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtopicrulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTopicRulesRequestListTopicRulesPaginateTypeDef]
    ) -> _PageIterator[ListTopicRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTopicRules.html#IoT.Paginator.ListTopicRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listtopicrulespaginator)
        """

class ListV2LoggingLevelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListV2LoggingLevels.html#IoT.Paginator.ListV2LoggingLevels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listv2logginglevelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListV2LoggingLevelsRequestListV2LoggingLevelsPaginateTypeDef]
    ) -> _PageIterator[ListV2LoggingLevelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListV2LoggingLevels.html#IoT.Paginator.ListV2LoggingLevels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listv2logginglevelspaginator)
        """

class ListViolationEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListViolationEvents.html#IoT.Paginator.ListViolationEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listviolationeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListViolationEventsRequestListViolationEventsPaginateTypeDef]
    ) -> _PageIterator[ListViolationEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListViolationEvents.html#IoT.Paginator.ListViolationEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot/paginators/#listviolationeventspaginator)
        """
