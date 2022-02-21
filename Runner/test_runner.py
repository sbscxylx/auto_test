import sys
sys.path.append(r'C:\Users\Administrator\Desktop\AutomatedTesting')
import unittest
import os
# from Comm.html_test_runner import HTMLTestRunner
import time

from Comm import HTMLTestReportCN, HwTestReport
from Comm.html_test_runner import HTMLTestRunner
from Runner import send_email


class IEMSRunner:

    def runner(self):
        """收集并运行用例"""

        # 实例化 TestSuite 类，创建测试套件
        suite = unittest.TestSuite()

        # 添加测试用例到测试套件中
        dir = '../IemsTestcase'  # 相对路径

        # suite.addTests(unittest.TestLoader().discover(start_dir=dir,pattern='se1112_case1.py'))
        suite.addTests(unittest.TestLoader().discover(start_dir=dir, pattern='test*.py'))

        # 创建报告文件,b是二进制
        t = time.strftime('%Y-%m-%d_%H-%M-%S')
        report_path = '../Results/reports/iems-reports%s.html' % t

        # 打开文件，把结果写进文件中，w，有内容的话，清空了再写进去
        report_file = open(report_path, 'wb')

        # 实例化HTMLTestRunner类，运行用例和把测试结果写入到报告文件

        # htm_test_runner = HTMLTestRunner(stream=report_file,
        #                                  title='iems系统自动化测试报告',
        #                                  description='报告详细描述',
        #                                  verbosity=2)

        a = HTMLTestReportCN.HTMLTestReportCN(stream=report_file,
                                              title='iems系统自动化测试报告',
                                              description='报告详细描述',
                                              verbosity=2)

        # a = HwTestReport.HTMLTestReport(
        #     stream=report_file,
        #     images=True,
        #     title='iems系统自动化测试报告',
        #     description='报告详细描述',
        #     verbosity=2
        # )

        # 运行用例
        # htm_test_runner.run(suite)
        a.run(suite)

        # 关闭报告文件，如果不关闭有可能会导致报告内容为空
        report_file.close()

        # content = "Hi，你好！请查看接口运行详情。"
        # attachfilepath = report_path
        # send_email(content=content)
        # print('报告出现fail，请查看邮件！')


if __name__ == '__main__':
    IEMSRunner().runner()
