# Copyright 2022 Karlsruhe Institute of Technology
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
from flask import current_app
from flask import render_template
from flask import request
from flask_login import login_required

import kadi.lib.constants as const
from kadi.lib.api.blueprint import bp as api_bp
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.config.core import get_user_config
from kadi.lib.plugins.core import get_plugin_config
from kadi.lib.utils import as_list
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.groups.models import Group
from kadi.modules.groups.utils import get_user_groups
from kadi.plugins import hookimpl

from . import DEFAULT_CONTENT_TYPE
from . import PLUGIN_NAME
from . import USER_CONFIG_INFLUXDBS
from .utils import InfluxDBConfigForm


bp = Blueprint(
    PLUGIN_NAME,
    __name__,
    url_prefix="/influxdb",
    template_folder="templates",
    static_folder="static",
)


TRANSLATIONS = {
    "de": {
        "Configured globally": "Global konfiguriert",
        "Database disabled or no access rights.": "Datenbank deaktiviert oder keine"
        " Zugriffsrechte.",
        "Name": "Name",
        "Query endpoint:": "Query-Endpunkt:",
        "Token": "Token",
    }
}


def _validate_instance_config(plugin_config, name):
    instance_config = plugin_config.get(name)

    if not isinstance(instance_config, dict) or not instance_config.get("url"):
        current_app.logger.error(
            f"Invalid configuration for '{name}' in '{PLUGIN_NAME}' plugin."
        )
        return False

    return True


def _get_group_ids():
    user_groups = get_user_groups().with_entities(Group.id).all()
    return {id for (id,) in user_groups}


def _has_group_access(user_groups, db_groups):
    return db_groups is None or bool(user_groups.intersection(db_groups))


@api_bp.post("/influxdb/<name>/query")
@login_required
@qparam("orgID")
def influxdb_query(name, qparams):
    """Query data from a configured InfluxDB instance.

    This endpoint is simply a proxy to the InfluxDB query endpoint documented at:
    https://docs.influxdata.com/influxdb/v2.2/api/#operation/PostQuery
    """
    plugin_config = get_plugin_config(PLUGIN_NAME)

    if not _validate_instance_config(plugin_config, name):
        return json_error_response(
            500, description=f"InfluxDB '{name}' is configured incorrectly."
        )

    used_plugin_config = plugin_config[name]

    if not _has_group_access(
        _get_group_ids(), as_list(used_plugin_config.get("groups"))
    ):
        return json_error_response(403)

    user_config = get_user_config(key=USER_CONFIG_INFLUXDBS, default=[], decrypt=True)
    user_config = {config["name"]: config for config in user_config}

    # Globally provided token.
    if used_plugin_config.get("token"):
        used_token = used_plugin_config["token"]
    # User provided token.
    elif name in user_config and user_config[name].get("token"):
        used_token = user_config[name]["token"]
    else:
        return json_error_response(
            401, description=f"No access token was supplied for InfluxDB '{name}'."
        )

    # Set the headers required by InfluxDB.
    content_type = request.content_type

    if content_type not in {DEFAULT_CONTENT_TYPE, const.MIMETYPE_JSON}:
        content_type = DEFAULT_CONTENT_TYPE

    headers = {
        "Authorization": f"Token {used_token}",
        "Content-Type": content_type,
    }

    try:
        url = f"{used_plugin_config['url']}/api/v2/query?orgID={qparams['orgID']}"
        response = requests.post(
            url=url,
            data=request.data,
            headers=headers,
            timeout=used_plugin_config.get("timeout", 10),
        )
    except Exception as e:
        current_app.logger.exception(e)
        return json_error_response(
            502, description=f"Request to InfluxDB '{name}' failed."
        )

    # Return errors that are produced directly by the accessed InfluxDB instance as-is.
    if response.status_code != 200:
        return json_response(response.status_code, response.json())

    return current_app.response_class(
        response=response.content, mimetype=const.MIMETYPE_CSV
    )


@hookimpl
def kadi_get_blueprints():
    return bp


@hookimpl
def kadi_get_capabilities():
    return "influxdb"


@hookimpl
def kadi_get_scripts():
    if request.endpoint != "settings.manage_preferences":
        return None

    return url_for("influxdb.static", filename="influxdb-field.js")


@hookimpl
def kadi_get_translations_bundles(locale):
    if request.endpoint != "settings.manage_preferences":
        return None

    return TRANSLATIONS.get(locale)


@hookimpl
def kadi_get_preferences_config():
    plugin_config = get_plugin_config(PLUGIN_NAME)
    influxdbs = {}

    user_groups = _get_group_ids()

    for name in plugin_config:
        if _validate_instance_config(plugin_config, name) and _has_group_access(
            user_groups, as_list(plugin_config[name].get("groups"))
        ):
            influxdbs[name] = {
                "title": plugin_config[name].get("title", name),
                "has_token": bool(plugin_config[name].get("token")),
                "query_endpoint": url_for("api.influxdb_query", name=name, orgID="..."),
            }

    user_config = get_user_config(key=USER_CONFIG_INFLUXDBS, decrypt=True)

    # Check if either at least one valid InfluxDB instance is configured or if the
    # current user configured any InfluxDB instance in the past.
    if not influxdbs and not user_config:
        return None

    form = InfluxDBConfigForm()

    return {
        "title": "InfluxDB",
        "form": form,
        "get_template": lambda: render_template(
            "influxdb/preferences.html", form=form, influxdbs=influxdbs
        ),
    }
