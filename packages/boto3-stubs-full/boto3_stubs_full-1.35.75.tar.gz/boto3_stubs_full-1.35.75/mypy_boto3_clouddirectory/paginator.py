"""
Type annotations for clouddirectory service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_clouddirectory.client import CloudDirectoryClient
    from mypy_boto3_clouddirectory.paginator import (
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

    session = Session()
    client: CloudDirectoryClient = session.client("clouddirectory")

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
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

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


class ListAppliedSchemaArnsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListAppliedSchemaArns.html#CloudDirectory.Paginator.ListAppliedSchemaArns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listappliedschemaarnspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAppliedSchemaArnsRequestListAppliedSchemaArnsPaginateTypeDef]
    ) -> _PageIterator[ListAppliedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListAppliedSchemaArns.html#CloudDirectory.Paginator.ListAppliedSchemaArns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listappliedschemaarnspaginator)
        """


class ListAttachedIndicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListAttachedIndices.html#CloudDirectory.Paginator.ListAttachedIndices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listattachedindicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAttachedIndicesRequestListAttachedIndicesPaginateTypeDef]
    ) -> _PageIterator[ListAttachedIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListAttachedIndices.html#CloudDirectory.Paginator.ListAttachedIndices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listattachedindicespaginator)
        """


class ListDevelopmentSchemaArnsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListDevelopmentSchemaArns.html#CloudDirectory.Paginator.ListDevelopmentSchemaArns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listdevelopmentschemaarnspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListDevelopmentSchemaArnsRequestListDevelopmentSchemaArnsPaginateTypeDef],
    ) -> _PageIterator[ListDevelopmentSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListDevelopmentSchemaArns.html#CloudDirectory.Paginator.ListDevelopmentSchemaArns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listdevelopmentschemaarnspaginator)
        """


class ListDirectoriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListDirectories.html#CloudDirectory.Paginator.ListDirectories)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listdirectoriespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDirectoriesRequestListDirectoriesPaginateTypeDef]
    ) -> _PageIterator[ListDirectoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListDirectories.html#CloudDirectory.Paginator.ListDirectories.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listdirectoriespaginator)
        """


class ListFacetAttributesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListFacetAttributes.html#CloudDirectory.Paginator.ListFacetAttributes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listfacetattributespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFacetAttributesRequestListFacetAttributesPaginateTypeDef]
    ) -> _PageIterator[ListFacetAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListFacetAttributes.html#CloudDirectory.Paginator.ListFacetAttributes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listfacetattributespaginator)
        """


class ListFacetNamesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListFacetNames.html#CloudDirectory.Paginator.ListFacetNames)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listfacetnamespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFacetNamesRequestListFacetNamesPaginateTypeDef]
    ) -> _PageIterator[ListFacetNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListFacetNames.html#CloudDirectory.Paginator.ListFacetNames.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listfacetnamespaginator)
        """


class ListIncomingTypedLinksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListIncomingTypedLinks.html#CloudDirectory.Paginator.ListIncomingTypedLinks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listincomingtypedlinkspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIncomingTypedLinksRequestListIncomingTypedLinksPaginateTypeDef]
    ) -> _PageIterator[ListIncomingTypedLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListIncomingTypedLinks.html#CloudDirectory.Paginator.ListIncomingTypedLinks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listincomingtypedlinkspaginator)
        """


class ListIndexPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListIndex.html#CloudDirectory.Paginator.ListIndex)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listindexpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIndexRequestListIndexPaginateTypeDef]
    ) -> _PageIterator[ListIndexResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListIndex.html#CloudDirectory.Paginator.ListIndex.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listindexpaginator)
        """


class ListManagedSchemaArnsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListManagedSchemaArns.html#CloudDirectory.Paginator.ListManagedSchemaArns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listmanagedschemaarnspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListManagedSchemaArnsRequestListManagedSchemaArnsPaginateTypeDef]
    ) -> _PageIterator[ListManagedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListManagedSchemaArns.html#CloudDirectory.Paginator.ListManagedSchemaArns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listmanagedschemaarnspaginator)
        """


class ListObjectAttributesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectAttributes.html#CloudDirectory.Paginator.ListObjectAttributes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listobjectattributespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListObjectAttributesRequestListObjectAttributesPaginateTypeDef]
    ) -> _PageIterator[ListObjectAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectAttributes.html#CloudDirectory.Paginator.ListObjectAttributes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listobjectattributespaginator)
        """


class ListObjectParentPathsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectParentPaths.html#CloudDirectory.Paginator.ListObjectParentPaths)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listobjectparentpathspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListObjectParentPathsRequestListObjectParentPathsPaginateTypeDef]
    ) -> _PageIterator[ListObjectParentPathsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectParentPaths.html#CloudDirectory.Paginator.ListObjectParentPaths.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listobjectparentpathspaginator)
        """


class ListObjectPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectPolicies.html#CloudDirectory.Paginator.ListObjectPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listobjectpoliciespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListObjectPoliciesRequestListObjectPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListObjectPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectPolicies.html#CloudDirectory.Paginator.ListObjectPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listobjectpoliciespaginator)
        """


class ListOutgoingTypedLinksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListOutgoingTypedLinks.html#CloudDirectory.Paginator.ListOutgoingTypedLinks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listoutgoingtypedlinkspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOutgoingTypedLinksRequestListOutgoingTypedLinksPaginateTypeDef]
    ) -> _PageIterator[ListOutgoingTypedLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListOutgoingTypedLinks.html#CloudDirectory.Paginator.ListOutgoingTypedLinks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listoutgoingtypedlinkspaginator)
        """


class ListPolicyAttachmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListPolicyAttachments.html#CloudDirectory.Paginator.ListPolicyAttachments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listpolicyattachmentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPolicyAttachmentsRequestListPolicyAttachmentsPaginateTypeDef]
    ) -> _PageIterator[ListPolicyAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListPolicyAttachments.html#CloudDirectory.Paginator.ListPolicyAttachments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listpolicyattachmentspaginator)
        """


class ListPublishedSchemaArnsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListPublishedSchemaArns.html#CloudDirectory.Paginator.ListPublishedSchemaArns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listpublishedschemaarnspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPublishedSchemaArnsRequestListPublishedSchemaArnsPaginateTypeDef]
    ) -> _PageIterator[ListPublishedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListPublishedSchemaArns.html#CloudDirectory.Paginator.ListPublishedSchemaArns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listpublishedschemaarnspaginator)
        """


class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTagsForResource.html#CloudDirectory.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTagsForResource.html#CloudDirectory.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listtagsforresourcepaginator)
        """


class ListTypedLinkFacetAttributesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTypedLinkFacetAttributes.html#CloudDirectory.Paginator.ListTypedLinkFacetAttributes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listtypedlinkfacetattributespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListTypedLinkFacetAttributesRequestListTypedLinkFacetAttributesPaginateTypeDef
        ],
    ) -> _PageIterator[ListTypedLinkFacetAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTypedLinkFacetAttributes.html#CloudDirectory.Paginator.ListTypedLinkFacetAttributes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listtypedlinkfacetattributespaginator)
        """


class ListTypedLinkFacetNamesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTypedLinkFacetNames.html#CloudDirectory.Paginator.ListTypedLinkFacetNames)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listtypedlinkfacetnamespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTypedLinkFacetNamesRequestListTypedLinkFacetNamesPaginateTypeDef]
    ) -> _PageIterator[ListTypedLinkFacetNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTypedLinkFacetNames.html#CloudDirectory.Paginator.ListTypedLinkFacetNames.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#listtypedlinkfacetnamespaginator)
        """


class LookupPolicyPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/LookupPolicy.html#CloudDirectory.Paginator.LookupPolicy)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#lookuppolicypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[LookupPolicyRequestLookupPolicyPaginateTypeDef]
    ) -> _PageIterator[LookupPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/LookupPolicy.html#CloudDirectory.Paginator.LookupPolicy.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators/#lookuppolicypaginator)
        """
