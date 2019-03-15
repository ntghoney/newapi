# -*- coding: utf-8 -*-
'''
@File  : parseConfig.py
@Date  : 2019/1/15/015 16:34
'''
from utils.common import MyConf
import os
from config.config import PRODIR

DEFAULT = os.path.abspath(os.path.join(PRODIR, "config/info.ini"))


class ParseConfig(object):
    def __init__(self, path=DEFAULT):
        self.cf = MyConf()
        self.cf.read(path, encoding="gbk")
        self.path = path

    # 根据section读取配置文件信息，返回数据字典
    def get_info(self, section):
        """
        根据section读取配置文件信息，返回数据字典
        """
        info = {}
        if section in self.cf.sections():
            for i in self.cf.options(section):
                info[i] = self.cf.get(section, i)
            return info
        return None

    def get_report_info(self):
        return self.cf.options("report")

    def wirte_info(self, section, option, info):
        """
        往配置文件中写入内容
        :param info: 写入的内容信息
        """
        if section not in self.cf.sections():
            self.cf.add_section(section)
        self.cf.set(section, option, info)
        with open(self.path, "w", encoding="gbk") as f:
            self.cf.write(f)
            f.close()

    def remote_section(self, section):
        """
        删除section
        """
        if section in self.cf.sections():
            self.cf.remove_section(section)
        else:
            return
        with open(self.path, "w") as f:
            self.cf.write(f)
            f.close()

    def remote_option(self, section, option):
        """
        删除option
        """
        if section in self.cf.sections():
            if option in self.cf.options(section):
                self.cf.remove_option(section, section)
            else:
                return
        else:
            return
        with open(self.path, "w") as f:
            self.cf.write(f)
            f.close()


if __name__ == '__main__':
    pc = ParseConfig()
    pc.wirte_info("params", "a", "b")
