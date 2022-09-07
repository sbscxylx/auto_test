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
from IemsPage.iems_user.iems_user import IEMSUser
from IemsPage.iems_login.iems_login import IemsLogin


@allure.severity(allure.severity_level.CRITICAL)
@allure.feature('测试sit计费方案相关')
class TestIEMSTmpl(unittest.TestCase):
    """测试sit项目级相关"""

    Logger().rm_log()
    databases = MysqlConn().read_all_databases()
    backup_files = MysqlConn().backup_databases(databases,
                                                ['mbr_tmpl_billing_scheme',
                                                 'mbr_tmpl_billing_scheme_edition',
                                                 'mbr_tmpl_billing_scheme_edition_charging'])
    test_login_data = ReadData('test_login_data.xlsx').read_excel()
    test_project_data = ReadData('test_project_data.xlsx').read_excel()
    Logger().info(test_project_data)


    def check_assert(self, actual, expect):
        """
        确认数据是否导入
        :param actual:
        :param expect:
        :return:
        """
        Logger().info('预期数据{}, 实际数据{}'.format(expect, actual))
        self.assertEqual(str(expect), actual)

    @classmethod
    def setUpClass(cls):
        cls.driver = Base('c')

    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)

    @allure.story('计费方案(不含附加费)')
    @allure.title('测试sit新建计费方案')
    def test_01_add_tmpl(self):
        """测试sit新建计费方案(不含附加费)"""

        tmplName = '方案1(不含附加费)'

        with allure.step("登录sit2.3"):
            IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        with allure.step("进入计费档案界面"):
            IEMSProject(self.driver).enter_tmpl()
        with allure.step('选择项目'):
            IEMSUser(self.driver).user_project(self.test_project_data[1]['project_name'])
        with allure.step('新建计费方案'):
            IEMSProject(self.driver).add_tmpl(tmplName, '电表')
        with allure.step('查询方案1'):
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
            IEMSEquipment(self.driver).select_index(tmplName)
        with allure.step('验证方案新建成功'):
            tmplName_a = self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[3]/table/tbody/tr[1]/td[3]/div').text
            self.check_assert(tmplName_a, tmplName)

    @allure.story('计费方案(不含附加费)')
    @allure.title('测试sit新建计费方案版本')
    def test_02_add_tmpl_edition(self):
        """测试sit新建计费方案版本(不含附加费)"""

        editionNo = '新增版本'
        # with allure.step("登录sit2.3"):
        #     IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # with allure.step("进入计费档案界面"):
        #     IEMSProject(self.driver).enter_tmpl()
        # with allure.step('选择项目'):
        #     IEMSUser(self.driver).user_project(self.test_project_data[1]['project_name'])
        # with allure.step('查询方案1'):
        #     self.driver.get_element(
        #         'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        #     IEMSEquipment(self.driver).select_index(self.tmplName)
        with allure.step('点击查看'):
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[4]/div[2]/table/tbody/tr/td[6]/div/button').click()
            self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[4]')
            # tmplName = self.driver.get_element(
            #     'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/header/div').text
            # self.check_assert(tmplName, self.tmplName)
        with allure.step('新增版本'):
            IEMSProject(self.driver).add_tmpl_edition(editionNo, editionNo)
        with allure.step('验证版本是否新建'):
            editionName_a = self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr/td[3]/div').text
            self.check_assert(editionName_a, editionNo)

    @allure.story('计费方案(不含附加费)')
    @allure.title('测试sit新建计费方案版本费率（复费率）')
    def test_03_add_edition_charging_fu(self):
        """测试sit新建计费方案版本费率-复费率(不含附加费)"""
        tmplType = '复费率'
        tmplCharging1 = 1
        tmplCharging2 = 2
        tmplCharging3 = 3
        tmplCharging4 = 4

        # with allure.step("登录sit2.3"):
        #     IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # with allure.step("进入计费档案界面"):
        #     IEMSProject(self.driver).enter_tmpl()
        # with allure.step('选择项目'):
        #     IEMSUser(self.driver).user_project(self.test_project_data[1]['project_name'])
        # with allure.step('查询方案1'):
        #     self.driver.get_element(
        #         'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        #     IEMSEquipment(self.driver).select_index(self.tmplName)
        # with allure.step('点击查看'):
        #     self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[4]/div[2]/table/tbody/tr/td[6]/div/button').click()
        #     self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/header/div')
        #     tmplName = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/header/div').text
        #     self.check_assert(tmplName, self.tmplName)
        with allure.step('新增费率'):
            self.driver.wait_until(
                'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr/td[9]/div/button')
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr/td[9]/div/button').click()
            Logger().info('点击详情')
            IEMSProject(self.driver).add_tmpl_edition_charging(tmplType=tmplType, tmplCharging1=tmplCharging1,
                                                               tmplCharging2=tmplCharging2,
                                                               tmplCharging3=tmplCharging3, tmplCharging4=tmplCharging4)
        with allure.step('验证复费率是否新建'):
            self.driver.wait_until(
                'x, //*[@id="app"]/div/div[2]/section/div/div[6]/div/div/section/div/div[3]/table/tbody/tr/td[2]/div')
            tmplType_a = self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[6]/div/div/section/div/div[3]/table/tbody/tr/td[2]/div').text
            self.check_assert(tmplType_a, tmplType + '类型')

    @allure.story('计费方案(不含附加费)')
    @allure.title('测试sit新建计费方案版本费率（复费率）')
    def test_04_add_edition_charging_dan(self):
        """测试sit新建计费方案版本费率-单费率(不含附加费)"""
        tmplType = '单一费率'
        tmplCharging = 1

        # with allure.step("登录sit2.3"):
        #     IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # with allure.step("进入计费档案界面"):
        #     IEMSProject(self.driver).enter_tmpl()
        # with allure.step('选择项目'):
        #     IEMSUser(self.driver).user_project(self.test_project_data[1]['project_name'])
        # with allure.step('查询方案1'):
        #     self.driver.get_element(
        #         'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        #     IEMSEquipment(self.driver).select_index(self.tmplName)
        # with allure.step('点击查看'):
        #     self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[4]/div[2]/table/tbody/tr/td[6]/div/button').click()
        #     self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/header/div')
        #     tmplName = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/header/div').text
        #     self.check_assert(tmplName, self.tmplName)
        with allure.step('新增费率'):
            # self.driver.wait_until(
            #     'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr/td[9]/div/button')
            # time.sleep(1)
            # self.driver.get_element(
            #     'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr/td[9]/div/button').click()
            # Logger().info('点击详情')
            # self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[6]')
            self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[6]/div/div/section/button')
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[6]/div/div/section/button').click()
            Logger().info('点击年时段表')
            self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[7]')
            time.sleep(1)
            self.driver.wait_until(
                'x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/form/div[1]/label')
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/form/div[2]/div/div/label[1]/span[1]/span').click()
            Logger().info('点击单费率')
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/form/div[3]/div/div/div/input').send_keys(
                tmplCharging)
            Logger().info('单费率输入费率')
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/form/div[1]/div/div/div/input').click()
            self.driver.wait_play('x, //body/div[last()]/div/div/div[2]/table/tbody/tr[last()-1]/td[last()]/div/span')
            self.driver.get_element(
                'x, //body/div[last()]/div/div/div[2]/table/tbody/tr[last()-1]/td[last()]/div/span').click()
            Logger().info('选择生效时间')
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/div/button').click()
            Logger().info('点击保存')
            self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[7]')
        with allure.step('验证单费率是否新建'):
            self.driver.wait_until(
                'x, //*[@id="app"]/div/div[2]/section/div/div[6]/div/div/section/div/div[3]/table/tbody/tr[2]/td[2]/div')
            tmplType_a = self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[6]/div/div/section/div/div[3]/table/tbody/tr[2]/td[2]/div').text
            self.check_assert(tmplType_a, tmplType + '类型')

    @allure.story('计费方案(不含附加费)')
    @allure.title('测试sit删除计费方案版本费率')
    def test_05_del_edition_charging(self):
        """测试sit删除计费方案版本费率(不含附加费)"""

        # with allure.step("登录sit2.3"):
        #     IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # with allure.step("进入计费档案界面"):
        #     IEMSProject(self.driver).enter_tmpl()
        # with allure.step('选择项目'):
        #     IEMSUser(self.driver).user_project(self.test_project_data[1]['project_name'])
        # with allure.step('查询方案1'):
        #     self.driver.get_element(
        #         'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        #     IEMSEquipment(self.driver).select_index(self.tmplName)
        # with allure.step('点击查看'):
        #     self.driver.get_element(
        #         'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[4]/div[2]/table/tbody/tr/td[6]/div/button').click()
        #     self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/header/div')
        #     tmplName = self.driver.get_element(
        #         'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/header/div').text
        #     self.check_assert(tmplName, self.tmplName)
        with allure.step('删除费率'):
            # self.driver.wait_until(
            #     'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr/td[9]/div/button')
            # time.sleep(1)
            # self.driver.get_element(
            #     'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr/td[9]/div/button').click()
            # Logger().info('点击详情')
            IEMSProject(self.driver).del_edition_charging()
        with allure.step('验证计费是否删除'):
            self.driver.wait_until(
                'x, //*[@id="app"]/div/div[2]/section/div/div[6]/div/div/section/div/div[3]/table/tbody/tr[last()]/td[2]/div')
            tmplType_a = self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[6]/div/div/section/div/div[3]/table/tbody/tr[last()]/td[2]/div').text
            self.assertNotEqual(tmplType_a, '单一费率类型')

    @allure.story('计费方案(含附加费)')
    @allure.title('测试sit新建计费方案')
    def test_06_add_tmpl_fee(self):
        """测试sit新建计费方案(含附加费)"""

        tmplNameFee = '方案1（含附加费）'

        with allure.step("登录sit2.3"):
            IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        with allure.step("进入计费档案界面"):
            IEMSProject(self.driver).enter_tmpl(isFee='yes')
        with allure.step('选择项目'):
            IEMSUser(self.driver).user_project(self.test_project_data[1]['project_name'])
        with allure.step('新建计费方案（含附加费）'):
            IEMSProject(self.driver).add_tmpl(tmplNameFee, '电表')
        with allure.step('查询方案1（含附加费）'):
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
            IEMSEquipment(self.driver).select_index(tmplNameFee)
        with allure.step('验证方案新建成功'):
            tmplName = self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[3]/table/tbody/tr[1]/td[3]/div').text
            self.check_assert(tmplName, tmplNameFee)

    @allure.story('计费方案(含附加费)')
    @allure.title('测试sit新建计费方案版本(不开启附加费)')
    def test_07_add_tmpl_edition_fee(self):
        """测试sit新建计费方案版本(不开启附加费)"""

        tmplNameFee = '方案1（含附加费）'
        editionNo = '新增版本(不开启附加费)'
        # with allure.step("登录sit2.3"):
        #     IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # with allure.step("进入计费档案界面"):
        #     IEMSProject(self.driver).enter_tmpl(isFee='yes')
        # with allure.step('选择项目'):
        #     IEMSUser(self.driver).user_project(self.test_project_data[1]['project_name'])
        # with allure.step('查询方案1'):
        #     self.driver.get_element(
        #         'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        #     IEMSEquipment(self.driver).select_index(tmplNameFee)
        with allure.step('点击查看'):
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[4]/div[2]/table/tbody/tr/td[6]/div/button').click()
            self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[4]')
            # tmplName = self.driver.get_element(
            #     'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/header/div').text
            # self.check_assert(tmplName, self.tmplName)
        with allure.step('新增版本'):
            IEMSProject(self.driver).add_tmpl_edition_fee(editionNo, editionNo)
        with allure.step('验证版本是否新建'):
            editionName_a = self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr/td[2]/div').text
            self.check_assert(editionName_a, editionNo)
        with allure.step('验证附加费未开启'):
            feeName_a = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr/td[5]/div').text
            self.check_assert(feeName_a, '-')

    @allure.story('计费方案(含附加费)')
    @allure.title('测试sit新建计费方案版本(固定价格)')
    def test_08_add_tmpl_edition_fee(self):
        """测试sit新建计费方案版本(固定价格)"""

        editionNo = '新增版本(固定价格)'
        feeName = '固定价格'
        feeMoney = '1.1314'
        # with allure.step("登录sit2.3"):
        #     IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # with allure.step("进入计费档案界面"):
        #     IEMSProject(self.driver).enter_tmpl(isFee='yes')
        # with allure.step('选择项目'):
        #     IEMSUser(self.driver).user_project(self.test_project_data[1]['project_name'])
        # with allure.step('查询方案1'):
        #     self.driver.get_element(
        #         'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        #     IEMSEquipment(self.driver).select_index('方案1')
        # with allure.step('点击查看'):
        #     self.driver.get_element(
        #         'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[4]/div[2]/table/tbody/tr/td[6]/div/button').click()
        #     self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[4]')
            # tmplName = self.driver.get_element(
            #     'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/header/div').text
            # self.check_assert(tmplName, self.tmplName)
        with allure.step('新增版本'):
            IEMSProject(self.driver).add_tmpl_edition_fee(editionNo, editionNo, 'yes', feeName, feeType=feeName, feeMoney=feeMoney)
        with allure.step('验证版本是否新建'):
            editionName_a = self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr/td[2]/div').text
            self.check_assert(editionName_a, editionNo)
        with allure.step('验证附加费为固定价格'):
            feeName_a = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr[1]/td[5]/div').text
            self.check_assert(feeName_a, feeName)
            feeType_a = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr[1]/td[6]/div').text
            self.check_assert(feeType_a, feeName)
            feeMoney_a = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr/td[7]/div').text
            self.check_assert(feeMoney_a, feeMoney)

    @allure.story('计费方案(含附加费)')
    @allure.title('测试sit新建计费方案版本(上浮比例)')
    def test_09_add_tmpl_edition_fee(self):
        """测试sit新建计费方案版本(上浮比例)"""

        editionNo = '新增版本(上浮比例)'
        feeName = '上浮比例'
        feeMoney = '1.13'
        # with allure.step("登录sit2.3"):
        #     IemsLogin(self.driver).iems_login_new(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # with allure.step("进入计费档案界面"):
        #     IEMSProject(self.driver).enter_tmpl(isFee='yes')
        # with allure.step('选择项目'):
        #     IEMSUser(self.driver).user_project(self.test_project_data[1]['project_name'])
        # with allure.step('查询方案1'):
        #     self.driver.get_element(
        #         'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[2]/table/thead/tr/th[3]/div/span/span/span').click()
        #     IEMSEquipment(self.driver).select_index('方案1')
        # with allure.step('点击查看'):
        #     self.driver.get_element(
        #         'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/div[4]/div[2]/table/tbody/tr/td[6]/div/button').click()
        #     self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[4]')
            # tmplName = self.driver.get_element(
            #     'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/header/div').text
            # self.check_assert(tmplName, self.tmplName)
        with allure.step('新增版本'):
            IEMSProject(self.driver).add_tmpl_edition_fee(editionNo, editionNo, 'yes', feeName, feeType=feeName, feeMoney=feeMoney)
        with allure.step('验证版本是否新建'):
            editionName_a = self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr/td[2]/div').text
            self.check_assert(editionName_a, editionNo)
        with allure.step('验证附加费为固定价格'):
            feeName_a = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr[1]/td[5]/div').text
            self.check_assert(feeName_a, feeName)
            feeType_a = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr[1]/td[6]/div').text
            self.check_assert(feeType_a, feeName)
            feeMoney_a = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/div/div[3]/table/tbody/tr[1]/td[8]/div').text
            self.check_assert(feeMoney_a, feeMoney)



    def tearDown(self) -> None:
        # self.driver.driver.refresh()
        print('测试结束')

    @classmethod
    def tearDownClass(cls):
        MysqlConn().restore_databases(cls.databases, cls.backup_files)
        cls.driver.driver.quit()


if __name__ == '__main__':
    unittest.main()
