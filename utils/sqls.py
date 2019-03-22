# -*- coding: utf-8 -*-
'''
@File  : conDatabase.py
@Date  : 2019/1/18/018 9:35
'''
import pymysql
from utils.log import log
from config.config import SQLINFO, CASEID, TESTDATA, METHOD
import json


# def data_for_dict(data):
#     """
#     将数据转换成字典形式储存
#     :param data:
#     :return:
#     """
#     if len(data) == 8:
#         data_dic = {}
#         data_dic[CASEID] = int(data[0])
#         data_dic[CASEDESCRIBE] = str(data[1])
#         data_dic[APIHOST] = str(data[2])
#         data_dic["params"] = data[3]
#         data_dic[METHOD] = data[4]
#         data_dic[RELATEDAPI] = data[5]
#         data_dic[RELEATEDPARAMS] = data[6]
#         data_dic[EXPECT] = json.loads(data[7])
#         return data_dic
#     else:
#         log.error("获取数据长度不正确")
#         return None
#
#
# database_info = ParseConfig().get_info("MyDatabase")
# mysqlInfo = get_base_info(database_info)


class ConMysql(object):
    def __init__(self, uri="local"):
        sql_info = SQLINFO.get(uri)
        if not sql_info:
            raise Exception("数据库配置失败，不存在%s" % uri)
        self.conn = pymysql.connect(**sql_info)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def truncate_data(self, table):
        """
        删除表数据
        :param table:表名
        :return:
        """
        self.execute_sql("TRUNCATE TABLE {}".format(table))

    # def execute_sql(self, sql):
    #     """
    #     执行sql
    #     :param sql:
    #     :return:
    #     """
    #     self.cursor.execute(sql)

    def execute_sql(self, sql):
        """
        执行sql
        :param sql:
        :return:
        """
        try:
            rv = self.cursor.execute(sql)
            self.conn.commit()
            return rv
        except Exception as e:
            print(e)
            log.error("sql语句错误---->{}".format(sql))

    def query_one(self, sql):
        """
        查询单条
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            datas = self.cursor.fetchone()
        except Exception as e:
            log.error("sql语句错误---->%s,%s" % (sql, e))
            return {"block": "sql语句错误"}
        return datas

    def query_all(self, sql):
        """
        查询所有
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            datas = self.cursor.fetchall()
        except Exception as e:
            log.error("sql语句错误---->%s,%s" % (sql, e))
            return {"block": "sql语句错误"}
        return datas

    def insert_data(self, table, **kwargs):
        """
        插入数据
        :param table:
        :param kwargs: (字段=value)
        :return:
        """
        from utils.common import MyEncoder
        sql = "INSERT INTO %s SET " % table
        for key, value in kwargs.items():
            if key == TESTDATA:
                continue
            if value is None:
                sql += " %s=Null," % (key)
            elif isinstance(value, str):
                value=value.replace('"',"'")
                sql += """ %s="%s",""" % (key, value)
            elif isinstance(value, dict):
                value = json.dumps(value, ensure_ascii=False, cls=MyEncoder)
                sql += " %s='%s'," % (key, value)
            elif isinstance(value, list):
                value = str(value)
                sql += """ %s="%s", """ % (key, value)
            else:
                sql += " %s=%s," % (key, value)
        sql = sql[:-1]
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            log.error("sql语句错误---->%s,%s" % (sql, e))
        # for key in kwargs.keys():
        #     if not key.__eq__(CASEID) and not key.__eq__(TESTDATA) and not key.__eq__(METHOD):
        #         if isinstance(kwargs[key], dict):
        #             kwargs[key] = json.dumps(kwargs[key], ensure_ascii=False)
        #         elif isinstance(kwargs[key], str):
        #             kwargs[key] = kwargs[key].replace("\'", "\"")
        #         elif isinstance(kwargs[key], list):
        #             if kwargs[key]:
        #                 kwargs[key] = str(kwargs[key]).replace("\'", "").replace("[", "").replace("]", "")
        #         elif isinstance(kwargs[key], int):
        #             kwargs[key] = kwargs[key]
        #         elif kwargs[key].__eq__(""):
        #             continue
        #         sql += "{}='{}',".format(key, kwargs[key])

    def update_data(self, sql):
        """
        修改表数据
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            log.error("sql语句错误---->%s,%s" % (sql, e))

    def close(self):
        """
        关闭链接
        :return:
        """
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    # cases = HandleCase().get_cases()[0]
    sql = ConMysql()
    a = sql.query_one("select * from apiinfo ")
    print(a)
