from app import db
from sqlalchemy import text
from flask_sqlalchemy.model import declared_attr


class APIProjects(db.Model):
    """Class for projects"""
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    remark = db.Column(db.String(64), nullable=True)
    create_time = db.Column(db.TIMESTAMP(True), nullable=True, server_default=text('NOW()'))
    operator = db.Column(db.String(64), nullable=True)
    op_time = db.Column(db.TIMESTAMP(True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return '{}'.format(self.name)

        # object_module = db.relationship('APIModules', backref='project')


class APIModules(db.Model):
    """War name, e.g.  mobile-war"""
    __tablename__ = 'modules'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    remark = db.Column(db.String(64), nullable=False)
    projectID = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    create_time = db.Column(db.TIMESTAMP(True), nullable=True, server_default=text('NOW()'))
    operator = db.Column(db.String(64), nullable=True)
    op_time = db.Column(db.DateTime, nullable=True,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    project = db.relationship(APIProjects, backref='modules')

    def __repr__(self):
        # return '%r, <project_id> %r' % (self.name, self.projectID)
        return '{}'.format(self.name)

        # object_APIName = db.relationship('APIDoc', backref='modules')


class APIDoc(db.Model):
    """API doc"""
    __tablename__ = 'api_doc'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=False)
    moduleID = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    # type = db.Column(db.Integer, nullable=True)  # 0 is http, 1 is RPC
    Api_priority = db.Column(db.Integer)
    path = db.Column(db.String(512))  # only contain path, NOT contain IP,Port
    is_https = db.Column(db.Integer, nullable=True, default=0)
    http_method = db.Column(db.String(16), nullable=False)  # get, post, put
    headers = db.Column(db.Text, nullable=True, default='Content-Type:application/json;charset=utf-8')
    body = db.Column(db.Text, nullable=True)
    remark = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.TIMESTAMP(True), nullable=True, server_default=text('NOW()'))
    operator = db.Column(db.String(64), nullable=True)
    op_time = db.Column(db.DateTime, nullable=True,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    module = db.relationship(APIModules, backref='APIDoc')

    def __repr__(self):
        return '{}'.format(self.name)

        # object_APICases = db.relationship('APICases', backref='API_name')


class APICases(db.Model):
    """http_method: 1 get//2 post//3 del//4 put...
     ..Change http_method to string field for using requests module easily"""
    __tablename__ = 'api_cases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True, default='interface test')
    APINameID = db.Column(db.Integer, db.ForeignKey('api_doc.id'), nullable=False)
    url = db.Column(db.String(512), nullable=True)
    Api_priority = db.Column(db.Integer)
    is_https = db.Column(db.Integer, nullable=True, default=0)
    http_method = db.Column(db.String(16), nullable=True)
    headers = db.Column(db.Text, nullable=True, default='Content-Type:application/json;charset=utf-8')
    body = db.Column(db.Text)
    remark = db.Column(db.Text, nullable=True)
    http_response = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.TIMESTAMP(True), nullable=True, server_default=text('NOW()'))
    operator = db.Column(db.String(64), nullable=True)
    op_time = db.Column(db.DateTime, nullable=True,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    doc = db.relationship(APIDoc, backref='APICase')

    def __repr__(self):
        return '{}'.format(self.name)


class CasesVerify(db.Model):
    """verify parts, containing json data(according to json path) verify,\
     mysql script verify, and operation//// """
    __tablename__ = 'case_verify'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('api_cases.id'), nullable=False)
    # verify_path is the data(to be verify)'s path in result json
    verify_path = db.Column(db.String(128))
    # verify_expect is the expect value
    verify_expect = db.Column(db.String(512))
    # verify_method 'connect/compare' the result and expect value, e.g:Equal, not Equal
    verify_method = db.Column(db.String(128))
    set_up = db.Column(db.String(256))
    set_down = db.Column(db.String(256))
    create_time = db.Column(db.TIMESTAMP(True), nullable=True, server_default=text('NOW()'))
    operator = db.Column(db.String(64), nullable=True)
    op_time = db.Column(db.DateTime, nullable=True,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    case = db.relationship(APICases, backref='verify')


class CasesResult(db.Model):
    __tablename__ = 'cases_result'
    id = db.Column(db.INTEGER, primary_key=True)
    task_id = db.Column(db.INTEGER)
    case_id = db.Column(db.INTEGER, db.ForeignKey('api_cases.id'), nullable=False)
    result = db.Column(db.Text)  # may be save batch results
    create_time = db.Column(db.TIMESTAMP(True), nullable=True, server_default=text('NOW()'))
    operator = db.Column(db.String(64), nullable=True)
    op_time = db.Column(db.DateTime, nullable=True,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    case = db.relationship(APICases, backref='result')


class TaskStatus(db.Model):
    """flag is a task complete, 1 is complte run, 0 is running
    -1 is wrong, maybe need -2 not start?
    After run case, case runner should set status to 1"""
    __tablename__ = 'task_status'
    id = db.Column(db.INTEGER, primary_key=True)
    task_id = db.Column(db.INTEGER)
    status = db.Column(db.Integer)
    create_time = db.Column(db.TIMESTAMP(True), nullable=True, server_default=text('NOW()'))
    operator = db.Column(db.String(64), nullable=True)
    op_time = db.Column(db.DateTime, nullable=True,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class TomcatEnv(db.Model):
    """tomcat IP+ port, not contact with project or module"""
    __tablename__ = 'tomcat_env'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(256), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    tomcatName = db.Column(db.String(64), nullable=True)
    remark = db.Column(db.String(64), nullable=True)
    create_time = db.Column(db.TIMESTAMP(True), nullable=True, server_default=text('NOW()'))
    operator = db.Column(db.String(64), nullable=True)
    op_time = db.Column(db.DateTime, nullable=True,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return '{}'.format(self.ip)


class ParameterData(db.Model):
    """Case parameters saved in here"""
    __tablename__ = 'parameter_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    dataList = db.Column(db.Text)
    remark = db.Column(db.String(64), nullable=True)
    create_time = db.Column(db.TIMESTAMP(True), nullable=True, server_default=text('NOW()'))
    operator = db.Column(db.String(64), nullable=True)
    op_time = db.Column(db.DateTime, nullable=True,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return 'ID:{}_name: {}'.format(self.id, self.name)


class ReplaceInfo(db.Model):
    """replace json path value with parameter"""
    __talbename__ = 'replace_info'
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(128), nullable=False) # this data didn't need name for simply using.
    json_path = db.Column(db.String(256), nullable=False)  # e.g. $.userId
    replace_key = db.Column(db.String(64), nullable=False)  # e.g. data
    remark = db.Column(db.String(64), nullable=True)
    create_time = db.Column(db.TIMESTAMP(True), nullable=True, server_default=text('NOW()'))
    operator = db.Column(db.String(64), nullable=True)
    op_time = db.Column(db.DateTime, nullable=True,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return 'ID:{}_Json path:{}_replace key:_{}'.format(self.id, self.json_path, self.replace_key)


class RunCase(db.Model):
    __tablename__ = 'run_case'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=True)
    case_id = db.Column(db.Integer, db.ForeignKey('api_cases.id'), nullable=False)

    old_env_id = db.Column(db.Integer, db.ForeignKey('tomcat_env.id'), nullable=False)
    old_ = db.relationship(TomcatEnv,
                           primaryjoin='TomcatEnv.id==RunCase.old_env_id')  # , backref=backref('oldCreater',cascade='all,delete-orphan'))

    new_env_id = db.Column(db.Integer, db.ForeignKey('tomcat_env.id'), nullable=False)
    new_ = db.relationship(TomcatEnv, primaryjoin='TomcatEnv.id==RunCase.new_env_id')

    replace_id = db.Column(db.Integer, db.ForeignKey('replace_info.id'), nullable=False)
    paramter_list_id = db.Column(db.Integer, db.ForeignKey('parameter_data.id'), nullable=False)
    result_file = db.Column(db.String(128), nullable=True)
    replace = db.relationship(ReplaceInfo, backref='runcase')
    paramter_list = db.relationship(ParameterData, backref='runcase')
    create_time = db.Column(db.TIMESTAMP(True), nullable=True, server_default=text('NOW()'))
    operator = db.Column(db.String(64), nullable=True)

    case = db.relationship(APICases, backref='runCase')



class BlueprintTask(db.Model):
    """
    models for blueprint project
    """
    __tablename = 'blueprint_task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=True)
    content = db.Column(db.String(256), nullable=True)  # task deatils
    high_level = db.Column(db.SmallInteger, nullable=True)  # 0 is most important
    is_complete = db.Column(db.Boolean, nullable=True, default=False)
    is_cancelled = db.Column(db.Boolean, nullable=True, default=False)
    delay_days = db.Column(db.SmallInteger, default=0)
    user_id = db.Column(db.Integer, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.SmallInteger, nullable=False)
    create_time = db.Column(db.TIMESTAMP(True), nullable=True, server_default=text('NOW()'))
    operator = db.Column(db.String(64), nullable=True)


class BlueprintSubtask(db.Model):
    __tablename__ = 'blueprint_subtask'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    sub_content = db.Column(db.String(256), nullable=True)  # task deatils
    # high_level = db.Column(db.SmallInteger,nulable=True) # 0 is most important
    main_task = db.Column(db.Integer)  # db.ForeignKey('blueprint_task.id')
    task_order = db.Column(db.SmallInteger, nullable=True)
    is_complete = db.Column(db.Boolean, nullable=True, default=False)
    is_cancelled = db.Column(db.Boolean, nullable=True, default=False)
    delay_days = db.Column(db.SmallInteger, default=0)
    create_time = db.Column(db.TIMESTAMP(True), nullable=True, server_default=text('NOW()'))
    operator = db.Column(db.String(64), nullable=True)
