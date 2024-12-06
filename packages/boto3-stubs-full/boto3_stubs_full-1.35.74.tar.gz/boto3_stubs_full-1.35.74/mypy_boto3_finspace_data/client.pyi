"""
Type annotations for finspace-data service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_finspace_data.client import FinSpaceDataClient

    session = Session()
    client: FinSpaceDataClient = session.client("finspace-data")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListChangesetsPaginator,
    ListDatasetsPaginator,
    ListDataViewsPaginator,
    ListPermissionGroupsPaginator,
    ListUsersPaginator,
)
from .type_defs import (
    AssociateUserToPermissionGroupRequestRequestTypeDef,
    AssociateUserToPermissionGroupResponseTypeDef,
    CreateChangesetRequestRequestTypeDef,
    CreateChangesetResponseTypeDef,
    CreateDatasetRequestRequestTypeDef,
    CreateDatasetResponseTypeDef,
    CreateDataViewRequestRequestTypeDef,
    CreateDataViewResponseTypeDef,
    CreatePermissionGroupRequestRequestTypeDef,
    CreatePermissionGroupResponseTypeDef,
    CreateUserRequestRequestTypeDef,
    CreateUserResponseTypeDef,
    DeleteDatasetRequestRequestTypeDef,
    DeleteDatasetResponseTypeDef,
    DeletePermissionGroupRequestRequestTypeDef,
    DeletePermissionGroupResponseTypeDef,
    DisableUserRequestRequestTypeDef,
    DisableUserResponseTypeDef,
    DisassociateUserFromPermissionGroupRequestRequestTypeDef,
    DisassociateUserFromPermissionGroupResponseTypeDef,
    EnableUserRequestRequestTypeDef,
    EnableUserResponseTypeDef,
    GetChangesetRequestRequestTypeDef,
    GetChangesetResponseTypeDef,
    GetDatasetRequestRequestTypeDef,
    GetDatasetResponseTypeDef,
    GetDataViewRequestRequestTypeDef,
    GetDataViewResponseTypeDef,
    GetExternalDataViewAccessDetailsRequestRequestTypeDef,
    GetExternalDataViewAccessDetailsResponseTypeDef,
    GetPermissionGroupRequestRequestTypeDef,
    GetPermissionGroupResponseTypeDef,
    GetProgrammaticAccessCredentialsRequestRequestTypeDef,
    GetProgrammaticAccessCredentialsResponseTypeDef,
    GetUserRequestRequestTypeDef,
    GetUserResponseTypeDef,
    GetWorkingLocationRequestRequestTypeDef,
    GetWorkingLocationResponseTypeDef,
    ListChangesetsRequestRequestTypeDef,
    ListChangesetsResponseTypeDef,
    ListDatasetsRequestRequestTypeDef,
    ListDatasetsResponseTypeDef,
    ListDataViewsRequestRequestTypeDef,
    ListDataViewsResponseTypeDef,
    ListPermissionGroupsByUserRequestRequestTypeDef,
    ListPermissionGroupsByUserResponseTypeDef,
    ListPermissionGroupsRequestRequestTypeDef,
    ListPermissionGroupsResponseTypeDef,
    ListUsersByPermissionGroupRequestRequestTypeDef,
    ListUsersByPermissionGroupResponseTypeDef,
    ListUsersRequestRequestTypeDef,
    ListUsersResponseTypeDef,
    ResetUserPasswordRequestRequestTypeDef,
    ResetUserPasswordResponseTypeDef,
    UpdateChangesetRequestRequestTypeDef,
    UpdateChangesetResponseTypeDef,
    UpdateDatasetRequestRequestTypeDef,
    UpdateDatasetResponseTypeDef,
    UpdatePermissionGroupRequestRequestTypeDef,
    UpdatePermissionGroupResponseTypeDef,
    UpdateUserRequestRequestTypeDef,
    UpdateUserResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("FinSpaceDataClient",)

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
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class FinSpaceDataClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FinSpaceDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#close)
        """

    def associate_user_to_permission_group(
        self, **kwargs: Unpack[AssociateUserToPermissionGroupRequestRequestTypeDef]
    ) -> AssociateUserToPermissionGroupResponseTypeDef:
        """
        Adds a user to a permission group to grant permissions for actions a user can
        perform in FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/associate_user_to_permission_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#associate_user_to_permission_group)
        """

    def create_changeset(
        self, **kwargs: Unpack[CreateChangesetRequestRequestTypeDef]
    ) -> CreateChangesetResponseTypeDef:
        """
        Creates a new Changeset in a FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/create_changeset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#create_changeset)
        """

    def create_data_view(
        self, **kwargs: Unpack[CreateDataViewRequestRequestTypeDef]
    ) -> CreateDataViewResponseTypeDef:
        """
        Creates a Dataview for a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/create_data_view.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#create_data_view)
        """

    def create_dataset(
        self, **kwargs: Unpack[CreateDatasetRequestRequestTypeDef]
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a new FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/create_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#create_dataset)
        """

    def create_permission_group(
        self, **kwargs: Unpack[CreatePermissionGroupRequestRequestTypeDef]
    ) -> CreatePermissionGroupResponseTypeDef:
        """
        Creates a group of permissions for various actions that a user can perform in
        FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/create_permission_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#create_permission_group)
        """

    def create_user(
        self, **kwargs: Unpack[CreateUserRequestRequestTypeDef]
    ) -> CreateUserResponseTypeDef:
        """
        Creates a new user in FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/create_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#create_user)
        """

    def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestRequestTypeDef]
    ) -> DeleteDatasetResponseTypeDef:
        """
        Deletes a FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/delete_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#delete_dataset)
        """

    def delete_permission_group(
        self, **kwargs: Unpack[DeletePermissionGroupRequestRequestTypeDef]
    ) -> DeletePermissionGroupResponseTypeDef:
        """
        Deletes a permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/delete_permission_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#delete_permission_group)
        """

    def disable_user(
        self, **kwargs: Unpack[DisableUserRequestRequestTypeDef]
    ) -> DisableUserResponseTypeDef:
        """
        Denies access to the FinSpace web application and API for the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/disable_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#disable_user)
        """

    def disassociate_user_from_permission_group(
        self, **kwargs: Unpack[DisassociateUserFromPermissionGroupRequestRequestTypeDef]
    ) -> DisassociateUserFromPermissionGroupResponseTypeDef:
        """
        Removes a user from a permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/disassociate_user_from_permission_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#disassociate_user_from_permission_group)
        """

    def enable_user(
        self, **kwargs: Unpack[EnableUserRequestRequestTypeDef]
    ) -> EnableUserResponseTypeDef:
        """
        Allows the specified user to access the FinSpace web application and API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/enable_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#enable_user)
        """

    def get_changeset(
        self, **kwargs: Unpack[GetChangesetRequestRequestTypeDef]
    ) -> GetChangesetResponseTypeDef:
        """
        Get information about a Changeset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_changeset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#get_changeset)
        """

    def get_data_view(
        self, **kwargs: Unpack[GetDataViewRequestRequestTypeDef]
    ) -> GetDataViewResponseTypeDef:
        """
        Gets information about a Dataview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_data_view.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#get_data_view)
        """

    def get_dataset(
        self, **kwargs: Unpack[GetDatasetRequestRequestTypeDef]
    ) -> GetDatasetResponseTypeDef:
        """
        Returns information about a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#get_dataset)
        """

    def get_external_data_view_access_details(
        self, **kwargs: Unpack[GetExternalDataViewAccessDetailsRequestRequestTypeDef]
    ) -> GetExternalDataViewAccessDetailsResponseTypeDef:
        """
        Returns the credentials to access the external Dataview from an S3 location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_external_data_view_access_details.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#get_external_data_view_access_details)
        """

    def get_permission_group(
        self, **kwargs: Unpack[GetPermissionGroupRequestRequestTypeDef]
    ) -> GetPermissionGroupResponseTypeDef:
        """
        Retrieves the details of a specific permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_permission_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#get_permission_group)
        """

    def get_programmatic_access_credentials(
        self, **kwargs: Unpack[GetProgrammaticAccessCredentialsRequestRequestTypeDef]
    ) -> GetProgrammaticAccessCredentialsResponseTypeDef:
        """
        Request programmatic credentials to use with FinSpace SDK.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_programmatic_access_credentials.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#get_programmatic_access_credentials)
        """

    def get_user(self, **kwargs: Unpack[GetUserRequestRequestTypeDef]) -> GetUserResponseTypeDef:
        """
        Retrieves details for a specific user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#get_user)
        """

    def get_working_location(
        self, **kwargs: Unpack[GetWorkingLocationRequestRequestTypeDef]
    ) -> GetWorkingLocationResponseTypeDef:
        """
        A temporary Amazon S3 location, where you can copy your files from a source
        location to stage or use as a scratch space in FinSpace notebook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_working_location.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#get_working_location)
        """

    def list_changesets(
        self, **kwargs: Unpack[ListChangesetsRequestRequestTypeDef]
    ) -> ListChangesetsResponseTypeDef:
        """
        Lists the FinSpace Changesets for a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_changesets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#list_changesets)
        """

    def list_data_views(
        self, **kwargs: Unpack[ListDataViewsRequestRequestTypeDef]
    ) -> ListDataViewsResponseTypeDef:
        """
        Lists all available Dataviews for a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_data_views.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#list_data_views)
        """

    def list_datasets(
        self, **kwargs: Unpack[ListDatasetsRequestRequestTypeDef]
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists all of the active Datasets that a user has access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_datasets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#list_datasets)
        """

    def list_permission_groups(
        self, **kwargs: Unpack[ListPermissionGroupsRequestRequestTypeDef]
    ) -> ListPermissionGroupsResponseTypeDef:
        """
        Lists all available permission groups in FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_permission_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#list_permission_groups)
        """

    def list_permission_groups_by_user(
        self, **kwargs: Unpack[ListPermissionGroupsByUserRequestRequestTypeDef]
    ) -> ListPermissionGroupsByUserResponseTypeDef:
        """
        Lists all the permission groups that are associated with a specific user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_permission_groups_by_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#list_permission_groups_by_user)
        """

    def list_users(
        self, **kwargs: Unpack[ListUsersRequestRequestTypeDef]
    ) -> ListUsersResponseTypeDef:
        """
        Lists all available users in FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_users.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#list_users)
        """

    def list_users_by_permission_group(
        self, **kwargs: Unpack[ListUsersByPermissionGroupRequestRequestTypeDef]
    ) -> ListUsersByPermissionGroupResponseTypeDef:
        """
        Lists details of all the users in a specific permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_users_by_permission_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#list_users_by_permission_group)
        """

    def reset_user_password(
        self, **kwargs: Unpack[ResetUserPasswordRequestRequestTypeDef]
    ) -> ResetUserPasswordResponseTypeDef:
        """
        Resets the password for a specified user ID and generates a temporary one.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/reset_user_password.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#reset_user_password)
        """

    def update_changeset(
        self, **kwargs: Unpack[UpdateChangesetRequestRequestTypeDef]
    ) -> UpdateChangesetResponseTypeDef:
        """
        Updates a FinSpace Changeset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/update_changeset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#update_changeset)
        """

    def update_dataset(
        self, **kwargs: Unpack[UpdateDatasetRequestRequestTypeDef]
    ) -> UpdateDatasetResponseTypeDef:
        """
        Updates a FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/update_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#update_dataset)
        """

    def update_permission_group(
        self, **kwargs: Unpack[UpdatePermissionGroupRequestRequestTypeDef]
    ) -> UpdatePermissionGroupResponseTypeDef:
        """
        Modifies the details of a permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/update_permission_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#update_permission_group)
        """

    def update_user(
        self, **kwargs: Unpack[UpdateUserRequestRequestTypeDef]
    ) -> UpdateUserResponseTypeDef:
        """
        Modifies the details of the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/update_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#update_user)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_changesets"]) -> ListChangesetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_data_views"]) -> ListDataViewsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_datasets"]) -> ListDatasetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_permission_groups"]
    ) -> ListPermissionGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace_data/client/#get_paginator)
        """
