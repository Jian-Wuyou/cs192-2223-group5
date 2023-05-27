from flask import Blueprint, render_template

register = Blueprint("register", __name__)


@register.route("/register")
def register_page():
    return render_template("lms/register.html")