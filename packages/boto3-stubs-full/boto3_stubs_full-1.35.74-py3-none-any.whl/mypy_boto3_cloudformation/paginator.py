"""
Type annotations for cloudformation service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cloudformation.client import CloudFormationClient
    from mypy_boto3_cloudformation.paginator import (
        DescribeAccountLimitsPaginator,
        DescribeChangeSetPaginator,
        DescribeStackEventsPaginator,
        DescribeStacksPaginator,
        ListChangeSetsPaginator,
        ListExportsPaginator,
        ListGeneratedTemplatesPaginator,
        ListImportsPaginator,
        ListResourceScanRelatedResourcesPaginator,
        ListResourceScanResourcesPaginator,
        ListResourceScansPaginator,
        ListStackInstancesPaginator,
        ListStackResourcesPaginator,
        ListStackSetOperationResultsPaginator,
        ListStackSetOperationsPaginator,
        ListStackSetsPaginator,
        ListStacksPaginator,
        ListTypesPaginator,
    )

    session = Session()
    client: CloudFormationClient = session.client("cloudformation")

    describe_account_limits_paginator: DescribeAccountLimitsPaginator = client.get_paginator("describe_account_limits")
    describe_change_set_paginator: DescribeChangeSetPaginator = client.get_paginator("describe_change_set")
    describe_stack_events_paginator: DescribeStackEventsPaginator = client.get_paginator("describe_stack_events")
    describe_stacks_paginator: DescribeStacksPaginator = client.get_paginator("describe_stacks")
    list_change_sets_paginator: ListChangeSetsPaginator = client.get_paginator("list_change_sets")
    list_exports_paginator: ListExportsPaginator = client.get_paginator("list_exports")
    list_generated_templates_paginator: ListGeneratedTemplatesPaginator = client.get_paginator("list_generated_templates")
    list_imports_paginator: ListImportsPaginator = client.get_paginator("list_imports")
    list_resource_scan_related_resources_paginator: ListResourceScanRelatedResourcesPaginator = client.get_paginator("list_resource_scan_related_resources")
    list_resource_scan_resources_paginator: ListResourceScanResourcesPaginator = client.get_paginator("list_resource_scan_resources")
    list_resource_scans_paginator: ListResourceScansPaginator = client.get_paginator("list_resource_scans")
    list_stack_instances_paginator: ListStackInstancesPaginator = client.get_paginator("list_stack_instances")
    list_stack_resources_paginator: ListStackResourcesPaginator = client.get_paginator("list_stack_resources")
    list_stack_set_operation_results_paginator: ListStackSetOperationResultsPaginator = client.get_paginator("list_stack_set_operation_results")
    list_stack_set_operations_paginator: ListStackSetOperationsPaginator = client.get_paginator("list_stack_set_operations")
    list_stack_sets_paginator: ListStackSetsPaginator = client.get_paginator("list_stack_sets")
    list_stacks_paginator: ListStacksPaginator = client.get_paginator("list_stacks")
    list_types_paginator: ListTypesPaginator = client.get_paginator("list_types")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef,
    DescribeAccountLimitsOutputTypeDef,
    DescribeChangeSetInputDescribeChangeSetPaginateTypeDef,
    DescribeChangeSetOutputTypeDef,
    DescribeStackEventsInputDescribeStackEventsPaginateTypeDef,
    DescribeStackEventsOutputTypeDef,
    DescribeStacksInputDescribeStacksPaginateTypeDef,
    DescribeStacksOutputTypeDef,
    ListChangeSetsInputListChangeSetsPaginateTypeDef,
    ListChangeSetsOutputTypeDef,
    ListExportsInputListExportsPaginateTypeDef,
    ListExportsOutputTypeDef,
    ListGeneratedTemplatesInputListGeneratedTemplatesPaginateTypeDef,
    ListGeneratedTemplatesOutputTypeDef,
    ListImportsInputListImportsPaginateTypeDef,
    ListImportsOutputTypeDef,
    ListResourceScanRelatedResourcesInputListResourceScanRelatedResourcesPaginateTypeDef,
    ListResourceScanRelatedResourcesOutputTypeDef,
    ListResourceScanResourcesInputListResourceScanResourcesPaginateTypeDef,
    ListResourceScanResourcesOutputTypeDef,
    ListResourceScansInputListResourceScansPaginateTypeDef,
    ListResourceScansOutputTypeDef,
    ListStackInstancesInputListStackInstancesPaginateTypeDef,
    ListStackInstancesOutputTypeDef,
    ListStackResourcesInputListStackResourcesPaginateTypeDef,
    ListStackResourcesOutputTypeDef,
    ListStackSetOperationResultsInputListStackSetOperationResultsPaginateTypeDef,
    ListStackSetOperationResultsOutputTypeDef,
    ListStackSetOperationsInputListStackSetOperationsPaginateTypeDef,
    ListStackSetOperationsOutputTypeDef,
    ListStackSetsInputListStackSetsPaginateTypeDef,
    ListStackSetsOutputTypeDef,
    ListStacksInputListStacksPaginateTypeDef,
    ListStacksOutputTypeDef,
    ListTypesInputListTypesPaginateTypeDef,
    ListTypesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAccountLimitsPaginator",
    "DescribeChangeSetPaginator",
    "DescribeStackEventsPaginator",
    "DescribeStacksPaginator",
    "ListChangeSetsPaginator",
    "ListExportsPaginator",
    "ListGeneratedTemplatesPaginator",
    "ListImportsPaginator",
    "ListResourceScanRelatedResourcesPaginator",
    "ListResourceScanResourcesPaginator",
    "ListResourceScansPaginator",
    "ListStackInstancesPaginator",
    "ListStackResourcesPaginator",
    "ListStackSetOperationResultsPaginator",
    "ListStackSetOperationsPaginator",
    "ListStackSetsPaginator",
    "ListStacksPaginator",
    "ListTypesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAccountLimitsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeAccountLimits.html#CloudFormation.Paginator.DescribeAccountLimits)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#describeaccountlimitspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef]
    ) -> _PageIterator[DescribeAccountLimitsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeAccountLimits.html#CloudFormation.Paginator.DescribeAccountLimits.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#describeaccountlimitspaginator)
        """


class DescribeChangeSetPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeChangeSet.html#CloudFormation.Paginator.DescribeChangeSet)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#describechangesetpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeChangeSetInputDescribeChangeSetPaginateTypeDef]
    ) -> _PageIterator[DescribeChangeSetOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeChangeSet.html#CloudFormation.Paginator.DescribeChangeSet.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#describechangesetpaginator)
        """


class DescribeStackEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeStackEvents.html#CloudFormation.Paginator.DescribeStackEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#describestackeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeStackEventsInputDescribeStackEventsPaginateTypeDef]
    ) -> _PageIterator[DescribeStackEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeStackEvents.html#CloudFormation.Paginator.DescribeStackEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#describestackeventspaginator)
        """


class DescribeStacksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeStacks.html#CloudFormation.Paginator.DescribeStacks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#describestackspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeStacksInputDescribeStacksPaginateTypeDef]
    ) -> _PageIterator[DescribeStacksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeStacks.html#CloudFormation.Paginator.DescribeStacks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#describestackspaginator)
        """


class ListChangeSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListChangeSets.html#CloudFormation.Paginator.ListChangeSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listchangesetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListChangeSetsInputListChangeSetsPaginateTypeDef]
    ) -> _PageIterator[ListChangeSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListChangeSets.html#CloudFormation.Paginator.ListChangeSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listchangesetspaginator)
        """


class ListExportsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListExports.html#CloudFormation.Paginator.ListExports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listexportspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListExportsInputListExportsPaginateTypeDef]
    ) -> _PageIterator[ListExportsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListExports.html#CloudFormation.Paginator.ListExports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listexportspaginator)
        """


class ListGeneratedTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListGeneratedTemplates.html#CloudFormation.Paginator.ListGeneratedTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listgeneratedtemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGeneratedTemplatesInputListGeneratedTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListGeneratedTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListGeneratedTemplates.html#CloudFormation.Paginator.ListGeneratedTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listgeneratedtemplatespaginator)
        """


class ListImportsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListImports.html#CloudFormation.Paginator.ListImports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listimportspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListImportsInputListImportsPaginateTypeDef]
    ) -> _PageIterator[ListImportsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListImports.html#CloudFormation.Paginator.ListImports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listimportspaginator)
        """


class ListResourceScanRelatedResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScanRelatedResources.html#CloudFormation.Paginator.ListResourceScanRelatedResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listresourcescanrelatedresourcespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResourceScanRelatedResourcesInputListResourceScanRelatedResourcesPaginateTypeDef
        ],
    ) -> _PageIterator[ListResourceScanRelatedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScanRelatedResources.html#CloudFormation.Paginator.ListResourceScanRelatedResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listresourcescanrelatedresourcespaginator)
        """


class ListResourceScanResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScanResources.html#CloudFormation.Paginator.ListResourceScanResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listresourcescanresourcespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListResourceScanResourcesInputListResourceScanResourcesPaginateTypeDef],
    ) -> _PageIterator[ListResourceScanResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScanResources.html#CloudFormation.Paginator.ListResourceScanResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listresourcescanresourcespaginator)
        """


class ListResourceScansPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScans.html#CloudFormation.Paginator.ListResourceScans)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listresourcescanspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResourceScansInputListResourceScansPaginateTypeDef]
    ) -> _PageIterator[ListResourceScansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScans.html#CloudFormation.Paginator.ListResourceScans.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listresourcescanspaginator)
        """


class ListStackInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackInstances.html#CloudFormation.Paginator.ListStackInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#liststackinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStackInstancesInputListStackInstancesPaginateTypeDef]
    ) -> _PageIterator[ListStackInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackInstances.html#CloudFormation.Paginator.ListStackInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#liststackinstancespaginator)
        """


class ListStackResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackResources.html#CloudFormation.Paginator.ListStackResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#liststackresourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStackResourcesInputListStackResourcesPaginateTypeDef]
    ) -> _PageIterator[ListStackResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackResources.html#CloudFormation.Paginator.ListStackResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#liststackresourcespaginator)
        """


class ListStackSetOperationResultsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSetOperationResults.html#CloudFormation.Paginator.ListStackSetOperationResults)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#liststacksetoperationresultspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListStackSetOperationResultsInputListStackSetOperationResultsPaginateTypeDef
        ],
    ) -> _PageIterator[ListStackSetOperationResultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSetOperationResults.html#CloudFormation.Paginator.ListStackSetOperationResults.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#liststacksetoperationresultspaginator)
        """


class ListStackSetOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSetOperations.html#CloudFormation.Paginator.ListStackSetOperations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#liststacksetoperationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStackSetOperationsInputListStackSetOperationsPaginateTypeDef]
    ) -> _PageIterator[ListStackSetOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSetOperations.html#CloudFormation.Paginator.ListStackSetOperations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#liststacksetoperationspaginator)
        """


class ListStackSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSets.html#CloudFormation.Paginator.ListStackSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#liststacksetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStackSetsInputListStackSetsPaginateTypeDef]
    ) -> _PageIterator[ListStackSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSets.html#CloudFormation.Paginator.ListStackSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#liststacksetspaginator)
        """


class ListStacksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStacks.html#CloudFormation.Paginator.ListStacks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#liststackspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStacksInputListStacksPaginateTypeDef]
    ) -> _PageIterator[ListStacksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStacks.html#CloudFormation.Paginator.ListStacks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#liststackspaginator)
        """


class ListTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListTypes.html#CloudFormation.Paginator.ListTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listtypespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTypesInputListTypesPaginateTypeDef]
    ) -> _PageIterator[ListTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListTypes.html#CloudFormation.Paginator.ListTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/paginators/#listtypespaginator)
        """
