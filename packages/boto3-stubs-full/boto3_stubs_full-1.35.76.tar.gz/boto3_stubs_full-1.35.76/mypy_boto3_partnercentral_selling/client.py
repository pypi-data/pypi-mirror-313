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
    ListEngagementByAcceptingInvitationTasksPaginator,
    ListEngagementFromOpportunityTasksPaginator,
    ListEngagementInvitationsPaginator,
    ListEngagementMembersPaginator,
    ListEngagementResourceAssociationsPaginator,
    ListEngagementsPaginator,
    ListOpportunitiesPaginator,
    ListResourceSnapshotJobsPaginator,
    ListResourceSnapshotsPaginator,
    ListSolutionsPaginator,
)
from .type_defs import (
    AcceptEngagementInvitationRequestRequestTypeDef,
    AssignOpportunityRequestRequestTypeDef,
    AssociateOpportunityRequestRequestTypeDef,
    CreateEngagementInvitationRequestRequestTypeDef,
    CreateEngagementInvitationResponseTypeDef,
    CreateEngagementRequestRequestTypeDef,
    CreateEngagementResponseTypeDef,
    CreateOpportunityRequestRequestTypeDef,
    CreateOpportunityResponseTypeDef,
    CreateResourceSnapshotJobRequestRequestTypeDef,
    CreateResourceSnapshotJobResponseTypeDef,
    CreateResourceSnapshotRequestRequestTypeDef,
    CreateResourceSnapshotResponseTypeDef,
    DeleteResourceSnapshotJobRequestRequestTypeDef,
    DisassociateOpportunityRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAwsOpportunitySummaryRequestRequestTypeDef,
    GetAwsOpportunitySummaryResponseTypeDef,
    GetEngagementInvitationRequestRequestTypeDef,
    GetEngagementInvitationResponseTypeDef,
    GetEngagementRequestRequestTypeDef,
    GetEngagementResponseTypeDef,
    GetOpportunityRequestRequestTypeDef,
    GetOpportunityResponseTypeDef,
    GetResourceSnapshotJobRequestRequestTypeDef,
    GetResourceSnapshotJobResponseTypeDef,
    GetResourceSnapshotRequestRequestTypeDef,
    GetResourceSnapshotResponseTypeDef,
    GetSellingSystemSettingsRequestRequestTypeDef,
    GetSellingSystemSettingsResponseTypeDef,
    ListEngagementByAcceptingInvitationTasksRequestRequestTypeDef,
    ListEngagementByAcceptingInvitationTasksResponseTypeDef,
    ListEngagementFromOpportunityTasksRequestRequestTypeDef,
    ListEngagementFromOpportunityTasksResponseTypeDef,
    ListEngagementInvitationsRequestRequestTypeDef,
    ListEngagementInvitationsResponseTypeDef,
    ListEngagementMembersRequestRequestTypeDef,
    ListEngagementMembersResponseTypeDef,
    ListEngagementResourceAssociationsRequestRequestTypeDef,
    ListEngagementResourceAssociationsResponseTypeDef,
    ListEngagementsRequestRequestTypeDef,
    ListEngagementsResponseTypeDef,
    ListOpportunitiesRequestRequestTypeDef,
    ListOpportunitiesResponseTypeDef,
    ListResourceSnapshotJobsRequestRequestTypeDef,
    ListResourceSnapshotJobsResponseTypeDef,
    ListResourceSnapshotsRequestRequestTypeDef,
    ListResourceSnapshotsResponseTypeDef,
    ListSolutionsRequestRequestTypeDef,
    ListSolutionsResponseTypeDef,
    PutSellingSystemSettingsRequestRequestTypeDef,
    PutSellingSystemSettingsResponseTypeDef,
    RejectEngagementInvitationRequestRequestTypeDef,
    StartEngagementByAcceptingInvitationTaskRequestRequestTypeDef,
    StartEngagementByAcceptingInvitationTaskResponseTypeDef,
    StartEngagementFromOpportunityTaskRequestRequestTypeDef,
    StartEngagementFromOpportunityTaskResponseTypeDef,
    StartResourceSnapshotJobRequestRequestTypeDef,
    StopResourceSnapshotJobRequestRequestTypeDef,
    SubmitOpportunityRequestRequestTypeDef,
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

    def accept_engagement_invitation(
        self, **kwargs: Unpack[AcceptEngagementInvitationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Use the <code>AcceptEngagementInvitation</code> action to accept an engagement
        invitation shared by AWS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/accept_engagement_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#accept_engagement_invitation)
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

    def create_engagement(
        self, **kwargs: Unpack[CreateEngagementRequestRequestTypeDef]
    ) -> CreateEngagementResponseTypeDef:
        """
        The <code>CreateEngagement</code> action allows you to create an
        <code>Engagement</code>, which serves as a collaborative space between
        different parties such as AWS Partners and AWS Sellers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_engagement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#create_engagement)
        """

    def create_engagement_invitation(
        self, **kwargs: Unpack[CreateEngagementInvitationRequestRequestTypeDef]
    ) -> CreateEngagementInvitationResponseTypeDef:
        """
        This action creates an invitation from a sender to a single receiver to join an
        engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_engagement_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#create_engagement_invitation)
        """

    def create_opportunity(
        self, **kwargs: Unpack[CreateOpportunityRequestRequestTypeDef]
    ) -> CreateOpportunityResponseTypeDef:
        """
        Creates an <code>Opportunity</code> record in Partner Central.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#create_opportunity)
        """

    def create_resource_snapshot(
        self, **kwargs: Unpack[CreateResourceSnapshotRequestRequestTypeDef]
    ) -> CreateResourceSnapshotResponseTypeDef:
        """
        This action allows you to create an immutable snapshot of a specific resource,
        such as an opportunity, within the context of an engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_resource_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#create_resource_snapshot)
        """

    def create_resource_snapshot_job(
        self, **kwargs: Unpack[CreateResourceSnapshotJobRequestRequestTypeDef]
    ) -> CreateResourceSnapshotJobResponseTypeDef:
        """
        Use this action to create a job to generate a snapshot of the specified
        resource within an engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_resource_snapshot_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#create_resource_snapshot_job)
        """

    def delete_resource_snapshot_job(
        self, **kwargs: Unpack[DeleteResourceSnapshotJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Use this action to deletes a previously created resource snapshot job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/delete_resource_snapshot_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#delete_resource_snapshot_job)
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

    def get_engagement(
        self, **kwargs: Unpack[GetEngagementRequestRequestTypeDef]
    ) -> GetEngagementResponseTypeDef:
        """
        Use this action to retrieve the engagement record for a given
        <code>EngagementIdentifier</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_engagement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_engagement)
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

    def get_resource_snapshot(
        self, **kwargs: Unpack[GetResourceSnapshotRequestRequestTypeDef]
    ) -> GetResourceSnapshotResponseTypeDef:
        """
        Use this action to retrieve a specific snapshot record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_resource_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_resource_snapshot)
        """

    def get_resource_snapshot_job(
        self, **kwargs: Unpack[GetResourceSnapshotJobRequestRequestTypeDef]
    ) -> GetResourceSnapshotJobResponseTypeDef:
        """
        Use this action to retrieves information about a specific resource snapshot job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_resource_snapshot_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_resource_snapshot_job)
        """

    def get_selling_system_settings(
        self, **kwargs: Unpack[GetSellingSystemSettingsRequestRequestTypeDef]
    ) -> GetSellingSystemSettingsResponseTypeDef:
        """
        Retrieves the currently set system settings, which include the IAM Role used
        for resource snapshot jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_selling_system_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_selling_system_settings)
        """

    def list_engagement_by_accepting_invitation_tasks(
        self, **kwargs: Unpack[ListEngagementByAcceptingInvitationTasksRequestRequestTypeDef]
    ) -> ListEngagementByAcceptingInvitationTasksResponseTypeDef:
        """
        Lists all in-progress, completed, or failed
        StartEngagementByAcceptingInvitationTask tasks that were initiated by the
        caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_by_accepting_invitation_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagement_by_accepting_invitation_tasks)
        """

    def list_engagement_from_opportunity_tasks(
        self, **kwargs: Unpack[ListEngagementFromOpportunityTasksRequestRequestTypeDef]
    ) -> ListEngagementFromOpportunityTasksResponseTypeDef:
        """
        Lists all in-progress, completed, or failed
        <code>EngagementFromOpportunity</code> tasks that were initiated by the
        caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_from_opportunity_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagement_from_opportunity_tasks)
        """

    def list_engagement_invitations(
        self, **kwargs: Unpack[ListEngagementInvitationsRequestRequestTypeDef]
    ) -> ListEngagementInvitationsResponseTypeDef:
        """
        Retrieves a list of engagement invitations sent to the partner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_invitations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagement_invitations)
        """

    def list_engagement_members(
        self, **kwargs: Unpack[ListEngagementMembersRequestRequestTypeDef]
    ) -> ListEngagementMembersResponseTypeDef:
        """
        Retrieves the details of member partners in an engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagement_members)
        """

    def list_engagement_resource_associations(
        self, **kwargs: Unpack[ListEngagementResourceAssociationsRequestRequestTypeDef]
    ) -> ListEngagementResourceAssociationsResponseTypeDef:
        """
        Lists the associations between resources and engagements where the caller is a
        member and has at least one snapshot in the engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_resource_associations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagement_resource_associations)
        """

    def list_engagements(
        self, **kwargs: Unpack[ListEngagementsRequestRequestTypeDef]
    ) -> ListEngagementsResponseTypeDef:
        """
        This action allows users to retrieve a list of engagement records from Partner
        Central.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagements.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagements)
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

    def list_resource_snapshot_jobs(
        self, **kwargs: Unpack[ListResourceSnapshotJobsRequestRequestTypeDef]
    ) -> ListResourceSnapshotJobsResponseTypeDef:
        """
        Lists resource snapshot jobs owned by the customer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_resource_snapshot_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_resource_snapshot_jobs)
        """

    def list_resource_snapshots(
        self, **kwargs: Unpack[ListResourceSnapshotsRequestRequestTypeDef]
    ) -> ListResourceSnapshotsResponseTypeDef:
        """
        Retrieves a list of resource view snapshots based on specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_resource_snapshots.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_resource_snapshots)
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

    def put_selling_system_settings(
        self, **kwargs: Unpack[PutSellingSystemSettingsRequestRequestTypeDef]
    ) -> PutSellingSystemSettingsResponseTypeDef:
        """
        Updates the currently set system settings, which include the IAM Role used for
        resource snapshot jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/put_selling_system_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#put_selling_system_settings)
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

    def start_resource_snapshot_job(
        self, **kwargs: Unpack[StartResourceSnapshotJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a resource snapshot job that has been previously created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/start_resource_snapshot_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#start_resource_snapshot_job)
        """

    def stop_resource_snapshot_job(
        self, **kwargs: Unpack[StopResourceSnapshotJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a resource snapshot job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/stop_resource_snapshot_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#stop_resource_snapshot_job)
        """

    def submit_opportunity(
        self, **kwargs: Unpack[SubmitOpportunityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Use this action to submit an opportunity that was previously created by partner
        for AWS review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/submit_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#submit_opportunity)
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
        self, operation_name: Literal["list_engagement_by_accepting_invitation_tasks"]
    ) -> ListEngagementByAcceptingInvitationTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_engagement_from_opportunity_tasks"]
    ) -> ListEngagementFromOpportunityTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
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
        self, operation_name: Literal["list_engagement_members"]
    ) -> ListEngagementMembersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_engagement_resource_associations"]
    ) -> ListEngagementResourceAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_engagements"]
    ) -> ListEngagementsPaginator:
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
    def get_paginator(
        self, operation_name: Literal["list_resource_snapshot_jobs"]
    ) -> ListResourceSnapshotJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_snapshots"]
    ) -> ListResourceSnapshotsPaginator:
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
