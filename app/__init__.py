from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_admin import Admin
from app.admin.views import CustomModelView


db = SQLAlchemy()
app_admin = Admin(name='API auto')

def create_app(config_name):
    """Use factory to product app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    #flask_admin
    app_admin.init_app(app)
    from app.models import APIProjects, APIModules, APICases, APIDoc, TomcatEnv, CasesVerify
    app_admin.add_view(CustomModelView(APIProjects,db.session,category='新增'))
    app_admin.add_view(CustomModelView(TomcatEnv, db.session, category='新增'))
    app_admin.add_view(CustomModelView(APIModules, db.session, category='新增'))
    app_admin.add_view(CustomModelView(APIDoc, db.session, category='新增'))
    app_admin.add_view(CustomModelView(APICases, db.session, category='新增'))
    app_admin.add_view(CustomModelView(CasesVerify, db.session, category='新增'))



    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    print('^_^ APP is created ^_^')
    return app
