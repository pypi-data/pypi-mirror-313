"""
Type annotations for bedrock-data-automation service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_bedrock_data_automation.client import DataAutomationforBedrockClient
    from types_boto3_bedrock_data_automation.paginator import (
        ListBlueprintsPaginator,
        ListDataAutomationProjectsPaginator,
    )

    session = Session()
    client: DataAutomationforBedrockClient = session.client("bedrock-data-automation")

    list_blueprints_paginator: ListBlueprintsPaginator = client.get_paginator("list_blueprints")
    list_data_automation_projects_paginator: ListDataAutomationProjectsPaginator = client.get_paginator("list_data_automation_projects")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListBlueprintsRequestListBlueprintsPaginateTypeDef,
    ListBlueprintsResponseTypeDef,
    ListDataAutomationProjectsRequestListDataAutomationProjectsPaginateTypeDef,
    ListDataAutomationProjectsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListBlueprintsPaginator", "ListDataAutomationProjectsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBlueprintsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListBlueprints.html#DataAutomationforBedrock.Paginator.ListBlueprints)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/paginators/#listblueprintspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBlueprintsRequestListBlueprintsPaginateTypeDef]
    ) -> _PageIterator[ListBlueprintsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListBlueprints.html#DataAutomationforBedrock.Paginator.ListBlueprints.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/paginators/#listblueprintspaginator)
        """


class ListDataAutomationProjectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationProjects.html#DataAutomationforBedrock.Paginator.ListDataAutomationProjects)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/paginators/#listdataautomationprojectspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDataAutomationProjectsRequestListDataAutomationProjectsPaginateTypeDef
        ],
    ) -> _PageIterator[ListDataAutomationProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationProjects.html#DataAutomationforBedrock.Paginator.ListDataAutomationProjects.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/paginators/#listdataautomationprojectspaginator)
        """
