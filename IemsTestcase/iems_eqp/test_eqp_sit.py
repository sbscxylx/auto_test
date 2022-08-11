import unittest
import warnings
from Comm.data import ReadData
from Comm.mysql_backup import MysqlConn
from IemsPage.basePage import *
from IemsPage.iems_eqp.iems_eqp import IEMSEquipment
from IemsPage.iems_login.iems_login import IemsLogin


class TestIEMSEqp(unittest.TestCase):
    """测试档案相关"""

    Logger().rm_log()
    databases = MysqlConn().read_all_databases()
    backup_files = MysqlConn().backup_databases(databases,
                                                ['bar_measure', 'bar_gateway', 'bar_building', 'bar_container'])

    # file_path = os.path.abspath('../../IemsTestcase/Testdata/test_login_data.xlsx')
    # file_path = GetPath().get_abs_path('../Testdata/test_login_data.xlsx')
    # file_path = os.path.abspath(file_path)
    # driver = Base('c')
    test_login_data = ReadData('test_login_data.xlsx').read_excel()
    test_measure_data = ReadData('test_measure_data.xls').read_excel()
    test_project_data = ReadData('test_project_data.xlsx').read_excel()
    test_gateway_data = ReadData('test_gateway_data.xls').read_excel()

    Logger().info(test_measure_data)
    Logger().info(test_project_data)
    Logger().info(test_gateway_data)

    def check_assert(self, actual, eqpNo):
        """
        确认数据是否导入
        :param actual:
        :param eqpNo:
        :return:
        """
        Logger().info('预期数据{}, 实际数据{}'.format(eqpNo, actual))
        self.assertEqual(str(eqpNo), actual)

    @classmethod
    def setUpClass(cls):
        cls.driver = Base('c')

    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)


    def test_01_import_gateway(self):
        """测试正常导入376网关"""

        IemsLogin(self.driver).iems_login_old(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        IEMSEquipment(self.driver).enter_eqp(self.test_project_data[1]['project_name'])
        IEMSEquipment(self.driver).import_eqp('网关', r'C:\Users\Administrator\Desktop\UIAutoTest\IemsTestcase\Testdata'
                                                    r'\test_gateway_data.xls')
        IEMSEquipment(self.driver).select_eqp('网关', self.test_gateway_data[0]['智能网关编号'])
        time.sleep(10)
        actual = self.driver.get_element(
            'x, //*[@id="pane-网关"]/div[3]/div[4]/div[2]/table/tbody/tr/td[2]/div/button[1]/span').text
        self.check_assert(actual, self.test_gateway_data[0]['智能网关编号'])


    def test_02_import_eqp(self):
        """测试正常导入表计"""

        # IemsLogin(self.driver).iems_login_old(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # IEMSEquipment(self.driver).enter_eqp(self.test_project_data[1]['project_name'])

        IEMSEquipment(self.driver).import_eqp('00080001',
                                              r'C:\Users\Administrator\Desktop\UIAutoTest\IemsTestcase\Testdata'
                                              r'\test_measure_data.xls')

        # 核对表计1（485）
        IEMSEquipment(self.driver).select_eqp('00080001', self.test_measure_data[0]['测量表计编号'])
        meter_no = self.driver.get_element(
            'x, //*[@id="pane-电表"]/div[3]/div[4]/div[2]/table/tbody/tr/td[3]/div/button[1]/span').text
        self.check_assert(meter_no, self.test_measure_data[0]['测量表计编号'])
        gateway_no = self.driver.get_element(
            'x, //*[@id="pane-电表"]/div[3]/div[3]/table/tbody/tr[1]/td[5]/div/span').text
        self.check_assert(gateway_no, '')
        comm_type = self.driver.get_element('x, //*[@id="pane-电表"]/div[3]/div[3]/table/tbody/tr[1]/td[6]/div').text
        self.check_assert(comm_type, '485')

        # 核对表计2（485关联网关）
        self.driver.get_element('x, //*[@id="pane-电表"]/div[2]/button').click()  # 点击重置
        self.driver.wait_display('x, //*[@id="pane-电表"]/div[3]/div[8]')
        IEMSEquipment(self.driver).select_eqp('00080001', self.test_measure_data[1]['测量表计编号'])
        meter_no = self.driver.get_element(
            'x, //*[@id="pane-电表"]/div[3]/div[4]/div[2]/table/tbody/tr/td[3]/div/button[1]/span').text
        self.check_assert(meter_no, self.test_measure_data[1]['测量表计编号'])
        gateway_no = self.driver.get_element(
            'x, //*[@id="pane-电表"]/div[3]/div[3]/table/tbody/tr[1]/td[5]/div/span').text
        self.check_assert(gateway_no, self.test_gateway_data[0]['智能网关编号'])

        # 核对表计3（NB表）
        self.driver.get_element('x, //*[@id="pane-电表"]/div[2]/button').click()
        self.driver.wait_display('x, //*[@id="pane-电表"]/div[3]/div[8]')
        IEMSEquipment(self.driver).select_eqp('00080001', self.test_measure_data[2]['测量表计编号'])
        meter_no = self.driver.get_element(
            'x, //*[@id="pane-电表"]/div[3]/div[4]/div[2]/table/tbody/tr/td[3]/div/button[1]/span').text
        self.check_assert(meter_no, self.test_measure_data[2]['测量表计编号'])
        gateway_no = self.driver.get_element(
            'x, //*[@id="pane-电表"]/div[3]/div[3]/table/tbody/tr[1]/td[5]/div/span').text
        self.check_assert(gateway_no, self.test_measure_data[2]['测量表计编号'])
        comm_type = self.driver.get_element('x, //*[@id="pane-电表"]/div[3]/div[3]/table/tbody/tr[1]/td[6]/div').text
        self.check_assert(comm_type, '电信NB-IoT')

        # 核对表计4（GPRS/4G）
        self.driver.get_element('x, //*[@id="pane-电表"]/div[2]/button').click()
        self.driver.wait_display('x, //*[@id="pane-电表"]/div[3]/div[8]')
        IEMSEquipment(self.driver).select_eqp('00080001', self.test_measure_data[3]['测量表计编号'])
        meter_no = self.driver.get_element(
            'x, //*[@id="pane-电表"]/div[3]/div[4]/div[2]/table/tbody/tr/td[3]/div/button[1]/span').text
        self.check_assert(meter_no, self.test_measure_data[3]['测量表计编号'])
        gateway_no = self.driver.get_element(
            'x, //*[@id="pane-电表"]/div[3]/div[3]/table/tbody/tr[1]/td[5]/div/span').text
        self.check_assert(gateway_no, self.test_measure_data[3]['测量表计编号'])
        comm_type = self.driver.get_element('x, //*[@id="pane-电表"]/div[3]/div[3]/table/tbody/tr[1]/td[6]/div').text
        self.check_assert(comm_type, 'GPRS/4G')


    def test_03_connect_gateway(self):
        """测试关联网关"""

        # IemsLogin(self.driver).iems_login_old(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # IEMSEquipment(self.driver).enter_eqp(self.test_project_data[1]['project_name'])
        IEMSEquipment(self.driver).select_type('00080001')
        IEMSEquipment(self.driver).select_eqp('00080001', self.test_measure_data[0]['测量表计编号'])
        IEMSEquipment(self.driver).connect_gateway('00080001')
        IEMSEquipment(self.driver).select_eqp('00080001', self.test_measure_data[0]['测量表计编号'])
        gateway_no = self.driver.get_element(
            'x, //*[@id="pane-电表"]/div[3]/div[3]/table/tbody/tr[1]/td[5]/div/span').text
        Logger().info('成功关联网关'.format(gateway_no))
        self.assertNotEqual(gateway_no, '')


    def test_04_disconnect_gateway(self):
        """测试解绑网关"""

        # IemsLogin(self.driver).iems_login_old(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # IEMSEquipment(self.driver).enter_eqp(self.test_project_data[1]['project_name'])
        # IEMSEquipment(self.driver).select_type('00080001')
        # IEMSEquipment(self.driver).select_eqp('00080001', self.test_measure_data[0]['测量表计编号'])
        # IEMSEquipment(self.driver).select_eqp('00080001', '202205310001')
        IEMSEquipment(self.driver).disconnect_gateway('00080001')
        IEMSEquipment(self.driver).select_eqp('00080001', self.test_measure_data[0]['测量表计编号'])
        gateway_no = self.driver.get_element(
            'x, //*[@id="pane-电表"]/div[3]/div[3]/table/tbody/tr[1]/td[5]/div/span').text
        Logger().info(gateway_no)
        self.assertEqual(gateway_no, '')


    def test_05_edit_bulid(self):
        """测试新增建筑"""

        # IemsLogin(self.driver).iems_login_old(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        IEMSEquipment(self.driver).enter_project_space(self.test_project_data[1]['project_name'])
        # 新增建筑
        self.driver.action_chains('右键', 'x, //*[@id="left"]/div[3]/div[1]/div[1]/span[2]/span/span')
        IEMSEquipment(self.driver).add_building('build', '新增建筑', '新增建筑', 100, '新增建筑')
        self.driver.wait_until('x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[1]/span[2]/span/span')

        # 新增楼栋
        self.driver.action_chains('右键', 'x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[1]/span[2]/span/span')
        IEMSEquipment(self.driver).add_building('block', '新增楼栋', '新增楼栋', 100, '新增楼栋')
        self.driver.wait_until('x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[1]/span[2]/span/span')

        # 新增楼层
        self.driver.action_chains('右键', 'x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[1]/span['
                                        '2]/span/span')
        IEMSEquipment(self.driver).add_building('floor', '新增楼层', '新增楼层', 100, '新增楼层')
        self.driver.wait_until('x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/span['
                               '2]/span/span')

        # 新增房间
        self.driver.action_chains('右键', 'x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div['
                                        '1]/span[2]/span/span')
        IEMSEquipment(self.driver).add_building('room', '新增房间', '新增房间', 100, '新增房间')
        self.driver.wait_until('x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/div['
                               '1]/span[2]/span/span')


    def test_06_add_measure(self):
        """测试新增表计"""

        # IemsLogin(self.driver).iems_login_old(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # IEMSEquipment(self.driver).enter_project_space(self.test_project_data[1]['project_name'])
        self.driver.action_chains('右键', 'x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div['
                                        '2]/div/div[1]/span[2]/span/span')
        IEMSEquipment(self.driver).add_measure(self.test_measure_data[0]['测量表计编号'],
                                               'x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div['
                                               '2]/div/div[2]/div/div[1]/span[2]/span/span')
        bar_measure_no = self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[2]/div['
                                                 '2]/div[3]/table/tbody/tr/td[1]/div/div').text
        self.check_assert(bar_measure_no, self.test_measure_data[0]['测量表计编号'])


    def test_07_edit_measure(self):
        """测试修改表计"""

        # IemsLogin(self.driver).iems_login_old(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # IEMSEquipment(self.driver).enter_project_space(self.test_project_data[1]['project_name'])
        # self.driver.get_element('x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/div['
        #                         '1]/span[2]/span/span').click()
        # self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[2]/div[2]/div['
        #                        '3]/table/tbody/tr/td[11]/div/button[1]/span')
        # bar_measure_no = self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[2]/div['
        #                                          '2]/div[3]/table/tbody/tr/td[1]/div/div').text
        # self.check_assert(bar_measure_no, self.test_measure_data[0]['测量表计编号'])
        install_time_old = self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[2]/div['
                                                   '2]/div[3]/table/tbody/tr/td[7]/div/div').text
        IEMSEquipment(self.driver).edit_measure()
        install_time_new = self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[2]/div['
                                                   '2]/div[3]/table/tbody/tr/td[7]/div/div').text
        self.assertNotEqual(install_time_old, install_time_new)
        Logger().info('维护前安装时间{}, 维护后安装时间{}'.format(install_time_old, install_time_new))


    def test_08_unbind_measure(self):
        """测试解绑表计"""

        # IemsLogin(self.driver).iems_login_old(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # IEMSEquipment(self.driver).enter_project_space(self.test_project_data[1]['project_name'])
        self.driver.wait_until('x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/div['
                               '1]/span[2]/span/span')
        self.driver.get_element('x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/div['
                                '1]/span[2]/span/span').click()
        self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[2]/div[2]/div['
                               '3]/table/tbody/tr/td[11]/div/button[1]/span')
        bar_measure_no = self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[2]/div['
                                                 '2]/div[3]/table/tbody/tr/td[1]/div/div').text
        self.check_assert(bar_measure_no, self.test_measure_data[0]['测量表计编号'])
        IEMSEquipment(self.driver).unbind_measure()
        self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[2]/div[2]/div[3]/div/span')
        self.driver.assert_text('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[2]/div[2]/div[3]/div/span',
                                '暂无数据')
        self.driver.action_chains('右键', 'x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div['
                                        '1]/span[2]/span/span')


    def test_09_delete_gateway(self):
        """删除网关"""

        IemsLogin(self.driver).iems_login_old(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        IEMSEquipment(self.driver).enter_eqp(self.test_project_data[1]['project_name'])
        IEMSEquipment(self.driver).select_type('网关')

        # 删除376设备网关会删除下面所有表计
        IEMSEquipment(self.driver).select_eqp('网关', self.test_gateway_data[0]['智能网关编号'])
        IEMSEquipment(self.driver).delete_eqp('网关')
        # IEMSEquipment(self.driver).select_eqp('网关', self.test_gateway_data[0]['智能网关编号'])
        gateway_no_new = self.driver.get_element('x, //*[@id="pane-网关"]/div[3]/div[3]/div/span').text
        self.check_assert(gateway_no_new, '暂无数据')
        Logger().info('网关{}已被删除'.format(self.test_gateway_data[0]['智能网关编号']))
        time.sleep(1)
        IEMSEquipment(self.driver).select_type('00080001')
        IEMSEquipment(self.driver).select_eqp('00080001', self.test_measure_data[1]['测量表计编号'])
        bar_measure_new = self.driver.get_element('x, //*[@id="pane-电表"]/div[3]/div[3]/div/span').text
        self.check_assert(bar_measure_new, '暂无数据')
        Logger().info('网关绑定表计{}已被删除'.format(self.test_measure_data[1]['测量表计编号']))

        # 删除NB/GPRS设备网关会删除对应表计
        IEMSEquipment(self.driver).select_type('网关')
        IEMSEquipment(self.driver).select_eqp('网关', self.test_measure_data[2]['测量表计编号'])
        IEMSEquipment(self.driver).delete_eqp('网关')
        gateway_no_new = self.driver.get_element('x, //*[@id="pane-网关"]/div[3]/div[3]/div/span').text
        self.check_assert(gateway_no_new, '暂无数据')
        Logger().info('网关{}已被删除'.format(self.test_measure_data[2]['测量表计编号']))
        IEMSEquipment(self.driver).select_type('00080001')
        IEMSEquipment(self.driver).select_eqp('00080001', self.test_measure_data[2]['测量表计编号'])
        bar_measure_new = self.driver.get_element('x, //*[@id="pane-电表"]/div[3]/div[3]/div/span').text
        self.check_assert(bar_measure_new, '暂无数据')
        Logger().info('网关绑定表计{}已被删除'.format(self.test_measure_data[2]['测量表计编号']))


    def test_10_delete_measure(self):
        """删除表计"""
        #
        # IemsLogin(self.driver).iems_login_old(self.test_login_data[0]['user'], self.test_login_data[0]['pwd'])
        # IEMSEquipment(self.driver).enter_eqp(self.test_project_data[1]['project_name'])

        # 删除485表计
        IEMSEquipment(self.driver).select_type('00080001')
        IEMSEquipment(self.driver).select_eqp('00080001', self.test_measure_data[0]['测量表计编号'])
        IEMSEquipment(self.driver).delete_eqp('00080001')
        bar_measure_new = self.driver.get_element('x, //*[@id="pane-电表"]/div[3]/div[3]/div/span').text
        self.check_assert(bar_measure_new, '暂无数据')
        Logger().info('网关绑定表计{}已被删除'.format(self.test_measure_data[0]['测量表计编号']))
        self.driver.get_element('x, //*[@id="pane-电表"]/div[2]/button').click()  # 点击重置
        self.driver.wait_display('x, //*[@id="pane-电表"]/div[3]/div[8]')

        # 删除NB/GPRS表计会删除对应网关
        IEMSEquipment(self.driver).select_eqp('00080001', self.test_measure_data[3]['测量表计编号'])
        IEMSEquipment(self.driver).delete_eqp('00080001')
        bar_measure_new = self.driver.get_element('x, //*[@id="pane-电表"]/div[3]/div[3]/div/span').text
        self.check_assert(bar_measure_new, '暂无数据')
        Logger().info('网关绑定表计{}已被删除'.format(self.test_measure_data[3]['测量表计编号']))
        IEMSEquipment(self.driver).select_type('网关')
        IEMSEquipment(self.driver).select_eqp('网关', self.test_measure_data[3]['测量表计编号'])
        gateway_no_new = self.driver.get_element('x, //*[@id="pane-网关"]/div[3]/div[3]/div/span').text
        self.check_assert(gateway_no_new, '暂无数据')

    def tearDown(self) -> None:
        # self.driver.driver.refresh()
        print('测试结束')

    @classmethod
    def tearDownClass(cls):
        MysqlConn().restore_databases(cls.databases, cls.backup_files)
        cls.driver.driver.quit()


if __name__ == '__main__':
    unittest.main()
