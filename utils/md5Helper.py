# -*- coding: utf-8 -*-
'''
@File  : md5Helper.py
@Date  : 2019/3/12/012 12:51
'''
import hashlib
import logging


logger = logging.getLogger(__name__)


class DigestHelper(object):

    def md5sum(self, b):
        """
        获取bytes内容对应的MD5摘要结果

        Args:
            :b: bytes

        Returns:
            str
        """
        if not isinstance(b, bytes):
            raise TypeError('b should be bytes')
        m = hashlib.md5()
        m.update(b)
        rv = m.hexdigest()
        return rv

    def md5(self, string):
        """

        :param string: string类型
        :return:
        """
        if not isinstance(string, str):
            raise TypeError('string should be str')
        m = hashlib.md5()
        m.update(string.encode())
        rv = m.hexdigest()
        return rv

    def sha1(self, string):
        """
        sha1加密
        :param string: string类型的参数
        :return:
        """
        return hashlib.sha1(string.encode()).hexdigest()


digest_helper = DigestHelper()
