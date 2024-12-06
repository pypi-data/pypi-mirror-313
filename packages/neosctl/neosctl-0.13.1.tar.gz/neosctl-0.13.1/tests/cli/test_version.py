import importlib.metadata


def test_version(cli_runner):
    result = cli_runner.invoke(["--version"])
    assert result.output == f"neosctl {importlib.metadata.version('neosctl')}\n"
