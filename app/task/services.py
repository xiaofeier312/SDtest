import datetime
from app.models import db
from app.models import BlueprintSubtask, BlueprintTask
import calendar
from copy import deepcopy


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
        now_weekday = datetime.datetime.now().weekday()
        return [now_year, now_month, now_day,now_weekday, now_time]

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
            sub_task = BlueprintSubtask.query.filter_by(main_task_id=main_task_ref_id).first()
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
                days_order = datetime.timedelta(days=i)
                sub_task.work_day = main_task.start_date +days_order
                db.session.add(sub_task)
                db.session.commit()
            return {"rs": 0, "desc": "completes"}

    def get_year_month(self):
        """
        Return all month in 2017 and 2018
        :return:
        """
        month = [x for x in range(1,13)]
        all_month = []

    def get_day_list_by_month(self,year,month):
        """
        Get all days in one month.
        :param year:
        :param month:
        :return:
        """
        days_in_month = calendar.monthrange(year,month)
        return days_in_month

    def get_tasks_by_month(self,year,month):
        pass


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

    def get_calendar(self):
        month_list = list(range(1, 13))
        month_max = calendar.mdays[1:13]
        print('month_max is: {}'.format(month_max))
        cal = {2018: month_list, 2019: month_list}
        cal_result = {2018: {}, 2019: {}}

        for year in cal.keys():
            for month in cal[year]:
                print(month)
                cal_result[year][month] = list(range(1, month_max[month - 1] + 1))
        return cal_result

    def get_calendar_task(self):
        all_subtasks = self.get_sub_task()
        cal = self.get_calendar()
        cal_task = deepcopy(cal)
        for year in cal.keys():
            for month in cal[year]:
                cal_task[year][month] = {}
                for day in cal[year][month]:
                    cal_task[year][month][day] = [None, None, None]
                    for subtask in all_subtasks:
                        dic_date = datetime.date(year,month,day)
                        if dic_date == subtask.work_day:
                            print('Match work date {}_{}_{}'.format(year,month,day))
                            cal_task[year][month][day]=[subtask.name,subtask.work_day,subtask.is_complete]
        return cal_task


    def get_task_by_day(self, day):
        """
        e.g. day is 2018-02-03
        :param day:
        :return:
        """
        subtasks = BlueprintSubtask.query.filter_by(work_day=day).all()


if __name__ == '__main__':
    t = Task()
    print(t.get_time())
    print(t.get_all_main_tasks())
