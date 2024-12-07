"""
Type annotations for clouddirectory service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_clouddirectory.client import CloudDirectoryClient
    from types_aiobotocore_clouddirectory.paginator import (
        ListAppliedSchemaArnsPaginator,
        ListAttachedIndicesPaginator,
        ListDevelopmentSchemaArnsPaginator,
        ListDirectoriesPaginator,
        ListFacetAttributesPaginator,
        ListFacetNamesPaginator,
        ListIncomingTypedLinksPaginator,
        ListIndexPaginator,
        ListManagedSchemaArnsPaginator,
        ListObjectAttributesPaginator,
        ListObjectParentPathsPaginator,
        ListObjectPoliciesPaginator,
        ListOutgoingTypedLinksPaginator,
        ListPolicyAttachmentsPaginator,
        ListPublishedSchemaArnsPaginator,
        ListTagsForResourcePaginator,
        ListTypedLinkFacetAttributesPaginator,
        ListTypedLinkFacetNamesPaginator,
        LookupPolicyPaginator,
    )

    session = get_session()
    with session.create_client("clouddirectory") as client:
        client: CloudDirectoryClient

        list_applied_schema_arns_paginator: ListAppliedSchemaArnsPaginator = client.get_paginator("list_applied_schema_arns")
        list_attached_indices_paginator: ListAttachedIndicesPaginator = client.get_paginator("list_attached_indices")
        list_development_schema_arns_paginator: ListDevelopmentSchemaArnsPaginator = client.get_paginator("list_development_schema_arns")
        list_directories_paginator: ListDirectoriesPaginator = client.get_paginator("list_directories")
        list_facet_attributes_paginator: ListFacetAttributesPaginator = client.get_paginator("list_facet_attributes")
        list_facet_names_paginator: ListFacetNamesPaginator = client.get_paginator("list_facet_names")
        list_incoming_typed_links_paginator: ListIncomingTypedLinksPaginator = client.get_paginator("list_incoming_typed_links")
        list_index_paginator: ListIndexPaginator = client.get_paginator("list_index")
        list_managed_schema_arns_paginator: ListManagedSchemaArnsPaginator = client.get_paginator("list_managed_schema_arns")
        list_object_attributes_paginator: ListObjectAttributesPaginator = client.get_paginator("list_object_attributes")
        list_object_parent_paths_paginator: ListObjectParentPathsPaginator = client.get_paginator("list_object_parent_paths")
        list_object_policies_paginator: ListObjectPoliciesPaginator = client.get_paginator("list_object_policies")
        list_outgoing_typed_links_paginator: ListOutgoingTypedLinksPaginator = client.get_paginator("list_outgoing_typed_links")
        list_policy_attachments_paginator: ListPolicyAttachmentsPaginator = client.get_paginator("list_policy_attachments")
        list_published_schema_arns_paginator: ListPublishedSchemaArnsPaginator = client.get_paginator("list_published_schema_arns")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        list_typed_link_facet_attributes_paginator: ListTypedLinkFacetAttributesPaginator = client.get_paginator("list_typed_link_facet_attributes")
        list_typed_link_facet_names_paginator: ListTypedLinkFacetNamesPaginator = client.get_paginator("list_typed_link_facet_names")
        lookup_policy_paginator: LookupPolicyPaginator = client.get_paginator("lookup_policy")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAppliedSchemaArnsRequestListAppliedSchemaArnsPaginateTypeDef,
    ListAppliedSchemaArnsResponseTypeDef,
    ListAttachedIndicesRequestListAttachedIndicesPaginateTypeDef,
    ListAttachedIndicesResponseTypeDef,
    ListDevelopmentSchemaArnsRequestListDevelopmentSchemaArnsPaginateTypeDef,
    ListDevelopmentSchemaArnsResponseTypeDef,
    ListDirectoriesRequestListDirectoriesPaginateTypeDef,
    ListDirectoriesResponseTypeDef,
    ListFacetAttributesRequestListFacetAttributesPaginateTypeDef,
    ListFacetAttributesResponseTypeDef,
    ListFacetNamesRequestListFacetNamesPaginateTypeDef,
    ListFacetNamesResponseTypeDef,
    ListIncomingTypedLinksRequestListIncomingTypedLinksPaginateTypeDef,
    ListIncomingTypedLinksResponseTypeDef,
    ListIndexRequestListIndexPaginateTypeDef,
    ListIndexResponseTypeDef,
    ListManagedSchemaArnsRequestListManagedSchemaArnsPaginateTypeDef,
    ListManagedSchemaArnsResponseTypeDef,
    ListObjectAttributesRequestListObjectAttributesPaginateTypeDef,
    ListObjectAttributesResponseTypeDef,
    ListObjectParentPathsRequestListObjectParentPathsPaginateTypeDef,
    ListObjectParentPathsResponseTypeDef,
    ListObjectPoliciesRequestListObjectPoliciesPaginateTypeDef,
    ListObjectPoliciesResponseTypeDef,
    ListOutgoingTypedLinksRequestListOutgoingTypedLinksPaginateTypeDef,
    ListOutgoingTypedLinksResponseTypeDef,
    ListPolicyAttachmentsRequestListPolicyAttachmentsPaginateTypeDef,
    ListPolicyAttachmentsResponseTypeDef,
    ListPublishedSchemaArnsRequestListPublishedSchemaArnsPaginateTypeDef,
    ListPublishedSchemaArnsResponseTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTypedLinkFacetAttributesRequestListTypedLinkFacetAttributesPaginateTypeDef,
    ListTypedLinkFacetAttributesResponseTypeDef,
    ListTypedLinkFacetNamesRequestListTypedLinkFacetNamesPaginateTypeDef,
    ListTypedLinkFacetNamesResponseTypeDef,
    LookupPolicyRequestLookupPolicyPaginateTypeDef,
    LookupPolicyResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAppliedSchemaArnsPaginator",
    "ListAttachedIndicesPaginator",
    "ListDevelopmentSchemaArnsPaginator",
    "ListDirectoriesPaginator",
    "ListFacetAttributesPaginator",
    "ListFacetNamesPaginator",
    "ListIncomingTypedLinksPaginator",
    "ListIndexPaginator",
    "ListManagedSchemaArnsPaginator",
    "ListObjectAttributesPaginator",
    "ListObjectParentPathsPaginator",
    "ListObjectPoliciesPaginator",
    "ListOutgoingTypedLinksPaginator",
    "ListPolicyAttachmentsPaginator",
    "ListPublishedSchemaArnsPaginator",
    "ListTagsForResourcePaginator",
    "ListTypedLinkFacetAttributesPaginator",
    "ListTypedLinkFacetNamesPaginator",
    "LookupPolicyPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAppliedSchemaArnsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListAppliedSchemaArns.html#CloudDirectory.Paginator.ListAppliedSchemaArns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listappliedschemaarnspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAppliedSchemaArnsRequestListAppliedSchemaArnsPaginateTypeDef]
    ) -> AsyncIterator[ListAppliedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListAppliedSchemaArns.html#CloudDirectory.Paginator.ListAppliedSchemaArns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listappliedschemaarnspaginator)
        """

class ListAttachedIndicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListAttachedIndices.html#CloudDirectory.Paginator.ListAttachedIndices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listattachedindicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAttachedIndicesRequestListAttachedIndicesPaginateTypeDef]
    ) -> AsyncIterator[ListAttachedIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListAttachedIndices.html#CloudDirectory.Paginator.ListAttachedIndices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listattachedindicespaginator)
        """

class ListDevelopmentSchemaArnsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListDevelopmentSchemaArns.html#CloudDirectory.Paginator.ListDevelopmentSchemaArns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listdevelopmentschemaarnspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListDevelopmentSchemaArnsRequestListDevelopmentSchemaArnsPaginateTypeDef],
    ) -> AsyncIterator[ListDevelopmentSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListDevelopmentSchemaArns.html#CloudDirectory.Paginator.ListDevelopmentSchemaArns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listdevelopmentschemaarnspaginator)
        """

class ListDirectoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListDirectories.html#CloudDirectory.Paginator.ListDirectories)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listdirectoriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDirectoriesRequestListDirectoriesPaginateTypeDef]
    ) -> AsyncIterator[ListDirectoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListDirectories.html#CloudDirectory.Paginator.ListDirectories.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listdirectoriespaginator)
        """

class ListFacetAttributesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListFacetAttributes.html#CloudDirectory.Paginator.ListFacetAttributes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listfacetattributespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFacetAttributesRequestListFacetAttributesPaginateTypeDef]
    ) -> AsyncIterator[ListFacetAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListFacetAttributes.html#CloudDirectory.Paginator.ListFacetAttributes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listfacetattributespaginator)
        """

class ListFacetNamesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListFacetNames.html#CloudDirectory.Paginator.ListFacetNames)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listfacetnamespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFacetNamesRequestListFacetNamesPaginateTypeDef]
    ) -> AsyncIterator[ListFacetNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListFacetNames.html#CloudDirectory.Paginator.ListFacetNames.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listfacetnamespaginator)
        """

class ListIncomingTypedLinksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListIncomingTypedLinks.html#CloudDirectory.Paginator.ListIncomingTypedLinks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listincomingtypedlinkspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIncomingTypedLinksRequestListIncomingTypedLinksPaginateTypeDef]
    ) -> AsyncIterator[ListIncomingTypedLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListIncomingTypedLinks.html#CloudDirectory.Paginator.ListIncomingTypedLinks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listincomingtypedlinkspaginator)
        """

class ListIndexPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListIndex.html#CloudDirectory.Paginator.ListIndex)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listindexpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIndexRequestListIndexPaginateTypeDef]
    ) -> AsyncIterator[ListIndexResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListIndex.html#CloudDirectory.Paginator.ListIndex.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listindexpaginator)
        """

class ListManagedSchemaArnsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListManagedSchemaArns.html#CloudDirectory.Paginator.ListManagedSchemaArns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listmanagedschemaarnspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListManagedSchemaArnsRequestListManagedSchemaArnsPaginateTypeDef]
    ) -> AsyncIterator[ListManagedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListManagedSchemaArns.html#CloudDirectory.Paginator.ListManagedSchemaArns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listmanagedschemaarnspaginator)
        """

class ListObjectAttributesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectAttributes.html#CloudDirectory.Paginator.ListObjectAttributes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listobjectattributespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListObjectAttributesRequestListObjectAttributesPaginateTypeDef]
    ) -> AsyncIterator[ListObjectAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectAttributes.html#CloudDirectory.Paginator.ListObjectAttributes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listobjectattributespaginator)
        """

class ListObjectParentPathsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectParentPaths.html#CloudDirectory.Paginator.ListObjectParentPaths)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listobjectparentpathspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListObjectParentPathsRequestListObjectParentPathsPaginateTypeDef]
    ) -> AsyncIterator[ListObjectParentPathsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectParentPaths.html#CloudDirectory.Paginator.ListObjectParentPaths.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listobjectparentpathspaginator)
        """

class ListObjectPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectPolicies.html#CloudDirectory.Paginator.ListObjectPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listobjectpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListObjectPoliciesRequestListObjectPoliciesPaginateTypeDef]
    ) -> AsyncIterator[ListObjectPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectPolicies.html#CloudDirectory.Paginator.ListObjectPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listobjectpoliciespaginator)
        """

class ListOutgoingTypedLinksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListOutgoingTypedLinks.html#CloudDirectory.Paginator.ListOutgoingTypedLinks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listoutgoingtypedlinkspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOutgoingTypedLinksRequestListOutgoingTypedLinksPaginateTypeDef]
    ) -> AsyncIterator[ListOutgoingTypedLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListOutgoingTypedLinks.html#CloudDirectory.Paginator.ListOutgoingTypedLinks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listoutgoingtypedlinkspaginator)
        """

class ListPolicyAttachmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListPolicyAttachments.html#CloudDirectory.Paginator.ListPolicyAttachments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listpolicyattachmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPolicyAttachmentsRequestListPolicyAttachmentsPaginateTypeDef]
    ) -> AsyncIterator[ListPolicyAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListPolicyAttachments.html#CloudDirectory.Paginator.ListPolicyAttachments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listpolicyattachmentspaginator)
        """

class ListPublishedSchemaArnsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListPublishedSchemaArns.html#CloudDirectory.Paginator.ListPublishedSchemaArns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listpublishedschemaarnspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPublishedSchemaArnsRequestListPublishedSchemaArnsPaginateTypeDef]
    ) -> AsyncIterator[ListPublishedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListPublishedSchemaArns.html#CloudDirectory.Paginator.ListPublishedSchemaArns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listpublishedschemaarnspaginator)
        """

class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTagsForResource.html#CloudDirectory.Paginator.ListTagsForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> AsyncIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTagsForResource.html#CloudDirectory.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listtagsforresourcepaginator)
        """

class ListTypedLinkFacetAttributesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTypedLinkFacetAttributes.html#CloudDirectory.Paginator.ListTypedLinkFacetAttributes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listtypedlinkfacetattributespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListTypedLinkFacetAttributesRequestListTypedLinkFacetAttributesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListTypedLinkFacetAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTypedLinkFacetAttributes.html#CloudDirectory.Paginator.ListTypedLinkFacetAttributes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listtypedlinkfacetattributespaginator)
        """

class ListTypedLinkFacetNamesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTypedLinkFacetNames.html#CloudDirectory.Paginator.ListTypedLinkFacetNames)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listtypedlinkfacetnamespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTypedLinkFacetNamesRequestListTypedLinkFacetNamesPaginateTypeDef]
    ) -> AsyncIterator[ListTypedLinkFacetNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTypedLinkFacetNames.html#CloudDirectory.Paginator.ListTypedLinkFacetNames.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#listtypedlinkfacetnamespaginator)
        """

class LookupPolicyPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/LookupPolicy.html#CloudDirectory.Paginator.LookupPolicy)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#lookuppolicypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[LookupPolicyRequestLookupPolicyPaginateTypeDef]
    ) -> AsyncIterator[LookupPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/LookupPolicy.html#CloudDirectory.Paginator.LookupPolicy.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_clouddirectory/paginators/#lookuppolicypaginator)
        """
