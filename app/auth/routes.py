# is-it-in-yet/app/auth/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import db
from .forms import LoginForm, SignupForm
from app.models.user import User

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles user signup."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = SignupForm()
    if form.validate_on_submit():
        # Create a new user instance
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        
        # Add the new user to the database
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('signup.html', title='Sign Up', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
            
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.dashboard'))
        
    return render_template('login.html', title='Log In', form=form)

@auth_bp.route('/logout')
def logout():
    """Handles user logout."""
    logout_user()
    return redirect(url_for('main.index'))