"""
Type annotations for geo-places service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_geo_places.client import LocationServicePlacesV2Client

    session = Session()
    client: LocationServicePlacesV2Client = session.client("geo-places")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    AutocompleteRequestRequestTypeDef,
    AutocompleteResponseTypeDef,
    GeocodeRequestRequestTypeDef,
    GeocodeResponseTypeDef,
    GetPlaceRequestRequestTypeDef,
    GetPlaceResponseTypeDef,
    ReverseGeocodeRequestRequestTypeDef,
    ReverseGeocodeResponseTypeDef,
    SearchNearbyRequestRequestTypeDef,
    SearchNearbyResponseTypeDef,
    SearchTextRequestRequestTypeDef,
    SearchTextResponseTypeDef,
    SuggestRequestRequestTypeDef,
    SuggestResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("LocationServicePlacesV2Client",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class LocationServicePlacesV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LocationServicePlacesV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#close)
        """

    def autocomplete(
        self, **kwargs: Unpack[AutocompleteRequestRequestTypeDef]
    ) -> AutocompleteResponseTypeDef:
        """
        The autocomplete operation speeds up and increases the accuracy of entering
        addresses by providing a list of address candidates matching a partially
        entered address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/autocomplete.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#autocomplete)
        """

    def geocode(self, **kwargs: Unpack[GeocodeRequestRequestTypeDef]) -> GeocodeResponseTypeDef:
        """
        The <code>Geocode</code> action allows you to obtain coordinates, addresses,
        and other information about places.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/geocode.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#geocode)
        """

    def get_place(self, **kwargs: Unpack[GetPlaceRequestRequestTypeDef]) -> GetPlaceResponseTypeDef:
        """
        Finds a place by its unique ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/get_place.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#get_place)
        """

    def reverse_geocode(
        self, **kwargs: Unpack[ReverseGeocodeRequestRequestTypeDef]
    ) -> ReverseGeocodeResponseTypeDef:
        """
        The <code>ReverseGeocode</code> operation allows you to retrieve addresses and
        place information from coordinates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/reverse_geocode.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#reverse_geocode)
        """

    def search_nearby(
        self, **kwargs: Unpack[SearchNearbyRequestRequestTypeDef]
    ) -> SearchNearbyResponseTypeDef:
        """
        Search nearby a specified location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/search_nearby.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#search_nearby)
        """

    def search_text(
        self, **kwargs: Unpack[SearchTextRequestRequestTypeDef]
    ) -> SearchTextResponseTypeDef:
        """
        Use the <code>SearchText</code> operation to search for geocode and place
        information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/search_text.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#search_text)
        """

    def suggest(self, **kwargs: Unpack[SuggestRequestRequestTypeDef]) -> SuggestResponseTypeDef:
        """
        The <code>Suggest</code> operation finds addresses or place candidates based on
        incomplete or misspelled queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/suggest.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/client/#suggest)
        """
