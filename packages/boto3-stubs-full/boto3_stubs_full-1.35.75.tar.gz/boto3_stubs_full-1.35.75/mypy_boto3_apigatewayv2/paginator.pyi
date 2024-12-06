"""
Type annotations for apigatewayv2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_apigatewayv2.client import ApiGatewayV2Client
    from mypy_boto3_apigatewayv2.paginator import (
        GetApisPaginator,
        GetAuthorizersPaginator,
        GetDeploymentsPaginator,
        GetDomainNamesPaginator,
        GetIntegrationResponsesPaginator,
        GetIntegrationsPaginator,
        GetModelsPaginator,
        GetRouteResponsesPaginator,
        GetRoutesPaginator,
        GetStagesPaginator,
    )

    session = Session()
    client: ApiGatewayV2Client = session.client("apigatewayv2")

    get_apis_paginator: GetApisPaginator = client.get_paginator("get_apis")
    get_authorizers_paginator: GetAuthorizersPaginator = client.get_paginator("get_authorizers")
    get_deployments_paginator: GetDeploymentsPaginator = client.get_paginator("get_deployments")
    get_domain_names_paginator: GetDomainNamesPaginator = client.get_paginator("get_domain_names")
    get_integration_responses_paginator: GetIntegrationResponsesPaginator = client.get_paginator("get_integration_responses")
    get_integrations_paginator: GetIntegrationsPaginator = client.get_paginator("get_integrations")
    get_models_paginator: GetModelsPaginator = client.get_paginator("get_models")
    get_route_responses_paginator: GetRouteResponsesPaginator = client.get_paginator("get_route_responses")
    get_routes_paginator: GetRoutesPaginator = client.get_paginator("get_routes")
    get_stages_paginator: GetStagesPaginator = client.get_paginator("get_stages")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetApisRequestGetApisPaginateTypeDef,
    GetApisResponseTypeDef,
    GetAuthorizersRequestGetAuthorizersPaginateTypeDef,
    GetAuthorizersResponseTypeDef,
    GetDeploymentsRequestGetDeploymentsPaginateTypeDef,
    GetDeploymentsResponseTypeDef,
    GetDomainNamesRequestGetDomainNamesPaginateTypeDef,
    GetDomainNamesResponseTypeDef,
    GetIntegrationResponsesRequestGetIntegrationResponsesPaginateTypeDef,
    GetIntegrationResponsesResponseTypeDef,
    GetIntegrationsRequestGetIntegrationsPaginateTypeDef,
    GetIntegrationsResponseTypeDef,
    GetModelsRequestGetModelsPaginateTypeDef,
    GetModelsResponseTypeDef,
    GetRouteResponsesRequestGetRouteResponsesPaginateTypeDef,
    GetRouteResponsesResponseTypeDef,
    GetRoutesRequestGetRoutesPaginateTypeDef,
    GetRoutesResponseTypeDef,
    GetStagesRequestGetStagesPaginateTypeDef,
    GetStagesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetApisPaginator",
    "GetAuthorizersPaginator",
    "GetDeploymentsPaginator",
    "GetDomainNamesPaginator",
    "GetIntegrationResponsesPaginator",
    "GetIntegrationsPaginator",
    "GetModelsPaginator",
    "GetRouteResponsesPaginator",
    "GetRoutesPaginator",
    "GetStagesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetApisPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetApis.html#ApiGatewayV2.Paginator.GetApis)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getapispaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetApisRequestGetApisPaginateTypeDef]
    ) -> _PageIterator[GetApisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetApis.html#ApiGatewayV2.Paginator.GetApis.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getapispaginator)
        """

class GetAuthorizersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetAuthorizers.html#ApiGatewayV2.Paginator.GetAuthorizers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getauthorizerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetAuthorizersRequestGetAuthorizersPaginateTypeDef]
    ) -> _PageIterator[GetAuthorizersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetAuthorizers.html#ApiGatewayV2.Paginator.GetAuthorizers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getauthorizerspaginator)
        """

class GetDeploymentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetDeployments.html#ApiGatewayV2.Paginator.GetDeployments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getdeploymentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDeploymentsRequestGetDeploymentsPaginateTypeDef]
    ) -> _PageIterator[GetDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetDeployments.html#ApiGatewayV2.Paginator.GetDeployments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getdeploymentspaginator)
        """

class GetDomainNamesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetDomainNames.html#ApiGatewayV2.Paginator.GetDomainNames)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getdomainnamespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDomainNamesRequestGetDomainNamesPaginateTypeDef]
    ) -> _PageIterator[GetDomainNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetDomainNames.html#ApiGatewayV2.Paginator.GetDomainNames.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getdomainnamespaginator)
        """

class GetIntegrationResponsesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetIntegrationResponses.html#ApiGatewayV2.Paginator.GetIntegrationResponses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getintegrationresponsespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetIntegrationResponsesRequestGetIntegrationResponsesPaginateTypeDef]
    ) -> _PageIterator[GetIntegrationResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetIntegrationResponses.html#ApiGatewayV2.Paginator.GetIntegrationResponses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getintegrationresponsespaginator)
        """

class GetIntegrationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetIntegrations.html#ApiGatewayV2.Paginator.GetIntegrations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getintegrationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetIntegrationsRequestGetIntegrationsPaginateTypeDef]
    ) -> _PageIterator[GetIntegrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetIntegrations.html#ApiGatewayV2.Paginator.GetIntegrations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getintegrationspaginator)
        """

class GetModelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetModels.html#ApiGatewayV2.Paginator.GetModels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getmodelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetModelsRequestGetModelsPaginateTypeDef]
    ) -> _PageIterator[GetModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetModels.html#ApiGatewayV2.Paginator.GetModels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getmodelspaginator)
        """

class GetRouteResponsesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetRouteResponses.html#ApiGatewayV2.Paginator.GetRouteResponses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getrouteresponsespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetRouteResponsesRequestGetRouteResponsesPaginateTypeDef]
    ) -> _PageIterator[GetRouteResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetRouteResponses.html#ApiGatewayV2.Paginator.GetRouteResponses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getrouteresponsespaginator)
        """

class GetRoutesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetRoutes.html#ApiGatewayV2.Paginator.GetRoutes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getroutespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetRoutesRequestGetRoutesPaginateTypeDef]
    ) -> _PageIterator[GetRoutesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetRoutes.html#ApiGatewayV2.Paginator.GetRoutes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getroutespaginator)
        """

class GetStagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetStages.html#ApiGatewayV2.Paginator.GetStages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getstagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetStagesRequestGetStagesPaginateTypeDef]
    ) -> _PageIterator[GetStagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetStages.html#ApiGatewayV2.Paginator.GetStages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigatewayv2/paginators/#getstagespaginator)
        """
