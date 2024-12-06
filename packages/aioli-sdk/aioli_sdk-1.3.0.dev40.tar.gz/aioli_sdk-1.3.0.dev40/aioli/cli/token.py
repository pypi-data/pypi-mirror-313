# © Copyright 2024 Hewlett Packard Enterprise Development LP
import argparse
import datetime
from typing import Any, List

import aiolirest
from aioli import cli
from aioli.cli import render
from aioli.cli.errors import CliError
from aioli.common.api import authentication
from aioli.common.declarative_argparse import Arg, Cmd, Group
from aiolirest.models.deployment_token import DeploymentToken
from aiolirest.models.deployment_token_patch_request import DeploymentTokenPatchRequest
from aiolirest.models.deployment_token_request import DeploymentTokenRequest


def format_token(t: DeploymentToken) -> List[Any]:
    result = [t.id, t.description, t.username, t.deployment, t.expiration, t.revoked]
    return result


@authentication.required
def create_token(args: argparse.Namespace) -> None:
    """Create a deployment token with the provided arguments.

    Invoke the Aioli Tokens API to create the deployment token. Print the ID of the deployment
    token created on the console.

    Args:
        args: command line arguments provided by the user. The deployment name argument
        is required, and the description and expiration arguments are optional.
    """
    with cli.setup_session(args) as session:
        tokens_api = aiolirest.TokensApi(session)

    # Check the format of the expiration provided by the user. If it doesn't include a timezone,
    # convert the expiration in to the ISO 8601 format with timezone details.
    if args.expiration:
        # Continue if the expiration is in ISO 8601 format and includes timezone.
        try:
            datetime.datetime.strptime(args.expiration, "%Y-%m-%dT%H:%M:%S%z")
        except Exception:
            # else if the expiration is in date and time format or date only format,
            # convert it to ISO 8601 format with timezone.
            accepted_formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
            for datetime_format in accepted_formats:
                try:
                    # Adding astimezone method ensure we capture the user's timezone.
                    expiration_date = datetime.datetime.strptime(
                        args.expiration, datetime_format
                    ).astimezone()
                except Exception:
                    pass
                else:
                    args.expiration = expiration_date.isoformat()
                    break

    token_request = DeploymentTokenRequest(
        user=args.username,
        deployment=args.deployment,
        description=args.description,
        expiration=args.expiration,
    )
    token = tokens_api.tokens_post(request=token_request)
    print(token.id)


@authentication.required
def list_tokens(args: argparse.Namespace) -> None:
    """List active deployment tokens accessible to the current user.

    Invoke the Aioli Tokens API and fetch deployment tokens accessible to the current user.
    Only active tokens are listed by default. Adding the all flag will get all tokens for the
    all users if the user is has an admin role and all tokens for the current user otherwise.
    Format and display the deployment tokens on the console as a table by default. Output can be
    formatted as JSON or CSV based on the json or csv flag provided by the user.

    Args:
        args: command line arguments provided by the user. Includes json or csv flag to
        indicating output format. Includes all flag indicating token list should
        include all tokens for all users for admin users and all tokens for current user for other
        users.
    """
    with cli.setup_session(args) as session:
        tokens_api = aiolirest.TokensApi(session)
        if args.all:
            response = tokens_api.tokens_get(all="")
        else:
            response = tokens_api.tokens_get()

    if args.json:
        render.print_json([token.to_dict() for token in response])
    elif args.yaml:
        print(render.format_object_as_yaml([token.to_dict() for token in response]))
    else:
        headers = ["ID", "Description", "Username", "Deployment", "Expiration", "Revoked"]
        values = [format_token(t) for t in response]
        render.tabulate_or_csv(headers, values, args.csv)


@authentication.required
def get_token(args: argparse.Namespace) -> None:
    """Get the deployment token with the provided ID.

    Invoke the Aioli Tokens API to get the deployment token with the provided ID. Display the
    deployment token details in JSON format on the console.

    Args:
        args: command line arguments provided by the user. Includes ID for the deployment
        token.
    """
    with cli.setup_session(args) as session:
        tokens_api = aiolirest.TokensApi(session)
        token = tokens_api.tokens_id_get(args.id)
        if args.json:
            render.print_json(token.to_json())
        else:
            token_yaml = render.format_object_as_yaml(token.to_dict())
            print(token_yaml)


@authentication.required
def delete_token(args: argparse.Namespace) -> None:
    """Delete the deployment token with the provided ID.

    Invoke the Aioli Tokens API to delete the deployment token with the provided ID.

    Args:
        args: command line arguments provided by the user. Includes ID for the deployment
        token.
    """
    with cli.setup_session(args) as session:
        tokens_api = aiolirest.TokensApi(session)
        tokens_api.tokens_id_delete(args.id)


@authentication.required
def update_token(args: argparse.Namespace) -> None:
    """Update the description for the deployment token with the provided ID.

    Invoke the Aioli Tokens API to update the description for the deployment token with the
    provided ID.

    Args:
        args: command line arguments provided by the user. It contains deployment token ID
        and description.
    """
    if not args.description:
        raise CliError("No description provided. Use 'aioli token update -h' for usage.")
    with cli.setup_session(args) as session:
        tokens_api = aiolirest.TokensApi(session)
        token_patch_request = DeploymentTokenPatchRequest(
            description=args.description,
        )
        tokens_api.tokens_id_patch(args.id, token_patch_request)


@authentication.required
def revoke_token(args: argparse.Namespace) -> None:
    """Revoke the deployment token with the provided ID.

    Invoke the Aioli Tokens API to revoke the deployment token with the provided ID.

    Args:
        args: command line arguments provided by the user. Includes ID for the deployment
        token to be revoked.
    """
    with cli.setup_session(args) as session:
        tokens_api = aiolirest.TokensApi(session)
        token_patch_request = DeploymentTokenPatchRequest(
            revoked=True,
        )
        tokens_api.tokens_id_patch(args.id, token_patch_request)


args_description = [
    Cmd(
        "t|oken|s",
        None,
        "manage deployment tokens",
        [
            Cmd(
                "create",
                create_token,
                "create deployment token",
                [
                    Arg(
                        "deployment",
                        help="The deployment for which the token will be created.",
                    ),
                    Arg(
                        "--username",
                        help="The username for whom the token will be created. "
                        "If no username is provided, the current user's username will be used.",
                    ),
                    Arg(
                        "--description",
                        help="Description for the deployment token. "
                        "Enclose in quotes if the description contains spaces.",
                    ),
                    Arg("--expiration", help="Expiration date for the token."),
                ],
            ),
            Cmd(
                "list ls",
                list_tokens,
                "list the deployment tokens",
                [
                    Group(
                        Arg("--csv", action="store_true", help="print as CSV"),
                        Arg("--json", action="store_true", help="print as JSON"),
                        Arg("--yaml", action="store_true", help="print as YAML"),
                    ),
                    Arg(
                        "--all",
                        action="store_true",
                        help="Get all tokens for all users if you have an Admin role. Otherwise, "
                        "get all tokens accessible to you.",
                    ),
                ],
                is_default=True,
            ),
            Cmd(
                "show",
                get_token,
                "show the details of the deployment token with given ID",
                [
                    Arg("id", help="ID of the token"),
                    Group(
                        Arg("--json", action="store_true", help="print as JSON"),
                        Arg("--yaml", action="store_true", help="print as YAML"),
                    ),
                ],
            ),
            Cmd(
                "update",
                update_token,
                "update the description for deployment token with given ID",
                [
                    Arg("id", help="ID of the token"),
                    Arg(
                        "--description",
                        help="New description for the deployment token. "
                        "Enclose in quotes if the description contains spaces.",
                    ),
                ],
            ),
            Cmd(
                "revoke",
                revoke_token,
                "revoke the deployment token with given ID",
                [
                    Arg("id", help="ID of the token"),
                ],
            ),
            Cmd(
                "delete",
                delete_token,
                "delete the deployment token with given ID",
                [
                    Arg("id", help="ID of the token"),
                ],
            ),
        ],
    )
]  # type: List[Any]
