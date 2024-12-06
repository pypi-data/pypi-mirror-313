import typer

from neosctl import constant
from neosctl.services.gateway import (
    data_product,
    data_source,
    data_system,
    data_unit,
    journal_note,
    link,
    output,
    secret,
    spark,
    tag,
)

app = typer.Typer(name=constant.GATEWAY)
app.add_typer(data_system.app, name="data-system", help="Manage data system entity.")
app.add_typer(data_source.app, name="data-source", help="Manage data source entity.")
app.add_typer(data_unit.app, name="data-unit", help="Manage data unit entity.")
app.add_typer(data_product.app, name="data-product", help="Manage data product entity.")
app.add_typer(output.app, name="output", help="Manage output entity.")
app.add_typer(link.app, name="link", help="Manage links.")
app.add_typer(secret.app, name="secret", help="Manage secrets.")
app.add_typer(tag.app, name="tag", help="Manage tags.")
app.add_typer(spark.app, name="spark", help="Manage spark job.")
app.add_typer(journal_note.app, name="journal-note", help="Manage journal note element.")
