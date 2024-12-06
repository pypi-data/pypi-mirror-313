"""
Type annotations for guardduty service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_guardduty.client import GuardDutyClient

    session = Session()
    client: GuardDutyClient = session.client("guardduty")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeMalwareScansPaginator,
    ListCoveragePaginator,
    ListDetectorsPaginator,
    ListFiltersPaginator,
    ListFindingsPaginator,
    ListInvitationsPaginator,
    ListIPSetsPaginator,
    ListMembersPaginator,
    ListOrganizationAdminAccountsPaginator,
    ListThreatIntelSetsPaginator,
)
from .type_defs import (
    AcceptAdministratorInvitationRequestRequestTypeDef,
    AcceptInvitationRequestRequestTypeDef,
    ArchiveFindingsRequestRequestTypeDef,
    CreateDetectorRequestRequestTypeDef,
    CreateDetectorResponseTypeDef,
    CreateFilterRequestRequestTypeDef,
    CreateFilterResponseTypeDef,
    CreateIPSetRequestRequestTypeDef,
    CreateIPSetResponseTypeDef,
    CreateMalwareProtectionPlanRequestRequestTypeDef,
    CreateMalwareProtectionPlanResponseTypeDef,
    CreateMembersRequestRequestTypeDef,
    CreateMembersResponseTypeDef,
    CreatePublishingDestinationRequestRequestTypeDef,
    CreatePublishingDestinationResponseTypeDef,
    CreateSampleFindingsRequestRequestTypeDef,
    CreateThreatIntelSetRequestRequestTypeDef,
    CreateThreatIntelSetResponseTypeDef,
    DeclineInvitationsRequestRequestTypeDef,
    DeclineInvitationsResponseTypeDef,
    DeleteDetectorRequestRequestTypeDef,
    DeleteFilterRequestRequestTypeDef,
    DeleteInvitationsRequestRequestTypeDef,
    DeleteInvitationsResponseTypeDef,
    DeleteIPSetRequestRequestTypeDef,
    DeleteMalwareProtectionPlanRequestRequestTypeDef,
    DeleteMembersRequestRequestTypeDef,
    DeleteMembersResponseTypeDef,
    DeletePublishingDestinationRequestRequestTypeDef,
    DeleteThreatIntelSetRequestRequestTypeDef,
    DescribeMalwareScansRequestRequestTypeDef,
    DescribeMalwareScansResponseTypeDef,
    DescribeOrganizationConfigurationRequestRequestTypeDef,
    DescribeOrganizationConfigurationResponseTypeDef,
    DescribePublishingDestinationRequestRequestTypeDef,
    DescribePublishingDestinationResponseTypeDef,
    DisableOrganizationAdminAccountRequestRequestTypeDef,
    DisassociateFromAdministratorAccountRequestRequestTypeDef,
    DisassociateFromMasterAccountRequestRequestTypeDef,
    DisassociateMembersRequestRequestTypeDef,
    DisassociateMembersResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableOrganizationAdminAccountRequestRequestTypeDef,
    GetAdministratorAccountRequestRequestTypeDef,
    GetAdministratorAccountResponseTypeDef,
    GetCoverageStatisticsRequestRequestTypeDef,
    GetCoverageStatisticsResponseTypeDef,
    GetDetectorRequestRequestTypeDef,
    GetDetectorResponseTypeDef,
    GetFilterRequestRequestTypeDef,
    GetFilterResponseTypeDef,
    GetFindingsRequestRequestTypeDef,
    GetFindingsResponseTypeDef,
    GetFindingsStatisticsRequestRequestTypeDef,
    GetFindingsStatisticsResponseTypeDef,
    GetInvitationsCountResponseTypeDef,
    GetIPSetRequestRequestTypeDef,
    GetIPSetResponseTypeDef,
    GetMalwareProtectionPlanRequestRequestTypeDef,
    GetMalwareProtectionPlanResponseTypeDef,
    GetMalwareScanSettingsRequestRequestTypeDef,
    GetMalwareScanSettingsResponseTypeDef,
    GetMasterAccountRequestRequestTypeDef,
    GetMasterAccountResponseTypeDef,
    GetMemberDetectorsRequestRequestTypeDef,
    GetMemberDetectorsResponseTypeDef,
    GetMembersRequestRequestTypeDef,
    GetMembersResponseTypeDef,
    GetOrganizationStatisticsResponseTypeDef,
    GetRemainingFreeTrialDaysRequestRequestTypeDef,
    GetRemainingFreeTrialDaysResponseTypeDef,
    GetThreatIntelSetRequestRequestTypeDef,
    GetThreatIntelSetResponseTypeDef,
    GetUsageStatisticsRequestRequestTypeDef,
    GetUsageStatisticsResponseTypeDef,
    InviteMembersRequestRequestTypeDef,
    InviteMembersResponseTypeDef,
    ListCoverageRequestRequestTypeDef,
    ListCoverageResponseTypeDef,
    ListDetectorsRequestRequestTypeDef,
    ListDetectorsResponseTypeDef,
    ListFiltersRequestRequestTypeDef,
    ListFiltersResponseTypeDef,
    ListFindingsRequestRequestTypeDef,
    ListFindingsResponseTypeDef,
    ListInvitationsRequestRequestTypeDef,
    ListInvitationsResponseTypeDef,
    ListIPSetsRequestRequestTypeDef,
    ListIPSetsResponseTypeDef,
    ListMalwareProtectionPlansRequestRequestTypeDef,
    ListMalwareProtectionPlansResponseTypeDef,
    ListMembersRequestRequestTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsRequestRequestTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListPublishingDestinationsRequestRequestTypeDef,
    ListPublishingDestinationsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListThreatIntelSetsRequestRequestTypeDef,
    ListThreatIntelSetsResponseTypeDef,
    StartMalwareScanRequestRequestTypeDef,
    StartMalwareScanResponseTypeDef,
    StartMonitoringMembersRequestRequestTypeDef,
    StartMonitoringMembersResponseTypeDef,
    StopMonitoringMembersRequestRequestTypeDef,
    StopMonitoringMembersResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UnarchiveFindingsRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDetectorRequestRequestTypeDef,
    UpdateFilterRequestRequestTypeDef,
    UpdateFilterResponseTypeDef,
    UpdateFindingsFeedbackRequestRequestTypeDef,
    UpdateIPSetRequestRequestTypeDef,
    UpdateMalwareProtectionPlanRequestRequestTypeDef,
    UpdateMalwareScanSettingsRequestRequestTypeDef,
    UpdateMemberDetectorsRequestRequestTypeDef,
    UpdateMemberDetectorsResponseTypeDef,
    UpdateOrganizationConfigurationRequestRequestTypeDef,
    UpdatePublishingDestinationRequestRequestTypeDef,
    UpdateThreatIntelSetRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("GuardDutyClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class GuardDutyClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GuardDutyClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#close)
        """

    def accept_administrator_invitation(
        self, **kwargs: Unpack[AcceptAdministratorInvitationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Accepts the invitation to be a member account and get monitored by a GuardDuty
        administrator account that sent the invitation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/accept_administrator_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#accept_administrator_invitation)
        """

    def accept_invitation(
        self, **kwargs: Unpack[AcceptInvitationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Accepts the invitation to be monitored by a GuardDuty administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/accept_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#accept_invitation)
        """

    def archive_findings(
        self, **kwargs: Unpack[ArchiveFindingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Archives GuardDuty findings that are specified by the list of finding IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/archive_findings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#archive_findings)
        """

    def create_detector(
        self, **kwargs: Unpack[CreateDetectorRequestRequestTypeDef]
    ) -> CreateDetectorResponseTypeDef:
        """
        Creates a single GuardDuty detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/create_detector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#create_detector)
        """

    def create_filter(
        self, **kwargs: Unpack[CreateFilterRequestRequestTypeDef]
    ) -> CreateFilterResponseTypeDef:
        """
        Creates a filter using the specified finding criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/create_filter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#create_filter)
        """

    def create_ip_set(
        self, **kwargs: Unpack[CreateIPSetRequestRequestTypeDef]
    ) -> CreateIPSetResponseTypeDef:
        """
        Creates a new IPSet, which is called a trusted IP list in the console user
        interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/create_ip_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#create_ip_set)
        """

    def create_malware_protection_plan(
        self, **kwargs: Unpack[CreateMalwareProtectionPlanRequestRequestTypeDef]
    ) -> CreateMalwareProtectionPlanResponseTypeDef:
        """
        Creates a new Malware Protection plan for the protected resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/create_malware_protection_plan.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#create_malware_protection_plan)
        """

    def create_members(
        self, **kwargs: Unpack[CreateMembersRequestRequestTypeDef]
    ) -> CreateMembersResponseTypeDef:
        """
        Creates member accounts of the current Amazon Web Services account by
        specifying a list of Amazon Web Services account IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/create_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#create_members)
        """

    def create_publishing_destination(
        self, **kwargs: Unpack[CreatePublishingDestinationRequestRequestTypeDef]
    ) -> CreatePublishingDestinationResponseTypeDef:
        """
        Creates a publishing destination where you can export your GuardDuty findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/create_publishing_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#create_publishing_destination)
        """

    def create_sample_findings(
        self, **kwargs: Unpack[CreateSampleFindingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Generates sample findings of types specified by the list of finding types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/create_sample_findings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#create_sample_findings)
        """

    def create_threat_intel_set(
        self, **kwargs: Unpack[CreateThreatIntelSetRequestRequestTypeDef]
    ) -> CreateThreatIntelSetResponseTypeDef:
        """
        Creates a new ThreatIntelSet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/create_threat_intel_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#create_threat_intel_set)
        """

    def decline_invitations(
        self, **kwargs: Unpack[DeclineInvitationsRequestRequestTypeDef]
    ) -> DeclineInvitationsResponseTypeDef:
        """
        Declines invitations sent to the current member account by Amazon Web Services
        accounts specified by their account IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/decline_invitations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#decline_invitations)
        """

    def delete_detector(
        self, **kwargs: Unpack[DeleteDetectorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon GuardDuty detector that is specified by the detector ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/delete_detector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#delete_detector)
        """

    def delete_filter(self, **kwargs: Unpack[DeleteFilterRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the filter specified by the filter name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/delete_filter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#delete_filter)
        """

    def delete_ip_set(self, **kwargs: Unpack[DeleteIPSetRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the IPSet specified by the <code>ipSetId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/delete_ip_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#delete_ip_set)
        """

    def delete_invitations(
        self, **kwargs: Unpack[DeleteInvitationsRequestRequestTypeDef]
    ) -> DeleteInvitationsResponseTypeDef:
        """
        Deletes invitations sent to the current member account by Amazon Web Services
        accounts specified by their account IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/delete_invitations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#delete_invitations)
        """

    def delete_malware_protection_plan(
        self, **kwargs: Unpack[DeleteMalwareProtectionPlanRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the Malware Protection plan ID associated with the Malware Protection
        plan resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/delete_malware_protection_plan.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#delete_malware_protection_plan)
        """

    def delete_members(
        self, **kwargs: Unpack[DeleteMembersRequestRequestTypeDef]
    ) -> DeleteMembersResponseTypeDef:
        """
        Deletes GuardDuty member accounts (to the current GuardDuty administrator
        account) specified by the account IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/delete_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#delete_members)
        """

    def delete_publishing_destination(
        self, **kwargs: Unpack[DeletePublishingDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the publishing definition with the specified <code>destinationId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/delete_publishing_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#delete_publishing_destination)
        """

    def delete_threat_intel_set(
        self, **kwargs: Unpack[DeleteThreatIntelSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the ThreatIntelSet specified by the ThreatIntelSet ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/delete_threat_intel_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#delete_threat_intel_set)
        """

    def describe_malware_scans(
        self, **kwargs: Unpack[DescribeMalwareScansRequestRequestTypeDef]
    ) -> DescribeMalwareScansResponseTypeDef:
        """
        Returns a list of malware scans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/describe_malware_scans.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#describe_malware_scans)
        """

    def describe_organization_configuration(
        self, **kwargs: Unpack[DescribeOrganizationConfigurationRequestRequestTypeDef]
    ) -> DescribeOrganizationConfigurationResponseTypeDef:
        """
        Returns information about the account selected as the delegated administrator
        for GuardDuty.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/describe_organization_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#describe_organization_configuration)
        """

    def describe_publishing_destination(
        self, **kwargs: Unpack[DescribePublishingDestinationRequestRequestTypeDef]
    ) -> DescribePublishingDestinationResponseTypeDef:
        """
        Returns information about the publishing destination specified by the provided
        <code>destinationId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/describe_publishing_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#describe_publishing_destination)
        """

    def disable_organization_admin_account(
        self, **kwargs: Unpack[DisableOrganizationAdminAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the existing GuardDuty delegated administrator of the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/disable_organization_admin_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#disable_organization_admin_account)
        """

    def disassociate_from_administrator_account(
        self, **kwargs: Unpack[DisassociateFromAdministratorAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the current GuardDuty member account from its administrator
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/disassociate_from_administrator_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#disassociate_from_administrator_account)
        """

    def disassociate_from_master_account(
        self, **kwargs: Unpack[DisassociateFromMasterAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the current GuardDuty member account from its administrator
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/disassociate_from_master_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#disassociate_from_master_account)
        """

    def disassociate_members(
        self, **kwargs: Unpack[DisassociateMembersRequestRequestTypeDef]
    ) -> DisassociateMembersResponseTypeDef:
        """
        Disassociates GuardDuty member accounts (from the current administrator
        account) specified by the account IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/disassociate_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#disassociate_members)
        """

    def enable_organization_admin_account(
        self, **kwargs: Unpack[EnableOrganizationAdminAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Designates an Amazon Web Services account within the organization as your
        GuardDuty delegated administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/enable_organization_admin_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#enable_organization_admin_account)
        """

    def get_administrator_account(
        self, **kwargs: Unpack[GetAdministratorAccountRequestRequestTypeDef]
    ) -> GetAdministratorAccountResponseTypeDef:
        """
        Provides the details of the GuardDuty administrator account associated with the
        current GuardDuty member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_administrator_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_administrator_account)
        """

    def get_coverage_statistics(
        self, **kwargs: Unpack[GetCoverageStatisticsRequestRequestTypeDef]
    ) -> GetCoverageStatisticsResponseTypeDef:
        """
        Retrieves aggregated statistics for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_coverage_statistics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_coverage_statistics)
        """

    def get_detector(
        self, **kwargs: Unpack[GetDetectorRequestRequestTypeDef]
    ) -> GetDetectorResponseTypeDef:
        """
        Retrieves a GuardDuty detector specified by the detectorId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_detector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_detector)
        """

    def get_filter(
        self, **kwargs: Unpack[GetFilterRequestRequestTypeDef]
    ) -> GetFilterResponseTypeDef:
        """
        Returns the details of the filter specified by the filter name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_filter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_filter)
        """

    def get_findings(
        self, **kwargs: Unpack[GetFindingsRequestRequestTypeDef]
    ) -> GetFindingsResponseTypeDef:
        """
        Describes Amazon GuardDuty findings specified by finding IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_findings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_findings)
        """

    def get_findings_statistics(
        self, **kwargs: Unpack[GetFindingsStatisticsRequestRequestTypeDef]
    ) -> GetFindingsStatisticsResponseTypeDef:
        """
        Lists GuardDuty findings statistics for the specified detector ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_findings_statistics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_findings_statistics)
        """

    def get_ip_set(
        self, **kwargs: Unpack[GetIPSetRequestRequestTypeDef]
    ) -> GetIPSetResponseTypeDef:
        """
        Retrieves the IPSet specified by the <code>ipSetId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_ip_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_ip_set)
        """

    def get_invitations_count(self) -> GetInvitationsCountResponseTypeDef:
        """
        Returns the count of all GuardDuty membership invitations that were sent to the
        current member account except the currently accepted invitation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_invitations_count.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_invitations_count)
        """

    def get_malware_protection_plan(
        self, **kwargs: Unpack[GetMalwareProtectionPlanRequestRequestTypeDef]
    ) -> GetMalwareProtectionPlanResponseTypeDef:
        """
        Retrieves the Malware Protection plan details associated with a Malware
        Protection plan ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_malware_protection_plan.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_malware_protection_plan)
        """

    def get_malware_scan_settings(
        self, **kwargs: Unpack[GetMalwareScanSettingsRequestRequestTypeDef]
    ) -> GetMalwareScanSettingsResponseTypeDef:
        """
        Returns the details of the malware scan settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_malware_scan_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_malware_scan_settings)
        """

    def get_master_account(
        self, **kwargs: Unpack[GetMasterAccountRequestRequestTypeDef]
    ) -> GetMasterAccountResponseTypeDef:
        """
        Provides the details for the GuardDuty administrator account associated with
        the current GuardDuty member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_master_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_master_account)
        """

    def get_member_detectors(
        self, **kwargs: Unpack[GetMemberDetectorsRequestRequestTypeDef]
    ) -> GetMemberDetectorsResponseTypeDef:
        """
        Describes which data sources are enabled for the member account's detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_member_detectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_member_detectors)
        """

    def get_members(
        self, **kwargs: Unpack[GetMembersRequestRequestTypeDef]
    ) -> GetMembersResponseTypeDef:
        """
        Retrieves GuardDuty member accounts (of the current GuardDuty administrator
        account) specified by the account IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_members)
        """

    def get_organization_statistics(self) -> GetOrganizationStatisticsResponseTypeDef:
        """
        Retrieves how many active member accounts have each feature enabled within
        GuardDuty.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_organization_statistics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_organization_statistics)
        """

    def get_remaining_free_trial_days(
        self, **kwargs: Unpack[GetRemainingFreeTrialDaysRequestRequestTypeDef]
    ) -> GetRemainingFreeTrialDaysResponseTypeDef:
        """
        Provides the number of days left for each data source used in the free trial
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_remaining_free_trial_days.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_remaining_free_trial_days)
        """

    def get_threat_intel_set(
        self, **kwargs: Unpack[GetThreatIntelSetRequestRequestTypeDef]
    ) -> GetThreatIntelSetResponseTypeDef:
        """
        Retrieves the ThreatIntelSet that is specified by the ThreatIntelSet ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_threat_intel_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_threat_intel_set)
        """

    def get_usage_statistics(
        self, **kwargs: Unpack[GetUsageStatisticsRequestRequestTypeDef]
    ) -> GetUsageStatisticsResponseTypeDef:
        """
        Lists Amazon GuardDuty usage statistics over the last 30 days for the specified
        detector ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_usage_statistics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_usage_statistics)
        """

    def invite_members(
        self, **kwargs: Unpack[InviteMembersRequestRequestTypeDef]
    ) -> InviteMembersResponseTypeDef:
        """
        Invites Amazon Web Services accounts to become members of an organization
        administered by the Amazon Web Services account that invokes this API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/invite_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#invite_members)
        """

    def list_coverage(
        self, **kwargs: Unpack[ListCoverageRequestRequestTypeDef]
    ) -> ListCoverageResponseTypeDef:
        """
        Lists coverage details for your GuardDuty account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/list_coverage.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#list_coverage)
        """

    def list_detectors(
        self, **kwargs: Unpack[ListDetectorsRequestRequestTypeDef]
    ) -> ListDetectorsResponseTypeDef:
        """
        Lists detectorIds of all the existing Amazon GuardDuty detector resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/list_detectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#list_detectors)
        """

    def list_filters(
        self, **kwargs: Unpack[ListFiltersRequestRequestTypeDef]
    ) -> ListFiltersResponseTypeDef:
        """
        Returns a paginated list of the current filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/list_filters.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#list_filters)
        """

    def list_findings(
        self, **kwargs: Unpack[ListFindingsRequestRequestTypeDef]
    ) -> ListFindingsResponseTypeDef:
        """
        Lists GuardDuty findings for the specified detector ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/list_findings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#list_findings)
        """

    def list_ip_sets(
        self, **kwargs: Unpack[ListIPSetsRequestRequestTypeDef]
    ) -> ListIPSetsResponseTypeDef:
        """
        Lists the IPSets of the GuardDuty service specified by the detector ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/list_ip_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#list_ip_sets)
        """

    def list_invitations(
        self, **kwargs: Unpack[ListInvitationsRequestRequestTypeDef]
    ) -> ListInvitationsResponseTypeDef:
        """
        Lists all GuardDuty membership invitations that were sent to the current Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/list_invitations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#list_invitations)
        """

    def list_malware_protection_plans(
        self, **kwargs: Unpack[ListMalwareProtectionPlansRequestRequestTypeDef]
    ) -> ListMalwareProtectionPlansResponseTypeDef:
        """
        Lists the Malware Protection plan IDs associated with the protected resources
        in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/list_malware_protection_plans.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#list_malware_protection_plans)
        """

    def list_members(
        self, **kwargs: Unpack[ListMembersRequestRequestTypeDef]
    ) -> ListMembersResponseTypeDef:
        """
        Lists details about all member accounts for the current GuardDuty administrator
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/list_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#list_members)
        """

    def list_organization_admin_accounts(
        self, **kwargs: Unpack[ListOrganizationAdminAccountsRequestRequestTypeDef]
    ) -> ListOrganizationAdminAccountsResponseTypeDef:
        """
        Lists the accounts designated as GuardDuty delegated administrators.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/list_organization_admin_accounts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#list_organization_admin_accounts)
        """

    def list_publishing_destinations(
        self, **kwargs: Unpack[ListPublishingDestinationsRequestRequestTypeDef]
    ) -> ListPublishingDestinationsResponseTypeDef:
        """
        Returns a list of publishing destinations associated with the specified
        <code>detectorId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/list_publishing_destinations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#list_publishing_destinations)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#list_tags_for_resource)
        """

    def list_threat_intel_sets(
        self, **kwargs: Unpack[ListThreatIntelSetsRequestRequestTypeDef]
    ) -> ListThreatIntelSetsResponseTypeDef:
        """
        Lists the ThreatIntelSets of the GuardDuty service specified by the detector ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/list_threat_intel_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#list_threat_intel_sets)
        """

    def start_malware_scan(
        self, **kwargs: Unpack[StartMalwareScanRequestRequestTypeDef]
    ) -> StartMalwareScanResponseTypeDef:
        """
        Initiates the malware scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/start_malware_scan.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#start_malware_scan)
        """

    def start_monitoring_members(
        self, **kwargs: Unpack[StartMonitoringMembersRequestRequestTypeDef]
    ) -> StartMonitoringMembersResponseTypeDef:
        """
        Turns on GuardDuty monitoring of the specified member accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/start_monitoring_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#start_monitoring_members)
        """

    def stop_monitoring_members(
        self, **kwargs: Unpack[StopMonitoringMembersRequestRequestTypeDef]
    ) -> StopMonitoringMembersResponseTypeDef:
        """
        Stops GuardDuty monitoring for the specified member accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/stop_monitoring_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#stop_monitoring_members)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#tag_resource)
        """

    def unarchive_findings(
        self, **kwargs: Unpack[UnarchiveFindingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Unarchives GuardDuty findings specified by the <code>findingIds</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/unarchive_findings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#unarchive_findings)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#untag_resource)
        """

    def update_detector(
        self, **kwargs: Unpack[UpdateDetectorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the GuardDuty detector specified by the detector ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/update_detector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#update_detector)
        """

    def update_filter(
        self, **kwargs: Unpack[UpdateFilterRequestRequestTypeDef]
    ) -> UpdateFilterResponseTypeDef:
        """
        Updates the filter specified by the filter name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/update_filter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#update_filter)
        """

    def update_findings_feedback(
        self, **kwargs: Unpack[UpdateFindingsFeedbackRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Marks the specified GuardDuty findings as useful or not useful.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/update_findings_feedback.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#update_findings_feedback)
        """

    def update_ip_set(self, **kwargs: Unpack[UpdateIPSetRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the IPSet specified by the IPSet ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/update_ip_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#update_ip_set)
        """

    def update_malware_protection_plan(
        self, **kwargs: Unpack[UpdateMalwareProtectionPlanRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an existing Malware Protection plan resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/update_malware_protection_plan.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#update_malware_protection_plan)
        """

    def update_malware_scan_settings(
        self, **kwargs: Unpack[UpdateMalwareScanSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the malware scan settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/update_malware_scan_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#update_malware_scan_settings)
        """

    def update_member_detectors(
        self, **kwargs: Unpack[UpdateMemberDetectorsRequestRequestTypeDef]
    ) -> UpdateMemberDetectorsResponseTypeDef:
        """
        Contains information on member accounts to be updated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/update_member_detectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#update_member_detectors)
        """

    def update_organization_configuration(
        self, **kwargs: Unpack[UpdateOrganizationConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Configures the delegated administrator account with the provided values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/update_organization_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#update_organization_configuration)
        """

    def update_publishing_destination(
        self, **kwargs: Unpack[UpdatePublishingDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates information about the publishing destination specified by the
        <code>destinationId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/update_publishing_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#update_publishing_destination)
        """

    def update_threat_intel_set(
        self, **kwargs: Unpack[UpdateThreatIntelSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the ThreatIntelSet specified by the ThreatIntelSet ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/update_threat_intel_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#update_threat_intel_set)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_malware_scans"]
    ) -> DescribeMalwareScansPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_coverage"]) -> ListCoveragePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_detectors"]) -> ListDetectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_filters"]) -> ListFiltersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_findings"]) -> ListFindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_ip_sets"]) -> ListIPSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_invitations"]
    ) -> ListInvitationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_members"]) -> ListMembersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_organization_admin_accounts"]
    ) -> ListOrganizationAdminAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_threat_intel_sets"]
    ) -> ListThreatIntelSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/client/#get_paginator)
        """
