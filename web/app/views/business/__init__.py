from flask import Blueprint, render_template
from flask_login import login_required

module = Blueprint('business', __name__, url_prefix='/business')


@module.route('/')
@login_required
def index():
    """
    Home
    :return:
    """

    return render_template('business/index.html',)

