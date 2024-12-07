"""
Type annotations for pca-connector-ad service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_pca_connector_ad.client import PcaConnectorAdClient

    session = Session()
    client: PcaConnectorAdClient = session.client("pca-connector-ad")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListConnectorsPaginator,
    ListDirectoryRegistrationsPaginator,
    ListServicePrincipalNamesPaginator,
    ListTemplateGroupAccessControlEntriesPaginator,
    ListTemplatesPaginator,
)
from .type_defs import (
    CreateConnectorRequestRequestTypeDef,
    CreateConnectorResponseTypeDef,
    CreateDirectoryRegistrationRequestRequestTypeDef,
    CreateDirectoryRegistrationResponseTypeDef,
    CreateServicePrincipalNameRequestRequestTypeDef,
    CreateTemplateGroupAccessControlEntryRequestRequestTypeDef,
    CreateTemplateRequestRequestTypeDef,
    CreateTemplateResponseTypeDef,
    DeleteConnectorRequestRequestTypeDef,
    DeleteDirectoryRegistrationRequestRequestTypeDef,
    DeleteServicePrincipalNameRequestRequestTypeDef,
    DeleteTemplateGroupAccessControlEntryRequestRequestTypeDef,
    DeleteTemplateRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetConnectorRequestRequestTypeDef,
    GetConnectorResponseTypeDef,
    GetDirectoryRegistrationRequestRequestTypeDef,
    GetDirectoryRegistrationResponseTypeDef,
    GetServicePrincipalNameRequestRequestTypeDef,
    GetServicePrincipalNameResponseTypeDef,
    GetTemplateGroupAccessControlEntryRequestRequestTypeDef,
    GetTemplateGroupAccessControlEntryResponseTypeDef,
    GetTemplateRequestRequestTypeDef,
    GetTemplateResponseTypeDef,
    ListConnectorsRequestRequestTypeDef,
    ListConnectorsResponseTypeDef,
    ListDirectoryRegistrationsRequestRequestTypeDef,
    ListDirectoryRegistrationsResponseTypeDef,
    ListServicePrincipalNamesRequestRequestTypeDef,
    ListServicePrincipalNamesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTemplateGroupAccessControlEntriesRequestRequestTypeDef,
    ListTemplateGroupAccessControlEntriesResponseTypeDef,
    ListTemplatesRequestRequestTypeDef,
    ListTemplatesResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateTemplateGroupAccessControlEntryRequestRequestTypeDef,
    UpdateTemplateRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("PcaConnectorAdClient",)

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

class PcaConnectorAdClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad.html#PcaConnectorAd.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PcaConnectorAdClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad.html#PcaConnectorAd.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#close)
        """

    def create_connector(
        self, **kwargs: Unpack[CreateConnectorRequestRequestTypeDef]
    ) -> CreateConnectorResponseTypeDef:
        """
        Creates a connector between Amazon Web Services Private CA and an Active
        Directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/create_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#create_connector)
        """

    def create_directory_registration(
        self, **kwargs: Unpack[CreateDirectoryRegistrationRequestRequestTypeDef]
    ) -> CreateDirectoryRegistrationResponseTypeDef:
        """
        Creates a directory registration that authorizes communication between Amazon
        Web Services Private CA and an Active Directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/create_directory_registration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#create_directory_registration)
        """

    def create_service_principal_name(
        self, **kwargs: Unpack[CreateServicePrincipalNameRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a service principal name (SPN) for the service account in Active
        Directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/create_service_principal_name.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#create_service_principal_name)
        """

    def create_template(
        self, **kwargs: Unpack[CreateTemplateRequestRequestTypeDef]
    ) -> CreateTemplateResponseTypeDef:
        """
        Creates an Active Directory compatible certificate template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/create_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#create_template)
        """

    def create_template_group_access_control_entry(
        self, **kwargs: Unpack[CreateTemplateGroupAccessControlEntryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Create a group access control entry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/create_template_group_access_control_entry.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#create_template_group_access_control_entry)
        """

    def delete_connector(
        self, **kwargs: Unpack[DeleteConnectorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a connector for Active Directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/delete_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#delete_connector)
        """

    def delete_directory_registration(
        self, **kwargs: Unpack[DeleteDirectoryRegistrationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a directory registration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/delete_directory_registration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#delete_directory_registration)
        """

    def delete_service_principal_name(
        self, **kwargs: Unpack[DeleteServicePrincipalNameRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the service principal name (SPN) used by a connector to authenticate
        with your Active Directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/delete_service_principal_name.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#delete_service_principal_name)
        """

    def delete_template(
        self, **kwargs: Unpack[DeleteTemplateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/delete_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#delete_template)
        """

    def delete_template_group_access_control_entry(
        self, **kwargs: Unpack[DeleteTemplateGroupAccessControlEntryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a group access control entry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/delete_template_group_access_control_entry.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#delete_template_group_access_control_entry)
        """

    def get_connector(
        self, **kwargs: Unpack[GetConnectorRequestRequestTypeDef]
    ) -> GetConnectorResponseTypeDef:
        """
        Lists information about your connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/get_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#get_connector)
        """

    def get_directory_registration(
        self, **kwargs: Unpack[GetDirectoryRegistrationRequestRequestTypeDef]
    ) -> GetDirectoryRegistrationResponseTypeDef:
        """
        A structure that contains information about your directory registration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/get_directory_registration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#get_directory_registration)
        """

    def get_service_principal_name(
        self, **kwargs: Unpack[GetServicePrincipalNameRequestRequestTypeDef]
    ) -> GetServicePrincipalNameResponseTypeDef:
        """
        Lists the service principal name that the connector uses to authenticate with
        Active Directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/get_service_principal_name.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#get_service_principal_name)
        """

    def get_template(
        self, **kwargs: Unpack[GetTemplateRequestRequestTypeDef]
    ) -> GetTemplateResponseTypeDef:
        """
        Retrieves a certificate template that the connector uses to issue certificates
        from a private CA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/get_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#get_template)
        """

    def get_template_group_access_control_entry(
        self, **kwargs: Unpack[GetTemplateGroupAccessControlEntryRequestRequestTypeDef]
    ) -> GetTemplateGroupAccessControlEntryResponseTypeDef:
        """
        Retrieves the group access control entries for a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/get_template_group_access_control_entry.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#get_template_group_access_control_entry)
        """

    def list_connectors(
        self, **kwargs: Unpack[ListConnectorsRequestRequestTypeDef]
    ) -> ListConnectorsResponseTypeDef:
        """
        Lists the connectors that you created by using the <a
        href="https://docs.aws.amazon.com/pca-connector-ad/latest/APIReference/API_CreateConnector">https://docs.aws.amazon.com/pca-connector-ad/latest/APIReference/API_CreateConnector</a>
        action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/list_connectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#list_connectors)
        """

    def list_directory_registrations(
        self, **kwargs: Unpack[ListDirectoryRegistrationsRequestRequestTypeDef]
    ) -> ListDirectoryRegistrationsResponseTypeDef:
        """
        Lists the directory registrations that you created by using the <a
        href="https://docs.aws.amazon.com/pca-connector-ad/latest/APIReference/API_CreateDirectoryRegistration">https://docs.aws.amazon.com/pca-connector-ad/latest/APIReference/API_CreateDirectoryRegistration</a>
        action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/list_directory_registrations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#list_directory_registrations)
        """

    def list_service_principal_names(
        self, **kwargs: Unpack[ListServicePrincipalNamesRequestRequestTypeDef]
    ) -> ListServicePrincipalNamesResponseTypeDef:
        """
        Lists the service principal names that the connector uses to authenticate with
        Active Directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/list_service_principal_names.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#list_service_principal_names)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags, if any, that are associated with your resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#list_tags_for_resource)
        """

    def list_template_group_access_control_entries(
        self, **kwargs: Unpack[ListTemplateGroupAccessControlEntriesRequestRequestTypeDef]
    ) -> ListTemplateGroupAccessControlEntriesResponseTypeDef:
        """
        Lists group access control entries you created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/list_template_group_access_control_entries.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#list_template_group_access_control_entries)
        """

    def list_templates(
        self, **kwargs: Unpack[ListTemplatesRequestRequestTypeDef]
    ) -> ListTemplatesResponseTypeDef:
        """
        Lists the templates, if any, that are associated with a connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/list_templates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#list_templates)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to your resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes one or more tags from your resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#untag_resource)
        """

    def update_template(
        self, **kwargs: Unpack[UpdateTemplateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update template configuration to define the information included in
        certificates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/update_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#update_template)
        """

    def update_template_group_access_control_entry(
        self, **kwargs: Unpack[UpdateTemplateGroupAccessControlEntryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update a group access control entry you created using <a
        href="https://docs.aws.amazon.com/pca-connector-ad/latest/APIReference/API_CreateTemplateGroupAccessControlEntry.html">CreateTemplateGroupAccessControlEntry</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/update_template_group_access_control_entry.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#update_template_group_access_control_entry)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_connectors"]) -> ListConnectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_directory_registrations"]
    ) -> ListDirectoryRegistrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_principal_names"]
    ) -> ListServicePrincipalNamesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_template_group_access_control_entries"]
    ) -> ListTemplateGroupAccessControlEntriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_templates"]) -> ListTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_ad/client/#get_paginator)
        """
