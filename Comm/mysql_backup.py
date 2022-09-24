import paramiko
import pymysql
from sshtunnel import SSHTunnelForwarder
import Comm
from Comm import *


class MysqlConn():

    def __init__(self):

        self.ssh_address = Comm.config.sit_ssh.ssh_address
        self.ssh_host = Comm.config.sit_ssh.ssh_host
        self.ssh_username = Comm.config.sit_ssh.ssh_username
        self.ssh_pwd = Comm.config.sit_ssh.ssh_pwd
        self.remote_bind_address = Comm.config.sit_ssh.remote_bind_address
        self.remote_bind_address_host = Comm.config.sit_ssh.remote_bind_address_host
        self.mysql_user = Comm.config.sit_ssh.mysql_user
        self.mysql_pwd = Comm.config.sit_ssh.mysql_pwd
        self.mysql_host = Comm.config.sit_ssh.mysql_host
        self.mysql_db = Comm.config.sit_ssh.mysql_db
        self.disabled_databases = {'information_schema', 'mysql', 'nacos', 'performance_schema', 'sys', 'xxl_job',
                                   'vx_api_gateway'}
        self.backup_path = Comm.config.sit_ssh.backup_path

    def create_mysql_conn(self):

        server = SSHTunnelForwarder(
            ssh_address_or_host=(self.ssh_address, self.ssh_host),  # 指定ssh登录的跳转机的address
            ssh_username=self.ssh_username,  # 跳转机的用户
            ssh_password=self.ssh_pwd,  # 跳转机的密码
            remote_bind_address=(self.remote_bind_address, self.remote_bind_address_host))
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
        log.Logger().info('开始执行sql语句')
        cursor.execute(sql)
        res = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return res

    # def MysqlConnect(sql):
    #     ssh_address = Readconfig().get_sit_mysql('ssh_address')
    #     ssh_host = readComm.config.ReadComm.config().get_sit_mysql('ssh_host')
    #     ssh_username = readComm.config.ReadComm.config().get_sit_mysql('ssh_username')
    #     ssh_pwd = readComm.config.ReadComm.config().get_sit_mysql('ssh_pwd')
    #     remote_bind_address = readComm.config.ReadComm.config().get_sit_mysql('remote_bind_address')
    #     remote_bind_address_host = readComm.config.ReadComm.config().get_sit_mysql('remote_bind_address_host')
    #     mysql_user = readComm.config.ReadComm.config().get_sit_mysql('mysql_user')
    #     mysql_pwd = readComm.config.ReadComm.config().get_sit_mysql('mysql_pwd')
    #     mysql_host = readComm.config.ReadComm.config().get_sit_mysql('mysql_host')
    #     mysql_db = readComm.config.ReadComm.config().get_sit_mysql('mysql_db')
    #
    #     server = SSHTunnelForwarder(
    #             ssh_address_or_host=(ssh_address, int(ssh_host)),  # 指定ssh登录的跳转机的address
    #             ssh_username=ssh_username,  # 跳转机的用户
    #             ssh_password=ssh_pwd,  # 跳转机的密码
    #             remote_bind_address=(remote_bind_address, int(remote_bind_address_host)))
    #     server.start()
    #     myComm.config = pymysql.connect(
    #         user=mysql_user,
    #         passwd=mysql_pwd,
    #         host=mysql_host,
    #         db=mysql_db,
    #         port=server.local_bind_port,
    #         cursorclass=pymysql.cursors.DictCursor)
    #
    #
    #     # 连接数据库
    #     cursor = myComm.config.cursor()
    #
    #     if sql == None:
    #
    #         # 查询并打印数据
    #         cursor.execute(sql)
    #         myComm.config.commit()
    #
    #
    #     # print(cursor.fetchall())

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

        log.Logger().info('读取全部数据库名称..')
        res = self.mysql_sql(sql='show databases')
        databases = {item['Database'] for item in res}
        databases = list(databases - self.disabled_databases)
        log.Logger().info('读取完毕，数据库列表如下：{}'.format(databases))

        return databases

    def backup_databases(self, tables):
        """
        备份指定数据库的数据和表结构
        :param database: 待备份的数据库名称 iems
        :param table: 待备份的数据库表
        :return:
        """

        database = self.read_all_databases()
        backup_files = []
        channel = self.ssh_connect()
        time.sleep(1)
        rm_file_cmd = f"""
            find {self.backup_path} -mtime +1 -name "*.sql.gz" -exec rm -rf {{}} \;
            """
        channel.send(rm_file_cmd + "\n")
        time.sleep(1)
        log.Logger().info('删除一天前的备份数据')
        for table in tables:
            timestr = time.strftime("%Y%m%d", time.localtime(time.time()))
            backup_file = database[0] + table + timestr
            log.Logger().info(backup_file)
            # backup_cmd = f"mysqldump -u{self.mysql_user} -p --default-character-set=utf8 {database[0]} {table} | gzip > /www/backup/database/{backup_file}.sql.gz"
            backup_cmd = f"mysqldump -p --default-character-set=utf8 {database[0]} {table} | gzip > {self.backup_path}/{backup_file}.sql.gz"
            log.Logger().info(backup_cmd)
            while True:
                channel.send(backup_cmd + "\n")
                time.sleep(1)
                channel.send(self.mysql_pwd + '\n')
                time.sleep(1)
                log.Logger().info('开始备份数据库：{}.表:{}...'.format(database, table))
                rst = channel.recv(1024).decode('utf-8')
                log.Logger().info(rst)
                # time.sleep(10)
                log.Logger().info('数据库：{}.表:{}备份完毕'.format(database, table))
                backup_files.append(backup_file)
                print('数据库：{}.表:{}备份完毕'.format(database, table))
                break
        channel.close()
        log.Logger().info(backup_files)
        return backup_files

    def databases_rm(self):
        """
        删除备份文件
        :param :
        :return:
        """

        channel = self.ssh_connect()
        time.sleep(2)
        rst = channel.recv(1024).decode('utf-8')
        log.Logger().info(rst)
        rm_file_cmd = f"""
            find {self.backup_path} -mtime +1 -name "*.sql.gz" -exec rm -rf {{}} \;
            """
        channel.send(rm_file_cmd + "\n")
        rst = channel.recv(1024).decode('utf-8')
        log.Logger().info(rst)
        log.Logger().info('删除一天前的备份数据')
        channel.close()

    def restore_databases(self, restore_files, wait=8):
        """
        还远数据库表
        :param wait:
        :param database:
        :param restore_files:
        :return:
        """

        restore_path = self.backup_path
        database = self.read_all_databases()
        channel = self.ssh_connect()
        for restore_file in restore_files:
            log.Logger().info('开始还原数据库{}...'.format(database))

            restore_cmd = f"gunzip < {restore_path}/{restore_file}.sql.gz | mysql -u {self.mysql_user} -p {database[0]}"
            log.Logger().info(restore_cmd)
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
    channel = MysqlConn().backup_databases(['bar_project'])

