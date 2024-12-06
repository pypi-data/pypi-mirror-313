"""
Type annotations for proton service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_proton.client import ProtonClient
    from mypy_boto3_proton.waiter import (
        ComponentDeletedWaiter,
        ComponentDeployedWaiter,
        EnvironmentDeployedWaiter,
        EnvironmentTemplateVersionRegisteredWaiter,
        ServiceCreatedWaiter,
        ServiceDeletedWaiter,
        ServiceInstanceDeployedWaiter,
        ServicePipelineDeployedWaiter,
        ServiceTemplateVersionRegisteredWaiter,
        ServiceUpdatedWaiter,
    )

    session = Session()
    client: ProtonClient = session.client("proton")

    component_deleted_waiter: ComponentDeletedWaiter = client.get_waiter("component_deleted")
    component_deployed_waiter: ComponentDeployedWaiter = client.get_waiter("component_deployed")
    environment_deployed_waiter: EnvironmentDeployedWaiter = client.get_waiter("environment_deployed")
    environment_template_version_registered_waiter: EnvironmentTemplateVersionRegisteredWaiter = client.get_waiter("environment_template_version_registered")
    service_created_waiter: ServiceCreatedWaiter = client.get_waiter("service_created")
    service_deleted_waiter: ServiceDeletedWaiter = client.get_waiter("service_deleted")
    service_instance_deployed_waiter: ServiceInstanceDeployedWaiter = client.get_waiter("service_instance_deployed")
    service_pipeline_deployed_waiter: ServicePipelineDeployedWaiter = client.get_waiter("service_pipeline_deployed")
    service_template_version_registered_waiter: ServiceTemplateVersionRegisteredWaiter = client.get_waiter("service_template_version_registered")
    service_updated_waiter: ServiceUpdatedWaiter = client.get_waiter("service_updated")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    GetComponentInputComponentDeletedWaitTypeDef,
    GetComponentInputComponentDeployedWaitTypeDef,
    GetEnvironmentInputEnvironmentDeployedWaitTypeDef,
    GetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef,
    GetServiceInputServiceCreatedWaitTypeDef,
    GetServiceInputServiceDeletedWaitTypeDef,
    GetServiceInputServicePipelineDeployedWaitTypeDef,
    GetServiceInputServiceUpdatedWaitTypeDef,
    GetServiceInstanceInputServiceInstanceDeployedWaitTypeDef,
    GetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ComponentDeletedWaiter",
    "ComponentDeployedWaiter",
    "EnvironmentDeployedWaiter",
    "EnvironmentTemplateVersionRegisteredWaiter",
    "ServiceCreatedWaiter",
    "ServiceDeletedWaiter",
    "ServiceInstanceDeployedWaiter",
    "ServicePipelineDeployedWaiter",
    "ServiceTemplateVersionRegisteredWaiter",
    "ServiceUpdatedWaiter",
)


class ComponentDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ComponentDeleted.html#Proton.Waiter.ComponentDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#componentdeletedwaiter)
    """

    def wait(self, **kwargs: Unpack[GetComponentInputComponentDeletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ComponentDeleted.html#Proton.Waiter.ComponentDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#componentdeletedwaiter)
        """


class ComponentDeployedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ComponentDeployed.html#Proton.Waiter.ComponentDeployed)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#componentdeployedwaiter)
    """

    def wait(self, **kwargs: Unpack[GetComponentInputComponentDeployedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ComponentDeployed.html#Proton.Waiter.ComponentDeployed.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#componentdeployedwaiter)
        """


class EnvironmentDeployedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/EnvironmentDeployed.html#Proton.Waiter.EnvironmentDeployed)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#environmentdeployedwaiter)
    """

    def wait(self, **kwargs: Unpack[GetEnvironmentInputEnvironmentDeployedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/EnvironmentDeployed.html#Proton.Waiter.EnvironmentDeployed.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#environmentdeployedwaiter)
        """


class EnvironmentTemplateVersionRegisteredWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/EnvironmentTemplateVersionRegistered.html#Proton.Waiter.EnvironmentTemplateVersionRegistered)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#environmenttemplateversionregisteredwaiter)
    """

    def wait(
        self,
        **kwargs: Unpack[
            GetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef
        ],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/EnvironmentTemplateVersionRegistered.html#Proton.Waiter.EnvironmentTemplateVersionRegistered.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#environmenttemplateversionregisteredwaiter)
        """


class ServiceCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceCreated.html#Proton.Waiter.ServiceCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#servicecreatedwaiter)
    """

    def wait(self, **kwargs: Unpack[GetServiceInputServiceCreatedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceCreated.html#Proton.Waiter.ServiceCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#servicecreatedwaiter)
        """


class ServiceDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceDeleted.html#Proton.Waiter.ServiceDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#servicedeletedwaiter)
    """

    def wait(self, **kwargs: Unpack[GetServiceInputServiceDeletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceDeleted.html#Proton.Waiter.ServiceDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#servicedeletedwaiter)
        """


class ServiceInstanceDeployedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceInstanceDeployed.html#Proton.Waiter.ServiceInstanceDeployed)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#serviceinstancedeployedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[GetServiceInstanceInputServiceInstanceDeployedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceInstanceDeployed.html#Proton.Waiter.ServiceInstanceDeployed.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#serviceinstancedeployedwaiter)
        """


class ServicePipelineDeployedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServicePipelineDeployed.html#Proton.Waiter.ServicePipelineDeployed)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#servicepipelinedeployedwaiter)
    """

    def wait(self, **kwargs: Unpack[GetServiceInputServicePipelineDeployedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServicePipelineDeployed.html#Proton.Waiter.ServicePipelineDeployed.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#servicepipelinedeployedwaiter)
        """


class ServiceTemplateVersionRegisteredWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceTemplateVersionRegistered.html#Proton.Waiter.ServiceTemplateVersionRegistered)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#servicetemplateversionregisteredwaiter)
    """

    def wait(
        self,
        **kwargs: Unpack[GetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceTemplateVersionRegistered.html#Proton.Waiter.ServiceTemplateVersionRegistered.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#servicetemplateversionregisteredwaiter)
        """


class ServiceUpdatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceUpdated.html#Proton.Waiter.ServiceUpdated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#serviceupdatedwaiter)
    """

    def wait(self, **kwargs: Unpack[GetServiceInputServiceUpdatedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceUpdated.html#Proton.Waiter.ServiceUpdated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/waiters/#serviceupdatedwaiter)
        """
