import configparser
from unittest import mock

import pytest
import typer
from minio import S3Error

from neosctl.services.storage import storage
from tests.helper import render_cmd_output


@pytest.fixture(autouse=True)
def mock_minio(monkeypatch):
    minio_client = mock.Mock()
    monkeypatch.setattr(storage.minio, "Minio", mock.Mock(return_value=minio_client))
    return minio_client


@pytest.fixture(autouse=True)
def credential(request, credential_filepath):
    if "nocredential_patch" in request.keywords:
        return None
    c = configparser.ConfigParser()
    c["test"] = {"access_key_id": "access-key", "secret_access_key": "secret-key"}

    with credential_filepath.open("w") as credential_file:
        c.write(credential_file)

    return c


STORAGE_URL = "https://saas.core-gateway/{}"


def test_list_buckets(cli_runner, mock_minio):
    mock_minio.list_buckets = mock.Mock(return_value=["test", "tmp"])

    result = cli_runner.invoke(
        [
            "storage",
            "bucket",
            "list",
        ],
    )

    assert result.exit_code == 0
    assert mock_minio.list_buckets.call_args == mock.call()


@pytest.mark.nocredential_patch
def test_list_buckets_no_credentials(cli_runner, mock_minio):
    mock_minio.list_buckets = mock.Mock(return_value=["test", "tmp"])

    result = cli_runner.invoke(
        [
            "storage",
            "bucket",
            "list",
        ],
    )

    assert result.exit_code == 1
    assert result.output == "Environment test not configured with credentials.\n"


@pytest.mark.parametrize("command", ["create", "delete"])
def test_manage_bucket_fails(cli_runner, command):
    result = cli_runner.invoke(
        [
            "storage",
            "bucket",
            command,
            "",
        ],
    )

    assert result.exit_code == typer.BadParameter.exit_code
    cli_runner.assert_output_contains("Value does not satisfy the rule\n ^[a-z0-9][a-z0-9\\.\\-]{2,62}$")


def test_create_bucket(cli_runner, mock_minio):
    result = cli_runner.invoke(
        [
            "storage",
            "bucket",
            "create",
            "test-bucket",
        ],
    )

    assert result.exit_code == 0
    assert mock_minio.make_bucket.call_args == mock.call("test-bucket")


def test_delete_bucket(cli_runner, mock_minio):
    result = cli_runner.invoke(
        [
            "storage",
            "bucket",
            "delete",
            "test-bucket",
        ],
    )

    assert result.exit_code == 0
    assert mock_minio.remove_bucket.call_args == mock.call("test-bucket")


def test_list_objects(cli_runner, mock_minio):
    mock_minio.list_objects = mock.Mock(return_value=[])
    result = cli_runner.invoke(
        [
            "storage",
            "object",
            "list",
            "test-bucket",
        ],
    )

    assert result.exit_code == 0
    assert mock_minio.list_objects.call_args == mock.call("test-bucket", prefix=None, recursive=False)


def test_list_objects_with_prefix(cli_runner, mock_minio):
    mock_minio.list_objects = mock.Mock(return_value=[])
    result = cli_runner.invoke(
        [
            "storage",
            "object",
            "list",
            "test-bucket",
            "--prefix",
            "path/to/file/",
        ],
    )

    assert result.exit_code == 0
    assert mock_minio.list_objects.call_args == mock.call("test-bucket", prefix="path/to/file/", recursive=False)


def test_list_objects_recursive(cli_runner, mock_minio):
    mock_minio.list_objects = mock.Mock(return_value=[])
    result = cli_runner.invoke(
        [
            "storage",
            "object",
            "list",
            "test-bucket",
            "--recursive",
        ],
    )

    assert result.exit_code == 0
    assert mock_minio.list_objects.call_args == mock.call("test-bucket", prefix=None, recursive=True)


@pytest.mark.parametrize(
    ("prefix", "target_prefix", "object_path"),
    [
        ("source/path", "target/path", "target/path"),
        ("source/path/", "target/path/", "target/path"),
        (None, "target/path", "target/path/source/path"),
        (None, "target/path/", "target/path/source/path"),
        ("source/path", None, "source/path"),
        ("source/path/", None, "source/path"),
        (None, None, "source/path"),
    ],
)
def test_copy_object(cli_runner, mock_minio, prefix, target_prefix, object_path):
    mock_minio.list_objects = mock.Mock(
        return_value=[mock.Mock(_object_name="source/path/file1.txt"), mock.Mock(_object_name="source/path/file2.txt")],
    )
    args = [
        "storage",
        "object",
        "copy",
        "source-bucket",
        "target-bucket",
    ]
    if prefix:
        args.extend(["--prefix", prefix])
    if target_prefix:
        args.extend(["--target-prefix", target_prefix])
    result = cli_runner.invoke(args)

    class MockCopySource:
        def __init__(self, source, path):
            self.source = source
            self.path = path

        def __eq__(self, other):
            return (
                isinstance(other, storage.CopySource)
                and other._bucket_name == self.source
                and other._object_name == self.path
            )

    assert result.exit_code == 0, result.output
    assert mock_minio.copy_object.call_args_list == [
        mock.call(
            "target-bucket",
            f"{object_path}/file1.txt",
            MockCopySource("source-bucket", "source/path/file1.txt"),
        ),
        mock.call(
            "target-bucket",
            f"{object_path}/file2.txt",
            MockCopySource("source-bucket", "source/path/file2.txt"),
        ),
    ]


@pytest.mark.parametrize(
    ("command", "bucket_name", "object_name", "file_path", "message"),
    [
        (
            "create",
            "",
            "test-object",
            "test-file-path",
            "Value does not satisfy the rule\n ^[a-z0-9][a-z0-9\\.\\-]{2,62}$",
        ),
        (
            "create",
            "test-bucket",
            "",
            "test-file-path",
            "Value must be a non-empty string.",
        ),
        ("create", "test-bucket", "test-object", "", "Invalid value for 'FILE': Value must be a non-empty string."),
        (
            "get",
            "",
            "test-object",
            "test-file-path",
            "Value does not satisfy the rule\n ^[a-z0-9][a-z0-9\\.\\-]{2,62}$",
        ),
        (
            "get",
            "test-bucket",
            "",
            "test-file-path",
            "Value must be a non-empty string.",
        ),
        ("get", "test-bucket", "test-object", "", "Invalid value for 'FILE': Value must be a non-empty string."),
        ("delete", "", "test-object", None, "Value does not satisfy the rule\n ^[a-z0-9][a-z0-9\\.\\-]{2,62}$"),
        (
            "delete",
            "test-bucket",
            "",
            None,
            "Value must be a non-empty string.",
        ),
    ],
)
def test_manage_object_fails(cli_runner, command, bucket_name, object_name, file_path, message):
    invoke_args = [
        "storage",
        "object",
        command,
        bucket_name,
        object_name,
    ]
    if file_path is not None:
        invoke_args.append(file_path)
    result = cli_runner.invoke(invoke_args)

    assert result.exit_code == typer.BadParameter.exit_code
    cli_runner.assert_output_contains(message)


def test_create_object(cli_runner, mock_minio, tmp_path):
    fp = tmp_path / "file.txt"
    with fp.open("wb") as fh:
        fh.write(b"file content")

    result = cli_runner.invoke(
        [
            "storage",
            "object",
            "create",
            "test-bucket",
            "test-object",
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert mock_minio.fput_object.call_args == mock.call(
        "test-bucket",
        "test-object",
        str(fp.resolve()),
    )


def test_get_object(cli_runner, mock_minio, tmp_path):
    mock_minio.get_object.return_value = mock.Mock(data=b"object content")

    fp = tmp_path / "file.txt"

    result = cli_runner.invoke(
        [
            "storage",
            "object",
            "get",
            "test-bucket",
            "test-object",
            str(fp.resolve()),
        ],
    )

    with fp.open("rb") as fh:
        file_content = fh.read()

    assert result.exit_code == 0
    assert file_content == b"object content"


def test_get_not_found_object(cli_runner, mock_minio, tmp_path):
    response_payload = {
        "code": "TestCode",
        "message": "test message",
    }

    def raise_error(*args, **kwargs):  # noqa: ARG001
        code = "TestCode"
        message = "test message"
        resource = "resource"
        request_id = "request_id"
        host_id = "host_id"
        response = mock.Mock()

        raise S3Error(code, message, resource, request_id, host_id, response)

    mock_minio.get_object.side_effect = raise_error

    fp = tmp_path / "file.txt"

    result = cli_runner.invoke(
        [
            "storage",
            "object",
            "get",
            "test-bucket",
            "test-object",
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 1
    assert result.output == render_cmd_output(response_payload)


def test_delete_object(cli_runner, mock_minio):
    result = cli_runner.invoke(
        [
            "storage",
            "object",
            "delete",
            "test-bucket",
            "test-object",
        ],
    )

    assert result.exit_code == 0
    assert mock_minio.remove_object.call_args == mock.call("test-bucket", "test-object")


@pytest.mark.parametrize(
    ("command", "bucket_name", "object_name", "tags", "message"),
    [
        (
            "set",
            "",
            "test-object",
            ["tag1=value1", "tag2=value2"],
            "Value does not satisfy the rule\n ^[a-z0-9][a-z0-9\\.\\-]{2,62}$",
        ),
        (
            "set",
            "test-bucket",
            "",
            ["tag1=value1", "tag2=value2"],
            "Value must be a non-empty string.",
        ),
        ("set", "test-bucket", "test-object", [""], "Invalid value for 'TAGS...': Value must be a non-empty string."),
        ("get", "", "test-object", None, "Value does not satisfy the rule\n ^[a-z0-9][a-z0-9\\.\\-]{2,62}$"),
        ("get", "test-bucket", "", None, "Value must be a non-empty string."),
        ("delete", "", "test-object", None, "Value does not satisfy the rule\n ^[a-z0-9][a-z0-9\\.\\-]{2,62}$"),
        (
            "delete",
            "test-bucket",
            "",
            None,
            "Value must be a non-empty string.",
        ),
    ],
)
def test_manage_object_tags_fails(cli_runner, command, bucket_name, object_name, tags, message):
    invoke_args = [
        "storage",
        "object",
        "tags",
        command,
        bucket_name,
        object_name,
    ]
    if tags is not None:
        invoke_args.extend(tags)
    result = cli_runner.invoke(invoke_args)

    assert result.exit_code == typer.BadParameter.exit_code
    cli_runner.assert_output_contains(message)


def test_set_object_tags(cli_runner, mock_minio):
    result = cli_runner.invoke(
        [
            "storage",
            "object",
            "tags",
            "set",
            "test-bucket",
            "test-object",
            "key-cli=value-cli",
            "testk=testv",
        ],
    )

    assert result.exit_code == 0
    assert mock_minio.set_object_tags.call_args == mock.call(
        "test-bucket",
        "test-object",
        {
            "key-cli": "value-cli",
            "testk": "testv",
        },
    )


def test_get_object_tags(cli_runner, mock_minio):
    result = cli_runner.invoke(
        [
            "storage",
            "object",
            "tags",
            "get",
            "test-bucket",
            "test-object",
        ],
    )

    assert result.exit_code == 0
    assert mock_minio.get_object_tags.call_args == mock.call("test-bucket", "test-object")


def test_delete_object_tags(cli_runner, mock_minio):
    result = cli_runner.invoke(
        [
            "storage",
            "object",
            "tags",
            "delete",
            "test-bucket",
            "test-object",
        ],
    )

    assert result.exit_code == 0
    assert mock_minio.delete_object_tags.call_args == mock.call("test-bucket", "test-object")
