# is-it-in-yet/app/models/user.py

from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """
    User model for storing user accounts and their authentication details.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Establish the one-to-many relationship with alerts
    # 'backref' creates a virtual 'user' attribute on the Alert model
    # 'lazy=True' means the alerts for a user are loaded on-demand
    alerts = db.relationship('Alert', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        """Hashes the user's password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'
