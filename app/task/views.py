from . import task
from flask import render_template



@task.route('/index', methods=['GET'])
def task_index():

    return render_template('do_task/task.html')



@task.route('/test', methods=['GET'])
def task_test():

    return render_template('do_task/test_task.html')