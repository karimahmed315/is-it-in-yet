# is-it-in-yet/app/models/alert.py

from app import db

class Alert(db.Model):
    """
    Alert model for storing product tracking information.
    """
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    product_url = db.Column(db.String(2048), nullable=False)
    product_name = db.Column(db.String(255), nullable=True) # We can scrape this later
    status = db.Column(db.String(50), nullable=False, default='Checking...') # e.g., 'In Stock', 'Out of Stock'
    last_checked = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Foreign Key to link to the User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Alert for {self.product_url}>'

