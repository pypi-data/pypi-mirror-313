"""
Type annotations for route53-recovery-cluster service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_route53_recovery_cluster.client import Route53RecoveryClusterClient

    session = Session()
    client: Route53RecoveryClusterClient = session.client("route53-recovery-cluster")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListRoutingControlsPaginator
from .type_defs import (
    GetRoutingControlStateRequestRequestTypeDef,
    GetRoutingControlStateResponseTypeDef,
    ListRoutingControlsRequestRequestTypeDef,
    ListRoutingControlsResponseTypeDef,
    UpdateRoutingControlStateRequestRequestTypeDef,
    UpdateRoutingControlStatesRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("Route53RecoveryClusterClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    EndpointTemporarilyUnavailableException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class Route53RecoveryClusterClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53RecoveryClusterClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/client/#close)
        """

    def get_routing_control_state(
        self, **kwargs: Unpack[GetRoutingControlStateRequestRequestTypeDef]
    ) -> GetRoutingControlStateResponseTypeDef:
        """
        Get the state for a routing control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/client/get_routing_control_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/client/#get_routing_control_state)
        """

    def list_routing_controls(
        self, **kwargs: Unpack[ListRoutingControlsRequestRequestTypeDef]
    ) -> ListRoutingControlsResponseTypeDef:
        """
        List routing control names and Amazon Resource Names (ARNs), as well as the
        routing control state for each routing control, along with the control panel
        name and control panel ARN for the routing controls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/client/list_routing_controls.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/client/#list_routing_controls)
        """

    def update_routing_control_state(
        self, **kwargs: Unpack[UpdateRoutingControlStateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Set the state of the routing control to reroute traffic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/client/update_routing_control_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/client/#update_routing_control_state)
        """

    def update_routing_control_states(
        self, **kwargs: Unpack[UpdateRoutingControlStatesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Set multiple routing control states.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/client/update_routing_control_states.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/client/#update_routing_control_states)
        """

    def get_paginator(
        self, operation_name: Literal["list_routing_controls"]
    ) -> ListRoutingControlsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/client/#get_paginator)
        """
