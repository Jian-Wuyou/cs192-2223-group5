from json import dumps

from flask import Blueprint, current_app, redirect, url_for
from flask_login import current_user, login_required
from lms_hub.controllers.gclass import GoogleClassroomClient
from lms_hub.models.credentials import GoogleCredentials
from lms_hub.models.deadline import sort_deadlines
from lms_hub.models.learning_env_class import LearningEnvClassEnc

gclass = Blueprint("gclass", __name__)

# Nice way to require login for entire blueprint
@gclass.before_request
@login_required
def gclass_before_request():
    # Check if user has Google credentials
    if "gclass" not in current_user.accounts:
        # Redirect to Google account linking page
        return redirect(url_for("link-gclass.login_page"))
    return None


# Will run if tokens are updated
def on_token_refresh(google_credentials: GoogleCredentials):
    # Update credentials in DB
    db = current_app.config["DB"]
    db.update_user_lms_creds(
        "gclass", current_user.user_id, google_credentials
    )


@gclass.route("/classes")
@login_required
def gclass_get_classes():
    # Perform request for all linked accounts
    all_classes = {}

    google_credentials = current_user.accounts["gclass"]

    # Get list of classes from Google Classroom API
    client = GoogleClassroomClient(
        google_credentials,
        current_app.config["GOOGLE_CLIENT_SECRET"],
        on_token_refresh,
    )
    all_classes = client.get_classes()

    # The classes are returned as a list of GoogleClass dataclass instances,
    # so we need to serialize them to JSON.
    return dumps({"courses": all_classes}, cls=LearningEnvClassEnc)


@gclass.route("/deadlines")
@login_required
def gclass_get_deadlines():
    # Perform request for all linked accounts
    raw_deadlines = []

    google_credentials = current_user.accounts['gclass']

    # Get list of coursework from Google Classroom API
    client = GoogleClassroomClient(
        google_credentials,
        current_app.config["GOOGLE_CLIENT_SECRET"],
        on_token_refresh,
    )
    raw_deadlines.extend(client.get_deadlines())

    # The coursework is returned as a list of GoogleCoursework dataclass instances,
    # so we need to serialize them to JSON.
    return dumps({"deadlines": sort_deadlines(raw_deadlines)})
