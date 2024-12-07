"""
Type annotations for inspector service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_inspector.client import InspectorClient
    from mypy_boto3_inspector.paginator import (
        ListAssessmentRunAgentsPaginator,
        ListAssessmentRunsPaginator,
        ListAssessmentTargetsPaginator,
        ListAssessmentTemplatesPaginator,
        ListEventSubscriptionsPaginator,
        ListExclusionsPaginator,
        ListFindingsPaginator,
        ListRulesPackagesPaginator,
        PreviewAgentsPaginator,
    )

    session = Session()
    client: InspectorClient = session.client("inspector")

    list_assessment_run_agents_paginator: ListAssessmentRunAgentsPaginator = client.get_paginator("list_assessment_run_agents")
    list_assessment_runs_paginator: ListAssessmentRunsPaginator = client.get_paginator("list_assessment_runs")
    list_assessment_targets_paginator: ListAssessmentTargetsPaginator = client.get_paginator("list_assessment_targets")
    list_assessment_templates_paginator: ListAssessmentTemplatesPaginator = client.get_paginator("list_assessment_templates")
    list_event_subscriptions_paginator: ListEventSubscriptionsPaginator = client.get_paginator("list_event_subscriptions")
    list_exclusions_paginator: ListExclusionsPaginator = client.get_paginator("list_exclusions")
    list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
    list_rules_packages_paginator: ListRulesPackagesPaginator = client.get_paginator("list_rules_packages")
    preview_agents_paginator: PreviewAgentsPaginator = client.get_paginator("preview_agents")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAssessmentRunAgentsRequestListAssessmentRunAgentsPaginateTypeDef,
    ListAssessmentRunAgentsResponseTypeDef,
    ListAssessmentRunsRequestListAssessmentRunsPaginateTypeDef,
    ListAssessmentRunsResponseTypeDef,
    ListAssessmentTargetsRequestListAssessmentTargetsPaginateTypeDef,
    ListAssessmentTargetsResponseTypeDef,
    ListAssessmentTemplatesRequestListAssessmentTemplatesPaginateTypeDef,
    ListAssessmentTemplatesResponseTypeDef,
    ListEventSubscriptionsRequestListEventSubscriptionsPaginateTypeDef,
    ListEventSubscriptionsResponseTypeDef,
    ListExclusionsRequestListExclusionsPaginateTypeDef,
    ListExclusionsResponseTypeDef,
    ListFindingsRequestListFindingsPaginateTypeDef,
    ListFindingsResponseTypeDef,
    ListRulesPackagesRequestListRulesPackagesPaginateTypeDef,
    ListRulesPackagesResponseTypeDef,
    PreviewAgentsRequestPreviewAgentsPaginateTypeDef,
    PreviewAgentsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAssessmentRunAgentsPaginator",
    "ListAssessmentRunsPaginator",
    "ListAssessmentTargetsPaginator",
    "ListAssessmentTemplatesPaginator",
    "ListEventSubscriptionsPaginator",
    "ListExclusionsPaginator",
    "ListFindingsPaginator",
    "ListRulesPackagesPaginator",
    "PreviewAgentsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAssessmentRunAgentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentRunAgents.html#Inspector.Paginator.ListAssessmentRunAgents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listassessmentrunagentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAssessmentRunAgentsRequestListAssessmentRunAgentsPaginateTypeDef]
    ) -> _PageIterator[ListAssessmentRunAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentRunAgents.html#Inspector.Paginator.ListAssessmentRunAgents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listassessmentrunagentspaginator)
        """

class ListAssessmentRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentRuns.html#Inspector.Paginator.ListAssessmentRuns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listassessmentrunspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAssessmentRunsRequestListAssessmentRunsPaginateTypeDef]
    ) -> _PageIterator[ListAssessmentRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentRuns.html#Inspector.Paginator.ListAssessmentRuns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listassessmentrunspaginator)
        """

class ListAssessmentTargetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentTargets.html#Inspector.Paginator.ListAssessmentTargets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listassessmenttargetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAssessmentTargetsRequestListAssessmentTargetsPaginateTypeDef]
    ) -> _PageIterator[ListAssessmentTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentTargets.html#Inspector.Paginator.ListAssessmentTargets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listassessmenttargetspaginator)
        """

class ListAssessmentTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentTemplates.html#Inspector.Paginator.ListAssessmentTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listassessmenttemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAssessmentTemplatesRequestListAssessmentTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListAssessmentTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentTemplates.html#Inspector.Paginator.ListAssessmentTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listassessmenttemplatespaginator)
        """

class ListEventSubscriptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListEventSubscriptions.html#Inspector.Paginator.ListEventSubscriptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listeventsubscriptionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEventSubscriptionsRequestListEventSubscriptionsPaginateTypeDef]
    ) -> _PageIterator[ListEventSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListEventSubscriptions.html#Inspector.Paginator.ListEventSubscriptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listeventsubscriptionspaginator)
        """

class ListExclusionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListExclusions.html#Inspector.Paginator.ListExclusions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listexclusionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListExclusionsRequestListExclusionsPaginateTypeDef]
    ) -> _PageIterator[ListExclusionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListExclusions.html#Inspector.Paginator.ListExclusions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listexclusionspaginator)
        """

class ListFindingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListFindings.html#Inspector.Paginator.ListFindings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listfindingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFindingsRequestListFindingsPaginateTypeDef]
    ) -> _PageIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListFindings.html#Inspector.Paginator.ListFindings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listfindingspaginator)
        """

class ListRulesPackagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListRulesPackages.html#Inspector.Paginator.ListRulesPackages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listrulespackagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRulesPackagesRequestListRulesPackagesPaginateTypeDef]
    ) -> _PageIterator[ListRulesPackagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListRulesPackages.html#Inspector.Paginator.ListRulesPackages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#listrulespackagespaginator)
        """

class PreviewAgentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/PreviewAgents.html#Inspector.Paginator.PreviewAgents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#previewagentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[PreviewAgentsRequestPreviewAgentsPaginateTypeDef]
    ) -> _PageIterator[PreviewAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/PreviewAgents.html#Inspector.Paginator.PreviewAgents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector/paginators/#previewagentspaginator)
        """
