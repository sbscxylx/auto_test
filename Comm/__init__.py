import datetime
import os
import time
from Comm import allure_report_data
from Comm import data
from Comm import get_local_ip
from Comm import log
from Comm import mysql_backup
from Comm import get_path
from Comm import ssh_conn
from Comm import time_control
from Comm import wechat_send
from Conf.models import Config
from Conf.yaml_control import GetYamlData

_data = GetYamlData(get_path.ensure_path_sep("/Conf/config.yaml")).get_yaml_data()
config = Config(**_data)

#
__all__ = ["log", "data", "mysql_backup", "allure_report_data", "get_local_ip", "get_path", "ssh_conn", "time_control",
           "wechat_send", "os", "time", "datetime", "config"]

if __name__ == '__main__':
    print(config)