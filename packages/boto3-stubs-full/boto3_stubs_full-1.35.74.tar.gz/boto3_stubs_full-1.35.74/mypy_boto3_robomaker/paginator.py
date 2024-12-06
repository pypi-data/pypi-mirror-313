"""
Type annotations for robomaker service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_robomaker.client import RoboMakerClient
    from mypy_boto3_robomaker.paginator import (
        ListDeploymentJobsPaginator,
        ListFleetsPaginator,
        ListRobotApplicationsPaginator,
        ListRobotsPaginator,
        ListSimulationApplicationsPaginator,
        ListSimulationJobBatchesPaginator,
        ListSimulationJobsPaginator,
        ListWorldExportJobsPaginator,
        ListWorldGenerationJobsPaginator,
        ListWorldTemplatesPaginator,
        ListWorldsPaginator,
    )

    session = Session()
    client: RoboMakerClient = session.client("robomaker")

    list_deployment_jobs_paginator: ListDeploymentJobsPaginator = client.get_paginator("list_deployment_jobs")
    list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
    list_robot_applications_paginator: ListRobotApplicationsPaginator = client.get_paginator("list_robot_applications")
    list_robots_paginator: ListRobotsPaginator = client.get_paginator("list_robots")
    list_simulation_applications_paginator: ListSimulationApplicationsPaginator = client.get_paginator("list_simulation_applications")
    list_simulation_job_batches_paginator: ListSimulationJobBatchesPaginator = client.get_paginator("list_simulation_job_batches")
    list_simulation_jobs_paginator: ListSimulationJobsPaginator = client.get_paginator("list_simulation_jobs")
    list_world_export_jobs_paginator: ListWorldExportJobsPaginator = client.get_paginator("list_world_export_jobs")
    list_world_generation_jobs_paginator: ListWorldGenerationJobsPaginator = client.get_paginator("list_world_generation_jobs")
    list_world_templates_paginator: ListWorldTemplatesPaginator = client.get_paginator("list_world_templates")
    list_worlds_paginator: ListWorldsPaginator = client.get_paginator("list_worlds")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDeploymentJobsRequestListDeploymentJobsPaginateTypeDef,
    ListDeploymentJobsResponseTypeDef,
    ListFleetsRequestListFleetsPaginateTypeDef,
    ListFleetsResponseTypeDef,
    ListRobotApplicationsRequestListRobotApplicationsPaginateTypeDef,
    ListRobotApplicationsResponseTypeDef,
    ListRobotsRequestListRobotsPaginateTypeDef,
    ListRobotsResponseTypeDef,
    ListSimulationApplicationsRequestListSimulationApplicationsPaginateTypeDef,
    ListSimulationApplicationsResponseTypeDef,
    ListSimulationJobBatchesRequestListSimulationJobBatchesPaginateTypeDef,
    ListSimulationJobBatchesResponseTypeDef,
    ListSimulationJobsRequestListSimulationJobsPaginateTypeDef,
    ListSimulationJobsResponseTypeDef,
    ListWorldExportJobsRequestListWorldExportJobsPaginateTypeDef,
    ListWorldExportJobsResponseTypeDef,
    ListWorldGenerationJobsRequestListWorldGenerationJobsPaginateTypeDef,
    ListWorldGenerationJobsResponseTypeDef,
    ListWorldsRequestListWorldsPaginateTypeDef,
    ListWorldsResponseTypeDef,
    ListWorldTemplatesRequestListWorldTemplatesPaginateTypeDef,
    ListWorldTemplatesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDeploymentJobsPaginator",
    "ListFleetsPaginator",
    "ListRobotApplicationsPaginator",
    "ListRobotsPaginator",
    "ListSimulationApplicationsPaginator",
    "ListSimulationJobBatchesPaginator",
    "ListSimulationJobsPaginator",
    "ListWorldExportJobsPaginator",
    "ListWorldGenerationJobsPaginator",
    "ListWorldTemplatesPaginator",
    "ListWorldsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDeploymentJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListDeploymentJobs.html#RoboMaker.Paginator.ListDeploymentJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listdeploymentjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeploymentJobsRequestListDeploymentJobsPaginateTypeDef]
    ) -> _PageIterator[ListDeploymentJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListDeploymentJobs.html#RoboMaker.Paginator.ListDeploymentJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listdeploymentjobspaginator)
        """


class ListFleetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListFleets.html#RoboMaker.Paginator.ListFleets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listfleetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFleetsRequestListFleetsPaginateTypeDef]
    ) -> _PageIterator[ListFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListFleets.html#RoboMaker.Paginator.ListFleets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listfleetspaginator)
        """


class ListRobotApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListRobotApplications.html#RoboMaker.Paginator.ListRobotApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listrobotapplicationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRobotApplicationsRequestListRobotApplicationsPaginateTypeDef]
    ) -> _PageIterator[ListRobotApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListRobotApplications.html#RoboMaker.Paginator.ListRobotApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listrobotapplicationspaginator)
        """


class ListRobotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListRobots.html#RoboMaker.Paginator.ListRobots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listrobotspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRobotsRequestListRobotsPaginateTypeDef]
    ) -> _PageIterator[ListRobotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListRobots.html#RoboMaker.Paginator.ListRobots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listrobotspaginator)
        """


class ListSimulationApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationApplications.html#RoboMaker.Paginator.ListSimulationApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listsimulationapplicationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListSimulationApplicationsRequestListSimulationApplicationsPaginateTypeDef
        ],
    ) -> _PageIterator[ListSimulationApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationApplications.html#RoboMaker.Paginator.ListSimulationApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listsimulationapplicationspaginator)
        """


class ListSimulationJobBatchesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationJobBatches.html#RoboMaker.Paginator.ListSimulationJobBatches)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listsimulationjobbatchespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListSimulationJobBatchesRequestListSimulationJobBatchesPaginateTypeDef],
    ) -> _PageIterator[ListSimulationJobBatchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationJobBatches.html#RoboMaker.Paginator.ListSimulationJobBatches.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listsimulationjobbatchespaginator)
        """


class ListSimulationJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationJobs.html#RoboMaker.Paginator.ListSimulationJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listsimulationjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSimulationJobsRequestListSimulationJobsPaginateTypeDef]
    ) -> _PageIterator[ListSimulationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationJobs.html#RoboMaker.Paginator.ListSimulationJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listsimulationjobspaginator)
        """


class ListWorldExportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldExportJobs.html#RoboMaker.Paginator.ListWorldExportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listworldexportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorldExportJobsRequestListWorldExportJobsPaginateTypeDef]
    ) -> _PageIterator[ListWorldExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldExportJobs.html#RoboMaker.Paginator.ListWorldExportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listworldexportjobspaginator)
        """


class ListWorldGenerationJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldGenerationJobs.html#RoboMaker.Paginator.ListWorldGenerationJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listworldgenerationjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorldGenerationJobsRequestListWorldGenerationJobsPaginateTypeDef]
    ) -> _PageIterator[ListWorldGenerationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldGenerationJobs.html#RoboMaker.Paginator.ListWorldGenerationJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listworldgenerationjobspaginator)
        """


class ListWorldTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldTemplates.html#RoboMaker.Paginator.ListWorldTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listworldtemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorldTemplatesRequestListWorldTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListWorldTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldTemplates.html#RoboMaker.Paginator.ListWorldTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listworldtemplatespaginator)
        """


class ListWorldsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorlds.html#RoboMaker.Paginator.ListWorlds)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listworldspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorldsRequestListWorldsPaginateTypeDef]
    ) -> _PageIterator[ListWorldsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorlds.html#RoboMaker.Paginator.ListWorlds.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_robomaker/paginators/#listworldspaginator)
        """
