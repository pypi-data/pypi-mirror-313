import concurrent.futures
import contextlib
import datetime
import mimetypes
import os
import tempfile
from dataclasses import dataclass

import boto3
from botocore.client import BaseClient

from iker.common.utils.shutils import glob_match, listfile, path_depth
from iker.common.utils.strutils import is_empty, trim_to_none

__all__ = [
    "S3ObjectMeta",
    "s3_make_client",
    "s3_list_objects",
    "s3_listfile",
    "s3_cp_download",
    "s3_cp_upload",
    "s3_sync_download",
    "s3_sync_upload",
    "s3_pull_text",
    "s3_push_text",
]


@dataclass
class S3ObjectMeta(object):
    key: str
    last_modified: datetime.datetime
    size: int


def s3_make_client(
    access_key_id: str = None,
    secret_access_key: str = None,
    region_name: str = None,
    endpoint_url: str = None,
) -> contextlib.AbstractContextManager[BaseClient]:
    """
    Makes an AWS S3 client

    :param access_key_id: AWS access key id
    :param secret_access_key: AWS secret access key
    :param region_name: AWS service region name
    :param endpoint_url: AWS service endpoint url
    :return: context manager which wraps the AWS S3 client instance
    """
    client = boto3.client("s3",
                          region_name=trim_to_none(region_name),
                          endpoint_url=trim_to_none(endpoint_url),
                          aws_access_key_id=trim_to_none(access_key_id),
                          aws_secret_access_key=trim_to_none(secret_access_key))
    return contextlib.closing(client)


def s3_list_objects(client: BaseClient, bucket: str, prefix: str, limit: int = None) -> list[S3ObjectMeta]:
    """
    Lists all objects from the given bucket and prefix

    :param client: AWS S3 client instance
    :param bucket: bucket name
    :param prefix: object keys prefix
    :param limit: maximum count of objects returns
    :return: list of object meta items
    """
    entries = []

    next_marker = None
    while True:
        if is_empty(next_marker):
            response = client.list_objects(MaxKeys=1000, Bucket=bucket, Prefix=prefix)
        else:
            response = client.list_objects(MaxKeys=1000, Bucket=bucket, Prefix=prefix, Marker=next_marker)

        entries.extend(response.get("Contents", []))

        if limit is not None and len(entries) >= limit:
            entries = entries[:limit]

        if not response.get("IsTruncated"):
            break

        next_marker = response.get("NextMarker")
        if is_empty(next_marker):
            next_marker = entries[-1]["Key"]

    return [S3ObjectMeta(key=e["Key"], last_modified=e["LastModified"], size=e["Size"]) for e in entries]


def s3_listfile(
    client: BaseClient,
    bucket: str,
    prefix: str,
    *,
    include_patterns: list[str] = None,
    exclude_patterns: list[str] = None,
    depth: int = 0,
) -> list[S3ObjectMeta]:
    """
    Lists all objects from the given bucket and prefix

    :param client: AWS S3 client instance
    :param bucket: bucket name
    :param prefix: object keys prefix
    :param include_patterns: inclusive glob patterns applied to the filenames
    :param exclude_patterns: exclusive glob patterns applied to the filenames
    :param depth: maximum depth of the subdirectories included in the scan
    :return: list of object meta items
    """

    # We add trailing slash "/" to the prefix if it is absent
    if not prefix.endswith("/"):
        prefix = prefix + "/"

    objects = s3_list_objects(client, bucket, prefix)

    def filter_object_meta(object_meta: S3ObjectMeta) -> bool:
        if 0 < depth <= path_depth(prefix, os.path.dirname(object_meta.key)):
            return False
        if len(glob_match([os.path.basename(object_meta.key)], include_patterns, exclude_patterns)) == 0:
            return False
        return True

    return list(filter(filter_object_meta, objects))


def s3_cp_download(client: BaseClient, bucket: str, key: str, file_path: str):
    """
    Downloads object from the given bucket and key to the given local file path

    :param client: AWS S3 client instance
    :param bucket: bucket name
    :param key: object key
    :param file_path: local file path
    """
    client.download_file(bucket, key, file_path)


def s3_cp_upload(client: BaseClient, file_path: str, bucket: str, key: str):
    """
    Uploads object of the given local file path to the given bucket and key

    :param client: AWS S3 client instance
    :param file_path: local file path
    :param bucket: bucket name
    :param key: object key
    """
    t, _ = mimetypes.MimeTypes().guess_type(file_path)
    client.upload_file(file_path, bucket, key, ExtraArgs={"ContentType": "binary/octet-stream" if t is None else t})


def s3_sync_download(
    client: BaseClient,
    bucket: str,
    prefix: str,
    dir_path: str,
    *,
    max_workers: int = None,
    include_patterns: list[str] = None,
    exclude_patterns: list[str] = None,
    depth: int = 0,
):
    """
    Recursively downloads all objects from the given bucket and prefix to the given local directory path

    :param client: AWS S3 client instance
    :param bucket: bucket name
    :param prefix: object keys prefix
    :param dir_path: local directory path
    :param max_workers: number of maximum workers in thread pool
    :param include_patterns: inclusive glob patterns applied to the filenames
    :param exclude_patterns: exclusive glob patterns applied to the filenames
    :param depth: maximum depth of the subdirectories included in the scan
    """

    # We add trailing slash "/" to the prefix if it is absent
    if not prefix.endswith("/"):
        prefix = prefix + "/"

    objects = s3_listfile(client,
                          bucket,
                          prefix,
                          include_patterns=include_patterns,
                          exclude_patterns=exclude_patterns,
                          depth=depth)

    def download_file(key: str):
        file_path = os.path.join(dir_path, key[len(prefix):])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        s3_cp_download(client, bucket, key, file_path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        concurrent.futures.wait([executor.submit(download_file, obj.key) for obj in objects],
                                return_when=concurrent.futures.FIRST_EXCEPTION)


def s3_sync_upload(
    client: BaseClient,
    dir_path: str,
    bucket: str,
    prefix: str,
    *,
    max_workers: int = None,
    include_patterns: list[str] = None,
    exclude_patterns: list[str] = None,
    depth: int = 0,
):
    """
    Recursively uploads all objects from the given local directory path to the given bucket and prefix

    :param client: AWS S3 client instance
    :param dir_path: local directory
    :param bucket: bucket name
    :param prefix: object keys prefix
    :param max_workers: number of maximum workers in thread pool
    :param include_patterns: inclusive glob patterns applied to the filenames
    :param exclude_patterns: exclusive glob patterns applied to the filenames
    :param depth: maximum depth of the subdirectories included in the scan
    """

    # We add trailing slash "/" to the prefix if it is absent
    if not prefix.endswith("/"):
        prefix = prefix + "/"

    file_paths = listfile(dir_path,
                          include_patterns=include_patterns,
                          exclude_patterns=exclude_patterns,
                          depth=depth)

    def upload_file(file_path: str):
        s3_cp_upload(client, file_path, bucket, prefix + os.path.relpath(file_path, dir_path))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        concurrent.futures.wait([executor.submit(upload_file, file_path) for file_path in file_paths],
                                return_when=concurrent.futures.FIRST_EXCEPTION)


def s3_pull_text(client: BaseClient, bucket: str, key: str, encoding: str = None) -> str:
    """
    Pulls text stored as object from the given bucket and key

    :param client: AWS S3 client instance
    :param bucket: bucket name
    :param key: key of the object storing the text
    :param encoding: string encoding
    :return: text content
    """
    with tempfile.TemporaryFile() as fp:
        client.download_fileobj(bucket, key, fp)
        fp.seek(0)
        return fp.read().decode(encoding or "utf-8")


def s3_push_text(client: BaseClient, text: str, bucket: str, key: str, encoding: str = None):
    """
    Pushes the given text to the object stored by the given bucket and key

    :param client: AWS S3 client instance
    :param text: text content
    :param bucket: bucket name
    :param key: key of the object storing the text
    :param encoding: string encoding
    """
    with tempfile.TemporaryFile() as fp:
        fp.write(text.encode(encoding or "utf-8"))
        fp.seek(0)
        client.upload_fileobj(fp, bucket, key)
