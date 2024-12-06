# SPDX-License-Identifier: MIT
# Copyright 2020-2023 Big Bad Wolf Security, LLC

"""Generate and write the JSON files.

This module runs all of the other module code to fetch current action
and service information from Amazon, and it outputs the restructured
data as JSON files.  It is only intended to be run as a script, e.g.
with "python -m iam_actions.generate".  The CLI is described using the
"--help" argument.
"""

import argparse
import dataclasses
import json
from .services import create_services, download_policy_definitions
from .aws_docs import fetch_docs_for_services
from pathlib import Path

__all__ = ["run"]


class JSONEncoderDataclass(json.JSONEncoder):
    """Define a JSON encoder that knows how to handle dataclasses."""

    def default(self, o):
        """Return a presumed order-preserving dict for dataclasses."""
        if dataclasses.is_dataclass(o):
            return {f.name: getattr(o, f.name) for f in dataclasses.fields(o)}
        return super().default(o)


def default_directory() -> str:
    return str(Path(__file__).parent.parent.resolve())


def create_argument_parser() -> argparse.ArgumentParser:
    """Return an `argparse.ArgumentParser` defining the CLI."""
    parser = argparse.ArgumentParser(
        description="Generate the AWS services and action map",
    )
    parser.add_argument(
        "-a",
        "--actions",
        metavar="PATH",
        help="Path to write the generated action map JSON",
        type=argparse.FileType("w", encoding="UTF-8"),
        default=f"{default_directory()}/actions.json",
    )
    parser.add_argument(
        "-s",
        "--services",
        metavar="PATH",
        help="Path to write the generated services JSON",
        type=argparse.FileType("w", encoding="UTF-8"),
        default=f"{default_directory()}/services.json",
    )
    parser.add_argument(
        "-r",
        "--resourcetypes",
        metavar="PATH",
        help="Path to write resource types JSON",
        type=argparse.FileType("w", encoding="UTF-8"),
        default=f"{default_directory()}/resourcetypes.json",
    )
    parser.add_argument(
        "-p",
        "--policies",
        metavar="PATH",
        help="Path to write Amazon's policies JSON (to debug)",
        type=argparse.FileType("w", encoding="UTF-8"),
        default=f"{default_directory()}/policies.json",
    )
    parser.add_argument(
        "-e", "--errors", metavar="PATH", help="Path to write errors and warnings JSON", type=argparse.FileType("w", encoding="UTF-8"), default=f"{default_directory()}/errors.json"
    )
    parser.add_argument("-i", "--indent", default=True, action=argparse.BooleanOptionalAction, help="Pretty-print the JSON files", type=argparse.FileType("w", encoding="UTF-8"))
    return parser


def run(*pargs, **kwargs) -> None:
    """This is the entry point function."""
    args = create_argument_parser().parse_args()

    policies = download_policy_definitions()
    if args.policies:
        json.dump(policies, args.policies, cls=JSONEncoderDataclass, indent=1 if args.indent else None)

    services = create_services(policies)
    if args.services:
        json.dump(services, args.services, cls=JSONEncoderDataclass, indent=1 if args.indent else None)

    actions, resource_types, errors = fetch_docs_for_services(services)
    if args.actions:
        json.dump(actions, args.actions, cls=JSONEncoderDataclass, indent=1 if args.indent else None)
    if args.resourcetypes:
        json.dump(resource_types, args.resourcetypes, cls=JSONEncoderDataclass, indent=1 if args.indent else None)
    if args.errors:
        json.dump(errors, args.errors, cls=JSONEncoderDataclass, indent=1 if args.indent else None)


if __name__ == "__main__":
    run()
