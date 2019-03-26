# # -*- coding: utf-8 -*-
# '''
# @File  : test.py
# @Date  : 2019/3/15/015 10:19
# '''
# from utils.log import log
#
#
# class __Result(object):
#     def __init__(self):
#         self.ispass = "pass"
#         self.reason = None
#         self.time = None
#         self.fact = None
#         self.sql_res = None
#
#     def get_ss(self):
#         return self.__dict__
#
#
# a = __Result()
# a.ispass = "fail"
# print(a.get_ss())
#
#
# def __check_point(self, points, res, result):
#     """
#     接口检查点判断
#     :param result:__Result对象
#     :return:
#     """
#     # 执行用例前，不符合用例书写规则的用例执行结果全部定位block
#     if res.get("block"):
#         result.ispass = "block"
#         res
#     try:
#         for key, value in points.items():
#             if "." not in key:
#                 if res.get(key) is None:
#                     reason = "返回结果中没有检查点字段%s" % key
#                     return self.__excute_result(
#                         ispass=FAIL,
#                         reason=reason,
#                         time=get_current_time(),
#                         fact=res
#                     )
#                 if str(res.get(key)) != str(value):
#                     reason = "检查点%s预期结果为:%s,实际结果为:%s" % (
#                         key, str(res.get(key)), value)
#                     return self.__excute_result(
#                         ispass=FAIL,
#                         reason=reason,
#                         time=get_current_time(),
#                         fact=res
#                     )
#                 return self.__excute_result(
#                     ispass=PASS,
#                     time=get_current_time(),
#                     fact=res
#                 )
#             temp_res = res
#             for point in key.split("."):
#                 temp_res = temp_res.get(point)
#                 if not isinstance(temp_res, dict):
#                     if str(temp_res) != str(value):
#                         reason = "检查点%s预期结果为:%s,实际结果为:%s" % (
#                             key, str(res.get(key)), value)
#                         return self.__excute_result(
#                             ispass=FAIL,
#                             reason=reason,
#                             time=get_current_time(),
#                             fact=res
#                         )
#                     return self.__excute_result(
#                         ispass=PASS,
#                         time=get_current_time(),
#                         fact=res
#                     )
#                 if temp_res is None:
#                     reason = "返回结果中没有检查点字段%s" % key
#                     return self.__excute_result(
#                         ispass=FAIL,
#                         reason=reason,
#                         time=get_current_time(),
#                         fact=res
#                     )
#     except JSONDecodeError as e:
#         print(e)
#         pass


import requests,re
from main import bind_key,install_certificate
from utils.sqls import ConMysql

h={"task_id":1}
# dis_p = re.compile(r"DIS4=(.*?);")
# s=requests.post("http://fp01.ops.gaoshou.me/s5/create_user")
# s_id=re.findall(dis_p, s.headers["Set-Cookie"])[-1]
# print(s_id)
# g=requests.get("http://fp01.ops.gaoshou.me//s4k/subtask.list",headers={"cookie":"7f7dbd23417541a2a639b31491ec12c1"})
# print(g.text)
# bind_key("7f7dbd23417541a2a639b31491ec12c1")
# install_certificate(sid="7f7dbd23417541a2a639b31491ec12c1",db=ConMysql("fp01"))
# a=requests.get("http://fp01.ops.gaoshou.me/s4/lite.subtask.start")
# print(a.text)
a = {'X-QK-EXTENSION': '12.2|1|1517bfd3f7ea41c4abc',
     'X-QK-AUTH': 'A624A1D7-E227-431A-8413-E50638B56C0A|000007A8-26B2-4749-AFF3-0435B6ED525E|',
     'X-QK-TOKEN': '20d2277d121c3a4fabdb86360cf117cf', 'X-QK-DIS': '35568b53766c4d36b0e0795d5e2dbf68',
     'X-QK-API-KEY': 'c26007f41f472932454ea80deabd612c', 'X-QK-SIGN': 'CF5ACB4B34625C3774302A4C1781F488',
     'X-QK-CDID': 'D2szej8SQavz6V+lQlLlhNsgn4rLJgKcXOxtWzdkI6VigXe5', 'X-QK-PUSH-STATE': '1', 'X-QK-TIME': '1553245274',
     'X-QK-APPV': 'iPhone11,6|1570.120000|com.qqsp.app|1.0.1', 'X-QK-SCHEME': 'com.qqsp.app', 'X-QK-TAG': ''}

pp = {"name": "zs", "age": 15}
from utils.cryptor_util import Crypto
import msgpack,requests
crypto=Crypto()
crypto.configure(CRYPTO_KEY = b'1514e2f07add21f4a6aba875588592a')

s='+'.join([
	'%s=%s' % (k, v) for k, v in sorted(pp.items())])


value=msgpack.dumps(pp)
plan_data=crypto.encrypt(value,iterations=10)
print(plan_data)

g=requests.post("http://172.16.2.244:5000/demo",data="ssss",json={"data":str(plan_data)})
print(g.text)
print(g.request.body)
print(type(g.request.body))



# print(g.request.values)
# print(g.text)

#
# decode_plan_data=crypto.decrypt(plan_data,iterations=10)
# decode_value=msgpack.loads(decode_plan_data,encoding="utf8")
# print(sorted(pp))
# print("value----->%s"%value)
# print("plan_data------->%s"%plan_data)
#
# print("decode_plan_data------->%s"%decode_plan_data)
# print("decode_value--------%s"%decode_value)

