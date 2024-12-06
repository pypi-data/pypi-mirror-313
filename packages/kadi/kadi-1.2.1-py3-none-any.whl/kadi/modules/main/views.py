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
from authlib.oauth2 import OAuth2Error
from flask import redirect
from flask import render_template
from flask_babel import gettext as _
from flask_login import current_user
from flask_login import login_required

import kadi.lib.constants as const
from kadi.ext.csrf import csrf
from kadi.ext.oauth import oauth_server
from kadi.lib.config.core import get_sys_config
from kadi.lib.oauth.core import RevocationEndpoint
from kadi.lib.web import get_preferred_locale
from kadi.lib.web import html_error_response
from kadi.lib.web import url_for

from .blueprint import bp
from .forms import AuthorizeApplicationForm
from .utils import get_favorite_resources
from .utils import get_latest_resources
from .utils import get_resource_searches


@bp.get("/")
def index():
    """The index/home page.

    Will change depending on whether the current user is authenticated or not.
    """
    preferred_locale = get_preferred_locale()

    if not current_user.is_authenticated:
        return render_template("main/index.html", preferred_locale=preferred_locale)

    return render_template(
        "main/home.html",
        title=_("Home"),
        preferred_locale=preferred_locale,
        js_context={
            "favorite_resources": get_favorite_resources(),
            "saved_searches": get_resource_searches(),
            "latest_resources": get_latest_resources(),
        },
    )


@bp.get("/about")
def about():
    """The about page."""
    return render_template("main/about.html", title=_("About"))


@bp.get("/help")
def help():
    """The help page."""
    return render_template("main/help.html", title=_("Help"))


@bp.get("/terms-of-use")
def terms_of_use():
    """Page showing the terms of use, if configured."""
    config_item = const.SYS_CONFIG_TERMS_OF_USE

    if not get_sys_config(config_item):
        return redirect(url_for("main.index"))

    return render_template(
        "main/legals.html",
        title=_("Terms of use"),
        endpoint="terms_of_use",
        config_item=config_item,
    )


@bp.get("/privacy-policy")
def privacy_policy():
    """Page showing the privacy policy, if configured."""
    config_item = const.SYS_CONFIG_PRIVACY_POLICY

    if not get_sys_config(config_item):
        return redirect(url_for("main.index"))

    return render_template(
        "main/legals.html",
        title=_("Privacy policy"),
        endpoint="privacy_policy",
        config_item=config_item,
    )


@bp.get("/legal-notice")
def legal_notice():
    """Page showing the legal notice, if configured."""
    config_item = const.SYS_CONFIG_LEGAL_NOTICE

    if not get_sys_config(config_item):
        return redirect(url_for("main.index"))

    return render_template(
        "main/legals.html",
        title=_("Legal notice"),
        endpoint="legal_notice",
        config_item=config_item,
    )


@bp.route("/oauth/authorize", methods=["GET", "POST"])
@login_required
def oauth2_server_authorize():
    """Authorization endpoint for the OAuth2 server implementation."""
    form = AuthorizeApplicationForm()

    if form.validate_on_submit():
        # Check if authorization was granted by the user.
        if form.submit_auth.data:
            grant_user = current_user
        else:
            grant_user = None

        return oauth_server.create_authorization_response(grant_user=grant_user)

    try:
        grant = oauth_server.get_consent_grant(end_user=current_user)
    except OAuth2Error as e:
        description = e.description

        if not description:
            description = _(
                "The service that redirected you here made an invalid authorization"
                " request."
            )

        return html_error_response(e.status_code, description=description)

    return render_template(
        "main/oauth_consent.html",
        title=_("Authorize application"),
        form=form,
        client=grant.client,
    )


@bp.post("/oauth/token")
@csrf.exempt
def oauth2_server_token():
    """Token endpoint for the OAuth2 server implementation."""
    return oauth_server.create_token_response()


@bp.post("/oauth/revoke")
@csrf.exempt
def oauth2_server_revoke():
    """Token revocation endpoint for the OAuth2 server implementation."""
    return oauth_server.create_endpoint_response(RevocationEndpoint.ENDPOINT_NAME)
