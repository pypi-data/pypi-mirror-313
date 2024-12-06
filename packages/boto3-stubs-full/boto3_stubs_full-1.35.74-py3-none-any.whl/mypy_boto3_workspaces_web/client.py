"""
Type annotations for workspaces-web service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_workspaces_web.client import WorkSpacesWebClient

    session = Session()
    client: WorkSpacesWebClient = session.client("workspaces-web")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListDataProtectionSettingsPaginator, ListSessionsPaginator
from .type_defs import (
    AssociateBrowserSettingsRequestRequestTypeDef,
    AssociateBrowserSettingsResponseTypeDef,
    AssociateDataProtectionSettingsRequestRequestTypeDef,
    AssociateDataProtectionSettingsResponseTypeDef,
    AssociateIpAccessSettingsRequestRequestTypeDef,
    AssociateIpAccessSettingsResponseTypeDef,
    AssociateNetworkSettingsRequestRequestTypeDef,
    AssociateNetworkSettingsResponseTypeDef,
    AssociateTrustStoreRequestRequestTypeDef,
    AssociateTrustStoreResponseTypeDef,
    AssociateUserAccessLoggingSettingsRequestRequestTypeDef,
    AssociateUserAccessLoggingSettingsResponseTypeDef,
    AssociateUserSettingsRequestRequestTypeDef,
    AssociateUserSettingsResponseTypeDef,
    CreateBrowserSettingsRequestRequestTypeDef,
    CreateBrowserSettingsResponseTypeDef,
    CreateDataProtectionSettingsRequestRequestTypeDef,
    CreateDataProtectionSettingsResponseTypeDef,
    CreateIdentityProviderRequestRequestTypeDef,
    CreateIdentityProviderResponseTypeDef,
    CreateIpAccessSettingsRequestRequestTypeDef,
    CreateIpAccessSettingsResponseTypeDef,
    CreateNetworkSettingsRequestRequestTypeDef,
    CreateNetworkSettingsResponseTypeDef,
    CreatePortalRequestRequestTypeDef,
    CreatePortalResponseTypeDef,
    CreateTrustStoreRequestRequestTypeDef,
    CreateTrustStoreResponseTypeDef,
    CreateUserAccessLoggingSettingsRequestRequestTypeDef,
    CreateUserAccessLoggingSettingsResponseTypeDef,
    CreateUserSettingsRequestRequestTypeDef,
    CreateUserSettingsResponseTypeDef,
    DeleteBrowserSettingsRequestRequestTypeDef,
    DeleteDataProtectionSettingsRequestRequestTypeDef,
    DeleteIdentityProviderRequestRequestTypeDef,
    DeleteIpAccessSettingsRequestRequestTypeDef,
    DeleteNetworkSettingsRequestRequestTypeDef,
    DeletePortalRequestRequestTypeDef,
    DeleteTrustStoreRequestRequestTypeDef,
    DeleteUserAccessLoggingSettingsRequestRequestTypeDef,
    DeleteUserSettingsRequestRequestTypeDef,
    DisassociateBrowserSettingsRequestRequestTypeDef,
    DisassociateDataProtectionSettingsRequestRequestTypeDef,
    DisassociateIpAccessSettingsRequestRequestTypeDef,
    DisassociateNetworkSettingsRequestRequestTypeDef,
    DisassociateTrustStoreRequestRequestTypeDef,
    DisassociateUserAccessLoggingSettingsRequestRequestTypeDef,
    DisassociateUserSettingsRequestRequestTypeDef,
    ExpireSessionRequestRequestTypeDef,
    GetBrowserSettingsRequestRequestTypeDef,
    GetBrowserSettingsResponseTypeDef,
    GetDataProtectionSettingsRequestRequestTypeDef,
    GetDataProtectionSettingsResponseTypeDef,
    GetIdentityProviderRequestRequestTypeDef,
    GetIdentityProviderResponseTypeDef,
    GetIpAccessSettingsRequestRequestTypeDef,
    GetIpAccessSettingsResponseTypeDef,
    GetNetworkSettingsRequestRequestTypeDef,
    GetNetworkSettingsResponseTypeDef,
    GetPortalRequestRequestTypeDef,
    GetPortalResponseTypeDef,
    GetPortalServiceProviderMetadataRequestRequestTypeDef,
    GetPortalServiceProviderMetadataResponseTypeDef,
    GetSessionRequestRequestTypeDef,
    GetSessionResponseTypeDef,
    GetTrustStoreCertificateRequestRequestTypeDef,
    GetTrustStoreCertificateResponseTypeDef,
    GetTrustStoreRequestRequestTypeDef,
    GetTrustStoreResponseTypeDef,
    GetUserAccessLoggingSettingsRequestRequestTypeDef,
    GetUserAccessLoggingSettingsResponseTypeDef,
    GetUserSettingsRequestRequestTypeDef,
    GetUserSettingsResponseTypeDef,
    ListBrowserSettingsRequestRequestTypeDef,
    ListBrowserSettingsResponseTypeDef,
    ListDataProtectionSettingsRequestRequestTypeDef,
    ListDataProtectionSettingsResponseTypeDef,
    ListIdentityProvidersRequestRequestTypeDef,
    ListIdentityProvidersResponseTypeDef,
    ListIpAccessSettingsRequestRequestTypeDef,
    ListIpAccessSettingsResponseTypeDef,
    ListNetworkSettingsRequestRequestTypeDef,
    ListNetworkSettingsResponseTypeDef,
    ListPortalsRequestRequestTypeDef,
    ListPortalsResponseTypeDef,
    ListSessionsRequestRequestTypeDef,
    ListSessionsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrustStoreCertificatesRequestRequestTypeDef,
    ListTrustStoreCertificatesResponseTypeDef,
    ListTrustStoresRequestRequestTypeDef,
    ListTrustStoresResponseTypeDef,
    ListUserAccessLoggingSettingsRequestRequestTypeDef,
    ListUserAccessLoggingSettingsResponseTypeDef,
    ListUserSettingsRequestRequestTypeDef,
    ListUserSettingsResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateBrowserSettingsRequestRequestTypeDef,
    UpdateBrowserSettingsResponseTypeDef,
    UpdateDataProtectionSettingsRequestRequestTypeDef,
    UpdateDataProtectionSettingsResponseTypeDef,
    UpdateIdentityProviderRequestRequestTypeDef,
    UpdateIdentityProviderResponseTypeDef,
    UpdateIpAccessSettingsRequestRequestTypeDef,
    UpdateIpAccessSettingsResponseTypeDef,
    UpdateNetworkSettingsRequestRequestTypeDef,
    UpdateNetworkSettingsResponseTypeDef,
    UpdatePortalRequestRequestTypeDef,
    UpdatePortalResponseTypeDef,
    UpdateTrustStoreRequestRequestTypeDef,
    UpdateTrustStoreResponseTypeDef,
    UpdateUserAccessLoggingSettingsRequestRequestTypeDef,
    UpdateUserAccessLoggingSettingsResponseTypeDef,
    UpdateUserSettingsRequestRequestTypeDef,
    UpdateUserSettingsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("WorkSpacesWebClient",)


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
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class WorkSpacesWebClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web.html#WorkSpacesWeb.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkSpacesWebClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web.html#WorkSpacesWeb.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#close)
        """

    def associate_browser_settings(
        self, **kwargs: Unpack[AssociateBrowserSettingsRequestRequestTypeDef]
    ) -> AssociateBrowserSettingsResponseTypeDef:
        """
        Associates a browser settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_browser_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#associate_browser_settings)
        """

    def associate_data_protection_settings(
        self, **kwargs: Unpack[AssociateDataProtectionSettingsRequestRequestTypeDef]
    ) -> AssociateDataProtectionSettingsResponseTypeDef:
        """
        Associates a data protection settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_data_protection_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#associate_data_protection_settings)
        """

    def associate_ip_access_settings(
        self, **kwargs: Unpack[AssociateIpAccessSettingsRequestRequestTypeDef]
    ) -> AssociateIpAccessSettingsResponseTypeDef:
        """
        Associates an IP access settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_ip_access_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#associate_ip_access_settings)
        """

    def associate_network_settings(
        self, **kwargs: Unpack[AssociateNetworkSettingsRequestRequestTypeDef]
    ) -> AssociateNetworkSettingsResponseTypeDef:
        """
        Associates a network settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_network_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#associate_network_settings)
        """

    def associate_trust_store(
        self, **kwargs: Unpack[AssociateTrustStoreRequestRequestTypeDef]
    ) -> AssociateTrustStoreResponseTypeDef:
        """
        Associates a trust store with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_trust_store.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#associate_trust_store)
        """

    def associate_user_access_logging_settings(
        self, **kwargs: Unpack[AssociateUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> AssociateUserAccessLoggingSettingsResponseTypeDef:
        """
        Associates a user access logging settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_user_access_logging_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#associate_user_access_logging_settings)
        """

    def associate_user_settings(
        self, **kwargs: Unpack[AssociateUserSettingsRequestRequestTypeDef]
    ) -> AssociateUserSettingsResponseTypeDef:
        """
        Associates a user settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_user_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#associate_user_settings)
        """

    def create_browser_settings(
        self, **kwargs: Unpack[CreateBrowserSettingsRequestRequestTypeDef]
    ) -> CreateBrowserSettingsResponseTypeDef:
        """
        Creates a browser settings resource that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_browser_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#create_browser_settings)
        """

    def create_data_protection_settings(
        self, **kwargs: Unpack[CreateDataProtectionSettingsRequestRequestTypeDef]
    ) -> CreateDataProtectionSettingsResponseTypeDef:
        """
        Creates a data protection settings resource that can be associated with a web
        portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_data_protection_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#create_data_protection_settings)
        """

    def create_identity_provider(
        self, **kwargs: Unpack[CreateIdentityProviderRequestRequestTypeDef]
    ) -> CreateIdentityProviderResponseTypeDef:
        """
        Creates an identity provider resource that is then associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_identity_provider.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#create_identity_provider)
        """

    def create_ip_access_settings(
        self, **kwargs: Unpack[CreateIpAccessSettingsRequestRequestTypeDef]
    ) -> CreateIpAccessSettingsResponseTypeDef:
        """
        Creates an IP access settings resource that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_ip_access_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#create_ip_access_settings)
        """

    def create_network_settings(
        self, **kwargs: Unpack[CreateNetworkSettingsRequestRequestTypeDef]
    ) -> CreateNetworkSettingsResponseTypeDef:
        """
        Creates a network settings resource that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_network_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#create_network_settings)
        """

    def create_portal(
        self, **kwargs: Unpack[CreatePortalRequestRequestTypeDef]
    ) -> CreatePortalResponseTypeDef:
        """
        Creates a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_portal.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#create_portal)
        """

    def create_trust_store(
        self, **kwargs: Unpack[CreateTrustStoreRequestRequestTypeDef]
    ) -> CreateTrustStoreResponseTypeDef:
        """
        Creates a trust store that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_trust_store.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#create_trust_store)
        """

    def create_user_access_logging_settings(
        self, **kwargs: Unpack[CreateUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> CreateUserAccessLoggingSettingsResponseTypeDef:
        """
        Creates a user access logging settings resource that can be associated with a
        web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_user_access_logging_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#create_user_access_logging_settings)
        """

    def create_user_settings(
        self, **kwargs: Unpack[CreateUserSettingsRequestRequestTypeDef]
    ) -> CreateUserSettingsResponseTypeDef:
        """
        Creates a user settings resource that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_user_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#create_user_settings)
        """

    def delete_browser_settings(
        self, **kwargs: Unpack[DeleteBrowserSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes browser settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_browser_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#delete_browser_settings)
        """

    def delete_data_protection_settings(
        self, **kwargs: Unpack[DeleteDataProtectionSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes data protection settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_data_protection_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#delete_data_protection_settings)
        """

    def delete_identity_provider(
        self, **kwargs: Unpack[DeleteIdentityProviderRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_identity_provider.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#delete_identity_provider)
        """

    def delete_ip_access_settings(
        self, **kwargs: Unpack[DeleteIpAccessSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes IP access settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_ip_access_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#delete_ip_access_settings)
        """

    def delete_network_settings(
        self, **kwargs: Unpack[DeleteNetworkSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes network settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_network_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#delete_network_settings)
        """

    def delete_portal(self, **kwargs: Unpack[DeletePortalRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_portal.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#delete_portal)
        """

    def delete_trust_store(
        self, **kwargs: Unpack[DeleteTrustStoreRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_trust_store.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#delete_trust_store)
        """

    def delete_user_access_logging_settings(
        self, **kwargs: Unpack[DeleteUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes user access logging settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_user_access_logging_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#delete_user_access_logging_settings)
        """

    def delete_user_settings(
        self, **kwargs: Unpack[DeleteUserSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes user settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_user_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#delete_user_settings)
        """

    def disassociate_browser_settings(
        self, **kwargs: Unpack[DisassociateBrowserSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates browser settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_browser_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#disassociate_browser_settings)
        """

    def disassociate_data_protection_settings(
        self, **kwargs: Unpack[DisassociateDataProtectionSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates data protection settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_data_protection_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#disassociate_data_protection_settings)
        """

    def disassociate_ip_access_settings(
        self, **kwargs: Unpack[DisassociateIpAccessSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates IP access settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_ip_access_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#disassociate_ip_access_settings)
        """

    def disassociate_network_settings(
        self, **kwargs: Unpack[DisassociateNetworkSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates network settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_network_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#disassociate_network_settings)
        """

    def disassociate_trust_store(
        self, **kwargs: Unpack[DisassociateTrustStoreRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a trust store from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_trust_store.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#disassociate_trust_store)
        """

    def disassociate_user_access_logging_settings(
        self, **kwargs: Unpack[DisassociateUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates user access logging settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_user_access_logging_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#disassociate_user_access_logging_settings)
        """

    def disassociate_user_settings(
        self, **kwargs: Unpack[DisassociateUserSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates user settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_user_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#disassociate_user_settings)
        """

    def expire_session(
        self, **kwargs: Unpack[ExpireSessionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Expires an active secure browser session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/expire_session.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#expire_session)
        """

    def get_browser_settings(
        self, **kwargs: Unpack[GetBrowserSettingsRequestRequestTypeDef]
    ) -> GetBrowserSettingsResponseTypeDef:
        """
        Gets browser settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_browser_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_browser_settings)
        """

    def get_data_protection_settings(
        self, **kwargs: Unpack[GetDataProtectionSettingsRequestRequestTypeDef]
    ) -> GetDataProtectionSettingsResponseTypeDef:
        """
        Gets the data protection settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_data_protection_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_data_protection_settings)
        """

    def get_identity_provider(
        self, **kwargs: Unpack[GetIdentityProviderRequestRequestTypeDef]
    ) -> GetIdentityProviderResponseTypeDef:
        """
        Gets the identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_identity_provider.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_identity_provider)
        """

    def get_ip_access_settings(
        self, **kwargs: Unpack[GetIpAccessSettingsRequestRequestTypeDef]
    ) -> GetIpAccessSettingsResponseTypeDef:
        """
        Gets the IP access settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_ip_access_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_ip_access_settings)
        """

    def get_network_settings(
        self, **kwargs: Unpack[GetNetworkSettingsRequestRequestTypeDef]
    ) -> GetNetworkSettingsResponseTypeDef:
        """
        Gets the network settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_network_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_network_settings)
        """

    def get_portal(
        self, **kwargs: Unpack[GetPortalRequestRequestTypeDef]
    ) -> GetPortalResponseTypeDef:
        """
        Gets the web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_portal.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_portal)
        """

    def get_portal_service_provider_metadata(
        self, **kwargs: Unpack[GetPortalServiceProviderMetadataRequestRequestTypeDef]
    ) -> GetPortalServiceProviderMetadataResponseTypeDef:
        """
        Gets the service provider metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_portal_service_provider_metadata.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_portal_service_provider_metadata)
        """

    def get_session(
        self, **kwargs: Unpack[GetSessionRequestRequestTypeDef]
    ) -> GetSessionResponseTypeDef:
        """
        Gets information for a secure browser session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_session.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_session)
        """

    def get_trust_store(
        self, **kwargs: Unpack[GetTrustStoreRequestRequestTypeDef]
    ) -> GetTrustStoreResponseTypeDef:
        """
        Gets the trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_trust_store.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_trust_store)
        """

    def get_trust_store_certificate(
        self, **kwargs: Unpack[GetTrustStoreCertificateRequestRequestTypeDef]
    ) -> GetTrustStoreCertificateResponseTypeDef:
        """
        Gets the trust store certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_trust_store_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_trust_store_certificate)
        """

    def get_user_access_logging_settings(
        self, **kwargs: Unpack[GetUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> GetUserAccessLoggingSettingsResponseTypeDef:
        """
        Gets user access logging settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_user_access_logging_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_user_access_logging_settings)
        """

    def get_user_settings(
        self, **kwargs: Unpack[GetUserSettingsRequestRequestTypeDef]
    ) -> GetUserSettingsResponseTypeDef:
        """
        Gets user settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_user_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_user_settings)
        """

    def list_browser_settings(
        self, **kwargs: Unpack[ListBrowserSettingsRequestRequestTypeDef]
    ) -> ListBrowserSettingsResponseTypeDef:
        """
        Retrieves a list of browser settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_browser_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#list_browser_settings)
        """

    def list_data_protection_settings(
        self, **kwargs: Unpack[ListDataProtectionSettingsRequestRequestTypeDef]
    ) -> ListDataProtectionSettingsResponseTypeDef:
        """
        Retrieves a list of data protection settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_data_protection_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#list_data_protection_settings)
        """

    def list_identity_providers(
        self, **kwargs: Unpack[ListIdentityProvidersRequestRequestTypeDef]
    ) -> ListIdentityProvidersResponseTypeDef:
        """
        Retrieves a list of identity providers for a specific web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_identity_providers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#list_identity_providers)
        """

    def list_ip_access_settings(
        self, **kwargs: Unpack[ListIpAccessSettingsRequestRequestTypeDef]
    ) -> ListIpAccessSettingsResponseTypeDef:
        """
        Retrieves a list of IP access settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_ip_access_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#list_ip_access_settings)
        """

    def list_network_settings(
        self, **kwargs: Unpack[ListNetworkSettingsRequestRequestTypeDef]
    ) -> ListNetworkSettingsResponseTypeDef:
        """
        Retrieves a list of network settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_network_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#list_network_settings)
        """

    def list_portals(
        self, **kwargs: Unpack[ListPortalsRequestRequestTypeDef]
    ) -> ListPortalsResponseTypeDef:
        """
        Retrieves a list or web portals.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_portals.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#list_portals)
        """

    def list_sessions(
        self, **kwargs: Unpack[ListSessionsRequestRequestTypeDef]
    ) -> ListSessionsResponseTypeDef:
        """
        Lists information for multiple secure browser sessions from a specific portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_sessions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#list_sessions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves a list of tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#list_tags_for_resource)
        """

    def list_trust_store_certificates(
        self, **kwargs: Unpack[ListTrustStoreCertificatesRequestRequestTypeDef]
    ) -> ListTrustStoreCertificatesResponseTypeDef:
        """
        Retrieves a list of trust store certificates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_trust_store_certificates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#list_trust_store_certificates)
        """

    def list_trust_stores(
        self, **kwargs: Unpack[ListTrustStoresRequestRequestTypeDef]
    ) -> ListTrustStoresResponseTypeDef:
        """
        Retrieves a list of trust stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_trust_stores.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#list_trust_stores)
        """

    def list_user_access_logging_settings(
        self, **kwargs: Unpack[ListUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> ListUserAccessLoggingSettingsResponseTypeDef:
        """
        Retrieves a list of user access logging settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_user_access_logging_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#list_user_access_logging_settings)
        """

    def list_user_settings(
        self, **kwargs: Unpack[ListUserSettingsRequestRequestTypeDef]
    ) -> ListUserSettingsResponseTypeDef:
        """
        Retrieves a list of user settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_user_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#list_user_settings)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds or overwrites one or more tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#untag_resource)
        """

    def update_browser_settings(
        self, **kwargs: Unpack[UpdateBrowserSettingsRequestRequestTypeDef]
    ) -> UpdateBrowserSettingsResponseTypeDef:
        """
        Updates browser settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_browser_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#update_browser_settings)
        """

    def update_data_protection_settings(
        self, **kwargs: Unpack[UpdateDataProtectionSettingsRequestRequestTypeDef]
    ) -> UpdateDataProtectionSettingsResponseTypeDef:
        """
        Updates data protection settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_data_protection_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#update_data_protection_settings)
        """

    def update_identity_provider(
        self, **kwargs: Unpack[UpdateIdentityProviderRequestRequestTypeDef]
    ) -> UpdateIdentityProviderResponseTypeDef:
        """
        Updates the identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_identity_provider.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#update_identity_provider)
        """

    def update_ip_access_settings(
        self, **kwargs: Unpack[UpdateIpAccessSettingsRequestRequestTypeDef]
    ) -> UpdateIpAccessSettingsResponseTypeDef:
        """
        Updates IP access settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_ip_access_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#update_ip_access_settings)
        """

    def update_network_settings(
        self, **kwargs: Unpack[UpdateNetworkSettingsRequestRequestTypeDef]
    ) -> UpdateNetworkSettingsResponseTypeDef:
        """
        Updates network settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_network_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#update_network_settings)
        """

    def update_portal(
        self, **kwargs: Unpack[UpdatePortalRequestRequestTypeDef]
    ) -> UpdatePortalResponseTypeDef:
        """
        Updates a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_portal.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#update_portal)
        """

    def update_trust_store(
        self, **kwargs: Unpack[UpdateTrustStoreRequestRequestTypeDef]
    ) -> UpdateTrustStoreResponseTypeDef:
        """
        Updates the trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_trust_store.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#update_trust_store)
        """

    def update_user_access_logging_settings(
        self, **kwargs: Unpack[UpdateUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> UpdateUserAccessLoggingSettingsResponseTypeDef:
        """
        Updates the user access logging settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_user_access_logging_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#update_user_access_logging_settings)
        """

    def update_user_settings(
        self, **kwargs: Unpack[UpdateUserSettingsRequestRequestTypeDef]
    ) -> UpdateUserSettingsResponseTypeDef:
        """
        Updates the user settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_user_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#update_user_settings)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_protection_settings"]
    ) -> ListDataProtectionSettingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_sessions"]) -> ListSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_web/client/#get_paginator)
        """
