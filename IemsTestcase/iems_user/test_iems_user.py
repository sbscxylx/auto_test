import time
import unittest
import warnings
import os
from Comm.data import ReadData
from Comm.mysql_backup import MysqlConn
from IemsPage.basePage import *
from IemsPage.iems_eqp.iems_eqp import IEMSEquipment
from IemsPage.iems_login.iems_login import IemsLogin
from IemsPage.iems_user.iems_user import IEMSUser


class TestIEMSUser(unittest.TestCase):
    """测试档案相关"""

    Logger().rm_log()
    # databases = MysqlConn().read_all_databases()
    # backup_files = MysqlConn().backup_databases(databases,
    #                                             ['bar_container', 'mbr_consumer_config', 'mbr_consumer', 'mbr_cons_cntr_billing_scheme', 'mbr_inner_account'])
    driver = Base('c')
    test_login_data = ReadData('test_login_data.xlsx').read_excel()
    test_user_data = ReadData('test_open_user_data.xlsx').read_excel()
    Logger().info(test_user_data)

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
        pass

    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)

    def test_01_open_user(self):
        """测试开户"""

        IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[3]/div/div[1]').click()
        IEMSUser(self.driver).user_project('发布回归')
        IEMSUser(self.driver).open_user(self.test_user_data[0]['mbrConsName'], self.test_user_data[0]['contacter'], self.test_user_data[0]['contactMobile'])
        actual = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div/h2').text
        mbrConsName = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[1]/div/div[2]/div/form/div[2]/div/div').text
        self.check_assert(actual, '开户成功')
        self.check_assert(mbrConsName, self.test_user_data[0]['mbrConsName'])
        IEMSUser(self.driver).enter_user()
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        IEMSEquipment(self.driver).select_index(self.test_user_data[0]['mbrConsName'])
        self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[8]/div/p')
        mbrConsName = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[3]/table/tbody/tr/td[3]/div').text
        print(mbrConsName)
        self.check_assert(mbrConsName, self.test_user_data[0]['mbrConsName'])


    def test_02_change_user(self):
        """测试变更"""
        # IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # IEMSUser(self.driver).enter_user()
        # IEMSUser(self.driver).user_project('发布回归')
        # self.driver.get_element(
        #     'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        # IEMSEquipment(self.driver).select_index(self.test_user_data[0]['mbrConsName'])
        self.driver.move_to_click('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[5]/div[2]/table/tbody/tr/td[17]/div/button[1]')
        IEMSUser(self.driver).change_user('变更')
        actual = self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[2]/div[1]/div[1]/div/h2').text
        mbrConsName = self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[2]/div[1]/div[2]/div/form/div[2]/div/div').text
        self.check_assert(actual, '变更成功')
        self.check_assert(mbrConsName, self.test_user_data[0]['mbrConsName']+'变更')
        IEMSUser(self.driver).enter_user()
        self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        IEMSEquipment(self.driver).select_index(self.test_user_data[0]['mbrConsName'])
        self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[8]/div/p')
        mbrConsName = self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[3]/table/tbody/tr/td[3]/div').text
        print(mbrConsName)
        self.check_assert(mbrConsName, self.test_user_data[0]['mbrConsName']+'变更')


    def test_03_recharge_user(self):
        """测试充值"""

        # IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # IEMSUser(self.driver).enter_user()
        # IEMSUser(self.driver).user_project('发布回归')
        self.driver.move_to_click('x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[2]/div/div/li/ul/div[2]/div/li/span')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div[1]/div[4]/div[1]/table/thead/tr/th[3]/div/span[1]/span/span')
        self.driver.move_to_click('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div[1]/div[2]/table/thead/tr/th[4]/div/span[1]/span/span')
        IEMSEquipment(self.driver).select_index(self.test_user_data[0]['mbrConsName'])
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div[1]/div[5]/div[2]/table/tbody/tr/td[12]/div/div/button[1]').click()
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[2]/div/form/div[2]/div/div[1]/label[1]')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[2]/div/form/div[2]/div/div[1]/label[1]').click()
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[2]/div/form/div[3]/div/button[2]').click()
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div/div[2]/div[2]/span/button[2]')
        self.driver.move_to_click('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div/div[2]/div[2]/span/button[2]')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[2]/div/div/div[1]/div[7]/div[2]')
        pay_status = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[2]/div/div/div[1]/div[7]/div[2]').text
        self.check_assert(pay_status, '支付成功')


    def test_04_refund_user(self):
        """测试退款"""
        # IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # IEMSUser(self.driver).enter_user()
        IEMSUser(self.driver).user_project('发布回归')
        self.driver.move_to_click(
            'x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[2]/div/div/li/ul/div[2]/div/li/span')
        self.driver.wait_until(
            'x, //*[@id="app"]/div/div[2]/section/div/div[3]/div[1]/div[4]/div[1]/table/thead/tr/th[3]/div/span[1]/span/span')
        time.sleep(1)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div[1]/div[5]/div[2]/table/tbody/tr/td[12]/div/div/button[2]').click()
        IEMSUser(self.driver).refund_money('1')
        actual = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/section/div[2]/div/div[1]/div[1]/div/div/h2').text
        self.check_assert(actual, '退款成功')



    def test_05_exit_user(self):
        """测试退租"""
        # IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # IEMSUser(self.driver).enter_user()
        # IEMSUser(self.driver).user_project('发布回归')
        # self.driver.get_element(
        #     'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        # IEMSEquipment(self.driver).select_index(self.test_user_data[0]['mbrConsName'])
        # self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[5]/div[2]/table/tbody/tr/td[17]/div/button[2]')
        IEMSUser(self.driver).enter_user()
        self.driver.move_to_click(
            'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[5]/div[2]/table/tbody/tr/td[17]/div/button[2]')
        IEMSUser(self.driver).exit_user()
        actual = self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div[1]/div[1]/div/h2').text
        mbrConsName = self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div[1]/div[2]/div/form/div[2]/div/div').text
        self.check_assert(actual, '退租成功')
        self.check_assert(mbrConsName, self.test_user_data[0]['mbrConsName'] + '变更')
        IEMSUser(self.driver).enter_user()
        self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        IEMSEquipment(self.driver).select_index(self.test_user_data[0]['mbrConsName'])
        self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[8]/div/p')
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