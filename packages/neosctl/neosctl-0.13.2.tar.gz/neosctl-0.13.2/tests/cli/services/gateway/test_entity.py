import typer

from neosctl.services.gateway import entity
from tests.cli.services.gateway.util import get_journal_note_filepath
from tests.helper import render_cmd_output

ZERO_ID = "00000000-0000-0000-0000-000000000000"
BASE_DATA_PRODUCT_URL = "https://core-gateway/api/gateway/v2/data_product"
SOME_DATA_PRODUCT_URL = f"https://core-gateway/api/gateway/v2/data_product/{ZERO_ID}"

INFO_EXAMPLE = {"label": "ABC", "owner": None, "contact_ids": [], "links": [], "notes": None}


class TestEntityArgGenerator:
    generator = entity.EntityArgGenerator("Entity")

    def test_identifier(self):
        assert self.generator.identifier.help == "Entity identifier"
        assert isinstance(self.generator.identifier, typer.models.ArgumentInfo)

    def test_name(self):
        assert self.generator.name.help == "Entity name"
        assert isinstance(self.generator.name, typer.models.ArgumentInfo)

    def test_label(self):
        assert self.generator.label.help == "Entity label"
        assert isinstance(self.generator.label, typer.models.ArgumentInfo)

    def test_description(self):
        assert self.generator.description.help == "Entity description"
        assert isinstance(self.generator.description, typer.models.ArgumentInfo)

    def test_note(self):
        assert self.generator.note.help == "Entity note"
        assert isinstance(self.generator.note, typer.models.ArgumentInfo)

    def test_owner(self):
        assert self.generator.owner.help == "Entity owner"
        assert isinstance(self.generator.owner, typer.models.OptionInfo)

    def test_owner_optional(self):
        assert self.generator.owner_optional.help == "Entity owner"
        assert isinstance(self.generator.owner_optional, typer.models.OptionInfo)

    def test_contacts(self):
        assert self.generator.contacts.help == "Entity contact IDs"
        assert isinstance(self.generator.contacts, typer.models.OptionInfo)

    def test_links(self):
        assert self.generator.links.help == "Entity links"
        assert isinstance(self.generator.links, typer.models.OptionInfo)


def test_list_entities(cli_runner, httpx_mock):
    response_payload = {
        "entities": [
            {
                "identifier": "9cc29604-cc0b-490d-ba2f-9c945c9a393c",
                "urn": "urn:ksa:core:168415628435:root:data_product:9cc29604-cc0b-490d-ba2f-9c945c9a393c",
                "name": "product_name",
                "description": "a description",
                "label": "ABC",
                "state": {"state": "Created.", "healthy": True},
            },
        ],
    }
    httpx_mock.add_response(
        method="GET",
        url=BASE_DATA_PRODUCT_URL,
        json=response_payload,
    )

    result = cli_runner.invoke(["gateway", "data-product", "list"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload["entities"])


def test_create_entity(cli_runner, httpx_mock):
    response_payload = {
        "description": "description",
        "identifier": "d953d89c-f85c-4a78-8f62-7161b07431e7",
        "label": "LBL",
        "name": "name",
        "urn": "urn:ksa:core:168415628435:root:data_product:d953d89c-f85c-4a78-8f62-7161b07431e7",
    }
    httpx_mock.add_response(
        method="POST",
        url=BASE_DATA_PRODUCT_URL,
        json=response_payload,
    )

    result = cli_runner.invoke(["gateway", "data-product", "create", "LBL", "name", "description"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_create_entity_with_info(cli_runner, httpx_mock):
    response_payload = {
        "description": "description",
        "identifier": ZERO_ID,
        "label": "LBL",
        "name": "name",
        "urn": f"urn:ksa:core:168415628435:root:data_product:{ZERO_ID}",
    }
    httpx_mock.add_response(
        method="POST",
        url=BASE_DATA_PRODUCT_URL,
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "create",
            "LBL",
            "name",
            "description",
            "--owner",
            "owner",
            "-l",
            "link 1",
            "-l",
            "link 2",
            "-c",
            "contact",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_create_entity_with_wrong_info(cli_runner):
    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "create",
            "LBL",
            "name",
            "description",
            "-l",
            "link 1",
            "-l",
            "link 2",
            "-c",
            "contact",
        ],
    )

    assert result.exit_code == 1
    assert result.output == "Set info fields: owner (required), contacts (optional) and links (optional).\n"


def test_get_entity(cli_runner, httpx_mock):
    response_payload = {
        "entity": {
            "description": "description",
            "identifier": ZERO_ID,
            "label": "LBL",
            "name": "name",
            "urn": "urn:ksa:core:168415628435:root:data_product:00000000-0000-0000-0000-000000000000",
        },
        "entity_info": None,
        "links": {"children": [], "parents": []},
        "schema_available": False,
        "spark_identifier": None,
        "table": None,
        "tags": [],
    }
    httpx_mock.add_response(
        method="GET",
        url=SOME_DATA_PRODUCT_URL,
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "data-product", "get", ZERO_ID],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_delete_entity(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url=SOME_DATA_PRODUCT_URL,
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "data-product", "delete", ZERO_ID],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_update_entity(cli_runner, httpx_mock):
    response_payload = {
        "entity": {
            "description": "new description",
            "identifier": ZERO_ID,
            "label": "AAA",
            "name": "new name",
            "urn": "urn:ksa:core:168415628435:root:data_product:00000000-0000-0000-0000-000000000000",
        },
        "entity_info": None,
        "links": {"children": [], "parents": []},
        "schema_available": False,
        "spark_identifier": None,
        "table": None,
        "tags": [],
    }
    httpx_mock.add_response(
        method="PUT",
        url=SOME_DATA_PRODUCT_URL,
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "update",
            ZERO_ID,
            "AAA",
            "new name",
            "new description",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_get_entity_info(cli_runner, httpx_mock):
    response_payload = {"contact_ids": [], "links": [], "owner": "owner"}
    httpx_mock.add_response(
        method="GET",
        url=f"{SOME_DATA_PRODUCT_URL}/info",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-info",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_update_entity_info(cli_runner, httpx_mock):
    response_payload = {"contact_ids": ["contact"], "links": ["link 1", "link 2"], "owner": "owner"}
    httpx_mock.add_response(
        method="PUT",
        url=f"{SOME_DATA_PRODUCT_URL}/info",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "update-info",
            ZERO_ID,
            "--owner",
            "owner",
            "-l",
            "link 1",
            "-l",
            "link 2",
            "-c",
            "contact",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_get_entity_journal(cli_runner, httpx_mock):
    response_payload = {"notes": []}
    httpx_mock.add_response(
        method="GET",
        url=f"{SOME_DATA_PRODUCT_URL}/journal?page=1&per_page=25",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-journal",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_update_entity_journal(cli_runner, httpx_mock, tmp_path):
    response_payload = {"notes": ["my note"]}
    httpx_mock.add_response(
        method="POST",
        url=f"{SOME_DATA_PRODUCT_URL}/journal",
        json=response_payload,
    )

    filepath = get_journal_note_filepath(tmp_path)
    result = cli_runner.invoke(
        ["gateway", "data-product", "update-journal", ZERO_ID, filepath],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_get_entity_links(cli_runner, httpx_mock):
    response_payload = {"children": [], "parents": []}
    httpx_mock.add_response(
        method="GET",
        url=f"{SOME_DATA_PRODUCT_URL}/link",
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "data-product", "get-links", ZERO_ID],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)
