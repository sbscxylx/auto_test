import csv
import pandas as pd

from Comm.path import ensure_path_sep
from Conf.readconfig import ReadConfig
import os


class ReadData:

    def __init__(self, file_name):
        self.file_name = file_name

    def read_csv(self, encoding='utf8'):
        data = []
        file_path = ReadConfig().get_file_path("path_name") + '/' + self.file_name
        f = open(file_path, mode='r', encoding=encoding)
        csv_data = csv.reader(f)
        for i in csv_data:
            data.append(tuple(i))
        f.close()
        return data

    def read_excel(self, **kwargs):
        data = []
        file_path = ReadConfig().get_file_path("data_path") + '/' + self.file_name
        try:
            excel_data = pd.read_excel(file_path, **kwargs)
            data = excel_data.to_dict('records')
        finally:
            return data




if __name__ == '__main__':
    # a = ReadData('../IemsTestcase/Testdata/test_login_data.xlsx').read_excel()
    # print(a)
    # r = GetPath().get_abs_path('../IemsTestcase/Testdata/test_login_data.xlsx')
    # print(r)
    # test_login_data = ReadData('test_login_data.xlsx').read_excel()
    # print(test_login_data)
    a = ReadData(ensure_path_sep("/Results/html/data/test-cases")).get_all_files()
    print(a)