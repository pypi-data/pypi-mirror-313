"""
Type annotations for codebuild service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codebuild.client import CodeBuildClient
    from mypy_boto3_codebuild.paginator import (
        DescribeCodeCoveragesPaginator,
        DescribeTestCasesPaginator,
        ListBuildBatchesForProjectPaginator,
        ListBuildBatchesPaginator,
        ListBuildsForProjectPaginator,
        ListBuildsPaginator,
        ListProjectsPaginator,
        ListReportGroupsPaginator,
        ListReportsForReportGroupPaginator,
        ListReportsPaginator,
        ListSharedProjectsPaginator,
        ListSharedReportGroupsPaginator,
    )

    session = Session()
    client: CodeBuildClient = session.client("codebuild")

    describe_code_coverages_paginator: DescribeCodeCoveragesPaginator = client.get_paginator("describe_code_coverages")
    describe_test_cases_paginator: DescribeTestCasesPaginator = client.get_paginator("describe_test_cases")
    list_build_batches_for_project_paginator: ListBuildBatchesForProjectPaginator = client.get_paginator("list_build_batches_for_project")
    list_build_batches_paginator: ListBuildBatchesPaginator = client.get_paginator("list_build_batches")
    list_builds_for_project_paginator: ListBuildsForProjectPaginator = client.get_paginator("list_builds_for_project")
    list_builds_paginator: ListBuildsPaginator = client.get_paginator("list_builds")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    list_report_groups_paginator: ListReportGroupsPaginator = client.get_paginator("list_report_groups")
    list_reports_for_report_group_paginator: ListReportsForReportGroupPaginator = client.get_paginator("list_reports_for_report_group")
    list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
    list_shared_projects_paginator: ListSharedProjectsPaginator = client.get_paginator("list_shared_projects")
    list_shared_report_groups_paginator: ListSharedReportGroupsPaginator = client.get_paginator("list_shared_report_groups")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeCodeCoveragesInputDescribeCodeCoveragesPaginateTypeDef,
    DescribeCodeCoveragesOutputTypeDef,
    DescribeTestCasesInputDescribeTestCasesPaginateTypeDef,
    DescribeTestCasesOutputTypeDef,
    ListBuildBatchesForProjectInputListBuildBatchesForProjectPaginateTypeDef,
    ListBuildBatchesForProjectOutputTypeDef,
    ListBuildBatchesInputListBuildBatchesPaginateTypeDef,
    ListBuildBatchesOutputTypeDef,
    ListBuildsForProjectInputListBuildsForProjectPaginateTypeDef,
    ListBuildsForProjectOutputTypeDef,
    ListBuildsInputListBuildsPaginateTypeDef,
    ListBuildsOutputTypeDef,
    ListProjectsInputListProjectsPaginateTypeDef,
    ListProjectsOutputTypeDef,
    ListReportGroupsInputListReportGroupsPaginateTypeDef,
    ListReportGroupsOutputTypeDef,
    ListReportsForReportGroupInputListReportsForReportGroupPaginateTypeDef,
    ListReportsForReportGroupOutputTypeDef,
    ListReportsInputListReportsPaginateTypeDef,
    ListReportsOutputTypeDef,
    ListSharedProjectsInputListSharedProjectsPaginateTypeDef,
    ListSharedProjectsOutputTypeDef,
    ListSharedReportGroupsInputListSharedReportGroupsPaginateTypeDef,
    ListSharedReportGroupsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeCodeCoveragesPaginator",
    "DescribeTestCasesPaginator",
    "ListBuildBatchesForProjectPaginator",
    "ListBuildBatchesPaginator",
    "ListBuildsForProjectPaginator",
    "ListBuildsPaginator",
    "ListProjectsPaginator",
    "ListReportGroupsPaginator",
    "ListReportsForReportGroupPaginator",
    "ListReportsPaginator",
    "ListSharedProjectsPaginator",
    "ListSharedReportGroupsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeCodeCoveragesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/DescribeCodeCoverages.html#CodeBuild.Paginator.DescribeCodeCoverages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#describecodecoveragespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeCodeCoveragesInputDescribeCodeCoveragesPaginateTypeDef]
    ) -> _PageIterator[DescribeCodeCoveragesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/DescribeCodeCoverages.html#CodeBuild.Paginator.DescribeCodeCoverages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#describecodecoveragespaginator)
        """

class DescribeTestCasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/DescribeTestCases.html#CodeBuild.Paginator.DescribeTestCases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#describetestcasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeTestCasesInputDescribeTestCasesPaginateTypeDef]
    ) -> _PageIterator[DescribeTestCasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/DescribeTestCases.html#CodeBuild.Paginator.DescribeTestCases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#describetestcasespaginator)
        """

class ListBuildBatchesForProjectPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuildBatchesForProject.html#CodeBuild.Paginator.ListBuildBatchesForProject)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listbuildbatchesforprojectpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListBuildBatchesForProjectInputListBuildBatchesForProjectPaginateTypeDef],
    ) -> _PageIterator[ListBuildBatchesForProjectOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuildBatchesForProject.html#CodeBuild.Paginator.ListBuildBatchesForProject.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listbuildbatchesforprojectpaginator)
        """

class ListBuildBatchesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuildBatches.html#CodeBuild.Paginator.ListBuildBatches)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listbuildbatchespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBuildBatchesInputListBuildBatchesPaginateTypeDef]
    ) -> _PageIterator[ListBuildBatchesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuildBatches.html#CodeBuild.Paginator.ListBuildBatches.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listbuildbatchespaginator)
        """

class ListBuildsForProjectPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuildsForProject.html#CodeBuild.Paginator.ListBuildsForProject)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listbuildsforprojectpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBuildsForProjectInputListBuildsForProjectPaginateTypeDef]
    ) -> _PageIterator[ListBuildsForProjectOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuildsForProject.html#CodeBuild.Paginator.ListBuildsForProject.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listbuildsforprojectpaginator)
        """

class ListBuildsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuilds.html#CodeBuild.Paginator.ListBuilds)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listbuildspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBuildsInputListBuildsPaginateTypeDef]
    ) -> _PageIterator[ListBuildsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuilds.html#CodeBuild.Paginator.ListBuilds.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listbuildspaginator)
        """

class ListProjectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListProjects.html#CodeBuild.Paginator.ListProjects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listprojectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProjectsInputListProjectsPaginateTypeDef]
    ) -> _PageIterator[ListProjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListProjects.html#CodeBuild.Paginator.ListProjects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listprojectspaginator)
        """

class ListReportGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListReportGroups.html#CodeBuild.Paginator.ListReportGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listreportgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListReportGroupsInputListReportGroupsPaginateTypeDef]
    ) -> _PageIterator[ListReportGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListReportGroups.html#CodeBuild.Paginator.ListReportGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listreportgroupspaginator)
        """

class ListReportsForReportGroupPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListReportsForReportGroup.html#CodeBuild.Paginator.ListReportsForReportGroup)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listreportsforreportgrouppaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListReportsForReportGroupInputListReportsForReportGroupPaginateTypeDef],
    ) -> _PageIterator[ListReportsForReportGroupOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListReportsForReportGroup.html#CodeBuild.Paginator.ListReportsForReportGroup.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listreportsforreportgrouppaginator)
        """

class ListReportsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListReports.html#CodeBuild.Paginator.ListReports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listreportspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListReportsInputListReportsPaginateTypeDef]
    ) -> _PageIterator[ListReportsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListReports.html#CodeBuild.Paginator.ListReports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listreportspaginator)
        """

class ListSharedProjectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListSharedProjects.html#CodeBuild.Paginator.ListSharedProjects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listsharedprojectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSharedProjectsInputListSharedProjectsPaginateTypeDef]
    ) -> _PageIterator[ListSharedProjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListSharedProjects.html#CodeBuild.Paginator.ListSharedProjects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listsharedprojectspaginator)
        """

class ListSharedReportGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListSharedReportGroups.html#CodeBuild.Paginator.ListSharedReportGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listsharedreportgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSharedReportGroupsInputListSharedReportGroupsPaginateTypeDef]
    ) -> _PageIterator[ListSharedReportGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListSharedReportGroups.html#CodeBuild.Paginator.ListSharedReportGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/paginators/#listsharedreportgroupspaginator)
        """
