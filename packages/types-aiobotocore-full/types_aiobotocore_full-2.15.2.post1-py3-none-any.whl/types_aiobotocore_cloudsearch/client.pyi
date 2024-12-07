"""
Type annotations for cloudsearch service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudsearch.client import CloudSearchClient

    session = get_session()
    async with session.create_client("cloudsearch") as client:
        client: CloudSearchClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    BuildSuggestersRequestRequestTypeDef,
    BuildSuggestersResponseTypeDef,
    CreateDomainRequestRequestTypeDef,
    CreateDomainResponseTypeDef,
    DefineAnalysisSchemeRequestRequestTypeDef,
    DefineAnalysisSchemeResponseTypeDef,
    DefineExpressionRequestRequestTypeDef,
    DefineExpressionResponseTypeDef,
    DefineIndexFieldRequestRequestTypeDef,
    DefineIndexFieldResponseTypeDef,
    DefineSuggesterRequestRequestTypeDef,
    DefineSuggesterResponseTypeDef,
    DeleteAnalysisSchemeRequestRequestTypeDef,
    DeleteAnalysisSchemeResponseTypeDef,
    DeleteDomainRequestRequestTypeDef,
    DeleteDomainResponseTypeDef,
    DeleteExpressionRequestRequestTypeDef,
    DeleteExpressionResponseTypeDef,
    DeleteIndexFieldRequestRequestTypeDef,
    DeleteIndexFieldResponseTypeDef,
    DeleteSuggesterRequestRequestTypeDef,
    DeleteSuggesterResponseTypeDef,
    DescribeAnalysisSchemesRequestRequestTypeDef,
    DescribeAnalysisSchemesResponseTypeDef,
    DescribeAvailabilityOptionsRequestRequestTypeDef,
    DescribeAvailabilityOptionsResponseTypeDef,
    DescribeDomainEndpointOptionsRequestRequestTypeDef,
    DescribeDomainEndpointOptionsResponseTypeDef,
    DescribeDomainsRequestRequestTypeDef,
    DescribeDomainsResponseTypeDef,
    DescribeExpressionsRequestRequestTypeDef,
    DescribeExpressionsResponseTypeDef,
    DescribeIndexFieldsRequestRequestTypeDef,
    DescribeIndexFieldsResponseTypeDef,
    DescribeScalingParametersRequestRequestTypeDef,
    DescribeScalingParametersResponseTypeDef,
    DescribeServiceAccessPoliciesRequestRequestTypeDef,
    DescribeServiceAccessPoliciesResponseTypeDef,
    DescribeSuggestersRequestRequestTypeDef,
    DescribeSuggestersResponseTypeDef,
    IndexDocumentsRequestRequestTypeDef,
    IndexDocumentsResponseTypeDef,
    ListDomainNamesResponseTypeDef,
    UpdateAvailabilityOptionsRequestRequestTypeDef,
    UpdateAvailabilityOptionsResponseTypeDef,
    UpdateDomainEndpointOptionsRequestRequestTypeDef,
    UpdateDomainEndpointOptionsResponseTypeDef,
    UpdateScalingParametersRequestRequestTypeDef,
    UpdateScalingParametersResponseTypeDef,
    UpdateServiceAccessPoliciesRequestRequestTypeDef,
    UpdateServiceAccessPoliciesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("CloudSearchClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BaseException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DisabledOperationException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidTypeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CloudSearchClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudSearchClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#close)
        """

    async def build_suggesters(
        self, **kwargs: Unpack[BuildSuggestersRequestRequestTypeDef]
    ) -> BuildSuggestersResponseTypeDef:
        """
        Indexes the search suggestions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/build_suggesters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#build_suggesters)
        """

    async def create_domain(
        self, **kwargs: Unpack[CreateDomainRequestRequestTypeDef]
    ) -> CreateDomainResponseTypeDef:
        """
        Creates a new search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/create_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#create_domain)
        """

    async def define_analysis_scheme(
        self, **kwargs: Unpack[DefineAnalysisSchemeRequestRequestTypeDef]
    ) -> DefineAnalysisSchemeResponseTypeDef:
        """
        Configures an analysis scheme that can be applied to a <code>text</code> or
        <code>text-array</code> field to define language-specific text processing
        options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/define_analysis_scheme.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#define_analysis_scheme)
        """

    async def define_expression(
        self, **kwargs: Unpack[DefineExpressionRequestRequestTypeDef]
    ) -> DefineExpressionResponseTypeDef:
        """
        Configures an <code><a>Expression</a></code> for the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/define_expression.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#define_expression)
        """

    async def define_index_field(
        self, **kwargs: Unpack[DefineIndexFieldRequestRequestTypeDef]
    ) -> DefineIndexFieldResponseTypeDef:
        """
        Configures an <code><a>IndexField</a></code> for the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/define_index_field.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#define_index_field)
        """

    async def define_suggester(
        self, **kwargs: Unpack[DefineSuggesterRequestRequestTypeDef]
    ) -> DefineSuggesterResponseTypeDef:
        """
        Configures a suggester for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/define_suggester.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#define_suggester)
        """

    async def delete_analysis_scheme(
        self, **kwargs: Unpack[DeleteAnalysisSchemeRequestRequestTypeDef]
    ) -> DeleteAnalysisSchemeResponseTypeDef:
        """
        Deletes an analysis scheme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/delete_analysis_scheme.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#delete_analysis_scheme)
        """

    async def delete_domain(
        self, **kwargs: Unpack[DeleteDomainRequestRequestTypeDef]
    ) -> DeleteDomainResponseTypeDef:
        """
        Permanently deletes a search domain and all of its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/delete_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#delete_domain)
        """

    async def delete_expression(
        self, **kwargs: Unpack[DeleteExpressionRequestRequestTypeDef]
    ) -> DeleteExpressionResponseTypeDef:
        """
        Removes an <code><a>Expression</a></code> from the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/delete_expression.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#delete_expression)
        """

    async def delete_index_field(
        self, **kwargs: Unpack[DeleteIndexFieldRequestRequestTypeDef]
    ) -> DeleteIndexFieldResponseTypeDef:
        """
        Removes an <code><a>IndexField</a></code> from the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/delete_index_field.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#delete_index_field)
        """

    async def delete_suggester(
        self, **kwargs: Unpack[DeleteSuggesterRequestRequestTypeDef]
    ) -> DeleteSuggesterResponseTypeDef:
        """
        Deletes a suggester.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/delete_suggester.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#delete_suggester)
        """

    async def describe_analysis_schemes(
        self, **kwargs: Unpack[DescribeAnalysisSchemesRequestRequestTypeDef]
    ) -> DescribeAnalysisSchemesResponseTypeDef:
        """
        Gets the analysis schemes configured for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_analysis_schemes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_analysis_schemes)
        """

    async def describe_availability_options(
        self, **kwargs: Unpack[DescribeAvailabilityOptionsRequestRequestTypeDef]
    ) -> DescribeAvailabilityOptionsResponseTypeDef:
        """
        Gets the availability options configured for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_availability_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_availability_options)
        """

    async def describe_domain_endpoint_options(
        self, **kwargs: Unpack[DescribeDomainEndpointOptionsRequestRequestTypeDef]
    ) -> DescribeDomainEndpointOptionsResponseTypeDef:
        """
        Returns the domain's endpoint options, specifically whether all requests to the
        domain must arrive over HTTPS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_domain_endpoint_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_domain_endpoint_options)
        """

    async def describe_domains(
        self, **kwargs: Unpack[DescribeDomainsRequestRequestTypeDef]
    ) -> DescribeDomainsResponseTypeDef:
        """
        Gets information about the search domains owned by this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_domains.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_domains)
        """

    async def describe_expressions(
        self, **kwargs: Unpack[DescribeExpressionsRequestRequestTypeDef]
    ) -> DescribeExpressionsResponseTypeDef:
        """
        Gets the expressions configured for the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_expressions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_expressions)
        """

    async def describe_index_fields(
        self, **kwargs: Unpack[DescribeIndexFieldsRequestRequestTypeDef]
    ) -> DescribeIndexFieldsResponseTypeDef:
        """
        Gets information about the index fields configured for the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_index_fields.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_index_fields)
        """

    async def describe_scaling_parameters(
        self, **kwargs: Unpack[DescribeScalingParametersRequestRequestTypeDef]
    ) -> DescribeScalingParametersResponseTypeDef:
        """
        Gets the scaling parameters configured for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_scaling_parameters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_scaling_parameters)
        """

    async def describe_service_access_policies(
        self, **kwargs: Unpack[DescribeServiceAccessPoliciesRequestRequestTypeDef]
    ) -> DescribeServiceAccessPoliciesResponseTypeDef:
        """
        Gets information about the access policies that control access to the domain's
        document and search endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_service_access_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_service_access_policies)
        """

    async def describe_suggesters(
        self, **kwargs: Unpack[DescribeSuggestersRequestRequestTypeDef]
    ) -> DescribeSuggestersResponseTypeDef:
        """
        Gets the suggesters configured for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_suggesters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_suggesters)
        """

    async def index_documents(
        self, **kwargs: Unpack[IndexDocumentsRequestRequestTypeDef]
    ) -> IndexDocumentsResponseTypeDef:
        """
        Tells the search domain to start indexing its documents using the latest
        indexing options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/index_documents.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#index_documents)
        """

    async def list_domain_names(self) -> ListDomainNamesResponseTypeDef:
        """
        Lists all search domains owned by an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/list_domain_names.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#list_domain_names)
        """

    async def update_availability_options(
        self, **kwargs: Unpack[UpdateAvailabilityOptionsRequestRequestTypeDef]
    ) -> UpdateAvailabilityOptionsResponseTypeDef:
        """
        Configures the availability options for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/update_availability_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#update_availability_options)
        """

    async def update_domain_endpoint_options(
        self, **kwargs: Unpack[UpdateDomainEndpointOptionsRequestRequestTypeDef]
    ) -> UpdateDomainEndpointOptionsResponseTypeDef:
        """
        Updates the domain's endpoint options, specifically whether all requests to the
        domain must arrive over HTTPS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/update_domain_endpoint_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#update_domain_endpoint_options)
        """

    async def update_scaling_parameters(
        self, **kwargs: Unpack[UpdateScalingParametersRequestRequestTypeDef]
    ) -> UpdateScalingParametersResponseTypeDef:
        """
        Configures scaling parameters for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/update_scaling_parameters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#update_scaling_parameters)
        """

    async def update_service_access_policies(
        self, **kwargs: Unpack[UpdateServiceAccessPoliciesRequestRequestTypeDef]
    ) -> UpdateServiceAccessPoliciesResponseTypeDef:
        """
        Configures the access rules that control access to the domain's document and
        search endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/update_service_access_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#update_service_access_policies)
        """

    async def __aenter__(self) -> "CloudSearchClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/)
        """
