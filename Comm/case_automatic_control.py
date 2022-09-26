#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
from typing import Text, Dict
from Comm import *
from Conf.exceptions import ValueNotFoundError
from Conf.yaml_control import GetYamlData


class TestCaseAutomaticGeneration:
    """自动生成自动化测试中的test_case代码"""

    def __init__(self, env):

        self.env = env

    @staticmethod
    def case_date_path() -> Text:
        """返回 yaml 用例文件路径"""
        return get_path.ensure_path_sep("\\data")

    @staticmethod
    def case_path() -> Text:
        """ 存放用例代码路径"""
        return get_path.ensure_path_sep(f"\\test_case")

    def file_name(self, file: Text) -> Text:
        """
        通过 yaml文件的命名，将名称转换成 py文件的名称
        :param file: yaml 文件路径
        :return:  示例： DateDemo.py
        """

        i = len(self.case_date_path())
        yaml_path = file[i:]
        file_name = None
        # 路径转换
        if '.yaml' in yaml_path:
            file_name = yaml_path.replace('.yaml', '.py')
        elif '.yml' in yaml_path:
            file_name = yaml_path.replace('.yml', '.py')
        return file_name

    def get_case_path(self, file_path: Text) -> tuple:
        """
        根据 yaml 中的用例，生成对应 testCase 层代码的路径
        :param file_path: yaml用例路径
        :return: D:\\Project\\test_case\\test_case_demo.py, test_case_demo.py
        """

        # 这里通过“\\” 符号进行分割，提取出来文件名称
        path = self.file_name(file_path).split(os.sep)
        path1 = path[-1].split('.')
        # 判断生成的 testcase 文件名称，需要以test_ 开头,已_{env}结尾
        path[-1] = path1[0].replace(path1[0], "test_" + path1[0] + f'_{self.env}.py')
        case_name = path[-2] = path[-2].replace(path[-2], f"{config.project_name}_" + path[-2])
        new_name = os.sep.join(path)

        return get_path.ensure_path_sep(f"\\IemsTestcase\\{self.env}" + new_name), case_name

    def get_test_class_title(self, file_path: Text) -> Text:
        """
        自动生成类名称
        :param file_path:
        :return: sup_apply_list --> SupApplyList
        """
        # 提取文件名称
        _file_name = os.path.split(self.get_case_path(file_path)[0])[1]
        _name = _file_name.split('.')[0].split('_')
        _name_len = len(_name)
        # 将文件名称格式，转换成类名称: sup_apply_list --> SupApplyList
        for i in range(_name_len):
            _name[i] = _name[i].capitalize()
        _class_name = "".join(_name)

        return _class_name

    @staticmethod
    def error_message(param_name, file_path):
        """
        用例中填写不正确的相关提示
        :return:
        """
        msg = f"用例中未找到 {param_name} 参数值，请检查新增的用例中是否填写对应的参数内容" \
              "如已填写，可能是 yaml 参数缩进不正确\n" \
              f"用例路径: {file_path}"
        return msg

    @staticmethod
    def func_title(case_id) -> Text:
        """
        用于生成用例名称
        :param case_id: 用例名称
        :return:
        """

        log.Logger().info(f'用例标题{case_id}')
        return case_id

    @staticmethod
    def allure_severity(case_data: Dict, file_path) -> Text:
        """
        用于 allure 报告装饰器中的内容 @allure.severity("")
        :param file_path: 用例路径
        :param case_data: 用例数据
        :return:
        """
        try:
            log.Logger().info(f"class用例优先级{case_data['case_common']['allureSeverity']}")
            return case_data['case_common']['allureSeverity']
        except KeyError as exc:
            raise ValueNotFoundError(TestCaseAutomaticGeneration.error_message(
                param_name="allureSeverity",
                file_path=file_path
            )) from exc

    @staticmethod
    def allure_feature(case_data: Dict, file_path) -> Text:
        """
        用于 allure 报告装饰器中的内容 @allure.feature("模块名称")
        :param file_path:
        :param case_data:
        :return:
        """
        try:
            log.Logger().info(f"class用例模块{case_data['case_common']['allureFeature']}")
            return case_data['case_common']['allureFeature']
        except KeyError as exc:
            raise ValueNotFoundError(TestCaseAutomaticGeneration.error_message(
                param_name="allureFeature",
                file_path=file_path
            )) from exc

    @staticmethod
    def allure_story(case_data: Dict, case_id, file_path) -> Text:
        """
        用于 allure 报告装饰器中的内容  @allure.story("测试功能页面")
        :param case_data:
        :param file_path:
        :param case_id:
        :return:
        """
        try:
            log.Logger().info(f"用例功能页面{case_data[case_id]['allureStory']}")
            return case_data[case_id]['allureStory']
        except KeyError as exc:
            raise ValueNotFoundError(TestCaseAutomaticGeneration.error_message(
                param_name="allureStory",
                file_path=file_path
            )) from exc

    @staticmethod
    def allure_title(case_data: Dict, case_id, file_path) -> Text:
        """
        用于 allure 报告装饰器中的内容  @allure.title("测试用例标题")
        :param case_data:
        :param file_path:
        :param case_id:
        :return:
        """
        try:
            log.Logger().info(f"用例功能页面{case_data[case_id]['allureTitle']}")
            return case_data[case_id]['allureTitle']
        except KeyError as exc:
            raise ValueNotFoundError(TestCaseAutomaticGeneration.error_message(
                param_name="allureTitle",
                file_path=file_path
            )) from exc

    @staticmethod
    def allure_step(case_data: Dict, case_id, file_path) -> Text:
        """

        :param case_data:
        :param case_id:
        :param file_path:
        :return:
        """
        allure_step = ''
        try:
            for k, v in case_data[case_id]['allureStep'].items():
                allure_step = allure_step + f'with allure.step("{v}"):' + '\n\t\t\tpass\n\t\t'
            log.Logger().info(f'用例步骤{allure_step}')
            return allure_step
        except KeyError as exc:
            raise ValueNotFoundError(TestCaseAutomaticGeneration.error_message(
                param_name="allureStep",
                file_path=file_path
            )) from exc


    def mk_dir(self, file_path: Text, isInit=True) -> None:
        """ 判断生成自动化代码的文件夹路径是否存在，如果不存在，则自动创建 """
        # _LibDirPath = os.path.split(self.libPagePath(filePath))[0]

        _case_dir_path = os.path.split(self.get_case_path(file_path)[0])[0]
        log.Logger().info(f'生成测试用例文件路径{_case_dir_path}')
        if isInit:
            _case_dir_path_init = _case_dir_path + '\\__init__.py'
            if not os.path.exists(_case_dir_path):
                os.makedirs(_case_dir_path)
                f = open(_case_dir_path_init, 'w')
                f.close()
            else:
                f = open(_case_dir_path_init, 'w')
                f.close()
        else:
            if not os.path.exists(_case_dir_path):
                os.makedirs(_case_dir_path)

        return

    @staticmethod
    def case_ids(test_case):
        """
        获取用例 ID
        :param test_case: 测试用例内容
        :return:
        """
        ids = []
        for k, v in test_case.items():
            if 'test' in k:
                ids.append(k)
        return ids

    def yaml_path(self, file_path: Text) -> Text:
        """
        生成动态 yaml 路径, 主要处理业务分层场景
        :param file_path: 如业务有多个层级, 则获取到每一层/test_demo/DateDemo.py
        :return: Login/common.yaml
        """
        i = len(self.case_date_path())
        # 兼容 linux 和 window 操作路径
        yaml_path = file_path[i:].replace("\\", "/")
        return yaml_path

    def get_case_automatic(self) -> None:
        """ 自动生成 测试代码"""

        file_path = get_path.ensure_path_sep("\\data")
        file_path = get_path.get_all_files(file_path, yaml_data_switch=True)
        log.Logger().info('用例yaml文件{}'.format(file_path))

        for file in file_path:
            # 判断代理拦截的yaml文件，不生成test_case代码
            if 'proxy_data.yaml' not in file:
                # 判断用例需要用的文件夹路径是否存在，不存在则创建


                yaml_case_process = GetYamlData(file).get_yaml_data()
                log.Logger().info(f'yaml文件数据{yaml_case_process}')


                if yaml_case_process['is_created'] is False:

                    case_ids = self.case_ids(yaml_case_process)
                    log.Logger().info(f'用例列表{case_ids}')
                    self.mk_dir(file)

                    testcase_template.write_testcase_file_start(
                        allure_severity=self.allure_severity(yaml_case_process, file_path=file),
                        allure_feature=self.allure_feature(yaml_case_process, file_path=file),
                        class_title=self.get_test_class_title(file),
                        case_path=self.get_case_path(file)[0]
                    )

                    for case_id in case_ids:
                        log.Logger().info(f'用例{case_id}')
                        testcase_template.write_func_file(
                            case_path=self.get_case_path(file)[0],
                            allure_story=self.allure_story(yaml_case_process, case_id, file),
                            allure_title=self.allure_title(yaml_case_process, case_id, file),
                            allure_step=self.allure_step(yaml_case_process, case_id, file),
                            func_title=self.func_title(case_id),
                            login_info='old'
                        )

                    testcase_template.write_testcase_file_end(
                        case_path=self.get_case_path(file)[0]
                    )


                    GetYamlData(file).write_yaml_data(key='is_created', value='True')


                else:
                    log.Logger().info(f'该文件{file}已生成过测试用例')


if __name__ == '__main__':
    TestCaseAutomaticGeneration(env='sit').get_case_automatic()

    # yaml_case_process = GetYamlData(r'C:\Users\Administrator\Desktop\UIAutoTest\data\collect\collect_edittool.yaml').get_yaml_data()
    # path_file = r'C:\\Users\\Administrator\\Desktop\\UIAutoTest\\data\\collect\\collect_addtool.yaml'

    # get_case_path = TestCaseAutomaticGeneration().get_case_path(path_file)
    # print(get_case_path)
    # _case_dir_path = os.path.split(get_case_path[0])
    # print(_case_dir_path)
    # _case_dir_path = _case_dir_path[0]
    # print(_case_dir_path + '4444')
    # # TestCaseAutomaticGeneration().mk_dir(path_file)
    # _case_dir_path = os.path.split(TestCaseAutomaticGeneration().get_case_path(path_file)[0])[0]
    # print(_case_dir_path)



    # yaml_case_process = GetYamlData(path_file).get_yaml_data()
    # case_ids = TestCaseAutomaticGeneration().case_ids(yaml_case_process)
    # print(yaml_case_process['test_collector_configuration_01']['allureStep'])
    # allure_step = ''
    # for k, v in yaml_case_process['test_collector_configuration_01']['allureStep'].items():
    #     allure_step = allure_step + f'with allure.step("{v}"):' + '\n'
    # print(allure_step)
