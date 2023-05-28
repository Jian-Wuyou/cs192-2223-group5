from flask import Flask

from .api_uvle import uvle
from .api_gclass import gclass

def init_api(app: Flask):
    app.register_blueprint(uvle, url_prefix="/api/uvle")
    app.register_blueprint(gclass, url_prefix="/api/gclass")