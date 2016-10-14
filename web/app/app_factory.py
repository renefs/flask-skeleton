from flask import Flask
from extensions import assets, db, security, api
import static_assets
from config import BaseConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    db.init_app(app=app)
    api.init_app(app=app)
    assets.init_app(app=app)
    security.init_app(app=app)

    from views.common import module_common
    app.register_blueprint(module_common)

    with app.app_context():
        static_assets.register_assets()

    return app
