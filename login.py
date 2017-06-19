import requests
from bs4 import BeautifulSoup
from getpass import getpass
from sys import stderr

authurl = 'http://idas.uestc.edu.cn/authserver/login'

class LoginError(Exception):
    def __init__(self, message):
        super().__init__(message)

def login(username=None, password=None):
    session = requests.Session()
    idas = session.get(authurl).text
    idas = BeautifulSoup(idas, 'html.parser')
    idas = idas.select('#casLoginForm')[0].find_all('input')
    post_form = {}
    for input in idas:
        post_form[input['name']] = input['value']
    post_form['username'] = username
    post_form['password'] = password
    response = session.post(authurl, post_form).text
    response = BeautifulSoup(response, 'html.parser')
    login_error = response.select('#msg')
    if login_error:
        raise LoginError(login_error[0].string)
    return session

if __name__ == '__main__':
    stderr.write('Username: ')
    username = input()
    password = getpass()
    login(username, password)

