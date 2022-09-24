#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Comm import *


def write_case(case_path, page):
    """ 写入用例模板 """
    with open(case_path, 'a', encoding="utf-8") as file:
        file.write(page + '\n')


def write_testcase_file_start(*, allure_severity, allure_feature, class_title,
                              case_path):
    """
        编写用例前面部分
        :param allure_severity: 用例级别
        :param allure_feature: 模块名称
        :param class_title: 类名称
        :param case_path: case 路径
        :return:
        """

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    start_page = f'''#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : {now}
    
    
from IemsPage.iems_eqp.iems_eqp import IEMSEquipment
from IemsPage.iems_login.iems_login import IemsLogin
from IemsPage.iems_project.iems_project import IEMSProject
from IemsTestcase import *


@allure.severity("allure.severity_level.{allure_severity}")
@allure.feature("{allure_feature}")
class {class_title}(unittest.TestCase):
    """{allure_feature}"""
    
    def check_assert(self, actual, expect):
        """
        确认数据是否正确
        :param actual:
        :param expect:
        :return:
        """
        log.Logger().info('预期数据{{}}, 实际数据{{}}'.format(expect, actual))
        self.assertEqual(expect, actual)

    @classmethod
    def setUpClass(cls):

        cls.backup_files = mysql_backup.MysqlConn().backup_databases(['bar_project'])
        cls.login = TestData.login_data
        cls.project = TestData.project_data
        log.Logger().info(f'登录信息{{cls.login}}')
        log.Logger().info(f'项目信息{{cls.project}}')
        cls.driver = Base('c')

    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        
'''

    log.Logger().info(f'编写用例前面部分')
    write_case(case_path=case_path, page=start_page)


def write_func_file(case_path, allure_story, allure_title, allure_step, func_title, login_info):
    """
    编写用例部分
    :param allure_step: 用例步骤
    :param login_info: 登录系统{old（2.0）, new（2.3）}
    :param allure_title: 用例中文标题
    :param case_path:
    :param allure_story: 用例所属页面
    :param func_title: 用例标题
    :return:
    """

    func_page = f'''
    @Screen
    @allure.story("{allure_story}")
    @allure.title("{allure_title}")
    def {func_title}(self):
        """{allure_title}"""
        
        with allure.step("登录系统"):
            IemsLogin(self.driver).iems_login_{login_info}(self.login.user[0], self.login.pwd[0])
        {allure_step}                                                    
    '''

    log.Logger().info(f'编写用例部分')
    write_case(case_path=case_path, page=func_page)


def write_testcase_file_end(case_path):
    """
    编写用例后面部分
    :param case_path:
    :return:
    """

    end_page = f'''
    def tearDown(self) -> None:
        log.Logger().info('测试结束')

    @classmethod
    def tearDownClass(cls):
        try:
            mysql_backup.MysqlConn().restore_databases(cls.backup_files)
        except:
            pass
        cls.driver.driver.quit()
        
        
if __name__ == '__main__':
    unittest.main()
    
'''

    log.Logger().info(f'编写用例后面部分')
    write_case(case_path=case_path, page=end_page)


def write_case_yaml(case_path, allureSeverity, allureFeature, test_case):
    """

    :param case_path:
    :return:
    """

    case_yaml = f'''# 公共参数
case_common:
    allureSeverity: {allureSeverity}
    allureFeature: {allureFeature}

{test_case}
'''

    write_case(case_path, page=case_yaml)