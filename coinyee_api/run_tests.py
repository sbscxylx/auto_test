#!/usr/bin/python
# -*- coding: UTF-8 _*_

import pytest, time, yagmail, click
from conftest import rerun, cases_path
from common.emails import send_mail


# jenkins解析编码
# import sys, io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")


@click.command()
@click.option('-m', default=None, help='输入运行模式：run或debug')
def run(m):
    if m is None or m == "run":
        print("回归模式，执行完成，生成测试结果")

        # 生成HTML,xml格式的报告
        # 获取当前时间
        now_time = time.strftime("%Y-%m-%d %H_%M_%S")
        html_report = './test_report/' + now_time + ' test_report.html'
        xml_report = './test_report/' + now_time + ' test_report.xml'
        fp1 = open(html_report, 'wb')
        fp2 = open(xml_report, 'wb')

        pytest.main(['-s', '-v', cases_path, '--html=' + html_report, '--junit-xml=' + xml_report,
                     '--self-contained-html', '--reruns', rerun, '--reruns-delay', '1'])

        fp1.close()
        fp2.close()

        # 发送邮件
        reports = [html_report, xml_report]
        send_mail(reports)

    elif m == "debug":
        print("debug模式运行测试用例：")
        pytest.main(["-v", "-s", cases_path])
        print("运行结束")



if __name__ == '__main__':
    run()


