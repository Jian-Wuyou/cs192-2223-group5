from flask import Flask
from .login import login

def init_views(app: Flask):
    app.register_blueprint(login)