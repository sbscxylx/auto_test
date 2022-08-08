import time
from time import sleep
from Conf.readconfig import ReadConfig
from IemsPage.basePage import BasePage, Base
from Comm.log import Logger


class IemsLogin(BasePage):

    sit_url_old = ReadConfig().get_url('sit_old_url')
    sit_url_new = ReadConfig().get_url('sit_new_url')
    a_url_old = ReadConfig().get_url('a_old_url')
    a_url_new = ReadConfig().get_url('a_new_url')

    def iems_login_old(self, user, pwd, url=sit_url_old):
        driver = self.driver
        driver.open_url(url)
        driver.get_element('x, //*[@id="app"]/div/div[1]/div/div[2]/div/ul/li[5]/span/div[2]').click()
        driver.wait_until('x, //*[@id="app"]/div/form/div[2]/div/div/input')
        driver.get_element('x, //*[@id="app"]/div/form/div[2]/div/div/input').send_keys(user)
        driver.get_element('x, //*[@id="app"]/div/form/div[3]/div/div/input').send_keys(pwd)
        driver.wait_until('x, //*[@id="app"]/div/form/div[5]/div/button/span/span')
        driver.get_element('x, //*[@id="app"]/div/form/div[5]/div/button/span/span').click()
        sleep(2)
        if driver.element_existance('x, //*[@class="el-dialog__body"]'):
            self.driver.wait_until('x, //*[@class="el-dialog__body"]//button')
            driver.get_element('x, //*[@class="el-dialog__body"]//button').click()
        Logger().info('2.0登录成功')
        sleep(1)


    def iems_login_new(self, user, pwd, url=sit_url_new):
        driver = self.driver
        driver.open_url(url)
        driver.get_element('x, //*[@id="app"]/div/div[1]/div/div[2]/div/ul/li[5]/span/div[2]').click()
        driver.wait_until('x, //*[@id="app"]/div/div[2]/form/div[2]/div/div/input')
        driver.get_element('x, //*[@id="app"]/div/div[2]/form/div[2]/div/div/input').send_keys(user)
        driver.get_element('x, //*[@id="app"]/div/div[2]/form/div[3]/div/div/input').send_keys(pwd)
        driver.wait_until('x, //*[@id="app"]/div/div[2]/form/div[5]/div/button')
        driver.get_element('x, //*[@id="app"]/div/div[2]/form/div[5]/div/button').click()
        sleep(2)
        if driver.element_existance('x, //*[@class="el-dialog__body"]'):
            self.driver.wait_until('x, //*[@class="el-dialog__body"]//button')
            driver.get_element('x, //*[@class="el-dialog__body"]//button').click()
        Logger().info('2.3登录成功')


    def a_login_old(self, user, pwd, url=a_url_old):
        driver = self.driver
        driver.open_url(url)
        driver.get_element('x, //*[@id="app"]/div/div[1]/div/div[2]/div/ul/li[5]/span/div[2]').click()
        driver.wait_until('x, //*[@id="app"]/div/form/div[2]/div/div/input')
        driver.get_element('x, //*[@id="app"]/div/form/div[2]/div/div/input').send_keys(user)
        driver.get_element('x, //*[@id="app"]/div/form/div[3]/div/div/input').send_keys(pwd)
        driver.wait_until('x, //*[@id="app"]/div/form/div[5]/div/button/span/span')
        driver.get_element('x, //*[@id="app"]/div/form/div[5]/div/button/span/span').click()
        sleep(2)
        if driver.element_existance('x, //*[@class="el-dialog__body"]'):
            self.driver.wait_until('x, //*[@class="el-dialog__body"]//button')
            driver.get_element('x, //*[@class="el-dialog__body"]//button').click()
        Logger().info('2.0登录成功')
        sleep(1)


    def a_login_new(self, user, pwd, url=a_url_new):
        driver = self.driver
        driver.open_url(url)
        driver.get_element('x, //*[@id="app"]/div/div[1]/div/div[2]/div/ul/li[5]/span/div[2]').click()
        driver.wait_until('x, //*[@id="app"]/div/div[2]/form/div[2]/div/div/input')
        driver.get_element('x, //*[@id="app"]/div/div[2]/form/div[2]/div/div/input').send_keys(user)
        driver.get_element('x, //*[@id="app"]/div/div[2]/form/div[3]/div/div/input').send_keys(pwd)
        driver.wait_until('x, //*[@id="app"]/div/div[2]/form/div[5]/div/button')
        driver.get_element('x, //*[@id="app"]/div/div[2]/form/div[5]/div/button').click()
        sleep(2)
        if driver.element_existance('x, //*[@class="el-dialog__body"]'):
            self.driver.wait_until('x, //*[@class="el-dialog__body"]//button')
            driver.get_element('x, //*[@class="el-dialog__body"]//button').click()
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div[3]/div/div[1]')
        Logger().info('2.3登录成功')


if __name__ == '__main__':
    b = Base('c')
    # IemsLogin(b).iems_login_old(user='admin1', pwd='admin')
    # IemsLogin(b).iems_login_old(user='admin1', pwd='admin')
    IemsLogin(b).a_login_old('admin', '9999#hz')