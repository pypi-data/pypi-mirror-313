import json
import uuid

from tests.helper import render_cmd_output


def test_core_register(cli_runner, httpx_mock):
    response_payload = {
        "identifier": "core-identifier",
        "urn": "urn:core",
    }
    httpx_mock.add_response(
        method="POST",
        url="https://hub-host/api/hub/registry/core",
        match_content=b'{"name": "product_name", "public": true}',
        headers={"X-Partition": "ksa", "X-Account": "root"},
        json=response_payload,
    )

    result = cli_runner.invoke(["registry", "core", "register", "ksa", "product_name"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_list_cores(cli_runner, httpx_mock):
    response_payload = {
        "cores": [
            {
                "host": None,
                "name": "local",
                "urn": "urn:ksa:core:166601224459",
            },
            {
                "host": None,
                "name": "my-core",
                "urn": "urn:ksa:core:166601243158",
            },
            {
                "host": None,
                "name": "smartconstruction",
                "urn": "urn:ksa:core:166601412405",
            },
        ],
    }
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/registry/core",
        json=response_payload,
    )

    result = cli_runner.invoke(["registry", "core", "list"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload["cores"])


def test_core_remove(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url="https://hub-host/api/hub/registry/core/identifier",
        json=response_payload,
    )

    result = cli_runner.invoke(["registry", "core", "remove", "--identifier", "identifier"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_core_migrate(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="POST",
        url="https://hub-host/api/hub/registry/core/identifier/migrate",
        match_content=b'{"urn": "urn", "account": "account"}',
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["registry", "core", "migrate", "--identifier", "identifier", "--urn", "urn", "--account", "account"],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_search_products(cli_runner, httpx_mock):
    response_payload = {
        "data_products": [],
    }

    # Hybrid cases
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/registry/data_product/search?search_term=product&keyword_search=false",
        json=response_payload,
    )

    result = cli_runner.invoke(["registry", "product", "search", "product"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload["data_products"])

    result = cli_runner.invoke(["registry", "product", "search", "product", "--hybrid"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload["data_products"])

    # Keyword cases
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/registry/data_product/search?search_term=product&keyword_search=true",
        json=response_payload,
    )

    result = cli_runner.invoke(["registry", "product", "search", "product", "--keyword"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload["data_products"])


def test_get_product(cli_runner, httpx_mock):
    response_payload = {
        "core_urn": "urn:core",
        "name": "data-product-name",
        "urn": "urn:region:core:testing:root:data_product:dp",
        "metadata": {
            "id": {
                "data_type": {
                    "meta": {},
                    "type": "INTEGER",
                },
                "name": "id",
                "description": "A product for smart people",
                "primary": True,
                "optional": False,
                "type": "NUMBER",
                "tags": ["worker"],
            },
        },
    }
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/registry/data_product/urn/urn:region:core:testing:root:data_product:dp",
        json=response_payload,
    )

    result = cli_runner.invoke(["registry", "product", "get", "urn:region:core:testing:root:data_product:dp"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_upsert_contact(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="POST",
        url="https://hub-host/api/hub/registry/core/identifier/contact",
        match_content=b'{"user_id": "5c199653-678a-4c57-b439-2487d674e855", "role": "role"}',
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "registry",
            "core",
            "upsert-contact",
            "--identifier",
            "identifier",
            "--user-id",
            "5c199653-678a-4c57-b439-2487d674e855",
            "--role",
            "role",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_remove_contact(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url="https://hub-host/api/hub/registry/core/identifier/contact",
        match_content=b'{"user_id": "5c199653-678a-4c57-b439-2487d674e855"}',
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "registry",
            "core",
            "remove-contact",
            "--identifier",
            "identifier",
            "--user-id",
            "5c199653-678a-4c57-b439-2487d674e855",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_mesh_cores(cli_runner, httpx_mock):
    response_payload = {
        "cores": [
            {
                "host": None,
                "name": "local",
                "urn": "urn:ksa:core:166601224459",
            },
            {
                "host": None,
                "name": "my-core",
                "urn": "urn:ksa:core:166601243158",
            },
            {
                "host": None,
                "name": "smartconstruction",
                "urn": "urn:ksa:core:166601412405",
            },
        ],
    }
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/registry/mesh/core",
        json=response_payload,
    )

    result = cli_runner.invoke(["registry", "mesh", "cores"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_mesh_cores_search(cli_runner, httpx_mock):
    response_payload = {
        "cores": [
            {
                "host": None,
                "name": "local",
                "urn": "urn:ksa:core:166601224459",
            },
        ],
    }
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/registry/mesh/core?search=local",
        json=response_payload,
    )

    result = cli_runner.invoke(["registry", "mesh", "cores", "--search", "local"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_mesh_core_products(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="GET",
        url="https://hub-host/api/hub/registry/mesh/core/identifier/data_product",
        json=response_payload,
    )

    result = cli_runner.invoke(["registry", "mesh", "core-products", "--identifier", "identifier"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_mesh_subscriptions(cli_runner, httpx_mock):
    response_payload = {
        "subscriptions": [
            {
                "core": {
                    "host": None,
                    "name": "core-name",
                    "urn": f"urn:test:registry::root:core:{uuid.uuid4()!s}",
                    "version": None,
                },
                "data_product": {
                    "name": "dp-name",
                    "urn": "urn:region:core:testing:root:data_product:dp",
                    "metadata": {},
                    "description": "",
                    "core": {
                        "host": None,
                        "name": "core-name",
                        "urn": f"urn:test:registry::root:core:{uuid.uuid4()!s}",
                        "version": None,
                    },
                },
            },
        ],
    }
    httpx_mock.add_response(
        method="get",
        url="https://hub-host/api/hub/registry/mesh/subscriptions",
        headers={"X-Partition": "ksa", "X-Account": "root", "X-Account-Override": "test"},
        json=response_payload,
    )

    result = cli_runner.invoke(["registry", "mesh", "subscriptions", "--account", "test"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_subscribe_data_product(cli_runner, httpx_mock):
    response_payload = {}
    core_id = str(uuid.uuid4())
    dp_id = str(uuid.uuid4())

    body = json.dumps({"data_product_urn": dp_id})

    httpx_mock.add_response(
        method="POST",
        url=f"https://hub-host/api/hub/registry/core/{core_id}/data_product/subscribe",
        headers={"X-Partition": "ksa", "X-Account": "root", "X-Account-Override": "test"},
        match_content=body.encode("utf-8"),
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["registry", "product", "subscribe", "--account", "test", "-cid", core_id, "-pid", dp_id],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_unsubscribe_data_product(cli_runner, httpx_mock):
    response_payload = {}
    core_id = str(uuid.uuid4())
    dp_id = str(uuid.uuid4())

    body = json.dumps({"data_product_urn": dp_id})

    httpx_mock.add_response(
        method="DELETE",
        url=f"https://hub-host/api/hub/registry/core/{core_id}/data_product/subscribe",
        headers={"X-Partition": "ksa", "X-Account": "root", "X-Account-Override": "test"},
        match_content=body.encode("utf-8"),
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["registry", "product", "unsubscribe", "--account", "test", "-cid", core_id, "-pid", dp_id],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_update_subscription(cli_runner, httpx_mock):
    response_payload = {}
    core_id = str(uuid.uuid4())
    subscriber_core_id = str(uuid.uuid4())
    dp_id = str(uuid.uuid4())

    body = json.dumps(
        {
            "data_product_urn": dp_id,
            "subscriber_core_identifier": subscriber_core_id,
            "status": "approved",
            "reason": "reason",
        },
    )

    httpx_mock.add_response(
        method="PUT",
        url=f"https://hub-host/api/hub/registry/core/{core_id}/data_product/subscription",
        headers={"X-Partition": "ksa", "X-Account": "root", "X-Account-Override": "test"},
        match_content=body.encode("utf-8"),
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "registry",
            "product",
            "update-subscription",
            "--account",
            "test",
            "-cid",
            core_id,
            "-pid",
            dp_id,
            "-scid",
            subscriber_core_id,
            "--reason",
            "reason",
            "--status",
            "approved",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)
