import sys
sys.path.append(r'C:\Users\Administrator\Desktop\AutomatedTesting')
import os
from Conf.readconfig import ReadConfig
from Runner.send_email import send_email
from Runner.test_runner import IEMSRunner


class IEMS_start:
    def run(self):
        IEMSRunner().runner()


if __name__ == '__main__':
    # filename = r'C:\Users\Administrator\Desktop\AutomatedTesting\Results\reports\iems-reports2022-02-21_09-59-23.html'
    # send_email(filename)
    IEMS_start().run()
    file_list = []
    file_path = ReadConfig().get_file_path('report_path')
    for filename in os.listdir(file_path):
        file_list.append(filename)
    send_email(file_path + '/' + file_list[-1])
    # filename = os.path.split(file_path)
    # print(filename)
    # filename = '../Results/reports/*.html'
    # print(filename)

    # a = 'AssertionError'
    # IEMS_start().run()
    # with open(filename, 'r') as foo:
    #     for line in foo.readlines():
    #         if a in line:
    #             attachfilepath = filename
    #             send_email(file=attachfilepath)
    #             print('报告出现fail，请查看邮件！')
    #             break
