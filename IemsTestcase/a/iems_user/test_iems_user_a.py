import time
import unittest
import warnings
import allure
import os
from Comm.data import ReadData
from Comm.mysql_backup import MysqlConn
from IemsPage.basePage import *
from IemsPage.iems_eqp.iems_eqp import IEMSEquipment
from IemsPage.iems_login.iems_login import IemsLogin
from IemsPage.iems_user.iems_user import IEMSUser


@allure.severity(allure.severity_level.CRITICAL)
@allure.feature('测试a用户相关')
class TestIEMSUser(unittest.TestCase):
    """测试档案相关"""


    # databases = MysqlConn().read_all_databases()
    # backup_files = MysqlConn().backup_databases(databases,
    #                                             ['bar_container', 'mbr_consumer_config', 'mbr_consumer', 'mbr_cons_cntr_billing_scheme', 'mbr_inner_account'])

    test_login_data = ReadData('test_login_data.xlsx').read_excel()
    test_user_data = ReadData('test_open_user_data.xlsx').read_excel()
    test_project_data = ReadData('test_project_data.xlsx').read_excel()
    Logger().info(test_user_data)
    driver = Base('c')

    def check_assert(self, actual, expect):
        """
        确认数据是否正确
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
    @allure.story('用户档案')
    @allure.title('测试a用户开户')
    def test_01_open_user(self):
        """用户开户"""

        with allure.step("登录a2.4"):
            IemsLogin(self.driver).a_login_new(self.test_login_data[2]['user'], self.test_login_data[2]['pwd'])
        with allure.step("点击运营界面开户按钮，进入用户开户页面"):
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[3]/div/div[1]').click()
        with allure.step("选择项目"):
            IEMSUser(self.driver).user_project(self.test_project_data[2]['project_name'])
        with allure.step("用户开户"):
            IEMSUser(self.driver).open_user_a(self.test_user_data[0]['mbrConsName'], self.test_user_data[0]['contacter'],
                                            self.test_user_data[0]['contactMobile'])
        actual = self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div/h2').text
        mbrConsName = self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[1]/div/div[2]/div/form/div[2]/div/div').text
        with allure.step("判断开户是否成功"):
            self.check_assert(actual, '开户成功')
            self.check_assert(mbrConsName, self.test_user_data[0]['mbrConsName'])
        with allure.step("进入用户档案界面"):
            IEMSUser(self.driver).enter_user()
        with allure.step("点击用户名搜索"):
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div['
                                    '2]/table/thead/tr/th[3]/div/span/span/span').click()
        with allure.step("搜索刚开户的用户号"):
            IEMSEquipment(self.driver).select_index(self.test_user_data[0]['mbrConsName'])
        self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[8]/div/p')
        with allure.step("核对用户档案界面是否有该数据"):
            mbrConsName = self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[3]/table/tbody/tr/td[3]/div').text
            print(mbrConsName)
            self.check_assert(mbrConsName, self.test_user_data[0]['mbrConsName'])

    @Screen(driver)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story('用户档案')
    @allure.title('测试a用户变更')
    def test_02_change_user(self):
        """测试变更"""
        # IemsLogin(self.driver).a_login_new(self.test_login_data[2]['user'], self.test_login_data[2]['pwd'])
        # IEMSUser(self.driver).enter_user()
        # IEMSUser(self.driver).user_project('发布回归')
        # self.driver.get_element(
        #     'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        # IEMSEquipment(self.driver).select_index(self.test_user_data[0]['mbrConsName'])
        with allure.step('新开户的用户点击变更'):
            self.driver.move_to_click('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[5]/div['
                                      '2]/table/tbody/tr/td[17]/div/button[1]')
        with allure.step('修改用户名加上变更2字'):
            IEMSUser(self.driver).change_user('变更')
        actual = self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[2]/div[1]/div[1]/div/h2').text
        mbrConsName = self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[2]/div[1]/div[2]/div/form/div[2]/div/div').text
        with allure.step('核对是否变更成功'):
            self.check_assert(actual, '变更成功')
            self.check_assert(mbrConsName, self.test_user_data[0]['mbrConsName'] + '变更')
        with allure.step('进入用户档案'):
            IEMSUser(self.driver).enter_user()
        with allure.step("点击用户名搜索"):
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/table/thead/tr/th['
                '3]/div/span/span/span').click()
            IEMSEquipment(self.driver).select_index(self.test_user_data[0]['mbrConsName'])
        self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[8]/div/p')
        with allure.step("核对用户档案界面是否变更成功"):
            mbrConsName = self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[3]/table/tbody/tr/td[3]/div').text
            print(mbrConsName)
            self.check_assert(mbrConsName, self.test_user_data[0]['mbrConsName'] + '变更')

    @Screen(driver)
    @allure.story('账户档案')
    @allure.title('测试a现金充值')
    def test_03_recharge_user(self):
        """测试现金充值"""

        # IemsLogin(self.driver).a_login_new(self.test_login_data[2]['user'], self.test_login_data[2]['pwd'])
        # IEMSUser(self.driver).enter_user()
        # IEMSUser(self.driver).user_project('发布回归')
        with allure.step("点击账户档案"):
            self.driver.move_to_click('x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[2]/div/div/li/ul/div['
                                      '2]/div/li/span')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div[1]/div[4]/div['
                               '1]/table/thead/tr/th[3]/div/span[1]/span/span')
        with allure.step("点击用户名搜索"):
            self.driver.move_to_click('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div[1]/div['
                                      '2]/table/thead/tr/th[4]/div/span[1]/span/span')
            IEMSEquipment(self.driver).select_index(self.test_user_data[0]['mbrConsName'])
        with allure.step("点击充值按钮"):
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div[1]/div[5]/div['
                                    '2]/table/tbody/tr/td[12]/div/div/button[1]').click()
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[2]/div/form/div['
                               '2]/div/div[1]/label[1]')
        with allure.step("选择充值金额"):
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[2]/div/form/div['
                                    '2]/div/div[1]/label[1]').click()
        with allure.step("点击充值"):
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[2]/div/form/div['
                                    '3]/div/button[2]').click()
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div/div[2]/div[2]/span/button[2]')
        with allure.step("点击确定"):
            self.driver.move_to_click(
                'x, //*[@id="app"]/div/div[2]/section/div/div[3]/div/div[2]/div[2]/span/button[2]')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[2]/div/div/div[1]/div['
                               '7]/div[2]')
        with allure.step("核对是都支付成功"):
            pay_status = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div['
                                                 '2]/div/div/div[1]/div[7]/div[2]').text
            self.check_assert(pay_status, '支付成功')

    @Screen(driver)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story('账户档案')
    @allure.title('测试a用户退款')
    def test_04_refund_user(self):
        """测试退款"""
        # IemsLogin(self.driver).a_login_new(self.test_login_data[2]['user'], self.test_login_data[2]['pwd'])
        # IEMSUser(self.driver).enter_user()
        IEMSUser(self.driver).user_project(self.test_project_data[2]['project_name'])
        with allure.step("进入账户档案界面"):
            self.driver.move_to_click(
                'x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[2]/div/div/li/ul/div[2]/div/li/span')
        self.driver.wait_until(
            'x, //*[@id="app"]/div/div[2]/section/div/div[3]/div[1]/div[4]/div[1]/table/thead/tr/th[3]/div/span['
            '1]/span/span')
        time.sleep(1)
        with allure.step("点击退款按钮"):
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div[1]/div[5]/div['
                                    '2]/table/tbody/tr/td[12]/div/div/button[2]').click()
        with allure.step("进行退款"):
            IEMSUser(self.driver).refund_money('1')
        with allure.step("核对是否退款成功"):
            actual = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/section/div['
                                             '2]/div/div[1]/div[1]/div/div/h2').text
            self.check_assert(actual, '退款成功')

    @Screen(driver)
    @allure.story('用户档案')
    @allure.title('测试a用户退租')
    def test_05_exit_user(self):
        """测试退租"""
        # IemsLogin(self.driver).a_login_new(self.test_login_data[2]['user'], self.test_login_data[2]['pwd'])
        # IEMSUser(self.driver).enter_user()
        # IEMSUser(self.driver).user_project('发布回归')
        # self.driver.get_element(
        #     'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        # IEMSEquipment(self.driver).select_index(self.test_user_data[0]['mbrConsName'])
        # self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[5]/div[2]/table/tbody/tr/td[17]/div/button[2]')
        with allure.step("进入用户档案界面"):
            IEMSUser(self.driver).enter_user()
        with allure.step("点击退租按钮"):
            self.driver.move_to_click(
                'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[5]/div[2]/table/tbody/tr/td['
                '17]/div/button[2]')
        with allure.step("进行退租"):
            IEMSUser(self.driver).exit_user()
        actual = self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div[1]/div[1]/div/h2').text
        mbrConsName = self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div[1]/div[2]/div/form/div[2]/div/div').text
        with allure.step("核对是否退租成功"):
            self.check_assert(actual, '退租成功')
            self.check_assert(mbrConsName, self.test_user_data[0]['mbrConsName'] + '变更')
        with allure.step("进入用户档案界面"):
            IEMSUser(self.driver).enter_user()
        with allure.step("查找刚开户的用户"):
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/table/thead/tr/th['
                '3]/div/span/span/span').click()
            IEMSEquipment(self.driver).select_index(self.test_user_data[0]['mbrConsName'])
            time.sleep(1)
        # self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[8]/div/p')
        with allure.step("核对用户档案界面是否还有该用户"):
            mbrConsName = self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[3]/div/span').text
            print(mbrConsName)
            self.check_assert(mbrConsName, '暂无数据')
        # time.sleep(10)


    def tearDown(self) -> None:
        # self.driver.driver.refresh()
        print('测试结束')

    @classmethod
    def tearDownClass(cls):
        # MysqlConn().restore_databases(cls.databases, cls.backup_files)
        cls.driver.driver.quit()


if __name__ == '__main__':
    unittest.main()