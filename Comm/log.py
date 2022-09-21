import Comm
from Comm.get_path import ensure_path_sep
import logging


class Logger():

    if not Comm.os.path.exists(ensure_path_sep('/Log/log')):
        Comm.os.makedirs(ensure_path_sep('/Log/log'))
    log = 'log_' + (Comm.time.strftime("%Y-%m-%d%H%M", Comm.time.localtime(Comm.time.time())) + '.txt').replace('\\', '/')
    log_name = Comm.os.path.join(ensure_path_sep('/Log/log'), log)

    def __init__(self):

        self.logger = logging.getLogger('Tester')
        self.log_level = eval(Comm.config.log.log_level)

        # 设置日志的级别
        self.logger.setLevel((self.log_level))
        # 设置日志的输出格式
        fmt = logging.Formatter("%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s")

        # 借助handle将日志输出到test.log文件中
        fh = logging.FileHandler(r'{}'.format(self.log_name), encoding="utf-8")
        fh.setLevel(self.log_level)

        fh.setFormatter(fmt)

        # 给logger添加handle
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.rm_log()
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def rm_log(self, rm_day=1):

        try:
            for parent, dirnames, filenames in Comm.os.walk(Comm.get_path.ensure_path_sep('/Log/log')):
                for filename in filenames:
                    fullname = parent + "/" + filename  # 文件全称
                    createTime = int(Comm.os.path.getctime(fullname))  # 文件创建时间
                    nDayAgo = (Comm.datetime.datetime.now() - Comm.datetime.timedelta(days=rm_day))  # 当前时间的n天前的时间
                    timeStamp = int(Comm.time.mktime(nDayAgo.timetuple()))
                    if createTime < timeStamp:  # 创建时间在n天前的文件删除
                        Comm.os.remove(Comm.os.path.join(parent, filename))
        except:
            print('没有可删除日志')


if __name__ == "__main__":
    log = Logger()
    #
    log.info("---测试开始----")
    #
    # log.error("输入密码")
    #
    # log.warn("----测试结束----")

    # log.rm_log()
