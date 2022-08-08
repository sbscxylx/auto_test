import unittest
import warnings
import os
from Comm.data import ReadData
from IemsPage.basePage import *
from IemsPage.iems_login.iems_login import IemsLogin


@unittest.skip
class TestIEMSLogin(unittest.TestCase):
    """测试登录"""

    # driver = Base('c')
    # file_path = os.path.abspath('../../IemsTestcase/Testdata/test_login_data.xlsx')
    # file_path = GetPath().get_abs_path('../Testdata/test_login_data.xlsx')
    # file_path = os.path.abspath(file_path)
    test_login_data = ReadData('test_login_data.xlsx').read_excel()
    # print(test_login_data)

    @classmethod
    def setUpClass(cls):
        cls.driver = Base('c')


    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)


    def test_right_login_01(self):
        """测试登录成功"""

        IemsLogin(self.driver).iems_login_old(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        self.driver.wait_until('x, //*[@id="navbar-container"]/div[3]/div[2]/div/span[2]')
        actual = self.driver.get_element('x, //*[@id="navbar-container"]/div[3]/div[2]/div/span[2]').text
        self.assertIn(self.test_login_data[0]['result'], actual)


    def test_wrong_login_02(self):
        """测试登录失败-密码错误"""
        IemsLogin(self.driver).iems_login_old(self.test_login_data[1]['user'], self.test_login_data[1]['pwd'])
        self.driver.wait_until('x, /html/body/div[3]/p')
        actual = self.driver.get_element('x, /html/body/div[3]/p').text
        self.assertIn(self.test_login_data[1]['result'], actual)


    def tearDown(self) -> None:
        self.driver.driver.refresh()
        print('测试结束')

    @classmethod
    def tearDownClass(cls):

        cls.driver.driver.quit()


if __name__ == '__main__':

    # suite = unittest.TestSuite()
    # # suite.addTest(TestIEMSLogin('test_right_login_01'))
    # dir = './'
    # suite.addTests(unittest.TestLoader().discover(start_dir=dir, pattern='test*.py'))
    unittest.main()
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)