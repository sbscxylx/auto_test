import datetime
import os
import logging
import time

from Conf import readconfig
from Conf.readconfig import ReadConfig

# logger = logging.getLogger('Tester')
#
# logger.setLevel('INFO')
#
# fmt = logging.Formatter("%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s")
#
# file_handler = logging.FileHandler('../Log/log')


class Logger():

    log = 'log_' + (time.strftime("%Y-%m-%d%H%M", time.localtime(time.time())) + '.txt').replace('\\', '/')
    log_path = ReadConfig().get_log('log_path')
    log_name = os.path.join(log_path, log)

    def __init__(self):

        self.logger = logging.getLogger('Tester')
        self.log_level = eval(ReadConfig().get_log('log_level'))

        # 设置日志的级别
        self.logger.setLevel((self.log_level))
        # 设置日志的输出格式
        fmt = logging.Formatter("%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s")

        # 借助handle将日志输出到test.log文件中
        fh = logging.FileHandler(self.log_name, encoding="utf-8")
        fh.setLevel(self.log_level)

        fh.setFormatter(fmt)

        # 给logger添加handle
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def rm_log(self, rm_day=1):

        for parent, dirnames, filenames in os.walk(self.log_path):
            for filename in filenames:
                fullname = parent + "/" + filename  # 文件全称
                createTime = int(os.path.getctime(fullname))  # 文件创建时间
                nDayAgo = (datetime.datetime.now() - datetime.timedelta(days=rm_day))  # 当前时间的n天前的时间
                timeStamp = int(time.mktime(nDayAgo.timetuple()))
                if createTime < timeStamp:  # 创建时间在n天前的文件删除
                    os.remove(os.path.join(parent, filename))


if __name__ == "__main__":

    log = Logger()
    #
    # log.info("---测试开始----")
    #
    # log.error("输入密码")
    #
    # log.warn("----测试结束----")

    log.rm_log()