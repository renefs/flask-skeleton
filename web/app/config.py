import os


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")


class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = str2bool(os.environ['DEBUG'])

    APP_NAME = os.environ['APP_NAME']

    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASS = os.environ['DB_PASS']
    DB_SERVICE = os.environ['DB_SERVICE']
    DB_PORT = os.environ['DB_PORT']

    LOGS_FOLDER = os.environ['LOGS_FOLDER']

    API_URL_PREFIX = os.environ['API_URL_PREFIX']

    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
    GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']

    FACEBOOK_CLIENT_ID = os.environ['FACEBOOK_CLIENT_ID']
    FACEBOOK_CLIENT_SECRET = os.environ['FACEBOOK_CLIENT_SECRET']


class TestConfig(object):
    pass
