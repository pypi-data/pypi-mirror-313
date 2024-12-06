"""Registry service commands."""

import enum
import typing
from uuid import UUID

import typer

from neosctl import constant, util
from neosctl.schema import Common
from neosctl.services.registry import schema

app = typer.Typer()
product_app = typer.Typer()
core_app = typer.Typer()
mesh_app = typer.Typer()

app.add_typer(product_app, name="product", help="Manage products.")
app.add_typer(core_app, name="core", help="Manage cores.")
app.add_typer(mesh_app, name="mesh", help="Manage mesh.")

ACCOUNT_OPT = typer.Option(None, help="Account override (root only).", callback=util.sanitize)


class SubscriptionStatus(enum.Enum):
    """Possible subscription status update values."""

    approved = "approved"
    rejected = "rejected"
    revoked = "revoked"


def _core_url(obj: Common) -> str:
    return "{}/registry/core".format(obj.hub_api_url.rstrip("/"))


def _mesh_core_url(obj: Common) -> str:
    return "{}/registry/mesh/core".format(obj.hub_api_url.rstrip("/"))


def _mesh_subscriptions_url(obj: Common) -> str:
    return "{}/registry/mesh/subscriptions".format(obj.hub_api_url.rstrip("/"))


def _data_product_url(obj: Common, postfix: str = "") -> str:
    return "{}/registry/data_product{}".format(obj.hub_api_url.rstrip("/"), postfix)


def _mesh_data_product_url(obj: Common, identifier: str) -> str:
    return "{}/registry/mesh/core/{}/data_product".format(obj.hub_api_url.rstrip("/"), identifier)


def _subscribe_data_product_url(obj: Common, identifier: str) -> str:
    return "{}/registry/core/{}/data_product/subscribe".format(obj.hub_api_url.rstrip("/"), identifier)


def _subscription_data_product_url(obj: Common, identifier: str) -> str:
    return "{}/registry/core/{}/data_product/subscription".format(obj.hub_api_url.rstrip("/"), identifier)


@core_app.command(name="register")
def register_core(
    ctx: typer.Context,
    partition: str = typer.Argument(..., help="Core partition", callback=util.sanitize),
    name: str = typer.Argument(..., help="Core name", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    *,
    private: bool = typer.Option(
        False,
        "--private",
        help="Limit visibility in mesh to core account.",
        callback=util.sanitize,
    ),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Register a core.

    Register a core to receive an identifier and access key for use in deployment.
    """
    rc = schema.RegisterCore(name=name, public=not private)
    util.post_and_process(
        ctx,
        constant.REGISTRY,
        _core_url(ctx.obj),
        json=rc.model_dump(exclude_none=True),
        headers={"X-Partition": partition},
        account=account,
    )


@core_app.command(name="migrate")
def migrate_core(
    ctx: typer.Context,
    identifier: str = typer.Option(..., help="Core identifier"),
    urn: str = typer.Option(..., help="Core urn", callback=util.sanitize),
    account: str = typer.Option(..., help="Account name", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Migrate a core out of root account.

    Migrate a core from `root` into an actual account.
    """
    mc = schema.MigrateCore(
        urn=urn,
        account=account,
    )

    util.post_and_process(
        ctx,
        constant.REGISTRY,
        f"{_core_url(ctx.obj)}/{identifier}/migrate",
        json=mc.model_dump(),
    )


@core_app.command(name="list")
def list_cores(
    ctx: typer.Context,
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """List accessible cores."""
    util.get_and_process(
        ctx,
        constant.REGISTRY,
        _core_url(ctx.obj),
        account=account,
        data_key="cores",
    )


@core_app.command(name="remove")
def remove_core(
    ctx: typer.Context,
    identifier: str = typer.Option(..., help="Core identifier"),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Remove a registered core."""
    util.delete_and_process(
        ctx,
        constant.REGISTRY,
        f"{_core_url(ctx.obj)}/{identifier}",
        account=account,
    )


@product_app.command(name="search")
def search_products(
    ctx: typer.Context,
    search_term: str = typer.Argument(..., callback=util.sanitize),
    *,
    keyword: bool = typer.Option(False, "--keyword/--hybrid", help="Search mode"),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Search published data products across cores."""
    util.get_and_process(
        ctx,
        constant.REGISTRY,
        _data_product_url(ctx.obj, "/search"),
        params={"search_term": search_term, "keyword_search": keyword},
        data_key="data_products",
    )


@product_app.command(name="get")
def get_product(
    ctx: typer.Context,
    urn: str = typer.Argument(..., callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product details."""
    util.get_and_process(
        ctx,
        constant.REGISTRY,
        _data_product_url(ctx.obj, f"/urn/{urn}"),
        sort_keys=True,
    )


@core_app.command(name="upsert-contact")
def upsert_contact(
    ctx: typer.Context,
    identifier: str = typer.Option(..., help="Core identifier"),
    user_id: UUID = typer.Option(..., help="Contact id"),
    role: str = typer.Option(..., help="Contact role"),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Add/Update a contact for a core."""
    c = schema.AddCoreContact(
        user_id=str(user_id),
        role=role,
    )

    util.post_and_process(
        ctx,
        constant.REGISTRY,
        f"{_core_url(ctx.obj)}/{identifier}/contact",
        json=c.model_dump(),
        account=account,
    )


@core_app.command(name="remove-contact")
def remove_contact(
    ctx: typer.Context,
    identifier: str = typer.Option(..., help="Core identifier"),
    user_id: UUID = typer.Option(..., help="Contact id"),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Remove a contact for a core."""
    c = schema.RemoveCoreContact(
        user_id=str(user_id),
    )

    util.delete_and_process(
        ctx,
        constant.REGISTRY,
        f"{_core_url(ctx.obj)}/{identifier}/contact",
        json=c.model_dump(),
        account=account,
    )


@mesh_app.command(name="cores")
def mesh_cores(
    ctx: typer.Context,
    account: typing.Optional[str] = ACCOUNT_OPT,
    search: str = typer.Option(None, help="Search core name(s)", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """List visible cores."""
    util.get_and_process(
        ctx,
        constant.REGISTRY,
        _mesh_core_url(ctx.obj),
        params={"search": search} if search else None,
        account=account,
    )


@mesh_app.command(name="core-products")
def mesh_core_products(
    ctx: typer.Context,
    identifier: str = typer.Option(..., help="Core identifier"),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """List visible products in a core."""
    util.get_and_process(
        ctx,
        constant.REGISTRY,
        _mesh_data_product_url(ctx.obj, identifier),
        account=account,
    )


@mesh_app.command(name="subscriptions")
def mesh_subscriptions(
    ctx: typer.Context,
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """List mesh subscriptions."""
    util.get_and_process(
        ctx,
        constant.REGISTRY,
        _mesh_subscriptions_url(ctx.obj),
        account=account,
    )


@product_app.command(name="subscribe")
def subscribe_product(
    ctx: typer.Context,
    identifier: str = typer.Option(
        ...,
        "--core-id",
        "-cid",
        help="Core identifier",
    ),
    product_identifier: str = typer.Option(
        ...,
        "--product-id",
        "-pid",
        help="Data product identifier",
    ),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Subscribe to a data product."""
    util.post_and_process(
        ctx,
        constant.REGISTRY,
        _subscribe_data_product_url(ctx.obj, identifier),
        account=account,
        json={"data_product_urn": product_identifier},
    )


@product_app.command(name="unsubscribe")
def unsubscribe_product(
    ctx: typer.Context,
    identifier: str = typer.Option(
        ...,
        "--core-id",
        "-cid",
        help="Core identifier",
    ),
    product_identifier: str = typer.Option(
        ...,
        "--product-id",
        "-pid",
        help="Data product identifier",
    ),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Unsubscribe from a data product."""
    util.delete_and_process(
        ctx,
        constant.REGISTRY,
        _subscribe_data_product_url(ctx.obj, identifier),
        account=account,
        json={"data_product_urn": product_identifier},
    )


@product_app.command(name="update-subscription")
def update_subscription(
    ctx: typer.Context,
    identifier: str = typer.Option(
        ...,
        "--core-id",
        "-cid",
        help="Core identifier",
    ),
    product_identifier: str = typer.Option(
        ...,
        "--product-id",
        "-pid",
        help="Data product identifier",
    ),
    subscriber_core_identifier: str = typer.Option(
        ...,
        "--sub-core-id",
        "-scid",
        help="Subscriber core identifier.",
    ),
    status: SubscriptionStatus = typer.Option(...),
    reason: str = typer.Option(...),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update subscription to a data product."""
    util.put_and_process(
        ctx,
        constant.REGISTRY,
        _subscription_data_product_url(ctx.obj, identifier),
        account=account,
        json={
            "data_product_urn": product_identifier,
            "subscriber_core_identifier": subscriber_core_identifier,
            "status": status.value,
            "reason": reason,
        },
    )
