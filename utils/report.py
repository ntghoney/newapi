# -*- coding: utf-8 -*-
'''
@File  : report.py
@Date  : 2019/1/16/016 9:45
'''
from utils.log import log, get_now
import xlwt
from xlwt import *
from config.config import *


class Report(object):
    def __init__(self):
        self.__result_info = None
        self.reportNcols = REPORT.get("ncols") # 总列数
        self.reportTitle = REPORT.get("title")  # 报告标题
        self.reportColName = REPORT.get("colname").split(",")  # 报告列名
        self.report_name="{}接口自动化测试报告.xls".format(get_now().strftime("%Y%m%d"))
        self.reportPath = os.path.abspath(os.path.join(PRODIR,"report/%s"%self.report_name))
        # 新建excel
        self.workbook = xlwt.Workbook()

        self.table = self.workbook.add_sheet(u"接口测试报告", cell_overwrite_ok=True)

    # 设置列宽
    def set_col_width(self, ncols, width):
        for i in range(ncols):
            self.table.col(i).width = width

    # 设置垂直居中
    def set_center(self):
        alignment = xlwt.Alignment()  # 设置居中
        # alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        return alignment

    # 设置垂直水平居中
    def set_all_center(self):
        alignment = xlwt.Alignment()  # 设置居中
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        return alignment

    # 设置自动换行
    def auto_line(self):
        alignment = xlwt.Alignment()
        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        return alignment

    # 标题样式
    def title_style(self):
        style = xlwt.easyxf('pattern: pattern solid, fore_colour 0x16;')  # 设置背景颜色为灰色
        style.alignment = self.set_all_center()
        style.font.height = 800
        style.font.bold = True  # 设置加粗
        return style

    # 列名单元格样式
    def col_name_style(self):
        style = xlwt.easyxf('pattern: pattern solid, fore_colour 0x16;')
        style.font.height = 400
        style.alignment = self.set_center()
        return style

    # 自动换行样式
    def col_auto_line_style(self):
        style = XFStyle()
        style.font.height = 250
        style.alignment = self.set_center()
        return style

    # 自动换行，垂直居中
    def style1(self):
        style = XFStyle()
        style.font.height = 250
        style.alignment = self.auto_line()
        style.alignment.vert = xlwt.Alignment.VERT_CENTER
        return style

    def result_info_style(self):
        style = XFStyle()
        font = xlwt.Font()
        font.name = "宋体"
        font.height = 300
        style.font = font
        return style

    # 普通单元个样式
    def col_style(self):
        style = XFStyle()
        style.alignment = self.set_center()
        style.font.height = 250
        return style

    def write(self, row, col, msg="", style=Style.default_style):
        self.table.write(row, col, msg, style)

    def write_merge(self, r1, r2, c1, c2, msg="", style=Style.default_style):
        self.table.write_merge(r1, r2, c1, c2, msg, style)

    def set_result_info(self, result_info):
        self.__result_info = result_info

    # 逐行写入数据
    def write_line(self, row, resdic):
        for key in resdic.keys():
            if key.__eq__(CASEID):
                self.write(row, 0, resdic[key], self.style1())
            elif key.__eq__(CASEDESCRIBE):
                self.write(row, 1, resdic[key], self.style1())
            elif key.__eq__(APIHOST):
                self.write(row, 2, resdic[key], self.style1())
            elif key.__eq__(METHOD):
                self.write(row, 3, resdic[key], self.style1())
            elif key.__eq__(PARMAS):
                self.write(row, 4, resdic[key], self.style1())
            elif key.__eq__(EXPECT):
                self.write(row, 5, resdic[key], self.style1())
            elif key.__eq__(FACT):
                self.write(row, 6, resdic[key], self.col_style())
            elif key.__eq__(DATABASERESUTL):
                self.write(row, 7, resdic[key], self.col_style())
            elif key.__eq__(DATABASEEXPECT):
                self.write(row, 8, resdic[key], self.col_style())
            elif key.__eq__(ISPASS):
                self.write(row, 9, resdic[key], self.style1())
            elif key.__eq__(TIME):
                self.write(row, 10, resdic[key], self.style1())
            elif key.__eq__(REASON):
                self.write(row, 11, resdic[key], self.style1())

    def get_report(self, result):
        """
        生成excel报告
        :param result:
        :return: reportPath：报告保存路径 report_name：报告名字
        """
        import json
        from utils.common import MyEncoder
        ncols = self.reportNcols
        row = 3  # 从第二行写入用例执行情况
        # 设置测试报告列宽
        self.set_col_width(ncols, 6000)
        # 标题内容
        self.write_merge(0, 0, 0, ncols - 1, self.reportTitle, self.title_style())
        # 写入列名，逐列写入
        for col in range(ncols):
            self.write(2, col, self.reportColName[col], self.col_name_style())
        # 写入用例执行统计情况
        self.write_merge(1, 1, 0, ncols - 1, self.__result_info, self.result_info_style())
        # 写如用例执行情况
        log.info("正在写入用例执行情况")
        for res in result:
            for key,value in res.items():
                if isinstance(value,dict):
                    value=json.dumps(value,ensure_ascii=False,cls=MyEncoder)
                    res[key]=value
                if value is None:
                    value="None"
                    res[key]=value

            self.write_line(row, res)
            row += 1
        self.workbook.save(self.reportPath)
        return self.reportPath,self.report_name


if __name__ == '__main__':
    r_set = [{'method': 'post', 'caseId': 1, 'caseDescribe': '创建用户，正常请求', 'apiHost': '/s5/create_user', 'apiParams': '',
              'expect': '{"err_code": "0", "err_msg": ""}',
              'fact': '{\n  "err_code": 0,\n  "err_msg": "",\n  "messages": [],\n  "payload": {\n    "uid": 51229992\n  }\n}',
              'databaseResult': '{"a": [{"id": 51229992, "apprentice_integral": 0.0, "apprentice_num": 0, "masterid": 0, "currency": 0.0, "degree": 0, "master_degree": 0, "create_time": 1551924692, "create_day": 20190307, "create_reward": 1, "income": 0.0, "today_income": 0.0, "expenses": 0.0, "expenses_price": 0.0, "login_time": 1551924692, "isvalid": 1}], "b": [{"id": 51229992, "apprentice_integral": 0.0, "apprentice_num": 0, "masterid": 0, "currency": 0.0, "degree": 0, "master_degree": 0, "create_time": 1551924692, "create_day": 20190307, "create_reward": 1, "income": 0.0, "today_income": 0.0, "expenses": 0.0, "expenses_price": 0.0, "login_time": 1551924692, "isvalid": 1, "is_new_to_sq": 1}], "c": [{"user_id": 51229992, "mobile_number": "", "nickname": "", "head_portrait": "v3:43182fd4080fa912dd0f421158187f0b.png", "user_gender": "", "user_birthday": "", "user_profession": "", "device_quantity": "", "last_time": 1551924692, "is_upload": 0, "is_complete": 0, "is_reward": 0}]}',
              'databaseExpect': '{"a": "len=1,create_reward=1", "b": "len=1", "c": "len=1"}', 'ispass': 'fail',
              'time': '2019/03/07 10:11:35', 'reason': ''},
             {'method': 'get', 'caseId': 2, 'caseDescribe': '主页，正常请求', 'apiHost': '/s5/dashboard', 'apiParams': '',
              'expect': '{"payload.level_info.next_level_more_coin": "1", "payload.reward": "5", "payload.invalid_apprentice_num": "0", "payload.shoutu_v5_3_open": "1"}',
              'fact': '{\n  "err_code": 0, \n  "err_msg": "", \n  "messages": [], \n  "payload": {\n    "ad_tpl": {\n      "action_id": 74, \n      "ad_url": "https://game.baichuanhd.com.cn/show.htm?app_key=a4604da129644ae0", \n      "ext": 6, \n      "img_url": "https://assets.qkcdn.com/images/8be91e6f5f1f8b6754aa33e2bb64fc4a.png", \n      "pos": 99, \n      "sub_title": "每天8次 最高888元", \n      "superscript": "", \n      "title": "红包福利", \n      "type": "juta_ad"\n    }, \n    "app_start": 0, \n    "avatar": "http://assets.qkcdn.com/images/43182fd4080fa912dd0f421158187f0b.png!200x200/rotate/auto", \n    "balance": "0.00", \n    "bind_mobile": 0, \n    "claim_level_coin_open": 1, \n    "clock_countdown_day": 0, \n    "clock_extends": {}, \n    "clock_switch": 0, \n    "coin_balance": "0", \n    "explore_switch": 1, \n    "explore_tags": {\n      "new_tasks": 0, \n      "tasks_reward": 0\n    }, \n    "first_claim": 1, \n    "has_explore_task": 0, \n    "has_finished_task_once": 0, \n    "has_new_tudi": 0, \n    "has_rewarded": 0, \n    "highearn_v5_6_switch": 0, \n    "invalid_apprentice_num": 0, \n    "invite_code": "0", \n    "is_inside": 0, \n    "is_lite": 0, \n    "level_info": {\n      "level": 1, \n      "next_level": 2, \n      "next_level_more_coin": 1, \n      "next_level_more_income": "0.04", \n      "next_level_need": "2.00"\n    }, \n    "msg_num": 0, \n    "need_up_v5": 0, \n    "newyear_activity_switch": 0, \n    "next_level_coin": 8, \n    "nickname": "", \n    "old_user_trial_card_info": {}, \n    "online_reward_open": 0, \n    "open_msg": 1, \n    "qt_sale_switch": 1, \n    "receive_shoutu_income": "0.00", \n    "reward": 5, \n    "reward_by_tudi_num": 0, \n    "reward_coin": 5, \n    "sdj_loan": 1, \n    "shandw_game_switch": 1, \n    "shoutu_v5_3_open": 1, \n    "shoutu_v5_9_open": 1, \n    "thumb_switch": 1, \n    "today_reward": "0.00", \n    "total_reward": "0.00", \n    "trial_card": {}, \n    "tudi_online_num": 0, \n    "tusun_online_num": 0, \n    "uid": 51229992, \n    "webclip": "", \n    "xing_shoutu_switch": 0, \n    "xnhb_show_alert": 0, \n    "xnhb_switch": 0, \n    "yl_article_switch": 1, \n    "yl_huan_info": {\n      "miniprogram_type": 1, \n      "path": "/pages/index%3Fqk_uid%3D51229992%26source%3Dqk%26sign%3D8A25A6E8CC", \n      "username": "gh_3cf20e1090fe", \n      "wx_app_id": ""\n    }, \n    "yydk_switch": 1\n  }\n}',
              'databaseResult': ' ', 'databaseExpect': ' ', 'ispass': 'block', 'time': '2019/03/07 10:11:35',
              'reason': ''},
             {'method': 'get', 'caseId': 3, 'caseDescribe': '试玩赚钱列表，正常请求', 'apiHost': '/s4/lite.subtask.list',
              'apiParams': '', 'expect': '{"err_code": "0", "payload.tasks": "[id=261567]"}',
              'fact': '{"err_code": 0, "err_msg": "", "messages": [], "payload": {"assistant_info": {}, "incoming": [], "tasks": [{"appstore_cost": "0.00", "bid": "com.ios.lsnovel", "icon": "https://upload.qkcdn.com/90f4066130ed581be411b161f98b7eee.jpg", "id": 261567, "is_pay": 0, "is_quality": 0, "qty": 298, "reward": "1.50", "status": 1, "status_for_order": null, "tags": ["\\u5269298\\u4efd"], "title": "\\u8fde***", "type": 1, "zs_reward": "0.00"}, {"appstore_cost": "0.00", "bid": "com.xiaomi.loan", "icon": "https://upload.qkcdn.com/c4b848ad98df77dd6b51a497a9df5d95.jpg", "id": 261568, "is_pay": 0, "is_quality": 0, "qty": 297, "reward": "1.50", "status": 1, "status_for_order": null, "tags": ["\\u5269297\\u4efd"], "title": "\\u5c0f***", "type": 1, "zs_reward": "0.00"}, {"appstore_cost": "0.00", "bid": "com.wbtczufang01.iphone", "icon": "https://upload.qkcdn.com/83a7eded3a24f902b8592f3c87463b66.jpg", "id": 261569, "is_pay": 0, "is_quality": 0, "qty": 292, "reward": "1.50", "status": 1, "status_for_order": null, "tags": ["\\u5269292\\u4efd"], "title": "5***", "type": 1, "zs_reward": "0.00"}, {"appstore_cost": "0.00", "bid": "com.michael.help", "icon": "https://upload.qkcdn.com/0d87c96782f9ff985475409d2fb6a768.jpg", "id": 261564, "is_pay": 0, "is_quality": 0, "qty": 298, "reward": "1.00", "status": 1, "status_for_order": null, "tags": ["\\u5269298\\u4efd"], "title": "\\u83e0***", "type": 1, "zs_reward": "0.00"}, {"appstore_cost": "0.00", "bid": "com.guanglei.LightningBorrow", "icon": "https://upload.qkcdn.com/81cf1a61010e545b0e94bb6222a34a7b.jpg", "id": 261565, "is_pay": 0, "is_quality": 0, "qty": 298, "reward": "1.00", "status": 1, "status_for_order": null, "tags": ["\\u5269298\\u4efd"], "title": "\\u95ea***", "type": 1, "zs_reward": "0.00"}, {"appstore_cost": "0.00", "bid": "com.smart.job", "icon": "https://upload.qkcdn.com/2aca211d344a3808bdca6b3cc5c5e277.jpg", "id": 261566, "is_pay": 0, "is_quality": 0, "qty": 298, "reward": "1.00", "status": 1, "status_for_order": null, "tags": ["\\u5269298\\u4efd"], "title": "\\u76ae***", "type": 1, "zs_reward": "0.00"}], "type": "newbie"}}',
              'databaseResult': ' ', 'databaseExpect': ' ', 'ispass': 'pass', 'time': '2019/03/07 10:11:35',
              'reason': ''},
             {'method': 'get', 'caseId': 4, 'caseDescribe': '创建用户，请求方式为get', 'apiHost': '/s5/create_user',
              'apiParams': '', 'expect': '{"err_code": "405"}',
              'fact': '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>405 Method Not Allowed</title>\n<h1>Method Not Allowed</h1>\n<p>The method is not allowed for the requested URL.</p>\n',
              'databaseResult': ' ', 'databaseExpect': ' ', 'ispass': 'pass', 'time': '2019/03/07 10:11:36',
              'reason': ''},
             {'method': 'post', 'caseId': 5, 'caseDescribe': '创建用户，添加cookie信息', 'apiHost': '/s5/create_user',
              'apiParams': '', 'expect': '{"err_code": "0"}',
              'fact': '{\n  "err_code": 0,\n  "err_msg": "",\n  "messages": [],\n  "payload": {\n    "uid": 51229993\n  }\n}',
              'databaseResult': ' ', 'databaseExpect': ' ', 'ispass': 'pass', 'time': '2019/03/07 10:11:36',
              'reason': ''},
             {'method': 'post', 'caseId': 6, 'caseDescribe': '创建用户，师傅邀请创建', 'apiHost': '/s5/create_user',
              'apiParams': '', 'expect': '{"err_code": "0"}',
              'fact': '{\n  "err_code": 0,\n  "err_msg": "",\n  "messages": [],\n  "payload": {\n    "uid": 51229994\n  }\n}',
              'databaseResult': ' ', 'databaseExpect': ' ', 'ispass': 'pass', 'time': '2019/03/07 10:11:36',
              'reason': ''},
             {'method': 'get', 'caseId': 7, 'caseDescribe': '主页，用户没有领取金币', 'apiHost': '/s5/dashboard', 'apiParams': '',
              'expect': '{"err_code": "0", "payload.first_claim": "1"}',
              'fact': '{\n  "err_code": 0, \n  "err_msg": "", \n  "messages": [], \n  "payload": {\n    "ad_tpl": {\n      "action_id": 74, \n      "ad_url": "https://game.baichuanhd.com.cn/show.htm?app_key=a4604da129644ae0", \n      "ext": 6, \n      "img_url": "https://assets.qkcdn.com/images/8be91e6f5f1f8b6754aa33e2bb64fc4a.png", \n      "pos": 99, \n      "sub_title": "每天8次 最高888元", \n      "superscript": "", \n      "title": "红包福利", \n      "type": "juta_ad"\n    }, \n    "app_start": 0, \n    "avatar": "http://assets.qkcdn.com/images/db99250e5611f108a76c12de7a0364fb.png!200x200/rotate/auto", \n    "balance": "0.00", \n    "bind_mobile": 0, \n    "claim_level_coin_open": 1, \n    "clock_countdown_day": 0, \n    "clock_extends": {}, \n    "clock_switch": 0, \n    "coin_balance": "0", \n    "explore_switch": 1, \n    "explore_tags": {\n      "new_tasks": 0, \n      "tasks_reward": 0\n    }, \n    "first_claim": 1, \n    "has_explore_task": 0, \n    "has_finished_task_once": 0, \n    "has_new_tudi": 0, \n    "has_rewarded": 0, \n    "highearn_v5_6_switch": 0, \n    "invalid_apprentice_num": 0, \n    "invite_code": "0", \n    "is_inside": 0, \n    "is_lite": 0, \n    "level_info": {\n      "level": 1, \n      "next_level": 2, \n      "next_level_more_coin": 1, \n      "next_level_more_income": "0.04", \n      "next_level_need": "2.00"\n    }, \n    "msg_num": 0, \n    "need_up_v5": 0, \n    "newyear_activity_switch": 0, \n    "next_level_coin": 8, \n    "nickname": "", \n    "old_user_trial_card_info": {}, \n    "online_reward_open": 0, \n    "open_msg": 1, \n    "qt_sale_switch": 1, \n    "receive_shoutu_income": "0.00", \n    "reward": 5, \n    "reward_by_tudi_num": 0, \n    "reward_coin": 5, \n    "sdj_loan": 1, \n    "shandw_game_switch": 1, \n    "shoutu_v5_3_open": 1, \n    "shoutu_v5_9_open": 1, \n    "thumb_switch": 1, \n    "today_reward": "0.00", \n    "total_reward": "0.00", \n    "trial_card": {}, \n    "tudi_online_num": 0, \n    "tusun_online_num": 0, \n    "uid": 51229994, \n    "webclip": "", \n    "xing_shoutu_switch": 0, \n    "xnhb_show_alert": 0, \n    "xnhb_switch": 0, \n    "yl_article_switch": 1, \n    "yl_huan_info": {\n      "miniprogram_type": 1, \n      "path": "/pages/index%3Fqk_uid%3D51229994%26source%3Dqk%26sign%3DDBF7BC7146", \n      "username": "gh_3cf20e1090fe", \n      "wx_app_id": ""\n    }, \n    "yydk_switch": 1\n  }\n}',
              'databaseResult': ' ', 'databaseExpect': ' ', 'ispass': 'pass', 'time': '2019/03/07 10:11:37',
              'reason': ''},
             {'method': 'get', 'caseId': 8, 'caseDescribe': '主页，用户领取金币', 'apiHost': '/s5/dashboard', 'apiParams': '',
              'expect': '{"err_code": "0", "payload.first_claim": "0"}',
              'fact': '{\n  "err_code": 0, \n  "err_msg": "", \n  "messages": [], \n  "payload": {\n    "ad_tpl": {\n      "action_id": 74, \n      "ad_url": "https://game.baichuanhd.com.cn/show.htm?app_key=a4604da129644ae0", \n      "ext": 6, \n      "img_url": "https://assets.qkcdn.com/images/8be91e6f5f1f8b6754aa33e2bb64fc4a.png", \n      "pos": 99, \n      "sub_title": "每天8次 最高888元", \n      "superscript": "", \n      "title": "红包福利", \n      "type": "juta_ad"\n    }, \n    "app_start": 0, \n    "avatar": "http://assets.qkcdn.com/images/db99250e5611f108a76c12de7a0364fb.png!200x200/rotate/auto", \n    "balance": "0.00", \n    "bind_mobile": 0, \n    "claim_level_coin_open": 1, \n    "clock_countdown_day": 0, \n    "clock_extends": {}, \n    "clock_switch": 0, \n    "coin_balance": "5", \n    "explore_switch": 1, \n    "explore_tags": {\n      "new_tasks": 0, \n      "tasks_reward": 0\n    }, \n    "first_claim": 0, \n    "has_explore_task": 0, \n    "has_finished_task_once": 0, \n    "has_new_tudi": 0, \n    "has_rewarded": 1, \n    "highearn_v5_6_switch": 0, \n    "invalid_apprentice_num": 0, \n    "invite_code": "0", \n    "is_inside": 0, \n    "is_lite": 0, \n    "level_info": {\n      "level": 1, \n      "next_level": 2, \n      "next_level_more_coin": 1, \n      "next_level_more_income": "0.04", \n      "next_level_need": "2.00"\n    }, \n    "msg_num": 0, \n    "need_up_v5": 0, \n    "newyear_activity_switch": 0, \n    "next_level_coin": 8, \n    "nickname": "", \n    "old_user_trial_card_info": {}, \n    "online_reward_open": 0, \n    "open_msg": 1, \n    "qt_sale_switch": 1, \n    "receive_shoutu_income": "0.00", \n    "reward": 5, \n    "reward_by_tudi_num": 0, \n    "reward_coin": 5, \n    "sdj_loan": 1, \n    "shandw_game_switch": 1, \n    "shoutu_v5_3_open": 1, \n    "shoutu_v5_9_open": 1, \n    "thumb_switch": 1, \n    "today_reward": "0.00", \n    "total_reward": "0.00", \n    "trial_card": {}, \n    "tudi_online_num": 0, \n    "tusun_online_num": 0, \n    "uid": 51229994, \n    "webclip": "", \n    "xing_shoutu_switch": 0, \n    "xnhb_show_alert": 0, \n    "xnhb_switch": 0, \n    "yl_article_switch": 1, \n    "yl_huan_info": {\n      "miniprogram_type": 1, \n      "path": "/pages/index%3Fqk_uid%3D51229994%26source%3Dqk%26sign%3DDBF7BC7146", \n      "username": "gh_3cf20e1090fe", \n      "wx_app_id": ""\n    }, \n    "yydk_switch": 1\n  }\n}',
              'databaseResult': ' ', 'databaseExpect': ' ', 'ispass': 'pass', 'time': '2019/03/07 10:11:37',
              'reason': ''}]
    r = Report()
    r.get_report(r_set)
