# `neosctl`

Interact with NEOS environments and cores.

**Usage**:

```console
$ neosctl [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`: Print version and exit.
* `-p, --profile TEXT`: Profile name  [default: default]
* `-e, --env TEXT`: Active env override
* `-c, --core TEXT`: Active core override
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `auth`: Manage authentication status.
* `env`: Manage environments.
* `gateway`: Interact with Gateway service.
* `iam`: Manage access policies.
* `profile`: Manage profiles.
* `registry`: Manage cores and search data products.
* `storage`: Interact with Storage (as a service).

## `neosctl auth`

Manage authentication status. [DEPRECATED]

**Usage**:

```console
$ neosctl auth [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `login`: Login to neos.
* `logout`: Logout from neos.

### `neosctl auth login`

Login to neos.

**Usage**:

```console
$ neosctl auth login [OPTIONS]
```

**Options**:

* `-p, --password TEXT`
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl auth logout`

Logout from neos.

**Usage**:

```console
$ neosctl auth logout [OPTIONS]
```

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

## `neosctl env`

Manage environments.

**Usage**:

```console
$ neosctl env [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `activate`: Activate an environment.
* `activate-core`: Activate a core in current environment.
* `active`: View configuration for active environment.
* `credentials`: Configure access keys for an environment.
* `delete`: Delete an environment.
* `init`: Initialise an environment.
* `list`: List available environments.
* `list-cores`: List available cores.
* `login`: Login to environment.
* `logout`: Logout from neos.
* `set-account`: Switch active environment account.
* `view`: View configuration for an environment.
* `whoami`: Get current user ID

### `neosctl env activate`

Activate an environment.

Activate an environment to use its configuration for subsequent requests.

**Usage**:

```console
$ neosctl env activate [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--refresh / --no-refresh`: Refresh core cache.  [default: refresh]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl env activate-core`

Activate a core in current environment.

**Usage**:

```console
$ neosctl env activate-core [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl env active`

View configuration for active environment.

**Usage**:

```console
$ neosctl env active [OPTIONS]
```

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl env credentials`

Configure access keys for an environment.

**Usage**:

```console
$ neosctl env credentials [OPTIONS] NAME ACCESS_KEY_ID SECRET_ACCESS_KEY
```

**Arguments**:

* `NAME`: [required]
* `ACCESS_KEY_ID`: [required]
* `SECRET_ACCESS_KEY`: [required]

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl env delete`

Delete an environment.

**Usage**:

```console
$ neosctl env delete [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl env init`

Initialise an environment.

Create an environment that can be reused in later commands to define which
services to interact with, and which user to interact as.

Call `init` on an existing environment will update it.

**Usage**:

```console
$ neosctl env init [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `-h, --hub-api-url TEXT`: [required]
* `-u, --username TEXT`: [required]
* `-a, --account TEXT`: [required]
* `--ignore-tls`: Ignore TLS errors (useful in local/development environments)
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl env list`

List available environments.

**Usage**:

```console
$ neosctl env list [OPTIONS]
```

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: text]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl env list-cores`

List available cores.

**Usage**:

```console
$ neosctl env list-cores [OPTIONS]
```

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: text]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl env login`

Login to environment.

**Usage**:

```console
$ neosctl env login [OPTIONS]
```

**Options**:

* `-p, --password TEXT`
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl env logout`

Logout from neos.

**Usage**:

```console
$ neosctl env logout [OPTIONS]
```

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl env set-account`

Switch active environment account.

**Usage**:

```console
$ neosctl env set-account [OPTIONS] ACCOUNT
```

**Arguments**:

* `ACCOUNT`: [required]

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl env view`

View configuration for an environment.

**Usage**:

```console
$ neosctl env view [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl env whoami`

Get current user ID.

**Usage**:

```console
$ neosctl env whoami [OPTIONS]
```

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

## `neosctl gateway`

Interact with Gateway service.

**Usage**:

```console
$ neosctl gateway [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `data-product`: Manage data product entity.
* `data-source`: Manage data source entity.
* `data-system`: Manage data system entity.
* `data-unit`: Manage data unit entity.
* `journal-note`: Manage journal note element.
* `link`: Manage links.
* `output`: Manage output entity.
* `secret`: Manage secrets.
* `spark`: Manage spark job.
* `tag`: Manage tags.

### `neosctl gateway data-product`

Manage data product entity.

**Usage**:

```console
$ neosctl gateway data-product [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create data product.
* `create-expectation-custom`: Add data product custom expectation.
* `delete`: Delete data product.
* `delete-data`: Delete data product data.
* `delete-expectation-custom`: Delete data product custom expectation.
* `delete-metadata`: Delete data product metadata.
* `get`: Get data product.
* `get-builder`: Get data product builder.
* `get-builder-state`: Get data product builder state.
* `get-classification-result`: Get data product classification result.
* `get-classification-rule`: Get data product classification rule.
* `get-data`: Get data product data.
* `get-expectation`: Get data product expectation settings.
* `get-expectation-rules`: Get data product expectation rules.
* `get-info`: Get data product info.
* `get-journal`: Get data product journal.
* `get-lineage`: Get data product lineage.
* `get-links`: Get data product links.
* `get-metadata`: Get data product metadata.
* `get-quality-profiling`: Get data product profiling.
* `get-quality-validations`: Get data product validations.
* `get-schema`: Get data product schema.
* `get-spark-lineage`: Get data product spark lineage.
* `list`: List data products.
* `publish`: Publish data product.
* `unpublish`: Unpublish data product.
* `update`: Update data product.
* `update-builder`: Update data product builder.
* `update-classification-result`: Update data product classification result.
* `update-classification-rule`: Update data product classification rule.
* `update-expectation-custom`: Update data product custom expectation.
* `update-expectation-thresholds`: Update data product expectation thresholds.
* `update-expectation-weights`: Update data product expectation weights.
* `update-info`: Update data product info.
* `update-journal`: Update data product journal.
* `update-metadata`: Update data product metadata.
* `update-schema`: Update data product schema.
* `update-spark-file`: Update data product spark file.
* `update-spark-state`: Update data product spark state.

#### `neosctl gateway data-product create`

Create data product.

**Usage**:

```console
$ neosctl gateway data-product create [OPTIONS] LABEL NAME DESCRIPTION
```

**Arguments**:

* `LABEL`: Data Product label  [required]
* `NAME`: Data Product name  [required]
* `DESCRIPTION`: Data Product description  [required]

**Options**:

* `--owner TEXT`: Data Product owner
* `-c, --contact TEXT`: Data Product contact IDs
* `-l, --link TEXT`: Data Product links
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product create-expectation-custom`

Add data product custom expectation.

**Usage**:

```console
$ neosctl gateway data-product create-expectation-custom [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `FILEPATH`: Filepath to custom expectation description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product delete`

Delete data product.

**Usage**:

```console
$ neosctl gateway data-product delete [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product delete-data`

Delete data product data.

**Usage**:

```console
$ neosctl gateway data-product delete-data [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product delete-expectation-custom`

Delete data product custom expectation.

**Usage**:

```console
$ neosctl gateway data-product delete-expectation-custom [OPTIONS] IDENTIFIER CUSTOM_IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `CUSTOM_IDENTIFIER`: Custom expectation identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product delete-metadata`

Delete data product metadata.

**Usage**:

```console
$ neosctl gateway data-product delete-metadata [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `FILEPATH`: Filepath to metadata description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get`

Get data product.

**Usage**:

```console
$ neosctl gateway data-product get [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-builder`

Get data product builder.

**Usage**:

```console
$ neosctl gateway data-product get-builder [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-builder-state`

Get data product builder state.

**Usage**:

```console
$ neosctl gateway data-product get-builder-state [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-classification-result`

Get data product classification result.

**Usage**:

```console
$ neosctl gateway data-product get-classification-result [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-classification-rule`

Get data product classification rule.

**Usage**:

```console
$ neosctl gateway data-product get-classification-rule [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-data`

Get data product data.

**Usage**:

```console
$ neosctl gateway data-product get-data [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-expectation`

Get data product expectation settings.

**Usage**:

```console
$ neosctl gateway data-product get-expectation [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-l, --last-only`: Return only last settings.
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-expectation-rules`

Get data product expectation rules.

**Usage**:

```console
$ neosctl gateway data-product get-expectation-rules [OPTIONS]
```

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-info`

Get data product info.

**Usage**:

```console
$ neosctl gateway data-product get-info [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-journal`

Get data product journal.

**Usage**:

```console
$ neosctl gateway data-product get-journal [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-p, --page INTEGER`: Page number  [default: 1]
* `-pp, --per-page INTEGER`: Number of items per page  [default: 25]
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-lineage`

Get data product lineage.

**Usage**:

```console
$ neosctl gateway data-product get-lineage [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-links`

Get data product links.

**Usage**:

```console
$ neosctl gateway data-product get-links [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-metadata`

Get data product metadata.

**Usage**:

```console
$ neosctl gateway data-product get-metadata [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-quality-profiling`

Get data product profiling.

**Usage**:

```console
$ neosctl gateway data-product get-quality-profiling [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-quality-validations`

Get data product validations.

**Usage**:

```console
$ neosctl gateway data-product get-quality-validations [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-schema`

Get data product schema.

**Usage**:

```console
$ neosctl gateway data-product get-schema [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product get-spark-lineage`

Get data product spark lineage.

**Usage**:

```console
$ neosctl gateway data-product get-spark-lineage [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product list`

List data products.

**Usage**:

```console
$ neosctl gateway data-product list [OPTIONS]
```

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product publish`

Publish data product.

**Usage**:

```console
$ neosctl gateway data-product publish [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `--private`: Limit visibility in mesh to core account.
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product unpublish`

Unpublish data product.

**Usage**:

```console
$ neosctl gateway data-product unpublish [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product update`

Update data product.

**Usage**:

```console
$ neosctl gateway data-product update [OPTIONS] IDENTIFIER LABEL NAME DESCRIPTION
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `LABEL`: Data Product label  [required]
* `NAME`: Data Product name  [required]
* `DESCRIPTION`: Data Product description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product update-builder`

Update data product builder.

**Usage**:

```console
$ neosctl gateway data-product update-builder [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `FILEPATH`: Filepath to builder description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product update-classification-result`

Update data product classification result.

**Usage**:

```console
$ neosctl gateway data-product update-classification-result [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `FILEPATH`: Filepath to classification rule description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product update-classification-rule`

Update data product classification rule.

**Usage**:

```console
$ neosctl gateway data-product update-classification-rule [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `FILEPATH`: Filepath to classification rule description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product update-expectation-custom`

Update data product custom expectation.

**Usage**:

```console
$ neosctl gateway data-product update-expectation-custom [OPTIONS] IDENTIFIER CUSTOM_IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `CUSTOM_IDENTIFIER`: Custom expectation identifier  [required]
* `FILEPATH`: Filepath to custom expectation description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product update-expectation-thresholds`

Update data product expectation thresholds.

**Usage**:

```console
$ neosctl gateway data-product update-expectation-thresholds [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `FILEPATH`: Filepath to expectation thresholds description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product update-expectation-weights`

Update data product expectation weights.

**Usage**:

```console
$ neosctl gateway data-product update-expectation-weights [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `FILEPATH`: Filepath to expectation weights description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product update-info`

Update data product info.

**Usage**:

```console
$ neosctl gateway data-product update-info [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]

**Options**:

* `--owner TEXT`: Data Product owner  [required]
* `-c, --contact TEXT`: Data Product contact IDs
* `-l, --link TEXT`: Data Product links
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product update-journal`

Update data product journal.

**Usage**:

```console
$ neosctl gateway data-product update-journal [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `FILEPATH`: Filepath to journal note payload  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product update-metadata`

Update data product metadata.

**Usage**:

```console
$ neosctl gateway data-product update-metadata [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `FILEPATH`: Filepath to metadata description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product update-schema`

Update data product schema.

**Usage**:

```console
$ neosctl gateway data-product update-schema [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `FILEPATH`: Filepath to schema description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product update-spark-file`

Update data product spark file.

**Usage**:

```console
$ neosctl gateway data-product update-spark-file [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `FILEPATH`: Spark job filepath  [required]

**Options**:

* `-s, --secret TEXT`: Secret identifier
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-product update-spark-state`

Update data product spark state.

**Usage**:

```console
$ neosctl gateway data-product update-spark-state [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Product identifier  [required]
* `FILEPATH`: Filepath to spark state description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl gateway data-source`

Manage data source entity.

**Usage**:

```console
$ neosctl gateway data-source [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create data source.
* `delete`: Delete data source.
* `get`: Get data source.
* `get-connection`: Get data source connection.
* `get-info`: Get data source info.
* `get-journal`: Get data source journal.
* `get-links`: Get data source links.
* `list`: List data sources.
* `set-connection-secrets`: Set data source connection secrets.
* `update`: Update data source.
* `update-connection`: Update data source connection.
* `update-info`: Update data source info.
* `update-journal`: Update data source journal.

#### `neosctl gateway data-source create`

Create data source.

**Usage**:

```console
$ neosctl gateway data-source create [OPTIONS] LABEL NAME DESCRIPTION
```

**Arguments**:

* `LABEL`: Data Source label  [required]
* `NAME`: Data Source name  [required]
* `DESCRIPTION`: Data Source description  [required]

**Options**:

* `--owner TEXT`: Data Source owner
* `-c, --contact TEXT`: Data Source contact IDs
* `-l, --link TEXT`: Data Source links
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-source delete`

Delete data source.

**Usage**:

```console
$ neosctl gateway data-source delete [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Source identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-source get`

Get data source.

**Usage**:

```console
$ neosctl gateway data-source get [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Source identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-source get-connection`

Get data source connection.

**Usage**:

```console
$ neosctl gateway data-source get-connection [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Source identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-source get-info`

Get data source info.

**Usage**:

```console
$ neosctl gateway data-source get-info [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Source identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-source get-journal`

Get data source journal.

**Usage**:

```console
$ neosctl gateway data-source get-journal [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Source identifier  [required]

**Options**:

* `-p, --page INTEGER`: Page number  [default: 1]
* `-pp, --per-page INTEGER`: Number of items per page  [default: 25]
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-source get-links`

Get data source links.

**Usage**:

```console
$ neosctl gateway data-source get-links [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Source identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-source list`

List data sources.

**Usage**:

```console
$ neosctl gateway data-source list [OPTIONS]
```

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-source set-connection-secrets`

Set data source connection secrets.

**Usage**:

```console
$ neosctl gateway data-source set-connection-secrets [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Source identifier  [required]
* `FILEPATH`: Filepath to secrets description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-source update`

Update data source.

**Usage**:

```console
$ neosctl gateway data-source update [OPTIONS] IDENTIFIER LABEL NAME DESCRIPTION
```

**Arguments**:

* `IDENTIFIER`: Data Source identifier  [required]
* `LABEL`: Data Source label  [required]
* `NAME`: Data Source name  [required]
* `DESCRIPTION`: Data Source description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-source update-connection`

Update data source connection.

**Usage**:

```console
$ neosctl gateway data-source update-connection [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Source identifier  [required]
* `FILEPATH`: Filepath to connection description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-source update-info`

Update data source info.

**Usage**:

```console
$ neosctl gateway data-source update-info [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Source identifier  [required]

**Options**:

* `--owner TEXT`: Data Source owner  [required]
* `-c, --contact TEXT`: Data Source contact IDs
* `-l, --link TEXT`: Data Source links
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-source update-journal`

Update data source journal.

**Usage**:

```console
$ neosctl gateway data-source update-journal [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Source identifier  [required]
* `FILEPATH`: Filepath to journal note payload  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl gateway data-system`

Manage data system entity.

**Usage**:

```console
$ neosctl gateway data-system [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create data system.
* `delete`: Delete data system.
* `get`: Get data system.
* `get-info`: Get data system info.
* `get-journal`: Get data system journal.
* `get-links`: Get data system links.
* `list`: List data systems.
* `update`: Update data system.
* `update-info`: Update data system info.
* `update-journal`: Update data system journal.

#### `neosctl gateway data-system create`

Create data system.

**Usage**:

```console
$ neosctl gateway data-system create [OPTIONS] LABEL NAME DESCRIPTION
```

**Arguments**:

* `LABEL`: Data System label  [required]
* `NAME`: Data System name  [required]
* `DESCRIPTION`: Data System description  [required]

**Options**:

* `--owner TEXT`: Data System owner
* `-c, --contact TEXT`: Data System contact IDs
* `-l, --link TEXT`: Data System links
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-system delete`

Delete data system.

**Usage**:

```console
$ neosctl gateway data-system delete [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data System identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-system get`

Get data system.

**Usage**:

```console
$ neosctl gateway data-system get [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data System identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-system get-info`

Get data system info.

**Usage**:

```console
$ neosctl gateway data-system get-info [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data System identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-system get-journal`

Get data system journal.

**Usage**:

```console
$ neosctl gateway data-system get-journal [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data System identifier  [required]

**Options**:

* `-p, --page INTEGER`: Page number  [default: 1]
* `-pp, --per-page INTEGER`: Number of items per page  [default: 25]
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-system get-links`

Get data system links.

**Usage**:

```console
$ neosctl gateway data-system get-links [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data System identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-system list`

List data systems.

**Usage**:

```console
$ neosctl gateway data-system list [OPTIONS]
```

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-system update`

Update data system.

**Usage**:

```console
$ neosctl gateway data-system update [OPTIONS] IDENTIFIER LABEL NAME DESCRIPTION
```

**Arguments**:

* `IDENTIFIER`: Data System identifier  [required]
* `LABEL`: Data System label  [required]
* `NAME`: Data System name  [required]
* `DESCRIPTION`: Data System description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-system update-info`

Update data system info.

**Usage**:

```console
$ neosctl gateway data-system update-info [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data System identifier  [required]

**Options**:

* `--owner TEXT`: Data System owner  [required]
* `-c, --contact TEXT`: Data System contact IDs
* `-l, --link TEXT`: Data System links
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-system update-journal`

Update data system journal.

**Usage**:

```console
$ neosctl gateway data-system update-journal [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data System identifier  [required]
* `FILEPATH`: Filepath to journal note payload  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl gateway data-unit`

Manage data unit entity.

**Usage**:

```console
$ neosctl gateway data-unit [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create data unit.
* `delete`: Delete data unit.
* `delete-metadata`: Delete data unit metadata.
* `get`: Get data unit.
* `get-config`: Get data unit config.
* `get-info`: Get data unit info.
* `get-journal`: Get data unit journal.
* `get-links`: Get data unit links.
* `get-schema`: Get data unit schema.
* `list`: List data units.
* `update`: Update data unit.
* `update-config`: Update data unit config.
* `update-info`: Update data unit info.
* `update-journal`: Update data unit journal.
* `update-metadata`: Update data unit metadata.

#### `neosctl gateway data-unit create`

Create data unit.

**Usage**:

```console
$ neosctl gateway data-unit create [OPTIONS] LABEL NAME DESCRIPTION
```

**Arguments**:

* `LABEL`: Data Unit label  [required]
* `NAME`: Data Unit name  [required]
* `DESCRIPTION`: Data Unit description  [required]

**Options**:

* `--owner TEXT`: Data Unit owner
* `-c, --contact TEXT`: Data Unit contact IDs
* `-l, --link TEXT`: Data Unit links
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit delete`

Delete data unit.

**Usage**:

```console
$ neosctl gateway data-unit delete [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Unit identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit delete-metadata`

Delete data unit metadata.

**Usage**:

```console
$ neosctl gateway data-unit delete-metadata [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Unit identifier  [required]
* `FILEPATH`: Filepath to metadata description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit get`

Get data unit.

**Usage**:

```console
$ neosctl gateway data-unit get [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Unit identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit get-config`

Get data unit config.

**Usage**:

```console
$ neosctl gateway data-unit get-config [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Unit identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit get-info`

Get data unit info.

**Usage**:

```console
$ neosctl gateway data-unit get-info [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Unit identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit get-journal`

Get data unit journal.

**Usage**:

```console
$ neosctl gateway data-unit get-journal [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Unit identifier  [required]

**Options**:

* `-p, --page INTEGER`: Page number  [default: 1]
* `-pp, --per-page INTEGER`: Number of items per page  [default: 25]
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit get-links`

Get data unit links.

**Usage**:

```console
$ neosctl gateway data-unit get-links [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Unit identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit get-schema`

Get data unit schema.

**Usage**:

```console
$ neosctl gateway data-unit get-schema [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Unit identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit list`

List data units.

**Usage**:

```console
$ neosctl gateway data-unit list [OPTIONS]
```

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit update`

Update data unit.

**Usage**:

```console
$ neosctl gateway data-unit update [OPTIONS] IDENTIFIER LABEL NAME DESCRIPTION
```

**Arguments**:

* `IDENTIFIER`: Data Unit identifier  [required]
* `LABEL`: Data Unit label  [required]
* `NAME`: Data Unit name  [required]
* `DESCRIPTION`: Data Unit description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit update-config`

Update data unit config.

**Usage**:

```console
$ neosctl gateway data-unit update-config [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Unit identifier  [required]
* `FILEPATH`: Filepath to config description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit update-info`

Update data unit info.

**Usage**:

```console
$ neosctl gateway data-unit update-info [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Data Unit identifier  [required]

**Options**:

* `--owner TEXT`: Data Unit owner  [required]
* `-c, --contact TEXT`: Data Unit contact IDs
* `-l, --link TEXT`: Data Unit links
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit update-journal`

Update data unit journal.

**Usage**:

```console
$ neosctl gateway data-unit update-journal [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Unit identifier  [required]
* `FILEPATH`: Filepath to journal note payload  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway data-unit update-metadata`

Update data unit metadata.

**Usage**:

```console
$ neosctl gateway data-unit update-metadata [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Data Unit identifier  [required]
* `FILEPATH`: Filepath to metadata description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl gateway journal-note`

Manage journal note element.

**Usage**:

```console
$ neosctl gateway journal-note [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `delete`: Delete journal note.
* `get`: Get journal note.
* `update`: Update journal note.

#### `neosctl gateway journal-note delete`

Delete journal note.

**Usage**:

```console
$ neosctl gateway journal-note delete [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Journal Note identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway journal-note get`

Get journal note.

**Usage**:

```console
$ neosctl gateway journal-note get [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Journal Note identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway journal-note update`

Update journal note.

**Usage**:

```console
$ neosctl gateway journal-note update [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Journal Note identifier  [required]
* `FILEPATH`: Filepath to journal note payload  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl gateway link`

Manage links.

**Usage**:

```console
$ neosctl gateway link [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create link between entities.
* `delete`: Delete link between entities.

#### `neosctl gateway link create`

Create link between entities.

**Usage**:

```console
$ neosctl gateway link create [OPTIONS] PARENT_TYPE:{data_system|data_source|data_unit|data_product} PARENT_IDENTIFIER CHILD_TYPE:{data_source|data_unit|data_product|output} CHILD_IDENTIFIER
```

**Arguments**:

* `PARENT_TYPE:{data_system|data_source|data_unit|data_product}`: Parent entity type  [required]
* `PARENT_IDENTIFIER`: Parent identifier  [required]
* `CHILD_TYPE:{data_source|data_unit|data_product|output}`: Child entity type  [required]
* `CHILD_IDENTIFIER`: Child identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway link delete`

Delete link between entities.

**Usage**:

```console
$ neosctl gateway link delete [OPTIONS] PARENT_TYPE:{data_system|data_source|data_unit|data_product} PARENT_IDENTIFIER CHILD_TYPE:{data_source|data_unit|data_product|output} CHILD_IDENTIFIER
```

**Arguments**:

* `PARENT_TYPE:{data_system|data_source|data_unit|data_product}`: Parent entity type  [required]
* `PARENT_IDENTIFIER`: Parent identifier  [required]
* `CHILD_TYPE:{data_source|data_unit|data_product|output}`: Child entity type  [required]
* `CHILD_IDENTIFIER`: Child identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl gateway output`

Manage output entity.

**Usage**:

```console
$ neosctl gateway output [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create output.
* `delete`: Delete output.
* `get`: Get output.
* `get-info`: Get output info.
* `get-journal`: Get output journal.
* `get-links`: Get output links.
* `list`: List outputs.
* `update`: Update output.
* `update-info`: Update output info.
* `update-journal`: Update output journal.

#### `neosctl gateway output create`

Create output.

**Usage**:

```console
$ neosctl gateway output create [OPTIONS] LABEL NAME DESCRIPTION [OUTPUT_TYPE]:[application|dashboard]
```

**Arguments**:

* `LABEL`: Output label  [required]
* `NAME`: Output name  [required]
* `DESCRIPTION`: Output description  [required]
* `[OUTPUT_TYPE]:[application|dashboard]`: Output type  [default: application]

**Options**:

* `--owner TEXT`: Output owner
* `-c, --contact TEXT`: Output contact IDs
* `-l, --link TEXT`: Output links
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway output delete`

Delete output.

**Usage**:

```console
$ neosctl gateway output delete [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Output identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway output get`

Get output.

**Usage**:

```console
$ neosctl gateway output get [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Output identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway output get-info`

Get output info.

**Usage**:

```console
$ neosctl gateway output get-info [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Output identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway output get-journal`

Get output journal.

**Usage**:

```console
$ neosctl gateway output get-journal [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Output identifier  [required]

**Options**:

* `-p, --page INTEGER`: Page number  [default: 1]
* `-pp, --per-page INTEGER`: Number of items per page  [default: 25]
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway output get-links`

Get output links.

**Usage**:

```console
$ neosctl gateway output get-links [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Output identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway output list`

List outputs.

**Usage**:

```console
$ neosctl gateway output list [OPTIONS]
```

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway output update`

Update output.

**Usage**:

```console
$ neosctl gateway output update [OPTIONS] IDENTIFIER LABEL NAME DESCRIPTION [OUTPUT_TYPE]:[application|dashboard]
```

**Arguments**:

* `IDENTIFIER`: Output identifier  [required]
* `LABEL`: Output label  [required]
* `NAME`: Output name  [required]
* `DESCRIPTION`: Output description  [required]
* `[OUTPUT_TYPE]:[application|dashboard]`: Output type  [default: application]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway output update-info`

Update output info.

**Usage**:

```console
$ neosctl gateway output update-info [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Output identifier  [required]

**Options**:

* `--owner TEXT`: Output owner  [required]
* `-c, --contact TEXT`: Output contact IDs
* `-l, --link TEXT`: Output links
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway output update-journal`

Update output journal.

**Usage**:

```console
$ neosctl gateway output update-journal [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Output identifier  [required]
* `FILEPATH`: Filepath to journal note payload  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl gateway secret`

Manage secrets.

**Usage**:

```console
$ neosctl gateway secret [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create new secret.
* `delete`: Delete secret.
* `delete-keys`: Delete secret keys.
* `get`: Get secret.
* `list`: List secrets.
* `update`: Update secret.

#### `neosctl gateway secret create`

Create new secret.

**Usage**:

```console
$ neosctl gateway secret create [OPTIONS] FILEPATH
```

**Arguments**:

* `FILEPATH`: Filepath to secret description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway secret delete`

Delete secret.

**Usage**:

```console
$ neosctl gateway secret delete [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Secret identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway secret delete-keys`

Delete secret keys.

**Usage**:

```console
$ neosctl gateway secret delete-keys [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Secret identifier  [required]
* `FILEPATH`: Filepath to secret keys description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway secret get`

Get secret.

**Usage**:

```console
$ neosctl gateway secret get [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Secret identifier  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway secret list`

List secrets.

**Usage**:

```console
$ neosctl gateway secret list [OPTIONS]
```

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway secret update`

Update secret.

**Usage**:

```console
$ neosctl gateway secret update [OPTIONS] IDENTIFIER FILEPATH
```

**Arguments**:

* `IDENTIFIER`: Secret identifier  [required]
* `FILEPATH`: Filepath to secret description  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl gateway spark`

Manage spark job.

**Usage**:

```console
$ neosctl gateway spark [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `history`: Get spark history.
* `log`: Get spark logs.
* `status`: Get spark status.

#### `neosctl gateway spark history`

Get spark history.

**Usage**:

```console
$ neosctl gateway spark history [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Spark identifier  [required]

**Options**:

* `-s, --suffix TEXT`: Job run suffix
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway spark log`

Get spark logs.

**Usage**:

```console
$ neosctl gateway spark log [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Spark identifier  [required]

**Options**:

* `-s, --suffix TEXT`: Job run suffix  [default: latest]
* `-r, --run TEXT`: Job run
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway spark status`

Get spark status.

**Usage**:

```console
$ neosctl gateway spark status [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Spark identifier  [required]

**Options**:

* `-s, --suffix TEXT`: Job run suffix  [default: latest]
* `-r, --run TEXT`: Job run
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl gateway tag`

Manage tags.

**Usage**:

```console
$ neosctl gateway tag [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create new tag.
* `delete`: Delete tag.
* `list`: List tags.

#### `neosctl gateway tag create`

Create new tag.

**Usage**:

```console
$ neosctl gateway tag create [OPTIONS] NAME SCOPE:{SCHEMA|FIELD}
```

**Arguments**:

* `NAME`: Tag name  [required]
* `SCOPE:{SCHEMA|FIELD}`: Tag scope  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway tag delete`

Delete tag.

**Usage**:

```console
$ neosctl gateway tag delete [OPTIONS] NAME SCOPE:{SCHEMA|FIELD}
```

**Arguments**:

* `NAME`: Tag name  [required]
* `SCOPE:{SCHEMA|FIELD}`: Tag scope  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl gateway tag list`

List tags.

**Usage**:

```console
$ neosctl gateway tag list [OPTIONS] SCOPE:{SCHEMA|FIELD}
```

**Arguments**:

* `SCOPE:{SCHEMA|FIELD}`: Tag scope  [required]

**Options**:

* `-s, --system-defined`: System defined
* `-f, --filter TEXT`: Filter query
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

## `neosctl iam`

Manage access policies.

**Usage**:

```console
$ neosctl iam [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `account`: Manage accounts.
* `group`: Manage groups.
* `policy`: Manage policies.
* `user`: Manage users.

### `neosctl iam account`

Manage accounts.

**Usage**:

```console
$ neosctl iam account [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a system account.
* `delete`: Delete an account.
* `list`: List system accounts.
* `update`: Update an account.

#### `neosctl iam account create`

Create a system account.

**Usage**:

```console
$ neosctl iam account create [OPTIONS]
```

**Options**:

* `-d, --display-name TEXT`: Account display name.  [required]
* `-n, --name TEXT`: Account name (used in urns).  [required]
* `--description, --desc TEXT`: Account description.  [required]
* `--owner TEXT`: Account owner.  [required]
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam account delete`

Delete an account.

**Usage**:

```console
$ neosctl iam account delete [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Account identifier.  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam account list`

List system accounts.

**Usage**:

```console
$ neosctl iam account list [OPTIONS]
```

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam account update`

Update an account.

**Usage**:

```console
$ neosctl iam account update [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Account identifier.  [required]

**Options**:

* `-d, --display-name TEXT`: Account display name.  [required]
* `--description, --desc TEXT`: Account description.  [required]
* `--owner TEXT`: Account owner.  [required]
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl iam group`

Manage groups.

**Usage**:

```console
$ neosctl iam group [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add-principals`: Add principal(s) to an IAM group.
* `create`: Create an IAM group.
* `delete`: Delete an IAM group.
* `get`: Get an IAM group.
* `list`: List IAM groups.
* `remove-principals`: Remove principal(s) from an IAM group.
* `update`: Update an IAM group.

#### `neosctl iam group add-principals`

Add principal(s) to an IAM group.

**Usage**:

```console
$ neosctl iam group add-principals [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Group identifier  [required]

**Options**:

* `-p, --principal TEXT`: Principal identifiers  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam group create`

Create an IAM group.

**Usage**:

```console
$ neosctl iam group create [OPTIONS]
```

**Options**:

* `--name TEXT`: Group name  [required]
* `--description TEXT`: Group description  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam group delete`

Delete an IAM group.

**Usage**:

```console
$ neosctl iam group delete [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Group identifier  [required]

**Options**:

* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam group get`

Get an IAM group.

**Usage**:

```console
$ neosctl iam group get [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Group identifier  [required]

**Options**:

* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam group list`

List IAM groups.

**Usage**:

```console
$ neosctl iam group list [OPTIONS]
```

**Options**:

* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam group remove-principals`

Remove principal(s) from an IAM group.

**Usage**:

```console
$ neosctl iam group remove-principals [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Group identifier  [required]

**Options**:

* `-p, --principal TEXT`: Principal identifiers  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam group update`

Update an IAM group.

**Usage**:

```console
$ neosctl iam group update [OPTIONS] IDENTIFIER
```

**Arguments**:

* `IDENTIFIER`: Group identifier  [required]

**Options**:

* `--name TEXT`: Group name  [required]
* `--description TEXT`: Group description  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl iam policy`

Manage policies.

**Usage**:

```console
$ neosctl iam policy [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create an IAM policy.
* `delete`: Delete an existing IAM policy.
* `get`: Get an existing IAM policy.
* `list`: List existing policies.
* `update`: Update an existing IAM policy.

#### `neosctl iam policy create`

Create an IAM policy.

**Usage**:

```console
$ neosctl iam policy create [OPTIONS] FILEPATH
```

**Arguments**:

* `FILEPATH`: Filepath of the user policy json payload  [required]

**Options**:

* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam policy delete`

Delete an existing IAM policy.

**Usage**:

```console
$ neosctl iam policy delete [OPTIONS] USER_NRN
```

**Arguments**:

* `USER_NRN`: [required]

**Options**:

* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam policy get`

Get an existing IAM policy.

**Usage**:

```console
$ neosctl iam policy get [OPTIONS] USER_NRN
```

**Arguments**:

* `USER_NRN`: [required]

**Options**:

* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam policy list`

List existing policies.

**Usage**:

```console
$ neosctl iam policy list [OPTIONS]
```

**Options**:

* `--page INTEGER`: Page number.  [default: 1]
* `--page-size INTEGER`: Page size number.  [default: 10]
* `--resource TEXT`: Resource nrn.
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam policy update`

Update an existing IAM policy.

**Usage**:

```console
$ neosctl iam policy update [OPTIONS] PRINCIPAL FILEPATH
```

**Arguments**:

* `PRINCIPAL`: Principal uuid  [required]
* `FILEPATH`: Filepath of the user policy json payload  [required]

**Options**:

* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl iam user`

Manage users.

**Usage**:

```console
$ neosctl iam user [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a keycloak user, and assign to...
* `create-key-pair`: Create an access key_pair and assign to a...
* `delete`: Detach user from account.
* `delete-key-pair`: Delete the access key_pair from the user.
* `list`: List existing keycloak users.
* `permissions`: List existing keycloak user permissions.
* `purge`: Purge user from core and IAM.
* `reset-password`: Request a password reset for a user.

#### `neosctl iam user create`

Create a keycloak user, and assign to account.

**Usage**:

```console
$ neosctl iam user create [OPTIONS]
```

**Options**:

* `-u, --username TEXT`: [required]
* `-e, --email TEXT`: [required]
* `-f, --first-name TEXT`: [required]
* `-l, --last-name TEXT`: [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam user create-key-pair`

Create an access key_pair and assign to a user.

**Usage**:

```console
$ neosctl iam user create-key-pair [OPTIONS] USER_NRN
```

**Arguments**:

* `USER_NRN`: [required]

**Options**:

* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam user delete`

Detach user from account.

**Usage**:

```console
$ neosctl iam user delete [OPTIONS]
```

**Options**:

* `-uid, --user-id TEXT`: User id in keycloak.  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam user delete-key-pair`

Delete the access key_pair from the user.

**Usage**:

```console
$ neosctl iam user delete-key-pair [OPTIONS] USER_NRN ACCESS_KEY_ID
```

**Arguments**:

* `USER_NRN`: [required]
* `ACCESS_KEY_ID`: [required]

**Options**:

* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam user list`

List existing keycloak users.

Filter by search term on username, first_name, last_name, or email.

**Usage**:

```console
$ neosctl iam user list [OPTIONS]
```

**Options**:

* `--search TEXT`: Search term
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam user permissions`

List existing keycloak user permissions.

**Usage**:

```console
$ neosctl iam user permissions [OPTIONS]
```

**Options**:

* `--username TEXT`: Keycloak username
* `--identifier UUID`: User or Group identifier
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam user purge`

Purge user from core and IAM.

**Usage**:

```console
$ neosctl iam user purge [OPTIONS]
```

**Options**:

* `-uid, --user-id TEXT`: User id in keycloak.  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl iam user reset-password`

Request a password reset for a user.

**Usage**:

```console
$ neosctl iam user reset-password [OPTIONS] USERNAME
```

**Arguments**:

* `USERNAME`: Keycloak user `username`  [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

## `neosctl profile`

Manage profiles. [DEPRECATED]

**Usage**:

```console
$ neosctl profile [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `credentials`: View configuration for a profile.
* `delete`: Delete a profile.
* `init`: Initialise a profile.
* `list`: List available profiles.
* `view`: View configuration for a profile.

### `neosctl profile credentials`

View configuration for a profile.

**Usage**:

```console
$ neosctl profile credentials [OPTIONS] ACCESS_KEY_ID SECRET_ACCESS_KEY
```

**Arguments**:

* `ACCESS_KEY_ID`: [required]
* `SECRET_ACCESS_KEY`: [required]

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl profile delete`

Delete a profile.

**Usage**:

```console
$ neosctl profile delete [OPTIONS]
```

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl profile init`

Initialise a profile.

Create a profile that can be reused in later commands to define which
services to interact with, and which user to interact as.

Call `init` on an existing profile will update the existing profile.

**Usage**:

```console
$ neosctl profile init [OPTIONS]
```

**Options**:

* `-h, --host TEXT`
* `-g, --gateway-api-url TEXT`
* `--hub-api-url TEXT`
* `-s, --storage-api-url TEXT`
* `-u, --username TEXT`
* `-a, --account TEXT`: [default: root]
* `--ignore-tls`: Ignore TLS errors (useful in local/development environments
* `--non-interactive`: Don't ask for input, generate api values based on hostname.
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl profile list`

List available profiles.

**Usage**:

```console
$ neosctl profile list [OPTIONS]
```

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl profile view`

View configuration for a profile.

**Usage**:

```console
$ neosctl profile view [OPTIONS]
```

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

## `neosctl registry`

Manage cores and search data products.

**Usage**:

```console
$ neosctl registry [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `core`: Manage cores.
* `get-product`: Get data product details.
* `list-cores`: List accessible cores.
* `mesh`: Manage mesh.
* `mesh-core-products`: List visible products in a core.
* `mesh-cores`: List visible cores.
* `mesh-subscriptions`: List mesh subscriptions.
* `migrate-core`: Migrate a core.
* `product`: Manage products.
* `register-core`: Register a core.
* `remove-contact`: Remove a contact for a core.
* `remove-core`: Remove a registered core.
* `search`: Search published data products.
* `subscribe-product`: Subscribe to a data product.
* `unsubscribe-product`: Unsubscribe from a data product.
* `update-subscription`: Update subscription to a data product.
* `upsert-contact`: Add/Update a contact for a core.

### `neosctl registry core`

Manage cores.

**Usage**:

```console
$ neosctl registry core [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List accessible cores.
* `migrate`: Migrate a core out of root account.
* `register`: Register a core.
* `remove`: Remove a registered core.
* `remove-contact`: Remove a contact for a core.
* `upsert-contact`: Add/Update a contact for a core.

#### `neosctl registry core list`

List accessible cores.

**Usage**:

```console
$ neosctl registry core list [OPTIONS]
```

**Options**:

* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl registry core migrate`

Migrate a core out of root account.

Migrate a core from `root` into an actual account.

**Usage**:

```console
$ neosctl registry core migrate [OPTIONS]
```

**Options**:

* `--identifier TEXT`: Core identifier  [required]
* `--urn TEXT`: Core urn  [required]
* `--account TEXT`: Account name  [required]
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl registry core register`

Register a core.

Register a core to receive an identifier and access key for use in deployment.

**Usage**:

```console
$ neosctl registry core register [OPTIONS] PARTITION NAME
```

**Arguments**:

* `PARTITION`: Core partition  [required]
* `NAME`: Core name  [required]

**Options**:

* `--account TEXT`: Account override (root only).
* `--private`: Limit visibility in mesh to core account.
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl registry core remove`

Remove a registered core.

**Usage**:

```console
$ neosctl registry core remove [OPTIONS]
```

**Options**:

* `--identifier TEXT`: Core identifier  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl registry core remove-contact`

Remove a contact for a core.

**Usage**:

```console
$ neosctl registry core remove-contact [OPTIONS]
```

**Options**:

* `--identifier TEXT`: Core identifier  [required]
* `--user-id UUID`: Contact id  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl registry core upsert-contact`

Add/Update a contact for a core.

**Usage**:

```console
$ neosctl registry core upsert-contact [OPTIONS]
```

**Options**:

* `--identifier TEXT`: Core identifier  [required]
* `--user-id UUID`: Contact id  [required]
* `--role TEXT`: Contact role  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry get-product`

Get data product details. [DEPRECATED]

**Usage**:

```console
$ neosctl registry get-product [OPTIONS] URN
```

**Arguments**:

* `URN`: [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry list-cores`

List accessible cores. [DEPRECATED]

**Usage**:

```console
$ neosctl registry list-cores [OPTIONS]
```

**Options**:

* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry mesh`

Manage mesh.

**Usage**:

```console
$ neosctl registry mesh [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `core-products`: List visible products in a core.
* `cores`: List visible cores.
* `subscriptions`: List mesh subscriptions.

#### `neosctl registry mesh core-products`

List visible products in a core.

**Usage**:

```console
$ neosctl registry mesh core-products [OPTIONS]
```

**Options**:

* `--identifier TEXT`: Core identifier  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl registry mesh cores`

List visible cores.

**Usage**:

```console
$ neosctl registry mesh cores [OPTIONS]
```

**Options**:

* `--account TEXT`: Account override (root only).
* `--search TEXT`: Search core name(s)
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl registry mesh subscriptions`

List mesh subscriptions.

**Usage**:

```console
$ neosctl registry mesh subscriptions [OPTIONS]
```

**Options**:

* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry mesh-core-products`

List visible products in a core. [DEPRECATED]

**Usage**:

```console
$ neosctl registry mesh-core-products [OPTIONS]
```

**Options**:

* `--identifier TEXT`: Core identifier  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry mesh-cores`

List visible cores. [DEPRECATED]

**Usage**:

```console
$ neosctl registry mesh-cores [OPTIONS]
```

**Options**:

* `--account TEXT`: Account override (root only).
* `--search TEXT`: Search core name(s)
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry mesh-subscriptions`

List mesh subscriptions. [DEPRECATED]

**Usage**:

```console
$ neosctl registry mesh-subscriptions [OPTIONS]
```

**Options**:

* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry migrate-core`

Migrate a core. [DEPRECATED]

**Usage**:

```console
$ neosctl registry migrate-core [OPTIONS]
```

**Options**:

* `--identifier TEXT`: Core identifier  [required]
* `--urn TEXT`: Core urn  [required]
* `--account TEXT`: Account name  [required]
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry product`

Manage products.

**Usage**:

```console
$ neosctl registry product [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get`: Get data product details.
* `search`: Search published data products across cores.
* `subscribe`: Subscribe to a data product.
* `unsubscribe`: Unsubscribe from a data product.
* `update-subscription`: Update subscription to a data product.

#### `neosctl registry product get`

Get data product details.

**Usage**:

```console
$ neosctl registry product get [OPTIONS] URN
```

**Arguments**:

* `URN`: [required]

**Options**:

* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl registry product search`

Search published data products across cores.

**Usage**:

```console
$ neosctl registry product search [OPTIONS] SEARCH_TERM
```

**Arguments**:

* `SEARCH_TERM`: [required]

**Options**:

* `--keyword / --hybrid`: Search mode  [default: hybrid]
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl registry product subscribe`

Subscribe to a data product.

**Usage**:

```console
$ neosctl registry product subscribe [OPTIONS]
```

**Options**:

* `-cid, --core-id TEXT`: Core identifier  [required]
* `-pid, --product-id TEXT`: Data product identifier  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl registry product unsubscribe`

Unsubscribe from a data product.

**Usage**:

```console
$ neosctl registry product unsubscribe [OPTIONS]
```

**Options**:

* `-cid, --core-id TEXT`: Core identifier  [required]
* `-pid, --product-id TEXT`: Data product identifier  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl registry product update-subscription`

Update subscription to a data product.

**Usage**:

```console
$ neosctl registry product update-subscription [OPTIONS]
```

**Options**:

* `-cid, --core-id TEXT`: Core identifier  [required]
* `-pid, --product-id TEXT`: Data product identifier  [required]
* `-scid, --sub-core-id TEXT`: Subscriber core identifier.  [required]
* `--reason TEXT`: [required]
* `--status [active|inactive]`: [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry register-core`

Register a core. [DEPRECATED]

**Usage**:

```console
$ neosctl registry register-core [OPTIONS] PARTITION NAME
```

**Arguments**:

* `PARTITION`: Core partition  [required]
* `NAME`: Core name  [required]

**Options**:

* `--account TEXT`: Account override (root only).
* `--private`: Limit visibility in mesh to core account.
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry remove-contact`

Remove a contact for a core. [DEPRECATED]

**Usage**:

```console
$ neosctl registry remove-contact [OPTIONS]
```

**Options**:

* `--identifier TEXT`: Core identifier  [required]
* `--user-id UUID`: Contact id  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry remove-core`

Remove a registered core. [DEPRECATED]

**Usage**:

```console
$ neosctl registry remove-core [OPTIONS]
```

**Options**:

* `--identifier TEXT`: Core identifier  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry search`

Search published data products. [DEPRECATED]

**Usage**:

```console
$ neosctl registry search [OPTIONS] SEARCH_TERM
```

**Arguments**:

* `SEARCH_TERM`: [required]

**Options**:

* `--keyword / --hybrid`: Search mode  [default: hybrid]
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry subscribe-product`

Subscribe to a data product. [DEPRECATED]

**Usage**:

```console
$ neosctl registry subscribe-product [OPTIONS]
```

**Options**:

* `-cid, --core-id TEXT`: Core identifier  [required]
* `-pid, --product-id TEXT`: Data product identifier  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry unsubscribe-product`

Unsubscribe from a data product. [DEPRECATED]

**Usage**:

```console
$ neosctl registry unsubscribe-product [OPTIONS]
```

**Options**:

* `-cid, --core-id TEXT`: Core identifier  [required]
* `-pid, --product-id TEXT`: Data product identifier  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry update-subscription`

Update subscription to a data product. [DEPRECATED]

**Usage**:

```console
$ neosctl registry update-subscription [OPTIONS]
```

**Options**:

* `-cid, --core-id TEXT`: Core identifier  [required]
* `-pid, --product-id TEXT`: Data product identifier  [required]
* `-scid, --sub-core-id TEXT`: Subscriber core identifier.  [required]
* `--reason TEXT`: [required]
* `--status [active|inactive]`: [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl registry upsert-contact`

Add/Update a contact for a core. [DEPRECATED]

**Usage**:

```console
$ neosctl registry upsert-contact [OPTIONS]
```

**Options**:

* `--identifier TEXT`: Core identifier  [required]
* `--user-id UUID`: Contact id  [required]
* `--role TEXT`: Contact role  [required]
* `--account TEXT`: Account override (root only).
* `-o, --output [json|yaml|toml|text]`: Output format  [default: json]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

## `neosctl storage`

Interact with Storage (as a service).

**Usage**:

```console
$ neosctl storage [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `bucket`: Manage object buckets.
* `object`: Manage objects.

### `neosctl storage bucket`

Manage object buckets.

**Usage**:

```console
$ neosctl storage bucket [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create new bucket.
* `delete`: Delete bucket.
* `list`: List buckets.

#### `neosctl storage bucket create`

Create new bucket.

**Usage**:

```console
$ neosctl storage bucket create [OPTIONS] BUCKET_NAME
```

**Arguments**:

* `BUCKET_NAME`: Bucket name  [required]

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl storage bucket delete`

Delete bucket.

**Usage**:

```console
$ neosctl storage bucket delete [OPTIONS] BUCKET_NAME
```

**Arguments**:

* `BUCKET_NAME`: Bucket name  [required]

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl storage bucket list`

List buckets.

**Usage**:

```console
$ neosctl storage bucket list [OPTIONS]
```

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

### `neosctl storage object`

Manage objects.

**Usage**:

```console
$ neosctl storage object [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `copy`: List objects.
* `create`: Create object.
* `delete`: Delete object.
* `get`: Get object.
* `list`: List objects.
* `tags`: Manage object tags.

#### `neosctl storage object copy`

List objects.

**Usage**:

```console
$ neosctl storage object copy [OPTIONS] BUCKET_NAME TARGET_BUCKET_NAME
```

**Arguments**:

* `BUCKET_NAME`: Bucket name  [required]
* `TARGET_BUCKET_NAME`: Bucket name  [required]

**Options**:

* `--prefix TEXT`: Path prefix
* `--target-prefix TEXT`: Target path prefix
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl storage object create`

Create object.

**Usage**:

```console
$ neosctl storage object create [OPTIONS] BUCKET_NAME OBJECT_NAME FILE
```

**Arguments**:

* `BUCKET_NAME`: Bucket name  [required]
* `OBJECT_NAME`: Object name  [required]
* `FILE`: Path to the object file.  [required]

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl storage object delete`

Delete object.

**Usage**:

```console
$ neosctl storage object delete [OPTIONS] BUCKET_NAME OBJECT_NAME
```

**Arguments**:

* `BUCKET_NAME`: Bucket name  [required]
* `OBJECT_NAME`: Object name  [required]

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl storage object get`

Get object.

**Usage**:

```console
$ neosctl storage object get [OPTIONS] BUCKET_NAME OBJECT_NAME FILE
```

**Arguments**:

* `BUCKET_NAME`: Bucket name  [required]
* `OBJECT_NAME`: Object name  [required]
* `FILE`: Path to file where to store the object.  [required]

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl storage object list`

List objects.

**Usage**:

```console
$ neosctl storage object list [OPTIONS] BUCKET_NAME
```

**Arguments**:

* `BUCKET_NAME`: Bucket name  [required]

**Options**:

* `--prefix TEXT`: Path prefix
* `--recursive / --no-recursive`: Recursively list bucket contents  [default: no-recursive]
* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

#### `neosctl storage object tags`

Manage object tags.

**Usage**:

```console
$ neosctl storage object tags [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `delete`: Delete object tags.
* `get`: Get object tags.
* `set`: Set object tags.

##### `neosctl storage object tags delete`

Delete object tags.

**Usage**:

```console
$ neosctl storage object tags delete [OPTIONS] BUCKET_NAME OBJECT_NAME
```

**Arguments**:

* `BUCKET_NAME`: Bucket name  [required]
* `OBJECT_NAME`: Object name  [required]

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

##### `neosctl storage object tags get`

Get object tags.

**Usage**:

```console
$ neosctl storage object tags get [OPTIONS] BUCKET_NAME OBJECT_NAME
```

**Arguments**:

* `BUCKET_NAME`: Bucket name  [required]
* `OBJECT_NAME`: Object name  [required]

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.

##### `neosctl storage object tags set`

Set object tags. Be aware that this command overwrites any tags that are already set to the object.

**Usage**:

```console
$ neosctl storage object tags set [OPTIONS] BUCKET_NAME OBJECT_NAME TAGS...
```

**Arguments**:

* `BUCKET_NAME`: Bucket name  [required]
* `OBJECT_NAME`: Object name  [required]
* `TAGS...`: Tags as pairs of key=value  [required]

**Options**:

* `-v, --verbose`: Verbose output. Use multiple times to increase level of verbosity.  [default: 0; x<=3]
* `--help`: Show this message and exit.
