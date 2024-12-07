"""
Type annotations for codedeploy service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codedeploy.client import CodeDeployClient
    from mypy_boto3_codedeploy.paginator import (
        ListApplicationRevisionsPaginator,
        ListApplicationsPaginator,
        ListDeploymentConfigsPaginator,
        ListDeploymentGroupsPaginator,
        ListDeploymentInstancesPaginator,
        ListDeploymentTargetsPaginator,
        ListDeploymentsPaginator,
        ListGitHubAccountTokenNamesPaginator,
        ListOnPremisesInstancesPaginator,
    )

    session = Session()
    client: CodeDeployClient = session.client("codedeploy")

    list_application_revisions_paginator: ListApplicationRevisionsPaginator = client.get_paginator("list_application_revisions")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_deployment_configs_paginator: ListDeploymentConfigsPaginator = client.get_paginator("list_deployment_configs")
    list_deployment_groups_paginator: ListDeploymentGroupsPaginator = client.get_paginator("list_deployment_groups")
    list_deployment_instances_paginator: ListDeploymentInstancesPaginator = client.get_paginator("list_deployment_instances")
    list_deployment_targets_paginator: ListDeploymentTargetsPaginator = client.get_paginator("list_deployment_targets")
    list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
    list_git_hub_account_token_names_paginator: ListGitHubAccountTokenNamesPaginator = client.get_paginator("list_git_hub_account_token_names")
    list_on_premises_instances_paginator: ListOnPremisesInstancesPaginator = client.get_paginator("list_on_premises_instances")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef,
    ListApplicationRevisionsOutputTypeDef,
    ListApplicationsInputListApplicationsPaginateTypeDef,
    ListApplicationsOutputTypeDef,
    ListDeploymentConfigsInputListDeploymentConfigsPaginateTypeDef,
    ListDeploymentConfigsOutputTypeDef,
    ListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef,
    ListDeploymentGroupsOutputTypeDef,
    ListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef,
    ListDeploymentInstancesOutputTypeDef,
    ListDeploymentsInputListDeploymentsPaginateTypeDef,
    ListDeploymentsOutputTypeDef,
    ListDeploymentTargetsInputListDeploymentTargetsPaginateTypeDef,
    ListDeploymentTargetsOutputTypeDef,
    ListGitHubAccountTokenNamesInputListGitHubAccountTokenNamesPaginateTypeDef,
    ListGitHubAccountTokenNamesOutputTypeDef,
    ListOnPremisesInstancesInputListOnPremisesInstancesPaginateTypeDef,
    ListOnPremisesInstancesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListApplicationRevisionsPaginator",
    "ListApplicationsPaginator",
    "ListDeploymentConfigsPaginator",
    "ListDeploymentGroupsPaginator",
    "ListDeploymentInstancesPaginator",
    "ListDeploymentTargetsPaginator",
    "ListDeploymentsPaginator",
    "ListGitHubAccountTokenNamesPaginator",
    "ListOnPremisesInstancesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationRevisionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListApplicationRevisions.html#CodeDeploy.Paginator.ListApplicationRevisions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listapplicationrevisionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef]
    ) -> _PageIterator[ListApplicationRevisionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListApplicationRevisions.html#CodeDeploy.Paginator.ListApplicationRevisions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listapplicationrevisionspaginator)
        """


class ListApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListApplications.html#CodeDeploy.Paginator.ListApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listapplicationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApplicationsInputListApplicationsPaginateTypeDef]
    ) -> _PageIterator[ListApplicationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListApplications.html#CodeDeploy.Paginator.ListApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listapplicationspaginator)
        """


class ListDeploymentConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentConfigs.html#CodeDeploy.Paginator.ListDeploymentConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentconfigspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeploymentConfigsInputListDeploymentConfigsPaginateTypeDef]
    ) -> _PageIterator[ListDeploymentConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentConfigs.html#CodeDeploy.Paginator.ListDeploymentConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentconfigspaginator)
        """


class ListDeploymentGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentGroups.html#CodeDeploy.Paginator.ListDeploymentGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef]
    ) -> _PageIterator[ListDeploymentGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentGroups.html#CodeDeploy.Paginator.ListDeploymentGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentgroupspaginator)
        """


class ListDeploymentInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentInstances.html#CodeDeploy.Paginator.ListDeploymentInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef]
    ) -> _PageIterator[ListDeploymentInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentInstances.html#CodeDeploy.Paginator.ListDeploymentInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentinstancespaginator)
        """


class ListDeploymentTargetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentTargets.html#CodeDeploy.Paginator.ListDeploymentTargets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymenttargetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeploymentTargetsInputListDeploymentTargetsPaginateTypeDef]
    ) -> _PageIterator[ListDeploymentTargetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentTargets.html#CodeDeploy.Paginator.ListDeploymentTargets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymenttargetspaginator)
        """


class ListDeploymentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeployments.html#CodeDeploy.Paginator.ListDeployments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeploymentsInputListDeploymentsPaginateTypeDef]
    ) -> _PageIterator[ListDeploymentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeployments.html#CodeDeploy.Paginator.ListDeployments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listdeploymentspaginator)
        """


class ListGitHubAccountTokenNamesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListGitHubAccountTokenNames.html#CodeDeploy.Paginator.ListGitHubAccountTokenNames)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listgithubaccounttokennamespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListGitHubAccountTokenNamesInputListGitHubAccountTokenNamesPaginateTypeDef
        ],
    ) -> _PageIterator[ListGitHubAccountTokenNamesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListGitHubAccountTokenNames.html#CodeDeploy.Paginator.ListGitHubAccountTokenNames.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listgithubaccounttokennamespaginator)
        """


class ListOnPremisesInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListOnPremisesInstances.html#CodeDeploy.Paginator.ListOnPremisesInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listonpremisesinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOnPremisesInstancesInputListOnPremisesInstancesPaginateTypeDef]
    ) -> _PageIterator[ListOnPremisesInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListOnPremisesInstances.html#CodeDeploy.Paginator.ListOnPremisesInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/paginators/#listonpremisesinstancespaginator)
        """
