from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from app.models import APIProjects, APIModules, APIDoc, APICases
from .services import DataChoice
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import SelectField
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from app import db
from wtforms import form, fields, validators, widgets
from flask import request


class CustomModelView(ModelView):
    """View function of Flask-Admin for Models page."""
    page_size = 10


class projectsModelView(ModelView):
    """custom view for projects"""
    can_view_details = True
    page_size = 10
    column_exclude_list = ['operator', ]
    # column_editable_list = ['name', 'remark']
    column_searchable_list = ['name']
    column_filters = ['name']
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time']  # remove fields from the create and edit forms
    # column_select_related_list = ('id','name')


class newItemAjaxModelLoader(QueryAjaxModelLoader):
    def get_list(self, term, offset=0, limit=10):
        query = self.session.query(self.model).filter_by(mid=term)
        return query.offset(offset).limit(limit).all()


class modulesModelView(ModelView):
    """custom view for modules"""
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time']
    form_columns = ('name', 'project', 'remark')
    # column_searchable_list = ('projectID',APIProjects.id)
    form_ajax_refs = {
        # 'projectID': QueryAjaxModelLoader('projectID', db.session, APIProjects, fields=['id', 'name'])
        'project': {
            'fields': [APIProjects.name],
            'page_size': 10
        }
    }
    # column_select_related_list = ('id','name')
    # form_overrides = dict(projectID=SelectField)
    # form_args = dict(
    #     projectID=dict(
    #         choices=DataChoice.get_projects()
    #         # choices=[(0, 'waiting'), (1, 'in_progress'), (2, 'finished')]
    #     )
    # )


class DocModelView(ModelView):
    """Custom APIDoc view"""
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time']
    form_columns = ('name', 'module', 'Api_priority', 'path', 'http_method', 'headers', 'body', 'remark', 'operator')
    form_ajax_refs = {
        'module': {
            'fields': [APIModules.name],
            'pagesize': 10
        }
    }
    form_choices = {
        'Api_priority':[('1','1'),('2','2'),('3','3')],
        'http_method':[('get','get'),('post','post'),('put','put')]
    }


class caseModelView(ModelView):
    """Custom API cases view"""
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time','Api_priority', 'is_https', 'http_method', 'http_response' ]
    form_columns = ('name', 'doc', 'url', 'headers', 'body', 'remark', 'operator')
    form_ajax_refs = {
        'doc': {
            'fields': [APIDoc.name],
            'pagesize': 10
        }
    }
    form_choices = {
        'Api_priority':[('1','1'),('2','2'),('3','3')],
        'http_method':[('get','get'),('post','post'),('put','put')]
    }
    column_exclude_list = ['Api_priority', 'is_https', 'http_method', 'http_response']


class verifyModelView(ModelView):
    """Custom caseVerify view"""
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time']
    form_columns = ('case','verify_path','verify_expect','verify_method','set_up','set_down','operator')
    form_ajax_refs = {
        'case':{
            'fields':[APICases.name],
            'pagesize': 10
        }
    }

class resultModelView(ModelView):
    """Custom result view"""
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time']
    form_columns = ('task_id','case','result')









