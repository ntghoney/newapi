# -*- coding: utf-8 -*-
'''
@File  : parseExc.py
@Date  : 2019/1/15/015 17:50
'''
import xlrd
import os
from utils.log import log


class ParseExcel(object):
    """
    解析Excel
    ParseExcel("path",index).get_all_for_row()
    获得excel所有数据，按行返回数据列表
    """

    def __init__(self, excel_path, sheet_index: int):
        if os.path.isfile(excel_path):
            if os.path.exists(excel_path):
                self.workbook = xlrd.open_workbook(excel_path)
                self.sheet = self.workbook.sheet_by_index(sheet_index)
                log.info("用例路径：{}".format(excel_path))
            else:
                log.error("{}文件不存在".format(excel_path))
        else:
            log.error("请检查{}路径是否正确".format(excel_path))

    # 获得总行数
    def get_rows(self):
        return self.sheet.nrows

    # 获得总列数
    def get_cols(self):
        return self.sheet.ncols

    # 按行获得所有数据
    def get_all_for_row(self):
        rv = []
        for row in range(self.get_rows()):
            rv.append(self.sheet.row_values(row))
        return rv


if __name__ == '__main__':
    print(ParseExcel(r"E:\project\newapi\cases\case_subtask.xlsx", 0).get_all_for_row())
