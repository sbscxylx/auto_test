from dataclasses import dataclass
from typing import Text, Union
from pydantic import BaseModel


@dataclass
class TestMetrics:
    """ 用例执行数据 """
    passed: int
    failed: int
    broken: int
    skipped: int
    total: int
    pass_rate: float
    time: Text


class DingTalk(BaseModel):
    webhook: Union[Text, None]
    secret: Union[Text, None]


class Webhook(BaseModel):
    webhook: Union[Text, None]


class MySqlDB(BaseModel):
    switch: bool = False
    host: Union[Text, None] = None
    user: Union[Text, None] = None
    password: Union[Text, None] = None
    port: Union[int, None] = 3306


class SitSsh(BaseModel):
    ssh_address: str
    ssh_host: int
    ssh_username: str
    ssh_pwd: str
    remote_bind_address: str
    remote_bind_address_host: int
    mysql_user: str
    mysql_pwd: str
    mysql_host: str
    mysql_db: str
    backup_path: str


class Log(BaseModel):
    log_level: str
    log_format: Text


class Url(BaseModel):
    sit_old_url: Text
    sit_new_url: Text
    a_old_url: Text
    a_new_url: Text


class Email(BaseModel):
    send_user: Union[Text, None]
    email_host: Union[Text, None]
    stamp_key: Union[Text, None]
    # 收件人
    send_list: Union[Text, None]


class projectData(BaseModel):
    bar_project_name: list = None
    Address: Text = None
    direct: Text = None
    directMobile: Text = None
    business: Text = None
    directMobile: Text = None
    businessMobile: Text = None


class LoginData(BaseModel):
    user: list = None
    pwd: list = None


class UserData(BaseModel):
    mbrConsName: str
    contacter: str
    contacterMobile: str


class MeasureData(BaseModel):
    barMeasureNO: list
    commType: list
    gatewayNo: list
    collertorNo: list
    commProto: list


class Config(BaseModel):
    project_name: Text
    env: Text
    tester_name: Text
    notification_type: int = 0
    excel_report: bool
    ding_talk: "DingTalk"
    mysql_db: "MySqlDB"
    mirror_source: Text
    wechat: "Webhook"
    email: "Email"
    lark: "Webhook"
    real_time_update_test_cases: bool = False
    host: Text
    app_host: Union[Text, None]
    sit_ssh: "SitSsh"
    log: "Log"
    url: "Url"


class TestData(BaseModel):
    project_data: "projectData"
    login_data: "LoginData"
    user_data: "UserData"
    measure_data: "MeasureData"




