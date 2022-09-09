from time import sleep
from Comm.log import Logger
from IemsPage.basePage import BasePage, Base


class IEMSEquipment(BasePage):

    def enter_eqp(self, barProjectName):
        """
        进入设备档案界面
        :param barProjectName: 项目名称
        :return:
        """

        self.driver.get_element('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/div').click()
        sleep(1)
        self.driver.get_element(
            'x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[2]/div/li/div').click()
        sleep(1)
        self.driver.get_element(
            'x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[2]/div/li/ul/div[1]/li').click()
        self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[1]/div/div[2]')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div/div[1]/input').send_keys(
            barProjectName)
        self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[2]/div/button')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div/button').click()
        sleep(1)
        while True:
            if self.driver.assert_text('x, //*[@class="el-card__body"]/div[2]/div/div/div/div/div/div[2]',
                                       barProjectName, '查找成功', '未查询到指定项目'):
                self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[2]/div/div[2]/div/div/div[1]/div')
                self.driver.get_element(
                    'x, //*[@id="appMain-container"]/div[1]/div[2]/div/div[2]/div/div/div[1]/div/div/div[2]').click()
                sleep(1)
                self.driver.wait_display('x, //*[@id="pane-电表"]/div[3]/div[8]')
                break
            else:
                self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div/button').click()
                sleep(1)
                self.driver.assert_text('x, //*[@class="el-card__body"]/div[2]/div/div/div/div/div/div[2]',
                                        barProjectName, '查找成功', '未查询到指定项目')
                self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[2]/div/div[2]/div/div/div[1]/div')
                self.driver.get_element(
                    'x, //*[@id="appMain-container"]/div[1]/div[2]/div/div[2]/div/div/div[1]/div/div/div[2]').click()
                sleep(1)
                self.driver.wait_display('x, //*[@id="pane-电表"]/div[3]/div[8]')
                break
        Logger().info('进入{}设备档案'.format(barProjectName))


    def select_type(self, type):
        """
        选择设备档案类型
        :param type: 00080001，00080002，网关
        :return:
        """

        if type == '00080001':
            self.driver.get_element('x, //*[@id="tab-电表"]').click()
            self.driver.wait_display(timeout=60, selector='x, //*[@id="pane-电表"]/div[3]/div[8]')
            sleep(1)
            Logger().info('进入设备档案电表界面')
        if type == '00080002':
            self.driver.get_element('x, //*[@id="tab-水表"]').click()
            self.driver.wait_display(timeout=60, selector='x, //*[@id="pane-水表"]/div[3]/div[8]')
            sleep(1)
            Logger().info('进入设备档案水表界面')
        if type == '网关':
            self.driver.get_element('x, //*[@id="tab-网关"]').click()
            self.driver.wait_display(timeout=60, selector='x, //*[@id="pane-网关"]/div[3]/div[8]')
            sleep(1)
            Logger().info('进入设备档案网关界面')


    def import_eqp_a(self, type, eqpFile):
        """
        导入设备
        :param type: 00080001，00080002，网关
        :param eqpFile: 设备文件
        :return:
        """

        Logger().info('开始导入设备')
        if type == '00080001':
            self.select_type(type)
            self.driver.get_element('x, //*[@id="pane-电表"]/div[1]/div/button').click()
            self.driver.get_element('x, //*[@id="con_lf_top_div"]/div[3]/div/div/section/div/div/div/input').send_keys(
                eqpFile)
            self.driver.wait_play(timeout=120, selector='x, //*[@id="pane-电表"]/div[3]/div[8]')
            self.driver.wait_display('x, //*[@id="pane-电表"]/div[3]/div[8]')
            sleep(1)
        if type == '00080002':
            self.select_type(type)
            self.driver.get_element('x, //*[@id="pane-水表"]/div[1]/div/button').click()
            self.driver.get_element('x, //*[@id="con_lf_top_div"]/div[3]/div/div/section/div/div/div/input').send_keys(
                eqpFile)
            self.driver.wait_play(timeout=120, selector='x, //*[@id="pane-水表"]/div[3]/div[8]')
            self.driver.wait_display('x, //*[@id="pane-水表"]/div[3]/div[8]')
            sleep(1)
        if type == '网关':
            self.select_type(type)
            self.driver.wait_until('x, //*[@id="pane-网关"]/div[1]/div/button')
            self.driver.get_element('x, //*[@id="pane-网关"]/div[1]/div/button').click()
            self.driver.get_element('x, //*[@id="con_lf_top_div"]/div[3]/div/div/section/div/div/div/input').send_keys(
                eqpFile)
            self.driver.wait_play(timeout=120, selector='x, //*[@id="pane-网关"]/div[3]/div[8]')
            # if self.driver.assert_text('x, //body/div[last()]/p', '数据文件上传成功'):
            #     self.driver.get_element('x, //*[@id="tab-网关"]').click()
            self.driver.wait_display(timeout=120, selector='x, //*[@id="pane-网关"]/div[3]/div[8]')
            sleep(1)
        Logger().info('导入设备成功')


    def import_eqp(self, type, eqpFile):
        """
        导入设备
        :param type: 00080001，00080002，网关
        :param eqpFile: 设备文件
        :return:
        """

        Logger().info('开始导入设备')
        if type == '00080001':
            self.select_type(type)
            self.driver.get_element('x, //*[@id="pane-电表"]/div[1]/div/button').click()
            self.driver.get_element('x, //*[@id="con_lf_top_div"]/div[3]/div/div/section/div/div/div/input').send_keys(
                eqpFile)
            # self.driver.wait_play(timeout=60, selector='x, //*[@id="pane-电表"]/div[3]/div[8]')
            self.driver.wait_display('x, //*[@id="pane-电表"]/div[3]/div[8]')
            sleep(1)
        if type == '00080002':
            self.select_type(type)
            self.driver.get_element('x, //*[@id="pane-水表"]/div[1]/div/button').click()
            self.driver.get_element('x, //*[@id="con_lf_top_div"]/div[3]/div/div/section/div/div/div/input').send_keys(
                eqpFile)
            # self.driver.wait_play(timeout=60, selector='x, //*[@id="pane-水表"]/div[3]/div[8]')
            self.driver.wait_display('x, //*[@id="pane-水表"]/div[3]/div[8]')
            sleep(1)
        if type == '网关':
            self.select_type(type)
            self.driver.wait_until('x, //*[@id="pane-网关"]/div[1]/div/button')
            self.driver.get_element('x, //*[@id="pane-网关"]/div[1]/div/button').click()
            self.driver.get_element('x, //*[@id="con_lf_top_div"]/div[3]/div/div/section/div/div/div/input').send_keys(
                eqpFile)
            # self.driver.wait_play(timeout=60, selector='x, //*[@id="pane-网关"]/div[3]/div[8]')
            # if self.driver.assert_text('x, //body/div[last()]/p', '数据文件上传成功'):
            #     self.driver.get_element('x, //*[@id="tab-网关"]').click()
            self.driver.wait_display(timeout=120, selector='x, //*[@id="pane-网关"]/div[3]/div[8]')
            sleep(1)
        Logger().info('导入设备成功')


    def select_index(self, index):
        """
        通用查询
        :param index:
        :return:
        """

        Logger().info('开始搜索{}'.format(index))
        self.driver.wait_until('x, //body/div[last()]/div/input')
        self.driver.get_element('x, //body/div[last()]/div/input').send_keys(index)
        sleep(1)
        self.driver.get_element('x, //body/div[last()]/div/div/button').click()
        Logger().info('查到{}'.format(index))
        sleep(1)

    def select_eqp(self, type, eqpNo):
        """
        查询设备
        :param type: 类型{00080001，00080002，网关}
        :param eqpNo: 设备号
        :return:
        """

        if type == '00080001':
            self.driver.move_to_click(
                'x, //*[@id="pane-电表"]/div[3]/div[4]/div[1]/table/thead/tr[1]/th[3]/div/span/span/span')
            sleep(1)
            self.select_index(eqpNo)
            # self.driver.wait_until('x, //body/div[last()]/div/input')
            # self.driver.get_element('x, //body/div[last()]/div/input').send_keys(eqpNo)
            # self.driver.get_element('x, //body/div[last()]/div/div/button').click()
            self.driver.wait_display('x, //*[@id="pane-电表"]/div[3]/div[8]')
            sleep(1)
        if type == '00080002':
            self.driver.move_to_click(
                'x, //*[@id="pane-水表"]/div[3]/div[4]/div[1]/table/thead/tr[1]/th[3]/div/span/span/span').click()
            self.driver.wait_until('x, //body/div[last()]/div/input')
            self.driver.get_element('x, //body/div[last()]/div/input').send_keys(eqpNo)
            self.driver.get_element('x, //body/div[last()]/div/div/button').click()
            self.driver.wait_display('x, //*[@id="pane-水表"]/div[3]/div[8]')
            sleep(1)
        if type == '网关':
            self.driver.move_to_click('x, //*[@id="pane-网关"]/div[3]/div[4]/div[1]/table/thead/tr/th['
                                      '2]/div/span/span/span')
            self.driver.wait_until('x, //body/div[last()]/div/input')
            self.driver.get_element('x, //body/div[last()]/div/input').send_keys(eqpNo)
            self.driver.wait_until('x, //body/div[last()]/div/div/button')
            self.driver.get_element('x, //body/div[last()]/div/div/button').click()
            self.driver.wait_display('x,//*[@id="pane-网关"]/div[3]/div[8]/div/p')
            sleep(1)
        Logger().info('查到设备{}'.format(eqpNo))


    def connect_gateway(self, type):
        """
        绑定网关
        :param type:
        :return:
        """

        Logger().info('开始关联网关')
        if type == '00080001':
            self.driver.get_element(
                'x, //*[@id="pane-电表"]/div[3]/div[5]/div[2]/table/tbody/tr/td[18]/div/button[2]/span').click()
            self.driver.wait_until('x, //*[@id="con_lf_top_div"]/div[7]/div/div[2]/form/div[2]/div/div/div[1]/input')
            self.driver.get_element(
                'x, //*[@id="con_lf_top_div"]/div[7]/div/div[2]/form/div[2]/div/div/div/input').click()
            sleep(1)
            self.driver.move_to_click('x, //body/div[last()]/div[1]/div[1]/ul/li[last()]/span')
            self.driver.get_element(
                'x, //*[@id="con_lf_top_div"]/div[7]/div/div[2]/form/div[3]/div/button/span').click()
            self.driver.wait_play('x, //body/div[last()]/p')
            self.driver.wait_display('x, //body/div[last()]/p')
            self.driver.wait_display('x, //*[@id="pane-电表"]/div[3]/div[8]')
            sleep(1)
        Logger().info('关联网关结束')


    def disconnect_gateway_a(self, type):
        """
        解绑网关
        :param type:
        :return:
        """

        Logger().info('开始解绑网关')
        if type == '00080001':
            self.driver.get_element(
                'x, //*[@id="pane-电表"]/div[3]/div[5]/div[2]/table/tbody/tr[1]/td[18]/div/button[2]/span').click()
            self.driver.get_element(
                'x, //body/div[last()-1]/div/div[3]/button[2]').click()
            self.driver.wait_play('x, //*[@id="pane-电表"]/div[3]/div[8]')
            self.driver.wait_display('x, //*[@id="pane-电表"]/div[3]/div[8]')
            sleep(1)
        Logger().info('成功解绑')


    def disconnect_gateway(self, type):
        """
        解绑网关
        :param type:
        :return:
        """

        Logger().info('开始解绑网关')
        if type == '00080001':
            self.driver.get_element(
                'x, //*[@id="pane-电表"]/div[3]/div[5]/div[2]/table/tbody/tr[1]/td[18]/div/button[2]/span').click()
            self.driver.get_element(
                'x, //body/div[last()-1]/div/div[3]/button[2]').click()
            # self.driver.wait_play('x, //*[@id="pane-电表"]/div[3]/div[8]')
            self.driver.wait_display('x, //*[@id="pane-电表"]/div[3]/div[8]')
            sleep(1)
        Logger().info('成功解绑')


    def enter_project(self):
        """
        进入项目列表
        :return:
        """

        self.driver.wait_until('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/div')
        if self.driver.get_element('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul').is_displayed():
            self.driver.get_element(
                'x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[1]/div/li/div').click()
        else:
            self.driver.get_element('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/div').click()
        self.driver.wait_play('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[1]/div/li/div')
        self.driver.move_to_click('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[1]/div/li/div')
        self.driver.wait_until('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div[1]/div/li/ul/div['
                               '1]/li/span')
        self.driver.move_to_click('x, //*[@id="menu-container"]/div[1]/div/ul/div/div[1]/div/li/ul/div['
                                  '1]/div/li/ul/div[1]/li/span')
        self.driver.wait_display('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[8]')
        sleep(1)
        Logger().info('进入项目列表')


    def enter_project_space(self, barProjectName):
        """
        进入项目空间
        :param barProjectName:
        :return:
        """

        self.enter_project()
        self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[4]/div['
                               '1]/table/thead/tr/th[2]/div/span/span/span')
        self.driver.move_to_click('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[4]/div['
                                  '1]/table/thead/tr/th[2]/div/span/span/span')
        self.select_index(barProjectName)
        self.driver.wait_display('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[8]')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[5]/div['
                                '2]/table/tbody/tr/td[12]/div/button[1]').click()
        self.driver.wait_until('x, //*[@id="left"]/div[3]/div[1]/div[1]/span[2]/span/span')
        self.driver.assert_text('x, //*[@id="left"]/div[3]/div[1]/div[1]/span[2]/span/span', barProjectName)
        Logger().info('进入{}项目空间'.format(barProjectName))


    def add_building(self, type, buildName, buildAbbr, buildArea, buildDesc):
        """
        新增建筑/楼栋/楼层/房间
        :param type: build/
        :param buildName:
        :param buildAbbr:
        :param buildArea:
        :param buildDesc:
        :return:
        """

        Logger().info('开始新增建筑')
        self.driver.move_to_click('x, //body/div[last()]/div/div[2]/span')
        if type == 'build':
            self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[3]/div/div[1]/span')
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/div/div[2]/form/div[1]/div/div['
                                    '1]/input').send_keys(buildName)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/div/div[2]/form/div[2]/div/div/input').send_keys(buildAbbr)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/div/div[2]/form/div[3]/div/div/input').send_keys(buildArea)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/div/div[2]/form/div['
                                    '4]/div/div/textarea').send_keys(buildDesc)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/div/div[2]/div/button[2]').click()
        if type == 'block':
            self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[1]/span')
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/form/div[1]/div/div/input').send_keys(buildName)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/form/div[2]/div/div/input').send_keys(buildAbbr)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/form/div[3]/div/div/input').send_keys(buildArea)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/form/div['
                                    '4]/div/div/textarea').send_keys(buildDesc)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/div/button[2]').click()
        if type == 'floor':
            self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[1]/span')
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/form/div[1]/div/div['
                                    '1]/input').send_keys(buildName)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/form/div[2]/div/div/input').send_keys(buildAbbr)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/form/div[3]/div/div/input').send_keys(buildArea)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/form/div['
                                    '4]/div/div/textarea').send_keys(buildDesc)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/div/button[2]').click()
        if type == 'room':
            self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[1]/span')
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/form/div[1]/div/div/input').send_keys(buildName)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/form/div[2]/div/div/input').send_keys(buildAbbr)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/form/div[3]/div/div/input').send_keys(buildArea)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/form/div['
                                    '4]/div/div/textarea').send_keys(buildDesc)
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/div/button[2]').click()
            self.driver.wait_until('x, //*[@id="left"]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/span['
                                   '2]/span/span')
        Logger().info('新增结束')


    def delete_building(self):
        """
        删除检建筑
        :return:
        """

        Logger().info('开始删除建筑')
        self.driver.move_to_click('x, //body/div[5]/div/div[last()]/span')
        self.driver.get_element('x, //body/div[4]/div/div[3]/button[last()]').click()
        Logger().info('删除建筑结束')


    def add_measure(self, eqpNo, selector):
        """
        表计和房间绑定
        :param eqpNo:
        :param selector:
        :return:
        """

        Logger().info('开始表计和房间绑定')
        self.driver.move_to_click('x, //body/div[last()]/div/div[2]/span')
        self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[12]/div/div[1]/span')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[12]/div/div[2]/form/div['
                                '2]/div/div/div/input').send_keys(eqpNo)
        self.driver.wait_until('x, //body/div[last()]/div[1]/div[1]/ul/li[1]/span')
        self.driver.move_to_click('x, //body/div[last()]/div[1]/div[1]/ul/li[1]/span')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[12]/div/div[2]/form/div[18]/div/div['
                                '1]/input').click()
        self.driver.wait_until('x, //body/div[last()]/div[2]/button[1]')
        sleep(1)
        self.driver.move_to_click('x, //body/div[last()]/div[2]/button[1]')
        # self.driver.get_element('x, //body/div[last()]/div[2]/button[1]').click()
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[12]/div/div[3]/span/button[2]').click()
        self.driver.wait_display(timeout=60, selector='x, //*[@id="appMain-container"]/div[1]/div[12]/div/div[1]/span')
        while True:
            self.driver.get_element(selector).click()
            self.driver.wait_until(timeout=60, selector='x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[2]/div[2]/div['
                                       '3]/table/tbody/tr/td[11]/div/button[1]/span')
            break
        sleep(1)
        Logger().info('新增表计结束')


    def edit_measure(self):
        """
        维护表计
        :return:
        """

        Logger().info('开始维护表计')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[2]/div[2]/div['
                                '3]/table/tbody/tr/td[11]/div/button[1]').click()   # 点击维护表计
        self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[12]/div/div[1]/span')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[13]/div/div[2]/form/div[19]/div/div/input').click()
        self.driver.wait_until('x, //body/div[last()]/div[2]/button[1]')
        sleep(1)
        self.driver.move_to_click('x, //body/div[last()]/div[2]/button[1]')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[13]/div/div[3]/span/button[2]').click()
        # self.driver.get_element('x, //body/div[last()]/div[2]/button[1]').click()
        self.driver.wait_play('x, //body/div[last()]/p')
        self.driver.wait_display('x, //body/div[last()]/p')
        self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[2]/div[2]/div['
                               '3]/table/tbody/tr/td[11]/div/button[1]/span')
        sleep(1)
        Logger().info('维护表计结束')


    def unbind_measure(self):
        """
        解绑表计
        :return:
        """

        Logger().info('开始解绑表计')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[2]/div[2]/div[2]/div[2]/div['
                                '3]/table/tbody/tr[1]/td[11]/div/button[last()]').click()
        self.driver.get_element('x, //body/div[last()-1]/div/div[3]/button[2]').click()
        sleep(1)
        Logger().info('解绑表计结束')


    def delete_eqp(self, type):
        """
        删除设备
        :param type:
        :return:
        """

        Logger().info('开始删除设备')
        self.driver.wait_until('x, //*[@id="pane-网关"]/div[3]/div[5]/div[2]/table/tbody/tr/td[13]/div/button[last()]')
        if type == '网关':
            self.driver.get_element(
                    'x, //*[@id="pane-网关"]/div[3]/div[5]/div[2]/table/tbody/tr/td[13]/div/button[last()]').click()
            sleep(2)
            if self.driver.assert_text('x, //body/div[last()-1]/div/div[2]/div[1]/div[2]/p', '删除网关会删除该网关下所有表计，是否删除？'):
                self.driver.get_element(
                    'x, //body/div[last()-1]/div/div[3]/button[2]').click()
            self.driver.wait_play('x, //body/div[last()]/p')
            self.driver.wait_display(timeout=600, selector='x, //body/div[last()]/p')
            sleep(1)
        if type == '00080001':
            self.driver.get_element(
                'x, //*[@id="pane-电表"]/div[3]/div[5]/div[2]/table/tbody/tr/td[18]/div/button[last()]').click()
            sleep(2)
            # if self.driver.assert_text('x, //body/div[last()-1]/div/div[2]/div[1]/div[2]/p', '是否删除该表计？'):
            self.driver.get_element('x, //body/div[last()-1]/div/div[3]/button[2]').click()
            self.driver.wait_play('x, //body/div[last()]/p')
            self.driver.wait_display(timeout=120, selector='x, //body/div[last()]/p')
            sleep(1)
        Logger().info('成功删除')







if __name__ == '__main__':
    from IemsPage.iems_login.iems_login import IemsLogin

    b = Base('c')
    IemsLogin(b).iems_login_old(user='admin1', pwd='admin')
    IEMSEquipment(b).enter_eqp('发布回归')
    # IEMSEquipment(b).enter_project_space('发布回归')
    # IEMSEquipment(b).import_eqp( r"C:\Users\Administrator\Desktop\UIAutoTest\IemsTestcase\Testdata\test_measure_data.xls", 1)
