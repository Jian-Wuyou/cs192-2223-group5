from flask import Flask

from .api_uvle import uvle

def init_api(app: Flask):
    app.register_blueprint(uvle, url_prefix="/api/uvle")