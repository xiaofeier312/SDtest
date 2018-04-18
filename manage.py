import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, Migrate
from app.models import APIModules, APIProjects

app = create_app('default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))
migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)


@manager.command
def init_db():
    db.create_all(bind=None)

@manager.command
def create_db():
    db.create_all(bind=None)

if __name__ == '__main__':
    manager.run()