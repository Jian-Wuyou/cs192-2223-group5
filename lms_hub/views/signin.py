from flask import Blueprint, render_template

signin = Blueprint("signin", __name__)


@signin.route("/signin")
def signin_page():
    return render_template("lms/signin.html")