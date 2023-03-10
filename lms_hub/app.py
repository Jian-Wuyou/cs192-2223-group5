import json
from os import environ, path

import firebase_admin
from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_login import LoginManager

from lms_hub.controllers.database import Database
from lms_hub.models.profile import Profile
from lms_hub.views import init_views

# Environment variables
load_dotenv()

# Flask app
root_path = path.abspath(path.join(path.dirname(__file__), ".."))
app = Flask(__name__, root_path=root_path)


app.secret_key = environ["FLASK_SECRET_KEY"]
login_manager = LoginManager()
login_manager.init_app(app)

cred = firebase_admin.credentials.Certificate(environ["FIREBASE_CREDENTIALS_FILE"])

firebase_admin.initialize_app(cred, {"databaseURL": environ["FIREBASE_DATABASE_URL"]})
app.config["DB"] = Database(firebase_admin.db.reference())

with open(environ["GOOGLE_CREDENTIALS_FILE"], encoding="utf-8") as file:
    data = json.load(file)
    app.config["GOOGLE_CLIENT_ID"] = data["web"]["client_id"]
    app.config["GOOGLE_CLIENT_SECRET"] = data["web"]["client_secret"]

# User loader
@login_manager.user_loader
def user_loader(user_id: str) -> Profile:
    return app.config["DB"].lookup_user_by_id(user_id)


# Unauthorized error handler
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login.login_page") + "?next=" + request.path)

init_views(app)

# Run app
if __name__ == "__main__":
    app.run(debug=True)