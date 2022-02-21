import codecs
import configparser
import os
from configparser import ConfigParser

# 使用相对目录确定文件位置

conf_dir = os.path.dirname(__file__)  # 获取当前目录位置
conf_file = os.path.join(conf_dir, 'config.ini')  # 目录拼接
# pro_dir = os.path.split(os.path.realpath(__file__))[0]
# print(pro_dir)


class ReadConfig:

    def __init__(self):
        fd = open(conf_file, 'r', encoding='utf8')
        data = fd.read()    # 读取配置文件内容
        fd.close()
        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(conf_file, "w")
            file.write(data)
            file.close()
        fd.close()
        self.cf = configparser.ConfigParser()
        self.cf.read(conf_file, encoding='utf8')

    def get_url(self, option_name):
        value = self.cf.get("url", option_name)
        return value

    def get_sit_mysql(self, option_name):
        value = self.cf.get("sit_mysql", option_name)
        return value

    def get_file_path(self, option_name):
        value = self.cf.get("file_path", option_name)
        return value

    def get_email(self, option_name):
        value = self.cf.get("email", option_name)
        return value

    def get_all_options(self, section_name):
        value = self.cf.items(section_name)
        options_dict = {}
        for name, name1 in value:
            options_dict[name] = name1
        return options_dict




if __name__ == '__main__':
    a = ReadConfig().get_url('base_url')
    print(a)
    b = ReadConfig().get_all_options('sit_mysql')
    print(b)
    c = b['remote_bind_address_host']
    print(c)


    # cf = configparser.ConfigParser()
    # cf.read(conf_file, encoding='utf8')
    # a = cf.get('url', 'base_url')
    # print(a)