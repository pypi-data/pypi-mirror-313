"""
Type annotations for route53resolver service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53resolver.client import Route53ResolverClient
    from types_aiobotocore_route53resolver.paginator import (
        ListFirewallConfigsPaginator,
        ListFirewallDomainListsPaginator,
        ListFirewallDomainsPaginator,
        ListFirewallRuleGroupAssociationsPaginator,
        ListFirewallRuleGroupsPaginator,
        ListFirewallRulesPaginator,
        ListOutpostResolversPaginator,
        ListResolverConfigsPaginator,
        ListResolverDnssecConfigsPaginator,
        ListResolverEndpointIpAddressesPaginator,
        ListResolverEndpointsPaginator,
        ListResolverQueryLogConfigAssociationsPaginator,
        ListResolverQueryLogConfigsPaginator,
        ListResolverRuleAssociationsPaginator,
        ListResolverRulesPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    with session.create_client("route53resolver") as client:
        client: Route53ResolverClient

        list_firewall_configs_paginator: ListFirewallConfigsPaginator = client.get_paginator("list_firewall_configs")
        list_firewall_domain_lists_paginator: ListFirewallDomainListsPaginator = client.get_paginator("list_firewall_domain_lists")
        list_firewall_domains_paginator: ListFirewallDomainsPaginator = client.get_paginator("list_firewall_domains")
        list_firewall_rule_group_associations_paginator: ListFirewallRuleGroupAssociationsPaginator = client.get_paginator("list_firewall_rule_group_associations")
        list_firewall_rule_groups_paginator: ListFirewallRuleGroupsPaginator = client.get_paginator("list_firewall_rule_groups")
        list_firewall_rules_paginator: ListFirewallRulesPaginator = client.get_paginator("list_firewall_rules")
        list_outpost_resolvers_paginator: ListOutpostResolversPaginator = client.get_paginator("list_outpost_resolvers")
        list_resolver_configs_paginator: ListResolverConfigsPaginator = client.get_paginator("list_resolver_configs")
        list_resolver_dnssec_configs_paginator: ListResolverDnssecConfigsPaginator = client.get_paginator("list_resolver_dnssec_configs")
        list_resolver_endpoint_ip_addresses_paginator: ListResolverEndpointIpAddressesPaginator = client.get_paginator("list_resolver_endpoint_ip_addresses")
        list_resolver_endpoints_paginator: ListResolverEndpointsPaginator = client.get_paginator("list_resolver_endpoints")
        list_resolver_query_log_config_associations_paginator: ListResolverQueryLogConfigAssociationsPaginator = client.get_paginator("list_resolver_query_log_config_associations")
        list_resolver_query_log_configs_paginator: ListResolverQueryLogConfigsPaginator = client.get_paginator("list_resolver_query_log_configs")
        list_resolver_rule_associations_paginator: ListResolverRuleAssociationsPaginator = client.get_paginator("list_resolver_rule_associations")
        list_resolver_rules_paginator: ListResolverRulesPaginator = client.get_paginator("list_resolver_rules")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListFirewallConfigsRequestListFirewallConfigsPaginateTypeDef,
    ListFirewallConfigsResponseTypeDef,
    ListFirewallDomainListsRequestListFirewallDomainListsPaginateTypeDef,
    ListFirewallDomainListsResponseTypeDef,
    ListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef,
    ListFirewallDomainsResponseTypeDef,
    ListFirewallRuleGroupAssociationsRequestListFirewallRuleGroupAssociationsPaginateTypeDef,
    ListFirewallRuleGroupAssociationsResponseTypeDef,
    ListFirewallRuleGroupsRequestListFirewallRuleGroupsPaginateTypeDef,
    ListFirewallRuleGroupsResponseTypeDef,
    ListFirewallRulesRequestListFirewallRulesPaginateTypeDef,
    ListFirewallRulesResponseTypeDef,
    ListOutpostResolversRequestListOutpostResolversPaginateTypeDef,
    ListOutpostResolversResponseTypeDef,
    ListResolverConfigsRequestListResolverConfigsPaginateTypeDef,
    ListResolverConfigsResponseTypeDef,
    ListResolverDnssecConfigsRequestListResolverDnssecConfigsPaginateTypeDef,
    ListResolverDnssecConfigsResponseTypeDef,
    ListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef,
    ListResolverEndpointIpAddressesResponseTypeDef,
    ListResolverEndpointsRequestListResolverEndpointsPaginateTypeDef,
    ListResolverEndpointsResponseTypeDef,
    ListResolverQueryLogConfigAssociationsRequestListResolverQueryLogConfigAssociationsPaginateTypeDef,
    ListResolverQueryLogConfigAssociationsResponseTypeDef,
    ListResolverQueryLogConfigsRequestListResolverQueryLogConfigsPaginateTypeDef,
    ListResolverQueryLogConfigsResponseTypeDef,
    ListResolverRuleAssociationsRequestListResolverRuleAssociationsPaginateTypeDef,
    ListResolverRuleAssociationsResponseTypeDef,
    ListResolverRulesRequestListResolverRulesPaginateTypeDef,
    ListResolverRulesResponseTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListFirewallConfigsPaginator",
    "ListFirewallDomainListsPaginator",
    "ListFirewallDomainsPaginator",
    "ListFirewallRuleGroupAssociationsPaginator",
    "ListFirewallRuleGroupsPaginator",
    "ListFirewallRulesPaginator",
    "ListOutpostResolversPaginator",
    "ListResolverConfigsPaginator",
    "ListResolverDnssecConfigsPaginator",
    "ListResolverEndpointIpAddressesPaginator",
    "ListResolverEndpointsPaginator",
    "ListResolverQueryLogConfigAssociationsPaginator",
    "ListResolverQueryLogConfigsPaginator",
    "ListResolverRuleAssociationsPaginator",
    "ListResolverRulesPaginator",
    "ListTagsForResourcePaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListFirewallConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallConfigs.html#Route53Resolver.Paginator.ListFirewallConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listfirewallconfigspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFirewallConfigsRequestListFirewallConfigsPaginateTypeDef]
    ) -> AsyncIterator[ListFirewallConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallConfigs.html#Route53Resolver.Paginator.ListFirewallConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listfirewallconfigspaginator)
        """


class ListFirewallDomainListsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallDomainLists.html#Route53Resolver.Paginator.ListFirewallDomainLists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listfirewalldomainlistspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFirewallDomainListsRequestListFirewallDomainListsPaginateTypeDef]
    ) -> AsyncIterator[ListFirewallDomainListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallDomainLists.html#Route53Resolver.Paginator.ListFirewallDomainLists.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listfirewalldomainlistspaginator)
        """


class ListFirewallDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallDomains.html#Route53Resolver.Paginator.ListFirewallDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listfirewalldomainspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFirewallDomainsRequestListFirewallDomainsPaginateTypeDef]
    ) -> AsyncIterator[ListFirewallDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallDomains.html#Route53Resolver.Paginator.ListFirewallDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listfirewalldomainspaginator)
        """


class ListFirewallRuleGroupAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallRuleGroupAssociations.html#Route53Resolver.Paginator.ListFirewallRuleGroupAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listfirewallrulegroupassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListFirewallRuleGroupAssociationsRequestListFirewallRuleGroupAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListFirewallRuleGroupAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallRuleGroupAssociations.html#Route53Resolver.Paginator.ListFirewallRuleGroupAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listfirewallrulegroupassociationspaginator)
        """


class ListFirewallRuleGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallRuleGroups.html#Route53Resolver.Paginator.ListFirewallRuleGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listfirewallrulegroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFirewallRuleGroupsRequestListFirewallRuleGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListFirewallRuleGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallRuleGroups.html#Route53Resolver.Paginator.ListFirewallRuleGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listfirewallrulegroupspaginator)
        """


class ListFirewallRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallRules.html#Route53Resolver.Paginator.ListFirewallRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listfirewallrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFirewallRulesRequestListFirewallRulesPaginateTypeDef]
    ) -> AsyncIterator[ListFirewallRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListFirewallRules.html#Route53Resolver.Paginator.ListFirewallRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listfirewallrulespaginator)
        """


class ListOutpostResolversPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListOutpostResolvers.html#Route53Resolver.Paginator.ListOutpostResolvers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listoutpostresolverspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOutpostResolversRequestListOutpostResolversPaginateTypeDef]
    ) -> AsyncIterator[ListOutpostResolversResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListOutpostResolvers.html#Route53Resolver.Paginator.ListOutpostResolvers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listoutpostresolverspaginator)
        """


class ListResolverConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverConfigs.html#Route53Resolver.Paginator.ListResolverConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverconfigspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResolverConfigsRequestListResolverConfigsPaginateTypeDef]
    ) -> AsyncIterator[ListResolverConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverConfigs.html#Route53Resolver.Paginator.ListResolverConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverconfigspaginator)
        """


class ListResolverDnssecConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverDnssecConfigs.html#Route53Resolver.Paginator.ListResolverDnssecConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverdnssecconfigspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListResolverDnssecConfigsRequestListResolverDnssecConfigsPaginateTypeDef],
    ) -> AsyncIterator[ListResolverDnssecConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverDnssecConfigs.html#Route53Resolver.Paginator.ListResolverDnssecConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverdnssecconfigspaginator)
        """


class ListResolverEndpointIpAddressesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverEndpointIpAddresses.html#Route53Resolver.Paginator.ListResolverEndpointIpAddresses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverendpointipaddressespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResolverEndpointIpAddressesRequestListResolverEndpointIpAddressesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListResolverEndpointIpAddressesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverEndpointIpAddresses.html#Route53Resolver.Paginator.ListResolverEndpointIpAddresses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverendpointipaddressespaginator)
        """


class ListResolverEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverEndpoints.html#Route53Resolver.Paginator.ListResolverEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverendpointspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResolverEndpointsRequestListResolverEndpointsPaginateTypeDef]
    ) -> AsyncIterator[ListResolverEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverEndpoints.html#Route53Resolver.Paginator.ListResolverEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverendpointspaginator)
        """


class ListResolverQueryLogConfigAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverQueryLogConfigAssociations.html#Route53Resolver.Paginator.ListResolverQueryLogConfigAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverquerylogconfigassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResolverQueryLogConfigAssociationsRequestListResolverQueryLogConfigAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListResolverQueryLogConfigAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverQueryLogConfigAssociations.html#Route53Resolver.Paginator.ListResolverQueryLogConfigAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverquerylogconfigassociationspaginator)
        """


class ListResolverQueryLogConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverQueryLogConfigs.html#Route53Resolver.Paginator.ListResolverQueryLogConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverquerylogconfigspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResolverQueryLogConfigsRequestListResolverQueryLogConfigsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListResolverQueryLogConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverQueryLogConfigs.html#Route53Resolver.Paginator.ListResolverQueryLogConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverquerylogconfigspaginator)
        """


class ListResolverRuleAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverRuleAssociations.html#Route53Resolver.Paginator.ListResolverRuleAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverruleassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResolverRuleAssociationsRequestListResolverRuleAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListResolverRuleAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverRuleAssociations.html#Route53Resolver.Paginator.ListResolverRuleAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverruleassociationspaginator)
        """


class ListResolverRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverRules.html#Route53Resolver.Paginator.ListResolverRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResolverRulesRequestListResolverRulesPaginateTypeDef]
    ) -> AsyncIterator[ListResolverRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListResolverRules.html#Route53Resolver.Paginator.ListResolverRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listresolverrulespaginator)
        """


class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListTagsForResource.html#Route53Resolver.Paginator.ListTagsForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> AsyncIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver/paginator/ListTagsForResource.html#Route53Resolver.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53resolver/paginators/#listtagsforresourcepaginator)
        """
