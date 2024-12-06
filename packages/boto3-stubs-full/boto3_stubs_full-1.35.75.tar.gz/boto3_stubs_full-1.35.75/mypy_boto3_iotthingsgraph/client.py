"""
Type annotations for iotthingsgraph service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iotthingsgraph.client import IoTThingsGraphClient

    session = Session()
    client: IoTThingsGraphClient = session.client("iotthingsgraph")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetFlowTemplateRevisionsPaginator,
    GetSystemTemplateRevisionsPaginator,
    ListFlowExecutionMessagesPaginator,
    ListTagsForResourcePaginator,
    SearchEntitiesPaginator,
    SearchFlowExecutionsPaginator,
    SearchFlowTemplatesPaginator,
    SearchSystemInstancesPaginator,
    SearchSystemTemplatesPaginator,
    SearchThingsPaginator,
)
from .type_defs import (
    AssociateEntityToThingRequestRequestTypeDef,
    CreateFlowTemplateRequestRequestTypeDef,
    CreateFlowTemplateResponseTypeDef,
    CreateSystemInstanceRequestRequestTypeDef,
    CreateSystemInstanceResponseTypeDef,
    CreateSystemTemplateRequestRequestTypeDef,
    CreateSystemTemplateResponseTypeDef,
    DeleteFlowTemplateRequestRequestTypeDef,
    DeleteNamespaceResponseTypeDef,
    DeleteSystemInstanceRequestRequestTypeDef,
    DeleteSystemTemplateRequestRequestTypeDef,
    DeploySystemInstanceRequestRequestTypeDef,
    DeploySystemInstanceResponseTypeDef,
    DeprecateFlowTemplateRequestRequestTypeDef,
    DeprecateSystemTemplateRequestRequestTypeDef,
    DescribeNamespaceRequestRequestTypeDef,
    DescribeNamespaceResponseTypeDef,
    DissociateEntityFromThingRequestRequestTypeDef,
    GetEntitiesRequestRequestTypeDef,
    GetEntitiesResponseTypeDef,
    GetFlowTemplateRequestRequestTypeDef,
    GetFlowTemplateResponseTypeDef,
    GetFlowTemplateRevisionsRequestRequestTypeDef,
    GetFlowTemplateRevisionsResponseTypeDef,
    GetNamespaceDeletionStatusResponseTypeDef,
    GetSystemInstanceRequestRequestTypeDef,
    GetSystemInstanceResponseTypeDef,
    GetSystemTemplateRequestRequestTypeDef,
    GetSystemTemplateResponseTypeDef,
    GetSystemTemplateRevisionsRequestRequestTypeDef,
    GetSystemTemplateRevisionsResponseTypeDef,
    GetUploadStatusRequestRequestTypeDef,
    GetUploadStatusResponseTypeDef,
    ListFlowExecutionMessagesRequestRequestTypeDef,
    ListFlowExecutionMessagesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    SearchEntitiesRequestRequestTypeDef,
    SearchEntitiesResponseTypeDef,
    SearchFlowExecutionsRequestRequestTypeDef,
    SearchFlowExecutionsResponseTypeDef,
    SearchFlowTemplatesRequestRequestTypeDef,
    SearchFlowTemplatesResponseTypeDef,
    SearchSystemInstancesRequestRequestTypeDef,
    SearchSystemInstancesResponseTypeDef,
    SearchSystemTemplatesRequestRequestTypeDef,
    SearchSystemTemplatesResponseTypeDef,
    SearchThingsRequestRequestTypeDef,
    SearchThingsResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UndeploySystemInstanceRequestRequestTypeDef,
    UndeploySystemInstanceResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateFlowTemplateRequestRequestTypeDef,
    UpdateFlowTemplateResponseTypeDef,
    UpdateSystemTemplateRequestRequestTypeDef,
    UpdateSystemTemplateResponseTypeDef,
    UploadEntityDefinitionsRequestRequestTypeDef,
    UploadEntityDefinitionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("IoTThingsGraphClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class IoTThingsGraphClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTThingsGraphClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#close)
        """

    def associate_entity_to_thing(
        self, **kwargs: Unpack[AssociateEntityToThingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a device with a concrete thing that is in the user's registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/associate_entity_to_thing.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#associate_entity_to_thing)
        """

    def create_flow_template(
        self, **kwargs: Unpack[CreateFlowTemplateRequestRequestTypeDef]
    ) -> CreateFlowTemplateResponseTypeDef:
        """
        Creates a workflow template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/create_flow_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#create_flow_template)
        """

    def create_system_instance(
        self, **kwargs: Unpack[CreateSystemInstanceRequestRequestTypeDef]
    ) -> CreateSystemInstanceResponseTypeDef:
        """
        Creates a system instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/create_system_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#create_system_instance)
        """

    def create_system_template(
        self, **kwargs: Unpack[CreateSystemTemplateRequestRequestTypeDef]
    ) -> CreateSystemTemplateResponseTypeDef:
        """
        Creates a system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/create_system_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#create_system_template)
        """

    def delete_flow_template(
        self, **kwargs: Unpack[DeleteFlowTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/delete_flow_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#delete_flow_template)
        """

    def delete_namespace(self) -> DeleteNamespaceResponseTypeDef:
        """
        Deletes the specified namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/delete_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#delete_namespace)
        """

    def delete_system_instance(
        self, **kwargs: Unpack[DeleteSystemInstanceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a system instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/delete_system_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#delete_system_instance)
        """

    def delete_system_template(
        self, **kwargs: Unpack[DeleteSystemTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/delete_system_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#delete_system_template)
        """

    def deploy_system_instance(
        self, **kwargs: Unpack[DeploySystemInstanceRequestRequestTypeDef]
    ) -> DeploySystemInstanceResponseTypeDef:
        """
        <b>Greengrass and Cloud Deployments</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/deploy_system_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#deploy_system_instance)
        """

    def deprecate_flow_template(
        self, **kwargs: Unpack[DeprecateFlowTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deprecates the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/deprecate_flow_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#deprecate_flow_template)
        """

    def deprecate_system_template(
        self, **kwargs: Unpack[DeprecateSystemTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deprecates the specified system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/deprecate_system_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#deprecate_system_template)
        """

    def describe_namespace(
        self, **kwargs: Unpack[DescribeNamespaceRequestRequestTypeDef]
    ) -> DescribeNamespaceResponseTypeDef:
        """
        Gets the latest version of the user's namespace and the public version that it
        is tracking.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/describe_namespace.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#describe_namespace)
        """

    def dissociate_entity_from_thing(
        self, **kwargs: Unpack[DissociateEntityFromThingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Dissociates a device entity from a concrete thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/dissociate_entity_from_thing.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#dissociate_entity_from_thing)
        """

    def get_entities(
        self, **kwargs: Unpack[GetEntitiesRequestRequestTypeDef]
    ) -> GetEntitiesResponseTypeDef:
        """
        Gets definitions of the specified entities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_entities.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_entities)
        """

    def get_flow_template(
        self, **kwargs: Unpack[GetFlowTemplateRequestRequestTypeDef]
    ) -> GetFlowTemplateResponseTypeDef:
        """
        Gets the latest version of the <code>DefinitionDocument</code> and
        <code>FlowTemplateSummary</code> for the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_flow_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_flow_template)
        """

    def get_flow_template_revisions(
        self, **kwargs: Unpack[GetFlowTemplateRevisionsRequestRequestTypeDef]
    ) -> GetFlowTemplateRevisionsResponseTypeDef:
        """
        Gets revisions of the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_flow_template_revisions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_flow_template_revisions)
        """

    def get_namespace_deletion_status(self) -> GetNamespaceDeletionStatusResponseTypeDef:
        """
        Gets the status of a namespace deletion task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_namespace_deletion_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_namespace_deletion_status)
        """

    def get_system_instance(
        self, **kwargs: Unpack[GetSystemInstanceRequestRequestTypeDef]
    ) -> GetSystemInstanceResponseTypeDef:
        """
        Gets a system instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_system_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_system_instance)
        """

    def get_system_template(
        self, **kwargs: Unpack[GetSystemTemplateRequestRequestTypeDef]
    ) -> GetSystemTemplateResponseTypeDef:
        """
        Gets a system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_system_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_system_template)
        """

    def get_system_template_revisions(
        self, **kwargs: Unpack[GetSystemTemplateRevisionsRequestRequestTypeDef]
    ) -> GetSystemTemplateRevisionsResponseTypeDef:
        """
        Gets revisions made to the specified system template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_system_template_revisions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_system_template_revisions)
        """

    def get_upload_status(
        self, **kwargs: Unpack[GetUploadStatusRequestRequestTypeDef]
    ) -> GetUploadStatusResponseTypeDef:
        """
        Gets the status of the specified upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_upload_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_upload_status)
        """

    def list_flow_execution_messages(
        self, **kwargs: Unpack[ListFlowExecutionMessagesRequestRequestTypeDef]
    ) -> ListFlowExecutionMessagesResponseTypeDef:
        """
        Returns a list of objects that contain information about events in a flow
        execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/list_flow_execution_messages.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#list_flow_execution_messages)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags on an AWS IoT Things Graph resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#list_tags_for_resource)
        """

    def search_entities(
        self, **kwargs: Unpack[SearchEntitiesRequestRequestTypeDef]
    ) -> SearchEntitiesResponseTypeDef:
        """
        Searches for entities of the specified type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/search_entities.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#search_entities)
        """

    def search_flow_executions(
        self, **kwargs: Unpack[SearchFlowExecutionsRequestRequestTypeDef]
    ) -> SearchFlowExecutionsResponseTypeDef:
        """
        Searches for AWS IoT Things Graph workflow execution instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/search_flow_executions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#search_flow_executions)
        """

    def search_flow_templates(
        self, **kwargs: Unpack[SearchFlowTemplatesRequestRequestTypeDef]
    ) -> SearchFlowTemplatesResponseTypeDef:
        """
        Searches for summary information about workflows.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/search_flow_templates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#search_flow_templates)
        """

    def search_system_instances(
        self, **kwargs: Unpack[SearchSystemInstancesRequestRequestTypeDef]
    ) -> SearchSystemInstancesResponseTypeDef:
        """
        Searches for system instances in the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/search_system_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#search_system_instances)
        """

    def search_system_templates(
        self, **kwargs: Unpack[SearchSystemTemplatesRequestRequestTypeDef]
    ) -> SearchSystemTemplatesResponseTypeDef:
        """
        Searches for summary information about systems in the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/search_system_templates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#search_system_templates)
        """

    def search_things(
        self, **kwargs: Unpack[SearchThingsRequestRequestTypeDef]
    ) -> SearchThingsResponseTypeDef:
        """
        Searches for things associated with the specified entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/search_things.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#search_things)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates a tag for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#tag_resource)
        """

    def undeploy_system_instance(
        self, **kwargs: Unpack[UndeploySystemInstanceRequestRequestTypeDef]
    ) -> UndeploySystemInstanceResponseTypeDef:
        """
        Removes a system instance from its target (Cloud or Greengrass).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/undeploy_system_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#undeploy_system_instance)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#untag_resource)
        """

    def update_flow_template(
        self, **kwargs: Unpack[UpdateFlowTemplateRequestRequestTypeDef]
    ) -> UpdateFlowTemplateResponseTypeDef:
        """
        Updates the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/update_flow_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#update_flow_template)
        """

    def update_system_template(
        self, **kwargs: Unpack[UpdateSystemTemplateRequestRequestTypeDef]
    ) -> UpdateSystemTemplateResponseTypeDef:
        """
        Updates the specified system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/update_system_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#update_system_template)
        """

    def upload_entity_definitions(
        self, **kwargs: Unpack[UploadEntityDefinitionsRequestRequestTypeDef]
    ) -> UploadEntityDefinitionsResponseTypeDef:
        """
        Asynchronously uploads one or more entity definitions to the user's namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/upload_entity_definitions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#upload_entity_definitions)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_flow_template_revisions"]
    ) -> GetFlowTemplateRevisionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_system_template_revisions"]
    ) -> GetSystemTemplateRevisionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_flow_execution_messages"]
    ) -> ListFlowExecutionMessagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_entities"]) -> SearchEntitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_flow_executions"]
    ) -> SearchFlowExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_flow_templates"]
    ) -> SearchFlowTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_system_instances"]
    ) -> SearchSystemInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_system_templates"]
    ) -> SearchSystemTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_things"]) -> SearchThingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotthingsgraph/client/#get_paginator)
        """
