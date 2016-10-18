from flask import Flask
from flask import flash
from flask.ext.security import SQLAlchemyUserDatastore
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_login import LoginManager, login_user
from sqlalchemy.orm.exc import NoResultFound

from common.resources.v1 import example_api_v1_bp, API_VERSION_V1
from extensions import assets, db, security, api, user_datastore
import static_assets
from config import BaseConfig
from flask_dance.contrib.google import make_google_blueprint
from users.models import User, OAuth, Role

from flask_login import (
    current_user
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    db.init_app(app=app)

    @app.before_first_request
    def setup_database():
        db.create_all()

    assets.init_app(app=app)
    # Setup Flask-Security
    security.init_app(app=app, datastore=user_datastore)
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