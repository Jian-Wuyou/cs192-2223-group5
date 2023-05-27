from flask import Flask

from .calendar import calendar
from .classcard import classcard
from .dashboard import dashboard
from .link_lms.uvle import UVLe
from .login import login
from .logout import logout
from .register import register
from .settings import settings
from .signin import signin


def init_views(app: Flask):
    app.register_blueprint(calendar)
    app.register_blueprint(classcard)
    app.register_blueprint(dashboard)
    app.register_blueprint(UVLe)
    app.register_blueprint(login)
    app.register_blueprint(logout)
    app.register_blueprint(register)
    app.register_blueprint(settings)
    app.register_blueprint(signin)