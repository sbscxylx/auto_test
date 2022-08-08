import csv
import time

from selenium.webdriver import ActionChains
from Comm.log import Logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from Conf.readconfig import ReadConfig
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Base:

    def __init__(self, browser):
        if browser == 'chrome' or browser == 'c':
            self.driver = webdriver.Chrome()
        elif browser == 'firefox' or browser == 'f':
            self.driver = webdriver.Firefox()
        elif browser == 'ie' or browser == 'i':
            self.driver = webdriver.Ie()
        else:
            raise Exception('输入正确的浏览器！')

    def open_url(self, url):
        self.driver.get(url)
        self.driver.maximize_window()

    def selector_convert_to_locator(self, selector):
        '''
        把selector转换成定位元素的locator
        :param selector: 类似于'i,account'
        :return: locator元组。类似于(By.ID,account)
        '''
        selector_key = selector.split(',')[0]
        selector_value = selector.split(',')[1]
        if selector_key == 'id' or selector_key == 'i':
            locator = (By.ID, selector_value)
        elif selector_key == 'xpath' or selector_key == 'x':
            locator = (By.XPATH, selector_value)
        elif selector_key == 'class' or selector_key == 'c':
            locator = (By.CLASS_NAME, selector_value)
        elif selector_key == 'name' or selector_key == 'n':
            locator = (By.NAME, selector_value)
        elif selector_key == 'css' or selector_key == 's':
            locator = (By.CSS_SELECTOR, selector_value)
        elif selector_key == 'link' or selector_key == 'l':
            locator = (By.LINK_TEXT, selector_value)
        elif selector_key == 'partial' or selector_key == 'p':
            locator = (By.PARTIAL_LINK_TEXT, selector_value)
        elif selector_key == 'tag' or selector_key == 't':
            locator = (By.TAG_NAME, selector_value)
        else:
            raise Exception('输入正确的选择器！')
        return locator

    def get_element(self, selector):
        '''
        找单个元素
        :param selector: 类似于'i,account'
        :return: 网页元素
        '''
        locator = self.selector_convert_to_locator(selector)
        element = self.driver.find_element(*locator)
        return element

    def sleep(self, second):
        time.sleep(second)

    def wait_until(self, selector, timeout=20, poll_frequency=0.2):
        """
        等待直达元素出现
        :param selector: 类似于'i,account'
        :param timeout: 超时时间
        :param poll_frequency: 使用方法间隔
        :return:
        """
        locator = self.selector_convert_to_locator(selector)
        method = EC.presence_of_element_located(locator)
        WebDriverWait(self.driver, timeout, poll_frequency).until(method)

    def wait_play(self, selector,  timeout=20, poll_frequency=0.2):
        """
        等待元素可见
        :param selector:
        :param timeout:
        :param poll_frequency:
        :return:
        """
        locator = self.selector_convert_to_locator(selector)
        method = EC.visibility_of_element_located(locator)
        WebDriverWait(self.driver, timeout, poll_frequency).until(method)

    def wait_display(self, selector, timeout=20, poll_frequency=0.2):
        """
        等待直到元素消失
        :param selector:
        :param timeout:
        :param poll_frequency:
        :return:
        """

        locator = self.selector_convert_to_locator(selector)
        method = EC.invisibility_of_element_located(locator)
        WebDriverWait(self.driver, timeout, poll_frequency).until(method)

    def assert_text(self, selector, value, success_text='', failure_text=''):
        flag = True
        element_text = self.get_element(selector).text
        Logger().info('实际数据{}'.format(element_text))
        if element_text == value:
            Logger().info(success_text)
        else:
            flag = False
            print(failure_text)
        return flag


    def switch_to_frame(self, selector):
        element = self.get_element(selector)
        self.driver.switch_to.frame(element)

    def select_by_index(self, selector, index):
        '''
        根据index定位select下拉框中的元素
        :param selector: 类似于'i,account'
        :param index: 下拉框中的元素序号
        :return:
        '''
        element = self.get_element(selector)
        select = Select(element)
        select.select_by_index(int(index))

    def select_by_visible_text(self, selector, text):
        '''
        根据元素文本中包含的文本，获取下拉框中的元素
        :param selector: 类似于'i,account'
        :param text: 下拉框中元素文本中包含的文本
        :return:
        '''
        element = self.get_element(selector)
        select = Select(element)
        select.select_by_visible_text(text)

    def select_by_value(self, selector, value):
        '''
        根据元素文本中包含的文本，获取下拉框中的元素
        :param selector: 类似于'i,account'
        :param value: 下拉框中元素的value值
        :return:
        '''
        element = self.get_element(selector)
        select = Select(element)
        select.select_by_value(value)

    def alert_accept(self):
        self.driver.switch_to.alert.accept()

    def alert_dismiss(self):
        self.driver.switch_to.alert.dismiss()

    def move_to_click(self, selector):
        element = self.get_element(selector)
        time.sleep(1)
        self.driver.execute_script('arguments[0].click();', element)

    def element_existance(self, selector):
        """
        判断元素是否存在
        :param selector:
        :return:
        """
        element_existance = True
        try:
            element = self.get_element(selector)
        except:
            element_existance = False
        return element_existance

    def action_chains(self, action, selector):
        element = self.get_element(selector)
        if action == '右键':
            ActionChains(self.driver).context_click(element).perform()
        if action == '左键':
            ActionChains(self.driver).click(element).perform()



class BasePage:

    def __init__(self, driver: Base):
        self.driver = driver


if __name__ == '__main__':
    b = Base('c')
    url = ReadConfig().get_url('base_url')
    b.open_url(url)
    # b.get_element('i,account').send_keys('admin')
    # b.get_element('i,password').send_keys('123456')
    # b.get_element('i,submit').click()
    # b.sleep(2)
    # b.get_element('x,//*[@id="s-menu-superadmin"]/button').click()
    # b.switch_to_frame('i,iframe-superadmin')
    # b.get_element('x,//*[@id="shortcutBox"]/div/div[1]/div/a/h3').click()
