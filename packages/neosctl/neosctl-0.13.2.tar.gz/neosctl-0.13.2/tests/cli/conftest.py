import pytest


@pytest.fixture(autouse=True)
def _patch_term(monkeypatch):
    """
    Make cli output easier to test
    """
    monkeypatch.setenv("COLUMNS", "80")
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setenv("TERM", "unknown")
