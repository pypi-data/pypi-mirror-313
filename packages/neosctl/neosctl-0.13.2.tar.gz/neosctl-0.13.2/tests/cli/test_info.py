import pytest

from tests.helper import render_cmd_output


@pytest.fixture(autouse=True)
def _active_env_core(active_env_core_dotfile):
    pass


def test_permissions_hub(cli_runner, httpx_mock):
    response_payload = {
        "routes": [],
    }
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/__neos/permissions",
        json=response_payload,
    )
    args = ["-s", "hub"]
    result = cli_runner.invoke(
        ["info", "permissions", *args],
    )

    assert result.exit_code == 0, result.output
    assert result.output == render_cmd_output(response_payload["routes"])


def test_permissions_core(cli_runner, httpx_mock):
    response_payload = {
        "routes": [],
    }
    httpx_mock.add_response(
        method="GET",
        url="https://core-gateway/api/gateway/__neos/permissions",
        json=response_payload,
    )
    args = ["-s", "core"]
    result = cli_runner.invoke(
        ["info", "permissions", *args],
    )

    assert result.exit_code == 0, result.output
    assert result.output == render_cmd_output(response_payload["routes"])


def test_error_codes_hub(cli_runner, httpx_mock):
    response_payload = {
        "errors": [],
    }
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/__neos/error_codes",
        json=response_payload,
    )
    args = ["-s", "hub"]
    result = cli_runner.invoke(
        ["info", "error-codes", *args],
    )

    assert result.exit_code == 0, result.output
    assert result.output == render_cmd_output(response_payload["errors"])


def test_error_codes_core(cli_runner, httpx_mock):
    response_payload = {
        "errors": [],
    }
    httpx_mock.add_response(
        method="GET",
        url="https://core-gateway/api/gateway/__neos/error_codes",
        json=response_payload,
    )
    args = ["-s", "core"]
    result = cli_runner.invoke(
        ["info", "error-codes", *args],
    )

    assert result.exit_code == 0, result.output
    assert result.output == render_cmd_output(response_payload["errors"])


def test_version_hub(cli_runner, httpx_mock):
    response_payload = {
        "timestamp": "xxx",
        "version": "v1.2.3",
    }
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/__neos/status",
        json=response_payload,
    )
    args = ["-s", "hub"]
    result = cli_runner.invoke(
        ["info", "version", *args],
    )

    assert result.exit_code == 0, result.output
    assert result.output == render_cmd_output(response_payload)


def test_version_core(cli_runner, httpx_mock):
    response_payload = {
        "timestamp": "xxx",
        "version": "v1.2.3",
    }
    httpx_mock.add_response(
        method="GET",
        url="https://core-gateway/api/gateway/__neos/status",
        json=response_payload,
    )
    args = ["-s", "core"]
    result = cli_runner.invoke(
        ["info", "version", *args],
    )

    assert result.exit_code == 0, result.output
    assert result.output == render_cmd_output(response_payload)


def test_version_storage(cli_runner, httpx_mock):
    response_payload = {
        "timestamp": "xxx",
        "version": "v1.2.3",
    }
    httpx_mock.add_response(
        method="GET",
        url="https://saas.core-gateway/__neos/status",
        json=response_payload,
    )
    args = ["-s", "storage"]
    result = cli_runner.invoke(
        ["info", "version", *args],
    )

    assert result.exit_code == 0, result.output
    assert result.output == render_cmd_output(response_payload)
