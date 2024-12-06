"""
Type annotations for partnercentral-selling service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_partnercentral_selling.client import PartnerCentralSellingAPIClient
    from mypy_boto3_partnercentral_selling.paginator import (
        ListEngagementInvitationsPaginator,
        ListOpportunitiesPaginator,
        ListSolutionsPaginator,
    )

    session = Session()
    client: PartnerCentralSellingAPIClient = session.client("partnercentral-selling")

    list_engagement_invitations_paginator: ListEngagementInvitationsPaginator = client.get_paginator("list_engagement_invitations")
    list_opportunities_paginator: ListOpportunitiesPaginator = client.get_paginator("list_opportunities")
    list_solutions_paginator: ListSolutionsPaginator = client.get_paginator("list_solutions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListEngagementInvitationsRequestListEngagementInvitationsPaginateTypeDef,
    ListEngagementInvitationsResponseTypeDef,
    ListOpportunitiesRequestListOpportunitiesPaginateTypeDef,
    ListOpportunitiesResponseTypeDef,
    ListSolutionsRequestListSolutionsPaginateTypeDef,
    ListSolutionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListEngagementInvitationsPaginator",
    "ListOpportunitiesPaginator",
    "ListSolutionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
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
