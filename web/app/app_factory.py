from flask import Flask

from app.api.v1 import example_api_v1_bp, API_VERSION_V1
from app.common import load_flask_dance_authorization
from app.extensions import db, security, api
from app.models import user_datastore
from app.static_assets import register_assets
from flask_migrate import Migrate


def create_app(config):
    application = Flask(__name__)
    application.config.from_object(config)

    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    application.jinja_env.add_extension('jinja2.ext.do')

    db.init_app(app=application)
    security.init_app(app=application, datastore=user_datastore)
    api.init_app(app=application)


    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    migrate = Migrate(application, db)

    _load_application_blueprints(application)

    _load_api_blueprints(application)

    load_flask_dance_authorization(application)

    register_assets(application)

    _register_global_variables(application)

    return application


def _register_global_variables(application):
    @application.context_processor
    def inject_application_data():
        return dict(global_app_name=application.config.get('APP_NAME', 'TO DO'))


def _load_application_blueprints(application):
    from app.views.common import common_bp
    application.register_blueprint(common_bp)

    from app.views.users import module as module_users
    application.register_blueprint(module_users)

    from app.views.business import module as module_business
    application.register_blueprint(module_business)


def _load_api_blueprints(application):
    application.register_blueprint(
        example_api_v1_bp, url_prefix='{prefix}/v{version}'.format(
            prefix=application.config['API_URL_PREFIX'],
            version=API_VERSION_V1))
