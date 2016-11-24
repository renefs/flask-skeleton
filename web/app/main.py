from app.app_factory import create_app
from app.cli import initialize_cli
from app.config import BaseConfig

app = create_app(BaseConfig)

initialize_cli(app)

if __name__ == "__main__":
        # handler = RotatingFileHandler("/web/logs/webapp.log", maxBytes=100000, backupCount=1)
        # handler.setLevel(logging.DEBUG)
        # app.logger.addHandler(handler)
        app.run(host='0.0.0.0', debug=True, port=80)
