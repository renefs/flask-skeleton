from flask import current_app
from flask import request
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_login import LoginManager, current_user

from app.extensions import db
from app.models.users import OAuth, User
from .google_auth import load_google_authentication
from .facebook_auth import load_facebook_authentication


def load_flask_dance_authorization(app):
    facebook_bp = load_google_authentication(app)
    google_bp = load_facebook_authentication(app)

    # setup login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))

    @login_manager.user_loader
    def load_user(user_id):
        """
        This will be used many times like on using current_user
        :param user_id: username
        :return: user or none
        """
        # http://librelist.com/browser/flask/2012/4/7/current-blueprint/#44814417e8289f5f5bb9683d416ee1ee
        blueprint = current_app.blueprints[request.blueprint]

        if hasattr(blueprint, 'load_user'):
            # return User.query.get(int(user_id))
            return blueprint.load_user(user_id)

        # https://flask-login.readthedocs.org/en/latest/#how-it-works
        return None

    # setup SQLAlchemy backend
    facebook_bp.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)
    google_bp.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

