from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from app.models import APIProjects
from .services import DataChoice
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import SelectField


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


class modulesModelView(ModelView):
    """custom view for modules"""
    form_excluded_columns = ['create_time', 'op_time']
    form_overrides = dict(projectID=SelectField)
    form_args = dict(
        projectID=dict(
            choices=DataChoice.get_projects()
            # choices=[(0, 'waiting'), (1, 'in_progress'), (2, 'finished')]
        )
    )
