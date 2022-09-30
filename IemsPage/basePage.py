import shutil
from functools import wraps
from Comm import *
from selenium.webdriver import ActionChains, Keys
from Comm.log import Logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class Base:

    def __init__(self, browser):
        if browser == 'chrome' or browser == 'c':

            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.driver = webdriver.Chrome(options=options)

        elif browser == 'firefox' or browser == 'f':
            options = webdriver.FirefoxOptions()
            self.driver = webdriver.Firefox(options=options)
        elif browser == 'ie' or browser == 'i':
            options = webdriver.IeOptions()
            options.add_additional_option('excludeSwitches', ['enable-logging'])
            self.driver = webdriver.Ie(options=options)
        else:
            raise Exception('输入正确的浏览器！')

    def save_screen(self):
        '''
        页面截屏保存截图
        :return:
        '''

        try:
            self.rm_screenshoot()
            file_path = get_path.ensure_path_sep('/Log/screen') + f"\\{time.strftime('%Y-%m-%d%H', time.localtime(time.time()))}"
            Logger().info(f'文件路径{file_path}')
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_name = file_path + f"\\{time.strftime('%Y-%m-%d%H%M%S', time.localtime(time.time()))}" + "失败截图.png"
            Logger().info(f'文件名称{file_name}')
            self.driver.get_screenshot_as_file(file_name)
            with open(file_name, mode='rb') as f:
                file = f.read()
            allure.attach(file, '失败截图', allure.attachment_type.PNG)
            Logger().info("页面截图文件保存在：{}".format(file_name))
            return file_name

        except:
            Logger().info('截图失败')


    def rm_screenshoot(self, rm_day=1):

        try:
            for parent, dirnames, filenames in os.walk(get_path.ensure_path_sep('/Log/screen')):
                for dirname in dirnames:
                    fullname = parent + "/" + dirname  # 文件全称
                    createTime = int(os.path.getctime(r'{}'.format(fullname)))  # 文件创建时间
                    nDayAgo = (datetime.datetime.now() - datetime.timedelta(days=rm_day))  # 当前时间的n天前的时间
                    timeStamp = int(time.mktime(nDayAgo.timetuple()))
                    if createTime < timeStamp:  # 创建时间在n天前的文件删除
                        shutil.rmtree(os.path.join(parent, dirname))
        except:
            print('没有可删除截图')

    def open_url(self, url):
        """
        打开网址
        :param url:请求链接
        :return:
        """
        self.driver.get(url)
        self.driver.maximize_window()

    def selector_convert_to_locator(self, selector):
        """
        把selector转换成定位元素的locator
        :param selector: 类似于'i,account'
        :return: locator元组。类似于(By.ID,account)
        """
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
        """
        找单个元素
        :param selector: 类似于'i,account'
        :return: 网页元素
        """
        locator = self.selector_convert_to_locator(selector)
        element = self.driver.find_element(*locator)
        return element

    def clear_and_input(self, selector, value):
        """
        清空文本再输入
        :param selector:
        :param value:
        :return:
        """

        self.get_element(selector).clear()
        self.get_element(selector).send_keys(value)

    def sleep(self, second):
        """
        等待
        :param second:秒
        :return:
        """
        time.sleep(second)

    def date_day(self, symbol='minus', index=0):
        """
        日期获取
        :param symbol: [minus,plus]
        :param index: 天数
        :return:
        """

        if symbol == 'minus':
            time = (datetime.datetime.now() - datetime.timedelta(days=index)).strftime("%Y-%m-%d")
            Logger().info(time)
            return time

        if symbol == 'plus':
            time = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime("%Y-%m-%d")
            Logger().info(time)
            return time

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
        self.sleep(0.5)

    def wait_play(self, selector, timeout=20, poll_frequency=0.2):
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
        self.sleep(0.5)

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
        self.sleep(0.5)

    def wait_clickable(self, selector, timeout=20, poll_frequency=0.2):
        """
        等待直到元素可点击
        :param selector:
        :param timeout:
        :param poll_frequency:
        :return:
        """

        locator = self.selector_convert_to_locator(selector)
        method = EC.element_to_be_clickable(locator)
        WebDriverWait(self.driver, timeout, poll_frequency).until(method)
        self.sleep(0.5)

    def isPresent(self, selector, timeout=20):
        """
        存在的元素返回True;不存在的元素返回False
        :param selector:
        :return:
        """

        try:
            self.wait_until(timeout=timeout, selector=selector)
            self.get_element(selector)
            return True
        except:
            return False

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

    def text_in(self, selector, value):
        flag = True
        element_text = self.get_element(selector).text
        Logger().info('实际数据{}'.format(element_text))
        if value in element_text:
            Logger().info(value + '数据存在')
        else:
            flag = False
            Logger().info(value + '数据不存在')
        return flag

    def switch_to_frame(self, selector):
        element = self.get_element(selector)
        self.driver.switch_to.frame(element)

    def select_by_index(self, selector, index):
        """
        根据index定位select下拉框中的元素
        :param selector: 类似于'i,account'
        :param index: 下拉框中的元素序号
        :return:
        """
        element = self.get_element(selector)
        select = Select(element)
        select.select_by_index(int(index))

    def select_by_visible_text(self, selector, text):
        """
        根据元素文本中包含的文本，获取下拉框中的元素
        :param selector: 类似于'i,account'
        :param text: 下拉框中元素文本中包含的文本
        :return:
        """
        element = self.get_element(selector)
        select = Select(element)
        select.select_by_visible_text(text)

    def select_by_value(self, selector, value):
        """
        根据元素文本中包含的文本，获取下拉框中的元素
        :param selector: 类似于'i,account'
        :param value: 下拉框中元素的value值
        :return:
        """
        element = self.get_element(selector)
        select = Select(element)
        select.select_by_value(value)

    def alert_accept(self):
        self.driver.switch_to.alert.accept()

    def alert_dismiss(self):
        self.driver.switch_to.alert.dismiss()

    def move_to_click(self, selector):
        """
        强制点击
        :param selector:
        :return:
        """
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
            self.get_element(selector)
        except:
            element_existance = False
        return element_existance

    def action_chains(self, action, selector):
        """
        鼠标操作
        :param action: ['左键', '右键']
        :param selector:
        :return:
        """
        element = self.get_element(selector)
        if action == '右键':
            ActionChains(self.driver).context_click(element).perform()
        if action == '左键':
            ActionChains(self.driver).click(element).perform()

    def keys_control(self, selector, keys):

        if keys == 'enter':
            self.get_element(selector).send_keys(Keys.ENTER)
        if keys == 'esc':
            self.get_element(selector).send_keys(Keys.ESCAPE)


class BasePage:

    def __init__(self, driver: Base):
        self.driver = driver


class Screen:

    def __new__(cls, func_or_cls=None):
        self = object.__new__(cls)
        if func_or_cls:
            return self(func_or_cls)
        else:
            return self

    def __init__(self, func_or_class=None):
        pass

    def __call__(self, func_or_cls=None):
        @wraps(func_or_cls)
        def inner(*args, **kwargs):
            try:
                return func_or_cls(*args, **kwargs)
            except:
                args[0].driver.save_screen()
                raise

        return inner


if __name__ == '__main__':
    # b = Base('c')
    # b.save_screen()
    # print(int(os.path.getctime('C:\Users\Administrator\Desktop\UIAutoTest\Log\screen/2022-09-081454')))
    # os.rmdir(r'C:\Users\Administrator\Desktop\UIAutoTest\Log\screen\2022-09-0815')
    file_path = get_path.ensure_path_sep(
        '/Log/screen') + f"\\{time.strftime('%Y-%m-%d%H', time.localtime(time.time()))}"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_name = file_path + f"\\{time.strftime('%Y-%m-%d%H%M%S', time.localtime(time.time()))}" + "失败截图.png"
    driver.get_screenshot_as_file(file_name)
    with open(file_name, mode='rb') as f:
        print('截图开始3')
        file = f.read()