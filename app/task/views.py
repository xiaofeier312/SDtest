from . import task
from flask import render_template
from .services import Task
import json


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

@task.route('/divide_task/<main_task_Id>', methods=['GET','POST'])
def divide_task(main_task_Id):
    t=Task()
    cal_result = t.get_calendar_task()

    result = t.divide_task(main_task_id=main_task_Id)
    print("----{}".format(result))
    return result
    #return render_template('do_task/task.html', cal=cal_result)

@task.route('/complete_sub_task/<subtask_id>')
def complete_subtask(subtask_id):
    t=Task()
    t.sub_task_complete(subtask_id)
    dic = {'r':1,'desc':'complete'}
    return json.dumps(dic)