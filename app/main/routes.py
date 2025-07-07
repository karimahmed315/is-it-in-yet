# is-it-in-yet/app/main/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db # Import db from extensions
from app.models import Alert
from .forms import AlertForm
from app.tasks import run_scrape_task # <-- CHANGE: Import from the new tasks file

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    """Serves the landing page."""
    return render_template('index.html')

@main_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = AlertForm()

    if form.validate_on_submit():
        product_url = form.product_url.data
        
        existing_alert = Alert.query.filter_by(user_id=current_user.id, product_url=product_url).first()
        if existing_alert:
            flash('You are already tracking this product.', 'info')
        else:
            new_alert = Alert(product_url=product_url, user_id=current_user.id)
            db.session.add(new_alert)
            db.session.commit()
            
            run_scrape_task.delay(new_alert.id)
            
            flash('New alert added! We are fetching the product details now.', 'success')
        
        return redirect(url_for('main.dashboard'))

    user_alerts = Alert.query.filter_by(user_id=current_user.id).order_by(Alert.created_at.desc()).all()
    return render_template('dashboard.html', user=current_user, form=form, alerts=user_alerts)

