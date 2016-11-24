import argparse
from logging.handlers import RotatingFileHandler
from app.app_factory import create_app
from app.config import BaseConfig
from app.extensions import db

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the application')
    parser.add_argument('-s', '--setup', dest='run_setup', action='store_true', help='Sets up database and tables')
    parser.add_argument('-r', '--reset', dest='run_reset', action='store_true', help='Resets database and tables')

    args = parser.parse_args()

    app = create_app(BaseConfig)

    if args.run_setup:
        with app.app_context():
            db.create_all()

    if args.run_reset:
        with app.app_context():
            db.drop_all()
            db.create_all()

    else:
        # handler = RotatingFileHandler("/web/logs/webapp.log", maxBytes=100000, backupCount=1)
        # handler.setLevel(logging.DEBUG)
        # app.logger.addHandler(handler)
        app.run(host='0.0.0.0', debug=True, port=80)
