"""Gateway data product commands."""

from typing import Optional

import typer

from neosctl import constant, util
from neosctl.services.gateway import entity, schema

app = typer.Typer(name="data_product")


def _data_product_url(ctx: typer.Context) -> str:
    return "{}/v2/data_product".format(ctx.obj.gateway_api_url.rstrip("/"))


def _identified_data_product_url(ctx: typer.Context, identifier: str) -> str:
    return "{}/v2/data_product/{}".format(
        ctx.obj.gateway_api_url.rstrip("/"),
        identifier,
    )


arg_generator = entity.EntityArgGenerator("Data Product")


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
    """Create data product."""
    entity.create_entity(
        ctx=ctx,
        url=_data_product_url(ctx=ctx),
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
    """List data products."""
    entity.list_entities(ctx=ctx, url=_data_product_url(ctx=ctx))


@app.command(name="get")
def get_entity(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product."""
    entity.get_entity(
        ctx=ctx,
        url=_data_product_url(ctx=ctx),
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
    """Delete data product."""
    entity.delete_entity(
        ctx=ctx,
        url=_data_product_url(ctx=ctx),
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
    """Get data product info."""
    entity.get_entity_info(
        ctx=ctx,
        url=_data_product_url(ctx=ctx),
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
    """Update data product."""
    entity.update_entity(
        ctx=ctx,
        url=_data_product_url(ctx=ctx),
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
    """Update data product info."""
    entity.update_entity_info(
        ctx=ctx,
        url=_data_product_url(ctx=ctx),
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
    """Get data product journal."""
    entity.get_entity_journal(
        ctx=ctx,
        url=_data_product_url(ctx=ctx),
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
    """Update data product journal."""
    entity.update_entity_journal(
        ctx=ctx,
        url=_data_product_url(ctx=ctx),
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
    """Get data product links."""
    entity.get_entity_links(
        ctx=ctx,
        url=_data_product_url(ctx=ctx),
        identifier=identifier,
    )


@app.command(name="get-metadata")
def get_entity_metadata(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product metadata."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/metadata",
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
    """Update data product metadata."""
    data = util.load_object(schema.UpdateEntityMetadataRequest, filepath, "metadata")

    util.put_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/metadata",
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
    """Delete data product metadata."""
    data = util.load_object(schema.DeleteEntityMetadataRequest, filepath, "metadata")

    util.delete_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/metadata",
        json=data.model_dump(by_alias=True),
    )


@app.command(name="update-schema")
def update_entity_schema(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Filepath to schema description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data product schema."""
    data = util.load_object(schema.UpdateDataProductSchema, filepath, "schema")

    util.put_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/schema",
        json=data.model_dump(by_alias=True),
        timeout=20,
    )


@app.command(name="get-schema")
def get_entity_schema(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product schema."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/schema",
    )


@app.command(name="get-expectation-rules")
def get_entity_expectation_rules(
    ctx: typer.Context,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product expectation rules."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_data_product_url(ctx)}/expectation/rules",
    )


@app.command(name="get-expectation")
def get_entity_expectation(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    *,
    last_only: bool = typer.Option(
        False,
        "--last-only",
        "-l",
        help="Return only last settings.",
        callback=util.sanitize,
    ),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product expectation settings."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/quality/expectation?last_only={last_only}",
    )


@app.command(name="create-expectation-custom")
def create_expectation_custom(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Filepath to custom expectation description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Add data product custom expectation."""
    data = util.load_object(schema.ExpectationItem, filepath, "custom expectation")
    util.post_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/quality/expectation/custom",
        json=data.model_dump(by_alias=True),
    )


@app.command(name="update-expectation-custom")
def update_expectation_custom(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    custom_identifier: str = typer.Argument(..., help="Custom expectation identifier", callback=util.sanitize),
    filepath: str = typer.Argument(..., help="Filepath to custom expectation description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data product custom expectation."""
    data = util.load_object(schema.ExpectationItem, filepath, "custom expectation")
    util.put_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/quality/expectation/custom/{custom_identifier}",
        json=data.model_dump(by_alias=True),
    )


@app.command(name="delete-expectation-custom")
def delete_expectation_custom(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    custom_identifier: str = typer.Argument(..., help="Custom expectation identifier", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Delete data product custom expectation."""
    util.delete_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/quality/expectation/custom/{custom_identifier}",
    )


@app.command(name="update-expectation-weights")
def update_expectation_weights(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Filepath to expectation weights description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data product expectation weights."""
    data = util.load_object(schema.ExpectationWeights, filepath, "expectation weights")
    util.put_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/quality/expectation/weights",
        json=data.model_dump(by_alias=True),
    )


@app.command(name="update-expectation-thresholds")
def update_expectation_thresholds(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Filepath to expectation thresholds description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data product expectation thresholds."""
    data = util.load_object(schema.ExpectationThresholds, filepath, "expectation thresholds")
    util.put_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/quality/expectation/thresholds",
        json=data.model_dump(by_alias=True),
    )


@app.command(name="get-quality-profiling")
def get_entity_quality_profiling(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product profiling."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/quality/profiling",
    )


@app.command(name="get-quality-validations")
def get_entity_quality_validations(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product validations."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/quality/validations",
    )


@app.command(name="get-classification-rule")
def get_data_product_classification_rule(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product classification rule."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/classification/rule",
    )


@app.command(name="update-classification-rule")
def update_data_product_classification_rule(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Filepath to classification rule description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data product classification rule."""
    data = util.load_object(schema.ClassificationRule, filepath, "classification rule")
    util.put_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/classification/rule",
        json=data.model_dump(by_alias=True),
    )


@app.command(name="get-classification-result")
def get_data_product_classification_result(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product classification result."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/classification/result",
    )


@app.command(name="update-classification-result")
def update_data_product_classification_result(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Filepath to classification rule description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data product classification result."""
    data = util.load_object(schema.UpdateClassificationResult, filepath, "classification result")
    util.put_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/classification/result",
        json=data.model_dump(by_alias=True),
    )


@app.command(name="get-lineage")
def get_entity_lineage(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product lineage."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/lineage",
    )


@app.command(name="get-data")
def get_entity_data(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product data."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/data",
    )


@app.command(name="delete-data")
def delete_entity_data(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Delete data product data."""
    util.delete_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/data",
    )


@app.command(name="publish")
def publish_entity(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    *,
    private: bool = typer.Option(
        False,
        "--private",
        help="Limit visibility in mesh to core account.",
        callback=util.sanitize,
    ),
    approval_required: bool = typer.Option(
        False,
        "--approval-required",
        help="Require approval before a subscription is finalised.",
        callback=util.sanitize,
    ),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Publish data product."""
    util.post_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/publish",
        json={
            "contract": {
                "visibility": "private" if private else "public",
                "subscription": {"approval": approval_required},
            },
        },
    )


@app.command(name="unpublish")
def unpublish_entity(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Unpublish data product."""
    util.delete_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/publish",
    )


@app.command(name="update-spark-file")
def update_entity_spark_file(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Spark job filepath", callback=util.sanitize),
    secrets: Optional[list[str]] = typer.Option(None, "--secret", "-s", help="Secret identifier"),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data product spark file."""
    fp = util.get_file_location(filepath)

    with fp.open("rb") as f:
        util.put_and_process(
            ctx,
            constant.GATEWAY,
            f"{_identified_data_product_url(ctx, identifier)}/spark/file",
            files={"spark_file": f},
            params={"secret_identifiers": secrets} if secrets else None,
        )


@app.command(name="get-builder")
def get_entity_builder(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product builder."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/spark/builder",
        sort_keys=False,
    )


@app.command(name="get-spark-lineage")
def get_entity_spark_lineage(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product spark lineage."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/spark/lineage",
    )


@app.command(name="get-builder-state")
def get_entity_builder_state(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get data product builder state."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/spark/builder/state",
    )


@app.command(name="update-builder")
def update_entity_builder(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Filepath to builder description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data product builder."""
    data = util.load_object(schema.BuilderPipeline, filepath, "builder")
    util.put_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/spark/builder",
        json=data.model_dump(by_alias=True),
        timeout=20,
    )


@app.command(name="update-spark-state")
def update_entity_spark_state(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Filepath to spark state description", callback=util.sanitize),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Update data product spark state."""
    data = util.load_object(schema.UpdateSparkState, filepath, "state")
    util.put_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_data_product_url(ctx, identifier)}/spark/state",
        json=data.model_dump(by_alias=True),
    )
