import datetime
from app.models import db
from app.models import BlueprintSubtask,BlueprintTask

class Task(object):
    """
    Task
    """
    @staticmethod
    def get_time():
        """
        get current time
        :return: [now_year, now_month, now_day, now_time]
        """
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        now_month = datetime.datetime.now().month
        now_year = datetime.datetime.now().year
        now_day = datetime.datetime.now().day
        return [now_year, now_month, now_day, now_time]

    def get_all_main_task(self):
        """
        Get all tasks, return which is current one
        :return:
        """
        main_tasks = BlueprintTask.query.all()
        return main_tasks

    def get_sub_task(self, main_task_ref_id ):
        """
        Get sub task by main task
        :param main_task_id:
        :return:
        """
        if main_task_ref_id:
            sub_task = BlueprintSubtask.query.filter_by(main_task_id=main_task_ref_id)
        else:
            sub_task = BlueprintSubtask.query.all()
        return sub_task









if __name__ == '__main__':
    t=Task()
    print(t.get_time())
    print(t.get_all_main_task())
