import tempfile
import unittest

import ddt
import moto

from iker.common.utils.randutils import randomizer
from iker.common.utils.s3utils import *
from iker.common.utils.shutils import listfile
from iker.common.utils.testutils import norm_path
from iker_tests import resources_directory


@ddt.ddt
class S3UtilsTest(unittest.TestCase):

    def test_s3_list_object__random_text_files(self):
        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.create_bucket(Bucket="dummy-bucket")

            data = []
            for i in range(0, 1000):
                text = randomizer().random_alphanumeric(randomizer().next_int(1000, 2000))
                key = "dummy_prefix/%03d" % i
                data.append((key, text))

            for key, text in data:
                s3_push_text(client, text, "dummy-bucket", key)

            result = s3_list_objects(client, "dummy-bucket", "dummy_prefix/")

            for key, text in data:
                self.assertTrue(any(o.key == key for o in result))
                self.assertEqual(s3_pull_text(client, "dummy-bucket", key), text)

    def test_s3_listfile__random_text_files(self):
        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.create_bucket(Bucket="dummy-bucket")

            data = []
            for i in range(0, 1000):
                text = randomizer().random_alphanumeric(randomizer().next_int(1000, 2000))
                key = "dummy_prefix/%03d" % i
                data.append((key, text))

            for key, text in data:
                s3_push_text(client, text, "dummy-bucket", key)

            result = s3_listfile(client, "dummy-bucket", "dummy_prefix/")

            for key, text in data:
                self.assertTrue(any(o.key == key for o in result))
                self.assertEqual(s3_pull_text(client, "dummy-bucket", key), text)

    @ddt.data(
        (
            "{res_dir}/unittest/shutils/",
            "dummy-bucket",
            "unittest/shutils/",
            [],
            [],
            0,
            [
                "unittest/shutils/dir.baz/file.foo.bar",
                "unittest/shutils/dir.baz/file.foo.baz",
                "unittest/shutils/dir.baz/file.bar.baz",
                "unittest/shutils/dir.foo/file.bar",
                "unittest/shutils/dir.foo/file.baz",
                "unittest/shutils/dir.foo/file.foo",
                "unittest/shutils/dir.foo/dir.foo.bar/file.foo.bar",
                "unittest/shutils/dir.foo/dir.foo.bar/file.foo.baz",
                "unittest/shutils/dir.foo/dir.foo.bar/file.bar.baz",
                "unittest/shutils/dir.foo/dir.foo.bar/dir.foo.bar.baz/file.foo.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/shutils",
            "dummy-bucket",
            "unittest/shutils/",
            [],
            [],
            0,
            [
                "unittest/shutils/dir.baz/file.foo.bar",
                "unittest/shutils/dir.baz/file.foo.baz",
                "unittest/shutils/dir.baz/file.bar.baz",
                "unittest/shutils/dir.foo/file.bar",
                "unittest/shutils/dir.foo/file.baz",
                "unittest/shutils/dir.foo/file.foo",
                "unittest/shutils/dir.foo/dir.foo.bar/file.foo.bar",
                "unittest/shutils/dir.foo/dir.foo.bar/file.foo.baz",
                "unittest/shutils/dir.foo/dir.foo.bar/file.bar.baz",
                "unittest/shutils/dir.foo/dir.foo.bar/dir.foo.bar.baz/file.foo.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/shutils/dir.foo",
            "dummy-bucket",
            "unittest/shutils/dir.foo",
            [],
            [],
            0,
            [
                "unittest/shutils/dir.foo/file.bar",
                "unittest/shutils/dir.foo/file.baz",
                "unittest/shutils/dir.foo/file.foo",
                "unittest/shutils/dir.foo/dir.foo.bar/file.foo.bar",
                "unittest/shutils/dir.foo/dir.foo.bar/file.foo.baz",
                "unittest/shutils/dir.foo/dir.foo.bar/file.bar.baz",
                "unittest/shutils/dir.foo/dir.foo.bar/dir.foo.bar.baz/file.foo.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/shutils/dir.baz",
            "dummy-bucket",
            "unittest/shutils/dir.baz",
            [],
            [],
            0,
            [
                "unittest/shutils/dir.baz/file.foo.bar",
                "unittest/shutils/dir.baz/file.foo.baz",
                "unittest/shutils/dir.baz/file.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/shutils",
            "dummy-bucket",
            "unittest/shutils/",
            ["*.foo", "*.bar"],
            ["*.foo.bar"],
            0,
            [
                "unittest/shutils/dir.foo/file.bar",
                "unittest/shutils/dir.foo/file.foo",
            ],
        ),
        (
            "{res_dir}/unittest/shutils",
            "dummy-bucket",
            "unittest/shutils/",
            ["*.foo", "*.bar"],
            [],
            0,
            [
                "unittest/shutils/dir.baz/file.foo.bar",
                "unittest/shutils/dir.foo/file.bar",
                "unittest/shutils/dir.foo/file.foo",
                "unittest/shutils/dir.foo/dir.foo.bar/file.foo.bar",
            ],
        ),
        (
            "{res_dir}/unittest/shutils",
            "dummy-bucket",
            "unittest/shutils/",
            [],
            ["*.baz"],
            0,
            [
                "unittest/shutils/dir.baz/file.foo.bar",
                "unittest/shutils/dir.foo/file.bar",
                "unittest/shutils/dir.foo/file.foo",
                "unittest/shutils/dir.foo/dir.foo.bar/file.foo.bar",
            ],
        ),
        (
            "{res_dir}/unittest/shutils",
            "dummy-bucket",
            "unittest/shutils",
            [],
            [],
            2,
            [
                "unittest/shutils/dir.baz/file.foo.bar",
                "unittest/shutils/dir.baz/file.foo.baz",
                "unittest/shutils/dir.baz/file.bar.baz",
                "unittest/shutils/dir.foo/file.bar",
                "unittest/shutils/dir.foo/file.baz",
                "unittest/shutils/dir.foo/file.foo",
            ],
        ),
    )
    @ddt.unpack
    def test_s3_listfile(self, src, bucket, prefix, include_patterns, exclude_patterns, depth, expect):
        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.create_bucket(Bucket=bucket)

            s3_sync_upload(client,
                           src.format(res_dir=resources_directory),
                           bucket,
                           prefix)

            object_metas = s3_listfile(client,
                                       bucket,
                                       prefix,
                                       include_patterns=include_patterns,
                                       exclude_patterns=exclude_patterns,
                                       depth=depth)

            self.assertSetEqual(set(map(lambda x: norm_path(x.key), object_metas)),
                                set(map(lambda x: norm_path(x), expect)))

    @ddt.data(
        (
            "{res_dir}/unittest/shutils/",
            "{tmp_dir}/unittest/shutils/",
            "dummy-bucket",
            "unittest/shutils/",
            [],
            [],
            0,
            [
                "{tmp_dir}/unittest/shutils/dir.baz/file.foo.bar",
                "{tmp_dir}/unittest/shutils/dir.baz/file.foo.baz",
                "{tmp_dir}/unittest/shutils/dir.baz/file.bar.baz",
                "{tmp_dir}/unittest/shutils/dir.foo/file.bar",
                "{tmp_dir}/unittest/shutils/dir.foo/file.baz",
                "{tmp_dir}/unittest/shutils/dir.foo/file.foo",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/file.foo.bar",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/file.foo.baz",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/file.bar.baz",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/dir.foo.bar.baz/file.foo.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/shutils",
            "{tmp_dir}/unittest/shutils",
            "dummy-bucket",
            "unittest/shutils/",
            [],
            [],
            0,
            [
                "{tmp_dir}/unittest/shutils/dir.baz/file.foo.bar",
                "{tmp_dir}/unittest/shutils/dir.baz/file.foo.baz",
                "{tmp_dir}/unittest/shutils/dir.baz/file.bar.baz",
                "{tmp_dir}/unittest/shutils/dir.foo/file.bar",
                "{tmp_dir}/unittest/shutils/dir.foo/file.baz",
                "{tmp_dir}/unittest/shutils/dir.foo/file.foo",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/file.foo.bar",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/file.foo.baz",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/file.bar.baz",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/dir.foo.bar.baz/file.foo.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/shutils/dir.foo",
            "{tmp_dir}/unittest/shutils/dir.foo",
            "dummy-bucket",
            "unittest/shutils/dir.foo",
            [],
            [],
            0,
            [
                "{tmp_dir}/unittest/shutils/dir.foo/file.bar",
                "{tmp_dir}/unittest/shutils/dir.foo/file.baz",
                "{tmp_dir}/unittest/shutils/dir.foo/file.foo",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/file.foo.bar",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/file.foo.baz",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/file.bar.baz",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/dir.foo.bar.baz/file.foo.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/shutils/dir.baz",
            "{tmp_dir}/unittest/shutils/dir.baz",
            "dummy-bucket",
            "unittest/shutils/dir.baz",
            [],
            [],
            0,
            [
                "{tmp_dir}/unittest/shutils/dir.baz/file.foo.bar",
                "{tmp_dir}/unittest/shutils/dir.baz/file.foo.baz",
                "{tmp_dir}/unittest/shutils/dir.baz/file.bar.baz",
            ],
        ),
        (
            "{res_dir}/unittest/shutils",
            "{tmp_dir}/unittest/shutils",
            "dummy-bucket",
            "unittest/shutils/",
            ["*.foo", "*.bar"],
            ["*.foo.bar"],
            0,
            [
                "{tmp_dir}/unittest/shutils/dir.foo/file.bar",
                "{tmp_dir}/unittest/shutils/dir.foo/file.foo",
            ],
        ),
        (
            "{res_dir}/unittest/shutils",
            "{tmp_dir}/unittest/shutils",
            "dummy-bucket",
            "unittest/shutils/",
            ["*.foo", "*.bar"],
            [],
            0,
            [
                "{tmp_dir}/unittest/shutils/dir.baz/file.foo.bar",
                "{tmp_dir}/unittest/shutils/dir.foo/file.bar",
                "{tmp_dir}/unittest/shutils/dir.foo/file.foo",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/file.foo.bar",
            ],
        ),
        (
            "{res_dir}/unittest/shutils",
            "{tmp_dir}/unittest/shutils",
            "dummy-bucket",
            "unittest/shutils/",
            [],
            ["*.baz"],
            0,
            [
                "{tmp_dir}/unittest/shutils/dir.baz/file.foo.bar",
                "{tmp_dir}/unittest/shutils/dir.foo/file.bar",
                "{tmp_dir}/unittest/shutils/dir.foo/file.foo",
                "{tmp_dir}/unittest/shutils/dir.foo/dir.foo.bar/file.foo.bar",
            ],
        ),
        (
            "{res_dir}/unittest/shutils",
            "{tmp_dir}/unittest/shutils",
            "dummy-bucket",
            "unittest/shutils",
            [],
            [],
            2,
            [
                "{tmp_dir}/unittest/shutils/dir.baz/file.foo.bar",
                "{tmp_dir}/unittest/shutils/dir.baz/file.foo.baz",
                "{tmp_dir}/unittest/shutils/dir.baz/file.bar.baz",
                "{tmp_dir}/unittest/shutils/dir.foo/file.bar",
                "{tmp_dir}/unittest/shutils/dir.foo/file.baz",
                "{tmp_dir}/unittest/shutils/dir.foo/file.foo",
            ],
        ),
    )
    @ddt.unpack
    def test_s3_sync(self, src, dst, bucket, prefix, include_patterns, exclude_patterns, depth, expect):
        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.create_bucket(Bucket=bucket)

            s3_sync_upload(client,
                           src.format(res_dir=resources_directory),
                           bucket,
                           prefix,
                           include_patterns=include_patterns,
                           exclude_patterns=exclude_patterns,
                           depth=depth)

            with tempfile.TemporaryDirectory() as temp_directory:
                s3_sync_download(client,
                                 bucket,
                                 prefix,
                                 dst.format(tmp_dir=temp_directory))

                self.assertSetEqual(set(map(lambda x: norm_path(x), listfile(dst.format(tmp_dir=temp_directory)))),
                                    set(map(lambda x: norm_path(x.format(tmp_dir=temp_directory)), expect)))

        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.create_bucket(Bucket=bucket)

            s3_sync_upload(client,
                           src.format(res_dir=resources_directory),
                           bucket,
                           prefix)

            with tempfile.TemporaryDirectory() as temp_directory:
                s3_sync_download(client,
                                 bucket,
                                 prefix,
                                 dst.format(tmp_dir=temp_directory),
                                 include_patterns=include_patterns,
                                 exclude_patterns=exclude_patterns,
                                 depth=depth)

                self.assertSetEqual(set(map(lambda x: norm_path(x), listfile(dst.format(tmp_dir=temp_directory)))),
                                    set(map(lambda x: norm_path(x.format(tmp_dir=temp_directory)), expect)))

        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.create_bucket(Bucket=bucket)

            s3_sync_upload(client,
                           src.format(res_dir=resources_directory),
                           bucket,
                           prefix,
                           include_patterns=include_patterns,
                           depth=depth)

            with tempfile.TemporaryDirectory() as temp_directory:
                s3_sync_download(client,
                                 bucket,
                                 prefix,
                                 dst.format(tmp_dir=temp_directory),
                                 exclude_patterns=exclude_patterns,
                                 depth=depth)

                self.assertSetEqual(set(map(lambda x: norm_path(x), listfile(dst.format(tmp_dir=temp_directory)))),
                                    set(map(lambda x: norm_path(x.format(tmp_dir=temp_directory)), expect)))

    @ddt.data(
        ("dummy-bucket", "dummy/key", "dummy content", None),
        ("dummy-bucket", "dummy/key.alpha", "Old MacDonald had a farm", None),
        ("dummy-bucket", "dummy/key.beta", "Ee-i-ee-i-o", None),
        ("dummy-bucket", "dummy/key", "dummy content", "ascii"),
        ("dummy-bucket", "dummy/key.alpha", "Old MacDonald had a farm", "ascii"),
        ("dummy-bucket", "dummy/key.beta", "Ee-i-ee-i-o", "ascii"),
    )
    @ddt.unpack
    def test_s3_text(self, bucket, key, text, encoding):
        with moto.mock_aws(), s3_make_client(region_name="us-east-1") as client:
            client.create_bucket(Bucket=bucket)

            s3_push_text(client, text, bucket, key, encoding=encoding)
            self.assertEqual(s3_pull_text(client, bucket, key, encoding=encoding), text)
