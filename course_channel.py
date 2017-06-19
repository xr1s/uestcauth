import requests
from login import login
from sys import stderr
from getpass import getpass
import re

channel_list = range(2000)
open_channel = []

channel_url = 'http://eams.uestc.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id={channel}'

failregex = re.compile('失败|没有开放')

if __name__ == '__main__':
    stderr.write('Username: ')
    username = input()
    password = getpass()
    session = login(username, password)
    for chan in channel_list:
        result = session.get(channel_url.format(channel=chan)).text
        if failregex.search(result):
            print(chan, 'closed')
        else:
            open_channel.append(chan)
            print(chan, 'open')
    print(open_channel)

