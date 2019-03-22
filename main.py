# -*- coding: utf-8 -*-
'''
@File  : main.py
@Date  : 2019/3/15/015 15:02
'''
from utils.handle_case import get_case, get_api, get_excute_case
from utils.sqls import ConMysql
from config.config import *
from utils.parse_config import ParseConfig
from utils.common import (get_current_time, request_api,
                          KeyHeaders, MakeSign, generate_random_str,
                          login)
from utils.log import log
import json, re, time, datetime, sys
from json import JSONDecodeError
from utils.report import Report
from utils.html_report import get_html_report
from utils.hebe_session import HebeSession
from utils.send_email import send_email_for_all

CASETABLE = "testcase"
RESULTTABLE = "testresult"
APITABLE = "apiinfo"
pc = ParseConfig()
dis_p = re.compile(r"DIS4=(.*?);")


def get_user_info():
    uid = pc.get_info("user").get("uid")
    session = pc.get_info("user").get("session")
    return uid, session


class Result(object):
    def __init__(self):
        self.method = None
        self.caseId = None
        self.caseDescribe = None
        self.apiHost = None
        self.apiParams = None
        self.expect = None
        self.ispass = "pass"
        self.reason = None
        if self.ispass == "pass":
            self.reason = ""
        self.time = get_current_time()
        self.fact = None
        self.databaseResult = None
        self.databaseExpect = None

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


def bind_key(session_id):
    """
    绑定钥匙
    :param session_id:
    :return:
    """
    kHeader = KeyHeaders(sid=session_id)
    m_headers = kHeader.build_headers()
    uri = '/s5k/v2/key.bind'
    sign = MakeSign.sign(uri, m_headers, {})
    m_headers = kHeader.with_sign_headers(sign)
    s = request_api(
        host=uri,
        my_params={},
        my_headers=m_headers,
        request_method="GET"
    )
    try:
        resp = s.json()
        if resp["err_code"] == 0 and resp["payload"]["lppa"] == 1:
            log.info("绑定钥匙成功")
        else:
            log.info("绑定钥匙失败,err_code:%s,payload:%s" % (resp["err_code"], resp["payload"]))
    except:
        log.info("绑定钥匙失败")
        sys.exit(-1)


def install_certificate(sid, uid, db: ConMysql):
    """
    安装证书
    :param sid:session_id
    :return:
    """
    cu = HebeSession(db)
    udid = "udid07A8-26B2-4749-AFF3-0435B6ED525"
    sql = """
           INSERT INTO user_device_certificate
           (user_id,udid,issuer_cn,subject_cn,serial_number,not_before,client_ip,created_at)
           VALUES (%s,"%s","33ab9800f1378cb13ea4eeb6a4ce56af2987ec69",
           "D8DEBC4A-8EE7-4953-9259-556F87353D5C","13220895031545118235832",
           "2017-03-11 07:55:23","10.168.205.147","%s")
       """ % (uid, udid,get_current_time())
    db.execute_sql(sql)
    cu.bind_sid_udid(sid=sid, udid=udid)
    info = cu.get_session_info(sid)
    if info.get("udid", "") == udid:
        log.info("证书安装成功")
    else:
        log.info("证书安装失败")
        sys.exit(-1)


class Run(object):
    def __init__(self):
        self.db_local = ConMysql()
        self.db_server = ConMysql("fp01")
        self.cases = None
        self.api = None
        self.start_time = None
        self.end_time = None

    def __update_message(self, number):
        """
        更新t_user_verify表信息
        :param number: 用户手机号，从apiParams中获取
        :return:
        """
        result = self.db_server.query_one(
            "select * from t_user_verify where number ={}"
                .format(number)
        )
        # 十分钟前的时间
        timedelta = datetime.datetime.now() - datetime.timedelta(minutes=10)
        if not result:
            self.db_server.insert_data("t_user_verify",
                                       number=number,
                                       call_sid=generate_random_str(32),
                                       verify="123456",
                                       date_created=get_current_time(),
                                       status=1)
            return
        if result["date_created"] < timedelta:
            sql = "update t_user_verify set date_created='{}'where number={}". \
                format(get_current_time(), number)
            self.db_server.update_data(sql)
        if result["status"] == 0:
            self.db_server.update_data(
                "update t_user_verify set status=1 where number={}"
                    .format(number)
            )

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
        log.info("参数化前%s" % parmas)
        if rp is None:
            log.info("参数化失败，related_params为空")
            return parmas
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
        log.info("参数化后%s" % parmas)
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

        return case

    def __begin_paramertrize(self, case):
        """
        开始参数化
        :param case:
        :return:
        """
        d = dict()
        api_params = case.get(PARMAS)
        api_headers = case.get(APIHEADERS)
        api_sql = case.get(SQLSTATEMENT)
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

    def __get_related_api(self, related_api):
        """
        获得关联接口信息
        :param related_api:用例中related_api的值
        related_api 可能为接口id，接口路径，接口信息（json格式）
        :return:
        """
        if not related_api:
            return []
        infos = []
        while related_api is not None:
            if isinstance(related_api, dict):
                for key, value in related_api.items():
                    if value == "":
                        related_api[key] = None
                    if key == "method":
                        related_api[key] = value.upper()
                infos.append(related_api)
                related_api = related_api.get(RELATEDAPI)
                continue
            try:
                related_api = json.loads(related_api, encoding="utf8")
                for key, value in related_api:
                    if value == "":
                        related_api[key] = None
                    if key == "method":
                        value = value.upper()
                        related_api[key] = value
                infos.append(related_api)
                related_api = related_api.get(RELATEDAPI)
                continue
            except (JSONDecodeError, TypeError):
                info_for_id = self.db_local.query_one(
                    "SELECT * FROM apiinfo WHERE apiId='%s' " % related_api)
                if info_for_id is None:
                    info_for_host = self.db_local.query_one(
                        "SELECT * FROM apiinfo WHERE apiHost='%s' " % related_api)
                    if info_for_host is None:
                        return {"error": "关联接口不存在%s" % related_api}
                    related_api = info_for_host.get(RELATEDAPI)
                    infos.append(info_for_host)
                else:
                    related_api = info_for_id.get(RELATEDAPI)
                    infos.append(info_for_id)
        for api in infos:
            for key, value in api.items():
                try:
                    # 关联接口从数据库中取出来，保存的字典在数据库中只能以字符串保存
                    # 所以使用时先转换为字典
                    value = json.loads(value, encoding="utf8")
                    api[key] = value
                except (JSONDecodeError, TypeError):
                    pass
        # 关联接口列表反转
        infos.reverse()
        return infos

    def __excute_case(self, case):

        # 执行前判断用例必填参数是否为空
        case = self.__before_excute(case)
        # 清除上一条用例所产生的参数
        pc.remote_section("related_params")
        if case.get("block") is not None:
            return case
        api_headers = case.get(APIHEADERS)
        related_api = case.get(RELATEDAPI)
        # 获得关联接口
        related_api_info = self.__get_related_api(related_api)
        # 将当前用例执行的接口信息信息附加在关联接口后
        related_api_info.append(get_api(case))
        # 如果关联接口中的headers信息为空，使用当前用例接口的headers信息
        log.info("当前接口headers信息为%s" % api_headers)
        log.info("当前用户uid:%s,session:%s")
        for api in related_api_info:
            api = self.__begin_paramertrize(api)
            api_host = api.get(APIHOST)
            api_params = api.get(PARMAS)
            api_method = api.get(METHOD)
            related_params = api.get(RELEATEDPARAMS)
            log.info("执行接口%s" % api_host)
            if api_params is not None and \
                    isinstance(api_params, dict) \
                    and "phone" in api_params.keys():
                # self.db_server
                phone = api_params.get("phone")
                self.__update_message(phone)
            if api_host is None or api_method is None:
                return {"error": "接口信息不完整"}
            if api.get(APIHEADERS) is None:
                # 如果关联接口中的headers信息为空，使用当前用例接口的headers信息
                api_headers = api_headers
            res = request_api(
                host=api_host,
                request_method=api_method,
                my_params=api_params,
                my_headers=api_headers
            )
            if "create_user" in api_host or "login.mobile" in api_host:
                h = res.headers["Set-Cookie"]
                s_id = re.findall(dis_p, h)[-1]
                api_headers = {"cookie": "DIS4=%s" % s_id}
                log.info("调用%s接口，headers信息改变，为%s" % (api_host, api_headers))
            if isinstance(res, dict) and res.get("error"):
                return {"code": "error",
                        "status_code": 10086,
                        "response": res.get("error")}
            # 处理关联参数
            try:
                response = res.json()
                print(response)
                if related_params is not None:
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
                                # json数组,取第一个json作为关联参数
                                if isinstance(temp_res, list):
                                    if temp_res:
                                        temp_res = temp_res[0]
                                        continue
                                    break
                                pc.wirte_info("related_params", rp, str(temp_res))
                            if temp_res is None:
                                break
                # 遍历到最后一个接口，即当前用例接口
                if related_api_info.index(api) == len(related_api_info) - 1:
                    # 用例执行完毕后再次参数化
                    self.__begin_paramertrize(case)
                    return {"code": "success",
                            "status_code": res.status_code,
                            "response": response}
            except (JSONDecodeError, TypeError):
                log.info("当前接口%s返回%s,无法转换为json，参数化失败"
                         % (api.get(APIID), res))
                return {"code": "error",
                        "status_code": res.status_code,
                        "response": "status_code=%s" % res.status_code}

    def __prapare_data(self, data):
        """
        准备用例前置数据
        :param data:用例test_data的值
        :return:
        """
        if not data:
            return
        for key, value in data.items():
            if key == "sql":
                try:
                    self.db_server.execute_sql(value)
                    log.info("执行sql成功%s" % value)
                except Exception as e:
                    log.error("sql语句出错：%s,%s" % (value, e))
            elif key == "sh":
                try:
                    os.system(value)
                except:
                    log.error("shell文件出错")
            else:
                pass

    def before_test(self):
        # 登陆,创建一个新用户作为本次测试的用户
        user_info = login()
        # 写入配置文件
        if user_info:
            pc.wirte_info("user", "session", user_info["sid"])
            pc.wirte_info("user", "uid", user_info["uid"])
        # 清除数据库信息
        self.db_local.truncate_data(APITABLE)
        self.db_local.truncate_data(CASETABLE)
        self.db_local.truncate_data(RESULTTABLE)
        all_case = get_case()  # 获得所有用例
        self.start_time = time.time()
        s_id = pc.get_info("user").get("session")
        u_id=pc.get_info("user").get("uid")
        # 绑定钥匙
        bind_key(s_id)
        # 安装证书
        install_certificate(s_id, u_id,self.db_server)
        # 获得本次测试执行的用例
        self.cases = get_excute_case(all_case)
        log.info("本次测试共执行%s条用例" % len(self.cases))
        if not self.cases:
            log.error("用例为空，无匹配格式的.xlsx文件或文件中暂无用例数据")
            return
        self.api = [get_api(case) for case in all_case]
        # 数据库保存接口信息
        for api in self.api:
            self.db_local.insert_data(APITABLE, **api)
        # 数据库保存用例信息
        for case in self.cases:
            self.db_local.insert_data(CASETABLE, **case)

    def after_test(self, result_set):
        self.end_time = time.time()
        for result in result_set:
            # 将执行结果写入数据库
            self.db_local.insert_data(RESULTTABLE, **result)
        time_consum = self.end_time - self.start_time  # 测试耗时
        case_count = self.db_local.query_all(
            "SELECT caseId FROM {}".format(RESULTTABLE)
        )  # 执行用例
        fail_case = self.db_local.query_all(
            "SELECT caseId "
            "FROM {} WHERE ispass='{}'".format(RESULTTABLE, FAIL)
        )  # 执行失败的用例
        block_case = self.db_local.query_all(
            "SELECT caseId FROM {} WHERE ispass='{}'".format(RESULTTABLE, BLOCK)
        )  # 执行阻塞的用例
        success_case = self.db_local.query_all(
            "SELECT caseId FROM {} WHERE ispass='{}'".format(RESULTTABLE, PASS)
        )  # 执行成功的用例

        if case_count is None:
            case_count = 0
        else:
            case_count = len(case_count)
        if fail_case is None:
            fail_case = 0
        else:
            fail_case = len(fail_case)
        if block_case is None:
            block_case = 0
        else:
            block_case = len(block_case)
        if success_case is None:
            success_case = 0
        else:
            success_case = len(success_case)
        result_info = "本次测试执行完毕，本次测试环境为：{}，" \
                      "共耗时{}秒，共执行用例：{}条，" \
                      "成功：{}条，失败：{}条，阻塞：{}条" \
            .format("fp01", float("%.2f" % time_consum),
                    case_count, success_case,
                    fail_case, block_case)
        log.info(result_info)
        # 生成excel报告
        report = Report()
        report.set_result_info(result_info)
        exc_path = report.get_report(result_set)

        # 生成html报告
        import datetime
        html_title = "%s接口自动化测试报告" % (datetime.datetime.now().strftime("%Y/%m/%d"))
        html_path = get_html_report(
            total=case_count,
            starttime=time.strftime(FORMORT, time.localtime(self.start_time)),
            endtime=time.strftime(FORMORT, time.localtime(self.end_time)),
            during=time_consum,
            passd=success_case,
            fail=fail_case,
            block=block_case,
            titles=html_title,
            details=result_set
        )
        self.db_local.close()
        self.db_server.close()

        # 测试完成发送邮件
        if fail_case == 0 and block_case == 0:
            send_email_for_all(
                msg=result_info,
                part_path=[exc_path, html_path])

    def begin_test(self):
        result_set = []  # 用例执行结果集
        for case in self.cases:
            log.info("正在执行caseId为%s的用例" % case.get(CASEID))
            result = Result()
            result.method = case.get(METHOD)
            result.time = get_current_time()
            result.apiHost = case.get(APIHOST)
            result.caseDescribe = case.get(CASEDESCRIBE)
            result.databaseExpect = case.get(DATABASEEXPECT)
            result.caseId = case.get(CASEID)
            result.apiParams = case.get(PARMAS)
            check_points = case[EXPECT]
            result.expect = check_points
            sqls = case[SQLSTATEMENT]
            sql_points = case[DATABASEEXPECT]
            test_data = case[TESTDATA]  # 测试前提数据
            self.__prapare_data(test_data)  # 准备数据，执行sql或者shell

            # 请求接口
            res = self.__excute_case(case)
            result.fact = res.get("response")
            # 验证检查点
            self.__check_point(
                points=check_points,
                res=res,
                result=result
            )
            # 数据库检查
            self.__check_sql(
                sql=sqls,
                sql_checks=sql_points,
                result=result
            )
            test_result = result.get_result()
            result_set.append(test_result)
            log.info("caseId为%s的用例完毕" % case.get(CASEID))
        return result_set

    def __check_point(self, points, res, result):
        """
        接口检查点判断
        :param result:__Result对象
        :return:
        """
        assert isinstance(result, Result)
        # 执行用例前，不符合用例书写规则的用例执行结果全部定位block
        if res.get("code") == "error":
            status_code = res.get("status_code")
            for key, value in points.items():
                if key == "status_code":
                    if str(value) != str(status_code):
                        reason = "status_code预期为%s,实际为%s" % (value, status_code)
                        result.ispass = FAIL
                        result.reason = reason
                        return
            return
        if res.get("block"):
            result.ispass = "block"
            result.reason = res.get("block")
            return
        if result.ispass != "pass":
            return
        res = res.get("response")
        for key, value in points.items():
            # 简单检查点 eg:err_code=0
            if "." not in key:
                if res.get(key) is None:
                    reason = "返回结果中没有检查点字段%s" % key
                    result.ispass = FAIL
                    result.reason = reason
                    return
                if str(res.get(key)) != str(value):
                    reason = "检查点%s预期结果为:%s,实际结果为:%s" % (
                        key, value, str(res.get(key)))
                    result.ispass = FAIL
                    result.reason = reason
                    return
            temp_res = res
            # 多重json，eg:payload.uid=12345
            for point in key.split("."):
                temp_res = temp_res.get(point)
                if not isinstance(temp_res, dict):
                    # json数组检查点 eg:payload.tasks=id:(1,2,3)
                    if isinstance(temp_res, list):
                        k, v = value.split("=")
                        p = re.compile(r"\((.*?)\)")
                        tem = re.findall(p, v)
                        if not tem:
                            reason = "用例书写json数组的方式错误"
                            result.ispass = BLOCK
                            result.reason = reason
                            return
                        v = tem[0].split(",")
                        vv = [str(gg.get(k)) for gg in temp_res]
                        for i in v:
                            if i not in vv:
                                reason = "%s字段预期的值不在返回结果集中，预期%s=%s，实际%s=%s" % (
                                    k, k, v, k, vv
                                )
                                result.ispass = FAIL
                                result.reason = reason
                                return
                        return
                    if str(temp_res) != str(value):
                        reason = "检查点%s预期结果为:%s,实际结果为:%s" % (
                            key, value, str(temp_res))
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
        assert isinstance(result, Result)
        if result.ispass != "pass":
            return
        if sql is None:
            return
        if sql is not None and sql_checks is None:
            reason = "未设置sql检查点"
            result.ispass = BLOCK
            result.reason = reason
            return
        if not isinstance(sql, dict) or not isinstance(sql_checks, dict):
            reason = "数据库语句或数据库检查点书写格式错误，无法转换为字典"
            result.ispass = BLOCK
            result.reason = reason
            return
        sql_res_all = {}
        for key, value in sql.items():
            sql_res = self.db_server.query_all(value)
            sql_res_all[key] = sql_res
            if isinstance(sql_res, dict) and sql_res.get("block"):
                result.ispass = BLOCK
                result.reason = "sql检查点%s:%s" % (key, sql_res.get("block"))
                result.databaseResult = sql_res_all
                return
            if sql_checks.get(key) is None:
                reason = "sql语句中设置了key为：%s,在sql检查点中没有设置对应key的检查点" % key
                result.ispass = BLOCK
                result.reason = reason
                result.databaseResult = sql_res_all
                return
            for k, v in sql_checks.get(key).items():
                if k == "len":
                    if str(len(sql_res)) != str(v):
                        result.ispass = FAIL
                        reason = "sql检查点%s中%s的值期望为：%s,实际为：%s" % (
                            key, k, v, len(sql_res))
                        result.reason = reason
                        result.databaseResult = sql_res_all
                        return
                    continue
                if sql_res[0].get(k) is None:
                    result.ispass = FAIL
                    reason = "sql检查点%s中的%s不在数据库返回结果的字段中" % (key, k)
                    result.reason = reason
                    result.databaseResult = sql_res_all
                    return
                if str(sql_res[0].get(k)) != str(v):
                    result.ispass = FAIL
                    reason = "sql检查点%s中%s的值期望为：%s,实际为：%s" % (
                        key, k, v, sql_res[0].get(k))
                    result.reason = reason
                    result.databaseResult = sql_res_all
                    return

    def run(self):
        # 执行前d
        self.before_test()
        # 执行
        result_set = self.begin_test()
        # 执行完毕生成报告,清除数据
        self.after_test(result_set)
        #


if __name__ == '__main__':
    r = Run()
    r.run()
