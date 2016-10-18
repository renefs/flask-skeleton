from flask import Flask

from common.resources.v1 import example_api_v1_bp, API_VERSION_V1
from extensions import assets, db, security, api
import static_assets
from config import BaseConfig
from flask_dance.contrib.google import make_google_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    db.init_app(app=app)
    assets.init_app(app=app)
    # security.init_app(app=app)
    api.init_app(app=app)

    from common.views import module_common
    app.register_blueprint(module_common)

    load_api_module(app)

    load_flask_dance_authorization(app)

    with app.app_context():
        static_assets.register_assets()

    return app


def load_api_module(app):
    app.register_blueprint(
        example_api_v1_bp, url_prefix='{prefix}/v{version}'.format(
            prefix=app.config['API_URL_PREFIX'],
            version=API_VERSION_V1))


def load_flask_dance_authorization(app):
    blueprint = make_google_blueprint(
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        scope=["profile", "email"]
    )
    app.register_blueprint(blueprint, url_prefix="/login")
