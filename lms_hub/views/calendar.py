from flask import Blueprint, render_template
from flask_login import login_required, current_user

calendar = Blueprint("calendar", __name__)


@calendar.route("/calendar")
# @login_required
def calendar_page():
    return render_template("lms/calendar.html", active_nav="calendar")