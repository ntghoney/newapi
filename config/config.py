# -*- coding: utf-8 -*-
'''
@File  : config.py
@Date  : 2019/3/15/015 10:08
'''
import os
from qianka_cache import QKCache

CONFIGPATH = os.path.abspath(os.path.dirname(__file__))  # 配置文件路径
PRODIR = os.path.abspath(os.path.join(CONFIGPATH, "../"))  # 项目路径

# 用例数据键名
CASENAME = ["caseId", "apiId", "caseDescribe", "apiHost", "testData", "apiParams", "apiHeaders", "method", "relatedApi",
            "relatedParams", "expect", "sqlStatement", "databaseExpect", "isExcute"]

PARAMETERIZE = "parameterize"
CASEID = "caseId"
APIID = "apiId"
CASEDESCRIBE = "caseDescribe"
APIHOST = "apiHost"
PARMAS = "apiParams"
TESTDATA = "testData"
METHOD = "method"
APIHEADERS = "apiHeaders"
HEADERS = "headers"
RELATEDAPI = "relatedApi"
RELEATEDPARAMS = "relatedParams"
FACT = "fact"
EXPECT = "expect"
SQLSTATEMENT = "sqlStatement"
DATABASERESUTL = "databaseResult"
DATABASEEXPECT = "databaseExpect"
ISPASS = "ispass"
TIME = "time"
FORMORT = "%Y/%m/%d %H:%M:%S"

PASS = "pass"
FAIL = "fail"
BLOCK = "block"
REASON = "reason"
# 数据库配置信息
SQLINFO = {
    "local": {
        "host": "fp01.ops.gaoshou.me",
        "port": 3307,
        "user": "root",
        "password": "",
        "database": "api_test1"
    },
    "fp01":{
        "host": "fp01.ops.gaoshou.me",
        "port": 3307,
        "user": "root",
        "password": "",
        "database": "zhuanqian"
    }
}

CRYPTO_KEY = b'1514e2f07add21f4a6aba875588592a'

# 邮件配置信息
EMAIL = {
    "server":"smtp.exmail.qq.com",
    "port":465,
    "user":"ning.tonggang@qianka.com",
    "pwd":"Ntg.123",
    "msgfrom":"宁同刚",
    "subject":"接口自动化测试报告"
}

# 邮件接受人邮箱
# RECEIVERS = ["ning.tonggang@qianka.com","ge.yuan@qianka.com","wu.zhishan@qianka.com","pei.qingling@qianka.com"]
RECEIVERS = ["ning.tonggang@qianka.com"]

REPORT={
    "ncols":12,
    "title":"接口自动化测试报告",
    "colname":"用例编号,用例名称,接口路径,请求方法,接口参数,预期结果,实际结果,sql查询结果,sql期望,测试判定,测试时间,失败原因"
}

ENV={
    "fp01":"http://fp01.ops.gaoshou.me/",
    "fp02":"http://fp03.ops.gaoshou.me/",
    "fp03":"http://fp03.ops.gaoshou.me/",
    "test":"https://www.baidu.com/"
}

SHARED_KEYS_MAPPING = {
    'c26007f41f472932454ea80deabd612c': 'aa005ddfcdfed328878fb81e76cc2969',
    '16b9b1a405fd772ba74549d8b53c3454': 'df240a556341ba71b277e1b298c384e3'
}

"""
缓存配置
"""
cache = QKCache()
cache.configure({
    "CACHE_ENABLED":True,
    "CACHE_KEY_PREFIX" :'hera:',
    "CACHE_NODES":{
          'session':('redis',['redis://fp01.ops.gaoshou.me:6380/0'])
          # with weight
        }
})

"""
Session UDID UserID相关
"""
SESSION_CACHE_KEY = 'sid:info:%s'  # SessionID , 保存当前 SessionID 下的 UDID ，UserID
SESSION_UID_CACHE_KEY = 'user:sid:%s'  # UserID , 保存当前用户所使用的 SessionID
IDFA_SESSION_CACHE_KEY = 'idfa:session:%s'  # DIFA对应的最后session id
UID_UDID_CACHE_KEY = 'user:udid:%s'  # UserID , 保存用户的 UDID

USER_LAST_IDFA_KEY = 'user_last_idfa:%s'  # UserID 保存用户最后一个idfa

# 标识执行了SDK的任务可以完成
KEY_SDK_IDFA_BUNDLEID = 'sdk_idfa_bundleid:%s:%s'