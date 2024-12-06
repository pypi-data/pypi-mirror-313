from tests.cli.services.gateway.util import get_journal_note_filepath
from tests.helper import render_cmd_output

ZERO_ID = "00000000-0000-0000-0000-000000000000"
URL_IDENTIFIED_PREFIX = f"https://core-gateway/api/gateway/v2/journal_note/{ZERO_ID}"


def test_journal_note_update(cli_runner, httpx_mock, tmp_path):
    response_payload = {
        "identifier": ZERO_ID,
        "name": "aaa",
        "urn": f"urn:ksa:core:168415628435:root:journal_note:{ZERO_ID}",
        "note": "a note",
        "owner": "owner",
    }
    httpx_mock.add_response(
        method="PUT",
        url=URL_IDENTIFIED_PREFIX,
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "journal-note",
            "update",
            ZERO_ID,
            get_journal_note_filepath(tmp_path),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_journal_note_get(cli_runner, httpx_mock):
    response_payload = {
        "identifier": ZERO_ID,
        "name": "aaa",
        "urn": f"urn:ksa:core:168415628435:root:journal_note:{ZERO_ID}",
        "note": "a note",
        "owner": "owner",
    }
    httpx_mock.add_response(
        method="GET",
        url=URL_IDENTIFIED_PREFIX,
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "journal-note",
            "get",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_journal_note_delete(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url=URL_IDENTIFIED_PREFIX,
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "journal-note",
            "delete",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)
