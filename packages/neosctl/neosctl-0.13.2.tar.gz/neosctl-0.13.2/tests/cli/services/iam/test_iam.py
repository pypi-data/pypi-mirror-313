import json
from uuid import uuid4

from tests.helper import render_cmd_output

USER_ID = uuid4()
ACCOUNT_URL = "https://hub-host/api/hub/iam/account"
POLICY_USERS_URL = "https://hub-host/api/hub/iam/policy/users"
POLICY_USER_URL = "https://hub-host/api/hub/iam/policy/user"
GROUP_URL = "https://hub-host/api/hub/iam/group"
USER_URL = "https://hub-host/api/hub/iam/user"
USERS_URL = "https://hub-host/api/hub/iam/users"
RESET_PASSWORD_URL = "https://hub-host/api/hub/iam/user/password/reset"  # nosec: B105


def test_account_create(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="POST",
        url=ACCOUNT_URL,
        json=response_payload,
        match_content=b'{"name": "name", "display_name": "display name", "description": "description", "owner": "owner"}',  # noqa: E501
    )

    result = cli_runner.invoke(
        [
            "iam",
            "account",
            "create",
            "-d",
            "display name",
            "-n",
            "name",
            "--desc",
            "description",
            "--owner",
            "owner",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_account_delete(cli_runner, httpx_mock):
    identifier = uuid4()

    response_payload = {
        "identifier": str(identifier),
        "urn": f"nrn:ksa:iam::root:account:{identifier}",
        "name": "foo",
        "display_name": "foo",
        "description": "description",
        "owner": "foo",
        "is_system": False,
    }

    httpx_mock.add_response(
        method="DELETE",
        url=f"{ACCOUNT_URL}/{identifier}",
        json=response_payload,
    )

    result = cli_runner.invoke(
        [
            "iam",
            "account",
            "delete",
            str(identifier),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_account_update(cli_runner, httpx_mock):
    identifier = uuid4()

    response_payload = {
        "identifier": str(identifier),
        "urn": f"nrn:ksa:iam::root:account:{identifier}",
        "name": "foo",
        "display_name": "updated",
        "description": "updated",
        "owner": "updated",
        "is_system": False,
    }

    httpx_mock.add_response(
        method="PUT",
        url=f"{ACCOUNT_URL}/{identifier}",
        json=response_payload,
        match_content=b'{"display_name": "updated", "description": "updated", "owner": "updated"}',
    )

    result = cli_runner.invoke(
        [
            "iam",
            "account",
            "update",
            "-d",
            "updated",
            "--desc",
            "updated",
            "--owner",
            "updated",
            str(identifier),
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_account_list(cli_runner, httpx_mock):
    response_payload = {"accounts": []}

    httpx_mock.add_response(
        method="GET",
        url=ACCOUNT_URL,
        json=response_payload,
        headers={"X-Account": "root"},
    )

    result = cli_runner.invoke(["iam", "account", "list"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_policy_list(cli_runner, httpx_mock):
    response_payload = {
        "user_policies": [
            {
                "policy": {
                    "statements": [
                        {
                            "action": [
                                "product:create",
                                "product:manage",
                            ],
                            "condition": [],
                            "effect": "allow",
                            "principal": [
                                "nrn:ksa:iam::root:user/ann",
                            ],
                            "resource": [
                                "nrn:ksa:product:core:root:product",
                            ],
                            "sid": "allow_all",
                        },
                        {
                            "action": [
                                "product:browse",
                            ],
                            "condition": [],
                            "effect": "allow",
                            "principal": [
                                "nrn:ksa:iam::root:user/ann",
                            ],
                            "resource": [
                                "nrn:ksa:product:core:root:product/my-dp1",
                                "nrn:ksa:product:core:root:product/my-dp2",
                            ],
                            "sid": "allow_one",
                        },
                    ],
                    "version": "2022-10-01",
                },
                "user": "nrn:ksa:iam::root:user/ann",
            },
        ],
    }

    httpx_mock.add_response(
        method="GET",
        url=f"{POLICY_USERS_URL}?page=1&page_size=10",
        json=response_payload,
        headers={"X-Account": "root"},
    )

    result = cli_runner.invoke(["iam", "policy", "list"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_policy_list_account_override(cli_runner, httpx_mock):
    response_payload = {
        "user_policies": [
            {
                "policy": {
                    "statements": [
                        {
                            "action": [
                                "product:create",
                                "product:manage",
                            ],
                            "condition": [],
                            "effect": "allow",
                            "principal": [
                                "nrn:ksa:iam::root:user/ann",
                            ],
                            "resource": [
                                "nrn:ksa:product:core:root:product",
                            ],
                            "sid": "allow_all",
                        },
                        {
                            "action": [
                                "product:browse",
                            ],
                            "condition": [],
                            "effect": "allow",
                            "principal": [
                                "nrn:ksa:iam::root:user/ann",
                            ],
                            "resource": [
                                "nrn:ksa:product:core:root:product/my-dp1",
                                "nrn:ksa:product:core:root:product/my-dp2",
                            ],
                            "sid": "allow_one",
                        },
                    ],
                    "version": "2022-10-01",
                },
                "user": "nrn:ksa:iam::root:user/ann",
            },
        ],
    }

    httpx_mock.add_response(
        method="GET",
        url=f"{POLICY_USERS_URL}?page=1&page_size=10",
        json=response_payload,
        headers={"X-Account": "root", "X-Account-Override": "test"},
    )

    result = cli_runner.invoke(["iam", "policy", "list", "--account", "test"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_policy_list_with_resource(cli_runner, httpx_mock):
    response_payload = {
        "user_policies": [
            {
                "policy": {
                    "statements": [
                        {
                            "action": [
                                "product:create",
                                "product:manage",
                            ],
                            "condition": [],
                            "effect": "allow",
                            "principal": [
                                "nrn:ksa:iam::root:user/ann",
                            ],
                            "resource": [
                                "nrn:ksa:product:core:root:product",
                            ],
                            "sid": "allow_all",
                        },
                    ],
                },
            },
        ],
    }

    httpx_mock.add_response(
        method="GET",
        url=f"{POLICY_USERS_URL}?page=1&page_size=10&resource=nrn%3Aksa%3Aproduct%3Acore%3Aroot%3Aproduct",
        json=response_payload,
    )

    result = cli_runner.invoke(["iam", "policy", "list", "--resource=nrn:ksa:product:core:root:product"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_policy_create_from_json(cli_runner, httpx_mock, tmp_path):
    response_payload = {}
    httpx_mock.add_response(
        method="POST",
        url=POLICY_USER_URL,
        json=response_payload,
    )

    fp = tmp_path / "user_policy.json"
    with fp.open("w") as f:
        json.dump(
            {
                "policy": {
                    "statements": [
                        {
                            "sid": "VTHOEXIM",
                            "effect": "allow",
                            "principal": str(USER_ID),
                            "action": [
                                "product:browse",
                            ],
                            "resource": [
                                "nrn:ksa:core:smartconstruction:root:product/my-dp-1",
                            ],
                            "condition": [],
                        },
                    ],
                    "version": "2022-10-01",
                },
                "user": str(USER_ID),
            },
            f,
        )

    result = cli_runner.invoke(["iam", "policy", "create", str(fp.resolve())])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_policy_create_from_json_missing(cli_runner, tmp_path):
    fp = tmp_path / "user_policy.json"

    result = cli_runner.invoke(["iam", "policy", "create", str(fp.resolve())])

    assert result.exit_code == 1
    assert result.output == f"Can not find file: {fp.resolve()}\n"


def test_policy_create_from_non_json(cli_runner, tmp_path):
    fp = tmp_path / "user_policy.json"
    with fp.open("w") as f:
        f.write("not a json format")

    result = cli_runner.invoke(["iam", "policy", "create", str(fp.resolve())])

    assert result.exit_code == 1
    assert result.output == "Invalid policy file, must be json format.\n"


def test_policy_update_from_json(cli_runner, httpx_mock, tmp_path):
    response_payload = {}
    httpx_mock.add_response(
        method="PUT",
        url="{}?user_nrn={}".format(POLICY_USER_URL, "cf061980-74b9-4c9b-a8ae-7817c7133068"),
        json=response_payload,
    )

    fp = tmp_path / "user_policy.json"
    with fp.open("w") as f:
        json.dump(
            {
                "policy": {
                    "statements": [
                        {
                            "sid": "VTHOEXIM",
                            "effect": "allow",
                            "principal": "cf061980-74b9-4c9b-a8ae-7817c7133068",
                            "action": [
                                "product:browse",
                            ],
                            "resource": [
                                "nrn:ksa:core:smartconstruction:root:product/my-dp-1",
                            ],
                            "condition": [],
                        },
                    ],
                    "version": "2022-10-01",
                },
                "user": "cf061980-74b9-4c9b-a8ae-7817c7133068",
            },
            f,
        )

    result = cli_runner.invoke(["iam", "policy", "update", "cf061980-74b9-4c9b-a8ae-7817c7133068", str(fp.resolve())])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_policy_update_from_unknown_file(cli_runner, tmp_path):
    fp = tmp_path / "dp.json"

    result = cli_runner.invoke(["iam", "policy", "update", "cf061980-74b9-4c9b-a8ae-7817c7133068", str(fp.resolve())])

    assert result.exit_code == 1
    assert result.output == f"Can not find file: {fp.resolve()}\n"


def test_policy_update_from_non_json(cli_runner, tmp_path):
    fp = tmp_path / "dp.json"
    with fp.open("w") as f:
        f.write("not a json format")

    result = cli_runner.invoke(["iam", "policy", "update", "cf061980-74b9-4c9b-a8ae-7817c7133068", str(fp.resolve())])

    assert result.exit_code == 1
    assert result.output == "Invalid policy file, must be json format.\n"


def test_policy_delete(cli_runner, httpx_mock):
    user_nrn = "user_nrn"

    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url=f"{POLICY_USER_URL}?user_nrn={user_nrn}",
        json=response_payload,
    )

    result = cli_runner.invoke(["iam", "policy", "delete", user_nrn])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_policy_get(cli_runner, httpx_mock):
    user_nrn = "user_nrn"

    response_payload = {
        "user": "nrn:ksa:iam::root:user/david",
        "policy": {
            "statements": [
                {
                    "sid": "VTHOEXIM",
                    "effect": "allow",
                    "principal": [
                        "nrn:ksa:iam::root:user/david",
                    ],
                    "action": [
                        "product:browse",
                    ],
                    "resource": [
                        "nrn:ksa:core:smartconstruction:root:product/my-dp-1",
                    ],
                    "condition": [],
                },
            ],
            "version": "2022-10-01",
        },
    }

    httpx_mock.add_response(
        method="GET",
        url=f"{POLICY_USER_URL}?user_nrn={user_nrn}",
        json=response_payload,
    )

    result = cli_runner.invoke(["iam", "policy", "get", user_nrn])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_user_list(cli_runner, httpx_mock):
    response_payload = {
        "users": [
            {
                "id": "1546fb05-b12b-4cda-b49c-be591b42fde6",
                "username": "consumer.education",
                "enabled": False,
                "first_name": "consumer",
                "last_name": "education",
                "email": "consumer.education@neos.com",
            },
            {
                "id": "15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
                "username": "consumer.smartconstruction",
                "enabled": True,
                "first_name": None,
                "last_name": None,
                "email": None,
            },
        ],
    }

    httpx_mock.add_response(
        method="GET",
        url=f"{USERS_URL}",
        json=response_payload,
    )

    result = cli_runner.invoke(["iam", "user", "list"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_user_list_search(cli_runner, httpx_mock):
    response_payload = {
        "users": [
            {
                "id": "15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
                "username": "consumer.smartconstruction",
                "enabled": True,
                "first_name": None,
                "last_name": None,
                "email": None,
            },
        ],
    }

    httpx_mock.add_response(
        method="GET",
        url=f"{USERS_URL}?search=smartconstruction",
        json=response_payload,
    )

    result = cli_runner.invoke(["iam", "user", "list", "--search", "smartconstruction"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_user_permissions(cli_runner, httpx_mock):
    user_payload = {
        "users": [
            {
                "id": "15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
                "username": "smartconstruction",
                "enabled": True,
                "first_name": None,
                "last_name": None,
                "email": None,
            },
        ],
    }

    httpx_mock.add_response(
        method="GET",
        url=f"{USERS_URL}?search=smartconstruction",
        json=user_payload,
    )
    policy_payload = {
        "user": "nrn:ksa:iam::root:user:15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
        "policy": {
            "statements": [
                {
                    "sid": "VTHOEXIM",
                    "effect": "allow",
                    "principal": [
                        "nrn:ksa:iam::root:user:15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
                    ],
                    "action": [
                        "product:browse",
                    ],
                    "resource": [
                        "nrn:ksa:core:smartconstruction:root:product:my-dp-1",
                    ],
                    "condition": [],
                },
            ],
            "version": "2022-10-01",
        },
    }

    httpx_mock.add_response(
        method="GET",
        url=f"{POLICY_USER_URL}?user_nrn=15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
        json=policy_payload,
    )

    result = cli_runner.invoke(["iam", "user", "permissions", "--username", "smartconstruction"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(policy_payload)


def test_user_permissions_unknown_user(cli_runner, httpx_mock):
    user_payload = {
        "users": [],
    }

    httpx_mock.add_response(
        method="GET",
        url=f"{USERS_URL}?search=smartconstruction",
        json=user_payload,
    )

    result = cli_runner.invoke(["iam", "user", "permissions", "--username", "smartconstruction"])

    assert result.exit_code == 1
    assert result.output == "User not found.\n"


def test_user_permissions_by_id(cli_runner, httpx_mock):
    policy_payload = {
        "user": "nrn:ksa:iam::root:user:15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
        "policy": {
            "statements": [
                {
                    "sid": "VTHOEXIM",
                    "effect": "allow",
                    "principal": [
                        "nrn:ksa:iam::root:user:15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
                    ],
                    "action": [
                        "product:browse",
                    ],
                    "resource": [
                        "nrn:ksa:core:smartconstruction:root:product:my-dp-1",
                    ],
                    "condition": [],
                },
            ],
            "version": "2022-10-01",
        },
    }

    httpx_mock.add_response(
        method="GET",
        url=f"{POLICY_USER_URL}?user_nrn=15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
        json=policy_payload,
    )

    result = cli_runner.invoke(["iam", "user", "permissions", "--identifier", "15bd37e0-7cab-4bdd-b11e-ac2ef6747113"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(policy_payload)


def test_user_reset_password(cli_runner, httpx_mock):
    payload = {}

    httpx_mock.add_response(
        method="POST",
        url=f"{RESET_PASSWORD_URL}?username=test.user",
        json=payload,
    )

    result = cli_runner.invoke(["iam", "user", "reset-password", "test.user"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output(payload)


def test_user_create(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="POST",
        url=f"{USER_URL}",
        json=response_payload,
        match_content=b'{"username": "user.name", "enabled": true, "first_name": "first", "last_name": "last", "email": "email"}',  # noqa: E501
        headers={"X-Account": "root", "X-Account-Override": "test"},
    )

    result = cli_runner.invoke(
        [
            "iam",
            "user",
            "create",
            "-u",
            "user.name",
            "-e",
            "email",
            "-n",
            "first",
            "-l",
            "last",
            "--account",
            "test",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_user_delete(cli_runner, httpx_mock):
    response_payload = {}
    user_id = uuid4()
    httpx_mock.add_response(
        method="DELETE",
        url=f"{USER_URL}/{user_id}",
        json=response_payload,
        headers={"X-Account": "root", "X-Account-Override": "test"},
    )

    result = cli_runner.invoke(
        [
            "iam",
            "user",
            "delete",
            "--user-id",
            user_id,
            "--account",
            "test",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_user_purge(cli_runner, httpx_mock):
    response_payload = {}
    user_id = uuid4()
    httpx_mock.add_response(
        method="DELETE",
        url=f"{USER_URL}/{user_id}/purge",
        json=response_payload,
        headers={"X-Account": "root", "X-Account-Override": "test"},
    )

    result = cli_runner.invoke(
        [
            "iam",
            "user",
            "purge",
            "--user-id",
            user_id,
            "--account",
            "test",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_key_pair_create(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="POST",
        url=f"{USER_URL}/user_nrn/key_pair",
        json=response_payload,
        headers={"X-Account": "root", "X-Account-Override": "test"},
    )

    result = cli_runner.invoke(
        [
            "iam",
            "user",
            "create-key-pair",
            "user_nrn",
            "--account",
            "test",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_key_pair_delete(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url=f"{USER_URL}/user_nrn/key_pair/ACCESS_KEY_ID",
        json=response_payload,
        headers={"X-Account": "root", "X-Account-Override": "test"},
    )

    result = cli_runner.invoke(
        [
            "iam",
            "user",
            "delete-key-pair",
            "user_nrn",
            "ACCESS_KEY_ID",
            "--account",
            "test",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_group_create(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="POST",
        url=f"{GROUP_URL}",
        json=response_payload,
        match_content=b'{"name": "name", "description": "description"}',
        headers={"X-Account": "root", "X-Account-Override": "test"},
    )

    result = cli_runner.invoke(
        [
            "iam",
            "group",
            "create",
            "--name",
            "name",
            "--description",
            "description",
            "--account",
            "test",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_group_list(cli_runner, httpx_mock):
    response_payload = {"groups": []}
    httpx_mock.add_response(
        method="GET",
        url=f"{GROUP_URL}",
        json=response_payload,
        headers={"X-Account": "root", "X-Account-Override": "test"},
    )

    result = cli_runner.invoke(
        [
            "iam",
            "group",
            "list",
            "--account",
            "test",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_group_update(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="POST",
        url=f"{GROUP_URL}/15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
        json=response_payload,
        match_content=b'{"name": "name", "description": "description"}',
        headers={"X-Account": "root", "X-Account-Override": "test"},
    )

    result = cli_runner.invoke(
        [
            "iam",
            "group",
            "update",
            "15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
            "--name",
            "name",
            "--description",
            "description",
            "--account",
            "test",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_group_get(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="GET",
        url=f"{GROUP_URL}/15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
        json=response_payload,
        headers={"X-Account": "root", "X-Account-Override": "test"},
    )

    result = cli_runner.invoke(
        [
            "iam",
            "group",
            "get",
            "15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
            "--account",
            "test",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_group_delete(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url=f"{GROUP_URL}/15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
        json=response_payload,
        headers={"X-Account": "root", "X-Account-Override": "test"},
    )

    result = cli_runner.invoke(
        [
            "iam",
            "group",
            "delete",
            "15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
            "--account",
            "test",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_group_add_principals(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="POST",
        url=f"{GROUP_URL}/15bd37e0-7cab-4bdd-b11e-ac2ef6747113/principals",
        json=response_payload,
        match_content=b'{"principals": ["f304f517-4a5e-40a6-9d79-c4a4e31101c6", "6cbfc083-d65f-4598-9478-9565da8c9a04"]}',  # noqa: E501
        headers={"X-Account": "root", "X-Account-Override": "test"},
    )

    result = cli_runner.invoke(
        [
            "iam",
            "group",
            "add-principals",
            "15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
            "-p",
            "f304f517-4a5e-40a6-9d79-c4a4e31101c6",
            "-p",
            "6cbfc083-d65f-4598-9478-9565da8c9a04",
            "--account",
            "test",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)


def test_group_remove_principals(cli_runner, httpx_mock):
    response_payload = {}
    httpx_mock.add_response(
        method="DELETE",
        url=f"{GROUP_URL}/15bd37e0-7cab-4bdd-b11e-ac2ef6747113/principals",
        json=response_payload,
        match_content=b'{"principals": ["f304f517-4a5e-40a6-9d79-c4a4e31101c6", "6cbfc083-d65f-4598-9478-9565da8c9a04"]}',  # noqa: E501
        headers={"X-Account": "root", "X-Account-Override": "test"},
    )

    result = cli_runner.invoke(
        [
            "iam",
            "group",
            "remove-principals",
            "15bd37e0-7cab-4bdd-b11e-ac2ef6747113",
            "-p",
            "f304f517-4a5e-40a6-9d79-c4a4e31101c6",
            "-p",
            "6cbfc083-d65f-4598-9478-9565da8c9a04",
            "--account",
            "test",
        ],
    )

    assert result.exit_code == 0
    assert result.output == render_cmd_output(response_payload)
