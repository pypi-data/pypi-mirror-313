# Copyright 2020 Karlsruhe Institute of Technology
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


import os

from flask import Blueprint
from flask import current_app
from flask import render_template
from flask_babel import gettext as _

import kadi.lib.constants as const
from kadi.lib.conversion import markdown_to_html
from kadi.lib.oauth.utils import get_refresh_token_handler
from kadi.lib.plugins.core import get_plugin_config
from kadi.lib.resources.utils import get_linked_resources
from kadi.lib.utils import utcnow
from kadi.lib.web import url_for
from kadi.modules.records.extras import extras_to_plain_json
from kadi.modules.records.models import Record
from kadi.plugins import hookimpl

from . import DEFAULT_LICENSE
from . import DEFAULT_URL
from . import INVENIO_API_URL
from . import PLUGIN_NAME
from .utils import UploadCanceledException
from .utils import UploadStream
from .utils import ZenodoForm


# Currently only used for the custom template folder.
bp = Blueprint(PLUGIN_NAME, __name__, template_folder="templates")


def _validate_plugin_config(plugin_config):
    if not plugin_config.get("client_id") or not plugin_config.get("client_secret"):
        current_app.logger.error(
            f"Missing client ID and/or secret in '{PLUGIN_NAME}' plugin."
        )
        return False

    return True


@hookimpl
def kadi_get_blueprints():
    return bp


@hookimpl
def kadi_get_translations_paths():
    return os.path.join(os.path.dirname(__file__), "translations")


@hookimpl
def kadi_register_oauth2_providers(registry):
    plugin_config = get_plugin_config(PLUGIN_NAME)

    if not _validate_plugin_config(plugin_config):
        return

    client_id = plugin_config["client_id"]
    client_secret = plugin_config["client_secret"]
    base_url = plugin_config.get("base_url", DEFAULT_URL)

    registry.register(
        name=PLUGIN_NAME,
        client_id=client_id,
        client_secret=client_secret,
        access_token_url=f"{base_url}/oauth/token",
        access_token_params={"client_id": client_id, "client_secret": client_secret},
        authorize_url=f"{base_url}/oauth/authorize",
        api_base_url=f"{base_url}/api/",
        client_kwargs={"scope": "deposit:write"},
        compliance_fix=get_refresh_token_handler(client_id, client_secret),
    )


@hookimpl
def kadi_get_oauth2_providers():
    plugin_config = get_plugin_config(PLUGIN_NAME)

    if not _validate_plugin_config(plugin_config):
        return None

    description = _(
        "Zenodo is a general-purpose open-access repository developed and operated by"
        " CERN. It allows researchers to deposit and publish data sets, research"
        " software, reports, and any other research related digital objects. Connecting"
        " your account to Zenodo makes it possible to directly upload resources to"
        " Zenodo."
    )

    return {
        "name": PLUGIN_NAME,
        "title": "Zenodo",
        "website": plugin_config.get("base_url", DEFAULT_URL),
        "description": description,
    }


@hookimpl
def kadi_get_publication_providers(resource):
    plugin_config = get_plugin_config(PLUGIN_NAME)

    if isinstance(resource, Record):
        export_endpoint = "records.export_record"
    else:
        export_endpoint = "collections.export_collection"

    warning_msg = plugin_config.get("warning_msg")
    export_url = url_for(
        export_endpoint, id=resource.id, export_type=const.EXPORT_TYPE_RO_CRATE
    )

    return {
        "name": PLUGIN_NAME,
        "description": render_template(
            "zenodo/description_publication.html",
            warning_msg=warning_msg,
            export_url=export_url,
            invenio_url=INVENIO_API_URL,
        ),
    }


@hookimpl
def kadi_get_publication_form(provider, resource):
    if provider != PLUGIN_NAME:
        return None

    return ZenodoForm()


@hookimpl
def kadi_get_publication_form_template(provider, resource, form):
    if provider != PLUGIN_NAME:
        return None

    return render_template("zenodo/publication_form.html", form=form, resource=resource)


def _delete_draft(draft_record, client, token):
    try:
        client.delete(f"records/{draft_record['id']}/draft", token=token)
    except:
        pass


def _make_error_template(message=None, response=None):
    status = response.status_code if response is not None else None

    if message is None:
        try:
            # If the email address of the account is not confirmed yet, no records can
            # be created. Unfortunately, Zenodo only returns an HTML response in this
            # case, so we try to catch that.
            if (
                response.status_code == 403
                and response.headers["Content-Type"]
                == f"{const.MIMETYPE_HTML}; charset=utf-8"
            ):
                message = _("Please verify your email address first.")
            else:
                message = response.json()["message"]
        except:
            message = _("Unknown error.")

    return render_template("zenodo/upload_error.html", message=message, status=status)


def _extract_basic_metadata(resource, user):
    creator_meta = {"type": "personal"}
    name = user.displayname.rsplit(" ", 1)

    if len(name) == 2:
        creator_meta.update({"given_name": name[0], "family_name": name[1]})
    else:
        creator_meta["family_name"] = name[0]

    if user.orcid:
        creator_meta["identifiers"] = [{"scheme": "orcid", "identifier": user.orcid}]

    license_meta = {"id": DEFAULT_LICENSE}

    if isinstance(resource, Record) and resource.license:
        # Zenodo uses lower case license IDs in its vocabulary.
        license_meta["id"] = resource.license.name.lower()

    return {
        "resource_type": {"id": "dataset"},
        "title": resource.title,
        "publication_date": utcnow().strftime("%Y-%m-%d"),
        "creators": [{"person_or_org": creator_meta}],
        "description": markdown_to_html(resource.description),
        "rights": [license_meta],
        "subjects": [{"subject": tag.name} for tag in resource.tags.order_by("name")],
        "publisher": "Zenodo",
    }


@hookimpl
def kadi_publish_resource(provider, resource, form_data, user, client, token, task):
    if provider != PLUGIN_NAME:
        return None

    basic_metadata = _extract_basic_metadata(resource, user)
    custom_metadata = extras_to_plain_json(form_data["extras"])

    draft_record = None

    try:
        # Check if the extracted license is supported by Zenodo.
        license_meta = basic_metadata["rights"][0]
        response = client.get(
            f"vocabularies/licenses/{license_meta['id']}", token=token
        )

        if not response.ok:
            license_meta["id"] = DEFAULT_LICENSE

        basic_metadata |= custom_metadata.pop("metadata", {})
        community = custom_metadata.pop("community", None)
        metadata = {
            "metadata": basic_metadata,
            **custom_metadata,
        }

        # Create a new draft record using the InvenioRDM API.
        response = client.post("records", token=token, json=metadata)

        if not response.ok:
            return False, _make_error_template(response=response)

        draft_record = response.json()

        # If applicable, create a review request for the given community. This requires
        # retrieving the community ID first.
        if community:
            response = client.get(f"communities/{community}", token=token)

            if response.ok:
                response = client.put(
                    f"records/{draft_record['id']}/draft/review",
                    token=token,
                    json={
                        "receiver": {"community": response.json()["id"]},
                        "type": "community-submission",
                    },
                )

                if not response.ok:
                    _delete_draft(draft_record, client, token)
                    return False, _make_error_template(response=response)

        if isinstance(resource, Record):
            record_or_records = resource
        else:
            if form_data["export_filter"].get("records", False):
                record_or_records = []
            else:
                record_or_records = get_linked_resources(
                    Record, resource.records, user=user
                )

        # Initialize a file upload within the draft record.
        response = client.post(
            draft_record["links"]["files"],
            token=token,
            json=[{"key": f"{resource.identifier}.zip"}],
        )

        if not response.ok:
            _delete_draft(draft_record, client, token)
            return False, _make_error_template(response=response)

        # Upload the content of the file.
        stream = UploadStream(
            record_or_records, resource, form_data["export_filter"], user, task=task
        )
        response = client.put(
            response.json()["entries"][0]["links"]["content"],
            token=token,
            data=stream,
            headers={
                "Content-Type": const.MIMETYPE_BINARY,
                "Content-Length": str(len(stream)),
            },
        )

        if not response.ok:
            _delete_draft(draft_record, client, token)
            return False, _make_error_template(response=response)

        # Complete the file upload.
        response = client.post(response.json()["links"]["commit"], token=token)

        if not response.ok:
            _delete_draft(draft_record, client, token)
            return False, _make_error_template(response=response)

    except UploadCanceledException:
        _delete_draft(draft_record, client, token)
        return False, _("Upload canceled.")

    except Exception as e:
        current_app.logger.debug(e, exc_info=True)

        if draft_record is not None:
            _delete_draft(draft_record, client, token)

        return False, _make_error_template(message=repr(e))

    return True, render_template(
        "zenodo/upload_success.html", record_url=draft_record["links"]["self_html"]
    )
