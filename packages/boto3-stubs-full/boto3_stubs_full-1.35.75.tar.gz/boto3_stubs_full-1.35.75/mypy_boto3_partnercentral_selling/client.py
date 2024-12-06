"""
Type annotations for partnercentral-selling service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_partnercentral_selling.client import PartnerCentralSellingAPIClient

    session = Session()
    client: PartnerCentralSellingAPIClient = session.client("partnercentral-selling")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListEngagementInvitationsPaginator,
    ListOpportunitiesPaginator,
    ListSolutionsPaginator,
)
from .type_defs import (
    AssignOpportunityRequestRequestTypeDef,
    AssociateOpportunityRequestRequestTypeDef,
    CreateOpportunityRequestRequestTypeDef,
    CreateOpportunityResponseTypeDef,
    DisassociateOpportunityRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAwsOpportunitySummaryRequestRequestTypeDef,
    GetAwsOpportunitySummaryResponseTypeDef,
    GetEngagementInvitationRequestRequestTypeDef,
    GetEngagementInvitationResponseTypeDef,
    GetOpportunityRequestRequestTypeDef,
    GetOpportunityResponseTypeDef,
    ListEngagementInvitationsRequestRequestTypeDef,
    ListEngagementInvitationsResponseTypeDef,
    ListOpportunitiesRequestRequestTypeDef,
    ListOpportunitiesResponseTypeDef,
    ListSolutionsRequestRequestTypeDef,
    ListSolutionsResponseTypeDef,
    RejectEngagementInvitationRequestRequestTypeDef,
    StartEngagementByAcceptingInvitationTaskRequestRequestTypeDef,
    StartEngagementByAcceptingInvitationTaskResponseTypeDef,
    StartEngagementFromOpportunityTaskRequestRequestTypeDef,
    StartEngagementFromOpportunityTaskResponseTypeDef,
    UpdateOpportunityRequestRequestTypeDef,
    UpdateOpportunityResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("PartnerCentralSellingAPIClient",)


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
    ValidationException: Type[BotocoreClientError]


class PartnerCentralSellingAPIClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling.html#PartnerCentralSellingAPI.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PartnerCentralSellingAPIClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling.html#PartnerCentralSellingAPI.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#close)
        """

    def assign_opportunity(
        self, **kwargs: Unpack[AssignOpportunityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables you to reassign an existing <code>Opportunity</code> to another user
        within your Partner Central account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/assign_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#assign_opportunity)
        """

    def associate_opportunity(
        self, **kwargs: Unpack[AssociateOpportunityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables you to create a formal association between an <code>Opportunity</code>
        and various related entities, enriching the context and details of the
        opportunity for better collaboration and decision making.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/associate_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#associate_opportunity)
        """

    def create_opportunity(
        self, **kwargs: Unpack[CreateOpportunityRequestRequestTypeDef]
    ) -> CreateOpportunityResponseTypeDef:
        """
        Creates an <code>Opportunity</code> record in Partner Central.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#create_opportunity)
        """

    def disassociate_opportunity(
        self, **kwargs: Unpack[DisassociateOpportunityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Allows you to remove an existing association between an
        <code>Opportunity</code> and related entities, such as a Partner Solution,
        Amazon Web Services product, or an Amazon Web Services Marketplace offer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/disassociate_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#disassociate_opportunity)
        """

    def get_aws_opportunity_summary(
        self, **kwargs: Unpack[GetAwsOpportunitySummaryRequestRequestTypeDef]
    ) -> GetAwsOpportunitySummaryResponseTypeDef:
        """
        Retrieves a summary of an AWS Opportunity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_aws_opportunity_summary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_aws_opportunity_summary)
        """

    def get_engagement_invitation(
        self, **kwargs: Unpack[GetEngagementInvitationRequestRequestTypeDef]
    ) -> GetEngagementInvitationResponseTypeDef:
        """
        Retrieves the details of an engagement invitation shared by AWS with a partner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_engagement_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_engagement_invitation)
        """

    def get_opportunity(
        self, **kwargs: Unpack[GetOpportunityRequestRequestTypeDef]
    ) -> GetOpportunityResponseTypeDef:
        """
        Fetches the <code>Opportunity</code> record from Partner Central by a given
        <code>Identifier</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_opportunity)
        """

    def list_engagement_invitations(
        self, **kwargs: Unpack[ListEngagementInvitationsRequestRequestTypeDef]
    ) -> ListEngagementInvitationsResponseTypeDef:
        """
        Retrieves a list of engagement invitations sent to the partner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_invitations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagement_invitations)
        """

    def list_opportunities(
        self, **kwargs: Unpack[ListOpportunitiesRequestRequestTypeDef]
    ) -> ListOpportunitiesResponseTypeDef:
        """
        This request accepts a list of filters that retrieve opportunity subsets as
        well as sort options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_opportunities.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_opportunities)
        """

    def list_solutions(
        self, **kwargs: Unpack[ListSolutionsRequestRequestTypeDef]
    ) -> ListSolutionsResponseTypeDef:
        """
        Retrieves a list of Partner Solutions that the partner registered on Partner
        Central.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_solutions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_solutions)
        """

    def reject_engagement_invitation(
        self, **kwargs: Unpack[RejectEngagementInvitationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This action rejects an <code>EngagementInvitation</code> that AWS shared.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/reject_engagement_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#reject_engagement_invitation)
        """

    def start_engagement_by_accepting_invitation_task(
        self, **kwargs: Unpack[StartEngagementByAcceptingInvitationTaskRequestRequestTypeDef]
    ) -> StartEngagementByAcceptingInvitationTaskResponseTypeDef:
        """
        This action starts the engagement by accepting an
        <code>EngagementInvitation</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/start_engagement_by_accepting_invitation_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#start_engagement_by_accepting_invitation_task)
        """

    def start_engagement_from_opportunity_task(
        self, **kwargs: Unpack[StartEngagementFromOpportunityTaskRequestRequestTypeDef]
    ) -> StartEngagementFromOpportunityTaskResponseTypeDef:
        """
        This action initiates the engagement process from an existing opportunity by
        accepting the engagement invitation and creating a corresponding opportunity in
        the partner's system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/start_engagement_from_opportunity_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#start_engagement_from_opportunity_task)
        """

    def update_opportunity(
        self, **kwargs: Unpack[UpdateOpportunityRequestRequestTypeDef]
    ) -> UpdateOpportunityResponseTypeDef:
        """
        Updates the <code>Opportunity</code> record identified by a given
        <code>Identifier</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/update_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#update_opportunity)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_engagement_invitations"]
    ) -> ListEngagementInvitationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_opportunities"]
    ) -> ListOpportunitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_solutions"]) -> ListSolutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """
