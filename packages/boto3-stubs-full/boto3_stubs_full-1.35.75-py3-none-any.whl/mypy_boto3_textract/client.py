"""
Type annotations for textract service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_textract.client import TextractClient

    session = Session()
    client: TextractClient = session.client("textract")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListAdaptersPaginator, ListAdapterVersionsPaginator
from .type_defs import (
    AnalyzeDocumentRequestRequestTypeDef,
    AnalyzeDocumentResponseTypeDef,
    AnalyzeExpenseRequestRequestTypeDef,
    AnalyzeExpenseResponseTypeDef,
    AnalyzeIDRequestRequestTypeDef,
    AnalyzeIDResponseTypeDef,
    CreateAdapterRequestRequestTypeDef,
    CreateAdapterResponseTypeDef,
    CreateAdapterVersionRequestRequestTypeDef,
    CreateAdapterVersionResponseTypeDef,
    DeleteAdapterRequestRequestTypeDef,
    DeleteAdapterVersionRequestRequestTypeDef,
    DetectDocumentTextRequestRequestTypeDef,
    DetectDocumentTextResponseTypeDef,
    GetAdapterRequestRequestTypeDef,
    GetAdapterResponseTypeDef,
    GetAdapterVersionRequestRequestTypeDef,
    GetAdapterVersionResponseTypeDef,
    GetDocumentAnalysisRequestRequestTypeDef,
    GetDocumentAnalysisResponseTypeDef,
    GetDocumentTextDetectionRequestRequestTypeDef,
    GetDocumentTextDetectionResponseTypeDef,
    GetExpenseAnalysisRequestRequestTypeDef,
    GetExpenseAnalysisResponseTypeDef,
    GetLendingAnalysisRequestRequestTypeDef,
    GetLendingAnalysisResponseTypeDef,
    GetLendingAnalysisSummaryRequestRequestTypeDef,
    GetLendingAnalysisSummaryResponseTypeDef,
    ListAdaptersRequestRequestTypeDef,
    ListAdaptersResponseTypeDef,
    ListAdapterVersionsRequestRequestTypeDef,
    ListAdapterVersionsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartDocumentAnalysisRequestRequestTypeDef,
    StartDocumentAnalysisResponseTypeDef,
    StartDocumentTextDetectionRequestRequestTypeDef,
    StartDocumentTextDetectionResponseTypeDef,
    StartExpenseAnalysisRequestRequestTypeDef,
    StartExpenseAnalysisResponseTypeDef,
    StartLendingAnalysisRequestRequestTypeDef,
    StartLendingAnalysisResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAdapterRequestRequestTypeDef,
    UpdateAdapterResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("TextractClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadDocumentException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DocumentTooLargeException: Type[BotocoreClientError]
    HumanLoopQuotaExceededException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidJobIdException: Type[BotocoreClientError]
    InvalidKMSKeyException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidS3ObjectException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ProvisionedThroughputExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnsupportedDocumentException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class TextractClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TextractClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#close)
        """

    def analyze_document(
        self, **kwargs: Unpack[AnalyzeDocumentRequestRequestTypeDef]
    ) -> AnalyzeDocumentResponseTypeDef:
        """
        Analyzes an input document for relationships between detected items.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/analyze_document.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#analyze_document)
        """

    def analyze_expense(
        self, **kwargs: Unpack[AnalyzeExpenseRequestRequestTypeDef]
    ) -> AnalyzeExpenseResponseTypeDef:
        """
        <code>AnalyzeExpense</code> synchronously analyzes an input document for
        financially related relationships between text.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/analyze_expense.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#analyze_expense)
        """

    def analyze_id(
        self, **kwargs: Unpack[AnalyzeIDRequestRequestTypeDef]
    ) -> AnalyzeIDResponseTypeDef:
        """
        Analyzes identity documents for relevant information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/analyze_id.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#analyze_id)
        """

    def create_adapter(
        self, **kwargs: Unpack[CreateAdapterRequestRequestTypeDef]
    ) -> CreateAdapterResponseTypeDef:
        """
        Creates an adapter, which can be fine-tuned for enhanced performance on user
        provided documents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/create_adapter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#create_adapter)
        """

    def create_adapter_version(
        self, **kwargs: Unpack[CreateAdapterVersionRequestRequestTypeDef]
    ) -> CreateAdapterVersionResponseTypeDef:
        """
        Creates a new version of an adapter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/create_adapter_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#create_adapter_version)
        """

    def delete_adapter(
        self, **kwargs: Unpack[DeleteAdapterRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Textract adapter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/delete_adapter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#delete_adapter)
        """

    def delete_adapter_version(
        self, **kwargs: Unpack[DeleteAdapterVersionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Textract adapter version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/delete_adapter_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#delete_adapter_version)
        """

    def detect_document_text(
        self, **kwargs: Unpack[DetectDocumentTextRequestRequestTypeDef]
    ) -> DetectDocumentTextResponseTypeDef:
        """
        Detects text in the input document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/detect_document_text.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#detect_document_text)
        """

    def get_adapter(
        self, **kwargs: Unpack[GetAdapterRequestRequestTypeDef]
    ) -> GetAdapterResponseTypeDef:
        """
        Gets configuration information for an adapter specified by an AdapterId,
        returning information on AdapterName, Description, CreationTime, AutoUpdate
        status, and FeatureTypes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/get_adapter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_adapter)
        """

    def get_adapter_version(
        self, **kwargs: Unpack[GetAdapterVersionRequestRequestTypeDef]
    ) -> GetAdapterVersionResponseTypeDef:
        """
        Gets configuration information for the specified adapter version, including:
        AdapterId, AdapterVersion, FeatureTypes, Status, StatusMessage, DatasetConfig,
        KMSKeyId, OutputConfig, Tags and EvaluationMetrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/get_adapter_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_adapter_version)
        """

    def get_document_analysis(
        self, **kwargs: Unpack[GetDocumentAnalysisRequestRequestTypeDef]
    ) -> GetDocumentAnalysisResponseTypeDef:
        """
        Gets the results for an Amazon Textract asynchronous operation that analyzes
        text in a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/get_document_analysis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_document_analysis)
        """

    def get_document_text_detection(
        self, **kwargs: Unpack[GetDocumentTextDetectionRequestRequestTypeDef]
    ) -> GetDocumentTextDetectionResponseTypeDef:
        """
        Gets the results for an Amazon Textract asynchronous operation that detects
        text in a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/get_document_text_detection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_document_text_detection)
        """

    def get_expense_analysis(
        self, **kwargs: Unpack[GetExpenseAnalysisRequestRequestTypeDef]
    ) -> GetExpenseAnalysisResponseTypeDef:
        """
        Gets the results for an Amazon Textract asynchronous operation that analyzes
        invoices and receipts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/get_expense_analysis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_expense_analysis)
        """

    def get_lending_analysis(
        self, **kwargs: Unpack[GetLendingAnalysisRequestRequestTypeDef]
    ) -> GetLendingAnalysisResponseTypeDef:
        """
        Gets the results for an Amazon Textract asynchronous operation that analyzes
        text in a lending document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/get_lending_analysis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_lending_analysis)
        """

    def get_lending_analysis_summary(
        self, **kwargs: Unpack[GetLendingAnalysisSummaryRequestRequestTypeDef]
    ) -> GetLendingAnalysisSummaryResponseTypeDef:
        """
        Gets summarized results for the <code>StartLendingAnalysis</code> operation,
        which analyzes text in a lending document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/get_lending_analysis_summary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_lending_analysis_summary)
        """

    def list_adapter_versions(
        self, **kwargs: Unpack[ListAdapterVersionsRequestRequestTypeDef]
    ) -> ListAdapterVersionsResponseTypeDef:
        """
        List all version of an adapter that meet the specified filtration criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/list_adapter_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#list_adapter_versions)
        """

    def list_adapters(
        self, **kwargs: Unpack[ListAdaptersRequestRequestTypeDef]
    ) -> ListAdaptersResponseTypeDef:
        """
        Lists all adapters that match the specified filtration criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/list_adapters.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#list_adapters)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags for an Amazon Textract resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#list_tags_for_resource)
        """

    def start_document_analysis(
        self, **kwargs: Unpack[StartDocumentAnalysisRequestRequestTypeDef]
    ) -> StartDocumentAnalysisResponseTypeDef:
        """
        Starts the asynchronous analysis of an input document for relationships between
        detected items such as key-value pairs, tables, and selection elements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/start_document_analysis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#start_document_analysis)
        """

    def start_document_text_detection(
        self, **kwargs: Unpack[StartDocumentTextDetectionRequestRequestTypeDef]
    ) -> StartDocumentTextDetectionResponseTypeDef:
        """
        Starts the asynchronous detection of text in a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/start_document_text_detection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#start_document_text_detection)
        """

    def start_expense_analysis(
        self, **kwargs: Unpack[StartExpenseAnalysisRequestRequestTypeDef]
    ) -> StartExpenseAnalysisResponseTypeDef:
        """
        Starts the asynchronous analysis of invoices or receipts for data like contact
        information, items purchased, and vendor names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/start_expense_analysis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#start_expense_analysis)
        """

    def start_lending_analysis(
        self, **kwargs: Unpack[StartLendingAnalysisRequestRequestTypeDef]
    ) -> StartLendingAnalysisResponseTypeDef:
        """
        Starts the classification and analysis of an input document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/start_lending_analysis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#start_lending_analysis)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes any tags with the specified keys from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#untag_resource)
        """

    def update_adapter(
        self, **kwargs: Unpack[UpdateAdapterRequestRequestTypeDef]
    ) -> UpdateAdapterResponseTypeDef:
        """
        Update the configuration for an adapter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/update_adapter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#update_adapter)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_adapter_versions"]
    ) -> ListAdapterVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_adapters"]) -> ListAdaptersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_paginator)
        """
