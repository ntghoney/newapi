# -*- coding: utf-8 -*-
'''
@File  : html_report.py
@Date  : 2019/3/6/006 17:43
'''
import os
from utils.log import get_now
from config.config import PRODIR

titles = '接口测试'

STYLE = '''
 <style type="text/css">
        .hidden-detail, .hidden-tr {
            display: none;
        }
        table{
            width: 100%;
        }
        a{
            color: darkcyan;
            text-underline: none;
        }
        .tr_sign {
            background: grey;
        }

        #result_table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        #result_table th,#result_table td{
            padding: 8px;
            line-height: 20px;
            text-align: left;
            border: 1px solid #ddd;
            width: 100px;
            white-space: nowrap;
            text-overflow: ellipsis;
            overflow: hidden;
        }
        .tr_success{
            background:#fff;
        }
        .tr_block{
            background: darkgray;
        }
        .tr_fail{
            background: lightgrey;
        }
        .table {
            width: 100%;
            margin-bottom: 20px
        }

        .table th, .table td {
            padding: 8px;
            line-height: 20px;
            text-align: left;
            border-top: 1px solid #ddd
        }

        .table th {
            font-weight: bold
        }


        .div_top {
            width: 41.66666667%;
            margin-top: 56px;
            margin-left: 45px;
        }

        .div_content {
            margin-top: 1px;
            margin-left: 45px;
            margin-right: 45px;
        }

        .button {
            display: inline-block;
            margin-bottom: 0;
            font-weight: normal;
            text-align: center;
            vertical-align: middle;
            -ms-touch-action: manipulation;
            touch-action: manipulation;
            cursor: pointer;
            background-image: none;
            border: 1px solid transparent;
            white-space: nowrap;
            padding: 8px 12px;
            font-size: 15px;
            line-height: 1.4;
            border-radius: 14px;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none
        }

        .btns {
            position: relative;
            display: inline-block;
            *display: inline;
            *margin-left: .3em;
            font-size: 0;
            white-space: nowrap;
            vertical-align: middle;
            *zoom: 1
        }

        .button-primary {
            -webkit-background-size: 200% 200%;
            background-size: 200%;
            background-position: 50%
        }

        .button-primary {
            -webkit-background-size: 200% 200%;
            background-size: 200%;
            background-position: 50%;
            background-color: #2196f3
        }

        .button-primary:focus {
            background-color: #2196f3
        }

        .button-primary:hover, .button-primary:active:hover {
            background-color: #0d87e9
        }

        .button-primary:active {
            background-color: #0b76cc;
            background-image: -webkit-radial-gradient(circle, #0b76cc 10%, #2196f3 11%);
            background-image: -o-radial-gradient(circle, #0b76cc 10%, #2196f3 11%);
            background-image: radial-gradient(circle, #0b76cc 10%, #2196f3 11%);
            background-repeat: no-repeat;
            -webkit-background-size: 1000% 1000%;
            background-size: 1000%;
            -webkit-box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
            box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4)
        }

        .button-success {
            -webkit-background-size: 200% 200%;
            background-size: 200%;
            background-position: 50%;
            background-color: #4caf50
        }

        .button-success:focus {
            background-color: #4caf50
        }

        .button-success:hover, .btn-success:active:hover {
            background-color: #439a46
        }

        .button-success:active {
            background-color: #39843c;
            background-image: -webkit-radial-gradient(circle, #39843c 10%, #4caf50 11%);
            background-image: -o-radial-gradient(circle, #39843c 10%, #4caf50 11%);
            background-image: radial-gradient(circle, #39843c 10%, #4caf50 11%);
            background-repeat: no-repeat;
            -webkit-background-size: 1000% 1000%;
            background-size: 1000%;
            -webkit-box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
            box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4)
        }

        .button_block {
            -webkit-background-size: 200% 200%;
            background-size: 200%;
            background-position: 50%;
            background-color: #ff9800
        }

        .button_block:focus {
            background-color: #ff9800
        }

        .button_block:hover, .btn-warning:active:hover {
            background-color: #e08600
        }

        .button_block:active {
            background-color: #c27400;
            background-image: -webkit-radial-gradient(circle, #c27400 10%, #ff9800 11%);
            background-image: -o-radial-gradient(circle, #c27400 10%, #ff9800 11%);
            background-image: radial-gradient(circle, #c27400 10%, #ff9800 11%);
            background-repeat: no-repeat;
            -webkit-background-size: 1000% 1000%;
            background-size: 1000%;
            -webkit-box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
            box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4)
        }

        .button_fail {
            -webkit-background-size: 200% 200%;
            background-size: 200%;
            background-position: 50%;
            background-color: #e51c23
        }

        .button_fail:focus {
            background-color: #e51c23
        }

        .button_fail:hover, .btn-danger:active:hover {
            background-color: #cb171e
        }

        .button_fail:active {
            background-color: #b0141a;
            background-image: -webkit-radial-gradient(circle, #b0141a 10%, #e51c23 11%);
            background-image: -o-radial-gradient(circle, #b0141a 10%, #e51c23 11%);
            background-image: radial-gradient(circle, #b0141a 10%, #e51c23 11%);
            background-repeat: no-repeat;
            -webkit-background-size: 1000% 1000%;
            background-size: 1000%;
            -webkit-box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
            box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4)
        }

    </style>
'''

H_SIGN = '''<div class="div_content">
                <div>
                    <div class="btns" role="group" aria-label="...">
                        <button type="button" id="check-all" class="button button-primary">所有用例</button>
                        <button type="button" id="check-success" class="button button-success">成功用例</button>
                        <button type="button" id="check-fail" class="button button_fail">失败用例</button>
                        <button type="button" id="check-block" class="button button_block">阻塞用例</button>
                    </div>
                    <!--<div class="btn-group" role="group" aria-label="...">-->
                    <!--</div>-->
                    <table id="result_table">
                        <tr>
                            <td class="tr_sign"><strong>用例ID&nbsp;</strong></td>
                            <td class="tr_sign"><strong>描述</strong></td>
                            <td class="tr_sign"><strong>url</strong></td>
                            <td class="tr_sign"><strong>请求方式</strong></td>
                            <td class="tr_sign"><strong>参数</strong></td>
                            <td class="tr_sign"><strong>预期结果</strong></td>
                            <td class="tr_sign"><strong>实际结果</strong></td>
                            <td class="tr_sign"><strong>sql查询结果</strong></td>
                            <td class="tr_sign"><strong>sql查询期望</strong></td>
                            <td class="tr_sign"><strong>测试判定</strong></td>
                            <td class="tr_sign"><strong>测试时间</strong></td>
                            <td class="tr_sign"><strong>失败原因</strong></td>
                        </tr>
        '''

SCRIPT = """
      <script src="https://code.jquery.com/jquery.js"></script>
        <script src="https://cdn.bootcss.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
        <script type="text/javascript">
            $("#result_table td").each(function (i) {
                var text = $(this).text();
                //获取td当前对象的文本,如果长度大于5;
                if (text.length > 50) {
                    //给td设置title属性,并且设置td的完整值.给title属性.
                    $(this).attr("title", $(this).text());
                    var showText = text.substring(0, 50);
                    var hidderText = text.substring(50, text.length );
                    var newText = $(this).text().substring(0, 50) + "<span>...</span><span style='display:none;'>" + 
                    hidderText + "</span><br><a>显示全部</a>";
                    //重新为td赋值;
                    $(this).html(newText);
                }
            });
            $("#result_table td a").each(function (i) {
                $(this).click(function () {
                    var text = $(this).text();
                    if ("显示全部" === text) {
                        $(this).prev().prev().prev().hide();
                        $(this).prev().prev().show();
                        $(this).text("收起");
                    }
                    if ("收起" === text) {
                        $(this).prev().prev().prev().show()
                        $(this).prev().prev().hide();
                        $(this).text("显示全部");
                    }
                });
            });
            $("#check-all").click(function (e) {
                $(".tr_success").show();
                $(".tr_block").show();
                $(".tr_fail").show();
            });
            $("#check-success").click(function (e) {
                $(".tr_success").show();
                $(".tr_block").hide();
                $(".tr_fail").hide();
            });
            $("#check-fail").click(function (e) {
                $(".tr_success").hide();
                $(".tr_block").hide();
                $(".tr_fail").show();
            });
           $("#check-block").click(function (e) {
                $(".tr_success").hide();
                $(".tr_block").show();
                $(".tr_fail").hide();
            });
        </script>
    """


def html_head(titles):
    title = '''
                <title>%s</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                %s
           ''' % (titles, STYLE)
    return title


def test_describe(total, starttime, endtime, during, passd, fail, block):
    text = """
            <div class='div_top'>
        <h1>接口测试结果</h1>
        <table class="table">
            <tbody>
            <tr>
                <td><strong>开始时间:%(starttime)s</td>
            </tr>
            <td><strong>结束时间:</strong> %(endtime)s</td>
            </tr>
            <td><strong>耗时:</strong> %(during)s</td>
            </tr>
            <td>
                <strong>结果:</strong>
                <span>总共:
                <strong>%(total)s</strong>
                <span>通过:
                <strong>%(passd)s</strong>
                失败:
                <strong>%(fail)s</strong>
                阻塞:
                <strong>%(block)s</strong>
            </td>
            </tbody>
        </table>
    </div>
        """ % {
        "starttime": starttime,
        "endtime": endtime,
        "during": during,
        "passd": passd,
        "fail": fail,
        "total": total,
        "block": block
    }
    return text

def test_detail(*details):
    """
    测试结果明细
    :param details:
    :return:
    """
    s = """"""
    for detail in details:
        middle = '''
               <td>{caseId}</td>
               <td>{caseDescribe}</td>
               <td>{apiHost}</td>
               <td>{method}</td>
               <td>{apiParams}</td>
               <td>{expect}</td>
               <td>{fact}</td>
               <td>{databaseResult}</td>
               <td>{databaseExpect}</td>
            '''.format(**detail)
        if detail["ispass"] == 'pass':
            start = '<tr class="tr_success ">'
            td_pass = ' <td bgcolor="green">pass</td>'
        elif detail["ispass"] == 'fail':
            start = '<tr class="tr_fail ">'
            td_pass = ' <td bgcolor="fail">fail</td>'
        else:
            start = '<tr class="tr_block ">'
            td_pass = '<td bgcolor="#8b0000">block</td>'
        end = '''
               <td>{time}</td>
               <td>{reason}</td>
           </tr>
            '''.format(**detail)
        s += start + middle + td_pass + end
    return s + "\n</table></div></div>"


def html_body(total, starttime, endtime, during, passd, fail, block, titles, details):
    h_head = html_head(titles)
    text = """
            <!DOCTYPE html>
            <html>
                <head>
                    %(head)s
                </head>
                <body>
                    %(describe)s
                    %(sign)s
                    %(details)s
                    %(script)s
                </body>
            </html>
        """ % {
                "head": h_head,
                "describe": test_describe(
                    total=total,
                    starttime=starttime,
                    endtime=endtime,
                    during=during,
                    passd=passd,
                    fail=fail,
                    block=block
                ),
                "details":test_detail(*details),
                "script":SCRIPT,
                "sign":H_SIGN
             }
    report_name="%s接口自动化测试报告.html"%get_now().strftime("%Y%m%d")
    report_path=os.path.abspath(os.path.join(PRODIR,"report/%s"%report_name))
    with open(report_path,"w",encoding="utf8") as f:
        f.write(text)
        f.close()
    return report_path

if __name__ == '__main__':
    # s = test_detail(*[{"id": "1", "url": "www.baidu.com"}, {"id": "1", "url": "www.baidu.com"}])
    # print(s)
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
    html_body("5","2001/01/01",endtime="2001/01/01",during="1",passd=4,fail=4,block=4,titles="sss",details=r_set)
