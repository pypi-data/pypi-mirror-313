import contextlib
import unittest

import ddt
import docker.errors
import docker.models.containers
import docker.models.images
import pytest
import pytest_mock
import requests.exceptions

from iker.common.utils.dockerutils import *
from iker.common.utils.testutils import return_callee
from iker_tests.docker_fixtures import MockedDockerClient, MockedDockerContainer, MockedDockerImage


@ddt.ddt
class DockerUtilsTest(unittest.TestCase):

    def setUp(self):
        super(DockerUtilsTest, self).setUp()
        self.mocker = pytest_mock.MockerFixture(None)

    def tearDown(self):
        super(DockerUtilsTest, self).tearDown()
        self.mocker.stopall()

    @ddt.data(
        (
            "ubuntu",
            ImageName(None, None, ["ubuntu"], None),
            "",
            "ubuntu",
        ),
        (
            "ubuntu:latest",
            ImageName(None, None, ["ubuntu"], "latest"),
            "",
            "ubuntu",
        ),
        (
            "ubuntu:22.04",
            ImageName(None, None, ["ubuntu"], "22.04"),
            "",
            "ubuntu",
        ),
        (
            "canonical/ubuntu",
            ImageName(None, None, ["canonical", "ubuntu"], None),
            "",
            "canonical/ubuntu",
        ),
        (
            "canonical/ubuntu:latest",
            ImageName(None, None, ["canonical", "ubuntu"], "latest"),
            "",
            "canonical/ubuntu",
        ),
        (
            "canonical/ubuntu:22.04",
            ImageName(None, None, ["canonical", "ubuntu"], "22.04"),
            "",
            "canonical/ubuntu",
        ),
        (
            "hub.docker.com/canonical/ubuntu",
            ImageName("hub.docker.com", None, ["canonical", "ubuntu"], None),
            "hub.docker.com",
            "canonical/ubuntu",
        ),
        (
            "hub.docker.com/canonical/ubuntu:latest",
            ImageName("hub.docker.com", None, ["canonical", "ubuntu"], "latest"),
            "hub.docker.com",
            "canonical/ubuntu",
        ),
        (
            "hub.docker.com/canonical/ubuntu:22.04",
            ImageName("hub.docker.com", None, ["canonical", "ubuntu"], "22.04"),
            "hub.docker.com",
            "canonical/ubuntu",
        ),
        (
            "hub.docker.com:8080/canonical/ubuntu",
            ImageName("hub.docker.com", 8080, ["canonical", "ubuntu"], None),
            "hub.docker.com:8080",
            "canonical/ubuntu",
        ),
        (
            "hub.docker.com:8080/canonical/ubuntu:latest",
            ImageName("hub.docker.com", 8080, ["canonical", "ubuntu"], "latest"),
            "hub.docker.com:8080",
            "canonical/ubuntu",
        ),
        (
            "hub.docker.com:8080/canonical/ubuntu:22.04",
            ImageName("hub.docker.com", 8080, ["canonical", "ubuntu"], "22.04"),
            "hub.docker.com:8080",
            "canonical/ubuntu",
        ),
        (
            "hub.docker.com:8080/ubuntu",
            ImageName("hub.docker.com", 8080, ["ubuntu"], None),
            "hub.docker.com:8080",
            "ubuntu",
        ),
        (
            "hub.docker.com:8080/ubuntu:latest",
            ImageName("hub.docker.com", 8080, ["ubuntu"], "latest"),
            "hub.docker.com:8080",
            "ubuntu",
        ),
        (
            "hub.docker.com:8080/ubuntu:22.04",
            ImageName("hub.docker.com", 8080, ["ubuntu"], "22.04"),
            "hub.docker.com:8080",
            "ubuntu",
        ),
        (
            "hub.docker.com:8080/docker-hub/canonical/ubuntu",
            ImageName("hub.docker.com", 8080, ["docker-hub", "canonical", "ubuntu"], None),
            "hub.docker.com:8080",
            "docker-hub/canonical/ubuntu",
        ),
        (
            "hub.docker.com:8080/docker-hub/canonical/ubuntu:latest",
            ImageName("hub.docker.com", 8080, ["docker-hub", "canonical", "ubuntu"], "latest"),
            "hub.docker.com:8080",
            "docker-hub/canonical/ubuntu",
        ),
        (
            "hub.docker.com:8080/docker-hub/canonical/ubuntu:22.04",
            ImageName("hub.docker.com", 8080, ["docker-hub", "canonical", "ubuntu"], "22.04"),
            "hub.docker.com:8080",
            "docker-hub/canonical/ubuntu",
        ),
    )
    @ddt.unpack
    def test_image_name(self, image_name_str, image_name, registry, repository):
        actual = ImageName.parse(image_name_str)

        self.assertEqual(image_name.registry_host, actual.registry_host)
        self.assertEqual(image_name.registry_port, actual.registry_port)
        self.assertEqual(image_name.components, actual.components)
        self.assertEqual(image_name.tag, actual.tag)
        self.assertEqual(image_name.registry, actual.registry)
        self.assertEqual(image_name.repository, actual.repository)

        self.assertEqual(registry, actual.registry)
        self.assertEqual(repository, actual.repository)

    def test_docker_build_image(self):
        patched_images_build = self.mocker.patch.object(
            docker.models.images.ImageCollection,
            "build",
            return_value=(
                MockedDockerImage("dummy_image",
                                  tags_callee=return_callee("dummy_tags"),
                                  labels_callee=return_callee("dummy_labels")),
                {"dummy_key": "dummy_value"},
            ),
        )

        with contextlib.closing(MockedDockerClient()) as client:
            image_model, build_logs = docker_build_image(client,
                                                         "dummy_tag",
                                                         "dummy_path",
                                                         "dummy_dockerfile",
                                                         {"dummy_arg": "dummy_value"})

        self.assertEqual(image_model.id, "dummy_image")
        self.assertEqual(image_model.tags, "dummy_tags")
        self.assertEqual(image_model.labels, "dummy_labels")
        self.assertEqual(build_logs, {"dummy_key": "dummy_value"})

        patched_images_build.assert_called_with(tag="dummy_tag",
                                                path="dummy_path",
                                                dockerfile="dummy_dockerfile",
                                                buildargs={"dummy_arg": "dummy_value"},
                                                rm=True,
                                                forcerm=True,
                                                nocache=True)

    @ddt.data(
        (docker.errors.BuildError, ("dummy reason", "dummy log")),
        (docker.errors.APIError, ("dummy message",)),
        (Exception, ()),
    )
    @ddt.unpack
    def test_docker_build_image__with_exception(self, exception_type, exception_args):
        patched_images_build = self.mocker.patch.object(
            docker.models.images.ImageCollection,
            "build",
            return_value=(
                MockedDockerImage("dummy_image",
                                  tags_callee=return_callee("dummy_tags"),
                                  labels_callee=return_callee("dummy_labels")),
                {"dummy_key": "dummy_value"},
            ),
        )
        patched_images_build.side_effect = exception_type(*exception_args)

        with pytest.raises(exception_type):
            with contextlib.closing(MockedDockerClient()) as client:
                docker_build_image(client,
                                   "dummy_tag",
                                   "dummy_path",
                                   "dummy_dockerfile",
                                   {"dummy_arg": "dummy_value"})

        patched_images_build.assert_called_with(tag="dummy_tag",
                                                path="dummy_path",
                                                dockerfile="dummy_dockerfile",
                                                buildargs={"dummy_arg": "dummy_value"},
                                                rm=True,
                                                forcerm=True,
                                                nocache=True)

    def test_docker_get_image(self):
        patched_images_get = self.mocker.patch.object(
            docker.models.images.ImageCollection,
            "get",
            return_value=MockedDockerImage("dummy_image",
                                           tags_callee=return_callee("dummy_tags"),
                                           labels_callee=return_callee("dummy_labels")),
        )

        with contextlib.closing(MockedDockerClient()) as client:
            image_model = docker_get_image(client, "dummy_image")

        self.assertEqual(image_model.id, "dummy_image")
        self.assertEqual(image_model.tags, "dummy_tags")
        self.assertEqual(image_model.labels, "dummy_labels")

        patched_images_get.assert_called_with("dummy_image")

    @ddt.data(
        (docker.errors.ImageNotFound, ("dummy message",)),
        (docker.errors.APIError, ("dummy message",)),
        (Exception, ()),
    )
    @ddt.unpack
    def test_docker_get_image__with_exception(self, exception_type, exception_args):
        patched_images_get = self.mocker.patch.object(
            docker.models.images.ImageCollection,
            "get",
            return_value=MockedDockerImage("dummy_image",
                                           tags_callee=return_callee("dummy_tags"),
                                           labels_callee=return_callee("dummy_labels")),
        )
        patched_images_get.side_effect = exception_type(*exception_args)

        with pytest.raises(exception_type):
            with contextlib.closing(MockedDockerClient()) as client:
                docker_get_image(client, "dummy_image")

        patched_images_get.assert_called_with("dummy_image")

    def test_docker_pull_image(self):
        patched_images_get = self.mocker.patch.object(
            docker.models.images.ImageCollection,
            "get",
            return_value=MockedDockerImage("dummy_get_image",
                                           tags_callee=return_callee("dummy_get_tags"),
                                           labels_callee=return_callee("dummy_get_labels")),
        )

        patched_images_pull = self.mocker.patch.object(
            docker.models.images.ImageCollection,
            "pull",
            return_value=MockedDockerImage("dummy_pull_image",
                                           tags_callee=return_callee("dummy_pull_tags"),
                                           labels_callee=return_callee("dummy_pull_labels")),
        )

        with contextlib.closing(MockedDockerClient()) as client:
            image_model = docker_pull_image(client, "dummy_image", fallback_local=True)

        self.assertEqual(image_model.id, "dummy_pull_image")
        self.assertEqual(image_model.tags, "dummy_pull_tags")
        self.assertEqual(image_model.labels, "dummy_pull_labels")

        patched_images_get.assert_not_called()
        patched_images_pull.assert_called_with("dummy_image")

    def test_docker_pull_image__fallback(self):
        patched_images_get = self.mocker.patch.object(
            docker.models.images.ImageCollection,
            "get",
            return_value=MockedDockerImage("dummy_get_image",
                                           tags_callee=return_callee("dummy_get_tags"),
                                           labels_callee=return_callee("dummy_get_labels")),
        )

        patched_images_pull = self.mocker.patch.object(
            docker.models.images.ImageCollection,
            "pull",
            return_value=MockedDockerImage("dummy_pull_image",
                                           tags_callee=return_callee("dummy_pull_tags"),
                                           labels_callee=return_callee("dummy_pull_labels")),
        )
        patched_images_pull.side_effect = docker.errors.APIError("dummy message")

        with contextlib.closing(MockedDockerClient()) as client:
            image_model = docker_pull_image(client, "dummy_image", fallback_local=True)

        self.assertEqual(image_model.id, "dummy_get_image")
        self.assertEqual(image_model.tags, "dummy_get_tags")
        self.assertEqual(image_model.labels, "dummy_get_labels")

        patched_images_get.assert_called_with("dummy_image")
        patched_images_pull.assert_called_with("dummy_image")

    @ddt.data(
        (docker.errors.ImageNotFound, ("dummy message",)),
        (docker.errors.APIError, ("dummy message",)),
        (Exception, ()),
    )
    @ddt.unpack
    def test_docker_pull_image__with_exception(self, exception_type, exception_args):
        patched_images_get = self.mocker.patch.object(
            docker.models.images.ImageCollection,
            "get",
            return_value=MockedDockerImage("dummy_get_image",
                                           tags_callee=return_callee("dummy_get_tags"),
                                           labels_callee=return_callee("dummy_get_labels")),
        )
        patched_images_get.side_effect = docker.errors.APIError("dummy message")

        patched_images_pull = self.mocker.patch.object(
            docker.models.images.ImageCollection,
            "pull",
            return_value=MockedDockerImage("dummy_pull_image",
                                           tags_callee=return_callee("dummy_pull_tags"),
                                           labels_callee=return_callee("dummy_pull_labels")),
        )
        patched_images_pull.side_effect = exception_type(*exception_args)

        with pytest.raises(exception_type):
            with contextlib.closing(MockedDockerClient()) as client:
                docker_pull_image(client, "dummy_image", fallback_local=False)

        patched_images_get.assert_not_called()
        patched_images_pull.assert_called_with("dummy_image")

    @ddt.data(
        (docker.errors.ImageNotFound, ("dummy message",)),
        (docker.errors.APIError, ("dummy message",)),
        (Exception, ()),
    )
    @ddt.unpack
    def test_docker_pull_image__fallback_with_exception(self, exception_type, exception_args):
        patched_images_get = self.mocker.patch.object(
            docker.models.images.ImageCollection,
            "get",
            return_value=MockedDockerImage("dummy_get_image",
                                           tags_callee=return_callee("dummy_get_tags"),
                                           labels_callee=return_callee("dummy_get_labels")),
        )
        patched_images_get.side_effect = exception_type(*exception_args)

        patched_images_pull = self.mocker.patch.object(
            docker.models.images.ImageCollection,
            "pull",
            return_value=MockedDockerImage("dummy_pull_image",
                                           tags_callee=return_callee("dummy_pull_tags"),
                                           labels_callee=return_callee("dummy_pull_labels")),
        )
        patched_images_pull.side_effect = docker.errors.APIError("dummy message")

        with pytest.raises(exception_type):
            with contextlib.closing(MockedDockerClient()) as client:
                docker_pull_image(client, "dummy_image", fallback_local=True)

        patched_images_get.assert_called_with("dummy_image")
        patched_images_pull.assert_called_with("dummy_image")

    def test_docker_run_detached(self):
        patched_containers_run_status_callee = return_callee("dummy_status")
        patched_containers_run_wait_callee = return_callee({"dummy_key": "dummy_value"})
        patched_containers_run_logs_callee = return_callee("dummy log")
        patched_containers_run_stop_callee = return_callee()
        patched_containers_run_remove_callee = return_callee()

        patched_containers_run = self.mocker.patch.object(
            docker.models.containers.ContainerCollection,
            "run",
            return_value=MockedDockerContainer("dummy_container",
                                               status_callee=patched_containers_run_status_callee,
                                               wait_callee=patched_containers_run_wait_callee,
                                               logs_callee=patched_containers_run_logs_callee,
                                               stop_callee=patched_containers_run_stop_callee,
                                               remove_callee=patched_containers_run_remove_callee),
        )

        with contextlib.closing(MockedDockerClient()) as client:
            result, log = docker_run_detached(client,
                                              "dummy_image",
                                              "dummy_container",
                                              "dummy_command",
                                              {"/dummy/src/path": {"bind": "/dummy/dst/path", "mode": "rw"}},
                                              {"DUMMY_ENV_KEY": "DUMMY_ENV_VALUE"},
                                              {"dummy.ip.address": "127.0.0.1"},
                                              1000,
                                              dummy_kwarg="dummy_value")

        self.assertEqual(result, {"dummy_key": "dummy_value"})
        self.assertEqual(log, "dummy log")

        patched_containers_run.assert_called_with(
            image="dummy_image",
            name="dummy_container",
            command="dummy_command",
            volumes={"/dummy/src/path": {"bind": "/dummy/dst/path", "mode": "rw"}},
            environment={"DUMMY_ENV_KEY": "DUMMY_ENV_VALUE"},
            extra_hosts={"dummy.ip.address": "127.0.0.1"},
            detach=True,
            dummy_kwarg="dummy_value",
        )
        patched_containers_run_status_callee.assert_called_once()
        patched_containers_run_wait_callee.assert_called_once_with()(timeout=1000)
        patched_containers_run_wait_callee.assert_called_once_with()()
        patched_containers_run_logs_callee.assert_called_once()
        patched_containers_run_stop_callee.assert_called_once()
        patched_containers_run_remove_callee.assert_called_once()

    @ddt.data(
        (requests.exceptions.ReadTimeout, ()),
        (docker.errors.ImageNotFound, ("dummy message",)),
        (
            docker.errors.ContainerError,
            ("dummy container", "dummy exit status", "dummy command", "dummy image", "dummy stderr"),
        ),
        (docker.errors.APIError, ("dummy message",)),
        (Exception, ()),
    )
    @ddt.unpack
    def test_docker_run_detached__with_exception_on_wait(self, exception_type, exception_args):
        def patched_containers_run_wait_valuer(*args, **kwargs):
            if kwargs == dict(timeout=1000):
                raise exception_type(*exception_args)

        patched_containers_run_status_callee = return_callee("dummy_status")
        patched_containers_run_wait_callee = return_callee(patched_containers_run_wait_valuer)
        patched_containers_run_logs_callee = return_callee("dummy log")
        patched_containers_run_stop_callee = return_callee()
        patched_containers_run_remove_callee = return_callee()

        patched_containers_run = self.mocker.patch.object(
            docker.models.containers.ContainerCollection,
            "run",
            return_value=MockedDockerContainer("dummy_container",
                                               status_callee=patched_containers_run_status_callee,
                                               wait_callee=patched_containers_run_wait_callee,
                                               logs_callee=patched_containers_run_logs_callee,
                                               stop_callee=patched_containers_run_stop_callee,
                                               remove_callee=patched_containers_run_remove_callee),
        )

        with pytest.raises(exception_type):
            with contextlib.closing(MockedDockerClient()) as client:
                docker_run_detached(client,
                                    "dummy_image",
                                    "dummy_container",
                                    "dummy_command",
                                    {"/dummy/src/path": {"bind": "/dummy/dst/path", "mode": "rw"}},
                                    {"DUMMY_ENV_KEY": "DUMMY_ENV_VALUE"},
                                    {"dummy.ip.address": "127.0.0.1"},
                                    1000,
                                    dummy_kwarg="dummy_value")

        patched_containers_run.assert_called_with(
            image="dummy_image",
            name="dummy_container",
            command="dummy_command",
            volumes={"/dummy/src/path": {"bind": "/dummy/dst/path", "mode": "rw"}},
            environment={"DUMMY_ENV_KEY": "DUMMY_ENV_VALUE"},
            extra_hosts={"dummy.ip.address": "127.0.0.1"},
            detach=True,
            dummy_kwarg="dummy_value",
        )
        patched_containers_run_status_callee.assert_called_once()
        patched_containers_run_wait_callee.assert_called_once_with()(timeout=1000)
        patched_containers_run_wait_callee.assert_called_once_with()()
        patched_containers_run_logs_callee.assert_not_called()
        patched_containers_run_stop_callee.assert_called_once()
        patched_containers_run_remove_callee.assert_called_once()

    @ddt.data(
        (docker.errors.ImageNotFound, ("dummy message",)),
        (
            docker.errors.ContainerError,
            ("dummy container", "dummy exit status", "dummy command", "dummy image", "dummy stderr"),
        ),
        (docker.errors.APIError, ("dummy message",)),
    )
    @ddt.unpack
    def test_docker_run_detached__with_exception_on_stop(self, exception_type, exception_args):
        def patched_containers_run_stop_valuer(*args, **kwargs):
            raise exception_type(*exception_args)

        patched_containers_run_status_callee = return_callee("dummy_status")
        patched_containers_run_wait_callee = return_callee({"dummy_key": "dummy_value"})
        patched_containers_run_logs_callee = return_callee("dummy log")
        patched_containers_run_stop_callee = return_callee(patched_containers_run_stop_valuer)
        patched_containers_run_remove_callee = return_callee()

        patched_containers_run = self.mocker.patch.object(
            docker.models.containers.ContainerCollection,
            "run",
            return_value=MockedDockerContainer("dummy_container",
                                               status_callee=patched_containers_run_status_callee,
                                               wait_callee=patched_containers_run_wait_callee,
                                               logs_callee=patched_containers_run_logs_callee,
                                               stop_callee=patched_containers_run_stop_callee,
                                               remove_callee=patched_containers_run_remove_callee),
        )

        with contextlib.closing(MockedDockerClient()) as client:
            result, log = docker_run_detached(client,
                                              "dummy_image",
                                              "dummy_container",
                                              "dummy_command",
                                              {"/dummy/src/path": {"bind": "/dummy/dst/path", "mode": "rw"}},
                                              {"DUMMY_ENV_KEY": "DUMMY_ENV_VALUE"},
                                              {"dummy.ip.address": "127.0.0.1"},
                                              1000,
                                              dummy_kwarg="dummy_value")

        self.assertEqual(result, {"dummy_key": "dummy_value"})
        self.assertEqual(log, "dummy log")

        patched_containers_run.assert_called_with(
            image="dummy_image",
            name="dummy_container",
            command="dummy_command",
            volumes={"/dummy/src/path": {"bind": "/dummy/dst/path", "mode": "rw"}},
            environment={"DUMMY_ENV_KEY": "DUMMY_ENV_VALUE"},
            extra_hosts={"dummy.ip.address": "127.0.0.1"},
            detach=True,
            dummy_kwarg="dummy_value",
        )
        patched_containers_run_status_callee.assert_called_once()
        patched_containers_run_wait_callee.assert_called_once_with()(timeout=1000)
        patched_containers_run_wait_callee.assert_called_once_with()()
        patched_containers_run_logs_callee.assert_called_once()
        patched_containers_run_stop_callee.assert_called_once()
        patched_containers_run_remove_callee.assert_called_once()
