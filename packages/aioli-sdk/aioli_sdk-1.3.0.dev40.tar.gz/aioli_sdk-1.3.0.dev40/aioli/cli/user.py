# © Copyright 2024 Hewlett Packard Enterprise Development LP
import getpass
from argparse import Namespace
from typing import Any, Dict, List

import aiolirest
from aioli import cli
from aioli.cli import errors, render
from aioli.common.api import authentication, certs
from aioli.common.api.errors import NotFoundException
from aioli.common.declarative_argparse import Arg, Cmd, Group, string_to_bool
from aiolirest.api import UsersApi
from aiolirest.models.user import User
from aiolirest.models.user_patch_request import UserPatchRequest
from aiolirest.models.user_request import UserRequest


@authentication.required
def list_users(args: Namespace) -> None:
    projects = {}
    with cli.setup_session(args) as session:
        api_instance = aiolirest.UsersApi(session)
        response = api_instance.users_get()
        for project in aiolirest.ProjectsApi(session).projects_get():
            projects[project.id] = project

    def format_json(response: List[User]) -> List[Dict[str, str]]:
        users = []
        for r in response:
            # Don't use the r.to_json() method as it adds backslash escapes for double quote
            d = r.to_dict()
            users.append(d)
        return users

    def format_user(u: User) -> List[Any]:
        project = ""
        if u.default_project and projects[u.default_project]:
            project = projects[u.default_project].name
        result = [u.username, u.display_name, u.active, u.remote, project]
        return result

    if args.json:
        render.print_json(format_json(response))
    elif args.yaml:
        print(render.format_object_as_yaml(format_json(response)))
    else:
        headers = ["Username", "Display Name", "Active", "Remote", "Default Project"]
        values = [format_user(u) for u in response]
        render.tabulate_or_csv(headers, values, args.csv)


@authentication.required
def activate_user(parsed_args: Namespace) -> None:
    patch = UserPatchRequest(active=True)
    patch_user(parsed_args, parsed_args.username, patch)


@authentication.required
def deactivate_user(parsed_args: Namespace) -> None:
    patch = UserPatchRequest(active=False)
    patch_user(parsed_args, parsed_args.username, patch)


def patch_user(
    parsed_args: Namespace,
    username: str,
    patch_data: UserPatchRequest,
) -> None:
    with cli.setup_session(parsed_args) as session:
        api_instance = aiolirest.UsersApi(session)

    user = get_user_by_name(username, api_instance)

    assert user.id is not None

    api_instance.users_id_patch(id=user.id, user_patch_request=patch_data)


def get_user_by_name(username: str, api_instance: UsersApi) -> User:
    for u in api_instance.users_get():
        if u.username == username:
            return u
    raise NotFoundException(f"user {username} not found")


def log_in_user(parsed_args: Namespace) -> None:
    if parsed_args.username is None:
        username = input("Username: ")
    else:
        username = parsed_args.username

    message = "Password for user '{}': ".format(username)
    password = getpass.getpass(message)

    token_store = authentication.TokenStore(parsed_args.controller)

    try:
        token = authentication.do_login(
            parsed_args.controller,
            username,
            authentication.salt_and_hash(password),
            True,
            certs.cli_cert,
        )
    except aiolirest.exceptions.ForbiddenException:
        # log in request was possibly for user that was created before INF-851,
        # retry log in using the password without apply salt_and_hash
        token = authentication.do_login(
            parsed_args.controller, username, password, False, certs.cli_cert
        )

    token_store.set_token(username, token)
    token_store.set_active(username)


@authentication.required
def log_out_user(parsed_args: Namespace) -> None:
    if parsed_args.all:
        authentication.logout_all(parsed_args.controller, certs.cli_cert)
    else:
        # Log out of the user specified by the command line, or the active user.
        authentication.logout(parsed_args.controller, parsed_args.user, certs.cli_cert)


@authentication.required
def change_password(parsed_args: Namespace) -> None:
    if parsed_args.target_user:
        username = parsed_args.target_user
    elif parsed_args.user:
        username = parsed_args.user
    elif authentication.cli_auth is not None:
        username = authentication.cli_auth.get_session_user()

    if not username:
        # The default user should have been set by now by autologin.
        raise errors.CliError("Please log in as an admin or user to change passwords")
    password = getpass.getpass("New password for user '{}': ".format(username))
    check_password = getpass.getpass("Confirm password: ")

    if password != check_password:
        raise errors.CliError("Passwords do not match")

    password = authentication.salt_and_hash(password)
    patch_data = UserPatchRequest(password=password, isHashed=True)

    patch_user(parsed_args, username, patch_data)

    # If the target user's password isn't being changed by another user, reauthenticate after
    # password change so that the user doesn't have to do so manually.
    if parsed_args.target_user is None:
        token_store = authentication.TokenStore(parsed_args.controller)
        token = authentication.do_login(
            parsed_args.controller, username, password, True, certs.cli_cert
        )
        token_store.set_token(username, token)
        token_store.set_active(username)


@authentication.required
def create_user(parsed_args: Namespace) -> None:
    with cli.setup_session(parsed_args) as session:
        api_instance = aiolirest.UsersApi(session)

    remote = parsed_args.remote
    display_name: str = parsed_args.display_name
    if display_name is None:
        display_name = ""

    role_name: str = parsed_args.role
    if role_name is None:
        role_name = "Viewer"

    password: str = parsed_args.password
    if not remote and password is None:
        password = getpass.getpass("Password for user '{}': ".format(parsed_args.username))
        check_password = getpass.getpass("Confirm password: ")

        if password != check_password:
            raise errors.CliError("Passwords do not match")

    new_user = UserRequest(
        username=parsed_args.username,
        active=True,
        displayName=display_name,
        remote=remote,
        roleName=role_name,
        password=authentication.salt_and_hash(password),
        isHashed=True,
    )
    api_instance.users_post(user=new_user)


@authentication.required
def update(parsed_args: Namespace) -> None:
    changes = []
    patch = UserPatchRequest()

    if parsed_args.username is not None:
        patch.username = parsed_args.username
        changes.append("Username")

    if parsed_args.display_name is not None:
        patch.display_name = parsed_args.display_name
        changes.append("Display Name")

    if parsed_args.activate is not None:
        patch.active = parsed_args.activate
        changes.append("Active")

    if parsed_args.default_project is not None:
        patch.default_project = parsed_args.default_project
        changes.append("Default Project")

    if len(changes) > 0:
        patch_user(parsed_args, parsed_args.target_user, patch)
        print("Changes made to the following fields: " + ", ".join(changes))
    else:
        raise errors.CliError("No field provided. Use 'aioli user update -h' for usage.")


@authentication.required
def whoami(parsed_args: Namespace) -> None:
    with cli.setup_session(parsed_args) as session:
        api_instance = aiolirest.UsersApi(session)
        user = api_instance.users_me_get()

    print("You are logged in as user '{}'".format(user.username))


@authentication.required
def delete(parsed_args: Namespace) -> None:
    with cli.setup_session(parsed_args) as session:
        api_instance = aiolirest.UsersApi(session)
        found = get_user_by_name(parsed_args.username, api_instance)
        assert found.id is not None
        api_instance.users_id_delete(int(found.id))


# fmt: off
args_description = [
    Cmd("u|ser", None, "manage users", [
        Cmd("list ls", list_users, "list users",
            [
                Group(
                    Arg("--csv", action="store_true", help="print as CSV"),
                    Arg("--json", action="store_true", help="print as JSON"),
                    Arg("--yaml", action="store_true", help="print as YAML"),
                ),
            ],
            is_default=True),
        Cmd("login", log_in_user, "log in user", [
            Arg("username", nargs="?", default=None, help="name of user to log in as")
        ]),
        Cmd("change-password", change_password, "change password for user", [
            Arg("target_user", nargs="?", default=None, help="name of user to change password of")
        ]),
        Cmd("logout", log_out_user, "log out user", [
            Arg(
                "--all",
                "-a",
                action="store_true",
                help="log out of all cached sessions for the current controller",
            ),
        ]),
        Cmd("activate", activate_user, "activate user", [
            Arg("username", help="name of user to activate")
        ]),
        Cmd("deactivate", deactivate_user, "deactivate user", [
            Arg("username", help="name of user to deactivate")
        ]),
        Cmd("create", create_user, "create user", [
            Arg("username", help="name of new user"),
            Arg("--password", help="password of the new user"),
            Arg("--display-name", default=None, help="new display name for target_user"),
            Arg("--remote", action="store_true",
                help="disallow using passwords, user must use the configured external IdP"),
            Arg("--role", help="assign a role to the created user"),
        ]),
        Cmd("whoami", whoami, "print the active user", []),
        Cmd("update", update, "update user fields", [
            Arg(
                "target_user",
                default=None,
                help="name of user that should be updated"
            ),
            Arg("--display-name", default=None, help="new display name for target_user"),
            Arg("--username", default=None, help="new username for target_user"),
            Arg("--default-project", default=None, help="new default project for target_user"),
            Arg(
                "--active",
                dest="activate",
                type=string_to_bool,
                metavar="(true|false)",
                default=None,
                help="set user as active/inactive",
            ),
        ]),
        Cmd("delete", delete, "delete user", [
            Arg("username", help="name of user to delete")
        ]),
    ])
]  # type: List[Any]

# fmt: on
