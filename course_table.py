# 查询某学期课程表
# semester.id是学期的编号，在我的课表，切换学期里可以看到每学期的id
# semester.id暂时没加入自动对应功能，之后可能会加入到注释里，总之要手动

from uestcauth import uestc
from getpass import getpass
from sys import stderr
import re
from pprint import pprint

refer_url = 'http://eams.uestc.edu.cn/eams/courseTableForStd.action'
table_url = 'http://eams.uestc.edu.cn/eams/courseTableForStd!courseTable.action'

# 用来在源码中提取POST数据和课程信息的正则
ids_pattern = re.compile(r'"ids","(\d+)"')
course_pattern = re.compile(r'TaskActivity\((.*)\)([^T]*)')
info_pattern = re.compile(r'"(.*?)",?' * 7)
time_pattern = re.compile(r'index =(\d+)\*unitCount\+(\d+);')

def course_info(user, semesterid=None):
    post_form = {
        'ignoreHead': 1,
        'setting.kind': 'std',
        'startWeek': 1,
        'semester.id': semesterid,
        'ids': ids_pattern.search(user.visit(refer_url)).group(1),
    }
    courses = []
    for match in course_pattern.finditer(user.visit(table_url, post_form)):
        course = {}
        info = info_pattern.search(match[1])
        course['teacher_id'] = info.group(1)
        course['teacher_name'] = info.group(2)
        course['course_id'] = info.group(3)
        course['course_name'] = info.group(4)
        course['room_id'] = info.group(5)
        course['room_name'] = info.group(6)
        course['weeks'] = tuple(i for i, v in enumerate(info[7]) if v == '1')
        course['time'] = []
        time = time_pattern.findall(match[2])
        for weekday, clss in time:
            course['time'].append((int(weekday) + 1, int(clss) + 1))
        courses.append(course)
    return courses

if __name__ == '__main__':
    stderr.write('Username: ')
    username = input()
    password = getpass()
    user = uestc(username, password)
    # 123为2016-2017学年第1学期
    # 143为2016-2017学年第2学期
    # 163为2017-2018学年第1学期
    pprint(course_info(user, 123))

