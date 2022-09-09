import time, datetime
import unittest
import warnings
import os
import allure
from Comm.data import ReadData
from Comm.mysql_backup import MysqlConn
from IemsPage.basePage import *
from IemsPage.iems_eqp.iems_eqp import IEMSEquipment
from IemsPage.iems_project.iems_project import IEMSProject
from IemsPage.iems_login.iems_login import IemsLogin


@allure.severity(allure.severity_level.CRITICAL)
@allure.feature('测试sit项目相关')
class TestIEMSProject(unittest.TestCase):
    """测试sit项目级相关"""


    databases = MysqlConn().read_all_databases()
    backup_files = MysqlConn().backup_databases(databases,
                                                ['bar_project'])
    test_login_data = ReadData('test_login_data.xlsx').read_excel()
    test_project_data = ReadData('test_project_data.xlsx').read_excel()
    Logger().info(test_project_data)
    driver = Base('c')

    def check_assert(self, actual, expect):
        """
        确认数据是否导入
        :param actual:
        :param expect:
        :return:
        """
        Logger().info('预期数据{}, 实际数据{}'.format(expect, actual))
        self.assertEqual(expect, actual)

    @classmethod
    def setUpClass(cls):
        Logger().rm_log()

    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)

    @Screen(driver)
    @allure.story('项目列表')
    @allure.title('测试sit新建项目')
    def test_01_add_project(self):
        """测试sit新建项目"""

        with allure.step("登录sit2.0"):
            IemsLogin(self.driver).iems_login_old(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        with allure.step("进入项目列表"):
            IEMSEquipment(self.driver).enter_project()
            self.driver.wait_until('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[1]/div/li/ul/div[last()]/li/span')
        with allure.step("点击项目新增"):
            self.driver.move_to_click('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[1]/div/li/ul/div[last()]/li/span')
        with allure.step("新建项目"):
            IEMSProject(self.driver).add_project(self.test_project_data[3]['project_name'], self.driver.date_day(index=1),
                                                 self.driver.date_day(), self.test_project_data[3]['Address'],
                                                 self.test_project_data[3]['direct'], self.test_project_data[3]['directMobile'],
                                                 self.test_project_data[3]['business'], self.test_project_data[3]['businessMobile'],
                                                 self.driver.date_day('plus', 1))
        with allure.step("点击关闭"):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[8]/div/div[2]/button/span').click()
        self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[4]/div[2]/table/tbody/tr[1]/td[2]/div')
        with allure.step("验证是否新建成功"):
            projectName = self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[4]/div[2]/table/tbody/tr[1]/td[2]/div').text
            self.check_assert(projectName, self.test_project_data[3]['project_name'])

    @Screen(driver)
    @allure.story('项目列表')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('测试sit编辑项目')
    def test_02_edit_project(self):
        """测试sit编辑项目"""

        # with allure.step("登录sit2.0"):
        #     IemsLogin(self.driver).iems_login_old(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # with allure.step("进入项目列表"):
        #     IEMSEquipment(self.driver).enter_project()
        #     self.driver.wait_until('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[1]/div/li/ul/div[last()]/li/span')
        with allure.step('点击编辑项目'):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[5]/div[2]/table/tbody/tr[1]/td[12]/div/button[2]').click()
            self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[1]/label')
            self.driver.assert_text('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[1]/label', '项目名称')
            projectName = self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[1]/div/div/input').text
            Logger().info('项目名称{}'.format(projectName))
        with allure.step('修改项目名称'):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[1]/div/div/input').send_keys('编辑')
        with allure.step('修改项目资料'):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/div/button').click()
            Logger().info('点击下一步')
        with allure.step('项目地图定位'):
            self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[4]/div[1]/div[3]')
            if self.driver.text_in('x, //*[@id="appMain-container"]/div[1]/div[4]/div[1]/div[3]', '详细地址'):
                self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[4]/div[2]/button[2]/span').click()
                Logger().info('点击下一步')
        with allure.step('负责人信息'):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[5]/div/button[2]/span').click()
            Logger().info('点击下一步')
        with allure.step('维保截止时间'):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[6]/div/button[2]/span').click()
            Logger().info('点击下一步')
        with allure.step('确认保存信息'):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/button[2]/span').click()
            Logger().info('点击确认保存信息')
            self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[8]/div/div[2]/button/span')
            Logger().info('保存成功')
            time.sleep(1)
        with allure.step("点击关闭"):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[8]/div/div[2]/button/span').click()
        with allure.step('进入项目列表'):
            IEMSEquipment(self.driver).enter_project()
            self.driver.wait_until(
                'x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[4]/div[2]/table/tbody/tr[1]/td[2]/div')
        with allure.step("验证是否新建成功"):
            projectName = self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[4]/div[2]/table/tbody/tr[1]/td[2]/div').text
            Logger().info("修改后项目名称：{}".format(projectName))
            self.check_assert(projectName, self.test_project_data[3]['project_name'] + '编辑')


    def tearDown(self) -> None:
        # self.driver.driver.refresh()
        print('测试结束')

    @classmethod
    def tearDownClass(cls):
        MysqlConn().restore_databases(cls.databases, cls.backup_files)
        cls.driver.driver.quit()


if __name__ == '__main__':
    unittest.main()

