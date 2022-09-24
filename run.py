import os

import pytest
from Comm import *




def run(filename='\\IemsTestcase'):
    """

    :param filename:
        所有用例：不填
        整个文件夹下的用例：\\IemsTestcase\\sit
        一个模块下的用例: \\IemsTestcase\\sit\\sit_iems_eqp
        单个文件下的用例：\\IemsTestcase\\sit\\sit_iems_eqp\\test_eqp_sit.py
        单个用例：\\IemsTestcase\\sit\\sit_iems_eqp\\test_eqp_sit.py::TestIemsEqp::test_01_import_gateway
    :return:
    """
    # 从配置文件中获取项目名称
    try:
        log.Logger().info(
            """
                             _    _         _      _____         _
              __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
             / _` | '_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
            | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
             \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
                  |_|
                  开始执行{}项目...
                """
        )

        # os.system(f"python -m pytest {filename}")

        """
                   --reruns: 失败重跑次数
                   --count: 重复执行次数
                   -v: 显示错误位置以及错误的详细信息
                   -s: 等价于 pytest --capture=no 可以捕获print函数的输出
                   -q: 简化输出信息
                   -m: 运行指定标签的测试用例
                   -x: 一旦错误，则停止运行
                   --maxfail: 设置最大失败次数，当超出这个阈值时，则不会在执行测试用例
                    "--reruns=3", "--reruns-delay=2"
                    fi
                   """

        # os.system(r"allure generate ./Results/allure_reports -o ./Results/html --clean")


        allure_data = allure_report_data.AllureFileClean().get_case_count()

        log.Logger().info(allure_data)

        report = wechat_send.WeChatSend(allure_report_data.AllureFileClean().get_case_count()).report('py')

        log.Logger().info(report)


        wechat_send.WeChatSend(allure_report_data.AllureFileClean().get_case_count()).send_wechat_notification(report=report)

        # 程序运行之后，自动启动报告，如果不想启动报告，可注释这段代码
        os.system(f"allure serve ./Results/allure_reports -h 127.0.0.1 -p 9999")


    except :
        raise Exception
        # 如有异常，相关异常发送邮件
        # e = traceback.format_exc()
        # send_email = SendEmail(AllureFileClean.get_case_count())
        # send_email.error_mail(e)
        # raise


if __name__ == '__main__':
    filename = f'/IemsTestcase/sit/iems_project/test_iems_project_sit.py::TestIemsProjectSit::test_01_add_project'
    filename = get_path.ensure_path_sep(filename)
    run(filename)
    # os.system(f"allure serve ./Results/allure_reports -h 127.0.0.1 -p 9999")