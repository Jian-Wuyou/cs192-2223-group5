from os import environ
from urllib.parse import urljoin, urlparse

from lms_hub.models.profile import from_google_jwt

from flask import (Blueprint, current_app, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_user
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token

login = Blueprint("login", __name__)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@login.route("/login", methods=["GET"])
def login_page():
    # Redirect to dashboard if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_page"))

    return render_template(
        "login.html",
        full_width="true",
        domain=environ["DOMAIN"],
        google_client_id=current_app.config["GOOGLE_CLIENT_ID"],
    )

@login.route("/login", methods=["POST"])
def login_form():
    db = current_app.config["DB"]

    if "g_csrf_token" not in request.form:
        
        return "CSRF token missing", 400
    csrf_cookie = request.cookies.get("g_csrf_token")
    if not csrf_cookie or csrf_cookie != request.form["g_csrf_token"]:
        return "CSRF cookie missing", 400

    try:
        id_info = id_token.verify_oauth2_token(
            request.form["credential"],
            requests.Request(),
            current_app.config["GOOGLE_CLIENT_ID"],
        )
    except (ValueError, GoogleAuthError) as e:
        return f"Invalid JWT: {str(e)}", 400
    else:
        if not id_info["email_verified"]:
            return "Email not verified", 400

    email = id_info["email"]
    matching_user = db.lookup_user_by_email(email)
    if matching_user is None:
        if not id_info["email_verified"]:
            return "Email not verified", 400

        matching_user = from_google_jwt(id_info)
        db.add_user(matching_user)

    # Log in
    login_user(matching_user)

    # Redirect to the next page
    next_url = request.args.get("next")
    if not is_safe_url(next_url):
        return "Unsafe redirect URL", 400
    return redirect(next_url or url_for("dashboard.dashboard_page"))
