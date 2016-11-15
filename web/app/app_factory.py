from flask import Flask

from app.api.v1 import example_api_v1_bp, API_VERSION_V1
from app.common.google_auth import load_flash_dance_blueprints
from app.config import BaseConfig
from app.extensions import db, security, api
from app.static_assets import register_assets


def create_app():
    application = Flask(__name__)
    application.config.from_object(BaseConfig)

    db.init_app(app=application)
    security.init_app(app=application)
    api.init_app(app=application)

    _load_application_blueprints(application)

    _load_api_module(application)
    load_flash_dance_blueprints(application)

    register_assets(application)

    return application


def _load_application_blueprints(application):
    from app.views.common import module_common
    application.register_blueprint(module_common)


def _load_api_module(application):
    application.register_blueprint(
        example_api_v1_bp, url_prefix='{prefix}/v{version}'.format(
            prefix=application.config['API_URL_PREFIX'],
            version=API_VERSION_V1))


