# is-it-in-yet/app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from celery import Celery

# Initialize all extensions here
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
celery = Celery(__name__,
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')
