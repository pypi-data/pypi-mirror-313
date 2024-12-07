# SPDX-License-Identifier: MIT
# Copyright 2020-2023 Big Bad Wolf Security, LLC

import json
import urllib.request
from dataclasses import dataclass, field

__all__ = ["create_services", "download_policy_definitions"]

# From: https://awspolicygen.s3.amazonaws.com/policygen.html
POLICIES_URL = "https://awspolicygen.s3.amazonaws.com/js/policies.js"


@dataclass
class Service:
    """Define the structure of an AWS service definition."""

    Actions: list[str] = field(default_factory=list)
    ServiceNames: list[str] = field(default_factory=list)
    ARNFormats: list[str] = field(default_factory=list)
    ARNRegexes: list[str] = field(default_factory=list)
    ConditionKeys: list[str] = field(default_factory=list)
    HasResource: bool = False

    def merge_list(self, field: str, values: list[str] | str) -> None:
        """Merge the list with the given value(s), dedupe, and sort."""
        value = getattr(self, field, [])
        value += values if isinstance(values, list) else [values]
        setattr(self, field, sorted({x for x in value if x}))


def download_policy_definitions(url: str = POLICIES_URL) -> dict:
    """Return Amazon's policy definitions as a parsed JSON object."""
    with urllib.request.urlopen(url) as response:
        json_string = response.read().removeprefix(b"app.PolicyEditorConfig=")
    return json.loads(json_string)


def create_services(policies: dict) -> dict[str, Service]:
    """Return service definitions created from the given policy object.

    The input dict's "serviceMap" element is converted from a map keyed
    on the service name to a map keyed on "StringPrefix".
    """
    services = {}

    for service_name, v in policies.get("serviceMap", {}).items():
        prefix = v.get("StringPrefix")
        if prefix not in services:
            services[prefix] = Service()

        services[prefix].merge_list("Actions", v.get("Actions"))
        services[prefix].merge_list("ServiceNames", service_name)
        services[prefix].merge_list("ARNFormats", v.get("ARNFormat"))
        services[prefix].merge_list("ARNRegexes", v.get("ARNRegex"))
        services[prefix].merge_list("ConditionKeys", v.get("conditionKeys"))
        services[prefix].HasResource |= v.get("HasResource", False)

    return services
