from os import environ

import google_auth_oauthlib.flow
from flask import Blueprint, current_app, redirect, request, session, url_for
from flask_login import current_user, login_required
from lms_hub.models.credentials import GoogleCredentials
from requests import get, post
from requests.exceptions import RequestException

GClass = Blueprint("link-gclass", __name__)

# Google OAuth2 scopes
scopes = [
    "openid",
    "https://www.googleapis.com/auth/classroom.announcements.readonly",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
    "https://www.googleapis.com/auth/classroom.topics.readonly",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

@GClass.route("/link/gclass")
@login_required
def login_page():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        current_app.config["GOOGLE_CREDENTIALS"], scopes=scopes)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = url_for("link-gclass.login_callback", _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)

@GClass.route("/link/gclass/callback")
@login_required
def login_callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        current_app.config["GOOGLE_CREDENTIALS"], scopes=scopes, state=state)
    flow.redirect_uri = url_for('link-gclass.login_callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    if not credentials.refresh_token:
        # No refresh token means the user has already authenticated with Google once.
        # Tell them to revoke access and try again.
        session["link_status"] = "failure"
        return redirect(url_for("dashboard.dashboard_page"))
    
    # Get ID and e-mail address associated with credentials
    try:
        user_info = get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": "Bearer " + credentials.token},
        ).json()
    except RequestException:
        session["link_status"] = "failure"
        return redirect(url_for("dashboard.dashboard_page"))

    db = current_app.config["DB"]
    google_credentials = GoogleCredentials(
        user_id=user_info["id"],
        email=user_info["email"],
        token=credentials.token,
        refresh_token=credentials.refresh_token,
        token_uri=credentials.token_uri,
        client_id=credentials.client_id,
        scopes=credentials.scopes,
        id_token=credentials.id_token,
        expiry=f"{credentials.expiry.isoformat()}Z",
    )
    db.update_user_lms_creds(
        "gclass", current_user.user_id, google_credentials
    )

    return redirect(url_for("dashboard.dashboard_page"))

@GClass.route("/unlink/gclass")
@login_required
def logout_post():
    post('https://oauth2.googleapis.com/revoke',
    params={'token': current_user.accounts["gclass"].token},
    headers = {'content-type': 'application/x-www-form-urlencoded'})
    db = current_app.config["DB"]
    db.delete_user_lms_creds("gclass", current_user.user_id)
    return redirect(url_for("dashboard.dashboard_page"))