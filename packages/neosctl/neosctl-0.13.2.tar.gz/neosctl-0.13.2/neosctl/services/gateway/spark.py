"""Gateway spark commands."""

from typing import Optional

import typer

from neosctl import constant, util

app = typer.Typer(name="output")


def _identified_spark_url(ctx: typer.Context, identifier: str) -> str:
    return "{}/v2/spark/{}".format(
        ctx.obj.gateway_api_url.rstrip("/"),
        identifier,
    )


IDENTIFIER_ARGUMENT = typer.Argument(..., help="Spark identifier", callback=util.sanitize)


@app.command(name="status")
def element_status(
    ctx: typer.Context,
    identifier: str = IDENTIFIER_ARGUMENT,
    suffix: Optional[str] = typer.Option("latest", "--suffix", "-s", help="Job run suffix"),
    run: Optional[str] = typer.Option(None, "--run", "-r", help="Job run"),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get spark status."""
    params = {"suffix": suffix}
    if run is not None:
        params["run"] = run
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_spark_url(ctx, identifier)}",
        params=params,
    )


@app.command(name="log")
def element_log(
    ctx: typer.Context,
    identifier: str = IDENTIFIER_ARGUMENT,
    suffix: Optional[str] = typer.Option("latest", "--suffix", "-s", help="Job run suffix"),
    run: Optional[str] = typer.Option(None, "--run", "-r", help="Job run"),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get spark logs."""
    params = {"suffix": suffix}
    if run is not None:
        params["run"] = run
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        f"{_identified_spark_url(ctx, identifier)}/log",
        params=params,
    )


@app.command(name="history")
def element_history(
    ctx: typer.Context,
    identifier: str = IDENTIFIER_ARGUMENT,
    suffix: Optional[str] = typer.Option(None, "--suffix", "-s", help="Job run suffix"),
    _fields: util.Fields = None,
    _output: util.Output = constant.Output.json.value,
    _verbose: util.Verbosity = 0,
) -> None:
    """Get spark history."""
    if suffix:
        util.get_and_process(
            ctx,
            constant.GATEWAY,
            f"{_identified_spark_url(ctx, identifier)}/history/{suffix}",
        )
    else:
        util.get_and_process(
            ctx,
            constant.GATEWAY,
            f"{_identified_spark_url(ctx, identifier)}/history",
        )
