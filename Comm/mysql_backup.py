import datetime
import re
import time

import paramiko
import pymysql
from sshtunnel import SSHTunnelForwarder
from Comm.log import Logger
from Conf.readconfig import ReadConfig


class MysqlConn():

    def __init__(self):
        self.ssh_address = ReadConfig().get_sit_mysql('ssh_address')
        self.ssh_host = int(ReadConfig().get_sit_mysql('ssh_host'))
        self.ssh_username = ReadConfig().get_sit_mysql('ssh_username')
        self.ssh_pwd = ReadConfig().get_sit_mysql('ssh_pwd')
        self.remote_bind_address = ReadConfig().get_sit_mysql('remote_bind_address')
        self.remote_bind_address_host = int(ReadConfig().get_sit_mysql('remote_bind_address_host'))
        self.mysql_user = ReadConfig().get_sit_mysql('mysql_user')
        self.mysql_pwd = ReadConfig().get_sit_mysql('mysql_pwd')
        self.mysql_host = ReadConfig().get_sit_mysql('mysql_host')
        self.mysql_db = ReadConfig().get_sit_mysql('mysql_db')
        # self.disabled_databases = ReadConfig().get_sit_mysql('disabled_databases')
        self.disabled_databases = {'information_schema', 'mysql', 'nacos', 'performance_schema', 'sys', 'xxl_job', 'vx_api_gateway'}
        self.backup_path = 'backup'


    def create_mysql_conn(self):

        server = SSHTunnelForwarder(
            ssh_address_or_host=(self.ssh_address, int(self.ssh_host)),  # 指定ssh登录的跳转机的address
            ssh_username=self.ssh_username,  # 跳转机的用户
            ssh_password=self.ssh_pwd,  # 跳转机的密码
            remote_bind_address=(self.remote_bind_address, int(self.remote_bind_address_host)))
        server.start()
        conn = pymysql.connect(
            user=self.mysql_user,
            passwd=self.mysql_pwd,
            host=self.mysql_host,
            db=self.mysql_db,
            port=server.local_bind_port,
            cursorclass=pymysql.cursors.DictCursor)

        return conn


    def mysql_sql(self, sql):
        """
        连接后可执行sql语句
        :param sql:
        :return: res
        """

        conn = MysqlConn().create_mysql_conn()
        cursor = conn.cursor()
        Logger().info('开始执行sql语句')
        cursor.execute(sql)
        res = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return res


    def MysqlConnect(sql):
        ssh_address = ReadConfig().get_sit_mysql('ssh_address')
        ssh_host = ReadConfig().get_sit_mysql('ssh_host')
        ssh_username = ReadConfig().get_sit_mysql('ssh_username')
        ssh_pwd = ReadConfig().get_sit_mysql('ssh_pwd')
        remote_bind_address = ReadConfig().get_sit_mysql('remote_bind_address')
        remote_bind_address_host = ReadConfig().get_sit_mysql('remote_bind_address_host')
        mysql_user = ReadConfig().get_sit_mysql('mysql_user')
        mysql_pwd = ReadConfig().get_sit_mysql('mysql_pwd')
        mysql_host = ReadConfig().get_sit_mysql('mysql_host')
        mysql_db = ReadConfig().get_sit_mysql('mysql_db')

        server = SSHTunnelForwarder(
                ssh_address_or_host=(ssh_address, int(ssh_host)),  # 指定ssh登录的跳转机的address
                ssh_username=ssh_username,  # 跳转机的用户
                ssh_password=ssh_pwd,  # 跳转机的密码
                remote_bind_address=(remote_bind_address, int(remote_bind_address_host)))
        server.start()
        myConfig = pymysql.connect(
            user=mysql_user,
            passwd=mysql_pwd,
            host=mysql_host,
            db=mysql_db,
            port=server.local_bind_port,
            cursorclass=pymysql.cursors.DictCursor)


        # 连接数据库
        cursor = myConfig.cursor()

        if sql == None:

            # 查询并打印数据
            cursor.execute(sql)
            myConfig.commit()


        # print(cursor.fetchall())


    def ssh_transport(self):
        """

        :return:
        """
        transport = paramiko.Transport((self.ssh_address, self.ssh_host))  # s.set_missing_host_key_policy()
        transport.connect(username=self.ssh_username, password=self.ssh_pwd)
        return transport


    def ssh_connect(self):
        """
        连接sit，ssh
        :return:channel
        """

        transport = self.ssh_transport()
        ssh = paramiko.SSHClient()
        ssh._transport = transport
        channel = ssh.invoke_shell(width=1024, height=100)
        return channel


    def ssh_sftp(self, linux_path):
        """
        获取linux文件
        :param linux_path:
        :return:
        """

        transport = self.ssh_transport()
        sftp_client = paramiko.SFTPClient.from_transport(transport)
        remote_file = sftp_client.listdir(linux_path)
        return remote_file


    def read_all_databases(self):
        """
        从数据库中读取全部数据库名称
        :return:
            list,数据库名称列表
        """

        Logger().info('读取全部数据库名称..')
        res = self.mysql_sql(sql='show databases')
        databases = {item['Database'] for item in res}
        databases = list(databases - self.disabled_databases)
        Logger().info('读取完毕，数据库列表如下：{}'.format(databases))

        return databases


    def backup_databases2(self, database, tables):
        """
        备份指定数据库的数据和表结构
        :param database: 待备份的数据库名称 iems
        :param table: 待备份的数据库表
        :return:
        """

        channel = self.ssh_connect()
        for table in tables:
            timestr = time.strftime("%Y%m%d", time.localtime(time.time()))
            backup_file = database[0] + table + timestr
            Logger().info(backup_file)
            # backup_cmd = f"mysqldump -u{self.mysql_user} -p --default-character-set=utf8 {database[0]} {table} | gzip > /www/backup/database/{backup_file}.sql.gz"
            backup_cmd = f"mysqldump -p --default-character-set=utf8 {database[0]} {table} | gzip > /www/backup/database/{backup_file}.sql.gz"
            Logger().info(backup_cmd)
            while True:
                time.sleep(1)
                rst = channel.recv(1024).decode('utf-8')
                Logger().info(rst)
                if 'Last login' in rst:
                    channel.send(backup_cmd + "\n")
                    time.sleep(1)
                    rst2 = channel.recv(1024).decode('utf-8')
                    Logger().info(rst2 + '2')
                    if 'Enter password' in rst2:
                        channel.send(self.mysql_pwd + '\n')
                        time.sleep(1)
                        Logger().info('输入密码{}'.format(self.mysql_pwd))
                        print('输入数据库密码....')
                        rst3 = channel.recv(1024).decode('utf-8')
                        if 'error' in rst3:
                            Logger().info('数据库密码错误，备份失败')
                            break
                        Logger().info('开始备份数据库：{}.表:{}...'.format(database, table))
                        print("开始备份....")
                        time.sleep(10)
                        # rst4 = channel.recv(1024).decode('utf-8')
                        # print(rst4)
                        # Logger().info(rst4)
                        Logger().info('数据库：{}.表:{}备份完毕'.format(database, table))
                        print("备份完成....")
                        break
                        # if 'password' not in rst4:
                        #     Logger().info('数据库：{}.表:{}备份完毕'.format(database, table))
                        #     print("备份成功....")
                        #     break
                        # else:
                        #     Logger().info('备份失败')
                        #     print("备份失败")
                        #     break
                else:
                    channel.send(backup_cmd + "\n")
                    time.sleep(1)
                    rst2 = channel.recv(1024).decode('utf-8')
                    Logger().info(rst2 + '2')
                    if 'Enter password' in rst2:
                        channel.send(self.mysql_pwd + '\n')
                        time.sleep(1)
                        Logger().info('输入密码{}'.format(self.mysql_pwd))
                        print('输入数据库密码....')
                        rst3 = channel.recv(1024).decode('utf-8')
                        if 'error' in rst3:
                            Logger().info('数据库密码错误，备份失败')
                            break
                        Logger().info('开始备份数据库：{}.表:{}...'.format(database, table))
                        print("开始备份....")
                        time.sleep(10)
                        # rst4 = channel.recv(1024).decode('utf-8')
                        # print(rst4)
                        # Logger().info(rst4)
                        Logger().info('数据库：{}.表:{}备份完毕'.format(database, table))
                        print("备份完成....")
                        break
        channel.close()


    def backup_databases(self, database, tables):
        """
        备份指定数据库的数据和表结构
        :param database: 待备份的数据库名称 iems
        :param table: 待备份的数据库表
        :return:
        """
        self.databases_rm()
        backup_files = []
        channel = self.ssh_connect()
        for table in tables:
            timestr = time.strftime("%Y%m%d", time.localtime(time.time()))
            backup_file = database[0] + table + timestr
            Logger().info(backup_file)
            # backup_cmd = f"mysqldump -u{self.mysql_user} -p --default-character-set=utf8 {database[0]} {table} | gzip > /www/backup/database/{backup_file}.sql.gz"
            backup_cmd = f"mysqldump -p --default-character-set=utf8 {database[0]} {table} | gzip > /www/backup/database/{backup_file}.sql.gz"
            Logger().info(backup_cmd)
            while True:
                channel.send(backup_cmd + "\n")
                time.sleep(1)
                channel.send(self.mysql_pwd + '\n')
                time.sleep(1)
                Logger().info('开始备份数据库：{}.表:{}...'.format(database, table))
                rst = channel.recv(1024).decode('utf-8')
                Logger().info(rst)
                # time.sleep(10)
                Logger().info('数据库：{}.表:{}备份完毕'.format(database, table))
                backup_files.append(backup_file)
                print('数据库：{}.表:{}备份完毕'.format(database, table))
                break
        channel.close()
        Logger().info(backup_files)
        return backup_files

    def databases_rm(self, linuxPath='/www/backup/database', rm_time='atime +1'):
        """
        删除备份文件
        :param linuxPath: 路径
        :param rm_time: 日期格式“amin +10”, "atime +1"
        :return:
        """

        channel = self.ssh_connect()
        channel.send('cd {}'.format(linuxPath) + '\n')
        time.sleep(1)
        channel.send('find . -a{} -name "*.sql.gz"'.format(rm_time) + "\n")
        time.sleep(1)
        rst = channel.recv(1024).decode('utf-8')
        Logger().info('删除备份文件{}'.format(rst))
        time.sleep(1)
        channel.send('find . -a{} -name "*.sql.gz" -delete'.format(rm_time) + '\n')


    def restore_databases(self, database, restore_files, wait=8):
        """
        还远数据库表
        :param wait:
        :param database:
        :param restore_files:
        :return:
        """

        # timestr = time.strftime("%Y%m%d", time.localtime(time.time()))
        # restore_file = database[0] + timestr
        # print(restore_file)
        channel = self.ssh_connect()
        for restore_file in restore_files:
            Logger().info('开始还原数据库{}...'.format(database))

            restore_cmd = f"gunzip < /www/backup/database/{restore_file}.sql.gz | mysql -u {self.mysql_user} -p {database[0]}"
            Logger().info(restore_cmd)
            channel.send(restore_cmd + "\n")
            time.sleep(1)
            channel.send(self.mysql_pwd + "\n")
            time.sleep(wait)
            print('还原数据库{}完毕...'.format(restore_file))
        channel.close()



if __name__ == '__main__':

    #
    # sql = '''INSERT INTO `iems`.`col_task_202202`(`meter_no`, `bar_project_id`, `gmt_create`, `sjsj`, `yxzt`, `sjzt`,
    # `jdqzt`, `axdy`, `bxdy`, `cxdy`, `axdl`, `bxdl`, `cxdl`, `sydl`, `zyggl`, `axyggl`, `bxyggl`, `cxyggl`, `zwggl`,
    #  `axwggl`, `bxwggl`, `cxwggl`, `zglys`, `axglys`, `bxglys`, `cxglys`, `zxygzdl`, `zxygzdl1`, `zxygzdl2`, `zxygzdl3`,
    #  `zxygzdl4`, `axwd`, `bxwd`, `cxwd`, `lxwd`, `hjwd`, `is_use`) VALUES ('202104200001', 202104200000000001,
    #  '2022-02-23 01:15:00', '2022-02-23 01:15:00', '00000000', NULL, '00120001', 236.5204, 238.5177, 239.2274,
    #   1.5546, 0.6774, 1.8485, 0.0000, 0.8310, 0.2918, 0.8360, 0.6681, 1.1330, 0.4805, 0.1126, 1.1947, 0.8393,
    #   1.6216, 0.8603, 0.5334, 485, 120, 120, 125, 120, NULL, NULL, NULL, NULL, NULL, 1);'''
    #
    # sql2 = '''INSERT INTO `iems`.`col_task_202202`(`meter_no`, `bar_project_id`, `gmt_create`, `sjsj`, `yxzt`, `sjzt`,
    # `jdqzt`, `axdy`, `bxdy`, `cxdy`, `axdl`, `bxdl`, `cxdl`, `sydl`, `zyggl`, `axyggl`, `bxyggl`, `cxyggl`, `zwggl`,
    #  `axwggl`, `bxwggl`, `cxwggl`, `zglys`, `axglys`, `bxglys`, `cxglys`, `zxygzdl`, `zxygzdl1`, `zxygzdl2`, `zxygzdl3`,
    #  `zxygzdl4`, `axwd`, `bxwd`, `cxwd`, `lxwd`, `hjwd`, `is_use`) VALUES ('202105100012', 202104200000000001,
    #  '2022-02-28 01:15:00', '2022-02-28 01:15:00', '00000000', NULL, '00120001', 236.5204, 238.5177, 239.2274,
    #   1.5546, 0.6774, 1.8485, 0.0000, 0.8310, 0.2918, 0.8360, 0.6681, 1.1330, 0.4805, 0.1126, 1.1947, 0.8393,
    #   1.6216, 0.8603, 0.5334, 84, 84, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1);'''

    # databases = MysqlConn().read_all_databases()
    # backup_files = MysqlConn().backup_databases(databases, ['wx_user', 'sys_user'])
    # MysqlConn().restore_databases(databases, backup_files)
    MysqlConn().databases_rm('/www/backup/database', 'min +1')