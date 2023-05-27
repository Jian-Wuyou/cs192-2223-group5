from flask import Blueprint, render_template
from flask_login import login_required, current_user

classcard = Blueprint("classcard", __name__)


@classcard.route("/classcard")
# @login_required
def classcard_page():
    return render_template("lms/classcard.html", active_nav="classcard")