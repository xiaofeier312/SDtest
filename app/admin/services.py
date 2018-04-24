from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import APIProjects, APIModules


class DataChoice(object):
    """give (ID, name) to the web page, for user can select name not ID where he creating project or others"""
    engine = create_engine('mysql+pymysql://alimysql:alimysql7933@47.98.133.163/sdauto?charset=utf8', echo=True)
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    @staticmethod
    def get_projects():
        """return [tuple(project.id,project.name),]"""
        pros = DataChoice.session.query(APIProjects).all()
        print('----pros: {}'.format(pros[0]))
        project_tuples = []  # project info as tuple saved in list
        for i in pros:
            project_tuples.append((str(i.id), i.name))
        return project_tuples

    @staticmethod
    def get_modules():
        """return [tuple(moduleID,moduleName),]"""
        mods = DataChoice.session.query(APIModules).all()
        mods_tuple = []
        for i in mods:
            mods_tuple.append((str(i.id), i.name))
        return mods_tuple

    @staticmethod
    def clear_db_session():
        print('@Clear db.session')
        DataChoice.session._flush() # flush()s