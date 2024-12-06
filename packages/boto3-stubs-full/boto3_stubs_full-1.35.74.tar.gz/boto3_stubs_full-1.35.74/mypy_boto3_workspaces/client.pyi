"""
Type annotations for workspaces service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_workspaces.client import WorkSpacesClient

    session = Session()
    client: WorkSpacesClient = session.client("workspaces")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeAccountModificationsPaginator,
    DescribeIpGroupsPaginator,
    DescribeWorkspaceBundlesPaginator,
    DescribeWorkspaceDirectoriesPaginator,
    DescribeWorkspaceImagesPaginator,
    DescribeWorkspacesConnectionStatusPaginator,
    DescribeWorkspacesPaginator,
    ListAccountLinksPaginator,
    ListAvailableManagementCidrRangesPaginator,
)
from .type_defs import (
    AcceptAccountLinkInvitationRequestRequestTypeDef,
    AcceptAccountLinkInvitationResultTypeDef,
    AssociateConnectionAliasRequestRequestTypeDef,
    AssociateConnectionAliasResultTypeDef,
    AssociateIpGroupsRequestRequestTypeDef,
    AssociateWorkspaceApplicationRequestRequestTypeDef,
    AssociateWorkspaceApplicationResultTypeDef,
    AuthorizeIpRulesRequestRequestTypeDef,
    CopyWorkspaceImageRequestRequestTypeDef,
    CopyWorkspaceImageResultTypeDef,
    CreateAccountLinkInvitationRequestRequestTypeDef,
    CreateAccountLinkInvitationResultTypeDef,
    CreateConnectClientAddInRequestRequestTypeDef,
    CreateConnectClientAddInResultTypeDef,
    CreateConnectionAliasRequestRequestTypeDef,
    CreateConnectionAliasResultTypeDef,
    CreateIpGroupRequestRequestTypeDef,
    CreateIpGroupResultTypeDef,
    CreateStandbyWorkspacesRequestRequestTypeDef,
    CreateStandbyWorkspacesResultTypeDef,
    CreateTagsRequestRequestTypeDef,
    CreateUpdatedWorkspaceImageRequestRequestTypeDef,
    CreateUpdatedWorkspaceImageResultTypeDef,
    CreateWorkspaceBundleRequestRequestTypeDef,
    CreateWorkspaceBundleResultTypeDef,
    CreateWorkspaceImageRequestRequestTypeDef,
    CreateWorkspaceImageResultTypeDef,
    CreateWorkspacesPoolRequestRequestTypeDef,
    CreateWorkspacesPoolResultTypeDef,
    CreateWorkspacesRequestRequestTypeDef,
    CreateWorkspacesResultTypeDef,
    DeleteAccountLinkInvitationRequestRequestTypeDef,
    DeleteAccountLinkInvitationResultTypeDef,
    DeleteClientBrandingRequestRequestTypeDef,
    DeleteConnectClientAddInRequestRequestTypeDef,
    DeleteConnectionAliasRequestRequestTypeDef,
    DeleteIpGroupRequestRequestTypeDef,
    DeleteTagsRequestRequestTypeDef,
    DeleteWorkspaceBundleRequestRequestTypeDef,
    DeleteWorkspaceImageRequestRequestTypeDef,
    DeployWorkspaceApplicationsRequestRequestTypeDef,
    DeployWorkspaceApplicationsResultTypeDef,
    DeregisterWorkspaceDirectoryRequestRequestTypeDef,
    DescribeAccountModificationsRequestRequestTypeDef,
    DescribeAccountModificationsResultTypeDef,
    DescribeAccountResultTypeDef,
    DescribeApplicationAssociationsRequestRequestTypeDef,
    DescribeApplicationAssociationsResultTypeDef,
    DescribeApplicationsRequestRequestTypeDef,
    DescribeApplicationsResultTypeDef,
    DescribeBundleAssociationsRequestRequestTypeDef,
    DescribeBundleAssociationsResultTypeDef,
    DescribeClientBrandingRequestRequestTypeDef,
    DescribeClientBrandingResultTypeDef,
    DescribeClientPropertiesRequestRequestTypeDef,
    DescribeClientPropertiesResultTypeDef,
    DescribeConnectClientAddInsRequestRequestTypeDef,
    DescribeConnectClientAddInsResultTypeDef,
    DescribeConnectionAliasesRequestRequestTypeDef,
    DescribeConnectionAliasesResultTypeDef,
    DescribeConnectionAliasPermissionsRequestRequestTypeDef,
    DescribeConnectionAliasPermissionsResultTypeDef,
    DescribeImageAssociationsRequestRequestTypeDef,
    DescribeImageAssociationsResultTypeDef,
    DescribeIpGroupsRequestRequestTypeDef,
    DescribeIpGroupsResultTypeDef,
    DescribeTagsRequestRequestTypeDef,
    DescribeTagsResultTypeDef,
    DescribeWorkspaceAssociationsRequestRequestTypeDef,
    DescribeWorkspaceAssociationsResultTypeDef,
    DescribeWorkspaceBundlesRequestRequestTypeDef,
    DescribeWorkspaceBundlesResultTypeDef,
    DescribeWorkspaceDirectoriesRequestRequestTypeDef,
    DescribeWorkspaceDirectoriesResultTypeDef,
    DescribeWorkspaceImagePermissionsRequestRequestTypeDef,
    DescribeWorkspaceImagePermissionsResultTypeDef,
    DescribeWorkspaceImagesRequestRequestTypeDef,
    DescribeWorkspaceImagesResultTypeDef,
    DescribeWorkspacesConnectionStatusRequestRequestTypeDef,
    DescribeWorkspacesConnectionStatusResultTypeDef,
    DescribeWorkspaceSnapshotsRequestRequestTypeDef,
    DescribeWorkspaceSnapshotsResultTypeDef,
    DescribeWorkspacesPoolSessionsRequestRequestTypeDef,
    DescribeWorkspacesPoolSessionsResultTypeDef,
    DescribeWorkspacesPoolsRequestRequestTypeDef,
    DescribeWorkspacesPoolsResultTypeDef,
    DescribeWorkspacesRequestRequestTypeDef,
    DescribeWorkspacesResultTypeDef,
    DisassociateConnectionAliasRequestRequestTypeDef,
    DisassociateIpGroupsRequestRequestTypeDef,
    DisassociateWorkspaceApplicationRequestRequestTypeDef,
    DisassociateWorkspaceApplicationResultTypeDef,
    GetAccountLinkRequestRequestTypeDef,
    GetAccountLinkResultTypeDef,
    ImportClientBrandingRequestRequestTypeDef,
    ImportClientBrandingResultTypeDef,
    ImportWorkspaceImageRequestRequestTypeDef,
    ImportWorkspaceImageResultTypeDef,
    ListAccountLinksRequestRequestTypeDef,
    ListAccountLinksResultTypeDef,
    ListAvailableManagementCidrRangesRequestRequestTypeDef,
    ListAvailableManagementCidrRangesResultTypeDef,
    MigrateWorkspaceRequestRequestTypeDef,
    MigrateWorkspaceResultTypeDef,
    ModifyAccountRequestRequestTypeDef,
    ModifyCertificateBasedAuthPropertiesRequestRequestTypeDef,
    ModifyClientPropertiesRequestRequestTypeDef,
    ModifySamlPropertiesRequestRequestTypeDef,
    ModifySelfservicePermissionsRequestRequestTypeDef,
    ModifyStreamingPropertiesRequestRequestTypeDef,
    ModifyWorkspaceAccessPropertiesRequestRequestTypeDef,
    ModifyWorkspaceCreationPropertiesRequestRequestTypeDef,
    ModifyWorkspacePropertiesRequestRequestTypeDef,
    ModifyWorkspaceStateRequestRequestTypeDef,
    RebootWorkspacesRequestRequestTypeDef,
    RebootWorkspacesResultTypeDef,
    RebuildWorkspacesRequestRequestTypeDef,
    RebuildWorkspacesResultTypeDef,
    RegisterWorkspaceDirectoryRequestRequestTypeDef,
    RegisterWorkspaceDirectoryResultTypeDef,
    RejectAccountLinkInvitationRequestRequestTypeDef,
    RejectAccountLinkInvitationResultTypeDef,
    RestoreWorkspaceRequestRequestTypeDef,
    RevokeIpRulesRequestRequestTypeDef,
    StartWorkspacesPoolRequestRequestTypeDef,
    StartWorkspacesRequestRequestTypeDef,
    StartWorkspacesResultTypeDef,
    StopWorkspacesPoolRequestRequestTypeDef,
    StopWorkspacesRequestRequestTypeDef,
    StopWorkspacesResultTypeDef,
    TerminateWorkspacesPoolRequestRequestTypeDef,
    TerminateWorkspacesPoolSessionRequestRequestTypeDef,
    TerminateWorkspacesRequestRequestTypeDef,
    TerminateWorkspacesResultTypeDef,
    UpdateConnectClientAddInRequestRequestTypeDef,
    UpdateConnectionAliasPermissionRequestRequestTypeDef,
    UpdateRulesOfIpGroupRequestRequestTypeDef,
    UpdateWorkspaceBundleRequestRequestTypeDef,
    UpdateWorkspaceImagePermissionRequestRequestTypeDef,
    UpdateWorkspacesPoolRequestRequestTypeDef,
    UpdateWorkspacesPoolResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("WorkSpacesClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ApplicationNotSupportedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ComputeNotCompatibleException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    IncompatibleApplicationsException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidParameterValuesException: Type[BotocoreClientError]
    InvalidResourceStateException: Type[BotocoreClientError]
    OperatingSystemNotCompatibleException: Type[BotocoreClientError]
    OperationInProgressException: Type[BotocoreClientError]
    OperationNotSupportedException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceAssociatedException: Type[BotocoreClientError]
    ResourceCreationFailedException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceUnavailableException: Type[BotocoreClientError]
    UnsupportedNetworkConfigurationException: Type[BotocoreClientError]
    UnsupportedWorkspaceConfigurationException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]
    WorkspacesDefaultRoleNotFoundException: Type[BotocoreClientError]

class WorkSpacesClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkSpacesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#close)
        """

    def accept_account_link_invitation(
        self, **kwargs: Unpack[AcceptAccountLinkInvitationRequestRequestTypeDef]
    ) -> AcceptAccountLinkInvitationResultTypeDef:
        """
        Accepts the account link invitation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/accept_account_link_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#accept_account_link_invitation)
        """

    def associate_connection_alias(
        self, **kwargs: Unpack[AssociateConnectionAliasRequestRequestTypeDef]
    ) -> AssociateConnectionAliasResultTypeDef:
        """
        Associates the specified connection alias with the specified directory to
        enable cross-Region redirection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/associate_connection_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#associate_connection_alias)
        """

    def associate_ip_groups(
        self, **kwargs: Unpack[AssociateIpGroupsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates the specified IP access control group with the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/associate_ip_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#associate_ip_groups)
        """

    def associate_workspace_application(
        self, **kwargs: Unpack[AssociateWorkspaceApplicationRequestRequestTypeDef]
    ) -> AssociateWorkspaceApplicationResultTypeDef:
        """
        Associates the specified application to the specified WorkSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/associate_workspace_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#associate_workspace_application)
        """

    def authorize_ip_rules(
        self, **kwargs: Unpack[AuthorizeIpRulesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds one or more rules to the specified IP access control group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/authorize_ip_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#authorize_ip_rules)
        """

    def copy_workspace_image(
        self, **kwargs: Unpack[CopyWorkspaceImageRequestRequestTypeDef]
    ) -> CopyWorkspaceImageResultTypeDef:
        """
        Copies the specified image from the specified Region to the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/copy_workspace_image.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#copy_workspace_image)
        """

    def create_account_link_invitation(
        self, **kwargs: Unpack[CreateAccountLinkInvitationRequestRequestTypeDef]
    ) -> CreateAccountLinkInvitationResultTypeDef:
        """
        Creates the account link invitation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/create_account_link_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#create_account_link_invitation)
        """

    def create_connect_client_add_in(
        self, **kwargs: Unpack[CreateConnectClientAddInRequestRequestTypeDef]
    ) -> CreateConnectClientAddInResultTypeDef:
        """
        Creates a client-add-in for Amazon Connect within a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/create_connect_client_add_in.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#create_connect_client_add_in)
        """

    def create_connection_alias(
        self, **kwargs: Unpack[CreateConnectionAliasRequestRequestTypeDef]
    ) -> CreateConnectionAliasResultTypeDef:
        """
        Creates the specified connection alias for use with cross-Region redirection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/create_connection_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#create_connection_alias)
        """

    def create_ip_group(
        self, **kwargs: Unpack[CreateIpGroupRequestRequestTypeDef]
    ) -> CreateIpGroupResultTypeDef:
        """
        Creates an IP access control group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/create_ip_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#create_ip_group)
        """

    def create_standby_workspaces(
        self, **kwargs: Unpack[CreateStandbyWorkspacesRequestRequestTypeDef]
    ) -> CreateStandbyWorkspacesResultTypeDef:
        """
        Creates a standby WorkSpace in a secondary Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/create_standby_workspaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#create_standby_workspaces)
        """

    def create_tags(self, **kwargs: Unpack[CreateTagsRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates the specified tags for the specified WorkSpaces resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/create_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#create_tags)
        """

    def create_updated_workspace_image(
        self, **kwargs: Unpack[CreateUpdatedWorkspaceImageRequestRequestTypeDef]
    ) -> CreateUpdatedWorkspaceImageResultTypeDef:
        """
        Creates a new updated WorkSpace image based on the specified source image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/create_updated_workspace_image.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#create_updated_workspace_image)
        """

    def create_workspace_bundle(
        self, **kwargs: Unpack[CreateWorkspaceBundleRequestRequestTypeDef]
    ) -> CreateWorkspaceBundleResultTypeDef:
        """
        Creates the specified WorkSpace bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/create_workspace_bundle.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#create_workspace_bundle)
        """

    def create_workspace_image(
        self, **kwargs: Unpack[CreateWorkspaceImageRequestRequestTypeDef]
    ) -> CreateWorkspaceImageResultTypeDef:
        """
        Creates a new WorkSpace image from an existing WorkSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/create_workspace_image.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#create_workspace_image)
        """

    def create_workspaces(
        self, **kwargs: Unpack[CreateWorkspacesRequestRequestTypeDef]
    ) -> CreateWorkspacesResultTypeDef:
        """
        Creates one or more WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/create_workspaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#create_workspaces)
        """

    def create_workspaces_pool(
        self, **kwargs: Unpack[CreateWorkspacesPoolRequestRequestTypeDef]
    ) -> CreateWorkspacesPoolResultTypeDef:
        """
        Creates a pool of WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/create_workspaces_pool.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#create_workspaces_pool)
        """

    def delete_account_link_invitation(
        self, **kwargs: Unpack[DeleteAccountLinkInvitationRequestRequestTypeDef]
    ) -> DeleteAccountLinkInvitationResultTypeDef:
        """
        Deletes the account link invitation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/delete_account_link_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#delete_account_link_invitation)
        """

    def delete_client_branding(
        self, **kwargs: Unpack[DeleteClientBrandingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes customized client branding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/delete_client_branding.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#delete_client_branding)
        """

    def delete_connect_client_add_in(
        self, **kwargs: Unpack[DeleteConnectClientAddInRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a client-add-in for Amazon Connect that is configured within a
        directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/delete_connect_client_add_in.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#delete_connect_client_add_in)
        """

    def delete_connection_alias(
        self, **kwargs: Unpack[DeleteConnectionAliasRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified connection alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/delete_connection_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#delete_connection_alias)
        """

    def delete_ip_group(
        self, **kwargs: Unpack[DeleteIpGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified IP access control group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/delete_ip_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#delete_ip_group)
        """

    def delete_tags(self, **kwargs: Unpack[DeleteTagsRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified tags from the specified WorkSpaces resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/delete_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#delete_tags)
        """

    def delete_workspace_bundle(
        self, **kwargs: Unpack[DeleteWorkspaceBundleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified WorkSpace bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/delete_workspace_bundle.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#delete_workspace_bundle)
        """

    def delete_workspace_image(
        self, **kwargs: Unpack[DeleteWorkspaceImageRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified image from your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/delete_workspace_image.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#delete_workspace_image)
        """

    def deploy_workspace_applications(
        self, **kwargs: Unpack[DeployWorkspaceApplicationsRequestRequestTypeDef]
    ) -> DeployWorkspaceApplicationsResultTypeDef:
        """
        Deploys associated applications to the specified WorkSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/deploy_workspace_applications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#deploy_workspace_applications)
        """

    def deregister_workspace_directory(
        self, **kwargs: Unpack[DeregisterWorkspaceDirectoryRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deregisters the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/deregister_workspace_directory.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#deregister_workspace_directory)
        """

    def describe_account(self) -> DescribeAccountResultTypeDef:
        """
        Retrieves a list that describes the configuration of Bring Your Own License
        (BYOL) for the specified account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_account)
        """

    def describe_account_modifications(
        self, **kwargs: Unpack[DescribeAccountModificationsRequestRequestTypeDef]
    ) -> DescribeAccountModificationsResultTypeDef:
        """
        Retrieves a list that describes modifications to the configuration of Bring
        Your Own License (BYOL) for the specified account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_account_modifications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_account_modifications)
        """

    def describe_application_associations(
        self, **kwargs: Unpack[DescribeApplicationAssociationsRequestRequestTypeDef]
    ) -> DescribeApplicationAssociationsResultTypeDef:
        """
        Describes the associations between the application and the specified associated
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_application_associations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_application_associations)
        """

    def describe_applications(
        self, **kwargs: Unpack[DescribeApplicationsRequestRequestTypeDef]
    ) -> DescribeApplicationsResultTypeDef:
        """
        Describes the specified applications by filtering based on their compute types,
        license availability, operating systems, and owners.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_applications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_applications)
        """

    def describe_bundle_associations(
        self, **kwargs: Unpack[DescribeBundleAssociationsRequestRequestTypeDef]
    ) -> DescribeBundleAssociationsResultTypeDef:
        """
        Describes the associations between the applications and the specified bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_bundle_associations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_bundle_associations)
        """

    def describe_client_branding(
        self, **kwargs: Unpack[DescribeClientBrandingRequestRequestTypeDef]
    ) -> DescribeClientBrandingResultTypeDef:
        """
        Describes the specified client branding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_client_branding.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_client_branding)
        """

    def describe_client_properties(
        self, **kwargs: Unpack[DescribeClientPropertiesRequestRequestTypeDef]
    ) -> DescribeClientPropertiesResultTypeDef:
        """
        Retrieves a list that describes one or more specified Amazon WorkSpaces clients.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_client_properties.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_client_properties)
        """

    def describe_connect_client_add_ins(
        self, **kwargs: Unpack[DescribeConnectClientAddInsRequestRequestTypeDef]
    ) -> DescribeConnectClientAddInsResultTypeDef:
        """
        Retrieves a list of Amazon Connect client add-ins that have been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_connect_client_add_ins.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_connect_client_add_ins)
        """

    def describe_connection_alias_permissions(
        self, **kwargs: Unpack[DescribeConnectionAliasPermissionsRequestRequestTypeDef]
    ) -> DescribeConnectionAliasPermissionsResultTypeDef:
        """
        Describes the permissions that the owner of a connection alias has granted to
        another Amazon Web Services account for the specified connection alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_connection_alias_permissions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_connection_alias_permissions)
        """

    def describe_connection_aliases(
        self, **kwargs: Unpack[DescribeConnectionAliasesRequestRequestTypeDef]
    ) -> DescribeConnectionAliasesResultTypeDef:
        """
        Retrieves a list that describes the connection aliases used for cross-Region
        redirection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_connection_aliases.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_connection_aliases)
        """

    def describe_image_associations(
        self, **kwargs: Unpack[DescribeImageAssociationsRequestRequestTypeDef]
    ) -> DescribeImageAssociationsResultTypeDef:
        """
        Describes the associations between the applications and the specified image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_image_associations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_image_associations)
        """

    def describe_ip_groups(
        self, **kwargs: Unpack[DescribeIpGroupsRequestRequestTypeDef]
    ) -> DescribeIpGroupsResultTypeDef:
        """
        Describes one or more of your IP access control groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_ip_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_ip_groups)
        """

    def describe_tags(
        self, **kwargs: Unpack[DescribeTagsRequestRequestTypeDef]
    ) -> DescribeTagsResultTypeDef:
        """
        Describes the specified tags for the specified WorkSpaces resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_tags)
        """

    def describe_workspace_associations(
        self, **kwargs: Unpack[DescribeWorkspaceAssociationsRequestRequestTypeDef]
    ) -> DescribeWorkspaceAssociationsResultTypeDef:
        """
        Describes the associations betweens applications and the specified WorkSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_workspace_associations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_workspace_associations)
        """

    def describe_workspace_bundles(
        self, **kwargs: Unpack[DescribeWorkspaceBundlesRequestRequestTypeDef]
    ) -> DescribeWorkspaceBundlesResultTypeDef:
        """
        Retrieves a list that describes the available WorkSpace bundles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_workspace_bundles.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_workspace_bundles)
        """

    def describe_workspace_directories(
        self, **kwargs: Unpack[DescribeWorkspaceDirectoriesRequestRequestTypeDef]
    ) -> DescribeWorkspaceDirectoriesResultTypeDef:
        """
        Describes the available directories that are registered with Amazon WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_workspace_directories.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_workspace_directories)
        """

    def describe_workspace_image_permissions(
        self, **kwargs: Unpack[DescribeWorkspaceImagePermissionsRequestRequestTypeDef]
    ) -> DescribeWorkspaceImagePermissionsResultTypeDef:
        """
        Describes the permissions that the owner of an image has granted to other
        Amazon Web Services accounts for an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_workspace_image_permissions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_workspace_image_permissions)
        """

    def describe_workspace_images(
        self, **kwargs: Unpack[DescribeWorkspaceImagesRequestRequestTypeDef]
    ) -> DescribeWorkspaceImagesResultTypeDef:
        """
        Retrieves a list that describes one or more specified images, if the image
        identifiers are provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_workspace_images.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_workspace_images)
        """

    def describe_workspace_snapshots(
        self, **kwargs: Unpack[DescribeWorkspaceSnapshotsRequestRequestTypeDef]
    ) -> DescribeWorkspaceSnapshotsResultTypeDef:
        """
        Describes the snapshots for the specified WorkSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_workspace_snapshots.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_workspace_snapshots)
        """

    def describe_workspaces(
        self, **kwargs: Unpack[DescribeWorkspacesRequestRequestTypeDef]
    ) -> DescribeWorkspacesResultTypeDef:
        """
        Describes the specified WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_workspaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_workspaces)
        """

    def describe_workspaces_connection_status(
        self, **kwargs: Unpack[DescribeWorkspacesConnectionStatusRequestRequestTypeDef]
    ) -> DescribeWorkspacesConnectionStatusResultTypeDef:
        """
        Describes the connection status of the specified WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_workspaces_connection_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_workspaces_connection_status)
        """

    def describe_workspaces_pool_sessions(
        self, **kwargs: Unpack[DescribeWorkspacesPoolSessionsRequestRequestTypeDef]
    ) -> DescribeWorkspacesPoolSessionsResultTypeDef:
        """
        Retrieves a list that describes the streaming sessions for a specified pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_workspaces_pool_sessions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_workspaces_pool_sessions)
        """

    def describe_workspaces_pools(
        self, **kwargs: Unpack[DescribeWorkspacesPoolsRequestRequestTypeDef]
    ) -> DescribeWorkspacesPoolsResultTypeDef:
        """
        Describes the specified WorkSpaces Pools.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/describe_workspaces_pools.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#describe_workspaces_pools)
        """

    def disassociate_connection_alias(
        self, **kwargs: Unpack[DisassociateConnectionAliasRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a connection alias from a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/disassociate_connection_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#disassociate_connection_alias)
        """

    def disassociate_ip_groups(
        self, **kwargs: Unpack[DisassociateIpGroupsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified IP access control group from the specified
        directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/disassociate_ip_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#disassociate_ip_groups)
        """

    def disassociate_workspace_application(
        self, **kwargs: Unpack[DisassociateWorkspaceApplicationRequestRequestTypeDef]
    ) -> DisassociateWorkspaceApplicationResultTypeDef:
        """
        Disassociates the specified application from a WorkSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/disassociate_workspace_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#disassociate_workspace_application)
        """

    def get_account_link(
        self, **kwargs: Unpack[GetAccountLinkRequestRequestTypeDef]
    ) -> GetAccountLinkResultTypeDef:
        """
        Retrieves account link information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/get_account_link.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#get_account_link)
        """

    def import_client_branding(
        self, **kwargs: Unpack[ImportClientBrandingRequestRequestTypeDef]
    ) -> ImportClientBrandingResultTypeDef:
        """
        Imports client branding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/import_client_branding.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#import_client_branding)
        """

    def import_workspace_image(
        self, **kwargs: Unpack[ImportWorkspaceImageRequestRequestTypeDef]
    ) -> ImportWorkspaceImageResultTypeDef:
        """
        Imports the specified Windows 10 or 11 Bring Your Own License (BYOL) image into
        Amazon WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/import_workspace_image.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#import_workspace_image)
        """

    def list_account_links(
        self, **kwargs: Unpack[ListAccountLinksRequestRequestTypeDef]
    ) -> ListAccountLinksResultTypeDef:
        """
        Lists all account links.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/list_account_links.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#list_account_links)
        """

    def list_available_management_cidr_ranges(
        self, **kwargs: Unpack[ListAvailableManagementCidrRangesRequestRequestTypeDef]
    ) -> ListAvailableManagementCidrRangesResultTypeDef:
        """
        Retrieves a list of IP address ranges, specified as IPv4 CIDR blocks, that you
        can use for the network management interface when you enable Bring Your Own
        License (BYOL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/list_available_management_cidr_ranges.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#list_available_management_cidr_ranges)
        """

    def migrate_workspace(
        self, **kwargs: Unpack[MigrateWorkspaceRequestRequestTypeDef]
    ) -> MigrateWorkspaceResultTypeDef:
        """
        Migrates a WorkSpace from one operating system or bundle type to another, while
        retaining the data on the user volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/migrate_workspace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#migrate_workspace)
        """

    def modify_account(
        self, **kwargs: Unpack[ModifyAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies the configuration of Bring Your Own License (BYOL) for the specified
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/modify_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#modify_account)
        """

    def modify_certificate_based_auth_properties(
        self, **kwargs: Unpack[ModifyCertificateBasedAuthPropertiesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies the properties of the certificate-based authentication you want to use
        with your WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/modify_certificate_based_auth_properties.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#modify_certificate_based_auth_properties)
        """

    def modify_client_properties(
        self, **kwargs: Unpack[ModifyClientPropertiesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies the properties of the specified Amazon WorkSpaces clients.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/modify_client_properties.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#modify_client_properties)
        """

    def modify_saml_properties(
        self, **kwargs: Unpack[ModifySamlPropertiesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies multiple properties related to SAML 2.0 authentication, including the
        enablement status, user access URL, and relay state parameter name that are
        used for configuring federation with an SAML 2.0 identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/modify_saml_properties.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#modify_saml_properties)
        """

    def modify_selfservice_permissions(
        self, **kwargs: Unpack[ModifySelfservicePermissionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies the self-service WorkSpace management capabilities for your users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/modify_selfservice_permissions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#modify_selfservice_permissions)
        """

    def modify_streaming_properties(
        self, **kwargs: Unpack[ModifyStreamingPropertiesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies the specified streaming properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/modify_streaming_properties.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#modify_streaming_properties)
        """

    def modify_workspace_access_properties(
        self, **kwargs: Unpack[ModifyWorkspaceAccessPropertiesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Specifies which devices and operating systems users can use to access their
        WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/modify_workspace_access_properties.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#modify_workspace_access_properties)
        """

    def modify_workspace_creation_properties(
        self, **kwargs: Unpack[ModifyWorkspaceCreationPropertiesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modify the default properties used to create WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/modify_workspace_creation_properties.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#modify_workspace_creation_properties)
        """

    def modify_workspace_properties(
        self, **kwargs: Unpack[ModifyWorkspacePropertiesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies the specified WorkSpace properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/modify_workspace_properties.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#modify_workspace_properties)
        """

    def modify_workspace_state(
        self, **kwargs: Unpack[ModifyWorkspaceStateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the state of the specified WorkSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/modify_workspace_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#modify_workspace_state)
        """

    def reboot_workspaces(
        self, **kwargs: Unpack[RebootWorkspacesRequestRequestTypeDef]
    ) -> RebootWorkspacesResultTypeDef:
        """
        Reboots the specified WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/reboot_workspaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#reboot_workspaces)
        """

    def rebuild_workspaces(
        self, **kwargs: Unpack[RebuildWorkspacesRequestRequestTypeDef]
    ) -> RebuildWorkspacesResultTypeDef:
        """
        Rebuilds the specified WorkSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/rebuild_workspaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#rebuild_workspaces)
        """

    def register_workspace_directory(
        self, **kwargs: Unpack[RegisterWorkspaceDirectoryRequestRequestTypeDef]
    ) -> RegisterWorkspaceDirectoryResultTypeDef:
        """
        Registers the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/register_workspace_directory.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#register_workspace_directory)
        """

    def reject_account_link_invitation(
        self, **kwargs: Unpack[RejectAccountLinkInvitationRequestRequestTypeDef]
    ) -> RejectAccountLinkInvitationResultTypeDef:
        """
        Rejects the account link invitation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/reject_account_link_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#reject_account_link_invitation)
        """

    def restore_workspace(
        self, **kwargs: Unpack[RestoreWorkspaceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Restores the specified WorkSpace to its last known healthy state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/restore_workspace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#restore_workspace)
        """

    def revoke_ip_rules(
        self, **kwargs: Unpack[RevokeIpRulesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more rules from the specified IP access control group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/revoke_ip_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#revoke_ip_rules)
        """

    def start_workspaces(
        self, **kwargs: Unpack[StartWorkspacesRequestRequestTypeDef]
    ) -> StartWorkspacesResultTypeDef:
        """
        Starts the specified WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/start_workspaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#start_workspaces)
        """

    def start_workspaces_pool(
        self, **kwargs: Unpack[StartWorkspacesPoolRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts the specified pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/start_workspaces_pool.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#start_workspaces_pool)
        """

    def stop_workspaces(
        self, **kwargs: Unpack[StopWorkspacesRequestRequestTypeDef]
    ) -> StopWorkspacesResultTypeDef:
        """
        Stops the specified WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/stop_workspaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#stop_workspaces)
        """

    def stop_workspaces_pool(
        self, **kwargs: Unpack[StopWorkspacesPoolRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops the specified pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/stop_workspaces_pool.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#stop_workspaces_pool)
        """

    def terminate_workspaces(
        self, **kwargs: Unpack[TerminateWorkspacesRequestRequestTypeDef]
    ) -> TerminateWorkspacesResultTypeDef:
        """
        Terminates the specified WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/terminate_workspaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#terminate_workspaces)
        """

    def terminate_workspaces_pool(
        self, **kwargs: Unpack[TerminateWorkspacesPoolRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Terminates the specified pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/terminate_workspaces_pool.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#terminate_workspaces_pool)
        """

    def terminate_workspaces_pool_session(
        self, **kwargs: Unpack[TerminateWorkspacesPoolSessionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Terminates the pool session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/terminate_workspaces_pool_session.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#terminate_workspaces_pool_session)
        """

    def update_connect_client_add_in(
        self, **kwargs: Unpack[UpdateConnectClientAddInRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a Amazon Connect client add-in.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/update_connect_client_add_in.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#update_connect_client_add_in)
        """

    def update_connection_alias_permission(
        self, **kwargs: Unpack[UpdateConnectionAliasPermissionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Shares or unshares a connection alias with one account by specifying whether
        that account has permission to associate the connection alias with a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/update_connection_alias_permission.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#update_connection_alias_permission)
        """

    def update_rules_of_ip_group(
        self, **kwargs: Unpack[UpdateRulesOfIpGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Replaces the current rules of the specified IP access control group with the
        specified rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/update_rules_of_ip_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#update_rules_of_ip_group)
        """

    def update_workspace_bundle(
        self, **kwargs: Unpack[UpdateWorkspaceBundleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a WorkSpace bundle with a new image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/update_workspace_bundle.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#update_workspace_bundle)
        """

    def update_workspace_image_permission(
        self, **kwargs: Unpack[UpdateWorkspaceImagePermissionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Shares or unshares an image with one account in the same Amazon Web Services
        Region by specifying whether that account has permission to copy the image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/update_workspace_image_permission.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#update_workspace_image_permission)
        """

    def update_workspaces_pool(
        self, **kwargs: Unpack[UpdateWorkspacesPoolRequestRequestTypeDef]
    ) -> UpdateWorkspacesPoolResultTypeDef:
        """
        Updates the specified pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/update_workspaces_pool.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#update_workspaces_pool)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_account_modifications"]
    ) -> DescribeAccountModificationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_ip_groups"]
    ) -> DescribeIpGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_workspace_bundles"]
    ) -> DescribeWorkspaceBundlesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_workspace_directories"]
    ) -> DescribeWorkspaceDirectoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_workspace_images"]
    ) -> DescribeWorkspaceImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_workspaces_connection_status"]
    ) -> DescribeWorkspacesConnectionStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_workspaces"]
    ) -> DescribeWorkspacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_links"]
    ) -> ListAccountLinksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_available_management_cidr_ranges"]
    ) -> ListAvailableManagementCidrRangesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces/client/#get_paginator)
        """
