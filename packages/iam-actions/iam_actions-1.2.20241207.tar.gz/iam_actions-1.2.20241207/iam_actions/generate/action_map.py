# SPDX-License-Identifier: MIT
# Copyright 2020-2022 Big Bad Wolf Security, LLC

"""Define and create action structures.

Calling `create_action_map` with a dict from the services module is the
main entry point for this module.
"""

from bs4 import Tag
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger


class AccessLevel(str, Enum):
    """Enumerate the possible action "AccessLevel" item values."""

    READ = "Read"
    WRITE = "Write"
    PUT = "Put"
    DELETE = "Delete"
    GET = "Get"
    LIST = "List"
    PERMISSIONS_MANAGE = "Permissions management"
    TAGGING = "Tagging"
    REPLICATE = "Replicate"
    NONE = "None"
    UNDOCUMENTED = "Undocumented"

    def __repr__(self) -> str:
        """Represent `AccessLevel` items as their bare string values."""
        return self.value


@dataclass
class ActionMap:
    """Define the structure of an AWS action definition."""

    access_level: AccessLevel = AccessLevel.NONE
    action: str = ""
    condition_keys: list[str] = field(default_factory=list, repr=False)
    description: str = ""
    orphan: bool = False
    resources: list[str] = field(default_factory=list)


def process_actions_table(table: Tag) -> list[ActionMap]:
    """Return a list of actions, one per row of the given table."""
    return [
        ActionMap(
            action=row[0].replace("[permission only]", "").strip(),
            access_level=AccessLevel(row[2]),
            resources=sorted({x.replace("*", "") for x in row[3].split()}),
            condition_keys=sorted({x for x in row[4].split()}),
            description=" ".join(row[1].split()),
        )
        for row in table
    ]


def generate_action_map(docs: list[Tag], acts: list[str]) -> tuple[dict, list[str]]:
    """Return a tuple of service actions and any errors encountered.

    The given service name has its documentation URLs searched for
    action definitions.  They are then compared with the given known
    service action names to find undocumented actions.  The whole set of
    actions is then returned as a dict keyed on their names, alongside a
    list of any error messages.
    """
    actions = {}
    errors = []
    service = None
    for doc in docs:
        service = doc.service
        table = doc.flat_action_map_table()
        if not table:
            logger.info(f"Page missing actions table: {doc.readable_url()}")
            continue
        for map in process_actions_table(table):
            # Keep the first one as defined in the URL map.
            if map.action not in actions:
                actions[map.action] = map

    # Check if any known actions are missing from the documentation.
    boto_defined_actions = set(acts)
    found_actions = set(actions.keys())
    for action in boto_defined_actions - found_actions:
        actions[action] = ActionMap(
            action=action,
            access_level=AccessLevel.UNDOCUMENTED,
            description="Not Documented by AWS",
        )
        errors.append(f"Undocumented action found: {service}:{action}")

    return actions, errors
