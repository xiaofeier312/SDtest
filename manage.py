import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, Migrate
from app.models import APIModules, APIProjects

app = create_app('default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, mod = APIModules, pro = APIProjects)

manager.add_command('shell', Shell(make_context=make_shell_context))
migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)

#
from app import app_admin
from app.admin.views import CustomModelView, projectsModelView, modulesModelView
from app.models import APIProjects, APIModules, APICases, APIDoc, TomcatEnv, CasesVerify

app_admin.add_view(projectsModelView(APIProjects, db.session, category='新增'))
app_admin.add_view(CustomModelView(TomcatEnv, db.session, category='新增'))
app_admin.add_view(modulesModelView(APIModules, db.session, category='新增'))
app_admin.add_view(CustomModelView(APIDoc, db.session, category='新增'))
app_admin.add_view(CustomModelView(APICases, db.session, category='新增'))
app_admin.add_view(CustomModelView(CasesVerify, db.session, category='新增'))


@manager.command
def init_db():
    db.create_all(bind=None)

@manager.command
def create_db():
    db.create_all(bind=None)

@manager.command
def init_data():
    p1 = APIProjects()
    p1.name = '个人中心'
    p2 = APIProjects()
    p2.name = '企业家'
    m1 = APIModules()
    m1.name = '个人中心-mobile war'
    m1.projectID = 1
    m1.remark = 'module of mobile war'
    m2 = APIModules()
    m2.name = 'portal war'
    m2.projectID = 2
    m2.remark = 'remark of protal war'
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(m1)
    db.session.add(m2)
    db.session.commit()

if __name__ == '__main__':
    manager.run()