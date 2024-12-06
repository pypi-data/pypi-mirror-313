"""
Type annotations for servicecatalog service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_servicecatalog.client import ServiceCatalogClient

    session = Session()
    client: ServiceCatalogClient = session.client("servicecatalog")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
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
from .type_defs import (
    AcceptPortfolioShareInputRequestTypeDef,
    AssociateBudgetWithResourceInputRequestTypeDef,
    AssociatePrincipalWithPortfolioInputRequestTypeDef,
    AssociateProductWithPortfolioInputRequestTypeDef,
    AssociateServiceActionWithProvisioningArtifactInputRequestTypeDef,
    AssociateTagOptionWithResourceInputRequestTypeDef,
    BatchAssociateServiceActionWithProvisioningArtifactInputRequestTypeDef,
    BatchAssociateServiceActionWithProvisioningArtifactOutputTypeDef,
    BatchDisassociateServiceActionFromProvisioningArtifactInputRequestTypeDef,
    BatchDisassociateServiceActionFromProvisioningArtifactOutputTypeDef,
    CopyProductInputRequestTypeDef,
    CopyProductOutputTypeDef,
    CreateConstraintInputRequestTypeDef,
    CreateConstraintOutputTypeDef,
    CreatePortfolioInputRequestTypeDef,
    CreatePortfolioOutputTypeDef,
    CreatePortfolioShareInputRequestTypeDef,
    CreatePortfolioShareOutputTypeDef,
    CreateProductInputRequestTypeDef,
    CreateProductOutputTypeDef,
    CreateProvisionedProductPlanInputRequestTypeDef,
    CreateProvisionedProductPlanOutputTypeDef,
    CreateProvisioningArtifactInputRequestTypeDef,
    CreateProvisioningArtifactOutputTypeDef,
    CreateServiceActionInputRequestTypeDef,
    CreateServiceActionOutputTypeDef,
    CreateTagOptionInputRequestTypeDef,
    CreateTagOptionOutputTypeDef,
    DeleteConstraintInputRequestTypeDef,
    DeletePortfolioInputRequestTypeDef,
    DeletePortfolioShareInputRequestTypeDef,
    DeletePortfolioShareOutputTypeDef,
    DeleteProductInputRequestTypeDef,
    DeleteProvisionedProductPlanInputRequestTypeDef,
    DeleteProvisioningArtifactInputRequestTypeDef,
    DeleteServiceActionInputRequestTypeDef,
    DeleteTagOptionInputRequestTypeDef,
    DescribeConstraintInputRequestTypeDef,
    DescribeConstraintOutputTypeDef,
    DescribeCopyProductStatusInputRequestTypeDef,
    DescribeCopyProductStatusOutputTypeDef,
    DescribePortfolioInputRequestTypeDef,
    DescribePortfolioOutputTypeDef,
    DescribePortfolioSharesInputRequestTypeDef,
    DescribePortfolioSharesOutputTypeDef,
    DescribePortfolioShareStatusInputRequestTypeDef,
    DescribePortfolioShareStatusOutputTypeDef,
    DescribeProductAsAdminInputRequestTypeDef,
    DescribeProductAsAdminOutputTypeDef,
    DescribeProductInputRequestTypeDef,
    DescribeProductOutputTypeDef,
    DescribeProductViewInputRequestTypeDef,
    DescribeProductViewOutputTypeDef,
    DescribeProvisionedProductInputRequestTypeDef,
    DescribeProvisionedProductOutputTypeDef,
    DescribeProvisionedProductPlanInputRequestTypeDef,
    DescribeProvisionedProductPlanOutputTypeDef,
    DescribeProvisioningArtifactInputRequestTypeDef,
    DescribeProvisioningArtifactOutputTypeDef,
    DescribeProvisioningParametersInputRequestTypeDef,
    DescribeProvisioningParametersOutputTypeDef,
    DescribeRecordInputRequestTypeDef,
    DescribeRecordOutputTypeDef,
    DescribeServiceActionExecutionParametersInputRequestTypeDef,
    DescribeServiceActionExecutionParametersOutputTypeDef,
    DescribeServiceActionInputRequestTypeDef,
    DescribeServiceActionOutputTypeDef,
    DescribeTagOptionInputRequestTypeDef,
    DescribeTagOptionOutputTypeDef,
    DisassociateBudgetFromResourceInputRequestTypeDef,
    DisassociatePrincipalFromPortfolioInputRequestTypeDef,
    DisassociateProductFromPortfolioInputRequestTypeDef,
    DisassociateServiceActionFromProvisioningArtifactInputRequestTypeDef,
    DisassociateTagOptionFromResourceInputRequestTypeDef,
    ExecuteProvisionedProductPlanInputRequestTypeDef,
    ExecuteProvisionedProductPlanOutputTypeDef,
    ExecuteProvisionedProductServiceActionInputRequestTypeDef,
    ExecuteProvisionedProductServiceActionOutputTypeDef,
    GetAWSOrganizationsAccessStatusOutputTypeDef,
    GetProvisionedProductOutputsInputRequestTypeDef,
    GetProvisionedProductOutputsOutputTypeDef,
    ImportAsProvisionedProductInputRequestTypeDef,
    ImportAsProvisionedProductOutputTypeDef,
    ListAcceptedPortfolioSharesInputRequestTypeDef,
    ListAcceptedPortfolioSharesOutputTypeDef,
    ListBudgetsForResourceInputRequestTypeDef,
    ListBudgetsForResourceOutputTypeDef,
    ListConstraintsForPortfolioInputRequestTypeDef,
    ListConstraintsForPortfolioOutputTypeDef,
    ListLaunchPathsInputRequestTypeDef,
    ListLaunchPathsOutputTypeDef,
    ListOrganizationPortfolioAccessInputRequestTypeDef,
    ListOrganizationPortfolioAccessOutputTypeDef,
    ListPortfolioAccessInputRequestTypeDef,
    ListPortfolioAccessOutputTypeDef,
    ListPortfoliosForProductInputRequestTypeDef,
    ListPortfoliosForProductOutputTypeDef,
    ListPortfoliosInputRequestTypeDef,
    ListPortfoliosOutputTypeDef,
    ListPrincipalsForPortfolioInputRequestTypeDef,
    ListPrincipalsForPortfolioOutputTypeDef,
    ListProvisionedProductPlansInputRequestTypeDef,
    ListProvisionedProductPlansOutputTypeDef,
    ListProvisioningArtifactsForServiceActionInputRequestTypeDef,
    ListProvisioningArtifactsForServiceActionOutputTypeDef,
    ListProvisioningArtifactsInputRequestTypeDef,
    ListProvisioningArtifactsOutputTypeDef,
    ListRecordHistoryInputRequestTypeDef,
    ListRecordHistoryOutputTypeDef,
    ListResourcesForTagOptionInputRequestTypeDef,
    ListResourcesForTagOptionOutputTypeDef,
    ListServiceActionsForProvisioningArtifactInputRequestTypeDef,
    ListServiceActionsForProvisioningArtifactOutputTypeDef,
    ListServiceActionsInputRequestTypeDef,
    ListServiceActionsOutputTypeDef,
    ListStackInstancesForProvisionedProductInputRequestTypeDef,
    ListStackInstancesForProvisionedProductOutputTypeDef,
    ListTagOptionsInputRequestTypeDef,
    ListTagOptionsOutputTypeDef,
    NotifyProvisionProductEngineWorkflowResultInputRequestTypeDef,
    NotifyTerminateProvisionedProductEngineWorkflowResultInputRequestTypeDef,
    NotifyUpdateProvisionedProductEngineWorkflowResultInputRequestTypeDef,
    ProvisionProductInputRequestTypeDef,
    ProvisionProductOutputTypeDef,
    RejectPortfolioShareInputRequestTypeDef,
    ScanProvisionedProductsInputRequestTypeDef,
    ScanProvisionedProductsOutputTypeDef,
    SearchProductsAsAdminInputRequestTypeDef,
    SearchProductsAsAdminOutputTypeDef,
    SearchProductsInputRequestTypeDef,
    SearchProductsOutputTypeDef,
    SearchProvisionedProductsInputRequestTypeDef,
    SearchProvisionedProductsOutputTypeDef,
    TerminateProvisionedProductInputRequestTypeDef,
    TerminateProvisionedProductOutputTypeDef,
    UpdateConstraintInputRequestTypeDef,
    UpdateConstraintOutputTypeDef,
    UpdatePortfolioInputRequestTypeDef,
    UpdatePortfolioOutputTypeDef,
    UpdatePortfolioShareInputRequestTypeDef,
    UpdatePortfolioShareOutputTypeDef,
    UpdateProductInputRequestTypeDef,
    UpdateProductOutputTypeDef,
    UpdateProvisionedProductInputRequestTypeDef,
    UpdateProvisionedProductOutputTypeDef,
    UpdateProvisionedProductPropertiesInputRequestTypeDef,
    UpdateProvisionedProductPropertiesOutputTypeDef,
    UpdateProvisioningArtifactInputRequestTypeDef,
    UpdateProvisioningArtifactOutputTypeDef,
    UpdateServiceActionInputRequestTypeDef,
    UpdateServiceActionOutputTypeDef,
    UpdateTagOptionInputRequestTypeDef,
    UpdateTagOptionOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ServiceCatalogClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    DuplicateResourceException: Type[BotocoreClientError]
    InvalidParametersException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    OperationNotSupportedException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TagOptionNotMigratedException: Type[BotocoreClientError]

class ServiceCatalogClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ServiceCatalogClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#close)
        """

    def accept_portfolio_share(
        self, **kwargs: Unpack[AcceptPortfolioShareInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Accepts an offer to share the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/accept_portfolio_share.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#accept_portfolio_share)
        """

    def associate_budget_with_resource(
        self, **kwargs: Unpack[AssociateBudgetWithResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates the specified budget with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/associate_budget_with_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#associate_budget_with_resource)
        """

    def associate_principal_with_portfolio(
        self, **kwargs: Unpack[AssociatePrincipalWithPortfolioInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates the specified principal ARN with the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/associate_principal_with_portfolio.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#associate_principal_with_portfolio)
        """

    def associate_product_with_portfolio(
        self, **kwargs: Unpack[AssociateProductWithPortfolioInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates the specified product with the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/associate_product_with_portfolio.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#associate_product_with_portfolio)
        """

    def associate_service_action_with_provisioning_artifact(
        self, **kwargs: Unpack[AssociateServiceActionWithProvisioningArtifactInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a self-service action with a provisioning artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/associate_service_action_with_provisioning_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#associate_service_action_with_provisioning_artifact)
        """

    def associate_tag_option_with_resource(
        self, **kwargs: Unpack[AssociateTagOptionWithResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associate the specified TagOption with the specified portfolio or product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/associate_tag_option_with_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#associate_tag_option_with_resource)
        """

    def batch_associate_service_action_with_provisioning_artifact(
        self,
        **kwargs: Unpack[BatchAssociateServiceActionWithProvisioningArtifactInputRequestTypeDef],
    ) -> BatchAssociateServiceActionWithProvisioningArtifactOutputTypeDef:
        """
        Associates multiple self-service actions with provisioning artifacts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/batch_associate_service_action_with_provisioning_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#batch_associate_service_action_with_provisioning_artifact)
        """

    def batch_disassociate_service_action_from_provisioning_artifact(
        self,
        **kwargs: Unpack[BatchDisassociateServiceActionFromProvisioningArtifactInputRequestTypeDef],
    ) -> BatchDisassociateServiceActionFromProvisioningArtifactOutputTypeDef:
        """
        Disassociates a batch of self-service actions from the specified provisioning
        artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/batch_disassociate_service_action_from_provisioning_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#batch_disassociate_service_action_from_provisioning_artifact)
        """

    def copy_product(
        self, **kwargs: Unpack[CopyProductInputRequestTypeDef]
    ) -> CopyProductOutputTypeDef:
        """
        Copies the specified source product to the specified target product or a new
        product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/copy_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#copy_product)
        """

    def create_constraint(
        self, **kwargs: Unpack[CreateConstraintInputRequestTypeDef]
    ) -> CreateConstraintOutputTypeDef:
        """
        Creates a constraint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/create_constraint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_constraint)
        """

    def create_portfolio(
        self, **kwargs: Unpack[CreatePortfolioInputRequestTypeDef]
    ) -> CreatePortfolioOutputTypeDef:
        """
        Creates a portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/create_portfolio.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_portfolio)
        """

    def create_portfolio_share(
        self, **kwargs: Unpack[CreatePortfolioShareInputRequestTypeDef]
    ) -> CreatePortfolioShareOutputTypeDef:
        """
        Shares the specified portfolio with the specified account or organization node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/create_portfolio_share.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_portfolio_share)
        """

    def create_product(
        self, **kwargs: Unpack[CreateProductInputRequestTypeDef]
    ) -> CreateProductOutputTypeDef:
        """
        Creates a product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/create_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_product)
        """

    def create_provisioned_product_plan(
        self, **kwargs: Unpack[CreateProvisionedProductPlanInputRequestTypeDef]
    ) -> CreateProvisionedProductPlanOutputTypeDef:
        """
        Creates a plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/create_provisioned_product_plan.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_provisioned_product_plan)
        """

    def create_provisioning_artifact(
        self, **kwargs: Unpack[CreateProvisioningArtifactInputRequestTypeDef]
    ) -> CreateProvisioningArtifactOutputTypeDef:
        """
        Creates a provisioning artifact (also known as a version) for the specified
        product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/create_provisioning_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_provisioning_artifact)
        """

    def create_service_action(
        self, **kwargs: Unpack[CreateServiceActionInputRequestTypeDef]
    ) -> CreateServiceActionOutputTypeDef:
        """
        Creates a self-service action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/create_service_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_service_action)
        """

    def create_tag_option(
        self, **kwargs: Unpack[CreateTagOptionInputRequestTypeDef]
    ) -> CreateTagOptionOutputTypeDef:
        """
        Creates a TagOption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/create_tag_option.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#create_tag_option)
        """

    def delete_constraint(
        self, **kwargs: Unpack[DeleteConstraintInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified constraint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/delete_constraint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_constraint)
        """

    def delete_portfolio(
        self, **kwargs: Unpack[DeletePortfolioInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/delete_portfolio.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_portfolio)
        """

    def delete_portfolio_share(
        self, **kwargs: Unpack[DeletePortfolioShareInputRequestTypeDef]
    ) -> DeletePortfolioShareOutputTypeDef:
        """
        Stops sharing the specified portfolio with the specified account or
        organization node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/delete_portfolio_share.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_portfolio_share)
        """

    def delete_product(self, **kwargs: Unpack[DeleteProductInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/delete_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_product)
        """

    def delete_provisioned_product_plan(
        self, **kwargs: Unpack[DeleteProvisionedProductPlanInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/delete_provisioned_product_plan.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_provisioned_product_plan)
        """

    def delete_provisioning_artifact(
        self, **kwargs: Unpack[DeleteProvisioningArtifactInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified provisioning artifact (also known as a version) for the
        specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/delete_provisioning_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_provisioning_artifact)
        """

    def delete_service_action(
        self, **kwargs: Unpack[DeleteServiceActionInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a self-service action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/delete_service_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_service_action)
        """

    def delete_tag_option(
        self, **kwargs: Unpack[DeleteTagOptionInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified TagOption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/delete_tag_option.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#delete_tag_option)
        """

    def describe_constraint(
        self, **kwargs: Unpack[DescribeConstraintInputRequestTypeDef]
    ) -> DescribeConstraintOutputTypeDef:
        """
        Gets information about the specified constraint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_constraint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_constraint)
        """

    def describe_copy_product_status(
        self, **kwargs: Unpack[DescribeCopyProductStatusInputRequestTypeDef]
    ) -> DescribeCopyProductStatusOutputTypeDef:
        """
        Gets the status of the specified copy product operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_copy_product_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_copy_product_status)
        """

    def describe_portfolio(
        self, **kwargs: Unpack[DescribePortfolioInputRequestTypeDef]
    ) -> DescribePortfolioOutputTypeDef:
        """
        Gets information about the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_portfolio.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_portfolio)
        """

    def describe_portfolio_share_status(
        self, **kwargs: Unpack[DescribePortfolioShareStatusInputRequestTypeDef]
    ) -> DescribePortfolioShareStatusOutputTypeDef:
        """
        Gets the status of the specified portfolio share operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_portfolio_share_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_portfolio_share_status)
        """

    def describe_portfolio_shares(
        self, **kwargs: Unpack[DescribePortfolioSharesInputRequestTypeDef]
    ) -> DescribePortfolioSharesOutputTypeDef:
        """
        Returns a summary of each of the portfolio shares that were created for the
        specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_portfolio_shares.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_portfolio_shares)
        """

    def describe_product(
        self, **kwargs: Unpack[DescribeProductInputRequestTypeDef]
    ) -> DescribeProductOutputTypeDef:
        """
        Gets information about the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_product)
        """

    def describe_product_as_admin(
        self, **kwargs: Unpack[DescribeProductAsAdminInputRequestTypeDef]
    ) -> DescribeProductAsAdminOutputTypeDef:
        """
        Gets information about the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_product_as_admin.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_product_as_admin)
        """

    def describe_product_view(
        self, **kwargs: Unpack[DescribeProductViewInputRequestTypeDef]
    ) -> DescribeProductViewOutputTypeDef:
        """
        Gets information about the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_product_view.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_product_view)
        """

    def describe_provisioned_product(
        self, **kwargs: Unpack[DescribeProvisionedProductInputRequestTypeDef]
    ) -> DescribeProvisionedProductOutputTypeDef:
        """
        Gets information about the specified provisioned product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_provisioned_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_provisioned_product)
        """

    def describe_provisioned_product_plan(
        self, **kwargs: Unpack[DescribeProvisionedProductPlanInputRequestTypeDef]
    ) -> DescribeProvisionedProductPlanOutputTypeDef:
        """
        Gets information about the resource changes for the specified plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_provisioned_product_plan.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_provisioned_product_plan)
        """

    def describe_provisioning_artifact(
        self, **kwargs: Unpack[DescribeProvisioningArtifactInputRequestTypeDef]
    ) -> DescribeProvisioningArtifactOutputTypeDef:
        """
        Gets information about the specified provisioning artifact (also known as a
        version) for the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_provisioning_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_provisioning_artifact)
        """

    def describe_provisioning_parameters(
        self, **kwargs: Unpack[DescribeProvisioningParametersInputRequestTypeDef]
    ) -> DescribeProvisioningParametersOutputTypeDef:
        """
        Gets information about the configuration required to provision the specified
        product using the specified provisioning artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_provisioning_parameters.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_provisioning_parameters)
        """

    def describe_record(
        self, **kwargs: Unpack[DescribeRecordInputRequestTypeDef]
    ) -> DescribeRecordOutputTypeDef:
        """
        Gets information about the specified request operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_record.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_record)
        """

    def describe_service_action(
        self, **kwargs: Unpack[DescribeServiceActionInputRequestTypeDef]
    ) -> DescribeServiceActionOutputTypeDef:
        """
        Describes a self-service action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_service_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_service_action)
        """

    def describe_service_action_execution_parameters(
        self, **kwargs: Unpack[DescribeServiceActionExecutionParametersInputRequestTypeDef]
    ) -> DescribeServiceActionExecutionParametersOutputTypeDef:
        """
        Finds the default parameters for a specific self-service action on a specific
        provisioned product and returns a map of the results to the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_service_action_execution_parameters.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_service_action_execution_parameters)
        """

    def describe_tag_option(
        self, **kwargs: Unpack[DescribeTagOptionInputRequestTypeDef]
    ) -> DescribeTagOptionOutputTypeDef:
        """
        Gets information about the specified TagOption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/describe_tag_option.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#describe_tag_option)
        """

    def disable_aws_organizations_access(self) -> Dict[str, Any]:
        """
        Disable portfolio sharing through the Organizations service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/disable_aws_organizations_access.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#disable_aws_organizations_access)
        """

    def disassociate_budget_from_resource(
        self, **kwargs: Unpack[DisassociateBudgetFromResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified budget from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/disassociate_budget_from_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#disassociate_budget_from_resource)
        """

    def disassociate_principal_from_portfolio(
        self, **kwargs: Unpack[DisassociatePrincipalFromPortfolioInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a previously associated principal ARN from a specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/disassociate_principal_from_portfolio.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#disassociate_principal_from_portfolio)
        """

    def disassociate_product_from_portfolio(
        self, **kwargs: Unpack[DisassociateProductFromPortfolioInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified product from the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/disassociate_product_from_portfolio.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#disassociate_product_from_portfolio)
        """

    def disassociate_service_action_from_provisioning_artifact(
        self, **kwargs: Unpack[DisassociateServiceActionFromProvisioningArtifactInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified self-service action association from the specified
        provisioning artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/disassociate_service_action_from_provisioning_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#disassociate_service_action_from_provisioning_artifact)
        """

    def disassociate_tag_option_from_resource(
        self, **kwargs: Unpack[DisassociateTagOptionFromResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified TagOption from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/disassociate_tag_option_from_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#disassociate_tag_option_from_resource)
        """

    def enable_aws_organizations_access(self) -> Dict[str, Any]:
        """
        Enable portfolio sharing feature through Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/enable_aws_organizations_access.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#enable_aws_organizations_access)
        """

    def execute_provisioned_product_plan(
        self, **kwargs: Unpack[ExecuteProvisionedProductPlanInputRequestTypeDef]
    ) -> ExecuteProvisionedProductPlanOutputTypeDef:
        """
        Provisions or modifies a product based on the resource changes for the
        specified plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/execute_provisioned_product_plan.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#execute_provisioned_product_plan)
        """

    def execute_provisioned_product_service_action(
        self, **kwargs: Unpack[ExecuteProvisionedProductServiceActionInputRequestTypeDef]
    ) -> ExecuteProvisionedProductServiceActionOutputTypeDef:
        """
        Executes a self-service action against a provisioned product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/execute_provisioned_product_service_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#execute_provisioned_product_service_action)
        """

    def get_aws_organizations_access_status(self) -> GetAWSOrganizationsAccessStatusOutputTypeDef:
        """
        Get the Access Status for Organizations portfolio share feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_aws_organizations_access_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_aws_organizations_access_status)
        """

    def get_provisioned_product_outputs(
        self, **kwargs: Unpack[GetProvisionedProductOutputsInputRequestTypeDef]
    ) -> GetProvisionedProductOutputsOutputTypeDef:
        """
        This API takes either a <code>ProvisonedProductId</code> or a
        <code>ProvisionedProductName</code>, along with a list of one or more output
        keys, and responds with the key/value pairs of those outputs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_provisioned_product_outputs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_provisioned_product_outputs)
        """

    def import_as_provisioned_product(
        self, **kwargs: Unpack[ImportAsProvisionedProductInputRequestTypeDef]
    ) -> ImportAsProvisionedProductOutputTypeDef:
        """
        Requests the import of a resource as an Service Catalog provisioned product
        that is associated to an Service Catalog product and provisioning artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/import_as_provisioned_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#import_as_provisioned_product)
        """

    def list_accepted_portfolio_shares(
        self, **kwargs: Unpack[ListAcceptedPortfolioSharesInputRequestTypeDef]
    ) -> ListAcceptedPortfolioSharesOutputTypeDef:
        """
        Lists all imported portfolios for which account-to-account shares were accepted
        by this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_accepted_portfolio_shares.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_accepted_portfolio_shares)
        """

    def list_budgets_for_resource(
        self, **kwargs: Unpack[ListBudgetsForResourceInputRequestTypeDef]
    ) -> ListBudgetsForResourceOutputTypeDef:
        """
        Lists all the budgets associated to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_budgets_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_budgets_for_resource)
        """

    def list_constraints_for_portfolio(
        self, **kwargs: Unpack[ListConstraintsForPortfolioInputRequestTypeDef]
    ) -> ListConstraintsForPortfolioOutputTypeDef:
        """
        Lists the constraints for the specified portfolio and product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_constraints_for_portfolio.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_constraints_for_portfolio)
        """

    def list_launch_paths(
        self, **kwargs: Unpack[ListLaunchPathsInputRequestTypeDef]
    ) -> ListLaunchPathsOutputTypeDef:
        """
        Lists the paths to the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_launch_paths.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_launch_paths)
        """

    def list_organization_portfolio_access(
        self, **kwargs: Unpack[ListOrganizationPortfolioAccessInputRequestTypeDef]
    ) -> ListOrganizationPortfolioAccessOutputTypeDef:
        """
        Lists the organization nodes that have access to the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_organization_portfolio_access.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_organization_portfolio_access)
        """

    def list_portfolio_access(
        self, **kwargs: Unpack[ListPortfolioAccessInputRequestTypeDef]
    ) -> ListPortfolioAccessOutputTypeDef:
        """
        Lists the account IDs that have access to the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_portfolio_access.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_portfolio_access)
        """

    def list_portfolios(
        self, **kwargs: Unpack[ListPortfoliosInputRequestTypeDef]
    ) -> ListPortfoliosOutputTypeDef:
        """
        Lists all portfolios in the catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_portfolios.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_portfolios)
        """

    def list_portfolios_for_product(
        self, **kwargs: Unpack[ListPortfoliosForProductInputRequestTypeDef]
    ) -> ListPortfoliosForProductOutputTypeDef:
        """
        Lists all portfolios that the specified product is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_portfolios_for_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_portfolios_for_product)
        """

    def list_principals_for_portfolio(
        self, **kwargs: Unpack[ListPrincipalsForPortfolioInputRequestTypeDef]
    ) -> ListPrincipalsForPortfolioOutputTypeDef:
        """
        Lists all <code>PrincipalARN</code>s and corresponding
        <code>PrincipalType</code>s associated with the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_principals_for_portfolio.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_principals_for_portfolio)
        """

    def list_provisioned_product_plans(
        self, **kwargs: Unpack[ListProvisionedProductPlansInputRequestTypeDef]
    ) -> ListProvisionedProductPlansOutputTypeDef:
        """
        Lists the plans for the specified provisioned product or all plans to which the
        user has access.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_provisioned_product_plans.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_provisioned_product_plans)
        """

    def list_provisioning_artifacts(
        self, **kwargs: Unpack[ListProvisioningArtifactsInputRequestTypeDef]
    ) -> ListProvisioningArtifactsOutputTypeDef:
        """
        Lists all provisioning artifacts (also known as versions) for the specified
        product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_provisioning_artifacts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_provisioning_artifacts)
        """

    def list_provisioning_artifacts_for_service_action(
        self, **kwargs: Unpack[ListProvisioningArtifactsForServiceActionInputRequestTypeDef]
    ) -> ListProvisioningArtifactsForServiceActionOutputTypeDef:
        """
        Lists all provisioning artifacts (also known as versions) for the specified
        self-service action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_provisioning_artifacts_for_service_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_provisioning_artifacts_for_service_action)
        """

    def list_record_history(
        self, **kwargs: Unpack[ListRecordHistoryInputRequestTypeDef]
    ) -> ListRecordHistoryOutputTypeDef:
        """
        Lists the specified requests or all performed requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_record_history.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_record_history)
        """

    def list_resources_for_tag_option(
        self, **kwargs: Unpack[ListResourcesForTagOptionInputRequestTypeDef]
    ) -> ListResourcesForTagOptionOutputTypeDef:
        """
        Lists the resources associated with the specified TagOption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_resources_for_tag_option.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_resources_for_tag_option)
        """

    def list_service_actions(
        self, **kwargs: Unpack[ListServiceActionsInputRequestTypeDef]
    ) -> ListServiceActionsOutputTypeDef:
        """
        Lists all self-service actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_service_actions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_service_actions)
        """

    def list_service_actions_for_provisioning_artifact(
        self, **kwargs: Unpack[ListServiceActionsForProvisioningArtifactInputRequestTypeDef]
    ) -> ListServiceActionsForProvisioningArtifactOutputTypeDef:
        """
        Returns a paginated list of self-service actions associated with the specified
        Product ID and Provisioning Artifact ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_service_actions_for_provisioning_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_service_actions_for_provisioning_artifact)
        """

    def list_stack_instances_for_provisioned_product(
        self, **kwargs: Unpack[ListStackInstancesForProvisionedProductInputRequestTypeDef]
    ) -> ListStackInstancesForProvisionedProductOutputTypeDef:
        """
        Returns summary information about stack instances that are associated with the
        specified <code>CFN_STACKSET</code> type provisioned product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_stack_instances_for_provisioned_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_stack_instances_for_provisioned_product)
        """

    def list_tag_options(
        self, **kwargs: Unpack[ListTagOptionsInputRequestTypeDef]
    ) -> ListTagOptionsOutputTypeDef:
        """
        Lists the specified TagOptions or all TagOptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/list_tag_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#list_tag_options)
        """

    def notify_provision_product_engine_workflow_result(
        self, **kwargs: Unpack[NotifyProvisionProductEngineWorkflowResultInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Notifies the result of the provisioning engine execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/notify_provision_product_engine_workflow_result.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#notify_provision_product_engine_workflow_result)
        """

    def notify_terminate_provisioned_product_engine_workflow_result(
        self,
        **kwargs: Unpack[NotifyTerminateProvisionedProductEngineWorkflowResultInputRequestTypeDef],
    ) -> Dict[str, Any]:
        """
        Notifies the result of the terminate engine execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/notify_terminate_provisioned_product_engine_workflow_result.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#notify_terminate_provisioned_product_engine_workflow_result)
        """

    def notify_update_provisioned_product_engine_workflow_result(
        self,
        **kwargs: Unpack[NotifyUpdateProvisionedProductEngineWorkflowResultInputRequestTypeDef],
    ) -> Dict[str, Any]:
        """
        Notifies the result of the update engine execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/notify_update_provisioned_product_engine_workflow_result.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#notify_update_provisioned_product_engine_workflow_result)
        """

    def provision_product(
        self, **kwargs: Unpack[ProvisionProductInputRequestTypeDef]
    ) -> ProvisionProductOutputTypeDef:
        """
        Provisions the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/provision_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#provision_product)
        """

    def reject_portfolio_share(
        self, **kwargs: Unpack[RejectPortfolioShareInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Rejects an offer to share the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/reject_portfolio_share.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#reject_portfolio_share)
        """

    def scan_provisioned_products(
        self, **kwargs: Unpack[ScanProvisionedProductsInputRequestTypeDef]
    ) -> ScanProvisionedProductsOutputTypeDef:
        """
        Lists the provisioned products that are available (not terminated).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/scan_provisioned_products.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#scan_provisioned_products)
        """

    def search_products(
        self, **kwargs: Unpack[SearchProductsInputRequestTypeDef]
    ) -> SearchProductsOutputTypeDef:
        """
        Gets information about the products to which the caller has access.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/search_products.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#search_products)
        """

    def search_products_as_admin(
        self, **kwargs: Unpack[SearchProductsAsAdminInputRequestTypeDef]
    ) -> SearchProductsAsAdminOutputTypeDef:
        """
        Gets information about the products for the specified portfolio or all products.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/search_products_as_admin.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#search_products_as_admin)
        """

    def search_provisioned_products(
        self, **kwargs: Unpack[SearchProvisionedProductsInputRequestTypeDef]
    ) -> SearchProvisionedProductsOutputTypeDef:
        """
        Gets information about the provisioned products that meet the specified
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/search_provisioned_products.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#search_provisioned_products)
        """

    def terminate_provisioned_product(
        self, **kwargs: Unpack[TerminateProvisionedProductInputRequestTypeDef]
    ) -> TerminateProvisionedProductOutputTypeDef:
        """
        Terminates the specified provisioned product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/terminate_provisioned_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#terminate_provisioned_product)
        """

    def update_constraint(
        self, **kwargs: Unpack[UpdateConstraintInputRequestTypeDef]
    ) -> UpdateConstraintOutputTypeDef:
        """
        Updates the specified constraint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/update_constraint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_constraint)
        """

    def update_portfolio(
        self, **kwargs: Unpack[UpdatePortfolioInputRequestTypeDef]
    ) -> UpdatePortfolioOutputTypeDef:
        """
        Updates the specified portfolio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/update_portfolio.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_portfolio)
        """

    def update_portfolio_share(
        self, **kwargs: Unpack[UpdatePortfolioShareInputRequestTypeDef]
    ) -> UpdatePortfolioShareOutputTypeDef:
        """
        Updates the specified portfolio share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/update_portfolio_share.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_portfolio_share)
        """

    def update_product(
        self, **kwargs: Unpack[UpdateProductInputRequestTypeDef]
    ) -> UpdateProductOutputTypeDef:
        """
        Updates the specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/update_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_product)
        """

    def update_provisioned_product(
        self, **kwargs: Unpack[UpdateProvisionedProductInputRequestTypeDef]
    ) -> UpdateProvisionedProductOutputTypeDef:
        """
        Requests updates to the configuration of the specified provisioned product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/update_provisioned_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_provisioned_product)
        """

    def update_provisioned_product_properties(
        self, **kwargs: Unpack[UpdateProvisionedProductPropertiesInputRequestTypeDef]
    ) -> UpdateProvisionedProductPropertiesOutputTypeDef:
        """
        Requests updates to the properties of the specified provisioned product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/update_provisioned_product_properties.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_provisioned_product_properties)
        """

    def update_provisioning_artifact(
        self, **kwargs: Unpack[UpdateProvisioningArtifactInputRequestTypeDef]
    ) -> UpdateProvisioningArtifactOutputTypeDef:
        """
        Updates the specified provisioning artifact (also known as a version) for the
        specified product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/update_provisioning_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_provisioning_artifact)
        """

    def update_service_action(
        self, **kwargs: Unpack[UpdateServiceActionInputRequestTypeDef]
    ) -> UpdateServiceActionOutputTypeDef:
        """
        Updates a self-service action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/update_service_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_service_action)
        """

    def update_tag_option(
        self, **kwargs: Unpack[UpdateTagOptionInputRequestTypeDef]
    ) -> UpdateTagOptionOutputTypeDef:
        """
        Updates the specified TagOption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/update_tag_option.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#update_tag_option)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_accepted_portfolio_shares"]
    ) -> ListAcceptedPortfolioSharesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_constraints_for_portfolio"]
    ) -> ListConstraintsForPortfolioPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_launch_paths"]
    ) -> ListLaunchPathsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_organization_portfolio_access"]
    ) -> ListOrganizationPortfolioAccessPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_portfolios_for_product"]
    ) -> ListPortfoliosForProductPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_portfolios"]) -> ListPortfoliosPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_principals_for_portfolio"]
    ) -> ListPrincipalsForPortfolioPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provisioned_product_plans"]
    ) -> ListProvisionedProductPlansPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provisioning_artifacts_for_service_action"]
    ) -> ListProvisioningArtifactsForServiceActionPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_record_history"]
    ) -> ListRecordHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resources_for_tag_option"]
    ) -> ListResourcesForTagOptionPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_actions_for_provisioning_artifact"]
    ) -> ListServiceActionsForProvisioningArtifactPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_actions"]
    ) -> ListServiceActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tag_options"]) -> ListTagOptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["scan_provisioned_products"]
    ) -> ScanProvisionedProductsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_products_as_admin"]
    ) -> SearchProductsAsAdminPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/client/#get_paginator)
        """
