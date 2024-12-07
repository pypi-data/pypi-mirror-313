"""
Type annotations for s3 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_s3.client import S3Client
    from types_aiobotocore_s3.paginator import (
        ListBucketsPaginator,
        ListDirectoryBucketsPaginator,
        ListMultipartUploadsPaginator,
        ListObjectVersionsPaginator,
        ListObjectsPaginator,
        ListObjectsV2Paginator,
        ListPartsPaginator,
    )

    session = get_session()
    with session.create_client("s3") as client:
        client: S3Client

        list_buckets_paginator: ListBucketsPaginator = client.get_paginator("list_buckets")
        list_directory_buckets_paginator: ListDirectoryBucketsPaginator = client.get_paginator("list_directory_buckets")
        list_multipart_uploads_paginator: ListMultipartUploadsPaginator = client.get_paginator("list_multipart_uploads")
        list_object_versions_paginator: ListObjectVersionsPaginator = client.get_paginator("list_object_versions")
        list_objects_paginator: ListObjectsPaginator = client.get_paginator("list_objects")
        list_objects_v2_paginator: ListObjectsV2Paginator = client.get_paginator("list_objects_v2")
        list_parts_paginator: ListPartsPaginator = client.get_paginator("list_parts")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListBucketsOutputTypeDef,
    ListBucketsRequestListBucketsPaginateTypeDef,
    ListDirectoryBucketsOutputTypeDef,
    ListDirectoryBucketsRequestListDirectoryBucketsPaginateTypeDef,
    ListMultipartUploadsOutputTypeDef,
    ListMultipartUploadsRequestListMultipartUploadsPaginateTypeDef,
    ListObjectsOutputTypeDef,
    ListObjectsRequestListObjectsPaginateTypeDef,
    ListObjectsV2OutputTypeDef,
    ListObjectsV2RequestListObjectsV2PaginateTypeDef,
    ListObjectVersionsOutputTypeDef,
    ListObjectVersionsRequestListObjectVersionsPaginateTypeDef,
    ListPartsOutputTypeDef,
    ListPartsRequestListPartsPaginateTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListBucketsPaginator",
    "ListDirectoryBucketsPaginator",
    "ListMultipartUploadsPaginator",
    "ListObjectVersionsPaginator",
    "ListObjectsPaginator",
    "ListObjectsV2Paginator",
    "ListPartsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListBucketsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListBuckets.html#S3.Paginator.ListBuckets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listbucketspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBucketsRequestListBucketsPaginateTypeDef]
    ) -> AsyncIterator[ListBucketsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListBuckets.html#S3.Paginator.ListBuckets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listbucketspaginator)
        """

class ListDirectoryBucketsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListDirectoryBuckets.html#S3.Paginator.ListDirectoryBuckets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listdirectorybucketspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDirectoryBucketsRequestListDirectoryBucketsPaginateTypeDef]
    ) -> AsyncIterator[ListDirectoryBucketsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListDirectoryBuckets.html#S3.Paginator.ListDirectoryBuckets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listdirectorybucketspaginator)
        """

class ListMultipartUploadsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListMultipartUploads.html#S3.Paginator.ListMultipartUploads)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listmultipartuploadspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMultipartUploadsRequestListMultipartUploadsPaginateTypeDef]
    ) -> AsyncIterator[ListMultipartUploadsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListMultipartUploads.html#S3.Paginator.ListMultipartUploads.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listmultipartuploadspaginator)
        """

class ListObjectVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListObjectVersions.html#S3.Paginator.ListObjectVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listobjectversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListObjectVersionsRequestListObjectVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListObjectVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListObjectVersions.html#S3.Paginator.ListObjectVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listobjectversionspaginator)
        """

class ListObjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListObjects.html#S3.Paginator.ListObjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listobjectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListObjectsRequestListObjectsPaginateTypeDef]
    ) -> AsyncIterator[ListObjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListObjects.html#S3.Paginator.ListObjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listobjectspaginator)
        """

class ListObjectsV2Paginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListObjectsV2.html#S3.Paginator.ListObjectsV2)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listobjectsv2paginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListObjectsV2RequestListObjectsV2PaginateTypeDef]
    ) -> AsyncIterator[ListObjectsV2OutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListObjectsV2.html#S3.Paginator.ListObjectsV2.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listobjectsv2paginator)
        """

class ListPartsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListParts.html#S3.Paginator.ListParts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listpartspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPartsRequestListPartsPaginateTypeDef]
    ) -> AsyncIterator[ListPartsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListParts.html#S3.Paginator.ListParts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listpartspaginator)
        """
