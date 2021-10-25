from datetime import datetime

import requests
import requests.utils
from requests.exceptions import ConnectTimeout, ReadTimeout
from urllib3.exceptions import MaxRetryError
import time
import os
from bs4 import BeautifulSoup

from shzs_sys.settings import BASE_DIR

path = os.path.join(BASE_DIR, 'media/captcha')


def get_week(string):
    """
    获取周数
    :param string:
    :return:
    """
    s = string.replace('周', '').replace(
        ')', '').replace('(', '').split(',')
    week = []
    for item in s:
        if item.find('单') == -1 and item.find('双') == -1:
            if item.find('-') == -1:
                week.append(int(item))
            else:
                temp = item.split('-')
                for i in range(int(temp[0]), int(temp[1]) + 1):
                    week.append(i)
        elif item.find('单') == -1 and item.find('双') != -1:
            temp = item.replace('双', '').split('-')
            if int(temp[0]) % 2 == 0:
                for i in range(int(temp[0]), int(temp[1]) + 1, 2):
                    week.append(i)
            else:
                for i in range(int(temp[0]) + 1, int(temp[1]) + 1, 2):
                    week.append(i)
        elif item.find('单') != -1 and item.find('双') == -1:
            temp = item.replace('单', '').split('-')
            if int(temp[0]) % 2 == 1:
                for i in range(int(temp[0]), int(temp[1]) + 1, 2):
                    week.append(i)
            else:
                for i in range(int(temp[0]) + 1, int(temp[1]) + 1, 2):
                    week.append(i)
    return week


def date_minus(date2):
    """
    计算考试倒计时
    :param date2:
    :return:
    """
    now = datetime.strptime(time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime())[0:10], "%Y-%m-%d")
    # now = datetime.datetime.strptime('2019-01-06'[0:10], "%Y-%m-%d")
    exam_time = datetime.strptime(date2[0:10], "%Y-%m-%d")
    days = (exam_time - now).days
    if days > 0:
        return '剩余' + str(days) + '天'
    elif days < 0:
        return '已结束'
    else:
        return '今天'


class Study:
    def __init__(self, params):
        self.session = requests.Session()

        self.auth_url = 'https://xxxxx/'
        self.login_url = 'https://xxxxx/'
        self.captcha_url = 'https://xxxxx/'
        self.user_info_url = 'https://xxxxx/'
        self.jump_url = 'https://xxxxx/'
        self.timetable_url = 'https://xxxxx/'
        self.teacher_timetable = 'https://xxxxx/'
        self.grade_url = 'https://xxxxx/'
        self.detail_grade_url = 'https://xxxxx/'
        self.exam_url = 'https://xxxxx/'
        self.classroom_url = 'https://xxxxx/'
        self.teacher_info_url = 'https://xxxxx/'

        self.username = params.get('username')
        self.password = params.get('password')
        self.term = ['', '3', '12']  # 第一学期为3，第2学期为12，全部为空
        self.xnm = params.get('xnm')
        self.xqm = self.term[int(params.get('xqm')) if params.get('xqm') else 0]

        self.cookies = params.get('cookies')
        self.captcha = params.get('captcha')

        # 课表
        self.kc_list = []  # 存放课程信息

        # 成绩详情
        self.jxb_id = params.get('jxb_id')

        # 空教室
        self.this_local = params.get('this_local')
        self.this_week = params.get('this_week')
        self.this_day = params.get('this_day')
        self.jcd = params.get('jcd')

        # 教师姓名
        self.tea_name = params.get('tea_name')

        self.res = {
            '10000': {
                'code': 10000,
                'msg': '数据获取成功',
                'data': {},
            },
            '10001': {
                'code': 10001,
                'msg': '输入错误',
                'data': {},
            },
            '10002': {
                'code': 10002,
                'msg': '需要验证码',
                'data': {},
            },
            '10003': {
                'code': 10003,
                'msg': '系统维护中',
                'data': {},
            },
            '10004': {
                'code': 10004,
                'msg': '服务响应超时',
                'data': {},
            },
            '10005': {
                'code': 10005,
                'msg': '数据未找到',
                'data': {},
            }

        }
        """
        10000   正常
        10001   输入错误
        10002   需要验证码
        10003   系统维护
        10004   响应超时
        10005   未找到
        """

    def ty_login(self):
        """
        统一身份认证登录
        :return:
        """
        username = self.username
        password = self.password
        if self.cookies:
            cookies = requests.utils.cookiejar_from_dict(
                eval(self.cookies), cookiejar=None, overwrite=True)
            self.session.cookies.update(cookies)
        try:
            html = self.session.get(
                self.login_url, timeout=5).text
            soup = BeautifulSoup(html, 'html.parser')
            lt = soup.find("input", {"name": "lt"})['value']
            execution = soup.find("input", {"name": "execution"})['value']
            post_data = {
                '_eventId': 'submit',
                'execution': execution,
                'lt': lt,
                'username': username,
                'password': password,
                'rmShown': 1,
                'signIn': '',
            }
            if self.cookies:
                post_data['captchaResponse'] = self.captcha
            try:
                auth_res = self.session.post(self.auth_url, data=post_data, timeout=5).text
                soup = BeautifulSoup(auth_res, 'html.parser')
                if soup.find("div", {"class": "errors"}):
                    error = soup.find("div", {"class": "errors"}).text
                    if error == '您提供的用户名或者密码有误。':
                        self.res['10001']['msg'] = '用户名或者密码有误'
                        return self.res['10001']
                    elif error == '为了保证您的账号安全，请输入验证码' or error == '验证码错误，请重新输入':
                        img_path = os.path.join(path, username + '.png')
                        img = self.session.get(self.captcha_url).content
                        if not os.path.exists(path):
                            os.makedirs(path)
                        with open(img_path, "wb+") as f:
                            f.write(img)
                        cookies = requests.utils.dict_from_cookiejar(
                            self.session.cookies)
                        self.res['10002']['msg'] = error
                        self.res['10002']['data']['cookie'] = str(cookies)
                        return self.res['10002']
                    else:
                        self.res['10001']['msg'] = '用户名或者密码有误'
                        return self.res['10001']
                else:
                    try:
                        self.session.get(self.jump_url, timeout=5)
                    except ConnectTimeout as e:
                        return self.res['10003']
                    except MaxRetryError as e:
                        return self.res['10003']
                    except TimeoutError as e:
                        return self.res['10004']
                    except ReadTimeout as e:
                        return self.res['10004']
                    self.res['10000']['msg'] = '登陆成功'
                    return self.res['10000']
            except TimeoutError as e:
                return self.res['10004']
        except TimeoutError as e:
            return self.res['10004']

    def get_info(self):
        """
        获得用户的个人信息
        :return:
        """
        try:
            if len(self.username) < 8:
                info_res = self.session.post(self.teacher_timetable, data={
                    'xnm': '2020',
                    'xqm': '3'
                }, timeout=3).json()['jsxx']
                self.res['10000']['data']['username'] = self.username
                self.res['10000']['data']['user_name'] = info_res.get('XM')
                self.res['10000']['data']['user_college'] = info_res.get('JGMC')
                self.res['10000']['data']['user_profession'] = '暂无'
                self.res['10000']['data']['user_class'] = info_res.get('JGMC')
            else:
                info_res = self.session.post(self.user_info_url + self.username, timeout=3).json()
                self.res['10000']['data']['username'] = self.username
                self.res['10000']['data']['user_name'] = info_res.get('xm')
                self.res['10000']['data']['user_college'] = info_res.get('jg_id')
                self.res['10000']['data']['user_profession'] = info_res.get('zyh_id')
                self.res['10000']['data']['user_class'] = info_res.get('bh_id')
            self.res['10000']['msg'] = '个人信息获取成功'
            return self.res['10000']
        except TimeoutError as e:
            return self.res['10004']
        except ReadTimeout as e:
            return self.res['10004']

    def get_num(self, kcmc):
        """
        获得课程唯一id后两位，以便着色
        :param kcmc:
        :return:
        """
        if kcmc in self.kc_list:
            return self.kc_list.index(kcmc)
        else:
            self.kc_list.append(kcmc)
            return self.kc_list.index(kcmc)

    def get_course_list(self):
        """
        获取课表信息
        :return:
        """
        post_data = {
            'xnm': self.xnm,
            'xqm': self.xqm,
        }
        try:
            if len(self.username) < 8:
                response = self.session.post(self.teacher_timetable, data=post_data, timeout=3).json()
            else:
                response = self.session.post(self.timetable_url, data=post_data, timeout=3).json()
            # print(response)
            response = response['kbList']
        except TimeoutError as e:
            return self.res['10004']
        course_list = []
        color_list = [
            '#1fb49b',
            '#cf667d',
            '#139ad4',
            '#c19191',
            '#da95b7',
            '#a685c0',
            '#00bdaa',
            '#e29aad',
            '#81cc74',
            '#e29e6a',
            '#7397db',
            '#c496c9',
            '#d3695b',
            '#a1d699',
        ]
        for item in response:
            # 获得持续节数
            temp = item['jcs'].split('-')
            kc_num = self.get_num(item['kcmc'])

            course_list.append({
                'kcmc': item['kcmc'],
                'cdmc': item['cdmc'],
                'jcs': int(item['jcs'].split('-')[0]),
                'cxjs': int(temp[1]) - int(temp[0]) + 1,
                'xm': item['xm'],
                'xqj': item['xqj'],
                'zcd': get_week(item['zcd']),
                'zcdd': item['zcd'],
                'bg': color_list[kc_num % len(color_list)],
                'jgh_id': kc_num,
                'kcxz': item['kcxz'],
                'zxs': item['zxs'],
                'xf': item['xf'],
            })
        self.res['10000']['data'] = {
            'course_list': course_list,
        }
        self.res['10000']['msg'] = '课表信息获取成功'
        return self.res['10000']

    def get_grade(self):
        """
        获取成绩
        :return:
        """
        post_data = {
            'xnm': self.xnm,
            'xqm': self.xqm,
            'queryModel.showCount': 200
        }
        try:
            response = self.session.post(self.grade_url, data=post_data, timeout=3).json()['items']
        except TimeoutError as e:
            return self.res['10004']
        grade_list = []
        for item in response:
            if item.get('cj') == '旷考':
                grade_list.append({
                    'kc': item.get('kcmc'),
                    'cj': 0.00,
                    'jd': item.get('jd', 0.00),
                    'jxb_id': item.get('jxb_id'),
                    'xf': item.get('xf'),
                    'xnm': item.get('xnm'),
                    'xqm': item.get('xqm'),
                })
            else:
                grade_list.append({
                    'kc': item.get('kcmc'),
                    'cj': item.get('cj'),
                    'jd': item.get('jd', 0.00),
                    'jxb_id': item.get('jxb_id'),
                    'xf': item.get('xf'),
                    'xnm': item.get('xnm'),
                    'xqm': item.get('xqm'),
                })
        self.res['10000']['msg'] = '成绩获取成功'
        self.res['10000']['data'] = {
            'grade_list': grade_list,
        }
        return self.res['10000']

    def get_detail_grade(self):
        """
        获取详细成绩
        :return:
        """
        post_data = {
            'xnm': self.xnm,
            'xqm': self.xqm,
            'xh_id': self.username,
            'jxb_id': self.jxb_id,
            '_search': 'false',
            'nd': str(time.time()),
            'queryModel.showCount': 15,
            'queryModel.currentPage': 1
        }
        try:
            response = self.session.post(
                self.detail_grade_url + self.username, data=post_data, timeout=3).json()['items']
        except TimeoutError as e:
            return self.res['10004']
        detail_grade = []
        for item in response:
            detail_grade.append({
                'xmblmc': item['xmblmc'],
                'xmcj': item['xmcj']
            })
        self.res['10000']['msg'] = '成绩详情获取成功'
        self.res['10000']['data'] = {
            'detail_grade': detail_grade,
        }
        return self.res['10000']

    def get_exam(self):
        """
        获取考试信息
        :return:
        """
        post_data = {
            'xnm': self.xnm,
            'xqm': self.xqm,
            'queryModel.showCount': 30
        }
        try:
            response = self.session.post(
                self.exam_url + self.username, data=post_data, timeout=3).json()['items']
        except TimeoutError as e:
            return self.res['10004']
        exam_list = []
        for item in response:
            exam_list.append({
                'kcmc': item['kcmc'],
                'cdbh': item['cdbh'],
                'rday': date_minus(item['kssj']),
                'kssj': item['kssj'],
            })

        self.res['10000']['msg'] = '考试信息获取成功'
        self.res['10000']['data'] = {
            'exam_list': exam_list,
        }
        return self.res['10000']

    def get_empty_class(self):
        """
        获取空教室
        :return:
        """
        post_data = {
            'xnm': self.xnm,
            'xqm': self.xqm,
            'fwzt': 'cx',
            'xqh_id': 2,
            'lh': '博' + self.this_local,
            'jyfs': '0',
            'zcd': pow(2, int(self.this_week) - 1),
            'xqj': self.this_day,
            'jcd': self.jcd,
            '_search': 'false',
            'queryModel.showCount': 100,
            'queryModel.currentPage': 1,
            'queryModel.sortName': 'cdbh',
            'queryModel.sortOrder': 'asc',
            'time': 1
        }
        try:
            response = self.session.post(
                self.classroom_url, data=post_data).json()['items']
        except TimeoutError as e:
            return self.res['10004']
        empty_class_list = []
        for item in response:
            empty_class_list.append(item['cdbh'])
        self.res['10000']['msg'] = '空教室数据获取成功'
        self.res['10000']['data'] = {
            'empty_class_list': empty_class_list,
        }
        return self.res['10000']

    def get_teacher_tel(self):
        """
        获得教师联系方式
        :param params:
        :return:
        """
        post_data = {
            'func_widget_guid': 'DA1B5BB30E1F4CB99D1F6F526537777B',
            'gnmkdm': 'N219904',
            'su': self.username,
            'xnm': self.xnm,
            'xqm': self.xqm,
            'js': self.tea_name,
            '_search': 'false',
            'nd': str(time.time()),
            'queryModel.showCount': 100,
            'queryModel.currentPage': 1,
            'queryModel.sortName': '',
            'queryModel.sortOrder': 'asc',
        }
        try:
            response = self.session.post(self.teacher_info_url, data=post_data, timeout=3).json()[
                'items']
        except TimeoutError as e:
            return self.res['10004']

        teacher_tel_list = []
        for item in response:
            tec_info = {
                'kcmc': item['kcmc'],
                'cdmc': item.get('cdmc', '未填写'),
                'xm': item['xm'],
                'jslxdh': item.get('jslxdh', '未填写')
            }
            if tec_info not in teacher_tel_list:
                teacher_tel_list.append(tec_info)
        self.res['10000']['msg'] = '教师联系方式获取成功'
        self.res['10000']['data'] = {
            'teacher_tel_list': teacher_tel_list,
        }
        return self.res['10000']
