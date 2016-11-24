from flask import Blueprint
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import login_required, logout_user

module = Blueprint('users', __name__)


@module.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("common.index"))