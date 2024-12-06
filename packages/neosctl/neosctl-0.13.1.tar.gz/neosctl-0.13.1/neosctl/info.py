"""Info commands, like info permissions, errors etc."""

from enum import Enum

import httpx
import typer

from neosctl import constant, util

app = typer.Typer()


class Service(Enum):
    """Supported information services."""

    hub = "hub"
    core = "core"
    storage = "storage"


def _get_host(ctx: typer.Context, service: Service) -> str:
    host = ctx.obj.hub_api_url
    if service == Service.core:
        host = ctx.obj.gateway_api_url
    elif service == Service.storage:
        host = ctx.obj.storage_api_url

    return host


@util.ensure_login
def get_permissions(ctx: typer.Context, service: Service) -> httpx.Response:
    """Get list of permissions."""
    host = _get_host(ctx, service)
    return util.get(
        ctx,
        service.value,
        f"{host}/__neos/permissions",
    )


@util.ensure_login
def get_error_codes(ctx: typer.Context, service: Service) -> httpx.Response:
    """Get list of permissions."""
    host = _get_host(ctx, service)
    return util.get(
        ctx,
        service.value,
        f"{host}/__neos/error_codes",
    )


@util.ensure_login
def get_version(ctx: typer.Context, service: Service) -> httpx.Response:
    """Get deployed version."""
    host = _get_host(ctx, service)
    return util.get(
        ctx,
        service.value,
        f"{host}/__neos/status",
    )


@app.command()
def permissions(
    ctx: typer.Context,
    *,
    service: Service = typer.Option(..., "--service", "-s"),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get current routes and permissions for a service."""
    r = get_permissions(ctx, service)
    util.process_response(r, output_format=ctx.obj.output_format, data_key="routes")


@app.command()
def error_codes(
    ctx: typer.Context,
    *,
    service: Service = typer.Option(..., "--service", "-s"),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get current errors for a service."""
    r = get_error_codes(ctx, service)
    util.process_response(r, output_format=ctx.obj.output_format, data_key="errors")


@app.command()
def version(
    ctx: typer.Context,
    *,
    service: Service = typer.Option(..., "--service", "-s"),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get deployed version for a service."""
    r = get_version(ctx, service)
    util.process_response(r, output_format=ctx.obj.output_format)
