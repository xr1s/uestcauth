# 暴力扫描开放的选课通道脚本
# 可以更改下面的channel_list来更改扫描范围

import requests
from uestcauth import uestc
from sys import stderr
from getpass import getpass
import asyncio

channel_list = range(2000)
open_channel = []

channel_url = 'http://eams.uestc.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id={channel}'

async def get_channel_status(user, chan):
    response = user.visit(channel_url.format(channel=chan))
    if response.find('当前用户存在重复登录的情况，已将之前的登录踢出：') != -1:
        return 'retry'
    if response.find('本次会话已经被过期（可能是由于重复登录）') != -1:
        return 'retry'
    if response.find('没有开放的选课轮次') != -1:
        return 'invalid'
    if response.find('不在选课时间内') != -1:
        return 'closed'
    return 'open'

async def check_channel(user, chan):
    status = await get_channel_status(user, chan)
    print(chan, status)
    while status == 'retry':
        status = await get_channel_status(user, chan)
        print(chan, status)
    if status == 'open':
        open_channel.append(chan)

async def main():
    stderr.write('Username: ')
    username = input()
    password = getpass()
    user = uestc(username, password)
    tasks = [check_channel(user, chan) for chan in channel_list]
    await asyncio.wait(tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    print(open_channel)

