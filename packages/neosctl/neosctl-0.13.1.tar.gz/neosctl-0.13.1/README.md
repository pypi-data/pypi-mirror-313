# Core CLI v0.13.1

## Setup

### Install CLI

Install the CLI using [pip](https://pypi.org/project/neosctl/):

```bash
pip install neosctl
```

See [Local Development](https://github.com/NEOS-Critical/neos-platform-cli/tree/main/DEVELOP.md) for details on installing from source.

### Setup environment

To setup an environment, run the following command:

```bash
neosctl env init <env-name> -h <hub-host> -u <username> -a <account>
```
More information about this command you can find in the [DOCS.md](https://github.com/NEOS-Critical/neos-platform-cli/tree/main/DOCS.md) file.

### Activate an environment
To activate an environment (for use in subsequent requests):

```bash
neosctl env activate <env-name>
```

### Login to the system

To login to the system, run the following command:

```bash
neosctl env login
```

You will need username and password for that.

### Activate a core
To activate a core (for use in subsequent requests):

```bash
neoctl env list-cores
neosctl env activate-core <core-name>
```

### Setup service user (optional)

For some operations, you will need to provide a service user `access_key_id`
and `secret_access_key`. To create service user and get it's access and secret
key, use:

```bash
neosctl env whoami

{
  "user_id": "<user-id>"
}
```

```bash
neosctl iam user create-access-key <user-id>
```

To configure the environment to use the key pair:

```bash
neosctl env credential <env-name> <access-key> <secret-key>
```

### Review settings

All setting are stored by default in the folder `~/.neosctl/`.

You can also review all settings by running the following commands:

```bash
neosctl env list
neosctl env view <env-name>
neosctl env active
```

## Usage

To see all available commands, run the following command:

```bash
neosctl --help
```

or go to the [DOCS.md](https://github.com/NEOS-Critical/neos-platform-cli/tree/main/DOCS.md) file.
