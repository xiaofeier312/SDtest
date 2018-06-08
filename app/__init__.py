from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_admin import Admin
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
app_admin = Admin(name='API auto', template_mode='bootstrap3')
bootstrap = Bootstrap()


def create_app(config_name):
    """Use factory to product app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    app.config['SQLALCHEMY_POOL_PRE_PING'] = True  # Try to fix auto disconnect bug
    app.config['pool_pre_ping'] = True
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 1

    # flask_admin
    app_admin.init_app(app)
    bootstrap.init_app(app)
    # set flask admin swatch
    app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    init_custom_view()  # !!!When first create DB, comment this. or it will occur exception: cannot find table XXX
    print('^_^ APP is created ^_^')
    return app


# Add_view
def init_custom_view():
    """customModelView for every data class"""
    from app import app_admin
    from app.admin.views import CustomModelView, projectsModelView, modulesModelView, DocModelView, caseModelView, \
        verifyModelView, resultModelView
    from app.models import APIProjects, APIModules, APICases, APIDoc, TomcatEnv, CasesVerify

    app_admin.add_view(CustomModelView(TomcatEnv, db.session, category='新增'))
    app_admin.add_view(projectsModelView(APIProjects, db.session, category='新增'))
    app_admin.add_view(modulesModelView(APIModules, db.session, category='新增'))
    app_admin.add_view(DocModelView(APIDoc, db.session, category='新增'))
    app_admin.add_view(caseModelView(APICases, db.session, category='新增'))
    app_admin.add_view(verifyModelView(CasesVerify, db.session, category='新增'))
    app_admin.add_view(verifyModelView(CasesVerify, db.session, endpoint='ss'))
