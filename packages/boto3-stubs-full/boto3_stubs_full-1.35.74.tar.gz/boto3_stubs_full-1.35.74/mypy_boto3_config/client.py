"""
Type annotations for config service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_config.client import ConfigServiceClient

    session = Session()
    client: ConfigServiceClient = session.client("config")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeAggregateComplianceByConfigRulesPaginator,
    DescribeAggregateComplianceByConformancePacksPaginator,
    DescribeAggregationAuthorizationsPaginator,
    DescribeComplianceByConfigRulePaginator,
    DescribeComplianceByResourcePaginator,
    DescribeConfigRuleEvaluationStatusPaginator,
    DescribeConfigRulesPaginator,
    DescribeConfigurationAggregatorSourcesStatusPaginator,
    DescribeConfigurationAggregatorsPaginator,
    DescribeConformancePacksPaginator,
    DescribeConformancePackStatusPaginator,
    DescribeOrganizationConfigRulesPaginator,
    DescribeOrganizationConfigRuleStatusesPaginator,
    DescribeOrganizationConformancePacksPaginator,
    DescribeOrganizationConformancePackStatusesPaginator,
    DescribePendingAggregationRequestsPaginator,
    DescribeRemediationExecutionStatusPaginator,
    DescribeRetentionConfigurationsPaginator,
    GetAggregateComplianceDetailsByConfigRulePaginator,
    GetComplianceDetailsByConfigRulePaginator,
    GetComplianceDetailsByResourcePaginator,
    GetConformancePackComplianceSummaryPaginator,
    GetOrganizationConfigRuleDetailedStatusPaginator,
    GetOrganizationConformancePackDetailedStatusPaginator,
    GetResourceConfigHistoryPaginator,
    ListAggregateDiscoveredResourcesPaginator,
    ListConfigurationRecordersPaginator,
    ListDiscoveredResourcesPaginator,
    ListResourceEvaluationsPaginator,
    ListTagsForResourcePaginator,
    SelectAggregateResourceConfigPaginator,
    SelectResourceConfigPaginator,
)
from .type_defs import (
    AssociateResourceTypesRequestRequestTypeDef,
    AssociateResourceTypesResponseTypeDef,
    BatchGetAggregateResourceConfigRequestRequestTypeDef,
    BatchGetAggregateResourceConfigResponseTypeDef,
    BatchGetResourceConfigRequestRequestTypeDef,
    BatchGetResourceConfigResponseTypeDef,
    DeleteAggregationAuthorizationRequestRequestTypeDef,
    DeleteConfigRuleRequestRequestTypeDef,
    DeleteConfigurationAggregatorRequestRequestTypeDef,
    DeleteConfigurationRecorderRequestRequestTypeDef,
    DeleteConformancePackRequestRequestTypeDef,
    DeleteDeliveryChannelRequestRequestTypeDef,
    DeleteEvaluationResultsRequestRequestTypeDef,
    DeleteOrganizationConfigRuleRequestRequestTypeDef,
    DeleteOrganizationConformancePackRequestRequestTypeDef,
    DeletePendingAggregationRequestRequestRequestTypeDef,
    DeleteRemediationConfigurationRequestRequestTypeDef,
    DeleteRemediationExceptionsRequestRequestTypeDef,
    DeleteRemediationExceptionsResponseTypeDef,
    DeleteResourceConfigRequestRequestTypeDef,
    DeleteRetentionConfigurationRequestRequestTypeDef,
    DeleteServiceLinkedConfigurationRecorderRequestRequestTypeDef,
    DeleteServiceLinkedConfigurationRecorderResponseTypeDef,
    DeleteStoredQueryRequestRequestTypeDef,
    DeliverConfigSnapshotRequestRequestTypeDef,
    DeliverConfigSnapshotResponseTypeDef,
    DescribeAggregateComplianceByConfigRulesRequestRequestTypeDef,
    DescribeAggregateComplianceByConfigRulesResponseTypeDef,
    DescribeAggregateComplianceByConformancePacksRequestRequestTypeDef,
    DescribeAggregateComplianceByConformancePacksResponseTypeDef,
    DescribeAggregationAuthorizationsRequestRequestTypeDef,
    DescribeAggregationAuthorizationsResponseTypeDef,
    DescribeComplianceByConfigRuleRequestRequestTypeDef,
    DescribeComplianceByConfigRuleResponseTypeDef,
    DescribeComplianceByResourceRequestRequestTypeDef,
    DescribeComplianceByResourceResponseTypeDef,
    DescribeConfigRuleEvaluationStatusRequestRequestTypeDef,
    DescribeConfigRuleEvaluationStatusResponseTypeDef,
    DescribeConfigRulesRequestRequestTypeDef,
    DescribeConfigRulesResponseTypeDef,
    DescribeConfigurationAggregatorSourcesStatusRequestRequestTypeDef,
    DescribeConfigurationAggregatorSourcesStatusResponseTypeDef,
    DescribeConfigurationAggregatorsRequestRequestTypeDef,
    DescribeConfigurationAggregatorsResponseTypeDef,
    DescribeConfigurationRecordersRequestRequestTypeDef,
    DescribeConfigurationRecordersResponseTypeDef,
    DescribeConfigurationRecorderStatusRequestRequestTypeDef,
    DescribeConfigurationRecorderStatusResponseTypeDef,
    DescribeConformancePackComplianceRequestRequestTypeDef,
    DescribeConformancePackComplianceResponseTypeDef,
    DescribeConformancePacksRequestRequestTypeDef,
    DescribeConformancePacksResponseTypeDef,
    DescribeConformancePackStatusRequestRequestTypeDef,
    DescribeConformancePackStatusResponseTypeDef,
    DescribeDeliveryChannelsRequestRequestTypeDef,
    DescribeDeliveryChannelsResponseTypeDef,
    DescribeDeliveryChannelStatusRequestRequestTypeDef,
    DescribeDeliveryChannelStatusResponseTypeDef,
    DescribeOrganizationConfigRulesRequestRequestTypeDef,
    DescribeOrganizationConfigRulesResponseTypeDef,
    DescribeOrganizationConfigRuleStatusesRequestRequestTypeDef,
    DescribeOrganizationConfigRuleStatusesResponseTypeDef,
    DescribeOrganizationConformancePacksRequestRequestTypeDef,
    DescribeOrganizationConformancePacksResponseTypeDef,
    DescribeOrganizationConformancePackStatusesRequestRequestTypeDef,
    DescribeOrganizationConformancePackStatusesResponseTypeDef,
    DescribePendingAggregationRequestsRequestRequestTypeDef,
    DescribePendingAggregationRequestsResponseTypeDef,
    DescribeRemediationConfigurationsRequestRequestTypeDef,
    DescribeRemediationConfigurationsResponseTypeDef,
    DescribeRemediationExceptionsRequestRequestTypeDef,
    DescribeRemediationExceptionsResponseTypeDef,
    DescribeRemediationExecutionStatusRequestRequestTypeDef,
    DescribeRemediationExecutionStatusResponseTypeDef,
    DescribeRetentionConfigurationsRequestRequestTypeDef,
    DescribeRetentionConfigurationsResponseTypeDef,
    DisassociateResourceTypesRequestRequestTypeDef,
    DisassociateResourceTypesResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAggregateComplianceDetailsByConfigRuleRequestRequestTypeDef,
    GetAggregateComplianceDetailsByConfigRuleResponseTypeDef,
    GetAggregateConfigRuleComplianceSummaryRequestRequestTypeDef,
    GetAggregateConfigRuleComplianceSummaryResponseTypeDef,
    GetAggregateConformancePackComplianceSummaryRequestRequestTypeDef,
    GetAggregateConformancePackComplianceSummaryResponseTypeDef,
    GetAggregateDiscoveredResourceCountsRequestRequestTypeDef,
    GetAggregateDiscoveredResourceCountsResponseTypeDef,
    GetAggregateResourceConfigRequestRequestTypeDef,
    GetAggregateResourceConfigResponseTypeDef,
    GetComplianceDetailsByConfigRuleRequestRequestTypeDef,
    GetComplianceDetailsByConfigRuleResponseTypeDef,
    GetComplianceDetailsByResourceRequestRequestTypeDef,
    GetComplianceDetailsByResourceResponseTypeDef,
    GetComplianceSummaryByConfigRuleResponseTypeDef,
    GetComplianceSummaryByResourceTypeRequestRequestTypeDef,
    GetComplianceSummaryByResourceTypeResponseTypeDef,
    GetConformancePackComplianceDetailsRequestRequestTypeDef,
    GetConformancePackComplianceDetailsResponseTypeDef,
    GetConformancePackComplianceSummaryRequestRequestTypeDef,
    GetConformancePackComplianceSummaryResponseTypeDef,
    GetCustomRulePolicyRequestRequestTypeDef,
    GetCustomRulePolicyResponseTypeDef,
    GetDiscoveredResourceCountsRequestRequestTypeDef,
    GetDiscoveredResourceCountsResponseTypeDef,
    GetOrganizationConfigRuleDetailedStatusRequestRequestTypeDef,
    GetOrganizationConfigRuleDetailedStatusResponseTypeDef,
    GetOrganizationConformancePackDetailedStatusRequestRequestTypeDef,
    GetOrganizationConformancePackDetailedStatusResponseTypeDef,
    GetOrganizationCustomRulePolicyRequestRequestTypeDef,
    GetOrganizationCustomRulePolicyResponseTypeDef,
    GetResourceConfigHistoryRequestRequestTypeDef,
    GetResourceConfigHistoryResponseTypeDef,
    GetResourceEvaluationSummaryRequestRequestTypeDef,
    GetResourceEvaluationSummaryResponseTypeDef,
    GetStoredQueryRequestRequestTypeDef,
    GetStoredQueryResponseTypeDef,
    ListAggregateDiscoveredResourcesRequestRequestTypeDef,
    ListAggregateDiscoveredResourcesResponseTypeDef,
    ListConfigurationRecordersRequestRequestTypeDef,
    ListConfigurationRecordersResponseTypeDef,
    ListConformancePackComplianceScoresRequestRequestTypeDef,
    ListConformancePackComplianceScoresResponseTypeDef,
    ListDiscoveredResourcesRequestRequestTypeDef,
    ListDiscoveredResourcesResponseTypeDef,
    ListResourceEvaluationsRequestRequestTypeDef,
    ListResourceEvaluationsResponseTypeDef,
    ListStoredQueriesRequestRequestTypeDef,
    ListStoredQueriesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutAggregationAuthorizationRequestRequestTypeDef,
    PutAggregationAuthorizationResponseTypeDef,
    PutConfigRuleRequestRequestTypeDef,
    PutConfigurationAggregatorRequestRequestTypeDef,
    PutConfigurationAggregatorResponseTypeDef,
    PutConfigurationRecorderRequestRequestTypeDef,
    PutConformancePackRequestRequestTypeDef,
    PutConformancePackResponseTypeDef,
    PutDeliveryChannelRequestRequestTypeDef,
    PutEvaluationsRequestRequestTypeDef,
    PutEvaluationsResponseTypeDef,
    PutExternalEvaluationRequestRequestTypeDef,
    PutOrganizationConfigRuleRequestRequestTypeDef,
    PutOrganizationConfigRuleResponseTypeDef,
    PutOrganizationConformancePackRequestRequestTypeDef,
    PutOrganizationConformancePackResponseTypeDef,
    PutRemediationConfigurationsRequestRequestTypeDef,
    PutRemediationConfigurationsResponseTypeDef,
    PutRemediationExceptionsRequestRequestTypeDef,
    PutRemediationExceptionsResponseTypeDef,
    PutResourceConfigRequestRequestTypeDef,
    PutRetentionConfigurationRequestRequestTypeDef,
    PutRetentionConfigurationResponseTypeDef,
    PutServiceLinkedConfigurationRecorderRequestRequestTypeDef,
    PutServiceLinkedConfigurationRecorderResponseTypeDef,
    PutStoredQueryRequestRequestTypeDef,
    PutStoredQueryResponseTypeDef,
    SelectAggregateResourceConfigRequestRequestTypeDef,
    SelectAggregateResourceConfigResponseTypeDef,
    SelectResourceConfigRequestRequestTypeDef,
    SelectResourceConfigResponseTypeDef,
    StartConfigRulesEvaluationRequestRequestTypeDef,
    StartConfigurationRecorderRequestRequestTypeDef,
    StartRemediationExecutionRequestRequestTypeDef,
    StartRemediationExecutionResponseTypeDef,
    StartResourceEvaluationRequestRequestTypeDef,
    StartResourceEvaluationResponseTypeDef,
    StopConfigurationRecorderRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ConfigServiceClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ConformancePackTemplateValidationException: Type[BotocoreClientError]
    IdempotentParameterMismatch: Type[BotocoreClientError]
    InsufficientDeliveryPolicyException: Type[BotocoreClientError]
    InsufficientPermissionsException: Type[BotocoreClientError]
    InvalidConfigurationRecorderNameException: Type[BotocoreClientError]
    InvalidDeliveryChannelNameException: Type[BotocoreClientError]
    InvalidExpressionException: Type[BotocoreClientError]
    InvalidLimitException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidRecordingGroupException: Type[BotocoreClientError]
    InvalidResultTokenException: Type[BotocoreClientError]
    InvalidRoleException: Type[BotocoreClientError]
    InvalidS3KeyPrefixException: Type[BotocoreClientError]
    InvalidS3KmsKeyArnException: Type[BotocoreClientError]
    InvalidSNSTopicARNException: Type[BotocoreClientError]
    InvalidTimeRangeException: Type[BotocoreClientError]
    LastDeliveryChannelDeleteFailedException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MaxActiveResourcesExceededException: Type[BotocoreClientError]
    MaxNumberOfConfigRulesExceededException: Type[BotocoreClientError]
    MaxNumberOfConfigurationRecordersExceededException: Type[BotocoreClientError]
    MaxNumberOfConformancePacksExceededException: Type[BotocoreClientError]
    MaxNumberOfDeliveryChannelsExceededException: Type[BotocoreClientError]
    MaxNumberOfOrganizationConfigRulesExceededException: Type[BotocoreClientError]
    MaxNumberOfOrganizationConformancePacksExceededException: Type[BotocoreClientError]
    MaxNumberOfRetentionConfigurationsExceededException: Type[BotocoreClientError]
    NoAvailableConfigurationRecorderException: Type[BotocoreClientError]
    NoAvailableDeliveryChannelException: Type[BotocoreClientError]
    NoAvailableOrganizationException: Type[BotocoreClientError]
    NoRunningConfigurationRecorderException: Type[BotocoreClientError]
    NoSuchBucketException: Type[BotocoreClientError]
    NoSuchConfigRuleException: Type[BotocoreClientError]
    NoSuchConfigRuleInConformancePackException: Type[BotocoreClientError]
    NoSuchConfigurationAggregatorException: Type[BotocoreClientError]
    NoSuchConfigurationRecorderException: Type[BotocoreClientError]
    NoSuchConformancePackException: Type[BotocoreClientError]
    NoSuchDeliveryChannelException: Type[BotocoreClientError]
    NoSuchOrganizationConfigRuleException: Type[BotocoreClientError]
    NoSuchOrganizationConformancePackException: Type[BotocoreClientError]
    NoSuchRemediationConfigurationException: Type[BotocoreClientError]
    NoSuchRemediationExceptionException: Type[BotocoreClientError]
    NoSuchRetentionConfigurationException: Type[BotocoreClientError]
    OrganizationAccessDeniedException: Type[BotocoreClientError]
    OrganizationAllFeaturesNotEnabledException: Type[BotocoreClientError]
    OrganizationConformancePackTemplateValidationException: Type[BotocoreClientError]
    OversizedConfigurationItemException: Type[BotocoreClientError]
    RemediationInProgressException: Type[BotocoreClientError]
    ResourceConcurrentModificationException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotDiscoveredException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnmodifiableEntityException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ConfigServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConfigServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#close)
        """

    def associate_resource_types(
        self, **kwargs: Unpack[AssociateResourceTypesRequestRequestTypeDef]
    ) -> AssociateResourceTypesResponseTypeDef:
        """
        Adds all resource types specified in the <code>ResourceTypes</code> list to the
        <a
        href="https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html">RecordingGroup</a>
        of specified configuration recorder and includes those resource types when
        recording.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/associate_resource_types.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#associate_resource_types)
        """

    def batch_get_aggregate_resource_config(
        self, **kwargs: Unpack[BatchGetAggregateResourceConfigRequestRequestTypeDef]
    ) -> BatchGetAggregateResourceConfigResponseTypeDef:
        """
        Returns the current configuration items for resources that are present in your
        Config aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/batch_get_aggregate_resource_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#batch_get_aggregate_resource_config)
        """

    def batch_get_resource_config(
        self, **kwargs: Unpack[BatchGetResourceConfigRequestRequestTypeDef]
    ) -> BatchGetResourceConfigResponseTypeDef:
        """
        Returns the <code>BaseConfigurationItem</code> for one or more requested
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/batch_get_resource_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#batch_get_resource_config)
        """

    def delete_aggregation_authorization(
        self, **kwargs: Unpack[DeleteAggregationAuthorizationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the authorization granted to the specified configuration aggregator
        account in a specified region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_aggregation_authorization.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_aggregation_authorization)
        """

    def delete_config_rule(
        self, **kwargs: Unpack[DeleteConfigRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Config rule and all of its evaluation results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_config_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_config_rule)
        """

    def delete_configuration_aggregator(
        self, **kwargs: Unpack[DeleteConfigurationAggregatorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified configuration aggregator and the aggregated data
        associated with the aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_configuration_aggregator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_configuration_aggregator)
        """

    def delete_configuration_recorder(
        self, **kwargs: Unpack[DeleteConfigurationRecorderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the customer managed configuration recorder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_configuration_recorder.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_configuration_recorder)
        """

    def delete_conformance_pack(
        self, **kwargs: Unpack[DeleteConformancePackRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified conformance pack and all the Config rules, remediation
        actions, and all evaluation results within that conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_conformance_pack.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_conformance_pack)
        """

    def delete_delivery_channel(
        self, **kwargs: Unpack[DeleteDeliveryChannelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the delivery channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_delivery_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_delivery_channel)
        """

    def delete_evaluation_results(
        self, **kwargs: Unpack[DeleteEvaluationResultsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the evaluation results for the specified Config rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_evaluation_results.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_evaluation_results)
        """

    def delete_organization_config_rule(
        self, **kwargs: Unpack[DeleteOrganizationConfigRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified organization Config rule and all of its evaluation
        results from all member accounts in that organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_organization_config_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_organization_config_rule)
        """

    def delete_organization_conformance_pack(
        self, **kwargs: Unpack[DeleteOrganizationConformancePackRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified organization conformance pack and all of the Config rules
        and remediation actions from all member accounts in that organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_organization_conformance_pack.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_organization_conformance_pack)
        """

    def delete_pending_aggregation_request(
        self, **kwargs: Unpack[DeletePendingAggregationRequestRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes pending authorization requests for a specified aggregator account in a
        specified region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_pending_aggregation_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_pending_aggregation_request)
        """

    def delete_remediation_configuration(
        self, **kwargs: Unpack[DeleteRemediationConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the remediation configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_remediation_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_remediation_configuration)
        """

    def delete_remediation_exceptions(
        self, **kwargs: Unpack[DeleteRemediationExceptionsRequestRequestTypeDef]
    ) -> DeleteRemediationExceptionsResponseTypeDef:
        """
        Deletes one or more remediation exceptions mentioned in the resource keys.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_remediation_exceptions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_remediation_exceptions)
        """

    def delete_resource_config(
        self, **kwargs: Unpack[DeleteResourceConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Records the configuration state for a custom resource that has been deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_resource_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_resource_config)
        """

    def delete_retention_configuration(
        self, **kwargs: Unpack[DeleteRetentionConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the retention configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_retention_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_retention_configuration)
        """

    def delete_service_linked_configuration_recorder(
        self, **kwargs: Unpack[DeleteServiceLinkedConfigurationRecorderRequestRequestTypeDef]
    ) -> DeleteServiceLinkedConfigurationRecorderResponseTypeDef:
        """
        Deletes an existing service-linked configuration recorder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_service_linked_configuration_recorder.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_service_linked_configuration_recorder)
        """

    def delete_stored_query(
        self, **kwargs: Unpack[DeleteStoredQueryRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the stored query for a single Amazon Web Services account and a single
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/delete_stored_query.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#delete_stored_query)
        """

    def deliver_config_snapshot(
        self, **kwargs: Unpack[DeliverConfigSnapshotRequestRequestTypeDef]
    ) -> DeliverConfigSnapshotResponseTypeDef:
        """
        Schedules delivery of a configuration snapshot to the Amazon S3 bucket in the
        specified delivery channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/deliver_config_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#deliver_config_snapshot)
        """

    def describe_aggregate_compliance_by_config_rules(
        self, **kwargs: Unpack[DescribeAggregateComplianceByConfigRulesRequestRequestTypeDef]
    ) -> DescribeAggregateComplianceByConfigRulesResponseTypeDef:
        """
        Returns a list of compliant and noncompliant rules with the number of resources
        for compliant and noncompliant rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_aggregate_compliance_by_config_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_aggregate_compliance_by_config_rules)
        """

    def describe_aggregate_compliance_by_conformance_packs(
        self, **kwargs: Unpack[DescribeAggregateComplianceByConformancePacksRequestRequestTypeDef]
    ) -> DescribeAggregateComplianceByConformancePacksResponseTypeDef:
        """
        Returns a list of the existing and deleted conformance packs and their
        associated compliance status with the count of compliant and noncompliant
        Config rules within each conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_aggregate_compliance_by_conformance_packs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_aggregate_compliance_by_conformance_packs)
        """

    def describe_aggregation_authorizations(
        self, **kwargs: Unpack[DescribeAggregationAuthorizationsRequestRequestTypeDef]
    ) -> DescribeAggregationAuthorizationsResponseTypeDef:
        """
        Returns a list of authorizations granted to various aggregator accounts and
        regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_aggregation_authorizations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_aggregation_authorizations)
        """

    def describe_compliance_by_config_rule(
        self, **kwargs: Unpack[DescribeComplianceByConfigRuleRequestRequestTypeDef]
    ) -> DescribeComplianceByConfigRuleResponseTypeDef:
        """
        Indicates whether the specified Config rules are compliant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_compliance_by_config_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_compliance_by_config_rule)
        """

    def describe_compliance_by_resource(
        self, **kwargs: Unpack[DescribeComplianceByResourceRequestRequestTypeDef]
    ) -> DescribeComplianceByResourceResponseTypeDef:
        """
        Indicates whether the specified Amazon Web Services resources are compliant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_compliance_by_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_compliance_by_resource)
        """

    def describe_config_rule_evaluation_status(
        self, **kwargs: Unpack[DescribeConfigRuleEvaluationStatusRequestRequestTypeDef]
    ) -> DescribeConfigRuleEvaluationStatusResponseTypeDef:
        """
        Returns status information for each of your Config managed rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_config_rule_evaluation_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_config_rule_evaluation_status)
        """

    def describe_config_rules(
        self, **kwargs: Unpack[DescribeConfigRulesRequestRequestTypeDef]
    ) -> DescribeConfigRulesResponseTypeDef:
        """
        Returns details about your Config rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_config_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_config_rules)
        """

    def describe_configuration_aggregator_sources_status(
        self, **kwargs: Unpack[DescribeConfigurationAggregatorSourcesStatusRequestRequestTypeDef]
    ) -> DescribeConfigurationAggregatorSourcesStatusResponseTypeDef:
        """
        Returns status information for sources within an aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_configuration_aggregator_sources_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_configuration_aggregator_sources_status)
        """

    def describe_configuration_aggregators(
        self, **kwargs: Unpack[DescribeConfigurationAggregatorsRequestRequestTypeDef]
    ) -> DescribeConfigurationAggregatorsResponseTypeDef:
        """
        Returns the details of one or more configuration aggregators.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_configuration_aggregators.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_configuration_aggregators)
        """

    def describe_configuration_recorder_status(
        self, **kwargs: Unpack[DescribeConfigurationRecorderStatusRequestRequestTypeDef]
    ) -> DescribeConfigurationRecorderStatusResponseTypeDef:
        """
        Returns the current status of the configuration recorder you specify as well as
        the status of the last recording event for the configuration recorders.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_configuration_recorder_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_configuration_recorder_status)
        """

    def describe_configuration_recorders(
        self, **kwargs: Unpack[DescribeConfigurationRecordersRequestRequestTypeDef]
    ) -> DescribeConfigurationRecordersResponseTypeDef:
        """
        Returns details for the configuration recorder you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_configuration_recorders.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_configuration_recorders)
        """

    def describe_conformance_pack_compliance(
        self, **kwargs: Unpack[DescribeConformancePackComplianceRequestRequestTypeDef]
    ) -> DescribeConformancePackComplianceResponseTypeDef:
        """
        Returns compliance details for each rule in that conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_conformance_pack_compliance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_conformance_pack_compliance)
        """

    def describe_conformance_pack_status(
        self, **kwargs: Unpack[DescribeConformancePackStatusRequestRequestTypeDef]
    ) -> DescribeConformancePackStatusResponseTypeDef:
        """
        Provides one or more conformance packs deployment status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_conformance_pack_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_conformance_pack_status)
        """

    def describe_conformance_packs(
        self, **kwargs: Unpack[DescribeConformancePacksRequestRequestTypeDef]
    ) -> DescribeConformancePacksResponseTypeDef:
        """
        Returns a list of one or more conformance packs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_conformance_packs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_conformance_packs)
        """

    def describe_delivery_channel_status(
        self, **kwargs: Unpack[DescribeDeliveryChannelStatusRequestRequestTypeDef]
    ) -> DescribeDeliveryChannelStatusResponseTypeDef:
        """
        Returns the current status of the specified delivery channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_delivery_channel_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_delivery_channel_status)
        """

    def describe_delivery_channels(
        self, **kwargs: Unpack[DescribeDeliveryChannelsRequestRequestTypeDef]
    ) -> DescribeDeliveryChannelsResponseTypeDef:
        """
        Returns details about the specified delivery channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_delivery_channels.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_delivery_channels)
        """

    def describe_organization_config_rule_statuses(
        self, **kwargs: Unpack[DescribeOrganizationConfigRuleStatusesRequestRequestTypeDef]
    ) -> DescribeOrganizationConfigRuleStatusesResponseTypeDef:
        """
        Provides organization Config rule deployment status for an organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_organization_config_rule_statuses.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_organization_config_rule_statuses)
        """

    def describe_organization_config_rules(
        self, **kwargs: Unpack[DescribeOrganizationConfigRulesRequestRequestTypeDef]
    ) -> DescribeOrganizationConfigRulesResponseTypeDef:
        """
        Returns a list of organization Config rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_organization_config_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_organization_config_rules)
        """

    def describe_organization_conformance_pack_statuses(
        self, **kwargs: Unpack[DescribeOrganizationConformancePackStatusesRequestRequestTypeDef]
    ) -> DescribeOrganizationConformancePackStatusesResponseTypeDef:
        """
        Provides organization conformance pack deployment status for an organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_organization_conformance_pack_statuses.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_organization_conformance_pack_statuses)
        """

    def describe_organization_conformance_packs(
        self, **kwargs: Unpack[DescribeOrganizationConformancePacksRequestRequestTypeDef]
    ) -> DescribeOrganizationConformancePacksResponseTypeDef:
        """
        Returns a list of organization conformance packs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_organization_conformance_packs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_organization_conformance_packs)
        """

    def describe_pending_aggregation_requests(
        self, **kwargs: Unpack[DescribePendingAggregationRequestsRequestRequestTypeDef]
    ) -> DescribePendingAggregationRequestsResponseTypeDef:
        """
        Returns a list of all pending aggregation requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_pending_aggregation_requests.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_pending_aggregation_requests)
        """

    def describe_remediation_configurations(
        self, **kwargs: Unpack[DescribeRemediationConfigurationsRequestRequestTypeDef]
    ) -> DescribeRemediationConfigurationsResponseTypeDef:
        """
        Returns the details of one or more remediation configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_remediation_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_remediation_configurations)
        """

    def describe_remediation_exceptions(
        self, **kwargs: Unpack[DescribeRemediationExceptionsRequestRequestTypeDef]
    ) -> DescribeRemediationExceptionsResponseTypeDef:
        """
        Returns the details of one or more remediation exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_remediation_exceptions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_remediation_exceptions)
        """

    def describe_remediation_execution_status(
        self, **kwargs: Unpack[DescribeRemediationExecutionStatusRequestRequestTypeDef]
    ) -> DescribeRemediationExecutionStatusResponseTypeDef:
        """
        Provides a detailed view of a Remediation Execution for a set of resources
        including state, timestamps for when steps for the remediation execution occur,
        and any error messages for steps that have failed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_remediation_execution_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_remediation_execution_status)
        """

    def describe_retention_configurations(
        self, **kwargs: Unpack[DescribeRetentionConfigurationsRequestRequestTypeDef]
    ) -> DescribeRetentionConfigurationsResponseTypeDef:
        """
        Returns the details of one or more retention configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/describe_retention_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#describe_retention_configurations)
        """

    def disassociate_resource_types(
        self, **kwargs: Unpack[DisassociateResourceTypesRequestRequestTypeDef]
    ) -> DisassociateResourceTypesResponseTypeDef:
        """
        Removes all resource types specified in the <code>ResourceTypes</code> list
        from the <a
        href="https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html">RecordingGroup</a>
        of configuration recorder and excludes these resource types when recording.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/disassociate_resource_types.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#disassociate_resource_types)
        """

    def get_aggregate_compliance_details_by_config_rule(
        self, **kwargs: Unpack[GetAggregateComplianceDetailsByConfigRuleRequestRequestTypeDef]
    ) -> GetAggregateComplianceDetailsByConfigRuleResponseTypeDef:
        """
        Returns the evaluation results for the specified Config rule for a specific
        resource in a rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_aggregate_compliance_details_by_config_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_aggregate_compliance_details_by_config_rule)
        """

    def get_aggregate_config_rule_compliance_summary(
        self, **kwargs: Unpack[GetAggregateConfigRuleComplianceSummaryRequestRequestTypeDef]
    ) -> GetAggregateConfigRuleComplianceSummaryResponseTypeDef:
        """
        Returns the number of compliant and noncompliant rules for one or more accounts
        and regions in an aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_aggregate_config_rule_compliance_summary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_aggregate_config_rule_compliance_summary)
        """

    def get_aggregate_conformance_pack_compliance_summary(
        self, **kwargs: Unpack[GetAggregateConformancePackComplianceSummaryRequestRequestTypeDef]
    ) -> GetAggregateConformancePackComplianceSummaryResponseTypeDef:
        """
        Returns the count of compliant and noncompliant conformance packs across all
        Amazon Web Services accounts and Amazon Web Services Regions in an aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_aggregate_conformance_pack_compliance_summary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_aggregate_conformance_pack_compliance_summary)
        """

    def get_aggregate_discovered_resource_counts(
        self, **kwargs: Unpack[GetAggregateDiscoveredResourceCountsRequestRequestTypeDef]
    ) -> GetAggregateDiscoveredResourceCountsResponseTypeDef:
        """
        Returns the resource counts across accounts and regions that are present in
        your Config aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_aggregate_discovered_resource_counts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_aggregate_discovered_resource_counts)
        """

    def get_aggregate_resource_config(
        self, **kwargs: Unpack[GetAggregateResourceConfigRequestRequestTypeDef]
    ) -> GetAggregateResourceConfigResponseTypeDef:
        """
        Returns configuration item that is aggregated for your specific resource in a
        specific source account and region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_aggregate_resource_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_aggregate_resource_config)
        """

    def get_compliance_details_by_config_rule(
        self, **kwargs: Unpack[GetComplianceDetailsByConfigRuleRequestRequestTypeDef]
    ) -> GetComplianceDetailsByConfigRuleResponseTypeDef:
        """
        Returns the evaluation results for the specified Config rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_compliance_details_by_config_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_compliance_details_by_config_rule)
        """

    def get_compliance_details_by_resource(
        self, **kwargs: Unpack[GetComplianceDetailsByResourceRequestRequestTypeDef]
    ) -> GetComplianceDetailsByResourceResponseTypeDef:
        """
        Returns the evaluation results for the specified Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_compliance_details_by_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_compliance_details_by_resource)
        """

    def get_compliance_summary_by_config_rule(
        self,
    ) -> GetComplianceSummaryByConfigRuleResponseTypeDef:
        """
        Returns the number of Config rules that are compliant and noncompliant, up to a
        maximum of 25 for each.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_compliance_summary_by_config_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_compliance_summary_by_config_rule)
        """

    def get_compliance_summary_by_resource_type(
        self, **kwargs: Unpack[GetComplianceSummaryByResourceTypeRequestRequestTypeDef]
    ) -> GetComplianceSummaryByResourceTypeResponseTypeDef:
        """
        Returns the number of resources that are compliant and the number that are
        noncompliant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_compliance_summary_by_resource_type.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_compliance_summary_by_resource_type)
        """

    def get_conformance_pack_compliance_details(
        self, **kwargs: Unpack[GetConformancePackComplianceDetailsRequestRequestTypeDef]
    ) -> GetConformancePackComplianceDetailsResponseTypeDef:
        """
        Returns compliance details of a conformance pack for all Amazon Web Services
        resources that are monitered by conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_conformance_pack_compliance_details.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_conformance_pack_compliance_details)
        """

    def get_conformance_pack_compliance_summary(
        self, **kwargs: Unpack[GetConformancePackComplianceSummaryRequestRequestTypeDef]
    ) -> GetConformancePackComplianceSummaryResponseTypeDef:
        """
        Returns compliance details for the conformance pack based on the cumulative
        compliance results of all the rules in that conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_conformance_pack_compliance_summary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_conformance_pack_compliance_summary)
        """

    def get_custom_rule_policy(
        self, **kwargs: Unpack[GetCustomRulePolicyRequestRequestTypeDef]
    ) -> GetCustomRulePolicyResponseTypeDef:
        """
        Returns the policy definition containing the logic for your Config Custom
        Policy rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_custom_rule_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_custom_rule_policy)
        """

    def get_discovered_resource_counts(
        self, **kwargs: Unpack[GetDiscoveredResourceCountsRequestRequestTypeDef]
    ) -> GetDiscoveredResourceCountsResponseTypeDef:
        """
        Returns the resource types, the number of each resource type, and the total
        number of resources that Config is recording in this region for your Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_discovered_resource_counts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_discovered_resource_counts)
        """

    def get_organization_config_rule_detailed_status(
        self, **kwargs: Unpack[GetOrganizationConfigRuleDetailedStatusRequestRequestTypeDef]
    ) -> GetOrganizationConfigRuleDetailedStatusResponseTypeDef:
        """
        Returns detailed status for each member account within an organization for a
        given organization Config rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_organization_config_rule_detailed_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_organization_config_rule_detailed_status)
        """

    def get_organization_conformance_pack_detailed_status(
        self, **kwargs: Unpack[GetOrganizationConformancePackDetailedStatusRequestRequestTypeDef]
    ) -> GetOrganizationConformancePackDetailedStatusResponseTypeDef:
        """
        Returns detailed status for each member account within an organization for a
        given organization conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_organization_conformance_pack_detailed_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_organization_conformance_pack_detailed_status)
        """

    def get_organization_custom_rule_policy(
        self, **kwargs: Unpack[GetOrganizationCustomRulePolicyRequestRequestTypeDef]
    ) -> GetOrganizationCustomRulePolicyResponseTypeDef:
        """
        Returns the policy definition containing the logic for your organization Config
        Custom Policy rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_organization_custom_rule_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_organization_custom_rule_policy)
        """

    def get_resource_config_history(
        self, **kwargs: Unpack[GetResourceConfigHistoryRequestRequestTypeDef]
    ) -> GetResourceConfigHistoryResponseTypeDef:
        """
        For accurate reporting on the compliance status, you must record the
        <code>AWS::Config::ResourceCompliance</code> resource type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_resource_config_history.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_resource_config_history)
        """

    def get_resource_evaluation_summary(
        self, **kwargs: Unpack[GetResourceEvaluationSummaryRequestRequestTypeDef]
    ) -> GetResourceEvaluationSummaryResponseTypeDef:
        """
        Returns a summary of resource evaluation for the specified resource evaluation
        ID from the proactive rules that were run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_resource_evaluation_summary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_resource_evaluation_summary)
        """

    def get_stored_query(
        self, **kwargs: Unpack[GetStoredQueryRequestRequestTypeDef]
    ) -> GetStoredQueryResponseTypeDef:
        """
        Returns the details of a specific stored query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_stored_query.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_stored_query)
        """

    def list_aggregate_discovered_resources(
        self, **kwargs: Unpack[ListAggregateDiscoveredResourcesRequestRequestTypeDef]
    ) -> ListAggregateDiscoveredResourcesResponseTypeDef:
        """
        Accepts a resource type and returns a list of resource identifiers that are
        aggregated for a specific resource type across accounts and regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/list_aggregate_discovered_resources.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#list_aggregate_discovered_resources)
        """

    def list_configuration_recorders(
        self, **kwargs: Unpack[ListConfigurationRecordersRequestRequestTypeDef]
    ) -> ListConfigurationRecordersResponseTypeDef:
        """
        Returns a list of configuration recorders depending on the filters you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/list_configuration_recorders.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#list_configuration_recorders)
        """

    def list_conformance_pack_compliance_scores(
        self, **kwargs: Unpack[ListConformancePackComplianceScoresRequestRequestTypeDef]
    ) -> ListConformancePackComplianceScoresResponseTypeDef:
        """
        Returns a list of conformance pack compliance scores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/list_conformance_pack_compliance_scores.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#list_conformance_pack_compliance_scores)
        """

    def list_discovered_resources(
        self, **kwargs: Unpack[ListDiscoveredResourcesRequestRequestTypeDef]
    ) -> ListDiscoveredResourcesResponseTypeDef:
        """
        Accepts a resource type and returns a list of resource identifiers for the
        resources of that type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/list_discovered_resources.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#list_discovered_resources)
        """

    def list_resource_evaluations(
        self, **kwargs: Unpack[ListResourceEvaluationsRequestRequestTypeDef]
    ) -> ListResourceEvaluationsResponseTypeDef:
        """
        Returns a list of proactive resource evaluations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/list_resource_evaluations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#list_resource_evaluations)
        """

    def list_stored_queries(
        self, **kwargs: Unpack[ListStoredQueriesRequestRequestTypeDef]
    ) -> ListStoredQueriesResponseTypeDef:
        """
        Lists the stored queries for a single Amazon Web Services account and a single
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/list_stored_queries.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#list_stored_queries)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags for Config resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#list_tags_for_resource)
        """

    def put_aggregation_authorization(
        self, **kwargs: Unpack[PutAggregationAuthorizationRequestRequestTypeDef]
    ) -> PutAggregationAuthorizationResponseTypeDef:
        """
        Authorizes the aggregator account and region to collect data from the source
        account and region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_aggregation_authorization.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_aggregation_authorization)
        """

    def put_config_rule(
        self, **kwargs: Unpack[PutConfigRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates an Config rule to evaluate if your Amazon Web Services
        resources comply with your desired configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_config_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_config_rule)
        """

    def put_configuration_aggregator(
        self, **kwargs: Unpack[PutConfigurationAggregatorRequestRequestTypeDef]
    ) -> PutConfigurationAggregatorResponseTypeDef:
        """
        Creates and updates the configuration aggregator with the selected source
        accounts and regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_configuration_aggregator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_configuration_aggregator)
        """

    def put_configuration_recorder(
        self, **kwargs: Unpack[PutConfigurationRecorderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates the customer managed configuration recorder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_configuration_recorder.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_configuration_recorder)
        """

    def put_conformance_pack(
        self, **kwargs: Unpack[PutConformancePackRequestRequestTypeDef]
    ) -> PutConformancePackResponseTypeDef:
        """
        Creates or updates a conformance pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_conformance_pack.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_conformance_pack)
        """

    def put_delivery_channel(
        self, **kwargs: Unpack[PutDeliveryChannelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates a delivery channel to deliver configuration information and
        other compliance information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_delivery_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_delivery_channel)
        """

    def put_evaluations(
        self, **kwargs: Unpack[PutEvaluationsRequestRequestTypeDef]
    ) -> PutEvaluationsResponseTypeDef:
        """
        Used by an Lambda function to deliver evaluation results to Config.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_evaluations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_evaluations)
        """

    def put_external_evaluation(
        self, **kwargs: Unpack[PutExternalEvaluationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Add or updates the evaluations for process checks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_external_evaluation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_external_evaluation)
        """

    def put_organization_config_rule(
        self, **kwargs: Unpack[PutOrganizationConfigRuleRequestRequestTypeDef]
    ) -> PutOrganizationConfigRuleResponseTypeDef:
        """
        Adds or updates an Config rule for your entire organization to evaluate if your
        Amazon Web Services resources comply with your desired configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_organization_config_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_organization_config_rule)
        """

    def put_organization_conformance_pack(
        self, **kwargs: Unpack[PutOrganizationConformancePackRequestRequestTypeDef]
    ) -> PutOrganizationConformancePackResponseTypeDef:
        """
        Deploys conformance packs across member accounts in an Amazon Web Services
        Organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_organization_conformance_pack.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_organization_conformance_pack)
        """

    def put_remediation_configurations(
        self, **kwargs: Unpack[PutRemediationConfigurationsRequestRequestTypeDef]
    ) -> PutRemediationConfigurationsResponseTypeDef:
        """
        Adds or updates the remediation configuration with a specific Config rule with
        the selected target or action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_remediation_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_remediation_configurations)
        """

    def put_remediation_exceptions(
        self, **kwargs: Unpack[PutRemediationExceptionsRequestRequestTypeDef]
    ) -> PutRemediationExceptionsResponseTypeDef:
        """
        A remediation exception is when a specified resource is no longer considered
        for auto-remediation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_remediation_exceptions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_remediation_exceptions)
        """

    def put_resource_config(
        self, **kwargs: Unpack[PutResourceConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Records the configuration state for the resource provided in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_resource_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_resource_config)
        """

    def put_retention_configuration(
        self, **kwargs: Unpack[PutRetentionConfigurationRequestRequestTypeDef]
    ) -> PutRetentionConfigurationResponseTypeDef:
        """
        Creates and updates the retention configuration with details about retention
        period (number of days) that Config stores your historical information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_retention_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_retention_configuration)
        """

    def put_service_linked_configuration_recorder(
        self, **kwargs: Unpack[PutServiceLinkedConfigurationRecorderRequestRequestTypeDef]
    ) -> PutServiceLinkedConfigurationRecorderResponseTypeDef:
        """
        Creates a service-linked configuration recorder that is linked to a specific
        Amazon Web Services service based on the <code>ServicePrincipal</code> you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_service_linked_configuration_recorder.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_service_linked_configuration_recorder)
        """

    def put_stored_query(
        self, **kwargs: Unpack[PutStoredQueryRequestRequestTypeDef]
    ) -> PutStoredQueryResponseTypeDef:
        """
        Saves a new query or updates an existing saved query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_stored_query.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#put_stored_query)
        """

    def select_aggregate_resource_config(
        self, **kwargs: Unpack[SelectAggregateResourceConfigRequestRequestTypeDef]
    ) -> SelectAggregateResourceConfigResponseTypeDef:
        """
        Accepts a structured query language (SQL) SELECT command and an aggregator to
        query configuration state of Amazon Web Services resources across multiple
        accounts and regions, performs the corresponding search, and returns resource
        configurations matching the properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/select_aggregate_resource_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#select_aggregate_resource_config)
        """

    def select_resource_config(
        self, **kwargs: Unpack[SelectResourceConfigRequestRequestTypeDef]
    ) -> SelectResourceConfigResponseTypeDef:
        """
        Accepts a structured query language (SQL) <code>SELECT</code> command, performs
        the corresponding search, and returns resource configurations matching the
        properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/select_resource_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#select_resource_config)
        """

    def start_config_rules_evaluation(
        self, **kwargs: Unpack[StartConfigRulesEvaluationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Runs an on-demand evaluation for the specified Config rules against the last
        known configuration state of the resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/start_config_rules_evaluation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#start_config_rules_evaluation)
        """

    def start_configuration_recorder(
        self, **kwargs: Unpack[StartConfigurationRecorderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts the customer managed configuration recorder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/start_configuration_recorder.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#start_configuration_recorder)
        """

    def start_remediation_execution(
        self, **kwargs: Unpack[StartRemediationExecutionRequestRequestTypeDef]
    ) -> StartRemediationExecutionResponseTypeDef:
        """
        Runs an on-demand remediation for the specified Config rules against the last
        known remediation configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/start_remediation_execution.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#start_remediation_execution)
        """

    def start_resource_evaluation(
        self, **kwargs: Unpack[StartResourceEvaluationRequestRequestTypeDef]
    ) -> StartResourceEvaluationResponseTypeDef:
        """
        Runs an on-demand evaluation for the specified resource to determine whether
        the resource details will comply with configured Config rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/start_resource_evaluation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#start_resource_evaluation)
        """

    def stop_configuration_recorder(
        self, **kwargs: Unpack[StopConfigurationRecorderRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops the customer managed configuration recorder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/stop_configuration_recorder.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#stop_configuration_recorder)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates the specified tags to a resource with the specified
        <code>ResourceArn</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_aggregate_compliance_by_config_rules"]
    ) -> DescribeAggregateComplianceByConfigRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_aggregate_compliance_by_conformance_packs"]
    ) -> DescribeAggregateComplianceByConformancePacksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_aggregation_authorizations"]
    ) -> DescribeAggregationAuthorizationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_compliance_by_config_rule"]
    ) -> DescribeComplianceByConfigRulePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_compliance_by_resource"]
    ) -> DescribeComplianceByResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_config_rule_evaluation_status"]
    ) -> DescribeConfigRuleEvaluationStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_config_rules"]
    ) -> DescribeConfigRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_configuration_aggregator_sources_status"]
    ) -> DescribeConfigurationAggregatorSourcesStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_configuration_aggregators"]
    ) -> DescribeConfigurationAggregatorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_conformance_pack_status"]
    ) -> DescribeConformancePackStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_conformance_packs"]
    ) -> DescribeConformancePacksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_organization_config_rule_statuses"]
    ) -> DescribeOrganizationConfigRuleStatusesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_organization_config_rules"]
    ) -> DescribeOrganizationConfigRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_organization_conformance_pack_statuses"]
    ) -> DescribeOrganizationConformancePackStatusesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_organization_conformance_packs"]
    ) -> DescribeOrganizationConformancePacksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_pending_aggregation_requests"]
    ) -> DescribePendingAggregationRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_remediation_execution_status"]
    ) -> DescribeRemediationExecutionStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_retention_configurations"]
    ) -> DescribeRetentionConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_aggregate_compliance_details_by_config_rule"]
    ) -> GetAggregateComplianceDetailsByConfigRulePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_compliance_details_by_config_rule"]
    ) -> GetComplianceDetailsByConfigRulePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_compliance_details_by_resource"]
    ) -> GetComplianceDetailsByResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_conformance_pack_compliance_summary"]
    ) -> GetConformancePackComplianceSummaryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_organization_config_rule_detailed_status"]
    ) -> GetOrganizationConfigRuleDetailedStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_organization_conformance_pack_detailed_status"]
    ) -> GetOrganizationConformancePackDetailedStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_config_history"]
    ) -> GetResourceConfigHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_aggregate_discovered_resources"]
    ) -> ListAggregateDiscoveredResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configuration_recorders"]
    ) -> ListConfigurationRecordersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_discovered_resources"]
    ) -> ListDiscoveredResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_evaluations"]
    ) -> ListResourceEvaluationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["select_aggregate_resource_config"]
    ) -> SelectAggregateResourceConfigPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["select_resource_config"]
    ) -> SelectResourceConfigPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_config/client/#get_paginator)
        """
