"""
Type annotations for connect service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_connect.client import ConnectClient
    from mypy_boto3_connect.paginator import (
        GetMetricDataPaginator,
        ListAgentStatusesPaginator,
        ListApprovedOriginsPaginator,
        ListAuthenticationProfilesPaginator,
        ListBotsPaginator,
        ListContactEvaluationsPaginator,
        ListContactFlowModulesPaginator,
        ListContactFlowVersionsPaginator,
        ListContactFlowsPaginator,
        ListContactReferencesPaginator,
        ListDefaultVocabulariesPaginator,
        ListEvaluationFormVersionsPaginator,
        ListEvaluationFormsPaginator,
        ListFlowAssociationsPaginator,
        ListHoursOfOperationsPaginator,
        ListInstanceAttributesPaginator,
        ListInstanceStorageConfigsPaginator,
        ListInstancesPaginator,
        ListIntegrationAssociationsPaginator,
        ListLambdaFunctionsPaginator,
        ListLexBotsPaginator,
        ListPhoneNumbersPaginator,
        ListPhoneNumbersV2Paginator,
        ListPredefinedAttributesPaginator,
        ListPromptsPaginator,
        ListQueueQuickConnectsPaginator,
        ListQueuesPaginator,
        ListQuickConnectsPaginator,
        ListRoutingProfileQueuesPaginator,
        ListRoutingProfilesPaginator,
        ListRulesPaginator,
        ListSecurityKeysPaginator,
        ListSecurityProfileApplicationsPaginator,
        ListSecurityProfilePermissionsPaginator,
        ListSecurityProfilesPaginator,
        ListTaskTemplatesPaginator,
        ListTrafficDistributionGroupUsersPaginator,
        ListTrafficDistributionGroupsPaginator,
        ListUseCasesPaginator,
        ListUserHierarchyGroupsPaginator,
        ListUserProficienciesPaginator,
        ListUsersPaginator,
        ListViewVersionsPaginator,
        ListViewsPaginator,
        SearchAgentStatusesPaginator,
        SearchAvailablePhoneNumbersPaginator,
        SearchContactFlowModulesPaginator,
        SearchContactFlowsPaginator,
        SearchContactsPaginator,
        SearchHoursOfOperationsPaginator,
        SearchPredefinedAttributesPaginator,
        SearchPromptsPaginator,
        SearchQueuesPaginator,
        SearchQuickConnectsPaginator,
        SearchResourceTagsPaginator,
        SearchRoutingProfilesPaginator,
        SearchSecurityProfilesPaginator,
        SearchUserHierarchyGroupsPaginator,
        SearchUsersPaginator,
        SearchVocabulariesPaginator,
    )

    session = Session()
    client: ConnectClient = session.client("connect")

    get_metric_data_paginator: GetMetricDataPaginator = client.get_paginator("get_metric_data")
    list_agent_statuses_paginator: ListAgentStatusesPaginator = client.get_paginator("list_agent_statuses")
    list_approved_origins_paginator: ListApprovedOriginsPaginator = client.get_paginator("list_approved_origins")
    list_authentication_profiles_paginator: ListAuthenticationProfilesPaginator = client.get_paginator("list_authentication_profiles")
    list_bots_paginator: ListBotsPaginator = client.get_paginator("list_bots")
    list_contact_evaluations_paginator: ListContactEvaluationsPaginator = client.get_paginator("list_contact_evaluations")
    list_contact_flow_modules_paginator: ListContactFlowModulesPaginator = client.get_paginator("list_contact_flow_modules")
    list_contact_flow_versions_paginator: ListContactFlowVersionsPaginator = client.get_paginator("list_contact_flow_versions")
    list_contact_flows_paginator: ListContactFlowsPaginator = client.get_paginator("list_contact_flows")
    list_contact_references_paginator: ListContactReferencesPaginator = client.get_paginator("list_contact_references")
    list_default_vocabularies_paginator: ListDefaultVocabulariesPaginator = client.get_paginator("list_default_vocabularies")
    list_evaluation_form_versions_paginator: ListEvaluationFormVersionsPaginator = client.get_paginator("list_evaluation_form_versions")
    list_evaluation_forms_paginator: ListEvaluationFormsPaginator = client.get_paginator("list_evaluation_forms")
    list_flow_associations_paginator: ListFlowAssociationsPaginator = client.get_paginator("list_flow_associations")
    list_hours_of_operations_paginator: ListHoursOfOperationsPaginator = client.get_paginator("list_hours_of_operations")
    list_instance_attributes_paginator: ListInstanceAttributesPaginator = client.get_paginator("list_instance_attributes")
    list_instance_storage_configs_paginator: ListInstanceStorageConfigsPaginator = client.get_paginator("list_instance_storage_configs")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    list_integration_associations_paginator: ListIntegrationAssociationsPaginator = client.get_paginator("list_integration_associations")
    list_lambda_functions_paginator: ListLambdaFunctionsPaginator = client.get_paginator("list_lambda_functions")
    list_lex_bots_paginator: ListLexBotsPaginator = client.get_paginator("list_lex_bots")
    list_phone_numbers_paginator: ListPhoneNumbersPaginator = client.get_paginator("list_phone_numbers")
    list_phone_numbers_v2_paginator: ListPhoneNumbersV2Paginator = client.get_paginator("list_phone_numbers_v2")
    list_predefined_attributes_paginator: ListPredefinedAttributesPaginator = client.get_paginator("list_predefined_attributes")
    list_prompts_paginator: ListPromptsPaginator = client.get_paginator("list_prompts")
    list_queue_quick_connects_paginator: ListQueueQuickConnectsPaginator = client.get_paginator("list_queue_quick_connects")
    list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    list_quick_connects_paginator: ListQuickConnectsPaginator = client.get_paginator("list_quick_connects")
    list_routing_profile_queues_paginator: ListRoutingProfileQueuesPaginator = client.get_paginator("list_routing_profile_queues")
    list_routing_profiles_paginator: ListRoutingProfilesPaginator = client.get_paginator("list_routing_profiles")
    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    list_security_keys_paginator: ListSecurityKeysPaginator = client.get_paginator("list_security_keys")
    list_security_profile_applications_paginator: ListSecurityProfileApplicationsPaginator = client.get_paginator("list_security_profile_applications")
    list_security_profile_permissions_paginator: ListSecurityProfilePermissionsPaginator = client.get_paginator("list_security_profile_permissions")
    list_security_profiles_paginator: ListSecurityProfilesPaginator = client.get_paginator("list_security_profiles")
    list_task_templates_paginator: ListTaskTemplatesPaginator = client.get_paginator("list_task_templates")
    list_traffic_distribution_group_users_paginator: ListTrafficDistributionGroupUsersPaginator = client.get_paginator("list_traffic_distribution_group_users")
    list_traffic_distribution_groups_paginator: ListTrafficDistributionGroupsPaginator = client.get_paginator("list_traffic_distribution_groups")
    list_use_cases_paginator: ListUseCasesPaginator = client.get_paginator("list_use_cases")
    list_user_hierarchy_groups_paginator: ListUserHierarchyGroupsPaginator = client.get_paginator("list_user_hierarchy_groups")
    list_user_proficiencies_paginator: ListUserProficienciesPaginator = client.get_paginator("list_user_proficiencies")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    list_view_versions_paginator: ListViewVersionsPaginator = client.get_paginator("list_view_versions")
    list_views_paginator: ListViewsPaginator = client.get_paginator("list_views")
    search_agent_statuses_paginator: SearchAgentStatusesPaginator = client.get_paginator("search_agent_statuses")
    search_available_phone_numbers_paginator: SearchAvailablePhoneNumbersPaginator = client.get_paginator("search_available_phone_numbers")
    search_contact_flow_modules_paginator: SearchContactFlowModulesPaginator = client.get_paginator("search_contact_flow_modules")
    search_contact_flows_paginator: SearchContactFlowsPaginator = client.get_paginator("search_contact_flows")
    search_contacts_paginator: SearchContactsPaginator = client.get_paginator("search_contacts")
    search_hours_of_operations_paginator: SearchHoursOfOperationsPaginator = client.get_paginator("search_hours_of_operations")
    search_predefined_attributes_paginator: SearchPredefinedAttributesPaginator = client.get_paginator("search_predefined_attributes")
    search_prompts_paginator: SearchPromptsPaginator = client.get_paginator("search_prompts")
    search_queues_paginator: SearchQueuesPaginator = client.get_paginator("search_queues")
    search_quick_connects_paginator: SearchQuickConnectsPaginator = client.get_paginator("search_quick_connects")
    search_resource_tags_paginator: SearchResourceTagsPaginator = client.get_paginator("search_resource_tags")
    search_routing_profiles_paginator: SearchRoutingProfilesPaginator = client.get_paginator("search_routing_profiles")
    search_security_profiles_paginator: SearchSecurityProfilesPaginator = client.get_paginator("search_security_profiles")
    search_user_hierarchy_groups_paginator: SearchUserHierarchyGroupsPaginator = client.get_paginator("search_user_hierarchy_groups")
    search_users_paginator: SearchUsersPaginator = client.get_paginator("search_users")
    search_vocabularies_paginator: SearchVocabulariesPaginator = client.get_paginator("search_vocabularies")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetMetricDataRequestGetMetricDataPaginateTypeDef,
    GetMetricDataResponseTypeDef,
    ListAgentStatusRequestListAgentStatusesPaginateTypeDef,
    ListAgentStatusResponseTypeDef,
    ListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef,
    ListApprovedOriginsResponseTypeDef,
    ListAuthenticationProfilesRequestListAuthenticationProfilesPaginateTypeDef,
    ListAuthenticationProfilesResponseTypeDef,
    ListBotsRequestListBotsPaginateTypeDef,
    ListBotsResponseTypeDef,
    ListContactEvaluationsRequestListContactEvaluationsPaginateTypeDef,
    ListContactEvaluationsResponseTypeDef,
    ListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef,
    ListContactFlowModulesResponseTypeDef,
    ListContactFlowsRequestListContactFlowsPaginateTypeDef,
    ListContactFlowsResponseTypeDef,
    ListContactFlowVersionsRequestListContactFlowVersionsPaginateTypeDef,
    ListContactFlowVersionsResponseTypeDef,
    ListContactReferencesRequestListContactReferencesPaginateTypeDef,
    ListContactReferencesResponseTypeDef,
    ListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef,
    ListDefaultVocabulariesResponseTypeDef,
    ListEvaluationFormsRequestListEvaluationFormsPaginateTypeDef,
    ListEvaluationFormsResponseTypeDef,
    ListEvaluationFormVersionsRequestListEvaluationFormVersionsPaginateTypeDef,
    ListEvaluationFormVersionsResponseTypeDef,
    ListFlowAssociationsRequestListFlowAssociationsPaginateTypeDef,
    ListFlowAssociationsResponseTypeDef,
    ListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef,
    ListHoursOfOperationsResponseTypeDef,
    ListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef,
    ListInstanceAttributesResponseTypeDef,
    ListInstancesRequestListInstancesPaginateTypeDef,
    ListInstancesResponseTypeDef,
    ListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef,
    ListInstanceStorageConfigsResponseTypeDef,
    ListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef,
    ListIntegrationAssociationsResponseTypeDef,
    ListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef,
    ListLambdaFunctionsResponseTypeDef,
    ListLexBotsRequestListLexBotsPaginateTypeDef,
    ListLexBotsResponseTypeDef,
    ListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef,
    ListPhoneNumbersResponseTypeDef,
    ListPhoneNumbersV2RequestListPhoneNumbersV2PaginateTypeDef,
    ListPhoneNumbersV2ResponseTypeDef,
    ListPredefinedAttributesRequestListPredefinedAttributesPaginateTypeDef,
    ListPredefinedAttributesResponseTypeDef,
    ListPromptsRequestListPromptsPaginateTypeDef,
    ListPromptsResponseTypeDef,
    ListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef,
    ListQueueQuickConnectsResponseTypeDef,
    ListQueuesRequestListQueuesPaginateTypeDef,
    ListQueuesResponseTypeDef,
    ListQuickConnectsRequestListQuickConnectsPaginateTypeDef,
    ListQuickConnectsResponseTypeDef,
    ListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef,
    ListRoutingProfileQueuesResponseTypeDef,
    ListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef,
    ListRoutingProfilesResponseTypeDef,
    ListRulesRequestListRulesPaginateTypeDef,
    ListRulesResponseTypeDef,
    ListSecurityKeysRequestListSecurityKeysPaginateTypeDef,
    ListSecurityKeysResponseTypeDef,
    ListSecurityProfileApplicationsRequestListSecurityProfileApplicationsPaginateTypeDef,
    ListSecurityProfileApplicationsResponseTypeDef,
    ListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef,
    ListSecurityProfilePermissionsResponseTypeDef,
    ListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef,
    ListTaskTemplatesResponseTypeDef,
    ListTrafficDistributionGroupsRequestListTrafficDistributionGroupsPaginateTypeDef,
    ListTrafficDistributionGroupsResponseTypeDef,
    ListTrafficDistributionGroupUsersRequestListTrafficDistributionGroupUsersPaginateTypeDef,
    ListTrafficDistributionGroupUsersResponseTypeDef,
    ListUseCasesRequestListUseCasesPaginateTypeDef,
    ListUseCasesResponseTypeDef,
    ListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef,
    ListUserHierarchyGroupsResponseTypeDef,
    ListUserProficienciesRequestListUserProficienciesPaginateTypeDef,
    ListUserProficienciesResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
    ListViewsRequestListViewsPaginateTypeDef,
    ListViewsResponseTypeDef,
    ListViewVersionsRequestListViewVersionsPaginateTypeDef,
    ListViewVersionsResponseTypeDef,
    SearchAgentStatusesRequestSearchAgentStatusesPaginateTypeDef,
    SearchAgentStatusesResponseTypeDef,
    SearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef,
    SearchAvailablePhoneNumbersResponseTypeDef,
    SearchContactFlowModulesRequestSearchContactFlowModulesPaginateTypeDef,
    SearchContactFlowModulesResponseTypeDef,
    SearchContactFlowsRequestSearchContactFlowsPaginateTypeDef,
    SearchContactFlowsResponseTypeDef,
    SearchContactsRequestSearchContactsPaginateTypeDef,
    SearchContactsResponseTypeDef,
    SearchHoursOfOperationsRequestSearchHoursOfOperationsPaginateTypeDef,
    SearchHoursOfOperationsResponseTypeDef,
    SearchPredefinedAttributesRequestSearchPredefinedAttributesPaginateTypeDef,
    SearchPredefinedAttributesResponseTypeDef,
    SearchPromptsRequestSearchPromptsPaginateTypeDef,
    SearchPromptsResponseTypeDef,
    SearchQueuesRequestSearchQueuesPaginateTypeDef,
    SearchQueuesResponseTypeDef,
    SearchQuickConnectsRequestSearchQuickConnectsPaginateTypeDef,
    SearchQuickConnectsResponseTypeDef,
    SearchResourceTagsRequestSearchResourceTagsPaginateTypeDef,
    SearchResourceTagsResponseTypeDef,
    SearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef,
    SearchRoutingProfilesResponseTypeDef,
    SearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef,
    SearchSecurityProfilesResponseTypeDef,
    SearchUserHierarchyGroupsRequestSearchUserHierarchyGroupsPaginateTypeDef,
    SearchUserHierarchyGroupsResponseTypeDef,
    SearchUsersRequestSearchUsersPaginateTypeDef,
    SearchUsersResponseTypeDef,
    SearchVocabulariesRequestSearchVocabulariesPaginateTypeDef,
    SearchVocabulariesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetMetricDataPaginator",
    "ListAgentStatusesPaginator",
    "ListApprovedOriginsPaginator",
    "ListAuthenticationProfilesPaginator",
    "ListBotsPaginator",
    "ListContactEvaluationsPaginator",
    "ListContactFlowModulesPaginator",
    "ListContactFlowVersionsPaginator",
    "ListContactFlowsPaginator",
    "ListContactReferencesPaginator",
    "ListDefaultVocabulariesPaginator",
    "ListEvaluationFormVersionsPaginator",
    "ListEvaluationFormsPaginator",
    "ListFlowAssociationsPaginator",
    "ListHoursOfOperationsPaginator",
    "ListInstanceAttributesPaginator",
    "ListInstanceStorageConfigsPaginator",
    "ListInstancesPaginator",
    "ListIntegrationAssociationsPaginator",
    "ListLambdaFunctionsPaginator",
    "ListLexBotsPaginator",
    "ListPhoneNumbersPaginator",
    "ListPhoneNumbersV2Paginator",
    "ListPredefinedAttributesPaginator",
    "ListPromptsPaginator",
    "ListQueueQuickConnectsPaginator",
    "ListQueuesPaginator",
    "ListQuickConnectsPaginator",
    "ListRoutingProfileQueuesPaginator",
    "ListRoutingProfilesPaginator",
    "ListRulesPaginator",
    "ListSecurityKeysPaginator",
    "ListSecurityProfileApplicationsPaginator",
    "ListSecurityProfilePermissionsPaginator",
    "ListSecurityProfilesPaginator",
    "ListTaskTemplatesPaginator",
    "ListTrafficDistributionGroupUsersPaginator",
    "ListTrafficDistributionGroupsPaginator",
    "ListUseCasesPaginator",
    "ListUserHierarchyGroupsPaginator",
    "ListUserProficienciesPaginator",
    "ListUsersPaginator",
    "ListViewVersionsPaginator",
    "ListViewsPaginator",
    "SearchAgentStatusesPaginator",
    "SearchAvailablePhoneNumbersPaginator",
    "SearchContactFlowModulesPaginator",
    "SearchContactFlowsPaginator",
    "SearchContactsPaginator",
    "SearchHoursOfOperationsPaginator",
    "SearchPredefinedAttributesPaginator",
    "SearchPromptsPaginator",
    "SearchQueuesPaginator",
    "SearchQuickConnectsPaginator",
    "SearchResourceTagsPaginator",
    "SearchRoutingProfilesPaginator",
    "SearchSecurityProfilesPaginator",
    "SearchUserHierarchyGroupsPaginator",
    "SearchUsersPaginator",
    "SearchVocabulariesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetMetricDataPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/GetMetricData.html#Connect.Paginator.GetMetricData)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#getmetricdatapaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetMetricDataRequestGetMetricDataPaginateTypeDef]
    ) -> _PageIterator[GetMetricDataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/GetMetricData.html#Connect.Paginator.GetMetricData.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#getmetricdatapaginator)
        """


class ListAgentStatusesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAgentStatuses.html#Connect.Paginator.ListAgentStatuses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listagentstatusespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAgentStatusRequestListAgentStatusesPaginateTypeDef]
    ) -> _PageIterator[ListAgentStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAgentStatuses.html#Connect.Paginator.ListAgentStatuses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listagentstatusespaginator)
        """


class ListApprovedOriginsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListApprovedOrigins.html#Connect.Paginator.ListApprovedOrigins)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listapprovedoriginspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef]
    ) -> _PageIterator[ListApprovedOriginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListApprovedOrigins.html#Connect.Paginator.ListApprovedOrigins.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listapprovedoriginspaginator)
        """


class ListAuthenticationProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAuthenticationProfiles.html#Connect.Paginator.ListAuthenticationProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listauthenticationprofilespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAuthenticationProfilesRequestListAuthenticationProfilesPaginateTypeDef
        ],
    ) -> _PageIterator[ListAuthenticationProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAuthenticationProfiles.html#Connect.Paginator.ListAuthenticationProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listauthenticationprofilespaginator)
        """


class ListBotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListBots.html#Connect.Paginator.ListBots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listbotspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBotsRequestListBotsPaginateTypeDef]
    ) -> _PageIterator[ListBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListBots.html#Connect.Paginator.ListBots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listbotspaginator)
        """


class ListContactEvaluationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactEvaluations.html#Connect.Paginator.ListContactEvaluations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactevaluationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContactEvaluationsRequestListContactEvaluationsPaginateTypeDef]
    ) -> _PageIterator[ListContactEvaluationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactEvaluations.html#Connect.Paginator.ListContactEvaluations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactevaluationspaginator)
        """


class ListContactFlowModulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlowModules.html#Connect.Paginator.ListContactFlowModules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactflowmodulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef]
    ) -> _PageIterator[ListContactFlowModulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlowModules.html#Connect.Paginator.ListContactFlowModules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactflowmodulespaginator)
        """


class ListContactFlowVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlowVersions.html#Connect.Paginator.ListContactFlowVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactflowversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContactFlowVersionsRequestListContactFlowVersionsPaginateTypeDef]
    ) -> _PageIterator[ListContactFlowVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlowVersions.html#Connect.Paginator.ListContactFlowVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactflowversionspaginator)
        """


class ListContactFlowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlows.html#Connect.Paginator.ListContactFlows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactflowspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContactFlowsRequestListContactFlowsPaginateTypeDef]
    ) -> _PageIterator[ListContactFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlows.html#Connect.Paginator.ListContactFlows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactflowspaginator)
        """


class ListContactReferencesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactReferences.html#Connect.Paginator.ListContactReferences)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactreferencespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContactReferencesRequestListContactReferencesPaginateTypeDef]
    ) -> _PageIterator[ListContactReferencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactReferences.html#Connect.Paginator.ListContactReferences.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactreferencespaginator)
        """


class ListDefaultVocabulariesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListDefaultVocabularies.html#Connect.Paginator.ListDefaultVocabularies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listdefaultvocabulariespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef]
    ) -> _PageIterator[ListDefaultVocabulariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListDefaultVocabularies.html#Connect.Paginator.ListDefaultVocabularies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listdefaultvocabulariespaginator)
        """


class ListEvaluationFormVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListEvaluationFormVersions.html#Connect.Paginator.ListEvaluationFormVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listevaluationformversionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListEvaluationFormVersionsRequestListEvaluationFormVersionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListEvaluationFormVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListEvaluationFormVersions.html#Connect.Paginator.ListEvaluationFormVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listevaluationformversionspaginator)
        """


class ListEvaluationFormsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListEvaluationForms.html#Connect.Paginator.ListEvaluationForms)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listevaluationformspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEvaluationFormsRequestListEvaluationFormsPaginateTypeDef]
    ) -> _PageIterator[ListEvaluationFormsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListEvaluationForms.html#Connect.Paginator.ListEvaluationForms.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listevaluationformspaginator)
        """


class ListFlowAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListFlowAssociations.html#Connect.Paginator.ListFlowAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listflowassociationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFlowAssociationsRequestListFlowAssociationsPaginateTypeDef]
    ) -> _PageIterator[ListFlowAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListFlowAssociations.html#Connect.Paginator.ListFlowAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listflowassociationspaginator)
        """


class ListHoursOfOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListHoursOfOperations.html#Connect.Paginator.ListHoursOfOperations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listhoursofoperationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef]
    ) -> _PageIterator[ListHoursOfOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListHoursOfOperations.html#Connect.Paginator.ListHoursOfOperations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listhoursofoperationspaginator)
        """


class ListInstanceAttributesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstanceAttributes.html#Connect.Paginator.ListInstanceAttributes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listinstanceattributespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef]
    ) -> _PageIterator[ListInstanceAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstanceAttributes.html#Connect.Paginator.ListInstanceAttributes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listinstanceattributespaginator)
        """


class ListInstanceStorageConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstanceStorageConfigs.html#Connect.Paginator.ListInstanceStorageConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listinstancestorageconfigspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef
        ],
    ) -> _PageIterator[ListInstanceStorageConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstanceStorageConfigs.html#Connect.Paginator.ListInstanceStorageConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listinstancestorageconfigspaginator)
        """


class ListInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstances.html#Connect.Paginator.ListInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInstancesRequestListInstancesPaginateTypeDef]
    ) -> _PageIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstances.html#Connect.Paginator.ListInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listinstancespaginator)
        """


class ListIntegrationAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListIntegrationAssociations.html#Connect.Paginator.ListIntegrationAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listintegrationassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListIntegrationAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListIntegrationAssociations.html#Connect.Paginator.ListIntegrationAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listintegrationassociationspaginator)
        """


class ListLambdaFunctionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListLambdaFunctions.html#Connect.Paginator.ListLambdaFunctions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listlambdafunctionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef]
    ) -> _PageIterator[ListLambdaFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListLambdaFunctions.html#Connect.Paginator.ListLambdaFunctions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listlambdafunctionspaginator)
        """


class ListLexBotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListLexBots.html#Connect.Paginator.ListLexBots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listlexbotspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLexBotsRequestListLexBotsPaginateTypeDef]
    ) -> _PageIterator[ListLexBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListLexBots.html#Connect.Paginator.ListLexBots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listlexbotspaginator)
        """


class ListPhoneNumbersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPhoneNumbers.html#Connect.Paginator.ListPhoneNumbers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listphonenumberspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef]
    ) -> _PageIterator[ListPhoneNumbersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPhoneNumbers.html#Connect.Paginator.ListPhoneNumbers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listphonenumberspaginator)
        """


class ListPhoneNumbersV2Paginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPhoneNumbersV2.html#Connect.Paginator.ListPhoneNumbersV2)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listphonenumbersv2paginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPhoneNumbersV2RequestListPhoneNumbersV2PaginateTypeDef]
    ) -> _PageIterator[ListPhoneNumbersV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPhoneNumbersV2.html#Connect.Paginator.ListPhoneNumbersV2.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listphonenumbersv2paginator)
        """


class ListPredefinedAttributesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPredefinedAttributes.html#Connect.Paginator.ListPredefinedAttributes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listpredefinedattributespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListPredefinedAttributesRequestListPredefinedAttributesPaginateTypeDef],
    ) -> _PageIterator[ListPredefinedAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPredefinedAttributes.html#Connect.Paginator.ListPredefinedAttributes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listpredefinedattributespaginator)
        """


class ListPromptsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPrompts.html#Connect.Paginator.ListPrompts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listpromptspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPromptsRequestListPromptsPaginateTypeDef]
    ) -> _PageIterator[ListPromptsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPrompts.html#Connect.Paginator.ListPrompts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listpromptspaginator)
        """


class ListQueueQuickConnectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQueueQuickConnects.html#Connect.Paginator.ListQueueQuickConnects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listqueuequickconnectspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef]
    ) -> _PageIterator[ListQueueQuickConnectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQueueQuickConnects.html#Connect.Paginator.ListQueueQuickConnects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listqueuequickconnectspaginator)
        """


class ListQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQueues.html#Connect.Paginator.ListQueues)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listqueuespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListQueuesRequestListQueuesPaginateTypeDef]
    ) -> _PageIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQueues.html#Connect.Paginator.ListQueues.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listqueuespaginator)
        """


class ListQuickConnectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQuickConnects.html#Connect.Paginator.ListQuickConnects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listquickconnectspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListQuickConnectsRequestListQuickConnectsPaginateTypeDef]
    ) -> _PageIterator[ListQuickConnectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQuickConnects.html#Connect.Paginator.ListQuickConnects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listquickconnectspaginator)
        """


class ListRoutingProfileQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRoutingProfileQueues.html#Connect.Paginator.ListRoutingProfileQueues)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listroutingprofilequeuespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef],
    ) -> _PageIterator[ListRoutingProfileQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRoutingProfileQueues.html#Connect.Paginator.ListRoutingProfileQueues.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listroutingprofilequeuespaginator)
        """


class ListRoutingProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRoutingProfiles.html#Connect.Paginator.ListRoutingProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listroutingprofilespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef]
    ) -> _PageIterator[ListRoutingProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRoutingProfiles.html#Connect.Paginator.ListRoutingProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listroutingprofilespaginator)
        """


class ListRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRules.html#Connect.Paginator.ListRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRulesRequestListRulesPaginateTypeDef]
    ) -> _PageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRules.html#Connect.Paginator.ListRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listrulespaginator)
        """


class ListSecurityKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityKeys.html#Connect.Paginator.ListSecurityKeys)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecuritykeyspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSecurityKeysRequestListSecurityKeysPaginateTypeDef]
    ) -> _PageIterator[ListSecurityKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityKeys.html#Connect.Paginator.ListSecurityKeys.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecuritykeyspaginator)
        """


class ListSecurityProfileApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfileApplications.html#Connect.Paginator.ListSecurityProfileApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecurityprofileapplicationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListSecurityProfileApplicationsRequestListSecurityProfileApplicationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListSecurityProfileApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfileApplications.html#Connect.Paginator.ListSecurityProfileApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecurityprofileapplicationspaginator)
        """


class ListSecurityProfilePermissionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfilePermissions.html#Connect.Paginator.ListSecurityProfilePermissions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecurityprofilepermissionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListSecurityProfilePermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfilePermissions.html#Connect.Paginator.ListSecurityProfilePermissions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecurityprofilepermissionspaginator)
        """


class ListSecurityProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfiles.html#Connect.Paginator.ListSecurityProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecurityprofilespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef]
    ) -> _PageIterator[ListSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfiles.html#Connect.Paginator.ListSecurityProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecurityprofilespaginator)
        """


class ListTaskTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTaskTemplates.html#Connect.Paginator.ListTaskTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listtasktemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListTaskTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTaskTemplates.html#Connect.Paginator.ListTaskTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listtasktemplatespaginator)
        """


class ListTrafficDistributionGroupUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTrafficDistributionGroupUsers.html#Connect.Paginator.ListTrafficDistributionGroupUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listtrafficdistributiongroupuserspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListTrafficDistributionGroupUsersRequestListTrafficDistributionGroupUsersPaginateTypeDef
        ],
    ) -> _PageIterator[ListTrafficDistributionGroupUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTrafficDistributionGroupUsers.html#Connect.Paginator.ListTrafficDistributionGroupUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listtrafficdistributiongroupuserspaginator)
        """


class ListTrafficDistributionGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTrafficDistributionGroups.html#Connect.Paginator.ListTrafficDistributionGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listtrafficdistributiongroupspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListTrafficDistributionGroupsRequestListTrafficDistributionGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[ListTrafficDistributionGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTrafficDistributionGroups.html#Connect.Paginator.ListTrafficDistributionGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listtrafficdistributiongroupspaginator)
        """


class ListUseCasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUseCases.html#Connect.Paginator.ListUseCases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listusecasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUseCasesRequestListUseCasesPaginateTypeDef]
    ) -> _PageIterator[ListUseCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUseCases.html#Connect.Paginator.ListUseCases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listusecasespaginator)
        """


class ListUserHierarchyGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUserHierarchyGroups.html#Connect.Paginator.ListUserHierarchyGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listuserhierarchygroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef]
    ) -> _PageIterator[ListUserHierarchyGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUserHierarchyGroups.html#Connect.Paginator.ListUserHierarchyGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listuserhierarchygroupspaginator)
        """


class ListUserProficienciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUserProficiencies.html#Connect.Paginator.ListUserProficiencies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listuserproficienciespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUserProficienciesRequestListUserProficienciesPaginateTypeDef]
    ) -> _PageIterator[ListUserProficienciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUserProficiencies.html#Connect.Paginator.ListUserProficiencies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listuserproficienciespaginator)
        """


class ListUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUsers.html#Connect.Paginator.ListUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listuserspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> _PageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUsers.html#Connect.Paginator.ListUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listuserspaginator)
        """


class ListViewVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListViewVersions.html#Connect.Paginator.ListViewVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listviewversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListViewVersionsRequestListViewVersionsPaginateTypeDef]
    ) -> _PageIterator[ListViewVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListViewVersions.html#Connect.Paginator.ListViewVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listviewversionspaginator)
        """


class ListViewsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListViews.html#Connect.Paginator.ListViews)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listviewspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListViewsRequestListViewsPaginateTypeDef]
    ) -> _PageIterator[ListViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListViews.html#Connect.Paginator.ListViews.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listviewspaginator)
        """


class SearchAgentStatusesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchAgentStatuses.html#Connect.Paginator.SearchAgentStatuses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchagentstatusespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchAgentStatusesRequestSearchAgentStatusesPaginateTypeDef]
    ) -> _PageIterator[SearchAgentStatusesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchAgentStatuses.html#Connect.Paginator.SearchAgentStatuses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchagentstatusespaginator)
        """


class SearchAvailablePhoneNumbersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchAvailablePhoneNumbers.html#Connect.Paginator.SearchAvailablePhoneNumbers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchavailablephonenumberspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            SearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef
        ],
    ) -> _PageIterator[SearchAvailablePhoneNumbersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchAvailablePhoneNumbers.html#Connect.Paginator.SearchAvailablePhoneNumbers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchavailablephonenumberspaginator)
        """


class SearchContactFlowModulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContactFlowModules.html#Connect.Paginator.SearchContactFlowModules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchcontactflowmodulespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[SearchContactFlowModulesRequestSearchContactFlowModulesPaginateTypeDef],
    ) -> _PageIterator[SearchContactFlowModulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContactFlowModules.html#Connect.Paginator.SearchContactFlowModules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchcontactflowmodulespaginator)
        """


class SearchContactFlowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContactFlows.html#Connect.Paginator.SearchContactFlows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchcontactflowspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchContactFlowsRequestSearchContactFlowsPaginateTypeDef]
    ) -> _PageIterator[SearchContactFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContactFlows.html#Connect.Paginator.SearchContactFlows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchcontactflowspaginator)
        """


class SearchContactsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContacts.html#Connect.Paginator.SearchContacts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchcontactspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchContactsRequestSearchContactsPaginateTypeDef]
    ) -> _PageIterator[SearchContactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContacts.html#Connect.Paginator.SearchContacts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchcontactspaginator)
        """


class SearchHoursOfOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchHoursOfOperations.html#Connect.Paginator.SearchHoursOfOperations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchhoursofoperationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchHoursOfOperationsRequestSearchHoursOfOperationsPaginateTypeDef]
    ) -> _PageIterator[SearchHoursOfOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchHoursOfOperations.html#Connect.Paginator.SearchHoursOfOperations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchhoursofoperationspaginator)
        """


class SearchPredefinedAttributesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchPredefinedAttributes.html#Connect.Paginator.SearchPredefinedAttributes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchpredefinedattributespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            SearchPredefinedAttributesRequestSearchPredefinedAttributesPaginateTypeDef
        ],
    ) -> _PageIterator[SearchPredefinedAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchPredefinedAttributes.html#Connect.Paginator.SearchPredefinedAttributes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchpredefinedattributespaginator)
        """


class SearchPromptsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchPrompts.html#Connect.Paginator.SearchPrompts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchpromptspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchPromptsRequestSearchPromptsPaginateTypeDef]
    ) -> _PageIterator[SearchPromptsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchPrompts.html#Connect.Paginator.SearchPrompts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchpromptspaginator)
        """


class SearchQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchQueues.html#Connect.Paginator.SearchQueues)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchqueuespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchQueuesRequestSearchQueuesPaginateTypeDef]
    ) -> _PageIterator[SearchQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchQueues.html#Connect.Paginator.SearchQueues.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchqueuespaginator)
        """


class SearchQuickConnectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchQuickConnects.html#Connect.Paginator.SearchQuickConnects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchquickconnectspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchQuickConnectsRequestSearchQuickConnectsPaginateTypeDef]
    ) -> _PageIterator[SearchQuickConnectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchQuickConnects.html#Connect.Paginator.SearchQuickConnects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchquickconnectspaginator)
        """


class SearchResourceTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchResourceTags.html#Connect.Paginator.SearchResourceTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchresourcetagspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchResourceTagsRequestSearchResourceTagsPaginateTypeDef]
    ) -> _PageIterator[SearchResourceTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchResourceTags.html#Connect.Paginator.SearchResourceTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchresourcetagspaginator)
        """


class SearchRoutingProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchRoutingProfiles.html#Connect.Paginator.SearchRoutingProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchroutingprofilespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef]
    ) -> _PageIterator[SearchRoutingProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchRoutingProfiles.html#Connect.Paginator.SearchRoutingProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchroutingprofilespaginator)
        """


class SearchSecurityProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchSecurityProfiles.html#Connect.Paginator.SearchSecurityProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchsecurityprofilespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef]
    ) -> _PageIterator[SearchSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchSecurityProfiles.html#Connect.Paginator.SearchSecurityProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchsecurityprofilespaginator)
        """


class SearchUserHierarchyGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchUserHierarchyGroups.html#Connect.Paginator.SearchUserHierarchyGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchuserhierarchygroupspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[SearchUserHierarchyGroupsRequestSearchUserHierarchyGroupsPaginateTypeDef],
    ) -> _PageIterator[SearchUserHierarchyGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchUserHierarchyGroups.html#Connect.Paginator.SearchUserHierarchyGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchuserhierarchygroupspaginator)
        """


class SearchUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchUsers.html#Connect.Paginator.SearchUsers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchuserspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchUsersRequestSearchUsersPaginateTypeDef]
    ) -> _PageIterator[SearchUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchUsers.html#Connect.Paginator.SearchUsers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchuserspaginator)
        """


class SearchVocabulariesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchVocabularies.html#Connect.Paginator.SearchVocabularies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchvocabulariespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchVocabulariesRequestSearchVocabulariesPaginateTypeDef]
    ) -> _PageIterator[SearchVocabulariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchVocabularies.html#Connect.Paginator.SearchVocabularies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchvocabulariespaginator)
        """
