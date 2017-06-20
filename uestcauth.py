# 电子科技大学认证服务
# 获取session，用于其它操作
# TODO: 获取登录用户的信息

import requests
from bs4 import BeautifulSoup
from getpass import getpass
from sys import stderr
import re

class LoginError(Exception):
    def __init__(self, message):
        super().__init__(message)

class uestc(object):
    authurl = 'http://idas.uestc.edu.cn/authserver/login'
    eamsurl = 'http://eams.uestc.edu.cn/eams/home.action'

    def __init__(self, username=None, password=None):
        self._id = username
        # get cookie
        self._session = requests.Session()
        idas = self._session.get(uestc.authurl).text
        idas = BeautifulSoup(idas, 'html.parser')
        idas = idas.select('#casLoginForm')[0].find_all('input')
        post_form = {}
        for input in idas:
            post_form[input['name']] = input['value']
        post_form['username'] = username
        post_form['password'] = password
        response = self._session.post(uestc.authurl, post_form).text
        response = BeautifulSoup(response, 'html.parser')
        login_error = response.select('#msg')
        if login_error:
            raise LoginError(login_error[0].string)
        self._session.get(uestc.eamsurl)
        # will be set if self.name was used
        self._name = ''

    @property
    def cookies(self):
        return dict(self._session.cookies)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        if not self._name:
            info = self._session.get(uestc.eamsurl)
            self._name = re.search(r'>(.*)\(' + self.id + r'\)<', info.text)[1]
        return self._name

    def visit(self, url, data=None):
        if data == None:
            return self._session.get(url).text
        else:
            return self._session.post(url, data).text
   
if __name__ == '__main__':
    stderr.write('Username: ')
    username = input()
    password = getpass()
    user = uestc(username, password)
    print(user.id)
    print(user.name)

