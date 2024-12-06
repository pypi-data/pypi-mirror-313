from unittest import mock

import pytest
import typer

from neosctl.env import get_cores
from tests.helper import render_cmd_output


def test_get_cores(httpx_mock):
    response_payload = {
        "cores": [
            {
                "host": None,
                "name": "local",
                "version": "v1.2.3",
                "account": "dev",
                "urn": "urn:ksa:core:166601224459",
            },
            {
                "host": None,
                "name": "my-core",
                "version": "v1.2.3",
                "account": "test",
                "urn": "urn:ksa:core:166601243158",
            },
            {
                "host": "https://core",
                "name": "smartconstruction",
                "version": "v1.2.2",
                "account": "smartcon",
                "urn": "urn:ksa:core:166601412405",
            },
        ],
    }
    httpx_mock.add_response(
        method="GET",
        url="https://hub/registry/core",
        json=response_payload,
    )

    ctx = typer.Context(mock.Mock())
    ctx.obj = mock.Mock()
    ctx.obj.credential = {}
    ctx.obj.http_proxy = None
    ctx.obj.account = "root"
    ctx.obj.hub_api_url = "https://hub"

    result = get_cores(ctx)

    assert result.json() == {
        "cores": [
            {
                "host": None,
                "name": "local",
                "version": "v1.2.3",
                "account": "dev",
                "urn": "urn:ksa:core:166601224459",
            },
            {
                "host": None,
                "name": "my-core",
                "version": "v1.2.3",
                "account": "test",
                "urn": "urn:ksa:core:166601243158",
            },
            {
                "host": "https://core",
                "name": "smartconstruction",
                "version": "v1.2.2",
                "account": "smartcon",
                "urn": "urn:ksa:core:166601412405",
            },
        ],
    }


def test_get_cores_failure(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url="https://hub/registry/core",
        json={
            "type": "authorization-required",
            "error": {
                "error": "invalid_grant",
                "error_description": "Token is not active",
            },
            "title": "Problem with Identity Access Manager.",
        },
        status_code=401,
    )

    ctx = typer.Context(mock.Mock())
    ctx.obj = mock.Mock()
    ctx.obj.credential = {}
    ctx.obj.http_proxy = None
    ctx.obj.account = "root"
    ctx.obj.hub_api_url = "https://hub"

    with pytest.raises(typer.Exit):
        get_cores(ctx)


def test_init_new_env(cli_runner, env_filepath):
    args = [
        "-h",
        "https://hub",
        "-u",
        "some-username",
        "-a",
        "root",
        "-p",
        "http://proxy",
    ]
    result = cli_runner.invoke(
        ["env", "init", "test", *args],
    )

    assert result.exit_code == 0, result.output

    config_file = """[test]
hub_api_url = "https://hub"
user = "some-username"
access_token = ""
refresh_token = ""
ignore_tls = false
active = false
account = "root"
http_proxy = "http://proxy"

[test.cores]
"""

    with env_filepath.open() as f:
        assert f.read() == config_file


def test_init_new_env_ignore_tls(cli_runner, env_filepath):
    args = [
        "-h",
        "https://hub",
        "-u",
        "some-username",
        "-a",
        "root",
    ]
    # Add default env
    result = cli_runner.invoke(
        ["env", "init", "test", "--ignore-tls", *args],
    )

    assert result.exit_code == 0

    config_file = """[test]
hub_api_url = "https://hub"
user = "some-username"
access_token = ""
refresh_token = ""
ignore_tls = true
active = false
account = "root"
http_proxy = "null"

[test.cores]
"""

    with env_filepath.open() as f:
        assert f.read() == config_file


def test_init_new_env_url_validation(cli_runner):
    args = [
        "-h",
        "hub",
        "-u",
        "some-username",
        "-a",
        "root",
    ]
    # Add default env
    result = cli_runner.invoke(
        ["env", "init", "test", *args],
    )

    assert result.exit_code == 2  # noqa: PLR2004
    cli_runner.assert_output(
        r"""Initialising [test] environment.
Usage: neosctl env init [OPTIONS] NAME
Try 'neosctl env init --help' for help.

 Error

 Invalid url, must match pattern: `re.compile('http[s]?:\\/\\/.*')`.
""",
    )


def test_init_existing_env(cli_runner, env_filepath, env_dotfile_factory):
    envs = {
        "test": {
            "hub_api_url": "https://hub",
            "user": "some-username",
            "access_token": "",
            "refresh_token": "",
            "ignore_tls": False,
            "active": True,
            "active_core": {"name": "core", "host": "https://gateway"},
            "account": "root",
            "cores": {
                "core": {"name": "core", "host": "https://gateway", "active": True, "account": "test"},
            },
        },
    }
    env_dotfile_factory(envs)

    args = [
        "-h",
        "https://a-new-hub",
        "-u",
        "some-username",
        "-a",
        "root",
    ]
    # Add another env
    result = cli_runner.invoke(["env", "init", "test", *args])

    assert result.exit_code == 0

    config_file = """[test]
hub_api_url = "https://a-new-hub"
user = "some-username"
access_token = ""
refresh_token = ""
ignore_tls = false
active = true
account = "root"
http_proxy = "null"
[test.cores.core]
name = "core"
host = "https://gateway"
account = "test"
active = true
"""

    with env_filepath.open() as f:
        assert config_file == f.read()


@pytest.mark.usefixtures("env_dotfile")
def test_init_additional_env(cli_runner, env_filepath):
    args = [
        "-h",
        "https://a-new-hub",
        "-u",
        "another-username",
        "-a",
        "foo",
    ]
    # Add another env
    result = cli_runner.invoke(["env", "init", "foo", *args])

    assert result.exit_code == 0

    config_file = """[test]
hub_api_url = "https://hub-host/api/hub"
user = "some-username"
access_token = ""
refresh_token = ""
ignore_tls = false
active = false
account = "root"

[test.cores]

[foo]
hub_api_url = "https://a-new-hub"
user = "another-username"
access_token = ""
refresh_token = ""
ignore_tls = false
active = false
account = "foo"
http_proxy = "null"

[foo.cores]
"""

    with env_filepath.open() as f:
        assert config_file == f.read()


def test_view(cli_runner, env_dotfile):
    result = cli_runner.invoke(["env", "view", "test"])

    assert result.exit_code == 0, result.output
    data = env_dotfile["test"]
    data["http_proxy"] = None
    assert result.output == render_cmd_output({"name": "test", **data})


def test_active(cli_runner, active_env_dotfile):
    result = cli_runner.invoke(["env", "active"])

    assert result.exit_code == 0, result.output
    data = active_env_dotfile["test"]
    data["http_proxy"] = None
    assert result.output == render_cmd_output({"name": "test", **data})


@pytest.mark.usefixtures("active_env_dotfile")
def test_list(cli_runner):
    result = cli_runner.invoke(["env", "list"])

    assert result.exit_code == 0
    assert (
        result.output
        == """Environment Name    Active
------------------  --------
test                *
"""
    )


def test_credentials(cli_runner, credential_filepath):
    result = cli_runner.invoke(["env", "credentials", "test", "key", "secret"])

    assert result.exit_code == 0

    config_file = """[test]
access_key_id = key
secret_access_key = secret

"""

    with credential_filepath.open() as f:
        assert config_file == f.read()


@pytest.mark.usefixtures("env_dotfile")
def test_delete(cli_runner, env_filepath):
    result = cli_runner.invoke(["env", "delete", "test"], input="y\n")

    assert result.exit_code == 0

    with env_filepath.open() as f:
        assert not f.read()


def test_delete_unknown_env(cli_runner):
    result = cli_runner.invoke(["env", "delete", "foo"], input="y\n")

    assert result.exit_code == 1
    assert (
        result.output
        == """Remove [foo] environment [y/N]: y
Can not remove foo environment, environment not found.
"""
    )


@pytest.mark.usefixtures("env_dotfile")
def test_delete_abort(cli_runner, env_filepath):
    result = cli_runner.invoke(["env", "delete", "test"], input="n\n")

    assert result.exit_code == 1

    with env_filepath.open() as f:
        assert (
            f.read()
            == """[test]
hub_api_url = "https://hub-host/api/hub"
user = "some-username"
access_token = ""
refresh_token = ""
ignore_tls = false
active = false
account = "root"

[test.cores]
"""
        )


@pytest.mark.usefixtures("env_dotfile")
def test_activate(cli_runner, env_filepath, httpx_mock):
    response_payload = {
        "cores": [
            {
                "host": None,
                "name": "local",
                "version": "v1.2.3",
                "account": "dev",
                "urn": "urn:ksa:core:166601224459",
            },
            {
                "host": None,
                "name": "my-core",
                "version": "v1.2.3",
                "account": "test",
                "urn": "urn:ksa:core:166601243158",
            },
            {
                "host": "https://core",
                "name": "smartconstruction",
                "version": "v1.2.2",
                "account": "smartcon",
                "urn": "urn:ksa:core:166601412405",
            },
        ],
    }
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/registry/core",
        json=response_payload,
    )
    result = cli_runner.invoke(["env", "activate", "test"])

    assert result.exit_code == 0

    with env_filepath.open() as f:
        assert (
            f.read()
            == """[test]
hub_api_url = "https://hub-host/api/hub"
user = "some-username"
access_token = ""
refresh_token = ""
ignore_tls = false
active = true
account = "root"
http_proxy = "null"
[test.cores.smartconstruction]
name = "smartconstruction"
host = "https://core"
account = "smartcon"
active = false
"""
        )


@pytest.mark.usefixtures("active_env_dotfile")
def test_activate_unknown(cli_runner, env_filepath):
    result = cli_runner.invoke(["env", "activate", "unknown"])

    assert result.exit_code == 1
    assert result.output == "Activating [unknown] environment.\nEnvironment unknown not found.\n"

    with env_filepath.open() as f:
        assert (
            f.read()
            == """[test]
hub_api_url = "https://hub-host/api/hub"
user = "some-username"
access_token = "access-token"
refresh_token = "refresh-token"
ignore_tls = false
active = false
account = "root"
http_proxy = "null"

[test.cores]
"""
        )


@pytest.mark.usefixtures("active_env_core_dotfile")
def test_activate_no_refresh(cli_runner, env_filepath):
    result = cli_runner.invoke(["env", "activate", "test", "--no-refresh"])

    assert result.exit_code == 0

    with env_filepath.open() as f:
        assert (
            f.read()
            == """[test]
hub_api_url = "https://hub-host/api/hub"
user = "some-username"
access_token = "access-token"
refresh_token = "refresh-token"
ignore_tls = false
active = true
account = "root"
http_proxy = "null"
[test.cores.smartconstruction]
name = "smartconstruction"
host = "https://core-gateway/api/gateway"
account = "sc"
active = true
"""
        )


@pytest.mark.usefixtures("active_env_dotfile")
def test_set_account(cli_runner, env_filepath):
    result = cli_runner.invoke(["env", "set-account", "foo"])

    assert result.exit_code == 0

    with env_filepath.open() as f:
        assert (
            f.read()
            == """[test]
hub_api_url = "https://hub-host/api/hub"
user = "some-username"
access_token = "access-token"
refresh_token = "refresh-token"
ignore_tls = false
active = true
account = "foo"
http_proxy = "null"

[test.cores]
"""
        )


IAM_URL = "https://hub-host/api/hub/iam"
LOGIN_URL = f"{IAM_URL}/login"
REFRESH_URL = f"{IAM_URL}/refresh"
LOGOUT_URL = f"{IAM_URL}/logout"


@pytest.mark.usefixtures("active_env_dotfile")
def test_login(cli_runner, httpx_mock):
    payload = {
        "access_token": "some-access-token",
        "refresh_token": "some-refresh-token",
        "expires_in": "300",
        "refresh_expires_in": "1800",
        "scope": "email profile",
        "token_type": "Bearer",
        "session_state": "some-session-state",
    }

    httpx_mock.add_response(
        method="POST",
        url=LOGIN_URL,
        json=payload,
    )

    result = cli_runner.invoke(["env", "login"], input="some-pass\n")

    assert result.exit_code == 0
    assert "Login success" in result.output


@pytest.mark.usefixtures("active_env_dotfile")
def test_login_non_interactive(cli_runner, httpx_mock):
    payload = {
        "access_token": "some-access-token",
        "refresh_token": "some-refresh-token",
        "expires_in": "300",
        "refresh_expires_in": "1800",
        "scope": "email profile",
        "token_type": "Bearer",
        "session_state": "some-session-state",
    }

    httpx_mock.add_response(
        method="POST",
        url=LOGIN_URL,
        json=payload,
    )

    result = cli_runner.invoke(["env", "login", "-p", "some-pass"])

    assert result.exit_code == 0
    assert "Login success" in result.output


@pytest.mark.usefixtures("active_env_dotfile")
def test_login_bad_credentials(cli_runner, httpx_mock):
    payload = {
        "type": "failed-authorization",
        "title": "Authorization failed.",
        "error": {
            "error": "invalid_grant",
            "error_description": "Invalid user credentials",
        },
    }

    httpx_mock.add_response(
        url=LOGIN_URL,
        json=payload,
        status_code=401,
    )

    result = cli_runner.invoke(["env", "login"], input="some-pass\n")

    assert result.exit_code == 1
    assert (
        result.output
        == f"[test] Enter password for user (some-username): \n{render_cmd_output(payload, sort_keys=False)}"
    )


@pytest.mark.usefixtures("active_env_dotfile")
def test_logout(cli_runner, httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url=LOGOUT_URL,
        json={},
    )
    result = cli_runner.invoke(["env", "logout"])

    assert result.exit_code == 0
    assert "Logout success" in result.output


@pytest.mark.usefixtures("active_env_dotfile")
def test_logout_bad_credentials(cli_runner, httpx_mock):
    payload = {
        "type": "failed-authorization",
        "title": "Authorization failed.",
        "error": {
            "error": "invalid_grant",
            "error_description": "Invalid user credentials",
        },
    }

    httpx_mock.add_response(
        url=LOGOUT_URL,
        json=payload,
        status_code=401,
    )

    result = cli_runner.invoke(["env", "logout"])

    assert result.exit_code == 1
    assert result.output == render_cmd_output(payload, sort_keys=False)


@pytest.mark.usefixtures("active_env_core_dotfile")
def test_list_cores(cli_runner, httpx_mock):
    response_payload = {
        "cores": [
            {
                "host": None,
                "name": "local",
                "version": "v1.2.3",
                "account": "dev",
                "urn": "urn:ksa:core:166601224459",
            },
            {
                "host": None,
                "name": "my-core",
                "version": "v1.2.3",
                "account": "test",
                "urn": "urn:ksa:core:166601243158",
            },
            {
                "host": "https://core",
                "name": "smartconstruction",
                "version": "v1.2.2",
                "account": "smartcon",
                "urn": "urn:ksa:core:166601412405",
            },
        ],
    }
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/registry/core",
        json=response_payload,
    )

    result = cli_runner.invoke(["env", "list-cores"])

    assert result.exit_code == 0, result.output
    assert (
        result.output
        == """
Core Name          Version    Host          Account    Urn                        Active
-----------------  ---------  ------------  ---------  -------------------------  --------
local              v1.2.3                   dev        urn:ksa:core:166601224459
my-core            v1.2.3                   test       urn:ksa:core:166601243158
smartconstruction  v1.2.2     https://core  smartcon   urn:ksa:core:166601412405  *
""".lstrip()
    )


@pytest.mark.usefixtures("active_env_core_dotfile")
def test_activate_core_already_cached(cli_runner, env_filepath):
    result = cli_runner.invoke(["env", "activate-core", "smartconstruction"])

    assert result.exit_code == 0, result.output

    config_file = """[test]
hub_api_url = "https://hub-host/api/hub"
user = "some-username"
access_token = "access-token"
refresh_token = "refresh-token"
ignore_tls = false
active = true
account = "root"
http_proxy = "null"
[test.cores.smartconstruction]
name = "smartconstruction"
host = "https://core-gateway/api/gateway"
account = "sc"
active = true
"""

    with env_filepath.open() as f:
        assert f.read() == config_file


@pytest.mark.usefixtures("active_env_dotfile")
def test_activate_core(cli_runner, httpx_mock, env_filepath):
    response_payload = {
        "cores": [
            {
                "host": None,
                "name": "local",
                "version": "v1.2.3",
                "account": "dev",
                "urn": "urn:ksa:core:166601224459",
            },
            {
                "host": None,
                "name": "my-core",
                "version": "v1.2.3",
                "account": "test",
                "urn": "urn:ksa:core:166601243158",
            },
            {
                "host": "https://core",
                "name": "smartconstruction",
                "version": "v1.2.2",
                "account": "smartcon",
                "urn": "urn:ksa:core:166601412405",
            },
        ],
    }
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/registry/core",
        json=response_payload,
    )

    result = cli_runner.invoke(["env", "activate-core", "smartconstruction"])

    assert result.exit_code == 0

    config_file = """[test]
hub_api_url = "https://hub-host/api/hub"
user = "some-username"
access_token = "access-token"
refresh_token = "refresh-token"
ignore_tls = false
active = true
account = "root"
http_proxy = "null"
[test.cores.smartconstruction]
name = "smartconstruction"
host = "https://core"
account = "smartcon"
active = true
"""

    with env_filepath.open() as f:
        assert f.read() == config_file


@pytest.mark.usefixtures("active_env_dotfile")
def test_activate_core_no_host(cli_runner, httpx_mock, env_filepath):
    response_payload = {
        "cores": [
            {
                "host": None,
                "name": "local",
                "version": "v1.2.3",
                "account": "dev",
                "urn": "urn:ksa:core:166601224459",
            },
            {
                "host": None,
                "name": "my-core",
                "version": "v1.2.3",
                "account": "test",
                "urn": "urn:ksa:core:166601243158",
            },
            {
                "host": "https://core",
                "name": "smartconstruction",
                "version": "v1.2.2",
                "account": "smartcon",
                "urn": "urn:ksa:core:166601412405",
            },
        ],
    }
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/registry/core",
        json=response_payload,
    )

    result = cli_runner.invoke(["env", "activate-core", "local"])

    assert result.exit_code == 1
    assert result.output == "Core local has no host.\n"

    config_file = """[test]
hub_api_url = "https://hub-host/api/hub"
user = "some-username"
access_token = "access-token"
refresh_token = "refresh-token"
ignore_tls = false
active = true
account = "root"

[test.cores]
"""

    with env_filepath.open() as f:
        assert f.read() == config_file


@pytest.mark.usefixtures("active_env_dotfile")
def test_activate_unknown_core(cli_runner, httpx_mock):
    response_payload = {"cores": []}

    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/registry/core",
        json=response_payload,
    )

    result = cli_runner.invoke(["env", "activate-core", "smartconstruction"])

    assert result.exit_code == 1
    assert result.output == "Core smartconstruction not found.\n"


@pytest.mark.usefixtures("active_env_dotfile")
def test_whoami(cli_runner, httpx_mock):
    response_payload = {"user_id": "uuid"}

    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/iam/user",
        json=response_payload,
    )

    result = cli_runner.invoke(["env", "whoami"])

    assert result.exit_code == 0
    assert (
        result.output
        == """{
  "user_id": "uuid"
}

"""
    )
