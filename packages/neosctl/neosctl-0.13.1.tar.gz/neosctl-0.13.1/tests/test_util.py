# TODO: Write explicit tests for util functions. Don't rely on usage in other tests.
import json
from textwrap import dedent
from unittest import mock

import httpx
import pytest
import typer

from neosctl import schema, util
from tests.helper import render_cmd_output

GATEWAY_URL = "https://core-gateway/api/gateway"
IAM_URL = "https://hub-host/api/hub/iam"
REFRESH_URL = f"{IAM_URL}/refresh"


def test_dumps_formatted_json_dict_unsorted():
    assert (
        util.dumps_formatted_json({"f": "a", "a": "b", "c": "c"}, sort_keys=False)
        == dedent("""
    {
      "f": "a",
      "a": "b",
      "c": "c"
    }""").lstrip()
    )


def test_dumps_formatted_json_dict_sorted():
    assert (
        util.dumps_formatted_json({"f": "a", "a": "b", "c": "c"}, sort_keys=True)
        == dedent("""
    {
      "a": "b",
      "c": "c",
      "f": "a"
    }""").lstrip()
    )


def test_dumps_formatted_json_list_unsorted():
    assert (
        util.dumps_formatted_json([{"f": "a"}, {"a": "b"}, {"c": "c"}], sort_keys=False)
        == dedent("""
    [
      {
        "f": "a"
      },
      {
        "a": "b"
      },
      {
        "c": "c"
      }
    ]""").lstrip()
    )


def test_dumps_formatted_json_list_sorted():
    assert (
        util.dumps_formatted_json([{"f": "a"}, {"a": "b"}, {"c": "c"}], sort_keys=True)
        == dedent("""
    [
      {
        "f": "a"
      },
      {
        "a": "b"
      },
      {
        "c": "c"
      }
    ]""").lstrip()
    )


def test_prettify_json():
    assert (
        util.prettify_json({"f": "a", "a": "b", "c": "c"})
        == dedent("""
    {\x1b[37m\x1b[39;49;00m
    \x1b[37m  \x1b[39;49;00m\x1b[94m"a"\x1b[39;49;00m:\x1b[37m \x1b[39;49;00m\x1b[33m"b"\x1b[39;49;00m,\x1b[37m\x1b[39;49;00m
    \x1b[37m  \x1b[39;49;00m\x1b[94m"c"\x1b[39;49;00m:\x1b[37m \x1b[39;49;00m\x1b[33m"c"\x1b[39;49;00m,\x1b[37m\x1b[39;49;00m
    \x1b[37m  \x1b[39;49;00m\x1b[94m"f"\x1b[39;49;00m:\x1b[37m \x1b[39;49;00m\x1b[33m"a"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
    }\x1b[37m\x1b[39;49;00m\n""").lstrip()  # noqa: E501
    )


def test_prettify_json_no_sort():
    assert (
        util.prettify_json({"f": "a", "a": "b", "c": "c"}, sort_keys=False)
        == dedent("""
    {\x1b[37m\x1b[39;49;00m
    \x1b[37m  \x1b[39;49;00m\x1b[94m"f"\x1b[39;49;00m:\x1b[37m \x1b[39;49;00m\x1b[33m"a"\x1b[39;49;00m,\x1b[37m\x1b[39;49;00m
    \x1b[37m  \x1b[39;49;00m\x1b[94m"a"\x1b[39;49;00m:\x1b[37m \x1b[39;49;00m\x1b[33m"b"\x1b[39;49;00m,\x1b[37m\x1b[39;49;00m
    \x1b[37m  \x1b[39;49;00m\x1b[94m"c"\x1b[39;49;00m:\x1b[37m \x1b[39;49;00m\x1b[33m"c"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
    }\x1b[37m\x1b[39;49;00m\n""").lstrip()  # noqa: E501
    )


@pytest.mark.usefixtures("env_dotfile")
def test_get_env_section(monkeypatch):
    env = util.read_env_dotfile()
    monkeypatch.setattr(util.typer, "echo", mock.Mock())

    e = util.get_env_section(env, "test")

    assert e == schema.Env(
        name="test",
        user="some-username",
        access_token="",
        refresh_token="",
        ignore_tls=False,
        active=False,
        account="root",
        hub_api_url="https://hub-host/api/hub",
        cores={},
    )


def test_get_env_section_unknown_env(monkeypatch):
    monkeypatch.setattr(util.typer, "echo", mock.Mock())
    with pytest.raises(typer.Exit) as e:
        util.get_env_section({}, "any")

    assert e.value.exit_code == 1
    assert util.typer.echo.call_args == mock.call("Environment any not found.")


def test_get_active_env_none_active():
    envs = {
        "test": {
            "access_token": "",
            "account": "root",
            "active": False,
            "hub_api_url": "https://hub",
            "ignore_tls": False,
            "refresh_token": "",
            "user": "some-username",
            "cores": {},
        },
        "test2": {
            "access_token": "",
            "account": "root",
            "active": False,
            "hub_api_url": "https://hub2",
            "ignore_tls": False,
            "refresh_token": "",
            "user": "some-username2",
            "cores": {},
        },
    }

    assert util.get_active_env(envs, None) is None


def test_get_active_env():
    envs = {
        "test": {
            "access_token": "",
            "account": "root",
            "active": True,
            "hub_api_url": "https://hub",
            "ignore_tls": False,
            "refresh_token": "",
            "user": "some-username",
            "cores": {},
        },
        "test2": {
            "access_token": "",
            "account": "root",
            "active": False,
            "hub_api_url": "https://hub2",
            "ignore_tls": False,
            "refresh_token": "",
            "user": "some-username2",
            "cores": {},
        },
    }

    assert util.get_active_env(envs, None) == schema.Env(
        name="test",
        user="some-username",
        access_token="",
        refresh_token="",
        ignore_tls=False,
        active=True,
        account="root",
        hub_api_url="https://hub",
        cores={},
    )


def test_get_active_env_override():
    envs = {
        "test": {
            "access_token": "",
            "account": "root",
            "active": True,
            "hub_api_url": "https://hub",
            "ignore_tls": False,
            "refresh_token": "",
            "user": "some-username",
            "cores": {},
        },
        "test2": {
            "access_token": "",
            "account": "root",
            "active": False,
            "hub_api_url": "https://hub2",
            "ignore_tls": False,
            "refresh_token": "",
            "user": "some-username2",
            "cores": {},
        },
    }

    assert util.get_active_env(envs, "test2") == schema.Env(
        name="test2",
        user="some-username2",
        access_token="",
        refresh_token="",
        ignore_tls=False,
        active=False,
        account="root",
        hub_api_url="https://hub2",
        cores={},
    )


def test_get_active_env_not_found(monkeypatch):
    monkeypatch.setattr(util.typer, "echo", mock.Mock())
    envs = {
        "test": {
            "access_token": "",
            "account": "root",
            "active": True,
            "hub_api_url": "https://hub",
            "ignore_tls": False,
            "refresh_token": "",
            "user": "some-username",
            "cores": {},
        },
        "test2": {
            "access_token": "",
            "account": "root",
            "active": False,
            "hub_api_url": "https://hub2",
            "ignore_tls": False,
            "refresh_token": "",
            "user": "some-username2",
            "cores": {},
        },
    }

    with pytest.raises(typer.Exit):
        util.get_active_env(envs, "test3")

    assert util.typer.echo.call_args == mock.call("Environment test3 not found.")


def test_get_active_core_no_active_env():
    assert util.get_active_core(None, None) is None


def test_get_active_core_no_active_core():
    env = schema.Env(
        name="test",
        user="some-username",
        access_token="",
        refresh_token="",
        ignore_tls=False,
        active=True,
        account="root",
        hub_api_url="https://hub",
        cores={
            "test": schema.Core(name="test", host="host", account="test", active=False),
            "test2": schema.Core(name="test2", host="host", account="test", active=False),
        },
    )
    assert util.get_active_core(env, None) is None


def test_get_active_core():
    env = schema.Env(
        name="test",
        user="some-username",
        access_token="",
        refresh_token="",
        ignore_tls=False,
        active=True,
        account="root",
        hub_api_url="https://hub",
        cores={
            "test": schema.Core(name="test", host="host", account="test", active=False),
            "test2": schema.Core(name="test2", host="host", account="test", active=True),
        },
    )
    assert util.get_active_core(env, None) == schema.Core(name="test2", host="host", account="test", active=True)


def test_get_active_core_override():
    env = schema.Env(
        name="test",
        user="some-username",
        access_token="",
        refresh_token="",
        ignore_tls=False,
        active=True,
        account="root",
        hub_api_url="https://hub",
        cores={
            "test": schema.Core(name="test", host="host", account="test", active=False),
            "test2": schema.Core(name="test2", host="host", account="test", active=True),
        },
    )
    assert util.get_active_core(env, "test") == schema.Core(name="test", host="host", account="test", active=False)


def test_get_active_core_override_not_found(monkeypatch):
    monkeypatch.setattr(util.typer, "echo", mock.Mock())
    env = schema.Env(
        name="test",
        user="some-username",
        access_token="",
        refresh_token="",
        ignore_tls=False,
        active=True,
        account="root",
        hub_api_url="https://hub",
        cores={
            "test": schema.Core(name="test", host="host", account="test", active=False),
            "test2": schema.Core(name="test2", host="host", account="test", active=True),
        },
    )
    with pytest.raises(typer.Exit):
        util.get_active_core(env, "test3")
    assert util.typer.echo.call_args == mock.call("Core test3 not found!")


def test_sanitize():
    assert util.sanitize(mock.Mock(), mock.Mock(), value="some value \r\n") == "some value "


@pytest.mark.parametrize(
    ("code", "result"),
    [
        (200, True),
        (299, True),
        (300, False),
        (199, False),
    ],
)
def test_is_success_response_(code, result):
    assert util.is_success_response(httpx.Response(code)) is result


def test_exit_with_output():
    exit_code = 25
    r = util.exit_with_output("I'm tired", exit_code)
    assert r.exit_code == exit_code


def test_bearer_success(monkeypatch):
    mocked = mock.Mock()
    mocked.obj.access_token = "abracadabra"
    monkeypatch.setattr(util.click, "Context", mocked)

    assert util.bearer(mocked) == {"Authorization": "Bearer abracadabra"}


def test_bearer_failure(monkeypatch):
    mocked = mock.Mock()
    mocked.obj.access_token = ""
    monkeypatch.setattr(util.click, "Context", mocked)

    assert util.bearer(mocked) is None


def test_ensure_login_bad_context():
    def inner(number: int) -> httpx.Response:
        return httpx.Response(status_code=number)

    with pytest.raises(TypeError):
        util.ensure_login(inner)(0)


def test_request(monkeypatch):
    mocked_ctx = mock.Mock()
    mocked_ctx.obj.access_token = "token"
    mocked_ctx.obj.ignore_tls = True
    mocked_ctx.obj.account = "root"
    mocked = mock.Mock()

    monkeypatch.setattr(util.NeosClient, "request", mocked)
    monkeypatch.setattr(util, "get_user_credential", mock.Mock(return_value=None))
    util._request(mocked_ctx, "GET", "service", "url", timeout=1)

    mocked.assert_called_once_with(
        "url",
        util.Method.GET,
        verify=False,
        params={},
        headers={"X-Account": "root", "X-Partition": "ksa"},
        timeout=1,
    )


def test_request_with_account_override(monkeypatch):
    mocked_ctx = mock.Mock()
    mocked_ctx.obj.access_token = "token"
    mocked_ctx.obj.ignore_tls = True
    mocked_ctx.obj.account = "root"
    mocked = mock.Mock()

    monkeypatch.setattr(util.NeosClient, "request", mocked)
    monkeypatch.setattr(util, "get_user_credential", mock.Mock(return_value=None))
    util._request(mocked_ctx, "GET", "service", "url", timeout=1, account="test")

    mocked.assert_called_once_with(
        "url",
        util.Method.GET,
        verify=False,
        params={},
        headers={"X-Account": "root", "X-Partition": "ksa", "X-Account-Override": "test"},
        timeout=1,
    )


def test_process_response_handles_invalid_response_content(monkeypatch):
    monkeypatch.setattr(util.logger, "info", mock.Mock())
    monkeypatch.setattr(util.logger, "exception", mock.Mock())
    monkeypatch.setattr(util.typer, "echo", mock.Mock())

    mock_response = mock.Mock()
    mock_response.json.side_effect = Exception
    mock_response.content = "invalid-content"

    with pytest.raises(typer.Exit) as e:
        util.process_response(mock_response)

    assert util.logger.info.call_args == mock.call("invalid-content")
    assert util.logger.exception.call_args == mock.call("Failure to parse response.")

    assert e.value.exit_code == 1
    assert util.typer.echo.call_args == mock.call(
        "Unable to parse response.",
    )


def test_process_response_handles_bad_request(monkeypatch):
    monkeypatch.setattr(util.typer, "echo", mock.Mock())
    monkeypatch.setattr(util, "prettify_json", json.dumps)

    mock_response = mock.Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"bad": "request"}

    with pytest.raises(typer.Exit) as e:
        util.process_response(mock_response)

    assert e.value.exit_code == 1
    assert util.typer.echo.call_args == mock.call(
        '{"bad": "request"}',
    )


def test_process_response_uses_provided_callable(monkeypatch):
    monkeypatch.setattr(util.typer, "echo", mock.Mock())

    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"good": "request"}

    with pytest.raises(typer.Exit) as e:
        util.process_response(mock_response, render_callable=json.dumps)

    assert e.value.exit_code == 0
    assert util.typer.echo.call_args == mock.call(
        '{"good": "request"}',
    )


@pytest.mark.parametrize(
    ("output_format", "expected"),
    [
        ("json", '{\n  "good": "request"\n}'),
        ("toml", "good = 'request'\n"),
        ("text", "good  request"),
        ("yaml", "---\ngood: request\n"),
    ],
)
def test_process_response_output_format(monkeypatch, output_format, expected):
    def mock_highlight(content, *args):  # noqa: ARG001
        return content

    monkeypatch.setattr(util, "highlight", mock_highlight)
    monkeypatch.setattr(util.typer, "echo", mock.Mock())

    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"good": "request"}

    with pytest.raises(typer.Exit) as e:
        util.process_response(mock_response, output_format=output_format)

    assert e.value.exit_code == 0
    assert util.typer.echo.call_args == mock.call(expected)


@pytest.mark.parametrize(
    ("output_format", "expected"),
    [
        ("json", '[\n  {\n    "good": "request"\n  }\n]'),
        ("toml", "[[]]\ngood = 'request'\n"),
        ("text", "Good\n-------\nrequest"),
        ("yaml", "---\n- good: request\n"),
    ],
)
def test_process_response_output_format_list(monkeypatch, output_format, expected):
    def mock_highlight(content, *args):  # noqa: ARG001
        return content

    monkeypatch.setattr(util, "highlight", mock_highlight)
    monkeypatch.setattr(util.typer, "echo", mock.Mock())

    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"good": "request"}]

    with pytest.raises(typer.Exit) as e:
        util.process_response(mock_response, output_format=output_format)

    assert e.value.exit_code == 0
    assert util.typer.echo.call_args == mock.call(expected)


def test_process_response_fields(monkeypatch):
    def mock_highlight(content, *args):  # noqa: ARG001
        return content

    monkeypatch.setattr(util, "highlight", mock_highlight)
    monkeypatch.setattr(util.typer, "echo", mock.Mock())

    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"good": "request", "better": "value", "best": "woo"}

    with pytest.raises(typer.Exit) as e:
        util.process_response(mock_response, fields=["good", "better"], sort_keys=False)

    assert e.value.exit_code == 0
    assert util.typer.echo.call_args == mock.call('{\n  "good": "request",\n  "better": "value"\n}')


def test_process_response_fields_list(monkeypatch):
    def mock_highlight(content, *args):  # noqa: ARG001
        return content

    monkeypatch.setattr(util, "highlight", mock_highlight)
    monkeypatch.setattr(util.typer, "echo", mock.Mock())

    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"good": "request", "better": "value", "best": "woo"}]

    with pytest.raises(typer.Exit) as e:
        util.process_response(mock_response, fields=["good", "better"], sort_keys=False)

    assert e.value.exit_code == 0
    assert util.typer.echo.call_args == mock.call('[\n  {\n    "good": "request",\n    "better": "value"\n  }\n]')


def test_process_payload(monkeypatch):
    def mock_highlight(content, *args):  # noqa: ARG001
        return content

    monkeypatch.setattr(util, "highlight", mock_highlight)

    payload = {"good": "request", "better": "value", "best": "woo"}

    r = util.process_payload(payload, sort_keys=False)
    assert r == '{\n  "good": "request",\n  "better": "value",\n  "best": "woo"\n}'


def test_process_payload_fields(monkeypatch):
    def mock_highlight(content, *args):  # noqa: ARG001
        return content

    monkeypatch.setattr(util, "highlight", mock_highlight)

    payload = {"good": "request", "better": "value", "best": "woo"}

    r = util.process_payload(payload, sort_keys=False, fields=["good", "better"])
    assert r == '{\n  "good": "request",\n  "better": "value"\n}'


def test_process_payload_fields_list(monkeypatch):
    def mock_highlight(content, *args):  # noqa: ARG001
        return content

    monkeypatch.setattr(util, "highlight", mock_highlight)

    payload = [{"good": "request", "better": "value", "best": "woo"}]

    r = util.process_payload(payload, sort_keys=False, fields=["good", "better"])
    assert r == '[\n  {\n    "good": "request",\n    "better": "value"\n  }\n]'


def test_request_and_process(monkeypatch):
    mocked = mock.Mock()
    mocked_ctx = mock.Mock()
    monkeypatch.setattr(util, "ensure_login", mocked)
    mocked_process_response = mock.Mock()
    monkeypatch.setattr(util, "process_response", mocked_process_response)
    util._request_and_process(mocked_ctx, "POST", "service", "url", key="value")

    mocked.assert_called_once()
    mocked_process_response.assert_called_once()


def test_get_and_process(monkeypatch):
    mocked_ctx = mock.Mock()
    mocked = mock.Mock()
    monkeypatch.setattr(util, "_request_and_process", mocked)
    util.get_and_process(mocked_ctx, "service", "url", key="value")
    mocked.assert_called_once_with(mocked_ctx, "GET", "service", "url", key="value")


def test_post_and_process(monkeypatch):
    mocked_ctx = mock.Mock()
    mocked = mock.Mock()
    monkeypatch.setattr(util, "_request_and_process", mocked)
    util.post_and_process(mocked_ctx, "service", "url", key="value")
    mocked.assert_called_once_with(mocked_ctx, "POST", "service", "url", key="value")


def test_put_and_process(monkeypatch):
    mocked_ctx = mock.Mock()
    mocked = mock.Mock()
    monkeypatch.setattr(util, "_request_and_process", mocked)
    util.put_and_process(mocked_ctx, "service", "url", key="value")
    mocked.assert_called_once_with(mocked_ctx, "PUT", "service", "url", key="value")


def test_delete_and_process(monkeypatch):
    mocked_ctx = mock.Mock()
    mocked = mock.Mock()
    monkeypatch.setattr(util, "_request_and_process", mocked)
    util.delete_and_process(mocked_ctx, "service", "url", key="value")
    mocked.assert_called_once_with(mocked_ctx, "DELETE", "service", "url", key="value")


def test_patch_and_process(monkeypatch):
    mocked_ctx = mock.Mock()
    mocked = mock.Mock()
    monkeypatch.setattr(util, "_request_and_process", mocked)
    util.patch_and_process(mocked_ctx, "service", "url", key="value")
    mocked.assert_called_once_with(mocked_ctx, "PATCH", "service", "url", key="value")


def test_validate_string_not_empty():
    with pytest.raises(typer.BadParameter) as exc:
        util.validate_string_not_empty(mock.Mock(), mock.Mock(), "")

    assert exc.value.message == "Value must be a non-empty string."


def test_validate_strings_are_not_empty():
    with pytest.raises(typer.BadParameter) as exc:
        util.validate_strings_are_not_empty(mock.Mock(), mock.Mock(), ["A", ""])

    assert exc.value.message == "Value must be a non-empty string."


def test_validate_regex():
    with pytest.raises(typer.BadParameter) as exc:
        util.validate_regex("^[0-9]{1,3}$")(mock.Mock(), mock.Mock(), "")

    assert exc.value.message == "Value does not satisfy the rule ^[0-9]{1,3}$"


def test_read_env_dotfile_handles_missing():
    c = util.read_env_dotfile()

    assert c == {}


@pytest.mark.usefixtures("env_dotfile")
def test_read_env_dotfile():
    c = util.read_env_dotfile()

    assert c == {
        "test": {
            "access_token": "",
            "account": "root",
            "active": False,
            "hub_api_url": "https://hub-host/api/hub",
            "ignore_tls": False,
            "refresh_token": "",
            "user": "some-username",
            "cores": {},
        },
    }


def test_check_refresh_token_exists_env_no_token(monkeypatch):
    monkeypatch.setattr(util.typer, "echo", mock.Mock())
    ctx = mock.Mock()
    ctx.obj.credential = {}
    ctx.obj.active_env.refresh_token = ""

    with pytest.raises(typer.Exit):
        util.check_refresh_token_exists(ctx)

    assert util.typer.echo.call_args == mock.call("You need to login. Run neosctl env login")


def test_check_refresh_token_exists_env_has_token(monkeypatch):
    monkeypatch.setattr(util.typer, "echo", mock.Mock())
    ctx = mock.Mock()
    ctx.obj.credential = {}
    ctx.obj.active_env.refresh_token = "refresh-token"

    assert util.check_refresh_token_exists(ctx) is True


def test_check_env_active_no_env(monkeypatch):
    monkeypatch.setattr(util.typer, "echo", mock.Mock())
    ctx = mock.Mock()
    ctx.obj.active_env = None

    with pytest.raises(typer.Exit):
        util.check_env_active(ctx)

    assert util.typer.echo.call_args == mock.call("Environment not active! Run neosctl env activate <env>")


def test_check_env_active_with_env():
    ctx = mock.Mock()

    assert util.check_env_active(ctx) is True


@pytest.mark.usefixtures("active_env_core_dotfile")
def test_token_refresh_flow(cli_runner, httpx_mock, env_filepath):
    httpx_mock.add_response(
        method="GET",
        url=f"{GATEWAY_URL}/v2/data_product",
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

    httpx_mock.add_response(
        method="POST",
        url=REFRESH_URL,
        json={
            "access_token": "some-new-access-token",
            "refresh_token": "some-new-refresh-token",
            "expires_in": "300",
            "refresh_expires_in": "1800",
            "scope": "email profile",
            "token_type": "Bearer",
            "session_state": "some-session-state",
        },
    )

    response_payload = {
        "entities": [],
    }
    httpx_mock.add_response(
        method="GET",
        url=f"{GATEWAY_URL}/v2/data_product",
        json=response_payload,
    )

    result = cli_runner.invoke(["gateway", "data-product", "list"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload["entities"])

    config_file = """[test]
hub_api_url = "https://hub-host/api/hub"
user = "some-username"
access_token = "some-new-access-token"
refresh_token = "some-new-refresh-token"
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
        assert config_file == f.read()


def test_token_refresh_flow_bad_env(cli_runner):
    result = cli_runner.invoke(["--env=bad-env", "gateway", "data-product", "list"])

    assert result.exit_code == 1
    assert "Environment bad-env not found." in result.output


def test_token_refresh_flow_no_refresh_token(
    cli_runner,
    httpx_mock,
    env_dotfile_factory,
):
    envs = {
        "test": {
            "hub_api_url": "https://hub",
            "user": "some-username",
            "access_token": "access-token",
            "refresh_token": "",
            "ignore_tls": False,
            "active": True,
            "account": "root",
            "cores": {
                "smartconstruction": {
                    "name": "smartconstruction",
                    "host": "https://core",
                    "active": True,
                    "account": "sc",
                },
            },
        },
    }
    env_dotfile_factory(envs)

    httpx_mock.add_response(
        json={
            "type": "invalid-authorization",
            "error": {
                "error": "invalid_grant",
                "error_description": "Token is not active",
            },
            "title": "Problem with Identity Access Manager.",
        },
        status_code=401,
    )

    result = cli_runner.invoke(["gateway", "data-product", "list"])

    assert result.exit_code == 1
    assert "You need to login" in result.output


def test_token_refresh_flow_invalid_refresh_token(
    cli_runner,
    httpx_mock,
    env_dotfile_factory,
):
    httpx_mock.add_response(
        method="GET",
        url=f"{GATEWAY_URL}/v2/data_product",
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

    payload = {
        "type": "authorization-required",
        "error": {
            "error": "invalid_grant",
            "error_description": "Token is not active",
        },
        "title": "Problem with Identity Access Manager.",
    }

    httpx_mock.add_response(
        method="POST",
        url=REFRESH_URL,
        json=payload,
        status_code=401,
    )

    envs = {
        "test": {
            "hub_api_url": "https://hub-host/api/hub",
            "user": "some-username",
            "access_token": "access-token",
            "refresh_token": "invalid",
            "ignore_tls": False,
            "active": True,
            "account": "root",
            "cores": {
                "smartconstruction": {
                    "name": "smartconstruction",
                    "host": "https://core-gateway/api/gateway",
                    "active": True,
                    "account": "sc",
                },
            },
        },
    }
    env_dotfile_factory(envs)

    result = cli_runner.invoke(["gateway", "data-product", "list"])

    assert result.exit_code == 1
    assert result.output == render_cmd_output(payload, sort_keys=False)


def test_non_token_error_auth_error(
    cli_runner,
    httpx_mock,
    env_dotfile_factory,
):
    payload = {
        "type": "insufficient-permissions",
        "details": "Invalid access key",
        "title": "Registry failure.",
    }
    httpx_mock.add_response(
        method="GET",
        url=f"{GATEWAY_URL}/v2/data_product",
        json=payload,
        status_code=401,
    )

    envs = {
        "test": {
            "hub_api_url": "https://hub-host/api/hub",
            "user": "some-username",
            "access_token": "access-token",
            "refresh_token": "",
            "ignore_tls": False,
            "active": True,
            "account": "root",
            "cores": {
                "smartconstruction": {
                    "name": "smartconstruction",
                    "host": "https://core-gateway/api/gateway",
                    "active": True,
                    "account": "sc",
                },
            },
        },
    }
    env_dotfile_factory(envs)

    result = cli_runner.invoke(["gateway", "data-product", "list"])

    assert result.exit_code == 1
    assert result.output == render_cmd_output(payload, sort_keys=False)
