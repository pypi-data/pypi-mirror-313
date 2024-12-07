"""
Type annotations for apprunner service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_apprunner.client import AppRunnerClient

    session = get_session()
    async with session.create_client("apprunner") as client:
        client: AppRunnerClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    AssociateCustomDomainRequestRequestTypeDef,
    AssociateCustomDomainResponseTypeDef,
    CreateAutoScalingConfigurationRequestRequestTypeDef,
    CreateAutoScalingConfigurationResponseTypeDef,
    CreateConnectionRequestRequestTypeDef,
    CreateConnectionResponseTypeDef,
    CreateObservabilityConfigurationRequestRequestTypeDef,
    CreateObservabilityConfigurationResponseTypeDef,
    CreateServiceRequestRequestTypeDef,
    CreateServiceResponseTypeDef,
    CreateVpcConnectorRequestRequestTypeDef,
    CreateVpcConnectorResponseTypeDef,
    CreateVpcIngressConnectionRequestRequestTypeDef,
    CreateVpcIngressConnectionResponseTypeDef,
    DeleteAutoScalingConfigurationRequestRequestTypeDef,
    DeleteAutoScalingConfigurationResponseTypeDef,
    DeleteConnectionRequestRequestTypeDef,
    DeleteConnectionResponseTypeDef,
    DeleteObservabilityConfigurationRequestRequestTypeDef,
    DeleteObservabilityConfigurationResponseTypeDef,
    DeleteServiceRequestRequestTypeDef,
    DeleteServiceResponseTypeDef,
    DeleteVpcConnectorRequestRequestTypeDef,
    DeleteVpcConnectorResponseTypeDef,
    DeleteVpcIngressConnectionRequestRequestTypeDef,
    DeleteVpcIngressConnectionResponseTypeDef,
    DescribeAutoScalingConfigurationRequestRequestTypeDef,
    DescribeAutoScalingConfigurationResponseTypeDef,
    DescribeCustomDomainsRequestRequestTypeDef,
    DescribeCustomDomainsResponseTypeDef,
    DescribeObservabilityConfigurationRequestRequestTypeDef,
    DescribeObservabilityConfigurationResponseTypeDef,
    DescribeServiceRequestRequestTypeDef,
    DescribeServiceResponseTypeDef,
    DescribeVpcConnectorRequestRequestTypeDef,
    DescribeVpcConnectorResponseTypeDef,
    DescribeVpcIngressConnectionRequestRequestTypeDef,
    DescribeVpcIngressConnectionResponseTypeDef,
    DisassociateCustomDomainRequestRequestTypeDef,
    DisassociateCustomDomainResponseTypeDef,
    ListAutoScalingConfigurationsRequestRequestTypeDef,
    ListAutoScalingConfigurationsResponseTypeDef,
    ListConnectionsRequestRequestTypeDef,
    ListConnectionsResponseTypeDef,
    ListObservabilityConfigurationsRequestRequestTypeDef,
    ListObservabilityConfigurationsResponseTypeDef,
    ListOperationsRequestRequestTypeDef,
    ListOperationsResponseTypeDef,
    ListServicesForAutoScalingConfigurationRequestRequestTypeDef,
    ListServicesForAutoScalingConfigurationResponseTypeDef,
    ListServicesRequestRequestTypeDef,
    ListServicesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVpcConnectorsRequestRequestTypeDef,
    ListVpcConnectorsResponseTypeDef,
    ListVpcIngressConnectionsRequestRequestTypeDef,
    ListVpcIngressConnectionsResponseTypeDef,
    PauseServiceRequestRequestTypeDef,
    PauseServiceResponseTypeDef,
    ResumeServiceRequestRequestTypeDef,
    ResumeServiceResponseTypeDef,
    StartDeploymentRequestRequestTypeDef,
    StartDeploymentResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDefaultAutoScalingConfigurationRequestRequestTypeDef,
    UpdateDefaultAutoScalingConfigurationResponseTypeDef,
    UpdateServiceRequestRequestTypeDef,
    UpdateServiceResponseTypeDef,
    UpdateVpcIngressConnectionRequestRequestTypeDef,
    UpdateVpcIngressConnectionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("AppRunnerClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]

class AppRunnerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppRunnerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#close)
        """

    async def associate_custom_domain(
        self, **kwargs: Unpack[AssociateCustomDomainRequestRequestTypeDef]
    ) -> AssociateCustomDomainResponseTypeDef:
        """
        Associate your own domain name with the App Runner subdomain URL of your App
        Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/associate_custom_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#associate_custom_domain)
        """

    async def create_auto_scaling_configuration(
        self, **kwargs: Unpack[CreateAutoScalingConfigurationRequestRequestTypeDef]
    ) -> CreateAutoScalingConfigurationResponseTypeDef:
        """
        Create an App Runner automatic scaling configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/create_auto_scaling_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#create_auto_scaling_configuration)
        """

    async def create_connection(
        self, **kwargs: Unpack[CreateConnectionRequestRequestTypeDef]
    ) -> CreateConnectionResponseTypeDef:
        """
        Create an App Runner connection resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/create_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#create_connection)
        """

    async def create_observability_configuration(
        self, **kwargs: Unpack[CreateObservabilityConfigurationRequestRequestTypeDef]
    ) -> CreateObservabilityConfigurationResponseTypeDef:
        """
        Create an App Runner observability configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/create_observability_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#create_observability_configuration)
        """

    async def create_service(
        self, **kwargs: Unpack[CreateServiceRequestRequestTypeDef]
    ) -> CreateServiceResponseTypeDef:
        """
        Create an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/create_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#create_service)
        """

    async def create_vpc_connector(
        self, **kwargs: Unpack[CreateVpcConnectorRequestRequestTypeDef]
    ) -> CreateVpcConnectorResponseTypeDef:
        """
        Create an App Runner VPC connector resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/create_vpc_connector.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#create_vpc_connector)
        """

    async def create_vpc_ingress_connection(
        self, **kwargs: Unpack[CreateVpcIngressConnectionRequestRequestTypeDef]
    ) -> CreateVpcIngressConnectionResponseTypeDef:
        """
        Create an App Runner VPC Ingress Connection resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/create_vpc_ingress_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#create_vpc_ingress_connection)
        """

    async def delete_auto_scaling_configuration(
        self, **kwargs: Unpack[DeleteAutoScalingConfigurationRequestRequestTypeDef]
    ) -> DeleteAutoScalingConfigurationResponseTypeDef:
        """
        Delete an App Runner automatic scaling configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/delete_auto_scaling_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#delete_auto_scaling_configuration)
        """

    async def delete_connection(
        self, **kwargs: Unpack[DeleteConnectionRequestRequestTypeDef]
    ) -> DeleteConnectionResponseTypeDef:
        """
        Delete an App Runner connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/delete_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#delete_connection)
        """

    async def delete_observability_configuration(
        self, **kwargs: Unpack[DeleteObservabilityConfigurationRequestRequestTypeDef]
    ) -> DeleteObservabilityConfigurationResponseTypeDef:
        """
        Delete an App Runner observability configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/delete_observability_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#delete_observability_configuration)
        """

    async def delete_service(
        self, **kwargs: Unpack[DeleteServiceRequestRequestTypeDef]
    ) -> DeleteServiceResponseTypeDef:
        """
        Delete an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/delete_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#delete_service)
        """

    async def delete_vpc_connector(
        self, **kwargs: Unpack[DeleteVpcConnectorRequestRequestTypeDef]
    ) -> DeleteVpcConnectorResponseTypeDef:
        """
        Delete an App Runner VPC connector resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/delete_vpc_connector.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#delete_vpc_connector)
        """

    async def delete_vpc_ingress_connection(
        self, **kwargs: Unpack[DeleteVpcIngressConnectionRequestRequestTypeDef]
    ) -> DeleteVpcIngressConnectionResponseTypeDef:
        """
        Delete an App Runner VPC Ingress Connection resource that's associated with an
        App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/delete_vpc_ingress_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#delete_vpc_ingress_connection)
        """

    async def describe_auto_scaling_configuration(
        self, **kwargs: Unpack[DescribeAutoScalingConfigurationRequestRequestTypeDef]
    ) -> DescribeAutoScalingConfigurationResponseTypeDef:
        """
        Return a full description of an App Runner automatic scaling configuration
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/describe_auto_scaling_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#describe_auto_scaling_configuration)
        """

    async def describe_custom_domains(
        self, **kwargs: Unpack[DescribeCustomDomainsRequestRequestTypeDef]
    ) -> DescribeCustomDomainsResponseTypeDef:
        """
        Return a description of custom domain names that are associated with an App
        Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/describe_custom_domains.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#describe_custom_domains)
        """

    async def describe_observability_configuration(
        self, **kwargs: Unpack[DescribeObservabilityConfigurationRequestRequestTypeDef]
    ) -> DescribeObservabilityConfigurationResponseTypeDef:
        """
        Return a full description of an App Runner observability configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/describe_observability_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#describe_observability_configuration)
        """

    async def describe_service(
        self, **kwargs: Unpack[DescribeServiceRequestRequestTypeDef]
    ) -> DescribeServiceResponseTypeDef:
        """
        Return a full description of an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/describe_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#describe_service)
        """

    async def describe_vpc_connector(
        self, **kwargs: Unpack[DescribeVpcConnectorRequestRequestTypeDef]
    ) -> DescribeVpcConnectorResponseTypeDef:
        """
        Return a description of an App Runner VPC connector resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/describe_vpc_connector.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#describe_vpc_connector)
        """

    async def describe_vpc_ingress_connection(
        self, **kwargs: Unpack[DescribeVpcIngressConnectionRequestRequestTypeDef]
    ) -> DescribeVpcIngressConnectionResponseTypeDef:
        """
        Return a full description of an App Runner VPC Ingress Connection resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/describe_vpc_ingress_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#describe_vpc_ingress_connection)
        """

    async def disassociate_custom_domain(
        self, **kwargs: Unpack[DisassociateCustomDomainRequestRequestTypeDef]
    ) -> DisassociateCustomDomainResponseTypeDef:
        """
        Disassociate a custom domain name from an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/disassociate_custom_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#disassociate_custom_domain)
        """

    async def list_auto_scaling_configurations(
        self, **kwargs: Unpack[ListAutoScalingConfigurationsRequestRequestTypeDef]
    ) -> ListAutoScalingConfigurationsResponseTypeDef:
        """
        Returns a list of active App Runner automatic scaling configurations in your
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_auto_scaling_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#list_auto_scaling_configurations)
        """

    async def list_connections(
        self, **kwargs: Unpack[ListConnectionsRequestRequestTypeDef]
    ) -> ListConnectionsResponseTypeDef:
        """
        Returns a list of App Runner connections that are associated with your Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#list_connections)
        """

    async def list_observability_configurations(
        self, **kwargs: Unpack[ListObservabilityConfigurationsRequestRequestTypeDef]
    ) -> ListObservabilityConfigurationsResponseTypeDef:
        """
        Returns a list of active App Runner observability configurations in your Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_observability_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#list_observability_configurations)
        """

    async def list_operations(
        self, **kwargs: Unpack[ListOperationsRequestRequestTypeDef]
    ) -> ListOperationsResponseTypeDef:
        """
        Return a list of operations that occurred on an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_operations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#list_operations)
        """

    async def list_services(
        self, **kwargs: Unpack[ListServicesRequestRequestTypeDef]
    ) -> ListServicesResponseTypeDef:
        """
        Returns a list of running App Runner services in your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_services.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#list_services)
        """

    async def list_services_for_auto_scaling_configuration(
        self, **kwargs: Unpack[ListServicesForAutoScalingConfigurationRequestRequestTypeDef]
    ) -> ListServicesForAutoScalingConfigurationResponseTypeDef:
        """
        Returns a list of the associated App Runner services using an auto scaling
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_services_for_auto_scaling_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#list_services_for_auto_scaling_configuration)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List tags that are associated with for an App Runner resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#list_tags_for_resource)
        """

    async def list_vpc_connectors(
        self, **kwargs: Unpack[ListVpcConnectorsRequestRequestTypeDef]
    ) -> ListVpcConnectorsResponseTypeDef:
        """
        Returns a list of App Runner VPC connectors in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_vpc_connectors.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#list_vpc_connectors)
        """

    async def list_vpc_ingress_connections(
        self, **kwargs: Unpack[ListVpcIngressConnectionsRequestRequestTypeDef]
    ) -> ListVpcIngressConnectionsResponseTypeDef:
        """
        Return a list of App Runner VPC Ingress Connections in your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/list_vpc_ingress_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#list_vpc_ingress_connections)
        """

    async def pause_service(
        self, **kwargs: Unpack[PauseServiceRequestRequestTypeDef]
    ) -> PauseServiceResponseTypeDef:
        """
        Pause an active App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/pause_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#pause_service)
        """

    async def resume_service(
        self, **kwargs: Unpack[ResumeServiceRequestRequestTypeDef]
    ) -> ResumeServiceResponseTypeDef:
        """
        Resume an active App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/resume_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#resume_service)
        """

    async def start_deployment(
        self, **kwargs: Unpack[StartDeploymentRequestRequestTypeDef]
    ) -> StartDeploymentResponseTypeDef:
        """
        Initiate a manual deployment of the latest commit in a source code repository
        or the latest image in a source image repository to an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/start_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#start_deployment)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Add tags to, or update the tag values of, an App Runner resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove tags from an App Runner resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#untag_resource)
        """

    async def update_default_auto_scaling_configuration(
        self, **kwargs: Unpack[UpdateDefaultAutoScalingConfigurationRequestRequestTypeDef]
    ) -> UpdateDefaultAutoScalingConfigurationResponseTypeDef:
        """
        Update an auto scaling configuration to be the default.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/update_default_auto_scaling_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#update_default_auto_scaling_configuration)
        """

    async def update_service(
        self, **kwargs: Unpack[UpdateServiceRequestRequestTypeDef]
    ) -> UpdateServiceResponseTypeDef:
        """
        Update an App Runner service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/update_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#update_service)
        """

    async def update_vpc_ingress_connection(
        self, **kwargs: Unpack[UpdateVpcIngressConnectionRequestRequestTypeDef]
    ) -> UpdateVpcIngressConnectionResponseTypeDef:
        """
        Update an existing App Runner VPC Ingress Connection resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner/client/update_vpc_ingress_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/#update_vpc_ingress_connection)
        """

    async def __aenter__(self) -> "AppRunnerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apprunner.html#AppRunner.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/client/)
        """
