from unittest import mock

from neosctl.services.gateway import output
from tests.cli.services.gateway.util import get_journal_note_filepath
from tests.conftest import FakeContext
from tests.helper import render_cmd_output

ZERO_ID = "00000000-0000-0000-0000-000000000000"
URL_PREFIX = "https://core-gateway/api/gateway/v2/output"


def test_output_list(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(output.entity, "list_entities", mocked)
    cli_runner.invoke(["gateway", "output", "list"])

    mocked.assert_called_once_with(ctx=FakeContext(), url=URL_PREFIX)


def test_output_create(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(output.entity, "create_entity", mocked)
    cli_runner.invoke(["gateway", "output", "create", "LBL", "name", "description", "application"])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        label="LBL",
        name="name",
        description="description",
        owner=None,
        contacts=[],
        links=[],
        entity_schema=output.schema.CreateOutput(
            name="name",
            label="LBL",
            description="description",
            output_type="application",
        ),
    )


def test_create_entity_real_test(cli_runner, httpx_mock):
    response_payload = {
        "description": "description",
        "identifier": "d953d89c-f85c-4a78-8f62-7161b07431e7",
        "label": "LBL",
        "name": "name",
        "urn": "urn:ksa:core:168415628435:root:data_product:d953d89c-f85c-4a78-8f62-7161b07431e7",
        "output_type": "application",
    }
    httpx_mock.add_response(
        method="POST",
        url=URL_PREFIX,
        json=response_payload,
    )

    result = cli_runner.invoke(["gateway", "output", "create", "LBL", "name", "description", "application"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_output_get(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(output.entity, "get_entity", mocked)
    cli_runner.invoke(["gateway", "output", "get", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_output_delete(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(output.entity, "delete_entity", mocked)
    cli_runner.invoke(["gateway", "output", "delete", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_output_get_info(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(output.entity, "get_entity_info", mocked)
    cli_runner.invoke(["gateway", "output", "get-info", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_output_update(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(output.entity, "update_entity", mocked)
    cli_runner.invoke(
        [
            "gateway",
            "output",
            "update",
            ZERO_ID,
            "AAA",
            "new name",
            "new description",
            "application",
        ],
    )

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        label="AAA",
        name="new name",
        description="new description",
        entity_schema=output.schema.CreateOutput(
            name="new name",
            label="AAA",
            description="new description",
            output_type="application",
        ),
    )


def test_update_entity_real_test(cli_runner, httpx_mock):
    response_payload = {
        "description": "description",
        "identifier": ZERO_ID,
        "label": "LBL",
        "name": "name",
        "urn": f"urn:ksa:core:168415628435:root:data_product:{ZERO_ID}",
        "output_type": "application",
    }
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_PREFIX}/{ZERO_ID}",
        json=response_payload,
    )

    result = cli_runner.invoke(["gateway", "output", "update", ZERO_ID, "LBL", "name", "description", "application"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_output_update_info(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(output.entity, "update_entity_info", mocked)
    cli_runner.invoke(
        [
            "gateway",
            "output",
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


def test_output_get_journal(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(output.entity, "get_entity_journal", mocked)
    cli_runner.invoke(["gateway", "output", "get-journal", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        page=1,
        per_page=25,
    )


def test_output_update_journal(cli_runner, monkeypatch, tmp_path):
    filepath = get_journal_note_filepath(tmp_path)

    mocked = mock.Mock()
    monkeypatch.setattr(output.entity, "update_entity_journal", mocked)
    cli_runner.invoke(["gateway", "output", "update-journal", ZERO_ID, filepath])
    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        filepath=filepath,
    )


def test_output_get_links(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(output.entity, "get_entity_links", mocked)
    cli_runner.invoke(["gateway", "output", "get-links", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )
