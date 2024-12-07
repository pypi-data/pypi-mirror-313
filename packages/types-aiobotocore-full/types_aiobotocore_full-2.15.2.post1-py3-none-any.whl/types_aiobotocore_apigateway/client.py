"""
Type annotations for apigateway service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_apigateway.client import APIGatewayClient

    session = get_session()
    async with session.create_client("apigateway") as client:
        client: APIGatewayClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
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
from .type_defs import (
    AccountTypeDef,
    ApiKeyIdsTypeDef,
    ApiKeyResponseTypeDef,
    ApiKeysTypeDef,
    AuthorizerResponseTypeDef,
    AuthorizersTypeDef,
    BasePathMappingResponseTypeDef,
    BasePathMappingsTypeDef,
    ClientCertificateResponseTypeDef,
    ClientCertificatesTypeDef,
    CreateApiKeyRequestRequestTypeDef,
    CreateAuthorizerRequestRequestTypeDef,
    CreateBasePathMappingRequestRequestTypeDef,
    CreateDeploymentRequestRequestTypeDef,
    CreateDocumentationPartRequestRequestTypeDef,
    CreateDocumentationVersionRequestRequestTypeDef,
    CreateDomainNameRequestRequestTypeDef,
    CreateModelRequestRequestTypeDef,
    CreateRequestValidatorRequestRequestTypeDef,
    CreateResourceRequestRequestTypeDef,
    CreateRestApiRequestRequestTypeDef,
    CreateStageRequestRequestTypeDef,
    CreateUsagePlanKeyRequestRequestTypeDef,
    CreateUsagePlanRequestRequestTypeDef,
    CreateVpcLinkRequestRequestTypeDef,
    DeleteApiKeyRequestRequestTypeDef,
    DeleteAuthorizerRequestRequestTypeDef,
    DeleteBasePathMappingRequestRequestTypeDef,
    DeleteClientCertificateRequestRequestTypeDef,
    DeleteDeploymentRequestRequestTypeDef,
    DeleteDocumentationPartRequestRequestTypeDef,
    DeleteDocumentationVersionRequestRequestTypeDef,
    DeleteDomainNameRequestRequestTypeDef,
    DeleteGatewayResponseRequestRequestTypeDef,
    DeleteIntegrationRequestRequestTypeDef,
    DeleteIntegrationResponseRequestRequestTypeDef,
    DeleteMethodRequestRequestTypeDef,
    DeleteMethodResponseRequestRequestTypeDef,
    DeleteModelRequestRequestTypeDef,
    DeleteRequestValidatorRequestRequestTypeDef,
    DeleteResourceRequestRequestTypeDef,
    DeleteRestApiRequestRequestTypeDef,
    DeleteStageRequestRequestTypeDef,
    DeleteUsagePlanKeyRequestRequestTypeDef,
    DeleteUsagePlanRequestRequestTypeDef,
    DeleteVpcLinkRequestRequestTypeDef,
    DeploymentResponseTypeDef,
    DeploymentsTypeDef,
    DocumentationPartIdsTypeDef,
    DocumentationPartResponseTypeDef,
    DocumentationPartsTypeDef,
    DocumentationVersionResponseTypeDef,
    DocumentationVersionsTypeDef,
    DomainNameResponseTypeDef,
    DomainNamesTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportResponseTypeDef,
    FlushStageAuthorizersCacheRequestRequestTypeDef,
    FlushStageCacheRequestRequestTypeDef,
    GatewayResponseResponseTypeDef,
    GatewayResponsesTypeDef,
    GenerateClientCertificateRequestRequestTypeDef,
    GetApiKeyRequestRequestTypeDef,
    GetApiKeysRequestRequestTypeDef,
    GetAuthorizerRequestRequestTypeDef,
    GetAuthorizersRequestRequestTypeDef,
    GetBasePathMappingRequestRequestTypeDef,
    GetBasePathMappingsRequestRequestTypeDef,
    GetClientCertificateRequestRequestTypeDef,
    GetClientCertificatesRequestRequestTypeDef,
    GetDeploymentRequestRequestTypeDef,
    GetDeploymentsRequestRequestTypeDef,
    GetDocumentationPartRequestRequestTypeDef,
    GetDocumentationPartsRequestRequestTypeDef,
    GetDocumentationVersionRequestRequestTypeDef,
    GetDocumentationVersionsRequestRequestTypeDef,
    GetDomainNameRequestRequestTypeDef,
    GetDomainNamesRequestRequestTypeDef,
    GetExportRequestRequestTypeDef,
    GetGatewayResponseRequestRequestTypeDef,
    GetGatewayResponsesRequestRequestTypeDef,
    GetIntegrationRequestRequestTypeDef,
    GetIntegrationResponseRequestRequestTypeDef,
    GetMethodRequestRequestTypeDef,
    GetMethodResponseRequestRequestTypeDef,
    GetModelRequestRequestTypeDef,
    GetModelsRequestRequestTypeDef,
    GetModelTemplateRequestRequestTypeDef,
    GetRequestValidatorRequestRequestTypeDef,
    GetRequestValidatorsRequestRequestTypeDef,
    GetResourceRequestRequestTypeDef,
    GetResourcesRequestRequestTypeDef,
    GetRestApiRequestRequestTypeDef,
    GetRestApisRequestRequestTypeDef,
    GetSdkRequestRequestTypeDef,
    GetSdkTypeRequestRequestTypeDef,
    GetSdkTypesRequestRequestTypeDef,
    GetStageRequestRequestTypeDef,
    GetStagesRequestRequestTypeDef,
    GetTagsRequestRequestTypeDef,
    GetUsagePlanKeyRequestRequestTypeDef,
    GetUsagePlanKeysRequestRequestTypeDef,
    GetUsagePlanRequestRequestTypeDef,
    GetUsagePlansRequestRequestTypeDef,
    GetUsageRequestRequestTypeDef,
    GetVpcLinkRequestRequestTypeDef,
    GetVpcLinksRequestRequestTypeDef,
    ImportApiKeysRequestRequestTypeDef,
    ImportDocumentationPartsRequestRequestTypeDef,
    ImportRestApiRequestRequestTypeDef,
    IntegrationExtraResponseTypeDef,
    IntegrationResponseResponseTypeDef,
    MethodExtraResponseTypeDef,
    MethodResponseResponseTypeDef,
    ModelResponseTypeDef,
    ModelsTypeDef,
    PutGatewayResponseRequestRequestTypeDef,
    PutIntegrationRequestRequestTypeDef,
    PutIntegrationResponseRequestRequestTypeDef,
    PutMethodRequestRequestTypeDef,
    PutMethodResponseRequestRequestTypeDef,
    PutRestApiRequestRequestTypeDef,
    RequestValidatorResponseTypeDef,
    RequestValidatorsTypeDef,
    ResourceResponseTypeDef,
    ResourcesTypeDef,
    RestApiResponseTypeDef,
    RestApisTypeDef,
    SdkResponseTypeDef,
    SdkTypeResponseTypeDef,
    SdkTypesTypeDef,
    StageResponseTypeDef,
    StagesTypeDef,
    TagResourceRequestRequestTypeDef,
    TagsTypeDef,
    TemplateTypeDef,
    TestInvokeAuthorizerRequestRequestTypeDef,
    TestInvokeAuthorizerResponseTypeDef,
    TestInvokeMethodRequestRequestTypeDef,
    TestInvokeMethodResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAccountRequestRequestTypeDef,
    UpdateApiKeyRequestRequestTypeDef,
    UpdateAuthorizerRequestRequestTypeDef,
    UpdateBasePathMappingRequestRequestTypeDef,
    UpdateClientCertificateRequestRequestTypeDef,
    UpdateDeploymentRequestRequestTypeDef,
    UpdateDocumentationPartRequestRequestTypeDef,
    UpdateDocumentationVersionRequestRequestTypeDef,
    UpdateDomainNameRequestRequestTypeDef,
    UpdateGatewayResponseRequestRequestTypeDef,
    UpdateIntegrationRequestRequestTypeDef,
    UpdateIntegrationResponseRequestRequestTypeDef,
    UpdateMethodRequestRequestTypeDef,
    UpdateMethodResponseRequestRequestTypeDef,
    UpdateModelRequestRequestTypeDef,
    UpdateRequestValidatorRequestRequestTypeDef,
    UpdateResourceRequestRequestTypeDef,
    UpdateRestApiRequestRequestTypeDef,
    UpdateStageRequestRequestTypeDef,
    UpdateUsagePlanRequestRequestTypeDef,
    UpdateUsageRequestRequestTypeDef,
    UpdateVpcLinkRequestRequestTypeDef,
    UsagePlanKeyResponseTypeDef,
    UsagePlanKeysTypeDef,
    UsagePlanResponseTypeDef,
    UsagePlansTypeDef,
    UsageTypeDef,
    VpcLinkResponseTypeDef,
    VpcLinksTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("APIGatewayClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class APIGatewayClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        APIGatewayClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#close)
        """

    async def create_api_key(
        self, **kwargs: Unpack[CreateApiKeyRequestRequestTypeDef]
    ) -> ApiKeyResponseTypeDef:
        """
        Create an ApiKey resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_api_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_api_key)
        """

    async def create_authorizer(
        self, **kwargs: Unpack[CreateAuthorizerRequestRequestTypeDef]
    ) -> AuthorizerResponseTypeDef:
        """
        Adds a new Authorizer resource to an existing RestApi resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_authorizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_authorizer)
        """

    async def create_base_path_mapping(
        self, **kwargs: Unpack[CreateBasePathMappingRequestRequestTypeDef]
    ) -> BasePathMappingResponseTypeDef:
        """
        Creates a new BasePathMapping resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_base_path_mapping.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_base_path_mapping)
        """

    async def create_deployment(
        self, **kwargs: Unpack[CreateDeploymentRequestRequestTypeDef]
    ) -> DeploymentResponseTypeDef:
        """
        Creates a Deployment resource, which makes a specified RestApi callable over
        the internet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_deployment)
        """

    async def create_documentation_part(
        self, **kwargs: Unpack[CreateDocumentationPartRequestRequestTypeDef]
    ) -> DocumentationPartResponseTypeDef:
        """
        Creates a documentation part.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_documentation_part.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_documentation_part)
        """

    async def create_documentation_version(
        self, **kwargs: Unpack[CreateDocumentationVersionRequestRequestTypeDef]
    ) -> DocumentationVersionResponseTypeDef:
        """
        Creates a documentation version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_documentation_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_documentation_version)
        """

    async def create_domain_name(
        self, **kwargs: Unpack[CreateDomainNameRequestRequestTypeDef]
    ) -> DomainNameResponseTypeDef:
        """
        Creates a new domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_domain_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_domain_name)
        """

    async def create_model(
        self, **kwargs: Unpack[CreateModelRequestRequestTypeDef]
    ) -> ModelResponseTypeDef:
        """
        Adds a new Model resource to an existing RestApi resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_model)
        """

    async def create_request_validator(
        self, **kwargs: Unpack[CreateRequestValidatorRequestRequestTypeDef]
    ) -> RequestValidatorResponseTypeDef:
        """
        Creates a RequestValidator of a given RestApi.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_request_validator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_request_validator)
        """

    async def create_resource(
        self, **kwargs: Unpack[CreateResourceRequestRequestTypeDef]
    ) -> ResourceResponseTypeDef:
        """
        Creates a Resource resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_resource)
        """

    async def create_rest_api(
        self, **kwargs: Unpack[CreateRestApiRequestRequestTypeDef]
    ) -> RestApiResponseTypeDef:
        """
        Creates a new RestApi resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_rest_api.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_rest_api)
        """

    async def create_stage(
        self, **kwargs: Unpack[CreateStageRequestRequestTypeDef]
    ) -> StageResponseTypeDef:
        """
        Creates a new Stage resource that references a pre-existing Deployment for the
        API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_stage)
        """

    async def create_usage_plan(
        self, **kwargs: Unpack[CreateUsagePlanRequestRequestTypeDef]
    ) -> UsagePlanResponseTypeDef:
        """
        Creates a usage plan with the throttle and quota limits, as well as the
        associated API stages, specified in the payload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_usage_plan.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_usage_plan)
        """

    async def create_usage_plan_key(
        self, **kwargs: Unpack[CreateUsagePlanKeyRequestRequestTypeDef]
    ) -> UsagePlanKeyResponseTypeDef:
        """
        Creates a usage plan key for adding an existing API key to a usage plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_usage_plan_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_usage_plan_key)
        """

    async def create_vpc_link(
        self, **kwargs: Unpack[CreateVpcLinkRequestRequestTypeDef]
    ) -> VpcLinkResponseTypeDef:
        """
        Creates a VPC link, under the caller's account in a selected region, in an
        asynchronous operation that typically takes 2-4 minutes to complete and become
        operational.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/create_vpc_link.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_vpc_link)
        """

    async def delete_api_key(
        self, **kwargs: Unpack[DeleteApiKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the ApiKey resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_api_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_api_key)
        """

    async def delete_authorizer(
        self, **kwargs: Unpack[DeleteAuthorizerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an existing Authorizer resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_authorizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_authorizer)
        """

    async def delete_base_path_mapping(
        self, **kwargs: Unpack[DeleteBasePathMappingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the BasePathMapping resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_base_path_mapping.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_base_path_mapping)
        """

    async def delete_client_certificate(
        self, **kwargs: Unpack[DeleteClientCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the ClientCertificate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_client_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_client_certificate)
        """

    async def delete_deployment(
        self, **kwargs: Unpack[DeleteDeploymentRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Deployment resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_deployment)
        """

    async def delete_documentation_part(
        self, **kwargs: Unpack[DeleteDocumentationPartRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a documentation part.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_documentation_part.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_documentation_part)
        """

    async def delete_documentation_version(
        self, **kwargs: Unpack[DeleteDocumentationVersionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a documentation version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_documentation_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_documentation_version)
        """

    async def delete_domain_name(
        self, **kwargs: Unpack[DeleteDomainNameRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the DomainName resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_domain_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_domain_name)
        """

    async def delete_gateway_response(
        self, **kwargs: Unpack[DeleteGatewayResponseRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Clears any customization of a GatewayResponse of a specified response type on
        the given RestApi and resets it with the default settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_gateway_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_gateway_response)
        """

    async def delete_integration(
        self, **kwargs: Unpack[DeleteIntegrationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Represents a delete integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_integration)
        """

    async def delete_integration_response(
        self, **kwargs: Unpack[DeleteIntegrationResponseRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Represents a delete integration response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_integration_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_integration_response)
        """

    async def delete_method(
        self, **kwargs: Unpack[DeleteMethodRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an existing Method resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_method.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_method)
        """

    async def delete_method_response(
        self, **kwargs: Unpack[DeleteMethodResponseRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an existing MethodResponse resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_method_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_method_response)
        """

    async def delete_model(
        self, **kwargs: Unpack[DeleteModelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_model)
        """

    async def delete_request_validator(
        self, **kwargs: Unpack[DeleteRequestValidatorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a RequestValidator of a given RestApi.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_request_validator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_request_validator)
        """

    async def delete_resource(
        self, **kwargs: Unpack[DeleteResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Resource resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_resource)
        """

    async def delete_rest_api(
        self, **kwargs: Unpack[DeleteRestApiRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_rest_api.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_rest_api)
        """

    async def delete_stage(
        self, **kwargs: Unpack[DeleteStageRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Stage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_stage)
        """

    async def delete_usage_plan(
        self, **kwargs: Unpack[DeleteUsagePlanRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a usage plan of a given plan Id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_usage_plan.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_usage_plan)
        """

    async def delete_usage_plan_key(
        self, **kwargs: Unpack[DeleteUsagePlanKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a usage plan key and remove the underlying API key from the associated
        usage plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_usage_plan_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_usage_plan_key)
        """

    async def delete_vpc_link(
        self, **kwargs: Unpack[DeleteVpcLinkRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an existing VpcLink of a specified identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/delete_vpc_link.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_vpc_link)
        """

    async def flush_stage_authorizers_cache(
        self, **kwargs: Unpack[FlushStageAuthorizersCacheRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Flushes all authorizer cache entries on a stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/flush_stage_authorizers_cache.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#flush_stage_authorizers_cache)
        """

    async def flush_stage_cache(
        self, **kwargs: Unpack[FlushStageCacheRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Flushes a stage's cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/flush_stage_cache.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#flush_stage_cache)
        """

    async def generate_client_certificate(
        self, **kwargs: Unpack[GenerateClientCertificateRequestRequestTypeDef]
    ) -> ClientCertificateResponseTypeDef:
        """
        Generates a ClientCertificate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/generate_client_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#generate_client_certificate)
        """

    async def get_account(self) -> AccountTypeDef:
        """
        Gets information about the current Account resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_account)
        """

    async def get_api_key(
        self, **kwargs: Unpack[GetApiKeyRequestRequestTypeDef]
    ) -> ApiKeyResponseTypeDef:
        """
        Gets information about the current ApiKey resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_api_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_api_key)
        """

    async def get_api_keys(
        self, **kwargs: Unpack[GetApiKeysRequestRequestTypeDef]
    ) -> ApiKeysTypeDef:
        """
        Gets information about the current ApiKeys resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_api_keys.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_api_keys)
        """

    async def get_authorizer(
        self, **kwargs: Unpack[GetAuthorizerRequestRequestTypeDef]
    ) -> AuthorizerResponseTypeDef:
        """
        Describe an existing Authorizer resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_authorizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_authorizer)
        """

    async def get_authorizers(
        self, **kwargs: Unpack[GetAuthorizersRequestRequestTypeDef]
    ) -> AuthorizersTypeDef:
        """
        Describe an existing Authorizers resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_authorizers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_authorizers)
        """

    async def get_base_path_mapping(
        self, **kwargs: Unpack[GetBasePathMappingRequestRequestTypeDef]
    ) -> BasePathMappingResponseTypeDef:
        """
        Describe a BasePathMapping resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_base_path_mapping.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_base_path_mapping)
        """

    async def get_base_path_mappings(
        self, **kwargs: Unpack[GetBasePathMappingsRequestRequestTypeDef]
    ) -> BasePathMappingsTypeDef:
        """
        Represents a collection of BasePathMapping resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_base_path_mappings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_base_path_mappings)
        """

    async def get_client_certificate(
        self, **kwargs: Unpack[GetClientCertificateRequestRequestTypeDef]
    ) -> ClientCertificateResponseTypeDef:
        """
        Gets information about the current ClientCertificate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_client_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_client_certificate)
        """

    async def get_client_certificates(
        self, **kwargs: Unpack[GetClientCertificatesRequestRequestTypeDef]
    ) -> ClientCertificatesTypeDef:
        """
        Gets a collection of ClientCertificate resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_client_certificates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_client_certificates)
        """

    async def get_deployment(
        self, **kwargs: Unpack[GetDeploymentRequestRequestTypeDef]
    ) -> DeploymentResponseTypeDef:
        """
        Gets information about a Deployment resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_deployment)
        """

    async def get_deployments(
        self, **kwargs: Unpack[GetDeploymentsRequestRequestTypeDef]
    ) -> DeploymentsTypeDef:
        """
        Gets information about a Deployments collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_deployments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_deployments)
        """

    async def get_documentation_part(
        self, **kwargs: Unpack[GetDocumentationPartRequestRequestTypeDef]
    ) -> DocumentationPartResponseTypeDef:
        """
        Gets a documentation part.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_documentation_part.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_documentation_part)
        """

    async def get_documentation_parts(
        self, **kwargs: Unpack[GetDocumentationPartsRequestRequestTypeDef]
    ) -> DocumentationPartsTypeDef:
        """
        Gets documentation parts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_documentation_parts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_documentation_parts)
        """

    async def get_documentation_version(
        self, **kwargs: Unpack[GetDocumentationVersionRequestRequestTypeDef]
    ) -> DocumentationVersionResponseTypeDef:
        """
        Gets a documentation version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_documentation_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_documentation_version)
        """

    async def get_documentation_versions(
        self, **kwargs: Unpack[GetDocumentationVersionsRequestRequestTypeDef]
    ) -> DocumentationVersionsTypeDef:
        """
        Gets documentation versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_documentation_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_documentation_versions)
        """

    async def get_domain_name(
        self, **kwargs: Unpack[GetDomainNameRequestRequestTypeDef]
    ) -> DomainNameResponseTypeDef:
        """
        Represents a domain name that is contained in a simpler, more intuitive URL
        that can be called.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_domain_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_domain_name)
        """

    async def get_domain_names(
        self, **kwargs: Unpack[GetDomainNamesRequestRequestTypeDef]
    ) -> DomainNamesTypeDef:
        """
        Represents a collection of DomainName resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_domain_names.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_domain_names)
        """

    async def get_export(
        self, **kwargs: Unpack[GetExportRequestRequestTypeDef]
    ) -> ExportResponseTypeDef:
        """
        Exports a deployed version of a RestApi in a specified format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_export)
        """

    async def get_gateway_response(
        self, **kwargs: Unpack[GetGatewayResponseRequestRequestTypeDef]
    ) -> GatewayResponseResponseTypeDef:
        """
        Gets a GatewayResponse of a specified response type on the given RestApi.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_gateway_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_gateway_response)
        """

    async def get_gateway_responses(
        self, **kwargs: Unpack[GetGatewayResponsesRequestRequestTypeDef]
    ) -> GatewayResponsesTypeDef:
        """
        Gets the GatewayResponses collection on the given RestApi.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_gateway_responses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_gateway_responses)
        """

    async def get_integration(
        self, **kwargs: Unpack[GetIntegrationRequestRequestTypeDef]
    ) -> IntegrationExtraResponseTypeDef:
        """
        Get the integration settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_integration)
        """

    async def get_integration_response(
        self, **kwargs: Unpack[GetIntegrationResponseRequestRequestTypeDef]
    ) -> IntegrationResponseResponseTypeDef:
        """
        Represents a get integration response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_integration_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_integration_response)
        """

    async def get_method(
        self, **kwargs: Unpack[GetMethodRequestRequestTypeDef]
    ) -> MethodExtraResponseTypeDef:
        """
        Describe an existing Method resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_method.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_method)
        """

    async def get_method_response(
        self, **kwargs: Unpack[GetMethodResponseRequestRequestTypeDef]
    ) -> MethodResponseResponseTypeDef:
        """
        Describes a MethodResponse resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_method_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_method_response)
        """

    async def get_model(
        self, **kwargs: Unpack[GetModelRequestRequestTypeDef]
    ) -> ModelResponseTypeDef:
        """
        Describes an existing model defined for a RestApi resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_model)
        """

    async def get_model_template(
        self, **kwargs: Unpack[GetModelTemplateRequestRequestTypeDef]
    ) -> TemplateTypeDef:
        """
        Generates a sample mapping template that can be used to transform a payload
        into the structure of a model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_model_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_model_template)
        """

    async def get_models(self, **kwargs: Unpack[GetModelsRequestRequestTypeDef]) -> ModelsTypeDef:
        """
        Describes existing Models defined for a RestApi resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_models.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_models)
        """

    async def get_request_validator(
        self, **kwargs: Unpack[GetRequestValidatorRequestRequestTypeDef]
    ) -> RequestValidatorResponseTypeDef:
        """
        Gets a RequestValidator of a given RestApi.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_request_validator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_request_validator)
        """

    async def get_request_validators(
        self, **kwargs: Unpack[GetRequestValidatorsRequestRequestTypeDef]
    ) -> RequestValidatorsTypeDef:
        """
        Gets the RequestValidators collection of a given RestApi.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_request_validators.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_request_validators)
        """

    async def get_resource(
        self, **kwargs: Unpack[GetResourceRequestRequestTypeDef]
    ) -> ResourceResponseTypeDef:
        """
        Lists information about a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_resource)
        """

    async def get_resources(
        self, **kwargs: Unpack[GetResourcesRequestRequestTypeDef]
    ) -> ResourcesTypeDef:
        """
        Lists information about a collection of Resource resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_resources)
        """

    async def get_rest_api(
        self, **kwargs: Unpack[GetRestApiRequestRequestTypeDef]
    ) -> RestApiResponseTypeDef:
        """
        Lists the RestApi resource in the collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_rest_api.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_rest_api)
        """

    async def get_rest_apis(
        self, **kwargs: Unpack[GetRestApisRequestRequestTypeDef]
    ) -> RestApisTypeDef:
        """
        Lists the RestApis resources for your collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_rest_apis.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_rest_apis)
        """

    async def get_sdk(self, **kwargs: Unpack[GetSdkRequestRequestTypeDef]) -> SdkResponseTypeDef:
        """
        Generates a client SDK for a RestApi and Stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_sdk.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_sdk)
        """

    async def get_sdk_type(
        self, **kwargs: Unpack[GetSdkTypeRequestRequestTypeDef]
    ) -> SdkTypeResponseTypeDef:
        """
        Gets an SDK type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_sdk_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_sdk_type)
        """

    async def get_sdk_types(
        self, **kwargs: Unpack[GetSdkTypesRequestRequestTypeDef]
    ) -> SdkTypesTypeDef:
        """
        Gets SDK types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_sdk_types.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_sdk_types)
        """

    async def get_stage(
        self, **kwargs: Unpack[GetStageRequestRequestTypeDef]
    ) -> StageResponseTypeDef:
        """
        Gets information about a Stage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_stage)
        """

    async def get_stages(self, **kwargs: Unpack[GetStagesRequestRequestTypeDef]) -> StagesTypeDef:
        """
        Gets information about one or more Stage resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_stages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_stages)
        """

    async def get_tags(self, **kwargs: Unpack[GetTagsRequestRequestTypeDef]) -> TagsTypeDef:
        """
        Gets the Tags collection for a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_tags)
        """

    async def get_usage(self, **kwargs: Unpack[GetUsageRequestRequestTypeDef]) -> UsageTypeDef:
        """
        Gets the usage data of a usage plan in a specified time interval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_usage)
        """

    async def get_usage_plan(
        self, **kwargs: Unpack[GetUsagePlanRequestRequestTypeDef]
    ) -> UsagePlanResponseTypeDef:
        """
        Gets a usage plan of a given plan identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_usage_plan.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_usage_plan)
        """

    async def get_usage_plan_key(
        self, **kwargs: Unpack[GetUsagePlanKeyRequestRequestTypeDef]
    ) -> UsagePlanKeyResponseTypeDef:
        """
        Gets a usage plan key of a given key identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_usage_plan_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_usage_plan_key)
        """

    async def get_usage_plan_keys(
        self, **kwargs: Unpack[GetUsagePlanKeysRequestRequestTypeDef]
    ) -> UsagePlanKeysTypeDef:
        """
        Gets all the usage plan keys representing the API keys added to a specified
        usage plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_usage_plan_keys.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_usage_plan_keys)
        """

    async def get_usage_plans(
        self, **kwargs: Unpack[GetUsagePlansRequestRequestTypeDef]
    ) -> UsagePlansTypeDef:
        """
        Gets all the usage plans of the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_usage_plans.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_usage_plans)
        """

    async def get_vpc_link(
        self, **kwargs: Unpack[GetVpcLinkRequestRequestTypeDef]
    ) -> VpcLinkResponseTypeDef:
        """
        Gets a specified VPC link under the caller's account in a region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_vpc_link.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_vpc_link)
        """

    async def get_vpc_links(
        self, **kwargs: Unpack[GetVpcLinksRequestRequestTypeDef]
    ) -> VpcLinksTypeDef:
        """
        Gets the VpcLinks collection under the caller's account in a selected region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_vpc_links.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_vpc_links)
        """

    async def import_api_keys(
        self, **kwargs: Unpack[ImportApiKeysRequestRequestTypeDef]
    ) -> ApiKeyIdsTypeDef:
        """
        Import API keys from an external source, such as a CSV-formatted file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/import_api_keys.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#import_api_keys)
        """

    async def import_documentation_parts(
        self, **kwargs: Unpack[ImportDocumentationPartsRequestRequestTypeDef]
    ) -> DocumentationPartIdsTypeDef:
        """
        Imports documentation parts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/import_documentation_parts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#import_documentation_parts)
        """

    async def import_rest_api(
        self, **kwargs: Unpack[ImportRestApiRequestRequestTypeDef]
    ) -> RestApiResponseTypeDef:
        """
        A feature of the API Gateway control service for creating a new API from an
        external API definition file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/import_rest_api.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#import_rest_api)
        """

    async def put_gateway_response(
        self, **kwargs: Unpack[PutGatewayResponseRequestRequestTypeDef]
    ) -> GatewayResponseResponseTypeDef:
        """
        Creates a customization of a GatewayResponse of a specified response type and
        status code on the given RestApi.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/put_gateway_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#put_gateway_response)
        """

    async def put_integration(
        self, **kwargs: Unpack[PutIntegrationRequestRequestTypeDef]
    ) -> IntegrationExtraResponseTypeDef:
        """
        Sets up a method's integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/put_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#put_integration)
        """

    async def put_integration_response(
        self, **kwargs: Unpack[PutIntegrationResponseRequestRequestTypeDef]
    ) -> IntegrationResponseResponseTypeDef:
        """
        Represents a put integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/put_integration_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#put_integration_response)
        """

    async def put_method(
        self, **kwargs: Unpack[PutMethodRequestRequestTypeDef]
    ) -> MethodExtraResponseTypeDef:
        """
        Add a method to an existing Resource resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/put_method.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#put_method)
        """

    async def put_method_response(
        self, **kwargs: Unpack[PutMethodResponseRequestRequestTypeDef]
    ) -> MethodResponseResponseTypeDef:
        """
        Adds a MethodResponse to an existing Method resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/put_method_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#put_method_response)
        """

    async def put_rest_api(
        self, **kwargs: Unpack[PutRestApiRequestRequestTypeDef]
    ) -> RestApiResponseTypeDef:
        """
        A feature of the API Gateway control service for updating an existing API with
        an input of external API definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/put_rest_api.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#put_rest_api)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates a tag on a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#tag_resource)
        """

    async def test_invoke_authorizer(
        self, **kwargs: Unpack[TestInvokeAuthorizerRequestRequestTypeDef]
    ) -> TestInvokeAuthorizerResponseTypeDef:
        """
        Simulate the execution of an Authorizer in your RestApi with headers,
        parameters, and an incoming request body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/test_invoke_authorizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#test_invoke_authorizer)
        """

    async def test_invoke_method(
        self, **kwargs: Unpack[TestInvokeMethodRequestRequestTypeDef]
    ) -> TestInvokeMethodResponseTypeDef:
        """
        Simulate the invocation of a Method in your RestApi with headers, parameters,
        and an incoming request body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/test_invoke_method.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#test_invoke_method)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a tag from a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#untag_resource)
        """

    async def update_account(
        self, **kwargs: Unpack[UpdateAccountRequestRequestTypeDef]
    ) -> AccountTypeDef:
        """
        Changes information about the current Account resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_account)
        """

    async def update_api_key(
        self, **kwargs: Unpack[UpdateApiKeyRequestRequestTypeDef]
    ) -> ApiKeyResponseTypeDef:
        """
        Changes information about an ApiKey resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_api_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_api_key)
        """

    async def update_authorizer(
        self, **kwargs: Unpack[UpdateAuthorizerRequestRequestTypeDef]
    ) -> AuthorizerResponseTypeDef:
        """
        Updates an existing Authorizer resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_authorizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_authorizer)
        """

    async def update_base_path_mapping(
        self, **kwargs: Unpack[UpdateBasePathMappingRequestRequestTypeDef]
    ) -> BasePathMappingResponseTypeDef:
        """
        Changes information about the BasePathMapping resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_base_path_mapping.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_base_path_mapping)
        """

    async def update_client_certificate(
        self, **kwargs: Unpack[UpdateClientCertificateRequestRequestTypeDef]
    ) -> ClientCertificateResponseTypeDef:
        """
        Changes information about an ClientCertificate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_client_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_client_certificate)
        """

    async def update_deployment(
        self, **kwargs: Unpack[UpdateDeploymentRequestRequestTypeDef]
    ) -> DeploymentResponseTypeDef:
        """
        Changes information about a Deployment resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_deployment)
        """

    async def update_documentation_part(
        self, **kwargs: Unpack[UpdateDocumentationPartRequestRequestTypeDef]
    ) -> DocumentationPartResponseTypeDef:
        """
        Updates a documentation part.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_documentation_part.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_documentation_part)
        """

    async def update_documentation_version(
        self, **kwargs: Unpack[UpdateDocumentationVersionRequestRequestTypeDef]
    ) -> DocumentationVersionResponseTypeDef:
        """
        Updates a documentation version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_documentation_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_documentation_version)
        """

    async def update_domain_name(
        self, **kwargs: Unpack[UpdateDomainNameRequestRequestTypeDef]
    ) -> DomainNameResponseTypeDef:
        """
        Changes information about the DomainName resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_domain_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_domain_name)
        """

    async def update_gateway_response(
        self, **kwargs: Unpack[UpdateGatewayResponseRequestRequestTypeDef]
    ) -> GatewayResponseResponseTypeDef:
        """
        Updates a GatewayResponse of a specified response type on the given RestApi.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_gateway_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_gateway_response)
        """

    async def update_integration(
        self, **kwargs: Unpack[UpdateIntegrationRequestRequestTypeDef]
    ) -> IntegrationExtraResponseTypeDef:
        """
        Represents an update integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_integration)
        """

    async def update_integration_response(
        self, **kwargs: Unpack[UpdateIntegrationResponseRequestRequestTypeDef]
    ) -> IntegrationResponseResponseTypeDef:
        """
        Represents an update integration response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_integration_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_integration_response)
        """

    async def update_method(
        self, **kwargs: Unpack[UpdateMethodRequestRequestTypeDef]
    ) -> MethodExtraResponseTypeDef:
        """
        Updates an existing Method resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_method.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_method)
        """

    async def update_method_response(
        self, **kwargs: Unpack[UpdateMethodResponseRequestRequestTypeDef]
    ) -> MethodResponseResponseTypeDef:
        """
        Updates an existing MethodResponse resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_method_response.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_method_response)
        """

    async def update_model(
        self, **kwargs: Unpack[UpdateModelRequestRequestTypeDef]
    ) -> ModelResponseTypeDef:
        """
        Changes information about a model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_model)
        """

    async def update_request_validator(
        self, **kwargs: Unpack[UpdateRequestValidatorRequestRequestTypeDef]
    ) -> RequestValidatorResponseTypeDef:
        """
        Updates a RequestValidator of a given RestApi.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_request_validator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_request_validator)
        """

    async def update_resource(
        self, **kwargs: Unpack[UpdateResourceRequestRequestTypeDef]
    ) -> ResourceResponseTypeDef:
        """
        Changes information about a Resource resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_resource)
        """

    async def update_rest_api(
        self, **kwargs: Unpack[UpdateRestApiRequestRequestTypeDef]
    ) -> RestApiResponseTypeDef:
        """
        Changes information about the specified API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_rest_api.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_rest_api)
        """

    async def update_stage(
        self, **kwargs: Unpack[UpdateStageRequestRequestTypeDef]
    ) -> StageResponseTypeDef:
        """
        Changes information about a Stage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_stage)
        """

    async def update_usage(
        self, **kwargs: Unpack[UpdateUsageRequestRequestTypeDef]
    ) -> UsageTypeDef:
        """
        Grants a temporary extension to the remaining quota of a usage plan associated
        with a specified API key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_usage)
        """

    async def update_usage_plan(
        self, **kwargs: Unpack[UpdateUsagePlanRequestRequestTypeDef]
    ) -> UsagePlanResponseTypeDef:
        """
        Updates a usage plan of a given plan Id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_usage_plan.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_usage_plan)
        """

    async def update_vpc_link(
        self, **kwargs: Unpack[UpdateVpcLinkRequestRequestTypeDef]
    ) -> VpcLinkResponseTypeDef:
        """
        Updates an existing VpcLink of a specified identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/update_vpc_link.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_vpc_link)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_api_keys"]) -> GetApiKeysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_authorizers"]) -> GetAuthorizersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_base_path_mappings"]
    ) -> GetBasePathMappingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_client_certificates"]
    ) -> GetClientCertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_deployments"]) -> GetDeploymentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_documentation_parts"]
    ) -> GetDocumentationPartsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_documentation_versions"]
    ) -> GetDocumentationVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_domain_names"]) -> GetDomainNamesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_gateway_responses"]
    ) -> GetGatewayResponsesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_models"]) -> GetModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_request_validators"]
    ) -> GetRequestValidatorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_resources"]) -> GetResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_rest_apis"]) -> GetRestApisPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_sdk_types"]) -> GetSdkTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_usage"]) -> GetUsagePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_usage_plan_keys"]
    ) -> GetUsagePlanKeysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_usage_plans"]) -> GetUsagePlansPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_vpc_links"]) -> GetVpcLinksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    async def __aenter__(self) -> "APIGatewayClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/)
        """
