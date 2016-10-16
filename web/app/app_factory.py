from flask import Flask

from common.resources.v1 import example_api_v1_bp, API_VERSION_V1
from extensions import assets, db, security, api
import static_assets
from config import BaseConfig


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

    with app.app_context():
        static_assets.register_assets()

    return app


def load_api_module(app):
    app.register_blueprint(
        example_api_v1_bp, url_prefix='{prefix}/v{version}'.format(
            prefix=app.config['API_URL_PREFIX'],
            version=API_VERSION_V1))
