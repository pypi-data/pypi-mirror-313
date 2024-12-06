"""
Type annotations for appfabric service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_appfabric.client import AppFabricClient

    session = Session()
    client: AppFabricClient = session.client("appfabric")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAppAuthorizationsPaginator,
    ListAppBundlesPaginator,
    ListIngestionDestinationsPaginator,
    ListIngestionsPaginator,
)
from .type_defs import (
    BatchGetUserAccessTasksRequestRequestTypeDef,
    BatchGetUserAccessTasksResponseTypeDef,
    ConnectAppAuthorizationRequestRequestTypeDef,
    ConnectAppAuthorizationResponseTypeDef,
    CreateAppAuthorizationRequestRequestTypeDef,
    CreateAppAuthorizationResponseTypeDef,
    CreateAppBundleRequestRequestTypeDef,
    CreateAppBundleResponseTypeDef,
    CreateIngestionDestinationRequestRequestTypeDef,
    CreateIngestionDestinationResponseTypeDef,
    CreateIngestionRequestRequestTypeDef,
    CreateIngestionResponseTypeDef,
    DeleteAppAuthorizationRequestRequestTypeDef,
    DeleteAppBundleRequestRequestTypeDef,
    DeleteIngestionDestinationRequestRequestTypeDef,
    DeleteIngestionRequestRequestTypeDef,
    GetAppAuthorizationRequestRequestTypeDef,
    GetAppAuthorizationResponseTypeDef,
    GetAppBundleRequestRequestTypeDef,
    GetAppBundleResponseTypeDef,
    GetIngestionDestinationRequestRequestTypeDef,
    GetIngestionDestinationResponseTypeDef,
    GetIngestionRequestRequestTypeDef,
    GetIngestionResponseTypeDef,
    ListAppAuthorizationsRequestRequestTypeDef,
    ListAppAuthorizationsResponseTypeDef,
    ListAppBundlesRequestRequestTypeDef,
    ListAppBundlesResponseTypeDef,
    ListIngestionDestinationsRequestRequestTypeDef,
    ListIngestionDestinationsResponseTypeDef,
    ListIngestionsRequestRequestTypeDef,
    ListIngestionsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartIngestionRequestRequestTypeDef,
    StartUserAccessTasksRequestRequestTypeDef,
    StartUserAccessTasksResponseTypeDef,
    StopIngestionRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAppAuthorizationRequestRequestTypeDef,
    UpdateAppAuthorizationResponseTypeDef,
    UpdateIngestionDestinationRequestRequestTypeDef,
    UpdateIngestionDestinationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("AppFabricClient",)

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

class AppFabricClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppFabricClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#close)
        """

    def batch_get_user_access_tasks(
        self, **kwargs: Unpack[BatchGetUserAccessTasksRequestRequestTypeDef]
    ) -> BatchGetUserAccessTasksResponseTypeDef:
        """
        Gets user access details in a batch request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/batch_get_user_access_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#batch_get_user_access_tasks)
        """

    def connect_app_authorization(
        self, **kwargs: Unpack[ConnectAppAuthorizationRequestRequestTypeDef]
    ) -> ConnectAppAuthorizationResponseTypeDef:
        """
        Establishes a connection between Amazon Web Services AppFabric and an
        application, which allows AppFabric to call the APIs of the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/connect_app_authorization.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#connect_app_authorization)
        """

    def create_app_authorization(
        self, **kwargs: Unpack[CreateAppAuthorizationRequestRequestTypeDef]
    ) -> CreateAppAuthorizationResponseTypeDef:
        """
        Creates an app authorization within an app bundle, which allows AppFabric to
        connect to an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/create_app_authorization.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#create_app_authorization)
        """

    def create_app_bundle(
        self, **kwargs: Unpack[CreateAppBundleRequestRequestTypeDef]
    ) -> CreateAppBundleResponseTypeDef:
        """
        Creates an app bundle to collect data from an application using AppFabric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/create_app_bundle.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#create_app_bundle)
        """

    def create_ingestion(
        self, **kwargs: Unpack[CreateIngestionRequestRequestTypeDef]
    ) -> CreateIngestionResponseTypeDef:
        """
        Creates a data ingestion for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/create_ingestion.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#create_ingestion)
        """

    def create_ingestion_destination(
        self, **kwargs: Unpack[CreateIngestionDestinationRequestRequestTypeDef]
    ) -> CreateIngestionDestinationResponseTypeDef:
        """
        Creates an ingestion destination, which specifies how an application's ingested
        data is processed by Amazon Web Services AppFabric and where it's delivered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/create_ingestion_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#create_ingestion_destination)
        """

    def delete_app_authorization(
        self, **kwargs: Unpack[DeleteAppAuthorizationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an app authorization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/delete_app_authorization.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#delete_app_authorization)
        """

    def delete_app_bundle(
        self, **kwargs: Unpack[DeleteAppBundleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an app bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/delete_app_bundle.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#delete_app_bundle)
        """

    def delete_ingestion(
        self, **kwargs: Unpack[DeleteIngestionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an ingestion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/delete_ingestion.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#delete_ingestion)
        """

    def delete_ingestion_destination(
        self, **kwargs: Unpack[DeleteIngestionDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an ingestion destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/delete_ingestion_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#delete_ingestion_destination)
        """

    def get_app_authorization(
        self, **kwargs: Unpack[GetAppAuthorizationRequestRequestTypeDef]
    ) -> GetAppAuthorizationResponseTypeDef:
        """
        Returns information about an app authorization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_app_authorization.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#get_app_authorization)
        """

    def get_app_bundle(
        self, **kwargs: Unpack[GetAppBundleRequestRequestTypeDef]
    ) -> GetAppBundleResponseTypeDef:
        """
        Returns information about an app bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_app_bundle.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#get_app_bundle)
        """

    def get_ingestion(
        self, **kwargs: Unpack[GetIngestionRequestRequestTypeDef]
    ) -> GetIngestionResponseTypeDef:
        """
        Returns information about an ingestion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_ingestion.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#get_ingestion)
        """

    def get_ingestion_destination(
        self, **kwargs: Unpack[GetIngestionDestinationRequestRequestTypeDef]
    ) -> GetIngestionDestinationResponseTypeDef:
        """
        Returns information about an ingestion destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_ingestion_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#get_ingestion_destination)
        """

    def list_app_authorizations(
        self, **kwargs: Unpack[ListAppAuthorizationsRequestRequestTypeDef]
    ) -> ListAppAuthorizationsResponseTypeDef:
        """
        Returns a list of all app authorizations configured for an app bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/list_app_authorizations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#list_app_authorizations)
        """

    def list_app_bundles(
        self, **kwargs: Unpack[ListAppBundlesRequestRequestTypeDef]
    ) -> ListAppBundlesResponseTypeDef:
        """
        Returns a list of app bundles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/list_app_bundles.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#list_app_bundles)
        """

    def list_ingestion_destinations(
        self, **kwargs: Unpack[ListIngestionDestinationsRequestRequestTypeDef]
    ) -> ListIngestionDestinationsResponseTypeDef:
        """
        Returns a list of all ingestion destinations configured for an ingestion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/list_ingestion_destinations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#list_ingestion_destinations)
        """

    def list_ingestions(
        self, **kwargs: Unpack[ListIngestionsRequestRequestTypeDef]
    ) -> ListIngestionsResponseTypeDef:
        """
        Returns a list of all ingestions configured for an app bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/list_ingestions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#list_ingestions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#list_tags_for_resource)
        """

    def start_ingestion(
        self, **kwargs: Unpack[StartIngestionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts (enables) an ingestion, which collects data from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/start_ingestion.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#start_ingestion)
        """

    def start_user_access_tasks(
        self, **kwargs: Unpack[StartUserAccessTasksRequestRequestTypeDef]
    ) -> StartUserAccessTasksResponseTypeDef:
        """
        Starts the tasks to search user access status for a specific email address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/start_user_access_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#start_user_access_tasks)
        """

    def stop_ingestion(
        self, **kwargs: Unpack[StopIngestionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops (disables) an ingestion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/stop_ingestion.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#stop_ingestion)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag or tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#untag_resource)
        """

    def update_app_authorization(
        self, **kwargs: Unpack[UpdateAppAuthorizationRequestRequestTypeDef]
    ) -> UpdateAppAuthorizationResponseTypeDef:
        """
        Updates an app authorization within an app bundle, which allows AppFabric to
        connect to an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/update_app_authorization.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#update_app_authorization)
        """

    def update_ingestion_destination(
        self, **kwargs: Unpack[UpdateIngestionDestinationRequestRequestTypeDef]
    ) -> UpdateIngestionDestinationResponseTypeDef:
        """
        Updates an ingestion destination, which specifies how an application's ingested
        data is processed by Amazon Web Services AppFabric and where it's delivered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/update_ingestion_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#update_ingestion_destination)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_app_authorizations"]
    ) -> ListAppAuthorizationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_app_bundles"]) -> ListAppBundlesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ingestion_destinations"]
    ) -> ListIngestionDestinationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_ingestions"]) -> ListIngestionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/client/#get_paginator)
        """
