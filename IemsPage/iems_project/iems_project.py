from Comm import *
from IemsPage.basePage import BasePage


class IEMSProject(BasePage):
    """项目级"""


    def add_project(self, projectName, sssj, sxsj, Address, direct, directMobile, business, businessMobile, wbsj):
        """
        新增项目
        :return:
        """
        self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[1]/div/div/input')
        log.Logger().info('进入项目新增页面')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[1]/div/div/input').send_keys(projectName)
        log.Logger().info('输入项目名称:{}'.format(projectName))
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[3]/div/div/input').send_keys(
            sssj)
        self.driver.keys_control('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[3]/div/div/input', 'enter')
        log.Logger().info('输入实施时间:{}'.format(sssj))
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[4]/div/div/input').send_keys(sxsj)
        self.driver.keys_control('x, //*[@id="appMain-container"]/div[1]/div[3]/form/div[4]/div/div/input', 'enter')
        log.Logger().info('输入上线时间:{}'.format(sxsj))
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[3]/div/button').click()
        log.Logger().info('点击下一步')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[4]/div[1]/div[1]/div[1]/input').send_keys(Address)
        self.driver.wait_until('x, //*[@id="appMain-container"]/*[@class="head_app"]/div[4]/div/div/*[@class="search-tips"]/ul/li[last()]')
        self.driver.get_element('x, //*[@id="appMain-container"]/*[@class="head_app"]/div[4]/div/div/*[@class="search-tips"]/ul/li[last()]').click()
        self.driver.wait_until('x, //*[@id="amapDemo"]/div[1]/div/div[1]/div[1]/div/div/img')
        log.Logger().info('选择地址')
        if self.driver.text_in('x, //*[@id="appMain-container"]/div[1]/div[4]/div[1]/div[3]', '详细地址'):
            self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[4]/div[2]/button[2]/span').click()
            log.Logger().info('点击下一步')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[5]/form/div[2]/div/div[1]/input').send_keys(direct)
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[5]/form/div[2]/div/div[2]/input').send_keys(directMobile)
        log.Logger().info('填写工程联系人和联系方式')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[5]/form/div[4]/div/div[1]/input').send_keys(business)
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[5]/form/div[4]/div/div[2]/input').send_keys(businessMobile)
        log.Logger().info('填写物业联系人和联系方式')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[5]/div/button[2]/span').click()
        log.Logger().info('点击下一步')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[6]/form/div[1]/div/div/input').send_keys(wbsj)
        self.driver.keys_control('x, //*[@id="appMain-container"]/div[1]/div[6]/form/div[1]/div/div/input', 'enter')
        log.Logger().info('输入维保时间:{}'.format(wbsj))
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[6]/div/button[2]/span').click()
        log.Logger().info('点击下一步')
        self.driver.get_element('x, //*[@id="appMain-container"]/div[1]/div[7]/div/div[2]/button[2]/span').click()
        log.Logger().info('点击确认保存信息')
        self.driver.wait_until('x, //*[@id="appMain-container"]/div[1]/div[8]/div/div[2]/button/span')
        log.Logger().info('保存成功')
        time.sleep(1)


    def enter_tmpl(self, isFee='no'):
        """
        进入计费方案界面
        :return:
        """

        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/div/div/div[last()]/span/span[2]/span/span')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/div/div/div[last()]/span/span[2]/span/span').click()
        time.sleep(1)
        log.Logger().info('点击财务')
        self.driver.wait_until('x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[1]/div/div/li/div')
        self.driver.get_element('x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[1]/div/div/li/div').click()
        self.driver.wait_play('x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[1]/div/div/li/ul')
        log.Logger().info('点击财务中心')
        time.sleep(1)
        if isFee == 'no':
            self.driver.wait_until('x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[1]/div/div/li/ul/div[last()]')
            self.driver.get_element('x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[1]/div/div/li/ul/div[last()]').click()
            time.sleep(1)
            log.Logger().info('点击计费方案')
        if isFee == 'yes':
            self.driver.wait_until('x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[1]/div/div/li/ul/div[last()-1]/div/li')
            self.driver.get_element('x, //*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[1]/div/div/li/ul/div[last()-1]/div/li').click()
            time.sleep(1)
            log.Logger().info('点击计费方案（含附加费）')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/button/span')
        log.Logger().info('进入新建计费方案界面')


    def add_tmpl(self, tmplName, meterType):
        """
        添加计费方案
        :param tmplName: 方案名称
        :param meterType: 表计类型
        :return:
        """
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/button')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[2]/div/button').click()
        log.Logger().info('点击新建计费方案')
        self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[3]')
        if self.driver.text_in('x, //*[@id="el-drawer__title"]/div', '新建计费方案'):
            self.driver.wait_until(
                'x, //*[@id="app"]/div/div[2]/section/div/div[3]/div/div/section/form/div[2]/div/div/input')
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[3]/div/div/section/form/div[2]/div/div/input').send_keys(
                tmplName)
            log.Logger().info('进入新建计费方案界面')
        else:
            time.sleep(1)
            self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div/div/section/form/div[2]/div/div/input')
            log.Logger().info('进入新建计费方案界面')
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div/div/section/form/div[2]/div/div/input').send_keys(tmplName)
            log.Logger().info('输入方案名称')
        if meterType == '电表':
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div/div/section/form/div[3]/div/div/span[1]').click()
            log.Logger().info('选择电表')
        if meterType == '水表':
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div/div/section/form/div[3]/div/div/span[2]').click()
            log.Logger().info('选择水表')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[3]/div/div/section/div/button').click()
        log.Logger().info('点击保存')
        self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[3]')
        time.sleep(1)


    def add_tmpl_edition(self, editionNO, editionName):
        """
        添加计费方案版本
        :param editionNO: 版本编号
        :param editionName: 版本名称
        :return:
        """
        self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[4]')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/button').click()
        log.Logger().info('点击新增版本')
        self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[5]')
        time.sleep(1)
        self.driver.wait_until(
            'x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[1]/div/div[1]/input')
        self.driver.clear_and_input('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[1]/div/div[1]/input', editionNO)
        log.Logger().info('输入版本编号')
        self.driver.clear_and_input('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[2]/div/div/input', editionName)
        log.Logger().info('输入版本名称')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[3]/div/div[1]/input').click()
        self.driver.wait_play('x, //body/div[last()]/div/div/div[2]/table/tbody/tr[last()-1]/td[last()]/div/span')
        self.driver.get_element('x, //body/div[last()]/div/div/div[2]/table/tbody/tr[last()-1]/td[last()]/div/span').click()
        log.Logger().info('选择生效时间')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/button').click()
        log.Logger().info('点击保存')
        self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[5]')
        time.sleep(1)


    def add_tmpl_edition_fee(self, editionNO, editionName, isFee='no', feeName='', feeType='', feeMoney='', sxsj='month'):
        """
        添加计费方案版本
        :param editionNO: 版本编号
        :param editionName: 版本名称
        :return:
        """
        self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[4]')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[4]/div/div/section/button').click()
        log.Logger().info('点击新增版本')
        self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[5]')
        time.sleep(1)
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[1]/div/div[1]/input')
        self.driver.clear_and_input('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[1]/div/div[1]/input', editionNO)
        log.Logger().info('输入版本编号')
        self.driver.clear_and_input('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[2]/div/div/input', editionName)
        log.Logger().info('输入版本名称')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[3]/div/div[1]/input').click()
        self.driver.wait_play('x, //body/div[last()]/div/div/div[2]/table/tbody/tr[last()-1]/td[last()]/div/span')
        self.driver.get_element('x, //body/div[last()]/div/div/div[2]/table/tbody/tr[last()-1]/td[last()]/div/span').click()
        log.Logger().info('选择生效时间')
        if isFee == 'no':
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[5]/div/div/div/label[1]').click()
            log.Logger().info('附加费不开启')
        if isFee == 'yes':
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[5]/div/div/div/label[2]').click()
            log.Logger().info('附加费开启')
            self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[5]/div[2]/div[1]/div/div/input')
            self.driver.clear_and_input('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[5]/div[2]/div[1]/div/div/input', feeName)
            log.Logger().info('输入附加费名称')
            if feeType == '固定价格':
                self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[5]/div[2]/div[2]/div/div/label[1]').click()
                log.Logger().info('点击固定价格')
                self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[5]/div[2]/div[3]/div/div/div/input').send_keys(feeMoney)
                log.Logger().info('输入固定价格')
            if feeType == '上浮比例':
                self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[5]/div[2]/div[2]/div/div/label[2]').click()
                log.Logger().info('点击上浮比例')
                self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[5]/div[2]/div[3]/div/div/div/input').send_keys(feeMoney)
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/button').click()
        log.Logger().info('点击保存')
        time.sleep(1)
        if self.driver.isPresent('x, //body/div[last()]/div/div[1]/p'):
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/form/div[3]/div/div[1]/input').click()
            self.driver.wait_play('x, //body/div[last()]/div/div/div[2]/table/tbody/tr[last()-1]/td[last()]/div/span')
            self.driver.get_element('x, //body/div[last()]/div[1]/div/div[1]/button[4]').click()
            self.driver.get_element('x, //body/div[last()]/div/div/div[2]/table/tbody/tr[last()-1]/td[last()]/div/span').click()
            log.Logger().info('重新选择生效时间')
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[5]/div/div/section/div/button').click()
            log.Logger().info('点击保存')
        self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[5]')
        time.sleep(1)


    def add_tmpl_edition_charging(self, tmplType, tmplCharging='', tmplCharging1='', tmplCharging2='', tmplCharging3='', tmplCharging4=''):
        """
        添加计费方案费率
        :param tmplType: 费率类型
        :param tmplCharging: 单费率
        :param tmplCharging1: 复费率尖
        :param tmplCharging2: 复费率峰
        :param tmplCharging3: 复费率平
        :param tmplCharging4: 复费率谷
        :return:
        """

        self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[6]')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[6]/div/div/section/button').click()
        log.Logger().info('点击年时段表')
        self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[7]')
        self.driver.wait_until(
            'x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/form/div[1]/label')
        time.sleep(1)
        if tmplType == '复费率':
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/form/div[2]/div/div/label[2]/span[1]/span').click()
            log.Logger().info('点击复费率')
            self.driver.get_element(
                'x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/form/div[3]/div/div/div[1]/input').send_keys(
                tmplCharging1)
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/form/div[3]/div/div/div[2]/input').send_keys(tmplCharging2)
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/form/div[3]/div/div/div[3]/input').send_keys(tmplCharging3)
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/form/div[3]/div/div/div[4]/input').send_keys(tmplCharging4)
            log.Logger().info('复费率输入费率')
        if tmplType == '单费率':
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/form/div[2]/div/div/label[1]/span[1]/span').click()
            log.Logger().info('点击单费率')
            self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/form/div[3]/div/div/div/input').send_keys(tmplCharging)
            log.Logger().info('单费率输入费率')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[7]/div/div/section/div/button').click()
        log.Logger().info('点击保存')
        self.driver.wait_display('x, //*[@id="app"]/div/div[2]/section/div/div[7]')
        time.sleep(1)


    def del_edition_charging(self):
        """
        删除费率
        :return:
        """

        self.driver.wait_play('x, //*[@id="app"]/div/div[2]/section/div/div[6]')
        self.driver.wait_until('x, //*[@id="app"]/div/div[2]/section/div/div[6]/div/div/section/div/div[3]/table/tbody/tr[last()]/td[last()]')
        self.driver.get_element('x, //*[@id="app"]/div/div[2]/section/div/div[6]/div/div/section/div/div[3]/table/tbody/tr[last()]/td[last()]/div/button').click()
        log.Logger().info('点击删除按钮')
        self.driver.wait_play('x, //body/div[last()-1]')
        if self.driver.text_in('x, //body/div[last()-1]/div/div[2]/div[1]/div[2]/p', '确定删除此记录吗？'):
            self.driver.get_element('x, //body/div[last()-1]/div/div[3]/button[2]').click()
            log.Logger().info('点击提示的确定')
        self.driver.wait_display('x, //body/div[last()-1]')
        time.sleep(1)






if __name__ == '__main__':
    now = datetime.datetime.now()
    print(now)
    today = now.strftime("%Y-%m-%d")
    print(today)
    yesterday = (now - datetime.timedelta(days=0)).strftime("%Y-%m-%d")
    print(yesterday)
    tomorrow = (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    print(tomorrow)