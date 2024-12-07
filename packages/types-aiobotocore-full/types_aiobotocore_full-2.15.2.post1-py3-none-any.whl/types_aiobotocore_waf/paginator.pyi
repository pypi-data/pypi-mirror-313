"""
Type annotations for waf service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_waf.client import WAFClient
    from types_aiobotocore_waf.paginator import (
        GetRateBasedRuleManagedKeysPaginator,
        ListActivatedRulesInRuleGroupPaginator,
        ListByteMatchSetsPaginator,
        ListGeoMatchSetsPaginator,
        ListIPSetsPaginator,
        ListLoggingConfigurationsPaginator,
        ListRateBasedRulesPaginator,
        ListRegexMatchSetsPaginator,
        ListRegexPatternSetsPaginator,
        ListRuleGroupsPaginator,
        ListRulesPaginator,
        ListSizeConstraintSetsPaginator,
        ListSqlInjectionMatchSetsPaginator,
        ListSubscribedRuleGroupsPaginator,
        ListWebACLsPaginator,
        ListXssMatchSetsPaginator,
    )

    session = get_session()
    with session.create_client("waf") as client:
        client: WAFClient

        get_rate_based_rule_managed_keys_paginator: GetRateBasedRuleManagedKeysPaginator = client.get_paginator("get_rate_based_rule_managed_keys")
        list_activated_rules_in_rule_group_paginator: ListActivatedRulesInRuleGroupPaginator = client.get_paginator("list_activated_rules_in_rule_group")
        list_byte_match_sets_paginator: ListByteMatchSetsPaginator = client.get_paginator("list_byte_match_sets")
        list_geo_match_sets_paginator: ListGeoMatchSetsPaginator = client.get_paginator("list_geo_match_sets")
        list_ip_sets_paginator: ListIPSetsPaginator = client.get_paginator("list_ip_sets")
        list_logging_configurations_paginator: ListLoggingConfigurationsPaginator = client.get_paginator("list_logging_configurations")
        list_rate_based_rules_paginator: ListRateBasedRulesPaginator = client.get_paginator("list_rate_based_rules")
        list_regex_match_sets_paginator: ListRegexMatchSetsPaginator = client.get_paginator("list_regex_match_sets")
        list_regex_pattern_sets_paginator: ListRegexPatternSetsPaginator = client.get_paginator("list_regex_pattern_sets")
        list_rule_groups_paginator: ListRuleGroupsPaginator = client.get_paginator("list_rule_groups")
        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
        list_size_constraint_sets_paginator: ListSizeConstraintSetsPaginator = client.get_paginator("list_size_constraint_sets")
        list_sql_injection_match_sets_paginator: ListSqlInjectionMatchSetsPaginator = client.get_paginator("list_sql_injection_match_sets")
        list_subscribed_rule_groups_paginator: ListSubscribedRuleGroupsPaginator = client.get_paginator("list_subscribed_rule_groups")
        list_web_acls_paginator: ListWebACLsPaginator = client.get_paginator("list_web_acls")
        list_xss_match_sets_paginator: ListXssMatchSetsPaginator = client.get_paginator("list_xss_match_sets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetRateBasedRuleManagedKeysRequestGetRateBasedRuleManagedKeysPaginateTypeDef,
    GetRateBasedRuleManagedKeysResponseTypeDef,
    ListActivatedRulesInRuleGroupRequestListActivatedRulesInRuleGroupPaginateTypeDef,
    ListActivatedRulesInRuleGroupResponseTypeDef,
    ListByteMatchSetsRequestListByteMatchSetsPaginateTypeDef,
    ListByteMatchSetsResponseTypeDef,
    ListGeoMatchSetsRequestListGeoMatchSetsPaginateTypeDef,
    ListGeoMatchSetsResponseTypeDef,
    ListIPSetsRequestListIPSetsPaginateTypeDef,
    ListIPSetsResponseTypeDef,
    ListLoggingConfigurationsRequestListLoggingConfigurationsPaginateTypeDef,
    ListLoggingConfigurationsResponseTypeDef,
    ListRateBasedRulesRequestListRateBasedRulesPaginateTypeDef,
    ListRateBasedRulesResponseTypeDef,
    ListRegexMatchSetsRequestListRegexMatchSetsPaginateTypeDef,
    ListRegexMatchSetsResponseTypeDef,
    ListRegexPatternSetsRequestListRegexPatternSetsPaginateTypeDef,
    ListRegexPatternSetsResponseTypeDef,
    ListRuleGroupsRequestListRuleGroupsPaginateTypeDef,
    ListRuleGroupsResponseTypeDef,
    ListRulesRequestListRulesPaginateTypeDef,
    ListRulesResponseTypeDef,
    ListSizeConstraintSetsRequestListSizeConstraintSetsPaginateTypeDef,
    ListSizeConstraintSetsResponseTypeDef,
    ListSqlInjectionMatchSetsRequestListSqlInjectionMatchSetsPaginateTypeDef,
    ListSqlInjectionMatchSetsResponseTypeDef,
    ListSubscribedRuleGroupsRequestListSubscribedRuleGroupsPaginateTypeDef,
    ListSubscribedRuleGroupsResponseTypeDef,
    ListWebACLsRequestListWebACLsPaginateTypeDef,
    ListWebACLsResponseTypeDef,
    ListXssMatchSetsRequestListXssMatchSetsPaginateTypeDef,
    ListXssMatchSetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetRateBasedRuleManagedKeysPaginator",
    "ListActivatedRulesInRuleGroupPaginator",
    "ListByteMatchSetsPaginator",
    "ListGeoMatchSetsPaginator",
    "ListIPSetsPaginator",
    "ListLoggingConfigurationsPaginator",
    "ListRateBasedRulesPaginator",
    "ListRegexMatchSetsPaginator",
    "ListRegexPatternSetsPaginator",
    "ListRuleGroupsPaginator",
    "ListRulesPaginator",
    "ListSizeConstraintSetsPaginator",
    "ListSqlInjectionMatchSetsPaginator",
    "ListSubscribedRuleGroupsPaginator",
    "ListWebACLsPaginator",
    "ListXssMatchSetsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetRateBasedRuleManagedKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/GetRateBasedRuleManagedKeys.html#WAF.Paginator.GetRateBasedRuleManagedKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#getratebasedrulemanagedkeyspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetRateBasedRuleManagedKeysRequestGetRateBasedRuleManagedKeysPaginateTypeDef
        ],
    ) -> AsyncIterator[GetRateBasedRuleManagedKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/GetRateBasedRuleManagedKeys.html#WAF.Paginator.GetRateBasedRuleManagedKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#getratebasedrulemanagedkeyspaginator)
        """

class ListActivatedRulesInRuleGroupPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListActivatedRulesInRuleGroup.html#WAF.Paginator.ListActivatedRulesInRuleGroup)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listactivatedrulesinrulegrouppaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListActivatedRulesInRuleGroupRequestListActivatedRulesInRuleGroupPaginateTypeDef
        ],
    ) -> AsyncIterator[ListActivatedRulesInRuleGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListActivatedRulesInRuleGroup.html#WAF.Paginator.ListActivatedRulesInRuleGroup.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listactivatedrulesinrulegrouppaginator)
        """

class ListByteMatchSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListByteMatchSets.html#WAF.Paginator.ListByteMatchSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listbytematchsetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListByteMatchSetsRequestListByteMatchSetsPaginateTypeDef]
    ) -> AsyncIterator[ListByteMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListByteMatchSets.html#WAF.Paginator.ListByteMatchSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listbytematchsetspaginator)
        """

class ListGeoMatchSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListGeoMatchSets.html#WAF.Paginator.ListGeoMatchSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listgeomatchsetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGeoMatchSetsRequestListGeoMatchSetsPaginateTypeDef]
    ) -> AsyncIterator[ListGeoMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListGeoMatchSets.html#WAF.Paginator.ListGeoMatchSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listgeomatchsetspaginator)
        """

class ListIPSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListIPSets.html#WAF.Paginator.ListIPSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listipsetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIPSetsRequestListIPSetsPaginateTypeDef]
    ) -> AsyncIterator[ListIPSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListIPSets.html#WAF.Paginator.ListIPSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listipsetspaginator)
        """

class ListLoggingConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListLoggingConfigurations.html#WAF.Paginator.ListLoggingConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listloggingconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListLoggingConfigurationsRequestListLoggingConfigurationsPaginateTypeDef],
    ) -> AsyncIterator[ListLoggingConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListLoggingConfigurations.html#WAF.Paginator.ListLoggingConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listloggingconfigurationspaginator)
        """

class ListRateBasedRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRateBasedRules.html#WAF.Paginator.ListRateBasedRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listratebasedrulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRateBasedRulesRequestListRateBasedRulesPaginateTypeDef]
    ) -> AsyncIterator[ListRateBasedRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRateBasedRules.html#WAF.Paginator.ListRateBasedRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listratebasedrulespaginator)
        """

class ListRegexMatchSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRegexMatchSets.html#WAF.Paginator.ListRegexMatchSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listregexmatchsetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRegexMatchSetsRequestListRegexMatchSetsPaginateTypeDef]
    ) -> AsyncIterator[ListRegexMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRegexMatchSets.html#WAF.Paginator.ListRegexMatchSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listregexmatchsetspaginator)
        """

class ListRegexPatternSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRegexPatternSets.html#WAF.Paginator.ListRegexPatternSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listregexpatternsetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRegexPatternSetsRequestListRegexPatternSetsPaginateTypeDef]
    ) -> AsyncIterator[ListRegexPatternSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRegexPatternSets.html#WAF.Paginator.ListRegexPatternSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listregexpatternsetspaginator)
        """

class ListRuleGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRuleGroups.html#WAF.Paginator.ListRuleGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listrulegroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRuleGroupsRequestListRuleGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListRuleGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRuleGroups.html#WAF.Paginator.ListRuleGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listrulegroupspaginator)
        """

class ListRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRules.html#WAF.Paginator.ListRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listrulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRulesRequestListRulesPaginateTypeDef]
    ) -> AsyncIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRules.html#WAF.Paginator.ListRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listrulespaginator)
        """

class ListSizeConstraintSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSizeConstraintSets.html#WAF.Paginator.ListSizeConstraintSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listsizeconstraintsetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSizeConstraintSetsRequestListSizeConstraintSetsPaginateTypeDef]
    ) -> AsyncIterator[ListSizeConstraintSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSizeConstraintSets.html#WAF.Paginator.ListSizeConstraintSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listsizeconstraintsetspaginator)
        """

class ListSqlInjectionMatchSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSqlInjectionMatchSets.html#WAF.Paginator.ListSqlInjectionMatchSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listsqlinjectionmatchsetspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListSqlInjectionMatchSetsRequestListSqlInjectionMatchSetsPaginateTypeDef],
    ) -> AsyncIterator[ListSqlInjectionMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSqlInjectionMatchSets.html#WAF.Paginator.ListSqlInjectionMatchSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listsqlinjectionmatchsetspaginator)
        """

class ListSubscribedRuleGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSubscribedRuleGroups.html#WAF.Paginator.ListSubscribedRuleGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listsubscribedrulegroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListSubscribedRuleGroupsRequestListSubscribedRuleGroupsPaginateTypeDef],
    ) -> AsyncIterator[ListSubscribedRuleGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSubscribedRuleGroups.html#WAF.Paginator.ListSubscribedRuleGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listsubscribedrulegroupspaginator)
        """

class ListWebACLsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListWebACLs.html#WAF.Paginator.ListWebACLs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listwebaclspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWebACLsRequestListWebACLsPaginateTypeDef]
    ) -> AsyncIterator[ListWebACLsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListWebACLs.html#WAF.Paginator.ListWebACLs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listwebaclspaginator)
        """

class ListXssMatchSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListXssMatchSets.html#WAF.Paginator.ListXssMatchSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listxssmatchsetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListXssMatchSetsRequestListXssMatchSetsPaginateTypeDef]
    ) -> AsyncIterator[ListXssMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListXssMatchSets.html#WAF.Paginator.ListXssMatchSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listxssmatchsetspaginator)
        """
