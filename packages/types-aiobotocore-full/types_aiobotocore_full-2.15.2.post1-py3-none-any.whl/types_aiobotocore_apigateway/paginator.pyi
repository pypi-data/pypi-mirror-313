"""
Type annotations for apigateway service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_apigateway.client import APIGatewayClient
    from types_aiobotocore_apigateway.paginator import (
        GetApiKeysPaginator,
        GetAuthorizersPaginator,
        GetBasePathMappingsPaginator,
        GetClientCertificatesPaginator,
        GetDeploymentsPaginator,
        GetDocumentationPartsPaginator,
        GetDocumentationVersionsPaginator,
        GetDomainNamesPaginator,
        GetGatewayResponsesPaginator,
        GetModelsPaginator,
        GetRequestValidatorsPaginator,
        GetResourcesPaginator,
        GetRestApisPaginator,
        GetSdkTypesPaginator,
        GetUsagePaginator,
        GetUsagePlanKeysPaginator,
        GetUsagePlansPaginator,
        GetVpcLinksPaginator,
    )

    session = get_session()
    with session.create_client("apigateway") as client:
        client: APIGatewayClient

        get_api_keys_paginator: GetApiKeysPaginator = client.get_paginator("get_api_keys")
        get_authorizers_paginator: GetAuthorizersPaginator = client.get_paginator("get_authorizers")
        get_base_path_mappings_paginator: GetBasePathMappingsPaginator = client.get_paginator("get_base_path_mappings")
        get_client_certificates_paginator: GetClientCertificatesPaginator = client.get_paginator("get_client_certificates")
        get_deployments_paginator: GetDeploymentsPaginator = client.get_paginator("get_deployments")
        get_documentation_parts_paginator: GetDocumentationPartsPaginator = client.get_paginator("get_documentation_parts")
        get_documentation_versions_paginator: GetDocumentationVersionsPaginator = client.get_paginator("get_documentation_versions")
        get_domain_names_paginator: GetDomainNamesPaginator = client.get_paginator("get_domain_names")
        get_gateway_responses_paginator: GetGatewayResponsesPaginator = client.get_paginator("get_gateway_responses")
        get_models_paginator: GetModelsPaginator = client.get_paginator("get_models")
        get_request_validators_paginator: GetRequestValidatorsPaginator = client.get_paginator("get_request_validators")
        get_resources_paginator: GetResourcesPaginator = client.get_paginator("get_resources")
        get_rest_apis_paginator: GetRestApisPaginator = client.get_paginator("get_rest_apis")
        get_sdk_types_paginator: GetSdkTypesPaginator = client.get_paginator("get_sdk_types")
        get_usage_paginator: GetUsagePaginator = client.get_paginator("get_usage")
        get_usage_plan_keys_paginator: GetUsagePlanKeysPaginator = client.get_paginator("get_usage_plan_keys")
        get_usage_plans_paginator: GetUsagePlansPaginator = client.get_paginator("get_usage_plans")
        get_vpc_links_paginator: GetVpcLinksPaginator = client.get_paginator("get_vpc_links")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ApiKeysTypeDef,
    AuthorizersTypeDef,
    BasePathMappingsTypeDef,
    ClientCertificatesTypeDef,
    DeploymentsTypeDef,
    DocumentationPartsTypeDef,
    DocumentationVersionsTypeDef,
    DomainNamesTypeDef,
    GatewayResponsesTypeDef,
    GetApiKeysRequestGetApiKeysPaginateTypeDef,
    GetAuthorizersRequestGetAuthorizersPaginateTypeDef,
    GetBasePathMappingsRequestGetBasePathMappingsPaginateTypeDef,
    GetClientCertificatesRequestGetClientCertificatesPaginateTypeDef,
    GetDeploymentsRequestGetDeploymentsPaginateTypeDef,
    GetDocumentationPartsRequestGetDocumentationPartsPaginateTypeDef,
    GetDocumentationVersionsRequestGetDocumentationVersionsPaginateTypeDef,
    GetDomainNamesRequestGetDomainNamesPaginateTypeDef,
    GetGatewayResponsesRequestGetGatewayResponsesPaginateTypeDef,
    GetModelsRequestGetModelsPaginateTypeDef,
    GetRequestValidatorsRequestGetRequestValidatorsPaginateTypeDef,
    GetResourcesRequestGetResourcesPaginateTypeDef,
    GetRestApisRequestGetRestApisPaginateTypeDef,
    GetSdkTypesRequestGetSdkTypesPaginateTypeDef,
    GetUsagePlanKeysRequestGetUsagePlanKeysPaginateTypeDef,
    GetUsagePlansRequestGetUsagePlansPaginateTypeDef,
    GetUsageRequestGetUsagePaginateTypeDef,
    GetVpcLinksRequestGetVpcLinksPaginateTypeDef,
    ModelsTypeDef,
    RequestValidatorsTypeDef,
    ResourcesTypeDef,
    RestApisTypeDef,
    SdkTypesTypeDef,
    UsagePlanKeysTypeDef,
    UsagePlansTypeDef,
    UsageTypeDef,
    VpcLinksTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetApiKeysPaginator",
    "GetAuthorizersPaginator",
    "GetBasePathMappingsPaginator",
    "GetClientCertificatesPaginator",
    "GetDeploymentsPaginator",
    "GetDocumentationPartsPaginator",
    "GetDocumentationVersionsPaginator",
    "GetDomainNamesPaginator",
    "GetGatewayResponsesPaginator",
    "GetModelsPaginator",
    "GetRequestValidatorsPaginator",
    "GetResourcesPaginator",
    "GetRestApisPaginator",
    "GetSdkTypesPaginator",
    "GetUsagePaginator",
    "GetUsagePlanKeysPaginator",
    "GetUsagePlansPaginator",
    "GetVpcLinksPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetApiKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetApiKeys.html#APIGateway.Paginator.GetApiKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getapikeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetApiKeysRequestGetApiKeysPaginateTypeDef]
    ) -> AsyncIterator[ApiKeysTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetApiKeys.html#APIGateway.Paginator.GetApiKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getapikeyspaginator)
        """

class GetAuthorizersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetAuthorizers.html#APIGateway.Paginator.GetAuthorizers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getauthorizerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetAuthorizersRequestGetAuthorizersPaginateTypeDef]
    ) -> AsyncIterator[AuthorizersTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetAuthorizers.html#APIGateway.Paginator.GetAuthorizers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getauthorizerspaginator)
        """

class GetBasePathMappingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetBasePathMappings.html#APIGateway.Paginator.GetBasePathMappings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getbasepathmappingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetBasePathMappingsRequestGetBasePathMappingsPaginateTypeDef]
    ) -> AsyncIterator[BasePathMappingsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetBasePathMappings.html#APIGateway.Paginator.GetBasePathMappings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getbasepathmappingspaginator)
        """

class GetClientCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetClientCertificates.html#APIGateway.Paginator.GetClientCertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getclientcertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetClientCertificatesRequestGetClientCertificatesPaginateTypeDef]
    ) -> AsyncIterator[ClientCertificatesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetClientCertificates.html#APIGateway.Paginator.GetClientCertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getclientcertificatespaginator)
        """

class GetDeploymentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDeployments.html#APIGateway.Paginator.GetDeployments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdeploymentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDeploymentsRequestGetDeploymentsPaginateTypeDef]
    ) -> AsyncIterator[DeploymentsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDeployments.html#APIGateway.Paginator.GetDeployments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdeploymentspaginator)
        """

class GetDocumentationPartsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDocumentationParts.html#APIGateway.Paginator.GetDocumentationParts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdocumentationpartspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDocumentationPartsRequestGetDocumentationPartsPaginateTypeDef]
    ) -> AsyncIterator[DocumentationPartsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDocumentationParts.html#APIGateway.Paginator.GetDocumentationParts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdocumentationpartspaginator)
        """

class GetDocumentationVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDocumentationVersions.html#APIGateway.Paginator.GetDocumentationVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdocumentationversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[GetDocumentationVersionsRequestGetDocumentationVersionsPaginateTypeDef],
    ) -> AsyncIterator[DocumentationVersionsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDocumentationVersions.html#APIGateway.Paginator.GetDocumentationVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdocumentationversionspaginator)
        """

class GetDomainNamesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDomainNames.html#APIGateway.Paginator.GetDomainNames)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdomainnamespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDomainNamesRequestGetDomainNamesPaginateTypeDef]
    ) -> AsyncIterator[DomainNamesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDomainNames.html#APIGateway.Paginator.GetDomainNames.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdomainnamespaginator)
        """

class GetGatewayResponsesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetGatewayResponses.html#APIGateway.Paginator.GetGatewayResponses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getgatewayresponsespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetGatewayResponsesRequestGetGatewayResponsesPaginateTypeDef]
    ) -> AsyncIterator[GatewayResponsesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetGatewayResponses.html#APIGateway.Paginator.GetGatewayResponses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getgatewayresponsespaginator)
        """

class GetModelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetModels.html#APIGateway.Paginator.GetModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getmodelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetModelsRequestGetModelsPaginateTypeDef]
    ) -> AsyncIterator[ModelsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetModels.html#APIGateway.Paginator.GetModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getmodelspaginator)
        """

class GetRequestValidatorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetRequestValidators.html#APIGateway.Paginator.GetRequestValidators)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getrequestvalidatorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetRequestValidatorsRequestGetRequestValidatorsPaginateTypeDef]
    ) -> AsyncIterator[RequestValidatorsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetRequestValidators.html#APIGateway.Paginator.GetRequestValidators.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getrequestvalidatorspaginator)
        """

class GetResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetResources.html#APIGateway.Paginator.GetResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetResourcesRequestGetResourcesPaginateTypeDef]
    ) -> AsyncIterator[ResourcesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetResources.html#APIGateway.Paginator.GetResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getresourcespaginator)
        """

class GetRestApisPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetRestApis.html#APIGateway.Paginator.GetRestApis)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getrestapispaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetRestApisRequestGetRestApisPaginateTypeDef]
    ) -> AsyncIterator[RestApisTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetRestApis.html#APIGateway.Paginator.GetRestApis.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getrestapispaginator)
        """

class GetSdkTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetSdkTypes.html#APIGateway.Paginator.GetSdkTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getsdktypespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetSdkTypesRequestGetSdkTypesPaginateTypeDef]
    ) -> AsyncIterator[SdkTypesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetSdkTypes.html#APIGateway.Paginator.GetSdkTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getsdktypespaginator)
        """

class GetUsagePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsage.html#APIGateway.Paginator.GetUsage)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getusagepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetUsageRequestGetUsagePaginateTypeDef]
    ) -> AsyncIterator[UsageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsage.html#APIGateway.Paginator.GetUsage.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getusagepaginator)
        """

class GetUsagePlanKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsagePlanKeys.html#APIGateway.Paginator.GetUsagePlanKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getusageplankeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetUsagePlanKeysRequestGetUsagePlanKeysPaginateTypeDef]
    ) -> AsyncIterator[UsagePlanKeysTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsagePlanKeys.html#APIGateway.Paginator.GetUsagePlanKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getusageplankeyspaginator)
        """

class GetUsagePlansPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsagePlans.html#APIGateway.Paginator.GetUsagePlans)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getusageplanspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetUsagePlansRequestGetUsagePlansPaginateTypeDef]
    ) -> AsyncIterator[UsagePlansTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsagePlans.html#APIGateway.Paginator.GetUsagePlans.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getusageplanspaginator)
        """

class GetVpcLinksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetVpcLinks.html#APIGateway.Paginator.GetVpcLinks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getvpclinkspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetVpcLinksRequestGetVpcLinksPaginateTypeDef]
    ) -> AsyncIterator[VpcLinksTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetVpcLinks.html#APIGateway.Paginator.GetVpcLinks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getvpclinkspaginator)
        """
