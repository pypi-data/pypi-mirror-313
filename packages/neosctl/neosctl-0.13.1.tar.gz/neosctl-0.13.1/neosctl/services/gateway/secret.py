"""Gateway secret commands."""

import typer

from neosctl import constant, util
from neosctl.services.gateway import schema

app = typer.Typer(name="output")


def _secret_url(ctx: typer.Context) -> str:
    return "{}/v2/secret".format(ctx.obj.gateway_api_url.rstrip("/"))


def _identified_secret_url(ctx: typer.Context, identifier: str) -> str:
    return "{}/v2/secret/{}".format(
        ctx.obj.gateway_api_url.rstrip("/"),
        identifier,
    )


IDENTIFIER_ARGUMENT = typer.Argument(..., help="Secret identifier", callback=util.sanitize)


@app.command(name="create")
def create_element(
    ctx: typer.Context,
    filepath: str = typer.Argument(..., help="Filepath to secret description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Create new secret."""
    data = util.load_object(schema.UpdateSecret, filepath, "secret")
    util.post_and_process(
        ctx,
        constant.GATEWAY,
        _secret_url(ctx),
        json=data.model_dump(by_alias=True),
    )


@app.command(name="list")
def list_elements(
    ctx: typer.Context,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """List secrets."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        _secret_url(ctx),
    )


@app.command(name="get")
def get_element(
    ctx: typer.Context,
    identifier: str = IDENTIFIER_ARGUMENT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get secret."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        _identified_secret_url(ctx, identifier),
    )


@app.command(name="update")
def update_element(
    ctx: typer.Context,
    identifier: str = IDENTIFIER_ARGUMENT,
    filepath: str = typer.Argument(..., help="Filepath to secret description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update secret."""
    data = util.load_object(schema.UpdateSecret, filepath, "secret")
    util.put_and_process(
        ctx,
        constant.GATEWAY,
        _identified_secret_url(ctx, identifier),
        json=data.model_dump(by_alias=True),
    )


@app.command(name="delete")
def delete_element(
    ctx: typer.Context,
    identifier: str = IDENTIFIER_ARGUMENT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Delete secret."""
    util.delete_and_process(
        ctx,
        constant.GATEWAY,
        _identified_secret_url(ctx, identifier),
    )


@app.command(name="delete-keys")
def delete_element_keys(
    ctx: typer.Context,
    identifier: str = IDENTIFIER_ARGUMENT,
    filepath: str = typer.Argument(..., help="Filepath to secret keys description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Delete secret keys."""
    data = util.load_object(schema.SecretKeys, filepath, "secret")
    util.delete_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_secret_url(ctx, identifier)}/keys",
        json=data.model_dump(by_alias=True),
    )
