from flask import Flask
from .login import login
from .logout import logout
from .dashboard import dashboard

def init_views(app: Flask):
    app.register_blueprint(login)
    app.register_blueprint(logout)
    app.register_blueprint(dashboard)