import pytest, time, pymysql, os
from py._xmlgen import html


# 设备类型
apptype = "ios"

# 版本号
version = "1.0"

# 设置失败重试次数
rerun = "1"

# 运行测试用例的目录或文件
cases_path = "./test_case"

# 接口响应时间list，单位毫秒
STRESS_LIST = []

# 接口执行结果list
RESULT_LIST = []


# 连接mysql数据库
@pytest.fixture(scope='session', autouse=True)
def sql_connect():
    global coon
    global cursor
    # 获取连接数据库
    coon = pymysql.connect(host="47.52.226.3", db="test_coinyee", user="coinyee", password="coinyee16888", port=3306,
                           database="coinyee", charset="utf8", autocommit=True)
    # 创建游标
    cursor = coon.cursor(cursor=pymysql.cursors.DictCursor)
    return cursor


# 从测试结果中获取测试报告
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    '''从测试结果中获取测试报告'''
    # 获取钩子函数的调用结果
    outcome = yield
    # 从钩子函数的调用结果中获取测试报告
    report = outcome.get_result()
    report.description = str(item.function.__doc__)  # 测试报告类型


# 测试报告填写字段Description
@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))



