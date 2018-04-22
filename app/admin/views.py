from flask_admin.contrib.sqla import ModelView


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
    form_excluded_columns = ['create_time', 'op_time'] # remove fields from the create and edit forms


class modulesModelView(ModelView):
    """custom view for modules"""
    can_view_details = True
    page_size = 10
    # column_exclude_list = ['operator', ]
    # column_editable_list = ['name', 'remark']
    column_searchable_list = ['name']
    column_filters = ['name']
    create_modal = True
    edit_modal = True
    form_choices = {
        'projectID': [
            ('1','project1'),
            ('2', 'project2'),

        ]
    }
    form_excluded_columns = ['create_time', 'op_time']

