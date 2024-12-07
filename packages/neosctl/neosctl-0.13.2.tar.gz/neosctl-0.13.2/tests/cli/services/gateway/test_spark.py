from tests.helper import render_cmd_output

ZERO_ID = "00000000-0000-0000-0000-000000000000"
URL_IDENTIFIED_PREFIX = f"https://core-gateway/api/gateway/v2/spark/{ZERO_ID}"


def test_spark_status(cli_runner, httpx_mock):
    response_payload = {"status": "success"}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}?suffix=latest",
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "spark", "status", ZERO_ID],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_spark_status_previous_status(cli_runner, httpx_mock):
    response_payload = {"status": "success"}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}?suffix=older",
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "spark", "status", "-s", "older", ZERO_ID],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_spark_status_previous_run_status(cli_runner, httpx_mock):
    response_payload = {"status": "success"}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}?suffix=older&run=1234",
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "spark", "status", "-s", "older", "-r", "1234", ZERO_ID],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_spark_log(cli_runner, httpx_mock):
    response_payload = {"logs": []}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/log?suffix=latest",
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "spark", "log", ZERO_ID],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_spark_log_previous(cli_runner, httpx_mock):
    response_payload = {"logs": []}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/log?suffix=older",
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "spark", "log", "-s", "older", ZERO_ID],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_spark_log_previous_run(cli_runner, httpx_mock):
    response_payload = {"logs": []}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/log?suffix=older&run=1234",
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "spark", "log", "-s", "older", "-r", "1234", ZERO_ID],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_spark_history(cli_runner, httpx_mock):
    response_payload = {"logs": []}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/history",
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "spark", "history", ZERO_ID],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_spark_history_with_suffix(cli_runner, httpx_mock):
    response_payload = {"logs": []}
    httpx_mock.add_response(
        method="GET",
        url=f"{URL_IDENTIFIED_PREFIX}/history/abc",
        json=response_payload,
    )

    result = cli_runner.invoke(
        ["gateway", "spark", "history", ZERO_ID, "-s", "abc"],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)
