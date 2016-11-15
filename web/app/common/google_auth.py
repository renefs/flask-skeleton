from flask_login import (
    LoginManager, current_user,
    login_required, login_user, logout_user
)

from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend

from app.extensions import db
from app.models.users import User, OAuth


def load_flash_dance_blueprints(application):
    blueprint = make_google_blueprint(
        client_id=application.config['GOOGLE_CLIENT_ID'],
        client_secret=application.config['GOOGLE_CLIENT_SECRET'],
        scope=["profile", "email"]
    )
    application.register_blueprint(blueprint, url_prefix="/login")

    # setup login manager
    login_manager = LoginManager()
    login_manager.login_view = 'google.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # setup SQLAlchemy backend
    blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)
