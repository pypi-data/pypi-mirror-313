"""
Type annotations for detective service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_detective.client import DetectiveClient

    session = Session()
    client: DetectiveClient = session.client("detective")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    AcceptInvitationRequestRequestTypeDef,
    BatchGetGraphMemberDatasourcesRequestRequestTypeDef,
    BatchGetGraphMemberDatasourcesResponseTypeDef,
    BatchGetMembershipDatasourcesRequestRequestTypeDef,
    BatchGetMembershipDatasourcesResponseTypeDef,
    CreateGraphRequestRequestTypeDef,
    CreateGraphResponseTypeDef,
    CreateMembersRequestRequestTypeDef,
    CreateMembersResponseTypeDef,
    DeleteGraphRequestRequestTypeDef,
    DeleteMembersRequestRequestTypeDef,
    DeleteMembersResponseTypeDef,
    DescribeOrganizationConfigurationRequestRequestTypeDef,
    DescribeOrganizationConfigurationResponseTypeDef,
    DisassociateMembershipRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableOrganizationAdminAccountRequestRequestTypeDef,
    GetInvestigationRequestRequestTypeDef,
    GetInvestigationResponseTypeDef,
    GetMembersRequestRequestTypeDef,
    GetMembersResponseTypeDef,
    ListDatasourcePackagesRequestRequestTypeDef,
    ListDatasourcePackagesResponseTypeDef,
    ListGraphsRequestRequestTypeDef,
    ListGraphsResponseTypeDef,
    ListIndicatorsRequestRequestTypeDef,
    ListIndicatorsResponseTypeDef,
    ListInvestigationsRequestRequestTypeDef,
    ListInvestigationsResponseTypeDef,
    ListInvitationsRequestRequestTypeDef,
    ListInvitationsResponseTypeDef,
    ListMembersRequestRequestTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsRequestRequestTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RejectInvitationRequestRequestTypeDef,
    StartInvestigationRequestRequestTypeDef,
    StartInvestigationResponseTypeDef,
    StartMonitoringMemberRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDatasourcePackagesRequestRequestTypeDef,
    UpdateInvestigationStateRequestRequestTypeDef,
    UpdateOrganizationConfigurationRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DetectiveClient",)

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
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class DetectiveClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DetectiveClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#close)
        """

    def accept_invitation(
        self, **kwargs: Unpack[AcceptInvitationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Accepts an invitation for the member account to contribute data to a behavior
        graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/accept_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#accept_invitation)
        """

    def batch_get_graph_member_datasources(
        self, **kwargs: Unpack[BatchGetGraphMemberDatasourcesRequestRequestTypeDef]
    ) -> BatchGetGraphMemberDatasourcesResponseTypeDef:
        """
        Gets data source package information for the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/batch_get_graph_member_datasources.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#batch_get_graph_member_datasources)
        """

    def batch_get_membership_datasources(
        self, **kwargs: Unpack[BatchGetMembershipDatasourcesRequestRequestTypeDef]
    ) -> BatchGetMembershipDatasourcesResponseTypeDef:
        """
        Gets information on the data source package history for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/batch_get_membership_datasources.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#batch_get_membership_datasources)
        """

    def create_graph(
        self, **kwargs: Unpack[CreateGraphRequestRequestTypeDef]
    ) -> CreateGraphResponseTypeDef:
        """
        Creates a new behavior graph for the calling account, and sets that account as
        the administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/create_graph.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#create_graph)
        """

    def create_members(
        self, **kwargs: Unpack[CreateMembersRequestRequestTypeDef]
    ) -> CreateMembersResponseTypeDef:
        """
        <code>CreateMembers</code> is used to send invitations to accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/create_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#create_members)
        """

    def delete_graph(
        self, **kwargs: Unpack[DeleteGraphRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables the specified behavior graph and queues it to be deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/delete_graph.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#delete_graph)
        """

    def delete_members(
        self, **kwargs: Unpack[DeleteMembersRequestRequestTypeDef]
    ) -> DeleteMembersResponseTypeDef:
        """
        Removes the specified member accounts from the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/delete_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#delete_members)
        """

    def describe_organization_configuration(
        self, **kwargs: Unpack[DescribeOrganizationConfigurationRequestRequestTypeDef]
    ) -> DescribeOrganizationConfigurationResponseTypeDef:
        """
        Returns information about the configuration for the organization behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/describe_organization_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#describe_organization_configuration)
        """

    def disable_organization_admin_account(self) -> EmptyResponseMetadataTypeDef:
        """
        Removes the Detective administrator account in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/disable_organization_admin_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#disable_organization_admin_account)
        """

    def disassociate_membership(
        self, **kwargs: Unpack[DisassociateMembershipRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the member account from the specified behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/disassociate_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#disassociate_membership)
        """

    def enable_organization_admin_account(
        self, **kwargs: Unpack[EnableOrganizationAdminAccountRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Designates the Detective administrator account for the organization in the
        current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/enable_organization_admin_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#enable_organization_admin_account)
        """

    def get_investigation(
        self, **kwargs: Unpack[GetInvestigationRequestRequestTypeDef]
    ) -> GetInvestigationResponseTypeDef:
        """
        Detective investigations lets you investigate IAM users and IAM roles using
        indicators of compromise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/get_investigation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#get_investigation)
        """

    def get_members(
        self, **kwargs: Unpack[GetMembersRequestRequestTypeDef]
    ) -> GetMembersResponseTypeDef:
        """
        Returns the membership details for specified member accounts for a behavior
        graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/get_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#get_members)
        """

    def list_datasource_packages(
        self, **kwargs: Unpack[ListDatasourcePackagesRequestRequestTypeDef]
    ) -> ListDatasourcePackagesResponseTypeDef:
        """
        Lists data source packages in the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_datasource_packages.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_datasource_packages)
        """

    def list_graphs(
        self, **kwargs: Unpack[ListGraphsRequestRequestTypeDef]
    ) -> ListGraphsResponseTypeDef:
        """
        Returns the list of behavior graphs that the calling account is an
        administrator account of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_graphs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_graphs)
        """

    def list_indicators(
        self, **kwargs: Unpack[ListIndicatorsRequestRequestTypeDef]
    ) -> ListIndicatorsResponseTypeDef:
        """
        Gets the indicators from an investigation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_indicators.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_indicators)
        """

    def list_investigations(
        self, **kwargs: Unpack[ListInvestigationsRequestRequestTypeDef]
    ) -> ListInvestigationsResponseTypeDef:
        """
        Detective investigations lets you investigate IAM users and IAM roles using
        indicators of compromise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_investigations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_investigations)
        """

    def list_invitations(
        self, **kwargs: Unpack[ListInvitationsRequestRequestTypeDef]
    ) -> ListInvitationsResponseTypeDef:
        """
        Retrieves the list of open and accepted behavior graph invitations for the
        member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_invitations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_invitations)
        """

    def list_members(
        self, **kwargs: Unpack[ListMembersRequestRequestTypeDef]
    ) -> ListMembersResponseTypeDef:
        """
        Retrieves the list of member accounts for a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_members)
        """

    def list_organization_admin_accounts(
        self, **kwargs: Unpack[ListOrganizationAdminAccountsRequestRequestTypeDef]
    ) -> ListOrganizationAdminAccountsResponseTypeDef:
        """
        Returns information about the Detective administrator account for an
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_organization_admin_accounts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_organization_admin_accounts)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the tag values that are assigned to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_tags_for_resource)
        """

    def reject_invitation(
        self, **kwargs: Unpack[RejectInvitationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Rejects an invitation to contribute the account data to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/reject_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#reject_invitation)
        """

    def start_investigation(
        self, **kwargs: Unpack[StartInvestigationRequestRequestTypeDef]
    ) -> StartInvestigationResponseTypeDef:
        """
        Detective investigations lets you investigate IAM users and IAM roles using
        indicators of compromise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/start_investigation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#start_investigation)
        """

    def start_monitoring_member(
        self, **kwargs: Unpack[StartMonitoringMemberRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sends a request to enable data ingest for a member account that has a status of
        <code>ACCEPTED_BUT_DISABLED</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/start_monitoring_member.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#start_monitoring_member)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Applies tag values to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#untag_resource)
        """

    def update_datasource_packages(
        self, **kwargs: Unpack[UpdateDatasourcePackagesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a data source packages for the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/update_datasource_packages.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#update_datasource_packages)
        """

    def update_investigation_state(
        self, **kwargs: Unpack[UpdateInvestigationStateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the state of an investigation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/update_investigation_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#update_investigation_state)
        """

    def update_organization_configuration(
        self, **kwargs: Unpack[UpdateOrganizationConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the configuration for the Organizations integration in the current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/update_organization_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#update_organization_configuration)
        """
