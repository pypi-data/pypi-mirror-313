"""
Type annotations for bcm-pricing-calculator service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_bcm_pricing_calculator.client import BillingandCostManagementPricingCalculatorClient
    from mypy_boto3_bcm_pricing_calculator.paginator import (
        ListBillEstimateCommitmentsPaginator,
        ListBillEstimateInputCommitmentModificationsPaginator,
        ListBillEstimateInputUsageModificationsPaginator,
        ListBillEstimateLineItemsPaginator,
        ListBillEstimatesPaginator,
        ListBillScenarioCommitmentModificationsPaginator,
        ListBillScenarioUsageModificationsPaginator,
        ListBillScenariosPaginator,
        ListWorkloadEstimateUsagePaginator,
        ListWorkloadEstimatesPaginator,
    )

    session = Session()
    client: BillingandCostManagementPricingCalculatorClient = session.client("bcm-pricing-calculator")

    list_bill_estimate_commitments_paginator: ListBillEstimateCommitmentsPaginator = client.get_paginator("list_bill_estimate_commitments")
    list_bill_estimate_input_commitment_modifications_paginator: ListBillEstimateInputCommitmentModificationsPaginator = client.get_paginator("list_bill_estimate_input_commitment_modifications")
    list_bill_estimate_input_usage_modifications_paginator: ListBillEstimateInputUsageModificationsPaginator = client.get_paginator("list_bill_estimate_input_usage_modifications")
    list_bill_estimate_line_items_paginator: ListBillEstimateLineItemsPaginator = client.get_paginator("list_bill_estimate_line_items")
    list_bill_estimates_paginator: ListBillEstimatesPaginator = client.get_paginator("list_bill_estimates")
    list_bill_scenario_commitment_modifications_paginator: ListBillScenarioCommitmentModificationsPaginator = client.get_paginator("list_bill_scenario_commitment_modifications")
    list_bill_scenario_usage_modifications_paginator: ListBillScenarioUsageModificationsPaginator = client.get_paginator("list_bill_scenario_usage_modifications")
    list_bill_scenarios_paginator: ListBillScenariosPaginator = client.get_paginator("list_bill_scenarios")
    list_workload_estimate_usage_paginator: ListWorkloadEstimateUsagePaginator = client.get_paginator("list_workload_estimate_usage")
    list_workload_estimates_paginator: ListWorkloadEstimatesPaginator = client.get_paginator("list_workload_estimates")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListBillEstimateCommitmentsRequestListBillEstimateCommitmentsPaginateTypeDef,
    ListBillEstimateCommitmentsResponseTypeDef,
    ListBillEstimateInputCommitmentModificationsRequestListBillEstimateInputCommitmentModificationsPaginateTypeDef,
    ListBillEstimateInputCommitmentModificationsResponseTypeDef,
    ListBillEstimateInputUsageModificationsRequestListBillEstimateInputUsageModificationsPaginateTypeDef,
    ListBillEstimateInputUsageModificationsResponsePaginatorTypeDef,
    ListBillEstimateLineItemsRequestListBillEstimateLineItemsPaginateTypeDef,
    ListBillEstimateLineItemsResponseTypeDef,
    ListBillEstimatesRequestListBillEstimatesPaginateTypeDef,
    ListBillEstimatesResponseTypeDef,
    ListBillScenarioCommitmentModificationsRequestListBillScenarioCommitmentModificationsPaginateTypeDef,
    ListBillScenarioCommitmentModificationsResponseTypeDef,
    ListBillScenariosRequestListBillScenariosPaginateTypeDef,
    ListBillScenariosResponseTypeDef,
    ListBillScenarioUsageModificationsRequestListBillScenarioUsageModificationsPaginateTypeDef,
    ListBillScenarioUsageModificationsResponsePaginatorTypeDef,
    ListWorkloadEstimatesRequestListWorkloadEstimatesPaginateTypeDef,
    ListWorkloadEstimatesResponseTypeDef,
    ListWorkloadEstimateUsageRequestListWorkloadEstimateUsagePaginateTypeDef,
    ListWorkloadEstimateUsageResponsePaginatorTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListBillEstimateCommitmentsPaginator",
    "ListBillEstimateInputCommitmentModificationsPaginator",
    "ListBillEstimateInputUsageModificationsPaginator",
    "ListBillEstimateLineItemsPaginator",
    "ListBillEstimatesPaginator",
    "ListBillScenarioCommitmentModificationsPaginator",
    "ListBillScenarioUsageModificationsPaginator",
    "ListBillScenariosPaginator",
    "ListWorkloadEstimateUsagePaginator",
    "ListWorkloadEstimatesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListBillEstimateCommitmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillEstimateCommitments.html#BillingandCostManagementPricingCalculator.Paginator.ListBillEstimateCommitments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillestimatecommitmentspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListBillEstimateCommitmentsRequestListBillEstimateCommitmentsPaginateTypeDef
        ],
    ) -> _PageIterator[ListBillEstimateCommitmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillEstimateCommitments.html#BillingandCostManagementPricingCalculator.Paginator.ListBillEstimateCommitments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillestimatecommitmentspaginator)
        """

class ListBillEstimateInputCommitmentModificationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillEstimateInputCommitmentModifications.html#BillingandCostManagementPricingCalculator.Paginator.ListBillEstimateInputCommitmentModifications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillestimateinputcommitmentmodificationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListBillEstimateInputCommitmentModificationsRequestListBillEstimateInputCommitmentModificationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListBillEstimateInputCommitmentModificationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillEstimateInputCommitmentModifications.html#BillingandCostManagementPricingCalculator.Paginator.ListBillEstimateInputCommitmentModifications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillestimateinputcommitmentmodificationspaginator)
        """

class ListBillEstimateInputUsageModificationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillEstimateInputUsageModifications.html#BillingandCostManagementPricingCalculator.Paginator.ListBillEstimateInputUsageModifications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillestimateinputusagemodificationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListBillEstimateInputUsageModificationsRequestListBillEstimateInputUsageModificationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListBillEstimateInputUsageModificationsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillEstimateInputUsageModifications.html#BillingandCostManagementPricingCalculator.Paginator.ListBillEstimateInputUsageModifications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillestimateinputusagemodificationspaginator)
        """

class ListBillEstimateLineItemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillEstimateLineItems.html#BillingandCostManagementPricingCalculator.Paginator.ListBillEstimateLineItems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillestimatelineitemspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListBillEstimateLineItemsRequestListBillEstimateLineItemsPaginateTypeDef],
    ) -> _PageIterator[ListBillEstimateLineItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillEstimateLineItems.html#BillingandCostManagementPricingCalculator.Paginator.ListBillEstimateLineItems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillestimatelineitemspaginator)
        """

class ListBillEstimatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillEstimates.html#BillingandCostManagementPricingCalculator.Paginator.ListBillEstimates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillestimatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBillEstimatesRequestListBillEstimatesPaginateTypeDef]
    ) -> _PageIterator[ListBillEstimatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillEstimates.html#BillingandCostManagementPricingCalculator.Paginator.ListBillEstimates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillestimatespaginator)
        """

class ListBillScenarioCommitmentModificationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillScenarioCommitmentModifications.html#BillingandCostManagementPricingCalculator.Paginator.ListBillScenarioCommitmentModifications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillscenariocommitmentmodificationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListBillScenarioCommitmentModificationsRequestListBillScenarioCommitmentModificationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListBillScenarioCommitmentModificationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillScenarioCommitmentModifications.html#BillingandCostManagementPricingCalculator.Paginator.ListBillScenarioCommitmentModifications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillscenariocommitmentmodificationspaginator)
        """

class ListBillScenarioUsageModificationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillScenarioUsageModifications.html#BillingandCostManagementPricingCalculator.Paginator.ListBillScenarioUsageModifications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillscenariousagemodificationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListBillScenarioUsageModificationsRequestListBillScenarioUsageModificationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListBillScenarioUsageModificationsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillScenarioUsageModifications.html#BillingandCostManagementPricingCalculator.Paginator.ListBillScenarioUsageModifications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillscenariousagemodificationspaginator)
        """

class ListBillScenariosPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillScenarios.html#BillingandCostManagementPricingCalculator.Paginator.ListBillScenarios)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillscenariospaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBillScenariosRequestListBillScenariosPaginateTypeDef]
    ) -> _PageIterator[ListBillScenariosResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListBillScenarios.html#BillingandCostManagementPricingCalculator.Paginator.ListBillScenarios.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listbillscenariospaginator)
        """

class ListWorkloadEstimateUsagePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListWorkloadEstimateUsage.html#BillingandCostManagementPricingCalculator.Paginator.ListWorkloadEstimateUsage)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listworkloadestimateusagepaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListWorkloadEstimateUsageRequestListWorkloadEstimateUsagePaginateTypeDef],
    ) -> _PageIterator[ListWorkloadEstimateUsageResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListWorkloadEstimateUsage.html#BillingandCostManagementPricingCalculator.Paginator.ListWorkloadEstimateUsage.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listworkloadestimateusagepaginator)
        """

class ListWorkloadEstimatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListWorkloadEstimates.html#BillingandCostManagementPricingCalculator.Paginator.ListWorkloadEstimates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listworkloadestimatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWorkloadEstimatesRequestListWorkloadEstimatesPaginateTypeDef]
    ) -> _PageIterator[ListWorkloadEstimatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/paginator/ListWorkloadEstimates.html#BillingandCostManagementPricingCalculator.Paginator.ListWorkloadEstimates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/paginators/#listworkloadestimatespaginator)
        """
