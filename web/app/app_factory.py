from flask import Flask
from flask import flash
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_login import LoginManager, login_user

from common.resources.v1 import example_api_v1_bp, API_VERSION_V1
from extensions import assets, db, security, api, user_datastore
import static_assets

from flask_dance.contrib.google import make_google_blueprint

from flask_login import (
    current_user
)


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app=app)

    @app.before_first_request
    def setup_database():
        db.create_all()

    assets.init_app(app=app)
    # Setup Flask-Security
    security.init_app(app=app, datastore=user_datastore)
    api.init_app(app=app)

    _load_blueprints(app)
    _load_api_module(app)
    _load_flask_dance_authorization(app)

    with app.app_context():
        static_assets.register_assets()

    return app


def _load_blueprints(app):
    from common.views import module as module_common
    app.register_blueprint(module_common)

    from users.views import module as module_users
    app.register_blueprint(module_users)


def _load_api_module(app):
    app.register_blueprint(
        example_api_v1_bp, url_prefix='{prefix}/v{version}'.format(
            prefix=app.config['API_URL_PREFIX'],
            version=API_VERSION_V1))


def _load_flask_dance_authorization(app):
    from users.models import User, OAuth

    blueprint = make_google_blueprint(
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        scope=["profile", "email"],
        offline=True
    )
    app.register_blueprint(blueprint, url_prefix="/login")

    # setup login manager
    login_manager = LoginManager()
    login_manager.login_view = 'google.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # setup SQLAlchemy backend
    blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)


    # create/login local user on successful OAuth login
    @oauth_authorized.connect_via(blueprint)
    def google_logged_in(blueprint, token):
        if not token:
            flash("Failed to log in with {name}".format(name=blueprint.name))
            return
        # figure out who the user is
        resp = blueprint.session.get("/plus/v1/people/me")
        # TODO Extract the position of the account email
        flash("You are {name}".format(name=resp.json()['emails'][0]['value']))
        if resp.ok:
            username = resp.json()['emails'][0]['value']
            existing_user = user_datastore.find_user(username=username)
            flash("User already exist")
            if not existing_user:
                flash("User does not exist")
                # create a user
                existing_user = user_datastore.create_user(username=username)
                user_datastore.commit()
            login_user(existing_user)
            flash("Successfully signed in with Google")
        else:
            msg = "Failed to fetch user info from {name}".format(name=blueprint.name)
            flash(msg, category="error")

    login_manager.init_app(app)