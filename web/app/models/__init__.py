from flask_security import SQLAlchemyUserDatastore
from app.extensions import db
from .users import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)