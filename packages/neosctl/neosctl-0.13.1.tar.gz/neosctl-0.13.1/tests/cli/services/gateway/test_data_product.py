import json
from unittest import mock
from uuid import uuid4

from neosctl.services.gateway import data_product, schema
from tests.cli.services.gateway.util import get_journal_note_filepath
from tests.conftest import FakeContext
from tests.helper import render_cmd_output

ZERO_ID = "00000000-0000-0000-0000-000000000000"
URL_PREFIX = "https://core-gateway/api/gateway/v2/data_product"
URL_IDENTIFIED_PREFIX = f"https://core-gateway/api/gateway/v2/data_product/{ZERO_ID}"


def test_data_product_list(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_product.entity, "list_entities", mocked)
    cli_runner.invoke(["gateway", "data-product", "list"])

    mocked.assert_called_once_with(ctx=FakeContext(), url=URL_PREFIX)


def test_data_product_create(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_product.entity, "create_entity", mocked)
    cli_runner.invoke(["gateway", "data-product", "create", "LBL", "name", "description"])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        label="LBL",
        name="name",
        description="description",
        owner=None,
        contacts=[],
        links=[],
    )


def test_data_product_get(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_product.entity, "get_entity", mocked)
    cli_runner.invoke(["gateway", "data-product", "get", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_product_delete(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_product.entity, "delete_entity", mocked)
    cli_runner.invoke(["gateway", "data-product", "delete", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_product_get_info(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_product.entity, "get_entity_info", mocked)
    cli_runner.invoke(["gateway", "data-product", "get-info", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_product_update(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_product.entity, "update_entity", mocked)
    cli_runner.invoke(
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

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        label="AAA",
        name="new name",
        description="new description",
    )


def test_data_product_update_info(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_product.entity, "update_entity_info", mocked)
    cli_runner.invoke(
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

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        contacts=["contact"],
        links=["link 1", "link 2"],
        owner="owner",
    )


def test_data_product_get_journal(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_product.entity, "get_entity_journal", mocked)
    cli_runner.invoke(["gateway", "data-product", "get-journal", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        page=1,
        per_page=25,
    )


def test_data_product_update_journal(cli_runner, monkeypatch, tmp_path):
    filepath = get_journal_note_filepath(tmp_path)

    mocked = mock.Mock()
    monkeypatch.setattr(data_product.entity, "update_entity_journal", mocked)

    cli_runner.invoke(["gateway", "data-product", "update-journal", ZERO_ID, filepath])
    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
        filepath=filepath,
    )


def test_data_product_get_links(cli_runner, monkeypatch):
    mocked = mock.Mock()
    monkeypatch.setattr(data_product.entity, "get_entity_links", mocked)
    cli_runner.invoke(["gateway", "data-product", "get-links", ZERO_ID])

    mocked.assert_called_once_with(
        ctx=FakeContext(),
        url=URL_PREFIX,
        identifier=ZERO_ID,
    )


def test_data_product_get_metadata(cli_runner, httpx_mock):
    response_payload = {
        "identifier": "3c8e9b8e-d623-4084-830f-2f99562c3b94",
        "name": "data",
        "description": "string",
        "owner": "string",
        "created": "2023-07-18T07:30:09.258479+00:00",
        "last_updated": "2023-07-27T09:34:47.568830+00:00",
        "is_active": True,
        "update_frequency": None,
        "quality": "N/A",
        "schema": [],
        "core_id": "168750762250",
        "lineage": {},
        "relates_to": [],
        "tags": [],
        "rows": None,
        "columns": None,
        "data_profiling": None,
        "data_quality": [],
        "data_quality_score": None,
        "data_quality_scores_by_dimension": None,
    }
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/metadata",
        json=response_payload,
    )
    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-metadata",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_update_metadata(cli_runner, httpx_mock, tmp_path):
    response_payload = {}
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/metadata",
        json=response_payload,
    )

    fp = tmp_path / "metadata_update.json"
    with fp.open("w") as f:
        json.dump(
            schema.UpdateEntityMetadataRequest(
                tags=["top-secret"],
                fields={
                    "field": schema.FieldMetadata(tags=["secret"], description=None),
                },
            ).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "update-metadata",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_delete_metadata(cli_runner, httpx_mock, tmp_path):
    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url=f"{URL_IDENTIFIED_PREFIX}/metadata",
        json=response_payload,
    )

    fp = tmp_path / "metadata_update.json"
    with fp.open("w") as f:
        json.dump(
            schema.DeleteEntityMetadataRequest(
                tags=["top-secret"],
                fields={
                    "field": schema.FieldMetadata(tags=["secret"], description=None),
                },
            ).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "delete-metadata",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_update_schema(cli_runner, httpx_mock, tmp_path):
    response_payload = {
        "fields": [
            {
                "data_type": {"column_type": "VARCHAR", "meta": {}},
                "description": "string",
                "name": "foo",
                "optional": False,
                "primary": True,
                "tags": [],
            },
        ],
    }
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/schema",
        json=response_payload,
    )

    fp = tmp_path / "schema_update.json"
    with fp.open("w") as f:
        json.dump(
            schema.UpdateDataProductSchema(
                details=schema.StoredDataProductSchema(
                    product_type="stored",
                    fields=[
                        schema.CreateFieldDefinition(
                            name="foo",
                            description="string",
                            primary=True,
                            optional=False,
                            data_type=schema.FieldDataType(
                                meta={},
                                column_type="VARCHAR",
                            ),
                        ),
                    ],
                ),
            ).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "update-schema",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_get_schema(cli_runner, httpx_mock):
    response_payload = {
        "fields": [
            {
                "data_type": {"column_type": "VARCHAR", "meta": {}},
                "description": "string",
                "name": "foo",
                "optional": False,
                "primary": True,
                "tags": [],
            },
        ],
    }
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/schema",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-schema",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_get_expectation_rules(cli_runner, httpx_mock):
    response_payload = {
        "rules": [
            {
                "category": "accuracy",
                "critically": 2,
                "description": "Expect each column value to be in a given set.",
                "expectation_type": "expect_column_values_to_be_in_set",
                "level": "column",
                "parameters": [
                    {
                        "default": None,
                        "description": "The column name.",
                        "name": "column",
                        "required": True,
                        "type": "str",
                    },
                    {
                        "default": None,
                        "description": "A set of objects used for comparison.",
                        "name": "value_set",
                        "required": True,
                        "type": "set-like",
                    },
                ],
            },
        ],
    }
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_PREFIX}/expectation/rules",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-expectation-rules",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_get_quality_expectation(cli_runner, httpx_mock):
    response_payload = {
        "results": [],
    }
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/quality/expectation?last_only=False",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-expectation",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_create_expectation_custom(cli_runner, httpx_mock, tmp_path):
    response_payload = {
        "created_at": "2023-05-26T09:41:31.585983+00:00",
        "entity": "entity",
        "expectations": {
            "auto": [],
            "custom": [
                {
                    "expectation_type": "expect_column_values_to_be_between",
                    "kwargs": {"column": "year", "min_value": 1980, "max_value": 2020},
                    "meta": {
                        "description": "Expect a year min max values 111",
                        "id": "00000000-0000-0000-0000-000000000000",
                    },
                },
            ],
        },
        "id": ZERO_ID,
        "thresholds": None,
        "weights": None,
    }
    httpx_mock.add_response(
        method="POST",
        url=f"{URL_IDENTIFIED_PREFIX}/quality/expectation/custom",
        json=response_payload,
    )

    fp = tmp_path / "schema_update.json"
    with fp.open("w") as f:
        json.dump(
            schema.ExpectationItem(
                expectation_type="expect_column_values_to_be_between",
                kwargs={"column": "year", "min_value": 1980, "max_value": 2020},
                meta={"description": "Expect a year min max values 111"},
            ).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "create-expectation-custom",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_update_expectation_custom(cli_runner, httpx_mock, tmp_path):
    response_payload = {
        "created_at": "2023-05-26T09:41:31.585983+00:00",
        "entity": "entity",
        "expectations": {
            "auto": [],
            "custom": [
                {
                    "expectation_type": "expect_column_values_to_be_between",
                    "kwargs": {"column": "year", "min_value": 1980, "max_value": 2020},
                    "meta": {
                        "description": "Expect a year min max values 111",
                        "id": ZERO_ID,
                    },
                },
            ],
        },
        "id": ZERO_ID,
        "thresholds": None,
        "weights": None,
    }
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/quality/expectation/custom/{ZERO_ID}",
        json=response_payload,
    )

    fp = tmp_path / "schema_update.json"
    with fp.open("w") as f:
        json.dump(
            schema.ExpectationItem(
                expectation_type="expect_column_values_to_be_between",
                kwargs={"column": "year", "min_value": 1980, "max_value": 2020},
                meta={
                    "description": "Expect a year min max values 111",
                    "id": "00000000-0000-0000-0000-000000000000",
                },
            ).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "update-expectation-custom",
            ZERO_ID,
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_delete_expectation_custom(cli_runner, httpx_mock):
    response_payload = {
        "created_at": "2023-05-26T09:41:31.585983+00:00",
        "entity": "entity",
        "expectations": {
            "auto": [],
            "custom": [],
        },
        "id": ZERO_ID,
        "thresholds": None,
        "weights": None,
    }
    httpx_mock.add_response(
        method="DELETE",
        url=f"{URL_IDENTIFIED_PREFIX}/quality/expectation/custom/{ZERO_ID}",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "delete-expectation-custom",
            ZERO_ID,
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_update_expectation_weights(cli_runner, httpx_mock, tmp_path):
    response_payload = {
        "created_at": "2023-05-26T09:41:31.585983+00:00",
        "entity": "entity",
        "expectations": {
            "auto": [],
            "custom": [],
        },
        "id": ZERO_ID,
        "thresholds": None,
        "weights": {"accuracy": 0.2, "completeness": 0.3, "consistency": 0.1, "uniqueness": 0.1, "validity": 0.3},
    }
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/quality/expectation/weights",
        json=response_payload,
    )

    fp = tmp_path / "schema_update.json"
    with fp.open("w") as f:
        json.dump(
            schema.ExpectationWeights(
                accuracy=0.2,
                completeness=0.3,
                consistency=0.1,
                uniqueness=0.1,
                validity=0.3,
            ).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "update-expectation-weights",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_update_expectation_thresholds(cli_runner, httpx_mock, tmp_path):
    response_payload = {
        "created_at": "2023-05-26T09:41:31.585983+00:00",
        "entity": "entity",
        "expectations": {
            "auto": [],
            "custom": [],
        },
        "id": ZERO_ID,
        "thresholds": {"table": 0.8, "columns": {}},
        "weights": None,
    }
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/quality/expectation/thresholds",
        json=response_payload,
    )

    fp = tmp_path / "schema_update.json"
    with fp.open("w") as f:
        json.dump(
            schema.ExpectationThresholds(table=0.8, columns={}).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "update-expectation-thresholds",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_get_quality_profiling(cli_runner, httpx_mock):
    response_payload = {
        "results": [],
    }
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/quality/profiling",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-quality-profiling",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_get_quality_validations(cli_runner, httpx_mock):
    response_payload = {
        "results": [],
    }
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/quality/validations",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-quality-validations",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_get_classification_rule(cli_runner, httpx_mock):
    response_payload = {
        "excluded_columns": [],
        "model": "",
        "regex_recognizers": [
            {
                "description": "Description goes here...",
                "label": "SUPER",
                "name": "Super recognizer",
                "patterns": [".*(super).*"],
            },
        ],
    }
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/classification/rule",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-classification-rule",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_update_classification_rule(cli_runner, httpx_mock, tmp_path):
    response_payload = {
        "excluded_columns": [],
        "model": "",
        "regex_recognizers": [
            {
                "description": "New description goes here...",
                "label": "DUPER",
                "name": "Updated super recognizer",
                "patterns": [".*(super).*"],
            },
        ],
    }
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/classification/rule",
        json=response_payload,
    )

    fp = tmp_path / "classification_rule_update.json"
    with fp.open("w") as f:
        json.dump(
            schema.ClassificationRule(
                model="",
                excluded_columns=[],
                regex_recognizers=[
                    schema.ClassificationRegexRecognizer(
                        name="Updated super recognizer",
                        description="New description goes here...",
                        label="DUPER",
                        patterns=[".*(super).*"],
                    ),
                ],
            ).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "update-classification-rule",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_get_classification_result(cli_runner, httpx_mock):
    response_payload = {
        "results": [
            {
                "config": {},
                "created_at": "2023-09-06T10:53:16.278324Z",
                "field": "foo",
                "identifier": "78077a80-795e-4f4d-8248-c9547ae9fdb7",
                "label": "WORD",
                "resolved": False,
                "updated_at": "2023-09-06T10:53:16.278324Z",
            },
            {
                "config": {},
                "created_at": "2023-09-06T10:53:16.278324Z",
                "field": "year",
                "identifier": "fad47d6c-656c-4bc9-8252-c1010018514d",
                "label": "YEAR",
                "resolved": False,
                "updated_at": "2023-09-06T10:53:16.278324Z",
            },
        ],
    }
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/classification/result",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-classification-result",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_update_classification_result(cli_runner, httpx_mock, tmp_path):
    response_payload = {
        "results": [
            {
                "config": {},
                "created_at": "2023-09-06T10:53:16.278324Z",
                "field": "year",
                "identifier": "fad47d6c-656c-4bc9-8252-c1010018514d",
                "label": "YEAR",
                "resolved": True,
                "updated_at": "2023-09-06T12:22:08.853038Z",
            },
        ],
    }
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/classification/result",
        json=response_payload,
    )

    fp = tmp_path / "classification_result_update.json"
    with fp.open("w") as f:
        json.dump(
            schema.UpdateClassificationResult(
                resolve=["00000000-0000-0000-0000-000000000000"],
            ).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "update-classification-result",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_get_spark_lineage(cli_runner, httpx_mock):
    response_payload = {"ok": True, "directed": True, "multigraph": False, "graph": {}, "nodes": [], "links": []}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/spark/lineage",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-spark-lineage",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_get_lineage(cli_runner, httpx_mock):
    response_payload = {"ok": True, "directed": True, "multigraph": False, "graph": {}, "nodes": [], "links": []}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/lineage",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-lineage",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_get_data(cli_runner, httpx_mock):
    response_payload = {"results": []}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/data",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-data",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_delete_data(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url=f"{URL_IDENTIFIED_PREFIX}/data",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "delete-data",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_publish(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="POST",
        url=f"{URL_IDENTIFIED_PREFIX}/publish",
        json=response_payload,
        match_content=b'{"contract": {"visibility": "public", "subscription": {"approval": false}}}',
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "publish",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_publish_private(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="POST",
        url=f"{URL_IDENTIFIED_PREFIX}/publish",
        json=response_payload,
        match_content=b'{"contract": {"visibility": "private", "subscription": {"approval": false}}}',
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "publish",
            ZERO_ID,
            "--private",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_publish_approval_required(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="POST",
        url=f"{URL_IDENTIFIED_PREFIX}/publish",
        json=response_payload,
        match_content=b'{"contract": {"visibility": "public", "subscription": {"approval": true}}}',
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "publish",
            ZERO_ID,
            "--approval-required",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_unpublish(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url=f"{URL_IDENTIFIED_PREFIX}/publish",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "unpublish",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_update_spark_file(cli_runner, httpx_mock, tmp_path):
    response_payload = {}
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/spark/file",
        json=response_payload,
    )

    fp = tmp_path / "job.spark"
    with fp.open("w") as f:
        f.write("print('hello')")

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "update-spark-file",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_update_spark_file_with_secrets(cli_runner, httpx_mock, tmp_path):
    s1 = uuid4()
    s2 = uuid4()
    response_payload = {}
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/spark/file?secret_identifiers={s1}&secret_identifiers={s2}",
        json=response_payload,
    )

    fp = tmp_path / "job.spark"
    with fp.open("w") as f:
        f.write("print('hello')")

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "update-spark-file",
            ZERO_ID,
            str(fp.resolve()),
            "-s",
            str(s1),
            "-s",
            str(s2),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_get_builder(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/spark/builder",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-builder",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_get_builder_state(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/spark/builder/state",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "get-builder-state",
            ZERO_ID,
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_update_builder(cli_runner, httpx_mock, tmp_path):
    response_payload = {}
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/spark/builder",
        json=response_payload,
    )

    fp = tmp_path / "builder.json"
    with fp.open("w") as f:
        json.dump(
            schema.BuilderPipeline(
                config={},
                inputs={},
                transformations=[],
                finalisers={},
                preview=False,
            ).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "update-builder",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_data_product_update_sparl_state(cli_runner, httpx_mock, tmp_path):
    response_payload = {}
    httpx_mock.add_response(
        method="PUT",
        url=f"{URL_IDENTIFIED_PREFIX}/spark/state",
        json=response_payload,
    )

    fp = tmp_path / "spark_state.json"
    with fp.open("w") as f:
        json.dump(
            schema.UpdateSparkState(
                state={"state": "remove_job", "force": True},
            ).model_dump(),
            f,
        )

    result = cli_runner.invoke(
        [
            "gateway",
            "data-product",
            "update-spark-state",
            ZERO_ID,
            str(fp.resolve()),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)
