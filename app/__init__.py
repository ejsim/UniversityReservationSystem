import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_assets import Environment
from flask_wtf import CsrfProtect
from flask_compress import Compress
from flask_rq import RQ
from flask_restless import APIManager
from config import config
from .assets import app_css, app_js, vendor_css, vendor_js

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()
csrf = CsrfProtect()
compress = Compress()

# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    config[config_name].init_app(app)

    # Set up extensions
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    compress.init_app(app)
    RQ(app)



    with app.app_context():
        from .models import User, Role, Campus, Location, Department, Equipment_Type, Condition, Equipment, Equipment_Reservation, Space_Type, Space, Ammenity_Type, Space_Ammenity, Space_Reservation
        flask_manager = APIManager(app, flask_sqlalchemy_db=db)
        flask_manager.create_api(User, methods=[], results_per_page=0)
        flask_manager.create_api(Ammenity_Type, methods=['GET'], results_per_page=0)
        flask_manager.create_api(Campus, methods=['GET'], results_per_page=0)
        location_blueprint = flask_manager.create_api_blueprint(Location, methods=['GET', 'POST'], results_per_page=0)
        csrf.exempt(location_blueprint)
        app.register_blueprint(location_blueprint)
        flask_manager.create_api(Department, methods=['GET'], results_per_page=0)
        equipment_blueprint = flask_manager.create_api_blueprint(Equipment, methods=['GET', 'POST'], results_per_page=0)
        csrf.exempt(equipment_blueprint)
        app.register_blueprint(equipment_blueprint)
        flask_manager.create_api(Equipment_Reservation, methods=['GET'], results_per_page=0)
        flask_manager.create_api(Equipment_Type, methods=['GET'], results_per_page=0)
        flask_manager.create_api(Role, methods=['GET'], results_per_page=0)
        flask_manager.create_api(Space_Ammenity, methods=['GET'], results_per_page=0)
        flask_manager.create_api(Space_Reservation, methods=['GET'], results_per_page=0)
        flask_manager.create_api(Space_Type, methods=['GET'], results_per_page=0)
        space_blueprint = flask_manager.create_api_blueprint(Space, methods=['GET', 'POST'], results_per_page=0)
        csrf.exempt(space_blueprint)
        app.register_blueprint(space_blueprint)

    # Register Jinja template functions
    from .utils import register_template_utils
    register_template_utils(app)

    # Set up asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/styles', 'assets/scripts']
    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))
    assets_env.url_expire = True

    assets_env.register('app_css', app_css)
    assets_env.register('app_js', app_js)
    assets_env.register('vendor_css', vendor_css)
    assets_env.register('vendor_js', vendor_js)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Create app blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .reserve import reserve as reserve_blueprint
    app.register_blueprint(reserve_blueprint, url_prefix='/reserve')

    from .api import api as api_blueprint
    print("api should be exempt")
    app.register_blueprint(api_blueprint, url_prefix='/api')
    csrf.exempt(api_blueprint)

    return app
