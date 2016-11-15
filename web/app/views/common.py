from flask import Blueprint, redirect, url_for

from flask_dance.contrib.google import google

module_common = Blueprint('module_common', __name__)


@module_common.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["emails"][0]["value"])

