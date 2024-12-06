# Copyright 2023 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# pylint: disable=missing-function-docstring


import requests
from flask import Blueprint
from flask import render_template

from kadi.lib.conversion import truncate
from kadi.lib.plugins.core import get_plugin_config
from kadi.plugins import hookimpl

from . import DEFAULT_ENDPOINT
from . import PLUGIN_NAME


# Currently only used for the custom template folder.
bp = Blueprint(PLUGIN_NAME, __name__, template_folder="templates")


@hookimpl
def kadi_get_blueprints():
    return bp


@hookimpl
def kadi_get_capabilities():
    return "term_search"


TYPE_COLOR_MAP = {
    "class": "success",
    "property": "info",
    "individual": "warning",
}


@hookimpl
def kadi_get_terms(query, page, per_page):
    plugin_config = get_plugin_config(PLUGIN_NAME)
    endpoint = plugin_config.get("endpoint", DEFAULT_ENDPOINT)

    params = {
        # Specifying an empty query will lead to no results otherwise.
        "q": query or "*",
        "type": ["class", "property", "individual"],
        "fieldList": ["iri", "label", "description", "type"],
        "queryFields": ["label", "synonym", "description", "iri"],
        "groupField": "true",
        "rows": per_page,
        "start": (page - 1) * per_page,
    }
    response = requests.get(endpoint, params=params, timeout=10)

    if response.ok:
        data = response.json()["response"]
        items = []

        for item in data["docs"]:
            term = item["iri"]
            item_type = item["type"]
            description = ""

            if "description" in item:
                # Descriptions seems to always be wrapped in a list with a single entry,
                # but we try to be flexible in case this changes in the future.
                descriptions = item["description"]

                if isinstance(descriptions, list):
                    description = descriptions[0]
                else:
                    description = descriptions

                description = truncate(description, 350)

            items.append(
                {
                    "term": term,
                    "body": render_template(
                        "tib_ts/term.html",
                        term=term,
                        label=item["label"],
                        description=description,
                        type=item_type,
                        type_color=TYPE_COLOR_MAP[item_type],
                    ),
                }
            )

        return data["numFound"], items

    return None
