import datetime

from flask import Blueprint, render_template
from flask import current_app


module_common = Blueprint('module_common', __name__)


@module_common.route("/")
def hello():
    current_app.logger.debug("Index route")
    return render_template('index.html', variable=datetime.datetime.now())
