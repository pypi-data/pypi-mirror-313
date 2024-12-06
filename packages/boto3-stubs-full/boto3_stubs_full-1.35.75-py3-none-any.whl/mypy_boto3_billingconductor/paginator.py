"""
Type annotations for billingconductor service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_billingconductor.client import BillingConductorClient
    from mypy_boto3_billingconductor.paginator import (
        ListAccountAssociationsPaginator,
        ListBillingGroupCostReportsPaginator,
        ListBillingGroupsPaginator,
        ListCustomLineItemVersionsPaginator,
        ListCustomLineItemsPaginator,
        ListPricingPlansAssociatedWithPricingRulePaginator,
        ListPricingPlansPaginator,
        ListPricingRulesAssociatedToPricingPlanPaginator,
        ListPricingRulesPaginator,
        ListResourcesAssociatedToCustomLineItemPaginator,
    )

    session = Session()
    client: BillingConductorClient = session.client("billingconductor")

    list_account_associations_paginator: ListAccountAssociationsPaginator = client.get_paginator("list_account_associations")
    list_billing_group_cost_reports_paginator: ListBillingGroupCostReportsPaginator = client.get_paginator("list_billing_group_cost_reports")
    list_billing_groups_paginator: ListBillingGroupsPaginator = client.get_paginator("list_billing_groups")
    list_custom_line_item_versions_paginator: ListCustomLineItemVersionsPaginator = client.get_paginator("list_custom_line_item_versions")
    list_custom_line_items_paginator: ListCustomLineItemsPaginator = client.get_paginator("list_custom_line_items")
    list_pricing_plans_associated_with_pricing_rule_paginator: ListPricingPlansAssociatedWithPricingRulePaginator = client.get_paginator("list_pricing_plans_associated_with_pricing_rule")
    list_pricing_plans_paginator: ListPricingPlansPaginator = client.get_paginator("list_pricing_plans")
    list_pricing_rules_associated_to_pricing_plan_paginator: ListPricingRulesAssociatedToPricingPlanPaginator = client.get_paginator("list_pricing_rules_associated_to_pricing_plan")
    list_pricing_rules_paginator: ListPricingRulesPaginator = client.get_paginator("list_pricing_rules")
    list_resources_associated_to_custom_line_item_paginator: ListResourcesAssociatedToCustomLineItemPaginator = client.get_paginator("list_resources_associated_to_custom_line_item")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAccountAssociationsInputListAccountAssociationsPaginateTypeDef,
    ListAccountAssociationsOutputTypeDef,
    ListBillingGroupCostReportsInputListBillingGroupCostReportsPaginateTypeDef,
    ListBillingGroupCostReportsOutputTypeDef,
    ListBillingGroupsInputListBillingGroupsPaginateTypeDef,
    ListBillingGroupsOutputTypeDef,
    ListCustomLineItemsInputListCustomLineItemsPaginateTypeDef,
    ListCustomLineItemsOutputTypeDef,
    ListCustomLineItemVersionsInputListCustomLineItemVersionsPaginateTypeDef,
    ListCustomLineItemVersionsOutputTypeDef,
    ListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef,
    ListPricingPlansAssociatedWithPricingRuleOutputTypeDef,
    ListPricingPlansInputListPricingPlansPaginateTypeDef,
    ListPricingPlansOutputTypeDef,
    ListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef,
    ListPricingRulesAssociatedToPricingPlanOutputTypeDef,
    ListPricingRulesInputListPricingRulesPaginateTypeDef,
    ListPricingRulesOutputTypeDef,
    ListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef,
    ListResourcesAssociatedToCustomLineItemOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAccountAssociationsPaginator",
    "ListBillingGroupCostReportsPaginator",
    "ListBillingGroupsPaginator",
    "ListCustomLineItemVersionsPaginator",
    "ListCustomLineItemsPaginator",
    "ListPricingPlansAssociatedWithPricingRulePaginator",
    "ListPricingPlansPaginator",
    "ListPricingRulesAssociatedToPricingPlanPaginator",
    "ListPricingRulesPaginator",
    "ListResourcesAssociatedToCustomLineItemPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccountAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListAccountAssociations.html#BillingConductor.Paginator.ListAccountAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listaccountassociationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAccountAssociationsInputListAccountAssociationsPaginateTypeDef]
    ) -> _PageIterator[ListAccountAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListAccountAssociations.html#BillingConductor.Paginator.ListAccountAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listaccountassociationspaginator)
        """


class ListBillingGroupCostReportsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListBillingGroupCostReports.html#BillingConductor.Paginator.ListBillingGroupCostReports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listbillinggroupcostreportspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListBillingGroupCostReportsInputListBillingGroupCostReportsPaginateTypeDef
        ],
    ) -> _PageIterator[ListBillingGroupCostReportsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListBillingGroupCostReports.html#BillingConductor.Paginator.ListBillingGroupCostReports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listbillinggroupcostreportspaginator)
        """


class ListBillingGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListBillingGroups.html#BillingConductor.Paginator.ListBillingGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listbillinggroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBillingGroupsInputListBillingGroupsPaginateTypeDef]
    ) -> _PageIterator[ListBillingGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListBillingGroups.html#BillingConductor.Paginator.ListBillingGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listbillinggroupspaginator)
        """


class ListCustomLineItemVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListCustomLineItemVersions.html#BillingConductor.Paginator.ListCustomLineItemVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listcustomlineitemversionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListCustomLineItemVersionsInputListCustomLineItemVersionsPaginateTypeDef],
    ) -> _PageIterator[ListCustomLineItemVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListCustomLineItemVersions.html#BillingConductor.Paginator.ListCustomLineItemVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listcustomlineitemversionspaginator)
        """


class ListCustomLineItemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListCustomLineItems.html#BillingConductor.Paginator.ListCustomLineItems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listcustomlineitemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCustomLineItemsInputListCustomLineItemsPaginateTypeDef]
    ) -> _PageIterator[ListCustomLineItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListCustomLineItems.html#BillingConductor.Paginator.ListCustomLineItems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listcustomlineitemspaginator)
        """


class ListPricingPlansAssociatedWithPricingRulePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingPlansAssociatedWithPricingRule.html#BillingConductor.Paginator.ListPricingPlansAssociatedWithPricingRule)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingplansassociatedwithpricingrulepaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef
        ],
    ) -> _PageIterator[ListPricingPlansAssociatedWithPricingRuleOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingPlansAssociatedWithPricingRule.html#BillingConductor.Paginator.ListPricingPlansAssociatedWithPricingRule.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingplansassociatedwithpricingrulepaginator)
        """


class ListPricingPlansPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingPlans.html#BillingConductor.Paginator.ListPricingPlans)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingplanspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPricingPlansInputListPricingPlansPaginateTypeDef]
    ) -> _PageIterator[ListPricingPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingPlans.html#BillingConductor.Paginator.ListPricingPlans.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingplanspaginator)
        """


class ListPricingRulesAssociatedToPricingPlanPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingRulesAssociatedToPricingPlan.html#BillingConductor.Paginator.ListPricingRulesAssociatedToPricingPlan)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingrulesassociatedtopricingplanpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef
        ],
    ) -> _PageIterator[ListPricingRulesAssociatedToPricingPlanOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingRulesAssociatedToPricingPlan.html#BillingConductor.Paginator.ListPricingRulesAssociatedToPricingPlan.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingrulesassociatedtopricingplanpaginator)
        """


class ListPricingRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingRules.html#BillingConductor.Paginator.ListPricingRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPricingRulesInputListPricingRulesPaginateTypeDef]
    ) -> _PageIterator[ListPricingRulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingRules.html#BillingConductor.Paginator.ListPricingRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listpricingrulespaginator)
        """


class ListResourcesAssociatedToCustomLineItemPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListResourcesAssociatedToCustomLineItem.html#BillingConductor.Paginator.ListResourcesAssociatedToCustomLineItem)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listresourcesassociatedtocustomlineitempaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef
        ],
    ) -> _PageIterator[ListResourcesAssociatedToCustomLineItemOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListResourcesAssociatedToCustomLineItem.html#BillingConductor.Paginator.ListResourcesAssociatedToCustomLineItem.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/paginators/#listresourcesassociatedtocustomlineitempaginator)
        """
