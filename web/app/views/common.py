import datetime

from flask import Blueprint, render_template
from flask import current_app
from flask_dance.contrib.google import google
from oauthlib.oauth2 import InvalidGrantError, TokenExpiredError

common_bp = Blueprint('module_common', __name__)


def token_is_expired():
    try:
        resp = google.get("/plus/v1/people/me")
        assert resp.ok, resp.text
    except (InvalidGrantError, TokenExpiredError) as e:  # or maybe any OAuth2Error
        return True


@common_bp.route("/")
def index():
    current_app.logger.debug("Index route")
    return render_template('index.html', variable=datetime.datetime.now())