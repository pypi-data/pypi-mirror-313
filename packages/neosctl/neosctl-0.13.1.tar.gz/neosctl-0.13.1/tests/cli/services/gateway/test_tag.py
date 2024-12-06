import pytest

from tests.helper import render_cmd_output

URL_PREFIX = "https://core-gateway/api/gateway/v2/tag"


@pytest.mark.parametrize(
    ("args", "suffix"),
    [
        (["gateway", "tag", "list", "FIELD"], "scope=FIELD&system_defined=false&tag_filter="),
        (["gateway", "tag", "list", "FIELD", "-s"], "scope=FIELD&system_defined=true&tag_filter="),
        (["gateway", "tag", "list", "FIELD", "--filter", "abc"], "scope=FIELD&system_defined=false&tag_filter=abc"),
        (
            ["gateway", "tag", "list", "FIELD", "-s", "--filter", "abc"],
            "scope=FIELD&system_defined=true&tag_filter=abc",
        ),
        (["gateway", "tag", "list", "SCHEMA"], "scope=SCHEMA&system_defined=false&tag_filter="),
        (["gateway", "tag", "list", "SCHEMA", "-s"], "scope=SCHEMA&system_defined=true&tag_filter="),
        (["gateway", "tag", "list", "SCHEMA", "--filter", "abc"], "scope=SCHEMA&system_defined=false&tag_filter=abc"),
        (
            ["gateway", "tag", "list", "SCHEMA", "-s", "--filter", "abc"],
            "scope=SCHEMA&system_defined=true&tag_filter=abc",
        ),
    ],
)
def test_tag_list(cli_runner, httpx_mock, args, suffix):
    response_payload = {"tag": []}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_PREFIX}?{suffix}",
        json=response_payload,
    )

    result = cli_runner.invoke(args)

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_tag_create(cli_runner, httpx_mock):
    response_payload = {
        "scope": "FIELD",
        "system_defined": False,
        "tag": "a tag",
        "tag_type": "CLASSIFICATION",
    }
    httpx_mock.add_response(
        method="POST",
        url=URL_PREFIX,
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "tag", "create", "a tag", "FIELD"],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_tag_delete(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url=URL_PREFIX,
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "tag", "delete", "a tag", "FIELD"],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)
