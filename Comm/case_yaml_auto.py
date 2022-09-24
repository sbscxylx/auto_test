from Comm import *


def get_case_yaml_automatic(case_yaml) -> None:
    """
    生成测试用例yaml文件
    :param case_yaml: 模块+文件名称 '\\collect\\collect_edittool.yaml'
    :return:
    """

    test_cases = ['test_01', 'test_02']
    test_case_page = ''
    file_path = get_path.ensure_path_sep("\\data")
    file_path2 = get_path.get_all_files(file_path, yaml_data_switch=True)
    try:
        for file in file_path2:
            if case_yaml not in file:
                case_yaml = file_path + case_yaml
                for test_case in test_cases:
                    test_case_page = test_case_page + f'''{test_case}:
\tallureStory:
\tallureTitle:
\tallureStep: {{}}\n
'''
        testcase_template.write_case_yaml(
            case_path=case_yaml,
            allureSeverity='CRITICAL',
            allureFeature='测试采集器配置',
            test_case=test_case_page
        )
    except:
        print(f'{case_yaml}文件已存在')


if __name__ == '__main__':
    get_case_yaml_automatic('\\collect\\collect_edittool.yaml')