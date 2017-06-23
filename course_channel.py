# 暴力扫描开放的选课通道脚本
# 可以更改下面的channel_list来更改扫描范围
# TODO: 多线程或异步优化查询速度

import requests
from uestcauth import uestc
from sys import stderr
from getpass import getpass

channel_list = range(2000)
open_channel = []

channel_url = 'http://eams.uestc.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id={channel}'

def valid_channel(chan):
    response = user.visit(channel_url.format(channel=chan))
    if response.find('当前用户存在重复登录的情况，已将之前的登录踢出：') != -1:
        return
    if response.find('本次会话已经被过期（可能是由于重复登录）') != -1:
        return
    if response.find('没有开放的选课轮次') != -1:
        return 'invalid'
    if response.find('不在选课时间内') != -1:
        return 'closed'
    return 'open'

if __name__ == '__main__':
    stderr.write('Username: ')
    username = input()
    password = getpass()
    user = uestc(username, password)
    for chan in channel_list:
        try:
            status = ''
            while not status:
                status = valid_channel(chan)
                if not status:
                    print(chan, 'kicked out, retry...')
        except KeyboardInterrupt:
            print('keyboard interrupted, exit')
            break
        print(chan, status)
    print(open_channel)

