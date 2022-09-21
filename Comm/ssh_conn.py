from Comm import *
import paramiko


def sshclient_execmd():

    hostname = '47.110.48.39'
    port = 22
    username = 'root'
    password = 'sit@bbieat.com@123!'

    paramiko.util.log_to_file("paramiko.log")

    s = paramiko.SSHClient()    # s.set_missing_host_key_policy()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        s.connect(hostname=hostname, port=port, username=username, password=password)
    except:
        raise Exception
    s.invoke_shell('cd /')
    s.invoke_shell("mysqldump -u root -p --default-character-set=utf8 iems wx_user > /www/backup/database/wx_user.sql")
    s.exec_command('cd /')
    s.exec_command("mysqldump -u root -p --default-character-set=utf8 iems wx_user > /www/backup/database/wx_user.sql")
    # stdin.write("")



    # stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.

    # print(stdout.read())

    # s.close()
# mysql -h -u root -p f0744af873317d5e

def transport_execmd():

    hostname = '47.110.48.39'
    port = 22
    username = 'root'
    password = 'sit@bbieat.com@123!'

    paramiko.util.log_to_file("paramiko.log")

    transport = paramiko.Transport((hostname, port))    # s.set_missing_host_key_policy()
    transport.connect(username=username, password=password)
    ssh = paramiko.SSHClient()
    ssh._transport = transport

    # try:
    #     s.connect(hostname=hostname, port=port, username=username, password=password)
    # except:
    #     raise Exception
    # s.invoke_shell('cd /')
    # ssh.exec_command('mysql -u root -p')
    ssh.exec_command(
        "mysqldump -u root -p --default-character-set=utf8 iems wx_user > /www/backup/database/wx_user.sql")

    # stdin.write('f0744af873317d5e')
    # ssh.exec_command('f0744af873317d5e')
    # print(stdout.read().decode())

    # s.invoke_shell("mysqldump -u root -p --default-character-set=utf8 iems wx_user > /www/backup/database/wx_user.sql")

    # stdin.write("")

    # transport.close()



    # stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.

    # print(stdout.read())

    # s.close()


def transport_shell():

    hostname = '47.110.48.39'
    port = 22
    username = 'root'
    password = 'sit@bbieat.com@123!'

    paramiko.util.log_to_file("paramiko.log")

    transport = paramiko.Transport((hostname, port))  # s.set_missing_host_key_policy()
    transport.connect(username=username, password=password)
    ssh = paramiko.SSHClient()
    ssh._transport = transport

    channel = ssh.invoke_shell(width=1024, height=100)
    cmd = "mysqldump -u root -p --default-character-set=utf8 iems bar_measure mbr_cons_energy_order mbr_cons_order_consume > /www/backup/database/iems_test.sql"
    channel.send(cmd + "\n")
    while True:
        time.sleep(1)
        rst = channel.recv(1024).decode('utf-8')
        print(rst)
        if 'password' in rst:
            channel.send('f0744af873317d5e\n')
            time.sleep(1)
            ret = channel.recv(1024).decode('utf-8')
            print(ret)
            break

    # s.close()


def transport_shell2():

    hostname = '47.110.48.39'
    port = 22
    username = 'root'
    password = 'sit@bbieat.com@123!'

    paramiko.util.log_to_file("paramiko.log")

    transport = paramiko.Transport((hostname, port))  # s.set_missing_host_key_policy()
    transport.connect(username=username, password=password)
    ssh = paramiko.SSHClient()
    ssh._transport = transport

    channel = ssh.invoke_shell(width=1024, height=100)
    cmd = "mysqldump -u root -p --default-character-set=utf8 iems wx_user |gzip  > /www/backup/database/wx_user.sql.gz"
    channel.send(cmd + "\n")
    while True:
        time.sleep(1)
        rst = channel.recv(1024).decode('utf-8')
        print(rst)
        if 'password' in rst:
            channel.send('f0744af873317d5e\n')
            time.sleep(1)
            ret = channel.recv(1024).decode('utf-8')
            print(ret)
            if channel.exit_status_ready():
                break

    # s.close()

def huany():
    hostname = '47.110.48.39'
    port = 22
    username = 'root'
    password = 'sit@bbieat.com@123!'

    paramiko.util.log_to_file("paramiko.log")

    transport = paramiko.Transport((hostname, port))  # s.set_missing_host_key_policy()
    transport.connect(username=username, password=password)
    ssh = paramiko.SSHClient()
    ssh._transport = transport

    channel = ssh.invoke_shell(width=1024, height=100)
    # channel.send("cd /www/backup/database")
    # cmd = "mysqldump -u root -p --default-character-set=utf8 iems wx_user |gzip  > /www/backup/database/wx_user.sql.gz"
    cmd = "gunzip < /www/backup/database/wx_user.sql.gz | mysql -u root -p iems"
    channel.send(cmd + "\n")
    while True:
        time.sleep(1)
        rst = channel.recv(1024).decode('utf-8')
        print(rst)
        if 'password' in rst:
            channel.send('f0744af873317d5e\n')
            time.sleep(1)
            ret = channel.recv(1024).decode('utf-8')
            print(ret)
            if channel.exit_status_ready():
                break


def main():
    hostname = '47.110.48.39'
    port = 22
    username = 'root'
    password = 'sit@bbieat.com@123!'
    execmd1 = "mysqldump -u root -p --default-character-set=utf8 iems wx_user > /www/backup/database/wx_user.sql"
    execmd = 'pwd'
    sshclient_execmd(hostname, port, username, password, execmd1)


if __name__ == "__main__":
  # transport_shell2()
  huany()
