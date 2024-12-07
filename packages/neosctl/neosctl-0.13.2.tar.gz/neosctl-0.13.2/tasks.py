"""Collection of useful commands for `neosctl` management.

To view a list of available commands:

$ invoke --list
"""

import subprocess

import invoke


def current_branch():
    """Get the current branch from git cli using subprocess."""
    try:
        rev_parse_out = (
            subprocess.check_output(
                [
                    "git",
                    "rev-parse",
                    "--tags",
                    "--abbrev-ref",
                    "HEAD",
                ],
                stderr=subprocess.STDOUT,
            )
            .decode()
            .strip()
            .split("\n")
        )
    except subprocess.CalledProcessError as e:
        msg = "Could not get current branch name."
        raise invoke.exceptions.Exit(msg) from e

    return rev_parse_out[-1]


def enforce_branch(branch_name):
    """Enforce that the current branch matches the supplied branch_name."""
    if current_branch() != branch_name:
        msg = f"Command can not be run outside of {branch_name}."
        raise invoke.exceptions.Exit(msg)


@invoke.task
def install(context):
    """Install production requirements for `neosctl`."""
    context.run("uv sync")


@invoke.task
def install_dev(context):
    """Install development requirements for `neosctl`."""
    context.run("uv sync --extra dev")
    context.run("uv run pre-commit install")
    context.run(
        """
        echo "Generating pyrightconfig.json";
        echo "{\\"venv\\": \\".\\", \\"venvPath\\": \\".venv\\", \\"exclude\\": [\\"tests\\"], \\"include\\": [\\"neosctl\\"]}" > pyrightconfig.json
    """,
    )


@invoke.task
def check_style(context):
    """Run style checks."""
    context.run("ruff .")


@invoke.task
def check_types(context):
    """Run pyright checks."""
    context.run("pyright neosctl")


@invoke.task
def tests(context):
    """Run pytest unit tests."""
    context.run("pytest -x -s")


@invoke.task
def tests_coverage(context, output="xml"):
    """Run pytest unit tests with coverage."""
    context.run(f"pytest --cov=neosctl -x --cov-report={output}")


@invoke.task
def generate_docs_md(context):
    """Generate markdown documentation."""
    context.run("typer neosctl.cli utils docs --name neosctl --output DOCS.md")


@invoke.task
def release(context):
    """Bump to next X.Y.Z version."""
    context.run("changelog generate")


@invoke.task
def bump_patch(context):
    """Bump to next X.Y.patch version."""
    context.run("changelog generate --version-part=patch")


@invoke.task
def bump_minor(context):
    """Bump to next X.minor.0 version."""
    context.run("changelog generate --version-part=minor")


@invoke.task
def bump_major(context):
    """Bump to next major.0.0 version."""
    context.run("changelog generate --version-part=major")


@invoke.task
def generate_docs(context):
    """Generate docstrings pdoc html documentation."""
    context.run("pdoc -o docs -d google ./neosctl")
