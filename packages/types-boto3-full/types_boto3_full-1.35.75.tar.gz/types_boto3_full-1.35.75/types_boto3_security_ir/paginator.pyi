"""
Type annotations for security-ir service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_security_ir.client import SecurityIncidentResponseClient
    from types_boto3_security_ir.paginator import (
        ListCaseEditsPaginator,
        ListCasesPaginator,
        ListCommentsPaginator,
        ListMembershipsPaginator,
    )

    session = Session()
    client: SecurityIncidentResponseClient = session.client("security-ir")

    list_case_edits_paginator: ListCaseEditsPaginator = client.get_paginator("list_case_edits")
    list_cases_paginator: ListCasesPaginator = client.get_paginator("list_cases")
    list_comments_paginator: ListCommentsPaginator = client.get_paginator("list_comments")
    list_memberships_paginator: ListMembershipsPaginator = client.get_paginator("list_memberships")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCaseEditsRequestListCaseEditsPaginateTypeDef,
    ListCaseEditsResponseTypeDef,
    ListCasesRequestListCasesPaginateTypeDef,
    ListCasesResponseTypeDef,
    ListCommentsRequestListCommentsPaginateTypeDef,
    ListCommentsResponseTypeDef,
    ListMembershipsRequestListMembershipsPaginateTypeDef,
    ListMembershipsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCaseEditsPaginator",
    "ListCasesPaginator",
    "ListCommentsPaginator",
    "ListMembershipsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCaseEditsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListCaseEdits.html#SecurityIncidentResponse.Paginator.ListCaseEdits)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/paginators/#listcaseeditspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCaseEditsRequestListCaseEditsPaginateTypeDef]
    ) -> _PageIterator[ListCaseEditsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListCaseEdits.html#SecurityIncidentResponse.Paginator.ListCaseEdits.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/paginators/#listcaseeditspaginator)
        """

class ListCasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListCases.html#SecurityIncidentResponse.Paginator.ListCases)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/paginators/#listcasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCasesRequestListCasesPaginateTypeDef]
    ) -> _PageIterator[ListCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListCases.html#SecurityIncidentResponse.Paginator.ListCases.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/paginators/#listcasespaginator)
        """

class ListCommentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListComments.html#SecurityIncidentResponse.Paginator.ListComments)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/paginators/#listcommentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCommentsRequestListCommentsPaginateTypeDef]
    ) -> _PageIterator[ListCommentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListComments.html#SecurityIncidentResponse.Paginator.ListComments.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/paginators/#listcommentspaginator)
        """

class ListMembershipsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListMemberships.html#SecurityIncidentResponse.Paginator.ListMemberships)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/paginators/#listmembershipspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMembershipsRequestListMembershipsPaginateTypeDef]
    ) -> _PageIterator[ListMembershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListMemberships.html#SecurityIncidentResponse.Paginator.ListMemberships.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/paginators/#listmembershipspaginator)
        """
