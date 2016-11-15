from app.extensions import db
from flask_login import UserMixin
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = (db.CheckConstraint('email = lower(email)', 'lowercase_email'),)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())


class OAuth(db.Model, OAuthConsumerMixin):
    __tablename__ = 'flask_dance_oauth'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
