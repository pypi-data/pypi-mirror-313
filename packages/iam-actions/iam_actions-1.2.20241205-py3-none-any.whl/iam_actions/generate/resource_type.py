# SPDX-License-Identifier: MIT
# Copyright 2020-2022 Big Bad Wolf Security, LLC

from dataclasses import dataclass
from typing import Optional
from bs4 import Tag
from loguru import logger


@dataclass
class ResouceTypeDetail:
    resource_type_name: str = ""
    arn_pattern: str = ""
    condition_keys: Optional[str] = None


def resource_type_arn_to_globs(arn):
    out = []
    in_replacement = False
    for c in arn:
        if in_replacement:
            if c == "}":
                in_replacement = False
        elif c == "$":
            out.append("*")
            in_replacement = True
        else:
            out.append(c)
    return "".join(out)


def process_resource_type_table(table: list[list[str]]) -> dict[str, dict[str, str]]:
    if not table:
        return None
    rts = {}
    rows = [x for x in table.contents if x.name == "tr"]
    for row in rows:
        cells = [x for x in row.contents if x.name == "td"]
        if len(cells) == 0:
            continue

        rt = ResouceTypeDetail()
        rt.resource_type_name = str(cells[0].text.strip())

        assert rt.resource_type_name is not None

        rt.arn_pattern = resource_type_arn_to_globs("".join([str(x.string) for x in cells[1].code.contents]))

        if cells[2].a is not None:
            rt.condition_keys = str(cells[2].a.string)

        rts[rt.resource_type_name] = {"arn_pattern": rt.arn_pattern, "condition_keys": rt.condition_keys}

    return rts


def generate_resource_type(docs: list[Tag]):
    rts = {}
    errors = []
    for doc in docs:
        resource_types = process_resource_type_table(doc.resource_type_table())
        if not resource_types:
            logger.info(f"Page missing resource type table: {doc.readable_url()}")
            continue
        for k in resource_types:
            if not rts.get(k):
                rts[k] = resource_types[k]
    return (rts, errors)
