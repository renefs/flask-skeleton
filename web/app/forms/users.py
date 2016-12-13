from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, ValidationError, StringField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, DataRequired
from app.models import user_datastore


class UniqueUser(object):
    def __init__(self, message="User exists"):
        self.message = message

    def __call__(self, form, field):
        if user_datastore.find_user(email=field.data):
            raise ValidationError(self.message)


validators = {
    'email': [
        DataRequired(),
        Email(),
        UniqueUser(message='Email address is associated with '
                           'an existing account')
    ],
    'password': [
        DataRequired(),
        Length(min=6, max=50),
        EqualTo('confirm', message='Passwords must match'),
        Regexp(r'[A-Za-z0-9@#$%^&+=]',
               message='Password contains invalid characters')
    ]
}


class RegisterForm(FlaskForm):
    email = StringField('Email', validators['email'])
    password = PasswordField('Password', validators['password'], )
    confirm = PasswordField('Confirm Password')


class ChangeSocialPasswordForm(FlaskForm):
    password = PasswordField('Password', validators['password'], )
    confirm = PasswordField('Confirm Password')