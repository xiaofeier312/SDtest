import datetime


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

    def get_all_task(self):
        """
        Get all tasks, return which is current one
        :return:
        """










if __name__ == '__main__':
    t=Task()
    print(t.get_time())
