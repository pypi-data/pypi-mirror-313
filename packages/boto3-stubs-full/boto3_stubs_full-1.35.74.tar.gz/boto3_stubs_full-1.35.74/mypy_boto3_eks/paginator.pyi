"""
Type annotations for eks service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_eks.client import EKSClient
    from mypy_boto3_eks.paginator import (
        DescribeAddonVersionsPaginator,
        ListAccessEntriesPaginator,
        ListAccessPoliciesPaginator,
        ListAddonsPaginator,
        ListAssociatedAccessPoliciesPaginator,
        ListClustersPaginator,
        ListEksAnywhereSubscriptionsPaginator,
        ListFargateProfilesPaginator,
        ListIdentityProviderConfigsPaginator,
        ListInsightsPaginator,
        ListNodegroupsPaginator,
        ListPodIdentityAssociationsPaginator,
        ListUpdatesPaginator,
    )

    session = Session()
    client: EKSClient = session.client("eks")

    describe_addon_versions_paginator: DescribeAddonVersionsPaginator = client.get_paginator("describe_addon_versions")
    list_access_entries_paginator: ListAccessEntriesPaginator = client.get_paginator("list_access_entries")
    list_access_policies_paginator: ListAccessPoliciesPaginator = client.get_paginator("list_access_policies")
    list_addons_paginator: ListAddonsPaginator = client.get_paginator("list_addons")
    list_associated_access_policies_paginator: ListAssociatedAccessPoliciesPaginator = client.get_paginator("list_associated_access_policies")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_eks_anywhere_subscriptions_paginator: ListEksAnywhereSubscriptionsPaginator = client.get_paginator("list_eks_anywhere_subscriptions")
    list_fargate_profiles_paginator: ListFargateProfilesPaginator = client.get_paginator("list_fargate_profiles")
    list_identity_provider_configs_paginator: ListIdentityProviderConfigsPaginator = client.get_paginator("list_identity_provider_configs")
    list_insights_paginator: ListInsightsPaginator = client.get_paginator("list_insights")
    list_nodegroups_paginator: ListNodegroupsPaginator = client.get_paginator("list_nodegroups")
    list_pod_identity_associations_paginator: ListPodIdentityAssociationsPaginator = client.get_paginator("list_pod_identity_associations")
    list_updates_paginator: ListUpdatesPaginator = client.get_paginator("list_updates")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAddonVersionsRequestDescribeAddonVersionsPaginateTypeDef,
    DescribeAddonVersionsResponseTypeDef,
    ListAccessEntriesRequestListAccessEntriesPaginateTypeDef,
    ListAccessEntriesResponseTypeDef,
    ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef,
    ListAccessPoliciesResponseTypeDef,
    ListAddonsRequestListAddonsPaginateTypeDef,
    ListAddonsResponseTypeDef,
    ListAssociatedAccessPoliciesRequestListAssociatedAccessPoliciesPaginateTypeDef,
    ListAssociatedAccessPoliciesResponseTypeDef,
    ListClustersRequestListClustersPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListEksAnywhereSubscriptionsRequestListEksAnywhereSubscriptionsPaginateTypeDef,
    ListEksAnywhereSubscriptionsResponseTypeDef,
    ListFargateProfilesRequestListFargateProfilesPaginateTypeDef,
    ListFargateProfilesResponseTypeDef,
    ListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef,
    ListIdentityProviderConfigsResponseTypeDef,
    ListInsightsRequestListInsightsPaginateTypeDef,
    ListInsightsResponseTypeDef,
    ListNodegroupsRequestListNodegroupsPaginateTypeDef,
    ListNodegroupsResponseTypeDef,
    ListPodIdentityAssociationsRequestListPodIdentityAssociationsPaginateTypeDef,
    ListPodIdentityAssociationsResponseTypeDef,
    ListUpdatesRequestListUpdatesPaginateTypeDef,
    ListUpdatesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAddonVersionsPaginator",
    "ListAccessEntriesPaginator",
    "ListAccessPoliciesPaginator",
    "ListAddonsPaginator",
    "ListAssociatedAccessPoliciesPaginator",
    "ListClustersPaginator",
    "ListEksAnywhereSubscriptionsPaginator",
    "ListFargateProfilesPaginator",
    "ListIdentityProviderConfigsPaginator",
    "ListInsightsPaginator",
    "ListNodegroupsPaginator",
    "ListPodIdentityAssociationsPaginator",
    "ListUpdatesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAddonVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/DescribeAddonVersions.html#EKS.Paginator.DescribeAddonVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#describeaddonversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeAddonVersionsRequestDescribeAddonVersionsPaginateTypeDef]
    ) -> _PageIterator[DescribeAddonVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/DescribeAddonVersions.html#EKS.Paginator.DescribeAddonVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#describeaddonversionspaginator)
        """

class ListAccessEntriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAccessEntries.html#EKS.Paginator.ListAccessEntries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listaccessentriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccessEntriesRequestListAccessEntriesPaginateTypeDef]
    ) -> _PageIterator[ListAccessEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAccessEntries.html#EKS.Paginator.ListAccessEntries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listaccessentriespaginator)
        """

class ListAccessPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAccessPolicies.html#EKS.Paginator.ListAccessPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listaccesspoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListAccessPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAccessPolicies.html#EKS.Paginator.ListAccessPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listaccesspoliciespaginator)
        """

class ListAddonsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAddons.html#EKS.Paginator.ListAddons)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listaddonspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAddonsRequestListAddonsPaginateTypeDef]
    ) -> _PageIterator[ListAddonsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAddons.html#EKS.Paginator.ListAddons.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listaddonspaginator)
        """

class ListAssociatedAccessPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAssociatedAccessPolicies.html#EKS.Paginator.ListAssociatedAccessPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listassociatedaccesspoliciespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAssociatedAccessPoliciesRequestListAssociatedAccessPoliciesPaginateTypeDef
        ],
    ) -> _PageIterator[ListAssociatedAccessPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAssociatedAccessPolicies.html#EKS.Paginator.ListAssociatedAccessPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listassociatedaccesspoliciespaginator)
        """

class ListClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListClusters.html#EKS.Paginator.ListClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClustersRequestListClustersPaginateTypeDef]
    ) -> _PageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListClusters.html#EKS.Paginator.ListClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listclusterspaginator)
        """

class ListEksAnywhereSubscriptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListEksAnywhereSubscriptions.html#EKS.Paginator.ListEksAnywhereSubscriptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listeksanywheresubscriptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListEksAnywhereSubscriptionsRequestListEksAnywhereSubscriptionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListEksAnywhereSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListEksAnywhereSubscriptions.html#EKS.Paginator.ListEksAnywhereSubscriptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listeksanywheresubscriptionspaginator)
        """

class ListFargateProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListFargateProfiles.html#EKS.Paginator.ListFargateProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listfargateprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFargateProfilesRequestListFargateProfilesPaginateTypeDef]
    ) -> _PageIterator[ListFargateProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListFargateProfiles.html#EKS.Paginator.ListFargateProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listfargateprofilespaginator)
        """

class ListIdentityProviderConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListIdentityProviderConfigs.html#EKS.Paginator.ListIdentityProviderConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listidentityproviderconfigspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef
        ],
    ) -> _PageIterator[ListIdentityProviderConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListIdentityProviderConfigs.html#EKS.Paginator.ListIdentityProviderConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listidentityproviderconfigspaginator)
        """

class ListInsightsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListInsights.html#EKS.Paginator.ListInsights)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listinsightspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInsightsRequestListInsightsPaginateTypeDef]
    ) -> _PageIterator[ListInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListInsights.html#EKS.Paginator.ListInsights.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listinsightspaginator)
        """

class ListNodegroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListNodegroups.html#EKS.Paginator.ListNodegroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listnodegroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNodegroupsRequestListNodegroupsPaginateTypeDef]
    ) -> _PageIterator[ListNodegroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListNodegroups.html#EKS.Paginator.ListNodegroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listnodegroupspaginator)
        """

class ListPodIdentityAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListPodIdentityAssociations.html#EKS.Paginator.ListPodIdentityAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listpodidentityassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListPodIdentityAssociationsRequestListPodIdentityAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListPodIdentityAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListPodIdentityAssociations.html#EKS.Paginator.ListPodIdentityAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listpodidentityassociationspaginator)
        """

class ListUpdatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListUpdates.html#EKS.Paginator.ListUpdates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listupdatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUpdatesRequestListUpdatesPaginateTypeDef]
    ) -> _PageIterator[ListUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListUpdates.html#EKS.Paginator.ListUpdates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eks/paginators/#listupdatespaginator)
        """
