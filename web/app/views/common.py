
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask_security import current_user, login_required

common_bp = Blueprint('common', __name__)


@common_bp.route("/")
@login_required
def index():

    if current_user.is_authenticated:
        return redirect(url_for("business.index"))
    #
    # current_app.logger.debug("Index route")
    # current_app.logger.info("Index route")
    # return render_template('index.html', variable=datetime.datetime.now(), current_user=current_user)