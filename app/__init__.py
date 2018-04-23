from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_admin import Admin


db = SQLAlchemy()
app_admin = Admin(name='API auto',template_mode='bootstrap3')


def create_app(config_name):
    """Use factory to product app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    # flask_admin
    app_admin.init_app(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .admin import sd_admin as sd_admin_blueprint
    app.register_blueprint(sd_admin_blueprint)

    print('^_^ APP is created ^_^')
    return app
