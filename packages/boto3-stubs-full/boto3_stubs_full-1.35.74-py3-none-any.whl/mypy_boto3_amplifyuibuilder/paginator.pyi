"""
Type annotations for amplifyuibuilder service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_amplifyuibuilder.client import AmplifyUIBuilderClient
    from mypy_boto3_amplifyuibuilder.paginator import (
        ExportComponentsPaginator,
        ExportFormsPaginator,
        ExportThemesPaginator,
        ListCodegenJobsPaginator,
        ListComponentsPaginator,
        ListFormsPaginator,
        ListThemesPaginator,
    )

    session = Session()
    client: AmplifyUIBuilderClient = session.client("amplifyuibuilder")

    export_components_paginator: ExportComponentsPaginator = client.get_paginator("export_components")
    export_forms_paginator: ExportFormsPaginator = client.get_paginator("export_forms")
    export_themes_paginator: ExportThemesPaginator = client.get_paginator("export_themes")
    list_codegen_jobs_paginator: ListCodegenJobsPaginator = client.get_paginator("list_codegen_jobs")
    list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
    list_forms_paginator: ListFormsPaginator = client.get_paginator("list_forms")
    list_themes_paginator: ListThemesPaginator = client.get_paginator("list_themes")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ExportComponentsRequestExportComponentsPaginateTypeDef,
    ExportComponentsResponsePaginatorTypeDef,
    ExportFormsRequestExportFormsPaginateTypeDef,
    ExportFormsResponsePaginatorTypeDef,
    ExportThemesRequestExportThemesPaginateTypeDef,
    ExportThemesResponsePaginatorTypeDef,
    ListCodegenJobsRequestListCodegenJobsPaginateTypeDef,
    ListCodegenJobsResponseTypeDef,
    ListComponentsRequestListComponentsPaginateTypeDef,
    ListComponentsResponseTypeDef,
    ListFormsRequestListFormsPaginateTypeDef,
    ListFormsResponseTypeDef,
    ListThemesRequestListThemesPaginateTypeDef,
    ListThemesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ExportComponentsPaginator",
    "ExportFormsPaginator",
    "ExportThemesPaginator",
    "ListCodegenJobsPaginator",
    "ListComponentsPaginator",
    "ListFormsPaginator",
    "ListThemesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ExportComponentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportComponents.html#AmplifyUIBuilder.Paginator.ExportComponents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#exportcomponentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ExportComponentsRequestExportComponentsPaginateTypeDef]
    ) -> _PageIterator[ExportComponentsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportComponents.html#AmplifyUIBuilder.Paginator.ExportComponents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#exportcomponentspaginator)
        """

class ExportFormsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportForms.html#AmplifyUIBuilder.Paginator.ExportForms)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#exportformspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ExportFormsRequestExportFormsPaginateTypeDef]
    ) -> _PageIterator[ExportFormsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportForms.html#AmplifyUIBuilder.Paginator.ExportForms.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#exportformspaginator)
        """

class ExportThemesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportThemes.html#AmplifyUIBuilder.Paginator.ExportThemes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#exportthemespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ExportThemesRequestExportThemesPaginateTypeDef]
    ) -> _PageIterator[ExportThemesResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportThemes.html#AmplifyUIBuilder.Paginator.ExportThemes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#exportthemespaginator)
        """

class ListCodegenJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListCodegenJobs.html#AmplifyUIBuilder.Paginator.ListCodegenJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#listcodegenjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCodegenJobsRequestListCodegenJobsPaginateTypeDef]
    ) -> _PageIterator[ListCodegenJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListCodegenJobs.html#AmplifyUIBuilder.Paginator.ListCodegenJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#listcodegenjobspaginator)
        """

class ListComponentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListComponents.html#AmplifyUIBuilder.Paginator.ListComponents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#listcomponentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListComponentsRequestListComponentsPaginateTypeDef]
    ) -> _PageIterator[ListComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListComponents.html#AmplifyUIBuilder.Paginator.ListComponents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#listcomponentspaginator)
        """

class ListFormsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListForms.html#AmplifyUIBuilder.Paginator.ListForms)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#listformspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFormsRequestListFormsPaginateTypeDef]
    ) -> _PageIterator[ListFormsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListForms.html#AmplifyUIBuilder.Paginator.ListForms.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#listformspaginator)
        """

class ListThemesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListThemes.html#AmplifyUIBuilder.Paginator.ListThemes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#listthemespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThemesRequestListThemesPaginateTypeDef]
    ) -> _PageIterator[ListThemesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListThemes.html#AmplifyUIBuilder.Paginator.ListThemes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/paginators/#listthemespaginator)
        """
