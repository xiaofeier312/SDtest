import datetime
from app.models import db
from app.models import BlueprintSubtask, BlueprintTask


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

    def get_all_main_tasks(self):
        """
        Get all tasks, return which is current one
        :return:
        """
        main_tasks = BlueprintTask.query.all()
        return main_tasks

    def get_single_task(self, main_task_id):
        single_task = BlueprintTask.query.filter_by(id=main_task_id).first()
        return single_task

    def get_sub_task(self, main_task_ref_id=None):
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

    def divide_task(self, main_task_id):
        """
        Divide main task to sub task by days - create sub tasks.
        :param main_task_id:
        :return:
        """
        main_task = self.get_single_task(main_task_id)
        if main_task.is_divided or (main_task.total_days <= 1):
            return {"rs": 0, "desc": "No need to divied"}
        else:
            for i in range(0, main_task.total_days):
                sub_task = BlueprintSubtask()
                sub_task.name = main_task.name + '_day_' + str(i + 1)
                db.session.add(sub_task)
                db.session.commit()
            return {"rs": 0, "desc": "completes"}

    def main_task_complete(self,main_task_id):
        task = BlueprintTask.query.filter_by(id=main_task_id).first()
        task.is_complete = True
        db.session.add(task)
        db.session.commit()

    def sub_task_complete(self,subtask_id):
        subtask = BlueprintSubtask.query.filter_by(id=subtask_id).first()
        subtask.is_complete = True
        db.session.add(subtask)
        db.session.commit()


if __name__ == '__main__':
    t = Task()
    print(t.get_time())
    print(t.get_all_main_tasks())
