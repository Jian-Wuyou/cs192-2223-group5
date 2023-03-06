from os import environ

from flask import (
    Blueprint,
    current_app,
    render_template,
)

login = Blueprint("login", __name__)

@login.route("/login", methods=["GET"])
def login_page():
    # Redirect to dashboard if already logged in

    return render_template(
        "login.html",
        full_width="true",
        domain=environ["DOMAIN"],
        google_client_id=current_app.config["GOOGLE_CLIENT_ID"],
    )
