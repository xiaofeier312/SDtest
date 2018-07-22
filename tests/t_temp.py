from jsonpath_rw import Fields, jsonpath, parse,Root
import calendar
from copy import deepcopy

d1={'foo': [{'baz': 1}, {'baz': 2}]}
jsp = parse("$.foo[0].baz")
r1=jsp.find(d1)
#r2 = Fields(jsp).update(d1,33)


jsp2 = parse("$..baz")
r2=jsp2.find(d1)

#print(r2.value)


def get_calendar():
    month_list = list(range(1, 13))
    month_max = calendar.mdays[1:13]
    print('month_max is: {}'.format(month_max))
    cal = {2018: month_list, 2019: month_list}
    cal_result = {2018:{},2019:{}}

    for year in cal.keys():
        for month in cal[year]:
            print(month)
            cal_result[year][month] = list(range(1, month_max[month-1]+1))
    return cal_result

if __name__ == '__main__':
    print('r1 : {}'.format(r1))
    #Root.update(jsp)
    r1=get_calendar()
    for i in r1:
        for j in r1[i]:
            print(r1[i][j])