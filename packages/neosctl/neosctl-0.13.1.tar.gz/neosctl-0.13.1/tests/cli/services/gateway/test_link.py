from tests.helper import render_cmd_output

LINK_URL = "https://core-gateway/api/gateway/v2/link/{}/{}/{}/{}"


def test_link_entities(cli_runner, httpx_mock):
    response_payload = {
        "child": {
            "description": "",
            "entity_type": "data_product",
            "identifier": "d953d89c-f85c-4a78-8f62-7161b07431e7",
            "label": "LBL",
            "name": "name",
            "urn": "urn:ksa:core:168415628435:root:data_product:d953d89c-f85c-4a78-8f62-7161b07431e7",
        },
        "parent": {
            "description": "",
            "entity_type": "data_product",
            "identifier": "9cc29604-cc0b-490d-ba2f-9c945c9a393c",
            "label": "ABC",
            "name": "name",
            "urn": "urn:ksa:core:168415628435:root:data_product:9cc29604-cc0b-490d-ba2f-9c945c9a393c",
        },
    }
    httpx_mock.add_response(
        method="POST",
        url=LINK_URL.format(
            "data_product",
            "9cc29604-cc0b-490d-ba2f-9c945c9a393c",
            "data_product",
            "d953d89c-f85c-4a78-8f62-7161b07431e7",
        ),
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "link",
            "create",
            "data_product",
            "9cc29604-cc0b-490d-ba2f-9c945c9a393c",
            "data_product",
            "d953d89c-f85c-4a78-8f62-7161b07431e7",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_link_invalid_entities(cli_runner):
    result = cli_runner.invoke(
        [
            "gateway",
            "link",
            "create",
            "data_product",
            "9cc29604-cc0b-490d-ba2f-9c945c9a393c",
            "data_unit",
            "d953d89c-f85c-4a78-8f62-7161b07431e7",
        ],
    )
    assert result.exit_code == 1


def test_unlink_entities(cli_runner, httpx_mock):
    httpx_mock.add_response(
        method="DELETE",
        url=LINK_URL.format(
            "data_product",
            "9cc29604-cc0b-490d-ba2f-9c945c9a393c",
            "data_product",
            "d953d89c-f85c-4a78-8f62-7161b07431e7",
        ),
        json={},
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "link",
            "delete",
            "data_product",
            "9cc29604-cc0b-490d-ba2f-9c945c9a393c",
            "data_product",
            "d953d89c-f85c-4a78-8f62-7161b07431e7",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output({})
