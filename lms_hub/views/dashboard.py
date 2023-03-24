from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def dashboard_page():
    uvle_islinked = "uvle" in current_user.accounts and current_user.accounts["uvle"].token != ""

    # User is returning, show normal dashboard
    return render_template(
        "dashboard.html",
        uvle_islinked=uvle_islinked
    )