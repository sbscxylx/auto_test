#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2022/3/28 10:51
# @Author : 余少琪
"""

from Comm import *
import yaml.scanner
from pydantic import ValidationError
from Conf.models import TestData


class GetYamlData:
    """ 获取 yaml 文件中的数据 """

    def __init__(self, file_dir):
        self.file_dir = str(file_dir)

    def get_yaml_data(self) -> dict:
        """
        获取 yaml 中的数据
        :param: fileDir:
        :return:
        """
        # 判断文件是否存在
        if os.path.exists(self.file_dir):
            data = open(self.file_dir, 'r', encoding='utf-8')
            res = yaml.load(data, Loader=yaml.FullLoader)
            data.close()
        else:
            raise FileNotFoundError("文件路径不存在")
        return res

    def write_yaml_data(self, key: str, value) -> int:
        """
        更改 yaml 文件中的值, 并且保留注释内容
        :param key: 字典的key
        :param value: 写入的值
        :return:
        """
        with open(self.file_dir, 'r', encoding='utf-8') as file:
            # 创建了一个空列表，里面没有元素
            lines = []
            for line in file.readlines():
                if line != '\n':
                    lines.append(line)
            file.close()

        with open(self.file_dir, 'w', encoding='utf-8') as file:
            flag = 0
            for line in lines:
                left_str = line.split(":")[0]
                if key == left_str and '#' not in line:
                    newline = f"{left_str}: {value}"
                    line = newline
                    file.write(f'{line}\n')
                    flag = 1
                else:
                    file.write(f'{line}')
            file.close()
            return flag

    def circle_yaml_datas(self):

        yaml_datas = self.get_yaml_data()

        # print(yaml_datas)
        try:
            _yaml_datas = TestData(**yaml_datas)
            # print(_yaml_datas)
        except ValidationError as e:
            print(e.json())

        return _yaml_datas


        # yaml_datas_list = {k: v for k, v in _yaml_datas[key].items()}
        # print(_yaml_datas.projetc_data)


class GetCaseData(GetYamlData):
    """ 获取测试用例中的数据 """

    def get_different_formats_yaml_data(self) -> list:
        """
        获取兼容不同格式的yaml数据
        :return:
        """
        res_list = []
        for i in self.get_yaml_data():
            res_list.append(i)
        return res_list

    # def get_yaml_case_data(self):
    #     """
    #     获取测试用例数据, 转换成指定数据格式
    #     :return:
    #     """
    #
    #     _yaml_data = self.get_yaml_data()
    #     # 正则处理yaml文件中的数据
    #     re_data = regular(str(_yaml_data))
    #     return ast.literal_eval(re_data)


if __name__ == '__main__':
    # a = GetYamlData(ensure_path_sep("/IemsTestcase/Testdata/test_data.yaml")).get_yaml_data()
    b = GetYamlData(ensure_path_sep("/IemsTestcase/Testdata/test_data.yaml")).circle_yaml_datas()
    print(b.project_data.bar_project_name)