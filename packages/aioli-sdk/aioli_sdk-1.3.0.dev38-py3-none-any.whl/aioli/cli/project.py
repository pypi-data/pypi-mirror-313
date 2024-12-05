# © Copyright 2024 Hewlett Packard Enterprise Development LP
from argparse import Namespace
from typing import Any, Dict, List

import aiolirest
from aioli import cli
from aioli.cli import render
from aioli.common.api import authentication
from aioli.common.api.errors import NotFoundException
from aioli.common.declarative_argparse import Arg, Cmd, Group
from aiolirest.models.project import Project
from aiolirest.models.project_request import ProjectRequest
from aiolirest.models.user_session import UserSession


@authentication.required
def list_projects(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.ProjectsApi(session)
        response = api_instance.projects_get()

    if args.json:
        render.print_json(format_json(response))
    elif args.yaml:
        print(render.format_object_as_yaml(format_json(response)))
    else:
        headers = ["Name", "Description", "Owner"]
        values = [[p.name, p.description, p.owner] for p in response]
        values.sort()  # sort values by the first column
        render.tabulate_or_csv(headers, values, args.csv)


def format_json(response: List[Project]) -> List[Dict[str, str]]:
    return [project_to_dict(r) for r in response]


def project_to_dict(project: Project) -> Dict[str, str]:
    # Don't use the r.to_json() method as it adds backslash escapes for double quotes
    d: Dict[str, str] = project.to_dict()
    d.pop("id")
    d.pop("modifiedAt")
    return d


@authentication.required
def create_project(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.ProjectsApi(session)

        project_request = ProjectRequest(
            name=args.name,
            description=args.description,
            owner=args.owner,
        )
        api_instance.projects_post(project_request)


@authentication.required
def update_project(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.ProjectsApi(session)
        found = lookup_project(args.projectname, api_instance)
        request = ProjectRequest(
            name=found.name,
            description=found.description,
            owner=found.owner,
        )
        if args.name is not None:
            request.name = args.name

        if args.description is not None:
            request.description = args.description

        if args.owner is not None:
            request.owner = args.owner

        headers = {"Content-Type": "application/json"}
        assert found.id is not None
        api_instance.projects_id_put(found.id, request, _headers=headers)


@authentication.required
def delete_project(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.ProjectsApi(session)
        found = lookup_project(args.name, api_instance)
        assert found.id is not None
        api_instance.projects_id_delete(found.id)


@authentication.required
def show_project(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.ProjectsApi(session)

    project = lookup_project(args.name, api_instance)

    d = project.to_dict()
    if args.json:
        render.print_json(d)
    else:
        print(render.format_object_as_yaml(d))


def lookup_project(name: str, api: aiolirest.ProjectsApi) -> Project:
    for p in api.projects_get():
        if p.name == name:
            return p
    raise NotFoundException(f"Project {name} not found")


def lookup_project_by_id(project_id: str, api: aiolirest.ProjectsApi) -> Project:
    p = api.projects_id_get(project_id)
    if p.id != project_id:
        NotFoundException(f"Project {project_id} not found")
    return p


@authentication.required
def activate_project(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.AuthenticationApi(session)
        user_session: UserSession = UserSession(project=args.name)
        api_instance.session_put(user_session=user_session)


@authentication.required
def clear_project(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.AuthenticationApi(session)
        user_session: UserSession = UserSession(project=None)
        api_instance.session_put(user_session=user_session)


@authentication.required
def display_project(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.AuthenticationApi(session)
        user_session: UserSession = api_instance.session_get()
        if user_session.project is None or user_session.project == "":
            print("No project set")
            return
        print(lookup_project_by_id(user_session.project, aiolirest.ProjectsApi(session)).name)


main_cmd = Cmd(
    "projects p|roject",
    None,
    "Manage projects",
    [
        Cmd(
            "list ls",
            list_projects,
            "list all projects",
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
            "create",
            create_project,
            "create a new project",
            [
                Arg(
                    "name",
                    help="The name of the project. Must begin with a letter and may "
                    "contain letters, numbers, and hyphens.",
                ),
                Arg("--description", help="The description of the project"),
                Arg("--owner", help="The owner of the project"),
            ],
        ),
        Cmd(
            "update",
            update_project,
            "update an existing project",
            [
                Arg("projectname", help="The current name of the project"),
                Arg(
                    "--name",
                    help="The new name of the project. Must begin with a letter and may "
                    "contain letters, numbers, and hyphens.",
                ),
                Arg("--description", help="The new description of the project"),
                Arg("--owner", help="The new owner of the project"),
            ],
        ),
        Cmd(
            "delete",
            delete_project,
            "delete a project",
            [
                Arg("name", help="The name of the project to delete"),
            ],
        ),
        Cmd(
            "show",
            show_project,
            "show details of a project",
            [
                Arg("name", help="The name of the project"),
                Group(
                    Arg("--yaml", action="store_true", help="print as YAML", default=True),
                    Arg("--json", action="store_true", help="print as JSON"),
                ),
            ],
        ),
        Cmd(
            "set|-for-session",
            activate_project,
            "set the project for the current session, limiting future commands to show and affect "
            "resources from that project only.",
            [
                Arg("name", help="The name of the project"),
            ],
        ),
        Cmd(
            "clear|-for-session",
            clear_project,
            "clear the project from the current session.  Display all resources.  New resources "
            "will be created in the default project limiting future commands to show and affect "
            "resources from the default project only.",
            [],
        ),
        Cmd("display|-for-session", display_project, "display the current session project", []),
    ],
)

args_description = [main_cmd]  # type: List[Any]
