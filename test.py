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
