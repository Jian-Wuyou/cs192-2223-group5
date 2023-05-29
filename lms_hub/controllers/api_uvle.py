from json import dumps
from typing import List

from flask import Blueprint, current_app, redirect, url_for, request
from flask_login import current_user, login_required
from lms_hub.controllers.uvle import UVLeClient
from lms_hub.models.credentials import UVLeCredentials
from lms_hub.models.deadline import Deadline, sort_deadlines
from lms_hub.models.learning_env_class import LearningEnvClassEnc

uvle = Blueprint("uvle", __name__)

@uvle.before_request
@login_required
def uvle_before_request():
    # Check if user has UVLe credentials
    if len(current_user.accounts['uvle'].token) == 0:
        # Redirect to UVLe account linking page
        return redirect(url_for("link-uvle.login_page"))
    return None


# Create client if it doesn't exist yet
def create_uvle_client(creds: UVLeCredentials) -> UVLeClient:
    if "uvle_client" not in current_app.config:
        current_app.config["uvle_client"] = UVLeClient(creds)
    return current_app.config["uvle_client"]


@uvle.route("/classes")
@login_required
def uvle_get_classes():
    client = create_uvle_client(current_user.accounts['uvle'])
    return dumps({"courses": client.get_classes()}, cls=LearningEnvClassEnc)


@uvle.route("/deadlines", methods=["POST"])
@login_required
def uvle_get_deadlines():
    # Get JSON body parameters
    r = request.json
    payload =  {
        "from": r.get("from", None),
        "to": r.get("to", None),
        "description": r.get("description", True)
    }

    client = create_uvle_client(current_user.accounts['uvle'])
    deadlines = sort_deadlines(client.get_deadlines())

    if not payload["description"]:
        for deadline in deadlines:
            deadline.pop("description")

    return dumps({"deadlines": deadlines})
