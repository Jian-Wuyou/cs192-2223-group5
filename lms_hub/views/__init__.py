from flask import Flask

from .calendar import calendar
from .classcard import classcard
from .dashboard import dashboard
from .link_lms.uvle import UVLe
from .link_lms.gclass import GClass
from .login import login
from .logout import logout
from .settings import settings


def init_views(app: Flask):
    app.register_blueprint(calendar)
    app.register_blueprint(classcard)
    app.register_blueprint(dashboard)
    app.register_blueprint(UVLe)
    app.register_blueprint(GClass)
    app.register_blueprint(login)
    app.register_blueprint(logout)
    app.register_blueprint(settings)