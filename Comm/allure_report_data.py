import json
from typing import List, Text
from Comm.path import *
from Conf.models import TestMetrics


class AllureFileClean:
    """allure 报告数据清洗，提取业务需要得数据"""

    @classmethod
    def get_testcases(cls) -> List:
        """ 获取所有 allure 报告中执行用例的情况"""
        # 将所有数据都收集到files中
        files = []
        for i in get_all_files(ensure_path_sep("\\Results\\html2\\data\\test-cases")):
            # print(i)
            with open(i, 'r', encoding='utf-8') as file:
                date = json.load(file)
                files.append(date)
        return files

    def get_failed_case(self) -> List:
        """ 获取到所有失败的用例标题和用例代码路径"""
        error_case = []
        for i in self.get_testcases():
            if i['status'] == 'failed' or i['status'] == 'broken':
                error_case.append((i['name'], i['fullName']))
        return error_case

    def get_failed_cases_detail(self) -> Text:
        """ 返回所有失败的测试用例相关内容 """
        date = self.get_failed_case()
        values = ""
        # 判断有失败用例，则返回内容
        if len(date) >= 1:
            values = "失败用例:\n"
            values += "        **********************************\n"
            for i in date:
                values += "        " + i[0] + ":" + i[1] + "\n"
        return values

    @classmethod
    def get_case_count(cls) -> "TestMetrics":
        """ 统计用例数量 """
        try:
            file_name = ensure_path_sep("\\Results\\html2\\widgets\\summary.json")
            # print(file_name)
            with open(file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # print(data)
            _case_count = data['statistic']
            # print(_case_count)
            _time = data['time']
            # print(_time)
            keep_keys = {"passed", "failed", "broken", "skipped", "total"}
            # print(data['statistic'].items())
            # run_case_data = {}
            # for key, value in data['statistic'].items():
            #     if key in keep_keys:
            #         run_case_data[key] = value
            # print(run_case_data)
            run_case_data = {k: v for k, v in data['statistic'].items() if k in keep_keys}
            # print(run_case_data)
            # 判断运行用例总数大于0
            if _case_count["total"] > 0:
                # 计算用例成功率
                run_case_data["pass_rate"] = round(
                    (_case_count["passed"] + _case_count["skipped"]) / _case_count["total"] * 100, 2
                )
            else:
                # 如果未运行用例，则成功率为 0.0
                run_case_data["pass_rate"] = 0.0
            # 收集用例运行时长
            # print(run_case_data)
            run_case_data['time'] = _time if run_case_data['total'] == 0 else round(_time['duration'] / 1000, 2)
            # print(run_case_data)
            return TestMetrics(**run_case_data)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                "程序中检查到您未生成allure报告，"
            ) from exc


if __name__ == '__main__':
    a = AllureFileClean().get_testcases()
    b = AllureFileClean().get_failed_case()
    c = AllureFileClean().get_failed_cases_detail()
    d = AllureFileClean().get_case_count()
    print(d)