import uuid

from flask import flash
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.contrib.google import make_google_blueprint
from flask_login import (
    LoginManager, current_user,
    login_user
)

<<<<<<< HEAD
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend

=======
>>>>>>> 9e0f916b1e264167d2c0dcdf03a929b98d24dc41
from app.extensions import db
from app.models import user_datastore
from app.models.users import User, OAuth


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
            email = resp.json()['emails'][0]['value']
            existing_user = user_datastore.find_user(email=email)
            flash("User already exist")
            if not existing_user:
                flash("User does not exist")
                # create a user
                existing_user = user_datastore.create_user(username=email, email=email, password=str(uuid.uuid4()))
                user_datastore.commit()
            login_user(existing_user)
            flash("Successfully signed in with Google")
        else:
            msg = "Failed to fetch user info from {name}".format(name=blueprint.name)
            flash(msg, category="error")

    login_manager.init_app(app)
