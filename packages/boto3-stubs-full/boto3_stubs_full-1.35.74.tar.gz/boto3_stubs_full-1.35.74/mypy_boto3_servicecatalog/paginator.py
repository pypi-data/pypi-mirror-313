"""
Type annotations for servicecatalog service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_servicecatalog.client import ServiceCatalogClient
    from mypy_boto3_servicecatalog.paginator import (
        ListAcceptedPortfolioSharesPaginator,
        ListConstraintsForPortfolioPaginator,
        ListLaunchPathsPaginator,
        ListOrganizationPortfolioAccessPaginator,
        ListPortfoliosForProductPaginator,
        ListPortfoliosPaginator,
        ListPrincipalsForPortfolioPaginator,
        ListProvisionedProductPlansPaginator,
        ListProvisioningArtifactsForServiceActionPaginator,
        ListRecordHistoryPaginator,
        ListResourcesForTagOptionPaginator,
        ListServiceActionsForProvisioningArtifactPaginator,
        ListServiceActionsPaginator,
        ListTagOptionsPaginator,
        ScanProvisionedProductsPaginator,
        SearchProductsAsAdminPaginator,
    )

    session = Session()
    client: ServiceCatalogClient = session.client("servicecatalog")

    list_accepted_portfolio_shares_paginator: ListAcceptedPortfolioSharesPaginator = client.get_paginator("list_accepted_portfolio_shares")
    list_constraints_for_portfolio_paginator: ListConstraintsForPortfolioPaginator = client.get_paginator("list_constraints_for_portfolio")
    list_launch_paths_paginator: ListLaunchPathsPaginator = client.get_paginator("list_launch_paths")
    list_organization_portfolio_access_paginator: ListOrganizationPortfolioAccessPaginator = client.get_paginator("list_organization_portfolio_access")
    list_portfolios_for_product_paginator: ListPortfoliosForProductPaginator = client.get_paginator("list_portfolios_for_product")
    list_portfolios_paginator: ListPortfoliosPaginator = client.get_paginator("list_portfolios")
    list_principals_for_portfolio_paginator: ListPrincipalsForPortfolioPaginator = client.get_paginator("list_principals_for_portfolio")
    list_provisioned_product_plans_paginator: ListProvisionedProductPlansPaginator = client.get_paginator("list_provisioned_product_plans")
    list_provisioning_artifacts_for_service_action_paginator: ListProvisioningArtifactsForServiceActionPaginator = client.get_paginator("list_provisioning_artifacts_for_service_action")
    list_record_history_paginator: ListRecordHistoryPaginator = client.get_paginator("list_record_history")
    list_resources_for_tag_option_paginator: ListResourcesForTagOptionPaginator = client.get_paginator("list_resources_for_tag_option")
    list_service_actions_for_provisioning_artifact_paginator: ListServiceActionsForProvisioningArtifactPaginator = client.get_paginator("list_service_actions_for_provisioning_artifact")
    list_service_actions_paginator: ListServiceActionsPaginator = client.get_paginator("list_service_actions")
    list_tag_options_paginator: ListTagOptionsPaginator = client.get_paginator("list_tag_options")
    scan_provisioned_products_paginator: ScanProvisionedProductsPaginator = client.get_paginator("scan_provisioned_products")
    search_products_as_admin_paginator: SearchProductsAsAdminPaginator = client.get_paginator("search_products_as_admin")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAcceptedPortfolioSharesInputListAcceptedPortfolioSharesPaginateTypeDef,
    ListAcceptedPortfolioSharesOutputTypeDef,
    ListConstraintsForPortfolioInputListConstraintsForPortfolioPaginateTypeDef,
    ListConstraintsForPortfolioOutputTypeDef,
    ListLaunchPathsInputListLaunchPathsPaginateTypeDef,
    ListLaunchPathsOutputTypeDef,
    ListOrganizationPortfolioAccessInputListOrganizationPortfolioAccessPaginateTypeDef,
    ListOrganizationPortfolioAccessOutputTypeDef,
    ListPortfoliosForProductInputListPortfoliosForProductPaginateTypeDef,
    ListPortfoliosForProductOutputTypeDef,
    ListPortfoliosInputListPortfoliosPaginateTypeDef,
    ListPortfoliosOutputTypeDef,
    ListPrincipalsForPortfolioInputListPrincipalsForPortfolioPaginateTypeDef,
    ListPrincipalsForPortfolioOutputTypeDef,
    ListProvisionedProductPlansInputListProvisionedProductPlansPaginateTypeDef,
    ListProvisionedProductPlansOutputTypeDef,
    ListProvisioningArtifactsForServiceActionInputListProvisioningArtifactsForServiceActionPaginateTypeDef,
    ListProvisioningArtifactsForServiceActionOutputTypeDef,
    ListRecordHistoryInputListRecordHistoryPaginateTypeDef,
    ListRecordHistoryOutputTypeDef,
    ListResourcesForTagOptionInputListResourcesForTagOptionPaginateTypeDef,
    ListResourcesForTagOptionOutputTypeDef,
    ListServiceActionsForProvisioningArtifactInputListServiceActionsForProvisioningArtifactPaginateTypeDef,
    ListServiceActionsForProvisioningArtifactOutputTypeDef,
    ListServiceActionsInputListServiceActionsPaginateTypeDef,
    ListServiceActionsOutputTypeDef,
    ListTagOptionsInputListTagOptionsPaginateTypeDef,
    ListTagOptionsOutputTypeDef,
    ScanProvisionedProductsInputScanProvisionedProductsPaginateTypeDef,
    ScanProvisionedProductsOutputTypeDef,
    SearchProductsAsAdminInputSearchProductsAsAdminPaginateTypeDef,
    SearchProductsAsAdminOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAcceptedPortfolioSharesPaginator",
    "ListConstraintsForPortfolioPaginator",
    "ListLaunchPathsPaginator",
    "ListOrganizationPortfolioAccessPaginator",
    "ListPortfoliosForProductPaginator",
    "ListPortfoliosPaginator",
    "ListPrincipalsForPortfolioPaginator",
    "ListProvisionedProductPlansPaginator",
    "ListProvisioningArtifactsForServiceActionPaginator",
    "ListRecordHistoryPaginator",
    "ListResourcesForTagOptionPaginator",
    "ListServiceActionsForProvisioningArtifactPaginator",
    "ListServiceActionsPaginator",
    "ListTagOptionsPaginator",
    "ScanProvisionedProductsPaginator",
    "SearchProductsAsAdminPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAcceptedPortfolioSharesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListAcceptedPortfolioShares.html#ServiceCatalog.Paginator.ListAcceptedPortfolioShares)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listacceptedportfoliosharespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAcceptedPortfolioSharesInputListAcceptedPortfolioSharesPaginateTypeDef
        ],
    ) -> _PageIterator[ListAcceptedPortfolioSharesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListAcceptedPortfolioShares.html#ServiceCatalog.Paginator.ListAcceptedPortfolioShares.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listacceptedportfoliosharespaginator)
        """


class ListConstraintsForPortfolioPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListConstraintsForPortfolio.html#ServiceCatalog.Paginator.ListConstraintsForPortfolio)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listconstraintsforportfoliopaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListConstraintsForPortfolioInputListConstraintsForPortfolioPaginateTypeDef
        ],
    ) -> _PageIterator[ListConstraintsForPortfolioOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListConstraintsForPortfolio.html#ServiceCatalog.Paginator.ListConstraintsForPortfolio.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listconstraintsforportfoliopaginator)
        """


class ListLaunchPathsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListLaunchPaths.html#ServiceCatalog.Paginator.ListLaunchPaths)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listlaunchpathspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLaunchPathsInputListLaunchPathsPaginateTypeDef]
    ) -> _PageIterator[ListLaunchPathsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListLaunchPaths.html#ServiceCatalog.Paginator.ListLaunchPaths.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listlaunchpathspaginator)
        """


class ListOrganizationPortfolioAccessPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListOrganizationPortfolioAccess.html#ServiceCatalog.Paginator.ListOrganizationPortfolioAccess)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listorganizationportfolioaccesspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListOrganizationPortfolioAccessInputListOrganizationPortfolioAccessPaginateTypeDef
        ],
    ) -> _PageIterator[ListOrganizationPortfolioAccessOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListOrganizationPortfolioAccess.html#ServiceCatalog.Paginator.ListOrganizationPortfolioAccess.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listorganizationportfolioaccesspaginator)
        """


class ListPortfoliosForProductPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPortfoliosForProduct.html#ServiceCatalog.Paginator.ListPortfoliosForProduct)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listportfoliosforproductpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPortfoliosForProductInputListPortfoliosForProductPaginateTypeDef]
    ) -> _PageIterator[ListPortfoliosForProductOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPortfoliosForProduct.html#ServiceCatalog.Paginator.ListPortfoliosForProduct.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listportfoliosforproductpaginator)
        """


class ListPortfoliosPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPortfolios.html#ServiceCatalog.Paginator.ListPortfolios)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listportfoliospaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPortfoliosInputListPortfoliosPaginateTypeDef]
    ) -> _PageIterator[ListPortfoliosOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPortfolios.html#ServiceCatalog.Paginator.ListPortfolios.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listportfoliospaginator)
        """


class ListPrincipalsForPortfolioPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPrincipalsForPortfolio.html#ServiceCatalog.Paginator.ListPrincipalsForPortfolio)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listprincipalsforportfoliopaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListPrincipalsForPortfolioInputListPrincipalsForPortfolioPaginateTypeDef],
    ) -> _PageIterator[ListPrincipalsForPortfolioOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPrincipalsForPortfolio.html#ServiceCatalog.Paginator.ListPrincipalsForPortfolio.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listprincipalsforportfoliopaginator)
        """


class ListProvisionedProductPlansPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListProvisionedProductPlans.html#ServiceCatalog.Paginator.ListProvisionedProductPlans)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listprovisionedproductplanspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListProvisionedProductPlansInputListProvisionedProductPlansPaginateTypeDef
        ],
    ) -> _PageIterator[ListProvisionedProductPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListProvisionedProductPlans.html#ServiceCatalog.Paginator.ListProvisionedProductPlans.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listprovisionedproductplanspaginator)
        """


class ListProvisioningArtifactsForServiceActionPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListProvisioningArtifactsForServiceAction.html#ServiceCatalog.Paginator.ListProvisioningArtifactsForServiceAction)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listprovisioningartifactsforserviceactionpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListProvisioningArtifactsForServiceActionInputListProvisioningArtifactsForServiceActionPaginateTypeDef
        ],
    ) -> _PageIterator[ListProvisioningArtifactsForServiceActionOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListProvisioningArtifactsForServiceAction.html#ServiceCatalog.Paginator.ListProvisioningArtifactsForServiceAction.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listprovisioningartifactsforserviceactionpaginator)
        """


class ListRecordHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListRecordHistory.html#ServiceCatalog.Paginator.ListRecordHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listrecordhistorypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRecordHistoryInputListRecordHistoryPaginateTypeDef]
    ) -> _PageIterator[ListRecordHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListRecordHistory.html#ServiceCatalog.Paginator.ListRecordHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listrecordhistorypaginator)
        """


class ListResourcesForTagOptionPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListResourcesForTagOption.html#ServiceCatalog.Paginator.ListResourcesForTagOption)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listresourcesfortagoptionpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListResourcesForTagOptionInputListResourcesForTagOptionPaginateTypeDef],
    ) -> _PageIterator[ListResourcesForTagOptionOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListResourcesForTagOption.html#ServiceCatalog.Paginator.ListResourcesForTagOption.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listresourcesfortagoptionpaginator)
        """


class ListServiceActionsForProvisioningArtifactPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListServiceActionsForProvisioningArtifact.html#ServiceCatalog.Paginator.ListServiceActionsForProvisioningArtifact)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listserviceactionsforprovisioningartifactpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListServiceActionsForProvisioningArtifactInputListServiceActionsForProvisioningArtifactPaginateTypeDef
        ],
    ) -> _PageIterator[ListServiceActionsForProvisioningArtifactOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListServiceActionsForProvisioningArtifact.html#ServiceCatalog.Paginator.ListServiceActionsForProvisioningArtifact.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listserviceactionsforprovisioningartifactpaginator)
        """


class ListServiceActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListServiceActions.html#ServiceCatalog.Paginator.ListServiceActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listserviceactionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListServiceActionsInputListServiceActionsPaginateTypeDef]
    ) -> _PageIterator[ListServiceActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListServiceActions.html#ServiceCatalog.Paginator.ListServiceActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listserviceactionspaginator)
        """


class ListTagOptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListTagOptions.html#ServiceCatalog.Paginator.ListTagOptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listtagoptionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTagOptionsInputListTagOptionsPaginateTypeDef]
    ) -> _PageIterator[ListTagOptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListTagOptions.html#ServiceCatalog.Paginator.ListTagOptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#listtagoptionspaginator)
        """


class ScanProvisionedProductsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ScanProvisionedProducts.html#ServiceCatalog.Paginator.ScanProvisionedProducts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#scanprovisionedproductspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ScanProvisionedProductsInputScanProvisionedProductsPaginateTypeDef]
    ) -> _PageIterator[ScanProvisionedProductsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ScanProvisionedProducts.html#ServiceCatalog.Paginator.ScanProvisionedProducts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#scanprovisionedproductspaginator)
        """


class SearchProductsAsAdminPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/SearchProductsAsAdmin.html#ServiceCatalog.Paginator.SearchProductsAsAdmin)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#searchproductsasadminpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchProductsAsAdminInputSearchProductsAsAdminPaginateTypeDef]
    ) -> _PageIterator[SearchProductsAsAdminOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/SearchProductsAsAdmin.html#ServiceCatalog.Paginator.SearchProductsAsAdmin.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/paginators/#searchproductsasadminpaginator)
        """
