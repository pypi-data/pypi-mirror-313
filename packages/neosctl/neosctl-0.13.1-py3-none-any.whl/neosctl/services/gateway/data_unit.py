"""Gateway data unit commands."""

from typing import Optional

import typer

from neosctl import constant, util
from neosctl.services.gateway import entity, schema

app = typer.Typer(name="data_unit")


def _data_unit_url(ctx: typer.Context) -> str:
    return "{}/v2/data_unit".format(ctx.obj.gateway_api_url.rstrip("/"))


def _identified_data_unit_url(ctx: typer.Context, identifier: str) -> str:
    return "{}/v2/data_unit/{}".format(
        ctx.obj.gateway_api_url.rstrip("/"),
        identifier,
    )


arg_generator = entity.EntityArgGenerator("Data Unit")


@app.command(name="create")
def create_entity(
    ctx: typer.Context,
    label: str = arg_generator.label,
    name: str = arg_generator.name,
    description: str = arg_generator.description,
    owner: Optional[str] = arg_generator.owner_optional,
    contacts: list[str] = arg_generator.contacts,
    links: list[str] = arg_generator.links,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Create data unit."""
    entity.create_entity(
        ctx=ctx,
        url=_data_unit_url(ctx=ctx),
        label=label,
        name=name,
        description=description,
        owner=owner,
        contacts=contacts,
        links=links,
    )


@app.command(name="list")
def list_entities(
    ctx: typer.Context,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """List data units."""
    entity.list_entities(ctx=ctx, url=_data_unit_url(ctx=ctx))


@app.command(name="get")
def get_entity(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data unit."""
    entity.get_entity(
        ctx=ctx,
        url=_data_unit_url(ctx=ctx),
        identifier=identifier,
    )


@app.command(name="delete")
def delete_entity(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Delete data unit."""
    entity.delete_entity(
        ctx=ctx,
        url=_data_unit_url(ctx=ctx),
        identifier=identifier,
    )


@app.command(name="get-info")
def get_entity_info(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data unit info."""
    entity.get_entity_info(
        ctx=ctx,
        url=_data_unit_url(ctx=ctx),
        identifier=identifier,
    )


@app.command(name="update")
def update_entity(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    label: str = arg_generator.label,
    name: str = arg_generator.name,
    description: str = arg_generator.description,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data unit."""
    entity.update_entity(
        ctx=ctx,
        url=_data_unit_url(ctx=ctx),
        identifier=identifier,
        label=label,
        name=name,
        description=description,
    )


@app.command(name="update-info")
def update_entity_info(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    owner: str = arg_generator.owner,
    contacts: list[str] = arg_generator.contacts,
    links: list[str] = arg_generator.links,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data unit info."""
    entity.update_entity_info(
        ctx=ctx,
        url=_data_unit_url(ctx=ctx),
        identifier=identifier,
        owner=owner,
        contacts=contacts,
        links=links,
    )


@app.command(name="get-journal")
def get_entity_journal(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    page: int = typer.Option(1, "--page", "-p", help="Page number", callback=util.sanitize),
    per_page: int = typer.Option(25, "--per-page", "-pp", help="Number of items per page", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data unit journal."""
    entity.get_entity_journal(
        ctx=ctx,
        url=_data_unit_url(ctx=ctx),
        identifier=identifier,
        page=page,
        per_page=per_page,
    )


@app.command(name="update-journal")
def update_entity_journal(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Filepath to journal note payload", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data unit journal."""
    entity.update_entity_journal(
        ctx=ctx,
        url=_data_unit_url(ctx=ctx),
        identifier=identifier,
        filepath=filepath,
    )


@app.command(name="get-links")
def get_entity_links(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data unit links."""
    entity.get_entity_links(
        ctx=ctx,
        url=_data_unit_url(ctx=ctx),
        identifier=identifier,
    )


@app.command(name="update-metadata")
def update_entity_metadata(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Filepath to metadata description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data unit metadata."""
    data = util.load_object(schema.UpdateEntityMetadataRequest, filepath, "metadata")

    util.put_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_unit_url(ctx, identifier)}/metadata",
        json=data.model_dump(by_alias=True),
    )


@app.command(name="delete-metadata")
def delete_entity_metadata(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Filepath to metadata description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Delete data unit metadata."""
    data = util.load_object(schema.DeleteEntityMetadataRequest, filepath, "metadata")

    util.delete_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_unit_url(ctx, identifier)}/metadata",
        json=data.model_dump(by_alias=True),
    )


@app.command(name="get-schema")
def get_entity_schema(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data unit schema."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_unit_url(ctx, identifier)}/schema",
    )


@app.command(name="get-config")
def get_entity_config(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data unit config."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_unit_url(ctx, identifier)}/config",
    )


@app.command(name="update-config")
def update_entity_config(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Filepath to config description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data unit config."""
    data = util.load_object(schema.UpdateDataUnitConfiguration, filepath, "configuration")
    util.put_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_unit_url(ctx, identifier)}/config",
        json=data.model_dump(by_alias=True),
    )
