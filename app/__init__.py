from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# loginmanager importieren
from flask_login import LoginManager
from config import Config
from flask_bootstrap import Bootstrap
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_wtf import CSRFProtect





app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# hier wird die erweiterung inistalisiert
login = LoginManager(app)
login.login_view = 'login'

bootstrap = Bootstrap(app)
csrf = CSRFProtect(app)


#LOGVERZEICHNISS ERSTELLEN BEI FEHLER
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/PAITARARBEIT.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in (pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('PAITARARBEIT startup')

from app import routes, models, errors, api
