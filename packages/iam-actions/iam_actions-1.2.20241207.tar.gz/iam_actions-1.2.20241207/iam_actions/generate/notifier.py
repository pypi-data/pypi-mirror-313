# SPDX-License-Identifier: MIT
# Copyright 2020-2022 Big Bad Wolf Security, LLC

"""Upload generated JSON files to S3 to track revisions.

The JSON files written by iam_actions.generate.run can be given to this
script to upload them to S3 and notify about any changes since the
previous run.

The environment variable S3_BUCKET defines the bucket that will store
the uploaded files, and WEBHOOK optionally defines a Slack hook URL to
send notifications.
"""

import argparse
import boto3
import json
import os
from datetime import datetime
from slack_sdk.webhook import WebhookClient
from pathlib import Path

now = datetime.utcnow().isoformat()


def default_directory() -> str:
    return str(Path(__file__).parent.parent.resolve())


def create_argument_parser() -> argparse.ArgumentParser:
    """Return an `argparse.ArgumentParser` defining the CLI."""
    parser = argparse.ArgumentParser(
        description="Upload new IAM action JSON files to S3",
    )
    parser.add_argument(
        "-a",
        "--actions",
        dest="action_map",
        metavar="PATH",
        help="Path to the actions JSON file to upload",
        type=argparse.FileType("rb"),
        default=f"{default_directory()}/actions.json",
    )
    parser.add_argument(
        "-s",
        "--services",
        metavar="PATH",
        help="Path to the services JSON file to upload",
        type=argparse.FileType("rb"),
        default=f"{default_directory()}/services.json",
    )
    parser.add_argument(
        "-r",
        "--resourcetypes",
        metavar="PATH",
        help="Path to the resource types JSON file to upload",
        type=argparse.FileType("rb"),
        default=f"{default_directory()}/resourcetypes.json",
    )
    parser.add_argument(
        "-e",
        "--errors",
        metavar="PATH",
        help="Path to the errors JSON file to upload",
        type=argparse.FileType("rb"),
        default=f"{default_directory()}/errors.json",
    )
    return parser


def main(*pargs, **kwargs) -> None:
    """This is the entry point function."""
    args = create_argument_parser().parse_args()
    bucket = os.getenv("S3_BUCKET", None)
    webhook = os.getenv("SLACK_WEBHOOK", None)

    messages = [f"Scraping run completed {now}", ""]
    if args.errors:
        with args.errors as file:
            errors = json.loads(file.read())
        if errors:
            messages += ["\r\n".join(["**Errors:**"] + [f"- {e}" for e in sorted(errors)])]

    if bucket:
        client = boto3.client("s3")
        dest_dir = f"archived/{now}"

        for name, source in vars(args).items():
            dest_path = f"{dest_dir}/{name}.json"
            latest_path = f"current/{name}.json"

            # Upload the file
            client.upload_fileobj(source, bucket, dest_path)["ETag"]
            # old_hash = client.head_object(Bucket=bucket, Key=latest_path)["ETag"]

            # Update the file at the latest URL.
            client.copy_object(Bucket=bucket, CopySource=f"{bucket}/{dest_path}", Key=latest_path)

    if webhook:
        print("\r\n\r\n".join(messages))
        if WebhookClient and webhook:
            slack = WebhookClient(webhook)
            slack.send(text="\r\n\r\n".join(messages))


if __name__ == "__main__":
    main()
