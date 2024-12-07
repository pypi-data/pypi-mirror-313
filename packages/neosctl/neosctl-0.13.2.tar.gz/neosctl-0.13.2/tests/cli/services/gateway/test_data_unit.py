import json
from unittest import mock

from neosctl.services.gateway import data_unit, schema
from tests.cli.services.gateway.util import get_journal_note_filepath
from tests.conftest import FakeContext
from tests.helper import render_cmd_output

ZERO_ID = "00000000-0000-0000-0000-000000000000"
URL_PREFIX = "https://core-gateway/api/gateway/v2/data_unit"
URL_IDENTIFIED_PREFIX = f"https://core-gateway/api/gateway/v2/data_unit/{ZERO_ID}"


def test_data_unit_list(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_unit.entity, "list_entities", mocked)
    cli_runner.invoke(["gateway", "data-unit", "list"])

    mocked.assert_called_once_with(ctx=FakeContext(), url=URL_PREFIX)


def test_data_unit_create(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_unit.entity, "create_entity", mocked)
    cli_runner.invoke(["gateway", "data-unit", "create", "LBL", "name", "description"])

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


def test_data_unit_get(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_unit.entity, "get_entity", mocked)
    cli_runner.invoke(["gateway", "data-unit", "get", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_unit_delete(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_unit.entity, "delete_entity", mocked)
    cli_runner.invoke(["gateway", "data-unit", "delete", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_unit_get_info(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_unit.entity, "get_entity_info", mocked)
    cli_runner.invoke(["gateway", "data-unit", "get-info", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_unit_update(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_unit.entity, "update_entity", mocked)
    cli_runner.invoke(
        [
            "gateway",
            "data-unit",
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


def test_data_unit_update_info(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_unit.entity, "update_entity_info", mocked)
    cli_runner.invoke(
        [
            "gateway",
            "data-unit",
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


def test_data_unit_get_journal(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_unit.entity, "get_entity_journal", mocked)
    cli_runner.invoke(["gateway", "data-unit", "get-journal", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        page=1,
        per_page=25,
    )


def test_data_unit_update_journal(cli_runner, monkeypatch, tmp_path):
    filepath = get_journal_note_filepath(tmp_path)

    mocked = mock.Mock()
    monkeypatch.setattr(data_unit.entity, "update_entity_journal", mocked)
    cli_runner.invoke(["gateway", "data-unit", "update-journal", ZERO_ID, filepath])
    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        filepath=filepath,
    )


def test_data_unit_get_links(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_unit.entity, "get_entity_links", mocked)
    cli_runner.invoke(["gateway", "data-unit", "get-links", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_unit_update_metadata(cli_runner, httpx_mock, tmp_path):
    response_payload = {}
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/metadata",
        json=response_payload,
    )

    fp = tmp_path / "metadata_update.json"
    with fp.open("w") as f:
        json.dump(
            schema.UpdateEntityMetadataRequest(
                tags=["top-secret"],
                fields={
                    "field": schema.FieldMetadata(tags=["secret"], description=None),
                },
            ).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-unit",
            "update-metadata",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_unit_delete_metadata(cli_runner, httpx_mock, tmp_path):
    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url=f"{URL_IDENTIFIED_PREFIX}/metadata",
        json=response_payload,
    )

    fp = tmp_path / "metadata_update.json"
    with fp.open("w") as f:
        json.dump(
            schema.DeleteEntityMetadataRequest(
                tags=["top-secret"],
                fields={
                    "field": schema.FieldMetadata(tags=["secret"], description=None),
                },
            ).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-unit",
            "delete-metadata",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_unit_get_schema(cli_runner, httpx_mock):
    response_payload = {"fields": []}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/schema",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-unit",
            "get-schema",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_unit_get_config(cli_runner, httpx_mock):
    response_payload = {"configuration": None}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/config",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-unit",
            "get-config",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_unit_update_config(cli_runner, httpx_mock, tmp_path):
    response_payload = {"configuration": None}
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/config",
        json=response_payload,
    )

    fp = tmp_path / "update_config.json"
    with fp.open("w") as f:
        json.dump(
            schema.UpdateDataUnitConfiguration(configuration={}).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-unit",
            "update-config",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)
