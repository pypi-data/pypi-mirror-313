"""Utility functions for neosctl."""

import configparser
import logging
import pathlib
import re
import sys
import typing

import click
import httpx
import orjson as json
import pydantic
import rtoml
import ryaml as yaml
import tabulate
import typer
from aws4.key_pair import KeyPair
from pygments import formatters, highlight, lexers

from neosctl import constant, schema
from neosctl.http import Method, NeosClient, RequestException

logger = logging.getLogger("neosctl.error")

if sys.version_info < (3, 10):  # pragma: no cover
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec  # pragma: no cover


def output_format_callback(
    ctx: typer.Context,
    output_format: constant.Output,
) -> constant.Output:
    """Inject output format into the context."""
    ctx.obj.output_format = output_format.value
    return output_format


def fields_callback(
    ctx: typer.Context,
    fields: typing.Optional[list[str]],
) -> list[str]:
    """Inject fields selection into the context."""
    ctx.obj.fields = fields
    return fields or []


Verbosity = typing.Annotated[
    int,
    typer.Option(
        ...,
        "-v",
        "--verbose",
        help="Verbose output. Use multiple times to increase level of verbosity.",
        count=True,
        max=3,
    ),
]

Output = typing.Annotated[
    constant.Output,
    typer.Option(
        ...,
        "--output",
        "-o",
        help="Output format",
        callback=output_format_callback,
    ),
]


Fields = typing.Annotated[
    typing.Optional[list[str]],
    typer.Option(
        ...,
        "-f",
        "--field",
        help="Filter response fields.",
        callback=fields_callback,
    ),
]


def dumps_formatted_json(
    payload: typing.Union[dict, list[dict]],
    *,
    sort_keys: bool = True,
) -> str:
    """Dump formatted json.

    json.dump provided payload with indent 2 and (un)sorted keys.
    """
    option = json.OPT_SORT_KEYS | json.OPT_INDENT_2 if sort_keys else json.OPT_INDENT_2
    return json.dumps(payload, option=option).decode()


def prettify_json(payload: typing.Union[dict, list[dict]], *, sort_keys: bool = True) -> str:
    """Dump formatted json with colour highlighting and sorted keys."""
    return highlight(
        dumps_formatted_json(payload, sort_keys=sort_keys),
        lexers.JsonLexer(),
        formatters.TerminalFormatter(),
    )


def prettify_yaml(payload: typing.Union[dict, list[dict]], *, sort_keys: bool = True) -> str:  # noqa: ARG001
    """Dump formatted yaml with colour highlighting and sorted keys."""
    return highlight(
        yaml.dumps(payload),
        lexers.YamlLexer(),
        formatters.TerminalFormatter(),
    )


def prettify_toml(payload: typing.Union[dict, list[dict]], *, sort_keys: bool = True) -> str:  # noqa: ARG001
    """Dump formatted toml with colour highlighting and sorted keys."""
    return highlight(
        rtoml.dumps(payload, pretty=True),
        lexers.TOMLLexer(),
        formatters.TerminalFormatter(),
    )


def tabulate_data(payload: typing.Union[dict, list[dict]], *, sort_keys: bool = True) -> str:
    """Render data in a text table."""
    if not isinstance(payload, list):
        ret = payload.items()
        if sort_keys:
            ret = sorted(ret)
        headers = ()
        tablefmt = "plain"

    else:
        ret = [
            [
                *(row.model_dump(mode="json").values() if isinstance(row, pydantic.BaseModel) else row.values()),
            ]
            for row in payload
        ]
        headers = (k.title() for k in payload[0])
        tablefmt = "simple"

    return tabulate.tabulate(ret, headers=headers, tablefmt=tablefmt)


def is_success_response(response: httpx.Response) -> bool:
    """Check if a response is `successful`."""
    return constant.SUCCESS_CODE <= response.status_code < constant.REDIRECT_CODE


def exit_with_output(msg: str, exit_code: int = 0) -> typer.Exit:
    """Render output to terminal and exit."""
    typer.echo(msg)

    return typer.Exit(exit_code)


render_callables: dict[str, typing.Callable[[typing.Union[dict, list[dict]], bool], str]] = {
    "json": prettify_json,
    "yaml": prettify_yaml,
    "toml": prettify_toml,
    "text": tabulate_data,
}


def process_payload(
    payload: typing.Union[dict, list[dict]],
    output_format: str = "json",
    fields: typing.Optional[list[str]] = None,
    *,
    sort_keys: bool = True,
) -> str:
    """Process a payload and convert to a string in requested format."""
    if fields:
        if isinstance(payload, list):
            payload = [{k: v for k, v in row.items() if k in fields} for row in payload]
        else:
            payload = {k: v for k, v in payload.items() if k in fields}
    render_callable = render_callables.get(output_format, prettify_json)
    return render_callable(payload, sort_keys=sort_keys)


def process_response(
    response: httpx.Response,
    output_format: str = "json",
    render_callable: typing.Optional[typing.Callable[[typing.Union[dict, list], list[str], bool], str]] = None,
    data_key: typing.Optional[str] = None,
    fields: typing.Optional[list[str]] = None,
    *,
    sort_keys: bool = True,
) -> None:
    """Process a server response, render the output and exit."""
    exit_code = 0
    if render_callable is None:
        render_callable = render_callables.get(output_format, prettify_json)
    try:
        data = response.json()

        if response.status_code >= constant.BAD_REQUEST_CODE:
            exit_code = 1
            message = prettify_json(data, sort_keys=False)
        else:
            if data_key:
                data = data[data_key]

            if fields:
                if isinstance(data, list):
                    data = [{k: v for k, v in row.items() if k in fields} for row in data]
                else:
                    data = {k: v for k, v in data.items() if k in fields}
            # TODO: Inspect function definition detect sort_keys support
            message = render_callable(data, sort_keys=sort_keys)
    except Exception:
        logger.info(response.content)
        logger.exception("Failure to parse response.")
        exit_code = 1
        message = "Unable to parse response."

    raise exit_with_output(
        msg=message,
        exit_code=exit_code,
    )


def read_env_dotfile() -> dict:
    """Read in `.neosctl/env` configuration file and parse."""
    if pathlib.Path(constant.ENV_FILEPATH).exists():
        return rtoml.load(constant.ENV_FILEPATH)

    return {}


def read_credential_dotfile() -> configparser.ConfigParser:
    """Read in `.neosctl/credential` configuration file and parse."""
    c = configparser.ConfigParser()
    c.read(constant.CREDENTIAL_FILEPATH)
    return c


def get_env_section(c: dict, name: str) -> schema.Env:
    """Get env from neosctl configuration.

    If env is not found exit cli.

    Returns:
    -------
    schema.Env for the requested environment.
    """
    try:
        return schema.Env(name=name, **c[name])
    except KeyError:
        pass

    raise exit_with_output(
        msg=f"Environment {name} not found.",
        exit_code=1,
    )


def get_user_credential(
    c: configparser.ConfigParser,
    name: str,
    *,
    optional: bool = False,
) -> typing.Optional[schema.Credential]:
    """Get neosctl credentials for environment.

    If env credentials are not found exit cli.

    Returns:
    -------
    schema.Credential for the requested environment.
    """
    try:
        return schema.Credential(**c[name])
    except KeyError:
        pass

    if not optional:
        raise exit_with_output(
            msg=f"Environment {name} not configured with credentials.",
            exit_code=1,
        )
    return None


def _auth_url(hub_api_url: str) -> str:
    return "{}".format(hub_api_url.rstrip("/"))


def check_refresh_token_exists(ctx: typer.Context) -> bool:
    """Check if refresh token exists."""
    credential = get_user_credential(ctx.obj.credential, ctx.obj.name, optional=True)
    if ctx.obj.active_env is None or (not ctx.obj.active_env.refresh_token and credential is None):
        raise exit_with_output(
            msg="You need to login. Run neosctl env login",
            exit_code=1,
        )

    return True


def _refresh_token(ctx: typer.Context) -> httpx.Response:
    check_env_active(ctx)
    check_refresh_token_exists(ctx)

    refresh_token = ctx.obj.refresh_token
    r = post(
        ctx,
        constant.IAM,
        f"{_auth_url(ctx.obj.hub_api_url)}/iam/refresh",
        json={"refresh_token": refresh_token},
    )

    if not is_success_response(r):
        process_response(r)

    if ctx.obj.active_env:
        d = r.json()
        ctx.obj.active_env.access_token = d["access_token"]
        ctx.obj.active_env.refresh_token = d["refresh_token"]

        upsert_env(ctx, ctx.obj.active_env)

    return r


P = ParamSpec("P")


def ensure_login(method: typing.Callable[P, httpx.Response]) -> typing.Callable[P, httpx.Response]:
    """Capture authentication errors and retry requests.

    On request failure check if the response is a 401, and attempt to refresh the access_token.
    Retry the request with refreshed token, on subsequent failure, return.
    """

    def check_access_token(*args: P.args, **kwargs: P.kwargs) -> httpx.Response:
        ctx = args[0]
        if not isinstance(ctx, (typer.Context, click.Context)):
            # Developer reminder
            msg = "First argument should be click.Context instance"
            raise TypeError(msg)

        r = method(*args, **kwargs)

        check_env_active(ctx)

        # Try to refresh token
        # Confirm it is a token invalid 401, registry not configured mistriggers this flow.
        if r.status_code == constant.UNAUTHORISED_CODE:
            data = r.json()
            if "type" in data and data["type"] in {
                "authorization-required",
                "authorization-failed",
                "invalid-authorization",
            }:
                _refresh_token(ctx)

                r = method(*args, **kwargs)

        return r

    return check_access_token


def get_active_env(
    c: dict,
    override_name: typing.Optional[str],
) -> typing.Optional[schema.Env]:
    """Get active environment."""
    for name, data in c.items():
        if override_name == name:
            return schema.Env(name=name, **data)

        if data["active"] and override_name is None:
            return schema.Env(name=name, **data)

    if override_name is not None:
        raise exit_with_output(
            msg=f"Environment {override_name} not found.",
            exit_code=1,
        )
    return None


def get_active_core(
    env: typing.Optional[schema.Env],
    override_name: typing.Optional[str],
) -> typing.Optional[schema.Core]:
    """Get active environment."""
    if env:
        if override_name:
            try:
                return env.cores[override_name]
            except KeyError as e:
                raise exit_with_output(
                    msg=f"Core {override_name} not found!",
                    exit_code=1,
                ) from e
        for core in env.cores.values():
            if core.active:
                return core

    return None


def bearer(ctx: typer.Context) -> typing.Optional[dict]:
    """Generate bearer authorization header."""
    if not ctx.obj.access_token:  # nosec: B105
        return None

    return {"Authorization": f"Bearer {ctx.obj.access_token}"}


def check_env_active(ctx: typer.Context) -> bool:
    """Check if an env is active in neosctl configuration or exit."""
    if not ctx.obj.active_env:
        raise exit_with_output(
            msg="Environment not active! Run neosctl env activate <env>",
            exit_code=1,
        )

    return True


def upsert_env(
    ctx: typer.Context,
    env: schema.Env,
) -> configparser.ConfigParser:
    """Update neosctl env configuration in place."""
    ctx.obj.env[env.name] = env.model_dump(exclude=["name"], mode="json")

    with constant.ENV_FILEPATH.open("w") as env_file:
        rtoml.dump(ctx.obj.env, env_file)

    return ctx.obj.env


def upsert_credential(
    ctx: typer.Context,
    access_key_id: str,
    secret_access_key: str,
    name: str,
) -> None:
    """Update neosctl credential in place."""
    ctx.obj.credential[name] = {"access_key_id": access_key_id, "secret_access_key": secret_access_key}

    with constant.CREDENTIAL_FILEPATH.open("w") as credential_file:
        ctx.obj.credential.write(credential_file)


def remove_env(
    ctx: typer.Context,
    name: str,
) -> configparser.ConfigParser:
    """Remove an environment from neosctl configuration."""
    if name not in ctx.obj.env:
        raise exit_with_output(
            msg=f"Can not remove {name} environment, environment not found.",
            exit_code=1,
        )
    ctx.obj.env.pop(name)
    ctx.obj.credential.remove_section(name)

    with constant.ENV_FILEPATH.open("w") as env_file:
        rtoml.dump(ctx.obj.env, env_file)

    with constant.CREDENTIAL_FILEPATH.open("w") as credential_file:
        ctx.obj.credential.write(credential_file)

    return ctx.obj.env


def get_file_location(filepath: str) -> pathlib.Path:
    """Get a Path for the provided filepath, exit if not found."""
    fp = pathlib.Path(filepath)
    if not fp.exists():
        raise exit_with_output(
            msg=f"Can not find file: {fp}",
            exit_code=1,
        )
    return fp


def load_json_file(fp: pathlib.Path, content_type: str) -> typing.Union[dict, list[dict]]:
    """Load contents of json file, exit if not found."""
    with fp.open() as f:
        try:
            data = json.loads(f.read())
        except json.JSONDecodeError:
            logger.exception("Error loading json file.")
            raise exit_with_output(  # noqa: B904
                msg=f"Invalid {content_type} file, must be json format.",
                exit_code=1,
            )
            return []  # never reached as raise exit_with_output, but it makes type checker happy

    return data


T = typing.TypeVar("T", bound=pydantic.BaseModel)


def load_object(t: type[T], filepath: str, file_description: str) -> T:
    """Trying to read and parse JSON file into the given data type."""
    fp = get_file_location(filepath)
    obj = load_json_file(fp, file_description)
    if not isinstance(obj, dict):
        raise exit_with_output(
            msg=f"Require a json file containing an object, `{type(obj)}` provided.",
            exit_code=1,
        )
    try:
        return t(**obj)
    except pydantic.ValidationError as e:
        logger.exception("Error loading json file.")
        raise exit_with_output(
            msg=str(e),
            exit_code=1,
        ) from e


def _request(ctx: typer.Context, method: str, service: str, url: str, **kwargs: ...) -> httpx.Response:
    credential = get_user_credential(ctx.obj.credential, ctx.obj.name, optional=True)
    bearer = ctx.obj.access_token if credential is None else None

    c = NeosClient(
        service=service,
        token=bearer,
        key_pair=KeyPair(credential.access_key_id, credential.secret_access_key) if credential else None,
        partition="ksa",
        proxy=ctx.obj.http_proxy,
    )

    headers = kwargs.pop("headers", None) or {}
    headers_ = extract_account(ctx, account=kwargs.pop("account", None))
    headers_["X-Partition"] = "ksa"
    headers.update(headers_)

    params = kwargs.pop("params", None) or {}

    try:
        return c.request(
            url,
            Method[method],
            verify=not ctx.obj.ignore_tls,
            params=params,
            headers=headers,
            **kwargs,
        )
    except RequestException as e:
        logger.exception("Request failed.")
        raise exit_with_output(
            msg=f"{service.title()} {method} request to {url} failed ({e.status}). [{e.type}]",
            exit_code=1,
        ) from e


def _request_and_process(
    ctx: typer.Context,
    method: str,
    service: str,
    url: str,
    data_key: typing.Optional[str] = None,
    render_callable: typing.Optional[typing.Callable[[typing.Union[dict, list[dict]], bool], str]] = None,
    *,
    sort_keys: bool = True,
    **kwargs: ...,
) -> None:
    @ensure_login
    def internal_request(context: typer.Context) -> httpx.Response:
        return _request(context, method, service, url, **kwargs)

    response = internal_request(ctx)

    process_response(
        response,
        data_key=data_key,
        output_format=ctx.obj.output_format,
        sort_keys=sort_keys,
        fields=ctx.obj.fields,
        render_callable=render_callable,
    )


def get_and_process(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> None:
    """Execute and process GET request."""
    _request_and_process(ctx, "GET", service, url, **kwargs)


def post_and_process(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> None:
    """Execute and process POST request."""
    _request_and_process(ctx, "POST", service, url, **kwargs)


def put_and_process(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> None:
    """Execute and process PUT request."""
    _request_and_process(ctx, "PUT", service, url, **kwargs)


def delete_and_process(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> None:
    """Execute and process DELETE request."""
    _request_and_process(ctx, "DELETE", service, url, **kwargs)


def patch_and_process(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> None:
    """Execute and process PATCH request."""
    _request_and_process(ctx, "PATCH", service, url, **kwargs)


def get(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> httpx.Response:
    """Execute a GET request."""
    return _request(ctx, "GET", service, url, **kwargs)


def post(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> httpx.Response:
    """Execute a POST request."""
    return _request(ctx, "POST", service, url, **kwargs)


def put(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> httpx.Response:
    """Execute a PUT request."""
    return _request(ctx, "PUT", service, url, **kwargs)


def delete(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> httpx.Response:
    """Execute a DELETE request."""
    return _request(ctx, "DELETE", service, url, **kwargs)


def sanitize(
    ctx: typer.Context,  # noqa: ARG001
    param: click.Parameter,  # noqa: ARG001
    value: typing.Optional[str],
) -> typing.Optional[str]:
    """Parameter's sanitize callback."""
    if value and isinstance(value, str):
        return value.rstrip("\r\n")

    return value


def validate_string_not_empty(
    ctx: typer.Context,
    param: click.Parameter,
    value: str,
) -> str:
    """String validation callback."""
    value = value.strip()

    if not value:
        message = "Value must be a non-empty string."
        raise typer.BadParameter(message, ctx=ctx, param=param)

    return value


def validate_strings_are_not_empty(
    ctx: typer.Context,
    param: click.Parameter,
    values: list[str],
) -> list[str]:
    """List of strings validation callback."""
    return [validate_string_not_empty(ctx, param, value) for value in values]


def validate_regex(
    pattern: str,
) -> typing.Callable[[typer.Context, click.Parameter, str], str]:
    """Regex validation callback."""

    def factory(
        ctx: typer.Context,
        param: click.Parameter,
        value: str,
    ) -> str:
        value = value.strip()

        if not re.match(pattern, value):
            message = f"Value does not satisfy the rule {pattern}"
            raise typer.BadParameter(message, ctx=ctx, param=param)

        return value

    return factory


def extract_account(
    ctx: typer.Context,
    account: typing.Optional[str] = None,
) -> dict:
    """Set up account header and params."""
    active_account = ctx.obj.account
    if active_account != "root" and account is not None:
        raise exit_with_output(
            msg="Only root account admins can impersonate other accounts.",
            exit_code=1,
        )

    headers = {"X-Account": active_account}
    if account:
        headers["X-Account-Override"] = account

    return headers
