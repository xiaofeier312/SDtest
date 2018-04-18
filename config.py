import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRECT_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/tushare?charset=utf8'


class TestingConfig(Config):
    TESTING = True
    #old config: #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/tushare?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/sdauto?charset=utf8'


config = {
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': TestingConfig
}
