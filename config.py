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
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://alimysql:alimysql7933@47.98.133.163/sdauto?charset=utf8'
    SQLALCHEMY_BINDS = {
        # 'mock_data': 'mysql+pymysql://root:adadad1@127.0.0.1:3306/mock?charset=utf8',
        # 'mysql_117.226': 'mysql+pymysql://ent_all:ent@172.16.117.226:3306/ent_portal?charset=utf8'
    }
    SQLALCHEMY_ECHO = True # set sql echo = true


class TestingConfig(Config):
    DEBUG = True
    # old config:
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/tushare?charset=utf8'
    # mac mysql
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:adadad1@localhost/sdauto?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://alimysql:alimysql7933@47.98.133.163/sdauto?charset=utf8'
    SQLALCHEMY_BINDS = {
        # 'mock_data': 'mysql+pymysql://root:adadad1@127.0.0.1:3306/mock?charset=utf8',
        # 'mysql_117.226': 'mysql+pymysql://ent_all:ent@172.16.117.226:3306/ent_portal?charset=utf8'
    }
    SQLALCHEMY_ECHO = True # set sql echo = true



config = {
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': TestingConfig
}

class NormalConfig(Config):
    """
    1. set variable 'sdauto_env' in linux//sdauto_env=testing//declare -x sdauto
    2. call this class
    """
    server_http_ip = 'http://47.98.133.163/'
    # server_ip = '47.98.133.163'
    local_ip = 'http://127.0.0.1:5000/'

    def get_current_env(self):
        env_list = os.environ
        if 'sdauto_env' in env_list:
            env = env_list['sdauto_env']
        else:
            env = 'default'
        print('-- Get env is: {}'.format(env))
        return env

    def get_current_ip(self):
        env = self.get_current_env()
        if env == 'default':
            return self.local_ip
        else:
            return self.server_http_ip