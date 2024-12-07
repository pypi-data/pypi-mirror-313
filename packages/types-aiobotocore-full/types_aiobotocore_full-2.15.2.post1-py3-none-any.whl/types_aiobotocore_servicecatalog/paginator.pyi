"""
Type annotations for servicecatalog service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_servicecatalog.client import ServiceCatalogClient
    from types_aiobotocore_servicecatalog.paginator import (
        ListAcceptedPortfolioSharesPaginator,
        ListConstraintsForPortfolioPaginator,
        ListLaunchPathsPaginator,
        ListOrganizationPortfolioAccessPaginator,
        ListPortfoliosForProductPaginator,
        ListPortfoliosPaginator,
        ListPrincipalsForPortfolioPaginator,
        ListProvisionedProductPlansPaginator,
        ListProvisioningArtifactsForServiceActionPaginator,
        ListRecordHistoryPaginator,
        ListResourcesForTagOptionPaginator,
        ListServiceActionsForProvisioningArtifactPaginator,
        ListServiceActionsPaginator,
        ListTagOptionsPaginator,
        ScanProvisionedProductsPaginator,
        SearchProductsAsAdminPaginator,
    )

    session = get_session()
    with session.create_client("servicecatalog") as client:
        client: ServiceCatalogClient

        list_accepted_portfolio_shares_paginator: ListAcceptedPortfolioSharesPaginator = client.get_paginator("list_accepted_portfolio_shares")
        list_constraints_for_portfolio_paginator: ListConstraintsForPortfolioPaginator = client.get_paginator("list_constraints_for_portfolio")
        list_launch_paths_paginator: ListLaunchPathsPaginator = client.get_paginator("list_launch_paths")
        list_organization_portfolio_access_paginator: ListOrganizationPortfolioAccessPaginator = client.get_paginator("list_organization_portfolio_access")
        list_portfolios_for_product_paginator: ListPortfoliosForProductPaginator = client.get_paginator("list_portfolios_for_product")
        list_portfolios_paginator: ListPortfoliosPaginator = client.get_paginator("list_portfolios")
        list_principals_for_portfolio_paginator: ListPrincipalsForPortfolioPaginator = client.get_paginator("list_principals_for_portfolio")
        list_provisioned_product_plans_paginator: ListProvisionedProductPlansPaginator = client.get_paginator("list_provisioned_product_plans")
        list_provisioning_artifacts_for_service_action_paginator: ListProvisioningArtifactsForServiceActionPaginator = client.get_paginator("list_provisioning_artifacts_for_service_action")
        list_record_history_paginator: ListRecordHistoryPaginator = client.get_paginator("list_record_history")
        list_resources_for_tag_option_paginator: ListResourcesForTagOptionPaginator = client.get_paginator("list_resources_for_tag_option")
        list_service_actions_for_provisioning_artifact_paginator: ListServiceActionsForProvisioningArtifactPaginator = client.get_paginator("list_service_actions_for_provisioning_artifact")
        list_service_actions_paginator: ListServiceActionsPaginator = client.get_paginator("list_service_actions")
        list_tag_options_paginator: ListTagOptionsPaginator = client.get_paginator("list_tag_options")
        scan_provisioned_products_paginator: ScanProvisionedProductsPaginator = client.get_paginator("scan_provisioned_products")
        search_products_as_admin_paginator: SearchProductsAsAdminPaginator = client.get_paginator("search_products_as_admin")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAcceptedPortfolioSharesInputListAcceptedPortfolioSharesPaginateTypeDef,
    ListAcceptedPortfolioSharesOutputTypeDef,
    ListConstraintsForPortfolioInputListConstraintsForPortfolioPaginateTypeDef,
    ListConstraintsForPortfolioOutputTypeDef,
    ListLaunchPathsInputListLaunchPathsPaginateTypeDef,
    ListLaunchPathsOutputTypeDef,
    ListOrganizationPortfolioAccessInputListOrganizationPortfolioAccessPaginateTypeDef,
    ListOrganizationPortfolioAccessOutputTypeDef,
    ListPortfoliosForProductInputListPortfoliosForProductPaginateTypeDef,
    ListPortfoliosForProductOutputTypeDef,
    ListPortfoliosInputListPortfoliosPaginateTypeDef,
    ListPortfoliosOutputTypeDef,
    ListPrincipalsForPortfolioInputListPrincipalsForPortfolioPaginateTypeDef,
    ListPrincipalsForPortfolioOutputTypeDef,
    ListProvisionedProductPlansInputListProvisionedProductPlansPaginateTypeDef,
    ListProvisionedProductPlansOutputTypeDef,
    ListProvisioningArtifactsForServiceActionInputListProvisioningArtifactsForServiceActionPaginateTypeDef,
    ListProvisioningArtifactsForServiceActionOutputTypeDef,
    ListRecordHistoryInputListRecordHistoryPaginateTypeDef,
    ListRecordHistoryOutputTypeDef,
    ListResourcesForTagOptionInputListResourcesForTagOptionPaginateTypeDef,
    ListResourcesForTagOptionOutputTypeDef,
    ListServiceActionsForProvisioningArtifactInputListServiceActionsForProvisioningArtifactPaginateTypeDef,
    ListServiceActionsForProvisioningArtifactOutputTypeDef,
    ListServiceActionsInputListServiceActionsPaginateTypeDef,
    ListServiceActionsOutputTypeDef,
    ListTagOptionsInputListTagOptionsPaginateTypeDef,
    ListTagOptionsOutputTypeDef,
    ScanProvisionedProductsInputScanProvisionedProductsPaginateTypeDef,
    ScanProvisionedProductsOutputTypeDef,
    SearchProductsAsAdminInputSearchProductsAsAdminPaginateTypeDef,
    SearchProductsAsAdminOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAcceptedPortfolioSharesPaginator",
    "ListConstraintsForPortfolioPaginator",
    "ListLaunchPathsPaginator",
    "ListOrganizationPortfolioAccessPaginator",
    "ListPortfoliosForProductPaginator",
    "ListPortfoliosPaginator",
    "ListPrincipalsForPortfolioPaginator",
    "ListProvisionedProductPlansPaginator",
    "ListProvisioningArtifactsForServiceActionPaginator",
    "ListRecordHistoryPaginator",
    "ListResourcesForTagOptionPaginator",
    "ListServiceActionsForProvisioningArtifactPaginator",
    "ListServiceActionsPaginator",
    "ListTagOptionsPaginator",
    "ScanProvisionedProductsPaginator",
    "SearchProductsAsAdminPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAcceptedPortfolioSharesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListAcceptedPortfolioShares.html#ServiceCatalog.Paginator.ListAcceptedPortfolioShares)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listacceptedportfoliosharespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAcceptedPortfolioSharesInputListAcceptedPortfolioSharesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAcceptedPortfolioSharesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListAcceptedPortfolioShares.html#ServiceCatalog.Paginator.ListAcceptedPortfolioShares.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listacceptedportfoliosharespaginator)
        """

class ListConstraintsForPortfolioPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListConstraintsForPortfolio.html#ServiceCatalog.Paginator.ListConstraintsForPortfolio)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listconstraintsforportfoliopaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListConstraintsForPortfolioInputListConstraintsForPortfolioPaginateTypeDef
        ],
    ) -> AsyncIterator[ListConstraintsForPortfolioOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListConstraintsForPortfolio.html#ServiceCatalog.Paginator.ListConstraintsForPortfolio.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listconstraintsforportfoliopaginator)
        """

class ListLaunchPathsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListLaunchPaths.html#ServiceCatalog.Paginator.ListLaunchPaths)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listlaunchpathspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLaunchPathsInputListLaunchPathsPaginateTypeDef]
    ) -> AsyncIterator[ListLaunchPathsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListLaunchPaths.html#ServiceCatalog.Paginator.ListLaunchPaths.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listlaunchpathspaginator)
        """

class ListOrganizationPortfolioAccessPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListOrganizationPortfolioAccess.html#ServiceCatalog.Paginator.ListOrganizationPortfolioAccess)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listorganizationportfolioaccesspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListOrganizationPortfolioAccessInputListOrganizationPortfolioAccessPaginateTypeDef
        ],
    ) -> AsyncIterator[ListOrganizationPortfolioAccessOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListOrganizationPortfolioAccess.html#ServiceCatalog.Paginator.ListOrganizationPortfolioAccess.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listorganizationportfolioaccesspaginator)
        """

class ListPortfoliosForProductPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPortfoliosForProduct.html#ServiceCatalog.Paginator.ListPortfoliosForProduct)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listportfoliosforproductpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPortfoliosForProductInputListPortfoliosForProductPaginateTypeDef]
    ) -> AsyncIterator[ListPortfoliosForProductOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPortfoliosForProduct.html#ServiceCatalog.Paginator.ListPortfoliosForProduct.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listportfoliosforproductpaginator)
        """

class ListPortfoliosPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPortfolios.html#ServiceCatalog.Paginator.ListPortfolios)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listportfoliospaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPortfoliosInputListPortfoliosPaginateTypeDef]
    ) -> AsyncIterator[ListPortfoliosOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPortfolios.html#ServiceCatalog.Paginator.ListPortfolios.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listportfoliospaginator)
        """

class ListPrincipalsForPortfolioPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPrincipalsForPortfolio.html#ServiceCatalog.Paginator.ListPrincipalsForPortfolio)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprincipalsforportfoliopaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListPrincipalsForPortfolioInputListPrincipalsForPortfolioPaginateTypeDef],
    ) -> AsyncIterator[ListPrincipalsForPortfolioOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPrincipalsForPortfolio.html#ServiceCatalog.Paginator.ListPrincipalsForPortfolio.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprincipalsforportfoliopaginator)
        """

class ListProvisionedProductPlansPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListProvisionedProductPlans.html#ServiceCatalog.Paginator.ListProvisionedProductPlans)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprovisionedproductplanspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListProvisionedProductPlansInputListProvisionedProductPlansPaginateTypeDef
        ],
    ) -> AsyncIterator[ListProvisionedProductPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListProvisionedProductPlans.html#ServiceCatalog.Paginator.ListProvisionedProductPlans.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprovisionedproductplanspaginator)
        """

class ListProvisioningArtifactsForServiceActionPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListProvisioningArtifactsForServiceAction.html#ServiceCatalog.Paginator.ListProvisioningArtifactsForServiceAction)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprovisioningartifactsforserviceactionpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListProvisioningArtifactsForServiceActionInputListProvisioningArtifactsForServiceActionPaginateTypeDef
        ],
    ) -> AsyncIterator[ListProvisioningArtifactsForServiceActionOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListProvisioningArtifactsForServiceAction.html#ServiceCatalog.Paginator.ListProvisioningArtifactsForServiceAction.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprovisioningartifactsforserviceactionpaginator)
        """

class ListRecordHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListRecordHistory.html#ServiceCatalog.Paginator.ListRecordHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listrecordhistorypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRecordHistoryInputListRecordHistoryPaginateTypeDef]
    ) -> AsyncIterator[ListRecordHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListRecordHistory.html#ServiceCatalog.Paginator.ListRecordHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listrecordhistorypaginator)
        """

class ListResourcesForTagOptionPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListResourcesForTagOption.html#ServiceCatalog.Paginator.ListResourcesForTagOption)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listresourcesfortagoptionpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListResourcesForTagOptionInputListResourcesForTagOptionPaginateTypeDef],
    ) -> AsyncIterator[ListResourcesForTagOptionOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListResourcesForTagOption.html#ServiceCatalog.Paginator.ListResourcesForTagOption.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listresourcesfortagoptionpaginator)
        """

class ListServiceActionsForProvisioningArtifactPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListServiceActionsForProvisioningArtifact.html#ServiceCatalog.Paginator.ListServiceActionsForProvisioningArtifact)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listserviceactionsforprovisioningartifactpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListServiceActionsForProvisioningArtifactInputListServiceActionsForProvisioningArtifactPaginateTypeDef
        ],
    ) -> AsyncIterator[ListServiceActionsForProvisioningArtifactOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListServiceActionsForProvisioningArtifact.html#ServiceCatalog.Paginator.ListServiceActionsForProvisioningArtifact.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listserviceactionsforprovisioningartifactpaginator)
        """

class ListServiceActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListServiceActions.html#ServiceCatalog.Paginator.ListServiceActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listserviceactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServiceActionsInputListServiceActionsPaginateTypeDef]
    ) -> AsyncIterator[ListServiceActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListServiceActions.html#ServiceCatalog.Paginator.ListServiceActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listserviceactionspaginator)
        """

class ListTagOptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListTagOptions.html#ServiceCatalog.Paginator.ListTagOptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listtagoptionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagOptionsInputListTagOptionsPaginateTypeDef]
    ) -> AsyncIterator[ListTagOptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListTagOptions.html#ServiceCatalog.Paginator.ListTagOptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listtagoptionspaginator)
        """

class ScanProvisionedProductsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ScanProvisionedProducts.html#ServiceCatalog.Paginator.ScanProvisionedProducts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#scanprovisionedproductspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ScanProvisionedProductsInputScanProvisionedProductsPaginateTypeDef]
    ) -> AsyncIterator[ScanProvisionedProductsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ScanProvisionedProducts.html#ServiceCatalog.Paginator.ScanProvisionedProducts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#scanprovisionedproductspaginator)
        """

class SearchProductsAsAdminPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/SearchProductsAsAdmin.html#ServiceCatalog.Paginator.SearchProductsAsAdmin)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#searchproductsasadminpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchProductsAsAdminInputSearchProductsAsAdminPaginateTypeDef]
    ) -> AsyncIterator[SearchProductsAsAdminOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/SearchProductsAsAdmin.html#ServiceCatalog.Paginator.SearchProductsAsAdmin.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#searchproductsasadminpaginator)
        """
