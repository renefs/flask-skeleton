import uuid

from flask import flash
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_login import (
    LoginManager, current_user,
    login_user
)

from app.extensions import db
from app.models import user_datastore
from app.models.users import User, OAuth


def load_facebook_authentication(app):
    blueprint = make_facebook_blueprint(
        client_id=app.config['FACEBOOK_CLIENT_ID'],
        client_secret=app.config['FACEBOOK_CLIENT_SECRET'],
        scope="email"
    )
    app.register_blueprint(blueprint, url_prefix="/login/facebook")

    def load_user(user_id):
        """
        This will be used many times like on using current_user
        :param user_id: username
        :return: user or none
        """
        user = None
        try:
            return User.query.get(int(user_id))
        except:
            # https://flask-login.readthedocs.org/en/latest/#how-it-works
            pass
        return user

    # create/login local user on successful OAuth login
    @oauth_authorized.connect_via(blueprint)
    def facebook_logged_in(blueprint, token):
        if not token:
            flash("Failed to log in with {name}".format(name=blueprint.name))
            return
        # figure out who the user is
        resp = blueprint.session.get("/me?fields=id,name,email")
        # resp = None
        app.logger.debug(resp.json())
        # # TODO Extract the position of the account email
        flash("You are {name}".format(name=resp.json()['name']))
        if resp.ok:
            # flash(resp)
            email = resp.json()['email']
            existing_user = user_datastore.find_user(email=email)
            flash("User already exist")
            if not existing_user:
                flash("User does not exist")
                # create a user
                existing_user = user_datastore.create_user(username=email, email=email, password=str(uuid.uuid4()))
                user_datastore.commit()
            result = login_user(existing_user)
            flash(result)
            flash(current_user.is_authenticated)
            flash("Successfully signed in with Facebook")
        else:
            msg = "Failed to fetch user info from {name}".format(name=blueprint.name)
            flash(msg, category="error")

    @blueprint.record_once
    def on_load(state):
        """
        http://stackoverflow.com/a/20172064/742173

        :param state: state
        """
        blueprint.load_user = load_user
        state.app.login_manager.blueprint_login_views[blueprint.name] = 'facebook.login'

    return blueprint

