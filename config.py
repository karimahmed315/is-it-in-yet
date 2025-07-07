# is-it-in-yet/config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    """
    Base configuration class. Contains default settings and settings loaded
    from environment variables.
    """
    # --- Core Application Settings ---
    # A secret key is required for session management and security features like CSRF protection.
    # It should be a long, random string. We'll pull it from an environment variable.
    SECRET_KEY = os.getenv('SECRET_KEY', 'a-very-secret-key-that-you-should-change')

    # --- Database Settings ---
    # This specifies the database URI. For development, we'll use a simple SQLite database.
    # For production, you would change this to a PostgreSQL or MySQL URI.
    # The 'instance' folder is a special Flask folder that is not tracked by Git,
    # making it a safe place for the development database.
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///../instance/isitinyet.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disables a feature that signals the application every time a change is about to be made in the database, which is not needed.

    # --- Email Settings for Notifications ---
    # These will be used later for sending alerts.
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    # --- Celery (Background Tasks) Settings ---
    # Connects our application to the Redis server for managing background jobs.
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
