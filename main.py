# -*- coding: utf-8 -*-
'''
@File  : main.py
@Date  : 2019/3/15/015 15:02
'''
from utils.handle_case import get_case, get_api
from utils.sqls import ConMysql
from config.config import *
from utils.parse_config import ParseConfig

CASETABLE = "testcase"
RESULTTABLE = "testresult"
APITABLE = "apiinfo"
pc = ParseConfig()


def get_user_info():
    uid = pc.get_info("user").get("uid")
    session = pc.get_info("user").get("session")
    return uid, session

def build_cookie(**kwargs):
    uid, session = get_user_info()
    if kwargs.get("uid"):
        uid=kwargs.get("uid")
    if kwargs.get("session"):
        session=kwargs.get("session")
    cookie="DIS4={session};ln=1;lu={uid}".format(
        uid=uid,
        session=session
    )
    return cookie


class Run(object):
    def __init__(self):
        self.db_local = ConMysql()
        self.db_server = ConMysql("fp01")
        self.cases = None
        self.api = None

    def __excute_case(self, case):
        api_host = case[APIHOST]
        api_params = case[PARMAS]
        api_method = case[METHOD]
        api_headers = case[APIHEADERS]

    def before_test(self):
        # 清除数据库信息
        self.db_local.truncate_data(APITABLE)
        self.db_local.truncate_data(CASETABLE)
        self.db_local.truncate_data(RESULTTABLE)

        self.cases = get_case()
        self.api = [get_api(case) for case in self.cases]
        # 数据库保存接口信息
        for api in self.api:
            self.db_local.insert_data(APITABLE, **api)
        # 数据库保存用例信息
        for case in self.cases:
            self.db_local.insert_data(CASETABLE, **case)

    def after_test(self):
        self.db_local.close()
        self.db_server.close()

    def begin_test(self):
        pass

    def run(self):
        pass

if __name__ == '__main__':
    s=build_cookie(uid="aaa",session="bbb")
    print(s)