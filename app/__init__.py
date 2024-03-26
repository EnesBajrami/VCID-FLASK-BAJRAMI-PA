from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager  # Import des Login-Managers
from config import Config
from flask_bootstrap import Bootstrap
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_wtf import CSRFProtect

# Erstellen der Flask-App
app = Flask(__name__)
# Laden der Konfiguration aus der Config-Klasse
app.config.from_object(Config)
# Initialisieren der SQLAlchemy-Erweiterung für die Datenbankverwaltung
db = SQLAlchemy(app)
# Initialisieren der Flask-Migrate-Erweiterung für Datenbankmigrationen
migrate = Migrate(app, db)
# Initialisieren des Login-Managers
login = LoginManager(app)
login.login_view = 'login'  # Festlegen der Route für den Login

# Initialisieren der Bootstrap-Erweiterung für das Frontend-Styling
bootstrap = Bootstrap(app)
# Initialisieren des CSRF-Schutzes
csrf = CSRFProtect(app)

# Erstellen eines RotatingFileHandler für das Logging bei Produktionsumgebung
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/PAITARARBEIT.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('PAITARARBEIT startup')

# Import der Routen, Modelle, Fehlerbehandlungen und API-Endpunkte
from app import routes, models, errors, api
