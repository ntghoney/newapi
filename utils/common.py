# -*- coding: utf-8 -*-
'''
@File  : common.py
@Date  : 2019/3/15/015 12:33
'''

from configparser import ConfigParser
import decimal, json
import requests, datetime
from config.config import ENV
from utils.log import log
import time
from utils.md5Helper import digest_helper
from config.config import SHARED_KEYS_MAPPING
import hashlib, random


class MyConf(ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(MyEncoder, self).default(o)


class __Http(object):
    """
    请求封装，post,get
    """

    def __init__(self, bind="fp01"):
        self.bind = bind
        env = ENV.get(self.bind)
        if not env:
            raise Exception("请求域名为空，bind %s在配置文件中不存在" % bind)
        self.env = env

    def get(self, path, params=None, headers=None):
        res = requests.get(self.env + path, params=params, headers=headers)
        return res

    def post(self, path, params=None, headers=None,data=None):
        res = requests.post(self.env + path, params=params,data=data,headers=headers)
        return res

    def get_env(self):
        return self.bind


def login(bind="fp01"):
    from json import JSONDecodeError
    import re
    dis_p = re.compile(r"DIS4=(.*?);")
    res = request_api(
        host="s5/create_user",
        my_params={},
        my_headers={},
        request_method="POST",
        bind=bind
    )
    try:
        uid = res.json()["payload"]["uid"]
        s_id = re.findall(dis_p, res.headers["Set-Cookie"])[-1]
        return {"uid": str(uid), "sid": str(s_id)}
    except (TypeError, JSONDecodeError):
        log.info("登陆失败")
        return None


def request_api(host, my_params, my_headers, request_method, bind="fp01",data=None):
    """
    接口请求
    """
    http = __Http(bind=bind)
    if request_method == "POST":
        res = http.post(host, params=my_params, data=data,headers=my_headers)
    elif request_method == "GET":
        res = http.get(host, params=my_params,headers=my_headers)
    else:
        log.error("ERRRR:暂不支持%s这种请求方式" % request_method)
        return {"error": "暂不支持%s这种请求方式" % request_method}
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


def get_token_by_idfa(idfa):
    """

    :param idfa:
    :return:
    """
    if not idfa:
        return ''

    return digest_helper.md5(idfa)


def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串
    :param randomlength: 指定长度，默认16
    :return:random_str str
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


class MakeSign(object):
    @staticmethod
    def sign(method, headers, params, rawData=None):
        """
        生成签名
            带所有X-QK-的headers
        :param method:
        :param headers:
        :param params:
        :param rawData:
        :return:
        """
        print(params)
        params = '+'.join([
            '%s=%s' % (k, v) for k, v in sorted(params.items())
        ])

        tmp_headers = headers
        # 过滤非X-QK-开头的key和排除header头签名字段X-QK-SIGN
        _headers = {k.upper(): v for k, v in tmp_headers.items()
                    if k.upper().find('X-QK-') == 0 and k.upper() != 'X-QK-SIGN'}
        # 把header参数按key排序连成字符串
        _headers = '+'.join(
            ['%s=%s' % (k, v) for k, v in sorted(_headers.items())])

        try:
            API_KEY = headers['X-QK-API-KEY']
            shared_key = SHARED_KEYS_MAPPING[API_KEY]
        except KeyError:
            # 没有对应的 API_KEY, 不签名
            return ''

        s = "{method}{params}{shared_key}{headers}".format(
            method=method,
            params=params,
            shared_key=shared_key,
            headers=_headers
        )
        print(s)
        m = hashlib.md5()
        m.update(s.encode())
        if rawData:
            m.update(rawData)
        return m.hexdigest().upper()


class KeyHeaders(object):

    def __init__(self, sid, **kwargs):
        # idfa = 'A624A1D7-E227-431A-8413-E50638B56C0A'
        # uuid = '000007A8-26B2-4749-AFF3-0435B6ED525E'
        # self._idfa = idfa
        self._sid = sid
        self._uuid = kwargs.get("uuid", '000007A8-26B2-4749-AFF3-0435B6ED525E')
        self._idfa = kwargs.get("idfa", 'A624A1D7-E227-431A-8413-E50638B56C0A')
        self._bundle_id = kwargs.get('bundle_id', 'com.qqsp.app')
        self._api_key = kwargs.get('api_key',
                                   'c26007f41f472932454ea80deabd612c')

        self._extension = kwargs.get('extension', '12.2|1|1517bfd3f7ea41c4abc')
        self._push_state = kwargs.get('push_state', "1")
        self._cdid = kwargs.get(
            'cdid', 'D2szej8SQavz6V+lQlLlhNsgn4rLJgKcXOxtWzdkI6VigXe5')

        self._device_model = kwargs.get('device_model', 'iPhone11,6')
        self._os_version = kwargs.get('os_version', '1570.120000')
        self._bundle_version = kwargs.get('bundle_version', '1.0.1')

    def build_headers(self):
        """

        :return:
        """

        headers = {}
        idfa = self._idfa
        uuid = self._uuid
        did = ''
        headers.setdefault("X-QK-AUTH", '%s|%s|%s' % (idfa, uuid, did))
        headers.setdefault("X-QK-SCHEME", self._bundle_id)

        headers.setdefault('X-QK-DIS', self._sid)
        headers.setdefault('X-QK-TIME', str(int(time.time())))

        headers.setdefault('X-QK-EXTENSION', '12.2|1|1517bfd3f7ea41c4abc')
        headers.setdefault('X-QK-PUSH-STATE', "1")

        token = get_token_by_idfa(idfa)
        headers.setdefault('X-QK-TOKEN', token)
        headers.setdefault('X-QK-TAG', '')
        headers.setdefault('X-QK-API-KEY', self._api_key)
        headers.setdefault('X-QK-APPV', '%s|%s|%s|%s' % (self._device_model,
                                                         self._os_version,
                                                         self._bundle_id,
                                                         self._bundle_version))
        headers.setdefault('X-QK-CDID', self._cdid)
        return headers

    def with_sign_headers(self, sign):
        """

        :param sign:
        :return:
        """

        headers = self.build_headers()
        headers.setdefault('X-QK-SIGN', sign)
        return headers
