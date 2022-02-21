from time import sleep

import self as self

from Conf.readconfig import ReadConfig
from IemsPage.basePage import BasePage, Base


class IemsLogin(BasePage):

    url_old = ReadConfig().get_url('old_url')
    url_new = ReadConfig().get_url('new_url')

    def iems_login_old(self, user, pwd, url=url_old):
        driver = self.driver
        driver.open_url(url)
        driver.get_element('x, //*[@id="app"]/div/div[1]/div/div[2]/div/ul/li[5]/span/div[2]').click()
        driver.wait_until('x, //*[@id="app"]/div/form/div[2]/div/div/input')
        sleep(2)
        driver.get_element('x, //*[@id="app"]/div/form/div[2]/div/div/input').send_keys(user)
        driver.get_element('x, //*[@id="app"]/div/form/div[3]/div/div/input').send_keys(pwd)
        driver.get_element('x, //*[@id="app"]/div/form/div[5]/div/button/span/span').click()




    def iems_login_new(self, user, pwd, url=url_new):
        driver = self.driver
        driver.open_url(url)
        driver.get_element('x, //*[@id="app"]/div/div[1]/div/div[2]/div/ul/li[5]/span/div[2]').click()
        driver.wait_until('x, //*[@id="app"]/div/div[2]/form/div[2]/div/div/input')
        driver.get_element('x, //*[@id="app"]/div/div[2]/form/div[2]/div/div/input').send_keys(user)
        driver.get_element('x, //*[@id="app"]/div/div[2]/form/div[3]/div/div/input').send_keys(pwd)
        driver.get_element('x, //*[@id="app"]/div/div[2]/form/div[5]/div/button').click()
        driver.wait_until('x, //*[@id="navbar-container"]/div[3]/div[2]/div/span[2]')
        driver.assert_text('x, //*[@id="app"]/div/div[2]/div/div/div[5]/div/div', ' 欢迎您!' + user, '登录成功！',
                           '登录失败！')



if __name__ == '__main__':
    b = Base('c')
    IemsLogin(b).iems_login_old(user='admin1', pwd='admin')
    # IemsLogin(b).iems_login_new(user='admin1', pwd='admin')