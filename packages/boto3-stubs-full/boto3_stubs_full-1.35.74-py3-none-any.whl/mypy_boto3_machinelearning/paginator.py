"""
Type annotations for machinelearning service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_machinelearning.client import MachineLearningClient
    from mypy_boto3_machinelearning.paginator import (
        DescribeBatchPredictionsPaginator,
        DescribeDataSourcesPaginator,
        DescribeEvaluationsPaginator,
        DescribeMLModelsPaginator,
    )

    session = Session()
    client: MachineLearningClient = session.client("machinelearning")

    describe_batch_predictions_paginator: DescribeBatchPredictionsPaginator = client.get_paginator("describe_batch_predictions")
    describe_data_sources_paginator: DescribeDataSourcesPaginator = client.get_paginator("describe_data_sources")
    describe_evaluations_paginator: DescribeEvaluationsPaginator = client.get_paginator("describe_evaluations")
    describe_ml_models_paginator: DescribeMLModelsPaginator = client.get_paginator("describe_ml_models")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeBatchPredictionsInputDescribeBatchPredictionsPaginateTypeDef,
    DescribeBatchPredictionsOutputTypeDef,
    DescribeDataSourcesInputDescribeDataSourcesPaginateTypeDef,
    DescribeDataSourcesOutputTypeDef,
    DescribeEvaluationsInputDescribeEvaluationsPaginateTypeDef,
    DescribeEvaluationsOutputTypeDef,
    DescribeMLModelsInputDescribeMLModelsPaginateTypeDef,
    DescribeMLModelsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeBatchPredictionsPaginator",
    "DescribeDataSourcesPaginator",
    "DescribeEvaluationsPaginator",
    "DescribeMLModelsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeBatchPredictionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/paginator/DescribeBatchPredictions.html#MachineLearning.Paginator.DescribeBatchPredictions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describebatchpredictionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeBatchPredictionsInputDescribeBatchPredictionsPaginateTypeDef]
    ) -> _PageIterator[DescribeBatchPredictionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/paginator/DescribeBatchPredictions.html#MachineLearning.Paginator.DescribeBatchPredictions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describebatchpredictionspaginator)
        """


class DescribeDataSourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/paginator/DescribeDataSources.html#MachineLearning.Paginator.DescribeDataSources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describedatasourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeDataSourcesInputDescribeDataSourcesPaginateTypeDef]
    ) -> _PageIterator[DescribeDataSourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/paginator/DescribeDataSources.html#MachineLearning.Paginator.DescribeDataSources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describedatasourcespaginator)
        """


class DescribeEvaluationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/paginator/DescribeEvaluations.html#MachineLearning.Paginator.DescribeEvaluations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describeevaluationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeEvaluationsInputDescribeEvaluationsPaginateTypeDef]
    ) -> _PageIterator[DescribeEvaluationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/paginator/DescribeEvaluations.html#MachineLearning.Paginator.DescribeEvaluations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describeevaluationspaginator)
        """


class DescribeMLModelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/paginator/DescribeMLModels.html#MachineLearning.Paginator.DescribeMLModels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describemlmodelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeMLModelsInputDescribeMLModelsPaginateTypeDef]
    ) -> _PageIterator[DescribeMLModelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning/paginator/DescribeMLModels.html#MachineLearning.Paginator.DescribeMLModels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_machinelearning/paginators/#describemlmodelspaginator)
        """
