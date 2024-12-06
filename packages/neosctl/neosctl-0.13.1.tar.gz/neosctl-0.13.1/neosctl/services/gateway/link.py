"""Gateway entities link commands."""

import enum

import typer

from neosctl import constant, util
from neosctl.util import exit_with_output

app = typer.Typer()


def _link_url(
    ctx: typer.Context,
    p_type: str,
    p_identifier: str,
    c_type: str,
    c_identifier: str,
) -> str:
    return "{}/v2/link/{}/{}/{}/{}".format(
        ctx.obj.gateway_api_url.rstrip("/"),
        p_type,
        p_identifier,
        c_type,
        c_identifier,
    )


class ParentEntityType(enum.Enum):
    """Valid types for parent entity."""

    data_system = "data_system"
    data_source = "data_source"
    data_unit = "data_unit"
    data_product = "data_product"


class ChildEntityType(enum.Enum):
    """Valid types for child entity."""

    data_source = "data_source"
    data_unit = "data_unit"
    data_product = "data_product"
    output = "output"


VALID_LINKS = [
    (ParentEntityType.data_system, ChildEntityType.data_source),
    (ParentEntityType.data_source, ChildEntityType.data_unit),
    (ParentEntityType.data_unit, ChildEntityType.data_product),
    (ParentEntityType.data_product, ChildEntityType.data_product),
    (ParentEntityType.data_product, ChildEntityType.output),
]


def _check_link_types(p: ParentEntityType, c: ChildEntityType) -> None:
    if (p, c) not in VALID_LINKS:
        raise exit_with_output(
            msg=f"Link between {p.value} and {c.value} is not allowed.",
            exit_code=1,
        )


@app.command(name="create")
def link_entities(
    ctx: typer.Context,
    parent_type: ParentEntityType = typer.Argument(..., help="Parent entity type"),
    parent_identifier: str = typer.Argument(..., help="Parent identifier"),
    child_type: ChildEntityType = typer.Argument(..., help="Child entity type"),
    child_identifier: str = typer.Argument(..., help="Child identifier"),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Create link between entities."""
    _check_link_types(parent_type, child_type)
    url = _link_url(ctx, parent_type.value, parent_identifier, child_type.value, child_identifier)
    util.post_and_process(ctx, constant.GATEWAY, url)


@app.command(name="delete")
def unlink_entities(
    ctx: typer.Context,
    parent_type: ParentEntityType = typer.Argument(..., help="Parent entity type"),
    parent_identifier: str = typer.Argument(..., help="Parent identifier"),
    child_type: ChildEntityType = typer.Argument(..., help="Child entity type"),
    child_identifier: str = typer.Argument(..., help="Child identifier"),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Delete link between entities."""
    _check_link_types(parent_type, child_type)
    url = _link_url(ctx, parent_type.value, parent_identifier, child_type.value, child_identifier)
    util.delete_and_process(ctx, constant.GATEWAY, url)
