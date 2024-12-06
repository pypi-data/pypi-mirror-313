import json
from unittest import mock

from neosctl.services.gateway import data_source, schema
from tests.cli.services.gateway.util import get_journal_note_filepath
from tests.conftest import FakeContext
from tests.helper import render_cmd_output

ZERO_ID = "00000000-0000-0000-0000-000000000000"
URL_PREFIX = "https://core-gateway/api/gateway/v2/data_source"
URL_IDENTIFIED_PREFIX = f"https://core-gateway/api/gateway/v2/data_source/{ZERO_ID}"


def test_data_source_list(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_source.entity, "list_entities", mocked)
    cli_runner.invoke(["gateway", "data-source", "list"])

    mocked.assert_called_once_with(ctx=FakeContext(), url=URL_PREFIX)


def test_data_source_create(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_source.entity, "create_entity", mocked)
    cli_runner.invoke(["gateway", "data-source", "create", "LBL", "name", "description"])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        label="LBL",
        name="name",
        description="description",
        owner=None,
        contacts=[],
        links=[],
    )


def test_data_source_get(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_source.entity, "get_entity", mocked)
    cli_runner.invoke(["gateway", "data-source", "get", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_source_delete(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_source.entity, "delete_entity", mocked)
    cli_runner.invoke(["gateway", "data-source", "delete", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_source_get_info(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_source.entity, "get_entity_info", mocked)
    cli_runner.invoke(["gateway", "data-source", "get-info", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_source_update(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_source.entity, "update_entity", mocked)
    cli_runner.invoke(
        [
            "gateway",
            "data-source",
            "update",
            ZERO_ID,
            "AAA",
            "new name",
            "new description",
        ],
    )

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        label="AAA",
        name="new name",
        description="new description",
    )


def test_data_source_update_info(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_source.entity, "update_entity_info", mocked)
    cli_runner.invoke(
        [
            "gateway",
            "data-source",
            "update-info",
            ZERO_ID,
            "--owner",
            "owner",
            "-l",
            "link 1",
            "-l",
            "link 2",
            "-c",
            "contact",
        ],
    )

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        contacts=["contact"],
        links=["link 1", "link 2"],
        owner="owner",
    )


def test_data_source_get_journal(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_source.entity, "get_entity_journal", mocked)
    cli_runner.invoke(["gateway", "data-source", "get-journal", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        page=1,
        per_page=25,
    )


def test_data_source_update_journal(cli_runner, monkeypatch, tmp_path):
    filepath = get_journal_note_filepath(tmp_path)

    mocked = mock.Mock()
    monkeypatch.setattr(data_source.entity, "update_entity_journal", mocked)
    cli_runner.invoke(["gateway", "data-source", "update-journal", ZERO_ID, filepath])
    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        filepath=filepath,
    )


def test_data_source_get_links(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_source.entity, "get_entity_links", mocked)
    cli_runner.invoke(["gateway", "data-source", "get-links", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_source_get_connection(cli_runner, httpx_mock):
    response_payload = {"connection": None, "secret_identifier": None}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/connection",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-source",
            "get-connection",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_source_update_connection(cli_runner, httpx_mock, tmp_path):
    response_payload = {"connection": None}
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/connection",
        json=response_payload,
    )

    fp = tmp_path / "update_connection.json"
    with fp.open("w") as f:
        json.dump(
            schema.UpdateDataSourceConnection(connection={}).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-source",
            "update-connection",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_source_update_connection_secrets(cli_runner, httpx_mock, tmp_path):
    response_payload = {"connection": None}
    httpx_mock.add_response(
        method="POST",
        url=f"{URL_IDENTIFIED_PREFIX}/secret",
        json=response_payload,
    )

    fp = tmp_path / "update_connection_secrets.json"
    with fp.open("w") as f:
        json.dump(
            schema.UpdateDataSourceConnectionSecret(secrets={}).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-source",
            "set-connection-secrets",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)
