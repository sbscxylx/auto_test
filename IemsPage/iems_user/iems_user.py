import time
from time import sleep
from Conf.readconfig import ReadConfig
from Comm.log import Logger
from IemsPage.basePage import BasePage, Base
from selenium.webdriver.common.keys import Keys


class IEMSUser(BasePage):

    def user_project(self, projectName):
        """选择项目"""

        while True:
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/div/div/div[2]/span/button/i').click()
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


    def enter_user(self):
        """
        进入用户档案
        :return:
        """

        self.driver.wait_until('x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[2]/div/div/li/div/span')
        self.driver.move_to_click('x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[2]/div/div/li/div/span')
        self.driver.move_to_click('x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[2]/div/div/li/ul/div[1]/div/li/span')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[1]/button[3]/span')
        if self.driver.assert_text('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[1]/button[3]/span', '开户'):
            Logger().info('进入用户档案界面')
            self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[8]/div/p')
        sleep(1)


    def open_user_a(self, mbrConsName, contacter, contactMobile):
        """
        用户开户
        :param mbrConsName: 用户户名
        :param contacter: 联 系 人
        :param contactMobile: 手机号码
        :return:
        """

        Logger().info('开始开户')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/form/div[1]/div/div/input')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/form/div[1]/div/div/input').send_keys(mbrConsName)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/form/div[4]/div/div/input').send_keys(contacter)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/form/div[5]/div/div/input').send_keys(contactMobile)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/form/div[6]/div/div/div[1]/input').click()
        sleep(1)
        self.driver.move_to_click('x, //body/div[last()]/div[1]/div[1]/div/ul/li/span')
        # self.driver.get_element('x, //body/div[last()]/div[1]/div[1]/div/ul/li/span').click()
        self.driver.get_element('x, //body/div[last()]/div[1]/div[last()]/div/ul/li/span').click()
        self.driver.get_element('x, //body/div[last()]/div[1]/div[last()]/div/ul/li/span').click()
        self.driver.get_element('x, //body/div[last()]/div[1]/div[last()]/div/ul/li/span').click()
        sleep(1)
        self.driver.get_element('x, //body/div[last()]/div[1]/div[last()]/div/ul/li/span').click()
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/form/div[7]/div/button').click()
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr[1]/td[8]/div/div/button[1]')
        Logger().info('等待表计加载')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr[1]/td[8]/div/div/button[1]').click()
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr[1]/td[6]/div/button[1]')
        Logger().info('等待计费方案加载')
        billingScheme = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr[1]/td[3]/div').text
        self.driver.move_to_click('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr[1]/td[6]/div/button[1]')
        Logger().info('选择计费方案{}'.format(billingScheme))
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr[1]/td[6]/div/button[1]')
        billingScheme2 = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr[1]/td[3]/div').text
        Logger().info('计费方案{}'.format(billingScheme2))
        if billingScheme == billingScheme2:
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr[2]/td[8]/div/div/button[1]').click()
            self.driver.wait_until(
                'x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr/td[6]/div/button[1]')
            self.driver.move_to_click(
                'x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr/td[6]/div/button[1]')
            self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr[1]/td[8]/div/div/button[1]')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[6]/button[2]').click()
        sleep(1)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[6]/button[2]').click()
        sleep(1)
        self.driver.wait_until('x, //body/div[last()-1]/div/div[last()]/div/span')
        if self.driver.assert_text('x, //body/div[last()-1]/div/div[last()]/div/span', '（表计底度错误会影响后续扣费，请仔细确认！）'):
            self.driver.get_element('x, //body/div[last()-1]/div/div[last()]/div[last()]/button[1]').click()
            Logger().info('开户确认')
            self.driver.wait_display('x, //body/div[last()-1]/div/p')
            self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[7]/div/p')
            self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[7]/div/p')
            self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div/h2')
            Logger().info('开户结束')
            sleep(1)


    def open_user(self, mbrConsName, contacter, contactMobile):
        """
        用户开户
        :param mbrConsName: 用户户名
        :param contacter: 联 系 人
        :param contactMobile: 手机号码
        :return:
        """

        Logger().info('开始开户')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/form/div[1]/div/div/input')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/form/div[1]/div/div/input').send_keys(mbrConsName)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/form/div[4]/div/div/input').send_keys(contacter)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/form/div[5]/div/div/input').send_keys(contactMobile)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/form/div[6]/div/div/div[1]/input').click()
        sleep(1)
        self.driver.move_to_click('x, //body/div[last()]/div[1]/div[1]/div/ul/li/span')
        # self.driver.get_element('x, //body/div[last()]/div[1]/div[1]/div/ul/li/span').click()
        self.driver.get_element('x, //body/div[last()]/div[1]/div[last()]/div/ul/li/span').click()
        self.driver.get_element('x, //body/div[last()]/div[1]/div[last()]/div/ul/li/span').click()
        self.driver.get_element('x, //body/div[last()]/div[1]/div[last()]/div/ul/li/span').click()
        sleep(1)
        self.driver.get_element('x, //body/div[last()]/div[1]/div[last()]/div/ul/li/span').click()
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/form/div[7]/div/button').click()
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr[1]/td[8]/div/div/button[1]')
        Logger().info('等待表计加载')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr[1]/td[8]/div/div/button[1]').click()
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr[1]/td[6]/div/button[1]')
        Logger().info('等待计费方案加载')
        billingScheme = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr[1]/td[3]/div').text
        self.driver.move_to_click('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr[1]/td[6]/div/button[1]')
        Logger().info('选择计费方案{}'.format(billingScheme))
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr[1]/td[6]/div/button[1]')
        billingScheme2 = self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr[1]/td[3]/div').text
        Logger().info('计费方案{}'.format(billingScheme2))
        if billingScheme == billingScheme2:
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr[2]/td[8]/div/div/button[1]').click()
            self.driver.wait_until(
                'x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr/td[6]/div/button[1]')
            self.driver.move_to_click(
                'x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/div/div[3]/table/tbody/tr/td[6]/div/button[1]')
            self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr[1]/td[8]/div/div/button[1]')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[6]/button[2]').click()
        sleep(1)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[6]/button[2]').click()
        sleep(1)
        self.driver.wait_until('x, //body/div[last()-1]/div/div[last()]/div/span')
        if self.driver.assert_text('x, //body/div[last()-1]/div/div[last()]/div/span', '（表计底度错误会影响后续扣费，请仔细确认！）'):
            self.driver.get_element('x, //body/div[last()-1]/div/div[last()]/div[last()]/button[1]').click()
            Logger().info('开户确认')
            self.driver.wait_display('x, //body/div[last()-1]/div/p')
            # self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[7]/div/p')
            self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[7]/div/p')
            self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div/h2')
            Logger().info('开户结束')
            sleep(1)


    def change_user(self, mbrConsName):
        """
        用户变更
        :param mbrConsName: 用户户名
        :return:
        """

        Logger().info('开始变更')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[2]/form/div[2]/div/div/input')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[2]/form/div[2]/div/div/input').send_keys(mbrConsName)
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[2]/div/button')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[2]/div/button').click()
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[2]/div[2]/div[3]/table/tbody/tr[1]/td[8]/div/div/button')
        Logger().info('等待表计加载')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[2]/div[6]/button[2]').click()
        sleep(1)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[2]/div[6]/button[2]').click()
        sleep(1)
        self.driver.wait_display('x, //body/div[last()-1]/div/p')
        # self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[7]/div/p')
        self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[7]/div/p')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[2]/div[1]/div[1]/div/h2')
        Logger().info('变更结束')
        sleep(1)


    def refund_money(self, refundMoney):
        """
        退款
        :param refundMoney: 退款金额
        :return:
        """
        Logger().info('开始退款')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[1]/div[3]/table/tbody/tr[1]/td[last()]/div/div/button')
        self.driver.move_to_click('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div/div[1]/div[3]/table/tbody/tr[1]/td[last()]/div/div/button')
        sleep(1)
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/section/div[2]/div/div[1]/div[2]/div/div[4]/div/input')
        self.driver.get_element(
            'x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/section/div[2]/div/div[1]/div[2]/div/div[4]/div/input').send_keys(refundMoney)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/section/div[2]/div/div[2]/button').click()
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/section/div[2]/div/div[2]/button[2]').click()
        self.driver.assert_text('x, //body/div[last()-1]/div/div[2]/div[1]/div[2]/p', '当前为现金退款，请确保用户收到现金')
        self.driver.get_element('x, //body/div[last()-1]/div/div[3]/button[2]').click()
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div/section/div[2]/div/div[1]/div[1]/div/div/h2')
        Logger().info('退款成功')
        sleep(1)

    def exit_user(self, zxygzdl=0, zxygzdl1=0, zxygzdl2=0, zxygzdl3=0, zxygzdl4=0, zxygzdls=0):
        """
        退租
        :param zxygzdl:
        :param zxygzdl1:
        :param zxygzdl2:
        :param zxygzdl3:
        :param zxygzdl4:
        :param zxygzdls:
        :return:
        """

        Logger().info('开始退租')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div[2]/div[4]/div['
                                '2]/table/tbody/tr[1]/td[5]/div/div/div[1]/div/input')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div[2]/div[4]/div['
                                '2]/table/tbody/tr[1]/td[5]/div/div/div[1]/div/input').send_keys(zxygzdl)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div[2]/div[4]/div['
                                '2]/table/tbody/tr[1]/td[5]/div/div/div[3]/div/div[1]/div[1]/div/input').send_keys(zxygzdl1)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div[2]/div[4]/div['
                                '2]/table/tbody/tr[1]/td[5]/div/div/div[3]/div/div[2]/div[1]/div/input').send_keys(zxygzdl2)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div[2]/div[4]/div['
                                '2]/table/tbody/tr[1]/td[5]/div/div/div[3]/div/div[1]/div[3]/div/input').send_keys(zxygzdl3)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div[2]/div[4]/div['
                                '2]/table/tbody/tr[1]/td[5]/div/div/div[3]/div/div[2]/div[3]/div/input').send_keys(zxygzdl4)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div[2]/div[4]/div['
                                '2]/table/tbody/tr[2]/td[5]/div/div/div[1]/div/input').send_keys(zxygzdls)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div[3]/button').click()
        Logger().info('输入底度')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div/button[2]')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div/button[2]').click()
        self.driver.assert_text('x, //body/div[last()-1]/div/div[2]/div[1]/div[2]/p', '确定退租吗？请核对是否已结清费用')
        self.driver.get_element('x, //body/div[last()-1]/div/div[3]/button[2]').click()
        sleep(1)
        self.driver.wait_display('x, //body/div[last()-1]/div/p')
        # self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[7]/div/p')
        self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[7]/div/p')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/section/main/div/div[2]/div[1]/div[1]/div/h2')
        Logger().info('退租成功')
        sleep(1)





if __name__ == '__main__':
    from IemsPage.iems_login.iems_login import IemsLogin

    b = Base('c')
    IemsLogin(b).iems_login_new(user='admin1', pwd='admin')
    b.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[3]/div/div[1]').click()
    IEMSUser(b).user_project('发布回归')
    IEMSUser(b).open_user('发布回归', '联系人', '15000000000')
