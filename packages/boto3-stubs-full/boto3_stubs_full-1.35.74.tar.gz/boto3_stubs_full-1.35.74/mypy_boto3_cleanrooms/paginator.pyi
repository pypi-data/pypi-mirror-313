"""
Type annotations for cleanrooms service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cleanrooms.client import CleanRoomsServiceClient
    from mypy_boto3_cleanrooms.paginator import (
        ListAnalysisTemplatesPaginator,
        ListCollaborationAnalysisTemplatesPaginator,
        ListCollaborationConfiguredAudienceModelAssociationsPaginator,
        ListCollaborationIdNamespaceAssociationsPaginator,
        ListCollaborationPrivacyBudgetTemplatesPaginator,
        ListCollaborationPrivacyBudgetsPaginator,
        ListCollaborationsPaginator,
        ListConfiguredAudienceModelAssociationsPaginator,
        ListConfiguredTableAssociationsPaginator,
        ListConfiguredTablesPaginator,
        ListIdMappingTablesPaginator,
        ListIdNamespaceAssociationsPaginator,
        ListMembersPaginator,
        ListMembershipsPaginator,
        ListPrivacyBudgetTemplatesPaginator,
        ListPrivacyBudgetsPaginator,
        ListProtectedQueriesPaginator,
        ListSchemasPaginator,
    )

    session = Session()
    client: CleanRoomsServiceClient = session.client("cleanrooms")

    list_analysis_templates_paginator: ListAnalysisTemplatesPaginator = client.get_paginator("list_analysis_templates")
    list_collaboration_analysis_templates_paginator: ListCollaborationAnalysisTemplatesPaginator = client.get_paginator("list_collaboration_analysis_templates")
    list_collaboration_configured_audience_model_associations_paginator: ListCollaborationConfiguredAudienceModelAssociationsPaginator = client.get_paginator("list_collaboration_configured_audience_model_associations")
    list_collaboration_id_namespace_associations_paginator: ListCollaborationIdNamespaceAssociationsPaginator = client.get_paginator("list_collaboration_id_namespace_associations")
    list_collaboration_privacy_budget_templates_paginator: ListCollaborationPrivacyBudgetTemplatesPaginator = client.get_paginator("list_collaboration_privacy_budget_templates")
    list_collaboration_privacy_budgets_paginator: ListCollaborationPrivacyBudgetsPaginator = client.get_paginator("list_collaboration_privacy_budgets")
    list_collaborations_paginator: ListCollaborationsPaginator = client.get_paginator("list_collaborations")
    list_configured_audience_model_associations_paginator: ListConfiguredAudienceModelAssociationsPaginator = client.get_paginator("list_configured_audience_model_associations")
    list_configured_table_associations_paginator: ListConfiguredTableAssociationsPaginator = client.get_paginator("list_configured_table_associations")
    list_configured_tables_paginator: ListConfiguredTablesPaginator = client.get_paginator("list_configured_tables")
    list_id_mapping_tables_paginator: ListIdMappingTablesPaginator = client.get_paginator("list_id_mapping_tables")
    list_id_namespace_associations_paginator: ListIdNamespaceAssociationsPaginator = client.get_paginator("list_id_namespace_associations")
    list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
    list_memberships_paginator: ListMembershipsPaginator = client.get_paginator("list_memberships")
    list_privacy_budget_templates_paginator: ListPrivacyBudgetTemplatesPaginator = client.get_paginator("list_privacy_budget_templates")
    list_privacy_budgets_paginator: ListPrivacyBudgetsPaginator = client.get_paginator("list_privacy_budgets")
    list_protected_queries_paginator: ListProtectedQueriesPaginator = client.get_paginator("list_protected_queries")
    list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef,
    ListAnalysisTemplatesOutputTypeDef,
    ListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef,
    ListCollaborationAnalysisTemplatesOutputTypeDef,
    ListCollaborationConfiguredAudienceModelAssociationsInputListCollaborationConfiguredAudienceModelAssociationsPaginateTypeDef,
    ListCollaborationConfiguredAudienceModelAssociationsOutputTypeDef,
    ListCollaborationIdNamespaceAssociationsInputListCollaborationIdNamespaceAssociationsPaginateTypeDef,
    ListCollaborationIdNamespaceAssociationsOutputTypeDef,
    ListCollaborationPrivacyBudgetsInputListCollaborationPrivacyBudgetsPaginateTypeDef,
    ListCollaborationPrivacyBudgetsOutputTypeDef,
    ListCollaborationPrivacyBudgetTemplatesInputListCollaborationPrivacyBudgetTemplatesPaginateTypeDef,
    ListCollaborationPrivacyBudgetTemplatesOutputTypeDef,
    ListCollaborationsInputListCollaborationsPaginateTypeDef,
    ListCollaborationsOutputTypeDef,
    ListConfiguredAudienceModelAssociationsInputListConfiguredAudienceModelAssociationsPaginateTypeDef,
    ListConfiguredAudienceModelAssociationsOutputTypeDef,
    ListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef,
    ListConfiguredTableAssociationsOutputTypeDef,
    ListConfiguredTablesInputListConfiguredTablesPaginateTypeDef,
    ListConfiguredTablesOutputTypeDef,
    ListIdMappingTablesInputListIdMappingTablesPaginateTypeDef,
    ListIdMappingTablesOutputTypeDef,
    ListIdNamespaceAssociationsInputListIdNamespaceAssociationsPaginateTypeDef,
    ListIdNamespaceAssociationsOutputTypeDef,
    ListMembershipsInputListMembershipsPaginateTypeDef,
    ListMembershipsOutputTypeDef,
    ListMembersInputListMembersPaginateTypeDef,
    ListMembersOutputTypeDef,
    ListPrivacyBudgetsInputListPrivacyBudgetsPaginateTypeDef,
    ListPrivacyBudgetsOutputTypeDef,
    ListPrivacyBudgetTemplatesInputListPrivacyBudgetTemplatesPaginateTypeDef,
    ListPrivacyBudgetTemplatesOutputTypeDef,
    ListProtectedQueriesInputListProtectedQueriesPaginateTypeDef,
    ListProtectedQueriesOutputTypeDef,
    ListSchemasInputListSchemasPaginateTypeDef,
    ListSchemasOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAnalysisTemplatesPaginator",
    "ListCollaborationAnalysisTemplatesPaginator",
    "ListCollaborationConfiguredAudienceModelAssociationsPaginator",
    "ListCollaborationIdNamespaceAssociationsPaginator",
    "ListCollaborationPrivacyBudgetTemplatesPaginator",
    "ListCollaborationPrivacyBudgetsPaginator",
    "ListCollaborationsPaginator",
    "ListConfiguredAudienceModelAssociationsPaginator",
    "ListConfiguredTableAssociationsPaginator",
    "ListConfiguredTablesPaginator",
    "ListIdMappingTablesPaginator",
    "ListIdNamespaceAssociationsPaginator",
    "ListMembersPaginator",
    "ListMembershipsPaginator",
    "ListPrivacyBudgetTemplatesPaginator",
    "ListPrivacyBudgetsPaginator",
    "ListProtectedQueriesPaginator",
    "ListSchemasPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAnalysisTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListAnalysisTemplates.html#CleanRoomsService.Paginator.ListAnalysisTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listanalysistemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListAnalysisTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListAnalysisTemplates.html#CleanRoomsService.Paginator.ListAnalysisTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listanalysistemplatespaginator)
        """

class ListCollaborationAnalysisTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationAnalysisTemplates.html#CleanRoomsService.Paginator.ListCollaborationAnalysisTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listcollaborationanalysistemplatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef
        ],
    ) -> _PageIterator[ListCollaborationAnalysisTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationAnalysisTemplates.html#CleanRoomsService.Paginator.ListCollaborationAnalysisTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listcollaborationanalysistemplatespaginator)
        """

class ListCollaborationConfiguredAudienceModelAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationConfiguredAudienceModelAssociations.html#CleanRoomsService.Paginator.ListCollaborationConfiguredAudienceModelAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listcollaborationconfiguredaudiencemodelassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCollaborationConfiguredAudienceModelAssociationsInputListCollaborationConfiguredAudienceModelAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCollaborationConfiguredAudienceModelAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationConfiguredAudienceModelAssociations.html#CleanRoomsService.Paginator.ListCollaborationConfiguredAudienceModelAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listcollaborationconfiguredaudiencemodelassociationspaginator)
        """

class ListCollaborationIdNamespaceAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationIdNamespaceAssociations.html#CleanRoomsService.Paginator.ListCollaborationIdNamespaceAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listcollaborationidnamespaceassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCollaborationIdNamespaceAssociationsInputListCollaborationIdNamespaceAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCollaborationIdNamespaceAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationIdNamespaceAssociations.html#CleanRoomsService.Paginator.ListCollaborationIdNamespaceAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listcollaborationidnamespaceassociationspaginator)
        """

class ListCollaborationPrivacyBudgetTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationPrivacyBudgetTemplates.html#CleanRoomsService.Paginator.ListCollaborationPrivacyBudgetTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listcollaborationprivacybudgettemplatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCollaborationPrivacyBudgetTemplatesInputListCollaborationPrivacyBudgetTemplatesPaginateTypeDef
        ],
    ) -> _PageIterator[ListCollaborationPrivacyBudgetTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationPrivacyBudgetTemplates.html#CleanRoomsService.Paginator.ListCollaborationPrivacyBudgetTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listcollaborationprivacybudgettemplatespaginator)
        """

class ListCollaborationPrivacyBudgetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationPrivacyBudgets.html#CleanRoomsService.Paginator.ListCollaborationPrivacyBudgets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listcollaborationprivacybudgetspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCollaborationPrivacyBudgetsInputListCollaborationPrivacyBudgetsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCollaborationPrivacyBudgetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborationPrivacyBudgets.html#CleanRoomsService.Paginator.ListCollaborationPrivacyBudgets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listcollaborationprivacybudgetspaginator)
        """

class ListCollaborationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborations.html#CleanRoomsService.Paginator.ListCollaborations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listcollaborationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCollaborationsInputListCollaborationsPaginateTypeDef]
    ) -> _PageIterator[ListCollaborationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListCollaborations.html#CleanRoomsService.Paginator.ListCollaborations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listcollaborationspaginator)
        """

class ListConfiguredAudienceModelAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListConfiguredAudienceModelAssociations.html#CleanRoomsService.Paginator.ListConfiguredAudienceModelAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listconfiguredaudiencemodelassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListConfiguredAudienceModelAssociationsInputListConfiguredAudienceModelAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListConfiguredAudienceModelAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListConfiguredAudienceModelAssociations.html#CleanRoomsService.Paginator.ListConfiguredAudienceModelAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listconfiguredaudiencemodelassociationspaginator)
        """

class ListConfiguredTableAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListConfiguredTableAssociations.html#CleanRoomsService.Paginator.ListConfiguredTableAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listconfiguredtableassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListConfiguredTableAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListConfiguredTableAssociations.html#CleanRoomsService.Paginator.ListConfiguredTableAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listconfiguredtableassociationspaginator)
        """

class ListConfiguredTablesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListConfiguredTables.html#CleanRoomsService.Paginator.ListConfiguredTables)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listconfiguredtablespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListConfiguredTablesInputListConfiguredTablesPaginateTypeDef]
    ) -> _PageIterator[ListConfiguredTablesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListConfiguredTables.html#CleanRoomsService.Paginator.ListConfiguredTables.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listconfiguredtablespaginator)
        """

class ListIdMappingTablesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListIdMappingTables.html#CleanRoomsService.Paginator.ListIdMappingTables)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listidmappingtablespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIdMappingTablesInputListIdMappingTablesPaginateTypeDef]
    ) -> _PageIterator[ListIdMappingTablesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListIdMappingTables.html#CleanRoomsService.Paginator.ListIdMappingTables.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listidmappingtablespaginator)
        """

class ListIdNamespaceAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListIdNamespaceAssociations.html#CleanRoomsService.Paginator.ListIdNamespaceAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listidnamespaceassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListIdNamespaceAssociationsInputListIdNamespaceAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListIdNamespaceAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListIdNamespaceAssociations.html#CleanRoomsService.Paginator.ListIdNamespaceAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listidnamespaceassociationspaginator)
        """

class ListMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListMembers.html#CleanRoomsService.Paginator.ListMembers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listmemberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMembersInputListMembersPaginateTypeDef]
    ) -> _PageIterator[ListMembersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListMembers.html#CleanRoomsService.Paginator.ListMembers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listmemberspaginator)
        """

class ListMembershipsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListMemberships.html#CleanRoomsService.Paginator.ListMemberships)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listmembershipspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMembershipsInputListMembershipsPaginateTypeDef]
    ) -> _PageIterator[ListMembershipsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListMemberships.html#CleanRoomsService.Paginator.ListMemberships.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listmembershipspaginator)
        """

class ListPrivacyBudgetTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListPrivacyBudgetTemplates.html#CleanRoomsService.Paginator.ListPrivacyBudgetTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listprivacybudgettemplatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListPrivacyBudgetTemplatesInputListPrivacyBudgetTemplatesPaginateTypeDef],
    ) -> _PageIterator[ListPrivacyBudgetTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListPrivacyBudgetTemplates.html#CleanRoomsService.Paginator.ListPrivacyBudgetTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listprivacybudgettemplatespaginator)
        """

class ListPrivacyBudgetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListPrivacyBudgets.html#CleanRoomsService.Paginator.ListPrivacyBudgets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listprivacybudgetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPrivacyBudgetsInputListPrivacyBudgetsPaginateTypeDef]
    ) -> _PageIterator[ListPrivacyBudgetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListPrivacyBudgets.html#CleanRoomsService.Paginator.ListPrivacyBudgets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listprivacybudgetspaginator)
        """

class ListProtectedQueriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListProtectedQueries.html#CleanRoomsService.Paginator.ListProtectedQueries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listprotectedqueriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProtectedQueriesInputListProtectedQueriesPaginateTypeDef]
    ) -> _PageIterator[ListProtectedQueriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListProtectedQueries.html#CleanRoomsService.Paginator.ListProtectedQueries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listprotectedqueriespaginator)
        """

class ListSchemasPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListSchemas.html#CleanRoomsService.Paginator.ListSchemas)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listschemaspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSchemasInputListSchemasPaginateTypeDef]
    ) -> _PageIterator[ListSchemasOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms/paginator/ListSchemas.html#CleanRoomsService.Paginator.ListSchemas.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanrooms/paginators/#listschemaspaginator)
        """
