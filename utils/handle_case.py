# -*- coding: utf-8 -*-
'''
@File  : handle_case.py
@Date  : 2019/3/15/015 10:41
处理用例格式
'''
# -*- coding: utf-8 -*-
'''
@File  : handleCase.py
@Date  : 2019/1/15/015 18:24
'''
from utils.parse_excel import ParseExcel
from utils.log import log
import re, json
from config.config import *


def get_case_path():
    """
    用例路径，以case_开头的.xlsx文件
    :return:
    """
    path = os.path.abspath(os.path.join(PRODIR, "cases"))
    rep = re.compile(r"^case_")
    dir_name = os.listdir(path)
    case_path = []
    for file in dir_name:
        extension = os.path.splitext(file)[1]  # 文件拓展名
        file_name = os.path.splitext(file)[0]  # 文件名
        if extension == ".xlsx" and re.findall(rep, file_name):
            case_path.append(os.path.join(path, file))
    if not case_path:
        raise Exception("无符合规则的用例")
    return case_path


class __HandleCase(object):
    def __init__(self, case_path):
        # 实例parseExc对象
        self.pe = ParseExcel(case_path, 0)

    # 总用例数
    def get_totals(self):
        return self.pe.get_all_for_row() - 1

    def __handle_checkpoint(self, item):
        """
        处理检查点数据格式
        :param item:
        :return:
        """
        checkPints = {}
        if "\n" in item:
            point = item.split("\n")
            for i in point:
                if "=" in i:
                    key, value = i.split("=", 1)
                    if ":" in value:
                        value = value.replace(":", "：")
                    checkPints[key] = value
        else:
            key, value = item.split("=",1)
            if "=" in item:
                key, value = item.split("=",1)
                if ":" in value:
                    value = value.replace(":", "：")
            checkPints[key] = value
        return checkPints

    def __handle_sql_expect(self, sql_point):
        points = self.__handle_sql_point(sql_point)
        rv = dict()
        for key, value in points.items():
            value_dic = dict()
            if "," in value:
                value = value.split(",")
                a = [t.split("=") for t in value]
                for i in a:
                    value_dic[i[0]] = i[1]
                rv[key] = value_dic
                continue
            a = value.split("=")
            value_dic[a[0]] = a[1]
            rv[key] = value_dic
        return rv

    def __handle_sql_point(self, sqls):
        """
        处理用例sql语句和sql检查点格式
        :param sqls:
        :return:
        """
        sqlstate = dict()
        if "\n" in sqls:
            sqls = str(sqls).split("\n")
            for i in sqls:
                if ":" in i:
                    key, value = str(i).split(":")
                elif "：" in i:
                    key, value = str(i).split("：")
                else:
                    continue
                sqlstate[key] = value
        else:
            key = ""
            value = ""
            if ":" in sqls:
                key, value = str(sqls).split(":")
            if "：" in sqls:
                key, value = str(sqls).split("：")
            if key and value:
                sqlstate[key] = value
        return sqlstate

    def __handle_related_params(self, params):
        """
        处理关联参数格式
        :param params:
        :return:
        """
        return params.replace("\n", ",")

    def get_excute_cases(self, cases):
        """
        获取执行的用例
        :return:
        """
        excute_case = [case for case in cases
                       if case["isExcute"] != "y"
                       or case["isExcute"] == "Y"
                       or case["isExcute"] == ""]
        return excute_case

    def get_cases(self):
        """
        获取所有用例，包括不执行的
        :return:
        """
        row_values = self.pe.get_all_for_row()[1:]

        # 用例按列名转换为字典,所有用例
        all_case = [dict(zip(CASENAME, row)) for row in row_values]
        for case in all_case:
            for k, v in case.items():
                if (k == CASEID or k == APIID or k == RELATEDAPI) and not isinstance(v, str):
                    case[k] = int(v)
                if k == RELATEDAPI and isinstance(v,str):
                    v = v.replace("\n", "")
                if not v:
                    case[k] = None
                    continue
                if k == PARMAS:
                    try:
                        case[k] = json.loads(v, encoding="utf8")
                    except Exception as e:
                        log.info(e)
                        case[k] = {}
                        log.info("参数不符合json格式")
                if k == METHOD:
                    case[k] = v.upper()
                if k == RELATEDAPI and isinstance(v, str):
                    try:
                        v = json.loads(v, encoding="utf8")
                        case[k] = v
                    except json.JSONDecodeError as e:
                        case[k] = v
                if k == EXPECT:
                    v = self.__handle_checkpoint(v)
                    case[k] = v
                if k == DATABASEEXPECT:
                    v = self.__handle_sql_expect(v)
                    case[k] = v
                if k == SQLSTATEMENT or k == TESTDATA or k == APIHEADERS:
                    v = self.__handle_sql_point(v)
                    case[k] = v
                if k == RELEATEDPARAMS:
                    v = self.__handle_related_params(v)
                    case[k] = v
        return all_case


__case_path = get_case_path()


def get_case():
    cases = []
    for i in get_case_path():
        hc = __HandleCase(i)
        cases.extend(hc.get_cases())
    return cases


def get_excute_case(cases):
    # 测试执行的用例
    excute_cases = [case for case in cases if
                    case["isExcute"] == "y" or
                    case["isExcute"] == "Y" or
                    case["isExcute"] == ""]
    for case in excute_cases:
        case.pop("isExcute")
    return excute_cases


def get_api(case):
    api_info = dict()
    api_info.setdefault(APIID, case[APIID])
    api_info.setdefault(APIHOST, case[APIHOST])
    api_info.setdefault(METHOD, case[METHOD])
    api_info.setdefault(PARMAS, case[PARMAS])
    api_info.setdefault(APIHEADERS, case[APIHEADERS])
    api_info.setdefault(RELATEDAPI, case[RELATEDAPI])
    api_info.setdefault(RELEATEDPARAMS, case[RELEATEDPARAMS])

    return api_info


if __name__ == '__main__':
    cases = get_case()
    excute_case = get_excute_case(cases)
    print(len(excute_case))
    zz = [{'caseId': 1, 'apiId': 6, 'caseDescribe': '开始任务：正常请求', 'apiHost': '/s4/lite.subtask.start',
           'testData': {'sh': 't.sh', 'sql': 'select * from data'}, 'apiParams': '{"task_id":1}',
           'apiHeaders': {'cookie': 'mu=123456'}, 'method': 'GET', 'relatedApi': {'a': 1.0},
           'relatedParams': ['s', 'b'],
           'expect': {'payload.level_info.next_level_more_coin': '1', 'payload.reward': '5',
                      'payload.invalid_apprentice_num': '0', 'payload.shoutu_v5_3_open': '1'},
           'sqlStatement': {'a': 'select * from zhuanqian.user where id = ${payload.uid} ',
                            'b': 'select * from zhuanqian_1.user where id = ${payload.uid}',
                            'c': 'select * from zhuanqian.user_info where user_id=${payload.uid}'},
           'databaseExpect': {'a': 'len=1,create_reward=1', 'b': 'len=1', 'c': 'len=1'}, 'isExcute': 'Y'},
          {'caseId': 'sub_task_2', 'apiId': 'ss', 'caseDescribe': '开始任务：不传task_id', 'apiHost': '/s4/lite.subtask.start',
           'testData': None, 'apiParams': None, 'apiHeaders': None, 'method': 'GET', 'relatedApi': 2,
           'relatedParams': None, 'expect': {'err_code': '0', 'err_msg': '缺少参数：task_id'}, 'sqlStatement': None,
           'databaseExpect': None, 'isExcute': 'y'}]
    x = [{'caseId': 'case_1', 'apiId': 1, 'caseDescribe': 'sss', 'apiHost': '/s5/create_user',
          'testData': {'sql': 'select * from testcase'}, 'apiParams': {'s': '${id}'}, 'apiHeaders': None,
          'method': 'POST', 'relatedApi': {'apiHost': 'www.b'}, 'relatedParams': 'err_code,payload.uid',
          'expect': {'err_code': '0'}, 'sqlStatement': {'a': 'select * from zhuanqian.t_user_verify'},
          'databaseExpect': {'a': {'len': '5', 'id': '2'}}, 'isExcute': 'y'},
         {'caseId': 2, 'apiId': 2, 'caseDescribe': '主页，正常请求', 'apiHost': '/s5/dashboard', 'testData': None,
          'apiParams': None, 'apiHeaders': None, 'method': 'GET', 'relatedApi': 1, 'relatedParams': None,
          'expect': {'err_code': '0'}, 'sqlStatement': None, 'databaseExpect': None, 'isExcute': 'y'},
         {'caseId': 1.0, 'apiId': 6.0, 'caseDescribe': '开始任务：正常请求', 'apiHost': '/s4/lite.subtask.start',
          'testData': 'sh:t.sh\nsql:select * from data', 'apiParams': '{"task_id":1}', 'apiHeaders': 'cookie:mu=123456',
          'method': 'GET', 'relatedApi': '{"a":1.0}', 'relatedParams': 's\nb',
          'expect': 'payload.level_info.next_level_more_coin=1\npayload.reward=5\npayload.invalid_apprentice_num=0\npayload.shoutu_v5_3_open=1',
          'sqlStatement': 'a:select * from zhuanqian.user where id = ${payload.uid} \nb:select * from zhuanqian_1.user where id = ${payload.uid}\nc:select * from zhuanqian.user_info where user_id=${payload.uid}',
          'databaseExpect': 'a:len=1,create_reward=1\nb:len=1\nc:len=1', 'isExcute': 'n'},
         {'caseId': 'sub_task_2', 'apiId': 'ss', 'caseDescribe': '开始任务：不传task_id', 'apiHost': '/s4/lite.subtask.start',
          'testData': '', 'apiParams': '', 'apiHeaders': '', 'method': 'get', 'relatedApi': 2.0, 'relatedParams': '',
          'expect': 'err_code=0\nerr_msg=缺少参数：task_id', 'sqlStatement': '', 'databaseExpect': '', 'isExcute': 'n'},
         {'caseId': 'sub_task_3', 'apiId': 7.0, 'caseDescribe': '查看任务状态', 'apiHost': '/s4k/subtask.state',
          'testData': '', 'apiParams': '{"task_id":1}', 'apiHeaders': '', 'method': 'get', 'relatedApi': '',
          'relatedParams': '', 'expect': 'err_code=0', 'sqlStatement': '', 'databaseExpect': '', 'isExcute': 'n'},
         {'caseId': 1.0, 'apiId': 1.0, 'caseDescribe': '创建用户，正常请求', 'apiHost': '/s5/create_user', 'testData': '',
          'apiParams': '', 'apiHeaders': '', 'method': 'post', 'relatedApi': '', 'relatedParams': '$payload.uid',
          'expect': 'err_code=0\nerr_msg=',
          'sqlStatement': 'a:select * from zhuanqian.user where id = ${payload.uid} \nb:select * from zhuanqian_1.user where id = ${payload.uid}\nc:select * from zhuanqian.user_info where user_id=${payload.uid}',
          'databaseExpect': 'a:len=1,create_reward=1\nb:len=1\nc:len=1', 'isExcute': 'n'},
         {'caseId': 2.0, 'apiId': 2.0, 'caseDescribe': '主页，正常请求', 'apiHost': '/s5/dashboard', 'testData': '',
          'apiParams': '', 'apiHeaders': '', 'method': 'get', 'relatedApi': '', 'relatedParams': '',
          'expect': 'payload.level_info.next_level_more_coin=1\npayload.reward=5\npayload.invalid_apprentice_num=0\npayload.shoutu_v5_3_open=1',
          'sqlStatement': '', 'databaseExpect': '', 'isExcute': 'n'},
         {'caseId': 3.0, 'apiId': 3.0, 'caseDescribe': '试玩赚钱列表，正常请求', 'apiHost': '/s4/lite.subtask.list',
          'testData': '', 'apiParams': '', 'apiHeaders': '', 'method': 'get', 'relatedApi': '', 'relatedParams': '',
          'expect': 'err_code=0\npayload.tasks=[id=261567]', 'sqlStatement': '', 'databaseExpect': '', 'isExcute': 'n'},
         {'caseId': 4.0, 'apiId': 1.0, 'caseDescribe': '创建用户，请求方式为get', 'apiHost': '/s5/create_user', 'testData': '',
          'apiParams': '', 'apiHeaders': '', 'method': 'get', 'relatedApi': '', 'relatedParams': '',
          'expect': 'err_code=405', 'sqlStatement': '', 'databaseExpect': '', 'isExcute': 'n'},
         {'caseId': 5.0, 'apiId': 1.0, 'caseDescribe': '创建用户，添加cookie信息', 'apiHost': '/s5/create_user', 'testData': '',
          'apiParams': '', 'apiHeaders': 'cookie:DIS4=1122151', 'method': 'post', 'relatedApi': '', 'relatedParams': '',
          'expect': 'err_code=0', 'sqlStatement': '', 'databaseExpect': '', 'isExcute': 'n'},
         {'caseId': 6.0, 'apiId': 1.0, 'caseDescribe': '创建用户，师傅邀请创建', 'apiHost': '/s5/create_user', 'testData': '',
          'apiParams': '', 'apiHeaders': 'cookie:mu=123456', 'method': 'post', 'relatedApi': '', 'relatedParams': '',
          'expect': 'err_code=0', 'sqlStatement': '', 'databaseExpect': '', 'isExcute': 'n'},
         {'caseId': 7.0, 'apiId': 2.0, 'caseDescribe': '主页，用户没有领取金币', 'apiHost': '/s5/dashboard', 'testData': '',
          'apiParams': '', 'apiHeaders': '', 'method': 'get', 'relatedApi': '', 'relatedParams': '',
          'expect': 'err_code=0\npayload.first_claim=1', 'sqlStatement': '', 'databaseExpect': '', 'isExcute': 'n'},
         {'caseId': 8.0, 'apiId': 2.0, 'caseDescribe': '主页，用户领取金币', 'apiHost': '/s5/dashboard', 'testData': '',
          'apiParams': '', 'apiHeaders': '', 'method': 'get',
          'relatedApi': '{\n    "apiHost":"/s5/reward.coin.claim.today",\n    "method":"post",\n    "apiParams":"",\n    "apiHeaders":""\n}',
          'relatedParams': '$payload.level_info.next_level_more_coin\n$err_code',
          'expect': 'err_code=0\npayload.first_claim=0', 'sqlStatement': '', 'databaseExpect': '', 'isExcute': 'n'}]
