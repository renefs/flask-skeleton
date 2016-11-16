from flask_security import SQLAlchemyUserDatastore
from flask_restful import Api
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy


"""
All the extensions are loaded here except the Api, which is loaded using different blueprints
on the api module.
"""
api = Api()
db = SQLAlchemy()
security = Security()
# Setup Flask-Security
from app.models.users import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
