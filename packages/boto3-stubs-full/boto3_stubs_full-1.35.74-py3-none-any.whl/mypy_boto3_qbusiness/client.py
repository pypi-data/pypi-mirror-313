"""
Type annotations for qbusiness service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_qbusiness.client import QBusinessClient

    session = Session()
    client: QBusinessClient = session.client("qbusiness")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetChatControlsConfigurationPaginator,
    ListApplicationsPaginator,
    ListAttachmentsPaginator,
    ListConversationsPaginator,
    ListDataAccessorsPaginator,
    ListDataSourcesPaginator,
    ListDataSourceSyncJobsPaginator,
    ListDocumentsPaginator,
    ListGroupsPaginator,
    ListIndicesPaginator,
    ListMessagesPaginator,
    ListPluginActionsPaginator,
    ListPluginsPaginator,
    ListPluginTypeActionsPaginator,
    ListPluginTypeMetadataPaginator,
    ListRetrieversPaginator,
    ListWebExperiencesPaginator,
    SearchRelevantContentPaginator,
)
from .type_defs import (
    AssociatePermissionRequestRequestTypeDef,
    AssociatePermissionResponseTypeDef,
    BatchDeleteDocumentRequestRequestTypeDef,
    BatchDeleteDocumentResponseTypeDef,
    BatchPutDocumentRequestRequestTypeDef,
    BatchPutDocumentResponseTypeDef,
    ChatInputRequestTypeDef,
    ChatOutputTypeDef,
    ChatSyncInputRequestTypeDef,
    ChatSyncOutputTypeDef,
    CreateApplicationRequestRequestTypeDef,
    CreateApplicationResponseTypeDef,
    CreateDataAccessorRequestRequestTypeDef,
    CreateDataAccessorResponseTypeDef,
    CreateDataSourceRequestRequestTypeDef,
    CreateDataSourceResponseTypeDef,
    CreateIndexRequestRequestTypeDef,
    CreateIndexResponseTypeDef,
    CreatePluginRequestRequestTypeDef,
    CreatePluginResponseTypeDef,
    CreateRetrieverRequestRequestTypeDef,
    CreateRetrieverResponseTypeDef,
    CreateUserRequestRequestTypeDef,
    CreateWebExperienceRequestRequestTypeDef,
    CreateWebExperienceResponseTypeDef,
    DeleteApplicationRequestRequestTypeDef,
    DeleteChatControlsConfigurationRequestRequestTypeDef,
    DeleteConversationRequestRequestTypeDef,
    DeleteDataAccessorRequestRequestTypeDef,
    DeleteDataSourceRequestRequestTypeDef,
    DeleteGroupRequestRequestTypeDef,
    DeleteIndexRequestRequestTypeDef,
    DeletePluginRequestRequestTypeDef,
    DeleteRetrieverRequestRequestTypeDef,
    DeleteUserRequestRequestTypeDef,
    DeleteWebExperienceRequestRequestTypeDef,
    DisassociatePermissionRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetApplicationRequestRequestTypeDef,
    GetApplicationResponseTypeDef,
    GetChatControlsConfigurationRequestRequestTypeDef,
    GetChatControlsConfigurationResponseTypeDef,
    GetDataAccessorRequestRequestTypeDef,
    GetDataAccessorResponseTypeDef,
    GetDataSourceRequestRequestTypeDef,
    GetDataSourceResponseTypeDef,
    GetGroupRequestRequestTypeDef,
    GetGroupResponseTypeDef,
    GetIndexRequestRequestTypeDef,
    GetIndexResponseTypeDef,
    GetMediaRequestRequestTypeDef,
    GetMediaResponseTypeDef,
    GetPluginRequestRequestTypeDef,
    GetPluginResponseTypeDef,
    GetPolicyRequestRequestTypeDef,
    GetPolicyResponseTypeDef,
    GetRetrieverRequestRequestTypeDef,
    GetRetrieverResponseTypeDef,
    GetUserRequestRequestTypeDef,
    GetUserResponseTypeDef,
    GetWebExperienceRequestRequestTypeDef,
    GetWebExperienceResponseTypeDef,
    ListApplicationsRequestRequestTypeDef,
    ListApplicationsResponseTypeDef,
    ListAttachmentsRequestRequestTypeDef,
    ListAttachmentsResponseTypeDef,
    ListConversationsRequestRequestTypeDef,
    ListConversationsResponseTypeDef,
    ListDataAccessorsRequestRequestTypeDef,
    ListDataAccessorsResponseTypeDef,
    ListDataSourcesRequestRequestTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDataSourceSyncJobsRequestRequestTypeDef,
    ListDataSourceSyncJobsResponseTypeDef,
    ListDocumentsRequestRequestTypeDef,
    ListDocumentsResponseTypeDef,
    ListGroupsRequestRequestTypeDef,
    ListGroupsResponseTypeDef,
    ListIndicesRequestRequestTypeDef,
    ListIndicesResponseTypeDef,
    ListMessagesRequestRequestTypeDef,
    ListMessagesResponseTypeDef,
    ListPluginActionsRequestRequestTypeDef,
    ListPluginActionsResponseTypeDef,
    ListPluginsRequestRequestTypeDef,
    ListPluginsResponseTypeDef,
    ListPluginTypeActionsRequestRequestTypeDef,
    ListPluginTypeActionsResponseTypeDef,
    ListPluginTypeMetadataRequestRequestTypeDef,
    ListPluginTypeMetadataResponseTypeDef,
    ListRetrieversRequestRequestTypeDef,
    ListRetrieversResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWebExperiencesRequestRequestTypeDef,
    ListWebExperiencesResponseTypeDef,
    PutFeedbackRequestRequestTypeDef,
    PutGroupRequestRequestTypeDef,
    SearchRelevantContentRequestRequestTypeDef,
    SearchRelevantContentResponseTypeDef,
    StartDataSourceSyncJobRequestRequestTypeDef,
    StartDataSourceSyncJobResponseTypeDef,
    StopDataSourceSyncJobRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateApplicationRequestRequestTypeDef,
    UpdateChatControlsConfigurationRequestRequestTypeDef,
    UpdateDataAccessorRequestRequestTypeDef,
    UpdateDataSourceRequestRequestTypeDef,
    UpdateIndexRequestRequestTypeDef,
    UpdatePluginRequestRequestTypeDef,
    UpdateRetrieverRequestRequestTypeDef,
    UpdateUserRequestRequestTypeDef,
    UpdateUserResponseTypeDef,
    UpdateWebExperienceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("QBusinessClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ExternalResourceException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    LicenseNotFoundException: Type[BotocoreClientError]
    MediaTooLargeException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class QBusinessClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        QBusinessClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#close)
        """

    def associate_permission(
        self, **kwargs: Unpack[AssociatePermissionRequestRequestTypeDef]
    ) -> AssociatePermissionResponseTypeDef:
        """
        Adds or updates a permission policy for a Q Business application, allowing
        cross-account access for an ISV.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/associate_permission.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#associate_permission)
        """

    def batch_delete_document(
        self, **kwargs: Unpack[BatchDeleteDocumentRequestRequestTypeDef]
    ) -> BatchDeleteDocumentResponseTypeDef:
        """
        Asynchronously deletes one or more documents added using the
        <code>BatchPutDocument</code> API from an Amazon Q Business index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/batch_delete_document.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#batch_delete_document)
        """

    def batch_put_document(
        self, **kwargs: Unpack[BatchPutDocumentRequestRequestTypeDef]
    ) -> BatchPutDocumentResponseTypeDef:
        """
        Adds one or more documents to an Amazon Q Business index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/batch_put_document.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#batch_put_document)
        """

    def chat(self, **kwargs: Unpack[ChatInputRequestTypeDef]) -> ChatOutputTypeDef:
        """
        Starts or continues a streaming Amazon Q Business conversation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/chat.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#chat)
        """

    def chat_sync(self, **kwargs: Unpack[ChatSyncInputRequestTypeDef]) -> ChatSyncOutputTypeDef:
        """
        Starts or continues a non-streaming Amazon Q Business conversation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/chat_sync.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#chat_sync)
        """

    def create_application(
        self, **kwargs: Unpack[CreateApplicationRequestRequestTypeDef]
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates an Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/create_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#create_application)
        """

    def create_data_accessor(
        self, **kwargs: Unpack[CreateDataAccessorRequestRequestTypeDef]
    ) -> CreateDataAccessorResponseTypeDef:
        """
        Creates a new data accessor for an ISV to access data from a Q Business
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/create_data_accessor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#create_data_accessor)
        """

    def create_data_source(
        self, **kwargs: Unpack[CreateDataSourceRequestRequestTypeDef]
    ) -> CreateDataSourceResponseTypeDef:
        """
        Creates a data source connector for an Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/create_data_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#create_data_source)
        """

    def create_index(
        self, **kwargs: Unpack[CreateIndexRequestRequestTypeDef]
    ) -> CreateIndexResponseTypeDef:
        """
        Creates an Amazon Q Business index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/create_index.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#create_index)
        """

    def create_plugin(
        self, **kwargs: Unpack[CreatePluginRequestRequestTypeDef]
    ) -> CreatePluginResponseTypeDef:
        """
        Creates an Amazon Q Business plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/create_plugin.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#create_plugin)
        """

    def create_retriever(
        self, **kwargs: Unpack[CreateRetrieverRequestRequestTypeDef]
    ) -> CreateRetrieverResponseTypeDef:
        """
        Adds a retriever to your Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/create_retriever.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#create_retriever)
        """

    def create_user(self, **kwargs: Unpack[CreateUserRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates a universally unique identifier (UUID) mapped to a list of local user
        ids within an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/create_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#create_user)
        """

    def create_web_experience(
        self, **kwargs: Unpack[CreateWebExperienceRequestRequestTypeDef]
    ) -> CreateWebExperienceResponseTypeDef:
        """
        Creates an Amazon Q Business web experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/create_web_experience.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#create_web_experience)
        """

    def delete_application(
        self, **kwargs: Unpack[DeleteApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/delete_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#delete_application)
        """

    def delete_chat_controls_configuration(
        self, **kwargs: Unpack[DeleteChatControlsConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes chat controls configured for an existing Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/delete_chat_controls_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#delete_chat_controls_configuration)
        """

    def delete_conversation(
        self, **kwargs: Unpack[DeleteConversationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Q Business web experience conversation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/delete_conversation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#delete_conversation)
        """

    def delete_data_accessor(
        self, **kwargs: Unpack[DeleteDataAccessorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specified data accessor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/delete_data_accessor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#delete_data_accessor)
        """

    def delete_data_source(
        self, **kwargs: Unpack[DeleteDataSourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Q Business data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/delete_data_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#delete_data_source)
        """

    def delete_group(self, **kwargs: Unpack[DeleteGroupRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a group so that all users and sub groups that belong to the group can
        no longer access documents only available to that group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/delete_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#delete_group)
        """

    def delete_index(self, **kwargs: Unpack[DeleteIndexRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes an Amazon Q Business index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/delete_index.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#delete_index)
        """

    def delete_plugin(self, **kwargs: Unpack[DeletePluginRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes an Amazon Q Business plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/delete_plugin.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#delete_plugin)
        """

    def delete_retriever(
        self, **kwargs: Unpack[DeleteRetrieverRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the retriever used by an Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/delete_retriever.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#delete_retriever)
        """

    def delete_user(self, **kwargs: Unpack[DeleteUserRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a user by email id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/delete_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#delete_user)
        """

    def delete_web_experience(
        self, **kwargs: Unpack[DeleteWebExperienceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Q Business web experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/delete_web_experience.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#delete_web_experience)
        """

    def disassociate_permission(
        self, **kwargs: Unpack[DisassociatePermissionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a permission policy from a Q Business application, revoking the
        cross-account access that was previously granted to an ISV.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/disassociate_permission.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#disassociate_permission)
        """

    def get_application(
        self, **kwargs: Unpack[GetApplicationRequestRequestTypeDef]
    ) -> GetApplicationResponseTypeDef:
        """
        Gets information about an existing Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_application)
        """

    def get_chat_controls_configuration(
        self, **kwargs: Unpack[GetChatControlsConfigurationRequestRequestTypeDef]
    ) -> GetChatControlsConfigurationResponseTypeDef:
        """
        Gets information about an chat controls configured for an existing Amazon Q
        Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_chat_controls_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_chat_controls_configuration)
        """

    def get_data_accessor(
        self, **kwargs: Unpack[GetDataAccessorRequestRequestTypeDef]
    ) -> GetDataAccessorResponseTypeDef:
        """
        Retrieves information about a specified data accessor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_data_accessor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_data_accessor)
        """

    def get_data_source(
        self, **kwargs: Unpack[GetDataSourceRequestRequestTypeDef]
    ) -> GetDataSourceResponseTypeDef:
        """
        Gets information about an existing Amazon Q Business data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_data_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_data_source)
        """

    def get_group(self, **kwargs: Unpack[GetGroupRequestRequestTypeDef]) -> GetGroupResponseTypeDef:
        """
        Describes a group by group name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_group)
        """

    def get_index(self, **kwargs: Unpack[GetIndexRequestRequestTypeDef]) -> GetIndexResponseTypeDef:
        """
        Gets information about an existing Amazon Q Business index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_index.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_index)
        """

    def get_media(self, **kwargs: Unpack[GetMediaRequestRequestTypeDef]) -> GetMediaResponseTypeDef:
        """
        Returns the image bytes corresponding to a media object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_media.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_media)
        """

    def get_plugin(
        self, **kwargs: Unpack[GetPluginRequestRequestTypeDef]
    ) -> GetPluginResponseTypeDef:
        """
        Gets information about an existing Amazon Q Business plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_plugin.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_plugin)
        """

    def get_policy(
        self, **kwargs: Unpack[GetPolicyRequestRequestTypeDef]
    ) -> GetPolicyResponseTypeDef:
        """
        Retrieves the current permission policy for a Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_policy)
        """

    def get_retriever(
        self, **kwargs: Unpack[GetRetrieverRequestRequestTypeDef]
    ) -> GetRetrieverResponseTypeDef:
        """
        Gets information about an existing retriever used by an Amazon Q Business
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_retriever.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_retriever)
        """

    def get_user(self, **kwargs: Unpack[GetUserRequestRequestTypeDef]) -> GetUserResponseTypeDef:
        """
        Describes the universally unique identifier (UUID) associated with a local user
        in a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_user)
        """

    def get_web_experience(
        self, **kwargs: Unpack[GetWebExperienceRequestRequestTypeDef]
    ) -> GetWebExperienceResponseTypeDef:
        """
        Gets information about an existing Amazon Q Business web experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_web_experience.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_web_experience)
        """

    def list_applications(
        self, **kwargs: Unpack[ListApplicationsRequestRequestTypeDef]
    ) -> ListApplicationsResponseTypeDef:
        """
        Lists Amazon Q Business applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_applications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_applications)
        """

    def list_attachments(
        self, **kwargs: Unpack[ListAttachmentsRequestRequestTypeDef]
    ) -> ListAttachmentsResponseTypeDef:
        """
        Gets a list of attachments associated with an Amazon Q Business web experience
        or a list of attachements associated with a specific Amazon Q Business
        conversation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_attachments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_attachments)
        """

    def list_conversations(
        self, **kwargs: Unpack[ListConversationsRequestRequestTypeDef]
    ) -> ListConversationsResponseTypeDef:
        """
        Lists one or more Amazon Q Business conversations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_conversations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_conversations)
        """

    def list_data_accessors(
        self, **kwargs: Unpack[ListDataAccessorsRequestRequestTypeDef]
    ) -> ListDataAccessorsResponseTypeDef:
        """
        Lists the data accessors for a Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_data_accessors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_data_accessors)
        """

    def list_data_source_sync_jobs(
        self, **kwargs: Unpack[ListDataSourceSyncJobsRequestRequestTypeDef]
    ) -> ListDataSourceSyncJobsResponseTypeDef:
        """
        Get information about an Amazon Q Business data source connector
        synchronization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_data_source_sync_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_data_source_sync_jobs)
        """

    def list_data_sources(
        self, **kwargs: Unpack[ListDataSourcesRequestRequestTypeDef]
    ) -> ListDataSourcesResponseTypeDef:
        """
        Lists the Amazon Q Business data source connectors that you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_data_sources.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_data_sources)
        """

    def list_documents(
        self, **kwargs: Unpack[ListDocumentsRequestRequestTypeDef]
    ) -> ListDocumentsResponseTypeDef:
        """
        A list of documents attached to an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_documents.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_documents)
        """

    def list_groups(
        self, **kwargs: Unpack[ListGroupsRequestRequestTypeDef]
    ) -> ListGroupsResponseTypeDef:
        """
        Provides a list of groups that are mapped to users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_groups)
        """

    def list_indices(
        self, **kwargs: Unpack[ListIndicesRequestRequestTypeDef]
    ) -> ListIndicesResponseTypeDef:
        """
        Lists the Amazon Q Business indices you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_indices.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_indices)
        """

    def list_messages(
        self, **kwargs: Unpack[ListMessagesRequestRequestTypeDef]
    ) -> ListMessagesResponseTypeDef:
        """
        Gets a list of messages associated with an Amazon Q Business web experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_messages.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_messages)
        """

    def list_plugin_actions(
        self, **kwargs: Unpack[ListPluginActionsRequestRequestTypeDef]
    ) -> ListPluginActionsResponseTypeDef:
        """
        Lists configured Amazon Q Business actions for a specific plugin in an Amazon Q
        Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_plugin_actions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_plugin_actions)
        """

    def list_plugin_type_actions(
        self, **kwargs: Unpack[ListPluginTypeActionsRequestRequestTypeDef]
    ) -> ListPluginTypeActionsResponseTypeDef:
        """
        Lists configured Amazon Q Business actions for any plugin type—both built-in
        and custom.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_plugin_type_actions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_plugin_type_actions)
        """

    def list_plugin_type_metadata(
        self, **kwargs: Unpack[ListPluginTypeMetadataRequestRequestTypeDef]
    ) -> ListPluginTypeMetadataResponseTypeDef:
        """
        Lists metadata for all Amazon Q Business plugin types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_plugin_type_metadata.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_plugin_type_metadata)
        """

    def list_plugins(
        self, **kwargs: Unpack[ListPluginsRequestRequestTypeDef]
    ) -> ListPluginsResponseTypeDef:
        """
        Lists configured Amazon Q Business plugins.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_plugins.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_plugins)
        """

    def list_retrievers(
        self, **kwargs: Unpack[ListRetrieversRequestRequestTypeDef]
    ) -> ListRetrieversResponseTypeDef:
        """
        Lists the retriever used by an Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_retrievers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_retrievers)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets a list of tags associated with a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_tags_for_resource)
        """

    def list_web_experiences(
        self, **kwargs: Unpack[ListWebExperiencesRequestRequestTypeDef]
    ) -> ListWebExperiencesResponseTypeDef:
        """
        Lists one or more Amazon Q Business Web Experiences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/list_web_experiences.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#list_web_experiences)
        """

    def put_feedback(
        self, **kwargs: Unpack[PutFeedbackRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables your end user to provide feedback on their Amazon Q Business generated
        chat responses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/put_feedback.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#put_feedback)
        """

    def put_group(self, **kwargs: Unpack[PutGroupRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Create, or updates, a mapping of users—who have access to a document—to groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/put_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#put_group)
        """

    def search_relevant_content(
        self, **kwargs: Unpack[SearchRelevantContentRequestRequestTypeDef]
    ) -> SearchRelevantContentResponseTypeDef:
        """
        Searches for relevant content in a Q Business application based on a query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/search_relevant_content.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#search_relevant_content)
        """

    def start_data_source_sync_job(
        self, **kwargs: Unpack[StartDataSourceSyncJobRequestRequestTypeDef]
    ) -> StartDataSourceSyncJobResponseTypeDef:
        """
        Starts a data source connector synchronization job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/start_data_source_sync_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#start_data_source_sync_job)
        """

    def stop_data_source_sync_job(
        self, **kwargs: Unpack[StopDataSourceSyncJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an Amazon Q Business data source connector synchronization job already in
        progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/stop_data_source_sync_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#stop_data_source_sync_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tag to the specified Amazon Q Business application or data
        source resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag from an Amazon Q Business application or a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#untag_resource)
        """

    def update_application(
        self, **kwargs: Unpack[UpdateApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an existing Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/update_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#update_application)
        """

    def update_chat_controls_configuration(
        self, **kwargs: Unpack[UpdateChatControlsConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an set of chat controls configured for an existing Amazon Q Business
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/update_chat_controls_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#update_chat_controls_configuration)
        """

    def update_data_accessor(
        self, **kwargs: Unpack[UpdateDataAccessorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an existing data accessor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/update_data_accessor.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#update_data_accessor)
        """

    def update_data_source(
        self, **kwargs: Unpack[UpdateDataSourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an existing Amazon Q Business data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/update_data_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#update_data_source)
        """

    def update_index(self, **kwargs: Unpack[UpdateIndexRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates an Amazon Q Business index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/update_index.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#update_index)
        """

    def update_plugin(self, **kwargs: Unpack[UpdatePluginRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates an Amazon Q Business plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/update_plugin.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#update_plugin)
        """

    def update_retriever(
        self, **kwargs: Unpack[UpdateRetrieverRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the retriever used for your Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/update_retriever.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#update_retriever)
        """

    def update_user(
        self, **kwargs: Unpack[UpdateUserRequestRequestTypeDef]
    ) -> UpdateUserResponseTypeDef:
        """
        Updates a information associated with a user id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/update_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#update_user)
        """

    def update_web_experience(
        self, **kwargs: Unpack[UpdateWebExperienceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an Amazon Q Business web experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/update_web_experience.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#update_web_experience)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_chat_controls_configuration"]
    ) -> GetChatControlsConfigurationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_attachments"]
    ) -> ListAttachmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_conversations"]
    ) -> ListConversationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_accessors"]
    ) -> ListDataAccessorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_source_sync_jobs"]
    ) -> ListDataSourceSyncJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_sources"]
    ) -> ListDataSourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_documents"]) -> ListDocumentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_indices"]) -> ListIndicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_messages"]) -> ListMessagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_plugin_actions"]
    ) -> ListPluginActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_plugin_type_actions"]
    ) -> ListPluginTypeActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_plugin_type_metadata"]
    ) -> ListPluginTypeMetadataPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_plugins"]) -> ListPluginsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_retrievers"]) -> ListRetrieversPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_web_experiences"]
    ) -> ListWebExperiencesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_relevant_content"]
    ) -> SearchRelevantContentPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/client/#get_paginator)
        """
