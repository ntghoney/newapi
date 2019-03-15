# -*- coding: utf-8 -*-
'''
@File  : test.py
@Date  : 2019/3/15/015 10:19
'''
from utils.log import log

a="https://{host}:{port}/{route}".format(
    host="www.baidu",
    port="8080",
    route="/"
)
print(a)