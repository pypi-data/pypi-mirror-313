"""
Type annotations for migrationhuborchestrator service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_migrationhuborchestrator.client import MigrationHubOrchestratorClient
    from mypy_boto3_migrationhuborchestrator.paginator import (
        ListPluginsPaginator,
        ListTemplateStepGroupsPaginator,
        ListTemplateStepsPaginator,
        ListTemplatesPaginator,
        ListWorkflowStepGroupsPaginator,
        ListWorkflowStepsPaginator,
        ListWorkflowsPaginator,
    )

    session = Session()
    client: MigrationHubOrchestratorClient = session.client("migrationhuborchestrator")

    list_plugins_paginator: ListPluginsPaginator = client.get_paginator("list_plugins")
    list_template_step_groups_paginator: ListTemplateStepGroupsPaginator = client.get_paginator("list_template_step_groups")
    list_template_steps_paginator: ListTemplateStepsPaginator = client.get_paginator("list_template_steps")
    list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
    list_workflow_step_groups_paginator: ListWorkflowStepGroupsPaginator = client.get_paginator("list_workflow_step_groups")
    list_workflow_steps_paginator: ListWorkflowStepsPaginator = client.get_paginator("list_workflow_steps")
    list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListMigrationWorkflowsRequestListWorkflowsPaginateTypeDef,
    ListMigrationWorkflowsResponseTypeDef,
    ListMigrationWorkflowTemplatesRequestListTemplatesPaginateTypeDef,
    ListMigrationWorkflowTemplatesResponseTypeDef,
    ListPluginsRequestListPluginsPaginateTypeDef,
    ListPluginsResponseTypeDef,
    ListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef,
    ListTemplateStepGroupsResponseTypeDef,
    ListTemplateStepsRequestListTemplateStepsPaginateTypeDef,
    ListTemplateStepsResponseTypeDef,
    ListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef,
    ListWorkflowStepGroupsResponseTypeDef,
    ListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef,
    ListWorkflowStepsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListPluginsPaginator",
    "ListTemplateStepGroupsPaginator",
    "ListTemplateStepsPaginator",
    "ListTemplatesPaginator",
    "ListWorkflowStepGroupsPaginator",
    "ListWorkflowStepsPaginator",
    "ListWorkflowsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListPluginsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListPlugins.html#MigrationHubOrchestrator.Paginator.ListPlugins)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listpluginspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPluginsRequestListPluginsPaginateTypeDef]
    ) -> _PageIterator[ListPluginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListPlugins.html#MigrationHubOrchestrator.Paginator.ListPlugins.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listpluginspaginator)
        """


class ListTemplateStepGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplateStepGroups.html#MigrationHubOrchestrator.Paginator.ListTemplateStepGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listtemplatestepgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef]
    ) -> _PageIterator[ListTemplateStepGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplateStepGroups.html#MigrationHubOrchestrator.Paginator.ListTemplateStepGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listtemplatestepgroupspaginator)
        """


class ListTemplateStepsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplateSteps.html#MigrationHubOrchestrator.Paginator.ListTemplateSteps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listtemplatestepspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTemplateStepsRequestListTemplateStepsPaginateTypeDef]
    ) -> _PageIterator[ListTemplateStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplateSteps.html#MigrationHubOrchestrator.Paginator.ListTemplateSteps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listtemplatestepspaginator)
        """


class ListTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplates.html#MigrationHubOrchestrator.Paginator.ListTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listtemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMigrationWorkflowTemplatesRequestListTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListMigrationWorkflowTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplates.html#MigrationHubOrchestrator.Paginator.ListTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listtemplatespaginator)
        """


class ListWorkflowStepGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflowStepGroups.html#MigrationHubOrchestrator.Paginator.ListWorkflowStepGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listworkflowstepgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef]
    ) -> _PageIterator[ListWorkflowStepGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflowStepGroups.html#MigrationHubOrchestrator.Paginator.ListWorkflowStepGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listworkflowstepgroupspaginator)
        """


class ListWorkflowStepsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflowSteps.html#MigrationHubOrchestrator.Paginator.ListWorkflowSteps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listworkflowstepspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef]
    ) -> _PageIterator[ListWorkflowStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflowSteps.html#MigrationHubOrchestrator.Paginator.ListWorkflowSteps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listworkflowstepspaginator)
        """


class ListWorkflowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflows.html#MigrationHubOrchestrator.Paginator.ListWorkflows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listworkflowspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMigrationWorkflowsRequestListWorkflowsPaginateTypeDef]
    ) -> _PageIterator[ListMigrationWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflows.html#MigrationHubOrchestrator.Paginator.ListWorkflows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/paginators/#listworkflowspaginator)
        """
