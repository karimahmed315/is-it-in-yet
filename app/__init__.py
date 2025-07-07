# is-it-in-yet/app/__init__.py

from flask import Flask
import os
from .extensions import db, login_manager, migrate, celery # Import from central file

def create_app():
    """
    Application factory function.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # --- Initialize Extensions with the app ---
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Update celery config with app config
    celery.conf.update(app.config)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        from .auth.routes import auth_bp
        from .main.routes import main_bp

        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(main_bp)

        db.create_all()

        return app