from . import task
from flask import render_template
from .services import Task


@task.route('/index', methods=['GET'])
def task_index():
    task = Task()
    cal_result = task.get_calendar_task()
    return render_template('do_task/task.html', cal=cal_result)



@task.route('/test', methods=['GET'])
def task_test():
    task=Task()
    cal_result=task.get_calendar()
    return render_template('do_task/test_task.html',cal=cal_result)
