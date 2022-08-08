import sys
sys.path.append(r'C:\Users\Administrator\Desktop\UIAutoTest')
import os
from Conf.readconfig import ReadConfig
from Runner.send_email import send_email
from Runner.test_runner import IEMSRunner


class IEMS_start:
    def run(self, flag='no'):
        IEMSRunner().runner()
        file_path = ReadConfig().get_file_path('report_path')
        file_name = os.listdir(file_path)[-1]
        file = os.path.join(file_path, file_name)
        if flag == 'send':
            send_email(file)


if __name__ == '__main__':
    IEMS_start().run()