# © Copyright 2024 Hewlett Packard Enterprise Development LP

import argparse
import sys
from typing import Any, Dict

import termcolor
from packaging import version
from urllib3.exceptions import MaxRetryError, SSLError

import aioli
import aioli.cli
import aiolirest
from aioli import cli
from aioli.cli import render
from aioli.common.declarative_argparse import ArgsDescription, Cmd


def get_version(controller: str) -> Dict[str, Any]:
    client_info = {"version": aioli.__version__}

    controller_info = {"version": ""}

    with cli.setup_session_no_auth(controller) as session:
        api_instance = aiolirest.InformationApi(session)

        try:
            response = api_instance.version_get()
            controller_info["version"] = response
        except MaxRetryError as ex:
            # Most connection errors mean that the controller is unreachable, which this
            # function handles. An SSLError, however, means it was reachable but something
            # went wrong, so let that error propagate out.
            if ex.__cause__ and isinstance(ex.__cause__, SSLError):
                raise ex.__cause__
        except Exception:
            # Exceptions get a pass here so that the code in check_version can complete.
            pass

    return {
        "client": client_info,
        "controller": controller_info,
        "controller_address": controller,
    }


def check_version(controller: str) -> None:
    info = get_version(controller)

    controller_version = info["controller"]["version"]
    client_version = info["client"]["version"]

    if not controller_version:
        print(
            termcolor.colored(
                "Controller not found at {}. "
                "Hint: Remember to set the AIOLI_CONTROLLER environment variable "
                "to the correct controller IP and port, for example, "
                "export AIOLI_CONTROLLER=http://$AIOLI_IP:80. Or use the '-c' flag.".format(
                    controller
                ),
                "yellow",
            ),
            file=sys.stderr,
        )
    elif version.Version(client_version) < version.Version(controller_version):
        print(
            termcolor.colored(
                "CLI version {} is less than controller version {}. "
                "Consider upgrading the CLI.".format(client_version, controller_version),
                "yellow",
            ),
            file=sys.stderr,
        )
    elif version.Version(client_version) > version.Version(controller_version):
        print(
            termcolor.colored(
                "Controller version {} is less than CLI version {}. "
                "This CLI may utilize features not supported by an older "
                "controller. Install a compatible CLI with: "
                " pip install aioli-sdk=={}".format(
                    controller_version, client_version, controller_version
                ),
                "yellow",
            ),
            file=sys.stderr,
        )


def describe_version(parsed_args: argparse.Namespace) -> None:
    info = get_version(parsed_args.controller)
    print(render.format_object_as_yaml(info))


args_description: ArgsDescription = [
    Cmd("version", describe_version, "show version information", [])
]
