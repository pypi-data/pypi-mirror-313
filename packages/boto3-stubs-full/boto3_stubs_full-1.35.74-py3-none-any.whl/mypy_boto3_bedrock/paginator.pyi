"""
Type annotations for bedrock service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_bedrock.client import BedrockClient
    from mypy_boto3_bedrock.paginator import (
        ListCustomModelsPaginator,
        ListEvaluationJobsPaginator,
        ListGuardrailsPaginator,
        ListImportedModelsPaginator,
        ListInferenceProfilesPaginator,
        ListModelCopyJobsPaginator,
        ListModelCustomizationJobsPaginator,
        ListModelImportJobsPaginator,
        ListModelInvocationJobsPaginator,
        ListProvisionedModelThroughputsPaginator,
    )

    session = Session()
    client: BedrockClient = session.client("bedrock")

    list_custom_models_paginator: ListCustomModelsPaginator = client.get_paginator("list_custom_models")
    list_evaluation_jobs_paginator: ListEvaluationJobsPaginator = client.get_paginator("list_evaluation_jobs")
    list_guardrails_paginator: ListGuardrailsPaginator = client.get_paginator("list_guardrails")
    list_imported_models_paginator: ListImportedModelsPaginator = client.get_paginator("list_imported_models")
    list_inference_profiles_paginator: ListInferenceProfilesPaginator = client.get_paginator("list_inference_profiles")
    list_model_copy_jobs_paginator: ListModelCopyJobsPaginator = client.get_paginator("list_model_copy_jobs")
    list_model_customization_jobs_paginator: ListModelCustomizationJobsPaginator = client.get_paginator("list_model_customization_jobs")
    list_model_import_jobs_paginator: ListModelImportJobsPaginator = client.get_paginator("list_model_import_jobs")
    list_model_invocation_jobs_paginator: ListModelInvocationJobsPaginator = client.get_paginator("list_model_invocation_jobs")
    list_provisioned_model_throughputs_paginator: ListProvisionedModelThroughputsPaginator = client.get_paginator("list_provisioned_model_throughputs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCustomModelsRequestListCustomModelsPaginateTypeDef,
    ListCustomModelsResponseTypeDef,
    ListEvaluationJobsRequestListEvaluationJobsPaginateTypeDef,
    ListEvaluationJobsResponseTypeDef,
    ListGuardrailsRequestListGuardrailsPaginateTypeDef,
    ListGuardrailsResponseTypeDef,
    ListImportedModelsRequestListImportedModelsPaginateTypeDef,
    ListImportedModelsResponseTypeDef,
    ListInferenceProfilesRequestListInferenceProfilesPaginateTypeDef,
    ListInferenceProfilesResponseTypeDef,
    ListModelCopyJobsRequestListModelCopyJobsPaginateTypeDef,
    ListModelCopyJobsResponseTypeDef,
    ListModelCustomizationJobsRequestListModelCustomizationJobsPaginateTypeDef,
    ListModelCustomizationJobsResponseTypeDef,
    ListModelImportJobsRequestListModelImportJobsPaginateTypeDef,
    ListModelImportJobsResponseTypeDef,
    ListModelInvocationJobsRequestListModelInvocationJobsPaginateTypeDef,
    ListModelInvocationJobsResponseTypeDef,
    ListProvisionedModelThroughputsRequestListProvisionedModelThroughputsPaginateTypeDef,
    ListProvisionedModelThroughputsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCustomModelsPaginator",
    "ListEvaluationJobsPaginator",
    "ListGuardrailsPaginator",
    "ListImportedModelsPaginator",
    "ListInferenceProfilesPaginator",
    "ListModelCopyJobsPaginator",
    "ListModelCustomizationJobsPaginator",
    "ListModelImportJobsPaginator",
    "ListModelInvocationJobsPaginator",
    "ListProvisionedModelThroughputsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCustomModelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListCustomModels.html#Bedrock.Paginator.ListCustomModels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listcustommodelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCustomModelsRequestListCustomModelsPaginateTypeDef]
    ) -> _PageIterator[ListCustomModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListCustomModels.html#Bedrock.Paginator.ListCustomModels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listcustommodelspaginator)
        """

class ListEvaluationJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListEvaluationJobs.html#Bedrock.Paginator.ListEvaluationJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listevaluationjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEvaluationJobsRequestListEvaluationJobsPaginateTypeDef]
    ) -> _PageIterator[ListEvaluationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListEvaluationJobs.html#Bedrock.Paginator.ListEvaluationJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listevaluationjobspaginator)
        """

class ListGuardrailsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListGuardrails.html#Bedrock.Paginator.ListGuardrails)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listguardrailspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGuardrailsRequestListGuardrailsPaginateTypeDef]
    ) -> _PageIterator[ListGuardrailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListGuardrails.html#Bedrock.Paginator.ListGuardrails.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listguardrailspaginator)
        """

class ListImportedModelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListImportedModels.html#Bedrock.Paginator.ListImportedModels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listimportedmodelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListImportedModelsRequestListImportedModelsPaginateTypeDef]
    ) -> _PageIterator[ListImportedModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListImportedModels.html#Bedrock.Paginator.ListImportedModels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listimportedmodelspaginator)
        """

class ListInferenceProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListInferenceProfiles.html#Bedrock.Paginator.ListInferenceProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listinferenceprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInferenceProfilesRequestListInferenceProfilesPaginateTypeDef]
    ) -> _PageIterator[ListInferenceProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListInferenceProfiles.html#Bedrock.Paginator.ListInferenceProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listinferenceprofilespaginator)
        """

class ListModelCopyJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelCopyJobs.html#Bedrock.Paginator.ListModelCopyJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listmodelcopyjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListModelCopyJobsRequestListModelCopyJobsPaginateTypeDef]
    ) -> _PageIterator[ListModelCopyJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelCopyJobs.html#Bedrock.Paginator.ListModelCopyJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listmodelcopyjobspaginator)
        """

class ListModelCustomizationJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelCustomizationJobs.html#Bedrock.Paginator.ListModelCustomizationJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listmodelcustomizationjobspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListModelCustomizationJobsRequestListModelCustomizationJobsPaginateTypeDef
        ],
    ) -> _PageIterator[ListModelCustomizationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelCustomizationJobs.html#Bedrock.Paginator.ListModelCustomizationJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listmodelcustomizationjobspaginator)
        """

class ListModelImportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelImportJobs.html#Bedrock.Paginator.ListModelImportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listmodelimportjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListModelImportJobsRequestListModelImportJobsPaginateTypeDef]
    ) -> _PageIterator[ListModelImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelImportJobs.html#Bedrock.Paginator.ListModelImportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listmodelimportjobspaginator)
        """

class ListModelInvocationJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelInvocationJobs.html#Bedrock.Paginator.ListModelInvocationJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listmodelinvocationjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListModelInvocationJobsRequestListModelInvocationJobsPaginateTypeDef]
    ) -> _PageIterator[ListModelInvocationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelInvocationJobs.html#Bedrock.Paginator.ListModelInvocationJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listmodelinvocationjobspaginator)
        """

class ListProvisionedModelThroughputsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListProvisionedModelThroughputs.html#Bedrock.Paginator.ListProvisionedModelThroughputs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listprovisionedmodelthroughputspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListProvisionedModelThroughputsRequestListProvisionedModelThroughputsPaginateTypeDef
        ],
    ) -> _PageIterator[ListProvisionedModelThroughputsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListProvisionedModelThroughputs.html#Bedrock.Paginator.ListProvisionedModelThroughputs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listprovisionedmodelthroughputspaginator)
        """
