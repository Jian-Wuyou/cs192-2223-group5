import json
from os import environ, path

import firebase_admin
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, Response, request
from flask_login import LoginManager, current_user

from lms_hub.controllers.database import Database
from lms_hub.models.profile import Profile
from lms_hub.views import init_views
from lms_hub.controllers import init_api

# Environment variables
load_dotenv()

# FOR DEPLOYMENT: construct FIREBASE_CREDENTIALS_FILE
FIREBASE_CREDENTIALS_FILE = {
    "type": environ["FIREBASE_TYPE"],
    "project_id": environ["FIREBASE_PROJECT_ID"],
    "private_key_id": environ["FIREBASE_PRIVATE_KEY_ID"],
    "private_key": environ["FIREBASE_PRIVATE_KEY"],
    "client_email": environ["FIREBASE_CLIENT_EMAIL"],
    "client_id": environ["FIREBASE_CLIENT_ID"],
    "auth_uri": environ["FIREBASE_AUTH_URI"],
    "token_uri": environ["FIREBASE_TOKEN_URI"],
    "auth_provider_x509_cert_url": environ["FIREBASE_AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": environ["FIREBASE_CLIENT_X509_CERT_URL"]
}

GOOGLE_CREDENTIALS = {
    "web": {
        "client_id": environ["GOOGLE_CLIENT_ID"],
        "project_id": environ["GOOGLE_PROJECT_ID"],
        "auth_uri": environ["GOOGLE_AUTH_URI"],
        "token_uri": environ["GOOGLE_TOKEN_URI"],
        "auth_provider_x509_cert_url": environ["GOOGLE_AUTH_PROVIDER_X509_CERT_URL"],
        "client_secret": environ["GOOGLE_CLIENT_SECRET"],
        "redirect_uris": json.loads(environ["GOOGLE_REDIRECT_URIS"]),
        "javascript_origins": json.loads(environ["GOOGLE_JAVASCRIPT_ORIGINS"])
    }
}

# Flask app
root_path = path.abspath(path.join(path.dirname(__file__), ".."))
app = Flask(__name__, root_path=root_path)
app.config.from_prefixed_env()
print(app.config["PREFERRED_URL_SCHEME"])

app.secret_key = environ["FLASK_SECRET_KEY"]
login_manager = LoginManager()
login_manager.init_app(app)

cred = firebase_admin.credentials.Certificate(FIREBASE_CREDENTIALS_FILE)

firebase_admin.initialize_app(cred, {"databaseURL": environ["FIREBASE_DATABASE_URL"]})
app.config["DB"] = Database(firebase_admin.db.reference())


app.config["GOOGLE_CREDENTIALS"] = GOOGLE_CREDENTIALS
app.config["GOOGLE_CLIENT_ID"] = GOOGLE_CREDENTIALS["web"]["client_id"]
app.config["GOOGLE_CLIENT_SECRET"] = GOOGLE_CREDENTIALS["web"]["client_secret"]

init_views(app)
init_api(app)

# User loader
@login_manager.user_loader
def user_loader(user_id: str) -> Profile:
    return app.config["DB"].lookup_user_by_id(user_id)

# Unauthorized error handler
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login.login_page") + "?next=" + request.path)

@app.after_request
def add_cors(resp: Response):
    # Allow all domains for now
    resp.headers.update({
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, X-Requested-With",
        "Access-Control-Allow-Credentials": "true"
    })
    return resp

@app.route("/", methods=["GET"])
def index():
    # Redirect to dashboard if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_page"))
    return redirect(url_for("login.login_page"))

# Run app
if __name__ == "__main__":
    environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run("localhost", 29001, debug=True)