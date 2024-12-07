"""
Type annotations for proton service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_proton.client import ProtonClient
    from types_aiobotocore_proton.paginator import (
        ListComponentOutputsPaginator,
        ListComponentProvisionedResourcesPaginator,
        ListComponentsPaginator,
        ListDeploymentsPaginator,
        ListEnvironmentAccountConnectionsPaginator,
        ListEnvironmentOutputsPaginator,
        ListEnvironmentProvisionedResourcesPaginator,
        ListEnvironmentTemplateVersionsPaginator,
        ListEnvironmentTemplatesPaginator,
        ListEnvironmentsPaginator,
        ListRepositoriesPaginator,
        ListRepositorySyncDefinitionsPaginator,
        ListServiceInstanceOutputsPaginator,
        ListServiceInstanceProvisionedResourcesPaginator,
        ListServiceInstancesPaginator,
        ListServicePipelineOutputsPaginator,
        ListServicePipelineProvisionedResourcesPaginator,
        ListServiceTemplateVersionsPaginator,
        ListServiceTemplatesPaginator,
        ListServicesPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    with session.create_client("proton") as client:
        client: ProtonClient

        list_component_outputs_paginator: ListComponentOutputsPaginator = client.get_paginator("list_component_outputs")
        list_component_provisioned_resources_paginator: ListComponentProvisionedResourcesPaginator = client.get_paginator("list_component_provisioned_resources")
        list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
        list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
        list_environment_account_connections_paginator: ListEnvironmentAccountConnectionsPaginator = client.get_paginator("list_environment_account_connections")
        list_environment_outputs_paginator: ListEnvironmentOutputsPaginator = client.get_paginator("list_environment_outputs")
        list_environment_provisioned_resources_paginator: ListEnvironmentProvisionedResourcesPaginator = client.get_paginator("list_environment_provisioned_resources")
        list_environment_template_versions_paginator: ListEnvironmentTemplateVersionsPaginator = client.get_paginator("list_environment_template_versions")
        list_environment_templates_paginator: ListEnvironmentTemplatesPaginator = client.get_paginator("list_environment_templates")
        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
        list_repositories_paginator: ListRepositoriesPaginator = client.get_paginator("list_repositories")
        list_repository_sync_definitions_paginator: ListRepositorySyncDefinitionsPaginator = client.get_paginator("list_repository_sync_definitions")
        list_service_instance_outputs_paginator: ListServiceInstanceOutputsPaginator = client.get_paginator("list_service_instance_outputs")
        list_service_instance_provisioned_resources_paginator: ListServiceInstanceProvisionedResourcesPaginator = client.get_paginator("list_service_instance_provisioned_resources")
        list_service_instances_paginator: ListServiceInstancesPaginator = client.get_paginator("list_service_instances")
        list_service_pipeline_outputs_paginator: ListServicePipelineOutputsPaginator = client.get_paginator("list_service_pipeline_outputs")
        list_service_pipeline_provisioned_resources_paginator: ListServicePipelineProvisionedResourcesPaginator = client.get_paginator("list_service_pipeline_provisioned_resources")
        list_service_template_versions_paginator: ListServiceTemplateVersionsPaginator = client.get_paginator("list_service_template_versions")
        list_service_templates_paginator: ListServiceTemplatesPaginator = client.get_paginator("list_service_templates")
        list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListComponentOutputsInputListComponentOutputsPaginateTypeDef,
    ListComponentOutputsOutputTypeDef,
    ListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef,
    ListComponentProvisionedResourcesOutputTypeDef,
    ListComponentsInputListComponentsPaginateTypeDef,
    ListComponentsOutputTypeDef,
    ListDeploymentsInputListDeploymentsPaginateTypeDef,
    ListDeploymentsOutputTypeDef,
    ListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef,
    ListEnvironmentAccountConnectionsOutputTypeDef,
    ListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef,
    ListEnvironmentOutputsOutputTypeDef,
    ListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef,
    ListEnvironmentProvisionedResourcesOutputTypeDef,
    ListEnvironmentsInputListEnvironmentsPaginateTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListEnvironmentTemplatesInputListEnvironmentTemplatesPaginateTypeDef,
    ListEnvironmentTemplatesOutputTypeDef,
    ListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef,
    ListEnvironmentTemplateVersionsOutputTypeDef,
    ListRepositoriesInputListRepositoriesPaginateTypeDef,
    ListRepositoriesOutputTypeDef,
    ListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef,
    ListRepositorySyncDefinitionsOutputTypeDef,
    ListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef,
    ListServiceInstanceOutputsOutputTypeDef,
    ListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef,
    ListServiceInstanceProvisionedResourcesOutputTypeDef,
    ListServiceInstancesInputListServiceInstancesPaginateTypeDef,
    ListServiceInstancesOutputTypeDef,
    ListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef,
    ListServicePipelineOutputsOutputTypeDef,
    ListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef,
    ListServicePipelineProvisionedResourcesOutputTypeDef,
    ListServicesInputListServicesPaginateTypeDef,
    ListServicesOutputTypeDef,
    ListServiceTemplatesInputListServiceTemplatesPaginateTypeDef,
    ListServiceTemplatesOutputTypeDef,
    ListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef,
    ListServiceTemplateVersionsOutputTypeDef,
    ListTagsForResourceInputListTagsForResourcePaginateTypeDef,
    ListTagsForResourceOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListComponentOutputsPaginator",
    "ListComponentProvisionedResourcesPaginator",
    "ListComponentsPaginator",
    "ListDeploymentsPaginator",
    "ListEnvironmentAccountConnectionsPaginator",
    "ListEnvironmentOutputsPaginator",
    "ListEnvironmentProvisionedResourcesPaginator",
    "ListEnvironmentTemplateVersionsPaginator",
    "ListEnvironmentTemplatesPaginator",
    "ListEnvironmentsPaginator",
    "ListRepositoriesPaginator",
    "ListRepositorySyncDefinitionsPaginator",
    "ListServiceInstanceOutputsPaginator",
    "ListServiceInstanceProvisionedResourcesPaginator",
    "ListServiceInstancesPaginator",
    "ListServicePipelineOutputsPaginator",
    "ListServicePipelineProvisionedResourcesPaginator",
    "ListServiceTemplateVersionsPaginator",
    "ListServiceTemplatesPaginator",
    "ListServicesPaginator",
    "ListTagsForResourcePaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListComponentOutputsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListComponentOutputs.html#Proton.Paginator.ListComponentOutputs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listcomponentoutputspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListComponentOutputsInputListComponentOutputsPaginateTypeDef]
    ) -> AsyncIterator[ListComponentOutputsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListComponentOutputs.html#Proton.Paginator.ListComponentOutputs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listcomponentoutputspaginator)
        """

class ListComponentProvisionedResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListComponentProvisionedResources.html#Proton.Paginator.ListComponentProvisionedResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listcomponentprovisionedresourcespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListComponentProvisionedResourcesInputListComponentProvisionedResourcesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListComponentProvisionedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListComponentProvisionedResources.html#Proton.Paginator.ListComponentProvisionedResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listcomponentprovisionedresourcespaginator)
        """

class ListComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListComponents.html#Proton.Paginator.ListComponents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listcomponentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListComponentsInputListComponentsPaginateTypeDef]
    ) -> AsyncIterator[ListComponentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListComponents.html#Proton.Paginator.ListComponents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listcomponentspaginator)
        """

class ListDeploymentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListDeployments.html#Proton.Paginator.ListDeployments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listdeploymentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDeploymentsInputListDeploymentsPaginateTypeDef]
    ) -> AsyncIterator[ListDeploymentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListDeployments.html#Proton.Paginator.ListDeployments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listdeploymentspaginator)
        """

class ListEnvironmentAccountConnectionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentAccountConnections.html#Proton.Paginator.ListEnvironmentAccountConnections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentaccountconnectionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListEnvironmentAccountConnectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentAccountConnections.html#Proton.Paginator.ListEnvironmentAccountConnections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentaccountconnectionspaginator)
        """

class ListEnvironmentOutputsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentOutputs.html#Proton.Paginator.ListEnvironmentOutputs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentoutputspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef]
    ) -> AsyncIterator[ListEnvironmentOutputsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentOutputs.html#Proton.Paginator.ListEnvironmentOutputs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentoutputspaginator)
        """

class ListEnvironmentProvisionedResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentProvisionedResources.html#Proton.Paginator.ListEnvironmentProvisionedResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentprovisionedresourcespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListEnvironmentProvisionedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentProvisionedResources.html#Proton.Paginator.ListEnvironmentProvisionedResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentprovisionedresourcespaginator)
        """

class ListEnvironmentTemplateVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentTemplateVersions.html#Proton.Paginator.ListEnvironmentTemplateVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmenttemplateversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListEnvironmentTemplateVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentTemplateVersions.html#Proton.Paginator.ListEnvironmentTemplateVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmenttemplateversionspaginator)
        """

class ListEnvironmentTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentTemplates.html#Proton.Paginator.ListEnvironmentTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmenttemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEnvironmentTemplatesInputListEnvironmentTemplatesPaginateTypeDef]
    ) -> AsyncIterator[ListEnvironmentTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironmentTemplates.html#Proton.Paginator.ListEnvironmentTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmenttemplatespaginator)
        """

class ListEnvironmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironments.html#Proton.Paginator.ListEnvironments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEnvironmentsInputListEnvironmentsPaginateTypeDef]
    ) -> AsyncIterator[ListEnvironmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListEnvironments.html#Proton.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listenvironmentspaginator)
        """

class ListRepositoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListRepositories.html#Proton.Paginator.ListRepositories)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listrepositoriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRepositoriesInputListRepositoriesPaginateTypeDef]
    ) -> AsyncIterator[ListRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListRepositories.html#Proton.Paginator.ListRepositories.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listrepositoriespaginator)
        """

class ListRepositorySyncDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListRepositorySyncDefinitions.html#Proton.Paginator.ListRepositorySyncDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listrepositorysyncdefinitionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListRepositorySyncDefinitionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListRepositorySyncDefinitions.html#Proton.Paginator.ListRepositorySyncDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listrepositorysyncdefinitionspaginator)
        """

class ListServiceInstanceOutputsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceInstanceOutputs.html#Proton.Paginator.ListServiceInstanceOutputs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listserviceinstanceoutputspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef],
    ) -> AsyncIterator[ListServiceInstanceOutputsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceInstanceOutputs.html#Proton.Paginator.ListServiceInstanceOutputs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listserviceinstanceoutputspaginator)
        """

class ListServiceInstanceProvisionedResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceInstanceProvisionedResources.html#Proton.Paginator.ListServiceInstanceProvisionedResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listserviceinstanceprovisionedresourcespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListServiceInstanceProvisionedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceInstanceProvisionedResources.html#Proton.Paginator.ListServiceInstanceProvisionedResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listserviceinstanceprovisionedresourcespaginator)
        """

class ListServiceInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceInstances.html#Proton.Paginator.ListServiceInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listserviceinstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServiceInstancesInputListServiceInstancesPaginateTypeDef]
    ) -> AsyncIterator[ListServiceInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceInstances.html#Proton.Paginator.ListServiceInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listserviceinstancespaginator)
        """

class ListServicePipelineOutputsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServicePipelineOutputs.html#Proton.Paginator.ListServicePipelineOutputs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicepipelineoutputspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef],
    ) -> AsyncIterator[ListServicePipelineOutputsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServicePipelineOutputs.html#Proton.Paginator.ListServicePipelineOutputs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicepipelineoutputspaginator)
        """

class ListServicePipelineProvisionedResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServicePipelineProvisionedResources.html#Proton.Paginator.ListServicePipelineProvisionedResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicepipelineprovisionedresourcespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListServicePipelineProvisionedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServicePipelineProvisionedResources.html#Proton.Paginator.ListServicePipelineProvisionedResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicepipelineprovisionedresourcespaginator)
        """

class ListServiceTemplateVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceTemplateVersions.html#Proton.Paginator.ListServiceTemplateVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicetemplateversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListServiceTemplateVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceTemplateVersions.html#Proton.Paginator.ListServiceTemplateVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicetemplateversionspaginator)
        """

class ListServiceTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceTemplates.html#Proton.Paginator.ListServiceTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicetemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServiceTemplatesInputListServiceTemplatesPaginateTypeDef]
    ) -> AsyncIterator[ListServiceTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServiceTemplates.html#Proton.Paginator.ListServiceTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicetemplatespaginator)
        """

class ListServicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServices.html#Proton.Paginator.ListServices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServicesInputListServicesPaginateTypeDef]
    ) -> AsyncIterator[ListServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListServices.html#Proton.Paginator.ListServices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listservicespaginator)
        """

class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListTagsForResource.html#Proton.Paginator.ListTagsForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceInputListTagsForResourcePaginateTypeDef]
    ) -> AsyncIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/paginator/ListTagsForResource.html#Proton.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/paginators/#listtagsforresourcepaginator)
        """
