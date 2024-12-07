"""
Type annotations for lex-models service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_lex_models.client import LexModelBuildingServiceClient
    from mypy_boto3_lex_models.paginator import (
        GetBotAliasesPaginator,
        GetBotChannelAssociationsPaginator,
        GetBotVersionsPaginator,
        GetBotsPaginator,
        GetBuiltinIntentsPaginator,
        GetBuiltinSlotTypesPaginator,
        GetIntentVersionsPaginator,
        GetIntentsPaginator,
        GetSlotTypeVersionsPaginator,
        GetSlotTypesPaginator,
    )

    session = Session()
    client: LexModelBuildingServiceClient = session.client("lex-models")

    get_bot_aliases_paginator: GetBotAliasesPaginator = client.get_paginator("get_bot_aliases")
    get_bot_channel_associations_paginator: GetBotChannelAssociationsPaginator = client.get_paginator("get_bot_channel_associations")
    get_bot_versions_paginator: GetBotVersionsPaginator = client.get_paginator("get_bot_versions")
    get_bots_paginator: GetBotsPaginator = client.get_paginator("get_bots")
    get_builtin_intents_paginator: GetBuiltinIntentsPaginator = client.get_paginator("get_builtin_intents")
    get_builtin_slot_types_paginator: GetBuiltinSlotTypesPaginator = client.get_paginator("get_builtin_slot_types")
    get_intent_versions_paginator: GetIntentVersionsPaginator = client.get_paginator("get_intent_versions")
    get_intents_paginator: GetIntentsPaginator = client.get_paginator("get_intents")
    get_slot_type_versions_paginator: GetSlotTypeVersionsPaginator = client.get_paginator("get_slot_type_versions")
    get_slot_types_paginator: GetSlotTypesPaginator = client.get_paginator("get_slot_types")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetBotAliasesRequestGetBotAliasesPaginateTypeDef,
    GetBotAliasesResponseTypeDef,
    GetBotChannelAssociationsRequestGetBotChannelAssociationsPaginateTypeDef,
    GetBotChannelAssociationsResponseTypeDef,
    GetBotsRequestGetBotsPaginateTypeDef,
    GetBotsResponseTypeDef,
    GetBotVersionsRequestGetBotVersionsPaginateTypeDef,
    GetBotVersionsResponseTypeDef,
    GetBuiltinIntentsRequestGetBuiltinIntentsPaginateTypeDef,
    GetBuiltinIntentsResponseTypeDef,
    GetBuiltinSlotTypesRequestGetBuiltinSlotTypesPaginateTypeDef,
    GetBuiltinSlotTypesResponseTypeDef,
    GetIntentsRequestGetIntentsPaginateTypeDef,
    GetIntentsResponseTypeDef,
    GetIntentVersionsRequestGetIntentVersionsPaginateTypeDef,
    GetIntentVersionsResponseTypeDef,
    GetSlotTypesRequestGetSlotTypesPaginateTypeDef,
    GetSlotTypesResponseTypeDef,
    GetSlotTypeVersionsRequestGetSlotTypeVersionsPaginateTypeDef,
    GetSlotTypeVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetBotAliasesPaginator",
    "GetBotChannelAssociationsPaginator",
    "GetBotVersionsPaginator",
    "GetBotsPaginator",
    "GetBuiltinIntentsPaginator",
    "GetBuiltinSlotTypesPaginator",
    "GetIntentVersionsPaginator",
    "GetIntentsPaginator",
    "GetSlotTypeVersionsPaginator",
    "GetSlotTypesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetBotAliasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBotAliases.html#LexModelBuildingService.Paginator.GetBotAliases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotaliasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetBotAliasesRequestGetBotAliasesPaginateTypeDef]
    ) -> _PageIterator[GetBotAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBotAliases.html#LexModelBuildingService.Paginator.GetBotAliases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotaliasespaginator)
        """


class GetBotChannelAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBotChannelAssociations.html#LexModelBuildingService.Paginator.GetBotChannelAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotchannelassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[GetBotChannelAssociationsRequestGetBotChannelAssociationsPaginateTypeDef],
    ) -> _PageIterator[GetBotChannelAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBotChannelAssociations.html#LexModelBuildingService.Paginator.GetBotChannelAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotchannelassociationspaginator)
        """


class GetBotVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBotVersions.html#LexModelBuildingService.Paginator.GetBotVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetBotVersionsRequestGetBotVersionsPaginateTypeDef]
    ) -> _PageIterator[GetBotVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBotVersions.html#LexModelBuildingService.Paginator.GetBotVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotversionspaginator)
        """


class GetBotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBots.html#LexModelBuildingService.Paginator.GetBots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetBotsRequestGetBotsPaginateTypeDef]
    ) -> _PageIterator[GetBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBots.html#LexModelBuildingService.Paginator.GetBots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotspaginator)
        """


class GetBuiltinIntentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBuiltinIntents.html#LexModelBuildingService.Paginator.GetBuiltinIntents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbuiltinintentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetBuiltinIntentsRequestGetBuiltinIntentsPaginateTypeDef]
    ) -> _PageIterator[GetBuiltinIntentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBuiltinIntents.html#LexModelBuildingService.Paginator.GetBuiltinIntents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbuiltinintentspaginator)
        """


class GetBuiltinSlotTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBuiltinSlotTypes.html#LexModelBuildingService.Paginator.GetBuiltinSlotTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbuiltinslottypespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetBuiltinSlotTypesRequestGetBuiltinSlotTypesPaginateTypeDef]
    ) -> _PageIterator[GetBuiltinSlotTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBuiltinSlotTypes.html#LexModelBuildingService.Paginator.GetBuiltinSlotTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbuiltinslottypespaginator)
        """


class GetIntentVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetIntentVersions.html#LexModelBuildingService.Paginator.GetIntentVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getintentversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetIntentVersionsRequestGetIntentVersionsPaginateTypeDef]
    ) -> _PageIterator[GetIntentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetIntentVersions.html#LexModelBuildingService.Paginator.GetIntentVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getintentversionspaginator)
        """


class GetIntentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetIntents.html#LexModelBuildingService.Paginator.GetIntents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getintentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetIntentsRequestGetIntentsPaginateTypeDef]
    ) -> _PageIterator[GetIntentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetIntents.html#LexModelBuildingService.Paginator.GetIntents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getintentspaginator)
        """


class GetSlotTypeVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetSlotTypeVersions.html#LexModelBuildingService.Paginator.GetSlotTypeVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getslottypeversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetSlotTypeVersionsRequestGetSlotTypeVersionsPaginateTypeDef]
    ) -> _PageIterator[GetSlotTypeVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetSlotTypeVersions.html#LexModelBuildingService.Paginator.GetSlotTypeVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getslottypeversionspaginator)
        """


class GetSlotTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetSlotTypes.html#LexModelBuildingService.Paginator.GetSlotTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getslottypespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetSlotTypesRequestGetSlotTypesPaginateTypeDef]
    ) -> _PageIterator[GetSlotTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetSlotTypes.html#LexModelBuildingService.Paginator.GetSlotTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getslottypespaginator)
        """
