import time
from time import sleep
from selenium.webdriver import Keys
from Comm import *
from IemsPage.basePage import BasePage, Base


class IEMSCollector(BasePage):
    """采集器配置相关"""

    def user_project_old(self, projectName):
        """选择2.0项目"""

        while True:
            self.driver.get_element('x, //*[@id="navbar-container"]/div[2]/span/div/div').click()
            self.driver.get_element('x, //*[@id="project-container"]').send_keys(projectName)
            self.driver.get_element('x, //*[@id="project-container"]').send_keys(Keys.DOWN)
            sleep(1)
            self.driver.wait_until('x, //body/div[last()]/div/div/ul/li[1]')
            if self.driver.assert_text('x, //body/div[last()]/div/div/ul/li[1]', projectName):
                self.driver.move_to_click('x, //body/div[last()]/div/div/ul/li[1]')
                break
            else:
                self.driver.move_to_click('x, //body/div[last()]/div/div/ul/li[1]')
                self.driver.get_element('x, //*[@id="project-container"]').send_keys(projectName)
        time.sleep(1)

    def enter_collector(self):
        """
        进入采集器配置页面
        :param projectName:
        :return:
        """

        self.driver.get_element('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/div').click()
        self.driver.wait_play('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul')
        self.driver.get_element(
            'x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[2]/div/li/div').click()
        self.driver.wait_play('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[2]/div/li/ul')
        self.driver.get_element('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div['
                                '2]/div/li/ul/div[5]/li/span').click()
        self.driver.wait_until('x, //*[@id="tab-001"]')
        log.Logger().info('进入采集器配置界面')
        time.sleep(1)

    def enter_collector_archive(self):
        """进入档案配置界面"""
        self.driver.wait_until('x, //*[@id="pane-001"]/div[1]/div[4]/div[2]/table/tbody/tr/td[8]/div/button[1]')
        self.driver.get_element(
            'x, //*[@id="pane-001"]/div[1]/div[4]/div[2]/table/tbody/tr/td[8]/div/button[1]').click()
        self.driver.wait_until('x, //*[@id="pane-0"]/div[1]/div[2]/button[1]/span/a')
        log.Logger().info('进入档案配置界面')
        time.sleep(1)

    def import_collector(self, collectorFile):
        """导入采集器配置表"""

        self.driver.get_element('x, //*[@id="pane-0"]/div[1]/div[2]/button[2]').click()
        self.driver.keys_control('x, /html/body', 'esc')
        self.driver.get_element('x, //*[@id="pane-0"]/div[1]/div[2]/button[2]').click()
        self.driver.wait_until('x, //body/div[last()]/div/div[last()]/div/div/div/input')
        self.driver.get_element('x, //body/div[last()]/div/div[last()]/div/div/div/input').send_keys(collectorFile)
        time.sleep(1)
