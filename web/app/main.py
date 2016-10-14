from logging.handlers import RotatingFileHandler
from app_factory import create_app


if __name__ == "__main__":

    app = create_app()

    handler = RotatingFileHandler("/web/logs/webapp.log", maxBytes=100000, backupCount=1)
    # handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', debug=True, port=80)
