"""
Type annotations for appconfig service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_appconfig.client import AppConfigClient
    from mypy_boto3_appconfig.paginator import (
        ListApplicationsPaginator,
        ListConfigurationProfilesPaginator,
        ListDeploymentStrategiesPaginator,
        ListDeploymentsPaginator,
        ListEnvironmentsPaginator,
        ListExtensionAssociationsPaginator,
        ListExtensionsPaginator,
        ListHostedConfigurationVersionsPaginator,
    )

    session = Session()
    client: AppConfigClient = session.client("appconfig")

    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_configuration_profiles_paginator: ListConfigurationProfilesPaginator = client.get_paginator("list_configuration_profiles")
    list_deployment_strategies_paginator: ListDeploymentStrategiesPaginator = client.get_paginator("list_deployment_strategies")
    list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    list_extension_associations_paginator: ListExtensionAssociationsPaginator = client.get_paginator("list_extension_associations")
    list_extensions_paginator: ListExtensionsPaginator = client.get_paginator("list_extensions")
    list_hosted_configuration_versions_paginator: ListHostedConfigurationVersionsPaginator = client.get_paginator("list_hosted_configuration_versions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ApplicationsTypeDef,
    ConfigurationProfilesTypeDef,
    DeploymentStrategiesTypeDef,
    DeploymentsTypeDef,
    EnvironmentsTypeDef,
    ExtensionAssociationsTypeDef,
    ExtensionsTypeDef,
    HostedConfigurationVersionsTypeDef,
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListConfigurationProfilesRequestListConfigurationProfilesPaginateTypeDef,
    ListDeploymentsRequestListDeploymentsPaginateTypeDef,
    ListDeploymentStrategiesRequestListDeploymentStrategiesPaginateTypeDef,
    ListEnvironmentsRequestListEnvironmentsPaginateTypeDef,
    ListExtensionAssociationsRequestListExtensionAssociationsPaginateTypeDef,
    ListExtensionsRequestListExtensionsPaginateTypeDef,
    ListHostedConfigurationVersionsRequestListHostedConfigurationVersionsPaginateTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListApplicationsPaginator",
    "ListConfigurationProfilesPaginator",
    "ListDeploymentStrategiesPaginator",
    "ListDeploymentsPaginator",
    "ListEnvironmentsPaginator",
    "ListExtensionAssociationsPaginator",
    "ListExtensionsPaginator",
    "ListHostedConfigurationVersionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListApplications.html#AppConfig.Paginator.ListApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listapplicationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> _PageIterator[ApplicationsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListApplications.html#AppConfig.Paginator.ListApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listapplicationspaginator)
        """

class ListConfigurationProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListConfigurationProfiles.html#AppConfig.Paginator.ListConfigurationProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listconfigurationprofilespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListConfigurationProfilesRequestListConfigurationProfilesPaginateTypeDef],
    ) -> _PageIterator[ConfigurationProfilesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListConfigurationProfiles.html#AppConfig.Paginator.ListConfigurationProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listconfigurationprofilespaginator)
        """

class ListDeploymentStrategiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListDeploymentStrategies.html#AppConfig.Paginator.ListDeploymentStrategies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listdeploymentstrategiespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListDeploymentStrategiesRequestListDeploymentStrategiesPaginateTypeDef],
    ) -> _PageIterator[DeploymentStrategiesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListDeploymentStrategies.html#AppConfig.Paginator.ListDeploymentStrategies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listdeploymentstrategiespaginator)
        """

class ListDeploymentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListDeployments.html#AppConfig.Paginator.ListDeployments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listdeploymentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDeploymentsRequestListDeploymentsPaginateTypeDef]
    ) -> _PageIterator[DeploymentsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListDeployments.html#AppConfig.Paginator.ListDeployments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listdeploymentspaginator)
        """

class ListEnvironmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListEnvironments.html#AppConfig.Paginator.ListEnvironments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listenvironmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEnvironmentsRequestListEnvironmentsPaginateTypeDef]
    ) -> _PageIterator[EnvironmentsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListEnvironments.html#AppConfig.Paginator.ListEnvironments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listenvironmentspaginator)
        """

class ListExtensionAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExtensionAssociations.html#AppConfig.Paginator.ListExtensionAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listextensionassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListExtensionAssociationsRequestListExtensionAssociationsPaginateTypeDef],
    ) -> _PageIterator[ExtensionAssociationsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExtensionAssociations.html#AppConfig.Paginator.ListExtensionAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listextensionassociationspaginator)
        """

class ListExtensionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExtensions.html#AppConfig.Paginator.ListExtensions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listextensionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListExtensionsRequestListExtensionsPaginateTypeDef]
    ) -> _PageIterator[ExtensionsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListExtensions.html#AppConfig.Paginator.ListExtensions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listextensionspaginator)
        """

class ListHostedConfigurationVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListHostedConfigurationVersions.html#AppConfig.Paginator.ListHostedConfigurationVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listhostedconfigurationversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListHostedConfigurationVersionsRequestListHostedConfigurationVersionsPaginateTypeDef
        ],
    ) -> _PageIterator[HostedConfigurationVersionsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/paginator/ListHostedConfigurationVersions.html#AppConfig.Paginator.ListHostedConfigurationVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appconfig/paginators/#listhostedconfigurationversionspaginator)
        """
