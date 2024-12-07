"""
Type annotations for bcm-pricing-calculator service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_bcm_pricing_calculator.client import BillingandCostManagementPricingCalculatorClient

    session = Session()
    client: BillingandCostManagementPricingCalculatorClient = session.client("bcm-pricing-calculator")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListBillEstimateCommitmentsPaginator,
    ListBillEstimateInputCommitmentModificationsPaginator,
    ListBillEstimateInputUsageModificationsPaginator,
    ListBillEstimateLineItemsPaginator,
    ListBillEstimatesPaginator,
    ListBillScenarioCommitmentModificationsPaginator,
    ListBillScenariosPaginator,
    ListBillScenarioUsageModificationsPaginator,
    ListWorkloadEstimatesPaginator,
    ListWorkloadEstimateUsagePaginator,
)
from .type_defs import (
    BatchCreateBillScenarioCommitmentModificationRequestRequestTypeDef,
    BatchCreateBillScenarioCommitmentModificationResponseTypeDef,
    BatchCreateBillScenarioUsageModificationRequestRequestTypeDef,
    BatchCreateBillScenarioUsageModificationResponseTypeDef,
    BatchCreateWorkloadEstimateUsageRequestRequestTypeDef,
    BatchCreateWorkloadEstimateUsageResponseTypeDef,
    BatchDeleteBillScenarioCommitmentModificationRequestRequestTypeDef,
    BatchDeleteBillScenarioCommitmentModificationResponseTypeDef,
    BatchDeleteBillScenarioUsageModificationRequestRequestTypeDef,
    BatchDeleteBillScenarioUsageModificationResponseTypeDef,
    BatchDeleteWorkloadEstimateUsageRequestRequestTypeDef,
    BatchDeleteWorkloadEstimateUsageResponseTypeDef,
    BatchUpdateBillScenarioCommitmentModificationRequestRequestTypeDef,
    BatchUpdateBillScenarioCommitmentModificationResponseTypeDef,
    BatchUpdateBillScenarioUsageModificationRequestRequestTypeDef,
    BatchUpdateBillScenarioUsageModificationResponseTypeDef,
    BatchUpdateWorkloadEstimateUsageRequestRequestTypeDef,
    BatchUpdateWorkloadEstimateUsageResponseTypeDef,
    CreateBillEstimateRequestRequestTypeDef,
    CreateBillEstimateResponseTypeDef,
    CreateBillScenarioRequestRequestTypeDef,
    CreateBillScenarioResponseTypeDef,
    CreateWorkloadEstimateRequestRequestTypeDef,
    CreateWorkloadEstimateResponseTypeDef,
    DeleteBillEstimateRequestRequestTypeDef,
    DeleteBillScenarioRequestRequestTypeDef,
    DeleteWorkloadEstimateRequestRequestTypeDef,
    GetBillEstimateRequestRequestTypeDef,
    GetBillEstimateResponseTypeDef,
    GetBillScenarioRequestRequestTypeDef,
    GetBillScenarioResponseTypeDef,
    GetPreferencesResponseTypeDef,
    GetWorkloadEstimateRequestRequestTypeDef,
    GetWorkloadEstimateResponseTypeDef,
    ListBillEstimateCommitmentsRequestRequestTypeDef,
    ListBillEstimateCommitmentsResponseTypeDef,
    ListBillEstimateInputCommitmentModificationsRequestRequestTypeDef,
    ListBillEstimateInputCommitmentModificationsResponseTypeDef,
    ListBillEstimateInputUsageModificationsRequestRequestTypeDef,
    ListBillEstimateInputUsageModificationsResponseTypeDef,
    ListBillEstimateLineItemsRequestRequestTypeDef,
    ListBillEstimateLineItemsResponseTypeDef,
    ListBillEstimatesRequestRequestTypeDef,
    ListBillEstimatesResponseTypeDef,
    ListBillScenarioCommitmentModificationsRequestRequestTypeDef,
    ListBillScenarioCommitmentModificationsResponseTypeDef,
    ListBillScenariosRequestRequestTypeDef,
    ListBillScenariosResponseTypeDef,
    ListBillScenarioUsageModificationsRequestRequestTypeDef,
    ListBillScenarioUsageModificationsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorkloadEstimatesRequestRequestTypeDef,
    ListWorkloadEstimatesResponseTypeDef,
    ListWorkloadEstimateUsageRequestRequestTypeDef,
    ListWorkloadEstimateUsageResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateBillEstimateRequestRequestTypeDef,
    UpdateBillEstimateResponseTypeDef,
    UpdateBillScenarioRequestRequestTypeDef,
    UpdateBillScenarioResponseTypeDef,
    UpdatePreferencesRequestRequestTypeDef,
    UpdatePreferencesResponseTypeDef,
    UpdateWorkloadEstimateRequestRequestTypeDef,
    UpdateWorkloadEstimateResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("BillingandCostManagementPricingCalculatorClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DataUnavailableException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class BillingandCostManagementPricingCalculatorClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator.html#BillingandCostManagementPricingCalculator.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BillingandCostManagementPricingCalculatorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator.html#BillingandCostManagementPricingCalculator.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#close)
        """

    def batch_create_bill_scenario_commitment_modification(
        self, **kwargs: Unpack[BatchCreateBillScenarioCommitmentModificationRequestRequestTypeDef]
    ) -> BatchCreateBillScenarioCommitmentModificationResponseTypeDef:
        """
        Create Compute Savings Plans, EC2 Instance Savings Plans, or EC2 Reserved
        Instances commitments that you want to model in a Bill Scenario.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/batch_create_bill_scenario_commitment_modification.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#batch_create_bill_scenario_commitment_modification)
        """

    def batch_create_bill_scenario_usage_modification(
        self, **kwargs: Unpack[BatchCreateBillScenarioUsageModificationRequestRequestTypeDef]
    ) -> BatchCreateBillScenarioUsageModificationResponseTypeDef:
        """
        Create Amazon Web Services service usage that you want to model in a Bill
        Scenario.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/batch_create_bill_scenario_usage_modification.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#batch_create_bill_scenario_usage_modification)
        """

    def batch_create_workload_estimate_usage(
        self, **kwargs: Unpack[BatchCreateWorkloadEstimateUsageRequestRequestTypeDef]
    ) -> BatchCreateWorkloadEstimateUsageResponseTypeDef:
        """
        Create Amazon Web Services service usage that you want to model in a Workload
        Estimate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/batch_create_workload_estimate_usage.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#batch_create_workload_estimate_usage)
        """

    def batch_delete_bill_scenario_commitment_modification(
        self, **kwargs: Unpack[BatchDeleteBillScenarioCommitmentModificationRequestRequestTypeDef]
    ) -> BatchDeleteBillScenarioCommitmentModificationResponseTypeDef:
        """
        Delete commitment that you have created in a Bill Scenario.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/batch_delete_bill_scenario_commitment_modification.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#batch_delete_bill_scenario_commitment_modification)
        """

    def batch_delete_bill_scenario_usage_modification(
        self, **kwargs: Unpack[BatchDeleteBillScenarioUsageModificationRequestRequestTypeDef]
    ) -> BatchDeleteBillScenarioUsageModificationResponseTypeDef:
        """
        Delete usage that you have created in a Bill Scenario.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/batch_delete_bill_scenario_usage_modification.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#batch_delete_bill_scenario_usage_modification)
        """

    def batch_delete_workload_estimate_usage(
        self, **kwargs: Unpack[BatchDeleteWorkloadEstimateUsageRequestRequestTypeDef]
    ) -> BatchDeleteWorkloadEstimateUsageResponseTypeDef:
        """
        Delete usage that you have created in a Workload estimate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/batch_delete_workload_estimate_usage.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#batch_delete_workload_estimate_usage)
        """

    def batch_update_bill_scenario_commitment_modification(
        self, **kwargs: Unpack[BatchUpdateBillScenarioCommitmentModificationRequestRequestTypeDef]
    ) -> BatchUpdateBillScenarioCommitmentModificationResponseTypeDef:
        """
        Update a newly added or existing commitment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/batch_update_bill_scenario_commitment_modification.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#batch_update_bill_scenario_commitment_modification)
        """

    def batch_update_bill_scenario_usage_modification(
        self, **kwargs: Unpack[BatchUpdateBillScenarioUsageModificationRequestRequestTypeDef]
    ) -> BatchUpdateBillScenarioUsageModificationResponseTypeDef:
        """
        Update a newly added or existing usage lines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/batch_update_bill_scenario_usage_modification.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#batch_update_bill_scenario_usage_modification)
        """

    def batch_update_workload_estimate_usage(
        self, **kwargs: Unpack[BatchUpdateWorkloadEstimateUsageRequestRequestTypeDef]
    ) -> BatchUpdateWorkloadEstimateUsageResponseTypeDef:
        """
        Update a newly added or existing usage lines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/batch_update_workload_estimate_usage.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#batch_update_workload_estimate_usage)
        """

    def create_bill_estimate(
        self, **kwargs: Unpack[CreateBillEstimateRequestRequestTypeDef]
    ) -> CreateBillEstimateResponseTypeDef:
        """
        Create a Bill estimate from a Bill scenario.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/create_bill_estimate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#create_bill_estimate)
        """

    def create_bill_scenario(
        self, **kwargs: Unpack[CreateBillScenarioRequestRequestTypeDef]
    ) -> CreateBillScenarioResponseTypeDef:
        """
        Creates a new bill scenario to model potential changes to Amazon Web Services
        usage and costs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/create_bill_scenario.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#create_bill_scenario)
        """

    def create_workload_estimate(
        self, **kwargs: Unpack[CreateWorkloadEstimateRequestRequestTypeDef]
    ) -> CreateWorkloadEstimateResponseTypeDef:
        """
        Creates a new workload estimate to model costs for a specific workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/create_workload_estimate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#create_workload_estimate)
        """

    def delete_bill_estimate(
        self, **kwargs: Unpack[DeleteBillEstimateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing bill estimate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/delete_bill_estimate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#delete_bill_estimate)
        """

    def delete_bill_scenario(
        self, **kwargs: Unpack[DeleteBillScenarioRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing bill scenario.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/delete_bill_scenario.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#delete_bill_scenario)
        """

    def delete_workload_estimate(
        self, **kwargs: Unpack[DeleteWorkloadEstimateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing workload estimate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/delete_workload_estimate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#delete_workload_estimate)
        """

    def get_bill_estimate(
        self, **kwargs: Unpack[GetBillEstimateRequestRequestTypeDef]
    ) -> GetBillEstimateResponseTypeDef:
        """
        Retrieves details of a specific bill estimate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_bill_estimate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_bill_estimate)
        """

    def get_bill_scenario(
        self, **kwargs: Unpack[GetBillScenarioRequestRequestTypeDef]
    ) -> GetBillScenarioResponseTypeDef:
        """
        Retrieves details of a specific bill scenario.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_bill_scenario.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_bill_scenario)
        """

    def get_preferences(self) -> GetPreferencesResponseTypeDef:
        """
        Retrieves the current preferences for the Amazon Web Services Cost Explorer
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_preferences.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_preferences)
        """

    def get_workload_estimate(
        self, **kwargs: Unpack[GetWorkloadEstimateRequestRequestTypeDef]
    ) -> GetWorkloadEstimateResponseTypeDef:
        """
        Retrieves details of a specific workload estimate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_workload_estimate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_workload_estimate)
        """

    def list_bill_estimate_commitments(
        self, **kwargs: Unpack[ListBillEstimateCommitmentsRequestRequestTypeDef]
    ) -> ListBillEstimateCommitmentsResponseTypeDef:
        """
        Lists the commitments associated with a bill estimate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/list_bill_estimate_commitments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#list_bill_estimate_commitments)
        """

    def list_bill_estimate_input_commitment_modifications(
        self, **kwargs: Unpack[ListBillEstimateInputCommitmentModificationsRequestRequestTypeDef]
    ) -> ListBillEstimateInputCommitmentModificationsResponseTypeDef:
        """
        Lists the input commitment modifications associated with a bill estimate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/list_bill_estimate_input_commitment_modifications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#list_bill_estimate_input_commitment_modifications)
        """

    def list_bill_estimate_input_usage_modifications(
        self, **kwargs: Unpack[ListBillEstimateInputUsageModificationsRequestRequestTypeDef]
    ) -> ListBillEstimateInputUsageModificationsResponseTypeDef:
        """
        Lists the input usage modifications associated with a bill estimate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/list_bill_estimate_input_usage_modifications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#list_bill_estimate_input_usage_modifications)
        """

    def list_bill_estimate_line_items(
        self, **kwargs: Unpack[ListBillEstimateLineItemsRequestRequestTypeDef]
    ) -> ListBillEstimateLineItemsResponseTypeDef:
        """
        Lists the line items associated with a bill estimate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/list_bill_estimate_line_items.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#list_bill_estimate_line_items)
        """

    def list_bill_estimates(
        self, **kwargs: Unpack[ListBillEstimatesRequestRequestTypeDef]
    ) -> ListBillEstimatesResponseTypeDef:
        """
        Lists all bill estimates for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/list_bill_estimates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#list_bill_estimates)
        """

    def list_bill_scenario_commitment_modifications(
        self, **kwargs: Unpack[ListBillScenarioCommitmentModificationsRequestRequestTypeDef]
    ) -> ListBillScenarioCommitmentModificationsResponseTypeDef:
        """
        Lists the commitment modifications associated with a bill scenario.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/list_bill_scenario_commitment_modifications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#list_bill_scenario_commitment_modifications)
        """

    def list_bill_scenario_usage_modifications(
        self, **kwargs: Unpack[ListBillScenarioUsageModificationsRequestRequestTypeDef]
    ) -> ListBillScenarioUsageModificationsResponseTypeDef:
        """
        Lists the usage modifications associated with a bill scenario.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/list_bill_scenario_usage_modifications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#list_bill_scenario_usage_modifications)
        """

    def list_bill_scenarios(
        self, **kwargs: Unpack[ListBillScenariosRequestRequestTypeDef]
    ) -> ListBillScenariosResponseTypeDef:
        """
        Lists all bill scenarios for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/list_bill_scenarios.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#list_bill_scenarios)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags associated with a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#list_tags_for_resource)
        """

    def list_workload_estimate_usage(
        self, **kwargs: Unpack[ListWorkloadEstimateUsageRequestRequestTypeDef]
    ) -> ListWorkloadEstimateUsageResponseTypeDef:
        """
        Lists the usage associated with a workload estimate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/list_workload_estimate_usage.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#list_workload_estimate_usage)
        """

    def list_workload_estimates(
        self, **kwargs: Unpack[ListWorkloadEstimatesRequestRequestTypeDef]
    ) -> ListWorkloadEstimatesResponseTypeDef:
        """
        Lists all workload estimates for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/list_workload_estimates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#list_workload_estimates)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#untag_resource)
        """

    def update_bill_estimate(
        self, **kwargs: Unpack[UpdateBillEstimateRequestRequestTypeDef]
    ) -> UpdateBillEstimateResponseTypeDef:
        """
        Updates an existing bill estimate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/update_bill_estimate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#update_bill_estimate)
        """

    def update_bill_scenario(
        self, **kwargs: Unpack[UpdateBillScenarioRequestRequestTypeDef]
    ) -> UpdateBillScenarioResponseTypeDef:
        """
        Updates an existing bill scenario.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/update_bill_scenario.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#update_bill_scenario)
        """

    def update_preferences(
        self, **kwargs: Unpack[UpdatePreferencesRequestRequestTypeDef]
    ) -> UpdatePreferencesResponseTypeDef:
        """
        Updates the preferences for the Amazon Web Services Cost Explorer service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/update_preferences.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#update_preferences)
        """

    def update_workload_estimate(
        self, **kwargs: Unpack[UpdateWorkloadEstimateRequestRequestTypeDef]
    ) -> UpdateWorkloadEstimateResponseTypeDef:
        """
        Updates an existing workload estimate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/update_workload_estimate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#update_workload_estimate)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bill_estimate_commitments"]
    ) -> ListBillEstimateCommitmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bill_estimate_input_commitment_modifications"]
    ) -> ListBillEstimateInputCommitmentModificationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bill_estimate_input_usage_modifications"]
    ) -> ListBillEstimateInputUsageModificationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bill_estimate_line_items"]
    ) -> ListBillEstimateLineItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bill_estimates"]
    ) -> ListBillEstimatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bill_scenario_commitment_modifications"]
    ) -> ListBillScenarioCommitmentModificationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bill_scenario_usage_modifications"]
    ) -> ListBillScenarioUsageModificationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bill_scenarios"]
    ) -> ListBillScenariosPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_workload_estimate_usage"]
    ) -> ListWorkloadEstimateUsagePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_workload_estimates"]
    ) -> ListWorkloadEstimatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-pricing-calculator/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/client/#get_paginator)
        """
