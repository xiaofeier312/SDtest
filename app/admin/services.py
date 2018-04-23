from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import APIProjects


class DataChoice(object):

    @staticmethod
    def get_projects():
        """return [tuple(project.id,project.name),]"""
        engine = create_engine('mysql+pymysql://alimysql:alimysql7933@47.98.133.163/sdauto?charset=utf8', echo=True)
        DBsession = sessionmaker(bind=engine)
        session = DBsession()
        pros = session.query(APIProjects).all()
        print('----pros: {}'.format(pros[0]))
        project_tuples = []  # project info as tuple saved in list
        for i in pros:
            project_tuples.append((str(i.id), i.name))
        return project_tuples

