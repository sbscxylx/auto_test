import csv
import time
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
        '''
        等待直达元素出现
        :param selector: 类似于'i,account'
        :param timeout: 超时时间
        :param poll_frequency: 使用方法间隔
        :return:
        '''
        locator = self.selector_convert_to_locator(selector)
        method = EC.presence_of_element_located(locator)
        WebDriverWait(self.driver, timeout, poll_frequency).until(method)

    def assert_text(self, selector, value, success_text='', failure_text=''):
        locator = self.selector_convert_to_locator(selector)
        assert_text = EC.text_to_be_present_in_element_value(locator, value)
        if assert_text:
            print(success_text)
        else:
            print(failure_text)

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
