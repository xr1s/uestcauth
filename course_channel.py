# 暴力扫描开放的选课通道脚本
# 可以更改下面的channel_list来更改扫描范围
# TODO: 多线程或异步优化查询速度

import requests
from uestcauth import uestc
from sys import stderr
from getpass import getpass
import re

channel_list = range(2000)
open_channel = []

channel_url = 'http://eams.uestc.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id={channel}'

if __name__ == '__main__':
    stderr.write('Username: ')
    username = input()
    password = getpass()
    user = uestc(username, password)
    for chan in channel_list:
        result = user.visit(channel_url.format(channel=chan))
        if re.search('失败|没有开放', result):
            print(chan, 'closed')
        else:
            open_channel.append(chan)
            print(chan, 'open')
    print(open_channel)

