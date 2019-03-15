# -*- coding: utf-8 -*-
'''
@File  : sql.py
@Date  : 2019/3/15/015 15:23
'''
from config.config import SQLINFO


class SqlCon(object):
    def __init__(self):
        pass

    def get_bind(self, bind="local"):
        return SQLINFO.get(bind, "")

    def get_con(self,bind):
        bind=self.get_bind(bind)
