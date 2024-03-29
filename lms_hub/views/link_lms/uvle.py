from os import environ

from flask import Blueprint, current_app, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from lms_hub.models.credentials import UVLeCredentials

import requests

UVLe = Blueprint("link-uvle", __name__)

@UVLe.route("/link/uvle", methods=["GET"])
@login_required
def login_page():
    return render_template("lms/login-uvle.html")

@UVLe.route("/unlink/uvle")
@login_required
def logout_post():
    db = current_app.config["DB"]
    db.delete_user_lms_creds("uvle", current_user.user_id)
    return redirect(url_for('dashboard.dashboard_page'))

@UVLe.route("/link/uvle", methods=["POST"])
@login_required
def login_post():
    plaintext_creds = request.json["credentials"]
    username, password = plaintext_creds.split(":")
    domain = environ["UVLE_DOMAIN"]
    url = f"https://{domain}/login/token.php"
    payload = {
        "username": username,
        "password": password,
        "service": "moodle_mobile_app",
    }

    try:
        r = requests.get(url, params=payload)
    except requests.RequestException as e:
        return '{"success": false, "error": "Could not connect to the LMS server"}', 400

    if not 200 <= r.status_code <= 299:
        # Unsuccessful request
        # Could not connect to server, etc
        return '{"success": false, "error": "Could not connect to the LMS server"}', 400

    json = r.json()
    if "token" not in json or len(json["token"]) < 32:
        return '{"success": false, "error": "Invalid credentials"}', 400

    creds = UVLeCredentials(
        username = username,
        token = json["token"],
        server = domain
    )

    db = current_app.config["DB"]
    db.update_user_lms_creds("uvle", current_user.user_id, creds)

    return '{"success": true}'