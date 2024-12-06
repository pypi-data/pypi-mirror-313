"""
Type annotations for datazone service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_datazone.client import DataZoneClient

    session = Session()
    client: DataZoneClient = session.client("datazone")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAssetFiltersPaginator,
    ListAssetRevisionsPaginator,
    ListConnectionsPaginator,
    ListDataProductRevisionsPaginator,
    ListDataSourceRunActivitiesPaginator,
    ListDataSourceRunsPaginator,
    ListDataSourcesPaginator,
    ListDomainsPaginator,
    ListDomainUnitsForParentPaginator,
    ListEntityOwnersPaginator,
    ListEnvironmentActionsPaginator,
    ListEnvironmentBlueprintConfigurationsPaginator,
    ListEnvironmentBlueprintsPaginator,
    ListEnvironmentProfilesPaginator,
    ListEnvironmentsPaginator,
    ListJobRunsPaginator,
    ListLineageEventsPaginator,
    ListLineageNodeHistoryPaginator,
    ListMetadataGenerationRunsPaginator,
    ListNotificationsPaginator,
    ListPolicyGrantsPaginator,
    ListProjectMembershipsPaginator,
    ListProjectProfilesPaginator,
    ListProjectsPaginator,
    ListRulesPaginator,
    ListSubscriptionGrantsPaginator,
    ListSubscriptionRequestsPaginator,
    ListSubscriptionsPaginator,
    ListSubscriptionTargetsPaginator,
    ListTimeSeriesDataPointsPaginator,
    SearchGroupProfilesPaginator,
    SearchListingsPaginator,
    SearchPaginator,
    SearchTypesPaginator,
    SearchUserProfilesPaginator,
)
from .type_defs import (
    AcceptPredictionsInputRequestTypeDef,
    AcceptPredictionsOutputTypeDef,
    AcceptSubscriptionRequestInputRequestTypeDef,
    AcceptSubscriptionRequestOutputTypeDef,
    AddEntityOwnerInputRequestTypeDef,
    AddPolicyGrantInputRequestTypeDef,
    AssociateEnvironmentRoleInputRequestTypeDef,
    CancelMetadataGenerationRunInputRequestTypeDef,
    CancelSubscriptionInputRequestTypeDef,
    CancelSubscriptionOutputTypeDef,
    CreateAssetFilterInputRequestTypeDef,
    CreateAssetFilterOutputTypeDef,
    CreateAssetInputRequestTypeDef,
    CreateAssetOutputTypeDef,
    CreateAssetRevisionInputRequestTypeDef,
    CreateAssetRevisionOutputTypeDef,
    CreateAssetTypeInputRequestTypeDef,
    CreateAssetTypeOutputTypeDef,
    CreateConnectionInputRequestTypeDef,
    CreateConnectionOutputTypeDef,
    CreateDataProductInputRequestTypeDef,
    CreateDataProductOutputTypeDef,
    CreateDataProductRevisionInputRequestTypeDef,
    CreateDataProductRevisionOutputTypeDef,
    CreateDataSourceInputRequestTypeDef,
    CreateDataSourceOutputTypeDef,
    CreateDomainInputRequestTypeDef,
    CreateDomainOutputTypeDef,
    CreateDomainUnitInputRequestTypeDef,
    CreateDomainUnitOutputTypeDef,
    CreateEnvironmentActionInputRequestTypeDef,
    CreateEnvironmentActionOutputTypeDef,
    CreateEnvironmentInputRequestTypeDef,
    CreateEnvironmentOutputTypeDef,
    CreateEnvironmentProfileInputRequestTypeDef,
    CreateEnvironmentProfileOutputTypeDef,
    CreateFormTypeInputRequestTypeDef,
    CreateFormTypeOutputTypeDef,
    CreateGlossaryInputRequestTypeDef,
    CreateGlossaryOutputTypeDef,
    CreateGlossaryTermInputRequestTypeDef,
    CreateGlossaryTermOutputTypeDef,
    CreateGroupProfileInputRequestTypeDef,
    CreateGroupProfileOutputTypeDef,
    CreateListingChangeSetInputRequestTypeDef,
    CreateListingChangeSetOutputTypeDef,
    CreateProjectInputRequestTypeDef,
    CreateProjectMembershipInputRequestTypeDef,
    CreateProjectOutputTypeDef,
    CreateProjectProfileInputRequestTypeDef,
    CreateProjectProfileOutputTypeDef,
    CreateRuleInputRequestTypeDef,
    CreateRuleOutputTypeDef,
    CreateSubscriptionGrantInputRequestTypeDef,
    CreateSubscriptionGrantOutputTypeDef,
    CreateSubscriptionRequestInputRequestTypeDef,
    CreateSubscriptionRequestOutputTypeDef,
    CreateSubscriptionTargetInputRequestTypeDef,
    CreateSubscriptionTargetOutputTypeDef,
    CreateUserProfileInputRequestTypeDef,
    CreateUserProfileOutputTypeDef,
    DeleteAssetFilterInputRequestTypeDef,
    DeleteAssetInputRequestTypeDef,
    DeleteAssetTypeInputRequestTypeDef,
    DeleteConnectionInputRequestTypeDef,
    DeleteConnectionOutputTypeDef,
    DeleteDataProductInputRequestTypeDef,
    DeleteDataSourceInputRequestTypeDef,
    DeleteDataSourceOutputTypeDef,
    DeleteDomainInputRequestTypeDef,
    DeleteDomainOutputTypeDef,
    DeleteDomainUnitInputRequestTypeDef,
    DeleteEnvironmentActionInputRequestTypeDef,
    DeleteEnvironmentBlueprintConfigurationInputRequestTypeDef,
    DeleteEnvironmentInputRequestTypeDef,
    DeleteEnvironmentProfileInputRequestTypeDef,
    DeleteFormTypeInputRequestTypeDef,
    DeleteGlossaryInputRequestTypeDef,
    DeleteGlossaryTermInputRequestTypeDef,
    DeleteListingInputRequestTypeDef,
    DeleteProjectInputRequestTypeDef,
    DeleteProjectMembershipInputRequestTypeDef,
    DeleteProjectProfileInputRequestTypeDef,
    DeleteRuleInputRequestTypeDef,
    DeleteSubscriptionGrantInputRequestTypeDef,
    DeleteSubscriptionGrantOutputTypeDef,
    DeleteSubscriptionRequestInputRequestTypeDef,
    DeleteSubscriptionTargetInputRequestTypeDef,
    DeleteTimeSeriesDataPointsInputRequestTypeDef,
    DisassociateEnvironmentRoleInputRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAssetFilterInputRequestTypeDef,
    GetAssetFilterOutputTypeDef,
    GetAssetInputRequestTypeDef,
    GetAssetOutputTypeDef,
    GetAssetTypeInputRequestTypeDef,
    GetAssetTypeOutputTypeDef,
    GetConnectionInputRequestTypeDef,
    GetConnectionOutputTypeDef,
    GetDataProductInputRequestTypeDef,
    GetDataProductOutputTypeDef,
    GetDataSourceInputRequestTypeDef,
    GetDataSourceOutputTypeDef,
    GetDataSourceRunInputRequestTypeDef,
    GetDataSourceRunOutputTypeDef,
    GetDomainInputRequestTypeDef,
    GetDomainOutputTypeDef,
    GetDomainUnitInputRequestTypeDef,
    GetDomainUnitOutputTypeDef,
    GetEnvironmentActionInputRequestTypeDef,
    GetEnvironmentActionOutputTypeDef,
    GetEnvironmentBlueprintConfigurationInputRequestTypeDef,
    GetEnvironmentBlueprintConfigurationOutputTypeDef,
    GetEnvironmentBlueprintInputRequestTypeDef,
    GetEnvironmentBlueprintOutputTypeDef,
    GetEnvironmentCredentialsInputRequestTypeDef,
    GetEnvironmentCredentialsOutputTypeDef,
    GetEnvironmentInputRequestTypeDef,
    GetEnvironmentOutputTypeDef,
    GetEnvironmentProfileInputRequestTypeDef,
    GetEnvironmentProfileOutputTypeDef,
    GetFormTypeInputRequestTypeDef,
    GetFormTypeOutputTypeDef,
    GetGlossaryInputRequestTypeDef,
    GetGlossaryOutputTypeDef,
    GetGlossaryTermInputRequestTypeDef,
    GetGlossaryTermOutputTypeDef,
    GetGroupProfileInputRequestTypeDef,
    GetGroupProfileOutputTypeDef,
    GetIamPortalLoginUrlInputRequestTypeDef,
    GetIamPortalLoginUrlOutputTypeDef,
    GetJobRunInputRequestTypeDef,
    GetJobRunOutputTypeDef,
    GetLineageEventInputRequestTypeDef,
    GetLineageEventOutputTypeDef,
    GetLineageNodeInputRequestTypeDef,
    GetLineageNodeOutputTypeDef,
    GetListingInputRequestTypeDef,
    GetListingOutputTypeDef,
    GetMetadataGenerationRunInputRequestTypeDef,
    GetMetadataGenerationRunOutputTypeDef,
    GetProjectInputRequestTypeDef,
    GetProjectOutputTypeDef,
    GetProjectProfileInputRequestTypeDef,
    GetProjectProfileOutputTypeDef,
    GetRuleInputRequestTypeDef,
    GetRuleOutputTypeDef,
    GetSubscriptionGrantInputRequestTypeDef,
    GetSubscriptionGrantOutputTypeDef,
    GetSubscriptionInputRequestTypeDef,
    GetSubscriptionOutputTypeDef,
    GetSubscriptionRequestDetailsInputRequestTypeDef,
    GetSubscriptionRequestDetailsOutputTypeDef,
    GetSubscriptionTargetInputRequestTypeDef,
    GetSubscriptionTargetOutputTypeDef,
    GetTimeSeriesDataPointInputRequestTypeDef,
    GetTimeSeriesDataPointOutputTypeDef,
    GetUserProfileInputRequestTypeDef,
    GetUserProfileOutputTypeDef,
    ListAssetFiltersInputRequestTypeDef,
    ListAssetFiltersOutputTypeDef,
    ListAssetRevisionsInputRequestTypeDef,
    ListAssetRevisionsOutputTypeDef,
    ListConnectionsInputRequestTypeDef,
    ListConnectionsOutputTypeDef,
    ListDataProductRevisionsInputRequestTypeDef,
    ListDataProductRevisionsOutputTypeDef,
    ListDataSourceRunActivitiesInputRequestTypeDef,
    ListDataSourceRunActivitiesOutputTypeDef,
    ListDataSourceRunsInputRequestTypeDef,
    ListDataSourceRunsOutputTypeDef,
    ListDataSourcesInputRequestTypeDef,
    ListDataSourcesOutputTypeDef,
    ListDomainsInputRequestTypeDef,
    ListDomainsOutputTypeDef,
    ListDomainUnitsForParentInputRequestTypeDef,
    ListDomainUnitsForParentOutputTypeDef,
    ListEntityOwnersInputRequestTypeDef,
    ListEntityOwnersOutputTypeDef,
    ListEnvironmentActionsInputRequestTypeDef,
    ListEnvironmentActionsOutputTypeDef,
    ListEnvironmentBlueprintConfigurationsInputRequestTypeDef,
    ListEnvironmentBlueprintConfigurationsOutputTypeDef,
    ListEnvironmentBlueprintsInputRequestTypeDef,
    ListEnvironmentBlueprintsOutputTypeDef,
    ListEnvironmentProfilesInputRequestTypeDef,
    ListEnvironmentProfilesOutputTypeDef,
    ListEnvironmentsInputRequestTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListJobRunsInputRequestTypeDef,
    ListJobRunsOutputTypeDef,
    ListLineageEventsInputRequestTypeDef,
    ListLineageEventsOutputTypeDef,
    ListLineageNodeHistoryInputRequestTypeDef,
    ListLineageNodeHistoryOutputTypeDef,
    ListMetadataGenerationRunsInputRequestTypeDef,
    ListMetadataGenerationRunsOutputTypeDef,
    ListNotificationsInputRequestTypeDef,
    ListNotificationsOutputTypeDef,
    ListPolicyGrantsInputRequestTypeDef,
    ListPolicyGrantsOutputTypeDef,
    ListProjectMembershipsInputRequestTypeDef,
    ListProjectMembershipsOutputTypeDef,
    ListProjectProfilesInputRequestTypeDef,
    ListProjectProfilesOutputTypeDef,
    ListProjectsInputRequestTypeDef,
    ListProjectsOutputTypeDef,
    ListRulesInputRequestTypeDef,
    ListRulesOutputTypeDef,
    ListSubscriptionGrantsInputRequestTypeDef,
    ListSubscriptionGrantsOutputTypeDef,
    ListSubscriptionRequestsInputRequestTypeDef,
    ListSubscriptionRequestsOutputTypeDef,
    ListSubscriptionsInputRequestTypeDef,
    ListSubscriptionsOutputTypeDef,
    ListSubscriptionTargetsInputRequestTypeDef,
    ListSubscriptionTargetsOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTimeSeriesDataPointsInputRequestTypeDef,
    ListTimeSeriesDataPointsOutputTypeDef,
    PostLineageEventInputRequestTypeDef,
    PostLineageEventOutputTypeDef,
    PostTimeSeriesDataPointsInputRequestTypeDef,
    PostTimeSeriesDataPointsOutputTypeDef,
    PutEnvironmentBlueprintConfigurationInputRequestTypeDef,
    PutEnvironmentBlueprintConfigurationOutputTypeDef,
    RejectPredictionsInputRequestTypeDef,
    RejectPredictionsOutputTypeDef,
    RejectSubscriptionRequestInputRequestTypeDef,
    RejectSubscriptionRequestOutputTypeDef,
    RemoveEntityOwnerInputRequestTypeDef,
    RemovePolicyGrantInputRequestTypeDef,
    RevokeSubscriptionInputRequestTypeDef,
    RevokeSubscriptionOutputTypeDef,
    SearchGroupProfilesInputRequestTypeDef,
    SearchGroupProfilesOutputTypeDef,
    SearchInputRequestTypeDef,
    SearchListingsInputRequestTypeDef,
    SearchListingsOutputTypeDef,
    SearchOutputTypeDef,
    SearchTypesInputRequestTypeDef,
    SearchTypesOutputTypeDef,
    SearchUserProfilesInputRequestTypeDef,
    SearchUserProfilesOutputTypeDef,
    StartDataSourceRunInputRequestTypeDef,
    StartDataSourceRunOutputTypeDef,
    StartMetadataGenerationRunInputRequestTypeDef,
    StartMetadataGenerationRunOutputTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAssetFilterInputRequestTypeDef,
    UpdateAssetFilterOutputTypeDef,
    UpdateConnectionInputRequestTypeDef,
    UpdateConnectionOutputTypeDef,
    UpdateDataSourceInputRequestTypeDef,
    UpdateDataSourceOutputTypeDef,
    UpdateDomainInputRequestTypeDef,
    UpdateDomainOutputTypeDef,
    UpdateDomainUnitInputRequestTypeDef,
    UpdateDomainUnitOutputTypeDef,
    UpdateEnvironmentActionInputRequestTypeDef,
    UpdateEnvironmentActionOutputTypeDef,
    UpdateEnvironmentInputRequestTypeDef,
    UpdateEnvironmentOutputTypeDef,
    UpdateEnvironmentProfileInputRequestTypeDef,
    UpdateEnvironmentProfileOutputTypeDef,
    UpdateGlossaryInputRequestTypeDef,
    UpdateGlossaryOutputTypeDef,
    UpdateGlossaryTermInputRequestTypeDef,
    UpdateGlossaryTermOutputTypeDef,
    UpdateGroupProfileInputRequestTypeDef,
    UpdateGroupProfileOutputTypeDef,
    UpdateProjectInputRequestTypeDef,
    UpdateProjectOutputTypeDef,
    UpdateProjectProfileInputRequestTypeDef,
    UpdateProjectProfileOutputTypeDef,
    UpdateRuleInputRequestTypeDef,
    UpdateRuleOutputTypeDef,
    UpdateSubscriptionGrantStatusInputRequestTypeDef,
    UpdateSubscriptionGrantStatusOutputTypeDef,
    UpdateSubscriptionRequestInputRequestTypeDef,
    UpdateSubscriptionRequestOutputTypeDef,
    UpdateSubscriptionTargetInputRequestTypeDef,
    UpdateSubscriptionTargetOutputTypeDef,
    UpdateUserProfileInputRequestTypeDef,
    UpdateUserProfileOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("DataZoneClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class DataZoneClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DataZoneClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#close)
        """

    def accept_predictions(
        self, **kwargs: Unpack[AcceptPredictionsInputRequestTypeDef]
    ) -> AcceptPredictionsOutputTypeDef:
        """
        Accepts automatically generated business-friendly metadata for your Amazon
        DataZone assets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/accept_predictions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#accept_predictions)
        """

    def accept_subscription_request(
        self, **kwargs: Unpack[AcceptSubscriptionRequestInputRequestTypeDef]
    ) -> AcceptSubscriptionRequestOutputTypeDef:
        """
        Accepts a subscription request to a specific asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/accept_subscription_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#accept_subscription_request)
        """

    def add_entity_owner(
        self, **kwargs: Unpack[AddEntityOwnerInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds the owner of an entity (a domain unit).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/add_entity_owner.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#add_entity_owner)
        """

    def add_policy_grant(
        self, **kwargs: Unpack[AddPolicyGrantInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds a policy grant (an authorization policy) to a specified entity, including
        domain units, environment blueprint configurations, or environment profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/add_policy_grant.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#add_policy_grant)
        """

    def associate_environment_role(
        self, **kwargs: Unpack[AssociateEnvironmentRoleInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates the environment role in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/associate_environment_role.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#associate_environment_role)
        """

    def cancel_metadata_generation_run(
        self, **kwargs: Unpack[CancelMetadataGenerationRunInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels the metadata generation run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/cancel_metadata_generation_run.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#cancel_metadata_generation_run)
        """

    def cancel_subscription(
        self, **kwargs: Unpack[CancelSubscriptionInputRequestTypeDef]
    ) -> CancelSubscriptionOutputTypeDef:
        """
        Cancels the subscription to the specified asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/cancel_subscription.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#cancel_subscription)
        """

    def create_asset(
        self, **kwargs: Unpack[CreateAssetInputRequestTypeDef]
    ) -> CreateAssetOutputTypeDef:
        """
        Creates an asset in Amazon DataZone catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_asset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_asset)
        """

    def create_asset_filter(
        self, **kwargs: Unpack[CreateAssetFilterInputRequestTypeDef]
    ) -> CreateAssetFilterOutputTypeDef:
        """
        Creates a data asset filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_asset_filter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_asset_filter)
        """

    def create_asset_revision(
        self, **kwargs: Unpack[CreateAssetRevisionInputRequestTypeDef]
    ) -> CreateAssetRevisionOutputTypeDef:
        """
        Creates a revision of the asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_asset_revision.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_asset_revision)
        """

    def create_asset_type(
        self, **kwargs: Unpack[CreateAssetTypeInputRequestTypeDef]
    ) -> CreateAssetTypeOutputTypeDef:
        """
        Creates a custom asset type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_asset_type.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_asset_type)
        """

    def create_connection(
        self, **kwargs: Unpack[CreateConnectionInputRequestTypeDef]
    ) -> CreateConnectionOutputTypeDef:
        """
        Creates a new connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_connection)
        """

    def create_data_product(
        self, **kwargs: Unpack[CreateDataProductInputRequestTypeDef]
    ) -> CreateDataProductOutputTypeDef:
        """
        Creates a data product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_data_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_data_product)
        """

    def create_data_product_revision(
        self, **kwargs: Unpack[CreateDataProductRevisionInputRequestTypeDef]
    ) -> CreateDataProductRevisionOutputTypeDef:
        """
        Creates a data product revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_data_product_revision.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_data_product_revision)
        """

    def create_data_source(
        self, **kwargs: Unpack[CreateDataSourceInputRequestTypeDef]
    ) -> CreateDataSourceOutputTypeDef:
        """
        Creates an Amazon DataZone data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_data_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_data_source)
        """

    def create_domain(
        self, **kwargs: Unpack[CreateDomainInputRequestTypeDef]
    ) -> CreateDomainOutputTypeDef:
        """
        Creates an Amazon DataZone domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_domain)
        """

    def create_domain_unit(
        self, **kwargs: Unpack[CreateDomainUnitInputRequestTypeDef]
    ) -> CreateDomainUnitOutputTypeDef:
        """
        Creates a domain unit in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_domain_unit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_domain_unit)
        """

    def create_environment(
        self, **kwargs: Unpack[CreateEnvironmentInputRequestTypeDef]
    ) -> CreateEnvironmentOutputTypeDef:
        """
        Create an Amazon DataZone environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_environment)
        """

    def create_environment_action(
        self, **kwargs: Unpack[CreateEnvironmentActionInputRequestTypeDef]
    ) -> CreateEnvironmentActionOutputTypeDef:
        """
        Creates an action for the environment, for example, creates a console link for
        an analytics tool that is available in this environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_environment_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_environment_action)
        """

    def create_environment_profile(
        self, **kwargs: Unpack[CreateEnvironmentProfileInputRequestTypeDef]
    ) -> CreateEnvironmentProfileOutputTypeDef:
        """
        Creates an Amazon DataZone environment profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_environment_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_environment_profile)
        """

    def create_form_type(
        self, **kwargs: Unpack[CreateFormTypeInputRequestTypeDef]
    ) -> CreateFormTypeOutputTypeDef:
        """
        Creates a metadata form type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_form_type.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_form_type)
        """

    def create_glossary(
        self, **kwargs: Unpack[CreateGlossaryInputRequestTypeDef]
    ) -> CreateGlossaryOutputTypeDef:
        """
        Creates an Amazon DataZone business glossary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_glossary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_glossary)
        """

    def create_glossary_term(
        self, **kwargs: Unpack[CreateGlossaryTermInputRequestTypeDef]
    ) -> CreateGlossaryTermOutputTypeDef:
        """
        Creates a business glossary term.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_glossary_term.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_glossary_term)
        """

    def create_group_profile(
        self, **kwargs: Unpack[CreateGroupProfileInputRequestTypeDef]
    ) -> CreateGroupProfileOutputTypeDef:
        """
        Creates a group profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_group_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_group_profile)
        """

    def create_listing_change_set(
        self, **kwargs: Unpack[CreateListingChangeSetInputRequestTypeDef]
    ) -> CreateListingChangeSetOutputTypeDef:
        """
        Publishes a listing (a record of an asset at a given time) or removes a listing
        from the catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_listing_change_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_listing_change_set)
        """

    def create_project(
        self, **kwargs: Unpack[CreateProjectInputRequestTypeDef]
    ) -> CreateProjectOutputTypeDef:
        """
        Creates an Amazon DataZone project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_project)
        """

    def create_project_membership(
        self, **kwargs: Unpack[CreateProjectMembershipInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a project membership in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_project_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_project_membership)
        """

    def create_project_profile(
        self, **kwargs: Unpack[CreateProjectProfileInputRequestTypeDef]
    ) -> CreateProjectProfileOutputTypeDef:
        """
        Creates a project profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_project_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_project_profile)
        """

    def create_rule(
        self, **kwargs: Unpack[CreateRuleInputRequestTypeDef]
    ) -> CreateRuleOutputTypeDef:
        """
        Creates a rule in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_rule)
        """

    def create_subscription_grant(
        self, **kwargs: Unpack[CreateSubscriptionGrantInputRequestTypeDef]
    ) -> CreateSubscriptionGrantOutputTypeDef:
        """
        Creates a subsscription grant in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_subscription_grant.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_subscription_grant)
        """

    def create_subscription_request(
        self, **kwargs: Unpack[CreateSubscriptionRequestInputRequestTypeDef]
    ) -> CreateSubscriptionRequestOutputTypeDef:
        """
        Creates a subscription request in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_subscription_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_subscription_request)
        """

    def create_subscription_target(
        self, **kwargs: Unpack[CreateSubscriptionTargetInputRequestTypeDef]
    ) -> CreateSubscriptionTargetOutputTypeDef:
        """
        Creates a subscription target in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_subscription_target.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_subscription_target)
        """

    def create_user_profile(
        self, **kwargs: Unpack[CreateUserProfileInputRequestTypeDef]
    ) -> CreateUserProfileOutputTypeDef:
        """
        Creates a user profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/create_user_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#create_user_profile)
        """

    def delete_asset(self, **kwargs: Unpack[DeleteAssetInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes an asset in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_asset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_asset)
        """

    def delete_asset_filter(
        self, **kwargs: Unpack[DeleteAssetFilterInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an asset filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_asset_filter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_asset_filter)
        """

    def delete_asset_type(
        self, **kwargs: Unpack[DeleteAssetTypeInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an asset type in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_asset_type.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_asset_type)
        """

    def delete_connection(
        self, **kwargs: Unpack[DeleteConnectionInputRequestTypeDef]
    ) -> DeleteConnectionOutputTypeDef:
        """
        Deletes and connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_connection)
        """

    def delete_data_product(
        self, **kwargs: Unpack[DeleteDataProductInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a data product in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_data_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_data_product)
        """

    def delete_data_source(
        self, **kwargs: Unpack[DeleteDataSourceInputRequestTypeDef]
    ) -> DeleteDataSourceOutputTypeDef:
        """
        Deletes a data source in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_data_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_data_source)
        """

    def delete_domain(
        self, **kwargs: Unpack[DeleteDomainInputRequestTypeDef]
    ) -> DeleteDomainOutputTypeDef:
        """
        Deletes a Amazon DataZone domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_domain)
        """

    def delete_domain_unit(
        self, **kwargs: Unpack[DeleteDomainUnitInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a domain unit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_domain_unit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_domain_unit)
        """

    def delete_environment(
        self, **kwargs: Unpack[DeleteEnvironmentInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an environment in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_environment)
        """

    def delete_environment_action(
        self, **kwargs: Unpack[DeleteEnvironmentActionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an action for the environment, for example, deletes a console link for
        an analytics tool that is available in this environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_environment_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_environment_action)
        """

    def delete_environment_blueprint_configuration(
        self, **kwargs: Unpack[DeleteEnvironmentBlueprintConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the blueprint configuration in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_environment_blueprint_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_environment_blueprint_configuration)
        """

    def delete_environment_profile(
        self, **kwargs: Unpack[DeleteEnvironmentProfileInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an environment profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_environment_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_environment_profile)
        """

    def delete_form_type(
        self, **kwargs: Unpack[DeleteFormTypeInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delets and metadata form type in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_form_type.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_form_type)
        """

    def delete_glossary(
        self, **kwargs: Unpack[DeleteGlossaryInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a business glossary in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_glossary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_glossary)
        """

    def delete_glossary_term(
        self, **kwargs: Unpack[DeleteGlossaryTermInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a business glossary term in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_glossary_term.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_glossary_term)
        """

    def delete_listing(self, **kwargs: Unpack[DeleteListingInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a listing (a record of an asset at a given time).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_listing.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_listing)
        """

    def delete_project(self, **kwargs: Unpack[DeleteProjectInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a project in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_project)
        """

    def delete_project_membership(
        self, **kwargs: Unpack[DeleteProjectMembershipInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes project membership in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_project_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_project_membership)
        """

    def delete_project_profile(
        self, **kwargs: Unpack[DeleteProjectProfileInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a project profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_project_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_project_profile)
        """

    def delete_rule(self, **kwargs: Unpack[DeleteRuleInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a rule in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_rule)
        """

    def delete_subscription_grant(
        self, **kwargs: Unpack[DeleteSubscriptionGrantInputRequestTypeDef]
    ) -> DeleteSubscriptionGrantOutputTypeDef:
        """
        Deletes and subscription grant in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_subscription_grant.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_subscription_grant)
        """

    def delete_subscription_request(
        self, **kwargs: Unpack[DeleteSubscriptionRequestInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a subscription request in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_subscription_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_subscription_request)
        """

    def delete_subscription_target(
        self, **kwargs: Unpack[DeleteSubscriptionTargetInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a subscription target in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_subscription_target.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_subscription_target)
        """

    def delete_time_series_data_points(
        self, **kwargs: Unpack[DeleteTimeSeriesDataPointsInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified time series form for the specified asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/delete_time_series_data_points.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#delete_time_series_data_points)
        """

    def disassociate_environment_role(
        self, **kwargs: Unpack[DisassociateEnvironmentRoleInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the environment role in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/disassociate_environment_role.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#disassociate_environment_role)
        """

    def get_asset(self, **kwargs: Unpack[GetAssetInputRequestTypeDef]) -> GetAssetOutputTypeDef:
        """
        Gets an Amazon DataZone asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_asset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_asset)
        """

    def get_asset_filter(
        self, **kwargs: Unpack[GetAssetFilterInputRequestTypeDef]
    ) -> GetAssetFilterOutputTypeDef:
        """
        Gets an asset filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_asset_filter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_asset_filter)
        """

    def get_asset_type(
        self, **kwargs: Unpack[GetAssetTypeInputRequestTypeDef]
    ) -> GetAssetTypeOutputTypeDef:
        """
        Gets an Amazon DataZone asset type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_asset_type.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_asset_type)
        """

    def get_connection(
        self, **kwargs: Unpack[GetConnectionInputRequestTypeDef]
    ) -> GetConnectionOutputTypeDef:
        """
        Gets a connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_connection)
        """

    def get_data_product(
        self, **kwargs: Unpack[GetDataProductInputRequestTypeDef]
    ) -> GetDataProductOutputTypeDef:
        """
        Gets the data product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_data_product.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_data_product)
        """

    def get_data_source(
        self, **kwargs: Unpack[GetDataSourceInputRequestTypeDef]
    ) -> GetDataSourceOutputTypeDef:
        """
        Gets an Amazon DataZone data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_data_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_data_source)
        """

    def get_data_source_run(
        self, **kwargs: Unpack[GetDataSourceRunInputRequestTypeDef]
    ) -> GetDataSourceRunOutputTypeDef:
        """
        Gets an Amazon DataZone data source run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_data_source_run.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_data_source_run)
        """

    def get_domain(self, **kwargs: Unpack[GetDomainInputRequestTypeDef]) -> GetDomainOutputTypeDef:
        """
        Gets an Amazon DataZone domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_domain)
        """

    def get_domain_unit(
        self, **kwargs: Unpack[GetDomainUnitInputRequestTypeDef]
    ) -> GetDomainUnitOutputTypeDef:
        """
        Gets the details of the specified domain unit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_domain_unit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_domain_unit)
        """

    def get_environment(
        self, **kwargs: Unpack[GetEnvironmentInputRequestTypeDef]
    ) -> GetEnvironmentOutputTypeDef:
        """
        Gets an Amazon DataZone environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_environment)
        """

    def get_environment_action(
        self, **kwargs: Unpack[GetEnvironmentActionInputRequestTypeDef]
    ) -> GetEnvironmentActionOutputTypeDef:
        """
        Gets the specified environment action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_environment_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_environment_action)
        """

    def get_environment_blueprint(
        self, **kwargs: Unpack[GetEnvironmentBlueprintInputRequestTypeDef]
    ) -> GetEnvironmentBlueprintOutputTypeDef:
        """
        Gets an Amazon DataZone blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_environment_blueprint.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_environment_blueprint)
        """

    def get_environment_blueprint_configuration(
        self, **kwargs: Unpack[GetEnvironmentBlueprintConfigurationInputRequestTypeDef]
    ) -> GetEnvironmentBlueprintConfigurationOutputTypeDef:
        """
        Gets the blueprint configuration in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_environment_blueprint_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_environment_blueprint_configuration)
        """

    def get_environment_credentials(
        self, **kwargs: Unpack[GetEnvironmentCredentialsInputRequestTypeDef]
    ) -> GetEnvironmentCredentialsOutputTypeDef:
        """
        Gets the credentials of an environment in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_environment_credentials.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_environment_credentials)
        """

    def get_environment_profile(
        self, **kwargs: Unpack[GetEnvironmentProfileInputRequestTypeDef]
    ) -> GetEnvironmentProfileOutputTypeDef:
        """
        Gets an evinronment profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_environment_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_environment_profile)
        """

    def get_form_type(
        self, **kwargs: Unpack[GetFormTypeInputRequestTypeDef]
    ) -> GetFormTypeOutputTypeDef:
        """
        Gets a metadata form type in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_form_type.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_form_type)
        """

    def get_glossary(
        self, **kwargs: Unpack[GetGlossaryInputRequestTypeDef]
    ) -> GetGlossaryOutputTypeDef:
        """
        Gets a business glossary in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_glossary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_glossary)
        """

    def get_glossary_term(
        self, **kwargs: Unpack[GetGlossaryTermInputRequestTypeDef]
    ) -> GetGlossaryTermOutputTypeDef:
        """
        Gets a business glossary term in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_glossary_term.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_glossary_term)
        """

    def get_group_profile(
        self, **kwargs: Unpack[GetGroupProfileInputRequestTypeDef]
    ) -> GetGroupProfileOutputTypeDef:
        """
        Gets a group profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_group_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_group_profile)
        """

    def get_iam_portal_login_url(
        self, **kwargs: Unpack[GetIamPortalLoginUrlInputRequestTypeDef]
    ) -> GetIamPortalLoginUrlOutputTypeDef:
        """
        Gets the data portal URL for the specified Amazon DataZone domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_iam_portal_login_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_iam_portal_login_url)
        """

    def get_job_run(self, **kwargs: Unpack[GetJobRunInputRequestTypeDef]) -> GetJobRunOutputTypeDef:
        """
        The details of the job run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_job_run.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_job_run)
        """

    def get_lineage_event(
        self, **kwargs: Unpack[GetLineageEventInputRequestTypeDef]
    ) -> GetLineageEventOutputTypeDef:
        """
        Describes the lineage event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_lineage_event.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_lineage_event)
        """

    def get_lineage_node(
        self, **kwargs: Unpack[GetLineageNodeInputRequestTypeDef]
    ) -> GetLineageNodeOutputTypeDef:
        """
        Gets the data lineage node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_lineage_node.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_lineage_node)
        """

    def get_listing(
        self, **kwargs: Unpack[GetListingInputRequestTypeDef]
    ) -> GetListingOutputTypeDef:
        """
        Gets a listing (a record of an asset at a given time).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_listing.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_listing)
        """

    def get_metadata_generation_run(
        self, **kwargs: Unpack[GetMetadataGenerationRunInputRequestTypeDef]
    ) -> GetMetadataGenerationRunOutputTypeDef:
        """
        Gets a metadata generation run in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_metadata_generation_run.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_metadata_generation_run)
        """

    def get_project(
        self, **kwargs: Unpack[GetProjectInputRequestTypeDef]
    ) -> GetProjectOutputTypeDef:
        """
        Gets a project in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_project)
        """

    def get_project_profile(
        self, **kwargs: Unpack[GetProjectProfileInputRequestTypeDef]
    ) -> GetProjectProfileOutputTypeDef:
        """
        The details of the project profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_project_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_project_profile)
        """

    def get_rule(self, **kwargs: Unpack[GetRuleInputRequestTypeDef]) -> GetRuleOutputTypeDef:
        """
        Gets the details of a rule in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_rule)
        """

    def get_subscription(
        self, **kwargs: Unpack[GetSubscriptionInputRequestTypeDef]
    ) -> GetSubscriptionOutputTypeDef:
        """
        Gets a subscription in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_subscription.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_subscription)
        """

    def get_subscription_grant(
        self, **kwargs: Unpack[GetSubscriptionGrantInputRequestTypeDef]
    ) -> GetSubscriptionGrantOutputTypeDef:
        """
        Gets the subscription grant in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_subscription_grant.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_subscription_grant)
        """

    def get_subscription_request_details(
        self, **kwargs: Unpack[GetSubscriptionRequestDetailsInputRequestTypeDef]
    ) -> GetSubscriptionRequestDetailsOutputTypeDef:
        """
        Gets the details of the specified subscription request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_subscription_request_details.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_subscription_request_details)
        """

    def get_subscription_target(
        self, **kwargs: Unpack[GetSubscriptionTargetInputRequestTypeDef]
    ) -> GetSubscriptionTargetOutputTypeDef:
        """
        Gets the subscription target in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_subscription_target.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_subscription_target)
        """

    def get_time_series_data_point(
        self, **kwargs: Unpack[GetTimeSeriesDataPointInputRequestTypeDef]
    ) -> GetTimeSeriesDataPointOutputTypeDef:
        """
        Gets the existing data point for the asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_time_series_data_point.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_time_series_data_point)
        """

    def get_user_profile(
        self, **kwargs: Unpack[GetUserProfileInputRequestTypeDef]
    ) -> GetUserProfileOutputTypeDef:
        """
        Gets a user profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_user_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_user_profile)
        """

    def list_asset_filters(
        self, **kwargs: Unpack[ListAssetFiltersInputRequestTypeDef]
    ) -> ListAssetFiltersOutputTypeDef:
        """
        Lists asset filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_asset_filters.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_asset_filters)
        """

    def list_asset_revisions(
        self, **kwargs: Unpack[ListAssetRevisionsInputRequestTypeDef]
    ) -> ListAssetRevisionsOutputTypeDef:
        """
        Lists the revisions for the asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_asset_revisions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_asset_revisions)
        """

    def list_connections(
        self, **kwargs: Unpack[ListConnectionsInputRequestTypeDef]
    ) -> ListConnectionsOutputTypeDef:
        """
        Lists connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_connections.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_connections)
        """

    def list_data_product_revisions(
        self, **kwargs: Unpack[ListDataProductRevisionsInputRequestTypeDef]
    ) -> ListDataProductRevisionsOutputTypeDef:
        """
        Lists data product revisions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_data_product_revisions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_data_product_revisions)
        """

    def list_data_source_run_activities(
        self, **kwargs: Unpack[ListDataSourceRunActivitiesInputRequestTypeDef]
    ) -> ListDataSourceRunActivitiesOutputTypeDef:
        """
        Lists data source run activities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_data_source_run_activities.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_data_source_run_activities)
        """

    def list_data_source_runs(
        self, **kwargs: Unpack[ListDataSourceRunsInputRequestTypeDef]
    ) -> ListDataSourceRunsOutputTypeDef:
        """
        Lists data source runs in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_data_source_runs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_data_source_runs)
        """

    def list_data_sources(
        self, **kwargs: Unpack[ListDataSourcesInputRequestTypeDef]
    ) -> ListDataSourcesOutputTypeDef:
        """
        Lists data sources in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_data_sources.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_data_sources)
        """

    def list_domain_units_for_parent(
        self, **kwargs: Unpack[ListDomainUnitsForParentInputRequestTypeDef]
    ) -> ListDomainUnitsForParentOutputTypeDef:
        """
        Lists child domain units for the specified parent domain unit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_domain_units_for_parent.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_domain_units_for_parent)
        """

    def list_domains(
        self, **kwargs: Unpack[ListDomainsInputRequestTypeDef]
    ) -> ListDomainsOutputTypeDef:
        """
        Lists Amazon DataZone domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_domains.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_domains)
        """

    def list_entity_owners(
        self, **kwargs: Unpack[ListEntityOwnersInputRequestTypeDef]
    ) -> ListEntityOwnersOutputTypeDef:
        """
        Lists the entity (domain units) owners.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_entity_owners.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_entity_owners)
        """

    def list_environment_actions(
        self, **kwargs: Unpack[ListEnvironmentActionsInputRequestTypeDef]
    ) -> ListEnvironmentActionsOutputTypeDef:
        """
        Lists existing environment actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_environment_actions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_environment_actions)
        """

    def list_environment_blueprint_configurations(
        self, **kwargs: Unpack[ListEnvironmentBlueprintConfigurationsInputRequestTypeDef]
    ) -> ListEnvironmentBlueprintConfigurationsOutputTypeDef:
        """
        Lists blueprint configurations for a Amazon DataZone environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_environment_blueprint_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_environment_blueprint_configurations)
        """

    def list_environment_blueprints(
        self, **kwargs: Unpack[ListEnvironmentBlueprintsInputRequestTypeDef]
    ) -> ListEnvironmentBlueprintsOutputTypeDef:
        """
        Lists blueprints in an Amazon DataZone environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_environment_blueprints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_environment_blueprints)
        """

    def list_environment_profiles(
        self, **kwargs: Unpack[ListEnvironmentProfilesInputRequestTypeDef]
    ) -> ListEnvironmentProfilesOutputTypeDef:
        """
        Lists Amazon DataZone environment profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_environment_profiles.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_environment_profiles)
        """

    def list_environments(
        self, **kwargs: Unpack[ListEnvironmentsInputRequestTypeDef]
    ) -> ListEnvironmentsOutputTypeDef:
        """
        Lists Amazon DataZone environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_environments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_environments)
        """

    def list_job_runs(
        self, **kwargs: Unpack[ListJobRunsInputRequestTypeDef]
    ) -> ListJobRunsOutputTypeDef:
        """
        Lists job runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_job_runs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_job_runs)
        """

    def list_lineage_events(
        self, **kwargs: Unpack[ListLineageEventsInputRequestTypeDef]
    ) -> ListLineageEventsOutputTypeDef:
        """
        Lists lineage events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_lineage_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_lineage_events)
        """

    def list_lineage_node_history(
        self, **kwargs: Unpack[ListLineageNodeHistoryInputRequestTypeDef]
    ) -> ListLineageNodeHistoryOutputTypeDef:
        """
        Lists the history of the specified data lineage node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_lineage_node_history.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_lineage_node_history)
        """

    def list_metadata_generation_runs(
        self, **kwargs: Unpack[ListMetadataGenerationRunsInputRequestTypeDef]
    ) -> ListMetadataGenerationRunsOutputTypeDef:
        """
        Lists all metadata generation runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_metadata_generation_runs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_metadata_generation_runs)
        """

    def list_notifications(
        self, **kwargs: Unpack[ListNotificationsInputRequestTypeDef]
    ) -> ListNotificationsOutputTypeDef:
        """
        Lists all Amazon DataZone notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_notifications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_notifications)
        """

    def list_policy_grants(
        self, **kwargs: Unpack[ListPolicyGrantsInputRequestTypeDef]
    ) -> ListPolicyGrantsOutputTypeDef:
        """
        Lists policy grants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_policy_grants.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_policy_grants)
        """

    def list_project_memberships(
        self, **kwargs: Unpack[ListProjectMembershipsInputRequestTypeDef]
    ) -> ListProjectMembershipsOutputTypeDef:
        """
        Lists all members of the specified project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_project_memberships.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_project_memberships)
        """

    def list_project_profiles(
        self, **kwargs: Unpack[ListProjectProfilesInputRequestTypeDef]
    ) -> ListProjectProfilesOutputTypeDef:
        """
        Lists project profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_project_profiles.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_project_profiles)
        """

    def list_projects(
        self, **kwargs: Unpack[ListProjectsInputRequestTypeDef]
    ) -> ListProjectsOutputTypeDef:
        """
        Lists Amazon DataZone projects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_projects.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_projects)
        """

    def list_rules(self, **kwargs: Unpack[ListRulesInputRequestTypeDef]) -> ListRulesOutputTypeDef:
        """
        Lists existing rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_rules)
        """

    def list_subscription_grants(
        self, **kwargs: Unpack[ListSubscriptionGrantsInputRequestTypeDef]
    ) -> ListSubscriptionGrantsOutputTypeDef:
        """
        Lists subscription grants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_subscription_grants.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_subscription_grants)
        """

    def list_subscription_requests(
        self, **kwargs: Unpack[ListSubscriptionRequestsInputRequestTypeDef]
    ) -> ListSubscriptionRequestsOutputTypeDef:
        """
        Lists Amazon DataZone subscription requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_subscription_requests.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_subscription_requests)
        """

    def list_subscription_targets(
        self, **kwargs: Unpack[ListSubscriptionTargetsInputRequestTypeDef]
    ) -> ListSubscriptionTargetsOutputTypeDef:
        """
        Lists subscription targets in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_subscription_targets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_subscription_targets)
        """

    def list_subscriptions(
        self, **kwargs: Unpack[ListSubscriptionsInputRequestTypeDef]
    ) -> ListSubscriptionsOutputTypeDef:
        """
        Lists subscriptions in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_subscriptions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_subscriptions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for the specified resource in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_tags_for_resource)
        """

    def list_time_series_data_points(
        self, **kwargs: Unpack[ListTimeSeriesDataPointsInputRequestTypeDef]
    ) -> ListTimeSeriesDataPointsOutputTypeDef:
        """
        Lists time series data points.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/list_time_series_data_points.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#list_time_series_data_points)
        """

    def post_lineage_event(
        self, **kwargs: Unpack[PostLineageEventInputRequestTypeDef]
    ) -> PostLineageEventOutputTypeDef:
        """
        Posts a data lineage event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/post_lineage_event.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#post_lineage_event)
        """

    def post_time_series_data_points(
        self, **kwargs: Unpack[PostTimeSeriesDataPointsInputRequestTypeDef]
    ) -> PostTimeSeriesDataPointsOutputTypeDef:
        """
        Posts time series data points to Amazon DataZone for the specified asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/post_time_series_data_points.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#post_time_series_data_points)
        """

    def put_environment_blueprint_configuration(
        self, **kwargs: Unpack[PutEnvironmentBlueprintConfigurationInputRequestTypeDef]
    ) -> PutEnvironmentBlueprintConfigurationOutputTypeDef:
        """
        Writes the configuration for the specified environment blueprint in Amazon
        DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/put_environment_blueprint_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#put_environment_blueprint_configuration)
        """

    def reject_predictions(
        self, **kwargs: Unpack[RejectPredictionsInputRequestTypeDef]
    ) -> RejectPredictionsOutputTypeDef:
        """
        Rejects automatically generated business-friendly metadata for your Amazon
        DataZone assets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/reject_predictions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#reject_predictions)
        """

    def reject_subscription_request(
        self, **kwargs: Unpack[RejectSubscriptionRequestInputRequestTypeDef]
    ) -> RejectSubscriptionRequestOutputTypeDef:
        """
        Rejects the specified subscription request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/reject_subscription_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#reject_subscription_request)
        """

    def remove_entity_owner(
        self, **kwargs: Unpack[RemoveEntityOwnerInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes an owner from an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/remove_entity_owner.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#remove_entity_owner)
        """

    def remove_policy_grant(
        self, **kwargs: Unpack[RemovePolicyGrantInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a policy grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/remove_policy_grant.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#remove_policy_grant)
        """

    def revoke_subscription(
        self, **kwargs: Unpack[RevokeSubscriptionInputRequestTypeDef]
    ) -> RevokeSubscriptionOutputTypeDef:
        """
        Revokes a specified subscription in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/revoke_subscription.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#revoke_subscription)
        """

    def search(self, **kwargs: Unpack[SearchInputRequestTypeDef]) -> SearchOutputTypeDef:
        """
        Searches for assets in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/search.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#search)
        """

    def search_group_profiles(
        self, **kwargs: Unpack[SearchGroupProfilesInputRequestTypeDef]
    ) -> SearchGroupProfilesOutputTypeDef:
        """
        Searches group profiles in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/search_group_profiles.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#search_group_profiles)
        """

    def search_listings(
        self, **kwargs: Unpack[SearchListingsInputRequestTypeDef]
    ) -> SearchListingsOutputTypeDef:
        """
        Searches listings (records of an asset at a given time) in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/search_listings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#search_listings)
        """

    def search_types(
        self, **kwargs: Unpack[SearchTypesInputRequestTypeDef]
    ) -> SearchTypesOutputTypeDef:
        """
        Searches for types in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/search_types.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#search_types)
        """

    def search_user_profiles(
        self, **kwargs: Unpack[SearchUserProfilesInputRequestTypeDef]
    ) -> SearchUserProfilesOutputTypeDef:
        """
        Searches user profiles in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/search_user_profiles.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#search_user_profiles)
        """

    def start_data_source_run(
        self, **kwargs: Unpack[StartDataSourceRunInputRequestTypeDef]
    ) -> StartDataSourceRunOutputTypeDef:
        """
        Start the run of the specified data source in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/start_data_source_run.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#start_data_source_run)
        """

    def start_metadata_generation_run(
        self, **kwargs: Unpack[StartMetadataGenerationRunInputRequestTypeDef]
    ) -> StartMetadataGenerationRunOutputTypeDef:
        """
        Starts the metadata generation run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/start_metadata_generation_run.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#start_metadata_generation_run)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags a resource in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Untags a resource in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#untag_resource)
        """

    def update_asset_filter(
        self, **kwargs: Unpack[UpdateAssetFilterInputRequestTypeDef]
    ) -> UpdateAssetFilterOutputTypeDef:
        """
        Updates an asset filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_asset_filter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_asset_filter)
        """

    def update_connection(
        self, **kwargs: Unpack[UpdateConnectionInputRequestTypeDef]
    ) -> UpdateConnectionOutputTypeDef:
        """
        Updates a connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_connection)
        """

    def update_data_source(
        self, **kwargs: Unpack[UpdateDataSourceInputRequestTypeDef]
    ) -> UpdateDataSourceOutputTypeDef:
        """
        Updates the specified data source in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_data_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_data_source)
        """

    def update_domain(
        self, **kwargs: Unpack[UpdateDomainInputRequestTypeDef]
    ) -> UpdateDomainOutputTypeDef:
        """
        Updates a Amazon DataZone domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_domain)
        """

    def update_domain_unit(
        self, **kwargs: Unpack[UpdateDomainUnitInputRequestTypeDef]
    ) -> UpdateDomainUnitOutputTypeDef:
        """
        Updates the domain unit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_domain_unit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_domain_unit)
        """

    def update_environment(
        self, **kwargs: Unpack[UpdateEnvironmentInputRequestTypeDef]
    ) -> UpdateEnvironmentOutputTypeDef:
        """
        Updates the specified environment in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_environment)
        """

    def update_environment_action(
        self, **kwargs: Unpack[UpdateEnvironmentActionInputRequestTypeDef]
    ) -> UpdateEnvironmentActionOutputTypeDef:
        """
        Updates an environment action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_environment_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_environment_action)
        """

    def update_environment_profile(
        self, **kwargs: Unpack[UpdateEnvironmentProfileInputRequestTypeDef]
    ) -> UpdateEnvironmentProfileOutputTypeDef:
        """
        Updates the specified environment profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_environment_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_environment_profile)
        """

    def update_glossary(
        self, **kwargs: Unpack[UpdateGlossaryInputRequestTypeDef]
    ) -> UpdateGlossaryOutputTypeDef:
        """
        Updates the business glossary in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_glossary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_glossary)
        """

    def update_glossary_term(
        self, **kwargs: Unpack[UpdateGlossaryTermInputRequestTypeDef]
    ) -> UpdateGlossaryTermOutputTypeDef:
        """
        Updates a business glossary term in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_glossary_term.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_glossary_term)
        """

    def update_group_profile(
        self, **kwargs: Unpack[UpdateGroupProfileInputRequestTypeDef]
    ) -> UpdateGroupProfileOutputTypeDef:
        """
        Updates the specified group profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_group_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_group_profile)
        """

    def update_project(
        self, **kwargs: Unpack[UpdateProjectInputRequestTypeDef]
    ) -> UpdateProjectOutputTypeDef:
        """
        Updates the specified project in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_project)
        """

    def update_project_profile(
        self, **kwargs: Unpack[UpdateProjectProfileInputRequestTypeDef]
    ) -> UpdateProjectProfileOutputTypeDef:
        """
        Updates a project profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_project_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_project_profile)
        """

    def update_rule(
        self, **kwargs: Unpack[UpdateRuleInputRequestTypeDef]
    ) -> UpdateRuleOutputTypeDef:
        """
        Updates a rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_rule)
        """

    def update_subscription_grant_status(
        self, **kwargs: Unpack[UpdateSubscriptionGrantStatusInputRequestTypeDef]
    ) -> UpdateSubscriptionGrantStatusOutputTypeDef:
        """
        Updates the status of the specified subscription grant status in Amazon
        DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_subscription_grant_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_subscription_grant_status)
        """

    def update_subscription_request(
        self, **kwargs: Unpack[UpdateSubscriptionRequestInputRequestTypeDef]
    ) -> UpdateSubscriptionRequestOutputTypeDef:
        """
        Updates a specified subscription request in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_subscription_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_subscription_request)
        """

    def update_subscription_target(
        self, **kwargs: Unpack[UpdateSubscriptionTargetInputRequestTypeDef]
    ) -> UpdateSubscriptionTargetOutputTypeDef:
        """
        Updates the specified subscription target in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_subscription_target.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_subscription_target)
        """

    def update_user_profile(
        self, **kwargs: Unpack[UpdateUserProfileInputRequestTypeDef]
    ) -> UpdateUserProfileOutputTypeDef:
        """
        Updates the specified user profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/update_user_profile.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#update_user_profile)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_asset_filters"]
    ) -> ListAssetFiltersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_asset_revisions"]
    ) -> ListAssetRevisionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_connections"]
    ) -> ListConnectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_product_revisions"]
    ) -> ListDataProductRevisionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_source_run_activities"]
    ) -> ListDataSourceRunActivitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_source_runs"]
    ) -> ListDataSourceRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_sources"]
    ) -> ListDataSourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_domain_units_for_parent"]
    ) -> ListDomainUnitsForParentPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_entity_owners"]
    ) -> ListEntityOwnersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_actions"]
    ) -> ListEnvironmentActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_blueprint_configurations"]
    ) -> ListEnvironmentBlueprintConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_blueprints"]
    ) -> ListEnvironmentBlueprintsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_profiles"]
    ) -> ListEnvironmentProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_job_runs"]) -> ListJobRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_lineage_events"]
    ) -> ListLineageEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_lineage_node_history"]
    ) -> ListLineageNodeHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_metadata_generation_runs"]
    ) -> ListMetadataGenerationRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_notifications"]
    ) -> ListNotificationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_policy_grants"]
    ) -> ListPolicyGrantsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_project_memberships"]
    ) -> ListProjectMembershipsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_project_profiles"]
    ) -> ListProjectProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rules"]) -> ListRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscription_grants"]
    ) -> ListSubscriptionGrantsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscription_requests"]
    ) -> ListSubscriptionRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscription_targets"]
    ) -> ListSubscriptionTargetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscriptions"]
    ) -> ListSubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_time_series_data_points"]
    ) -> ListTimeSeriesDataPointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_group_profiles"]
    ) -> SearchGroupProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_listings"]) -> SearchListingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search"]) -> SearchPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_types"]) -> SearchTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_user_profiles"]
    ) -> SearchUserProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datazone/client/#get_paginator)
        """
