from logging.handlers import RotatingFileHandler
from app_factory import create_app
import argparse
from extensions import db

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the application')
    parser.add_argument('-s', '--setup', dest='run_setup', action='store_true', help='Sets up database and tables')

    args = parser.parse_args()

    app = create_app()

    if args.run_setup:
        with app.app_context():
            db.create_all()
    else:
        handler = RotatingFileHandler("/web/logs/webapp.log", maxBytes=100000, backupCount=1)
        # handler.setLevel(logging.DEBUG)
        app.logger.addHandler(handler)
        app.run(host='0.0.0.0', debug=True, port=80)
