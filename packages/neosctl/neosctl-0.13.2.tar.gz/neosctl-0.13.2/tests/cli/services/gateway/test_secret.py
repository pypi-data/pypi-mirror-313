import json

from neosctl.services.gateway import schema
from tests.helper import render_cmd_output

ZERO_ID = "00000000-0000-0000-0000-000000000000"
URL_PREFIX = "https://core-gateway/api/gateway/v2/secret"
URL_IDENTIFIED_PREFIX = f"https://core-gateway/api/gateway/v2/secret/{ZERO_ID}"


def test_secret_list(cli_runner, httpx_mock):
    response_payload = {"secrets": []}
    httpx_mock.add_response(
        method="GET",
        url=URL_PREFIX,
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "secret", "list"],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_secret_create(cli_runner, httpx_mock, tmp_path):
    response_payload = {
        "identifier": ZERO_ID,
        "keys": ["a"],
        "name": "aaa",
        "urn": f"urn:ksa:core:168415628435:root:secret:{ZERO_ID}",
    }
    httpx_mock.add_response(
        method="POST",
        url=URL_PREFIX,
        json=response_payload,
    )

    fp = tmp_path / "secret.json"
    with fp.open("w") as f:
        json.dump(
            schema.UpdateSecret(name="aaa", data={"a": "b"}).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "secret",
            "create",
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_secret_update(cli_runner, httpx_mock, tmp_path):
    response_payload = {
        "identifier": ZERO_ID,
        "keys": ["a"],
        "name": "aaa",
        "urn": f"urn:ksa:core:168415628435:root:secret:{ZERO_ID}",
    }
    httpx_mock.add_response(
        method="PUT",
        url=URL_IDENTIFIED_PREFIX,
        json=response_payload,
    )

    fp = tmp_path / "secret.json"
    with fp.open("w") as f:
        json.dump(
            schema.UpdateSecret(name="aaa", data={"a": "b"}).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "secret",
            "update",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_secret_get(cli_runner, httpx_mock):
    response_payload = {
        "identifier": ZERO_ID,
        "keys": ["a"],
        "name": "aaa",
        "urn": f"urn:ksa:core:168415628435:root:secret:{ZERO_ID}",
    }
    httpx_mock.add_response(
        method="GET",
        url=URL_IDENTIFIED_PREFIX,
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "secret",
            "get",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_secret_delete(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url=URL_IDENTIFIED_PREFIX,
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "secret",
            "delete",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_secret_delete_keys(cli_runner, httpx_mock, tmp_path):
    response_payload = {
        "identifier": ZERO_ID,
        "keys": ["a"],
        "name": "aaa",
        "urn": f"urn:ksa:core:168415628435:root:secret:{ZERO_ID}",
    }
    httpx_mock.add_response(
        method="DELETE",
        url=f"{URL_IDENTIFIED_PREFIX}/keys",
        json=response_payload,
    )

    fp = tmp_path / "keys.json"
    with fp.open("w") as f:
        json.dump(
            schema.SecretKeys(keys=["b"]).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "secret",
            "delete-keys",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)
