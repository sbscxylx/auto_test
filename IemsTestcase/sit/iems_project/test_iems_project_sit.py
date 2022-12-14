from IemsPage.iems_eqp.iems_eqp import IEMSEquipment
from IemsPage.iems_login.iems_login import IemsLogin
from IemsPage.iems_project.iems_project import IEMSProject
from IemsTestcase import *


@allure.severity(allure.severity_level.CRITICAL)
@allure.feature('测试sit项目相关')
class TestIemsProjectSit(unittest.TestCase):
    """测试sit项目级相关"""


    def check_assert(self, actual, expect):
        """
        确认数据是否导入
        :param actual:
        :param expect:
        :return:
        """
        log.Logger().info('预期数据{}, 实际数据{}'.format(expect, actual))
        self.assertEqual(expect, actual)


    @classmethod
    def setUpClass(cls):

        cls.backup_files = mysql_backup.MysqlConn().backup_databases(['bar_project'])
        cls.login = TestData.login_data
        cls.project = TestData.project_data
        log.Logger().info(f'登录信息{cls.login}')
        log.Logger().info(f'项目信息{cls.project}')
        cls.driver = Base('c')


    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)


    @Screen
    @allure.story('项目列表')
    @allure.title('测试sit新建项目')
    def test_01_add_project(self):
        """测试sit新建项目"""

        with allure.step("登录sit2.0"):
            IemsLogin(self.driver).iems_login_old(self.login.user[0], self.login.pwd[0])
        with allure.step("进入项目列表"):
            IEMSEquipment(self.driver).enter_project()
            self.driver.wait_until('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[1]/div/li/ul/div[last()]/li/span')
        with allure.step("点击项目新增"):
            self.driver.move_to_click('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[1]/div/li/ul/div[last()]/li/span')
        with allure.step("新建项目"):
            IEMSProject(self.driver).add_project(self.project.bar_project_name[3], self.driver.date_day(index=1),
                                                 self.driver.date_day(), self.project.Address,
                                                 self.project.direct, self.project.directMobile,
                                                 self.project.business, self.project.businessMobile,
                                                 self.driver.date_day('plus', 1))
        with allure.step("点击关闭"):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[8]/div/div[2]/button/span').click()
        self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[4]/div[2]/table/tbody/tr[1]/td[2]/div')
        with allure.step("验证是否新建成功"):
            projectName = self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[4]/div[2]/table/tbody/tr[1]/td[2]/div').text
            self.check_assert(projectName, self.project.bar_project_name[3])

    @Screen
    @allure.story('项目列表')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('测试sit编辑项目')
    def test_02_edit_project(self):
        """测试sit编辑项目"""

        # with allure.step("登录sit2.0"):
        #     IemsLogin(self.driver).iems_login_old(self.login.user[0], self.login.pwd[0])
        # with allure.step("进入项目列表"):
        #     IEMSEquipment(self.driver).enter_project()
        #     self.driver.wait_until('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[1]/div/li/ul/div[last()]/li/span')
        with allure.step('点击编辑项目'):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[5]/div[2]/table/tbody/tr[1]/td[12]/div/button[2]').click()
            self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[1]/label')
            self.driver.assert_text('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[1]/label', '项目名称')
            projectName = self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[1]/div/div/input').text
            log.Logger().info('项目名称{}'.format(projectName))
        with allure.step('修改项目名称'):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[1]/div/div/input').send_keys('编辑')
        with allure.step('修改项目资料'):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/div/button').click()
            log.Logger().info('点击下一步')
        with allure.step('项目地图定位'):
            self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[4]/div[1]/div[3]')
            if self.driver.text_in('x, //*[@id="appMain-container"]/div[1]/div[4]/div[1]/div[3]', '详细地址'):
                self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[4]/div[2]/button[2]/span').click()
                log.Logger().info('点击下一步')
        with allure.step('负责人信息'):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[5]/div/button[2]/span').click()
            log.Logger().info('点击下一步')
        with allure.step('维保截止时间'):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[6]/div/button[2]/span').click()
            log.Logger().info('点击下一步')
        with allure.step('确认保存信息'):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/button[2]/span').click()
            log.Logger().info('点击确认保存信息')
            self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[8]/div/div[2]/button/span')
            log.Logger().info('保存成功')
            time.sleep(1)
        with allure.step("点击关闭"):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[8]/div/div[2]/button/span').click()
        with allure.step('进入项目列表'):
            IEMSEquipment(self.driver).enter_project()
            self.driver.wait_until(
                'x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[4]/div[2]/table/tbody/tr[1]/td[2]/div')
        with allure.step("验证是否新建成功"):
            projectName = self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[4]/div[2]/table/tbody/tr[1]/td[2]/div').text
            log.Logger().info("修改后项目名称：{}".format(projectName))
            self.check_assert(projectName, self.project.bar_project_name[3] + '编辑')


    def tearDown(self) -> None:
        # self.driver.driver.refresh()
        print('测试结束')

    @classmethod
    def tearDownClass(cls):
        try:
            mysql_backup.MysqlConn().restore_databases(cls.backup_files)
            pass
        except:
            pass
        cls.driver.driver.quit()


if __name__ == '__main__':
    unittest.main()

