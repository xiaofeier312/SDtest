import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, Migrate
from app.models import APIModules, APIProjects, BlueprintTask, BlueprintSubtask
import datetime


app = create_app('default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, mod = APIModules, pro = APIProjects)

manager.add_command('shell', Shell(make_context=make_shell_context))
migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)


@manager.command
def init_db():
    db.create_all(bind=None)

@manager.command
def create_db():
    db.create_all(bind=None)

@manager.command
def init_data():
    # p1 = APIProjects()
    # p1.name = '个人2'
    # p2 = APIProjects()
    # p2.name = '企业2'
    # m1 = APIModules()
    # m1.name = '个人中心-mobile w2'
    # m1.projectID = 1
    # m1.remark = 'module of mobile '
    # m2 = APIModules()
    # m2.name = 'portal war2'
    # m2.projectID = 2
    # m2.remark = 'remark of protal war'

    mtask1 = BlueprintTask()
    mtask1.name = '学习任务1'
    mtask1.start_date = datetime.datetime.now().date().strftime('%Y-%m-%d')
    mtask1.total_days = 3
    subtask1 = BlueprintSubtask()
    subtask1.name= 'Spring'
    subtask1.main_task_id = 1
    subtask1.task_order = 1
    subtask1.work_day = '2018-06-11'
    # db.session.add(p1)
    # db.session.add(p2)
    # db.session.add(m1)
    # db.session.add(m2)
    db.session.add(mtask1)
    db.session.commit()
    db.session.add(subtask1)
    db.session.commit()

@manager.command
def test():
    """Run unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    # Serving HTTP on 0.0.0.0 port 8091 (http://0.0.0.0:8091/) ...
    # ^^ text main ftp server work with port 8091
    print('-------------Running-------------')
    manager.run()