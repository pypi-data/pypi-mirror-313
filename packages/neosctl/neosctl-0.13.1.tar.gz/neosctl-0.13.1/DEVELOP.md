## Prerequisites

The following packages are used across python repositories. A global install of them all is _highly_ recommended.

* [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Invoke](https://www.pyinvoke.org/installing.html)

## Local Development

To install the CLI from source, clone the repository and run the following

```bash
$ invoke install-dev
```

Check the [Prerequisites](#prerequisites) for global installs required for local development.

When running locally, uv will manage your virtual environment for you, if you
do not have automated virtualenv activation run `source .venv/bin/activate`.

Or use `uv run` to drop you into the environment to run a command.

```bash
$ uv run ...
```

## Code Quality

### Tests

```bash
invoke tests
invoke tests-coverage
```

## Linting

```bash
invoke check-style
invoke isort
```

## Generate docs

To generate docs in a markdown format, run the following command:

```bash
invoke generate-docs-md
```

The output [DOCS.md](https://github.com/NEOS-Critical/neos-platform-cli/tree/main/DOCS.md) file could be used to update the NEOS documentation site
([docs.neosmesh.com](https://docs.neosmesh.com)).

## Releases

Release management is handled using `changelog-gen`. The below commands will
tag a new release, and generate the matching changelog entries. Jenkins will
then publish the release to the artifact repository.

```bash
$ invoke release
$ invoke bump-patch
$ invoke bump-minor
$ invoke bump-major
> vX.Y.Z
```
