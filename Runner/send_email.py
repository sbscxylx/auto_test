# -*- coding:utf-8 -*-
# @Time    :2021/4/1 15:11
# @Author  :lixin
# @Email   :lix@bbieat.com
# @File    :send_email.PY
import time
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
import pathlib

from Conf.readconfig import ReadConfig


def send_email(file=None):

    # 发件人和密码
    sender = ReadConfig().get_email('sender')
    # password = 'LX151020*'
    password = ReadConfig().get_email('password')
    receiver = ReadConfig().get_email('receiver')

    # 邮件服务器
    imapserver = 'smtp.163.com'
    content = '自动化测试报告'

    if file:
        msg = MIMEMultipart()

        # 构建正文
        part_text = MIMEText(content, 'html', 'utf-8')
        msg.attach(part_text) # 把正文加到邮件体里面去

        # 构建邮件附件
        part_attach1 = MIMEApplication(open(file, 'rb').read())  # 打开附件
        part_attach1.add_header('Content-Disposition', 'attachment', filename=pathlib.Path(file).name)  # 为附件命名
        msg.attach(part_attach1)  # 添加附件

    else:
        msg = MIMEText(content)  # 邮件内容
    msg['Subject'] = '自动化测试报告'  # 邮件主题
    msg['From'] = Header('测试机<{}>'.format(sender))  # 发送者账号
    msg['To'] = Header('测试负责人<{}>'.format(receiver))  # 接收者账号列表
    smtp = smtplib.SMTP(imapserver, port=25)
    smtp.login(sender, password)  # 登录
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


if __name__ == '__main__':

    file_path = r'C:\Users\Administrator\Desktop\AutomatedTesting\Results\reports\iems-reports2022-02-21_09-59-23.html'
    send_email(file_path)


