from Comm import *
from Conf import *
import unittest
import warnings
import allure
import pytest
from IemsPage.basePage import *

_data = yaml_control.GetYamlData(get_path.ensure_path_sep("/IemsTestcase/Testdata/test_data.yaml")).get_yaml_data()
TestData = models.TestData(**_data)


if __name__ == '__main__':
    print(TestData.project_data)