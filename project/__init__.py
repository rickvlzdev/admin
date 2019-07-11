import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()

def create_app(script_info=None):
  app = Flask(__name__)

  app_settings = os.getenv('APP_SETTINGS')
  app.config.from_object(app_settings)

  db.init_app(app)
  login.init_app(app)
  mail.init_app(app)

  from project.auth import bp as auth_bp
  app.register_blueprint(auth_bp, url_prefix='/auth')

  from project.main import bp as main_bp
  app.register_blueprint(main_bp)

  from project.errors import bp as errors_bp
  app.register_blueprint(errors_bp)

  from project.models import User

  @app.shell_context_processor
  def ctx():
    return {'app': app, 'db': db, 'User': User}

  return app
