from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_admin import Admin
from flask_bootstrap import Bootstrap
import subprocess
from app.admin.views import myAdminModelView
from config import NormalConfig

db = SQLAlchemy()
app_admin = Admin(template_mode='bootstrap3', name='Compare tools')
# app_admin = Admin(name='API auto', template_mode='bootstrap3', url='/admin')
bootstrap = Bootstrap()


def create_app(config_name):
    """
    se factory to product app
    :param config_name:
    :return:
    """
    normal_config = NormalConfig()
    config_name = normal_config.get_current_env()
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    app.config['SQLALCHEMY_POOL_PRE_PING'] = True  # Try to fix auto disconnect bug
    app.config['pool_pre_ping'] = True
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 1

    # flask_admin
    app_admin.init_app(app, index_view=myAdminModelView(name='运行对比'))
    bootstrap.init_app(app)
    # set flask admin swatch
    app.config['FLASK_ADMIN_SWATCH'] = 'journal'  # cerulean  #superhero #flatly  #Amelia #journal

    from .main import main as main_blueprint
    from .task import task as task_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/main')
    app.register_blueprint(task_blueprint, url_prefix='/task')

    init_custom_view()  # !!!When first create DB, comment this. or it will occur exception: cannot find table XXX

    # os.system('./shell/run_ftp.sh&')
    print('^_^ APP is created ^_^')
    return app


# Add_view
def init_custom_view():
    """
    customModelView for every data class
    :return:
    """
    # from app import app_admin
    from app.admin.views import CustomModelView, projectsModelView, modulesModelView, DocModelView, caseModelView, \
        verifyModelView, resultModelView, runCaseModelView, ReviewResultModelView, myAdminModelView
    from app.models import APIProjects, APIModules, APICases, APIDoc, TomcatEnv, CasesVerify, ParameterData, \
        ReplaceInfo, RunCase, BlueprintTask, BlueprintSubtask

    app_admin.add_view(CustomModelView(TomcatEnv, db.session, category='新增'))
    app_admin.add_view(projectsModelView(APIProjects, db.session, category='新增'))
    app_admin.add_view(modulesModelView(APIModules, db.session, category='新增'))
    app_admin.add_view(DocModelView(APIDoc, db.session, category='新增'))
    app_admin.add_view(caseModelView(APICases, db.session, category='新增'))
    app_admin.add_view(verifyModelView(CasesVerify, db.session, category='新增'))
    app_admin.add_view(CustomModelView(ParameterData, db.session, category='新增'))
    app_admin.add_view(CustomModelView(ReplaceInfo, db.session, category='新增'))
    app_admin.add_view(runCaseModelView(RunCase, db.session, category='运行'))
    app_admin.add_view(ReviewResultModelView(name='结果对比：', category='查看结果'))
    app_admin.add_view(CustomModelView(BlueprintTask, db.session, category='任务管理'))
    app_admin.add_view(CustomModelView(BlueprintSubtask, db.session, category='任务管理'))


def start_ftp_server(port=8091):
    """
    Start ftp server for downloading result file, should use subprocess??
    :param port:
    :return:
    """
    port_str = str(port)
    print('>>>>> Run FTP server:')
    subprocess.call('python -m http.server ' + port_str, shell=True)
    print('>>>END')
