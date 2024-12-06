"""
Type annotations for qbusiness service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_qbusiness.client import QBusinessClient
    from mypy_boto3_qbusiness.paginator import (
        GetChatControlsConfigurationPaginator,
        ListApplicationsPaginator,
        ListAttachmentsPaginator,
        ListConversationsPaginator,
        ListDataAccessorsPaginator,
        ListDataSourceSyncJobsPaginator,
        ListDataSourcesPaginator,
        ListDocumentsPaginator,
        ListGroupsPaginator,
        ListIndicesPaginator,
        ListMessagesPaginator,
        ListPluginActionsPaginator,
        ListPluginTypeActionsPaginator,
        ListPluginTypeMetadataPaginator,
        ListPluginsPaginator,
        ListRetrieversPaginator,
        ListWebExperiencesPaginator,
        SearchRelevantContentPaginator,
    )

    session = Session()
    client: QBusinessClient = session.client("qbusiness")

    get_chat_controls_configuration_paginator: GetChatControlsConfigurationPaginator = client.get_paginator("get_chat_controls_configuration")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_attachments_paginator: ListAttachmentsPaginator = client.get_paginator("list_attachments")
    list_conversations_paginator: ListConversationsPaginator = client.get_paginator("list_conversations")
    list_data_accessors_paginator: ListDataAccessorsPaginator = client.get_paginator("list_data_accessors")
    list_data_source_sync_jobs_paginator: ListDataSourceSyncJobsPaginator = client.get_paginator("list_data_source_sync_jobs")
    list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
    list_documents_paginator: ListDocumentsPaginator = client.get_paginator("list_documents")
    list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
    list_indices_paginator: ListIndicesPaginator = client.get_paginator("list_indices")
    list_messages_paginator: ListMessagesPaginator = client.get_paginator("list_messages")
    list_plugin_actions_paginator: ListPluginActionsPaginator = client.get_paginator("list_plugin_actions")
    list_plugin_type_actions_paginator: ListPluginTypeActionsPaginator = client.get_paginator("list_plugin_type_actions")
    list_plugin_type_metadata_paginator: ListPluginTypeMetadataPaginator = client.get_paginator("list_plugin_type_metadata")
    list_plugins_paginator: ListPluginsPaginator = client.get_paginator("list_plugins")
    list_retrievers_paginator: ListRetrieversPaginator = client.get_paginator("list_retrievers")
    list_web_experiences_paginator: ListWebExperiencesPaginator = client.get_paginator("list_web_experiences")
    search_relevant_content_paginator: SearchRelevantContentPaginator = client.get_paginator("search_relevant_content")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetChatControlsConfigurationRequestGetChatControlsConfigurationPaginateTypeDef,
    GetChatControlsConfigurationResponseTypeDef,
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListAttachmentsRequestListAttachmentsPaginateTypeDef,
    ListAttachmentsResponseTypeDef,
    ListConversationsRequestListConversationsPaginateTypeDef,
    ListConversationsResponseTypeDef,
    ListDataAccessorsRequestListDataAccessorsPaginateTypeDef,
    ListDataAccessorsResponseTypeDef,
    ListDataSourcesRequestListDataSourcesPaginateTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDataSourceSyncJobsRequestListDataSourceSyncJobsPaginateTypeDef,
    ListDataSourceSyncJobsResponseTypeDef,
    ListDocumentsRequestListDocumentsPaginateTypeDef,
    ListDocumentsResponseTypeDef,
    ListGroupsRequestListGroupsPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListIndicesRequestListIndicesPaginateTypeDef,
    ListIndicesResponseTypeDef,
    ListMessagesRequestListMessagesPaginateTypeDef,
    ListMessagesResponseTypeDef,
    ListPluginActionsRequestListPluginActionsPaginateTypeDef,
    ListPluginActionsResponseTypeDef,
    ListPluginsRequestListPluginsPaginateTypeDef,
    ListPluginsResponseTypeDef,
    ListPluginTypeActionsRequestListPluginTypeActionsPaginateTypeDef,
    ListPluginTypeActionsResponseTypeDef,
    ListPluginTypeMetadataRequestListPluginTypeMetadataPaginateTypeDef,
    ListPluginTypeMetadataResponseTypeDef,
    ListRetrieversRequestListRetrieversPaginateTypeDef,
    ListRetrieversResponseTypeDef,
    ListWebExperiencesRequestListWebExperiencesPaginateTypeDef,
    ListWebExperiencesResponseTypeDef,
    SearchRelevantContentRequestSearchRelevantContentPaginateTypeDef,
    SearchRelevantContentResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetChatControlsConfigurationPaginator",
    "ListApplicationsPaginator",
    "ListAttachmentsPaginator",
    "ListConversationsPaginator",
    "ListDataAccessorsPaginator",
    "ListDataSourceSyncJobsPaginator",
    "ListDataSourcesPaginator",
    "ListDocumentsPaginator",
    "ListGroupsPaginator",
    "ListIndicesPaginator",
    "ListMessagesPaginator",
    "ListPluginActionsPaginator",
    "ListPluginTypeActionsPaginator",
    "ListPluginTypeMetadataPaginator",
    "ListPluginsPaginator",
    "ListRetrieversPaginator",
    "ListWebExperiencesPaginator",
    "SearchRelevantContentPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetChatControlsConfigurationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/GetChatControlsConfiguration.html#QBusiness.Paginator.GetChatControlsConfiguration)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#getchatcontrolsconfigurationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetChatControlsConfigurationRequestGetChatControlsConfigurationPaginateTypeDef
        ],
    ) -> _PageIterator[GetChatControlsConfigurationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/GetChatControlsConfiguration.html#QBusiness.Paginator.GetChatControlsConfiguration.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#getchatcontrolsconfigurationpaginator)
        """

class ListApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListApplications.html#QBusiness.Paginator.ListApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listapplicationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> _PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListApplications.html#QBusiness.Paginator.ListApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listapplicationspaginator)
        """

class ListAttachmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListAttachments.html#QBusiness.Paginator.ListAttachments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listattachmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAttachmentsRequestListAttachmentsPaginateTypeDef]
    ) -> _PageIterator[ListAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListAttachments.html#QBusiness.Paginator.ListAttachments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listattachmentspaginator)
        """

class ListConversationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListConversations.html#QBusiness.Paginator.ListConversations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listconversationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListConversationsRequestListConversationsPaginateTypeDef]
    ) -> _PageIterator[ListConversationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListConversations.html#QBusiness.Paginator.ListConversations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listconversationspaginator)
        """

class ListDataAccessorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataAccessors.html#QBusiness.Paginator.ListDataAccessors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listdataaccessorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataAccessorsRequestListDataAccessorsPaginateTypeDef]
    ) -> _PageIterator[ListDataAccessorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataAccessors.html#QBusiness.Paginator.ListDataAccessors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listdataaccessorspaginator)
        """

class ListDataSourceSyncJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataSourceSyncJobs.html#QBusiness.Paginator.ListDataSourceSyncJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listdatasourcesyncjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataSourceSyncJobsRequestListDataSourceSyncJobsPaginateTypeDef]
    ) -> _PageIterator[ListDataSourceSyncJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataSourceSyncJobs.html#QBusiness.Paginator.ListDataSourceSyncJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listdatasourcesyncjobspaginator)
        """

class ListDataSourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataSources.html#QBusiness.Paginator.ListDataSources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listdatasourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataSourcesRequestListDataSourcesPaginateTypeDef]
    ) -> _PageIterator[ListDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataSources.html#QBusiness.Paginator.ListDataSources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listdatasourcespaginator)
        """

class ListDocumentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDocuments.html#QBusiness.Paginator.ListDocuments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listdocumentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDocumentsRequestListDocumentsPaginateTypeDef]
    ) -> _PageIterator[ListDocumentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDocuments.html#QBusiness.Paginator.ListDocuments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listdocumentspaginator)
        """

class ListGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListGroups.html#QBusiness.Paginator.ListGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupsRequestListGroupsPaginateTypeDef]
    ) -> _PageIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListGroups.html#QBusiness.Paginator.ListGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listgroupspaginator)
        """

class ListIndicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListIndices.html#QBusiness.Paginator.ListIndices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listindicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIndicesRequestListIndicesPaginateTypeDef]
    ) -> _PageIterator[ListIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListIndices.html#QBusiness.Paginator.ListIndices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listindicespaginator)
        """

class ListMessagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListMessages.html#QBusiness.Paginator.ListMessages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listmessagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMessagesRequestListMessagesPaginateTypeDef]
    ) -> _PageIterator[ListMessagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListMessages.html#QBusiness.Paginator.ListMessages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listmessagespaginator)
        """

class ListPluginActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginActions.html#QBusiness.Paginator.ListPluginActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listpluginactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPluginActionsRequestListPluginActionsPaginateTypeDef]
    ) -> _PageIterator[ListPluginActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginActions.html#QBusiness.Paginator.ListPluginActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listpluginactionspaginator)
        """

class ListPluginTypeActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginTypeActions.html#QBusiness.Paginator.ListPluginTypeActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listplugintypeactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPluginTypeActionsRequestListPluginTypeActionsPaginateTypeDef]
    ) -> _PageIterator[ListPluginTypeActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginTypeActions.html#QBusiness.Paginator.ListPluginTypeActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listplugintypeactionspaginator)
        """

class ListPluginTypeMetadataPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginTypeMetadata.html#QBusiness.Paginator.ListPluginTypeMetadata)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listplugintypemetadatapaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPluginTypeMetadataRequestListPluginTypeMetadataPaginateTypeDef]
    ) -> _PageIterator[ListPluginTypeMetadataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginTypeMetadata.html#QBusiness.Paginator.ListPluginTypeMetadata.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listplugintypemetadatapaginator)
        """

class ListPluginsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPlugins.html#QBusiness.Paginator.ListPlugins)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listpluginspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPluginsRequestListPluginsPaginateTypeDef]
    ) -> _PageIterator[ListPluginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPlugins.html#QBusiness.Paginator.ListPlugins.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listpluginspaginator)
        """

class ListRetrieversPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListRetrievers.html#QBusiness.Paginator.ListRetrievers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listretrieverspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRetrieversRequestListRetrieversPaginateTypeDef]
    ) -> _PageIterator[ListRetrieversResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListRetrievers.html#QBusiness.Paginator.ListRetrievers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listretrieverspaginator)
        """

class ListWebExperiencesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListWebExperiences.html#QBusiness.Paginator.ListWebExperiences)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listwebexperiencespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWebExperiencesRequestListWebExperiencesPaginateTypeDef]
    ) -> _PageIterator[ListWebExperiencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListWebExperiences.html#QBusiness.Paginator.ListWebExperiences.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#listwebexperiencespaginator)
        """

class SearchRelevantContentPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/SearchRelevantContent.html#QBusiness.Paginator.SearchRelevantContent)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#searchrelevantcontentpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchRelevantContentRequestSearchRelevantContentPaginateTypeDef]
    ) -> _PageIterator[SearchRelevantContentResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/SearchRelevantContent.html#QBusiness.Paginator.SearchRelevantContent.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/paginators/#searchrelevantcontentpaginator)
        """
