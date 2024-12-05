# © Copyright 2024 Hewlett Packard Enterprise Development LP
from argparse import Namespace
from typing import Any, List

import aiolirest
from aioli import cli
from aioli.cli import render
from aioli.common.api import authentication
from aioli.common.declarative_argparse import Arg, Cmd, Group
from aiolirest.models.role_assignment import RoleAssignment
from aiolirest.models.role_assignments import RoleAssignments


@authentication.required
def list_roles(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.RolesApi(session)
        response = api_instance.roles_get()

    headers = [
        "ID",
        "Role Name",
    ]

    if args.json:
        render.print_json([r.to_dict() for r in response])
    elif args.yaml:
        print(render.format_object_as_yaml([r.to_dict() for r in response]))
    else:
        values = [[r.id, r.role_name] for r in response]
        render.tabulate_or_csv(headers, values, args.csv)


@authentication.required
def list_user_roles(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.RolesApi(session)
        response = api_instance.roles_assignments_get(args.username)

    headers = [
        "User Name",
        "Role Name",
    ]

    if args.json:
        render.print_json([r.to_dict() for r in response])
    elif args.yaml:
        print(render.format_object_as_yaml([r.to_dict() for r in response]))
    else:
        values = [[r.user_name, r.role_name] for r in response]
        render.tabulate_or_csv(headers, values, args.csv)


@authentication.required
def assign_role(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.RolesApi(session)

    assignments = []
    assignments.append(RoleAssignment(userName=args.u, roleName=args.role))

    api_instance.roles_add_assignments_post(RoleAssignments(userRoleAssignments=assignments))


@authentication.required
def unassign_role(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.RolesApi(session)

    assignments = []
    assignments.append(RoleAssignment(userName=args.u, roleName=args.role))

    api_instance.roles_remove_assignments_post(RoleAssignments(userRoleAssignments=assignments))


main_cmd = Cmd(
    "rbac",
    None,
    "role management",
    [
        Cmd(
            "list-roles ls",
            list_roles,
            "list roles",
            [
                Group(
                    Arg("--csv", action="store_true", help="print as CSV"),
                    Arg("--json", action="store_true", help="print as JSON"),
                    Arg("--yaml", action="store_true", help="print as YAML"),
                ),
            ],
            is_default=True,
        ),
        Cmd(
            "list-user-roles lu",
            list_user_roles,
            "list roles for a user",
            [
                Arg("username", help="The name of the user"),
                Group(
                    Arg("--csv", action="store_true", help="print as CSV"),
                    Arg("--json", action="store_true", help="print as JSON"),
                    Arg("--yaml", action="store_true", help="print as YAML"),
                ),
            ],
        ),
        Cmd(
            "assign-role",
            assign_role,
            "assign a role to a user",
            [
                Arg(
                    "role",
                    help="role name",
                ),
                Arg("-u", help="The name of the user", required="true"),
            ],
        ),
        Cmd(
            "unassign-role",
            unassign_role,
            "unassign a role for a user",
            [
                Arg(
                    "role",
                    help="role name",
                ),
                Arg("-u", help="The name of the user", required="true"),
            ],
        ),
    ],
)


args_description = [main_cmd]  # type: List[Any]
