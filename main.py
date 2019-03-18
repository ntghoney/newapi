# -*- coding: utf-8 -*-
'''
@File  : main.py
@Date  : 2019/3/15/015 15:02
'''
from utils.handle_case import get_case, get_api
from utils.sqls import ConMysql
from config.config import *
from utils.parse_config import ParseConfig
from utils.common import get_current_time, request_api, MyEncoder
from utils.log import log
import json, re
from json import JSONDecodeError

CASETABLE = "testcase"
RESULTTABLE = "testresult"
APITABLE = "apiinfo"
pc = ParseConfig()


def get_user_info():
    uid = pc.get_info("user").get("uid")
    session = pc.get_info("user").get("session")
    return uid, session


class Result(object):
    def __init__(self):
        self.ispass = "pass"
        self.reason = None
        self.time = get_current_time()
        self.fact = None
        self.sql_res = None

    def get_result(self):
        return self.__dict__


def build_cookie(**kwargs):
    uid, session = get_user_info()
    if kwargs.get("uid"):
        uid = kwargs.get("uid")
    if kwargs.get("session"):
        session = kwargs.get("session")
    cookie = "DIS4={session};ln=1;lu={uid}".format(
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
        self.start_time = None
        self.end_time = None

    def __excute_result(self, **kwargs):
        result = dict()  # 用例执行结果
        # result.setdefault("statue", 1)  # 执行状态 0：fail，1：success，2：block
        # 执行状态 0：fail，1：success，2：block
        result.setdefault("ispass", PASS)
        result.setdefault("fact", None)  # 用例执行结果
        result.setdefault("time", get_current_time())
        result.setdefault("reason", None)  # 执行失败原因，block，fail
        result.setdefault("sql_res", None)
        if kwargs.get("ispass"):
            result["ispass"] = kwargs.get("ispass")
        if kwargs.get("time"):
            result["time"] = kwargs.get("time")
        if kwargs.get("fact"):
            result["fact"] = kwargs.get("fact")
        if kwargs.get("reason"):
            result["reason"] = kwargs.get("reason")
        return result

    def __replace_params(self, parmas):
        """
        替换参数
        :params:
        :return:
        """
        p = re.compile("\${.*?}")
        p1 = re.compile("\${(.*?)}")
        rp = pc.get_info("related_params")
        s = re.findall(p, parmas)  # 找到${id}整体
        if not s:
            return parmas
        for i in s:
            key = re.findall(p1, parmas)[0]  # 找到${id} id
            v = rp.get(key)
            # 参数是否在配置文件中存在
            # 存在则替换，不存在返回
            if v is None:
                return None
            parmas = parmas.replace(i, v)
        return parmas

    def __parameterize(self, params):
        """
        参数化
        :param params:
        :return:
        """
        if isinstance(params, dict):
            for key, value in params.items():
                value = self.__replace_params(value)
                if value is None:
                    return None  # 参数化失败
                params[key] = value
            return params
        params = self.__replace_params(params)
        if params is None:
            return None
        return params

    def __is_params(self, params):
        """
        是否参数化
        :param params:
        :return:
        """
        if not params:
            return False
        if isinstance(params, str):
            if "$" in params:
                return True
        if isinstance(params, dict):
            params = json.dumps(params, ensure_ascii=False)
            if "$" in params:
                return True
        return False

    def test(self):
        self.__excute_case()

    def __before_excute(self, case):
        """
        用例数据判空
        :param case:
        :return:
        """
        d = dict()
        case_id = case.get(CASEID)
        api_id = case.get(APIID)
        api_host = case.get(APIHOST)
        api_params = case.get(PARMAS)
        api_method = case.get(METHOD)
        api_headers = case.get(APIHEADERS)
        api_sql = case.get(SQLSTATEMENT)
        api_sql_check = case.get(DATABASEEXPECT)
        check_point = case.get(EXPECT)
        if case_id is None:
            d.setdefault("block", "当前用例id为空")
            return d
        if api_id is None:
            d.setdefault("block", "当前用例api_id为空")
            return d
        if api_host is None:
            d.setdefault("block", "用例api_host为空")
            return
        if api_method is None:
            d.setdefault("block", "用例api_method为空")
            return d
        if check_point is None:
            d.setdefault("block", "用例检查点未设置")
            return d
        if api_sql and api_sql_check is None:
            d.setdefault("block", "用例设置sql语句，但未设置sql检查点")
            return d
        # 如果用例中没有写入headers信息
        # 采用当前用户的session和uid作为cookie去请求接口
        # 当前用户信息从配置文件中加载，默认为之前测试的用户
        if not api_headers:
            uid = pc.get_info("user").get("uid")
            session = pc.get_info("user").get("session")
            if uid and session:
                cookie = build_cookie(uid=uid, session=session)
                case[APIHEADERS] = {"cookie": cookie}
                api_headers = case[APIHEADERS]
        # 检查是否参数化
        if self.__is_params(api_params):
            api_params = self.__parameterize(api_params)
            if api_params is None:
                d.setdefault("block", "params参数化设置失败")
                return d
            case[PARMAS] = api_params
        if self.__is_params(api_sql):
            api_sql = self.__parameterize(api_sql)
            if api_sql is None:
                d.setdefault("block", "sql语句参数化设置失败")
                return d
            case[SQLSTATEMENT] = api_sql
        if self.__is_params(api_headers):
            api_headers = self.__parameterize(api_headers)
            if api_headers is None:
                d.setdefault("block", "headers参数化设置失败")
                return d
            case[APIHEADERS] = api_headers
        return case

    def __excute_case(self, case):

        # 执行前判断用例必填参数是否为空
        case = self.__before_excute(case)
        if case.get("block") is not None:
            return case
        api_host = case.get(APIHOST)
        api_params = case.get(PARMAS)
        api_method = case.get(METHOD)
        api_headers = case.get(APIHEADERS)
        related_params = case.get(RELEATEDPARAMS)
        log.info("当前接口headers信息为%s" % api_headers)
        # log.info("当前用户uid:%s,session:%s")
        res = request_api(
            host=api_host,
            request_method=api_method,
            my_params=api_params,
            my_headers=api_headers
        )
        # 处理关联参数
        try:
            response = res.json()
            if related_params is None:
                return response
            related_params = related_params.split(",")
            for rp in related_params:
                if "." not in rp:
                    if response.get(rp) is not None:
                        pc.wirte_info("related_params", rp, str(response.get(rp)))
                    continue
                temp_res = response
                for i in rp.split("."):
                    temp_res = temp_res.get(i)
                    if not isinstance(temp_res, dict):
                        pc.wirte_info("related_params", rp, str(temp_res))
                    if temp_res is None:
                        return response
            return response
        except JSONDecodeError:
            return {"error": res}

    def before_test(self):
        # 清除数据库信息
        self.db_local.truncate_data(APITABLE)
        self.db_local.truncate_data(CASETABLE)
        self.db_local.truncate_data(RESULTTABLE)

        # 获得本次测试执行的用例
        self.cases = get_case()
        print(self.cases)
        if not self.cases:
            log.error("用例为空，无匹配格式的.xlsx文件或文件中暂无用例数据")
            return
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

        for case in self.cases:
            result = Result()
            result.time = get_current_time()
            check_points = case[EXPECT]
            sqls=case[SQLSTATEMENT]
            sql_points=case[DATABASEEXPECT]
            res = self.__excute_case(case)
            result.fact = res
            # 验证检查点
            self.__check_point(
                points=check_points,
                res=res,
                result=result
            )
            #数据库检查
            self.__check_sql(
                sql=sqls,
                sql_checks=sql_points,
                result=result
            )
            print(result.get_result())


    def __check_point(self, points, res, result):
        """
        接口检查点判断
        :param result:__Result对象
        :return:
        """
        assert isinstance(result, Result)
        # 执行用例前，不符合用例书写规则的用例执行结果全部定位block
        if res.get("block"):
            result.ispass = "block"
            result.reason = res.get("block")
            return
        if result.ispass != "pass":
            return
        for key, value in points.items():
            if "." not in key:
                if res.get(key) is None:
                    reason = "返回结果中没有检查点字段%s" % key
                    result.ispass = FAIL
                    result.reason = reason
                    return
                if str(res.get(key)) != str(value):
                    reason = "检查点%s预期结果为:%s,实际结果为:%s" % (
                        key, str(res.get(key)), value)
                    result.ispass = FAIL
                    result.reason = reason
                    return
            temp_res = res
            for point in key.split("."):
                temp_res = temp_res.get(point)
                if not isinstance(temp_res, dict):
                    if str(temp_res) != str(value):
                        reason = "检查点%s预期结果为:%s,实际结果为:%s" % (
                            key, str(res.get(key)), value)
                        result.ispass = FAIL
                        result.reason = reason
                        return
                if temp_res is None:
                    reason = "返回结果中没有检查点字段%s" % key
                    result.ispass = FAIL
                    result.reason = reason
                    return

    def __check_sql(self, sql, sql_checks, result):
        """
        sql检查
        :param sql:
        :param sql_checks:result: Result对象
        :return:
        """
        assert isinstance(result,Result)
        if result.ispass!="pass":
            return
        if isinstance(sql, dict) or isinstance(sql_checks, dict):
            reason="数据库语句或数据库检查点书写格式错误，无法转换为字典"
            result.ispass=BLOCK
            result.reason=reason
            return

        for key, value in sql.items():
            sql_res = self.db_server.query_all(value)
            result.sql_res=sql_res
            if sql_res.get("block"):
                result.ispass=BLOCK
                result.reason=sql_res.get("block")
                return
            if sql_checks.get(key) is None:
                reason="sql语句中设置了key为：%s,在sql检查点中没有设置对应key的检查点"%key
                result.ispass=BLOCK
                result.reason=reason
                return
            for k,v in value.items():
                if sql_res[0].get(k) is None:
                    result.ispass=FAIL
                    reason="sql检查点%s中的%s不在数据库返回结果的字段中"%(key,k)
                    result.reason=reason
                    return
                if sql_res.get(k) !=v:
                    result.ispass=FAIL
                    reason="sql检查点%s中%s的值期望为：%s,实际为：%s"%(
                        key,k,v,sql_res.get(k))
                    result.reason=reason
                    return

    def run(self):
        pass


if __name__ == '__main__':
    r = Run()
    r.before_test()
    g = r.begin_test()
