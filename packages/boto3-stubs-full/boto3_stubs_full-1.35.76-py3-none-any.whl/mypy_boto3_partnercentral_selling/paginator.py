"""
Type annotations for partnercentral-selling service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_partnercentral_selling.client import PartnerCentralSellingAPIClient
    from mypy_boto3_partnercentral_selling.paginator import (
        ListEngagementByAcceptingInvitationTasksPaginator,
        ListEngagementFromOpportunityTasksPaginator,
        ListEngagementInvitationsPaginator,
        ListEngagementMembersPaginator,
        ListEngagementResourceAssociationsPaginator,
        ListEngagementsPaginator,
        ListOpportunitiesPaginator,
        ListResourceSnapshotJobsPaginator,
        ListResourceSnapshotsPaginator,
        ListSolutionsPaginator,
    )

    session = Session()
    client: PartnerCentralSellingAPIClient = session.client("partnercentral-selling")

    list_engagement_by_accepting_invitation_tasks_paginator: ListEngagementByAcceptingInvitationTasksPaginator = client.get_paginator("list_engagement_by_accepting_invitation_tasks")
    list_engagement_from_opportunity_tasks_paginator: ListEngagementFromOpportunityTasksPaginator = client.get_paginator("list_engagement_from_opportunity_tasks")
    list_engagement_invitations_paginator: ListEngagementInvitationsPaginator = client.get_paginator("list_engagement_invitations")
    list_engagement_members_paginator: ListEngagementMembersPaginator = client.get_paginator("list_engagement_members")
    list_engagement_resource_associations_paginator: ListEngagementResourceAssociationsPaginator = client.get_paginator("list_engagement_resource_associations")
    list_engagements_paginator: ListEngagementsPaginator = client.get_paginator("list_engagements")
    list_opportunities_paginator: ListOpportunitiesPaginator = client.get_paginator("list_opportunities")
    list_resource_snapshot_jobs_paginator: ListResourceSnapshotJobsPaginator = client.get_paginator("list_resource_snapshot_jobs")
    list_resource_snapshots_paginator: ListResourceSnapshotsPaginator = client.get_paginator("list_resource_snapshots")
    list_solutions_paginator: ListSolutionsPaginator = client.get_paginator("list_solutions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListEngagementByAcceptingInvitationTasksRequestListEngagementByAcceptingInvitationTasksPaginateTypeDef,
    ListEngagementByAcceptingInvitationTasksResponseTypeDef,
    ListEngagementFromOpportunityTasksRequestListEngagementFromOpportunityTasksPaginateTypeDef,
    ListEngagementFromOpportunityTasksResponseTypeDef,
    ListEngagementInvitationsRequestListEngagementInvitationsPaginateTypeDef,
    ListEngagementInvitationsResponseTypeDef,
    ListEngagementMembersRequestListEngagementMembersPaginateTypeDef,
    ListEngagementMembersResponseTypeDef,
    ListEngagementResourceAssociationsRequestListEngagementResourceAssociationsPaginateTypeDef,
    ListEngagementResourceAssociationsResponseTypeDef,
    ListEngagementsRequestListEngagementsPaginateTypeDef,
    ListEngagementsResponseTypeDef,
    ListOpportunitiesRequestListOpportunitiesPaginateTypeDef,
    ListOpportunitiesResponseTypeDef,
    ListResourceSnapshotJobsRequestListResourceSnapshotJobsPaginateTypeDef,
    ListResourceSnapshotJobsResponseTypeDef,
    ListResourceSnapshotsRequestListResourceSnapshotsPaginateTypeDef,
    ListResourceSnapshotsResponseTypeDef,
    ListSolutionsRequestListSolutionsPaginateTypeDef,
    ListSolutionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListEngagementByAcceptingInvitationTasksPaginator",
    "ListEngagementFromOpportunityTasksPaginator",
    "ListEngagementInvitationsPaginator",
    "ListEngagementMembersPaginator",
    "ListEngagementResourceAssociationsPaginator",
    "ListEngagementsPaginator",
    "ListOpportunitiesPaginator",
    "ListResourceSnapshotJobsPaginator",
    "ListResourceSnapshotsPaginator",
    "ListSolutionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEngagementByAcceptingInvitationTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementByAcceptingInvitationTasks.html#PartnerCentralSellingAPI.Paginator.ListEngagementByAcceptingInvitationTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementbyacceptinginvitationtaskspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListEngagementByAcceptingInvitationTasksRequestListEngagementByAcceptingInvitationTasksPaginateTypeDef
        ],
    ) -> _PageIterator[ListEngagementByAcceptingInvitationTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementByAcceptingInvitationTasks.html#PartnerCentralSellingAPI.Paginator.ListEngagementByAcceptingInvitationTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementbyacceptinginvitationtaskspaginator)
        """


class ListEngagementFromOpportunityTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementFromOpportunityTasks.html#PartnerCentralSellingAPI.Paginator.ListEngagementFromOpportunityTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementfromopportunitytaskspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListEngagementFromOpportunityTasksRequestListEngagementFromOpportunityTasksPaginateTypeDef
        ],
    ) -> _PageIterator[ListEngagementFromOpportunityTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementFromOpportunityTasks.html#PartnerCentralSellingAPI.Paginator.ListEngagementFromOpportunityTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementfromopportunitytaskspaginator)
        """


class ListEngagementInvitationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementInvitations.html#PartnerCentralSellingAPI.Paginator.ListEngagementInvitations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementinvitationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListEngagementInvitationsRequestListEngagementInvitationsPaginateTypeDef],
    ) -> _PageIterator[ListEngagementInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementInvitations.html#PartnerCentralSellingAPI.Paginator.ListEngagementInvitations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementinvitationspaginator)
        """


class ListEngagementMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementMembers.html#PartnerCentralSellingAPI.Paginator.ListEngagementMembers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementmemberspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEngagementMembersRequestListEngagementMembersPaginateTypeDef]
    ) -> _PageIterator[ListEngagementMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementMembers.html#PartnerCentralSellingAPI.Paginator.ListEngagementMembers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementmemberspaginator)
        """


class ListEngagementResourceAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementResourceAssociations.html#PartnerCentralSellingAPI.Paginator.ListEngagementResourceAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementresourceassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListEngagementResourceAssociationsRequestListEngagementResourceAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListEngagementResourceAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementResourceAssociations.html#PartnerCentralSellingAPI.Paginator.ListEngagementResourceAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementresourceassociationspaginator)
        """


class ListEngagementsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagements.html#PartnerCentralSellingAPI.Paginator.ListEngagements)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEngagementsRequestListEngagementsPaginateTypeDef]
    ) -> _PageIterator[ListEngagementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagements.html#PartnerCentralSellingAPI.Paginator.ListEngagements.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementspaginator)
        """


class ListOpportunitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListOpportunities.html#PartnerCentralSellingAPI.Paginator.ListOpportunities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listopportunitiespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOpportunitiesRequestListOpportunitiesPaginateTypeDef]
    ) -> _PageIterator[ListOpportunitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListOpportunities.html#PartnerCentralSellingAPI.Paginator.ListOpportunities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listopportunitiespaginator)
        """


class ListResourceSnapshotJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListResourceSnapshotJobs.html#PartnerCentralSellingAPI.Paginator.ListResourceSnapshotJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listresourcesnapshotjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListResourceSnapshotJobsRequestListResourceSnapshotJobsPaginateTypeDef],
    ) -> _PageIterator[ListResourceSnapshotJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListResourceSnapshotJobs.html#PartnerCentralSellingAPI.Paginator.ListResourceSnapshotJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listresourcesnapshotjobspaginator)
        """


class ListResourceSnapshotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListResourceSnapshots.html#PartnerCentralSellingAPI.Paginator.ListResourceSnapshots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listresourcesnapshotspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResourceSnapshotsRequestListResourceSnapshotsPaginateTypeDef]
    ) -> _PageIterator[ListResourceSnapshotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListResourceSnapshots.html#PartnerCentralSellingAPI.Paginator.ListResourceSnapshots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listresourcesnapshotspaginator)
        """


class ListSolutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListSolutions.html#PartnerCentralSellingAPI.Paginator.ListSolutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listsolutionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSolutionsRequestListSolutionsPaginateTypeDef]
    ) -> _PageIterator[ListSolutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListSolutions.html#PartnerCentralSellingAPI.Paginator.ListSolutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listsolutionspaginator)
        """
