# -*- coding: utf-8 -*-
'''
@File  : common.py
@Date  : 2019/3/15/015 12:33
'''

from configparser import ConfigParser
import decimal, json
import requests
from config.config import ENV
from utils.log import log


class MyConf(ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(MyEncoder, self).default(o)


class __Http(object):
    """
    请求封装，post,get
    """

    def __init__(self, bind="fp01"):
        env = ENV.get(bind)
        if not env:
            raise Exception("请求域名为空，bind %s在配置文件中不存在" % bind)
        self.env = env

    def get(self, path, params=None, headers=None):
        res = requests.get(self.env + path, params=params, headers=headers)
        return res

    def post(self, path, params=None, headers=None):
        res = requests.post(self.env + path, data=params, headers=headers)
        return res


def request_api(host, my_params, my_headers, request_method, bind="fp01"):
    """
    接口请求
    """
    http = __Http(bind=bind)
    if request_method == "POST":
        res = http.post(host, params=my_params, headers=my_headers)
    elif request_method == "GET":
        res = http.get(host, params=my_params, headers=my_headers)
    else:
        log.error("ERRRR:暂不支持%s这种请求方式" % request_method)
        return "ERRRR：暂不支持%s这种请求方式" % request_method
        # 如果调用创建用户或登录接口，将headers信息写入配置文件
    return res


def get_current_time():
    """
    获得当前时间
    :return: eg:2019/03/18 10:05:03
    """
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y/%m/%d %H:%M:%S")
