# -*- coding: utf-8 -*-
# @Time    : 2020/5/19 下午5:23
# @Author  : Danny
# @File    : Email.py

"""
封装发送邮件的方法

"""

import yagmail


# 把测试报告作为附件发送到指定邮箱
def send_mail(reports):
    yag = yagmail.SMTP(user="xiaoxinxing@aliyun.com", password="Abc09292752", host='smtp.aliyun.com')

    # 发送邮件主题
    subject = '币易自动化测试报告'

    # 邮箱正文
    contents = ['正文，请查看附件。']
    # 发送邮件
    yag.send('620700065@qq.com', subject, contents, reports)


