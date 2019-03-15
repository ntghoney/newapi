# -*- coding: utf-8 -*-
'''
@File  : send_email.py
@Date  : 2019/3/15/015 15:53
'''
# -*- coding: utf-8 -*-
'''
@File  : sendEmail.py
@Date  : 2019/1/15/015 17:32
'''
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from config.config import RECEIVERS,EMAIL
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from utils.log import log
import os


class __SendEmail(object):
    def __init__(self):
        self.stmp = smtplib.SMTP(EMAIL["server"])
        self.msg = None

    def set_msg(self, text,part_path=None):
        message = MIMEMultipart()
        message.attach(MIMEText(text, 'plain', 'utf-8'))
        message['From'] = Header(EMAIL["msgfrom"], 'gbk')  # 发送者
        subject = EMAIL["subject"]
        message['Subject'] = Header(subject, 'utf-8')
        if not part_path:
            self.msg = message
            return
        for path in part_path:
            fn=os.path.splitext(path)[1]
            if fn ==".xls":
                with open(path,"rb") as f:
                    part=MIMEApplication(f.read())
                    part.add_header('Content-Disposition', 'attachment', filename="测试报告.xls")
                    message.attach(part)
                    f.close()
            elif fn==".html":
                with open(path, "rb") as f:
                    part = MIMEApplication(f.read())
                    part.add_header('Content-Disposition', 'attachment', filename="测试报告.html")
                    message.attach(part)
                    f.close()
            else:
                raise TypeError("%s 文件类型错误"%path)
        self.msg = message

    def send_email(self, sender, recivers):
        self.stmp.login(EMAIL["user"], EMAIL["pwd"])
        self.stmp.sendmail(sender, recivers, self.msg.as_string())


def send_email_for_all(msg,part_path=None):
    """
    群发信息
    :param msg: 正文
    :param part_path:附件地址
    :return:
    """
    try:
        receivers = RECEIVERS
        sender = 'ning.tonggang@qianka.com'
        se = __SendEmail()
        if part_path:
            msg="Dear all,\n  {},详情见附件：".format(msg)
        else:
            msg="Dear all,\n  {}".format(msg)
        se.set_msg(msg,part_path)
        se.send_email(sender, receivers)
        log.info("邮件发送成功。。")
    except Exception as e :
        log.info(e)
        log.error("邮件发送失败。。")

if __name__ == '__main__':
    send_email_for_all("你好",[r"C:\a.html"])