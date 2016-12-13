from flask_security import RoleMixin
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_security import UserMixin

from app.extensions import db

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Role(Base, RoleMixin):
    __tablename__ = 'role'

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        assert name != '' or name is not None

        self.name = name
        self.description = description if description else ''

    def __repr__(self):
        return '<Role %r>' % self.name


class User(Base, UserMixin):
    __tablename__ = 'user'
    __table_args__ = (db.CheckConstraint('email = lower(email)', 'lowercase_email'),)

    username = db.Column(db.String(256), unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    has_auto_generated_password = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(256))

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User({}, {}, username={}): {}>'.format(self.id, self.username, self.email, self.is_authenticated)


class OAuth(db.Model, OAuthConsumerMixin):
    __tablename__ = 'flask_dance_oauth'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
