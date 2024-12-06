from unittest import mock

from neosctl.services.gateway import data_system
from tests.cli.services.gateway.util import get_journal_note_filepath
from tests.conftest import FakeContext

ZERO_ID = "00000000-0000-0000-0000-000000000000"
URL_PREFIX = "https://core-gateway/api/gateway/v2/data_system"


def test_data_system_list(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_system.entity, "list_entities", mocked)
    cli_runner.invoke(["gateway", "data-system", "list"])

    mocked.assert_called_once_with(ctx=FakeContext(), url=URL_PREFIX)


def test_data_system_create(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_system.entity, "create_entity", mocked)
    cli_runner.invoke(["gateway", "data-system", "create", "LBL", "name", "description"])

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


def test_data_system_get(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_system.entity, "get_entity", mocked)
    cli_runner.invoke(["gateway", "data-system", "get", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_system_delete(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_system.entity, "delete_entity", mocked)
    cli_runner.invoke(["gateway", "data-system", "delete", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_system_get_info(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_system.entity, "get_entity_info", mocked)
    cli_runner.invoke(["gateway", "data-system", "get-info", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_system_update(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_system.entity, "update_entity", mocked)
    cli_runner.invoke(
        [
            "gateway",
            "data-system",
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


def test_data_system_update_info(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_system.entity, "update_entity_info", mocked)
    cli_runner.invoke(
        [
            "gateway",
            "data-system",
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


def test_data_system_get_journal(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_system.entity, "get_entity_journal", mocked)
    cli_runner.invoke(["gateway", "data-system", "get-journal", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        page=1,
        per_page=25,
    )


def test_data_system_update_journal(cli_runner, monkeypatch, tmp_path):
    filepath = get_journal_note_filepath(tmp_path)

    mocked = mock.Mock()
    monkeypatch.setattr(data_system.entity, "update_entity_journal", mocked)
    cli_runner.invoke(["gateway", "data-system", "update-journal", ZERO_ID, filepath])
    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        filepath=filepath,
    )


def test_data_system_get_links(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_system.entity, "get_entity_links", mocked)
    cli_runner.invoke(["gateway", "data-system", "get-links", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )
