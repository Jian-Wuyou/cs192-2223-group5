from json import dumps
from typing import List

from flask import Blueprint, current_app, redirect, url_for
from flask_login import current_user, login_required
from lms_hub.controllers.uvle import UVLeClient
from lms_hub.models.credentials import UVLeCredentials
from lms_hub.models.deadline import Deadline, sort_deadlines
from lms_hub.models.learning_env_class import LearningEnvClassEnc

uvle = Blueprint("uvle", __name__)

@uvle.before_request
@login_required
def moodle_before_request():
    # Check if user has Moodle credentials
    if len(current_user.moodle_account.password) == 0:
        # Redirect to Moodle account linking page
        return redirect(url_for("link-moodle.link_moodle_page"))
    return None


# Create client if it doesn't exist yet
def create_uvle_client(creds: UVLeCredentials) -> UVLeClient:
    if "uvle_client" not in current_app.config:
        current_app.config["uvle_client"] = UVLeClient(creds)
    return current_app.config["uvle_client"]


@uvle.route("/courses")
def moodle_get_classes():
    client = create_uvle_client(current_user.uvle_account)
    return dumps(client.get_classes(), cls=LearningEnvClassEnc)


@uvle.route("/deadlines")
def moodle_get_deadlines():
    # Get deadlines from Moodle
    client = create_uvle_client(current_user.uvle_account)
    raw_deadlines: list[Deadline] = client.get_deadlines()
    return dumps(sort_deadlines(raw_deadlines))