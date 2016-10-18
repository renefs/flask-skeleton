from flask.ext.security import SQLAlchemyUserDatastore
from flask_restful import Api
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
# from flask_sso import SSO
from flask_assets import Environment


"""
All the extensions are loaded here except the Api, which is loaded using different blueprints
on the api module.
"""
api = Api()
assets = Environment()
db = SQLAlchemy()
# sso = SSO(app=None)
security = Security()
# Setup Flask-Security
from users.models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
