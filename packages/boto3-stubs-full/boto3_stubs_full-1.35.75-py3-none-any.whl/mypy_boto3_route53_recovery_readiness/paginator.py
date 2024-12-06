"""
Type annotations for route53-recovery-readiness service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_route53_recovery_readiness.client import Route53RecoveryReadinessClient
    from mypy_boto3_route53_recovery_readiness.paginator import (
        GetCellReadinessSummaryPaginator,
        GetReadinessCheckResourceStatusPaginator,
        GetReadinessCheckStatusPaginator,
        GetRecoveryGroupReadinessSummaryPaginator,
        ListCellsPaginator,
        ListCrossAccountAuthorizationsPaginator,
        ListReadinessChecksPaginator,
        ListRecoveryGroupsPaginator,
        ListResourceSetsPaginator,
        ListRulesPaginator,
    )

    session = Session()
    client: Route53RecoveryReadinessClient = session.client("route53-recovery-readiness")

    get_cell_readiness_summary_paginator: GetCellReadinessSummaryPaginator = client.get_paginator("get_cell_readiness_summary")
    get_readiness_check_resource_status_paginator: GetReadinessCheckResourceStatusPaginator = client.get_paginator("get_readiness_check_resource_status")
    get_readiness_check_status_paginator: GetReadinessCheckStatusPaginator = client.get_paginator("get_readiness_check_status")
    get_recovery_group_readiness_summary_paginator: GetRecoveryGroupReadinessSummaryPaginator = client.get_paginator("get_recovery_group_readiness_summary")
    list_cells_paginator: ListCellsPaginator = client.get_paginator("list_cells")
    list_cross_account_authorizations_paginator: ListCrossAccountAuthorizationsPaginator = client.get_paginator("list_cross_account_authorizations")
    list_readiness_checks_paginator: ListReadinessChecksPaginator = client.get_paginator("list_readiness_checks")
    list_recovery_groups_paginator: ListRecoveryGroupsPaginator = client.get_paginator("list_recovery_groups")
    list_resource_sets_paginator: ListResourceSetsPaginator = client.get_paginator("list_resource_sets")
    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef,
    GetCellReadinessSummaryResponseTypeDef,
    GetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef,
    GetReadinessCheckResourceStatusResponseTypeDef,
    GetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef,
    GetReadinessCheckStatusResponseTypeDef,
    GetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef,
    GetRecoveryGroupReadinessSummaryResponseTypeDef,
    ListCellsRequestListCellsPaginateTypeDef,
    ListCellsResponseTypeDef,
    ListCrossAccountAuthorizationsRequestListCrossAccountAuthorizationsPaginateTypeDef,
    ListCrossAccountAuthorizationsResponseTypeDef,
    ListReadinessChecksRequestListReadinessChecksPaginateTypeDef,
    ListReadinessChecksResponseTypeDef,
    ListRecoveryGroupsRequestListRecoveryGroupsPaginateTypeDef,
    ListRecoveryGroupsResponseTypeDef,
    ListResourceSetsRequestListResourceSetsPaginateTypeDef,
    ListResourceSetsResponseTypeDef,
    ListRulesRequestListRulesPaginateTypeDef,
    ListRulesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetCellReadinessSummaryPaginator",
    "GetReadinessCheckResourceStatusPaginator",
    "GetReadinessCheckStatusPaginator",
    "GetRecoveryGroupReadinessSummaryPaginator",
    "ListCellsPaginator",
    "ListCrossAccountAuthorizationsPaginator",
    "ListReadinessChecksPaginator",
    "ListRecoveryGroupsPaginator",
    "ListResourceSetsPaginator",
    "ListRulesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetCellReadinessSummaryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetCellReadinessSummary.html#Route53RecoveryReadiness.Paginator.GetCellReadinessSummary)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getcellreadinesssummarypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef]
    ) -> _PageIterator[GetCellReadinessSummaryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetCellReadinessSummary.html#Route53RecoveryReadiness.Paginator.GetCellReadinessSummary.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getcellreadinesssummarypaginator)
        """


class GetReadinessCheckResourceStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetReadinessCheckResourceStatus.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckResourceStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getreadinesscheckresourcestatuspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef
        ],
    ) -> _PageIterator[GetReadinessCheckResourceStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetReadinessCheckResourceStatus.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckResourceStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getreadinesscheckresourcestatuspaginator)
        """


class GetReadinessCheckStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetReadinessCheckStatus.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getreadinesscheckstatuspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef]
    ) -> _PageIterator[GetReadinessCheckStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetReadinessCheckStatus.html#Route53RecoveryReadiness.Paginator.GetReadinessCheckStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getreadinesscheckstatuspaginator)
        """


class GetRecoveryGroupReadinessSummaryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetRecoveryGroupReadinessSummary.html#Route53RecoveryReadiness.Paginator.GetRecoveryGroupReadinessSummary)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getrecoverygroupreadinesssummarypaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef
        ],
    ) -> _PageIterator[GetRecoveryGroupReadinessSummaryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/GetRecoveryGroupReadinessSummary.html#Route53RecoveryReadiness.Paginator.GetRecoveryGroupReadinessSummary.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#getrecoverygroupreadinesssummarypaginator)
        """


class ListCellsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListCells.html#Route53RecoveryReadiness.Paginator.ListCells)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listcellspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCellsRequestListCellsPaginateTypeDef]
    ) -> _PageIterator[ListCellsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListCells.html#Route53RecoveryReadiness.Paginator.ListCells.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listcellspaginator)
        """


class ListCrossAccountAuthorizationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListCrossAccountAuthorizations.html#Route53RecoveryReadiness.Paginator.ListCrossAccountAuthorizations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listcrossaccountauthorizationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListCrossAccountAuthorizationsRequestListCrossAccountAuthorizationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCrossAccountAuthorizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListCrossAccountAuthorizations.html#Route53RecoveryReadiness.Paginator.ListCrossAccountAuthorizations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listcrossaccountauthorizationspaginator)
        """


class ListReadinessChecksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListReadinessChecks.html#Route53RecoveryReadiness.Paginator.ListReadinessChecks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listreadinesscheckspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReadinessChecksRequestListReadinessChecksPaginateTypeDef]
    ) -> _PageIterator[ListReadinessChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListReadinessChecks.html#Route53RecoveryReadiness.Paginator.ListReadinessChecks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listreadinesscheckspaginator)
        """


class ListRecoveryGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListRecoveryGroups.html#Route53RecoveryReadiness.Paginator.ListRecoveryGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listrecoverygroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRecoveryGroupsRequestListRecoveryGroupsPaginateTypeDef]
    ) -> _PageIterator[ListRecoveryGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListRecoveryGroups.html#Route53RecoveryReadiness.Paginator.ListRecoveryGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listrecoverygroupspaginator)
        """


class ListResourceSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListResourceSets.html#Route53RecoveryReadiness.Paginator.ListResourceSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listresourcesetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResourceSetsRequestListResourceSetsPaginateTypeDef]
    ) -> _PageIterator[ListResourceSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListResourceSets.html#Route53RecoveryReadiness.Paginator.ListResourceSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listresourcesetspaginator)
        """


class ListRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListRules.html#Route53RecoveryReadiness.Paginator.ListRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRulesRequestListRulesPaginateTypeDef]
    ) -> _PageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-readiness/paginator/ListRules.html#Route53RecoveryReadiness.Paginator.ListRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/paginators/#listrulespaginator)
        """
