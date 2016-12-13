import uuid

from flask import flash
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import make_google_blueprint
from flask_login import (
    login_user
)

from app.models import user_datastore


def load_google_authentication(app):
    blueprint = make_google_blueprint(
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        scope=["profile", "email"],
        offline=True
    )
    app.register_blueprint(blueprint, url_prefix="/login")

    # create/login local user on successful OAuth login
    @oauth_authorized.connect_via(blueprint)
    def google_logged_in(blueprint, token):
        if not token:
            flash("Failed to log in with {name}".format(name=blueprint.name))
            return
        # figure out who the user is
        resp = blueprint.session.get("/plus/v1/people/me")
        # app.logger.debug(resp.json())
        # TODO Extract the position of the account email
        if resp.ok:
            email = resp.json()['emails'][0]['value']
            avatar = resp.json()['image']['url']
            existing_user = user_datastore.find_user(email=email)
            if not existing_user:
                # create a user
                existing_user = user_datastore.create_user(username=email, email=email, password=str(uuid.uuid4()))
                existing_user.has_auto_generated_password = True

            existing_user.avatar = avatar
            user_datastore.commit()
            login_user(existing_user)
            flash("Successfully signed in with Google", 'success')
        else:
            msg = "Failed to fetch user info from {name}".format(name=blueprint.name)
            flash(msg, category="error")

    @blueprint.record_once
    def on_load(state):
        """
        http://stackoverflow.com/a/20172064/742173

        :param state: state
        """
        state.app.login_manager.blueprint_login_views[blueprint.name] = 'google.login'

    return blueprint
