"""
Type annotations for elasticbeanstalk service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elasticbeanstalk.client import ElasticBeanstalkClient
    from mypy_boto3_elasticbeanstalk.paginator import (
        DescribeApplicationVersionsPaginator,
        DescribeEnvironmentManagedActionHistoryPaginator,
        DescribeEnvironmentsPaginator,
        DescribeEventsPaginator,
        ListPlatformVersionsPaginator,
    )

    session = Session()
    client: ElasticBeanstalkClient = session.client("elasticbeanstalk")

    describe_application_versions_paginator: DescribeApplicationVersionsPaginator = client.get_paginator("describe_application_versions")
    describe_environment_managed_action_history_paginator: DescribeEnvironmentManagedActionHistoryPaginator = client.get_paginator("describe_environment_managed_action_history")
    describe_environments_paginator: DescribeEnvironmentsPaginator = client.get_paginator("describe_environments")
    describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    list_platform_versions_paginator: ListPlatformVersionsPaginator = client.get_paginator("list_platform_versions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ApplicationVersionDescriptionsMessageTypeDef,
    DescribeApplicationVersionsMessageDescribeApplicationVersionsPaginateTypeDef,
    DescribeEnvironmentManagedActionHistoryRequestDescribeEnvironmentManagedActionHistoryPaginateTypeDef,
    DescribeEnvironmentManagedActionHistoryResultTypeDef,
    DescribeEnvironmentsMessageDescribeEnvironmentsPaginateTypeDef,
    DescribeEventsMessageDescribeEventsPaginateTypeDef,
    EnvironmentDescriptionsMessageTypeDef,
    EventDescriptionsMessageTypeDef,
    ListPlatformVersionsRequestListPlatformVersionsPaginateTypeDef,
    ListPlatformVersionsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeApplicationVersionsPaginator",
    "DescribeEnvironmentManagedActionHistoryPaginator",
    "DescribeEnvironmentsPaginator",
    "DescribeEventsPaginator",
    "ListPlatformVersionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeApplicationVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeApplicationVersions.html#ElasticBeanstalk.Paginator.DescribeApplicationVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/paginators/#describeapplicationversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeApplicationVersionsMessageDescribeApplicationVersionsPaginateTypeDef
        ],
    ) -> _PageIterator[ApplicationVersionDescriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeApplicationVersions.html#ElasticBeanstalk.Paginator.DescribeApplicationVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/paginators/#describeapplicationversionspaginator)
        """

class DescribeEnvironmentManagedActionHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeEnvironmentManagedActionHistory.html#ElasticBeanstalk.Paginator.DescribeEnvironmentManagedActionHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/paginators/#describeenvironmentmanagedactionhistorypaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEnvironmentManagedActionHistoryRequestDescribeEnvironmentManagedActionHistoryPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeEnvironmentManagedActionHistoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeEnvironmentManagedActionHistory.html#ElasticBeanstalk.Paginator.DescribeEnvironmentManagedActionHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/paginators/#describeenvironmentmanagedactionhistorypaginator)
        """

class DescribeEnvironmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeEnvironments.html#ElasticBeanstalk.Paginator.DescribeEnvironments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/paginators/#describeenvironmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEnvironmentsMessageDescribeEnvironmentsPaginateTypeDef]
    ) -> _PageIterator[EnvironmentDescriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeEnvironments.html#ElasticBeanstalk.Paginator.DescribeEnvironments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/paginators/#describeenvironmentspaginator)
        """

class DescribeEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeEvents.html#ElasticBeanstalk.Paginator.DescribeEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/paginators/#describeeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEventsMessageDescribeEventsPaginateTypeDef]
    ) -> _PageIterator[EventDescriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/DescribeEvents.html#ElasticBeanstalk.Paginator.DescribeEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/paginators/#describeeventspaginator)
        """

class ListPlatformVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/ListPlatformVersions.html#ElasticBeanstalk.Paginator.ListPlatformVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/paginators/#listplatformversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPlatformVersionsRequestListPlatformVersionsPaginateTypeDef]
    ) -> _PageIterator[ListPlatformVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk/paginator/ListPlatformVersions.html#ElasticBeanstalk.Paginator.ListPlatformVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/paginators/#listplatformversionspaginator)
        """
