import os
import sys
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 父路径的父路径
import Comm
from Comm import *
from Conf import exceptions
from Conf.models import TestMetrics

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class WeChatSend:
    """
    企业微信消息通知
    """

    def __init__(self, metrics: TestMetrics):
        self.metrics = metrics
        self.headers = {"Content-Type": "application/json"}
        self.BUILD_NUMBER = os.getenv('BUILD_NUMBER')
        self.JOB_NAME = os.getenv('JOB_NAME')

    def send_text(self, content, mentioned_mobile_list=None):
        """
        发送文本类型通知
        :param content: 文本内容，最长不超过2048个字节，必须是utf8编码
        :param mentioned_mobile_list: 手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人
        :return:
        """
        _data = {"msgtype": "text", "text": {"content": content, "mentioned_list": None,
                                             "mentioned_mobile_list": mentioned_mobile_list}}

        if mentioned_mobile_list is None or isinstance(mentioned_mobile_list, list):
            # 判断手机号码列表中得数据类型，如果为int类型，发送得消息会乱码
            if len(mentioned_mobile_list) >= 1:
                for i in mentioned_mobile_list:
                    if isinstance(i, str):
                        res = requests.post(url=config.wechat.webhook, json=_data, headers=self.headers)
                        if res.json()['errcode'] != 0:
                            log.Logger().error(res.json())
                            raise exceptions.SendMessageError("企业微信「文本类型」消息发送失败")

                    else:
                        raise exceptions.ValueTypeError("手机号码必须是字符串类型.")
        else:
            raise exceptions.ValueTypeError("手机号码列表必须是list类型.")

    def send_markdown(self, content):
        """
        发送 MarkDown 类型消息
        :param content: 消息内容，markdown形式
        :return:
        """
        _data = {"msgtype": "markdown", "markdown": {"content": content}}
        res = requests.post(url=Comm.config.wechat.webhook, json=_data, headers=self.headers)
        if res.json()['errcode'] != 0:
            log.Logger().error(res.json())
            raise exceptions.SendMessageError("企业微信「MarkDown类型」消息发送失败")

    def _upload_file(self, file):
        """
        先将文件上传到临时媒体库
        """
        key = config.wechat.webhook.split("key=")[1]
        url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file"
        data = {"file": open(file, "rb")}
        res = requests.post(url, files=data).json()
        return res['media_id']

    def send_file_msg(self, file):
        """
        发送文件类型的消息
        @return:
        """

        _data = {"msgtype": "file", "file": {"media_id": self._upload_file(file)}}
        res = requests.post(url=config.wechat.webhook, json=_data, headers=self.headers)
        if res.json()['errcode'] != 0:
            log.Logger().error(res.json())
            raise exceptions.SendMessageError("企业微信「file类型」消息发送失败")

    def report(self, type='jenkins'):

        if type == 'jenkins':
            report = f'(http://{get_local_ip.get_host_ip()}:8080/jenkins/job/{self.JOB_NAME}/{self.BUILD_NUMBER}/allure/)'
            return report
        else:
            report = f'(http://localhost:63342/UIAutoTest/Results/html/index.html)'
            # report = f'(http://transact.netsarang.com:9999/index.html)'
            return report

    def send_wechat_notification(self, report):
        """ 发送企业微信通知 """

        text = f"""{Comm.config.project_name}【自动化通知】
                                    >测试负责人：@{Comm.config.tester_name}
                                    >
                                    > **执行结果**
                                    ><font color=\"info\">成  功  率  : {self.metrics.pass_rate}%</font>
                                    >用例  总数：<font color=\"info\">{self.metrics.total}</font>                                    
                                    >成功用例数：<font color=\"info\">{self.metrics.passed}</font>
                                    >失败用例数：`{self.metrics.failed}个`
                                    >异常用例数：`{self.metrics.broken}个`
                                    >跳过用例数：<font color=\"warning\">{self.metrics.skipped}个</font>
                                    >用例执行时长：<font color=\"warning\">{self.metrics.time} s</font>
                                    >时间：<font color=\"comment\">{time_control.now_time()}</font>
                                    >测试报告，点击查看>>[测试报告入口]{report}
                                    >非相关负责人员可忽略此消息。"""

        WeChatSend(allure_report_data.AllureFileClean().get_case_count()).send_markdown(text)


if __name__ == '__main__':
    # print(ensure_path_sep('/Results/html/index.html'))
    report = WeChatSend(allure_report_data.AllureFileClean().get_case_count()).report()
    WeChatSend(allure_report_data.AllureFileClean().get_case_count()).send_wechat_notification(report)
