"""IAM service commands."""

import typing
from uuid import UUID

import httpx
import typer

from neosctl import constant, util
from neosctl.services.iam import schema
from neosctl.util import is_success_response, process_response

app = typer.Typer(name=constant.IAM)

account_app = typer.Typer(name="account")
user_app = typer.Typer(name="user")
policy_app = typer.Typer(name="policy")
group_app = typer.Typer(name="group")

app.add_typer(account_app, name="account", help="Manage accounts.")
app.add_typer(user_app, name="user", help="Manage users.")
app.add_typer(group_app, name="group", help="Manage groups.")
app.add_typer(policy_app, name="policy", help="Manage policies.")


ACCOUNT_OPT = typer.Option(None, help="Account override (root only).", callback=util.sanitize)


def _iam_url(hub_api_url: str, postfix: str = "") -> str:
    return "{}/iam/{}".format(hub_api_url.rstrip("/"), postfix)


@account_app.command(name="create")
def create_account(
    ctx: typer.Context,
    display_name: str = typer.Option(..., "--display-name", "-d", help="Account display name."),
    name: str = typer.Option(..., "--name", "-n", help="Account name (used in urns)."),
    description: str = typer.Option(..., "--description", "--desc", help="Account description."),
    owner: str = typer.Option(..., "--owner", help="Account owner."),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Create a system account."""
    data = schema.CreateAccount(
        display_name=display_name,
        name=name,
        description=description,
        owner=owner,
    )

    util.post_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, "account"),
        json=data.model_dump(mode="json"),
    )


@account_app.command(name="delete")
def delete_account(
    ctx: typer.Context,
    identifier: str = typer.Argument(..., help="Account identifier.", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Delete an account."""
    util.delete_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, f"account/{identifier}"),
    )


@account_app.command(name="update")
def update_account(
    ctx: typer.Context,
    display_name: str = typer.Option(..., "--display-name", "-d", help="Account display name."),
    description: str = typer.Option(..., "--description", "--desc", help="Account description."),
    owner: str = typer.Option(..., "--owner", help="Account owner."),
    identifier: str = typer.Argument(..., help="Account identifier.", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update an account."""
    data = schema.UpdateAccount(
        display_name=display_name,
        description=description,
        owner=owner,
    )

    util.put_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, f"account/{identifier}"),
        json=data.model_dump(mode="json"),
    )


@account_app.command(name="list")
def list_accounts(
    ctx: typer.Context,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """List system accounts."""
    util.get_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, "account"),
    )


@policy_app.command(name="list")
def list_policies(
    ctx: typer.Context,
    page: int = typer.Option(1, help="Page number."),
    page_size: int = typer.Option(10, help="Page size number."),
    resource: typing.Optional[str] = typer.Option(None, help="Resource nrn.", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """List existing policies."""
    params: dict[str, typing.Union[int, str]] = {"page": page, "page_size": page_size}
    if resource:
        params["resource"] = resource

    util.get_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, "policy/users"),
        params=params,
        account=account,
    )


@policy_app.command(name="create")
def create_from_json(
    ctx: typer.Context,
    filepath: str = typer.Argument(..., help="Filepath of the user policy json payload", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Create an IAM policy."""
    fp = util.get_file_location(filepath)
    user_policy_payload = util.load_json_file(fp, "policy")

    user_policy = schema.UserPolicy(**user_policy_payload)  # type: ignore[reportGeneralTypeIssues]

    util.post_and_process(
        ctx,
        constant.IAM,
        "{iam_url}".format(iam_url=_iam_url(ctx.obj.hub_api_url, "policy/user")),
        json=user_policy.model_dump(mode="json"),
        account=account,
    )


@policy_app.command(name="update")
def update_from_json(
    ctx: typer.Context,
    principal: str = typer.Argument(..., help="Principal uuid", callback=util.sanitize),
    filepath: str = typer.Argument(..., help="Filepath of the user policy json payload", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update an existing IAM policy."""
    fp = util.get_file_location(filepath)
    user_policy_payload = util.load_json_file(fp, "policy")

    user_policy = schema.UserPolicy(**user_policy_payload)  # type: ignore[reportGeneralTypeIssues]
    params = {"user_nrn": principal}

    util.put_and_process(
        ctx,
        constant.IAM,
        "{iam_url}".format(iam_url=_iam_url(ctx.obj.hub_api_url, "policy/user")),
        params=params,
        json=user_policy.model_dump(mode="json"),
        account=account,
    )


@policy_app.command()
def delete(
    ctx: typer.Context,
    user_nrn: str = typer.Argument(..., callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Delete an existing IAM policy."""
    params = {"user_nrn": user_nrn}

    util.delete_and_process(
        ctx,
        constant.IAM,
        "{iam_url}".format(iam_url=_iam_url(ctx.obj.hub_api_url, "policy/user")),
        params=params,
        account=account,
    )


@policy_app.command()
def get(
    ctx: typer.Context,
    user_nrn: str = typer.Argument(..., callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get an existing IAM policy."""
    params = {"user_nrn": user_nrn}

    util.get_and_process(
        ctx,
        constant.IAM,
        "{iam_url}".format(iam_url=_iam_url(ctx.obj.hub_api_url, "policy/user")),
        params=params,
        account=account,
    )


@user_app.command(name="create")
def create_user(
    ctx: typer.Context,
    username: str = typer.Option(..., "--username", "-u", callback=util.sanitize),
    email: str = typer.Option(..., "--email", "-e", callback=util.sanitize),
    first_name: str = typer.Option(..., "--first-name", "-n", callback=util.sanitize),
    last_name: str = typer.Option(..., "--last-name", "-l", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Create a keycloak user, and assign to account."""
    user = schema.CreateUser(
        enabled=True,
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

    util.post_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, "user"),
        json=user.model_dump(mode="json"),
        account=account,
        timeout=30,
    )


@user_app.command(name="delete")
def delete_user(
    ctx: typer.Context,
    user_id: str = typer.Option(
        ...,
        "--user-id",
        "-uid",
        help="User id in keycloak.",
        callback=util.sanitize,
    ),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Detach user from account."""
    util.delete_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, f"user/{user_id}"),
        account=account,
        timeout=30,
    )


@user_app.command(name="purge")
def purge_user(
    ctx: typer.Context,
    user_id: str = typer.Option(
        ...,
        "--user-id",
        "-uid",
        help="User id in keycloak.",
        callback=util.sanitize,
    ),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Purge user from core and IAM."""
    util.delete_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, f"user/{user_id}/purge"),
        account=account,
        timeout=30,
    )


@user_app.command(name="create-key-pair")
def create_key_pair(
    ctx: typer.Context,
    user_nrn: str = typer.Argument(..., callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Create an access key_pair and assign to a user."""
    util.post_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, f"user/{user_nrn}/key_pair"),
        account=account,
        timeout=30,
    )


@user_app.command(name="delete-key-pair")
def delete_key_pair(
    ctx: typer.Context,
    user_nrn: str = typer.Argument(..., callback=util.sanitize),
    access_key_id: str = typer.Argument(..., callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Delete the access key_pair from the user."""
    util.delete_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, f"user/{user_nrn}/key_pair/{access_key_id}"),
        account=account,
        timeout=30,
    )


@user_app.command(name="list")
def list_users(
    ctx: typer.Context,
    search: str = typer.Option(None, help="Search term", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """List existing keycloak users.

    Filter by search term on username, first_name, last_name, or email.
    """
    params = {"search": search} if search else None

    util.get_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, "users"),
        params=params,
        account=account,
    )


@user_app.command(name="permissions")
def user_permissions(
    ctx: typer.Context,
    username: str = typer.Option(None, help="Keycloak username", callback=util.sanitize),
    identifier: UUID = typer.Option(None, help="User or Group identifier", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """List existing keycloak user permissions."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        user_id = identifier

        if username:
            params = {"search": username}
            r = util.get(
                ctx,
                constant.IAM,
                _iam_url(ctx.obj.hub_api_url, "users"),
                params={"search": username},
                account=account,
            )
            if not is_success_response(r):
                process_response(r)

            data = r.json()
            # In case search term matches email/name of another user, filter for specific username
            user_id = next((user["id"] for user in data["users"] if user["username"] == username), None)

        if user_id is None:
            typer.echo("User not found.")
            raise typer.Exit(code=1)

        params = {"user_nrn": user_id}
        return util.get(
            ctx,
            constant.IAM,
            "{iam_url}".format(iam_url=_iam_url(ctx.obj.hub_api_url, "policy/user")),
            params=params,
            account=account,
        )

    r = _request(ctx)
    process_response(r, output_format=ctx.obj.output_format)


@user_app.command(name="reset-password")
def reset_password(
    ctx: typer.Context,
    username: str = typer.Argument(..., help="Keycloak user `username`", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Request a password reset for a user."""
    util.post_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, "user/password/reset"),
        params={"username": username},
    )


@group_app.command(name="create")
def create_group(
    ctx: typer.Context,
    name: str = typer.Option(..., help="Group name", callback=util.sanitize),
    description: str = typer.Option(..., help="Group description", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Create an IAM group."""
    group = schema.CreateUpdateGroup(name=name, description=description)

    util.post_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, "group"),
        json=group.model_dump(mode="json"),
        account=account,
    )


@group_app.command(name="update")
def update_group(
    ctx: typer.Context,
    identifier: UUID = typer.Argument(..., help="Group identifier", callback=util.sanitize),
    name: str = typer.Option(..., help="Group name", callback=util.sanitize),
    description: str = typer.Option(..., help="Group description", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update an IAM group."""
    group = schema.CreateUpdateGroup(name=name, description=description)

    util.post_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, f"group/{identifier}"),
        json=group.model_dump(mode="json"),
        account=account,
    )


@group_app.command(name="list")
def list_groups(
    ctx: typer.Context,
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """List IAM groups."""
    util.get_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, "group"),
        account=account,
    )


@group_app.command(name="get")
def get_group(
    ctx: typer.Context,
    identifier: UUID = typer.Argument(..., help="Group identifier", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get an IAM group."""
    util.get_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, f"group/{identifier}"),
        account=account,
    )


@group_app.command(name="delete")
def delete_group(
    ctx: typer.Context,
    identifier: UUID = typer.Argument(..., help="Group identifier", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Delete an IAM group."""
    util.delete_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, f"group/{identifier}"),
        account=account,
    )


@group_app.command(name="add-principals")
def add_principals(
    ctx: typer.Context,
    identifier: UUID = typer.Argument(..., help="Group identifier", callback=util.sanitize),
    principals: list[str] = typer.Option(
        ...,
        "--principal",
        "-p",
        help="Principal identifiers",
        callback=util.sanitize,
    ),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Add principal(s) to an IAM group."""
    update = schema.Principals(principals=principals)

    util.post_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, f"group/{identifier}/principals"),
        json=update.model_dump(mode="json"),
        account=account,
    )


@group_app.command(name="remove-principals")
def remove_principals(
    ctx: typer.Context,
    identifier: UUID = typer.Argument(..., help="Group identifier", callback=util.sanitize),
    principals: list[str] = typer.Option(
        ...,
        "--principal",
        "-p",
        help="Principal identifiers",
        callback=util.sanitize,
    ),
    account: typing.Optional[str] = ACCOUNT_OPT,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Remove principal(s) from an IAM group."""
    update = schema.Principals(principals=principals)

    util.delete_and_process(
        ctx,
        constant.IAM,
        _iam_url(ctx.obj.hub_api_url, f"group/{identifier}/principals"),
        json=update.model_dump(mode="json"),
        account=account,
    )
