"""Constant values for neosctl."""

import pathlib
from enum import Enum

ENV_FILENAME = "env"
CREDENTIAL_FILENAME = "credential"
LOG_FILENAME = "error.log"
ROOT_FILEPATH = pathlib.Path().home() / ".neosctl"
ENV_FILEPATH = ROOT_FILEPATH / ENV_FILENAME
CREDENTIAL_FILEPATH = ROOT_FILEPATH / CREDENTIAL_FILENAME
LOG_FILEPATH = ROOT_FILEPATH / LOG_FILENAME


SUCCESS_CODE = 200
REDIRECT_CODE = 300
BAD_REQUEST_CODE = 400
UNAUTHORISED_CODE = 401

GATEWAY = "gateway"
REGISTRY = "registry"
IAM = "iam"


class Output(Enum):
    """Supported output formats."""

    json = "json"
    yaml = "yaml"
    toml = "toml"
    text = "text"
