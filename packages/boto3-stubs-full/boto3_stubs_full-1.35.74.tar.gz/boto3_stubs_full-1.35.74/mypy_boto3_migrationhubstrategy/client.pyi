"""
Type annotations for migrationhubstrategy service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_migrationhubstrategy.client import MigrationHubStrategyRecommendationsClient

    session = Session()
    client: MigrationHubStrategyRecommendationsClient = session.client("migrationhubstrategy")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetServerDetailsPaginator,
    ListAnalyzableServersPaginator,
    ListApplicationComponentsPaginator,
    ListCollectorsPaginator,
    ListImportFileTaskPaginator,
    ListServersPaginator,
)
from .type_defs import (
    GetApplicationComponentDetailsRequestRequestTypeDef,
    GetApplicationComponentDetailsResponseTypeDef,
    GetApplicationComponentStrategiesRequestRequestTypeDef,
    GetApplicationComponentStrategiesResponseTypeDef,
    GetAssessmentRequestRequestTypeDef,
    GetAssessmentResponseTypeDef,
    GetImportFileTaskRequestRequestTypeDef,
    GetImportFileTaskResponseTypeDef,
    GetLatestAssessmentIdResponseTypeDef,
    GetPortfolioPreferencesResponseTypeDef,
    GetPortfolioSummaryResponseTypeDef,
    GetRecommendationReportDetailsRequestRequestTypeDef,
    GetRecommendationReportDetailsResponseTypeDef,
    GetServerDetailsRequestRequestTypeDef,
    GetServerDetailsResponseTypeDef,
    GetServerStrategiesRequestRequestTypeDef,
    GetServerStrategiesResponseTypeDef,
    ListAnalyzableServersRequestRequestTypeDef,
    ListAnalyzableServersResponseTypeDef,
    ListApplicationComponentsRequestRequestTypeDef,
    ListApplicationComponentsResponseTypeDef,
    ListCollectorsRequestRequestTypeDef,
    ListCollectorsResponseTypeDef,
    ListImportFileTaskRequestRequestTypeDef,
    ListImportFileTaskResponseTypeDef,
    ListServersRequestRequestTypeDef,
    ListServersResponseTypeDef,
    PutPortfolioPreferencesRequestRequestTypeDef,
    StartAssessmentRequestRequestTypeDef,
    StartAssessmentResponseTypeDef,
    StartImportFileTaskRequestRequestTypeDef,
    StartImportFileTaskResponseTypeDef,
    StartRecommendationReportGenerationRequestRequestTypeDef,
    StartRecommendationReportGenerationResponseTypeDef,
    StopAssessmentRequestRequestTypeDef,
    UpdateApplicationComponentConfigRequestRequestTypeDef,
    UpdateServerConfigRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("MigrationHubStrategyRecommendationsClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DependencyException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceLinkedRoleLockClientException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class MigrationHubStrategyRecommendationsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MigrationHubStrategyRecommendationsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#close)
        """

    def get_application_component_details(
        self, **kwargs: Unpack[GetApplicationComponentDetailsRequestRequestTypeDef]
    ) -> GetApplicationComponentDetailsResponseTypeDef:
        """
        Retrieves details about an application component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_application_component_details.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_application_component_details)
        """

    def get_application_component_strategies(
        self, **kwargs: Unpack[GetApplicationComponentStrategiesRequestRequestTypeDef]
    ) -> GetApplicationComponentStrategiesResponseTypeDef:
        """
        Retrieves a list of all the recommended strategies and tools for an application
        component running on a server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_application_component_strategies.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_application_component_strategies)
        """

    def get_assessment(
        self, **kwargs: Unpack[GetAssessmentRequestRequestTypeDef]
    ) -> GetAssessmentResponseTypeDef:
        """
        Retrieves the status of an on-going assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_assessment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_assessment)
        """

    def get_import_file_task(
        self, **kwargs: Unpack[GetImportFileTaskRequestRequestTypeDef]
    ) -> GetImportFileTaskResponseTypeDef:
        """
        Retrieves the details about a specific import task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_import_file_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_import_file_task)
        """

    def get_latest_assessment_id(self) -> GetLatestAssessmentIdResponseTypeDef:
        """
        Retrieve the latest ID of a specific assessment task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_latest_assessment_id.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_latest_assessment_id)
        """

    def get_portfolio_preferences(self) -> GetPortfolioPreferencesResponseTypeDef:
        """
        Retrieves your migration and modernization preferences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_portfolio_preferences.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_portfolio_preferences)
        """

    def get_portfolio_summary(self) -> GetPortfolioSummaryResponseTypeDef:
        """
        Retrieves overall summary including the number of servers to rehost and the
        overall number of anti-patterns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_portfolio_summary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_portfolio_summary)
        """

    def get_recommendation_report_details(
        self, **kwargs: Unpack[GetRecommendationReportDetailsRequestRequestTypeDef]
    ) -> GetRecommendationReportDetailsResponseTypeDef:
        """
        Retrieves detailed information about the specified recommendation report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_recommendation_report_details.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_recommendation_report_details)
        """

    def get_server_details(
        self, **kwargs: Unpack[GetServerDetailsRequestRequestTypeDef]
    ) -> GetServerDetailsResponseTypeDef:
        """
        Retrieves detailed information about a specified server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_server_details.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_server_details)
        """

    def get_server_strategies(
        self, **kwargs: Unpack[GetServerStrategiesRequestRequestTypeDef]
    ) -> GetServerStrategiesResponseTypeDef:
        """
        Retrieves recommended strategies and tools for the specified server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_server_strategies.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_server_strategies)
        """

    def list_analyzable_servers(
        self, **kwargs: Unpack[ListAnalyzableServersRequestRequestTypeDef]
    ) -> ListAnalyzableServersResponseTypeDef:
        """
        Retrieves a list of all the servers fetched from customer vCenter using
        Strategy Recommendation Collector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/list_analyzable_servers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#list_analyzable_servers)
        """

    def list_application_components(
        self, **kwargs: Unpack[ListApplicationComponentsRequestRequestTypeDef]
    ) -> ListApplicationComponentsResponseTypeDef:
        """
        Retrieves a list of all the application components (processes).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/list_application_components.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#list_application_components)
        """

    def list_collectors(
        self, **kwargs: Unpack[ListCollectorsRequestRequestTypeDef]
    ) -> ListCollectorsResponseTypeDef:
        """
        Retrieves a list of all the installed collectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/list_collectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#list_collectors)
        """

    def list_import_file_task(
        self, **kwargs: Unpack[ListImportFileTaskRequestRequestTypeDef]
    ) -> ListImportFileTaskResponseTypeDef:
        """
        Retrieves a list of all the imports performed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/list_import_file_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#list_import_file_task)
        """

    def list_servers(
        self, **kwargs: Unpack[ListServersRequestRequestTypeDef]
    ) -> ListServersResponseTypeDef:
        """
        Returns a list of all the servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/list_servers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#list_servers)
        """

    def put_portfolio_preferences(
        self, **kwargs: Unpack[PutPortfolioPreferencesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Saves the specified migration and modernization preferences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/put_portfolio_preferences.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#put_portfolio_preferences)
        """

    def start_assessment(
        self, **kwargs: Unpack[StartAssessmentRequestRequestTypeDef]
    ) -> StartAssessmentResponseTypeDef:
        """
        Starts the assessment of an on-premises environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/start_assessment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#start_assessment)
        """

    def start_import_file_task(
        self, **kwargs: Unpack[StartImportFileTaskRequestRequestTypeDef]
    ) -> StartImportFileTaskResponseTypeDef:
        """
        Starts a file import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/start_import_file_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#start_import_file_task)
        """

    def start_recommendation_report_generation(
        self, **kwargs: Unpack[StartRecommendationReportGenerationRequestRequestTypeDef]
    ) -> StartRecommendationReportGenerationResponseTypeDef:
        """
        Starts generating a recommendation report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/start_recommendation_report_generation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#start_recommendation_report_generation)
        """

    def stop_assessment(
        self, **kwargs: Unpack[StopAssessmentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops the assessment of an on-premises environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/stop_assessment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#stop_assessment)
        """

    def update_application_component_config(
        self, **kwargs: Unpack[UpdateApplicationComponentConfigRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the configuration of an application component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/update_application_component_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#update_application_component_config)
        """

    def update_server_config(
        self, **kwargs: Unpack[UpdateServerConfigRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the configuration of the specified server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/update_server_config.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#update_server_config)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_server_details"]
    ) -> GetServerDetailsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_analyzable_servers"]
    ) -> ListAnalyzableServersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_application_components"]
    ) -> ListApplicationComponentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_collectors"]) -> ListCollectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_import_file_task"]
    ) -> ListImportFileTaskPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_servers"]) -> ListServersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhubstrategy/client/#get_paginator)
        """
